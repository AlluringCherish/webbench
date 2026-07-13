# JobBoard Web Application - Design Specification

---

## 1. Flask Routes, HTTP Methods, and Templates

| Page Name               | Route Endpoint                  | HTTP Method | Template Filename          | Page Title           |
|-------------------------|--------------------------------|-------------|----------------------------|----------------------|
| Dashboard Page          | /                              | GET         | dashboard.html             | Job Board Dashboard  |
| Job Listings Page       | /jobs                          | GET         | job_listings.html          | Job Listings         |
| Job Details Page        | /jobs/<int:job_id>             | GET         | job_details.html           | Job Details          |
| Application Form Page   | /jobs/<int:job_id>/apply       | GET, POST   | application_form.html      | Submit Application   |
| Application Tracking    | /applications                  | GET         | application_tracking.html  | My Applications      |
| Application Detail View | /applications/<int:app_id>    | GET         | application_detail.html    | Application Details* |
| Companies Directory     | /companies                    | GET         | companies_directory.html   | Company Directory    |
| Company Profile Page    | /companies/<int:company_id>   | GET         | company_profile.html       | Company Profile      |
| Resume Management Page  | /resumes                     | GET, POST   | resume_management.html     | My Resumes           |
| Resume Delete Action    | /resumes/<int:resume_id>/delete| POST        | N/A (Redirect or JSON)     | N/A                  |
| Search Results Page     | /search                      | GET         | search_results.html        | Search Results       |

*Note: Application Detail View page is assumed; not explicitly listed but needed to fully support navigation.


## 2. Templates and Exact Page Titles

| Template Filename           | Exact Page Title             |
|-----------------------------|-----------------------------|
| dashboard.html              | Job Board Dashboard         |
| job_listings.html           | Job Listings                |
| job_details.html            | Job Details                 |
| application_form.html       | Submit Application          |
| application_tracking.html   | My Applications             |
| application_detail.html     | Application Details         |
| companies_directory.html    | Company Directory           |
| company_profile.html        | Company Profile             |
| resume_management.html      | My Resumes                  |
| search_results.html         | Search Results              |


## 3. UI Element IDs

### Static Element IDs
- dashboard-page
- featured-jobs
- browse-jobs-button
- my-applications-button
- companies-button

- listings-page
- search-input
- category-filter
- location-filter
- jobs-grid

- job-details-page
- job-title
- company-name
- job-description
- salary-range
- apply-now-button

- application-form-page
- applicant-name
- applicant-email
- resume-upload
- cover-letter
- submit-application-button

- tracking-page
- applications-table
- status-filter
- back-to-dashboard

- companies-page
- companies-list
- search-company-input

- company-profile-page
- company-info
- company-jobs
- jobs-list
- back-to-companies

- resume-page
- resumes-list
- upload-resume-button
- resume-file-input
- back-to-dashboard

- search-results-page
- search-query-display
- results-tabs
- job-results
- company-results
- no-results-message

### Dynamic Element IDs
- view-job-button-{job_id}
- view-application-button-{app_id}
- view-company-button-{company_id}
- delete-resume-button-{resume_id}


## 4. Navigation Flow

### Starting Point
- User starts at **Dashboard Page** (`/`)

### Navigation from Dashboard
- `browse-jobs-button` -> Job Listings Page (`/jobs`)
- `my-applications-button` -> Application Tracking Page (`/applications`)
- `companies-button` -> Companies Directory Page (`/companies`)

### Navigation from Job Listings Page
- `view-job-button-{job_id}` -> Job Details Page (`/jobs/<job_id>`)

### Navigation from Job Details Page
- `apply-now-button` -> Application Form Page (`/jobs/<job_id>/apply`)

### Navigation from Application Form Page
- On successful submission, redirect to Application Tracking Page (`/applications`)

### Navigation from Application Tracking Page
- `view-application-button-{app_id}` -> Application Detail View Page (`/applications/<app_id>`)
- `back-to-dashboard` -> Dashboard Page (`/`)

### Navigation from Companies Directory Page
- `view-company-button-{company_id}` -> Company Profile Page (`/companies/<company_id>`)
- `back-to-dashboard` -> Dashboard Page (`/`)

