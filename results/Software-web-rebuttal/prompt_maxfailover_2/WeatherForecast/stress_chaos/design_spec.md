# WeatherForecast Application - Design Specification

---

## Section 1: Backend Flask Routes Specification

### Route: `/`
- URL Path: `/`
- HTTP Methods: GET
- Function Name: `redirect_to_dashboard`
- Template: None (Redirect)
- Description: Redirects the root URL to the dashboard page `/dashboard`.
- Context Variables: None

---

### Route: `/dashboard`
- URL Path: `/dashboard`
- HTTP Methods: GET
- Function Name: `dashboard`
- Template: `dashboard.html`
- Description: Displays the Weather Dashboard page showing current weather summary for the default or saved locations, and navigation buttons.
- Context Variables:
  - `default_location` (Dict[str, any]): Details of the default location.
    - Fields:
      - `location_id` (int)
      - `location_name` (str)
      - `latitude` (float)
      - `longitude` (float)
      - `country` (str)
      - `timezone` (str)
  - `current_weather` (Dict[str, any]): Current weather data for the default location.
    - Fields:
      - `location_name` (str)
      - `temperature` (int)
      - `condition` (str)
      - `humidity` (int)
      - `wind_speed` (int)
      - `last_updated` (str) (Format: 'YYYY-MM-DD HH:MM')

---

### Route: `/weather/current/<int:location_id>`
- URL Path: `/weather/current/<int:location_id>`
- HTTP Methods: GET
- Function Name: `current_weather_page`
- Template: `current_weather.html`
- Description: Shows detailed current weather information for the selected location.
- Context Variables:
  - `location` (Dict[str, any]): Location details as above.
  - `temperature` (int)
  - `condition` (str)
  - `humidity` (int)
  - `wind_speed` (int)
  - `last_updated` (str)

---

### Route: `/weather/forecast/<int:location_id>`
- URL Path: `/weather/forecast/<int:location_id>`
- HTTP Methods: GET
- Function Name: `weekly_forecast_page`
- Template: `weekly_forecast.html`
- Description: Displays weekly weather forecast for the selected location.
- Context Variables:
  - `location` (Dict[str, any]): Location details.
  - `forecasts` (List[Dict[str, any]]): List of daily forecast entries.
    - Each forecast dict contains:
      - `forecast_id` (int)
      - `date` (str) (Format: 'YYYY-MM-DD')
      - `high_temp` (int)
      - `low_temp` (int)
      - `condition` (str)
      - `precipitation` (int) (percent)
      - `humidity` (int) (percent)

---

### Route: `/search`
- URL Path: `/search`
- HTTP Methods: GET
- Function Name: `search_locations_page`
- Template: `search_locations.html`
- Description: Allows the user to search for locations by name or coordinates.
- Context Variables:
  - `search_results` (List[Dict[str, any]]): Matching locations.
    - Fields per location:
      - `location_id` (int)
      - `location_name` (str)
      - `latitude` (float)
      - `longitude` (float)
      - `country` (str)
      - `timezone` (str)
  - `saved_locations` (List[Dict[str, any]]): Previously saved locations by the user.

---

### Route: `/alerts`
- URL Path: `/alerts`
- HTTP Methods: GET
- Function Name: `weather_alerts_page`
- Template: `alerts.html`
- Description: Displays active weather alerts for locations.
- Context Variables:
  - `alerts` (List[Dict[str, any]]): List of current alerts.
    - Each alert dict fields:
      - `alert_id` (int)
      - `location_id` (int)
      - `alert_type` (str)
      - `severity` (str)
      - `description` (str)
      - `start_time` (str) (Format: 'YYYY-MM-DD HH:MM')
      - `end_time` (str) (Format: 'YYYY-MM-DD HH:MM')
      - `is_acknowledged` (bool)

---

### Route: `/air_quality/<int:location_id>`
- URL Path: `/air_quality/<int:location_id>`
- HTTP Methods: GET
- Function Name: `air_quality_page`
- Template: `air_quality.html`
- Description: Shows air quality index and pollutant details for a location.
- Context Variables:
  - `location` (Dict[str, any])
  - `aqi_index` (int)
  - `aqi_description` (str)
  - `pollutants` (Dict[str, float]): PM2.5, PM10, NO2, O3 values.
  - `last_updated` (str)
  - `health_recommendation` (str)

