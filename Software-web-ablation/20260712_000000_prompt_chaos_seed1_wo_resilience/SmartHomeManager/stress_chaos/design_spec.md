# SmartHomeManager Design Specification

---

## Section 1: Flask Routes Specification

| Endpoint URL                      | HTTP Method(s) | Function Name            | Template File           | Context Variables (name: type)                               |
|---------------------------------|----------------|--------------------------|-------------------------|--------------------------------------------------------------|
| /                               | GET            | root_redirect            | N/A (redirect)          | N/A                                                          |
| /dashboard                      | GET            | dashboard_page           | dashboard.html          | devices_summary: dict, rooms_summary: list                   |
| /devices                       | GET            | device_list_page         | devices.html            | devices: list of dict, user_rooms: list                       |
| /device/add                    | GET, POST      | add_device_page          | add_device.html         | rooms: list, device_types: list, form_errors: dict (POST error)|
| /device/<int:device_id>        | GET, POST      | device_control_page      | device_control.html     | device: dict, status: str, form_errors: dict (POST error)      |
| /automation                    | GET, POST      | automation_rules_page    | automation_rules.html   | rules: list of dict, devices: list, form_errors: dict (POST error)|
| /energy                       | GET, POST      | energy_report_page       | energy_report.html      | energy_logs: list of dict, summary: dict, filter_date: str     |
| /activity                     | GET, POST      | activity_logs_page       | activity_logs.html      | activities: list of dict, search_term: str                     |

### Route Details

- **/**
  - Redirects to `/dashboard`.

- **/dashboard** (GET)
  - Renders dashboard.html
  - Context Variables:
    - `devices_summary` (dict): Counts {total: int, active: int, offline: int}
    - `rooms_summary` (list): List of dicts with room_name (str) and device_count (int)

- **/devices** (GET)
  - Renders devices.html
  - Context Variables:
    - `devices` (list): List of device dicts including id, name, type, room, status
    - `user_rooms` (list): List of user rooms for potential filters

- **/device/add** (GET, POST)
  - GET:
    - Renders add_device.html
    - Context Variables:
      - `rooms` (list): Available rooms
      - `device_types` (list): Device types
      - `form_errors` (dict): Empty or errors after POST
  - POST:
    - Processes form submission to add device
    - On validation error, re-render with form_errors
    - On success redirect to /devices

- **/device/<int:device_id>** (GET, POST)
  - GET:
    - Renders device_control.html
    - Context Variables:
      - `device` (dict): Device details
      - `status` (str): Device status
      - `form_errors` (dict): Empty or errors after POST
  - POST:
    - Handles control changes
    - On validation error, re-render
    - On success reload page or redirect

- **/automation** (GET, POST)
  - GET:
    - Renders automation_rules.html
    - Context Variables:
      - `rules` (list): Automation rules for user
      - `devices` (list): User devices
      - `form_errors` (dict): Empty or errors after POST
  - POST:
    - Add new rule or update existing
    - On error re-render
    - On success redirect

- **/energy** (GET, POST)
  - GET:
    - Renders energy_report.html
    - Context Variables:
      - `energy_logs` (list): Device energy data
      - `summary` (dict): Total kWh and cost estimate
      - `filter_date` (str): Date filter value
  - POST:
    - Apply date filter

- **/activity** (GET, POST)
  - GET:
    - Renders activity_logs.html
    - Context Variables:
      - `activities` (list): Activity log entries
      - `search_term` (str): Current search string
  - POST:
    - Apply search query filter

---

## Section 2: HTML Templates Specification

### 1. Dashboard Page
- Filepath: templates/dashboard.html
- Page Title: Smart Home Dashboard
- Element IDs:
  - `dashboard-page`: Div container for dashboard page
  - `device-summary`: Div showing total devices, active devices, offline devices count
  - `device-list-button`: Button to go to Device List page
  - `add-device-button`: Button to go to Add Device page
  - `automation-button`: Button to go to Automation Rules page
  - `energy-button`: Button to go to Energy Report page
  - `activity-button`: Button to go to Activity Logs page
  - `room-list`: Div listing rooms with device counts
- Navigation mappings:
  - `device-list-button`: url_for('device_list_page')
  - `add-device-button`: url_for('add_device_page')
  - `automation-button`: url_for('automation_rules_page')
  - `energy-button`: url_for('energy_report_page')
  - `activity-button`: url_for('activity_logs_page')

### 2. Device List Page
- Filepath: templates/devices.html
- Page Title: My Devices
- Element IDs:
  - `device-list-page`: Div container
  - `device-table`: Table listing devices with columns: name, type, room, status, actions
  - `control-device-button-{device_id}`: Button for each device row to control device. Pattern: control-device-button-{device_id} where device_id is int
  - `back-to-dashboard`: Button to return to dashboard
- Navigation mappings:
  - `control-device-button-{device_id}`: url_for('device_control_page', device_id=device_id)
  - `back-to-dashboard`: url_for('dashboard_page')

### 3. Add Device Page
- Filepath: templates/add_device.html
- Page Title: Add New Device
- Element IDs:
  - `add-device-page`: Div container
  - `device-name`: Input text for device name
  - `device-type`: Dropdown with options: Light, Thermostat, Camera, Lock, Sensor, Appliance
  - `device-room`: Dropdown with room options: Living Room, Bedroom, Kitchen, Bathroom, Garage
  - `submit-device-button`: Button to submit new device
  - `back-to-dashboard`: Button to return to dashboard
- Navigation mappings:
  - `back-to-dashboard`: url_for('dashboard_page')

