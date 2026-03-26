# JobBoard Application Design Specification

---

## Section 1: Flask Routes Specification

| Route Path              | Function Name              | HTTP Methods | Template Rendered       | Context Variables (name: type)                              | POST Form Inputs (if applicable)                                                     |
|-------------------------|----------------------------|--------------|------------------------|-------------------------------------------------------------|--------------------------------------------------------------------------------------|
| /                       | root_redirect               | GET          | Redirect to /dashboard | None                                                        | None                                                                                 |
| /dashboard              | dashboard_page             | GET          | dashboard.html          | featured_jobs: list of dicts (job_id: int, title: str, company_name: str, location: str, salary_range: str), latest_jobs: list of dicts (same fields), categories: list of str, locations: list of str | None                                                                                 |
| /jobs                   | job_listings_page          | GET          | job_listings.html       | jobs: list of dicts (job_id: int, title: str, company_name: str, location: str, salary_min: int, salary_max: int, category: str), categories: list of str, locations: list of str, selected_category: str or None, selected_location: str or None, search_query: str or None | None                                                                                 |
| /job/<int:job_id>       | job_details_page           | GET          | job_details.html        | job: dict (job_id: int, title: str, company_name: str, location: str, salary_min: int, salary_max: int, category: str, description: str, posted_date: str), company: dict (company_id: int, company_name: str, industry: str, location: str, employee_count: int, description: str) | None                                                                                 |
| /apply/<int:job_id>     | application_form_page      | GET, POST    | application_form.html   | job: dict (job_id: int, title: str, company_name: str), form_errors: dict or None | applicant_name: str (input), applicant_email: str (input), resume_file: file (upload), cover_letter: str (textarea) |
| /applications           | applications_tracking_page | GET          | applications.html       | applications: list of dicts (application_id: int, job_title: str, company_name: str, status: str, applied_date: str), status_filter: str or None | None                                                                                 |
| /application/<int:app_id>| application_details_page  | GET          | application_details.html | application: dict (application_id: int, job_title: str, company_name: str, applicant_name: str, applicant_email: str, status: str, applied_date: str, resume_filename: str, cover_letter: str) | None                                                                                 |
| /companies              | companies_directory_page   | GET          | companies.html          | companies: list of dicts (company_id: int, company_name: str, industry: str, employee_count: int) , search_query: str or None  | None                                                                                 |
| /company/<int:company_id>| company_profile_page      | GET          | company_profile.html    | company: dict (company_id: int, company_name: str, industry: str, location: str, employee_count: int, description: str), jobs: list of dicts (job_id: int, title: str, status: str) | None                                                                                 |
| /resumes                | resume_management_page     | GET, POST    | resumes.html            | resumes: list of dicts (resume_id: int, filename: str, upload_date: str, summary: str) | resume_file: file (upload), applicant_name: str (input), applicant_email: str (input)  |
| /delete_resume/<int:resume_id> | delete_resume        | POST         | Redirect (no direct template) | None                                                    | None (resume_id in URL path)                                                        |
| /search                 | search_results_page        | GET          | search_results.html     | query: str, job_results: list of dicts (job_id: int, title: str, company_name: str, location: str), company_results: list of dicts (company_id: int, company_name: str, industry: str) | None                                                                                 |

---

## Section 2: HTML Template Specifications

### 1. Dashboard Page
- **Template Filename**: templates/dashboard.html
- **Page Title**: Job Board Dashboard
- **<title> and <h1> Content**: "Job Board Dashboard"
- **Element IDs**:
  - dashboard-page (Div): Container for the dashboard page.
  - featured-jobs (Div): Display of featured job recommendations.
  - browse-jobs-button (Button): Button to navigate to job listings page.
    - Navigation: url_for('job_listings_page')
  - my-applications-button (Button): Button to navigate to applications tracking page.
    - Navigation: url_for('applications_tracking_page')
  - companies-button (Button): Button to navigate to companies directory page.
    - Navigation: url_for('companies_directory_page')
