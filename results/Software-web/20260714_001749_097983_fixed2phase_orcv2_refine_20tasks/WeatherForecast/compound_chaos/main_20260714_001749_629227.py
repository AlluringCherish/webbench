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
# 20260714_001749_629227/main_20260714_001749_629227.py

# Phase_info dictionary containing complete def blocks for failover context
Phase_info = {
    "phase1": "def design_specification_phase(\n    goal: str = \"Create a detailed adaptive design specification for the WeatherForecast web app with page layouts, element IDs, navigation, and data storage formats as explicit deliverables.\",\n    collab_pattern_name: str = \"Refinement Loop\",\n    collab_pattern_description: str = (\n        \"DesignGenerator writes design_spec.md, laying out all page designs, element IDs, navigation structure, \"\n        \"and data storage format based on the user_task_description string. DesignCritic reviews design_spec.md, \"\n        \"writes design_feedback.md beginning with [APPROVED] or NEED_MODIFY providing detailed feedback for improvements. \"\n        \"Data flow is design_spec.md from DesignGenerator to DesignCritic, design_feedback.md from DesignCritic to DesignGenerator.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"DesignGenerator\",\n            \"prompt\": \"\"\"You are a System Architect specializing in Python web application design specifications.\n\nYour goal is to create a complete design_spec.md defining all eight pages (Dashboard, Current Weather, Weekly Forecast, Location Search, Weather Alerts, Air Quality, Saved Locations, Settings) with exact element IDs, navigation flow, and local text file data schema for the WeatherForecast web app. Revise this specification based on critic feedback for at most two iterations.\n\nTask Details:\n- Read user_task_description from CONTEXT\n- Read existing design_spec.md and design_feedback.md when available\n- On the first iteration, create the full design_spec.md describing page layouts, element IDs, navigation, and data storage formats as specified\n- On feedback beginning with NEED_MODIFY, apply every correction and overwrite design_spec.md accordingly\n- On feedback beginning with [APPROVED], preserve the approved design_spec.md\n\n**Section 1: Page Layouts and Element IDs**\n- Define each of the eight pages with their exact page titles and container element IDs\n- List all specified UI elements per page with element IDs and types\n- Ensure elements match the requirements for each page as described in user_task_description\n\n**Section 2: Navigation Structure**\n- Define user navigation flow among the eight pages\n- Specify navigational button element IDs and their target pages/actions\n- Ensure dashboard is the app start page and back buttons lead accordingly\n\n**Section 3: Data Storage Formats**\n- Specify exact local text file names and data schemas for current weather, forecasts, locations, alerts, air quality, saved locations\n- Include field names, order, delimiters, and example data rows as given\n\nCRITICAL SUCCESS CRITERIA:\n- At most two iterations of Generator/Critic refinement loops\n- Fully cover each page's layout and elements as per requirements\n- Accurately define navigation element mappings and workflows\n- Precisely describe each text file format aligned with requirement document\n- Use write_text_file tool to output design_spec.md without adding extraneous sections or explanations\n\nOutput: design_spec.md\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"design_feedback.md\", \"source\": \"DesignCritic\"}\n            ],\n            \"output_artifacts\": [{\"type\": \"text_file\", \"name\": \"design_spec.md\"}]\n        },\n        {\n            \"agent_name\": \"DesignCritic\",\n            \"prompt\": \"\"\"You are a Design Reviewer specializing in Python web application design verification and specification review.\n\nYour goal is to review design_spec.md for completeness, consistency, and adherence to requirements regarding page layout, element IDs, navigation flow, and local text file data schemas. Provide gated feedback in design_feedback.md starting with [APPROVED] if fully compliant or NEED_MODIFY followed by detailed corrections. Refinement is limited to at most two iterations.\n\nTask Details:\n- Read user_task_description and design_spec.md from CONTEXT\n- Review if all eight pages are described with required element IDs and page titles\n- Verify navigational buttons and flows are logically and completely specified, with dashboard as start page\n- Check data storage sections specify exact text file names, data formats, fields, delimiters, and sample data matching requirements\n- Note any missing or inconsistent details that impair implementation or user navigation\n\nReview Checklist:\n1. All pages include specified container and UI element IDs matching requirements\n2. Navigation links/buttons are correctly assigned and consistent with pages defined\n3. Data file schemas fully match names, field order, delimiters, and example rows given\n4. No contradictions or omissions in page design or data specifications\n5. Feedback wording begins with exactly [APPROVED] or NEED_MODIFY, no other leading text or blank lines before marker\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save complete feedback in design_feedback.md\n- Feedback must begin with [APPROVED] if no issues\n- If NEED_MODIFY, list clear, actionable corrections only\n- Limit to two review iterations maximum, stop upon approval\n\nOutput: design_feedback.md\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignGenerator\"}\n            ],\n            \"output_artifacts\": [{\"type\": \"text_file\", \"name\": \"design_feedback.md\"}]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"DesignGenerator\",\n            \"reviewer_agent\": \"DesignCritic\",\n            \"review_criteria\": (\n                \"Ensure design_spec.md fully covers all stated requirements including page structure, element IDs, \"\n                \"navigation logic, and correct specification of local text file data formats as per the requirements document. \"\n                \"Check for clarity, completeness, and absence of contradictions.\"\n            ),\n            \"review_artifacts\": [{\"type\": \"text_file\", \"name\": \"design_spec.md\"}]\n        }\n    ]\n): pass",
    "phase2": "def implementation_and_verification_phase(\n    goal: str = \"Develop and iteratively refine an executable Python Flask web app (app.py, templates/*.html) implementing WeatherForecast design_spec.md and successfully passing code validation.\",\n    collab_pattern_name: str = \"Refinement Loop\",\n    collab_pattern_description: str = (\n        \"AppGenerator creates or revises app.py and templates/*.html implementing the comprehensive web app based on design_spec.md and code_feedback.md. \"\n        \"CodeCritic reviews the generated code and templates for functional correctness, syntax, integration with data files, adherence to element IDs, \"\n        \"and writes code_feedback.md starting with [APPROVED] or NEED_MODIFY. Artifact flow: app.py and templates/*.html authored by AppGenerator, \"\n        \"code_feedback.md authored by CodeCritic.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"AppGenerator\",\n            \"prompt\": \"\"\"You are a Python Flask Developer specializing in building full-stack web applications with local text file data management.\n\nYour goal is to translate design specifications into a complete, executable Flask application implementing all required pages, UI elements, routing, and data ingestion, then iteratively refine the code from critic feedback for at most two iterations.\n\nTask Details:\n- Read design_spec.md, existing app.py, templates/*.html, and code_feedback.md from CONTEXT\n- On the first iteration, implement the full application per design_spec.md starting at Dashboard, including all eight pages with exact element IDs\n- When code_feedback.md begins with NEED_MODIFY, revise and fully overwrite app.py and templates/*.html applying all corrections\n- When code_feedback.md begins with [APPROVED], finalize and preserve the approved code\n\n**Section 1: Application Structure and Routing**\n- Implement Flask routes for Dashboard, Current Weather, Weekly Forecast, Location Search, Weather Alerts, Air Quality, Saved Locations, and Settings pages\n- Ensure the starting page is the Dashboard\n- Use route functions matching design_spec.md specifications\n\n**Section 2: UI Elements and Templates**\n- Create templates/*.html files with exact element IDs as specified per page\n- Implement navigation via buttons with specified IDs to correct routes\n- Use Jinja2 templating for dynamic data injection from Python backend\n\n**Section 3: Data File Integration**\n- Read from local text files in the 'data' directory matching declared formats (current_weather.txt, forecasts.txt, locations.txt, alerts.txt, air_quality.txt, saved_locations.txt)\n- Parse data accurately and supply to templates as context variables\n- Handle data filtering and selection based on inputs like location and alerts\n\n**Section 4: Iteration and Refinement**\n- Run at most two Generator/Critic iterations\n- Apply every supported NEED_MODIFY correction without adding new features\n- Use the write_text_file tool to write app.py and templates/*.html files\n- Use validate_python_file tool to verify syntax and runtime before output\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file to save app.py and templates/*.html after each iteration\n- Use validate_python_file to check app.py correctness\n- Exactly handle input/output artifact names and data paths as declared\n- Start web app at Dashboard page with correct IDs and navigation\n- Do not add authentication or extraneous features\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\", \"validate_python_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"AppGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"AppGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"code_feedback.md\", \"source\": \"CodeCritic\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        },\n        {\n            \"agent_name\": \"CodeCritic\",\n            \"prompt\": \"\"\"You are a Software Test Engineer specializing in code and frontend review for Python Flask web applications.\n\nYour goal is to critically analyze the correctness, quality, and adherence of app.py and templates/*.html against design_spec.md and produce gated feedback for at most two iterations.\n\nTask Details:\n- Read design_spec.md, app.py, and templates/*.html from CONTEXT\n- Validate app.py syntax and runtime using validation tools\n- Verify all eight pages exist with correct Flask routes and starting page is Dashboard\n- Check templates for exact required element IDs and proper Jinja2 usage consistent with backend data\n- Confirm local text file data formats and loading code align with specification files (data/current_weather.txt etc.)\n- Check navigation buttons IDs and correct routing across pages\n- Write code_feedback.md starting with exactly [APPROVED] if fully compliant and error-free\n- Write NEED_MODIFY followed by detailed corrective instructions if issues found\n- Do not add requirements beyond design_spec.md\n\nReview Checklist:\n- Syntax and runtime correctness of app.py\n- Completeness of routing for all specified pages\n- Exact matching of element IDs in templates per design\n- Accurate data file parsing and integration with UI\n- Proper navigation flows with correct button IDs and targets\n- No unauthorized features or missing core functionality\n\nCRITICAL REQUIREMENTS:\n- Feedback artifact code_feedback.md must begin with [APPROVED] or NEED_MODIFY as byte-1 marker\n- Do not prepend feedback marker with any whitespace or text\n- Use write_text_file tool to save the complete feedback\n- Focus reviews strictly on declared inputs and outputs\n\nOutput: code_feedback.md\"\"\",\n            \"tools\": [\"write_text_file\", \"validate_python_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"AppGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"AppGenerator\"}\n            ],\n            \"output_artifacts\": [{\"type\": \"text_file\", \"name\": \"code_feedback.md\"}]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"AppGenerator\",\n            \"reviewer_agent\": \"CodeCritic\",\n            \"review_criteria\": (\n                \"Verify that app.py and templates/*.html fully implement the design_spec.md requirements without adding unauthorized features, \"\n                \"ensure code correctness, functional accuracy, proper use of element IDs, and seamless data file integration.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ]\n): pass",
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
    "DesignGenerator": {
        "prompt": (
            """You are a System Architect specializing in Python web application design specifications.

Your goal is to create a complete design_spec.md defining all eight pages (Dashboard, Current Weather, Weekly Forecast, Location Search, Weather Alerts, Air Quality, Saved Locations, Settings) with exact element IDs, navigation flow, and local text file data schema for the WeatherForecast web app. Revise this specification based on critic feedback for at most two iterations.

Task Details:
- Read user_task_description from CONTEXT
- Read existing design_spec.md and design_feedback.md when available
- On the first iteration, create the full design_spec.md describing page layouts, element IDs, navigation, and data storage formats as specified
- On feedback beginning with NEED_MODIFY, apply every correction and overwrite design_spec.md accordingly
- On feedback beginning with [APPROVED], preserve the approved design_spec.md

**Section 1: Page Layouts and Element IDs**
- Define each of the eight pages with their exact page titles and container element IDs
- List all specified UI elements per page with element IDs and types
- Ensure elements match the requirements for each page as described in user_task_description

**Section 2: Navigation Structure**
- Define user navigation flow among the eight pages
- Specify navigational button element IDs and their target pages/actions
- Ensure dashboard is the app start page and back buttons lead accordingly

**Section 3: Data Storage Formats**
- Specify exact local text file names and data schemas for current weather, forecasts, locations, alerts, air quality, saved locations
- Include field names, order, delimiters, and example data rows as given

CRITICAL SUCCESS CRITERIA:
- At most two iterations of Generator/Critic refinement loops
- Fully cover each page's layout and elements as per requirements
- Accurately define navigation element mappings and workflows
- Precisely describe each text file format aligned with requirement document
- Use write_text_file tool to output design_spec.md without adding extraneous sections or explanations

Output: design_spec.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignGenerator'}, {'type': 'text_file', 'name': 'design_feedback.md', 'source': 'DesignCritic'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_spec.md'}],

    },

    "DesignCritic": {
        "prompt": (
            """You are a Design Reviewer specializing in Python web application design verification and specification review.

Your goal is to review design_spec.md for completeness, consistency, and adherence to requirements regarding page layout, element IDs, navigation flow, and local text file data schemas. Provide gated feedback in design_feedback.md starting with [APPROVED] if fully compliant or NEED_MODIFY followed by detailed corrections. Refinement is limited to at most two iterations.

Task Details:
- Read user_task_description and design_spec.md from CONTEXT
- Review if all eight pages are described with required element IDs and page titles
- Verify navigational buttons and flows are logically and completely specified, with dashboard as start page
- Check data storage sections specify exact text file names, data formats, fields, delimiters, and sample data matching requirements
- Note any missing or inconsistent details that impair implementation or user navigation

Review Checklist:
1. All pages include specified container and UI element IDs matching requirements
2. Navigation links/buttons are correctly assigned and consistent with pages defined
3. Data file schemas fully match names, field order, delimiters, and example rows given
4. No contradictions or omissions in page design or data specifications
5. Feedback wording begins with exactly [APPROVED] or NEED_MODIFY, no other leading text or blank lines before marker

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save complete feedback in design_feedback.md
- Feedback must begin with [APPROVED] if no issues
- If NEED_MODIFY, list clear, actionable corrections only
- Limit to two review iterations maximum, stop upon approval

Output: design_feedback.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignGenerator'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_feedback.md'}],

    },

    "AppGenerator": {
        "prompt": (
            """You are a Python Flask Developer specializing in building full-stack web applications with local text file data management.

Your goal is to translate design specifications into a complete, executable Flask application implementing all required pages, UI elements, routing, and data ingestion, then iteratively refine the code from critic feedback for at most two iterations.

Task Details:
- Read design_spec.md, existing app.py, templates/*.html, and code_feedback.md from CONTEXT
- On the first iteration, implement the full application per design_spec.md starting at Dashboard, including all eight pages with exact element IDs
- When code_feedback.md begins with NEED_MODIFY, revise and fully overwrite app.py and templates/*.html applying all corrections
- When code_feedback.md begins with [APPROVED], finalize and preserve the approved code

**Section 1: Application Structure and Routing**
- Implement Flask routes for Dashboard, Current Weather, Weekly Forecast, Location Search, Weather Alerts, Air Quality, Saved Locations, and Settings pages
- Ensure the starting page is the Dashboard
- Use route functions matching design_spec.md specifications

**Section 2: UI Elements and Templates**
- Create templates/*.html files with exact element IDs as specified per page
- Implement navigation via buttons with specified IDs to correct routes
- Use Jinja2 templating for dynamic data injection from Python backend

**Section 3: Data File Integration**
- Read from local text files in the 'data' directory matching declared formats (current_weather.txt, forecasts.txt, locations.txt, alerts.txt, air_quality.txt, saved_locations.txt)
- Parse data accurately and supply to templates as context variables
- Handle data filtering and selection based on inputs like location and alerts

**Section 4: Iteration and Refinement**
- Run at most two Generator/Critic iterations
- Apply every supported NEED_MODIFY correction without adding new features
- Use the write_text_file tool to write app.py and templates/*.html files
- Use validate_python_file tool to verify syntax and runtime before output

CRITICAL REQUIREMENTS:
- Use write_text_file to save app.py and templates/*.html after each iteration
- Use validate_python_file to check app.py correctness
- Exactly handle input/output artifact names and data paths as declared
- Start web app at Dashboard page with correct IDs and navigation
- Do not add authentication or extraneous features

Output: app.py, templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file', 'validate_python_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignGenerator'}, {'type': 'text_file', 'name': 'app.py', 'source': 'AppGenerator'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'AppGenerator'}, {'type': 'text_file', 'name': 'code_feedback.md', 'source': 'CodeCritic'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}],

    },

    "CodeCritic": {
        "prompt": (
            """You are a Software Test Engineer specializing in code and frontend review for Python Flask web applications.

Your goal is to critically analyze the correctness, quality, and adherence of app.py and templates/*.html against design_spec.md and produce gated feedback for at most two iterations.

Task Details:
- Read design_spec.md, app.py, and templates/*.html from CONTEXT
- Validate app.py syntax and runtime using validation tools
- Verify all eight pages exist with correct Flask routes and starting page is Dashboard
- Check templates for exact required element IDs and proper Jinja2 usage consistent with backend data
- Confirm local text file data formats and loading code align with specification files (data/current_weather.txt etc.)
- Check navigation buttons IDs and correct routing across pages
- Write code_feedback.md starting with exactly [APPROVED] if fully compliant and error-free
- Write NEED_MODIFY followed by detailed corrective instructions if issues found
- Do not add requirements beyond design_spec.md

Review Checklist:
- Syntax and runtime correctness of app.py
- Completeness of routing for all specified pages
- Exact matching of element IDs in templates per design
- Accurate data file parsing and integration with UI
- Proper navigation flows with correct button IDs and targets
- No unauthorized features or missing core functionality

CRITICAL REQUIREMENTS:
- Feedback artifact code_feedback.md must begin with [APPROVED] or NEED_MODIFY as byte-1 marker
- Do not prepend feedback marker with any whitespace or text
- Use write_text_file tool to save the complete feedback
- Focus reviews strictly on declared inputs and outputs

Output: code_feedback.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file', 'validate_python_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignGenerator'}, {'type': 'text_file', 'name': 'app.py', 'source': 'AppGenerator'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'AppGenerator'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'code_feedback.md'}],

    }

}

REVIEW_PROFILES = {
    'DesignGenerator': [
        ("DesignCritic", """Ensure design_spec.md fully covers all stated requirements including page structure, element IDs, "
                "navigation logic, and correct specification of local text file data formats as per the requirements document. "
                "Check for clarity, completeness, and absence of contradictions.""", [{'type': 'text_file', 'name': 'design_spec.md'}])
    ],

    'AppGenerator': [
        ("CodeCritic", """Verify that app.py and templates/*.html fully implement the design_spec.md requirements without adding unauthorized features, "
                "ensure code correctness, functional accuracy, proper use of element IDs, and seamless data file integration.""", [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}])
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
    DesignGenerator = build_resilient_agent(
        chaos_controller=chaos_controller,
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
        chaos_controller=chaos_controller,
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
            "Create or revise the complete design_spec.md defining all eight pages, element IDs, navigation, and data storage formats.\n\n"
            f"=== Current design_spec.md ===\n{current_design}\n\n"
            f"=== DesignCritic Feedback ===\n{feedback_content}"
        )

        try:
            current_design = open("design_spec.md").read()
        except FileNotFoundError:
            current_design = ""

        await execute(
            DesignCritic,
            "Review the latest design_spec.md for completeness and adherence to user_task_description. "
            "Write design_feedback.md starting exactly with [APPROVED] or NEED_MODIFY with detailed feedback.\n\n"
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

async def implementation_and_verification_phase():
    import glob

    AppGenerator = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="AppGenerator",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=3,
        timeout_threshold=450,
        failure_threshold=2,
        recovery_time=50
    )
    CodeCritic = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="CodeCritic",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=3,
        timeout_threshold=400,
        failure_threshold=2,
        recovery_time=50
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

        # Compose prompt for AppGenerator with current artifacts and feedback
        await execute(
            AppGenerator,
            "Develop or refine the full Flask web application including app.py and all templates.\n\n"
            f"Design Specification (design_spec.md):\n{CONTEXT.get('design_spec.md','')}\n\n"
            f"Current app.py content:\n{app_content}\n\n"
            f"Current templates content:\n{templates_content}\n\n"
            f"CodeCritic feedback:\n{feedback_content}\n\n"
            "Apply the feedback if it starts with NEED_MODIFY; if [APPROVED], finalize and preserve the approved code."
        )

        # After AppGenerator finishes, reload contents for CodeCritic review
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

        # Have CodeCritic review the latest code and templates
        await execute(
            CodeCritic,
            "Review the Flask web application source code and templates to verify:\n"
            "- Syntax and runtime correctness\n"
            "- Inclusion of all eight specified pages with correct Flask routes\n"
            "- Starting page is Dashboard\n"
            "- Exact matching of all element IDs as specified\n"
            "- Proper data file parsing from declared 'data' folder files\n"
            "- Correct navigation button IDs and route targets\n"
            "- No unauthorized features or missing required functionality\n\n"
            f"Design Specification (design_spec.md):\n{CONTEXT.get('design_spec.md','')}\n\n"
            f"app.py content:\n{app_content}\n\n"
            f"Templates content:\n{templates_content}\n\n"
            "Write code_feedback.md starting with [APPROVED] if fully compliant, or NEED_MODIFY followed by detailed corrective instructions."
        )

        # Check the feedback content start to determine approval or continuation
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
