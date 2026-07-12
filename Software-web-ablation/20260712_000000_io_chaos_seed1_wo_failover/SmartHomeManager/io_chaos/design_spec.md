# SmartHomeManager Design Specification

---

## Section 1: Flask Routes Specification

| Endpoint URL                | HTTP Methods | Function Name            | Template Rendered           | Context Variables (Name : Type)                       |
|-----------------------------|--------------|-------------------------|-----------------------------|-------------------------------------------------------|
| /                           | GET          | root_redirect            | N/A (Redirect to /dashboard) | N/A                                                   |
| /dashboard                  | GET          | dashboard_page           | dashboard.html              | devices_summary : dict (total: int, active: int, offline: int), rooms : list of dict(room_name: str, device_count: int) |
| /devices                    | GET          | device_list_page         | device_list.html            | devices : list of dict(device_id: int, device_name: str, device_type: str, room: str, status: str)                     |
| /device/add                 | GET, POST    | add_device_page          | add_device.html             | device_types : list of str, rooms : list of str, form_errors : dict (optional, str) (only on POST errors)             |
| /device/control/<int:device_id> | GET, POST    | device_control_page     | device_control.html         | device : dict(device_id: int, device_name: str, status: str, power: str, brightness: int or None, temperature: int or None, mode: str, schedule_time: str) |
| /automation                 | GET, POST    | automation_rules_page    | automation.html             | automation_rules : list of dict(rule_id: int, rule_name: str, trigger_type: str, trigger_value: str, action_device_id: int, action_type: str, enabled: bool), devices : list of dict(device_id: int, device_name: str) |
| /energy                    | GET, POST    | energy_report_page       | energy_report.html          | energy_logs : list of dict(device_id: int, device_name: str, date: str, consumption_kwh: float), total_consumption : float, total_cost : float |
| /activity                  | GET, POST    | activity_logs_page       | activity_logs.html          | activity_logs : list of dict(timestamp: str, device_id: int, device_name: str, action: str, details: str)               |

---

## Section 2: HTML Templates Specification

### 1. dashboard.html
- Filepath: templates/dashboard.html
- Page Title: Smart Home Dashboard
- Element IDs:
  - dashboard-page (Div): Container for dashboard page
  - device-summary (Div): Summary showing total devices, active devices, offline devices count
  - device-list-button (Button): Navigate to device list page
  - add-device-button (Button): Navigate to add device page
  - automation-button (Button): Navigate to automation rules page
  - energy-button (Button): Navigate to energy report page
  - activity-button (Button): Navigate to activity logs page
  - room-list (Div): List of all rooms with device counts
- Navigation mappings:
  - device-list-button: url_for('device_list_page')
  - add-device-button: url_for('add_device_page')
  - automation-button: url_for('automation_rules_page')
  - energy-button: url_for('energy_report_page')
  - activity-button: url_for('activity_logs_page')

### 2. device_list.html
- Filepath: templates/device_list.html
- Page Title: My Devices
- Element IDs:
  - device-list-page (Div): Container for device list page
  - device-table (Table): Displays all devices with columns: name, type, room, status, actions
  - control-device-button-{device_id} (Button): Navigate to device control page
  - back-to-dashboard (Button): Navigate back to dashboard
- Navigation mappings:
  - control-device-button-{device_id}: url_for('device_control_page', device_id=device_id)
  - back-to-dashboard: url_for('dashboard_page')

### 3. add_device.html
- Filepath: templates/add_device.html
- Page Title: Add New Device
- Element IDs:
  - add-device-page (Div): Container for add device page
  - device-name (Input): Input for device name
  - device-type (Dropdown): Device type dropdown (Light, Thermostat, Camera, Lock, Sensor, Appliance)
  - device-room (Dropdown): Room dropdown (Living Room, Bedroom, Kitchen, Bathroom, Garage)
  - submit-device-button (Button): Submit new device
  - back-to-dashboard (Button): Navigate back to dashboard
- Navigation mappings:
  - submit-device-button: POST to current route
  - back-to-dashboard: url_for('dashboard_page')

### 4. device_control.html
- Filepath: templates/device_control.html
- Page Title: Device Control
- Element IDs:
  - device-control-page (Div): Container for device control page
  - device-name-display (H2): Displays device name
  - device-status-display (Div): Displays current status (Online/Offline)
  - power-toggle (Button): Toggle device power on/off
  - save-settings-button (Button): Save device settings
  - back-to-devices (Button): Navigate back to device list
- Navigation mappings:
  - power-toggle: POST action to toggle power on current device
  - save-settings-button: POST action to save settings
  - back-to-devices: url_for('device_list_page')

### 5. automation.html
- Filepath: templates/automation.html
- Page Title: Automation Rules
- Element IDs:
  - automation-page (Div): Container for automation rules page
  - rules-table (Table): Displays automation rules with columns: name, trigger, action, status
  - rule-name (Input): Input for rule name
  - trigger-type (Dropdown): Trigger type dropdown (Time, Motion, Temperature)
  - trigger-value (Input): Field for trigger value
  - action-device (Dropdown): Dropdown to select target device
  - action-type (Dropdown): Action type dropdown (Turn On, Turn Off, Set Brightness, Set Temperature)
  - add-rule-button (Button): Add automation rule
  - back-to-dashboard (Button): Navigate back to dashboard
