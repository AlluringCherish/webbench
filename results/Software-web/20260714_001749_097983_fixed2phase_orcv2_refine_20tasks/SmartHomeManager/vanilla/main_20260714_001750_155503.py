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
# 20260714_001750_155503/main_20260714_001750_155503.py

# Phase_info dictionary containing complete def blocks for failover context
Phase_info = {
    "phase1": "def design_specification_phase(\n    goal: str = \"Refine the comprehensive design specification for the SmartHomeManager Flask web application including page structure, navigation, UI elements with exact element IDs, and data file organization, producing design_spec.md and gated design_feedback.md\",\n    collab_pattern_name: str = \"Refinement Loop\",\n    collab_pattern_description: str = \"DesignGenerator produces design_spec.md detailing pages, element IDs, and data storage contract; DesignCritic reviews this specification and produces design_feedback.md with either [APPROVED] or NEED_MODIFY to guide revision; iteration halts after approval or two cycles.\",\n    team: list = [\n        {\n            \"agent_name\": \"DesignGenerator\",\n            \"prompt\": \"\"\"You are a System Architect specializing in Flask web application design specifications.\n\nYour goal is to create and iteratively refine a complete design specification for the SmartHomeManager Flask web application, including detailed page structures, element IDs, navigation flows, and data storage formats.\n\nTask Details:\n- Read full user_task_description from CONTEXT describing all pages, UI elements with exact IDs, and data files\n- Read previous design_spec.md and design_feedback.md when available for refinement\n- On first iteration, author the complete design_spec.md covering page design, navigation, element IDs, and data file schemas\n- On feedback starting with NEED_MODIFY, apply all indicated corrections thoroughly and overwrite design_spec.md\n- When feedback starts with [APPROVED], preserve the final approved design_spec.md\n\n**Section 1: Page and Navigation Design**\n- Enumerate all seven pages with their Flask route paths starting at dashboard ('/dashboard')\n- Specify each page's title, container div IDs, button IDs, inputs, tables, and UI components as per user_task_description\n- Define navigation flow via buttons exactly by ID references (e.g., 'device-list-button' navigates to '/devices')\n\n**Section 2: UI Element ID Specifications**\n- Provide exact element IDs and their types (div, button, input, dropdown, table, etc.) for every page element listed\n- Maintain consistency in ID naming and type matching user_task_description details\n\n**Section 3: Data Storage Contract**\n- Define the 'data' folder usage and detail each data file (name, path)\n- Specify file formats with pipe-delimited fields and exact column names matching user_task_description\n- Include example rows for each data file as provided\n- Keep data isolation by type for efficient management\n\nCRITICAL SUCCESS CRITERIA:\n- Must run at most two Generator/Critic iterations and incorporate all NEED_MODIFY feedback\n- Use write_text_file tool to save complete design_spec.md after each iteration\n- Deliver well-structured design_spec.md enabling implementation and consistent critique\n- Reflect accurate Flask routing starting with dashboard page ('/dashboard')\n\nOutput: design_spec.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"design_feedback.md\", \"source\": \"DesignCritic\"}\n            ],\n            \"output_artifacts\": [{\"type\": \"text_file\", \"name\": \"design_spec.md\"}]\n        },\n        {\n            \"agent_name\": \"DesignCritic\",\n            \"prompt\": \"\"\"You are a Design Reviewer specializing in Flask web application design specifications.\n\nYour goal is to critically review the design_spec.md against the user_task_description and produce gated feedback that either approves the design or requests revisions with clear actionable details.\n\nTask Details:\n- Read user_task_description and design_spec.md from CONTEXT\n- Verify every page is defined with exact Flask route paths, beginning with dashboard page ('/dashboard')\n- Confirm all UI element IDs, types, and navigation flows fully match user requirements and are unambiguous\n- Validate all data storage file definitions, formats, delimiters, field names, and example data accurately reflect the user specification\n- Produce feedback starting exactly with [APPROVED] if complete and consistent, or NEED_MODIFY followed by specific corrections required\n\nReview Criteria:\n1. All seven pages with their respective IDs and navigation buttons are present and correctly specified\n2. Element IDs precisely match those from user_task_description with correct element types\n3. Flask routes are appropriate and start at the dashboard\n4. Data files are correctly named, formatted using pipe delimiters, with exact field names and example rows\n5. No missing or extraneous UI elements or data file fields beyond user specification\n\nCRITICAL REQUIREMENTS:\n- The first bytes of design_feedback.md MUST be exactly [APPROVED] or NEED_MODIFY\n- Do not prepend any headings, whitespace, or other markers before the feedback marker\n- Use write_text_file tool exclusively to output the full design_feedback.md content\n- Feedback must enable generator to fully resolve all requested changes in at most two iterations\n\nOutput: design_feedback.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignGenerator\"}\n            ],\n            \"output_artifacts\": [{\"type\": \"text_file\", \"name\": \"design_feedback.md\"}]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"DesignGenerator\",\n            \"reviewer_agent\": \"DesignCritic\",\n            \"review_criteria\": \"Verify that the design_spec.md fully captures the user requirements, uses exact element IDs for all components, defines the Flask page routing starting at the dashboard, and correctly specifies all data storage files and formats.\",\n            \"review_artifacts\": [{\"type\": \"text_file\", \"name\": \"design_spec.md\"}]\n        }\n    ]\n): pass",
    "phase2": "def implementation_and_verification_phase(\n    goal: str = \"Produce and iteratively refine the complete Flask application code (app.py and templates/*.html) for SmartHomeManager with data handling per design_spec.md, and gated by code_feedback.md\",\n    collab_pattern_name: str = \"Refinement Loop\",\n    collab_pattern_description: str = \"AppGenerator creates or revises app.py and all corresponding HTML templates under templates/ directory based on design_spec.md and code_feedback.md; CodeCritic reviews these artifacts for functional correctness, UI compliance, data handling accuracy, and Flask conventions and produces code_feedback.md with [APPROVED] or NEED_MODIFY; up to two iterations per refinement.\",\n    team: list = [\n        {\n            \"agent_name\": \"AppGenerator\",\n            \"prompt\": \"\"\"You are a Python Flask Developer specializing in building full-stack web applications with data persisted in local text files.\n\nYour goal is to develop or iteratively refine the complete SmartHomeManager Flask application implementation, including app.py backend and all HTML templates under the templates/ directory, based on design_spec.md and code_feedback.md.\n\nTask Details:\n- Read design_spec.md, existing app.py, templates/*.html, and code_feedback.md from CONTEXT\n- On initial iteration, produce full app.py and all templates/*.html per design_spec.md requirements\n- On feedback NEED_MODIFY, incorporate all corrections fully and rewrite the complete artifacts\n- On [APPROVED], preserve approved implementation unchanged\n- Focus exclusively on implementing declared pages, exact element IDs, navigation flows starting at dashboard page, data interactions with local text files as specified\n- Write app.py and templates/*.html output files precisely with exact naming under expected folders\n\n**Section 1: Flask App Implementation**\n- Implement Flask routes for all seven pages named in design_spec.md, starting with dashboard route as root\n- Ensure route handlers manage reading and writing to data files in 'data' directory according to specified data schemas\n- Handle device control, automation rules, energy reports, and activity logs with correct business logic and persistent storage\n- Use proper Flask url_for navigation and POST/GET as appropriate\n\n**Section 2: HTML Templates Requirements**\n- Create HTML templates with exactly the specified element IDs (e.g., dashboard-page, device-list-page, add-device-page, etc.)\n- Implement button and link navigation that matches route names and element IDs in design_spec.md\n- Reflect all UI components for forms, tables, buttons, divs, and inputs as declared\n\n**Section 3: Iterative Refinement**\n- On feedback NEED_MODIFY, address all changes comprehensively per CodeCritic comments, rewriting all files\n- Use write_text_file tool to save updated app.py and each HTML file in templates/\n- Maintain code readability, Flask conventions and UI consistency throughout\n\nCRITICAL SUCCESS CRITERIA:\n- Complete implementation covers all functionalities per design_spec.md\n- Exact element IDs and navigation routes without omission\n- Persistent data stored in text files under 'data' as specified\n- Use write_text_file tool strictly to output app.py and templates/*.html files\n- Stop after at most two iterations or upon [APPROVED] feedback\n\nOutput: app.py and templates/*.html\n\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"AppGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"AppGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"code_feedback.md\", \"source\": \"CodeCritic\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        },\n        {\n            \"agent_name\": \"CodeCritic\",\n            \"prompt\": \"\"\"You are a Software Test Engineer specializing in Flask web applications and code quality assurance.\n\nYour goal is to perform detailed reviews of SmartHomeManager’s app.py and templates/*.html implementation against design_spec.md and produce gated code_feedback.md for at most two refinement iterations.\n\nTask Details:\n- Read design_spec.md, app.py, and all templates/*.html from CONTEXT\n- Verify compliance with all page requirements, exact element IDs, UI consistency, and correct Flask routing starting at dashboard page\n- Validate data handling correctness: local text file reading/writing matching declared formats and storage directory 'data'\n- Confirm navigation buttons and links align precisely with route endpoints and element IDs\n- Write code_feedback.md beginning exactly with [APPROVED] if fully compliant or NEED_MODIFY followed by clear correction directives if not\n- Feedback must guide fixing missing elements, incorrect routes, data handling errors, or UI inconsistencies\n\nReview Requirements:\n1. All seven pages exist as Flask routes and correspond to templates/*.html matching design_spec.md\n2. Every required UI element ID (buttons, divs, forms, tables) is present and correctly named\n3. Data interaction in app.py uses local text files in 'data' folder with exact field parsing per specification\n4. Navigation flows through buttons exactly match the specified page transitions\n5. No missing functionality or features declared in design_spec.md\n\nCRITICAL REQUIREMENTS:\n- code_feedback.md must start with [APPROVED] or NEED_MODIFY with no leading whitespace or extraneous content\n- Use write_text_file tool to save complete, precise feedback text\n- Limit refinement cycles to two iterations, stop immediately on approval\n- Focus feedback exclusively on detail accuracy and completeness without adding new feature requests\n\nOutput: code_feedback.md\n\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"AppGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"AppGenerator\"}\n            ],\n            \"output_artifacts\": [{\"type\": \"text_file\", \"name\": \"code_feedback.md\"}]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"AppGenerator\",\n            \"reviewer_agent\": \"CodeCritic\",\n            \"review_criteria\": \"Check that app.py and templates/*.html fully implement the design_spec.md features, use exact element IDs, Flask routes start at dashboard page, and manage local text data files correctly without missing elements.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ]\n): pass",
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
    "DesignGenerator": {
        "prompt": (
            """You are a System Architect specializing in Flask web application design specifications.

Your goal is to create and iteratively refine a complete design specification for the SmartHomeManager Flask web application, including detailed page structures, element IDs, navigation flows, and data storage formats.

Task Details:
- Read full user_task_description from CONTEXT describing all pages, UI elements with exact IDs, and data files
- Read previous design_spec.md and design_feedback.md when available for refinement
- On first iteration, author the complete design_spec.md covering page design, navigation, element IDs, and data file schemas
- On feedback starting with NEED_MODIFY, apply all indicated corrections thoroughly and overwrite design_spec.md
- When feedback starts with [APPROVED], preserve the final approved design_spec.md

**Section 1: Page and Navigation Design**
- Enumerate all seven pages with their Flask route paths starting at dashboard ('/dashboard')
- Specify each page's title, container div IDs, button IDs, inputs, tables, and UI components as per user_task_description
- Define navigation flow via buttons exactly by ID references (e.g., 'device-list-button' navigates to '/devices')

**Section 2: UI Element ID Specifications**
- Provide exact element IDs and their types (div, button, input, dropdown, table, etc.) for every page element listed
- Maintain consistency in ID naming and type matching user_task_description details

**Section 3: Data Storage Contract**
- Define the 'data' folder usage and detail each data file (name, path)
- Specify file formats with pipe-delimited fields and exact column names matching user_task_description
- Include example rows for each data file as provided
- Keep data isolation by type for efficient management

CRITICAL SUCCESS CRITERIA:
- Must run at most two Generator/Critic iterations and incorporate all NEED_MODIFY feedback
- Use write_text_file tool to save complete design_spec.md after each iteration
- Deliver well-structured design_spec.md enabling implementation and consistent critique
- Reflect accurate Flask routing starting with dashboard page ('/dashboard')

Output: design_spec.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignGenerator'}, {'type': 'text_file', 'name': 'design_feedback.md', 'source': 'DesignCritic'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_spec.md'}],

    },

    "DesignCritic": {
        "prompt": (
            """You are a Design Reviewer specializing in Flask web application design specifications.

Your goal is to critically review the design_spec.md against the user_task_description and produce gated feedback that either approves the design or requests revisions with clear actionable details.

Task Details:
- Read user_task_description and design_spec.md from CONTEXT
- Verify every page is defined with exact Flask route paths, beginning with dashboard page ('/dashboard')
- Confirm all UI element IDs, types, and navigation flows fully match user requirements and are unambiguous
- Validate all data storage file definitions, formats, delimiters, field names, and example data accurately reflect the user specification
- Produce feedback starting exactly with [APPROVED] if complete and consistent, or NEED_MODIFY followed by specific corrections required

Review Criteria:
1. All seven pages with their respective IDs and navigation buttons are present and correctly specified
2. Element IDs precisely match those from user_task_description with correct element types
3. Flask routes are appropriate and start at the dashboard
4. Data files are correctly named, formatted using pipe delimiters, with exact field names and example rows
5. No missing or extraneous UI elements or data file fields beyond user specification

CRITICAL REQUIREMENTS:
- The first bytes of design_feedback.md MUST be exactly [APPROVED] or NEED_MODIFY
- Do not prepend any headings, whitespace, or other markers before the feedback marker
- Use write_text_file tool exclusively to output the full design_feedback.md content
- Feedback must enable generator to fully resolve all requested changes in at most two iterations

Output: design_feedback.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignGenerator'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_feedback.md'}],

    },

    "AppGenerator": {
        "prompt": (
            """You are a Python Flask Developer specializing in building full-stack web applications with data persisted in local text files.

Your goal is to develop or iteratively refine the complete SmartHomeManager Flask application implementation, including app.py backend and all HTML templates under the templates/ directory, based on design_spec.md and code_feedback.md.

Task Details:
- Read design_spec.md, existing app.py, templates/*.html, and code_feedback.md from CONTEXT
- On initial iteration, produce full app.py and all templates/*.html per design_spec.md requirements
- On feedback NEED_MODIFY, incorporate all corrections fully and rewrite the complete artifacts
- On [APPROVED], preserve approved implementation unchanged
- Focus exclusively on implementing declared pages, exact element IDs, navigation flows starting at dashboard page, data interactions with local text files as specified
- Write app.py and templates/*.html output files precisely with exact naming under expected folders

**Section 1: Flask App Implementation**
- Implement Flask routes for all seven pages named in design_spec.md, starting with dashboard route as root
- Ensure route handlers manage reading and writing to data files in 'data' directory according to specified data schemas
- Handle device control, automation rules, energy reports, and activity logs with correct business logic and persistent storage
- Use proper Flask url_for navigation and POST/GET as appropriate

**Section 2: HTML Templates Requirements**
- Create HTML templates with exactly the specified element IDs (e.g., dashboard-page, device-list-page, add-device-page, etc.)
- Implement button and link navigation that matches route names and element IDs in design_spec.md
- Reflect all UI components for forms, tables, buttons, divs, and inputs as declared

**Section 3: Iterative Refinement**
- On feedback NEED_MODIFY, address all changes comprehensively per CodeCritic comments, rewriting all files
- Use write_text_file tool to save updated app.py and each HTML file in templates/
- Maintain code readability, Flask conventions and UI consistency throughout

CRITICAL SUCCESS CRITERIA:
- Complete implementation covers all functionalities per design_spec.md
- Exact element IDs and navigation routes without omission
- Persistent data stored in text files under 'data' as specified
- Use write_text_file tool strictly to output app.py and templates/*.html files
- Stop after at most two iterations or upon [APPROVED] feedback

Output: app.py and templates/*.html
"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignGenerator'}, {'type': 'text_file', 'name': 'app.py', 'source': 'AppGenerator'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'AppGenerator'}, {'type': 'text_file', 'name': 'code_feedback.md', 'source': 'CodeCritic'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}],

    },

    "CodeCritic": {
        "prompt": (
            """You are a Software Test Engineer specializing in Flask web applications and code quality assurance.

Your goal is to perform detailed reviews of SmartHomeManager’s app.py and templates/*.html implementation against design_spec.md and produce gated code_feedback.md for at most two refinement iterations.

Task Details:
- Read design_spec.md, app.py, and all templates/*.html from CONTEXT
- Verify compliance with all page requirements, exact element IDs, UI consistency, and correct Flask routing starting at dashboard page
- Validate data handling correctness: local text file reading/writing matching declared formats and storage directory 'data'
- Confirm navigation buttons and links align precisely with route endpoints and element IDs
- Write code_feedback.md beginning exactly with [APPROVED] if fully compliant or NEED_MODIFY followed by clear correction directives if not
- Feedback must guide fixing missing elements, incorrect routes, data handling errors, or UI inconsistencies

Review Requirements:
1. All seven pages exist as Flask routes and correspond to templates/*.html matching design_spec.md
2. Every required UI element ID (buttons, divs, forms, tables) is present and correctly named
3. Data interaction in app.py uses local text files in 'data' folder with exact field parsing per specification
4. Navigation flows through buttons exactly match the specified page transitions
5. No missing functionality or features declared in design_spec.md

CRITICAL REQUIREMENTS:
- code_feedback.md must start with [APPROVED] or NEED_MODIFY with no leading whitespace or extraneous content
- Use write_text_file tool to save complete, precise feedback text
- Limit refinement cycles to two iterations, stop immediately on approval
- Focus feedback exclusively on detail accuracy and completeness without adding new feature requests

Output: code_feedback.md
"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignGenerator'}, {'type': 'text_file', 'name': 'app.py', 'source': 'AppGenerator'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'AppGenerator'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'code_feedback.md'}],

    }

}

REVIEW_PROFILES = {
    'DesignGenerator': [
        ("DesignCritic", """Verify that the design_spec.md fully captures the user requirements, uses exact element IDs for all components, defines the Flask page routing starting at the dashboard, and correctly specifies all data storage files and formats.""", [{'type': 'text_file', 'name': 'design_spec.md'}])
    ],

    'AppGenerator': [
        ("CodeCritic", """Check that app.py and templates/*.html fully implement the design_spec.md features, use exact element IDs, Flask routes start at dashboard page, and manage local text data files correctly without missing elements.""", [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}])
    ]

}



# Orchestration Functions
async def design_specification_phase():
    DesignGenerator = build_resilient_agent(
        agent_name="DesignGenerator",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=2,
        timeout_threshold=300,
        failure_threshold=1,
        recovery_time=30
    )
    DesignCritic = build_resilient_agent(
        agent_name="DesignCritic",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=2,
        timeout_threshold=300,
        failure_threshold=1,
        recovery_time=30
    )

    MAX_ITERATIONS = 2
    for iteration in range(MAX_ITERATIONS):
        current_design = ""
        feedback_content = ""
        try:
            current_design = open("design_spec.md").read()
        except FileNotFoundError:
            pass
        if iteration > 0:
            try:
                feedback_content = open("design_feedback.md").read()
            except FileNotFoundError:
                pass

        await execute(
            DesignGenerator,
            "Create and iteratively refine a complete design_spec.md.\n\n"
            f"=== Current design_spec.md ===\n{current_design}\n\n"
            f"=== DesignCritic Feedback ===\n{feedback_content}"
        )

        try:
            current_design = open("design_spec.md").read()
        except FileNotFoundError:
            current_design = ""

        await execute(
            DesignCritic,
            "Critically review the latest design_spec.md against user_task_description. "
            "Produce design_feedback.md starting exactly with [APPROVED] or NEED_MODIFY.\n\n"
            f"=== Latest design_spec.md ===\n{current_design}"
        )

        try:
            feedback_content = open("design_feedback.md").read()
        except FileNotFoundError:
            feedback_content = ""
        if feedback_content.startswith("[APPROVED]"):
            break
# Phase1_End
# Phase2_Start
import glob

async def implementation_and_verification_phase():
    AppGenerator = build_resilient_agent(
        agent_name="AppGenerator",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=2,
        timeout_threshold=400,
        failure_threshold=1,
        recovery_time=30
    )
    CodeCritic = build_resilient_agent(
        agent_name="CodeCritic",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=2,
        timeout_threshold=350,
        failure_threshold=1,
        recovery_time=30
    )

    MAX_ITERATIONS = 2
    for iteration in range(MAX_ITERATIONS):
        app_content = ""
        templates_content = ""
        feedback_content = ""
        try:
            app_content = open("app.py").read()
        except FileNotFoundError:
            pass
        for template_path in sorted(glob.glob("templates/*.html")):
            try:
                templates_content += f"\n=== {template_path} ===\n" + open(template_path).read()
            except OSError:
                pass
        if iteration > 0:
            try:
                feedback_content = open("code_feedback.md").read()
            except FileNotFoundError:
                pass

        await execute(
            AppGenerator,
            "Create or revise the complete app.py and templates/*.html.\n\n"
            f"=== Current app.py ===\n{app_content}\n\n"
            f"=== Current Templates ===\n{templates_content}\n\n"
            f"=== CodeCritic Feedback ===\n{feedback_content}"
        )

        try:
            app_content = open("app.py").read()
        except FileNotFoundError:
            app_content = ""
        templates_content = ""
        for template_path in sorted(glob.glob("templates/*.html")):
            try:
                templates_content += f"\n=== {template_path} ===\n" + open(template_path).read()
            except OSError:
                pass

        await execute(
            CodeCritic,
            "Review the latest app.py and templates against design_spec.md. "
            "Write code_feedback.md beginning exactly with [APPROVED] or NEED_MODIFY.\n\n"
            f"=== Latest app.py ===\n{app_content}\n\n"
            f"=== Latest Templates ===\n{templates_content}"
        )

        try:
            feedback_content = open("code_feedback.md").read()
        except FileNotFoundError:
            feedback_content = ""
        if feedback_content.startswith("[APPROVED]"):
            break
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
