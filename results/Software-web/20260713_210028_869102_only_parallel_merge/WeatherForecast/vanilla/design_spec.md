# WeatherForecast Flask Application - Unified Design Specification

---

## 1. Overview

This document defines the comprehensive design specification for the WeatherForecast Flask web application. It unifies and harmonizes the two candidate designs and the user task requirements into a single consistent implementation-ready specification. The application manages data locally in text files under the `data/` directory. It contains 8 primary pages covering weather monitoring, searching, alerts, air quality, saved locations, and user settings.

The specification includes: Flask routes and HTTP methods, page titles, all page element IDs (including dynamic IDs), and details of all associated data files with formats and example data.

---

## 2. Flask Routes, HTTP Methods, Page Titles, and Descriptions

| Route URL                         | HTTP Methods | Page Title         | Description                               |
|----------------------------------|--------------|--------------------|-------------------------------------------|
| `/` or `/dashboard`              | GET          | Weather Dashboard  | Main dashboard page, shows current summary and navigation |
| `/current-weather/<int:location_id>` | GET      | Current Weather    | Detailed current weather for a specific location |
| `/forecast`                     | GET          | Weekly Forecast    | 7-day weather forecast with location filtering |
| `/search`                      | GET, POST    | Search Locations   | Search and select locations, manage saved locations |
| `/alerts`                      | GET          | Weather Alerts     | View active weather alerts and warnings with filters and acknowledgement |
| `/air-quality`                 | GET          | Air Quality Index  | Display air quality index and pollutants, filter by location |
| `/saved-locations`             | GET          | Saved Locations    | List and manage saved locations with current weather |
| `/settings`                   | GET, POST    | Settings           | Configure temperature units, notification preferences, and default location |

---

## 3. Page Element IDs

### 3.1 Weather Dashboard Page
- **Route:** `/` or `/dashboard`
- **Page Title:** Weather Dashboard
- **Container div:** `dashboard-page`
- **Elements:**
  - `current-weather-summary` (Div) - Shows current weather for default location
  - `search-location-button` (Button) - Navigate to `/search`
  - `view-forecast-button` (Button) - Navigate to `/forecast`
  - `view-alerts-button` (Button) - Navigate to `/alerts`

---

### 3.2 Current Weather Page
- **Route:** `/current-weather/<location_id>`
- **Page Title:** Current Weather
- **Container div:** `current-weather-page`
- **Elements:**
  - `location-name` (H1) - Location name
  - `temperature-display` (Div) - Current temperature
  - `weather-condition` (Div) - Weather condition description
  - `humidity-info` (Div) - Humidity percentage
  - `wind-speed-info` (Div) - Wind speed

---

### 3.3 Weekly Forecast Page
- **Route:** `/forecast`
- **Page Title:** Weekly Forecast
- **Container div:** `forecast-page`
- **Elements:**
  - `location-filter` (Dropdown) - Filter forecasts by location
  - `forecast-table` (Table) - Daily forecasts showing date, high temp, low temp, condition
  - `forecast-list` (Div) - Grid display of daily forecast cards
  - `back-to-dashboard` (Button) - Navigate back to `/`

---

### 3.4 Location Search Page
- **Route:** `/search`
- **HTTP Methods:** GET and POST (POST for submitting saved locations or selections)
- **Page Title:** Search Locations
- **Container div:** `search-page`
- **Elements:**
  - `location-search-input` (Input) - Search by city name or coordinates
  - `search-results` (Div) - List of matching locations
  - `select-location-button-{location_id}` (Button) - Dynamic button for each search result to select location
  - `saved-locations-list` (Div) - Display previously saved locations

---

### 3.5 Weather Alerts Page
- **Route:** `/alerts`
- **Page Title:** Weather Alerts
- **Container div:** `alerts-page`
- **Elements:**
  - `alerts-list` (Div) - List all active weather alerts
  - `severity-filter` (Dropdown) - Filter alerts by severity (All, Critical, High, Medium, Low)
  - `location-filter-alerts` (Dropdown) - Filter alerts by location
  - `acknowledge-alert-button-{alert_id}` (Button) - Dynamic button to acknowledge alerts

---

### 3.6 Air Quality Page
- **Route:** `/air-quality`
- **Page Title:** Air Quality Index
- **Container div:** `air-quality-page`
- **Elements:**
  - `aqi-display` (Div) - Numeric Air Quality Index value (0-500)
  - `aqi-description` (Div) - Textual description of AQI (Good, Moderate, etc.)
  - `pollution-details` (Table) - Detailed pollutant data: PM2.5, PM10, NO2, O3
  - `location-aqi-filter` (Dropdown) - Filter by location
  - `health-recommendation` (Div) - Health advice based on AQI

---

