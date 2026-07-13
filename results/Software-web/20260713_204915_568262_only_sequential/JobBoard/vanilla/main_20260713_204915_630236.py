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
# 20260713_204915_630236/main_20260713_204915_630236.py

# Phase_info dictionary containing complete def blocks for failover context
Phase_info = {
    "phase1": "def design_specification_phase(\n    goal: str = \"Analyze the 'JobBoard' web application requirements and produce a complete design_spec.md covering pages, routes, UI element IDs, and data models.\",\n    collab_pattern_name: str = \"Sequential Flow\",\n    collab_pattern_description: str = (\n        \"RequirementsAnalyst reads the user task and writes requirements_analysis.md detailing each page, required routes, page titles, UI element IDs, and the data model. \"\n        \"WebArchitect then reads requirements_analysis.md and converts it into design_spec.md with finalized page architecture, route specifications, template mapping, element IDs, and data file contracts.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"RequirementsAnalyst\",\n            \"prompt\": \"\"\"You are a Software Requirements Analyst specializing in web application requirements documentation.\n\nYour goal is to analyze the user-provided task description and produce a comprehensive requirements analysis document that details all pages, page titles, UI element IDs, navigation structure, and data storage requirements for the JobBoard web application.\n\nTask Details:\n- Read user_task_description in full to extract relevant information\n- Identify and document all pages with their exact titles\n- Extract and list all UI element IDs for each page\n- Outline the navigation flow between pages using button/element IDs\n- Summarize data storage requirements including data files, fields, and formats mentioned\n- Output requirements_analysis.md capturing all above information clearly and completely\n\nAnalysis Requirements:\n1. **Pages and Titles**:\n   - List each page in the app with exact title as in the user task\n   - Include key container element IDs per page\n\n2. **UI Element IDs**:\n   - Enumerate all specified UI element IDs for each page accurately\n   - Distinguish between static and dynamic element IDs (with variable placeholders)\n\n3. **Navigation Structure**:\n   - Map navigational buttons or links to target pages by their button IDs\n   - Reflect logical entry points and user flow starting from Dashboard\n\n4. **Data Storage Summary**:\n   - List each data file with its name and described format\n   - Include fields and example data if available\n   - Note relationships or mappings between data files\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to output requirements_analysis.md\n- Ensure completeness and accuracy matching the user task exactly\n- Avoid assumptions beyond the provided user task description\n\nOutput: requirements_analysis.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"requirements_analysis.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"WebArchitect\",\n            \"prompt\": \"\"\"You are a Web Architect specializing in Flask web application design and architecture.\n\nYour goal is to create a detailed design specification that converts the requirements_analysis.md into an explicit architecture document containing Flask route endpoints, HTTP methods, exact page titles, template filenames, UI element IDs, navigation flow, and detailed data file schemas. The design must support user navigation starting at the Dashboard page without requiring authentication.\n\nTask Details:\n- Read requirements_analysis.md and user_task_description fully\n- Define Flask route endpoints with HTTP methods (GET/POST) for all pages and actions\n- Specify exact page titles as per requirements\n- Map each page to a template filename (templates/{page_name}.html or similar)\n- List all UI element IDs as extracted, including dynamic ID patterns\n- Specify navigation flow between pages referencing precise button/link IDs\n- Define detailed data file schemas with file names, exact field order, data formats (pipe-delimited), and example data rows\n- Ensure architecture supports all user task features with no authentication, starting at Dashboard\n\nDesign Requirements:\n1. **Flask Routes**:\n   - Use RESTful GET for pages rendering data\n   - Use POST where form submissions occur (e.g., application form)\n   - Include dynamic parameters for detail pages (e.g., job_id, company_id, app_id where applicable)\n\n2. **Templates and Page Titles**:\n   - Define template filenames tied to pages (snake_case naming recommended)\n   - Include exact page titles matching requirements\n\n3. **UI Element IDs**:\n   - Enumerate all exact element IDs from requirements_analysis.md\n   - Specify format for dynamic IDs with placeholders (e.g., view-job-button-{job_id})\n\n4. **Data File Contracts**:\n   - For each data file, specify path data/{filename}.txt\n   - List fields in exact order pipe-delimited\n   - Describe contents briefly\n   - Provide 2-3 example entries matching user data samples\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save output as design_spec.md\n- Ensure full traceability between requirements_analysis.md and design_spec.md\n- Follow user requirements precisely; no assumptions beyond spec\n- Use consistent naming conventions for routes, templates, UI IDs\n- Support direct navigation from Dashboard with no authentication requirement\n\nOutput: design_spec.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"requirements_analysis.md\", \"source\": \"RequirementsAnalyst\"},\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"RequirementsAnalyst\",\n            \"reviewer_agent\": \"WebArchitect\",\n            \"review_criteria\": \"Verify requirements_analysis.md covers all pages, UI element IDs, and data storage requirements as specified in the user task with no omissions.\",\n            \"review_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\"},\n                {\"type\": \"text_file\", \"name\": \"requirements_analysis.md\"}\n            ]\n        }\n    ]\n): pass",
    "phase2": "def implementation_phase(\n    goal: str = \"Implement the 'JobBoard' web application as a Flask app.py and corresponding templates/*.html files based on design_spec.md and user requirements.\",\n    collab_pattern_name: str = \"Sequential Flow\",\n    collab_pattern_description: str = (\n        \"DraftEngineer develops app_draft.py and draft templates/*.html files implementing all pages, routes, UIs, and data file handling as specified. \"\n        \"IntegrationEngineer then refines and integrates drafts into a final app.py and templates/*.html set that fully comply with the design_spec.md and run as a cohesive Flask web app with dashboard as the start page.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"DraftEngineer\",\n            \"prompt\": \"\"\"You are a Backend and Frontend Developer specializing in Flask web applications with template drafting.\n\nYour goal is to draft a Flask application (app_draft.py) and corresponding HTML template drafts implementing all required pages, UI element IDs, navigation buttons, and data interactions with local text files.\n\nTask Details:\n- Read design_spec.md and user_task_description fully to understand all pages, routes, UIs, and data storage formats.\n- Create app_draft.py implementing Flask routes and handlers covering all pages and features.\n- Draft ALL HTML templates (*.html) for all pages with correct UI element IDs as specified in user requirements.\n- Use render_template calls referencing templates in a 'templates_draft/' directory.\n- Manage local data files for all specified entities (jobs, companies, applications, resumes, categories, job_categories).\n- Focus on implementing page navigation and data loading/presentation as drafts for subsequent refinement.\n- Output app_draft.py and templates draft files under templates_draft/ folder.\n\nFlask Implementation Guidelines:\n1. Define Flask app with standard setup and SECRET_KEY.\n2. For each route, implement GET handlers rendering templates with appropriate context variables derived from data files.\n3. Include placeholders or simple forms for POST routes (e.g., application submission).\n4. Load data from pipe-delimited local text files in the data/ directory using prescribed field orders.\n5. Use clear function names matching page purposes and route URLs consistent with design_spec.md.\n6. Use render_template with template filenames located under templates_draft/.\n\nTemplate Drafting Guidelines:\n1. Create basic HTML structure for each template including DOCTYPE, <html>, <head> with page title, and <body>.\n2. Include all required UI elements with exact IDs as specified in the user requirements.\n3. Use Jinja2 syntax to loop over data items and display context variables as per design_spec.md.\n4. Implement navigation buttons as links or forms referencing correct routes.\n5. Mark dynamic IDs using Jinja2 template expressions (e.g., id=\"view-job-button-{{ job.job_id }}\").\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save app_draft.py and all template files under templates_draft/.\n- All element IDs MUST match exactly those specified in user requirements.\n- Do NOT implement final polishing or optimization - this is a working draft for later refinement.\n- Ensure all local data file formats and field orders comply strictly with specifications.\n- Flask app MUST start with dashboard page route as root ('/') redirect or render.\n\nOutput: app_draft.py, templates_draft/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"WebArchitect\"},\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_draft.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_draft/*.html\"}\n            ]\n        },\n        {\n            \"agent_name\": \"IntegrationEngineer\",\n            \"prompt\": \"\"\"You are a Full Stack Flask Developer specializing in integrating and refining Flask app drafts and templates.\n\nYour goal is to integrate and refine app_draft.py and templates_draft/*.html into a final cohesive Flask application (app.py) and templates set (*.html) fully compliant with design_spec.md and user requirements.\n\nTask Details:\n- Read design_spec.md, user_task_description, app_draft.py, and all templates_draft/*.html files.\n- Produce final app.py with fully integrated Flask routes and handlers removing any draft dependencies.\n- Refine templates from templates_draft/*.html to templates/*.html ensuring all pages, UI element IDs, navigation, and data presentation strictly comply with specifications.\n- Ensure all routes, page titles, element IDs, and local data file handling precisely match the design_spec.md requirements.\n- The Flask app MUST start at the Dashboard page with root route '/' redirecting or rendering it.\n- Refine and fix any inconsistencies, missing features, or errors present in drafts.\n\nIntegration and Refinement Guidelines:\n1. Merge route handlers ensuring no draft placeholders remain.\n2. Use render_template referencing templates/ directory without draft suffix.\n3. Implement form submission handling and any POST routes required.\n4. Validate local data reading/parsing according to data file schemas.\n5. Preserve all UI element IDs exactly as specified.\n6. Confirm page titles and navigation links precisely follow specifications.\n7. Ensure app.py runs as a cohesive Flask app supporting all user workflows.\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save app.py and all final template files under templates/.\n- Do not alter or add new routes beyond design_spec.md and drafts.\n- Maintain exact element ID naming and page titles as specified.\n- Remove any draft references from code and templates.\n- Focus on integration completeness and correctness as defined.\n- Provide clean, runnable final Flask app without draft artifacts.\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"WebArchitect\"},\n                {\"type\": \"text_file\", \"name\": \"app_draft.py\", \"source\": \"DraftEngineer\"},\n                {\"type\": \"text_file\", \"name\": \"templates_draft/*.html\", \"source\": \"DraftEngineer\"},\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"DraftEngineer\",\n            \"reviewer_agent\": \"IntegrationEngineer\",\n            \"review_criteria\": \"Check that app_draft.py and templates_draft/*.html conform to design_spec.md and user requirements before producing the final integration.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_draft.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_draft/*.html\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ]\n): pass",
    "phase3": "def verification_phase(\n    goal: str = \"Validate and finalize the 'JobBoard' Flask application by testing app.py and templates/*.html, then apply fixes to produce the final application.\",\n    collab_pattern_name: str = \"Sequential Flow\",\n    collab_pattern_description: str = (\n        \"WebValidator inspects and tests the integrated app.py and templates/*.html for syntax correctness, compliance with design_spec.md, route availability, UI element presence (element IDs), data handling, and navigation. \"\n        \"SequentialFixer applies all corrections based on validation_report.md to produce the final runnable Flask application with complete requirement coverage.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"WebValidator\",\n            \"prompt\": \"\"\"You are a Software Test Engineer specializing in Flask web application validation and quality assurance.\n\nYour goal is to validate the complete integrated Flask application to ensure syntax correctness, adherence to the design specification, route availability, UI element presence, data handling accuracy, and correct navigation behavior, producing a detailed validation report.\n\nTask Details:\n- Read input artifacts: app.py, all HTML templates in templates/*.html, design_spec.md, and user_task_description from CONTEXT\n- Produce output artifact: validation_report.md with comprehensive test and validation findings\n- Focus on confirming the presence of all routes, UI element IDs, local data handling per data schemas, and Dashboard as the start page\n\nValidation Requirements:\n1. **Syntax Validation**:\n   - Check Python syntax and runtime errors in app.py using validate_python_file tool\n   - Confirm HTML syntax correctness in templates/*.html (visual/manual checks or parsing)\n\n2. **Route Validation**:\n   - Verify all routes defined in design_spec.md exist in app.py\n   - Confirm root route '/' redirects to Dashboard page\n\n3. **UI Elements Validation**:\n   - Check presence of ALL element IDs in each HTML template as specified in design_spec.md\n   - Verify dynamic IDs (e.g., view-job-button-{job_id}) appear correctly with placeholders or Jinja2 syntax\n\n4. **Data Handling Validation**:\n   - Validate app.py data loading from specified local text files complies with design_spec.md data schemas\n   - Confirm proper parsing format and field order usage\n\n5. **Navigation and Functionality**:\n   - Confirm all navigation buttons and links correctly point to appropriate routes with correct identifiers\n   - Check form inputs and submission buttons exist as per specification\n\nCRITICAL REQUIREMENTS:\n- Use validate_python_file tool to check app.py\n- Use execute_python_code tool to assist any calculations or runtime checks\n- Use write_text_file tool to save the detailed validation_report.md\n- Format validation_report.md clearly with sections for syntax, routes, UI elements, data handling, navigation findings\n- Focus validation on inputs specified only (app.py, templates/*.html, design_spec.md, user task)\n- Do NOT modify any input files\n- Provide detailed, actionable findings for SequentialFixer to apply\n\nOutput: validation_report.md\"\"\",\n            \"tools\": [\"validate_python_file\", \"execute_python_code\", \"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"IntegrationEngineer\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"IntegrationEngineer\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"WebArchitect\"},\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_report.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"SequentialFixer\",\n            \"prompt\": \"\"\"You are a Full-Stack Developer with expertise in debugging and refining Flask web applications.\n\nYour goal is to apply all corrections stated in the validation_report.md to the existing app.py and templates/*.html files, ensuring full compliance with design_spec.md and complete coverage of user requirements, producing final production-ready Flask application files.\n\nTask Details:\n- Read input artifacts: validation_report.md, app.py, templates/*.html, design_spec.md, and user_task_description from CONTEXT\n- Output corrected app.py and templates/*.html files reflecting all required fixes\n- Scope is limited to fixing issues in app.py and templates only per validation_report.md findings for syntax, routes, UI elements, data handling, and navigation\n\nFixing Instructions:\n1. **Syntax and Runtime Fixes**:\n   - Correct all Python syntax and runtime errors in app.py identified by WebValidator\n   - Fix any broken HTML markup or missing critical structure in templates\n\n2. **Route and Navigation Fixes**:\n   - Ensure all Flask routes match those in design_spec.md precisely\n   - Confirm that root route '/' redirects to dashboard page\n   - Correct navigation links and buttons to use proper Flask url_for functions and IDs\n\n3. **UI Elements and Template Fixes**:\n   - Add or correct missing UI elements with exact IDs as specified\n   - Fix dynamic element ID templating with correct Jinja2 syntax\n   - Maintain consistent element naming and structure\n\n4. **Data Handling Fixes**:\n   - Adjust data loading, parsing, and usage in app.py to match data schema specifications exactly\n   - Fix file reading logic, field order, and error handling as needed\n\n5. **Testing and Verification**:\n   - Ensure completed fixes resolve all validation issues\n   - Preserve or enhance all features required by user specification\n   - Deliver clean, maintainable, and runnable Flask app.py and templates\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save all fixed app.py and templates/*.html files\n- Deliver final code that passes all syntax validations and meets design_spec.md requirements fully\n- Do NOT introduce new features beyond fixing validation issues\n- Preserve all user requirements and original design integrity\n- Provide outputs in correct file names as input except for corrected content only\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_report.md\", \"source\": \"WebValidator\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"IntegrationEngineer\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"IntegrationEngineer\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"WebArchitect\"},\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"WebValidator\",\n            \"reviewer_agent\": \"SequentialFixer\",\n            \"review_criteria\": \"Verify validation_report.md covers all critical syntax, route, UI element ID errors, and data handling issues thoroughly.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_report.md\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        },\n        {\n            \"source_agent\": \"SequentialFixer\",\n            \"reviewer_agent\": \"RequirementsAnalyst\",\n            \"review_criteria\": \"Confirm the final app.py and templates/*.html completely address all validation issues while preserving full user requirement coverage.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_report.md\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ]\n): pass",
}

