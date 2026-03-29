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
- **HTTP Methods:** GET
- **Function Name:** `weekly_forecast`
- **Template:** `weekly_forecast.html`
- **Context Variables:**
  - `locations` (list of dicts): each dict has fields - `location_id` (int), `location_name` (str)
  - `selected_location_id` (int)
  - `forecasts` (list of dicts): each dict has fields - `forecast_id` (int), `date` (str, format YYYY-MM-DD), `high_temp` (int), `low_temp` (int), `condition` (str), `precipitation` (int), `humidity` (int)


### 5. Location Search Page
- **URL Path:** `/locations/search`
- **HTTP Methods:** GET, POST
- **Function Name:** `location_search`
- **Template:** `location_search.html`
- **Context Variables:**
  - `search_query` (str) [optional; when POST]
  - `search_results` (list of dicts): each with fields - `location_id` (int), `location_name` (str), `latitude` (float), `longitude` (float), `country` (str), `timezone` (str)
  - `saved_locations` (list of dicts): each with fields - `location_id` (int), `location_name` (str)


### 6. Weather Alerts Page
- **URL Path:** `/alerts`
- **HTTP Methods:** GET
- **Function Name:** `alerts`
- **Template:** `alerts.html`
- **Context Variables:**
  - `alerts` (list of dicts): each dict with fields - `alert_id` (int), `location_id` (int), `alert_type` (str), `severity` (str), `description` (str), `start_time` (str), `end_time` (str), `is_acknowledged` (bool)
  - `severity_filter` (str): selected severity filter. One of `All`, `Critical`, `High`, `Medium`, `Low`
  - `location_filter` (int or None): selected location_id filter or None for all
  - `locations` (list of dicts): each dict - `location_id` (int), `location_name` (str)


### 7. Air Quality Page
- **URL Path:** `/air_quality`
- **HTTP Methods:** GET
- **Function Name:** `air_quality`
- **Template:** `air_quality.html`
- **Context Variables:**
  - `locations` (list of dicts): each dict - `location_id` (int), `location_name` (str)
  - `selected_location_id` (int)
  - `air_quality` (dict): fields - `aqi_index` (int), `pm25` (float), `pm10` (float), `no2` (float), `o3` (float), `last_updated` (str)
  - `aqi_description` (str)
  - `health_recommendation` (str)


### 8. Saved Locations Page
- **URL Path:** `/locations/saved`
- **HTTP Methods:** GET
- **Function Name:** `saved_locations`
- **Template:** `saved_locations.html`
- **Context Variables:**
  - `locations` (list of dicts): each dict with fields - `location_id` (int), `location_name` (str), `temperature` (int), `condition` (str)


### 9. Settings Page
- **URL Path:** `/settings`
- **HTTP Methods:** GET, POST
- **Function Name:** `settings`
- **Template:** `settings.html`
- **Context Variables:**
  - `temperature_units` (list of str): `['Celsius', 'Fahrenheit', 'Kelvin']`
  - `current_unit` (str)
  - `locations` (list of dicts): each dict - `location_id` (int), `location_name` (str)
  - `default_location_id` (int)
  - `alert_notifications_enabled` (bool)


---

## Section 2: Frontend HTML Templates Specification

### 1. templates/dashboard.html
- **Page Title:** Weather Dashboard
- **Element IDs:**
  - `dashboard-page` (Div): Container for dashboard page
  - `current-weather-summary` (Div): Shows current weather summary for default location
  - `search-location-button` (Button): Navigates to Location Search page `url_for('location_search')`
  - `view-forecast-button` (Button): Navigates to Weekly Forecast page `url_for('weekly_forecast')`
  - `view-alerts-button` (Button): Navigates to Weather Alerts page `url_for('alerts')`
- **Navigation Links:**
  - `search-location-button` &rarr; `location_search`
  - `view-forecast-button` &rarr; `weekly_forecast`
  - `view-alerts-button` &rarr; `alerts`
- **Context Variables:**
  - `default_location` (dict)
- **Usage Notes:**
  - Displays current weather details from `default_location` context


### 2. templates/current_weather.html
- **Page Title:** Current Weather
- **Element IDs:**
  - `current-weather-page` (Div): Container for page
  - `location-name` (H1): Displays location name from `location.location_name`
  - `temperature-display` (Div): Displays current temperature
  - `weather-condition` (Div): Displays weather condition
  - `humidity-info` (Div): Displays humidity percentage
  - `wind-speed-info` (Div): Displays wind speed
- **Navigation Links:**
  - None specified
- **Context Variables:**
  - `location` (dict)
  - `temperature` (int)
  - `condition` (str)
  - `humidity` (int)
  - `wind_speed` (int)
- **Usage Notes:**
  - Render the weather details for the selected location dynamically


