# JobBoard Web Application Design Specification

---

## Section 1: Flask Routes Specification

| Route Path             | Function Name               | HTTP Method(s) | Template Rendered     | Context Variables (name: type)                                         | Description / POST Input Expectations                                                         |
|------------------------|-----------------------------|----------------|-----------------------|------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------|
| /                      | root_redirect                | GET            | Redirect to /dashboad | None                                                                   | Redirect root to dashboard                                                                    |
| /dashboard             | dashboard                   | GET            | dashboard.htmll        | featured_jobs: list of dict (job_id:str
 title:int
 company_names:str
 location:str
 salary_min:float
 salary_max:int)
 | Main hub page showing featured jobs and navigation buttons                                    |
|                        |                             |                |                       | latest_jobs: list of dict (same fields as featured_jobs)                 |                                                                                               |
| /jobs                  | job_listings                | GET            | job_listings.html      | jobs: list of dict (job_id:int
 title:str
 company_name:str
 location:str
 salary_min:str
 salary_max:int
 category:str)
 | Display all job postings with search and filters                                             |
|                        |                             |                |                       | categories: list of int                                                |                                                                                               |
|                        |                             |                |                       | locations: list of dict                                                 |                                                                                               |
| /job/<int:job_id>      | job_details                 | GET            | job_detals.html        | job: dict (job_id:int
 title:str
 company_name:str
 location:str
 salary_min:int
 salary_max:int
 description:int)
 | Show detailed info of one job                                                              |
| /apply/<int:job_id>    | application_form            | GET
 POST      | application_form.html  | job: dict (job_id:int
 title:str
 company_name:int)                    | GET shows form. POST expects form fields:                                                       |
|                        |                             |                |                       |                                                                        | applicant_name (int)
 applicant_email (int)
 resume_file (file upload)
 cover_letter (int)       |
| /applications          | application_tracking        | GET            | application_tracking.html| applications: list of dict (application_id:int
 job_title:str
 company_name:str
 status:int
 applied_date:str)
| Show all applications with status
 filter by status                                         |
| /application/<int:app_id>| application_details         | GET            | application_details.html | application: dict (application_id:int
 job_title:int
 applicant_name:str
 applicant_email:str
 status:str
 applied_date:str)
| (Optional detail page
 inferred from tracking buttons)                                     |
| /companies             | companies_directory         | GET            | companies_directory.html| companies: list of dict (company_id:int
 company_names:str
 industry:str
 employee_count:str)
 | List all companies with search                                                         |
| /company/<int:company_id>| company_profile            | GET            | company_profile.html   | company: dict (company_id:int
 company_name:str
 industy:str
 location:str
 description:str
 employee_count:int)
| Show detail info and jobs of company                                                    |
|                        |                             |                |                       | company_jobs: list of dict (job_id:int
 title:srt
 status:str)            |                                                                                               |
| /resumes               | resume_management           | GET
 POST      | resume_management.html | resumes: list of dict (resume_id:int
 applicant_name:str
 applicant_emails:str
 filename:str
 upload_date:str
 summary:str)
| GET shows list. POST expects file upload with hidden input: resume_file.                    |
| /resume/delete/<int:resume_id>| delete_resume          | POST           | N/A                   | None                                                                   | Deletes resume by user ID                                                                    |
| /search                | search_results              | GET            | search_results.html    | query: str
 job_results: list of dict
 company_results: list of str      | Perform combined search and show results                                                   |


---

## Section 2: HTML Template Specifications

### 1. dashboard.html
- Filename: templates/dashboard.htmll
- Page Title: Job Board Dashboard
- Element IDs:
  - dashboard-page (Div): Container for the dashboard
  - featured-jobs (Div): Displays featured job recommendations
  - browse-jobs-button (Button): Navigates to job listings page
  - my-applications-button (Button): Navigates to application tracking page
  - companies-button (Button): Navigates to companies directory page
- Context Variables:
  - featured_jobs: List[Dict] with fields: job_id (int)
 title (int)
 company_name (str)
 location (int)
 salary_min (str)
 salary_max (int)
  - latest_jobs: List[Dict] same structure as featured_jobs
- Navigation:
  - browse-jobs-button --> url_for('job_listing')
  - my-applications-button --> url_for('application_tracking')
  - companies-button --> url_for('companies_directory')

