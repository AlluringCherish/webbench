# Design Specification Document for WeatherForecast Web Application

---

## Section 1: Flask Routes Specification

| URL Path                       | HTTP Methods | Function Name         | Template Filename               | Context Variables (name: type)                                                                                                         |
|-------------------------------|--------------|-----------------------|-------------------------------|----------------------------------------------------------------------------------------------------------------------------------------|
| /                              | GET          | root_redirect          | None (redirects to /dashboard)  | None                                                                                                                                   |
| /dashboard                    | GET          | dashboard_page         | dashboard.html                 | current_weather: dict {location_id: int, location_name: str, temperature: int, condition: str, humidity: int, wind_speed: int, last_updated: str}                                             |
| /weather/current/<int:location_id> | GET          | current_weather_page   | current_weather.html           | weather: dict {location_id: int, location_name: str, temperature: int, condition: str, humidity: int, wind_speed: int, last_updated: str}                                                      |
| /forecast/weekly               | GET          | weekly_forecast_page   | weekly_forecast.html           | location_id: int, forecasts: list of dict {forecast_id: int, location_id: int, date: str (YYYY-MM-DD), high_temp: int, low_temp: int, condition: str, precipitation: int, humidity: int}
| /locations/search             | GET, POST    | location_search_page   | location_search.html           | search_results: list of dict {location_id: int, location_name: str, latitude: float, longitude: float, country: str, timezone: str}
|                              |              |                       |                               | saved_locations: list of dict {saved_id: int, user_id: int, location_id: int, location_name: str, is_default: int}                                                                               |
| /alerts                      | GET          | alerts_page            | alerts.html                   | alerts: list of dict {alert_id: int, location_id: int, alert_type: str, severity: str, description: str, start_time: str, end_time: str, is_acknowledged: int}
|                              |              |                       |                               | severity_filter: str, location_filter: int                                                                                           |
| /alerts/acknowledge/<int:alert_id> | POST         | acknowledge_alert      | None (redirect or JSON response) | alert_id: int                                                                                                                        |
| /airquality                  | GET          | air_quality_page       | air_quality.html               | air_quality: list of dict {aqi_id: int, location_id: int, aqi_index: int, pm25: float, pm10: float, no2: float, o3: float, last_updated: str}
|                              |              |                       |                               | location_filter: int                                                                                                                |
| /locations/saved             | GET          | saved_locations_page   | saved_locations.html           | saved_locations: list of dict {saved_id: int, user_id: int, location_id: int, location_name: str, is_default: int}
|                              |              |                       |                               | weather_summary: dict {location_id: int, temperature: int, condition: str}                                                           |
| /locations/save              | POST         | add_new_location       | None (redirect or JSON response) | location_id: int, location_name: str                                                                                                |
| /locations/remove/<int:location_id> | POST         | remove_saved_location  | None (redirect or JSON response) | location_id: int                                                                                                                    |
| /settings                    | GET, POST    | settings_page          | settings.html                 | temperature_units: str ("Celsius", "Fahrenheit", "Kelvin")
|                               |              |                       |                               | default_location_id: int
|                               |              |                       |                               | alert_notifications_enabled: bool

**Details:**

- `/` redirects (HTTP 302) to `/dashboard` handled by `root_redirect` function.
- `dashboard_page` displays summary of current weather for default location and navigation buttons.
- `current_weather_page` shows detailed weather info for location identified by `<location_id>`.
- `weekly_forecast_page` allows filtering by location; shows 7-day forecasts.
- `location_search_page` supports GET showing search form and results, POST to perform search.
- `alerts_page` shows current alerts; filters by severity and location.
- `acknowledge_alert` POST route marks alert acknowledged.
- `air_quality_page` shows AQI and pollution details, filter by location.
- `saved_locations_page` lists saved locations with weather summary and controls.
- `/locations/save` POST to add new location.
- `/locations/remove/<location_id>` POST to remove saved location.
- `settings_page` GET shows current settings; POST updates preferences.

---

## Section 2: Frontend HTML Templates Specification

### 1. templates/dashboard.html
- Page Title: Weather Dashboard
- Main Heading: <h1 id="dashboard-page">Weather Dashboard</h1>
- Element IDs:
  - dashboard-page (Div): container for whole dashboard page
  - current-weather-summary (Div): display current weather summary of default location
  - search-location-button (Button): navigates to location search page (`url_for('location_search_page')`)
  - view-forecast-button (Button): navigates to weekly forecast page (`url_for('weekly_forecast_page')`)
  - view-alerts-button (Button): navigates to alerts page (`url_for('alerts_page')`)
- Navigation:
  - Buttons use `url_for` with backend function names as above.
- Context Variables:
  - current_weather: dict
- Notes: Render current_weather details inside `current-weather-summary` div.

---

