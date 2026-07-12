# JobBoard Application Design Specification

---

## Section 1: Flask Routes Specification

| Route Path                 | Function Name           | HTTP Method(s) | Template Rendered       | Context Variables (name: type)                                                                                               | POST Input Expectations                      |
|----------------------------|------------------------|----------------|-------------------------|------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------|
| /                          | root_redirect           | GET            | None                    | None (Redirects to /dashboard)                                                                                               | None                                         |
| /dashboard                 | dashboard              | GET            | dashboard.html          | featured_jobs: list of dict (each dict: job_id: int, title: str, company_name: str, location: str, salary_min: int, salary_max: int)
|                                           | browse_jobs_button: none
| /jobs                      | job_listings           | GET            | job_listings.html       | jobs: list of dict (job_id: int, title: str, company_name: str, location: str, salary_min: int, salary_max: int, category: str)  | search: str (optional), category_filter: str (optional), location_filter: str (optional)                      |
| /job/<int:job_id>           | job_details            | GET            | job_details.html        | job: dict (job_id: int, title: str, company_name: str, location: str, salary_min: int, salary_max: int, description: str)       | None                                         |
| /apply/<int:job_id>         | application_form       | GET, POST      | application_form.html   | job: dict (job_id: int, title: str, company_name: str)                                                                        | applicant_name: str, applicant_email: str, resume_file: file upload, cover_letter: str                      |
| /applications              | application_tracking   | GET            | application_tracking.html | applications: list of dict (application_id: int, job_title: str, company_name: str, status: str, applied_date: str)             | status_filter: str (optional)                 |
| /application/<int:application_id> | application_details (optional)  | GET            | application_details.html (optional) | application: dict (application_id: int, job_title: str, company_name: str, status: str, applied_date: str, cover_letter: str)   | None                                         |
| /companies                 | companies_directory    | GET            | companies.html          | companies: list of dict (company_id: int, company_name: str, industry: str, employee_count: int)                               | search_company: str (optional)                |
| /company/<int:company_id>   | company_profile        | GET            | company_profile.html    | company: dict (company_id: int, company_name: str, industry: str, location: str, description: str), jobs: list of dict          | None                                         |
| /resumes                   | resume_management      | GET, POST      | resume_management.html  | resumes: list of dict (resume_id: int, applicant_name: str, applicant_email: str, filename: str, upload_date: str, summary: str) | POST input: resume_file: file upload          |
| /resume/delete/<int:resume_id> | delete_resume         | POST           | Redirect (resume_management.html) | resume_id: int                                                                                                                | None                                         |
| /search                    | search_results         | GET            | search_results.html     | query: str, job_results: list of dict, company_results: list of dict                                                           | query: str (via query params)                  |

---

## Detailed Routes Description

### 1. Root Redirect
- **Route path:** `/`
- **Function name:** `root_redirect`
- **HTTP methods:** GET
- **Behavior:** Redirects user to `/dashboard`.
- **Template:** None
- **Context:** None

### 2. Dashboard Route
- **Route path:** `/dashboard`
- **Function name:** `dashboard`
- **HTTP methods:** GET
- **Template rendered:** `dashboard.html`
- **Context variables:**
  - `featured_jobs` (list of dict): Each dict contains:
    - `job_id` (int)
    - `title` (str)
    - `company_name` (str)
    - `location` (str)
    - `salary_min` (int)
    - `salary_max` (int)

### 3. Job Listings Route
- **Route path:** `/jobs`
- **Function name:** `job_listings`
- **HTTP methods:** GET
- **Template rendered:** `job_listings.html`
- **Context variables:**
  - `jobs` (list of dict): Each dict contains:
    - `job_id` (int)
    - `title` (str)
    - `company_name` (str)
    - `location` (str)
    - `salary_min` (int)
    - `salary_max` (int)
    - `category` (str)
- **Query parameters (optional):**
  - `search` (str): search term entered by user
  - `category_filter` (str): category name to filter
  - `location_filter` (str): location filter

### 4. Job Details Route
- **Route path:** `/job/<int:job_id>`
- **Function name:** `job_details`
- **HTTP methods:** GET
- **Template rendered:** `job_details.html`
- **Context variables:**
  - `job` (dict): contains:
    - `job_id` (int)
    - `title` (str)
    - `company_name` (str)
    - `location` (str)
    - `salary_min` (int)
    - `salary_max` (int)
    - `description` (str)

### 5. Application Form Route
- **Route path:** `/apply/<int:job_id>`
- **Function name:** `application_form`
- **HTTP methods:** GET, POST
- **Template rendered:** `application_form.html`
- **Context variables:**
  - `job` (dict): contains:
    - `job_id` (int)
    - `title` (str)
    - `company_name` (str)
