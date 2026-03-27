import asyncio
import sys
import os
import time
import asyncio
from typing import List, Dict, Any
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from essential_modules import build_resilient_agent, execute, aggregate_task_metrics
from chaos import ChaosController

# Phase_info dictionary containing complete def blocks for failover context
Phase_info = {
    "phase1": "def design_specification_phase(\n    goal: str = \"Create complete design specification enabling independent backend and frontend development with all page and data schema details\",\n    collab_pattern_name: str = \"Sequential Flow\",\n    collab_pattern_description: str = (\n        \"SystemArchitect creates design_spec.md detailing Flask routes, HTML templates with element IDs, \"\n        \"and data schemas for all entities to enable parallel backend/frontend implementation.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"SystemArchitect\",\n            \"prompt\": \"\"\"You are a System Architect specializing in Flask web application design specifications.\n\nYour goal is to produce comprehensive design specifications that enable Backend and Frontend developers to work independently based on a single source of truth.\n\nTask Details:\n- Read user_task_description from CONTEXT\n- Produce design_spec.md covering three main areas:\n  • Flask routes including endpoints, HTTP methods, and function names for all pages\n  • HTML templates with exact element IDs, page titles, and navigation mappings using url_for\n  • Data schemas for all text data files with precise field order and pipe-delimited format\n- Ensure completeness: all pages, UI elements, and data entities described accurately\n- Do NOT assume or omit any page or schema specified in user_task_description\n\n**Section 1: Flask Routes Specification**\n\nDefine a route table listing for each:\n- Endpoint URL (e.g., /dashboard, /devices, /device/<int:device_id>)\n- HTTP Methods (GET, POST as appropriate)\n- Function names (snake_case, descriptive)\n- Template file names rendered\n- Context variables passed to templates with types (list, dict, str, int, bool, etc.)\n\nInclude:\n- Root route '/' redirects to dashboard\n- Routes for all pages and actions (e.g., adding device, control device, applying filters)\n- For dynamic routes, specify parameters clearly (e.g., device_id as int)\n\n**Section 2: HTML Templates Specification**\n\nFor each page template:\n- Filepath: templates/{template_name}.html\n- Exact Page Title (used in <title> and <h1>)\n- Full list of all required element IDs with their HTML types and purpose\n- Navigation mappings for buttons and links using url_for() with precise function names from Flask routes\n- Include dynamic element IDs (e.g., control-device-button-{device_id}) with pattern definitions\n\nRequirements:\n- Include all UI elements specified in user_task_description with exact IDs and labels\n- Maintain naming consistency with routes and context variables\n- Cover all pages: Dashboard, Device List, Add Device, Device Control, Automation Rules, Energy Report, Activity Logs\n\n**Section 3: Data File Schemas**\n\nFor each data file stored in data/ directory:\n- Filename and path (e.g., data/devices.txt)\n- Pipe-delimited field order matching specification exactly\n- Description of each field and its data type/format\n- Provide 2-3 realistic example lines\n- Emphasize no header line, parse strictly by field order\n\nFiles to specify include: users.txt, devices.txt, rooms.txt, automation_rules.txt, energy_logs.txt, activity_logs.txt\n\nCRITICAL SUCCESS CRITERIA:\n- Backend can implement full Flask routes and data handling solely from Sections 1 and 3\n- Frontend can implement all templates solely from Section 2\n- Element IDs, function names, and context variables are consistent and exact\n- No missing pages or UI elements\n- Data schemas accurately reflect field order and types as specified\n- Use write_text_file tool exclusively to output design_spec.md\n- Do NOT add any assumptions or features beyond user requirements\n\nOutput: design_spec.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"SystemArchitect\",\n            \"reviewer_agent\": \"BackendDeveloper\",\n            \"review_criteria\": (\n                \"Verify design_spec.md for backend completeness: all Flask routes with correct endpoints, HTTP methods, and function names; \"\n                \"accurate data schemas including all required fields with pipe delimiter and exact order; \"\n                \"correct route coverage for all pages specified.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        },\n        {\n            \"source_agent\": \"SystemArchitect\",\n            \"reviewer_agent\": \"FrontendDeveloper\",\n            \"review_criteria\": (\n                \"Verify design_spec.md for frontend completeness: HTML templates section with exact element IDs, page titles, button labels, and navigation mapping using url_for functions; \"\n                \"ensure all functional pages and UI elements are included and precisely described.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ]\n): pass",
    "phase2": "def parallel_implementation_phase(\n    goal: str = \"Implement backend and frontend components in parallel from design specification files\",\n    collab_pattern_name: str = \"Parallel Flow\",\n    collab_pattern_description: str = (\n        \"BackendDeveloper implements app.py with Flask routes and data handling modules per design_spec.md sections for Flask routes and data schemas. \"\n        \"FrontendDeveloper implements all HTML template files with specified element IDs, page titles, and navigation logic from the design_spec.md templates section. \"\n        \"Both agents work independently in parallel.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"BackendDeveloper\",\n            \"prompt\": \"\"\"You are a Backend Developer specializing in Flask web applications.\n\nYour goal is to implement a complete Flask backend application (app.py) including all routes and data file operations as specified by the design specification documents.\n\nTask Details:\n- Read design_spec.md sections for Flask routes and data schemas ONLY from CONTEXT\n- Implement all Flask routes with correct HTTP methods reflecting design_spec.md instructions\n- Load and save data from/to data/*.txt files according to exact field order in schemas\n- Ensure root route '/' redirects to the dashboard page\n- Do NOT read or assume frontend template implementation details or data formats not specified in data schemas\n- Do NOT modify design_spec.md or any templates\n\nImplementation Guidelines:\n1. Flask App Setup:\n   # ''' \n   # from flask import Flask, render_template, redirect, url_for, request\n   # app = Flask(__name__)\n   # app.config['SECRET_KEY'] = 'dev-secret-key'\n   # '''\n\n2. Root and Other Routes:\n   - Implement '/' route that redirects to dashboard using redirect(url_for('dashboard'))\n   - Implement all routes specified in design_spec.md with exact function names and parameters\n   - Use render_template() with template names from design_spec.md\n\n3. Data Loading:\n   - Read data from pipe-delimited text files in data/ directory using exact field order specified\n   - Parse lines with line.strip().split('|')\n   - Construct dictionaries reflecting field names and data types specified\n   - Handle file reading exceptions gracefully\n\n4. Route Handlers:\n   - Support GET and POST methods as per design_spec.md route definition\n   - Use request.form to handle POST data when needed\n   - Validate input data according to specification\n   - Return appropriate HTTP responses and render templates with correct context variables\n\n5. Code Practices:\n   - Use url_for for redirects and URL generation\n   - Maintain clear consistent function and variable names as per specification\n   - Include if __name__ == '__main__': app.run(debug=True, port=5000) block\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save app.py\n- Do NOT add extra routes or data outside design_spec.md specifications\n- Strictly adhere to data file formats and field orders\n- Function names and route paths must match design_spec.md exactly\n- Do NOT embed code snippets only in chat; write output files\n- Ensure root route redirects to dashboard page\n\nOutput: app.py\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"SystemArchitect\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"}\n            ]\n        },\n        {\n            \"agent_name\": \"FrontendDeveloper\",\n            \"prompt\": \"\"\"You are a Frontend Developer specializing in HTML and Jinja2 templating for Flask web applications.\n\nYour goal is to implement complete frontend HTML templates with all specified element IDs, page titles, UI controls, and navigation as described in the design specification documents.\n\nTask Details:\n- Read design_spec.md templates section ONLY from CONTEXT\n- Implement ALL HTML template files (*.html) with correct filenames and structure\n- Include all specified element IDs exactly as documented (case-sensitive)\n- Use Jinja2 templating syntax to render dynamic content based on provided context variables\n- Implement navigation using url_for() calls as specified for buttons and links\n- Do NOT read or modify backend route code or data schemas\n- Do NOT assume data formats beyond those specified in design_spec.md templates section\n\nImplementation Guidelines:\n1. Template Structure:\n   # '''\n   # <!DOCTYPE html>\n   # <html lang=\"en\">\n   # <head>\n   #     <meta charset=\"UTF-8\">\n   #     <title>Page Title from spec</title>\n   # </head>\n   # <body>\n   #     <div id=\"main-container-id\">\n   #         <h1>Page Title from spec</h1>\n   #         <!-- Page content with elements having specified IDs -->\n   #     </div>\n   # </body>\n   # </html>\n   # '''\n\n2. Element IDs:\n   - Implement all static and dynamic element IDs exactly, e.g., control-device-button-{device_id}\n   - Use Jinja2 syntax for dynamic IDs, e.g., id=\"control-device-button-{{ device.device_id }}\"\n\n3. Navigation:\n   - For buttons and links, wrap in <a href=\"{{ url_for('function_name') }}\"> or with parameters as needed\n   - Match function names for navigation exactly as in design_spec.md\n\n4. Forms and Controls:\n   - For forms, use method=\"POST\" and action with url_for as specified\n   - Include all input fields, dropdowns, buttons with specified IDs\n   - Use proper names for input fields matching backend expectations\n\n5. Consistency:\n   - Page titles must match design_spec.md exactly both in <title> and main <h1> tags\n   - All UI controls must be included and correctly labeled\n   - Use proper indentation and valid HTML5/Jinja2 syntax\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save template files in templates/ directory\n- Each template file must be named exactly as specified\n- Do NOT add extra UI elements beyond specification\n- Do NOT provide partial code snippets only in chat\n- Ensure all navigation links use url_for with correct function names and parameters\n- All element IDs must match specification exactly (case-sensitive)\n\nOutput: templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"SystemArchitect\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"BackendDeveloper\",\n            \"reviewer_agent\": \"SystemArchitect\",\n            \"review_criteria\": (\n                \"Confirm app.py implements all specified Flask routes and handles data files exactly as defined; \"\n                \"validate route accessibility, correct HTTP methods, data field order, and root route redirects to dashboard page.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\"}\n            ]\n        },\n        {\n            \"source_agent\": \"FrontendDeveloper\",\n            \"reviewer_agent\": \"SystemArchitect\",\n            \"review_criteria\": (\n                \"Confirm all templates/*.html have exact element IDs, match page titles from spec, \"\n                \"contain correct navigation links with url_for, and include all specified UI controls.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ]\n): pass",
}

