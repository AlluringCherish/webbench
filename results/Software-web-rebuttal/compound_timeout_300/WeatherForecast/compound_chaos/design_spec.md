# WeatherForecast Web Application Design Specification

---

## Section 1: Flask Routes Specification

### 1. Root Route
- **URL Path:** `/`
- **HTTP Methods:** GET
- **Function Name:** `root_redirect`
- **Template:** None (redirect only)
- **Behavior:** Redirects to dashboard page `/dashboard`
- **Context Variables:** None


### 2. Dashboard Page
- **URL Path:** `/dashboard`
- **HTTP Methods:** GET
- **Function Name:** `dashboard`
- **Template:** `dashboard.html`
- **Context Variables:**
  - `default_location` (dict): Fields - `location_id` (int), `location_name` (str), `temperature` (int), `condition` (str), `humidity` (int), `wind_speed` (int), `last_updated` (str)


### 3. Current Weather Page
- **URL Path:** `/weather/current/<int:location_id>`
- **HTTP Methods:** GET
- **Function Name:** `current_weather`
- **Template:** `current_weather.html`
- **Context Variables:**
  - `location` (dict): Fields - `location_id` (int), `location_name` (str)
  - `temperature` (int)
  - `condition` (str)
  - `humidity` (int)
  - `wind_speed` (int)


### 4. Weekly Forecast Page
- **URL Path:** `/forecast/weekly`
- **HTTP Methods:** GET, POST
- **Function Name:** `weekly_forecast`
- **Template:** `weekly_forecast.html`
- **Context Variables:**
  - `locations` (list of dict): Each dict fields - `location_id` (int), `location_name` (str)
  - `selected_location_id` (int)
  - `forecasts` (list of dict): Each dict fields - `forecast_id` (int), `date` (str, YYYY-MM-DD), `high_temp` (int), `low_temp` (int), `condition` (str), `precipitation` (int), `humidity` (int)


### 5. Location Search Page
- **URL Path:** `/locations/search`
- **HTTP Methods:** GET, POST
- **Function Name:** `search_locations`
- **Template:** `location_search.html`
- **Context Variables:**
  - `search_query` (str)
  - `search_results` (list of dict): Each dict fields - `location_id` (int), `location_name` (str), `latitude` (float), `longitude` (float), `country` (str), `timezone` (str)
  - `saved_locations` (list of dict): Each dict fields - `location_id` (int), `location_name` (str), `latitude` (float), `longitude` (float), `country` (str), `timezone` (str)


### 6. Weather Alerts Page
- **URL Path:** `/alerts`
- **HTTP Methods:** GET, POST
- **Function Name:** `weather_alerts`
- **Template:** `weather_alerts.html`
- **Context Variables:**
  - `alerts` (list of dict): Each dict fields - `alert_id` (int), `location_id` (int), `alert_type` (str), `severity` (str), `description` (str), `start_time` (str), `end_time` (str), `is_acknowledged` (bool)
  - `severity_filter` (str) [Allowed values: "All", "Critical", "High", "Medium", "Low"]
  - `location_filter` (int or None) - location_id or None for all
  - `locations` (list of dict): Each dict fields - `location_id` (int), `location_name` (str)


### 7. Air Quality Page
- **URL Path:** `/air_quality`
- **HTTP Methods:** GET, POST
- **Function Name:** `air_quality`
- **Template:** `air_quality.html`
- **Context Variables:**
  - `locations` (list of dict): Each dict fields - `location_id` (int), `location_name` (str)
  - `selected_location_id` (int)
  - `aqi_info` (dict): Fields - `aqi_index` (int), `aqi_description` (str), `pm25` (float), `pm10` (float), `no2` (float), `o3` (float), `last_updated` (str)
  - `health_recommendation` (str)


### 8. Saved Locations Page
- **URL Path:** `/locations/saved`
- **HTTP Methods:** GET, POST
- **Function Name:** `saved_locations`
- **Template:** `saved_locations.html`
- **Context Variables:**
  - `saved_locations` (list of dict): Each dict fields - `saved_id` (int), `user_id` (int), `location_id` (int), `location_name` (str), `is_default` (bool)


### 9. Settings Page
- **URL Path:** `/settings`
- **HTTP Methods:** GET, POST
- **Function Name:** `settings`
- **Template:** `settings.html`
- **Context Variables:**
  - `temperature_units` (list of str): Options `["Celsius", "Fahrenheit", "Kelvin"]`
  - `selected_unit` (str)
  - `locations` (list of dict): Each dict fields - `location_id` (int), `location_name` (str)
  - `selected_default_location_id` (int)
  - `alert_notifications_enabled` (bool)


