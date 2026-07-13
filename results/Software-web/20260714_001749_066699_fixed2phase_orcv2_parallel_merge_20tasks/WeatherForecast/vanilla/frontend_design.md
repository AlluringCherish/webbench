# Frontend Design for WeatherForecast Web Application

---

## Section 1: HTML Template Specification

### 1. Dashboard Page
- **Template Filename:** dashboard.html
- **Page Title:** Weather Dashboard
- **Container Element:** 
  - ID: `dashboard-page` (div) - Main container for dashboard page
- **Page Elements:**
  - `current-weather-summary` (div) - Displays current weather summary for default location.
  - `search-location-button` (button) - Navigates user to Location Search Page.
  - `view-forecast-button` (button) - Navigates user to Weekly Forecast Page.
  - `view-alerts-button` (button) - Navigates user to Weather Alerts Page.

### 2. Current Weather Page
- **Template Filename:** current_weather.html
- **Page Title:** Current Weather
- **Container Element:**
  - ID: `current-weather-page` (div) - Page container
- **Page Elements:**
  - `location-name` (h1) - Shows selected location's name
  - `temperature-display` (div) - Shows current temperature
  - `weather-condition` (div) - Shows weather condition text/icon
  - `humidity-info` (div) - Shows humidity percentage
  - `wind-speed-info` (div) - Shows wind speed

### 3. Weekly Forecast Page
- **Template Filename:** weekly_forecast.html
- **Page Title:** Weekly Forecast
- **Container Element:**
  - ID: `forecast-page` (div) - Main container
- **Page Elements:**
  - `forecast-table` (table) - Tabular display of daily forecast details (date, highs, lows, condition)
  - `location-filter` (select dropdown) - Dropdown for filtering forecasts by location
  - `forecast-list` (div) - Grid layout showing individual day forecast cards
  - `back-to-dashboard` (button) - Navigates user back to Dashboard Page

### 4. Location Search Page
- **Template Filename:** location_search.html
- **Page Title:** Search Locations
- **Container Element:**
  - ID: `search-page` (div) - Main container
- **Page Elements:**
  - `location-search-input` (input, text) - Input field for searching city name or coordinates
  - `search-results` (div) - Displays list of matching location results
  - `select-location-button-{location_id}` (button) - Dynamic button per search result to select that location
  - `saved-locations-list` (div) - Displays previously saved locations

### 5. Weather Alerts Page
- **Template Filename:** weather_alerts.html
- **Page Title:** Weather Alerts
- **Container Element:**
  - ID: `alerts-page` (div) - Main container
- **Page Elements:**
  - `alerts-list` (div) - List of active weather alerts with details and acknowledgement
  - `severity-filter` (select dropdown) - Dropdown to filter alerts by severity
  - `location-filter-alerts` (select dropdown) - Dropdown to filter alerts by location
  - `acknowledge-alert-button-{alert_id}` (button) - Dynamic button to acknowledge each alert

### 6. Air Quality Page
- **Template Filename:** air_quality.html
- **Page Title:** Air Quality Index
- **Container Element:**
  - ID: `air-quality-page` (div) - Main container
- **Page Elements:**
  - `aqi-display` (div) - Shows Air Quality Index numeric value (0-500)
  - `aqi-description` (div) - Air quality category description text
  - `pollution-details` (table) - Tabular data for pollutants: PM2.5, PM10, NO2, O3
  - `location-aqi-filter` (select dropdown) - Dropdown to filter air quality data by location
  - `health-recommendation` (div) - Displays health-related recommendations based on AQI

### 7. Saved Locations Page
- **Template Filename:** saved_locations.html
- **Page Title:** Saved Locations
- **Container Element:**
  - ID: `saved-locations-page` (div) - Main container
- **Page Elements:**
  - `locations-table` (table) - Table of saved locations showing name, temperature, and condition
  - `view-location-weather-{location_id}` (button) - Dynamic button to view weather of a saved location
  - `remove-location-button-{location_id}` (button) - Dynamic button to remove a saved location
  - `add-new-location-button` (button) - Button to add new location

### 8. Settings Page
- **Template Filename:** settings.html
- **Page Title:** Settings
- **Container Element:**
  - ID: `settings-page` (div) - Main container