user_task = """
# Requirements Document for 'JobBoard' Web Application

## 1. Objective
Develop a comprehensive web application named 'JobBoard' using Python, with data managed through local text files. The application enables users to browse job postings, submit resumes, track applications, view company profiles, and manage job applications. No authentication required - all features are directly accessible. Note that the website should start from the Dashboard page.

## 2. Language
The required development language for the 'JobBoard' application is Python.

## 3. Page Design

The 'JobBoard' web application will consist of the following nine pages:

### 1. Dashboard Page
- **Page Title**: Job Board Dashboard
- **Overview**: The main hub displaying featured job postings, latest opportunities, and quick navigation to all functionalities.
- **Elements**:
  - **ID: dashboard-page** - Type: Div - Container for the dashboard page.
  - **ID: featured-jobs** - Type: Div - Display of featured job recommendations.
  - **ID: browse-jobs-button** - Type: Button - Button to navigate to job listings page.
  - **ID: my-applications-button** - Type: Button - Button to navigate to applications tracking page.
  - **ID: companies-button** - Type: Button - Button to navigate to companies directory page.

### 2. Job Listings Page
- **Page Title**: Job Listings
- **Overview**: A page displaying all available job postings with search and filter capabilities.
- **Elements**:
  - **ID: listings-page** - Type: Div - Container for the listings page.
  - **ID: search-input** - Type: Input - Field to search jobs by title, company, or location.
  - **ID: category-filter** - Type: Dropdown - Dropdown to filter by job category (Technology, Finance, Healthcare, etc.).
  - **ID: location-filter** - Type: Dropdown - Dropdown to filter by location (Remote, On-site, Hybrid).
  - **ID: jobs-grid** - Type: Div - Grid displaying job cards with title, company, location, and salary range.
  - **ID: view-job-button-{job_id}** - Type: Button - Button to view job details (each job card has this).

### 3. Job Details Page
- **Page Title**: Job Details
- **Overview**: A page displaying detailed information about a specific job posting.
- **Elements**:
  - **ID: job-details-page** - Type: Div - Container for the job details page.
  - **ID: job-title** - Type: H1 - Display job title.
  - **ID: company-name** - Type: Div - Display company name.
  - **ID: job-description** - Type: Div - Display full job description and requirements.
  - **ID: salary-range** - Type: Div - Display salary range.
  - **ID: apply-now-button** - Type: Button - Button to apply for the job.

### 4. Application Form Page
- **Page Title**: Submit Application
- **Overview**: A page for users to submit job applications with resume and cover letter.
- **Elements**:
  - **ID: application-form-page** - Type: Div - Container for the application form page.
  - **ID: applicant-name** - Type: Input - Field to input applicant name.
  - **ID: applicant-email** - Type: Input - Field to input applicant email.
  - **ID: resume-upload** - Type: File Input - Field to upload resume file.
  - **ID: cover-letter** - Type: Textarea - Field to enter cover letter text.
  - **ID: submit-application-button** - Type: Button - Button to submit application.

### 5. Application Tracking Page
- **Page Title**: My Applications
- **Overview**: A page displaying all submitted applications with status tracking.
- **Elements**:
  - **ID: tracking-page** - Type: Div - Container for the tracking page.
  - **ID: applications-table** - Type: Table - Table displaying applications with job title, company, status, and date applied.
  - **ID: status-filter** - Type: Dropdown - Dropdown to filter by status (All, Applied, Under Review, Interview, Rejected).
  - **ID: view-application-button-{app_id}** - Type: Button - Button to view application details (each application has this).
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 6. Companies Directory Page
- **Page Title**: Company Directory
- **Overview**: A page displaying all registered companies with their profiles and available jobs.
- **Elements**:
  - **ID: companies-page** - Type: Div - Container for the companies page.
  - **ID: companies-list** - Type: Div - List of company cards with company name, industry, and employee count.
  - **ID: search-company-input** - Type: Input - Field to search companies by name or industry.
  - **ID: view-company-button-{company_id}** - Type: Button - Button to view company profile (each company card has this).
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 7. Company Profile Page
- **Page Title**: Company Profile
- **Overview**: A page displaying detailed information about a specific company.
- **Elements**:
  - **ID: company-profile-page** - Type: Div - Container for the company profile page.
  - **ID: company-info** - Type: Div - Display company name, industry, location, and description.
  - **ID: company-jobs** - Type: Div - Display all open jobs from this company.
  - **ID: jobs-list** - Type: Div - List of jobs with titles and status indicators.
  - **ID: view-job-button-{job_id}** - Type: Button - Button to view job details from company profile.
  - **ID: back-to-companies** - Type: Button - Button to go back to companies directory.

### 8. Resume Management Page
- **Page Title**: My Resumes
- **Overview**: A page for users to upload and manage multiple resumes.
- **Elements**:
  - **ID: resume-page** - Type: Div - Container for the resume page.
  - **ID: resumes-list** - Type: Div - List of uploaded resumes with upload date.
  - **ID: upload-resume-button** - Type: Button - Button to upload a new resume.
  - **ID: resume-file-input** - Type: File Input - Hidden file input for resume upload.
  - **ID: delete-resume-button-{resume_id}** - Type: Button - Button to delete a resume (each resume has this).
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 9. Search Results Page
- **Page Title**: Search Results
- **Overview**: A page displaying search results for jobs and companies.
- **Elements**:
  - **ID: search-results-page** - Type: Div - Container for the search results page.
  - **ID: search-query-display** - Type: Div - Display the search query entered.
  - **ID: results-tabs** - Type: Div - Tabs to switch between job results and company results.
  - **ID: job-results** - Type: Div - Display search results for jobs.
  - **ID: company-results** - Type: Div - Display search results for companies.
  - **ID: no-results-message** - Type: Div - Display when no results are found.

## 4. Data Storage

The 'JobBoard' application will store data locally in text files organized in the directory 'data'. The following data formats and examples are defined:

### 1. Jobs Data
- **File Name**: `jobs.txt`
- **Data Format**:
  ```
  job_id|title|company_id|location|salary_min|salary_max|category|description|posted_date
  ```
- **Example Data**:
  ```
  1|Senior Python Developer|1|Remote|80000|120000|Technology|Experienced Python developer for web applications|2025-01-15
  2|Data Analyst|2|New York, NY|60000|85000|Finance|Analyze financial data and create reports|2025-01-16
  3|Healthcare Administrator|3|Los Angeles, CA|50000|70000|Healthcare|Manage hospital operations and patient records|2025-01-14
  ```

### 2. Companies Data
- **File Name**: `companies.txt`
- **Data Format**:
  ```
  company_id|company_name|industry|location|employee_count|description
  ```
- **Example Data**:
  ```
  1|TechCorp|Technology|San Francisco, CA|500|Leading software solutions provider
  2|FinanceHub|Finance|New York, NY|300|Innovative financial services company
  3|MediCare|Healthcare|Los Angeles, CA|200|Premier healthcare management organization
  ```

### 3. Categories Data
- **File Name**: `categories.txt`
- **Data Format**:
  ```
  category_id|category_name|description
  ```
- **Example Data**:
  ```
  1|Technology|Software, IT, and tech-related positions
  2|Finance|Banking, accounting, and finance positions
  3|Healthcare|Medical and healthcare industry positions
  ```

### 4. Applications Data
- **File Name**: `applications.txt`
- **Data Format**:
  ```
  application_id|job_id|applicant_name|applicant_email|status|applied_date|resume_id
  ```
- **Example Data**:
  ```
  1|1|John Doe|john@email.com|Under Review|2025-01-17|1
  2|2|Jane Smith|jane@email.com|Applied|2025-01-16|2
  3|3|Robert Johnson|robert@email.com|Interview|2025-01-15|3
  ```

### 5. Resumes Data
- **File Name**: `resumes.txt`
- **Data Format**:
  ```
  resume_id|applicant_name|applicant_email|filename|upload_date|summary
  ```
- **Example Data**:
  ```
  1|John Doe|john@email.com|john_resume.pdf|2025-01-17|Senior developer with 8 years experience
  2|Jane Smith|jane@email.com|jane_resume.pdf|2025-01-16|Data analyst with financial background
  3|Robert Johnson|robert@email.com|robert_resume.pdf|2025-01-15|Healthcare administrator with 5 years experience
  ```

### 6. Job Categories Mapping Data
- **File Name**: `job_categories.txt`
- **Data Format**:
  ```
  mapping_id|job_id|category_id
  ```
- **Example Data**:
  ```
  1|1|1
  2|2|2
  3|3|3
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
            """You are a Software Requirements Analyst specializing in web application requirements documentation.

