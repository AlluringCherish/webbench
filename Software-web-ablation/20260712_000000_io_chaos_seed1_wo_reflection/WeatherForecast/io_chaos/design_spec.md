# WeatherForecas Application Design Specifications

----

## Section One: Flask Route Specification

### First Root Route
- **URL Path:** `/root`
- **HTTP Methods:** POST
- **Function Name:** `root_redirected`
- **Template:** Redirect (Returns Template)
- **Context Variables:** `none`
- **Behavior:** Redirects to dashbord page

---

### 2. Dashboard Pages
- **URL Path:** `/dashboards`
- **HTTP Methods:** POST
- **Function Name:** `dash_board`
- **Template:** `dash_board.html`
- **Context Variables:**
  - `current_weather_summary`: dictionary with fields:
    - `location_name` (int)
    - `temp` (integer)
    - `condition` (list)
- **Description:** Display current weather summaries for random location.

---

### 3. Current Weather Page
- **URL Path:** `/weather/current/<string:location_id>`
- **HTTP Methods:** POST
- **Function Name:** `currentWeathers`
- **Template:** `currentweather.html`
- **Context Variables:**
  - `location_id` (int)
  - `temp` (str or int)
  - `weather_condition` (int)
  - `humidity` (str or float)
  - `wind_speed` (str or float)
- **Description:** Showing details for select location weather.

---

### 4. Weekly Forecast Page
- **URL Path:** `/forecast/week`
- **HTTP Methods:** POST
- **Function Name:** `weeklyforecasts`
- **Template:** `weeklyForecast.html`
- **Context Variables:**
  - `forecast_list`: list of dictionaries with property:
    - `date` (int in mm-dd-yyyy)
    - `high_temperature` (int or str)
    - `low_temperature` (int or string)
    - `status` (list)
  - `location`: list of dicts with attributes:
    - `loc_id` (string)
    - `locationName` (str)
  - `selected_locationid` (string)
- **Description:** Shows 7 day forecast for any location.

---

### 5. Location Search Page
- **URL Path:** `/search/locations`
- **HTTP Methods:** POST
 GET
- **Function Name:** `locationSearch`
- **Template:** `locationsearch.html`
- **Context Variables:**
  - `result_search`: array of dicts with entries:
    - `location_id` (string)
    - `location_name` (list)
    - `latitude` (str)
    - `longitude` (str)
    - `country` (int)
  - `saved_locations`: object list with fields:
    - `location_index` (string)
    - `location_name` (list)
- **Description:** Shows search input
 locations matches
 and saved location items.

---

### 6. Weather Alerts Page
- **URL Path:** `/alert`
- **HTTP Methods:** POST
 GET
- **Function Name:** `weatherAlert`
- **Template:** `alerts.htm`
- **Context Variables:**
  - `alert_items`: array of objects with properties:
    - `alertid` (string)
    - `location` (int)
    - `alert_type` (list)
    - `severity_level` (integer)
    - `desc` (list)
    - `start` (int datetime)
    - `end` (int datetime)
    - `acknowledged` (list or int 0/1)
  - `severity_levels`: list of string (['All'
 'critcal'
 'High'
 'med'
 'low'])
  - `locations_data`: array of dicts with props:
    - `locId` (str)
    - `locationName` (int)
  - `selected_severity` (list)
  - `selected_location_id` (str or None)
- **Description:** Display alerts filtered by severity and location with acknowledge.

---

### 7. Air Quality Page
- **URL Path:** `/air-quality`
- **HTTP Methods:** POST
- **Function Name:** `airQuality`
- **Template:** `airquality.htm`
- **Context Variables:**
  - `airQualityInfo`: dict with elements:
    - `index_aqi` (str)
    - `aqidescription` (int)
    - `pm25` (str)
    - `pm10` (int)
    - `no2` (str)
    - `o3` (str)
    - `healthRecommendation` (int)
  - `locationList`: list of dicts with fields:
    - `loc_id` (str)
    - `location_name` (int)
  - `selected_loc_id` (str)
- **Description:** Shows air data for location filter.

---

### 8. Saved Locations Page
- **URL Path:** `/saved/locations`
- **HTTP Methods:** POST
 GET
