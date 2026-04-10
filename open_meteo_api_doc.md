# Open-Meteo Forecast API Documentation

## Authorization

- **Auth method (free tier)**: No authentication required. The free API is open to everyone for non-commercial use.
- **Auth method (commercial)**: API key passed as a query parameter `&apikey=<your_key>`. Commercial API uses distinct domains such as `customer-api.open-meteo.com`.
- **Free tier terms**: Limited to non-commercial use under CC-BY 4.0 license.
- **Free tier rate limits**:
  - 600 API calls per minute
  - 5,000 API calls per hour
  - 10,000 API calls per day
  - ~300,000 API calls per month
- **Commercial tier rate limits**: Unlimited (varies by plan: Standard, Professional, etc.)

### Connection Parameters

| Parameter | Type   | Required | Default | Description                                                                 |
|-----------|--------|----------|---------|-----------------------------------------------------------------------------|
| `apikey`  | string | No       | (none)  | API key for commercial subscriptions. Omit for free tier (non-commercial).  |

**Notes**:
- The free API and commercial API share identical syntax; the only differences are the domain (`api.open-meteo.com` vs `customer-api.open-meteo.com`) and the `&apikey=` query parameter.
- Requests selecting more than 10 weather variables or spanning more than 2 weeks for a single location are counted as multiple API calls.
- Data is provided under the CC-BY 4.0 license.

---

## Object List

The Open-Meteo Forecast API returns weather data in a single JSON response. Two logical tables can be extracted:

| Table Name         | API Response Section | Description                              | Ingestion Type |
|--------------------|----------------------|------------------------------------------|----------------|
| `hourly_forecast`  | `hourly`             | Hourly weather forecast variables         | `snapshot`     |
| `daily_forecast`   | `daily`              | Daily aggregated weather forecast variables | `snapshot`   |

Both tables are requested from the same endpoint (`GET /v1/forecast`) by specifying the `hourly` and/or `daily` query parameters with comma-separated variable names.

The object list is **static** (hard-coded) -- the API does not have a discovery endpoint for listing available tables.

---

## Object Schema

### Metadata Fields (present in all responses)

These top-level fields are returned with every API response and should be included as columns in both tables:

| Field                     | JSON Type | Description                                                  |
|---------------------------|-----------|--------------------------------------------------------------|
| `latitude`                | Float     | Resolved latitude of the nearest grid point (WGS84)         |
| `longitude`               | Float     | Resolved longitude of the nearest grid point (WGS84)        |
| `elevation`               | Float     | Elevation of the grid point in meters above sea level        |
| `generationtime_ms`       | Float     | Time taken to generate the response in milliseconds          |
| `utc_offset_seconds`      | Integer   | UTC offset in seconds based on the `timezone` parameter      |
| `timezone`                | String    | Timezone name (e.g., "GMT", "Europe/Berlin")                 |
| `timezone_abbreviation`   | String    | Timezone abbreviation (e.g., "GMT", "GMT+2")                 |

### hourly_forecast

Each row represents one hour at one location. The `time` array contains ISO 8601 timestamps (e.g., `"2026-04-10T00:00"`), and each variable is a parallel array of values.

**Primary Key**: `latitude`, `longitude`, `time`

#### Hourly Weather Variables

