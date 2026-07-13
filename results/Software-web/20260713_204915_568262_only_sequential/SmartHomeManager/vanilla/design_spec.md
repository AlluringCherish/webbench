# Design Specification for SmartHomeManager Web Application

---

## 1. Page and Element Specification

### 1. Dashboard Page
- **Container Div ID:** dashboard-page
- **Page Title:** Smart Home Dashboard
- **Elements:**
  - device-summary (Div): Summary showing total devices, active devices, and offline devices count.
  - device-list-button (Button): Navigates to Device List Page.
  - add-device-button (Button): Navigates to Add Device Page.
  - automation-button (Button): Navigates to Automation Rules Page.
  - energy-button (Button): Navigates to Energy Report Page.
  - activity-button (Button): Navigates to Activity Logs Page.
  - room-list (Div): List of all rooms with device counts display section.

### 2. Device List Page
- **Container Div ID:** device-list-page
- **Page Title:** My Devices
- **Elements:**
  - device-table (Table): Displays devices with columns for name, type, room, status, actions.
  - control-device-button-{device_id} (Button): Navigate to Device Control Page for specific device (dynamic per device).
  - back-to-dashboard (Button): Navigates back to Dashboard Page.

### 3. Add Device Page
- **Container Div ID:** add-device-page
- **Page Title:** Add New Device
- **Elements:**
  - device-name (Input): Input field for device name.
  - device-type (Dropdown): Select device type (Light, Thermostat, Camera, Lock, Sensor, Appliance).
  - device-room (Dropdown): Select room (Living Room, Bedroom, Kitchen, Bathroom, Garage).
  - submit-device-button (Button): Submit new device.
  - back-to-dashboard (Button): Navigate back to Dashboard Page.

### 4. Device Control Page
- **Container Div ID:** device-control-page
- **Page Title:** Device Control
- **Elements:**
  - device-name-display (H2): Displays device name.
  - device-status-display (Div): Displays device status (Online/Offline).
  - power-toggle (Button): Toggle power on/off.
  - save-settings-button (Button): Save device settings.
  - back-to-devices (Button): Navigate back to Device List Page.

### 5. Automation Rules Page
- **Container Div ID:** automation-page
- **Page Title:** Automation Rules
- **Elements:**
  - rules-table (Table): Displays automation rules with columns for name, trigger, action, status.
  - rule-name (Input): Input for rule name.
  - trigger-type (Dropdown): Select trigger type (Time, Motion, Temperature).
  - trigger-value (Input): Input trigger value.
  - action-device (Dropdown): Select target device.
  - action-type (Dropdown): Select action type (Turn On, Turn Off, Set Brightness, Set Temperature).
  - add-rule-button (Button): Add new rule.
  - back-to-dashboard (Button): Navigate back to Dashboard Page.

### 6. Energy Report Page
- **Container Div ID:** energy-page
- **Page Title:** Energy Report
- **Elements:**
  - energy-summary (Div): Shows total energy consumption and cost estimate.
  - energy-table (Table): Energy consumption per device with date and kWh columns.
  - date-filter (Input date): Filter energy data by date.
  - apply-filter-button (Button): Apply date filter.
  - back-to-dashboard (Button): Navigate back to Dashboard Page.

### 7. Activity Logs Page
- **Container Div ID:** activity-page
- **Page Title:** Activity Logs
- **Elements:**
  - activity-table (Table): Displays activity logs with columns timestamp, device, action, details.
  - search-activity (Input): Search activity logs.
  - apply-search-button (Button): Apply search filter.
  - back-to-dashboard (Button): Navigate back to Dashboard Page.

---

## 2. Navigation Routing

| Button ID                 | Origin Page       | Target Page           |
|---------------------------|-------------------|-----------------------|
| device-list-button         | Dashboard Page    | Device List Page      |
| add-device-button          | Dashboard Page    | Add Device Page       |
| automation-button          | Dashboard Page    | Automation Rules Page |
| energy-button              | Dashboard Page    | Energy Report Page    |
| activity-button            | Dashboard Page    | Activity Logs Page    |
| control-device-button-{id} | Device List Page  | Device Control Page   |
| back-to-dashboard          | Device List Page  | Dashboard Page        |
| back-to-dashboard          | Add Device Page   | Dashboard Page        |
| back-to-devices            | Device Control    | Device List Page      |
| back-to-dashboard          | Automation Rules  | Dashboard Page        |
| back-to-dashboard          | Energy Report     | Dashboard Page        |
| back-to-dashboard          | Activity Logs     | Dashboard Page        |


