# WeatherForecast Application Design Specification

---

## Section 1: Flask Routes Specification

| URL Path                      | Allowed Methods | Function Name           | Template Filename           | Context Variables (name: type)                                                                                                                               |
|-------------------------------|-----------------|------------------------|-----------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------|
| /                             | GET             | root_redirect          | N/A (redirect to /dashboard) | None (Redirect to dashboard page)                                                                                                                           |
| /dashboard                    | GET             | dashboard_page         | dashboard.html              | current_weather_summary: dict {location_name: str, temperature: float, condition: str, humidity: int, wind_speed: float},
 quick_access_buttons: dict {search_location: str, weekly_forecast: str, alerts: str} (URLs)            |
| /weather/current/<int:location_id> | GET             | current_weather_page   | current_weather.html        | location_name: str,
 temperature: float,
 condition: str,
 humidity: int,
 wind_speed: float                                                                 |
| /forecast/weekly/<int:location_id>  | GET             | weekly_forecast_page   | weekly_forecast.html        | location_id: int,
 location_name: str,
 weekly_forecast: list[dict {date: str, high_temp: float, low_temp: float, condition: str, precipitation: int, humidity: int}] |
| /location/search              | GET             | location_search_page   | location_search.html        | search_results: list[dict {location_id: int, location_name: str, latitude: float, longitude: float, country: str, timezone: str}],
 saved_locations: list[dict {location_id: int, location_name: str}]                             |
| /alerts                      | GET             | weather_alerts_page    | alerts.html                 | alerts: list[dict {alert_id: int, location_id: int, alert_type: str, severity: str, description: str, start_time: str, end_time: str, is_acknowledged: bool}],
 severity_filter_options: list[str],
 location_filter_options: list[dict {location_id: int, location_name: str}]                                   |
| /alerts/acknowledge/<int:alert_id> | POST            | acknowledge_alert      | N/A (redirect to /alerts)   | None (action route for alert acknowledgment)                                                                                                              |
| /airquality                   | GET             | air_quality_page       | air_quality.html            | aqi_data: dict {location_id: int, aqi_index: int, pm25: float, pm10: float, no2: float, o3: float, last_updated: str},
 health_recommendation: str,
 location_filter_options: list[dict {location_id: int, location_name: str}]                       |
| /savedlocations              | GET             | saved_locations_page   | saved_locations.html        | saved_locations: list[dict {location_id: int, location_name: str, temperature: float, condition: str}],
 user_default_location_id: int                                                                                 |
| /savedlocations/remove/<int:location_id> | POST            | remove_saved_location  | N/A (redirect to /savedlocations) | None (action route for removing saved location)                                                                                                         |
| /savedlocations/view/<int:location_id> | GET             | view_location_weather  | current_weather.html        | location_name: str,
 temperature: float,
 condition: str,
 humidity: int,
 wind_speed: float                                                                 |
| /settings                    | GET             | settings_page          | settings.html               | temperature_units: list[str],
 default_location_id: int,
 locations: list[dict {location_id: int, location_name: str}],
 alert_notifications_enabled: bool                          |
| /settings/save               | POST            | save_settings          | N/A (redirect to /settings) | None (action route for saving settings)                                                                                                                   |


Note:
- The root '/' route performs a redirect to the dashboard page.
- Dynamic route parameters are in angular brackets with explicit types (e.g. <int:location_id>).
- POST methods are used for state-changing operations like acknowledging alerts, removing saved locations, and saving settings.
- Context variables are precisely typed and structured to align with frontend requirements.

---

## Section 2: Frontend HTML Templates Specification

### 1. Template: dashboard.html
- File Path: templates/dashboard.html
- Page Title: Weather Dashboard
- Element IDs and Descriptions:
  - dashboard-page (Div) - Container for the dashboard page.
  - current-weather-summary (Div) - Display of current weather conditions for default location.
  - search-location-button (Button) - Navigates to Location Search page.
  - view-forecast-button (Button) - Navigates to Weekly Forecast page.
  - view-alerts-button (Button) - Navigates to Weather Alerts page.