### 2. templates/current_weather.html
- Page Title: Current Weather
- Main Heading: <h1 id="location-name"></h1> (location name)
- Element IDs:
  - current-weather-page (Div): main container
  - location-name (H1): location name
  - temperature-display (Div): current temperature
  - weather-condition (Div): weather condition
  - humidity-info (Div): humidity percentage
  - wind-speed-info (Div): wind speed
- Navigation:
  - No navigation buttons specified here (back via dashboard)
- Context Variables:
  - weather: dict
- Notes: Render respective weather values inside elements.

---

### 3. templates/weekly_forecast.html
- Page Title: Weekly Forecast
- Main Heading: <h1 id="forecast-page">Weekly Forecast</h1>
- Elements:
  - forecast-page (Div): main container
  - forecast-table (Table): displays daily forecast rows with columns: Date, High Temp, Low Temp, Condition
  - location-filter (Dropdown): select location to filter forecasts (send location_id)
  - forecast-list (Div): grid with individual day forecast cards
  - back-to-dashboard (Button): navigates to dashboard (`url_for('dashboard_page')`)
- Navigation:
  - back-to-dashboard button uses `url_for('dashboard_page')`
- Context Variables:
  - location_id: int
  - forecasts: list of dict
- Notes: Use loops to render each forecast in forecast-table and forecast-list.

---

### 4. templates/location_search.html
- Page Title: Search Locations
- Main Heading: <h1 id="search-page">Search Locations</h1>
- Elements:
  - search-page (Div): main container
  - location-search-input (Input): text input for city name or coordinates
  - search-results (Div): container listing search results
  - select-location-button-{location_id} (Button): per search result, button to select location
  - saved-locations-list (Div): listing saved locations
- Navigation:
  - No navigation buttons explicitly detailed
- Context Variables:
  - search_results: list of dict
  - saved_locations: list of dict
- Notes: Dynamic IDs for select-location-button must include location_id value, e.g., `select-location-button-3`.

---

### 5. templates/alerts.html
- Page Title: Weather Alerts
- Main Heading: <h1 id="alerts-page">Weather Alerts</h1>
- Elements:
  - alerts-page (Div): main container
  - alerts-list (Div): container listing alerts
  - severity-filter (Dropdown): filter alerts by severity
  - location-filter-alerts (Dropdown): filter alerts by location
  - acknowledge-alert-button-{alert_id} (Button): per alert, acknowledge button
- Navigation:
  - No explicit navigation buttons indicated
- Context Variables:
  - alerts: list of dict
  - severity_filter: str
  - location_filter: int
- Notes: Dynamic IDs for acknowledge-alert-button must include alert_id, e.g., `acknowledge-alert-button-5`.

---

### 6. templates/air_quality.html
- Page Title: Air Quality Index
- Main Heading: <h1 id="air-quality-page">Air Quality Index</h1>
- Elements:
  - air-quality-page (Div): main container
  - aqi-display (Div): displays AQI numeric value
  - aqi-description (Div): text description of AQI
  - pollution-details (Table): table listing PM2.5, PM10, NO2, O3 levels
  - location-aqi-filter (Dropdown): filter pollution info by location
  - health-recommendation (Div): health tips based on AQI
- Navigation:
  - No navigation buttons detailed
- Context Variables:
  - air_quality: list of dict
  - location_filter: int
- Notes: Use table rows for pollutant details.

---

### 7. templates/saved_locations.html
- Page Title: Saved Locations
- Main Heading: <h1 id="saved-locations-page">Saved Locations</h1>
- Elements:
  - saved-locations-page (Div): main container
  - locations-table (Table): lists saved locations with columns: Location Name, Current Temp, Weather Condition
  - view-location-weather-{location_id} (Button): per location, button to view weather
  - remove-location-button-{location_id} (Button): per location, button to remove saved location
  - add-new-location-button (Button): add new location
- Navigation:
  - view-location-weather-buttons link to `url_for('current_weather_page', location_id=location_id)`
  - add-new-location-button navigates to `url_for('location_search_page')`
- Context Variables:
  - saved_locations: list of dict
  - weather_summary: dict (location_id mapped to temperature and condition)
- Notes: Dynamic button IDs must embed location_id value.

---

### 8. templates/settings.html
- Page Title: Settings
- Main Heading: <h1 id="settings-page">Settings</h1>
- Elements:
  - settings-page (Div): main container
  - temperature-unit-select (Dropdown): units selection (Celsius, Fahrenheit, Kelvin)
  - default-location-select (Dropdown): select default location
  - alert-notifications-toggle (Checkbox): toggle alert notifications
  - save-settings-button (Button): save changes
  - back-to-dashboard (Button): back to dashboard
- Navigation:
  - back-to-dashboard uses `url_for('dashboard_page')`
- Context Variables:
  - temperature_units: str
  - default_location_id: int
  - alert_notifications_enabled: bool
- Notes: Form submission triggers POST to save settings.

---

## Section 3: Data File Schemas

