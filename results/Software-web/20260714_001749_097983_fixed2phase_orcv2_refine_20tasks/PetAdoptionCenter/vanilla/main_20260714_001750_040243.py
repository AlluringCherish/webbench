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
# 20260714_001750_040243/main_20260714_001750_040243.py

# Phase_info dictionary containing complete def blocks for failover context
Phase_info = {
    "phase1": "def design_specification_phase(\n    goal: str = \"Create a detailed adaptive web design contract defining all 10 web pages with exact element IDs, navigation flows, user roles, and local data file formats in design_spec.md and gate it with design_feedback.md.\",\n    collab_pattern_name: str = \"Refinement Loop\",\n    collab_pattern_description: str = \"DesignGenerator produces the design_spec.md text file from the user task description and any previous feedback; DesignCritic reviews the design_spec.md for completeness, correctness, and adherence to user specifications, producing design_feedback.md with approval or revision requests.\",\n    team: list = [\n        {\n            \"agent_name\": \"DesignGenerator\",\n            \"prompt\": \"\"\"You are a Software Architect specializing in adaptive web application design specifications using Python and local text file data management.\n\nYour goal is to draft or revise a comprehensive web design specification that covers all required pages, exact element IDs, navigation flows, user roles, and local data file formats, producing a complete design_spec.md.\n\nTask Details:\n- Read user_task_description from CONTEXT to extract requirements and data formats\n- Read existing design_spec.md and design_feedback.md if they exist, applying any NEED_MODIFY feedback\n- Produce or update the entire design_spec.md artifact reflecting all 10 pages, element IDs, navigation, workflows, and data file structure\n- Overwrite design_spec.md whenever feedback begins NEED_MODIFY; preserve if feedback is [APPROVED]\n- Focus solely on specified inputs and outputs; do not add unrequested features\n\n**Section 1: Page Structure and Element IDs**\n- Define each of the 10 pages with exact page titles and container element IDs\n- Specify all required element IDs per page with their types and roles exactly as described\n- Ensure the starting page is Dashboard with the correct ID\n\n**Section 2: Navigation and User Workflows**\n- Describe navigation buttons and flows between pages with element IDs used for navigation actions\n- Define user roles and relevant access/navigation differences if applicable\n\n**Section 3: Local Data File Formats**\n- Detail the data directory structure and text file names (e.g., users.txt, pets.txt, etc.)\n- Specify exact data formats with field order, delimiters, and sample example lines\n- Ensure data isolation per file type and consistent usage across the application\n\nCRITICAL SUCCESS CRITERIA:\n- Run at most two iterations with the critic feedback identifying corrections\n- Apply every supported NEED_MODIFY item fully and overwrite design_spec.md accordingly\n- Use the write_text_file tool to save the finalized design_spec.md\n- Maintain clean separation of concerns: pages, navigation, data formats\n- Do not include feedback status markers in design_spec.md\n\nOutput: design_spec.md\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"design_feedback.md\", \"source\": \"DesignCritic\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"DesignCritic\",\n            \"prompt\": \"\"\"You are a Design Quality Assurance Engineer specializing in reviewing adaptive web application design specifications for Python projects with local file data handling.\n\nYour goal is to review the design_spec.md against the full user_task_description and requirements, providing structured feedback in design_feedback.md starting explicitly with [APPROVED] or NEED_MODIFY, enabling gated refinement for at most two iterations.\n\nTask Details:\n- Read user_task_description and design_spec.md from CONTEXT\n- Review coverage of all 10 pages, exact element IDs, page titles, and container elements\n- Verify navigation flows between pages and correct usage of navigation element IDs\n- Confirm user roles and any access distinctions are properly described\n- Validate local data file structures, names, delimiters, field ordering, and example data lines\n- Ensure the Dashboard page is the starting page and uses the correct container ID\n- Write feedback that begins exactly with [APPROVED] if all criteria met or NEED_MODIFY with precise changes if issues found\n\nReview Criteria:\n1. Complete page specifications with exact element IDs matching user requirements\n2. Correct, unambiguous navigation flows and user workflow definitions\n3. Accurate data file formats and examples consistent with user_task_description\n4. No additions beyond user-defined requirements or unsupported features\n\nCRITICAL REQUIREMENTS:\n- design_feedback.md must start at byte-1 with [APPROVED] or NEED_MODIFY marker, no preceding whitespace or text\n- Use write_text_file tool to save the entire feedback artifact\n- At most two critique iterations; stop immediately on [APPROVED]\n\nOutput: design_feedback.md\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignGenerator\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_feedback.md\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"DesignGenerator\",\n            \"reviewer_agent\": \"DesignCritic\",\n            \"review_criteria\": \"Verify the design specification correctly covers all pages, elements, data files, navigation flows, user roles, and the start point dashboard with required element IDs exactly.\"\n            ,\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ]\n): pass",
    "phase2": "def implementation_and_verification_phase(\n    goal: str = \"Fully implement the PetAdoptionCenter Python web app with all pages, exact element IDs, local text file data storage, and navigation as per design_spec.md; produce app.py and templates/*.html, and gate implementation with code_feedback.md.\",\n    collab_pattern_name: str = \"Refinement Loop\",\n    collab_pattern_description: str = \"AppGenerator creates or revises the Python Flask app.py source code and the complete set of HTML templates in templates/*.html based on design_spec.md and code_feedback.md; CodeCritic reviews the app.py and templates for conformity, correctness, and functionality producing code_feedback.md with approval or revision requests.\",\n    team: list = [\n        {\n            \"agent_name\": \"AppGenerator\",\n            \"prompt\": \"\"\"You are a Python Flask full-stack developer specialized in building web applications with local text file-based data storage.\n\nYour goal is to fully implement or revise the entire Python Flask backend app.py and the complete frontend HTML templates (templates/*.html) to fulfill the design_spec.md specification, for at most two iterations of refinement.\n\nTask Details:\n- Read design_spec.md, the current app.py, templates/*.html, and code_feedback.md from CONTEXT.\n- On the first iteration, create complete app.py and all HTML templates implementing all 10 pages exactly as specified.\n- On later iterations, when code_feedback.md begins with NEED_MODIFY, revise the entire app.py and templates to address all feedback.\n- When feedback begins [APPROVED], preserve the approved implementation.\n- Focus on exact element IDs, correct Flask routes, page navigation starting from dashboard, and local text file data handling as specified.\n- Output complete app.py and all template files under templates/ directory.\n\n**Section 1: Flask Backend Implementation**\n- Implement all routes for the 10 pages with HTTP methods and route paths as per design_spec.md.\n- Handle reading, writing, and updating all required local text files in the 'data' directory exactly as specified.\n- Ensure data formats, parsing, and updates follow the specification.\n- Implement form data handling, filtering, and session state (e.g., favorites).\n- Use Python code comments with single-quote docstrings only, no triple-double quotes.\n\n**Section 2: Frontend Templates Implementation**\n- Develop complete HTML templates for each page inside templates/*.html directories.\n- Include all specified elements with exact IDs and types as described.\n- Ensure buttons and navigation links correctly route between pages.\n- Keep consistent naming and structure matching backend context variables and routes.\n\n**Section 3: Integration and Navigation**\n- Ensure the app starts at the Dashboard page.\n- Navigation buttons route correctly back and forth as per spec.\n- All user actions like adding pets, submitting applications, managing favorites, and messaging function fully.\n\nCRITICAL REQUIREMENTS:\n- Run at most two Generator/Critic iterations.\n- Apply every supported NEED_MODIFY feedback item fully.\n- Use write_text_file tool to save all output files.\n- Respect the data formats and local text files specified.\n- Do not invent unrequested features or pages.\n- Use single-quote docstrings for all code documentation.\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"AppGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"AppGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"code_feedback.md\", \"source\": \"CodeCritic\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        },\n        {\n            \"agent_name\": \"CodeCritic\",\n            \"prompt\": \"\"\"You are a Software Test Engineer specialized in reviewing Python Flask web applications and frontend templates for correctness and specification adherence.\n\nYour goal is to examine the combined app.py backend and templates/*.html frontend code, verify conformity to design_spec.md, and produce gated code_feedback.md for at most two iterations.\n\nTask Details:\n- Read design_spec.md, app.py, and templates/*.html from CONTEXT.\n- Validate syntax and runtime correctness of app.py using validate_python_file tool.\n- Verify all required pages exist with exact element IDs as specified.\n- Check that Flask routes and navigation start from dashboard and function correctly.\n- Confirm local text file data handling is per specification (data formats, files, read/write logic).\n- Ensure frontend templates match backend routes and context variables.\n- Write code_feedback.md starting exactly with [APPROVED] if all checks pass.\n- Write code_feedback.md starting exactly with NEED_MODIFY followed by detailed correction instructions if issues found.\n- Do not add new unrequested features or requirements.\n\nReview Criteria:\n1. Flask app.py syntax and runtime correctness.\n2. All ten pages implemented with required routes and exact element IDs.\n3. Navigation flows and buttons function as described.\n4. Local text file data access (read/write) matches specified data formats and files.\n5. Frontend templates correctly implement layout, elements, and bindings.\n6. Consistency between backend and frontend (e.g., route names, context variables).\n\nCRITICAL REQUIREMENTS:\n- The first bytes of code_feedback.md MUST be exactly [APPROVED] or NEED_MODIFY.\n- Do not include any prefixes, headers, or whitespace before the approval marker.\n- Use write_text_file tool to save the full feedback.\n- Use validate_python_file tool to check backend correctness.\n\nOutput: code_feedback.md\"\"\",\n            \"tools\": [\"write_text_file\", \"validate_python_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"AppGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"AppGenerator\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"code_feedback.md\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"AppGenerator\",\n            \"reviewer_agent\": \"CodeCritic\",\n            \"review_criteria\": \"Validate adherence to design_spec.md with correct element IDs, page navigation from dashboard, data management in local text files, and Python Flask app correctness.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ]\n): pass",
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
    "DesignGenerator": {
        "prompt": (
            """You are a Software Architect specializing in adaptive web application design specifications using Python and local text file data management.

Your goal is to draft or revise a comprehensive web design specification that covers all required pages, exact element IDs, navigation flows, user roles, and local data file formats, producing a complete design_spec.md.

Task Details:
- Read user_task_description from CONTEXT to extract requirements and data formats
- Read existing design_spec.md and design_feedback.md if they exist, applying any NEED_MODIFY feedback
- Produce or update the entire design_spec.md artifact reflecting all 10 pages, element IDs, navigation, workflows, and data file structure
- Overwrite design_spec.md whenever feedback begins NEED_MODIFY; preserve if feedback is [APPROVED]
- Focus solely on specified inputs and outputs; do not add unrequested features

**Section 1: Page Structure and Element IDs**
- Define each of the 10 pages with exact page titles and container element IDs
- Specify all required element IDs per page with their types and roles exactly as described
- Ensure the starting page is Dashboard with the correct ID

**Section 2: Navigation and User Workflows**
- Describe navigation buttons and flows between pages with element IDs used for navigation actions
- Define user roles and relevant access/navigation differences if applicable

**Section 3: Local Data File Formats**
- Detail the data directory structure and text file names (e.g., users.txt, pets.txt, etc.)
- Specify exact data formats with field order, delimiters, and sample example lines
- Ensure data isolation per file type and consistent usage across the application

CRITICAL SUCCESS CRITERIA:
- Run at most two iterations with the critic feedback identifying corrections
- Apply every supported NEED_MODIFY item fully and overwrite design_spec.md accordingly
- Use the write_text_file tool to save the finalized design_spec.md
- Maintain clean separation of concerns: pages, navigation, data formats
- Do not include feedback status markers in design_spec.md

Output: design_spec.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignGenerator'}, {'type': 'text_file', 'name': 'design_feedback.md', 'source': 'DesignCritic'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_spec.md'}],

    },

    "DesignCritic": {
        "prompt": (
            """You are a Design Quality Assurance Engineer specializing in reviewing adaptive web application design specifications for Python projects with local file data handling.

Your goal is to review the design_spec.md against the full user_task_description and requirements, providing structured feedback in design_feedback.md starting explicitly with [APPROVED] or NEED_MODIFY, enabling gated refinement for at most two iterations.

Task Details:
- Read user_task_description and design_spec.md from CONTEXT
- Review coverage of all 10 pages, exact element IDs, page titles, and container elements
- Verify navigation flows between pages and correct usage of navigation element IDs
- Confirm user roles and any access distinctions are properly described
- Validate local data file structures, names, delimiters, field ordering, and example data lines
- Ensure the Dashboard page is the starting page and uses the correct container ID
- Write feedback that begins exactly with [APPROVED] if all criteria met or NEED_MODIFY with precise changes if issues found

Review Criteria:
1. Complete page specifications with exact element IDs matching user requirements
2. Correct, unambiguous navigation flows and user workflow definitions
3. Accurate data file formats and examples consistent with user_task_description
4. No additions beyond user-defined requirements or unsupported features

CRITICAL REQUIREMENTS:
- design_feedback.md must start at byte-1 with [APPROVED] or NEED_MODIFY marker, no preceding whitespace or text
- Use write_text_file tool to save the entire feedback artifact
- At most two critique iterations; stop immediately on [APPROVED]

Output: design_feedback.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignGenerator'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_feedback.md'}],

    },

    "AppGenerator": {
        "prompt": (
            """You are a Python Flask full-stack developer specialized in building web applications with local text file-based data storage.

Your goal is to fully implement or revise the entire Python Flask backend app.py and the complete frontend HTML templates (templates/*.html) to fulfill the design_spec.md specification, for at most two iterations of refinement.

Task Details:
- Read design_spec.md, the current app.py, templates/*.html, and code_feedback.md from CONTEXT.
- On the first iteration, create complete app.py and all HTML templates implementing all 10 pages exactly as specified.
- On later iterations, when code_feedback.md begins with NEED_MODIFY, revise the entire app.py and templates to address all feedback.
- When feedback begins [APPROVED], preserve the approved implementation.
- Focus on exact element IDs, correct Flask routes, page navigation starting from dashboard, and local text file data handling as specified.
- Output complete app.py and all template files under templates/ directory.

**Section 1: Flask Backend Implementation**
- Implement all routes for the 10 pages with HTTP methods and route paths as per design_spec.md.
- Handle reading, writing, and updating all required local text files in the 'data' directory exactly as specified.
- Ensure data formats, parsing, and updates follow the specification.
- Implement form data handling, filtering, and session state (e.g., favorites).
- Use Python code comments with single-quote docstrings only, no triple-double quotes.

**Section 2: Frontend Templates Implementation**
- Develop complete HTML templates for each page inside templates/*.html directories.
- Include all specified elements with exact IDs and types as described.
- Ensure buttons and navigation links correctly route between pages.
- Keep consistent naming and structure matching backend context variables and routes.

**Section 3: Integration and Navigation**
- Ensure the app starts at the Dashboard page.
- Navigation buttons route correctly back and forth as per spec.
- All user actions like adding pets, submitting applications, managing favorites, and messaging function fully.

CRITICAL REQUIREMENTS:
- Run at most two Generator/Critic iterations.
- Apply every supported NEED_MODIFY feedback item fully.
- Use write_text_file tool to save all output files.
- Respect the data formats and local text files specified.
- Do not invent unrequested features or pages.
- Use single-quote docstrings for all code documentation.

Output: app.py, templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignGenerator'}, {'type': 'text_file', 'name': 'app.py', 'source': 'AppGenerator'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'AppGenerator'}, {'type': 'text_file', 'name': 'code_feedback.md', 'source': 'CodeCritic'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}],

    },

    "CodeCritic": {
        "prompt": (
            """You are a Software Test Engineer specialized in reviewing Python Flask web applications and frontend templates for correctness and specification adherence.

Your goal is to examine the combined app.py backend and templates/*.html frontend code, verify conformity to design_spec.md, and produce gated code_feedback.md for at most two iterations.

Task Details:
- Read design_spec.md, app.py, and templates/*.html from CONTEXT.
- Validate syntax and runtime correctness of app.py using validate_python_file tool.
- Verify all required pages exist with exact element IDs as specified.
- Check that Flask routes and navigation start from dashboard and function correctly.
- Confirm local text file data handling is per specification (data formats, files, read/write logic).
- Ensure frontend templates match backend routes and context variables.
- Write code_feedback.md starting exactly with [APPROVED] if all checks pass.
- Write code_feedback.md starting exactly with NEED_MODIFY followed by detailed correction instructions if issues found.
- Do not add new unrequested features or requirements.

Review Criteria:
1. Flask app.py syntax and runtime correctness.
2. All ten pages implemented with required routes and exact element IDs.
3. Navigation flows and buttons function as described.
4. Local text file data access (read/write) matches specified data formats and files.
5. Frontend templates correctly implement layout, elements, and bindings.
6. Consistency between backend and frontend (e.g., route names, context variables).

CRITICAL REQUIREMENTS:
- The first bytes of code_feedback.md MUST be exactly [APPROVED] or NEED_MODIFY.
- Do not include any prefixes, headers, or whitespace before the approval marker.
- Use write_text_file tool to save the full feedback.
- Use validate_python_file tool to check backend correctness.

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
        ("DesignCritic", """Verify the design specification correctly covers all pages, elements, data files, navigation flows, user roles, and the start point dashboard with required element IDs exactly."
            ,
            "review_artifacts": [
                {"type": "text_file", "name": "design_spec.md""", [])
    ],

    'AppGenerator': [
        ("CodeCritic", """Validate adherence to design_spec.md with correct element IDs, page navigation from dashboard, data management in local text files, and Python Flask app correctness.""", [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}])
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
            "Create or revise the complete design_spec.md covering all 10 pages, element IDs, navigation flows, user roles, and data file formats.\n\n"
            f"=== Current design_spec.md ===\n{current_design}\n\n"
            f"=== DesignCritic Feedback ===\n{feedback_content}"
        )

        try:
            current_design = open("design_spec.md").read()
        except FileNotFoundError:
            current_design = ""

        await execute(
            DesignCritic,
            "Review the latest design_spec.md against user_task_description for coverage, correctness, and completeness of all 10 pages, element IDs, navigation flows, user roles, and local data file formats.\n"
            "Write design_feedback.md starting exactly with [APPROVED] or NEED_MODIFY.\n\n"
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
import asyncio
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

        # Run AppGenerator with current app.py, templates/*.html, design_spec.md, and feedback
        await execute(
            AppGenerator,
            "Create or revise the complete app.py and templates/*.html.\n\n"
            f"=== design_spec.md ===\n{CONTEXT.get('design_spec.md', '')}\n\n"
            f"=== Current app.py ===\n{app_content}\n\n"
            f"=== Current Templates ===\n{templates_content}\n\n"
            f"=== CodeCritic Feedback ===\n{feedback_content}"
        )

        # Reload updated app.py and templates for CodeCritic review
        app_content = ""
        templates_content = ""
        try:
            app_content = open("app.py").read()
        except FileNotFoundError:
            pass
        for template_path in sorted(glob.glob("templates/*.html")):
            try:
                templates_content += f"\n=== {template_path} ===\n" + open(template_path).read()
            except OSError:
                pass
        
        await execute(
            CodeCritic,
            "Review the latest app.py and templates against design_spec.md. "
            "Write code_feedback.md starting exactly with [APPROVED] or NEED_MODIFY.\n\n"
            f"=== design_spec.md ===\n{CONTEXT.get('design_spec.md', '')}\n\n"
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
