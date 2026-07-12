# JobBoard Web Application Design Specification

---

# Section 1: Flask Routes Specification

| Route Path               | Function Name          | HTTP Method(s) | Template Rendered    | Context Variables Passed to Template                         | 
|-------------------------|------------------------|----------------|---------------------|--------------------------------------------------------------|
| /                       | root_redirect           | GET            | Redirect to /dashboard | None                                                           |
| /dashboard              | dashboard_page          | GET            | dashboard.html       | featured_jobs: List[dict], each with keys: job_id(int), title(str), company_name(str), location(str), salary_min(int), salary_max(int)
|                         |                        |                |                     | categories: List[str] (for featured categories shown in dashboard, if needed)                        |
| /jobs                   | job_listings            | GET            | job_listings.html    | jobs: List[dict], each with job_id(int), title(str), company_name(str), location(str), salary_min(int), salary_max(int), category(str)
|                         |                        |                |                     | categories: List[str] (job categories for filter dropdown)
|                         |                        |                |                     | locations: List[str] (unique job locations for filter dropdown)
| /jobs                   | filter_jobs             | POST           | job_listings.html    | jobs: List[dict] (filtered jobs after search/filter)
|                         |                        |                |                     | categories: List[str]
|                         |                        |                |                     | locations: List[str]
| /job/<int:job_id>        | job_details             | GET            | job_details.html     | job: dict with keys: job_id(int), title(str), company_name(str), location(str), salary_min(int), salary_max(int), description(str)
| /job/<int:job_id>/apply  | application_form        | GET            | application_form.html| job_id: int
| /job/<int:job_id>/apply  | submit_application      | POST           | application_form.html or redirect to /my_applications | On POST submission, processes application form fields:
|                         |                        |                |                     | - applicant_name (str)
|                         |                        |                |                     | - applicant_email (str)
|                         |                        |                |                     | - cover_letter (str)
|                         |                        |                |                     | - resume_file (file upload)
| /my_applications         | application_tracking    | GET            | application_tracking.html | applications: List[dict] each with application_id(int), job_title(str), company_name(str), status(str), applied_date(str)
|                         |                        |                |                     | filtered_status: str (selected status filter)
| /application/<int:app_id>| application_details     | GET            | application_details.html | application: dict with details of the application and resume
| /companies              | companies_directory      | GET            | companies.html       | companies: List[dict] each with company_id(int), company_name(str), industry(str), employee_count(int)
| /company/<int:company_id>| company_profile         | GET            | company_profile.html | company: dict with company_id(int), company_name(str), industry(str), location(str), description(str), employee_count(int)
|                         |                        |                |                     | jobs: List[dict] of open jobs for this company: job_id(int), title(str), status(str) if applicable
| /resumes                | resume_management        | GET            | resume_management.html | resumes: List[dict] each with resume_id(int), applicant_name(str), applicant_email(str), filename(str), upload_date(str), summary(str)
| /resumes/upload         | upload_resume            | POST           | redirect to /resumes | Form fields:
|                         |                        |                |                     | - resume_file (file upload)
| /resumes/delete/<int:resume_id>| delete_resume      | POST           | redirect to /resumes | No context
| /search                 | search_results           | GET            | search_results.html  | query: str (search query)
|                         |                        |                |                     | job_results: List[dict], each with job_id(int), title(str), company_name(str), location(str), salary_min(int), salary_max(int)
|                         |                        |                |                     | company_results: List[dict], each with company_id(int), company_name(str), industry(str)


---

# Section 2: HTML Template Specifications

## 1. dashboard.html
- Filename: templates/dashboard.html
- Page Title: Job Board Dashboard
- Element IDs:
  - dashboard-page (Div): Container for the dashboard page
  - featured-jobs (Div): Display of featured job recommendations
  - browse-jobs-button (Button): Navigates to job listings page
  - my-applications-button (Button): Navigates to applications tracking page
  - companies-button (Button): Navigates to companies directory page
- Context Variables:
  - featured_jobs: List[dict] (keys: job_id, title, company_name, location, salary_min, salary_max)
- Navigation Mappings:
  - browse-jobs-button: url_for('job_listings')
  - my-applications-button: url_for('application_tracking')
  - companies-button: url_for('companies_directory')

## 2. job_listings.html
- Filename: templates/job_listings.html
- Page Title: Job Listings
- Element IDs:
  - listings-page (Div): Container for the listings page
  - search-input (Input): Input field for searching jobs
  - category-filter (Dropdown): Filter jobs by category
  - location-filter (Dropdown): Filter jobs by location
  - jobs-grid (Div): Grid layout displaying job cards
  - view-job-button-{{ job.job_id }} (Button): View details button for each job
