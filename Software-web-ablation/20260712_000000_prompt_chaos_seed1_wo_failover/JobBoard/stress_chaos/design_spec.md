# JobBoard Web Application Design Specification

---

## Section 1: Flask Routes Specification

| Route Path               | Function Name            | HTTP Method(s) | Template File         | Context Variables                                                                                     |
|--------------------------|--------------------------|----------------|-----------------------|------------------------------------------------------------------------------------------------------|
| /                        | root_redirect             | GET            | None                  | Redirects to /dashboard                                                                                |
| /dashboard               | dashboard                | GET            | dashboard.html        | featured_jobs: list of dict (job_id:int, title:str, company_name:str, location:str, salary_min:int, salary_max:int)
|                          |                          |                |                       | navigation buttons: browse_jobs_button (button), my_applications_button (button), companies_button (button) |
| /jobs                    | job_listings             | GET            | job_listings.html     | jobs: list of dict (job_id:int, title:str, company_name:str, location:str, salary_min:int, salary_max:int, category:str)
|                          |                          |                |                       | categories: list of str (category names), locations: list of str (location options)                   |
| /job/<int:job_id>        | job_details              | GET            | job_details.html      | job: dict (job_id:int, title:str, company_name:str, location:str, salary_min:int, salary_max:int, description:str)
|                          |                          |                |                       | company: dict (company_id:int, company_name:str)                                                     |
| /job/<int:job_id>/apply  | application_form         | GET, POST      | application_form.html | GET: job: dict (job_id:int, title:str)
|                          |                          |                |                       | POST: form fields - applicant_name:str, applicant_email:str, resume_file:file, cover_letter:str       |
| /applications            | application_tracking     | GET            | application_tracking.html | applications: list of dict (application_id:int, job_title:str, company_name:str, status:str, applied_date:str)
|                          |                          |                |                       | status_filter_options: list of str (All, Applied, Under Review, Interview, Rejected)                  |
| /application/<int:app_id>| application_details      | GET            | application_details.html (additional template for detail view - suggests) | application: dict (all application fields with job title and company name)                           |
| /companies               | companies_directory      | GET            | companies.html        | companies: list of dict (company_id:int, company_name:str, industry:str, employee_count:int)          |
| /company/<int:company_id>| company_profile          | GET            | company_profile.html  | company: dict (company_id:int, company_name:str, industry:str, location:str, description:str)
|                          |                          |                |                       | jobs: list of dict (job_id:int, title:str, status:str) (open jobs from company)                      |
| /resumes                 | resume_management        | GET, POST      | resumes.html          | GET: resumes: list of dict (resume_id:int, applicant_name:str, applicant_email:str, filename:str, upload_date:str, summary:str)
|                          |                          |                |                       | POST: form fields - resume_file:file                                                                  |
| /resume/<int:resume_id>/delete | delete_resume      | POST           | None                  | Deletes specified resume; redirects                                                                |
| /search                  | search_results           | GET            | search_results.html   | query: str, job_results: list of dict, company_results: list of dict                                  |

**Details and Input Expectations**

- The root path `/` acts as a redirect to `/dashboard` handled by `root_redirect`.
- The application form POST route `/job/<int:job_id>/apply` expects form-data with fields:
  - `applicant_name` (str)
  - `applicant_email` (str)
  - `resume_file` (file upload)
  - `cover_letter` (str)
- The resume upload POST via `/resumes` expects a file input named `resume_file`.
- Deletion of resumes is done via POST to `/resume/<int:resume_id>/delete`.

---

## Section 2: HTML Template Specifications

### 1. dashboard.html
- **Filename:** templates/dashboard.html
- **Page Title:** Job Board Dashboard
- **Element IDs:**
  - `dashboard-page` (Div) - Container for dashboard page
  - `featured-jobs` (Div) - Shows featured job recommendations
  - `browse-jobs-button` (Button) - Navigates to job listings page
  - `my-applications-button` (Button) - Navigates to application tracking page
  - `companies-button` (Button) - Navigates to companies directory page
- **Context Variables:**
  - `featured_jobs`: List of dict with keys `job_id`, `title`, `company_name`, `location`, `salary_min`, `salary_max`
- **Navigation (button actions):**
  - browse-jobs-button: `url_for('job_listings')`
  - my-applications-button: `url_for('application_tracking')`
  - companies-button: `url_for('companies_directory')`

### 2. job_listings.html
- **Filename:** templates/job_listings.html
- **Page Title:** Job Listings
- **Element IDs:**
  - `listings-page` (Div) - Container for listings page
  - `search-input` (Input) - Search by title, company, or location
  - `category-filter` (Dropdown) - Filter by job category
  - `location-filter` (Dropdown) - Filter by location
  - `jobs-grid` (Div) - Displays job cards
  - Dynamic buttons per job:
    - `view-job-button-{{ job.job_id }}` (Button) - View job details