### 3. templates/weekly_forecast.html
- **Page Title:** Weekly Forecast
- **Element IDs:**
  - `forecast-page` (Div): Container for weekly forecast content
  - `forecast-table` (Table): Displays forecast data with columns Date, High Temp, Low Temp, Condition
  - `location-filter` (Dropdown): Used to select/filter location, options generated from `locations`
  - `forecast-list` (Div): Displays forecast cards for each day
  - `back-to-dashboard` (Button): Navigates back to dashboard page `url_for('dashboard')`
- **Navigation Links:**
  - `back-to-dashboard` &rarr; `dashboard`
- **Context Variables:**
  - `locations` (list of dicts)
  - `selected_location_id` (int)
  - `forecasts` (list of dicts)
- **Usage Notes:**
  - Use loop to render forecast rows/cards.
  - Location filter updates displayed forecasts.


### 4. templates/location_search.html
- **Page Title:** Search Locations
- **Element IDs:**
  - `search-page` (Div): Container for search
  - `location-search-input` (Input): Input field for search query
  - `search-results` (Div): Displays list of search results
  - Patterned IDs for each search result button: `select-location-button-{location_id}` (Button)
  - `saved-locations-list` (Div): Displays saved locations
- **Navigation Links:**
  - None specified
- **Context Variables:**
  - `search_query` (str) [optional]
  - `search_results` (list of dicts)
  - `saved_locations` (list of dicts)
- **Usage Notes:**
  - Render search results dynamically.
  - For each result, a button with corresponding patterned ID.
  - List saved locations separately.


### 5. templates/alerts.html
- **Page Title:** Weather Alerts
- **Element IDs:**
  - `alerts-page` (Div): Container for alerts
  - `alerts-list` (Div): Displays all active alerts
  - `severity-filter` (Dropdown): For filtering by severity
  - `location-filter-alerts` (Dropdown): For filtering by location
  - Patterned IDs for each alert button: `acknowledge-alert-button-{alert_id}` (Button)
- **Navigation Links:**
  - None specified
- **Context Variables:**
  - `alerts` (list of dicts)
  - `severity_filter` (str)
  - `location_filter` (int or None)
  - `locations` (list of dicts)
- **Usage Notes:**
  - Loop through alerts to display.
  - Each alert includes acknowledge button.
  - Filters affect displayed alerts.


### 6. templates/air_quality.html
- **Page Title:** Air Quality Index
- **Element IDs:**
  - `air-quality-page` (Div): Container
  - `aqi-display` (Div): Displays AQI value
  - `aqi-description` (Div): Displays descriptive text for AQI
  - `pollution-details` (Table): Shows pollutants PM2.5, PM10, NO2, O3
  - `location-aqi-filter` (Dropdown): Location filter
  - `health-recommendation` (Div): Shows health advice
- **Navigation Links:**
  - None specified
- **Context Variables:**
  - `locations` (list of dicts)
  - `selected_location_id` (int)
  - `air_quality` (dict)
  - `aqi_description` (str)
  - `health_recommendation` (str)
- **Usage Notes:**
  - Render pollutant values in table.
  - Display AQI description and health recommendation based on selected location.


### 7. templates/saved_locations.html
- **Page Title:** Saved Locations
- **Element IDs:**
  - `saved-locations-page` (Div): Container
  - `locations-table` (Table): Displays saved locations with current temperature and condition
  - For each location, patterned buttons:
    - `view-location-weather-{location_id}` (Button): View weather page for location
    - `remove-location-button-{location_id}` (Button): Remove location from saved
  - `add-new-location-button` (Button): Button to add new saved location
- **Navigation Links:**
  - None specified
- **Context Variables:**
  - `locations` (list of dicts)
- **Usage Notes:**
  - Loop through saved locations.
  - Provide buttons with patterned IDs for each location.


### 8. templates/settings.html
- **Page Title:** Settings
- **Element IDs:**
  - `settings-page` (Div): Container
  - `temperature-unit-select` (Dropdown): Select temp unit
  - `default-location-select` (Dropdown): Select default location
  - `alert-notifications-toggle` (Checkbox): Toggle alert notifications
  - `save-settings-button` (Button): Save settings
  - `back-to-dashboard` (Button): Navigate back to dashboard `url_for('dashboard')`
- **Navigation Links:**
  - `back-to-dashboard` &rarr; `dashboard`
- **Context Variables:**
  - `temperature_units` (list of str)
  - `current_unit` (str)
  - `locations` (list of dicts)
  - `default_location_id` (int)
  - `alert_notifications_enabled` (bool)
- **Usage Notes:**
  - Render dropdowns with appropriate selected values.
  - Toggle checkbox checked state.


---

## Section 3: Data File Schemas

### 1. Current Weather Data
- **File:** `data/current_weather.txt`
- **Field Order:**
  `location_id|location_name|temperature|condition|humidity|wind_speed|last_updated`
