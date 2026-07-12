# Flask Routes and HTML Element IDs Specification for SmartHomeManager

## Section 1: Flask Routes and URL Patterns

### 1. Root Route
- **Route:** `/`  
- **Methods:** GET
- **Description:** Redirect to dashboard
- **Function Name:** `root_redirect`

### 2. Dashboard Route
- **Route:** `/dashboard`
- **Methods:** GET
- **Function Name:** `dashboard`
- **Purpose:** Show summary of all devices, quick controls, and navigation buttons

### 3. Devices List Route
- **Route:** `/devices`
- **Methods:** GET
- **Function Name:** `device_list`
- **Purpose:** Display all devices with status and control navigation

### 4. Add Device Route
- **Route:** `/device/add`
- **Methods:** GET, POST
- **Function Name:** `add_device`
- **Purpose:** Provide form to add device; POST to save new device

### 5. Device Control Route
- **Route:** `/device/<int:device_id>/control`
- **Methods:** GET, POST
- **Function Name:** `device_control`
- **Purpose:** Control and settings for device specified by `device_id`

### 6. Automation Rules Route
- **Route:** `/automation`
- **Methods:** GET, POST
- **Function Name:** `automation`
- **Purpose:** List and create/update automation rules

### 7. Energy Consumption Route
- **Route:** `/energy`
- **Methods:** GET
- **Function Name:** `energy`
- **Purpose:** Show energy consumption data and filters

### 8. Activity Logs Route
- **Route:** `/activity`
- **Methods:** GET, POST
- **Function Name:** `activity_logs`
- **Purpose:** Display and search user activity logs


## Section 2: HTML Element IDs and Types per Page

### Dashboard Page (at `/dashboard`)
- Root container div: `dashboard-page` (Div)
- Summary stats div: `dashboard-summary` (Div)
- Button: `device-list-button` (Button) - Navigate to `/devices`
- Button: `add-device-button` (Button) - Navigate to `/device/add`
- Button: `automation-button` (Button) - Navigate to `/automation`
- Button: `energy-button` (Button) - Navigate to `/energy`
- Button: `activity-button` (Button) - Navigate to `/activity`
- Div: `room-list` (Div) - List of rooms with device counts

### Devices List Page (at `/devices`)
- Container div: `device-list-container` (Div)
- Device table: `devices-table` (Table) with columns Name, Type, Room, Status, Control
- Buttons for each device control: `control-device-button-{device_id}` (Button) 
- Button: `back-to-dashboard` (Button) - Navigate to `/dashboard`

### Add Device Page (at `/device/add`)
- Form id: `add-device-form` (Form)
- Input: `device-name` (Input) - Text input for device name
- Select: `device-type` (Select) - Dropdown for device types (Light, Thermostat, Appliance, Camera, etc.)
- Select: `device-room` (Select) - Dropdown for rooms
- Button: `submit-add-device` (Button) - Submit new device
- Button: `back-to-dashboard` (Button) - Navigate to `/dashboard`

### Device Control Page (at `/device/<int:device_id>/control`)
- Container div: `device-control-page` (Div)
- Span: `device-name-display` (Span) - Displays device name
- Span: `device-status-display` (Span) - Displays device status
- Div: `control-panel` (Div) - Device-specific controls
- Button: `power-toggle` (Button) - Toggle device power
- Button: `save-settings-button` (Button) - Save control settings
- Button: `back-to-device-list` (Button) - Navigate to `/devices`

### Automation Rules Page (at `/automation`)
- Container Div: `automation-page` (Div)
- Table: `automation-rules-table` (Table) - List all automation rules
- Input: `rule-name` (Input) - Rule name input
- Select: `trigger-type` (Select) - Trigger type dropdown (Motion, Temperature, Brightness, Time)
- Input: `trigger-value` (Input) - Trigger value input
- Select: `action-device` (Select) - Device selection for action
- Select: `action-type` (Select) - Action type dropdown (On, Off, Adjust, Brightness)
- Input: `action-value` (Input) - Action parameter
- Button: `add-rule-button` (Button) - Add new rule
- Button: `back-to-dashboard` (Button) - Navigate to `/dashboard`

### Energy Consumption Page (at `/energy`)
- Container Div: `energy-report` (Div)
- Table: `energy-table` (Table) - Energy consumption data
- Input: `filter-date-input` (Input type date) - Filter date selector
- Button: `apply-filter-button` (Button) - Apply date filter
- Button: `back-to-dashboard` (Button) - Navigate to `/dashboard`

### Activity Logs Page (at `/activity`)
- Container Div: `activity-page` (Div)
- Table: `activity-table` (Table) - Activity log entries
- Input: `search-activity` (Input) - Search text box
- Button: `search-button` (Button) - Execute search
- Button: `back-to-dashboard` (Button) - Navigate to `/dashboard`


## Section 3: Data File Formats

All data files to be stored locally in a `data/` directory using pipe `|` as delimiter.

### 1. users.txt
- Format: `username|email`
- Example:
  ```
  john_doe|john@example.com
  jane_smith|jane@example.com
  ```

### 2. devices.txt
- Format:
  `username|device_id|device_name|device_type|room|brand|model|status|power|brightness|temperature|mode|schedule_time`
- Example:
  ```
  john_doe|1|Living Room Light|Light|Living Room|Philips|Hue|Online|on|75|||Auto|22:00
  john_doe|2|Bedroom Thermostat|Thermostat|Bedroom|Nest|Learning|Online|on||72|Auto|22:00
  jane_smith|3|Security Camera|Camera|Kitchen|Ring|Indoor|Online|on||||Manual|
  ```

### 3. rooms.txt
- Format:
  `username|room_id|room_name`
- Example:
  ```
  john_doe|1|Living Room
  john_doe|2|Bedroom
  john_doe|3|Kitchen
  ```

### 4. automation_rules.txt
- Format:
  `username|rule_id|rule_name|trigger_type|trigger_value|action_device_id|action_type|action_value|enabled`
- Example:
  ```
  john_doe|1|Night Light On|Motion|detected|2|On||true
  john_doe|2|Morning Thermostat|Time|06:30|2|Adjust|72|true
  ```

### 5. energy_logs.txt
- Format:
  `username|device_id|date|consumption_kwh`
- Example:
  ```
  john_doe|2|2024-11-01|2.3
  john_doe|1|2024-11-02|0.6
  jane_smith|3|2024-11-01|0.2
  ```

### 6. activity_logs.txt
- Format:
  `username|timestamp|device_id|action|details`
- Example:
  ```
  john_doe|2024-11-01 07:00:00|1|Power On|Triggered manually
  jane_smith|2024-11-01 08:30:00|2|Settings Changed|Set temperature to 68
  ```


This concludes the specification of the Flask routes with corresponding exact element IDs and data file formats.

This specification enables full implementation of the backend API endpoints and frontend UI per page, with independent and consistent development possible.