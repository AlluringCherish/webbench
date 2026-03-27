# WeatherForecast Web Application - Detailed Design Specification

---

## Section 1: Flask Routes Specification

---

### 1. Root Route
- URL Path: `/`
- HTTP Methods: GET
- Function Name: `root_redirect`
- Behavior: Redirects to `/dashboard`
- No template rendering; uses `redirect(url_for('dashboard'))`
- Context Variables: None

### 2. Dashboard Page
- URL Path: `/dashboard`
- HTTP Methods: GET
- Function Name: `dashboard`
- Template: `dashboard.html`
- Context Variables:
  - `saved_locations`: List[Dict] of {
      `saved_id`: int,
      `user_id`: int,
      `location_id`: int,
      `location_name`: str,
      `is_default`: bool
    }
  - `default_location_id`: int
  - `current_weather`: Dict{
      `location_id`: int,
      `location_name`: str,
      `temperature`: int or float,
      `condition`: str,
      `humidity`: int,
      `wind_speed`: int or float,
      `last_updated`: str
    }
  - `alerts`: List[Dict] of {
      `alert_id`: int,
      `location_id`: int,
      `alert_type`: str,
      `severity`: str,
      `description`: str,
      `start_time`: str,
      `end_time`: str,
      `is_acknowledged`: bool
    }
  - `forecast_list`: List[Dict] of {
      `forecast_id`: int,
      `location_id`: int,
      `date`: str (YYYY-MM-DD),
      `high_temp`: int or float,
      `low_temp`: int or float,
      `condition`: str,
      `precipitation`: int,
      `humidity`: int
    }
  - `air_quality`: Dict{
      `aqi_id`: int,
      `location_id`: int,
      `aqi_index`: int,
      `pm25`: float,
      `pm10`: float,
      `no2`: float,
      `o3`: float,
      `last_updated`: str
    }
  - `alerts_enabled`: bool

### 3. Current Weather Page
- URL Path: `/weather/current/<int:location_id>`
- HTTP Methods: GET
- Function Name: `current_weather`
- Template: `current_weather.html`
- Context Variables:
  - `location_name`: str
  - `current_weather`: Dict{
      `temperature`: int or float,
      `condition`: str,
      `humidity`: int,
      `wind_speed`: int or float,
      `last_updated`: str
    }

### 4. Weekly Forecast Page
- URL Path: `/weather/forecast/<int:location_id>`
- HTTP Methods: GET
- Function Name: `weekly_forecast`
- Template: `weekly_forecast.html`
- Context Variables:
  - `location_name`: str
  - `forecast_list`: List[Dict] of {
      `forecast_id`: int,
      `date`: str,
      `high_temp`: int or float,
      `low_temp`: int or float,
      `condition`: str,
      `precipitation`: int,
      `humidity`: int
    }

### 5. Location Search Page
- URL Path: `/search`
- HTTP Methods: GET, POST
- Function Name: `search_locations`
- Template: `search.html`
- Context Variables:
  - `search_results`: List[Dict] of {
      `location_id`: int,
      `location_name`: str,
      `latitude`: float,
      `longitude`: float,
      `country`: str,
      `timezone`: str
    }
  - `saved_locations`: List[Dict], same structure as in dashboard

### 6. Weather Alerts Page
- URL Path: `/alerts/<int:location_id>`
- HTTP Methods: GET
- Function Name: `alerts_page`
- Template: `alerts.html`
- Context Variables:
  - `alerts`: List[Dict], filtered by `location_id` and optionally `severity`, same structure as in dashboard
  - `location_filter_options`: List[Dict] of locations
  - `severity_filter_options`: List[str] with ['All', 'Critical', 'High', 'Medium', 'Low']
  - `selected_location_id`: int
  - `selected_severity`: str

### 7. Air Quality Page
- URL Path: `/air-quality/<int:location_id>`
- HTTP Methods: GET
- Function Name: `air_quality_page`
- Template: `air_quality.html`
- Context Variables:
  - `air_quality`: Dict, same structure as in dashboard
  - `location_name`: str
  - `aqi_description`: str
  - `health_recommendation`: str
  - `location_filter_options`: List of locations
  - `selected_location_id`: int

### 8. Saved Locations Page
- URL Path: `/saved-locations`
- HTTP Methods: GET
- Function Name: `saved_locations_page`
- Template: `saved_locations.html`
- Context Variables:
  - `saved_locations`: List[Dict], same structure as dashboard
  - `weather_summary_per_location`: Dict mapping location_id to current_weather Dict

