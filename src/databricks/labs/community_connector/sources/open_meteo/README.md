# Lakeflow Open-Meteo Community Connector

This documentation provides setup instructions and reference information for the Open-Meteo source connector.

## Prerequisites

- A Databricks workspace with Unity Catalog enabled.
- The geographic coordinates (latitude and longitude) of the location you want to fetch weather forecasts for.
- (Optional) An API key from [Open-Meteo](https://open-meteo.com/) if you are using a commercial subscription. The free tier requires no authentication and is available for non-commercial use under the CC-BY 4.0 license.

## Setup

### Required Connection Parameters

To configure the connector, provide the following parameters in your connector options:

| Parameter | Type | Required | Description | Example |
|---|---|---|---|---|
| `latitude` | String | Yes | Geographic latitude in decimal degrees (WGS84) for the forecast location. | `"52.52"` |
| `longitude` | String | Yes | Geographic longitude in decimal degrees (WGS84) for the forecast location. | `"13.41"` |
| `apikey` | String | No | API key for commercial Open-Meteo subscriptions. Omit for free tier (non-commercial use). When provided, requests are routed to the commercial API endpoint. | `"your-api-key"` |
| `externalOptionsAllowList` | String | Yes | A comma-separated list of table-specific options that can be configured per table. Must be set to: `forecast_days,timezone,temperature_unit,wind_speed_unit,precipitation_unit,models,hourly_variables,daily_variables` | `"forecast_days,timezone,temperature_unit,wind_speed_unit,precipitation_unit,models,hourly_variables,daily_variables"` |

### Obtaining Coordinates

You can find the latitude and longitude for any location using:
- [Open-Meteo's Geocoding API](https://open-meteo.com/en/docs/geocoding-api) to search by city name.
- Any mapping service such as Google Maps (right-click a point on the map to copy coordinates).

### Obtaining an API Key (Commercial Use Only)

If you need higher rate limits or are using the data for commercial purposes, sign up for a commercial plan at [open-meteo.com](https://open-meteo.com/en/pricing). Your API key will be provided after subscribing. For non-commercial use, no API key is needed.

### Create a Unity Catalog Connection

A Unity Catalog connection for this connector can be created in two ways:

**Via the UI:**
1. Follow the Lakeflow Community Connector UI flow from the "Add Data" page.
2. Select any existing Lakeflow Community Connector connection for this source or create a new one.
3. Set `externalOptionsAllowList` to `forecast_days,timezone,temperature_unit,wind_speed_unit,precipitation_unit,models,hourly_variables,daily_variables` so that these options can be configured per table.

**Via SQL:**
```sql
CREATE CONNECTION `open-meteo` TYPE lakeflow_community
OPTIONS (
  latitude = '52.52',
  longitude = '13.41',
  externalOptionsAllowList = 'forecast_days,timezone,temperature_unit,wind_speed_unit,precipitation_unit,models,hourly_variables,daily_variables'
);
```

To update an existing connection (e.g., to change coordinates):
```sql
ALTER CONNECTION `open-meteo` SET OPTIONS (
  latitude = '48.8566',
  longitude = '2.3522'
);
```


## Supported Objects

This connector provides two tables, both ingested as **snapshots** (the full forecast window is replaced on each pipeline run):

| Table Name | Description | Ingestion Type |
|---|---|---|
| `hourly_forecast` | Hourly weather forecast data. Each row represents one hour at the configured location. | Snapshot |
| `daily_forecast` | Daily aggregated weather forecast data. Each row represents one day at the configured location. | Snapshot |

**Primary keys** for both tables: `latitude`, `longitude`, `time`

- `latitude` and `longitude` identify the resolved grid point returned by the API.
- `time` contains an ISO 8601 timestamp (`"2026-04-10T14:00"` for hourly, `"2026-04-10"` for daily).

Because these tables use snapshot ingestion, every pipeline run fetches the complete forecast window and replaces the previous data. There is no incremental or CDC mechanism. Delete synchronization is not applicable.

Each table also includes metadata columns such as `elevation`, `timezone`, `timezone_abbreviation`, `utc_offset_seconds`, and `generationtime_ms`.

### hourly_forecast

Returns one row per hour with weather variables such as temperature, humidity, precipitation, wind speed, cloud cover, UV index, solar radiation, soil conditions, and atmospheric stability indicators. The default set of variables fetched includes: `temperature_2m`, `relative_humidity_2m`, `dew_point_2m`, `apparent_temperature`, `precipitation_probability`, `precipitation`, `rain`, `snowfall`, `weather_code`, `cloud_cover`, `wind_speed_10m`, `wind_direction_10m`, `wind_gusts_10m`, `visibility`, and `uv_index`. You can customize which variables are fetched using the `hourly_variables` table option.

### daily_forecast

Returns one row per day with aggregated weather variables such as max/min/mean temperatures, sunrise/sunset times, precipitation totals, wind speed extremes, UV index, and more. The default set of variables fetched includes: `weather_code`, `temperature_2m_max`, `temperature_2m_min`, `apparent_temperature_max`, `apparent_temperature_min`, `sunrise`, `sunset`, `precipitation_sum`, `rain_sum`, `snowfall_sum`, `precipitation_probability_max`, `wind_speed_10m_max`, `wind_gusts_10m_max`, `wind_direction_10m_dominant`, and `uv_index_max`. You can customize which variables are fetched using the `daily_variables` table option.


## Table Configurations

### Source & Destination

These are set directly under each `table` object in the pipeline spec:

| Option | Required | Description |
|---|---|---|
| `source_table` | Yes | Table name in the source system. Must be `hourly_forecast` or `daily_forecast`. |
| `destination_catalog` | No | Target catalog (defaults to pipeline's default) |
| `destination_schema` | No | Target schema (defaults to pipeline's default) |
| `destination_table` | No | Target table name (defaults to `source_table`) |

### Common `table_configuration` options

These are set inside the `table_configuration` map alongside any source-specific options:

| Option | Required | Description |
|---|---|---|
| `scd_type` | No | `SCD_TYPE_1` (default) or `SCD_TYPE_2`. Only applicable to tables with CDC or SNAPSHOT ingestion mode; APPEND_ONLY tables do not support this option. |
| `primary_keys` | No | List of columns to override the connector's default primary keys |
| `sequence_by` | No | Column used to order records for SCD Type 2 change tracking |

### Special `table_configuration` Options

The following options can be set per table in the `table_configuration` map. These must be included in the `externalOptionsAllowList` connection parameter.

| Option | Required | Default | Description |
|---|---|---|---|
| `forecast_days` | No | `7` | Number of forecast days to retrieve (1-16). |
| `timezone` | No | `GMT` | Timezone for time values. Use an IANA timezone name (e.g., `Europe/Berlin`) or `auto` for automatic detection. |
| `temperature_unit` | No | `celsius` | Unit for temperature values. Options: `celsius`, `fahrenheit`. |
| `wind_speed_unit` | No | `kmh` | Unit for wind speed values. Options: `kmh`, `ms`, `mph`, `kn`. |
| `precipitation_unit` | No | `mm` | Unit for precipitation values. Options: `mm`, `inch`. |
| `models` | No | `best_match` | Weather model to use for forecasts. The default (`best_match`) automatically selects the best available model for the location. See the [Open-Meteo documentation](https://open-meteo.com/en/docs) for the full list of available models. |
| `hourly_variables` | No | See below | Comma-separated list of hourly weather variable names to fetch. Only applies to the `hourly_forecast` table. When omitted, a default set of common variables is used. |
| `daily_variables` | No | See below | Comma-separated list of daily weather variable names to fetch. Only applies to the `daily_forecast` table. When omitted, a default set of common variables is used. |


## Data Type Mapping

The following table describes how Open-Meteo API data types are mapped to Spark/Databricks types in the ingested tables:

| Open-Meteo API Type | Databricks Type | Examples |
|---|---|---|
| Float | DoubleType | `latitude`, `longitude`, `elevation`, `temperature_2m`, `precipitation` |
| Integer | LongType | `relative_humidity_2m`, `weather_code`, `cloud_cover`, `wind_direction_10m`, `utc_offset_seconds` |
| String | StringType | `time`, `timezone`, `timezone_abbreviation`, `sunrise`, `sunset` |


## How to Run

### Step 1: Clone/Copy the Source Connector Code
Follow the Lakeflow Community Connector UI, which will guide you through setting up a pipeline using the selected source connector code.

### Step 2: Configure Your Pipeline
1. Update the `pipeline_spec` in the main pipeline file (e.g., `ingest.py`).
2. Set the `source_table` to either `hourly_forecast` or `daily_forecast` for each table you want to ingest. Use the `table_configuration` map to customize forecast options per table.

```python
pipeline_spec = {
    "connection_name": "open-meteo",
    "objects": [
        {
            "table": {
                "source_table": "hourly_forecast",
                "destination_table": "open_meteo_hourly_forecast",
                "table_configuration": {
                    "forecast_days": "3",
                    "timezone": "auto",
                    "hourly_variables": "temperature_2m,precipitation,wind_speed_10m"
                }
            }
        },
        {
            "table": {
                "source_table": "daily_forecast",
                "destination_table": "open_meteo_daily_forecast",
                "table_configuration": {
                    "forecast_days": "7",
                    "timezone": "auto",
                    "daily_variables": "temperature_2m_max,temperature_2m_min,precipitation_sum"
                }
            }
        }
    ],
}
```

3. (Optional) Customize the source connector code if needed for special use cases.

### Step 3: Run and Schedule the Pipeline

#### Best Practices

- **Start Small**: Begin by syncing a single table (e.g., `daily_forecast`) with the default variables to verify your pipeline works correctly.
- **Customize Variables**: Only request the weather variables you need. Requesting fewer variables reduces response size and API usage.
- **Set Appropriate Schedules**: Forecast data updates frequently (typically every 1-6 hours depending on the model). Schedule your pipeline accordingly to balance data freshness with API usage.
- **Mind Rate Limits (Free Tier)**: The free tier is limited to 600 calls per minute, 5,000 per hour, and 10,000 per day. Requests with more than 10 weather variables or spanning more than 2 weeks count as multiple API calls.

#### Troubleshooting

**Common Issues:**

- **Invalid variable name**: If you specify a variable name in `hourly_variables` or `daily_variables` that the API does not recognize, the pipeline will fail with an error message from the Open-Meteo API. Double-check variable names against the [Open-Meteo Forecast API documentation](https://open-meteo.com/en/docs).
- **Rate limiting (HTTP 429)**: The connector automatically retries on rate-limit responses with exponential backoff. If you consistently hit rate limits on the free tier, consider reducing your pipeline frequency or upgrading to a commercial plan.
- **Empty results**: Ensure that at least one weather variable is being requested. If both `hourly_variables` and `daily_variables` are left empty for a table, the API may return no data.
- **Incorrect coordinates**: The API resolves coordinates to the nearest grid point. If your results seem wrong, verify that your latitude and longitude values are correct and in decimal degrees.


## References

- [Open-Meteo Forecast API Documentation](https://open-meteo.com/en/docs)
- [Open-Meteo Geocoding API](https://open-meteo.com/en/docs/geocoding-api)
- [Open-Meteo Pricing (Commercial Plans)](https://open-meteo.com/en/pricing)
- [Open-Meteo GitHub Repository](https://github.com/open-meteo/open-meteo)
