# JobBoard Web Application Design Specification

---

## 1. Flask Routes and Templates

| Route Path               | HTTP Method(s) | Template File           | Context Variables Passed to Template                                    |
|--------------------------|----------------|-------------------------|--------------------------------------------------------------------------|
| /dashboard               | GET            | dashboard.html          | featured_jobs (list of featured job dicts), latest_jobs (list of job dicts) |
| /jobs                   | GET            | job_listings.html       | jobs (list of all job dicts), categories (list of category dicts), locations (list of location strings) |
| /job/<int:job_id>        | GET            | job_details.html        | job (job dict), company (company dict)                                  |
| /apply/<int:job_id>      | GET, POST      | application_form.html   | job (job dict)                                                          |
| /applications            | GET            | applications_tracking.html | applications (list of application dicts), filter_status (string)       |
| /application/<int:app_id>| GET            | application_details.html (Not specified but implied for detail view) | application (application dict), job (job dict)                          |
| /companies               | GET            | companies_directory.html| companies (list of company dicts)                                       |
| /company/<int:company_id>| GET            | company_profile.html    | company (company dict), jobs (list of job dicts belonging to company)  |
| /resumes                 | GET, POST      | resume_management.html  | resumes (list of resume dicts)                                          |
| /resume/delete/<int:resume_id> | POST       | (no template - redirect) | N/A                                                                    |
| /search                  | GET            | search_results.html     | query (string), job_results (list of job dicts), company_results (list of company dicts) |


## 2. Page Elements and Layout

### 1. Dashboard Page
- Page Title: Job Board Dashboard
- Element IDs:
  - dashboard-page (Div): Main container
  - featured-jobs (Div): Shows featured job recommendations
  - browse-jobs-button (Button): Navigate to Job Listings page (/jobs)
  - my-applications-button (Button): Navigate to Application Tracking page (/applications)
  - companies-button (Button): Navigate to Companies Directory page (/companies)

### 2. Job Listings Page
- Page Title: Job Listings
- Element IDs:
  - listings-page (Div): Container for job listings
  - search-input (Input): Search field for job title, company, or location
  - category-filter (Dropdown): Filter jobs by category
  - location-filter (Dropdown): Filter jobs by location (Remote, On-site, Hybrid)
  - jobs-grid (Div): Grid containing job cards
  - view-job-button-{job_id} (Button): Button on each job card to view job details (/job/<job_id>)

### 3. Job Details Page
- Page Title: Job Details
- Element IDs:
  - job-details-page (Div): Container for job details
  - job-title (H1): Displays job title
  - company-name (Div): Displays company name
  - job-description (Div): Displays full job description and requirements
  - salary-range (Div): Displays salary range
  - apply-now-button (Button): Button to apply for job (/apply/<job_id>)

### 4. Application Form Page
- Page Title: Submit Application
- Element IDs:
  - application-form-page (Div): Container for the form
  - applicant-name (Input): Applicant's name
  - applicant-email (Input): Applicant's email
  - resume-upload (File Input): Upload resume file
  - cover-letter (Textarea): Text field for cover letter
  - submit-application-button (Button): Submits application form

### 5. Application Tracking Page
- Page Title: My Applications
- Element IDs:
  - tracking-page (Div): Container for tracking page
  - applications-table (Table): Shows applications with job title, company, status, date applied
  - status-filter (Dropdown): Filter applications by status (All, Applied, Under Review, Interview, Rejected)
  - view-application-button-{app_id} (Button): View details of each application (/application/<app_id>)
  - back-to-dashboard (Button): Navigate back to dashboard (/dashboard)

### 6. Companies Directory Page
- Page Title: Company Directory
- Element IDs:
  - companies-page (Div): Container for companies directory
  - companies-list (Div): List of company cards
  - search-company-input (Input): Search companies by name or industry
  - view-company-button-{company_id} (Button): View company profile (/company/<company_id>)
  - back-to-dashboard (Button): Navigate back to dashboard (/dashboard)

### 7. Company Profile Page
- Page Title: Company Profile
- Element IDs:
  - company-profile-page (Div): Container for company profile
  - company-info (Div): Shows company name, industry, location, description
  - company-jobs (Div): Shows open jobs for the company
  - jobs-list (Div): List of jobs with titles and status indicators
  - view-job-button-{job_id} (Button): View job details (/job/<job_id>)
  - back-to-companies (Button): Navigate back to companies directory (/companies)

