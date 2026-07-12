# JobBoard Web Application Design Specification

---

# Section 1: Flask Routes Specification

| Route Path               | Function Name          | HTTP Method(s) | Template Rendered    | Context Variables Passed to Template                         | POST Input Expectations                           |
|--------------------------|------------------------|----------------|---------------------|--------------------------------------------------------------|--------------------------------------------------|
| `/`                      | root_redirect           | GET            | Redirect to `/dashboard` | None                                                         | N/A                                              |
| `/dashboard`             | dashboard_page         | GET            | dashboard.html       | featured_jobs: list of dict with keys: job_id(int), title(str), company_name(str), location(str), salary_min(int), salary_max(int) | None                                             |
| `/jobs`                  | job_listings_page       | GET            | listings.html        | jobs: list of dict {job_id(int), title(str), company_name(str), location(str), salary_min(int), salary_max(int), category(str)}
categories: list of str
locations: list of str | None                                             |
| `/job/<int:job_id>`      | job_details_page        | GET            | job_details.html     | job: dict {job_id(int), title(str), company_name(str), location(str), salary_min(int), salary_max(int), category(str), description(str), posted_date(str)} | None                                             |
| `/job/<int:job_id>/apply`| application_form_page   | GET            | application_form.html| job_id: int                                                  | None                                             |
| `/job/<int:job_id>/apply`| submit_application      | POST           | application_form.html or redirect | form error messages (if any), else redirect to `/applications` | applicant_name: str, applicant_email: str, resume_file: file upload, cover_letter: str |
| `/applications`          | application_tracking_page| GET           | tracking.html        | applications: list of dict {application_id(int), job_title(str), company_name(str), status(str), applied_date(str)}
status_filter: str (from query parameters, optional) | None                                             |
| `/application/<int:application_id>` | application_details_page | GET       | application_details.html (note: page not explicitly described, assumed) | application: dict {application_id(int), job_id(int), applicant_name(str), applicant_email(str), status(str), applied_date(str), resume_id(int)} | None |
| `/companies`             | companies_directory_page| GET            | companies.html       | companies: list of dict {company_id(int), company_name(str), industry(str), location(str), employee_count(int)} | None                                             |
| `/company/<int:company_id>`| company_profile_page  | GET            | company_profile.html | company: dict {company_id(int), company_name(str), industry(str), location(str), employee_count(int), description(str)}
jobs: list of dict containing jobs from this company with keys as per job_details_page without description and posted_date | None                                             |
| `/resumes`               | resume_management_page  | GET            | resume.html          | resumes: list of dict {resume_id(int), applicant_name(str), applicant_email(str), filename(str), upload_date(str), summary(str)} | None                                             |
| `/resumes/upload`        | upload_resume           | POST           | resume.html (re-rendered on error) or redirect | form error messages (if any)                      | resume_file: file upload, applicant_name: str, applicant_email: str, summary: str |
| `/resumes/delete/<int:resume_id>` | delete_resume     | POST           | redirect to `/resumes`| None                                                         | None                                             |
| `/search`                | search_results_page     | GET            | search_results.html  | query: str, job_results: list of dict{job_id(int), title(str), company_name(str), location(str), salary_min(int), salary_max(int)}
company_results: list of dict{company_id(int), company_name(str), industry(str), location(str)} | None                                             |

**Detailed Route Specifications:**

---

1. `/` (Root)  
- Function Name: `root_redirect`  
- HTTP Method: GET  
- Action: Redirects to `/dashboard`

2. `/dashboard`  
- Function Name: `dashboard_page`  
- HTTP Method: GET  
- Template: `dashboard.html`  
- Context Variables:  
  - `featured_jobs` (list of dict): Each dict includes: `job_id` (int), `title` (str), `company_name` (str), `location` (str), `salary_min` (int), `salary_max` (int)

3. `/jobs`  
- Function Name: `job_listings_page`  
- HTTP Method: GET  
- Template: `listings.html`  
- Context Variables:  
  - `jobs` (list of dict): Each includes: `job_id` (int), `title` (str), `company_name` (str), `location` (str), `salary_min` (int), `salary_max` (int), `category` (str)
  - `categories` (list of str): Available categories extracted from `categories.txt` (category_name)
  - `locations` (list of str): Unique locations from jobs data

4. `/job/<int:job_id>`  
- Function Name: `job_details_page`  
- HTTP Method: GET  
- Template: `job_details.html`  
- Context Variables:  
  - `job` (dict): Complete job details including `job_id`, `title`, `company_name`, `location`, `salary_min`, `salary_max`, `category`, `description`, `posted_date`

