# SmartHomeManager Design Specification

---

## Section 1: Flask Routes Specification

| Endpoint URL                | HTTP Methods | Function Name               | Template Filename           | Context Variables (name:type)                                      |
|----------------------------|--------------|-----------------------------|-----------------------------|------------------------------------------------------------------|
| /                          | GET          | root_redirect               | None                        | None (redirects to dashboard)                                    |
| /dashboard                 | GET          | dashboard_page             | dashboard.html              | total_devices:int, active_devices:int, offline_devices:int, rooms:list[dict] |
| /devices                   | GET          | device_list_page           | device_list.html            | devices:list[dict]                                               |
| /devices/add               | GET, POST    | add_device_page            | add_device.html             | If GET: none; If POST: form_submission_result:str                |
| /devices/control/<int:device_id> | GET, POST    | device_control_page        | device_control.html         | device:dict                                                      |
| /automation                | GET, POST    | automation_rules_page      | automation_rules.html       | rules:list[dict], devices:list[dict], form_result:str            |
| /energy                   | GET, POST    | energy_report_page         | energy_report.html          | energy_records:list[dict], total_consumption:float, cost_estimate:float, filter_date:str |
| /activity                 | GET, POST    | activity_logs_page         | activity_logs.html          | activities:list[dict], search_query:str                          |

---

## Section 2: HTML Templates Specification

### 1. dashboard.html
- File Path: templates/dashboard.html
- Page Title: Smart Home Dashboard
- Elements:
  - ID: dashboard-page (Div) - Container for the dashboard page
  - ID: device-summary (Div) - Summary showing total devices, active devices, and offline devices count
  - ID: device-list-button (Button) - Navigate to device list page
  - ID: add-device-button (Button) - Navigate to add device page
  - ID: automation-button (Button) - Navigate to automation rules page
  - ID: energy-button (Button) - Navigate to energy report page
  - ID: activity-button (Button) - Navigate to activity logs page
  - ID: room-list (Div) - List of all rooms with device counts
- Navigation mappings:
  - device-list-button: url_for('device_list_page')
  - add-device-button: url_for('add_device_page')
  - automation-button: url_for('automation_rules_page')
  - energy-button: url_for('energy_report_page')
  - activity-button: url_for('activity_logs_page')

### 2. device_list.html
- File Path: templates/device_list.html
- Page Title: My Devices
- Elements:
  - ID: device-list-page (Div) - Container for the device list page
  - ID: device-table (Table) - Displays all devices with name, type, room, status, actions
  - ID Pattern: control-device-button-{device_id} (Button) - Navigate to device control page for device_id
  - ID: back-to-dashboard (Button) - Navigate back to dashboard
- Navigation mappings:
  - control-device-button-{device_id}: url_for('device_control_page', device_id=device_id)
  - back-to-dashboard: url_for('dashboard_page')

### 3. add_device.html
- File Path: templates/add_device.html
- Page Title: Add New Device
- Elements:
  - ID: add-device-page (Div) - Container for the add device page
  - ID: device-name (Input) - Input for device name
  - ID: device-type (Dropdown) - Device type options: Light, Thermostat, Camera, Lock, Sensor, Appliance
  - ID: device-room (Dropdown) - Room options: Living Room, Bedroom, Kitchen, Bathroom, Garage
  - ID: submit-device-button (Button) - Submit new device
  - ID: back-to-dashboard (Button) - Navigate back to dashboard
- Navigation mappings:
  - back-to-dashboard: url_for('dashboard_page')

### 4. device_control.html
- File Path: templates/device_control.html
- Page Title: Device Control
- Elements:
  - ID: device-control-page (Div) - Container for the device control page
  - ID: device-name-display (H2) - Display device name
  - ID: device-status-display (Div) - Display current status (Online/Offline)
  - ID: power-toggle (Button) - Toggle power on/off
  - ID: save-settings-button (Button) - Save device settings
  - ID: back-to-devices (Button) - Navigate back to device list
- Navigation mappings:
  - back-to-devices: url_for('device_list_page')

### 5. automation_rules.html
- File Path: templates/automation_rules.html
- Page Title: Automation Rules
- Elements:
  - ID: automation-page (Div) - Container for the automation rules page
  - ID: rules-table (Table) - Displays all automation rules with name, trigger, action, status
  - ID: rule-name (Input) - Input rule name
  - ID: trigger-type (Dropdown) - Trigger type options: Time, Motion, Temperature
  - ID: trigger-value (Input) - Input trigger value (time or threshold)
  - ID: action-device (Dropdown) - Device selection
  - ID: action-type (Dropdown) - Actions: Turn On, Turn Off, Set Brightness, Set Temperature
  - ID: add-rule-button (Button) - Add new automation rule
  - ID: back-to-dashboard (Button) - Navigate back to dashboard
- Navigation mappings:
  - back-to-dashboard: url_for('dashboard_page')

