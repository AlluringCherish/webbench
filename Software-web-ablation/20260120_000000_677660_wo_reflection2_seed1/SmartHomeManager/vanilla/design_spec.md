# SmartHomeManager Design Specification

---

## Section 1: Flask Routes Specification

| Endpoint URL                | HTTP Methods | Function Name           | Template Rendered          | Context Variables (Name: Type)                          |
|-----------------------------|--------------|------------------------|----------------------------|--------------------------------------------------------|
| /
| GET        | root_redirect          | Redirects to '/dashboard' (no template)                   | None                                                   |
| /dashboard                  | GET          | dashboard_page         | dashboard.html             | devices: list of dict, rooms: list of dict, device_summary: dict |
| /devices                    | GET          | device_list_page       | devices.html               | devices: list of dict                                   |
| /device/add                 | GET          | add_device_form        | add_device.html            | device_types: list of str, rooms: list of str           |
| /device/add                 | POST         | add_device_submit      | Redirect to '/devices' (no direct template)            | form data from request                                  |
| /device/<int:device_id>     | GET          | device_control_page    | device_control.html        | device: dict                                          |
| /device/<int:device_id>/control | POST     | control_device_submit  | Redirect to '/devices' or '/device/<device_id>' (no template) | form data from request                                  |
| /automation                 | GET          | automation_rules_page  | automation.html            | automation_rules: list of dict, devices: list of dict    |
| /automation/add             | POST         | add_automation_rule    | Redirect to '/automation' (no template)                 | form data from request                                  |
| /energy                    | GET          | energy_report_page     | energy.html                | energy_logs: list of dict, total_consumption: float, total_cost: float |
| /energy/filter              | POST         | apply_energy_filter    | energy.html                | energy_logs: list of dict filtered by date             |
| /activity                  | GET          | activity_logs_page     | activity.html              | activity_logs: list of dict                              |
| /activity/search            | POST         | search_activity_logs   | activity.html              | activity_logs filtered by search string                 |

---

## Section 2: HTML Templates Specification

### 1. Dashboard Page
- Filepath: templates/dashboard.html
- Page Title: Smart Home Dashboard
- Element IDs:
  - dashboard-page (Div): Container for the dashboard page.
  - device-summary (Div): Summary showing total devices, active devices, and offline devices count.
  - device-list-button (Button): Navigates to device list page.
  - add-device-button (Button): Navigates to add device page.
  - automation-button (Button): Navigates to automation rules page.
  - energy-button (Button): Navigates to energy report page.
  - activity-button (Button): Navigates to activity logs page.
  - room-list (Div): List of all rooms with device counts.
- Navigation mappings:
  - device-list-button: url_for('device_list_page')
  - add-device-button: url_for('add_device_form')
  - automation-button: url_for('automation_rules_page')
  - energy-button: url_for('energy_report_page')
  - activity-button: url_for('activity_logs_page')

### 2. Device List Page
- Filepath: templates/devices.html
- Page Title: My Devices
- Element IDs:
  - device-list-page (Div): Container for device list page.
  - device-table (Table): Displays all devices with columns: name, type, room, status, actions.
  - control-device-button-{device_id} (Button): Navigate to device control page for each device, pattern: control-device-button-{device_id}.
  - back-to-dashboard (Button): Navigates back to dashboard.
- Navigation mappings:
  - control-device-button-{device_id}: url_for('device_control_page', device_id=device_id)
  - back-to-dashboard: url_for('dashboard_page')

### 3. Add Device Page
- Filepath: templates/add_device.html
- Page Title: Add New Device
- Element IDs:
  - add-device-page (Div): Container for add device page.
  - device-name (Input): Input field for device name.
  - device-type (Dropdown): Dropdown to select device type (Light, Thermostat, Camera, Lock, Sensor, Appliance).
  - device-room (Dropdown): Dropdown to select room (Living Room, Bedroom, Kitchen, Bathroom, Garage).
  - submit-device-button (Button): Button to submit new device.
  - back-to-dashboard (Button): Navigate back to dashboard.
- Navigation mappings:
  - back-to-dashboard: url_for('dashboard_page')

### 4. Device Control Page
- Filepath: templates/device_control.html
- Page Title: Device Control
- Element IDs:
  - device-control-page (Div): Container for device control page.
  - device-name-display (H2): Displays device name.
  - device-status-display (Div): Displays current device status (Online/Offline).
  - power-toggle (Button): Button to toggle device power on/off.
  - save-settings-button (Button): Button to save device settings.
  - back-to-devices (Button): Navigate back to device list.
- Navigation mappings:
  - back-to-devices: url_for('device_list_page')

### 5. Automation Rules Page
- Filepath: templates/automation.html
- Page Title: Automation Rules
- Element IDs:
  - automation-page (Div): Container for automation rules page.
  - rules-table (Table): Displays automation rules with name, trigger, action, and status.
  - rule-name (Input): Input field for rule name.
  - trigger-type (Dropdown): Dropdown to select trigger type (Time, Motion, Temperature).
  - trigger-value (Input): Input to enter trigger value.
  - action-device (Dropdown): Dropdown to select target device.
  - action-type (Dropdown): Dropdown to select action type (Turn On, Turn Off, Set Brightness, Set Temperature).
  - add-rule-button (Button): Button to add new automation rule.
  - back-to-dashboard (Button): Navigate back to dashboard.