- **Context Variables Available**:
  - featured_jobs: list of dicts with fields:
    - job_id: int
    - title: str
    - company_name: str
    - location: str
    - salary_range: str (e.g., "$80,000 - $120,000")
  - latest_jobs: list of dicts with same fields as featured_jobs
- **Navigation Mappings**:
  - browse-jobs-button: url_for('job_listings_page')
  - my-applications-button: url_for('applications_tracking_page')
  - companies-button: url_for('companies_directory_page')


### 2. Job Listings Page
- **Template Filename**: templates/job_listings.html
- **Page Title**: Job Listings
- **<title> and <h1> Content**: "Job Listings"
- **Element IDs**:
  - listings-page (Div): Container for the listings page.
  - search-input (Input): Field to search jobs by title, company, or location.
  - category-filter (Dropdown): Dropdown to filter by job category.
  - location-filter (Dropdown): Dropdown to filter by location.
  - jobs-grid (Div): Grid displaying job cards.
  - view-job-button-{{ job.job_id }} (Button): Button to view details of each job.
    - Navigation: url_for('job_details_page', job_id=job.job_id)
- **Context Variables Available**:
  - jobs: list of dicts with fields:
    - job_id: int
    - title: str
    - company_name: str
    - location: str
    - salary_min: int
    - salary_max: int
    - category: str
  - categories: list of str
  - locations: list of str
  - selected_category: str or None
  - selected_location: str or None
  - search_query: str or None
- **Navigation Mappings**:
  - view-job-button-{{ job.job_id }}: url_for('job_details_page', job_id=job.job_id)


### 3. Job Details Page
- **Template Filename**: templates/job_details.html
- **Page Title**: Job Details
- **<title> and <h1> Content**: "Job Details"
- **Element IDs**:
  - job-details-page (Div): Container for the job details page.
  - job-title (H1): Displays job title.
  - company-name (Div): Displays company name.
  - job-description (Div): Displays full job description and requirements.
  - salary-range (Div): Displays salary range.
  - apply-now-button (Button): Button to apply for the job.
    - Navigation: url_for('application_form_page', job_id=job.job_id)
- **Context Variables Available**:
  - job: dict with fields:
    - job_id: int
    - title: str
    - company_name: str
    - location: str
    - salary_min: int
    - salary_max: int
    - category: str
    - description: str
    - posted_date: str (YYYY-MM-DD)
  - company: dict with fields:
    - company_id: int
    - company_name: str
    - industry: str
    - location: str
    - employee_count: int
    - description: str
- **Navigation Mappings**:
  - apply-now-button: url_for('application_form_page', job_id=job.job_id)


### 4. Application Form Page
- **Template Filename**: templates/application_form.html
- **Page Title**: Submit Application
- **<title> and <h1> Content**: "Submit Application"
- **Element IDs**:
  - application-form-page (Div): Container for the application form page.
  - applicant-name (Input): Input for applicant name.
  - applicant-email (Input): Input for applicant email.
  - resume-upload (File Input): File input for resume upload.
  - cover-letter (Textarea): Textarea for cover letter.
  - submit-application-button (Button): Button to submit application.
- **Context Variables Available**:
  - job: dict with fields:
    - job_id: int
    - title: str
    - company_name: str
  - form_errors: dict (field_name: str -> error_message: str) or None
- **Navigation Mappings**:
  - submit-application-button: Submits form to POST /apply/{{ job.job_id }}

- **POST Form Inputs**:
  - applicant_name (text input)
  - applicant_email (text input)
  - resume_file (file upload)
  - cover_letter (textarea)


### 5. Application Tracking Page
- **Template Filename**: templates/applications.html
- **Page Title**: My Applications
- **<title> and <h1> Content**: "My Applications"
- **Element IDs**:
  - tracking-page (Div): Container for the tracking page.
  - applications-table (Table): Displays applications.
  - status-filter (Dropdown): Dropdown to filter by application status.
  - view-application-button-{{ application.application_id }} (Button): Button to view each application details.
    - Navigation: url_for('application_details_page', app_id=application.application_id)
  - back-to-dashboard (Button): Button to navigate back to dashboard.
    - Navigation: url_for('dashboard_page')
