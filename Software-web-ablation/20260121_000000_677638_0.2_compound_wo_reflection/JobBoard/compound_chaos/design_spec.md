# Design Specifications for JobBoard Web Application using Flask

---

## Section 1: Flask Application Routes and Function Specifications

The JobBoard web application will consist of multiple routes handling different functionalities. Each route uses Flask HTTP methods, renders HTML templates, and passes context variables required for template rendering and navigation.

---

### Route: `/` (Dashboard)
- **Function**: `dashboard()`
- **HTTP Methods**: `GET`
- **Template Rendered**: `dashboard.html`
- **Context Variables**:
  - `page_id`: "dashboard-page"
  - Navigation IDs: `jobs_button_id` = "jobs-button", `applications_button_id` = "applications-button", `companies_button_id` = "companies-button"  

---

### Route: `/jobs` (Job Listings)
- **Function**: `jobs()`
- **HTTP Methods**: `GET`, `POST` (For search/filter form)
- **Template Rendered**: `jobs.html`
- **Context Variables**:
  - `search_input_id`: "search-input"
  - `filter_type_dropdown_id`: "filter-type-dropdown"
  - `filter_location_dropdown_id`: "filter-location-dropdown"
  - `job_cards`: list of job dicts (each with keys `job_id`, `title`, `company`, `salary_range`)
  - For each job card, the apply button's ID format: `view-job-button-{job_id}`

---

### Route: `/job/<int:job_id>` (Job Detail Page)
- **Function**: `job_detail(job_id)`
- **HTTP Methods**: `GET`
- **Template Rendered**: `job_detail.html`
- **Context Variables**:
  - `job_title_id`: "job-title"
  - `company_name_id`: "company-name"
  - `description_id`: "job-description"
  - `requirements_id`: "job-requirements"
  - `salary_range_id`: "salary-range"
  - `apply_button_id`: "apply-job-button"

---

### Route: `/apply/<int:job_id>` (Submit Application)
- **Function**: `submit_application(job_id)`
- **HTTP Methods**: `GET`, `POST` (Form submission)
- **Template Rendered**: `application_form.html` (on GET and on POST error)
- **Context Variables**:
  - `form_container_id`: "application-form-container"
  - `applicant_name_id`: "applicant-name"
  - `applicant_email_id`: "applicant-email"
  - `resume_upload_id`: "resume-upload"
  - `cover_letter_id`: "cover-letter"
  - `submit_button_id`: "submit-application-button"

- **Form Fields (POST)**:
  - Clear input fields on successful POST

---

### Route: `/applications` (My Applications Page)
- **Function**: `my_applications()`
- **HTTP Methods**: `GET`
- **Template Rendered**: `applications.html`
- **Context Variables**:
  - `applications_table_id`: "applications-table"
  - `status_filter_dropdown_id`: "status-filter-dropdown"
  - Application view button IDs format: `view-application-button-{app_id}`
  - `back_button_id`: "back-to-dashboard"

---

### Route: `/directory` (Company Directory Page)
- **Function**: `company_directory()`
- **HTTP Methods**: `GET`, `POST` (search companies)
- **Template Rendered**: `directory.html`
- **Context Variables**:
  - `companies_list_id`: "companies-list"
  - `search_company_input_id`: "search-company-input"
  - Company view button IDs format: `view-company-button-{company_id}`
  - `back_to_dashboard_id`: "back-to-dashboard"

---

### Route: `/company/<int:company_id>` (Company Profile Page)
- **Function**: `company_profile(company_id)`
- **HTTP Methods**: `GET`
- **Template Rendered**: `company_profile.html`
- **Context Variables**:
  - `company_profile_container_id`: "company-profile-container"
  - `location_id`: "company-location"
  - `industry_id`: "company-industry"
  - `company_jobs_id`: "company-jobs"
  - `job_list_id`: "company-job-list"
  - Job view button IDs format: `view-job-from-company-{job_id}`
  - `back_to_companies_id`: "back-to-companies"

