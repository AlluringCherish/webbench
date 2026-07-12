# Design Specification Document for WeatherForecast Web Application

---

## Section 1: Flask Routes Specification

### 1. Root Route
- URL Path: `/`
- Methods Allowed: `GET`
- Function Name: `root_redirect`
- Behavior: Redirects to `/dashboard` route
- Template: None
- Context Variables: None

### 2. Dashboard Page
- URL Path: `/dashboard`
- Methods Allowed: `GET`
- Function Name: `dashboard`
- Template Filename: `dashboard.html`
- Context Variables:
  - `default_location`: `dict` with fields:
    - `location_id` (int)
    - `location_name` (str)
    - `temperature` (float or int)
    - `condition` (str)
  - `saved_locations`: list of dicts with fields:
    - `location_id` (int)
    - `location_name` (str)

### 3. Current Weather Page
- URL Path: `/weather/current/<int:location_id>`
- Methods Allowed: `GET`
- Function Name: `current_weather`
- Template Filename: `current_weather.html`
- Context Variables:
  - `location_name`: `str`
  - `temperature`: `float` or `int`
  - `condition`: `str`
  - `humidity`: `int` (percentage)
  - `wind_speed`: `float` or `int`

### 4. Weekly Forecast Page
- URL Path: `/forecast/weekly`
- Methods Allowed: `GET`, `POST`
- Function Name: `weekly_forecast`
- Template Filename: `weekly_forecast.html`
- Context Variables:
  - `locations`: list of dicts with fields:
    - `location_id` (int)
    - `location_name` (str)
  - `selected_location_id`: `int`
  - `forecasts`: list of dicts with fields:
    - `date` (str, formatted as `YYYY-MM-DD`)
    - `high_temp` (float or int)
    - `low_temp` (float or int)
    - `condition` (str)

### 5. Location Search Page
- URL Path: `/search`
- Methods Allowed: `GET`, `POST`
- Function Name: `location_search`
- Template Filename: `location_search.html`
- Context Variables:
  - `search_results`: list of dicts with fields:
    - `location_id` (int)
    - `location_name` (str)
    - `latitude` (float)
    - `longitude` (float)
  - `saved_locations`: list of dicts with fields:
    - `location_id` (int)
    - `location_name` (str)

### 6. Weather Alerts Page
- URL Path: `/alerts`
- Methods Allowed: `GET`, `POST`
- Function Name: `weather_alerts`
- Template Filename: `alerts.html`
- Context Variables:
  - `alerts`: list of dicts with fields:
    - `alert_id` (int)
    - `location_id` (int)
    - `alert_type` (str)
    - `severity` (str)
    - `description` (str)
    - `start_time` (str, formatted `YYYY-MM-DD HH:MM`)
    - `end_time` (str, formatted `YYYY-MM-DD HH:MM`)
    - `is_acknowledged` (bool)
  - `severity_filter`: `str`
  - `location_filter`: `int` or `None`

### 7. Air Quality Page
- URL Path: `/air_quality`
- Methods Allowed: `GET`, `POST`
- Function Name: `air_quality`
- Template Filename: `air_quality.html`
- Context Variables:
  - `locations`: list of dicts with fields:
    - `location_id` (int)
    - `location_name` (str)
  - `selected_location_id`: `int`
  - `aqi_data`: `dict` with fields:
    - `aqi_index` (int)
    - `pm25` (float)
    - `pm10` (float)
    - `no2` (float)
    - `o3` (float)
    - `last_updated` (str, formatted `YYYY-MM-DD HH:MM`)
  - `description`: `str`
  - `health_recommendation`: `str`

### 8. Saved Locations Page
- URL Path: `/saved_locations`
- Methods Allowed: `GET`, `POST`
- Function Name: `saved_locations`
- Template Filename: `saved_locations.html`
- Context Variables:
  - `saved_locations`: list of dicts with fields:
    - `location_id` (int)
    - `location_name` (str)
    - `temperature` (float or int)
    - `condition` (str)

