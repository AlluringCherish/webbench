# WeatherForecast Web Application - Design Specification

---

## 1. Flask Routes and Methods

| Route Path                  | Function Name           | HTTP Method | Description / Notes                                   |
|-----------------------------|------------------------|-------------|-----------------------------------------------------|
| `/`                         | dashboard              | GET         | Render Dashboard Page                               |
| `/current_weather/<int:location_id>` | current_weather       | GET         | Display current weather for specified location     |
| `/weekly_forecast`           | weekly_forecast         | GET, POST   | Show weekly forecast; POST for location filter change|
| `/location_search`           | location_search         | GET, POST   | Location search page; POST for searching locations |
| `/weather_alerts`            | weather_alerts          | GET, POST   | Show alerts; POST to filter or acknowledge alerts  |
| `/air_quality`               | air_quality             | GET, POST   | Show air quality; POST for location filter change  |
| `/saved_locations`           | saved_locations         | GET, POST   | Show saved locations; POST for add/remove actions  |
| `/settings`                  | settings                | GET, POST   | Show and update user settings                       |

[Note: POST methods are for filtering, submitting forms, acknowledging alerts, or modifying data.]

Navigations from buttons on Dashboard:
- search-location-button -> `/location_search`
- view-forecast-button -> `/weekly_forecast`
- view-alerts-button -> `/weather_alerts`

Navigation:
- back-to-dashboard buttons on Weekly Forecast and Settings routes redirect to `/`

---

## 2. Template Files, Element IDs & Context Variables

### 2.1 Dashboard Page
- Template: `dashboard.html`
- Page title: "Weather Dashboard"
- HTML Element IDs:
  - `dashboard-page` (Div)
  - `current-weather-summary` (Div) -- Shows brief weather for default or selected location
  - `search-location-button` (Button)
  - `view-forecast-button` (Button)
  - `view-alerts-button` (Button)
- Context Variables:
  - `current_weather` (dict) with keys: `location_id`(int), `location_name`(str), `temperature`(int), `condition`(str), `humidity`(int), `wind_speed`(int)
  - `default_location_id` (int) - for highlight/navigation

### 2.2 Current Weather Page
- Template: `current_weather.html`
- Page title: "Current Weather"
- IDs:
  - `current-weather-page` (Div)
  - `location-name` (H1) - location name display
  - `temperature-display` (Div)
  - `weather-condition` (Div)
  - `humidity-info` (Div)
  - `wind-speed-info` (Div)
- Context:
  - `weather` (dict) with keys: `location_name`(str), `temperature`(int), `condition`(str), `humidity`(int), `wind_speed`(int)

### 2.3 Weekly Forecast Page
- Template: `weekly_forecast.html`
- Page title: "Weekly Forecast"
- IDs:
  - `forecast-page` (Div)
  - `forecast-table` (Table) - tabular forecast
  - `location-filter` (Dropdown) - select location to filter forecasts
  - `forecast-list` (Div) - forecast entries container
  - `back-to-dashboard` (Button)
- Context:
  - `locations` (list of dicts) each with `location_id`(int), `location_name`(str)
  - `selected_location_id` (int)
  - `forecasts` (list of dicts) each with keys: `forecast_id`, `date`, `high_temp`, `low_temp`, `condition`, `precipitation`, `humidity`

### 2.4 Location Search Page
- Template: `location_search.html`
- Page title: "Search Locations"
- IDs:
  - `search-page` (Div)
  - `location-search-input` (Input) - user text entry
  - `search-results` (Div) - contains search result entries
  - `select-location-button-{location_id}` (Button for each search result)
  - `saved-locations-list` (Div) - display saved locations
- Context:
  - `search_query` (str)
  - `search_results` (list of dicts) each with `location_id`, `location_name`, `country`
  - `saved_locations` (list of dicts) each with `location_id`, `location_name`, `is_default`(bool)

### 2.5 Weather Alerts Page
- Template: `weather_alerts.html`
- Page title: "Weather Alerts"
- IDs:
  - `alerts-page` (Div)
  - `alerts-list` (Div) - list of active or filtered alerts
  - `severity-filter` (Dropdown) - filter by alert severity
  - `location-filter-alerts` (Dropdown) - filter by location
  - `acknowledge-alert-button-{alert_id}` (Button per alert)
- Context:
  - `alerts` (list of dicts) each with `alert_id`, `location_name`, `alert_type`, `severity`, `description`, `start_time`, `end_time`, `is_acknowledged`(bool)
  - `location_options` (list of dicts) each with `location_id`, `location_name`
  - `selected_severity` (str or None)
  - `selected_location_id` (int or None)

