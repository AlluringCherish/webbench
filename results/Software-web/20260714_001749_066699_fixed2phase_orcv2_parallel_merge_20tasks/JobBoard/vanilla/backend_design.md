# JobBoard Backend Design Document

---

## 1. Overview

This document specifies the backend architecture of the JobBoard web application using Flask in Python. The backend handles routes, data operations using local text files, and business logic for job browsing, applications, company directories, resume management, and search functionalities.

No user authentication is required; all features are open access.

Data files are stored in the `data/` directory with specified schemas.

---

## 2. Flask Routes and Handlers

### 2.1 Dashboard
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

### 2.2 Job Listings
- **Route:** `/jobs`
- **Methods:** GET
- **Handler Function:** `list_jobs()`
- **Request Params:**
  - `search` (optional string) - Keywords to search in job title, company name, location
  - `category` (optional string) - Category name filter
  - `location` (optional string) - Location filter (Remote, On-site, Hybrid)
- **Behavior:**
  - Reads `jobs.txt`, `companies.txt`, and `categories.txt` for filters.
  - Applies search and filters.
  - Renders job listings with filtered jobs.
  - Each job card includes button with ID: `view-job-button-{job_id}` redirects to `/jobs/<job_id>`

---

### 2.3 Job Details
- **Route:** `/jobs/<int:job_id>`
- **Methods:** GET
- **Handler Function:** `job_details(job_id)`
- **Behavior:**
  - Reads `jobs.txt`, `companies.txt` to display full job details and company info.
  - Renders job details template.
  - Button `apply-now-button` redirects to application form `/apply/<job_id>`

---

### 2.4 Application Form
- **Route:** `/apply/<int:job_id>`
- **Methods:**
  - GET: `application_form(job_id)` - renders form
  - POST: `submit_application(job_id)` - processes submission
- **Form Fields:**
  - `applicant_name` (string)
  - `applicant_email` (string)
  - `resume_upload` (file upload)
  - `cover_letter` (string)
- **Behavior:**
  - GET: Display form for specific job.
  - POST: Validates inputs.
    - Saves uploaded resume file.
    - Creates a new resume entry in `resumes.txt` with unique `resume_id`.
    - Creates new application entry in `applications.txt` with unique `application_id`, current date, and status "Applied".
  - Redirects to `/applications` after successful submission.

---

### 2.5 Application Tracking
- **Route:** `/applications`
- **Methods:** GET
- **Handler Function:** `track_applications()`
- **Request Params:**
  - `status` (optional string) - Filter by application status
- **Behavior:**
  - Reads `applications.txt`, `jobs.txt`, and `companies.txt`.
  - Filters applications by status if provided.
  - Renders applications table with job title, company, status, apply date.
  - Each application row has button `view-application-button-{application_id}` to show application details (could be modal or another route).
  - Button `back-to-dashboard` redirects to `/`

---

### 2.6 Companies Directory
- **Route:** `/companies`
- **Methods:** GET
- **Handler Function:** `list_companies()`
- **Request Params:**
  - `search` (optional string) - Keyword search over company name or industry
- **Behavior:**
  - Reads `companies.txt`.
  - Applies search filter.
  - Renders a list of companies.
  - Each company card has button `view-company-button-{company_id}` redirects to `/companies/<company_id>`
  - Button `back-to-dashboard` redirects to `/`

---

### 2.7 Company Profile
- **Route:** `/companies/<int:company_id>`
- **Methods:** GET
- **Handler Function:** `company_profile(company_id)`
- **Behavior:**
  - Reads `companies.txt`, `jobs.txt` for jobs by the company.
  - Renders company profile page including info and open jobs list.
  - Each job has button `view-job-button-{job_id}` redirects to `/jobs/<job_id>`
  - Button `back-to-companies` redirects to `/companies`

---

### 2.8 Resume Management
- **Route:** `/resumes`
- **Methods:**
  - GET: `list_resumes()` - lists uploaded resumes
  - POST: `upload_resume()` - uploads a new resume
  - POST (or DELETE): `delete_resume(resume_id)` - deletes a resume
- **Form Fields for Upload:**
  - `resume_file` (file upload)
  - `applicant_name` (string)
  - `applicant_email` (string)
  - `summary` (string)
- **Behavior:**
  - GET: Reads `resumes.txt` and displays list.
  - POST Upload:
    - Saves uploaded resume file.
    - Appends new entry to `resumes.txt`.
  - DELETE or POST Delete:
    - Removes resume record and deletes file.
  - Button `back-to-dashboard` redirects to `/`

