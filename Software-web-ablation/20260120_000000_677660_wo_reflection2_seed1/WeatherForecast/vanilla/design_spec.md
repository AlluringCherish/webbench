# Design Specification Document for WeatherForecast Web Application

---

## Section 1: Flask Routes Specification

| URL Path                       | HTTP Methods | Function Name            | Template Filename               | Context Variables (name: type)                                                                                                         |
|-------------------------------|--------------|--------------------------|-------------------------------|----------------------------------------------------------------------------------------------------------------------------------------|
| /                              | GET          | root_redirect             | None (redirects to /dashboard) | None                                                                                                                                   |
| /dashboard                    | GET          | dashboard                 | dashboard.html                 | current_weather: dict {
  location_id: int,
  location_name: str,
  temperature: float,
  condition: str,
  humidity: int,
  wind_speed: float,
  last_updated: str
}

// This is for default location display on dashboard

| /weather/current/<int:location_id> | GET          | current_weather           | current_weather.html           | location_name: str
 temperature: float
 condition: str
 humidity: int
 wind_speed: float

| /forecast/weekly               | GET          | weekly_forecast           | weekly_forecast.html           | location_id: int
 locations: list of dict {
  location_id: int,
  location_name: str
 }
 forecasts: list of dict {
  forecast_id: int,
  location_id: int,
  date: str (YYYY-MM-DD),
  high_temp: float,
  low_temp: float,
  condition: str,
  precipitation: int,
  humidity: int
 }
 selected_location_id: int

| /locations/search             | GET          | location_search           | location_search.html           | search_results: list of dict {
  location_id: int,
  location_name: str,
  latitude: float,
  longitude: float,
  country: str,
  timezone: str
 }
 saved_locations: list of dict {
  saved_id: int,
  user_id: int,
  location_id: int,
  location_name: str,
  is_default: bool
 }
 query: str (optional)

| /alerts                      | GET          | weather_alerts            | weather_alerts.html            | alerts: list of dict {
  alert_id: int,
  location_id: int,
  alert_type: str,
  severity: str,
  description: str,
  start_time: str,
  end_time: str,
  is_acknowledged: bool
 }
 locations: list of dict {
  location_id: int,
  location_name: str
 }
 selected_severity: str
 selected_location_id: int

| /airquality                  | GET          | air_quality               | air_quality.html              | air_quality_data: list of dict {
  aqi_id: int,
  location_id: int,
  aqi_index: int,
  pm25: float,
  pm10: float,
  no2: float,
  o3: float,
  last_updated: str
 }
 locations: list of dict {
  location_id: int,
  location_name: str
 }
 selected_location_id: int
 health_recommendation: str

| /locations/saved             | GET          | saved_locations           | saved_locations.html          | saved_locations: list of dict {
  saved_id: int,
  user_id: int,
  location_id: int,
  location_name: str,
  is_default: bool
 }
 current_weather: dict {
  location_id: int,
  temperature: float,
  condition: str
 }

| /settings                   | GET, POST   | settings                  | settings.html                | temperature_unit: str (one of "Celsius", "Fahrenheit", "Kelvin")
 default_location_id: int
 saved_locations: list of dict {
  saved_id: int,
  user_id: int,
  location_id: int,
  location_name: str,
  is_default: bool
 }
 alert_notifications_enabled: bool

### Notes:
- The root route '/' redirects (HTTP 302) to '/dashboard'.
- Dynamic routes clearly specify path parameters such as <int:location_id>.
- POST on /settings route to update user preferences.

---

## Section 2: Frontend HTML Templates Specification

### 1. templates/dashboard.html
- **Page Title:** Weather Dashboard
- **Element IDs:**
  - dashboard-page (Div): container div for entire page
  - current-weather-summary (Div): displays current weather summary for default location
  - search-location-button (Button): navigates to location search page
  - view-forecast-button (Button): navigates to weekly forecast page
  - view-alerts-button (Button): navigates to weather alerts page
- **Navigation Buttons (url_for):**
  - search-location-button: url_for('location_search')
  - view-forecast-button: url_for('weekly_forecast')
  - view-alerts-button: url_for('weather_alerts')
- **Context Variables:**
  - current_weather: dict containing {
      location_id: int,
      location_name: str,
      temperature: float,
      condition: str,
      humidity: int,
      wind_speed: float,
      last_updated: str
    }
- **Usage Notes:**
  - Render current_weather_summary with values such as temperature, condition, humidity, and wind speed.

### 2. templates/current_weather.html
- **Page Title:** Current Weather
- **Element IDs:**
  - current-weather-page (Div): container for page
  - location-name (H1): shows the location name
  - temperature-display (Div): current temperature
  - weather-condition (Div): condition (e.g. Sunny)
  - humidity-info (Div): humidity percentage
  - wind-speed-info (Div): wind speed
- **Navigation Buttons:** None specified
- **Context Variables:**
  - location_name: str
  - temperature: float
  - condition: str
  - humidity: int
  - wind_speed: float
- **Usage Notes:**
  - Display all detailed current weather info clearly

