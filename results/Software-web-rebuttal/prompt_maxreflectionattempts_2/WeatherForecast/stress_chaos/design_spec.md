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
  - `default_location` (dict): {
      - `location_id` (int),
      - `location_name` (str),
      - `temperature` (float),
      - `condition` (str),
      - `humidity` (int),
      - `wind_speed` (float)
    }
  - `saved_locations` (list of dict): Each dict with fields:
      - `location_id` (int),
      - `location_name` (str)

### 3. Current Weather Page
- **URL Path:** `/weather/current/<int:location_id>`
- **HTTP Methods:** GET
- **Function Name:** `current_weather`
- **Template:** `current_weather.html`
- **Context Variables:**
  - `location_info` (dict): {
      - `location_id` (int),
      - `location_name` (str)
    }
  - `weather_data` (dict): {
      - `temperature` (float),
      - `condition` (str),
      - `humidity` (int),
      - `wind_speed` (float),
      - `last_updated` (str, datetime formatted string)
    }

### 4. Weekly Forecast Page
- **URL Path:** `/forecast/weekly`
- **HTTP Methods:** GET
- **Function Name:** `weekly_forecast`
- **Template:** `weekly_forecast.html`
- **Context Variables:**
  - `locations` (list of dict): Each dict with fields:
      - `location_id` (int),
      - `location_name` (str)
  - `selected_location_id` (int or None): Currently selected location to filter forecast
  - `forecasts` (list of dict): Each dict with fields:
      - `forecast_id` (int),
      - `date` (str, YYYY-MM-DD),
      - `high_temp` (float),
      - `low_temp` (float),
      - `condition` (str),
      - `precipitation` (int),
      - `humidity` (int)

### 5. Location Search Page
- **URL Path:** `/search/locations`
- **HTTP Methods:** GET, POST
- **Function Name:** `location_search`
- **Template:** `location_search.html`
- **Context Variables:**
  - `search_query` (str, optional): Current search string or empty
  - `search_results` (list of dict): Each dict with fields:
      - `location_id` (int),
      - `location_name` (str),
      - `latitude` (float),
      - `longitude` (float),
      - `country` (str)
  - `saved_locations` (list of dict): Each dict with fields:
      - `location_id` (int),
      - `location_name` (str)

### 6. Weather Alerts Page
- **URL Path:** `/alerts`
- **HTTP Methods:** GET
- **Function Name:** `weather_alerts`
- **Template:** `weather_alerts.html`
- **Context Variables:**
  - `alerts` (list of dict): Each dict with fields:
      - `alert_id` (int),
      - `location_id` (int),
      - `location_name` (str),
      - `alert_type` (str),
      - `severity` (str),
      - `description` (str),
      - `start_time` (str, datetime formatted string),
      - `end_time` (str, datetime formatted string),
      - `is_acknowledged` (bool)
  - `severity_filter` (str): Current selected filter e.g. "All", "Critical", "High", "Medium", "Low"
  - `location_filter` (int or None): Selected location id for filtering

### 7. Air Quality Page
- **URL Path:** `/air_quality`
- **HTTP Methods:** GET
- **Function Name:** `air_quality`
- **Template:** `air_quality.html`
- **Context Variables:**
  - `locations` (list of dict): Each dict with fields:
      - `location_id` (int),
      - `location_name` (str)
  - `selected_location_id` (int or None)
  - `air_quality_data` (dict or None): {
      - `aqi_index` (int),
      - `pm25` (float),
      - `pm10` (float),
      - `no2` (float),
      - `o3` (float),
      - `last_updated` (str, datetime formatted string)
    } or None if no data available
  - `aqi_description` (str): Based on `aqi_index` value (e.g., Good, Moderate, Unhealthy)
  - `health_recommendation` (str): Text recommendation based on air quality

### 8. Saved Locations Page
- **URL Path:** `/saved_locations`
- **HTTP Methods:** GET
- **Function Name:** `saved_locations`
- **Template:** `saved_locations.html`
- **Context Variables:**
  - `saved_locations` (list of dict): Each dict with fields:
      - `saved_id` (int),
      - `location_id` (int),
      - `location_name` (str),
      - `current_temperature` (float),
      - `current_condition` (str),
      - `is_default` (bool)