| Variable Name                        | Unit       | JSON Type | Description                                                        |
|--------------------------------------|------------|-----------|--------------------------------------------------------------------|
| `time`                               | iso8601    | String    | Timestamp for each hourly step (e.g., "2026-04-10T00:00")         |
| `temperature_2m`                     | C          | Float     | Air temperature at 2 meters above ground                          |
| `relative_humidity_2m`               | %          | Integer   | Relative humidity at 2 meters above ground                        |
| `dew_point_2m`                       | C          | Float     | Dew point temperature at 2 meters above ground                    |
| `apparent_temperature`               | C          | Float     | Perceived temperature combining wind chill and heat index          |
| `precipitation_probability`          | %          | Integer   | Probability of precipitation                                       |
| `precipitation`                      | mm         | Float     | Total precipitation (rain + showers + snowfall)                    |
| `rain`                               | mm         | Float     | Rain from large-scale weather systems                              |
| `showers`                            | mm         | Float     | Showers from convective precipitation                              |
| `snowfall`                           | cm         | Float     | Snowfall amount                                                    |
| `snow_depth`                         | m          | Float     | Snow depth on the ground                                           |
| `weather_code`                       | wmo code   | Integer   | WMO weather interpretation code                                    |
| `pressure_msl`                       | hPa        | Float     | Atmospheric pressure at mean sea level                             |
| `surface_pressure`                   | hPa        | Float     | Atmospheric pressure at surface level                              |
| `cloud_cover`                        | %          | Integer   | Total cloud cover as percentage                                    |
| `cloud_cover_low`                    | %          | Integer   | Low-level cloud cover (below ~2 km)                                |
| `cloud_cover_mid`                    | %          | Integer   | Mid-level cloud cover (~2-6 km)                                    |
| `cloud_cover_high`                   | %          | Integer   | High-level cloud cover (above ~6 km)                               |
| `visibility`                         | m          | Float     | Viewing distance in meters                                         |
| `evapotranspiration`                 | mm         | Float     | Evapotranspiration from land surface and plants                    |
| `et0_fao_evapotranspiration`         | mm         | Float     | Reference evapotranspiration (ET0) using FAO standard              |
| `vapour_pressure_deficit`            | kPa        | Float     | Vapour pressure deficit                                            |
| `wind_speed_10m`                     | km/h       | Float     | Wind speed at 10 meters above ground                               |
| `wind_speed_80m`                     | km/h       | Float     | Wind speed at 80 meters above ground                               |
| `wind_speed_120m`                    | km/h       | Float     | Wind speed at 120 meters above ground                              |
| `wind_speed_180m`                    | km/h       | Float     | Wind speed at 180 meters above ground                              |
| `wind_direction_10m`                 | degrees    | Integer   | Wind direction at 10 meters above ground (0-360)                   |
| `wind_direction_80m`                 | degrees    | Integer   | Wind direction at 80 meters above ground                           |
| `wind_direction_120m`               | degrees    | Integer   | Wind direction at 120 meters above ground                          |
| `wind_direction_180m`               | degrees    | Integer   | Wind direction at 180 meters above ground                          |
| `wind_gusts_10m`                     | km/h       | Float     | Wind gusts at 10 meters above ground                               |
| `temperature_80m`                    | C          | Float     | Air temperature at 80 meters above ground                          |
| `temperature_120m`                   | C          | Float     | Air temperature at 120 meters above ground                         |
| `temperature_180m`                   | C          | Float     | Air temperature at 180 meters above ground                         |
| `soil_temperature_0cm`               | C          | Float     | Soil temperature at 0 cm depth (surface)                           |
| `soil_temperature_6cm`               | C          | Float     | Soil temperature at 6 cm depth                                     |
| `soil_temperature_18cm`              | C          | Float     | Soil temperature at 18 cm depth                                    |
| `soil_temperature_54cm`              | C          | Float     | Soil temperature at 54 cm depth                                    |
| `soil_moisture_0_to_1cm`             | m3/m3      | Float     | Soil moisture at 0-1 cm depth (volumetric)                         |
| `soil_moisture_1_to_3cm`             | m3/m3      | Float     | Soil moisture at 1-3 cm depth                                      |
| `soil_moisture_3_to_9cm`             | m3/m3      | Float     | Soil moisture at 3-9 cm depth                                      |
| `soil_moisture_9_to_27cm`            | m3/m3      | Float     | Soil moisture at 9-27 cm depth                                     |
| `soil_moisture_27_to_81cm`           | m3/m3      | Float     | Soil moisture at 27-81 cm depth                                    |
| `surface_temperature`                | C          | Float     | Temperature at the surface level                                   |
| `cape`                               | J/kg       | Float     | Convective Available Potential Energy                              |
| `lifted_index`                       | (unitless) | Float     | Lifted index (atmospheric stability indicator)                     |
| `convective_inhibition`              | J/kg       | Float     | Convective Inhibition (CIN)                                        |
| `freezing_level_height`              | m          | Float     | Height of the 0C isotherm above ground                             |
| `boundary_layer_height`              | m          | Float     | Planetary boundary layer height                                    |
| `is_day`                             | (unitless) | Integer   | 1 if daytime, 0 if nighttime                                      |
| `sunshine_duration`                  | s          | Float     | Sunshine duration in seconds per hour                              |
| `shortwave_radiation`                | W/m2       | Float     | Shortwave solar radiation (average over hour)                      |
| `direct_radiation`                   | W/m2       | Float     | Direct solar radiation on a horizontal surface                     |
| `diffuse_radiation`                  | W/m2       | Float     | Diffuse solar radiation                                            |
| `direct_normal_irradiance`           | W/m2       | Float     | Direct Normal Irradiance (DNI)                                     |
| `global_tilted_irradiance`           | W/m2       | Float     | Global Tilted Irradiance (GTI) for a given tilt angle              |
| `terrestrial_radiation`              | W/m2       | Float     | Terrestrial (longwave) radiation                                   |
| `shortwave_radiation_instant`        | W/m2       | Float     | Shortwave radiation (instantaneous value at timestamp)             |
| `direct_radiation_instant`           | W/m2       | Float     | Direct radiation (instantaneous)                                   |
| `diffuse_radiation_instant`          | W/m2       | Float     | Diffuse radiation (instantaneous)                                  |
| `direct_normal_irradiance_instant`   | W/m2       | Float     | DNI (instantaneous)                                                |
| `global_tilted_irradiance_instant`   | W/m2       | Float     | GTI (instantaneous)                                                |
| `terrestrial_radiation_instant`      | W/m2       | Float     | Terrestrial radiation (instantaneous)                              |
| `uv_index`                           | (unitless) | Float     | UV index                                                           |
| `uv_index_clear_sky`                 | (unitless) | Float     | UV index under clear-sky conditions                                |
| `wet_bulb_temperature_2m`            | C          | Float     | Wet bulb temperature at 2 meters                                   |
| `lightning_potential`                 | J/kg       | Float     | Lightning potential index (based on CAPE)                          |
| `total_column_integrated_water_vapour` | kg/m2    | Float     | Total column integrated water vapour                               |
| `snowfall_height`                    | m          | Float     | Height above which precipitation falls as snow                     |

