# WeatherForecast Application - Design Specification Candidate B

## Overview
This document specifies the Flask route mappings, page titles, element IDs, and local text file data source formats for the WeatherForecast application. It is a fully independent design covering all eight pages starting from the Dashboard.

---

## 1. Flask Routes and Page Details

### 1. Dashboard Page
- **URL:** `/` (GET)
- **Page Title:** Weather Dashboard
- **Purpose:** Main landing page showing current weather summary and navigation buttons.
- **Element IDs:**
  - `dashboard-page` (Div container)
  - `current-weather-summary` (Div showing current weather for default location)
  - `search-location-button` (Button navigates to /search)
  - `view-forecast-button` (Button navigates to /forecast)
  - `view-alerts-button` (Button navigates to /alerts)

### 2. Current Weather Page
- **URL:** `/current-weather/<int:location_id>` (GET)
- **Page Title:** Current Weather
- **Purpose:** Detail current weather of selected location.
- **Element IDs:**
  - `current-weather-page` (Div container)
  - `location-name` (H1 displaying location name)
  - `temperature-display` (Div showing temperature)
  - `weather-condition` (Div showing weather condition)
  - `humidity-info` (Div showing humidity %)
  - `wind-speed-info` (Div showing wind speed)

### 3. Weekly Forecast Page
- **URL:** `/forecast` (GET)
- **Page Title:** Weekly Forecast
- **Purpose:** Display 7-day forecast with filtering by location.
- **Element IDs:**
  - `forecast-page` (Div container)
  - `location-filter` (Dropdown to select location for forecast)
  - `forecast-table` (Table with date, high temp, low temp, condition per day)
  - `forecast-list` (Div grid of forecast cards)
  - `back-to-dashboard` (Button navigating to `/`)

### 4. Location Search Page
- **URL:** `/search` (GET, POST)
- **Page Title:** Search Locations
- **Purpose:** Search locations by name/coordinates and select/save them.
- **Element IDs:**
  - `search-page` (Div container)
  - `location-search-input` (Input text for search)
  - `search-results` (Div listing matched locations)
  - `select-location-button-{location_id}` (Button per location in search results)
  - `saved-locations-list` (Div showing previously saved locations)

### 5. Weather Alerts Page
- **URL:** `/alerts` (GET)
- **Page Title:** Weather Alerts
- **Purpose:** View active weather alerts with filters and acknowledge alerts.
- **Element IDs:**
  - `alerts-page` (Div container)
  - `alerts-list` (Div listing alerts with severity, description, location)
  - `severity-filter` (Dropdown filter: All, Critical, High, Medium, Low)
  - `location-filter-alerts` (Dropdown to filter alerts by location)
  - `acknowledge-alert-button-{alert_id}` (Button per alert to acknowledge)

### 6. Air Quality Page
- **URL:** `/air-quality` (GET)
- **Page Title:** Air Quality Index
- **Purpose:** Show air quality indices and pollution details filtered by location.
- **Element IDs:**
  - `air-quality-page` (Div container)
  - `aqi-display` (Div showing AQI numeric value)
  - `aqi-description` (Div describing AQI level)
  - `pollution-details` (Table listing PM2.5, PM10, NO2, O3 values)
  - `location-aqi-filter` (Dropdown to select location)
  - `health-recommendation` (Div with health advice based on AQI)

### 7. Saved Locations Page
- **URL:** `/saved-locations` (GET)
- **Page Title:** Saved Locations
- **Purpose:** List saved locations with current weather access and management.
- **Element IDs:**
  - `saved-locations-page` (Div container)
  - `locations-table` (Table of saved locations with temp and condition)
  - `view-location-weather-{location_id}` (Button to view current weather)
  - `remove-location-button-{location_id}` (Button to remove location)
  - `add-new-location-button` (Button to add new location)

### 8. Settings Page
- **URL:** `/settings` (GET, POST)
- **Page Title:** Settings
- **Purpose:** Configure temperature units, notifications, and default location.
- **Element IDs:**
  - `settings-page` (Div container)
  - `temperature-unit-select` (Dropdown for Celsius, Fahrenheit, Kelvin)
  - `default-location-select` (Dropdown for default location)
  - `alert-notifications-toggle` (Checkbox to toggle alerts)
  - `save-settings-button` (Button to save settings)
  - `back-to-dashboard` (Button to return to `/`)


---

## 2. Data Files and Formats

All data is stored locally in the `data` directory in text files using pipe (`|`) delimiter. Each file is read and parsed for use in page rendering.

### 2.1 Current Weather Data: `current_weather.txt`
Format per line:
```
location_id|location_name|temperature|condition|humidity|wind_speed|last_updated
```
Example:
```
1|New York|72|Sunny|65|10|2025-01-20 14:30
2|London|55|Rainy|80|15|2025-01-20 14:30
3|Tokyo|45|Cloudy|72|8|2025-01-20 14:30
```

### 2.2 Forecasts Data: `forecasts.txt`
Format per line:
```
forecast_id|location_id|date|high_temp|low_temp|condition|precipitation|humidity
```
Example:
```
1|1|2025-01-21|75|60|Sunny|0|60
2|1|2025-01-22|68|55|Cloudy|10|70
3|2|2025-01-21|58|48|Rainy|80|85
```

### 2.3 Locations Data: `locations.txt`
Format per line:
```
location_id|location_name|latitude|longitude|country|timezone
```
Example:
```
1|New York|40.7128|-74.0060|USA|EST
2|London|51.5074|-0.1278|UK|GMT
3|Tokyo|35.6762|139.6503|Japan|JST
```

### 2.4 Weather Alerts Data: `alerts.txt`
Format per line:
```
alert_id|location_id|alert_type|severity|description|start_time|end_time|is_acknowledged
```
Example:
```
1|1|Thunderstorm|High|Severe thunderstorm warning in effect until 8 PM|2025-01-20 14:00|2025-01-20 20:00|0
2|2|Fog|Medium|Dense fog advisory in effect until noon tomorrow|2025-01-20 06:00|2025-01-21 12:00|0
3|1|Wind|Medium|High wind advisory with gusts up to 45 mph|2025-01-20 15:00|2025-01-21 09:00|1
```

### 2.5 Air Quality Data: `air_quality.txt`
Format per line:
```
aqi_id|location_id|aqi_index|pm25|pm10|no2|o3|last_updated
```
Example:
```
1|1|45|12.5|35|28|55|2025-01-20 14:30
2|2|67|22.3|48|42|78|2025-01-20 14:30
3|3|120|68.5|95|65|110|2025-01-20 14:30
```

### 2.6 Saved Locations Data: `saved_locations.txt`
Format per line:
```
saved_id|user_id|location_id|location_name|is_default
```
Example:
```
1|1|1|New York|1
2|1|2|London|0
3|2|3|Tokyo|1
```

---

## 3. Integration Details

- Each Flask route reads from the respective data files in `data/` directory to load needed data.
- Dynamic button IDs (e.g., `select-location-button-{location_id}`, `acknowledge-alert-button-{alert_id}`, `view-location-weather-{location_id}`, `remove-location-button-{location_id}`) are dynamically rendered according to data identifiers.
- Filtering options (dropdowns) use `locations.txt` to populate choices.
- Settings changes (POST) update configuration on disk or in a suitable local state file (not specified here).
- Dashboard uses the default location from saved locations marked `is_default=1`.
- All pages return HTML templates structured with the specified element IDs.

---

This specification provides a complete independent design candidate for WeatherForecast using Flask and local text files, sufficient for direct implementation.