# Design Specification Document for WeatherForecast Web Application

---

## Section 1: Flask Routes Specification

### 1. Root Route
- URL Path: `/`
- HTTP Methods: `GET`
- Function Name: `root_redirect`
- Template Rendered: None (Redirect)
- Behavior: Redirect to dashboard page using `url_for('dashboard')`
- Context Variables: None

---

### 2. Dashboard Page
- URL Path: `/dashboard`
- HTTP Methods: `GET`
- Function Name: `dashboard`
- Template Filename: `dashboard.html`
- Context Variables:
  - `current_weather`: dict with fields:
    - `location_id` (int)
    - `location_name` (str)
    - `temperature` (int or float)
    - `condition` (str)
    - `humidity` (int)
    - `wind_speed` (int or float)
    - `last_updated` (str, datetime in format 'YYYY-MM-DD HH:mm')

---

### 3. Current Weather Page
- URL Path: `/weather/current/<int:location_id>`
- HTTP Methods: `GET`
- Function Name: `current_weather`
- Template Filename: `current_weather.html`
- Context Variables:
  - `location_name` (str)
  - `temperature` (int or float)
  - `condition` (str)
  - `humidity` (int)
  - `wind_speed` (int or float)

---

### 4. Weekly Forecast Page
- URL Path: `/forecast/weekly`
- HTTP Methods: `GET, POST`
- Function Name: `weekly_forecast`
- Template Filename: `weekly_forecast.html`
- Context Variables:
  - `locations`: list of dicts, each dict with fields:
    - `location_id` (int)
    - `location_name` (str)
  - `selected_location_id` (int) - selected location for filtering (None if not selected)
  - `forecasts`: list of dicts, each dict with fields:
    - `date` (str, format YYYY-MM-DD)
    - `high_temp` (int or float)
    - `low_temp` (int or float)
    - `condition` (str)

---

### 5. Location Search Page
- URL Path: `/locations/search`
- HTTP Methods: `GET, POST`
- Function Name: `location_search`
- Template Filename: `location_search.html`
- Context Variables:
  - `search_query` (str) - current search input value
  - `search_results`: list of dicts, each dict with fields:
    - `location_id` (int)
    - `location_name` (str)
    - `latitude` (float)
    - `longitude` (float)
    - `country` (str)
  - `saved_locations`: list of dicts, each dict with fields:
    - `location_id` (int)
    - `location_name` (str)

---

### 6. Weather Alerts Page
- URL Path: `/alerts`
- HTTP Methods: `GET, POST`
- Function Name: `weather_alerts`
- Template Filename: `alerts.html`
- Context Variables:
  - `alerts`: list of dicts, each dict with fields:
    - `alert_id` (int)
    - `location_id` (int)
    - `alert_type` (str)
    - `severity` (str) - one of 'Critical', 'High', 'Medium', 'Low'
    - `description` (str)
    - `start_time` (str, format 'YYYY-MM-DD HH:mm')
    - `end_time` (str, format 'YYYY-MM-DD HH:mm')
    - `is_acknowledged` (bool)
    - `location_name` (str)
  - `severity_filter` (str) - current filter selected (All, Critical, High, Medium, Low)
  - `location_filter` (int or None) - selected location_id or None

---

### 7. Air Quality Page
- URL Path: `/airquality`
- HTTP Methods: `GET, POST`
- Function Name: `air_quality`
- Template Filename: `air_quality.html`
- Context Variables:
  - `locations`: list of dicts, each dict with fields:
    - `location_id` (int)
    - `location_name` (str)
  - `selected_location_id` (int or None)
  - `aqi_data`: dict with fields:
    - `aqi_index` (int)
    - `aqi_description` (str)
    - `pm25` (float)
    - `pm10` (float)
    - `no2` (float)
    - `o3` (float)
    - `last_updated` (str, format 'YYYY-MM-DD HH:mm')
  - `health_recommendation` (str)

---

### 8. Saved Locations Page
- URL Path: `/locations/saved`
- HTTP Methods: `GET, POST`
- Function Name: `saved_locations`
- Template Filename: `saved_locations.html`
- Context Variables:
  - `saved_locations`: list of dicts, each dict with fields:
    - `location_id` (int)
    - `location_name` (str)
    - `current_temperature` (int or float)
    - `condition` (str)
    - `is_default` (bool)

