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
# 20260714_001750_079330/main_20260714_001750_079330.py

# Phase_info dictionary containing complete def blocks for failover context
Phase_info = {
    "phase1": "def design_specification_phase(\n    goal: str = \"Refine and produce a comprehensive design specification document for the RealEstate Python web app, delivering design_spec.md and gated design_feedback.md.\",\n    collab_pattern_name: str = \"Refinement Loop\",\n    collab_pattern_description: str = (\n        \"DesignGenerator creates or revises design_spec.md detailing the architecture, pages, elements with exact IDs, \"\n        \"and data storage model from user_task_description and design_feedback.md; DesignCritic reviews the design_spec.md \"\n        \"against the user requirements and writes design_feedback.md to be either [APPROVED] or NEED_MODIFY, \"\n        \"enabling iterative refinement up to two iterations.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"DesignGenerator\",\n            \"prompt\": \"\"\"You are a Software Architect specializing in Python web application design specifications.\n\nYour goal is to produce and iteratively refine a complete design_spec.md for a RealEstate web application based on user requirements, architecture, UI elements, and data storage models.\n\nTask Details:\n- Read user_task_description from CONTEXT to understand all user requirements\n- Read current design_spec.md and design_feedback.md from CONTEXT if present\n- On first iteration, author a full design_spec.md describing dashboard start page, all eight pages with exact element IDs, user interactions, navigation flows, and local text file data storage schema\n- On feedback beginning with NEED_MODIFY, incorporate every requested correction fully and rewrite complete design_spec.md\n- Stop iteration on feedback starting with [APPROVED]\n\n**Section 1: UI Pages and Navigation**\n- Specify the eight defined pages with exact page titles and all element IDs as given\n- Detail user interface components, including buttons, inputs, dropdowns, tables, and their roles\n- Describe navigation flows between pages and how buttons and links trigger navigation actions\n\n**Section 2: User Interaction and Functionality**\n- Define core user interactions like search filters, property detail views, inquiry submissions, favorites management, and agent/contact actions\n- Include precise button IDs, action triggers, and expected behaviors for dynamic elements and property listings\n\n**Section 3: Data Storage Model**\n- Specify text file names, data formats, field sequences, and sample data content exactly as required\n- Describe how data files support UI features and link to element functionality (e.g., properties.txt for listings, inquiries.txt for submissions)\n- Do not invent additional data files or fields\n\nCRITICAL SUCCESS CRITERIA:\n- Run at most two iterations incorporating all NEED_MODIFY feedback exactly\n- Deliver design_spec.md with no partial or summary feedback\n- Use write_text_file tool to save design_spec.md\n- Do not write any feedback markers in design_spec.md\n- Align all naming conventions and data formats exactly to user requirements\n\nOutput: design_spec.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"design_feedback.md\", \"source\": \"DesignCritic\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"DesignCritic\",\n            \"prompt\": \"\"\"You are a Design Reviewer specializing in Python web application specification audits.\n\nYour goal is to critically evaluate design_spec.md for compliance with full user requirements and provide gated, actionable feedback for at most two refinement iterations.\n\nTask Details:\n- Read user_task_description and design_spec.md from CONTEXT\n- Review design_spec.md coverage of all eight specified pages, exact element IDs, navigation flows, user interactions, and data storage files/formats\n- Ensure no user requirement or data specification is omitted or inaccurately represented\n- Write feedback file design_feedback.md starting with either [APPROVED] if fully compliant, or NEED_MODIFY for required corrections with clear detail\n\nReview Checklist:\n1. Verify inclusion and accuracy of all eight pages with correct page titles and element IDs as per user task\n2. Check user interaction details (search, filtering, property viewing, inquiry submission, favorites, agent contacts) are complete and consistent\n3. Confirm navigation and button action flows correctly described and aligned with UI elements\n4. Validate all local data file names, fields, formats, and example data exactly match user requirements\n5. Do not add requirements beyond those specified by the user\n\nCRITICAL REQUIREMENTS:\n- The first bytes of design_feedback.md must be exactly [APPROVED] or NEED_MODIFY\n- Provide precise, actionable feedback for each missing or inconsistent item on NEED_MODIFY\n- Use write_text_file tool to save design_feedback.md\n- Limit to at most two iterations, stop immediately when [APPROVED]\n\nOutput: design_feedback.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignGenerator\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_feedback.md\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"DesignGenerator\",\n            \"reviewer_agent\": \"DesignCritic\",\n            \"review_criteria\": \"Validate comprehensive coverage of all 8 pages, accurate element IDs, data file formats, and logical navigation flows; ensure design is fully aligned with user requirements without missing any constraint.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"},\n                {\"type\": \"text_file\", \"name\": \"design_feedback.md\"}\n            ]\n        }\n    ]\n): pass",
    "phase2": "def implementation_and_verification_phase(\n    goal: str = \"Refine the Python Flask web app implementation including app.py and templates/*.html for the RealEstate site, plus gated code_feedback.md for correctness and completeness.\",\n    collab_pattern_name: str = \"Refinement Loop\",\n    collab_pattern_description: str = (\n        \"AppGenerator writes or revises app.py and all required templates/*.html files implementing the RealEstate app functionality \"\n        \"based on design_spec.md and previous code_feedback.md; CodeCritic reviews the code and templates for full adherence to design, \"\n        \"correct element IDs, functionality, and data file integration; then writes code_feedback.md with either [APPROVED] or NEED_MODIFY, \"\n        \"allowing up to two iterations of refinement.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"AppGenerator\",\n            \"prompt\": \"\"\"You are a Python Flask Developer specializing in building full-stack web applications with local text file data integration.\n\nYour goal is to develop and iteratively refine a complete Flask web application implementation including app.py and HTML templates, fully realizing the dashboard, search, details, inquiries, favorites, agents directory, and locations pages, with precise element IDs and data file usage.\n\nTask Details:\n- Read design_spec.md, existing app.py, templates/*.html, and code_feedback.md from CONTEXT\n- On the first iteration, deliver a complete implementation of app.py and all HTML templates\n- When code_feedback.md begins with NEED_MODIFY, incorporate all requested changes and overwrite the complete implementation\n- When code_feedback.md begins with [APPROVED], preserve the approved implementation without changes\n- Output updated app.py and all templates/*.html implementing all features and correct UI element IDs described in design_spec.md\n\n**Implementation Requirements:**\n- Implement all 8 specified pages with correct routing, templates, and UI elements matching exact element IDs\n- Enable browsing, filtering, searching properties by location/price/type\n- Implement property details viewing, inquiry submission, favorites management, agents directory, and location listings\n- Manage data solely via local text files in the data directory using formats specified (properties.txt, inquiries.txt, favorites.txt, agents.txt, locations.txt)\n- Integrate loading, saving, and updating data files for dynamic features (e.g., adding favorites, submitting inquiries)\n\n**Templates Specification:**\n- Create HTML files for each page per design_spec.md structure\n- Use exact element IDs for containers, inputs, buttons, tables, and other UI components\n- Ensure buttons and interactive elements trigger correct Flask route functionality\n\n**Code Style and Tools:**\n- Use Flask best practices with route decorators, functions, template rendering, and file I/O\n- Write modular, readable code with comments explaining key sections\n- Use write_text_file tool to save app.py and all templates/*.html files\n\nCRITICAL SUCCESS CRITERIA:\n- Run at most two iterations incorporating every NEED_MODIFY feedback fully\n- Maintain exact element IDs and input/output contracts as per design_spec.md\n- Do not add unrequested functionality or deviate from design_spec.md\n- Use write_text_file exclusively for output\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"AppGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"AppGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"code_feedback.md\", \"source\": \"CodeCritic\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        },\n        {\n            \"agent_name\": \"CodeCritic\",\n            \"prompt\": \"\"\"You are a Software Test Engineer specializing in Python Flask web application code and template review.\n\nYour goal is to rigorously review app.py and all HTML templates for completeness, correctness, and full adherence to the design_spec.md, providing gated feedback for up to two iterations.\n\nTask Details:\n- Read design_spec.md, app.py, and templates/*.html from CONTEXT\n- Verify that all 8 specified pages are implemented with exact element IDs as described\n- Confirm routes and navigation work correctly and correspond to all required pages and features\n- Validate that local text file integration is correctly implemented for properties, inquiries, favorites, agents, and locations data\n- Check for absence of errors, inconsistencies, or deviations from design_spec.md in both code and templates\n- Write code_feedback.md starting with either [APPROVED] if the implementation fully meets requirements,\n  or NEED_MODIFY followed by detailed, actionable corrections specifying what to fix\n\nReview Checklist:\n1. Complete implementation of all pages and UI elements per design_spec.md including correct element IDs\n2. Correct Flask routing and handling of HTTP methods for all user actions\n3. Proper data file reading, writing, and updating logic matching specified local text files formats\n4. Consistency and correctness of navigation buttons and interactive elements\n5. No missing features or extraneous deviations from design_spec.md\n6. Clear, precise feedback with byte-1 feedback marker ([APPROVED] or NEED_MODIFY)\n\nCRITICAL REQUIREMENTS:\n- The first bytes of code_feedback.md MUST be exactly [APPROVED] or NEED_MODIFY\n- Provide no additional prefix or extraneous content before the feedback marker\n- Use write_text_file tool to save complete feedback text file\n\nOutput: code_feedback.md\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"AppGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"AppGenerator\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"code_feedback.md\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"AppGenerator\",\n            \"reviewer_agent\": \"CodeCritic\",\n            \"review_criteria\": \"Review for complete functional implementation of all required pages with correct element IDs, full data access and manipulation, navigation correctness, and absence of errors or deviations from design_spec.md.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ]\n): pass",
}

