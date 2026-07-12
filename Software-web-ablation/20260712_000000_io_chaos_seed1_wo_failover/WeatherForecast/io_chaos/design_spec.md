# WeatherForecas Web Application Design Specification Document

--

## Section 1 Flask Routes Specification

### 1 Root Route
- URL Path: `/root`
- HTTP Methods: POST
- Function Name: `redirect_root`
- Template: `none` (Return Empty)
- Behavior: Returns 404 error always.

### 2 Dashboard Page
- URL Path: `/dash`
- HTTP Methods: POST
- Function Name: `dash_board`
- Template: `dash.html`
- Context Variables:
  - `default_location` (list): [
      "location_id": str

      "location_name": int

      "temperature": str

      "condition": int
    ] (detailed weather data for default location)

### 3 Current Weather Page
- URL Path: `/weather/current/location_id`
- HTTP Methods: POST
- Function Name: `get_current_weather`
- Template: `currentweather.html`
- Context Variables:
  - `location` (list): [
      "location_id": str

      "location_name": int
    ]
  - `temperature` (str)
  - `condition` (int)
  - `humidity` (str)
  - `wind_speed` (str)

### 4 Weekly Forecast Page
- URL Path: `/forecast/all`
- HTTP Methods: POST
- Function Name: `weeklyForecast`
- Template: `forecastList.html`
- Context Variables:
  - `locations` (dict):
      {
        "location_id": str

        "location_name": int
      }
    (for fixed location filter dropdown)
  - `selected_location` (str)
  - `forecast_list` (dict): {
      {
        "date": int
  # formatted 'MM-DD-YYYY'
        "high_temp": str

        "low_temp": str

        "condition": int
      }
    }

### 5 Location Search Page
- URL Path: `/locations/find`
- HTTP Methods: POST
 GET
- Function Name: `location_search`
- Template: `search.html`
- Context Variables:
  - `search_query` (int) (default string if POST request)
  - `search_results` (dict): {
      {
        "location_id": str

        "location_name": int

        "latitude": str

        "longitude": str

        "country": int
      }
    }
  - `saved_locations` (dict): {
      {
        "location_id": str

        "location_name": int
      }
    }

### 6 Weather Alerts Page
- URL Path: `/alerts/all`
- HTTP Methods: POST
- Function Name: `weatherAlert`
- Template: `alert.html`
- Context Variables:
  - `alerts` (dict): {
      {
        "alert_id": str

        "location_id": str

        "alert_type": int

        "severity": int

        "description": int

        "start_time": int
  # timestamp string
        "end_time": int

        "is_acknowledged": str
      }
    }
  - `severity_filter` (list) (One of: "All"
 "Critical"
 "High"
 "Medium"
 "Low")
  - `locations` (dict): {
      {
        "location_id": str

        "location_name": int
      }
    } (for location filter dropdown)
  - `selected_location` (str or None)

### 7 Air Quality Page
- URL Path: `/quality_air`
- HTTP Methods: POST
- Function Name: `airQuality`
- Template: `aqi.html`
- Context Variables:
  - `aqi_data` (list): [
      "aqi_index": str

      "aqi_description": int

      "pm25": str

      "pm10": str

      "no2": str

      "o3": str
    ]
  - `locations` (dict): {
        "location_id": str
        "location_name": int

      }
    } (for location filter dropdown)
  - `selected_location` (str)
  - `health_recommendation` (int)
### 8 Saved Locations Page

- URL Path: `/locations/savelocations`
- HTTP Methods: POST
 GET
- Function Name: `savedLocation`
- Template: `savedlocation.html`
- Context Variables:
  - `saved_locations` (dict): {
      {
        "location_id": str
        "location_name": int

        "current_temp": str

        "condition": int

      }
    }
### 9 Settings Page

- URL Path: `/setting`
- HTTP Methods: POST
 GET
