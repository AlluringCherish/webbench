# Design Specification for JobBoard Web Application

---

## Section 1: Flask Routes Specification

| Route Path                 | Function Name            | HTTP Method(s) | Template Rendered       | Context Variables Passed to Templates                                  |
|----------------------------|--------------------------|----------------|-------------------------|-------------------------------------------------------------------------|
| /                          | root_redirect            | GET            | Redirects to /dashboard  | None                                                                    |
| /dashboard                 | dashboard                | GET            | dashboard.html          | featured_jobs: List[Dict] with keys (job_id:int, title:str, company_name:str, location:str, salary_min:int, salary_max:int)           |
|                            |                          |                |                         |                                                                                |
| /jobs                      | job_listings             | GET            | jobs.html               | jobs: List[Dict] with keys (job_id:int, title:str, company_name:str, location:str, salary_min:int, salary_max:int, category:str)    |
|                            |                          | POST           | jobs.html               | jobs (filtered after POST) - same as above; form data: search_input(str), category_filter(str), location_filter(str)                 |
| /job/<int:job_id>          | job_details              | GET            | job_details.html        | job: Dict with keys (job_id:int, title:str, company_name:str, description:str, salary_min:int, salary_max:int, location:str)         |
| /apply/<int:job_id>        | application_form         | GET            | application_form.html   | job: Dict with keys (job_id:int, title:str, company_name:str)                                                                  |
|                            |                          | POST           | application_form.html   | success_msg: str (on successful submission) or error_msg: str (on failure); form fields: applicant_name(str), applicant_email(str), resume_upload (File), cover_letter(str)         |
| /applications              | application_tracking     | GET            | applications.html       | applications: List[Dict] with keys (application_id:int, job_title:str, company_name:str, status:str, applied_date:str)           |
|                            |                          | POST           | applications.html       | applications (filtered by status); form data: status_filter(str)                                                                |
| /application/<int:app_id>  | application_details      | GET            | application_details.html| application: Dict (application_id:int, job_title:str, company_name:str, status:str, applied_date:str, applicant_name:str, applicant_email:str, resume_id:int, cover_letter:str)    |
| /companies                 | companies_directory      | GET            | companies.html          | companies: List[Dict] with keys (company_id:int, company_name:str, industry:str, employee_count:int)                             |
|                            |                          | POST           | companies.html          | companies filtered by search input: search_company_input(str)                                                                  |
| /company/<int:company_id>  | company_profile          | GET            | company_profile.html    | company: Dict (company_id:int, company_name:str, industry:str, location:str, description:str, employee_count:int)                 |
|                            |                          |                         | company_jobs: List[Dict] with keys (job_id:int, title:str, status:str)                                                           |
| /resumes                   | resume_management        | GET            | resumes.html            | resumes: List[Dict] with keys (resume_id:int, filename:str, upload_date:str, summary:str)                                       |
|                            |                          | POST           | resumes.html            | form fields: resume_file (File), applicant_name (str), applicant_email (str); updated resumes list after upload                   |
| /resume/delete/<int:resume_id> | delete_resume         | POST           | resumes.html            | updated resumes list after deletion                                                                                           |
| /search                   | search_results           | GET            | search_results.html     | query_str: str, job_results: List[Dict] with keys (job_id:int, title:str, company_name:str, location:str),
|                            |                          |                         | company_results: List[Dict] with keys (company_id:int, company_name:str, industry:str)                                        |

### Notes for POST routes:
- `/jobs` POST expects form data: `search_input` (str), `category_filter` (str), `location_filter` (str) to filter jobs.
- `/apply/<int:job_id>` POST expects form fields: `applicant_name` (str), `applicant_email` (str), `resume_upload` (File), `cover_letter` (str).
- `/applications` POST expects form field: `status_filter` (str).
- `/companies` POST expects form field: `search_company_input` (str).
- `/resumes` POST expects form fields: `resume_file` (File), `applicant_name` (str), `applicant_email` (str).
- `/resume/delete/<int:resume_id>` POST expects no form fields other than the route parameter.

---

## Section 2: HTML Template Specifications

All templates are located in the `templates/` directory.

### 1. dashboard.html
- Page Title: "Job Board Dashboard"
- Element IDs:
  - `dashboard-page` (Div): Container for the dashboard page
  - `featured-jobs` (Div): Display of featured job recommendations
  - `browse-jobs-button` (Button): Navigate to job listings page
  - `my-applications-button` (Button): Navigate to applications tracking page
  - `companies-button` (Button): Navigate to companies directory page
- Context Variables:
  - `featured_jobs`: List of dicts each with keys `job_id` (int), `title` (str), `company_name` (str), `location` (str), `salary_min` (int), `salary_max` (int)
- Navigation Mappings:
  - `browse-jobs-button`: `url_for('job_listings')`
  - `my-applications-button`: `url_for('application_tracking')`
  - `companies-button`: `url_for('companies_directory')`