---

## Section 2: Frontend HTML Templates Specification

### 1. templates/dashboard.html
- **Page Title:** Weather Dashboard
- **Context Variables:**
  - `default_location` (dict): Fields - `location_id` (int), `location_name` (str), `temperature` (int), `condition` (str), `humidity` (int), `wind_speed` (int), `last_updated` (str)
- **Element IDs and Types:**
  - `dashboard-page` (Div): Container for the dashboard page.
  - `current-weather-summary` (Div): Displays the current weather summary of the default location.
  - `search-location-button` (Button): Navigates to `search_locations` route.
  - `view-forecast-button` (Button): Navigates to `weekly_forecast` route.
  - `view-alerts-button` (Button): Navigates to `weather_alerts` route.
- **Navigation Links:**
  - `search-location-button`: Calls `url_for('search_locations')`
  - `view-forecast-button`: Calls `url_for('weekly_forecast')`
  - `view-alerts-button`: Calls `url_for('weather_alerts')`
- **Usage Notes:**
  - `current-weather-summary` renders data from `default_location` showing temperature, condition, humidity, wind speed.


### 2. templates/current_weather.html
- **Page Title:** Current Weather
- **Context Variables:**
  - `location` (dict):  Fields - `location_id` (int), `location_name` (str)
  - `temperature` (int)
  - `condition` (str)
  - `humidity` (int)
  - `wind_speed` (int)
- **Element IDs and Types:**
  - `current-weather-page` (Div): Container for the current weather page.
  - `location-name` (H1): Displays the location's name.
  - `temperature-display` (Div): Displays the current temperature.
  - `weather-condition` (Div): Displays weather condition description.
  - `humidity-info` (Div): Displays humidity percentage.
  - `wind-speed-info` (Div): Displays wind speed.
- **Navigation Links:**
  - None specified.
- **Usage Notes:**
  - The page uses dynamic data for a selected location identified by the route parameter `location_id`.


### 3. templates/weekly_forecast.html
- **Page Title:** Weekly Forecast
- **Context Variables:**
  - `locations` (list of dict): Fields - `location_id` (int), `location_name` (str)
  - `selected_location_id` (int)
  - `forecasts` (list of dict): Fields - `forecast_id` (int), `date` (str), `high_temp` (int), `low_temp` (int), `condition` (str), `precipitation` (int), `humidity` (int)
- **Element IDs and Types:**
  - `forecast-page` (Div): Container for the forecast page.
  - `forecast-table` (Table): Displays daily forecast data in rows.
  - `location-filter` (Dropdown): Allows user to select location to filter forecasts.
  - `forecast-list` (Div): Displays forecast cards for each day (alternative to table).
  - `back-to-dashboard` (Button): Navigates back to dashboard page `dashboard`
- **Navigation Links:**
  - `back-to-dashboard`: Calls `url_for('dashboard')`
- **Usage Notes:**
  - The `location-filter` dropdown triggers filter action; POST method can be used.
  - The `forecast-table` renders rows for each forecast in `forecasts` list.


### 4. templates/location_search.html
- **Page Title:** Search Locations
- **Context Variables:**
  - `search_query` (str)
  - `search_results` (list of dict): Fields - `location_id` (int), `location_name` (str), `latitude` (float), `longitude` (float), `country` (str), `timezone` (str)
  - `saved_locations` (list of dict): Fields - `location_id` (int), `location_name` (str), `latitude` (float), `longitude` (float), `country` (str), `timezone` (str)
- **Element IDs and Types:**
  - `search-page` (Div): Container for the search page.
  - `location-search-input` (Input): Input field for user to enter search query.
  - `search-results` (Div): Displays matching locations based on search.
  - `select-location-button-{location_id}` (Button): Button to select location; dynamic ID per location.
  - `saved-locations-list` (Div): Displays previously saved locations.
- **Navigation Links:**
  - `select-location-button-{location_id}`: Trigger action to save/select location by POST, linked to backend logic.
- **Usage Notes:**
  - Iterates over `search_results` to render each location and its corresponding `select-location-button-{location_id}`.
  - Displays list of saved locations with `saved-locations-list`.


### 5. templates/weather_alerts.html
- **Page Title:** Weather Alerts
- **Context Variables:**
  - `alerts` (list of dict): Fields - `alert_id` (int), `location_id` (int), `alert_type` (str), `severity` (str), `description` (str), `start_time` (str), `end_time` (str), `is_acknowledged` (bool)
  - `severity_filter` (str)
  - `location_filter` (int or None)
  - `locations` (list of dict): Fields - `location_id` (int), `location_name` (str)
