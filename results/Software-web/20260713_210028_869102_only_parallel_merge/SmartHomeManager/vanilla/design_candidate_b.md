# SmartHomeManager Flask Web Application Design Specification (Candidate B)

---

## General Notes
- The application is developed using Python and Flask.
- All data is stored locally in text files under the `data` directory.
- The website's starting point is the Dashboard page (`/`).
- Navigation buttons use consistent element IDs across pages for uniform UX.
- Page routes and navigation button mappings are explicitly defined.
- Data fixture files are referenced where relevant to indicate data usage and interaction.

---

## 1. Dashboard Page

- **Route:** `/`
- **Page Title:** Smart Home Dashboard
- **Elements:**
  - `dashboard-page`: Div container for the dashboard page.
  - `device-summary`: Div showing total devices, active devices, offline devices count.
  - `device-list-button`: Button navigating to Device List page (`/devices`).
  - `add-device-button`: Button navigating to Add Device page (`/devices/add`).
  - `automation-button`: Button navigating to Automation Rules page (`/automation`).
  - `energy-button`: Button navigating to Energy Report page (`/energy`).
  - `activity-button`: Button navigating to Activity Logs page (`/activity`).
  - `room-list`: Div listing all rooms with device counts.

- **Navigation Button Mappings:**
  - `device-list-button` → `/devices`
  - `add-device-button` → `/devices/add`
  - `automation-button` → `/automation`
  - `energy-button` → `/energy`
  - `activity-button` → `/activity`

- **Data Fixtures Referenced:**
  - `devices.txt` (for device summaries and status counts)
  - `rooms.txt` (to show rooms and device counts)

---

## 2. Device List Page

- **Route:** `/devices`
- **Page Title:** My Devices
- **Elements:**
  - `device-list-page`: Div container for device list.
  - `device-table`: Table showing all devices with columns - name, type, room, status, actions.
  - `control-device-button-{device_id}`: Button in each device row; navigates to Device Control page for that device.
  - `back-to-dashboard`: Button navigating back to Dashboard (`/`).

- **Navigation Button Mappings:**
  - `back-to-dashboard` → `/`
  - `control-device-button-{device_id}` → `/devices/control/<device_id>`

- **Data Fixtures Referenced:**
  - `devices.txt` (to populate device list table)

---

## 3. Add Device Page

- **Route:** `/devices/add`
- **Page Title:** Add New Device
- **Elements:**
  - `add-device-page`: Div container for the add device form.
  - `device-name`: Input field for device name.
  - `device-type`: Dropdown for selecting device type [Light, Thermostat, Camera, Lock, Sensor, Appliance].
  - `device-room`: Dropdown for selecting room [Living Room, Bedroom, Kitchen, Bathroom, Garage].
  - `submit-device-button`: Button to submit and register the new device.
  - `back-to-dashboard`: Button navigating back to Dashboard (`/`).

- **Navigation Button Mappings:**
  - `back-to-dashboard` → `/`

- **Data Fixtures Referenced:**
  - `rooms.txt` (to populate room dropdown)

---

## 4. Device Control Page

- **Route:** `/devices/control/<device_id>`
- **Page Title:** Device Control
- **Elements:**
  - `device-control-page`: Div container for device control.
  - `device-name-display`: H2 element displaying the device's name.
  - `device-status-display`: Div displaying device status (Online/Offline).
  - `power-toggle`: Button to toggle device power on/off.
  - `save-settings-button`: Button to save updated device settings.
  - `back-to-devices`: Button navigating back to Device List page (`/devices`).

- **Navigation Button Mappings:**
  - `back-to-devices` → `/devices`

- **Data Fixtures Referenced:**
  - `devices.txt` (to load and update device details and control status)

---

## 5. Automation Rules Page

