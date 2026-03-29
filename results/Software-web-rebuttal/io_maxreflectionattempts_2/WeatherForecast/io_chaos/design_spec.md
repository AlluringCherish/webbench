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
  - `default_location` (dict):
    - Fields:
      - `location_id` (int)
      - `location_name` (str)
      - `temperature` (float or int)
      - `condition` (str)
- **Description:** Displays current weather summary for default location


### 3. Current Weather Page
- **URL Path:** `/weather/current/<int:location_id>`
- **HTTP Methods:** GET
- **Function Name:** `current_weather`
- **Template:** `current_weather.html`
- **Context Variables:**
  - `location` (dict):
    - `location_id` (int)
    - `location_name` (str)
  - `weather` (dict):
    - `temperature` (float or int)
    - `condition` (str)
    - `humidity` (int)
    - `wind_speed` (float or int)


### 4. Weekly Forecast Page
- **URL Path:** `/forecast`
- **HTTP Methods:** GET
- **Function Name:** `weekly_forecast`
- **Template:** `forecast.html`
- **Context Variables:**
  - `locations` (list of dicts): Each dict has:
    - `location_id` (int)
    - `location_name` (str)
  - `selected_location_id` (int or None)
  - `forecast_list` (list of dicts): Each dict has:
    - `date` (str, e.g., "2025-01-21")
    - `high_temp` (int or float)
    - `low_temp` (int or float)
    - `condition` (str)
- **Notes:** The `location-filter` dropdown populated with `locations`. Selecting location filters forecast.


### 5. Location Search Page
- **URL Path:** `/locations/search`
- **HTTP Methods:** GET, POST
- **Function Name:** `location_search`
- **Template:** `search.html`
- **Context Variables:**
  - `search_query` (str) - present if POST
  - `search_results` (list of dicts): each dict:
    - `location_id` (int)
    - `location_name` (str)
  - `saved_locations` (list of dicts):
    - `location_id` (int)
    - `location_name` (str)
- **Notes:** POST submits query, GET loads page or returns search results


### 6. Weather Alerts Page
- **URL Path:** `/alerts`
- **HTTP Methods:** GET
- **Function Name:** `alerts`
- **Template:** `alerts.html`
- **Context Variables:**
  - `alerts_list` (list of dicts): Each dict has:
    - `alert_id` (int)
    - `location_id` (int)
    - `alert_type` (str)
    - `severity` (str) - one of "Critical", "High", "Medium", "Low"
    - `description` (str)
    - `start_time` (str, datetime format)
    - `end_time` (str, datetime format)
    - `is_acknowledged` (bool)
  - `severity_filter` (str) - selected severity filter value
  - `location_filter` (int or None) - selected location id filter
  - `locations` (list of dicts):
    - `location_id` (int)
    - `location_name` (str)


### 7. Air Quality Page
- **URL Path:** `/air_quality`
- **HTTP Methods:** GET
- **Function Name:** `air_quality`
- **Template:** `air_quality.html`
- **Context Variables:**
  - `locations` (list of dicts):
    - `location_id` (int)
    - `location_name` (str)
  - `selected_location_id` (int or None)
  - `aqi_data` (dict):
    - `aqi_index` (int)
    - `aqi_description` (str)
    - `pm25` (float)
    - `pm10` (float)
    - `no2` (float)
    - `o3` (float)
    - `health_recommendation` (str)


### 8. Saved Locations Page
- **URL Path:** `/locations/saved`
- **HTTP Methods:** GET
- **Function Name:** `saved_locations`
- **Template:** `saved_locations.html`
- **Context Variables:**
  - `saved_locations` (list of dicts): Each dict:
    - `location_id` (int)
    - `location_name` (str)
    - `temperature` (float or int)
    - `condition` (str)


### 9. Settings Page
- **URL Path:** `/settings`
- **HTTP Methods:** GET, POST
- **Function Name:** `settings`
- **Template:** `settings.html`
- **Context Variables:**
  - `temperature_units` (list of str): [`Celsius`, `Fahrenheit`, `Kelvin`]
  - `current_unit` (str)
  - `default_locations` (list of dicts):
    - `location_id` (int)
    - `location_name` (str)
  - `current_default_location_id` (int or None)
  - `alert_notifications_enabled` (bool)


