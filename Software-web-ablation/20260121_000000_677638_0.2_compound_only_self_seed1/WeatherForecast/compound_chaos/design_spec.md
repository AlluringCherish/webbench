# Design Specification Document for WeatherForecast Application

---

## Section 1: Flask Routes Specification

### 1. Root Route
- URL Path: `/`
- Allowed HTTP Methods: GET
- Function Name: `root_redirect`
- Template: None (Redirects to `/dashboard`)
- Context Variables: None

### 2. Dashboard Page
- URL Path: `/dashboard`
- Allowed HTTP Methods: GET
- Function Name: `dashboard`
- Template Filename: `dashboard.html`
- Context Variables:
  - `current_weather`: dict {
    location_id: int,
    location_name: str,
    temperature: float,
    condition: str,
    humidity: int,
    wind_speed: float,
    last_updated: str (format "YYYY-MM-DD HH:MM")
  }

### 3. Current Weather Page
- URL Path: `/weather/current/<int:location_id>`
- Allowed HTTP Methods: GET
- Function Name: `current_weather`
- Template Filename: `current_weather.html`
- Context Variables:
  - `location_name`: str
  - `temperature`: float
  - `condition`: str
  - `humidity`: int
  - `wind_speed`: float

### 4. Weekly Forecast Page
- URL Path: `/forecast/weekly`
- Allowed HTTP Methods: GET
- Function Name: `weekly_forecast`
- Template Filename: `weekly_forecast.html`
- Context Variables:
  - `forecasts`: list of dict {
    forecast_id: int,
    location_id: int,
    date: str ("YYYY-MM-DD"),
    high_temp: float,
    low_temp: float,
    condition: str,
    precipitation: int,
    humidity: int
  }
  - `locations`: list of dict {
    location_id: int,
    location_name: str
  }
  - `selected_location_id`: int or None

### 5. Location Search Page
- URL Path: `/locations/search`
- Allowed HTTP Methods: GET, POST
- Function Name: `location_search`
- Template Filename: `location_search.html`
- Context Variables:
  - `search_query`: str (optional, for POST requests)
  - `search_results`: list of dict {
    location_id: int,
    location_name: str,
    latitude: float,
    longitude: float,
    country: str,
    timezone: str
  }
  - `saved_locations`: list of dict {
    location_id: int,
    location_name: str
  }
  - `selected_location_id`: int or None

### 6. Weather Alerts Page
- URL Path: `/alerts`
- Allowed HTTP Methods: GET
- Function Name: `weather_alerts`
- Template Filename: `alerts.html`
- Context Variables:
  - `alerts`: list of dict {
    alert_id: int,
    location_id: int,
    alert_type: str,
    severity: str (One of: 'All', 'Critical', 'High', 'Medium', 'Low'),
    description: str,
    start_time: str ("YYYY-MM-DD HH:MM"),
    end_time: str ("YYYY-MM-DD HH:MM"),
    is_acknowledged: bool
  }
  - `severity_filter`: str
  - `location_filter`: int or None

### 7. Acknowledge Alert Route
- URL Path: `/alerts/acknowledge/<int:alert_id>`
- Allowed HTTP Methods: POST
- Function Name: `acknowledge_alert`
- Template Filename: None (no template, redirect or JSON response)
- Context Variables:
  - `alert_id`: int (from URL parameter)

### 8. Air Quality Page
- URL Path: `/airquality`
- Allowed HTTP Methods: GET
- Function Name: `air_quality_page`
- Template Filename: `air_quality.html`
- Context Variables:
  - `air_quality_data`: list of dict {
    aqi_id: int,
    location_id: int,
    aqi_index: int,
    pm25: float,
    pm10: float,
    no2: float,
    o3: float,
    last_updated: str ("YYYY-MM-DD HH:MM")
  }
  - `locations`: list of dict {
    location_id: int,
    location_name: str
  }
  - `selected_location_id`: int or None
  - `health_recommendation`: str

### 9. Saved Locations Page
- URL Path: `/locations/saved`
- Allowed HTTP Methods: GET
- Function Name: `saved_locations`
- Template Filename: `saved_locations.html`
- Context Variables:
  - `saved_locations`: list of dict {
    saved_id: int,
    user_id: int (always 1 as no authentication),
    location_id: int,
    location_name: str,
    is_default: bool
  }
  - `current_weather_map`: dict mapping location_id (int) to dict {
    temperature: float,
    condition: str
  }

### 10. Settings Page
- URL Path: `/settings`
- Allowed HTTP Methods: GET, POST
- Function Name: `settings`
- Template Filename: `settings.html`
- Context Variables:
  - `temperature_unit`: str (One of: 'Celsius', 'Fahrenheit', 'Kelvin')
  - `default_location_id`: int
  - `alert_notifications_enabled`: bool
  - `locations`: list of dict {
    location_id: int,
    location_name: str
  }

---

## Section 2: Frontend HTML Templates Specification

