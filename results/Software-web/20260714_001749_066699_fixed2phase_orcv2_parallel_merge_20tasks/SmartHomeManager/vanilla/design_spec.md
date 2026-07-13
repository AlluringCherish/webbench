# SmartHomeManager Design Specification

---

## Section 1: Backend Specifications

### 1. Data Models and File Formats

All data files reside in the `data` directory and use pipe (`|`) as the delimiter.

#### 1.1 User Data
- **File:** `data/users.txt`
- **Schema:**
  ```
  username|email
  ```
- **Fields:**
  - `username`: string, unique user identifier
  - `email`: string, user email
- **Example:**
  ```
  john_doe|john@example.com
  jane_smith|jane@example.com
  ```

#### 1.2 Device Data
- **File:** `data/devices.txt`
- **Schema:**
  ```
  username|device_id|device_name|device_type|room|brand|model|status|power|brightness|temperature|mode|schedule_time
  ```
- **Fields:**
  - `username`: string, owner user
  - `device_id`: integer/string, unique per user
  - `device_name`: string, friendly name
  - `device_type`: string, one of (Light, Thermostat, Camera, Lock, Sensor, Appliance)
  - `room`: string (e.g., Living Room, Bedroom)
  - `brand`: string, manufacturer
  - `model`: string, model identifier
  - `status`: string, Online or Offline
  - `power`: string, "on" or "off"
  - `brightness`: integer/string or empty for non-applicable devices
  - `temperature`: integer/string or empty for non-applicable devices
  - `mode`: string (e.g., Auto, Manual) or empty
  - `schedule_time`: string (HH:MM) or empty
- **Example:**
  ```
  john_doe|1|Living Room Light|Light|Living Room|Philips|Hue|Online|on|75|||Auto|
  john_doe|2|Bedroom Thermostat|Thermostat|Bedroom|Nest|Learning|Online|on||72|Auto|22:00
  jane_smith|3|Kitchen Camera|Camera|Kitchen|Ring|Indoor|Online|on||||Manual|
  ```

#### 1.3 Room Data
- **File:** `data/rooms.txt`
- **Schema:**
  ```
  username|room_id|room_name
  ```
- **Fields:**
  - `username`: string, owner user
  - `room_id`: integer/string unique per user
  - `room_name`: string
- **Example:**
  ```
  john_doe|1|Living Room
  john_doe|2|Bedroom
  john_doe|3|Kitchen
  jane_smith|1|Living Room
  ```

#### 1.4 Automation Rules Data
- **File:** `data/automation_rules.txt`
- **Schema:**
  ```
  username|rule_id|rule_name|trigger_type|trigger_value|action_device_id|action_type|action_value|enabled
  ```
- **Fields:**
  - `username`: string, owner user
  - `rule_id`: integer/string unique per user
  - `rule_name`: string, descriptive name
  - `trigger_type`: string (Time, Motion, Temperature)
  - `trigger_value`: string (e.g., "07:00", "detected")
  - `action_device_id`: integer/string device affected
  - `action_type`: string (Turn On, Turn Off, Set Brightness, Set Temperature)
  - `action_value`: string or empty
  - `enabled`: boolean string "true" or "false"
- **Example:**
  ```
  john_doe|1|Morning Lights|Time|07:00|1|Turn On||true
  john_doe|2|Night Mode|Time|22:00|1|Set Brightness|20|true
  jane_smith|1|Motion Alert|Motion|detected|3|Turn On||true
  ```

#### 1.5 Energy Consumption Logs
- **File:** `data/energy_logs.txt`
- **Schema:**
  ```
  username|device_id|date|consumption_kwh
  ```
- **Fields:**
  - `username`: string, owner user
  - `device_id`: integer/string
  - `date`: string (YYYY-MM-DD)
  - `consumption_kwh`: decimal string
- **Example:**
  ```
  john_doe|1|2024-11-01|0.5
  john_doe|2|2024-11-01|2.3
  john_doe|1|2024-11-02|0.6
  jane_smith|3|2024-11-01|0.2
  ```

