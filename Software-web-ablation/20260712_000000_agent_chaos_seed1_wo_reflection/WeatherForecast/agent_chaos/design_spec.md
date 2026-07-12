# WeatherForecast Application Design Specification

---

## Section 1: Flask Routes Specification

### 1. Root Route
- **URL Path:** /
- **Methods:** GET
- **Function Name:** root_redirect
- **Template Rendered:** Redirects to dashboard page (`/dashboard`)
- **Context Variables:** None

### 2. Dashboard Page
- **URL Path:** /dashboard
- **Methods:** GET
- **Function Name:** dashboard_page
- **Template Rendered:** dashboard.html
- **Context Variables:**
  - `default_location` (dict): Fields - location_id (int), location_name (str)
  - `current_weather` (dict): Fields - temperature (float), condition (str), humidity (int), wind_speed (float), last_updated (str)

### 3. Current Weather Page
- **URL Path:** /weather/current/<int:location_id>
- **Methods:** GET
- **Function Name:** current_weather_page
- **Template Rendered:** current_weather.html
- **Context Variables:**
  - `location` (dict): Fields - location_id (int), location_name (str)
  - `current_weather` (dict): Fields - temperature (float), condition (str), humidity (int), wind_speed (float), last_updated (str)

### 4. Weekly Forecast Page
- **URL Path:** /forecast/weekly
- **Methods:** GET
- **Function Name:** weekly_forecast_page
- **Template Rendered:** weekly_forecast.html
- **Context Variables:**
  - `locations` (list of dict): Each dict fields - location_id (int), location_name (str)
  - `selected_location` (dict): Fields - location_id (int), location_name (str)
  - `forecasts` (list of dict): Each dict fields - date (str), high_temp (float), low_temp (float), condition (str), precipitation (int), humidity (int)

### 5. Location Search Page
- **URL Path:** /locations/search
- **Methods:** GET, POST
- **Function Name:** location_search_page
- **Template Rendered:** location_search.html
- **Context Variables:**
  - `search_query` (str): Current search term from input (optional)
  - `search_results` (list of dict): Each dict fields - location_id (int), location_name (str), latitude (float), longitude (float), country (str), timezone (str)
  - `saved_locations` (list of dict): Each dict fields - location_id (int), location_name (str)

### 6. Weather Alerts Page
- **URL Path:** /alerts
- **Methods:** GET, POST
- **Function Name:** weather_alerts_page
- **Template Rendered:** alerts.html
- **Context Variables:**
  - `alerts` (list of dict): Each dict fields - alert_id (int), location_id (int), alert_type (str), severity (str), description (str), start_time (str), end_time (str), is_acknowledged (bool)
  - `severity_filter` (str): Current severity filter selection
  - `location_filter` (int or None): Currently selected location_id for filtering or None for all
  - `locations` (list of dict): Each dict fields - location_id (int), location_name (str)

### 7. Air Quality Page
- **URL Path:** /air-quality
- **Methods:** GET
- **Function Name:** air_quality_page
- **Template Rendered:** air_quality.html
- **Context Variables:**
  - `locations` (list of dict): Each dict fields - location_id (int), location_name (str)
  - `selected_location` (dict): Fields - location_id (int), location_name (str)
  - `air_quality` (dict): Fields - aqi_index (int), pm25 (float), pm10 (float), no2 (float), o3 (float), last_updated (str)
  - `aqi_description` (str): Descriptive text for the AQI category
  - `health_recommendation` (str): Health recommendations based on AQI

### 8. Saved Locations Page
- **URL Path:** /locations/saved
- **Methods:** GET, POST
- **Function Name:** saved_locations_page
- **Template Rendered:** saved_locations.html
- **Context Variables:**
  - `saved_locations` (list of dict): Each dict fields - saved_id (int), location_id (int), location_name (str), is_default (bool), current_temp (float), current_condition (str)

### 9. Settings Page
- **URL Path:** /settings
- **Methods:** GET, POST
- **Function Name:** settings_page
- **Template Rendered:** settings.html
- **Context Variables:**
  - `temperature_units` (list of str): ['Celsius', 'Fahrenheit', 'Kelvin']
  - `selected_unit` (str): Current temperature unit selected
  - `locations` (list of dict): Each dict fields - location_id (int), location_name (str)
  - `default_location_id` (int): Location ID currently set as default
  - `alert_notifications_enabled` (bool): Alert notification toggle state

