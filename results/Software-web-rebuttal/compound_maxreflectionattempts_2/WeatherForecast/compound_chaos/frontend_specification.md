# Frontend Template Specifications for Weather Forecast Web Application

This detailed frontend specification covers each template, including file path, page titles, element IDs, element types, purposes, dynamic ID patterns, navigation mappings, context variables with types, loops, conditionals, and dynamic rendering notes.

---

## 1. Dashboard Page
- **Template File:** `templates/dashboard.html`
- **Route Function:** `dashboard` at `/dashboard`
- **Page Title:**
  - In `<title>` tag: "Dashboard"
  - Visible `<h1>` (ID: `dashboard-title`): "Dashboard"

### Element IDs and Purpose
| ID | HTML Element Type | Purpose |
| --- | --- | --- |
| `dashboard-title` | `h1` | Page title heading |
| `saved-locations-list` | `div` | Container listing user saved locations |
| `select-location-button-{location_id}` | `button` | Button to select this saved location (dynamic ID; e.g. `select-location-button-2`)|
| `remove-location-button-{location_id}` | `button` | Button to remove this saved location (dynamic)|
| `default-location-select` | `select` (dropdown) | Dropdown to choose default location from saved locations |
| `current-weather-summary` | `div` | Container showing current weather summary |
| `temperature-display` | `div` or `span` | Displays current temperature with unit |
| `weather-condition` | `div` or `span` | Displays weather condition description |
| `humidity-info` | `div` or `span` | Displays current humidity as percentage |
| `wind-speed-info` | `div` or `span` | Displays wind speed |
| `forecast-table` | `table` | Displays upcoming forecasts
| `aqi-display` | `div` or `span` | Shows Air Quality Index number |
| `aqi-description` | `div` or `span` | Shows AQI description like "Good", "Unhealthy" |
| `alerts-list` | `div` | Lists active alerts for current locations |
| `acknowledge-alert-button-{alert_id}` | `button` | Button to acknowledge an alert (dynamic ID)|
| `alert-notifications-toggle` | `input` (checkbox) | Toggle enable/disable alerts |
| `view-forecast-button` | `button` | Navigation button to Weekly Forecast Page |

### Navigation Mappings
- `select-location-button-{location_id}`: On click, route to current weather page `/weather/current/<location_id>` using
  `{{ url_for('current_weather', location_id=location.location_id) }}`
- `remove-location-button-{location_id}`: Posts to location remove function; form action with CSRF.
- `view-forecast-button`: Link/button directs to weekly forecast page for default/current location:
  `{{ url_for('weekly_forecast', location_id=default_location_id) }}`

### Context Variables Passed
```python
{
  "saved_locations": List[Dict]{"location_id": int, "location_name": str, "is_default": bool},
  "default_location_id": int,
  "current_weather": Dict{"temperature": float, "condition": str, "humidity": int, "wind_speed": float},
  "forecast_list": List[Dict]{"date": str, "high_temp": float, "low_temp": float, "condition": str, "precipitation": int, "humidity": int},
  "air_quality": Dict{"aqi_index": int, "description": str},
  "alerts": List[Dict]{"alert_id": int, "alert_type": str, "severity": str, "description": str, "start_time": str, "end_time": str, "is_acknowledged": bool},
  "alerts_enabled": bool
}
```

### Dynamic Rendering Notes
- Loop over `saved_locations` for location buttons.
- Loop over `forecast_list` to populate `forecast-table` rows.
- Loop over `alerts` to display active alerts.
- Conditional display of alerts only if `alerts_enabled` is `True`.

---

## 2. Settings Page
- **Template File:** `templates/settings.html`
- **Route Function:** `settings` at `/settings`
- **Page Title:**
  - `<title>`: "Settings"
  - `<h1>` (No specific ID needed, but recommended `settings-title`.)

### Element IDs and Purpose
| ID | HTML Element Type | Purpose |
| --- | --- | --- |
| `temperature-unit-select` | `select` | Dropdown to choose temperature unit ("Celsius", "Fahrenheit") |
| `default-location-select` | `select` | Dropdown to select default location from saved locations |
| `save-settings-button` | `button` | Button to save settings |

### Navigation Mappings
- `save-settings-button` triggers POST on `/settings` that saves user preferences.

### Context Variables Passed
```python
{
  "temperature_unit": str,  # "Celsius" or "Fahrenheit"
  "saved_locations": List[Dict]{"location_id": int, "location_name": str},
  "default_location_id": int
}
```

### Dynamic Rendering Notes
- The default selected option in both dropdowns is set via context variables.

---

## 3. Current Weather Page
- **Template File:** `templates/current_weather.html`
- **Route Function:** `current_weather(location_id)` at `/weather/current/<int:location_id>`
- **Page Title:**
  - `<title>`: "Current Weather - {location_name}"
  - `<h1>` (ID: `location-name`): location name display

### Element IDs and Purpose
| ID | HTML Element Type | Purpose |
| --- | --- | --- |
| `location-name` | `h1` | Location name heading |
| `temperature-display` | `div` or `span` | Current temperature with unit |
| `weather-condition` | `div` or `span` | Weather condition text |
| `humidity-info` | `div` or `span` | Humidity percentage |
| `wind-speed-info` | `div` or `span` | Wind speed display |
| `back-to-dashboard` | `button` | Button to navigate back to dashboard |

