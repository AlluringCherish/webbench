# WeatherForecast Application Design Specification

---

## Section 1: Flask Routes Specification

### 1. Root Route
- URL Path: `/`
- Methods: GET
- Function Name: `root_redirect`
- Action: Redirects to dashboard page (URL `/dashboard`)
- Template: None (redirect)
- Context Variables: None

### 2. Dashboard Page
- URL Path: `/dashboard`
- Methods: GET
- Function Name: `dashboard`
- Template Filename: `dashboard.html`
- Context Variables:
  - `default_location` (dict):
    - `location_id` (int)
    - `location_name` (str)
    - `temperature` (float or int)
    - `condition` (str)
    - `humidity` (int)
    - `wind_speed` (int)
  - `saved_locations_count` (int): Count of saved locations for quick access

### 3. Current Weather Page
- URL Path: `/weather/current/<int:location_id>`
- Methods: GET
- Function Name: `current_weather`
- Template Filename: `current_weather.html`
- Context Variables:
  - `location_name` (str)
  - `temperature` (float or int)
  - `condition` (str)
  - `humidity` (int)
  - `wind_speed` (int)

### 4. Weekly Forecast Page
- URL Path: `/forecast/weekly`
- Methods: GET
- Function Name: `weekly_forecast`
- Template Filename: `weekly_forecast.html`
- Context Variables:
  - `locations` (list of dicts): Each dict contains:
    - `location_id` (int)
    - `location_name` (str)
  - `selected_location_id` (int): Currently selected location for forecast filter
  - `forecasts` (list of dicts): Each dict has fields:
    - `forecast_id` (int)
    - `location_id` (int)
    - `date` (str, format YYYY-MM-DD)
    - `high_temp` (float or int)
    - `low_temp` (float or int)
    - `condition` (str)
    - `precipitation` (int)
    - `humidity` (int)

### 5. Location Search Page
- URL Path: `/locations/search`
- Methods: GET, POST
- Function Name: `search_locations`
- Template Filename: `search_locations.html`
- Context Variables:
  - `search_query` (str): Input query string from user (empty or None if GET)
  - `search_results` (list of dicts): Matching locations with fields:
    - `location_id` (int)
    - `location_name` (str)
    - `country` (str)
    - `latitude` (float)
    - `longitude` (float)
  - `saved_locations` (list of dicts): Previously saved locations with same structure as `search_results`

### 6. Weather Alerts Page
- URL Path: `/alerts`
- Methods: GET
- Function Name: `weather_alerts`
- Template Filename: `alerts.html`
- Context Variables:
  - `alerts` (list of dicts): Each alert dict has:
    - `alert_id` (int)
    - `location_id` (int)
    - `alert_type` (str)
    - `severity` (str)
    - `description` (str)
    - `start_time` (str, datetime format)
    - `end_time` (str, datetime format)
    - `is_acknowledged` (bool)
  - `severity_levels` (list of str): Fixed list ["All", "Critical", "High", "Medium", "Low"]
  - `locations` (list of dicts): Each with `location_id` (int) and `location_name` (str)
  - `selected_severity` (str): Currently selected severity filter
  - `selected_location_id` (int or None): Currently selected location filter

### 7. Air Quality Page
- URL Path: `/airquality`
- Methods: GET
- Function Name: `air_quality`
- Template Filename: `air_quality.html`
- Context Variables:
  - `aqi_data` (dict):
    - `aqi_index` (int)
    - `description` (str)
    - `pm25` (float)
    - `pm10` (float)
    - `no2` (float)
    - `o3` (float)
  - `locations` (list of dicts): Each dict with `location_id` (int) and `location_name` (str)
  - `selected_location_id` (int)
  - `health_recommendation` (str)

### 8. Saved Locations Page
- URL Path: `/locations/saved`
- Methods: GET
- Function Name: `saved_locations`
- Template Filename: `saved_locations.html`
- Context Variables:
  - `saved_locations` (list of dicts): Each dict fields:
    - `saved_id` (int)
    - `location_id` (int)
    - `location_name` (str)
    - `temperature` (float or int)
    - `condition` (str)
    - `is_default` (bool)

