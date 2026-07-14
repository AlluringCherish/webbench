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
# 20260714_021737_473295/main_20260714_021737_473295.py

# Phase_info dictionary containing complete def blocks for failover context
Phase_info = {
    "phase1": "def design_specification_phase(\n    goal: str = \"Debate and finalize a comprehensive adaptive design_spec.md for the TravelPlanner Flask web application with exact page routes, method contracts, element IDs, and data storage formats.\",\n    collab_pattern_name: str = \"Multi-Agent Debate\",\n    collab_pattern_description: str = (\n        \"DesignDebaterA and DesignDebaterB independently draft their candidate design_spec.md documents in round 1 based on user requirements, \"\n        \"then each revises their documents in round 2 by incorporating or rebutting peer artifacts. DesignJudge adjudicates and synthesizes the final \"\n        \"design_spec.md reflecting the adaptive Web Contract and user requirements.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"DesignDebaterA\",\n            \"prompt\": \"\"\"You are a System Architect specializing in Flask web application design specifications.\n\nYour goal is to create and revise a complete design_spec.md for the TravelPlanner web app through exactly two debate rounds.\n\nTask Details:\n- Read the entire user_task_description in every round for design context\n- In round 1, independently draft design_debate_a.md covering Flask route mappings, HTTP methods, template files, and exact element IDs for all TravelPlanner pages\n- In round 2, revise design_debate_a.md by reading the input design_debate_a.md and peer design_debate_b.md, integrating valid peer improvements or rebuttals\n- Output a complete, implementation-ready design_debate_a.md after each round\n\n**Section 1: Flask Routes and HTTP Methods**\n- Specify each route path exactly as in the User Task\n- Define the HTTP methods allowed (GET, POST, etc.) with correct forms and actions\n- Explicitly mark the route for root '/' as entry rendering Dashboard page\n\n**Section 2: Template Files and HTML Elements**\n- List precise template filenames per page\n- Define all element IDs including dynamic IDs exactly as declared (e.g., view-destination-button-{dest_id})\n- Describe page titles and navigation button routes\n\n**Section 3: Data Storage File Formats**\n- Specify all local text file names and exact data formats with field order, delimiters, and example rows\n- Do not invent data files beyond user specification\n\nCRITICAL SUCCESS CRITERIA:\n- Must strictly preserve all user-declared routes, methods, template names, and element IDs\n- Produce a design document fully consistent with user requirements and peer feedback after round 2\n- Use write_text_file tool to output design_debate_a.md\n\nOutput: design_debate_a.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_debate_a.md\", \"source\": \"DesignDebaterA\"},\n                {\"type\": \"text_file\", \"name\": \"design_debate_b.md\", \"source\": \"DesignDebaterB\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_debate_a.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"DesignDebaterB\",\n            \"prompt\": \"\"\"You are a Software Architect specializing in Flask web application design specifications.\n\nYour goal is to produce and refine a comprehensive design_spec.md for the TravelPlanner app in exactly two debate rounds.\n\nTask Details:\n- Thoroughly review user_task_description in every round to understand the app workflow\n- Independently write design_debate_b.md in round 1 focusing on route definitions, data persistence behavior, template filenames, and exact HTML element IDs for all pages\n- In round 2, read the round 1 artifact and the peer's final design_debate_a.md, revising your design_debate_b.md to address peer points supported by user requirements\n- Overwrite and submit the complete design_debate_b.md after each round\n\n**Section 1: Route and URL Structure**\n- Define exact route paths and navigation targets, including root '/' redirecting or rendering Dashboard page\n- Specify HTTP methods and form action attributes exactly as required\n\n**Section 2: Template and HTML Element Details**\n- Provide exact template filenames as used in the application\n- Enumerate all HTML element IDs including dynamic patterns like view-package-details-button-{pkg_id}\n- Maintain exact consistency of element IDs and navigation button targets\n\n**Section 3: Local Text Data Persistence**\n- Define all data files used with exact file names and delineate their content schema with fields and delimiters\n- Describe the reading and writing behavior tied to each data file without adding unsupported files\n\nCRITICAL SUCCESS CRITERIA:\n- Preserve all user-specified exact routes, methods, templates, and element IDs without deviation\n- Produce a clear, consistent, and complete design after two rounds integrating pertinent peer corrections\n- Use write_text_file tool to save output as design_debate_b.md\n\nOutput: design_debate_b.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_debate_b.md\", \"source\": \"DesignDebaterB\"},\n                {\"type\": \"text_file\", \"name\": \"design_debate_a.md\", \"source\": \"DesignDebaterA\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_debate_b.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"DesignJudge\",\n            \"prompt\": \"\"\"You are a Senior System Architect adjudicating two competing design specifications for a Flask web application.\n\nYour goal is to produce a final canonical design_spec.md fully aligned to the TravelPlanner user requirements and the adaptive Web Contract after the two debate rounds.\n\nTask Details:\n- Carefully read user_task_description, final design_debate_a.md, and final design_debate_b.md\n- Compare every route, method, template, and element ID across both final debater artifacts\n- Validate complete coverage of all pages and local text data files as per user requirements\n- Resolve any conflicts by strictly adhering to user specifications and preserving exact route paths, HTTP methods, template file names, and element IDs\n- Compile a consistent, authoritative design_spec.md without introducing new requirements or deviations\n\n**Section 1: Routes and Methods**\n- Verify root '/' route renders or redirects to Dashboard page exactly\n- Confirm all declared routes, methods, and form actions are specified verbatim\n\n**Section 2: Template Filenames and HTML Elements**\n- Include all template filenames and exact HTML element IDs per page including dynamic ID patterns\n- Ensure navigation button targets and page titles are exactly aligned\n\n**Section 3: Data File Formats and Persistence**\n- Synthesize precise data file names, formats, field orders, delimiters, and example data from both candidates\n- Confirm local text file data persistence matches user description exactly\n\nCRITICAL SUCCESS CRITERIA:\n- Output a comprehensive, exact design_spec.md suitable for implementation directly from this canonical design\n- Use write_text_file tool to save design_spec.md\n- Ensure all user requirements are met with perfect data integrity, no omitted elements or routes, and no added properties\n\nOutput: design_spec.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_debate_a.md\", \"source\": \"DesignDebaterA\"},\n                {\"type\": \"text_file\", \"name\": \"design_debate_b.md\", \"source\": \"DesignDebaterB\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"DesignDebaterA\",\n            \"reviewer_agent\": \"DesignJudge\",\n            \"review_criteria\": \"Approve if design_debate_a.md exists, is complete, non-empty, readable, aligned with user requirements, and has no formatting errors.\",\n            \"review_artifacts\": [{\"type\": \"text_file\", \"name\": \"design_debate_a.md\"}]\n        },\n        {\n            \"source_agent\": \"DesignDebaterB\",\n            \"reviewer_agent\": \"DesignJudge\",\n            \"review_criteria\": \"Approve if design_debate_b.md exists, is complete, non-empty, readable, aligned with user requirements, and has no formatting errors.\",\n            \"review_artifacts\": [{\"type\": \"text_file\", \"name\": \"design_debate_b.md\"}]\n        },\n        {\n            \"source_agent\": \"DesignJudge\",\n            \"reviewer_agent\": \"DesignDebaterA\",\n            \"review_criteria\": \"Approve if design_spec.md exists, is non-empty, broadly usable, well-structured, and sufficient for implementation without minor omissions.\",\n            \"review_artifacts\": [{\"type\": \"text_file\", \"name\": \"design_spec.md\"}]\n        }\n    ]\n): pass",
    "phase2": "def implementation_and_verification_phase(\n    goal: str = \"Debate complete implementation bundles of app.py and templates/*.html for the TravelPlanner Flask application with exact adaptive web contract compliance and local text data management, then finalize canonical artifacts.\",\n    collab_pattern_name: str = \"Multi-Agent Debate\",\n    collab_pattern_description: str = (\n        \"ImplementationDebaterA and ImplementationDebaterB independently create complete app.py source and all required HTML templates in separate directories in round 1, \"\n        \"revise once from peer artifacts in round 2, and ImplementationJudge adjudicates and combines them into canonical app.py and templates/*.html.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"ImplementationDebaterA\",\n            \"prompt\": \"\"\"You are a Backend Web Developer specializing in Flask applications with local text file data management.\n\nYour goal is to implement a complete Flask backend along with all frontend HTML templates, strictly following the adaptive Web interface contract and the design_spec.md reference, producing full application bundles independently and then revising with peer feedback.\n\nTask Details:\n- Read design_spec.md and both your own and peer's app.py and templates artifact sets for each round.\n- Independently draft entire app_debate_a.py and all templates_debate_a/*.html in round 1.\n- Revise app_debate_a.py and templates_debate_a/*.html after peer-informed round 2 incorporating supported corrections.\n- Output exact element IDs, page titles, route paths, HTTP methods, form actions, and local text file data handling per design_spec.md.\n- Ensure the root route (/) renders or redirects to the Dashboard page without authentication.\n- Preserve local text file read/write consistency with declared data file formats and names.\n\n**Implementation Requirements: Backend (app.py)**\n- Use Flask framework routes and views.\n- Implement data handling using local text files under 'data' directory with correct parsing and updates.\n- Implement all declared pages and routes with exact context variables.\n- Maintain precise HTTP methods and form action URLs.\n- Handle data validation and error conditions gracefully.\n\n**Implementation Requirements: Frontend Templates**\n- Create all HTML templates under templates_debate_a/ with exact filenames and element IDs as specified.\n- Templates must include the declared distinct elements like div IDs, input names, button IDs, dropdowns referencing design_spec.md exactly.\n- Navigation buttons trigger Flask routes as declared.\n- Include form fields with declared names and methods enforcing contract.\n\n**Coding and Collaboration**\n- Use 'write_text_file' tool to save all source files.\n- Use 'validate_python_file' tool to ensure syntax and runtime correctness for app_debate_a.py.\n- Retain full completeness and reject unsupported peer additions during revision round.\n\nCRITICAL REQUIREMENTS:\n- MUST write and update app_debate_a.py and templates_debate_a/*.html only.\n- MUST preserve all exact element IDs, routes, methods, and local data format handling.\n- MUST follow the adaptive Web contract preserving '/' as dashboard entry point.\n- Use only declared outputs; do not add refinement markers or extra files.\n\nOutput: app_debate_a.py, templates_debate_a/*.html\"\"\",\n            \"tools\": [\"write_text_file\", \"validate_python_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignJudge\"},\n                {\"type\": \"text_file\", \"name\": \"app_debate_a.py\", \"source\": \"ImplementationDebaterA\"},\n                {\"type\": \"text_file\", \"name\": \"templates_debate_a/*.html\", \"source\": \"ImplementationDebaterA\"},\n                {\"type\": \"text_file\", \"name\": \"app_debate_b.py\", \"source\": \"ImplementationDebaterB\"},\n                {\"type\": \"text_file\", \"name\": \"templates_debate_b/*.html\", \"source\": \"ImplementationDebaterB\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_debate_a.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_debate_a/*.html\"}\n            ]\n        },\n        {\n            \"agent_name\": \"ImplementationDebaterB\",\n            \"prompt\": \"\"\"You are a Backend Web Developer specializing in Flask applications with local text file data management.\n\nYour goal is to independently implement a full Flask backend and related frontend HTML templates based on design_spec.md with adherence to the adaptive Web interface contract, then revise your implementation after peer review.\n\nTask Details:\n- In each round, read the user design_spec.md plus your own and your peer's app.py and templates artifacts.\n- In round 1, author a full app_debate_b.py and templates_debate_b/*.html independently.\n- In round 2, revise app_debate_b.py and templates_debate_b/*.html incorporating peer-informed corrections consistent with design_spec.md.\n- Follow all declared page routes, HTTP methods, form actions, element IDs, navigation, and local text data management exactly.\n- Ensure '/' route serves or redirects to Dashboard page as per web contract.\n- Maintain strict data handling from text files with exact formats given.\n\n**Implementation Requirements: Backend (app.py)**\n- Flask routes for all pages and features with precise context variables.\n- Read and write all text data files under 'data' directory conforming to the provided schemas.\n- Handle all forms with correct POST/GET methods and data validation.\n\n**Implementation Requirements: Frontend Templates**\n- Full HTML templates in templates_debate_b/ directory with exact element IDs, input names, and buttons per design_spec.md.\n- Implement navigation consistent with backend routes and contract.\n- Include buttons and inputs with exact names, IDs, and dropdown options.\n\n**Collaboration and Tool Usage**\n- Use write_text_file tool to save code and templates.\n- Use validate_python_file tool to verify Python source syntax and runtime.\n- Preserve contract validation and no unsupported additions after peer review.\n\nCRITICAL REQUIREMENTS:\n- Output app_debate_b.py and templates_debate_b/*.html with exact contract adherence.\n- Must maintain exact element IDs, route names, and local file data handling.\n- Root '/' must provide dashboard page as entry point without authentication.\n- Produce only declared output artifacts with no extraneous files or feedback.\n\nOutput: app_debate_b.py, templates_debate_b/*.html\"\"\",\n            \"tools\": [\"write_text_file\", \"validate_python_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignJudge\"},\n                {\"type\": \"text_file\", \"name\": \"app_debate_b.py\", \"source\": \"ImplementationDebaterB\"},\n                {\"type\": \"text_file\", \"name\": \"templates_debate_b/*.html\", \"source\": \"ImplementationDebaterB\"},\n                {\"type\": \"text_file\", \"name\": \"app_debate_a.py\", \"source\": \"ImplementationDebaterA\"},\n                {\"type\": \"text_file\", \"name\": \"templates_debate_a/*.html\", \"source\": \"ImplementationDebaterA\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_debate_b.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_debate_b/*.html\"}\n            ]\n        },\n        {\n            \"agent_name\": \"ImplementationJudge\",\n            \"prompt\": \"\"\"You are a Senior Backend Web Developer and Code Reviewer specializing in Flask applications with local text file data management and UI contract compliance.\n\nYour goal is to evaluate and merge two complete implementations of the TravelPlanner Flask application, selecting and producing one canonical app.py and set of templates/*.html that conform fully to design_spec.md and the adaptive Web contract.\n\nTask Details:\n- Read design_spec.md plus final versions of app_debate_a.py, app_debate_b.py, templates_debate_a/*.html, and templates_debate_b/*.html.\n- Compare both implementations feature-by-feature, route-by-route, and template-by-template for exact contract adherence.\n- Verify all routes, HTTP methods, template usages, and context variables match design_spec.md precisely.\n- Ensure exactly one root route '/' serves or redirects to Dashboard page without authentication.\n- Check all element IDs, dynamic IDs, input names, and button IDs in templates for exact compliance.\n- Validate local data file reads and writes strictly follow declared formats.\n- Use validate_python_file tool to confirm syntax and runtime of candidate app.py files.\n- Produce merged canonical app.py and templates/*.html, choosing best contract-conforming parts from both debates.\n- Output complete, ready-to-deploy Flask backend and template files with no additions beyond authoritative inputs.\n\n**Review Criteria**\n- Syntax correctness and runtime pass of canonical app.py.\n- Precise adaptive Web contract compliance for routing and front-end elements.\n- Local text file data handling consistent with provided formats.\n- No unsupported features or missing essential routes or data handling.\n- Preserved root route '/' as Dashboard entry with no authentication.\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to output canonical app.py and templates/*.html.\n- Validate the final app.py with validate_python_file for syntax and runtime.\n- Deliver only the declared canonical artifacts.\n- Do not add new requirements or refinement markers.\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\", \"validate_python_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignJudge\"},\n                {\"type\": \"text_file\", \"name\": \"app_debate_a.py\", \"source\": \"ImplementationDebaterA\"},\n                {\"type\": \"text_file\", \"name\": \"templates_debate_a/*.html\", \"source\": \"ImplementationDebaterA\"},\n                {\"type\": \"text_file\", \"name\": \"app_debate_b.py\", \"source\": \"ImplementationDebaterB\"},\n                {\"type\": \"text_file\", \"name\": \"templates_debate_b/*.html\", \"source\": \"ImplementationDebaterB\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"ImplementationDebaterA\",\n            \"reviewer_agent\": \"ImplementationJudge\",\n            \"review_criteria\": \"Approve if app_debate_a.py and templates_debate_a/*.html exist, are syntactically correct, readable, relevant to design_spec.md, and without critical errors.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_debate_a.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_debate_a/*.html\"}\n            ]\n        },\n        {\n            \"source_agent\": \"ImplementationDebaterB\",\n            \"reviewer_agent\": \"ImplementationJudge\",\n            \"review_criteria\": \"Approve if app_debate_b.py and templates_debate_b/*.html exist, are syntactically correct, readable, relevant to design_spec.md, and without critical errors.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_debate_b.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_debate_b/*.html\"}\n            ]\n        },\n        {\n            \"source_agent\": \"ImplementationJudge\",\n            \"reviewer_agent\": \"ImplementationDebaterA\",\n            \"review_criteria\": \"Approve if app.py and templates/*.html exist as canonical deliverables, are readable, well-structured, and suitable for deployment with no blocking issues.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ]\n): pass",
}

