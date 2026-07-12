# Design Specification Document for WeatherForecast Web Application

---

## Section 1: Flask Routes Specification

| URL Path                       | HTTP Methods | Function Name            | Template Filename               | Context Variables (name: type)                                                                                                         |
|-------------------------------|--------------|--------------------------|-------------------------------|----------------------------------------------------------------------------------------------------------------------------------------|
| /                             | GET          | root_redirect             | None (redirects to /dashboard) | None                                                                                                                                   |
| /dashboard                    | GET          | dashboard                 | dashboard.html                 | current_weather: dict {
  location_id: int,
  location_name: str,
  temperature: float,
  condition: str,
  humidity: int,
  wind_speed: float,
  last_updated: str (format YYYY-MM-DD HH:MM)
}                                                                                           |
| /weather/current/<int:location_id> | GET          | current_weather           | current_weather.html           | location_name: str
  temperature: float
  condition: str
  humidity: int
  wind_speed: float
  last_updated: str (YYYY-MM-DD HH:MM)                                                                                      |
| /forecast/weekly              | GET          | weekly_forecast           | weekly_forecast.html           | forecasts: list of dict {
  forecast_id: int,
  location_id: int,
  date: str (YYYY-MM-DD),
  high_temp: float,
  low_temp: float,
  condition: str,
  precipitation: int,
  humidity: int
}
locations: list of dict {
  location_id: int,
  location_name: str
}
selected_location_id: int  (optional, default to first in locations if not provided)                                                     |
| /search/locations            | GET          | location_search           | location_search.html           | search_results: list of dict {
  location_id: int,
  location_name: str
}
saved_locations: list of dict {
  location_id: int,
  location_name: str
}
search_query: str (optional, empty string if none)                                                                                      |
| /alerts                     | GET          | alerts                   | alerts.html                   | alerts: list of dict {
  alert_id: int,
  location_id: int,
  alert_type: str,
  severity: str,
  description: str,
  start_time: str (YYYY-MM-DD HH:MM),
  end_time: str (YYYY-MM-DD HH:MM),
  is_acknowledged: bool
}
severity_filter: str (values: "All", "Critical", "High", "Medium", "Low")
location_filter: int (location_id) or None for all                                             |
| /air_quality                | GET          | air_quality               | air_quality.html             | air_quality_data: list of dict {
  aqi_id: int,
  location_id: int,
  aqi_index: int,
  pm25: float,
  pm10: float,
  no2: float,
  o3: float,
  last_updated: str (YYYY-MM-DD HH:MM)
}
locations: list of dict {
  location_id: int,
  location_name: str
}
selected_location_id: int (optional)                                                                                                   |
| /saved_locations            | GET          | saved_locations           | saved_locations.html           | saved_locations: list of dict {
  saved_id: int,
  location_id: int,
  location_name: str,
  is_default: bool,
  current_temperature: float,
  current_condition: str
}                                                                                                   |
| /settings                   | GET, POST    | settings                  | settings.html                 | temperature_unit_options: list of str ["Celsius", "Fahrenheit", "Kelvin"]
current_temperature_unit: str
saved_locations: list of dict {
  location_id: int,
  location_name: str
}
user_settings: dict {
  default_location_id: int,
  alert_notifications_enabled: bool
}                                                                                                                                   |

#### Notes:
- Root route `/` redirects to `/dashboard` via 302 redirect.
- For all pages with location filter dropdowns, `locations` list contains dictionaries each with `location_id` and `location_name` to populate dropdowns.
- The `saved_locations` list in their respective routes includes enriched data with current temperature and weather condition by joining with current_weather data for display.
- POST on `/settings` accepts form data for updating user preferences; on success, reloads or redirects back to `/settings`.

---

## Section 2: Frontend HTML Templates Specification

### 1. templates/dashboard.html
- Page Title: Weather Dashboard
- Main Heading (<h1>): Weather Dashboard
- Element IDs and details:
  - `dashboard-page` (div): Container for entire dashboard page.
  - `current-weather-summary` (div): Shows current weather conditions for default location.
  - `search-location-button` (button): Navigates to location search page.
  - `view-forecast-button` (button): Navigates to weekly forecast page.
  - `view-alerts-button` (button): Navigates to weather alerts page.
