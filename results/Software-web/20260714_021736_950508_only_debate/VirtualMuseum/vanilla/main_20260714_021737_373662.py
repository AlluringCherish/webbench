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
# 20260714_021737_373662/main_20260714_021737_373662.py

# Phase_info dictionary containing complete def blocks for failover context
Phase_info = {
    "phase1": "def design_specification_phase(\n    goal: str = \"Debate the detailed design specification for the 'VirtualMuseum' Flask web application respecting all user requirements and produce a complete design_spec.md\",\n    collab_pattern_name: str = \"Multi-Agent Debate\",\n    collab_pattern_description: str = (\n        \"DesignDebaterA and DesignDebaterB independently draft design_debate_a.md and design_debate_b.md respectively in round 1, \"\n        \"then each revises their draft once informed by the other's draft in round 2; \"\n        \"DesignJudge then adjudicates both final design drafts and writes the canonical design_spec.md.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"DesignDebaterA\",\n            \"prompt\": \"\"\"You are a Software Architect specializing in Flask web application design and local file data schema specifications.\n\nYour goal is to produce and iteratively improve a comprehensive design specification document covering all Flask routes, HTML templates with exact element IDs, local text file storage schemas, and navigation flows for a VirtualMuseum web app.\n\nTask Details:\n- Analyze user_task_description fully on every round.\n- In round 1, independently write a complete design_debate_a.md covering:\n  - All Flask routes with exact HTTP methods, paths, templates, context variables.\n  - Detailed HTML template specifications with page titles, element IDs (including dynamic IDs), and navigation target pages.\n  - Local text data management schema for all specified data files with formats and example records.\n- In round 2, refine design_debate_a.md by reviewing design_debate_b.md; accept only corrections or improvements supported by user requirements.\n- Overwrite entire design_debate_a.md each round to maintain a full, consistent design document.\n\n**Section 1: Flask Routes Specification**\n- Specify routes: path, method (GET/POST), template file, context variables and their structures exactly as required.\n- Include correct route for root path `/` rendering/redirecting to Dashboard page as primary entry.\n- Preserve user-declared button element IDs and their route navigation.\n\n**Section 2: HTML Template and Element Mapping**\n- Enumerate templates corresponding to the seven user pages.\n- Detail page titles, all element IDs including dynamic patterns (e.g. `view-exhibition-button-{exhibition_id}`).\n- Define context variables used in templates for dynamic rendering.\n- Specify navigation flows triggered by buttons, preserving exact element IDs.\n\n**Section 3: Local Text File Data Schemas**\n- Define each data file name and directory `data/`.\n- Specify exact pipe-delimited field orders as given; include field descriptions and example rows.\n- Cover all data files: users.txt, galleries.txt, exhibitions.txt, artifacts.txt, audioguides.txt, tickets.txt, events.txt, event_registrations.txt, collection_logs.txt.\n\nCRITICAL SUCCESS CRITERIA:\n- Deliver a ready-to-implement, precise design document adhering strictly to user requirements.\n- Ensure all page IDs, routes, method actions, and data schemas match authoritative user specs.\n- Use write_text_file tool to save output to design_debate_a.md.\n- Output only the declared artifact.\n\nOutput: design_debate_a.md\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_debate_a.md\", \"source\": \"DesignDebaterA\"},\n                {\"type\": \"text_file\", \"name\": \"design_debate_b.md\", \"source\": \"DesignDebaterB\"}\n            ],\n            \"output_artifacts\": [{\"type\": \"text_file\", \"name\": \"design_debate_a.md\"}]\n        },\n        {\n            \"agent_name\": \"DesignDebaterB\",\n            \"prompt\": \"\"\"You are a Software Architect specializing in Flask web application design and local text file data management.\n\nYour goal is to create and iteratively improve a detailed design specification document specifying Flask routes, templates with exact HTML element IDs, local text data storage schemas and navigation flows for a VirtualMuseum web app.\n\nTask Details:\n- Review user_task_description carefully each round.\n- In round 1, independently write a full design_debate_b.md covering:\n  - Precise web routes: URLs, HTTP methods, template filenames, and context variables exactly matching user requirements.\n  - Template page titles, all exact element IDs including dynamic patterns.\n  - Navigation buttons matching declared element IDs directing to correct routes.\n  - All local text data files stored in `data/`, with exact pipe-delimited fields, semantics, and examples.\n- In round 2, revise design_debate_b.md after reading design_debate_a.md; incorporate improvements only supported by user specifications.\n- Overwrite design_debate_b.md fully every round, maintaining a complete design.\n\n**Section 1: Flask Routes Specification**\n- Define all routes with correct methods and template rendering or redirecting behavior.\n- Ensure root path `/` is the main entry rendering or redirecting to the Dashboard page per user mandate.\n- Preserve all button element IDs and route actions strictly.\n\n**Section 2: HTML Templates and Dynamic Elements**\n- Include all seven pages with correct page titles.\n- List all HTML element IDs including dynamic IDs with bracketed variables.\n- Define context variables passed into templates.\n- Specify button navigations respecting user-stated IDs.\n\n**Section 3: Data Storage Schemas**\n- Document all text files in `data/` directory.\n- Provide field structure with pipe `|` delimiter, field order, and sample entries.\n- Cover all files: users.txt, galleries.txt, exhibitions.txt, artifacts.txt, audioguides.txt, tickets.txt, events.txt, event_registrations.txt, collection_logs.txt.\n\nCRITICAL SUCCESS CRITERIA:\n- Provide an implementation-ready design spec faithful to user inputs.\n- Strictly conserve all declared fields, IDs, routes, and data formats.\n- Use write_text_file tool to save final output to design_debate_b.md.\n- Output only the declared artifact.\n\nOutput: design_debate_b.md\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_debate_b.md\", \"source\": \"DesignDebaterB\"},\n                {\"type\": \"text_file\", \"name\": \"design_debate_a.md\", \"source\": \"DesignDebaterA\"}\n            ],\n            \"output_artifacts\": [{\"type\": \"text_file\", \"name\": \"design_debate_b.md\"}]\n        },\n        {\n            \"agent_name\": \"DesignJudge\",\n            \"prompt\": \"\"\"You are a Senior Software Architect responsible for adjudicating two competing Flask web app design specifications for VirtualMuseum.\n\nYour goal is to synthesize and produce a canonical, fully compliant design_spec.md document that consolidates all Flask routes, HTML templates with exact element IDs (including dynamic IDs), local text file data schemas in pipe-delimited format, and navigation rules per user requirements.\n\nTask Details:\n- Read user_task_description, final design_debate_a.md and design_debate_b.md after round 2.\n- Compare routes, templates, element IDs, data schemas, and navigation flows line-by-line.\n- Resolve discrepancies prioritizing strict adherence to user requirements.\n- Write one complete, consistent design_spec.md replacing both drafts.\n\n**Section 1: Flask Routes and Entry Points**\n- Confirm the `/` root route renders or redirects to the Dashboard page as per user spec.\n- List all routes, methods, templates, and context variable structures exactly.\n- Enforce button ID references remain constant and match route targets.\n\n**Section 2: HTML Templates**\n- Provide definitive page titles and complete element ID lists including dynamic element ID patterns.\n- Verify context variable usage.\n- Confirm navigation button routes and element IDs.\n\n**Section 3: Local Text File Schemas**\n- Authoritatively specify all `data/` text files.\n- Provide exact pipe-delimited field orders, field descriptions, and example records matching user input.\n\nCRITICAL SUCCESS CRITERIA:\n- Output comprehensive design_spec.md usable by backend and frontend developers.\n- No requirements beyond user's original specification.\n- Use write_text_file tool to save output to design_spec.md.\n- Output only the declared artifact.\n\nOutput: design_spec.md\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_debate_a.md\", \"source\": \"DesignDebaterA\"},\n                {\"type\": \"text_file\", \"name\": \"design_debate_b.md\", \"source\": \"DesignDebaterB\"}\n            ],\n            \"output_artifacts\": [{\"type\": \"text_file\", \"name\": \"design_spec.md\"}]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"DesignDebaterA\",\n            \"reviewer_agent\": \"DesignJudge\",\n            \"review_criteria\": (\n                \"Approve if design_debate_a.md exists, is non-empty, well-structured, relevant to the user requirements, \"\n                \"and free from catastrophic format or logical errors; completeness at this stage not mandatory.\"\n            ),\n            \"review_artifacts\": [{\"type\": \"text_file\", \"name\": \"design_debate_a.md\"}]\n        },\n        {\n            \"source_agent\": \"DesignDebaterB\",\n            \"reviewer_agent\": \"DesignJudge\",\n            \"review_criteria\": (\n                \"Approve if design_debate_b.md exists, is non-empty, well-structured, relevant to the user requirements, \"\n                \"and free from catastrophic format or logical errors; completeness at this stage not mandatory.\"\n            ),\n            \"review_artifacts\": [{\"type\": \"text_file\", \"name\": \"design_debate_b.md\"}]\n        },\n        {\n            \"source_agent\": \"DesignJudge\",\n            \"reviewer_agent\": \"DesignDebaterA\",\n            \"review_criteria\": (\n                \"Approve when design_spec.md exists, is non-empty, readable, broadly usable, \"\n                \"and captures all required design elements without feature additions.\"\n            ),\n            \"review_artifacts\": [{\"type\": \"text_file\", \"name\": \"design_spec.md\"}]\n        }\n    ]\n): pass",
    "phase2": "def implementation_and_verification_phase(\n    goal: str = \"Debate two full implementations of the VirtualMuseum Flask app including app.py and templates/*.html for two total rounds, then adjudicate the final canonical implementation\",\n    collab_pattern_name: str = \"Multi-Agent Debate\",\n    collab_pattern_description: str = (\n        \"ImplementationDebaterA and ImplementationDebaterB independently develop full candidate app.py and corresponding templates/*.html \"\n        \"based on design_spec.md in round 1, then revise once informed by peer artifacts in round 2; ImplementationJudge adjudicates \"\n        \"both bundles and produces the final app.py and templates/*.html set.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"ImplementationDebaterA\",\n            \"prompt\": \"\"\"You are a Python Flask Developer specializing in full-stack web application implementation using local text file persistence.\n\nYour goal is to implement and revise a complete VirtualMuseum Flask application covering all specified pages, routes, templates, exact HTML element IDs, and pipe-delimited local text file data management as described in a design specification.\n\nTask Details:\n- Read design_spec.md and all provided peer and own round candidate artifacts as input context\n- In round 1, independently produce a complete app_debate_a.py and templates_debate_a/*.html matching design_spec.md\n- In round 2, revise your app_debate_a.py and templates_debate_a/*.html incorporating only supported peer corrections from ImplementationDebaterB’s artifacts\n- Focus strictly on the Flask app module and HTML templates; implement all routes, page flows, and local text file CRUD operations with pipe delimiter\n\n**Section 1: Flask Application Implementation**\n- Implement app.py routes exactly as specified: use exact route paths, HTTP methods, and render templates preserving element IDs\n- Load and save data to local text files under a 'data' directory with pipe-delimited fields matching specification\n- Support user authentication state, public dashboard entry at '/', and precise navigation between pages\n\n**Section 2: HTML Template Implementation**\n- Implement templates/*.html with exact page titles and all declared element IDs including dynamic IDs (e.g., buttons with {exhibition_id})\n- Keep UI element types and IDs consistent with design_spec.md for each page: dashboard, artifact catalog, exhibitions, exhibition details, visitor tickets, virtual events, audio guides\n- Include navigation elements that link correctly using Flask route URLs as per design\n\n**Section 3: Revision and Collaboration Guidelines**\n- On round 2, compare own and peer implementations to identify missing or incorrect features supported by design_spec.md\n- Update your implementation to fix faults, improve compliance, and enhance completeness without adding unsupported functionality\n\nCRITICAL SUCCESS CRITERIA:\n- MUST use write_text_file tool to save app_debate_a.py and all templates_debate_a/*.html files\n- Output must include all application source and template files declared exactly with prescribed filenames\n- Persist application state strictly using local pipe-delimited text files as specified\n- Implement '/' route to serve or redirect to Dashboard page as authoritative entry\n\nOutput: app_debate_a.py, templates_debate_a/*.html\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignJudge\"},\n                {\"type\": \"text_file\", \"name\": \"app_debate_a.py\", \"source\": \"ImplementationDebaterA\"},\n                {\"type\": \"text_file\", \"name\": \"templates_debate_a/*.html\", \"source\": \"ImplementationDebaterA\"},\n                {\"type\": \"text_file\", \"name\": \"app_debate_b.py\", \"source\": \"ImplementationDebaterB\"},\n                {\"type\": \"text_file\", \"name\": \"templates_debate_b/*.html\", \"source\": \"ImplementationDebaterB\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_debate_a.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_debate_a/*.html\"}\n            ]\n        },\n        {\n            \"agent_name\": \"ImplementationDebaterB\",\n            \"prompt\": \"\"\"You are a Python Flask Developer specializing in robust full-stack web applications with local pipe-delimited text file persistence.\n\nYour goal is to independently implement and revise a full VirtualMuseum Flask application comprising all required routes, HTML templates with exact element IDs, and local data handling as defined in the authoritative design_spec.md.\n\nTask Details:\n- Read design_spec.md and all relevant own and peer candidate artifacts as context\n- In round 1, independently create app_debate_b.py and templates_debate_b/*.html implementing all specified pages and flows\n- In round 2, update app_debate_b.py and templates_debate_b/*.html guided by differences vs. ImplementationDebaterA’s artifacts and design_spec.md\n- Focus on complete correctness per spec including '/' entry routing and precise HTML IDs including dynamic buttons and controls\n\n**Section 1: Flask Application Responsibilities**\n- Implement every route with exact HTTP methods and render or redirect to templates with declared titles and element IDs\n- Manage all data reading and writing to local files using pipe-delimited format inside a 'data' folder\n- Preserve authentication logic and maintain navigation consistency complying with the design spec expectations\n\n**Section 2: HTML Template Responsibilities**\n- Produce the full set of templates/*.html with correct page titles, container div IDs, buttons, input IDs, tables, and dynamic ID patterns\n- Ensure navigation between pages functions via proper href or form actions as specified\n- Maintain element ID and navigation consistency especially for buttons corresponding to dynamic entities\n\n**Section 3: Round 2 Revision Protocol**\n- Review peer candidate artifacts and design_spec.md thoroughly\n- Revise own candidate to fix any deviations, missing elements, or inconsistencies supported by authoritative inputs\n- Avoid adding any unsupported features or routes not declared in design_spec.md\n\nCRITICAL SUCCESS CRITERIA:\n- MUST use write_text_file tool to write app_debate_b.py and all templates_debate_b/*.html files\n- Deliver a functioning Flask app source and template set strictly conforming to design_spec.md and local data storage patterns\n- Implement '/' route as the main entry rendering or redirecting to Dashboard page\n- Preserve all local file IO with pipe-delimited formatting as specified\n\nOutput: app_debate_b.py, templates_debate_b/*.html\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignJudge\"},\n                {\"type\": \"text_file\", \"name\": \"app_debate_b.py\", \"source\": \"ImplementationDebaterB\"},\n                {\"type\": \"text_file\", \"name\": \"templates_debate_b/*.html\", \"source\": \"ImplementationDebaterB\"},\n                {\"type\": \"text_file\", \"name\": \"app_debate_a.py\", \"source\": \"ImplementationDebaterA\"},\n                {\"type\": \"text_file\", \"name\": \"templates_debate_a/*.html\", \"source\": \"ImplementationDebaterA\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_debate_b.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_debate_b/*.html\"}\n            ]\n        },\n        {\n            \"agent_name\": \"ImplementationJudge\",\n            \"prompt\": \"\"\"You are a Lead Python Flask Developer and Code Reviewer specializing in authoritative adjudication of complete web application implementations.\n\nYour goal is to evaluate and merge final implementation candidates from ImplementationDebaterA and ImplementationDebaterB, producing one canonical, fully compliant VirtualMuseum Flask app.py and matching templates/*.html set.\n\nTask Details:\n- Read design_spec.md, and both final debate candidate implementations app_debate_a.py, templates_debate_a/*.html and app_debate_b.py, templates_debate_b/*.html\n- Compare implementations for completeness, correctness, and strict adherence to the design_spec.md including route definitions, template element IDs, and local file data management\n- Resolve disagreements by selecting best-supported code and template elements consistent with the authoritative design specification\n- Integrate chosen elements into one final canonical app.py and templates/*.html ensemble with no additional features or deviations\n\n**Section 1: Flask Application Evaluation and Merging**\n- Verify all declared routes, methods, and handlers exist and respect '/' as the dashboard entry point\n- Confirm all read/write operations use local pipe-delimited text files under 'data/' per spec\n- Evaluate code quality, syntax validity, and logical correctness aligned with design_spec.md\n\n**Section 2: HTML Template Evaluation and Merging**\n- Ensure templates/*.html have exact page titles, all required container divs, buttons, inputs, tables with exact element IDs including dynamic IDs\n- Verify navigation between pages aligns with route endpoints and no missing or extraneous UI elements are present\n\n**Section 3: Final Artifact Production**\n- Compose one canonical app.py source module and all templates/*.html in correct directories\n- Make sure the canonical output is readable, usable, and strictly compliant with design_spec.md requirements without introducing new content\n\nCRITICAL SUCCESS CRITERIA:\n- MUST use write_text_file tool to save final app.py and all templates/*.html files\n- Deliver a complete, consistent Flask app fully aligned with design_spec.md\n- Output must be error-free, ready to run, and maintain all local text file persistence contracts\n- Strictly preserve '/' main entry behavior to load or redirect to Dashboard page\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignJudge\"},\n                {\"type\": \"text_file\", \"name\": \"app_debate_a.py\", \"source\": \"ImplementationDebaterA\"},\n                {\"type\": \"text_file\", \"name\": \"templates_debate_a/*.html\", \"source\": \"ImplementationDebaterA\"},\n                {\"type\": \"text_file\", \"name\": \"app_debate_b.py\", \"source\": \"ImplementationDebaterB\"},\n                {\"type\": \"text_file\", \"name\": \"templates_debate_b/*.html\", \"source\": \"ImplementationDebaterB\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"ImplementationDebaterA\",\n            \"reviewer_agent\": \"ImplementationJudge\",\n            \"review_criteria\": (\n                \"Approve when app_debate_a.py and associated templates exist, are syntactically valid, meet design_spec.md requirements, \"\n                \"and exhibit no catastrophic format or logical errors.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_debate_a.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_debate_a/*.html\"}\n            ]\n        },\n        {\n            \"source_agent\": \"ImplementationDebaterB\",\n            \"reviewer_agent\": \"ImplementationJudge\",\n            \"review_criteria\": (\n                \"Approve when app_debate_b.py and associated templates exist, are syntactically valid, meet design_spec.md requirements, \"\n                \"and exhibit no catastrophic format or logical errors.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_debate_b.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_debate_b/*.html\"}\n            ]\n        },\n        {\n            \"source_agent\": \"ImplementationJudge\",\n            \"reviewer_agent\": \"ImplementationDebaterA\",\n            \"review_criteria\": (\n                \"Approve when the canonical app.py and templates/*.html exist, are non-empty, readable, usable, and strictly adhere to design_spec.md.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ]\n): pass",
}

