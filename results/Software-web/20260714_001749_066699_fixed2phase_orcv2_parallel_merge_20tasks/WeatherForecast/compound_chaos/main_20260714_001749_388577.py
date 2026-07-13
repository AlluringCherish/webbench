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
# 20260714_001749_388577/main_20260714_001749_388577.py

# Phase_info dictionary containing complete def blocks for failover context
Phase_info = {
    "phase1": "def design_specification_phase(\n    goal: str = \"Create complementary backend and frontend design documents and merge them into a unified design_spec.md for the WeatherForecast web application.\",\n    collab_pattern_name: str = \"Parallel + Merger\",\n    collab_pattern_description: str = (\n        \"BackendDesignArchitect and FrontendDesignArchitect independently prepare backend and frontend design specs respectively from the user task. \"\n        \"DesignMerger reconciles and merges backend_design.md and frontend_design.md into a single coherent design_spec.md.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"BackendDesignArchitect\",\n            \"prompt\": \"\"\"You are a System Architect specializing in Python backend web application design focusing on Flask routes, data schemas, and file storage.\n\nYour goal is to produce a detailed backend_design.md that defines the Flask routes, data storage format, and backend API structure for the WeatherForecast application as specified in the user task.\n\nTask Details:\n- Read the full user_task_description from CONTEXT to identify backend requirements\n- Create backend_design.md independently without reading frontend outputs\n- Specify all Flask routes with paths, HTTP methods, and expected parameters\n- Define schemas for all text file data storage as described, including format, delimiters, field names, and example rows\n- Document any data loading and saving logic related to the local text files\n\n**Section 1: Flask Routes Specification**\n- List every route required for WeatherForecast, including Dashboard, Current Weather, Forecast, Location Search, Alerts, Air Quality, Saved Locations, and Settings pages\n- For each route specify URL path, HTTP methods (GET, POST), expected inputs and outputs, and template names if applicable\n- Include API endpoints for data interactions as needed\n\n**Section 2: Data File Schemas**\n- For each data file (e.g., current_weather.txt, forecasts.txt), specify exact data schema with field names, types, delimiters (pipe |), and descriptions\n- Provide example data rows for clarity matching the user task examples\n- Clarify any file read/write access patterns and concurrency considerations if needed\n\n**Section 3: Backend Data Handling and Storage**\n- Describe how data files in the 'data/' directory are accessed and manipulated\n- Specify any caching, data refresh strategy, or error handling relevant to backend design\n- Include considerations for default location management and alert acknowledgment updates\n\nCRITICAL SUCCESS CRITERIA:\n- backend_design.md contains complete and unambiguous specifications for implementation\n- All routes and data schemas strictly derive from user task description only\n- Use write_text_file tool to save backend_design.md\n\nOutput: backend_design.md\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"backend_design.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"FrontendDesignArchitect\",\n            \"prompt\": \"\"\"You are a System Architect specializing in frontend web design focusing on HTML templates, UI components, and navigation for Python Flask apps.\n\nYour goal is to produce a detailed frontend_design.md that defines the HTML structure, element IDs, navigation flow, and interactive UI elements for the WeatherForecast app based on the user task.\n\nTask Details:\n- Read the full user_task_description from CONTEXT to identify frontend UI requirements\n- Create frontend_design.md independently without accessing backend outputs\n- Specify each of the 8 pages with page title, main container div ID, and all required element IDs with their types and roles\n- Provide navigation flow between pages, including button or link IDs and their target destinations\n- Detail interactive components such as dropdowns, buttons, inputs, and data display areas according to the user specs\n\n**Section 1: HTML Template Specification**\n- For each page, specify the template file name, page title, and container elements\n- List all elements with their element IDs, HTML tag types (div, button, table, input, etc.), and brief descriptions of their purpose\n\n**Section 2: Navigation and Interaction**\n- Define navigation logic mapping buttons or links to specific page routes\n- Detail UI interaction behaviors like filter dropdowns, search inputs, and acknowledgement buttons including dynamic ID patterns (e.g., select-location-button-{location_id})\n\n**Section 3: UI Data Binding**\n- Specify context variables (names and structures) required for dynamic data display on each page\n- Clarify expected data presentation formats such as tables, lists, or cards as described in the user task\n\nCRITICAL SUCCESS CRITERIA:\n- frontend_design.md fully enables frontend implementation of all pages\n- All specified element IDs and navigation paths comply with user task\n- Use write_text_file tool to save frontend_design.md\n\nOutput: frontend_design.md\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"frontend_design.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"DesignMerger\",\n            \"prompt\": \"\"\"You are a System Architect specializing in synthesizing frontend and backend design specifications into a unified design contract for Flask web applications.\n\nYour goal is to generate a consolidated design_spec.md that integrates backend_design.md and frontend_design.md into a consistent and complete specification matching the user task without additions or omissions.\n\nTask Details:\n- Read user_task_description, backend_design.md, and frontend_design.md from CONTEXT\n- Reconcile the backend and frontend documents to resolve any inconsistencies in routes, data schemas, element IDs, and navigation\n- Produce a merged design_spec.md that combines backend Flask route specs, data file schemas, and frontend HTML templates with element IDs and navigation flows\n- Ensure naming conventions are consistent between backend routes and frontend template references\n- Verify that all user requirements concerning pages, data storage, and UI are accurately represented\n\n**Section 1: Integrated Flask Routes and API**\n- Consolidate and preserve all independent backend route specifications\n- Verify that routes correspond to frontend navigation targets\n\n**Section 2: Unified Data Schema Definitions**\n- Confirm all file schemas are present and consistent with usage in both backend and frontend\n- Merge data examples and format rules from both specs without contradiction\n\n**Section 3: HTML Templates and Navigation Flow**\n- Merge frontend template details with backend route names\n- Ensure all HTML element IDs and page links match the navigation flow\n\n**Section 4: Consistency and Completeness Checks**\n- Validate cross-document references: route names, template names, element IDs, and variable names\n- Confirm no requirements are omitted or added beyond the original user task\n\nCRITICAL SUCCESS CRITERIA:\n- design_spec.md enables both backend and frontend developers to implement from a single source\n- No requirement conflicts or duplications remain\n- Use write_text_file tool to output design_spec.md\n\nOutput: design_spec.md\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"backend_design.md\", \"source\": \"BackendDesignArchitect\"},\n                {\"type\": \"text_file\", \"name\": \"frontend_design.md\", \"source\": \"FrontendDesignArchitect\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"BackendDesignArchitect\",\n            \"reviewer_agent\": \"DesignMerger\",\n            \"review_criteria\": \"Ensure backend_design.md fully covers all backend requirements, adheres to user specifications and data storage formats.\",\n            \"review_artifacts\": [{\"type\": \"text_file\", \"name\": \"backend_design.md\"}]\n        },\n        {\n            \"source_agent\": \"FrontendDesignArchitect\",\n            \"reviewer_agent\": \"DesignMerger\",\n            \"review_criteria\": \"Validate frontend_design.md for completeness of UI element IDs, page flows, accessibility, and compliance with user task.\",\n            \"review_artifacts\": [{\"type\": \"text_file\", \"name\": \"frontend_design.md\"}]\n        }\n    ]\n): pass",
    "phase2": "def implementation_and_verification_phase(\n    goal: str = \"Implement backend app.py and frontend HTML templates in parallel from design_spec.md and integrate them into a final consistent application bundle.\",\n    collab_pattern_name: str = \"Parallel + Merger\",\n    collab_pattern_description: str = (\n        \"BackendDeveloper and FrontendDeveloper independently implement backend Python app.py and frontend HTML templates respectively using design_spec.md. \"\n        \"IntegrationMerger reconciles and integrates their artifacts into a consistent app.py and templates/*.html set.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"BackendDeveloper\",\n            \"prompt\": \"\"\"You are a Python Flask backend developer specializing in implementing web application APIs and data handling.\n\nYour goal is to implement the complete backend application in app.py, fully aligned with the backend API design and data format contracts described in the design specifications.\n\nTask Details:\n- Read design_spec.md from CONTEXT as the sole source of backend requirements\n- Independently create app.py implementing routing, data access, and logic for all specified backend features\n- Do NOT read or assume any frontend templates or sibling outputs\n- Output a fully functional Flask backend adhering to declared data file formats and route interfaces\n\n**Implementation Requirements:**\n- Define Flask routes, functions, and logic exactly as specified without adding features\n- Implement data loading and saving from text files per described schema in design_spec.md\n- Return data suitable for frontend templates with correct variable names and types\n- Handle all backend-side processing, including search, filtering, and alert acknowledgement\n\n**Coding Guidelines:**\n- Use single-quote docstrings for all inline code comments and documentation\n- Ensure clear modular structure for readability and maintainability\n- Avoid any UI or frontend code; focus purely on backend Python code\n\nCRITICAL SUCCESS CRITERIA:\n- MUST use write_text_file tool to write output file app.py\n- Implementation strictly follows design_spec.md backend contracts\n- Produce only the declared output artifact app.py\n- Do not incorporate or assume frontend implementation details here\n\nOutput: app.py\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"}\n            ]\n        },\n        {\n            \"agent_name\": \"FrontendDeveloper\",\n            \"prompt\": \"\"\"You are a frontend developer specializing in HTML and Jinja2 template design.\n\nYour goal is to implement the full set of frontend HTML templates (*.html) with required element IDs, page titles, navigation flows, and UI components as defined in design_spec.md.\n\nTask Details:\n- Read design_spec.md from CONTEXT as the definitive specification for all frontend pages and UI components\n- Independently create all HTML templates (*.html) implementing the specified structure and elements\n- Do NOT read or assume any backend source code or sibling outputs\n- Implement each page with exact element IDs, button behaviors, and templating variables as specified\n\n**Implementation Requirements:**\n- For each of the eight pages, create corresponding template files with container divs and child elements identified by exact IDs\n- Use Jinja2 syntax for context variables and control structures as described\n- Implement dropdowns, buttons, tables, and interactive elements per design_spec.md\n- Ensure consistent page titles matching specification and navigation buttons link correctly\n\n**Coding Guidelines:**\n- Use single-quote docstrings to comment template files if needed\n- Maintain clean indentation and formatting for readability and correctness\n- Avoid embedding backend logic beyond template variables and standard Jinja2 usage\n\nCRITICAL SUCCESS CRITERIA:\n- MUST use write_text_file tool to save all created HTML templates under templates/*.html\n- Templates strictly follow design_spec.md element IDs and layout\n- Produce only the declared output artifact templates/*.html\n- Do not implement backend logic here; focus solely on frontend templating\n\nOutput: templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        },\n        {\n            \"agent_name\": \"IntegrationMerger\",\n            \"prompt\": \"\"\"You are an integration specialist with expertise in Flask backend and frontend template consistency for web applications.\n\nYour goal is to analyze, reconcile, and integrate the separately implemented backend (app.py) and frontend (templates/*.html) artifacts into a consistent, deployable application bundle without introducing new features.\n\nTask Details:\n- Read design_spec.md, app.py, and templates/*.html from CONTEXT\n- Verify interface consistency between backend routes and frontend template variables and navigation\n- Detect and resolve routing, naming, or context variable mismatches and inconsistencies\n- Merge final corrected versions of app.py and templates/*.html preserving original implementations\n- Do not add or remove functional features beyond resolving inconsistencies\n\n**Integration Requirements:**\n- Ensure all frontend pages and elements match backend route handlers and data variables\n- Validate template context variable names against backend response structures\n- Confirm navigation elements and button actions align with backend routing and URL endpoints\n- Reconcile any discrepancies in naming, routing, and data formats between backend and frontend\n\n**Validation and Output:**\n- Use write_text_file tool to output integrated final app.py and templates/*.html\n- Produce only the declared output artifacts app.py and templates/*.html after integration\n- Maintain separation of concerns: do not modify feature scope or add new logic\n\nCRITICAL SUCCESS CRITERIA:\n- Fully consistent, matched backend and frontend ready for deployment\n- All corrections strictly limited to resolving implementation inconsistencies\n- Use write_text_file tool for outputs app.py and templates/*.html only\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"BackendDeveloper\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"FrontendDeveloper\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"BackendDeveloper\",\n            \"reviewer_agent\": \"IntegrationMerger\",\n            \"review_criteria\": (\n                \"Verify app.py implementation adheres to backend design contracts and data format specifications outlined in design_spec.md.\"\n            ),\n            \"review_artifacts\": [{\"type\": \"text_file\", \"name\": \"app.py\"}]\n        },\n        {\n            \"source_agent\": \"FrontendDeveloper\",\n            \"reviewer_agent\": \"IntegrationMerger\",\n            \"review_criteria\": (\n                \"Confirm HTML templates conform exactly to UI element IDs, page structure, and navigation rules specified in design_spec.md.\"\n            ),\n            \"review_artifacts\": [{\"type\": \"text_file\", \"name\": \"templates/*.html\"}]\n        }\n    ]\n): pass",
}

