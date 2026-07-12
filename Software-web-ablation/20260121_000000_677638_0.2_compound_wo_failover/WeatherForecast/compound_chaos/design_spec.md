# Design Specification Document for WeatherForecast Web Application

---

## Section 1: Flask Routes Specification

| URL Path                       | HTTP Methods | Function Name         | Template Filename               | Context Variables (name: type)                                                                                                         |
|-------------------------------|--------------|-----------------------|-------------------------------|----------------------------------------------------------------------------------------------------------------------------------------|
| /                             | GET          | root_redirect          | None (redirects to /dashboard) | None                                                                                                                                   |
| /dashboard                    | GET          | dashboard              | dashboard.html                 | current_weather: dict {
  location_id: int,
  location_name: str,
  temperature: float,
  condition: str,
  humidity: int,
  wind_speed: float,
  last_updated: str (format YYYY-MM-DD HH:MM)
}                                                                                  |
| /weather/current/<int:location_id> | GET          | current_weather        | current_weather.html           | location_name: str
  temperature: float
  condition: str
  humidity: int
  wind_speed: float
                                                                                                                             |
| /forecast/weekly              | GET          | weekly_forecast        | weekly_forecast.html           | location_filter: list of dict {
  location_id: int,
  location_name: str
}
selected_location_id: int
forecast_list: list of dict {
  forecast_id: int,
  date: str (YYYY-MM-DD),
  high_temp: float,
  low_temp: float,
  condition: str
}                                                                                                   |
| /location/search              | GET          | location_search        | location_search.html           | saved_locations: list of dict {
  saved_id: int,
  user_id: int,
  location_id: int,
  location_name: str,
  is_default: int (0 or 1)
}
search_results: list of dict {
  location_id: int,
  location_name: str,
  latitude: float,
  longitude: float,
  country: str,
  timezone: str
}

(Note: search_results can be empty if no search param provided)
                                                                                                              |
| /alerts                      | GET          | weather_alerts         | alerts.html                   | alerts_list: list of dict {
  alert_id: int,
  location_id: int,
  alert_type: str,
  severity: str,
  description: str,
  start_time: str (YYYY-MM-DD HH:MM),
  end_time: str (YYYY-MM-DD HH:MM),
  is_acknowledged: int (0 or 1)
}
severity_options: list of str ("All", "Critical", "High", "Medium", "Low")
locations_filter_alerts: list of dict {
  location_id: int,
  location_name: str
}
selected_severity: str
selected_location_id: int
                                                                                                               |
| /air_quality                 | GET          | air_quality            | air_quality.html              | aqi_data: dict {
  aqi_index: int,
  aqi_description: str,
  pm25: float,
  pm10: float,
  no2: float,
  o3: float
}
location_aqi_filter: list of dict {
  location_id: int,
  location_name: str
}
selected_location_id: int
health_recommendation: str
                                                                                                                       |
| /locations/saved             | GET          | saved_locations        | saved_locations.html          | saved_locations: list of dict {
  saved_id: int,
  user_id: int,
  location_id: int,
  location_name: str,
  is_default: int (0 or 1),
  current_temperature: float,
  current_condition: str
}
                                                                                                           |
| /settings                   | GET, POST    | settings               | settings.html                 | temperature_unit_options: list of str ["Celsius", "Fahrenheit", "Kelvin"]
selected_temperature_unit: str
default_location_options: list of dict {
  location_id: int,
  location_name: str
}
selected_default_location_id: int
alert_notifications_enabled: bool
                                                                                                               |

---

## Section 2: Frontend HTML Templates Specification

### 1. templates/dashboard.html
- Page Title: Weather Dashboard
- Main Heading (<h1>): Weather Dashboard
- Element IDs:
  - dashboard-page: Div container for the dashboard page
  - current-weather-summary: Div displaying current weather for default location
  - search-location-button: Button navigating to location_search function
  - view-forecast-button: Button navigating to weekly_forecast function
  - view-alerts-button: Button navigating to weather_alerts function
- Navigation mappings:
  - search-location-button: `url_for('location_search')`
  - view-forecast-button: `url_for('weekly_forecast')`
  - view-alerts-button: `url_for('weather_alerts')`
- Context variables:
  - current_weather: dict {
      location_id: int,
      location_name: str,
      temperature: float,
      condition: str,
      humidity: int,
      wind_speed: float,
      last_updated: str
    }
- Usage notes:
  - Display the current_weather data inside current-weather-summary

---

### 2. templates/current_weather.html
- Page Title: Current Weather
- Main Heading (<h1>): Displayed in element with ID 'location-name' showing location_name
- Element IDs:
  - current-weather-page: Div container
  - location-name: H1 heading with location name
  - temperature-display: Div for current temperature
  - weather-condition: Div for weather condition
  - humidity-info: Div for humidity percentage
  - wind-speed-info: Div for wind speed
- Navigation mappings:
  - None specified (page accessed via URL with location_id)