- **POST input fields:**
  - `applicant_name` (str)
  - `applicant_email` (str)
  - `resume_upload` (file)
  - `cover_letter` (str)

### 6. Application Tracking Route
- **Route path:** `/applications`
- **Function name:** `application_tracking`
- **HTTP methods:** GET
- **Template rendered:** `application_tracking.html`
- **Context variables:**
  - `applications` (list of dict): Each dict contains:
    - `application_id` (int)
    - `job_title` (str)
    - `company_name` (str)
    - `status` (str)
    - `applied_date` (str)
- **Query parameters (optional):**
  - `status_filter` (str): status to filter applications

### 7. Companies Directory Route
- **Route path:** `/companies`
- **Function name:** `companies_directory`
- **HTTP methods:** GET
- **Template rendered:** `companies.html`
- **Context variables:**
  - `companies` (list of dict): Each dict contains:
    - `company_id` (int)
    - `company_name` (str)
    - `industry` (str)
    - `employee_count` (int)
- **Query parameters (optional):**
  - `search_company` (str): term to search in company name or industry

### 8. Company Profile Route
- **Route path:** `/company/<int:company_id>`
- **Function name:** `company_profile`
- **HTTP methods:** GET
- **Template rendered:** `company_profile.html`
- **Context variables:**
  - `company` (dict): contains:
    - `company_id` (int)
    - `company_name` (str)
    - `industry` (str)
    - `location` (str)
    - `description` (str)
  - `jobs` (list of dict): list of jobs by this company, each:
    - `job_id` (int)
    - `title` (str)
    - `status` (str) (optional: status indicator)

### 9. Resume Management Route
- **Route path:** `/resumes`
- **Function name:** `resume_management`
- **HTTP methods:** GET, POST
- **Template rendered:** `resume_management.html`
- **Context variables:**
  - `resumes` (list of dict): Each dict contains:
    - `resume_id` (int)
    - `applicant_name` (str)
    - `applicant_email` (str)
    - `filename` (str)
    - `upload_date` (str)
    - `summary` (str)
- **POST input:**
  - `resume_file` (file upload)

### 10. Delete Resume Route
- **Route path:** `/resume/delete/<int:resume_id>`
- **Function name:** `delete_resume`
- **HTTP methods:** POST
- **Template rendered:** None (redirects to resume management)
- **POST input:** None

### 11. Search Results Route
- **Route path:** `/search`
- **Function name:** `search_results`
- **HTTP methods:** GET
- **Template rendered:** `search_results.html`
- **Context variables:**
  - `query` (str): Search query string
  - `job_results` (list of dict): each dict:
    - `job_id` (int)
    - `title` (str)
    - `company_name` (str)
    - `location` (str)
  - `company_results` (list of dict): each dict:
    - `company_id` (int)
    - `company_name` (str)
    - `industry` (str)

---

## Section 2: HTML Template Specifications

### 1. dashboard.html
- **Filename:** templates/dashboard.html
- **Page Title:** Job Board Dashboard
- **Element IDs:**
  - `dashboard-page`: Div - Container for the dashboard page
  - `featured-jobs`: Div - Displays featured job recommendations
  - `browse-jobs-button`: Button - Navigates to job listings page
  - `my-applications-button`: Button - Navigates to application tracking page
  - `companies-button`: Button - Navigates to companies directory page
- **Context Variables:**
  - `featured_jobs`: list of dict with fields:
    - `job_id` (int)
    - `title` (str)
    - `company_name` (str)
    - `location` (str)
    - `salary_min` (int)
    - `salary_max` (int)
- **Navigation Mappings:**
  - `browse-jobs-button`: url_for('job_listings')
  - `my-applications-button`: url_for('application_tracking')
  - `companies-button`: url_for('companies_directory')

### 2. job_listings.html
- **Filename:** templates/job_listings.html
- **Page Title:** Job Listings
- **Element IDs:**
  - `listings-page`: Div - Container for job listings page
  - `search-input`: Input - Text input for search
  - `category-filter`: Dropdown - Filter by job category
  - `location-filter`: Dropdown - Filter by job location
  - `jobs-grid`: Div - Grid displaying job cards
  - Dynamic ID (for each job card): `view-job-button-{{ job.job_id }}`: Button - View job details button
- **Context Variables:**
  - `jobs`: list of dict with fields:
    - `job_id` (int)
    - `title` (str)
    - `company_name` (str)
    - `location` (str)
    - `salary_min` (int)
    - `salary_max` (int)
    - `category` (str)
- **Navigation Mappings:**
  - Each `view-job-button-{{ job.job_id }}`: url_for('job_details', job_id=job.job_id)