user_task = """
# Requirements Document for 'VirtualMuseum' Web Application

## 1. Objective
Develop a comprehensive web application named 'VirtualMuseum' using Python, with data managed through local text files. The application enables museums to manage virtual exhibitions, curate artifact collections, provide audio guides, sell visitor tickets, and host virtual events. Note that the website should start from the Dashboard page.

## 2. Language
The required development language for the 'VirtualMuseum' application is Python.

## 3. Page Design

The 'VirtualMuseum' web application will consist of the following seven pages:

### 1. Dashboard Page
- **Page Title**: Museum Dashboard
- **Overview**: The main hub displaying overview of exhibitions, artifacts, and navigation to all functionalities.
- **Elements**:
  - **ID: dashboard-page** - Type: Div - Container for the dashboard page.
  - **ID: exhibition-summary** - Type: Div - Summary showing total exhibitions, active exhibitions count.
  - **ID: artifact-catalog-button** - Type: Button - Button to navigate to artifact catalog page.
  - **ID: exhibitions-button** - Type: Button - Button to navigate to exhibitions page.
  - **ID: visitor-tickets-button** - Type: Button - Button to navigate to visitor tickets page.
  - **ID: virtual-events-button** - Type: Button - Button to navigate to virtual events page.
  - **ID: audio-guides-button** - Type: Button - Button to navigate to audio guides page.

### 2. Artifact Catalog Page
- **Page Title**: Artifact Catalog
- **Overview**: A page displaying all artifacts with search and filter capabilities.
- **Elements**:
  - **ID: artifact-catalog-page** - Type: Div - Container for the artifact catalog page.
  - **ID: artifact-table** - Type: Table - Table displaying artifacts with ID, name, period, origin, exhibition, and actions.
  - **ID: search-artifact** - Type: Input - Field to search artifacts by name or ID.
  - **ID: apply-artifact-filter** - Type: Button - Button to apply filters.
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 3. Exhibitions Page
- **Page Title**: Exhibitions
- **Overview**: A page displaying all exhibitions with details and status.
- **Elements**:
  - **ID: exhibitions-page** - Type: Div - Container for the exhibitions page.
  - **ID: exhibition-list** - Type: Table - Table displaying all exhibitions with title, type, dates, gallery, and status.
  - **ID: filter-exhibition-type** - Type: Dropdown - Dropdown to filter by exhibition type (Permanent, Temporary, Virtual).
  - **ID: apply-exhibition-filter** - Type: Button - Button to apply exhibition filter.
  - **ID: view-exhibition-button-{exhibition_id}** - Type: Button - Button to view exhibition details (each row has this button).
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 4. Exhibition Details Page
- **Page Title**: Exhibition Details
- **Overview**: A detailed view of a specific exhibition with its artifacts.
- **Elements**:
  - **ID: exhibition-details-page** - Type: Div - Container for the exhibition details page.
  - **ID: exhibition-title** - Type: H1 - Title of the exhibition.
  - **ID: exhibition-description** - Type: Div - Description of the exhibition.
  - **ID: exhibition-dates** - Type: Div - Start and end dates of the exhibition.
  - **ID: exhibition-artifacts** - Type: Table - Table displaying artifacts in this exhibition.
  - **ID: back-to-exhibitions** - Type: Button - Button to navigate back to exhibitions list.

### 5. Visitor Tickets Page
- **Page Title**: Visitor Tickets
- **Overview**: A page for visitors to purchase tickets and view ticket sales.
- **Elements**:
  - **ID: visitor-tickets-page** - Type: Div - Container for the visitor tickets page.
  - **ID: ticket-type** - Type: Dropdown - Dropdown to select ticket type (Standard, Student, Senior, Family, VIP).
  - **ID: number-of-tickets** - Type: Input (number) - Field to input number of tickets.
  - **ID: purchase-ticket-button** - Type: Button - Button to purchase tickets.
  - **ID: my-tickets-table** - Type: Table - Table displaying user's purchased tickets.
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 6. Virtual Events Page
- **Page Title**: Virtual Events
- **Overview**: A page to view and manage virtual museum events like webinars and artist talks.
- **Elements**:
  - **ID: virtual-events-page** - Type: Div - Container for the virtual events page.
  - **ID: event-list** - Type: Table - Table displaying all events with title, date, time, type, and registration status.
  - **ID: register-event-button-{event_id}** - Type: Button - Button to register for an event (each row has this button).
  - **ID: cancel-registration-button-{registration_id}** - Type: Button - Button to cancel registration (each row has this button).
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 7. Audio Guides Page
- **Page Title**: Audio Guides
- **Overview**: A page to browse and access audio guides for exhibits.
- **Elements**:
  - **ID: audio-guides-page** - Type: Div - Container for the audio guides page.
  - **ID: audio-guide-list** - Type: Table - Table displaying all audio guides with exhibit number, title, language, and duration.
  - **ID: filter-language** - Type: Dropdown - Dropdown to filter by language (English, Spanish, French).
  - **ID: apply-language-filter** - Type: Button - Button to apply language filter.
  - **ID: play-guide-button-{guide_id}** - Type: Button - Button to play audio guide (each row has this button).
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

## 4. Data Storage

The 'VirtualMuseum' application will store data locally in text files organized in the directory 'data'. The following data formats and examples are defined:

### 1. User Authentication Data
- **File Name**: `users.txt`
- **Data Format**:
  ```
  username
  ```
- **Example Data**:
  ```
  curator_john
  visitor_mary
  curator_sarah
  ```

### 2. Gallery Data
- **File Name**: `galleries.txt`
- **Data Format**:
  ```
  gallery_id|gallery_name|floor|capacity|theme|status
  ```
- **Example Data**:
  ```
  1|Ancient Civilizations Hall|1|50|Ancient|Open
  2|Modern Art Wing|2|30|Modern|Open
  3|Science Discovery Center|3|40|Science|Renovation
  ```

### 3. Exhibition Data
- **File Name**: `exhibitions.txt`
- **Data Format**:
  ```
  exhibition_id|title|description|gallery_id|exhibition_type|start_date|end_date|curator_name|created_by
  ```
- **Example Data**:
  ```
  1|Egyptian Treasures|Ancient artifacts from Egypt|1|Permanent|2024-01-01|2025-12-31|Dr. Smith|curator_john
  2|Pop Art Revolution|Contemporary pop art collection|2|Temporary|2024-11-01|2024-12-31|Lisa Chen|curator_sarah
  3|Virtual Space Exploration|Online space exhibition|2|Virtual|2024-10-01|2025-03-31|Mark Johnson|curator_john
  ```

### 4. Artifact Data
- **File Name**: `artifacts.txt`
- **Data Format**:
  ```
  artifact_id|artifact_name|period|origin|description|exhibition_id|storage_location|acquisition_date|added_by
  ```
- **Example Data**:
  ```
  1|Golden Mask of Tutankhamun|Ancient|Egypt|Famous golden funeral mask|1|A-101|2020-05-15|curator_john
  2|Warhol Soup Cans|Contemporary|USA|Iconic pop art piece|2|B-205|2023-08-20|curator_sarah
  3|Roman Amphora|Ancient|Italy|Ancient storage vessel|1|A-103|2019-11-10|curator_john
  ```

### 5. Audio Guide Data
- **File Name**: `audioguides.txt`
- **Data Format**:
  ```
  guide_id|exhibit_number|title|language|duration|script|narrator|created_by
  ```
- **Example Data**:
  ```
  1|101|Introduction to Egyptian Art|English|5|Welcome to the Egyptian exhibition...|James Brown|curator_john
  2|101|Introducción al Arte Egipcio|Spanish|5|Bienvenido a la exhibición egipcia...|Maria Garcia|curator_john
  3|205|Pop Art Explained|English|7|Pop art emerged in the 1950s...|Sarah Williams|curator_sarah
  ```

### 6. Ticket Data
- **File Name**: `tickets.txt`
- **Data Format**:
  ```
  ticket_id|username|ticket_type|visit_date|visit_time|number_of_tickets|price|visitor_name|visitor_email|purchase_date
  ```
- **Example Data**:
  ```
  1|visitor_mary|Standard|2024-11-25|11:00 AM|2|30|Mary Johnson|mary@email.com|2024-11-20
  2|visitor_mary|VIP|2024-12-01|1:00 PM|1|50|Mary Johnson|mary@email.com|2024-11-20
  3|visitor_tom|Student|2024-11-22|9:00 AM|1|10|Tom Lee|tom@email.com|2024-11-18
  ```

### 7. Virtual Event Data
- **File Name**: `events.txt`
- **Data Format**:
  ```
  event_id|title|date|time|event_type|speaker|capacity|description|created_by
  ```
- **Example Data**:
  ```
  1|Ancient Egypt Webinar|2024-12-05|2:00 PM|Webinar|Dr. Smith|100|Deep dive into Egyptian culture|curator_john
  2|Meet the Artist: Pop Art|2024-11-30|6:00 PM|Artist Talk|Andy Williams|50|Discussion with contemporary artist|curator_sarah
  3|Virtual Museum Tour|2024-12-10|10:00 AM|Virtual Tour|Lisa Chen|200|Guided tour of entire museum|curator_john
  ```

### 8. Event Registration Data
- **File Name**: `event_registrations.txt`
- **Data Format**:
  ```
  registration_id|event_id|username|registration_date
  ```
- **Example Data**:
  ```
  1|1|visitor_mary|2024-11-20
  2|2|visitor_mary|2024-11-21
  3|1|visitor_tom|2024-11-19
  ```

### 9. Collection Log Data
- **File Name**: `collection_logs.txt`
- **Data Format**:
  ```
  log_id|artifact_id|activity_type|date|notes|condition|curator
  ```
- **Example Data**:
  ```
  1|1|Inspection|2024-11-15|Routine quarterly inspection|Excellent|curator_john
  2|1|Cleaning|2024-11-16|Professional cleaning performed|Excellent|curator_john
  3|2|Photography|2024-10-20|High-resolution images taken|Good|curator_sarah
  4|3|Restoration|2024-09-10|Minor crack repair completed|Good|curator_john
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
    "DesignDebaterA": {
        "prompt": (
            """You are a Software Architect specializing in Flask web application design and local file data schema specifications.

