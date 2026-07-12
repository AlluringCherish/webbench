# JobBoard Web Application Design Specification

---

# Section 1: Flask Routes Specification

| Route Path               | Function Name          | HTTP Method(s) | Template Rendered    | Context Variables Passed to Template                         | 
|-------------------------|------------------------|----------------|---------------------|--------------------------------------------------------------|
| /                       | root_redirect          | GET            | Redirect to /dashboard | None                                                         |
| /dashboard              | dashboard_page          | GET            | dashboard.html       | featured_jobs: List[dict], each with keys: job_id(int), title(str), company_name(str), location(str), salary_min(int), salary_max(int) |
|                         |                        |                |                     | 
| /jobs                   | jobs_listings           | GET            | job_listings.html    | jobs: List[dict], each dict with job_id(int), title(str), company_name(str), location(str), salary_min(int), salary_max(int), category(str) |
|                         |                        |                |                     | filters: dict with keys 'categories' (List[str]) and 'locations' (List[str]) for dropdown options |
|                         |                        | POST           | job_listings.html    | jobs: List[dict] filtered by search and filters, same structure as GET |
| /job/<int:job_id>       | job_details             | GET            | job_details.html     | job: dict with keys job_id(int), title(str), company_name(str), location(str), salary_min(int), salary_max(int), description(str), category(str) |
| /apply/<int:job_id>     | application_form        | GET            | application_form.html| job: dict with job_id(int), title(str), company_name(str)         |
|                         |                         | POST           | application_submitted.html or application_form.html (with errors) | form_fields: "applicant_name"(str), "applicant_email"(str), "resume_file"(file), "cover_letter"(str) - POST request inputs |
| /applications           | application_tracking    | GET            | application_tracking.html | applications: List[dict], each with application_id(int), job_title(str), company_name(str), status(str), applied_date(str) |
|                         |                        | POST           | application_tracking.html | status_filter (str) - filter applications by status: 'All', 'Applied', 'Under Review', 'Interview', 'Rejected'|
| /companies              | companies_directory     | GET            | companies_directory.html | companies: List[dict], each with company_id(int), company_name(str), industry(str), employee_count(int) |
|                         |                        | POST           | companies_directory.html | company_search_query(str) - to search companies by name or industry |
| /company/<int:company_id>| company_profile         | GET            | company_profile.html | company: dict with company_id(int), company_name(str), industry(str), location(str), description(str), employee_count(int) |
|                         |                        |                     | company_jobs: List[dict], each with job_id(int), title(str), status(str, e.g. 'Open') |
| /resumes                | resume_management       | GET            | resume_management.html | resumes: List[dict], each with resume_id(int), filename(str), upload_date(str), summary(str) |
|                         |                        | POST           | resume_management.html | form field: resume_file(file input for uploading new resume) |
| /search                 | search_results          | GET            | search_results.html   | query(str), job_results: List[dict], company_results: List[dict] |


# Section 2: HTML Template Specifications

## 1. dashboard.html
- Filename: templates/dashboard.html
- Page Title: Job Board Dashboard
- Element IDs:
  - dashboard-page (Div): Container for the dashboard page.
  - featured-jobs (Div): Display of featured job recommendations.
  - browse-jobs-button (Button): Navigates to job listings page.
  - my-applications-button (Button): Navigates to applications tracking page.
  - companies-button (Button): Navigates to companies directory page.
- Context Variables:
  - featured_jobs: List[dict], each dict with keys: job_id(int), title(str), company_name(str), location(str), salary_min(int), salary_max(int)
- Navigation Mappings:
  - browse-jobs-button: url_for('jobs_listings')
  - my-applications-button: url_for('application_tracking')
  - companies-button: url_for('companies_directory')

## 2. job_listings.html
- Filename: templates/job_listings.html
- Page Title: Job Listings
- Element IDs:
  - listings-page (Div): Container for the listings page.
  - search-input (Input): To search jobs by title, company, or location.
  - category-filter (Dropdown): Filter by job category.
  - location-filter (Dropdown): Filter by location.
  - jobs-grid (Div): Grid displaying job cards.
  - view-job-button-{{ job.job_id }} (Button): Button to view job details; for each job in jobs list.