- Navigation Mappings:
  - search-location-button -> url_for('location_search_page')
  - view-forecast-button -> url_for('weekly_forecast_page', location_id=default_location_id)
  - view-alerts-button -> url_for('weather_alerts_page')
- Context Variables Available:
  - current_weather_summary: dict {location_name: str, temperature: float, condition: str, humidity: int, wind_speed: float}
- Usage Notes:
  - Display current weather details dynamically inside current-weather-summary.
  - Buttons trigger navigation to respective pages.

### 2. Template: current_weather.html
- File Path: templates/current_weather.html
- Page Title: Current Weather
- Element IDs and Descriptions:
  - current-weather-page (Div) - Container for current weather page.
  - location-name (H1) - Displays the selected location name.
  - temperature-display (Div) - Shows current temperature.
  - weather-condition (Div) - Shows weather condition description.
  - humidity-info (Div) - Displays humidity percentage.
  - wind-speed-info (Div) - Displays wind speed.
- Navigation Mappings:
  - (No direct navigation elements specified, back navigation handled by browser or dashboard navigation elsewhere.)
- Context Variables Available:
  - location_name: str
  - temperature: float
  - condition: str
  - humidity: int
  - wind_speed: float
- Usage Notes:
  - Purely a detail display page.

### 3. Template: weekly_forecast.html
- File Path: templates/weekly_forecast.html
- Page Title: Weekly Forecast
- Element IDs and Descriptions:
  - forecast-page (Div) - Container for the weekly forecast page.
  - forecast-table (Table) - Displays forecast with columns: date, high temp, low temp, condition.
  - location-filter (Dropdown) - Select location filter (populated with locations).
  - forecast-list (Div) - Displays forecast cards for each of the 7 days.
  - back-to-dashboard (Button) - Navigates back to the dashboard.
- Navigation Mappings:
  - back-to-dashboard -> url_for('dashboard_page')
- Context Variables Available:
  - location_id: int
  - location_name: str
  - weekly_forecast: list[dict {date: str, high_temp: float, low_temp: float, condition: str, precipitation: int, humidity: int}]
- Usage Notes:
  - Loop over weekly_forecast to render forecast cards.
  - Location-filter triggers page reload with selected location to update forecast.

### 4. Template: location_search.html
- File Path: templates/location_search.html
- Page Title: Search Locations
- Element IDs and Descriptions:
  - search-page (Div) - Container for location search page.
  - location-search-input (Input) - Input field for searching locations.
  - search-results (Div) - Container listing matching locations.
  - select-location-button-{location_id} (Button) - Button to select each location result; dynamic IDs per location.
  - saved-locations-list (Div) - Displays user's saved locations.
- Navigation Mappings:
  - select-location-button-{location_id} -> url_for('view_location_weather', location_id=location_id)
- Context Variables Available:
  - search_results: list[dict {location_id: int, location_name: str, latitude: float, longitude: float, country: str, timezone: str}]
  - saved_locations: list[dict {location_id: int, location_name: str}]
- Usage Notes:
  - Use a loop to generate search-results entries.
  - Buttons for each result use dynamic IDs.

### 5. Template: alerts.html
- File Path: templates/alerts.html
- Page Title: Weather Alerts
- Element IDs and Descriptions:
  - alerts-page (Div) - Container for alerts page.
  - alerts-list (Div) - Lists active alerts with details.
  - severity-filter (Dropdown) - Filter alerts by severity.
  - location-filter-alerts (Dropdown) - Filter alerts by location.
  - acknowledge-alert-button-{alert_id} (Button) - Acknowledge button for each alert, dynamic IDs.
- Navigation Mappings:
  - acknowledge-alert-button-{alert_id} -> POST to url_for('acknowledge_alert', alert_id=alert_id)