#### 1.6 Activity Logs
- **File:** `data/activity_logs.txt`
- **Schema:**
  ```
  username|timestamp|device_id|action|details
  ```
- **Fields:**
  - `username`: string, owner user
  - `timestamp`: string (YYYY-MM-DD HH:MM:SS)
  - `device_id`: integer/string
  - `action`: string describing action/event
  - `details`: string additional information
- **Example:**
  ```
  john_doe|2024-11-01 07:00:00|1|Power On|Automation triggered: Morning Lights
  john_doe|2024-11-01 08:30:00|2|Settings Changed|Temperature set to 72
  jane_smith|2024-11-01 09:15:00|3|Power On|Manual control
  ```

---

### 2. Flask Route Specifications

#### 2.1 Dashboard Page
- **Route:** `/` or `/dashboard`
- **Methods:** GET
- **Description:** Shows device summary counts, rooms with device counts, and quick navigation buttons.
- **Template Data:** Total devices count, active and offline devices counts, list of rooms for user with device counts.
- **Notes:** App start page.

#### 2.2 Device List Page
- **Route:** `/devices`
- **Methods:** GET
- **Description:** Lists all user's devices with details and action buttons.
- **Template Data:** List of device dictionaries including all device fields.
- **Notes:** Each device row includes a control button linking to the device control page.

#### 2.3 Add Device Page
- **Route:** `/devices/add`
- **Methods:** GET (render form), POST (process new device)
- **POST Data:**
  - `device_name`: string
  - `device_type`: string (Light, Thermostat, Camera, Lock, Sensor, Appliance)
  - `device_room`: string (valid room name for user)
  - `brand`: string (optional, empty if not provided)
  - `model`: string (optional, empty if not provided)
- **Behavior:** Generate unique device_id, save device with initial status Offline, power "off", default values. Redirect to device list page on success.
- **Notes:** Includes back to dashboard button.

#### 2.4 Device Control Page
- **Route:** `/devices/<device_id>`
- **Methods:** GET (show control), POST (update settings)
- **GET Param:** device_id
- **POST Data:**
  - `power`: "on" or "off"
  - `brightness`: optional integer
  - `temperature`: optional integer
  - `mode`: string (Auto, Manual, etc.)
  - `schedule_time`: string (HH:MM)
- **Behavior:** Update device data, log changes in activity logs, redirect appropriately.
- **Template Data:** Device current details.
- **Notes:** Includes back to device list button.

#### 2.5 Automation Rules Page
- **Route:** `/automation`
- **Methods:** GET (view rules), POST (add rule)
- **POST Data:**
  - `rule_name`: string
  - `trigger_type`: string (Time, Motion, Temperature)
  - `trigger_value`: string
  - `action_device_id`: device_id
  - `action_type`: string (Turn On, Turn Off, Set Brightness, Set Temperature)
  - `action_value`: string optional
  - `enabled`: string boolean "true" or "false"
- **Behavior:** Generate unique rule_id, save the rule, redirect to automation page.
- **Template Data:** List of automation rules for user.
- **Notes:** Includes back to dashboard button.

#### 2.6 Energy Report Page
- **Route:** `/energy`
- **Methods:** GET
- **Query Params:** Optional `date` (YYYY-MM-DD)
- **Description:** Show total energy consumption and per-device consumption filtered by date if provided.
- **Template Data:** Energy summary totals, list of energy logs.
- **Notes:** Includes back to dashboard button.

#### 2.7 Activity Logs Page
- **Route:** `/activity`
- **Methods:** GET
- **Query Params:** Optional `search` term
- **Description:** Display activity logs filtered by search in action or details.
- **Template Data:** Filtered activity logs list.
- **Notes:** Includes back to dashboard button.

---

## Section 2: Frontend Specifications

### 1. HTML Template Structure

