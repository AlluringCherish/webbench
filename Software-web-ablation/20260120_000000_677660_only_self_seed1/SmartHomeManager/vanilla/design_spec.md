# SmartHomeManager Design Specification

---

## Section 1: Flask Routes Specification

| Endpoint URL                | HTTP Methods | Function Name           | Template Rendered       | Context Variables (Name: Type)                          |
|-----------------------------|--------------|------------------------|-------------------------|--------------------------------------------------------|
| `/`                         | GET          | root_redirect           | -                       | -                                                      |
| `/dashboard`                | GET          | dashboard               | dashboard.html          | devices: list, rooms: list, device_summary: dict       |
| `/devices`                 | GET          | device_list             | devices.html            | devices: list                                           |
| `/devices/add`             | GET, POST    | add_device              | add_device.html         | rooms: list, device_types: list, form_errors: dict (POST) |
| `/device/<int:device_id>`  | GET, POST    | control_device          | device_control.html     | device: dict, status: str                               |
| `/automation`              | GET, POST    | automation_rules        | automation.html         | rules: list, devices: list, form_errors: dict (POST)   |
| `/energy`                 | GET, POST    | energy_report           | energy.html             | energy_logs: list, energy_summary: dict, filter_date: str (POST) |
| `/activity`               | GET, POST    | activity_logs           | activity.html           | activities: list, search_query: str (POST)              |


### Route Details
- **Root route `/`**: Redirects to `/dashboard`.
- **Dashboard `/dashboard` (GET):** Shows overview of all devices and rooms.
- **Device List `/devices` (GET):** Displays all devices.
- **Add Device `/devices/add` (GET, POST):** 
  - GET renders the add device form.
  - POST submits new device data.
- **Device Control `/device/<int:device_id>` (GET, POST):** 
  - GET displays device control page.
  - POST saves device settings.
- **Automation Rules `/automation` (GET, POST):**
  - GET displays existing rules.
  - POST adds new rule.
- **Energy Report `/energy` (GET, POST):**
  - GET displays energy data.
  - POST applies date filter.
- **Activity Logs `/activity` (GET, POST):**
  - GET shows logs.
  - POST applies search filter.


## Section 2: HTML Templates Specification

### 1. Dashboard Page
- Filepath: `templates/dashboard.html`
- Page Title: Smart Home Dashboard
- Element IDs:
  - `dashboard-page` (Div): Container for dashboard page.
  - `device-summary` (Div): Shows total devices, active and offline counts.
  - `device-list-button` (Button): Navigates to device list.
  - `add-device-button` (Button): Navigates to add device page.
  - `automation-button` (Button): Navigates to automation rules.
  - `energy-button` (Button): Navigates to energy report.
  - `activity-button` (Button): Navigates to activity logs.
  - `room-list` (Div): Lists all rooms with device counts.
- Navigation Mappings:
  - `device-list-button`: `url_for('device_list')`
  - `add-device-button`: `url_for('add_device')`
  - `automation-button`: `url_for('automation_rules')`
  - `energy-button`: `url_for('energy_report')`
  - `activity-button`: `url_for('activity_logs')`


### 2. Device List Page
- Filepath: `templates/devices.html`
- Page Title: My Devices
- Element IDs:
  - `device-list-page` (Div): Container.
  - `device-table` (Table): Displays devices.
  - `control-device-button-{device_id}` (Button): Controls device with ID pattern.
  - `back-to-dashboard` (Button): Button to dashboard.
- Navigation Mappings:
  - `back-to-dashboard`: `url_for('dashboard')`
  - `control-device-button-{device_id}`: `url_for('control_device', device_id=device_id)`


### 3. Add Device Page
- Filepath: `templates/add_device.html`
- Page Title: Add New Device
- Element IDs:
  - `add-device-page` (Div): Container.
  - `device-name` (Input): Enter device name.
  - `device-type` (Dropdown): Select device type.
  - `device-room` (Dropdown): Select room.
  - `submit-device-button` (Button): Submit device.
  - `back-to-dashboard` (Button): Navigate back.
- Navigation Mappings:
  - `back-to-dashboard`: `url_for('dashboard')`


### 4. Device Control Page
- Filepath: `templates/device_control.html`
- Page Title: Device Control
- Element IDs:
  - `device-control-page` (Div): Container.
  - `device-name-display` (H2): Shows device name.
  - `device-status-display` (Div): Shows status.
  - `power-toggle` (Button): Toggle power.
  - `save-settings-button` (Button): Save settings.
  - `back-to-devices` (Button): Back to device list.
- Navigation Mappings:
  - `back-to-devices`: `url_for('device_list')`


### 5. Automation Rules Page
- Filepath: `templates/automation.html`
- Page Title: Automation Rules
- Element IDs:
  - `automation-page` (Div): Container.
  - `rules-table` (Table): Shows rules.
  - `rule-name` (Input): Input rule name.
  - `trigger-type` (Dropdown): Select trigger.
  - `trigger-value` (Input): Input trigger value.
  - `action-device` (Dropdown): Select target device.
  - `action-type` (Dropdown): Select action type.
  - `add-rule-button` (Button): Add rule.
  - `back-to-dashboard` (Button): Back to dashboard.