### daily_forecast

Each row represents one day at one location. The `time` array contains ISO 8601 date strings (e.g., `"2026-04-10"`), and each variable is a parallel array of values.

**Primary Key**: `latitude`, `longitude`, `time`

#### Daily Weather Variables

| Variable Name                        | Unit       | JSON Type | Description                                                        |
|--------------------------------------|------------|-----------|--------------------------------------------------------------------|
| `time`                               | iso8601    | String    | Date for each daily step (e.g., "2026-04-10")                     |
| `weather_code`                       | wmo code   | Integer   | WMO weather interpretation code (most severe of the day)           |
| `temperature_2m_max`                 | C          | Float     | Maximum daily air temperature at 2 meters                          |
| `temperature_2m_min`                 | C          | Float     | Minimum daily air temperature at 2 meters                          |
| `temperature_2m_mean`                | C          | Float     | Mean daily air temperature at 2 meters                             |
| `apparent_temperature_max`           | C          | Float     | Maximum daily apparent temperature                                 |
| `apparent_temperature_min`           | C          | Float     | Minimum daily apparent temperature                                 |
| `apparent_temperature_mean`          | C          | Float     | Mean daily apparent temperature                                    |
| `sunrise`                            | iso8601    | String    | Sunrise time (e.g., "2026-04-10T06:19")                           |
| `sunset`                             | iso8601    | String    | Sunset time (e.g., "2026-04-10T19:55")                            |
| `daylight_duration`                  | s          | Float     | Duration of daylight in seconds                                    |
| `sunshine_duration`                  | s          | Float     | Duration of sunshine (direct radiation > 120 W/m2) in seconds     |
| `uv_index_max`                       | (unitless) | Float     | Maximum UV index of the day                                        |
| `uv_index_clear_sky_max`            | (unitless) | Float     | Maximum UV index under clear-sky conditions                        |
| `precipitation_sum`                  | mm         | Float     | Total daily precipitation sum                                      |
| `rain_sum`                           | mm         | Float     | Total daily rain sum                                               |
| `showers_sum`                        | mm         | Float     | Total daily showers sum                                            |
| `snowfall_sum`                       | cm         | Float     | Total daily snowfall sum                                           |
| `snowfall_water_equivalent_sum`      | mm         | Float     | Snowfall water equivalent sum                                      |
| `precipitation_hours`                | h          | Float     | Number of hours with precipitation                                 |
| `precipitation_probability_max`      | %          | Integer   | Maximum precipitation probability of the day                      |
| `precipitation_probability_min`      | %          | Integer   | Minimum precipitation probability of the day                      |
| `precipitation_probability_mean`     | %          | Integer   | Mean precipitation probability of the day                          |
| `wind_speed_10m_max`                | km/h       | Float     | Maximum daily wind speed at 10 meters                              |
| `wind_speed_10m_mean`               | km/h       | Float     | Mean daily wind speed at 10 meters                                 |
| `wind_speed_10m_min`                | km/h       | Float     | Minimum daily wind speed at 10 meters                              |
| `wind_gusts_10m_max`                | km/h       | Float     | Maximum daily wind gusts at 10 meters                              |
| `wind_gusts_10m_mean`               | km/h       | Float     | Mean daily wind gusts at 10 meters                                 |
| `wind_gusts_10m_min`                | km/h       | Float     | Minimum daily wind gusts at 10 meters                              |
| `wind_direction_10m_dominant`        | degrees    | Integer   | Dominant wind direction of the day                                 |
| `shortwave_radiation_sum`            | MJ/m2      | Float     | Total daily shortwave radiation sum                                |
| `et0_fao_evapotranspiration`         | mm         | Float     | Daily reference evapotranspiration (ET0, FAO standard)             |
| `dew_point_2m_max`                   | C          | Float     | Maximum daily dew point at 2 meters                                |
| `dew_point_2m_min`                   | C          | Float     | Minimum daily dew point at 2 meters                                |
| `dew_point_2m_mean`                  | C          | Float     | Mean daily dew point at 2 meters                                   |
| `relative_humidity_2m_max`           | %          | Integer   | Maximum daily relative humidity at 2 meters                        |
| `relative_humidity_2m_min`           | %          | Integer   | Minimum daily relative humidity at 2 meters                        |
| `relative_humidity_2m_mean`          | %          | Integer   | Mean daily relative humidity at 2 meters                           |
| `pressure_msl_max`                   | hPa        | Float     | Maximum daily pressure at mean sea level                           |
| `pressure_msl_min`                   | hPa        | Float     | Minimum daily pressure at mean sea level                           |
| `pressure_msl_mean`                  | hPa        | Float     | Mean daily pressure at mean sea level                              |
| `surface_pressure_max`               | hPa        | Float     | Maximum daily surface pressure                                     |
| `surface_pressure_min`               | hPa        | Float     | Minimum daily surface pressure                                     |
| `surface_pressure_mean`              | hPa        | Float     | Mean daily surface pressure                                        |
| `cloud_cover_max`                    | %          | Integer   | Maximum daily cloud cover                                          |
| `cloud_cover_min`                    | %          | Integer   | Minimum daily cloud cover                                          |
| `cloud_cover_mean`                   | %          | Integer   | Mean daily cloud cover                                             |
| `visibility_max`                     | m          | Float     | Maximum daily visibility                                           |
| `visibility_min`                     | m          | Float     | Minimum daily visibility                                           |
| `visibility_mean`                    | m          | Float     | Mean daily visibility                                              |
| `vapour_pressure_deficit_max`        | kPa        | Float     | Maximum daily vapour pressure deficit                              |
| `wet_bulb_temperature_2m_max`        | C          | Float     | Maximum daily wet bulb temperature at 2 meters                     |
| `wet_bulb_temperature_2m_min`        | C          | Float     | Minimum daily wet bulb temperature at 2 meters                     |
| `wet_bulb_temperature_2m_mean`       | C          | Float     | Mean daily wet bulb temperature at 2 meters                        |
| `cape_max`                           | J/kg       | Float     | Maximum daily CAPE                                                 |
| `cape_min`                           | J/kg       | Float     | Minimum daily CAPE                                                 |
| `cape_mean`                          | J/kg       | Float     | Mean daily CAPE                                                    |
| `updraft_max`                        | m/s        | Float     | Maximum daily updraft velocity                                     |

