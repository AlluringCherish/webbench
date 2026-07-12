# SmartHomeManager Design Specification

---

## Section 1: Flask Routes Specification

| Endpoint URL                  | HTTP Methods | Function Name            | Template Rendered          | Context Variables (name: type)                                              |
|------------------------------|--------------|-------------------------|----------------------------|----------------------------------------------------------------------------|
| /                            | GET          | root_redirect            | redirects to /dashboard     | None                                                                       |
| /dashboard                   | GET          | dashboard                | dashboard.html              | devices_summary: dict (with keys: total: int, active: int, offline: int)
|                              |              |                         |                            | rooms: list of dict {room_name: str, device_count: int}                     |
| /devices                    | GET          | device_list              | devices.html                | devices: list of dict {device_id: int, device_name: str, device_type: str, room:str, status: str} |
| /device/add                 | GET, POST    | add_device               | add_device.html             | device_types: list of str, rooms: list of str, error: str (optional)        |
| /device/<int:device_id>     | GET, POST    | device_control           | device_control.html         | device: dict with fields (device_id: int, device_name: str, status: str, power: str, brightness: int or None, temperature: int or None, mode: str, schedule_time: str) |
| /automation                 | GET, POST    | automation_rules         | automation.html             | automation_rules: list of dict with fields (rule_id: int, rule_name: str, trigger_type: str, trigger_value: str, action_device_id: int, action_type: str, action_value: str or None, enabled: bool) |
| /energy                    | GET, POST    | energy_report            | energy.html                 | energy_data: list of dict {device_id: int, device_name: str, date: str, consumption_kwh: float}
|                              |              |                         |                            | total_consumption: float, estimated_cost: float                             |
| /activity                  | GET, POST    | activity_logs            | activity_logs.html          | activities: list of dict {timestamp: str, device_id: int, device_name: str, action: str, details: str} |

Notes:
- Root route `/` redirects to `/dashboard`.
- POST methods on `/device/add`, `/device/<int:device_id>`, `/automation`, `/energy`, `/activity` are to handle form submissions like add device, update device, add automation rule, apply filters.
- Context variables are generalized for clarity.

---

## Section 2: HTML Templates Specification

### 1. Dashboard Page
- Filepath: templates/dashboard.html
- Page Title: Smart Home Dashboard
- Element IDs:
  - dashboard-page (Div): Container of the page
  - device-summary (Div): Summary showing total, active, offline device counts
  - device-list-button (Button): Navigates to device list page
  - add-device-button (Button): Navigates to add device page
  - automation-button (Button): Navigates to automation rules page
  - energy-button (Button): Navigates to energy report page
  - activity-button (Button): Navigates to activity logs page
  - room-list (Div): List of rooms with device counts
- Navigation mappings:
  - device-list-button: url_for('device_list')
  - add-device-button: url_for('add_device')
  - automation-button: url_for('automation_rules')
  - energy-button: url_for('energy_report')
  - activity-button: url_for('activity_logs')

### 2. Device List Page
- Filepath: templates/devices.html
- Page Title: My Devices
- Element IDs:
  - device-list-page (Div): Page container
  - device-table (Table): Displays devices data
  - control-device-button-{device_id} (Button): For each device row; navigates to control page
  - back-to-dashboard (Button): Navigates back to dashboard
- Navigation mappings:
  - control-device-button-{device_id}: url_for('device_control', device_id=device_id)
  - back-to-dashboard: url_for('dashboard')

### 3. Add Device Page
- Filepath: templates/add_device.html
- Page Title: Add New Device
- Element IDs:
  - add-device-page (Div): Page container
  - device-name (Input): Enter device name
  - device-type (Dropdown): Select device type (Light, Thermostat, Camera, Lock, Sensor, Appliance)
  - device-room (Dropdown): Select room (Living Room, Bedroom, Kitchen, Bathroom, Garage)
  - submit-device-button (Button): Submit form
  - back-to-dashboard (Button): Navigate to dashboard
- Navigation mappings:
  - back-to-dashboard: url_for('dashboard')

### 4. Device Control Page
- Filepath: templates/device_control.html
- Page Title: Device Control
- Element IDs:
  - device-control-page (Div): Page container
  - device-name-display (H2): Displays device name
  - device-status-display (Div): Shows current status (Online/Offline)
  - power-toggle (Button): Toggle power on/off
  - save-settings-button (Button): Save device settings
  - back-to-devices (Button): Navigate back to device list
- Navigation mappings:
  - back-to-devices: url_for('device_list')

### 5. Automation Rules Page
- Filepath: templates/automation.html
- Page Title: Automation Rules
- Element IDs:
  - automation-page (Div): Page container
  - rules-table (Table): Displays automation rules (name, trigger, action, status)
  - rule-name (Input): Enter rule name
  - trigger-type (Dropdown): Select trigger type (Time, Motion, Temperature)
  - trigger-value (Input): Enter trigger value
  - action-device (Dropdown): Select target device
  - action-type (Dropdown): Select action type (Turn On, Turn Off, Set Brightness, Set Temperature)
  - add-rule-button (Button): Add the new rule
  - back-to-dashboard (Button): Navigate to dashboard