- Navigation via `url_for`:
  - `search-location-button`: links to `location_search` function.
  - `view-forecast-button`: links to `weekly_forecast` function.
  - `view-alerts-button`: links to `alerts` function.
- Context variables:
  - `current_weather`: dict {
      `location_id`: int,
      `location_name`: str,
      `temperature`: float,
      `condition`: str,
      `humidity`: int,
      `wind_speed`: float,
      `last_updated`: str,
    }
- Usage Notes:
  - Render the `current-weather-summary` div with current temperature, condition, humidity, wind speed using the keys from `current_weather`.

### 2. templates/current_weather.html
- Page Title: Current Weather
- Main Heading (<h1>): location_name (dynamic)
- Element IDs and details:
  - `current-weather-page` (div): Container for current weather page.
  - `location-name` (h1): Displays location name.
  - `temperature-display` (div): Shows temperature.
  - `weather-condition` (div): Shows weather condition.
  - `humidity-info` (div): Shows humidity percentage.
  - `wind-speed-info` (div): Shows wind speed.
- Navigation:
  - Provide navigation to dashboard if needed (not detailed in spec).
- Context variables:
  - `location_name`: str
  - `temperature`: float
  - `condition`: str
  - `humidity`: int
  - `wind_speed`: float
  - `last_updated`: str
- Usage Notes:
  - Display all weather parameters clearly using the respective element IDs.

### 3. templates/weekly_forecast.html
- Page Title: Weekly Forecast
- Main Heading (<h1>): Weekly Forecast
- Element IDs and details:
  - `forecast-page` (div): Container for forecast page.
  - `forecast-table` (table): Shows daily forecasts with columns Date, High Temp, Low Temp, Condition.
  - `location-filter` (dropdown/select): Dropdown to filter forecast results by location.
  - `forecast-list` (div): Grid or list displaying forecast cards for each day.
  - `back-to-dashboard` (button): Navigates back to dashboard.
- Navigation via `url_for`:
  - `back-to-dashboard`: links to `dashboard` function.
- Context variables:
  - `forecasts`: list of dict {
      forecast_id: int,
      location_id: int,
      date: str,
      high_temp: float,
      low_temp: float,
      condition: str,
      precipitation: int,
      humidity: int
    }
  - `locations`: list of dict { location_id: int, location_name: str }
  - `selected_location_id`: int
- Usage Notes:
  - Use `location-filter` dropdown to filter `forecasts` by location.
  - Render `forecast-list` dynamically with forecast cards.
  - Render `forecast-table` summarizing the forecasts for the selected location.

### 4. templates/location_search.html
- Page Title: Search Locations
- Main Heading (<h1>): Search Locations
- Element IDs and details:
  - `search-page` (div): Container for the search page.
  - `location-search-input` (input): Text input to enter search queries for locations.
  - `search-results` (div): Displays matching location results.
  - `select-location-button-{location_id}` (button): Button to select and save location, one per search result.
  - `saved-locations-list` (div): Displays already saved locations.
- Navigation:
  - Navigation back to dashboard or other pages as needed (not explicitly defined).
- Context variables:
  - `search_results`: list of dict {location_id: int, location_name: str}
  - `saved_locations`: list of dict {location_id: int, location_name: str}
  - `search_query`: str
- Usage Notes:
  - Provide button `select-location-button-{location_id}` with dynamic locations.
  - Display saved locations distinctly.

### 5. templates/alerts.html
- Page Title: Weather Alerts
- Main Heading (<h1>): Weather Alerts
- Element IDs and details:
  - `alerts-page` (div): Container for alerts page.
  - `alerts-list` (div): Lists active alerts with details.
  - `severity-filter` (dropdown): Filter alerts by severity (All, Critical, High, Medium, Low).
  - `location-filter-alerts` (dropdown): Filter alerts by location.
  - `acknowledge-alert-button-{alert_id}` (button): Button to acknowledge alerts by id.