---

## Section 2: Frontend HTML Templates Specification

### 1. templates/dashboard.html
- **Page Title:** Weather Dashboard
- **Elements:**
  - `dashboard-page` (Div) - Main container for dashboard
  - `current-weather-summary` (Div) - Shows summary of current weather for default location
  - `search-location-button` (Button) - Navigates to location search page
  - `view-forecast-button` (Button) - Navigates to weekly forecast page
  - `view-alerts-button` (Button) - Navigates to weather alerts page
- **Navigation Mapping:**
  - `search-location-button` → url_for('location_search_page')
  - `view-forecast-button` → url_for('weekly_forecast_page')
  - `view-alerts-button` → url_for('weather_alerts_page')
- **Context Variables:**
  - `default_location` (dict) with keys: location_id (int), location_name (str)
  - `current_weather` (dict) with keys: temperature (float), condition (str), humidity (int), wind_speed (float), last_updated (str)
- **Dynamic Data Rendering:** Display current_weather fields inside `current-weather-summary`.

### 2. templates/current_weather.html
- **Page Title:** Current Weather
- **Elements:**
  - `current-weather-page` (Div) - Main container
  - `location-name` (H1) - Name of the current location
  - `temperature-display` (Div) - Current temperature value
  - `weather-condition` (Div) - Weather condition description
  - `humidity-info` (Div) - Humidity percentage
  - `wind-speed-info` (Div) - Wind speed information
- **Navigation Mapping:** Not specified (no navigation buttons)
- **Context Variables:**
  - `location` (dict) with keys: location_id (int), location_name (str)
  - `current_weather` (dict) with keys: temperature (float), condition (str), humidity (int), wind_speed (float), last_updated (str)
- **Dynamic Data Rendering:** Render weather data fields inside respective divs

### 3. templates/weekly_forecast.html
- **Page Title:** Weekly Forecast
- **Elements:**
  - `forecast-page` (Div) - Main container
  - `forecast-table` (Table) - Detailed table with date, high temp, low temp, condition
  - `location-filter` (Dropdown) - Select location to filter forecast
  - `forecast-list` (Div) - Grid of daily forecast cards
  - `back-to-dashboard` (Button) - Navigate back to dashboard
- **Navigation Mapping:**
  - `back-to-dashboard` → url_for('dashboard_page')
- **Context Variables:**
  - `locations` (list of dict): location_id (int), location_name (str)
  - `selected_location` (dict): location_id (int), location_name (str)
  - `forecasts` (list of dict): date (str), high_temp (float), low_temp (float), condition (str), precipitation (int), humidity (int)
- **Dynamic Data Rendering:**
  - Loop through `forecasts` to populate table rows and forecast cards
  - Conditional display for no forecasts message if empty list

### 4. templates/location_search.html
- **Page Title:** Search Locations
- **Elements:**
  - `search-page` (Div) - Main container
  - `location-search-input` (Input) - Text input for search query
  - `search-results` (Div) - Container listing search results
  - `select-location-button-{location_id}` (Button) - Button for each search result to select location
  - `saved-locations-list` (Div) - Display saved locations
- **Navigation Mapping:**
  - `select-location-button-{location_id}` → url_for('current_weather_page', location_id=location_id) for each location_id dynamically
- **Context Variables:**
  - `search_query` (str)
  - `search_results` (list of dict) with fields: location_id (int), location_name (str), latitude (float), longitude (float), country (str), timezone (str)
  - `saved_locations` (list of dict) with fields: location_id (int), location_name (str)
- **Dynamic Data Rendering:**
  - Loop through `search_results` to render search results each with unique button id `select-location-button-{location_id}`
  - Loop through `saved_locations` to render saved locations list

### 5. templates/alerts.html
- **Page Title:** Weather Alerts
- **Elements:**
  - `alerts-page` (Div) - Main container
  - `alerts-list` (Div) - Lists active alerts
  - `severity-filter` (Dropdown) - For selecting alert severity filter
  - `location-filter-alerts` (Dropdown) - Filter alerts by location
  - `acknowledge-alert-button-{alert_id}` (Button) - Button for each alert to acknowledge
- **Navigation Mapping:**
  - `acknowledge-alert-button-{alert_id}` → (POST action to acknowledge alert with alert_id)
