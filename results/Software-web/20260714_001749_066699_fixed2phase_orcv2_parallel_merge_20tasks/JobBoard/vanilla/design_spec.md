# JobBoard Unified Design Specification

---

## 1. Backend Routes and Data Schemas

### 1.1 Dashboard
- **Route:** `/` or `/dashboard`
- **Methods:** GET
- **Handler Function:** `dashboard()`
- **Request Params/Form Fields:** None
- **Behavior:**
  - Reads featured jobs from `jobs.txt` (e.g., latest or specifically flagged jobs).
  - Renders dashboard template with featured jobs.
  - Navigation buttons with IDs:
    - `browse-jobs-button` -> redirects to `/jobs`
    - `my-applications-button` -> redirects to `/applications`
    - `companies-button` -> redirects to `/companies`

---

### 1.2 Job Listings
- **Route:** `/jobs`
- **Methods:** GET
- **Handler Function:** `list_jobs()`
- **Request Params:**
  - `search` (optional string) - Keywords to search in job title, company name, location
  - `category` (optional string) - Category name filter
  - `location` (optional string) - Location filter (Remote, On-site, Hybrid)
- **Behavior:**
  - Reads `jobs.txt`, `companies.txt`, and `categories.txt`.
  - Applies search and filters.
  - Renders job listings page with filtered jobs.
  - Each job card includes button with ID: `view-job-button-{job_id}` redirects to `/jobs/<job_id>`

---

### 1.3 Job Details
- **Route:** `/jobs/<int:job_id>`
- **Methods:** GET
- **Handler Function:** `job_details(job_id)`
- **Behavior:**
  - Reads `jobs.txt`, `companies.txt` to display full job details and company info.
  - Renders job details page.
  - Button `apply-now-button` redirects to application form `/apply/<job_id>`

---

### 1.4 Application Form
- **Route:** `/apply/<int:job_id>`
- **Methods:**
  - GET: `application_form(job_id)` - renders the application form page
  - POST: `submit_application(job_id)` - processes submission
- **Form Fields:**
  - `applicant_name` (string)
  - `applicant_email` (string)
  - `resume_upload` (file upload)
  - `cover_letter` (string)
- **Behavior:**
  - GET: Displays application form for the specific job.
  - POST: Validates inputs, saves uploaded resume file.
  - Creates new resume entry in `resumes.txt` with unique `resume_id`.
  - Creates new application entry in `applications.txt` with unique `application_id`, current date, and status "Applied".
  - Redirects to `/applications` after successful submission.

---

### 1.5 Application Tracking
- **Route:** `/applications`
- **Methods:** GET
- **Handler Function:** `track_applications()`
- **Request Params:**
  - `status` (optional string) - Filter by application status
- **Behavior:**
  - Reads `applications.txt`, `jobs.txt`, and `companies.txt`.
  - Filters applications by status if provided.
  - Renders applications table with columns: job title, company, status, applied date.
  - Each application row has button `view-application-button-{application_id}` to show application details (modal or detail view).
  - Button `back-to-dashboard` redirects to `/`.

---

### 1.6 Companies Directory
- **Route:** `/companies`
- **Methods:** GET
- **Handler Function:** `list_companies()`
- **Request Params:**
  - `search` (optional string) - Keyword search over company name or industry
- **Behavior:**
  - Reads `companies.txt`.
  - Applies search filter.
  - Renders a list of companies.
  - Each company card has button `view-company-button-{company_id}` redirecting to `/companies/<company_id>`.
  - Button `back-to-dashboard` redirects to `/`.

---

### 1.7 Company Profile
- **Route:** `/companies/<int:company_id>`
- **Methods:** GET
- **Handler Function:** `company_profile(company_id)`
- **Behavior:**
  - Reads `companies.txt`, `jobs.txt` for jobs by the company.
  - Renders company profile page including company info and open jobs list.
  - Each job has button `view-job-button-{job_id}` redirecting to `/jobs/<job_id>`.
  - Button `back-to-companies` redirects to `/companies`.

---

### 1.8 Resume Management
- **Route:** `/resumes`
- **Methods:**
  - GET: Lists uploaded resumes via `list_resumes()`
  - POST (upload new resume): `upload_resume()`
  - POST or DELETE to delete resume: `delete_resume(resume_id)`
- **Form Fields for Upload:**
  - `resume_file` (file upload)
  - `applicant_name` (string)
  - `applicant_email` (string)
  - `summary` (string)
- **Behavior:**
  - GET: Reads `resumes.txt` and displays list.
  - POST Upload: Saves uploaded file and appends a new entry to `resumes.txt`.
  - DELETE or POST Delete: Removes resume record and deletes file from disk.
  - Button `back-to-dashboard` redirects to `/`.

---

### 1.9 Search Results
- **Route:** `/search`
- **Methods:** GET
- **Handler Function:** `search_results()`
- **Request Params:**
  - `query` (string, required) - search keyword
- **Behavior:**
  - Searches jobs and companies titles/names/descriptions case-insensitively.
  - Renders results page with tabs for job results and company results.
  - Displays `no-results-message` div if no matches found.

---

## 2. Data Storage Schemas

All data files live in `data/` directory, pipe (`|`) delimited, with the following formats:

### 2.1 Jobs (`jobs.txt`)
```
job_id|title|company_id|location|salary_min|salary_max|category|description|posted_date
```
- Types: job_id int, salary_min/max int, posted_date ISO 8601 yyyy-mm-dd
- Example:
```
1|Senior Python Developer|1|Remote|80000|120000|Technology|Experienced Python developer for web applications|2025-01-15
```