### 2. jobs.html
- Page Title: "Job Listings"
- Element IDs:
  - `listings-page` (Div): Container for the listings page
  - `search-input` (Input): Search jobs by title, company, or location
  - `category-filter` (Dropdown): Filter jobs by category
  - `location-filter` (Dropdown): Filter jobs by location
  - `jobs-grid` (Div): Displays job cards
  - `view-job-button-{{ job.job_id }}` (Button, dynamic): View details of the job with job_id
- Context Variables:
  - `jobs`: List of dicts with keys `job_id` (int), `title` (str), `company_name` (str), `location` (str), `salary_min` (int), `salary_max` (int), `category` (str)
- Navigation Mappings:
  - Each `view-job-button-{{ job.job_id }}` navigates to `url_for('job_details', job_id=job.job_id)`

### 3. job_details.html
- Page Title: "Job Details"
- Element IDs:
  - `job-details-page` (Div): Container for job details page
  - `job-title` (H1): Displays job title
  - `company-name` (Div): Displays company name
  - `job-description` (Div): Displays job description and requirements
  - `salary-range` (Div): Displays salary range
  - `apply-now-button` (Button): Navigate to application form
- Context Variables:
  - `job`: Dict with keys `job_id` (int), `title` (str), `company_name` (str), `description` (str), `salary_min` (int), `salary_max` (int), `location` (str)
- Navigation Mappings:
  - `apply-now-button`: `url_for('application_form', job_id=job.job_id)`

### 4. application_form.html
- Page Title: "Submit Application"
- Element IDs:
  - `application-form-page` (Div): Container for application form
  - `applicant-name` (Input): Input field for applicant name
  - `applicant-email` (Input): Input field for applicant email
  - `resume-upload` (File Input): Input for resume file upload
  - `cover-letter` (Textarea): Textarea for cover letter
  - `submit-application-button` (Button): Submit application form
- Context Variables:
  - `job`: Dict with keys `job_id` (int), `title` (str), `company_name` (str)
  - Optionally `success_msg` (str) or `error_msg` (str) for form submission feedback
- Navigation Mappings:
  - Form POSTs to `url_for('application_form', job_id=job.job_id)`

### 5. applications.html
- Page Title: "My Applications"
- Element IDs:
  - `tracking-page` (Div): Container for application tracking page
  - `applications-table` (Table): Displays applications
  - `status-filter` (Dropdown): Filter applications by status
  - `view-application-button-{{ application.application_id }}` (Button, dynamic): View application details
  - `back-to-dashboard` (Button): Navigate back to dashboard
- Context Variables:
  - `applications`: List of dicts each with keys `application_id` (int), `job_title` (str), `company_name` (str), `status` (str), `applied_date` (str)
- Navigation Mappings:
  - Each `view-application-button-{{ application.application_id }}` navigates to `url_for('application_details', app_id=application.application_id)`
  - `back-to-dashboard`: `url_for('dashboard')`

### 6. companies.html
- Page Title: "Company Directory"
- Element IDs:
  - `companies-page` (Div): Container for companies directory
  - `companies-list` (Div): List of company cards
  - `search-company-input` (Input): Search input for companies
  - `view-company-button-{{ company.company_id }}` (Button, dynamic): View company profile
  - `back-to-dashboard` (Button): Navigate back to dashboard
- Context Variables:
  - `companies`: List of dicts each with keys `company_id` (int), `company_name` (str), `industry` (str), `employee_count` (int)
- Navigation Mappings:
  - Each `view-company-button-{{ company.company_id }}` navigates to `url_for('company_profile', company_id=company.company_id)`
  - `back-to-dashboard`: `url_for('dashboard')`

### 7. company_profile.html
- Page Title: "Company Profile"
- Element IDs:
  - `company-profile-page` (Div): Container for company profile
  - `company-info` (Div): Displays company name, industry, location, description
  - `company-jobs` (Div): Displays all open jobs from company
  - `jobs-list` (Div): List of jobs
  - `view-job-button-{{ job.job_id }}` (Button, dynamic): View job details
  - `back-to-companies` (Button): Navigate back to companies directory
- Context Variables:
  - `company`: Dict with keys `company_id` (int), `company_name` (str), `industry` (str), `location` (str), `description` (str), `employee_count` (int)
  - `company_jobs`: List of dicts each with keys `job_id` (int), `title` (str), `status` (str)
- Navigation Mappings:
  - Each `view-job-button-{{ job.job_id }}` navigates to `url_for('job_details', job_id=job.job_id)`
  - `back-to-companies`: `url_for('companies_directory')`

### 8. resumes.html
- Page Title: "My Resumes"
- Element IDs:
  - `resume-page` (Div): Container for resume management
  - `resumes-list` (Div): List of uploaded resumes
  - `upload-resume-button` (Button): Button to upload new resume
  - `resume-file-input` (File Input): Hidden file input for uploading resume
  - `delete-resume-button-{{ resume.resume_id }}` (Button, dynamic): Delete resume
  - `back-to-dashboard` (Button): Navigate back to dashboard
- Context Variables:
  - `resumes`: List of dicts each with keys `resume_id` (int), `filename` (str), `upload_date` (str), `summary` (str)
