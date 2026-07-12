# WeatherForecast Web Application Design Specification

---

## Section 1: Flask Routes Specification

1. **Root Route**
- URL Path: `/`
- Methods: GET
- Function Name: `root_redirect`
- Template: None (Redirect to Dashboard)
- Context Variables: None
- Behavior: Redirects user to the Dashboard page.

2. **Dashboard Page**
- URL Path: `/dashboard`
- Methods: GET
- Function Name: `dashboard`
- Template: `dashboard.html`
- Context Variables:
  - `default_location` (dict) with fields:
    - `location_id` (int)
    - `location_name` (str)
    - `temperature` (float/int)
    - `condition` (str)
    - `humidity` (int)
    - `wind_speed` (float/int)

3. **Current Weather Page**
- URL Path: `/weather/current/<int:location_id>`
- Methods: GET
- Function Name: `current_weather`
- Template: `current_weather.html`
- Context Variables:
  - `location` (dict)
    - `location_id` (int)
    - `location_name` (str)
  - `temperature` (float/int)
  - `condition` (str)
  - `humidity` (int)
  - `wind_speed` (float/int)

4. **Weekly Forecast Page**
- URL Path: `/weather/forecast`
- Methods: GET
- Function Name: `weekly_forecast`
- Template: `weekly_forecast.html`
- Context Variables:
  - `locations` (list of dicts), each dict with:
    - `location_id` (int)
    - `location_name` (str)
  - `selected_location_id` (int)
  - `forecasts` (list of dicts), each dict with:
    - `date` (str, format YYYY-MM-DD)
    - `high_temp` (float/int)
    - `low_temp` (float/int)
    - `condition` (str)

5. **Location Search Page**
- URL Path: `/locations/search`
- Methods: GET, POST (POST for submitting search queries or selecting locations)
- Function Name: `location_search`
- Template: `location_search.html`
- Context Variables:
  - `search_results` (list of dicts), each dict:
    - `location_id` (int)
    - `location_name` (str)
  - `saved_locations` (list of dicts), each dict:
    - `location_id` (int)
    - `location_name` (str)

6. **Weather Alerts Page**
- URL Path: `/alerts`
- Methods: GET
- Function Name: `weather_alerts`
- Template: `weather_alerts.html`
- Context Variables:
  - `alerts` (list of dicts), each dict:
    - `alert_id` (int)
    - `location_id` (int)
    - `alert_type` (str)
    - `severity` (str)
    - `description` (str)
    - `start_time` (str)
    - `end_time` (str)
    - `is_acknowledged` (bool)
  - `severity_levels` (list of str): ["All", "Critical", "High", "Medium", "Low"]
  - `locations` (list of dicts), each dict:
    - `location_id` (int)
    - `location_name` (str)

7. **Air Quality Page**
- URL Path: `/air-quality`
- Methods: GET
- Function Name: `air_quality`
- Template: `air_quality.html`
- Context Variables:
  - `locations` (list of dicts), each dict:
    - `location_id` (int)
    - `location_name` (str)
  - `selected_location_id` (int)
  - `air_quality` (dict):
    - `aqi_index` (int)
    - `aqi_description` (str)
    - `pm25` (float)
    - `pm10` (float)
    - `no2` (float)
    - `o3` (float)
    - `last_updated` (str)
  - `health_recommendation` (str)

8. **Saved Locations Page**
- URL Path: `/locations/saved`
- Methods: GET
- Function Name: `saved_locations_page`
- Template: `saved_locations.html`
- Context Variables:
  - `saved_locations` (list of dicts), each dict:
    - `location_id` (int)
    - `location_name` (str)
    - `current_temp` (float/int)
    - `condition` (str)

9. **Settings Page**
- URL Path: `/settings`
- Methods: GET, POST (POST to save updated settings)
- Function Name: `settings`
- Template: `settings.html`
- Context Variables:
  - `temperature_unit` (str): "Celsius", "Fahrenheit", or "Kelvin"
  - `default_location_id` (int)
  - `locations` (list of dicts), each dict:
    - `location_id` (int)
    - `location_name` (str)
  - `alert_notifications_enabled` (bool)


---

## Section 2: Frontend HTML Templates Specification

1. **dashboard.html**
- File Path: `templates/dashboard.html`
- Page Title: "Weather Dashboard"
- Element IDs:
  - `dashboard-page` (div): Container for dashboard page
  - `current-weather-summary` (div): Displays current weather summary for default location
  - `search-location-button` (button): Navigate to `location_search` route
  - `view-forecast-button` (button): Navigate to `weekly_forecast` route
  - `view-alerts-button` (button): Navigate to `weather_alerts` route
- Navigation:
  - `search-location-button`: url_for('location_search')
  - `view-forecast-button`: url_for('weekly_forecast')
  - `view-alerts-button`: url_for('weather_alerts')
- Context Variables:
  - `default_location` (dict)
- Usage:
  - Display default_location weather in `current-weather-summary`.