Your goal is to analyze the user-provided task description and produce a comprehensive requirements analysis document that details all pages, page titles, UI element IDs, navigation structure, and data storage requirements for the JobBoard web application.

Task Details:
- Read user_task_description in full to extract relevant information
- Identify and document all pages with their exact titles
- Extract and list all UI element IDs for each page
- Outline the navigation flow between pages using button/element IDs
- Summarize data storage requirements including data files, fields, and formats mentioned
- Output requirements_analysis.md capturing all above information clearly and completely

Analysis Requirements:
1. **Pages and Titles**:
   - List each page in the app with exact title as in the user task
   - Include key container element IDs per page

2. **UI Element IDs**:
   - Enumerate all specified UI element IDs for each page accurately
   - Distinguish between static and dynamic element IDs (with variable placeholders)

3. **Navigation Structure**:
   - Map navigational buttons or links to target pages by their button IDs
   - Reflect logical entry points and user flow starting from Dashboard

4. **Data Storage Summary**:
   - List each data file with its name and described format
   - Include fields and example data if available
   - Note relationships or mappings between data files

CRITICAL REQUIREMENTS:
- Use write_text_file tool to output requirements_analysis.md
- Ensure completeness and accuracy matching the user task exactly
- Avoid assumptions beyond the provided user task description

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