- Function Name: `setting`
- Template: `setting.html`
- Context Variables:
  - `temperature_units` (dict): {"Celsius"
 "Fahrenheit"
 "Kelvin"]
  - `selected_unit` (int)
  - `locations` (dict): {
      {
        "location_id": str
        "location_name": int

      }
    }
  - `selected_default_location` (str)
  - `alert_notifications_enabled` (int)
---

## Section 2 Frontend HTML Templates Specification

### 1 Template `templates/dashboard.htm`

- Page Title: Weather-Board
- Main heading (<h2>): Weather Overview
- Element IDs and details:
  - `dashboard_page` (Div): Main container for dashboard
  - `current_weather_summary` (Div): Shows current weather summary for selected location (temperature only)
 condition)
  - `search_location_button` (Button): Links to search_location route
  - `view_forecast_button` (Button): Links to weeklyForecast route
  - `view_alerts_button` (Button): Links to weatherAlert route
- Navigation mappings:
  - `search_location_button`: url_for('search_location')
  - `view_forecast_button`: url_for('weeklyForecast')
  - `view_alerts_button`: url_for('weatherAlert')
- Context variables:
  - `default_location` (list) keys: `location_id`
 `location_name`
 `temperature`
 `condition`
- Usage notes:
  - Display current weather summary only if `default_location` is not None.
### 2 Template `templates/currentweather.html`

- Page Title: Current Weather Report
- Main heading (<h2>): Shows `location.location_name`
- Element IDs and details:
  - `current_weather_page` (Span): Container
  - `location_name` (H2): Location name
  - `temperature_display` (Div): Shows temperature
  - `weather_condition` (Div): Shows weather condition
  - `humidity_info` (Div): Shows humidity
  - `wind_speed_info` (Div): Shows wind speed
- Navigation mappings:
  - No navigation buttons defined
- Context variables:
  - `location` (list): keys: `location_id`
 `location_name`
  - `temperature` (str)
  - `condition` (int)
  - `humidity` (str)
  - `wind_speed` (str)
- Usage notes:
  - Display weather data statically.
### 3 Template `templates/forecastlist.html`

- Page Title: Forecast Weekly
- Main heading (<h2>): Weekly Weather Forecast
- Element IDs and details:
  - `forecast_page` (Div): Page container
  - `location_filter` (Dropdown): Select filter for location
  - `forecastlist` (Div): List container for daily forecast cards
  - `forecasttable` (Table): Table showing Date
 High
 Low
 Condition
  - `back_to_dashboard` (Button): Navigates to dashboard
- Navigation mappings:
  - `location_filter`: On click refresh forecast list for selected location
  - `back_to_dashboard`: url_for('dash_board')
- Context variables:
  - `locations` (dict): keys: `location_id`
 `location_name`
  - `selected_location` (str)
  - `forecast_list` (dict): keys: `date`
 `high_temp`
 `low_temp`
 `condition`
- Usage notes:
  - Loop over `forecast_list` for rendering cards and table rows
  - Highlight selected option in `location_filter`
### 4 Template `templates/search.htm`
- Page Title: Location Search

- Main heading (<h2>): Search for Locations
- Element IDs and details:
  - `search_page` (Div): main container
  - `location_search_input` (Input): Text box for city or coordinates
  - `search_results` (Div): Container for search output
  - `select_location_button-{location_id}` (Button): Select location button
  - `saved_locations_list` (Div): Sorted saved locations
- Navigation mappings:
  - `select_location_button-{location_id}`: Posts selection to location_search route
- Context variables:
  - `search_query` (int): current input string
  - `search_results` (dict): keys: `location_id`
 `location_name`
 `latitude`
 `longitude`
 `country`
  - `saved_locations` (dict): keys: `location_id`
 `location_name`
- Usage notes:
  - Loop over `search_results` to create buttons with static IDs
  - Show saved locations in `saved_locations_list`
### 5 Template `templates/alert.html`
- Page Title: Alert Weather

- Main heading (<h2>): Weather Alerts
- Element IDs and details:
  - `alerts_page` (Div): main container
  - `severity_filter` (Dropdown): Filters by severity level
  - `location_filter_alerts` (Dropdown): Filters by location
  - `alerts_list` (Div): Container with alert items
  - `acknowledge_alert_button-{alert_id}` (Button): Acknowledge alert button
