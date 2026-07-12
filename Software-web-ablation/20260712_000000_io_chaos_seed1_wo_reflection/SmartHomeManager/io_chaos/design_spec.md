# SmartHomeManager Design Specifications

---

## Section 1: Flask Routes Specification

| Endpoint URL                | HTTP Methods | Function Name           | Template Rendered         | Context Variables (var_name: type)                              |
|-----------------------------|--------------|------------------------|---------------------------|----------------------------------------------------------------|
| /                           | GET          | root_redirect          | None                      | None                                                           |
| /dashboard                  | GET          | dashboard_page         | dashboard.html            | devices_summary: dict, rooms_overview: list                    |
| /devices                   | GET          | device_list_page       | devices.html              | devices: list, user: str                                        |
| /device/add                | GET, POST    | add_device_page        | add_device.html           | device_types: list[str], rooms: list[str], form_errors: dict   |
| /device/control/<int:device_id> | GET, POST    | device_control_page    | device_control.html       | device: dict, form_errors: dict                                |
| /automation                | GET, POST    | automation_rules_page  | automation.html           | rules: list, devices: list, form_errors: dict                 |
| /energy                   | GET, POST    | energy_report_page     | energy.html               | energy_data: list, energy_summary: dict, filter_date: str      |
| /activity                 | GET, POST    | activity_logs_page     | activity.html             | activities: list, search_query: str                            |

---

### Route Descriptions:

- **root_redirect**: Redirects '/' to '/dashboard'.
- **dashboard_page**: Displays overview of devices and rooms.
- **device_list_page**: Lists all devices with quick controls.
- **add_device_page**: Displays form and handles adding new device.
- **device_control_page**: Controls a device by device_id, shows status, allows settings update.
- **automation_rules_page**: Lists, adds automation rules, manages form input.
- **energy_report_page**: Shows energy consumption data and filtering.
- **activity_logs_page**: Displays and filters activity logs.

---

## Section 2: HTML Templates Specification

### 1. Dashboard Page
- Filepath: templates/dashboard.html
- Page Title: Smart Home Dashboard
- Element IDs:
  - dashboard-page: Div - Container for entire dashboard.
  - device-summary: Div - Shows total, active, and offline devices count.
  - device-list-button: Button - Navigates to device list page.
  - add-device-button: Button - Navigates to add device page.
  - automation-button: Button - Navigates to automation rules page.
  - energy-button: Button - Navigates to energy report page.
  - activity-button: Button - Navigates to activity logs page.
  - room-list: Div - Displays rooms with device counts.
- Navigation mappings:
  - device-list-button: url_for('device_list_page')
  - add-device-button: url_for('add_device_page')
  - automation-button: url_for('automation_rules_page')
  - energy-button: url_for('energy_report_page')
  - activity-button: url_for('activity_logs_page')

---

### 2. Device List Page
- Filepath: templates/devices.html
- Page Title: My Devices
- Element IDs:
  - device-list-page: Div - Container for device list.
  - device-table: Table - Lists devices with columns: name, type, room, status, actions.
  - control-device-button-{device_id}: Button - Navigates to control page for each device.
    Pattern: control-device-button-{device_id} where device_id is int.
  - back-to-dashboard: Button - Navigates back to dashboard.
- Navigation mappings:
  - control-device-button-{device_id}: url_for('device_control_page', device_id=device_id)
  - back-to-dashboard: url_for('dashboard_page')

---

### 3. Add Device Page
- Filepath: templates/add_device.html
- Page Title: Add New Device
- Element IDs:
  - add-device-page: Div - Container for add device form.
  - device-name: Input - Text input for device name.
  - device-type: Dropdown - Select device type (Light, Thermostat, Camera, Lock, Sensor, Appliance).
  - device-room: Dropdown - Select room (Living Room, Bedroom, Kitchen, Bathroom, Garage).
  - submit-device-button: Button - Submits new device form.
  - back-to-dashboard: Button - Navigates back to dashboard.
- Navigation mappings:
  - back-to-dashboard: url_for('dashboard_page')

---

### 4. Device Control Page
- Filepath: templates/device_control.html
- Page Title: Device Control
- Element IDs:
  - device-control-page: Div - Container for device control.
  - device-name-display: H2 - Displays device name.
  - device-status-display: Div - Shows device status (Online/Offline).
  - power-toggle: Button - Toggles power state on/off.
  - save-settings-button: Button - Saves device settings.
  - back-to-devices: Button - Navigates back to device list.
- Navigation mappings:
  - back-to-devices: url_for('device_list_page')

---

### 5. Automation Rules Page
- Filepath: templates/automation.html
- Page Title: Automation Rules
- Element IDs:
  - automation-page: Div - Container for automation rules.
  - rules-table: Table - Shows rules with columns: name, trigger, action, status.
  - rule-name: Input - Text input for rule name.
  - trigger-type: Dropdown - Select trigger type (Time, Motion, Temperature).
  - trigger-value: Input - Input trigger value (time or threshold).
  - action-device: Dropdown - Select target device.
  - action-type: Dropdown - Select action type (Turn On, Turn Off, Set Brightness, Set Temperature).
  - add-rule-button: Button - Adds new rule.
  - back-to-dashboard: Button - Navigates back to dashboard.
- Navigation mappings:
  - back-to-dashboard: url_for('dashboard_page')

