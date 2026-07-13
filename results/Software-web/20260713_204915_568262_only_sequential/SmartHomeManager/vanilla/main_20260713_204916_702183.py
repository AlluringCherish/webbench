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
# 20260713_204916_702183/main_20260713_204916_702183.py

# Phase_info dictionary containing complete def blocks for failover context
Phase_info = {
    "phase1": "def design_specification_phase(\n    goal: str = \"Analyze the SmartHomeManager requirements and produce a detailed design_spec.md with complete page designs, elements, and data storage definitions\",\n    collab_pattern_name: str = \"Sequential Flow\",\n    collab_pattern_description: str = (\n        \"RequirementsAnalyst reads the user task description and writes requirements_analysis.md; then \"\n        \"WebArchitect converts requirements_analysis.md into design_spec.md with explicit page element details, navigation flows, and data formats.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"RequirementsAnalyst\",\n            \"prompt\": \"\"\"You are a Requirements Analyst specializing in analyzing web application requirements and documenting detailed specifications.\n\nYour goal is to extract all web application requirements including pages, element IDs, navigation flows, and data storage formats into a comprehensive requirements_analysis.md.\n\nTask Details:\n- Read user_task_description fully for comprehensive understanding\n- Extract details on all pages, page titles, element IDs and types\n- Extract navigation buttons and their target pages\n- Extract data storage file names, formats, field structures, and example data\n- Produce requirements_analysis.md containing all extracted info in organized format\n\nRequirements Documentation:\n1. **Page Details**:\n   - List all pages with exact page titles\n   - Include all specified elements with IDs, types, and descriptions\n   - Document navigation button IDs and their destination pages\n\n2. **Data Storage Specification**:\n   - List all data files used with filenames and exact fields\n   - Specify delimited format (pipe '|') and field order\n   - Provide sample example data for each file\n\n3. **User Flow Overview**:\n   - Describe main user flows starting from Dashboard page\n   - Summarize navigation paths among pages via specified buttons\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save output as requirements_analysis.md\n- Ensure completeness with no missing pages or elements\n- Follow user task description exactly without assumptions\n\nOutput: requirements_analysis.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"requirements_analysis.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"WebArchitect\",\n            \"prompt\": \"\"\"You are a Web Architect specializing in web application architecture and design specification.\n\nYour goal is to design the overall application architecture and create design_spec.md detailing pages, page titles, element IDs and types, navigation buttons with routes, data file formats and local storage paths, and user flow originating from the dashboard.\n\nTask Details:\n- Read requirements_analysis.md thoroughly for complete requirements\n- Define explicit page details with titles and all elements (IDs and types)\n- Specify navigation button mappings and routing between pages\n- Detail data files stored in local text files with exact filename, delimiter, fields, and sample data\n- Structure specification for developer-friendly usage\n\nDesign Specification Requirements:\n1. **Page and Element Specification**:\n   - Each page defined with a container div ID\n   - List all element IDs with HTML element types and their roles\n   - Include dynamic elements with placeholder notation if applicable (e.g., control-device-button-{device_id})\n\n2. **Navigation Routing**:\n   - Map each button ID to target page names/routes\n   - Ensure routing supports starting from dashboard page and subsequent navigations\n\n3. **Data Storage Formats**:\n   - Define each data file path relative to data/ directory\n   - Specify pipe-delimited fields with exact order\n   - Include realistic example rows from requirements\n\n4. **User Flows**:\n   - Describe user entry point and navigation sequences\n   - Highlight critical navigation buttons on dashboard and other key pages\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save detailed design_spec.md\n- Ensure full coverage of all specified pages and data files\n- Maintain strict adherence to extracted requirements without additions\n- Enable clear understanding for developers implementing frontend/backend\n\nOutput: design_spec.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"requirements_analysis.md\", \"source\": \"RequirementsAnalyst\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"RequirementsAnalyst\",\n            \"reviewer_agent\": \"WebArchitect\",\n            \"review_criteria\": (\n                \"Verify requirements_analysis.md covers all seven pages, element IDs, data file definitions, user flows and matches user task description fully.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\"},\n                {\"type\": \"text_file\", \"name\": \"requirements_analysis.md\"}\n            ]\n        }\n    ]\n): pass",
    "phase2": "def implementation_phase(\n    goal: str = \"Develop the SmartHomeManager Flask web application with page templates and app.py implementing exact routes, navigation, local data storage, \"\n                \"and all page-specific controls as described in design_spec.md\",\n    collab_pattern_name: str = \"Sequential Flow\",\n    collab_pattern_description: str = (\n        \"ImplementationEngineer writes the Flask app.py and templates/*.html files from design_spec.md, creating all pages, UI elements with correct IDs, and implementing data read/write to local text files. \"\n        \"No front-end or inline templates are allowed; all templates must be separate HTML files.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"ImplementationEngineer\",\n            \"prompt\": \"\"\"You are a Full-Stack Python Developer specializing in Flask web applications.\n\nYour goal is to produce the complete external Flask application code including app.py and all HTML template files to deliver a full SmartHomeManager web app based on design specifications.\n\nTask Details:\n- Read design_spec.md thoroughly to extract all route definitions, page templates, UI elements with exact IDs, and data storage requirements\n- Output app.py implementing all routes, logic, data reading and writing via local text files in 'data/' directory\n- Output separate HTML templates in templates/ folder with all specified elements, IDs, buttons, controls, and navigation\n- Focus on implementing the seven specified pages starting from dashboard page as entry point\n\nImplementation Guidelines:\n1. **Flask app.py structure and routes**\n   # Set up Flask app with necessary imports\n   '''\n   from flask import Flask, render_template, request, redirect, url_for\n   app = Flask(__name__)\n   app.config['SECRET_KEY'] = 'dev-secret-key'\n   '''\n   # Implement root route '/' to redirect to dashboard page\n   # Implement all routes for the seven pages with functions named as per design_spec.md\n   # Use render_template() to render corresponding HTML files with correct context variables\n   # Implement form handling for POST requests (e.g., add device, save settings, add rules)\n   # Read/write local text files in pipe-delimited format from data/ directory for user, device, room, automation, energy, and activity data\n   # Handle file I/O safely, including file not found and empty file scenarios\n\n2. **HTML templates in templates/ directory**\n   # Create one HTML file per page as specified in design_spec.md Section 2\n   # Include all required elements with exact ID attributes matching design_spec.md (case sensitive)\n   # Include page titles exactly as specified both in <title> tag and main heading tag\n   # Use Jinja2 templating syntax to loop over data lists and display dynamic content\n   # Include buttons and links with ids and correct navigation via url_for()\n   # Use forms with proper methods and input field IDs for user inputs where needed\n\n3. **Navigation and consistency**\n   # All navigation buttons and links must use url_for with exact route function names\n   # Maintain consistency of context variable names between backend and templates\n   # All data manipulation must correspond to schemas and formats in design_spec.md and stored in correct text files in 'data' folder\n\nCRITICAL REQUIREMENTS:\n- MUST use write_text_file tool to save app.py and all templates/*.html files separately\n- All IDs and element names in templates MUST match the design_spec.md exactly\n- All routes must be fully implemented with proper context and local file handling\n- No inline templates allowed: all template files must be external separate HTML files in templates/ folder\n- Follow design_spec.md explicitly; do not add or remove pages or controls beyond specification\n\nOutput: app.py and templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"WebArchitect\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"ImplementationEngineer\",\n            \"reviewer_agent\": \"DesignChecker\",\n            \"review_criteria\": (\n                \"Verify app.py and templates/*.html implement all pages, routes, element IDs, and local text file storage precisely according to design_spec.md.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ]\n): pass",
    "phase3": "def verification_phase(\n    goal: str = \"Validate the SmartHomeManager app.py and templates/*.html for runtime correctness, Flask compatibility, proper navigation, and data persistence; apply corrections as needed\",\n    collab_pattern_name: str = \"Sequential Flow\",\n    collab_pattern_description: str = (\n        \"Validator agent tests app.py and templates/*.html by running Flask test client and checking navigation, element presence, and local file data operations; \"\n        \"Fixer agent applies defect fixes and writes final runnable app.py and templates/*.html.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"Validator\",\n            \"prompt\": \"\"\"You are a Software Test Engineer specializing in Flask web application validation and verification.\n\nYour goal is to validate the SmartHomeManager Flask backend and HTML templates to ensure runtime correctness, proper Flask route handling, complete page elements as per design_spec.md, accurate navigation, and correct local data persistence.\n\nTask Details:\n- Read design_spec.md, app.py, and all HTML templates under templates/*.html\n- Validate syntax and runtime execution of app.py using Python validation tools\n- Test all Flask routes to confirm they render correct templates with required elements\n- Verify presence and correctness of critical element IDs on each page as specified\n- Check that local file operations correctly read/write data files in 'data' directory\n- Produce validation_report.md capturing all issues with detailed repro steps and design references\n\nValidation Requirements:\n1. **Python Code Validation**\n   - Perform syntax and runtime checks on app.py using validate_python_file tool\n2. **Functional Testing with Flask Test Client**\n   - Simulate HTTP requests to all routes\n   - Confirm response status codes are 200 OK\n   - Check rendered templates include ALL specified element IDs exactly\n3. **Data Persistence Verification**\n   - Perform test reads and writes on local text files in pipe-delimited format\n   - Confirm data integrity and format adherence per design_spec.md\n4. **Validation Report**\n   - Document every defect or discrepancy found with clear reproduction steps\n   - Reference design_spec.md sections to pinpoint expectation vs reality\n   - Structure report with summaries per page and per artifact\n\nCRITICAL REQUIREMENTS:\n- Use validate_python_file and execute_python_code tools for validation\n- Use write_text_file tool to output comprehensive validation_report.md\n- Ensure validation_report.md clearly differentiates syntax errors, runtime errors, UI defects, data issues\n- Focus exclusively on provided input artifacts - do not request additional information\n- Maintain professional thoroughness with reproducible findings and clear recommendations\n\nOutput: validation_report.md\"\"\",\n            \"tools\": [\"validate_python_file\", \"execute_python_code\", \"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"WebArchitect\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"ImplementationEngineer\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"ImplementationEngineer\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_report.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"Fixer\",\n            \"prompt\": \"\"\"You are a Software Developer specializing in Flask web application debugging and refinement.\n\nYour goal is to apply all necessary fixes to app.py and templates/*.html as documented in validation_report.md to ensure full runtime correctness, strict adherence to design_spec.md, and seamless Flask operation.\n\nTask Details:\n- Read validation_report.md for detailed defect descriptions and repro steps\n- Read design_spec.md as source of truth for specifications and element IDs\n- Modify app.py to resolve all backend defects including syntax, route, and data handling issues\n- Update all templates/*.html files to fix element ID presence, navigation links, and structural errors\n- Ensure final app.py and all templates strictly comply with design_spec.md without deviation\n- Maintain formatting, code style, and clarity in all fixes\n- Prepare corrected app.py and all templates/*.html for deployment\n\nFixing Guidelines:\n1. **Backend Corrections**\n   - Address all Python syntax and runtime errors\n   - Verify all Flask routes exist and function as expected\n   - Correct data file reading/writing following pipe-delimited schema exactly\n2. **Frontend Corrections**\n   - Insert all required element IDs exactly as specified per page\n   - Update navigation buttons and links to use correct url_for functions\n   - Ensure HTML structure matches design requirements precisely\n3. **Verification**\n   - Preliminary local verification of fixes before submission is encouraged but not required\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save final fixed app.py and all templates/*.html files\n- Do NOT add new features or functionality beyond fixes specified in validation_report.md\n- Do NOT omit any element IDs or navigation mappings in templates\n- Preserve overall project structure with no breaking changes or regressions\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_report.md\", \"source\": \"Validator\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"WebArchitect\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"ImplementationEngineer\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"ImplementationEngineer\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"Validator\",\n            \"reviewer_agent\": \"Fixer\",\n            \"review_criteria\": (\n                \"Verify validation_report.md contains all actionable findings with runnable repro steps and detailed design trace.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_report.md\"}\n            ]\n        },\n        {\n            \"source_agent\": \"Fixer\",\n            \"reviewer_agent\": \"RequirementsAnalyst\",\n            \"review_criteria\": (\n                \"Verify that final app.py and templates/*.html fully resolve validation issues and adhere strictly to design_spec.md specifications.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"},\n                {\"type\": \"text_file\", \"name\": \"validation_report.md\"}\n            ]\n        }\n    ]\n): pass",
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
    "RequirementsAnalyst": {
        "prompt": (
            """You are a Requirements Analyst specializing in analyzing web application requirements and documenting detailed specifications.

Your goal is to extract all web application requirements including pages, element IDs, navigation flows, and data storage formats into a comprehensive requirements_analysis.md.

Task Details:
- Read user_task_description fully for comprehensive understanding
- Extract details on all pages, page titles, element IDs and types
- Extract navigation buttons and their target pages
- Extract data storage file names, formats, field structures, and example data
- Produce requirements_analysis.md containing all extracted info in organized format

Requirements Documentation:
1. **Page Details**:
   - List all pages with exact page titles
   - Include all specified elements with IDs, types, and descriptions
   - Document navigation button IDs and their destination pages

2. **Data Storage Specification**:
   - List all data files used with filenames and exact fields
   - Specify delimited format (pipe '|') and field order
   - Provide sample example data for each file

3. **User Flow Overview**:
   - Describe main user flows starting from Dashboard page
   - Summarize navigation paths among pages via specified buttons

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save output as requirements_analysis.md
- Ensure completeness with no missing pages or elements
- Follow user task description exactly without assumptions

Output: requirements_analysis.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'requirements_analysis.md'}],

    },

    "WebArchitect": {
        "prompt": (
            """You are a Web Architect specializing in web application architecture and design specification.

Your goal is to design the overall application architecture and create design_spec.md detailing pages, page titles, element IDs and types, navigation buttons with routes, data file formats and local storage paths, and user flow originating from the dashboard.

Task Details:
- Read requirements_analysis.md thoroughly for complete requirements
- Define explicit page details with titles and all elements (IDs and types)
- Specify navigation button mappings and routing between pages
- Detail data files stored in local text files with exact filename, delimiter, fields, and sample data
- Structure specification for developer-friendly usage

Design Specification Requirements:
1. **Page and Element Specification**:
   - Each page defined with a container div ID
   - List all element IDs with HTML element types and their roles
   - Include dynamic elements with placeholder notation if applicable (e.g., control-device-button-{device_id})

2. **Navigation Routing**:
   - Map each button ID to target page names/routes
   - Ensure routing supports starting from dashboard page and subsequent navigations

3. **Data Storage Formats**:
   - Define each data file path relative to data/ directory
   - Specify pipe-delimited fields with exact order
   - Include realistic example rows from requirements

4. **User Flows**:
   - Describe user entry point and navigation sequences
   - Highlight critical navigation buttons on dashboard and other key pages

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save detailed design_spec.md
- Ensure full coverage of all specified pages and data files
- Maintain strict adherence to extracted requirements without additions
- Enable clear understanding for developers implementing frontend/backend

Output: design_spec.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'requirements_analysis.md', 'source': 'RequirementsAnalyst'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_spec.md'}],

    },

    "ImplementationEngineer": {
        "prompt": (
            """You are a Full-Stack Python Developer specializing in Flask web applications.

Your goal is to produce the complete external Flask application code including app.py and all HTML template files to deliver a full SmartHomeManager web app based on design specifications.

Task Details:
- Read design_spec.md thoroughly to extract all route definitions, page templates, UI elements with exact IDs, and data storage requirements
- Output app.py implementing all routes, logic, data reading and writing via local text files in 'data/' directory
- Output separate HTML templates in templates/ folder with all specified elements, IDs, buttons, controls, and navigation
- Focus on implementing the seven specified pages starting from dashboard page as entry point

Implementation Guidelines:
1. **Flask app.py structure and routes**
   # Set up Flask app with necessary imports
   '''
   from flask import Flask, render_template, request, redirect, url_for
   app = Flask(__name__)
   app.config['SECRET_KEY'] = 'dev-secret-key'
   '''
   # Implement root route '/' to redirect to dashboard page
   # Implement all routes for the seven pages with functions named as per design_spec.md
   # Use render_template() to render corresponding HTML files with correct context variables
   # Implement form handling for POST requests (e.g., add device, save settings, add rules)
   # Read/write local text files in pipe-delimited format from data/ directory for user, device, room, automation, energy, and activity data
   # Handle file I/O safely, including file not found and empty file scenarios

2. **HTML templates in templates/ directory**
   # Create one HTML file per page as specified in design_spec.md Section 2
   # Include all required elements with exact ID attributes matching design_spec.md (case sensitive)
   # Include page titles exactly as specified both in <title> tag and main heading tag
   # Use Jinja2 templating syntax to loop over data lists and display dynamic content
   # Include buttons and links with ids and correct navigation via url_for()
   # Use forms with proper methods and input field IDs for user inputs where needed

3. **Navigation and consistency**
   # All navigation buttons and links must use url_for with exact route function names
   # Maintain consistency of context variable names between backend and templates
   # All data manipulation must correspond to schemas and formats in design_spec.md and stored in correct text files in 'data' folder

CRITICAL REQUIREMENTS:
- MUST use write_text_file tool to save app.py and all templates/*.html files separately
- All IDs and element names in templates MUST match the design_spec.md exactly
- All routes must be fully implemented with proper context and local file handling
- No inline templates allowed: all template files must be external separate HTML files in templates/ folder
- Follow design_spec.md explicitly; do not add or remove pages or controls beyond specification

Output: app.py and templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'WebArchitect'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}],

    },

    "Validator": {
        "prompt": (
            """You are a Software Test Engineer specializing in Flask web application validation and verification.

Your goal is to validate the SmartHomeManager Flask backend and HTML templates to ensure runtime correctness, proper Flask route handling, complete page elements as per design_spec.md, accurate navigation, and correct local data persistence.

Task Details:
- Read design_spec.md, app.py, and all HTML templates under templates/*.html
- Validate syntax and runtime execution of app.py using Python validation tools
- Test all Flask routes to confirm they render correct templates with required elements
- Verify presence and correctness of critical element IDs on each page as specified
- Check that local file operations correctly read/write data files in 'data' directory
- Produce validation_report.md capturing all issues with detailed repro steps and design references

Validation Requirements:
1. **Python Code Validation**
   - Perform syntax and runtime checks on app.py using validate_python_file tool
2. **Functional Testing with Flask Test Client**
   - Simulate HTTP requests to all routes
   - Confirm response status codes are 200 OK
   - Check rendered templates include ALL specified element IDs exactly
3. **Data Persistence Verification**
   - Perform test reads and writes on local text files in pipe-delimited format
   - Confirm data integrity and format adherence per design_spec.md
4. **Validation Report**
   - Document every defect or discrepancy found with clear reproduction steps
   - Reference design_spec.md sections to pinpoint expectation vs reality
   - Structure report with summaries per page and per artifact

CRITICAL REQUIREMENTS:
- Use validate_python_file and execute_python_code tools for validation
- Use write_text_file tool to output comprehensive validation_report.md
- Ensure validation_report.md clearly differentiates syntax errors, runtime errors, UI defects, data issues
- Focus exclusively on provided input artifacts - do not request additional information
- Maintain professional thoroughness with reproducible findings and clear recommendations

Output: validation_report.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['validate_python_file', 'execute_python_code', 'write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'WebArchitect'}, {'type': 'text_file', 'name': 'app.py', 'source': 'ImplementationEngineer'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'ImplementationEngineer'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'validation_report.md'}],

    },

    "Fixer": {
        "prompt": (
            """You are a Software Developer specializing in Flask web application debugging and refinement.

Your goal is to apply all necessary fixes to app.py and templates/*.html as documented in validation_report.md to ensure full runtime correctness, strict adherence to design_spec.md, and seamless Flask operation.

Task Details:
- Read validation_report.md for detailed defect descriptions and repro steps
- Read design_spec.md as source of truth for specifications and element IDs
- Modify app.py to resolve all backend defects including syntax, route, and data handling issues
- Update all templates/*.html files to fix element ID presence, navigation links, and structural errors
- Ensure final app.py and all templates strictly comply with design_spec.md without deviation
- Maintain formatting, code style, and clarity in all fixes
- Prepare corrected app.py and all templates/*.html for deployment

Fixing Guidelines:
1. **Backend Corrections**
   - Address all Python syntax and runtime errors
   - Verify all Flask routes exist and function as expected
   - Correct data file reading/writing following pipe-delimited schema exactly
2. **Frontend Corrections**
   - Insert all required element IDs exactly as specified per page
   - Update navigation buttons and links to use correct url_for functions
   - Ensure HTML structure matches design requirements precisely
3. **Verification**
   - Preliminary local verification of fixes before submission is encouraged but not required

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save final fixed app.py and all templates/*.html files
- Do NOT add new features or functionality beyond fixes specified in validation_report.md
- Do NOT omit any element IDs or navigation mappings in templates
- Preserve overall project structure with no breaking changes or regressions

Output: app.py, templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'validation_report.md', 'source': 'Validator'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'WebArchitect'}, {'type': 'text_file', 'name': 'app.py', 'source': 'ImplementationEngineer'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'ImplementationEngineer'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}],

    }

}

REVIEW_PROFILES = {
    'RequirementsAnalyst': [
        ("WebArchitect", """Verify requirements_analysis.md covers all seven pages, element IDs, data file definitions, user flows and matches user task description fully.""", [{'type': 'user', 'name': 'user_task_description'}, {'type': 'text_file', 'name': 'requirements_analysis.md'}])
    ],

    'ImplementationEngineer': [
        ("DesignChecker", """Verify app.py and templates/*.html implement all pages, routes, element IDs, and local text file storage precisely according to design_spec.md.""", [{'type': 'text_file', 'name': 'design_spec.md'}, {'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}])
    ],

    'Validator': [
        ("Fixer", """Verify validation_report.md contains all actionable findings with runnable repro steps and detailed design trace.""", [{'type': 'text_file', 'name': 'validation_report.md'}])
    ],

    'Fixer': [
        ("RequirementsAnalyst", """Verify that final app.py and templates/*.html fully resolve validation issues and adhere strictly to design_spec.md specifications.""", [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}, {'type': 'text_file', 'name': 'design_spec.md'}, {'type': 'text_file', 'name': 'validation_report.md'}])
    ]

}



# Orchestration Functions
async def design_specification_phase():
    RequirementsAnalyst = build_resilient_agent(
        agent_name="RequirementsAnalyst",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=2,
        timeout_threshold=280,
        failure_threshold=1,
        recovery_time=40
    )
    WebArchitect = build_resilient_agent(
        agent_name="WebArchitect",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=2,
        timeout_threshold=280,
        failure_threshold=1,
        recovery_time=40
    )

    # Sequential execution: RequirementsAnalyst produces requirements_analysis.md, then WebArchitect produces design_spec.md
    await execute(RequirementsAnalyst,
                  "Analyze user task description and produce requirements_analysis.md including all pages, element IDs, navigation buttons, and data storage definitions.")
    
    # Read requirements_analysis.md content for injection
    requirements_analysis_content = ""
    try:
        requirements_analysis_content = open("requirements_analysis.md").read()
    except:
        pass

    await execute(WebArchitect,
                  f"Using the following requirements_analysis.md content, create a detailed design_spec.md with explicit page details, navigation routing, data file formats, and user flows.\n\n=== requirements_analysis.md ===\n{requirements_analysis_content}")
# Phase1_End

# Phase2_Start

async def implementation_phase():
    ImplementationEngineer = build_resilient_agent(
        agent_name="ImplementationEngineer",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=2,
        timeout_threshold=280,
        failure_threshold=1,
        recovery_time=40
    )

    design_spec_content = ""
    try:
        with open("design_spec.md", "r") as f:
            design_spec_content = f.read()
    except:
        pass

    await execute(
        ImplementationEngineer,
        f"Develop complete Flask app.py and all templates/*.html files based on the design_spec.md below. "
        f"Implement 7 pages with exact route functions, UI element IDs, navigation, and local data file read/write in 'data/' folder.\n\n"
        f"=== design_spec.md ===\n{design_spec_content}"
    )
# Phase2_End

# Phase3_Start

async def verification_phase():
    Validator = build_resilient_agent(
        agent_name="Validator",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase3"],
        max_retries=3,
        timeout_threshold=400,
        failure_threshold=1,
        recovery_time=40
    )
    Fixer = build_resilient_agent(
        agent_name="Fixer",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase3"],
        max_retries=3,
        timeout_threshold=450,
        failure_threshold=1,
        recovery_time=45
    )

    # Read all relevant files to inject into Validator
    design_spec_md = ""
    app_py = ""
    templates_html = ""
    try:
        design_spec_md = open("design_spec.md").read()
    except:
        pass
    try:
        app_py = open("app.py").read()
    except:
        pass
    import glob
    try:
        template_files = glob.glob("templates/*.html")
        templates_html = ""
        for tf in template_files:
            try:
                templates_html += f"=== {tf} ===\n" + open(tf).read() + "\n\n"
            except:
                pass
    except:
        pass

    # Execute Validator to produce validation_report.md
    await execute(
        Validator,
        f"Validate Flask backend and HTML templates for SmartHomeManager application.\n\n"
        f"=== design_spec.md ===\n{design_spec_md}\n\n"
        f"=== app.py ===\n{app_py}\n\n"
        f"=== Templates ===\n{templates_html}\n\n"
        "Perform syntax and runtime checks on app.py using validate_python_file and execute_python_code tools. "
        "Simulate HTTP requests to all Flask routes, check status codes and presence of all specified element IDs in templates. "
        "Verify correct local file data operations as per design_spec.md. "
        "Output a detailed validation_report.md including syntax errors, runtime errors, UI defects, and data issues."
    )

    # Read validation_report.md content for fixing
    validation_report_md = ""
    try:
        validation_report_md = open("validation_report.md").read()
    except:
        pass

    # Inject validation_report.md plus design_spec.md plus current app.py and templates/* for Fixer agent
    await execute(
        Fixer,
        f"Apply all fixes to app.py and all templates/*.html as per validation_report.md below:\n\n"
        f"=== validation_report.md ===\n{validation_report_md}\n\n"
        f"=== design_spec.md ===\n{design_spec_md}\n\n"
        f"=== Current app.py ===\n{app_py}\n\n"
        f"=== Current Templates ===\n{templates_html}\n\n"
        "Fix all backend defects (syntax, routes, data handling) and frontend defects (element IDs, navigation, structure). "
        "Output corrected app.py and templates/*.html files using write_text_file tool."
    )
# Phase3_End

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
        implementation_phase()
    ]
    step3 = [
        verification_phase()
    ]

    await asyncio.gather(*step1)
    await asyncio.gather(*step2)
    await asyncio.gather(*step3)

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
