# JobBoard Design Specification

---

## 1. Flask Routes Specification

| Route Path                      | Function Name          | HTTP Methods | Template Rendered       | Context Variables (Name : Type)                                                                                                   | POST Input Expectations (for POST routes)                                                                                     |
|--------------------------------|------------------------|--------------|------------------------|----------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------|
| /                              | root_redirect           | GET          | None (Redirect to /dashboard) | None                                                                                                                             | None                                                                                                                           |
| /dashboard                     | dashboard_view         | GET          | dashboard.html          | featured_jobs : list of dict, each dict with keys: job_id (int), title (str), company_name (str), location (str), salary_min (int), salary_max (int), category (str)               | None                                                                                                                           |
| /jobs                         | job_listings           | GET          | job_listings.html       | jobs : list of dict, each with job_id (int), title (str), company_name (str), location (str), salary_min (int), salary_max (int), category (str); categories : list of dict (category_id (int), category_name (str)); locations : list of str      | None                                                                                                                           |
| /job/<int:job_id>             | job_details            | GET          | job_details.html        | job : dict with job_id (int), title (str), company_name (str), location (str), salary_min (int), salary_max (int), category (str), description (str); company : dict with company_id (int), company_name (str)                                       | None                                                                                                                           |
| /apply/<int:job_id>            | application_form       | GET, POST    | application_form.html   | job : dict with job_id (int), title (str), company_name (str)                                                                      | applicant_name (str), applicant_email (str), resume_file (file upload), cover_letter (str)                                     |
| /applications                  | application_tracking   | GET          | application_tracking.html| applications : list of dict with application_id (int), job_title (str), company_name (str), status (str), applied_date (str)         | None                                                                                                                           |
| /company                      | companies_directory    | GET          | companies_directory.html| companies : list of dict with company_id (int), company_name (str), industry (str), employee_count (int)                            | None                                                                                                                           |
| /company/<int:company_id>      | company_profile        | GET          | company_profile.html    | company : dict with company_id (int), company_name (str), industry (str), location (str), description (str); jobs : list of dict with job_id (int), title (str), status (str)           | None                                                                                                                           |
| /resumes                      | resume_management      | GET, POST    | resume_management.html  | resumes : list of dict with resume_id (int), applicant_name (str), applicant_email (str), filename (str), upload_date (str), summary (str) | (POST) resume_file (file upload), applicant_name (str), applicant_email (str), summary (str)                                   |
| /resumes/delete/<int:resume_id>| delete_resume          | POST         | None (Redirect after deletion) | None                                                                                                                             | None (Resume ID from URL)                                                                                                     |
| /search                       | search_results         | GET          | search_results.html     | search_query : str, job_results : list of dict(job_id (int), title (str), company_name (str), location (str), salary_min (int), salary_max (int)), company_results : list of dict(company_id (int), company_name (str), industry (str)) | None                                                                                                                           |

---

## 2. HTML Template Specifications

### 1. Dashboard Page
- Filename: templates/dashboard.html
- Page Title: Job Board Dashboard
- Elements:
  - ID: dashboard-page (Div) - Container for the dashboard page
  - ID: featured-jobs (Div) - Display of featured job recommendations
  - ID: browse-jobs-button (Button) - Navigates to Job Listings Page
  - ID: my-applications-button (Button) - Navigates to Application Tracking Page
  - ID: companies-button (Button) - Navigates to Companies Directory Page
- Context Variables:
  - featured_jobs: List of dicts with keys:
    - job_id (int)
    - title (str)
    - company_name (str)
    - location (str)
    - salary_min (int)
    - salary_max (int)
    - category (str)
- Navigation Mappings:
  - browse-jobs-button: url_for('job_listings')
  - my-applications-button: url_for('application_tracking')
  - companies-button: url_for('companies_directory')

### 2. Job Listings Page
- Filename: templates/job_listings.html
- Page Title: Job Listings
- Elements:
  - ID: listings-page (Div) - Container for the listings page
  - ID: search-input (Input) - Search jobs by title, company, or location
  - ID: category-filter (Dropdown) - Filter jobs by category
  - ID: location-filter (Dropdown) - Filter jobs by location
  - ID: jobs-grid (Div) - Grid displaying job cards
  - ID: view-job-button-{{ job.job_id }} (Button) - Button to view job details for each job
- Context Variables:
  - jobs: List of dicts with keys:
    - job_id (int)
    - title (str)
    - company_name (str)
    - location (str)
    - salary_min (int)
    - salary_max (int)
    - category (str)
  - categories: List of dicts with keys:
    - category_id (int)
    - category_name (str)
  - locations: List of str
- Navigation Mappings:
  - view-job-button-{{ job.job_id }}: url_for('job_details', job_id=job.job_id)

