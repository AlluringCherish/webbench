# JobBoard Web Application Unified Design Specification

---

## 1. Flask Routes and Templates

| Route Path                     | HTTP Method(s) | Template Filename          | Context Variables Passed to Template                                                           |
|-------------------------------|----------------|----------------------------|------------------------------------------------------------------------------------------------|
| `/dashboard`                   | GET            | dashboard.html             | `featured_jobs` (list of featured job dicts), `latest_jobs` (list of latest job dicts)          |
| `/jobs`                       | GET            | jobs.html                  | `jobs` (filtered jobs list), `categories`, `locations`, `selected_category`, `selected_location`, `search_query` |
| `/jobs/<int:job_id>`           | GET            | job_details.html           | `job` (job dict), `company` (company dict)                                                      |
| `/apply/<int:job_id>`          | GET, POST      | application_form.html      | GET: `job` dict; POST: success/failure message                                                 |
| `/applications`               | GET            | applications.html          | `applications` (list of application dicts), `filter_status` (string)                           |
| `/applications/<int:app_id>`   | GET            | application_details.html   | `application` (dict), `job` (dict), `resume` (dict) (optional depending on implementation)     |
| `/companies`                  | GET            | companies.html             | `companies` (list of company dicts), `search_query` (string)                                   |
| `/companies/<int:company_id>`  | GET            | company_profile.html       | `company` (company dict), `jobs` (list of job dicts belonging to company)                      |
| `/resumes`                   | GET, POST      | resumes.html               | GET: `resumes` (list of resume dicts); POST: success/failure message                           |
| `/resumes/delete/<int:resume_id>` | POST       | (no template - redirect or JSON response) | success/failure message                                                      |
| `/search`                    | GET            | search_results.html        | `query` (string), `job_results` (list of job dicts), `company_results` (list of company dicts) |

---

## 2. Page Elements and Layout

### 2.1 Dashboard Page (`dashboard.html`)
- Page Title: Job Board Dashboard
- Element IDs:
  - `dashboard-page` (Div): Main container
  - `featured-jobs` (Div): Display featured job recommendations
  - `browse-jobs-button` (Button): Navigate to `/jobs`
  - `my-applications-button` (Button): Navigate to `/applications`
  - `companies-button` (Button): Navigate to `/companies`

### 2.2 Job Listings Page (`jobs.html`)
- Page Title: Job Listings
- Element IDs:
  - `listings-page` (Div): Container for job listings
  - `search-input` (Input text): Search by job title, company, or location
  - `category-filter` (Dropdown select): Filter jobs by category (e.g., Technology, Finance, Healthcare)
  - `location-filter` (Dropdown select): Filter jobs by location (Remote, On-site, Hybrid)
  - `jobs-grid` (Div): Grid showing job cards
  - `view-job-button-{job_id}` (Button): Button to view job details for each job card

### 2.3 Job Details Page (`job_details.html`)
- Page Title: Job Details
- Element IDs:
  - `job-details-page` (Div): Container for job details
  - `job-title` (H1): Display job title
  - `company-name` (Div): Display company name
  - `job-description` (Div): Complete job description and requirements
  - `salary-range` (Div): Salary range display
  - `apply-now-button` (Button): Button to apply for the job

### 2.4 Application Form Page (`application_form.html`)
- Page Title: Submit Application
- Element IDs:
  - `application-form-page` (Div): Container for application form
  - `applicant-name` (Input text): Applicant's name
  - `applicant-email` (Input email): Applicant's email
  - `resume-upload` (File input): Upload resume file
  - `cover-letter` (Textarea): Cover letter text field
  - `submit-application-button` (Button): Submit application

### 2.5 Application Tracking Page (`applications.html`)
- Page Title: My Applications
- Element IDs:
  - `tracking-page` (Div): Container for application tracking
  - `applications-table` (Table): Shows applications with columns: Job Title, Company, Status, Date Applied
  - `status-filter` (Dropdown select): Filter applications by status (All, Applied, Under Review, Interview, Rejected)
  - `view-application-button-{app_id}` (Button): View details of each application
  - `back-to-dashboard` (Button): Navigate back to `/dashboard`

### 2.6 Application Details Page (`application_details.html`)
- Page Title: Application Details (implied, not explicitly in candidate A but in candidate B)
- Element IDs (recommended for completeness):
  - `application-details-page` (Div): Container for application detail view
  - Elements to display application info, job info, and optionally resume info
  - Back button or link to return to `/applications`

### 2.7 Companies Directory Page (`companies.html`)
- Page Title: Company Directory
- Element IDs:
  - `companies-page` (Div): Container for companies directory
  - `companies-list` (Div): List of company cards with name, industry, employee count
  - `search-company-input` (Input text): Search companies by name or industry
  - `view-company-button-{company_id}` (Button): View company profile
  - `back-to-dashboard` (Button): Navigate back to `/dashboard`

### 2.8 Company Profile Page (`company_profile.html`)
- Page Title: Company Profile
- Element IDs:
  - `company-profile-page` (Div): Container for company profile
  - `company-info` (Div): Company name, industry, location, description
  - `company-jobs` (Div): Show company's open jobs
  - `jobs-list` (Div): List of job cards with titles and status indicators
  - `view-job-button-{job_id}` (Button): View job details
  - `back-to-companies` (Button): Navigate back to `/companies`