- Navigation:
  - Provide button to return to dashboard if needed.
- Context variables:
  - `alerts`: list of dict {
      alert_id: int,
      location_id: int,
      alert_type: str,
      severity: str,
      description: str,
      start_time: str,
      end_time: str,
      is_acknowledged: bool
    }
  - `severity_filter`: str
  - `location_filter`: int or None
- Usage Notes:
  - Render alerts-list dynamically.
  - Each alert includes acknowledge button with id `acknowledge-alert-button-{alert_id}`.

### 6. templates/air_quality.html
- Page Title: Air Quality Index
- Main Heading (<h1>): Air Quality Index
- Element IDs and details:
  - `air-quality-page` (div): Container for air quality page.
  - `aqi-display` (div): Shows AQI index value.
  - `aqi-description` (div): Shows descriptive AQI level (Good, Moderate, etc.).
  - `pollution-details` (table): Displays pollutant values PM2.5, PM10, NO2, O3.
  - `location-aqi-filter` (dropdown): Filter air quality data by location.
  - `health-recommendation` (div): Shows health suggestions based on AQI.
- Navigation:
  - Provide navigation to dashboard if needed.
- Context variables:
  - `air_quality_data`: list of dict {
      aqi_id: int,
      location_id: int,
      aqi_index: int,
      pm25: float,
      pm10: float,
      no2: float,
      o3: float,
      last_updated: str
    }
  - `locations`: list of dict {location_id: int, location_name: str}
  - `selected_location_id`: int
- Usage Notes:
  - Filter displayed data by `selected_location_id`.
  - Show pollutant values and AQI-related health recommendations.

### 7. templates/saved_locations.html
- Page Title: Saved Locations
- Main Heading (<h1>): Saved Locations
- Element IDs and details:
  - `saved-locations-page` (div): Container for saved locations page.
  - `locations-table` (table): Table showing saved locations.
  - `view-location-weather-{location_id}` (button): Button to view weather details for that location.
  - `remove-location-button-{location_id}` (button): Button to remove saved location.
  - `add-new-location-button` (button): Button to add a new location.
- Navigation:
  - Action buttons link appropriately to current weather or search page.
- Context variables:
  - `saved_locations`: list of dict {
      saved_id: int,
      location_id: int,
      location_name: str,
      is_default: bool,
      current_temperature: float,
      current_condition: str
    }
- Usage Notes:
  - Display saved locations with current weather info.

### 8. templates/settings.html
- Page Title: Settings
- Main Heading (<h1>): Settings
- Element IDs and details:
  - `settings-page` (div): Container for settings page.
  - `temperature-unit-select` (dropdown): Select temperature unit (Celsius, Fahrenheit, Kelvin).
  - `default-location-select` (dropdown): Select default location from saved locations.
  - `alert-notifications-toggle` (checkbox): Toggle for alert notifications.
  - `save-settings-button` (button): Save settings changes.
  - `back-to-dashboard` (button): Button to return to dashboard.
- Navigation via `url_for`:
  - `back-to-dashboard`: links to `dashboard` function.
- Context variables:
  - `temperature_unit_options`: list of str
  - `current_temperature_unit`: str
  - `saved_locations`: list of dict {location_id: int, location_name: str}
  - `user_settings`: dict {
      default_location_id: int,
      alert_notifications_enabled: bool
    }
- Usage Notes:
  - Render dropdowns with current selections.
  - Handle form submission on `save-settings-button` click.

---

## Section 3: Data File Schemas

### 1. data/current_weather.txt
- Fields (pipe-delimited):
  location_id|location_name|temperature|condition|humidity|wind_speed|last_updated
- Field Descriptions:
  - location_id (int): Unique identifier for location.
  - location_name (str): Name of the city/location.
  - temperature (float): Current temperature in degrees.
  - condition (str): Weather condition (e.g., Sunny, Rainy).
  - humidity (int): Humidity percentage.
  - wind_speed (float): Wind speed in appropriate units.
  - last_updated (str): Timestamp of last update (format YYYY-MM-DD HH:MM).