- **Page Elements:**
  - `temperature-unit-select` (select dropdown) - Select temperature unit (Celsius, Fahrenheit, Kelvin)
  - `default-location-select` (select dropdown) - Select default location
  - `alert-notifications-toggle` (checkbox) - Toggle for alert notifications on/off
  - `save-settings-button` (button) - Button to save settings
  - `back-to-dashboard` (button) - Button to navigate back to Dashboard Page

---

## Section 2: Navigation and Interaction

### Navigation Logic
- **Dashboard Page:**
  - `search-location-button` navigates to Location Search Page (`/search`)
  - `view-forecast-button` navigates to Weekly Forecast Page (`/forecast`)
  - `view-alerts-button` navigates to Weather Alerts Page (`/alerts`)

- **Weekly Forecast Page:**
  - `back-to-dashboard` navigates to Dashboard Page (`/dashboard`)

- **Settings Page:**
  - `back-to-dashboard` navigates to Dashboard Page (`/dashboard`)

- **Saved Locations Page:**
  - `add-new-location-button` navigates to Location Search Page (`/search`)

- **Location Search Page:**
  - `select-location-button-{location_id}` sets the selected location and redirects to Current Weather Page (`/current_weather`)

- **Saved Locations Page:**
  - `view-location-weather-{location_id}` navigates to Current Weather Page for that location (`/current_weather?location_id={location_id}`)
  - `remove-location-button-{location_id}` removes the saved location from the list

- **Weather Alerts Page:**
  - `acknowledge-alert-button-{alert_id}` acknowledges the alert and updates UI accordingly

### Interactive Component Behaviors
- **Dropdowns:**
  - `location-filter` (Weekly Forecast) dynamically populates from saved/available locations
  - `severity-filter` (Alerts) dynamically filters alerts by severity levels
  - `location-filter-alerts` filters alerts by location
  - `location-aqi-filter` filters air quality info by selected location
  - `temperature-unit-select` (Settings) sets temperature unit preference
  - `default-location-select` (Settings) sets user’s default location

- **Search Input:**
  - `location-search-input` filters locations in real-time or on submission

- **Buttons:**
  - All dynamic buttons follow pattern `id-{entity_id}` for specific entities to facilitate event binding

- **State Updates:**
  - Selecting location updates relevant pages with that location's data
  - Acknowledging alerts updates alert status and may disable acknowledge button

---

## Section 3: UI Data Binding

### 1. Dashboard Page
- **Context Variables:**
  - `default_location` (dict): {id, name}
  - `current_weather` (dict): temperature, condition, humidity, wind_speed

### 2. Current Weather Page
- **Context Variables:**
  - `location` (dict): {id, name}
  - `weather_details` (dict): temperature, condition, humidity, wind_speed

### 3. Weekly Forecast Page
- **Context Variables:**
  - `locations` (list of dict): [{id, name}]
  - `selected_location_id` (int)
  - `forecast_data` (list of dict): Each dict includes date, high_temp, low_temp, condition, precipitation, humidity

### 4. Location Search Page
- **Context Variables:**
  - `search_query` (string)
  - `search_results` (list of dict): Each dict with location_id, name, coordinates
  - `saved_locations` (list of dict): Saved location info

### 5. Weather Alerts Page
- **Context Variables:**
  - `alerts` (list of dict): alert_id, location_name, alert_type, severity, description, start_time, end_time, is_acknowledged
  - `severity_levels` (list of string): All, Critical, High, Medium, Low
  - `locations` (list of dict): for filter dropdown

### 6. Air Quality Page
- **Context Variables:**
  - `locations` (list of dict): [{id, name}]
  - `selected_location_id` (int)
  - `air_quality` (dict): aqi_index, description, pollutant_values (pm25, pm10, no2, o3)
  - `health_recs` (string): health recommendations text

### 7. Saved Locations Page
- **Context Variables:**
  - `saved_locations` (list of dict): Each dict includes location_id, location_name, current_temp, condition

### 8. Settings Page
- **Context Variables:**
  - `temperature_units` (list): ['Celsius', 'Fahrenheit', 'Kelvin']
  - `locations` (list of dict): for default location selection
  - `user_settings` (dict): current selections for temperature unit, default location, alert notifications toggle

---

This frontend design document should fully guide the implementation of all necessary HTML templates, UI components, navigation paths, and UI data bindings to build the WeatherForecast web application frontend.
