# SmartHomeManager Design Specification

---

## Section 1: Flask Routes Specification

| Endpoint URL                | HTTP Methods | Function Name           | Template Rendered          | Context Variables (Name: Type)                          |
|-----------------------------|--------------|------------------------|----------------------------|--------------------------------------------------------|
| `/`                         | GET          | root_redirect          | -                          | -                                                      |
| `/dashboard`                | GET          | dashboard_page         | dashboard.html             | devices: list of dict, rooms: list of dict              |
| `/devices`                 | GET          | device_list_page       | devices.html               | devices: list of dict                                   |
| `/devices/add`             | GET, POST    | add_device_page        | add_device.html (GET)      | rooms: list of str, device_types: list of str           |
|                            |              |                        | redirect to /devices (POST) | -                                                    |
| `/devices/control/<int:device_id>` | GET, POST    | device_control_page    | device_control.html        | device: dict, success: bool (optional)                  |
| `/automation`              | GET, POST    | automation_rules_page  | automation.html            | rules: list of dict, devices: list of dict               |
|                            |              |                        | redirect to /automation (POST) | -                                                    |
| `/energy`                  | GET, POST    | energy_report_page     | energy_report.html         | energy_data: list of dict, summary: dict, filter_date: str (optional) |
| `/activity`                | GET, POST    | activity_logs_page     | activity_logs.html         | logs: list of dict, search_query: str (optional)        |

---

- **Route Details:**

1. **`/`**
   - Redirects to `/dashboard`.

2. **`/dashboard`** (GET)
   - Renders `dashboard.html`.
   - Context variables:
     - `devices`: List containing device dictionaries.
     - `rooms`: List containing room dictionaries with device counts.

3. **`/devices`** (GET)
   - Renders `devices.html`.
   - Context variables:
     - `devices`: List of device dictionaries for current user.

4. **`/devices/add`** (GET, POST)
   - GET: Renders `add_device.html` with context:
     - `rooms`: List of room names (strings).
     - `device_types`: List of device type strings.
   - POST: Handles new device submission, then redirects to `/devices`.

5. **`/devices/control/<int:device_id>`** (GET, POST)
   - GET: Renders `device_control.html`.
   - POST: Saves settings; if success, may render same with success flag.
   - Context variables:
     - `device`: Dictionary of device details.
     - Optional `success`: Boolean to indicate if save was successful.

6. **`/automation`** (GET, POST)
   - GET: Renders `automation.html`.
   - POST: Handles adding/updating rules, then redirects back.
   - Context variables:
     - `rules`: List of automation rule dictionaries.
     - `devices`: List of device dictionaries for dropdown.

7. **`/energy`** (GET, POST)
   - GET and POST (with date filter): Renders `energy_report.html`.
   - Context variables:
     - `energy_data`: List of energy consumption dictionaries.
     - `summary`: Dictionary with total consumption and cost.
     - Optional `filter_date`: String (YYYY-MM-DD) if filtering applied.

8. **`/activity`** (GET, POST)
   - GET and POST (with search query): Renders `activity_logs.html`.
   - Context variables:
     - `logs`: List of activity log dictionaries.
     - Optional `search_query`: String with current search filter.


---

## Section 2: HTML Templates Specification

### 1. `templates/dashboard.html`
- **Page Title**: Smart Home Dashboard
- **Element IDs and Details:**
  - `dashboard-page`: Div. Main container.
  - `device-summary`: Div. Displays counts of total, active, offline devices.
  - `device-list-button`: Button. Navigates to device list page (`url_for('device_list_page')`).
  - `add-device-button`: Button. Navigates to add device page (`url_for('add_device_page')`).
  - `automation-button`: Button. Navigates to automation rules page (`url_for('automation_rules_page')`).
  - `energy-button`: Button. Navigates to energy report page (`url_for('energy_report_page')`).
  - `activity-button`: Button. Navigates to activity logs page (`url_for('activity_logs_page')`).
  - `room-list`: Div. Contains list of rooms with device counts.

---

### 2. `templates/devices.html`
- **Page Title**: My Devices
- **Element IDs and Details:**
  - `device-list-page`: Div. Main container.
  - `device-table`: Table. Lists devices with columns: Name, Type, Room, Status, Actions.
  - For each device row:
    - `control-device-button-{device_id}`: Button. Navigates to device control page (`url_for('device_control_page', device_id=device_id)`).
  - `back-to-dashboard`: Button. Navigates back to dashboard (`url_for('dashboard_page')`).

---

### 3. `templates/add_device.html`
- **Page Title**: Add New Device
- **Element IDs and Details:**
  - `add-device-page`: Div. Main container.
  - `device-name`: Input (text). Input for device name.
  - `device-type`: Dropdown (select).
    - Options: Light, Thermostat, Camera, Lock, Sensor, Appliance.
  - `device-room`: Dropdown (select).
    - Options: Living Room, Bedroom, Kitchen, Bathroom, Garage.
  - `submit-device-button`: Button. Submit new device.
  - `back-to-dashboard`: Button. Navigate back to dashboard (`url_for('dashboard_page')`).

---

### 4. `templates/device_control.html`
- **Page Title**: Device Control
- **Element IDs and Details:**
  - `device-control-page`: Div. Main container.
  - `device-name-display`: H2. Displays device name.
  - `device-status-display`: Div. Shows current device status (Online/Offline).
  - `power-toggle`: Button. Toggles device power on/off.
  - `save-settings-button`: Button. Saves device settings.
  - `back-to-devices`: Button. Navigates back to device list (`url_for('device_list_page')`).

---

