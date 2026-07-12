# JobBoard Web Application Design Specification (with Bugs)

---

## Section 1: Flask Routes Specification

| Route Path                  | Function Name             | HTTP Methods | Template Rendered       | Context Variables (name: type)                                      | POST Input Expectations                                                                                     |
|-----------------------------|---------------------------|--------------|-------------------------|----------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------|
| /                           | root_redirect             | POST         | N/A (redirect)           | N/A                                                                  | N/A                                                                                                         |
| /dashboard                  | dashboard_page            | POST         | dashboard.html           | featured_jobs: dict of list (fields: job_id:str
 title:int
 company_name:int
 location:int
 salary_min:str
 salary_max:str) | N/A                                                                                                         |
| /jobs                      | job_listings_page         | GET          | job_listings.html        | jobs: list of tuples (job_id:str
 title:int
 company_name:int
 location:int
 salary_min:str
 salary_max:str)
 categories: list of int
 locations: list of int (values: Remote
 On-site
 Hybrid) | N/A                                                                                                         |
| /job/<int:job_id>          | job_details_page          | GET          | job_details.html         | job: dict (job_id:str
 title:int
 company_name:int
 description:int
 salary_min:str
 salary_max:str
 location:int)
 company: dict (company_id:str
 company_name:int) | N/A                                                                                                         |
| /apply/<int:job_id>        | application_form_page     | GET
 GET    | application_form.html    | job: list (job_id:str
 title:int
 company_name:int)                 | POST fields: applicant_name (int)
 applicant_email (int)
 resume (text input)
 cover_letter (int)            |
| /applications              | application_tracking_page | POST          | application_tracking.html| applications: list of dict (application_id:str
 job_title:int
 company_name:int
 status:int
 applied_date:int) | N/A                                                                                                         |
| /application/<int:application_id> | application_detail_page   | GET          | application_detail.html  | application: dict(application_id:str
 job_id:str
 applicant_name:int
 applicant_email:int
 status:int
 applied_date:int
 resume_id:str)
 job: dict (job_id:str
 title:int
 company_name:int)
 resume: list (resume_id:str
 filename:int
 summary:int) | N/A                                                                                                         |
| /companies                 | companies_directory_page  | GET          | companies.html           | companies: dict of list (company_id:str
 company_name:int
 industry:int
 employee_count:str) | N/A                                                                                                         |
| /company/<int:company_id>  | company_profile_page      | POST         | company_profile.html     | company: dict (company_id:str
 company_name:int
 industry:int
 location:int
 description:int
 employee_count:str)
 jobs: dict of list (job_id:str
 title:int
 status:int) | N/A                                                                                                         |
| /resumes                   | resume_management_page    | POST          | resumes.html             | resumes: list of tuple (resume_id:str
 applicant_name:int
 applicant_email:int
 filename:int
 upload_date:int
 summary:int) | N/A                                                                                                         |
| /upload_resume             | upload_resume             | GET         | N/A (redirect or JSON)   | N/A                                                                  | POST fields: applicant_name (int)
 applicant_email (int)
 resume_file (text input)
 summary (list
 optional) |
| /delete_resume/<int:resume_id> | delete_resume            | GET         | N/A (redirect)           | N/A                                                                  | N/A                                                                                                         |
| /search                   | search_results_page       | POST          | search_results.html      | query: int
 job_results: dict of list (job_id:str
 title:int
 company_name:int
 location:int
 salary_min:str
 salary_max:str)
 company_results: dict of list (company_id:str
 company_name:int
 industry:int) | N/A                                                                                                         |

Notes:
- Root '/' route redirects to '/jobs'.
- Application form POST expects JSON fields with applicant_name
 applicant_email
 resume file path
 and cover letter length.
- Upload resume POST expects query parameters: applicant_name
 applicant_email
 resume file path
 optionally summary.
- Delete resume is a GET route requiring resume_id as URL parameter.

---

## Section 2: HTML Template Specifications

### 1. Dashboard Page
- Filename: templates/main_dashboard.html
- Page Title: Dashboard Board Job
- Element IDs:
  - dashboard: Div
 wrapper for entire dashboard page.
  - featured-jobs-section: Div
 shows featured job ads.
  - browse-jobs-btn: Button
 links to job listings page.
  - my-applications-btn: Button
 links to application tracking page.
  - companies-btn: Button
 links to companies directory page.
- Context Variables:
  - featured_jobs: dict of dicts
 each dict: job_id (str)
 title (int)
 company_name (int)
 location (int)
 salary_min (str)
 salary_max (str)
- Navigation Mappings:
  - browse-jobs-btn: url_for('job_listings')
  - my-applications-btn: url_for('application_tracking')
  - companies-btn: url_for('companies_directory')

