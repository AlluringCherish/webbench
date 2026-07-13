# SmartHomeManager Flask Application Design Specification

## Section 1: Page and Navigation Design

1. **Dashboard Page**
   - Route: `/dashboard`
   - Title: Smart Home Dashboard
   - Container Div ID: `dashboard-page`
   - Elements:
     - `device-summary` (Div) - shows total devices, active devices, offline devices count
     - Buttons for navigation:
       - `device-list-button` - navigates to `/devices`
       - `add-device-button` - navigates to `/add-device`
       - `automation-button` - navigates to `/automation`
       - `energy-button` - navigates to `/energy`
       - `activity-button` - navigates to `/activity`
     - `room-list` (Div) - list of all rooms with device counts

2. **Device List Page**
   - Route: `/devices`
   - Title: My Devices
   - Container Div ID: `device-list-page`
   - Elements:
     - `device-table` (Table) - listing all devices with columns for name, type, room, status, and actions
     - Per device row button: `control-device-button-{device_id}` (Button) - navigates to `/device-control/{device_id}`
     - `back-to-dashboard` (Button) - navigates back to `/dashboard`

3. **Add Device Page**
   - Route: `/add-device`
   - Title: Add New Device
   - Container Div ID: `add-device-page`
   - Elements:
     - `device-name` (Input) - input for device name
     - `device-type` (Dropdown) - select device type [Light, Thermostat, Camera, Lock, Sensor, Appliance]
     - `device-room` (Dropdown) - select room [Living Room, Bedroom, Kitchen, Bathroom, Garage]
     - `submit-device-button` (Button) - submits the new device
     - `back-to-dashboard` (Button) - navigates back to `/dashboard`

4. **Device Control Page**
   - Route: `/device-control/<device_id>`
   - Title: Device Control
   - Container Div ID: `device-control-page`
   - Elements:
     - `device-name-display` (H2) - displays device name
     - `device-status-display` (Div) - displays online/offline status
     - `power-toggle` (Button) - toggles power status
     - `save-settings-button` (Button) - saves device settings
     - `back-to-devices` (Button) - navigates back to `/devices`

5. **Automation Rules Page**
   - Route: `/automation`
   - Title: Automation Rules
   - Container Div ID: `automation-page`
   - Elements:
     - `rules-table` (Table) - lists automation rules with columns: name, trigger, action, status
     - `rule-name` (Input) - new rule name input
     - `trigger-type` (Dropdown) - trigger type [Time, Motion, Temperature]
     - `trigger-value` (Input) - trigger value (time or threshold)
     - `action-device` (Dropdown) - target device selection
     - `action-type` (Dropdown) - action type [Turn On, Turn Off, Set Brightness, Set Temperature]
     - `add-rule-button` (Button) - adds new automation rule
     - `back-to-dashboard` (Button) - navigates back to `/dashboard`

6. **Energy Report Page**
   - Route: `/energy`
   - Title: Energy Report
   - Container Div ID: `energy-page`
   - Elements:
     - `energy-summary` (Div) - shows total energy consumption and cost estimate
     - `energy-table` (Table) - energy consumption per device with columns: device, date, kWh
     - `date-filter` (Input date) - filter energy data by date
     - `apply-filter-button` (Button) - applies the date filter
     - `back-to-dashboard` (Button) - navigates back to `/dashboard`

7. **Activity Logs Page**
   - Route: `/activity`
   - Title: Activity Logs
   - Container Div ID: `activity-page`
   - Elements:
     - `activity-table` (Table) - activity logs with columns: timestamp, device, action, details
     - `search-activity` (Input) - search filter for activity logs
     - `apply-search-button` (Button) - applies search filter
     - `back-to-dashboard` (Button) - navigates back to `/dashboard`


## Section 2: UI Element ID Specifications

### Dashboard Page
- `dashboard-page` (Div)
- `device-summary` (Div)
- Buttons: `device-list-button`, `add-device-button`, `automation-button`, `energy-button`, `activity-button`
- `room-list` (Div)