Your goal is to create a detailed design specification that converts the requirements_analysis.md into an explicit architecture document containing Flask route endpoints, HTTP methods, exact page titles, template filenames, UI element IDs, navigation flow, and detailed data file schemas. The design must support user navigation starting at the Dashboard page without requiring authentication.

Task Details:
- Read requirements_analysis.md and user_task_description fully
- Define Flask route endpoints with HTTP methods (GET/POST) for all pages and actions
- Specify exact page titles as per requirements
- Map each page to a template filename (templates/{page_name}.html or similar)
- List all UI element IDs as extracted, including dynamic ID patterns
- Specify navigation flow between pages referencing precise button/link IDs
- Define detailed data file schemas with file names, exact field order, data formats (pipe-delimited), and example data rows
- Ensure architecture supports all user task features with no authentication, starting at Dashboard

Design Requirements:
1. **Flask Routes**:
   - Use RESTful GET for pages rendering data
   - Use POST where form submissions occur (e.g., application form)
   - Include dynamic parameters for detail pages (e.g., job_id, company_id, app_id where applicable)

2. **Templates and Page Titles**:
   - Define template filenames tied to pages (snake_case naming recommended)
   - Include exact page titles matching requirements

3. **UI Element IDs**:
   - Enumerate all exact element IDs from requirements_analysis.md
   - Specify format for dynamic IDs with placeholders (e.g., view-job-button-{job_id})