- Navigation mappings:
  - back-to-dashboard: url_for('dashboard_page')

### 6. Energy Report Page
- Filepath: templates/energy.html
- Page Title: Energy Report
- Element IDs:
  - energy-page (Div): Container for energy report page.
  - energy-summary (Div): Summary showing total energy consumption and cost estimate.
  - energy-table (Table): Displays energy consumption per device with date and kWh.
  - date-filter (Input date): Input to filter energy data by date.
  - apply-filter-button (Button): Button to apply date filter.
  - back-to-dashboard (Button): Navigate back to dashboard.
- Navigation mappings:
  - apply-filter-button: triggers POST to '/energy/filter'
  - back-to-dashboard: url_for('dashboard_page')

### 7. Activity Logs Page
- Filepath: templates/activity.html
- Page Title: Activity Logs
- Element IDs:
  - activity-page (Div): Container for activity logs page.
  - activity-table (Table): Displays activity logs with timestamp, device, action, and details.
  - search-activity (Input): Input field to search activity logs.
  - apply-search-button (Button): Button to apply search filter.
  - back-to-dashboard (Button): Navigate back to dashboard.
- Navigation mappings:
  - apply-search-button: triggers POST to '/activity/search'
  - back-to-dashboard: url_for('dashboard_page')

---

## Section 3: Data File Schemas

### 1. users.txt
- Filepath: data/users.txt
- Pipe-delimited Fields:
  1. username (str): Unique user ID
  2. email (str): User email address
- Examples:
  - john_doe|john@example.com
  - jane_smith|jane@example.com

### 2. devices.txt
- Filepath: data/devices.txt
- Pipe-delimited Fields:
  1. username (str): Owner username
  2. device_id (int): Unique device identifier
  3. device_name (str): Friendly device name
  4. device_type (str): Device category (Light, Thermostat, Camera, Lock, Sensor, Appliance)
  5. room (str): Assigned room name
  6. brand (str): Device brand
  7. model (str): Device model
  8. status (str): Status string e.g., Online, Offline
  9. power (str): Power state, "on" or "off"
  10. brightness (str): Brightness level or empty if not applicable
  11. temperature (str): Temperature setting or empty if not applicable
  12. mode (str): Mode setting e.g., Auto, Manual or empty
  13. schedule_time (str): Scheduled time string or empty
- Examples:
  - john_doe|1|Living Room Light|Light|Living Room|Philips|Hue|Online|on|75|||Auto|
  - john_doe|2|Bedroom Thermostat|Thermostat|Bedroom|Nest|Learning|Online|on||72|Auto|22:00
  - jane_smith|3|Kitchen Camera|Camera|Kitchen|Ring|Indoor|Online|on||||Manual|

### 3. rooms.txt
- Filepath: data/rooms.txt
- Pipe-delimited Fields:
  1. username (str): Owner username
  2. room_id (int): Room identifier
  3. room_name (str): Name of the room
- Examples:
  - john_doe|1|Living Room
  - john_doe|2|Bedroom
  - john_doe|3|Kitchen
  - jane_smith|1|Living Room

### 4. automation_rules.txt
- Filepath: data/automation_rules.txt
- Pipe-delimited Fields:
  1. username (str): Owner username
  2. rule_id (int): Automation rule ID
  3. rule_name (str): Friendly rule name
  4. trigger_type (str): Trigger category (Time, Motion, Temperature)
  5. trigger_value (str): Trigger value (e.g., time string, "detected", threshold)
  6. action_device_id (int): Device ID to act on
  7. action_type (str): Action type (Turn On, Turn Off, Set Brightness, Set Temperature)
  8. action_value (str): Value for action or empty if N/A
  9. enabled (str): "true" or "false" indicating active status
- Examples:
  - john_doe|1|Morning Lights|Time|07:00|1|Turn On||true
  - john_doe|2|Night Mode|Time|22:00|1|Set Brightness|20|true
  - jane_smith|1|Motion Alert|Motion|detected|3|Turn On||true

### 5. energy_logs.txt
- Filepath: data/energy_logs.txt
- Pipe-delimited Fields:
  1. username (str): Owner username
  2. device_id (int): Device identifier
  3. date (str): Date of consumption in YYYY-MM-DD format
  4. consumption_kwh (float): Energy consumed in kWh
- Examples:
  - john_doe|1|2024-11-01|0.5
  - john_doe|2|2024-11-01|2.3
  - john_doe|1|2024-11-02|0.6
  - jane_smith|3|2024-11-01|0.2

### 6. activity_logs.txt
- Filepath: data/activity_logs.txt
- Pipe-delimited Fields:
  1. username (str): Owner username
  2. timestamp (str): Date and time in YYYY-MM-DD HH:MM:SS format
  3. device_id (int): Device identifier
  4. action (str): Action taken (Power On, Settings Changed, etc.)
  5. details (str): Additional details describing the event
- Examples:
  - john_doe|2024-11-01 07:00:00|1|Power On|Automation triggered: Morning Lights
  - john_doe|2024-11-01 08:30:00|2|Settings Changed|Temperature set to 72
  - jane_smith|2024-11-01 09:15:00|3|Power On|Manual control

---

This specification provides a clear and complete blueprint enabling backend and frontend developers to build the 'SmartHomeManager' application independently and consistently based on a single source of truth.