### 8. Resume Management Page
- Page Title: My Resumes
- Element IDs:
  - resume-page (Div): Container for resume management
  - resumes-list (Div): List of uploaded resumes with upload date
  - upload-resume-button (Button): Trigger hidden file input for upload
  - resume-file-input (File Input): Hidden file input for resume upload
  - delete-resume-button-{resume_id} (Button): Delete resume action
  - back-to-dashboard (Button): Navigate back to dashboard (/dashboard)

### 9. Search Results Page
- Page Title: Search Results
- Element IDs:
  - search-results-page (Div): Main container for search results
  - search-query-display (Div): Displays the search query entered
  - results-tabs (Div): Tabs to toggle between job results and company results
  - job-results (Div): Container for job search results
  - company-results (Div): Container for company search results
  - no-results-message (Div): Displayed if no results found


## 3. Navigation Flow

- The application starts at the **Dashboard page** (/dashboard).
- From Dashboard:
  - Click **browse-jobs-button** -> navigates to Job Listings page (/jobs)
  - Click **my-applications-button** -> navigates to Application Tracking page (/applications)
  - Click **companies-button** -> navigates to Companies Directory page (/companies)
- From Job Listings (/jobs):
  - Use **search-input**, **category-filter**, and **location-filter** for filtering jobs.
  - Click any **view-job-button-{job_id}** -> navigates to Job Details page (/job/<job_id>)
- From Job Details (/job/<job_id>):
  - Click **apply-now-button** -> navigates to Application Form page (/apply/<job_id>)
- From Application Form (/apply/<job_id>):
  - Submit form with **submit-application-button** posts application data.
  - Upon success, navigate back or show confirmation.
- From Application Tracking (/applications):
  - Use **status-filter** to filter application list.
  - Click **view-application-button-{app_id}** for application details.
  - Click **back-to-dashboard** -> returns to Dashboard.
- From Companies Directory (/companies):
  - Use **search-company-input** to search companies.
  - Click **view-company-button-{company_id}** -> Company Profile page (/company/<company_id>)
  - Click **back-to-dashboard** -> returns to Dashboard.
- From Company Profile (/company/<company_id>):
  - Click **view-job-button-{job_id}** -> Job Details page (/job/<job_id>)
  - Click **back-to-companies** -> Companies Directory page (/companies)
- From Resume Management (/resumes):
  - Click **upload-resume-button** triggers **resume-file-input** upload
  - Click **delete-resume-button-{resume_id}** deletes resume
  - Click **back-to-dashboard** -> Dashboard page (/dashboard)
- From Search Results (/search):
  - Displays results for both jobs and companies.


## 4. Data File Integration

### Data Files Location: `data/`

### 1. Jobs Data - `jobs.txt`
- Format: `job_id|title|company_id|location|salary_min|salary_max|category|description|posted_date`
- Read to load job listings and details.
- Write when adding job postings (if application expands, though not currently specified).

### 2. Companies Data - `companies.txt`
- Format: `company_id|company_name|industry|location|employee_count|description`
- Read to display company directory and profiles.
- No write operations specified (no company creation in requirements).

### 3. Categories Data - `categories.txt`
- Format: `category_id|category_name|description`
- Read to populate category filters in job listings and categorize jobs.

### 4. Applications Data - `applications.txt`
- Format: `application_id|job_id|applicant_name|applicant_email|status|applied_date|resume_id`
- Read to display applications in tracking page.
- Write upon submission of new applications in Application Form page.

### 5. Resumes Data - `resumes.txt`
- Format: `resume_id|applicant_name|applicant_email|filename|upload_date|summary`
- Read to display resumes in resume management.
- Write on upload and delete operations.

### 6. Job Categories Mapping Data - `job_categories.txt`
- Format: `mapping_id|job_id|category_id`
- Read for mapping jobs to categories in listings and filters.

---

This design specification document provides a detailed blueprint for frontend and backend implementation of the JobBoard application using Flask with local text file data management.

All element IDs, routes, templates, navigation flows, and data file formats are specified to ensure independent and complete development.

End of Specification.
