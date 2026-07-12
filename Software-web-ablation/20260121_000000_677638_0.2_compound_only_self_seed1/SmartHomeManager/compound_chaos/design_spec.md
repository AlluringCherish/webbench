# SmartHomeManager Design Specification

---

## Section 1: Flask Routes Specification

### 1. Root Route
- **Endpoint URL:** `/`
- **HTTP Methods:** GET
- **Function Name:** `root_redirect`
- **Template Rendered:** None (redirect to dashboard)
- **Context Variables:** None

### 2. Dashboard Page
- **Endpoint URL:** `/dashboard`
- **HTTP Methods:** GET
- **Function Name:** `dashboard`
- **Template Rendered:** `dashboard.html`
- **Context Variables:**
  - `total_devices`: int
  - `active_devices`: int
  - `offline_devices`: int
  - `rooms`: dict[str, int]  # Room names to device counts

### 3. Device List Page
- **Endpoint URL:** `/devices`
- **HTTP Methods:** GET
- **Function Name:** `device_list`
- **Template Rendered:** `device_list.html`
- **Context Variables:**
  - `devices`: list of dicts with keys:
    - `device_id`: int
    - `device_name`: str
    - `device_type`: str
    - `room`: str
    - `status`: str

### 4. Add Device Page
- **Endpoint URL:** `/device/add`
- **HTTP Methods:** GET, POST
- **Function Name:** `add_device`
- **Template Rendered:** `add_device.html`
- **Context Variables (GET):**
  - `device_types`: list[str]
  - `rooms`: list[str]
- **POST behaviour:** Process add device form data and redirect to device list.

### 5. Device Control Page
- **Endpoint URL:** `/device/<int:device_id>/control`
- **HTTP Methods:** GET, POST
- **Function Name:** `device_control`
- **Template Rendered:** `device_control.html`
- **Context Variables:**
  - `device`: dict with keys:
    - `device_id`: int
    - `device_name`: str
    - `status`: str
    - `power`: str
    - other device settings may be included.
- **POST behaviour:** Save control changes and redirect or reload.

### 6. Automation Rules Page
- **Endpoint URL:** `/automation`
- **HTTP Methods:** GET, POST
- **Function Name:** `automation`
- **Template Rendered:** `automation.html`
- **Context Variables:**
  - `automation_rules`: list of dicts with keys:
    - `rule_id`: int
    - `rule_name`: str
    - `trigger_type`: str
    - `trigger_value`: str
    - `action_device_id`: int
    - `action_type`: str
    - `action_value`: str or empty
    - `enabled`: bool
  - `devices`: list of dicts with `device_id` and `device_name`
- **POST behaviour:** Add or update rules.

### 7. Energy Report Page
- **Endpoint URL:** `/energy`
- **HTTP Methods:** GET
- **Function Name:** `energy`
- **Template Rendered:** `energy.html`
- **Context Variables:**
  - `energy_records`: list of dicts with keys:
    - `username`: str
    - `device_id`: int
    - `device_name`: str
    - `date`: str
    - `consumption_kwh`: float
  - `date_filter`: str or None

### 8. Activity Logs Page
- **Endpoint URL:** `/activity`
- **HTTP Methods:** GET, POST
- **Function Name:** `activity_logs`
- **Template Rendered:** `activity_logs.html`
- **Context Variables:**
  - `logs`: list of dicts with keys:
    - `username`: str
    - `timestamp`: str
    - `device_id`: int
    - `action`: str
    - `details`: str
  - `search_query`: str or None

---

## Section 2: HTML Templates Specification

### Template: `dashboard.html`
- **Filepath:** `templates/dashboard.html`
- **Page Title:** "Smart Home Dashboard"
- **Element IDs:**
  - `dashboard-page` (Div): Dashboard container
  - `device-summary` (Div): Summary block with total, active, offline counts
  - `device-list-button` (Button): Link to `/devices`
  - `add-device-button` (Button): Link to `/device/add`
  - `automation-button` (Button): Link to `/automation`
  - `energy-button` (Button): Link to `/energy`
  - `activity-button` (Button): Link to `/activity`
  - `room-list` (Div): List rooms with their device count

### Template: `device_list.html`
- **Filepath:** `templates/device_list.html`
- **Page Title:** "My Devices"
- **Element IDs:**
  - `device-list-page` (Div): Container div
  - `device-table` (Table): Device info table
  - `control-device-button-{device_id}` (Button): For each device, navigates to control page
  - `back-to-dashboard` (Button): Link to `/dashboard`
- **Dynamic ID Pattern:** `control-device-button-{device_id}` where `{device_id}` is replaced with device ID

### Template: `add_device.html`
- **Filepath:** `templates/add_device.html`
- **Page Title:** "Add New Device"
- **Element IDs:**
  - `add-device-page` (Div): Container
  - `device-name` (Input): Text input for the device name
  - `device-type` (Dropdown): Device type selection
  - `device-room` (Dropdown): Room selection
  - `submit-device-button` (Button): Submit add device form
  - `back-to-dashboard` (Button): Link to `/dashboard`