Your goal is to produce and iteratively improve a comprehensive design specification document covering all Flask routes, HTML templates with exact element IDs, local text file storage schemas, and navigation flows for a VirtualMuseum web app.

Task Details:
- Analyze user_task_description fully on every round.
- In round 1, independently write a complete design_debate_a.md covering:
  - All Flask routes with exact HTTP methods, paths, templates, context variables.
  - Detailed HTML template specifications with page titles, element IDs (including dynamic IDs), and navigation target pages.
  - Local text data management schema for all specified data files with formats and example records.
- In round 2, refine design_debate_a.md by reviewing design_debate_b.md; accept only corrections or improvements supported by user requirements.
- Overwrite entire design_debate_a.md each round to maintain a full, consistent design document.

**Section 1: Flask Routes Specification**
- Specify routes: path, method (GET/POST), template file, context variables and their structures exactly as required.
- Include correct route for root path `/` rendering/redirecting to Dashboard page as primary entry.
- Preserve user-declared button element IDs and their route navigation.

**Section 2: HTML Template and Element Mapping**
- Enumerate templates corresponding to the seven user pages.
- Detail page titles, all element IDs including dynamic patterns (e.g. `view-exhibition-button-{exhibition_id}`).
- Define context variables used in templates for dynamic rendering.
- Specify navigation flows triggered by buttons, preserving exact element IDs.