user_task = """
# Requirements Document for 'WeatherForecast' Web Application

## 1. Objective
Develop a comprehensive web application named 'WeatherForecast' using Python, with data managed through local text files. The application enables users to view current weather conditions, check weekly forecasts, search for locations, receive weather alerts, and monitor air quality. No authentication required - all features are directly accessible. Note that the website should start from the Dashboard page.

## 2. Language
The required development language for the 'WeatherForecast' application is Python.

## 3. Page Design

The 'WeatherForecast' web application will consist of the following eight pages:

### 1. Dashboard Page
- **Page Title**: Weather Dashboard
- **Overview**: The main hub displaying current weather, quick location access, and navigation to all functionalities.
- **Elements**:
  - **ID: dashboard-page** - Type: Div - Container for the dashboard page.
  - **ID: current-weather-summary** - Type: Div - Display of current weather conditions for default location.
  - **ID: search-location-button** - Type: Button - Button to navigate to location search page.
  - **ID: view-forecast-button** - Type: Button - Button to navigate to weekly forecast page.
  - **ID: view-alerts-button** - Type: Button - Button to navigate to weather alerts page.

### 2. Current Weather Page
- **Page Title**: Current Weather
- **Overview**: A page displaying detailed current weather conditions for selected location.
- **Elements**:
  - **ID: current-weather-page** - Type: Div - Container for the current weather page.
  - **ID: location-name** - Type: H1 - Display location name.
  - **ID: temperature-display** - Type: Div - Display current temperature.
  - **ID: weather-condition** - Type: Div - Display weather condition (sunny, rainy, cloudy, etc.).
  - **ID: humidity-info** - Type: Div - Display humidity percentage.
  - **ID: wind-speed-info** - Type: Div - Display wind speed.

### 3. Weekly Forecast Page
- **Page Title**: Weekly Forecast
- **Overview**: A page displaying weather forecast for the next 7 days.
- **Elements**:
  - **ID: forecast-page** - Type: Div - Container for the forecast page.
  - **ID: forecast-table** - Type: Table - Table displaying daily forecasts with date, high temp, low temp, and condition.
  - **ID: location-filter** - Type: Dropdown - Dropdown to filter forecast by location.
  - **ID: forecast-list** - Type: Div - Grid displaying forecast cards for each day.
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 4. Location Search Page
- **Page Title**: Search Locations
- **Overview**: A page for users to search and select different locations.
- **Elements**:
  - **ID: search-page** - Type: Div - Container for the search page.
  - **ID: location-search-input** - Type: Input - Field to search locations by city name or coordinates.
  - **ID: search-results** - Type: Div - List of search results displaying matching locations.
  - **ID: select-location-button-{location_id}** - Type: Button - Button to select a location (each result has this).
  - **ID: saved-locations-list** - Type: Div - Display of previously saved locations.

### 5. Weather Alerts Page
- **Page Title**: Weather Alerts
- **Overview**: A page displaying active weather alerts and warnings for selected locations.
- **Elements**:
  - **ID: alerts-page** - Type: Div - Container for the alerts page.
  - **ID: alerts-list** - Type: Div - List of all active weather alerts with severity, description, and location.
  - **ID: severity-filter** - Type: Dropdown - Dropdown to filter alerts by severity (All, Critical, High, Medium, Low).
  - **ID: location-filter-alerts** - Type: Dropdown - Dropdown to filter alerts by location.
  - **ID: acknowledge-alert-button-{alert_id}** - Type: Button - Button to acknowledge an alert (each alert has this).

### 6. Air Quality Page
- **Page Title**: Air Quality Index
- **Overview**: A page displaying air quality information and pollution levels for locations.
- **Elements**:
  - **ID: air-quality-page** - Type: Div - Container for the air quality page.
  - **ID: aqi-display** - Type: Div - Display air quality index value (0-500).
  - **ID: aqi-description** - Type: Div - Display air quality description (Good, Moderate, Unhealthy, etc.).
  - **ID: pollution-details** - Type: Table - Table showing PM2.5, PM10, NO2, and other pollutants.
  - **ID: location-aqi-filter** - Type: Dropdown - Dropdown to filter by location.
  - **ID: health-recommendation** - Type: Div - Display health recommendations based on air quality.

### 7. Saved Locations Page
- **Page Title**: Saved Locations
- **Overview**: A page displaying all saved locations with quick weather access.
- **Elements**:
  - **ID: saved-locations-page** - Type: Div - Container for the saved locations page.
  - **ID: locations-table** - Type: Table - Table displaying saved locations with current temp and weather condition.
  - **ID: view-location-weather-{location_id}** - Type: Button - Button to view weather for a location (each location has this).
  - **ID: remove-location-button-{location_id}** - Type: Button - Button to remove saved location (each location has this).
  - **ID: add-new-location-button** - Type: Button - Button to add new location.

### 8. Settings Page
- **Page Title**: Settings
- **Overview**: A page for users to configure temperature units, notification preferences, and default location.
- **Elements**:
  - **ID: settings-page** - Type: Div - Container for the settings page.
  - **ID: temperature-unit-select** - Type: Dropdown - Dropdown to select temperature unit (Celsius, Fahrenheit, Kelvin).
  - **ID: default-location-select** - Type: Dropdown - Dropdown to set default location.
  - **ID: alert-notifications-toggle** - Type: Checkbox - Toggle to enable/disable alert notifications.
  - **ID: save-settings-button** - Type: Button - Button to save settings changes.
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

## 4. Data Storage

The 'WeatherForecast' application will store data locally in text files organized in the directory 'data'. The following data formats and examples are defined:

### 1. Current Weather Data
- **File Name**: `current_weather.txt`
- **Data Format**:
  ```
  location_id|location_name|temperature|condition|humidity|wind_speed|last_updated
  ```
- **Example Data**:
  ```
  1|New York|72|Sunny|65|10|2025-01-20 14:30
  2|London|55|Rainy|80|15|2025-01-20 14:30
  3|Tokyo|45|Cloudy|72|8|2025-01-20 14:30
  ```

### 2. Forecasts Data
- **File Name**: `forecasts.txt`
- **Data Format**:
  ```
  forecast_id|location_id|date|high_temp|low_temp|condition|precipitation|humidity
  ```
- **Example Data**:
  ```
  1|1|2025-01-21|75|60|Sunny|0|60
  2|1|2025-01-22|68|55|Cloudy|10|70
  3|2|2025-01-21|58|48|Rainy|80|85
  ```

### 3. Locations Data
- **File Name**: `locations.txt`
- **Data Format**:
  ```
  location_id|location_name|latitude|longitude|country|timezone
  ```
- **Example Data**:
  ```
  1|New York|40.7128|-74.0060|USA|EST
  2|London|51.5074|-0.1278|UK|GMT
  3|Tokyo|35.6762|139.6503|Japan|JST
  ```

### 4. Weather Alerts Data
- **File Name**: `alerts.txt`
- **Data Format**:
  ```
  alert_id|location_id|alert_type|severity|description|start_time|end_time|is_acknowledged
  ```
- **Example Data**:
  ```
  1|1|Thunderstorm|High|Severe thunderstorm warning in effect until 8 PM|2025-01-20 14:00|2025-01-20 20:00|0
  2|2|Fog|Medium|Dense fog advisory in effect until noon tomorrow|2025-01-20 06:00|2025-01-21 12:00|0
  3|1|Wind|Medium|High wind advisory with gusts up to 45 mph|2025-01-20 15:00|2025-01-21 09:00|1
  ```

### 5. Air Quality Data
- **File Name**: `air_quality.txt`
- **Data Format**:
  ```
  aqi_id|location_id|aqi_index|pm25|pm10|no2|o3|last_updated
  ```
- **Example Data**:
  ```
  1|1|45|12.5|35|28|55|2025-01-20 14:30
  2|2|67|22.3|48|42|78|2025-01-20 14:30
  3|3|120|68.5|95|65|110|2025-01-20 14:30
  ```

### 6. Saved Locations Data
- **File Name**: `saved_locations.txt`
- **Data Format**:
  ```
  saved_id|user_id|location_id|location_name|is_default
  ```
- **Example Data**:
  ```
  1|1|1|New York|1
  2|1|2|London|0
  3|2|3|Tokyo|1
  ```
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
            """You are a System Architect specializing in Python backend web application design focusing on Flask routes, data schemas, and file storage.

