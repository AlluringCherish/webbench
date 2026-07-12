# SmartHomeManager Design Specification

---

## Section 1: Flask Routes Specification

| Endpoint URL               | HTTP Methods | Function Name           | Template Rendered           | Context Variables (name:type)                          |
|----------------------------|--------------|------------------------|-----------------------------|--------------------------------------------------------|
| /                          | GET          | root_redirect          | None (redirect)              | None                                                   |
| /dashboard                 | GET          | dashboard              | dashboard.html              | devices_summary: dict, rooms: list                     |
| /devices                   | GET          | device_list            | devices.html                | devices: list of dicts                                 |
| /device/add                | GET, POST    | add_device             | add_device.html             | device_types: list(str), rooms: list(str), message:str |
| /device/<int:device_id>    | GET, POST    | device_control         | device_control.html         | device: dict, message: str                              |
| /automation                | GET, POST    | automation_rules       | automation.html             | rules: list of dicts, devices: list of dicts, message:str |
| /energy                   | GET, POST    | energy_report          | energy_report.html          | energy_logs: list of dicts, summary: dict, filter_date:str |
| /activity                 | GET, POST    | activity_logs          | activity_logs.html          | activities: list of dicts, search_query: str            |

**Details:**
- The root URL `/` redirects to `/dashboard`.
- `/devices` lists all devices for the logged-in user.
- `/device/add` allows displaying the add device form (GET) and submitting new devices (POST).
- `/device/<int:device_id>` shows device control page and handles updates (GET, POST).
- `/automation` manages automation rules with list display and adding new rules.
- `/energy` shows energy consumption with optional date filtering.
- `/activity` displays activity logs with optional search filtering.


---

## Section 2: HTML Templates Specification

### 1. dashboard.html
- Filepath: templates/dashboard.html
- Page Title: Smart Home Dashboard
- Elements:
  - `dashboard-page` (Div) - Container
  - `device-summary` (Div) - Shows total devices, active devices, offline devices
  - `device-list-button` (Button) - Navigate to device list page
  - `add-device-button` (Button) - Navigate to add device page
  - `automation-button` (Button) - Navigate to automation rules page
  - `energy-button` (Button) - Navigate to energy report page
  - `activity-button` (Button) - Navigate to activity logs page
  - `room-list` (Div) - Lists rooms with device counts
- Navigation mappings:
  - `device-list-button`: url_for('device_list')
  - `add-device-button`: url_for('add_device')
  - `automation-button`: url_for('automation_rules')
  - `energy-button`: url_for('energy_report')
  - `activity-button`: url_for('activity_logs')

### 2. devices.html
- Filepath: templates/devices.html
- Page Title: My Devices
- Elements:
  - `device-list-page` (Div)
  - `device-table` (Table) - Columns: name, type, room, status, actions
  - `control-device-button-{device_id}` (Button) - Navigate to control device page, pattern:
    `control-device-button-<device_id>`
  - `back-to-dashboard` (Button) - Navigate to dashboard
- Navigation mappings:
  - `control-device-button-{device_id}`: url_for('device_control', device_id=device_id)
  - `back-to-dashboard`: url_for('dashboard')

### 3. add_device.html
- Filepath: templates/add_device.html
- Page Title: Add New Device
- Elements:
  - `add-device-page` (Div)
  - `device-name` (Input text) - Device name input
  - `device-type` (Dropdown) - Options: Light, Thermostat, Camera, Lock, Sensor, Appliance
  - `device-room` (Dropdown) - Options: Living Room, Bedroom, Kitchen, Bathroom, Garage
  - `submit-device-button` (Button) - Submit new device
  - `back-to-dashboard` (Button) - Navigate to dashboard
- Navigation mappings:
  - `back-to-dashboard`: url_for('dashboard')

### 4. device_control.html
- Filepath: templates/device_control.html
- Page Title: Device Control
- Elements:
  - `device-control-page` (Div)
  - `device-name-display` (H2) - Shows device name
  - `device-status-display` (Div) - Shows current status (Online/Offline)
  - `power-toggle` (Button) - Toggle device power on/off
  - `save-settings-button` (Button) - Save device settings
  - `back-to-devices` (Button) - Navigate back to device list
- Navigation mappings:
  - `back-to-devices`: url_for('device_list')

### 5. automation.html
- Filepath: templates/automation.html
- Page Title: Automation Rules
- Elements:
  - `automation-page` (Div)
  - `rules-table` (Table) - Columns: name, trigger, action, status
  - `rule-name` (Input text) - New rule name
  - `trigger-type` (Dropdown) - Options: Time, Motion, Temperature
  - `trigger-value` (Input text) - Value for trigger
  - `action-device` (Dropdown) - List of user devices
  - `action-type` (Dropdown) - Options: Turn On, Turn Off, Set Brightness, Set Temperature
  - `add-rule-button` (Button) - Add new rule
  - `back-to-dashboard` (Button) - Navigate to dashboard