---

### Route: `/management` (Resume Management Page)
- **Function**: `management()`
- **HTTP Methods**: `GET`, `POST` (for uploading/deleting resumes)
- **Template Rendered**: `management.html`
- **Context Variables**:
  - `resume_page_id`: "resume-page"
  - `resumes_list_id`: "resumes-list"
  - `upload_resume_button_id`: "upload-resume-button"
  - `hidden_resume_input_id`: "hidden-resume-input"
  - Delete button IDs format: `delete-resume-button-{resume_id}`
  - `back_to_dashboard_id`: "back-to-dashboard"

---

### Route: `/search` (Search Results Page)
- **Function**: `search_results()`
- **HTTP Methods**: `GET` (taking search query params)
- **Template Rendered**: `search_results.html`
- **Context Variables**:
  - `search_query_display_id`: "search-query-display"
  - `tabs_id`: "search-tabs"
  - `job_results_id`: "job-results"
  - `company_results_id`: "company-results"

---

## Section 2: HTML Template Specifications

Each page uses consistent element IDs and variable passing using Flask's `url_for` syntax for navigation and form actions.

### Dashboard (`dashboard.html`)
- **Title**: "Board Dashboard" (used in `<title>` and `<h1>`)
- **Page container ID**: `dashboard-page`
- Buttons IDs:
  - Jobs button: `jobs-button`
  - Applications button: `applications-button`
  - Companies button: `companies-button`
- Navigation example:
  - `<a href="{{ url_for('jobs') }}" id="jobs-button">Jobs</a>`

### Job Listings (`jobs.html`)
- **Title**: "Job Listings"
- **IDs**:
  - Search input: `search-input`
  - Filter dropdowns: `filter-type-dropdown`, `filter-location-dropdown`
  - Job cards container: `job-cards-container`
  - Each job card includes an apply button with ID: `view-job-button-{{ job.job_id }}`
- Search and filter form action example:
  - `<form method="POST" action="{{ url_for('jobs') }}">
      <input id="search-input" name="search_query" type="text" />
      <select id="filter-type-dropdown" name="filter_type">
        <option value="">All Types</option>
        <!-- More options -->
      </select>
      <select id="filter-location-dropdown" name="filter_location">
        <option value="">All Locations</option>
        <option value="Remote">Remote</option>
        <!-- More options -->
      </select>
      <button type="submit">Search</button>
    </form>`

### Job Detail (`job_detail.html`)
- **Title**: Job title dynamically set
- **IDs**:
  - `job-title`
  - `company-name`
  - `job-description`
  - `job-requirements`
  - `salary-range`
  - Apply button: `apply-job-button`
- Apply button links to: `url_for('submit_application', job_id=job.job_id)`

### Submit Application (`application_form.html`)
- **Title**: "Submit Application"
- **IDs**:
  - Form container: `application-form-container`
  - Input name: `applicant-name`
  - Input email: `applicant-email`
  - File upload: `resume-upload`
  - Textarea cover letter: `cover-letter`
  - Submit button: `submit-application-button`
- Form action example:
  - `<form method="POST" action="{{ url_for('submit_application', job_id=job.job_id) }}" enctype="multipart/form-data">`

### My Applications (`applications.html`)
- **Title**: "My Applications"
- **IDs**:
  - Applications table: `applications-table`
  - Status filter dropdown: `status-filter-dropdown`
  - View button per application: `view-application-button-{{ application.application_id }}`
  - Back button: `back-to-dashboard`

### Company Directory (`directory.html`)
- **Title**: "Company Directory"
- **IDs**:
  - Companies list container: `companies-list`
  - Search input: `search-company-input`
  - Company view button: `view-company-button-{{ company.company_id }}`
  - Back button: `back-to-dashboard`