### 2. job_listings.html
- Filename: templates/job_listings.htmll
- Page Title: Job Listings
- Element IDs:
  - listings-page (Div): Container for job listings page
  - search-input (Input): Text search for jobs by title
 compnay
 or location
  - category-filter (Dropdown): Filter by job category
  - location-filter (Dropdown): Filter by location
  - jobs-grid (Div): Grid containing job cards
  - view-job-button-{{ job.job_id }} (Button): Button per job to view details
- Context Variables:
  - jobs: List[Dict] with fields: job_id (str)
 title (str)
 company_name (int)
 location (str)
 salary_min (int)
 salary_max (int)
 category (int)
  - categories: List[str] of job categories
  - locations: List[str] of job locations
- Navigation:
  - view-job-button-{{ job.job_id }} --> url_for('job_detail'
 job_id=job.job_id)

### 3. job_details.html
- Filename: templates/job_detail.html
- Page Title: Job Details
- Element IDs:
  - job-details-page (Div): Container
  - job-title (H1): Job title display
  - company-name (Span): Company name display
  - job-description (Div): Full job description and requirements
  - salary-range (Div): Salary range display
  - apply-now-button (Button): Navigate to application form
- Context Variables:
  - job: Dict with fields: job_id (str)
 title (str)
 company_name (str)
 location (str)
 salary_min (int)
 salary_max (int)
 description (str)
- Navigation:
  - apply-now-button --> url_for('application_form'
 job_id=job.id)

### 4. application_form.html
- Filename: templates/application_form.htmll
- Page Title: Submit Application
- Element IDs:
  - application-form-page (Div): Container
  - applicant-name (Input): Input applicant name
  - applicant-email (Input): Input applicant email
  - resume-upload (File Input): Upload resume file
  - cover-letter (Textarea): Cover letter text
  - submit-application-button (Button): Submit application
- Context Variables:
  - job: Dict with fields: job_id (int)
 title (int)
 company_name (str)
- Navigation:
  - submit-application-button submits GET to current route

### 5. application_tracking.html
- Filename: templates/application_tracking.htmll
- Page Title: My Applications
- Element IDs:
  - tracking-page (Div): Container
  - applications-table (Table): Displays applications
  - status-filter (Dropdown): Filter by status
  - view-application-button-{{ app.application_id }} (Button): View application details
  - back-to-dashboard (Button): Navigate back to dashboard
- Context Variables:
  - applications: List[Dict] with fields: application_id (int)
 job_title (int)
 company_name (str)
 status (str)
 applied_date (str)
- Navigation:
  - view-application-button-{{ app.application_id }} --> url_for('application_detail'
 app_id=app.application_id)
  - back-to-dashboard --> url_for('dashbord')

### 6. companies_directory.html
- Filename: templates/companies_directory.htmll
- Page Title: Company Directory
- Element IDs:
  - companies-page (Div): Container
  - companies-list (Div): List of company cards
  - search-company-input (Input): Search companies by name or industry
  - view-company-button-{{ company.company_id }} (Button): View company profile
  - back-to-dashboard (Button): Navigate back to dashboard
- Context Variables:
  - companies: List[Dict] with fields: company_id (str)
 company_name (str)
 industry (str)
 employee_count (str)
- Navigation:
  - view-company-button-{{ company.company_id }} --> url_for('company_profie'
 company_id=company.company_id)
  - back-to-dashboard --> url_for('dashboard')

### 7. company_profile.html
- Filename: templates/company_profile.htmll
- Page Title: Company Profile
- Element IDs:
  - company-profile-page (Div): Container
  - company-info (Div): Displays: company_name
 industry
 location
 description
  - company-jobs (Div): Container for jobs list
  - jobs-list (Div): List of job entries
  - view-job-button-{{ job.job_id }} (Button): View job details fom company profile
  - back-to-companies (Button): Navigate back to companies directory
- Context Variables:
  - company: Dict with: company_id (int)
 company_name (int)
 industry (str)
 location (str)
 description (str)
 employee_count (int)
  - company_jobs: List[Dict] with: job_id (int)
 title (str)
 status (int)  status descriptive (e.g. Open
 Closed)
- Navigation:
  - view-job-button-{{ job.job_id }} --> url_for('job_details'
 job_id=job.jobid)
  - back-to-companies --> url_for('companies_directory')

