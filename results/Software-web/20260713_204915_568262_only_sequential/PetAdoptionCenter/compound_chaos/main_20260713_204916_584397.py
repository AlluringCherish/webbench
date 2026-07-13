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
# 20260713_204916_584397/main_20260713_204916_584397.py

# Phase_info dictionary containing complete def blocks for failover context
Phase_info = {
    "phase1": "def design_specification_phase(\n    goal: str = \"Analyze the PetAdoptionCenter requirements and produce a complete design_spec.md describing all pages, routes, data files, and UI element mappings\",\n    collab_pattern_name: str = \"Sequential Flow\",\n    collab_pattern_description: str = (\n        \"RequirementsAnalyst first writes requirements_analysis.md with detailed page elements and data descriptions; only after it \"\n        \"completes, WebArchitect converts it into design_spec.md with precise Flask architecture, route definitions, data access strategies, \"\n        \"and UI contract specifications.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"RequirementsAnalyst\",\n            \"prompt\": \"\"\"You are a Business Analyst specializing in extracting detailed requirements from user task descriptions for web applications.\n\nYour goal is to produce a comprehensive requirements_analysis.md document that fully captures all user requirements, UI element specifications, page titles, data file formats, and user interaction flows from the user task description.\n\nTask Details:\n- Read the user_task_description artifact carefully\n- Extract every page with its exact name, title, and UI elements including element IDs and types\n- Document all data file formats with exact field order and example data\n- Describe user navigation flows and button actions linking pages\n\nSpecification Requirements:\n1. Page Specifications:\n   - List each page with exact page title and all element IDs & types as provided\n   - Include descriptions of element purposes where available\n2. Data Files:\n   - List each data file with filename, field order as pipe-delimited format, and example data rows\n3. User Flows:\n   - Describe navigation buttons and how users move between pages\n   - Highlight starting page as Dashboard\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save the artifact requirements_analysis.md\n- Keep all details exact as per user description without assumptions\n- Structure the document clearly for easy transformation by next agent\n\nOutput: requirements_analysis.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"requirements_analysis.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"WebArchitect\",\n            \"prompt\": \"\"\"You are a Web Architect specializing in Flask web applications and UI contract design.\n\nYour goal is to convert requirements_analysis.md into a detailed design_spec.md that defines the complete Flask route architecture, page-to-template mappings, exact UI element IDs and types per page, navigation logic starting from the Dashboard, local data storage schemas in the data/ directory, and interaction contracts for all user flows and UI buttons.\n\nTask Details:\n- Read user_task_description and requirements_analysis.md artifacts\n- Create design_spec.md specifying:\n  * Flask route table with routes, function names, HTTP methods, templates, context variables\n  * Mapping of pages to HTML templates with exact element IDs and their types\n  * Navigation rules for buttons and links (starting at Dashboard)\n  * Data storage file schemas matching provided formats and field order under data/\n  * Interaction contracts documenting actions triggered by UI elements\n\nDesign Spec Requirements:\n1. Flask Route Architecture:\n   - Define route paths with example: '/', '/pets', '/pet/<int:pet_id>'\n   - Specify function names (lowercase underscore style)\n   - HTTP methods: GET for views, POST for form submissions (e.g., adding pet, submitting applications)\n   - Associate each route with its template file and passed context variables with types\n\n2. Page and Template Mapping:\n   - Assign each page to a template file: templates/{page_name}.html\n   - List all UI element IDs and types exactly\n   - Define context variables provided to templates and their structure (list/dict/str/int, etc.)\n\n3. Navigation Logic:\n   - Specify button/link actions using url_for function names\n   - Mark Dashboard as the initial landing page ('/')\n\n4. Data Access and Files:\n   - Define reading/writing strategy for each data file in data/ directory\n   - Include field order and delimiter (pipe '|')\n   - Ensure consistent usage of filenames as per user requirements\n\nCRITICAL SUCCESS CRITERIA:\n- design_spec.md must be complete and precise for backend and frontend implementation\n- All element IDs and field names must match exactly user input and requirements_analysis.md\n- Navigation must be clearly defined with route and function names consistent throughout\n- Use write_text_file tool to save design_spec.md\n- Do not include any implementation code, only detailed specifications\n\nOutput: design_spec.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"requirements_analysis.md\", \"source\": \"RequirementsAnalyst\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"RequirementsAnalyst\",\n            \"reviewer_agent\": \"WebArchitect\",\n            \"review_criteria\": (\n                \"Verify requirements_analysis.md completely and accurately captures every required page, UI elements by ID, data files, their formats, and \"\n                \"the user interaction flows as described by the user.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\"},\n                {\"type\": \"text_file\", \"name\": \"requirements_analysis.md\"}\n            ]\n        }\n    ]\n): pass",
    "phase2": "def implementation_phase(\n    goal: str = \"Implement the PetAdoptionCenter Flask Web application as app.py and templates/*.html accurately reflecting design_spec.md\",\n    collab_pattern_name: str = \"Sequential Flow\",\n    collab_pattern_description: str = (\n        \"DraftEngineer writes app_draft.py and templates_draft/*.html from design_spec.md covering all 10 pages, exact routes, UI IDs, \"\n        \"buttons, and local file I/O; IntegrationEngineer then refines drafts into final app.py and templates/*.html fixing paths and final integration.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"DraftEngineer\",\n            \"prompt\": \"\"\"You are a Backend and Frontend Developer specializing in Flask web application development with local file I/O.\n\nYour goal is to create a complete Flask draft application (app_draft.py) and draft HTML templates (templates_draft/*.html) that fully implement the PetAdoptionCenter features based on the design specification.\n\nTask Details:\n- Read user_task_description and design_spec.md thoroughly to understand all page routes, UI element IDs, and data file schemas under data/\n- Implement app_draft.py with all Flask routes and view functions covering all 10 pages in the spec\n- Read from and write to local text files in data/ using pipe-delimited parsing exactly as specified\n- Implement all templates_draft/*.html with exact UI element IDs, Jinja2 templating, and proper render_template usage\n- Reference any required CSS/JS in templates; focus on UI correctness and data integration\n\nImplementation Requirements:\n1. **app_draft.py Structure**:\n   - Use Flask with standard imports and app initialization\n   - Implement routes for each page with correct URL paths and HTTP methods\n   - For data management: open, read, parse pipe-delimited files line-by-line; implement writing with proper data append or overwrite\n   - Ensure all business logic for browsing pets, applications, favorites, messages, profiles, and admin actions is included\n   - Use exact context variable names and structures matching design_spec.md\n   - Implement form handling for POST requests such as submitting applications, adding pets\n\n2. **Templates_draft/*.html**:\n   - Use Jinja2 syntax for loops, conditionals, and variable interpolation matching context variables passed from Flask routes\n   - Include all specified UI element IDs EXACTLY as listed, with correct casing\n   - Maintain page titles exactly as specified in the design spec\n   - Implement navigation buttons using url_for with correct route names\n   - Include forms for input pages with matching input element IDs and form methods\n\n3. **File and Path Usage**:\n   - Store all data files under 'data/' directory\n   - Read and write data files matching data schemas provided in design spec exactly (field order and format)\n   - Use relative file paths in file I/O code, consistent across all routes\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save 'app_draft.py' and all 'templates_draft/*.html' files\n- All Flask routes and template renders must strictly conform to design_spec.md\n- Element IDs in templates must exactly match provided design spec (case-sensitive)\n- Do not add any features or routes beyond those specified\n- Ensure local text file I/O uses pipe-delimited format and exact field order\n- Provide complete implementations; partial code snippets only in files via write_text_file output\n\nOutput: app_draft.py, templates_draft/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"WebArchitect\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_draft.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_draft/*.html\"}\n            ]\n        },\n        {\n            \"agent_name\": \"IntegrationEngineer\",\n            \"prompt\": \"\"\"You are a Software Integration Engineer specializing in Flask web applications and template integration.\n\nYour goal is to produce the final integrated Flask application (app.py) and HTML templates (templates/*.html) by refining and merging drafts to ensure correct runtime behavior.\n\nTask Details:\n- Read user_task_description, design_spec.md, app_draft.py, and templates_draft/*.html fully\n- Fix all runtime path issues so that app.py runs correctly with Flask using correct 'template_folder' and static file references\n- Ensure all routes, functions, and UI element IDs from drafts are preserved exactly without removal or addition\n- Validate that data file access in app.py matches design_spec.md specifications and all local file paths are correct\n- Refine templates to reside in templates/ with correct file names and maintain exact UI IDs and correctness\n- Perform final cleanups to confirm app.py executes without errors and templates render as intended\n\nIntegration Requirements:\n1. **app.py Adjustments**:\n   - Set Flask app = Flask(__name__, template_folder='templates') if needed\n   - Correct any relative paths in file I/O to match deployment environment\n   - Ensure imports, app.run block, and all route decorators are intact and operational\n\n2. **Templates/*.html**:\n   - Move and/or rename templates from templates_draft to templates/\n   - Fix any broken references to CSS/JS or static files\n   - Verify navigation buttons, forms, and UI element IDs exactly match design_spec.md and are consistent with app.py context variables\n\n3. **Testing**:\n   - Confirm app.py runs locally and routes navigate correctly\n   - Confirm templates render with correct data and UI elements populate as expected\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save 'app.py' and all 'templates/*.html' files\n- Maintain exact requested routes, UI element IDs, and local data file access as per design_spec.md\n- Do not alter or remove features or core logic from drafts; only fix integration and path issues\n- Ensure final deliverables are fully operational Flask app with working templates\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"WebArchitect\"},\n                {\"type\": \"text_file\", \"name\": \"app_draft.py\", \"source\": \"DraftEngineer\"},\n                {\"type\": \"text_file\", \"name\": \"templates_draft/*.html\", \"source\": \"DraftEngineer\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"DraftEngineer\",\n            \"reviewer_agent\": \"IntegrationEngineer\",\n            \"review_criteria\": (\n                \"Review app_draft.py and templates_draft/*.html against design_spec.md for correctness, completeness, and adherence to UI IDs and data storage before producing final files.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"},\n                {\"type\": \"text_file\", \"name\": \"app_draft.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_draft/*.html\"}\n            ]\n        }\n    ]\n): pass",
    "phase3": "def verification_phase(\n    goal: str = \"Validate the Flask app.py and templates/*.html for syntax, runtime behavior and correct implementation of all user requirements before final release\",\n    collab_pattern_name: str = \"Sequential Flow\",\n    collab_pattern_description: str = (\n        \"WebValidator runs syntax and runtime validation on app.py and templates/*.html verifying coverage of all design specification features \"\n        \"and writes validation_report.md; SequentialFixer reviews validation_report.md and applies all corrections to deliver the final application.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"WebValidator\",\n            \"prompt\": \"\"\"You are a Web Validator specializing in Flask applications and frontend template verification.\n\nYour goal is to validate the Flask app.py and all HTML templates for syntax correctness, runtime behavior, and adherence to all design specifications and user requirements.\n\nTask Details:\n- Read user_task_description, design_spec.md, app.py, and templates/*.html thoroughly\n- Validate Flask app.py for syntax and runtime errors using Python validation tools\n- Verify templates for presence of all required UI elements by ID and correct button actions\n- Check all Flask routes for coverage and correctness according to design_spec.md\n- Confirm correct data file I/O operations and consistency with specified schemas\n- Produce a comprehensive validation_report.md listing all found issues with clear details for fixes\n\nValidation Checklist:\n1. Syntax and Runtime Errors:\n   - Use validate_python_file on app.py for syntax and runtime checking\n   - Use execute_python_code to run key app functionalities safely\n2. Template Verification:\n   - Confirm presence of all elements by their exact IDs listed in design_spec.md\n   - Validate button actions, navigation links, and forms conform to design_spec.md\n3. Route Coverage:\n   - Verify that all routes defined in design_spec.md are implemented and functioning\n4. Data Storage:\n   - Check reading and writing to local data files matching specified field orders and formats\n\nCRITICAL REQUIREMENTS:\n- Use validate_python_file and execute_python_code tools for code validation\n- Use write_text_file tool to save validation_report.md\n- Provide precise, actionable feedback for each issue found\n- Do NOT modify any files; only produce the report\n- Maintain strict adherence to design specifications and user requirements\n\nOutput: validation_report.md\"\"\",\n            \"tools\": [\"validate_python_file\", \"execute_python_code\", \"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"WebArchitect\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"IntegrationEngineer\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"IntegrationEngineer\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_report.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"SequentialFixer\",\n            \"prompt\": \"\"\"You are a Software Developer specializing in Flask applications and frontend HTML template corrections.\n\nYour goal is to apply corrections from the validation_report.md to app.py and all templates/*.html to ensure full compliance with design specifications and user requirements.\n\nTask Details:\n- Read user_task_description, design_spec.md, app.py, templates/*.html, and validation_report.md carefully\n- Apply all fixes indicated in validation_report.md precisely to the source files\n- Ensure all pages, UI elements by ID, user interactions, and data file operations fully conform to design_spec.md and user requirements\n- Maintain consistent code quality, structure, and naming conventions as per design_spec.md\n\nCorrection Guidelines:\n1. Source Integrity:\n   - Update only app.py and templates/*.html files as needed based on report\n   - Preserve existing working features not marked for correction\n2. UI Elements:\n   - Add or fix missing or incorrect element IDs\n   - Correct button actions, navigation flows, forms, and data bindings\n3. Backend Logic:\n   - Fix syntax, runtime, and logical errors in app.py as identified\n   - Correct data file parsing and writing to match schema specifications\n4. Consistency:\n   - Ensure consistent naming conventions across code and templates\n   - Confirm all required routes and functionalities are implemented\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save corrected app.py and templates/*.html files\n- Implement only changes from validation_report.md; do NOT add new features\n- Ensure final outputs fully satisfy design_spec.md and user requirements\n- Provide clean, runnable, and maintainable code and templates\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"WebArchitect\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"IntegrationEngineer\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"IntegrationEngineer\"},\n                {\"type\": \"text_file\", \"name\": \"validation_report.md\", \"source\": \"WebValidator\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"WebValidator\",\n            \"reviewer_agent\": \"SequentialFixer\",\n            \"review_criteria\": (\n                \"Confirm validation_report.md precisely identifies all syntax, runtime, functional, and UI-related issues for targeted correction.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"},\n                {\"type\": \"text_file\", \"name\": \"validation_report.md\"}\n            ]\n        },\n        {\n            \"source_agent\": \"SequentialFixer\",\n            \"reviewer_agent\": \"RequirementsAnalyst\",\n            \"review_criteria\": (\n                \"Verify that the final app.py and templates/*.html fully implement all specified user requirements and resolve all validation issues.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_report.md\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ]\n): pass",
}

user_task = """
# Requirements Document for 'PetAdoptionCenter' Web Application

## 1. Objective
Develop a comprehensive web application named 'PetAdoptionCenter' using Python, with data managed through local text files. The application enables users to browse available pets for adoption, submit adoption applications, manage favorites, and communicate with shelters. Note that the website should start from the Dashboard page.

## 2. Language
The required development language for the 'PetAdoptionCenter' application is Python.

## 3. Page Design

The 'PetAdoptionCenter' web application will consist of the following ten pages:

### 1. Dashboard Page
- **Page Title**: Pet Adoption Dashboard
- **Overview**: The main hub displaying featured pets, recent activities, and navigation to other functionalities.
- **Elements**:
  - **ID: dashboard-page** - Type: Div - Container for the dashboard page.
  - **ID: featured-pets** - Type: Div - Display of featured pets available for adoption (limit 5).
  - **ID: browse-pets-button** - Type: Button - Button to navigate to pet listings page.
  - **ID: back-to-dashboard** - Type: Button - Button to refresh dashboard.

### 2. Pet Listings Page
- **Page Title**: Available Pets
- **Overview**: A page displaying all available pets with filtering and search options.
- **Elements**:
  - **ID: pet-listings-page** - Type: Div - Container for the pet listings page.
  - **ID: search-input** - Type: Input - Field to search pets by name.
  - **ID: filter-species** - Type: Dropdown - Dropdown to filter by species (All, Dog, Cat, Bird, Rabbit, Other).
  - **ID: pet-grid** - Type: Div - Grid displaying pet cards with photo, name, species, and age.
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 3. Pet Details Page
- **Page Title**: Pet Details
- **Overview**: A page displaying detailed information about a specific pet.
- **Elements**:
  - **ID: pet-details-page** - Type: Div - Container for the pet details page.
  - **ID: pet-name** - Type: H1 - Display pet name.
  - **ID: pet-species** - Type: Div - Display pet species.
  - **ID: pet-description** - Type: Div - Display detailed description about the pet.
  - **ID: adopt-button** - Type: Button - Button to start adoption application process.
  - **ID: back-to-listings** - Type: Button - Button to navigate back to pet listings.

### 4. Add Pet Page
- **Page Title**: Add New Pet
- **Overview**: A page for shelter administrators to add new pets for adoption.
- **Elements**:
  - **ID: add-pet-page** - Type: Div - Container for the add pet page.
  - **ID: pet-name-input** - Type: Input - Field to input pet name.
  - **ID: pet-species-input** - Type: Dropdown - Dropdown to select species (Dog, Cat, Bird, Rabbit, Other).
  - **ID: pet-breed-input** - Type: Input - Field to input breed.
  - **ID: pet-age-input** - Type: Input - Field to input age (e.g., "2 years").
  - **ID: pet-gender-input** - Type: Dropdown - Dropdown to select gender (Male, Female).
  - **ID: pet-size-input** - Type: Dropdown - Dropdown to select size (Small, Medium, Large).
  - **ID: pet-description-input** - Type: Textarea - Field to input detailed description.
  - **ID: submit-pet-button** - Type: Button - Button to submit new pet listing.
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 5. Adoption Application Page
- **Page Title**: Adoption Application
- **Overview**: A page for users to submit adoption applications.
- **Elements**:
  - **ID: application-page** - Type: Div - Container for the application page.
  - **ID: applicant-name** - Type: Input - Field to input applicant's full name.
  - **ID: applicant-phone** - Type: Input - Field to input phone number.
  - **ID: housing-type** - Type: Dropdown - Dropdown to select housing type (House, Apartment, Condo, Other).
  - **ID: reason** - Type: Textarea - Field to explain why they want to adopt this pet.
  - **ID: submit-application-button** - Type: Button - Button to submit application.
  - **ID: back-to-pet** - Type: Button - Button to navigate back to pet details.

### 6. My Applications Page
- **Page Title**: My Applications
- **Overview**: A page displaying all adoption applications submitted by the user.
- **Elements**:
  - **ID: my-applications-page** - Type: Div - Container for the my applications page.
  - **ID: filter-status** - Type: Dropdown - Dropdown to filter by status (All, Pending, Approved, Rejected).
  - **ID: applications-table** - Type: Table - Table displaying applications with pet name, date, status, and actions.
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 7. Favorites Page
- **Page Title**: My Favorites
- **Overview**: A page displaying all pets the user has saved as favorites.
- **Elements**:
  - **ID: favorites-page** - Type: Div - Container for the favorites page.
  - **ID: favorites-grid** - Type: Div - Grid displaying favorite pet cards.
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 8. Messages Page
- **Page Title**: Messages
- **Overview**: A page for users to view and send messages to shelters.
- **Elements**:
  - **ID: messages-page** - Type: Div - Container for the messages page.
  - **ID: conversation-list** - Type: Div - List of message conversations.
  - **ID: message-input** - Type: Textarea - Field to compose new message.
  - **ID: send-message-button** - Type: Button - Button to send message.
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 9. User Profile Page
- **Page Title**: My Profile
- **Overview**: A page for users to view and edit their profile information.
- **Elements**:
  - **ID: profile-page** - Type: Div - Container for the profile page.
  - **ID: profile-username** - Type: Div - Display username (not editable).
  - **ID: profile-email** - Type: Input - Field to update email.
  - **ID: update-profile-button** - Type: Button - Button to save profile changes.
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 10. Admin Panel Page
- **Page Title**: Admin Panel
- **Overview**: A page for administrators to manage applications and pets.
- **Elements**:
  - **ID: admin-panel-page** - Type: Div - Container for the admin panel page.
  - **ID: pending-applications** - Type: Div - List of pending adoption applications.
  - **ID: all-pets-list** - Type: Div - List of all pets with edit/delete options.
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

## 4. Data Storage

The 'PetAdoptionCenter' application will store data locally in text files organized in the directory 'data'. The following data formats and examples are defined:

### 1. User Data
- **File Name**: `users.txt`
- **Data Format**:
  ```
  username|email|phone|address
  ```
- **Example Data**:
  ```
  john_doe|john@example.com|555-1234|123 Main St, City
  admin_user|admin@shelter.com|555-0000|456 Shelter Ave
  jane_smith|jane@example.com|555-5678|789 Oak Rd, Town
  ```

### 2. Pet Data
- **File Name**: `pets.txt`
- **Data Format**:
  ```
  pet_id|name|species|breed|age|gender|size|description|shelter_id|status|date_added
  ```
- **Example Data**:
  ```
  1|Buddy|Dog|Golden Retriever|3 years|Male|Large|Friendly and energetic dog who loves to play fetch.|1|Available|2024-10-15
  2|Whiskers|Cat|Siamese|2 years|Female|Small|Calm and affectionate cat, great with children.|1|Pending|2024-10-20
  3|Charlie|Dog|Beagle|5 years|Male|Medium|Gentle senior dog looking for a quiet home.|2|Available|2024-11-01
  ```

### 3. Adoption Applications Data
- **File Name**: `applications.txt`
- **Data Format**:
  ```
  application_id|username|pet_id|applicant_name|phone|address|housing_type|has_yard|other_pets|experience|reason|status|date_submitted
  ```
- **Example Data**:
  ```
  1|john_doe|1|John Doe|555-1234|123 Main St|House|Yes|One cat|5 years with dogs|Looking for a companion for hiking|Pending|2024-11-10
  2|jane_smith|2|Jane Smith|555-5678|789 Oak Rd|Apartment|No|None|First time pet owner|Always wanted a cat|Approved|2024-11-05
  ```

### 4. Favorites Data
- **File Name**: `favorites.txt`
- **Data Format**:
  ```
  username|pet_id|date_added
  ```
- **Example Data**:
  ```
  john_doe|1|2024-11-01
  john_doe|3|2024-11-05
  jane_smith|2|2024-10-25
  ```

### 5. Messages Data
- **File Name**: `messages.txt`
- **Data Format**:
  ```
  message_id|sender_username|recipient_username|subject|content|timestamp|is_read
  ```
- **Example Data**:
  ```
  1|john_doe|admin_user|Question about Buddy|Is Buddy good with other dogs?|2024-11-10 14:30:00|true
  2|admin_user|john_doe|Re: Question about Buddy|Yes, Buddy is great with other dogs!|2024-11-10 15:00:00|false
  ```

### 6. Adoption History Data
- **File Name**: `adoption_history.txt`
- **Data Format**:
  ```
  history_id|username|pet_id|pet_name|adoption_date|shelter_id
  ```
- **Example Data**:
  ```
  1|jane_smith|2|Whiskers|2024-11-15|1
  ```

### 7. Shelters Data
- **File Name**: `shelters.txt`
- **Data Format**:
  ```
  shelter_id|name|address|phone|email
  ```
- **Example Data**:
  ```
  1|Happy Paws Shelter|100 Shelter Lane, City|555-1000|contact@happypaws.com
  2|Second Chance Animals|200 Rescue Road, Town|555-2000|info@secondchance.org
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
            """You are a Business Analyst specializing in extracting detailed requirements from user task descriptions for web applications.

Your goal is to produce a comprehensive requirements_analysis.md document that fully captures all user requirements, UI element specifications, page titles, data file formats, and user interaction flows from the user task description.

Task Details:
- Read the user_task_description artifact carefully
- Extract every page with its exact name, title, and UI elements including element IDs and types
- Document all data file formats with exact field order and example data
- Describe user navigation flows and button actions linking pages

Specification Requirements:
1. Page Specifications:
   - List each page with exact page title and all element IDs & types as provided
   - Include descriptions of element purposes where available
2. Data Files:
   - List each data file with filename, field order as pipe-delimited format, and example data rows
3. User Flows:
   - Describe navigation buttons and how users move between pages
   - Highlight starting page as Dashboard

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save the artifact requirements_analysis.md
- Keep all details exact as per user description without assumptions
- Structure the document clearly for easy transformation by next agent

Output: requirements_analysis.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'requirements_analysis.md'}],

    },

    "WebArchitect": {
        "prompt": (
            """You are a Web Architect specializing in Flask web applications and UI contract design.

Your goal is to convert requirements_analysis.md into a detailed design_spec.md that defines the complete Flask route architecture, page-to-template mappings, exact UI element IDs and types per page, navigation logic starting from the Dashboard, local data storage schemas in the data/ directory, and interaction contracts for all user flows and UI buttons.

Task Details:
- Read user_task_description and requirements_analysis.md artifacts
- Create design_spec.md specifying:
  * Flask route table with routes, function names, HTTP methods, templates, context variables
  * Mapping of pages to HTML templates with exact element IDs and their types
  * Navigation rules for buttons and links (starting at Dashboard)
  * Data storage file schemas matching provided formats and field order under data/
  * Interaction contracts documenting actions triggered by UI elements

Design Spec Requirements:
1. Flask Route Architecture:
   - Define route paths with example: '/', '/pets', '/pet/<int:pet_id>'
   - Specify function names (lowercase underscore style)
   - HTTP methods: GET for views, POST for form submissions (e.g., adding pet, submitting applications)
   - Associate each route with its template file and passed context variables with types

2. Page and Template Mapping:
   - Assign each page to a template file: templates/{page_name}.html
   - List all UI element IDs and types exactly
   - Define context variables provided to templates and their structure (list/dict/str/int, etc.)

3. Navigation Logic:
   - Specify button/link actions using url_for function names
   - Mark Dashboard as the initial landing page ('/')

4. Data Access and Files:
   - Define reading/writing strategy for each data file in data/ directory
   - Include field order and delimiter (pipe '|')
   - Ensure consistent usage of filenames as per user requirements

CRITICAL SUCCESS CRITERIA:
- design_spec.md must be complete and precise for backend and frontend implementation
- All element IDs and field names must match exactly user input and requirements_analysis.md
- Navigation must be clearly defined with route and function names consistent throughout
- Use write_text_file tool to save design_spec.md
- Do not include any implementation code, only detailed specifications

Output: design_spec.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'requirements_analysis.md', 'source': 'RequirementsAnalyst'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_spec.md'}],

    },

    "DraftEngineer": {
        "prompt": (
            """You are a Backend and Frontend Developer specializing in Flask web application development with local file I/O.

Your goal is to create a complete Flask draft application (app_draft.py) and draft HTML templates (templates_draft/*.html) that fully implement the PetAdoptionCenter features based on the design specification.

Task Details:
- Read user_task_description and design_spec.md thoroughly to understand all page routes, UI element IDs, and data file schemas under data/
- Implement app_draft.py with all Flask routes and view functions covering all 10 pages in the spec
- Read from and write to local text files in data/ using pipe-delimited parsing exactly as specified
- Implement all templates_draft/*.html with exact UI element IDs, Jinja2 templating, and proper render_template usage
- Reference any required CSS/JS in templates; focus on UI correctness and data integration

Implementation Requirements:
1. **app_draft.py Structure**:
   - Use Flask with standard imports and app initialization
   - Implement routes for each page with correct URL paths and HTTP methods
   - For data management: open, read, parse pipe-delimited files line-by-line; implement writing with proper data append or overwrite
   - Ensure all business logic for browsing pets, applications, favorites, messages, profiles, and admin actions is included
   - Use exact context variable names and structures matching design_spec.md
   - Implement form handling for POST requests such as submitting applications, adding pets

2. **Templates_draft/*.html**:
   - Use Jinja2 syntax for loops, conditionals, and variable interpolation matching context variables passed from Flask routes
   - Include all specified UI element IDs EXACTLY as listed, with correct casing
   - Maintain page titles exactly as specified in the design spec
   - Implement navigation buttons using url_for with correct route names
   - Include forms for input pages with matching input element IDs and form methods

3. **File and Path Usage**:
   - Store all data files under 'data/' directory
   - Read and write data files matching data schemas provided in design spec exactly (field order and format)
   - Use relative file paths in file I/O code, consistent across all routes

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save 'app_draft.py' and all 'templates_draft/*.html' files
- All Flask routes and template renders must strictly conform to design_spec.md
- Element IDs in templates must exactly match provided design spec (case-sensitive)
- Do not add any features or routes beyond those specified
- Ensure local text file I/O uses pipe-delimited format and exact field order
- Provide complete implementations; partial code snippets only in files via write_text_file output

Output: app_draft.py, templates_draft/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'WebArchitect'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app_draft.py'}, {'type': 'text_file', 'name': 'templates_draft/*.html'}],

    },

    "IntegrationEngineer": {
        "prompt": (
            """You are a Software Integration Engineer specializing in Flask web applications and template integration.

Your goal is to produce the final integrated Flask application (app.py) and HTML templates (templates/*.html) by refining and merging drafts to ensure correct runtime behavior.

Task Details:
- Read user_task_description, design_spec.md, app_draft.py, and templates_draft/*.html fully
- Fix all runtime path issues so that app.py runs correctly with Flask using correct 'template_folder' and static file references
- Ensure all routes, functions, and UI element IDs from drafts are preserved exactly without removal or addition
- Validate that data file access in app.py matches design_spec.md specifications and all local file paths are correct
- Refine templates to reside in templates/ with correct file names and maintain exact UI IDs and correctness
- Perform final cleanups to confirm app.py executes without errors and templates render as intended

Integration Requirements:
1. **app.py Adjustments**:
   - Set Flask app = Flask(__name__, template_folder='templates') if needed
   - Correct any relative paths in file I/O to match deployment environment
   - Ensure imports, app.run block, and all route decorators are intact and operational

2. **Templates/*.html**:
   - Move and/or rename templates from templates_draft to templates/
   - Fix any broken references to CSS/JS or static files
   - Verify navigation buttons, forms, and UI element IDs exactly match design_spec.md and are consistent with app.py context variables

3. **Testing**:
   - Confirm app.py runs locally and routes navigate correctly
   - Confirm templates render with correct data and UI elements populate as expected

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save 'app.py' and all 'templates/*.html' files
- Maintain exact requested routes, UI element IDs, and local data file access as per design_spec.md
- Do not alter or remove features or core logic from drafts; only fix integration and path issues
- Ensure final deliverables are fully operational Flask app with working templates

Output: app.py, templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'WebArchitect'}, {'type': 'text_file', 'name': 'app_draft.py', 'source': 'DraftEngineer'}, {'type': 'text_file', 'name': 'templates_draft/*.html', 'source': 'DraftEngineer'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}],

    },

    "WebValidator": {
        "prompt": (
            """You are a Web Validator specializing in Flask applications and frontend template verification.

Your goal is to validate the Flask app.py and all HTML templates for syntax correctness, runtime behavior, and adherence to all design specifications and user requirements.

Task Details:
- Read user_task_description, design_spec.md, app.py, and templates/*.html thoroughly
- Validate Flask app.py for syntax and runtime errors using Python validation tools
- Verify templates for presence of all required UI elements by ID and correct button actions
- Check all Flask routes for coverage and correctness according to design_spec.md
- Confirm correct data file I/O operations and consistency with specified schemas
- Produce a comprehensive validation_report.md listing all found issues with clear details for fixes

Validation Checklist:
1. Syntax and Runtime Errors:
   - Use validate_python_file on app.py for syntax and runtime checking
   - Use execute_python_code to run key app functionalities safely
2. Template Verification:
   - Confirm presence of all elements by their exact IDs listed in design_spec.md
   - Validate button actions, navigation links, and forms conform to design_spec.md
3. Route Coverage:
   - Verify that all routes defined in design_spec.md are implemented and functioning
4. Data Storage:
   - Check reading and writing to local data files matching specified field orders and formats

CRITICAL REQUIREMENTS:
- Use validate_python_file and execute_python_code tools for code validation
- Use write_text_file tool to save validation_report.md
- Provide precise, actionable feedback for each issue found
- Do NOT modify any files; only produce the report
- Maintain strict adherence to design specifications and user requirements

Output: validation_report.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['validate_python_file', 'execute_python_code', 'write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'WebArchitect'}, {'type': 'text_file', 'name': 'app.py', 'source': 'IntegrationEngineer'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'IntegrationEngineer'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'validation_report.md'}],

    },

    "SequentialFixer": {
        "prompt": (
            """You are a Software Developer specializing in Flask applications and frontend HTML template corrections.

Your goal is to apply corrections from the validation_report.md to app.py and all templates/*.html to ensure full compliance with design specifications and user requirements.

Task Details:
- Read user_task_description, design_spec.md, app.py, templates/*.html, and validation_report.md carefully
- Apply all fixes indicated in validation_report.md precisely to the source files
- Ensure all pages, UI elements by ID, user interactions, and data file operations fully conform to design_spec.md and user requirements
- Maintain consistent code quality, structure, and naming conventions as per design_spec.md

Correction Guidelines:
1. Source Integrity:
   - Update only app.py and templates/*.html files as needed based on report
   - Preserve existing working features not marked for correction
2. UI Elements:
   - Add or fix missing or incorrect element IDs
   - Correct button actions, navigation flows, forms, and data bindings
3. Backend Logic:
   - Fix syntax, runtime, and logical errors in app.py as identified
   - Correct data file parsing and writing to match schema specifications
4. Consistency:
   - Ensure consistent naming conventions across code and templates
   - Confirm all required routes and functionalities are implemented

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save corrected app.py and templates/*.html files
- Implement only changes from validation_report.md; do NOT add new features
- Ensure final outputs fully satisfy design_spec.md and user requirements
- Provide clean, runnable, and maintainable code and templates

Output: app.py, templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'WebArchitect'}, {'type': 'text_file', 'name': 'app.py', 'source': 'IntegrationEngineer'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'IntegrationEngineer'}, {'type': 'text_file', 'name': 'validation_report.md', 'source': 'WebValidator'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}],

    }

}

REVIEW_PROFILES = {
    'RequirementsAnalyst': [
        ("WebArchitect", """Verify requirements_analysis.md completely and accurately captures every required page, UI elements by ID, data files, their formats, and "
                "the user interaction flows as described by the user.""", [{'type': 'user', 'name': 'user_task_description'}, {'type': 'text_file', 'name': 'requirements_analysis.md'}])
    ],

    'DraftEngineer': [
        ("IntegrationEngineer", """Review app_draft.py and templates_draft/*.html against design_spec.md for correctness, completeness, and adherence to UI IDs and data storage before producing final files.""", [{'type': 'text_file', 'name': 'design_spec.md'}, {'type': 'text_file', 'name': 'app_draft.py'}, {'type': 'text_file', 'name': 'templates_draft/*.html'}])
    ],

    'WebValidator': [
        ("SequentialFixer", """Confirm validation_report.md precisely identifies all syntax, runtime, functional, and UI-related issues for targeted correction.""", [{'type': 'text_file', 'name': 'design_spec.md'}, {'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}, {'type': 'text_file', 'name': 'validation_report.md'}])
    ],

    'SequentialFixer': [
        ("RequirementsAnalyst", """Verify that the final app.py and templates/*.html fully implement all specified user requirements and resolve all validation issues.""", [{'type': 'text_file', 'name': 'validation_report.md'}, {'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}])
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
    RequirementsAnalyst = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="RequirementsAnalyst",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=2,
        timeout_threshold=300,
        failure_threshold=1,
        recovery_time=40
    )
    WebArchitect = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="WebArchitect",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=3,
        timeout_threshold=350,
        failure_threshold=1,
        recovery_time=40
    )

    # Sequential execution: RequirementsAnalyst first, then WebArchitect
    await execute(RequirementsAnalyst,
                  "Analyze user_task_description and produce requirements_analysis.md "
                  "capturing all pages, UI elements (IDs and types), data file formats, and user flows.")

    # Read generated requirements_analysis.md content for WebArchitect input injection
    requirements_analysis_content = ""
    try:
        requirements_analysis_content = open("requirements_analysis.md").read()
    except:
        pass

    await execute(WebArchitect,
                  f"Read user_task_description and the following requirements_analysis.md:\n{requirements_analysis_content}\n"
                  "Create design_spec.md with detailed Flask routes, page-template mappings, UI elements, navigation, and data schemas.")
# Phase1_End

# Phase2_Start

async def implementation_phase():
    # Create agents
    DraftEngineer = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="DraftEngineer",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=3,
        timeout_threshold=400,
        failure_threshold=1,
        recovery_time=40
    )
    IntegrationEngineer = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="IntegrationEngineer",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=3,
        timeout_threshold=450,
        failure_threshold=1,
        recovery_time=45
    )

    # Sequential execution: DraftEngineer then IntegrationEngineer

    # Step 1: DraftEngineer creates app_draft.py and templates_draft/*.html from design_spec.md
    await execute(DraftEngineer,
                  "Implement complete app_draft.py with all Flask routes and local file I/O, and all templates_draft/*.html "
                  "with exact UI element IDs and Jinja2 templating based on design_spec.md and user_task_description")

    # Reading draft outputs for IntegrationEngineer input injection
    app_draft_content, templates_draft_content = "", ""
    try:
        app_draft_content = open("app_draft.py").read()
    except Exception:
        pass
    try:
        # For templates_draft/*.html, concatenate all files contents or leave empty if none
        import glob
        drafts = glob.glob("templates_draft/*.html")
        templates_draft_content = ""
        for file_path in drafts:
            try:
                with open(file_path, "r") as f:
                    templates_draft_content += f"=== {file_path} ===\n" + f.read() + "\n\n"
            except Exception:
                continue
    except Exception:
        pass

    # Step 2: IntegrationEngineer refines draft app and templates into final app.py and templates/*.html
    await execute(
        IntegrationEngineer,
        f"Read user_task_description, design_spec.md, app_draft.py, and templates_draft/*.html fully. "
        f"Fix all runtime path issues, set correct template folders, refine app_draft.py and templates_draft into final app.py and templates/*.html. "
        f"Maintain exact UI element IDs, routes, and data file access.\n\n"
        f"=== app_draft.py ===\n{app_draft_content}\n\n"
        f"=== templates_draft ===\n{templates_draft_content}"
    )
# Phase2_End

# Phase3_Start

async def verification_phase():
    # Create agents
    WebValidator = build_resilient_agent(
        chaos_controller=chaos_controller,
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
        chaos_controller=chaos_controller,
        agent_name="SequentialFixer",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase3"],
        max_retries=3,
        timeout_threshold=450,
        failure_threshold=2,
        recovery_time=60
    )

    # Sequential Flow: WebValidator then SequentialFixer
    await execute(
        WebValidator,
        "Validate app.py and all templates/*.html for syntax correctness, runtime behavior, full coverage of design specifications and user requirements. "
        "Write detailed validation_report.md listing all issues with precise fix instructions."
    )

    # Read the validation report content for injection
    validation_report_content = ""
    try:
        validation_report_content = open("validation_report.md").read()
    except Exception:
        validation_report_content = ""

    await execute(
        SequentialFixer,
        f"Apply all corrections needed based on the following validation_report.md content. "
        f"Fix app.py and templates/*.html exactly accordingly while preserving existing correct functionality.\n\n"
        f"=== validation_report.md ===\n{validation_report_content}"
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
