# SmartHomeManager Design Specification

---

## Section 1: Flask Routes Specification

| Endpoint URL                | HTTP Methods | Function Name            | Template Rendered           | Context Variables (Type)                                              |
|-----------------------------|--------------|--------------------------|-----------------------------|----------------------------------------------------------------------|
| `/`                         | GET          | root_redirect             | N/A                         | N/A                                                                  |
| `/dashboard`                | GET          | dashboard                 | dashboard.html              | devices_summary (dict), rooms (list of dicts)                       |
| `/devices`                 | GET          | device_list               | devices.html                | devices (list of dicts)                                              |
| `/device/add`              | GET, POST    | add_device                | add_device.html             | On GET: rooms (list of str), device_types (list of str)
                                                On POST: redirect after submission (no template)
                                                           |
| `/device/<int:device_id>`  | GET, POST   | device_control             | device_control.html         | device (dict)                                                       |
| `/automation`              | GET, POST   | automation_rules           | automation.html             | automation_rules (list of dicts), devices (list of dicts)
                                                On POST: redirect after submission (no template)
                                                           |
| `/energy`                  | GET, POST   | energy_report              | energy.html                 | energy_data (list of dicts), energy_summary (dict), filter_date (str or None)
                                On POST: filtered results by date
                                                    |
| `/activity`                | GET, POST   | activity_logs              | activity.html               | activity_logs (list of dicts), search_query (str or None)
                                                On POST: filtered search results
                                                   |

### Route Descriptions

- `/` : Root route redirects to `/dashboard`.
- `/dashboard` : Displays dashboard with device summary and rooms with device counts.
- `/devices` : Shows list of all user devices with a button for control.
- `/device/add` : GET renders form to add device; POST handles device submission.
- `/device/<int:device_id>` : GET shows device control page; POST saves device settings.
- `/automation` : GET shows automation rules and a form to add; POST adds a new rule.
- `/energy` : GET shows energy report page with optional date filter; POST applies date filter.
- `/activity` : GET shows activity logs; POST applies search filter.

---

## Section 2: HTML Templates Specification

### 1. Dashboard Page
- Filepath: `templates/dashboard.html`
- Page Title: Smart Home Dashboard
- Elements:
  - `dashboard-page` (Div): Container for dashboard page
  - `device-summary` (Div): Displays total devices, active devices, offline devices count
  - `device-list-button` (Button): Navigate to device list page
  - `add-device-button` (Button): Navigate to add device page
  - `automation-button` (Button): Navigate to automation rules page
  - `energy-button` (Button): Navigate to energy report page
  - `activity-button` (Button): Navigate to activity logs page
  - `room-list` (Div): List of rooms with device counts displayed as a dashboard section
- Navigation mappings:
  - `device-list-button` -> url_for('device_list')
  - `add-device-button` -> url_for('add_device')
  - `automation-button` -> url_for('automation_rules')
  - `energy-button` -> url_for('energy_report')
  - `activity-button` -> url_for('activity_logs')

---

### 2. Device List Page
- Filepath: `templates/devices.html`
- Page Title: My Devices
- Elements:
  - `device-list-page` (Div): Container for device list
  - `device-table` (Table): Displays all devices; columns: Name, Type, Room, Status, Actions
  - `control-device-button-{device_id}` (Button): For each device row, navigate to device control page
  - `back-to-dashboard` (Button): Navigate back to dashboard
- Navigation mappings:
  - Each `control-device-button-{device_id}` -> url_for('device_control', device_id=device_id)
  - `back-to-dashboard` -> url_for('dashboard')

---

### 3. Add Device Page
- Filepath: `templates/add_device.html`
- Page Title: Add New Device
- Elements:
  - `add-device-page` (Div): Container for add device page
  - `device-name` (Input): Text input for device name
  - `device-type` (Dropdown): Select dropdown for device type options: Light, Thermostat, Camera, Lock, Sensor, Appliance
  - `device-room` (Dropdown): Select dropdown for rooms: Living Room, Bedroom, Kitchen, Bathroom, Garage
  - `submit-device-button` (Button): Submit new device
  - `back-to-dashboard` (Button): Navigate back to dashboard
- Navigation mappings:
  - `back-to-dashboard` -> url_for('dashboard')

---

### 4. Device Control Page
- Filepath: `templates/device_control.html`
- Page Title: Device Control
- Elements:
  - `device-control-page` (Div): Container for device control page
  - `device-name-display` (H2): Displays device name
  - `device-status-display` (Div): Displays current device status (Online/Offline)
  - `power-toggle` (Button): Toggle power on/off
  - `save-settings-button` (Button): Save device settings
  - `back-to-devices` (Button): Navigate back to device list
- Navigation mappings:
  - `back-to-devices` -> url_for('device_list')

---

### 5. Automation Rules Page
- Filepath: `templates/automation.html`
- Page Title: Automation Rules
- Elements:
  - `automation-page` (Div): Container for automation rules page
  - `rules-table` (Table): Displays automation rules with columns: Name, Trigger, Action, Status
  - `rule-name` (Input): Input for rule name
  - `trigger-type` (Dropdown): Dropdown triggers: Time, Motion, Temperature
  - `trigger-value` (Input): Input field for trigger value (e.g., time or threshold)
  - `action-device` (Dropdown): Dropdown of devices for action
  - `action-type` (Dropdown): Dropdown actions: Turn On, Turn Off, Set Brightness, Set Temperature
  - `add-rule-button` (Button): Add new automation rule
  - `back-to-dashboard` (Button): Navigate back to dashboard