### Company Profile (`company_profile.html`)
- **Title**: Company name dynamically set
- **IDs**:
  - Container: `company-profile-container`
  - Location: `company-location`
  - Industry: `company-industry`
  - Jobs container: `company-jobs`
  - Job list: `company-job-list`
  - View job button: `view-job-from-company-{{ job.job_id }}`
  - Back button: `back-to-companies`

### Management (`management.html`)
- **Title**: "Resume Management"
- **IDs**:
  - Page container: `resume-page`
  - Resumes list: `resumes-list`
  - Upload button: `upload-resume-button`
  - Hidden input: `hidden-resume-input`
  - Delete button: `delete-resume-button-{{ resume.resume_id }}`
  - Back button: `back-to-dashboard`

### Search Results (`search_results.html`)
- **Title**: "Search Results"
- **IDs**:
  - Search query display: `search-query-display`
  - Tabs container: `search-tabs`
  - Job results div: `job-results`
  - Company results div: `company-results`

---

## Section 3: Data Schemas and Sample Data

Files are stored under a local data directory and parsed using pipe-delimited fields. No empty lines allowed. Order and naming must match exactly.

---

### 1. `jobs.txt`
- **Schema** (pipe-delimited):
  - `job_id` (int)
  - `title` (string)
  - `company_id` (int)
  - `location` (string, e.g. "Remote", "NY", "CA")
  - `salary_min` (int)
  - `salary_max` (int)
  - `category` (string)
  - `description` (string)

- **Example rows**:
```
1|Python Developer|1|Remote|80000|120000|Technology|Experienced Python developer with 8 years...
2|Data Analyst|2|NY|60000|85000|Finance|Analyze financial data and reports
3|Healthcare Manager|3|CA|50000|70000|Healthcare|Manage patient care and hospital staff
```

---

### 2. `companies.txt`
- **Schema** (pipe-delimited):
  - `company_id` (int)
  - `name` (string)
  - `industry` (string)
  - `location` (string)
  - `employee_count` (int)
  - `description` (string)

- **Example rows**:
```
1|TechCorp|Technology|San Francisco, CA|500|Leading technology solutions provider
2|FinanceHub|Finance|New York, NY|300|New York financial services firm
3|MediCare|Healthcare|Los Angeles, CA|250|Healthcare organization
```

---

### 3. `job_categories.txt`
- **Schema** (pipe-delimited):
  - `category_id` (int)
  - `category_name` (string)
  - `description` (string)

- **Example rows**:
```
1|Technology|Technology related job roles
2|Finance|Banking and financial services
3|Healthcare|Healthcare and medical professionals
```

---

### 4. `applications.txt`
- **Schema** (pipe-delimited):
  - `application_id` (int)
  - `job_id` (int)
  - `applicant_name` (string)
  - `applicant_email` (string)
  - `status` (string) [e.g., Applied, Interview, Rejected]
  - `applied_date` (YYYY-MM-DD)
  - `resume_id` (int)

- **Example rows**:
```
1|1|John Johnson|john@example.com|Review|2025-01-17|1
2|2|Jane Smith|jane@example.com|Interview|2025-01-15|3
3|3|Robert Brown|robert@email.com|Applied|2025-01-10|2
```

---

### 5. `resumes.txt`
- **Schema** (pipe-delimited):
  - `resume_id` (int)
  - `applicant_name` (string)
  - `content` (string, multiline descriptions allowed)

- **Example rows**:
```
1|John Johnson|Experienced Python developer with 8 years background in software development.
2|Jane Smith|Financial analyst with 5 years in banking sector.
3|Robert Brown|Healthcare professional with expertise in patient management.
```

---

**Critical Success Criteria:**
- Flask app routes annotated with HTTP verbs, function names, templates, and EXACT context variable names.
- Clear input handling for POST routes to reset form inputs upon success.
- Precise element IDs for navigation and page components matching the specifications.
- URLs in templates use `url_for()` with example snippets.
- Pipe-delimited data schemas and example rows for all data files.
- Design spec fully enables backend developers to implement the Flask app and templates independently.