user_task = """
# Requirements Document for 'RealEstate' Web Application

## 1. Objective
Develop a comprehensive web application named 'RealEstate' using Python, with data managed through local text files. The application enables users to browse property listings, search by location and price, view property details, submit inquiries, and manage favorite properties. No authentication required - all features are directly accessible. Note that the website should start from the Dashboard page.

## 2. Language
The required development language for the 'RealEstate' application is Python.

## 3. Page Design

The 'RealEstate' web application will consist of the following eight pages:

### 1. Dashboard Page
- **Page Title**: Real Estate Dashboard
- **Overview**: The main hub displaying featured properties, recent listings, and quick navigation to all functionalities.
- **Elements**:
  - **ID: dashboard-page** - Type: Div - Container for the dashboard page.
  - **ID: featured-properties** - Type: Div - Display of featured property recommendations.
  - **ID: browse-properties-button** - Type: Button - Button to navigate to property search page.
  - **ID: my-inquiries-button** - Type: Button - Button to navigate to inquiries page.
  - **ID: my-favorites-button** - Type: Button - Button to navigate to favorites page.

### 2. Property Search Page
- **Page Title**: Property Search
- **Overview**: A page displaying all available properties with advanced search and filter capabilities.
- **Elements**:
  - **ID: search-page** - Type: Div - Container for the search page.
  - **ID: location-input** - Type: Input - Field to search properties by location/city.
  - **ID: price-range-min** - Type: Input (number) - Field to set minimum price filter.
  - **ID: price-range-max** - Type: Input (number) - Field to set maximum price filter.
  - **ID: property-type-filter** - Type: Dropdown - Dropdown to filter by property type (House, Apartment, Condo, Land).
  - **ID: properties-grid** - Type: Div - Grid displaying property cards with image, location, price, and beds/baths.
  - **ID: view-property-button-{property_id}** - Type: Button - Button to view property details (each property card has this).

### 3. Property Details Page
- **Page Title**: Property Details
- **Overview**: A page displaying detailed information about a specific property.
- **Elements**:
  - **ID: property-details-page** - Type: Div - Container for the property details page.
  - **ID: property-address** - Type: H1 - Display property address.
  - **ID: property-price** - Type: Div - Display property price.
  - **ID: property-description** - Type: Div - Display property description.
  - **ID: property-features** - Type: Div - Display property features (beds, baths, square footage).
  - **ID: add-to-favorites-button** - Type: Button - Button to add property to favorites.
  - **ID: submit-inquiry-button** - Type: Button - Button to submit inquiry for property.

### 4. Property Inquiry Page
- **Page Title**: Submit Property Inquiry
- **Overview**: A page for users to submit inquiries for properties they are interested in.
- **Elements**:
  - **ID: inquiry-page** - Type: Div - Container for the inquiry page.
  - **ID: select-property** - Type: Dropdown - Dropdown to select property for inquiry.
  - **ID: inquiry-name** - Type: Input - Field to input customer name.
  - **ID: inquiry-email** - Type: Input (email) - Field to input customer email.
  - **ID: inquiry-phone** - Type: Input (tel) - Field to input customer phone.
  - **ID: inquiry-message** - Type: Textarea - Field to write inquiry message.
  - **ID: submit-inquiry-button** - Type: Button - Button to submit inquiry.

### 5. My Inquiries Page
- **Page Title**: My Inquiries
- **Overview**: A page displaying all submitted inquiries and their status.
- **Elements**:
  - **ID: inquiries-page** - Type: Div - Container for the inquiries page.
  - **ID: inquiries-table** - Type: Table - Table displaying inquiries with property, date, status, and contact info.
  - **ID: inquiry-status-filter** - Type: Dropdown - Dropdown to filter by status (All, Pending, Contacted, Resolved).
  - **ID: delete-inquiry-button-{inquiry_id}** - Type: Button - Button to delete inquiry (each inquiry has this).
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 6. My Favorites Page
- **Page Title**: My Favorite Properties
- **Overview**: A page displaying all properties added to favorites.
- **Elements**:
  - **ID: favorites-page** - Type: Div - Container for the favorites page.
  - **ID: favorites-list** - Type: Div - List of all favorite properties with address, price, and action buttons.
  - **ID: remove-from-favorites-button-{property_id}** - Type: Button - Button to remove property from favorites (each property has this).
  - **ID: view-property-button-{property_id}** - Type: Button - Button to view property details (each property has this).
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 7. Agent Directory Page
- **Page Title**: Real Estate Agents
- **Overview**: A page displaying all real estate agents and their contact information.
- **Elements**:
  - **ID: agents-page** - Type: Div - Container for the agents page.
  - **ID: agents-list** - Type: Div - List of all agents with photo, name, specialization, and contact info.
  - **ID: agent-search** - Type: Input - Field to search agents by name.
  - **ID: contact-agent-button-{agent_id}** - Type: Button - Button to contact agent (each agent has this).
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 8. Locations Page
- **Page Title**: Featured Locations
- **Overview**: A page displaying popular locations with property count and details.
- **Elements**:
  - **ID: locations-page** - Type: Div - Container for the locations page.
  - **ID: locations-list** - Type: Div - List of all locations with name, property count, and average price.
  - **ID: view-location-button-{location_id}** - Type: Button - Button to view properties in location (each location has this).
  - **ID: location-sort** - Type: Dropdown - Dropdown to sort locations (By Name, By Properties Count, By Average Price).
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

## 4. Data Storage

The 'RealEstate' application will store data locally in text files organized in the directory 'data'. The following data formats and examples are defined:

### 1. Properties Data
- **File Name**: `properties.txt`
- **Data Format**:
  ```
  property_id|address|location|price|property_type|bedrooms|bathrooms|square_feet|description|agent_id|status
  ```
- **Example Data**:
  ```
  1|123 Oak Street|Downtown|450000|House|3|2|2500|Beautiful family home with large yard|101|Available
  2|456 Park Avenue|Midtown|350000|Apartment|2|1.5|1200|Modern apartment with city view|102|Available
  3|789 Elm Road|Suburb|280000|Condo|2|2|1500|Cozy condo in quiet neighborhood|101|Sold
  ```

### 2. Locations Data
- **File Name**: `locations.txt`
- **Data Format**:
  ```
  location_id|location_name|region|average_price|property_count|description
  ```
- **Example Data**:
  ```
  1|Downtown|Central|425000|45|Urban area with business district
  2|Midtown|Central|380000|38|Mixed residential and commercial zone
  3|Suburb|Outskirts|295000|52|Family-friendly residential area
  ```

### 3. Property Inquiries Data
- **File Name**: `inquiries.txt`
- **Data Format**:
  ```
  inquiry_id|property_id|customer_name|customer_email|customer_phone|message|inquiry_date|status
  ```
- **Example Data**:
  ```
  1|1|John Smith|john@email.com|555-1234|Interested in viewing this weekend|2025-01-15|Pending
  2|2|Sarah Johnson|sarah@email.com|555-5678|Can we schedule a showing?|2025-01-16|Contacted
  3|1|Mike Davis|mike@email.com|555-9012|What is the lowest offer?|2025-01-17|Resolved
  ```

### 4. Favorite Properties Data
- **File Name**: `favorites.txt`
- **Data Format**:
  ```
  favorite_id|property_id|added_date
  ```
- **Example Data**:
  ```
  1|1|2025-01-10
  2|2|2025-01-12
  3|3|2025-01-14
  ```

### 5. Real Estate Agents Data
- **File Name**: `agents.txt`
- **Data Format**:
  ```
  agent_id|agent_name|specialization|email|phone|properties_sold
  ```
- **Example Data**:
  ```
  101|Robert Wilson|Residential Properties|robert@email.com|555-0001|125
  102|Emily Chen|Commercial Real Estate|emily@email.com|555-0002|89
  103|James Martinez|Luxury Homes|james@email.com|555-0003|67
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
            """You are a Software Architect specializing in Python web application design specifications.

