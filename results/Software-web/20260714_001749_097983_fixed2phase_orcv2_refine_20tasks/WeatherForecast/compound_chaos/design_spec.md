# WeatherForecast Web Application Design Specification

---

## Section 1: Page Layouts and Element IDs

### 1. Dashboard Page
- Page Title: Weather Dashboard
- Container ID: dashboard-page (Div)
- Elements:
  - current-weather-summary (Div): Displays current weather conditions for default location
  - search-location-button (Button): Navigate to Location Search page
  - view-forecast-button (Button): Navigate to Weekly Forecast page
  - view-alerts-button (Button): Navigate to Weather Alerts page

### 2. Current Weather Page
- Page Title: Current Weather
- Container ID: current-weather-page (Div)
- Elements:
  - location-name (H1): Display location name
  - temperature-display (Div): Display current temperature
  - weather-condition (Div): Display weather condition (sunny, rainy, cloudy, etc.)
  - humidity-info (Div): Display humidity percentage
  - wind-speed-info (Div): Display wind speed

### 3. Weekly Forecast Page
- Page Title: Weekly Forecast
- Container ID: forecast-page (Div)
- Elements:
  - forecast-table (Table): Table displaying daily forecasts with date, high temp, low temp, and condition
  - location-filter (Dropdown): Dropdown to filter forecast by location
  - forecast-list (Div): Grid displaying forecast cards for each day
  - back-to-dashboard (Button): Button to navigate back to dashboard

### 4. Location Search Page
- Page Title: Search Locations
- Container ID: search-page (Div)
- Elements:
  - location-search-input (Input): Field to search locations by city name or coordinates
  - search-results (Div): List of search results displaying matching locations
  - select-location-button-{location_id} (Button): Button to select a location (each result has this)
  - saved-locations-list (Div): Display of previously saved locations

### 5. Weather Alerts Page
- Page Title: Weather Alerts
- Container ID: alerts-page (Div)
- Elements:
  - alerts-list (Div): List of all active weather alerts with severity, description, and location
  - severity-filter (Dropdown): Dropdown to filter alerts by severity (All, Critical, High, Medium, Low)
  - location-filter-alerts (Dropdown): Dropdown to filter alerts by location
  - acknowledge-alert-button-{alert_id} (Button): Button to acknowledge an alert (each alert has this)

### 6. Air Quality Page
- Page Title: Air Quality Index
- Container ID: air-quality-page (Div)
- Elements:
  - aqi-display (Div): Display air quality index value (0-500)
  - aqi-description (Div): Display air quality description (Good, Moderate, Unhealthy, etc.)
  - pollution-details (Table): Table showing PM2.5, PM10, NO2, and other pollutants
  - location-aqi-filter (Dropdown): Dropdown to filter by location
  - health-recommendation (Div): Display health recommendations based on air quality

### 7. Saved Locations Page
- Page Title: Saved Locations
- Container ID: saved-locations-page (Div)
- Elements:
  - locations-table (Table): Table displaying saved locations with current temp and weather condition
  - view-location-weather-{location_id} (Button): Button to view weather for a location (each location has this)
  - remove-location-button-{location_id} (Button): Button to remove saved location (each location has this)
  - add-new-location-button (Button): Button to add new location

### 8. Settings Page
- Page Title: Settings
- Container ID: settings-page (Div)
- Elements:
  - temperature-unit-select (Dropdown): Dropdown to select temperature unit (Celsius, Fahrenheit, Kelvin)
  - default-location-select (Dropdown): Dropdown to set default location
  - alert-notifications-toggle (Checkbox): Toggle to enable/disable alert notifications
  - save-settings-button (Button): Button to save settings changes
  - back-to-dashboard (Button): Button to navigate back to dashboard

---

## Section 2: Navigation Structure

- The app starts at the Dashboard page (dashboard-page).

- Dashboard navigation buttons:
  - search-location-button -> Location Search page
  - view-forecast-button -> Weekly Forecast page
  - view-alerts-button -> Weather Alerts page

- Weekly Forecast page:
  - back-to-dashboard button navigates back to Dashboard

- Settings page:
  - back-to-dashboard button navigates back to Dashboard

- Location Search page:
  - select-location-button-{location_id} sets the selected location and navigates to Current Weather page

- Saved Locations page:
  - view-location-weather-{location_id} navigates to Current Weather page for that location
  - remove-location-button-{location_id} removes the saved location
  - add-new-location-button navigates to Location Search page

- Weather Alerts page:
  - severity-filter and location-filter-alerts filter displayed alerts
  - acknowledge-alert-button-{alert_id} acknowledges the specific alert

- Air Quality page:
  - location-aqi-filter filters air quality data by location

- Settings page:
  - save-settings-button saves configuration changes

- Current Weather page has no explicit back button; navigation to other pages occurs via Dashboard or Saved Locations

---

## Section 3: Data Storage Formats

All data files are stored locally within a `data/` directory in pipe-delimited text formats.

### 1. Current Weather Data
- Filename: current_weather.txt
- Schema:
  `location_id|location_name|temperature|condition|humidity|wind_speed|last_updated`
- Example:
  `1|New York|72|Sunny|65|10|2025-01-20 14:30`
  `2|London|55|Rainy|80|15|2025-01-20 14:30`
  `3|Tokyo|45|Cloudy|72|8|2025-01-20 14:30`

### 2. Forecasts Data
- Filename: forecasts.txt
- Schema:
  `forecast_id|location_id|date|high_temp|low_temp|condition|precipitation|humidity`
- Example:
  `1|1|2025-01-21|75|60|Sunny|0|60`
  `2|1|2025-01-22|68|55|Cloudy|10|70`
  `3|2|2025-01-21|58|48|Rainy|80|85`

### 3. Locations Data
- Filename: locations.txt
- Schema:
  `location_id|location_name|latitude|longitude|country|timezone`
- Example:
  `1|New York|40.7128|-74.0060|USA|EST`
  `2|London|51.5074|-0.1278|UK|GMT`
  `3|Tokyo|35.6762|139.6503|Japan|JST`

### 4. Weather Alerts Data
- Filename: alerts.txt
- Schema:
  `alert_id|location_id|alert_type|severity|description|start_time|end_time|is_acknowledged`
- Example:
  `1|1|Thunderstorm|High|Severe thunderstorm warning in effect until 8 PM|2025-01-20 14:00|2025-01-20 20:00|0`
  `2|2|Fog|Medium|Dense fog advisory in effect until noon tomorrow|2025-01-20 06:00|2025-01-21 12:00|0`
  `3|1|Wind|Medium|High wind advisory with gusts up to 45 mph|2025-01-20 15:00|2025-01-21 09:00|1`

### 5. Air Quality Data
- Filename: air_quality.txt
- Schema:
  `aqi_id|location_id|aqi_index|pm25|pm10|no2|o3|last_updated`
- Example:
  `1|1|45|12.5|35|28|55|2025-01-20 14:30`
  `2|2|67|22.3|48|42|78|2025-01-20 14:30`
  `3|3|120|68.5|95|65|110|2025-01-20 14:30`

### 6. Saved Locations Data
- Filename: saved_locations.txt
- Schema:
  `saved_id|user_id|location_id|location_name|is_default`
- Example:
  `1|1|1|New York|1`
  `2|1|2|London|0`
  `3|2|3|Tokyo|1`

---

End of Design Specification