### Template: `templates/dashboard.html`
- Page Title: "Weather Dashboard"
- Main Heading: `<h1>` or included within page container with ID `dashboard-page`
- Element IDs:
  - `dashboard-page` (Div): container
  - `current-weather-summary` (Div): Displays current weather conditions
  - `search-location-button` (Button): Navigates to location search page
  - `view-forecast-button` (Button): Navigates to weekly forecast page
  - `view-alerts-button` (Button): Navigates to alerts page
- Navigation Mappings:
  - `search-location-button` -> `url_for('location_search')`
  - `view-forecast-button` -> `url_for('weekly_forecast')`
  - `view-alerts-button` -> `url_for('weather_alerts')`
- Context Variables:
  - `current_weather` (dict) as described
- Usage Notes: Render current weather details within `current-weather-summary` div

### Template: `templates/current_weather.html`
- Page Title: "Current Weather"
- Main Heading: `<h1 id="location-name">{{ location_name }}</h1>`
- Element IDs:
  - `current-weather-page` (Div): page container
  - `location-name` (H1): displays location name
  - `temperature-display` (Div): displays temperature
  - `weather-condition` (Div): displays weather condition
  - `humidity-info` (Div): displays humidity percentage
  - `wind-speed-info` (Div): displays wind speed
- Navigation: No explicit navigation; optional back button inside frontend UI
- Context Variables:
  - `location_name` (str)
  - `temperature` (float)
  - `condition` (str)
  - `humidity` (int)
  - `wind_speed` (float)
- Usage Notes: Populate respective elements with context variables

### Template: `templates/weekly_forecast.html`
- Page Title: "Weekly Forecast"
- Main Heading: `<h1>Weekly Forecast</h1>`
- Element IDs:
  - `forecast-page` (Div): page container
  - `forecast-table` (Table): daily forecast rows (date, high_temp, low_temp, condition)
  - `location-filter` (Dropdown): filter forecasts by location
  - `forecast-list` (Div): grid to display forecast cards
  - `back-to-dashboard` (Button): navigates to dashboard
- Navigation Mappings:
  - `location-filter` triggers reload/filtering
  - `back-to-dashboard` -> `url_for('dashboard')`
- Context Variables:
  - `forecasts`: list of forecast dicts
  - `locations`: list of location dicts
  - `selected_location_id`: int or None
- Usage Notes: Loop through `forecasts` to render data

### Template: `templates/location_search.html`
- Page Title: "Search Locations"
- Main Heading: `<h1>Search Locations</h1>`
- Element IDs:
  - `search-page` (Div): container
  - `location-search-input` (Input): search field
  - `search-results` (Div): displays results
  - `select-location-button-{location_id}` (Button): dynamic ID for each result button
  - `saved-locations-list` (Div): previously saved locations
- Navigation Mappings:
  - Each `select-location-button-{location_id}` triggers POST to select location
- Context Variables:
  - `search_query`: str
  - `search_results`: list of location dicts
  - `saved_locations`: list of saved location dicts
- Usage Notes: Loop over search results and saved locations rendering buttons

### Template: `templates/alerts.html`
- Page Title: "Weather Alerts"
- Main Heading: `<h1>Weather Alerts</h1>`
- Element IDs:
  - `alerts-page` (Div): container
  - `alerts-list` (Div): list of alerts
  - `severity-filter` (Dropdown): filter alerts by severity
  - `location-filter-alerts` (Dropdown): filter alerts by location
  - `acknowledge-alert-button-{alert_id}` (Button): dynamic ID for acknowledge button
- Navigation Mappings:
  - `acknowledge-alert-button-{alert_id}` triggers POST to `/alerts/acknowledge/<alert_id>`
- Context Variables:
  - `alerts`: list of alert dicts
  - `severity_filter`: str
  - `location_filter`: int or None
- Usage Notes: Loop alerts list to show alerts

### Template: `templates/air_quality.html`
- Page Title: "Air Quality Index"
- Main Heading: `<h1>Air Quality Index</h1>`
- Element IDs:
  - `air-quality-page` (Div): container
  - `aqi-display` (Div): shows AQI numeric value
  - `aqi-description` (Div): AQI description
  - `pollution-details` (Table): pollutant levels shown
  - `location-aqi-filter` (Dropdown): filter by location
  - `health-recommendation` (Div): health advice
- Navigation Mappings:
  - `location-aqi-filter` triggers refresh
- Context Variables:
  - `air_quality_data`: list of dicts
  - `locations`: list of dicts
  - `selected_location_id`: int or None
  - `health_recommendation`: str
- Usage Notes: Render pollutant data in table rows

### Template: `templates/saved_locations.html`
- Page Title: "Saved Locations"
- Main Heading: `<h1>Saved Locations</h1>`
- Element IDs:
  - `saved-locations-page` (Div): container
  - `locations-table` (Table): saved locations with current weather
  - `view-location-weather-{location_id}` (Button): dynamic ID to view weather
  - `remove-location-button-{location_id}` (Button): dynamic ID to remove location
  - `add-new-location-button` (Button): button to add new location