### Navigation Mappings
- `back-to-dashboard`: Link or button navigates to `/dashboard` via `url_for('dashboard')`

### Context Variables Passed
```python
{
  "location_name": str,
  "current_weather": {
    "temperature": float,
    "condition": str,
    "humidity": int,
    "wind_speed": float
  }
}
```

### Dynamic Rendering Notes
- Static values, no loops

---

## 4. Weekly Forecast Page
- **Template File:** `templates/weekly_forecast.html`
- **Route Function:** `weekly_forecast(location_id)` at `/weather/forecast/<int:location_id>`
- **Page Title:**
  - `<title>`: "Weekly Forecast - {location_name}"
  - `<h1>` (ID: `location-name`): Location name

### Element IDs and Purpose
| ID | HTML Element Type | Purpose |
| --- | --- | --- |
| `location-name` | `h1` | Location name heading |
| `forecast-list` | `table` | 7-day forecast list |
| `back-to-dashboard` | `button` | Navigate back to dashboard |

### Navigation Mappings
- `back-to-dashboard`: Navigate to `/dashboard`

### Context Variables Passed
```python
{
  "location_name": str,
  "forecast_list": List[Dict]{
    "date": str, "high_temp": float, "low_temp": float,
    "condition": str, "precipitation": int, "humidity": int
  }
}
```

### Dynamic Rendering Notes
- Loop over `forecast_list` rows

---

## 5. Air Quality Page
- **Template File:** `templates/air_quality.html`
- **Route Function:** `air_quality(location_id)` at `/air-quality/<int:location_id>`
- **Page Title:**
  - `<title>`: "Air Quality - {location_name}"

### Element IDs and Purpose
| ID | HTML Element Type | Purpose |
| --- | --- | --- |
| `air-quality-details` | `div` | Container with AQI details: AQI index, PM2.5, PM10, NO2, O3 |
| `aqi-description` | `div` | Text description of air quality |
| `back-to-dashboard` | `button` | Navigate back |

### Navigation Mapping
- `back-to-dashboard` to `/dashboard`

### Context Variables Passed
```python
{
  "location_name": str,
  "air_quality": {
    "aqi_index": int,
    "pm25": float,
    "pm10": float,
    "no2": float,
    "o3": float
  },
  "aqi_description": str
}
```

---

## 6. Alerts Page
- **Template File:** `templates/alerts.html`
- **Route Function:** `alerts(location_id)` at `/alerts/<int:location_id>`
- **Page Title:**
  - `<title>`: "Alerts - {location_name}"

### Element IDs and Purpose
| ID | HTML Element Type | Purpose |
| --- | --- | --- |
| `alerts-list` | `div` | Container listing active alerts for location |
| `acknowledge-alert-button-{alert_id}` | `button` | Button to acknowledge alert (dynamic ID) |
| `back-to-dashboard` | `button` | Navigate back to dashboard |

### Navigation Mappings
- `back-to-dashboard` to `/dashboard`

### Context Variables Passed
```python
{
  "location_name": str,
  "alerts": List[Dict]{
    "alert_id": int,
    "alert_type": str,
    "severity": str,
    "description": str,
    "start_time": str,
    "end_time": str,
    "is_acknowledged": bool
  }
}
```

### Dynamic Rendering
- Loop over alerts
- Conditional display if acknowledged

---

## 7. Locations Page
- **Template File:** `templates/locations.html`
- **Route Function:** `locations()` at `/locations`
- **Page Title:**
  - `<title>`: "Saved Locations"

### Element IDs and Purpose
| ID | HTML Element Type | Purpose |
| --- | --- | --- |
| `locations-table` | `table` | List all saved locations |
| `select-location-button-{location_id}` | `button` | Select location button (dynamic ID) |
| `remove-location-button-{location_id}` | `button` | Remove location button |
| `add-new-location-button` | `button` | Add new location button |
| `back-to-dashboard` | `button` | Back to dashboard |

### Navigation Mappings
- `back-to-dashboard` links to `/dashboard`
- `add-new-location-button` navigates to add location page or invokes modal

### Context Variables Passed
```python
{
  "saved_locations": List[Dict]{"location_id": int, "location_name": str, "latitude": float, "longitude": float, "country": str, "timezone": str}
}
```

---

## 8. Search Page
- **Template File:** `templates/search.html`
- **Route Function:** `search()` at `/search`
- **Page Title:**
  - `<title>`: "Search Locations"

### Element IDs and Purpose
| ID | HTML Element Type | Purpose |
| --- | --- | --- |
| `location-search-input` | `input` (text) | Input field for location name to search |
| `search-location-button` | `button` | Trigger search |
| `search-results` | `div` | Displays list of matching location results |

### Navigation Mappings
- Searching posts or gets query to `/search`
- Result buttons can link to select location page

### Context Variables Passed
```python
{
  "search_results": List[Dict]{"location_id": int, "location_name": str, "latitude": float, "longitude": float, "country": str, "timezone": str}
}
```

---

# Notes
- Use consistent ID names exactly as specified including case-sensitive.
- Use `url_for` for all internal link hrefs and form actions.
- Loops and conditionals in templates must be explicitly declared with Jinja2 syntax (`{% for %}`, `{% if %}`).
- Dynamic IDs are formatted by inserting the integer ID values dynamically.
- Ensure all pages present the `<title>` tag for SEO and clarity.
- The detailed data dict format above guarantees frontend unit coherence.

---

End of Frontend Specification
