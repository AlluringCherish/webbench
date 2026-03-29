# Design Specification Document for JobBoard Web Application

---

## Section 1: Flask Routes Specification

| Route Path                     | Function Name            | HTTP Method(s) | Template Rendered       | Context Variables Passed                                                                                   |
|--------------------------------|--------------------------|----------------|-------------------------|-----------------------------------------------------------------------------------------------------------|
| `/`                            | root_redirect_dashboard   | GET            | Redirects to `/dashboard` (no template)             | None                                                                                                  |
| `/dashboard`                  | dashboard_page           | GET            | dashboard.html           | featured_jobs (list of dict: job_id:int, title:str, company_name:str, location:str, salary_min:int, salary_max:int),
  latest_jobs (list of dict: same structure),
  categories (list of dict: category_id:int, category_name:str)
| `/jobs`                      | job_listings_page        | GET            | jobs.html                | jobs (list of dict: job_id:int, title:str, company_name:str, location:str, salary_min:int, salary_max:int),
  categories (list of dict: category_name:str),
  locations (list of str),
  selected_category (str or None),
  selected_location (str or None),
  search_query (str or None)
| `/jobs`                      | job_listings_page_search | POST           | jobs.html                | Same as GET but filtered by form data
| `/job/<int:job_id>`           | job_details_page          | GET            | job_details.html         | job (dict: job_id:int, title:str, company_name:str, location:str, salary_min:int, salary_max:int, category:str, description:str, posted_date:str)
| `/job/<int:job_id>/apply`    | application_form_page     | GET            | application_form.html    | job (dict: job_id:int, title:str, company_name:str)
| `/job/<int:job_id>/apply`    | submit_application        | POST           | application_form.html    | job (dict for redisplay if errors),
  form_errors (dict: field_name to str error messages, optional)
| `/applications`              | application_tracking_page| GET            | applications_tracking.html | applications (list of dict: application_id:int, job_title:str, company_name:str, status:str, applied_date:str),
  status_filter (str or None)
| `/application/<int:application_id>` | application_detail_page | GET            | application_detail.html  | application (dict: application_id:int, job_title:str, company_name:str, applicant_name:str, applicant_email:str, status:str, applied_date:str, resume_filename:str, cover_letter:str) |
| `/companies`                 | companies_directory_page | GET            | companies.html           | companies (list of dict: company_id:int, company_name:str, industry:str, employee_count:int),
  search_query (str or None)
| `/company/<int:company_id>`  | company_profile_page     | GET            | company_profile.html     | company (dict: company_id:int, company_name:str, industry:str, location:str, employee_count:int, description:str),
  jobs (list of dict: job_id:int, title:str, status:str)  
| `/resumes`                   | resume_management_page   | GET            | resumes.html             | resumes (list of dict: resume_id:int, filename:str, upload_date:str, summary:str)
| `/resumes/upload`            | upload_resume            | POST           | resumes.html             | resumes (list; for redisplay if errors),
  form_errors (dict optional)
| `/resume/<int:resume_id>/delete` | delete_resume          | POST           | Redirect to `/resumes` (no template)                   | None
| `/search`                    | search_results_page      | GET            | search_results.html      | query (str),
  job_results (list of dict: job_id:int, title:str, company_name:str, location:str, salary_min:int, salary_max:int),
  company_results (list of dict: company_id:int, company_name:str, industry:str)


### POST Route Input Expectations

- `/jobs` POST (job_listings_page_search):
  - form fields: search_input (str), category_filter (str), location_filter (str)

- `/job/<int:job_id>/apply` POST (submit_application):
  - form fields: applicant_name (str), applicant_email (str), resume_upload (file), cover_letter (str)

- `/search` GET parameters:
  - query (str) passed as URL parameter

- `/resumes/upload` POST (upload_resume):
  - form field: resume_file (file), summary (str)

- `/resume/<int:resume_id>/delete` POST (delete_resume): No form fields, resume_id from URL.

---

## Section 2: HTML Template Specifications

### templates/dashboard.html
- Page Title: "Job Board Dashboard"
- Element IDs:
  - `dashboard-page` (Div): Container for dashboard page
  - `featured-jobs` (Div): Displays featured job recommendations
  - `browse-jobs-button` (Button): Navigate to job listings page
  - `my-applications-button` (Button): Navigate to application tracking page
  - `companies-button` (Button): Navigate to companies directory page
- Context Variables:
  - featured_jobs: list of dicts with keys: job_id (int), title (str), company_name (str), location (str), salary_min (int), salary_max (int)
  - latest_jobs: list, similar structure arguably used for featured_jobs
  - categories: list of dicts: category_id (int), category_name (str)
- Navigation Mappings:
  - `browse-jobs-button`: url_for('job_listings_page')
  - `my-applications-button`: url_for('application_tracking_page')
  - `companies-button`: url_for('companies_directory_page')