- **Route:** `/automation`
- **Page Title:** Automation Rules
- **Elements:**
  - `automation-page`: Div container for automation rules.
  - `rules-table`: Table displaying all automation rules with name, trigger, action, and status.
  - `rule-name`: Input field to input new rule name.
  - `trigger-type`: Dropdown to select trigger type [Time, Motion, Temperature].
  - `trigger-value`: Input field to enter trigger value (time or threshold).
  - `action-device`: Dropdown to select the device to apply action.
  - `action-type`: Dropdown to select action type [Turn On, Turn Off, Set Brightness, Set Temperature].
  - `add-rule-button`: Button to add new automation rule.
  - `back-to-dashboard`: Button navigating back to Dashboard (`/`).

- **Navigation Button Mappings:**
  - `back-to-dashboard` → `/`

- **Data Fixtures Referenced:**
  - `automation_rules.txt` (for existing rules)
  - `devices.txt` (to populate list of devices for actions)

---

## 6. Energy Report Page

- **Route:** `/energy`
- **Page Title:** Energy Report
- **Elements:**
  - `energy-page`: Div container for energy report.
  - `energy-summary`: Div showing total energy consumption and estimated cost.
  - `energy-table`: Table listing energy consumption per device with date and kWh.
  - `date-filter`: Date input field to filter energy data.
  - `apply-filter-button`: Button to apply date filter.
  - `back-to-dashboard`: Button navigating back to Dashboard (`/`).

- **Navigation Button Mappings:**
  - `back-to-dashboard` → `/`

- **Data Fixtures Referenced:**
  - `energy_logs.txt` (source of historical energy consumption data)
  - `devices.txt` (to link device IDs to names)

---

## 7. Activity Logs Page

- **Route:** `/activity`
- **Page Title:** Activity Logs
- **Elements:**
  - `activity-page`: Div container for activity logs.
  - `activity-table`: Table showing activity logs with timestamp, device, action, and details.
  - `search-activity`: Input field for searching activity logs.
  - `apply-search-button`: Button to apply search filter.
  - `back-to-dashboard`: Button navigating back to Dashboard (`/`).

- **Navigation Button Mappings:**
  - `back-to-dashboard` → `/`

- **Data Fixtures Referenced:**
  - `activity_logs.txt` (for log data)
  - `devices.txt` (to resolve device names)

---

## Summary of Routes and Navigation

| Route                  | Page                    | Navigation Buttons and Targets                                   |
|------------------------|-------------------------|-----------------------------------------------------------------|
| `/`                    | Dashboard               | device-list-button → `/devices`<br>add-device-button → `/devices/add`<br>automation-button → `/automation`<br>energy-button → `/energy`<br>activity-button → `/activity` |
| `/devices`             | Device List             | back-to-dashboard → `/`<br>control-device-button-{device_id} → `/devices/control/<device_id>` |
| `/devices/add`         | Add Device              | back-to-dashboard → `/`                                          |
| `/devices/control/<device_id>` | Device Control         | back-to-devices → `/devices`                                    |
| `/automation`          | Automation Rules        | back-to-dashboard → `/`                                          |
| `/energy`              | Energy Report           | back-to-dashboard → `/`                                          |
| `/activity`            | Activity Logs           | back-to-dashboard → `/`                                          |

---

## Data Fixture File Summary

| Data Type           | Filename               | Usage Contexts                                 |
|---------------------|------------------------|------------------------------------------------|
| User Data           | `users.txt`            | User management and ownership (not detailed in UI) |
| Device Data         | `devices.txt`          | Device list, device control, automation target, energy report, activity logs |
| Room Data           | `rooms.txt`            | Room names for device addition and dashboard room listing |
| Automation Rules    | `automation_rules.txt` | Display and manage automation rules              |
| Energy Consumption  | `energy_logs.txt`      | Energy report filtering and summation            |
| Activity Logs       | `activity_logs.txt`    | Display of device and system activity logs       |

---

This completes the alternative comprehensive design specification for the SmartHomeManager Flask web application as per the user requirements.