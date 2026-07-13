# JobBoard Web Application - Requirements Analysis

## 1. Pages and Titles

### 1. Dashboard Page
- Title: Job Board Dashboard
- Container ID: dashboard-page
- UI Elements:
  - featured-jobs (div)
  - browse-jobs-button (button)
  - my-applications-button (button)
  - companies-button (button)

### 2. Job Listings Page
- Title: Job Listings
- Container ID: listings-page
- UI Elements:
  - search-input (input)
  - category-filter (dropdown)
  - location-filter (dropdown)
  - jobs-grid (div)
  - view-job-button-{job_id} (button) [dynamic]

### 3. Job Details Page
- Title: Job Details
- Container ID: job-details-page
- UI Elements:
  - job-title (h1)
  - company-name (div)
  - job-description (div)
  - salary-range (div)
  - apply-now-button (button)

### 4. Application Form Page
- Title: Submit Application
- Container ID: application-form-page
- UI Elements:
  - applicant-name (input)
  - applicant-email (input)
  - resume-upload (file input)
  - cover-letter (textarea)
  - submit-application-button (button)

### 5. Application Tracking Page
- Title: My Applications
- Container ID: tracking-page
- UI Elements:
  - applications-table (table)
  - status-filter (dropdown)
  - view-application-button-{app_id} (button) [dynamic]
  - back-to-dashboard (button)

### 6. Companies Directory Page
- Title: Company Directory
- Container ID: companies-page
- UI Elements:
  - companies-list (div)
  - search-company-input (input)
  - view-company-button-{company_id} (button) [dynamic]
  - back-to-dashboard (button)

### 7. Company Profile Page
- Title: Company Profile
- Container ID: company-profile-page
- UI Elements:
  - company-info (div)
  - company-jobs (div)
  - jobs-list (div)
  - view-job-button-{job_id} (button) [dynamic]
  - back-to-companies (button)

### 8. Resume Management Page
- Title: My Resumes
- Container ID: resume-page
- UI Elements:
  - resumes-list (div)
  - upload-resume-button (button)
  - resume-file-input (file input)
  - delete-resume-button-{resume_id} (button) [dynamic]
  - back-to-dashboard (button)

### 9. Search Results Page
- Title: Search Results
- Container ID: search-results-page
- UI Elements:
  - search-query-display (div)
  - results-tabs (div)
  - job-results (div)
  - company-results (div)
  - no-results-message (div)


## 2. UI Element IDs

- Static IDs: e.g., dashboard-page, listings-page, job-details-page, etc.
- Dynamic IDs with variable placeholders:
  - view-job-button-{job_id}
  - view-application-button-{app_id}
  - view-company-button-{company_id}
  - delete-resume-button-{resume_id}


## 3. Navigation Structure

- Entry Point: Dashboard Page (dashboard-page)

- From Dashboard:
  - browse-jobs-button -> Job Listings Page (listings-page)
  - my-applications-button -> Application Tracking Page (tracking-page)
  - companies-button -> Companies Directory Page (companies-page)

- From Job Listings Page:
  - view-job-button-{job_id} -> Job Details Page (job-details-page)

- From Job Details Page:
  - apply-now-button -> Application Form Page (application-form-page)

- From Application Tracking Page:
  - view-application-button-{app_id} -> Application Detail View (not separately listed, assumed in tracking or details page)
  - back-to-dashboard -> Dashboard Page

- From Companies Directory Page:
  - view-company-button-{company_id} -> Company Profile Page (company-profile-page)
  - back-to-dashboard -> Dashboard Page

- From Company Profile Page:
  - view-job-button-{job_id} -> Job Details Page
  - back-to-companies -> Companies Directory Page

- From Resume Management Page:
  - upload-resume-button -> Trigger resume-file-input for upload
  - delete-resume-button-{resume_id} -> Delete specific resume
  - back-to-dashboard -> Dashboard Page


## 4. Data Storage Summary

### Location
- All data files are stored in the directory named `data`.

### Data Files and Formats

1. **Jobs Data**
   - File: `jobs.txt`
   - Format:
     ```
     job_id|title|company_id|location|salary_min|salary_max|category|description|posted_date
     ```
   - Example:
     ```
     1|Senior Python Developer|1|Remote|80000|120000|Technology|Experienced Python developer for web applications|2025-01-15
     ```

2. **Companies Data**
   - File: `companies.txt`
   - Format:
     ```
     company_id|company_name|industry|location|employee_count|description
     ```
   - Example:
     ```
     1|TechCorp|Technology|San Francisco, CA|500|Leading software solutions provider
     ```

3. **Categories Data**
   - File: `categories.txt`
   - Format:
     ```
     category_id|category_name|description
     ```
   - Example:
     ```
     1|Technology|Software, IT, and tech-related positions
     ```

4. **Applications Data**
   - File: `applications.txt`
   - Format:
     ```
     application_id|job_id|applicant_name|applicant_email|status|applied_date|resume_id
     ```
   - Example:
     ```
     1|1|John Doe|john@email.com|Under Review|2025-01-17|1
     ```

5. **Resumes Data**
   - File: `resumes.txt`
   - Format:
     ```
     resume_id|applicant_name|applicant_email|filename|upload_date|summary
     ```
   - Example:
     ```
     1|John Doe|john@email.com|john_resume.pdf|2025-01-17|Senior developer with 8 years experience
     ```

6. **Job Categories Mapping Data**
   - File: `job_categories.txt`
   - Format:
     ```
     mapping_id|job_id|category_id
     ```
   - Example:
     ```
     1|1|1
     ```

### Data Relationships

- Jobs reference Companies by `company_id`.
- Jobs relate to Categories via `job_categories.txt` mapping.
- Applications link to Jobs and Resumes by `job_id` and `resume_id` respectively.
- Resumes contain applicant contact info and filename of upload.

---

This document provides a complete mapping of pages, UI elements, navigation flows, and data storage requirements as specified in the user task description for the JobBoard web application.