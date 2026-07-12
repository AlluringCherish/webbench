# SmartHomeManager Design Specification

---

## 1. Flask Routes Specification

| Endpoint URL                   | HTTP Methods | Function Name           | Template Rendered      | Context Variables and Types                                   |
|-------------------------------|--------------|-------------------------|------------------------|---------------------------------------------------------------|
| `/`                           | GET          | `root`                  | Redirect to `/dashboard`| None                                                         |
| `/dashboard`                  | GET          | `dashboard`             | `dashboard.html`       | `device_summary` (dict), `rooms` (list of dict)              |
| `/devices`                   | GET          | `devices`               | `devices.html`         | `devices` (list of dict)                                     |
| `/device/<int:device_id>`    | GET, POST    | `device_control`        | `device_control.html`  | `device` (dict)                                              |
| `/add_device`                | GET, POST    | `add_device`            | `add_device.html`      | `rooms` (list of dict)                                       |
| `/automation`                | GET          | `automation_rules`      | `automation.html`      | `rules` (list of dict), `devices` (list of dict)            |
| `/energy_report`             | GET, POST    | `energy_report`         | `energy_report.html`   | `energy_summary` (dict), `energy_entries` (list of dict)    |
| `/activity_logs`             | GET          | `activity_logs`         | `activity.html`        | `activity_logs` (list of dict)                               |

---

## 2. HTML Templates Specification

### 2.1 Dashboard Page
- Filepath: `templates/dashboard.html`
- Page Title: Smart Home Dashboard
- UI Elements:
  - ID: `dashboard-page` - Div - Container for the dashboard page.
  - ID: `device-summary` - Div - Summary displaying total, active, and offline devices.
  - ID: `device-list-button` - Button - Navigate to Device List page.
  - ID: `add-device-button` - Button - Navigate to Add Device page.
  - ID: `automation-button` - Button - Navigate to Automation Rules page.
  - ID: `energy-button` - Button - Navigate to Energy Report page.
  - ID: `activity-button` - Button - Navigate to Activity Logs page.
  - ID: `room-list` - Div - List of rooms with device counts.
- Navigation:
  - `device-list-button` -> `url_for('devices')`
  - `add-device-button` -> `url_for('add_device')`
  - `automation-button` -> `url_for('automation_rules')`
  - `energy-button` -> `url_for('energy_report')`
  - `activity-button` -> `url_for('activity_logs')`

### 2.2 Device List Page
- Filepath: `templates/devices.html`
- Page Title: My Devices
- UI Elements:
  - ID: `device-list-page` - Div - Container.
  - ID: `device-table` - Table with columns: Name, Type, Room, Status, Actions.
  - `control-device-button-{device_id}` - Button - Navigate to device control page.
  - ID: `back-to-dashboard` - Button - Navigate to Dashboard.
- Navigation:
  - Control buttons: `url_for('device_control', device_id=device_id)`
  - `back-to-dashboard` -> `url_for('dashboard')`

### 2.3 Add Device Page
- Filepath: `templates/add_device.html`
- Page Title: Add New Device
- UI Elements:
  - ID: `add-device-page` - Div container.
  - ID: `device-name` - Input field for device name.
  - ID: `device-type` - Dropdown for device type.
  - ID: `device-room` - Dropdown for room selection.
  - ID: `submit-device-button` - Button to submit the new device.
  - ID: `back-to-dashboard` - Button to navigate back to Dashboard.
- Navigation:
  - `back-to-dashboard` -> `url_for('dashboard')`

### 2.4 Device Control Page
- Filepath: `templates/device_control.html`
- Page Title: Device Control
- UI Elements:
  - ID: `device-control-page` - Div container.
  - ID: `device-name-display` - H2 displaying device name.
  - ID: `device-status-display` - Div displaying device status (Online/Offline).
  - ID: `power-toggle` - Button to toggle power.
  - ID: `save-settings-button` - Button to save settings.
  - ID: `back-to-devices` - Button to navigate back to devices list.
- Navigation:
  - `back-to-devices` -> `url_for('devices')`

### 2.5 Automation Rules Page
- Filepath: `templates/automation.html`
- Page Title: Automation Rules
- UI Elements:
  - ID: `automation-page` - Div container.
  - ID: `rules-table` - Table displaying automation rules.
  - ID: `rule-name` - Input for rule name.
  - ID: `trigger-type` - Dropdown for trigger type.
  - ID: `trigger-value` - Input for trigger value.
  - ID: `action-device` - Dropdown for target device.
  - ID: `action-type` - Dropdown for action type.
  - ID: `add-rule-button` - Button to add rule.
  - ID: `back-to-dashboard` - Button to dashboard.
- Navigation:
  - `back-to-dashboard` -> `url_for('dashboard')`