Your goal is to produce a detailed backend_design.md that defines the Flask routes, data storage format, and backend API structure for the WeatherForecast application as specified in the user task.

Task Details:
- Read the full user_task_description from CONTEXT to identify backend requirements
- Create backend_design.md independently without reading frontend outputs
- Specify all Flask routes with paths, HTTP methods, and expected parameters
- Define schemas for all text file data storage as described, including format, delimiters, field names, and example rows
- Document any data loading and saving logic related to the local text files

**Section 1: Flask Routes Specification**
- List every route required for WeatherForecast, including Dashboard, Current Weather, Forecast, Location Search, Alerts, Air Quality, Saved Locations, and Settings pages
- For each route specify URL path, HTTP methods (GET, POST), expected inputs and outputs, and template names if applicable
- Include API endpoints for data interactions as needed

**Section 2: Data File Schemas**
- For each data file (e.g., current_weather.txt, forecasts.txt), specify exact data schema with field names, types, delimiters (pipe |), and descriptions
- Provide example data rows for clarity matching the user task examples
- Clarify any file read/write access patterns and concurrency considerations if needed

**Section 3: Backend Data Handling and Storage**
- Describe how data files in the 'data/' directory are accessed and manipulated
- Specify any caching, data refresh strategy, or error handling relevant to backend design
- Include considerations for default location management and alert acknowledgment updates