---

### 9. Settings Page
- URL Path: `/settings`
- HTTP Methods: `GET, POST`
- Function Name: `settings`
- Template Filename: `settings.html`
- Context Variables:
  - `temperature_units`: list of str [`Celsius`, `Fahrenheit`, `Kelvin`]
  - `selected_unit` (str)
  - `saved_locations`: list of dicts with fields:
    - `location_id` (int)
    - `location_name` (str)
  - `default_location_id` (int or None)
  - `alert_notifications_enabled` (bool)

---

## Section 2: Frontend HTML Templates Specification

### 1. templates/dashboard.html
- Page Title: "Weather Dashboard"
- Main Heading (<h1>): "Weather Dashboard"
- Element IDs:
  - `dashboard-page` (div): Container div for dashboard page
  - `current-weather-summary` (div): Displays current weather summary for default location
  - `search-location-button` (button): Navigates to location search page
  - `view-forecast-button` (button): Navigates to weekly forecast page
  - `view-alerts-button` (button): Navigates to weather alerts page
- Navigation Links (Buttons) using Flask function names and url_for:
  - `search-location-button`: `url_for('location_search')`
  - `view-forecast-button`: `url_for('weekly_forecast')`
  - `view-alerts-button`: `url_for('weather_alerts')`
- Context Variables:
  - `current_weather` (dict as specified in Routes section)
- Usage Notes:
  - Display summary info inside `current-weather-summary` using `current_weather` keys

---

### 2. templates/current_weather.html
- Page Title: "Current Weather"
- Main Heading (<h1>): Display `location_name`
- Element IDs:
  - `current-weather-page` (div): Container div
  - `location-name` (h1): Displays name of location
  - `temperature-display` (div): Shows current temperature
  - `weather-condition` (div): Shows weather condition
  - `humidity-info` (div): Displays humidity percentage
  - `wind-speed-info` (div): Displays wind speed
- Navigation:
  - No navigation elements mandated in design.
- Context Variables:
  - `location_name` (str)
  - `temperature` (int or float)
  - `condition` (str)
  - `humidity` (int)
  - `wind_speed` (int or float)
- Usage Notes:
  - Data populated directly into respective element IDs

---

### 3. templates/weekly_forecast.html
- Page Title: "Weekly Forecast"
- Main Heading (<h1>): "Weekly Forecast"
- Element IDs:
  - `forecast-page` (div): Container div
  - `forecast-table` (table): Table showing forecast data
  - `location-filter` (dropdown/select): Select location to filter forecasts
  - `forecast-list` (div): Grid/section with daily forecast cards
  - `back-to-dashboard` (button): Button to navigate back to dashboard
- Navigation:
  - `back-to-dashboard`: `url_for('dashboard')`
- Context Variables:
  - `locations`: list of dicts `{location_id: int, location_name: str}`
  - `selected_location_id`: int or null
  - `forecasts`: list of dicts `{date: str, high_temp: float, low_temp: float, condition: str}`
- Usage Notes:
  - `location-filter` is populated with locations; selection posts back or filters forecasts
  - `forecast-list` or `forecast-table` lists all 7 day forecasts

---

### 4. templates/location_search.html
- Page Title: "Search Locations"
- Main Heading (<h1>): "Search Locations"
- Element IDs:
  - `search-page` (div): Container
  - `location-search-input` (input): Text input for location search
  - `search-results` (div): Container for search results
  - `select-location-button-{location_id}` (button): Buttons for each search result
  - `saved-locations-list` (div): Display saved locations
- Navigation:
  - Buttons `select-location-button-{location_id}` trigger selection actions (POST or JS)
- Context Variables:
  - `search_query` (str)
  - `search_results`: list of dicts `{location_id: int, location_name: str, latitude: float, longitude: float, country: str}`
  - `saved_locations`: list of dicts `{location_id: int, location_name: str}`
- Usage Notes:
  - `search-results` displayed by looping over `search_results`
  - Each result has a unique `select-location-button-{location_id}` for selection
  - `saved-locations-list` shows previously saved locations

---