---

## Get Object Primary Keys

Primary keys are not provided by the API -- they must be defined by the connector.

| Table              | Primary Key Columns            | Notes                                                    |
|--------------------|--------------------------------|----------------------------------------------------------|
| `hourly_forecast`  | `latitude`, `longitude`, `time` | Composite key. `time` is ISO 8601 hourly timestamp.     |
| `daily_forecast`   | `latitude`, `longitude`, `time` | Composite key. `time` is ISO 8601 date string.          |

**Note**: The API returns `latitude` and `longitude` as top-level metadata fields (not inside the `hourly`/`daily` arrays). The connector must inject these values into each row.

---

## Object Ingestion Type

| Table              | Ingestion Type | Rationale                                                                                    |
|--------------------|----------------|----------------------------------------------------------------------------------------------|
| `hourly_forecast`  | `snapshot`     | Forecast data is replaced on every API call. Each response is a full replacement of the forecast window. There is no cursor or incremental mechanism. |
| `daily_forecast`   | `snapshot`     | Same as hourly -- each response replaces the entire forecast window.                        |

---

## Read API for Data Retrieval

### Endpoint

```
GET https://api.open-meteo.com/v1/forecast
```

For commercial API:
```
GET https://customer-api.open-meteo.com/v1/forecast
```

### Required Parameters

| Parameter   | Type  | Description                                                      |
|-------------|-------|------------------------------------------------------------------|
| `latitude`  | Float | Geographic latitude in decimal degrees (WGS84). Example: `52.52` |
| `longitude` | Float | Geographic longitude in decimal degrees (WGS84). Example: `13.41` |

