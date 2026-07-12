# Design Specification Document for WeatherForecast Web Application

---

## Section 1: Flask Routes Specification

### 1. Root Route
- **URL Path**: `/`
- **Methods**: GET
- **Function Name**: `root_redirect`
- **Template Filename**: None (redirect)
- **Description**: Redirects to the dashboard page
- **Context Variables**: None

### 2. Dashboard Page
- **URL Path**: `/dashboard`
- **Methods**: GET
- **Function Name**: `dashboard`
- **Template Filename**: `dashboard.html`
- **Context Variables**:
  - `current_weather` : dict {
     - `location_id` (int),
     - `location_name` (str),
     - `temperature` (int),
     - `condition` (str),
     - `humidity` (int),
     - `wind_speed` (int),
     - `last_updated` (str, timestamp format `YYYY-MM-DD HH:mm`)
   } 

### 3. Current Weather Page
- **URL Path**: `/weather/current/<int:location_id>`
- **Methods**: GET
- **Function Name**: `current_weather`
- **Template Filename**: `current_weather.html`
- **Context Variables**:
  - `location_name` (str)
  - `temperature` (int)
  - `condition` (str)
  - `humidity` (int)
  - `wind_speed` (int)

### 4. Weekly Forecast Page
- **URL Path**: `/forecast/weekly`
- **Methods**: GET, POST (POST used to select/filter location)
- **Function Name**: `weekly_forecast`
- **Template Filename**: `weekly_forecast.html`
- **Context Variables**:
  - `locations` : list of dicts each with {
      - `location_id` (int),
      - `location_name` (str)
    }
  - `selected_location_id` (int)
  - `forecast_list` : list of dicts each with {
      - `date` (str, `YYYY-MM-DD`),
      - `high_temp` (int),
      - `low_temp` (int),
      - `condition` (str)
    }

### 5. Location Search Page
- **URL Path**: `/locations/search`
- **Methods**: GET, POST (POST to submit search query)
- **Function Name**: `location_search`
- **Template Filename**: `location_search.html`
- **Context Variables**:
  - `search_query` (str)
  - `search_results`: list of dicts each with {
      - `location_id` (int),
      - `location_name` (str),
      - `latitude` (float),
      - `longitude` (float),
      - `country` (str)
    }
  - `saved_locations`: list of dicts each with {
      - `location_id` (int),
      - `location_name` (str)
    }

### 6. Weather Alerts Page
- **URL Path**: `/alerts`
- **Methods**: GET, POST (POST used to filter or acknowledge)
- **Function Name**: `weather_alerts`
- **Template Filename**: `weather_alerts.html`
- **Context Variables**:
  - `alerts_list`: list of dicts each with {
      - `alert_id` (int),
      - `location_id` (int),
      - `alert_type` (str),
      - `severity` (str),
      - `description` (str),
      - `start_time` (str, `YYYY-MM-DD HH:mm`),
      - `end_time` (str, `YYYY-MM-DD HH:mm`),
      - `is_acknowledged` (bool)
    }
  - `severity_filter` (str) - one of: All, Critical, High, Medium, Low
  - `location_filter` (int or None) - location_id for filtering or None

### 7. Air Quality Page
- **URL Path**: `/air_quality`
- **Methods**: GET, POST (POST to select/filter location)
- **Function Name**: `air_quality`
- **Template Filename**: `air_quality.html`
- **Context Variables**:
  - `locations`: list of dicts each with {
      - `location_id` (int),
      - `location_name` (str)
    }
  - `selected_location_id` (int)
  - `aqi_index` (int, 0-500)
  - `aqi_description` (str)
  - `pollution_details`: dict {
      - `pm25` (float),
      - `pm10` (float),
      - `no2` (float),
      - `o3` (float)
    }
  - `health_recommendation` (str)

