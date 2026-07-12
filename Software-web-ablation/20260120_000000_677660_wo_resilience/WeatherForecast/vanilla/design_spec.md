# Design Specification Document for WeatherForecast Web Application

---

## Section 1: Flask Routes Specification

| URL Path                       | HTTP Methods | Function Name         | Template Filename               | Context Variables (name: type)                                                                                                         |
|-------------------------------|--------------|-----------------------|-------------------------------|----------------------------------------------------------------------------------------------------------------------------------------|
| /                             | GET          | root_redirect          | None (redirects to /dashboard) | None                                                                                                                                   |
| /dashboard                    | GET          | dashboard              | dashboard.html                 | current_weather: dict{location_id: int, location_name: str, temperature: int, condition: str, humidity: int, wind_speed: int, last_updated: str}                                                               |
| /weather/current/<int:location_id> | GET          | current_weather        | current_weather.html           | weather: dict{location_id: int, location_name: str, temperature: int, condition: str, humidity: int, wind_speed: int, last_updated: str}                                                  |
| /forecast/weekly              | GET          | weekly_forecast        | weekly_forecast.html           | location_list: list[dict{location_id: int, location_name: str}],
  selected_location_id: int,  
  forecast_list: list[dict{forecast_id: int, date: str, high_temp: int, low_temp: int, condition: str, precipitation: int, humidity: int}]                                                         |
| /search/locations             | GET, POST    | location_search        | location_search.html           | search_results: list[dict{location_id: int, location_name: str, latitude: float, longitude: float, country: str, timezone: str}],
  saved_locations: list[dict{saved_id: int, user_id: int, location_id: int, location_name: str, is_default: int}]                                          |
| /alerts                      | GET          | weather_alerts         | alerts.html                   | alerts: list[dict{alert_id: int, location_id: int, alert_type: str, severity: str, description: str, start_time: str, end_time: str, is_acknowledged: int}],
  severity_filter: str,  
  location_filter_alerts: int or None                                             |
| /airquality                  | GET          | air_quality            | air_quality.html              | air_quality_data: dict{aqi_id: int, location_id: int, aqi_index: int, pm25: float, pm10: float, no2: float, o3: float, last_updated: str},
  location_list: list[dict{location_id: int, location_name: str}]
  
|
| /locations/saved             | GET          | saved_locations        | saved_locations.html          | saved_locations: list[dict{saved_id: int, user_id: int, location_id: int, location_name: str, is_default: int}],
  current_weather_data: list[dict{location_id: int, temperature: int, condition: str}]                                                           |
| /settings                   | GET, POST    | settings               | settings.html                 | settings: dict{temperature_unit: str, default_location_id: int, alert_notifications_enabled: bool},
  location_list: list[dict{location_id: int, location_name: str}]                                  |

---

## Detailed Explanation of Routes:

- **/**: Redirects immediately to `/dashboard`.

- **/dashboard**: Displays main hub with current weather summary of default or selected location.

- **/weather/current/<location_id>**: Displays detailed current weather conditions for given location.

- **/forecast/weekly**: Displays 7-day forecast. Accepts location filter via query or form (selected_location_id).

- **/search/locations**: Page to search for locations (POST for search form submission), showing list of matching locations and saved locations.

- **/alerts**: Shows active weather alerts. Filters by severity and location optionally.

- **/airquality**: Shows air quality data for selected or default location.

- **/locations/saved**: Shows all saved locations with quick access buttons.

- **/settings**: Allows users to view and modify settings like temperature units, default location, and alerts toggle. POST to update.

---

## Section 2: Frontend HTML Templates Specification

### templates/dashboard.html
- Page Title: "Weather Dashboard"
- Main container ID: `dashboard-page` (Div)
- Elements:
  - `current-weather-summary` (Div): Shows current weather of default location.
  - `search-location-button` (Button): Navigates to `location_search` function (`url_for('location_search')`).
  - `view-forecast-button` (Button): Navigates to `weekly_forecast` function (`url_for('weekly_forecast')`).
  - `view-alerts-button` (Button): Navigates to `weather_alerts` function (`url_for('weather_alerts')`).
- Context Variables:
  - `current_weather`: dict with keys `location_id` (int), `location_name` (str), `temperature` (int), `condition` (str), `humidity` (int), `wind_speed` (int), `last_updated` (str).
- Usage Notes:
  - Displays a summary of current weather.
  - Buttons link to other pages.

---

### templates/current_weather.html
- Page Title: "Current Weather"
- Main container ID: `current-weather-page` (Div)
- Elements:
  - `location-name` (H1): Location name string.
  - `temperature-display` (Div): Current temperature.
  - `weather-condition` (Div): Current weather condition description.
  - `humidity-info` (Div): Humidity percentage.
  - `wind-speed-info` (Div): Wind speed.
- Context Variables:
  - `weather`: dict with fields `location_id` (int), `location_name` (str), `temperature` (int), `condition` (str), `humidity` (int), `wind_speed` (int), `last_updated` (str).
- Usage Notes:
  - Shows detailed weather data for selected location.

---

