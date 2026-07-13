# SmartHomeManager Flask Application Design Specification

---

## Section 1: Page and Navigation Design

### 1. Dashboard Page
- Flask Route Path: `/dashboard`
- Page Title: Smart Home Dashboard
- Container Div ID: `dashboard-page`
- Elements:
  - `device-summary` (Div)
  - Buttons:
    - `device-list-button` (navigates to `/devices`)
    - `add-device-button` (navigates to `/devices/add`)
    - `automation-button` (navigates to `/automation`)
    - `energy-button` (navigates to `/energy`)
    - `activity-button` (navigates to `/activity`)
  - `room-list` (Div)

### 2. Device List Page
- Flask Route Path: `/devices`
- Page Title: My Devices
- Container Div ID: `device-list-page`
- Elements:
  - `device-table` (Table) with columns: Name, Type, Room, Status, Actions
  - For each device row: `control-device-button-{device_id}` (Button) to navigate to `/devices/{device_id}/control`
  - `back-to-dashboard` (Button) navigates to `/dashboard`

### 3. Add Device Page
- Flask Route Path: `/devices/add`
- Page Title: Add New Device
- Container Div ID: `add-device-page`
- Elements:
  - Input: `device-name`
  - Dropdown: `device-type` (Options: Light, Thermostat, Camera, Lock, Sensor, Appliance)
  - Dropdown: `device-room` (Options: Living Room, Bedroom, Kitchen, Bathroom, Garage)
  - Buttons:
    - `submit-device-button` (submit new device)
    - `back-to-dashboard` (navigate to `/dashboard`)

### 4. Device Control Page
- Flask Route Path: `/devices/<device_id>/control`
- Page Title: Device Control
- Container Div ID: `device-control-page`
- Elements:
  - `device-name-display` (H2) shows the device's name
  - `device-status-display` (Div) shows current status (Online/Offline)
  - Button `power-toggle` (toggle power on/off)
  - Button `save-settings-button` (save settings)
  - Button `back-to-devices` (navigate to `/devices`)

### 5. Automation Rules Page
- Flask Route Path: `/automation`
- Page Title: Automation Rules
- Container Div ID: `automation-page`
- Elements:
  - Table `rules-table` with columns: Name, Trigger, Action, Status
  - Input `rule-name`
  - Dropdown `trigger-type` (Time, Motion, Temperature)
  - Input `trigger-value`
  - Dropdown `action-device` (device list)
  - Dropdown `action-type` (Turn On, Turn Off, Set Brightness, Set Temperature)
  - Button `add-rule-button`
  - Button `back-to-dashboard` (navigate to `/dashboard`)

### 6. Energy Report Page
- Flask Route Path: `/energy`
- Page Title: Energy Report
- Container Div ID: `energy-page`
- Elements:
  - `energy-summary` (Div)
  - Table `energy-table` with columns: Device, Date, kWh
  - Date input `date-filter`
  - Button `apply-filter-button`
  - Button `back-to-dashboard` (navigate to `/dashboard`)

### 7. Activity Logs Page
- Flask Route Path: `/activity`
- Page Title: Activity Logs
- Container Div ID: `activity-page`
- Elements:
  - Table `activity-table` with columns: Timestamp, Device, Action, Details
  - Input `search-activity`
  - Button `apply-search-button`
  - Button `back-to-dashboard` (navigate to `/dashboard`)

---

## Section 2: UI Element ID Specifications

