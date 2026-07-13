# WeatherForecast Web Application - Design Specification

## Section 1: Page Layouts and Element IDs

### 1. Dashboard Page
- Page Title: Weather Dashboard
- Container ID: dashboard-page (Div)
- Elements:
  - current-weather-summary (Div): Display of current weather for default location
  - search-location-button (Button): Navigate to Location Search page
  - view-forecast-button (Button): Navigate to Weekly Forecast page
  - view-alerts-button (Button): Navigate to Weather Alerts page
  - view-air-quality-button (Button): Navigate to Air Quality page
  - view-saved-locations-button (Button): Navigate to Saved Locations page
  - settings-button (Button): Navigate to Settings page

### 2. Current Weather Page
- Page Title: Current Weather
- Container ID: current-weather-page (Div)
- Elements:
  - location-name (H1): Display location name
  - temperature-display (Div): Current temperature
  - weather-condition (Div): Weather condition description
  - humidity-info (Div): Humidity percentage
  - wind-speed-info (Div): Wind speed

### 3. Weekly Forecast Page
- Page Title: Weekly Forecast
- Container ID: forecast-page (Div)
- Elements:
  - forecast-table (Table): Daily forecasts (date, high temp, low temp, condition)
  - location-filter (Dropdown): Filter forecast by location
  - forecast-list (Div): Grid showing forecast cards for each day
  - back-to-dashboard (Button): Navigate back to Dashboard

### 4. Location Search Page
- Page Title: Search Locations
- Container ID: search-page (Div)
- Elements:
  - location-search-input (Input): Search by city or coordinates
  - search-results (Div): List of matching locations
  - select-location-button-{location_id} (Button per result): Select location
  - saved-locations-list (Div): Previously saved locations

### 5. Weather Alerts Page
- Page Title: Weather Alerts
- Container ID: alerts-page (Div)
- Elements:
  - alerts-list (Div): Active weather alerts with severity, description, location
  - severity-filter (Dropdown): Filter alerts by severity
  - location-filter-alerts (Dropdown): Filter alerts by location
  - acknowledge-alert-button-{alert_id} (Button per alert): Acknowledge alert

### 6. Air Quality Page
- Page Title: Air Quality Index
- Container ID: air-quality-page (Div)
- Elements:
  - aqi-display (Div): Air quality index value (0-500)
  - aqi-description (Div): Air quality description
  - pollution-details (Table): PM2.5, PM10, NO2, O3 etc.
  - location-aqi-filter (Dropdown): Filter air quality by location
  - health-recommendation (Div): Health advice based on AQI

### 7. Saved Locations Page
- Page Title: Saved Locations
- Container ID: saved-locations-page (Div)
- Elements:
  - locations-table (Table): Saved locations with current temp and weather
  - view-location-weather-{location_id} (Button per location): View weather
  - remove-location-button-{location_id} (Button per location): Remove location
  - add-new-location-button (Button): Add new location

### 8. Settings Page
- Page Title: Settings
- Container ID: settings-page (Div)
- Elements:
  - temperature-unit-select (Dropdown): Select Celsius, Fahrenheit, Kelvin
  - default-location-select (Dropdown): Set default location
  - alert-notifications-toggle (Checkbox): Enable/disable notifications
  - save-settings-button (Button): Save changes
  - back-to-dashboard (Button): Navigate back to Dashboard


## Section 2: Navigation Structure

- Start Page: Dashboard (dashboard-page)

### Navigation Buttons & Flows:
- dashboard > search-location-button -> Location Search page
- dashboard > view-forecast-button -> Weekly Forecast page
- dashboard > view-alerts-button -> Weather Alerts page
- dashboard > view-air-quality-button -> Air Quality page
- dashboard > view-saved-locations-button -> Saved Locations page
- dashboard > settings-button -> Settings page

- Weekly Forecast page > back-to-dashboard -> Dashboard
- Settings page > back-to-dashboard -> Dashboard

- Location Search page > select-location-button-{location_id} -> Current Weather page for that location
- Saved Locations page > view-location-weather-{location_id} -> Current Weather page
- Saved Locations page > remove-location-button-{location_id} -> Removes location entry, remains on Saved Locations
- Saved Locations page > add-new-location-button -> Location Search page

- Weather Alerts page > acknowledge-alert-button-{alert_id} -> Marks alert acknowledged, updates list

- Air Quality page and Weekly Forecast page both filter by location dropdowns


## Section 3: Data Storage Formats

### 1. Current Weather Data
- File: data/current_weather.txt
- Schema: location_id|location_name|temperature|condition|humidity|wind_speed|last_updated
- Example:
  "1|New York|72|Sunny|65|10|2025-01-20 14:30"

### 2. Forecasts Data
- File: data/forecasts.txt
- Schema: forecast_id|location_id|date|high_temp|low_temp|condition|precipitation|humidity
- Example:
  "1|1|2025-01-21|75|60|Sunny|0|60"

### 3. Locations Data
- File: data/locations.txt
- Schema: location_id|location_name|latitude|longitude|country|timezone
- Example:
  "1|New York|40.7128|-74.0060|USA|EST"

### 4. Weather Alerts Data
- File: data/alerts.txt
- Schema: alert_id|location_id|alert_type|severity|description|start_time|end_time|is_acknowledged
- Example:
  "1|1|Thunderstorm|High|Severe thunderstorm warning in effect until 8 PM|2025-01-20 14:00|2025-01-20 20:00|0"

### 5. Air Quality Data
- File: data/air_quality.txt
- Schema: aqi_id|location_id|aqi_index|pm25|pm10|no2|o3|last_updated
- Example:
  "1|1|45|12.5|35|28|55|2025-01-20 14:30"

### 6. Saved Locations Data
- File: data/saved_locations.txt
- Schema: saved_id|location_id|location_name|is_default
- Example:
  "1|1|New York|1"


-- End of Design Specification --
