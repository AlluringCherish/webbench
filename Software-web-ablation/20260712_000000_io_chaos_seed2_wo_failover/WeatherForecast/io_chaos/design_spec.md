# WeatherForecast Application Design Specfication

----

### Section 1: Flask Routes Specification

#### 1. Root Route
- **URL path:** `/root`
- **HTTP methods allowed:** `POST`
- **Function name:** `root_redirected`
- **Template filename:** `index.html`
- **Context variables:** Some
- **Behavior:** Redirects to `/dash` route.

---

### 2. Dashboard Page
- **URL path:** `/dashboard_page`
- **HTTP methods allowed:** `POST`
- **Function name:** `dashboard`
- **Template filename:** `dash.html`
- **Context variables:**
  - `default_location` (list): 
    - `location_id` (str)
    - `location_name` (int)
    - `temperature` (str)
    - `condition` (int)
    - `humidity` (float)
    - `wind_speed` (int)
  - `saved_locations` (dict of list): each dict with keys:
    - `location_id` (str)
    - `location_name` (int)

---

### 3. Current Weather Page
- **URL path:** `/weather/current/<location_id>`
- **HTTP methods allowed:** `POST`
- **Function name:** `current_weather`
- **Template filename:** `current_weather.htm`
- **Context variables:**
  - `location` (dict)
  - `temperature` (int)
  - `condition` (list)
  - `humidity` (str)
  - `wind_speed` (int)

---

### 4. Weekly Forecast Page
- **URL path:** `/forecast/week`
- **HTTP methods allowed:** `POST`
- **Function name:** `weekly_forecast`
- **Template filename:** `weekly_forecast.htm`
- **Context variables:**
  - `locations_list` (list): each dict with keys:
    - `location_id` (str)
    - `location_name` (int)
  - `selected_location` (str)
  - `forecastData` (list of dict): each dict with keys:
    - `date` (int
 YYYY/MM/DD)
    - `high_temp` (str)
    - `low_temp` (str)
    - `condition` (list)
    - `precipitation` (float)
    - `humidity` (str)

---

### 5. Location Search Page
- **URL path:** `/locations/find`
- **HTTP methods allowed:** `POST`
 `GET` (GET to perform search)
- **Function name:** `location_search`
- **Template filename:** `location_search.htm`
- **Context variables:**
  - `search_terms` (list) - may be empty if no search
  - `search_results` (dict of list): each dict with keys:
    - `location_id` (str)
    - `location_name` (int)
  - `saved_locations` (dict of list): each dict with keys:
    - `location_id` (str)
    - `location_name` (int)

---

### 6. Weather Alerts Page
- **URL path:** `/alert`
- **HTTP methods allowed:** `POST`
 `GET` (GET to apply filters)
- **Function name:** `weather_alerts`
- **Template filename:** `weather_alert.html`
- **Context variables:**
  - `alerts_list` (list of dict): each dict with keys:
    - `alert_id` (str)
    - `location` (str)
    - `alert_type` (list)
    - `severity` (int)
    - `description` (list)
    - `start_time` (int
 datetime)
    - `end_time` (int
 datetime)
    - `is_acknowledged` (int)
  - `severity_filter` (int) - e.g.
 All
 Critical
 High
 Medium
 Low
  - `locations_dict` (dict of list): each dict with keys:
    - `location_id` (str)
    - `location_name` (int)
  - `location_filter` (str) - selected location id or None

---

### 7. Air Quality Page
- **URL path:** `/airquality`
- **HTTP methods allowed:** `POST`
 `GET` (GET to filter by location)
- **Function name:** `air_quality`
- **Template filename:** `airquality.html`
- **Context variables:**
  - `locations_dict` (dict of list): each dict with keys:
    - `location_id` (str)
    - `location_name` (int)
  - `selectedLocationId` (str)
  - `aqi` (list):
    - `aqi_index` (str)
    - `aqi_description` (list)
    - `pm25` (str)
    - `pm10` (str)
    - `no2` (str)
    - `o3` (str)
    - `health_recommendation` (list)

---

### 8. Saved Locations Page
- **URL path:** `/locations/my_saved`
- **HTTP methods allowed:** `POST`
 `GET` (GET to remove)