### 5. templates/alerts.html
- Page Title: "Weather Alerts"
- Main Heading (<h1>): "Weather Alerts"
- Element IDs:
  - `alerts-page` (div): Container of alerts page
  - `alerts-list` (div): List container for active alerts
  - `severity-filter` (dropdown): Filter alerts by severity
  - `location-filter-alerts` (dropdown): Filter alerts by location
  - `acknowledge-alert-button-{alert_id}` (button): Buttons to acknowledge alerts
- Navigation:
  - Filtering selects trigger POST or AJAX request to reload with filters
- Context Variables:
  - `alerts`: list of dicts:
    - `alert_id` (int)
    - `location_id` (int)
    - `alert_type` (str)
    - `severity` (str)
    - `description` (str)
    - `start_time` (str)
    - `end_time` (str)
    - `is_acknowledged` (bool)
    - `location_name` (str)
  - `severity_filter` (str)
  - `location_filter` (int or None)
- Usage Notes:
  - Each alert entry includes an acknowledge button with ID `acknowledge-alert-button-{alert_id}`

---

### 6. templates/air_quality.html
- Page Title: "Air Quality Index"
- Main Heading (<h1>): "Air Quality Index"
- Element IDs:
  - `air-quality-page` (div): Container
  - `aqi-display` (div): Shows air quality index value
  - `aqi-description` (div): Shows air quality textual description
  - `pollution-details` (table): Table of pollutants (PM2.5, PM10, NO2, O3)
  - `location-aqi-filter` (dropdown): Select location to filter AQI
  - `health-recommendation` (div): Text with health advice
- Navigation:
  - Changing `location-aqi-filter` triggers GET or POST for selected location
- Context Variables:
  - `locations`: list of dicts `{location_id: int, location_name: str}`
  - `selected_location_id`: int or None
  - `aqi_data`: dict with keys `aqi_index` (int), `aqi_description` (str), `pm25` (float), `pm10` (float), `no2` (float), `o3` (float), `last_updated` (str)
  - `health_recommendation` (str)
- Usage Notes:
  - Display pollutant values in `pollution-details` table rows

---

### 7. templates/saved_locations.html
- Page Title: "Saved Locations"
- Main Heading (<h1>): "Saved Locations"
- Element IDs:
  - `saved-locations-page` (div): Container
  - `locations-table` (table): Table showing saved locations with current temperature and weather
  - `view-location-weather-{location_id}` (button): View weather button for each location
  - `remove-location-button-{location_id}` (button): Remove saved location button
  - `add-new-location-button` (button): Button to add a new location
- Navigation:
  - `view-location-weather-{location_id}`: link to `url_for('current_weather', location_id=location_id)`
  - `remove-location-button-{location_id}` triggers removal action
  - `add-new-location-button`: `url_for('location_search')`
- Context Variables:
  - `saved_locations`: list of dicts `{location_id: int, location_name: str, current_temperature: float, condition: str, is_default: bool}`
- Usage Notes:
  - Loop over `saved_locations` to populate table rows with buttons having dynamic IDs

---

### 8. templates/settings.html
- Page Title: "Settings"
- Main Heading (<h1>): "Settings"
- Element IDs:
  - `settings-page` (div): Container
  - `temperature-unit-select` (dropdown): Select temperature unit
  - `default-location-select` (dropdown): Select default location
  - `alert-notifications-toggle` (checkbox): Enable or disable alert notifications
  - `save-settings-button` (button): Save changes
  - `back-to-dashboard` (button): Navigate back to dashboard
- Navigation:
  - `back-to-dashboard`: `url_for('dashboard')`
- Context Variables:
  - `temperature_units`: list[str]
  - `selected_unit`: str
  - `saved_locations`: list of dicts `{location_id: int, location_name: str}`
  - `default_location_id`: int or None
  - `alert_notifications_enabled`: bool
- Usage Notes:
  - Populate dropdowns with provided lists
  - Checkbox reflects current notification setting

---

## Section 3: Data File Schemas

### 1. Current Weather Data
- File: `data/current_weather.txt`
- Format (pipe-delimited):
  ```
  location_id|location_name|temperature|condition|humidity|wind_speed|last_updated
  ```
- Fields:
  - `location_id` (int): Unique ID of location
  - `location_name` (str): Name of location (city)
  - `temperature` (int or float): Current temperature
  - `condition` (str): Weather condition (Sunny, Rainy, etc.)
  - `humidity` (int): Humidity percentage
  - `wind_speed` (int or float): Wind speed
  - `last_updated` (str): Last update time in `YYYY-MM-DD HH:mm` format
