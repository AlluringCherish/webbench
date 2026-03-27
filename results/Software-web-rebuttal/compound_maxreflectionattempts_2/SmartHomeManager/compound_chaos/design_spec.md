# Design Specification for SmartHomeManager Web Application

---

## Section 1: Flask Routes Specification

| Endpoint URL             | HTTP Methods | Function Name          | Template Rendered         | Context Variables (name: type)                                                |
|--------------------------|--------------|------------------------|---------------------------|------------------------------------------------------------------------------|
| /                        | GET          | root_redirect          | N/A (redirect to /dashboard) | None                                                                         |
| /dashboard               | GET          | dashboard_page         | dashboard.html             | devices: list[dict], rooms: list[dict], device_summary: dict                  |
| /devices                 | GET          | device_list_page       | device_list.html           | devices: list[dict], rooms: dict                                             |
| /devices/add             | GET, POST    | add_device_page        | add_device.html            | device_types: list[str], rooms: list[str], form_errors: dict (on POST errors) |
| /devices/<int:device_id> | GET, POST    | device_control_page    | device_control.html        | device: dict, form_errors: dict (on POST errors)                             |
| /automation              | GET, POST    | automation_rules_page  | automation_rules.html      | automation_rules: list[dict], devices: list[dict], form_errors: dict (on POST)|
| /energy                  | GET, POST    | energy_report_page     | energy_report.html         | energy_logs: list[dict], energy_summary: dict, date_filter: str (on POST)    |
| /activity                | GET, POST    | activity_logs_page     | activity_logs.html         | activity_logs: list[dict], search_term: str (on POST)                        |

---

## Section 2: HTML Templates Specification

### templates/dashboard.html
- Page Title: Smart Home Dashboard
- Header `<title>`: Smart Home Dashboard
- Header `<h1>`: Smart Home Dashboard
- Element IDs:
  - dashboard-page: Div - Container for the dashboard page.
  - device-summary: Div - Shows total devices, active devices, and offline devices count.
  - device-list-button: Button - Navigates to the device list page.
  - add-device-button: Button - Navigates to add device page.
  - automation-button: Button - Navigates to automation rules page.
  - energy-button: Button - Navigates to energy report page.
  - activity-button: Button - Navigates to activity logs page.
  - room-list: Div - Lists all rooms with device counts.
- Navigation mappings:
  - device-list-button: url_for('device_list_page')
  - add-device-button: url_for('add_device_page')
  - automation-button: url_for('automation_rules_page')
  - energy-button: url_for('energy_report_page')
  - activity-button: url_for('activity_logs_page')

---

### templates/device_list.html
- Page Title: My Devices
- Header `<title>`: My Devices
- Header `<h1>`: My Devices
- Element IDs:
  - device-list-page: Div - Container for device list page.
  - device-table: Table - Displays device details with columns: name, type, room, status, actions.
  - back-to-dashboard: Button - Navigates back to dashboard.
  - control-device-button-{device_id}: Button - Navigates to control page for device with device_id.
    - Example: control-device-button-3 for device_id=3.
- Navigation mappings:
  - back-to-dashboard: url_for('dashboard_page')
  - control-device-button-{device_id}: url_for('device_control_page', device_id=device_id)

---

### templates/add_device.html
- Page Title: Add New Device
- Header `<title>`: Add New Device
- Header `<h1>`: Add New Device
- Element IDs:
  - add-device-page: Div - Container for add device page.
  - device-name: Input - Input for new device name.
  - device-type: Dropdown - Select device type (Light, Thermostat, Camera, Lock, Sensor, Appliance).
  - device-room: Dropdown - Select room (Living Room, Bedroom, Kitchen, Bathroom, Garage).
  - submit-device-button: Button - Submit the new device.
  - back-to-dashboard: Button - Navigate back to dashboard.
- Navigation mappings:
  - back-to-dashboard: url_for('dashboard_page')

---

### templates/device_control.html
- Page Title: Device Control
- Header `<title>`: Device Control
- Header `<h1>`: Device Control
- Element IDs:
  - device-control-page: Div - Container for device control page.
  - device-name-display: H2 - Displays the device name.
  - device-status-display: Div - Shows current status (Online/Offline).
  - power-toggle: Button - Toggle power on/off.
  - save-settings-button: Button - Save settings for the device.
  - back-to-devices: Button - Navigate back to device list.
- Navigation mappings:
  - back-to-devices: url_for('device_list_page')

---

### templates/automation_rules.html
- Page Title: Automation Rules
- Header `<title>`: Automation Rules
- Header `<h1>`: Automation Rules
- Element IDs:
  - automation-page: Div - Container for automation rules page.
  - rules-table: Table - Displays automation rules with columns: name, trigger, action, status.
  - rule-name: Input - Input for new rule name.
  - trigger-type: Dropdown - Trigger type (Time, Motion, Temperature).
  - trigger-value: Input - Trigger value (time or threshold).
  - action-device: Dropdown - Select target device.
  - action-type: Dropdown - Action type (Turn On, Turn Off, Set Brightness, Set Temperature).
  - add-rule-button: Button - Add new automation rule.
  - back-to-dashboard: Button - Navigate back to dashboard.