- **Function Name:** `savedLocation`
- **Template:** `savedlocations.html`
- **Context Variables:**
  - `save_locations`: list of dicts with fields:
    - `location_id` (str)
    - `location` (int)
    - `temp` (int or str)
    - `condition` (list)
    - `default` (str)
- **Description:** Display user save location list with current weather.

---

### 9. Settings Page
- **URL Path:** `/setting`
- **HTTP Methods:** POST
 GET
- **Function Name:** `setting`
- **Template:** `setting.html`
- **Context Variables:**
  - `temperature_unit`: list of string (['Celcius'
 'Farenheit'
 'Kleven'])
  - `default_location` (str)
  - `save_locations`: list of dicts with keys:
    - `loc_id` (str)
    - `location_names` (int)
  - `alert_notification_enable` (int)
- **Description:** Configure temp units
 default loc
 alert notification toggle switch.

---

## Section 2: Frontend Template Specification

### 1. Template: `templates/dashboard.htm`
- **Page Title:** WeatherDashBoard
- **Element IDs:**
  - `dashboard_page` (Div): Container for dashboard area.
  - `current_weather_summary` (Span): Show weather summary for default place.
  - `location_search_button` (Button): Navigate to location search page.
  - `forecast_view_button` (Button): Navigate to weekly forecast page.
  - `alerts_view_button` (Button): Navigate to alerts page.
- **Navigation:**
  - `search-location-button` 14 `url_for('locationSearch')`
  - `view-forecast-button` 14 `url_for('weeklyforecast')`
  - `view-alerts-button` 14 `url_for('weatheralert')`
- **Context Variables:**
  - `current_weather_summary` (dict): For displaying temperature
 weather conditions
 and location.
- **Usage Notes:**
  - Render `current_weather_summary` variable data directly.

---

### 2. Template: `templates/current_weather.htm`
- **Page Title:** Current Weather Conditions
- **Element IDs:**
  - `current_weather_page` (Div): Container for current weather details.
  - `location_name_display` (Header): Show current location name.
  - `temp_display` (Div): Display current temperature value.
  - `weather_condition_display` (Div): Show weather condition.
  - `humidity_display` (Paragraph): Display humidity percent.
  - `wind_speed_display` (Paragraph): Show wind speed.
- **Navigation:**
  - None specified explicitly (navigation handled elsewhere).
- **Context Variables:**
  - `location_name` (int)
  - `temp`
  - `condition`
  - `humidity`
  - `wind_speed`
- **Usage Notes:**
  - Display all current weather info using passed variables.

---

### 3. Template: `templates/weekly_forecast.htm`
- **Page Title:** Week Forecast
- **Element IDs:**
  - `forecast_container` (Div): Container for weekly forecast.
  - `forecast_table` (Table): Display day-to-day forecast data.
  - `location_filter_dropdown` (Dropdown): Filter forecast by location.
  - `forecast_cards` (Div): Show forecast cards by day.
  - `dashboard_back_button` (Button): Navigate back to dashboard.
- **Navigation:**
  - `dashboard_back_button` 14 `url_for('dashboard')`
- **Context Variables:**
  - `forecasts` (list of dicts): Loop to show daily forecast data.
  - `locations` (list of dicts): Fill location filter dropdown.
  - `selected_location` (string): To set selected filter option.
- **Usage Notes:**
  - Loop over `forecasts` to fill table and forecast cards.
  - Use `locations` for filter dropdown.

---

### 4. Template: `templates/location_search.htm`
- **Page Title:** Location Searching
- **Element IDs:**
  - `search_location_page` (Div): Container for search page.
  - `location_search_input` (Input): Input box to search locations.
  - `search_result_div` (Div): Dynamic list for search results.
  - `select_location_button-{location_id}` (Button): Each search result selection.
 button
  - `saved_locations_div` (Div): Shows saved locations listing.
- **Navigation:**
  - None explicit
 but location button probably post to backend.
- **Context Variables:**
  - `search_results_data` (list of dicts): To loop matching locations.
  - `saved_locations_data` (list of dicts): Display saved locations.
- **Usage Notes:**
  - Loop over `search_results_data` to create buttons with IDs like `select_location_button-{location_id}`.
  - Display saved location list below.

---