- **Context Variables:**
  - `jobs`: List of dict with `job_id`, `title`, `company_name`, `location`, `salary_min`, `salary_max`, `category`
  - `categories`: List of strings (category names)
  - `locations`: List of strings (location names)
- **Navigation:**
  - view-job-button-{{ job.job_id }}: `url_for('job_details', job_id=job.job_id)`

### 3. job_details.html
- **Filename:** templates/job_details.html
- **Page Title:** Job Details
- **Element IDs:**
  - `job-details-page` (Div) - Container
  - `job-title` (H1) - Job title display
  - `company-name` (Div) - Company name display
  - `job-description` (Div) - Full job description and requirements
  - `salary-range` (Div) - Salary range display
  - `apply-now-button` (Button) - To apply for job
- **Context Variables:**
  - `job`: dict with keys `job_id`, `title`, `company_name`, `location`, `salary_min`, `salary_max`, `description`
  - `company`: dict with keys `company_id`, `company_name`
- **Navigation:**
  - apply-now-button: `url_for('application_form', job_id=job.job_id)`

### 4. application_form.html
- **Filename:** templates/application_form.html
- **Page Title:** Submit Application
- **Element IDs:**
  - `application-form-page` (Div) - Container
  - `applicant-name` (Input) - Applicant name input
  - `applicant-email` (Input) - Applicant email input
  - `resume-upload` (File Input) - Resume file upload
  - `cover-letter` (Textarea) - Cover letter text
  - `submit-application-button` (Button) - Submit application
- **Context Variables:**
  - `job`: dict with keys `job_id`, `title`
- **Navigation:**
  - submit-application-button: Submission POST to `/job/{{ job.job_id }}/apply`

### 5. application_tracking.html
- **Filename:** templates/application_tracking.html
- **Page Title:** My Applications
- **Element IDs:**
  - `tracking-page` (Div) - Container
  - `applications-table` (Table) - Shows applications with columns: job title, company, status, date applied
  - `status-filter` (Dropdown) - Filter by status
  - Dynamic buttons per application:
    - `view-application-button-{{ app.application_id }}` (Button) - View application details
  - `back-to-dashboard` (Button) - Back to dashboard
- **Context Variables:**
  - `applications`: List of dict with keys `application_id`, `job_title`, `company_name`, `status`, `applied_date`
  - `status_filter_options`: List[str] including All, Applied, Under Review, Interview, Rejected
- **Navigation:**
  - view-application-button-{{ app.application_id }}: `url_for('application_details', app_id=app.application_id)`
  - back-to-dashboard: `url_for('dashboard')`

### 6. companies.html
- **Filename:** templates/companies.html
- **Page Title:** Company Directory
- **Element IDs:**
  - `companies-page` (Div) - Container
  - `companies-list` (Div) - List of company cards
  - `search-company-input` (Input) - Search companies input
  - Dynamic buttons per company:
    - `view-company-button-{{ company.company_id }}` (Button) - View company profile
  - `back-to-dashboard` (Button) - Back to dashboard
- **Context Variables:**
  - `companies`: List of dict with keys `company_id`, `company_name`, `industry`, `employee_count`
- **Navigation:**
  - view-company-button-{{ company.company_id }}: `url_for('company_profile', company_id=company.company_id)`
  - back-to-dashboard: `url_for('dashboard')`

### 7. company_profile.html
- **Filename:** templates/company_profile.html
- **Page Title:** Company Profile
- **Element IDs:**
  - `company-profile-page` (Div) - Container
  - `company-info` (Div) - Shows company name, industry, location, description
  - `company-jobs` (Div) - Shows open jobs for this company
  - `jobs-list` (Div) - List jobs with title and status
  - Dynamic buttons per job:
    - `view-job-button-{{ job.job_id }}` (Button) - View job from company profile
  - `back-to-companies` (Button) - Back to companies directory
- **Context Variables:**
  - `company`: dict with keys `company_id`, `company_name`, `industry`, `location`, `description`
  - `jobs`: List of dict with keys `job_id`, `title`, `status`
- **Navigation:**
  - view-job-button-{{ job.job_id }}: `url_for('job_details', job_id=job.job_id)`
  - back-to-companies: `url_for('companies_directory')`