### 2.6 Air Quality Page
- Template: `air_quality.html`
- Page title: "Air Quality Index"
- IDs:
  - `air-quality-page` (Div)
  - `aqi-display` (Div) - AQI number
  - `aqi-description` (Div) - textual interpretation
  - `pollution-details` (Table) - PM2.5, PM10, NO2, O3 values
  - `location-aqi-filter` (Dropdown) - select location
  - `health-recommendation` (Div) - health advice
- Context:
  - `locations` (list of dicts) e.g., `location_id`, `location_name`
  - `selected_location_id` (int)
  - `aqi_data` (dict) with keys: `aqi_index`, `pm25`, `pm10`, `no2`, `o3`, `last_updated`
  - `health_advice` (str)

### 2.7 Saved Locations Page
- Template: `saved_locations.html`
- Page title: "Saved Locations"
- IDs:
  - `saved-locations-page` (Div)
  - `locations-table` (Table)
  - `view-location-weather-{location_id}` (Button for each saved location)
  - `remove-location-button-{location_id}` (Button for each saved location)
  - `add-new-location-button` (Button)
- Context:
  - `saved_locations` (list of dicts) each with `location_id`, `location_name`, `is_default` (bool)

### 2.8 Settings Page
- Template: `settings.html`
- Page title: "Settings"
- IDs:
  - `settings-page` (Div)
  - `temperature-unit-select` (Dropdown)
  - `default-location-select` (Dropdown)
  - `alert-notifications-toggle` (Checkbox)
  - `save-settings-button` (Button)
  - `back-to-dashboard` (Button)
- Context:
  - `temperature_unit` (str) e.g., "F" or "C"
  - `locations` (list of dicts) - for default-location selection
  - `default_location_id` (int)
  - `alert_notifications_enabled` (bool)

---

## 3. Data File Interaction and Parsing Schemas

### 3.1 Current Weather Data (`current_weather.txt`)
- Fields: `location_id|location_name|temperature|condition|humidity|wind_speed|last_updated`
- Use:
  - Load all entries on app startup or request
  - Map by `location_id` for quick lookup
  - Types:
    - `location_id`: int
    - `location_name`: str
    - `temperature`: int
    - `condition`: str
    - `humidity`: int
    - `wind_speed`: int
    - `last_updated`: datetime string

### 3.2 Forecasts Data (`forecasts.txt`)
- Fields:
  `forecast_id|location_id|date|high_temp|low_temp|condition|precipitation|humidity`
- Use:
  - Parse all entries
  - Filter by `location_id` for weekly forecast page
  - Types:
    - `forecast_id`: int
    - `location_id`: int
    - `date`: date string
    - `high_temp`, `low_temp`: int
    - `condition`: str
    - `precipitation`: int or float
    - `humidity`: int

### 3.3 Locations Data (`locations.txt`)
- Fields:
  `location_id|location_name|latitude|longitude|country|timezone`
- Use:
  - Load all locations
  - Populate dropdowns for location selections
  - Types:
    - `location_id`: int
    - `location_name`: str
    - `latitude`, `longitude`: float
    - `country`: str
    - `timezone`: str

### 3.4 Weather Alerts Data (`alerts.txt`)
- Fields:
  `alert_id|location_id|alert_type|severity|description|start_time|end_time|is_acknowledged`
- Use:
  - Load all alerts
  - Filter by `location_id` and/or `severity`
  - Update acknowledgement state on POST
  - Types:
    - `alert_id`: int
    - `location_id`: int
    - `alert_type`: str
    - `severity`: str
    - `description`: str
    - `start_time`, `end_time`: datetime strings
    - `is_acknowledged`: bool (0 or 1 in file)

### 3.5 Air Quality Data (`air_quality.txt`)
- Fields:
  `aqi_id|location_id|aqi_index|pm25|pm10|no2|o3|last_updated`
- Use:
  - Load all AQI records
  - Filter by `location_id` for display
  - Types:
    - `aqi_id`: int
    - `location_id`: int
    - `aqi_index`: int
    - `pm25`, `pm10`, `no2`, `o3`: float
    - `last_updated`: datetime string

### 3.6 Saved Locations Data (`saved_locations.txt`)
- Fields:
  `saved_id|user_id|location_id|location_name|is_default`
- Use:
  - Load saved locations for user
  - Track default location
  - Support add/remove
  - Types:
    - `saved_id`: int
    - `user_id`: int (if user multiple supported)
    - `location_id`: int
    - `location_name`: str
    - `is_default`: bool (0 or 1)

---

# Notes:
- The application assumes one user (id=1) for saved locations in current scope.
- Location filters apply dropdown options sourced from `locations.txt`.
- Acknowledge Alert POST updates `alerts.txt` (flagging is_acknowledged=1).
- Settings stored either in session or separate config, not detailed here.

This comprehensive specification enables backend and frontend teams to implement coherent APIs, templates, and data access layers aligned with the requirements.