CRITICAL SUCCESS CRITERIA:
- backend_design.md contains complete and unambiguous specifications for implementation
- All routes and data schemas strictly derive from user task description only
- Use write_text_file tool to save backend_design.md

Output: backend_design.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'backend_design.md'}],

    },

    "FrontendDesignArchitect": {
        "prompt": (
            """You are a System Architect specializing in frontend web design focusing on HTML templates, UI components, and navigation for Python Flask apps.

Your goal is to produce a detailed frontend_design.md that defines the HTML structure, element IDs, navigation flow, and interactive UI elements for the WeatherForecast app based on the user task.

Task Details:
- Read the full user_task_description from CONTEXT to identify frontend UI requirements
- Create frontend_design.md independently without accessing backend outputs
- Specify each of the 8 pages with page title, main container div ID, and all required element IDs with their types and roles
- Provide navigation flow between pages, including button or link IDs and their target destinations
- Detail interactive components such as dropdowns, buttons, inputs, and data display areas according to the user specs

**Section 1: HTML Template Specification**
- For each page, specify the template file name, page title, and container elements
- List all elements with their element IDs, HTML tag types (div, button, table, input, etc.), and brief descriptions of their purpose

**Section 2: Navigation and Interaction**
- Define navigation logic mapping buttons or links to specific page routes
- Detail UI interaction behaviors like filter dropdowns, search inputs, and acknowledgement buttons including dynamic ID patterns (e.g., select-location-button-{location_id})

**Section 3: UI Data Binding**
- Specify context variables (names and structures) required for dynamic data display on each page
- Clarify expected data presentation formats such as tables, lists, or cards as described in the user task

CRITICAL SUCCESS CRITERIA:
- frontend_design.md fully enables frontend implementation of all pages
- All specified element IDs and navigation paths comply with user task
- Use write_text_file tool to save frontend_design.md

Output: frontend_design.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'frontend_design.md'}],

    },

    "DesignMerger": {
        "prompt": (
            """You are a System Architect specializing in synthesizing frontend and backend design specifications into a unified design contract for Flask web applications.

Your goal is to generate a consolidated design_spec.md that integrates backend_design.md and frontend_design.md into a consistent and complete specification matching the user task without additions or omissions.

Task Details:
- Read user_task_description, backend_design.md, and frontend_design.md from CONTEXT
- Reconcile the backend and frontend documents to resolve any inconsistencies in routes, data schemas, element IDs, and navigation
- Produce a merged design_spec.md that combines backend Flask route specs, data file schemas, and frontend HTML templates with element IDs and navigation flows
- Ensure naming conventions are consistent between backend routes and frontend template references
- Verify that all user requirements concerning pages, data storage, and UI are accurately represented

**Section 1: Integrated Flask Routes and API**
- Consolidate and preserve all independent backend route specifications
- Verify that routes correspond to frontend navigation targets

**Section 2: Unified Data Schema Definitions**
- Confirm all file schemas are present and consistent with usage in both backend and frontend
- Merge data examples and format rules from both specs without contradiction

**Section 3: HTML Templates and Navigation Flow**
- Merge frontend template details with backend route names
- Ensure all HTML element IDs and page links match the navigation flow

**Section 4: Consistency and Completeness Checks**
- Validate cross-document references: route names, template names, element IDs, and variable names
- Confirm no requirements are omitted or added beyond the original user task

CRITICAL SUCCESS CRITERIA:
- design_spec.md enables both backend and frontend developers to implement from a single source
- No requirement conflicts or duplications remain
- Use write_text_file tool to output design_spec.md

Output: design_spec.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'backend_design.md', 'source': 'BackendDesignArchitect'}, {'type': 'text_file', 'name': 'frontend_design.md', 'source': 'FrontendDesignArchitect'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_spec.md'}],

    },

    "BackendDeveloper": {
        "prompt": (
            """You are a Python Flask backend developer specializing in implementing web application APIs and data handling.

Your goal is to implement the complete backend application in app.py, fully aligned with the backend API design and data format contracts described in the design specifications.

Task Details:
- Read design_spec.md from CONTEXT as the sole source of backend requirements
- Independently create app.py implementing routing, data access, and logic for all specified backend features
- Do NOT read or assume any frontend templates or sibling outputs
- Output a fully functional Flask backend adhering to declared data file formats and route interfaces

**Implementation Requirements:**
- Define Flask routes, functions, and logic exactly as specified without adding features
- Implement data loading and saving from text files per described schema in design_spec.md
- Return data suitable for frontend templates with correct variable names and types
- Handle all backend-side processing, including search, filtering, and alert acknowledgement

**Coding Guidelines:**
- Use single-quote docstrings for all inline code comments and documentation
- Ensure clear modular structure for readability and maintainability
- Avoid any UI or frontend code; focus purely on backend Python code

CRITICAL SUCCESS CRITERIA:
- MUST use write_text_file tool to write output file app.py
- Implementation strictly follows design_spec.md backend contracts
- Produce only the declared output artifact app.py
- Do not incorporate or assume frontend implementation details here

Output: app.py"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}],

    },

    "FrontendDeveloper": {
        "prompt": (
            """You are a frontend developer specializing in HTML and Jinja2 template design.

Your goal is to implement the full set of frontend HTML templates (*.html) with required element IDs, page titles, navigation flows, and UI components as defined in design_spec.md.

Task Details:
- Read design_spec.md from CONTEXT as the definitive specification for all frontend pages and UI components
- Independently create all HTML templates (*.html) implementing the specified structure and elements
- Do NOT read or assume any backend source code or sibling outputs
- Implement each page with exact element IDs, button behaviors, and templating variables as specified

**Implementation Requirements:**
- For each of the eight pages, create corresponding template files with container divs and child elements identified by exact IDs
- Use Jinja2 syntax for context variables and control structures as described
- Implement dropdowns, buttons, tables, and interactive elements per design_spec.md
- Ensure consistent page titles matching specification and navigation buttons link correctly

**Coding Guidelines:**
- Use single-quote docstrings to comment template files if needed
- Maintain clean indentation and formatting for readability and correctness
- Avoid embedding backend logic beyond template variables and standard Jinja2 usage

CRITICAL SUCCESS CRITERIA:
- MUST use write_text_file tool to save all created HTML templates under templates/*.html
- Templates strictly follow design_spec.md element IDs and layout
- Produce only the declared output artifact templates/*.html
- Do not implement backend logic here; focus solely on frontend templating

Output: templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'templates/*.html'}],

    },

    "IntegrationMerger": {
        "prompt": (
            """You are an integration specialist with expertise in Flask backend and frontend template consistency for web applications.

Your goal is to analyze, reconcile, and integrate the separately implemented backend (app.py) and frontend (templates/*.html) artifacts into a consistent, deployable application bundle without introducing new features.

Task Details:
- Read design_spec.md, app.py, and templates/*.html from CONTEXT
- Verify interface consistency between backend routes and frontend template variables and navigation
- Detect and resolve routing, naming, or context variable mismatches and inconsistencies
- Merge final corrected versions of app.py and templates/*.html preserving original implementations
- Do not add or remove functional features beyond resolving inconsistencies

**Integration Requirements:**
- Ensure all frontend pages and elements match backend route handlers and data variables
- Validate template context variable names against backend response structures
- Confirm navigation elements and button actions align with backend routing and URL endpoints
- Reconcile any discrepancies in naming, routing, and data formats between backend and frontend

**Validation and Output:**
- Use write_text_file tool to output integrated final app.py and templates/*.html
- Produce only the declared output artifacts app.py and templates/*.html after integration
- Maintain separation of concerns: do not modify feature scope or add new logic

CRITICAL SUCCESS CRITERIA:
- Fully consistent, matched backend and frontend ready for deployment
- All corrections strictly limited to resolving implementation inconsistencies
- Use write_text_file tool for outputs app.py and templates/*.html only

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
        ("DesignMerger", """Ensure backend_design.md fully covers all backend requirements, adheres to user specifications and data storage formats.""", [{'type': 'text_file', 'name': 'backend_design.md'}])
    ],

    'FrontendDesignArchitect': [
        ("DesignMerger", """Validate frontend_design.md for completeness of UI element IDs, page flows, accessibility, and compliance with user task.""", [{'type': 'text_file', 'name': 'frontend_design.md'}])
    ],

    'BackendDeveloper': [
        ("IntegrationMerger", """Verify app.py implementation adheres to backend design contracts and data format specifications outlined in design_spec.md.""", [{'type': 'text_file', 'name': 'app.py'}])
    ],

    'FrontendDeveloper': [
        ("IntegrationMerger", """Confirm HTML templates conform exactly to UI element IDs, page structure, and navigation rules specified in design_spec.md.""", [{'type': 'text_file', 'name': 'templates/*.html'}])
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

    # Parallel execution of backend and frontend design architects
    await asyncio.gather(
        execute(BackendDesignArchitect, "Create backend_design.md focusing on Flask routes, data schemas, and backend API structure from user_task_description."),
        execute(FrontendDesignArchitect, "Create frontend_design.md focusing on HTML templates, UI elements, navigation flow, and context variables from user_task_description.")
    )

    # Read backend_design.md and frontend_design.md outputs for merger
    backend_design = ""
    frontend_design = ""
    try:
        backend_design = open("backend_design.md").read()
    except FileNotFoundError:
        pass
    try:
        frontend_design = open("frontend_design.md").read()
    except FileNotFoundError:
        pass

    # Merge backend and frontend design specs into unified design_spec.md
    await execute(DesignMerger,
                  f"User task description:\n{CONTEXT.get('user_task_description','')}\n\n"
                  f"=== Backend Design ===\n{backend_design}\n\n"
                  f"=== Frontend Design ===\n{frontend_design}")
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
        timeout_threshold=350,
        failure_threshold=2,
        recovery_time=45
    )
    FrontendDeveloper = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="FrontendDeveloper",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=3,
        timeout_threshold=350,
        failure_threshold=2,
        recovery_time=45
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
        failure_threshold=2,
        recovery_time=60
    )

    # Parallel implementation of backend and frontend
    await asyncio.gather(
        execute(
            BackendDeveloper,
            "Implement complete backend app.py fully aligned with backend API design and data contracts in design_spec.md."
        ),
        execute(
            FrontendDeveloper,
            "Implement all frontend HTML templates (*.html) with required element IDs, page titles, navigation, and UI components as specified in design_spec.md."
        )
    )

    # Read outputs for IntegrationMerger
    backend_code = ""
    frontend_templates = ""
    try:
        backend_code = open("app.py").read()
    except FileNotFoundError:
        pass
    for template_path in sorted(glob.glob("templates/*.html")):
        try:
            frontend_templates += f"\n=== {template_path} ===\n" + open(template_path).read()
        except OSError:
            pass

    # Integration and reconciliation of backend and frontend outputs
    await execute(
        IntegrationMerger,
        "Analyze, reconcile and integrate backend app.py and frontend templates/*.html into a consistent deployable application bundle.\n\n"
        f"=== design_spec.md content ===\n{CONTEXT.get('design_spec.md', '')}\n\n"
        f"=== Backend (app.py) Implementation ===\n{backend_code}\n\n"
        f"=== Frontend (templates/*.html) Implementation ===\n{frontend_templates}"
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
