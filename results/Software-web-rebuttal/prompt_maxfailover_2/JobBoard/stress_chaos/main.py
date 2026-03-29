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
    "phase1": "def architecture_design_phase(\n    goal: str = \"Create a detailed design specification for the JobBoard web app including Flask routes, HTML templates, and data schemas to guide parallel development\",\n    collab_pattern_name: str = \"Sequential Flow\",\n    collab_pattern_description: str = (\n        \"SystemArchitect drafts design_spec.md covering 3 sections: Flask routes with function names, context variables, HTTP methods; HTML templates with exact element IDs and navigation mappings; Data schemas with field orders and file formats.\"\n    ),\n    team: [\n        {\n            \"agent_name\": \"SystemArchitect\",\n            \"prompt\": \"\"\"You are a System Architect specializing in Flask web application design specifications.\n\nYour goal is to produce a comprehensive design specification document that enables Backend and Frontend developers to develop the JobBoard web application independently and in parallel.\n\nTask Details:\n- Read user_task_description from CONTEXT thoroughly to understand all required pages, their elements, and data storage schemas.\n- Create design_spec.md containing three detailed sections: Flask routes, HTML templates, and data file schemas.\n- Include complete specifications that allow backend developers to implement all Flask routes with correct function names, HTTP methods, template references, and context variables.\n- Include all frontend template details with exact element IDs, page titles, context variables, and navigation mappings using url_for functions.\n- Specify all data files with exact pipe-delimited field orders, descriptions, and realistic example data matching user requirements.\n- Do NOT omit or assume any information; provide precise, exhaustive, and consistent documentation.\n\n**Section 1: Flask Routes Specification**\n\n- List all routes required for JobBoard app covering dashboard, job listings, job details, application forms, tracking, companies, company profiles, resumes, and search results.\n- For each route, specify:\n  - Route path (e.g., /dashboard, /jobs, /job/<int:job_id>)\n  - Function name (snake_case, descriptive)\n  - HTTP method(s) allowed (GET, POST)\n  - Template file rendered (e.g., dashboard.html)\n  - Context variables passed to templates with exact names and types (list, dict, str, int, etc.)\n- The root '/' MUST redirect to the dashboard page.\n- Define clear input expectations for POST routes (e.g., form fields for application submissions).\n- Emphasize matching names exactly across all sections.\n\n**Section 2: HTML Template Specifications**\n\n- For each required page template, specify:\n  - Filename (templates/{name}.html)\n  - Exact Page Title (used in <title> and <h1>)\n  - Complete list of element IDs with element types and descriptions, including dynamic IDs using Jinja2 syntax.\n  - Context variables available in the template, with detailed structures (list of dict, fields).\n  - Navigation mappings for all buttons and links using url_for syntax referring to Flask function names.\n- Include examples for static and dynamic IDs, e.g.:\n  - Static ID: browse-jobs-button\n  - Dynamic ID: view-job-button-{{ job.job_id }}\n- Do NOT assume or omit any element IDs or context variables.\n\n**Section 3: Data File Schemas**\n\n- For each data file defined in the user task (jobs.txt, companies.txt, etc.), specify:\n  - File path in data/ directory\n  - Pipe-delimited field order with exact field names\n  - Description of the data each file stores\n  - Provide 2-3 realistic example rows matching user task data\n- Ensure field orders and names match exactly the given format in the requirements.\n- Reinforce that files have NO header lines; parsing starts from the first line.\n\nCRITICAL SUCCESS CRITERIA:\n- The design_spec.md must enable backend developers to implement ALL Flask routes, load data exactly as specified, handle form POST requests, and pass all review criteria.\n- Frontend developers must be able to implement ALL templates with EXACT element IDs, context variables, and navigation purely from the specification.\n- No discrepancies between sections (e.g., function names, variable names must match).\n- Use write_text_file tool to produce design_spec.md in markdown format.\n- Do NOT include any implementation code in this document—only detailed specifications.\n- Follow strict pipe-delimited format for data schemas and provide example rows.\n\nOutput: design_spec.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ],\n    review_policy: [\n        {\n            \"source_agent\": \"SystemArchitect\",\n            \"reviewer_agent\": \"BackendDeveloper\",\n            \"review_criteria\": (\n                \"Verify backend sections of design_spec.md: all Flask routes including dashboard, job listings, applications, companies, jobs, resumes, and search pages are specified with function names, methods, and context variables; data schemas for jobs, companies, categories, applications, resumes, and mappings match example formats exactly.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        },\n        {\n            \"source_agent\": \"SystemArchitect\",\n            \"reviewer_agent\": \"FrontendDeveloper\",\n            \"review_criteria\": (\n                \"Verify frontend sections of design_spec.md: all HTML templates for dashboard, listings, job details, application form, tracking, companies, company profile, resumes, and search results specify exact element IDs, context variables, navigation mappings with url_for functions, and page titles.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ]\n): pass",
    "phase2": "def parallel_implementation_phase(\n    goal: str = \"Implement backend and frontend components in parallel based on design_spec.md specifications\",\n    collab_pattern_name: str = \"Parallel Flow\",\n    collab_pattern_description: str = (\n        \"BackendDeveloper implements app.py with Flask routes, data loading/saving, and functionality using design_spec.md Sections 1 and 3; FrontendDeveloper implements all HTML templates for each page using design_spec.md Section 2; both work concurrently and independently.\"\n    ),\n    team: [\n        {\n            \"agent_name\": \"BackendDeveloper\",\n            \"prompt\": \"\"\"You are a Backend Developer specializing in Flask web applications.\n\nYour goal is to implement complete Flask backend components with all routes, data handling, and business logic based on the provided design specifications.\n\nTask Details:\n- Read design_spec.md Sections 1 (Flask Routes) and 3 (Data Schemas) ONLY from CONTEXT\n- Implement complete app.py with all Flask routes specified in Section 1\n- Load and save data using the exact field orders and pipe-delimited formats defined in Section 3 for all relevant text files in data/\n- Implement root '/' route to redirect to dashboard page as specified\n- DO NOT read or modify any frontend templates or Section 2 content\n- DO NOT assume any fields or routes beyond those in Sections 1 and 3\n\nImplementation Requirements:\n1. **Flask Application Setup**:\n   ```python\n   from flask import Flask, render_template, redirect, url_for, request\n   app = Flask(__name__)\n   app.config['SECRET_KEY'] = 'dev-secret-key'\n   ```\n\n2. **Routing and Views**:\n   - Implement all routes exactly as defined in Section 1\n   - Use function names and route paths exactly as specified\n   - Use render_template() with templates named per Section 1\n   - Pass context variables with exact names and data types specified\n   - For POST requests, handle form data correctly using request.form\n\n3. **Data Handling**:\n   - Read data files from data/ directory with exact pipe-delimited formats\n   - Parse data lines into dictionaries matching specified field orders in Section 3\n   - Handle file I/O robustly with error checking\n   - Save any updated data respecting the same format and encoding\n   - No assumptions about file headers; start parsing from first line\n\n4. **Root Route**:\n   - Implement '/' to redirect to dashboard page using:\n     `return redirect(url_for('dashboard'))`\n\n5. **Code Style and Best Practices**:\n   - Use url_for() for route references\n   - Include `if __name__ == '__main__':` block for standalone runs\n   - Gracefully handle missing or empty data cases\n   - Adhere strictly to the specification without extraneous functionality\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save app.py\n- Ensure function names, route paths, and context variables match design_spec.md exactly\n- Data file parsing and saving must match Section 3 field order and format precisely\n- Do NOT read or use Section 2 (frontend templates) contents in implementation\n- Do NOT add unapproved features or routes beyond design_spec.md Sections 1 and 3\n- Do NOT provide code snippets only in messages; always save full files via write_text_file\n\nOutput: app.py\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"SystemArchitect\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"}\n            ]\n        },\n        {\n            \"agent_name\": \"FrontendDeveloper\",\n            \"prompt\": \"\"\"You are a Frontend Developer specializing in HTML and Jinja2 templating for Flask web applications.\n\nYour goal is to implement all HTML templates for the 'JobBoard' application pages based solely on the provided design specifications.\n\nTask Details:\n- Read design_spec.md Section 2 (HTML Templates) ONLY from CONTEXT\n- Implement all HTML templates for these pages: dashboard, job listings, job details, application form, application tracking, companies directory, company profile, resumes management, and search results\n- Include all required element IDs exactly as specified\n- Implement context variables access as defined, using Jinja2 syntax\n- Respect navigation links using Flask url_for functions exactly as mapped\n- Do NOT read or modify backend code or Sections 1 and 3 content\n\nImplementation Requirements:\n1. **Template Structure**:\n   ```html\n   <!DOCTYPE html>\n   <html lang=\"en\">\n   <head>\n       <meta charset=\"UTF-8\">\n       <title>{{ page_title }}</title>\n   </head>\n   <body>\n       <div id=\"main-content-id\">\n           <h1>{{ page_title }}</h1>\n           <!-- Page specific content -->\n       </div>\n   </body>\n   </html>\n   ```\n\n2. **File Naming**:\n   - Save files under templates/ directory\n   - Use exact filenames specified in Section 2, for example: templates/dashboard.html, templates/listings.html, etc.\n   - One template file per page\n\n3. **Element IDs and Attributes**:\n   - Use exact element IDs as specified (case-sensitive)\n   - For dynamic element IDs, use Jinja2 formatting, e.g. id=\"view-job-button-{{ job.job_id }}\"\n   - Include all required elements (buttons, inputs, divs) on each page exactly as specified\n\n4. **Context Variable Usage**:\n   - Access variables using Jinja2 expressions and control structures\n   - Use loops, conditionals, and filters as needed to render data\n   - Do not introduce variables not specified in design_spec.md\n\n5. **Navigation**:\n   - Implement all navigation links as url_for('function_name') calls exactly as specified\n   - Use anchor tags wrapping buttons or links, for example:\n     ```html\n     <a href=\"{{ url_for('dashboard') }}\">\n         <button id=\"dashboard-button\">Dashboard</button>\n     </a>\n     ```\n   - Ensure dynamic links use variables with correct syntax\n\n6. **Forms and Uploads**:\n   - Implement forms with correct method and action attributes as specified\n   - Use file input fields for resume uploads\n   - Include submit buttons with specified IDs\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save all template files under templates/\n- All element IDs must exactly match design_spec.md Section 2 (no casing or spelling changes)\n- Page titles must match exactly in both <title> and <h1> tags\n- Navigation url_for function names must match design_spec.md exactly\n- Do NOT add templates beyond those specified\n- Do NOT provide code snippets only; always save complete files using write_text_file\n\nOutput: templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"SystemArchitect\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: [\n        {\n            \"source_agent\": \"BackendDeveloper\",\n            \"reviewer_agent\": \"SystemArchitect\",\n            \"review_criteria\": (\n                \"Verify app.py correctness versus design_spec.md: all routes exist, methods and context variables match design; data loading uses correct field order and file formats from design; root route redirects to dashboard.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\"}\n            ]\n        },\n        {\n            \"source_agent\": \"FrontendDeveloper\",\n            \"reviewer_agent\": \"SystemArchitect\",\n            \"review_criteria\": (\n                \"Validate templates/*.html implement all element IDs, context variables, navigation using url_for, and page titles exactly as specified in design_spec.md.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ]\n): pass",
    "phase3": "def integration_testing_phase(\n    goal: str = \"Conduct integration testing of backend and frontend to ensure all pages and functionalities work together seamlessly\",\n    collab_pattern_name: str = \"Refinement Loop\",\n    collab_pattern_description: str = (\n        \"Tester runs end-to-end test cases to validate app.py and templates/*.html integration; Tester writes feedback to feedback.txt for Developer to revise implementation until Tester writes '[APPROVED]' status.\"\n    ),\n    team: [\n        {\n            \"agent_name\": \"Developer\",\n            \"prompt\": \"\"\"You are a Full-Stack Developer with expertise in Python backend and HTML frontend integration.\n\nYour goal is to iteratively improve and fix both backend (app.py) and frontend (templates/*.html) code to ensure full integration and functional correctness as verified by integration tests.\n\nTask Details:\n- Read current app.py and templates/*.html implementations from CONTEXT\n- Read detailed feedback from feedback.txt produced by Tester\n- Apply code improvements and fixes addressing all Tester feedback\n- Do NOT proceed without addressing issues raised in feedback.txt until approval is achieved\n- Produce updated app.py and templates/*.html reflecting required fixes without changing unrelated functionality\n\nDevelopment Process:\n1. Parse feedback.txt carefully, identify all defects and integration issues reported by Tester\n2. Modify backend Python code (app.py) to fix functional errors, data flow issues, and integration points\n3. Modify frontend templates (*.html) to fix rendering, element IDs, context variable usage, and navigation\n4. Maintain consistency with design_spec.md requirements and data schemas\n5. Repeat until Tester writes \"[APPROVED]\" status in feedback.txt\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to output both updated app.py and all modified template files\n- Preserve file naming and structure; update all necessary files only\n- Do NOT introduce new features or remove existing approved functionality\n- Thoroughly address all Tester feedback in each iteration\n- Feedback file presence and content are gating conditions for progress\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"BackendDeveloper\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"FrontendDeveloper\"},\n                {\"type\": \"text_file\", \"name\": \"feedback.txt\", \"source\": \"Tester\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        },\n        {\n            \"agent_name\": \"Tester\",\n            \"prompt\": \"\"\"You are a Software Test Engineer specializing in integration and functional testing of Python web applications with HTML frontends.\n\nYour goal is to rigorously test the integration of backend (app.py) and frontend (templates/*.html) to identify any defects, inconsistencies, or missing functionality, and provide detailed corrective feedback until all tests are passed.\n\nTask Details:\n- Read app.py and all templates/*.html files from CONTEXT\n- Execute thorough integration tests covering all 'JobBoard' features and pages\n- Verify data flow matches design_spec.md expectations and UI elements are present and functional\n- Check navigation, input handling, dynamic content rendering, and file uploads across pages\n- Produce comprehensive feedback.txt with detailed issues, test results, and improvement suggestions\n- Write \"[APPROVED]\" in feedback.txt only when all test cases pass without any issues\n\nTesting Guidelines:\n1. Prepare end-to-end test cases for all nine pages ensuring coverage of navigation and functionalities\n2. Execute tests using execute_python_code tool for backend validation and manual or scripted frontend checks\n3. Confirm output consistency between backend data and frontend rendering\n4. Check that all input_artifacts specifications and output_artifacts contract are honored correctly\n5. Provide clear reproducible feedback items and required fixes with exact references to code or template locations\n\nCRITICAL REQUIREMENTS:\n- Use execute_python_code tool to run and validate backend where applicable\n- Write feedback.txt file with clear markings\n  - Include \"NEED_MODIFY\" marker when defects or missing features found\n  - Replace with \"[APPROVED]\" marker only when all tests pass fully\n- Feedback file content is gating condition for Developer improvements\n- Do NOT approve partial fixes or incomplete functionality\n\nOutput: feedback.txt\"\"\",\n            \"tools\": [\"execute_python_code\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"BackendDeveloper\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"FrontendDeveloper\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"feedback.txt\"}\n            ]\n        }\n    ],\n    review_policy: [\n        {\n            \"source_agent\": \"Developer\",\n            \"reviewer_agent\": \"Tester\",\n            \"review_criteria\": (\n                \"Tester verifies Developer's code revisions based on feedback; Tester ensures fixes are correctly applied for all tested functionalities.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"},\n                {\"type\": \"text_file\", \"name\": \"feedback.txt\"}\n            ]\n        },\n        {\n            \"source_agent\": \"Tester\",\n            \"reviewer_agent\": \"SystemArchitect\",\n            \"review_criteria\": (\n                \"SystemArchitect reviews testing coverage and feedback for completeness and correlation with initial design_spec.md.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"feedback.txt\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ]\n): pass",
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
    "SystemArchitect": {
        "prompt": (
            """You are a System Architect specializing in Flask web application design specifications.

Your goal is to produce a comprehensive design specification document that enables Backend and Frontend developers to develop the JobBoard web application independently and in parallel.

Task Details:
- Read user_task_description from CONTEXT thoroughly to understand all required pages, their elements, and data storage schemas.
- Create design_spec.md containing three detailed sections: Flask routes, HTML templates, and data file schemas.
- Include complete specifications that allow backend developers to implement all Flask routes with correct function names, HTTP methods, template references, and context variables.
- Include all frontend template details with exact element IDs, page titles, context variables, and navigation mappings using url_for functions.
- Specify all data files with exact pipe-delimited field orders, descriptions, and realistic example data matching user requirements.
- Do NOT omit or assume any information; provide precise, exhaustive, and consistent documentation.

**Section 1: Flask Routes Specification**

- List all routes required for JobBoard app covering dashboard, job listings, job details, application forms, tracking, companies, company profiles, resumes, and search results.
- For each route, specify:
  - Route path (e.g., /dashboard, /jobs, /job/<int:job_id>)
  - Function name (snake_case, descriptive)
  - HTTP method(s) allowed (GET, POST)
  - Template file rendered (e.g., dashboard.html)
  - Context variables passed to templates with exact names and types (list, dict, str, int, etc.)
- The root '/' MUST redirect to the dashboard page.
- Define clear input expectations for POST routes (e.g., form fields for application submissions).
- Emphasize matching names exactly across all sections.

**Section 2: HTML Template Specifications**

- For each required page template, specify:
  - Filename (templates/{name}.html)
  - Exact Page Title (used in <title> and <h1>)
  - Complete list of element IDs with element types and descriptions, including dynamic IDs using Jinja2 syntax.
  - Context variables available in the template, with detailed structures (list of dict, fields).
  - Navigation mappings for all buttons and links using url_for syntax referring to Flask function names.
- Include examples for static and dynamic IDs, e.g.:
  - Static ID: browse-jobs-button
  - Dynamic ID: view-job-button-{{ job.job_id }}
- Do NOT assume or omit any element IDs or context variables.

**Section 3: Data File Schemas**

- For each data file defined in the user task (jobs.txt, companies.txt, etc.), specify:
  - File path in data/ directory
  - Pipe-delimited field order with exact field names
  - Description of the data each file stores
  - Provide 2-3 realistic example rows matching user task data
- Ensure field orders and names match exactly the given format in the requirements.
- Reinforce that files have NO header lines; parsing starts from the first line.

CRITICAL SUCCESS CRITERIA:
- The design_spec.md must enable backend developers to implement ALL Flask routes, load data exactly as specified, handle form POST requests, and pass all review criteria.
- Frontend developers must be able to implement ALL templates with EXACT element IDs, context variables, and navigation purely from the specification.
- No discrepancies between sections (e.g., function names, variable names must match).
- Use write_text_file tool to produce design_spec.md in markdown format.
- Do NOT include any implementation code in this document—only detailed specifications.
- Follow strict pipe-delimited format for data schemas and provide example rows.

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

Your goal is to implement complete Flask backend components with all routes, data handling, and business logic based on the provided design specifications.

Task Details:
- Read design_spec.md Sections 1 (Flask Routes) and 3 (Data Schemas) ONLY from CONTEXT
- Implement complete app.py with all Flask routes specified in Section 1
- Load and save data using the exact field orders and pipe-delimited formats defined in Section 3 for all relevant text files in data/
- Implement root '/' route to redirect to dashboard page as specified
- DO NOT read or modify any frontend templates or Section 2 content
- DO NOT assume any fields or routes beyond those in Sections 1 and 3

Implementation Requirements:
1. **Flask Application Setup**:
   ```python
   from flask import Flask, render_template, redirect, url_for, request
   app = Flask(__name__)
   app.config['SECRET_KEY'] = 'dev-secret-key'
   ```

2. **Routing and Views**:
   - Implement all routes exactly as defined in Section 1
   - Use function names and route paths exactly as specified
   - Use render_template() with templates named per Section 1
   - Pass context variables with exact names and data types specified
   - For POST requests, handle form data correctly using request.form

3. **Data Handling**:
   - Read data files from data/ directory with exact pipe-delimited formats
   - Parse data lines into dictionaries matching specified field orders in Section 3
   - Handle file I/O robustly with error checking
   - Save any updated data respecting the same format and encoding
   - No assumptions about file headers; start parsing from first line

4. **Root Route**:
   - Implement '/' to redirect to dashboard page using:
     `return redirect(url_for('dashboard'))`

5. **Code Style and Best Practices**:
   - Use url_for() for route references
   - Include `if __name__ == '__main__':` block for standalone runs
   - Gracefully handle missing or empty data cases
   - Adhere strictly to the specification without extraneous functionality

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save app.py
- Ensure function names, route paths, and context variables match design_spec.md exactly
- Data file parsing and saving must match Section 3 field order and format precisely
- Do NOT read or use Section 2 (frontend templates) contents in implementation
- Do NOT add unapproved features or routes beyond design_spec.md Sections 1 and 3
- Do NOT provide code snippets only in messages; always save full files via write_text_file

Output: app.py"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'SystemArchitect'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}],
    },

    "FrontendDeveloper": {
        "prompt": (
            """You are a Frontend Developer specializing in HTML and Jinja2 templating for Flask web applications.

Your goal is to implement all HTML templates for the 'JobBoard' application pages based solely on the provided design specifications.

Task Details:
- Read design_spec.md Section 2 (HTML Templates) ONLY from CONTEXT
- Implement all HTML templates for these pages: dashboard, job listings, job details, application form, application tracking, companies directory, company profile, resumes management, and search results
- Include all required element IDs exactly as specified
- Implement context variables access as defined, using Jinja2 syntax
- Respect navigation links using Flask url_for functions exactly as mapped
- Do NOT read or modify backend code or Sections 1 and 3 content

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
       <div id="main-content-id">
           <h1>{{ page_title }}</h1>
           <!-- Page specific content -->
       </div>
   </body>
   </html>
   ```

2. **File Naming**:
   - Save files under templates/ directory
   - Use exact filenames specified in Section 2, for example: templates/dashboard.html, templates/listings.html, etc.
   - One template file per page

3. **Element IDs and Attributes**:
   - Use exact element IDs as specified (case-sensitive)
   - For dynamic element IDs, use Jinja2 formatting, e.g. id="view-job-button-{{ job.job_id }}"
   - Include all required elements (buttons, inputs, divs) on each page exactly as specified

4. **Context Variable Usage**:
   - Access variables using Jinja2 expressions and control structures
   - Use loops, conditionals, and filters as needed to render data
   - Do not introduce variables not specified in design_spec.md

5. **Navigation**:
   - Implement all navigation links as url_for('function_name') calls exactly as specified
   - Use anchor tags wrapping buttons or links, for example:
     ```html
     <a href="{{ url_for('dashboard') }}">
         <button id="dashboard-button">Dashboard</button>
     </a>
     ```
   - Ensure dynamic links use variables with correct syntax

6. **Forms and Uploads**:
   - Implement forms with correct method and action attributes as specified
   - Use file input fields for resume uploads
   - Include submit buttons with specified IDs

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save all template files under templates/
- All element IDs must exactly match design_spec.md Section 2 (no casing or spelling changes)
- Page titles must match exactly in both <title> and <h1> tags
- Navigation url_for function names must match design_spec.md exactly
- Do NOT add templates beyond those specified
- Do NOT provide code snippets only; always save complete files using write_text_file

Output: templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'SystemArchitect'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'templates/*.html'}],
    },

    "Developer": {
        "prompt": (
            """You are a Full-Stack Developer with expertise in Python backend and HTML frontend integration.

Your goal is to iteratively improve and fix both backend (app.py) and frontend (templates/*.html) code to ensure full integration and functional correctness as verified by integration tests.

Task Details:
- Read current app.py and templates/*.html implementations from CONTEXT
- Read detailed feedback from feedback.txt produced by Tester
- Apply code improvements and fixes addressing all Tester feedback
- Do NOT proceed without addressing issues raised in feedback.txt until approval is achieved
- Produce updated app.py and templates/*.html reflecting required fixes without changing unrelated functionality

Development Process:
1. Parse feedback.txt carefully, identify all defects and integration issues reported by Tester
2. Modify backend Python code (app.py) to fix functional errors, data flow issues, and integration points
3. Modify frontend templates (*.html) to fix rendering, element IDs, context variable usage, and navigation
4. Maintain consistency with design_spec.md requirements and data schemas
5. Repeat until Tester writes "[APPROVED]" status in feedback.txt

CRITICAL REQUIREMENTS:
- Use write_text_file tool to output both updated app.py and all modified template files
- Preserve file naming and structure; update all necessary files only
- Do NOT introduce new features or remove existing approved functionality
- Thoroughly address all Tester feedback in each iteration
- Feedback file presence and content are gating conditions for progress

Output: app.py, templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'app.py', 'source': 'BackendDeveloper'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'FrontendDeveloper'}, {'type': 'text_file', 'name': 'feedback.txt', 'source': 'Tester'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}],
    },

    "Tester": {
        "prompt": (
            """You are a Software Test Engineer specializing in integration and functional testing of Python web applications with HTML frontends.

Your goal is to rigorously test the integration of backend (app.py) and frontend (templates/*.html) to identify any defects, inconsistencies, or missing functionality, and provide detailed corrective feedback until all tests are passed.

Task Details:
- Read app.py and all templates/*.html files from CONTEXT
- Execute thorough integration tests covering all 'JobBoard' features and pages
- Verify data flow matches design_spec.md expectations and UI elements are present and functional
- Check navigation, input handling, dynamic content rendering, and file uploads across pages
- Produce comprehensive feedback.txt with detailed issues, test results, and improvement suggestions
- Write "[APPROVED]" in feedback.txt only when all test cases pass without any issues

Testing Guidelines:
1. Prepare end-to-end test cases for all nine pages ensuring coverage of navigation and functionalities
2. Execute tests using execute_python_code tool for backend validation and manual or scripted frontend checks
3. Confirm output consistency between backend data and frontend rendering
4. Check that all input_artifacts specifications and output_artifacts contract are honored correctly
5. Provide clear reproducible feedback items and required fixes with exact references to code or template locations

CRITICAL REQUIREMENTS:
- Use execute_python_code tool to run and validate backend where applicable
- Write feedback.txt file with clear markings
  - Include "NEED_MODIFY" marker when defects or missing features found
  - Replace with "[APPROVED]" marker only when all tests pass fully
- Feedback file content is gating condition for Developer improvements
- Do NOT approve partial fixes or incomplete functionality

Output: feedback.txt"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['execute_python_code'],
        "input_artifacts": [{'type': 'text_file', 'name': 'app.py', 'source': 'BackendDeveloper'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'FrontendDeveloper'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'feedback.txt'}],
    }

}

REVIEW_PROFILES = {
    'SystemArchitect': [
        ("BackendDeveloper", """Verify backend sections of design_spec.md: all Flask routes including dashboard, job listings, applications, companies, jobs, resumes, and search pages are specified with function names, methods, and context variables; data schemas for jobs, companies, categories, applications, resumes, and mappings match example formats exactly.""", [{'type': 'user', 'name': 'user_task_description'}, {'type': 'text_file', 'name': 'design_spec.md'}]),
        ("FrontendDeveloper", """Verify frontend sections of design_spec.md: all HTML templates for dashboard, listings, job details, application form, tracking, companies, company profile, resumes, and search results specify exact element IDs, context variables, navigation mappings with url_for functions, and page titles.""", [{'type': 'user', 'name': 'user_task_description'}, {'type': 'text_file', 'name': 'design_spec.md'}])
    ],

    'BackendDeveloper': [
        ("SystemArchitect", """Verify app.py correctness versus design_spec.md: all routes exist, methods and context variables match design; data loading uses correct field order and file formats from design; root route redirects to dashboard.""", [{'type': 'text_file', 'name': 'design_spec.md'}, {'type': 'text_file', 'name': 'app.py'}])
    ],

    'FrontendDeveloper': [
        ("SystemArchitect", """Validate templates/*.html implement all element IDs, context variables, navigation using url_for, and page titles exactly as specified in design_spec.md.""", [{'type': 'text_file', 'name': 'design_spec.md'}, {'type': 'text_file', 'name': 'templates/*.html'}])
    ],

    'Developer': [
        ("Tester", """Tester verifies Developer's code revisions based on feedback; Tester ensures fixes are correctly applied for all tested functionalities.""", [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}, {'type': 'text_file', 'name': 'feedback.txt'}])
    ],

    'Tester': [
        ("SystemArchitect", """SystemArchitect reviews testing coverage and feedback for completeness and correlation with initial design_spec.md.""", [{'type': 'text_file', 'name': 'feedback.txt'}, {'type': 'text_file', 'name': 'design_spec.md'}])
    ]

}




# ==================== Chaos Controller Setup ====================
chaos_controller = ChaosController(
    agent_chaos_enabled=False,
    stress_chaos_enabled=True,
    io_chaos_enabled=False,
    target_agent_names=list(AGENT_PROFILES.keys())
)

# Start chaos experiment with 20% probability
chaos_controller.start_experiment(
    running_agents=list(AGENT_PROFILES.keys()),
    agent_profiles=AGENT_PROFILES,
    probability=0.2
)

# Save chaos configuration to file for debugging
from datetime import datetime
import json

chaos_config_data = {
    "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    "scenario": "stress_chaos",
    "probability": 0.2,
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

print(f"Chaos scenario 'stress_chaos' activated with 20% probability")
print(f"Chaos configuration saved to: chaos_config.json")
# ================================================================

# Orchestration Functions
async def architecture_design_phase():
    # Create SystemArchitect agent
    SystemArchitect = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="SystemArchitect",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=2,
        timeout_threshold=180,
        failure_threshold=1,
        recovery_time=30
    )

    # Execute SystemArchitect
    await execute(SystemArchitect, "Draft design_spec.md with complete Flask routes, HTML templates, and data schemas as specified in user_task_description")
# Phase1_End

# Phase2_Start
import asyncio

async def parallel_implementation_phase():
    # Declare agents
    BackendDeveloper = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="BackendDeveloper",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=2,
        timeout_threshold=180,
        failure_threshold=1,
        recovery_time=30
    )
    FrontendDeveloper = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="FrontendDeveloper",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=2,
        timeout_threshold=160,
        failure_threshold=1,
        recovery_time=30
    )

    # Execute both agents in parallel
    await asyncio.gather(
        execute(BackendDeveloper, "Implement app.py backend routes and data handling from design_spec.md Sections 1 and 3"),
        execute(FrontendDeveloper, "Implement all HTML templates from design_spec.md Section 2 with exact element IDs and navigation")
    )
# Phase2_End

# Phase3_Start
import asyncio

async def integration_testing_phase():
    # Create Developer agent
    Developer = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="Developer",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase3"],
        max_retries=2,
        timeout_threshold=180,
        failure_threshold=1,
        recovery_time=40
    )
    # Create Tester agent
    Tester = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="Tester",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase3"],
        max_retries=2,
        timeout_threshold=160,
        failure_threshold=1,
        recovery_time=40
    )

    MAX_ITERATIONS = 5
    for iteration in range(MAX_ITERATIONS):
        if iteration == 0:
            # First iteration Developer works without feedback
            await execute(Developer, "Iteratively improve app.py and templates/*.html for full integration and functional correctness")
        else:
            # Read feedback.txt content for Developer
            try:
                with open("feedback.txt", "r") as f:
                    feedback_content = f.read()
            except FileNotFoundError:
                # If feedback file missing, stop loop
                break
            # Stop if approved
            if "[APPROVED]" in feedback_content:
                break
            await execute(Developer, f"Address all integration issues in feedback.txt:\n{feedback_content}")

        # Tester runs integration tests and writes feedback.txt
        await execute(Tester, "Run end-to-end integration tests on app.py and templates/*.html producing feedback.txt with detailed issues or [APPROVED] status")

        # Check for approval to break early
        try:
            with open("feedback.txt", "r") as f:
                feedback_content = f.read()
            if "[APPROVED]" in feedback_content:
                break
        except FileNotFoundError:
            pass
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
        architecture_design_phase()
    ]
    step2 = [
        parallel_implementation_phase()
    ]
    step3 = [
        integration_testing_phase()
    ]

    await asyncio.gather(*step1)
    await asyncio.gather(*step2)
    await asyncio.gather(*step3)

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
