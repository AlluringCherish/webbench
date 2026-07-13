# JobBoard Application Design Specification

## Section 1: Page Layouts and Element IDs

### 1. Dashboard Page
- Page Title: "Job Board Dashboard"
- Container: Div (ID: `dashboard-page`)
- Elements:
  - Div (ID: `featured-jobs`): Shows featured job recommendations.
  - Button (ID: `browse-jobs-button`): Navigate to Job Listings Page.
  - Button (ID: `my-applications-button`): Navigate to Application Tracking Page.
  - Button (ID: `companies-button`): Navigate to Companies Directory Page.

### 2. Job Listings Page
- Page Title: "Job Listings"
- Container: Div (ID: `listings-page`)
- Elements:
  - Input (ID: `search-input`): Search jobs by title, company, or location.
  - Dropdown (ID: `category-filter`): Filter by job category.
  - Dropdown (ID: `location-filter`): Filter by job location (Remote, On-site, Hybrid).
  - Div (ID: `jobs-grid`): Grid containing job cards.
  - Button (ID pattern: `view-job-button-{job_id}`): View specific job details.

### 3. Job Details Page
- Page Title: "Job Details"
- Container: Div (ID: `job-details-page`)
- Elements:
  - H1 (ID: `job-title`): Job title display.
  - Div (ID: `company-name`): Company name display.
  - Div (ID: `job-description`): Full job description and requirements.
  - Div (ID: `salary-range`): Salary range display.
  - Button (ID: `apply-now-button`): Apply to the job.

### 4. Application Form Page
- Page Title: "Submit Application"
- Container: Div (ID: `application-form-page`)
- Elements:
  - Input (ID: `applicant-name`): Applicant’s name.
  - Input (ID: `applicant-email`): Applicant’s email.
  - File Input (ID: `resume-upload`): Upload resume.
  - Textarea (ID: `cover-letter`): Applicant cover letter.
  - Button (ID: `submit-application-button`): Submit application.

### 5. Application Tracking Page
- Page Title: "My Applications"
- Container: Div (ID: `tracking-page`)
- Elements:
  - Table (ID: `applications-table`): List of applications with job title, company, status, and applied date.
  - Dropdown (ID: `status-filter`): Filter applications by status (All, Applied, Under Review, Interview, Rejected).
  - Button (ID pattern: `view-application-button-{app_id}`): View details of specific application.
  - Button (ID: `back-to-dashboard`): Navigate back to Dashboard.

### 6. Companies Directory Page
- Page Title: "Company Directory"
- Container: Div (ID: `companies-page`)
- Elements:
  - Div (ID: `companies-list`): List of company cards.
  - Input (ID: `search-company-input`): Search companies by name or industry.
  - Button (ID pattern: `view-company-button-{company_id}`): View company profile.
  - Button (ID: `back-to-dashboard`): Navigate back to Dashboard.

### 7. Company Profile Page
- Page Title: "Company Profile"
- Container: Div (ID: `company-profile-page`)
- Elements:
  - Div (ID: `company-info`): Company name, industry, location, and description.
  - Div (ID: `company-jobs`): Open jobs offered by the company.
  - Div (ID: `jobs-list`): List of job titles with status.
  - Button (ID pattern: `view-job-button-{job_id}`): View job details.
  - Button (ID: `back-to-companies`): Back to Companies Directory.

### 8. Resume Management Page
- Page Title: "My Resumes"
- Container: Div (ID: `resume-page`)
- Elements:
  - Div (ID: `resumes-list`): List of uploaded resumes with upload dates.
  - Button (ID: `upload-resume-button`): Trigger resume upload.
  - File Input (ID: `resume-file-input`): Hidden input for uploading resume file.
  - Button (ID pattern: `delete-resume-button-{resume_id}`): Delete specified resume.
  - Button (ID: `back-to-dashboard`): Navigate back to Dashboard.

