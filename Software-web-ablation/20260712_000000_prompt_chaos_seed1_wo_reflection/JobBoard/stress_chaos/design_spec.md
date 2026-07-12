# JobBoard Web Application Design Specification

---

## Section 1: Flask Routes Specification

| Route Path             | Function Name             | HTTP Methods | Template Rendered      | Context Variables Passed                         | Description / Input Expectations                         |
|------------------------|---------------------------|--------------|-----------------------|-------------------------------------------------|----------------------------------------------------------|
| /                      | root_redirect              | GET          | Redirects to /dashboard| None                                            | Redirect root URL to dashboard page                       |
| /dashboard             | dashboard                 | GET          | dashboard.html        | featured_jobs (list of dict), e.g. [{job_id:int, title:str, company_name:str, location:str, salary_min:int, salary_max:int}] | Display main dashboard page with featured jobs           |
| /jobs                  | job_listings              | GET          | job_listings.html     | jobs (list of dict), categories (list of dict), selected_category (str), selected_location (str), search_query (str) | Display all jobs with filtering and search                |
| /job/<int:job_id>       | job_details               | GET          | job_details.html      | job (dict), company (dict)                         | Show detailed job info                                   |
| /apply/<int:job_id>     | application_form          | GET, POST    | application_form.html | job (dict)                                       | GET shows form, POST expects form fields: applicant_name (str), applicant_email (str), resume_file (file upload), cover_letter (str) |
| /applications          | application_tracking      | GET          | application_tracking.html | applications (list of dict), status_filter (str)        | Show all applications, filterable by status              |
| /application/<int:app_id> | view_application          | GET          | application_details.html | application (dict), job (dict), resume (dict)           | View details of an application                            |
| /companies             | companies_directory       | GET          | companies_directory.html | companies (list of dict), search_query (str)              | List all companies with search                            |
| /company/<int:company_id>| company_profile          | GET          | company_profile.html  | company (dict), jobs (list of dict)                 | Show company details and jobs                            |
| /resumes               | resume_management         | GET, POST    | resumes.html          | resumes (list of dict)                              | GET shows resumes list; POST uploads a resume file with applicant_name, applicant_email, filename, summary |
| /resumes/delete/<int:resume_id> | delete_resume           | POST         | Redirects to /resumes | None                                            | Deletes resume with given ID                              |
| /search                | search_results            | GET          | search_results.html   | query (str), job_results (list of dict), company_results (list of dict) | Display search results for jobs and companies            |

Notes:
- All POST routes should validate inputs.
- Each dict in lists must contain fields specifically named to ensure consistent data access.

---

## Section 2: HTML Template Specifications

### 1. dashboard.html
- Filename: templates/dashboard.html
- Page Title: Job Board Dashboard
- Context Variables:
  - featured_jobs: list of dict with keys: job_id:int, title:str, company_name:str, location:str, salary_min:int, salary_max:int
- Elements:
  - div#dashboard-page: container div for dashboard
  - div#featured-jobs: displays featured job cards showing title, company, location, salary
  - button#browse-jobs-button: navigates to job listings (url_for('job_listings'))
  - button#my-applications-button: navigates to application tracking (url_for('application_tracking'))
  - button#companies-button: navigates to companies directory (url_for('companies_directory'))

### 2. job_listings.html
- Filename: templates/job_listings.html
- Page Title: Job Listings
- Context Variables:
  - jobs: list of dict with keys: job_id(int), title(str), company_name(str), location(str), salary_min(int), salary_max(int), category(str)
  - categories: list of dict with keys: category_id(int), category_name(str)
  - selected_category: str selected filter
  - selected_location: str selected location filter
  - search_query: str search input
- Elements:
  - div#listings-page
  - input#search-input: text input for search
  - select#category-filter: dropdown for category filter
  - select#location-filter: dropdown for location filter
  - div#jobs-grid: grid container for job cards
  - Each job card includes button#view-job-button-{{ job.job_id }} to view details (links to url_for('job_details', job_id=job.job_id))

### 3. job_details.html
- Filename: templates/job_details.html
- Page Title: Job Details
- Context Variables:
  - job: dict with fields: job_id, title, description, location, salary_min, salary_max, posted_date
  - company: dict with fields: company_id, company_name
- Elements:
  - div#job-details-page
  - h1#job-title (job.title)
  - div#company-name (company.company_name)
  - div#job-description (job.description)
  - div#salary-range (salary_min - salary_max)
  - button#apply-now-button (links to url_for('application_form', job_id=job.job_id))

### 4. application_form.html
- Filename: templates/application_form.html
- Page Title: Submit Application
- Context Variables:
  - job: dict job details
- Elements:
  - div#application-form-page
  - input#applicant-name (text input)
  - input#applicant-email (email input)
  - input#resume-upload (file input)
  - textarea#cover-letter
  - button#submit-application-button

### 5. application_tracking.html
- Filename: templates/application_tracking.html
- Page Title: My Applications
- Context Variables:
  - applications: list of dict with keys: application_id, job_title, company_name, status, applied_date
  - status_filter: str
- Elements:
  - div#tracking-page
  - table#applications-table with columns: Job Title, Company, Status, Date Applied
  - select#status-filter (All, Applied, Under Review, Interview, Rejected)
  - Each row includes button#view-application-button-{{ application.application_id }} (links to url_for('view_application', app_id=application.application_id))
  - button#back-to-dashboard (links to url_for('dashboard'))

