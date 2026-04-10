"""Schemas and constants for the Open-Meteo Forecast connector.

Defines static Spark schemas for the ``hourly_forecast`` and ``daily_forecast``
tables, default variable lists, and retry configuration.
"""

from pyspark.sql.types import (
    DoubleType,
    LongType,
    StringType,
    StructField,
    StructType,
)

# ---------------------------------------------------------------------------
# Retry / HTTP constants
# ---------------------------------------------------------------------------
RETRIABLE_STATUS_CODES = {429, 500, 503}
MAX_RETRIES = 5
INITIAL_BACKOFF = 1.0  # seconds; doubled after each retry

# ---------------------------------------------------------------------------
# Metadata fields (present in every API response, injected into each row)
# ---------------------------------------------------------------------------
_METADATA_FIELDS = [
    StructField("latitude", DoubleType(), nullable=False),
    StructField("longitude", DoubleType(), nullable=False),
    StructField("elevation", DoubleType(), nullable=True),
    StructField("timezone", StringType(), nullable=True),
    StructField("timezone_abbreviation", StringType(), nullable=True),
    StructField("utc_offset_seconds", LongType(), nullable=True),
    StructField("generationtime_ms", DoubleType(), nullable=True),
]

# ---------------------------------------------------------------------------
# hourly_forecast schema
# ---------------------------------------------------------------------------
HOURLY_FORECAST_SCHEMA = StructType(
    _METADATA_FIELDS
    + [
        # time (primary key component)
        StructField("time", StringType(), nullable=False),
        # Core temperature & humidity
        StructField("temperature_2m", DoubleType(), nullable=True),
        StructField("relative_humidity_2m", LongType(), nullable=True),
        StructField("dew_point_2m", DoubleType(), nullable=True),
        StructField("apparent_temperature", DoubleType(), nullable=True),
        # Precipitation
        StructField("precipitation_probability", LongType(), nullable=True),
        StructField("precipitation", DoubleType(), nullable=True),
        StructField("rain", DoubleType(), nullable=True),
        StructField("showers", DoubleType(), nullable=True),
        StructField("snowfall", DoubleType(), nullable=True),
        StructField("snow_depth", DoubleType(), nullable=True),
        # Weather code
        StructField("weather_code", LongType(), nullable=True),
        # Pressure
        StructField("pressure_msl", DoubleType(), nullable=True),
        StructField("surface_pressure", DoubleType(), nullable=True),
        # Cloud cover
        StructField("cloud_cover", LongType(), nullable=True),
        StructField("cloud_cover_low", LongType(), nullable=True),
        StructField("cloud_cover_mid", LongType(), nullable=True),
        StructField("cloud_cover_high", LongType(), nullable=True),
        # Visibility
        StructField("visibility", DoubleType(), nullable=True),
        # Evapotranspiration
        StructField("evapotranspiration", DoubleType(), nullable=True),
        StructField("et0_fao_evapotranspiration", DoubleType(), nullable=True),
        StructField("vapour_pressure_deficit", DoubleType(), nullable=True),
        # Wind (10 m)
        StructField("wind_speed_10m", DoubleType(), nullable=True),
        StructField("wind_speed_80m", DoubleType(), nullable=True),
        StructField("wind_speed_120m", DoubleType(), nullable=True),
        StructField("wind_speed_180m", DoubleType(), nullable=True),
        StructField("wind_direction_10m", LongType(), nullable=True),
        StructField("wind_direction_80m", LongType(), nullable=True),
        StructField("wind_direction_120m", LongType(), nullable=True),
        StructField("wind_direction_180m", LongType(), nullable=True),
        StructField("wind_gusts_10m", DoubleType(), nullable=True),
        # Temperature at altitude
        StructField("temperature_80m", DoubleType(), nullable=True),
        StructField("temperature_120m", DoubleType(), nullable=True),
        StructField("temperature_180m", DoubleType(), nullable=True),
        # Soil
        StructField("soil_temperature_0cm", DoubleType(), nullable=True),
        StructField("soil_temperature_6cm", DoubleType(), nullable=True),
        StructField("soil_temperature_18cm", DoubleType(), nullable=True),
        StructField("soil_temperature_54cm", DoubleType(), nullable=True),
        StructField("soil_moisture_0_to_1cm", DoubleType(), nullable=True),
        StructField("soil_moisture_1_to_3cm", DoubleType(), nullable=True),
        StructField("soil_moisture_3_to_9cm", DoubleType(), nullable=True),
        StructField("soil_moisture_9_to_27cm", DoubleType(), nullable=True),
        StructField("soil_moisture_27_to_81cm", DoubleType(), nullable=True),
        # Surface & atmospheric stability
        StructField("surface_temperature", DoubleType(), nullable=True),
        StructField("cape", DoubleType(), nullable=True),
        StructField("lifted_index", DoubleType(), nullable=True),
        StructField("convective_inhibition", DoubleType(), nullable=True),
        StructField("freezing_level_height", DoubleType(), nullable=True),
        StructField("boundary_layer_height", DoubleType(), nullable=True),
        # Day/night
        StructField("is_day", LongType(), nullable=True),
        # Sunshine & radiation
        StructField("sunshine_duration", DoubleType(), nullable=True),
        StructField("shortwave_radiation", DoubleType(), nullable=True),
        StructField("direct_radiation", DoubleType(), nullable=True),
        StructField("diffuse_radiation", DoubleType(), nullable=True),
        StructField("direct_normal_irradiance", DoubleType(), nullable=True),
        StructField("global_tilted_irradiance", DoubleType(), nullable=True),
        StructField("terrestrial_radiation", DoubleType(), nullable=True),
        StructField("shortwave_radiation_instant", DoubleType(), nullable=True),
        StructField("direct_radiation_instant", DoubleType(), nullable=True),
        StructField("diffuse_radiation_instant", DoubleType(), nullable=True),
        StructField("direct_normal_irradiance_instant", DoubleType(), nullable=True),
        StructField("global_tilted_irradiance_instant", DoubleType(), nullable=True),
        StructField("terrestrial_radiation_instant", DoubleType(), nullable=True),
        # UV
        StructField("uv_index", DoubleType(), nullable=True),
        StructField("uv_index_clear_sky", DoubleType(), nullable=True),
        # Misc
        StructField("wet_bulb_temperature_2m", DoubleType(), nullable=True),
        StructField("lightning_potential", DoubleType(), nullable=True),
        StructField("total_column_integrated_water_vapour", DoubleType(), nullable=True),
        StructField("snowfall_height", DoubleType(), nullable=True),
    ]
)

