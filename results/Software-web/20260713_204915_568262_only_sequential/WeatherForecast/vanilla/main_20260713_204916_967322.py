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
# 20260713_204916_967322/main_20260713_204916_967322.py

# Phase_info dictionary containing complete def blocks for failover context
Phase_info = {
    "phase1": "def design_specification_phase(\n    goal: str = \"Analyze 'WeatherForecast' app requirements and produce a detailed design_spec.md covering all pages, elements, routes, and data fixtures.\",\n    collab_pattern_name: str = \"Sequential Flow\",\n    collab_pattern_description: str = (\n        \"RequirementsAnalyst first writes requirements_analysis.md capturing all user-visible features, page titles, UI elements with IDs, \"\n        \"route mappings, and data file usage; then WebArchitect reads it and produces design_spec.md, specifying Flask application architecture, \"\n        \"template filenames and layouts, route methods, context variables, and data file interaction.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"RequirementsAnalyst\",\n            \"prompt\": \"\"\"You are a Business Analyst specializing in requirements tracing for web applications.\n\nYour goal is to produce a detailed requirements_analysis.md that comprehensively captures all user-visible features, UI element IDs, page titles, routes, and data files expected.\n\nTask Details:\n- Read user_task_description fully\n- Extract and document every UI page with its page title and all elements IDs as specified\n- Identify and list all user-accessible routes and navigation mappings based on pages and buttons\n- List expected data files with their formats and example usage as described\n- Output a clear, organized markdown file requirements_analysis.md reflecting full user requirements\n\nInstructions:\n1. Systematically scan each page section and collect:\n   - Page Title\n   - All element IDs and their types (button, div, input, dropdown, etc.)\n   - Navigation buttons and their linked pages/routes\n2. Record routes derived from navigation buttons and pages\n3. Summarize all data files, their fields, formats, and example rows\n4. Organize requirements_analysis.md into sections: Pages & Elements, Routes, Data Files\n\nCritical Requirements:\n- Use write_text_file tool to save output as requirements_analysis.md\n- Preserve exact element IDs and page titles as in the user input\n- Provide concise and unambiguous mappings\n- Focus only on information explicitly given in user_task_description\n\nOutput: requirements_analysis.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"requirements_analysis.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"WebArchitect\",\n            \"prompt\": \"\"\"You are a Web Architect specializing in Flask web application design and architecture.\n\nYour goal is to produce a detailed design_spec.md that specifies Flask routes, HTTP methods, template file names and layout, exact element IDs, context variables, and data file interactions per user feature.\n\nTask Details:\n- Read requirements_analysis.md fully\n- Define complete Flask route table: route paths, function names, HTTP methods (GET/POST)\n- Specify template filenames under templates/ with required HTML element IDs per page\n- Enumerate context variables passed to each template with types and structures\n- Describe data file reading/loading logic aligned to user features and design\n- Output a comprehensive design_spec.md covering application architecture for both backend and frontend teams\n\nInstructions:\n1. Draft route specification mapping each page and button navigation to Flask URL routes and methods\n2. Detail template files naming conventions and layout including required element IDs exactly\n3. Specify context variables for each template reflecting data to display (e.g. dicts, lists, primitives)\n4. Document data file usage: filenames, field formats, parsing order, and integration points\n5. Organize design_spec.md into:\n   - Flask Routes and Methods\n   - Template Files, Element IDs, Context Variables\n   - Data File Interaction and Parsing Schemas\n\nCritical Requirements:\n- Use write_text_file tool to save output as design_spec.md\n- Maintain exact element ID names and page titles from requirements_analysis.md\n- Define function names consistent with routes and templates naming conventions\n- Ensure clarity to enable independent backend and frontend developments based on this spec\n\nOutput: design_spec.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"requirements_analysis.md\", \"source\": \"RequirementsAnalyst\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"RequirementsAnalyst\",\n            \"reviewer_agent\": \"WebArchitect\",\n            \"review_criteria\": (\n                \"Verify requirements_analysis.md covers all user-visible pages, exact element IDs, page titles, navigation paths, and required data files \"\n                \"before architecture begins.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\"},\n                {\"type\": \"text_file\", \"name\": \"requirements_analysis.md\"}\n            ]\n        }\n    ]\n): pass",
    "phase2": "def implementation_phase(\n    goal: str = \"Implement the 'WeatherForecast' Flask application as app_draft.py and templates/*.html drafts according to design_spec.md.\",\n    collab_pattern_name: str = \"Sequential Flow\",\n    collab_pattern_description: str = (\n        \"DraftEngineer develops app_draft.py with all routes and logic plus templates_draft/*.html files for each page based on design_spec.md; \"\n        \"then IntegrationEngineer integrates drafts into final app.py and templates/*.html with correct render_template calls and local data file usage.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"DraftEngineer\",\n            \"prompt\": \"\"\"You are a Backend Developer and Frontend Developer specializing in Flask web applications and HTML templating.\n\nYour goal is to create draft implementations of the Flask backend and HTML views using the given design specifications to form a foundation for final integration.\n\nTask Details:\n- Read design_spec.md fully for all Flask routes, page element IDs, layout, and navigation requirements\n- Implement app_draft.py with all Flask routes, logic placeholders for data access only (no real data loading)\n- Create templates_draft/*.html files with exact page element IDs, buttons, inputs, and layouts as specified\n- Use placeholder content and comments in draft code for file I/O and dynamic data rendering\n- Output draft backend as app_draft.py and draft frontend templates in templates_draft/*.html\n\nImplementation Instructions:\n1. Flask Backend Draft:\n   - Implement Flask routes exactly as specified (route paths, function names, HTTP methods)\n   - For dynamic routes, use route parameters as in design spec\n   - Include placeholder comments for data reading from text files (e.g., # TODO: Load current_weather.txt)\n   - Use render_template with template names from templates_draft directory\n   - Include route navigations but omit actual data logic (stub function bodies allowed)\n\n2. HTML Templates Draft:\n   - Create one HTML file per page as specified\n   - Include all required element IDs exactly as listed (divs, buttons, inputs, tables, etc.)\n   - Use minimal placeholder content or dummy text for areas requiring dynamic data\n   - Structure content and layout according to design spec overview and page elements\n   - Use static references to buttons and links for navigation controls only\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save app_draft.py and all templates_draft/*.html files\n- Ensure all element IDs match design_spec.md exactly (case sensitive, including dynamic ID patterns)\n- Draft code must not include actual data file reading or integration logic\n- Do not finalize code for deployment—focus on structure and placeholders only\n\nOutput: app_draft.py, templates_draft/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"WebArchitect\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_draft.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_draft/*.html\"}\n            ]\n        },\n        {\n            \"agent_name\": \"IntegrationEngineer\",\n            \"prompt\": \"\"\"You are a Backend Developer and Frontend Developer specializing in Flask applications with local data integration.\n\nYour goal is to build the final production-ready Flask backend and HTML templates by integrating data file reads and completing the draft implementations.\n\nTask Details:\n- Read design_spec.md for reference on routes, element IDs, context variables, and navigation mappings\n- Read app_draft.py and templates_draft/*.html as draft starting points\n- Convert app_draft.py into fully functional app.py, implementing data file reading from the 'data' directory\n- Adjust render_template calls to use templates/*.html\n- Complete all routes with correct data loading from local text files using exact field orders\n- Convert each templates_draft/*.html to templates/*.html, preserving all element IDs and adding dynamic content placeholders accordingly\n- Ensure all navigation and UI elements conform exactly to design_spec.md specifications\n\nImplementation Instructions:\n1. Backend Integration:\n   - Implement file I/O to read data from text files located in 'data' directory, parsing with pipe-delimited format\n   - Load all required data into appropriate structures to pass as context variables to templates\n   - Use exact function and route names and HTTP methods as per design_spec.md\n   - Use render_template with final templates/*.html paths\n   - Handle edge cases such as missing files or empty data gracefully\n\n2. Frontend Integration:\n   - For each draft template, create a corresponding final template with dynamic placeholders using Jinja2 syntax\n   - Replace static placeholders with loops, conditionals, and variable insertions to reflect live data\n   - Preserve all element IDs exactly as specified (static and dynamic patterns)\n   - Ensure navigation buttons and links use url_for() with correct route names and parameters\n\n3. Quality:\n   - Ensure consistent naming and data usage across backend and frontend\n   - Confirm that all dynamic UI elements correspond correctly to data provided by backend routes\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save final app.py and templates/*.html files\n- Preserve all element IDs with case sensitivity and pattern accuracy\n- Data file parsing must match design_spec.md exact field orders for all data files\n- All render_template calls must refer to templates/*.html, not drafts\n- Ensure full feature completion as per design_spec.md\n- Avoid leaving stub placeholders—fully implement data retrieval and rendering for all routes\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"WebArchitect\"},\n                {\"type\": \"text_file\", \"name\": \"app_draft.py\", \"source\": \"DraftEngineer\"},\n                {\"type\": \"text_file\", \"name\": \"templates_draft/*.html\", \"source\": \"DraftEngineer\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"DraftEngineer\",\n            \"reviewer_agent\": \"IntegrationEngineer\",\n            \"review_criteria\": (\n                \"Ensure the draft app_draft.py and templates_draft/*.html correctly implement all routes and UI elements as per design_spec.md before integration.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"},\n                {\"type\": \"text_file\", \"name\": \"app_draft.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_draft/*.html\"}\n            ]\n        }\n    ]\n): pass",
    "phase3": "def verification_phase(\n    goal: str = \"Validate final app.py and templates/*.html to ensure correct functionality, route coverage, UI elements, and data integration.\",\n    collab_pattern_name: str = \"Sequential Flow\",\n    collab_pattern_description: str = (\n        \"WebValidator conducts thorough syntax, runtime, and functional validation on app.py and templates/*.html producing validation_report.md; \"\n        \"SequentialFixer applies all fixes identified and writes final corrected app.py and templates/*.html.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"WebValidator\",\n            \"prompt\": \"\"\"You are a Software Test Engineer specializing in web application validation and quality assurance.\n\nYour goal is to thoroughly validate the final backend and frontend implementation for correctness, covering syntax, runtime, route coverage, UI elements, and data integration. Your deliverable is a detailed validation_report.md.\n\nTask Details:\n- Read design_spec.md to understand expected routes, templates, element IDs, and data schemas\n- Validate app.py for Python syntax and runtime errors, ensuring it starts and runs correctly\n- Validate templates/*.html for presence of all specified element IDs and correct template rendering\n- Check that all routes defined in design_spec.md are implemented in app.py and render correct templates\n- Verify data files are used according to defined schemas and loaded correctly in the backend\n- Produce comprehensive validation_report.md describing findings with error traces and test results\n\nValidation Requirements:\n1. Syntax and Runtime Validation:\n   - Use validate_python_file tool for app.py syntax and runtime checks\n   - Use execute_python_code to attempt starting the Flask app or test key functions (simulate requests)\n\n2. Route and Template Coverage:\n   - Verify each route in design_spec.md Section 1 is implemented and renders correct template\n   - Confirm all HTML templates contain required element IDs exactly as specified\n\n3. Data Integration:\n   - Check usage and correctness of data files as per design_spec.md Section 3\n   - Confirm that field parsing matches specified schemas with exact field order\n\nCRITICAL REQUIREMENTS:\n- Use validate_python_file and execute_python_code tools for validations\n- Use write_text_file tool to output detailed validation_report.md\n- Validation report must clearly state all errors, warnings, and passes\n- Focus strictly on artifacts: app.py, templates/*.html, and design_spec.md\n- Provide actionable, descriptive feedback suitable for fixing in next phase\n\nOutput: validation_report.md\"\"\",\n            \"tools\": [\"validate_python_file\", \"execute_python_code\", \"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"WebArchitect\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"IntegrationEngineer\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"IntegrationEngineer\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_report.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"SequentialFixer\",\n            \"prompt\": \"\"\"You are a Software Developer specializing in sequential bug fixing and compliance enforcement for web applications.\n\nYour goal is to apply all corrections from validation_report.md to produce the final versions of app.py and templates/*.html fully compliant with design_spec.md and user requirements.\n\nTask Details:\n- Read validation_report.md for all identified issues and suggested fixes\n- Review current app.py and templates/*.html implementations\n- Update app.py and templates/*.html to fix all backend and frontend issues:\n  - Correct syntax and runtime errors\n  - Ensure full route coverage and correct template rendering\n  - Fix missing or incorrect UI element IDs\n  - Align data loading and usage with design_spec.md schemas\n- Produce final corrected app.py and templates/*.html ready for deployment\n\nFixing Guidelines:\n1. Prioritize critical errors affecting app startup or core functionality\n2. Address all missing or mismatched element IDs in templates\n3. Ensure all fixes conform strictly to design_spec.md specifications without adding extra features\n4. Maintain code quality, readability, and consistency\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save final app.py and all templates/*.html files\n- Fully resolve all validation_report.md issues without omissions\n- Maintain artifact filename conventions exactly as provided\n- Do not modify unrelated code or templates beyond necessary fixes\n- Deliver production-ready, error-free backend and frontend codebase\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_report.md\", \"source\": \"WebValidator\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"IntegrationEngineer\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"IntegrationEngineer\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"WebArchitect\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"WebValidator\",\n            \"reviewer_agent\": \"SequentialFixer\",\n            \"review_criteria\": (\n                \"Verify validation_report.md contains exhaustive test coverage results, error traces, and actionable fixes for both backend and frontend.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_report.md\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        },\n        {\n            \"source_agent\": \"SequentialFixer\",\n            \"reviewer_agent\": \"RequirementsAnalyst\",\n            \"review_criteria\": (\n                \"Confirm that the final app.py and templates/*.html address all validation issues and fully implement all user requirements \"\n                \"from requirements_analysis.md.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_report.md\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"},\n                {\"type\": \"text_file\", \"name\": \"requirements_analysis.md\"}\n            ]\n        }\n    ]\n): pass",
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
    "RequirementsAnalyst": {
        "prompt": (
            """You are a Business Analyst specializing in requirements tracing for web applications.

Your goal is to produce a detailed requirements_analysis.md that comprehensively captures all user-visible features, UI element IDs, page titles, routes, and data files expected.

Task Details:
- Read user_task_description fully
- Extract and document every UI page with its page title and all elements IDs as specified
- Identify and list all user-accessible routes and navigation mappings based on pages and buttons
- List expected data files with their formats and example usage as described
- Output a clear, organized markdown file requirements_analysis.md reflecting full user requirements

Instructions:
1. Systematically scan each page section and collect:
   - Page Title
   - All element IDs and their types (button, div, input, dropdown, etc.)
   - Navigation buttons and their linked pages/routes
2. Record routes derived from navigation buttons and pages
3. Summarize all data files, their fields, formats, and example rows
4. Organize requirements_analysis.md into sections: Pages & Elements, Routes, Data Files

Critical Requirements:
- Use write_text_file tool to save output as requirements_analysis.md
- Preserve exact element IDs and page titles as in the user input
- Provide concise and unambiguous mappings
- Focus only on information explicitly given in user_task_description

Output: requirements_analysis.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'requirements_analysis.md'}],

    },

    "WebArchitect": {
        "prompt": (
            """You are a Web Architect specializing in Flask web application design and architecture.

Your goal is to produce a detailed design_spec.md that specifies Flask routes, HTTP methods, template file names and layout, exact element IDs, context variables, and data file interactions per user feature.

Task Details:
- Read requirements_analysis.md fully
- Define complete Flask route table: route paths, function names, HTTP methods (GET/POST)
- Specify template filenames under templates/ with required HTML element IDs per page
- Enumerate context variables passed to each template with types and structures
- Describe data file reading/loading logic aligned to user features and design
- Output a comprehensive design_spec.md covering application architecture for both backend and frontend teams

Instructions:
1. Draft route specification mapping each page and button navigation to Flask URL routes and methods
2. Detail template files naming conventions and layout including required element IDs exactly
3. Specify context variables for each template reflecting data to display (e.g. dicts, lists, primitives)
4. Document data file usage: filenames, field formats, parsing order, and integration points
5. Organize design_spec.md into:
   - Flask Routes and Methods
   - Template Files, Element IDs, Context Variables
   - Data File Interaction and Parsing Schemas

Critical Requirements:
- Use write_text_file tool to save output as design_spec.md
- Maintain exact element ID names and page titles from requirements_analysis.md
- Define function names consistent with routes and templates naming conventions
- Ensure clarity to enable independent backend and frontend developments based on this spec

Output: design_spec.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'requirements_analysis.md', 'source': 'RequirementsAnalyst'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_spec.md'}],

    },

    "DraftEngineer": {
        "prompt": (
            """You are a Backend Developer and Frontend Developer specializing in Flask web applications and HTML templating.

Your goal is to create draft implementations of the Flask backend and HTML views using the given design specifications to form a foundation for final integration.

Task Details:
- Read design_spec.md fully for all Flask routes, page element IDs, layout, and navigation requirements
- Implement app_draft.py with all Flask routes, logic placeholders for data access only (no real data loading)
- Create templates_draft/*.html files with exact page element IDs, buttons, inputs, and layouts as specified
- Use placeholder content and comments in draft code for file I/O and dynamic data rendering
- Output draft backend as app_draft.py and draft frontend templates in templates_draft/*.html

Implementation Instructions:
1. Flask Backend Draft:
   - Implement Flask routes exactly as specified (route paths, function names, HTTP methods)
   - For dynamic routes, use route parameters as in design spec
   - Include placeholder comments for data reading from text files (e.g., # TODO: Load current_weather.txt)
   - Use render_template with template names from templates_draft directory
   - Include route navigations but omit actual data logic (stub function bodies allowed)

2. HTML Templates Draft:
   - Create one HTML file per page as specified
   - Include all required element IDs exactly as listed (divs, buttons, inputs, tables, etc.)
   - Use minimal placeholder content or dummy text for areas requiring dynamic data
   - Structure content and layout according to design spec overview and page elements
   - Use static references to buttons and links for navigation controls only

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save app_draft.py and all templates_draft/*.html files
- Ensure all element IDs match design_spec.md exactly (case sensitive, including dynamic ID patterns)
- Draft code must not include actual data file reading or integration logic
- Do not finalize code for deployment—focus on structure and placeholders only

Output: app_draft.py, templates_draft/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'WebArchitect'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app_draft.py'}, {'type': 'text_file', 'name': 'templates_draft/*.html'}],

    },

    "IntegrationEngineer": {
        "prompt": (
            """You are a Backend Developer and Frontend Developer specializing in Flask applications with local data integration.

Your goal is to build the final production-ready Flask backend and HTML templates by integrating data file reads and completing the draft implementations.

Task Details:
- Read design_spec.md for reference on routes, element IDs, context variables, and navigation mappings
- Read app_draft.py and templates_draft/*.html as draft starting points
- Convert app_draft.py into fully functional app.py, implementing data file reading from the 'data' directory
- Adjust render_template calls to use templates/*.html
- Complete all routes with correct data loading from local text files using exact field orders
- Convert each templates_draft/*.html to templates/*.html, preserving all element IDs and adding dynamic content placeholders accordingly
- Ensure all navigation and UI elements conform exactly to design_spec.md specifications

Implementation Instructions:
1. Backend Integration:
   - Implement file I/O to read data from text files located in 'data' directory, parsing with pipe-delimited format
   - Load all required data into appropriate structures to pass as context variables to templates
   - Use exact function and route names and HTTP methods as per design_spec.md
   - Use render_template with final templates/*.html paths
   - Handle edge cases such as missing files or empty data gracefully

2. Frontend Integration:
   - For each draft template, create a corresponding final template with dynamic placeholders using Jinja2 syntax
   - Replace static placeholders with loops, conditionals, and variable insertions to reflect live data
   - Preserve all element IDs exactly as specified (static and dynamic patterns)
   - Ensure navigation buttons and links use url_for() with correct route names and parameters

3. Quality:
   - Ensure consistent naming and data usage across backend and frontend
   - Confirm that all dynamic UI elements correspond correctly to data provided by backend routes

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save final app.py and templates/*.html files
- Preserve all element IDs with case sensitivity and pattern accuracy
- Data file parsing must match design_spec.md exact field orders for all data files
- All render_template calls must refer to templates/*.html, not drafts
- Ensure full feature completion as per design_spec.md
- Avoid leaving stub placeholders—fully implement data retrieval and rendering for all routes

Output: app.py, templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'WebArchitect'}, {'type': 'text_file', 'name': 'app_draft.py', 'source': 'DraftEngineer'}, {'type': 'text_file', 'name': 'templates_draft/*.html', 'source': 'DraftEngineer'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}],

    },

    "WebValidator": {
        "prompt": (
            """You are a Software Test Engineer specializing in web application validation and quality assurance.

Your goal is to thoroughly validate the final backend and frontend implementation for correctness, covering syntax, runtime, route coverage, UI elements, and data integration. Your deliverable is a detailed validation_report.md.

Task Details:
- Read design_spec.md to understand expected routes, templates, element IDs, and data schemas
- Validate app.py for Python syntax and runtime errors, ensuring it starts and runs correctly
- Validate templates/*.html for presence of all specified element IDs and correct template rendering
- Check that all routes defined in design_spec.md are implemented in app.py and render correct templates
- Verify data files are used according to defined schemas and loaded correctly in the backend
- Produce comprehensive validation_report.md describing findings with error traces and test results

Validation Requirements:
1. Syntax and Runtime Validation:
   - Use validate_python_file tool for app.py syntax and runtime checks
   - Use execute_python_code to attempt starting the Flask app or test key functions (simulate requests)

2. Route and Template Coverage:
   - Verify each route in design_spec.md Section 1 is implemented and renders correct template
   - Confirm all HTML templates contain required element IDs exactly as specified

3. Data Integration:
   - Check usage and correctness of data files as per design_spec.md Section 3
   - Confirm that field parsing matches specified schemas with exact field order

CRITICAL REQUIREMENTS:
- Use validate_python_file and execute_python_code tools for validations
- Use write_text_file tool to output detailed validation_report.md
- Validation report must clearly state all errors, warnings, and passes
- Focus strictly on artifacts: app.py, templates/*.html, and design_spec.md
- Provide actionable, descriptive feedback suitable for fixing in next phase

Output: validation_report.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['validate_python_file', 'execute_python_code', 'write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'WebArchitect'}, {'type': 'text_file', 'name': 'app.py', 'source': 'IntegrationEngineer'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'IntegrationEngineer'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'validation_report.md'}],

    },

    "SequentialFixer": {
        "prompt": (
            """You are a Software Developer specializing in sequential bug fixing and compliance enforcement for web applications.

Your goal is to apply all corrections from validation_report.md to produce the final versions of app.py and templates/*.html fully compliant with design_spec.md and user requirements.

Task Details:
- Read validation_report.md for all identified issues and suggested fixes
- Review current app.py and templates/*.html implementations
- Update app.py and templates/*.html to fix all backend and frontend issues:
  - Correct syntax and runtime errors
  - Ensure full route coverage and correct template rendering
  - Fix missing or incorrect UI element IDs
  - Align data loading and usage with design_spec.md schemas
- Produce final corrected app.py and templates/*.html ready for deployment

Fixing Guidelines:
1. Prioritize critical errors affecting app startup or core functionality
2. Address all missing or mismatched element IDs in templates
3. Ensure all fixes conform strictly to design_spec.md specifications without adding extra features
4. Maintain code quality, readability, and consistency

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save final app.py and all templates/*.html files
- Fully resolve all validation_report.md issues without omissions
- Maintain artifact filename conventions exactly as provided
- Do not modify unrelated code or templates beyond necessary fixes
- Deliver production-ready, error-free backend and frontend codebase

Output: app.py, templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'validation_report.md', 'source': 'WebValidator'}, {'type': 'text_file', 'name': 'app.py', 'source': 'IntegrationEngineer'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'IntegrationEngineer'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'WebArchitect'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}],

    }

}

REVIEW_PROFILES = {
    'RequirementsAnalyst': [
        ("WebArchitect", """Verify requirements_analysis.md covers all user-visible pages, exact element IDs, page titles, navigation paths, and required data files "
                "before architecture begins.""", [{'type': 'user', 'name': 'user_task_description'}, {'type': 'text_file', 'name': 'requirements_analysis.md'}])
    ],

    'DraftEngineer': [
        ("IntegrationEngineer", """Ensure the draft app_draft.py and templates_draft/*.html correctly implement all routes and UI elements as per design_spec.md before integration.""", [{'type': 'text_file', 'name': 'design_spec.md'}, {'type': 'text_file', 'name': 'app_draft.py'}, {'type': 'text_file', 'name': 'templates_draft/*.html'}])
    ],

    'WebValidator': [
        ("SequentialFixer", """Verify validation_report.md contains exhaustive test coverage results, error traces, and actionable fixes for both backend and frontend.""", [{'type': 'text_file', 'name': 'validation_report.md'}, {'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}, {'type': 'text_file', 'name': 'design_spec.md'}])
    ],

    'SequentialFixer': [
        ("RequirementsAnalyst", """Confirm that the final app.py and templates/*.html address all validation issues and fully implement all user requirements "
                "from requirements_analysis.md.""", [{'type': 'text_file', 'name': 'validation_report.md'}, {'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}, {'type': 'text_file', 'name': 'requirements_analysis.md'}])
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
        timeout_threshold=220,
        failure_threshold=1,
        recovery_time=30
    )
    WebArchitect = build_resilient_agent(
        agent_name="WebArchitect",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=2,
        timeout_threshold=250,
        failure_threshold=1,
        recovery_time=30
    )

    # Sequential execution: RequirementsAnalyst then WebArchitect
    await execute(RequirementsAnalyst, "Analyze user_task_description and produce requirements_analysis.md covering all pages, element IDs, routes, and data files.")
    requirements_analysis_content = ""
    try:
        requirements_analysis_content = open("requirements_analysis.md").read()
    except:
        pass

    await execute(WebArchitect,
                  f"Read requirements_analysis.md and produce design_spec.md specifying Flask routes, HTTP methods, template files, element IDs, context variables, and data file interactions.\n\n"
                  f"=== requirements_analysis.md ===\n{requirements_analysis_content}")
# Phase1_End

# Phase2_Start

async def implementation_phase():
    # Create agents
    DraftEngineer = build_resilient_agent(
        agent_name="DraftEngineer",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=2,
        timeout_threshold=260,
        failure_threshold=1,
        recovery_time=40
    )
    IntegrationEngineer = build_resilient_agent(
        agent_name="IntegrationEngineer",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=3,
        timeout_threshold=320,
        failure_threshold=1,
        recovery_time=50
    )

    # Sequential Flow
    # Step 1: DraftEngineer creates app_draft.py and templates_draft/*.html based on design_spec.md
    await execute(DraftEngineer, "Implement draft Flask backend as app_draft.py with route placeholders and templates_draft/*.html with exact element IDs and layouts from design_spec.md using placeholders for data and logic")

    # Read draft artifacts for IntegrationEngineer
    app_draft_content = ""
    templates_draft_content = ""
    try:
        app_draft_content = open("app_draft.py").read()
    except:
        pass
    try:
        # As templates_draft/*.html is a pattern, read all draft templates content concatenated
        import glob
        draft_files = glob.glob("templates_draft/*.html")
        contents = []
        for file in draft_files:
            try:
                contents.append(f"=== {file} ===\n" + open(file).read())
            except:
                pass
        templates_draft_content = "\n\n".join(contents)
    except:
        pass

    # Step 2: IntegrationEngineer integrates drafts into final app.py and templates/*.html with full data integration
    await execute(IntegrationEngineer,
        f"Integrate draft backend and frontend to fully functional app.py and templates/*.html. "
        f"Use design_spec.md, app_draft.py, and all templates_draft/*.html. "
        f"Implement file I/O from 'data' directory, parse exact field orders, convert templates with Jinja2 dynamic placeholders, preserve all element IDs and navigation as per design_spec.md.\n\n"
        f"=== app_draft.py ===\n{app_draft_content}\n\n=== Templates Draft ===\n{templates_draft_content}"
    )
# Phase2_End

# Phase3_Start
import asyncio

async def verification_phase():
    WebValidator = build_resilient_agent(
        agent_name="WebValidator",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase3"],
        max_retries=3,
        timeout_threshold=400,
        failure_threshold=2,
        recovery_time=60
    )
    SequentialFixer = build_resilient_agent(
        agent_name="SequentialFixer",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase3"],
        max_retries=3,
        timeout_threshold=400,
        failure_threshold=2,
        recovery_time=60
    )

    # Execute WebValidator to produce validation_report.md
    await execute(WebValidator,
                  "Perform thorough validation of app.py syntax and runtime using validate_python_file and execute_python_code tools. "
                  "Check that all routes from design_spec.md are implemented and render correct templates. "
                  "Verify all required UI element IDs are present in templates/*.html, ensure data files usage matches design_spec.md schemas. "
                  "Produce comprehensive validation_report.md with detailed findings, error traces, warnings, and passes.")

    # Read validation report content
    validation_report_content = ""
    try:
        with open("validation_report.md", "r") as f:
            validation_report_content = f.read()
    except FileNotFoundError:
        validation_report_content = ""

    # Execute SequentialFixer to fix all issues based on validation_report.md
    # Inject validation_report.md content directly for fixing
    await execute(SequentialFixer,
                  f"Apply all corrections identified in validation_report.md to produce final versions of app.py and templates/*.html. "
                  f"Fix syntax/runtime errors, complete route coverage, correct template UI element IDs, and align data loading with design_spec.md. "
                  f"Produce production-ready, error-free backend and frontend code.\n\n"
                  f"=== Validation Report ===\n"
                  f"{validation_report_content}")
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
