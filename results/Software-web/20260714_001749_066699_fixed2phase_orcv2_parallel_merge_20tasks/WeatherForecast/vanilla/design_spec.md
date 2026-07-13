# WeatherForecast Design Specification

---

## Section 1: Integrated Flask Routes and API

### 1. Dashboard Page
- **URL:** `/`
- **Methods:** GET
- **Description:** Render the main dashboard displaying current weather summary for the default location.
- **Inputs:** None
- **Outputs:** Render template `dashboard.html` with current weather data.

### 2. Current Weather Page
- **URL:** `/weather/current/<int:location_id>`
- **Methods:** GET
- **Description:** Display detailed current weather for the specified location.
- **Inputs:** `location_id` via URL path parameter.
- **Outputs:** Render template `current_weather.html` with weather details for location.

### 3. Weekly Forecast Page
- **URL:** `/forecast`
- **Methods:** GET
- **Query Parameters:** Optional `location_id` to filter forecasts; default location if absent.
- **Description:** Show 7-day weather forecast for selected or default location.
- **Outputs:** Render template `weekly_forecast.html` (note: filename aligned to frontend spec) with forecast data.

### 4. Location Search Page
- **URL:** `/locations/search`
- **Methods:** GET
- **Query Parameters:** Optional `query` string for location name or coordinates search.
- **Description:** Show search interface with saved locations and matching search results.
- **Outputs:** Render template `location_search.html` with search results and saved locations.

- **URL:** `/locations/select`
- **Methods:** POST
- **Payload:** JSON/form-data including `location_id` to add location to saved list.
- **Outputs:** JSON response with success status.

- **URL:** `/locations/remove`
- **Methods:** POST
- **Payload:** JSON/form-data including `location_id` to remove from saved locations.
- **Outputs:** JSON response with success status.

### 5. Weather Alerts Page
- **URL:** `/alerts`
- **Methods:** GET
- **Query Parameters:** Optional `location_id` and `severity` to filter alerts.
- **Description:** Show active weather alerts filtered accordingly.
- **Outputs:** Render template `weather_alerts.html` (aligned to frontend) with alert list.

- **URL:** `/alerts/acknowledge`
- **Methods:** POST
- **Payload:** JSON/form-data with `alert_id` to acknowledge alert.
- **Outputs:** JSON response with success status.

### 6. Air Quality Page
- **URL:** `/air_quality`
- **Methods:** GET
- **Query Parameters:** Optional `location_id` to filter air quality data.
- **Outputs:** Render template `air_quality.html` with air quality information and health recommendations.

### 7. Saved Locations Page
- **URL:** `/locations/saved`
- **Methods:** GET
- **Description:** Display saved locations with brief current weather.
- **Outputs:** Render template `saved_locations.html`.

### 8. Settings Page
- **URL:** `/settings`
- **Methods:** GET
- **Description:** Show settings UI with current user preferences.
- **Outputs:** Render template `settings.html`.

- **URL:** `/settings/save`
- **Methods:** POST
- **Payload:** JSON/form-data including `temperature_unit`, `default_location_id`, and `alert_notifications_enabled`.
- **Outputs:** JSON response with success status.

---

## Section 2: Unified Data Schema Definitions

All data files are located in the `data/` directory with the following schemas:

### 1. Current Weather Data (`current_weather.txt`)
- Fields: `location_id|location_name|temperature|condition|humidity|wind_speed|last_updated`
- Example:
  ```
1|New York|72|Sunny|65|10|2025-01-20 14:30
2|London|55|Rainy|80|15|2025-01-20 14:30
3|Tokyo|45|Cloudy|72|8|2025-01-20 14:30
  ```

### 2. Forecasts Data (`forecasts.txt`)
- Fields: `forecast_id|location_id|date|high_temp|low_temp|condition|precipitation|humidity`
- Example:
  ```
1|1|2025-01-21|75|60|Sunny|0|60
2|1|2025-01-22|68|55|Cloudy|10|70
3|2|2025-01-21|58|48|Rainy|80|85
  ```

### 3. Locations Data (`locations.txt`)
- Fields: `location_id|location_name|latitude|longitude|country|timezone`
- Example:
  ```
1|New York|40.7128|-74.0060|USA|EST
2|London|51.5074|-0.1278|UK|GMT
3|Tokyo|35.6762|139.6503|Japan|JST
  ```

