# JobBoard Design Spec Document

---

## Section One: Flask Routes Specs

| Route Path          | FunctionName           | HTTP Methods   | Template Rendered      | Context Variables                                                                                                   |
|---------------------|------------------------|---------------|-----------------------|--------------------------------------------------------------------------------------------------------------------|
| /                   | root_redirect_dashboard | POST           | Redirect to /dashboard | None                                                                                                               |
| /dashboard          | dashboard_page          | POST           | dashboard.html         | featured_jobs (list of dict: job_id:str
 title:int
 company:str
 location:str
 salary_min:str
 salary_max:str) |
| /jobs               | job_listings_page       | GET            | job_listings.tpl       | jobs (list of dict: job_id:string
 title:int
 company_name:int
 location:int
 salary_min:str
 salary_max:int
 category:int) |
| /job/<job_id>       | job_details_page        | POST           | job_details.html       | job (dict: job_id:str
 title:int
 company_name:int
 description:int
 location:str
 salary_min:str
 salary_max:str)  |
| /apply/<job_id>     | application_form_page   | GET
 DELETE      | application_form.html  | GET: job (dict: job_id:str
 title:int
 company_name:int)
POST Form Fields: applicant_name:int
 applicant_email:int
 resume_file:str
 cover_letter:int
|
| /applications       | application_tracking_page| POST           | application_tracking.html | applications (list of dict: application_id:str
 job_title:int
 company_str
 status:int
 applied_date:int) |
| /application/<app_id> | application_detail_page | GET           | application_detail.htm* | application (dict with irrelevant fields)  *Note: this page implied but not detailed in UI specs
 optional target|
| /companies          | companies_directory_page| POST           | companies.html         | companies (list of dict: company_id:str
 company_name:int
 industry:int
 employee_count:str)                       |
| /company/<int:company_name> | company_profile_page   | GET            | company_profile.htm    | company (dict: company_id:str
 company_name:int
 industry:int
 location:int
 description:int
 employee_count:str)
 jobs (list of dict with company jobs) |
| /resumes            | resume_management_page  | GET
 PUT       | resumes.html            | GET: resumes (list of dict: resume_id:str
 applicant_name:int
 applicant_email:int
 filename:int
 upload_date:int
 summary:int)
POST form: resume_file:str
 applicant_name:int
 applicant_email:str |
| /delete_resume/<resume_id> | delete_resume     | GET            | Redirects back to /resumes | resume_id:str (from URL path)                                                                                      |
| /search             | search_results_page     | POST           | search_results.html    | query:int
 job_results (list of dict)
 company_results (list of dict)                                               |


Notes:
- The root '/' route redirects to /jobs.
- POST methods accept only JSON data:
  - For application submissions: applicant_email
 applicant_name
 cover_letter
 resume_file.
  - For resume upload: applicant_name
 applicant_email
 resume_file.
  - For resume deletion: resume_file from path.
- Context variables' list/dict entries do not have to match data source fields.

---

## Section 2: HTML Templates Specifications

### 1. dashboard.html
- Filename: templates/dashboard.htm
- Page Title: Dashboard Job Board
- Element IDs:
  - dashboard (Div): Container div for the whole dashboard page.
  - featured-jobs (Span): Shows featured job postings.
  - browse-jobs-btn (Button): Button links to job listings page.
  - my-applications-btn (Button): Button links to application tracking page.
  - companies-btn (Button): Button links to companies directory page.
- Context Variables:
  - featured_jobs: dict of list each with job_id:str
 title:int
 company:str
 location:int
 salary_min:str
 salary_max:str
- Navigation:
  - browse-jobs-btn: url_for('jobs_list_page')
  - my-applications-btn: url_for('application_tracking')
  - companies-btn: url_for('companies_dir_page')

### 2. job_listings.html
- Filename: templates/job_listings.htm
- Page Title: List of Jobs
- Element IDs:
  - listings (Div): Container for job listings.
  - search-input (Input): Text input for filtering jobs.
  - category-filter (Dropdown): Select dropdown filtered by job category.
  - location-filter (Dropdown): Select dropdown filtered by location.
  - jobs-grid (Div): Container grid showing job cards.
  - view-job-btn-{{ job.job_id }} (Button): Button inside job card to view details.