### 9. Settings Page
- URL Path: `/settings`
- Methods: GET, POST
- Function Name: `settings`
- Template Filename: `settings.html`
- Context Variables:
  - `temperature_units` (list of str): ["Celsius", "Fahrenheit", "Kelvin"]
  - `default_location_id` (int)
  - `locations` (list of dicts): Each dict with `location_id` (int), `location_name` (str)
  - `alert_notifications_enabled` (bool)

---

## Section 2: Frontend HTML Templates Specification

### 1. templates/dashboard.html
- Page Title: "Weather Dashboard"
- Element IDs:
  - `dashboard-page` (Div): Container of dashboard page
  - `current-weather-summary` (Div): Displays current weather summary for default location
  - `search-location-button` (Button): Navigates to `search_locations`
  - `view-forecast-button` (Button): Navigates to `weekly_forecast`
  - `view-alerts-button` (Button): Navigates to `weather_alerts`
- Navigation Mapping:
  - `search-location-button` -> `url_for('search_locations')`
  - `view-forecast-button` -> `url_for('weekly_forecast')`
  - `view-alerts-button` -> `url_for('weather_alerts')`
- Context variables:
  - `default_location` (dict) with keys: `location_id`, `location_name`, `temperature`, `condition`, `humidity`, `wind_speed`
  - `saved_locations_count` (int)
- Usage Notes:
  - Display default location weather summary inside `current-weather-summary` div
  - Button clicks navigate to respective pages

### 2. templates/current_weather.html
- Page Title: "Current Weather"
- Element IDs:
  - `current-weather-page` (Div): Container for current weather page
  - `location-name` (H1): Displays selected location name
  - `temperature-display` (Div): Displays current temperature
  - `weather-condition` (Div): Displays weather condition
  - `humidity-info` (Div): Displays humidity percentage
  - `wind-speed-info` (Div): Displays wind speed
- Navigation:
  - Provide navigation to dashboard page if needed (no explicit button specified)
- Context variables:
  - `location_name` (str)
  - `temperature` (float or int)
  - `condition` (str)
  - `humidity` (int)
  - `wind_speed` (int)
- Usage Notes:
  - Populate elements with the respective data

### 3. templates/weekly_forecast.html
- Page Title: "Weekly Forecast"
- Element IDs:
  - `forecast-page` (Div): Main container
  - `forecast-table` (Table): Displays daily forecasts with columns date, high temp, low temp, condition
  - `location-filter` (Dropdown): To filter forecasts by location
  - `forecast-list` (Div): Grid displaying forecast cards for each day
  - `back-to-dashboard` (Button): Navigates back to dashboard
- Navigation:
  - `back-to-dashboard` -> `url_for('dashboard')`
- Context Variables:
  - `locations` (list of dicts with `location_id` (int), `location_name` (str))
  - `selected_location_id` (int)
  - `forecasts` (list of dicts with keys: `forecast_id`, `location_id`, `date`, `high_temp`, `low_temp`, `condition`, `precipitation`, `humidity`)
- Usage Notes:
  - Use `location-filter` dropdown to filter `forecasts` by `selected_location_id`
  - Loop over `forecasts` to populate `forecast-table` and `forecast-list`

### 4. templates/search_locations.html
- Page Title: "Search Locations"
- Element IDs:
  - `search-page` (Div): Container
  - `location-search-input` (Input): Text input for search queries
  - `search-results` (Div): Container for search results
  - `select-location-button-{location_id}` (Button): Button to select each location; `{location_id}` is dynamic
  - `saved-locations-list` (Div): Displays saved locations
- Navigation:
  - Navigation buttons or links to other pages if needed (not specified)
- Context Variables:
  - `search_query` (str)
  - `search_results` (list of dicts: `location_id`, `location_name`, `country`, `latitude`, `longitude`)
  - `saved_locations` (list of dicts: same fields)
- Usage Notes:
  - Render search results dynamically, each with a button id `select-location-button-{location_id}`
  - Display saved locations in `saved-locations-list`

### 5. templates/alerts.html
- Page Title: "Weather Alerts"
- Element IDs:
  - `alerts-page` (Div): Page container
  - `alerts-list` (Div): List of active alerts
  - `severity-filter` (Dropdown): Filter alerts by severity
  - `location-filter-alerts` (Dropdown): Filter alerts by location
  - `acknowledge-alert-button-{alert_id}` (Button): Acknowledge alert button for each alert; `{alert_id}` dynamic