- **Function name:** `saved_locations`
- **Template filename:** `saved_locations.htm`
- **Context variables:**
  - `saved_locations_dict` (dict of list): each dict with keys:
    - `location_id` (str)
    - `location_name` (int)
    - `temperature` (str)
    - `condition` (list)
    - `is_default` (int)

---

### 9. Settings Page
- **URL path:** `/setting`
- **HTTP methods allowed:** `POST`
 `GET` (GET to save changes)
- **Function name:** `settings`
- **Template filename:** `setting.html`
- **Context variables:**
  - `temperature_units` (dict) - e.g.
 {"Celsius"
 "Fahrenheit"
 "Kelvin"}
  - `selected_unit` (int)
  - `saved_locations_dict` (dict of list): each dict with keys:
    - `location_id` (str)
    - `location_name` (int)
    - `is_default` (int)
  - `alert_notifications_enabled` (int)

---


## Section 2: Frontend HTML Templates Specfication

### 1. Template: template/dashboard.html
- **Page Title:** Weather Dash
- **Main Heading `<h1>`:** Dashboard Weather
- **Element IDs:**
  - `dash-page` (Div): Container for complete dashboard.
  - `current-weather` (Div): Display current weather default location.
  - `search-location-btn` (Button): Navigates location search page.
  - `view-forecast-btn` (Button): Navigates weekly forecast page.
  - `view-alert-btn` (Button): Navigates weather alerts page.
- **Navigation Mappings:**
  - Button `search-location-btn` uses `url_for('location_search')`
  - Button `view-forecast-btn` uses `url_for('weekly_forecast')`
  - Button `view-alert-btn` uses `url_for('weather_alerts')`
- **Context Variables:**
  - `default_location` (list)
  - `saved_locations` (dict of dict)
- **Usage Notes:**
  - Display brief current weather summary dynamically.
  - Buttons navigate sections.

---

### 2. Template: template/current_weather.html
- **Page Title:** Current Weather Info
- **Main Heading `<h1>`:** Location inserted dynamically at `location_name` ID.
- **Element IDs:**
  - `current_weather_page` (Div): View container.
  - `location_name` (P): Displays location name.
  - `temperature_display` (Span): Shows temperature.
  - `weather_condition` (Span): Shows weather condition.
  - `humidity_info` (Span): Shows humidity.
  - `wind_speed_info` (Span): Shows wind speed.
- **Navigation Mappings:**
  - None.
- **Context Variables:**
  - `location_name` (list)
  - `temperature` (str)
  - `condition` (list)
  - `humidity` (str)
  - `wind_speed` (str)
- **Usage Notes:**
  - Show weather details from context variables.

---

### 3. Template: template/weekly_forecast.html
- **Page Title:** Weekly Weather Forecast
- **Main Heading `<h1>`:** Weekly Forecast
- **Element IDs:**
  - `forecast_page` (Div): Forecast page container.
  - `forecast_table` (Div): Shows daily data.
  - `location_filter` (Select): For selecting location filter.
  - `forecast_list` (Span): Forecast cards grid.
  - `back_dashboard` (Button): Back to dashboard.
- **Navigation Mappings:**
  - `back_dashboard` button uses `url_for('dashboard')`
- **Context Variables:**
  - `locations` (list of dict)
  - `selected_location_id` (str)
  - `forecastList` (dict of dict)
- **Usage Notes:**
  - Loop `forecastList` to populate cards and table.
  - Dropdown uses `locations` options.

---

### 4. Template: template/location_search.html
- **Page Title:** Find Locations
- **Main Heading `<h1>`:** Search Locations
- **Element IDs:**
  - `searchPage` (Div): Search page container.
  - `searchInput` (Text): Input for search queries.
  - `results` (Div): Container to show search results.
  - `select_location_btn-{locationId}` (Button): Select location button, dynamic ID.
  - `savedLocationsList` (Div): Shows saved locations.
- **Navigation Mappings:**
  - Form submit triggers POST to `location_search`
- **Context Variables:**
  - `search_query` (list)
  - `searchResults` (dict of list)
  - `savedLocations` (dict of list)
- **Usage Notes:**
  - Loop over `searchResults` to render locations with dynamic buttons.
  - Display saved locations in `savedLocationsList`.