### 2.6 Energy Report Page
- Filepath: `templates/energy_report.html`
- Page Title: Energy Report
- UI Elements:
  - ID: `energy-page` - Div container.
  - ID: `energy-summary` - Div showing energy consumption summary.
  - ID: `energy-table` - Table displaying energy consumption per device.
  - ID: `date-filter` - Input date to filter.
  - ID: `apply-filter-button` - Button to apply filter.
  - ID: `back-to-dashboard` - Button to dashboard.
- Navigation:
  - `back-to-dashboard` -> `url_for('dashboard')`

### 2.7 Activity Logs Page
- Filepath: `templates/activity.html`
- Page Title: Activity Logs
- UI Elements:
  - ID: `activity-page` - Div container.
  - ID: `activity-table` - Table listing activity logs.
  - ID: `search-activity` - Input for searching logs.
  - ID: `apply-search-button` - Button to apply search.
  - ID: `back-to-dashboard` - Button to dashboard.
- Navigation:
  - `back-to-dashboard` -> `url_for('dashboard')`

---

## 3. Data File Schemas

### 3.1 users.txt
- Path: `data/users.txt`
- Pipe-delimited fields:
  - `username` (str)
  - `email` (str)
- Example lines:
```
john_doe|john@example.com
jane_smith|jane@example.com
```

### 3.2 devices.txt
- Path: `data/devices.txt`
- Pipe-delimited fields:
  `username|device_id|device_name|device_type|room|brand|model|status|power|brightness|temperature|mode|schedule_time`
- Field Descriptions:
  - `username`: str
  - `device_id`: int
  - `device_name`: str
  - `device_type`: str (e.g., Light, Thermostat, Camera)
  - `room`: str
  - `brand`: str
  - `model`: str
  - `status`: str (Online/Offline)
  - `power`: str (on/off)
  - `brightness`: str or empty
  - `temperature`: str or empty
  - `mode`: str
  - `schedule_time`: str or empty
- Example lines:
```
john_doe|1|Living Room Light|Light|Living Room|Philips|Hue|Online|on|75|||Auto|
john_doe|2|Bedroom Thermostat|Thermostat|Bedroom|Nest|Learning|Online|on||72|Auto|22:00
jane_smith|3|Kitchen Camera|Camera|Kitchen|Ring|Indoor|Online|on||||Manual|
```

### 3.3 rooms.txt
- Path: `data/rooms.txt`
- Pipe-delimited fields:
  - `username` (str)
  - `room_id` (int)
  - `room_name` (str)
- Example lines:
```
john_doe|1|Living Room
john_doe|2|Bedroom
john_doe|3|Kitchen
jane_smith|1|Living Room
```

### 3.4 automation_rules.txt
- Path: `data/automation_rules.txt`
- Pipe-delimited fields:
  `username|rule_id|rule_name|trigger_type|trigger_value|action_device_id|action_type|action_value|enabled`
- Field Descriptions:
  - `username`: str
  - `rule_id`: int
  - `rule_name`: str
  - `trigger_type`: str (Time, Motion, Temperature)
  - `trigger_value`: str
  - `action_device_id`: int
  - `action_type`: str (Turn On, Turn Off, Set Brightness, Set Temperature)
  - `action_value`: str or empty
  - `enabled`: bool (`true` or `false`)
- Example lines:
```
john_doe|1|Morning Lights|Time|07:00|1|Turn On||true
john_doe|2|Night Mode|Time|22:00|1|Set Brightness|20|true
jane_smith|1|Motion Alert|Motion|detected|3|Turn On||true
```

### 3.5 energy_logs.txt
- Path: `data/energy_logs.txt`
- Pipe-delimited fields:
  - `username` (str)
  - `device_id` (int)
  - `date` (str, YYYY-MM-DD)
  - `consumption_kwh` (float)
- Example lines:
```
john_doe|1|2024-11-01|0.5
john_doe|2|2024-11-01|2.3
john_doe|1|2024-11-02|0.6
jane_smith|3|2024-11-01|0.2
```

### 3.6 activity_logs.txt
- Path: `data/activity_logs.txt`
- Pipe-delimited fields:
  - `username` (str)
  - `timestamp` (str, YYYY-MM-DD HH:MM:SS)
  - `device_id` (int)
  - `action` (str)
  - `details` (str)
- Example lines:
```
john_doe|2024-11-01 07:00:00|1|Power On|Automation triggered: Morning Lights
john_doe|2024-11-01 08:30:00|2|Settings Changed|Temperature set to 72
jane_smith|2024-11-01 09:15:00|3|Power On|Manual control
```

---

This design specification supports backend and frontend development for SmartHomeManager ensuring all functional, UI, and data management details are covered.