# Requirements Analysis for SmartHomeManager Web Application

## 1. Pages

### 1. Dashboard Page
- **Page Title**: Smart Home Dashboard
- **Elements**:
  - ID: dashboard-page (Div) - Container for the dashboard page.
  - ID: device-summary (Div) - Summary showing total devices, active devices, and offline devices count.
  - ID: device-list-button (Button) - Navigates to Device List Page.
  - ID: add-device-button (Button) - Navigates to Add Device Page.
  - ID: automation-button (Button) - Navigates to Automation Rules Page.
  - ID: energy-button (Button) - Navigates to Energy Report Page.
  - ID: activity-button (Button) - Navigates to Activity Logs Page.
  - ID: room-list (Div) - List of all rooms with device counts display section.

### 2. Device List Page
- **Page Title**: My Devices
- **Elements**:
  - ID: device-list-page (Div) - Container for device list.
  - ID: device-table (Table) - Displays devices with name, type, room, status, actions.
  - ID: control-device-button-{device_id} (Button) - Navigate to Device Control Page for specific device.
  - ID: back-to-dashboard (Button) - Navigates back to Dashboard Page.

### 3. Add Device Page
- **Page Title**: Add New Device
- **Elements**:
  - ID: add-device-page (Div) - Container for add device form.
  - ID: device-name (Input) - Input field for device name.
  - ID: device-type (Dropdown) - Select device type (Light, Thermostat, Camera, Lock, Sensor, Appliance).
  - ID: device-room (Dropdown) - Select room (Living Room, Bedroom, Kitchen, Bathroom, Garage).
  - ID: submit-device-button (Button) - Submit new device.
  - ID: back-to-dashboard (Button) - Navigate back to Dashboard Page.

### 4. Device Control Page
- **Page Title**: Device Control
- **Elements**:
  - ID: device-control-page (Div) - Container for device control.
  - ID: device-name-display (H2) - Displays device name.
  - ID: device-status-display (Div) - Displays device status (Online/Offline).
  - ID: power-toggle (Button) - Toggle power on/off.
  - ID: save-settings-button (Button) - Save device settings.
  - ID: back-to-devices (Button) - Navigate back to Device List Page.

### 5. Automation Rules Page
- **Page Title**: Automation Rules
- **Elements**:
  - ID: automation-page (Div) - Container for automation rules.
  - ID: rules-table (Table) - Display automation rules (name, trigger, action, status).
  - ID: rule-name (Input) - Input rule name.
  - ID: trigger-type (Dropdown) - Select trigger type (Time, Motion, Temperature).
  - ID: trigger-value (Input) - Input trigger value.
  - ID: action-device (Dropdown) - Select target device.
  - ID: action-type (Dropdown) - Select action type (Turn On, Turn Off, Set Brightness, Set Temperature).
  - ID: add-rule-button (Button) - Add new rule.
  - ID: back-to-dashboard (Button) - Navigate back to Dashboard Page.

### 6. Energy Report Page
- **Page Title**: Energy Report
- **Elements**:
  - ID: energy-page (Div) - Container for energy report.
  - ID: energy-summary (Div) - Shows total energy consumption and cost estimate.
  - ID: energy-table (Table) - Energy consumption per device with date and kWh.
  - ID: date-filter (Input date) - Filter energy data by date.
  - ID: apply-filter-button (Button) - Apply date filter.
  - ID: back-to-dashboard (Button) - Navigate back to Dashboard Page.

### 7. Activity Logs Page
- **Page Title**: Activity Logs
- **Elements**:
  - ID: activity-page (Div) - Container for activity logs.
  - ID: activity-table (Table) - Display activity logs (timestamp, device, action, details).
  - ID: search-activity (Input) - Search activity logs.
  - ID: apply-search-button (Button) - Apply search filter.
  - ID: back-to-dashboard (Button) - Navigate back to Dashboard Page.

## 2. Navigation Buttons and Target Pages