2. **current_weather.html**
- File Path: `templates/current_weather.html`
- Page Title: "Current Weather"
- Element IDs:
  - `current-weather-page` (div): Container for current weather page
  - `location-name` (h1): Shows the location name
  - `temperature-display` (div): Shows temperature
  - `weather-condition` (div): Shows weather condition
  - `humidity-info` (div): Shows humidity percentage
  - `wind-speed-info` (div): Shows wind speed
- Navigation:
  - None specified (navigation likely via header or dashboard)
- Context Variables:
  - `location` (dict)
  - `temperature` (float/int)
  - `condition` (str)
  - `humidity` (int)
  - `wind_speed` (float/int)
- Usage:
  - Populate each element with current weather data for selected location.

3. **weekly_forecast.html**
- File Path: `templates/weekly_forecast.html`
- Page Title: "Weekly Forecast"
- Element IDs:
  - `forecast-page` (div): Container for the forecast page
  - `forecast-table` (table): Table displaying daily forecasts (columns: date, high temp, low temp, condition)
  - `location-filter` (dropdown/select): To filter forecast by location
  - `forecast-list` (div): Grid showing forecast cards for 7 days
  - `back-to-dashboard` (button): Navigate back to `dashboard`
- Navigation:
  - `back-to-dashboard`: url_for('dashboard')
- Context Variables:
  - `locations` (list of dicts)
  - `selected_location_id` (int)
  - `forecasts` (list of dicts)
- Usage:
  - Use `location-filter` dropdown to select location
  - Render `forecasts` in `forecast-list` and `forecast-table`

4. **location_search.html**
- File Path: `templates/location_search.html`
- Page Title: "Search Locations"
- Element IDs:
  - `search-page` (div): Container for search page
  - `location-search-input` (input): Input for search queries
  - `search-results` (div): List container for search results
  - `select-location-button-{location_id}` (button): Button for each location in results, pattern with location_id
  - `saved-locations-list` (div): Container listing saved locations
- Navigation:
  - `select-location-button-{location_id}` triggers POST or GET to select location
- Context Variables:
  - `search_results` (list of dicts)
  - `saved_locations` (list of dicts)
- Usage:
  - Loop over `search_results` to display locations and each with `select-location-button-{location_id}`
  - Display previously saved locations in `saved-locations-list`

5. **weather_alerts.html**
- File Path: `templates/weather_alerts.html`
- Page Title: "Weather Alerts"
- Element IDs:
  - `alerts-page` (div): Container for alerts page
  - `alerts-list` (div): Display active alerts
  - `severity-filter` (dropdown): Filter alerts by severity
  - `location-filter-alerts` (dropdown): Filter alerts by location
  - `acknowledge-alert-button-{alert_id}` (button): Button to acknowledge each alert, dynamic pattern
- Navigation:
  - Filtering triggers page reload with query params
- Context Variables:
  - `alerts` (list of dicts)
  - `severity_levels` (list of str)
  - `locations` (list of dicts)
- Usage:
  - Loop over `alerts`, render data, each with acknowledge button

6. **air_quality.html**
- File Path: `templates/air_quality.html`
- Page Title: "Air Quality Index"
- Element IDs:
  - `air-quality-page` (div): Container
  - `aqi-display` (div): Air quality index value
  - `aqi-description` (div): Text description of air quality
  - `pollution-details` (table): Table showing pm25, pm10, no2, o3 values
  - `location-aqi-filter` (dropdown): Filter by location
  - `health-recommendation` (div): Health advice based on air quality
- Navigation:
  - Selection of location reloads page with selected location data
- Context Variables:
  - `locations` (list of dicts)
  - `selected_location_id` (int)
  - `air_quality` (dict)
  - `health_recommendation` (str)
- Usage:
  - Render air quality data for selected location

7. **saved_locations.html**
- File Path: `templates/saved_locations.html`
- Page Title: "Saved Locations"
- Element IDs:
  - `saved-locations-page` (div): Container
  - `locations-table` (table): Lists saved locations with current temperature and condition
  - `view-location-weather-{location_id}` (button): Button to view weather, dynamic pattern
  - `remove-location-button-{location_id}` (button): Button to remove saved location, dynamic pattern
  - `add-new-location-button` (button): Button to add a new location
- Navigation:
  - `view-location-weather-{location_id}` navigates to `current_weather` with location_id
  - `remove-location-button-{location_id}` triggers location removal
  - `add-new-location-button` navigates to `location_search`
- Context Variables:
  - `saved_locations` (list of dicts)
- Usage:
  - Loop and render rows for each saved location with buttons

8. **settings.html**
- File Path: `templates/settings.html`
- Page Title: "Settings"
- Element IDs:
  - `settings-page` (div): Container
  - `temperature-unit-select` (dropdown): Select temperature unit
  - `default-location-select` (dropdown): Select default location
  - `alert-notifications-toggle` (checkbox): Toggle alerts
  - `save-settings-button` (button): Save changes
  - `back-to-dashboard` (button): Navigate back to `dashboard`