- Example Lines:
  1|New York|72|Sunny|65|10|2025-01-20 14:30
  2|London|55|Rainy|80|15|2025-01-20 14:30
  3|Tokyo|45|Cloudy|72|8|2025-01-20 14:30

### 2. data/forecasts.txt
- Fields (pipe-delimited):
  forecast_id|location_id|date|high_temp|low_temp|condition|precipitation|humidity
- Field Descriptions:
  - forecast_id (int): Unique identifier for the forecast.
  - location_id (int): Reference to location.
  - date (str): Date of forecast (YYYY-MM-DD).
  - high_temp (float): Highest temperature expected.
  - low_temp (float): Lowest temperature expected.
  - condition (str): Forecasted weather condition.
  - precipitation (int): Precipitation percentage chance.
  - humidity (int): Humidity percentage.
- Example Lines:
  1|1|2025-01-21|75|60|Sunny|0|60
  2|1|2025-01-22|68|55|Cloudy|10|70
  3|2|2025-01-21|58|48|Rainy|80|85

### 3. data/locations.txt
- Fields (pipe-delimited):
  location_id|location_name|latitude|longitude|country|timezone
- Field Descriptions:
  - location_id (int): Unique identifier.
  - location_name (str): City or area name.
  - latitude (float): Latitude coordinate.
  - longitude (float): Longitude coordinate.
  - country (str): Country name.
  - timezone (str): Timezone abbreviation.
- Example Lines:
  1|New York|40.7128|-74.0060|USA|EST
  2|London|51.5074|-0.1278|UK|GMT
  3|Tokyo|35.6762|139.6503|Japan|JST

### 4. data/alerts.txt
- Fields (pipe-delimited):
  alert_id|location_id|alert_type|severity|description|start_time|end_time|is_acknowledged
- Field Descriptions:
  - alert_id (int): Unique alert identifier.
  - location_id (int): Location affected.
  - alert_type (str): Type of alert (e.g., Thunderstorm).
  - severity (str): Severity level (Critical, High, Medium, Low).
  - description (str): Detailed description.
  - start_time (str): Start timestamp.
  - end_time (str): End timestamp.
  - is_acknowledged (int): 0 (false) or 1 (true) for acknowledgment status.
- Example Lines:
  1|1|Thunderstorm|High|Severe thunderstorm warning in effect until 8 PM|2025-01-20 14:00|2025-01-20 20:00|0
  2|2|Fog|Medium|Dense fog advisory in effect until noon tomorrow|2025-01-20 06:00|2025-01-21 12:00|0
  3|1|Wind|Medium|High wind advisory with gusts up to 45 mph|2025-01-20 15:00|2025-01-21 09:00|1

### 5. data/air_quality.txt
- Fields (pipe-delimited):
  aqi_id|location_id|aqi_index|pm25|pm10|no2|o3|last_updated
- Field Descriptions:
  - aqi_id (int): Unique air quality record ID.
  - location_id (int): Location identifier.
  - aqi_index (int): Air Quality Index 0-500.
  - pm25 (float): PM2.5 concentration.
  - pm10 (float): PM10 concentration.
  - no2 (float): NO2 concentration.
  - o3 (float): O3 concentration.
  - last_updated (str): Timestamp.
- Example Lines:
  1|1|45|12.5|35|28|55|2025-01-20 14:30
  2|2|67|22.3|48|42|78|2025-01-20 14:30
  3|3|120|68.5|95|65|110|2025-01-20 14:30

### 6. data/saved_locations.txt
- Fields (pipe-delimited):
  saved_id|user_id|location_id|location_name|is_default
- Field Descriptions:
  - saved_id (int): Unique saved location entry ID.
  - user_id (int): User identifier (note: app is no-auth, user_id may be fixed).
  - location_id (int): Reference to location.
  - location_name (str): Name of location.
  - is_default (int): 1 for default location, 0 otherwise.
- Example Lines:
  1|1|1|New York|1
  2|1|2|London|0
  3|2|3|Tokyo|1

---

This specification document provides thorough guidance on implementing all aspects of the WeatherForecast web application independently for backend and frontend respective developers, ensuring consistency and correct data linkage across all application components.