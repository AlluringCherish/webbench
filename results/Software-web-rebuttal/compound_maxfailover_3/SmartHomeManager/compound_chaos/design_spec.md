# SmartHomeManager Design Specification

---

## Section 1: Flask Routes Specification

| Endpoint URL                     | HTTP Methods | Function Name            | Template Rendered        | Context Variables Passed                                                                                              |
|---------------------------------|--------------|--------------------------|--------------------------|----------------------------------------------------------------------------------------------------------------------|
| `/`                             | GET          | root_redirect             | None (redirect to `/dashboard`) | None                                                                                                                 |
| `/dashboard`                    | GET          | dashboard_page            | dashboard.html           | user_devices: list of dict (each device info), rooms_summary: dict (room_name -> device counts), device_counts: dict ({total:int, active:int, offline:int}) |
| `/devices`                     | GET          | device_list_page          | device_list.html         | devices: list of dict (all user's devices with id, name, type, room, status)                                         |
| `/device/add`                  | GET          | add_device_page           | add_device.html          | device_types: list of str (Light, Thermostat, Camera, Lock, Sensor, Appliance), rooms: list of str                    |
| `/device/add`                  | POST         | add_device_submit         | None (redirect usually)   | form data handled (device_name:str, device_type:str, device_room:str)                                                |
| `/device/<int:device_id>`      | GET          | device_control_page       | device_control.html      | device: dict (all device details including controls and status)                                                      |
| `/device/<int:device_id>/control` | POST      | device_control_submit     | None (redirect usually)   | form data with settings to update device                                                                             |
| `/automation`                  | GET          | automation_rules_page     | automation.html          | automation_rules: list of dict (rule details), devices: list of dict (id and name for action_device dropdown)       |
| `/automation`                  | POST         | add_automation_rule       | None (redirect usually)   | form data with new automation rule parameters                                                                        |
| `/energy`                     | GET          | energy_report_page        | energy_report.html       | energy_summary: dict (total_consumption: float, cost_estimate: float), energy_logs: list of dict (per device per date) |
| `/energy/filter`              | POST         | energy_filter             | None (redirect usually)   | filter_date: str (date in yyyy-mm-dd)                                                                                 |
| `/activity`                   | GET          | activity_logs_page        | activity_logs.html       | activity_logs: list of dict (timestamp, device, action, details), search_query: str (optional)                        |
| `/activity/search`            | POST         | activity_search           | None (redirect usually)   | search_query: str from form                                                                                           |

---

## Section 2: HTML Templates Specification

### 1. Dashboard Page
- Template Path: `templates/dashboard.html`
- Page Title: "Smart Home Dashboard"
- `<title>` and `<h1>`: "Smart Home Dashboard"
- Elements:
  - ID: `dashboard-page` - Div - Container for the dashboard
  - ID: `device-summary` - Div - Shows total devices, active devices, offline devices
  - ID: `device-list-button` - Button - Navigate to Device List page
  - ID: `add-device-button` - Button - Navigate to Add Device page
  - ID: `automation-button` - Button - Navigate to Automation Rules page
  - ID: `energy-button` - Button - Navigate to Energy Report page
  - ID: `activity-button` - Button - Navigate to Activity Logs page
  - ID: `room-list` - Div - List of all rooms with device counts
- Navigation mappings:
  - `device-list-button` -> `url_for('device_list_page')`
  - `add-device-button` -> `url_for('add_device_page')`
  - `automation-button` -> `url_for('automation_rules_page')`
  - `energy-button` -> `url_for('energy_report_page')`
  - `activity-button` -> `url_for('activity_logs_page')`

### 2. Device List Page
- Template Path: `templates/device_list.html`
- Page Title: "My Devices"
- `<title>` and `<h1>`: "My Devices"
- Elements:
  - ID: `device-list-page` - Div - Container for device list
  - ID: `device-table` - Table - Displays all devices (name, type, room, status, actions)
  - ID pattern: `control-device-button-{device_id}` - Button - Controls for each device to navigate to Device Control page
  - ID: `back-to-dashboard` - Button - Navigate back to Dashboard
- Navigation mappings:
  - `back-to-dashboard` -> `url_for('dashboard_page')`
  - `control-device-button-{device_id}` -> `url_for('device_control_page', device_id=device_id)`

### 3. Add Device Page
- Template Path: `templates/add_device.html`
- Page Title: "Add New Device"
- `<title>` and `<h1>`: "Add New Device"
- Elements:
  - ID: `add-device-page` - Div - Container for add device form
  - ID: `device-name` - Input - Text input for device name
  - ID: `device-type` - Dropdown - Select device type (Light, Thermostat, Camera, Lock, Sensor, Appliance)
  - ID: `device-room` - Dropdown - Select room (Living Room, Bedroom, Kitchen, Bathroom, Garage)
  - ID: `submit-device-button` - Button - Submit new device
  - ID: `back-to-dashboard` - Button - Navigate back to Dashboard
- Navigation mappings:
  - `back-to-dashboard` -> `url_for('dashboard_page')`

### 4. Device Control Page
- Template Path: `templates/device_control.html`
- Page Title: "Device Control"
- `<title>` and `<h1>`: "Device Control"
- Elements:
  - ID: `device-control-page` - Div - Container for device control
  - ID: `device-name-display` - H2 - Shows device name
  - ID: `device-status-display` - Div - Shows device status (Online/Offline)
  - ID: `power-toggle` - Button - Toggle device power on/off
  - ID: `save-settings-button` - Button - Save device settings
  - ID: `back-to-devices` - Button - Navigate back to Device List
- Navigation mappings:
  - `back-to-devices` -> `url_for('device_list_page')`

### 5. Automation Rules Page
- Template Path: `templates/automation.html`
- Page Title: "Automation Rules"
- `<title>` and `<h1>`: "Automation Rules"
- Elements:
  - ID: `automation-page` - Div - Container for automation rules
  - ID: `rules-table` - Table - Lists automation rules (name, trigger, action, status)
  - ID: `rule-name` - Input - Input new rule name
  - ID: `trigger-type` - Dropdown - Select trigger type (Time, Motion, Temperature)
  - ID: `trigger-value` - Input - Input trigger value
  - ID: `action-device` - Dropdown - Select target device
  - ID: `action-type` - Dropdown - Select action type (Turn On, Turn Off, Set Brightness, Set Temperature)
  - ID: `add-rule-button` - Button - Add new automation rule
  - ID: `back-to-dashboard` - Button - Navigate back to Dashboard
- Navigation mappings:
  - `back-to-dashboard` -> `url_for('dashboard_page')`

### 6. Energy Report Page
- Template Path: `templates/energy_report.html`
- Page Title: "Energy Report"
- `<title>` and `<h1>`: "Energy Report"
- Elements:
  - ID: `energy-page` - Div - Container for energy report
  - ID: `energy-summary` - Div - Shows total consumption and cost estimate
  - ID: `energy-table` - Table - Shows energy per device and date
  - ID: `date-filter` - Input (date) - Filter energy data by date
  - ID: `apply-filter-button` - Button - Apply date filter
  - ID: `back-to-dashboard` - Button - Navigate back to Dashboard
- Navigation mappings:
  - `back-to-dashboard` -> `url_for('dashboard_page')`

### 7. Activity Logs Page
- Template Path: `templates/activity_logs.html`
- Page Title: "Activity Logs"
- `<title>` and `<h1>`: "Activity Logs"
- Elements:
  - ID: `activity-page` - Div - Container for activity logs
  - ID: `activity-table` - Table - Lists activity logs (timestamp, device, action, details)
  - ID: `search-activity` - Input - Search field for logs
  - ID: `apply-search-button` - Button - Apply search
  - ID: `back-to-dashboard` - Button - Navigate back to Dashboard
- Navigation mappings:
  - `back-to-dashboard` -> `url_for('dashboard_page')`

---

## Section 3: Data File Schemas

### 1. User Data
- Filename & Path: `data/users.txt`
- Format (pipe-delimited, no header):
  ```
  username|email
  ```
- Fields:
  - username: str
  - email: str
- Examples:
  ```
  john_doe|john@example.com
  jane_smith|jane@example.com
  ```

### 2. Device Data
- Filename & Path: `data/devices.txt`
- Format (pipe-delimited, no header):
  ```
  username|device_id|device_name|device_type|room|brand|model|status|power|brightness|temperature|mode|schedule_time
  ```
- Fields:
  - username: str
  - device_id: int
  - device_name: str
  - device_type: str (Light, Thermostat, Camera, etc.)
  - room: str
  - brand: str
  - model: str
  - status: str (Online/Offline)
  - power: str (on/off)
  - brightness: str or empty (numeric value as string if applicable)
  - temperature: str or empty (numeric value as string if applicable)
  - mode: str (Auto, Manual, or empty)
  - schedule_time: str (time formatted e.g. "22:00" or empty)
- Examples:
  ```
  john_doe|1|Living Room Light|Light|Living Room|Philips|Hue|Online|on|75|||Auto|
  john_doe|2|Bedroom Thermostat|Thermostat|Bedroom|Nest|Learning|Online|on||72|Auto|22:00
  jane_smith|3|Kitchen Camera|Camera|Kitchen|Ring|Indoor|Online|on||||Manual|
  ```

### 3. Room Data
- Filename & Path: `data/rooms.txt`
- Format (pipe-delimited, no header):
  ```
  username|room_id|room_name
  ```
- Fields:
  - username: str
  - room_id: int
  - room_name: str
- Examples:
  ```
  john_doe|1|Living Room
  john_doe|2|Bedroom
  john_doe|3|Kitchen
  jane_smith|1|Living Room
  ```

### 4. Automation Rules Data
- Filename & Path: `data/automation_rules.txt`
- Format (pipe-delimited, no header):
  ```
  username|rule_id|rule_name|trigger_type|trigger_value|action_device_id|action_type|action_value|enabled
  ```
- Fields:
  - username: str
  - rule_id: int
  - rule_name: str
  - trigger_type: str (Time, Motion, Temperature)
  - trigger_value: str (e.g., "07:00", "detected", "22")
  - action_device_id: int
  - action_type: str (Turn On, Turn Off, Set Brightness, Set Temperature)
  - action_value: str (optional value depending on action, can be empty)
  - enabled: bool (true or false strings)
- Examples:
  ```
  john_doe|1|Morning Lights|Time|07:00|1|Turn On||true
  john_doe|2|Night Mode|Time|22:00|1|Set Brightness|20|true
  jane_smith|1|Motion Alert|Motion|detected|3|Turn On||true
  ```

### 5. Energy Consumption Logs
- Filename & Path: `data/energy_logs.txt`
- Format (pipe-delimited, no header):
  ```
  username|device_id|date|consumption_kwh
  ```
- Fields:
  - username: str
  - device_id: int
  - date: str (YYYY-MM-DD)
  - consumption_kwh: float
- Examples:
  ```
  john_doe|1|2024-11-01|0.5
  john_doe|2|2024-11-01|2.3
  john_doe|1|2024-11-02|0.6
  jane_smith|3|2024-11-01|0.2
  ```

### 6. Activity Logs
- Filename & Path: `data/activity_logs.txt`
- Format (pipe-delimited, no header):
  ```
  username|timestamp|device_id|action|details
  ```
- Fields:
  - username: str
  - timestamp: str (YYYY-MM-DD HH:MM:SS)
  - device_id: int
  - action: str
  - details: str
- Examples:
  ```
  john_doe|2024-11-01 07:00:00|1|Power On|Automation triggered: Morning Lights
  john_doe|2024-11-01 08:30:00|2|Settings Changed|Temperature set to 72
  jane_smith|2024-11-01 09:15:00|3|Power On|Manual control
  ```

---

# End of specification
