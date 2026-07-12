# JobBoard Web Application Design Specification

---

# Section 1: Flask Routes Specification

| Route Path               | Function Name          | HTTP Method(s) | Template Rendered    | Context Variables Passed to Template                         | POST Input Expectations                           |
|--------------------------|------------------------|----------------|----------------------|--------------------------------------------------------------|--------------------------------------------------|
| `/`                      | root_redirect           | GET            | Redirects to `/dashboard` (no template)                      | None                                                         | N/A                                              |
| `/dashboard`             | dashboard_page         | GET            | `dashboard.html`     | `featured_jobs` (list of dicts with job info), `latest_jobs` (list of dicts job info) | N/A                                              |
| `/jobs`                  | job_listings           | GET            | `job_listings.html`  | `jobs` (list of dicts), `categories` (list of dicts), `locations` (list of str)      | N/A                                              |
| `/jobs`                  | job_listings_search    | POST           | `job_listings.html`  | `jobs` (filtered list), `categories` (list), `locations` (list) | `search_input` (str), `category_filter` (str), `location_filter` (str) |
| `/job/<int:job_id>`      | job_details            | GET            | `job_details.html`   | `job` (dict), `company` (dict)                              | N/A                                              |
| `/job/<int:job_id>/apply`| application_form       | GET            | `application_form.html` | `job` (dict)                                                | N/A                                              |
| `/job/<int:job_id>/apply`| submit_application     | POST           | Redirect or flash  | N/A                                                        | `applicant_name` (str), `applicant_email` (str), `resume_file` (file), `cover_letter` (str) |
| `/applications`          | application_tracking   | GET            | `application_tracking.html` | `applications` (list of dicts), `status_filter` (str)    | N/A                                              |
| `/application/<int:app_id>`| view_application      | GET            | (Assumed detailed application view template: `application_details.html`) | `application` (dict), `job` (dict)                | N/A                                              |
| `/companies`             | companies_directory    | GET            | `companies.html`     | `companies` (list of dicts)                                 | N/A                                              |
| `/company/<int:company_id>`| company_profile       | GET            | `company_profile.html`| `company` (dict), `company_jobs` (list of dicts)           | N/A                                              |
| `/resumes`               | resumes_management     | GET            | `resumes.html`       | `resumes` (list of dicts)                                  | N/A                                              |
| `/resumes/upload`        | upload_resume          | POST           | Redirect or render  | N/A                                                        | `resume_file` (file)                              |
| `/resume/<int:resume_id>/delete`| delete_resume    | POST           | Redirect or render  | N/A                                                        | None                                             |
| `/search`                | search_results         | GET            | `search_results.html`| `query` (str), `job_results` (list of dicts), `company_results` (list of dicts)      | N/A                                              |

---

# Section 2: HTML Template Specifications

## 1. Dashboard Page
- Filename: templates/dashboard.html
- Page Title: Job Board Dashboard
- Elements:
  - `dashboard-page` (Div) - Container for the dashboard page
  - `featured-jobs` (Div) - Display of featured job recommendations
  - `browse-jobs-button` (Button) - Navigate to Job Listings page
  - `my-applications-button` (Button) - Navigate to Application Tracking page
  - `companies-button` (Button) - Navigate to Companies Directory page
- Context Variables:
  - `featured_jobs`: List[Dict] each dict contains:
    - `job_id` (int)
    - `title` (str)
    - `company_name` (str)
    - `location` (str)
    - `salary_min` (int)
    - `salary_max` (int)
  - `latest_jobs`: List[Dict] same structure as `featured_jobs`
- Navigation Mappings:
  - `browse-jobs-button`: `url_for('job_listings')`
  - `my-applications-button`: `url_for('application_tracking')`
  - `companies-button`: `url_for('companies_directory')`

## 2. Job Listings Page
- Filename: templates/job_listings.html
- Page Title: Job Listings
- Elements:
  - `listings-page` (Div) - Container for jobs listings
  - `search-input` (Input) - Search field for job title, company, location
  - `category-filter` (Dropdown) - Filter jobs by category
  - `location-filter` (Dropdown) - Filter jobs by location
  - `jobs-grid` (Div) - Grid display of job cards
  - Dynamic: `view-job-button-{{ job.job_id }}` (Button) - View job details
- Context Variables:
  - `jobs`: List[Dict] with fields:
    - `job_id` (int)
    - `title` (str)
    - `company_name` (str)
    - `location` (str)
    - `salary_min` (int)
    - `salary_max` (int)
    - `category` (str)
  - `categories`: List[Dict]
    - `category_id` (int)
    - `category_name` (str)
  - `locations`: List[str]
- Navigation Mappings:
  - `view-job-button-{{ job.job_id }}`: `url_for('job_details', job_id=job.job_id)`

