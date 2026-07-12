# Design Specification Document for WeatherForecast Web Application

---

## Section 1: Flask Routes Specification

### 1. Root Route
- URL Path: `/`
- HTTP Methods: GET
- Function Name: `root_redirect`
- Template: None (Redirect)
- Behavior: Redirects to `/dashboard`
- Context Variables: None

---

### 2. Dashboard Page
- URL Path: `/dashboard`
- HTTP Methods: GET
- Function Name: `dashboard`
- Template: `dashboard.html`
- Context Variables:
  - default_location: dict
    - Fields:
      - location_id (int)
      - location_name (str)
      - temperature (float)
      - condition (str)
- Notes: default_location contains current weather summary data for default location.

---

### 3. Current Weather Page
- URL Path: `/weather/current/<int:location_id>`
- HTTP Methods: GET
- Function Name: `current_weather`
- Template: `current_weather.html`
- Context Variables:
  - weather_details: dict
    - location_name (str)
    - temperature (float)
    - condition (str)
    - humidity (int)
    - wind_speed (int)
- Notes: weather_details provides detailed current weather for the given location_id.

---

### 4. Weekly Forecast Page
- URL Path: `/forecast/weekly`
- HTTP Methods: GET, POST
- Function Name: `weekly_forecast`
- Template: `weekly_forecast.html`
- Context Variables:
  - location_list: list of dict
    - location_id (int)
    - location_name (str)
  - selected_location_id: int
  - forecast_list: list of dict
    - date (str, ISO `YYYY-MM-DD`)
    - high_temp (float)
    - low_temp (float)
    - condition (str)
- Notes: POST to filter forecast by selected_location_id; GET provides forecast for default or first location.

---

### 5. Location Search Page
- URL Path: `/locations/search`
- HTTP Methods: GET, POST
- Function Name: `location_search`
- Template: `location_search.html`
- Context Variables:
  - search_query: str
  - search_results: list of dict
    - location_id (int)
    - location_name (str)
    - latitude (float)
    - longitude (float)
  - saved_locations: list of dict
    - location_id (int)
    - location_name (str)
- Notes: POST request to perform search by city name or coordinates; GET request shows saved locations and empty search.

---

### 6. Weather Alerts Page
- URL Path: `/alerts`
- HTTP Methods: GET, POST
- Function Name: `weather_alerts`
- Template: `weather_alerts.html`
- Context Variables:
  - alerts: list of dict
    - alert_id (int)
    - location_id (int)
    - alert_type (str)
    - severity (str)  # One of Critical, High, Medium, Low
    - description (str)
    - start_time (str, format `YYYY-MM-DD HH:MM`)
    - end_time (str, format `YYYY-MM-DD HH:MM`)
    - is_acknowledged (bool)
    - location_name (str)
  - severity_filter: str (values: All, Critical, High, Medium, Low)
  - location_filter: int or None
- Notes: POST used for filtering alerts or acknowledging.

---

### 7. Air Quality Page
- URL Path: `/air_quality`
- HTTP Methods: GET, POST
- Function Name: `air_quality`
- Template: `air_quality.html`
- Context Variables:
  - aqi_info: dict
    - aqi_index (int)
    - aqi_description (str)
    - pm25 (float)
    - pm10 (float)
    - no2 (float)
    - o3 (float)
    - last_updated (str, format `YYYY-MM-DD HH:MM`)
  - location_list: list of dict
    - location_id (int)
    - location_name (str)
  - selected_location_id: int
  - health_recommendation: str
- Notes: POST used for filtering by location.

---

### 8. Saved Locations Page
- URL Path: `/locations/saved`
- HTTP Methods: GET, POST
- Function Name: `saved_locations`
- Template: `saved_locations.html`
- Context Variables:
  - saved_locations: list of dict
    - location_id (int)
    - location_name (str)
    - temperature (float)
    - condition (str)
    - is_default (bool)
  - user_id (int)  # if applicable (can be fixed as 1 or omitted, given no authentication)
- Notes: POST methods for adding/removing default status or deleting saved locations.

---

### 9. Settings Page
- URL Path: `/settings`
- HTTP Methods: GET, POST
- Function Name: `settings`
- Template: `settings.html`
- Context Variables:
  - temperature_unit: str  # One of Celsius, Fahrenheit, Kelvin
  - default_location_id: int
  - location_list: list of dict
    - location_id (int)
    - location_name (str)
  - alert_notifications_enabled: bool