### 9. Settings Page
- **URL Path:** `/settings`
- **HTTP Methods:** GET, POST
- **Function Name:** `settings`
- **Template:** `settings.html`
- **Context Variables:**
  - `temperature_units` (list of str): ["Celsius", "Fahrenheit", "Kelvin"]
  - `selected_unit` (str): Current selected temperature unit
  - `saved_locations` (list of dict): Each dict with fields:
      - `location_id` (int),
      - `location_name` (str)
  - `default_location_id` (int or None)
  - `alert_notifications_enabled` (bool)

---

## Section 2: Frontend HTML Templates Specification

### 1. templates/dashboard.html
- **Page Title:** Weather Dashboard
- **Heading (h1):** Weather Dashboard
- **Element IDs and Types:**
  - `dashboard-page` (div): Container for dashboard page
  - `current-weather-summary` (div): Display current weather for default location
  - `search-location-button` (button): Navigates to `location_search` route
  - `view-forecast-button` (button): Navigates to `weekly_forecast` route
  - `view-alerts-button` (button): Navigates to `weather_alerts` route
- **Navigation mappings:**
  - `search-location-button` -> `url_for('location_search')`
  - `view-forecast-button` -> `url_for('weekly_forecast')`
  - `view-alerts-button` -> `url_for('weather_alerts')`
- **Context Variables:**
  - `default_location` (dict): use fields to fill current-weather-summary
  - `saved_locations` (list of dict): for any related UI if shown
- **Usage Notes:**
  - Static display of default location weather summary
  - Buttons trigger navigation to respective pages

### 2. templates/current_weather.html
- **Page Title:** Current Weather
- **Heading (h1):** Location Name from `location_info.location_name`
- **Element IDs and Types:**
  - `current-weather-page` (div): Container for the page
  - `location-name` (h1): Display location name
  - `temperature-display` (div): Show temperature value
  - `weather-condition` (div): Show weather condition text
  - `humidity-info` (div): Show humidity percentage
  - `wind-speed-info` (div): Show wind speed
- **Navigation mappings:** None explicitly
- **Context Variables:**
  - `location_info` (dict)
  - `weather_data` (dict)
- **Usage Notes:**
  - Static page filled with current weather details

### 3. templates/weekly_forecast.html
- **Page Title:** Weekly Forecast
- **Heading (h1):** Weekly Forecast
- **Element IDs and Types:**
  - `forecast-page` (div): Container
  - `forecast-table` (table): Display forecast rows
  - `location-filter` (select/dropdown): Select location filter
  - `forecast-list` (div): Grid displaying forecast cards for each day
  - `back-to-dashboard` (button): Navigates to dashboard
- **Navigation mappings:**
  - `location-filter` -> on change, reload page with location filtering
  - `back-to-dashboard` -> `url_for('dashboard')`
- **Context Variables:**
  - `locations` (list of dict)
  - `selected_location_id` (int or None)
  - `forecasts` (list of dict)
- **Usage Notes:**
  - Render location dropdown options
  - Render forecast_table rows dynamically using `forecasts`

### 4. templates/location_search.html
- **Page Title:** Search Locations
- **Heading (h1):** Search Locations
- **Element IDs and Types:**
  - `search-page` (div): Container
  - `location-search-input` (input, text): Input for search queries
  - `search-results` (div): List container for search results
  - `select-location-button-{location_id}` (button): Button to select locations; ID dynamic per location
  - `saved-locations-list` (div): Display list of saved locations
- **Navigation mappings:**
  - `select-location-button-{location_id}` -> Call POST to `location_search` with selected location
- **Context Variables:**
  - `search_query` (str)
  - `search_results` (list of dict)
  - `saved_locations` (list of dict)
- **Usage Notes:**
  - Loop over `search_results` to render each location with select button
  - Loop over `saved_locations` to show saved locations

### 5. templates/weather_alerts.html
- **Page Title:** Weather Alerts
- **Heading (h1):** Weather Alerts
- **Element IDs and Types:**
  - `alerts-page` (div): Container
  - `alerts-list` (div): List container for all alerts
  - `severity-filter` (select/dropdown): Filter alerts by severity
  - `location-filter-alerts` (select/dropdown): Filter alerts by location
  - `acknowledge-alert-button-{alert_id}` (button): Button to acknowledge alert; dynamic ID
- **Navigation mappings:**
  - Filter dropdowns trigger reload with selected filters
  - `acknowledge-alert-button-{alert_id}` triggers action to acknowledge alert