### templates/weekly_forecast.html
- Page Title: "Weekly Forecast"
- Main container ID: `forecast-page` (Div)
- Elements:
  - `forecast-table` (Table): Displays rows of daily forecasts.
  - `location-filter` (Dropdown): Allows location selection. Option values are `location_id` (int).
  - `forecast-list` (Div): Grid container for daily forecast cards.
  - `back-to-dashboard` (Button): Navigates back to dashboard (`url_for('dashboard')`).
- Context Variables:
  - `location_list`: list of dicts each with `location_id` (int) and `location_name` (str).
  - `selected_location_id`: int (currently selected location).
  - `forecast_list`: list of dicts each with `forecast_id` (int), `date` (str), `high_temp` (int), `low_temp` (int), `condition` (str), `precipitation` (int), `humidity` (int).
- Usage Notes:
  - Location filter dropdown changes page content.
  - Loops over `forecast_list` to render forecast_table and forecast_list content.

---

### templates/location_search.html
- Page Title: "Search Locations"
- Main container ID: `search-page` (Div)
- Elements:
  - `location-search-input` (Input): Search text input for city or coordinates.
  - `search-results` (Div): Displays results. Each result includes a button with dynamic ID `select-location-button-{location_id}`.
  - `saved-locations-list` (Div): Lists saved locations.
- Context Variables:
  - `search_results`: list of dicts with fields `location_id` (int), `location_name` (str), `latitude` (float), `longitude` (float), `country` (str), `timezone` (str).
  - `saved_locations`: list of dicts with fields `saved_id` (int), `user_id` (int), `location_id` (int), `location_name` (str), `is_default` (int).
- Navigation:
  - Selecting a location button triggers appropriate backend route or POST (implementation detail).
- Usage Notes:
  - Loop over `search_results` to render each location's button with ID `select-location-button-{location_id}`.

---

### templates/alerts.html
- Page Title: "Weather Alerts"
- Main container ID: `alerts-page` (Div)
- Elements:
  - `alerts-list` (Div): Lists alerts. Each alert includes button `acknowledge-alert-button-{alert_id}`.
  - `severity-filter` (Dropdown): Filters alerts by severity.
  - `location-filter-alerts` (Dropdown): Filters alerts by location.
- Context Variables:
  - `alerts`: list of dicts with fields `alert_id` (int), `location_id` (int), `alert_type` (str), `severity` (str), `description` (str), `start_time` (str), `end_time` (str), `is_acknowledged` (int).
  - `severity_filter`: str
  - `location_filter_alerts`: int or None
- Usage Notes:
  - Loop over `alerts` for display.
  - Buttons to acknowledge alerts have dynamic IDs based on `alert_id`.

---

### templates/air_quality.html
- Page Title: "Air Quality Index"
- Main container ID: `air-quality-page` (Div)
- Elements:
  - `aqi-display` (Div): Shows AQI numeric value.
  - `aqi-description` (Div): Text description of air quality.
  - `pollution-details` (Table): Shows PM2.5, PM10, NO2, and other pollutant values.
  - `location-aqi-filter` (Dropdown): Filter by location.
  - `health-recommendation` (Div): Shows health recommendations.
- Context Variables:
  - `air_quality_data`: dict{aqi_id: int, location_id: int, aqi_index: int, pm25: float, pm10: float, no2: float, o3: float, last_updated: str}
  - `location_list`: list of dict{location_id: int, location_name: str}
- Usage Notes:
  - AQI and pollutant data shown dynamically.
  - Location filter changes the displayed data.

---

### templates/saved_locations.html
- Page Title: "Saved Locations"
- Main container ID: `saved-locations-page` (Div)
- Elements:
  - `locations-table` (Table): Shows saved locations with current temperature and condition.
  - `view-location-weather-{location_id}` (Button): View weather details for location.
  - `remove-location-button-{location_id}` (Button): Remove saved location.
  - `add-new-location-button` (Button): Add new location.
- Context Variables:
  - `saved_locations`: list of dicts with fields `saved_id` (int), `user_id` (int), `location_id` (int), `location_name` (str), `is_default` (int)
  - `current_weather_data`: list of dicts with `location_id` (int), `temperature` (int), `condition` (str)
- Usage Notes:
  - Loop over `saved_locations` to render table rows.
  - Buttons use dynamic IDs for each location.

---

### templates/settings.html
- Page Title: "Settings"
- Main container ID: `settings-page` (Div)
- Elements:
  - `temperature-unit-select` (Dropdown): Options: Celsius, Fahrenheit, Kelvin.
  - `default-location-select` (Dropdown): Options from `location_list` (location_id, location_name).
  - `alert-notifications-toggle` (Checkbox): Enable/disable alerts.
  - `save-settings-button` (Button): Save changes.
  - `back-to-dashboard` (Button): Navigate back to dashboard (`url_for('dashboard')`).
- Context Variables:
  - `settings`: dict{temperature_unit: str, default_location_id: int, alert_notifications_enabled: bool}
  - `location_list`: list of dicts{location_id: int, location_name: str}
- Usage Notes:
  - Form for updating settings with dropdowns and checkbox.
  - Buttons navigate or submit.

