# SmartHomeManager Design Specification

---

## Section 1: Flask Routes Specification

| Endpoint                       | HTTP Methods | Function Name             | Template Rendered           | Context Variables                                |
|-------------------------------|--------------|---------------------------|----------------------------|-------------------------------------------------|
| `/`                           | GET          | root                      | Redirects to `/dashboard`  | None                                            |
| `/dashboard`                  | GET          | dashboard_page            | dashboard.html             | devices_summary: dict (total:int, active:int, offline:int), rooms_summary: list of dict(room_name:str, device_count:int) |
| `/devices`                   | GET          | device_list_page          | devices.html               | devices: list of dict(device_id:int, name:str, type:str, room:str, status:str) |
| `/device/add`                | GET          | add_device_page           | add_device.html            | device_types: list of str, rooms: list of str                       |
| `/device/add`                | POST         | submit_add_device         | Redirects to `/devices`    | Form data: device_name (str), device_type (str), device_room (str)  |
| `/device/<int:device_id>`   | GET          | device_control_page       | device_control.html        | device: dict with device detail fields          |
| `/device/<int:device_id>/control` | POST   | post_device_control       | Redirects to `/devices` or `/device/<device_id>` | Form data for device control settings            |
| `/automation`                | GET          | automation_rules_page     | automation.html            | rules: list of dict with rule details, devices: list of dict for dropdown |
| `/automation`                | POST         | add_automation_rule       | Redirects to `/automation` | Form data for new automation rule                |
| `/energy`                   | GET          | energy_report_page        | energy_report.html         | energy_summary: dict(total_kwh: float, cost_estimate: float), energy_data: list of dict(date:str, device_id:int, device_name:str, consumption_kwh: float) |
| `/energy/filter`            | POST         | apply_energy_filter       | Redirects to `/energy`     | Form data: date filter (str)                     |
| `/activity`                 | GET          | activity_logs_page        | activity_logs.html         | activity_logs: list of dict(timestamp:str, device_id:int, device_name:str, action:str, details:str) |
| `/activity/search`          | POST         | search_activity_logs      | Redirects to `/activity`   | Form data: search query (str)                    |


**Details:**
- Root route `/` redirects to `/dashboard`.
- For device control routes, device_id is an integer parameter.
- POST routes handle form submissions.

---

## Section 2: HTML Templates Specification

### 1. Dashboard Page
- Filepath: `templates/dashboard.html`
- Page Title: Smart Home Dashboard
- Element IDs:
  - `dashboard-page`: Div container for dashboard page
  - `device-summary`: Div showing total, active, and offline devices counts
  - `device-list-button`: Button to go to Device List page
  - `add-device-button`: Button to go to Add Device page
  - `automation-button`: Button to go to Automation Rules page
  - `energy-button`: Button to go to Energy Report page
  - `activity-button`: Button to go to Activity Logs page
  - `room-list`: Div showing list of rooms with device counts
- Navigation (all using `url_for`):
  - `device-list-button`: url_for('device_list_page')
  - `add-device-button`: url_for('add_device_page')
  - `automation-button`: url_for('automation_rules_page')
  - `energy-button`: url_for('energy_report_page')
  - `activity-button`: url_for('activity_logs_page')

### 2. Device List Page
- Filepath: `templates/devices.html`
- Page Title: My Devices
- Element IDs:
  - `device-list-page`: Div container
  - `device-table`: Table displaying devices
  - `control-device-button-{device_id}`: Button in each row with pattern `control-device-button-{device_id}` for device control. (Example: `control-device-button-1`)
  - `back-to-dashboard`: Button to go to Dashboard
- Navigation:
  - Each `control-device-button-{device_id}`: url_for('device_control_page', device_id=device_id)
  - `back-to-dashboard`: url_for('dashboard_page')

### 3. Add Device Page
- Filepath: `templates/add_device.html`
- Page Title: Add New Device
- Element IDs:
  - `add-device-page`: Div container
  - `device-name`: Input field for device name
  - `device-type`: Dropdown for device type selection
  - `device-room`: Dropdown for room selection
  - `submit-device-button`: Button to submit form
  - `back-to-dashboard`: Button to go to Dashboard
- Navigation:
  - `back-to-dashboard`: url_for('dashboard_page')

### 4. Device Control Page
- Filepath: `templates/device_control.html`
- Page Title: Device Control
- Element IDs:
  - `device-control-page`: Div container
  - `device-name-display`: H2 element for device name
  - `device-status-display`: Div displaying device status
  - `power-toggle`: Button to toggle power on/off
  - `save-settings-button`: Button to save settings
  - `back-to-devices`: Button to return to device list
- Navigation:
  - `back-to-devices`: url_for('device_list_page')

