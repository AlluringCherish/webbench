# JobBoard Web Application Detailed Design Specification (Design Candidate B)

---

## 1. Overview

This document specifies the detailed design for the JobBoard web application based on the provided user requirements. It includes the Flask routes, HTML template filenames, element IDs, user navigation flow, and data file organization for local storage as pipe-delimited text files.

---

## 2. Flask Routes and Templates

| Route | HTTP Method(s) | Template Filename | Context Variables Passed |
|-------|----------------|-------------------|--------------------------|
| `/`  | GET | dashboard.html | `featured_jobs` (list of job dicts), others as needed |
| `/jobs` | GET | jobs.html | `jobs` (filtered jobs list), `categories`, `locations`, `selected_category`, `selected_location`, `search_query` |
| `/jobs/<int:job_id>` | GET | job_details.html | `job`, `company` |
| `/apply/<int:job_id>` | GET, POST | application_form.html | GET: `job`; POST: success/failure message |
| `/applications` | GET | applications.html | `applications`, `filter_status` |
| `/applications/<int:app_id>` | GET | application_details.html | `application`, `job`, `resume` |
| `/companies` | GET | companies.html | `companies`, `search_query` |
| `/companies/<int:company_id>` | GET | company_profile.html | `company`, `jobs` |
| `/resumes` | GET, POST | resumes.html | `resumes`, POST: success/failure message |
| `/resumes/delete/<int:resume_id>` | POST | Redirect or JSON response | success/failure message |
| `/search` | GET | search_results.html | `query`, `job_results`, `company_results` |

---

## 3. Page Elements (Element IDs and Types)

### 3.1 Dashboard Page (`dashboard.html`)
- `dashboard-page` (Div)
- `featured-jobs` (Div) - shows featured job cards
- `browse-jobs-button` (Button) - navigates to `/jobs`
- `my-applications-button` (Button) - navigates to `/applications`
- `companies-button` (Button) - navigates to `/companies`

### 3.2 Job Listings Page (`jobs.html`)
- `listings-page` (Div)
- `search-input` (Input text) - search by job title, company, location
- `category-filter` (Dropdown select) - filter by category
- `location-filter` (Dropdown select) - filter by job location
- `jobs-grid` (Div) - contains job cards
- Dynamic Buttons:
  - `view-job-button-{job_id}` (Button) - navigates to `/jobs/<job_id>`

### 3.3 Job Details Page (`job_details.html`)
- `job-details-page` (Div)
- `job-title` (H1) - job title
- `company-name` (Div) - company name
- `job-description` (Div) - long description
- `salary-range` (Div) - salary min-max
- `apply-now-button` (Button) - navigates to `/apply/<job_id>`

### 3.4 Application Form Page (`application_form.html`)
- `application-form-page` (Div)
- `applicant-name` (Input text)
- `applicant-email` (Input email)
- `resume-upload` (File input)
- `cover-letter` (Textarea)
- `submit-application-button` (Button)

### 3.5 Application Tracking Page (`applications.html`)
- `tracking-page` (Div)
- `applications-table` (Table) - columns: Job Title, Company, Status, Date Applied
- `status-filter` (Dropdown select) - All, Applied, Under Review, Interview, Rejected
- Dynamic Buttons:
  - `view-application-button-{app_id}` (Button) - navigates to `/applications/<app_id>`
- `back-to-dashboard` (Button) - navigates to `/`

### 3.6 Companies Directory Page (`companies.html`)
- `companies-page` (Div)
- `companies-list` (Div) - company cards
- `search-company-input` (Input text)
- Dynamic Buttons:
  - `view-company-button-{company_id}` (Button) - navigates to `/companies/<company_id>`
- `back-to-dashboard` (Button) - navigates to `/`

### 3.7 Company Profile Page (`company_profile.html`)
- `company-profile-page` (Div)
- `company-info` (Div) - name, industry, location, description
- `company-jobs` (Div) - listing of open jobs
- `jobs-list` (Div) - job cards with title and status
- Dynamic Buttons:
  - `view-job-button-{job_id}` (Button) - navigates to `/jobs/<job_id>`
- `back-to-companies` (Button) - navigates to `/companies`

### 3.8 Resume Management Page (`resumes.html`)
- `resume-page` (Div)
- `resumes-list` (Div) - list of uploaded resumes
- `upload-resume-button` (Button) - triggers hidden file input
- `resume-file-input` (File input) - hidden for upload
- Dynamic Buttons:
  - `delete-resume-button-{resume_id}` (Button) - deletes resume
