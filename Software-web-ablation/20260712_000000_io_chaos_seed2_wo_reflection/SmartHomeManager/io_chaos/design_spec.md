# SmartHomeManager Design Specification

---

## Section 1: Flask Routes Specification

| Endpoint URL              | HTTP Methods | Function Name          | Template Rendered           | Context Variables (type)                      |
|---------------------------|--------------|------------------------|-----------------------------|----------------------------------------------|
| /                         | GET          | root_redirect          | Redirect to /dashboard      | None                                         |
| /dashboard                | GET          | dashboard_page         | dashboard.html              | devices (list of dict), rooms_summary (dict) |
| /devices                  | GET          | device_list_page       | devices.html                | devices (list of dict)                        |
| /devices/<int:device_id>  | GET          | device_control_page    | device_control.html         | device (dict)                                |
| /add-device               | GET          | add_device_page        | add_device.html             | device_types (list of str), rooms (list of str) |
| /add-device               | POST         | submit_new_device      | Redirect to /devices         | Form data processing                         |
| /automation               | GET          | automation_rules_page  | automation.html             | automation_rules (list of dict), devices (list of dict) |
| /automation               | POST         | add_automation_rule    | Redirect to /automation      | Form data processing                         |
| /energy                   | GET          | energy_report_page     | energy_report.html          | energy_logs (list of dict), total_consumption (float), total_cost (float) |
| /energy                   | POST         | apply_energy_date_filter| energy_report.html         | energy_logs (filtered list), total_consumption (float), total_cost (float) |
| /activity                 | GET          | activity_logs_page     | activity_logs.html          | activity_logs (list of dict)                 |
| /activity                 | POST         | apply_activity_search  | activity_logs.html          | activity_logs (filtered list)                |

Notes:
- root_redirect() redirects '/' to '/dashboard'
- Dynamic route /devices/<int:device_id> uses parameter device_id (int)
- POST routes handle form submissions with redirect after processing

---

## Section 2: HTML Templates Specification

### 1. dashboard.html
- Filepath: templates/dashboard.html
- Page Title: "Smart Home Dashboard"
- Element IDs:
  - dashboard-page (Div) - main container for dashboard
  - device-summary (Div) - summary with total devices, active devices, offline devices
  - device-list-button (Button) - navigates to device list page
  - add-device-button (Button) - navigates to add device page
  - automation-button (Button) - navigates to automation rules page
  - energy-button (Button) - navigates to energy report page
  - activity-button (Button) - navigates to activity logs page
  - room-list (Div) - displays all rooms with device counts
- Navigation url_for mappings:
  - device-list-button: url_for('device_list_page')
  - add-device-button: url_for('add_device_page')
  - automation-button: url_for('automation_rules_page')
  - energy-button: url_for('energy_report_page')
  - activity-button: url_for('activity_logs_page')

### 2. devices.html
- Filepath: templates/devices.html
- Page Title: "My Devices"
- Element IDs:
  - device-list-page (Div) - main container
  - device-table (Table) - table listing all devices
  - control-device-button-{device_id} (Button) - button per device to control device (pattern: control-device-button-{device_id} where device_id is int)
  - back-to-dashboard (Button) - button to return to dashboard
- Navigation url_for mappings:
  - control-device-button-{device_id}: url_for('device_control_page', device_id=device_id)
  - back-to-dashboard: url_for('dashboard_page')

### 3. add_device.html
- Filepath: templates/add_device.html
- Page Title: "Add New Device"
- Element IDs:
  - add-device-page (Div) - main container
  - device-name (Input) - field for device name
  - device-type (Dropdown) - device types dropdown (Light, Thermostat, Camera, Lock, Sensor, Appliance)
  - device-room (Dropdown) - room selection dropdown (Living Room, Bedroom, Kitchen, Bathroom, Garage)
  - submit-device-button (Button) - submit new device
  - back-to-dashboard (Button) - back to dashboard
- Navigation url_for mappings:
  - submit-device-button: form submission handled by POST to /add-device
  - back-to-dashboard: url_for('dashboard_page')

### 4. device_control.html
- Filepath: templates/device_control.html
- Page Title: "Device Control"
- Element IDs:
  - device-control-page (Div) - main container
  - device-name-display (H2) - display device name
  - device-status-display (Div) - shows online/offline status
  - power-toggle (Button) - toggle device power on/off
  - save-settings-button (Button) - save device settings
  - back-to-devices (Button) - back to devices list
- Navigation url_for mappings:
  - power-toggle, save-settings-button: handled by form or AJAX POST (not described explicitly)
  - back-to-devices: url_for('device_list_page')

