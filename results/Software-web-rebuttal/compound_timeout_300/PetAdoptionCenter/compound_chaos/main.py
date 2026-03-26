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
    "phase1": "def design_specification_phase(\n    goal: str = \"Create comprehensive design specification enabling independent backend/frontend development for PetAdoptionCenter with explicit page, data, and functional specifications\",\n    collab_pattern_name: str = \"Sequential Flow\",\n    collab_pattern_description: str = (\n        \"SystemArchitect produces design_spec.md containing detailed Flask routes with function names, context variables, HTTP methods; \"\n        \"HTML templates with element IDs and navigation mappings; Data schemas for all data files with exact field orders and pipe-delimited formats.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"SystemArchitect\",\n            \"prompt\": \"\"\"You are a System Architect specializing in Flask web application design specifications.\n\nYour goal is to create comprehensive design specifications that enable Backend and Frontend developers to work completely independently without needing to see each other's code or implementation details.\n\nTask Details:\n- Read user_task_description from CONTEXT\n- Create design_spec.md with three main sections: Flask routes, HTML templates, and data schemas\n- Include all details necessary for independent parallel development of backend and frontend components\n\n**Section 1: Flask Routes Specification (Backend Focus)**\n- Provide a complete list of routes with:\n  - Route path (e.g., /dashboard, /pets/<int:pet_id>)\n  - Function name (lowercase with underscores)\n  - HTTP method (GET, POST as appropriate)\n  - Template file rendered\n  - Context variables passed to templates with exact names and types\n- The root route '/' must redirect to the dashboard page\n- Include mechanisms for form submissions where applicable, with POST method usage\n- Context variables must be precisely typed (str, int, list, dict, etc.)\n\n**Section 2: HTML Template Specifications (Frontend Focus)**\n- For each page template, specify:\n  - File path in templates/ directory (e.g., templates/dashboard.html)\n  - Exact page title for <title> and <h1> tags\n  - Complete list of element IDs with exact casing and element types (div, button, input, etc.)\n  - Navigation mappings for all buttons and links using Flask url_for functions, with dynamic IDs described using Jinja2 syntax\n  - Context variables available in the template and their structures\n- Ensure all element IDs from the requirement document are included exactly as specified, supporting dynamic patterns as needed\n\n**Section 3: Data File Schemas (Backend Focus)**\n- For each data file in the data/ directory:\n  - Specify filename and exact pipe-delimited field order\n  - Provide field descriptions for clarity\n  - Include realistic example data rows matching the defined format\n- Ensure data schema precision for consistent parsing by backend code\n\nCRITICAL SUCCESS CRITERIA:\n- Backend can implement all Flask routes and data handling solely from Sections 1 and 3\n- Frontend can implement all HTML templates solely from Section 2\n- No assumptions or cross-reading of backend/frontend code allowed\n- All context variables and element IDs must match exactly across specifications\n- Use write_text_file tool to save design_spec.md\n- Provide the full specification in a single Markdown file\n\nOutput: design_spec.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"SystemArchitect\",\n            \"reviewer_agent\": \"BackendDeveloper\",\n            \"review_criteria\": (\n                \"Verify design_spec.md Section 1 for backend completeness: all Flask routes with function names, methods, and context variables; \"\n                \"all data schemas with exact field order and pipe-delimited format accurately described.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        },\n        {\n            \"source_agent\": \"SystemArchitect\",\n            \"reviewer_agent\": \"FrontendDeveloper\",\n            \"review_criteria\": (\n                \"Verify design_spec.md Section 2 for frontend completeness: all HTML templates with correct element IDs, context variables, navigation mappings using url_for functions;\"\n                \"page titles are correctly specified.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ]\n): pass",
    "phase2": "def parallel_implementation_phase(\n    goal: str = \"Implement backend and frontend in parallel based on the design specification for PetAdoptionCenter\",\n    collab_pattern_name: str = \"Parallel Flow\",\n    collab_pattern_description: str = (\n        \"BackendDeveloper implements app.py including all Flask routes, data handling using specified text file schemas, and business logic. \"\n        \"FrontendDeveloper implements all HTML templates with specified element IDs, context variables, and navigation links independently.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"BackendDeveloper\",\n            \"prompt\": \"\"\"You are a Backend Developer specializing in Flask web applications.\n\nYour goal is to implement the complete Flask backend including routes, data handling, and business logic based on the design specification.\n\nTask Details:\n- Read design_spec.md Section 1 (Flask Routes) and data schema from the CONTEXT\n- Implement app.py with all Flask routes exactly as specified\n- Handle data loading and saving from data/*.txt files using the given pipe-delimited schemas with exact field order\n- Do NOT read or modify frontend templates or their code\n- Do NOT assume data formats beyond provided schemas; parse and handle with strict adherence\n\nImplementation Requirements:\n1. **Flask App Initialization**:\n   ```python\n   from flask import Flask, render_template, redirect, url_for, request\n   app = Flask(__name__)\n   app.config['SECRET_KEY'] = 'dev-secret-key'\n   ```\n\n2. **Root Route**:\n   - Implement '/' route that redirects to the dashboard page\n   - Use: return redirect(url_for('dashboard'))\n\n3. **Data Handling**:\n   - Load data from text files in 'data' folder, e.g., data/pets.txt, data/users.txt\n   - Parse lines using pipe '|' delimiter: line.strip().split('|')\n   - Map parsed values to fields exactly as defined in data schema\n   - Handle file reading/writing with error checking and data integrity\n   - No header lines; parsing starts from first line\n\n4. **Route Logic**:\n   - Implement all routes as listed in design_spec.md Section 1\n   - Use exact function names and route paths from the specification\n   - Pass context variables to templates exactly as specified\n   - Handle POST requests for forms including adding pets, submitting applications, updating profiles\n   - Implement business logic related to adoption, favorites, messaging as per design\n\n5. **Additional Requirements**:\n   - Use url_for for all redirects and links within backend\n   - Gracefully handle missing or empty data sets\n   - Follow code best practices for Flask applications\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save app.py\n- Ensure all function names, routes, and context variables match design_spec.md Section 1 exactly\n- Follow exact field order and names when reading/writing data files\n- Do NOT add features outside the design specification\n- Do NOT output code snippets only; save full code to app.py using write_text_file\n\nOutput: app.py\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"SystemArchitect\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"}\n            ]\n        },\n        {\n            \"agent_name\": \"FrontendDeveloper\",\n            \"prompt\": \"\"\"You are a Frontend Developer specializing in HTML and Jinja2 templating for Flask applications.\n\nYour goal is to implement all HTML templates for the PetAdoptionCenter web app with exact element IDs, structure, and navigation links based on the design specification.\n\nTask Details:\n- Read design_spec.md Section 2 (HTML Templates) ONLY from CONTEXT\n- Implement all specified HTML templates (*.html) with exact IDs and structure\n- Use specified context variables for dynamic content rendering\n- Do NOT read backend source code or data schemas\n- Maintain navigation links using url_for function calls exactly as specified\n\nImplementation Requirements:\n1. **Template Structure**:\n   ```html\n   <!DOCTYPE html>\n   <html lang=\"en\">\n   <head>\n       <meta charset=\"UTF-8\">\n       <title>{{ page_title }}</title>\n   </head>\n   <body>\n       <div id=\"main-container-id\">\n           <h1>{{ page_title }}</h1>\n           <!-- Content here -->\n       </div>\n   </body>\n   </html>\n   ```\n\n2. **Naming and Storage**:\n   - Save templates inside templates/ directory\n   - Use exact filenames as specified in Section 2 (e.g., dashboard.html, pet_listings.html)\n\n3. **Element IDs**:\n   - Include all required element IDs exactly as specified including dynamic IDs using Jinja2 syntax\n   - Respect case sensitivity and naming patterns\n\n4. **Context Variables**:\n   - Use correct Jinja2 syntax to loop over lists and render variables: {{ variable }}, {% for ... %}, {% if ... %}\n   - Render all data-driven content according to specification\n\n5. **Navigation and Forms**:\n   - Implement navigation buttons and links with url_for referencing correct backend route functions\n   - Implement form elements with proper method and action attributes based on design\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save all individual HTML template files\n- All IDs must match exactly as defined in the specification\n- Navigation function names and URLs must correspond exactly to backend routes\n- Do NOT add templates or elements not specified in the design_spec.md\n- Do NOT output code snippets only; save full templates files using write_text_file\n\nOutput: templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"SystemArchitect\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"BackendDeveloper\",\n            \"reviewer_agent\": \"SystemArchitect\",\n            \"review_criteria\": (\n                \"Verify app.py implements all routes from design_spec.md Section 1 accurately, including data handling using the specified schemas; \"\n                \"Ensure that the root route redirects to the dashboard page.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\"}\n            ]\n        },\n        {\n            \"source_agent\": \"FrontendDeveloper\",\n            \"reviewer_agent\": \"SystemArchitect\",\n            \"review_criteria\": (\n                \"Verify all HTML templates conform to design_spec.md Section 2 requirements: correct element IDs, context variable usage, navigation via url_for, and accurate page titles.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ]\n): pass",
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
    "SystemArchitect": {
        "prompt": (
            """You are a System Architect specializing in Flask web application design specifications.

Your goal is to create comprehensive design specifications that enable Backend and Frontend developers to work completely independently without needing to see each other's code or implementation details.

Task Details:
- Read user_task_description from CONTEXT
- Create design_spec.md with three main sections: Flask routes, HTML templates, and data schemas
- Include all details necessary for independent parallel development of backend and frontend components

**Section 1: Flask Routes Specification (Backend Focus)**
- Provide a complete list of routes with:
  - Route path (e.g., /dashboard, /pets/<int:pet_id>)
  - Function name (lowercase with underscores)
  - HTTP method (GET, POST as appropriate)
  - Template file rendered
  - Context variables passed to templates with exact names and types
- The root route '/' must redirect to the dashboard page
- Include mechanisms for form submissions where applicable, with POST method usage
- Context variables must be precisely typed (str, int, list, dict, etc.)

**Section 2: HTML Template Specifications (Frontend Focus)**
- For each page template, specify:
  - File path in templates/ directory (e.g., templates/dashboard.html)
  - Exact page title for <title> and <h1> tags
  - Complete list of element IDs with exact casing and element types (div, button, input, etc.)
  - Navigation mappings for all buttons and links using Flask url_for functions, with dynamic IDs described using Jinja2 syntax
  - Context variables available in the template and their structures
- Ensure all element IDs from the requirement document are included exactly as specified, supporting dynamic patterns as needed

**Section 3: Data File Schemas (Backend Focus)**
- For each data file in the data/ directory:
  - Specify filename and exact pipe-delimited field order
  - Provide field descriptions for clarity
  - Include realistic example data rows matching the defined format
- Ensure data schema precision for consistent parsing by backend code

CRITICAL SUCCESS CRITERIA:
- Backend can implement all Flask routes and data handling solely from Sections 1 and 3
- Frontend can implement all HTML templates solely from Section 2
- No assumptions or cross-reading of backend/frontend code allowed
- All context variables and element IDs must match exactly across specifications
- Use write_text_file tool to save design_spec.md
- Provide the full specification in a single Markdown file

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

Your goal is to implement the complete Flask backend including routes, data handling, and business logic based on the design specification.

Task Details:
- Read design_spec.md Section 1 (Flask Routes) and data schema from the CONTEXT
- Implement app.py with all Flask routes exactly as specified
- Handle data loading and saving from data/*.txt files using the given pipe-delimited schemas with exact field order
- Do NOT read or modify frontend templates or their code
- Do NOT assume data formats beyond provided schemas; parse and handle with strict adherence

Implementation Requirements:
1. **Flask App Initialization**:
   ```python
   from flask import Flask, render_template, redirect, url_for, request
   app = Flask(__name__)
   app.config['SECRET_KEY'] = 'dev-secret-key'
   ```

2. **Root Route**:
   - Implement '/' route that redirects to the dashboard page
   - Use: return redirect(url_for('dashboard'))

3. **Data Handling**:
   - Load data from text files in 'data' folder, e.g., data/pets.txt, data/users.txt
   - Parse lines using pipe '|' delimiter: line.strip().split('|')
   - Map parsed values to fields exactly as defined in data schema
   - Handle file reading/writing with error checking and data integrity
   - No header lines; parsing starts from first line

4. **Route Logic**:
   - Implement all routes as listed in design_spec.md Section 1
   - Use exact function names and route paths from the specification
   - Pass context variables to templates exactly as specified
   - Handle POST requests for forms including adding pets, submitting applications, updating profiles
   - Implement business logic related to adoption, favorites, messaging as per design

5. **Additional Requirements**:
   - Use url_for for all redirects and links within backend
   - Gracefully handle missing or empty data sets
   - Follow code best practices for Flask applications

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save app.py
- Ensure all function names, routes, and context variables match design_spec.md Section 1 exactly
- Follow exact field order and names when reading/writing data files
- Do NOT add features outside the design specification
- Do NOT output code snippets only; save full code to app.py using write_text_file

Output: app.py"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'SystemArchitect'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}],
    },

    "FrontendDeveloper": {
        "prompt": (
            """You are a Frontend Developer specializing in HTML and Jinja2 templating for Flask applications.

Your goal is to implement all HTML templates for the PetAdoptionCenter web app with exact element IDs, structure, and navigation links based on the design specification.

Task Details:
- Read design_spec.md Section 2 (HTML Templates) ONLY from CONTEXT
- Implement all specified HTML templates (*.html) with exact IDs and structure
- Use specified context variables for dynamic content rendering
- Do NOT read backend source code or data schemas
- Maintain navigation links using url_for function calls exactly as specified

Implementation Requirements:
1. **Template Structure**:
   ```html
   <!DOCTYPE html>
   <html lang="en">
   <head>
       <meta charset="UTF-8">
       <title>{{ page_title }}</title>
   </head>
   <body>
       <div id="main-container-id">
           <h1>{{ page_title }}</h1>
           <!-- Content here -->
       </div>
   </body>
   </html>
   ```

2. **Naming and Storage**:
   - Save templates inside templates/ directory
   - Use exact filenames as specified in Section 2 (e.g., dashboard.html, pet_listings.html)

3. **Element IDs**:
   - Include all required element IDs exactly as specified including dynamic IDs using Jinja2 syntax
   - Respect case sensitivity and naming patterns

4. **Context Variables**:
   - Use correct Jinja2 syntax to loop over lists and render variables: {{ variable }}, {% for ... %}, {% if ... %}
   - Render all data-driven content according to specification

5. **Navigation and Forms**:
   - Implement navigation buttons and links with url_for referencing correct backend route functions
   - Implement form elements with proper method and action attributes based on design

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save all individual HTML template files
- All IDs must match exactly as defined in the specification
- Navigation function names and URLs must correspond exactly to backend routes
- Do NOT add templates or elements not specified in the design_spec.md
- Do NOT output code snippets only; save full templates files using write_text_file

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
        ("BackendDeveloper", """Verify design_spec.md Section 1 for backend completeness: all Flask routes with function names, methods, and context variables; "
                "all data schemas with exact field order and pipe-delimited format accurately described.""", [{'type': 'user', 'name': 'user_task_description'}, {'type': 'text_file', 'name': 'design_spec.md'}]),
        ("FrontendDeveloper", """Verify design_spec.md Section 2 for frontend completeness: all HTML templates with correct element IDs, context variables, navigation mappings using url_for functions;"
                "page titles are correctly specified.""", [{'type': 'user', 'name': 'user_task_description'}, {'type': 'text_file', 'name': 'design_spec.md'}])
    ],

    'BackendDeveloper': [
        ("SystemArchitect", """Verify app.py implements all routes from design_spec.md Section 1 accurately, including data handling using the specified schemas; "
                "Ensure that the root route redirects to the dashboard page.""", [{'type': 'text_file', 'name': 'design_spec.md'}, {'type': 'text_file', 'name': 'app.py'}])
    ],

    'FrontendDeveloper': [
        ("SystemArchitect", """Verify all HTML templates conform to design_spec.md Section 2 requirements: correct element IDs, context variable usage, navigation via url_for, and accurate page titles.""", [{'type': 'text_file', 'name': 'design_spec.md'}, {'type': 'text_file', 'name': 'templates/*.html'}])
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
        timeout_threshold=300,
        failure_threshold=1,
        recovery_time=30
    )

    # Execute SystemArchitect
    await execute(SystemArchitect, "Create comprehensive design_spec.md specifying Flask routes, HTML templates, and data schemas for PetAdoptionCenter")
# Phase1_End

# Phase2_Start
import asyncio

async def parallel_implementation_phase():
    # Create BackendDeveloper agent
    BackendDeveloper = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="BackendDeveloper",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=3,
        timeout_threshold=300,
        failure_threshold=1,
        recovery_time=30
    )
    # Create FrontendDeveloper agent
    FrontendDeveloper = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="FrontendDeveloper",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=3,
        timeout_threshold=300,
        failure_threshold=1,
        recovery_time=30
    )

    # Execute BackendDeveloper and FrontendDeveloper in parallel
    await asyncio.gather(
        execute(BackendDeveloper, "Implement complete Flask backend app.py based on design_spec.md Section 1"),
        execute(FrontendDeveloper, "Implement all HTML templates as per design_spec.md Section 2 in templates/")
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