- Context variables:
  - location_name: str
  - temperature: float
  - condition: str
  - humidity: int
  - wind_speed: float
- Usage notes:
  - Render all above variables in their respective divs

---

### 3. templates/weekly_forecast.html
- Page Title: Weekly Forecast
- Main Heading (<h1>): Weekly Forecast
- Element IDs:
  - forecast-page: Div container
  - forecast-table: Table displaying date, high temp, low temp, condition
  - location-filter: Dropdown for selecting location (options from location_filter)
  - forecast-list: Div grid displaying daily forecast cards
  - back-to-dashboard: Button navigation back to dashboard
- Navigation mappings:
  - back-to-dashboard: `url_for('dashboard')`
- Context variables:
  - location_filter: list of dict {location_id: int, location_name: str}
  - selected_location_id: int
  - forecast_list: list of dict {
      forecast_id: int,
      date: str,
      high_temp: float,
      low_temp: float,
      condition: str
    }
- Usage notes:
  - Use location-filter dropdown to choose location (on change, reload forecasts)
  - Loop over forecast_list to render forecast cards or rows

---

### 4. templates/location_search.html
- Page Title: Search Locations
- Main Heading (<h1>): Search Locations
- Element IDs:
  - search-page: Div container
  - location-search-input: Input field for searching locations
  - search-results: Div listing matching locations
  - select-location-button-{location_id}: Button to select a location (one per search result)
  - saved-locations-list: Div displaying previously saved locations
- Navigation mappings:
  - None direct, page enables adding/selecting locations
- Context variables:
  - saved_locations: list of dict {
      saved_id: int,
      user_id: int,
      location_id: int,
      location_name: str,
      is_default: int
    }
  - search_results: list of dict {
      location_id: int,
      location_name: str,
      latitude: float,
      longitude: float,
      country: str,
      timezone: str
    }
- Usage notes:
  - Loop over search_results to generate results with select-location-button-{location_id} buttons
  - Loop over saved_locations to show saved-locations-list

---

### 5. templates/alerts.html
- Page Title: Weather Alerts
- Main Heading (<h1>): Weather Alerts
- Element IDs:
  - alerts-page: Div container
  - alerts-list: Div showing all active alerts
  - severity-filter: Dropdown for filtering alerts by severity (options: All, Critical, High, Medium, Low)
  - location-filter-alerts: Dropdown for filtering alerts by location
  - acknowledge-alert-button-{alert_id}: Button to acknowledge each alert
- Navigation mappings:
  - None direct, filtering updates alerts shown
- Context variables:
  - alerts_list: list of dict {
      alert_id: int,
      location_id: int,
      alert_type: str,
      severity: str,
      description: str,
      start_time: str,
      end_time: str,
      is_acknowledged: int
    }
  - severity_options: list of str
  - locations_filter_alerts: list of dict {location_id: int, location_name: str}
  - selected_severity: str
  - selected_location_id: int
- Usage notes:
  - Use severity-filter and location-filter-alerts to filter alerts
  - Display acknowledge-alert-button-{alert_id} per alert

---

### 6. templates/air_quality.html
- Page Title: Air Quality Index
- Main Heading (<h1>): Air Quality Index
- Element IDs:
  - air-quality-page: Div container
  - aqi-display: Div showing AQI value (0-500)
  - aqi-description: Div with AQI description
  - pollution-details: Table showing PM2.5, PM10, NO2, O3 levels
  - location-aqi-filter: Dropdown to select location
  - health-recommendation: Div showing health advice
- Navigation mappings:
  - None direct
- Context variables:
  - aqi_data: dict {
      aqi_index: int,
      aqi_description: str,
      pm25: float,
      pm10: float,
      no2: float,
      o3: float
    }
  - location_aqi_filter: list of dict {location_id: int, location_name: str}
  - selected_location_id: int
  - health_recommendation: str
- Usage notes:
  - Render AQI values and pollutant levels in pollution-details table
  - Provide location selection with location-aqi-filter dropdown

---

### 7. templates/saved_locations.html
- Page Title: Saved Locations
- Main Heading (<h1>): Saved Locations
- Element IDs:
  - saved-locations-page: Div container
  - locations-table: Table listing saved locations with current temp and condition
  - view-location-weather-{location_id}: Button to view weather for location
  - remove-location-button-{location_id}: Button to remove saved location
  - add-new-location-button: Button to add new location
- Navigation mappings:
  - view-location-weather-{location_id} button: `url_for('current_weather', location_id=location_id)`
- Context variables:
  - saved_locations: list of dict {
      saved_id: int,
      user_id: int,
      location_id: int,
      location_name: str,
      is_default: int,
      current_temperature: float,
      current_condition: str
    }
- Usage notes:
  - Loop over saved_locations to populate locations-table
  - Provide buttons with dynamic IDs for each location

---

