# SmartHomeManager Design Specification

---

## Section 1: Flask Routes Specification

| Endpoint URL                 | HTTP Methods | Function Name             | Template Rendered           | Context Variables Passed (name: type)                                    |
|------------------------------|--------------|---------------------------|-----------------------------|-------------------------------------------------------------------------|
| /                            | GET          | root_redirect             | Redirect to /dashboard       | None                                                                    |
| /dashboard                   | GET          | dashboard_page            | dashboard.html              | devices_summary: dict (total: int, active: int, offline: int), rooms: list of dict (room_name: str, device_count: int) |
| /devices                    | GET          | device_list_page          | devices.html                | devices: list of dict (device_id: int, device_name: str, device_type: str, room: str, status: str)                   |
| /devices/<int:device_id>     | GET          | device_control_page       | device_control.html         | device: dict (device_id: int, device_name: str, status: str, other settings: various)                               |
| /devices/<int:device_id>     | POST         | save_device_settings      | Redirect or device_control.html | form data for device settings                                        |
| /devices/add                 | GET          | add_device_page           | add_device.html             | None                                                                    |
| /devices/add                 | POST         | submit_new_device         | Redirect to /devices         | form data for new device                                                |
| /automation                  | GET          | automation_rules_page     | automation.html             | rules: list of dict (rule_id: int, rule_name: str, trigger_type: str, trigger_value: str, action_device_id: int, action_type: str, enabled: bool), devices: list of dict (device_id: int, device_name: str) |
| /automation/add              | POST         | add_automation_rule       | Redirect or automation.html  | form data for new rule                                                  |
| /energy                     | GET          | energy_report_page        | energy.html                 | energy_summary: dict (total_kwh: float, cost_estimate: float), energy_logs: list of dict (device_id: int, date: str, consumption_kwh: float) |
| /energy/filter              | POST         | apply_energy_filter       | Render energy.html          | filter date: str                                                        |
| /activity                   | GET          | activity_logs_page        | activity.html               | activity_logs: list of dict (timestamp: str, device_id: int, action: str, details: str)                              |
| /activity/search            | POST         | apply_activity_search     | Render activity.html        | search_query: str                                                       |

Notes:
- All POST routes handling form submissions redirect back or render pages as appropriate.
- URL parameters appearing as `<int:device_id>` must be converted to integers.
- Context variable data types are descriptive for templates to access detailed data entities.

---

## Section 2: HTML Templates Specification

### Template: templates/dashboard.html
- Page Title: Smart Home Dashboard
- Element IDs:
  - dashboard-page (Div): Container for dashboard page.
  - device-summary (Div): Shows total devices, active devices, offline devices.
  - device-list-button (Button): Navigates to Device List page.
  - add-device-button (Button): Navigates to Add Device page.
  - automation-button (Button): Navigates to Automation Rules page.
  - energy-button (Button): Navigates to Energy Report page.
  - activity-button (Button): Navigates to Activity Logs page.
  - room-list (Div): Displays list of all rooms with device counts.
- Navigation mappings:
  - device-list-button -> url_for('device_list_page')
  - add-device-button -> url_for('add_device_page')
  - automation-button -> url_for('automation_rules_page')
  - energy-button -> url_for('energy_report_page')
  - activity-button -> url_for('activity_logs_page')

---

### Template: templates/devices.html
- Page Title: My Devices
- Element IDs:
  - device-list-page (Div): Container for devices page.
  - device-table (Table): Displays all devices with name, type, room, status, actions.
  - control-device-button-{device_id} (Button): Button on each device row to control the device. Pattern: control-device-button-\{device_id\}
  - back-to-dashboard (Button): Navigates back to dashboard.
- Navigation mappings:
  - control-device-button-{device_id} -> url_for('device_control_page', device_id=device_id)
  - back-to-dashboard -> url_for('dashboard_page')

---

### Template: templates/add_device.html
- Page Title: Add New Device
- Element IDs:
  - add-device-page (Div): Container for add device page.
  - device-name (Input): Input for device name.
  - device-type (Dropdown): Dropdown for device type selection (Light, Thermostat, Camera, Lock, Sensor, Appliance).
  - device-room (Dropdown): Dropdown for room selection (Living Room, Bedroom, Kitchen, Bathroom, Garage).
  - submit-device-button (Button): Submit form to add device.
  - back-to-dashboard (Button): Navigate back to dashboard.
- Navigation mappings:
  - back-to-dashboard -> url_for('dashboard_page')

---

### Template: templates/device_control.html
- Page Title: Device Control
- Element IDs:
  - device-control-page (Div): Container for device control page.
  - device-name-display (H2): Displays device name.
  - device-status-display (Div): Shows current device status (Online/Offline).
  - power-toggle (Button): Toggle device power on/off.
  - save-settings-button (Button): Save device settings.
  - back-to-devices (Button): Navigate back to device list.
- Navigation mappings:
  - back-to-devices -> url_for('device_list_page')

---

### Template: templates/automation.html
- Page Title: Automation Rules
- Element IDs:
  - automation-page (Div): Container for automation rules page.
  - rules-table (Table): Displays all automation rules with columns: name, trigger, action, status.
  - rule-name (Input): Input field for rule name.
  - trigger-type (Dropdown): Dropdown for trigger type (Time, Motion, Temperature).
  - trigger-value (Input): Input for trigger value.
  - action-device (Dropdown): Dropdown to select target device.
  - action-type (Dropdown): Dropdown for action type (Turn On, Turn Off, Set Brightness, Set Temperature).
  - add-rule-button (Button): Button to submit new automation rule.
  - back-to-dashboard (Button): Navigate back to dashboard.
