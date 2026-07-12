# JobBoard Web Application Design Specification

---

# Section 1: Flask Routes Specification

| Route Path               | Function Name          | HTTP Method(s) | Template Rendered    | Context Variables Passed to Template                         | POST Input Expectations                           |
|--------------------------|------------------------|----------------|----------------------|--------------------------------------------------------------|--------------------------------------------------|
| `/`                      | root_redirect          | GET            | Redirects to `/dashboard` | None                                                         | N/A                                              |
| `/dashboard`             | dashboard              | GET            | dashboard.html       | featured_jobs: list of dict with keys: job_id(int), title(str), company_name(str), location(str), salary_min(int), salary_max(int) | None                                             |
| `/jobs`                  | job_listings           | GET            | job_listings.html    | jobs: list of dict with keys: job_id(int), title(str), company(str), location(str), salary_min(int), salary_max(int), category(str) | query parameters optional for filtering: 'search'(str), 'category'(str), 'location'(str) ignored in route but used in backend |
| `/job/<int:job_id>`      | job_details            | GET            | job_details.html     | job: dict with keys: job_id(int), title(str), company_name(str), location(str), salary_min(int), salary_max(int), category(str), description(str), posted_date(str) | None                                             |
| `/apply/<int:job_id>`    | application_form       | GET, POST      | application_form.html| job: dict with keys same as in job_details; form fields on POST: applicant_name(str), applicant_email(str), resume_file(file), cover_letter(str) | POST form fields: 'applicant_name', 'applicant_email', 'resume_upload'(file), 'cover_letter' |
| `/applications`          | application_tracking   | GET            | application_tracking.html | applications: list of dict with keys: application_id(int), job_title(str), company(str), status(str), applied_date(str) | query parameter optional for filtering: 'status' (str) |
| `/application/<int:application_id>` | application_detail | GET            | application_detail.html | application: dict with keys: application_id(int), job_title(str), company(str), status(str), applied_date(str), applicant_name(str), applicant_email(str), resume_filename(str), cover_letter(str)| None |
| `/companies`             | companies_directory    | GET            | companies.html       | companies: list of dict with keys: company_id(int), company_name(str), industry(str), employee_count(int) | query parameter optional for searching: 'search'(str) |
| `/company/<int:company_id>` | company_profile     | GET            | company_profile.html | company: dict with keys: company_id(int), company_name(str), industry(str), location(str), employee_count(int), description(str) jobs: list of dict with keys: job_id(int), title(str), status(str) | None |
| `/resumes`               | resume_management      | GET            | resumes.html         | resumes: list of dict with keys: resume_id(int), applicant_name(str), applicant_email(str), filename(str), upload_date(str), summary(str) | None                                             |
| `/upload_resume`          | upload_resume          | POST           | N/A (redirect)        | N/A                                                        | POST form field: 'resume_file'(file), 'applicant_name'(str), 'applicant_email'(str), 'summary'(str) |
| `/delete_resume/<int:resume_id>` | delete_resume     | POST           | N/A (redirect)        | N/A                                                        | N/A                                              |
| `/search`                | search_results         | GET            | search_results.html  | query(str), job_results: list of dict, company_results: list of dict (both match respective structures as above) | query parameter: 'query'                          |

---

# Section 2: HTML Template Specifications

1. **dashboard.html**
- Filename: `templates/dashboard.html`
- Page Title: "Job Board Dashboard"
- Element IDs:
  - `dashboard-page`: Div - container for the entire dashboard page.
  - `featured-jobs`: Div - displays featured job recommendations.
  - `browse-jobs-button`: Button - navigates to job listings page.
  - `my-applications-button`: Button - navigates to application tracking page.
  - `companies-button`: Button - navigates to companies directory page.
- Context Variables:
  - `featured_jobs`: list of dicts with keys: job_id(int), title(str), company_name(str), location(str), salary_min(int), salary_max(int)
- Navigation Mappings:
  - `browse-jobs-button`: onClick -> `url_for('job_listings')`
  - `my-applications-button`: onClick -> `url_for('application_tracking')`
  - `companies-button`: onClick -> `url_for('companies_directory')`

2. **job_listings.html**
- Filename: `templates/job_listings.html`
- Page Title: "Job Listings"
- Element IDs:
  - `listings-page`: Div - container
  - `search-input`: Input type text - to enter search keywords
  - `category-filter`: Dropdown select - filter jobs by category
  - `location-filter`: Dropdown select - filter jobs by location
  - `jobs-grid`: Div - grid of job cards
  - `view-job-button-{{ job.job_id }}`: Button per job card - view job details
- Context Variables:
  - `jobs`: list of dicts with keys: job_id(int), title(str), company(str), location(str), salary_min(int), salary_max(int), category(str)
- Navigation Mappings:
  - `view-job-button-{{ job.job_id }}`: onClick -> `url_for('job_details', job_id=job.job_id)`