- Navigation mappings:
  - back-to-dashboard: url_for('dashboard')

### 6. Energy Report Page
- Filepath: templates/energy.html
- Page Title: Energy Report
- Element IDs:
  - energy-page (Div): Page container
  - energy-summary (Div): Shows total energy consumption and cost estimate
  - energy-table (Table): Displays energy data per device (date, kWh)
  - date-filter (Input type=date): Filter energy data by date
  - apply-filter-button (Button): Apply the date filter
  - back-to-dashboard (Button): Navigate to dashboard
- Navigation mappings:
  - back-to-dashboard: url_for('dashboard')

### 7. Activity Logs Page
- Filepath: templates/activity_logs.html
- Page Title: Activity Logs
- Element IDs:
  - activity-page (Div): Page container
  - activity-table (Table): Displays activity logs (timestamp, device, action, details)
  - search-activity (Input): Search activity logs
  - apply-search-button (Button): Apply search filter
  - back-to-dashboard (Button): Navigate to dashboard
- Navigation mappings:
  - back-to-dashboard: url_for('dashboard')

---

## Section 3: Data File Schemas

### 1. users.txt
- Path: data/users.txt
- Pipe-delimited Fields:
  1. username (str): User identifier
  2. email (str): User email address
- Example lines:
  john_doe|john@example.com
  jane_smith|jane@example.com

### 2. devices.txt
- Path: data/devices.txt
- Pipe-delimited Fields:
  1. username (str): Owner's username
  2. device_id (int): Unique device identifier
  3. device_name (str): Human readable device name
  4. device_type (str): Type of device (Light, Thermostat, etc.)
  5. room (str): Room name where device is located
  6. brand (str): Device brand
  7. model (str): Device model
  8. status (str): Device status (Online/Offline)
  9. power (str): Power state (on/off)
  10. brightness (int or empty): Brightness level if applicable
  11. temperature (int or empty): Temperature setting if applicable
  12. mode (str): Mode setting (Auto, Manual, etc.)
  13. schedule_time (str): Scheduled time for actions if any
- Example lines:
  john_doe|1|Living Room Light|Light|Living Room|Philips|Hue|Online|on|75|||Auto|
  john_doe|2|Bedroom Thermostat|Thermostat|Bedroom|Nest|Learning|Online|on||72|Auto|22:00
  jane_smith|3|Kitchen Camera|Camera|Kitchen|Ring|Indoor|Online|on||||Manual|

### 3. rooms.txt
- Path: data/rooms.txt
- Pipe-delimited Fields:
  1. username (str): Owner's username
  2. room_id (int): Unique room identifier
  3. room_name (str): Name of the room
- Example lines:
  john_doe|1|Living Room
  john_doe|2|Bedroom
  john_doe|3|Kitchen
  jane_smith|1|Living Room

### 4. automation_rules.txt
- Path: data/automation_rules.txt
- Pipe-delimited Fields:
  1. username (str): Owner's username
  2. rule_id (int): Unique rule identifier
  3. rule_name (str): Name of the automation rule
  4. trigger_type (str): Trigger (Time, Motion, Temperature)
  5. trigger_value (str): Value (e.g., 07:00, detected, threshold)
  6. action_device_id (int): Target device ID
  7. action_type (str): Action to perform (Turn On, Turn Off, Set Brightness, Set Temperature)
  8. action_value (str or empty): Value for action (brightness or temperature)
  9. enabled (bool): true or false
- Example lines:
  john_doe|1|Morning Lights|Time|07:00|1|Turn On||true
  john_doe|2|Night Mode|Time|22:00|1|Set Brightness|20|true
  jane_smith|1|Motion Alert|Motion|detected|3|Turn On||true

### 5. energy_logs.txt
- Path: data/energy_logs.txt
- Pipe-delimited Fields:
  1. username (str): Owner's username
  2. device_id (int): Device identifier
  3. date (str): Date in YYYY-MM-DD
  4. consumption_kwh (float): Energy consumed in kWh
- Example lines:
  john_doe|1|2024-11-01|0.5
  john_doe|2|2024-11-01|2.3
  john_doe|1|2024-11-02|0.6
  jane_smith|3|2024-11-01|0.2

### 6. activity_logs.txt
- Path: data/activity_logs.txt
- Pipe-delimited Fields:
  1. username (str): Owner's username
  2. timestamp (str): Datetime in YYYY-MM-DD HH:MM:SS
  3. device_id (int): Device identifier
  4. action (str): Action performed
  5. details (str): Additional details about the action
- Example lines:
  john_doe|2024-11-01 07:00:00|1|Power On|Automation triggered: Morning Lights
  john_doe|2024-11-01 08:30:00|2|Settings Changed|Temperature set to 72
  jane_smith|2024-11-01 09:15:00|3|Power On|Manual control

---

All templates and data files are defined to ensure consistent implementation and integration.

This single source of truth enables backend and frontend teams to develop independently with full accuracy and coherence.
