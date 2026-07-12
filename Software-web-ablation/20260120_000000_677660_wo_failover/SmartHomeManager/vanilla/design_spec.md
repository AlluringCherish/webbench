# SmartHomeManager Design Specification

---

## Section 1: Flask Routes Specification

| Endpoint URL                | HTTP Methods | Function Name           | Template Rendered          | Context Variables (Name: Type)                          |
|-----------------------------|--------------|------------------------|----------------------------|--------------------------------------------------------|
| /                           | GET          | root_redirect          | N/A (redirect)             | None                                                   |
| /dashboard                  | GET          | dashboard_page         | dashboard.html             | devices: list, rooms: list, device_counts: dict(str:int) |
| /devices                   | GET          | device_list_page       | devices.html               | devices: list, user: str                                |
| /devices/add               | GET, POST    | add_device_page        | add_device.html            | rooms: list, device_types: list, user: str             |
| /device/<int:device_id>    | GET, POST    | device_control_page    | device_control.html        | device: dict, user: str                                 |
| /automation                | GET, POST    | automation_rules_page  | automation.html            | rules: list, devices: list, user: str                   |
| /energy                   | GET, POST    | energy_report_page     | energy.html                | energy_logs: list, total_consumption: float, total_cost: float, user: str |
| /activity                 | GET, POST    | activity_logs_page     | activity.html              | activities: list, user: str                             |


### Notes:
- Root route `/` redirects to `/dashboard`.
- POST methods allow form submissions (e.g., adding devices, saving settings, filtering).
- Dynamic routes specify `device_id` as int parameter.

---

## Section 2: HTML Templates Specification

### 1. Dashboard Page
- Filepath: templates/dashboard.html
- Page Title: Smart Home Dashboard
- Element IDs:
  - dashboard-page (Div): Container for the dashboard.
  - device-summary (Div): Shows total devices, active devices, offline devices counts.
  - device-list-button (Button): Navigate to Device List page.
  - add-device-button (Button): Navigate to Add Device page.
  - automation-button (Button): Navigate to Automation Rules page.
  - energy-button (Button): Navigate to Energy Report page.
  - activity-button (Button): Navigate to Activity Logs page.
  - room-list (Div): Displays list of rooms with device counts.
- Navigation Mappings:
  - device-list-button: url_for('device_list_page')
  - add-device-button: url_for('add_device_page')
  - automation-button: url_for('automation_rules_page')
  - energy-button: url_for('energy_report_page')
  - activity-button: url_for('activity_logs_page')

### 2. Device List Page
- Filepath: templates/devices.html
- Page Title: My Devices
- Element IDs:
  - device-list-page (Div): Container.
  - device-table (Table): Shows all devices with columns: name, type, room, status, actions.
  - control-device-button-{device_id} (Button): Button on each row to device control page, pattern: 'control-device-button-<device_id>'
  - back-to-dashboard (Button): Navigate to dashboard.
- Navigation Mappings:
  - control-device-button-{device_id}: url_for('device_control_page', device_id=device_id)
  - back-to-dashboard: url_for('dashboard_page')

### 3. Add Device Page
- Filepath: templates/add_device.html
- Page Title: Add New Device
- Element IDs:
  - add-device-page (Div): Container.
  - device-name (Input): Text input for device name.
  - device-type (Dropdown): Options: Light, Thermostat, Camera, Lock, Sensor, Appliance.
  - device-room (Dropdown): Options: Living Room, Bedroom, Kitchen, Bathroom, Garage.
  - submit-device-button (Button): Submit new device.
  - back-to-dashboard (Button): Navigate to dashboard.
- Navigation Mappings:
  - submit-device-button: triggers form POST to add device.
  - back-to-dashboard: url_for('dashboard_page')

### 4. Device Control Page
- Filepath: templates/device_control.html
- Page Title: Device Control
- Element IDs:
  - device-control-page (Div): Container.
  - device-name-display (H2): Displays device name.
  - device-status-display (Div): Shows Online/Offline status.
  - power-toggle (Button): Toggle power on/off.
  - save-settings-button (Button): Save changed settings.
  - back-to-devices (Button): Navigate to device list page.
- Navigation Mappings:
  - power-toggle: triggers POST to toggle power.
  - save-settings-button: triggers POST to save settings.
  - back-to-devices: url_for('device_list_page')

### 5. Automation Rules Page
- Filepath: templates/automation.html
- Page Title: Automation Rules
- Element IDs:
  - automation-page (Div): Container.
  - rules-table (Table): Shows rules with columns: name, trigger, action, status.
  - rule-name (Input): Input for rule name.
  - trigger-type (Dropdown): Options: Time, Motion, Temperature.
  - trigger-value (Input): Text input for trigger value.
  - action-device (Dropdown): List of devices.
  - action-type (Dropdown): Options: Turn On, Turn Off, Set Brightness, Set Temperature.
  - add-rule-button (Button): Add new automation rule.
  - back-to-dashboard (Button): Navigate to dashboard.