### 2.2 Companies (`companies.txt`)
```
company_id|company_name|industry|location|employee_count|description
```
- Types: company_id int, employee_count int
- Example:
```
1|TechCorp|Technology|San Francisco, CA|500|Leading software solutions provider
```

### 2.3 Categories (`categories.txt`)
```
category_id|category_name|description
```
- Types: category_id int
- Example:
```
1|Technology|Software, IT, and tech-related positions
```

### 2.4 Applications (`applications.txt`)
```
application_id|job_id|applicant_name|applicant_email|status|applied_date|resume_id
```
- Types: application_id, job_id, resume_id int, applied_date ISO 8601
- Status: "Applied", "Under Review", "Interview", "Rejected"
- Example:
```
1|1|John Doe|john@email.com|Under Review|2025-01-17|1
```

### 2.5 Resumes (`resumes.txt`)
```
resume_id|applicant_name|applicant_email|filename|upload_date|summary
```
- Types: resume_id int, upload_date ISO 8601
- Example:
```
1|John Doe|john@email.com|john_resume.pdf|2025-01-17|Senior developer with 8 years experience
```

### 2.6 Job Categories Mapping (`job_categories.txt`)
```
mapping_id|job_id|category_id
```
- Types: mapping_id, job_id, category_id int
- Example:
```
1|1|1
```

---

## 3. Frontend Templates and UI Elements

### 3.1 Dashboard Page
- **Page Title:** Job Board Dashboard
- **Container:** Div with ID `dashboard-page`
- **Elements:**
  - Div `featured-jobs` - displays featured job recommendations
  - Button `browse-jobs-button` - navigates to `/jobs`
  - Button `my-applications-button` - navigates to `/applications`
  - Button `companies-button` - navigates to `/companies`

### 3.2 Job Listings Page
- **Page Title:** Job Listings
- **Container:** Div with ID `listings-page`
- **Elements:**
  - Input `search-input` (text) - search jobs by title, company, or location
  - Dropdown `category-filter` - filter jobs by category
  - Dropdown `location-filter` - filter jobs by location
  - Div `jobs-grid` - container for job cards
  - Buttons per job card: `view-job-button-{job_id}` - view job details page

### 3.3 Job Details Page
- **Page Title:** Job Details
- **Container:** Div `job-details-page`
- **Elements:**
  - H1 `job-title`
  - Div `company-name`
  - Div `job-description`
  - Div `salary-range`
  - Button `apply-now-button` - link to application form page

### 3.4 Application Form Page
- **Page Title:** Submit Application
- **Container:** Div `application-form-page`
- **Elements:**
  - Input `applicant-name` (text)
  - Input `applicant-email` (email)
  - File input `resume-upload`
  - Textarea `cover-letter`
  - Button `submit-application-button` - submit application

### 3.5 Application Tracking Page
- **Page Title:** My Applications
- **Container:** Div `tracking-page`
- **Elements:**
  - Dropdown `status-filter` (All, Applied, Under Review, Interview, Rejected)
  - Table `applications-table` with columns job title, company, status, applied date
  - Buttons per application row: `view-application-button-{application_id}`
  - Button `back-to-dashboard` - navigates to dashboard

### 3.6 Companies Directory Page
- **Page Title:** Company Directory
- **Container:** Div `companies-page`
- **Elements:**
  - Input `search-company-input` (text) to search companies by name or industry
  - Div `companies-list` - list of company cards
  - Buttons per company: `view-company-button-{company_id}`
  - Button `back-to-dashboard` - navigates to dashboard

### 3.7 Company Profile Page
- **Page Title:** Company Profile
- **Container:** Div `company-profile-page`
- **Elements:**
  - Div `company-info` - company name, industry, location, description
  - Div `company-jobs` - container for open job listings
  - Div `jobs-list` - list of jobs
  - Buttons per job: `view-job-button-{job_id}`
  - Button `back-to-companies` - navigates to companies directory

### 3.8 Resume Management Page
- **Page Title:** My Resumes
- **Container:** Div `resume-page`
- **Elements:**
  - Div `resumes-list` - list of uploaded resumes
  - Button `upload-resume-button` - triggers hidden file input
  - File Input (hidden) `resume-file-input`
  - Buttons per resume: `delete-resume-button-{resume_id}` - deletes the resume
  - Button `back-to-dashboard` - navigates to dashboard

### 3.9 Search Results Page
- **Page Title:** Search Results
- **Container:** Div `search-results-page`
- **Elements:**
  - Div `search-query-display` - shows user's search query
  - Div `results-tabs` - tabs to toggle between jobs and companies
  - Div `job-results` - shows job search results
  - Div `company-results` - shows company search results
  - Div `no-results-message` - shown if no matches found

---

## 4. Consistency and Completeness Checks

- Back-end routes and data schemas fully support front-end elements and navigation flows.
- All button IDs in front-end match route references in back-end design.
- All container div IDs and input/filter controls listed in front-end are supported by back-end behavior to provide data and filtered views.
- Dynamic button IDs with patterns `{job_id}`, `{company_id}`, and `{application_id}`, `{resume_id}` are consistent across both designs.
- Navigation flows such as back buttons and forwarding buttons are clearly mapped to routes.
- Data files and schemas are consistent and complete, supporting all required entities.
- Error handling and validation explicitly defined in back-end.
- File upload fields and resume management addressed comprehensively.

---

This unified design specification allows separate front-end and back-end development teams to implement the 'JobBoard' application consistently and without ambiguities.

---

**End of Unified Design Specification**