---

## 3. Data Storage Formats

All data files are stored in the `data/` directory and use pipe (`|`) delimiter.

### 3.1 User Data
- Filename: data/users.txt
- Fields (in order): username | email
- Sample Rows:
  ```
  john_doe|john@example.com
  jane_smith|jane@example.com
  ```

### 3.2 Device Data
- Filename: data/devices.txt
- Fields (in order): username | device_id | device_name | device_type | room | brand | model | status | power | brightness | temperature | mode | schedule_time
- Sample Rows:
  ```
  john_doe|1|Living Room Light|Light|Living Room|Philips|Hue|Online|on|75|||Auto|
  john_doe|2|Bedroom Thermostat|Thermostat|Bedroom|Nest|Learning|Online|on||72|Auto|22:00
  jane_smith|3|Kitchen Camera|Camera|Kitchen|Ring|Indoor|Online|on||||Manual|
  ```

### 3.3 Room Data
- Filename: data/rooms.txt
- Fields (in order): username | room_id | room_name
- Sample Rows:
  ```
  john_doe|1|Living Room
  john_doe|2|Bedroom
  john_doe|3|Kitchen
  jane_smith|1|Living Room
  ```

### 3.4 Automation Rules Data
- Filename: data/automation_rules.txt
- Fields (in order): username | rule_id | rule_name | trigger_type | trigger_value | action_device_id | action_type | action_value | enabled
- Sample Rows:
  ```
  john_doe|1|Morning Lights|Time|07:00|1|Turn On||true
  john_doe|2|Night Mode|Time|22:00|1|Set Brightness|20|true
  jane_smith|1|Motion Alert|Motion|detected|3|Turn On||true
  ```

### 3.5 Energy Consumption Logs
- Filename: data/energy_logs.txt
- Fields (in order): username | device_id | date | consumption_kwh
- Sample Rows:
  ```
  john_doe|1|2024-11-01|0.5
  john_doe|2|2024-11-01|2.3
  john_doe|1|2024-11-02|0.6
  jane_smith|3|2024-11-01|0.2
  ```

### 3.6 Activity Logs
- Filename: data/activity_logs.txt
- Fields (in order): username | timestamp | device_id | action | details
- Sample Rows:
  ```
  john_doe|2024-11-01 07:00:00|1|Power On|Automation triggered: Morning Lights
  john_doe|2024-11-01 08:30:00|2|Settings Changed|Temperature set to 72
  jane_smith|2024-11-01 09:15:00|3|Power On|Manual control
  ```

---

## 4. User Flows

- User entry point is the **Dashboard Page** (Smart Home Dashboard).

- From Dashboard, the user can navigate to:
  - Device List Page (My Devices) to view all devices and control them.
  - Add Device Page to register new devices.
  - Automation Rules Page to create and manage automation rules.
  - Energy Report Page to view detailed energy consumption statistics.
  - Activity Logs Page to view device and system activity logs.

- From Device List Page:
  - User selects a device’s control button (`control-device-button-{device_id}`) to navigate to the corresponding Device Control Page.
  - User can return back directly to Dashboard Page using `back-to-dashboard` button.

- From Add Device Page:
  - User can submit the new device via `submit-device-button`.
  - User can use the `back-to-dashboard` button to return without submission.

- From Device Control Page:
  - User can toggle power, adjust settings and save with `save-settings-button`.
  - User uses `back-to-devices` button to return to Device List Page.

- From Automation Rules Page:
  - User can add new automation rules using `add-rule-button`.
  - User can return to Dashboard Page using `back-to-dashboard` button.

- From Energy Report Page:
  - User can filter data by date using `date-filter` and `apply-filter-button`.
  - User can return to Dashboard Page using `back-to-dashboard` button.

- From Activity Logs Page:
  - User can search logs using `search-activity` and `apply-search-button`.
  - User can return to Dashboard Page using `back-to-dashboard` button.

---

This design specification strictly adheres to all extracted requirements for the SmartHomeManager web application to guide frontend and backend development with clear element IDs, page layouts, navigation routes, data storage format, and user interaction paths.
