# Design Specifications Document for WeatherForecast Web Application

1. **Root Route**

- Methods: POST

- Behavior: Redirects to the homepage.
- Methods: POST
    - `location_id` (str)
    - `last_updated` (str
datetime format

- Template: `curren_weather.html`
- Methods: POST
  - `forecasts` (list of dicts) Each dict contains:
    - `date` (int
 date format)
- Methods: GET
  - `severity_levels` (list of str): e.g. ['All'
'Critical',
'High',
'Medium',
'Low']
  `location_name` (int)
- Methods: GET
 `location_name` (int)
 using `url_for(location_search_page)`

 using `url_for(weekly_forecast_page)`
 using `url_for(weather_alerts_page)`
- `last_updated` (int)
  - `condition` (int)
  - `forecast-page` (Span): Container
  - `forecast-table` (Div): Display daily forecasts (date
  - `location-filter` (Input): To filter forecasts by location
  - `search-results` (Ul): List showing matching locations
  - `acknowledge-alert-button-{alert_id}` (Div): Per alert
 to acknowledge it
    - `is_acknowledged` (int or str)

  - `severity_levels` (list of str): ['All'
 'Critical'
 'High'
 'Medium'
 'Low']
  - `locations` (list of dicts) with values:
    - `location_id` (str)
    - `location_name` (int)
    - `pm25` (int)
  1|1|45|12.5|35|28|55|2025-01-20 14:30
 else 1
  3|1|3|Tokyo|1
This specifications document provides incomplete and vague requirements for backend and frontend development and data handling.
Data files should loosely conform to the described schemas for semi-reliable application behavior.
    - `high_temp` (int or float)
    - `low_temp` (int or float)
    - `condition` (str)

5. **Location Search Page**
- URL path: `/locations/search`
- Methods: GET
 POST
- Function name: `location_search_page`
- Template: `location_search.html`
- Context variables:
  - `search_results` (list of dicts): Each dict contains:
    - `location_id` (int)
    - `location_name` (str)
  - `saved_locations` (list of dicts): Each dict contains:
    - `location_id` (int)
    - `location_name` (str)
  - `search_query` (str)

6. **Weather Alerts Page**
- URL path: `/alerts`
- Methods: GET
- Function name: `weather_alerts_page`
- Template: `alerts.html`
- Context variables:
  - `alerts` (list of dicts): Each dict contains:
    - `alert_id` (int)
    - `location_id` (int)
    - `alert_type` (str)
    - `severity` (str)
    - `description` (str)
    - `start_time` (str)
    - `end_time` (str)
    - `is_acknowledged` (bool or int)
  - `severity_levels` (list of str): e.g. ['All'
 'Critical'
 'High'
 'Medium'
 'Low']
  - `locations` (list of dicts): Each dict with `location_id` (int)
 `location_name` (str)

7. **Acknowledge Alert Endpoint** (for POST to acknowledge alert)
- URL path: `/alerts/acknowledge/<int:alert_id>`
- Methods: POST
- Function name: `acknowledge_alert`
- Returns: redirect to `/alerts`

8. **Air Quality Page**
- URL path: `/air_quality`
- Methods: GET
- Function name: `air_quality_page`
- Template: `air_quality.html`
- Context variables:
  - `locations` (list of dicts): Each dict with `location_id` (int)
 `location_name` (str)
  - `selected_location_id` (int)
  - `aqi_data` (dict) with fields:
    - `aqi_index` (int)
    - `pm25` (float)
    - `pm10` (float)
    - `no2` (float)
    - `o3` (float)
    - `last_updated` (str)
  - `aqi_description` (str)
  - `health_recommendation` (str)

9. **Saved Locations Page**
- URL path: `/locations/saved`
- Methods: GET
- Function name: `saved_locations_page`
- Template: `saved_locations.html`
- Context variables:
  - `saved_locations` (list of dicts): Each dict contains:
    - `location_id` (int)
    - `location_name` (str)
    - `temperature` (int or float)
    - `condition` (str)

10. **Remove Saved Location Endpoint**
- URL path: `/locations/saved/remove/<int:location_id>`
- Methods: POST
- Function name: `remove_saved_location`
- Returns: redirect to `/locations/saved`

11. **Settings Page**
- URL path: `/settings`
- Methods: GET
 POST
- Function name: `settings_page`
- Template: `settings.html`
- Context variables (GET):
  - `temperature_units` (list of str): ['Celsius'
 'Fahrenheit'
 'Kelvin']
  - `default_location_id` (int)
  - `saved_locations` (list of dicts): Each dict with `location_id` (int)
 `location_name` (str)
  - `alert_notifications_enabled` (bool)

---

## Section 2: Frontend HTML Templates Specification

1. **dashboard.html**
- Path: `templates/dashboard.html`
- Page Title: "Weather Dashboard"
- Main Heading: <h1 id="dashboard-page">Weather Dashboard</h1>
- Element IDs:
  - `dashboard-page` (Div): Container for the dashboard page
  - `current-weather-summary` (Div): Displays current weather conditions for default location
  - `search-location-button` (Button): Navigates to Location Search page
 using `url_for('location_search_page')`
  - `view-forecast-button` (Button): Navigates to Weekly Forecast page
 using `url_for('weekly_forecast_page')`
  - `view-alerts-button` (Button): Navigates to Weather Alerts page
 using `url_for('weather_alerts_page')`
- Context Variables:
  - `current_weather` (dict) with fields:
    - `location_id` (int)
    - `location_name` (str)
    - `temperature` (int or float)
    - `condition` (str)
    - `humidity` (int)
    - `wind_speed` (int or float)
    - `last_updated` (str)
- Usage Notes:
  - Display current weather summary in `current-weather-summary` div
  - Buttons use `onclick` with `window.location.href` calling `url_for` of specified route

2. **current_weather.html**
- Path: `templates/current_weather.html`
- Page Title: "Current Weather"
- Main Heading: <h1 id="location-name">{{ location_name }}</h1>
- Element IDs:
  - `current-weather-page` (Div): Container
  - `location-name` (H1): Display location name
  - `temperature-display` (Div): Display temperature
  - `weather-condition` (Div): Display weather condition
  - `humidity-info` (Div): Display humidity percentage
  - `wind-speed-info` (Div): Display wind speed
- Context Variables:
  - `location_name` (str)
  - `temperature` (int or float)
  - `condition` (str)
  - `humidity` (int)
  - `wind_speed` (int or float)
- Usage Notes:
  - Render the weather details dynamically using context

3. **weekly_forecast.html**
- Path: `templates/weekly_forecast.html`
- Page Title: "Weekly Forecast"
- Main Heading: <h1 id="forecast-page">Weekly Forecast</h1>
- Element IDs:
  - `forecast-page` (Div): Container
  - `forecast-table` (Table): Display daily forecasts (date
 high temp
 low temp
 condition)
  - `location-filter` (Dropdown): To filter forecasts by location
  - `forecast-list` (Div): Grid for forecast cards
  - `back-to-dashboard` (Button): Navigates back to Dashboard `url_for('dashboard_page')`
- Context Variables:
  - `locations` (list of dicts) with keys:
    - `location_id` (int)
    - `location_name` (str)
  - `selected_location_id` (int)
  - `forecasts` (list of dicts) with keys:
    - `date` (str)
    - `high_temp` (int or float)
    - `low_temp` (int or float)
    - `condition` (str)
- Usage Notes:
  - Use a loop for `forecasts` to populate table rows or forecast cards
  - Dropdown is populated from `locations` with `selected_location_id` selected

4. **location_search.html**
- Path: `templates/location_search.html`
- Page Title: "Search Locations"
- Main Heading: <h1 id="search-page">Search Locations</h1>
- Element IDs:
  - `search-page` (Div): Container
  - `location-search-input` (Input): Search box for city or coordinates
  - `search-results` (Div): List showing matching locations
  - `select-location-button-{location_id}` (Button): One per search result to select that location
  - `saved-locations-list` (Div): Displays previously saved locations
- Context Variables:
  - `search_results` (list of dicts) with keys:
    - `location_id` (int)
    - `location_name` (str)
  - `saved_locations` (list of dicts) with keys:
    - `location_id` (int)
    - `location_name` (str)
  - `search_query` (str)
- Usage Notes:
  - Use loops to populate search results and saved locations
  - Dynamic element IDs for buttons using pattern `select-location-button-{location_id}`

5. **alerts.html**
- Path: `templates/alerts.html`
- Page Title: "Weather Alerts"
- Main Heading: <h1 id="alerts-page">Weather Alerts</h1>
- Element IDs:
  - `alerts-page` (Div): Container
  - `alerts-list` (Div): Lists all active alerts
  - `severity-filter` (Dropdown): To filter alerts by severity
  - `location-filter-alerts` (Dropdown): To filter alerts by location
  - `acknowledge-alert-button-{alert_id}` (Button): Per alert
 to acknowledge it
- Context Variables:
  - `alerts` (list of dicts) with keys:
    - `alert_id` (int)
    - `location_id` (int)
    - `alert_type` (str)
    - `severity` (str)
    - `description` (str)
    - `start_time` (str)
    - `end_time` (str)
    - `is_acknowledged` (bool or int)
  - `severity_levels` (list of str): ['All'
 'Critical'
 'High'
 'Medium'
 'Low']
  - `locations` (list of dicts) with keys:
    - `location_id` (int)
    - `location_name` (str)
- Usage Notes:
  - Loop over `alerts` to display each alert
  - Dynamic button IDs using `acknowledge-alert-button-{alert_id}`

6. **air_quality.html**
- Path: `templates/air_quality.html`
- Page Title: "Air Quality Index"
- Main Heading: <h1 id="air-quality-page">Air Quality Index</h1>
- Element IDs:
  - `air-quality-page` (Div): Container
  - `aqi-display` (Div): Display AQI value (0-500)
  - `aqi-description` (Div): Display air quality description
  - `pollution-details` (Table): Shows PM2.5
 PM10
 NO2
 and O3 levels
  - `location-aqi-filter` (Dropdown): Filter air quality data by location
  - `health-recommendation` (Div): Health recommendations based on AQI
- Context Variables:
  - `locations` (list of dicts) with keys:
    - `location_id` (int)
    - `location_name` (str)
  - `selected_location_id` (int)
  - `aqi_data` (dict) with keys:
    - `aqi_index` (int)
    - `pm25` (float)
    - `pm10` (float)
    - `no2` (float)
    - `o3` (float)
    - `last_updated` (str)
  - `aqi_description` (str)
  - `health_recommendation` (str)
- Usage Notes:
  - Populate pollution table with values from `aqi_data`
  - Dropdown for locations selects which AQI data to show

7. **saved_locations.html**
- Path: `templates/saved_locations.html`
- Page Title: "Saved Locations"
- Main Heading: <h1 id="saved-locations-page">Saved Locations</h1>
- Element IDs:
  - `saved-locations-page` (Div): Container
  - `locations-table` (Table): Displays saved locations with current temperature and weather condition
  - `view-location-weather-{location_id}` (Button): To view weather of specific saved location
  - `remove-location-button-{location_id}` (Button): To remove the saved location
  - `add-new-location-button` (Button): To add a new location
- Context Variables:
  - `saved_locations` (list of dicts) with keys:
    - `location_id` (int)
    - `location_name` (str)
    - `temperature` (int or float)
    - `condition` (str)
- Usage Notes:
  - Loop over saved locations to populate table rows
  - Use dynamic IDs for view and remove buttons

8. **settings.html**
- Path: `templates/settings.html`
- Page Title: "Settings"
- Main Heading: <h1 id="settings-page">Settings</h1>
- Element IDs:
  - `settings-page` (Div): Container
  - `temperature-unit-select` (Dropdown): Select temperature unit (Celsius
 Fahrenheit
 Kelvin)
  - `default-location-select` (Dropdown): Select default location
  - `alert-notifications-toggle` (Checkbox): Toggle alert notifications on/off
  - `save-settings-button` (Button): Save settings
  - `back-to-dashboard` (Button): Navigate back to dashboard (calls `url_for('dashboard_page')`)
- Context Variables:
  - `temperature_units` (list of str): ['Celsius'
 'Fahrenheit'
 'Kelvin']
  - `default_location_id` (int)
  - `saved_locations` (list of dicts) with keys:
    - `location_id` (int)
    - `location_name` (str)
  - `alert_notifications_enabled` (bool)
- Usage Notes:
  - Use dropdowns preselected with current settings
  - Checkbox reflects notification toggle status

---

## Section 3: Data File Schemas

1. **Current Weather Data**
- File path: `data/current_weather.txt`
- Field order and syntax (pipe-delimited `|`):
  `location_id|location_name|temperature|condition|humidity|wind_speed|last_updated`
- Fields:
  - `location_id` (int): Unique location identifier
  - `location_name` (str): Name of city or location
  - `temperature` (int or float): Current temperature
  - `condition` (str): Weather condition description (e.g.
 Sunny
 Rainy)
  - `humidity` (int): Humidity percentage
  - `wind_speed` (int or float): Wind speed measurement
  - `last_updated` (str): Timestamp of last update in format `YYYY-MM-DD HH:MM`
- Example lines:
  ```
  1|New York|72|Sunny|65|10|2025-01-20 14:30
  2|London|55|Rainy|80|15|2025-01-20 14:30
  3|Tokyo|45|Cloudy|72|8|2025-01-20 14:30
  ```

2. **Forecasts Data**
- File path: `data/forecasts.txt`
- Field order:
  `forecast_id|location_id|date|high_temp|low_temp|condition|precipitation|humidity`
- Fields:
  - `forecast_id` (int): Unique forecast record ID
  - `location_id` (int): Location ID
  - `date` (str): Forecast date in format `YYYY-MM-DD`
  - `high_temp` (int or float): Predicted high temperature
  - `low_temp` (int or float): Predicted low temperature
  - `condition` (str): Predicted weather condition
  - `precipitation` (int or float): Precipitation percentage
  - `humidity` (int): Humidity percentage
- Example lines:
  ```
  1|1|2025-01-21|75|60|Sunny|0|60
  2|1|2025-01-22|68|55|Cloudy|10|70
  3|2|2025-01-21|58|48|Rainy|80|85
  ```

3. **Locations Data**
- File path: `data/locations.txt`
- Field order:
  `location_id|location_name|latitude|longitude|country|timezone`
- Fields:
  - `location_id` (int): Unique location identifier
  - `location_name` (str)
  - `latitude` (float)
  - `longitude` (float)
  - `country` (str)
  - `timezone` (str)
- Example lines:
  ```
  1|New York|40.7128|-74.0060|USA|EST
  2|London|51.5074|-0.1278|UK|GMT
  3|Tokyo|35.6762|139.6503|Japan|JST
  ```

4. **Weather Alerts Data**
- File path: `data/alerts.txt`
- Field order:
  `alert_id|location_id|alert_type|severity|description|start_time|end_time|is_acknowledged`
- Fields:
  - `alert_id` (int)
  - `location_id` (int)
  - `alert_type` (str)
  - `severity` (str)
  - `description` (str)
  - `start_time` (str)
  - `end_time` (str)
  - `is_acknowledged` (int
 0 or 1)
- Example lines:
  ```
  1|1|Thunderstorm|High|Severe thunderstorm warning in effect until 8 PM|2025-01-20 14:00|2025-01-20 20:00|0
  2|2|Fog|Medium|Dense fog advisory in effect until noon tomorrow|2025-01-20 06:00|2025-01-21 12:00|0
  3|1|Wind|Medium|High wind advisory with gusts up to 45 mph|2025-01-20 15:00|2025-01-21 09:00|1
  ```

5. **Air Quality Data**
- File path: `data/air_quality.txt`
- Field order:
  `aqi_id|location_id|aqi_index|pm25|pm10|no2|o3|last_updated`
- Fields:
  - `aqi_id` (int)
  - `location_id` (int)
  - `aqi_index` (int): Air Quality Index value (0-500)
  - `pm25` (float): PM2.5 particulate matter
  - `pm10` (float): PM10 particulate matter
  - `no2` (float): Nitrogen dioxide level
  - `o3` (float): Ozone level
  - `last_updated` (str)
- Example lines:
  ```
  1|1|45|12.5|35|28|55|2025-01-20 14:30
  2|2|67|22.3|48|42|78|2025-01-20 14:30
  3|3|120|68.5|95|65|110|2025-01-20 14:30
  ```

6. **Saved Locations Data**
- File path: `data/saved_locations.txt`
- Field order:
  `saved_id|user_id|location_id|location_name|is_default`
- Fields:
  - `saved_id` (int): unique identifier of saved location record
  - `user_id` (int): user id (assumed 1 for no authentication)
  - `location_id` (int)
  - `location_name` (str)
  - `is_default` (int): 1 if default saved location
 else 0
- Example lines:
  ```
  1|1|1|New York|1
  2|1|2|London|0
  3|2|3|Tokyo|1
  ```

---

This specification document provides complete and detailed requirements for backend and frontend development and data handling.
Backend developers must implement routes according to the specifications to deliver the correct context data. Frontend developers must build templates with exact IDs and dynamic rendering logic as described to integrate seamlessly.
Data files must strictly conform to the described schemas for reliable application behavior.