- Notes: POST to save updated settings.

---

## Section 2: Frontend HTML Templates Specification

### Template 1: Dashboard
- File: `templates/dashboard.html`
- Page Title: "Weather Dashboard"
- Main Heading: "Weather Dashboard" (within element `dashboard-page`)
- Element IDs:
  - `dashboard-page` (div): container div for dashboard page
  - `current-weather-summary` (div): shows current weather info for default location
  - `search-location-button` (button): navigates to location search page (url_for 'location_search')
  - `view-forecast-button` (button): navigates to weekly forecast page (url_for 'weekly_forecast')
  - `view-alerts-button` (button): navigates to weather alerts page (url_for 'weather_alerts')
- Navigation Links:
  - `search-location-button` → url_for('location_search')
  - `view-forecast-button` → url_for('weekly_forecast')
  - `view-alerts-button` → url_for('weather_alerts')
- Context Variables:
  - `default_location`: dict with keys:
    - `location_id` (int)
    - `location_name` (str)
    - `temperature` (float)
    - `condition` (str)
- Usage Notes:
  - Render current weather summary inside `current-weather-summary`
  - Static navigation button actions

---

### Template 2: Current Weather
- File: `templates/current_weather.html`
- Page Title: "Current Weather"
- Main Heading: Location name inside `<h1>` with ID `location-name`
- Element IDs:
  - `current-weather-page` (div): container for page
  - `location-name` (h1): displays location name
  - `temperature-display` (div): shows current temperature
  - `weather-condition` (div): shows current condition
  - `humidity-info` (div): shows humidity percentage
  - `wind-speed-info` (div): shows wind speed
- Navigation Links:
  - Back to dashboard usually implemented via a separate button or link (not specified in elements but recommended)
- Context Variables:
  - `weather_details`: dict with keys:
    - `location_name` (str)
    - `temperature` (float)
    - `condition` (str)
    - `humidity` (int)
    - `wind_speed` (int)
- Usage Notes:
  - Show detailed weather data
  - Single location based on URL parameter

---

### Template 3: Weekly Forecast
- File: `templates/weekly_forecast.html`
- Page Title: "Weekly Forecast"
- Main Heading: Could be in `forecast-page` div
- Element IDs:
  - `forecast-page` (div): container
  - `forecast-table` (table): displays daily forecast data
  - `location-filter` (dropdown): select location to filter forecasts
  - `forecast-list` (div): grid of forecast cards for each day
  - `back-to-dashboard` (button): navigates back to dashboard (url_for 'dashboard')
- Navigation Links:
  - `back-to-dashboard` → url_for('dashboard')
- Context Variables:
  - `location_list`: list of dicts each with `location_id` (int), `location_name` (str)
  - `selected_location_id`: int
  - `forecast_list`: list of dicts each with:
    - `date` (str)
    - `high_temp` (float)
    - `low_temp` (float)
    - `condition` (str)
- Usage Notes:
  - Loop forecast_list to build table or days cards
  - Dropdown selection triggers POST to filter forecasts

---

### Template 4: Location Search
- File: `templates/location_search.html`
- Page Title: "Search Locations"
- Main Heading: Probably inside `search-page` div
- Element IDs:
  - `search-page` (div): container
  - `location-search-input` (input): text input for city or coordinates
  - `search-results` (div): container for search results
  - `select-location-button-{location_id}` (button): each search result has this button
  - `saved-locations-list` (div): shows previously saved locations
- Navigation Links:
  - Selecting a location triggers a POST or redirect to current weather or saved locations update
- Context Variables:
  - `search_query`: str
  - `search_results`: list of dicts with:
    - `location_id` (int)
    - `location_name` (str)
    - `latitude` (float)
    - `longitude` (float)
  - `saved_locations`: list of dicts with:
    - `location_id` (int)
    - `location_name` (str)
- Usage Notes:
  - Render search results with dynamic `select-location-button-{location_id}` IDs
  - Render saved locations list

---