### 3.7 Saved Locations Page
- **Route:** `/saved-locations`
- **Page Title:** Saved Locations
- **Container div:** `saved-locations-page`
- **Elements:**
  - `locations-table` (Table) - Saved locations listing including current temperature and condition
  - `view-location-weather-{location_id}` (Button) - Dynamic button to view current weather for a location
  - `remove-location-button-{location_id}` (Button) - Dynamic button to remove saved location
  - `add-new-location-button` (Button) - Button to add new location

---

### 3.8 Settings Page
- **Route:** `/settings`
- **HTTP Methods:** GET and POST
- **Page Title:** Settings
- **Container div:** `settings-page`
- **Elements:**
  - `temperature-unit-select` (Dropdown) - Select temperature unit (Celsius, Fahrenheit, Kelvin)
  - `default-location-select` (Dropdown) - Select default location
  - `alert-notifications-toggle` (Checkbox) - Enable/disable alert notifications
  - `save-settings-button` (Button) - Save the settings changes
  - `back-to-dashboard` (Button) - Navigate back to `/`

---

## 4. Data File Specifications

All data files reside in the `data/` directory with pipe-delimited (`|`) fields. Field order and data formats must be preserved exactly.

### 4.1 Current Weather Data
- **File:** `current_weather.txt`
- **Format:**
  ```
  location_id|location_name|temperature|condition|humidity|wind_speed|last_updated
  ```
- **Example:**
  ```
  1|New York|72|Sunny|65|10|2025-01-20 14:30
  2|London|55|Rainy|80|15|2025-01-20 14:30
  3|Tokyo|45|Cloudy|72|8|2025-01-20 14:30
  ```

### 4.2 Forecasts Data
- **File:** `forecasts.txt`
- **Format:**
  ```
  forecast_id|location_id|date|high_temp|low_temp|condition|precipitation|humidity
  ```
- **Example:**
  ```
  1|1|2025-01-21|75|60|Sunny|0|60
  2|1|2025-01-22|68|55|Cloudy|10|70
  3|2|2025-01-21|58|48|Rainy|80|85
  ```

### 4.3 Locations Data
- **File:** `locations.txt`
- **Format:**
  ```
  location_id|location_name|latitude|longitude|country|timezone
  ```
- **Example:**
  ```
  1|New York|40.7128|-74.0060|USA|EST
  2|London|51.5074|-0.1278|UK|GMT
  3|Tokyo|35.6762|139.6503|Japan|JST
  ```

### 4.4 Weather Alerts Data
- **File:** `alerts.txt`
- **Format:**
  ```
  alert_id|location_id|alert_type|severity|description|start_time|end_time|is_acknowledged
  ```
- **Example:**
  ```
  1|1|Thunderstorm|High|Severe thunderstorm warning in effect until 8 PM|2025-01-20 14:00|2025-01-20 20:00|0
  2|2|Fog|Medium|Dense fog advisory in effect until noon tomorrow|2025-01-20 06:00|2025-01-21 12:00|0
  3|1|Wind|Medium|High wind advisory with gusts up to 45 mph|2025-01-20 15:00|2025-01-21 09:00|1
  ```

### 4.5 Air Quality Data
- **File:** `air_quality.txt`
- **Format:**
  ```
  aqi_id|location_id|aqi_index|pm25|pm10|no2|o3|last_updated
  ```
- **Example:**
  ```
  1|1|45|12.5|35|28|55|2025-01-20 14:30
  2|2|67|22.3|48|42|78|2025-01-20 14:30
  3|3|120|68.5|95|65|110|2025-01-20 14:30
  ```

### 4.6 Saved Locations Data
- **File:** `saved_locations.txt`
- **Format:**
  ```
  saved_id|user_id|location_id|location_name|is_default
  ```
- **Example:**
  ```
  1|1|1|New York|1
  2|1|2|London|0
  3|2|3|Tokyo|1
  ```

---

## 5. Conflict Resolution and Decisions

- Route URL harmonization chose the more descriptive and RESTful URLs from Candidate B (e.g. `/current-weather/<int:location_id>` over `/current_weather/<int:location_id>`, `/forecast` over `/weekly_forecast`, `/search` over `/location_search`, `/alerts` over `/weather_alerts`, `/air-quality` over `/air_quality`, `/saved-locations` over `/saved_locations`). The dashboard retains the alias `/dashboard` alongside `/` for flexibility.
- HTTP methods: The search page supports both GET and POST for submit actions as per Candidate B. Settings page supports GET and POST likewise.
- Page titles and element IDs consistent across candidates are adopted exactly as per the candidate specs and detailed task description.
- Dynamic element IDs explicitly include `{location_id}` or `{alert_id}` placeholders as specified.
- Data file names, formats, field ordering, and examples are consistent and identical; these are unified preserving original schemas.
- All pages contain navigation buttons to improve user experience as detailed.

---

End of unified design_spec.md
