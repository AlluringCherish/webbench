# Design Specification for SmartHomeManager Web Application

---

## Section 1: Flask Routes Specification

| Endpoint URL             | HTTP Methods | Function Name            | Template File           | Context Variables (Name : Type)                                 |
|--------------------------|--------------|--------------------------|-------------------------|----------------------------------------------------------------|
| /                        | GET          | root_redirect            | None (redirect)          | None                                                           |
| /dashboard               | GET          | dashboard                | dashboard.html          | devices_summary: dict, rooms_summary: dict                      |
| /devices                 | GET          | device_list              | device_list.html        | devices: list[dict], user: str                                  |
| /devices/<int:device_id> | GET, POST    | device_control           | device_control.html     | device: dict                                                   |
| /devices/add             | GET, POST    | add_device               | add_device.html         | rooms: list[str], device_types: list[str], errors: dict (POST only) |
| /automation              | GET, POST    | automation_rules         | automation.html         | rules: list[dict], devices: list[dict], errors: dict (POST only) |
| /energy                  | GET, POST    | energy_report            | energy.html             | energy_data: list[dict], energy_summary: dict, filter_date: str (POST only) |
| /activity                | GET, POST    | activity_logs            | activity_logs.html      | activities: list[dict], search_query: str (POST only)          |

### Notes:
- The root '/' route will redirect to '/dashboard'.
- POST methods are used where user input or filtering is applied.
- Dynamic route `/devices/<int:device_id>` for controlling a specific device.

---

## Section 2: HTML Templates Specification

### 1. Dashboard Page
- Filepath: templates/dashboard.html
- Page Title: Smart Home Dashboard
- Elements:
  - dashboard-page (Div): Container for the dashboard page.
  - device-summary (Div): Shows total devices, active devices, offline devices counts.
  - device-list-button (Button): Navigates to device list page.
  - add-device-button (Button): Navigates to add device page.
  - automation-button (Button): Navigates to automation rules page.
  - energy-button (Button): Navigates to energy report page.
  - activity-button (Button): Navigates to activity logs page.
  - room-list (Div): List of all rooms with device counts.
- Navigation mappings:
  - device-list-button: url_for('device_list')
  - add-device-button: url_for('add_device')
  - automation-button: url_for('automation_rules')
  - energy-button: url_for('energy_report')
  - activity-button: url_for('activity_logs')


### 2. Device List Page
- Filepath: templates/device_list.html
- Page Title: My Devices
- Elements:
  - device-list-page (Div): Container for the device list page.
  - device-table (Table): Displays all devices with columns for name, type, room, status, and actions.
  - control-device-button-{device_id} (Button for each device): Navigates to device control page for that device.
  - back-to-dashboard (Button): Navigate back to dashboard.
- Navigation mappings:
  - control-device-button-{device_id}: url_for('device_control', device_id=device_id)
  - back-to-dashboard: url_for('dashboard')


### 3. Add Device Page
- Filepath: templates/add_device.html
- Page Title: Add New Device
- Elements:
  - add-device-page (Div): Container for the add device page.
  - device-name (Input - text): Field to input device name.
  - device-type (Dropdown): Select device type (Light, Thermostat, Camera, Lock, Sensor, Appliance).
  - device-room (Dropdown): Select room (Living Room, Bedroom, Kitchen, Bathroom, Garage).
  - submit-device-button (Button): Submit the new device.
  - back-to-dashboard (Button): Navigate back to dashboard.
- Navigation mappings:
  - submit-device-button: Form submit action POST to '/devices/add'
  - back-to-dashboard: url_for('dashboard')


### 4. Device Control Page
- Filepath: templates/device_control.html
- Page Title: Device Control
- Elements:
  - device-control-page (Div): Container for the device control page.
  - device-name-display (H2): Display device name.
  - device-status-display (Div): Display current device status (Online/Offline).
  - power-toggle (Button): Toggle device power on/off.
  - save-settings-button (Button): Save device settings.
  - back-to-devices (Button): Navigate back to device list.
- Navigation mappings:
  - power-toggle: POST action within device control page.
  - save-settings-button: POST action within device control page.
  - back-to-devices: url_for('device_list')


### 5. Automation Rules Page
- Filepath: templates/automation.html
- Page Title: Automation Rules
- Elements:
  - automation-page (Div): Container for the automation rules page.
  - rules-table (Table): Displays all automation rules with columns: name, trigger, action, status.
  - rule-name (Input - text): Input new rule name.
  - trigger-type (Dropdown): Select trigger type (Time, Motion, Temperature).
  - trigger-value (Input - text): Input trigger value.
  - action-device (Dropdown): Select target device.
  - action-type (Dropdown): Select action type (Turn On, Turn Off, Set Brightness, Set Temperature).
  - add-rule-button (Button): Add new automation rule.
  - back-to-dashboard (Button): Navigate back to dashboard.
- Navigation mappings:
  - add-rule-button: Form submit POST to '/automation'
  - back-to-dashboard: url_for('dashboard')