- **Element IDs and Types:**
  - `alerts-page` (Div): Container for the alerts page.
  - `alerts-list` (Div): Displays all active alerts.
  - `severity-filter` (Dropdown): Filter alerts by severity.
  - `location-filter-alerts` (Dropdown): Filter alerts by location.
  - `acknowledge-alert-button-{alert_id}` (Button): Dynamic ID for acknowledge button per alert.
- **Navigation Links:**
  - Filter dropdowns post back to `weather_alerts` route.
  - Acknowledge buttons trigger POST action to acknowledge alerts.
- **Usage Notes:**
  - Iterates through `alerts` for rendering in `alerts-list` with acknowledge button per alert.


### 6. templates/air_quality.html
- **Page Title:** Air Quality Index
- **Context Variables:**
  - `locations` (list of dict): Fields - `location_id` (int), `location_name` (str)
  - `selected_location_id` (int)
  - `aqi_info` (dict): Fields - `aqi_index` (int), `aqi_description` (str), `pm25` (float), `pm10` (float), `no2` (float), `o3` (float), `last_updated` (str)
  - `health_recommendation` (str)
- **Element IDs and Types:**
  - `air-quality-page` (Div): Container for the air quality page.
  - `aqi-display` (Div): Displays Air Quality Index value.
  - `aqi-description` (Div): Displays description of air quality.
  - `pollution-details` (Table): Shows pollutant values (PM2.5, PM10, NO2, O3).
  - `location-aqi-filter` (Dropdown): Select location to filter air quality.
  - `health-recommendation` (Div): Displays health recommendations.
- **Navigation Links:**
  - `location-aqi-filter` triggers filter POST to `air_quality` route.
- **Usage Notes:**
  - Pollution details table renders pollution components from `aqi_info`.


### 7. templates/saved_locations.html
- **Page Title:** Saved Locations
- **Context Variables:**
  - `saved_locations` (list of dict): Fields - `saved_id` (int), `user_id` (int), `location_id` (int), `location_name` (str), `is_default` (bool)
- **Element IDs and Types:**
  - `saved-locations-page` (Div): Container for the saved locations page.
  - `locations-table` (Table): Displays saved locations with current temperature and weather condition.
  - `view-location-weather-{location_id}` (Button): Dynamic ID button for viewing weather of a location.
  - `remove-location-button-{location_id}` (Button): Dynamic ID button for removing a saved location.
  - `add-new-location-button` (Button): Adds a new location by navigating to search.
- **Navigation Links:**
  - `view-location-weather-{location_id}`: Calls `url_for('current_weather', location_id=location_id)`
  - `remove-location-button-{location_id}`: Triggers POST to remove the saved location.
  - `add-new-location-button`: Calls `url_for('search_locations')`
- **Usage Notes:**
  - Iterates over `saved_locations` to populate `locations-table` and buttons with dynamic IDs.


### 8. templates/settings.html
- **Page Title:** Settings
- **Context Variables:**
  - `temperature_units` (list of str): `Celsius`, `Fahrenheit`, `Kelvin`
  - `selected_unit` (str)
  - `locations` (list of dict): Fields - `location_id` (int), `location_name` (str)
  - `selected_default_location_id` (int)
  - `alert_notifications_enabled` (bool)
- **Element IDs and Types:**
  - `settings-page` (Div): Container for settings page.
  - `temperature-unit-select` (Dropdown): Dropdown to select temperature unit.
  - `default-location-select` (Dropdown): Dropdown to select default location.
  - `alert-notifications-toggle` (Checkbox): Toggle alert notifications on/off.
  - `save-settings-button` (Button): Save changes.
  - `back-to-dashboard` (Button): Navigate back to dashboard.
- **Navigation Links:**
  - `back-to-dashboard`: Calls `url_for('dashboard')`
- **Usage Notes:**
  - Uses conditional rendering for toggles and selects based on context variables.


---

## Section 3: Data File Schemas

### 1. Current Weather Data
- **File:** `data/current_weather.txt`
- **Field Order:**
  1. `location_id` (int) - Unique identifier for the location
  2. `location_name` (str) - Name of the location
  3. `temperature` (int) - Current temperature in degrees
  4. `condition` (str) - Weather condition description
  5. `humidity` (int) - Humidity percentage
  6. `wind_speed` (int) - Wind speed in mph
  7. `last_updated` (str) - Timestamp in format `YYYY-MM-DD HH:MM`
