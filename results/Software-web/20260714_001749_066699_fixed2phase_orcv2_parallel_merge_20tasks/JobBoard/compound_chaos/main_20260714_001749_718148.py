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
# 20260714_001749_718148/main_20260714_001749_718148.py

# Phase_info dictionary containing complete def blocks for failover context
Phase_info = {
    "phase1": "def design_specification_phase(\n    goal: str = \"Define and merge comprehensive backend and frontend specifications for the JobBoard web application as complementary design documents and a unified design_spec.md\",\n    collab_pattern_name: str = \"Parallel + Merger\",\n    collab_pattern_description: str = \"BackendDesignArchitect and FrontendDesignArchitect independently produce backend and frontend design documents describing routes, data schemas, pages, and UI elements. DesignMerger merges these documents into one coherent design_spec.md ensuring internal consistency and alignment with user requirements.\",\n    team: list = [\n        {\n            \"agent_name\": \"BackendDesignArchitect\",\n            \"prompt\": \"\"\"You are a Software Architect specializing in Flask backend applications using Python.\n\nYour goal is to design the backend architecture of the JobBoard web application, producing a comprehensive design document independent of frontend specifications.\n\nTask Details:\n- Read user_task_description from CONTEXT\n- Produce backend_design.md specifying Flask route handlers, data schemas for local text files, and business logic\n- Do not read or assume frontend_design.md\n\n**Backend Routes and Handlers**\n- Specify each route path, HTTP methods, and handler function names\n- Define required request parameters and form fields\n- Outline response behavior including redirects and template rendering\n- Include routes for Dashboard, Job Listings, Job Details, Application Form, Application Tracking, Companies Directory, Company Profile, Resume Management, and Search Results\n- Specify navigation-related routes triggered by buttons with IDs like browse-jobs-button, companies-button, etc.\n\n**Data Storage Specifications**\n- Define schemas matching jobs.txt, companies.txt, categories.txt, applications.txt, resumes.txt, and job_categories.txt formats\n- Include field order, delimiter ('|'), data types, and example rows\n- Specify business logic connecting routes with data file read/write operations\n\n**Business Logic and Workflow**\n- Outline logic for job filtering, searching, application submissions, resume handling, and application status tracking\n- Detail how data consistency is maintained without authentication\n- Specify error handling and validation requirements\n\nCRITICAL SUCCESS CRITERIA:\n- MUST use write_text_file tool to output backend_design.md\n- Produced design must fully cover backend routes and data schemas per user_task_description\n- Design must be independent from frontend_design.md and not reference or require it for completeness\n\nOutput: backend_design.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"backend_design.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"FrontendDesignArchitect\",\n            \"prompt\": \"\"\"You are a UI/UX Designer specializing in HTML layouts and user interface design for Flask web applications.\n\nYour goal is to design the complete frontend layout and templates for the JobBoard web application, independently from backend design.\n\nTask Details:\n- Read user_task_description from CONTEXT\n- Produce frontend_design.md specifying HTML templates, element IDs, page structures, and UI navigation flows\n- Do not read or assume backend_design.md\n\n**Page Templates and Element IDs**\n- Define each of the nine pages with page titles and container divs as specified\n- Specify all element IDs with types and their roles within each page, e.g., buttons, tables, inputs, dropdowns\n- Include dynamic IDs where applicable (e.g., view-job-button-{job_id})\n\n**Navigation and Interaction Flow**\n- Map navigation buttons to target pages\n- Describe layout structure: div nesting, sections per page, and tab components for Search Results\n- Ensure UI elements match data interactions from user requirements\n\n**Accessibility and Usability**\n- Specify consistent naming conventions for element IDs\n- Ensure clear separation of interactive controls and data display areas\n- Outline any necessary UI states (empty results, filtered views)\n\nCRITICAL SUCCESS CRITERIA:\n- MUST use write_text_file tool to output frontend_design.md\n- Designs must reflect all pages and UI elements exactly as per user_task_description\n- Design must be independent from backend_design.md and sufficient for frontend implementation\n\nOutput: frontend_design.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"frontend_design.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"DesignMerger\",\n            \"prompt\": \"\"\"You are a Systems Architect specializing in full-stack Flask web application design integration.\n\nYour goal is to merge backend_design.md and frontend_design.md into one consistent design_spec.md without adding new requirements, ensuring alignment with user_task_description.\n\nTask Details:\n- Read user_task_description, backend_design.md, and frontend_design.md from CONTEXT\n- Validate completeness and consistency across backend routes, data schemas, and frontend templates with element IDs\n- Reconcile any discrepancies and unify naming conventions for seamless implementation\n\n**Integration Strategy**\n- Section 1: Backend Routes and Data Schemas\n  - Consolidate all Flask routes and corresponding data file schemas\n  - Maintain completeness and business logic from backend_design.md\n\n- Section 2: Frontend Templates and UI Elements\n  - Incorporate all page templates, element IDs, and navigation flows from frontend_design.md\n  - Align button IDs and navigation references with backend routes\n\n- Section 3: Consistency and Completeness Checks\n  - Ensure all elements used in frontend templates have backend support\n  - Confirm all backend routes serving UI pages correspond to frontend pages and controls\n  - Resolve conflicting or missing references without adding new features\n\nCRITICAL SUCCESS CRITERIA:\n- MUST use write_text_file tool to output design_spec.md\n- Final design_spec.md must be a coherent specification enabling independent full-stack development\n- Do not modify or invent artifacts beyond the inputs; preserve all declared output artifact names\n\nOutput: design_spec.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"backend_design.md\", \"source\": \"BackendDesignArchitect\"},\n                {\"type\": \"text_file\", \"name\": \"frontend_design.md\", \"source\": \"FrontendDesignArchitect\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"BackendDesignArchitect\",\n            \"reviewer_agent\": \"DesignMerger\",\n            \"review_criteria\": \"Verify completeness and correctness of backend routes, data schemas, and business logic for JobBoard functionality.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"backend_design.md\"}\n            ]\n        },\n        {\n            \"source_agent\": \"FrontendDesignArchitect\",\n            \"reviewer_agent\": \"DesignMerger\",\n            \"review_criteria\": \"Verify frontend page designs and element IDs match user requirements and complement the backend architecture.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"frontend_design.md\"}\n            ]\n        }\n    ]\n): pass",
    "phase2": "def implementation_and_verification_phase(\n    goal: str = \"Implement backend and frontend components in parallel per design_spec.md, then integrate into final app.py and templates/*.html files\",\n    collab_pattern_name: str = \"Parallel + Merger\",\n    collab_pattern_description: str = \"BackendDeveloper and FrontendDeveloper independently implement backend app.py and frontend templates/*.html from design_spec.md; IntegrationMerger reconciles and integrates their outputs into final deployable artifacts.\",\n    team: list = [\n        {\n            \"agent_name\": \"BackendDeveloper\",\n            \"prompt\": \"\"\"You are a Backend Developer specializing in Flask web applications using local text-file data management.\n\nYour goal is to implement the complete Flask backend for the JobBoard application according to the provided design_spec.md.\n\nTask Details:\n- Read design_spec.md from CONTEXT for detailed route specifications, data schemas, and business logic\n- Independently develop app.py implementing all specified routes, request handlers, and data persistence using local text files\n- Write complete app.py output artifact with all backend logic, including data loading/saving for jobs.txt, companies.txt, categories.txt, applications.txt, resumes.txt, and job_categories.txt\n- Do not read or depend on frontend templates during implementation\n\n**Implementation Requirements:**\n- Implement each Flask route as specified with correct URL endpoints, HTTP methods, and response structures\n- Load and save data exclusively from/to the given localized text files with their specified formats\n- Include validation, error handling, and business logic to manage job listings, applications, resumes, and company profiles\n- Use Python-standard idiomatic patterns for file I/O and Flask routing\n\n**Data Management:**\n- Adhere strictly to the data file formats and field orders given in design_spec.md without inventing fields\n- Handle all CRUD operations required by the application on those text files\n\nCRITICAL SUCCESS CRITERIA:\n- Use write_text_file tool to output app.py\n- Fully implement all backend features and routes defined only by design_spec.md\n- The backend app.py is independently runnable and complete without frontend assumptions\n\nOutput: app.py\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"}\n            ]\n        },\n        {\n            \"agent_name\": \"FrontendDeveloper\",\n            \"prompt\": \"\"\"You are a Frontend Developer specializing in HTML and Jinja2 templates for Flask applications.\n\nYour goal is to develop the complete set of HTML templates (*.html) for the JobBoard web app as specified in design_spec.md.\n\nTask Details:\n- Read design_spec.md from CONTEXT for page layouts, element IDs, template names, and navigation structure\n- Independently create all frontend templates covering all JobBoard pages and UI elements, following exact element ID conventions\n- Produce templates/*.html output artifact containing all required templates for dashboard, listings, job details, application form, tracking, companies, company profile, resumes, and search results\n- Do not read or rely on backend app.py during template creation\n\n**Template Specifications:**\n- Each page template must include all specified element IDs with correct HTML tags (div, input, button, table, etc.) as per design_spec.md\n- Implement template inheritance and layout reuse where appropriate\n- Navigation and buttons must correspond exactly with route names expected from backend specification\n\n**UI Consistency:**\n- Ensure UI elements reflect data context variables for dynamic content rendering\n- Use standard semantic HTML structures and accessible attributes\n\nCRITICAL SUCCESS CRITERIA:\n- Use write_text_file tool to output templates/*.html\n- Templates fully comply with design_spec.md element IDs, page structure, and navigation\n- Templates are complete and independently implementable without backend code assumptions\n\nOutput: templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        },\n        {\n            \"agent_name\": \"IntegrationMerger\",\n            \"prompt\": \"\"\"You are a Software Integration Engineer specializing in merging backend and frontend components for Flask web applications.\n\nYour goal is to integrate the backend app.py and frontend templates/*.html into a consistent, deployable JobBoard application codebase.\n\nTask Details:\n- Read design_spec.md, app.py from BackendDeveloper, and templates/*.html from FrontendDeveloper from CONTEXT\n- Verify and reconcile routing endpoints between app.py and templates to ensure UI and backend linkage matches design_spec.md requirements\n- Check consistency of route names, context variable names, and template references between backend and frontend\n- Merge and refine artifacts to produce final integrated app.py and templates/*.html with coherent interfaces and no mismatch in navigation or data flow\n- Ensure final artifacts are deployable as a unified Flask application\n\n**Integration Checks and Enhancements:**\n- Confirm that all URLs referenced in templates correspond to Flask routes implemented in app.py\n- Ensure context variables passed by backend match placeholders used in templates\n- Resolve any naming conflicts or missing references without adding new requirements beyond design_spec.md\n- Validate that output artifacts preserve all independent workers' functionality consolidated into one consistent system\n\nCRITICAL SUCCESS CRITERIA:\n- Use write_text_file tool to output final app.py and templates/*.html\n- Deliver deploy-ready, fully consistent backend and frontend code\n- Write only final app.py and templates/*.html without refinement markers or extraneous files\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"BackendDeveloper\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"FrontendDeveloper\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"BackendDeveloper\",\n            \"reviewer_agent\": \"IntegrationMerger\",\n            \"review_criteria\": \"Check backend implementation correctness, route completeness, compliance with design_spec.md, and data management accuracy.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        },\n        {\n            \"source_agent\": \"FrontendDeveloper\",\n            \"reviewer_agent\": \"IntegrationMerger\",\n            \"review_criteria\": \"Verify frontend templates match design_spec.md element IDs, page structure, and navigation requirements.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ]\n): pass",
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
    "BackendDesignArchitect": {
        "prompt": (
            """You are a Software Architect specializing in Flask backend applications using Python.

Your goal is to design the backend architecture of the JobBoard web application, producing a comprehensive design document independent of frontend specifications.

Task Details:
- Read user_task_description from CONTEXT
- Produce backend_design.md specifying Flask route handlers, data schemas for local text files, and business logic
- Do not read or assume frontend_design.md

**Backend Routes and Handlers**
- Specify each route path, HTTP methods, and handler function names
- Define required request parameters and form fields
- Outline response behavior including redirects and template rendering
- Include routes for Dashboard, Job Listings, Job Details, Application Form, Application Tracking, Companies Directory, Company Profile, Resume Management, and Search Results
- Specify navigation-related routes triggered by buttons with IDs like browse-jobs-button, companies-button, etc.

**Data Storage Specifications**
- Define schemas matching jobs.txt, companies.txt, categories.txt, applications.txt, resumes.txt, and job_categories.txt formats
- Include field order, delimiter ('|'), data types, and example rows
- Specify business logic connecting routes with data file read/write operations

**Business Logic and Workflow**
- Outline logic for job filtering, searching, application submissions, resume handling, and application status tracking
- Detail how data consistency is maintained without authentication
- Specify error handling and validation requirements

CRITICAL SUCCESS CRITERIA:
- MUST use write_text_file tool to output backend_design.md
- Produced design must fully cover backend routes and data schemas per user_task_description
- Design must be independent from frontend_design.md and not reference or require it for completeness

Output: backend_design.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'backend_design.md'}],

    },

    "FrontendDesignArchitect": {
        "prompt": (
            """You are a UI/UX Designer specializing in HTML layouts and user interface design for Flask web applications.

Your goal is to design the complete frontend layout and templates for the JobBoard web application, independently from backend design.

Task Details:
- Read user_task_description from CONTEXT
- Produce frontend_design.md specifying HTML templates, element IDs, page structures, and UI navigation flows
- Do not read or assume backend_design.md

**Page Templates and Element IDs**
- Define each of the nine pages with page titles and container divs as specified
- Specify all element IDs with types and their roles within each page, e.g., buttons, tables, inputs, dropdowns
- Include dynamic IDs where applicable (e.g., view-job-button-{job_id})

**Navigation and Interaction Flow**
- Map navigation buttons to target pages
- Describe layout structure: div nesting, sections per page, and tab components for Search Results
- Ensure UI elements match data interactions from user requirements

**Accessibility and Usability**
- Specify consistent naming conventions for element IDs
- Ensure clear separation of interactive controls and data display areas
- Outline any necessary UI states (empty results, filtered views)

CRITICAL SUCCESS CRITERIA:
- MUST use write_text_file tool to output frontend_design.md
- Designs must reflect all pages and UI elements exactly as per user_task_description
- Design must be independent from backend_design.md and sufficient for frontend implementation

Output: frontend_design.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'frontend_design.md'}],

    },

    "DesignMerger": {
        "prompt": (
            """You are a Systems Architect specializing in full-stack Flask web application design integration.

Your goal is to merge backend_design.md and frontend_design.md into one consistent design_spec.md without adding new requirements, ensuring alignment with user_task_description.

Task Details:
- Read user_task_description, backend_design.md, and frontend_design.md from CONTEXT
- Validate completeness and consistency across backend routes, data schemas, and frontend templates with element IDs
- Reconcile any discrepancies and unify naming conventions for seamless implementation

**Integration Strategy**
- Section 1: Backend Routes and Data Schemas
  - Consolidate all Flask routes and corresponding data file schemas
  - Maintain completeness and business logic from backend_design.md

- Section 2: Frontend Templates and UI Elements
  - Incorporate all page templates, element IDs, and navigation flows from frontend_design.md
  - Align button IDs and navigation references with backend routes

- Section 3: Consistency and Completeness Checks
  - Ensure all elements used in frontend templates have backend support
  - Confirm all backend routes serving UI pages correspond to frontend pages and controls
  - Resolve conflicting or missing references without adding new features

CRITICAL SUCCESS CRITERIA:
- MUST use write_text_file tool to output design_spec.md
- Final design_spec.md must be a coherent specification enabling independent full-stack development
- Do not modify or invent artifacts beyond the inputs; preserve all declared output artifact names

Output: design_spec.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'backend_design.md', 'source': 'BackendDesignArchitect'}, {'type': 'text_file', 'name': 'frontend_design.md', 'source': 'FrontendDesignArchitect'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_spec.md'}],

    },

    "BackendDeveloper": {
        "prompt": (
            """You are a Backend Developer specializing in Flask web applications using local text-file data management.

Your goal is to implement the complete Flask backend for the JobBoard application according to the provided design_spec.md.

Task Details:
- Read design_spec.md from CONTEXT for detailed route specifications, data schemas, and business logic
- Independently develop app.py implementing all specified routes, request handlers, and data persistence using local text files
- Write complete app.py output artifact with all backend logic, including data loading/saving for jobs.txt, companies.txt, categories.txt, applications.txt, resumes.txt, and job_categories.txt
- Do not read or depend on frontend templates during implementation

**Implementation Requirements:**
- Implement each Flask route as specified with correct URL endpoints, HTTP methods, and response structures
- Load and save data exclusively from/to the given localized text files with their specified formats
- Include validation, error handling, and business logic to manage job listings, applications, resumes, and company profiles
- Use Python-standard idiomatic patterns for file I/O and Flask routing

**Data Management:**
- Adhere strictly to the data file formats and field orders given in design_spec.md without inventing fields
- Handle all CRUD operations required by the application on those text files

CRITICAL SUCCESS CRITERIA:
- Use write_text_file tool to output app.py
- Fully implement all backend features and routes defined only by design_spec.md
- The backend app.py is independently runnable and complete without frontend assumptions

Output: app.py"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}],

    },

    "FrontendDeveloper": {
        "prompt": (
            """You are a Frontend Developer specializing in HTML and Jinja2 templates for Flask applications.

Your goal is to develop the complete set of HTML templates (*.html) for the JobBoard web app as specified in design_spec.md.

Task Details:
- Read design_spec.md from CONTEXT for page layouts, element IDs, template names, and navigation structure
- Independently create all frontend templates covering all JobBoard pages and UI elements, following exact element ID conventions
- Produce templates/*.html output artifact containing all required templates for dashboard, listings, job details, application form, tracking, companies, company profile, resumes, and search results
- Do not read or rely on backend app.py during template creation

**Template Specifications:**
- Each page template must include all specified element IDs with correct HTML tags (div, input, button, table, etc.) as per design_spec.md
- Implement template inheritance and layout reuse where appropriate
- Navigation and buttons must correspond exactly with route names expected from backend specification

**UI Consistency:**
- Ensure UI elements reflect data context variables for dynamic content rendering
- Use standard semantic HTML structures and accessible attributes

CRITICAL SUCCESS CRITERIA:
- Use write_text_file tool to output templates/*.html
- Templates fully comply with design_spec.md element IDs, page structure, and navigation
- Templates are complete and independently implementable without backend code assumptions

Output: templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'templates/*.html'}],

    },

    "IntegrationMerger": {
        "prompt": (
            """You are a Software Integration Engineer specializing in merging backend and frontend components for Flask web applications.

Your goal is to integrate the backend app.py and frontend templates/*.html into a consistent, deployable JobBoard application codebase.

Task Details:
- Read design_spec.md, app.py from BackendDeveloper, and templates/*.html from FrontendDeveloper from CONTEXT
- Verify and reconcile routing endpoints between app.py and templates to ensure UI and backend linkage matches design_spec.md requirements
- Check consistency of route names, context variable names, and template references between backend and frontend
- Merge and refine artifacts to produce final integrated app.py and templates/*.html with coherent interfaces and no mismatch in navigation or data flow
- Ensure final artifacts are deployable as a unified Flask application

**Integration Checks and Enhancements:**
- Confirm that all URLs referenced in templates correspond to Flask routes implemented in app.py
- Ensure context variables passed by backend match placeholders used in templates
- Resolve any naming conflicts or missing references without adding new requirements beyond design_spec.md
- Validate that output artifacts preserve all independent workers' functionality consolidated into one consistent system

CRITICAL SUCCESS CRITERIA:
- Use write_text_file tool to output final app.py and templates/*.html
- Deliver deploy-ready, fully consistent backend and frontend code
- Write only final app.py and templates/*.html without refinement markers or extraneous files

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
        ("DesignMerger", """Verify completeness and correctness of backend routes, data schemas, and business logic for JobBoard functionality.""", [{'type': 'text_file', 'name': 'backend_design.md'}])
    ],

    'FrontendDesignArchitect': [
        ("DesignMerger", """Verify frontend page designs and element IDs match user requirements and complement the backend architecture.""", [{'type': 'text_file', 'name': 'frontend_design.md'}])
    ],

    'BackendDeveloper': [
        ("IntegrationMerger", """Check backend implementation correctness, route completeness, compliance with design_spec.md, and data management accuracy.""", [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'design_spec.md'}])
    ],

    'FrontendDeveloper': [
        ("IntegrationMerger", """Verify frontend templates match design_spec.md element IDs, page structure, and navigation requirements.""", [{'type': 'text_file', 'name': 'templates/*.html'}, {'type': 'text_file', 'name': 'design_spec.md'}])
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
        max_retries=2,
        timeout_threshold=300,
        failure_threshold=1,
        recovery_time=30
    )

    # Parallel execution of backend and frontend design
    await asyncio.gather(
        execute(BackendDesignArchitect, "Produce backend_design.md specifying Flask routes, data schemas, and business logic for JobBoard backend."),
        execute(FrontendDesignArchitect, "Produce frontend_design.md specifying HTML templates, element IDs, page structures, and UI navigation flows for JobBoard frontend.")
    )

    # Read generated backend and frontend design files
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

    # Merge backend and frontend designs into unified design_spec.md ensuring consistency
    await execute(
        DesignMerger,
        f"Merge backend_design.md and frontend_design.md into a unified design_spec.md ensuring consistency and alignment with user_task_description.\n\n"
        f"=== backend_design.md ===\n{backend_design_content}\n\n"
        f"=== frontend_design.md ===\n{frontend_design_content}"
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
        timeout_threshold=450,
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
        timeout_threshold=450,
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
        timeout_threshold=400,
        failure_threshold=2,
        recovery_time=60
    )

    # Parallel implementation by BackendDeveloper and FrontendDeveloper
    await asyncio.gather(
        execute(BackendDeveloper, "Implement complete backend app.py according to design_spec.md, with all routes and data file management."),
        execute(FrontendDeveloper, "Implement complete frontend templates/*.html according to design_spec.md, following all page structures and element IDs.")
    )

    # Read produced artifacts for integration
    app_py_content = ""
    templates_content = ""
    try:
        app_py_content = open("app.py").read()
    except FileNotFoundError:
        pass
    for template_path in sorted(glob.glob("templates/*.html")):
        try:
            templates_content += f"\n=== {template_path} ===\n" + open(template_path).read()
        except OSError:
            pass

    # IntegrationMerger merges backend and frontend into final deployable artifacts
    await execute(
        IntegrationMerger,
        f"Integrate backend app.py and frontend templates/*.html for final deployable JobBoard application.\n\n"
        f"=== design_spec.md ===\n{CONTEXT.get('design_spec.md','')}\n\n"
        f"=== Backend app.py ===\n{app_py_content}\n\n"
        f"=== Frontend Templates ===\n{templates_content}"
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
