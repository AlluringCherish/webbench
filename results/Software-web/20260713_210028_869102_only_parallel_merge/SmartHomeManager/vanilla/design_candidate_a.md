# SmartHomeManager Flask Web Application Design Specification

## Routes and Pages

| Page Name           | Route URL         | Route Function Name          | Page Title           |
|---------------------|-------------------|------------------------------|----------------------|
| Dashboard           | `/`               | dashboard()                  | Smart Home Dashboard |
| Device List         | `/devices`        | device_list()                | My Devices           |
| Add Device          | `/devices/add`    | add_device()                 | Add New Device       |
| Device Control      | `/devices/<int:device_id>` | device_control(device_id) | Device Control       |
| Automation Rules    | `/automation`     | automation_rules()           | Automation Rules     |
| Energy Report       | `/energy`        | energy_report()              | Energy Report        |
| Activity Logs       | `/activity`      | activity_logs()              | Activity Logs        |

---

## Page Elements

### 1. Dashboard Page
- **Page Title**: Smart Home Dashboard
- **Element IDs and Types:**
  - `dashboard-page` (Div) - Container for the dashboard page
  - `device-summary` (Div) - Summary showing total devices, active devices, offline devices count
  - `device-list-button` (Button) - Navigate to Device List page
  - `add-device-button` (Button) - Navigate to Add Device page
  - `automation-button` (Button) - Navigate to Automation Rules page
  - `energy-button` (Button) - Navigate to Energy Report page
  - `activity-button` (Button) - Navigate to Activity Logs page
  - `room-list` (Div) - List of all rooms with device counts

### 2. Device List Page
- **Page Title**: My Devices
- **Element IDs and Types:**
  - `device-list-page` (Div) - Container for device list page
  - `device-table` (Table) - Shows all devices with columns: name, type, room, status, actions
  - `control-device-button-{device_id}` (Button) - Dynamic button per device to navigate to device control page
  - `back-to-dashboard` (Button) - Button to go back to dashboard

### 3. Add Device Page
- **Page Title**: Add New Device
- **Element IDs and Types:**
  - `add-device-page` (Div) - Container for add device page
  - `device-name` (Input) - Input for device name
  - `device-type` (Dropdown) - Select device type (Light, Thermostat, Camera, Lock, Sensor, Appliance)
  - `device-room` (Dropdown) - Select room (Living Room, Bedroom, Kitchen, Bathroom, Garage)
  - `submit-device-button` (Button) - Submit new device
  - `back-to-dashboard` (Button) - Button to return to dashboard

### 4. Device Control Page
- **Page Title**: Device Control
- **Element IDs and Types:**
  - `device-control-page` (Div) - Container for device control page
  - `device-name-display` (H2) - Show device name
  - `device-status-display` (Div) - Show device status (Online/Offline)
  - `power-toggle` (Button) - Toggle device power on/off
  - `save-settings-button` (Button) - Save device settings
  - `back-to-devices` (Button) - Return to device list page

### 5. Automation Rules Page
- **Page Title**: Automation Rules
- **Element IDs and Types:**
  - `automation-page` (Div) - Container for automation rules page
  - `rules-table` (Table) - Displays automation rules with columns: name, trigger, action, status
  - `rule-name` (Input) - Enter new rule name
  - `trigger-type` (Dropdown) - Select trigger type (Time, Motion, Temperature)
  - `trigger-value` (Input) - Enter trigger value (time or threshold)
  - `action-device` (Dropdown) - Select target device
  - `action-type` (Dropdown) - Select action (Turn On, Turn Off, Set Brightness, Set Temperature)
  - `add-rule-button` (Button) - Add new automation rule
  - `back-to-dashboard` (Button) - Return to dashboard

### 6. Energy Report Page
- **Page Title**: Energy Report
- **Element IDs and Types:**
  - `energy-page` (Div) - Container for energy report page
  - `energy-summary` (Div) - Shows total energy consumption and cost
  - `energy-table` (Table) - Display energy consumption per device with date and kWh
  - `date-filter` (Input date) - Filter energy data by date
  - `apply-filter-button` (Button) - Apply date filter
  - `back-to-dashboard` (Button) - Return to dashboard

