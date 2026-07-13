# SmartHomeManager Backend Design Specification

## Section 1: Data Models and File Formats

All data files reside in the `data` directory. Each file uses pipe (`|`) as delimiter for fields.

### 1. User Data
- **File:** `data/users.txt`
- **Schema:**
  ```
  username|email
  ```
- **Fields:**
  - `username`: string, unique identifier for the user
  - `email`: string, user's email
- **Example:**
  ```
  john_doe|john@example.com
  jane_smith|jane@example.com
  ```

### 2. Device Data
- **File:** `data/devices.txt`
- **Schema:**
  ```
  username|device_id|device_name|device_type|room|brand|model|status|power|brightness|temperature|mode|schedule_time
  ```
- **Fields:**
  - `username`: string, owner user
  - `device_id`: integer/string, unique device identifier per user
  - `device_name`: string, friendly device name
  - `device_type`: string, one of (Light, Thermostat, Camera, Lock, Sensor, Appliance)
  - `room`: string, e.g., Living Room, Bedroom
  - `brand`: string, device manufacturer
  - `model`: string, model identifier
  - `status`: string, Online or Offline
  - `power`: string, "on" or "off" to indicate power state
  - `brightness`: integer/string, brightness level (for applicable devices) or empty
  - `temperature`: integer/string, temperature value (for thermostats) or empty
  - `mode`: string, e.g., Auto, Manual, or empty
  - `schedule_time`: string, time in HH:MM or empty
- **Example:**
  ```
  john_doe|1|Living Room Light|Light|Living Room|Philips|Hue|Online|on|75|||Auto|
  john_doe|2|Bedroom Thermostat|Thermostat|Bedroom|Nest|Learning|Online|on||72|Auto|22:00
  jane_smith|3|Kitchen Camera|Camera|Kitchen|Ring|Indoor|Online|on||||Manual|
  ```

### 3. Room Data
- **File:** `data/rooms.txt`
- **Schema:**
  ```
  username|room_id|room_name
  ```
- **Fields:**
  - `username`: string, owner user
  - `room_id`: integer/string, room identifier unique per user
  - `room_name`: string, name of the room
- **Example:**
  ```
  john_doe|1|Living Room
  john_doe|2|Bedroom
  john_doe|3|Kitchen
  jane_smith|1|Living Room
  ```

### 4. Automation Rules Data
- **File:** `data/automation_rules.txt`
- **Schema:**
  ```
  username|rule_id|rule_name|trigger_type|trigger_value|action_device_id|action_type|action_value|enabled
  ```
- **Fields:**
  - `username`: string, owner user
  - `rule_id`: integer/string, unique rule identifier per user
  - `rule_name`: string, descriptive name of the rule
  - `trigger_type`: string, e.g. Time, Motion, Temperature
  - `trigger_value`: string, the value triggering the rule (e.g., time "07:00", motion "detected")
  - `action_device_id`: integer/string, device_id of the device affected
  - `action_type`: string, e.g., Turn On, Turn Off, Set Brightness, Set Temperature
  - `action_value`: string, optional value for action (brightness, temp etc.) or empty
  - `enabled`: boolean string `true` or `false` indicating if rule is active
- **Example:**
  ```
  john_doe|1|Morning Lights|Time|07:00|1|Turn On||true
  john_doe|2|Night Mode|Time|22:00|1|Set Brightness|20|true
  jane_smith|1|Motion Alert|Motion|detected|3|Turn On||true
  ```

### 5. Energy Consumption Logs
- **File:** `data/energy_logs.txt`
- **Schema:**
  ```
  username|device_id|date|consumption_kwh
  ```
- **Fields:**
  - `username`: string, owner user
  - `device_id`: integer/string
  - `date`: string, format YYYY-MM-DD
  - `consumption_kwh`: decimal string, e.g., 0.5
- **Example:**
  ```
  john_doe|1|2024-11-01|0.5
  john_doe|2|2024-11-01|2.3
  john_doe|1|2024-11-02|0.6
  jane_smith|3|2024-11-01|0.2
  ```

### 6. Activity Logs
- **File:** `data/activity_logs.txt`
- **Schema:**
  ```
  username|timestamp|device_id|action|details
  ```
- **Fields:**
  - `username`: string, owner user
  - `timestamp`: string, format YYYY-MM-DD HH:MM:SS
  - `device_id`: integer/string
  - `action`: string describing the action/event
  - `details`: string, additional info