### Template: `device_control.html`
- **Filepath:** `templates/device_control.html`
- **Page Title:** "Device Control"
- **Element IDs:**
  - `device-control-page` (Div): Container
  - `device-name-display` (H2): Displays device name
  - `device-status-display` (Div): Displays current device status
  - `power-toggle` (Button): Toggle device power
  - `save-settings-button` (Button): Save device settings
  - `back-to-devices` (Button): Link to `/devices`

### Template: `automation.html`
- **Filepath:** `templates/automation.html`
- **Page Title:** "Automation Rules"
- **Element IDs:**
  - `automation-page` (Div): Container
  - `rules-table` (Table): Automation rules list
  - `rule-name` (Input): Rule name input
  - `trigger-type` (Dropdown): Trigger type selection
  - `trigger-value` (Input): Trigger value input
  - `action-device` (Dropdown): Action target device selection
  - `action-type` (Dropdown): Action type selection
  - `add-rule-button` (Button): Submit new rule
  - `back-to-dashboard` (Button): Link to `/dashboard`

### Template: `energy.html`
- **Filepath:** `templates/energy.html`
- **Page Title:** "Energy Report"
- **Element IDs:**
  - `energy-page` (Div): Container
  - `energy-summary` (Div): Energy stats summary
  - `energy-table` (Table): Energy data per device with date and consumption
  - `date-filter` (Input type date): Date filter for energy data
  - `apply-filter-button` (Button): Apply filter button
  - `back-to-dashboard` (Button): Link to `/dashboard`

### Template: `activity_logs.html`
- **Filepath:** `templates/activity_logs.html`
- **Page Title:** "Activity Logs"
- **Element IDs:**
  - `activity-page` (Div): Container
  - `activity-table` (Table): Activity logs
  - `search-activity` (Input): Search input field
  - `apply-search-button` (Button): Apply search
  - `back-to-dashboard` (Button): Link to `/dashboard`

---

## Section 3: Data File Schemas

### 1. `data/users.txt`
- Fields (pipe-delimited):
  1. `username` (str)  
  2. `email` (str)
- Example lines:
```
john_doe|john@example.com
jane_smith|jane@example.com
```
- No header line; strict pipe-delimited fields

---

### 2. `data/devices.txt`
- Fields (pipe-delimited):
  1. `username` (str)
  2. `device_id` (int)
  3. `device_name` (str)
  4. `device_type` (str)
  5. `room` (str)
  6. `brand` (str)
  7. `model` (str)
  8. `status` (str) e.g. Online/Offline
  9. `power` (str) e.g. "on" or "off"
  10. `brightness` (str) or empty
  11. `temperature` (str) or empty
  12. `mode` (str)
  13. `schedule_time` (str)
- Example lines:
```
john_doe|1|Living Room Light|Light|Living Room|Philips|Hue|Online|on|75|||Auto|
john_doe|2|Bedroom Thermostat|Thermostat|Bedroom|Nest|Learning|Online|on||72|Auto|22:00
jane_smith|3|Kitchen Camera|Camera|Kitchen|Ring|Indoor|Online|on||||Manual|
```

---

### 3. `data/rooms.txt`
- Fields (pipe-delimited):
  1. `username` (str)
  2. `room_id` (int)
  3. `room_name` (str)
- Example lines:
```
john_doe|1|Living Room
john_doe|2|Bedroom
john_doe|3|Kitchen
jane_smith|1|Living Room
```

---

### 4. `data/automation_rules.txt`
- Fields (pipe-delimited):
  1. `username` (str)
  2. `rule_id` (int)
  3. `rule_name` (str)
  4. `trigger_type` (str)
  5. `trigger_value` (str)
  6. `action_device_id` (int)
  7. `action_type` (str)
  8. `action_value` (str) or empty
  9. `enabled` (bool as string "true" or "false")
- Example lines:
```
john_doe|1|Morning Lights|Time|07:00|1|Turn On||true
john_doe|2|Night Mode|Time|22:00|1|Set Brightness|20|true
jane_smith|1|Motion Alert|Motion|detected|3|Turn On||true
```

---

### 5. `data/energy_logs.txt`
- Fields (pipe-delimited):
  1. `username` (str)
  2. `device_id` (int)
  3. `date` (str in YYYY-MM-DD format)
  4. `consumption_kwh` (float)
- Example lines:
```
john_doe|1|2024-11-01|0.5
john_doe|2|2024-11-01|2.3
john_doe|1|2024-11-02|0.6
jane_smith|3|2024-11-01|0.2
```

---

### 6. `data/activity_logs.txt`
- Fields (pipe-delimited):
  1. `username` (str)
  2. `timestamp` (str datetime in "YYYY-MM-DD HH:MM:SS" format)
  3. `device_id` (int)
  4. `action` (str)
  5. `details` (str)
- Example lines:
```
john_doe|2024-11-01 07:00:00|1|Power On|Automation triggered: Morning Lights
john_doe|2024-11-01 08:30:00|2|Settings Changed|Temperature set to 72
jane_smith|2024-11-01 09:15:00|3|Power On|Manual control
```

---

This document fully specifies the Flask routes and function handlers, front-end templates with precise element IDs, and the local file data schemas with examples, enabling frontend and backend teams to develop independently and cohesively.