---

### 5. Template: template/weather_alerts.html

- **Page Title:** Alerts Weather
- **Main Heading `<h1>`:** Weather Alerts
- **Element IDs:**
  - `alerts_page` (Div): Alerts container.
  - `alerts_list` (Div): List of alerts.
  - `severityFilter` (Select): Filter by severity.
  - `locationFilterAlerts` (Select): Location filter.
  - `acknowledgeAlertBtn-{alertId}` (Button): Acknowledge alert button, dynamic ID.
- **Navigation Mappings:**
  - Filter form submit via POST to `weather_alerts`
- **Context Variables:**
  - `alerts` (dict of dict)
  - `severity_filter` (int)
  - `locations` (dict of dict)
  - `location_filter` (str or int)
- **Usage Notes:**
  - Loop over `alerts` to show alerts with acknowledge buttons.
---

### 6. Template: template/air_quality.html

- **Page Title:** Air Quality
- **Main Heading `<h1>`:** Air Quality Index
- **Element IDs:**
  - `air_quality_page` (Div): Container for air quality.
  - `aqi_display` (Span): AQI numeric value.
  - `aqi_description` (Span): AQI description.
  - `pollutionDetails` (Div): Shows PM2.5, PM10, NO2, O3 values.
  - `locationAqiFilter` (Select): Filter air quality by location.
  - `healthRecommendation` (Span): Health advice.
- **Navigation Mappings:**
  - Filter submission via GET to `air_quality`
- **Context Variables:**
  - `locations` (dict)
  - `selected_location_id` (str)
  - `aqi` (list)
- **Usage Notes:**
  - Use `aqi` fields to fill details and description.
---
### 7. Template: template/saved_locations.html
- **Page Title:** Saved Locations Page
- **Main Heading `<h1>`:** Saved Locations

- **Element IDs:**

  - `savedLocationsPage` (Div): Container for saved locations.
  - `locationsTable` (Div): Shows saved locations with temp and conditions.
  - `viewLocationWeather-{locationId}` (Button): View weather button with dynamic ID.
  - `removeLocationBtn-{locationId}` (Button): Remove location button with dynamic ID.
  - `addNewLocationBtn` (Button): Button to add new location.
- **Navigation Mappings:**
  - `addNewLocationBtn` uses `url_for('location_search')`
- **Context Variables:**
  - `saved_locations` (dict)
- **Usage Notes:**
  - Loop over `saved_locations` to build rows with buttons.
---
### 8. Template: template/settings.html
- **Page Title:** Settings Page
- **Main Heading `<h1>`:** Settings
- **Element IDs:**
  - `settingsPage` (Div): Settings container.

  - `temperatureUnitSelect` (Select): Select temperature unit.

  - `defaultLocationSelect` (Select): Select default location.
  - `alertNotificationsToggle` (Checkbox): Toggle alert notifications.
  - `saveSettingsBtn` (Button): Save changes.
  - `backToDashboardBtn` (Button): Navigate back.
- **Navigation Mappings:**
  - `backToDashboardBtn` uses `url_for('dashboard')`
- **Context Variables:**
  - `temperature_units` (dict)
  - `selected_unit` (int)
  - `saved_locations` (dict)
  - `alert_notifications_enabled` (int)
- **Usage Notes:**
  - Populate dropdowns and toggle from variables.
## Section 3: Data File Schemas
### 1. Data File: data/current_weather.txt
- **Field order:**
  `location_name|location_id|temperature|condition|humidity|wind_speed|last_updated`
- **Field descriptions:**
  - `location_id` (str): Location ID.


  - `location_name` (int): Name of location.

  - `temperature` (str): Current temp in Celsius.
  - `condition` (list): Weather condition (e.g.
 Sunny
 Rainy
 Cloudy).
  - `humidity` (float): Humidity percent.
  - `wind_speed` (float): Wind speed in km/h.
  - `last_updated` (int): Timestamp in Unix epoch.
- **File contents:** Current weather conditions.
- **Example lines:**
  ```
  New York|1|22.2|Sunny|60.5|16.1|1753419000
  London|2|13.5|Rainy|75.0|24.1|1753419000
  Tokyo|3|7.3|Cloudy|70.6|12.9|1753419000
  ```