- **Example:**
  ```
  john_doe|2024-11-01 07:00:00|1|Power On|Automation triggered: Morning Lights
  john_doe|2024-11-01 08:30:00|2|Settings Changed|Temperature set to 72
  jane_smith|2024-11-01 09:15:00|3|Power On|Manual control
  ```

---

## Section 2: Flask Route Specifications

The Flask app should support the following routes handling CRUD operations and page navigation.

---

### 1. Dashboard Page
- **Route:** `/` or `/dashboard`
- **Methods:** GET
- **Description:**
  - Displays dashboard overview including device summary, quick controls, and rooms with device counts.
  - Loads user-specific data (e.g. devices, rooms).
- **Template Data:**
  - Total devices count, active and offline device counts.
  - List of rooms for the user with device counts.
- **Notes:** Starts page on app launch.

---

### 2. Device List Page
- **Route:** `/devices`
- **Methods:** GET
- **Description:**
  - Displays all devices registered for the logged-in user.
  - Shows device name, type, room, status, and actions.
- **Template Data:**
  - List of device dictionaries with all device fields.
- **Notes:** Each device row has a button linking to device control page.

---

### 3. Add Device Page
- **Route:** `/devices/add`
- **Methods:**
  - GET: Render add device form.
  - POST: Process form submission to add a new device.
- **POST Form Data:**
  - `device_name`: string
  - `device_type`: string (must be one of defined types)
  - `device_room`: string (must be valid room name for user)
  - `brand`: string (optional, else empty string assumed)
  - `model`: string (optional, else empty string assumed)
- **Behavior:**
  - Generate a new unique device_id for the user.
  - Save the device with initial status Offline, power off, and other applicable default values.
  - Redirect to device list on success.
- **Notes:**
  - Back to dashboard button included.

---

### 4. Device Control Page
- **Route:** `/devices/<device_id>`
- **Methods:**
  - GET: Show the device control page.
  - POST: Update device control settings.
- **GET Params:**
  - `device_id`: identifies which device to control
- **POST Form Data:**
  - `power`: string "on" or "off"
  - `brightness`: optional integer (if applicable)
  - `temperature`: optional integer (if applicable)
  - `mode`: string (e.g., Auto, Manual)
  - `schedule_time`: string (HH:MM format)
- **Behavior:**
  - Update device data with new settings.
  - Log changes in activity logs.
  - Redirect back to device control page or device list as needed.
- **Template Data:**
  - Device details including current status.
- **Notes:** Back to device list button included.

---

### 5. Automation Rules Page
- **Route:** `/automation`
- **Methods:**
  - GET: Show all automation rules.
  - POST: Add a new automation rule.
- **POST Form Data:**
  - `rule_name`: string
  - `trigger_type`: string (Time, Motion, Temperature)
  - `trigger_value`: string
  - `action_device_id`: integer/string
  - `action_type`: string (Turn On, Turn Off, Set Brightness, Set Temperature)
  - `action_value`: string (optional)
  - `enabled`: string boolean, typically 'true'
- **Behavior:**
  - Generate unique rule_id.
  - Save the rule.
  - Redirect back to automation page.
- **Template Data:**
  - List of automation rules for user.
- **Notes:** Back to dashboard button included.

---

### 6. Energy Report Page
- **Route:** `/energy`
- **Methods:**
  - GET: Display energy consumption data.
- **Query Params:**
  - Optional date filter: `date` in YYYY-MM-DD format
- **Description:**
  - Show summary total consumption and cost estimate.
  - Show energy consumption per device, filtered by date if provided.
- **Template Data:**
  - Energy summary totals.
  - List of energy logs for devices.
- **Notes:** Back to dashboard button included.

---

### 7. Activity Logs Page
- **Route:** `/activity`
- **Methods:**
  - GET: Show all activity logs.
- **Query Params:**
  - Optional search term: `search`
- **Description:**
  - Display logs filtered by optional search in action/details.
- **Template Data:**
  - Filtered list of activity logs.
- **Notes:** Back to dashboard button included.

---

# Summary
This design provides a clear, consistent data model with exact schemas in flat files to support all user and device data. Flask routes cover all pages with appropriate methods and parameters for CRUD operations and navigation flows as required. Backend implementation following this will enable the full SmartHomeManager app functionality as specified.