At least one of `hourly` or `daily` must also be specified, or the response will be empty.

### Optional Parameters

| Parameter            | Type    | Default       | Description                                                                                      |
|----------------------|---------|---------------|--------------------------------------------------------------------------------------------------|
| `hourly`             | String  | (none)        | Comma-separated list of hourly weather variables to include.                                     |
| `daily`              | String  | (none)        | Comma-separated list of daily weather variables to include.                                      |
| `timezone`           | String  | `"GMT"`       | Timezone for time values. Use `"auto"` for automatic detection, or IANA timezone (e.g., `"Europe/Berlin"`). |
| `temperature_unit`   | String  | `"celsius"`   | Temperature unit. Options: `"celsius"`, `"fahrenheit"`.                                          |
| `wind_speed_unit`    | String  | `"kmh"`       | Wind speed unit. Options: `"kmh"`, `"ms"`, `"mph"`, `"kn"`.                                     |
| `precipitation_unit` | String  | `"mm"`        | Precipitation unit. Options: `"mm"`, `"inch"`.                                                   |
| `timeformat`         | String  | `"iso8601"`   | Time format. Options: `"iso8601"`, `"unixtime"`.                                                |
| `forecast_days`      | Integer | `7`           | Number of forecast days (1-16).                                                                  |
| `forecast_hours`     | Integer | (none)        | Number of forecast hours. Alternative to `forecast_days`.                                        |
| `past_days`          | Integer | `0`           | Number of past days to include (0-92).                                                           |
| `past_hours`         | Integer | (none)        | Number of past hours to include.                                                                 |
| `start_date`         | String  | (none)        | Start date in `YYYY-MM-DD` format. Used with `end_date` to define a custom date range.          |
| `end_date`           | String  | (none)        | End date in `YYYY-MM-DD` format.                                                                |
| `models`             | String  | `"best_match"` | Comma-separated weather model(s). See "Available Weather Models" below.                         |
| `cell_selection`     | String  | `"land"`      | Grid cell selection method. Options: `"land"`, `"sea"`, `"nearest"`.                            |
| `apikey`             | String  | (none)        | API key for commercial subscriptions.                                                            |

### Available Weather Models

The `models` parameter selects which numerical weather model(s) to use. Default is `best_match`, which automatically selects the best available model for the location.

**Global Models:**
- `best_match` -- Automatically selects the best model (default)
- `ecmwf_ifs` -- ECMWF IFS (European Centre for Medium-Range Weather Forecasts)
- `ecmwf_ifs025` -- ECMWF IFS at 0.25 degree resolution
- `ecmwf_aifs025_single` -- ECMWF AI-based forecast model
- `gfs_seamless` -- GFS seamless (NOAA, combines HRRR + GFS)
- `gfs_global` -- NOAA GFS Global
- `gfs_hrrr` -- NOAA HRRR (High-Resolution Rapid Refresh, US only)
- `gfs_graphcast025` -- Google GraphCast via NOAA
- `icon_seamless` -- DWD ICON seamless (combines global + EU + D2)
- `icon_global` -- DWD ICON Global
- `icon_eu` -- DWD ICON EU (Europe, ~7 km)
- `icon_d2` -- DWD ICON D2 (Germany, ~2 km)
- `gem_seamless` -- Canadian GEM seamless
- `gem_global` -- Canadian GEM Global
- `gem_regional` -- Canadian GEM Regional
- `gem_hrdps_continental` -- Canadian HRDPS Continental
- `gem_hrdps_west` -- Canadian HRDPS West
- `meteofrance_seamless` -- Meteo-France seamless
- `meteofrance_arpege_world` -- Meteo-France ARPEGE World
- `meteofrance_arpege_europe` -- Meteo-France ARPEGE Europe
- `meteofrance_arome_france` -- Meteo-France AROME France
- `meteofrance_arome_france_hd` -- Meteo-France AROME France HD
- `jma_seamless` -- Japan Meteorological Agency seamless
- `jma_gsm` -- JMA Global Spectral Model
- `jma_msm` -- JMA Mesoscale Model
- `metno_seamless` -- Norwegian Meteorological Institute seamless
- `metno_nordic` -- MET Nordic (Scandinavia, ~2.5 km)
- `knmi_seamless` -- KNMI seamless
- `knmi_harmonie_arome_europe` -- KNMI HARMONIE AROME Europe
- `knmi_harmonie_arome_netherlands` -- KNMI HARMONIE AROME Netherlands
- `dmi_seamless` -- Danish Meteorological Institute seamless
- `dmi_harmonie_arome_europe` -- DMI HARMONIE AROME Europe
- `bom_access_global` -- Australian Bureau of Meteorology ACCESS Global
- `cma_grapes_global` -- China Meteorological Administration GRAPES Global
- `kma_seamless` -- Korean Meteorological Administration seamless
- `kma_gdps` -- KMA GDPS
- `kma_ldps` -- KMA LDPS (local, Korea region)
- `ukmo_seamless` -- UK Met Office seamless
- `ukmo_global_deterministic_10km` -- UKMO Global Deterministic 10km
- `ukmo_uk_deterministic_2km` -- UKMO UK Deterministic 2km
- `geosphere_seamless` -- GeoSphere Austria seamless
- `geosphere_arome_austria` -- GeoSphere AROME Austria
- `meteoswiss_icon_seamless` -- MeteoSwiss ICON seamless
- `meteoswiss_icon_ch1` -- MeteoSwiss ICON CH1 (~1 km, Switzerland)
- `meteoswiss_icon_ch2` -- MeteoSwiss ICON CH2 (~2 km, Switzerland)
- `italia_meteo_arpae_icon_2i` -- Italia Meteo ARPAE ICON 2I
- `ncep_nam_conus` -- NCEP NAM CONUS (North America)
- `ncep_nbm_conus` -- NCEP NBM CONUS (National Blend of Models)
- `ncep_aigfs025` -- NCEP AI-based Global Forecast
- `ncep_hgefs025_ensemble_mean` -- NCEP HGEFS Ensemble Mean

