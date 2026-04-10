"""Open-Meteo Forecast connector for LakeflowConnect.

Fetches hourly and daily weather forecast data from the Open-Meteo API
(https://open-meteo.com/) and exposes it as two snapshot tables:
``hourly_forecast`` and ``daily_forecast``.
"""

import logging
import time
from typing import Iterator

import requests
from pyspark.sql.types import StructType

from lakeflow_connect_interface import LakeflowConnect
from open_meteo_schemas import (
    DAILY_FORECAST_SCHEMA,
    DEFAULT_DAILY_VARIABLES,
    DEFAULT_HOURLY_VARIABLES,
    HOURLY_FORECAST_SCHEMA,
    INITIAL_BACKOFF,
    MAX_RETRIES,
    RETRIABLE_STATUS_CODES,
)

logger = logging.getLogger(__name__)

_SUPPORTED_TABLES = ["hourly_forecast", "daily_forecast"]

# Maps table name -> API response section key
_TABLE_SECTION_MAP = {
    "hourly_forecast": "hourly",
    "daily_forecast": "daily",
}


class OpenMeteoLakeflowConnect(LakeflowConnect):
    """LakeflowConnect implementation for the Open-Meteo Forecast API."""

    def __init__(self, options: dict[str, str]) -> None:
        super().__init__(options)
        self._latitude = options["latitude"]
        self._longitude = options["longitude"]
        self._apikey = options.get("apikey")

        if self._apikey:
            self._base_url = "https://customer-api.open-meteo.com/v1/forecast"
        else:
            self._base_url = "https://api.open-meteo.com/v1/forecast"

    # ------------------------------------------------------------------
    # HTTP helpers
    # ------------------------------------------------------------------

    def _request_with_retry(self, params: dict) -> requests.Response:
        """Issue a GET request to the Open-Meteo API with exponential-backoff retry."""
        backoff = INITIAL_BACKOFF
        resp = None
        for attempt in range(MAX_RETRIES):
            resp = requests.get(self._base_url, params=params, timeout=20)

            if resp.status_code not in RETRIABLE_STATUS_CODES:
                return resp

            if attempt < MAX_RETRIES - 1:
                logger.warning(
                    "Open-Meteo API returned %s on attempt %d/%d, retrying in %.1fs",
                    resp.status_code,
                    attempt + 1,
                    MAX_RETRIES,
                    backoff,
                )
                time.sleep(backoff)
                backoff *= 2

        return resp  # type: ignore[return-value]

    # ------------------------------------------------------------------
    # LakeflowConnect interface
    # ------------------------------------------------------------------

    def list_tables(self) -> list[str]:
        """Return the static list of supported tables."""
        return list(_SUPPORTED_TABLES)

    def get_table_schema(
        self, table_name: str, table_options: dict[str, str]
    ) -> StructType:
        """Return the full static schema for the requested table."""
        self._validate_table(table_name)
        if table_name == "hourly_forecast":
            return HOURLY_FORECAST_SCHEMA
        return DAILY_FORECAST_SCHEMA

    def read_table_metadata(
        self, table_name: str, table_options: dict[str, str]
    ) -> dict:
        """Return snapshot metadata with composite primary keys."""
        self._validate_table(table_name)
        return {
            "primary_keys": ["latitude", "longitude", "time"],
            "ingestion_type": "snapshot",
        }

    def read_table(
        self, table_name: str, start_offset: dict, table_options: dict[str, str]
    ) -> tuple[Iterator[dict], dict]:
        """Fetch forecast data and return row-oriented dicts.

        The Open-Meteo API returns parallel arrays; this method pivots them
        into one dict per timestep, injecting top-level metadata fields into
        each row.
        """
        self._validate_table(table_name)

        section_key = _TABLE_SECTION_MAP[table_name]

        # Determine which weather variables to request
        variables = self._resolve_variables(table_name, table_options)

        # Build query params
        params = self._build_params(section_key, variables, table_options)

        # Call the API
        resp = self._request_with_retry(params)

        if resp.status_code != 200:
            raise RuntimeError(
                f"Open-Meteo API error (HTTP {resp.status_code}): {resp.text}"
            )

        body = resp.json()

        # The API returns {"error": true, "reason": "..."} on logical errors
        if body.get("error"):
            raise RuntimeError(f"Open-Meteo API error: {body.get('reason', body)}")

        section_data = body.get(section_key, {})
        rows = self._pivot_to_rows(body, section_data, variables)

        return iter(rows), {}

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _validate_table(self, table_name: str) -> None:
        if table_name not in _SUPPORTED_TABLES:
            raise ValueError(
                f"Table '{table_name}' is not supported. "
                f"Supported tables: {_SUPPORTED_TABLES}"
            )

    def _resolve_variables(
        self, table_name: str, table_options: dict[str, str]
    ) -> list[str]:
        """Determine the list of weather variables to request.

        Users can override via ``hourly_variables`` or ``daily_variables`` in
        table_options (comma-separated).  Falls back to the default list.
        """
        if table_name == "hourly_forecast":
            opt_key = "hourly_variables"
            defaults = DEFAULT_HOURLY_VARIABLES
        else:
            opt_key = "daily_variables"
            defaults = DEFAULT_DAILY_VARIABLES

        raw = table_options.get(opt_key, "")
        if raw.strip():
            return [v.strip() for v in raw.split(",") if v.strip()]
        return list(defaults)

    def _build_params(
        self,
        section_key: str,
        variables: list[str],
        table_options: dict[str, str],
    ) -> dict:
        """Assemble query parameters for the API request."""
        params: dict[str, str] = {
            "latitude": self._latitude,
            "longitude": self._longitude,
            section_key: ",".join(variables),
        }

        # Optional parameters forwarded from table_options
        for opt_key in (
            "forecast_days",
            "timezone",
            "temperature_unit",
            "wind_speed_unit",
            "precipitation_unit",
            "models",
        ):
            value = table_options.get(opt_key, "")
            if value.strip():
                params[opt_key] = value.strip()

        # API key (from connection options)
        if self._apikey:
            params["apikey"] = self._apikey

        return params

    def _pivot_to_rows(
        self,
        body: dict,
        section_data: dict,
        variables: list[str],
    ) -> list[dict]:
        """Convert the parallel-array response into row-oriented dicts.

        Each row includes the top-level metadata fields plus one timestep's
        values for all requested variables.
        """
        time_values = section_data.get("time", [])
        if not time_values:
            return []

        # Extract top-level metadata once
        metadata = {
            "latitude": body.get("latitude"),
            "longitude": body.get("longitude"),
            "elevation": body.get("elevation"),
            "timezone": body.get("timezone"),
            "timezone_abbreviation": body.get("timezone_abbreviation"),
            "utc_offset_seconds": body.get("utc_offset_seconds"),
            "generationtime_ms": body.get("generationtime_ms"),
        }

        num_rows = len(time_values)
        rows: list[dict] = []

        for i in range(num_rows):
            row = dict(metadata)
            row["time"] = time_values[i]
            for var in variables:
                values = section_data.get(var)
                if values is not None and i < len(values):
                    row[var] = values[i]
                else:
                    row[var] = None
            rows.append(row)

        return rows