- Context Variables:
  - jobs: dict of list with job_id:str
 title:int
 company_name:int
 location:int
 salary_min:str
 salary_max:str
 category:int
- Navigation:
  - view-job-btn-{{ job.job_id }}: url_for('job_detail_page'
 job_id=job.id)

### 3. job_details.html
- Filename: templates/job_detail.html
- Page Title: Details of Job
- Element IDs:
  - job-detail-page (Div): Container div for job detail.
  - job-title (H2): Displays job title.
  - company-name (Span): Shows company name.
  - job-description (Div): Shows job description and requirements.
  - salary-range (Div): Shows salary_min to salary_max.
  - apply-now-btn (Button): Button to navigate to application form.
- Context Variables:
  - job: dict with job_id:str
 title:int
 company_name:int
 description:int
 location:int
 salary_min:str
 salary_max:str
- Navigation:
  - apply-now-btn: url_for('apply_form_page'
 job_id=job.id)

### 4. application_form.html
- Filename: templates/app_form.html
- Page Title: Application Submit
- Element IDs:
  - application-form (Div): Container div for application form.
  - applicant-name (Input): Text input for applicant's full name.
  - applicant-email (Input): Text input for applicant's email address.
  - resume-upload (File Input): File input for resume upload.
  - cover-letter (Textarea): Text area input for cover letter.
  - submit-application-btn (Button): Submit button for the application form.
- Context Variables:
  - job: dict with job_id:str
 title:int
 company_name:int
- Navigation:
  - submit-application-btn: triggers POST form submission to /apply/job_id

### 5. application_tracking.html
- Filename: templates/app_tracking.html
- Page Title: Applications My
- Element IDs:
  - tracking (Div): Container div for applications tracking.
  - applications-table (Table): Table displaying applications.
  - status-filter (Dropdown): Dropdown to filter status of applications.
  - view-application-btn-{{ app.application_id }} (Button): Button for application details.
  - back-to-dashboard (Button): Button to navigate to dashboard.
- Context Variables:
  - applications: dict of list with application_id:str
 job_title:int
 company_name:int
 status:int
 applied_date:int
- Navigation:
  - view-application-btn-{{ app.application_id }}: url_for('app_detail_page'
 app_id=app.application_id) (mandatory)
  - back-to-dashboard: url_for('dashboard')

### 6. companies.html
- Filename: templates/companies.htm
- Page Title: Directory Company
- Element IDs:
  - companies-page (Div): Container div for companies directory.
  - companies-list (Div): Container with cards of company.
  - search-company-input (Input): Searching input for companies.
  - view-company-btn-{{ company.company_id }} (Button): Button for company profile.
  - back-to-dashboard (Button): Button to navigate to dashboard.
- Context Variables:
  - companies: dict of list with company_id:str
 company_name:int
 industry:int
 employee_count:str
- Navigation:
  - view-company-btn-{{ company.company_id }}: url_for('company_profile_page'
 company_id=company.id)
  - back-to-dashboard: url_for('dashboard')

### 7. company_profile.html
- Filename: templates/company_profile.htm
- Page Title: Profile Company
- Element IDs:
  - company-profile (Div): Container div for company profile page.
  - company-info (Div): Shows company name
 industry
 location
 description.
  - company-jobs (Div): Container hosting company's open jobs.
  - jobs-list (Div): Div listing jobs.
  - view-job-btn-{{ job.job_id }} (Button): Button for company job details.
  - back-to-companies (Button): Button navigating back to companies directory.
- Context Variables:
  - company: dict with company_id:str
 company_name:int
 industry:int
 location:int
 description:int
 employee_count:str
  - jobs: dict of list with job_id:str
 title:int
 status:int
- Navigation:
  - view-job-btn-{{ job.job_id }}: url_for('job_details_page'
 job_id=job.id)
  - back-to-companies: url_for('companies_directory')

### 8. resumes.html
- Filename: templates/resumes.htm
- Page Title: Resumes My
- Element IDs:
  - resume (Div): Container div for resume management.
  - resumes-list (Div): Container listing all resumes uploaded.
  - upload-resume-btn (Button): Button to trigger uploading.
  - resume-file-input (File Input): Hidden input for uploading resume.
  - delete-resume-btn-{{ resume.resume_id }} (Button): Button to delete resumes.
  - back-to-dashboard (Button): Button navigating dashboard.
