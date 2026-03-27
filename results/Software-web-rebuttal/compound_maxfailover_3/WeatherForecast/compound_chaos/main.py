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
    "phase1": "def architecture_design_phase(\n    goal: str = \"Produce a detailed design specification for the WeatherForecast app enabling independent backend and frontend development, delivered as design_spec.md\",\n    collab_pattern_name: str = \"Sequential Flow\",\n    collab_pattern_description: str = (\n        \"SystemArchitect writes design_spec.md covering 3 sections: Flask routes with names, methods, context variables; HTML templates with element IDs and nav mappings; Data schemas with exact field ordering for text storage.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"SystemArchitect\",\n            \"prompt\": \"\"\"You are a System Architect specializing in Flask web application design specifications.\n\nYour goal is to produce a detailed design specification document that enables Backend and Frontend developers to implement the WeatherForecast web app independently without relying on each other's implementation details.\n\nTask Details:\n- Read the user_task_description from CONTEXT\n- Create design_spec.md with three comprehensive sections: Flask routes, frontend HTML templates, and data file schemas\n- Include ALL necessary details for implementing routes, template element IDs, navigation links (url_for), and exact data file field orders\n- The document must cover the entire WeatherForecast app features and pages as described in input artifacts\n- Do NOT assume or modify data file formats; use the exact specifications provided\n- Do NOT include implementation code, focus on specifications only\n\n**Section 1: Flask Routes Specification**\n\nSpecify for each route:\n- URL path (e.g., /dashboard, /weather/current/<location_id>)\n- HTTP methods allowed (GET, POST)\n- Function name (snake_case, lowercase)\n- Template filename to render\n- Context variables passed to template, with type annotations (str, int, float, list, dict)\n- For lists of dicts, specify dict field structure explicitly\n\nRequirements:\n- Root route '/' must redirect to dashboard page\n- Include all pages: Dashboard, Current Weather, Weekly Forecast, Location Search, Alerts, Air Quality, Saved Locations, Settings\n- For routes with dynamic parameters (e.g., location_id), specify clearly\n- Context variables must match frontend template requirements exactly\n\n**Section 2: Frontend HTML Templates Specification**\n\nSpecify for each template:\n- File path and name (e.g., templates/dashboard.html)\n- Exact page title (for <title> and main headings <h1>)\n- Complete list of element IDs with element types and purpose\n- Navigation mappings: buttons/links to Flask route functions using url_for\n- Patterns for dynamic element IDs (e.g., select-location-button-{location_id})\n- Context variables available in template with type and structure\n- Usage notes on loops, conditionals, and dynamic data rendering\n\nRequirements:\n- Include ALL element IDs specified in user_task_description exactly (case-sensitive)\n- Navigation must use correct Flask function names and url_for parameters\n- Ensure frontend developers have complete info to implement templates independently\n\n**Section 3: Data File Schemas**\n\nSpecify for each data file:\n- File path and name under data/ directory (e.g., data/current_weather.txt)\n- Field order and pipe-delimited syntax (|)\n- Field names and descriptions, including data types\n- Short explanation of what data the file contains\n- 2-3 example lines illustrating realistic data following the format precisely\n\nRequirements:\n- Field order must match exactly for backend parsing\n- Use provided example data exactly to illustrate format\n- Do NOT include headers in data files (parsing starts at first line)\n- Cover all data files: current_weather, forecasts, locations, alerts, air_quality, saved_locations\n\nCRITICAL SUCCESS CRITERIA:\n- Design spec enables backend and frontend implementation with zero overlap or missing info\n- Strict format adherence ensures synchronization between frontend variables and backend routes\n- Use write_text_file tool to save design_spec.md\n- Do NOT add any implementation or testing code in specification\n- Do NOT modify provided data storage formats or example data\n\nOutput: design_spec.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"SystemArchitect\",\n            \"reviewer_agent\": \"BackendDeveloper\",\n            \"review_criteria\": (\n                \"Verify design_spec.md Section 1 for Flask routes including route URLs, HTTP methods, function names, and context variable definitions; \"\n                \"Section 3 for data schemas and local text file structures as specified; ensure completeness and correctness for backend implementation.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        },\n        {\n            \"source_agent\": \"SystemArchitect\",\n            \"reviewer_agent\": \"FrontendDeveloper\",\n            \"review_criteria\": (\n                \"Check design_spec.md Section 2 for frontend HTML templates specifications including exact element IDs, context variables usage, and navigation url_for mappings; \"\n                \"validate consistency and completeness for frontend implementation.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ]\n): pass",
    "phase2": "def parallel_implementation_phase(\n    goal: str = \"Concurrently implement backend app.py and frontend templates based on design_spec.md for WeatherForecast app\",\n    collab_pattern_name: str = \"Parallel Flow\",\n    collab_pattern_description: str = (\n        \"BackendDeveloper implements app.py including all Flask routes and data access per design_spec.md Sections 1 and 3; \"\n        \"FrontendDeveloper implements templates/*.html with all specified page designs and elements per design_spec.md Section 2.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"BackendDeveloper\",\n            \"prompt\": \"\"\"You are a Backend Developer specializing in Flask web applications.\n\nYour goal is to implement complete backend Flask application based strictly on design specification.\n\nTask Details:\n- Read design_spec.md Sections 1 (Flask Routes) and 3 (Data Schemas) ONLY from CONTEXT\n- Implement complete app.py including all Flask routes, handlers, and data loading mechanisms\n- Use exact data schemas and local file formats as specified in Section 3 for loading data from data/*.txt\n- Do NOT read or assume any frontend templates or code beyond what is specified in Sections 1 and 3\n- Do NOT add features or routes not listed in the specification\n\nImplementation Requirements:\n1. **Flask Application Setup:**\n   ```python\n   from flask import Flask, render_template, redirect, url_for, request\n   app = Flask(__name__)\n   app.config['SECRET_KEY'] = 'dev-secret-key'\n   ```\n\n2. **Root Route:**\n   - Implement '/' route to redirect to dashboard page using:\n     ```python\n     return redirect(url_for('dashboard'))\n     ```\n\n3. **Data Loading:**\n   - Load data from data/*.txt files using pipe-delimited parsing exactly as defined in Section 3\n   - Use safe file I/O with error handling\n   - Parse lines with `line.strip().split('|')` matching field order precisely\n   - Create appropriate data structures (lists, dicts) matching schema field names\n   - Data files have no headers; parsers start from first line\n\n4. **Route Implementations:**\n   - Create all routes specified in Section 1 with exact function names and HTTP methods\n   - Use render_template() with exact template file names as specified\n   - Pass exact context variables with correct names and types as specified\n   - Handle POST requests correctly when applicable (processing form data with request.form)\n\n5. **Best Practices:**\n   - Add `if __name__ == '__main__': app.run(debug=True, port=5000)`\n   - Use url_for() for redirects and links\n   - Handle missing or empty data gracefully without crashing\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save the complete app.py\n- Do NOT deviate from design_spec.md Sections 1 and 3 in naming, data formats, or routes\n- Do NOT add features, routes, or assumptions beyond specification\n- Do NOT provide code snippets only in messages—always output full code files\n- Ensure loaded data and route context variables exactly match specification\n\nOutput: app.py\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"SystemArchitect\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"}\n            ]\n        },\n        {\n            \"agent_name\": \"FrontendDeveloper\",\n            \"prompt\": \"\"\"You are a Frontend Developer specializing in HTML and Jinja2 templating for Flask web applications.\n\nYour goal is to implement comprehensive frontend HTML templates with all required page structures and element IDs, as specified in the design specification.\n\nTask Details:\n- Read design_spec.md Section 2 (HTML Templates) ONLY from CONTEXT\n- Implement all eight pages' HTML templates with exact element IDs, page titles, and navigation mappings\n- Do NOT access backend code, Section 1 (Flask Routes), or Section 3 (Data Schemas)\n- Do NOT assume or create elements or navigation beyond specification\n- Variable and context names must match exactly to specification\n\nImplementation Requirements:\n1. **Template Structure:**\n   ```html\n   <!DOCTYPE html>\n   <html lang=\"en\">\n   <head>\n       <meta charset=\"UTF-8\">\n       <title>Page Title from Specification</title>\n   </head>\n   <body>\n       <div id=\"page-container-id\">\n           <h1>Page Title from Specification</h1>\n           <!-- Additional page content -->\n       </div>\n   </body>\n   </html>\n   ```\n\n2. **File Naming and Locations:**\n   - Store templates under `templates/` directory\n   - Use exact file names as specified (e.g., dashboard.html, current_weather.html, etc.)\n   - Create one file per page\n\n3. **Element IDs:**\n   - Include all static and dynamic element IDs exactly as specified, including patterns like `select-location-button-{location_id}`\n   - Use Jinja2 templating for dynamic IDs:\n     ```html\n     id=\"select-location-button-{{ location.location_id }}\"\n     ```\n   - All IDs must match case and format precisely\n\n4. **Context Variables and Rendering:**\n   - Use Jinja2 syntax for looping, conditionals, and variable output\n   - Use exact variable names and field access as specified\n   - For loops, e.g. `{% for forecast in forecasts %}`\n\n5. **Navigation:**\n   - Implement all navigation buttons and links exactly as specified\n   - Use url_for with exact function names from specification\n   - For buttons, wrap in anchor tags if needed for navigation:\n     ```html\n     <a href=\"{{ url_for('function_name') }}\">\n         <button id=\"button-id\">Button Label</button>\n     </a>\n     ```\n\n6. **Form Inputs and POST Handling:**\n   - Use exact element IDs for inputs and buttons\n   - Use correct form methods and action URLs with url_for\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save all template files under templates/\n- All element IDs, page titles, and variable names must match spec exactly\n- Do NOT add extra pages, elements, or navigation not described in specification\n- Do NOT provide partial code snippets—always output full files\n- Each template file must be saved separately (e.g. templates/dashboard.html, templates/current_weather.html, etc.)\n\nOutput: templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"SystemArchitect\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"BackendDeveloper\",\n            \"reviewer_agent\": \"SystemArchitect\",\n            \"review_criteria\": (\n                \"Verify that app.py correctly implements all Flask routes with expected URL, methods, context variables, and uses correct data schemas and local file formats; \"\n                \"ensure root route redirects to dashboard as required.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\"}\n            ]\n        },\n        {\n            \"source_agent\": \"FrontendDeveloper\",\n            \"reviewer_agent\": \"SystemArchitect\",\n            \"review_criteria\": (\n                \"Verify all templates/*.html implement the element IDs, page titles, navigation routes, and context variables exactly as specified; \"\n                \"ensure full coverage of all eight pages.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ]\n): pass",
    "phase3": "def testing_and_validation_phase(\n    goal: str = \"Test and validate backend and frontend integration, local text file data handling, and UI correctness; produce test_report.md\",\n    collab_pattern_name: str = \"Sequential Flow\",\n    collab_pattern_description: str = (\n        \"Tester executes functional tests covering all Flask routes, verifies data files loading and saving correctness, and UI rendering per requirements; \"\n        \"Tester produces test_report.md detailing coverage and issues found.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"Tester\",\n            \"prompt\": \"\"\"You are a Software Test Engineer specializing in functional and integration testing for Flask web applications with local file data storage.\n\nYour goal is to perform comprehensive functional and integration testing covering backend Flask routes, frontend UI correctness, and local text file data storage consistency, producing a detailed test_report.md including test coverage and issues found.\n\nTask Details:\n- Read app.py, templates/*.html, and design_spec.md from CONTEXT fully\n- Verify all Flask routes implement user requirements, including correct HTTP methods and context variables\n- Validate data loading and saving for all specified data files in data/ directory per design_spec.md schemas\n- Test UI element presence and behavior for all pages and element IDs per design_spec.md and user requirements\n- Do NOT modify source code or design_spec.md; only perform tests and analysis\n- Write test_report.md with clear test cases, results, and summary\n- Write test_approval_status with either \"[APPROVED]\" if all criteria met or \"NEED_MODIFY\" if issues found\n\nTesting Requirements:\n1. **Functional Backend Tests**:\n   - Execute HTTP requests for all Flask routes covering GET and POST as specified\n   - Confirm correct rendering templates and context variable usage\n   - Validate data loading matches field order and format in text files\n\n2. **Frontend UI Validation**:\n   - Check presence and correctness of all required element IDs on each page\n   - Confirm navigation links and buttons correspond to specified routes\n   - Verify dynamic elements render correctly for sample data\n\n3. **Data Integrity Tests**:\n   - Load and parse all data files (current_weather.txt, forecasts.txt, locations.txt, alerts.txt, air_quality.txt, saved_locations.txt)\n   - Validate data format, field consistency, and absence of parsing errors\n   - Test saving/updating if applicable and verify persistence\n\n4. **Integration Testing**:\n   - Combine backend responses with frontend rendering to verify full user workflows (dashboard display, location search, forecast view, alerts acknowledgment, settings update)\n   - Check error handling for missing or malformed data\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save test_report.md and test_approval_status\n- Use execute_python_code tool for running test scripts as needed\n- Include explicit test coverage details and specify any failed cases or bugs found\n- Write \"[APPROVED]\" to test_approval_status only if all tests pass with no critical issues\n- Otherwise, write \"NEED_MODIFY\" to test_approval_status\n- Do NOT modify input source files or design documents\n\nOutput: test_report.md, test_approval_status\"\"\",\n            \"tools\": [\"write_text_file\", \"execute_python_code\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"BackendDeveloper\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"FrontendDeveloper\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"SystemArchitect\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"test_report.md\"},\n                {\"type\": \"string\", \"name\": \"test_approval_status\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"Tester\",\n            \"reviewer_agent\": \"SystemArchitect\",\n            \"review_criteria\": (\n                \"Review test_report.md for coverage completeness, critical issues and bug fixes suggestions; confirm the app fulfills the user requirements.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"test_report.md\"}\n            ]\n        },\n        {\n            \"source_agent\": \"Tester\",\n            \"reviewer_agent\": \"BackendDeveloper\",\n            \"review_criteria\": (\n                \"Review test_report.md for backend-specific test coverage, data integrity, and functional correctness.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"test_report.md\"}\n            ]\n        }\n    ]\n): pass",
    "phase4": "def refinement_loop_phase(\n    goal: str = \"Iteratively improve implementation based on testing feedback until approved\",\n    collab_pattern_name: str = \"Refinement Loop\",\n    collab_pattern_description: str = (\n        \"ImplementationRefiner revises app.py and templates/*.html based on feedback.md from Tester; \"\n        \"Tester reviews revised outputs and writes approval status '[APPROVED]' or 'NEED_MODIFY' in feedback.md; \"\n        \"Loop continues until Tester writes '[APPROVED]'.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"ImplementationRefiner\",\n            \"prompt\": \"\"\"You are a Full Stack Developer specializing in Flask web applications including backend and frontend code refinement.\n\nYour goal is to iteratively improve the backend (app.py) and frontend (templates/*.html) code based on tester feedback until the implementation meets quality standards and is approved.\n\nTask Details:\n- Read current app.py and all HTML templates from CONTEXT\n- Read feedback.md containing tester's detailed feedback and status markers\n- Update app.py and templates/*.html addressing all issues in feedback\n- Do NOT modify any other artifacts or add unrelated features\n\n**Guidelines for Refinement:**\n\n1. **Review Feedback Thoroughly:**\n   - Extract all issues and recommendations from feedback.md\n   - Identify specific backend or frontend problems mentioned\n\n2. **Backend Refinements (app.py):**\n   - Fix bugs or errors reported by Tester\n   - Improve code quality, readability, and compliance with requirements\n   - Ensure all dynamic routes and data handling match specifications\n\n3. **Frontend Refinements (templates/*.html):**\n   - Correct element IDs, layouts, and data bindings as per requirements\n   - Ensure consistent use of Jinja2 syntax and matching variable names\n   - Verify all buttons and navigation links function as specified\n\n4. **Iterative Updates:**\n   - Make minimal changes to address feedback precisely\n   - Do not add speculative features or unrelated modifications\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to overwrite updated app.py and templates/*.html files\n- Preserve filenames exactly; update all modified template files individually\n- Do NOT write feedback.md or other outputs\n- Wait for next testing cycle after writing outputs\n\nOutput: Updated app.py and templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"BackendDeveloper\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"FrontendDeveloper\"},\n                {\"type\": \"text_file\", \"name\": \"feedback.md\", \"source\": \"Tester\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        },\n        {\n            \"agent_name\": \"Tester\",\n            \"prompt\": \"\"\"You are a Software Test Engineer specializing in web application functional and UI testing for Flask projects.\n\nYour goal is to thoroughly test the backend code (app.py) and frontend templates (*.html) and provide detailed feedback in feedback.md including an approval status.\n\nTask Details:\n- Read the latest app.py and templates/*.html from CONTEXT\n- Execute app.py in a test environment to verify backend functionality\n- Inspect frontend templates for correct IDs, layout, data bindings, and navigation\n- Perform functional tests covering all user interactions and page requirements\n- Document all defects, missing features, or inconsistencies in feedback.md\n- Provide clear, actionable feedback for ImplementationRefiner\n\n**Testing and Feedback Requirements:**\n\n1. **Functional Testing:**\n   - Run the Flask app and verify all routes and pages load correctly\n   - Test data loading from all specified data files with correct parsing\n   - Check dynamic content, forms, buttons, and navigation behave per requirements\n\n2. **UI/UX Verification:**\n   - Verify all element IDs exist exactly as specified\n   - Ensure page titles match requirements\n   - Confirm correct display of data variables and templates syntax usage\n\n3. **Feedback File (feedback.md):**\n   - Summarize findings with error reports, suggestions, and observations\n   - Clearly state approval status line at document start or end:\n     - Write \"[APPROVED]\" if all criteria are met\n     - Write \"NEED_MODIFY\" if any issues are found\n\nCRITICAL REQUIREMENTS:\n- Use execute_python_code tool to run and test app.py as needed\n- Use write_text_file tool to save all feedback in feedback.md\n- Do NOT modify app.py or templates\n- Write explicit approval status \"[APPROVED]\" ONLY when all tests pass perfectly\n- Write \"NEED_MODIFY\" if corrections are necessary\n\nOutput: feedback.md\"\"\",\n            \"tools\": [\"write_text_file\", \"execute_python_code\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"ImplementationRefiner\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"ImplementationRefiner\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"feedback.md\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"ImplementationRefiner\",\n            \"reviewer_agent\": \"Tester\",\n            \"review_criteria\": (\n                \"Tester ensures app.py and templates meet all functional and UI requirements and writes approval status in feedback.md.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ]\n): pass",
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
    "SystemArchitect": {
        "prompt": (
            """You are a System Architect specializing in Flask web application design specifications.

Your goal is to produce a detailed design specification document that enables Backend and Frontend developers to implement the WeatherForecast web app independently without relying on each other's implementation details.

Task Details:
- Read the user_task_description from CONTEXT
- Create design_spec.md with three comprehensive sections: Flask routes, frontend HTML templates, and data file schemas
- Include ALL necessary details for implementing routes, template element IDs, navigation links (url_for), and exact data file field orders
- The document must cover the entire WeatherForecast app features and pages as described in input artifacts
- Do NOT assume or modify data file formats; use the exact specifications provided
- Do NOT include implementation code, focus on specifications only

**Section 1: Flask Routes Specification**

Specify for each route:
- URL path (e.g., /dashboard, /weather/current/<location_id>)
- HTTP methods allowed (GET, POST)
- Function name (snake_case, lowercase)
- Template filename to render
- Context variables passed to template, with type annotations (str, int, float, list, dict)
- For lists of dicts, specify dict field structure explicitly

Requirements:
- Root route '/' must redirect to dashboard page
- Include all pages: Dashboard, Current Weather, Weekly Forecast, Location Search, Alerts, Air Quality, Saved Locations, Settings
- For routes with dynamic parameters (e.g., location_id), specify clearly
- Context variables must match frontend template requirements exactly

**Section 2: Frontend HTML Templates Specification**

Specify for each template:
- File path and name (e.g., templates/dashboard.html)
- Exact page title (for <title> and main headings <h1>)
- Complete list of element IDs with element types and purpose
- Navigation mappings: buttons/links to Flask route functions using url_for
- Patterns for dynamic element IDs (e.g., select-location-button-{location_id})
- Context variables available in template with type and structure
- Usage notes on loops, conditionals, and dynamic data rendering

Requirements:
- Include ALL element IDs specified in user_task_description exactly (case-sensitive)
- Navigation must use correct Flask function names and url_for parameters
- Ensure frontend developers have complete info to implement templates independently

**Section 3: Data File Schemas**

Specify for each data file:
- File path and name under data/ directory (e.g., data/current_weather.txt)
- Field order and pipe-delimited syntax (|)
- Field names and descriptions, including data types
- Short explanation of what data the file contains
- 2-3 example lines illustrating realistic data following the format precisely

Requirements:
- Field order must match exactly for backend parsing
- Use provided example data exactly to illustrate format
- Do NOT include headers in data files (parsing starts at first line)
- Cover all data files: current_weather, forecasts, locations, alerts, air_quality, saved_locations

CRITICAL SUCCESS CRITERIA:
- Design spec enables backend and frontend implementation with zero overlap or missing info
- Strict format adherence ensures synchronization between frontend variables and backend routes
- Use write_text_file tool to save design_spec.md
- Do NOT add any implementation or testing code in specification
- Do NOT modify provided data storage formats or example data

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

Your goal is to implement complete backend Flask application based strictly on design specification.

Task Details:
- Read design_spec.md Sections 1 (Flask Routes) and 3 (Data Schemas) ONLY from CONTEXT
- Implement complete app.py including all Flask routes, handlers, and data loading mechanisms
- Use exact data schemas and local file formats as specified in Section 3 for loading data from data/*.txt
- Do NOT read or assume any frontend templates or code beyond what is specified in Sections 1 and 3
- Do NOT add features or routes not listed in the specification

Implementation Requirements:
1. **Flask Application Setup:**
   ```python
   from flask import Flask, render_template, redirect, url_for, request
   app = Flask(__name__)
   app.config['SECRET_KEY'] = 'dev-secret-key'
   ```

2. **Root Route:**
   - Implement '/' route to redirect to dashboard page using:
     ```python
     return redirect(url_for('dashboard'))
     ```

3. **Data Loading:**
   - Load data from data/*.txt files using pipe-delimited parsing exactly as defined in Section 3
   - Use safe file I/O with error handling
   - Parse lines with `line.strip().split('|')` matching field order precisely
   - Create appropriate data structures (lists, dicts) matching schema field names
   - Data files have no headers; parsers start from first line

4. **Route Implementations:**
   - Create all routes specified in Section 1 with exact function names and HTTP methods
   - Use render_template() with exact template file names as specified
   - Pass exact context variables with correct names and types as specified
   - Handle POST requests correctly when applicable (processing form data with request.form)

5. **Best Practices:**
   - Add `if __name__ == '__main__': app.run(debug=True, port=5000)`
   - Use url_for() for redirects and links
   - Handle missing or empty data gracefully without crashing

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save the complete app.py
- Do NOT deviate from design_spec.md Sections 1 and 3 in naming, data formats, or routes
- Do NOT add features, routes, or assumptions beyond specification
- Do NOT provide code snippets only in messages—always output full code files
- Ensure loaded data and route context variables exactly match specification

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

Your goal is to implement comprehensive frontend HTML templates with all required page structures and element IDs, as specified in the design specification.

Task Details:
- Read design_spec.md Section 2 (HTML Templates) ONLY from CONTEXT
- Implement all eight pages' HTML templates with exact element IDs, page titles, and navigation mappings
- Do NOT access backend code, Section 1 (Flask Routes), or Section 3 (Data Schemas)
- Do NOT assume or create elements or navigation beyond specification
- Variable and context names must match exactly to specification

Implementation Requirements:
1. **Template Structure:**
   ```html
   <!DOCTYPE html>
   <html lang="en">
   <head>
       <meta charset="UTF-8">
       <title>Page Title from Specification</title>
   </head>
   <body>
       <div id="page-container-id">
           <h1>Page Title from Specification</h1>
           <!-- Additional page content -->
       </div>
   </body>
   </html>
   ```

2. **File Naming and Locations:**
   - Store templates under `templates/` directory
   - Use exact file names as specified (e.g., dashboard.html, current_weather.html, etc.)
   - Create one file per page

3. **Element IDs:**
   - Include all static and dynamic element IDs exactly as specified, including patterns like `select-location-button-{location_id}`
   - Use Jinja2 templating for dynamic IDs:
     ```html
     id="select-location-button-{{ location.location_id }}"
     ```
   - All IDs must match case and format precisely

4. **Context Variables and Rendering:**
   - Use Jinja2 syntax for looping, conditionals, and variable output
   - Use exact variable names and field access as specified
   - For loops, e.g. `{% for forecast in forecasts %}`

5. **Navigation:**
   - Implement all navigation buttons and links exactly as specified
   - Use url_for with exact function names from specification
   - For buttons, wrap in anchor tags if needed for navigation:
     ```html
     <a href="{{ url_for('function_name') }}">
         <button id="button-id">Button Label</button>
     </a>
     ```

6. **Form Inputs and POST Handling:**
   - Use exact element IDs for inputs and buttons
   - Use correct form methods and action URLs with url_for

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save all template files under templates/
- All element IDs, page titles, and variable names must match spec exactly
- Do NOT add extra pages, elements, or navigation not described in specification
- Do NOT provide partial code snippets—always output full files
- Each template file must be saved separately (e.g. templates/dashboard.html, templates/current_weather.html, etc.)

Output: templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'SystemArchitect'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'templates/*.html'}],
    },

    "Tester": {
        "prompt": (
            """You are a Software Test Engineer specializing in functional and integration testing for Flask web applications with local file data storage.

Your goal is to perform comprehensive functional and integration testing covering backend Flask routes, frontend UI correctness, and local text file data storage consistency, producing a detailed test_report.md including test coverage and issues found.

Task Details:
- Read app.py, templates/*.html, and design_spec.md from CONTEXT fully
- Verify all Flask routes implement user requirements, including correct HTTP methods and context variables
- Validate data loading and saving for all specified data files in data/ directory per design_spec.md schemas
- Test UI element presence and behavior for all pages and element IDs per design_spec.md and user requirements
- Do NOT modify source code or design_spec.md; only perform tests and analysis
- Write test_report.md with clear test cases, results, and summary
- Write test_approval_status with either "[APPROVED]" if all criteria met or "NEED_MODIFY" if issues found

Testing Requirements:
1. **Functional Backend Tests**:
   - Execute HTTP requests for all Flask routes covering GET and POST as specified
   - Confirm correct rendering templates and context variable usage
   - Validate data loading matches field order and format in text files

2. **Frontend UI Validation**:
   - Check presence and correctness of all required element IDs on each page
   - Confirm navigation links and buttons correspond to specified routes
   - Verify dynamic elements render correctly for sample data

3. **Data Integrity Tests**:
   - Load and parse all data files (current_weather.txt, forecasts.txt, locations.txt, alerts.txt, air_quality.txt, saved_locations.txt)
   - Validate data format, field consistency, and absence of parsing errors
   - Test saving/updating if applicable and verify persistence

4. **Integration Testing**:
   - Combine backend responses with frontend rendering to verify full user workflows (dashboard display, location search, forecast view, alerts acknowledgment, settings update)
   - Check error handling for missing or malformed data

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save test_report.md and test_approval_status
- Use execute_python_code tool for running test scripts as needed
- Include explicit test coverage details and specify any failed cases or bugs found
- Write "[APPROVED]" to test_approval_status only if all tests pass with no critical issues
- Otherwise, write "NEED_MODIFY" to test_approval_status
- Do NOT modify input source files or design documents

Output: test_report.md, test_approval_status"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file', 'execute_python_code'],
        "input_artifacts": [{'type': 'text_file', 'name': 'app.py', 'source': 'BackendDeveloper'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'FrontendDeveloper'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'SystemArchitect'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'test_report.md'}, {'type': 'string', 'name': 'test_approval_status'}],
    },

    "ImplementationRefiner": {
        "prompt": (
            """You are a Full Stack Developer specializing in Flask web applications including backend and frontend code refinement.

Your goal is to iteratively improve the backend (app.py) and frontend (templates/*.html) code based on tester feedback until the implementation meets quality standards and is approved.

Task Details:
- Read current app.py and all HTML templates from CONTEXT
- Read feedback.md containing tester's detailed feedback and status markers
- Update app.py and templates/*.html addressing all issues in feedback
- Do NOT modify any other artifacts or add unrelated features

**Guidelines for Refinement:**

1. **Review Feedback Thoroughly:**
   - Extract all issues and recommendations from feedback.md
   - Identify specific backend or frontend problems mentioned

2. **Backend Refinements (app.py):**
   - Fix bugs or errors reported by Tester
   - Improve code quality, readability, and compliance with requirements
   - Ensure all dynamic routes and data handling match specifications

3. **Frontend Refinements (templates/*.html):**
   - Correct element IDs, layouts, and data bindings as per requirements
   - Ensure consistent use of Jinja2 syntax and matching variable names
   - Verify all buttons and navigation links function as specified

4. **Iterative Updates:**
   - Make minimal changes to address feedback precisely
   - Do not add speculative features or unrelated modifications

CRITICAL REQUIREMENTS:
- Use write_text_file tool to overwrite updated app.py and templates/*.html files
- Preserve filenames exactly; update all modified template files individually
- Do NOT write feedback.md or other outputs
- Wait for next testing cycle after writing outputs

Output: Updated app.py and templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'app.py', 'source': 'BackendDeveloper'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'FrontendDeveloper'}, {'type': 'text_file', 'name': 'feedback.md', 'source': 'Tester'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}],
    },

    "Tester": {
        "prompt": (
            """You are a Software Test Engineer specializing in web application functional and UI testing for Flask projects.

Your goal is to thoroughly test the backend code (app.py) and frontend templates (*.html) and provide detailed feedback in feedback.md including an approval status.

Task Details:
- Read the latest app.py and templates/*.html from CONTEXT
- Execute app.py in a test environment to verify backend functionality
- Inspect frontend templates for correct IDs, layout, data bindings, and navigation
- Perform functional tests covering all user interactions and page requirements
- Document all defects, missing features, or inconsistencies in feedback.md
- Provide clear, actionable feedback for ImplementationRefiner

**Testing and Feedback Requirements:**

1. **Functional Testing:**
   - Run the Flask app and verify all routes and pages load correctly
   - Test data loading from all specified data files with correct parsing
   - Check dynamic content, forms, buttons, and navigation behave per requirements

2. **UI/UX Verification:**
   - Verify all element IDs exist exactly as specified
   - Ensure page titles match requirements
   - Confirm correct display of data variables and templates syntax usage

3. **Feedback File (feedback.md):**
   - Summarize findings with error reports, suggestions, and observations
   - Clearly state approval status line at document start or end:
     - Write "[APPROVED]" if all criteria are met
     - Write "NEED_MODIFY" if any issues are found

CRITICAL REQUIREMENTS:
- Use execute_python_code tool to run and test app.py as needed
- Use write_text_file tool to save all feedback in feedback.md
- Do NOT modify app.py or templates
- Write explicit approval status "[APPROVED]" ONLY when all tests pass perfectly
- Write "NEED_MODIFY" if corrections are necessary

Output: feedback.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file', 'execute_python_code'],
        "input_artifacts": [{'type': 'text_file', 'name': 'app.py', 'source': 'ImplementationRefiner'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'ImplementationRefiner'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'feedback.md'}],
    }

}

REVIEW_PROFILES = {
    'SystemArchitect': [
        ("BackendDeveloper", """Verify design_spec.md Section 1 for Flask routes including route URLs, HTTP methods, function names, and context variable definitions; "
                "Section 3 for data schemas and local text file structures as specified; ensure completeness and correctness for backend implementation.""", [{'type': 'user', 'name': 'user_task_description'}, {'type': 'text_file', 'name': 'design_spec.md'}]),
        ("FrontendDeveloper", """Check design_spec.md Section 2 for frontend HTML templates specifications including exact element IDs, context variables usage, and navigation url_for mappings; "
                "validate consistency and completeness for frontend implementation.""", [{'type': 'user', 'name': 'user_task_description'}, {'type': 'text_file', 'name': 'design_spec.md'}])
    ],

    'BackendDeveloper': [
        ("SystemArchitect", """Verify that app.py correctly implements all Flask routes with expected URL, methods, context variables, and uses correct data schemas and local file formats; "
                "ensure root route redirects to dashboard as required.""", [{'type': 'text_file', 'name': 'design_spec.md'}, {'type': 'text_file', 'name': 'app.py'}])
    ],

    'FrontendDeveloper': [
        ("SystemArchitect", """Verify all templates/*.html implement the element IDs, page titles, navigation routes, and context variables exactly as specified; "
                "ensure full coverage of all eight pages.""", [{'type': 'text_file', 'name': 'design_spec.md'}, {'type': 'text_file', 'name': 'templates/*.html'}])
    ],

    'Tester': [
        ("SystemArchitect", """Review test_report.md for coverage completeness, critical issues and bug fixes suggestions; confirm the app fulfills the user requirements.""", [{'type': 'text_file', 'name': 'test_report.md'}]),
        ("BackendDeveloper", """Review test_report.md for backend-specific test coverage, data integrity, and functional correctness.""", [{'type': 'text_file', 'name': 'test_report.md'}])
    ],

    'ImplementationRefiner': [
        ("Tester", """Tester ensures app.py and templates meet all functional and UI requirements and writes approval status in feedback.md.""", [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}])
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
async def architecture_design_phase():
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
    await execute(
        SystemArchitect,
        "Produce design_spec.md with detailed Flask routes specification, frontend HTML templates details, and data file schemas based on user_task_description"
    )
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
        timeout_threshold=180,
        failure_threshold=1,
        recovery_time=40
    )

    # Execute both agents in parallel
    await asyncio.gather(
        execute(BackendDeveloper, "Implement complete backend app.py based on design_spec.md Sections 1 and 3"),
        execute(FrontendDeveloper, "Implement all frontend templates (*.html) based on design_spec.md Section 2")
    )
# Phase2_End

# Phase3_Start

async def testing_and_validation_phase():
    # Create Tester agent
    Tester = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="Tester",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase3"],
        max_retries=3,
        timeout_threshold=180,
        failure_threshold=1,
        recovery_time=40
    )

    # Execute Tester sequentially according to the Sequential Flow
    await execute(
        Tester,
        "Perform comprehensive functional and integration testing of app.py, templates/*.html, and design_spec.md; "
        "produce test_report.md and test_approval_status with [APPROVED] or NEED_MODIFY"
    )
# Phase3_End

# Phase4_Start

async def refinement_loop_phase():
    # Create agents
    ImplementationRefiner = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="ImplementationRefiner",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase4"],
        max_retries=3,
        timeout_threshold=200,
        failure_threshold=1,
        recovery_time=40
    )
    Tester = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="Tester",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase4"],
        max_retries=3,
        timeout_threshold=180,
        failure_threshold=1,
        recovery_time=40
    )

    MAX_LOOPS = 5
    for iteration in range(MAX_LOOPS):
        # Execute ImplementationRefiner to update app.py and templates based on feedback.md
        if iteration == 0:
            # Initial loop, assume feedback.md exists from prior testing phase
            await execute(ImplementationRefiner, "Refine app.py and templates/*.html based on feedback.md")
        else:
            # Read feedback.md content from CONTEXT to include in message
            try:
                with open("feedback.md", "r") as f:
                    feedback_content = f.read()
                await execute(ImplementationRefiner, f"Refine implementation addressing the following feedback:\n{feedback_content}")
            except FileNotFoundError:
                # If no feedback file, break the loop early
                break

        # Execute Tester to perform testing and write feedback.md
        await execute(Tester, "Thoroughly test app.py and templates/*.html and write feedback.md")

        # Read feedback.md to check for approval status
        try:
            with open("feedback.md", "r") as f:
                feedback_content = f.read()
            if "[APPROVED]" in feedback_content:
                break
        except FileNotFoundError:
            # If feedback.md missing, continue next iteration or break
            pass
# Phase4_End

# Orchestrate_Start

async def orchestrate():
    """Execute the complete multi-agent workflow in steps."""
    import time
    import json
    from pathlib import Path
    from essential_modules import aggregate_task_metrics
    orchestrate_start_time = time.time()

    step1 = [
        architecture_design_phase()
    ]
    step2 = [
        parallel_implementation_phase()
    ]
    step3 = [
        testing_and_validation_phase()
    ]
    step4 = [
        refinement_loop_phase()
    ]

    await asyncio.gather(*step1)
    await asyncio.gather(*step2)
    await asyncio.gather(*step3)
    await asyncio.gather(*step4)

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
