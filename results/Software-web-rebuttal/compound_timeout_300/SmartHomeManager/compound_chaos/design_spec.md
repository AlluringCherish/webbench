# SmartHomeManager Design Specification

---

## Section 1: Flask Routes Specification

| Endpoint                  | HTTP Method | Function Name          | Rendered Template               | Context Variables (Name: Type)                                                     |
|---------------------------|-------------|------------------------|--------------------------------|-----------------------------------------------------------------------------------|
| /** (root)                | GET         | root_redirect          | redirect to dashboard           | None                                                                              |
| /dashboard                | GET         | dashboard              | dashboard.html                 | devices_summary: dict (total: int, active: int, offline: int)
  rooms_summary: list of dict {room_name: str, device_count: int}            |
| /devices                  | GET         | device_list            | device_list.html               | devices: list of dict {device_id: int, device_name: str, device_type: str, room: str, status: str}                      |
| /device/<int:device_id>   | GET         | device_control         | device_control.html            | device: dict {device_id: int, device_name: str, status: str, power: str, brightness: (int or None), temperature: (int or None), mode: str} |
| /device/<int:device_id>/control | POST        | device_control_post    | redirect to /device/<device_id> or error page | updated device data from form (handled internally)                             |
| /add_device               | GET         | add_device             | add_device.html                | rooms: list of str (room names)
  device_types: list of str (Light, Thermostat, Camera, Lock, Sensor, Appliance)                      |
| /add_device               | POST        | add_device_post        | redirect to /devices or error page | new device data from form (handled internally)                                |
| /automation               | GET         | automation_rules       | automation.html                | rules: list of dict {rule_id: int, rule_name: str, trigger_type: str, trigger_value: str, action_device_id: int, action_type: str, enabled: bool}
  devices: list of dict {device_id: int, device_name: str}                      |
| /automation               | POST        | add_automation_rule    | redirect to /automation or error page | new automation rule data from form (handled internally)                      |
| /energy                   | GET         | energy_report          | energy_report.html             | energy_summary: dict (total_kwh: float, estimated_cost: float)
  energy_logs: list of dict {device_id: int, device_name: str, date: str, consumption_kwh: float}
  filter_date: str or None                                                   |
| /energy/filter            | POST        | energy_filter_post     | redirect to /energy or error page | filter_date: str (parsed from form)                                          |
| /activity                 | GET         | activity_logs          | activity_logs.html             | activities: list of dict {timestamp: str, device_id: int, device_name: str, action: str, details: str}
  search_text: str or None                                                    |
| /activity/search          | POST        | activity_search_post   | redirect to /activity or error page | search_text: str (from form)                                                  |

---

## Section 2: HTML Templates Specification

### 1. templates/dashboard.html
- Page Title: Smart Home Dashboard
- Element IDs:
  - dashboard-page: Div - Main container for dashboard page
  - device-summary: Div - Summary display (total devices, active, offline counts)
  - device-list-button: Button - Navigate to Device List (url_for('device_list'))
  - add-device-button: Button - Navigate to Add Device (url_for('add_device'))
  - automation-button: Button - Navigate to Automation Rules (url_for('automation_rules'))
  - energy-button: Button - Navigate to Energy Report (url_for('energy_report'))
  - activity-button: Button - Navigate to Activity Logs (url_for('activity_logs'))
  - room-list: Div - List of rooms with device counts

### 2. templates/device_list.html
- Page Title: My Devices
- Element IDs:
  - device-list-page: Div - Main container
  - device-table: Table - Showing all devices with columns name, type, room, status, actions
  - control-device-button-{device_id}: Button - Navigate to Device Control (url_for('device_control', device_id=device_id))
  - back-to-dashboard: Button - Navigate back to Dashboard (url_for('dashboard'))

### 3. templates/add_device.html
- Page Title: Add New Device
- Element IDs:
  - add-device-page: Div - Main container
  - device-name: Input - Text input for device name
  - device-type: Dropdown - Select device type ['Light', 'Thermostat', 'Camera', 'Lock', 'Sensor', 'Appliance']
  - device-room: Dropdown - Select room ['Living Room', 'Bedroom', 'Kitchen', 'Bathroom', 'Garage']
  - submit-device-button: Button - Submits form
  - back-to-dashboard: Button - Navigate back to Dashboard (url_for('dashboard'))

### 4. templates/device_control.html
- Page Title: Device Control
- Element IDs:
  - device-control-page: Div - Main container
  - device-name-display: H2 - Displays device name
  - device-status-display: Div - Displays device status (Online/Offline)
  - power-toggle: Button - Toggle device power on/off
  - save-settings-button: Button - Save current settings
  - back-to-devices: Button - Navigate back to Device List (url_for('device_list'))

### 5. templates/automation.html
- Page Title: Automation Rules
- Element IDs:
  - automation-page: Div - Main container
  - rules-table: Table - List all automation rules (name, trigger, action, status)
  - rule-name: Input - Input for rule name
  - trigger-type: Dropdown - Trigger type ['Time', 'Motion', 'Temperature']
  - trigger-value: Input - Text input for trigger value
  - action-device: Dropdown - Select device for action
  - action-type: Dropdown - Action type ['Turn On', 'Turn Off', 'Set Brightness', 'Set Temperature']
  - add-rule-button: Button - Add automation rule
  - back-to-dashboard: Button - Navigate back to Dashboard (url_for('dashboard'))

### 6. templates/energy_report.html
- Page Title: Energy Report
- Element IDs:
  - energy-page: Div - Main container
  - energy-summary: Div - Summary of total energy and estimated cost
  - energy-table: Table - Energy consumption details per device with date and kWh
  - date-filter: Input (date) - Filter energy data by date
  - apply-filter-button: Button - Apply date filter
  - back-to-dashboard: Button - Navigate back to Dashboard (url_for('dashboard'))

### 7. templates/activity_logs.html
- Page Title: Activity Logs
- Element IDs:
  - activity-page: Div - Main container
  - activity-table: Table - Activity logs with timestamp, device, action, details
  - search-activity: Input - Search activity logs
  - apply-search-button: Button - Apply search
  - back-to-dashboard: Button - Navigate back to Dashboard (url_for('dashboard'))

---

## Section 3: Data File Schemas

### 1. data/users.txt
- Filename and Path: data/users.txt
- Pipe-Delimited Fields (no header):
  1. username: string
  2. email: string (email format)
- Examples:
  - john_doe|john@example.com
  - jane_smith|jane@example.com
- Strict parsing: No header; fields separated by pipe character; exactly 2 fields per line.

### 2. data/devices.txt
- Filename and Path: data/devices.txt
- Pipe-Delimited Fields (no header):
  1. username: string
  2. device_id: int
  3. device_name: string
  4. device_type: string (one of Light, Thermostat, Camera, Lock, Sensor, Appliance)
  5. room: string (e.g., Living Room, Bedroom, Kitchen...)
  6. brand: string
  7. model: string
  8. status: string (Online, Offline)
  9. power: string (on/off)
  10. brightness: int or empty if not applicable
  11. temperature: int or empty if not applicable
  12. mode: string (Auto, Manual or empty)
  13. schedule_time: string (HH:MM format or empty)
- Examples:
  - john_doe|1|Living Room Light|Light|Living Room|Philips|Hue|Online|on|75|||Auto|
  - john_doe|2|Bedroom Thermostat|Thermostat|Bedroom|Nest|Learning|Online|on||72|Auto|22:00
  - jane_smith|3|Kitchen Camera|Camera|Kitchen|Ring|Indoor|Online|on||||Manual|
- Parsing notes: No header; pipe delimiter; empty fields allowed for non-applicable columns.

### 3. data/rooms.txt
- Filename and Path: data/rooms.txt
- Pipe-Delimited Fields (no header):
  1. username: string
  2. room_id: int
  3. room_name: string
- Examples:
  - john_doe|1|Living Room
  - john_doe|2|Bedroom
  - john_doe|3|Kitchen
  - jane_smith|1|Living Room
- Strict parsing: No header; exactly 3 fields per line; pipe-delimited.

### 4. data/automation_rules.txt
- Filename and Path: data/automation_rules.txt
- Pipe-Delimited Fields (no header):
  1. username: string
  2. rule_id: int
  3. rule_name: string
  4. trigger_type: string (Time, Motion, Temperature)
  5. trigger_value: string (e.g., time '07:00' or motion 'detected', temperature threshold)
  6. action_device_id: int
  7. action_type: string (Turn On, Turn Off, Set Brightness, Set Temperature)
  8. action_value: string (can be empty for actions without value)
  9. enabled: bool (true/false in string form)
- Examples:
  - john_doe|1|Morning Lights|Time|07:00|1|Turn On||true
  - john_doe|2|Night Mode|Time|22:00|1|Set Brightness|20|true
  - jane_smith|1|Motion Alert|Motion|detected|3|Turn On||true
- Parsing notes: No header; pipe-separated; fields strict.

### 5. data/energy_logs.txt
- Filename and Path: data/energy_logs.txt
- Pipe-Delimited Fields (no header):
  1. username: string
  2. device_id: int
  3. date: string (YYYY-MM-DD format)
  4. consumption_kwh: float
- Examples:
  - john_doe|1|2024-11-01|0.5
  - john_doe|2|2024-11-01|2.3
  - john_doe|1|2024-11-02|0.6
  - jane_smith|3|2024-11-01|0.2
- Strict parsing: no header; pipe delimiter; exact fields

### 6. data/activity_logs.txt
- Filename and Path: data/activity_logs.txt
- Pipe-Delimited Fields (no header):
  1. username: string
  2. timestamp: string (YYYY-MM-DD HH:MM:SS format)
  3. device_id: int
  4. action: string
  5. details: string
- Examples:
  - john_doe|2024-11-01 07:00:00|1|Power On|Automation triggered: Morning Lights
  - john_doe|2024-11-01 08:30:00|2|Settings Changed|Temperature set to 72
  - jane_smith|2024-11-01 09:15:00|3|Power On|Manual control
- Parsing notes: no header; pipe-delimited; exact 5 fields per line

---