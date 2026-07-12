# SmartHomeManager Design Specification

---

## Section 1: Flask Routes Specification

| Endpoint URL                | HTTP Methods | Function Name           | Template Rendered          | Context Variables (Name: Type)                          |
|-----------------------------|--------------|------------------------|----------------------------|--------------------------------------------------------|
| /                           | GET          | root_redirect          | N/A (redirect)             | None                                                   |
| /dashboard                  | GET          | dashboard_page         | dashboard.html             | devices: list, rooms: list, device_counts: dict(str:int) |
| /devices                   | GET          | device_list_page       | devices.html               | devices: list, user: str                                |
| /devices/add               | GET, POST    | add_device_page        | add_device.html            | rooms: list, device_types: list, user: str             |
| /device/<int:device_id>    | GET, POST    | device_control_page    | device_control.html        | device: dict, device_id: int                            |
| /automation                | GET, POST    | automation_rules_page  | automation.html            | rules: list, devices: list, user: str                   |
| /energy                   | GET, POST    | energy_report_page     | energy.html                | energy_data: list, total_consumption: float, total_cost: float, user: str |
| /activity                 | GET, POST    | activity_logs_page     | activity.html              | activities: list, user: str                             |

### Notes:
- Root route `/` redirects to `/dashboard`.
- POST methods are used for adding or updating data (add device, save device control, add automation rule, apply filters/search).
- Dynamic parameter `device_id` is integer.

---

## Section 2: HTML Templates Specification

### 1. Dashboard Page
- Filepath: templates/dashboard.html
- Page Title: Smart Home Dashboard
- Element IDs:
  - dashboard-page: Div container for the dashboard page
  - device-summary: Div showing total devices, active devices, offline devices
  - device-list-button: Button to navigate to /devices
  - add-device-button: Button to navigate to /devices/add
  - automation-button: Button to navigate to /automation
  - energy-button: Button to navigate to /energy
  - activity-button: Button to navigate to /activity
  - room-list: Div listing all rooms with device counts

- Navigation Mappings:
  - device-list-button → url_for('device_list_page')
  - add-device-button → url_for('add_device_page')
  - automation-button → url_for('automation_rules_page')
  - energy-button → url_for('energy_report_page')
  - activity-button → url_for('activity_logs_page')

---

### 2. Device List Page
- Filepath: templates/devices.html
- Page Title: My Devices
- Element IDs:
  - device-list-page: Div container
  - device-table: Table displaying devices
  - control-device-button-{device_id}: Button to control device, pattern example: control-device-button-1
  - back-to-dashboard: Button to navigate back to dashboard

- Navigation Mappings:
  - control-device-button-{device_id} → url_for('device_control_page', device_id=device_id)
  - back-to-dashboard → url_for('dashboard_page')

---

### 3. Add Device Page
- Filepath: templates/add_device.html
- Page Title: Add New Device
- Element IDs:
  - add-device-page: Div container
  - device-name: Input text for device name
  - device-type: Dropdown with options [Light, Thermostat, Camera, Lock, Sensor, Appliance]
  - device-room: Dropdown with options [Living Room, Bedroom, Kitchen, Bathroom, Garage]
  - submit-device-button: Button to submit new device
  - back-to-dashboard: Button to navigate to dashboard

- Navigation Mappings:
  - submit-device-button: submits form POST
  - back-to-dashboard → url_for('dashboard_page')

---

### 4. Device Control Page
- Filepath: templates/device_control.html
- Page Title: Device Control
- Element IDs:
  - device-control-page: Div container
  - device-name-display: H2 showing device name
  - device-status-display: Div showing Online/Offline status
  - power-toggle: Button to toggle power
  - save-settings-button: Button to save device settings
  - back-to-devices: Button to navigate back to device list

- Navigation Mappings:
  - save-settings-button: submits form POST
  - power-toggle: triggers toggle action
  - back-to-devices → url_for('device_list_page')

---

### 5. Automation Rules Page
- Filepath: templates/automation.html
- Page Title: Automation Rules
- Element IDs:
  - automation-page: Div container
  - rules-table: Table displaying automation rules
  - rule-name: Input text for rule name
  - trigger-type: Dropdown [Time, Motion, Temperature]
  - trigger-value: Input text
  - action-device: Dropdown of devices
  - action-type: Dropdown [Turn On, Turn Off, Set Brightness, Set Temperature]
  - add-rule-button: Button to add rule
  - back-to-dashboard: Button to navigate to dashboard

- Navigation Mappings:
  - add-rule-button: submits form POST
  - back-to-dashboard → url_for('dashboard_page')

