# JobBoard Web Application Design Specification

---

## Section 1: Flask Routes Specification

### Route List and Details

| Route Path | Function Name | HTTP Method(s) | Template Rendered | Context Variables |
|------------|---------------|----------------|-------------------|-------------------|
| `/` | `root_redirect` | GET | Redirects to `/dashboard` (no template) | None |
| `/dashboard` | `dashboard` | GET | `dashboard.html` |
- `featured_jobs`: list of dict; each dict includes: `job_id` (int), `title` (str), `company_name` (str), `location` (str), `salary_min` (int), `salary_max` (int)

| `/jobs` | `job_listings` | GET | `job_listings.html` |
- `jobs`: list of dict; each includes `job_id` (int), `title` (str), `company_name` (str), `location` (str), `salary_min` (int), `salary_max` (int), `category` (str)
- `categories`: list of str (category names for dropdown)
- `locations`: list of str (location names for dropdown)
- `selected_category`: str or None (currently selected category filter)
- `selected_location`: str or None (currently selected location filter)

| `/job/<int:job_id>` | `job_details` | GET | `job_details.html` |
- `job`: dict with `job_id` (int), `title` (str), `company_name` (str), `description` (str), `location` (str), `salary_min` (int), `salary_max` (int)

| `/apply/<int:job_id>` | `application_form` | GET, POST | `application_form.html` |
- GET context:
  - `job`: dict as above with `job_id`, `title`, `company_name`
- POST expected form fields:
  - `applicant_name` (str)
  - `applicant_email` (str)
  - `resume_file` (file upload)
  - `cover_letter` (str)

| `/applications` | `application_tracking` | GET | `application_tracking.html` |
- `applications`: list of dict; each dict with `application_id` (int), `job_title` (str), `company_name` (str), `status` (str), `applied_date` (str, format "YYYY-MM-DD")
- `status_options`: list of str: ["All", "Applied", "Under Review", "Interview", "Rejected"]
- `selected_status`: str or None (current filter)

| `/application/<int:application_id>` | `application_details` | GET | `application_details.html` |
- `application`: dict including `application_id` (int), `job_title` (str), `company_name` (str), `applicant_name` (str), `applicant_email` (str), `status` (str), `applied_date` (str), `resume_filename` (str), `cover_letter` (str)

| `/companies` | `companies_directory` | GET | `companies.html` |
- `companies`: list of dict; each with `company_id` (int), `company_name` (str), `industry` (str), `employee_count` (int)
- `search_query`: str or None (search input)

| `/company/<int:company_id>` | `company_profile` | GET | `company_profile.html` |
- `company`: dict with `company_id` (int), `company_name` (str), `industry` (str), `location` (str), `description` (str), `employee_count` (int)
- `jobs`: list of dict; each job with `job_id` (int), `title` (str), `status` (str, typically "Open")

| `/resumes` | `resume_management` | GET | `resume_management.html` |
- `resumes`: list of dict; each with `resume_id` (int), `applicant_name` (str), `applicant_email` (str), `filename` (str), `upload_date` (str)

| `/upload_resume` | `upload_resume` | POST | Redirect (no template) |
- Expected form fields:
  - `applicant_name` (str)
  - `applicant_email` (str)
  - `resume_file` (file upload)
  - `summary` (str, optional)

| `/delete_resume/<int:resume_id>` | `delete_resume` | POST | Redirect (no template) |

| `/search` | `search_results` | GET | `search_results.html` |
- `query`: str (search query)
- `job_results`: list of dict; each with `job_id` (int), `title` (str), `company_name` (str), `location` (str), `salary_min` (int), `salary_max` (int)
- `company_results`: list of dict; each with `company_id` (int), `company_name` (str), `industry` (str), `location` (str)

---

## Section 2: HTML Template Specifications

### 1. templates/dashboard.html
- Page Title: "Job Board Dashboard"
- Element IDs:
  - `dashboard-page` (Div): Container for dashboard page
  - `featured-jobs` (Div): Shows featured job recommendations
  - `browse-jobs-button` (Button): Navigates to Job Listings page
  - `my-applications-button` (Button): Navigates to Application Tracking page
  - `companies-button` (Button): Navigates to Companies Directory page
- Context Variables:
  - `featured_jobs` (list of dict): Each dict with `job_id`, `title`, `company_name`, `location`, `salary_min`, `salary_max`
- Navigation:
  - `browse-jobs-button`: `url_for('job_listings')`
  - `my-applications-button`: `url_for('application_tracking')`
  - `companies-button`: `url_for('companies_directory')`

### 2. templates/job_listings.html
- Page Title: "Job Listings"
- Element IDs:
  - `listings-page` (Div): Container for job listings
  - `search-input` (Input): Text input for searching jobs
  - `category-filter` (Dropdown): Dropdown for job categories
  - `location-filter` (Dropdown): Dropdown for locations
  - `jobs-grid` (Div): Grid displaying job cards
  - `view-job-button-{{ job.job_id }}` (Button): View details for specific job