---

### Route: `/saved_locations`
- URL Path: `/saved_locations`
- HTTP Methods: GET
- Function Name: `saved_locations_page`
- Template: `saved_locations.html`
- Description: Display user's saved locations with quick access buttons.
- Context Variables:
  - `saved_locations` (List[Dict[str, any]]):
    - `saved_id` (int)
    - `user_id` (int) (even if no authentication, can be '1')
    - `location_id` (int)
    - `location_name` (str)
    - `is_default` (bool)

---

### Route: `/settings`
- URL Path: `/settings`
- HTTP Methods: GET, POST
- Function Name: `settings_page`
- Template: `settings.html`
- Description: Allow the user to update settings including temperature unit, default location, and alert notifications.
- Context Variables (GET):
  - `temperature_unit` (str) (e.g., 'Celsius', 'Fahrenheit', 'Kelvin')
  - `default_location` (int)
  - `alert_notifications` (bool)

---

## Section 2: Frontend HTML Templates Specification

### Template: `dashboard.html`
- File Path: `templates/dashboard.html`
- Page Title: "Weather Dashboard"
- Elements:
  - Div `dashboard-page`: Container for the entire dashboard.
  - Div `current-weather-summary`: Displays current weather summary for the default location.
  - Button `search-location-button`: Navigates to Search Locations page.
  - Button `view-forecast-button`: Navigates to Weekly Forecast page for default location.
  - Button `view-alerts-button`: Navigates to Weather Alerts page.

- Navigation Mappings:
  - `search-location-button`: calls `url_for('search_locations_page')`
  - `view-forecast-button`: calls `url_for('weekly_forecast_page', location_id=default_location['location_id'])`
  - `view-alerts-button`: calls `url_for('weather_alerts_page')`

- Context Variables Available:
  - `default_location` (Dict)
  - `current_weather` (Dict)

- Dynamic Rendering Notes:
  - `current-weather-summary` shows data such as temperature, condition, humidity, wind speed.

---

### Template: `current_weather.html`
- File Path: `templates/current_weather.html`
- Page Title: "Current Weather"
- Elements:
  - Div `current-weather-page`: Container.
  - H1 `location-name`: Shows location name.
  - Div `temperature-display`: Current temperature.
  - Div `weather-condition`: Current condition description.
  - Div `humidity-info`: Humidity percentage.
  - Div `wind-speed-info`: Wind speed.

- Navigation Mappings:
  - No explicit navigation buttons by spec, but navigation likely back elsewhere available.

- Context Variables:
  - `location` (Dict)
  - `temperature` (int)
  - `condition` (str)
  - `humidity` (int)
  - `wind_speed` (int)
  - `last_updated` (str)

- Dynamic Rendering Notes: All values displayed dynamically.

---

### Template: `weekly_forecast.html`
- File Path: `templates/weekly_forecast.html`
- Page Title: "Weekly Forecast"
- Elements:
  - Div `forecast-page`: Container
  - Dropdown `location-filter`: To select location filter.
  - Table `forecast-table`: Displays daily forecasts.
  - Div `forecast-list`: Grid of forecast cards.
  - Button `back-to-dashboard`: Navigate back.

- Navigation Mappings:
  - `back-to-dashboard`: calls `url_for('dashboard')`

- Context Variables:
  - `location` (Dict)
  - `forecasts` (List[Dict])

- Dynamic Rendering:
  - Loop over `forecasts` to render rows/cards.
  - Location filter dropdown dynamically loads locations.

---

### Template: `search_locations.html`
- File Path: `templates/search_locations.html`
- Page Title: "Search Locations"
- Elements:
  - Div `search-page`: Container
  - Input `location-search-input`: Text box for search query.
  - Div `search-results`: Container showing search results.
  - Multiple Buttons `select-location-button-{location_id}`: To select and add a saved location.
  - Div `saved-locations-list`: Display already saved locations.

- Navigation Mappings:
  - Each `select-location-button-{location_id}` calls `url_for` to add location (route name assumed `add_saved_location`, accepting location_id)

- Context Variables:
  - `search_results` (List[Dict])
  - `saved_locations` (List[Dict])

- Dynamic Rendering:
  - Loop `search_results` to show matching locations.
  - Loop `saved_locations` to show existing saved list.