---

## Section 2: Frontend HTML Templates Specification

### 1. templates/dashboard.html
- **Page Title:** Weather Dashboard
- **Main Heading (<h1>):** Weather Dashboard
- **Element IDs:**
  - `dashboard-page` (Div): Container for dashboard page
  - `current-weather-summary` (Div): Show current weather for default location
  - `search-location-button` (Button): Navigate to location search page
  - `view-forecast-button` (Button): Navigate to weekly forecast page
  - `view-alerts-button` (Button): Navigate to weather alerts page
- **Navigation Mappings:**
  - `search-location-button` --> `url_for('location_search')`
  - `view-forecast-button` --> `url_for('weekly_forecast')`
  - `view-alerts-button` --> `url_for('alerts')`
- **Context Variables:**
  - `default_location` (dict): `location_id` (int), `location_name` (str), `temperature` (float), `condition` (str)
- **Usage Notes:**
  - Display basic weather data in `current-weather-summary`


### 2. templates/current_weather.html
- **Page Title:** Current Weather
- **Main Heading (<h1>):** Using `location_name` variable
- **Element IDs:**
  - `current-weather-page` (Div): Container for the page
  - `location-name` (H1): Location name
  - `temperature-display` (Div): Current temperature
  - `weather-condition` (Div): Weather condition description
  - `humidity-info` (Div): Humidity percentage
  - `wind-speed-info` (Div): Wind speed
- **Navigation Mappings:** None specified
- **Context Variables:**
  - `location` (dict): `location_id`, `location_name`
  - `weather` (dict): `temperature`, `condition`, `humidity`, `wind_speed`
- **Usage Notes:**
  - Render weather stats exactly in respective elements


### 3. templates/forecast.html
- **Page Title:** Weekly Forecast
- **Main Heading (<h1>):** Weekly Forecast
- **Element IDs:**
  - `forecast-page` (Div): Container
  - `forecast-table` (Table): Forecast data
  - `location-filter` (Dropdown): Locations for filtering forecast
  - `forecast-list` (Div): Grid of daily forecast cards
  - `back-to-dashboard` (Button): Navigate back to dashboard
- **Navigation Mappings:**
  - `back-to-dashboard` --> `url_for('dashboard')`
- **Context Variables:**
  - `locations` (list of dicts): `location_id`, `location_name`
  - `selected_location_id` (int)
  - `forecast_list` (list of dicts): `date`, `high_temp`, `low_temp`, `condition`
- **Usage Notes:**
  - Dropdown populates from `locations`
  - Display forecast data per day in table and cards


### 4. templates/search.html
- **Page Title:** Search Locations
- **Main Heading (<h1>):** Search Locations
- **Element IDs:**
  - `search-page` (Div): Container
  - `location-search-input` (Input): For entering search query
  - `search-results` (Div): List matching locations
  - `select-location-button-{location_id}` (Button): Button to select a location - dynamic ID with placeholder `{location_id}`
  - `saved-locations-list` (Div): Previously saved locations display
- **Navigation Mappings:** None specified
- **Context Variables:**
  - `search_query` (str, optional)
  - `search_results` (list of dicts): `location_id`, `location_name`
  - `saved_locations` (list of dicts): `location_id`, `location_name`
- **Usage Notes:**
  - Loop through search_results to generate buttons with dynamic IDs `select-location-button-{location_id}`
  - Display saved locations in `saved-locations-list`


### 5. templates/alerts.html
- **Page Title:** Weather Alerts
- **Main Heading (<h1>):** Weather Alerts
- **Element IDs:**
  - `alerts-page` (Div): Container
  - `alerts-list` (Div): List of active alerts
  - `severity-filter` (Dropdown): Filter alerts by severity
  - `location-filter-alerts` (Dropdown): Filter alerts by location
  - `acknowledge-alert-button-{alert_id}` (Button): Button to acknowledge alert - dynamic ID with `{alert_id}`
- **Navigation Mappings:** None specified
- **Context Variables:**
  - `alerts_list` (list of dicts): `alert_id`, `location_id`, `alert_type`, `severity`, `description`, `start_time`, `end_time`, `is_acknowledged`
  - `severity_filter` (str)
  - `location_filter` (int or None)
  - `locations` (list of dicts): `location_id`, `location_name`