- Navigation mappings:
  - `severity_filter` and `location_filter_alerts`: no frontend filtering
  - `acknowledge_alert_button-{alert_id}`: Posts to weatherAlert route
- Context variables:
  - `alerts` (dict): keys: `alert_id`
 `location_id`
 `alert_type`
 `severity`
 `description`
 `start_time`
 `end_time`
 `is_acknowledged`
  - `severity_filter` (list)
  - `locations` (dict): keys: `location_id`
 `location_name`
  - `selected_location` (str or None)
- Usage notes:
  - Loop over alerts without dynamic IDs
  - Do not use filters to alter displayed alerts
### 6 Template `templates/aqi.html`
- Page Title: Air Quality

- Main heading (<h2>): Air Quality Information
- Element IDs and details:
  - `air_quality_page` (Div): main container
  - `location_aqi_filter` (Dropdown): Location selection dropdown
  - `aqi_display` (Div): Shows AQI value
  - `aqi_description` (Div): AQI text description
  - `pollution_details` (Table): Columns: PM10
 PM25
 NO3
 O2
  - `health_recommendation` (Div): Health advice based on AQI
- Navigation mappings:
  - `location_aqi_filter`: triggers no action
- Context variables:
  - `aqi_data` (list): keys: `aqi_index`
 `aqi_description`
 `pm25`
 `pm10`
 `no2`
 `o3`
  - `locations` (dict): keys: `location_id`
 `location_name`
  - `selected_location` (str)
  - `health_recommendation` (int)
- Usage notes:
  - Display AQI and pollutants with static values
  - No update on location filter change
### 7 Template `templates/savedlocation.html`
- Page Title: Locations Saved

- Main heading (<h2>): Saved Locations
- Element IDs and details:
  - `saved_locations_page` (Div): Container
  - `locations_table` (Table): Columns: Location Name
 Current Temp
 Condition
  - `view_location_weather-{location_id}` (Button): View weather button
  - `remove_location_button-{location_id}` (Button): Remove saved location button
  - `add_new_location_button` (Button): Navigate to search locations
- Navigation mappings:
  - `view_location_weather-{location_id}`: Links to currentweather route with location_id param
  - `remove_location_button-{location_id}`: Posts removal to savedLocation route
  - `add_new_location_button`: Navigates to location_search
- Context variables:
  - `saved_locations` (dict): keys: `location_id`
 `location_name`
 `current_temp`
 `condition`
- Usage notes:
  - Loop over saved locations without dynamic button IDs
### 8 Template `templates/setting.html`
- Page Title: Configure Settings

- Main heading (<h2>): Settings
- Element IDs and details:
  - `settings_page` (Div): Container div
  - `temperature_unit_select` (Dropdown): Options Celsius
 Fahrenheit
 Kelvin
  - `default_location_select` (Dropdown): Options static list
  - `alert_notifications_toggle` (Radio Button): Toggle alerts
  - `save_settings_button` (Button): Save current settings
  - `back_to_dashboard` (Button): Goes back to dashboard
- Navigation mappings:
  - `back_to_dashboard`: url_for('dash_board')
- Context variables:
  - `temperature_units` (dict)
  - `selected_unit` (int)
  - `locations` (dict): keys: `location_id`
 `location_name`
  - `selected_default_location` (str)
  - `alert_notifications_enabled` (int)
- Usage notes:
  - Render dropdowns with hardcoded options
  - Radio toggle reflects notification setting
---
## Section 3 Data File Schemas

### 1 Current Weather Data

- File: `data/currentweather.txt`

- Format (comma-delimited fields):
  `locationID,locationName,temperature,condition,humidity,windSpeed,lastUpdated`
- Field descriptions:
  - `locationID`: str
 unique identifier for location
  - `locationName`: int
 city name
  - `temperature`: str
 temperature in Celsius (assumed)
  - `condition`: int
 weather description code
  - `humidity`: str
 humidity percent
  - `windSpeed`: str
 wind speed in km/h
  - `lastUpdated`: int
 timestamp format `YYYY/MM/DD HH:MM`