### 2.9 Resume Management Page (`resumes.html`)
- Page Title: My Resumes
- Element IDs:
  - `resume-page` (Div): Container for resume management
  - `resumes-list` (Div): List of uploaded resumes with upload dates or summary
  - `upload-resume-button` (Button): Button to trigger hidden file input
  - `resume-file-input` (File input): Hidden file input for resume upload
  - `delete-resume-button-{resume_id}` (Button): Delete resume action
  - `back-to-dashboard` (Button): Navigate back to `/dashboard`

### 2.10 Search Results Page (`search_results.html`)
- Page Title: Search Results
- Element IDs:
  - `search-results-page` (Div): Container for search results
  - `search-query-display` (Div): Displays the entered search query
  - `results-tabs` (Div): Tabs to switch between job results and company results
  - `job-results` (Div): Display the job search results
  - `company-results` (Div): Display the company search results
  - `no-results-message` (Div): Displayed if no results found

---

## 3. Navigation Flow

- The application starts at the **Dashboard page** (`/dashboard` or `/` - both routes resolved to dashboard.html for clarity, use `/dashboard` as canonical start).

- From Dashboard:
  - Click `browse-jobs-button` → navigates to Job Listings page (`/jobs`)
  - Click `my-applications-button` → navigates to Application Tracking page (`/applications`)
  - Click `companies-button` → navigates to Companies Directory page (`/companies`)

- From Job Listings (`/jobs`):
  - Use `search-input`, `category-filter`, and `location-filter` to filter jobs.
  - Click `view-job-button-{job_id}` → navigates to Job Details page (`/jobs/<job_id>`)

- From Job Details (`/jobs/<job_id>`):
  - Click `apply-now-button` → takes user to Application Form page (`/apply/<job_id>`)

- From Application Form (`/apply/<job_id>`):
  - Submit form via `submit-application-button`. POST submission with application data.
  - Upon successful application submission, redirect to Application Tracking page (`/applications`).

- From Application Tracking (`/applications`):
  - Use `status-filter` to filter applications.
  - Click `view-application-button-{app_id}` → go to Application Details page (`/applications/<app_id>`).
  - Click `back-to-dashboard` → return to Dashboard.

- From Application Details (`/applications/<app_id>`):
  - Recommended a back link/button to return to `/applications`.

- From Companies Directory (`/companies`):
  - Use `search-company-input` to search companies.
  - Click `view-company-button-{company_id}` → Company Profile page (`/companies/<company_id>`)
  - Click `back-to-dashboard` → return to Dashboard.

- From Company Profile (`/companies/<company_id>`):
  - Click `view-job-button-{job_id}` → Job Details page (`/jobs/<job_id>`)
  - Click `back-to-companies` → Companies Directory page (`/companies`)

- From Resume Management (`/resumes`):
  - Click `upload-resume-button` triggers hidden file input (`resume-file-input`) for upload.
  - Click `delete-resume-button-{resume_id}` to delete a resume.
  - Click `back-to-dashboard` → Dashboard page (`/dashboard`)

- From Search Results (`/search`):
  - Displays job and company matches for the search query.
  - `results-tabs` toggles view between `job-results` and `company-results`.
  - Click job result → `/jobs/<job_id>`, company result → `/companies/<company_id>`.

---

## 4. Data File Specifications

- Data files are stored in `data/` directory.

### 4.1 jobs.txt
- Format:
  `job_id|title|company_id|location|salary_min|salary_max|category|description|posted_date`
- Used for loading job listings, details, category filtering via job_categories.txt.
- Writes not specified in scope (administrative use possible).

### 4.2 companies.txt
- Format:
  `company_id|company_name|industry|location|employee_count|description`
- Used for company directory and profiles.

### 4.3 categories.txt
- Format:
  `category_id|category_name|description`
- Used to populate category filters and job classifications.

### 4.4 applications.txt
- Format:
  `application_id|job_id|applicant_name|applicant_email|status|applied_date|resume_id`
- Read to display user applications and statuses.
- Write on new application submission.

### 4.5 resumes.txt
- Format:
  `resume_id|applicant_name|applicant_email|filename|upload_date|summary`
- Holds uploaded resumes metadata.
- Write on upload, remove on delete.
- Resume files themselves to be stored in `uploads/` folder.

### 4.6 job_categories.txt
- Format:
  `mapping_id|job_id|category_id`
- Used to map jobs to categories for filtering.

---

## 5. Additional Notes

- Page titles correspond to the specified page titles in each section.
- All dynamic buttons have IDs suffixed with relevant IDs (e.g., `{job_id}`, `{app_id}`, `{company_id}`, `{resume_id}`).
- Dates are to use ISO `YYYY-MM-DD` format.
- Uploads require a dedicated folder `uploads/` referenced by resumes.txt.
- No authentication required; all data and pages accessible to users.
- Use canonical route patterns combining Candidate A and B with preferred names from Candidate B and user task.

---

This unified specification provides a complete, consistent blueprint for frontend and backend teams to implement the JobBoard application without ambiguity, covering all routes, page elements, navigation flows, and data file interactions as required.

End of Unified Design Specification.