- **Context Variables:**
  - `alerts` (list of dict)
  - `severity_filter` (str)
  - `location_filter` (int or None)
- **Usage Notes:**
  - Loop over alerts displaying details
  - Provide acknowledge buttons for each alert

### 6. templates/air_quality.html
- **Page Title:** Air Quality Index
- **Heading (h1):** Air Quality Index
- **Element IDs and Types:**
  - `air-quality-page` (div): Container
  - `aqi-display` (div): Display AQI value
  - `aqi-description` (div): Text description of AQI
  - `pollution-details` (table): Display pollutant levels (PM2.5, PM10, NO2, O3)
  - `location-aqi-filter` (select/dropdown): Filter by location
  - `health-recommendation` (div): Health recommendations
- **Navigation mappings:**
  - `location-aqi-filter` triggers page reload with filter
- **Context Variables:**
  - `locations` (list of dict)
  - `selected_location_id` (int or None)
  - `air_quality_data` (dict or None)
  - `aqi_description` (str)
  - `health_recommendation` (str)
- **Usage Notes:**
  - Render AQI data or show message if no data
  - Render pollutant table and health recommendations

### 7. templates/saved_locations.html
- **Page Title:** Saved Locations
- **Heading (h1):** Saved Locations
- **Element IDs and Types:**
  - `saved-locations-page` (div): Container
  - `locations-table` (table): Display saved locations with current temp and condition
  - `view-location-weather-{location_id}` (button): Button to view weather for location (dynamic ID)
  - `remove-location-button-{location_id}` (button): Button to remove location (dynamic ID)
  - `add-new-location-button` (button): Button to add new location
- **Navigation mappings:**
  - `view-location-weather-{location_id}` -> Navigate to `current_weather` with location_id
  - `remove-location-button-{location_id}` -> Perform remove location action
  - `add-new-location-button` -> Navigate to `location_search`
- **Context Variables:**
  - `saved_locations` (list of dict)
- **Usage Notes:**
  - Loop saved locations to fill table rows with action buttons

### 8. templates/settings.html
- **Page Title:** Settings
- **Heading (h1):** Settings
- **Element IDs and Types:**
  - `settings-page` (div): Container
  - `temperature-unit-select` (select/dropdown): Choose temperature unit
  - `default-location-select` (select/dropdown): Choose default location
  - `alert-notifications-toggle` (checkbox): Toggle notifications
  - `save-settings-button` (button): Save settings
  - `back-to-dashboard` (button): Navigate back to dashboard
- **Navigation mappings:**
  - `save-settings-button` triggers POST to save settings
  - `back-to-dashboard` -> `url_for('dashboard')`
- **Context Variables:**
  - `temperature_units` (list of str)
  - `selected_unit` (str)
  - `saved_locations` (list of dict)
  - `default_location_id` (int or None)
  - `alert_notifications_enabled` (bool)
- **Usage Notes:**
  - Render dropdowns and checkbox reflecting current settings
  - Button triggers appropriate actions

---

## Section 3: Data File Schemas

### 1. Current Weather Data
- **File:** `data/current_weather.txt`
- **Field Order and Delimiter:** `location_id|location_name|temperature|condition|humidity|wind_speed|last_updated`
- **Field Descriptions:**
  1. `location_id` (int): Unique identifier of location
  2. `location_name` (str): Name of location city
  3. `temperature` (float): Temperature in degrees (unit depends on settings)
  4. `condition` (str): Weather condition (Sunny, Rainy, Cloudy, etc.)
  5. `humidity` (int): Humidity percentage
  6. `wind_speed` (float): Wind speed in appropriate units
  7. `last_updated` (str): Timestamp in `YYYY-MM-DD HH:mm` format
- **Data Description:** Contains latest current weather data by location.
- **Example Lines:**
```
1|New York|72|Sunny|65|10|2025-01-20 14:30
2|London|55|Rainy|80|15|2025-01-20 14:30
3|Tokyo|45|Cloudy|72|8|2025-01-20 14:30
```

### 2. Forecasts Data
- **File:** `data/forecasts.txt`
- **Field Order and Delimiter:** `forecast_id|location_id|date|high_temp|low_temp|condition|precipitation|humidity`
- **Field Descriptions:**
  1. `forecast_id` (int): Unique forecast entry ID
  2. `location_id` (int): Location identifier
  3. `date` (str): Forecast date in `YYYY-MM-DD`
  4. `high_temp` (float): Predicted high temperature
  5. `low_temp` (float): Predicted low temperature
  6. `condition` (str): Weather condition
  7. `precipitation` (int): Precipitation percentage chance
  8. `humidity` (int): Humidity percentage