3. **job_details.html**
- Filename: `templates/job_details.html`
- Page Title: "Job Details"
- Element IDs:
  - `job-details-page`: Div container
  - `job-title`: H1 with job title
  - `company-name`: Div with company name
  - `job-description`: Div with full job description and requirements
  - `salary-range`: Div with salary range
  - `apply-now-button`: Button to apply for the job
- Context Variables:
  - `job`: dict with keys: job_id(int), title(str), company_name(str), location(str), salary_min(int), salary_max(int), category(str), description(str), posted_date(str)
- Navigation Mappings:
  - `apply-now-button`: onClick -> `url_for('application_form', job_id=job.job_id)`

4. **application_form.html**
- Filename: `templates/application_form.html`
- Page Title: "Submit Application"
- Element IDs:
  - `application-form-page`: Div container
  - `applicant-name`: Input text for applicant's name
  - `applicant-email`: Input email for applicant's email
  - `resume-upload`: File input for resume upload
  - `cover-letter`: Textarea for cover letter
  - `submit-application-button`: Button to submit form
- Context Variables:
  - `job`: dict same as in job_details
- Navigation Mappings:
  - Form submits POST to current route

5. **application_tracking.html**
- Filename: `templates/application_tracking.html`
- Page Title: "My Applications"
- Element IDs:
  - `tracking-page`: Div container
  - `applications-table`: Table with columns: Job Title, Company, Status, Date Applied
  - `status-filter`: Dropdown select to filter by status
  - `view-application-button-{{ app.application_id }}`: Button per application row
  - `back-to-dashboard`: Button to go back to dashboard
- Context Variables:
  - `applications`: list of dicts with keys: application_id(int), job_title(str), company(str), status(str), applied_date(str)
- Navigation Mappings:
  - `view-application-button-{{ app.application_id }}`: onClick -> `url_for('application_detail', application_id=app.application_id)`
  - `back-to-dashboard`: onClick -> `url_for('dashboard')`

6. **companies.html**
- Filename: `templates/companies.html`
- Page Title: "Company Directory"
- Element IDs:
  - `companies-page`: Div container
  - `companies-list`: Div list of company cards
  - `search-company-input`: Input text for company searching
  - `view-company-button-{{ company.company_id }}`: Button per company
  - `back-to-dashboard`: Button to return to dashboard
- Context Variables:
  - `companies`: list of dicts with keys: company_id(int), company_name(str), industry(str), employee_count(int)
- Navigation Mappings:
  - `view-company-button-{{ company.company_id }}`: onClick -> `url_for('company_profile', company_id=company.company_id)`
  - `back-to-dashboard`: onClick -> `url_for('dashboard')`

7. **company_profile.html**
- Filename: `templates/company_profile.html`
- Page Title: "Company Profile"
- Element IDs:
  - `company-profile-page`: Div container
  - `company-info`: Div showing company details: name, industry, location, description
  - `company-jobs`: Div container for jobs list
  - `jobs-list`: Div listing jobs with title and status
  - `view-job-button-{{ job.job_id }}`: Button per job in profile
  - `back-to-companies`: Button to go back to companies directory
- Context Variables:
  - `company`: dict with keys: company_id(int), company_name(str), industry(str), location(str), employee_count(int), description(str)
  - `jobs`: list of dicts with keys: job_id(int), title(str), status(str)
- Navigation Mappings:
  - `view-job-button-{{ job.job_id }}`: onClick -> `url_for('job_details', job_id=job.job_id)`
  - `back-to-companies`: onClick -> `url_for('companies_directory')`

8. **resumes.html**
- Filename: `templates/resumes.html`
- Page Title: "My Resumes"
- Element IDs:
  - `resume-page`: Div container
  - `resumes-list`: Div list of resumes with upload dates
  - `upload-resume-button`: Button to initiate resume upload
  - `resume-file-input`: Hidden file input for file selection
  - `delete-resume-button-{{ resume.resume_id }}`: Button per resume
  - `back-to-dashboard`: Button to go back to dashboard
- Context Variables:
  - `resumes`: list of dicts with keys: resume_id(int), applicant_name(str), applicant_email(str), filename(str), upload_date(str), summary(str)
- Navigation Mappings:
  - `upload-resume-button`: triggers click on `resume-file-input` (frontend JavaScript required)
  - `delete-resume-button-{{ resume.resume_id }}`: form submission POST to `/delete_resume/<resume_id>`
  - `back-to-dashboard`: onClick -> `url_for('dashboard')`

9. **search_results.html**
- Filename: `templates/search_results.html`
- Page Title: "Search Results"
- Element IDs:
  - `search-results-page`: Div main container
  - `search-query-display`: Div displaying current search query
  - `results-tabs`: Div to switch between Jobs and Companies results
  - `job-results`: Div with job results
  - `company-results`: Div with company results
  - `no-results-message`: Div shown when no results found