### Example Requests

**Hourly forecast (single variable):**
```
GET https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&hourly=temperature_2m
```

**Hourly forecast (multiple variables):**
```
GET https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m,precipitation&forecast_days=3
```

**Daily forecast:**
```
GET https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,wind_speed_10m_max&timezone=auto
```

**Combined hourly and daily:**
```
GET https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&hourly=temperature_2m&daily=temperature_2m_max&timezone=auto&forecast_days=3
```

**With specific model:**
```
GET https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&hourly=temperature_2m&models=icon_seamless&forecast_days=1
```

**With date range:**
```
GET https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&hourly=temperature_2m&start_date=2026-04-10&end_date=2026-04-10
```

### Example Response: Hourly

```json
{
    "latitude": 52.52,
    "longitude": 13.419998,
    "generationtime_ms": 0.096,
    "utc_offset_seconds": 0,
    "timezone": "GMT",
    "timezone_abbreviation": "GMT",
    "elevation": 38.0,
    "hourly_units": {
        "time": "iso8601",
        "temperature_2m": "\u00b0C"
    },
    "hourly": {
        "time": [
            "2026-04-10T00:00",
            "2026-04-10T01:00",
            "2026-04-10T02:00"
        ],
        "temperature_2m": [
            3.7,
            2.8,
            2.5
        ]
    }
}
```

### Example Response: Daily

```json
{
    "latitude": 52.52,
    "longitude": 13.419998,
    "generationtime_ms": 0.316,
    "utc_offset_seconds": 7200,
    "timezone": "Europe/Berlin",
    "timezone_abbreviation": "GMT+2",
    "elevation": 38.0,
    "daily_units": {
        "time": "iso8601",
        "weather_code": "wmo code",
        "temperature_2m_max": "\u00b0C",
        "temperature_2m_min": "\u00b0C",
        "sunrise": "iso8601",
        "sunset": "iso8601",
        "precipitation_sum": "mm"
    },
    "daily": {
        "time": ["2026-04-10", "2026-04-11"],
        "weather_code": [3, 3],
        "temperature_2m_max": [8.4, 13.3],
        "temperature_2m_min": [1.7, 2.0],
        "sunrise": ["2026-04-10T06:19", "2026-04-11T06:17"],
        "sunset": ["2026-04-10T19:55", "2026-04-11T19:57"],
        "precipitation_sum": [0.0, 0.0]
    }
}
```

### Example Response: Error

```json
{
    "reason": "Data corrupted at path ''. Cannot initialize ... from invalid String value invalid_variable.",
    "error": true
}
```

Missing or invalid latitude/longitude:
```json
{
    "reason": "Parameter 'latitude' and 'longitude' must have the same number of elements",
    "error": true
}
```

### Response JSON Structure

The response is a flat JSON object with these top-level keys:

| Key                        | Type    | Present When              | Description                                      |
|----------------------------|---------|---------------------------|--------------------------------------------------|
| `latitude`                 | Float   | Always (success)          | Resolved latitude                                |
| `longitude`                | Float   | Always (success)          | Resolved longitude                               |
| `generationtime_ms`        | Float   | Always (success)          | Response generation time in ms                   |
| `utc_offset_seconds`       | Integer | Always (success)          | UTC offset based on timezone param               |
| `timezone`                 | String  | Always (success)          | Timezone name                                    |
| `timezone_abbreviation`    | String  | Always (success)          | Timezone abbreviation                            |
| `elevation`                | Float   | Always (success)          | Grid point elevation in meters                   |
| `hourly_units`             | Object  | When `hourly` requested   | Map of variable name to unit string              |
| `hourly`                   | Object  | When `hourly` requested   | Map of variable name to array of values          |
| `daily_units`              | Object  | When `daily` requested    | Map of variable name to unit string              |
| `daily`                    | Object  | When `daily` requested    | Map of variable name to array of values          |
| `error`                    | Boolean | On error                  | `true` when error                                |
| `reason`                   | String  | On error                  | Error description                                |

**Key structural feature**: The `hourly` and `daily` objects use **parallel arrays** -- the `time` array and all variable arrays have the same length. Each index `i` across all arrays corresponds to the same time step.

### Rate Limits

**Free tier:**
| Limit          | Value                  |
|----------------|------------------------|
| Per minute     | 600 API calls          |
| Per hour       | 5,000 API calls        |
| Per day        | 10,000 API calls       |
| Per month      | ~300,000 API calls     |

**Note**: Requests with more than 10 weather variables or spanning more than 2 weeks for a single location count as multiple API calls.

**Commercial tiers**: Unlimited API calls (Standard: ~1M/month, Professional: ~5M/month, Enterprise: 50M+/month).

### Pagination

The Open-Meteo Forecast API does **not** use pagination. Each request returns the complete forecast for the specified time range in a single response. There is no `next_page` or cursor mechanism.

For multiple locations, separate API calls must be made for each latitude/longitude pair.

---

## Error Handling

| Scenario                             | HTTP Status | Response Body                                     | Action            |
|--------------------------------------|-------------|---------------------------------------------------|--------------------|
| Success                              | `200`       | JSON with forecast data                           | Process response   |
| Invalid variable name                | `400`       | `{"error": true, "reason": "..."}`                | Do not retry       |
| Missing required parameter           | `400`       | `{"error": true, "reason": "..."}`                | Do not retry       |
| Rate limit exceeded                  | `429`       | (varies)                                          | Retry with backoff |
| Server error                         | `5xx`       | (varies)                                          | Retry with backoff |

---

## Field Type Mapping

### Open-Meteo JSON Type to Spark Data Type

| JSON Value Type | API Unit Category                                                   | Spark Data Type   |
|-----------------|---------------------------------------------------------------------|-------------------|
| Float           | Temperature (C), pressure (hPa), precipitation (mm), wind speed (km/h), radiation (W/m2), soil moisture (m3/m3), elevation (m), etc. | `DoubleType`      |
| Integer         | Relative humidity (%), cloud cover (%), wind direction (degrees), weather code (wmo code), is_day, precipitation probability (%) | `LongType`        |
| String          | Time/date (iso8601), sunrise/sunset (iso8601)                       | `StringType`      |
| Integer (unix)  | Time when `timeformat=unixtime`                                     | `LongType`        |
| Float (top-level) | latitude, longitude, elevation, generationtime_ms                 | `DoubleType`      |
| Integer (top-level) | utc_offset_seconds                                              | `LongType`        |
| String (top-level)  | timezone, timezone_abbreviation                                 | `StringType`      |

**Recommended approach**: Since the connector knows the variable names requested, it should use a static mapping. Most weather values are `DoubleType`, with the following exceptions:
- **`LongType`**: `relative_humidity_2m`, `weather_code`, `cloud_cover`, `cloud_cover_low`, `cloud_cover_mid`, `cloud_cover_high`, `wind_direction_10m`, `wind_direction_80m`, `wind_direction_120m`, `wind_direction_180m`, `is_day`, `precipitation_probability`, `precipitation_probability_max`, `precipitation_probability_min`, `precipitation_probability_mean`, `wind_direction_10m_dominant`, `relative_humidity_2m_max`, `relative_humidity_2m_min`, `relative_humidity_2m_mean`, `cloud_cover_max`, `cloud_cover_min`, `cloud_cover_mean`
- **`StringType`**: `time`, `sunrise`, `sunset`
- **`DoubleType`**: All other numeric weather variables

**Note on timestamps**: The `time` field in hourly responses uses format `"YYYY-MM-DDTHH:MM"` (no seconds, no timezone suffix). For daily responses, time uses `"YYYY-MM-DD"`. Both are strings in the JSON. The connector may choose to parse these into `TimestampType` or `DateType` respectively.