### 3. Job Details Page
- Filename: templates/job_details.html
- Page Title: Job Details
- Elements:
  - ID: job-details-page (Div) - Container for the job details page
  - ID: job-title (H1) - Displays job title
  - ID: company-name (Div) - Displays company name
  - ID: job-description (Div) - Displays full job description and requirements
  - ID: salary-range (Div) - Displays salary range
  - ID: apply-now-button (Button) - Button to apply for the job
- Context Variables:
  - job: dict with keys:
    - job_id (int)
    - title (str)
    - company_name (str)
    - location (str)
    - salary_min (int)
    - salary_max (int)
    - category (str)
    - description (str)
  - company: dict with keys:
    - company_id (int)
    - company_name (str)
- Navigation Mappings:
  - apply-now-button: url_for('application_form', job_id=job.job_id)

### 4. Application Form Page
- Filename: templates/application_form.html
- Page Title: Submit Application
- Elements:
  - ID: application-form-page (Div) - Container for the application form
  - ID: applicant-name (Input) - Input for applicant name
  - ID: applicant-email (Input) - Input for applicant email
  - ID: resume-upload (File Input) - Upload resume file
  - ID: cover-letter (Textarea) - Input for cover letter
  - ID: submit-application-button (Button) - Submit application
- Context Variables:
  - job: dict with keys:
    - job_id (int)
    - title (str)
    - company_name (str)
- Navigation Mappings:
  - submit-application-button: form POST to url_for('application_form', job_id=job.job_id)

### 5. Application Tracking Page
- Filename: templates/application_tracking.html
- Page Title: My Applications
- Elements:
  - ID: tracking-page (Div) - Container for tracking page
  - ID: applications-table (Table) - Displays applications with columns: job title, company, status, date applied
  - ID: status-filter (Dropdown) - Filter applications by status
  - ID: view-application-button-{{ app.application_id }} (Button) - View application details per application
  - ID: back-to-dashboard (Button) - Navigate to dashboard
- Context Variables:
  - applications: List of dicts with keys:
    - application_id (int)
    - job_title (str)
    - company_name (str)
    - status (str)
    - applied_date (str)
- Navigation Mappings:
  - view-application-button-{{ app.application_id }}: (Optional, not specified in user task)
  - back-to-dashboard: url_for('dashboard_view')

### 6. Companies Directory Page
- Filename: templates/companies_directory.html
- Page Title: Company Directory
- Elements:
  - ID: companies-page (Div) - Container for companies page
  - ID: companies-list (Div) - List of company cards
  - ID: search-company-input (Input) - Search companies by name or industry
  - ID: view-company-button-{{ company.company_id }} (Button) - View company profile
  - ID: back-to-dashboard (Button) - Navigate to dashboard
- Context Variables:
  - companies: List of dicts with keys:
    - company_id (int)
    - company_name (str)
    - industry (str)
    - employee_count (int)
- Navigation Mappings:
  - view-company-button-{{ company.company_id }}: url_for('company_profile', company_id=company.company_id)
  - back-to-dashboard: url_for('dashboard_view')

### 7. Company Profile Page
- Filename: templates/company_profile.html
- Page Title: Company Profile
- Elements:
  - ID: company-profile-page (Div) - Container for company profile
  - ID: company-info (Div) - Displays company name, industry, location, description
  - ID: company-jobs (Div) - Displays all open jobs for company
  - ID: jobs-list (Div) - List of jobs with titles and status
  - ID: view-job-button-{{ job.job_id }} (Button) - View job details from company profile
  - ID: back-to-companies (Button) - Navigate to companies directory
- Context Variables:
  - company: dict with keys:
    - company_id (int)
    - company_name (str)
    - industry (str)
    - location (str)
    - description (str)
  - jobs: List of dicts with keys:
    - job_id (int)
    - title (str)
    - status (str)  # status if available, else could be inferred as 'Open'
- Navigation Mappings:
  - view-job-button-{{ job.job_id }}: url_for('job_details', job_id=job.job_id)
  - back-to-companies: url_for('companies_directory')

### 8. Resume Management Page
- Filename: templates/resume_management.html
- Page Title: My Resumes
- Elements:
  - ID: resume-page (Div) - Container for resume page
  - ID: resumes-list (Div) - List of uploaded resumes
  - ID: upload-resume-button (Button) - Upload a new resume
  - ID: resume-file-input (File Input) - Hidden file input for upload
  - ID: delete-resume-button-{{ resume.resume_id }} (Button) - Delete a resume
  - ID: back-to-dashboard (Button) - Navigate back to dashboard
- Context Variables:
  - resumes: List of dicts with keys:
    - resume_id (int)
    - applicant_name (str)
    - applicant_email (str)
    - filename (str)
    - upload_date (str)
    - summary (str)