- **Context Variables:**
  - `alerts` (list of dict): alert_id (int), location_id (int), alert_type (str), severity (str), description (str), start_time (str), end_time (str), is_acknowledged (bool)
  - `severity_filter` (str)
  - `location_filter` (int or None)
  - `locations` (list of dict): location_id (int), location_name (str)
- **Dynamic Data Rendering:**
  - Loop through `alerts` to render each alert with unique `acknowledge-alert-button-{alert_id}`
  - Conditional display of alerts based on filters

### 6. templates/air_quality.html
- **Page Title:** Air Quality Index
- **Elements:**
  - `air-quality-page` (Div) - Main container
  - `aqi-display` (Div) - AQI numeric value
  - `aqi-description` (Div) - Descriptive text for AQI
  - `pollution-details` (Table) - Table showing PM2.5, PM10, NO2, O3 concentrations
  - `location-aqi-filter` (Dropdown) - Filter air quality info by location
  - `health-recommendation` (Div) - Health advice based on AQI
- **Navigation Mapping:** N/A
- **Context Variables:**
  - `locations` (list of dict): location_id (int), location_name (str)
  - `selected_location` (dict): location_id (int), location_name (str)
  - `air_quality` (dict): aqi_index (int), pm25 (float), pm10 (float), no2 (float), o3 (float), last_updated (str)
  - `aqi_description` (str)
  - `health_recommendation` (str)
- **Dynamic Data Rendering:**
  - Render AQI values and pollution data inside respective elements

### 7. templates/saved_locations.html
- **Page Title:** Saved Locations
- **Elements:**
  - `saved-locations-page` (Div) - Main container
  - `locations-table` (Table) - Displays saved locations with current temp and condition
  - `view-location-weather-{location_id}` (Button) - For each saved location to view weather
  - `remove-location-button-{location_id}` (Button) - For each saved location to remove it
  - `add-new-location-button` (Button) - Button to add new location
- **Navigation Mapping:**
  - `view-location-weather-{location_id}` → url_for('current_weather_page', location_id=location_id)
  - `remove-location-button-{location_id}` → (POST action to remove saved location with location_id)
  - `add-new-location-button` → url_for('location_search_page')
- **Context Variables:**
  - `saved_locations` (list of dict): saved_id (int), location_id (int), location_name (str), is_default (bool), current_temp (float), current_condition (str)
- **Dynamic Data Rendering:** Loop through saved_locations rendering rows with buttons having dynamic IDs

### 8. templates/settings.html
- **Page Title:** Settings
- **Elements:**
  - `settings-page` (Div) - Main container
  - `temperature-unit-select` (Dropdown) - Temperature unit selection
  - `default-location-select` (Dropdown) - Default location selection
  - `alert-notifications-toggle` (Checkbox) - Toggle for alert notifications
  - `save-settings-button` (Button) - Button to save settings
  - `back-to-dashboard` (Button) - Navigate back to dashboard
- **Navigation Mapping:**
  - `back-to-dashboard` → url_for('dashboard_page')
- **Context Variables:**
  - `temperature_units` (list of str): e.g., ['Celsius', 'Fahrenheit', 'Kelvin']
  - `selected_unit` (str)
  - `locations` (list of dict): location_id (int), location_name (str)
  - `default_location_id` (int)
  - `alert_notifications_enabled` (bool)
- **Dynamic Data Rendering:** Render dropdown options for temperature units and locations

---

## Section 3: Data File Schemas

### 1. data/current_weather.txt
- **File Path:** data/current_weather.txt
- **Field Order:** location_id|location_name|temperature|condition|humidity|wind_speed|last_updated
- **Fields:**
  - `location_id` (int): Unique identifier for the location
  - `location_name` (str): Name of the location
  - `temperature` (float): Current temperature in degrees (unit per settings)
  - `condition` (str): Weather condition description (e.g., Sunny, Rainy)
  - `humidity` (int): Humidity percentage
  - `wind_speed` (float): Wind speed in mph or km/h
  - `last_updated` (str): Timestamp of last update in 'YYYY-MM-DD HH:MM' format
- **Description:** Contains current weather data for each monitored location.
- **Example Lines:**
  ```
  1|New York|72|Sunny|65|10|2025-01-20 14:30
  2|London|55|Rainy|80|15|2025-01-20 14:30
  3|Tokyo|45|Cloudy|72|8|2025-01-20 14:30
  ```