---

### 6. Energy Report Page
- Filepath: templates/energy.html
- Page Title: Energy Report
- Element IDs:
  - energy-page: Div - Container for energy report.
  - energy-summary: Div - Shows total energy consumption and cost estimate.
  - energy-table: Table - Shows energy consumption per device with date and kWh.
  - date-filter: Input (date) - Filters energy data by date.
  - apply-filter-button: Button - Applies date filter.
  - back-to-dashboard: Button - Navigates back to dashboard.
- Navigation mappings:
  - apply-filter-button: Submits filter (form POST to /energy)
  - back-to-dashboard: url_for('dashboard_page')

---

### 7. Activity Logs Page
- Filepath: templates/activity.html
- Page Title: Activity Logs
- Element IDs:
  - activity-page: Div - Container for activity logs.
  - activity-table: Table - Shows logs with timestamp, device, action, details.
  - search-activity: Input - Text input to search activity logs.
  - apply-search-button: Button - Applies search filter.
  - back-to-dashboard: Button - Navigates back to dashboard.
- Navigation mappings:
  - apply-search-button: Submits search form (POST /activity)
  - back-to-dashboard: url_for('dashboard_page')

---

## Section 3: Data File Schemas

### 1. users.txt
- Path: data/users.txt
- Fields (pipe-delimited): username | email
- Description:
  - username: str, unique user identifier
  - email: str, user email address
- Example Lines:
  - john_doe|john@example.com
  - jane_smith|jane@example.com

---

### 2. devices.txt
- Path: data/devices.txt
- Fields (pipe-delimited): username | device_id | device_name | device_type | room | brand | model | status | power | brightness | temperature | mode | schedule_time
- Description:
  - username: str, owner user
  - device_id: int, unique device identifier
  - device_name: str, device display name
  - device_type: str, type of device (Light, Thermostat, Camera, etc.)
  - room: str, room name
  - brand: str, manufacturer brand
  - model: str, model name
  - status: str, device connectivity status (Online/Offline)
  - power: str, power state (on/off)
  - brightness: int or empty, brightness level (0-100) for lights
  - temperature: int or empty, temperature setting for thermostats
  - mode: str, mode status (Auto, Manual, etc.)
  - schedule_time: str or empty, time string for scheduled action
- Example Lines:
  - john_doe|1|Living Room Light|Light|Living Room|Philips|Hue|Online|on|75|||Auto|
  - john_doe|2|Bedroom Thermostat|Thermostat|Bedroom|Nest|Learning|Online|on||72|Auto|22:00
  - jane_smith|3|Kitchen Camera|Camera|Kitchen|Ring|Indoor|Online|on||||Manual|

---

### 3. rooms.txt
- Path: data/rooms.txt
- Fields (pipe-delimited): username | room_id | room_name
- Description:
  - username: str, owner user
  - room_id: int, unique room identifier
  - room_name: str, name of the room
- Example Lines:
  - john_doe|1|Living Room
  - john_doe|2|Bedroom
  - john_doe|3|Kitchen
  - jane_smith|1|Living Room

---

### 4. automation_rules.txt
- Path: data/automation_rules.txt
- Fields (pipe-delimited): username | rule_id | rule_name | trigger_type | trigger_value | action_device_id | action_type | action_value | enabled
- Description:
  - username: str, owner user
  - rule_id: int, unique rule identifier
  - rule_name: str, name describing the rule
  - trigger_type: str, e.g., Time, Motion, Temperature
  - trigger_value: str, value for trigger (e.g., time or detected)
  - action_device_id: int, device to perform action on
  - action_type: str, e.g., Turn On, Turn Off, Set Brightness
  - action_value: str, optional value (brightness, temperature), may be empty
  - enabled: bool as string ('true'/'false'), status of rule
- Example Lines:
  - john_doe|1|Morning Lights|Time|07:00|1|Turn On||true
  - john_doe|2|Night Mode|Time|22:00|1|Set Brightness|20|true
  - jane_smith|1|Motion Alert|Motion|detected|3|Turn On||true

---

### 5. energy_logs.txt
- Path: data/energy_logs.txt
- Fields (pipe-delimited): username | device_id | date | consumption_kwh
- Description:
  - username: str, owner user
  - device_id: int, device identifier
  - date: str, in format YYYY-MM-DD
  - consumption_kwh: float, energy consumed in kWh
- Example Lines:
  - john_doe|1|2024-11-01|0.5
  - john_doe|2|2024-11-01|2.3
  - john_doe|1|2024-11-02|0.6
  - jane_smith|3|2024-11-01|0.2

---

### 6. activity_logs.txt
- Path: data/activity_logs.txt
- Fields (pipe-delimited): username | timestamp | device_id | action | details
- Description:
  - username: str, owner user
  - timestamp: str, datetime in format YYYY-MM-DD HH:MM:SS
  - device_id: int, device identifier
  - action: str, action performed (Power On, Settings Changed, etc.)
  - details: str, description of event
- Example Lines:
  - john_doe|2024-11-01 07:00:00|1|Power On|Automation triggered: Morning Lights
  - john_doe|2024-11-01 08:30:00|2|Settings Changed|Temperature set to 72
  - jane_smith|2024-11-01 09:15:00|3|Power On|Manual control

---

# End of design_spec.md