- Navigation Mappings:
  - `upload-resume-button`: triggers click on hidden `resume-file-input`
  - Each `delete-resume-button-{{ resume.resume_id }}` posts to `url_for('delete_resume', resume_id=resume.resume_id)`
  - `back-to-dashboard`: `url_for('dashboard')`

### 9. search_results.html
- Page Title: "Search Results"
- Element IDs:
  - `search-results-page` (Div): Container for search results
  - `search-query-display` (Div): Displays search query
  - `results-tabs` (Div): Tabs to switch between jobs and companies results
  - `job-results` (Div): Displays job results
  - `company-results` (Div): Displays company results
  - `no-results-message` (Div): Message when no results found
- Context Variables:
  - `query_str`: str - The search query
  - `job_results`: List of dicts with keys `job_id` (int), `title` (str), `company_name` (str), `location` (str)
  - `company_results`: List of dicts with keys `company_id` (int), `company_name` (str), `industry` (str)
- Navigation Mappings:
  - Job entries link to job details page: `url_for('job_details', job_id=job.job_id)`
  - Company entries link to company profile page: `url_for('company_profile', company_id=company.company_id)`

---

## Section 3: Data File Schemas

Data files are stored in the `data/` directory, pipe-delimited, with NO header line.

### 1. jobs.txt
- File Path: `data/jobs.txt`
- Fields (pipe `|` delimited):
  - job_id (int): Unique ID of the job
  - title (str): Job title
  - company_id (int): The ID of the company offering the job
  - location (str): Location string, e.g. "Remote", "New York, NY"
  - salary_min (int): Minimum salary
  - salary_max (int): Maximum salary
  - category (str): Category string, e.g. "Technology"
  - description (str): Full job description
  - posted_date (str): Date the job was posted, format YYYY-MM-DD
- Description: Stores all job postings
- Example rows:
```
1|Senior Python Developer|1|Remote|80000|120000|Technology|Experienced Python developer for web applications|2025-01-15
2|Data Analyst|2|New York, NY|60000|85000|Finance|Analyze financial data and create reports|2025-01-16
3|Healthcare Administrator|3|Los Angeles, CA|50000|70000|Healthcare|Manage hospital operations and patient records|2025-01-14
```

### 2. companies.txt
- File Path: `data/companies.txt`
- Fields (pipe `|` delimited):
  - company_id (int): Unique company ID
  - company_name (str): Name of the company
  - industry (str): Industry, e.g. "Technology"
  - location (str): Company headquarters or main location
  - employee_count (int): Number of employees
  - description (str): Company description
- Description: Stores company profiles
- Example rows:
```
1|TechCorp|Technology|San Francisco, CA|500|Leading software solutions provider
2|FinanceHub|Finance|New York, NY|300|Innovative financial services company
3|MediCare|Healthcare|Los Angeles, CA|200|Premier healthcare management organization
```

### 3. categories.txt
- File Path: `data/categories.txt`
- Fields (pipe `|` delimited):
  - category_id (int): Unique category ID
  - category_name (str): Name of the category
  - description (str): Description of category
- Description: Stores job categories
- Example rows:
```
1|Technology|Software, IT, and tech-related positions
2|Finance|Banking, accounting, and finance positions
3|Healthcare|Medical and healthcare industry positions
```

### 4. applications.txt
- File Path: `data/applications.txt`
- Fields (pipe `|` delimited):
  - application_id (int): Unique ID for application
  - job_id (int): ID of applied job
  - applicant_name (str): Applicant's full name
  - applicant_email (str): Applicant's email address
  - status (str): Application status (All, Applied, Under Review, Interview, Rejected)
  - applied_date (str): Date of application submission, format YYYY-MM-DD
  - resume_id (int): ID referencing a resume
- Description: Stores job application submissions
- Example rows:
```
1|1|John Doe|john@email.com|Under Review|2025-01-17|1
2|2|Jane Smith|jane@email.com|Applied|2025-01-16|2
3|3|Robert Johnson|robert@email.com|Interview|2025-01-15|3
```

### 5. resumes.txt
- File Path: `data/resumes.txt`
- Fields (pipe `|` delimited):
  - resume_id (int): Unique resume ID
  - applicant_name (str): Applicant name
  - applicant_email (str): Applicant email
  - filename (str): Filename of uploaded resume document
  - upload_date (str): Date of upload, format YYYY-MM-DD
  - summary (str): Short summary or note about the resume
- Description: Stores uploaded resumes
- Example rows:
```
1|John Doe|john@email.com|john_resume.pdf|2025-01-17|Senior developer with 8 years experience
2|Jane Smith|jane@email.com|jane_resume.pdf|2025-01-16|Data analyst with financial background
3|Robert Johnson|robert@email.com|robert_resume.pdf|2025-01-15|Healthcare administrator with 5 years experience
```

### 6. job_categories.txt
- File Path: `data/job_categories.txt`
- Fields (pipe `|` delimited):
  - mapping_id (int): Unique mapping ID
  - job_id (int): Job ID
  - category_id (int): Category ID
- Description: Stores many-to-many mapping of jobs to categories
- Example rows:
```
1|1|1
2|2|2
3|3|3
```