5. `/job/<int:job_id>/apply` (GET)  
- Function Name: `application_form_page`  
- HTTP Method: GET  
- Template: `application_form.html`  
- Context Variables:  
  - `job_id` (int): ID of job applied for

6. `/job/<int:job_id>/apply` (POST)  
- Function Name: `submit_application`  
- HTTP Method: POST  
- Template: `application_form.html` (re-rendered if form errors)  
- Inputs:  
  - `applicant_name`: string from form
  - `applicant_email`: string from form
  - `resume_file`: file upload
  - `cover_letter`: string from form

7. `/applications`  
- Function Name: `application_tracking_page`  
- HTTP Method: GET  
- Template: `tracking.html`  
- Context Variables:  
  - `applications` (list of dict): Each dict contains: `application_id`, `job_title`, `company_name`, `status`, `applied_date`
  - `status_filter` (str): filter value from query parameter; default is 'All'

8. `/application/<int:application_id>` [Assumed Route for application details page]
- Function Name: `application_details_page`
- HTTP Method: GET
- Template: `application_details.html`
- Context Variables:
  - `application` (dict): all details about the application, includes `application_id`, `job_id`, `applicant_name`, `applicant_email`, `status`, `applied_date`, `resume_id`

9. `/companies`  
- Function Name: `companies_directory_page`  
- HTTP Method: GET  
- Template: `companies.html`  
- Context Variables:  
  - `companies` (list of dict): Each dict has: `company_id`, `company_name`, `industry`, `location`, `employee_count`

10. `/company/<int:company_id>`  
- Function Name: `company_profile_page`  
- HTTP Method: GET  
- Template: `company_profile.html`  
- Context Variables:  
  - `company` (dict): company details including `company_id`, `company_name`, `industry`, `location`, `employee_count`, `description`
  - `jobs` (list of dict): jobs associated with the company, with keys: `job_id`, `title`, `location`, `salary_min`, `salary_max`, `category`, `status` (optional, default to open if not specified or could omit if no status field)

11. `/resumes`  
- Function Name: `resume_management_page`  
- HTTP Method: GET  
- Template: `resume.html`  
- Context Variables:  
  - `resumes` (list of dict): each dict contains `resume_id`, `applicant_name`, `applicant_email`, `filename`, `upload_date`, `summary`

12. `/resumes/upload`  
- Function Name: `upload_resume`  
- HTTP Method: POST  
- Template: `resume.html` (re-rendered if error)  
- Inputs:  
  - resume_file: uploaded file
  - applicant_name: string
  - applicant_email: string
  - summary: string description

13. `/resumes/delete/<int:resume_id>`  
- Function Name: `delete_resume`  
- HTTP Method: POST  
- Template: Redirect to `/resumes`  
- Inputs: None

14. `/search`  
- Function Name: `search_results_page`  
- HTTP Method: GET  
- Template: `search_results.html`  
- Context Variables:  
  - `query` (str): the search query string
  - `job_results` (list of dict): search results for jobs, with keys: `job_id`, `title`, `company_name`, `location`, `salary_min`, `salary_max`
  - `company_results` (list of dict): search results for companies, with keys: `company_id`, `company_name`, `industry`, `location`

# Section 2: HTML Template Specifications

## 1. dashboard.html
- Filename: `templates/dashboard.html`
- Page Title: "Job Board Dashboard"
- Element IDs:
  - `dashboard-page`: div container for dashboard page
  - `featured-jobs`: div showing featured job listings
  - `browse-jobs-button`: button to navigate to `/jobs`
  - `my-applications-button`: button to navigate to `/applications`
  - `companies-button`: button to navigate to `/companies`
- Context Variables:
  - `featured_jobs`: list of dict, each dict with keys: `job_id` (int), `title` (str), `company_name` (str), `location` (str), `salary_min` (int), `salary_max` (int)
- Navigation:
  - `browse-jobs-button` -> url_for('job_listings_page')
  - `my-applications-button` -> url_for('application_tracking_page')
  - `companies-button` -> url_for('companies_directory_page')

## 2. listings.html
- Filename: `templates/listings.html`
- Page Title: "Job Listings"
- Element IDs:
  - `listings-page`: div container for job listings
  - `search-input`: input field to enter search terms
  - `category-filter`: dropdown to select job category filter
  - `location-filter`: dropdown to select location filter
  - `jobs-grid`: div container grid for job cards
  - `view-job-button-{{ job.job_id }}`: button on each job card to view details
- Context Variables:
  - `jobs`: list of dict, each with keys: `job_id` (int), `title` (str), `company_name` (str), `location` (str), `salary_min` (int), `salary_max` (int), `category` (str)
  - `categories`: list of str for category names
  - `locations`: list of str for locations
- Navigation:
  - `view-job-button-{{ job.job_id }}` -> url_for('job_details_page', job_id=job.job_id)