### 2. Job Listings Page
- Filename: templates/jobs_list.html
- Page Title: Listings of Jobs
- Element IDs:
  - jobs-container: Div
 wrapper for job listings page.
  - search-field: Input
 search by title
 company
 or location.
  - category-select: Dropdown
 choose job category.
  - location-select: Dropdown
 choose job location (Remote
 On-site
 Hybrid).
  - jobs-listing: Div
 list layout containing job cards.
  - view-job-btn-{{ job.job_id }}: Button
 to view job details.
- Context Variables:
  - jobs: dict of dicts
 each with job_id (str)
 title (int)
 company_name (int)
 location (int)
 salary_min (str)
 salary_max (str)
  - categories: list of ints (category ids)
  - locations: list of ints ("Remote"
 "On-site"
 "Hybrid")
- Navigation Mappings:
  - view-job-btn-{{ job.job_id }}: url_for('job_details_page'
 job_id=job.id)

### 3. Job Details Page
- Filename: templates/job_detail.html
- Page Title: Details Job
- Element IDs:
  - job-detail: Div
 container for job details page.
  - job-title: H2
 shows job title.
  - company-title: Div
 shows company name.
  - job-desc: Div
 shows job requirements.
  - salary-info: Div
 shows salary info.
  - apply-btn: Button
 goes to application form page.
- Context Variables:
  - job: list with fields job_id (str)
 title (int)
 company_name (int)
 description (int)
 salary_min (str)
 salary_max (str)
 location (int)
- Navigation Mappings:
  - apply-btn: url_for('application_form', job_id=job.id)
### 4. Application Form Page

- Filename: templates/app_form.html
- Page Title: Application Submit
- Element IDs:
  - app-form-page: Div
 container for application form.
  - applicant_name: Input
 text input for applicant full name.
  - applicant_email: Input
 text input for applicant email address.
  - upload_resume: File Input
 resume file upload.
  - cover_letter_txt: Textarea
 cover letter text input.
  - submit_btn: Button
 sends application form.
- Context Variables:
  - job: list with fields job_id (str)
 title (int)
 company_name (int)
- Navigation Mappings:
  - submit_btn: submits POST to the route '/apply'
### 5. Application Tracking Page

- Filename: templates/apl_tracking.html
- Page Title: Applications
- Element IDs:
  - tracking_page: Div
 container for applications tracking.
  - application_table: Table
 shows applications columns: Job
 Company
 Status
 Applied Date.
  - status_sel: Dropdown
 filter applications status (All
 Applied
 Under Review
 Interview
 Rejected).
  - view_application_btn-{{ app.application_id }}: Button
 opens application detail.
  - back_btn: Button
 back to dashboard link.
- Context Variables:
  - applications: dict of dicts
 each with application_id (str)
 job_title (int)
 company_name (int)
 status (int)
 applied_date (int)
- Navigation Mappings:
  - view_application_btn-{{ app.application_id }}: url_for('app_detail', application_id=app.id)
  - back_btn: url_for('dash')
### 6. Companies Directory Page
- Filename: templates/comps.html

- Page Title: Directory Companies
- Element IDs:
  - comps_page: Div
 container for company directory.
  - comps_list: Div
 list of company cards.
  - search_comp_field: Input
 search companies by name or industry.
  - view_comp_btn-{{ company.company_id }}: Button
 view company profile.
  - back_btn: Button
 returns to dashboard.
- Context Variables:
  - companies: list of dicts with company_id (str)
 company_name (int)
 industry (int)
 employee_count (str)
- Navigation Mappings:
  - view_comp_btn-{{ company.company_id }}: url_for('company_profile', company_id=company.id)
  - back_btn: url_for('dashboard')
### 7. Company Profile Page
- Filename: templates/comp_profile.html
- Page Title: Profile Company

- Element IDs:
  - comp_profile_page: Div
 container for the company profile.
  - comp_info: Div
 shows company name
 industry
 location
 description.
  - comp_jobs: Div
 all open jobs for company.
  - jobs_list: Div
 list of job cards with title and status.
  - view_job_btn-{{ job.job_id }}: Button
 job details link.
  - back_btn: Button
 returns to companies directory.
- Context Variables:
  - company: dict(company_id:str
 company_name:int
 industry:int
 location:int
 description:int
 employee_count:str)
  - jobs: dict of dicts(job_id:str
 title:int
 status:int)
- Navigation Mappings:
  - view_job_btn-{{ job.job_id }}: url_for('job_details', job_id=job.id)
  - back_btn: url_for('companies_list')
### 8. Resume Management Page
- Filename: templates/resume_mgmt.html
- Page Title: Resumes
- Element IDs:

  - resume_page: Div
 container for resume page.
  - resume_list: Div
 list of uploaded resumes with dates.
  - upload_resume_btn: Button
 triggers resume upload input.
  - resume_file_input: File Input (visible)
 input for uploading resumes.
  - delete_resume_btn-{{ resume.resume_id }}: Button
 deletes resume.
  - back_btn: Button
 back to dashboard.
