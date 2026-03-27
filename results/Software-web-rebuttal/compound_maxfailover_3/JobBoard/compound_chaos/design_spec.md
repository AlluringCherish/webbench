# Design Specification for JobBoard Web Application

---

## 1. Flask Routes Specification

| Route Path               | Function Name              | HTTP Methods | Template Rendered       | Context Variables and Types                                                | Form Fields (POST)                                         |
|--------------------------|----------------------------|--------------|-------------------------|---------------------------------------------------------------------------|------------------------------------------------------------|
| /                        | redirect_to_dashboard       | GET          | Redirect to /dashboard  | None                                                                      | None                                                       |
| /dashboard               | dashboard                  | GET          | dashboard.html          | featured_jobs: List[Dict] (job data), new_opportunities: List[Dict] (job data)
                                                                                         | None                                                       |
| /jobs                    | job_listings               | GET          | job_listings.html       | jobs: List[Dict], categories: List[Dict], locations: List[str], filters: Dict[str,str]
                                       | None                                                       |
| /jobs/<int:job_id>       | job_details                | GET          | job_details.html        | job: Dict, company: Dict                                                 | None                                                       |
| /apply/<int:job_id>      | application_form           | GET, POST    | application_form.html   | job: Dict, errors: Dict[str,str] (only for GET with errors or POST failure) | applicant_name (str), applicant_email (str), resume_file (file), cover_letter (str) |
| /applications            | applications_tracking      | GET          | applications.html       | applications: List[Dict], filter_status: str                             | None                                                       |
| /application/<int:app_id>| application_details        | GET          | application_details.html | application: Dict, job: Dict, resume: Dict                                | None                                                       |
| /companies               | companies_directory        | GET          | companies.html          | companies: List[Dict], search_query: str                                | None                                                       |
| /companies/<int:company_id> | company_profile          | GET          | company_profile.html    | company: Dict, jobs: List[Dict]                                         | None                                                       |
| /resumes                 | resume_management          | GET, POST    | resumes.html            | resumes: List[Dict], errors: Dict[str,str] (optional)                    | resume_file (file, optional)                              |
| /resumes/delete/<int:resume_id> | delete_resume         | POST         | redirects to /resumes   | None                                                                      | None                                                       |
| /search                  | search_results             | GET          | search_results.html     | query: str, job_results: List[Dict], company_results: List[Dict]          | None                                                       |


### Details per route:

#### Root '/'
- Redirects to `/dashboard` route.

#### /dashboard
- Function: `dashboard`
- Method: GET
- Template: `dashboard.html`
- Context:
  - `featured_jobs`: List of dictionaries representing featured job postings. Each dictionary includes job_id, title, company_name, location, salary_min, salary_max.
  - `new_opportunities`: List of dictionaries representing latest job opportunities similarly structured.

#### /jobs
- Function: `job_listings`
- Method: GET
- Template: `job_listings.html`
- Context:
  - `jobs`: List of job dictionaries for display.
  - `categories`: List of category dictionaries with category_id and category_name.
  - `locations`: List of strings representing location filters.
  - `filters`: Dictionary containing keys 'search', 'category', 'location' representing current filter values.

#### /jobs/<int:job_id>
- Function: `job_details`
- Method: GET
- Template: `job_details.html`
- Context:
  - `job`: Dictionary with full job details.
  - `company`: Dictionary containing company details.

#### /apply/<int:job_id>
- Function: `application_form`
- Methods: GET, POST
- Template: `application_form.html`
- Context:
  - `job`: Job dict for the job being applied to.
  - `errors`: For GET or POST failures, dictionary mapping field name to error message.
- POST Form Fields:
  - `applicant_name`: string
  - `applicant_email`: string
  - `resume_file`: file upload
  - `cover_letter`: string

#### /applications
- Function: `applications_tracking`
- Method: GET
- Template: `applications.html`
- Context:
  - `applications`: List of applications with job title, company name, status, and date applied.
  - `filter_status`: string indicating current status filter.

#### /application/<int:app_id>
- Function: `application_details`
- Method: GET
- Template: `application_details.html`
- Context:
  - `application`: Application dict
  - `job`: Related job dict
  - `resume`: Resume dict associated with application

#### /companies
- Function: `companies_directory`
- Method: GET
- Template: `companies.html`
- Context:
  - `companies`: List of company dictionaries.
  - `search_query`: String search filter.

#### /companies/<int:company_id>
- Function: `company_profile`
- Method: GET
- Template: `company_profile.html`
- Context:
  - `company`: Company dictionary
  - `jobs`: List of job dicts from the company

#### /resumes
- Function: `resume_management`
- Methods: GET, POST
- Template: `resumes.html`
- Context:
  - `resumes`: List of resume dicts.
  - `errors`: Dict of errors from resume upload if any.