### 4. Weather Alerts Data (`alerts.txt`)
- Fields: `alert_id|location_id|alert_type|severity|description|start_time|end_time|is_acknowledged`
- Example:
  ```
1|1|Thunderstorm|High|Severe thunderstorm warning in effect until 8 PM|2025-01-20 14:00|2025-01-20 20:00|0
2|2|Fog|Medium|Dense fog advisory in effect until noon tomorrow|2025-01-20 06:00|2025-01-21 12:00|0
3|1|Wind|Medium|High wind advisory with gusts up to 45 mph|2025-01-20 15:00|2025-01-21 09:00|1
  ```

### 5. Air Quality Data (`air_quality.txt`)
- Fields: `aqi_id|location_id|aqi_index|pm25|pm10|no2|o3|last_updated`
- Example:
  ```
1|1|45|12.5|35|28|55|2025-01-20 14:30
2|2|67|22.3|48|42|78|2025-01-20 14:30
3|3|120|68.5|95|65|110|2025-01-20 14:30
  ```

### 6. Saved Locations Data (`saved_locations.txt`)
- Fields: `saved_id|user_id|location_id|location_name|is_default` (user_id fixed as 1 since no auth)
- Example:
  ```
1|1|1|New York|1
2|1|2|London|0
3|2|3|Tokyo|1
  ```

---

## Section 3: HTML Templates and Navigation Flow

### Template Files and Page Elements

| Page                | Template Filename       | Container ID           | Key Elements (ID)                                              |
|---------------------|------------------------|------------------------|--------------------------------------------------------------|
| Dashboard           | dashboard.html          | dashboard-page         | current-weather-summary, search-location-button, view-forecast-button, view-alerts-button |
| Current Weather     | current_weather.html    | current-weather-page   | location-name, temperature-display, weather-condition, humidity-info, wind-speed-info       |
| Weekly Forecast     | weekly_forecast.html    | forecast-page          | forecast-table, location-filter, forecast-list, back-to-dashboard                          |
| Location Search     | location_search.html    | search-page            | location-search-input, search-results, select-location-button-{location_id}, saved-locations-list |
| Weather Alerts      | weather_alerts.html     | alerts-page            | alerts-list, severity-filter, location-filter-alerts, acknowledge-alert-button-{alert_id}   |
| Air Quality        | air_quality.html        | air-quality-page       | aqi-display, aqi-description, pollution-details, location-aqi-filter, health-recommendation |
| Saved Locations     | saved_locations.html    | saved-locations-page   | locations-table, view-location-weather-{location_id}, remove-location-button-{location_id}, add-new-location-button |
| Settings            | settings.html           | settings-page          | temperature-unit-select, default-location-select, alert-notifications-toggle, save-settings-button, back-to-dashboard |

### Navigation Flow and Routes

- From **Dashboard**:
  - `search-location-button` ➔ `/locations/search`
  - `view-forecast-button` ➔ `/forecast`
  - `view-alerts-button` ➔ `/alerts`

- From **Weekly Forecast**:
  - `back-to-dashboard` ➔ `/`

- From **Settings**:
  - `back-to-dashboard` ➔ `/`

- From **Saved Locations**:
  - `add-new-location-button` ➔ `/locations/search`

- From **Location Search**:
  - `select-location-button-{location_id}` ➔ POST `/locations/select` then redirect to `/weather/current/{location_id}`

- From **Saved Locations**:
  - `view-location-weather-{location_id}` ➔ `/weather/current/{location_id}`
  - `remove-location-button-{location_id}` ➔ POST `/locations/remove`

- From **Weather Alerts**:
  - `acknowledge-alert-button-{alert_id}` ➔ POST `/alerts/acknowledge`

### Interactive Component Behavior

- Dropdowns populate dynamically from saved or available locations (filters and settings).
- Search input dynamically filters locations by name or coordinates.
- Button IDs for dynamic elements follow `{action}-{entity_id}` pattern (e.g., `select-location-button-3`).
- State updates cause UI refresh or navigation accordingly.

---

## Section 4: Consistency and Completeness Checks

- All backend routes and frontend navigation URLs are aligned with each other.
- Template filenames correspond exactly between backend render calls and frontend templates.
- Element IDs in HTML templates match those specified in the user tasks and frontend design.
- Dynamic element IDs and their patterns are consistent for each data entity.
- Data file schemas are complete and consistent, and examples cover expected formats.
- No authentication; user_id consistently treated as 1 where needed.
- Navigation flows from all pages lead to valid backend routes that render correct templates.
- All user requirements for pages, UI elements, data storage, and interaction are covered.

This design specification document provides a single comprehensive source for developers to implement both backend and frontend of the WeatherForecast web application with coherent and error-free integration.