- Context Variables:
  - jobs: List[dict] with keys: job_id(int), title(str), company_name(str), location(str), salary_min(int), salary_max(int), category(str)
  - filters: dict with keys 'categories'(List[str]) and 'locations'(List[str])
- Navigation Mappings:
  - view-job-button-{{ job.job_id }}: url_for('job_details', job_id=job.job_id)

## 3. job_details.html
- Filename: templates/job_details.html
- Page Title: Job Details
- Element IDs:
  - job-details-page (Div): Container
  - job-title (H1): Job title
  - company-name (Div): Company name
  - job-description (Div): Full job description and requirements
  - salary-range (Div): Salary range
  - apply-now-button (Button): Navigate to application form page
- Context Variables:
  - job: dict with keys job_id(int), title(str), company_name(str), location(str), salary_min(int), salary_max(int), description(str), category(str)
- Navigation Mappings:
  - apply-now-button: url_for('application_form', job_id=job.job_id)

## 4. application_form.html
- Filename: templates/application_form.html
- Page Title: Submit Application
- Element IDs:
  - application-form-page (Div): Container
  - applicant-name (Input): Applicant name input
  - applicant-email (Input): Applicant email input
  - resume-upload (File Input): Resume upload field
  - cover-letter (Textarea): Cover letter text
  - submit-application-button (Button): Submit application
- Context Variables:
  - job: dict with job_id(int), title(str), company_name(str)
- Navigation Mappings:
  - submit-application-button: submits POST to url_for('application_form', job_id=job.job_id)

## 5. application_tracking.html
- Filename: templates/application_tracking.html
- Page Title: My Applications
- Element IDs:
  - tracking-page (Div): Container
  - applications-table (Table): Displays applications with job title, company, status, date applied
  - status-filter (Dropdown): Filter by application status
  - view-application-button-{{ app.application_id }} (Button): View application details
  - back-to-dashboard (Button): Go back to dashboard
- Context Variables:
  - applications: List[dict], each with application_id(int), job_title(str), company_name(str), status(str), applied_date(str)
- Navigation Mappings:
  - view-application-button-{{ app.application_id }}: url_for('application_tracking') or another route if detailed application page is added
  - back-to-dashboard: url_for('dashboard_page')

## 6. companies_directory.html
- Filename: templates/companies_directory.html
- Page Title: Company Directory
- Element IDs:
  - companies-page (Div): Container
  - companies-list (Div): List of company cards
  - search-company-input (Input): Search companies by name or industry
  - view-company-button-{{ company.company_id }} (Button): View company profile
  - back-to-dashboard (Button): Go back to dashboard
- Context Variables:
  - companies: List[dict], each with company_id(int), company_name(str), industry(str), employee_count(int)
- Navigation Mappings:
  - view-company-button-{{ company.company_id }}: url_for('company_profile', company_id=company.company_id)
  - back-to-dashboard: url_for('dashboard_page')

## 7. company_profile.html
- Filename: templates/company_profile.html
- Page Title: Company Profile
- Element IDs:
  - company-profile-page (Div): Container
  - company-info (Div): Displays company details
  - company-jobs (Div): Display all open jobs
  - jobs-list (Div): List of jobs with titles and status indicators
  - view-job-button-{{ job.job_id }} (Button): View job details
  - back-to-companies (Button): Return to companies directory
- Context Variables:
  - company: dict with company_id(int), company_name(str), industry(str), location(str), description(str), employee_count(int)
  - company_jobs: List[dict], each with job_id(int), title(str), status(str)
- Navigation Mappings:
  - view-job-button-{{ job.job_id }}: url_for('job_details', job_id=job.job_id)
  - back-to-companies: url_for('companies_directory')

## 8. resume_management.html
- Filename: templates/resume_management.html
- Page Title: My Resumes
- Element IDs:
  - resume-page (Div): Container
  - resumes-list (Div): List of uploaded resumes
  - upload-resume-button (Button): Upload new resume
  - resume-file-input (File Input): Hidden file input for resume upload
  - delete-resume-button-{{ resume.resume_id }} (Button): Delete resume
  - back-to-dashboard (Button): Back to dashboard
- Context Variables:
  - resumes: List[dict], each with resume_id(int), filename(str), upload_date(str), summary(str)