user_task = """
# Requirements Document for 'TravelPlanner' Web Application

## 1. Objective
Develop a comprehensive web application named 'TravelPlanner' using Python, with data managed through local text files. The application enables users to browse destinations, plan itineraries, search accommodations, book flights, view travel packages, and manage trip details. No authentication required - all features are directly accessible. Note that the website should start from the Dashboard page.

## 2. Language
The required development language for the 'TravelPlanner' application is Python.

## 3. Page Design

The 'TravelPlanner' web application will consist of the following ten pages:

### 1. Dashboard Page
- **Page Title**: Travel Planner Dashboard
- **Overview**: The main hub displaying featured destinations, upcoming trips, and quick navigation to all functionalities.
- **Elements**:
  - **ID: dashboard-page** - Type: Div - Container for the dashboard page.
  - **ID: featured-destinations** - Type: Div - Display of featured travel destinations.
  - **ID: upcoming-trips** - Type: Div - Display of upcoming planned trips.
  - **ID: browse-destinations-button** - Type: Button - Button to navigate to destinations page.
  - **ID: plan-itinerary-button** - Type: Button - Button to navigate to itinerary planning page.

### 2. Destinations Page
- **Page Title**: Travel Destinations
- **Overview**: A page displaying all available travel destinations with search and filter capabilities.
- **Elements**:
  - **ID: destinations-page** - Type: Div - Container for the destinations page.
  - **ID: search-destination** - Type: Input - Field to search destinations by name or country.
  - **ID: region-filter** - Type: Dropdown - Dropdown to filter by region (Asia, Europe, Americas, Africa, Oceania).
  - **ID: destinations-grid** - Type: Div - Grid displaying destination cards with image, name, and country.
  - **ID: view-destination-button-{dest_id}** - Type: Button - Button to view destination details (each destination card has this).

### 3. Destination Details Page
- **Page Title**: Destination Details
- **Overview**: A page displaying detailed information about a specific destination.
- **Elements**:
  - **ID: destination-details-page** - Type: Div - Container for the destination details page.
  - **ID: destination-name** - Type: H1 - Display destination name.
  - **ID: destination-country** - Type: Div - Display destination country.
  - **ID: destination-description** - Type: Div - Display detailed description of the destination.
  - **ID: add-to-trip-button** - Type: Button - Button to add destination to trip.
  - **ID: destination-attractions** - Type: Div - Section displaying main attractions and activities.

### 4. Itinerary Planning Page
- **Page Title**: Plan Your Itinerary
- **Overview**: A page for users to create and manage travel itineraries with activities and schedules.
- **Elements**:
  - **ID: itinerary-page** - Type: Div - Container for the itinerary page.
  - **ID: itinerary-name-input** - Type: Input - Field to enter itinerary name.
  - **ID: start-date-input** - Type: Input (date) - Field to select trip start date.
  - **ID: end-date-input** - Type: Input (date) - Field to select trip end date.
  - **ID: add-activity-button** - Type: Button - Button to add activity to itinerary.
  - **ID: itinerary-list** - Type: Div - Display list of created itineraries with edit/delete options.

### 5. Accommodations Page
- **Page Title**: Search Accommodations
- **Overview**: A page for searching and browsing hotel options with filters and pricing.
- **Elements**:
  - **ID: accommodations-page** - Type: Div - Container for the accommodations page.
  - **ID: destination-input** - Type: Input - Field to enter destination city for hotels.
  - **ID: check-in-date** - Type: Input (date) - Field to select check-in date.
  - **ID: check-out-date** - Type: Input (date) - Field to select check-out date.
  - **ID: price-filter** - Type: Dropdown - Dropdown to filter hotels by price range (Budget, Mid-range, Luxury).
  - **ID: hotels-list** - Type: Div - List of available hotels with name, rating, price, and amenities.

### 6. Transportation Page
- **Page Title**: Book Flights
- **Overview**: A page for searching and booking flights with departure and arrival options.
- **Elements**:
  - **ID: transportation-page** - Type: Div - Container for the transportation page.
  - **ID: departure-city** - Type: Input - Field to enter departure city.
  - **ID: arrival-city** - Type: Input - Field to enter arrival city.
  - **ID: departure-date** - Type: Input (date) - Field to select departure date.
  - **ID: flight-class-filter** - Type: Dropdown - Dropdown to filter by flight class (Economy, Business, First Class).
  - **ID: available-flights** - Type: Div - List of available flights with airlines, times, and prices.

### 7. Travel Packages Page
- **Page Title**: Travel Packages
- **Overview**: A page displaying pre-designed travel packages with complete trip information.
- **Elements**:
  - **ID: packages-page** - Type: Div - Container for the packages page.
  - **ID: packages-grid** - Type: Div - Grid displaying travel package cards with destination, duration, and price.
  - **ID: duration-filter** - Type: Dropdown - Dropdown to filter packages by duration (3-5 days, 7-10 days, 14+ days).
  - **ID: view-package-details-button-{pkg_id}** - Type: Button - Button to view package details (each package has this).
  - **ID: book-package-button-{pkg_id}** - Type: Button - Button to book selected package (each package has this).

### 8. Trip Management Page
- **Page Title**: My Trips
- **Overview**: A page displaying all created trips with options to view, edit, or delete them.
- **Elements**:
  - **ID: trips-page** - Type: Div - Container for the trips page.
  - **ID: trips-table** - Type: Table - Table displaying all trips with destination, dates, and status.
  - **ID: view-trip-details-button-{trip_id}** - Type: Button - Button to view trip details (each trip has this).
  - **ID: edit-trip-button-{trip_id}** - Type: Button - Button to edit trip (each trip has this).
  - **ID: delete-trip-button-{trip_id}** - Type: Button - Button to delete trip (each trip has this).

### 9. Booking Confirmation Page
- **Page Title**: Booking Confirmation
- **Overview**: A page displaying booking confirmation details with reservation information.
- **Elements**:
  - **ID: confirmation-page** - Type: Div - Container for the confirmation page.
  - **ID: confirmation-number** - Type: Div - Display confirmation/booking number.
  - **ID: booking-details** - Type: Div - Display detailed booking information (dates, amounts, locations).
  - **ID: download-itinerary-button** - Type: Button - Button to download trip itinerary as PDF.
  - **ID: share-trip-button** - Type: Button - Button to share trip details.
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 10. Travel Recommendations Page
- **Page Title**: Travel Recommendations
- **Overview**: A page displaying personalized travel recommendations and trending destinations.
- **Elements**:
  - **ID: recommendations-page** - Type: Div - Container for the recommendations page.
  - **ID: trending-destinations** - Type: Div - Display trending destinations ranked by popularity.
  - **ID: recommendation-season-filter** - Type: Dropdown - Dropdown to filter by travel season (Spring, Summer, Fall, Winter).
  - **ID: budget-filter** - Type: Dropdown - Dropdown to filter by budget range (Low, Medium, High).
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

## 4. Data Storage

The 'TravelPlanner' application will store data locally in text files organized in the directory 'data'. The following data formats and examples are defined:

### 1. Destinations Data
- **File Name**: `destinations.txt`
- **Data Format**:
  ```
  dest_id|name|country|region|description|attractions|climate
  ```
- **Example Data**:
  ```
  1|Paris|France|Europe|City of lights and romance with world-class museums|Eiffel Tower, Louvre Museum, Notre-Dame|Temperate
  2|Tokyo|Japan|Asia|Modern metropolis blending tradition and innovation|Senso-ji Temple, Shibuya Crossing, Meiji Shrine|Temperate
  3|Rio de Janeiro|Brazil|Americas|Vibrant beach city with iconic landmarks|Christ the Redeemer, Copacabana Beach, Sugarloaf Mountain|Tropical
  ```

### 2. Itineraries Data
- **File Name**: `itineraries.txt`
- **Data Format**:
  ```
  itinerary_id|itinerary_name|destination|start_date|end_date|activities|status
  ```
- **Example Data**:
  ```
  1|Paris Spring Break|Paris|2025-03-20|2025-03-27|Museum tours, River cruise, Cafe hopping|Planned
  2|Tokyo Adventure|Tokyo|2025-05-01|2025-05-14|Temple visits, Anime district tour, Cooking class|In Progress
  3|Rio Beach Trip|Rio de Janeiro|2025-07-15|2025-07-22|Beach days, Hiking, Night clubs|Planned
  ```

### 3. Hotels Data
- **File Name**: `hotels.txt`
- **Data Format**:
  ```
  hotel_id|name|city|rating|price_per_night|amenities|category
  ```
- **Example Data**:
  ```
  1|Ritz Paris|Paris|5.0|450.00|WiFi, Spa, Restaurant, Pool|Luxury
  2|Hotel Shibuya|Tokyo|4.5|120.00|WiFi, Cafe, Business Center|Mid-range
  3|Copacabana Beach Hotel|Rio de Janeiro|4.0|95.00|Beach access, Restaurant, WiFi|Mid-range
  ```

### 4. Flights Data
- **File Name**: `flights.txt`
- **Data Format**:
  ```
  flight_id|airline|departure_city|arrival_city|departure_time|arrival_time|price|class_type|duration
  ```
- **Example Data**:
  ```
  1|Air France|New York|Paris|10:00|22:30|850.00|Economy|7 hours 30 minutes
  2|JAL|Los Angeles|Tokyo|14:30|15:20 next day|920.00|Business|11 hours 50 minutes
  3|Latam|Miami|Rio de Janeiro|18:00|23:45|380.00|Economy|5 hours 45 minutes
  ```

### 5. Travel Packages Data
- **File Name**: `packages.txt`
- **Data Format**:
  ```
  package_id|package_name|destination|duration_days|price|included_items|difficulty_level
  ```
- **Example Data**:
  ```
  1|Paris Classic Tour|Paris|5|1500.00|Hotel, Flights, Guided tours, Meals|Easy
  2|Tokyo Experience|Tokyo|10|2200.00|Hotel, Flights, Activities, Cultural events|Moderate
  3|Rio Adventure|Rio de Janeiro|7|1800.00|Hotel, Flights, Beach activities, Mountain hiking|Moderate
  ```

### 6. Trips Data
- **File Name**: `trips.txt`
- **Data Format**:
  ```
  trip_id|trip_name|destination|start_date|end_date|total_budget|status|created_date
  ```
- **Example Data**:
  ```
  1|Summer Vacation 2025|Paris|2025-06-01|2025-06-15|3000.00|Booked|2025-01-10
  2|Winter Holiday|Tokyo|2025-12-15|2025-12-30|4500.00|Planned|2025-01-11
  3|Beach Getaway|Rio de Janeiro|2025-07-01|2025-07-08|2000.00|Pending|2025-01-12
  ```

### 7. Bookings Data
- **File Name**: `bookings.txt`
- **Data Format**:
  ```
  booking_id|trip_id|booking_type|booking_date|amount|confirmation_number|status
  ```
- **Example Data**:
  ```
  1|1|Hotel|2025-01-10|750.00|CONF001|Confirmed
  2|2|Flight|2025-01-11|1840.00|CONF002|Confirmed
  3|3|Package|2025-01-12|1800.00|CONF003|Pending
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
    "DesignDebaterA": {
        "prompt": (
            """You are a System Architect specializing in Flask web application design specifications.