- `back-to-dashboard` (Button) - navigates to `/`

### 3.9 Search Results Page (`search_results.html`)
- `search-results-page` (Div)
- `search-query-display` (Div) - shows query string
- `results-tabs` (Div) - tabs for Jobs and Companies
- `job-results` (Div) - job search results
- `company-results` (Div) - company search results
- `no-results-message` (Div) - when no matches found

---

## 4. User Navigation Flow

Starts at Dashboard Page `/`:

- Buttons on Dashboard:
  - `browse-jobs-button` &rarr; `/jobs`
  - `my-applications-button` &rarr; `/applications`
  - `companies-button` &rarr; `/companies`

From Job Listings (`/jobs`):
- Search and filter jobs.
- Click `view-job-button-{job_id}` to go to `/jobs/<job_id>`.

From Job Details (`/jobs/<job_id>`):
- Click `apply-now-button` to go to `/apply/<job_id>`.

From Application Form (`/apply/<job_id>`):
- Submit form posts application.
- Upon success, redirect to `/applications`.

From Application Tracking (`/applications`):
- Use `status-filter` to filter applications.
- Click `view-application-button-{app_id}` to see details.
- `back-to-dashboard` button to `/`.

From Application Details (`/applications/<app_id>`):
- Back link to `/applications` (not specified but recommended).

From Companies Directory (`/companies`):
- Search companies.
- Click `view-company-button-{company_id}` to go to `/companies/<company_id>`.
- `back-to-dashboard` button to `/`.

From Company Profile (`/companies/<company_id>`):
- Click `view-job-button-{job_id}` to navigate to `/jobs/<job_id>`.
- `back-to-companies` button to `/companies`.

From Resume Management (`/resumes`):
- Upload new resume.
- Delete resume with `delete-resume-button-{resume_id}`.
- `back-to-dashboard` button to `/`.

From Search Results (`/search`):
- Displays job and company matches for query.
- Tabs switch between job-results and company-results.
- Click jobs to `/jobs/<job_id>`, companies to `/companies/<company_id>` (IDs included in results links).

---

## 5. Data Files: Formats and Usage

### 5.1 jobs.txt
- Location: `data/jobs.txt`
- Format: `job_id|title|company_id|location|salary_min|salary_max|category|description|posted_date`
- Reads:
  - Load all jobs for listings, filters, featured display.
- Writes:
  - New jobs added administratively (not covered here).

### 5.2 companies.txt
- Location: `data/companies.txt`
- Format: `company_id|company_name|industry|location|employee_count|description`
- Reads:
  - Load companies for directory and profile pages.

### 5.3 categories.txt
- Location: `data/categories.txt`
- Format: `category_id|category_name|description`
- Reads:
  - Load job categories for filtering dropdown.

### 5.4 applications.txt
- Location: `data/applications.txt`
- Format: `application_id|job_id|applicant_name|applicant_email|status|applied_date|resume_id`
- Reads:
  - Load all applications for tracking page.
- Writes:
  - Append on successful application submission.

### 5.5 resumes.txt
- Location: `data/resumes.txt`
- Format: `resume_id|applicant_name|applicant_email|filename|upload_date|summary`
- Reads:
  - Load all resumes for resume management and application views.
- Writes:
  - Append on new resume upload.
  - Remove on resume deletion.

### 5.6 job_categories.txt
- Location: `data/job_categories.txt`
- Format: `mapping_id|job_id|category_id`
- Reads:
  - Load job to category mapping for filtering and category display.

---

## 6. Additional Notes

- All pages have their specified page titles as `<title>` HTML elements.
- All dynamic buttons are named as specified with `{job_id}`, `{app_id}`, `{company_id}`, and `{resume_id}` replaced by their actual numeric IDs.
- Navigation is designed to minimize user clicks and provide a clear path back to dashboard or parent pages.
- File uploads (resumes) must be saved to a dedicated directory (e.g., `uploads/`) with filename referenced in `resumes.txt`.
- Dates use YYYY-MM-DD format.
- No authentication is implemented; all data is accessible.

---

This specification enables separate FE and BE development by clearly defining routes, templates, element IDs, navigation flows, and data file specifications.

---

*End of Design Candidate B Specification*