### 4. Device Control Page
- Filepath: templates/device_control.html
- Page Title: Device Control
- Element IDs:
  - `device-control-page`: Div container
  - `device-name-display`: H2 element that displays device name
  - `device-status-display`: Div showing status (Online/Offline)
  - `power-toggle`: Button to toggle power on/off
  - `save-settings-button`: Button to save settings
  - `back-to-devices`: Button to go back to Device List
- Navigation mappings:
  - `back-to-devices`: url_for('device_list_page')

### 5. Automation Rules Page
- Filepath: templates/automation_rules.html
- Page Title: Automation Rules
- Element IDs:
  - `automation-page`: Div container
  - `rules-table`: Table showing name, trigger, action, status
  - `rule-name`: Input for rule name
  - `trigger-type`: Dropdown with values: Time, Motion, Temperature
  - `trigger-value`: Input for trigger value
  - `action-device`: Dropdown for selecting target device
  - `action-type`: Dropdown with values: Turn On, Turn Off, Set Brightness, Set Temperature
  - `add-rule-button`: Button to add rule
  - `back-to-dashboard`: Button to return to dashboard
- Navigation mappings:
  - `back-to-dashboard`: url_for('dashboard_page')

### 6. Energy Report Page
- Filepath: templates/energy_report.html
- Page Title: Energy Report
- Element IDs:
  - `energy-page`: Div container
  - `energy-summary`: Div showing total consumption and estimated cost
  - `energy-table`: Table listing device energy usage by date and kWh
  - `date-filter`: Input date field for filtering
  - `apply-filter-button`: Button to filter by date
  - `back-to-dashboard`: Button to go to dashboard
- Navigation mappings:
  - `back-to-dashboard`: url_for('dashboard_page')

### 7. Activity Logs Page
- Filepath: templates/activity_logs.html
- Page Title: Activity Logs
- Element IDs:
  - `activity-page`: Div container
  - `activity-table`: Table showing timestamp, device, action, details
  - `search-activity`: Input for search query
  - `apply-search-button`: Button to apply search
  - `back-to-dashboard`: Button to return to dashboard
- Navigation mappings:
  - `back-to-dashboard`: url_for('dashboard_page')

---

## Section 3: Data File Schemas

### 1. users.txt
- Path: data/users.txt
- Fields (pipe-delimited):
  1. username (str) - unique user identifier
  2. email (str) - user email address
- Examples:
  ```
  john_doe|john@example.com
  jane_smith|jane@example.com
  ```

### 2. devices.txt
- Path: data/devices.txt
- Fields (pipe-delimited):
  1. username (str)
  2. device_id (int)
  3. device_name (str)
  4. device_type (str; e.g. Light, Thermostat)
  5. room (str)
  6. brand (str)
  7. model (str)
  8. status (str; Online or Offline)
  9. power (str; "on" or "off")
 10. brightness (int or empty) - e.g. 0-100
 11. temperature (int or empty) - e.g. degrees in Fahrenheit
 12. mode (str or empty) - e.g. Auto, Manual
 13. schedule_time (str or empty) - e.g. "22:00"
- Examples:
  ```
  john_doe|1|Living Room Light|Light|Living Room|Philips|Hue|Online|on|75|||Auto|
  john_doe|2|Bedroom Thermostat|Thermostat|Bedroom|Nest|Learning|Online|on||72|Auto|22:00
  jane_smith|3|Kitchen Camera|Camera|Kitchen|Ring|Indoor|Online|on||||Manual|
  ```

### 3. rooms.txt
- Path: data/rooms.txt
- Fields (pipe-delimited):
  1. username (str)
  2. room_id (int)
  3. room_name (str)
- Examples:
  ```
  john_doe|1|Living Room
  john_doe|2|Bedroom
  john_doe|3|Kitchen
  jane_smith|1|Living Room
  ```

### 4. automation_rules.txt
- Path: data/automation_rules.txt
- Fields (pipe-delimited):
  1. username (str)
  2. rule_id (int)
  3. rule_name (str)
  4. trigger_type (str; Time, Motion, Temperature)
  5. trigger_value (str; e.g. "07:00", "detected", "75")
  6. action_device_id (int)
  7. action_type (str; Turn On, Turn Off, Set Brightness, Set Temperature)
  8. action_value (str or empty)
  9. enabled (bool as string; "true" or "false")
- Examples:
  ```
  john_doe|1|Morning Lights|Time|07:00|1|Turn On||true
  john_doe|2|Night Mode|Time|22:00|1|Set Brightness|20|true
  jane_smith|1|Motion Alert|Motion|detected|3|Turn On||true
  ```

### 5. energy_logs.txt
- Path: data/energy_logs.txt
- Fields (pipe-delimited):
  1. username (str)
  2. device_id (int)
  3. date (str; YYYY-MM-DD)
  4. consumption_kwh (float)
- Examples:
  ```
  john_doe|1|2024-11-01|0.5
  john_doe|2|2024-11-01|2.3
  john_doe|1|2024-11-02|0.6
  jane_smith|3|2024-11-01|0.2
  ```

### 6. activity_logs.txt
- Path: data/activity_logs.txt
- Fields (pipe-delimited):
  1. username (str)
  2. timestamp (str; YYYY-MM-DD HH:MM:SS)
  3. device_id (int)
  4. action (str)
  5. details (str)
- Examples:
  ```
  john_doe|2024-11-01 07:00:00|1|Power On|Automation triggered: Morning Lights
  john_doe|2024-11-01 08:30:00|2|Settings Changed|Temperature set to 72
  jane_smith|2024-11-01 09:15:00|3|Power On|Manual control
  ```

---

This design specification enables backend developers to implement the Flask routes and data handling independently, while frontend developers can use the template details and element IDs to build UI components. All elements, routes, and data schemas are consistent and complete as per requirements.