## 3. job_details.html
- Filename: `templates/job_details.html`
- Page Title: "Job Details"
- Element IDs:
  - `job-details-page`: div container for job details
  - `job-title`: h1 element showing job title
  - `company-name`: div showing company name
  - `job-description`: div with full job description and requirements
  - `salary-range`: div with salary range
  - `apply-now-button`: button to navigate to application form
- Context Variables:
  - `job`: dict with keys matching jobs data and company_name
- Navigation:
  - `apply-now-button` -> url_for('application_form_page', job_id=job.job_id)

## 4. application_form.html
- Filename: `templates/application_form.html`
- Page Title: "Submit Application"
- Element IDs:
  - `application-form-page`: div container for application form
  - `applicant-name`: input field for applicant's name
  - `applicant-email`: input field for applicant's email
  - `resume-upload`: file input for uploading resume
  - `cover-letter`: textarea for cover letter
  - `submit-application-button`: button to submit application
- Context Variables:
  - `job_id`: int for job being applied to
  - `error_messages` (optional): list of error strings from form validation
- Navigation:
  - Form POSTs to url_for('submit_application', job_id=job_id)

## 5. tracking.html
- Filename: `templates/tracking.html`
- Page Title: "My Applications"
- Element IDs:
  - `tracking-page`: div container for tracking
  - `applications-table`: table listing applications with columns: job title, company, status, date applied
  - `status-filter`: dropdown to filter applications by status
  - `view-application-button-{{ application.application_id }}`: button to view specific application
  - `back-to-dashboard`: button to go back to dashboard
- Context Variables:
  - `applications`: list of dict, each with keys: `application_id` (int), `job_title` (str), `company_name` (str), `status` (str), `applied_date` (str)
  - `status_filter`: str representing selected filter
- Navigation:
  - `view-application-button-{{ application.application_id }}` -> url_for('application_details_page', application_id=application.application_id)
  - `back-to-dashboard` -> url_for('dashboard_page')

## 6. companies.html
- Filename: `templates/companies.html`
- Page Title: "Company Directory"
- Element IDs:
  - `companies-page`: div container for companies directory
  - `companies-list`: div containing company cards
  - `search-company-input`: input field to search companies
  - `view-company-button-{{ company.company_id }}`: button to view company profile
  - `back-to-dashboard`: button to navigate back to dashboard
- Context Variables:
  - `companies`: list of dict, each with keys: `company_id` (int), `company_name` (str), `industry` (str), `location` (str), `employee_count` (int)
- Navigation:
  - `view-company-button-{{ company.company_id }}` -> url_for('company_profile_page', company_id=company.company_id)
  - `back-to-dashboard` -> url_for('dashboard_page')

## 7. company_profile.html
- Filename: `templates/company_profile.html`
- Page Title: "Company Profile"
- Element IDs:
  - `company-profile-page`: div container for company profile
  - `company-info`: div showing company name, industry, location, and description
  - `company-jobs`: div container for jobs at this company
  - `jobs-list`: div listing job items
  - `view-job-button-{{ job.job_id }}`: button to view job details from company profile
  - `back-to-companies`: button to return to companies directory
- Context Variables:
  - `company`: dict with keys: `company_id`, `company_name`, `industry`, `location`, `employee_count`, `description`
  - `jobs`: list of dict with keys: `job_id`, `title`, `location`, `salary_min`, `salary_max`, `category`
- Navigation:
  - `view-job-button-{{ job.job_id }}` -> url_for('job_details_page', job_id=job.job_id)
  - `back-to-companies` -> url_for('companies_directory_page')

## 8. resume.html
- Filename: `templates/resume.html`
- Page Title: "My Resumes"
- Element IDs:
  - `resume-page`: div container for resumes page
  - `resumes-list`: div listing uploaded resumes with details
  - `upload-resume-button`: button to trigger hidden file input
  - `resume-file-input`: hidden file input for uploading resumes
  - `delete-resume-button-{{ resume.resume_id }}`: button to delete specific resume
  - `back-to-dashboard`: button to navigate back to dashboard
- Context Variables:
  - `resumes`: list of dict with keys: `resume_id`, `applicant_name`, `applicant_email`, `filename`, `upload_date`, `summary`
- Navigation:
  - `upload-resume-button` triggers click on `resume-file-input`
  - `delete-resume-button-{{ resume.resume_id }}` -> POST to a route to delete (e.g., `/resumes/delete/<resume_id>`)
  - `back-to-dashboard` -> url_for('dashboard_page')

