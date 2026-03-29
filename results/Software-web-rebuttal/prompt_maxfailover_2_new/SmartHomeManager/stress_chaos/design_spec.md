# SmartHomeManager Web Application Design Specification

---

## 1. Flask Routes Specification

| Endpoint URL                  | HTTP Methods | Function Name         | Template Filename           | Context Variables (Name: Type)                                    |
|------------------------------|--------------|-----------------------|-----------------------------|-------------------------------------------------------------------|
| /                            | GET          | redirect_to_dashboard | (redirects to /dashboard)    | None                                                              |
| /dashboard                   | GET          | dashboard             | dashboard.html              | username: str, devices: list of dict                                |
| /devices                     | GET          | device_list           | device_list_page.html       | username: str, devices: list of dict                                |
| /add-device                  | GET, POST    | add_device            | add_device_page.html        | username: str                                                     |
| /device/<int:device_id>      | GET, POST    | device_control        | device_control_page.html    | username: str, device: dict                                        |
| /automation-rules            | GET, POST    | automation_rules      | automation_rules.html       | username: str, rules: list of dict                                 |
| /energy-report               | GET          | energy_report         | energy_report_page.html     | username: str, energy_summary: dict, energy_logs: list of dict     |
| /activity-logs               | GET          | activity_logs         | activity_logs_page.html     | username: str, activities: list of dict, search_filter: str        |

**Notes:**
- The root route `/` redirects to `/dashboard`.
- All pages correspond exactly to those specified in the user requirements.

---

## 2. HTML Templates Specification

### 1. Dashboard Page
- Filepath: templates/dashboard.html
- Page Title: "Smart Home Dashboard"
- HTML Title & H1: "Smart Home Dashboard"
- UI Elements:
  - Div `dashboard-page`: Container for the dashboard.
  - Div `device-summary`: Summary of total, active, and offline devices.
  - Button `device-list-button`: Navigates to device list page (`url_for('device_list')`).
  - Button `add-device-button`: Navigates to add device page (`url_for('add_device')`).
  - Button `automation-button`: Navigates to automation rules page (`url_for('automation_rules')`).
  - Button `energy-button`: Navigates to energy report page (`url_for('energy_report')`).
  - Button `activity-button`: Navigates to activity logs page (`url_for('activity_logs')`).
  - Div `room-list`: Displays list of rooms with device counts.

### 2. Device List Page
- Filepath: templates/device_list_page.html
- Page Title: "My Devices"
- HTML Title & H1: "My Devices"
- UI Elements:
  - Div `device-list-page`: Container for device list.
  - Table `device-table`: Displays devices with columns Name, Type, Room, Status, Actions.
  - Button `control-device-button-{device_id}` (dynamic): Button to navigate to device control page for each device (`url_for('device_control', device_id=device_id)`).
  - Button `back-to-dashboard`: Navigates back to dashboard (`url_for('dashboard')`).

### 3. Add Device Page
- Filepath: templates/add_device_page.html
- Page Title: "Add New Device"
- HTML Title & H1: "Add New Device"
- UI Elements:
  - Div `add-device-page`: Container for adding devices.
  - Input `device-name`: Text input for device name.
  - Dropdown `device-type`: Select device type (Light, Thermostat, Camera, Lock, Sensor, Appliance).
  - Dropdown `device-room`: Select room (Living Room, Bedroom, Kitchen, Bathroom, Garage).
  - Button `submit-device-button`: Submit to add device.
  - Button `back-to-dashboard`: Navigate back to dashboard (`url_for('dashboard')`).

### 4. Device Control Page
- Filepath: templates/device_control_page.html
- Page Title: "Device Control"
- HTML Title & H1: "Device Control"
- UI Elements:
  - Div `device-control-page`: Container.
  - H2 `device-name-display`: Shows device name.
  - Div `device-status-display`: Shows device status (Online/Offline).
  - Button `power-toggle`: Toggles power on/off.
  - Button `save-settings-button`: Save device settings.
  - Button `back-to-devices`: Navigate back to device list (`url_for('device_list')`).

### 5. Automation Rules Page
- Filepath: templates/automation_rules.html
- Page Title: "Automation Rules"
- HTML Title & H1: "Automation Rules"
- UI Elements:
  - Div `automation-page`: Container.
  - Table `rules-table`: Displays rules with Name, Trigger, Action, Status.
  - Input `rule-name`: Input for rule name.
  - Dropdown `trigger-type`: Select trigger type (Time, Motion, Temperature).
  - Input `trigger-value`: Input for trigger value.
  - Dropdown `action-device`: Select device for action.
  - Dropdown `action-type`: Select action type (Turn On, Turn Off, Set Brightness, Set Temperature).
  - Button `add-rule-button`: Add new automation rule.
  - Button `back-to-dashboard`: Navigate back to dashboard (`url_for('dashboard')`).

### 6. Energy Report Page
- Filepath: templates/energy_report_page.html
- Page Title: "Energy Report"
- HTML Title & H1: "Energy Report"
- UI Elements:
  - Div `energy-page`: Container.
  - Div `energy-summary`: Summary data of consumption and cost.
  - Table `energy-table`: Displays energy consumption per device with Date and kWh.
  - Input `date-filter`: Date input to filter energy data.
  - Button `apply-filter-button`: Apply the date filter.
  - Button `back-to-dashboard`: Navigate back to dashboard (`url_for('dashboard')`).