- Context Variables:
  - jobs: List[dict] (keys: job_id, title, company_name, location, salary_min, salary_max, category)
  - categories: List[str]
  - locations: List[str]
- Navigation Mappings:
  - view-job-button-{{ job.job_id }}: url_for('job_details', job_id=job.job_id)

## 3. job_details.html
- Filename: templates/job_details.html
- Page Title: Job Details
- Element IDs:
  - job-details-page (Div): Container for the job details page
  - job-title (H1): Displays job title
  - company-name (Div): Displays company name
  - job-description (Div): Displays full job description and requirements
  - salary-range (Div): Displays salary range
  - apply-now-button (Button): Button to apply for the job
- Context Variables:
  - job: dict (keys: job_id, title, company_name, location, salary_min, salary_max, description)
- Navigation Mappings:
  - apply-now-button: url_for('application_form', job_id=job.job_id)

## 4. application_form.html
- Filename: templates/application_form.html
- Page Title: Submit Application
- Element IDs:
  - application-form-page (Div): Container for the application form page
  - applicant-name (Input): Input field for applicant name
  - applicant-email (Input): Input field for applicant email
  - resume-upload (File Input): File upload field for resume
  - cover-letter (Textarea): Textarea for cover letter
  - submit-application-button (Button): Submits the application form
- Context Variables:
  - job_id: int
- Navigation Mappings:
  - submit-application-button: Submits form via POST to url_for('submit_application', job_id=job_id)

## 5. application_tracking.html
- Filename: templates/application_tracking.html
- Page Title: My Applications
- Element IDs:
  - tracking-page (Div): Container for tracking page
  - applications-table (Table): Table showing applications
  - status-filter (Dropdown): Filter applications by status (All, Applied, Under Review, Interview, Rejected)
  - view-application-button-{{ app.application_id }} (Button): View applications details button
  - back-to-dashboard (Button): Navigate back to dashboard
- Context Variables:
  - applications: List[dict] (keys: application_id, job_title, company_name, status, applied_date)
  - filtered_status: str
- Navigation Mappings:
  - view-application-button-{{ app.application_id }}: url_for('application_details', app_id=app.application_id)
  - back-to-dashboard: url_for('dashboard_page')

## 6. companies.html
- Filename: templates/companies.html
- Page Title: Company Directory
- Element IDs:
  - companies-page (Div): Container for companies directory page
  - companies-list (Div): List of company cards
  - search-company-input (Input): Search input for company name or industry
  - view-company-button-{{ company.company_id }} (Button): Button to view company profile
  - back-to-dashboard (Button): Button to return to dashboard
- Context Variables:
  - companies: List[dict] (keys: company_id, company_name, industry, employee_count)
- Navigation Mappings:
  - view-company-button-{{ company.company_id }}: url_for('company_profile', company_id=company.company_id)
  - back-to-dashboard: url_for('dashboard_page')

## 7. company_profile.html
- Filename: templates/company_profile.html
- Page Title: Company Profile
- Element IDs:
  - company-profile-page (Div): Container for company profile page
  - company-info (Div): Displays company name, industry, location, and description
  - company-jobs (Div): Displays all open jobs for the company
  - jobs-list (Div): List container for job summaries
  - view-job-button-{{ job.job_id }} (Button): View job details button
  - back-to-companies (Button): Return to companies directory
- Context Variables:
  - company: dict (company_id, company_name, industry, location, description, employee_count)
  - jobs: List[dict] (job_id, title, status)
- Navigation Mappings:
  - view-job-button-{{ job.job_id }}: url_for('job_details', job_id=job.job_id)
  - back-to-companies: url_for('companies_directory')

## 8. resume_management.html
- Filename: templates/resume_management.html
- Page Title: My Resumes
- Element IDs:
  - resume-page (Div): Container for resume management page
  - resumes-list (Div): List of uploaded resumes
  - upload-resume-button (Button): Button triggers file upload
  - resume-file-input (File Input): Hidden file input for uploading resumes
  - delete-resume-button-{{ resume.resume_id }} (Button): Button to delete a resume
  - back-to-dashboard (Button): Navigate back to dashboard
- Context Variables:
  - resumes: List[dict] (resume_id, applicant_name, applicant_email, filename, upload_date, summary)