## 9. search_results.html
- Filename: `templates/search_results.html`
- Page Title: "Search Results"
- Element IDs:
  - `search-results-page`: div container for search results
  - `search-query-display`: div showing the user's search query
  - `results-tabs`: div with tabs to toggle between job and company results
  - `job-results`: div container for job search results
  - `company-results`: div container for company search results
  - `no-results-message`: div shown if no results found
- Context Variables:
  - `query`: str for user search input
  - `job_results`: list of dict, each with keys: `job_id`, `title`, `company_name`, `location`, `salary_min`, `salary_max`
  - `company_results`: list of dict, each with keys: `company_id`, `company_name`, `industry`, `location`
- Navigation:
  - Job or company items linking to their respective details pages using url_for functions

---

# Section 3: Data File Schemas

### 1. Jobs Data - `data/jobs.txt`
- Fields (pipe `|` delimited):
  - `job_id` (int): Unique job identifier
  - `title` (str): Job title
  - `company_id` (int): Identifier for company offering the job
  - `location` (str): Job location
  - `salary_min` (int): Minimum salary
  - `salary_max` (int): Maximum salary
  - `category` (str): Job category name
  - `description` (str): Job description and requirements
  - `posted_date` (str, YYYY-MM-DD): Date posted
- Description: Stores all job postings with details
- Example rows:
  ```
  1|Senior Python Developer|1|Remote|80000|120000|Technology|Experienced Python developer for web applications|2025-01-15
  2|Data Analyst|2|New York, NY|60000|85000|Finance|Analyze financial data and create reports|2025-01-16
  3|Healthcare Administrator|3|Los Angeles, CA|50000|70000|Healthcare|Manage hospital operations and patient records|2025-01-14
  ```

### 2. Companies Data - `data/companies.txt`
- Fields (pipe `|` delimited):
  - `company_id` (int): Unique company identifier
  - `company_name` (str): Company name
  - `industry` (str): Industry sector
  - `location` (str): Company location
  - `employee_count` (int): Number of employees
  - `description` (str): Company overview
- Description: Stores all companies with details
- Example rows:
  ```
  1|TechCorp|Technology|San Francisco, CA|500|Leading software solutions provider
  2|FinanceHub|Finance|New York, NY|300|Innovative financial services company
  3|MediCare|Healthcare|Los Angeles, CA|200|Premier healthcare management organization
  ```

### 3. Categories Data - `data/categories.txt`
- Fields (pipe `|` delimited):
  - `category_id` (int): Category identifier
  - `category_name` (str): Name of category
  - `description` (str): Description of category
- Description: Stores job categories
- Example rows:
  ```
  1|Technology|Software, IT, and tech-related positions
  2|Finance|Banking, accounting, and finance positions
  3|Healthcare|Medical and healthcare industry positions
  ```

### 4. Applications Data - `data/applications.txt`
- Fields (pipe `|` delimited):
  - `application_id` (int): Unique application identifier
  - `job_id` (int): Job applied for
  - `applicant_name` (str): Applicant's full name
  - `applicant_email` (str): Applicant's email address
  - `status` (str): Current application status (Applied, Under Review, Interview, Rejected)
  - `applied_date` (str, YYYY-MM-DD): Date application submitted
  - `resume_id` (int): Identifier for uploaded resume
- Description: Records job applications submitted
- Example rows:
  ```
  1|1|John Doe|john@email.com|Under Review|2025-01-17|1
  2|2|Jane Smith|jane@email.com|Applied|2025-01-16|2
  3|3|Robert Johnson|robert@email.com|Interview|2025-01-15|3
  ```

### 5. Resumes Data - `data/resumes.txt`
- Fields (pipe `|` delimited):
  - `resume_id` (int): Unique resume identifier
  - `applicant_name` (str): Applicant name associated with resume
  - `applicant_email` (str): Applicant email
  - `filename` (str): Uploaded filename
  - `upload_date` (str, YYYY-MM-DD): Date uploaded
  - `summary` (str): Brief summary or description of resume
- Description: Stores uploaded resumes metadata
- Example rows:
  ```
  1|John Doe|john@email.com|john_resume.pdf|2025-01-17|Senior developer with 8 years experience
  2|Jane Smith|jane@email.com|jane_resume.pdf|2025-01-16|Data analyst with financial background
  3|Robert Johnson|robert@email.com|robert_resume.pdf|2025-01-15|Healthcare administrator with 5 years experience
  ```

### 6. Job Categories Mapping Data - `data/job_categories.txt`
- Fields (pipe `|` delimited):
  - `mapping_id` (int): Unique mapping identifier
  - `job_id` (int): Job identifier
  - `category_id` (int): Category identifier
- Description: Mapping between jobs and categories for indexing 
- Example rows:
  ```
  1|1|1
  2|2|2
  3|3|3
  ```

---

End of design_spec.md