- Example:
  ```
  1|New York|72|Sunny|65|10|2025-01-20 14:30
  2|London|55|Rainy|80|15|2025-01-20 14:30
  3|Tokyo|45|Cloudy|72|8|2025-01-20 14:30
  ```

---

### 2. Forecasts Data
- File: `data/forecasts.txt`
- Format:
  ```
  forecast_id|location_id|date|high_temp|low_temp|condition|precipitation|humidity
  ```
- Fields:
  - `forecast_id` (int): Unique forecast entry ID
  - `location_id` (int)
  - `date` (str): Date of forecast in `YYYY-MM-DD`
  - `high_temp` (int or float): High temperature
  - `low_temp` (int or float): Low temperature
  - `condition` (str): Weather condition
  - `precipitation` (int): Percentage precipitation chance
  - `humidity` (int): Humidity percentage
- Example:
  ```
  1|1|2025-01-21|75|60|Sunny|0|60
  2|1|2025-01-22|68|55|Cloudy|10|70
  3|2|2025-01-21|58|48|Rainy|80|85
  ```

---

### 3. Locations Data
- File: `data/locations.txt`
- Format:
  ```
  location_id|location_name|latitude|longitude|country|timezone
  ```
- Fields:
  - `location_id` (int)
  - `location_name` (str)
  - `latitude` (float)
  - `longitude` (float)
  - `country` (str)
  - `timezone` (str)
- Example:
  ```
  1|New York|40.7128|-74.0060|USA|EST
  2|London|51.5074|-0.1278|UK|GMT
  3|Tokyo|35.6762|139.6503|Japan|JST
  ```

---

### 4. Weather Alerts Data
- File: `data/alerts.txt`
- Format:
  ```
  alert_id|location_id|alert_type|severity|description|start_time|end_time|is_acknowledged
  ```
- Fields:
  - `alert_id` (int)
  - `location_id` (int)
  - `alert_type` (str)
  - `severity` (str): One of `Critical`, `High`, `Medium`, `Low`
  - `description` (str)
  - `start_time` (str): Format `YYYY-MM-DD HH:mm`
  - `end_time` (str): Format `YYYY-MM-DD HH:mm`
  - `is_acknowledged` (int): 0 (False) or 1 (True)
- Example:
  ```
  1|1|Thunderstorm|High|Severe thunderstorm warning in effect until 8 PM|2025-01-20 14:00|2025-01-20 20:00|0
  2|2|Fog|Medium|Dense fog advisory in effect until noon tomorrow|2025-01-20 06:00|2025-01-21 12:00|0
  3|1|Wind|Medium|High wind advisory with gusts up to 45 mph|2025-01-20 15:00|2025-01-21 09:00|1
  ```

---

### 5. Air Quality Data
- File: `data/air_quality.txt`
- Format:
  ```
  aqi_id|location_id|aqi_index|pm25|pm10|no2|o3|last_updated
  ```
- Fields:
  - `aqi_id` (int)
  - `location_id` (int)
  - `aqi_index` (int): Air Quality Index value (0-500)
  - `pm25` (float): Particulate Matter 2.5 concentration
  - `pm10` (float): Particulate Matter 10 concentration
  - `no2` (float): Nitrogen Dioxide concentration
  - `o3` (float): Ozone concentration
  - `last_updated` (str): DateTime string `YYYY-MM-DD HH:mm`
- Example:
  ```
  1|1|45|12.5|35|28|55|2025-01-20 14:30
  2|2|67|22.3|48|42|78|2025-01-20 14:30
  3|3|120|68.5|95|65|110|2025-01-20 14:30
  ```

---

### 6. Saved Locations Data
- File: `data/saved_locations.txt`
- Format:
  ```
  saved_id|user_id|location_id|location_name|is_default
  ```
- Fields:
  - `saved_id` (int)
  - `user_id` (int) - Note: app does not require separate user auth, user_id can be fixed to 1 if needed
  - `location_id` (int)
  - `location_name` (str)
  - `is_default` (int): 0 or 1 to mark default location
- Example:
  ```
  1|1|1|New York|1
  2|1|2|London|0
  3|2|3|Tokyo|1
  ```

---

# End of Design Specification