| Page                 | Element ID                | Element Type | Notes / Options                                                                 |
|----------------------|---------------------------|--------------|-------------------------------------------------------------------------------|
| Dashboard            | dashboard-page            | Div          | Container div for dashboard page                                              |
|                      | device-summary            | Div          | Summary counts for devices                                                    |
|                      | device-list-button        | Button       | Navigates to device list                                                      |
|                      | add-device-button         | Button       | Navigates to add device page                                                  |
|                      | automation-button         | Button       | Navigates to automation rules page                                            |
|                      | energy-button             | Button       | Navigates to energy report                                                    |
|                      | activity-button           | Button       | Navigates to activity logs                                                    |
|                      | room-list                 | Div          | Lists rooms and device counts                                                 |
| Device List          | device-list-page          | Div          | Container div for device list page                                            |
|                      | device-table              | Table        | Displays all devices                                                          |
|                      | control-device-button-{id}| Button       | Controls device (dynamic per device)                                         |
|                      | back-to-dashboard         | Button       | Back to dashboard                                                            |
| Add Device           | add-device-page           | Div          | Container div                                                                |
|                      | device-name               | Input        | Device name input                                                            |
|                      | device-type               | Dropdown     | Options: Light, Thermostat, Camera, Lock, Sensor, Appliance                  |
|                      | device-room               | Dropdown     | Options: Living Room, Bedroom, Kitchen, Bathroom, Garage                     |
|                      | submit-device-button      | Button       | Submit new device                                                            |
|                      | back-to-dashboard         | Button       | Back to dashboard                                                            |
| Device Control       | device-control-page       | Div          | Container div                                                                |
|                      | device-name-display       | H2           | Displays device name                                                         |
|                      | device-status-display     | Div          | Status display (Online/Offline)                                              |
|                      | power-toggle              | Button       | Toggle power on/off                                                          |
|                      | save-settings-button      | Button       | Save settings                                                                |
|                      | back-to-devices           | Button       | Back to device list                                                          |
| Automation Rules     | automation-page           | Div          | Container div                                                                |
|                      | rules-table               | Table        | Automation rules table                                                       |
|                      | rule-name                 | Input        | Rule name input                                                              |
|                      | trigger-type              | Dropdown     | Trigger types: Time, Motion, Temperature                                     |
|                      | trigger-value             | Input        | Trigger value input                                                          |
|                      | action-device             | Dropdown     | Target devices                                                               |
|                      | action-type               | Dropdown     | Actions: Turn On, Turn Off, Set Brightness, Set Temperature                  |
|                      | add-rule-button           | Button       | Add new automation rule                                                      |
|                      | back-to-dashboard         | Button       | Back to dashboard                                                            |
| Energy Report        | energy-page               | Div          | Container div                                                                |
|                      | energy-summary            | Div          | Energy consumption summary                                                   |
|                      | energy-table              | Table        | Device energy consumption                                                    |
|                      | date-filter               | Input (date) | Date filter input                                                            |
|                      | apply-filter-button       | Button       | Apply date filter                                                            |
|                      | back-to-dashboard         | Button       | Back to dashboard                                                            |
| Activity Logs        | activity-page             | Div          | Container div                                                                |
|                      | activity-table            | Table        | Activity logs                                                                |
|                      | search-activity           | Input        | Search input                                                                 |
|                      | apply-search-button       | Button       | Apply search                                                                 |
|                      | back-to-dashboard         | Button       | Back to dashboard                                                            |

---

## Section 3: Data Storage Contract

All data files are stored in the `data` folder, with pipe (`|`) delimited fields as specified.

### 1. User Data
- File Name: `data/users.txt`
- Format: `username|email`
- Example:
  ```
  john_doe|john@example.com
  jane_smith|jane@example.com
  ```

### 2. Device Data
- File Name: `data/devices.txt`
- Format: `username|device_id|device_name|device_type|room|brand|model|status|power|brightness|temperature|mode|schedule_time`
- Example:
  ```
  john_doe|1|Living Room Light|Light|Living Room|Philips|Hue|Online|on|75|||Auto|
  john_doe|2|Bedroom Thermostat|Thermostat|Bedroom|Nest|Learning|Online|on||72|Auto|22:00
  jane_smith|3|Kitchen Camera|Camera|Kitchen|Ring|Indoor|Online|on||||Manual|
  ```

### 3. Room Data
- File Name: `data/rooms.txt`
- Format: `username|room_id|room_name`
- Example:
  ```
  john_doe|1|Living Room
  john_doe|2|Bedroom
  john_doe|3|Kitchen
  jane_smith|1|Living Room
  ```

### 4. Automation Rules Data
- File Name: `data/automation_rules.txt`
- Format: `username|rule_id|rule_name|trigger_type|trigger_value|action_device_id|action_type|action_value|enabled`
- Example:
  ```
  john_doe|1|Morning Lights|Time|07:00|1|Turn On||true
  john_doe|2|Night Mode|Time|22:00|1|Set Brightness|20|true
  jane_smith|1|Motion Alert|Motion|detected|3|Turn On||true
  ```

### 5. Energy Consumption Logs
- File Name: `data/energy_logs.txt`
- Format: `username|device_id|date|consumption_kwh`
- Example:
  ```
  john_doe|1|2024-11-01|0.5
  john_doe|2|2024-11-01|2.3
  john_doe|1|2024-11-02|0.6
  jane_smith|3|2024-11-01|0.2
  ```

### 6. Activity Logs
- File Name: `data/activity_logs.txt`
- Format: `username|timestamp|device_id|action|details`
- Example:
  ```
  john_doe|2024-11-01 07:00:00|1|Power On|Automation triggered: Morning Lights
  john_doe|2024-11-01 08:30:00|2|Settings Changed|Temperature set to 72
  jane_smith|2024-11-01 09:15:00|3|Power On|Manual control
  ```

---

This design_spec.md fully covers the Flask routes, UI element IDs and types, navigation flows, and local text file data storage formats with examples. It enables systematic development and consistent evaluation for the SmartHomeManager application.