- Context Variables:
  - `jobs` (list of dict): Jobs data with `job_id`, `title`, `company_name`, `location`, `salary_min`, `salary_max`, `category`
  - `categories` (list of str): Available categories
  - `locations` (list of str): Available locations
  - `selected_category` (str or None): Current category filter
  - `selected_location` (str or None): Current location filter
- Navigation:
  - For each job card, `view-job-button-{{ job.job_id }}` directs to `url_for('job_details', job_id=job.job_id)`

### 3. templates/job_details.html
- Page Title: "Job Details"
- Element IDs:
  - `job-details-page` (Div): Container page element
  - `job-title` (H1): Displays job title
  - `company-name` (Div): Displays company name
  - `job-description` (Div): Displays full job description and requirements
  - `salary-range` (Div): Displays salary range
  - `apply-now-button` (Button): Button to apply for the job
- Context Variables:
  - `job` (dict): Job details - `job_id`, `title`, `company_name`, `description`, `location`, `salary_min`, `salary_max`
- Navigation:
  - `apply-now-button` triggers navigation to `url_for('application_form', job_id=job.job_id)`

### 4. templates/application_form.html
- Page Title: "Submit Application"
- Element IDs:
  - `application-form-page` (Div): Container for application form
  - `applicant-name` (Input): For applicant to enter their name
  - `applicant-email` (Input): For applicant to enter their email
  - `resume-upload` (File Input): Upload resume file
  - `cover-letter` (Textarea): Input for cover letter text
  - `submit-application-button` (Button): Submit application
- Context Variables:
  - `job` (dict): Job info - `job_id`, `title`, `company_name`
- Navigation:
  - Form should POST to `url_for('application_form', job_id=job.job_id)`

### 5. templates/application_tracking.html
- Page Title: "My Applications"
- Element IDs:
  - `tracking-page` (Div): Container page
  - `applications-table` (Table): Table displaying applications with columns for job title, company, status, applied date
  - `status-filter` (Dropdown): Dropdown for filtering application status
  - `view-application-button-{{ application.application_id }}` (Button): View details for each application
  - `back-to-dashboard` (Button): Button to go back to dashboard
- Context Variables:
  - `applications` (list of dict): Each dict with `application_id`, `job_title`, `company_name`, `status`, `applied_date`
  - `status_options` (list of str): ["All", "Applied", "Under Review", "Interview", "Rejected"]
  - `selected_status` (str or None): Currently selected status filter
- Navigation:
  - For each application, `view-application-button-{{ application.application_id }}` directs to `url_for('application_details', application_id=application.application_id)`
  - `back-to-dashboard` routes to `url_for('dashboard')`

### 6. templates/application_details.html
- Page Title: "Application Details"
- Element IDs:
  - `application-details-page` (Div): Container page
  - `job-title` (Div): Job title
  - `company-name` (Div): Company name
  - `applicant-name` (Div): Applicant's name
  - `applicant-email` (Div): Applicant's email
  - `status` (Div): Current application status
  - `applied-date` (Div): Date application was submitted
  - `resume-filename` (Div): Filename of uploaded resume
  - `cover-letter` (Div): Cover letter text
  - `back-to-applications` (Button): Button to navigate back to application tracking
- Context Variables:
  - `application` (dict): Includes all above fields
- Navigation:
  - `back-to-applications` routes to `url_for('application_tracking')`

### 7. templates/companies.html
- Page Title: "Company Directory"
- Element IDs:
  - `companies-page` (Div): Container for page
  - `companies-list` (Div): List container for company cards
  - `search-company-input` (Input): Search input for companies
  - `view-company-button-{{ company.company_id }}` (Button): View specific company profile
  - `back-to-dashboard` (Button): Navigate back to dashboard
- Context Variables:
  - `companies` (list of dict): Each dict has `company_id`, `company_name`, `industry`, `employee_count`
  - `search_query` (str or None): Current search string
- Navigation:
  - For each company card, `view-company-button-{{ company.company_id }}` links to `url_for('company_profile', company_id=company.company_id)`
  - `back-to-dashboard` links to `url_for('dashboard')`

### 8. templates/company_profile.html
- Page Title: "Company Profile"
- Element IDs:
  - `company-profile-page` (Div): Page container
  - `company-info` (Div): Displays company info: name, industry, location, description
  - `company-jobs` (Div): Container for jobs of the company
  - `jobs-list` (Div): List of jobs
  - `view-job-button-{{ job.job_id }}` (Button): Button to view job detail
  - `back-to-companies` (Button): Button to go back to companies directory
- Context Variables:
  - `company` (dict): Company info as above
  - `jobs` (list of dict): Each with `job_id`, `title`, `status` (typically "Open")
- Navigation:
  - For each job, `view-job-button-{{ job.job_id }}` links to `url_for('job_details', job_id=job.job_id)`
  - `back-to-companies` routes to `url_for('companies_directory')`

### 9. templates/resume_management.html
- Page Title: "My Resumes"
- Element IDs:
  - `resume-page` (Div): Page container
  - `resumes-list` (Div): List of resumes
  - `upload-resume-button` (Button): Button to initiate upload
  - `resume-file-input` (File Input, hidden): Hidden file input for upload
  - `delete-resume-button-{{ resume.resume_id }}` (Button): Delete button for each resume
  - `back-to-dashboard` (Button): Return to dashboard