### 3. templates/weekly_forecast.html
- **Page Title:** Weekly Forecast
- **Element IDs:**
  - forecast-page (Div): container div for the forecast page
  - forecast-table (Table): shows forecast data
  - location-filter (Dropdown): select location to filter forecast
  - forecast-list (Div): grid with forecast cards for each day
  - back-to-dashboard (Button): navigates to dashboard
- **Navigation Buttons:**
  - back-to-dashboard: url_for('dashboard')
- **Context Variables:**
  - location_id: int (the currently selected location)
  - locations: list of dict {location_id: int, location_name: str} for dropdown
  - forecasts: list of dict {
      forecast_id: int,
      location_id: int,
      date: str (YYYY-MM-DD),
      high_temp: float,
      low_temp: float,
      condition: str,
      precipitation: int,
      humidity: int
    }
- **Usage Notes:**
  - Loop over forecasts filtered by selected location.
  - Dropdown populates from locations.

### 4. templates/location_search.html
- **Page Title:** Search Locations
- **Element IDs:**
  - search-page (Div): container div for page
  - location-search-input (Input): text input for city or coordinates
  - search-results (Div): container for search results list
  - select-location-button-{location_id} (Button): button for each search result
  - saved-locations-list (Div): list showing saved locations
- **Navigation Buttons:**
  - Buttons to select location call url_for('save_location', location_id=location_id) (assumed for backend logic)
- **Context Variables:**
  - search_results: list of dict {
      location_id: int,
      location_name: str,
      latitude: float,
      longitude: float,
      country: str,
      timezone: str
    }
  - saved_locations: list of dict {
      saved_id: int,
      user_id: int,
      location_id: int,
      location_name: str,
      is_default: bool
    }
  - query: str (optional search query)
- **Usage Notes:**
  - Render search results with buttons having IDs select-location-button-{location_id}.
  - Saved locations displayed with list.

### 5. templates/weather_alerts.html
- **Page Title:** Weather Alerts
- **Element IDs:**
  - alerts-page (Div): main container
  - alerts-list (Div): container for listing alerts
  - severity-filter (Dropdown): filter alerts by severity
  - location-filter-alerts (Dropdown): filter alerts by location
  - acknowledge-alert-button-{alert_id} (Button): button for each alert
- **Navigation Buttons:**
  - Buttons for acknowledging alerts use url_for('acknowledge_alert', alert_id=alert_id) (assumed backend function)
- **Context Variables:**
  - alerts: list of dict {
      alert_id: int,
      location_id: int,
      alert_type: str,
      severity: str,
      description: str,
      start_time: str,
      end_time: str,
      is_acknowledged: bool
    }
  - locations: list of dict {location_id: int, location_name: str} for dropdown
  - selected_severity: str
  - selected_location_id: int
- **Usage Notes:**
  - Render alerts filtered by severity and location.
  - Buttons have IDs acknowledge-alert-button-{alert_id}.

### 6. templates/air_quality.html
- **Page Title:** Air Quality Index
- **Element IDs:**
  - air-quality-page (Div): container div
  - aqi-display (Div): display AQI value (0-500)
  - aqi-description (Div): text describing AQI
  - pollution-details (Table): pollution metrics (PM2.5, PM10, NO2, O3)
  - location-aqi-filter (Dropdown): filter by location
  - health-recommendation (Div): health advice based on AQI
- **Navigation Buttons:** None specified
- **Context Variables:**
  - air_quality_data: list of dict {
      aqi_id: int,
      location_id: int,
      aqi_index: int,
      pm25: float,
      pm10: float,
      no2: float,
      o3: float,
      last_updated: str
    }
  - locations: list of dict {location_id: int, location_name: str}
  - selected_location_id: int
  - health_recommendation: str
- **Usage Notes:**
  - Display data for selected location from air_quality_data.

### 7. templates/saved_locations.html
- **Page Title:** Saved Locations
- **Element IDs:**
  - saved-locations-page (Div): container div
  - locations-table (Table): table with saved locations including current temp and condition
  - view-location-weather-{location_id} (Button): button for viewing weather
  - remove-location-button-{location_id} (Button): button for removing location
  - add-new-location-button (Button): button to add new location
- **Navigation Buttons:**
  - view-location-weather-{location_id}: url_for('current_weather', location_id=location_id)
  - remove-location-button-{location_id}: url_for('remove_saved_location', location_id=location_id) (assumed endpoint)
  - add-new-location-button: url_for('location_search')
- **Context Variables:**
  - saved_locations: list of dict {
      saved_id: int,
      user_id: int,
      location_id: int,
      location_name: str,
      is_default: bool
    }
  - current_weather: dict {
      location_id: int,
      temperature: float,
      condition: str
    }
- **Usage Notes:**
  - Loop over saved_locations to populate table rows
  - Use dynamic button IDs with location_id