- **Context Variables Available**:
  - applications: list of dicts with fields:
    - application_id: int
    - job_title: str
    - company_name: str
    - status: str
    - applied_date: str (YYYY-MM-DD)
  - status_filter: str or None
- **Navigation Mappings**:
  - view-application-button-{{ application.application_id }}: url_for('application_details_page', app_id=application.application_id)
  - back-to-dashboard: url_for('dashboard_page')


### 6. Companies Directory Page
- **Template Filename**: templates/companies.html
- **Page Title**: Company Directory
- **<title> and <h1> Content**: "Company Directory"
- **Element IDs**:
  - companies-page (Div): Container for the companies page.
  - companies-list (Div): List of company cards.
  - search-company-input (Input): Input to search companies by name or industry.
  - view-company-button-{{ company.company_id }} (Button): Button to view company profile.
    - Navigation: url_for('company_profile_page', company_id=company.company_id)
  - back-to-dashboard (Button): Button to navigate back to dashboard.
    - Navigation: url_for('dashboard_page')
- **Context Variables Available**:
  - companies: list of dicts with fields:
    - company_id: int
    - company_name: str
    - industry: str
    - employee_count: int
  - search_query: str or None
- **Navigation Mappings**:
  - view-company-button-{{ company.company_id }}: url_for('company_profile_page', company_id=company.company_id)
  - back-to-dashboard: url_for('dashboard_page')


### 7. Company Profile Page
- **Template Filename**: templates/company_profile.html
- **Page Title**: Company Profile
- **<title> and <h1> Content**: "Company Profile"
- **Element IDs**:
  - company-profile-page (Div): Container for the company profile page.
  - company-info (Div): Displays company name, industry, location, and description.
  - company-jobs (Div): Displays all open jobs for the company.
  - jobs-list (Div): List of job cards.
  - view-job-button-{{ job.job_id }} (Button): Button to view job details.
    - Navigation: url_for('job_details_page', job_id=job.job_id)
  - back-to-companies (Button): Button to go back to companies directory.
    - Navigation: url_for('companies_directory_page')
- **Context Variables Available**:
  - company: dict with fields:
    - company_id: int
    - company_name: str
    - industry: str
    - location: str
    - employee_count: int
    - description: str
  - jobs: list of dicts with fields:
    - job_id: int
    - title: str
    - status: str
- **Navigation Mappings**:
  - view-job-button-{{ job.job_id }}: url_for('job_details_page', job_id=job.job_id)
  - back-to-companies: url_for('companies_directory_page')


### 8. Resume Management Page
- **Template Filename**: templates/resumes.html
- **Page Title**: My Resumes
- **<title> and <h1> Content**: "My Resumes"
- **Element IDs**:
  - resume-page (Div): Container for the resume page.
  - resumes-list (Div): List of uploaded resumes.
  - upload-resume-button (Button): Button to upload new resume.
  - resume-file-input (File Input): Hidden file input for resume upload.
  - delete-resume-button-{{ resume.resume_id }} (Button): Button to delete resume.
  - back-to-dashboard (Button): Button to navigate back to dashboard.
    - Navigation: url_for('dashboard_page')
- **Context Variables Available**:
  - resumes: list of dicts with fields:
    - resume_id: int
    - filename: str
    - upload_date: str (YYYY-MM-DD)
    - summary: str
- **Navigation Mappings**:
  - delete-resume-button-{{ resume.resume_id }}: Form POST action to /delete_resume/{{ resume.resume_id }}
  - back-to-dashboard: url_for('dashboard_page')
- **POST Form Inputs (Resume Upload)**:
  - resume_file (file upload)
  - applicant_name (text input)
  - applicant_email (text input)


### 9. Search Results Page
- **Template Filename**: templates/search_results.html
- **Page Title**: Search Results
- **<title> and <h1> Content**: "Search Results"
- **Element IDs**:
  - search-results-page (Div): Container for the search results page.
  - search-query-display (Div): Displays the search query.
  - results-tabs (Div): Tabs to switch between job and company results.
  - job-results (Div): Displays job search results.
  - company-results (Div): Displays company search results.
  - no-results-message (Div): Displays when no results found.