### 6. companies_directory.html
- Filename: templates/companies_directory.html
- Page Title: Company Directory
- Context Variables:
  - companies: list of dict with keys: company_id, company_name, industry, employee_count
  - search_query: str
- Elements:
  - div#companies-page
  - input#search-company-input
  - div#companies-list with company cards
  - Each company card includes button#view-company-button-{{ company.company_id }} (links to url_for('company_profile', company_id=company.company_id))
  - button#back-to-dashboard (links to url_for('dashboard'))

### 7. company_profile.html
- Filename: templates/company_profile.html
- Page Title: Company Profile
- Context Variables:
  - company: dict with keys: company_id, company_name, industry, location, description
  - jobs: list of dict with keys: job_id, title, status (assumed status like "Open")
- Elements:
  - div#company-profile-page
  - div#company-info showing company information
  - div#company-jobs
  - div#jobs-list listing jobs with button#view-job-button-{{ job.job_id }} (links to url_for('job_details', job_id=job.job_id))
  - button#back-to-companies (links to url_for('companies_directory'))

### 8. resumes.html
- Filename: templates/resumes.html
- Page Title: My Resumes
- Context Variables:
  - resumes: list of dict with keys: resume_id, applicant_name, applicant_email, filename, upload_date, summary
- Elements:
  - div#resume-page
  - div#resumes-list with each resume showing filename and upload_date
  - button#upload-resume-button (opens file input resume-file-input)
  - input#resume-file-input (type file, hidden)
  - Each resume item has button#delete-resume-button-{{ resume.resume_id }}
  - button#back-to-dashboard (links to url_for('dashboard'))

### 9. search_results.html
- Filename: templates/search_results.html
- Page Title: Search Results
- Context Variables:
  - query: str search query
  - job_results: list of dict as in job listings
  - company_results: list of dict as in companies listing
- Elements:
  - div#search-results-page
  - div#search-query-display (shows query)
  - div#results-tabs with tabs for jobs and companies
  - div#job-results listing jobs
  - div#company-results listing companies
  - div#no-results-message (shown if no results found)

---

## Section 3: Data File Schemas

### 1. data/jobs.txt
- Fields (pipe-delimited):
  - job_id (int)
  - title (str)
  - company_id (int)
  - location (str)
  - salary_min (int)
  - salary_max (int)
  - category (str)
  - description (str)
  - posted_date (YYYY-MM-DD)
- Description: Stores job postings with identifiers, associated companies, salary info, category, and date posted.
- Example rows:
```
1|Senior Python Developer|1|Remote|80000|120000|Technology|Experienced Python developer for web applications|2025-01-15
2|Data Analyst|2|New York, NY|60000|85000|Finance|Analyze financial data and create reports|2025-01-16
3|Healthcare Administrator|3|Los Angeles, CA|50000|70000|Healthcare|Manage hospital operations and patient records|2025-01-14
```

### 2. data/companies.txt
- Fields (pipe-delimited):
  - company_id (int)
  - company_name (str)
  - industry (str)
  - location (str)
  - employee_count (int)
  - description (str)
- Description: Stores company profiles with identifying information and details.
- Example rows:
```
1|TechCorp|Technology|San Francisco, CA|500|Leading software solutions provider
2|FinanceHub|Finance|New York, NY|300|Innovative financial services company
3|MediCare|Healthcare|Los Angeles, CA|200|Premier healthcare management organization
```

### 3. data/categories.txt
- Fields (pipe-delimited):
  - category_id (int)
  - category_name (str)
  - description (str)
- Description: Stores job categories with description.
- Example rows:
```
1|Technology|Software, IT, and tech-related positions
2|Finance|Banking, accounting, and finance positions
3|Healthcare|Medical and healthcare industry positions
```

### 4. data/applications.txt
- Fields (pipe-delimited):
  - application_id (int)
  - job_id (int)
  - applicant_name (str)
  - applicant_email (str)
  - status (str) [Possible values: Applied, Under Review, Interview, Rejected]
  - applied_date (YYYY-MM-DD)
  - resume_id (int)
- Description: Stores job applications with status and links to resume.
- Example rows:
```
1|1|John Doe|john@email.com|Under Review|2025-01-17|1
2|2|Jane Smith|jane@email.com|Applied|2025-01-16|2
3|3|Robert Johnson|robert@email.com|Interview|2025-01-15|3
```

### 5. data/resumes.txt
- Fields (pipe-delimited):
  - resume_id (int)
  - applicant_name (str)
  - applicant_email (str)
  - filename (str)
  - upload_date (YYYY-MM-DD)
  - summary (str)
- Description: Stores uploaded resumes with metadata.
- Example rows:
```
1|John Doe|john@email.com|john_resume.pdf|2025-01-17|Senior developer with 8 years experience
2|Jane Smith|jane@email.com|jane_resume.pdf|2025-01-16|Data analyst with financial background
3|Robert Johnson|robert@email.com|robert_resume.pdf|2025-01-15|Healthcare administrator with 5 years experience
```

### 6. data/job_categories.txt
- Fields (pipe-delimited):
  - mapping_id (int)
  - job_id (int)
  - category_id (int)
- Description: Maps jobs to one or more categories.
- Example rows:
```
1|1|1
2|2|2
3|3|3
```

---

This design specification ensures backend developers can implement Flask routes with the exact function names, method handling, templates, and context variables. Frontend developers can create the UI with precise element IDs and contextual data. The data file schemas guarantee consistent data parsing and usage across all layers.

All identifiers and names are consistent and exhaustive as per the requirements document.