### 8. Saved Locations Page
- **URL Path**: `/locations/saved`
- **Methods**: GET, POST (POST for actions like remove or add)
- **Function Name**: `saved_locations`
- **Template Filename**: `saved_locations.html`
- **Context Variables**:
  - `saved_locations`: list of dicts each with {
      - `location_id` (int),
      - `location_name` (str),
      - `current_temp` (int),
      - `condition` (str)
    }

### 9. Settings Page
- **URL Path**: `/settings`
- **Methods**: GET, POST (POST to save settings)
- **Function Name**: `settings`
- **Template Filename**: `settings.html`
- **Context Variables**:
  - `temperature_units_options`: list of str (exact values: "Celsius", "Fahrenheit", "Kelvin")
  - `selected_temperature_unit`: str
  - `locations`: list of dicts each with {
      - `location_id` (int),
      - `location_name` (str)
    }
  - `selected_default_location_id`: int
  - `alert_notifications_enabled`: bool

---

## Section 2: Frontend HTML Templates Specification

### 1. templates/dashboard.html
- **Page Title**: Weather Dashboard
- **Available Context Variables**:
  - `current_weather` (dict)
- **Element IDs and Details**:
  - `dashboard-page` (Div): Container for dashboard page
  - `current-weather-summary` (Div): Displays current weather for default location
  - `search-location-button` (Button): Navigate to Location Search page
  - `view-forecast-button` (Button): Navigate to Weekly Forecast page
  - `view-alerts-button` (Button): Navigate to Weather Alerts page
- **Navigation Mappings**:
  - `search-location-button` -> `url_for('location_search')`
  - `view-forecast-button` -> `url_for('weekly_forecast')`
  - `view-alerts-button` -> `url_for('weather_alerts')`
- **Usage Notes**:
  - Display weather information inside `current-weather-summary` using `current_weather` fields

### 2. templates/current_weather.html
- **Page Title**: Current Weather
- **Available Context Variables**:
  - `location_name` (str)
  - `temperature` (int)
  - `condition` (str)
  - `humidity` (int)
  - `wind_speed` (int)
- **Element IDs and Details**:
  - `current-weather-page` (Div): Container
  - `location-name` (H1): Display location name
  - `temperature-display` (Div): Show temperature
  - `weather-condition` (Div): Show weather condition
  - `humidity-info` (Div): Show humidity %
  - `wind-speed-info` (Div): Show wind speed
- **Navigation Mappings**:
  - No navigation buttons specified
- **Usage Notes**:
  - Render values directly into respective elements

### 3. templates/weekly_forecast.html
- **Page Title**: Weekly Forecast
- **Available Context Variables**:
  - `locations` (list of dicts)
  - `selected_location_id` (int)
  - `forecast_list` (list of dicts)
- **Element IDs and Details**:
  - `forecast-page` (Div): Container for forecast page
  - `forecast-table` (Table): Display rows with date, high temp, low temp, condition
  - `location-filter` (Dropdown): Select location filters
  - `forecast-list` (Div): Grid showing forecast cards for each day
  - `back-to-dashboard` (Button): Navigate back to dashboard
- **Navigation Mappings**:
  - `back-to-dashboard` -> `url_for('dashboard')`
- **Usage Notes**:
  - Use loop to render `forecast_list` rows/cards
  - Use dropdown `location-filter` linked to `selected_location_id`

### 4. templates/location_search.html
- **Page Title**: Search Locations
- **Available Context Variables**:
  - `search_query` (str)
  - `search_results` (list of dicts)
  - `saved_locations` (list of dicts)
- **Element IDs and Details**:
  - `search-page` (Div): Container
  - `location-search-input` (Input): Input for search
  - `search-results` (Div): List of matching locations
  - `select-location-button-{location_id}` (Button): Select location button for each result
  - `saved-locations-list` (Div): Display saved locations
- **Navigation Mappings**:
  - Selecting a location via `select-location-button-{location_id}` triggers POST to select/save
- **Usage Notes**:
  - Loop over `search_results` to create result items and dynamically IDed select buttons
  - Display `saved_locations` in `saved-locations-list`