- **Context Variables Available**:
  - query: str
  - job_results: list of dicts with fields:
    - job_id: int
    - title: str
    - company_name: str
    - location: str
  - company_results: list of dicts with fields:
    - company_id: int
    - company_name: str
    - industry: str
- **Navigation Mappings**:
  - Buttons or links within job_results and company_results should navigate to:
    - job details: url_for('job_details_page', job_id=job.job_id)
    - company profile: url_for('company_profile_page', company_id=company.company_id)


---

## Section 3: Data File Schemas

### 1. Jobs Data
- **File Path**: data/jobs.txt
- **Field Order & Names** (pipe-delimited):
  job_id|title|company_id|location|salary_min|salary_max|category|description|posted_date
- **Description**: Stores job postings with identification, location, salary, category, descriptive information, and posting date.
- **Example Data**:
  ```
  1|Senior Python Developer|1|Remote|80000|120000|Technology|Experienced Python developer for web applications|2025-01-15
  2|Data Analyst|2|New York, NY|60000|85000|Finance|Analyze financial data and create reports|2025-01-16
  3|Healthcare Administrator|3|Los Angeles, CA|50000|70000|Healthcare|Manage hospital operations and patient records|2025-01-14
  ```

### 2. Companies Data
- **File Path**: data/companies.txt
- **Field Order & Names** (pipe-delimited):
  company_id|company_name|industry|location|employee_count|description
- **Description**: Stores company profiles including name, industry, location, number of employees, and descriptive text.
- **Example Data**:
  ```
  1|TechCorp|Technology|San Francisco, CA|500|Leading software solutions provider
  2|FinanceHub|Finance|New York, NY|300|Innovative financial services company
  3|MediCare|Healthcare|Los Angeles, CA|200|Premier healthcare management organization
  ```

### 3. Categories Data
- **File Path**: data/categories.txt
- **Field Order & Names** (pipe-delimited):
  category_id|category_name|description
- **Description**: Stores job category definitions with IDs and descriptive text.
- **Example Data**:
  ```
  1|Technology|Software, IT, and tech-related positions
  2|Finance|Banking, accounting, and finance positions
  3|Healthcare|Medical and healthcare industry positions
  ```

### 4. Applications Data
- **File Path**: data/applications.txt
- **Field Order & Names** (pipe-delimited):
  application_id|job_id|applicant_name|applicant_email|status|applied_date|resume_id
- **Description**: Stores job applications submitted by users, tracking applicant info, job applied, status, and linked resume.
- **Example Data**:
  ```
  1|1|John Doe|john@email.com|Under Review|2025-01-17|1
  2|2|Jane Smith|jane@email.com|Applied|2025-01-16|2
  3|3|Robert Johnson|robert@email.com|Interview|2025-01-15|3
  ```

### 5. Resumes Data
- **File Path**: data/resumes.txt
- **Field Order & Names** (pipe-delimited):
  resume_id|applicant_name|applicant_email|filename|upload_date|summary
- **Description**: Stores uploaded resumes file metadata and summary details per applicant.
- **Example Data**:
  ```
  1|John Doe|john@email.com|john_resume.pdf|2025-01-17|Senior developer with 8 years experience
  2|Jane Smith|jane@email.com|jane_resume.pdf|2025-01-16|Data analyst with financial background
  3|Robert Johnson|robert@email.com|robert_resume.pdf|2025-01-15|Healthcare administrator with 5 years experience
  ```

### 6. Job Categories Mapping Data
- **File Path**: data/job_categories.txt
- **Field Order & Names** (pipe-delimited):
  mapping_id|job_id|category_id
- **Description**: Maps job postings to job categories to allow filtering and classification.
- **Example Data**:
  ```
  1|1|1
  2|2|2
  3|3|3
  ```

---

End of design_spec.md