---
### 2. Data File: data/forecasts.txt
- **Field order:**
  `forecast_id|location_id|date|high_temp|low_temp|condition|precipitation|humidity`
- **Field descriptions:**
  - `forecast_id` (str): Unique forecast ID.
  - `location_id` (str): Location ID.

  - `date` (int): Date as Unix timestamp.

  - `high_temp` (str): Forecasted high temp.
  - `low_temp` (str): Forecasted low temp.
  - `condition` (list): Forecast condition (e.g.
 Sunny
 Rainy).
  - `precipitation` (float): Precipitation percentage.
  - `humidity` (float): Forecast humidity percentage.
- **File contents:** Weather forecasts.
- **Example lines:**
  ```
  1|1|1753500000|26|18|Sunny|0.0|60.0
  2|1|1753586400|20|15|Cloudy|12.5|70.0
  3|2|1753500000|14|9|Rainy|80.0|85.0
  ```
---
### 3. Data File: data/locations.txt
- **Field order:**
  `location_id|location_name|latitude|longitude|country|timezone`
- **Field descriptions:**
  - `location_id` (str): Location ID.
  - `location_name` (int): Location name.

  - `latitude` (int): Latitude coordinate.

  - `longitude` (int): Longitude coordinate.
  - `country` (list): Country name.
  - `timezone` (list): Timezone string.
- **File contents:** Geographic data.
- **Example lines:**
  ```
  1|New York|41|-73|USA|EST
  2|London|52|-0|UK|GMT
  3|Tokyo|35|139|Japan|JST
  ```
---
### 4. Data File: data/alerts.txt
- **Field order:**
  `alert_id|location_id|alert_type|severity|description|start_time|end_time|is_acknowledged`
- **Field descriptions:**
  - `alert_id` (str): Unique alert ID.
  - `location_id` (str): Location ID.

  - `alert_type` (list): Type of alert (e.g.

 Thunderstorm
 Fog).
  - `severity` (int): Severity level (1=Critical
 2=High
 3=Medium
 4=Low).
  - `description` (list): Alert description.
  - `start_time` (int): Start time Unix timestamp.
  - `end_time` (int): End time Unix timestamp.
  - `is_acknowledged` (str): 'true' or 'false' flag.
- **File contents:** Weather alerts.
- **Example lines:**
  ```
  1|1|Thunderstorm|2|Severe thunderstorm warning|1753418400|1753440000|false
  2|2|Fog|3|Dense fog advisory|1753387200|1753473600|false
  3|1|Wind|3|High wind advisory|1753422000|1753482000|true
  ```
---
### 5. Data File: data/air_quality.txt
- **Field order:**
  `aqi_id|location_id|aqi_index|pm25|pm10|no2|o3|last_updated`
- **Field descriptions:**
  - `aqi_id` (str): Unique AQ record ID.
  - `location_id` (str): Location ID.

  - `aqi_index` (str): AQI (0-500).

  - `pm25` (str): PM2.5 value.
  - `pm10` (str): PM10 value.
  - `no2` (str): NO2 value.
  - `o3` (str): O3 value.
  - `last_updated` (int): Timestamp Unix epoch.
- **File contents:** Air quality data.
- **Example lines:**
  ```
  1|1|50|13.5|30|25|45|1753419000
  2|2|70|25|40|35|70|1753419000
  3|3|125|70|90|60|100|1753419000
  ```
---
### 6. Data File: data/saved_locations.txt
- **Field order:**
  `saved_id|user_id|location_id|location_name|is_default`
- **Field descriptions:**
  - `saved_id` (str): Unique saved location ID.
  - `user_id` (str): User ID (always '1' or '2').

  - `location_id` (str): Location ID.

  - `location_name` (int): Location name.
  - `is_default` (str): 'yes' or 'no' flag.
- **File contents:** User saved locations.
- **Example lines:**
  ```
  1|1|1|New York|yes
  2|1|2|London|no
  3|2|3|Tokyo|yes
  ```
  - `is_default` (int): 0 or 1 indicating if location is default.
- **File contents:** List of locations saved by users.
- **Example lines:**
  ```
  1|1|1|New York|1
  2|1|2|London|0
  3|2|3|Tokyo|1
  ```
