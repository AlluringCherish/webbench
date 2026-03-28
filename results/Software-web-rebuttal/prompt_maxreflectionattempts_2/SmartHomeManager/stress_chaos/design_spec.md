# SmartHomeManager Design Specification

---

## 1. Flask Routes Specification

| Endpoint URL                  | HTTP Methods | Flask Function Name      | Template File Rendered          | Context Variables (name: type)                             |
|------------------------------|--------------|-------------------------|--------------------------------|-------------------------------------------------------------|
| /                            | GET          | redirect_to_dashboard    | Redirect                       | None                                                        |
| /dashboard                   | GET          | dashboard_page          | dashboard.html                | device_counts: dict, rooms: list[str], user: str             |
| /devices                    | GET          | list_devices            | devices/list.html             | devices: list[dict], user: str                               |
| /devices/add                | GET, POST    | add_device              | devices/add.html              | rooms: list[str], device_types: list[str], user: str        |
| /devices/<int:device_id>    | GET, POST    | control_device          | devices/control.html          | device: dict, user: str                                     |
| /automation                 | GET, POST    | automation_page         | automation.html              | rules: list[dict], devices: list[dict], user: str           |
| /reports                   | GET          | reports_page            | reports.html                 | energy_summary: dict, energy_logs: list[dict], user: str    |
| /activity                  | GET          | activity_page           | activity.html                | activities: list[dict], user: str                           |


---

## 2. HTML Templates Specification

### Dashboard Page
- Filepath: templates/dashboard.html
- Page Title: Smart Home Dashboard
- Element IDs:
  - dashboard-page (Div): Main container
  - device-summary (Div): Summary of total, active, offline devices
  - device-list-button (Button): Navigate to device list page
  - add-device-button (Button): Navigate to add device page
  - automation-button (Button): Navigate to automation rules page
  - energy-button (Button): Navigate to energy report page
  - activity-button (Button): Navigate to activity logs page
  - room-list (Div): List of rooms with counts
- Navigation repointed using url_for:
  - device-list-button: url_for('list_devices')
  - add-device-button: url_for('add_device')
  - automation-button: url_for('automation_page')
  - energy-button: url_for('reports_page')
  - activity-button: url_for('activity_page')

### Device List Page
- Filepath: templates/devices/list.html
- Page Title: My Devices
- Element IDs:
  - device-list-page (Div): Container for devices
  - device-table (Table): Device listing
  - control-device-button-{device_id} (Button): Dynamic button per device row to control device
  - back-to-dashboard (Button): Navigate back to dashboard
- Navigation:
  - control-device-button-{device_id}: url_for('control_device', device_id=device_id)
  - back-to-dashboard: url_for('dashboard_page')

### Add Device Page
- Filepath: templates/devices/add.html
- Page Title: Add New Device
- Element IDs:
  - add-device-page (Div): Main container
  - device-name (Input): Device name input
  - device-type (Dropdown): Device type select
  - device-room (Dropdown): Room select
  - submit-device-button (Button): Submit new device
  - back-to-dashboard (Button): Navigate back to dashboard
- Navigation:
  - back-to-dashboard: url_for('dashboard_page')

### Device Control Page
- Filepath: templates/devices/control.html
- Page Title: Device Control
- Element IDs:
  - device-control-page (Div): Main container
  - device-name-display (H2): Display device name
  - device-status-display (Div): Display device status
  - power-toggle (Button): Toggle power on/off
  - save-settings-button (Button): Save settings
  - back-to-devices (Button): Navigate back to device list
- Navigation:
  - back-to-devices: url_for('list_devices')

### Automation Rules Page
- Filepath: templates/automation.html
- Page Title: Automation Rules
- Element IDs:
  - automation-page (Div): Main container
  - rules-table (Table): Automation rules list
  - rule-name (Input): Rule name input
  - trigger-type (Dropdown): Trigger type select
  - trigger-value (Input): Trigger value
  - action-device (Dropdown): Target device select
  - action-type (Dropdown): Action type select
  - add-rule-button (Button): Add new rule
  - back-to-dashboard (Button): Navigate back to dashboard