### 5. `templates/automation.html`
- **Page Title**: Automation Rules
- **Element IDs and Details:**
  - `automation-page`: Div. Main container.
  - `rules-table`: Table. Lists rules with columns: Name, Trigger, Action, Status.
  - `rule-name`: Input (text). For rule name.
  - `trigger-type`: Dropdown (select).
    - Options: Time, Motion, Temperature.
  - `trigger-value`: Input (text). For trigger value (e.g., time or threshold).
  - `action-device`: Dropdown (select).
    - Options populated from devices context variable.
  - `action-type`: Dropdown (select).
    - Options: Turn On, Turn Off, Set Brightness, Set Temperature.
  - `add-rule-button`: Button. Adds new automation rule.
  - `back-to-dashboard`: Button. Navigate back to dashboard (`url_for('dashboard_page')`).

---

### 6. `templates/energy_report.html`
- **Page Title**: Energy Report
- **Element IDs and Details:**
  - `energy-page`: Div. Main container.
  - `energy-summary`: Div. Shows total energy consumption and cost estimate.
  - `energy-table`: Table. Lists consumption per device with columns: Date, Device, kWh.
  - `date-filter`: Input (date). Filter energy data by date.
  - `apply-filter-button`: Button. Applies the date filter.
  - `back-to-dashboard`: Button. Navigate back to dashboard (`url_for('dashboard_page')`).

---

### 7. `templates/activity_logs.html`
- **Page Title**: Activity Logs
- **Element IDs and Details:**
  - `activity-page`: Div. Main container.
  - `activity-table`: Table. Lists logs with columns: Timestamp, Device, Action, Details.
  - `search-activity`: Input (text). Search filter for activity logs.
  - `apply-search-button`: Button. Applies the search filter.
  - `back-to-dashboard`: Button. Navigate back to dashboard (`url_for('dashboard_page')`).


---

## Section 3: Data File Schemas

### 1. `data/users.txt`
- Pipe-delimited fields:
  1. username (str): Unique user identifier.
  2. email (str): User email address.

- Examples:
  ```
john_doe|john@example.com
jane_smith|jane@example.com
  ```

---

### 2. `data/devices.txt`
- Pipe-delimited fields:
  1. username (str): Owner username.
  2. device_id (int): Unique device identifier.
  3. device_name (str): Name given to the device.
  4. device_type (str): Type of device (Light, Thermostat, etc.).
  5. room (str): Room name.
  6. brand (str): Brand of device.
  7. model (str): Model of device.
  8. status (str): Status string, e.g. Online or Offline.
  9. power (str): power state, e.g. on/off.
  10. brightness (int or empty): brightness level (0-100), empty if not applicable.
  11. temperature (int or empty): temperature value, empty if not applicable.
  12. mode (str): Mode string e.g. Auto, Manual, or empty.
  13. schedule_time (str): Scheduled time in HH:MM format or empty.

- Examples:
  ```
john_doe|1|Living Room Light|Light|Living Room|Philips|Hue|Online|on|75|||Auto|
john_doe|2|Bedroom Thermostat|Thermostat|Bedroom|Nest|Learning|Online|on||72|Auto|22:00
jane_smith|3|Kitchen Camera|Camera|Kitchen|Ring|Indoor|Online|on||||Manual|
  ```

---

### 3. `data/rooms.txt`
- Pipe-delimited fields:
  1. username (str): Owner username.
  2. room_id (int): Unique room identifier.
  3. room_name (str): Name of the room.

- Examples:
  ```
john_doe|1|Living Room
john_doe|2|Bedroom
john_doe|3|Kitchen
jane_smith|1|Living Room
  ```

---

### 4. `data/automation_rules.txt`
- Pipe-delimited fields:
  1. username (str): Owner username.
  2. rule_id (int): Unique rule identifier.
  3. rule_name (str): Name of the rule.
  4. trigger_type (str): Trigger type (Time, Motion, Temperature).
  5. trigger_value (str): Value for the trigger, e.g., time or detected.
  6. action_device_id (int): Device ID to which the action applies.
  7. action_type (str): Action to perform (Turn On, Turn Off, Set Brightness, Set Temperature).
  8. action_value (str): Value for action, e.g. brightness level, else empty.
  9. enabled (bool as str): 'true' or 'false' string indicating if rule is enabled.

- Examples:
  ```
john_doe|1|Morning Lights|Time|07:00|1|Turn On||true
john_doe|2|Night Mode|Time|22:00|1|Set Brightness|20|true
jane_smith|1|Motion Alert|Motion|detected|3|Turn On||true
  ```

---

### 5. `data/energy_logs.txt`
- Pipe-delimited fields:
  1. username (str): Owner username.
  2. device_id (int): Device identifier.
  3. date (str): Date in YYYY-MM-DD format.
  4. consumption_kwh (float): Energy consumed in kilowatt-hours.

- Examples:
  ```
john_doe|1|2024-11-01|0.5
john_doe|2|2024-11-01|2.3
john_doe|1|2024-11-02|0.6
jane_smith|3|2024-11-01|0.2
  ```

---

### 6. `data/activity_logs.txt`
- Pipe-delimited fields:
  1. username (str): Owner username.
  2. timestamp (str): Timestamp in YYYY-MM-DD HH:MM:SS format.
  3. device_id (int): Device identifier.
  4. action (str): Action performed.
  5. details (str): Additional details or notes.

- Examples:
  ```
john_doe|2024-11-01 07:00:00|1|Power On|Automation triggered: Morning Lights
john_doe|2024-11-01 08:30:00|2|Settings Changed|Temperature set to 72
jane_smith|2024-11-01 09:15:00|3|Power On|Manual control
  ```

---

End of Design Specification
