# JobBoard Application Design Specification

## Section 1: Page Layouts and Element IDs

### 1. Dashboard Page
- **Title**: Job Board Dashboard
- **Container**: Div with ID `dashboard-page`
- **Elements**:
  - Div `featured-jobs`: Displays featured job recommendations.
  - Button `browse-jobs-button`: Navigate to Job Listings page.
  - Button `my-applications-button`: Navigate to Application Tracking page.
  - Button `companies-button`: Navigate to Companies Directory page.

### 2. Job Listings Page
- **Title**: Job Listings
- **Container**: Div with ID `listings-page`
- **Elements**:
  - Input `search-input`: Search field for job title, company, or location.
  - Dropdown `category-filter`: Filter jobs by category.
  - Dropdown `location-filter`: Filter jobs by location.
  - Div `jobs-grid`: Displays cards for each job.
  - Buttons for each job card: ID pattern `view-job-button-{job_id}` to view job details.

### 3. Job Details Page
- **Title**: Job Details
- **Container**: Div with ID `job-details-page`
- **Elements**:
  - H1 `job-title`: Displays job title.
  - Div `company-name`: Displays company name.
  - Div `job-description`: Full job description and requirements.
  - Div `salary-range`: Displays salary range.
  - Button `apply-now-button`: Submit application for this job.

### 4. Application Form Page
- **Title**: Submit Application
- **Container**: Div with ID `application-form-page`
- **Elements**:
  - Input `applicant-name`: Applicant's name.
  - Input `applicant-email`: Applicant's email.
  - File Input `resume-upload`: Upload resume file.
  - Textarea `cover-letter`: Enter cover letter.
  - Button `submit-application-button`: Submit the application.

### 5. Application Tracking Page
- **Title**: My Applications
- **Container**: Div with ID `tracking-page`
- **Elements**:
  - Table `applications-table`: Displays applications with job title, company, status, date applied.
  - Dropdown `status-filter`: Filter applications by status.
  - Buttons for each application: ID pattern `view-application-button-{app_id}` to view details.
  - Button `back-to-dashboard`: Return to Dashboard.

### 6. Companies Directory Page
- **Title**: Company Directory
- **Container**: Div with ID `companies-page`
- **Elements**:
  - Div `companies-list`: List of companies with name, industry, employee count.
  - Input `search-company-input`: Search companies by name or industry.
  - Buttons for each company: ID pattern `view-company-button-{company_id}` to view profile.
  - Button `back-to-dashboard`: Return to Dashboard.

### 7. Company Profile Page
- **Title**: Company Profile
- **Container**: Div with ID `company-profile-page`
- **Elements**:
  - Div `company-info`: Displays company name, industry, location, description.
  - Div `company-jobs`: Shows all open jobs for the company.
  - Div `jobs-list`: List of jobs with titles, status indicators.
  - Buttons for each job: ID pattern `view-job-button-{job_id}` to view job details.
  - Button `back-to-companies`: Return to Companies Directory.

### 8. Resume Management Page
- **Title**: My Resumes
- **Container**: Div with ID `resume-page`
- **Elements**:
  - Div `resumes-list`: List of uploaded resumes with upload dates.
  - Button `upload-resume-button`: Initiate resume upload.
  - File Input `resume-file-input`: Hidden file input for uploading.
  - Buttons for each resume: ID pattern `delete-resume-button-{resume_id}` to delete.
  - Button `back-to-dashboard`: Return to Dashboard.

### 9. Search Results Page
- **Title**: Search Results
- **Container**: Div with ID `search-results-page`
- **Elements**:
  - Div `search-query-display`: Shows the search query.
  - Div `results-tabs`: Switch tabs between job and company results.
  - Div `job-results`: Display job search results.
  - Div `company-results`: Display company search results.
  - Div `no-results-message`: Display when no results found.

---

## Section 2: Navigation and Interaction Flow

- From **Dashboard Page**:
  - Button `browse-jobs-button` -> Job Listings Page
  - Button `my-applications-button` -> Application Tracking Page
  - Button `companies-button` -> Companies Directory Page

- From **Job Listings Page**:
  - Each job card `view-job-button-{job_id}` -> Job Details Page for that job

- From **Job Details Page**:
  - Button `apply-now-button` -> Application Form Page (job context preserved)

- From **Application Form Page**:
  - Button `submit-application-button` -> Submit application and redirect to Application Tracking Page

- From **Application Tracking Page**:
  - Each application `view-application-button-{app_id}` -> View application details (same Application Tracking Page or a modal)
  - Button `back-to-dashboard` -> Dashboard Page

- From **Companies Directory Page**:
  - Each company `view-company-button-{company_id}` -> Company Profile Page
  - Button `back-to-dashboard` -> Dashboard Page

- From **Company Profile Page**:
  - Each job `view-job-button-{job_id}` -> Job Details Page
  - Button `back-to-companies` -> Companies Directory Page

- From **Resume Management Page**:
  - Button `upload-resume-button` -> Trigger file input `resume-file-input`
  - Each resume `delete-resume-button-{resume_id}` -> Deletes the resume
  - Button `back-to-dashboard` -> Dashboard Page

- From **Search Results Page**:
  - Tabs in `results-tabs` switch displayed content between `job-results` and `company-results`

---

## Section 3: Data Storage Schemas

### 1. Jobs Data (`jobs.txt`)
- Format: `job_id|title|company_id|location|salary_min|salary_max|category|description|posted_date`
- Example:
  - `1|Senior Python Developer|1|Remote|80000|120000|Technology|Experienced Python developer for web applications|2025-01-15`

### 2. Companies Data (`companies.txt`)
- Format: `company_id|company_name|industry|location|employee_count|description`
- Example:
  - `1|TechCorp|Technology|San Francisco, CA|500|Leading software solutions provider`

### 3. Categories Data (`categories.txt`)
- Format: `category_id|category_name|description`
- Example:
  - `1|Technology|Software, IT, and tech-related positions`

### 4. Applications Data (`applications.txt`)
- Format: `application_id|job_id|applicant_name|applicant_email|status|applied_date|resume_id`
- Example:
  - `1|1|John Doe|john@email.com|Under Review|2025-01-17|1`

### 5. Resumes Data (`resumes.txt`)
- Format: `resume_id|applicant_name|applicant_email|filename|upload_date|summary`
- Example:
  - `1|John Doe|john@email.com|john_resume.pdf|2025-01-17|Senior developer with 8 years experience`

### 6. Job Categories Mapping Data (`job_categories.txt`)
- Format: `mapping_id|job_id|category_id`
- Example:
  - `1|1|1`

---

This design specification fully covers all pages, element IDs, navigation flows, and data storage formats as required.