### 6. energy_report.html
- File Path: templates/energy_report.html
- Page Title: Energy Report
- Elements:
  - ID: energy-page (Div) - Container for the energy report page
  - ID: energy-summary (Div) - Summary of total consumption and cost
  - ID: energy-table (Table) - Displays energy consumption per device with date and kWh
  - ID: date-filter (Input date) - Filter energy data by date
  - ID: apply-filter-button (Button) - Apply date filter
  - ID: back-to-dashboard (Button) - Navigate back to dashboard
- Navigation mappings:
  - back-to-dashboard: url_for('dashboard_page')

### 7. activity_logs.html
- File Path: templates/activity_logs.html
- Page Title: Activity Logs
- Elements:
  - ID: activity-page (Div) - Container for activity logs page
  - ID: activity-table (Table) - Displays logs with timestamp, device, action, details
  - ID: search-activity (Input) - Search field
  - ID: apply-search-button (Button) - Apply search filter
  - ID: back-to-dashboard (Button) - Navigate back to dashboard
- Navigation mappings:
  - back-to-dashboard: url_for('dashboard_page')

---

## Section 3: Data File Schemas

### 1. users.txt
- Filename: data/users.txt
- Fields (pipe-delimited, order-sensitive): username|email
- Field Descriptions:
  - username (str): Unique user identifier
  - email (str): User email address
- Examples:
  - john_doe|john@example.com
  - jane_smith|jane@example.com

### 2. devices.txt
- Filename: data/devices.txt
- Fields (pipe-delimited, order-sensitive): username|device_id|device_name|device_type|room|brand|model|status|power|brightness|temperature|mode|schedule_time
- Field Descriptions:
  - username (str): Owner of device
  - device_id (int): Unique device identifier
  - device_name (str): Name given to device
  - device_type (str): Device category (Light, Thermostat, Camera, Lock, Sensor, Appliance)
  - room (str): Assigned room
  - brand (str): Device brand
  - model (str): Device model
  - status (str): Current status (Online/Offline)
  - power (str): Power state (on/off)
  - brightness (int or empty): Brightness level (0-100), empty if not applicable
  - temperature (int or empty): Temperature setting, empty if not applicable
  - mode (str): Operating mode (Auto, Manual)
  - schedule_time (str): Scheduled time for action, may be empty
- Examples:
  - john_doe|1|Living Room Light|Light|Living Room|Philips|Hue|Online|on|75|||Auto|
  - john_doe|2|Bedroom Thermostat|Thermostat|Bedroom|Nest|Learning|Online|on||72|Auto|22:00
  - jane_smith|3|Kitchen Camera|Camera|Kitchen|Ring|Indoor|Online|on||||Manual|

### 3. rooms.txt
- Filename: data/rooms.txt
- Fields (pipe-delimited, order-sensitive): username|room_id|room_name
- Field Descriptions:
  - username (str): Owner of the rooms
  - room_id (int): Unique room identifier
  - room_name (str): Name of the room
- Examples:
  - john_doe|1|Living Room
  - john_doe|2|Bedroom
  - john_doe|3|Kitchen
  - jane_smith|1|Living Room

### 4. automation_rules.txt
- Filename: data/automation_rules.txt
- Fields (pipe-delimited, order-sensitive): username|rule_id|rule_name|trigger_type|trigger_value|action_device_id|action_type|action_value|enabled
- Field Descriptions:
  - username (str): Owner of rule
  - rule_id (int): Unique rule identifier
  - rule_name (str): Name of the rule
  - trigger_type (str): Type of trigger (Time, Motion, Temperature)
  - trigger_value (str): Trigger specifics (time, detected, threshold)
  - action_device_id (int): Target device ID for action
  - action_type (str): Action to perform (Turn On, Turn Off, Set Brightness, Set Temperature)
  - action_value (str): Parameter value for action if applicable
  - enabled (bool): Rule enabled status
- Examples:
  - john_doe|1|Morning Lights|Time|07:00|1|Turn On||true
  - john_doe|2|Night Mode|Time|22:00|1|Set Brightness|20|true
  - jane_smith|1|Motion Alert|Motion|detected|3|Turn On||true

### 5. energy_logs.txt
- Filename: data/energy_logs.txt
- Fields (pipe-delimited, order-sensitive): username|device_id|date|consumption_kwh
- Field Descriptions:
  - username (str): Owner of record
  - device_id (int): Device identifier
  - date (ISO date str): Date of consumption record
  - consumption_kwh (float): Energy consumed in kWh
- Examples:
  - john_doe|1|2024-11-01|0.5
  - john_doe|2|2024-11-01|2.3
  - john_doe|1|2024-11-02|0.6
  - jane_smith|3|2024-11-01|0.2

### 6. activity_logs.txt
- Filename: data/activity_logs.txt
- Fields (pipe-delimited, order-sensitive): username|timestamp|device_id|action|details
- Field Descriptions:
  - username (str): Owner of log
  - timestamp (ISO datetime str): Timestamp of event
  - device_id (int): Device involved
  - action (str): Action taken
  - details (str): Detail description
- Examples:
  - john_doe|2024-11-01 07:00:00|1|Power On|Automation triggered: Morning Lights
  - john_doe|2024-11-01 08:30:00|2|Settings Changed|Temperature set to 72
  - jane_smith|2024-11-01 09:15:00|3|Power On|Manual control