- Navigation mappings:
  - back-to-dashboard -> url_for('dashboard_page')

---

### Template: templates/energy.html
- Page Title: Energy Report
- Element IDs:
  - energy-page (Div): Container for energy report page.
  - energy-summary (Div): Shows total energy consumption and cost estimate.
  - energy-table (Table): Displays energy consumption per device with date and kWh.
  - date-filter (Input of type date): Filter energy data by date.
  - apply-filter-button (Button): Apply date filter.
  - back-to-dashboard (Button): Navigate back to dashboard.
- Navigation mappings:
  - apply-filter-button -> triggers form submit with date filter
  - back-to-dashboard -> url_for('dashboard_page')

---

### Template: templates/activity.html
- Page Title: Activity Logs
- Element IDs:
  - activity-page (Div): Container for activity logs page.
  - activity-table (Table): Shows activity logs with timestamp, device, action, details.
  - search-activity (Input): Search input for activity logs.
  - apply-search-button (Button): Apply search filter.
  - back-to-dashboard (Button): Navigate back to dashboard.
- Navigation mappings:
  - apply-search-button -> triggers form submit with search query
  - back-to-dashboard -> url_for('dashboard_page')

---

## Section 3: Data File Schemas

### 1. users.txt
- Path: data/users.txt
- Pipe-delimited fields:
  1. username (str) - unique user identifier
  2. email (str) - user email address
- No header line
- Example lines:
  john_doe|john@example.com
  jane_smith|jane@example.com

---

### 2. devices.txt
- Path: data/devices.txt
- Pipe-delimited fields:
  1. username (str) - user who owns the device
  2. device_id (int) - unique device identifier
  3. device_name (str) - name of the device
  4. device_type (str) - type of device (Light, Thermostat, etc.)
  5. room (str) - room name where device is located
  6. brand (str) - brand of the device
  7. model (str) - model name/number
  8. status (str) - Online or Offline
  9. power (str) - on/off status
  10. brightness (int or empty) - brightness level (if applicable)
  11. temperature (int or empty) - temperature setting (if applicable)
  12. mode (str or empty) - mode setting (e.g., Auto, Manual)
  13. schedule_time (str or empty) - scheduled time string
- No header line
- Example lines:
  john_doe|1|Living Room Light|Light|Living Room|Philips|Hue|Online|on|75|||Auto|
  john_doe|2|Bedroom Thermostat|Thermostat|Bedroom|Nest|Learning|Online|on||72|Auto|22:00
  jane_smith|3|Kitchen Camera|Camera|Kitchen|Ring|Indoor|Online|on||||Manual|

---

### 3. rooms.txt
- Path: data/rooms.txt
- Pipe-delimited fields:
  1. username (str) - user who owns the room
  2. room_id (int) - unique room identifier
  3. room_name (str) - name of the room
- No header line
- Example lines:
  john_doe|1|Living Room
  john_doe|2|Bedroom
  john_doe|3|Kitchen
  jane_smith|1|Living Room

---

### 4. automation_rules.txt
- Path: data/automation_rules.txt
- Pipe-delimited fields:
  1. username (str) - rule owner user
  2. rule_id (int) - unique rule identifier
  3. rule_name (str) - name of the rule
  4. trigger_type (str) - type of trigger (Time, Motion, Temperature)
  5. trigger_value (str) - value for the trigger (time string, detected, threshold)
  6. action_device_id (int) - device id the action applies to
  7. action_type (str) - type of action (Turn On, Turn Off, Set Brightness, Set Temperature)
  8. action_value (str or empty) - value associated with action (e.g., brightness level)
  9. enabled (bool) - whether the rule is active (`true` or `false`)
- No header line
- Example lines:
  john_doe|1|Morning Lights|Time|07:00|1|Turn On||true
  john_doe|2|Night Mode|Time|22:00|1|Set Brightness|20|true
  jane_smith|1|Motion Alert|Motion|detected|3|Turn On||true

---

### 5. energy_logs.txt
- Path: data/energy_logs.txt
- Pipe-delimited fields:
  1. username (str) - user owning the device consumption log
  2. device_id (int) - device identifier
  3. date (str) - date in YYYY-MM-DD format
  4. consumption_kwh (float) - energy consumed in kilowatt hours
- No header line
- Example lines:
  john_doe|1|2024-11-01|0.5
  john_doe|2|2024-11-01|2.3
  john_doe|1|2024-11-02|0.6
  jane_smith|3|2024-11-01|0.2

---

### 6. activity_logs.txt
- Path: data/activity_logs.txt
- Pipe-delimited fields:
  1. username (str) - user owning the log
  2. timestamp (str) - timestamp in YYYY-MM-DD HH:MM:SS format
  3. device_id (int) - device identifier
  4. action (str) - action performed
  5. details (str) - additional details about the action
- No header line
- Example lines:
  john_doe|2024-11-01 07:00:00|1|Power On|Automation triggered: Morning Lights
  john_doe|2024-11-01 08:30:00|2|Settings Changed|Temperature set to 72
  jane_smith|2024-11-01 09:15:00|3|Power On|Manual control

---

# End of Design Specification