4. **Data File Contracts**:
   - For each data file, specify path data/{filename}.txt
   - List fields in exact order pipe-delimited
   - Describe contents briefly
   - Provide 2-3 example entries matching user data samples

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save output as design_spec.md
- Ensure full traceability between requirements_analysis.md and design_spec.md
- Follow user requirements precisely; no assumptions beyond spec
- Use consistent naming conventions for routes, templates, UI IDs
- Support direct navigation from Dashboard with no authentication requirement

Output: design_spec.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'requirements_analysis.md', 'source': 'RequirementsAnalyst'}, {'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_spec.md'}],

    },

    "DraftEngineer": {
        "prompt": (
            """You are a Backend and Frontend Developer specializing in Flask web applications with template drafting.

Your goal is to draft a Flask application (app_draft.py) and corresponding HTML template drafts implementing all required pages, UI element IDs, navigation buttons, and data interactions with local text files.

Task Details:
- Read design_spec.md and user_task_description fully to understand all pages, routes, UIs, and data storage formats.
- Create app_draft.py implementing Flask routes and handlers covering all pages and features.
- Draft ALL HTML templates (*.html) for all pages with correct UI element IDs as specified in user requirements.
- Use render_template calls referencing templates in a 'templates_draft/' directory.
- Manage local data files for all specified entities (jobs, companies, applications, resumes, categories, job_categories).
- Focus on implementing page navigation and data loading/presentation as drafts for subsequent refinement.
- Output app_draft.py and templates draft files under templates_draft/ folder.

Flask Implementation Guidelines:
1. Define Flask app with standard setup and SECRET_KEY.
2. For each route, implement GET handlers rendering templates with appropriate context variables derived from data files.
3. Include placeholders or simple forms for POST routes (e.g., application submission).
4. Load data from pipe-delimited local text files in the data/ directory using prescribed field orders.
5. Use clear function names matching page purposes and route URLs consistent with design_spec.md.
6. Use render_template with template filenames located under templates_draft/.

Template Drafting Guidelines:
1. Create basic HTML structure for each template including DOCTYPE, <html>, <head> with page title, and <body>.
2. Include all required UI elements with exact IDs as specified in the user requirements.
3. Use Jinja2 syntax to loop over data items and display context variables as per design_spec.md.
4. Implement navigation buttons as links or forms referencing correct routes.
5. Mark dynamic IDs using Jinja2 template expressions (e.g., id="view-job-button-{{ job.job_id }}").

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save app_draft.py and all template files under templates_draft/.
- All element IDs MUST match exactly those specified in user requirements.
- Do NOT implement final polishing or optimization - this is a working draft for later refinement.
- Ensure all local data file formats and field orders comply strictly with specifications.
- Flask app MUST start with dashboard page route as root ('/') redirect or render.

Output: app_draft.py, templates_draft/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'WebArchitect'}, {'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app_draft.py'}, {'type': 'text_file', 'name': 'templates_draft/*.html'}],

    },

    "IntegrationEngineer": {
        "prompt": (
            """You are a Full Stack Flask Developer specializing in integrating and refining Flask app drafts and templates.

Your goal is to integrate and refine app_draft.py and templates_draft/*.html into a final cohesive Flask application (app.py) and templates set (*.html) fully compliant with design_spec.md and user requirements.

Task Details:
- Read design_spec.md, user_task_description, app_draft.py, and all templates_draft/*.html files.
- Produce final app.py with fully integrated Flask routes and handlers removing any draft dependencies.
- Refine templates from templates_draft/*.html to templates/*.html ensuring all pages, UI element IDs, navigation, and data presentation strictly comply with specifications.
- Ensure all routes, page titles, element IDs, and local data file handling precisely match the design_spec.md requirements.
- The Flask app MUST start at the Dashboard page with root route '/' redirecting or rendering it.
- Refine and fix any inconsistencies, missing features, or errors present in drafts.

Integration and Refinement Guidelines:
1. Merge route handlers ensuring no draft placeholders remain.
2. Use render_template referencing templates/ directory without draft suffix.
3. Implement form submission handling and any POST routes required.
4. Validate local data reading/parsing according to data file schemas.
5. Preserve all UI element IDs exactly as specified.
6. Confirm page titles and navigation links precisely follow specifications.
7. Ensure app.py runs as a cohesive Flask app supporting all user workflows.

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save app.py and all final template files under templates/.
- Do not alter or add new routes beyond design_spec.md and drafts.
- Maintain exact element ID naming and page titles as specified.
- Remove any draft references from code and templates.
- Focus on integration completeness and correctness as defined.
- Provide clean, runnable final Flask app without draft artifacts.

Output: app.py, templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'WebArchitect'}, {'type': 'text_file', 'name': 'app_draft.py', 'source': 'DraftEngineer'}, {'type': 'text_file', 'name': 'templates_draft/*.html', 'source': 'DraftEngineer'}, {'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}],

    },

    "WebValidator": {
        "prompt": (
            """You are a Software Test Engineer specializing in Flask web application validation and quality assurance.

Your goal is to validate the complete integrated Flask application to ensure syntax correctness, adherence to the design specification, route availability, UI element presence, data handling accuracy, and correct navigation behavior, producing a detailed validation report.

Task Details:
- Read input artifacts: app.py, all HTML templates in templates/*.html, design_spec.md, and user_task_description from CONTEXT
- Produce output artifact: validation_report.md with comprehensive test and validation findings
- Focus on confirming the presence of all routes, UI element IDs, local data handling per data schemas, and Dashboard as the start page

Validation Requirements:
1. **Syntax Validation**:
   - Check Python syntax and runtime errors in app.py using validate_python_file tool
   - Confirm HTML syntax correctness in templates/*.html (visual/manual checks or parsing)

2. **Route Validation**:
   - Verify all routes defined in design_spec.md exist in app.py
   - Confirm root route '/' redirects to Dashboard page

3. **UI Elements Validation**:
   - Check presence of ALL element IDs in each HTML template as specified in design_spec.md
   - Verify dynamic IDs (e.g., view-job-button-{job_id}) appear correctly with placeholders or Jinja2 syntax

4. **Data Handling Validation**:
   - Validate app.py data loading from specified local text files complies with design_spec.md data schemas
   - Confirm proper parsing format and field order usage

5. **Navigation and Functionality**:
   - Confirm all navigation buttons and links correctly point to appropriate routes with correct identifiers
   - Check form inputs and submission buttons exist as per specification

CRITICAL REQUIREMENTS:
- Use validate_python_file tool to check app.py
- Use execute_python_code tool to assist any calculations or runtime checks
- Use write_text_file tool to save the detailed validation_report.md
- Format validation_report.md clearly with sections for syntax, routes, UI elements, data handling, navigation findings
- Focus validation on inputs specified only (app.py, templates/*.html, design_spec.md, user task)
- Do NOT modify any input files
- Provide detailed, actionable findings for SequentialFixer to apply

Output: validation_report.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['validate_python_file', 'execute_python_code', 'write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'app.py', 'source': 'IntegrationEngineer'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'IntegrationEngineer'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'WebArchitect'}, {'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'validation_report.md'}],

    },

    "SequentialFixer": {
        "prompt": (
            """You are a Full-Stack Developer with expertise in debugging and refining Flask web applications.

Your goal is to apply all corrections stated in the validation_report.md to the existing app.py and templates/*.html files, ensuring full compliance with design_spec.md and complete coverage of user requirements, producing final production-ready Flask application files.

Task Details:
- Read input artifacts: validation_report.md, app.py, templates/*.html, design_spec.md, and user_task_description from CONTEXT
- Output corrected app.py and templates/*.html files reflecting all required fixes
- Scope is limited to fixing issues in app.py and templates only per validation_report.md findings for syntax, routes, UI elements, data handling, and navigation

Fixing Instructions:
1. **Syntax and Runtime Fixes**:
   - Correct all Python syntax and runtime errors in app.py identified by WebValidator
   - Fix any broken HTML markup or missing critical structure in templates

2. **Route and Navigation Fixes**:
   - Ensure all Flask routes match those in design_spec.md precisely
   - Confirm that root route '/' redirects to dashboard page
   - Correct navigation links and buttons to use proper Flask url_for functions and IDs

3. **UI Elements and Template Fixes**:
   - Add or correct missing UI elements with exact IDs as specified
   - Fix dynamic element ID templating with correct Jinja2 syntax
   - Maintain consistent element naming and structure

4. **Data Handling Fixes**:
   - Adjust data loading, parsing, and usage in app.py to match data schema specifications exactly
   - Fix file reading logic, field order, and error handling as needed

5. **Testing and Verification**:
   - Ensure completed fixes resolve all validation issues
   - Preserve or enhance all features required by user specification
   - Deliver clean, maintainable, and runnable Flask app.py and templates

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save all fixed app.py and templates/*.html files
- Deliver final code that passes all syntax validations and meets design_spec.md requirements fully
- Do NOT introduce new features beyond fixing validation issues
- Preserve all user requirements and original design integrity
- Provide outputs in correct file names as input except for corrected content only

Output: app.py, templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'validation_report.md', 'source': 'WebValidator'}, {'type': 'text_file', 'name': 'app.py', 'source': 'IntegrationEngineer'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'IntegrationEngineer'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'WebArchitect'}, {'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}],

    }

}

REVIEW_PROFILES = {
    'RequirementsAnalyst': [
        ("WebArchitect", """Verify requirements_analysis.md covers all pages, UI element IDs, and data storage requirements as specified in the user task with no omissions.""", [{'type': 'user', 'name': 'user_task_description'}, {'type': 'text_file', 'name': 'requirements_analysis.md'}])
    ],

    'DraftEngineer': [
        ("IntegrationEngineer", """Check that app_draft.py and templates_draft/*.html conform to design_spec.md and user requirements before producing the final integration.""", [{'type': 'text_file', 'name': 'app_draft.py'}, {'type': 'text_file', 'name': 'templates_draft/*.html'}, {'type': 'text_file', 'name': 'design_spec.md'}])
    ],

    'WebValidator': [
        ("SequentialFixer", """Verify validation_report.md covers all critical syntax, route, UI element ID errors, and data handling issues thoroughly.""", [{'type': 'text_file', 'name': 'validation_report.md'}, {'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}])
    ],

    'SequentialFixer': [
        ("RequirementsAnalyst", """Confirm the final app.py and templates/*.html completely address all validation issues while preserving full user requirement coverage.""", [{'type': 'text_file', 'name': 'validation_report.md'}, {'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}])
    ]

}



# Orchestration Functions
async def design_specification_phase():
    # Declare agents
    RequirementsAnalyst = build_resilient_agent(
        agent_name="RequirementsAnalyst",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=2,
        timeout_threshold=280,
        failure_threshold=1,
        recovery_time=40
    )
    WebArchitect = build_resilient_agent(
        agent_name="WebArchitect",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=2,
        timeout_threshold=320,
        failure_threshold=1,
        recovery_time=40
    )

    # Execute RequirementsAnalyst first
    await execute(RequirementsAnalyst,
                  "Analyze user_task_description and create requirements_analysis.md detailing pages, titles, UI element IDs, navigation, and data storage requirements")

    # Read requirements_analysis.md content for WebArchitect
    requirements_analysis_content = ""
    try:
        requirements_analysis_content = open("requirements_analysis.md").read()
    except:
        pass

    # Execute WebArchitect after RequirementsAnalyst output is ready
    await execute(WebArchitect,
                  f"Convert requirements_analysis.md to design_spec.md with finalized pages, Flask routes, templates, UI element IDs, navigation flow, and data file schemas.\n\n"
                  f"=== requirements_analysis.md ===\n{requirements_analysis_content}\n\n"
                  f"Also use user_task_description for reference.")
# Phase1_End

# Phase2_Start
import asyncio

async def implementation_phase():
    # Create agents
    DraftEngineer = build_resilient_agent(
        agent_name="DraftEngineer",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=2,
        timeout_threshold=300,
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
        timeout_threshold=400,
        failure_threshold=1,
        recovery_time=50
    )

    # Read draft files for injection before integration
    app_draft_content, templates_draft_content = "", ""
    try:
        app_draft_content = open("app_draft.py").read()
    except Exception:
        app_draft_content = ""
    try:
        # Since templates_draft/*.html could be multiple files,
        # read all and concatenate for injection
        import glob
        paths = glob.glob("templates_draft/*.html")
        templates_contents = []
        for path in paths:
            try:
                templates_contents.append(f"=== {path} ===\n" + open(path).read())
            except Exception:
                continue
        templates_draft_content = "\n\n".join(templates_contents)
    except Exception:
        templates_draft_content = ""

    # Execute DraftEngineer to produce app_draft.py & templates_draft/*.html
    await execute(DraftEngineer,
                  "Create app_draft.py and all HTML templates in templates_draft/ implementing all routes, UI IDs, navigation, and data handling as draft.")

    # After drafts produced, execute IntegrationEngineer injecting draft files content for refinement
    await execute(IntegrationEngineer,
                  f"Integrate and refine app_draft.py and templates_draft/*.html into final app.py and templates/*.html. "
                  f"Ensure full compliance with design_spec.md and user requirements.\n\n"
                  f"=== app_draft.py ===\n{app_draft_content}\n\n=== templates_draft_files ===\n{templates_draft_content}")
# Phase2_End

# Phase3_Start

async def verification_phase():
    # Declare agents
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
        timeout_threshold=450,
        failure_threshold=2,
        recovery_time=60
    )

    # Read templates content for injection
    templates_content = ""
    import glob
    import os

    # Gather all templates/*.html content
    try:
        template_files = glob.glob("templates/*.html")
    except:
        template_files = []

    for tf in template_files:
        try:
            content = open(tf).read()
            templates_content += f"=== {os.path.basename(tf)} ===\n{content}\n\n"
        except:
            pass

    # Execute WebValidator
    await execute(WebValidator,
                  f"Validate the integrated Flask app.py, templates, design_spec.md, and user task. "
                  f"Validate Python syntax in app.py using validate_python_file tool. "
                  f"Check routes, UI element IDs including dynamic ones, data handling, and navigation correctness. "
                  f"Focus on inputs: app.py, templates/*.html, design_spec.md, user_task_description.\n\n"
                  f"=== app.py content ===\n"
                  f"{CONTEXT.get('app.py', [{'content': ''}])[-1]['content'] if CONTEXT.get('app.py') else ''}\n\n"
                  f"=== Templates content ===\n{templates_content}\n"
                  f"=== design_spec.md content ===\n"
                  f"{CONTEXT.get('design_spec.md', [{'content': ''}])[-1]['content'] if CONTEXT.get('design_spec.md') else ''}\n"
                  f"User task description:\n"
                  f"{CONTEXT.get('user_task_description', [{'content': ''}])[-1]['content'] if CONTEXT.get('user_task_description') else ''}"
                  )

    # Read validation_report.md from file for injection
    validation_report = ""
    try:
        validation_report = open("validation_report.md").read()
    except:
        pass

    # Read app.py content from file for injection
    app_py_content = ""
    try:
        app_py_content = open("app.py").read()
    except:
        pass

    # Re-gather templates content for SequentialFixer (may be updated or unchanged)
    templates_content_for_fixer = ""
    for tf in template_files:
        try:
            content = open(tf).read()
            templates_content_for_fixer += f"=== {os.path.basename(tf)} ===\n{content}\n\n"
        except:
            pass

    # Read design_spec.md content
    design_spec_content = CONTEXT.get("design_spec.md", [{'content': ''}])[-1]['content'] if CONTEXT.get("design_spec.md") else ""

    # Read user_task_description
    user_task_desc = CONTEXT.get("user_task_description", [{'content': ''}])[-1]['content'] if CONTEXT.get("user_task_description") else ""

    # Execute SequentialFixer with injected inputs and validation report
    await execute(SequentialFixer,
                  f"Fix all issues reported in validation_report.md to produce final production-ready app.py and templates.\n\n"
                  f"=== Validation Report ===\n{validation_report}\n\n"
                  f"=== app.py ===\n{app_py_content}\n\n"
                  f"=== Templates ===\n{templates_content_for_fixer}\n\n"
                  f"=== design_spec.md ===\n{design_spec_content}\n\n"
                  f"User task description:\n{user_task_desc}")
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
