# WeatherForecast Backend Design Document

---

## Section 1: Flask Routes Specification

### 1. Dashboard Page
- **URL:** `/`
- **Methods:** GET
- **Description:** Render main dashboard with current weather summary for default location.
- **Inputs:** None
- **Outputs:** Render template `dashboard.html` with current weather data.

### 2. Current Weather Page
- **URL:** `/weather/current/<int:location_id>`
- **Methods:** GET
- **Description:** Display detailed current weather for given location.
- **Inputs:** `location_id` as URL path parameter
- **Outputs:** Render template `current_weather.html` with weather details for the specified location.

### 3. Weekly Forecast Page
- **URL:** `/forecast`
- **Methods:** GET
- **Query Parameters:** Optional `location_id` to filter forecast by location; if absent use default location.
- **Description:** Show 7-day forecast for selected or default location.
- **Outputs:** Render template `forecast.html` with forecast data.

### 4. Location Search Page
- **URL:** `/locations/search`
- **Methods:** GET
- **Query Parameters:** Optional `query` string to search for location names or coordinates.
- **Description:** Render search page with saved locations and search results.
- **Outputs:** Render template `location_search.html` with search results and saved locations.

- **URL:** `/locations/select`
- **Methods:** POST
- **Payload:** JSON or form-data with `location_id` to add location to saved list.
- **Outputs:** JSON response with success status.

- **URL:** `/locations/remove`
- **Methods:** POST
- **Payload:** JSON or form-data with `location_id` to remove from saved locations.
- **Outputs:** JSON response with success status.

### 5. Weather Alerts Page
- **URL:** `/alerts`
- **Methods:** GET
- **Query Parameters:** Optional `location_id` and `severity` to filter alerts.
- **Description:** Displays active alerts filtered by location and severity.
- **Outputs:** Render template `alerts.html` with filtered alert list.

- **URL:** `/alerts/acknowledge`
- **Methods:** POST
- **Payload:** JSON or form-data with `alert_id` to mark alert as acknowledged.
- **Outputs:** JSON response with success status.

### 6. Air Quality Page
- **URL:** `/air_quality`
- **Methods:** GET
- **Query Parameters:** Optional `location_id` to filter air quality information.
- **Outputs:** Render template `air_quality.html` with air quality details and health recommendations.

### 7. Saved Locations Page
- **URL:** `/locations/saved`
- **Methods:** GET
- **Description:** List saved locations with current weather snapshots.
- **Outputs:** Render template `saved_locations.html`.

### 8. Settings Page
- **URL:** `/settings`
- **Methods:** GET
- **Description:** Render settings page with current configuration values.
- **Outputs:** Render template `settings.html`.

- **URL:** `/settings/save`
- **Methods:** POST
- **Payload:** JSON or form-data including:
  - `temperature_unit` (Celsius, Fahrenheit, Kelvin)
  - `default_location_id`
  - `alert_notifications_enabled` (boolean)
- **Description:** Save user settings and update default location.
- **Outputs:** JSON response with success status.

---

## Section 2: Data File Schemas

### 1. Current Weather Data (`data/current_weather.txt`)
- **Delimiter:** `|`
- **Fields:**
  - `location_id` (int): Unique identifier for location
  - `location_name` (str)
  - `temperature` (int or float): Current temperature
  - `condition` (str): Weather condition description
  - `humidity` (int): Percentage humidity
  - `wind_speed` (int or float): Wind speed in mph or kph
  - `last_updated` (str): Timestamp (`YYYY-MM-DD HH:MM`)

- **Example:**
  ```
  1|New York|72|Sunny|65|10|2025-01-20 14:30
  2|London|55|Rainy|80|15|2025-01-20 14:30
  3|Tokyo|45|Cloudy|72|8|2025-01-20 14:30
  ```

### 2. Forecasts Data (`data/forecasts.txt`)
- **Delimiter:** `|`
- **Fields:**
  - `forecast_id` (int)
  - `location_id` (int)
  - `date` (str): Date in `YYYY-MM-DD`
  - `high_temp` (int or float)
  - `low_temp` (int or float)
  - `condition` (str)
  - `precipitation` (int): percent chance
  - `humidity` (int): percent