### 3. job_details.html
- **Filename:** templates/job_details.html
- **Page Title:** Job Details
- **Element IDs:**
  - `job-details-page`: Div - Container for job details
  - `job-title`: H1 - Job title display
  - `company-name`: Div - Company name display
  - `job-description`: Div - Job description and requirements
  - `salary-range`: Div - Salary range display
  - `apply-now-button`: Button - Apply for job button
- **Context Variables:**
  - `job`: dict with fields:
    - `job_id` (int)
    - `title` (str)
    - `company_name` (str)
    - `location` (str)
    - `salary_min` (int)
    - `salary_max` (int)
    - `description` (str)
- **Navigation Mappings:**
  - `apply-now-button`: url_for('application_form', job_id=job.job_id)

### 4. application_form.html
- **Filename:** templates/application_form.html
- **Page Title:** Submit Application
- **Element IDs:**
  - `application-form-page`: Div - Container for application form
  - `applicant-name`: Input - Applicant name input
  - `applicant-email`: Input - Applicant email input
  - `resume-upload`: File Input - Upload resume file
  - `cover-letter`: Textarea - Cover letter input
  - `submit-application-button`: Button - Submit application button
- **Context Variables:**
  - `job`: dict with fields:
    - `job_id` (int)
    - `title` (str)
    - `company_name` (str)
- **Navigation Mappings:**
  - Form submission: POST to url_for('application_form', job_id=job.job_id)

### 5. application_tracking.html
- **Filename:** templates/application_tracking.html
- **Page Title:** My Applications
- **Element IDs:**
  - `tracking-page`: Div - Container for tracking page
  - `applications-table`: Table - Table listing applications
  - `status-filter`: Dropdown - Filter by status
  - Dynamic ID for each application: `view-application-button-{{ app.application_id }}`: Button - View application details
  - `back-to-dashboard`: Button - Navigate back to dashboard
- **Context Variables:**
  - `applications`: list of dict with fields:
    - `application_id` (int)
    - `job_title` (str)
    - `company_name` (str)
    - `status` (str)
    - `applied_date` (str)
- **Navigation Mappings:**
  - Each `view-application-button-{{ app.application_id }}`: url_for('application_details', application_id=app.application_id) [If implemented]
  - `back-to-dashboard`: url_for('dashboard')

### 6. companies.html
- **Filename:** templates/companies.html
- **Page Title:** Company Directory
- **Element IDs:**
  - `companies-page`: Div - Container for companies page
  - `companies-list`: Div - List of company cards
  - `search-company-input`: Input - Search companies
  - Dynamic ID for each company: `view-company-button-{{ company.company_id }}`: Button - View company profile
  - `back-to-dashboard`: Button - Navigate back to dashboard
- **Context Variables:**
  - `companies`: list of dict with fields:
    - `company_id` (int)
    - `company_name` (str)
    - `industry` (str)
    - `employee_count` (int)
- **Navigation Mappings:**
  - Each `view-company-button-{{ company.company_id }}`: url_for('company_profile', company_id=company.company_id)
  - `back-to-dashboard`: url_for('dashboard')

### 7. company_profile.html
- **Filename:** templates/company_profile.html
- **Page Title:** Company Profile
- **Element IDs:**
  - `company-profile-page`: Div - Container company profile
  - `company-info`: Div - Displays company name, industry, location, description
  - `company-jobs`: Div - Displays open jobs from company
  - `jobs-list`: Div - List of job postings
  - Dynamic ID for jobs: `view-job-button-{{ job.job_id }}`: Button - View job detail
  - `back-to-companies`: Button - Navigate back to company directory
- **Context Variables:**
  - `company`: dict with fields:
    - `company_id` (int)
    - `company_name` (str)
    - `industry` (str)
    - `location` (str)
    - `description` (str)
  - `jobs`: list of dict with fields:
    - `job_id` (int)
    - `title` (str)
    - `status` (str)
- **Navigation Mappings:**
  - Each `view-job-button-{{ job.job_id }}`: url_for('job_details', job_id=job.job_id)
  - `back-to-companies`: url_for('companies_directory')

### 8. resume_management.html
- **Filename:** templates/resume_management.html
- **Page Title:** My Resumes
- **Element IDs:**
  - `resume-page`: Div - Container for resume management page
  - `resumes-list`: Div - List of uploaded resumes
  - Dynamic ID for each resume delete button: `delete-resume-button-{{ resume.resume_id }}`: Button - Delete resume
  - `upload-resume-button`: Button - Upload new resume
  - `resume-file-input`: Hidden File Input - For resume upload
  - `back-to-dashboard`: Button - Navigate back to dashboard
- **Context Variables:**
  - `resumes`: list of dict with fields:
    - `resume_id` (int)
    - `applicant_name` (str)
    - `applicant_email` (str)
    - `filename` (str)
    - `upload_date` (str)
    - `summary` (str)