From Dashboard Page:
- device-list-button --> Device List Page
- add-device-button --> Add Device Page
- automation-button --> Automation Rules Page
- energy-button --> Energy Report Page
- activity-button --> Activity Logs Page

From Device List Page:
- control-device-button-{device_id} --> Device Control Page (specific device)
- back-to-dashboard --> Dashboard Page

From Add Device Page:
- back-to-dashboard --> Dashboard Page

From Device Control Page:
- back-to-devices --> Device List Page

From Automation Rules Page:
- back-to-dashboard --> Dashboard Page

From Energy Report Page:
- back-to-dashboard --> Dashboard Page

From Activity Logs Page:
- back-to-dashboard --> Dashboard Page

## 3. Data Storage Specifications

All data files stored in `data` directory using pipe (`|`) delimiter.

### 1. User Data
- Filename: users.txt
- Fields: username|email
- Sample:
  ```
  john_doe|john@example.com
  jane_smith|jane@example.com
  ```

### 2. Device Data
- Filename: devices.txt
- Fields: username|device_id|device_name|device_type|room|brand|model|status|power|brightness|temperature|mode|schedule_time
- Sample:
  ```
  john_doe|1|Living Room Light|Light|Living Room|Philips|Hue|Online|on|75|||Auto|
  john_doe|2|Bedroom Thermostat|Thermostat|Bedroom|Nest|Learning|Online|on||72|Auto|22:00
  jane_smith|3|Kitchen Camera|Camera|Kitchen|Ring|Indoor|Online|on||||Manual|
  ```

### 3. Room Data
- Filename: rooms.txt
- Fields: username|room_id|room_name
- Sample:
  ```
  john_doe|1|Living Room
  john_doe|2|Bedroom
  john_doe|3|Kitchen
  jane_smith|1|Living Room
  ```

### 4. Automation Rules Data
- Filename: automation_rules.txt
- Fields: username|rule_id|rule_name|trigger_type|trigger_value|action_device_id|action_type|action_value|enabled
- Sample:
  ```
  john_doe|1|Morning Lights|Time|07:00|1|Turn On||true
  john_doe|2|Night Mode|Time|22:00|1|Set Brightness|20|true
  jane_smith|1|Motion Alert|Motion|detected|3|Turn On||true
  ```

### 5. Energy Consumption Logs
- Filename: energy_logs.txt
- Fields: username|device_id|date|consumption_kwh
- Sample:
  ```
  john_doe|1|2024-11-01|0.5
  john_doe|2|2024-11-01|2.3
  john_doe|1|2024-11-02|0.6
  jane_smith|3|2024-11-01|0.2
  ```

### 6. Activity Logs
- Filename: activity_logs.txt
- Fields: username|timestamp|device_id|action|details
- Sample:
  ```
  john_doe|2024-11-01 07:00:00|1|Power On|Automation triggered: Morning Lights
  john_doe|2024-11-01 08:30:00|2|Settings Changed|Temperature set to 72
  jane_smith|2024-11-01 09:15:00|3|Power On|Manual control
  ```

## 4. User Flow Overview

- User starts from **Dashboard Page** (Smart Home Dashboard).
- From Dashboard, user can navigate to:
  - Device List Page (My Devices) to view all devices and control them.
  - Add Device Page to register new devices.
  - Automation Rules Page to create/manage automation.
  - Energy Report Page to view energy usage statistics.
  - Activity Logs Page to view device and system logs.

- From Device List Page, user can:
  - Use control-device-button to go to Device Control Page for a specific device.
  - Return back to Dashboard Page.

- From Add Device Page, user can submit new device or return to Dashboard.

- From Device Control Page, user can modify settings and save or go back to Device List.

- From Automation Rules Page, user can add rules or return to Dashboard.

- From Energy Report Page and Activity Logs Page, user can return to Dashboard.

This completes the detailed requirements extracted strictly from the provided description for the SmartHomeManager application.