### 5. Automation Rules Page
- Filepath: `templates/automation.html`
- Page Title: Automation Rules
- Element IDs:
  - `automation-page`: Div container
  - `rules-table`: Table showing automation rules
  - `rule-name`: Input field for rule name
  - `trigger-type`: Dropdown for trigger type
  - `trigger-value`: Input field for trigger value
  - `action-device`: Dropdown for selecting device
  - `action-type`: Dropdown for action type
  - `add-rule-button`: Button to add new rule
  - `back-to-dashboard`: Button to go to Dashboard
- Navigation:
  - `back-to-dashboard`: url_for('dashboard_page')

### 6. Energy Report Page
- Filepath: `templates/energy_report.html`
- Page Title: Energy Report
- Element IDs:
  - `energy-page`: Div container
  - `energy-summary`: Div showing total energy consumption and cost
  - `energy-table`: Table with energy consumption per device
  - `date-filter`: Date input for filtering
  - `apply-filter-button`: Button to apply filter
  - `back-to-dashboard`: Button to go to Dashboard
- Navigation:
  - `back-to-dashboard`: url_for('dashboard_page')

### 7. Activity Logs Page
- Filepath: `templates/activity_logs.html`
- Page Title: Activity Logs
- Element IDs:
  - `activity-page`: Div container
  - `activity-table`: Table showing activity logs
  - `search-activity`: Input text for searching logs
  - `apply-search-button`: Button to apply search
  - `back-to-dashboard`: Button to go to Dashboard
- Navigation:
  - `back-to-dashboard`: url_for('dashboard_page')

---

## Section 3: Data File Schemas

### 1. users.txt
- Filepath: `data/users.txt`
- Fields (pipe-delimited):
  1. username (str)
  2. email (str)
- Description: Stores user account information.
- Examples:
```
john_doe|john@example.com
jane_smith|jane@example.com
```

### 2. devices.txt
- Filepath: `data/devices.txt`
- Fields (pipe-delimited):
  1. username (str)
  2. device_id (int)
  3. device_name (str)
  4. device_type (str) - e.g. Light, Thermostat
  5. room (str)
  6. brand (str)
  7. model (str)
  8. status (str) - Online/Offline
  9. power (str) - on/off
  10. brightness (str) - percentage or empty
  11. temperature (str) - degrees or empty
  12. mode (str) - e.g. Auto, Manual or empty
  13. schedule_time (str) - e.g. 22:00 or empty
- Description: Stores all devices owned by each user with detailed properties.
- Examples:
```
john_doe|1|Living Room Light|Light|Living Room|Philips|Hue|Online|on|75|||Auto|
john_doe|2|Bedroom Thermostat|Thermostat|Bedroom|Nest|Learning|Online|on||72|Auto|22:00
jane_smith|3|Kitchen Camera|Camera|Kitchen|Ring|Indoor|Online|on||||Manual|
```

### 3. rooms.txt
- Filepath: `data/rooms.txt`
- Fields (pipe-delimited):
  1. username (str)
  2. room_id (int)
  3. room_name (str)
- Description: Stores rooms associated with each user.
- Examples:
```
john_doe|1|Living Room
john_doe|2|Bedroom
john_doe|3|Kitchen
jane_smith|1|Living Room
```

### 4. automation_rules.txt
- Filepath: `data/automation_rules.txt`
- Fields (pipe-delimited):
  1. username (str)
  2. rule_id (int)
  3. rule_name (str)
  4. trigger_type (str) - Time, Motion, Temperature
  5. trigger_value (str)
  6. action_device_id (int)
  7. action_type (str) - Turn On, Turn Off, Set Brightness, Set Temperature
  8. action_value (str) - might be empty
  9. enabled (str) - "true" or "false"
- Description: Stores automation rules for users.
- Examples:
```
john_doe|1|Morning Lights|Time|07:00|1|Turn On||true
john_doe|2|Night Mode|Time|22:00|1|Set Brightness|20|true
jane_smith|1|Motion Alert|Motion|detected|3|Turn On||true
```

### 5. energy_logs.txt
- Filepath: `data/energy_logs.txt`
- Fields (pipe-delimited):
  1. username (str)
  2. device_id (int)
  3. date (str) - YYYY-MM-DD
  4. consumption_kwh (float)
- Description: Records energy consumption per device per date.
- Examples:
```
john_doe|1|2024-11-01|0.5
john_doe|2|2024-11-01|2.3
john_doe|1|2024-11-02|0.6
jane_smith|3|2024-11-01|0.2
```

### 6. activity_logs.txt
- Filepath: `data/activity_logs.txt`
- Fields (pipe-delimited):
  1. username (str)
  2. timestamp (str) - YYYY-MM-DD HH:MM:SS
  3. device_id (int)
  4. action (str)
  5. details (str)
- Description: Logs all device activities and system events.
- Examples:
```
john_doe|2024-11-01 07:00:00|1|Power On|Automation triggered: Morning Lights
john_doe|2024-11-01 08:30:00|2|Settings Changed|Temperature set to 72
jane_smith|2024-11-01 09:15:00|3|Power On|Manual control
```

---

This completes the full design specification for the SmartHomeManager web application.