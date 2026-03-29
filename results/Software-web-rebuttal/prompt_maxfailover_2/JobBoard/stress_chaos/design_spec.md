# JobBoard Web Application Design Specification

---

## Section 1: Flask Routes Specification

| Route Path               | Function Name          | HTTP Method(s) | Template Rendered     | Context Variables Passed (Name: Type)                                           | POST Input Expectations / Notes                                                                                       |
|--------------------------|------------------------|----------------|-----------------------|---------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------|
| /                        | root_redirect           | GET            | N/A (redirect)        | None                                                                            | Redirects to `/dashboard`                                                                                             |
| /dashboard               | dashboard              | GET            | dashboard.html        | featured_jobs: list of dict (each job), latest_jobs: list of dict                 | None                                                                                                                  |
| /jobs                    | job_listings           | GET            | job_listings.html     | jobs: list of dict, categories: list of dict, locations: list of str             | Accepts query parameters for search and filters via GET (optional): search_query (str), category_filter (str), location_filter (str) |
| /job/<int:job_id>        | job_details            | GET            | job_details.html      | job: dict, company: dict, categories: list of dict                             | None                                                                                                                  |
| /apply/<int:job_id>      | application_form       | GET, POST      | application_form.html | job: dict                                                                     | POST form fields: applicant_name (str), applicant_email (str), resume_file (file upload), cover_letter (str)            |
| /applications            | application_tracking   | GET            | application_tracking.html | applications: list of dict                                                      | Accepts optional query param for status filter via GET: status_filter (str)                                         |
| /application/<int:app_id>| application_details    | GET            | application_details.html | application: dict, job: dict, resume: dict (optional)                         | None                                                                                                                  |
| /companies               | companies_directory    | GET            | companies_directory.html | companies: list of dict                                                      | Accepts optional query param for search via GET: search_company_query (str)                                          |
| /company/<int:company_id>| company_profile        | GET            | company_profile.html  | company: dict, jobs: list of dict                                              | None                                                                                                                  |
| /resumes                 | resume_management      | GET, POST      | resume_management.html | resumes: list of dict                                                          | POST form fields: resume_file (file upload), applicant_name (str), applicant_email (str), summary (str)               |
| /resumes/delete/<int:resume_id> | delete_resume    | POST           | N/A (redirect)        | None                                                                            | No form fields; deletes the resume and redirects back to /resumes                                                    |
| /search                  | search_results         | GET            | search_results.html   | query: str, job_results: list of dict, company_results: list of dict             | Accepts query parameter `query` via GET                                                                             |

---

## Section 2: HTML Template Specifications

### 1. templates/dashboard.html
- Page Title: "Job Board Dashboard"
- Element IDs:
  - dashboard-page (Div) - Main container for dashboard page
  - featured-jobs (Div) - Container displaying featured jobs
  - browse-jobs-button (Button) - Navigate to /jobs
  - my-applications-button (Button) - Navigate to /applications
  - companies-button (Button) - Navigate to /companies
- Context Variables:
  - featured_jobs: list of dict with keys: job_id (int), title (str), company_name (str), location (str), salary_min (int), salary_max (int)
  - latest_jobs: list of dict (same keys as featured_jobs)
- Navigation Mapping:
  - #browse-jobs-button: url_for('job_listings')
  - #my-applications-button: url_for('application_tracking')
  - #companies-button: url_for('companies_directory')

### 2. templates/job_listings.html
- Page Title: "Job Listings"
- Element IDs:
  - listings-page (Div) - Container for listings
  - search-input (Input) - Search jobs by title, company, or location
  - category-filter (Dropdown) - Filter by job category
  - location-filter (Dropdown) - Filter by location
  - jobs-grid (Div) - Displays job cards
  - view-job-button-{{ job.job_id }} (Button) - View job details
- Context Variables:
  - jobs: list of dict with keys: job_id (int), title (str), company_name (str), location (str), salary_min (int), salary_max (int), category (str)
  - categories: list of dict with keys: category_id (int), category_name (str)
  - locations: list of str
- Navigation Mapping:
  - #view-job-button-{{ job.job_id }}: url_for('job_details', job_id=job.job_id)