- Context Variables Available:
  - alerts: list[dict {alert_id: int, location_id: int, alert_type: str, severity: str, description: str, start_time: str, end_time: str, is_acknowledged: bool}]
  - severity_filter_options: list[str]
  - location_filter_options: list[dict {location_id: int, location_name: str}]
- Usage Notes:
  - Loop over alerts to display each active alert.
  - Filter dropdowns control displayed alerts.

### 6. Template: air_quality.html
- File Path: templates/air_quality.html
- Page Title: Air Quality Index
- Element IDs and Descriptions:
  - air-quality-page (Div) - Container for air quality page.
  - aqi-display (Div) - Displays AQI value (0-500).
  - aqi-description (Div) - Displays descriptive AQI category.
  - pollution-details (Table) - Table showing PM2.5, PM10, NO2, O3 levels.
  - location-aqi-filter (Dropdown) - Filter AQI data by location.
  - health-recommendation (Div) - Health advisory based on AQI.
- Navigation Mappings:
  - location-aqi-filter -> reloads page filtered by selected location
- Context Variables Available:
  - aqi_data: dict {location_id: int, aqi_index: int, pm25: float, pm10: float, no2: float, o3: float, last_updated: str}
  - health_recommendation: str
  - location_filter_options: list[dict {location_id: int, location_name: str}]
- Usage Notes:
  - Data displayed updates by selected location filter.

### 7. Template: saved_locations.html
- File Path: templates/saved_locations.html
- Page Title: Saved Locations
- Element IDs and Descriptions:
  - saved-locations-page (Div) - Container for saved locations page.
  - locations-table (Table) - Displays saved locations with current temperature and condition.
  - view-location-weather-{location_id} (Button) - View weather for location; dynamic IDs.
  - remove-location-button-{location_id} (Button) - Remove saved location; dynamic IDs.
  - add-new-location-button (Button) - Add new location button.
- Navigation Mappings:
  - view-location-weather-{location_id} -> url_for('view_location_weather', location_id=location_id)
  - remove-location-button-{location_id} -> POST to url_for('remove_saved_location', location_id=location_id)
  - add-new-location-button -> url_for('location_search_page')
- Context Variables Available:
  - saved_locations: list[dict {location_id: int, location_name: str, temperature: float, condition: str}]
- Usage Notes:
  - Loops used to render table rows per saved location.
  - Buttons have dynamic IDs following location_id.

### 8. Template: settings.html
- File Path: templates/settings.html
- Page Title: Settings
- Element IDs and Descriptions:
  - settings-page (Div) - Container for settings page.
  - temperature-unit-select (Dropdown) - Select temperature unit (Celsius, Fahrenheit, Kelvin).
  - default-location-select (Dropdown) - Select default location.
  - alert-notifications-toggle (Checkbox) - Enable/disable alert notifications.
  - save-settings-button (Button) - Save settings button.
  - back-to-dashboard (Button) - Navigate back to dashboard.
- Navigation Mappings:
  - back-to-dashboard -> url_for('dashboard_page')
- Context Variables Available:
  - temperature_units: list[str] (e.g., ["Celsius", "Fahrenheit", "Kelvin"])
  - default_location_id: int
  - locations: list[dict {location_id: int, location_name: str}]
  - alert_notifications_enabled: bool
- Usage Notes:
  - Dropdowns pre-selected based on current settings.
  - Save button triggers POST to save settings.
  - Back button returns to dashboard.

---

## Section 3: Data File Schemas

### 1. current_weather.txt
- File Path: data/current_weather.txt
- Format (pipe-delimited, no headers):
  location_id|location_name|temperature|condition|humidity|wind_speed|last_updated
- Field Descriptions:
  - location_id: int, unique ID of the location
  - location_name: str, name of the location
  - temperature: float, current temperature (assumed Fahrenheit)
  - condition: str, weather condition description
  - humidity: int, humidity percentage
  - wind_speed: float, wind speed in mph
  - last_updated: str, date and time of last update in YYYY-MM-DD HH:mm format