---

## Section 3: Data File Schemas

### data/current_weather.txt
- Format (pipe delimited fields in order):
  `location_id|location_name|temperature|condition|humidity|wind_speed|last_updated`
- Field Descriptions:
  - `location_id` (int): Unique location identifier.
  - `location_name` (str): Name of the location.
  - `temperature` (int): Current temperature in chosen unit.
  - `condition` (str): Weather condition description (e.g., Sunny, Rainy).
  - `humidity` (int): Humidity percentage.
  - `wind_speed` (int): Wind speed (unit consistent).
  - `last_updated` (str): Timestamp of last update (YYYY-MM-DD HH:MM).
- Example Lines:
  ```
  1|New York|72|Sunny|65|10|2025-01-20 14:30
  2|London|55|Rainy|80|15|2025-01-20 14:30
  3|Tokyo|45|Cloudy|72|8|2025-01-20 14:30
  ```

---

### data/forecasts.txt
- Format:
  `forecast_id|location_id|date|high_temp|low_temp|condition|precipitation|humidity`
- Field Descriptions:
  - `forecast_id` (int): Unique identifier for forecast entry.
  - `location_id` (int): Location this forecast applies to.
  - `date` (str): Date of forecast (YYYY-MM-DD).
  - `high_temp` (int): High temperature forecasted.
  - `low_temp` (int): Low temperature forecasted.
  - `condition` (str): Weather condition (e.g., Sunny).
  - `precipitation` (int): Percentage chance of precipitation.
  - `humidity` (int): Humidity percentage forecasted.
- Example Lines:
  ```
  1|1|2025-01-21|75|60|Sunny|0|60
  2|1|2025-01-22|68|55|Cloudy|10|70
  3|2|2025-01-21|58|48|Rainy|80|85
  ```

---

### data/locations.txt
- Format:
  `location_id|location_name|latitude|longitude|country|timezone`
- Field Descriptions:
  - `location_id` (int): Unique location identifier.
  - `location_name` (str): Name of location.
  - `latitude` (float): Latitude of the location.
  - `longitude` (float): Longitude of the location.
  - `country` (str): Country name.
  - `timezone` (str): Timezone abbreviation.
- Example Lines:
  ```
  1|New York|40.7128|-74.0060|USA|EST
  2|London|51.5074|-0.1278|UK|GMT
  3|Tokyo|35.6762|139.6503|Japan|JST
  ```

---

### data/alerts.txt
- Format:
  `alert_id|location_id|alert_type|severity|description|start_time|end_time|is_acknowledged`
- Field Descriptions:
  - `alert_id` (int): Unique alert identifier.
  - `location_id` (int): Location affected by alert.
  - `alert_type` (str): Type of alert (e.g., Thunderstorm).
  - `severity` (str): Severity level (Critical, High, Medium, Low).
  - `description` (str): Alert description.
  - `start_time` (str): Start timestamp (YYYY-MM-DD HH:MM).
  - `end_time` (str): End timestamp (YYYY-MM-DD HH:MM).
  - `is_acknowledged` (int): 0 for unacknowledged, 1 for acknowledged.
- Example Lines:
  ```
  1|1|Thunderstorm|High|Severe thunderstorm warning in effect until 8 PM|2025-01-20 14:00|2025-01-20 20:00|0
  2|2|Fog|Medium|Dense fog advisory in effect until noon tomorrow|2025-01-20 06:00|2025-01-21 12:00|0
  3|1|Wind|Medium|High wind advisory with gusts up to 45 mph|2025-01-20 15:00|2025-01-21 09:00|1
  ```

---

### data/air_quality.txt
- Format:
  `aqi_id|location_id|aqi_index|pm25|pm10|no2|o3|last_updated`
- Field Descriptions:
  - `aqi_id` (int): Unique air quality entry ID.
  - `location_id` (int): Location identifier.
  - `aqi_index` (int): Air Quality Index (0-500).
  - `pm25` (float): PM2.5 concentration.
  - `pm10` (float): PM10 concentration.
  - `no2` (float): NO2 concentration.
  - `o3` (float): O3 concentration.
  - `last_updated` (str): Timestamp of last measurement.
- Example Lines:
  ```
  1|1|45|12.5|35|28|55|2025-01-20 14:30
  2|2|67|22.3|48|42|78|2025-01-20 14:30
  3|3|120|68.5|95|65|110|2025-01-20 14:30
  ```

---

### data/saved_locations.txt
- Format:
  `saved_id|user_id|location_id|location_name|is_default`
- Field Descriptions:
  - `saved_id` (int): Unique ID for saved location.
  - `user_id` (int): User identifier (note: user auth not required, default to 1 or similar).
  - `location_id` (int): Location identifier.
  - `location_name` (str): Name of saved location.
  - `is_default` (int): 1 if default location, 0 otherwise.
- Example Lines:
  ```
  1|1|1|New York|1
  2|1|2|London|0
  3|2|3|Tokyo|1
  ```

---

# End of Design Specification

This document contains all necessary details for Backend and Frontend development of WeatherForecast application, ensuring full independence and consistent data usage.