Your goal is to create and revise a complete design_spec.md for the TravelPlanner web app through exactly two debate rounds.

Task Details:
- Read the entire user_task_description in every round for design context
- In round 1, independently draft design_debate_a.md covering Flask route mappings, HTTP methods, template files, and exact element IDs for all TravelPlanner pages
- In round 2, revise design_debate_a.md by reading the input design_debate_a.md and peer design_debate_b.md, integrating valid peer improvements or rebuttals
- Output a complete, implementation-ready design_debate_a.md after each round

**Section 1: Flask Routes and HTTP Methods**
- Specify each route path exactly as in the User Task
- Define the HTTP methods allowed (GET, POST, etc.) with correct forms and actions
- Explicitly mark the route for root '/' as entry rendering Dashboard page

**Section 2: Template Files and HTML Elements**
- List precise template filenames per page
- Define all element IDs including dynamic IDs exactly as declared (e.g., view-destination-button-{dest_id})
- Describe page titles and navigation button routes

**Section 3: Data Storage File Formats**
- Specify all local text file names and exact data formats with field order, delimiters, and example rows
- Do not invent data files beyond user specification

CRITICAL SUCCESS CRITERIA:
- Must strictly preserve all user-declared routes, methods, template names, and element IDs
- Produce a design document fully consistent with user requirements and peer feedback after round 2
- Use write_text_file tool to output design_debate_a.md