## 3. Job Details Page
- Filename: templates/job_details.html
- Page Title: Job Details
- Elements:
  - `job-details-page` (Div) - Container
  - `job-title` (H1) - Job title
  - `company-name` (Div) - Company name
  - `job-description` (Div) - Full job description and requirements
  - `salary-range` (Div) - Salary range display
  - `apply-now-button` (Button) - Apply for job
- Context Variables:
  - `job`: Dict
    - `job_id` (int)
    - `title` (str)
    - `company_id` (int)
    - `location` (str)
    - `salary_min` (int)
    - `salary_max` (int)
    - `category` (str)
    - `description` (str)
    - `posted_date` (str)
  - `company`: Dict
    - `company_id` (int)
    - `company_name` (str)
- Navigation Mappings:
  - `apply-now-button`: `url_for('application_form', job_id=job.job_id)`

## 4. Application Form Page
- Filename: templates/application_form.html
- Page Title: Submit Application
- Elements:
  - `application-form-page` (Div) - Container
  - `applicant-name` (Input) - Applicant name field
  - `applicant-email` (Input) - Applicant email field
  - `resume-upload` (File Input) - Resume upload field
  - `cover-letter` (Textarea) - Cover letter field
  - `submit-application-button` (Button) - Submit application
- Context Variables:
  - `job`: Dict as above
- Navigation Mappings:
  - (Form submission to the POST route of `/job/<job_id>/apply`)

## 5. Application Tracking Page
- Filename: templates/application_tracking.html
- Page Title: My Applications
- Elements:
  - `tracking-page` (Div) - Container
  - `applications-table` (Table) - Displays applications
  - `status-filter` (Dropdown) - Filter applications by status
  - Dynamic: `view-application-button-{{ app.application_id }}` (Button) - View application details
  - `back-to-dashboard` (Button) - Go back to dashboard
- Context Variables:
  - `applications`: List[Dict]
    - `application_id` (int)
    - `job_title` (str)
    - `company_name` (str)
    - `status` (str)
    - `applied_date` (str)
  - `status_filter`: str
- Navigation Mappings:
  - `view-application-button-{{ app.application_id }}`: `url_for('view_application', app_id=app.application_id)`
  - `back-to-dashboard`: `url_for('dashboard_page')`

## 6. Companies Directory Page
- Filename: templates/companies.html
- Page Title: Company Directory
- Elements:
  - `companies-page` (Div) - Container
  - `companies-list` (Div) - List of company cards
  - `search-company-input` (Input) - Search companies
  - Dynamic: `view-company-button-{{ company.company_id }}` (Button) - View company profile
  - `back-to-dashboard` (Button) - Go back to dashboard
- Context Variables:
  - `companies`: List[Dict]
    - `company_id` (int)
    - `company_name` (str)
    - `industry` (str)
    - `employee_count` (int)
- Navigation Mappings:
  - `view-company-button-{{ company.company_id }}`: `url_for('company_profile', company_id=company.company_id)`
  - `back-to-dashboard`: `url_for('dashboard_page')`

## 7. Company Profile Page
- Filename: templates/company_profile.html
- Page Title: Company Profile
- Elements:
  - `company-profile-page` (Div) - Container
  - `company-info` (Div) - Displays company details
  - `company-jobs` (Div) - Displays open jobs
  - `jobs-list` (Div) - List of job titles with status
  - Dynamic: `view-job-button-{{ job.job_id }}` (Button) - View job details
  - `back-to-companies` (Button) - Back to companies directory
- Context Variables:
  - `company`: Dict
    - `company_id` (int)
    - `company_name` (str)
    - `industry` (str)
    - `location` (str)
    - `description` (str)
  - `company_jobs`: List[Dict] each with:
    - `job_id` (int)
    - `title` (str)
    - `status` (str)
- Navigation Mappings:
  - `view-job-button-{{ job.job_id }}`: `url_for('job_details', job_id=job.job_id)`
  - `back-to-companies`: `url_for('companies_directory')`

## 8. Resume Management Page
- Filename: templates/resumes.html
- Page Title: My Resumes
- Elements:
  - `resume-page` (Div) - Container
  - `resumes-list` (Div) - List of uploaded resumes
  - `upload-resume-button` (Button) - Upload new resume action
  - `resume-file-input` (File Input) - Hidden input for resume upload
  - Dynamic: `delete-resume-button-{{ resume.resume_id }}` (Button) - Delete a resume
  - `back-to-dashboard` (Button) - Back to dashboard
- Context Variables:
  - `resumes`: List[Dict]
    - `resume_id` (int)
    - `applicant_name` (str)
    - `applicant_email` (str)
    - `filename` (str)
    - `upload_date` (str)
    - `summary` (str)