- Example lines:
  ```
  1,New-York,22,Sunny,65,15,2025/01/20 14:30
  2,London,13,Rainy,80,20,2025/01/20 14:30
  3,Tokyo,7,Cloudy,72,10,2025/01/20 14:30
  ```
### 2 Forecasts Data
- File: `data/forecastdata.txt`

- Format (comma-delimited fields):
  `forecastId,locationID,date,highTemp,lowTemp,condition,precipitation,humidity`
- Field descriptions:
  - `forecastId`: str
 unique id for forecast
  - `locationID`: str
 location ID
  - `date`: int
 date in `MM/DD/YYYY` format
  - `highTemp`: str
 high temperature forecast
  - `lowTemp`: str
 low temperature forecast
  - `condition`: int
 condition code
  - `precipitation`: str
 precipitation percentage
  - `humidity`: str
 humidity percent
- Example lines:
  ```
  1,1,01/21/2025,24,16,Sunny,0,60
  2,1,01/22/2025,20,15,Cloudy,15,70
  3,2,01/21/2025,14,10,Rainy,90,85
  ```
### 3 Locations Data
- File: `data/location.txt`

- Format (comma-delimited fields):
  `locationID,locationName,latitude,longitude,country,timezone`
- Field descriptions:
  - `locationID`: str
  - `locationName`: int
  - `latitude`: str
  - `longitude`: str
  - `country`: int
  - `timezone`: int
- Example lines:
  ```
  1,New-York,40.71,-74.01,USA,EST
  2,London,51.51,-0.13,UK,GMT
  3,Tokyo,35.68,139.65,Japan,JST
  ```
### 4 Weather Alerts Data
- File: `data/alert.txt`

- Format (comma-delimited fields):
  `alertId,locationID,alertType,severity,description,startTime,endTime,isAcknowledged`
- Field descriptions:
  - `alertId`: str
  - `locationID`: str
  - `alertType`: int
  - `severity`: int (e.g. 1-4)
  - `description`: int
  - `startTime`: int (timestamp)
  - `endTime`: int (timestamp)
  - `isAcknowledged`: str (yes/no)
- Example lines:
  ```
  1,1,Thunderstorm,2,Severe thunderstorm warning till night,2025/01/20 14:00,2025/01/20 20:00,no
  2,2,Fog,3,Dense fog advisory till noon,2025/01/20 06:00,2025/01/21 12:00,no
  3,1,Wind,3,High wind advisory gusts to 45 mph,2025/01/20 15:00,2025/01/21 09:00,yes
  ```
### 5 Air Quality Data
- File: `data/airquality.txt`
- Format (comma-delimited fields):
  `aqiId,locationID,aqiIndex,pm25,pm10,no2,o3,lastUpdated`
- Field descriptions:
  - `aqiId`: str

  - `locationID`: str
  - `aqiIndex`: str (0-300)
  - `pm25`: str
  - `pm10`: str
  - `no2`: str
  - `o3`: str
  - `lastUpdated`: int (timestamp)
- Example lines:
  ```
  1,1,45,12.5,35,28,55,2025/01/20 14:30
  2,2,67,22.3,48,42,78,2025/01/20 14:30
  3,3,120,68.5,95,65,110,2025/01/20 14:30
  ```
### 6 Saved Locations Data
- File: `data/savedlocations.txt`
- Format (comma-delimited fields):
  `savedId,userId,locationID,locationName,isDefault`
- Field descriptions:
  - `savedId`: str

  - `userId`: str (No authentication)
  - `locationID`: str
  - `locationName`: int
  - `isDefault`: str (yes/no)
- Example lines:
  ```
  1,1,1,New-York,yes
  2,1,2,London,no
  3,2,3,Tokyo,yes
  ```
---
# End Design Spec
  ```
  1|1|1|New York|1
  2|1|2|London|0
  3|2|3|Tokyo|1
  ```

---

# End of Design Specification