### 3. templates/job_details.html
- Page Title: "Job Details"
- Element IDs:
  - job-details-page (Div) - Container
  - job-title (H1) - Job title display
  - company-name (Div) - Company name display
  - job-description (Div) - Job description and requirements
  - salary-range (Div) - Salary range display
  - apply-now-button (Button) - Apply for the job
- Context Variables:
  - job: dict with keys: job_id, title, company_id, location, salary_min, salary_max, description
  - company: dict with keys: company_id, company_name
  - categories: list of dict (category info used if needed)
- Navigation Mapping:
  - #apply-now-button: url_for('application_form', job_id=job.job_id)

### 4. templates/application_form.html
- Page Title: "Submit Application"
- Element IDs:
  - application-form-page (Div) - Container
  - applicant-name (Input) - Input applicant name
  - applicant-email (Input) - Input applicant email
  - resume-upload (File Input) - Upload resume file
  - cover-letter (Textarea) - Enter cover letter
  - submit-application-button (Button) - Submit application
- Context Variables:
  - job: dict with keys: job_id, title
- Navigation Mapping:
  - Form submits POST to url_for('application_form', job_id=job.job_id)

### 5. templates/application_tracking.html
- Page Title: "My Applications"
- Element IDs:
  - tracking-page (Div) - Container
  - applications-table (Table) - List of applications
  - status-filter (Dropdown) - Filter by application status
  - view-application-button-{{ app.application_id }} (Button) - View application detail
  - back-to-dashboard (Button) - Navigate to dashboard
- Context Variables:
  - applications: list of dict with keys: application_id, job_title, company_name, status, applied_date
- Navigation Mapping:
  - #view-application-button-{{ app.application_id }}: url_for('application_details', app_id=app.application_id)
  - #back-to-dashboard: url_for('dashboard')

### 6. templates/companies_directory.html
- Page Title: "Company Directory"
- Element IDs:
  - companies-page (Div) - Container
  - companies-list (Div) - List of company cards
  - search-company-input (Input) - Search companies by name or industry
  - view-company-button-{{ company.company_id }} (Button) - View company profile
  - back-to-dashboard (Button) - Navigate to dashboard
- Context Variables:
  - companies: list of dict with keys: company_id, company_name, industry, employee_count
- Navigation Mapping:
  - #view-company-button-{{ company.company_id }}: url_for('company_profile', company_id=company.company_id)
  - #back-to-dashboard: url_for('dashboard')

### 7. templates/company_profile.html
- Page Title: "Company Profile"
- Element IDs:
  - company-profile-page (Div) - Container
  - company-info (Div) - Shows company name, industry, location, description
  - company-jobs (Div) - Container for jobs list
  - jobs-list (Div) - List of job titles and status
  - view-job-button-{{ job.job_id }} (Button) - View job details
  - back-to-companies (Button) - Go back to companies directory
- Context Variables:
  - company: dict with keys: company_id, company_name, industry, location, description
  - jobs: list of dict with keys: job_id, title, status
- Navigation Mapping:
  - #view-job-button-{{ job.job_id }}: url_for('job_details', job_id=job.job_id)
  - #back-to-companies: url_for('companies_directory')

### 8. templates/resume_management.html
- Page Title: "My Resumes"
- Element IDs:
  - resume-page (Div) - Container
  - resumes-list (Div) - List of resumes with upload date
  - upload-resume-button (Button) - Upload new resume
  - resume-file-input (File Input - hidden) - Hidden file input for upload
  - delete-resume-button-{{ resume.resume_id }} (Button) - Delete a resume
  - back-to-dashboard (Button) - Navigate to dashboard
- Context Variables:
  - resumes: list of dict with keys: resume_id, applicant_name, applicant_email, filename, upload_date, summary
- Navigation Mapping:
  - #upload-resume-button: triggers file input click
  - #delete-resume-button-{{ resume.resume_id }}: form POST to url_for('delete_resume', resume_id=resume.resume_id)
  - #back-to-dashboard: url_for('dashboard')

### 9. templates/search_results.html
- Page Title: "Search Results"
- Element IDs:
  - search-results-page (Div) - Container
  - search-query-display (Div) - Show the search query term
  - results-tabs (Div) - Tabs to switch between job results and company results
  - job-results (Div) - Show job results
  - company-results (Div) - Show company results
  - no-results-message (Div) - Display if no results found