Your goal is to produce and iteratively refine a complete design_spec.md for a RealEstate web application based on user requirements, architecture, UI elements, and data storage models.

Task Details:
- Read user_task_description from CONTEXT to understand all user requirements
- Read current design_spec.md and design_feedback.md from CONTEXT if present
- On first iteration, author a full design_spec.md describing dashboard start page, all eight pages with exact element IDs, user interactions, navigation flows, and local text file data storage schema
- On feedback beginning with NEED_MODIFY, incorporate every requested correction fully and rewrite complete design_spec.md
- Stop iteration on feedback starting with [APPROVED]

**Section 1: UI Pages and Navigation**
- Specify the eight defined pages with exact page titles and all element IDs as given
- Detail user interface components, including buttons, inputs, dropdowns, tables, and their roles
- Describe navigation flows between pages and how buttons and links trigger navigation actions

**Section 2: User Interaction and Functionality**
- Define core user interactions like search filters, property detail views, inquiry submissions, favorites management, and agent/contact actions
- Include precise button IDs, action triggers, and expected behaviors for dynamic elements and property listings

**Section 3: Data Storage Model**
- Specify text file names, data formats, field sequences, and sample data content exactly as required
- Describe how data files support UI features and link to element functionality (e.g., properties.txt for listings, inquiries.txt for submissions)
- Do not invent additional data files or fields