- **Description:** Contains current weather data for multiple locations.
- **Example Lines:**
```
1|New York|72|Sunny|65|10|2025-01-20 14:30
2|London|55|Rainy|80|15|2025-01-20 14:30
3|Tokyo|45|Cloudy|72|8|2025-01-20 14:30
```


### 2. Forecasts Data
- **File:** `data/forecasts.txt`
- **Field Order:**
  1. `forecast_id` (int) - Unique forecast entry identifier
  2. `location_id` (int) - Location identifier
  3. `date` (str) - Date of forecast in `YYYY-MM-DD`
  4. `high_temp` (int) - High temperature forecast
  5. `low_temp` (int) - Low temperature forecast
  6. `condition` (str) - Forecasted weather condition
  7. `precipitation` (int) - Precipitation percentage
  8. `humidity` (int) - Humidity percentage
- **Description:** Contains 7-day weather forecasts for locations.
- **Example Lines:**
```
1|1|2025-01-21|75|60|Sunny|0|60
2|1|2025-01-22|68|55|Cloudy|10|70
3|2|2025-01-21|58|48|Rainy|80|85
```


### 3. Locations Data
- **File:** `data/locations.txt`
- **Field Order:**
  1. `location_id` (int) - Unique location identifier
  2. `location_name` (str) - Name of the location
  3. `latitude` (float) - Latitude coordinate
  4. `longitude` (float) - Longitude coordinate
  5. `country` (str) - Country name
  6. `timezone` (str) - Timezone string (e.g. EST, GMT)
- **Description:** Contains location metadata used across the app.
- **Example Lines:**
```
1|New York|40.7128|-74.0060|USA|EST
2|London|51.5074|-0.1278|UK|GMT
3|Tokyo|35.6762|139.6503|Japan|JST
```


### 4. Weather Alerts Data
- **File:** `data/alerts.txt`
- **Field Order:**
  1. `alert_id` (int) - Unique alert identifier
  2. `location_id` (int) - Location identifier
  3. `alert_type` (str) - Type of alert (e.g., Thunderstorm, Fog)
  4. `severity` (str) - Severity level (Critical, High, Medium, Low)
  5. `description` (str) - Alert description
  6. `start_time` (str) - Alert start timestamp `YYYY-MM-DD HH:MM`
  7. `end_time` (str) - Alert end timestamp `YYYY-MM-DD HH:MM`
  8. `is_acknowledged` (int) - 0 = Not acknowledged, 1 = Acknowledged
- **Description:** Stores active weather alerts and status.
- **Example Lines:**
```
1|1|Thunderstorm|High|Severe thunderstorm warning in effect until 8 PM|2025-01-20 14:00|2025-01-20 20:00|0
2|2|Fog|Medium|Dense fog advisory in effect until noon tomorrow|2025-01-20 06:00|2025-01-21 12:00|0
3|1|Wind|Medium|High wind advisory with gusts up to 45 mph|2025-01-20 15:00|2025-01-21 09:00|1
```


### 5. Air Quality Data
- **File:** `data/air_quality.txt`
- **Field Order:**
  1. `aqi_id` (int) - Unique air quality record ID
  2. `location_id` (int) - Location identifier
  3. `aqi_index` (int) - Air Quality Index (0-500)
  4. `pm25` (float) - PM2.5 pollutant value
  5. `pm10` (float) - PM10 pollutant value
  6. `no2` (float) - NO2 pollutant value
  7. `o3` (float) - O3 pollutant value
  8. `last_updated` (str) - Timestamp `YYYY-MM-DD HH:MM`
- **Description:** Stores air quality and pollution levels per location.
- **Example Lines:**
```
1|1|45|12.5|35|28|55|2025-01-20 14:30
2|2|67|22.3|48|42|78|2025-01-20 14:30
3|3|120|68.5|95|65|110|2025-01-20 14:30
```


### 6. Saved Locations Data
- **File:** `data/saved_locations.txt`
- **Field Order:**
  1. `saved_id` (int) - Unique saved location entry ID
  2. `user_id` (int) - User identifier (fixed since no authentication, default 1 assumed)
  3. `location_id` (int) - Location identifier
  4. `location_name` (str) - Name of saved location
  5. `is_default` (int) - 1 if this is default location, 0 otherwise
- **Description:** Stores locations saved by users.
- **Example Lines:**
```
1|1|1|New York|1
2|1|2|London|0
3|2|3|Tokyo|1
```

---

**End of Design Specification.**