- **Field Descriptions:**
  - `location_id` (int): Unique ID for location
  - `location_name` (str): Name of the location
  - `temperature` (int): Current temperature
  - `condition` (str): Weather condition description (Sunny, Rainy, etc.)
  - `humidity` (int): Humidity percentage
  - `wind_speed` (int): Wind speed in mph
  - `last_updated` (str): Timestamp in `YYYY-MM-DD HH:MM` format
- **Example Lines:**
  ```
  1|New York|72|Sunny|65|10|2025-01-20 14:30
  2|London|55|Rainy|80|15|2025-01-20 14:30
  3|Tokyo|45|Cloudy|72|8|2025-01-20 14:30
  ```


### 2. Forecasts Data
- **File:** `data/forecasts.txt`
- **Field Order:**
  `forecast_id|location_id|date|high_temp|low_temp|condition|precipitation|humidity`
- **Field Descriptions:**
  - `forecast_id` (int): Unique forecast entry ID
  - `location_id` (int): ID of the location
  - `date` (str): Date of forecast in `YYYY-MM-DD`
  - `high_temp` (int): High temperature forecast
  - `low_temp` (int): Low temperature forecast
  - `condition` (str): Weather condition (Sunny, Rainy, etc.)
  - `precipitation` (int): Precipitation chance percentage
  - `humidity` (int): Forecast humidity percentage
- **Example Lines:**
  ```
  1|1|2025-01-21|75|60|Sunny|0|60
  2|1|2025-01-22|68|55|Cloudy|10|70
  3|2|2025-01-21|58|48|Rainy|80|85
  ```


### 3. Locations Data
- **File:** `data/locations.txt`
- **Field Order:**
  `location_id|location_name|latitude|longitude|country|timezone`
- **Field Descriptions:**
  - `location_id` (int): Unique location ID
  - `location_name` (str): Location name
  - `latitude` (float): Latitude coordinate
  - `longitude` (float): Longitude coordinate
  - `country` (str): Country name
  - `timezone` (str): Time zone abbreviation
- **Example Lines:**
  ```
  1|New York|40.7128|-74.0060|USA|EST
  2|London|51.5074|-0.1278|UK|GMT
  3|Tokyo|35.6762|139.6503|Japan|JST
  ```


### 4. Weather Alerts Data
- **File:** `data/alerts.txt`
- **Field Order:**
  `alert_id|location_id|alert_type|severity|description|start_time|end_time|is_acknowledged`
- **Field Descriptions:**
  - `alert_id` (int): Unique alert ID
  - `location_id` (int): Location ID affected
  - `alert_type` (str): Type of alert (Thunderstorm, Fog, etc.)
  - `severity` (str): Severity level (Critical, High, Medium, Low)
  - `description` (str): Alert descriptive text
  - `start_time` (str): Alert start datetime `YYYY-MM-DD HH:MM`
  - `end_time` (str): Alert end datetime `YYYY-MM-DD HH:MM`
  - `is_acknowledged` (int): 0 = not acknowledged, 1 = acknowledged
- **Example Lines:**
  ```
  1|1|Thunderstorm|High|Severe thunderstorm warning in effect until 8 PM|2025-01-20 14:00|2025-01-20 20:00|0
  2|2|Fog|Medium|Dense fog advisory in effect until noon tomorrow|2025-01-20 06:00|2025-01-21 12:00|0
  3|1|Wind|Medium|High wind advisory with gusts up to 45 mph|2025-01-20 15:00|2025-01-21 09:00|1
  ```


### 5. Air Quality Data
- **File:** `data/air_quality.txt`
- **Field Order:**
  `aqi_id|location_id|aqi_index|pm25|pm10|no2|o3|last_updated`
- **Field Descriptions:**
  - `aqi_id` (int): Unique air quality record ID
  - `location_id` (int): Location ID
  - `aqi_index` (int): Air Quality Index (0-500)
  - `pm25` (float): PM2.5 concentration
  - `pm10` (float): PM10 concentration
  - `no2` (float): NO2 concentration
  - `o3` (float): Ozone concentration
  - `last_updated` (str): Timestamp `YYYY-MM-DD HH:MM`
- **Example Lines:**
  ```
  1|1|45|12.5|35|28|55|2025-01-20 14:30
  2|2|67|22.3|48|42|78|2025-01-20 14:30
  3|3|120|68.5|95|65|110|2025-01-20 14:30
  ```


### 6. Saved Locations Data
- **File:** `data/saved_locations.txt`
- **Field Order:**
  `saved_id|user_id|location_id|location_name|is_default`
- **Field Descriptions:**
  - `saved_id` (int): Unique saved location entry ID
  - `user_id` (int): User ID (though no auth, fixed user could be assumed)
  - `location_id` (int): Location ID saved
  - `location_name` (str): Name of saved location
  - `is_default` (int): 1 = default location, 0 = not default
- **Example Lines:**
  ```
  1|1|1|New York|1
  2|1|2|London|0
  3|2|3|Tokyo|1
  ```