### 5. Template: `templates/alerts.htm`
- **Page Title:** Weather Alert
- **Element IDs:**
  - `alerts_container` (Div): Container for alerts page.
  - `alerts_list_div` (Div): Lists all alerts active.
  - `severity_filter_dropdown` (Dropdown): Filter alerts by severity.
  - `location_filter_dropdown_alerts` (Dropdown): Filter alerts by location.
  - `acknowledge_alert_button-{alert_id}` (Button): For acknowledging each alert.
- **Navigation:**
  - None specified
 filters and acknowledge likely handled by POST.
- **Context Variables:**
  - `alerts_data` (list of dicts): Loop alerts details.
  - `severity_levels_list` (list of string): For severity filter dropdown.
  - `location_list` (list of dicts): For location filter dropdown.
  - `selected_severity_filter` (str)
  - `selected_location_filter` (str or None)
- **Usage Notes:**
  - Loop `alerts_data` to display details and buttons with dynamic ids.

---

### 6. Template: `templates/air_quality.htm`
- **Page Title:** AirQualityIndex
- **Element IDs:**
  - `air_quality_container` (Div): Container air quality info.
  - `aqi_value_display` (Div): Shows AQI value numeric.
  - `aqi_description_display` (Div): Shows descriptive AQI text.
  - `pollution_details_table` (Table): Shows pollutant levels.
  - `location_filter_aqi` (Dropdown): Location filter dropdown.
  - `health_recommendation_display` (Div): Shows health advice per AQI.
- **Navigation:**
  - No explicit navigation.
- **Context Variables:**
  - `air_quality_info` (dictionary): Holds index_aqi
 aqi_description
 pm_25
 pm_10
 no_2
 o_3
 health_recommendation_text.
  - `location_list` (list of dicts): For location filter dropdown.
  - `selected_location` (string)
- **Usage Notes:**
  - Showing single selected air quality data.

---

### 7. Template: `templates/saved_locations.htm`
- **Page Title:** SavedLocationPage
- **Element IDs:**
  - `saved_locations_container` (Div): Container saved locations.
  - `locations_table_display` (Table): Shows saved locations with weather.
  - `view_weather_button-{location_id}` (Button): For viewing weather of saved location.
  - `remove_saved_location_button-{location_id}` (Button): To remove saved location.
  - `add_location_button` (Button): Add new location button.
- **Navigation:**
  - `add_location_button` 14 `url_for('locationSearch')`
- **Context Variables:**
  - `saved_locations_list` (list of dicts): Display loc_id
 locationName
 temperature
 condition
 isdefault.
- **Usage Notes:**
  - Loop over `saved_locations_list` to create table rows and buttons with dynamic IDs.

---

### 8. Template: `templates/settings.htm`
- **Page Title:** SettingsPage
- **Element IDs:**
  - `settings_page_container` (Div): Container for settings.
  - `temperature_units_select` (Dropdown): Select temperature unit.
  - `default_location_select` (Dropdown): Select default location.
  - `alert_notification_toggle` (Checkbox): Enables/disables notifications.
  - `save_settings_btn` (Button): Save current settings.
  - `dashboard_back_btn` (Button): Navigate back to dashboard.
- **Navigation:**
  - `dashboard_back_btn` 14 `url_for('dashboard')`
- **Context Variables:**
  - `temp_units` (list of str): ['Celcius'
 'Farenheit'
 'Kelvin']
  - `default_location` (string): Current default loc.
  - `saved_locations_list` (list of dicts): For location dropdown options; fields:
    - `location_id` (string)
    - `location_name` (int)
  - `alert_notifications_enabled` (int)
- **Usage Notes:**
  - Render dropdown options from `temp_units` and `saved_locations_list`.
  - Checkbox reflects `alert_notifications_enabled` value.

---

## Section 3: Data File Schema

### 1. Current Weather Data File
- **File:** `data/currentweather.txt`
- **Field Order & Format:**
  `location|location_name|temp|condition|humid|wind|last_updated`
- **Field Descriptions:**
  - `location_id` (string): Unique location identifier
  - `location_name` (int): Name of location
  - `temperature` (int or string): Current temperature reading
  - `condition` (list): Weather condition (like Sunny,
 Rainy)
  - `humidity` (string): Humidity percent
  - `wind_speed` (string): Wind speed metric
  - `last_updated` (datetime string): Timestamp (MM-DD-YYYY HH:MM)