- Navigation Mappings:
  - upload-resume-button: triggers click on hidden resume-file-input
  - delete-resume-button-{{ resume.resume_id }}: POST to url_for('delete_resume', resume_id=resume.resume_id)
  - back-to-dashboard: url_for('dashboard_view')

### 9. Search Results Page
- Filename: templates/search_results.html
- Page Title: Search Results
- Elements:
  - ID: search-results-page (Div) - Container for search results
  - ID: search-query-display (Div) - Displays the search query string
  - ID: results-tabs (Div) - Tabs to switch between job and company results
  - ID: job-results (Div) - Displays search results for jobs
  - ID: company-results (Div) - Displays search results for companies
  - ID: no-results-message (Div) - Displays when no search results
- Context Variables:
  - search_query: str
  - job_results: List of dicts with keys:
    - job_id (int)
    - title (str)
    - company_name (str)
    - location (str)
    - salary_min (int)
    - salary_max (int)
  - company_results: List of dicts with keys:
    - company_id (int)
    - company_name (str)
    - industry (str)
- Navigation Mappings:
  - job-results's view buttons (if any): url_for('job_details', job_id=job.job_id)
  - company-results's view buttons (if any): url_for('company_profile', company_id=company.company_id)

---

## 3. Data File Schemas

### 1. jobs.txt
- File Path: data/jobs.txt
- Fields (Pipe-Delimited):
  - job_id (int)
  - title (str)
  - company_id (int)
  - location (str)
  - salary_min (int)
  - salary_max (int)
  - category (str)
  - description (str)
  - posted_date (YYYY-MM-DD string)
- Data Description: Contains all job postings with relevant details including company association, location, salary range, category, and the posting date.
- Example Rows:
  ```
  1|Senior Python Developer|1|Remote|80000|120000|Technology|Experienced Python developer for web applications|2025-01-15
  2|Data Analyst|2|New York, NY|60000|85000|Finance|Analyze financial data and create reports|2025-01-16
  3|Healthcare Administrator|3|Los Angeles, CA|50000|70000|Healthcare|Manage hospital operations and patient records|2025-01-14
  ```

### 2. companies.txt
- File Path: data/companies.txt
- Fields (Pipe-Delimited):
  - company_id (int)
  - company_name (str)
  - industry (str)
  - location (str)
  - employee_count (int)
  - description (str)
- Data Description: Contains records of companies with identifying information and descriptions.
- Example Rows:
  ```
  1|TechCorp|Technology|San Francisco, CA|500|Leading software solutions provider
  2|FinanceHub|Finance|New York, NY|300|Innovative financial services company
  3|MediCare|Healthcare|Los Angeles, CA|200|Premier healthcare management organization
  ```

### 3. categories.txt
- File Path: data/categories.txt
- Fields (Pipe-Delimited):
  - category_id (int)
  - category_name (str)
  - description (str)
- Data Description: Defines job categories with description
- Example Rows:
  ```
  1|Technology|Software, IT, and tech-related positions
  2|Finance|Banking, accounting, and finance positions
  3|Healthcare|Medical and healthcare industry positions
  ```

### 4. applications.txt
- File Path: data/applications.txt
- Fields (Pipe-Delimited):
  - application_id (int)
  - job_id (int)
  - applicant_name (str)
  - applicant_email (str)
  - status (str) # e.g., Applied, Under Review, Interview, Rejected
  - applied_date (YYYY-MM-DD string)
  - resume_id (int)
- Data Description: Contains user's job applications with status and related resume
- Example Rows:
  ```
  1|1|John Doe|john@email.com|Under Review|2025-01-17|1
  2|2|Jane Smith|jane@email.com|Applied|2025-01-16|2
  3|3|Robert Johnson|robert@email.com|Interview|2025-01-15|3
  ```

### 5. resumes.txt
- File Path: data/resumes.txt
- Fields (Pipe-Delimited):
  - resume_id (int)
  - applicant_name (str)
  - applicant_email (str)
  - filename (str) # uploaded file name
  - upload_date (YYYY-MM-DD string)
  - summary (str) # short description or summary of resume
- Data Description: User uploaded resumes with metadata
- Example Rows:
  ```
  1|John Doe|john@email.com|john_resume.pdf|2025-01-17|Senior developer with 8 years experience
  2|Jane Smith|jane@email.com|jane_resume.pdf|2025-01-16|Data analyst with financial background
  3|Robert Johnson|robert@email.com|robert_resume.pdf|2025-01-15|Healthcare administrator with 5 years experience
  ```

### 6. job_categories.txt
- File Path: data/job_categories.txt
- Fields (Pipe-Delimited):
  - mapping_id (int)
  - job_id (int)
  - category_id (int)
- Data Description: Mapping of jobs to categories
- Example Rows:
  ```
  1|1|1
  2|2|2
  3|3|3
  ```

---

All files do not contain header lines, parsing commences from line 1.


---

End of Design Specification