### 2. data/forecasts.txt
- **File Path:** data/forecasts.txt
- **Field Order:** forecast_id|location_id|date|high_temp|low_temp|condition|precipitation|humidity
- **Fields:**
  - `forecast_id` (int): Unique identifier for the forecast entry
  - `location_id` (int): Location identifier the forecast applies to
  - `date` (str): Date of forecast in 'YYYY-MM-DD' format
  - `high_temp` (float): Forecasted high temperature
  - `low_temp` (float): Forecasted low temperature
  - `condition` (str): Forecasted weather condition
  - `precipitation` (int): Precipitation percentage chance
  - `humidity` (int): Forecasted humidity percentage
- **Description:** Holds 7-day weather forecasts for locations.
- **Example Lines:**
  ```
  1|1|2025-01-21|75|60|Sunny|0|60
  2|1|2025-01-22|68|55|Cloudy|10|70
  3|2|2025-01-21|58|48|Rainy|80|85
  ```

### 3. data/locations.txt
- **File Path:** data/locations.txt
- **Field Order:** location_id|location_name|latitude|longitude|country|timezone
- **Fields:**
  - `location_id` (int): Unique identifier for location
  - `location_name` (str): Name of the city or region
  - `latitude` (float): Latitude coordinate
  - `longitude` (float): Longitude coordinate
  - `country` (str): Country name
  - `timezone` (str): Timezone abbreviation (e.g., EST, GMT)
- **Description:** Contains all available locations monitored by the system.
- **Example Lines:**
  ```
  1|New York|40.7128|-74.0060|USA|EST
  2|London|51.5074|-0.1278|UK|GMT
  3|Tokyo|35.6762|139.6503|Japan|JST
  ```

### 4. data/alerts.txt
- **File Path:** data/alerts.txt
- **Field Order:** alert_id|location_id|alert_type|severity|description|start_time|end_time|is_acknowledged
- **Fields:**
  - `alert_id` (int): Unique alert identifier
  - `location_id` (int): Location identifier
  - `alert_type` (str): Type of alert (e.g., Thunderstorm, Fog)
  - `severity` (str): Severity level (Critical, High, Medium, Low)
  - `description` (str): Text description of alert
  - `start_time` (str): Alert start datetime in 'YYYY-MM-DD HH:MM' format
  - `end_time` (str): Alert end datetime
  - `is_acknowledged` (bool): Whether alert has been acknowledged
- **Description:** Active weather alerts data for locations.
- **Example Lines:**
  ```
  1|1|Thunderstorm|High|Severe thunderstorm warning in effect until 8 PM|2025-01-20 14:00|2025-01-20 20:00|0
  2|2|Fog|Medium|Dense fog advisory in effect until noon tomorrow|2025-01-20 06:00|2025-01-21 12:00|0
  3|1|Wind|Medium|High wind advisory with gusts up to 45 mph|2025-01-20 15:00|2025-01-21 09:00|1
  ```

### 5. data/air_quality.txt
- **File Path:** data/air_quality.txt
- **Field Order:** aqi_id|location_id|aqi_index|pm25|pm10|no2|o3|last_updated
- **Fields:**
  - `aqi_id` (int): Unique identifier for AQI record
  - `location_id` (int): Location identifier
  - `aqi_index` (int): Air Quality Index value (0-500)
  - `pm25` (float): PM2.5 concentration
  - `pm10` (float): PM10 concentration
  - `no2` (float): NO2 concentration
  - `o3` (float): Ozone concentration
  - `last_updated` (str): Timestamp of last update
- **Description:** Air quality and pollution data for locations.
- **Example Lines:**
  ```
  1|1|45|12.5|35|28|55|2025-01-20 14:30
  2|2|67|22.3|48|42|78|2025-01-20 14:30
  3|3|120|68.5|95|65|110|2025-01-20 14:30
  ```

### 6. data/saved_locations.txt
- **File Path:** data/saved_locations.txt
- **Field Order:** saved_id|user_id|location_id|location_name|is_default
- **Fields:**
  - `saved_id` (int): Unique saved location record identifier
  - `user_id` (int): User identifier (note: app has no auth, but field present)
  - `location_id` (int): Location identifier
  - `location_name` (str): Location name
  - `is_default` (bool): Whether set as default location
- **Description:** Stores users' saved locations and default location flag.
- **Example Lines:**
  ```
  1|1|1|New York|1
  2|1|2|London|0
  3|2|3|Tokyo|1
  ```