- **Usage Notes:**
  - Render each alert with acknowledge button using dynamic ID
  - Filters control displayed alerts


### 6. templates/air_quality.html
- **Page Title:** Air Quality Index
- **Main Heading (<h1>):** Air Quality Index
- **Element IDs:**
  - `air-quality-page` (Div): Container
  - `aqi-display` (Div): AQI numeric value
  - `aqi-description` (Div): AQI description
  - `pollution-details` (Table): Pollutant levels
  - `location-aqi-filter` (Dropdown): Filter locations
  - `health-recommendation` (Div): Health recommendations
- **Navigation Mappings:** None specified
- **Context Variables:**
  - `locations` (list of dicts): `location_id`, `location_name`
  - `selected_location_id` (int or None)
  - `aqi_data` (dict): `aqi_index` (int), `aqi_description` (str), `pm25` (float), `pm10` (float), `no2` (float), `o3` (float), `health_recommendation` (str)
- **Usage Notes:**
  - Display AQI and pollutant data
  - Dropdown filters data by location


### 7. templates/saved_locations.html
- **Page Title:** Saved Locations
- **Main Heading (<h1>):** Saved Locations
- **Element IDs:**
  - `saved-locations-page` (Div): Container
  - `locations-table` (Table): Saved locations with current weather
  - `view-location-weather-{location_id}` (Button): Button to view location weather - dynamic ID `{location_id}`
  - `remove-location-button-{location_id}` (Button): Button to remove location - dynamic ID `{location_id}`
  - `add-new-location-button` (Button): Button to add new location
- **Navigation Mappings:**
  - `add-new-location-button` --> `url_for('location_search')`
- **Context Variables:**
  - `saved_locations` (list of dicts): `location_id`, `location_name`, `temperature`, `condition`
- **Usage Notes:**
  - Render tables rows with buttons having dynamic IDs


### 8. templates/settings.html
- **Page Title:** Settings
- **Main Heading (<h1>):** Settings
- **Element IDs:**
  - `settings-page` (Div): Container
  - `temperature-unit-select` (Dropdown): Temperature unit
  - `default-location-select` (Dropdown): Default location
  - `alert-notifications-toggle` (Checkbox): Alert notifications toggle
  - `save-settings-button` (Button): Save preferences
  - `back-to-dashboard` (Button): Back to dashboard
- **Navigation Mappings:**
  - `back-to-dashboard` --> `url_for('dashboard')`
- **Context Variables:**
  - `temperature_units` (list of str): e.g., [`Celsius`, `Fahrenheit`, `Kelvin`]
  - `current_unit` (str)
  - `default_locations` (list of dicts): `location_id`, `location_name`
  - `current_default_location_id` (int or None)
  - `alert_notifications_enabled` (bool)
- **Usage Notes:**
  - Render dropdowns with selections honor current settings

---

## Section 3: Data File Schemas

### 1. Current Weather Data
- **File Path:** `data/current_weather.txt`
- **Field Order & Syntax:**
  `location_id|location_name|temperature|condition|humidity|wind_speed|last_updated`
- **Field Descriptions:**
  - `location_id` (int): Unique identifier for location
  - `location_name` (str): Name of the location
  - `temperature` (float/int): Current temperature value
  - `condition` (str): Weather condition description
  - `humidity` (int): Humidity percentage
  - `wind_speed` (float): Wind speed
  - `last_updated` (str): Timestamp of last update in `YYYY-MM-DD HH:MM` format
- **Example Lines:**
  ```
  1|New York|72|Sunny|65|10|2025-01-20 14:30
  2|London|55|Rainy|80|15|2025-01-20 14:30
  3|Tokyo|45|Cloudy|72|8|2025-01-20 14:30
  ```


### 2. Forecasts Data
- **File Path:** `data/forecasts.txt`
- **Field Order & Syntax:**
  `forecast_id|location_id|date|high_temp|low_temp|condition|precipitation|humidity`