---

### Template: `alerts.html`
- File Path: `templates/alerts.html`
- Page Title: "Weather Alerts"
- Elements:
  - Div `alerts-page`: Container
  - Dropdown `severity-filter`: Filter alerts by severity.
  - Dropdown `location-filter-alerts`: Filter alerts by location.
  - Div `alerts-list`: List of alert entries.
  - Multiple Buttons `acknowledge-alert-button-{alert_id}`: Button to acknowledge alert.

- Navigation Mappings:
  - Buttons link to route that handles acknowledgment (route name assumed `acknowledge_alert`, parameter alert_id)

- Context Variables:
  - `alerts` (List[Dict])

- Dynamic Rendering:
  - Loop over `alerts` to render each alert.
  - Filter dropdowns used to refine displayed alerts.

---

### Template: `air_quality.html`
- File Path: `templates/air_quality.html`
- Page Title: "Air Quality Index"
- Elements:
  - Div `air-quality-page`: Container
  - Div `aqi-display`: Shows numeric AQI value.
  - Div `aqi-description`: Textual AQI description.
  - Table `pollution-details`: Pollutant levels (PM2.5, PM10, NO2, O3).
  - Dropdown `location-aqi-filter`: Filter by location.
  - Div `health-recommendation`: Health advice based on current AQI.

- Context Variables:
  - `location` (Dict)
  - `aqi_index` (int)
  - `aqi_description` (str)
  - `pollutants` (Dict[str, float])
  - `last_updated` (str)
  - `health_recommendation` (str)

- Dynamic Rendering:
  - Pollutant levels dynamically listed.
  - Dropdown filters AQI display.

---

### Template: `saved_locations.html`
- File Path: `templates/saved_locations.html`
- Page Title: "Saved Locations"
- Elements:
  - Div `saved-locations-page`: Container
  - Table `locations-table`: Lists saved locations.
  - Multiple Buttons `view-location-weather-{location_id}`: View weather per location.
  - Multiple Buttons `remove-location-button-{location_id}`: Remove location.
  - Button `add-new-location-button`: Add new location.

- Navigation Mappings:
  - `view-location-weather-{location_id}`: Calls `url_for('current_weather_page', location_id=location_id)`
  - `remove-location-button-{location_id}`: Calls route to remove location (route name assumed `remove_saved_location`)
  - `add-new-location-button`: Calls `url_for('search_locations_page')`

- Context Variables:
  - `saved_locations` (List[Dict])

- Dynamic Rendering:
  - Loop over `saved_locations` to generate table rows with controls.

---

### Template: `settings.html`
- File Path: `templates/settings.html`
- Page Title: "Settings"
- Elements:
  - Div `settings-page`: Container
  - Dropdown `temperature-unit-select`: Options Celsius, Fahrenheit, Kelvin.
  - Dropdown `default-location-select`: Select default location.
  - Checkbox `alert-notifications-toggle`: Enable or disable alert notifications.
  - Button `save-settings-button`: Save settings action.
  - Button `back-to-dashboard`: Return to dashboard.

- Navigation Mappings:
  - `back-to-dashboard`: Calls `url_for('dashboard')`

- Context Variables:
  - `temperature_unit` (str)
  - `default_location` (int)
  - `alert_notifications` (bool)

- Dynamic Rendering:
  - Set dropdowns and checkbox based on current settings.


---

## Section 3: Data File Schemas

All data files are pipe-delimited text files stored in the `data/` directory. No header lines present (parsing begins at first data line).

### 1. `data/current_weather.txt`
- Fields: 
  `location_id|location_name|temperature|condition|humidity|wind_speed|last_updated`
- Field Descriptions:
  - `location_id` (int): Unique ID of the location.
  - `location_name` (str): Name of the location.
  - `temperature` (int): Temperature in degrees Fahrenheit.
  - `condition` (str): Weather condition description (e.g., Sunny, Rainy).
  - `humidity` (int): Humidity percentage.
  - `wind_speed` (int): Wind speed in mph.
  - `last_updated` (str): Timestamp in `YYYY-MM-DD HH:MM` format.

- Example Data Lines:
```
1|New York|72|Sunny|65|10|2025-01-20 14:30
2|London|55|Rainy|80|15|2025-01-20 14:30
3|Tokyo|45|Cloudy|72|8|2025-01-20 14:30
```