### 5. templates/weather_alerts.html
- **Page Title**: Weather Alerts
- **Available Context Variables**:
  - `alerts_list` (list of dicts)
  - `severity_filter` (str)
  - `location_filter` (int or None)
- **Element IDs and Details**:
  - `alerts-page` (Div): Container
  - `alerts-list` (Div): List all active alerts
  - `severity-filter` (Dropdown): Filter by severity
  - `location-filter-alerts` (Dropdown): Filter by location
  - `acknowledge-alert-button-{alert_id}` (Button): Acknowledge alert button
- **Navigation Mappings**:
  - No direct navigation buttons specified
- **Usage Notes**:
  - Loop over `alerts_list` to show alerts with dynamic acknowledge buttons
  - Filters apply to filter displayed alerts

### 6. templates/air_quality.html
- **Page Title**: Air Quality Index
- **Available Context Variables**:
  - `locations` (list of dicts)
  - `selected_location_id` (int)
  - `aqi_index` (int)
  - `aqi_description` (str)
  - `pollution_details` (dict)
  - `health_recommendation` (str)
- **Element IDs and Details**:
  - `air-quality-page` (Div): Container
  - `aqi-display` (Div): Show AQI value
  - `aqi-description` (Div): Show AQI description
  - `pollution-details` (Table): Table with PM2.5, PM10, NO2, O3
  - `location-aqi-filter` (Dropdown): Filter location
  - `health-recommendation` (Div): Health recommendations
- **Navigation Mappings**:
  - No direct navigation buttons specified
- **Usage Notes**:
  - Render pollution details in table
  - Dropdown for location selection

### 7. templates/saved_locations.html
- **Page Title**: Saved Locations
- **Available Context Variables**:
  - `saved_locations` (list of dicts)
- **Element IDs and Details**:
  - `saved-locations-page` (Div): Container
  - `locations-table` (Table): Shows saved locations with current temperature and condition
  - `view-location-weather-{location_id}` (Button): View weather page button
  - `remove-location-button-{location_id}` (Button): Remove saved location
  - `add-new-location-button` (Button): Add new location
- **Navigation Mappings**:
  - `view-location-weather-{location_id}` -> `url_for('current_weather', location_id=location_id)`
  - `add-new-location-button` -> `url_for('location_search')`
- **Usage Notes**:
  - Loop over `saved_locations` to render table rows with buttons

### 8. templates/settings.html
- **Page Title**: Settings
- **Available Context Variables**:
  - `temperature_units_options` (list of str)
  - `selected_temperature_unit` (str)
  - `locations` (list of dicts)
  - `selected_default_location_id` (int)
  - `alert_notifications_enabled` (bool)
- **Element IDs and Details**:
  - `settings-page` (Div): Container
  - `temperature-unit-select` (Dropdown): Select temperature unit
  - `default-location-select` (Dropdown): Select default location
  - `alert-notifications-toggle` (Checkbox): Enable/disable alerts
  - `save-settings-button` (Button): Save changes
  - `back-to-dashboard` (Button): Navigate back to dashboard
- **Navigation Mappings**:
  - `back-to-dashboard` -> `url_for('dashboard')`
- **Usage Notes**:
  - Render dropdown selections with current choices
  - Checkbox reflects enabled state

---

## Section 3: Data File Schemas

### 1. data/current_weather.txt
- **Fields (pipe-delimited)**:
  1. `location_id` (int): Unique identifier for location
  2. `location_name` (str): Name of the location
  3. `temperature` (int): Current temperature in Fahrenheit (or unit as per settings)
  4. `condition` (str): Weather condition (e.g., Sunny, Rainy, Cloudy)
  5. `humidity` (int): Humidity percentage (0-100)
  6. `wind_speed` (int): Wind speed in mph
  7. `last_updated` (str): Timestamp in format `YYYY-MM-DD HH:mm`