- Navigation:
  - `back-to-dashboard` uses url_for('dashboard')
- Context Variables:
  - `temperature_unit` (str)
  - `default_location_id` (int)
  - `locations` (list of dicts)
  - `alert_notifications_enabled` (bool)
- Usage:
  - On page load, populate selects and toggle

---

## Section 3: Data File Schemas

1. **current_weather.txt**
- File Path: `data/current_weather.txt`
- Field Order (pipe-delimited):
  - `location_id` (int): Unique ID of location
  - `location_name` (str): Name of location
  - `temperature` (int/float): Current temperature
  - `condition` (str): Current weather condition (e.g., Sunny, Rainy)
  - `humidity` (int): Humidity percentage
  - `wind_speed` (int/float): Wind speed
  - `last_updated` (str): Timestamp "YYYY-MM-DD HH:MM"
- Purpose: Stores current weather conditions for multiple locations
- Examples:
  ```
  1|New York|72|Sunny|65|10|2025-01-20 14:30
  2|London|55|Rainy|80|15|2025-01-20 14:30
  3|Tokyo|45|Cloudy|72|8|2025-01-20 14:30
  ```

2. **forecasts.txt**
- File Path: `data/forecasts.txt`
- Field Order (pipe-delimited):
  - `forecast_id` (int): Unique forecast ID
  - `location_id` (int): Location unique ID
  - `date` (str): Date of forecast (YYYY-MM-DD)
  - `high_temp` (int/float): Highest temperature of the day
  - `low_temp` (int/float): Lowest temperature of the day
  - `condition` (str): Forecast condition
  - `precipitation` (int): Precipitation percentage
  - `humidity` (int): Humidity percentage
- Purpose: Stores daily weather forecasts for locations
- Examples:
  ```
  1|1|2025-01-21|75|60|Sunny|0|60
  2|1|2025-01-22|68|55|Cloudy|10|70
  3|2|2025-01-21|58|48|Rainy|80|85
  ```

3. **locations.txt**
- File Path: `data/locations.txt`
- Field Order (pipe-delimited):
  - `location_id` (int): Unique location ID
  - `location_name` (str): Location name
  - `latitude` (float): Latitude coordinate
  - `longitude` (float): Longitude coordinate
  - `country` (str): Country name
  - `timezone` (str): Timezone abbreviation
- Purpose: Stores geographic data for locations
- Examples:
  ```
  1|New York|40.7128|-74.0060|USA|EST
  2|London|51.5074|-0.1278|UK|GMT
  3|Tokyo|35.6762|139.6503|Japan|JST
  ```

4. **alerts.txt**
- File Path: `data/alerts.txt`
- Field Order (pipe-delimited):
  - `alert_id` (int): Unique alert ID
  - `location_id` (int): Location unique ID
  - `alert_type` (str): Type of alert
  - `severity` (str): Severity level (Critical, High, Medium, Low)
  - `description` (str): Alert description
  - `start_time` (str): Start timestamp
  - `end_time` (str): End timestamp
  - `is_acknowledged` (int): 0 or 1 indicating if alert acknowledged
- Purpose: Stores weather alerts and warnings
- Examples:
  ```
  1|1|Thunderstorm|High|Severe thunderstorm warning in effect until 8 PM|2025-01-20 14:00|2025-01-20 20:00|0
  2|2|Fog|Medium|Dense fog advisory in effect until noon tomorrow|2025-01-20 06:00|2025-01-21 12:00|0
  3|1|Wind|Medium|High wind advisory with gusts up to 45 mph|2025-01-20 15:00|2025-01-21 09:00|1
  ```

5. **air_quality.txt**
- File Path: `data/air_quality.txt`
- Field Order (pipe-delimited):
  - `aqi_id` (int): Unique air quality ID
  - `location_id` (int): Location ID
  - `aqi_index` (int): Air Quality Index value (0-500)
  - `pm25` (float): PM2.5 value
  - `pm10` (float): PM10 value
  - `no2` (float): NO2 value
  - `o3` (float): O3 value
  - `last_updated` (str): Timestamp
- Purpose: Stores air quality measurements
- Examples:
  ```
  1|1|45|12.5|35|28|55|2025-01-20 14:30
  2|2|67|22.3|48|42|78|2025-01-20 14:30
  3|3|120|68.5|95|65|110|2025-01-20 14:30
  ```

6. **saved_locations.txt**
- File Path: `data/saved_locations.txt`
- Field Order (pipe-delimited):
  - `saved_id` (int): Saved location ID
  - `user_id` (int): User ID (use fixed or dummy user since no auth)
  - `location_id` (int): Location ID
  - `location_name` (str): Name of location
  - `is_default` (int): 1 if default, 0 otherwise
- Purpose: Stores user saved locations
- Examples:
  ```
  1|1|1|New York|1
  2|1|2|London|0
  3|2|3|Tokyo|1
  ```

---

This design specification document provides comprehensive details for backend route implementation, frontend template layouts, and data file formats to ensure independent yet synchronized development of the WeatherForecast web application.