- Context Variables:
  - `resumes` (list of dict): Each dict with `resume_id`, `applicant_name`, `applicant_email`, `filename`, `upload_date`
- Navigation:
  - `upload-resume-button` triggers file input and submits form to `url_for('upload_resume')` (POST)
  - For each resume, `delete-resume-button-{{ resume.resume_id }}` triggers POST to `url_for('delete_resume', resume_id=resume.resume_id)`
  - `back-to-dashboard` links to `url_for('dashboard')`

### 10. templates/search_results.html
- Page Title: "Search Results"
- Element IDs:
  - `search-results-page` (Div): Page container
  - `search-query-display` (Div): Displays the search term
  - `results-tabs` (Div): Tabs to switch between job and company results
  - `job-results` (Div): Job search results container
  - `company-results` (Div): Company search results container
  - `no-results-message` (Div): Displayed if no results found
- Context Variables:
  - `query` (str): Search term
  - `job_results` (list of dict): Each with `job_id`, `title`, `company_name`, `location`, `salary_min`, `salary_max`
  - `company_results` (list of dict): Each with `company_id`, `company_name`, `industry`, `location`
- Navigation:
  - Job results link to: `url_for('job_details', job_id=job.job_id)`
  - Company results link to: `url_for('company_profile', company_id=company.company_id)`

---

## Section 3: Data File Schemas

### 1. data/jobs.txt
- Fields (Pipe-delimited, no header):
  1. `job_id` (int)
  2. `title` (str)
  3. `company_id` (int)
  4. `location` (str)
  5. `salary_min` (int)
  6. `salary_max` (int)
  7. `category` (str)
  8. `description` (str)
  9. `posted_date` (YYYY-MM-DD string)
- Description: Stores job postings.
- Example Rows:
  ```
  1|Senior Python Developer|1|Remote|80000|120000|Technology|Experienced Python developer for web applications|2025-01-15
  2|Data Analyst|2|New York, NY|60000|85000|Finance|Analyze financial data and create reports|2025-01-16
  3|Healthcare Administrator|3|Los Angeles, CA|50000|70000|Healthcare|Manage hospital operations and patient records|2025-01-14
  ```

### 2. data/companies.txt
- Fields (Pipe-delimited, no header):
  1. `company_id` (int)
  2. `company_name` (str)
  3. `industry` (str)
  4. `location` (str)
  5. `employee_count` (int)
  6. `description` (str)
- Description: Companies information.
- Example Rows:
  ```
  1|TechCorp|Technology|San Francisco, CA|500|Leading software solutions provider
  2|FinanceHub|Finance|New York, NY|300|Innovative financial services company
  3|MediCare|Healthcare|Los Angeles, CA|200|Premier healthcare management organization
  ```

### 3. data/categories.txt
- Fields (Pipe-delimited, no header):
  1. `category_id` (int)
  2. `category_name` (str)
  3. `description` (str)
- Description: Job categories.
- Example Rows:
  ```
  1|Technology|Software, IT, and tech-related positions
  2|Finance|Banking, accounting, and finance positions
  3|Healthcare|Medical and healthcare industry positions
  ```

### 4. data/applications.txt
- Fields (Pipe-delimited, no header):
  1. `application_id` (int)
  2. `job_id` (int)
  3. `applicant_name` (str)
  4. `applicant_email` (str)
  5. `status` (str, allowed values: "Applied", "Under Review", "Interview", "Rejected")
  6. `applied_date` (YYYY-MM-DD string)
  7. `resume_id` (int)
- Description: Job applications.
- Example Rows:
  ```
  1|1|John Doe|john@email.com|Under Review|2025-01-17|1
  2|2|Jane Smith|jane@email.com|Applied|2025-01-16|2
  3|3|Robert Johnson|robert@email.com|Interview|2025-01-15|3
  ```

### 5. data/resumes.txt
- Fields (Pipe-delimited, no header):
  1. `resume_id` (int)
  2. `applicant_name` (str)
  3. `applicant_email` (str)
  4. `filename` (str)
  5. `upload_date` (YYYY-MM-DD string)
  6. `summary` (str)
- Description: Resumes metadata.
- Example Rows:
  ```
  1|John Doe|john@email.com|john_resume.pdf|2025-01-17|Senior developer with 8 years experience
  2|Jane Smith|jane@email.com|jane_resume.pdf|2025-01-16|Data analyst with financial background
  3|Robert Johnson|robert@email.com|robert_resume.pdf|2025-01-15|Healthcare administrator with 5 years experience
  ```

### 6. data/job_categories.txt
- Fields (Pipe-delimited, no header):
  1. `mapping_id` (int)
  2. `job_id` (int)
  3. `category_id` (int)
- Description: Maps jobs to categories.
- Example Rows:
  ```
  1|1|1
  2|2|2
  3|3|3
  ```

---

**End of Design Specification Document**

---

This comprehensive design spec fully covers all routes, templates, and data schemas enabling backend and frontend development in parallel with no missing information or assumptions.