- **Example:**
  ```
  1|1|2025-01-21|75|60|Sunny|0|60
  2|1|2025-01-22|68|55|Cloudy|10|70
  3|2|2025-01-21|58|48|Rainy|80|85
  ```

### 3. Locations Data (`data/locations.txt`)
- **Delimiter:** `|`
- **Fields:**
  - `location_id` (int)
  - `location_name` (str)
  - `latitude` (float)
  - `longitude` (float)
  - `country` (str)
  - `timezone` (str)

- **Example:**
  ```
  1|New York|40.7128|-74.0060|USA|EST
  2|London|51.5074|-0.1278|UK|GMT
  3|Tokyo|35.6762|139.6503|Japan|JST
  ```

### 4. Weather Alerts Data (`data/alerts.txt`)
- **Delimiter:** `|`
- **Fields:**
  - `alert_id` (int)
  - `location_id` (int)
  - `alert_type` (str)
  - `severity` (str): Critical, High, Medium, Low
  - `description` (str)
  - `start_time` (str): `YYYY-MM-DD HH:MM`
  - `end_time` (str): `YYYY-MM-DD HH:MM`
  - `is_acknowledged` (int): 0 (false), 1 (true)

- **Example:**
  ```
  1|1|Thunderstorm|High|Severe thunderstorm warning in effect until 8 PM|2025-01-20 14:00|2025-01-20 20:00|0
  2|2|Fog|Medium|Dense fog advisory in effect until noon tomorrow|2025-01-20 06:00|2025-01-21 12:00|0
  3|1|Wind|Medium|High wind advisory with gusts up to 45 mph|2025-01-20 15:00|2025-01-21 09:00|1
  ```

### 5. Air Quality Data (`data/air_quality.txt`)
- **Delimiter:** `|`
- **Fields:**
  - `aqi_id` (int)
  - `location_id` (int)
  - `aqi_index` (int): 0-500
  - `pm25` (float): PM2.5 particulate level
  - `pm10` (float): PM10 particulate level
  - `no2` (float): Nitrogen dioxide level
  - `o3` (float): Ozone level
  - `last_updated` (str): `YYYY-MM-DD HH:MM`

- **Example:**
  ```
  1|1|45|12.5|35|28|55|2025-01-20 14:30
  2|2|67|22.3|48|42|78|2025-01-20 14:30
  3|3|120|68.5|95|65|110|2025-01-20 14:30
  ```

### 6. Saved Locations Data (`data/saved_locations.txt`)
- **Delimiter:** `|`
- **Fields:**
  - `saved_id` (int)
  - `user_id` (int): Since no auth, treat user_id as 1 default.
  - `location_id` (int)
  - `location_name` (str)
  - `is_default` (int): 0 (false), 1 (true)

- **Example:**
  ```
  1|1|1|New York|1
  2|1|2|London|0
  3|2|3|Tokyo|1
  ```

---

## Section 3: Backend Data Handling and Storage

### Data File Access & Manipulation
- All data files reside in the `data/` directory.
- Read operations open files and parse lines by splitting on `|`.
- Write operations overwrite entire files to persist changes.
- For updating single records (e.g., acknowledging alerts), read, modify in-memory, then rewrite file.

### Caching & Data Refresh Strategy
- Data is considered relatively static and updated externally; backend loads fresh data on each request.
- Optional caching layer could be added to reduce file I/O if needed.

### Default Location Handling
- Default location is stored in `saved_locations.txt` marked by `is_default=1` for user_id 1.
- Dashboard and main routes default to this location if no explicit location is provided.

### Alert Acknowledgment
- Alerts have `is_acknowledged` flag; POST endpoint updates this flag.
- Backend writes updated flag back into `alerts.txt`.

### Error Handling
- Validate input parameters for all routes.
- Return appropriate HTTP error codes (400, 404) when data or locations not found.
- Fail gracefully if file read/write errors occur, returning server error responses.

---

This document fully specifies the WeatherForecast backend design, enabling developers to implement Flask routes, manage local text file storage, and handle data according to requirements.