- Navigation mappings:
  - `back-to-dashboard` -> url_for('dashboard')

---

### 6. Energy Report Page
- Filepath: `templates/energy.html`
- Page Title: Energy Report
- Elements:
  - `energy-page` (Div): Container for energy report
  - `energy-summary` (Div): Shows total energy consumption and cost estimate
  - `energy-table` (Table): Displays energy consumption per device with date and kWh
  - `date-filter` (Input date): Filter energy data by date
  - `apply-filter-button` (Button): Apply date filter
  - `back-to-dashboard` (Button): Navigate back to dashboard
- Navigation mappings:
  - `apply-filter-button` -> triggers POST on `/energy` with date filter
  - `back-to-dashboard` -> url_for('dashboard')

---

### 7. Activity Logs Page
- Filepath: `templates/activity.html`
- Page Title: Activity Logs
- Elements:
  - `activity-page` (Div): Container for activity logs page
  - `activity-table` (Table): Displays activity logs with columns: Timestamp, Device, Action, Details
  - `search-activity` (Input): Text input to search activity
  - `apply-search-button` (Button): Apply search filter
  - `back-to-dashboard` (Button): Navigate back to dashboard
- Navigation mappings:
  - `apply-search-button` -> triggers POST on `/activity` with search query
  - `back-to-dashboard` -> url_for('dashboard')

---

## Section 3: Data File Schemas

### 1. users.txt
- Path: `data/users.txt`
- Fields (pipe-delimited, no header):
  1. username (str) - unique user identifier
  2. email (str) - user email address
- Example lines:
  - `john_doe|john@example.com`
  - `jane_smith|jane@example.com`

---

### 2. devices.txt
- Path: `data/devices.txt`
- Fields (pipe-delimited, no header):
  1. username (str) - owner username
  2. device_id (int) - unique id per device
  3. device_name (str) - device display name
  4. device_type (str) - e.g. Light, Thermostat, etc.
  5. room (str) - room name
  6. brand (str)
  7. model (str)
  8. status (str) - Online or Offline
  9. power (str) - on/off
  10. brightness (int or empty) - brightness level
  11. temperature (int or empty) - temperature setting
  12. mode (str or empty) - e.g. Auto, Manual
  13. schedule_time (str or empty) - e.g. "22:00"
- Example lines:
  - `john_doe|1|Living Room Light|Light|Living Room|Philips|Hue|Online|on|75|||Auto|`
  - `john_doe|2|Bedroom Thermostat|Thermostat|Bedroom|Nest|Learning|Online|on||72|Auto|22:00`
  - `jane_smith|3|Kitchen Camera|Camera|Kitchen|Ring|Indoor|Online|on||||Manual|`

---

### 3. rooms.txt
- Path: `data/rooms.txt`
- Fields (pipe-delimited, no header):
  1. username (str)
  2. room_id (int)
  3. room_name (str)
- Example lines:
  - `john_doe|1|Living Room`
  - `john_doe|2|Bedroom`
  - `john_doe|3|Kitchen`
  - `jane_smith|1|Living Room`

---

### 4. automation_rules.txt
- Path: `data/automation_rules.txt`
- Fields (pipe-delimited, no header):
  1. username (str)
  2. rule_id (int)
  3. rule_name (str)
  4. trigger_type (str) - e.g. Time, Motion, Temperature
  5. trigger_value (str) - e.g. 07:00, detected, threshold value
  6. action_device_id (int)
  7. action_type (str) - Turn On, Turn Off, Set Brightness, Set Temperature
  8. action_value (str, can be empty)
  9. enabled (bool) - true or false
- Example lines:
  - `john_doe|1|Morning Lights|Time|07:00|1|Turn On||true`
  - `john_doe|2|Night Mode|Time|22:00|1|Set Brightness|20|true`
  - `jane_smith|1|Motion Alert|Motion|detected|3|Turn On||true`

---

### 5. energy_logs.txt
- Path: `data/energy_logs.txt`
- Fields (pipe-delimited, no header):
  1. username (str)
  2. device_id (int)
  3. date (str) - format YYYY-MM-DD
  4. consumption_kwh (float)
- Example lines:
  - `john_doe|1|2024-11-01|0.5`
  - `john_doe|2|2024-11-01|2.3`
  - `john_doe|1|2024-11-02|0.6`
  - `jane_smith|3|2024-11-01|0.2`

---

### 6. activity_logs.txt
- Path: `data/activity_logs.txt`
- Fields (pipe-delimited, no header):
  1. username (str)
  2. timestamp (str) - format YYYY-MM-DD HH:MM:SS
  3. device_id (int)
  4. action (str) - e.g., Power On, Settings Changed
  5. details (str) - textual details of the event
- Example lines:
  - `john_doe|2024-11-01 07:00:00|1|Power On|Automation triggered: Morning Lights`
  - `john_doe|2024-11-01 08:30:00|2|Settings Changed|Temperature set to 72`
  - `jane_smith|2024-11-01 09:15:00|3|Power On|Manual control`

---

# End of Design Specification