### 9. Settings Page
- URL Path: `/settings`
- Methods Allowed: `GET`, `POST`
- Function Name: `settings`
- Template Filename: `settings.html`
- Context Variables:
  - `temperature_units`: list of `str` (e.g., ["Celsius", "Fahrenheit", "Kelvin"])
  - `selected_unit`: `str`
  - `saved_locations`: list of dicts with fields:
    - `location_id` (int)
    - `location_name` (str)
  - `default_location_id`: `int`
  - `alert_notifications_enabled`: `bool`

---

## Section 2: Frontend HTML Templates Specification

### 1. templates/dashboard.html
- Page Title: "Weather Dashboard"
- Element IDs:
  - `dashboard-page`: Div, main container for dashboard
  - `current-weather-summary`: Div, summary of current default location weather
  - `search-location-button`: Button, navigates to Location Search page
  - `view-forecast-button`: Button, navigates to Weekly Forecast page
  - `view-alerts-button`: Button, navigates to Weather Alerts page
- Navigation mappings:
  - `search-location-button` → `url_for('location_search')`
  - `view-forecast-button` → `url_for('weekly_forecast')`
  - `view-alerts-button` → `url_for('weather_alerts')`
- Context variables:
  - `default_location` (dict) with `location_id`, `location_name`, `temperature`, `condition`
  - `saved_locations` (list of dicts) with `location_id`, `location_name`
- Usage notes:
  - Display current weather summary for `default_location` in `current-weather-summary`
  - Provide quick navigation buttons to other pages

### 2. templates/current_weather.html
- Page Title: "Current Weather"
- Element IDs:
  - `current-weather-page`: Div, main container
  - `location-name`: H1, displays location name
  - `temperature-display`: Div, displays temperature
  - `weather-condition`: Div, displays current weather condition
  - `humidity-info`: Div, humidity percentage
  - `wind-speed-info`: Div, wind speed
- Navigation mappings:
  - Provide 'Back to Dashboard' link/button using `url_for('dashboard')`
- Context variables:
  - `location_name` (str)
  - `temperature` (float/int)
  - `condition` (str)
  - `humidity` (int)
  - `wind_speed` (float/int)
- Usage notes:
  - Display detailed weather info for selected location

### 3. templates/weekly_forecast.html
- Page Title: "Weekly Forecast"
- Element IDs:
  - `forecast-page`: Div, main container
  - `forecast-table`: Table, displays daily forecasts (date, high temp, low temp, condition)
  - `location-filter`: Dropdown, filter forecasts by location
  - `forecast-list`: Div, grid display of forecast cards for each day
  - `back-to-dashboard`: Button, navigates back to dashboard
- Navigation mappings:
  - `back-to-dashboard` → `url_for('dashboard')`
- Context variables:
  - `locations` (list of dicts with location_id, location_name)
  - `selected_location_id` (int)
  - `forecasts` (list of dicts with date, high_temp, low_temp, condition)
- Usage notes:
  - Use dropdown `location-filter` to select location and reload forecasts
  - Loop through `forecasts` to populate `forecast-list` and `forecast-table`

### 4. templates/location_search.html
- Page Title: "Search Locations"
- Element IDs:
  - `search-page`: Div, main container
  - `location-search-input`: Input field for search query
  - `search-results`: Div, displays list of matching locations
  - `select-location-button-{location_id}`: Button for each search result to select location
  - `saved-locations-list`: Div, displays previously saved locations
- Navigation mappings:
  - Buttons `select-location-button-{location_id}` trigger backend POST to select location
- Context variables:
  - `search_results` (list of dicts with location_id, location_name, latitude, longitude)
  - `saved_locations` (list of dicts with location_id, location_name)
- Usage notes:
  - Dynamic generation of `select-location-button-{location_id}` for each search result
  - Display saved locations with quick access

### 5. templates/alerts.html
- Page Title: "Weather Alerts"
- Element IDs:
  - `alerts-page`: Div, main container
  - `alerts-list`: Div, displays active alerts
  - `severity-filter`: Dropdown, filter alerts by severity
  - `location-filter-alerts`: Dropdown, filter alerts by location
  - `acknowledge-alert-button-{alert_id}`: Button to acknowledge each alert