### 5. automation.html
- Filepath: templates/automation.html
- Page Title: "Automation Rules"
- Element IDs:
  - automation-page (Div) - main container
  - rules-table (Table) - list automation rules
  - rule-name (Input) - input for rule name
  - trigger-type (Dropdown) - select trigger type (Time, Motion, Temperature)
  - trigger-value (Input) - input trigger value
  - action-device (Dropdown) - select device for action
  - action-type (Dropdown) - select action type (Turn On, Turn Off, Set Brightness, Set Temperature)
  - add-rule-button (Button) - add new automation rule
  - back-to-dashboard (Button) - back to dashboard
- Navigation url_for mappings:
  - add-rule-button: form submission handled by POST to /automation
  - back-to-dashboard: url_for('dashboard_page')

### 6. energy_report.html
- Filepath: templates/energy_report.html
- Page Title: "Energy Report"
- Element IDs:
  - energy-page (Div) - main container
  - energy-summary (Div) - showing total consumption and cost estimate
  - energy-table (Table) - energy data per device
  - date-filter (Input, type=date) - date filter
  - apply-filter-button (Button) - apply date filter
  - back-to-dashboard (Button) - back to dashboard
- Navigation url_for mappings:
  - apply-filter-button: form POST to /energy
  - back-to-dashboard: url_for('dashboard_page')

### 7. activity_logs.html
- Filepath: templates/activity_logs.html
- Page Title: "Activity Logs"
- Element IDs:
  - activity-page (Div) - main container
  - activity-table (Table) - logs table
  - search-activity (Input) - search input field
  - apply-search-button (Button) - apply search filter
  - back-to-dashboard (Button) - back to dashboard
- Navigation url_for mappings:
  - apply-search-button: form POST to /activity
  - back-to-dashboard: url_for('dashboard_page')

---

## Section 3: Data File Schemas

### 1. data/users.txt
- Pipe-delimited fields (no header):
  1. username (str) - unique user identifier
  2. email (str) - user email address
- Examples:
  john_doe|john@example.com
  jane_smith|jane@example.com

---

### 2. data/devices.txt
- Pipe-delimited fields (no header):
  1. username (str) - owner of device
  2. device_id (int) - unique device identifier
  3. device_name (str)
  4. device_type (str) - e.g., Light, Thermostat
  5. room (str) - room where device is located
  6. brand (str)
  7. model (str)
  8. status (str) - Online or Offline
  9. power (str) - on/off
  10. brightness (str) - number or empty
  11. temperature (str) - number or empty
  12. mode (str) - e.g., Auto, Manual
  13. schedule_time (str) - time string or empty
- Examples:
  john_doe|1|Living Room Light|Light|Living Room|Philips|Hue|Online|on|75|||Auto|
  john_doe|2|Bedroom Thermostat|Thermostat|Bedroom|Nest|Learning|Online|on||72|Auto|22:00
  jane_smith|3|Kitchen Camera|Camera|Kitchen|Ring|Indoor|Online|on||||Manual|

---

### 3. data/rooms.txt
- Pipe-delimited fields (no header):
  1. username (str)
  2. room_id (int)
  3. room_name (str)
- Examples:
  john_doe|1|Living Room
  john_doe|2|Bedroom
  john_doe|3|Kitchen
  jane_smith|1|Living Room

---

### 4. data/automation_rules.txt
- Pipe-delimited fields (no header):
  1. username (str)
  2. rule_id (int)
  3. rule_name (str)
  4. trigger_type (str) - Time, Motion, Temperature
  5. trigger_value (str)
  6. action_device_id (int)
  7. action_type (str) - Turn On, Turn Off, Set Brightness, Set Temperature
  8. action_value (str) - can be empty
  9. enabled (str) - 'true' or 'false'
- Examples:
  john_doe|1|Morning Lights|Time|07:00|1|Turn On||true
  john_doe|2|Night Mode|Time|22:00|1|Set Brightness|20|true
  jane_smith|1|Motion Alert|Motion|detected|3|Turn On||true

---

### 5. data/energy_logs.txt
- Pipe-delimited fields (no header):
  1. username (str)
  2. device_id (int)
  3. date (str) - YYYY-MM-DD
  4. consumption_kwh (float as string)
- Examples:
  john_doe|1|2024-11-01|0.5
  john_doe|2|2024-11-01|2.3
  john_doe|1|2024-11-02|0.6
  jane_smith|3|2024-11-01|0.2

---

### 6. data/activity_logs.txt
- Pipe-delimited fields (no header):
  1. username (str)
  2. timestamp (str) - YYYY-MM-DD HH:MM:SS
  3. device_id (int)
  4. action (str)
  5. details (str)
- Examples:
  john_doe|2024-11-01 07:00:00|1|Power On|Automation triggered: Morning Lights
  john_doe|2024-11-01 08:30:00|2|Settings Changed|Temperature set to 72
  jane_smith|2024-11-01 09:15:00|3|Power On|Manual control


---

**End of Design Specification**
