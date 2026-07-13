import asyncio
import sys
import os
import time
import asyncio
from typing import List, Dict, Any
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
import essential_modules
from essential_modules import build_resilient_agent, execute, aggregate_task_metrics
from chaos import ChaosController
# 20260714_001750_208033/main_20260714_001750_208033.py

# Phase_info dictionary containing complete def blocks for failover context
Phase_info = {
    "phase1": "def design_specification_phase(\n    goal: str = \"Create complementary backend and frontend design specifications for SmartHomeManager and merge them into one consistent design_spec.md\",\n    collab_pattern_name: str = \"Parallel + Merger\",\n    collab_pattern_description: str = (\n        \"BackendDesignArchitect and FrontendDesignArchitect independently produce backend_design.md and frontend_design.md respectively \"\n        \"based on the user task description. DesignMerger consumes both designs plus the original user task description, \"\n        \"reconciles them, and produces the merged design_spec.md.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"BackendDesignArchitect\",\n            \"prompt\": \"\"\"You are a System Architect specializing in backend design for Flask web applications managing smart home systems.\n\nYour goal is to create a backend design specification that describes data models and Flask routes to manage devices, automation, energy reports, and activity logs for the SmartHomeManager application.\n\nTask Details:\n- Read user_task_description from CONTEXT\n- Independently create backend_design.md\n- Specify all backend data schemas, file storage formats, and Flask route designs\n- Do not rely on or read frontend_design.md\n\n**Section 1: Data Models and File Formats**\n- Specify all required data files with exact file names and pipe-delimited field schemas\n- Include detailed field descriptions, data types, and example records\n- Ensure data model supports users, devices, rooms, automation rules, energy logs, and activity logs as per user specifications\n- Use the exact 'data' directory and text file conventions described\n\n**Section 2: Flask Route Specifications**\n- Define routes for managing all pages: dashboard, device list, add device, device control, automation rules, energy reports, and activity logs\n- Specify HTTP methods, URL paths, expected query or form parameters, and route handler responsibilities\n- Include notes on data passed to templates or expected user interactions\n- Routes must align with the data models and support complete CRUD and navigation flows\n\nCRITICAL SUCCESS CRITERIA:\n- Your backend_design.md enables backend developers to implement app.py with full support for all functional requirements\n- Use write_text_file tool to output backend_design.md\n- Follow all naming and format conventions strictly—no additions beyond user_task_description inputs\n- Write only the declared output artifact without refinement markers\n\nOutput: backend_design.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"backend_design.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"FrontendDesignArchitect\",\n            \"prompt\": \"\"\"You are a System Architect specializing in HTML and Jinja2 template frontend design for Flask web applications.\n\nYour goal is to create a frontend design specification that describes the HTML page structure, element IDs, UI components, and navigation flows for the seven SmartHomeManager application pages.\n\nTask Details:\n- Read user_task_description from CONTEXT\n- Independently create frontend_design.md\n- Specify HTML page templates for dashboard, device list, add device, device control, automation rules, energy report, and activity logs\n- List all element IDs with their types and descriptions exactly as specified in the user requirements\n- Define navigation buttons and links including their target pages and expected behaviors\n- Do not rely on or read backend_design.md\n\n**Section 1: HTML Template Structure**\n- For each page, specify filename and exact page title\n- List container Div IDs and named UI components with their element types\n- Define dynamic elements like tables, buttons, inputs, dropdowns by ID and purpose\n\n**Section 2: Navigation and Button Definitions**\n- Map navigation controls such as buttons to their target pages (e.g., device-list-button navigates to device list page)\n- Specify button IDs with action descriptions and target routes consistent with user navigation requirements\n- Include form submission buttons and back-navigation buttons with expected behaviors\n\nCRITICAL SUCCESS CRITERIA:\n- Frontend developers can implement all templates/*.html files fully from frontend_design.md\n- The design covers all UI elements and navigation flows exactly as per user specification\n- Use write_text_file tool to output frontend_design.md\n- Write only the declared output artifact without refinement markers\n\nOutput: frontend_design.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"frontend_design.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"DesignMerger\",\n            \"prompt\": \"\"\"You are a System Architect specializing in synthesizing backend and frontend design specifications for Flask web applications.\n\nYour goal is to merge backend_design.md and frontend_design.md into a single design_spec.md artifact that is internally consistent and complete according to the SmartHomeManager user requirements.\n\nTask Details:\n- Read user_task_description, backend_design.md, and frontend_design.md from CONTEXT\n- Reconcile the backend and frontend specifications for data schema and interface consistency\n- Resolve any inconsistencies in route naming, data variable naming, and navigation flows\n- Create a coherent design_spec.md combining sections from both input artifacts without introducing new requirements\n\n**Section 1: Backend Specifications**\n- Integrate backend data models and Flask route definitions\n- Ensure data file formats and schemas match expected frontend data usage\n\n**Section 2: Frontend Specifications**\n- Include complete HTML template structure, element IDs, and UI component definitions\n- Ensure navigation buttons and page flows align with backend route specifications\n\n**Section 3: Consistency and Completeness Checks**\n- Validate that all backend routes correspond to frontend navigation controls\n- Confirm that all data models have corresponding UI elements and that all user requirements are fully covered\n\nCRITICAL SUCCESS CRITERIA:\n- The resulting design_spec.md fully enables developers to implement both backend app.py and frontend templates/*.html\n- No missing requirements or contradictions remain between backend and frontend\n- Use write_text_file tool to output design_spec.md\n- Write only the declared output artifact without refinement markers\n\nOutput: design_spec.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"backend_design.md\", \"source\": \"BackendDesignArchitect\"},\n                {\"type\": \"text_file\", \"name\": \"frontend_design.md\", \"source\": \"FrontendDesignArchitect\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"BackendDesignArchitect\",\n            \"reviewer_agent\": \"DesignMerger\",\n            \"review_criteria\": \"Verify backend design completeness and conformance with user requirements and frontend design.\",\n            \"review_artifacts\": [{\"type\": \"text_file\", \"name\": \"backend_design.md\"}]\n        },\n        {\n            \"source_agent\": \"FrontendDesignArchitect\",\n            \"reviewer_agent\": \"DesignMerger\",\n            \"review_criteria\": \"Verify frontend design completeness and conformance with user requirements and backend design.\",\n            \"review_artifacts\": [{\"type\": \"text_file\", \"name\": \"frontend_design.md\"}]\n        }\n    ]\n): pass",
    "phase2": "def implementation_and_verification_phase(\n    goal: str = \"Independently implement backend app.py and frontend templates then integrate them into the final runnable application\",\n    collab_pattern_name: str = \"Parallel + Merger\",\n    collab_pattern_description: str = (\n        \"BackendDeveloper and FrontendDeveloper independently implement backend app.py and frontend templates/*.html respectively from design_spec.md. \"\n        \"IntegrationMerger reconciles their outputs, ensures interface consistency, and produces the final app.py and templates/*.html.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"BackendDeveloper\",\n            \"prompt\": \"\"\"You are a Backend Developer specializing in Flask web applications using Python.\n\nYour goal is to implement the complete Flask backend application as a runnable app.py based on the provided design_spec.md, handling all routing, business logic, and data file interactions for a smart home management system.\n\nTask Details:\n- Read design_spec.md from CONTEXT, focusing on Sections detailing Flask routes, data schemas, and business rules\n- Independently create app.py implementing all Flask routes, request handlers, data reads/writes to local text files, and application logic\n- Output a single runnable app.py that does not depend on any sibling agent output artifacts\n\n**Implementation Requirements:**\n- Implement Flask routes exactly as specified, including URLs, methods, and expected context variables\n- Integrate with local text files in the 'data' directory using prescribed data formats and delimiters\n- Handle user sessions, device management, automation rules, energy and activity logs as outlined\n- Ensure code readability with appropriate comments using only single-quote docstrings or inline hash comments\n- Include error handling for file accesses and input validations\n\n**Output and Tool Usage:**\n- Use the write_text_file tool to save the fully implemented app.py\n- The app.py must be runnable and self-contained based on design_spec.md contents only\n- Do not read or require any frontend template files or sibling agent outputs\n\nCRITICAL SUCCESS CRITERIA:\n- app.py runs successfully implementing all backend logic defined in design_spec.md\n- Data storage and retrieval conform to specified text file formats\n- Routes and function names are consistent with frontend expectations from design_spec.md\n\nOutput: app.py\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"}\n            ]\n        },\n        {\n            \"agent_name\": \"FrontendDeveloper\",\n            \"prompt\": \"\"\"You are a Frontend Developer specializing in HTML and Jinja2 template development for Flask web applications.\n\nYour goal is to develop complete, well-structured HTML templates (*.html) with the specified element IDs and UI layout for all specified pages, based solely on the design_spec.md.\n\nTask Details:\n- Read design_spec.md from CONTEXT focusing on all page and template specifications, element IDs, and navigation requirements\n- Independently create all required templates/*.html files for the seven defined pages:\n  Dashboard, Device List, Add Device, Device Control, Automation Rules, Energy Report, Activity Logs\n- Ensure each page has correct container divs, input fields, buttons, and tables with exact element IDs\n- Use Jinja2 templating syntax where applicable for dynamic content placeholders and control structures\n\n**Template Development Instructions:**\n- Use semantic HTML5 elements and accessible markup\n- Include all buttons and links with specified IDs for front-to-back navigation\n- Incorporate placeholders for context variables as per design_spec.md\n- Validate IDs are unique per page; no cross-page ID duplication\n- Comment code using single-quote docstrings or hash comments only\n\n**Output and Tool Usage:**\n- Use write_text_file tool to output all HTML templates in templates/*.html\n- Templates must form a cohesive frontend consistent with backend routes and context variables from design_spec.md\n- Do not read backend source files or sibling agent outputs\n\nCRITICAL SUCCESS CRITERIA:\n- All seven pages implemented with exact element IDs and layout as per design_spec.md\n- Templates fully compatible with Flask backend implementation\n- Output includes only declared templates/*.html files\n\nOutput: templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        },\n        {\n            \"agent_name\": \"IntegrationMerger\",\n            \"prompt\": \"\"\"You are a Software Integration Engineer specializing in full-stack Flask web application delivery.\n\nYour goal is to integrate the independently developed backend app.py and frontend templates/*.html into a final consistent, runnable application that fully satisfies design_spec.md.\n\nTask Details:\n- Read design_spec.md, app.py, and templates/*.html from CONTEXT\n- Verify backend routes and data handling in app.py match frontend templates and context variables exactly as specified\n- Reconcile any interface discrepancies between backend and frontend artifacts\n- Ensure navigation, page titles, element IDs, and data bindings are consistent and complete\n- Produce final versions of app.py and templates/*.html that are fully compatible and ready for deployment\n\n**Integration and Validation Instructions:**\n- Compare route names, HTTP methods, and expected template files in app.py against frontend templates\n- Confirm all dynamic data fields referenced in templates are provided by backend context\n- Validate element ID correctness and unique usage across templates\n- Refactor minor inconsistencies without adding or removing features beyond design_spec.md\n- Document key integration decisions and list any assumptions in comments using single-quote docstrings or hash comments\n\n**Output and Tool Usage:**\n- Use write_text_file tool to output merged app.py and complete templates/*.html\n- Do not produce additional artifacts or refinement markers\n- Final output must be deployable and consistent with all input artifacts and user task requirements\n\nCRITICAL SUCCESS CRITERIA:\n- Backend and frontend are fully integrated and interface consistent per design_spec.md\n- Final app.py and templates/*.html can be deployed as a working SmartHomeManager application\n- All review feedback from IntegrationMerger policy has been addressed\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"BackendDeveloper\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"FrontendDeveloper\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"BackendDeveloper\",\n            \"reviewer_agent\": \"IntegrationMerger\",\n            \"review_criteria\": \"Verify backend implementation code for correctness, completeness, and adherence to design_spec.md.\",\n            \"review_artifacts\": [{\"type\": \"text_file\", \"name\": \"app.py\"}]\n        },\n        {\n            \"source_agent\": \"FrontendDeveloper\",\n            \"reviewer_agent\": \"IntegrationMerger\",\n            \"review_criteria\": \"Verify frontend templates correctness, element ID accuracy, and conformance to design_spec.md.\",\n            \"review_artifacts\": [{\"type\": \"text_file\", \"name\": \"templates/*.html\"}]\n        }\n    ]\n): pass",
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
    "BackendDesignArchitect": {
        "prompt": (
            """You are a System Architect specializing in backend design for Flask web applications managing smart home systems.

Your goal is to create a backend design specification that describes data models and Flask routes to manage devices, automation, energy reports, and activity logs for the SmartHomeManager application.

Task Details:
- Read user_task_description from CONTEXT
- Independently create backend_design.md
- Specify all backend data schemas, file storage formats, and Flask route designs
- Do not rely on or read frontend_design.md

**Section 1: Data Models and File Formats**
- Specify all required data files with exact file names and pipe-delimited field schemas
- Include detailed field descriptions, data types, and example records
- Ensure data model supports users, devices, rooms, automation rules, energy logs, and activity logs as per user specifications
- Use the exact 'data' directory and text file conventions described

**Section 2: Flask Route Specifications**
- Define routes for managing all pages: dashboard, device list, add device, device control, automation rules, energy reports, and activity logs
- Specify HTTP methods, URL paths, expected query or form parameters, and route handler responsibilities
- Include notes on data passed to templates or expected user interactions
- Routes must align with the data models and support complete CRUD and navigation flows

CRITICAL SUCCESS CRITERIA:
- Your backend_design.md enables backend developers to implement app.py with full support for all functional requirements
- Use write_text_file tool to output backend_design.md
- Follow all naming and format conventions strictly—no additions beyond user_task_description inputs
- Write only the declared output artifact without refinement markers

Output: backend_design.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'backend_design.md'}],

    },

    "FrontendDesignArchitect": {
        "prompt": (
            """You are a System Architect specializing in HTML and Jinja2 template frontend design for Flask web applications.

Your goal is to create a frontend design specification that describes the HTML page structure, element IDs, UI components, and navigation flows for the seven SmartHomeManager application pages.

Task Details:
- Read user_task_description from CONTEXT
- Independently create frontend_design.md
- Specify HTML page templates for dashboard, device list, add device, device control, automation rules, energy report, and activity logs
- List all element IDs with their types and descriptions exactly as specified in the user requirements
- Define navigation buttons and links including their target pages and expected behaviors
- Do not rely on or read backend_design.md

**Section 1: HTML Template Structure**
- For each page, specify filename and exact page title
- List container Div IDs and named UI components with their element types
- Define dynamic elements like tables, buttons, inputs, dropdowns by ID and purpose

**Section 2: Navigation and Button Definitions**
- Map navigation controls such as buttons to their target pages (e.g., device-list-button navigates to device list page)
- Specify button IDs with action descriptions and target routes consistent with user navigation requirements
- Include form submission buttons and back-navigation buttons with expected behaviors

CRITICAL SUCCESS CRITERIA:
- Frontend developers can implement all templates/*.html files fully from frontend_design.md
- The design covers all UI elements and navigation flows exactly as per user specification
- Use write_text_file tool to output frontend_design.md
- Write only the declared output artifact without refinement markers

Output: frontend_design.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'frontend_design.md'}],

    },

    "DesignMerger": {
        "prompt": (
            """You are a System Architect specializing in synthesizing backend and frontend design specifications for Flask web applications.

Your goal is to merge backend_design.md and frontend_design.md into a single design_spec.md artifact that is internally consistent and complete according to the SmartHomeManager user requirements.

Task Details:
- Read user_task_description, backend_design.md, and frontend_design.md from CONTEXT
- Reconcile the backend and frontend specifications for data schema and interface consistency
- Resolve any inconsistencies in route naming, data variable naming, and navigation flows
- Create a coherent design_spec.md combining sections from both input artifacts without introducing new requirements

**Section 1: Backend Specifications**
- Integrate backend data models and Flask route definitions
- Ensure data file formats and schemas match expected frontend data usage

**Section 2: Frontend Specifications**
- Include complete HTML template structure, element IDs, and UI component definitions
- Ensure navigation buttons and page flows align with backend route specifications

**Section 3: Consistency and Completeness Checks**
- Validate that all backend routes correspond to frontend navigation controls
- Confirm that all data models have corresponding UI elements and that all user requirements are fully covered

CRITICAL SUCCESS CRITERIA:
- The resulting design_spec.md fully enables developers to implement both backend app.py and frontend templates/*.html
- No missing requirements or contradictions remain between backend and frontend
- Use write_text_file tool to output design_spec.md
- Write only the declared output artifact without refinement markers

Output: design_spec.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'backend_design.md', 'source': 'BackendDesignArchitect'}, {'type': 'text_file', 'name': 'frontend_design.md', 'source': 'FrontendDesignArchitect'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_spec.md'}],

    },

    "BackendDeveloper": {
        "prompt": (
            """You are a Backend Developer specializing in Flask web applications using Python.

Your goal is to implement the complete Flask backend application as a runnable app.py based on the provided design_spec.md, handling all routing, business logic, and data file interactions for a smart home management system.

Task Details:
- Read design_spec.md from CONTEXT, focusing on Sections detailing Flask routes, data schemas, and business rules
- Independently create app.py implementing all Flask routes, request handlers, data reads/writes to local text files, and application logic
- Output a single runnable app.py that does not depend on any sibling agent output artifacts

**Implementation Requirements:**
- Implement Flask routes exactly as specified, including URLs, methods, and expected context variables
- Integrate with local text files in the 'data' directory using prescribed data formats and delimiters
- Handle user sessions, device management, automation rules, energy and activity logs as outlined
- Ensure code readability with appropriate comments using only single-quote docstrings or inline hash comments
- Include error handling for file accesses and input validations

**Output and Tool Usage:**
- Use the write_text_file tool to save the fully implemented app.py
- The app.py must be runnable and self-contained based on design_spec.md contents only
- Do not read or require any frontend template files or sibling agent outputs

CRITICAL SUCCESS CRITERIA:
- app.py runs successfully implementing all backend logic defined in design_spec.md
- Data storage and retrieval conform to specified text file formats
- Routes and function names are consistent with frontend expectations from design_spec.md

Output: app.py"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}],

    },

    "FrontendDeveloper": {
        "prompt": (
            """You are a Frontend Developer specializing in HTML and Jinja2 template development for Flask web applications.

Your goal is to develop complete, well-structured HTML templates (*.html) with the specified element IDs and UI layout for all specified pages, based solely on the design_spec.md.

Task Details:
- Read design_spec.md from CONTEXT focusing on all page and template specifications, element IDs, and navigation requirements
- Independently create all required templates/*.html files for the seven defined pages:
  Dashboard, Device List, Add Device, Device Control, Automation Rules, Energy Report, Activity Logs
- Ensure each page has correct container divs, input fields, buttons, and tables with exact element IDs
- Use Jinja2 templating syntax where applicable for dynamic content placeholders and control structures

**Template Development Instructions:**
- Use semantic HTML5 elements and accessible markup
- Include all buttons and links with specified IDs for front-to-back navigation
- Incorporate placeholders for context variables as per design_spec.md
- Validate IDs are unique per page; no cross-page ID duplication
- Comment code using single-quote docstrings or hash comments only

**Output and Tool Usage:**
- Use write_text_file tool to output all HTML templates in templates/*.html
- Templates must form a cohesive frontend consistent with backend routes and context variables from design_spec.md
- Do not read backend source files or sibling agent outputs

CRITICAL SUCCESS CRITERIA:
- All seven pages implemented with exact element IDs and layout as per design_spec.md
- Templates fully compatible with Flask backend implementation
- Output includes only declared templates/*.html files

Output: templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'templates/*.html'}],

    },

    "IntegrationMerger": {
        "prompt": (
            """You are a Software Integration Engineer specializing in full-stack Flask web application delivery.

Your goal is to integrate the independently developed backend app.py and frontend templates/*.html into a final consistent, runnable application that fully satisfies design_spec.md.

Task Details:
- Read design_spec.md, app.py, and templates/*.html from CONTEXT
- Verify backend routes and data handling in app.py match frontend templates and context variables exactly as specified
- Reconcile any interface discrepancies between backend and frontend artifacts
- Ensure navigation, page titles, element IDs, and data bindings are consistent and complete
- Produce final versions of app.py and templates/*.html that are fully compatible and ready for deployment

**Integration and Validation Instructions:**
- Compare route names, HTTP methods, and expected template files in app.py against frontend templates
- Confirm all dynamic data fields referenced in templates are provided by backend context
- Validate element ID correctness and unique usage across templates
- Refactor minor inconsistencies without adding or removing features beyond design_spec.md
- Document key integration decisions and list any assumptions in comments using single-quote docstrings or hash comments

**Output and Tool Usage:**
- Use write_text_file tool to output merged app.py and complete templates/*.html
- Do not produce additional artifacts or refinement markers
- Final output must be deployable and consistent with all input artifacts and user task requirements

CRITICAL SUCCESS CRITERIA:
- Backend and frontend are fully integrated and interface consistent per design_spec.md
- Final app.py and templates/*.html can be deployed as a working SmartHomeManager application
- All review feedback from IntegrationMerger policy has been addressed

Output: app.py, templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}, {'type': 'text_file', 'name': 'app.py', 'source': 'BackendDeveloper'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'FrontendDeveloper'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}],

    }

}

REVIEW_PROFILES = {
    'BackendDesignArchitect': [
        ("DesignMerger", """Verify backend design completeness and conformance with user requirements and frontend design.""", [{'type': 'text_file', 'name': 'backend_design.md'}])
    ],

    'FrontendDesignArchitect': [
        ("DesignMerger", """Verify frontend design completeness and conformance with user requirements and backend design.""", [{'type': 'text_file', 'name': 'frontend_design.md'}])
    ],

    'BackendDeveloper': [
        ("IntegrationMerger", """Verify backend implementation code for correctness, completeness, and adherence to design_spec.md.""", [{'type': 'text_file', 'name': 'app.py'}])
    ],

    'FrontendDeveloper': [
        ("IntegrationMerger", """Verify frontend templates correctness, element ID accuracy, and conformance to design_spec.md.""", [{'type': 'text_file', 'name': 'templates/*.html'}])
    ]

}





# ==================== Chaos Controller Setup ====================
import random
import os
from chaos.injectors import ChaosMode

COMPOUND_CONFIG = {
    "agent_intensity": random.choice([0.2, 0.3, 0.4, 0.5, 0.6]),
    "stress_method": random.choice(['WORD_SHUFFLE', 'WORD_DELETION', 'WORD_REPLACEMENT']),
    "io_method": random.choice(['WORD_SHUFFLE', 'WORD_DELETION', 'WORD_REPLACEMENT']),
    "stress_probability": 0.2,
    "io_probability": 0.2
}
if os.environ.get("CHAOS_AGENT_PROBABILITY_OVERRIDE"):
    COMPOUND_CONFIG["agent_intensity"] = float(os.environ["CHAOS_AGENT_PROBABILITY_OVERRIDE"])
if os.environ.get("CHAOS_STRESS_PROBABILITY_OVERRIDE"):
    COMPOUND_CONFIG["stress_probability"] = float(os.environ["CHAOS_STRESS_PROBABILITY_OVERRIDE"])
if os.environ.get("CHAOS_IO_PROBABILITY_OVERRIDE"):
    COMPOUND_CONFIG["io_probability"] = float(os.environ["CHAOS_IO_PROBABILITY_OVERRIDE"])

MODE_MAP = {
    "WORD_SHUFFLE": ChaosMode.WORD_SHUFFLE,
    "WORD_DELETION": ChaosMode.WORD_DELETION,
    "WORD_REPLACEMENT": ChaosMode.WORD_REPLACEMENT,
}

chaos_target_agent_names = [
    name.strip()
    for name in os.environ.get("CHAOS_TARGET_AGENT_NAMES", "").split(",")
    if name.strip()
] or list(AGENT_PROFILES.keys())

chaos_controller = ChaosController(
    agent_chaos_enabled=True,
    stress_chaos_enabled=True,
    stress_chaos_mode=MODE_MAP[COMPOUND_CONFIG["stress_method"]],
    io_chaos_enabled=True,
    io_chaos_mode=MODE_MAP[COMPOUND_CONFIG["io_method"]],
    target_agent_names=chaos_target_agent_names
)

# V2 probabilities: agent chaos uses random 0.2-0.6; stress/io use 0.2.
# V1 methods: one word-based Stress mode and one word-based IO mode per task.
chaos_controller.start_experiment(
    running_agents=list(AGENT_PROFILES.keys()),
    agent_profiles=AGENT_PROFILES,
    probability=COMPOUND_CONFIG["agent_intensity"]
)

all_agents = list(AGENT_PROFILES.keys())
chaos_controller.set_targets_by_probability(
    "stress",
    running_agents=all_agents,
    agent_profiles=AGENT_PROFILES,
    probability=COMPOUND_CONFIG["stress_probability"]
)
chaos_controller.set_targets_by_probability(
    "io",
    running_agents=all_agents,
    agent_profiles=AGENT_PROFILES,
    probability=COMPOUND_CONFIG["io_probability"]
)

# Save chaos configuration to file for debugging
from datetime import datetime
import json

chaos_config_data = {
    "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    "scenario": "compound_chaos",
    "probability": COMPOUND_CONFIG["agent_intensity"],
    "target_agent_names": chaos_target_agent_names,
    "probabilities": {
        "agent_chaos": COMPOUND_CONFIG["agent_intensity"],
        "stress_chaos": COMPOUND_CONFIG["stress_probability"],
        "io_chaos": COMPOUND_CONFIG["io_probability"]
    },
    "compound_config": COMPOUND_CONFIG,
    "enabled_chaos_types": {
        "agent_chaos": chaos_controller.agent_chaos.enabled,
        "stress_chaos": chaos_controller.stress_chaos.enabled,
        "io_chaos": chaos_controller.io_chaos.enabled
    },
    "logical_targets": {
        "agent_chaos_targets": chaos_controller.agent_chaos_logical_targets,
        "stress_chaos_targets": chaos_controller.stress_chaos_logical_targets,
        "io_chaos_targets": chaos_controller.io_chaos_logical_targets
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

print("[*] Chaos scenario 'compound_chaos' activated with compound probabilities")
print(f"[*] Compound config: {COMPOUND_CONFIG}")
print(f"[*] Chaos configuration saved to: chaos_config.json")
# ================================================================

# Orchestration Functions
async def design_specification_phase():
    BackendDesignArchitect = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="BackendDesignArchitect",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=3,
        timeout_threshold=400,
        failure_threshold=1,
        recovery_time=40
    )
    FrontendDesignArchitect = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="FrontendDesignArchitect",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=3,
        timeout_threshold=400,
        failure_threshold=1,
        recovery_time=40
    )
    DesignMerger = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="DesignMerger",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=2,
        timeout_threshold=300,
        failure_threshold=1,
        recovery_time=30
    )

    # Parallel execution of BackendDesignArchitect and FrontendDesignArchitect
    await asyncio.gather(
        execute(BackendDesignArchitect, "Read user_task_description and create backend_design.md specifying backend data models and Flask routes according to requirements."),
        execute(FrontendDesignArchitect, "Read user_task_description and create frontend_design.md specifying HTML templates structure, element IDs, UI components, and navigation flows as per requirements.")
    )

    # Read outputs of both architects for merger
    backend_design_content, frontend_design_content = "", ""
    try:
        backend_design_content = open("backend_design.md").read()
    except FileNotFoundError:
        pass
    try:
        frontend_design_content = open("frontend_design.md").read()
    except FileNotFoundError:
        pass

    # Merge backend_design.md and frontend_design.md into design_spec.md
    await execute(
        DesignMerger,
        f"Read user_task_description, backend_design.md, and frontend_design.md.\n"
        f"Reconcile and merge into design_spec.md ensuring consistency and completeness.\n\n"
        f"=== backend_design.md ===\n{backend_design_content}\n\n"
        f"=== frontend_design.md ===\n{frontend_design_content}"
    )
# Phase1_End
# Phase2_Start

async def implementation_and_verification_phase():
    import glob

    BackendDeveloper = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="BackendDeveloper",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=3,
        timeout_threshold=450,
        failure_threshold=2,
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
        timeout_threshold=450,
        failure_threshold=2,
        recovery_time=40
    )

    IntegrationMerger = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="IntegrationMerger",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=3,
        timeout_threshold=400,
        failure_threshold=1,
        recovery_time=30
    )

    # Parallel implementation of backend and frontend
    await asyncio.gather(
        execute(BackendDeveloper,
                "Implement complete runnable app.py backend from design_spec.md, "
                "handling all Flask routes, data files and business logic for smart home system."),
        execute(FrontendDeveloper,
                "Implement all templates/*.html frontend pages with exact element IDs, layout and Jinja2 syntax "
                "from design_spec.md.")
    )

    # Read outputs from BackendDeveloper and FrontendDeveloper for integration
    design_spec_content = ""
    try:
        design_spec_content = open("design_spec.md").read()
    except FileNotFoundError:
        pass

    app_py_content = ""
    try:
        app_py_content = open("app.py").read()
    except FileNotFoundError:
        pass

    templates_content = ""
    for tpl_path in sorted(glob.glob("templates/*.html")):
        try:
            content = open(tpl_path).read()
            templates_content += f"\n=== {tpl_path} ===\n{content}"
        except OSError:
            pass

    # IntegrationMerger merges and reconciles backend and frontend into final deliverables
    await execute(
        IntegrationMerger,
        "Integrate backend app.py and frontend templates/*.html into final consistent application.\n\n"
        f"=== design_spec.md ===\n{design_spec_content}\n\n"
        f"=== Backend app.py ===\n{app_py_content}\n\n"
        f"=== Frontend templates ===\n{templates_content}"
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
        implementation_and_verification_phase()
    ]

    await asyncio.gather(*step1)
    await asyncio.gather(*step2)

    # Record task duration
    orchestrate_end_time = time.time()
    CONTEXT["_task_duration"] = orchestrate_end_time - orchestrate_start_time

    # Print chaos engineering report (if enabled)
    cc = None
    if 'chaos_controller' in globals():
        print("\n" + "="*80)
        print("Chaos Engineering Report")
        print("="*80)
        chaos_controller.print_report(context=CONTEXT)
        cc = chaos_controller

    # Print chaos engineering report
    print("\n" + "="*80)
    print("Chaos Engineering Report")
    print("="*80)
    chaos_controller.print_report(context=CONTEXT)


    # Save metrics to JSON (with resilience_metrics if chaos enabled)
    task_metrics = aggregate_task_metrics(CONTEXT, chaos_controller=cc)
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
        print(f"\n  Received signal {signum}, saving metrics and reports before exit...")

        # Save chaos reports if chaos_controller exists (chaos scenarios only)
        try:
            if 'chaos_controller' in globals():
                print("Generating chaos report on timeout...")
                chaos_controller.print_report(context=CONTEXT, save_to_file=True)
                print("Chaos reports saved successfully")
        except Exception as e:
            print(f"  Error saving chaos report: {e}")
            import traceback
            traceback.print_exc()

        # Save metrics (independent of chaos report success/failure)
        try:
            # Pass chaos_controller if available for resilience_metrics
            cc = chaos_controller if 'chaos_controller' in globals() else None
            task_metrics = aggregate_task_metrics(CONTEXT, chaos_controller=cc)
            metrics_path = Path("metrics.json")
            with open(metrics_path, "w") as f:
                json.dump(task_metrics, f, indent=2)
            print(f"Metrics saved to: {metrics_path.resolve()}")
        except Exception as e:
            print(f"Error saving metrics: {e}")
            import traceback
            traceback.print_exc()

        sys.exit(1)

    # Register signal handlers
    signal.signal(signal.SIGTERM, save_metrics_on_signal)
    signal.signal(signal.SIGINT, save_metrics_on_signal)

    # Open log file for real-time stdout/stderr capture
    log_file = open("execution_log.txt", "w", encoding="utf-8")
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

        log_file.close()