### Template 5: Weather Alerts
- File: `templates/weather_alerts.html`
- Page Title: "Weather Alerts"
- Main Heading: Could be inside `alerts-page` div
- Element IDs:
  - `alerts-page` (div): container
  - `alerts-list` (div): contains alert entries
  - `severity-filter` (dropdown): filter alerts by severity
  - `location-filter-alerts` (dropdown): filter alerts by location
  - `acknowledge-alert-button-{alert_id}` (button): each alert has this acknowledge button
- Navigation Links:
  - Filter controls POST to same route
- Context Variables:
  - `alerts`: list of dicts with:
    - `alert_id` (int)
    - `location_id` (int)
    - `alert_type` (str)
    - `severity` (str)
    - `description` (str)
    - `start_time` (str)
    - `end_time` (str)
    - `is_acknowledged` (bool)
    - `location_name` (str)
  - `severity_filter`: str
  - `location_filter`: int or None
- Usage Notes:
  - Render list with dynamic acknowledge buttons
  - Dropdown filters

---

### Template 6: Air Quality
- File: `templates/air_quality.html`
- Page Title: "Air Quality Index"
- Main Heading: In `air-quality-page` div
- Element IDs:
  - `air-quality-page` (div): container
  - `aqi-display` (div): displays AQI value
  - `aqi-description` (div): textual AQI description
  - `pollution-details` (table): shows pollutant values PM2.5, PM10, NO2, O3
  - `location-aqi-filter` (dropdown): selects location
  - `health-recommendation` (div): shows health advice
- Navigation Links:
  - Location filter triggers POST
- Context Variables:
  - `aqi_info`: dict with:
    - `aqi_index` (int)
    - `aqi_description` (str)
    - `pm25` (float)
    - `pm10` (float)
    - `no2` (float)
    - `o3` (float)
    - `last_updated` (str)
  - `location_list`: list of dict
  - `selected_location_id`: int
  - `health_recommendation`: str
- Usage Notes:
  - Render pollutant levels in table
  - Show dynamic AQI and description based on selected location

---

### Template 7: Saved Locations
- File: `templates/saved_locations.html`
- Page Title: "Saved Locations"
- Main Heading: In `saved-locations-page` div
- Element IDs:
  - `saved-locations-page` (div): container
  - `locations-table` (table): lists saved locations with current temperature and condition
  - `view-location-weather-{location_id}` (button): each location has button to view weather
  - `remove-location-button-{location_id}` (button): button to remove location
  - `add-new-location-button` (button): adds new location
- Navigation Links:
  - View weather button → url_for('current_weather', location_id=location_id)
- Context Variables:
  - `saved_locations`: list of dict with:
    - `location_id` (int)
    - `location_name` (str)
    - `temperature` (float)
    - `condition` (str)
    - `is_default` (bool)
- Usage Notes:
  - Render table rows dynamically
  - Buttons have dynamic IDs

---

### Template 8: Settings
- File: `templates/settings.html`
- Page Title: "Settings"
- Main Heading: In `settings-page` div
- Element IDs:
  - `settings-page` (div): container
  - `temperature-unit-select` (dropdown): unit selection
  - `default-location-select` (dropdown): default location selection
  - `alert-notifications-toggle` (checkbox): enable/disable notifications
  - `save-settings-button` (button): save settings
  - `back-to-dashboard` (button): navigate back to dashboard
- Navigation Links:
  - `back-to-dashboard` → url_for('dashboard')
- Context Variables:
  - `temperature_unit`: str
  - `default_location_id`: int
  - `location_list`: list of dict
    - `location_id` (int)
    - `location_name` (str)
  - `alert_notifications_enabled`: bool
- Usage Notes:
  - Render dropdowns pre-selected to current settings
  - Checkbox reflects current notification preference

---

## Section 3: Data File Schemas

### 1. Current Weather Data
- File: `data/current_weather.txt`
- Format:
  ```
  location_id|location_name|temperature|condition|humidity|wind_speed|last_updated
  ```
- Field Descriptions:
  - `location_id` (int): Unique identifier of the location
  - `location_name` (str): Name of the location
  - `temperature` (float): Current temperature in default unit
  - `condition` (str): Weather condition description
  - `humidity` (int): Percentage humidity
  - `wind_speed` (int): Wind speed in mph
  - `last_updated` (str): Timestamp in `YYYY-MM-DD HH:MM` format
- Example lines:
  ```
  1|New York|72|Sunny|65|10|2025-01-20 14:30
  2|London|55|Rainy|80|15|2025-01-20 14:30
  3|Tokyo|45|Cloudy|72|8|2025-01-20 14:30
  ```