**Section 3: Local Text File Data Schemas**
- Define each data file name and directory `data/`.
- Specify exact pipe-delimited field orders as given; include field descriptions and example rows.
- Cover all data files: users.txt, galleries.txt, exhibitions.txt, artifacts.txt, audioguides.txt, tickets.txt, events.txt, event_registrations.txt, collection_logs.txt.

CRITICAL SUCCESS CRITERIA:
- Deliver a ready-to-implement, precise design document adhering strictly to user requirements.
- Ensure all page IDs, routes, method actions, and data schemas match authoritative user specs.
- Use write_text_file tool to save output to design_debate_a.md.
- Output only the declared artifact.

Output: design_debate_a.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_debate_a.md', 'source': 'DesignDebaterA'}, {'type': 'text_file', 'name': 'design_debate_b.md', 'source': 'DesignDebaterB'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_debate_a.md'}],

    },

    "DesignDebaterB": {
        "prompt": (
            """You are a Software Architect specializing in Flask web application design and local text file data management.

Your goal is to create and iteratively improve a detailed design specification document specifying Flask routes, templates with exact HTML element IDs, local text data storage schemas and navigation flows for a VirtualMuseum web app.

Task Details:
- Review user_task_description carefully each round.
- In round 1, independently write a full design_debate_b.md covering:
  - Precise web routes: URLs, HTTP methods, template filenames, and context variables exactly matching user requirements.
  - Template page titles, all exact element IDs including dynamic patterns.
  - Navigation buttons matching declared element IDs directing to correct routes.
  - All local text data files stored in `data/`, with exact pipe-delimited fields, semantics, and examples.
- In round 2, revise design_debate_b.md after reading design_debate_a.md; incorporate improvements only supported by user specifications.
- Overwrite design_debate_b.md fully every round, maintaining a complete design.

**Section 1: Flask Routes Specification**
- Define all routes with correct methods and template rendering or redirecting behavior.
- Ensure root path `/` is the main entry rendering or redirecting to the Dashboard page per user mandate.
- Preserve all button element IDs and route actions strictly.

**Section 2: HTML Templates and Dynamic Elements**
- Include all seven pages with correct page titles.
- List all HTML element IDs including dynamic IDs with bracketed variables.
- Define context variables passed into templates.
- Specify button navigations respecting user-stated IDs.

**Section 3: Data Storage Schemas**
- Document all text files in `data/` directory.
- Provide field structure with pipe `|` delimiter, field order, and sample entries.
- Cover all files: users.txt, galleries.txt, exhibitions.txt, artifacts.txt, audioguides.txt, tickets.txt, events.txt, event_registrations.txt, collection_logs.txt.

CRITICAL SUCCESS CRITERIA:
- Provide an implementation-ready design spec faithful to user inputs.
- Strictly conserve all declared fields, IDs, routes, and data formats.
- Use write_text_file tool to save final output to design_debate_b.md.
- Output only the declared artifact.

Output: design_debate_b.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_debate_b.md', 'source': 'DesignDebaterB'}, {'type': 'text_file', 'name': 'design_debate_a.md', 'source': 'DesignDebaterA'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_debate_b.md'}],

    },

    "DesignJudge": {
        "prompt": (
            """You are a Senior Software Architect responsible for adjudicating two competing Flask web app design specifications for VirtualMuseum.

Your goal is to synthesize and produce a canonical, fully compliant design_spec.md document that consolidates all Flask routes, HTML templates with exact element IDs (including dynamic IDs), local text file data schemas in pipe-delimited format, and navigation rules per user requirements.

Task Details:
- Read user_task_description, final design_debate_a.md and design_debate_b.md after round 2.
- Compare routes, templates, element IDs, data schemas, and navigation flows line-by-line.
- Resolve discrepancies prioritizing strict adherence to user requirements.
- Write one complete, consistent design_spec.md replacing both drafts.

**Section 1: Flask Routes and Entry Points**
- Confirm the `/` root route renders or redirects to the Dashboard page as per user spec.
- List all routes, methods, templates, and context variable structures exactly.
- Enforce button ID references remain constant and match route targets.

**Section 2: HTML Templates**
- Provide definitive page titles and complete element ID lists including dynamic element ID patterns.
- Verify context variable usage.
- Confirm navigation button routes and element IDs.

**Section 3: Local Text File Schemas**
- Authoritatively specify all `data/` text files.
- Provide exact pipe-delimited field orders, field descriptions, and example records matching user input.

CRITICAL SUCCESS CRITERIA:
- Output comprehensive design_spec.md usable by backend and frontend developers.
- No requirements beyond user's original specification.
- Use write_text_file tool to save output to design_spec.md.
- Output only the declared artifact.

Output: design_spec.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_debate_a.md', 'source': 'DesignDebaterA'}, {'type': 'text_file', 'name': 'design_debate_b.md', 'source': 'DesignDebaterB'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_spec.md'}],

    },

    "ImplementationDebaterA": {
        "prompt": (
            """You are a Python Flask Developer specializing in full-stack web application implementation using local text file persistence.

Your goal is to implement and revise a complete VirtualMuseum Flask application covering all specified pages, routes, templates, exact HTML element IDs, and pipe-delimited local text file data management as described in a design specification.

Task Details:
- Read design_spec.md and all provided peer and own round candidate artifacts as input context
- In round 1, independently produce a complete app_debate_a.py and templates_debate_a/*.html matching design_spec.md
- In round 2, revise your app_debate_a.py and templates_debate_a/*.html incorporating only supported peer corrections from ImplementationDebaterB’s artifacts
- Focus strictly on the Flask app module and HTML templates; implement all routes, page flows, and local text file CRUD operations with pipe delimiter

**Section 1: Flask Application Implementation**
- Implement app.py routes exactly as specified: use exact route paths, HTTP methods, and render templates preserving element IDs
- Load and save data to local text files under a 'data' directory with pipe-delimited fields matching specification
- Support user authentication state, public dashboard entry at '/', and precise navigation between pages

**Section 2: HTML Template Implementation**
- Implement templates/*.html with exact page titles and all declared element IDs including dynamic IDs (e.g., buttons with {exhibition_id})
- Keep UI element types and IDs consistent with design_spec.md for each page: dashboard, artifact catalog, exhibitions, exhibition details, visitor tickets, virtual events, audio guides
- Include navigation elements that link correctly using Flask route URLs as per design

**Section 3: Revision and Collaboration Guidelines**
- On round 2, compare own and peer implementations to identify missing or incorrect features supported by design_spec.md
- Update your implementation to fix faults, improve compliance, and enhance completeness without adding unsupported functionality

CRITICAL SUCCESS CRITERIA:
- MUST use write_text_file tool to save app_debate_a.py and all templates_debate_a/*.html files
- Output must include all application source and template files declared exactly with prescribed filenames
- Persist application state strictly using local pipe-delimited text files as specified
- Implement '/' route to serve or redirect to Dashboard page as authoritative entry

Output: app_debate_a.py, templates_debate_a/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignJudge'}, {'type': 'text_file', 'name': 'app_debate_a.py', 'source': 'ImplementationDebaterA'}, {'type': 'text_file', 'name': 'templates_debate_a/*.html', 'source': 'ImplementationDebaterA'}, {'type': 'text_file', 'name': 'app_debate_b.py', 'source': 'ImplementationDebaterB'}, {'type': 'text_file', 'name': 'templates_debate_b/*.html', 'source': 'ImplementationDebaterB'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app_debate_a.py'}, {'type': 'text_file', 'name': 'templates_debate_a/*.html'}],

    },

    "ImplementationDebaterB": {
        "prompt": (
            """You are a Python Flask Developer specializing in robust full-stack web applications with local pipe-delimited text file persistence.

Your goal is to independently implement and revise a full VirtualMuseum Flask application comprising all required routes, HTML templates with exact element IDs, and local data handling as defined in the authoritative design_spec.md.

Task Details:
- Read design_spec.md and all relevant own and peer candidate artifacts as context
- In round 1, independently create app_debate_b.py and templates_debate_b/*.html implementing all specified pages and flows
- In round 2, update app_debate_b.py and templates_debate_b/*.html guided by differences vs. ImplementationDebaterA’s artifacts and design_spec.md
- Focus on complete correctness per spec including '/' entry routing and precise HTML IDs including dynamic buttons and controls

**Section 1: Flask Application Responsibilities**
- Implement every route with exact HTTP methods and render or redirect to templates with declared titles and element IDs
- Manage all data reading and writing to local files using pipe-delimited format inside a 'data' folder
- Preserve authentication logic and maintain navigation consistency complying with the design spec expectations

**Section 2: HTML Template Responsibilities**
- Produce the full set of templates/*.html with correct page titles, container div IDs, buttons, input IDs, tables, and dynamic ID patterns
- Ensure navigation between pages functions via proper href or form actions as specified
- Maintain element ID and navigation consistency especially for buttons corresponding to dynamic entities

**Section 3: Round 2 Revision Protocol**
- Review peer candidate artifacts and design_spec.md thoroughly
- Revise own candidate to fix any deviations, missing elements, or inconsistencies supported by authoritative inputs
- Avoid adding any unsupported features or routes not declared in design_spec.md

CRITICAL SUCCESS CRITERIA:
- MUST use write_text_file tool to write app_debate_b.py and all templates_debate_b/*.html files
- Deliver a functioning Flask app source and template set strictly conforming to design_spec.md and local data storage patterns
- Implement '/' route as the main entry rendering or redirecting to Dashboard page
- Preserve all local file IO with pipe-delimited formatting as specified

Output: app_debate_b.py, templates_debate_b/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignJudge'}, {'type': 'text_file', 'name': 'app_debate_b.py', 'source': 'ImplementationDebaterB'}, {'type': 'text_file', 'name': 'templates_debate_b/*.html', 'source': 'ImplementationDebaterB'}, {'type': 'text_file', 'name': 'app_debate_a.py', 'source': 'ImplementationDebaterA'}, {'type': 'text_file', 'name': 'templates_debate_a/*.html', 'source': 'ImplementationDebaterA'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app_debate_b.py'}, {'type': 'text_file', 'name': 'templates_debate_b/*.html'}],

    },

    "ImplementationJudge": {
        "prompt": (
            """You are a Lead Python Flask Developer and Code Reviewer specializing in authoritative adjudication of complete web application implementations.

Your goal is to evaluate and merge final implementation candidates from ImplementationDebaterA and ImplementationDebaterB, producing one canonical, fully compliant VirtualMuseum Flask app.py and matching templates/*.html set.

Task Details:
- Read design_spec.md, and both final debate candidate implementations app_debate_a.py, templates_debate_a/*.html and app_debate_b.py, templates_debate_b/*.html
- Compare implementations for completeness, correctness, and strict adherence to the design_spec.md including route definitions, template element IDs, and local file data management
- Resolve disagreements by selecting best-supported code and template elements consistent with the authoritative design specification
- Integrate chosen elements into one final canonical app.py and templates/*.html ensemble with no additional features or deviations

**Section 1: Flask Application Evaluation and Merging**
- Verify all declared routes, methods, and handlers exist and respect '/' as the dashboard entry point
- Confirm all read/write operations use local pipe-delimited text files under 'data/' per spec
- Evaluate code quality, syntax validity, and logical correctness aligned with design_spec.md

**Section 2: HTML Template Evaluation and Merging**
- Ensure templates/*.html have exact page titles, all required container divs, buttons, inputs, tables with exact element IDs including dynamic IDs
- Verify navigation between pages aligns with route endpoints and no missing or extraneous UI elements are present

**Section 3: Final Artifact Production**
- Compose one canonical app.py source module and all templates/*.html in correct directories
- Make sure the canonical output is readable, usable, and strictly compliant with design_spec.md requirements without introducing new content

CRITICAL SUCCESS CRITERIA:
- MUST use write_text_file tool to save final app.py and all templates/*.html files
- Deliver a complete, consistent Flask app fully aligned with design_spec.md
- Output must be error-free, ready to run, and maintain all local text file persistence contracts
- Strictly preserve '/' main entry behavior to load or redirect to Dashboard page

Output: app.py, templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignJudge'}, {'type': 'text_file', 'name': 'app_debate_a.py', 'source': 'ImplementationDebaterA'}, {'type': 'text_file', 'name': 'templates_debate_a/*.html', 'source': 'ImplementationDebaterA'}, {'type': 'text_file', 'name': 'app_debate_b.py', 'source': 'ImplementationDebaterB'}, {'type': 'text_file', 'name': 'templates_debate_b/*.html', 'source': 'ImplementationDebaterB'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}],

    }

}

REVIEW_PROFILES = {
    'DesignDebaterA': [
        ("DesignJudge", """Approve if design_debate_a.md exists, is non-empty, well-structured, relevant to the user requirements, "
                "and free from catastrophic format or logical errors; completeness at this stage not mandatory.""", [{'type': 'text_file', 'name': 'design_debate_a.md'}])
    ],

    'DesignDebaterB': [
        ("DesignJudge", """Approve if design_debate_b.md exists, is non-empty, well-structured, relevant to the user requirements, "
                "and free from catastrophic format or logical errors; completeness at this stage not mandatory.""", [{'type': 'text_file', 'name': 'design_debate_b.md'}])
    ],

    'DesignJudge': [
        ("DesignDebaterA", """Approve when design_spec.md exists, is non-empty, readable, broadly usable, "
                "and captures all required design elements without feature additions.""", [{'type': 'text_file', 'name': 'design_spec.md'}])
    ],

    'ImplementationDebaterA': [
        ("ImplementationJudge", """Approve when app_debate_a.py and associated templates exist, are syntactically valid, meet design_spec.md requirements, "
                "and exhibit no catastrophic format or logical errors.""", [{'type': 'text_file', 'name': 'app_debate_a.py'}, {'type': 'text_file', 'name': 'templates_debate_a/*.html'}])
    ],

    'ImplementationDebaterB': [
        ("ImplementationJudge", """Approve when app_debate_b.py and associated templates exist, are syntactically valid, meet design_spec.md requirements, "
                "and exhibit no catastrophic format or logical errors.""", [{'type': 'text_file', 'name': 'app_debate_b.py'}, {'type': 'text_file', 'name': 'templates_debate_b/*.html'}])
    ],

    'ImplementationJudge': [
        ("ImplementationDebaterA", """Approve when the canonical app.py and templates/*.html exist, are non-empty, readable, usable, and strictly adhere to design_spec.md.""", [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}])
    ]

}



# Orchestration Functions
async def design_specification_phase():
    DesignDebaterA = build_resilient_agent(
        agent_name="DesignDebaterA",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=2,
        timeout_threshold=350,
        failure_threshold=1,
        recovery_time=40
    )
    DesignDebaterB = build_resilient_agent(
        agent_name="DesignDebaterB",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=2,
        timeout_threshold=350,
        failure_threshold=1,
        recovery_time=40
    )
    DesignJudge = build_resilient_agent(
        agent_name="DesignJudge",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=2,
        timeout_threshold=400,
        failure_threshold=1,
        recovery_time=40
    )

    # Multi-Agent Debate: exactly 2 total rounds (1=initial, 2=one peer-informed revision)
    for round_num in range(1, 3):
        design_a_text = ""
        design_b_text = ""
        if round_num > 1:
            try:
                design_a_text = open("design_debate_a.md", "r", encoding="utf-8").read()
            except OSError:
                design_a_text = ""
            try:
                design_b_text = open("design_debate_b.md", "r", encoding="utf-8").read()
            except OSError:
                design_b_text = ""

        if round_num == 1:
            msg_a = "(No peer draft yet - initial independent draft round 1)"
            msg_b = "(No peer draft yet - initial independent draft round 1)"
        else:
            msg_a = f"Revise your draft after reviewing the peer draft below, incorporating only improvements supported by user requirements.\n\n=== Peer DesignDebaterB draft ===\n{design_b_text}"
            msg_b = f"Revise your draft after reviewing the peer draft below, incorporating only improvements supported by user requirements.\n\n=== Peer DesignDebaterA draft ===\n{design_a_text}"

        await asyncio.gather(
            execute(DesignDebaterA, msg_a),
            execute(DesignDebaterB, msg_b)
        )

    # After round 2, read both final drafts and run the judge to adjudicate canonical design_spec.md
    design_a_final = ""
    design_b_final = ""
    try:
        design_a_final = open("design_debate_a.md", "r", encoding="utf-8").read()
    except OSError:
        design_a_final = ""
    try:
        design_b_final = open("design_debate_b.md", "r", encoding="utf-8").read()
    except OSError:
        design_b_final = ""

    await execute(
        DesignJudge,
        "Adjudicate the two final design drafts and write canonical design_spec.md document.\n\n"
        "=== DesignDebaterA Final Draft ===\n"
        + design_a_final
        + "\n\n=== DesignDebaterB Final Draft ===\n"
        + design_b_final
    )
# Phase1_End
# Phase2_Start

async def implementation_and_verification_phase():
    import glob

    ImplementationDebaterA = build_resilient_agent(
        agent_name="ImplementationDebaterA",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=2,
        timeout_threshold=500,
        failure_threshold=1,
        recovery_time=30,
    )
    ImplementationDebaterB = build_resilient_agent(
        agent_name="ImplementationDebaterB",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=2,
        timeout_threshold=500,
        failure_threshold=1,
        recovery_time=30,
    )
    ImplementationJudge = build_resilient_agent(
        agent_name="ImplementationJudge",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=2,
        timeout_threshold=500,
        failure_threshold=1,
        recovery_time=30,
    )

    # Exactly 2 total debate rounds: round 1 initial, round 2 peer informed revision
    for round_num in range(1, 3):
        app_a_content = ""
        templates_a_content = ""
        app_b_content = ""
        templates_b_content = ""

        # Read latest candidate artifacts if available
        if round_num > 1:
            try:
                with open("app_debate_a.py", "r", encoding="utf-8") as f:
                    app_a_content = f.read()
            except OSError:
                app_a_content = ""
            try:
                template_paths_a = sorted(glob.glob("templates_debate_a/*.html"))
                for path in template_paths_a:
                    try:
                        templates_a_content += f"\n=== {path} ===\n" + open(path, "r", encoding="utf-8").read()
                    except OSError:
                        pass
            except OSError:
                templates_a_content = ""

            try:
                with open("app_debate_b.py", "r", encoding="utf-8") as f:
                    app_b_content = f.read()
            except OSError:
                app_b_content = ""
            try:
                template_paths_b = sorted(glob.glob("templates_debate_b/*.html"))
                for path in template_paths_b:
                    try:
                        templates_b_content += f"\n=== {path} ===\n" + open(path, "r", encoding="utf-8").read()
                    except OSError:
                        pass
            except OSError:
                templates_b_content = ""

        if round_num == 1:
            msg_a = "Round 1 of 2: Independently implement the full app_debate_a.py and templates_debate_a/*.html based on design_spec.md, with no peer info."
            msg_b = "Round 1 of 2: Independently implement the full app_debate_b.py and templates_debate_b/*.html based on design_spec.md, with no peer info."
        else:
            msg_a = (
                "Round 2 of 2: Revise your app_debate_a.py and templates_debate_a/*.html using the peer ImplementationDebaterB artifacts below "
                "and the design_spec.md as authoritative source.\n\n=== Peer app_debate_b.py ===\n"
                + app_b_content
                + "\n\n=== Peer templates_debate_b/*.html ===\n"
                + templates_b_content
            )
            msg_b = (
                "Round 2 of 2: Revise your app_debate_b.py and templates_debate_b/*.html using the peer ImplementationDebaterA artifacts below "
                "and the design_spec.md as authoritative source.\n\n=== Peer app_debate_a.py ===\n"
                + app_a_content
                + "\n\n=== Peer templates_debate_a/*.html ===\n"
                + templates_a_content
            )

        await asyncio.gather(
            execute(ImplementationDebaterA, msg_a),
            execute(ImplementationDebaterB, msg_b),
        )

    # After 2 rounds, read the final candidates for adjudication
    final_app_a = ""
    final_templates_a = ""
    final_app_b = ""
    final_templates_b = ""

    try:
        with open("app_debate_a.py", "r", encoding="utf-8") as f:
            final_app_a = f.read()
    except OSError:
        final_app_a = ""

    try:
        template_paths = sorted(glob.glob("templates_debate_a/*.html"))
        for path in template_paths:
            try:
                final_templates_a += f"\n=== {path} ===\n" + open(path, "r", encoding="utf-8").read()
            except OSError:
                pass
    except OSError:
        final_templates_a = ""

    try:
        with open("app_debate_b.py", "r", encoding="utf-8") as f:
            final_app_b = f.read()
    except OSError:
        final_app_b = ""

    try:
        template_paths = sorted(glob.glob("templates_debate_b/*.html"))
        for path in template_paths:
            try:
                final_templates_b += f"\n=== {path} ===\n" + open(path, "r", encoding="utf-8").read()
            except OSError:
                pass
    except OSError:
        final_templates_b = ""

    # Compose message to ImplementationJudge for final adjudication
    final_msg = (
        "Evaluate and merge the two final full implementation candidates from ImplementationDebaterA and ImplementationDebaterB, producing the final canonical app.py and templates/*.html.\n\n"
        "=== Candidate A: app_debate_a.py ===\n"
        + final_app_a
        + "\n\n=== Candidate A: templates_debate_a/*.html ===\n"
        + final_templates_a
        + "\n\n=== Candidate B: app_debate_b.py ===\n"
        + final_app_b
        + "\n\n=== Candidate B: templates_debate_b/*.html ===\n"
        + final_templates_b
    )

    await execute(ImplementationJudge, final_msg)
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