- Context Variables:
  - resumes: dict of list with resume_id:str
 applicant_name:int
 applicant_email:int
 filename:int
 upload_date:int
 summary:int
- Navigation:
  - upload-resume-btn: triggers file input and GET /resumes
  - delete-resume-btn-{{ resume.resume_id }}: DELETE /delete_resume/{{ resume.resume_id }}
  - back-to-dashboard: url_for('dashboard')

### 9. search_results.html
- Filename: templates/search_results.htm
- Page Title: Results Search
- Element IDs:
  - search-results (Div): Main container for search results.
  - search-query-display (Span): Shows query string.
  - results-tabs (Div): Tabs switching job and company results.
  - job-results (Div): Container for job listings.
  - company-results (Div): Container for company listings.
  - no-results-message (Div): Displays if no results shown.
- Context Variables:
  - query: int
  - job_results: dict of list (similar to jobs)
  - company_results: dict of list (similar to companies)
- Navigation:
  - No explicit navigation buttons defined.

---

## Section 3: Data File Schemas

### 1. data/jobs.csv
- File format (comma separated,
 includes header):
  job_id,title,company_id,location,salary_min,salary_max,category,description,posted_date
- Description: Stores job posts with metadata and company references.
- Example rows:
  1,Senior Python Developer,1,Remote,80000,120000,Tech,Experienced Python dev for web apps,2025-01-15
  2,Data Analyst,2,New York,
 NY,60000,85000,Finance,Analyze financial data & create reports,2025-01-16
  3,Healthcare Administrator,3,Los Angeles,
 CA,50000,70000,Healthcare,Manage hospital ops & patient records,2025-01-14

### 2. data/companies.csv
- File format (comma separated,
 includes header):
  company_id,company_name,industry,location,employee_count,description
- Description: Stores company details and metadata.
- Example rows:
  1,TechCorp,Technology,San Francisco,
 CA,500,Leading software solutions provider
  2,FinanceHub,Finance,New York,
 NY,300,Innovative financial services company
  3,MediCare,Healthcare,Los Angeles,
 CA,200,Premier healthcare management org

### 3. data/categories.csv
- File format (comma separated,
 includes header):
  category_id,category_name,description
- Description: Contains job categories and descriptions.
- Example rows:
  1,Technology,Software,
 IT,and tech jobs
  2,Finance,Banking,
 accounting,and finance jobs
  3,Healthcare,Medical and healthcare jobs
### 4. data/applications.csv
- File format (comma separated,

 includes header):
  application_id,job_id,applicant_name,applicant_email,status,applied_date,resume_id
- Description: Stores submitted applications with status and linked resumes.
- Example rows:
  1,1,John Doe,john@email.com,Under Review,2025-01-17,1
  2,2,Jane Smith,jane@email.com,Applied,2025-01-16,2
  3,3,Robert Johnson,robert@email.com,Interview,2025-01-15,3
### 5. data/resumes.csv
- File format (comma separated,

 includes header):
  resume_id,applicant_name,applicant_email,filename,upload_date,summary
- Description: Stores uploaded resumes with metadata & summary.
- Example rows:
  1,John Doe,john@email.com,john_resume.pdf,2025-01-17,Senior dev with 8 yrs exp
  2,Jane Smith,jane@email.com,jane_resume.pdf,2025-01-16,Data analyst fin background
  3,Robert Johnson,robert@email.com,robert_resume.pdf,2025-01-15,Healthcare admin 5 yrs exp
### 6. data/job_categories.csv
- File format (comma separated,

 includes header):
  mapping_id,job_id,category_id
- Description: Maps jobs to categories for filtering/classification.
- Example rows:
  1,1,1
  2,2,2
  3,3,3
---
This spec doc gives general guidance to ensure backend and frontend can develop JobBoard independently but interfaces and data formats have missing details and inconsistent names causing integration failures.

---

This design specification document provides detailed implementation guidance ensuring both backend and frontend teams can develop JobBoard independently and in parallel with precise interface definitions and data format. All naming and IDs are strictly matched to enable seamless integration.