- **Data Description:** Contains 7 days forecasts for locations.
- **Example Lines:**
```
1|1|2025-01-21|75|60|Sunny|0|60
2|1|2025-01-22|68|55|Cloudy|10|70
3|2|2025-01-21|58|48|Rainy|80|85
```

### 3. Locations Data
- **File:** `data/locations.txt`
- **Field Order and Delimiter:** `location_id|location_name|latitude|longitude|country|timezone`
- **Field Descriptions:**
  1. `location_id` (int): Unique location identifier
  2. `location_name` (str): City or area name
  3. `latitude` (float): Geographic latitude
  4. `longitude` (float): Geographic longitude
  5. `country` (str): Country name
  6. `timezone` (str): Timezone abbreviation
- **Data Description:** Location details for weather data association.
- **Example Lines:**
```
1|New York|40.7128|-74.0060|USA|EST
2|London|51.5074|-0.1278|UK|GMT
3|Tokyo|35.6762|139.6503|Japan|JST
```

### 4. Weather Alerts Data
- **File:** `data/alerts.txt`
- **Field Order and Delimiter:** `alert_id|location_id|alert_type|severity|description|start_time|end_time|is_acknowledged`
- **Field Descriptions:**
  1. `alert_id` (int): Unique alert identifier
  2. `location_id` (int): Location affected
  3. `alert_type` (str): Type of alert (Thunderstorm, Fog, Wind, etc.)
  4. `severity` (str): Alert severity (Critical, High, Medium, Low)
  5. `description` (str): Detailed alert message
  6. `start_time` (str): Start datetime `YYYY-MM-DD HH:mm`
  7. `end_time` (str): End datetime `YYYY-MM-DD HH:mm`
  8. `is_acknowledged` (int): 0 or 1 representing boolean status
- **Data Description:** Active and historical weather alerts.
- **Example Lines:**
```
1|1|Thunderstorm|High|Severe thunderstorm warning in effect until 8 PM|2025-01-20 14:00|2025-01-20 20:00|0
2|2|Fog|Medium|Dense fog advisory in effect until noon tomorrow|2025-01-20 06:00|2025-01-21 12:00|0
3|1|Wind|Medium|High wind advisory with gusts up to 45 mph|2025-01-20 15:00|2025-01-21 09:00|1
```

### 5. Air Quality Data
- **File:** `data/air_quality.txt`
- **Field Order and Delimiter:** `aqi_id|location_id|aqi_index|pm25|pm10|no2|o3|last_updated`
- **Field Descriptions:**
  1. `aqi_id` (int): Unique air quality record
  2. `location_id` (int): Associated location
  3. `aqi_index` (int): Air Quality Index value (0-500)
  4. `pm25` (float): PM2.5 concentration
  5. `pm10` (float): PM10 concentration
  6. `no2` (float): NO2 concentration
  7. `o3` (float): Ozone concentration
  8. `last_updated` (str): DateTime `YYYY-MM-DD HH:mm`
- **Data Description:** Air pollution indicators per location.
- **Example Lines:**
```
1|1|45|12.5|35|28|55|2025-01-20 14:30
2|2|67|22.3|48|42|78|2025-01-20 14:30
3|3|120|68.5|95|65|110|2025-01-20 14:30
```

### 6. Saved Locations Data
- **File:** `data/saved_locations.txt`
- **Field Order and Delimiter:** `saved_id|user_id|location_id|location_name|is_default`
- **Field Descriptions:**
  1. `saved_id` (int): Unique saved location ID
  2. `user_id` (int): User ID (since no auth, can be defaulted or ignored)
  3. `location_id` (int): Associated location
  4. `location_name` (str): Name of the saved location
  5. `is_default` (int): 0 or 1 indicating if location is default
- **Data Description:** Stored locations saved by user(s)
- **Example Lines:**
```
1|1|1|New York|1
2|1|2|London|0
3|2|3|Tokyo|1
```

---

This design specification document provides complete detailed guidance for the backend (Flask routes and data parsing) and frontend (template structure and element IDs) teams to independently implement the WeatherForecast app with accurate synchronization.