---

### 2. Forecasts Data
- File: `data/forecasts.txt`
- Format:
  ```
  forecast_id|location_id|date|high_temp|low_temp|condition|precipitation|humidity
  ```
- Field Descriptions:
  - `forecast_id` (int): Unique identifier for the forecast entry
  - `location_id` (int): Location identifier
  - `date` (str): Date of forecast (YYYY-MM-DD)
  - `high_temp` (float): High temperature for the day
  - `low_temp` (float): Low temperature for the day
  - `condition` (str): Weather condition
  - `precipitation` (int): Precipitation % chance
  - `humidity` (int): Humidity percentage
- Example lines:
  ```
  1|1|2025-01-21|75|60|Sunny|0|60
  2|1|2025-01-22|68|55|Cloudy|10|70
  3|2|2025-01-21|58|48|Rainy|80|85
  ```

---

### 3. Locations Data
- File: `data/locations.txt`
- Format:
  ```
  location_id|location_name|latitude|longitude|country|timezone
  ```
- Field Descriptions:
  - `location_id` (int): Unique location identifier
  - `location_name` (str): Name of the location
  - `latitude` (float): Latitude coordinate
  - `longitude` (float): Longitude coordinate
  - `country` (str): Country name
  - `timezone` (str): Timezone abbreviation
- Example lines:
  ```
  1|New York|40.7128|-74.0060|USA|EST
  2|London|51.5074|-0.1278|UK|GMT
  3|Tokyo|35.6762|139.6503|Japan|JST
  ```

---

### 4. Weather Alerts Data
- File: `data/alerts.txt`
- Format:
  ```
  alert_id|location_id|alert_type|severity|description|start_time|end_time|is_acknowledged
  ```
- Field Descriptions:
  - `alert_id` (int): Unique alert identifier
  - `location_id` (int): Location reference
  - `alert_type` (str): Type of alert (e.g., Thunderstorm, Fog)
  - `severity` (str): Severity level (Critical, High, Medium, Low)
  - `description` (str): Alert description
  - `start_time` (str): Start timestamp `YYYY-MM-DD HH:MM`
  - `end_time` (str): End timestamp `YYYY-MM-DD HH:MM`
  - `is_acknowledged` (int): 0 for False, 1 for True
- Example lines:
  ```
  1|1|Thunderstorm|High|Severe thunderstorm warning in effect until 8 PM|2025-01-20 14:00|2025-01-20 20:00|0
  2|2|Fog|Medium|Dense fog advisory in effect until noon tomorrow|2025-01-20 06:00|2025-01-21 12:00|0
  3|1|Wind|Medium|High wind advisory with gusts up to 45 mph|2025-01-20 15:00|2025-01-21 09:00|1
  ```

---

### 5. Air Quality Data
- File: `data/air_quality.txt`
- Format:
  ```
  aqi_id|location_id|aqi_index|pm25|pm10|no2|o3|last_updated
  ```
- Field Descriptions:
  - `aqi_id` (int): Unique AQI record ID
  - `location_id` (int): Location reference
  - `aqi_index` (int): Air Quality Index (0-500)
  - `pm25` (float): PM2.5 level
  - `pm10` (float): PM10 level
  - `no2` (float): NO2 level
  - `o3` (float): O3 level
  - `last_updated` (str): Timestamp `YYYY-MM-DD HH:MM`
- Example lines:
  ```
  1|1|45|12.5|35|28|55|2025-01-20 14:30
  2|2|67|22.3|48|42|78|2025-01-20 14:30
  3|3|120|68.5|95|65|110|2025-01-20 14:30
  ```

---

### 6. Saved Locations Data
- File: `data/saved_locations.txt`
- Format:
  ```
  saved_id|user_id|location_id|location_name|is_default
  ```
- Field Descriptions:
  - `saved_id` (int): Unique saved location record
  - `user_id` (int): User ID who saved the location (no authentication; can be fixed or default)
  - `location_id` (int): Location identifier
  - `location_name` (str): Location name
  - `is_default` (int): 0 or 1 indicating default status
- Example lines:
  ```
  1|1|1|New York|1
  2|1|2|London|0
  3|2|3|Tokyo|1
  ```

---

# End of Design Specification