- POST Form Fields:
  - `resume_file`: file upload

#### /resumes/delete/<int:resume_id>
- Function: `delete_resume`
- Method: POST
- Redirects to `/resumes`
- No template
- No context

#### /search
- Function: `search_results`
- Method: GET
- Template: `search_results.html`
- Context:
  - `query`: Search string
  - `job_results`: List of job dicts matching the query
  - `company_results`: List of company dicts matching the query


---

## 2. HTML Template Specifications

### dashboard.html
- Page Title: Job Board Dashboard (for `<title>` and `<h1>`)
- Elements:
  - `dashboard-page`: Div - container for full dashboard page
  - `featured-jobs`: Div - displays featured jobs (multiple job summary cards)
  - `browse-jobs-button`: Button - navigates to job listings page
  - `my-applications-button`: Button - navigates to applications tracking page
  - `companies-button`: Button - navigates to companies directory page
- Context Variables:
  - `featured_jobs`: List[Dict] (job_id, title, company_name, location, salary_min, salary_max)
  - `new_opportunities`: List[Dict] similar structure
- Navigation:
  - `browse-jobs-button` -> url_for('job_listings')
  - `my-applications-button` -> url_for('applications_tracking')
  - `companies-button` -> url_for('companies_directory')

### job_listings.html
- Page Title: Job Listings
- Elements:
  - `listings-page`: Div - main container
  - `search-input`: Input - search jobs text field
  - `category-filter`: Dropdown - category filter
  - `location-filter`: Dropdown - location filter
  - `jobs-grid`: Div - grid containing job cards
  - `view-job-button-{{ job.job_id }}`: Button - button on each job card for details
- Context Variables:
  - `jobs`: List[Dict] with job data
  - `categories`: List[Dict] with category_id, category_name
  - `locations`: List[str]
  - `filters`: Dict[str,str] keys: 'search', 'category', 'location'
- Navigation:
  - `view-job-button-{{ job.job_id }}` -> url_for('job_details', job_id=job.job_id)

### job_details.html
- Page Title: Job Details
- Elements:
  - `job-details-page`: Div - container
  - `job-title`: H1 - job title text
  - `company-name`: Div - company name
  - `job-description`: Div - job description and requirements
  - `salary-range`: Div - salary range
  - `apply-now-button`: Button - navigates to application form
- Context Variables:
  - `job`: Dict with job fields
  - `company`: Dict with company info
- Navigation:
  - `apply-now-button` -> url_for('application_form', job_id=job.job_id)

### application_form.html
- Page Title: Submit Application
- Elements:
  - `application-form-page`: Div - container
  - `applicant-name`: Input - text input for applicant name
  - `applicant-email`: Input - text input for applicant email
  - `resume-upload`: File Input - resume upload field
  - `cover-letter`: Textarea - input for cover letter
  - `submit-application-button`: Button - submit
- Context Variables:
  - `job`: Dict with job data
  - `errors`: Dict[str,str] error messages keyed by field
- Navigation:
  - Form POSTs to url_for('application_form', job_id=job.job_id)

### applications.html
- Page Title: My Applications
- Elements:
  - `tracking-page`: Div - container
  - `applications-table`: Table - lists applications with columns job title, company, status, date applied
  - `status-filter`: Dropdown - filter applications by status
  - `view-application-button-{{ app.application_id }}`: Button to view details
  - `back-to-dashboard`: Button - navigates to dashboard
- Context Variables:
  - `applications`: List[Dict]
  - `filter_status`: str
- Navigation:
  - `view-application-button-{{ app.application_id }}` -> url_for('application_details', app_id=app.application_id)
  - `back-to-dashboard` -> url_for('dashboard')

### companies.html
- Page Title: Company Directory
- Elements:
  - `companies-page`: Div - main container
  - `companies-list`: Div - list of company cards
  - `search-company-input`: Input - search field
  - `view-company-button-{{ company.company_id }}`: Button - view company profile
  - `back-to-dashboard`: Button - navigates to dashboard
- Context Variables:
  - `companies`: List[Dict]
  - `search_query`: str
- Navigation:
  - `view-company-button-{{ company.company_id }}` -> url_for('company_profile', company_id=company.company_id)
  - `back-to-dashboard` -> url_for('dashboard')

### company_profile.html
- Page Title: Company Profile
- Elements:
  - `company-profile-page`: Div - container
  - `company-info`: Div - shows company name, industry, location, description
  - `company-jobs`: Div - container for company's jobs
  - `jobs-list`: Div - list of jobs with titles and status indicators
  - `view-job-button-{{ job.job_id }}`: Button on each job to view details
  - `back-to-companies`: Button - navigates back to companies directory
- Context Variables:
  - `company`: Dict
  - `jobs`: List[Dict]