---

## Sources and References

### Research Log

| Source | URL | Information Gathered |
|--------|-----|---------------------|
| Open-Meteo Forecast API docs | https://open-meteo.com/en/docs | All parameters, hourly/daily variable names, available models, response structure |
| Open-Meteo Features page | https://open-meteo.com/en/features | Feature overview, model coverage, geographic scope |
| Open-Meteo Pricing page | https://open-meteo.com/en/pricing | Rate limits (free: 600/min, 5000/hr, 10000/day, 300K/month), commercial plans, API key usage, call counting rules |
| Open-Meteo Terms page | https://open-meteo.com/en/terms | Free tier is non-commercial only, CC-BY 4.0 license, commercial requires subscription |
| Live API response (hourly) | https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&hourly=temperature_2m | Confirmed JSON structure, field names, time format, 7-day default window |
| Live API response (all hourly vars) | https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&hourly=temperature_2m,...(38 vars)&forecast_days=1 | Confirmed all hourly variable names, units, and Python types (float vs int) |
| Live API response (daily) | https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&daily=weather_code,...(23 vars)&timezone=auto | Confirmed all daily variable names, units, and types |
| Live API response (daily aggregations) | https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&daily=temperature_2m_mean,...(11 vars) | Confirmed daily mean/max/min aggregation variables work |
| Live API response (additional daily) | https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&daily=wind_speed_10m_mean,...(24 vars) | Confirmed wind, humidity, pressure, visibility daily aggregations |
| Live API response (radiation hourly) | https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&hourly=shortwave_radiation,...(26 vars) | Confirmed radiation, UV, CAPE, boundary layer, precipitation probability, wet bulb, etc. |
| Live API response (extra hourly) | https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&hourly=lightning_potential,... | Confirmed lightning_potential, total_column_integrated_water_vapour, surface_temperature, snowfall_height |
| Live API error response | https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&hourly=invalid_variable | Confirmed error format: `{"reason": "...", "error": true}` |
| Live API (unixtime format) | https://api.open-meteo.com/v1/forecast?...&timeformat=unixtime | Confirmed unixtime returns integer timestamps |
| Live API (past_days) | https://api.open-meteo.com/v1/forecast?...&past_days=1 | Confirmed past_days extends the time range backwards |
| Live API (date range) | https://api.open-meteo.com/v1/forecast?...&start_date=2026-04-10&end_date=2026-04-10 | Confirmed start_date/end_date work for custom ranges |
| Live API (cell_selection) | https://api.open-meteo.com/v1/forecast?...&cell_selection=nearest | Confirmed cell_selection parameter is accepted |
| Live API (models parameter) | https://api.open-meteo.com/v1/forecast?...&models=icon_seamless | Confirmed models parameter selects specific weather model |
| HTML scraping of docs page | https://open-meteo.com/en/docs | Extracted complete list of weather models (~50+) and all variable names from page source |

### Existing Open-Meteo Connectors / Client Libraries

TBD: WebSearch was unavailable during research. Known community resources include:
- **openmeteo-requests**: Python library for Open-Meteo API (available on PyPI)
- **open-meteo**: Official npm package
- **Airbyte**: Has a community connector for Open-Meteo (source-open-meteo)
- No known Fivetran or Singer connector as of the research date

### WMO Weather Code Reference

The `weather_code` field uses standard WMO 4677 codes:

| Code | Description                |
|------|----------------------------|
| 0    | Clear sky                  |
| 1    | Mainly clear               |
| 2    | Partly cloudy              |
| 3    | Overcast                   |
| 45   | Fog                        |
| 48   | Depositing rime fog        |
| 51   | Drizzle: Light             |
| 53   | Drizzle: Moderate          |
| 55   | Drizzle: Dense             |
| 56   | Freezing drizzle: Light    |
| 57   | Freezing drizzle: Dense    |
| 61   | Rain: Slight               |
| 63   | Rain: Moderate             |
| 65   | Rain: Heavy                |
| 66   | Freezing rain: Light       |
| 67   | Freezing rain: Heavy       |
| 71   | Snow fall: Slight          |
| 73   | Snow fall: Moderate        |
| 75   | Snow fall: Heavy           |
| 77   | Snow grains                |
| 80   | Rain showers: Slight       |
| 81   | Rain showers: Moderate     |
| 82   | Rain showers: Violent      |
| 85   | Snow showers: Slight       |
| 86   | Snow showers: Heavy        |
| 95   | Thunderstorm: Slight/Moderate |
| 96   | Thunderstorm with slight hail |
| 99   | Thunderstorm with heavy hail  |