- Navigation mappings:
  - `back-to-dashboard`: url_for('dashboard')

### 6. energy_report.html
- Filepath: templates/energy_report.html
- Page Title: Energy Report
- Elements:
  - `energy-page` (Div)
  - `energy-summary` (Div) - Total consumption and cost
  - `energy-table` (Table) - Device energy data with date and kWh
  - `date-filter` (Input date) - Date filter field
  - `apply-filter-button` (Button) - Apply filter
  - `back-to-dashboard` (Button) - Navigate to dashboard
- Navigation mappings:
  - `back-to-dashboard`: url_for('dashboard')

### 7. activity_logs.html
- Filepath: templates/activity_logs.html
- Page Title: Activity Logs
- Elements:
  - `activity-page` (Div)
  - `activity-table` (Table) - Columns: timestamp, device, action, details
  - `search-activity` (Input text) - Search text
  - `apply-search-button` (Button) - Apply search
  - `back-to-dashboard` (Button) - Navigate to dashboard
- Navigation mappings:
  - `back-to-dashboard`: url_for('dashboard')

---

## Section 3: Data File Schemas

### 1. users.txt
- File: data/users.txt
- Fields (pipe-delimited):
  1. username (str) - User login name
  2. email (str) - User email address
- Example lines:
  ```
  john_doe|john@example.com
  jane_smith|jane@example.com
  ```

### 2. devices.txt
- File: data/devices.txt
- Fields:
  1. username (str) - Owning user
  2. device_id (int) - Unique device ID
  3. device_name (str) - Friendly device name
  4. device_type (str) - One of Light, Thermostat, Camera, Lock, Sensor, Appliance
  5. room (str) - Room name
  6. brand (str) - Device brand
  7. model (str) - Device model
  8. status (str) - Online or Offline
  9. power (str) - on or off
  10. brightness (str) - brightness level (0-100) or empty
  11. temperature (str) - temperature setting or empty
  12. mode (str) - mode string or empty
  13. schedule_time (str) - time string or empty
- Example lines:
  ```
  john_doe|1|Living Room Light|Light|Living Room|Philips|Hue|Online|on|75|||Auto|
  john_doe|2|Bedroom Thermostat|Thermostat|Bedroom|Nest|Learning|Online|on||72|Auto|22:00
  jane_smith|3|Kitchen Camera|Camera|Kitchen|Ring|Indoor|Online|on||||Manual|
  ```

### 3. rooms.txt
- File: data/rooms.txt
- Fields:
  1. username (str) - User owner
  2. room_id (int) - Room identifier
  3. room_name (str) - Room name
- Example lines:
  ```
  john_doe|1|Living Room
  john_doe|2|Bedroom
  john_doe|3|Kitchen
  jane_smith|1|Living Room
  ```

### 4. automation_rules.txt
- File: data/automation_rules.txt
- Fields:
  1. username (str) - User owner
  2. rule_id (int) - Rule identifier
  3. rule_name (str) - Name of the rule
  4. trigger_type (str) - Type of trigger (Time, Motion, Temperature)
  5. trigger_value (str) - Trigger value (time string or threshold)
  6. action_device_id (int) - Device ID for action
  7. action_type (str) - Action type (Turn On, Turn Off, Set Brightness, Set Temperature)
  8. action_value (str) - Value associated with action or empty
  9. enabled (str) - true or false (string)
- Example lines:
  ```
  john_doe|1|Morning Lights|Time|07:00|1|Turn On||true
  john_doe|2|Night Mode|Time|22:00|1|Set Brightness|20|true
  jane_smith|1|Motion Alert|Motion|detected|3|Turn On||true
  ```

### 5. energy_logs.txt
- File: data/energy_logs.txt
- Fields:
  1. username (str) - User owner
  2. device_id (int) - Device ID
  3. date (str) - Date in YYYY-MM-DD format
  4. consumption_kwh (float) - Energy consumption in kWh
- Example lines:
  ```
  john_doe|1|2024-11-01|0.5
  john_doe|2|2024-11-01|2.3
  john_doe|1|2024-11-02|0.6
  jane_smith|3|2024-11-01|0.2
  ```

### 6. activity_logs.txt
- File: data/activity_logs.txt
- Fields:
  1. username (str) - User owner
  2. timestamp (str) - Timestamp YYYY-MM-DD HH:MM:SS
  3. device_id (int) - Device ID
  4. action (str) - Action performed
  5. details (str) - Additional details
- Example lines:
  ```
  john_doe|2024-11-01 07:00:00|1|Power On|Automation triggered: Morning Lights
  john_doe|2024-11-01 08:30:00|2|Settings Changed|Temperature set to 72
  jane_smith|2024-11-01 09:15:00|3|Power On|Manual control
  ```

---

# End of SmartHomeManager Design Specification