- Navigation:
  - `view-job-button-{{ job.job_id }}` -> url_for('job_details', job_id=job.job_id)
  - `back-to-companies` -> url_for('companies_directory')

### resumes.html
- Page Title: My Resumes
- Elements:
  - `resume-page`: Div - container
  - `resumes-list`: Div - list of uploaded resumes
  - `upload-resume-button`: Button - triggers file input
  - `resume-file-input`: File Input (hidden) - upload field
  - `delete-resume-button-{{ resume.resume_id }}`: Button to delete resume
  - `back-to-dashboard`: Button - navigates to dashboard
- Context Variables:
  - `resumes`: List[Dict]
  - `errors`: Dict[str,str] (optional)
- Navigation:
  - `delete-resume-button-{{ resume.resume_id }}` -> form POST to url_for('delete_resume', resume_id=resume.resume_id)
  - `back-to-dashboard` -> url_for('dashboard')

### search_results.html
- Page Title: Search Results
- Elements:
  - `search-results-page`: Div - container
  - `search-query-display`: Div - shows entered search query
  - `results-tabs`: Div - tab control to switch between job and company results
  - `job-results`: Div - listing of job search results
  - `company-results`: Div - listing of company search results
  - `no-results-message`: Div - visible if no results found
- Context Variables:
  - `query`: str
  - `job_results`: List[Dict]
  - `company_results`: List[Dict]
- Navigation:
  - Each job and company entry includes buttons linking to their respective details pages using url_for('job_details', job_id=...) and url_for('company_profile', company_id=...)

---

## 3. Data File Schemas

### jobs.txt
- File Path: data/jobs.txt
- Fields:
  1. job_id (int)
  2. title (str)
  3. company_id (int)
  4. location (str)
  5. salary_min (int)
  6. salary_max (int)
  7. category (str)
  8. description (str)
  9. posted_date (YYYY-MM-DD str)
- Description: Stores all job postings.
- Examples:
  ```
  1|Senior Python Developer|1|Remote|80000|120000|Technology|Experienced Python developer for web applications|2025-01-15
  2|Data Analyst|2|New York, NY|60000|85000|Finance|Analyze financial data and create reports|2025-01-16
  3|Healthcare Administrator|3|Los Angeles, CA|50000|70000|Healthcare|Manage hospital operations and patient records|2025-01-14
  ```

### companies.txt
- File Path: data/companies.txt
- Fields:
  1. company_id (int)
  2. company_name (str)
  3. industry (str)
  4. location (str)
  5. employee_count (int)
  6. description (str)
- Description: Stores company profiles.
- Examples:
  ```
  1|TechCorp|Technology|San Francisco, CA|500|Leading software solutions provider
  2|FinanceHub|Finance|New York, NY|300|Innovative financial services company
  3|MediCare|Healthcare|Los Angeles, CA|200|Premier healthcare management organization
  ```

### categories.txt
- File Path: data/categories.txt
- Fields:
  1. category_id (int)
  2. category_name (str)
  3. description (str)
- Description: Stores categories for jobs.
- Examples:
  ```
  1|Technology|Software, IT, and tech-related positions
  2|Finance|Banking, accounting, and finance positions
  3|Healthcare|Medical and healthcare industry positions
  ```

### applications.txt
- File Path: data/applications.txt
- Fields:
  1. application_id (int)
  2. job_id (int)
  3. applicant_name (str)
  4. applicant_email (str)
  5. status (str) (e.g. Applied, Under Review, Interview, Rejected)
  6. applied_date (YYYY-MM-DD str)
  7. resume_id (int)
- Description: Stores job applications submitted by users.
- Examples:
  ```
  1|1|John Doe|john@email.com|Under Review|2025-01-17|1
  2|2|Jane Smith|jane@email.com|Applied|2025-01-16|2
  3|3|Robert Johnson|robert@email.com|Interview|2025-01-15|3
  ```

### resumes.txt
- File Path: data/resumes.txt
- Fields:
  1. resume_id (int)
  2. applicant_name (str)
  3. applicant_email (str)
  4. filename (str)
  5. upload_date (YYYY-MM-DD str)
  6. summary (str)
- Description: Stores uploaded resumes metadata.
- Examples:
  ```
  1|John Doe|john@email.com|john_resume.pdf|2025-01-17|Senior developer with 8 years experience
  2|Jane Smith|jane@email.com|jane_resume.pdf|2025-01-16|Data analyst with financial background
  3|Robert Johnson|robert@email.com|robert_resume.pdf|2025-01-15|Healthcare administrator with 5 years experience
  ```

### job_categories.txt
- File Path: data/job_categories.txt
- Fields:
  1. mapping_id (int)
  2. job_id (int)
  3. category_id (int)
- Description: Maps jobs to categories.
- Examples:
  ```
  1|1|1
  2|2|2
  3|3|3
  ```

---

End of Design Specification