- **Example Lines**:
  ```
  1|New York|72|Sunny|65|10|2025-01-20 14:30
  2|London|55|Rainy|80|15|2025-01-20 14:30
  3|Tokyo|45|Cloudy|72|8|2025-01-20 14:30
  ```

### 2. data/forecasts.txt
- **Fields (pipe-delimited)**:
  1. `forecast_id` (int): Unique forecast entry ID
  2. `location_id` (int): Location identifier
  3. `date` (str): Date for forecast, format `YYYY-MM-DD`
  4. `high_temp` (int): Highest temp predicted
  5. `low_temp` (int): Lowest temp predicted
  6. `condition` (str): Weather condition
  7. `precipitation` (int): Precipitation percentage (0-100)
  8. `humidity` (int): Humidity percentage (0-100)
- **Example Lines**:
  ```
  1|1|2025-01-21|75|60|Sunny|0|60
  2|1|2025-01-22|68|55|Cloudy|10|70
  3|2|2025-01-21|58|48|Rainy|80|85
  ```

### 3. data/locations.txt
- **Fields (pipe-delimited)**:
  1. `location_id` (int): Unique ID for location
  2. `location_name` (str): City or location name
  3. `latitude` (float): Latitude coordinate
  4. `longitude` (float): Longitude coordinate
  5. `country` (str): Country
  6. `timezone` (str): Timezone abbrev
- **Example Lines**:
  ```
  1|New York|40.7128|-74.0060|USA|EST
  2|London|51.5074|-0.1278|UK|GMT
  3|Tokyo|35.6762|139.6503|Japan|JST
  ```

### 4. data/alerts.txt
- **Fields (pipe-delimited)**:
  1. `alert_id` (int): Unique alert ID
  2. `location_id` (int): Location ID
  3. `alert_type` (str): Type of alert (e.g., Thunderstorm, Fog)
  4. `severity` (str): Severity level (Critical, High, Medium, Low)
  5. `description` (str): Description of alert
  6. `start_time` (str): Start time `YYYY-MM-DD HH:mm`
  7. `end_time` (str): End time `YYYY-MM-DD HH:mm`
  8. `is_acknowledged` (int): 0 = not acknowledged, 1 = acknowledged
- **Example Lines**:
  ```
  1|1|Thunderstorm|High|Severe thunderstorm warning in effect until 8 PM|2025-01-20 14:00|2025-01-20 20:00|0
  2|2|Fog|Medium|Dense fog advisory in effect until noon tomorrow|2025-01-20 06:00|2025-01-21 12:00|0
  3|1|Wind|Medium|High wind advisory with gusts up to 45 mph|2025-01-20 15:00|2025-01-21 09:00|1
  ```

### 5. data/air_quality.txt
- **Fields (pipe-delimited)**:
  1. `aqi_id` (int): Unique Air Quality Index entry ID
  2. `location_id` (int): Location ID
  3. `aqi_index` (int): AQI value (0-500 scale)
  4. `pm25` (float): PM2.5 pollutant level
  5. `pm10` (float): PM10 pollutant level
  6. `no2` (float): NO2 pollutant level
  7. `o3` (float): O3 pollutant level
  8. `last_updated` (str): Timestamp `YYYY-MM-DD HH:mm`
- **Example Lines**:
  ```
  1|1|45|12.5|35|28|55|2025-01-20 14:30
  2|2|67|22.3|48|42|78|2025-01-20 14:30
  3|3|120|68.5|95|65|110|2025-01-20 14:30
  ```

### 6. data/saved_locations.txt
- **Fields (pipe-delimited)**:
  1. `saved_id` (int): Unique saved location entry ID
  2. `user_id` (int): User ID (single user assumed, user_id=1)
  3. `location_id` (int): Location ID
  4. `location_name` (str): Location name
  5. `is_default` (int): 1 = default location, 0 = not default
- **Example Lines**:
  ```
  1|1|1|New York|1
  2|1|2|London|0
  3|2|3|Tokyo|1
  ```

---

End of Design Specification Document