### 1. current_weather.txt
- File Path: data/current_weather.txt
- Field Order (pipe-delimited):
  1. location_id (int) - Unique location identifier
  2. location_name (str) - Name of the location
  3. temperature (int) - Current temperature
  4. condition (str) - Weather condition (Sunny, Rainy, etc.)
  5. humidity (int) - Humidity percentage
  6. wind_speed (int) - Wind speed in mph
  7. last_updated (str) - Timestamp YYYY-MM-DD HH:MM
- Data Description: Contains current weather conditions for multiple locations.
- Example Lines:
  ```
  1|New York|72|Sunny|65|10|2025-01-20 14:30
  2|London|55|Rainy|80|15|2025-01-20 14:30
  3|Tokyo|45|Cloudy|72|8|2025-01-20 14:30
  ```

---

### 2. forecasts.txt
- File Path: data/forecasts.txt
- Field Order (pipe-delimited):
  1. forecast_id (int) - Unique forecast record identifier
  2. location_id (int) - Location identifier
  3. date (str) - Date of forecast YYYY-MM-DD
  4. high_temp (int) - Predicted high temperature
  5. low_temp (int) - Predicted low temperature
  6. condition (str) - Weather condition
  7. precipitation (int) - Precipitation percentage
  8. humidity (int) - Humidity percentage
- Data Description: Seven-day weather forecasts for locations.
- Example Lines:
  ```
  1|1|2025-01-21|75|60|Sunny|0|60
  2|1|2025-01-22|68|55|Cloudy|10|70
  3|2|2025-01-21|58|48|Rainy|80|85
  ```

---

### 3. locations.txt
- File Path: data/locations.txt
- Field Order (pipe-delimited):
  1. location_id (int) - Unique location identifier
  2. location_name (str) - Name of the city/location
  3. latitude (float) - Latitude coordinate
  4. longitude (float) - Longitude coordinate
  5. country (str) - Country name
  6. timezone (str) - Timezone identifier
- Data Description: Stores supported locations and their geo data.
- Example Lines:
  ```
  1|New York|40.7128|-74.0060|USA|EST
  2|London|51.5074|-0.1278|UK|GMT
  3|Tokyo|35.6762|139.6503|Japan|JST
  ```

---

### 4. alerts.txt
- File Path: data/alerts.txt
- Field Order (pipe-delimited):
  1. alert_id (int) - Unique alert identifier
  2. location_id (int) - Location identifier
  3. alert_type (str) - Type of alert (Thunderstorm etc.)
  4. severity (str) - Severity level (Critical, High, Medium, Low)
  5. description (str) - Description text of alert
  6. start_time (str) - Start timestamp YYYY-MM-DD HH:MM
  7. end_time (str) - End timestamp YYYY-MM-DD HH:MM
  8. is_acknowledged (int) - 0 = not acknowledged, 1 = acknowledged
- Data Description: Active weather alerts for locations.
- Example Lines:
  ```
  1|1|Thunderstorm|High|Severe thunderstorm warning in effect until 8 PM|2025-01-20 14:00|2025-01-20 20:00|0
  2|2|Fog|Medium|Dense fog advisory in effect until noon tomorrow|2025-01-20 06:00|2025-01-21 12:00|0
  3|1|Wind|Medium|High wind advisory with gusts up to 45 mph|2025-01-20 15:00|2025-01-21 09:00|1
  ```

---

### 5. air_quality.txt
- File Path: data/air_quality.txt
- Field Order (pipe-delimited):
  1. aqi_id (int) - Unique air quality record identifier
  2. location_id (int) - Location identifier
  3. aqi_index (int) - Air Quality Index (0-500)
  4. pm25 (float) - PM2.5 value
  5. pm10 (float) - PM10 value
  6. no2 (float) - NO2 measurement
  7. o3 (float) - O3 measurement
  8. last_updated (str) - Timestamp YYYY-MM-DD HH:MM
- Data Description: Air quality details per location.
- Example Lines:
  ```
  1|1|45|12.5|35|28|55|2025-01-20 14:30
  2|2|67|22.3|48|42|78|2025-01-20 14:30
  3|3|120|68.5|95|65|110|2025-01-20 14:30
  ```

---

### 6. saved_locations.txt
- File Path: data/saved_locations.txt
- Field Order (pipe-delimited):
  1. saved_id (int) - Unique saved location record
  2. user_id (int) - User identifier (dummy since no auth)
  3. location_id (int) - Location identifier
  4. location_name (str) - Location name
  5. is_default (int) - 1 = default location, 0 = not default
- Data Description: Stores user saved locations and default flag.
- Example Lines:
  ```
  1|1|1|New York|1
  2|1|2|London|0
  3|2|3|Tokyo|1
  ```

---

---

This completes the detailed design specification for all routes, templates, and data schemas of the WeatherForecast application.
Backend and frontend developers can proceed independently using this specification.