CRITICAL SUCCESS CRITERIA:
- Run at most two iterations incorporating all NEED_MODIFY feedback exactly
- Deliver design_spec.md with no partial or summary feedback
- Use write_text_file tool to save design_spec.md
- Do not write any feedback markers in design_spec.md
- Align all naming conventions and data formats exactly to user requirements

Output: design_spec.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignGenerator'}, {'type': 'text_file', 'name': 'design_feedback.md', 'source': 'DesignCritic'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_spec.md'}],

    },

    "DesignCritic": {
        "prompt": (
            """You are a Design Reviewer specializing in Python web application specification audits.

Your goal is to critically evaluate design_spec.md for compliance with full user requirements and provide gated, actionable feedback for at most two refinement iterations.

Task Details:
- Read user_task_description and design_spec.md from CONTEXT
- Review design_spec.md coverage of all eight specified pages, exact element IDs, navigation flows, user interactions, and data storage files/formats
- Ensure no user requirement or data specification is omitted or inaccurately represented
- Write feedback file design_feedback.md starting with either [APPROVED] if fully compliant, or NEED_MODIFY for required corrections with clear detail

Review Checklist:
1. Verify inclusion and accuracy of all eight pages with correct page titles and element IDs as per user task
2. Check user interaction details (search, filtering, property viewing, inquiry submission, favorites, agent contacts) are complete and consistent
3. Confirm navigation and button action flows correctly described and aligned with UI elements
4. Validate all local data file names, fields, formats, and example data exactly match user requirements
5. Do not add requirements beyond those specified by the user

CRITICAL REQUIREMENTS:
- The first bytes of design_feedback.md must be exactly [APPROVED] or NEED_MODIFY
- Provide precise, actionable feedback for each missing or inconsistent item on NEED_MODIFY
- Use write_text_file tool to save design_feedback.md
- Limit to at most two iterations, stop immediately when [APPROVED]

Output: design_feedback.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignGenerator'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_feedback.md'}],

    },

    "AppGenerator": {
        "prompt": (
            """You are a Python Flask Developer specializing in building full-stack web applications with local text file data integration.

Your goal is to develop and iteratively refine a complete Flask web application implementation including app.py and HTML templates, fully realizing the dashboard, search, details, inquiries, favorites, agents directory, and locations pages, with precise element IDs and data file usage.

Task Details:
- Read design_spec.md, existing app.py, templates/*.html, and code_feedback.md from CONTEXT
- On the first iteration, deliver a complete implementation of app.py and all HTML templates
- When code_feedback.md begins with NEED_MODIFY, incorporate all requested changes and overwrite the complete implementation
- When code_feedback.md begins with [APPROVED], preserve the approved implementation without changes
- Output updated app.py and all templates/*.html implementing all features and correct UI element IDs described in design_spec.md

**Implementation Requirements:**
- Implement all 8 specified pages with correct routing, templates, and UI elements matching exact element IDs
- Enable browsing, filtering, searching properties by location/price/type
- Implement property details viewing, inquiry submission, favorites management, agents directory, and location listings
- Manage data solely via local text files in the data directory using formats specified (properties.txt, inquiries.txt, favorites.txt, agents.txt, locations.txt)
- Integrate loading, saving, and updating data files for dynamic features (e.g., adding favorites, submitting inquiries)

**Templates Specification:**
- Create HTML files for each page per design_spec.md structure
- Use exact element IDs for containers, inputs, buttons, tables, and other UI components
- Ensure buttons and interactive elements trigger correct Flask route functionality

**Code Style and Tools:**
- Use Flask best practices with route decorators, functions, template rendering, and file I/O
- Write modular, readable code with comments explaining key sections
- Use write_text_file tool to save app.py and all templates/*.html files

CRITICAL SUCCESS CRITERIA:
- Run at most two iterations incorporating every NEED_MODIFY feedback fully
- Maintain exact element IDs and input/output contracts as per design_spec.md
- Do not add unrequested functionality or deviate from design_spec.md
- Use write_text_file exclusively for output

Output: app.py, templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignGenerator'}, {'type': 'text_file', 'name': 'app.py', 'source': 'AppGenerator'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'AppGenerator'}, {'type': 'text_file', 'name': 'code_feedback.md', 'source': 'CodeCritic'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}],

    },

    "CodeCritic": {
        "prompt": (
            """You are a Software Test Engineer specializing in Python Flask web application code and template review.

Your goal is to rigorously review app.py and all HTML templates for completeness, correctness, and full adherence to the design_spec.md, providing gated feedback for up to two iterations.

Task Details:
- Read design_spec.md, app.py, and templates/*.html from CONTEXT
- Verify that all 8 specified pages are implemented with exact element IDs as described
- Confirm routes and navigation work correctly and correspond to all required pages and features
- Validate that local text file integration is correctly implemented for properties, inquiries, favorites, agents, and locations data
- Check for absence of errors, inconsistencies, or deviations from design_spec.md in both code and templates
- Write code_feedback.md starting with either [APPROVED] if the implementation fully meets requirements,
  or NEED_MODIFY followed by detailed, actionable corrections specifying what to fix

Review Checklist:
1. Complete implementation of all pages and UI elements per design_spec.md including correct element IDs
2. Correct Flask routing and handling of HTTP methods for all user actions
3. Proper data file reading, writing, and updating logic matching specified local text files formats
4. Consistency and correctness of navigation buttons and interactive elements
5. No missing features or extraneous deviations from design_spec.md
6. Clear, precise feedback with byte-1 feedback marker ([APPROVED] or NEED_MODIFY)

CRITICAL REQUIREMENTS:
- The first bytes of code_feedback.md MUST be exactly [APPROVED] or NEED_MODIFY
- Provide no additional prefix or extraneous content before the feedback marker
- Use write_text_file tool to save complete feedback text file

Output: code_feedback.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignGenerator'}, {'type': 'text_file', 'name': 'app.py', 'source': 'AppGenerator'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'AppGenerator'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'code_feedback.md'}],

    }

}

REVIEW_PROFILES = {
    'DesignGenerator': [
        ("DesignCritic", """Validate comprehensive coverage of all 8 pages, accurate element IDs, data file formats, and logical navigation flows; ensure design is fully aligned with user requirements without missing any constraint.""", [{'type': 'text_file', 'name': 'design_spec.md'}, {'type': 'text_file', 'name': 'design_feedback.md'}])
    ],

    'AppGenerator': [
        ("CodeCritic", """Review for complete functional implementation of all required pages with correct element IDs, full data access and manipulation, navigation correctness, and absence of errors or deviations from design_spec.md.""", [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}, {'type': 'text_file', 'name': 'design_spec.md'}])
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
        timeout_threshold=350,
        failure_threshold=1,
        recovery_time=40
    )
    DesignCritic = build_resilient_agent(
        agent_name="DesignCritic",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=2,
        timeout_threshold=350,
        failure_threshold=1,
        recovery_time=40
    )

    MAX_ITERATIONS = 2
    for iteration in range(MAX_ITERATIONS):
        current_design = ""
        feedback_content = ""
        try:
            with open("design_spec.md", "r", encoding="utf-8") as f:
                current_design = f.read()
        except FileNotFoundError:
            current_design = ""

        if iteration > 0:
            try:
                with open("design_feedback.md", "r", encoding="utf-8") as f:
                    feedback_content = f.read()
            except FileNotFoundError:
                feedback_content = ""

        # Run DesignGenerator with current design and feedback
        await execute(
            DesignGenerator,
            "Produce or revise the complete design_spec.md for the RealEstate web app.\n"
            "Incorporate all NEED_MODIFY feedback if any; if feedback starts with [APPROVED], stop revisions.\n\n"
            f"=== Current design_spec.md ===\n{current_design}\n\n"
            f"=== DesignCritic Feedback ===\n{feedback_content}"
        )

        try:
            with open("design_spec.md", "r", encoding="utf-8") as f:
                current_design = f.read()
        except FileNotFoundError:
            current_design = ""

        # Run DesignCritic on latest design_spec.md
        await execute(
            DesignCritic,
            "Review the latest design_spec.md for full compliance with user requirements.\n"
            "Write design_feedback.md starting exactly with [APPROVED] if fully compliant or NEED_MODIFY with detailed corrections.\n\n"
            f"=== Latest design_spec.md ===\n{current_design}"
        )

        try:
            with open("design_feedback.md", "r", encoding="utf-8") as f:
                feedback_content = f.read()
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