### templates/jobs.html
- Page Title: "Job Listings"
- Element IDs:
  - `listings-page` (Div): Container for listings
  - `search-input` (Input): Search field for job title, company, or location
  - `category-filter` (Dropdown): Filter by job category
  - `location-filter` (Dropdown): Filter by location
  - `jobs-grid` (Div): Grid displaying job cards
  - `view-job-button-{{ job.job_id }}` (Button): View job details for each job
- Context Variables:
  - jobs: list of dicts with fields job_id, title, company_name, location, salary_min, salary_max
  - categories: list of strings (category names)
  - locations: list of strings
  - selected_category: string or None
  - selected_location: string or None
  - search_query: string or None
- Navigation Mappings:
  - For each `view-job-button-{{ job.job_id }}`: url_for('job_details_page', job_id=job.job_id)

### templates/job_details.html
- Page Title: "Job Details"
- Element IDs:
  - `job-details-page` (Div): Container
  - `job-title` (H1): Job title text
  - `company-name` (Div): Company name
  - `job-description` (Div): Full job description and requirements
  - `salary-range` (Div): Salary range display
  - `apply-now-button` (Button): Apply for job
- Context Variables:
  - job: dict with keys job_id, title, company_name, location, salary_min, salary_max, category, description, posted_date
- Navigation Mappings:
  - `apply-now-button`: url_for('application_form_page', job_id=job.job_id)

### templates/application_form.html
- Page Title: "Submit Application"
- Element IDs:
  - `application-form-page` (Div): Container
  - `applicant-name` (Input): Applicant name field
  - `applicant-email` (Input): Applicant email field
  - `resume-upload` (File Input): File upload field for resume
  - `cover-letter` (Textarea): Cover letter input
  - `submit-application-button` (Button): Submit application
- Context Variables:
  - job: dict with job_id, title, company_name
  - form_errors: dict mapping field names to error messages (optional)
- Navigation Mappings:
  - Form action POST to url_for('submit_application', job_id=job.job_id)

### templates/applications_tracking.html
- Page Title: "My Applications"
- Element IDs:
  - `tracking-page` (Div): Container
  - `applications-table` (Table): Lists applications with columns job title, company, status, applied date
  - `status-filter` (Dropdown): Filter by application status
  - `view-application-button-{{ application.application_id }}` (Button): View details for each application
  - `back-to-dashboard` (Button): Back to dashboard
- Context Variables:
  - applications: list of dicts with fields application_id, job_title, company_name, status, applied_date
  - status_filter (str or None)
- Navigation Mappings:
  - For each `view-application-button-{{ application.application_id }}`: url_for('application_detail_page', application_id=application.application_id)
  - `back-to-dashboard`: url_for('dashboard_page')

### templates/application_detail.html
- Page Title: "Application Detail"
- Element IDs:
  - `application-detail-page` (Div, implied container)
  - No explicit IDs given for fields, but template shows:
    - Application info: job title, company name
    - Applicant name, applicant email, status, applied date
    - Resume filename, cover letter
- Context Variables:
  - application: dict with application_id, job_title, company_name, applicant_name, applicant_email, status, applied_date, resume_filename, cover_letter
- Navigation Mappings:
  - Back buttons can use url_for('application_tracking_page')

### templates/companies.html
- Page Title: "Company Directory"
- Element IDs:
  - `companies-page` (Div): Container
  - `companies-list` (Div): List of company cards
  - `search-company-input` (Input): Search companies field
  - `view-company-button-{{ company.company_id }}` (Button): View company profile
  - `back-to-dashboard` (Button): Back to dashboard
- Context Variables:
  - companies: list of dicts with company_id, company_name, industry, employee_count
  - search_query (str or None)
- Navigation Mappings:
  - For each `view-company-button-{{ company.company_id }}`: url_for('company_profile_page', company_id=company.company_id)
  - `back-to-dashboard`: url_for('dashboard_page')

### templates/company_profile.html
- Page Title: "Company Profile"
- Element IDs:
  - `company-profile-page` (Div): Container
  - `company-info` (Div): Displays company name, industry, location, description
  - `company-jobs` (Div): Container for company jobs
  - `jobs-list` (Div): List of jobs
  - `view-job-button-{{ job.job_id }}` (Button): View job details for each job
  - `back-to-companies` (Button): Back to companies directory
- Context Variables:
  - company: dict with company_id, company_name, industry, location, employee_count, description
  - jobs: list of dicts with job_id, title, status
- Navigation Mappings:
  - For each `view-job-button-{{ job.job_id }}`: url_for('job_details_page', job_id=job.job_id)
  - `back-to-companies`: url_for('companies_directory_page')

### templates/resumes.html
- Page Title: "My Resumes"
- Element IDs:
  - `resume-page` (Div): Container
  - `resumes-list` (Div): List of resumes with upload date
  - `upload-resume-button` (Button): Upload new resume
  - `resume-file-input` (File Input, hidden): Resume file input
  - `delete-resume-button-{{ resume.resume_id }}` (Button): Delete resume
  - `back-to-dashboard` (Button): Back to dashboard