---

### 2.9 Search Results
- **Route:** `/search`
- **Methods:** GET
- **Handler Function:** `search_results()`
- **Request Params:**
  - `query` (string, required)
- **Behavior:**
  - Searches jobs and companies titles/names/descriptions by query.
  - Renders results page with tabs for jobs and companies results.
  - Shows `no-results-message` div if no matches.

---

## 3. Data Storage Schemas

Files stored in the `data/` folder use pipe-delimited `|` text format.

---

### 3.1 Jobs (`jobs.txt`)
```
job_id|title|company_id|location|salary_min|salary_max|category|description|posted_date
```
- Types: job_id (int), salary_min/max (int), posted_date (yyyy-mm-dd string)
- Example:
```
1|Senior Python Developer|1|Remote|80000|120000|Technology|Experienced Python developer for web applications|2025-01-15
```

### 3.2 Companies (`companies.txt`)
```
company_id|company_name|industry|location|employee_count|description
```
- Types: company_id (int), employee_count (int)
- Example:
```
1|TechCorp|Technology|San Francisco, CA|500|Leading software solutions provider
```

### 3.3 Categories (`categories.txt`)
```
category_id|category_name|description
```
- Types: category_id (int)
- Example:
```
1|Technology|Software, IT, and tech-related positions
```

### 3.4 Applications (`applications.txt`)
```
application_id|job_id|applicant_name|applicant_email|status|applied_date|resume_id
```
- Types: application_id, job_id, resume_id (int), applied_date (yyyy-mm-dd)
- Status values: "Applied", "Under Review", "Interview", "Rejected"
- Example:
```
1|1|John Doe|john@email.com|Under Review|2025-01-17|1
```

### 3.5 Resumes (`resumes.txt`)
```
resume_id|applicant_name|applicant_email|filename|upload_date|summary
```
- Types: resume_id (int), upload_date (yyyy-mm-dd)
- Example:
```
1|John Doe|john@email.com|john_resume.pdf|2025-01-17|Senior developer with 8 years experience
```

### 3.6 Job Categories Mapping (`job_categories.txt`)
```
mapping_id|job_id|category_id
```
- Types: mapping_id, job_id, category_id (int)
- Example:
```
1|1|1
```

---

## 4. Business Logic and Workflows

### 4.1 Job Filtering and Searching
- Load full jobs list and associated company and category data.
- Filtering by category and location via dropdown filters.
- Searching by keywords matched in job title, company name, or location.
- Filtering and search implemented in-memory on file-loaded datasets.

### 4.2 Viewing Job Details
- Use job_id to fetch job and company details.
- If job_id not found, return 404.

### 4.3 Job Application Submission
- Validate required fields in form.
- Save uploaded resume file to dedicated resumes folder.
- Append new resume record to `resumes.txt` with incremented `resume_id`.
- Append new application record to `applications.txt` with incremented `application_id`, date set to today, and status "Applied".
- Link application to resume by `resume_id`.
- No user authentication—applications distinguished by email/name combination.

### 4.4 Application Status Tracking
- Load applications list and join with job and company details.
- Filter by application status.
- Handle missing or malformed fields gracefully.

### 4.5 Companies Directory and Company Profile
- Search companies by name or industry.
- Company profile shows company info and all open jobs posted by the company.

### 4.6 Resume Management
- Allow multiple resumes upload with applicant_name and applicant_email stored.
- Resume deletion removes database record and associated file from disk.
- Resume files validated on upload (e.g., file type and size).

### 4.7 Searching Jobs and Companies
- Perform case-insensitive substring match on relevant fields.
- Return results grouped by jobs and companies.

### 4.8 Data Consistency Without Authentication
- Use data file atomic read and write with locking to avoid race conditions.
- Generate unique IDs by scanning current files and incrementing max IDs.
- Provide error handling for file access issues.

### 4.9 Error Handling and Validation
- Validate all user inputs from forms.
- Return appropriate HTTP status codes for not found resources or invalid requests.
- Handle file upload errors gracefully.
- Display informative user-friendly error messages when needed.

---

## 5. Additional Notes

- All dates stored as ISO 8601 strings (yyyy-mm-dd).
- File delimiters are strictly pipe (`|`) character.
- Uploaded resumes stored in a dedicated local directory for file management.
- Frontend navigation buttons trigger appropriate backend routes specified.
- This design is independent of any frontend details and focuses on backend data handling and route definitions.

---

**End of Design Document**