#### 1.1 Dashboard Page
- **Filename:** `dashboard.html`
- **Page Title:** Smart Home Dashboard
- **Containers & Elements:**
  - Div: **dashboard-page** (overall container)
  - Div: **device-summary** (total, active, offline devices count)
  - Button: **device-list-button** (navigates to Device List page)
  - Button: **add-device-button** (navigates to Add Device page)
  - Button: **automation-button** (navigates to Automation Rules page)
  - Button: **energy-button** (navigates to Energy Report page)
  - Button: **activity-button** (navigates to Activity Logs page)
  - Div: **room-list** (list of rooms with device counts)

#### 1.2 Device List Page
- **Filename:** `device_list.html`
- **Page Title:** My Devices
- **Containers & Elements:**
  - Div: **device-list-page** container
  - Table: **device-table** (columns: name, type, room, status, actions)
  - Button(s): **control-device-button-{device_id}** for each device row, navigates to Device Control page
  - Button: **back-to-dashboard**

#### 1.3 Add Device Page
- **Filename:** `add_device.html`
- **Page Title:** Add New Device
- **Containers & Elements:**
  - Div: **add-device-page** container
  - Input: **device-name**
  - Dropdown: **device-type** (Light, Thermostat, Camera, Lock, Sensor, Appliance)
  - Dropdown: **device-room** (Living Room, Bedroom, Kitchen, Bathroom, Garage)
  - Button: **submit-device-button** (submit form)
  - Button: **back-to-dashboard**

#### 1.4 Device Control Page
- **Filename:** `device_control.html`
- **Page Title:** Device Control
- **Containers & Elements:**
  - Div: **device-control-page** container
  - H2: **device-name-display**
  - Div: **device-status-display** (Online/Offline)
  - Button: **power-toggle** (toggle power on/off)
  - Button: **save-settings-button**
  - Button: **back-to-devices**

#### 1.5 Automation Rules Page
- **Filename:** `automation_rules.html`
- **Page Title:** Automation Rules
- **Containers & Elements:**
  - Div: **automation-page** container
  - Table: **rules-table** (columns: name, trigger, action, status)
  - Input: **rule-name**
  - Dropdown: **trigger-type** (Time, Motion, Temperature)
  - Input: **trigger-value**
  - Dropdown: **action-device** (select target device)
  - Dropdown: **action-type** (Turn On, Turn Off, Set Brightness, Set Temperature)
  - Button: **add-rule-button**
  - Button: **back-to-dashboard**

#### 1.6 Energy Report Page
- **Filename:** `energy_report.html`
- **Page Title:** Energy Report
- **Containers & Elements:**
  - Div: **energy-page** container
  - Div: **energy-summary** (total consumption and cost estimate)
  - Table: **energy-table** (energy per device with date and kWh)
  - Input (date): **date-filter**
  - Button: **apply-filter-button**
  - Button: **back-to-dashboard**

#### 1.7 Activity Logs Page
- **Filename:** `activity_logs.html`
- **Page Title:** Activity Logs
- **Containers & Elements:**
  - Div: **activity-page** container
  - Table: **activity-table** (timestamp, device, action, details)
  - Input: **search-activity**
  - Button: **apply-search-button**
  - Button: **back-to-dashboard**

---

### 2. Navigation and Button Definitions

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

## Section 3: Consistency and Completeness Checks

- All backend routes have corresponding frontend navigation buttons defined.
- Data schemas in the backend match data usage and UI elements presented in frontend templates.
- Device types, room names, rule and action options are consistent in backend validation and frontend dropdown options.
- Navigation flows are unified: all "back" buttons lead to correct parent pages.
- Template IDs match element IDs in the frontend design, facilitating DOM manipulation and integration.
- User requirements from the user_task_description are fully covered by the backend routes and frontend pages.


---

# Summary

This combined design specification enables developers to implement the full SmartHomeManager Flask web application, including backend data management, route handling, and frontend HTML template layout and navigation, ensuring a seamless, consistent user experience as specified by the requirements.