- Navigation mappings:
  - Filter dropdowns trigger POST requests to update alert list
  - Buttons `acknowledge-alert-button-{alert_id}` POST to acknowledge alert
- Context variables:
  - `alerts` (list of dicts with alert_id, location_id, alert_type, severity, description, start_time, end_time, is_acknowledged)
  - `severity_filter` (str)
  - `location_filter` (int or None)
- Usage notes:
  - Loop through `alerts` to display details
  - Buttons have dynamic IDs with alert_id

### 6. templates/air_quality.html
- Page Title: "Air Quality Index"
- Element IDs:
  - `air-quality-page`: Div, main container
  - `aqi-display`: Div, display AQI value
  - `aqi-description`: Div, display AQI description
  - `pollution-details`: Table, show PM2.5, PM10, NO2, O3
  - `location-aqi-filter`: Dropdown, filter by location
  - `health-recommendation`: Div, health recommendations
- Navigation mappings:
  - Changing `location-aqi-filter` triggers POST to update AQI data
- Context variables:
  - `locations` (list of dicts with location_id, location_name)
  - `selected_location_id` (int)
  - `aqi_data` (dict with aqi_index, pm25, pm10, no2, o3, last_updated)
  - `description` (str)
  - `health_recommendation` (str)
- Usage notes:
  - Show air quality details for selected location

### 7. templates/saved_locations.html
- Page Title: "Saved Locations"
- Element IDs:
  - `saved-locations-page`: Div, main container
  - `locations-table`: Table listing saved locations
  - `view-location-weather-{location_id}`: Button to view weather per location
  - `remove-location-button-{location_id}`: Button to remove saved location
  - `add-new-location-button`: Button to add location
- Navigation mappings:
  - Buttons with dynamic IDs send POST requests for viewing/removing
  - `add-new-location-button` navigates to `/search` via `url_for('location_search')`
- Context variables:
  - `saved_locations` (list of dicts with location_id, location_name, temperature, condition)
- Usage notes:
  - Loop to generate dynamic buttons with location_id

### 8. templates/settings.html
- Page Title: "Settings"
- Element IDs:
  - `settings-page`: Div, main container
  - `temperature-unit-select`: Dropdown for temp units
  - `default-location-select`: Dropdown for default location
  - `alert-notifications-toggle`: Checkbox toggle for alerts
  - `save-settings-button`: Button to save settings
  - `back-to-dashboard`: Button to navigate back
- Navigation mappings:
  - `back-to-dashboard` → `url_for('dashboard')`
- Context variables:
  - `temperature_units` (list of str)
  - `selected_unit` (str)
  - `saved_locations` (list of dicts with location_id, location_name)
  - `default_location_id` (int)
  - `alert_notifications_enabled` (bool)
- Usage notes:
  - Render dropdowns and toggles with current saved settings
  - Provide save button to persist changes

---

## Section 3: Data File Schemas

### 1. Current Weather Data
- File Path: `data/current_weather.txt`
- Format: Pipe-delimited
- Fields (in order):
  1. `location_id` (int): Unique identifier for location
  2. `location_name` (str): Name of the location
  3. `temperature` (int or float): Current temperature
  4. `condition` (str): Weather condition (e.g., Sunny, Rainy)
  5. `humidity` (int): Humidity percentage
  6. `wind_speed` (int or float): Wind speed
  7. `last_updated` (str): Timestamp in `YYYY-MM-DD HH:MM` format
- Data Description: Stores current weather conditions for multiple locations
- Example Lines:
  ```
  1|New York|72|Sunny|65|10|2025-01-20 14:30
  2|London|55|Rainy|80|15|2025-01-20 14:30
  3|Tokyo|45|Cloudy|72|8|2025-01-20 14:30
  ```

