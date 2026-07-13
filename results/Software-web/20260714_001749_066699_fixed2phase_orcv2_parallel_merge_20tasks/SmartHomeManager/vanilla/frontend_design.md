# Frontend Design Specification for SmartHomeManager

---

## Section 1: HTML Template Structure

### 1. Dashboard Page
- Filename: dashboard.html
- Page Title: Smart Home Dashboard
- Containers & UI Components:
  - Div: **dashboard-page** (Container for the entire dashboard page)
  - Div: **device-summary** (Displays total devices, active devices, offline devices count summary)
  - Button: **device-list-button** (Navigates to Device List page)
  - Button: **add-device-button** (Navigates to Add Device page)
  - Button: **automation-button** (Navigates to Automation Rules page)
  - Button: **energy-button** (Navigates to Energy Report page)
  - Button: **activity-button** (Navigates to Activity Logs page)
  - Div: **room-list** (Shows list of all rooms with device counts)

### 2. Device List Page
- Filename: device_list.html
- Page Title: My Devices
- Containers & UI Components:
  - Div: **device-list-page** (Container for device list page)
  - Table: **device-table** (Table displaying devices with columns: name, type, room, status, actions)
  - Button(s): **control-device-button-{device_id}** (One per row in device table, navigates to Device Control page for specific device)
  - Button: **back-to-dashboard** (Navigates back to Dashboard page)

### 3. Add Device Page
- Filename: add_device.html
- Page Title: Add New Device
- Containers & UI Components:
  - Div: **add-device-page** (Container for add device page)
  - Input: **device-name** (Input field for device name)
  - Dropdown: **device-type** (Dropdown for selecting device type: Light, Thermostat, Camera, Lock, Sensor, Appliance)
  - Dropdown: **device-room** (Dropdown for selecting room: Living Room, Bedroom, Kitchen, Bathroom, Garage)
  - Button: **submit-device-button** (Submits new device registration)
  - Button: **back-to-dashboard** (Navigates back to Dashboard page)

### 4. Device Control Page
- Filename: device_control.html
- Page Title: Device Control
- Containers & UI Components:
  - Div: **device-control-page** (Container for device control page)
  - H2: **device-name-display** (Displays device name)
  - Div: **device-status-display** (Displays device current status (Online/Offline))
  - Button: **power-toggle** (Toggles device power On/Off)
  - Button: **save-settings-button** (Saves current device settings)
  - Button: **back-to-devices** (Navigates back to Device List page)

### 5. Automation Rules Page
- Filename: automation_rules.html
- Page Title: Automation Rules
- Containers & UI Components:
  - Div: **automation-page** (Container for automation rules page)
  - Table: **rules-table** (Table displaying all automation rules with columns: name, trigger, action, status)
  - Input: **rule-name** (Input field for rule name)
  - Dropdown: **trigger-type** (Dropdown for trigger type: Time, Motion, Temperature)
  - Input: **trigger-value** (Input field for trigger value, e.g., time or threshold)
  - Dropdown: **action-device** (Dropdown for selecting target device)
  - Dropdown: **action-type** (Dropdown for selecting action type: Turn On, Turn Off, Set Brightness, Set Temperature)
  - Button: **add-rule-button** (Adds new automation rule)
  - Button: **back-to-dashboard** (Navigates back to Dashboard page)

### 6. Energy Report Page
- Filename: energy_report.html
- Page Title: Energy Report
- Containers & UI Components:
  - Div: **energy-page** (Container for energy report page)
  - Div: **energy-summary** (Summary of total energy consumption and cost estimate)
  - Table: **energy-table** (Table showing energy consumption per device with date and kWh)
  - Input (date): **date-filter** (Date field to filter energy data)
  - Button: **apply-filter-button** (Applies date filter on energy data)
  - Button: **back-to-dashboard** (Navigates back to Dashboard page)

### 7. Activity Logs Page
- Filename: activity_logs.html
- Page Title: Activity Logs
- Containers & UI Components:
  - Div: **activity-page** (Container for activity logs page)
  - Table: **activity-table** (Table displaying activity logs with columns: timestamp, device, action, details)
  - Input: **search-activity** (Input field to search activity logs)
  - Button: **apply-search-button** (Applies search filter)
  - Button: **back-to-dashboard** (Navigates back to Dashboard page)

---

## Section 2: Navigation and Button Definitions

| Button/Control ID           | Description                                       | Target Page / Action                      |
|----------------------------|-------------------------------------------------|------------------------------------------|
| device-list-button          | Navigate to Device List page                     | device_list.html                         |
| add-device-button           | Navigate to Add Device page                       | add_device.html                          |
| automation-button           | Navigate to Automation Rules page                 | automation_rules.html                    |
| energy-button               | Navigate to Energy Report page                    | energy_report.html                       |
| activity-button             | Navigate to Activity Logs page                     | activity_logs.html                       |
| control-device-button-{id}  | Navigate to Device Control page for device {id}  | device_control.html?id={device_id}      |
| back-to-dashboard           | Navigate back to Dashboard page                    | dashboard.html                           |
| back-to-devices             | Navigate back to Device List page                  | device_list.html                         |
| submit-device-button        | Submit Add Device form                             | Form submission on add_device.html       |
| power-toggle                | Toggle device power on/off                         | Toggle power status via device control  |
| save-settings-button        | Save current device settings                       | Save settings on device_control.html    |
| add-rule-button             | Add a new automation rule                          | Form submission on automation_rules.html|
| apply-filter-button         | Apply filter on energy data by date               | Refresh energy_report.html with filter  |
| apply-search-button         | Apply filter on activity logs search              | Refresh activity_logs.html with filter  |

---

This design document enables frontend developers to fully implement all required HTML templates and UI navigation flows for the SmartHomeManager web application as specified in the user requirements.