user_task = """
# Requirements Document for 'SmartHomeManager' Web Application

## 1. Objective
Develop a comprehensive web application named 'SmartHomeManager' using Python, with data managed through local text files. The application enables users to manage smart home devices, control them remotely, set automation rules, and monitor energy consumption. Note that the website should start from the Dashboard page.

## 2. Language
The required development language for the 'SmartHomeManager' application is Python.

## 3. Page Design

The 'SmartHomeManager' web application will consist of the following seven pages:

### 1. Dashboard Page
- **Page Title**: Smart Home Dashboard
- **Overview**: The main hub displaying overview of all devices, quick controls, and navigation to all functionality.
- **Elements**:
  - **ID: dashboard-page** - Type: Div - Container for the dashboard page.
  - **ID: device-summary** - Type: Div - Summary showing total devices, active devices, and offline devices count.
  - **ID: device-list-button** - Type: Button - Button to navigate to device list page.
  - **ID: add-device-button** - Type: Button - Button to navigate to add device page.
  - **ID: automation-button** - Type: Button - Button to navigate to automation rules page.
  - **ID: energy-button** - Type: Button - Button to navigate to energy report page.
  - **ID: activity-button** - Type: Button - Button to navigate to activity logs page.
  - **ID: room-list** - Type: Div - List of all rooms with device counts, displayed as a dashboard section.

### 2. Device List Page
- **Page Title**: My Devices
- **Overview**: A page displaying all registered smart devices with their status and quick controls.
- **Elements**:
  - **ID: device-list-page** - Type: Div - Container for the device list page.
  - **ID: device-table** - Type: Table - Table displaying all devices with name, type, room, status, and actions.
  - **ID: control-device-button-{device_id}** - Type: Button - Button to navigate to device control page (each row has this button).
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 3. Add Device Page
- **Page Title**: Add New Device
- **Overview**: A page for users to register a new smart device.
- **Elements**:
  - **ID: add-device-page** - Type: Div - Container for the add device page.
  - **ID: device-name** - Type: Input - Field to input device name.
  - **ID: device-type** - Type: Dropdown - Dropdown to select device type (Light, Thermostat, Camera, Lock, Sensor, Appliance).
  - **ID: device-room** - Type: Dropdown - Dropdown to select room (Living Room, Bedroom, Kitchen, Bathroom, Garage).
  - **ID: submit-device-button** - Type: Button - Button to submit the new device.
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 4. Device Control Page
- **Page Title**: Device Control
- **Overview**: A page for controlling a specific device with detailed settings.
- **Elements**:
  - **ID: device-control-page** - Type: Div - Container for the device control page.
  - **ID: device-name-display** - Type: H2 - Display device name.
  - **ID: device-status-display** - Type: Div - Display current device status (Online/Offline).
  - **ID: power-toggle** - Type: Button - Button to toggle device power on/off.
  - **ID: save-settings-button** - Type: Button - Button to save device settings.
  - **ID: back-to-devices** - Type: Button - Button to navigate back to device list.

### 5. Automation Rules Page
- **Page Title**: Automation Rules
- **Overview**: A page for creating and managing automation rules for devices.
- **Elements**:
  - **ID: automation-page** - Type: Div - Container for the automation rules page.
  - **ID: rules-table** - Type: Table - Table displaying all automation rules with name, trigger, action, and status.
  - **ID: rule-name** - Type: Input - Field to input rule name.
  - **ID: trigger-type** - Type: Dropdown - Dropdown to select trigger type (Time, Motion, Temperature).
  - **ID: trigger-value** - Type: Input - Field to input trigger value (e.g., time or threshold).
  - **ID: action-device** - Type: Dropdown - Dropdown to select target device.
  - **ID: action-type** - Type: Dropdown - Dropdown to select action type (Turn On, Turn Off, Set Brightness, Set Temperature).
  - **ID: add-rule-button** - Type: Button - Button to add new automation rule.
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 6. Energy Report Page
- **Page Title**: Energy Report
- **Overview**: A page displaying energy consumption data and statistics for all devices.
- **Elements**:
  - **ID: energy-page** - Type: Div - Container for the energy report page.
  - **ID: energy-summary** - Type: Div - Summary showing total energy consumption and cost estimate.
  - **ID: energy-table** - Type: Table - Table displaying energy consumption per device with date and kWh.
  - **ID: date-filter** - Type: Input (date) - Field to filter energy data by date.
  - **ID: apply-filter-button** - Type: Button - Button to apply date filter.
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 7. Activity Logs Page
- **Page Title**: Activity Logs
- **Overview**: A page displaying all device activity logs and system events.
- **Elements**:
  - **ID: activity-page** - Type: Div - Container for the activity logs page.
  - **ID: activity-table** - Type: Table - Table displaying activity logs with timestamp, device, action, and details.
  - **ID: search-activity** - Type: Input - Field to search activity logs.
  - **ID: apply-search-button** - Type: Button - Button to apply search filter.
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

## 4. Data Storage

The 'SmartHomeManager' application will store data locally in text files organized in the directory 'data'. The following data formats and examples are defined:

### 1. User Data
- **File Name**: `users.txt`
- **Data Format**:
  ```
  username|email
  ```
- **Example Data**:
  ```
  john_doe|john@example.com
  jane_smith|jane@example.com
  ```

### 2. Device Data
- **File Name**: `devices.txt`
- **Data Format**:
  ```
  username|device_id|device_name|device_type|room|brand|model|status|power|brightness|temperature|mode|schedule_time
  ```
- **Example Data**:
  ```
  john_doe|1|Living Room Light|Light|Living Room|Philips|Hue|Online|on|75|||Auto|
  john_doe|2|Bedroom Thermostat|Thermostat|Bedroom|Nest|Learning|Online|on||72|Auto|22:00
  jane_smith|3|Kitchen Camera|Camera|Kitchen|Ring|Indoor|Online|on||||Manual|
  ```

### 3. Room Data
- **File Name**: `rooms.txt`
- **Data Format**:
  ```
  username|room_id|room_name
  ```
- **Example Data**:
  ```
  john_doe|1|Living Room
  john_doe|2|Bedroom
  john_doe|3|Kitchen
  jane_smith|1|Living Room
  ```

### 4. Automation Rules Data
- **File Name**: `automation_rules.txt`
- **Data Format**:
  ```
  username|rule_id|rule_name|trigger_type|trigger_value|action_device_id|action_type|action_value|enabled
  ```
- **Example Data**:
  ```
  john_doe|1|Morning Lights|Time|07:00|1|Turn On||true
  john_doe|2|Night Mode|Time|22:00|1|Set Brightness|20|true
  jane_smith|1|Motion Alert|Motion|detected|3|Turn On||true
  ```

### 5. Energy Consumption Logs
- **File Name**: `energy_logs.txt`
- **Data Format**:
  ```
  username|device_id|date|consumption_kwh
  ```
- **Example Data**:
  ```
  john_doe|1|2024-11-01|0.5
  john_doe|2|2024-11-01|2.3
  john_doe|1|2024-11-02|0.6
  jane_smith|3|2024-11-01|0.2
  ```

### 6. Activity Logs
- **File Name**: `activity_logs.txt`
- **Data Format**:
  ```
  username|timestamp|device_id|action|details
  ```
- **Example Data**:
  ```
  john_doe|2024-11-01 07:00:00|1|Power On|Automation triggered: Morning Lights
  john_doe|2024-11-01 08:30:00|2|Settings Changed|Temperature set to 72
  jane_smith|2024-11-01 09:15:00|3|Power On|Manual control
  ```

All files will be saved in the `data` directory to ensure organization and easy access. The format uses a pipe (`|`) delimiter for better readability and parsing. Different types of data will be isolated to ensure efficient data management and retrieval.
"""