### 7. Activity Logs Page
- Filepath: templates/activity_logs_page.html
- Page Title: "Activity Logs"
- HTML Title & H1: "Activity Logs"
- UI Elements:
  - Div `activity-page`: Container.
  - Table `activity-table`: Displays logs with Timestamp, Device, Action, Details.
  - Input `search-activity`: Text input for searching logs.
  - Button `apply-search-button`: Apply search filter.
  - Button `back-to-dashboard`: Navigate back to dashboard (`url_for('dashboard')`).

---

## 3. Data File Schemas

### 1. users.txt
- Filename: `data/users.txt`
- Fields (pipe "|" delimited): username | email
- Field Descriptions:
  - username: str, user's unique identifier
  - email: str, user's email address
- Examples:
  ```
  john_doe|john@example.com
  jane_smith|jane@example.com
  ```

### 2. devices.txt
- Filename: `data/devices.txt`
- Fields (pipe "|" delimited): 
  username | device_id | device_name | device_type | room | brand | model | status | power | brightness | temperature | mode | schedule_time
- Field Descriptions:
  - username: str, owning user
  - device_id: int, unique device identifier
  - device_name: str, name of device
  - device_type: str, e.g. Light, Thermostat, Camera, Lock, Sensor, Appliance
  - room: str, room name
  - brand: str, manufacturer
  - model: str, model identifier
  - status: str, Online/Offline
  - power: str, on/off
  - brightness: int or empty, brightness level where applicable
  - temperature: int or empty, temperature setting
  - mode: str, mode setting
  - schedule_time: str or empty, format HH:MM
- Examples:
  ```
  john_doe|1|Living Room Light|Light|Living Room|Philips|Hue|Online|on|75|||Auto|
  john_doe|2|Bedroom Thermostat|Thermostat|Bedroom|Nest|Learning|Online|on||72|Auto|22:00
  jane_smith|3|Kitchen Camera|Camera|Kitchen|Ring|Indoor|Online|on||||Manual|
  ```

### 3. rooms.txt
- Filename: `data/rooms.txt`
- Fields (pipe "|" delimited): username | room_id | room_name
- Field Descriptions:
  - username: str, owning user
  - room_id: int, unique room ID
  - room_name: str, e.g. Living Room, Bedroom
- Examples:
  ```
  john_doe|1|Living Room
  john_doe|2|Bedroom
  john_doe|3|Kitchen
  jane_smith|1|Living Room
  ```

### 4. automation_rules.txt
- Filename: `data/automation_rules.txt`
- Fields (pipe "|" delimited):
  username | rule_id | rule_name | trigger_type | trigger_value | action_device_id | action_type | action_value | enabled
- Field Descriptions:
  - username: str, owning user
  - rule_id: int, unique rule ID
  - rule_name: str, rule identifier
  - trigger_type: str, Time/Motion/Temperature
  - trigger_value: str, e.g. time ("07:00") or "detected"
  - action_device_id: int, device to perform action on
  - action_type: str, e.g. Turn On, Turn Off, Set Brightness
  - action_value: str, e.g. brightness level or empty
  - enabled: bool, true/false (stored as string)
- Examples:
  ```
  john_doe|1|Morning Lights|Time|07:00|1|Turn On||true
  john_doe|2|Night Mode|Time|22:00|1|Set Brightness|20|true
  jane_smith|1|Motion Alert|Motion|detected|3|Turn On||true
  ```

### 5. energy_logs.txt
- Filename: `data/energy_logs.txt`
- Fields (pipe "|" delimited): username | device_id | date | consumption_kwh
- Field Descriptions:
  - username: str, owning user
  - device_id: int, device identifier
  - date: str, in ISO format YYYY-MM-DD
  - consumption_kwh: float, kWh consumption
- Examples:
  ```
  john_doe|1|2024-11-01|0.5
  john_doe|2|2024-11-01|2.3
  john_doe|1|2024-11-02|0.6
  jane_smith|3|2024-11-01|0.2
  ```

### 6. activity_logs.txt
- Filename: `data/activity_logs.txt`
- Fields (pipe "|" delimited): username | timestamp | device_id | action | details
- Field Descriptions:
  - username: str, owning user
  - timestamp: str, ISO format: YYYY-MM-DD HH:MM:SS
  - device_id: int, device ID related to activity
  - action: str, description of action (e.g., Power On, Settings Changed)
  - details: str, additional details
- Examples:
  ```
  john_doe|2024-11-01 07:00:00|1|Power On|Automation triggered: Morning Lights
  john_doe|2024-11-01 08:30:00|2|Settings Changed|Temperature set to 72
  jane_smith|2024-11-01 09:15:00|3|Power On|Manual control
  ```

---

This design specification is fully detailed to enable independent development of both backend Flask routes and frontend HTML templates with precise UI element IDs as well as data schemas necessary for direct file handling.