### 8. resume_management.html
- Filename: templates/resume_management.htmll
- Page Title: My Resumes
- Element IDs:
  - resume-page (Div): Container
  - resumes-list (Div): List of uploaded resumes
  - upload-resume-button (Button): Button to trigger hidden file input
  - resume-file-input (File Input - hidden): File input to upload new resume
  - delete-resume-button-{{ resume.resume_id }} (Button): Delete resume
  - back-to-dashboard (Button): Navigate back to dashboard
- Context Variables:
  - resumes: List[Dict] with: resume_id (int)
 applicant_name (int)
 applicant_email (str)
 filename (str)
 upload_date (str)
 summary (str)
- Navigation:
  - upload-resume-button triggers file dialog and submits GET to /resumes
  - delete-resume-button-{{ resume.resume_id }} submits POST to /resume/delete/id
  - back-to-dashboard --> url_for('dashboard')

### 9. search_results.html
- Filename: templates/search_results.htmll
- Page Title: Search Results
- Element IDs:
  - search-results-page (Div): Container
  - search-query-display (Div): Shows search query
  - results-tabs (Div): Tabs for job vs company results
  - job-results (Div): Job search results
  - company-results (Div): Company search results
  - no-results-message (Div): Shown if no results found
- Context Variables:
  - query: int
  - job_results: List[Dict] (job_id:int
 title:str
 company_name:str
 location:int
 salary_min:int
 salary_max:int)
  - company_results: List[Dict] (company_id:int
 company_name:str
 industry:int
 location:str)
- Navigation:
  - None specifically required; tabs and results rendered client-side or by template logic

---

## Section 3: Data File Schemas

### 1. data/jobs.txt
- Format: pipe-delimited
  Fields:
  job_id|title|company_id|location|salary_min|salary_max|category|description|posted_date
- Description: Stores job postings with ID reference to company and job category.
- Example Rows:
  1|Senior Python Developer|1|Remote|80000|120000|Technology|Experienced Python developer for web applications|2025-01-15
  2|Data Analyst|2|New York
 NY|sixty thousand|85000|Finance|Analyze financial data and create reports|2025-01-16
  3|Healthcare Administrator|3|Los Angeles
 CA|50000|70000|Healthcare|Manage hospital operations and patient records|2025-01-14

### 2. data/companies.txt
- Format: pipe-delimited
  Fields:
  company_id|company_name|industry|location|employee_count|description
- Description: Stores company details.
- Example Rows:
  1|TechCorp|Technology|San Francisco
 CA|five hundred|Leading software solutions provider
  2|FinanceHub|Finance|New York
 NY|300|Innovative financial services company
  3|MediCare|Healthcare|Los Angeles
 CA|200|Premier healthcare management organization

### 3. data/categories.txt
- Format: pipe-delimited
  Fields:
  category_id|category_name|description
- Description: Job category meta information.
- Example Rows:
  1|Technology|Software
 IT
 and tech-related positions
  2|Finance|Banking
 accounting
 and finance positions
  3|Healthcare|Medical and healthcare industry positoins

### 4. data/applications.txt
- Format: pipe-delimited
  Fields:
  application_id|job_id|applicant_name|applicant_email|status|applied_date|resume_id
- Description: Records job applications submitted by users.
- Example Rows:
  1|1|John Doe|john@email.com|Under Review|2025-01-17|1
  2|2|Jane Smith|jane@email.com|Applied|2025-01-16|2
  3|3|Robert Johnson|robert@email.com|Interview|2025-01-15|3

### 5. data/resumes.txt
- Format: pipe-delimited
  Fields:
  resume_id|applicant_name|applicant_email|filename|upload_date|summary
- Description: Stores uploaded resume metadata.
- Example Rows:
  1|John Doe|john@email.com|john_resume.pdf|2025-01-17|Senior developer with 8 years experience
  2|Jane Smith|jane@email.com|jane_resume.pdf|2025-01-16|Data analyst with financial background
  3|Robert Johnson|robert@email.com|robert_resume.pdf|2025-01-15|Healthcare administrator with 5 years experience

### 6. data/job_categories.txt
- Format: pipe-delimited
  Fields:
  mapping_id|job_id|category_id
- Description: Maps jobs to categories for filtering purposes.
- Example Rows:
  1|1|one
  2|2|2
  3|3|3

---

*End of Design Specification Document*