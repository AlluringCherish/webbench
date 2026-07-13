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
# 20260714_001750_094508/main_20260714_001750_094508.py

# Phase_info dictionary containing complete def blocks for failover context
Phase_info = {
    "phase1": "def design_specification_phase(\n    goal: str = \"Design comprehensive backend routes and frontend HTML templates reflecting all pages and specified element IDs; produce merged design specification document.\",\n    collab_pattern_name: str = \"Parallel + Merger\",\n    collab_pattern_description: str = (\n        \"BackendDesignArchitect defines the Flask routes, data handling flows, and input/output data schemas for all specified pages and data files;\"\n        \"FrontendDesignArchitect specifies HTML templates, with correct element IDs, page layouts, and navigation for all application pages;\"\n        \"DesignMerger reviews and merges backend_design.md and frontend_design.md into a single, consistent design_spec.md ensuring coherence and compliance to the user requirements.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"BackendDesignArchitect\",\n            \"prompt\": \"\"\"You are a System Architect specializing in backend Flask web application design and local text file data management.\n\nYour goal is to design the backend architecture addressing all user requirements by defining Flask routes, data handling, and input/output data schemas for all specified application pages and local text files independently.\n\nTask Details:\n- Read user_task_description from CONTEXT\n- Produce backend_design.md without referencing frontend_design.md\n- Define all Flask routes with required parameters and HTTP methods\n- Specify detailed data read/write schemas matching local text files for users, pets, applications, favorites, messages, adoption history, and shelters\n- Outline backend logic flows for all ten application pages including data interactions and route handlers\n\n**Section 1: Flask Routes Specification**\n- Enumerate route paths, allowed HTTP methods, and route parameters\n- Define route purposes linked to each application page and data operation\n- Include routes for listing, detail, creation, updating, and navigation actions\n\n**Section 2: Data Interaction and Schema Definition**\n- Specify file-based data formats, field order, delimiters, and example entries referencing all required data files in the 'data' directory\n- Detail data reading and writing operations per route\n- Confirm local text-file management including concurrency assumptions and error handling\n\n**Section 3: Backend Logic and Workflow**\n- Describe backend logic per route: input processing, validation, data updates, state changes, and response generation\n- Define session or user state considerations if applicable\n\nCRITICAL SUCCESS CRITERIA:\n- backend_design.md must fully enable implementation of backend app.py\n- Routes and data schemas must cover all user task requirements independently\n- Use write_text_file tool exclusively for outputting backend_design.md\n- Do not rely on or read sibling frontend_design.md artifact\n\nOutput: backend_design.md\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"backend_design.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"FrontendDesignArchitect\",\n            \"prompt\": \"\"\"You are a System Architect specializing in frontend HTML template design with detailed element ID and navigation planning.\n\nYour goal is to create comprehensive HTML templates layout, specifying exact element IDs, page structure, navigation flows, and data-binding placeholders for all pages independently.\n\nTask Details:\n- Read user_task_description from CONTEXT\n- Produce frontend_design.md independently without reading backend_design.md\n- Define precise HTML template names and page titles for all ten specified pages\n- Specify all required element IDs matching the user task elements described for each page\n- Include navigation flows between pages via buttons and links identified by element IDs\n- Outline placeholders for dynamic data binding and UI behavior from backend context\n\n**Section 1: HTML Template Structure and IDs**\n- For each page, list template filename, page title, and container elements with their exact IDs and element types\n- Include buttons, inputs, dropdowns, textareas, tables, and grids with specified IDs\n\n**Section 2: Navigation and Interaction Flow**\n- Map all navigation triggers (buttons, links) to target pages using element IDs\n- Detail form submission buttons and UI controls referencing backend interaction points\n\n**Section 3: Data Binding Placeholders**\n- Specify dynamic context variables or placeholders to be rendered per template element\n- Ensure consistency with backend data models without assuming backend_design.md\n\nCRITICAL SUCCESS CRITERIA:\n- frontend_design.md fully supports implementation of all templates in templates/*.html\n- All required IDs, page titles, and navigation described in user task must be included\n- Use write_text_file tool exclusively for outputting frontend_design.md\n- Do not reference or depend on backend_design.md\n\nOutput: frontend_design.md\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"frontend_design.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"DesignMerger\",\n            \"prompt\": \"\"\"You are a System Architect specializing in merging backend and frontend web application designs into a coherent specification document.\n\nYour goal is to consolidate backend_design.md and frontend_design.md into one consistent and complete design_spec.md, ensuring coverage of all functionalities, UI elements, and data flows as per user requirements without adding or omitting any features.\n\nTask Details:\n- Read user_task_description, backend_design.md, and frontend_design.md from CONTEXT\n- Analyze and reconcile route definitions with UI templates and navigation flows\n- Check consistency of route parameters with frontend data-binding placeholders and element usage\n- Merge backend route, data schema, and logic descriptions with frontend template and navigation specifications\n- Resolve conflicting or divergent details with strict adherence to user task inputs only\n- Assemble a final design_spec.md document organized with Sections for Backend Routes, Data Schemas, Frontend Templates, and Navigation\n\n**Section 1: Comprehensive Backend Routes and Data Schemas**\n- Present reconciled, coherent route list from backend_design.md\n- Include full data file schemas and examples integrated with backend logic\n\n**Section 2: Detailed Frontend Template Specifications**\n- Present finalized template filenames, page titles, element IDs, and UI components from frontend_design.md\n\n**Section 3: Cross-Artifact Consistency Checks and Navigation Mappings**\n- Ensure navigation flows and UI interactions are consistent with backend routes\n- Confirm matching field names and parameters between backend and frontend\n\nCRITICAL SUCCESS CRITERIA:\n- design_spec.md supports seamless backend and frontend implementation\n- No new requirements beyond input artifacts are introduced\n- Use write_text_file tool exclusively for outputting design_spec.md\n\nOutput: design_spec.md\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"backend_design.md\", \"source\": \"BackendDesignArchitect\"},\n                {\"type\": \"text_file\", \"name\": \"frontend_design.md\", \"source\": \"FrontendDesignArchitect\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"BackendDesignArchitect\",\n            \"reviewer_agent\": \"DesignMerger\",\n            \"review_criteria\": \"Verify backend design covers all routes, data storage schema, and specifications as per user requirements.\",\n            \"review_artifacts\": [{\"type\": \"text_file\", \"name\": \"backend_design.md\"}]\n        },\n        {\n            \"source_agent\": \"FrontendDesignArchitect\",\n            \"reviewer_agent\": \"DesignMerger\",\n            \"review_criteria\": \"Verify frontend design matches element IDs, page layouts, and navigation requirements.\",\n            \"review_artifacts\": [{\"type\": \"text_file\", \"name\": \"frontend_design.md\"}]\n        }\n    ]\n): pass",
    "phase2": "def implementation_and_verification_phase(\n    goal: str = \"Implement backend Flask app.py and frontend HTML templates in parallel from design_spec.md, then merge and integrate them into a consistent working web application.\",\n    collab_pattern_name: str = \"Parallel + Merger\",\n    collab_pattern_description: str = (\n        \"BackendDeveloper implements the Flask app.py file with routes, logic, and data file management strictly following design_spec.md;\"\n        \"FrontendDeveloper creates all required HTML templates with correct element IDs and structures as specified in design_spec.md;\"\n        \"IntegrationMerger reconciles the backend and frontend components, resolves interface mismatches, and produces integrated app.py and templates/*.html ensuring functional consistency.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"BackendDeveloper\",\n            \"prompt\": \"\"\"You are a Backend Developer specializing in Flask web applications using Python.\n\nYour goal is to implement the complete backend Flask application (app.py) including all routes, data file interactions, form handling, and business logic strictly according to the design specifications.\n\nTask Details:\n- Read design_spec.md artifact from CONTEXT for route, data structure, and application logic specifications.\n- Produce app.py implementing all Flask routes, handlers, and local text file data management as specified.\n- Focus only on backend functionality: routing, data reading/writing, application logic, and form processing.\n- Do NOT read or depend on frontend artifacts from siblings.\n\n**Implementation Requirements:**\n- Implement all routes as specified with proper HTTP methods (GET/POST).\n- Handle local data files under the 'data' directory for users, pets, applications, favorites, messages, etc.\n- Implement all form inputs, validation, submission logic, and status updates.\n- Use Flask features for route decorators, request parsing, session or context as needed.\n- Maintain modular code organization within app.py using functions or classes.\n- Follow the data formats and examples provided in design_spec.md strictly.\n- Include code comments using single-quote docstrings for clarity.\n- Ensure exception handling around file access and user inputs.\n\nCRITICAL SUCCESS CRITERIA:\n- app.py must be fully functional and runnable as a Flask application.\n- The implementation strictly follows design_spec.md routes and data schemas.\n- Use write_text_file tool to output app.py only.\n- Do not produce any files other than app.py.\n\nOutput: app.py\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [{\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"}],\n            \"output_artifacts\": [{\"type\": \"text_file\", \"name\": \"app.py\"}]\n        },\n        {\n            \"agent_name\": \"FrontendDeveloper\",\n            \"prompt\": \"\"\"You are a Frontend Developer specializing in HTML and Jinja2 templating for Flask applications.\n\nYour goal is to create all HTML templates with correct element IDs, page layouts, and navigation patterns as defined in design_spec.md.\n\nTask Details:\n- Read design_spec.md artifact from CONTEXT for templates structure, page titles, element IDs, and navigation flows.\n- Produce all required HTML template files under templates/ directory (*.html) implementing layouts for all pages.\n- Focus only on frontend artifacts: HTML structure, element IDs, navigation buttons, and integration placeholders.\n- Do NOT read or depend on backend code artifacts from siblings.\n\n**Template Specification Requirements:**\n- Create one HTML file per page: Dashboard, Pet Listings, Pet Details, Add Pet, Adoption Application, My Applications, Favorites, Messages, User Profile, Admin Panel.\n- Use element IDs exactly as specified, including buttons, inputs, divs, and other UI elements.\n- Structure pages for a consistent user experience with correct titles and navigation elements.\n- Use Jinja2 templating syntax for dynamic content placeholders but no actual data logic.\n- Include comments using single-quote docstrings formatting where appropriate.\n- Ensure navigation buttons link to correct routes based on design_spec.md.\n\nCRITICAL SUCCESS CRITERIA:\n- templates/*.html are complete and fully compliant with design_spec.md.\n- Files are independent of backend implementation details.\n- Use write_text_file tool to output templates/*.html only.\n- Do not produce any files other than templates/*.html.\n\nOutput: templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [{\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"}],\n            \"output_artifacts\": [{\"type\": \"text_file\", \"name\": \"templates/*.html\"}]\n        },\n        {\n            \"agent_name\": \"IntegrationMerger\",\n            \"prompt\": \"\"\"You are a Software Integration Specialist with expertise in combining Flask backend and HTML frontend components into a coherent web application.\n\nYour goal is to merge and integrate the app.py backend implementation and all HTML templates to ensure consistent interfaces, resolve mismatches, and produce a fully functional PetAdoptionCenter web application.\n\nTask Details:\n- Read design_spec.md, app.py, and templates/*.html artifacts from CONTEXT.\n- Perform reconciliation to resolve remaining interface mismatches between backend routes and frontend navigation.\n- Correct minor inconsistencies in route URLs, form action endpoints, element IDs, or variable references.\n- Ensure outputs conform strictly to design_spec.md specifications.\n- Produce final version of app.py and templates/*.html for deployment.\n\n**Integration and Consistency Checks:**\n- Verify all app.py routes are referenced correctly by HTML form actions and navigation links.\n- Confirm all element IDs in templates are consistent with backend route handlers and context variables.\n- Validate that all forms submit to correct backend endpoints.\n- Ensure navigation flows allow returning to Dashboard or other pages as described.\n- Keep code style consistent and add comments using single-quote docstrings.\n\nCRITICAL SUCCESS CRITERIA:\n- Final app.py and templates/*.html are fully consistent and deployable together.\n- No feature is added or removed beyond design_spec.md scope.\n- Use write_text_file tool to save final app.py and all templates/*.html.\n- Write ONLY the specified output artifacts.\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"BackendDeveloper\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"FrontendDeveloper\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"BackendDeveloper\",\n            \"reviewer_agent\": \"IntegrationMerger\",\n            \"review_criteria\": \"Check app.py conforms precisely to design_spec.md routes, data access, and requirements.\",\n            \"review_artifacts\": [{\"type\": \"text_file\", \"name\": \"app.py\"}]\n        },\n        {\n            \"source_agent\": \"FrontendDeveloper\",\n            \"reviewer_agent\": \"IntegrationMerger\",\n            \"review_criteria\": \"Check HTML templates conform completely to design_spec.md element IDs, structure, and navigation.\",\n            \"review_artifacts\": [{\"type\": \"text_file\", \"name\": \"templates/*.html\"}]\n        }\n    ]\n): pass",
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
    "BackendDesignArchitect": {
        "prompt": (
            """You are a System Architect specializing in backend Flask web application design and local text file data management.

Your goal is to design the backend architecture addressing all user requirements by defining Flask routes, data handling, and input/output data schemas for all specified application pages and local text files independently.

Task Details:
- Read user_task_description from CONTEXT
- Produce backend_design.md without referencing frontend_design.md
- Define all Flask routes with required parameters and HTTP methods
- Specify detailed data read/write schemas matching local text files for users, pets, applications, favorites, messages, adoption history, and shelters
- Outline backend logic flows for all ten application pages including data interactions and route handlers

**Section 1: Flask Routes Specification**
- Enumerate route paths, allowed HTTP methods, and route parameters
- Define route purposes linked to each application page and data operation
- Include routes for listing, detail, creation, updating, and navigation actions

**Section 2: Data Interaction and Schema Definition**
- Specify file-based data formats, field order, delimiters, and example entries referencing all required data files in the 'data' directory
- Detail data reading and writing operations per route
- Confirm local text-file management including concurrency assumptions and error handling

**Section 3: Backend Logic and Workflow**
- Describe backend logic per route: input processing, validation, data updates, state changes, and response generation
- Define session or user state considerations if applicable

CRITICAL SUCCESS CRITERIA:
- backend_design.md must fully enable implementation of backend app.py
- Routes and data schemas must cover all user task requirements independently
- Use write_text_file tool exclusively for outputting backend_design.md
- Do not rely on or read sibling frontend_design.md artifact

Output: backend_design.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'backend_design.md'}],

    },

    "FrontendDesignArchitect": {
        "prompt": (
            """You are a System Architect specializing in frontend HTML template design with detailed element ID and navigation planning.

Your goal is to create comprehensive HTML templates layout, specifying exact element IDs, page structure, navigation flows, and data-binding placeholders for all pages independently.

Task Details:
- Read user_task_description from CONTEXT
- Produce frontend_design.md independently without reading backend_design.md
- Define precise HTML template names and page titles for all ten specified pages
- Specify all required element IDs matching the user task elements described for each page
- Include navigation flows between pages via buttons and links identified by element IDs
- Outline placeholders for dynamic data binding and UI behavior from backend context

**Section 1: HTML Template Structure and IDs**
- For each page, list template filename, page title, and container elements with their exact IDs and element types
- Include buttons, inputs, dropdowns, textareas, tables, and grids with specified IDs

**Section 2: Navigation and Interaction Flow**
- Map all navigation triggers (buttons, links) to target pages using element IDs
- Detail form submission buttons and UI controls referencing backend interaction points

**Section 3: Data Binding Placeholders**
- Specify dynamic context variables or placeholders to be rendered per template element
- Ensure consistency with backend data models without assuming backend_design.md

CRITICAL SUCCESS CRITERIA:
- frontend_design.md fully supports implementation of all templates in templates/*.html
- All required IDs, page titles, and navigation described in user task must be included
- Use write_text_file tool exclusively for outputting frontend_design.md
- Do not reference or depend on backend_design.md

Output: frontend_design.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'frontend_design.md'}],

    },

    "DesignMerger": {
        "prompt": (
            """You are a System Architect specializing in merging backend and frontend web application designs into a coherent specification document.

Your goal is to consolidate backend_design.md and frontend_design.md into one consistent and complete design_spec.md, ensuring coverage of all functionalities, UI elements, and data flows as per user requirements without adding or omitting any features.

Task Details:
- Read user_task_description, backend_design.md, and frontend_design.md from CONTEXT
- Analyze and reconcile route definitions with UI templates and navigation flows
- Check consistency of route parameters with frontend data-binding placeholders and element usage
- Merge backend route, data schema, and logic descriptions with frontend template and navigation specifications
- Resolve conflicting or divergent details with strict adherence to user task inputs only
- Assemble a final design_spec.md document organized with Sections for Backend Routes, Data Schemas, Frontend Templates, and Navigation

**Section 1: Comprehensive Backend Routes and Data Schemas**
- Present reconciled, coherent route list from backend_design.md
- Include full data file schemas and examples integrated with backend logic

**Section 2: Detailed Frontend Template Specifications**
- Present finalized template filenames, page titles, element IDs, and UI components from frontend_design.md

**Section 3: Cross-Artifact Consistency Checks and Navigation Mappings**
- Ensure navigation flows and UI interactions are consistent with backend routes
- Confirm matching field names and parameters between backend and frontend

CRITICAL SUCCESS CRITERIA:
- design_spec.md supports seamless backend and frontend implementation
- No new requirements beyond input artifacts are introduced
- Use write_text_file tool exclusively for outputting design_spec.md

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

Your goal is to implement the complete backend Flask application (app.py) including all routes, data file interactions, form handling, and business logic strictly according to the design specifications.

Task Details:
- Read design_spec.md artifact from CONTEXT for route, data structure, and application logic specifications.
- Produce app.py implementing all Flask routes, handlers, and local text file data management as specified.
- Focus only on backend functionality: routing, data reading/writing, application logic, and form processing.
- Do NOT read or depend on frontend artifacts from siblings.

**Implementation Requirements:**
- Implement all routes as specified with proper HTTP methods (GET/POST).
- Handle local data files under the 'data' directory for users, pets, applications, favorites, messages, etc.
- Implement all form inputs, validation, submission logic, and status updates.
- Use Flask features for route decorators, request parsing, session or context as needed.
- Maintain modular code organization within app.py using functions or classes.
- Follow the data formats and examples provided in design_spec.md strictly.
- Include code comments using single-quote docstrings for clarity.
- Ensure exception handling around file access and user inputs.

CRITICAL SUCCESS CRITERIA:
- app.py must be fully functional and runnable as a Flask application.
- The implementation strictly follows design_spec.md routes and data schemas.
- Use write_text_file tool to output app.py only.
- Do not produce any files other than app.py.

Output: app.py"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}],

    },

    "FrontendDeveloper": {
        "prompt": (
            """You are a Frontend Developer specializing in HTML and Jinja2 templating for Flask applications.

Your goal is to create all HTML templates with correct element IDs, page layouts, and navigation patterns as defined in design_spec.md.

Task Details:
- Read design_spec.md artifact from CONTEXT for templates structure, page titles, element IDs, and navigation flows.
- Produce all required HTML template files under templates/ directory (*.html) implementing layouts for all pages.
- Focus only on frontend artifacts: HTML structure, element IDs, navigation buttons, and integration placeholders.
- Do NOT read or depend on backend code artifacts from siblings.

**Template Specification Requirements:**
- Create one HTML file per page: Dashboard, Pet Listings, Pet Details, Add Pet, Adoption Application, My Applications, Favorites, Messages, User Profile, Admin Panel.
- Use element IDs exactly as specified, including buttons, inputs, divs, and other UI elements.
- Structure pages for a consistent user experience with correct titles and navigation elements.
- Use Jinja2 templating syntax for dynamic content placeholders but no actual data logic.
- Include comments using single-quote docstrings formatting where appropriate.
- Ensure navigation buttons link to correct routes based on design_spec.md.

CRITICAL SUCCESS CRITERIA:
- templates/*.html are complete and fully compliant with design_spec.md.
- Files are independent of backend implementation details.
- Use write_text_file tool to output templates/*.html only.
- Do not produce any files other than templates/*.html.

Output: templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'templates/*.html'}],

    },

    "IntegrationMerger": {
        "prompt": (
            """You are a Software Integration Specialist with expertise in combining Flask backend and HTML frontend components into a coherent web application.

Your goal is to merge and integrate the app.py backend implementation and all HTML templates to ensure consistent interfaces, resolve mismatches, and produce a fully functional PetAdoptionCenter web application.

Task Details:
- Read design_spec.md, app.py, and templates/*.html artifacts from CONTEXT.
- Perform reconciliation to resolve remaining interface mismatches between backend routes and frontend navigation.
- Correct minor inconsistencies in route URLs, form action endpoints, element IDs, or variable references.
- Ensure outputs conform strictly to design_spec.md specifications.
- Produce final version of app.py and templates/*.html for deployment.

**Integration and Consistency Checks:**
- Verify all app.py routes are referenced correctly by HTML form actions and navigation links.
- Confirm all element IDs in templates are consistent with backend route handlers and context variables.
- Validate that all forms submit to correct backend endpoints.
- Ensure navigation flows allow returning to Dashboard or other pages as described.
- Keep code style consistent and add comments using single-quote docstrings.

CRITICAL SUCCESS CRITERIA:
- Final app.py and templates/*.html are fully consistent and deployable together.
- No feature is added or removed beyond design_spec.md scope.
- Use write_text_file tool to save final app.py and all templates/*.html.
- Write ONLY the specified output artifacts.

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
        ("DesignMerger", """Verify backend design covers all routes, data storage schema, and specifications as per user requirements.""", [{'type': 'text_file', 'name': 'backend_design.md'}])
    ],

    'FrontendDesignArchitect': [
        ("DesignMerger", """Verify frontend design matches element IDs, page layouts, and navigation requirements.""", [{'type': 'text_file', 'name': 'frontend_design.md'}])
    ],

    'BackendDeveloper': [
        ("IntegrationMerger", """Check app.py conforms precisely to design_spec.md routes, data access, and requirements.""", [{'type': 'text_file', 'name': 'app.py'}])
    ],

    'FrontendDeveloper': [
        ("IntegrationMerger", """Check HTML templates conform completely to design_spec.md element IDs, structure, and navigation.""", [{'type': 'text_file', 'name': 'templates/*.html'}])
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
        failure_threshold=2,
        recovery_time=60
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
        failure_threshold=2,
        recovery_time=60
    )
    DesignMerger = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="DesignMerger",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=3,
        timeout_threshold=450,
        failure_threshold=2,
        recovery_time=60
    )

    # Parallel execution of backend and frontend design architects
    await asyncio.gather(
        execute(
            BackendDesignArchitect,
            "Design backend architecture and produce backend_design.md based on user_task_description. "
            "Define Flask routes, data schemas, and backend logic for all pages."
        ),
        execute(
            FrontendDesignArchitect,
            "Design frontend templates and produce frontend_design.md based on user_task_description. "
            "Specify exact element IDs, page titles, navigation flows, and data placeholders for all pages."
        ),
    )

    # Read backend_design.md and frontend_design.md outputs for merger
    backend_design_content = ""
    frontend_design_content = ""
    try:
        backend_design_content = open("backend_design.md").read()
    except FileNotFoundError:
        pass
    try:
        frontend_design_content = open("frontend_design.md").read()
    except FileNotFoundError:
        pass

    # Run DesignMerger to produce final design_spec.md
    await execute(
        DesignMerger,
        f"Merge backend_design.md and frontend_design.md into a consistent design_spec.md with coverage of all user requirements.\n\n"
        f"=== Backend Design ===\n{backend_design_content}\n\n"
        f"=== Frontend Design ===\n{frontend_design_content}"
    )
# Phase1_End

# Phase2_Start
import asyncio
import glob

async def implementation_and_verification_phase():
    BackendDeveloper = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="BackendDeveloper",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=3,
        timeout_threshold=400,
        failure_threshold=2,
        recovery_time=60
    )
    FrontendDeveloper = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="FrontendDeveloper",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=3,
        timeout_threshold=400,
        failure_threshold=2,
        recovery_time=60
    )
    IntegrationMerger = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="IntegrationMerger",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=3,
        timeout_threshold=450,
        failure_threshold=2,
        recovery_time=60
    )

    # Parallel execution of BackendDeveloper and FrontendDeveloper
    await asyncio.gather(
        execute(BackendDeveloper,
                "Implement complete backend Flask app.py strictly from design_spec.md including all routes, data handling, forms."),
        execute(FrontendDeveloper,
                "Create all HTML templates in templates/*.html strictly from design_spec.md including correct element IDs and navigation.")
    )

    # Read the backend output app.py
    backend_code = ""
    try:
        with open("app.py", "r", encoding="utf-8") as f:
            backend_code = f.read()
    except FileNotFoundError:
        backend_code = ""

    # Read all frontend templates together content
    templates_content = ""
    for path in sorted(glob.glob("templates/*.html")):
        try:
            with open(path, "r", encoding="utf-8") as f:
                templates_content += f"\n=== {path} ===\n" + f.read()
        except OSError:
            continue

    # IntegrationMerger merges and reconciles
    await execute(
        IntegrationMerger,
        f"Integrate and reconcile backend app.py and frontend templates with design_spec.md.\n"
        f"=== design_spec.md ===\n{CONTEXT.get('design_spec.md', '')}\n\n"
        f"=== app.py ===\n{backend_code}\n\n"
        f"=== templates/*.html ===\n{templates_content}"
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