- Navigation Mappings:
  - `upload-resume-button`: On click, triggers `resume-file-input` click
  - `delete-resume-button-{{ resume.resume_id }}`: Posts to `/resume/<resume_id>/delete`
  - `back-to-dashboard`: `url_for('dashboard_page')`

## 9. Search Results Page
- Filename: templates/search_results.html
- Page Title: Search Results
- Elements:
  - `search-results-page` (Div) - Container
  - `search-query-display` (Div) - Displays search query string
  - `results-tabs` (Div) - Tabs for switching results
  - `job-results` (Div) - Job results list
  - `company-results` (Div) - Company results list
  - `no-results-message` (Div) - Message if no results found
- Context Variables:
  - `query` (str)
  - `job_results`: List[Dict] (job listings with: `job_id`, `title`, `company_name`, `location`, `salary_min`, `salary_max`)
  - `company_results`: List[Dict] (company listings with: `company_id`, `company_name`, `industry`, `location`)
- Navigation Mappings:
  - From job results buttons: `url_for('job_details', job_id=job.job_id)`
  - From company results buttons: `url_for('company_profile', company_id=company.company_id)`

---

# Section 3: Data File Schemas

## 1. Jobs Data
- File Path: data/jobs.txt
- Pipe-Delimited Fields:
  1. job_id (int) - Unique identifier for the job posting
  2. title (str) - Job title
  3. company_id (int) - Reference to company
  4. location (str) - Location string (Remote, City, State)
  5. salary_min (int) - Minimum salary
  6. salary_max (int) - Maximum salary
  7. category (str) - Job category name
  8. description (str) - Full job description
  9. posted_date (YYYY-MM-DD) - Date
data examples:
```
1|Senior Python Developer|1|Remote|80000|120000|Technology|Experienced Python developer for web applications|2025-01-15
2|Data Analyst|2|New York, NY|60000|85000|Finance|Analyze financial data and create reports|2025-01-16
3|Healthcare Administrator|3|Los Angeles, CA|50000|70000|Healthcare|Manage hospital operations and patient records|2025-01-14
```

## 2. Companies Data
- File Path: data/companies.txt
- Pipe-Delimited Fields:
  1. company_id (int) - Unique company identifier
  2. company_name (str) - Company name
  3. industry (str) - Industry sector
  4. location (str) - HQ location
  5. employee_count (int) - Number of employees
  6. description (str) - Short company description
Examples:
```
1|TechCorp|Technology|San Francisco, CA|500|Leading software solutions provider
2|FinanceHub|Finance|New York, NY|300|Innovative financial services company
3|MediCare|Healthcare|Los Angeles, CA|200|Premier healthcare management organization
```

## 3. Categories Data
- File Path: data/categories.txt
- Pipe-Delimited Fields:
  1. category_id (int)
  2. category_name (str)
  3. description (str)
Examples:
```
1|Technology|Software, IT, and tech-related positions
2|Finance|Banking, accounting, and finance positions
3|Healthcare|Medical and healthcare industry positions
```

## 4. Applications Data
- File Path: data/applications.txt
- Pipe-Delimited Fields:
  1. application_id (int)
  2. job_id (int)
  3. applicant_name (str)
  4. applicant_email (str)
  5. status (str) - Application status (Applied, Under Review, Interview, Rejected)
  6. applied_date (YYYY-MM-DD)
  7. resume_id (int) - Reference to resumes
Examples:
```
1|1|John Doe|john@email.com|Under Review|2025-01-17|1
2|2|Jane Smith|jane@email.com|Applied|2025-01-16|2
3|3|Robert Johnson|robert@email.com|Interview|2025-01-15|3
```

## 5. Resumes Data
- File Path: data/resumes.txt
- Pipe-Delimited Fields:
  1. resume_id (int)
  2. applicant_name (str)
  3. applicant_email (str)
  4. filename (str) - Name of uploaded resume file
  5. upload_date (YYYY-MM-DD)
  6. summary (str) - Short resume summary
Examples:
```
1|John Doe|john@email.com|john_resume.pdf|2025-01-17|Senior developer with 8 years experience
2|Jane Smith|jane@email.com|jane_resume.pdf|2025-01-16|Data analyst with financial background
3|Robert Johnson|robert@email.com|robert_resume.pdf|2025-01-15|Healthcare administrator with 5 years experience
```

## 6. Job Categories Mapping Data
- File Path: data/job_categories.txt
- Pipe-Delimited Fields:
  1. mapping_id (int)
  2. job_id (int)
  3. category_id (int)
Examples:
```
1|1|1
2|2|2
3|3|3
```

---

**Note:** All data files must have NO header lines; parsing starts from the first line.

---

This specification serves as a definitive guide for backend and frontend developers to implement the JobBoard web application independently and synchronously without assumptions or omissions. All names, IDs, routes, templates, and data structures must be implemented exactly as specified here to ensure seamless integration and functionality.

---