### 6. Energy Report Page
- Filepath: templates/energy.html
- Page Title: Energy Report
- Elements:
  - energy-page (Div): Container for the energy report page.
  - energy-summary (Div): Show total energy consumption and cost estimate.
  - energy-table (Table): Display energy consumption per device with date and kWh.
  - date-filter (Input - date): Filter energy data by date.
  - apply-filter-button (Button): Apply date filter.
  - back-to-dashboard (Button): Navigate back to dashboard.
- Navigation mappings:
  - apply-filter-button: Form submit POST with filter date
  - back-to-dashboard: url_for('dashboard')


### 7. Activity Logs Page
- Filepath: templates/activity_logs.html
- Page Title: Activity Logs
- Elements:
  - activity-page (Div): Container for the activity logs page.
  - activity-table (Table): Displays activity logs with columns: timestamp, device, action, details.
  - search-activity (Input - text): Search field for activity logs.
  - apply-search-button (Button): Apply search filter.
  - back-to-dashboard (Button): Navigate back to dashboard.
- Navigation mappings:
  - apply-search-button: Form submit POST with search query
  - back-to-dashboard: url_for('dashboard')

---

## Section 3: Data File Schemas

### 1. users.txt
- Path: data/users.txt
- Format: pipe-delimited
- Fields (in order):
  1. username (str) - unique user identifier
  2. email (str) - user email address
- Example lines:
  john_doe|john@example.com
  jane_smith|jane@example.com


### 2. devices.txt
- Path: data/devices.txt
- Format: pipe-delimited
- Fields (in order):
  1. username (str) - owner
  2. device_id (int) - unique device identifier
  3. device_name (str) - device name
  4. device_type (str) - type (Light, Thermostat, Camera, Lock, Sensor, Appliance)
  5. room (str) - which room
  6. brand (str)
  7. model (str)
  8. status (str) - Online or Offline
  9. power (str) - on/off
  10. brightness (int or empty) - brightness percent (0-100) or empty
  11. temperature (int or empty) - temperature value or empty
  12. mode (str) - e.g., Auto, Manual, or empty
  13. schedule_time (str) - scheduled time (e.g., 22:00) or empty
- Example lines:
  john_doe|1|Living Room Light|Light|Living Room|Philips|Hue|Online|on|75|||Auto|
  john_doe|2|Bedroom Thermostat|Thermostat|Bedroom|Nest|Learning|Online|on||72|Auto|22:00
  jane_smith|3|Kitchen Camera|Camera|Kitchen|Ring|Indoor|Online|on||||Manual|


### 3. rooms.txt
- Path: data/rooms.txt
- Format: pipe-delimited
- Fields (in order):
  1. username (str) - owner
  2. room_id (int) - unique room identifier
  3. room_name (str) - name of room
- Example lines:
  john_doe|1|Living Room
  john_doe|2|Bedroom
  john_doe|3|Kitchen
  jane_smith|1|Living Room


### 4. automation_rules.txt
- Path: data/automation_rules.txt
- Format: pipe-delimited
- Fields (in order):
  1. username (str) - owner
  2. rule_id (int) - unique rule identifier
  3. rule_name (str) - name of rule
  4. trigger_type (str) - Time, Motion, Temperature
  5. trigger_value (str) - trigger value (time like "07:00" or string like "detected")
  6. action_device_id (int) - device id to act on
  7. action_type (str) - Turn On, Turn Off, Set Brightness, Set Temperature
  8. action_value (str) - e.g., brightness %, temperature setting or empty
  9. enabled (bool) - true or false
- Example lines:
  john_doe|1|Morning Lights|Time|07:00|1|Turn On||true
  john_doe|2|Night Mode|Time|22:00|1|Set Brightness|20|true
  jane_smith|1|Motion Alert|Motion|detected|3|Turn On||true


### 5. energy_logs.txt
- Path: data/energy_logs.txt
- Format: pipe-delimited
- Fields (in order):
  1. username (str) - owner
  2. device_id (int) - device identifier
  3. date (str) - date in YYYY-MM-DD format
  4. consumption_kwh (float) - energy consumed in kWh
- Example lines:
  john_doe|1|2024-11-01|0.5
  john_doe|2|2024-11-01|2.3
  john_doe|1|2024-11-02|0.6
  jane_smith|3|2024-11-01|0.2


### 6. activity_logs.txt
- Path: data/activity_logs.txt
- Format: pipe-delimited
- Fields (in order):
  1. username (str) - owner
  2. timestamp (str) - date-time in YYYY-MM-DD HH:MM:SS
  3. device_id (int) - device identifier
  4. action (str) - type of activity
  5. details (str) - additional info
- Example lines:
  john_doe|2024-11-01 07:00:00|1|Power On|Automation triggered: Morning Lights
  john_doe|2024-11-01 08:30:00|2|Settings Changed|Temperature set to 72
  jane_smith|2024-11-01 09:15:00|3|Power On|Manual control

---

End of design_spec.md