- **Navigation Mappings:**
  - `upload-resume-button`: triggers `resume-file-input` click (JS handled)
  - `delete-resume-button-{{ resume.resume_id }}`: POST to '/resume/delete/{{ resume.resume_id }}'
  - `back-to-dashboard`: url_for('dashboard')

### 9. search_results.html
- **Filename:** templates/search_results.html
- **Page Title:** Search Results
- **Element IDs:**
  - `search-results-page`: Div - Container for search results
  - `search-query-display`: Div - Displays search query
  - `results-tabs`: Div - Tabs switch between job and company results
  - `job-results`: Div - Shows job search results
  - `company-results`: Div - Shows company search results
  - `no-results-message`: Div - Displays when no search results
- **Context Variables:**
  - `query`: str
  - `job_results`: list of dict with fields:
    - `job_id` (int)
    - `title` (str)
    - `company_name` (str)
    - `location` (str)
  - `company_results`: list of dict with fields:
    - `company_id` (int)
    - `company_name` (str)
    - `industry` (str)
- **Navigation Mappings:**
  - Jobs and companies listed link to their detail pages via url_for (job_details, company_profile)

---

## Section 3: Data File Schemas

### 1. jobs.txt
- **File path:** data/jobs.txt
- **Field order (pipe-delimited):**
  - job_id (int)
  - title (str)
  - company_id (int)
  - location (str)
  - salary_min (int)
  - salary_max (int)
  - category (str)
  - description (str)
  - posted_date (YYYY-MM-DD str)
- **Description:** Stores all job postings with detailed information.
- **Example rows:**
  ```
  1|Senior Python Developer|1|Remote|80000|120000|Technology|Experienced Python developer for web applications|2025-01-15
  2|Data Analyst|2|New York, NY|60000|85000|Finance|Analyze financial data and create reports|2025-01-16
  3|Healthcare Administrator|3|Los Angeles, CA|50000|70000|Healthcare|Manage hospital operations and patient records|2025-01-14
  ```

### 2. companies.txt
- **File path:** data/companies.txt
- **Field order (pipe-delimited):**
  - company_id (int)
  - company_name (str)
  - industry (str)
  - location (str)
  - employee_count (int)
  - description (str)
- **Description:** Stores company profiles and details.
- **Example rows:**
  ```
  1|TechCorp|Technology|San Francisco, CA|500|Leading software solutions provider
  2|FinanceHub|Finance|New York, NY|300|Innovative financial services company
  3|MediCare|Healthcare|Los Angeles, CA|200|Premier healthcare management organization
  ```

### 3. categories.txt
- **File path:** data/categories.txt
- **Field order (pipe-delimited):**
  - category_id (int)
  - category_name (str)
  - description (str)
- **Description:** Stores job categories.
- **Example rows:**
  ```
  1|Technology|Software, IT, and tech-related positions
  2|Finance|Banking, accounting, and finance positions
  3|Healthcare|Medical and healthcare industry positions
  ```

### 4. applications.txt
- **File path:** data/applications.txt
- **Field order (pipe-delimited):**
  - application_id (int)
  - job_id (int)
  - applicant_name (str)
  - applicant_email (str)
  - status (str)
  - applied_date (YYYY-MM-DD str)
  - resume_id (int)
- **Description:** Stores all job applications with status tracking.
- **Example rows:**
  ```
  1|1|John Doe|john@email.com|Under Review|2025-01-17|1
  2|2|Jane Smith|jane@email.com|Applied|2025-01-16|2
  3|3|Robert Johnson|robert@email.com|Interview|2025-01-15|3
  ```

### 5. resumes.txt
- **File path:** data/resumes.txt
- **Field order (pipe-delimited):**
  - resume_id (int)
  - applicant_name (str)
  - applicant_email (str)
  - filename (str)
  - upload_date (YYYY-MM-DD str)
  - summary (str)
- **Description:** Stores uploaded resume metadata.
- **Example rows:**
  ```
  1|John Doe|john@email.com|john_resume.pdf|2025-01-17|Senior developer with 8 years experience
  2|Jane Smith|jane@email.com|jane_resume.pdf|2025-01-16|Data analyst with financial background
  3|Robert Johnson|robert@email.com|robert_resume.pdf|2025-01-15|Healthcare administrator with 5 years experience
  ```

### 6. job_categories.txt
- **File path:** data/job_categories.txt
- **Field order (pipe-delimited):**
  - mapping_id (int)
  - job_id (int)
  - category_id (int)
- **Description:** Maps jobs to categories for filtering and classification.
- **Example rows:**
  ```
  1|1|1
  2|2|2
  3|3|3
  ```

---

This concludes the comprehensive design specification document for the JobBoard application. This specification ensures backend and frontend developers can work independently with full alignment on routes, templates, and data handling with exact details.