- Navigation mappings:
  - add-rule-button: POST to add new rule
  - back-to-dashboard: url_for('dashboard_page')

### 6. energy_report.html
- Filepath: templates/energy_report.html
- Page Title: Energy Report
- Element IDs:
  - energy-page (Div): Container for energy report page
  - energy-summary (Div): Shows total energy consumption and cost estimate
  - energy-table (Table): Displays energy consumption per device with date and kWh
  - date-filter (Input date): Filter energy data by date
  - apply-filter-button (Button): Apply date filter
  - back-to-dashboard (Button): Navigate back to dashboard
- Navigation mappings:
  - apply-filter-button: POST to apply filter
  - back-to-dashboard: url_for('dashboard_page')

### 7. activity_logs.html
- Filepath: templates/activity_logs.html
- Page Title: Activity Logs
- Element IDs:
  - activity-page (Div): Container for activity logs page
  - activity-table (Table): Displays activity logs with columns: timestamp, device, action, details
  - search-activity (Input): Search field for activity logs
  - apply-search-button (Button): Apply search filter
  - back-to-dashboard (Button): Navigate back to dashboard
- Navigation mappings:
  - apply-search-button: POST to apply search
  - back-to-dashboard: url_for('dashboard_page')

---

## Section 3: Data File Schemas

### 1. users.txt
- Path: data/users.txt
- Fields (Pipe-delimited): username|email
- Field descriptions:
  - username: str, unique user identifier
  - email: str, valid email address
- Examples:
  - john_doe|john@example.com
  - jane_smith|jane@example.com

### 2. devices.txt
- Path: data/devices.txt
- Fields (Pipe-delimited): username|device_id|device_name|device_type|room|brand|model|status|power|brightness|temperature|mode|schedule_time
- Field descriptions:
  - username: str, owner user
  - device_id: int, unique device identifier
  - device_name: str, friendly device name
  - device_type: str, one of (Light, Thermostat, Camera, Lock, Sensor, Appliance)
  - room: str, room name
  - brand: str, brand name
  - model: str, model identifier
  - status: str, "Online" or "Offline"
  - power: str, "on" or "off"
  - brightness: int or empty, brightness level (0-100) if applicable
  - temperature: int or empty, temperature setting if applicable
  - mode: str, operating mode (e.g., Auto, Manual)
  - schedule_time: str, time in HH:MM format or empty
- Examples:
  - john_doe|1|Living Room Light|Light|Living Room|Philips|Hue|Online|on|75|||Auto|
  - john_doe|2|Bedroom Thermostat|Thermostat|Bedroom|Nest|Learning|Online|on||72|Auto|22:00
  - jane_smith|3|Kitchen Camera|Camera|Kitchen|Ring|Indoor|Online|on||||Manual|

### 3. rooms.txt
- Path: data/rooms.txt
- Fields (Pipe-delimited): username|room_id|room_name
- Field descriptions:
  - username: str, owner user
  - room_id: int, unique room identifier
  - room_name: str, room name
- Examples:
  - john_doe|1|Living Room
  - john_doe|2|Bedroom
  - john_doe|3|Kitchen
  - jane_smith|1|Living Room

### 4. automation_rules.txt
- Path: data/automation_rules.txt
- Fields (Pipe-delimited): username|rule_id|rule_name|trigger_type|trigger_value|action_device_id|action_type|action_value|enabled
- Field descriptions:
  - username: str, owner user
  - rule_id: int, unique rule identifier
  - rule_name: str, friendly rule name
  - trigger_type: str, one of (Time, Motion, Temperature)
  - trigger_value: str, trigger detail (time HH:MM, detected, temperature value)
  - action_device_id: int, device id to control
  - action_type: str, one of (Turn On, Turn Off, Set Brightness, Set Temperature)
  - action_value: str, value for action or empty
  - enabled: bool ('true' or 'false')
- Examples:
  - john_doe|1|Morning Lights|Time|07:00|1|Turn On||true
  - john_doe|2|Night Mode|Time|22:00|1|Set Brightness|20|true
  - jane_smith|1|Motion Alert|Motion|detected|3|Turn On||true

### 5. energy_logs.txt
- Path: data/energy_logs.txt
- Fields (Pipe-delimited): username|device_id|date|consumption_kwh
- Field descriptions:
  - username: str, owner user
  - device_id: int, device identifier
  - date: str, in YYYY-MM-DD format
  - consumption_kwh: float, energy consumption in kWh
- Examples:
  - john_doe|1|2024-11-01|0.5
  - john_doe|2|2024-11-01|2.3
  - john_doe|1|2024-11-02|0.6
  - jane_smith|3|2024-11-01|0.2

### 6. activity_logs.txt
- Path: data/activity_logs.txt
- Fields (Pipe-delimited): username|timestamp|device_id|action|details
- Field descriptions:
  - username: str, owner user
  - timestamp: str, datetime format YYYY-MM-DD HH:MM:SS
  - device_id: int, device identifier
  - action: str, activity action performed
  - details: str, additional details of event
- Examples:
  - john_doe|2024-11-01 07:00:00|1|Power On|Automation triggered: Morning Lights
  - john_doe|2024-11-01 08:30:00|2|Settings Changed|Temperature set to 72
  - jane_smith|2024-11-01 09:15:00|3|Power On|Manual control

---

**End of Design Specification**