### 8. resumes.html
- **Filename:** templates/resumes.html
- **Page Title:** My Resumes
- **Element IDs:**
  - `resume-page` (Div) - Container
  - `resumes-list` (Div) - List uploaded resumes
  - Dynamic buttons for resumes:
    - `delete-resume-button-{{ resume.resume_id }}` (Button) - Delete resume
  - `upload-resume-button` (Button) - Upload new resume
  - `resume-file-input` (File Input, hidden) - File input for resume
  - `back-to-dashboard` (Button) - Back to dashboard
- **Context Variables:**
  - `resumes`: List of dict with keys `resume_id`, `applicant_name`, `applicant_email`, `filename`, `upload_date`, `summary`
- **Navigation:**
  - delete-resume-button-{{ resume.resume_id }}: POST to `/resume/{{ resume.resume_id }}/delete`
  - upload-resume-button: Triggers file input
  - back-to-dashboard: `url_for('dashboard')`

### 9. search_results.html
- **Filename:** templates/search_results.html
- **Page Title:** Search Results
- **Element IDs:**
  - `search-results-page` (Div) - Container
  - `search-query-display` (Div) - Shows search query
  - `results-tabs` (Div) - Tabs for switching result types
  - `job-results` (Div) - Displays job search results
  - `company-results` (Div) - Displays company search results
  - `no-results-message` (Div) - Shows no-result message if empty
- **Context Variables:**
  - `query`: str
  - `job_results`: List of dict (same keys as jobs)
  - `company_results`: List of dict (company_id, company_name, industry)
- **Navigation:**
  - Each job or company result can contain buttons/links to corresponding detail pages using `url_for`

---

## Section 3: Data File Schemas

### 1. Jobs Data
- **File Path:** data/jobs.txt
- **Field Order:** job_id | title | company_id | location | salary_min | salary_max | category | description | posted_date
- **Description:** Stores all job postings including key details such as title, company reference, location, salary range, category, detailed description, and posting date.
- **Example Rows:**
  ```
  1|Senior Python Developer|1|Remote|80000|120000|Technology|Experienced Python developer for web applications|2025-01-15
  2|Data Analyst|2|New York, NY|60000|85000|Finance|Analyze financial data and create reports|2025-01-16
  3|Healthcare Administrator|3|Los Angeles, CA|50000|70000|Healthcare|Manage hospital operations and patient records|2025-01-14
  ```

### 2. Companies Data
- **File Path:** data/companies.txt
- **Field Order:** company_id | company_name | industry | location | employee_count | description
- **Description:** Stores all company profiles with identifying information and summary description.
- **Example Rows:**
  ```
  1|TechCorp|Technology|San Francisco, CA|500|Leading software solutions provider
  2|FinanceHub|Finance|New York, NY|300|Innovative financial services company
  3|MediCare|Healthcare|Los Angeles, CA|200|Premier healthcare management organization
  ```

### 3. Categories Data
- **File Path:** data/categories.txt
- **Field Order:** category_id | category_name | description
- **Description:** Stores categories of jobs with descriptions.
- **Example Rows:**
  ```
  1|Technology|Software, IT, and tech-related positions
  2|Finance|Banking, accounting, and finance positions
  3|Healthcare|Medical and healthcare industry positions
  ```

### 4. Applications Data
- **File Path:** data/applications.txt
- **Field Order:** application_id | job_id | applicant_name | applicant_email | status | applied_date | resume_id
- **Description:** Stores job application records including applicant details, status, and linked resume.
- **Example Rows:**
  ```
  1|1|John Doe|john@email.com|Under Review|2025-01-17|1
  2|2|Jane Smith|jane@email.com|Applied|2025-01-16|2
  3|3|Robert Johnson|robert@email.com|Interview|2025-01-15|3
  ```

### 5. Resumes Data
- **File Path:** data/resumes.txt
- **Field Order:** resume_id | applicant_name | applicant_email | filename | upload_date | summary
- **Description:** Stores uploaded resumes metadata with applicant info and summary.
- **Example Rows:**
  ```
  1|John Doe|john@email.com|john_resume.pdf|2025-01-17|Senior developer with 8 years experience
  2|Jane Smith|jane@email.com|jane_resume.pdf|2025-01-16|Data analyst with financial background
  3|Robert Johnson|robert@email.com|robert_resume.pdf|2025-01-15|Healthcare administrator with 5 years experience
  ```

### 6. Job Categories Mapping Data
- **File Path:** data/job_categories.txt
- **Field Order:** mapping_id | job_id | category_id
- **Description:** Maps jobs to categories for filtering and organization.
- **Example Rows:**
  ```
  1|1|1
  2|2|2
  3|3|3
  ```

---

This design specification document fully defines all routes, templates, and data schemas for the JobBoard application to enable parallel and independent backend and frontend development.