- Navigation Mappings:
  - upload-resume-button: triggers file select for resume-file-input, which submits to upload POST route
  - delete-resume-button-{{ resume.resume_id }}: triggers resume delete action
  - back-to-dashboard: url_for('dashboard_page')

## 9. search_results.html
- Filename: templates/search_results.html
- Page Title: Search Results
- Element IDs:
  - search-results-page (Div): Container
  - search-query-display (Div): Displays input search query
  - results-tabs (Div): Tabs to switch between jobs and companies
  - job-results (Div): Shows job search results
  - company-results (Div): Shows company search results
  - no-results-message (Div): Displayed when no results found
- Context Variables:
  - query: str
  - job_results: List[dict], each dict with job_id(int), title(str), company_name(str), location(str), salary_min(int), salary_max(int)
  - company_results: List[dict], each dict with company_id(int), company_name(str), industry(str)
- Navigation Mappings:
  - view-job-button-{{ job.job_id }} (in job-results): url_for('job_details', job_id=job.job_id)
  - view-company-button-{{ company.company_id }} (in company-results): url_for('company_profile', company_id=company.company_id)

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
  - posted_date (YYYY-MM-DD, str)
- Description: Stores all the job postings with detailed info.
- Example rows:
  ```
  1|Senior Python Developer|1|Remote|80000|120000|Technology|Experienced Python developer for web applications|2025-01-15
  2|Data Analyst|2|New York, NY|60000|85000|Finance|Analyze financial data and create reports|2025-01-16
  3|Healthcare Administrator|3|Los Angeles, CA|50000|70000|Healthcare|Manage hospital operations and patient records|2025-01-14
  ```

## 2. data/companies.txt
- Pipe-delimited fields:
  - company_id (int)
  - company_name (str)
  - industry (str)
  - location (str)
  - employee_count (int)
  - description (str)
- Description: Stores company profile information.
- Example rows:
  ```
  1|TechCorp|Technology|San Francisco, CA|500|Leading software solutions provider
  2|FinanceHub|Finance|New York, NY|300|Innovative financial services company
  3|MediCare|Healthcare|Los Angeles, CA|200|Premier healthcare management organization
  ```

## 3. data/categories.txt
- Pipe-delimited fields:
  - category_id (int)
  - category_name (str)
  - description (str)
- Description: Job categories supported by the platform.
- Example rows:
  ```
  1|Technology|Software, IT, and tech-related positions
  2|Finance|Banking, accounting, and finance positions
  3|Healthcare|Medical and healthcare industry positions
  ```

## 4. data/applications.txt
- Pipe-delimited fields:
  - application_id (int)
  - job_id (int)
  - applicant_name (str)
  - applicant_email (str)
  - status (str) (e.g. Applied, Under Review, Interview, Rejected)
  - applied_date (YYYY-MM-DD, str)
  - resume_id (int)
- Description: Records all job applications submitted.
- Example rows:
  ```
  1|1|John Doe|john@email.com|Under Review|2025-01-17|1
  2|2|Jane Smith|jane@email.com|Applied|2025-01-16|2
  3|3|Robert Johnson|robert@email.com|Interview|2025-01-15|3
  ```

## 5. data/resumes.txt
- Pipe-delimited fields:
  - resume_id (int)
  - applicant_name (str)
  - applicant_email (str)
  - filename (str)
  - upload_date (YYYY-MM-DD, str)
  - summary (str)
- Description: Stores uploaded resumes with metadata.
- Example rows:
  ```
  1|John Doe|john@email.com|john_resume.pdf|2025-01-17|Senior developer with 8 years experience
  2|Jane Smith|jane@email.com|jane_resume.pdf|2025-01-16|Data analyst with financial background
  3|Robert Johnson|robert@email.com|robert_resume.pdf|2025-01-15|Healthcare administrator with 5 years experience
  ```

## 6. data/job_categories.txt
- Pipe-delimited fields:
  - mapping_id (int)
  - job_id (int)
  - category_id (int)
- Description: Maps jobs to their categories for complex queries.
- Example rows:
  ```
  1|1|1
  2|2|2
  3|3|3
  ```

---

This document provides complete specifications for backend Flask routing, frontend HTML template design, and all necessary data file schemas for seamless collaborative development of the JobBoard application.