- Context Variables:
  - resumes: list of dicts with resume_id, filename, upload_date, summary
- Navigation Mappings:
  - `upload-resume-button`: triggers file input and form submission for uploading
  - For each `delete-resume-button-{{ resume.resume_id }}`: form POST to url_for('delete_resume', resume_id=resume.resume_id)
  - `back-to-dashboard`: url_for('dashboard_page')

### templates/search_results.html
- Page Title: "Search Results"
- Element IDs:
  - `search-results-page` (Div): Container
  - `search-query-display` (Div): Shows the search query
  - `results-tabs` (Div): Tabs to switch between job and company results
  - `job-results` (Div): Job search results
  - `company-results` (Div): Company search results
  - `no-results-message` (Div): Displayed if no search results
- Context Variables:
  - query (str)
  - job_results: list of dicts with job_id, title, company_name, location, salary_min, salary_max
  - company_results: list of dicts with company_id, company_name, industry
- Navigation Mappings:
  - For job result view buttons: url_for('job_details_page', job_id=job.job_id)
  - For company result view buttons: url_for('company_profile_page', company_id=company.company_id)

---

## Section 3: Data File Schemas

### 1. Jobs Data File
- File path: `data/jobs.txt`
- Fields order (pipe-delimited):
  1. job_id (int)
  2. title (str)
  3. company_id (int)
  4. location (str)
  5. salary_min (int)
  6. salary_max (int)
  7. category (str)
  8. description (str)
  9. posted_date (str, YYYY-MM-DD)
- Description: Stores job postings with details including company reference, salary range, category, description, and posting date.
- Example rows:
```
1|Senior Python Developer|1|Remote|80000|120000|Technology|Experienced Python developer for web applications|2025-01-15
2|Data Analyst|2|New York, NY|60000|85000|Finance|Analyze financial data and create reports|2025-01-16
3|Healthcare Administrator|3|Los Angeles, CA|50000|70000|Healthcare|Manage hospital operations and patient records|2025-01-14
```

### 2. Companies Data File
- File path: `data/companies.txt`
- Fields order (pipe-delimited):
  1. company_id (int)
  2. company_name (str)
  3. industry (str)
  4. location (str)
  5. employee_count (int)
  6. description (str)
- Description: Stores company profiles including industry, location, employee count, and description.
- Example rows:
```
1|TechCorp|Technology|San Francisco, CA|500|Leading software solutions provider
2|FinanceHub|Finance|New York, NY|300|Innovative financial services company
3|MediCare|Healthcare|Los Angeles, CA|200|Premier healthcare management organization
```

### 3. Categories Data File
- File path: `data/categories.txt`
- Fields order (pipe-delimited):
  1. category_id (int)
  2. category_name (str)
  3. description (str)
- Description: Stores job category metadata.
- Example rows:
```
1|Technology|Software, IT, and tech-related positions
2|Finance|Banking, accounting, and finance positions
3|Healthcare|Medical and healthcare industry positions
```

### 4. Applications Data File
- File path: `data/applications.txt`
- Fields order (pipe-delimited):
  1. application_id (int)
  2. job_id (int)
  3. applicant_name (str)
  4. applicant_email (str)
  5. status (str) (e.g., Applied, Under Review, Interview, Rejected)
  6. applied_date (str, YYYY-MM-DD)
  7. resume_id (int)
- Description: Stores user job applications and their current status.
- Example rows:
```
1|1|John Doe|john@email.com|Under Review|2025-01-17|1
2|2|Jane Smith|jane@email.com|Applied|2025-01-16|2
3|3|Robert Johnson|robert@email.com|Interview|2025-01-15|3
```

### 5. Resumes Data File
- File path: `data/resumes.txt`
- Fields order (pipe-delimited):
  1. resume_id (int)
  2. applicant_name (str)
  3. applicant_email (str)
  4. filename (str) (uploaded resume file name)
  5. upload_date (str, YYYY-MM-DD)
  6. summary (str) (brief resume description)
- Description: Stores user's uploaded resumes with metadata.
- Example rows:
```
1|John Doe|john@email.com|john_resume.pdf|2025-01-17|Senior developer with 8 years experience
2|Jane Smith|jane@email.com|jane_resume.pdf|2025-01-16|Data analyst with financial background
3|Robert Johnson|robert@email.com|robert_resume.pdf|2025-01-15|Healthcare administrator with 5 years experience
```

### 6. Job Categories Mapping Data File
- File path: `data/job_categories.txt`
- Fields order (pipe-delimited):
  1. mapping_id (int)
  2. job_id (int)
  3. category_id (int)
- Description: Maps jobs to their categories for filtering purposes.
- Example rows:
```
1|1|1
2|2|2
3|3|3
```

---

**End of design_spec.md**