CONTEXT = {
    "_metrics": {},  # Metrics tracking for all agents
    "user_task_description": [{
        "timestamp": time.time(),
        "agent_name": "user",
        "content": user_task
    }]
}

AGENT_PROFILES = {
    "SystemArchitect": {
        "prompt": (
            """You are a System Architect specializing in Flask web application design specifications.

Your goal is to produce comprehensive design specifications that enable Backend and Frontend developers to work independently based on a single source of truth.

Task Details:
- Read user_task_description from CONTEXT
- Produce design_spec.md covering three main areas:
  • Flask routes including endpoints, HTTP methods, and function names for all pages
  • HTML templates with exact element IDs, page titles, and navigation mappings using url_for
  • Data schemas for all text data files with precise field order and pipe-delimited format
- Ensure completeness: all pages, UI elements, and data entities described accurately
- Do NOT assume or omit any page or schema specified in user_task_description

**Section 1: Flask Routes Specification**

Define a route table listing for each:
- Endpoint URL (e.g., /dashboard, /devices, /device/<int:device_id>)
- HTTP Methods (GET, POST as appropriate)
- Function names (snake_case, descriptive)
- Template file names rendered
- Context variables passed to templates with types (list, dict, str, int, bool, etc.)

Include:
- Root route '/' redirects to dashboard
- Routes for all pages and actions (e.g., adding device, control device, applying filters)
- For dynamic routes, specify parameters clearly (e.g., device_id as int)

**Section 2: HTML Templates Specification**

For each page template:
- Filepath: templates/{template_name}.html
- Exact Page Title (used in <title> and <h1>)
- Full list of all required element IDs with their HTML types and purpose
- Navigation mappings for buttons and links using url_for() with precise function names from Flask routes
- Include dynamic element IDs (e.g., control-device-button-{device_id}) with pattern definitions

Requirements:
- Include all UI elements specified in user_task_description with exact IDs and labels
- Maintain naming consistency with routes and context variables
- Cover all pages: Dashboard, Device List, Add Device, Device Control, Automation Rules, Energy Report, Activity Logs

**Section 3: Data File Schemas**

For each data file stored in data/ directory:
- Filename and path (e.g., data/devices.txt)
- Pipe-delimited field order matching specification exactly
- Description of each field and its data type/format
- Provide 2-3 realistic example lines
- Emphasize no header line, parse strictly by field order

Files to specify include: users.txt, devices.txt, rooms.txt, automation_rules.txt, energy_logs.txt, activity_logs.txt

CRITICAL SUCCESS CRITERIA:
- Backend can implement full Flask routes and data handling solely from Sections 1 and 3
- Frontend can implement all templates solely from Section 2
- Element IDs, function names, and context variables are consistent and exact
- No missing pages or UI elements
- Data schemas accurately reflect field order and types as specified
- Use write_text_file tool exclusively to output design_spec.md
- Do NOT add any assumptions or features beyond user requirements

Output: design_spec.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_spec.md'}],
    },

    "BackendDeveloper": {
        "prompt": (
            """You are a Backend Developer specializing in Flask web applications.

Your goal is to implement a complete Flask backend application (app.py) including all routes and data file operations as specified by the design specification documents.

Task Details:
- Read design_spec.md sections for Flask routes and data schemas ONLY from CONTEXT
- Implement all Flask routes with correct HTTP methods reflecting design_spec.md instructions
- Load and save data from/to data/*.txt files according to exact field order in schemas
- Ensure root route '/' redirects to the dashboard page
- Do NOT read or assume frontend template implementation details or data formats not specified in data schemas
- Do NOT modify design_spec.md or any templates

Implementation Guidelines:
1. Flask App Setup:
   # ''' 
   # from flask import Flask, render_template, redirect, url_for, request
   # app = Flask(__name__)
   # app.config['SECRET_KEY'] = 'dev-secret-key'
   # '''

2. Root and Other Routes:
   - Implement '/' route that redirects to dashboard using redirect(url_for('dashboard'))
   - Implement all routes specified in design_spec.md with exact function names and parameters
   - Use render_template() with template names from design_spec.md

3. Data Loading:
   - Read data from pipe-delimited text files in data/ directory using exact field order specified
   - Parse lines with line.strip().split('|')
   - Construct dictionaries reflecting field names and data types specified
   - Handle file reading exceptions gracefully

4. Route Handlers:
   - Support GET and POST methods as per design_spec.md route definition
   - Use request.form to handle POST data when needed
   - Validate input data according to specification
   - Return appropriate HTTP responses and render templates with correct context variables

5. Code Practices:
   - Use url_for for redirects and URL generation
   - Maintain clear consistent function and variable names as per specification
   - Include if __name__ == '__main__': app.run(debug=True, port=5000) block

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save app.py
- Do NOT add extra routes or data outside design_spec.md specifications
- Strictly adhere to data file formats and field orders
- Function names and route paths must match design_spec.md exactly
- Do NOT embed code snippets only in chat; write output files
- Ensure root route redirects to dashboard page

Output: app.py"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'SystemArchitect'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}],
    },

    "FrontendDeveloper": {
        "prompt": (
            """You are a Frontend Developer specializing in HTML and Jinja2 templating for Flask web applications.

Your goal is to implement complete frontend HTML templates with all specified element IDs, page titles, UI controls, and navigation as described in the design specification documents.

Task Details:
- Read design_spec.md templates section ONLY from CONTEXT
- Implement ALL HTML template files (*.html) with correct filenames and structure
- Include all specified element IDs exactly as documented (case-sensitive)
- Use Jinja2 templating syntax to render dynamic content based on provided context variables
- Implement navigation using url_for() calls as specified for buttons and links
- Do NOT read or modify backend route code or data schemas
- Do NOT assume data formats beyond those specified in design_spec.md templates section

Implementation Guidelines:
1. Template Structure:
   # '''
   # <!DOCTYPE html>
   # <html lang="en">
   # <head>
   #     <meta charset="UTF-8">
   #     <title>Page Title from spec</title>
   # </head>
   # <body>
   #     <div id="main-container-id">
   #         <h1>Page Title from spec</h1>
   #         <!-- Page content with elements having specified IDs -->
   #     </div>
   # </body>
   # </html>
   # '''

2. Element IDs:
   - Implement all static and dynamic element IDs exactly, e.g., control-device-button-{device_id}
   - Use Jinja2 syntax for dynamic IDs, e.g., id="control-device-button-{{ device.device_id }}"

3. Navigation:
   - For buttons and links, wrap in <a href="{{ url_for('function_name') }}"> or with parameters as needed
   - Match function names for navigation exactly as in design_spec.md

4. Forms and Controls:
   - For forms, use method="POST" and action with url_for as specified
   - Include all input fields, dropdowns, buttons with specified IDs
   - Use proper names for input fields matching backend expectations

5. Consistency:
   - Page titles must match design_spec.md exactly both in <title> and main <h1> tags
   - All UI controls must be included and correctly labeled
   - Use proper indentation and valid HTML5/Jinja2 syntax

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save template files in templates/ directory
- Each template file must be named exactly as specified
- Do NOT add extra UI elements beyond specification
- Do NOT provide partial code snippets only in chat
- Ensure all navigation links use url_for with correct function names and parameters
- All element IDs must match specification exactly (case-sensitive)

Output: templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'SystemArchitect'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'templates/*.html'}],
    }

}

REVIEW_PROFILES = {
    'SystemArchitect': [
        ("BackendDeveloper", """Verify design_spec.md for backend completeness: all Flask routes with correct endpoints, HTTP methods, and function names; "
                "accurate data schemas including all required fields with pipe delimiter and exact order; "
                "correct route coverage for all pages specified.""", [{'type': 'user', 'name': 'user_task_description'}, {'type': 'text_file', 'name': 'design_spec.md'}]),
        ("FrontendDeveloper", """Verify design_spec.md for frontend completeness: HTML templates section with exact element IDs, page titles, button labels, and navigation mapping using url_for functions; "
                "ensure all functional pages and UI elements are included and precisely described.""", [{'type': 'user', 'name': 'user_task_description'}, {'type': 'text_file', 'name': 'design_spec.md'}])
    ],

    'BackendDeveloper': [
        ("SystemArchitect", """Confirm app.py implements all specified Flask routes and handles data files exactly as defined; "
                "validate route accessibility, correct HTTP methods, data field order, and root route redirects to dashboard page.""", [{'type': 'text_file', 'name': 'design_spec.md'}, {'type': 'text_file', 'name': 'app.py'}])
    ],

    'FrontendDeveloper': [
        ("SystemArchitect", """Confirm all templates/*.html have exact element IDs, match page titles from spec, "
                "contain correct navigation links with url_for, and include all specified UI controls.""", [{'type': 'text_file', 'name': 'design_spec.md'}, {'type': 'text_file', 'name': 'templates/*.html'}])
    ]

}




# ==================== Compound Chaos Controller Setup ====================
import random
from chaos.injectors import ChaosMode

# Compound Chaos: Per-task sampling
COMPOUND_CONFIG = {
    "agent_intensity": random.choice([0.2, 0.3, 0.4, 0.5, 0.6]),
    "prompt_method": random.choice(["WORD_SHUFFLE", "WORD_DELETION", "WORD_REPLACEMENT"]),
    "io_method": random.choice(["WORD_SHUFFLE", "WORD_DELETION", "WORD_REPLACEMENT"]),
    "prompt_probability": 0.2,
    "io_probability": 0.2
}

# ChaosMode mapping
MODE_MAP = {
    "WORD_SHUFFLE": ChaosMode.WORD_SHUFFLE,
    "WORD_DELETION": ChaosMode.WORD_DELETION,
    "WORD_REPLACEMENT": ChaosMode.WORD_REPLACEMENT,
}

chaos_controller = ChaosController(
    agent_chaos_enabled=True,
    stress_chaos_enabled=True,
    stress_chaos_mode=MODE_MAP[COMPOUND_CONFIG["prompt_method"]],
    io_chaos_enabled=True,
    io_chaos_mode=MODE_MAP[COMPOUND_CONFIG["io_method"]],
    target_agent_names=list(AGENT_PROFILES.keys())
)

# Agent chaos is sampled with intensity
chaos_controller.start_experiment(
    running_agents=list(AGENT_PROFILES.keys()),
    agent_profiles=AGENT_PROFILES,
    probability=COMPOUND_CONFIG["agent_intensity"]
)

# Prompt/IO separately sampled at 0.2 probability (reset)
all_agents = list(AGENT_PROFILES.keys())
chaos_controller.stress_chaos_targets = [a for a in all_agents if random.random() < COMPOUND_CONFIG["prompt_probability"]]
chaos_controller.io_chaos_targets = [a for a in all_agents if random.random() < COMPOUND_CONFIG["io_probability"]]

# Guarantee at least 1
if not chaos_controller.stress_chaos_targets:
    chaos_controller.stress_chaos_targets = [random.choice(all_agents)]
if not chaos_controller.io_chaos_targets:
    chaos_controller.io_chaos_targets = [random.choice(all_agents)]

# Save chaos configuration to file for debugging
from datetime import datetime
import json

chaos_config_data = {
    "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    "scenario": "compound_chaos",
    "compound_config": COMPOUND_CONFIG,
    "enabled_chaos_types": {
        "agent_chaos": chaos_controller.agent_chaos.enabled,
        "stress_chaos": chaos_controller.stress_chaos.enabled,
        "io_chaos": chaos_controller.io_chaos.enabled
    },
    "targets": {
        "agent_chaos_targets": chaos_controller.agent_chaos_targets,
        "stress_chaos_targets": chaos_controller.stress_chaos_targets,
        "io_chaos_targets": chaos_controller.io_chaos_targets
    },
    "registered_files": dict(chaos_controller.agent_file_registry)
}

with open("chaos_config.json", "w") as f:
    json.dump(chaos_config_data, f, indent=2)

print(f"Compound Chaos activated: Agent={COMPOUND_CONFIG['agent_intensity']}, Prompt={COMPOUND_CONFIG['prompt_method']}, IO={COMPOUND_CONFIG['io_method']}")
print(f"Chaos configuration saved to: chaos_config.json")
# ================================================================

# Orchestration Functions
async def design_specification_phase():
    # Create SystemArchitect agent
    SystemArchitect = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="SystemArchitect",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=2,
        timeout_threshold=150,
        failure_threshold=1,
        recovery_time=30
    )

    # Execute SystemArchitect
    await execute(SystemArchitect, "Create design_spec.md detailing Flask routes, HTML templates with element IDs, and data schemas as specified")
# Phase1_End

# Phase2_Start
import asyncio

async def parallel_implementation_phase():
    # Create agents
    BackendDeveloper = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="BackendDeveloper",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=3,
        timeout_threshold=180,
        failure_threshold=1,
        recovery_time=40
    )
    FrontendDeveloper = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="FrontendDeveloper",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=3,
        timeout_threshold=160,
        failure_threshold=1,
        recovery_time=40
    )

    # Execute agents in parallel
    await asyncio.gather(
        execute(BackendDeveloper, "Implement app.py with Flask routes and data handling modules per design_spec.md"),
        execute(FrontendDeveloper, "Implement all HTML templates with specified element IDs, page titles, and navigation logic from design_spec.md")
    )
# Phase2_End

# Orchestrate_Start

async def orchestrate():
    """Execute the complete multi-agent workflow in steps."""
    import time
    import json
    from pathlib import Path
    from essential_modules import aggregate_task_metrics
    orchestrate_start_time = time.time()

    step1 = [
        design_specification_phase()
    ]
    step2 = [
        parallel_implementation_phase()
    ]

    await asyncio.gather(*step1)
    await asyncio.gather(*step2)

    # Record task duration
    orchestrate_end_time = time.time()
    CONTEXT["_task_duration"] = orchestrate_end_time - orchestrate_start_time

    # Print chaos engineering report (if enabled)
    if 'chaos_controller' in globals():
        print("\n" + "="*80)
        print("Chaos Engineering Report")
        print("="*80)
        chaos_controller.print_report(context=CONTEXT)

    # Save metrics to JSON
    task_metrics = aggregate_task_metrics(CONTEXT)
    metrics_path = Path("metrics.json")
    with open(metrics_path, "w") as f:
        json.dump(task_metrics, f, indent=2)
    print(f" Metrics saved to: {{metrics_path.resolve()}}")
# Orchestrate_End

if __name__ == "__main__":
    import sys
    import signal
    from datetime import datetime
    from pathlib import Path
    import json

    # Signal handler for graceful shutdown on timeout
    def save_metrics_on_signal(signum, frame):
        print(f"\n  Received signal {signum}, saving metrics before exit...")
        try:
            task_metrics = aggregate_task_metrics(CONTEXT)
            metrics_path = Path("metrics.json")
            with open(metrics_path, "w") as f:
                json.dump(task_metrics, f, indent=2)
            print(f"Metrics saved to: {metrics_path.resolve()}")
        except Exception as e:
            print(f"Error saving metrics: {e}")
        sys.exit(1)

    # Register signal handlers
    signal.signal(signal.SIGTERM, save_metrics_on_signal)
    signal.signal(signal.SIGINT, save_metrics_on_signal)

    # Open log file for real-time stdout/stderr capture
    log_file = open("execution_log.txt", "w", encoding="utf-8")

    # Write header
    log_file.write("=== Execution Log ===\n")
    log_file.write(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    log_file.write("\n=== OUTPUT ===\n")
    log_file.flush()

    # Create a Tee class to write to both stdout and file
    class Tee:
        def __init__(self, *files):
            self.files = files
        def write(self, data):
            for f in self.files:
                f.write(data)
                f.flush()
        def flush(self):
            for f in self.files:
                f.flush()

    # Redirect stdout and stderr to both console and log file
    original_stdout = sys.stdout
    original_stderr = sys.stderr
    sys.stdout = Tee(original_stdout, log_file)
    sys.stderr = Tee(original_stderr, log_file)

    try:
        # Run orchestration
        asyncio.run(orchestrate())
    finally:
        # Restore original stdout/stderr
        sys.stdout = original_stdout
        sys.stderr = original_stderr

        # Write summary
        log_file.write(f"\n\n=== Summary ===\n")
        log_file.write(f"End Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        log_file.close()