# ---------------------------------------------------------------------------
# daily_forecast schema
# ---------------------------------------------------------------------------
DAILY_FORECAST_SCHEMA = StructType(
    _METADATA_FIELDS
    + [
        # time (primary key component)
        StructField("time", StringType(), nullable=False),
        # Weather code
        StructField("weather_code", LongType(), nullable=True),
        # Temperature
        StructField("temperature_2m_max", DoubleType(), nullable=True),
        StructField("temperature_2m_min", DoubleType(), nullable=True),
        StructField("temperature_2m_mean", DoubleType(), nullable=True),
        StructField("apparent_temperature_max", DoubleType(), nullable=True),
        StructField("apparent_temperature_min", DoubleType(), nullable=True),
        StructField("apparent_temperature_mean", DoubleType(), nullable=True),
        # Sun
        StructField("sunrise", StringType(), nullable=True),
        StructField("sunset", StringType(), nullable=True),
        StructField("daylight_duration", DoubleType(), nullable=True),
        StructField("sunshine_duration", DoubleType(), nullable=True),
        # UV
        StructField("uv_index_max", DoubleType(), nullable=True),
        StructField("uv_index_clear_sky_max", DoubleType(), nullable=True),
        # Precipitation
        StructField("precipitation_sum", DoubleType(), nullable=True),
        StructField("rain_sum", DoubleType(), nullable=True),
        StructField("showers_sum", DoubleType(), nullable=True),
        StructField("snowfall_sum", DoubleType(), nullable=True),
        StructField("snowfall_water_equivalent_sum", DoubleType(), nullable=True),
        StructField("precipitation_hours", DoubleType(), nullable=True),
        StructField("precipitation_probability_max", LongType(), nullable=True),
        StructField("precipitation_probability_min", LongType(), nullable=True),
        StructField("precipitation_probability_mean", LongType(), nullable=True),
        # Wind
        StructField("wind_speed_10m_max", DoubleType(), nullable=True),
        StructField("wind_speed_10m_mean", DoubleType(), nullable=True),
        StructField("wind_speed_10m_min", DoubleType(), nullable=True),
        StructField("wind_gusts_10m_max", DoubleType(), nullable=True),
        StructField("wind_gusts_10m_mean", DoubleType(), nullable=True),
        StructField("wind_gusts_10m_min", DoubleType(), nullable=True),
        StructField("wind_direction_10m_dominant", LongType(), nullable=True),
        # Radiation
        StructField("shortwave_radiation_sum", DoubleType(), nullable=True),
        StructField("et0_fao_evapotranspiration", DoubleType(), nullable=True),
        # Dew point
        StructField("dew_point_2m_max", DoubleType(), nullable=True),
        StructField("dew_point_2m_min", DoubleType(), nullable=True),
        StructField("dew_point_2m_mean", DoubleType(), nullable=True),
        # Humidity
        StructField("relative_humidity_2m_max", LongType(), nullable=True),
        StructField("relative_humidity_2m_min", LongType(), nullable=True),
        StructField("relative_humidity_2m_mean", LongType(), nullable=True),
        # Pressure
        StructField("pressure_msl_max", DoubleType(), nullable=True),
        StructField("pressure_msl_min", DoubleType(), nullable=True),
        StructField("pressure_msl_mean", DoubleType(), nullable=True),
        StructField("surface_pressure_max", DoubleType(), nullable=True),
        StructField("surface_pressure_min", DoubleType(), nullable=True),
        StructField("surface_pressure_mean", DoubleType(), nullable=True),
        # Cloud cover
        StructField("cloud_cover_max", LongType(), nullable=True),
        StructField("cloud_cover_min", LongType(), nullable=True),
        StructField("cloud_cover_mean", LongType(), nullable=True),
        # Visibility
        StructField("visibility_max", DoubleType(), nullable=True),
        StructField("visibility_min", DoubleType(), nullable=True),
        StructField("visibility_mean", DoubleType(), nullable=True),
        # Vapour pressure deficit
        StructField("vapour_pressure_deficit_max", DoubleType(), nullable=True),
        # Wet bulb
        StructField("wet_bulb_temperature_2m_max", DoubleType(), nullable=True),
        StructField("wet_bulb_temperature_2m_min", DoubleType(), nullable=True),
        StructField("wet_bulb_temperature_2m_mean", DoubleType(), nullable=True),
        # CAPE
        StructField("cape_max", DoubleType(), nullable=True),
        StructField("cape_min", DoubleType(), nullable=True),
        StructField("cape_mean", DoubleType(), nullable=True),
        # Updraft
        StructField("updraft_max", DoubleType(), nullable=True),
    ]
)

# ---------------------------------------------------------------------------
# Default variable subsets (sensible defaults when the user does not specify)
# ---------------------------------------------------------------------------
DEFAULT_HOURLY_VARIABLES = [
    "temperature_2m",
    "relative_humidity_2m",
    "dew_point_2m",
    "apparent_temperature",
    "precipitation_probability",
    "precipitation",
    "rain",
    "snowfall",
    "weather_code",
    "cloud_cover",
    "wind_speed_10m",
    "wind_direction_10m",
    "wind_gusts_10m",
    "visibility",
    "uv_index",
]

DEFAULT_DAILY_VARIABLES = [
    "weather_code",
    "temperature_2m_max",
    "temperature_2m_min",
    "apparent_temperature_max",
    "apparent_temperature_min",
    "sunrise",
    "sunset",
    "precipitation_sum",
    "rain_sum",
    "snowfall_sum",
    "precipitation_probability_max",
    "wind_speed_10m_max",
    "wind_gusts_10m_max",
    "wind_direction_10m_dominant",
    "uv_index_max",
]