### Navigation from Company Profile Page
- `view-job-button-{job_id}` -> Job Details Page (`/jobs/<job_id>`)
- `back-to-companies` -> Companies Directory Page (`/companies`)

### Navigation from Resume Management Page
- `upload-resume-button` -> Triggers `resume-file-input` upload dialog
- `delete-resume-button-{resume_id}` -> Sends POST request to delete resume
- `back-to-dashboard` -> Dashboard Page (`/`)

### Navigation from Search Results Page
- Navigation via UI tabs for job results and company results
- Search query persists in `search-query-display`


## 5. Data File Schemas

All data files stored under `data/` directory.

---

### 1. Jobs Data
- File path: `data/jobs.txt`
- Fields (pipe-delimited, exact order):
  ```
  job_id|title|company_id|location|salary_min|salary_max|category|description|posted_date
  ```
- Description: Stores job postings with related company and categorization.
- Example rows:
  ```
  1|Senior Python Developer|1|Remote|80000|120000|Technology|Experienced Python developer for web applications|2025-01-15
  2|Data Analyst|2|New York, NY|60000|85000|Finance|Analyze financial data and create reports|2025-01-16
  3|Healthcare Administrator|3|Los Angeles, CA|50000|70000|Healthcare|Manage hospital operations and patient records|2025-01-14
  ```

### 2. Companies Data
- File path: `data/companies.txt`
- Fields (pipe-delimited, exact order):
  ```
  company_id|company_name|industry|location|employee_count|description
  ```
- Description: Stores company profiles and metadata.
- Example rows:
  ```
  1|TechCorp|Technology|San Francisco, CA|500|Leading software solutions provider
  2|FinanceHub|Finance|New York, NY|300|Innovative financial services company
  3|MediCare|Healthcare|Los Angeles, CA|200|Premier healthcare management organization
  ```

### 3. Categories Data
- File path: `data/categories.txt`
- Fields (pipe-delimited, exact order):
  ```
  category_id|category_name|description
  ```
- Description: Stores job categories metadata.
- Example rows:
  ```
  1|Technology|Software, IT, and tech-related positions
  2|Finance|Banking, accounting, and finance positions
  3|Healthcare|Medical and healthcare industry positions
  ```

### 4. Applications Data
- File path: `data/applications.txt`
- Fields (pipe-delimited, exact order):
  ```
  application_id|job_id|applicant_name|applicant_email|status|applied_date|resume_id
  ```
- Description: Stores job application records linking applicant, job, and resume.
- Example rows:
  ```
  1|1|John Doe|john@email.com|Under Review|2025-01-17|1
  2|2|Jane Smith|jane@email.com|Applied|2025-01-16|2
  3|3|Robert Johnson|robert@email.com|Interview|2025-01-15|3
  ```

### 5. Resumes Data
- File path: `data/resumes.txt`
- Fields (pipe-delimited, exact order):
  ```
  resume_id|applicant_name|applicant_email|filename|upload_date|summary
  ```
- Description: Stores uploaded resumes along with applicant contact info and summary.
- Example rows:
  ```
  1|John Doe|john@email.com|john_resume.pdf|2025-01-17|Senior developer with 8 years experience
  2|Jane Smith|jane@email.com|jane_resume.pdf|2025-01-16|Data analyst with financial background
  3|Robert Johnson|robert@email.com|robert_resume.pdf|2025-01-15|Healthcare administrator with 5 years experience
  ```

### 6. Job Categories Mapping Data
- File path: `data/job_categories.txt`
- Fields (pipe-delimited, exact order):
  ```
  mapping_id|job_id|category_id
  ```
- Description: Maps job postings to categories for filtering.
- Example rows:
  ```
  1|1|1
  2|2|2
  3|3|3
  ```

---

This design specification ensures:
- All pages and UI elements per requirements are listed with exact IDs.
- RESTful Flask routes with appropriate GET and POST methods for pages and forms.
- Explicit template filenames to maintain clear separation of concerns.
- Data files layout fully documented for local file storage and easy parsing.
- Navigation flow that allows starting at dashboard with no authentication and direct transitions per button IDs.

This completes the design specification for the JobBoard web application.