---

### 6. Energy Report Page
- Filepath: templates/energy.html
- Page Title: Energy Report
- Element IDs:
  - energy-page: Div container
  - energy-summary: Div showing total consumption and cost
  - energy-table: Table with energy data
  - date-filter: Input type date
  - apply-filter-button: Button to apply date filter
  - back-to-dashboard: Button to navigate to dashboard

- Navigation Mappings:
  - apply-filter-button: submits form POST
  - back-to-dashboard → url_for('dashboard_page')

---

### 7. Activity Logs Page
- Filepath: templates/activity.html
- Page Title: Activity Logs
- Element IDs:
  - activity-page: Div container
  - activity-table: Table displaying activity logs
  - search-activity: Input field for search query
  - apply-search-button: Button to apply search
  - back-to-dashboard: Button to navigate to dashboard

- Navigation Mappings:
  - apply-search-button: submits form POST
  - back-to-dashboard → url_for('dashboard_page')

---

## Section 3: Data File Schemas

### 1. users.txt
- Path: data/users.txt
- Format: pipe-delimited, no header
- Fields in order:
  1. username (str): unique user identifier
  2. email (str): user's email address
- Example lines:
  - john_doe|john@example.com
  - jane_smith|jane@example.com

---

### 2. devices.txt
- Path: data/devices.txt
- Format: pipe-delimited, no header
- Fields in order:
  1. username (str): owner username
  2. device_id (int): unique device ID
  3. device_name (str): name of device
  4. device_type (str): type of device (Light, Thermostat, etc.)
  5. room (str): room name
  6. brand (str)
  7. model (str)
  8. status (str): Online or Offline
  9. power (str): on or off
  10. brightness (int or empty): brightness value if applicable
  11. temperature (int or empty): temperature if applicable
  12. mode (str): mode setting (Auto, Manual, etc.)
  13. schedule_time (str): time string if scheduled
- Example lines:
  - john_doe|1|Living Room Light|Light|Living Room|Philips|Hue|Online|on|75|||Auto|
  - john_doe|2|Bedroom Thermostat|Thermostat|Bedroom|Nest|Learning|Online|on||72|Auto|22:00
  - jane_smith|3|Kitchen Camera|Camera|Kitchen|Ring|Indoor|Online|on||||Manual|

---

### 3. rooms.txt
- Path: data/rooms.txt
- Format: pipe-delimited, no header
- Fields in order:
  1. username (str)
  2. room_id (int)
  3. room_name (str)
- Example lines:
  - john_doe|1|Living Room
  - john_doe|2|Bedroom
  - john_doe|3|Kitchen
  - jane_smith|1|Living Room

---

### 4. automation_rules.txt
- Path: data/automation_rules.txt
- Format: pipe-delimited, no header
- Fields in order:
  1. username (str)
  2. rule_id (int)
  3. rule_name (str)
  4. trigger_type (str): Time, Motion, Temperature
  5. trigger_value (str): e.g. 07:00, detected
  6. action_device_id (int): device ID
  7. action_type (str): Turn On, Turn Off, Set Brightness, Set Temperature
  8. action_value (str): optional value, e.g. brightness level
  9. enabled (bool): true or false
- Example lines:
  - john_doe|1|Morning Lights|Time|07:00|1|Turn On||true
  - john_doe|2|Night Mode|Time|22:00|1|Set Brightness|20|true
  - jane_smith|1|Motion Alert|Motion|detected|3|Turn On||true

---

### 5. energy_logs.txt
- Path: data/energy_logs.txt
- Format: pipe-delimited, no header
- Fields in order:
  1. username (str)
  2. device_id (int)
  3. date (YYYY-MM-DD)
  4. consumption_kwh (float)
- Example lines:
  - john_doe|1|2024-11-01|0.5
  - john_doe|2|2024-11-01|2.3
  - john_doe|1|2024-11-02|0.6
  - jane_smith|3|2024-11-01|0.2

---

### 6. activity_logs.txt
- Path: data/activity_logs.txt
- Format: pipe-delimited, no header
- Fields in order:
  1. username (str)
  2. timestamp (YYYY-MM-DD HH:MM:SS)
  3. device_id (int)
  4. action (str)
  5. details (str)
- Example lines:
  - john_doe|2024-11-01 07:00:00|1|Power On|Automation triggered: Morning Lights
  - john_doe|2024-11-01 08:30:00|2|Settings Changed|Temperature set to 72
  - jane_smith|2024-11-01 09:15:00|3|Power On|Manual control

---

End of Design Specification