### 9. Search Results Page
- Page Title: "Search Results"
- Container: Div (ID: `search-results-page`)
- Elements:
  - Div (ID: `search-query-display`): Shows the entered search query.
  - Div (ID: `results-tabs`): Tabs to switch between job and company result views.
  - Div (ID: `job-results`): Display job search results.
  - Div (ID: `company-results`): Display company search results.
  - Div (ID: `no-results-message`): Message when no results found.


## Section 2: Navigation and Interaction Flow

- **Dashboard Page:**
  - `browse-jobs-button` 1212 Job Listings Page
  - `my-applications-button` 1212 Application Tracking Page
  - `companies-button` 1212 Companies Directory Page

- **Job Listings Page:**
  - `view-job-button-{job_id}` 1212 Job Details Page (specific job)

- **Job Details Page:**
  - `apply-now-button` 1212 Application Form Page

- **Application Form Page:**
  - `submit-application-button` 1212 Submit application and navigate to Application Tracking Page

- **Application Tracking Page:**
  - `view-application-button-{app_id}` 1212 View application details
  - `back-to-dashboard` 1212 Dashboard Page

- **Companies Directory Page:**
  - `view-company-button-{company_id}` 1212 Company Profile Page
  - `back-to-dashboard` 1212 Dashboard Page

- **Company Profile Page:**
  - `view-job-button-{job_id}` 1212 Job Details Page
  - `back-to-companies` 1212 Companies Directory Page

- **Resume Management Page:**
  - `upload-resume-button` 1212 Trigger file input `resume-file-input`
  - `delete-resume-button-{resume_id}` 1212 Delete resume
  - `back-to-dashboard` 1212 Dashboard Page

- **Search Results Page:**
  - Tabs in `results-tabs` to switch between `job-results` and `company-results`


## Section 3: Data Storage Schemas

### 1. Jobs Data (`jobs.txt`)
- Format: `job_id|title|company_id|location|salary_min|salary_max|category|description|posted_date`
- Example:
  `1|Senior Python Developer|1|Remote|80000|120000|Technology|Experienced Python developer for web applications|2025-01-15`
  `2|Data Analyst|2|New York, NY|60000|85000|Finance|Analyze financial data and create reports|2025-01-16`
  `3|Healthcare Administrator|3|Los Angeles, CA|50000|70000|Healthcare|Manage hospital operations and patient records|2025-01-14`

### 2. Companies Data (`companies.txt`)
- Format: `company_id|company_name|industry|location|employee_count|description`
- Example:
  `1|TechCorp|Technology|San Francisco, CA|500|Leading software solutions provider`
  `2|FinanceHub|Finance|New York, NY|300|Innovative financial services company`
  `3|MediCare|Healthcare|Los Angeles, CA|200|Premier healthcare management organization`

### 3. Categories Data (`categories.txt`)
- Format: `category_id|category_name|description`
- Example:
  `1|Technology|Software, IT, and tech-related positions`
  `2|Finance|Banking, accounting, and finance positions`
  `3|Healthcare|Medical and healthcare industry positions`

### 4. Applications Data (`applications.txt`)
- Format: `application_id|job_id|applicant_name|applicant_email|status|applied_date|resume_id`
- Example:
  `1|1|John Doe|john@email.com|Under Review|2025-01-17|1`
  `2|2|Jane Smith|jane@email.com|Applied|2025-01-16|2`
  `3|3|Robert Johnson|robert@email.com|Interview|2025-01-15|3`

### 5. Resumes Data (`resumes.txt`)
- Format: `resume_id|applicant_name|applicant_email|filename|upload_date|summary`
- Example:
  `1|John Doe|john@email.com|john_resume.pdf|2025-01-17|Senior developer with 8 years experience`
  `2|Jane Smith|jane@email.com|jane_resume.pdf|2025-01-16|Data analyst with financial background`
  `3|Robert Johnson|robert@email.com|robert_resume.pdf|2025-01-15|Healthcare administrator with 5 years experience`

### 6. Job Categories Mapping Data (`job_categories.txt`)
- Format: `mapping_id|job_id|category_id`
- Example:
  `1|1|1`
  `2|2|2`
  `3|3|3`