- Navigation:
  - Navigation to dashboard or other pages if needed
- Context Variables:
  - `alerts` (list of dicts with keys: `alert_id`, `location_id`, `alert_type`, `severity`, `description`, `start_time`, `end_time`, `is_acknowledged`)
  - `severity_levels` (list of str): ["All", "Critical", "High", "Medium", "Low"]
  - `locations` (list of dicts with `location_id`, `location_name`)
  - `selected_severity` (str)
  - `selected_location_id` (int or None)
- Usage Notes:
  - Loop over `alerts` to display each alert with acknowledge button
  - Use filters to update displayed alerts dynamically

### 6. templates/air_quality.html
- Page Title: "Air Quality Index"
- Element IDs:
  - `air-quality-page` (Div): Container
  - `aqi-display` (Div): Shows air quality index value
  - `aqi-description` (Div): Description of air quality
  - `pollution-details` (Table): Shows pollutants PM2.5, PM10, NO2, O3 levels
  - `location-aqi-filter` (Dropdown): Filter air quality data by location
  - `health-recommendation` (Div): Shows health advice based on air quality
- Navigation:
  - Navigation to dashboard or other pages if needed
- Context Variables:
  - `aqi_data` (dict): `aqi_index` (int), `description` (str), `pm25` (float), `pm10` (float), `no2` (float), `o3` (float)
  - `locations` (list of dicts with `location_id`, `location_name`)
  - `selected_location_id` (int)
  - `health_recommendation` (str)
- Usage Notes:
  - Render pollutant levels in `pollution-details` table
  - Update displayed data upon location filter changes

### 7. templates/saved_locations.html
- Page Title: "Saved Locations"
- Element IDs:
  - `saved-locations-page` (Div): Container
  - `locations-table` (Table): Displays saved locations data
  - `view-location-weather-{location_id}` (Button): Button to view weather for each location
  - `remove-location-button-{location_id}` (Button): Button to remove saved location
  - `add-new-location-button` (Button): To add new location
- Navigation:
  - Navigation to dashboard or other pages if needed
- Context Variables:
  - `saved_locations` (list of dicts with keys: `saved_id`, `location_id`, `location_name`, `temperature`, `condition`, `is_default`)
- Usage Notes:
  - Loop over `saved_locations` to populate `locations-table` with buttons using dynamic IDs

### 8. templates/settings.html
- Page Title: "Settings"
- Element IDs:
  - `settings-page` (Div): Container
  - `temperature-unit-select` (Dropdown): Select temperature unit
  - `default-location-select` (Dropdown): Select default location
  - `alert-notifications-toggle` (Checkbox): Enable/disable alert notifications
  - `save-settings-button` (Button): Save changes
  - `back-to-dashboard` (Button): Navigate back to dashboard
- Navigation:
  - `back-to-dashboard` -> `url_for('dashboard')`
- Context Variables:
  - `temperature_units` (list of str): ["Celsius", "Fahrenheit", "Kelvin"]
  - `default_location_id` (int)
  - `locations` (list of dicts with `location_id`, `location_name`)
  - `alert_notifications_enabled` (bool)
- Usage Notes:
  - Populate dropdowns with available options
  - Reflect current settings in inputs

---

## Section 3: Data File Schemas

### 1. data/current_weather.txt
- File Path: `data/current_weather.txt`
- Format (pipe-delimited):
  `location_id|location_name|temperature|condition|humidity|wind_speed|last_updated`
- Field Descriptions:
  - `location_id` (int): Unique identifier for location
  - `location_name` (str): Name of the location
  - `temperature` (float or int): Current temperature
  - `condition` (str): Weather condition description
  - `humidity` (int): Humidity percentage
  - `wind_speed` (int): Wind speed value
  - `last_updated` (str): Datetime string `YYYY-MM-DD HH:MM`
- Example Lines:
  ```
  1|New York|72|Sunny|65|10|2025-01-20 14:30
  2|London|55|Rainy|80|15|2025-01-20 14:30
  3|Tokyo|45|Cloudy|72|8|2025-01-20 14:30
  ```