### Device List Page
- `device-list-page` (Div)
- `device-table` (Table)
- Buttons per device: `control-device-button-{device_id}` (Button)
- `back-to-dashboard` (Button)

### Add Device Page
- `add-device-page` (Div)
- `device-name` (Input)
- `device-type` (Dropdown)
- `device-room` (Dropdown)
- Buttons: `submit-device-button`, `back-to-dashboard`

### Device Control Page
- `device-control-page` (Div)
- `device-name-display` (H2)
- `device-status-display` (Div)
- Buttons: `power-toggle`, `save-settings-button`, `back-to-devices`

### Automation Rules Page
- `automation-page` (Div)
- `rules-table` (Table)
- Inputs and Dropdowns: `rule-name` (Input), `trigger-type` (Dropdown), `trigger-value` (Input), `action-device` (Dropdown), `action-type` (Dropdown)
- Buttons: `add-rule-button`, `back-to-dashboard`

### Energy Report Page
- `energy-page` (Div)
- `energy-summary` (Div)
- `energy-table` (Table)
- Inputs and Buttons: `date-filter` (Input date), `apply-filter-button`
- `back-to-dashboard` (Button)

### Activity Logs Page
- `activity-page` (Div)
- `activity-table` (Table)
- Inputs and Buttons: `search-activity` (Input), `apply-search-button`, `back-to-dashboard`


## Section 3: Data Storage Contract

- Data folder: `data/`

### User Data
- File: `data/users.txt`
- Format (pipe-delimited): `username|email`
- Example:
  ```
  john_doe|john@example.com
  jane_smith|jane@example.com
  ```

### Device Data
- File: `data/devices.txt`
- Format:
  `username|device_id|device_name|device_type|room|brand|model|status|power|brightness|temperature|mode|schedule_time`
- Example:
  ```
  john_doe|1|Living Room Light|Light|Living Room|Philips|Hue|Online|on|75|||Auto
  john_doe|2|Bedroom Thermostat|Thermostat|Bedroom|Nest|Learning|Online|on||72|Auto|22:00
  jane_smith|3|Kitchen Camera|Camera|Kitchen|Ring|Indoor|Online|on||||Manual
  ```

### Room Data
- File: `data/rooms.txt`
- Format:
  `username|room_id|room_name`
- Example:
  ```
  john_doe|1|Living Room
  john_doe|2|Bedroom
  john_doe|3|Kitchen
  jane_smith|1|Living Room
  ```

### Automation Rules Data
- File: `data/automation_rules.txt`
- Format:
  `username|rule_id|rule_name|trigger_type|trigger_value|action_device_id|action_type|action_value|enabled`
- Example:
  ```
  john_doe|1|Morning Lights|Time|07:00|1|Turn On||true
  john_doe|2|Night Mode|Time|22:00|1|Set Brightness|20|true
  jane_smith|1|Motion Alert|Motion|detected|3|Turn On||true
  ```

### Energy Consumption Logs
- File: `data/energy_logs.txt`
- Format:
  `username|device_id|date|consumption_kwh`
- Example:
  ```
  john_doe|1|2024-11-01|0.5
  john_doe|2|2024-11-01|2.3
  john_doe|1|2024-11-02|0.6
  jane_smith|3|2024-11-01|0.2
  ```

### Activity Logs
- File: `data/activity_logs.txt`
- Format:
  `username|timestamp|device_id|action|details`
- Example:
  ```
  john_doe|2024-11-01 07:00:00|1|Power On|Automation triggered: Morning Lights
  john_doe|2024-11-01 08:30:00|2|Settings Changed|Temperature set to 72
  jane_smith|2024-11-01 09:15:00|3|Power On|Manual control
  ```

---

This design specification is complete and aligned with the user requirements and data management protocols for the SmartHomeManager Flask web application.