- **Field Descriptions:**
  - `forecast_id` (int): Unique identifier for forecast
  - `location_id` (int): Foreign key to location
  - `date` (str): Date in `YYYY-MM-DD` format
  - `high_temp` (float/int): High temperature forecast
  - `low_temp` (float/int): Low temperature forecast
  - `condition` (str): Weather condition
  - `precipitation` (int): Precipitation percentage
  - `humidity` (int): Humidity percentage
- **Example Lines:**
  ```
  1|1|2025-01-21|75|60|Sunny|0|60
  2|1|2025-01-22|68|55|Cloudy|10|70
  3|2|2025-01-21|58|48|Rainy|80|85
  ```


### 3. Locations Data
- **File Path:** `data/locations.txt`
- **Field Order & Syntax:**
  `location_id|location_name|latitude|longitude|country|timezone`
- **Field Descriptions:**
  - `location_id` (int): Unique location identifier
  - `location_name` (str): Name of location
  - `latitude` (float): Latitude coordinate
  - `longitude` (float): Longitude coordinate
  - `country` (str): Country name
  - `timezone` (str): Timezone abbreviation
- **Example Lines:**
  ```
  1|New York|40.7128|-74.0060|USA|EST
  2|London|51.5074|-0.1278|UK|GMT
  3|Tokyo|35.6762|139.6503|Japan|JST
  ```


### 4. Weather Alerts Data
- **File Path:** `data/alerts.txt`
- **Field Order & Syntax:**
  `alert_id|location_id|alert_type|severity|description|start_time|end_time|is_acknowledged`
- **Field Descriptions:**
  - `alert_id` (int): Unique alert identifier
  - `location_id` (int): Foreign key to location
  - `alert_type` (str): Description of alert (e.g., Thunderstorm)
  - `severity` (str): One of `Critical`, `High`, `Medium`, `Low`
  - `description` (str): Alert detail text
  - `start_time` (str): Datetime of alert start `YYYY-MM-DD HH:MM`
  - `end_time` (str): Datetime of alert end
  - `is_acknowledged` (int): 0 or 1 indicating if alert acknowledged
- **Example Lines:**
  ```
  1|1|Thunderstorm|High|Severe thunderstorm warning in effect until 8 PM|2025-01-20 14:00|2025-01-20 20:00|0
  2|2|Fog|Medium|Dense fog advisory in effect until noon tomorrow|2025-01-20 06:00|2025-01-21 12:00|0
  3|1|Wind|Medium|High wind advisory with gusts up to 45 mph|2025-01-20 15:00|2025-01-21 09:00|1
  ```


### 5. Air Quality Data
- **File Path:** `data/air_quality.txt`
- **Field Order & Syntax:**
  `aqi_id|location_id|aqi_index|pm25|pm10|no2|o3|last_updated`
- **Field Descriptions:**
  - `aqi_id` (int): Unique air quality data id
  - `location_id` (int): Foreign key to location
  - `aqi_index` (int): Air Quality Index (0-500)
  - `pm25` (float): PM2.5 pollutant level
  - `pm10` (float): PM10 pollutant level
  - `no2` (float): NO2 pollutant level
  - `o3` (float): O3 pollutant level
  - `last_updated` (str): Datetime `YYYY-MM-DD HH:MM`
- **Example Lines:**
  ```
  1|1|45|12.5|35|28|55|2025-01-20 14:30
  2|2|67|22.3|48|42|78|2025-01-20 14:30
  3|3|120|68.5|95|65|110|2025-01-20 14:30
  ```


### 6. Saved Locations Data
- **File Path:** `data/saved_locations.txt`
- **Field Order & Syntax:**
  `saved_id|user_id|location_id|location_name|is_default`
- **Field Descriptions:**
  - `saved_id` (int): Unique saved locations record id
  - `user_id` (int): User id (no auth required, assume 1 for default user)
  - `location_id` (int): Foreign key to location
  - `location_name` (str): Name of location
  - `is_default` (int): 1 if this is default location, else 0
- **Example Lines:**
  ```
  1|1|1|New York|1
  2|1|2|London|0
  3|2|3|Tokyo|1
  ```

---

This design specification document fully defines all Flask routes, HTML template requirements, and data file schemas for the WeatherForecast web application to ensure independent yet synchronized backend and frontend implementation.