### 7. Activity Logs Page
- **Page Title**: Activity Logs
- **Element IDs and Types:**
  - `activity-page` (Div) - Container for activity logs page
  - `activity-table` (Table) - Shows activity logs with timestamp, device, action, details
  - `search-activity` (Input) - Search activity logs
  - `apply-search-button` (Button) - Apply search filter
  - `back-to-dashboard` (Button) - Return to dashboard

---

## Navigation Mapping

| From Page             | Element ID               | Target Route Function   |
|-----------------------|--------------------------|------------------------|
| Dashboard             | `device-list-button`     | device_list()          |
| Dashboard             | `add-device-button`      | add_device()           |
| Dashboard             | `automation-button`      | automation_rules()     |
| Dashboard             | `energy-button`          | energy_report()        |
| Dashboard             | `activity-button`        | activity_logs()        |
| Device List           | `back-to-dashboard`      | dashboard()            |
| Device List (per device) | `control-device-button-{device_id}` | device_control(device_id) |
| Add Device            | `back-to-dashboard`      | dashboard()            |
| Device Control        | `back-to-devices`        | device_list()          |
| Automation Rules      | `back-to-dashboard`      | dashboard()            |
| Energy Report         | `back-to-dashboard`      | dashboard()            |
| Activity Logs         | `back-to-dashboard`      | dashboard()            |

---

## Data Fixtures

All data files are stored in the `data` directory.

### 1. users.txt
- **Path:** data/users.txt
- **Fields (pipe-delimited):** username|email
- **Example Data:**
  ```
  john_doe|john@example.com
  jane_smith|jane@example.com
  ```

### 2. devices.txt
- **Path:** data/devices.txt
- **Fields:**
  username|device_id|device_name|device_type|room|brand|model|status|power|brightness|temperature|mode|schedule_time
- **Example Data:**
  ```
  john_doe|1|Living Room Light|Light|Living Room|Philips|Hue|Online|on|75|||Auto|
  john_doe|2|Bedroom Thermostat|Thermostat|Bedroom|Nest|Learning|Online|on||72|Auto|22:00
  jane_smith|3|Kitchen Camera|Camera|Kitchen|Ring|Indoor|Online|on||||Manual|
  ```

### 3. rooms.txt
- **Path:** data/rooms.txt
- **Fields:** username|room_id|room_name
- **Example Data:**
  ```
  john_doe|1|Living Room
  john_doe|2|Bedroom
  john_doe|3|Kitchen
  jane_smith|1|Living Room
  ```

### 4. automation_rules.txt
- **Path:** data/automation_rules.txt
- **Fields:**
  username|rule_id|rule_name|trigger_type|trigger_value|action_device_id|action_type|action_value|enabled
- **Example Data:**
  ```
  john_doe|1|Morning Lights|Time|07:00|1|Turn On||true
  john_doe|2|Night Mode|Time|22:00|1|Set Brightness|20|true
  jane_smith|1|Motion Alert|Motion|detected|3|Turn On||true
  ```

### 5. energy_logs.txt
- **Path:** data/energy_logs.txt
- **Fields:** username|device_id|date|consumption_kwh
- **Example Data:**
  ```
  john_doe|1|2024-11-01|0.5
  john_doe|2|2024-11-01|2.3
  john_doe|1|2024-11-02|0.6
  jane_smith|3|2024-11-01|0.2
  ```

### 6. activity_logs.txt
- **Path:** data/activity_logs.txt
- **Fields:** username|timestamp|device_id|action|details
- **Example Data:**
  ```
  john_doe|2024-11-01 07:00:00|1|Power On|Automation triggered: Morning Lights
  john_doe|2024-11-01 08:30:00|2|Settings Changed|Temperature set to 72
  jane_smith|2024-11-01 09:15:00|3|Power On|Manual control
  ```

---

This completes the design specification document for the 'SmartHomeManager' Flask web application covering all routes, page structures, navigation, and data fixture formats.