### 2. data/forecasts.txt
- File Path: `data/forecasts.txt`
- Format (pipe-delimited):
  `forecast_id|location_id|date|high_temp|low_temp|condition|precipitation|humidity`
- Field Descriptions:
  - `forecast_id` (int): Unique forecast record ID
  - `location_id` (int): Location identifier
  - `date` (str): Forecast date in `YYYY-MM-DD`
  - `high_temp` (float or int): High temperature forecast
  - `low_temp` (float or int): Low temperature forecast
  - `condition` (str): Weather condition description
  - `precipitation` (int): Precipitation percentage
  - `humidity` (int): Humidity percentage
- Example Lines:
  ```
  1|1|2025-01-21|75|60|Sunny|0|60
  2|1|2025-01-22|68|55|Cloudy|10|70
  3|2|2025-01-21|58|48|Rainy|80|85
  ```

### 3. data/locations.txt
- File Path: `data/locations.txt`
- Format (pipe-delimited):
  `location_id|location_name|latitude|longitude|country|timezone`
- Field Descriptions:
  - `location_id` (int): Unique location identifier
  - `location_name` (str): Name of location
  - `latitude` (float): Latitude coordinate
  - `longitude` (float): Longitude coordinate
  - `country` (str): Country name
  - `timezone` (str): Time zone of location
- Example Lines:
  ```
  1|New York|40.7128|-74.0060|USA|EST
  2|London|51.5074|-0.1278|UK|GMT
  3|Tokyo|35.6762|139.6503|Japan|JST
  ```

### 4. data/alerts.txt
- File Path: `data/alerts.txt`
- Format (pipe-delimited):
  `alert_id|location_id|alert_type|severity|description|start_time|end_time|is_acknowledged`
- Field Descriptions:
  - `alert_id` (int): Unique alert identifier
  - `location_id` (int): Location identifier
  - `alert_type` (str): Type of alert
  - `severity` (str): Severity level (Critical, High, Medium, Low)
  - `description` (str): Alert details
  - `start_time` (str): Alert start datetime `YYYY-MM-DD HH:MM`
  - `end_time` (str): Alert end datetime `YYYY-MM-DD HH:MM`
  - `is_acknowledged` (int or bool): 0 (false) or 1 (true), whether alert is acknowledged
- Example Lines:
  ```
  1|1|Thunderstorm|High|Severe thunderstorm warning in effect until 8 PM|2025-01-20 14:00|2025-01-20 20:00|0
  2|2|Fog|Medium|Dense fog advisory in effect until noon tomorrow|2025-01-20 06:00|2025-01-21 12:00|0
  3|1|Wind|Medium|High wind advisory with gusts up to 45 mph|2025-01-20 15:00|2025-01-21 09:00|1
  ```

### 5. data/air_quality.txt
- File Path: `data/air_quality.txt`
- Format (pipe-delimited):
  `aqi_id|location_id|aqi_index|pm25|pm10|no2|o3|last_updated`
- Field Descriptions:
  - `aqi_id` (int): Unique air quality record ID
  - `location_id` (int): Location identifier
  - `aqi_index` (int): Air Quality Index (0-500)
  - `pm25` (float): PM2.5 level
  - `pm10` (float): PM10 level
  - `no2` (float): NO2 level
  - `o3` (float): O3 level
  - `last_updated` (str): Datetime `YYYY-MM-DD HH:MM`
- Example Lines:
  ```
  1|1|45|12.5|35|28|55|2025-01-20 14:30
  2|2|67|22.3|48|42|78|2025-01-20 14:30
  3|3|120|68.5|95|65|110|2025-01-20 14:30
  ```

### 6. data/saved_locations.txt
- File Path: `data/saved_locations.txt`
- Format (pipe-delimited):
  `saved_id|user_id|location_id|location_name|is_default`
- Field Descriptions:
  - `saved_id` (int): Unique saved location record ID
  - `user_id` (int): User identifier (note: given no authentication, user_id can be constant or optional)
  - `location_id` (int): Location identifier
  - `location_name` (str): Name of location
  - `is_default` (int or bool): 1 if default location, else 0
- Example Lines:
  ```
  1|1|1|New York|1
  2|1|2|London|0
  3|2|3|Tokyo|1
  ```

---

This design specification covers all routes, templates, and data files as required to enable independent frontend and backend development.