- Example Lines:
  1|New York|72|Sunny|65|10|2025-01-20 14:30
  2|London|55|Rainy|80|15|2025-01-20 14:30
  3|Tokyo|45|Cloudy|72|8|2025-01-20 14:30

### 2. forecasts.txt
- File Path: data/forecasts.txt
- Format:
  forecast_id|location_id|date|high_temp|low_temp|condition|precipitation|humidity
- Field Descriptions:
  - forecast_id: int, unique forecast entry
  - location_id: int, ID of location
  - date: str, forecast date (YYYY-MM-DD)
  - high_temp: float, forecast high temperature
  - low_temp: float, forecast low temperature
  - condition: str, forecasted weather condition
  - precipitation: int, precipitation percentage
  - humidity: int, humidity percentage
- Example Lines:
  1|1|2025-01-21|75|60|Sunny|0|60
  2|1|2025-01-22|68|55|Cloudy|10|70
  3|2|2025-01-21|58|48|Rainy|80|85

### 3. locations.txt
- File Path: data/locations.txt
- Format:
  location_id|location_name|latitude|longitude|country|timezone
- Field Descriptions:
  - location_id: int, unique ID
  - location_name: str
  - latitude: float
  - longitude: float
  - country: str
  - timezone: str, e.g. EST, GMT
- Example Lines:
  1|New York|40.7128|-74.0060|USA|EST
  2|London|51.5074|-0.1278|UK|GMT
  3|Tokyo|35.6762|139.6503|Japan|JST

### 4. alerts.txt
- File Path: data/alerts.txt
- Format:
  alert_id|location_id|alert_type|severity|description|start_time|end_time|is_acknowledged
- Field Descriptions:
  - alert_id: int
  - location_id: int
  - alert_type: str, type of alert
  - severity: str (Critical, High, Medium, Low)
  - description: str
  - start_time: str (YYYY-MM-DD HH:mm)
  - end_time: str (YYYY-MM-DD HH:mm)
  - is_acknowledged: int (0 or 1; boolean false/true)
- Example Lines:
  1|1|Thunderstorm|High|Severe thunderstorm warning in effect until 8 PM|2025-01-20 14:00|2025-01-20 20:00|0
  2|2|Fog|Medium|Dense fog advisory in effect until noon tomorrow|2025-01-20 06:00|2025-01-21 12:00|0
  3|1|Wind|Medium|High wind advisory with gusts up to 45 mph|2025-01-20 15:00|2025-01-21 09:00|1

### 5. air_quality.txt
- File Path: data/air_quality.txt
- Format:
  aqi_id|location_id|aqi_index|pm25|pm10|no2|o3|last_updated
- Field Descriptions:
  - aqi_id: int, unique ID
  - location_id: int
  - aqi_index: int (0-500)
  - pm25: float, PM2.5 pollution level
  - pm10: float, PM10 pollution level
  - no2: float, Nitrogen Dioxide level
  - o3: float, Ozone level
  - last_updated: str (YYYY-MM-DD HH:mm)
- Example Lines:
  1|1|45|12.5|35|28|55|2025-01-20 14:30
  2|2|67|22.3|48|42|78|2025-01-20 14:30
  3|3|120|68.5|95|65|110|2025-01-20 14:30

### 6. saved_locations.txt
- File Path: data/saved_locations.txt
- Format:
  saved_id|user_id|location_id|location_name|is_default
- Field Descriptions:
  - saved_id: int, unique saved location record
  - user_id: int (though no auth, user 1 assumed)
  - location_id: int
  - location_name: str
  - is_default: int (0 or 1) indicating default saved location
- Example Lines:
  1|1|1|New York|1
  2|1|2|London|0
  3|2|3|Tokyo|1

---

**End of Design Specification Document**