### 2. Forecasts Data
- File Path: `data/forecasts.txt`
- Format: Pipe-delimited
- Fields (in order):
  1. `forecast_id` (int): Unique forecast entry identifier
  2. `location_id` (int): Identifier of location
  3. `date` (str): Date of forecast `YYYY-MM-DD`
  4. `high_temp` (int or float): Forecast high temperature
  5. `low_temp` (int or float): Forecast low temperature
  6. `condition` (str): Weather condition
  7. `precipitation` (int): Percentage chance of precipitation
  8. `humidity` (int): Forecast humidity percentage
- Data Description: Daily weather forecast data for locations
- Example Lines:
  ```
  1|1|2025-01-21|75|60|Sunny|0|60
  2|1|2025-01-22|68|55|Cloudy|10|70
  3|2|2025-01-21|58|48|Rainy|80|85
  ```

### 3. Locations Data
- File Path: `data/locations.txt`
- Format: Pipe-delimited
- Fields (in order):
  1. `location_id` (int): Unique identifier for location
  2. `location_name` (str): Name of location
  3. `latitude` (float): Latitude coordinate
  4. `longitude` (float): Longitude coordinate
  5. `country` (str): Country name
  6. `timezone` (str): Time zone abbreviation
- Data Description: Stores metadata for all known locations
- Example Lines:
  ```
  1|New York|40.7128|-74.0060|USA|EST
  2|London|51.5074|-0.1278|UK|GMT
  3|Tokyo|35.6762|139.6503|Japan|JST
  ```

### 4. Weather Alerts Data
- File Path: `data/alerts.txt`
- Format: Pipe-delimited
- Fields (in order):
  1. `alert_id` (int): Unique alert identifier
  2. `location_id` (int): Location associated with alert
  3. `alert_type` (str): Type of alert (e.g., Thunderstorm)
  4. `severity` (str): Alert severity (Critical, High, Medium, Low)
  5. `description` (str): Alert text description
  6. `start_time` (str): Start timestamp `YYYY-MM-DD HH:MM`
  7. `end_time` (str): End timestamp `YYYY-MM-DD HH:MM`
  8. `is_acknowledged` (int): 0 for false, 1 for true
- Data Description: Active weather alerts
- Example Lines:
  ```
  1|1|Thunderstorm|High|Severe thunderstorm warning in effect until 8 PM|2025-01-20 14:00|2025-01-20 20:00|0
  2|2|Fog|Medium|Dense fog advisory in effect until noon tomorrow|2025-01-20 06:00|2025-01-21 12:00|0
  3|1|Wind|Medium|High wind advisory with gusts up to 45 mph|2025-01-20 15:00|2025-01-21 09:00|1
  ```

### 5. Air Quality Data
- File Path: `data/air_quality.txt`
- Format: Pipe-delimited
- Fields (in order):
  1. `aqi_id` (int): Unique air quality entry identifier
  2. `location_id` (int): Location identifier
  3. `aqi_index` (int): Air Quality Index value (0-500)
  4. `pm25` (float): PM2.5 concentration
  5. `pm10` (float): PM10 concentration
  6. `no2` (float): NO2 concentration
  7. `o3` (float): O3 concentration
  8. `last_updated` (str): Timestamp `YYYY-MM-DD HH:MM`
- Data Description: Air quality measurements for locations
- Example Lines:
  ```
  1|1|45|12.5|35|28|55|2025-01-20 14:30
  2|2|67|22.3|48|42|78|2025-01-20 14:30
  3|3|120|68.5|95|65|110|2025-01-20 14:30
  ```

### 6. Saved Locations Data
- File Path: `data/saved_locations.txt`
- Format: Pipe-delimited
- Fields (in order):
  1. `saved_id` (int): Unique saved location identifier
  2. `user_id` (int): User identifier (no authentication, can be static or default)
  3. `location_id` (int): Location identifier
  4. `location_name` (str): Name of saved location
  5. `is_default` (int): 1 if location is default, else 0
- Data Description: Locations saved by users for quick access
- Example Lines:
  ```
  1|1|1|New York|1
  2|1|2|London|0
  3|2|3|Tokyo|1
  ```
