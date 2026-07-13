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
# 20260714_001749_748773/main_20260714_001749_748773.py

# Phase_info dictionary containing complete def blocks for failover context
Phase_info = {
    "phase1": "def design_specification_phase(\n    goal: str = \"Refine the comprehensive Python web application design contract for JobBoard covering all 9 pages, data structures, navigation, and exact element IDs; deliver design_spec.md and gated design_feedback.md\",\n    collab_pattern_name: str = \"Refinement Loop\",\n    collab_pattern_description: str = \"DesignGenerator drafts design_spec.md consolidating user requirements; DesignCritic reviews and writes design_feedback.md with approval or requests modification.\",\n    team: list = [\n        {\n            \"agent_name\": \"DesignGenerator\",\n            \"prompt\": \"\"\"You are a Software Architect specializing in Python web application design specifications.\n\nYour goal is to generate or revise the comprehensive design_spec.md for the JobBoard application, incorporating user requirements and prior feedback, for at most two iterations.\n\nTask Details:\n- Read user_task_description, current design_spec.md and design_feedback.md from CONTEXT\n- On first iteration, produce complete design_spec.md covering all pages, element IDs, navigation flow, and data storage formats\n- If design_feedback.md starts with NEED_MODIFY, incorporate all correction requests and rewrite entire design_spec.md accordingly\n- Stop iterating if feedback begins with [APPROVED]\n\n**Section 1: Page Layouts and Element IDs**\n- Specify detailed layouts for all 9 pages, including exact element IDs, types, and purposes\n- Include page titles and structural hierarchy for container elements\n\n**Section 2: Navigation and Interaction Flow**\n- Define navigation paths between pages using button IDs and expected user actions\n- Capture any dynamic elements such as job or application ID-based buttons with their ID patterns\n\n**Section 3: Data Storage Schemas**\n- Describe the local text file formats with exact field orders, delimiters, and example data lines\n- Cover all declared data files: jobs.txt, companies.txt, categories.txt, applications.txt, resumes.txt, job_categories.txt\n\nCRITICAL SUCCESS CRITERIA:\n- Use write_text_file tool to output the full design_spec.md file\n- Preserve the exact input and output artifact names\n- Apply every supported correction when feedback begins NEED_MODIFY and rewrite design_spec.md fully\n- Limit iterations to two; stop immediately upon [APPROVED] feedback\n\nOutput: design_spec.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"design_feedback.md\", \"source\": \"DesignCritic\"}\n            ],\n            \"output_artifacts\": [{\"type\": \"text_file\", \"name\": \"design_spec.md\"}]\n        },\n        {\n            \"agent_name\": \"DesignCritic\",\n            \"prompt\": \"\"\"You are a Design Reviewer specializing in Python web application design specifications.\n\nYour goal is to review the design_spec.md artifact for completeness, correctness, and alignment with user_task_description, then provide gated feedback in design_feedback.md for at most two iterations.\n\nTask Details:\n- Read user_task_description and design_spec.md from CONTEXT\n- Verify each of the 9 pages is fully specified with correct element IDs and page titles\n- Confirm navigation flows match the described buttons and ID patterns exactly\n- Check all data storage files are defined with exact format, field order, delimiters, and sample entries\n- Provide feedback starting exactly with [APPROVED] if fully compliant, or NEED_MODIFY followed by detailed correction list\n- Do not add requirements beyond user_task_description\n\nReview Criteria:\n1. All pages have required containers and elements with specified IDs as per user requirements\n2. Navigation uses the declared button IDs and expected page transitions consistently\n3. Data files conform to declared text formats and examples strictly\n4. No missing or extra features beyond user scope\n5. Feedback file design_feedback.md includes no extra heading or prefix before [APPROVED] or NEED_MODIFY marker\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to output design_feedback.md with the exact feedback status marker at byte 1\n- Limit review to two iterations; stop immediately on [APPROVED]\n\nOutput: design_feedback.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignGenerator\"}\n            ],\n            \"output_artifacts\": [{\"type\": \"text_file\", \"name\": \"design_feedback.md\"}]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"DesignGenerator\",\n            \"reviewer_agent\": \"DesignCritic\",\n            \"review_criteria\": \"Verify design_spec.md completeness, correctness of page elements, data file consistency, navigation flow, and compliance with user requirements without adding new features.\",\n            \"review_artifacts\": [{\"type\": \"text_file\", \"name\": \"design_spec.md\"}]\n        }\n    ]\n): pass",
    "phase2": "def implementation_and_verification_phase(\n    goal: str = \"Refine the complete Python web app implementation and verification for JobBoard, producing app.py, templates/*.html, and gated code_feedback.md for at most two iterations\",\n    collab_pattern_name: str = \"Refinement Loop\",\n    collab_pattern_description: str = \"AppGenerator writes or revises app.py and templates/*.html based on design_spec.md and previous code_feedback.md; CodeCritic performs technical and functional review producing code_feedback.md with [APPROVED] or NEED_MODIFY.\",\n    team: list = [\n        {\n            \"agent_name\": \"AppGenerator\",\n            \"prompt\": \"\"\"You are a Python Web Developer specializing in complete web application implementations using Flask or similar Python frameworks.\n\nYour goal is to write or completely revise the full JobBoard Python web application source code (app.py) and all HTML templates (templates/*.html) consistent with design specifications and prior feedback, for at most two refinement iterations.\n\nTask Details:\n- Read design_spec.md, the current app.py, existing templates/*.html, and code_feedback.md from CONTEXT\n- On first iteration, implement a complete JobBoard app.py and all required HTML templates with exact page structures, element IDs, navigation buttons, and local text file data management as per design_spec.md\n- On feedback starting with NEED_MODIFY, apply all requested corrections and overwrite entire app.py and templates/*.html\n- When feedback starts with [APPROVED], preserve the approved code and templates\n\n**Section 1: Python Web Application Implementation**\n- Implement app.py with all routes, handlers, and logic for the 9 pages as described\n- Integrate local text file read/write for all data files: jobs.txt, companies.txt, categories.txt, applications.txt, resumes.txt, job_categories.txt\n- Implement navigation flows exactly matching page buttons and IDs from the specification\n- Manage data filtering, search, display, detailed views, application submission, and resume management as described\n\n**Section 2: HTML Template Structure**\n- Create templates for all 9 pages containing all required element IDs exactly as specified (e.g., dashboard-page, featured-jobs, browse-jobs-button, etc.)\n- Use proper HTML elements for each UI component (divs, buttons, inputs, tables, dropdowns) with correct IDs\n- Ensure templates render dynamic content consistent with backend-provided context data\n\n**Section 3: Integration and Consistency**\n- Ensure all backend route handlers render the correct templates with proper context variables\n- Ensure all page navigation buttons link to correct routes\n- Synchronize element IDs and data references exactly as specified to enable correct frontend-backend interaction\n\nCRITICAL REQUIREMENTS:\n- Run at most two iterations of refinement with CodeCritic feedback consumption; stop immediately on approval\n- Must use write_text_file tool to output complete app.py and the directory of templates/*.html files\n- Produce full complete rewritten artifacts on NEED_MODIFY feedback, no partial edits or incremental changes\n- Exactly follow the data storage formats and example data given for local text file management\n- Preserve all page structure and element ID exactness as specified for full UI compliance\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"AppGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"AppGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"code_feedback.md\", \"source\": \"CodeCritic\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        },\n        {\n            \"agent_name\": \"CodeCritic\",\n            \"prompt\": \"\"\"You are a Software Test Engineer specializing in Python web application code and template review.\n\nYour goal is to perform thorough code review of the JobBoard app.py and HTML templates against the design_spec.md and produce precise, actionable gated feedback with either [APPROVED] or NEED_MODIFY for at most two iterations.\n\nTask Details:\n- Read design_spec.md, app.py, and templates/*.html from CONTEXT\n- Validate app.py correctness including route handlers, data file usage, local text file read/write correctness, and overall functionality\n- Validate templates/*.html structure and correct element IDs for all 9 pages as specified\n- Check navigation flow correctness including all buttons and links as per spec\n- Assess code quality, syntax, and runtime viability using validate_python_file tool\n- Write code_feedback.md starting exactly with either [APPROVED] if all criteria are met, or NEED_MODIFY followed by detailed required corrections otherwise\n\nReview Criteria:\n1. Confirm all pages (Dashboard, Job Listings, Job Details, Application Form, Application Tracking, Companies Directory, Company Profile, Resume Management, Search Results) have exact element IDs as specified\n2. Confirm all navigation buttons perform correct routing actions matching user task navigation paths\n3. Confirm all local data file interactions fully comply with specified file formats and example data\n4. Confirm no deviations from design_spec.md in UI structure or backend logic\n5. Confirm app.py passes syntax and runtime validation via validate_python_file\n6. Ensure complete, clear, and minimal feedback focusing strictly on missing or incorrect elements, logic errors, code or template defects\n\nCRITICAL REQUIREMENTS:\n- The first bytes of code_feedback.md MUST be exactly [APPROVED] or NEED_MODIFY\n- No extra whitespace, headings, or prefixes before this marker\n- Use write_text_file to save the entire feedback file\n- Use validate_python_file tool to verify app.py correctness before writing feedback\n- Provide consistent and reproducible feedback enabling AppGenerator to fully revise correctly\n\nOutput: code_feedback.md\"\"\",\n            \"tools\": [\"write_text_file\", \"validate_python_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"AppGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"AppGenerator\"}\n            ],\n            \"output_artifacts\": [{\"type\": \"text_file\", \"name\": \"code_feedback.md\"}]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"AppGenerator\",\n            \"reviewer_agent\": \"CodeCritic\",\n            \"review_criteria\": \"Validate conformance to design_spec.md, page element correctness including all 9 pages with exact IDs, navigation flow, data file usage per specs, and code syntax/quality.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ]\n): pass",
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
    "DesignGenerator": {
        "prompt": (
            """You are a Software Architect specializing in Python web application design specifications.

Your goal is to generate or revise the comprehensive design_spec.md for the JobBoard application, incorporating user requirements and prior feedback, for at most two iterations.

Task Details:
- Read user_task_description, current design_spec.md and design_feedback.md from CONTEXT
- On first iteration, produce complete design_spec.md covering all pages, element IDs, navigation flow, and data storage formats
- If design_feedback.md starts with NEED_MODIFY, incorporate all correction requests and rewrite entire design_spec.md accordingly
- Stop iterating if feedback begins with [APPROVED]

**Section 1: Page Layouts and Element IDs**
- Specify detailed layouts for all 9 pages, including exact element IDs, types, and purposes
- Include page titles and structural hierarchy for container elements

**Section 2: Navigation and Interaction Flow**
- Define navigation paths between pages using button IDs and expected user actions
- Capture any dynamic elements such as job or application ID-based buttons with their ID patterns

**Section 3: Data Storage Schemas**
- Describe the local text file formats with exact field orders, delimiters, and example data lines
- Cover all declared data files: jobs.txt, companies.txt, categories.txt, applications.txt, resumes.txt, job_categories.txt

CRITICAL SUCCESS CRITERIA:
- Use write_text_file tool to output the full design_spec.md file
- Preserve the exact input and output artifact names
- Apply every supported correction when feedback begins NEED_MODIFY and rewrite design_spec.md fully
- Limit iterations to two; stop immediately upon [APPROVED] feedback

Output: design_spec.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignGenerator'}, {'type': 'text_file', 'name': 'design_feedback.md', 'source': 'DesignCritic'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_spec.md'}],

    },

    "DesignCritic": {
        "prompt": (
            """You are a Design Reviewer specializing in Python web application design specifications.

Your goal is to review the design_spec.md artifact for completeness, correctness, and alignment with user_task_description, then provide gated feedback in design_feedback.md for at most two iterations.

Task Details:
- Read user_task_description and design_spec.md from CONTEXT
- Verify each of the 9 pages is fully specified with correct element IDs and page titles
- Confirm navigation flows match the described buttons and ID patterns exactly
- Check all data storage files are defined with exact format, field order, delimiters, and sample entries
- Provide feedback starting exactly with [APPROVED] if fully compliant, or NEED_MODIFY followed by detailed correction list
- Do not add requirements beyond user_task_description

Review Criteria:
1. All pages have required containers and elements with specified IDs as per user requirements
2. Navigation uses the declared button IDs and expected page transitions consistently
3. Data files conform to declared text formats and examples strictly
4. No missing or extra features beyond user scope
5. Feedback file design_feedback.md includes no extra heading or prefix before [APPROVED] or NEED_MODIFY marker

CRITICAL REQUIREMENTS:
- Use write_text_file tool to output design_feedback.md with the exact feedback status marker at byte 1
- Limit review to two iterations; stop immediately on [APPROVED]

Output: design_feedback.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignGenerator'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_feedback.md'}],

    },

    "AppGenerator": {
        "prompt": (
            """You are a Python Web Developer specializing in complete web application implementations using Flask or similar Python frameworks.

Your goal is to write or completely revise the full JobBoard Python web application source code (app.py) and all HTML templates (templates/*.html) consistent with design specifications and prior feedback, for at most two refinement iterations.

Task Details:
- Read design_spec.md, the current app.py, existing templates/*.html, and code_feedback.md from CONTEXT
- On first iteration, implement a complete JobBoard app.py and all required HTML templates with exact page structures, element IDs, navigation buttons, and local text file data management as per design_spec.md
- On feedback starting with NEED_MODIFY, apply all requested corrections and overwrite entire app.py and templates/*.html
- When feedback starts with [APPROVED], preserve the approved code and templates

**Section 1: Python Web Application Implementation**
- Implement app.py with all routes, handlers, and logic for the 9 pages as described
- Integrate local text file read/write for all data files: jobs.txt, companies.txt, categories.txt, applications.txt, resumes.txt, job_categories.txt
- Implement navigation flows exactly matching page buttons and IDs from the specification
- Manage data filtering, search, display, detailed views, application submission, and resume management as described

**Section 2: HTML Template Structure**
- Create templates for all 9 pages containing all required element IDs exactly as specified (e.g., dashboard-page, featured-jobs, browse-jobs-button, etc.)
- Use proper HTML elements for each UI component (divs, buttons, inputs, tables, dropdowns) with correct IDs
- Ensure templates render dynamic content consistent with backend-provided context data

**Section 3: Integration and Consistency**
- Ensure all backend route handlers render the correct templates with proper context variables
- Ensure all page navigation buttons link to correct routes
- Synchronize element IDs and data references exactly as specified to enable correct frontend-backend interaction

CRITICAL REQUIREMENTS:
- Run at most two iterations of refinement with CodeCritic feedback consumption; stop immediately on approval
- Must use write_text_file tool to output complete app.py and the directory of templates/*.html files
- Produce full complete rewritten artifacts on NEED_MODIFY feedback, no partial edits or incremental changes
- Exactly follow the data storage formats and example data given for local text file management
- Preserve all page structure and element ID exactness as specified for full UI compliance

Output: app.py, templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignGenerator'}, {'type': 'text_file', 'name': 'app.py', 'source': 'AppGenerator'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'AppGenerator'}, {'type': 'text_file', 'name': 'code_feedback.md', 'source': 'CodeCritic'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}],

    },

    "CodeCritic": {
        "prompt": (
            """You are a Software Test Engineer specializing in Python web application code and template review.

Your goal is to perform thorough code review of the JobBoard app.py and HTML templates against the design_spec.md and produce precise, actionable gated feedback with either [APPROVED] or NEED_MODIFY for at most two iterations.

Task Details:
- Read design_spec.md, app.py, and templates/*.html from CONTEXT
- Validate app.py correctness including route handlers, data file usage, local text file read/write correctness, and overall functionality
- Validate templates/*.html structure and correct element IDs for all 9 pages as specified
- Check navigation flow correctness including all buttons and links as per spec
- Assess code quality, syntax, and runtime viability using validate_python_file tool
- Write code_feedback.md starting exactly with either [APPROVED] if all criteria are met, or NEED_MODIFY followed by detailed required corrections otherwise

Review Criteria:
1. Confirm all pages (Dashboard, Job Listings, Job Details, Application Form, Application Tracking, Companies Directory, Company Profile, Resume Management, Search Results) have exact element IDs as specified
2. Confirm all navigation buttons perform correct routing actions matching user task navigation paths
3. Confirm all local data file interactions fully comply with specified file formats and example data
4. Confirm no deviations from design_spec.md in UI structure or backend logic
5. Confirm app.py passes syntax and runtime validation via validate_python_file
6. Ensure complete, clear, and minimal feedback focusing strictly on missing or incorrect elements, logic errors, code or template defects

CRITICAL REQUIREMENTS:
- The first bytes of code_feedback.md MUST be exactly [APPROVED] or NEED_MODIFY
- No extra whitespace, headings, or prefixes before this marker
- Use write_text_file to save the entire feedback file
- Use validate_python_file tool to verify app.py correctness before writing feedback
- Provide consistent and reproducible feedback enabling AppGenerator to fully revise correctly

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
        ("DesignCritic", """Verify design_spec.md completeness, correctness of page elements, data file consistency, navigation flow, and compliance with user requirements without adding new features.""", [{'type': 'text_file', 'name': 'design_spec.md'}])
    ],

    'AppGenerator': [
        ("CodeCritic", """Validate conformance to design_spec.md, page element correctness including all 9 pages with exact IDs, navigation flow, data file usage per specs, and code syntax/quality.""", [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}])
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
    DesignGenerator = build_resilient_agent(
        chaos_controller=chaos_controller,
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
        chaos_controller=chaos_controller,
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
            "Generate or revise the complete design_spec.md for the JobBoard application.\n\n"
            f"=== Current design_spec.md ===\n{current_design}\n\n"
            f"=== DesignCritic Feedback ===\n{feedback_content}"
        )

        try:
            current_design = open("design_spec.md").read()
        except FileNotFoundError:
            current_design = ""

        await execute(
            DesignCritic,
            "Review the latest design_spec.md against user_task_description for completeness, correctness, and compliance.\n"
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
import glob

async def implementation_and_verification_phase():
    AppGenerator = build_resilient_agent(
        chaos_controller=chaos_controller,
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
        chaos_controller=chaos_controller,
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
            "Create or revise the complete JobBoard app.py and all templates/*.html.\n\n"
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
            "Write code_feedback.md starting exactly with [APPROVED] or NEED_MODIFY describing all issues or approval.\n\n"
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