- Navigation Mappings:
  - `back-to-dashboard`: `url_for('dashboard')`


### 6. Energy Report Page
- Filepath: `templates/energy.html`
- Page Title: Energy Report
- Element IDs:
  - `energy-page` (Div): Container.
  - `energy-summary` (Div): Shows total consumption and cost.
  - `energy-table` (Table): Lists energy usage per device.
  - `date-filter` (Input date): Filter date.
  - `apply-filter-button` (Button): Apply filter.
  - `back-to-dashboard` (Button): Back to dashboard.
- Navigation Mappings:
  - `back-to-dashboard`: `url_for('dashboard')`


### 7. Activity Logs Page
- Filepath: `templates/activity.html`
- Page Title: Activity Logs
- Element IDs:
  - `activity-page` (Div): Container.
  - `activity-table` (Table): Lists activities.
  - `search-activity` (Input): Search logs.
  - `apply-search-button` (Button): Apply search.
  - `back-to-dashboard` (Button): Back to dashboard.
- Navigation Mappings:
  - `back-to-dashboard`: `url_for('dashboard')`


## Section 3: Data File Schemas

### 1. users.txt
- Path: `data/users.txt`
- Pipe-delimited Fields:
  1. username (str): User's unique username
  2. email (str): User's email address
- Examples:
  ```
  john_doe|john@example.com
  jane_smith|jane@example.com
  ```


### 2. devices.txt
- Path: `data/devices.txt`
- Pipe-delimited Fields:
  1. username (str): Owner username
  2. device_id (int): Unique device numeric ID
  3. device_name (str): Name of device
  4. device_type (str): Type (Light, Thermostat, Camera, Lock, Sensor, Appliance)
  5. room (str): Assigned room
  6. brand (str): Device brand
  7. model (str): Device model
  8. status (str): Online or Offline
  9. power (str): 'on' or 'off'
  10. brightness (int or empty): Brightness setting (0-100) or empty
  11. temperature (int or empty): Temperature setting or empty
  12. mode (str or empty): Mode like Auto or Manual or empty
  13. schedule_time (str or empty): Scheduled time (HH:MM) or empty
- Examples:
  ```
  john_doe|1|Living Room Light|Light|Living Room|Philips|Hue|Online|on|75|||Auto|
  john_doe|2|Bedroom Thermostat|Thermostat|Bedroom|Nest|Learning|Online|on||72|Auto|22:00
  jane_smith|3|Kitchen Camera|Camera|Kitchen|Ring|Indoor|Online|on||||Manual|
  ```


### 3. rooms.txt
- Path: `data/rooms.txt`
- Pipe-delimited Fields:
  1. username (str): User owner
  2. room_id (int): Unique room ID
  3. room_name (str): Room name
- Examples:
  ```
  john_doe|1|Living Room
  john_doe|2|Bedroom
  john_doe|3|Kitchen
  jane_smith|1|Living Room
  ```


### 4. automation_rules.txt
- Path: `data/automation_rules.txt`
- Pipe-delimited Fields:
  1. username (str): Rule owner
  2. rule_id (int): Unique rule ID
  3. rule_name (str): Name of automation rule
  4. trigger_type (str): Trigger type (Time, Motion, Temperature)
  5. trigger_value (str): Value for trigger (e.g., time or detected)
  6. action_device_id (int): Device ID to act upon
  7. action_type (str): Action (Turn On, Turn Off, Set Brightness, Set Temperature)
  8. action_value (str or empty): Action parameter, e.g. brightness level
  9. enabled (bool): Rule enabled status ('true' or 'false')
- Examples:
  ```
  john_doe|1|Morning Lights|Time|07:00|1|Turn On||true
  john_doe|2|Night Mode|Time|22:00|1|Set Brightness|20|true
  jane_smith|1|Motion Alert|Motion|detected|3|Turn On||true
  ```


### 5. energy_logs.txt
- Path: `data/energy_logs.txt`
- Pipe-delimited Fields:
  1. username (str): User owner
  2. device_id (int): Device ID
  3. date (str): Date in YYYY-MM-DD
  4. consumption_kwh (float): Energy consumption in kWh
- Examples:
  ```
  john_doe|1|2024-11-01|0.5
  john_doe|2|2024-11-01|2.3
  john_doe|1|2024-11-02|0.6
  jane_smith|3|2024-11-01|0.2
  ```


### 6. activity_logs.txt
- Path: `data/activity_logs.txt`
- Pipe-delimited Fields:
  1. username (str): User owner
  2. timestamp (str): DateTime in YYYY-MM-DD HH:MM:SS
  3. device_id (int): Device ID
  4. action (str): Action performed
  5. details (str): Additional detail about action
- Examples:
  ```
  john_doe|2024-11-01 07:00:00|1|Power On|Automation triggered: Morning Lights
  john_doe|2024-11-01 08:30:00|2|Settings Changed|Temperature set to 72
  jane_smith|2024-11-01 09:15:00|3|Power On|Manual control
  ```


---

**End of SmartHomeManager Design Specification**