- Navigation Mappings:
  - add-rule-button: submit new rule (POST).
  - back-to-dashboard: url_for('dashboard_page')

### 6. Energy Report Page
- Filepath: templates/energy.html
- Page Title: Energy Report
- Element IDs:
  - energy-page (Div): Container.
  - energy-summary (Div): Shows total energy consumption and cost.
  - energy-table (Table): Shows energy per device with date and kWh.
  - date-filter (Input type=date): Date filter field.
  - apply-filter-button (Button): Apply date filter.
  - back-to-dashboard (Button): Navigate to dashboard.
- Navigation Mappings:
  - apply-filter-button: triggers POST to filter energy logs.
  - back-to-dashboard: url_for('dashboard_page')

### 7. Activity Logs Page
- Filepath: templates/activity.html
- Page Title: Activity Logs
- Element IDs:
  - activity-page (Div): Container.
  - activity-table (Table): Shows activity logs with columns: timestamp, device, action, details.
  - search-activity (Input): Search input.
  - apply-search-button (Button): Apply search.
  - back-to-dashboard (Button): Navigate to dashboard.
- Navigation Mappings:
  - apply-search-button: triggers POST to filter/search activity logs.
  - back-to-dashboard: url_for('dashboard_page')


---

## Section 3: Data File Schemas

### 1. users.txt
- Filename/Path: data/users.txt
- Pipe-delimited fields:
  1. username (str) - unique user ID
  2. email (str) - user email address
- Examples:
  john_doe|john@example.com
  jane_smith|jane@example.com

### 2. devices.txt
- Filename/Path: data/devices.txt
- Pipe-delimited fields:
  1. username (str) - owner username
  2. device_id (int) - unique device ID
  3. device_name (str) - name of device
  4. device_type (str) - device category (Light, Thermostat, etc.)
  5. room (str) - associated room name
  6. brand (str) - device brand
  7. model (str) - device model
  8. status (str) - Online or Offline
  9. power (str) - 'on' or 'off' power state
  10. brightness (int) - brightness level if applicable (empty if N/A)
  11. temperature (int) - temperature if applicable (empty if N/A)
  12. mode (str) - mode setting (e.g., Auto, Manual) (empty if N/A)
  13. schedule_time (str) - scheduled time (HH:MM) (empty if N/A)
- Examples:
  john_doe|1|Living Room Light|Light|Living Room|Philips|Hue|Online|on|75|||Auto|
  john_doe|2|Bedroom Thermostat|Thermostat|Bedroom|Nest|Learning|Online|on||72|Auto|22:00
  jane_smith|3|Kitchen Camera|Camera|Kitchen|Ring|Indoor|Online|on||||Manual|

### 3. rooms.txt
- Filename/Path: data/rooms.txt
- Pipe-delimited fields:
  1. username (str) - user owner
  2. room_id (int) - unique room ID
  3. room_name (str) - descriptive room name
- Examples:
  john_doe|1|Living Room
  john_doe|2|Bedroom
  john_doe|3|Kitchen
  jane_smith|1|Living Room

### 4. automation_rules.txt
- Filename/Path: data/automation_rules.txt
- Pipe-delimited fields:
  1. username (str) - owner username
  2. rule_id (int) - unique rule ID
  3. rule_name (str) - name of rule
  4. trigger_type (str) - trigger category (Time, Motion, Temperature)
  5. trigger_value (str) - value for trigger (e.g., time or threshold)
  6. action_device_id (int) - device ID to act on
  7. action_type (str) - action (Turn On, Turn Off, Set Brightness, Set Temperature)
  8. action_value (str) - value for action (empty if N/A)
  9. enabled (bool) - true or false
- Examples:
  john_doe|1|Morning Lights|Time|07:00|1|Turn On||true
  john_doe|2|Night Mode|Time|22:00|1|Set Brightness|20|true
  jane_smith|1|Motion Alert|Motion|detected|3|Turn On||true

### 5. energy_logs.txt
- Filename/Path: data/energy_logs.txt
- Pipe-delimited fields:
  1. username (str) - owner username
  2. device_id (int) - device ID
  3. date (str) - YYYY-MM-DD
  4. consumption_kwh (float) - energy consumed in kWh
- Examples:
  john_doe|1|2024-11-01|0.5
  john_doe|2|2024-11-01|2.3
  john_doe|1|2024-11-02|0.6
  jane_smith|3|2024-11-01|0.2

### 6. activity_logs.txt
- Filename/Path: data/activity_logs.txt
- Pipe-delimited fields:
  1. username (str) - user owner
  2. timestamp (str) - YYYY-MM-DD HH:MM:SS
  3. device_id (int) - device ID
  4. action (str) - action performed
  5. details (str) - additional details
- Examples:
  john_doe|2024-11-01 07:00:00|1|Power On|Automation triggered: Morning Lights
  john_doe|2024-11-01 08:30:00|2|Settings Changed|Temperature set to 72
  jane_smith|2024-11-01 09:15:00|3|Power On|Manual control

---

# End of Design Specification