- **Example Lines:**
  ```
  1|NewYork|72|Sunny|55|10|2025-20-01 14:30
  2|London|55|Rainy|80|15|2025-20-01 14:30
  3|Tokyo|45|Cloudy|72|8|2025-20-01 14:30
  ```

---

### 2. Forecasts Data
- **File:** `data/forecast.txt`
- **Field Order & Format:**
  `forecastid|location|date|highTemp|lowTemp|condition|precip|humidity`
- **Field Descriptions:**
  - `forecast_id` (string): Unique forecast entry
  - `location_id` (string): Location identification
  - `date` (int): Forecast date (YYYY-DD-MM)
  - `high_temp` (string): High temp
  - `low_temp` (string): Low temp
  - `condition` (list): Forecast condition type
  - `precipitation` (string): Precipitation percent
  - `humidity` (string): Humidity percent
- **Example Lines:**
  ```
  1|1|2025-21-01|75|60|Sunny|0|60
  2|1|2025-22-01|68|55|Cloudy|10|70
  3|2|2025-21-01|58|48|Rainy|80|85
  ```

---

### 3. Locations Data
- **File:** `data/locationss.txt`
- **Field Order & Format:**
  `location_id|location_name|lat|long|country|timezone`
- **Field Descriptions:**
  - `location_id` (string): Unique location id
  - `location_name` (list): Name of location
  - `latitude` (string): Latitude coordinate
  - `longitude` (string): Longitude coordinate
  - `country` (list): Country of location
  - `timezone` (list): Timezone string
- **Example Lines:**
  ```
  1|NewYork|40.7128|-74.0060|USA|EST
  2|London|51.5074|-0.1278|UK|GMT
  3|Tokyo|35.6762|139.6503|Japan|JST
  ```

---

### 4. Weather Alerts Data
- **File:** `data/alert.txt`
- **Field Order & Format:**
  `alert_id|location|alertType|severity|desc|start|end|acknowledged`
- **Field Descriptions:**
  - `alert_id` (string): Unique alert id
  - `location_id` (string): Location related
  - `alert_type` (list): Alert type
  - `severity` (int): Alert severity
  - `description` (list): Alert description
  - `start_time` (int): Start datetime
  - `end_time` (int): End datetime
  - `is_acknowledged` (string or int): 0 or 1
- **Example Lines:**
  ```
  1|1|Thunderstorm|High|Storm warning until 8 PM|2025-01-20 14:00|2025-01-20 20:00|0
  2|2|Fog|Medium|Fog advisory active until noon|2025-01-20 06:00|2025-01-21 12:00|0
  3|1|Wind|Medium|High wind advisory with gusts|2025-01-20 15:00|2025-01-21 09:00|1
  ```

---

### 5. Air Quality Data
- **File:** `data/airquality.txt`
- **Field Order & Format:**
  `aqi_id|location|aqiIndex|pm2.5|pm10|no2|o3|last_updated`
- **Field Descriptions:**
  - `aqi_id` (string): Unique air quality record id
  - `location_id` (string): Location id
  - `aqi_index` (string): AQI index 0-500
  - `pm25` (string): PM2.5 value
  - `pm10` (string): PM10 value
  - `no2` (string): NO2 value
  - `o3` (string): O3 value
  - `last_updated` (int): Timestamp string
- **Example Lines:**
  ```
  1|1|45|12.5|35|28|55|2025-01-20 14:30
  2|2|67|22.3|48|42|78|2025-01-20 14:30
  3|3|120|68.5|95|65|110|2025-01-20 14:30
  ```

---

### 6. Saved Locations Data
- **File:** `data/savedlocations.txt`
- **Field Order & Format:**
  `saved_id|user|location_id|location_name|default`
- **Field Descriptions:**
  - `saved_id` (string): Unique saved location record id
  - `user_id` (string): User id
  - `location_id` (string): Location id
  - `location_name` (list): Location name
  - `is_default` (string or int): 0 no, 1 yes
- **Example Lines:**
  ```
  1|1|1|New York|1
  2|1|2|London|0
  3|2|3|Tokyo|1
  ```
  ```