### 8. templates/settings.html
- **Page Title:** Settings
- **Element IDs:**
  - settings-page (Div): container div
  - temperature-unit-select (Dropdown): select temperature unit
  - default-location-select (Dropdown): select default location
  - alert-notifications-toggle (Checkbox): toggle alert notifications
  - save-settings-button (Button): save changes
  - back-to-dashboard (Button): navigate to dashboard
- **Navigation Buttons:**
  - back-to-dashboard: url_for('dashboard')
- **Context Variables:**
  - temperature_unit: str (Celsius, Fahrenheit, Kelvin)
  - default_location_id: int
  - saved_locations: list of dict {
      saved_id: int,
      user_id: int,
      location_id: int,
      location_name: str,
      is_default: bool
    }
  - alert_notifications_enabled: bool
- **Usage Notes:**
  - Form to update user preferences with POST to /settings
  - Dropdowns populated from saved_locations

---

## Section 3: Data File Schemas

### 1. data/current_weather.txt
- Fields (pipe-delimited): location_id|location_name|temperature|condition|humidity|wind_speed|last_updated
- Descriptions:
  - location_id: int, unique identifier for location
  - location_name: str, name of location
  - temperature: float, current temperature in default unit
  - condition: str, weather condition (Sunny, Rainy, etc.)
  - humidity: int, humidity percentage
  - wind_speed: float, wind speed in mph
  - last_updated: str, timestamp in 'YYYY-MM-DD HH:MM' format
- Example Lines:
  1|New York|72|Sunny|65|10|2025-01-20 14:30
  2|London|55|Rainy|80|15|2025-01-20 14:30
  3|Tokyo|45|Cloudy|72|8|2025-01-20 14:30

### 2. data/forecasts.txt
- Fields (pipe-delimited): forecast_id|location_id|date|high_temp|low_temp|condition|precipitation|humidity
- Descriptions:
  - forecast_id: int, unique identifier for forecast
  - location_id: int, foreign key to locations
  - date: str, date of forecast YYYY-MM-DD
  - high_temp: float, high temperature
  - low_temp: float, low temperature
  - condition: str, forecast condition
  - precipitation: int, precipitation percentage
  - humidity: int, humidity percentage
- Example Lines:
  1|1|2025-01-21|75|60|Sunny|0|60
  2|1|2025-01-22|68|55|Cloudy|10|70
  3|2|2025-01-21|58|48|Rainy|80|85

### 3. data/locations.txt
- Fields (pipe-delimited): location_id|location_name|latitude|longitude|country|timezone
- Descriptions:
  - location_id: int, unique location id
  - location_name: str, city or location name
  - latitude: float, geographic latitude
  - longitude: float, geographic longitude
  - country: str, country name
  - timezone: str, timezone code
- Example Lines:
  1|New York|40.7128|-74.0060|USA|EST
  2|London|51.5074|-0.1278|UK|GMT
  3|Tokyo|35.6762|139.6503|Japan|JST

### 4. data/alerts.txt
- Fields (pipe-delimited): alert_id|location_id|alert_type|severity|description|start_time|end_time|is_acknowledged
- Descriptions:
  - alert_id: int, unique alert identifier
  - location_id: int, related location id
  - alert_type: str, type of alert
  - severity: str, alert severity (Critical, High, Medium, Low)
  - description: str, detailed alert description
  - start_time: str, timestamp start 'YYYY-MM-DD HH:MM'
  - end_time: str, timestamp end
  - is_acknowledged: int (0 or 1), whether alert is acknowledged
- Example Lines:
  1|1|Thunderstorm|High|Severe thunderstorm warning in effect until 8 PM|2025-01-20 14:00|2025-01-20 20:00|0
  2|2|Fog|Medium|Dense fog advisory in effect until noon tomorrow|2025-01-20 06:00|2025-01-21 12:00|0
  3|1|Wind|Medium|High wind advisory with gusts up to 45 mph|2025-01-20 15:00|2025-01-21 09:00|1

### 5. data/air_quality.txt
- Fields (pipe-delimited): aqi_id|location_id|aqi_index|pm25|pm10|no2|o3|last_updated
- Descriptions:
  - aqi_id: int, unique air quality record id
  - location_id: int, linked location id
  - aqi_index: int, air quality index (0-500)
  - pm25: float, PM2.5 concentration
  - pm10: float, PM10 concentration
  - no2: float, NO2 concentration
  - o3: float, O3 concentration
  - last_updated: str, timestamp 'YYYY-MM-DD HH:MM'
- Example Lines:
  1|1|45|12.5|35|28|55|2025-01-20 14:30
  2|2|67|22.3|48|42|78|2025-01-20 14:30
  3|3|120|68.5|95|65|110|2025-01-20 14:30

### 6. data/saved_locations.txt
- Fields (pipe-delimited): saved_id|user_id|location_id|location_name|is_default
- Descriptions:
  - saved_id: int, unique saved location record id
  - user_id: int, user identifier (though app has no auth, use for data grouping)
  - location_id: int
  - location_name: str
  - is_default: int (0 or 1), 1 if default location
- Example Lines:
  1|1|1|New York|1
  2|1|2|London|0
  3|2|3|Tokyo|1

---

End of Design Specification Document