- Navigation mappings:
  - back-to-dashboard: url_for('dashboard_page')

---

### templates/energy_report.html
- Page Title: Energy Report
- Header `<title>`: Energy Report
- Header `<h1>`: Energy Report
- Element IDs:
  - energy-page: Div - Container for energy report page.
  - energy-summary: Div - Shows total energy consumption and cost estimate.
  - energy-table: Table - Displays energy consumption per device with date and kWh.
  - date-filter: Input (date) - Filter energy data by date.
  - apply-filter-button: Button - Apply date filter.
  - back-to-dashboard: Button - Navigate back to dashboard.
- Navigation mappings:
  - back-to-dashboard: url_for('dashboard_page')

---

### templates/activity_logs.html
- Page Title: Activity Logs
- Header `<title>`: Activity Logs
- Header `<h1>`: Activity Logs
- Element IDs:
  - activity-page: Div - Container for activity logs page.
  - activity-table: Table - Displays activity logs with timestamp, device, action, details.
  - search-activity: Input - Search activity logs.
  - apply-search-button: Button - Apply search filter.
  - back-to-dashboard: Button - Navigate back to dashboard.
- Navigation mappings:
  - back-to-dashboard: url_for('dashboard_page')

---

## Section 3: Data File Schemas

### 1. users.txt
- Path: data/users.txt
- Fields (pipe-delimited):
  1. username (str): User's unique username
  2. email (str): User's email address
- Examples:
  ```
  john_doe|john@example.com
  jane_smith|jane@example.com
  ```

---

### 2. devices.txt
- Path: data/devices.txt
- Fields (pipe-delimited):
  1. username (str): Owner username
  2. device_id (int): Unique device identifier
  3. device_name (str): Name of the device
  4. device_type (str): Type (Light, Thermostat, Camera, Lock, Sensor, Appliance)
  5. room (str): Room name where device is located
  6. brand (str): Device brand
  7. model (str): Device model
  8. status (str): Online or Offline
  9. power (str): Power state (on/off)
  10. brightness (str): Brightness level or empty
  11. temperature (str): Temperature setting or empty
  12. mode (str): Mode (Auto, Manual, etc.) or empty
  13. schedule_time (str): Scheduled time or empty
- Examples:
  ```
  john_doe|1|Living Room Light|Light|Living Room|Philips|Hue|Online|on|75|||Auto|
  john_doe|2|Bedroom Thermostat|Thermostat|Bedroom|Nest|Learning|Online|on||72|Auto|22:00
  jane_smith|3|Kitchen Camera|Camera|Kitchen|Ring|Indoor|Online|on||||Manual|
  ```

---

### 3. rooms.txt
- Path: data/rooms.txt
- Fields (pipe-delimited):
  1. username (str): Owner username
  2. room_id (int): Unique room identifier
  3. room_name (str): Name of the room
- Examples:
  ```
  john_doe|1|Living Room
  john_doe|2|Bedroom
  john_doe|3|Kitchen
  jane_smith|1|Living Room
  ```

---

### 4. automation_rules.txt
- Path: data/automation_rules.txt
- Fields (pipe-delimited):
  1. username (str): Owner username
  2. rule_id (int): Unique rule identifier
  3. rule_name (str): Name of the automation rule
  4. trigger_type (str): Type of trigger (Time, Motion, Temperature)
  5. trigger_value (str): Trigger value (e.g. time or threshold)
  6. action_device_id (int): Device ID the action applies to
  7. action_type (str): Action type (Turn On, Turn Off, Set Brightness, Set Temperature)
  8. action_value (str): Value for action or empty
  9. enabled (str): "true" or "false" indicating if rule is active
- Examples:
  ```
  john_doe|1|Morning Lights|Time|07:00|1|Turn On||true
  john_doe|2|Night Mode|Time|22:00|1|Set Brightness|20|true
  jane_smith|1|Motion Alert|Motion|detected|3|Turn On||true
  ```

---

### 5. energy_logs.txt
- Path: data/energy_logs.txt
- Fields (pipe-delimited):
  1. username (str): Owner username
  2. device_id (int): Device identifier
  3. date (str): Date in YYYY-MM-DD format
  4. consumption_kwh (float): Energy consumption in kWh
- Examples:
  ```
  john_doe|1|2024-11-01|0.5
  john_doe|2|2024-11-01|2.3
  john_doe|1|2024-11-02|0.6
  jane_smith|3|2024-11-01|0.2
  ```

---

### 6. activity_logs.txt
- Path: data/activity_logs.txt
- Fields (pipe-delimited):
  1. username (str): Owner username
  2. timestamp (str): Datetime timestamp YYYY-MM-DD HH:MM:SS
  3. device_id (int): Device identifier
  4. action (str): Action performed
  5. details (str): Additional details
- Examples:
  ```
  john_doe|2024-11-01 07:00:00|1|Power On|Automation triggered: Morning Lights
  john_doe|2024-11-01 08:30:00|2|Settings Changed|Temperature set to 72
  jane_smith|2024-11-01 09:15:00|3|Power On|Manual control
  ```

---