- Context Variables:
  - query: str
  - job_results: list of dict with keys: job_id, title, company_name, location, salary_min, salary_max
  - company_results: list of dict with keys: company_id, company_name, industry, location
- Navigation Mapping:
  - #view-job-button-{{ job.job_id }} (if used in job results): url_for('job_details', job_id=job.job_id)
  - #view-company-button-{{ company.company_id }} (if used in company results): url_for('company_profile', company_id=company.company_id)

---

## Section 3: Data File Schemas

### 1. data/jobs.txt
- Pipe-delimited Fields (no header):
  - job_id: int - Unique job identifier
  - title: str - Job title
  - company_id: int - Reference to company
  - location: str - Job location
  - salary_min: int - Minimum salary
  - salary_max: int - Maximum salary
  - category: str - Job category
  - description: str - Full job description and requirements
  - posted_date: str (YYYY-MM-DD) - Date posted
- Description: Stores all job postings available on the platform.
- Example Rows:
  1|Senior Python Developer|1|Remote|80000|120000|Technology|Experienced Python developer for web applications|2025-01-15
  2|Data Analyst|2|New York, NY|60000|85000|Finance|Analyze financial data and create reports|2025-01-16
  3|Healthcare Administrator|3|Los Angeles, CA|50000|70000|Healthcare|Manage hospital operations and patient records|2025-01-14

### 2. data/companies.txt
- Pipe-delimited Fields (no header):
  - company_id: int - Unique company identifier
  - company_name: str - Company name
  - industry: str - Industry category
  - location: str - Company location
  - employee_count: int - Number of employees
  - description: str - Company description
- Description: Stores company profiles.
- Example Rows:
  1|TechCorp|Technology|San Francisco, CA|500|Leading software solutions provider
  2|FinanceHub|Finance|New York, NY|300|Innovative financial services company
  3|MediCare|Healthcare|Los Angeles, CA|200|Premier healthcare management organization

### 3. data/categories.txt
- Pipe-delimited Fields (no header):
  - category_id: int - Unique category identifier
  - category_name: str - Name of category
  - description: str - Description of category
- Description: Stores job categories.
- Example Rows:
  1|Technology|Software, IT, and tech-related positions
  2|Finance|Banking, accounting, and finance positions
  3|Healthcare|Medical and healthcare industry positions

### 4. data/applications.txt
- Pipe-delimited Fields (no header):
  - application_id: int - Unique application identifier
  - job_id: int - Job applied for
  - applicant_name: str - Name of applicant
  - applicant_email: str - Applicant email
  - status: str - Application status (e.g., Applied, Under Review, Interview, Rejected)
  - applied_date: str (YYYY-MM-DD) - Date application submitted
  - resume_id: int - Reference to resume used
- Description: Stores job applications submitted by users.
- Example Rows:
  1|1|John Doe|john@email.com|Under Review|2025-01-17|1
  2|2|Jane Smith|jane@email.com|Applied|2025-01-16|2
  3|3|Robert Johnson|robert@email.com|Interview|2025-01-15|3

### 5. data/resumes.txt
- Pipe-delimited Fields (no header):
  - resume_id: int - Unique resume identifier
  - applicant_name: str - Name associated with resume
  - applicant_email: str - Applicant email
  - filename: str - Resume file name
  - upload_date: str (YYYY-MM-DD) - Upload date
  - summary: str - Summary or key highlights of the resume
- Description: Stores uploaded resumes.
- Example Rows:
  1|John Doe|john@email.com|john_resume.pdf|2025-01-17|Senior developer with 8 years experience
  2|Jane Smith|jane@email.com|jane_resume.pdf|2025-01-16|Data analyst with financial background
  3|Robert Johnson|robert@email.com|robert_resume.pdf|2025-01-15|Healthcare administrator with 5 years experience

### 6. data/job_categories.txt
- Pipe-delimited Fields (no header):
  - mapping_id: int - Unique mapping identifier
  - job_id: int - Job identifier
  - category_id: int - Category identifier
- Description: Maps jobs to categories (if multiple categories per job needed).
- Example Rows:
  1|1|1
  2|2|2
  3|3|3

---

# End of Design Specification