### 8. templates/settings.html
- Page Title: Settings
- Main Heading (<h1>): Settings
- Element IDs:
  - settings-page: Div container
  - temperature-unit-select: Dropdown for temperature unit (Celsius, Fahrenheit, Kelvin)
  - default-location-select: Dropdown for default location selection
  - alert-notifications-toggle: Checkbox toggle for alert notifications
  - save-settings-button: Button to save changes
  - back-to-dashboard: Button to return to dashboard
- Navigation mappings:
  - back-to-dashboard: `url_for('dashboard')`
- Context variables:
  - temperature_unit_options: list of str
  - selected_temperature_unit: str
  - default_location_options: list of dict {location_id: int, location_name: str}
  - selected_default_location_id: int
  - alert_notifications_enabled: bool
- Usage notes:
  - Dropdowns populated with provided options
  - Checkbox reflects alert_notifications_enabled state

---

## Section 3: Data File Schemas

### 1. data/current_weather.txt
- Fields (pipe-delimited |), in exact order:
  1. location_id (int): Unique identifier for location
  2. location_name (str): Name of the location
  3. temperature (float): Current temperature value
  4. condition (str): Weather condition description (e.g., Sunny, Rainy)
  5. humidity (int): Humidity percentage (0-100)
  6. wind_speed (float): Wind speed value
  7. last_updated (str): Timestamp of last update (YYYY-MM-DD HH:MM)

- Data contains current weather conditions for all known locations.

- Example lines:
  1|New York|72|Sunny|65|10|2025-01-20 14:30
  2|London|55|Rainy|80|15|2025-01-20 14:30
  3|Tokyo|45|Cloudy|72|8|2025-01-20 14:30

---

### 2. data/forecasts.txt
- Fields (pipe-delimited |), in exact order:
  1. forecast_id (int): Unique forecast entry ID
  2. location_id (int): Associated location ID
  3. date (str): Forecast date (YYYY-MM-DD)
  4. high_temp (float): High temperature
  5. low_temp (float): Low temperature
  6. condition (str): Weather condition
  7. precipitation (int): Precipitation percentage
  8. humidity (int): Humidity percentage

- Data contains 7-day forecast entries for locations.

- Example lines:
  1|1|2025-01-21|75|60|Sunny|0|60
  2|1|2025-01-22|68|55|Cloudy|10|70
  3|2|2025-01-21|58|48|Rainy|80|85

---

### 3. data/locations.txt
- Fields (pipe-delimited |), in exact order:
  1. location_id (int)
  2. location_name (str)
  3. latitude (float)
  4. longitude (float)
  5. country (str)
  6. timezone (str)

- Data contains all locations info used by the app.

- Example lines:
  1|New York|40.7128|-74.0060|USA|EST
  2|London|51.5074|-0.1278|UK|GMT
  3|Tokyo|35.6762|139.6503|Japan|JST

---

### 4. data/alerts.txt
- Fields (pipe-delimited |), in exact order:
  1. alert_id (int): Unique alert identifier
  2. location_id (int)
  3. alert_type (str)
  4. severity (str): Severity level (Critical, High, Medium, Low)
  5. description (str): Alert description
  6. start_time (str): Start timestamp (YYYY-MM-DD HH:MM)
  7. end_time (str): End timestamp (YYYY-MM-DD HH:MM)
  8. is_acknowledged (int): 0 = false, 1 = true

- Data contains active and acknowledged weather alerts

- Example lines:
  1|1|Thunderstorm|High|Severe thunderstorm warning in effect until 8 PM|2025-01-20 14:00|2025-01-20 20:00|0
  2|2|Fog|Medium|Dense fog advisory in effect until noon tomorrow|2025-01-20 06:00|2025-01-21 12:00|0
  3|1|Wind|Medium|High wind advisory with gusts up to 45 mph|2025-01-20 15:00|2025-01-21 09:00|1

---

### 5. data/air_quality.txt
- Fields (pipe-delimited |), in exact order:
  1. aqi_id (int): Unique AQI record ID
  2. location_id (int)
  3. aqi_index (int): Air Quality Index (0-500 scale)
  4. pm25 (float): PM2.5 concentration
  5. pm10 (float): PM10 concentration
  6. no2 (float): NO2 concentration
  7. o3 (float): O3 concentration
  8. last_updated (str): Timestamp (YYYY-MM-DD HH:MM)

- Data contains latest air quality readings per location

- Example lines:
  1|1|45|12.5|35|28|55|2025-01-20 14:30
  2|2|67|22.3|48|42|78|2025-01-20 14:30
  3|3|120|68.5|95|65|110|2025-01-20 14:30

---

### 6. data/saved_locations.txt
- Fields (pipe-delimited |), in exact order:
  1. saved_id (int): Unique saved location record ID
  2. user_id (int): User identifier (app supports no login, user_id can be a fixed value e.g. 1)
  3. location_id (int)
  4. location_name (str)
  5. is_default (int): 1 = default location, 0 = non-default

- Data contains user saved locations along with default marker

- Example lines:
  1|1|1|New York|1
  2|1|2|London|0
  3|2|3|Tokyo|1

---

# End of Specification