- Context Variables:
  - `query`: str search query
  - `job_results`: list of dicts with keys matching job listing structure
  - `company_results`: list of dicts with keys matching company listing structure
- Navigation Mappings:
  - Each job or company result links to the detail page via `url_for('job_details', job_id=job.job_id)` or `url_for('company_profile', company_id=company.company_id)` respectively.

---

# Section 3: Data File Schemas

Each data file is located in the `data/` directory. Files have NO header lines; parsing starts at the first line.

1. **jobs.txt**
- File path: `data/jobs.txt`
- Pipe-delimited fields in order:
  1. job_id (int): Unique job identifier
  2. title (str): Job title
  3. company_id (int): Identifier for company offering the job
  4. location (str): Job location description
  5. salary_min (int): Minimum salary offered
  6. salary_max (int): Maximum salary offered
  7. category (str): Job category
  8. description (str): Full job description and requirements
  9. posted_date (str - YYYY-MM-DD): Date job was posted
- Description: Stores all job postings with details associating jobs to companies.
- Example rows:
```
1|Senior Python Developer|1|Remote|80000|120000|Technology|Experienced Python developer for web applications|2025-01-15
2|Data Analyst|2|New York, NY|60000|85000|Finance|Analyze financial data and create reports|2025-01-16
3|Healthcare Administrator|3|Los Angeles, CA|50000|70000|Healthcare|Manage hospital operations and patient records|2025-01-14
```

2. **companies.txt**
- File path: `data/companies.txt`
- Pipe-delimited fields in order:
  1. company_id (int): Unique company identifier
  2. company_name (str): Company name
  3. industry (str): Industry sector
  4. location (str): Company location
  5. employee_count (int): Number of employees
  6. description (str): Company profile description
- Description: Stores company profiles.
- Example rows:
```
1|TechCorp|Technology|San Francisco, CA|500|Leading software solutions provider
2|FinanceHub|Finance|New York, NY|300|Innovative financial services company
3|MediCare|Healthcare|Los Angeles, CA|200|Premier healthcare management organization
```

3. **categories.txt**
- File path: `data/categories.txt`
- Pipe-delimited fields in order:
  1. category_id (int): Unique category identifier
  2. category_name (str): Name of category
  3. description (str): Description of category contents
- Description: Stores job categories.
- Example rows:
```
1|Technology|Software, IT, and tech-related positions
2|Finance|Banking, accounting, and finance positions
3|Healthcare|Medical and healthcare industry positions
```

4. **applications.txt**
- File path: `data/applications.txt`
- Pipe-delimited fields in order:
  1. application_id (int): Unique application identifier
  2. job_id (int): Job applied to
  3. applicant_name (str): Name of applicant
  4. applicant_email (str): Email of applicant
  5. status (str): Application status (Applied, Under Review, Interview, Rejected, etc.)
  6. applied_date (str - YYYY-MM-DD): Date application was submitted
  7. resume_id (int): Resume file associated
- Description: Stores job application submissions.
- Example rows:
```
1|1|John Doe|john@email.com|Under Review|2025-01-17|1
2|2|Jane Smith|jane@email.com|Applied|2025-01-16|2
3|3|Robert Johnson|robert@email.com|Interview|2025-01-15|3
```

5. **resumes.txt**
- File path: `data/resumes.txt`
- Pipe-delimited fields in order:
  1. resume_id (int): Unique resume identifier
  2. applicant_name (str): Name of resume owner
  3. applicant_email (str): Email of owner
  4. filename (str): Filename of uploaded resume
  5. upload_date (str - YYYY-MM-DD): Date of upload
  6. summary (str): Brief resume summary
- Description: Stores uploaded resumes metadata.
- Example rows:
```
1|John Doe|john@email.com|john_resume.pdf|2025-01-17|Senior developer with 8 years experience
2|Jane Smith|jane@email.com|jane_resume.pdf|2025-01-16|Data analyst with financial background
3|Robert Johnson|robert@email.com|robert_resume.pdf|2025-01-15|Healthcare administrator with 5 years experience
```

6. **job_categories.txt**
- File path: `data/job_categories.txt`
- Pipe-delimited fields in order:
  1. mapping_id (int): Unique mapping identifier
  2. job_id (int): Job identifier
  3. category_id (int): Category identifier linked to the job
- Description: Maps job postings to categories.
- Example rows:
```
1|1|1
2|2|2
3|3|3
```

---

This design specification document provides detailed, explicit instructions for backend developers to implement the Flask routes with their exact function names, expected HTTP methods, templates, and data passed to templates. It also details frontend developers' expected template structure, element IDs, variables, and navigation handling. The data file schemas define exactly how to parse and structure stored data.

This specification thus enables independent and parallel development of backend and frontend components for the JobBoard application.