### 9. Settings Page
- URL Path: `/settings`
- HTTP Methods: GET, POST
- Function Name: `settings_page`
- Template: `settings.html`
- Context Variables:
  - `temperature_unit`: str ("Celsius", "Fahrenheit", "Kelvin")
  - `default_location_id`: int
  - `alerts_enabled`: bool
  - `saved_locations`: List[Dict], as above

---

## Section 2: Frontend HTML Templates Specification

---

### 1. `templates/dashboard.html`
- Page Title: "Weather Dashboard"
- Main Heading: `<h1 id="dashboard-page">Weather Dashboard</h1>`
- Element IDs:
  - `dashboard-page` (Div container)
  - `current-weather-summary` (Div showing default location's current weather)
  - `search-location-button` (Button navigates to location search page)
  - `view-forecast-button` (Button navigates to weekly forecast page)
  - `view-alerts-button` (Button navigates to alerts page)
- Navigation:
  - `search-location-button` -> `search_locations`
  - `view-forecast-button` -> `weekly_forecast` with default location_id
  - `view-alerts-button` -> `alerts_page` with default location_id
- Context variables:
  - `saved_locations`, `default_location_id`, `current_weather`, `alerts_enabled`, `alerts`, `forecast_list`, `air_quality`
- Notes:
  - Dynamic elements generated for saved locations list with buttons having IDs `select-location-button-{location_id}` and `remove-location-button-{location_id}`.

### 2. `templates/current_weather.html`
- Page Title: "Current Weather"
- Elements:
  - Div.id=`current-weather-page`
  - H1.id=`location-name`
  - Divs with IDs: `temperature-display`, `weather-condition`, `humidity-info`, `wind-speed-info`
- Navigation:
  - Back button with ID `back-to-dashboard` links to `dashboard`
- Context:
  - `location_name`, `current_weather`

### 3. `templates/weekly_forecast.html`
- Page Title: "Weekly Forecast"
- Elements:
  - Div.id=`forecast-page`
  - Table.id=`forecast-table` with columns: Date, High Temp, Low Temp, Condition
  - Dropdown.id=`location-filter` to select/filter location
  - Div.id=`forecast-list` showing forecast cards
  - Button.id=`back-to-dashboard`
- Navigation:
  - `back-to-dashboard` routes to `dashboard`
- Context:
  - `location_name`, `forecast_list`
- Notes:
  - Use loops to iterate forecast_list

### 4. `templates/search.html`
- Page Title: "Search Locations"
- Elements:
  - Div.id=`search-page`
  - Input.id=`location-search-input`
  - Div.id=`search-results` lists matching locations
  - Buttons.id=`select-location-button-{location_id}` for each result
  - Div.id=`saved-locations-list` to display saved locations
- Navigation:
  - Search form submits to `search_locations`
- Context:
  - `search_results`, `saved_locations`

### 5. `templates/alerts.html`
- Page Title: "Weather Alerts"
- Elements:
  - Div.id=`alerts-page`
  - Div.id=`alerts-list` with alert entries
  - Dropdown.id=`severity-filter`
  - Dropdown.id=`location-filter-alerts`
  - Buttons.id=`acknowledge-alert-button-{alert_id}`
- Navigation:
  - Navigation back to `dashboard`
- Context:
  - `alerts`, `location_filter_options`, `severity_filter_options`, `selected_location_id`, `selected_severity`

### 6. `templates/air_quality.html`
- Page Title: "Air Quality Index"
- Elements:
  - Div.id=`air-quality-page`
  - Div.id=`aqi-display`
  - Div.id=`aqi-description`
  - Table.id=`pollution-details`
  - Dropdown.id=`location-aqi-filter`
  - Div.id=`health-recommendation`
- Navigation:
  - Navigation back to `dashboard`
- Context:
  - `air_quality`, `location_name`, `aqi_description`, `health_recommendation`, `location_filter_options`, `selected_location_id`

### 7. `templates/saved_locations.html`
- Page Title: "Saved Locations"
- Elements:
  - Div.id=`saved-locations-page`
  - Table.id=`locations-table`
  - Buttons.id=`view-location-weather-{location_id}`, `remove-location-button-{location_id}`
  - Button.id=`add-new-location-button`
- Navigation:
  - Navigation back to `dashboard`
- Context:
  - `saved_locations`, `weather_summary_per_location`

### 8. `templates/settings.html`
- Page Title: "Settings"
- Elements:
  - Div.id=`settings-page`
  - Dropdown.id=`temperature-unit-select`
  - Dropdown.id=`default-location-select`
  - Checkbox.id=`alert-notifications-toggle`
  - Button.id=`save-settings-button`
  - Button.id=`back-to-dashboard`
- Navigation:
  - Back button routes to `dashboard`
- Context:
  - `temperature_unit`, `default_location_id`, `alerts_enabled`, `saved_locations`

---

## Section 3: Data File Schemas

---

### 1. current_weather.txt
- File Path: `data/current_weather.txt`
- Fields (pipe-delimited): 
  `location_id|location_name|temperature|condition|humidity|wind_speed|last_updated`
- Field Descriptions:
  - `location_id`: int - Unique location identifier
  - `location_name`: str - Location city name
  - `temperature`: int/float - Current temperature (unit based on settings)
  - `condition`: str - Weather condition text
  - `humidity`: int - Percentage humidity
  - `wind_speed`: int/float - Wind speed in mph or kph
  - `last_updated`: str - Datetime in `YYYY-MM-DD HH:MM` format

- Example Lines:
  1|New York|72|Sunny|65|10|2025-01-20 14:30
  2|London|55|Rainy|80|15|2025-01-20 14:30
  3|Tokyo|45|Cloudy|72|8|2025-01-20 14:30

### 2. forecasts.txt
- File Path: `data/forecasts.txt`
- Fields:
  `forecast_id|location_id|date|high_temp|low_temp|condition|precipitation|humidity`
- Field Descriptions:
  - `forecast_id`: int
  - `location_id`: int
  - `date`: str in `YYYY-MM-DD`
  - `high_temp`, `low_temp`: int/float
  - `condition`: str
  - `precipitation`: int - percentage precipitation chance
  - `humidity`: int - percentage humidity

- Example Lines:
  1|1|2025-01-21|75|60|Sunny|0|60
  2|1|2025-01-22|68|55|Cloudy|10|70
  3|2|2025-01-21|58|48|Rainy|80|85

### 3. locations.txt
- File Path: `data/locations.txt`
- Fields:
  `location_id|location_name|latitude|longitude|country|timezone`
- Field Descriptions:
  - `location_id`: int
  - `location_name`: str
  - `latitude`: float
  - `longitude`: float
  - `country`: str
  - `timezone`: str

- Example Lines:
  1|New York|40.7128|-74.0060|USA|EST
  2|London|51.5074|-0.1278|UK|GMT
  3|Tokyo|35.6762|139.6503|Japan|JST

### 4. alerts.txt
- File Path: `data/alerts.txt`
- Fields:
  `alert_id|location_id|alert_type|severity|description|start_time|end_time|is_acknowledged`
- Field Descriptions:
  - `alert_id`: int
  - `location_id`: int
  - `alert_type`: str
  - `severity`: str ('Low', 'Medium', 'High', 'Critical')
  - `description`: str
  - `start_time`: str, datetime `YYYY-MM-DD HH:MM`
  - `end_time`: str, datetime `YYYY-MM-DD HH:MM`
  - `is_acknowledged`: bool (0 or 1)

- Example Lines:
  1|1|Thunderstorm|High|Severe thunderstorm warning in effect until 8 PM|2025-01-20 14:00|2025-01-20 20:00|0
  2|2|Fog|Medium|Dense fog advisory in effect until noon tomorrow|2025-01-20 06:00|2025-01-21 12:00|0
  3|1|Wind|Medium|High wind advisory with gusts up to 45 mph|2025-01-20 15:00|2025-01-21 09:00|1

### 5. air_quality.txt
- File Path: `data/air_quality.txt`
- Fields:
  `aqi_id|location_id|aqi_index|pm25|pm10|no2|o3|last_updated`
- Field Descriptions:
  - `aqi_id`: int
  - `location_id`: int
  - `aqi_index`: int (range 0 - 500)
  - `pm25`, `pm10`, `no2`, `o3`: float
  - `last_updated`: str, datetime `YYYY-MM-DD HH:MM`

- Example Lines:
  1|1|45|12.5|35|28|55|2025-01-20 14:30
  2|2|67|22.3|48|42|78|2025-01-20 14:30
  3|3|120|68.5|95|65|110|2025-01-20 14:30

### 6. saved_locations.txt
- File Path: `data/saved_locations.txt`
- Fields:
  `saved_id|user_id|location_id|location_name|is_default`
- Field Descriptions:
  - `saved_id`: int
  - `user_id`: int
  - `location_id`: int
  - `location_name`: str
  - `is_default`: bool (1 or 0)

- Example Lines:
  1|1|1|New York|1
  2|1|2|London|0
  3|2|3|Tokyo|1

---

# End of Design Specification