- Navigation Mappings:
  - `view-location-weather-{location_id}` -> `url_for('current_weather', location_id=location_id)`
  - `remove-location-button-{location_id}` triggers delete action
  - `add-new-location-button` -> `url_for('location_search')`
- Context Variables:
  - `saved_locations`: list of dicts
  - `current_weather_map`: dict mapping location_ids to weather status
- Usage Notes: Loop through saved locations for table rows

### Template: `templates/settings.html`
- Page Title: "Settings"
- Main Heading: `<h1>Settings</h1>`
- Element IDs:
  - `settings-page` (Div): container
  - `temperature-unit-select` (Dropdown): select temperature unit
  - `default-location-select` (Dropdown): select default location
  - `alert-notifications-toggle` (Checkbox): toggle alert notifications
  - `save-settings-button` (Button): save button
  - `back-to-dashboard` (Button): navigate to dashboard
- Navigation Mappings:
  - `save-settings-button` submits form (POST)
  - `back-to-dashboard` -> `url_for('dashboard')`
- Context Variables:
  - `temperature_unit`: str
  - `default_location_id`: int
  - `alert_notifications_enabled`: bool
  - `locations`: list of dict
- Usage Notes: Bind and render settings appropriately

---

## Section 3: Data File Schemas

### 1. Current Weather Data
- File Path: `data/current_weather.txt`
- Fields (pipe-delimited in order):
  1. `location_id` (int) - Unique identifier
  2. `location_name` (str) - Location name
  3. `temperature` (float) - Current temperature
  4. `condition` (str) - Weather condition
  5. `humidity` (int) - Humidity percentage
  6. `wind_speed` (float) - Wind speed
  7. `last_updated` (str) - Timestamp "YYYY-MM-DD HH:MM"
- Example Data:
```
1|New York|72|Sunny|65|10|2025-01-20 14:30
2|London|55|Rainy|80|15|2025-01-20 14:30
3|Tokyo|45|Cloudy|72|8|2025-01-20 14:30
```

### 2. Forecasts Data
- File Path: `data/forecasts.txt`
- Fields:
  1. `forecast_id` (int)
  2. `location_id` (int)
  3. `date` (str) - "YYYY-MM-DD"
  4. `high_temp` (float)
  5. `low_temp` (float)
  6. `condition` (str)
  7. `precipitation` (int)
  8. `humidity` (int)
- Example Data:
```
1|1|2025-01-21|75|60|Sunny|0|60
2|1|2025-01-22|68|55|Cloudy|10|70
3|2|2025-01-21|58|48|Rainy|80|85
```

### 3. Locations Data
- File Path: `data/locations.txt`
- Fields:
  1. `location_id` (int)
  2. `location_name` (str)
  3. `latitude` (float)
  4. `longitude` (float)
  5. `country` (str)
  6. `timezone` (str)
- Example Data:
```
1|New York|40.7128|-74.0060|USA|EST
2|London|51.5074|-0.1278|UK|GMT
3|Tokyo|35.6762|139.6503|Japan|JST
```

### 4. Weather Alerts Data
- File Path: `data/alerts.txt`
- Fields:
  1. `alert_id` (int)
  2. `location_id` (int)
  3. `alert_type` (str)
  4. `severity` (str)
  5. `description` (str)
  6. `start_time` (str, "YYYY-MM-DD HH:MM")
  7. `end_time` (str, "YYYY-MM-DD HH:MM")
  8. `is_acknowledged` (int, 0 or 1)
- Example Data:
```
1|1|Thunderstorm|High|Severe thunderstorm warning in effect until 8 PM|2025-01-20 14:00|2025-01-20 20:00|0
2|2|Fog|Medium|Dense fog advisory in effect until noon tomorrow|2025-01-20 06:00|2025-01-21 12:00|0
3|1|Wind|Medium|High wind advisory with gusts up to 45 mph|2025-01-20 15:00|2025-01-21 09:00|1
```

### 5. Air Quality Data
- File Path: `data/air_quality.txt`
- Fields:
  1. `aqi_id` (int)
  2. `location_id` (int)
  3. `aqi_index` (int, 0-500)
  4. `pm25` (float)
  5. `pm10` (float)
  6. `no2` (float)
  7. `o3` (float)
  8. `last_updated` (str, "YYYY-MM-DD HH:MM")
- Example Data:
```
1|1|45|12.5|35|28|55|2025-01-20 14:30
2|2|67|22.3|48|42|78|2025-01-20 14:30
3|3|120|68.5|95|65|110|2025-01-20 14:30
```

### 6. Saved Locations Data
- File Path: `data/saved_locations.txt`
- Fields:
  1. `saved_id` (int)
  2. `user_id` (int)
  3. `location_id` (int)
  4. `location_name` (str)
  5. `is_default` (int, 0 or 1)
- Example Data:
```
1|1|1|New York|1
2|1|2|London|0
3|2|3|Tokyo|1
```

---

End of Design Specification