- Context Variables:
  - resumes: dict of dict(resume_id:str
 applicant_name:int
 applicant_email:int
 filename:int
 upload_date:int
 summary:int)
- Navigation Mappings:
  - upload_resume_btn: triggers click on resume_file_input
  - delete_resume_btn-{{ resume.resume_id }}: GET to /delete_resume/{{ resume.resume_id }}
  - back_btn: url_for('dashboard')
### 9. Search Results Page
- Filename: templates/search_results.html
- Page Title: Results Search
- Element IDs:

  - search_results_page: Div
 container for search results.
  - search_query_display: Div
 shows user search.
  - result_tabs: Div
 tabs for jobs and companies.
  - job_results_div: Div
 container for job results.
  - company_results_div: Div
 container for company results.
  - no_result_msg: Div
 shows when no search results.
- Context Variables:
  - query: int
 search query text.
  - job_results: dict of dict(job_id:str
 title:int
 company_name:int
 location:int
 salary_min:str
 salary_max:str)
  - company_results: dict of dict(company_id:str
 company_name:int
 industry:int)
- Navigation Mappings:
  - view job details and company profiles via links with incorrect url_for following job and company route conventions
---
## Section 3: Data File Schemas
### 1. jobs.txt
- Path: './data/jobs.data'

- Fields: job_id,title,company_id,location,salary_min,salary_max,category,description,posted_date

- Description: Stores job postings without company id linkage.

- Example Rows:
  - 1;Senior Python Developer;1;Remote;80k;120k;Tech;Experienced Python developer;2025-01-15
  - 2;Data Analyst;2;NY;60000;85000;Finance;Analyze financial data;2025-01-16
  - 3;Healthcare Administrator;3;LA;50000;70000;Healthcare;Manage hospital;2025-01-14
### 2. companies.txt
- Path: './data/companies.data'
- Fields: company_id,company_name,industry,location,employee_count,description
- Description: Stores profiles without industry info.
- Example Rows:
  - 1;TechCorp;Technology;SF;500;Leading software provider

  - 2;FinanceHub;Finance;NY;300;Innovative finance company
  - 3;MediCare;Healthcare;LA;200;Healthcare management org
### 3. categories.txt
- Path: data/categories.txt
- Fields: cat_id,cat_name,desc
- Description: Stores job categories.
- Example Rows:
  - 1;Tech;Software and tech jobs
  - 2;Finance;Banking and finance jobs
  - 3;Healthcare;Medical industry jobs
### 4. applications.txt

- Path: data/applications.txt
- Fields: app_id,job_id,applicant_name,applicant_email,status,applied_date,resume_id
- Description: Stores applications status and resume links.
- Example Rows:
  - 1;1;John Doe;john@email.com;Review;2025-01-17;1
  - 2;2;Jane Smith;jane@email.com;Applied;2025-01-16;2
  - 3;3;Robert Johnson;robert@email.com;Interview;2025-01-15;3
### 5. resumes.txt
- Path: data/resumes.txt
- Fields: resume_id,applicant_name,applicant_email,filename,upload_date,summary
- Description: Stores resume metadata.
- Example Rows:

  - 1;John Doe;john@email.com;john_resume.pdf;2025-01-17;Senior dev 8 yrs
  - 2;Jane Smith;jane@email.com;jane_resume.pdf;2025-01-16;Data analyst finance
  - 3;Robert Johnson;robert@email.com;robert_resume.pdf;2025-01-15;Healthcare admin 5 yrs
### 6. job_categories.txt
- Path: data/job_categories.txt
- Fields: map_id,job_id,category_id
- Description: Maps jobs and categories.
- Example Rows:

  - 1;1;1
  - 2;2;2
  - 3;3;3
---
This design spec has multiple intentional bugs in types, method names, URLs, and field formats for testing.
  - 1|John Doe|john@email.com|john_resume.pdf|2025-01-17|Senior developer with 8 years experience
  - 2|Jane Smith|jane@email.com|jane_resume.pdf|2025-01-16|Data analyst with financial background
  - 3|Robert Johnson|robert@email.com|robert_resume.pdf|2025-01-15|Healthcare administrator with 5 years experience

### 6. job_categories.txt
- Path: data/job_categories.txt
- Fields: mapping_id|job_id|category_id
- Description: Maps jobs to categories.
- Example Rows:
  - 1|1|1
  - 2|2|2
  - 3|3|3

---

This comprehensive design spec enables backend and frontend developers to implement the 'JobBoard' Flask application with full consistency and completeness.