Output: design_debate_a.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_debate_a.md', 'source': 'DesignDebaterA'}, {'type': 'text_file', 'name': 'design_debate_b.md', 'source': 'DesignDebaterB'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_debate_a.md'}],

    },

    "DesignDebaterB": {
        "prompt": (
            """You are a Software Architect specializing in Flask web application design specifications.

Your goal is to produce and refine a comprehensive design_spec.md for the TravelPlanner app in exactly two debate rounds.

Task Details:
- Thoroughly review user_task_description in every round to understand the app workflow
- Independently write design_debate_b.md in round 1 focusing on route definitions, data persistence behavior, template filenames, and exact HTML element IDs for all pages
- In round 2, read the round 1 artifact and the peer's final design_debate_a.md, revising your design_debate_b.md to address peer points supported by user requirements
- Overwrite and submit the complete design_debate_b.md after each round

**Section 1: Route and URL Structure**
- Define exact route paths and navigation targets, including root '/' redirecting or rendering Dashboard page
- Specify HTTP methods and form action attributes exactly as required

**Section 2: Template and HTML Element Details**
- Provide exact template filenames as used in the application
- Enumerate all HTML element IDs including dynamic patterns like view-package-details-button-{pkg_id}
- Maintain exact consistency of element IDs and navigation button targets

**Section 3: Local Text Data Persistence**
- Define all data files used with exact file names and delineate their content schema with fields and delimiters
- Describe the reading and writing behavior tied to each data file without adding unsupported files

CRITICAL SUCCESS CRITERIA:
- Preserve all user-specified exact routes, methods, templates, and element IDs without deviation
- Produce a clear, consistent, and complete design after two rounds integrating pertinent peer corrections
- Use write_text_file tool to save output as design_debate_b.md

Output: design_debate_b.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_debate_b.md', 'source': 'DesignDebaterB'}, {'type': 'text_file', 'name': 'design_debate_a.md', 'source': 'DesignDebaterA'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_debate_b.md'}],

    },

    "DesignJudge": {
        "prompt": (
            """You are a Senior System Architect adjudicating two competing design specifications for a Flask web application.

Your goal is to produce a final canonical design_spec.md fully aligned to the TravelPlanner user requirements and the adaptive Web Contract after the two debate rounds.

Task Details:
- Carefully read user_task_description, final design_debate_a.md, and final design_debate_b.md
- Compare every route, method, template, and element ID across both final debater artifacts
- Validate complete coverage of all pages and local text data files as per user requirements
- Resolve any conflicts by strictly adhering to user specifications and preserving exact route paths, HTTP methods, template file names, and element IDs
- Compile a consistent, authoritative design_spec.md without introducing new requirements or deviations

**Section 1: Routes and Methods**
- Verify root '/' route renders or redirects to Dashboard page exactly
- Confirm all declared routes, methods, and form actions are specified verbatim

**Section 2: Template Filenames and HTML Elements**
- Include all template filenames and exact HTML element IDs per page including dynamic ID patterns
- Ensure navigation button targets and page titles are exactly aligned

**Section 3: Data File Formats and Persistence**
- Synthesize precise data file names, formats, field orders, delimiters, and example data from both candidates
- Confirm local text file data persistence matches user description exactly

CRITICAL SUCCESS CRITERIA:
- Output a comprehensive, exact design_spec.md suitable for implementation directly from this canonical design
- Use write_text_file tool to save design_spec.md
- Ensure all user requirements are met with perfect data integrity, no omitted elements or routes, and no added properties

Output: design_spec.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_debate_a.md', 'source': 'DesignDebaterA'}, {'type': 'text_file', 'name': 'design_debate_b.md', 'source': 'DesignDebaterB'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_spec.md'}],

    },

    "ImplementationDebaterA": {
        "prompt": (
            """You are a Backend Web Developer specializing in Flask applications with local text file data management.

Your goal is to implement a complete Flask backend along with all frontend HTML templates, strictly following the adaptive Web interface contract and the design_spec.md reference, producing full application bundles independently and then revising with peer feedback.

Task Details:
- Read design_spec.md and both your own and peer's app.py and templates artifact sets for each round.
- Independently draft entire app_debate_a.py and all templates_debate_a/*.html in round 1.
- Revise app_debate_a.py and templates_debate_a/*.html after peer-informed round 2 incorporating supported corrections.
- Output exact element IDs, page titles, route paths, HTTP methods, form actions, and local text file data handling per design_spec.md.
- Ensure the root route (/) renders or redirects to the Dashboard page without authentication.
- Preserve local text file read/write consistency with declared data file formats and names.

**Implementation Requirements: Backend (app.py)**
- Use Flask framework routes and views.
- Implement data handling using local text files under 'data' directory with correct parsing and updates.
- Implement all declared pages and routes with exact context variables.
- Maintain precise HTTP methods and form action URLs.
- Handle data validation and error conditions gracefully.

**Implementation Requirements: Frontend Templates**
- Create all HTML templates under templates_debate_a/ with exact filenames and element IDs as specified.
- Templates must include the declared distinct elements like div IDs, input names, button IDs, dropdowns referencing design_spec.md exactly.
- Navigation buttons trigger Flask routes as declared.
- Include form fields with declared names and methods enforcing contract.

**Coding and Collaboration**
- Use 'write_text_file' tool to save all source files.
- Use 'validate_python_file' tool to ensure syntax and runtime correctness for app_debate_a.py.
- Retain full completeness and reject unsupported peer additions during revision round.

CRITICAL REQUIREMENTS:
- MUST write and update app_debate_a.py and templates_debate_a/*.html only.
- MUST preserve all exact element IDs, routes, methods, and local data format handling.
- MUST follow the adaptive Web contract preserving '/' as dashboard entry point.
- Use only declared outputs; do not add refinement markers or extra files.

Output: app_debate_a.py, templates_debate_a/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file', 'validate_python_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignJudge'}, {'type': 'text_file', 'name': 'app_debate_a.py', 'source': 'ImplementationDebaterA'}, {'type': 'text_file', 'name': 'templates_debate_a/*.html', 'source': 'ImplementationDebaterA'}, {'type': 'text_file', 'name': 'app_debate_b.py', 'source': 'ImplementationDebaterB'}, {'type': 'text_file', 'name': 'templates_debate_b/*.html', 'source': 'ImplementationDebaterB'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app_debate_a.py'}, {'type': 'text_file', 'name': 'templates_debate_a/*.html'}],

    },

    "ImplementationDebaterB": {
        "prompt": (
            """You are a Backend Web Developer specializing in Flask applications with local text file data management.

Your goal is to independently implement a full Flask backend and related frontend HTML templates based on design_spec.md with adherence to the adaptive Web interface contract, then revise your implementation after peer review.

Task Details:
- In each round, read the user design_spec.md plus your own and your peer's app.py and templates artifacts.
- In round 1, author a full app_debate_b.py and templates_debate_b/*.html independently.
- In round 2, revise app_debate_b.py and templates_debate_b/*.html incorporating peer-informed corrections consistent with design_spec.md.
- Follow all declared page routes, HTTP methods, form actions, element IDs, navigation, and local text data management exactly.
- Ensure '/' route serves or redirects to Dashboard page as per web contract.
- Maintain strict data handling from text files with exact formats given.

**Implementation Requirements: Backend (app.py)**
- Flask routes for all pages and features with precise context variables.
- Read and write all text data files under 'data' directory conforming to the provided schemas.
- Handle all forms with correct POST/GET methods and data validation.

**Implementation Requirements: Frontend Templates**
- Full HTML templates in templates_debate_b/ directory with exact element IDs, input names, and buttons per design_spec.md.
- Implement navigation consistent with backend routes and contract.
- Include buttons and inputs with exact names, IDs, and dropdown options.

**Collaboration and Tool Usage**
- Use write_text_file tool to save code and templates.
- Use validate_python_file tool to verify Python source syntax and runtime.
- Preserve contract validation and no unsupported additions after peer review.

CRITICAL REQUIREMENTS:
- Output app_debate_b.py and templates_debate_b/*.html with exact contract adherence.
- Must maintain exact element IDs, route names, and local file data handling.
- Root '/' must provide dashboard page as entry point without authentication.
- Produce only declared output artifacts with no extraneous files or feedback.

Output: app_debate_b.py, templates_debate_b/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file', 'validate_python_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignJudge'}, {'type': 'text_file', 'name': 'app_debate_b.py', 'source': 'ImplementationDebaterB'}, {'type': 'text_file', 'name': 'templates_debate_b/*.html', 'source': 'ImplementationDebaterB'}, {'type': 'text_file', 'name': 'app_debate_a.py', 'source': 'ImplementationDebaterA'}, {'type': 'text_file', 'name': 'templates_debate_a/*.html', 'source': 'ImplementationDebaterA'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app_debate_b.py'}, {'type': 'text_file', 'name': 'templates_debate_b/*.html'}],

    },

    "ImplementationJudge": {
        "prompt": (
            """You are a Senior Backend Web Developer and Code Reviewer specializing in Flask applications with local text file data management and UI contract compliance.

Your goal is to evaluate and merge two complete implementations of the TravelPlanner Flask application, selecting and producing one canonical app.py and set of templates/*.html that conform fully to design_spec.md and the adaptive Web contract.

Task Details:
- Read design_spec.md plus final versions of app_debate_a.py, app_debate_b.py, templates_debate_a/*.html, and templates_debate_b/*.html.
- Compare both implementations feature-by-feature, route-by-route, and template-by-template for exact contract adherence.
- Verify all routes, HTTP methods, template usages, and context variables match design_spec.md precisely.
- Ensure exactly one root route '/' serves or redirects to Dashboard page without authentication.
- Check all element IDs, dynamic IDs, input names, and button IDs in templates for exact compliance.
- Validate local data file reads and writes strictly follow declared formats.
- Use validate_python_file tool to confirm syntax and runtime of candidate app.py files.
- Produce merged canonical app.py and templates/*.html, choosing best contract-conforming parts from both debates.
- Output complete, ready-to-deploy Flask backend and template files with no additions beyond authoritative inputs.

**Review Criteria**
- Syntax correctness and runtime pass of canonical app.py.
- Precise adaptive Web contract compliance for routing and front-end elements.
- Local text file data handling consistent with provided formats.
- No unsupported features or missing essential routes or data handling.
- Preserved root route '/' as Dashboard entry with no authentication.

CRITICAL REQUIREMENTS:
- Use write_text_file tool to output canonical app.py and templates/*.html.
- Validate the final app.py with validate_python_file for syntax and runtime.
- Deliver only the declared canonical artifacts.
- Do not add new requirements or refinement markers.

Output: app.py, templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file', 'validate_python_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignJudge'}, {'type': 'text_file', 'name': 'app_debate_a.py', 'source': 'ImplementationDebaterA'}, {'type': 'text_file', 'name': 'templates_debate_a/*.html', 'source': 'ImplementationDebaterA'}, {'type': 'text_file', 'name': 'app_debate_b.py', 'source': 'ImplementationDebaterB'}, {'type': 'text_file', 'name': 'templates_debate_b/*.html', 'source': 'ImplementationDebaterB'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}],

    }

}

REVIEW_PROFILES = {
    'DesignDebaterA': [
        ("DesignJudge", """Approve if design_debate_a.md exists, is complete, non-empty, readable, aligned with user requirements, and has no formatting errors.""", [{'type': 'text_file', 'name': 'design_debate_a.md'}])
    ],

    'DesignDebaterB': [
        ("DesignJudge", """Approve if design_debate_b.md exists, is complete, non-empty, readable, aligned with user requirements, and has no formatting errors.""", [{'type': 'text_file', 'name': 'design_debate_b.md'}])
    ],

    'DesignJudge': [
        ("DesignDebaterA", """Approve if design_spec.md exists, is non-empty, broadly usable, well-structured, and sufficient for implementation without minor omissions.""", [{'type': 'text_file', 'name': 'design_spec.md'}])
    ],

    'ImplementationDebaterA': [
        ("ImplementationJudge", """Approve if app_debate_a.py and templates_debate_a/*.html exist, are syntactically correct, readable, relevant to design_spec.md, and without critical errors.""", [{'type': 'text_file', 'name': 'app_debate_a.py'}, {'type': 'text_file', 'name': 'templates_debate_a/*.html'}])
    ],

    'ImplementationDebaterB': [
        ("ImplementationJudge", """Approve if app_debate_b.py and templates_debate_b/*.html exist, are syntactically correct, readable, relevant to design_spec.md, and without critical errors.""", [{'type': 'text_file', 'name': 'app_debate_b.py'}, {'type': 'text_file', 'name': 'templates_debate_b/*.html'}])
    ],

    'ImplementationJudge': [
        ("ImplementationDebaterA", """Approve if app.py and templates/*.html exist as canonical deliverables, are readable, well-structured, and suitable for deployment with no blocking issues.""", [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}])
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
    DesignDebaterA = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="DesignDebaterA",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=2,
        timeout_threshold=300,
        failure_threshold=1,
        recovery_time=30
    )
    DesignDebaterB = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="DesignDebaterB",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=2,
        timeout_threshold=300,
        failure_threshold=1,
        recovery_time=30
    )
    DesignJudge = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="DesignJudge",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=2,
        timeout_threshold=350,
        failure_threshold=1,
        recovery_time=30
    )

    # Multi-Agent Debate: exactly 2 total rounds (1=initial, 2=one peer-informed revision)
    for round_num in range(1, 3):
        design_a, design_b = "", ""
        if round_num > 1:
            try:
                design_a = open("design_debate_a.md", "r", encoding="utf-8").read()
            except OSError:
                design_a = ""
            try:
                design_b = open("design_debate_b.md", "r", encoding="utf-8").read()
            except OSError:
                design_b = ""

        if round_num == 1:
            msg_a = "(No peer design yet - initial draft based solely on user_task_description.)"
            msg_b = "(No peer design yet - initial draft based solely on user_task_description.)"
        else:
            msg_a = f"Peer DesignDebaterB's draft:\n{design_b}"
            msg_b = f"Peer DesignDebaterA's draft:\n{design_a}"

        await asyncio.gather(
            execute(DesignDebaterA, msg_a),
            execute(DesignDebaterB, msg_b)
        )

    # After 2 rounds, adjudicate final design_spec.md
    try:
        final_a = open("design_debate_a.md", "r", encoding="utf-8").read()
    except OSError:
        final_a = ""
    try:
        final_b = open("design_debate_b.md", "r", encoding="utf-8").read()
    except OSError:
        final_b = ""

    await execute(
        DesignJudge,
        "Adjudicate and synthesize the final design_spec.md using user_task_description and the two final candidate drafts.\n\n"
        "=== DesignDebaterA Final ===\n" + final_a + "\n\n"
        "=== DesignDebaterB Final ===\n" + final_b
    )
# Phase1_End
# Phase2_Start

async def implementation_and_verification_phase():
    import glob

    ImplementationDebaterA = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="ImplementationDebaterA",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=2,
        timeout_threshold=500,
        failure_threshold=1,
        recovery_time=40
    )
    ImplementationDebaterB = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="ImplementationDebaterB",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=2,
        timeout_threshold=500,
        failure_threshold=1,
        recovery_time=40
    )
    ImplementationJudge = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="ImplementationJudge",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=2,
        timeout_threshold=500,
        failure_threshold=1,
        recovery_time=40
    )

    # Multi-Agent Debate: exactly 2 total rounds
    for round_num in range(1, 3):
        # Read all current relevant artifacts for this round
        app_a = ""
        app_b = ""
        templates_a = ""
        templates_b = ""

        try:
            app_a = open("app_debate_a.py", "r", encoding="utf-8").read()
        except OSError:
            pass
        try:
            app_b = open("app_debate_b.py", "r", encoding="utf-8").read()
        except OSError:
            pass

        for path in sorted(glob.glob("templates_debate_a/*.html")):
            try:
                templates_a += f"\n=== {path} ===\n" + open(path, "r", encoding="utf-8").read()
            except OSError:
                pass
        for path in sorted(glob.glob("templates_debate_b/*.html")):
            try:
                templates_b += f"\n=== {path} ===\n" + open(path, "r", encoding="utf-8").read()
            except OSError:
                pass

        # Prepare messages for ImplementationDebaterA and ImplementationDebaterB
        if round_num == 1:
            msg_a = "Round 1 of 2: independently draft complete app_debate_a.py and all templates_debate_a/*.html based on design_spec.md without peer input."
            msg_b = "Round 1 of 2: independently draft complete app_debate_b.py and all templates_debate_b/*.html based on design_spec.md without peer input."
        else:
            msg_a = (
                "Round 2 of 2: revise app_debate_a.py and templates_debate_a/*.html incorporating peer revisions.\n\n"
                "=== Peer app_debate_b.py ===\n" + app_b + "\n\n"
                "=== Peer templates_debate_b/*.html ===" + templates_b
            )
            msg_b = (
                "Round 2 of 2: revise app_debate_b.py and templates_debate_b/*.html incorporating peer revisions.\n\n"
                "=== Peer app_debate_a.py ===\n" + app_a + "\n\n"
                "=== Peer templates_debate_a/*.html ===" + templates_a
            )

        # Run both debaters in parallel
        await asyncio.gather(
            execute(ImplementationDebaterA, msg_a),
            execute(ImplementationDebaterB, msg_b)
        )

    # After round 2, read final candidates for judge evaluation
    app_a = ""
    app_b = ""
    templates_a = ""
    templates_b = ""

    try:
        app_a = open("app_debate_a.py", "r", encoding="utf-8").read()
    except OSError:
        pass
    try:
        app_b = open("app_debate_b.py", "r", encoding="utf-8").read()
    except OSError:
        pass

    for path in sorted(glob.glob("templates_debate_a/*.html")):
        try:
            templates_a += f"\n=== {path} ===\n" + open(path, "r", encoding="utf-8").read()
        except OSError:
            pass
    for path in sorted(glob.glob("templates_debate_b/*.html")):
        try:
            templates_b += f"\n=== {path} ===\n" + open(path, "r", encoding="utf-8").read()
        except OSError:
            pass

    # Judge evaluates and merges final implementations
    await execute(
        ImplementationJudge,
        "Adjudicate the two final round-2 app and template bundles, and write canonical app.py and templates/*.html.\n\n"
        "=== Candidate A: app_debate_a.py ===\n" + app_a + "\n\n"
        "=== Candidate A: templates_debate_a/*.html ===" + templates_a + "\n\n"
        "=== Candidate B: app_debate_b.py ===\n" + app_b + "\n\n"
        "=== Candidate B: templates_debate_b/*.html ===" + templates_b
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