---

### 2. `data/forecasts.txt`
- Fields:
  `forecast_id|location_id|date|high_temp|low_temp|condition|precipitation|humidity`
- Field Descriptions:
  - `forecast_id` (int): Unique forecast entry ID.
  - `location_id` (int): Location ID.
  - `date` (str): Forecast date in `YYYY-MM-DD` format.
  - `high_temp` (int): High temperature.
  - `low_temp` (int): Low temperature.
  - `condition` (str): Weather condition.
  - `precipitation` (int): Probability of precipitation in percent.
  - `humidity` (int): Humidity percentage.

- Example Data Lines:
```
1|1|2025-01-21|75|60|Sunny|0|60
2|1|2025-01-22|68|55|Cloudy|10|70
3|2|2025-01-21|58|48|Rainy|80|85
```

---

### 3. `data/locations.txt`
- Fields:
  `location_id|location_name|latitude|longitude|country|timezone`
- Field Descriptions:
  - `location_id` (int): Unique location ID.
  - `location_name` (str): Name of location.
  - `latitude` (float): Latitude coordinate.
  - `longitude` (float): Longitude coordinate.
  - `country` (str): Country name.
  - `timezone` (str): Timezone abbreviation.

- Example Data Lines:
```
1|New York|40.7128|-74.0060|USA|EST
2|London|51.5074|-0.1278|UK|GMT
3|Tokyo|35.6762|139.6503|Japan|JST
```

---

### 4. `data/alerts.txt`
- Fields:
  `alert_id|location_id|alert_type|severity|description|start_time|end_time|is_acknowledged`
- Field Descriptions:
  - `alert_id` (int): Unique alert ID.
  - `location_id` (int): Location ID.
  - `alert_type` (str): Type of alert (Thunderstorm, Fog, etc).
  - `severity` (str): Severity level (All, Critical, High, Medium, Low).
  - `description` (str): Description text.
  - `start_time` (str): Start time `YYYY-MM-DD HH:MM`.
  - `end_time` (str): End time `YYYY-MM-DD HH:MM`.
  - `is_acknowledged` (int): 0 = not acknowledged, 1 = acknowledged.

- Example Data Lines:
```
1|1|Thunderstorm|High|Severe thunderstorm warning in effect until 8 PM|2025-01-20 14:00|2025-01-20 20:00|0
2|2|Fog|Medium|Dense fog advisory in effect until noon tomorrow|2025-01-20 06:00|2025-01-21 12:00|0
3|1|Wind|Medium|High wind advisory with gusts up to 45 mph|2025-01-20 15:00|2025-01-21 09:00|1
```

---

### 5. `data/air_quality.txt`
- Fields:
  `aqi_id|location_id|aqi_index|pm25|pm10|no2|o3|last_updated`
- Field Descriptions:
  - `aqi_id` (int): AQI record ID.
  - `location_id` (int): Location ID.
  - `aqi_index` (int): Air Quality Index number ranging 0-500.
  - `pm25` (float): PM2.5 particulate level.
  - `pm10` (float): PM10 particulate level.
  - `no2` (float): Nitrogen dioxide level.
  - `o3` (float): Ozone level.
  - `last_updated` (str): Timestamp `YYYY-MM-DD HH:MM`.

- Example Data Lines:
```
1|1|45|12.5|35|28|55|2025-01-20 14:30
2|2|67|22.3|48|42|78|2025-01-20 14:30
3|3|120|68.5|95|65|110|2025-01-20 14:30
```

---

### 6. `data/saved_locations.txt`
- Fields:
  `saved_id|user_id|location_id|location_name|is_default`
- Field Descriptions:
  - `saved_id` (int): Saved location unique record ID.
  - `user_id` (int): User ID (all users can be id=1 due to no auth).
  - `location_id` (int): Location ID.
  - `location_name` (str): Location name.
  - `is_default` (int): 0 = not default, 1 = default location.

- Example Data Lines:
```
1|1|1|New York|1
2|1|2|London|0
3|2|3|Tokyo|1
```

---

This concludes the detailed design specification for the WeatherForecast application backend route definitions, frontend HTML templates, and data file schemas as per user_task_description.