- Navigation:
  - back-to-dashboard: url_for('dashboard_page')

### Energy Report Page
- Filepath: templates/reports.html
- Page Title: Energy Report
- Element IDs:
  - energy-page (Div): Main container
  - energy-summary (Div): Summary of consumption
  - energy-table (Table): Energy consumption per device
  - date-filter (Input - date): Filter energy data by date
  - apply-filter-button (Button): Apply date filter
  - back-to-dashboard (Button): Navigate back to dashboard
- Navigation:
  - back-to-dashboard: url_for('dashboard_page')

### Activity Logs Page
- Filepath: templates/activity.html
- Page Title: Activity Logs
- Element IDs:
  - activity-page (Div): Main container
  - activity-table (Table): Activity logs
  - search-activity (Input): Search filter
  - apply-search-button (Button): Apply search
  - back-to-dashboard (Button): Navigate back to dashboard
- Navigation:
  - back-to-dashboard: url_for('dashboard_page')

---

## 3. Data File Schemas

### users.txt
- Path: data/users.txt
- Fields (pipe-delimited): username:str|email:str
- No header line
- Example Lines:
  - john_doe|john@example.com
  - jane_smith|jane@example.com

### devices.txt
- Path: data/devices.txt
- Fields (pipe-delimited): username:str|device_id:int|device_name:str|device_type:str|room:str|brand:str|model:str|status:str|power:str|brightness:int|temperature:int|mode:str|schedule_time:str
- No header line
- Example Lines:
  - john_doe|1|Living Room Light|Light|Living Room|Philips|Hue|Online|on|75|||Auto|
  - john_doe|2|Bedroom Thermostat|Thermostat|Bedroom|Nest|Learning|Online|on||72|Auto|22:00
  - jane_smith|3|Kitchen Camera|Camera|Kitchen|Ring|Indoor|Online|on||||Manual|

### rooms.txt
- Path: data/rooms.txt
- Fields (pipe-delimited): username:str|room_id:int|room_name:str
- No header line
- Example Lines:
  - john_doe|1|Living Room
  - john_doe|2|Bedroom
  - john_doe|3|Kitchen
  - jane_smith|1|Living Room

### automation_rules.txt
- Path: data/automation_rules.txt
- Fields (pipe-delimited): username:str|rule_id:int|rule_name:str|trigger_type:str|trigger_value:str|action_device_id:int|action_type:str|action_value:str|enabled:bool
- No header line
- Example Lines:
  - john_doe|1|Morning Lights|Time|07:00|1|Turn On||true
  - john_doe|2|Night Mode|Time|22:00|1|Set Brightness|20|true
  - jane_smith|1|Motion Alert|Motion|detected|3|Turn On||true

### energy_logs.txt
- Path: data/energy_logs.txt
- Fields (pipe-delimited): username:str|device_id:int|date:str (YYYY-MM-DD)|consumption_kwh:float
- No header line
- Example Lines:
  - john_doe|1|2024-11-01|0.5
  - john_doe|2|2024-11-01|2.3
  - john_doe|1|2024-11-02|0.6
  - jane_smith|3|2024-11-01|0.2

### activity_logs.txt
- Path: data/activity_logs.txt
- Fields (pipe-delimited): username:str|timestamp:str (YYYY-MM-DD HH:MM:SS)|device_id:int|action:str|details:str
- No header line
- Example Lines:
  - john_doe|2024-11-01 07:00:00|1|Power On|Automation triggered: Morning Lights
  - john_doe|2024-11-01 08:30:00|2|Settings Changed|Temperature set to 72
  - jane_smith|2024-11-01 09:15:00|3|Power On|Manual control

---

# End of Design Specification