- Navigation Mappings:
  - upload-resume-button: triggers file selection for resume-file-input
  - delete-resume-button-{{ resume.resume_id }}: submits POST to url_for('delete_resume', resume_id=resume.resume_id)
  - back-to-dashboard: url_for('dashboard_page')

## 9. search_results.html
- Filename: templates/search_results.html
- Page Title: Search Results
- Element IDs:
  - search-results-page (Div): Container for the search results page
  - search-query-display (Div): Displays the user's search query
  - results-tabs (Div): Tabs to toggle between job and company results
  - job-results (Div): Container to display job search results
  - company-results (Div): Container to display company search results
  - no-results-message (Div): Display if no results found
- Context Variables:
  - query: str (the search query string)
  - job_results: List[dict] (job_id, title, company_name, location, salary_min, salary_max)
  - company_results: List[dict] (company_id, company_name, industry)
- Navigation Mappings:
  - For job entries: button with url_for('job_details', job_id=job.job_id)
  - For company entries: button with url_for('company_profile', company_id=company.company_id)

---

# Section 3: Data File Schemas

## 1. data/jobs.txt
- Pipe-delimited fields:
  - job_id (int)
  - title (str)
  - company_id (int)
  - location (str)
  - salary_min (int)
  - salary_max (int)
  - category (str)
  - description (str)
  - posted_date (str in YYYY-MM-DD)
- Description: Stores job postings with related metadata for company, location, salary, category, and posting date.
- Example rows:
  - 1|Senior Python Developer|1|Remote|80000|120000|Technology|Experienced Python developer for web applications|2025-01-15
  - 2|Data Analyst|2|New York, NY|60000|85000|Finance|Analyze financial data and create reports|2025-01-16
  - 3|Healthcare Administrator|3|Los Angeles, CA|50000|70000|Healthcare|Manage hospital operations and patient records|2025-01-14

## 2. data/companies.txt
- Pipe-delimited fields:
  - company_id (int)
  - company_name (str)
  - industry (str)
  - location (str)
  - employee_count (int)
  - description (str)
- Description: Stores company profiles including industry, location, size, and descriptions.
- Example rows:
  - 1|TechCorp|Technology|San Francisco, CA|500|Leading software solutions provider
  - 2|FinanceHub|Finance|New York, NY|300|Innovative financial services company
  - 3|MediCare|Healthcare|Los Angeles, CA|200|Premier healthcare management organization

## 3. data/categories.txt
- Pipe-delimited fields:
  - category_id (int)
  - category_name (str)
  - description (str)
- Description: Stores categories of jobs for filtering and classification.
- Example rows:
  - 1|Technology|Software, IT, and tech-related positions
  - 2|Finance|Banking, accounting, and finance positions
  - 3|Healthcare|Medical and healthcare industry positions

## 4. data/applications.txt
- Pipe-delimited fields:
  - application_id (int)
  - job_id (int)
  - applicant_name (str)
  - applicant_email (str)
  - status (str, e.g. Applied, Under Review, Interview, Rejected)
  - applied_date (str in YYYY-MM-DD)
  - resume_id (int)
- Description: Stores job application submissions tracking applicant info, status and associated resume.
- Example rows:
  - 1|1|John Doe|john@email.com|Under Review|2025-01-17|1
  - 2|2|Jane Smith|jane@email.com|Applied|2025-01-16|2
  - 3|3|Robert Johnson|robert@email.com|Interview|2025-01-15|3

## 5. data/resumes.txt
- Pipe-delimited fields:
  - resume_id (int)
  - applicant_name (str)
  - applicant_email (str)
  - filename (str)
  - upload_date (str in YYYY-MM-DD)
  - summary (str)
- Description: Stores uploaded resume metadata including filename, upload date and a brief summary.
- Example rows:
  - 1|John Doe|john@email.com|john_resume.pdf|2025-01-17|Senior developer with 8 years experience
  - 2|Jane Smith|jane@email.com|jane_resume.pdf|2025-01-16|Data analyst with financial background
  - 3|Robert Johnson|robert@email.com|robert_resume.pdf|2025-01-15|Healthcare administrator with 5 years experience

## 6. data/job_categories.txt
- Pipe-delimited fields:
  - mapping_id (int)
  - job_id (int)
  - category_id (int)
- Description: Mapping between jobs and their categories, to handle jobs with multiple categories if needed.
- Example rows:
  - 1|1|1
  - 2|2|2
  - 3|3|3

---

(This completes the comprehensive design specification for the JobBoard application, enabling backend and frontend developers to implement all features independently and in parallel with exact consistency.)