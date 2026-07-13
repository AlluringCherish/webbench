# Design Specification for WeatherForecast Flask Application

---

## 1. Overview
This document specifies the complete design for the WeatherForecast Flask web app covering 8 pages. It defines Flask routes, page titles, all element IDs, and local text file data formats with examples. The application data is stored in `data` directory using text files as per requirements.

---

## 2. Flask Routes and Page Titles

| Route URL                      | HTTP Methods | Page Title         | Description                      |
|-------------------------------|--------------|--------------------|----------------------------------|
| `/` or `/dashboard`            | GET          | Weather Dashboard  | Main dashboard page               |
| `/current_weather/<int:location_id>` | GET     | Current Weather    | Detailed current weather for location|
| `/weekly_forecast`             | GET          | Weekly Forecast    | 7-day weather forecast            |
| `/location_search`             | GET          | Search Locations   | Search and select locations       |
| `/weather_alerts`             | GET          | Weather Alerts     | Active weather alerts and warnings|
| `/air_quality`                 | GET          | Air Quality Index  | Air quality data                  |
| `/saved_locations`             | GET          | Saved Locations    | List of saved locations           |
| `/settings`                   | GET, POST    | Settings           | App settings configuration        |

---

## 3. Page Element IDs

### 3.1 Dashboard Page
- Route: `/dashboard` or `/`
- Page Title: Weather Dashboard
- Container div: `dashboard-page`
- Elements:
  - `current-weather-summary` (Div)
  - `search-location-button` (Button)
  - `view-forecast-button` (Button)
  - `view-alerts-button` (Button)

---

### 3.2 Current Weather Page
- Route: `/current_weather/<location_id>`
- Page Title: Current Weather
- Container div: `current-weather-page`
- Elements:
  - `location-name` (H1)
  - `temperature-display` (Div)
  - `weather-condition` (Div)
  - `humidity-info` (Div)
  - `wind-speed-info` (Div)

---

### 3.3 Weekly Forecast Page
- Route: `/weekly_forecast`
- Page Title: Weekly Forecast
- Container div: `forecast-page`
- Elements:
  - `forecast-table` (Table)
  - `location-filter` (Dropdown)
  - `forecast-list` (Div) - grid of daily forecast cards
  - `back-to-dashboard` (Button)

---

### 3.4 Location Search Page
- Route: `/location_search`
- Page Title: Search Locations
- Container div: `search-page`
- Elements:
  - `location-search-input` (Input)
  - `search-results` (Div) - list of search results
  - Dynamic button for each search result: `select-location-button-{location_id}`
  - `saved-locations-list` (Div) - previously saved locations

---

### 3.5 Weather Alerts Page
- Route: `/weather_alerts`
- Page Title: Weather Alerts
- Container div: `alerts-page`
- Elements:
  - `alerts-list` (Div) - list of active alerts
  - `severity-filter` (Dropdown) - filter alerts by severity
  - `location-filter-alerts` (Dropdown) - filter alerts by location
  - Dynamic button per alert: `acknowledge-alert-button-{alert_id}`

---

### 3.6 Air Quality Page
- Route: `/air_quality`
- Page Title: Air Quality Index
- Container div: `air-quality-page`
- Elements:
  - `aqi-display` (Div) - Air Quality Index numeric value
  - `aqi-description` (Div) - AQ description text
  - `pollution-details` (Table) - details on pollutants PM2.5, PM10, NO2, O3
  - `location-aqi-filter` (Dropdown) - filter by location
  - `health-recommendation` (Div) - health advice text

---

### 3.7 Saved Locations Page
- Route: `/saved_locations`
- Page Title: Saved Locations
- Container div: `saved-locations-page`
- Elements:
  - `locations-table` (Table) - saved locations with current temp and condition
  - Dynamic buttons:
    - View weather: `view-location-weather-{location_id}`
    - Remove saved location: `remove-location-button-{location_id}`
  - `add-new-location-button` (Button)

---

### 3.8 Settings Page
- Route: `/settings`
- Page Title: Settings
- Container div: `settings-page`
- Elements:
  - `temperature-unit-select` (Dropdown) - units selection
  - `default-location-select` (Dropdown) - select default location
  - `alert-notifications-toggle` (Checkbox) - notification toggle
  - `save-settings-button` (Button)
  - `back-to-dashboard` (Button)

---

## 4. Data File Specifications

All data files are stored in the `data/` directory.

### 4.1 Current Weather Data
- Filename: `current_weather.txt`
- Format (pipe-delimited):
  ```
  location_id|location_name|temperature|condition|humidity|wind_speed|last_updated
  ```
- Example rows:
  ```
  1|New York|72|Sunny|65|10|2025-01-20 14:30
  2|London|55|Rainy|80|15|2025-01-20 14:30
  3|Tokyo|45|Cloudy|72|8|2025-01-20 14:30
  ```

---

### 4.2 Forecasts Data
- Filename: `forecasts.txt`
- Format:
  ```
  forecast_id|location_id|date|high_temp|low_temp|condition|precipitation|humidity
  ```
- Example rows:
  ```
  1|1|2025-01-21|75|60|Sunny|0|60
  2|1|2025-01-22|68|55|Cloudy|10|70
  3|2|2025-01-21|58|48|Rainy|80|85
  ```

---

### 4.3 Locations Data
- Filename: `locations.txt`
- Format:
  ```
  location_id|location_name|latitude|longitude|country|timezone
  ```
- Example rows:
  ```
  1|New York|40.7128|-74.0060|USA|EST
  2|London|51.5074|-0.1278|UK|GMT
  3|Tokyo|35.6762|139.6503|Japan|JST
  ```

---

### 4.4 Weather Alerts Data
- Filename: `alerts.txt`
- Format:
  ```
  alert_id|location_id|alert_type|severity|description|start_time|end_time|is_acknowledged
  ```
- Example rows:
  ```
  1|1|Thunderstorm|High|Severe thunderstorm warning in effect until 8 PM|2025-01-20 14:00|2025-01-20 20:00|0
  2|2|Fog|Medium|Dense fog advisory in effect until noon tomorrow|2025-01-20 06:00|2025-01-21 12:00|0
  3|1|Wind|Medium|High wind advisory with gusts up to 45 mph|2025-01-20 15:00|2025-01-21 09:00|1
  ```

---

### 4.5 Air Quality Data
- Filename: `air_quality.txt`
- Format:
  ```
  aqi_id|location_id|aqi_index|pm25|pm10|no2|o3|last_updated
  ```
- Example rows:
  ```
  1|1|45|12.5|35|28|55|2025-01-20 14:30
  2|2|67|22.3|48|42|78|2025-01-20 14:30
  3|3|120|68.5|95|65|110|2025-01-20 14:30
  ```

---

### 4.6 Saved Locations Data
- Filename: `saved_locations.txt`
- Format:
  ```
  saved_id|user_id|location_id|location_name|is_default
  ```
- Example rows:
  ```
  1|1|1|New York|1
  2|1|2|London|0
  3|2|3|Tokyo|1
  ```

---

## 5. Notes
- The routes and element IDs are strictly as defined to ensure compatibility with front-end and back-end logic.
- Dynamic IDs include `{location_id}` or `{alert_id}` to distinguish multiple elements in dynamic lists.
- Data files must be parsed and updated maintaining the field order and delimiter `|`.
- The app starts at the Dashboard page (`/` or `/dashboard`).

---

End of design_candidate_a.md
