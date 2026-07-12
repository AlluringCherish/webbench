# Design Specification for JobBoard Application

---

## Section 1: Flask Routes Specification

1. **Root Route**
- **Path:** /
- **Function Name:** redirect_to_dashboard
- **Methods:** GET
- **Renders Template:** None (redirect)
- **Notes:** Redirects to /dashboard

2. **Dashboard Page**
- **Path:** /dashboard
- **Function Name:** dashboard_page
- **Methods:** GET
- **Template:** dashboard.html
- **Context Variables:**
  - featured_jobs: List[dict] (Each dict: job_id[int], title[str], company_name[str], location[str], salary_min[int], salary_max[int])

3. **Job Listings Page**
- **Path:** /jobs
- **Function Name:** job_listings_page
- **Methods:** GET
- **Template:** job_listings.html
- **Context Variables:**
  - jobs: List[dict] (job_id[int], title[str], company_name[str], location[str], salary_min[int], salary_max[int], category[str])
  - categories: List[str] (category names)
  - locations: List[str] (Remote, On-site, Hybrid)
  - selected_category: Optional[str]
  - selected_location: Optional[str]
  - search_query: Optional[str]

4. **Job Details Page**
- **Path:** /job/<int:job_id>
- **Function Name:** job_details_page
- **Methods:** GET
- **Template:** job_details.html
- **Context Variables:**
  - job: dict (job_id[int], title[str], company_name[str], description[str], salary_min[int], salary_max[int], location[str], category[str], posted_date[str])

5. **Application Form Page**
- **Path:** /apply/<int:job_id>
- **Function Name:** application_form_page
- **Methods:** GET, POST
- **Template:** application_form.html
- **Context Variables (GET):**
  - job: dict (job_id[int], title[str])
- **POST Input Fields:**
  - applicant_name: str
  - applicant_email: str
  - resume_file: file
  - cover_letter: str

6. **Application Tracking Page**
- **Path:** /applications
- **Function Name:** application_tracking_page
- **Methods:** GET
- **Template:** applications_tracking.html
- **Context Variables:**
  - applications: List[dict] (application_id[int], job_title[str], company_name[str], status[str], applied_date[str])
  - status_filter_options: List[str] (All, Applied, Under Review, Interview, Rejected)
  - selected_status_filter: Optional[str]

7. **Application Details Page**
- **Path:** /application/<int:application_id>
- **Function Name:** application_details_page
- **Methods:** GET
- **Template:** application_details.html
- **Context Variables:**
  - application: dict (application_id[int], job_title[str], company_name[str], applicant_name[str], applicant_email[str], status[str], applied_date[str], resume_filename[str], cover_letter[str])

8. **Companies Directory Page**
- **Path:** /companies
- **Function Name:** companies_directory_page
- **Methods:** GET
- **Template:** companies_directory.html
- **Context Variables:**
  - companies: List[dict] (company_id[int], company_name[str], industry[str], employee_count[int])
  - search_query: Optional[str]

9. **Company Profile Page**
- **Path:** /company/<int:company_id>
- **Function Name:** company_profile_page
- **Methods:** GET
- **Template:** company_profile.html
- **Context Variables:**
  - company: dict (company_id[int], company_name[str], industry[str], location[str], employee_count[int], description[str])
  - jobs: List[dict] (job_id[int], title[str], status[str])

10. **Resume Management Page**
- **Path:** /resumes
- **Function Name:** resume_management_page
- **Methods:** GET
- **Template:** resumes.html
- **Context Variables:**
  - resumes: List[dict] (resume_id[int], applicant_name[str], applicant_email[str], filename[str], upload_date[str], summary[str])

11. **Upload Resume POST Route**
- **Path:** /resumes/upload
- **Function Name:** upload_resume
- **Methods:** POST
- **Template:** None (redirect or JSON response)
- **POST Input Fields:**
  - resume_file: file
  - applicant_name: str
  - applicant_email: str
  - summary: str

12. **Delete Resume POST Route**
- **Path:** /resumes/delete/<int:resume_id>
- **Function Name:** delete_resume
- **Methods:** POST
- **Template:** None (redirect or JSON response)
- **POST Input Fields:** None (only resume_id in URL)

13. **Search Results Page**
- **Path:** /search
- **Function Name:** search_results_page
- **Methods:** GET
- **Template:** search_results.html
- **Context Variables:**
  - query: str
  - job_results: List[dict] (job_id[int], title[str], company_name[str], location[str], salary_min[int], salary_max[int])
  - company_results: List[dict] (company_id[int], company_name[str], industry[str], employee_count[int])

---

## Section 2: HTML Template Specifications

### 1. templates/dashboard.html
- **Page Title:** Job Board Dashboard
- **Element IDs:**
  - dashboard-page (div): Container for dashboard.
  - featured-jobs (div): Featured job recommendations list.
  - browse-jobs-button (button): Navigate to job listings (/jobs).
  - my-applications-button (button): Navigate to application tracking (/applications).
  - companies-button (button): Navigate to companies directory (/companies).
- **Context Variables:**
  - featured_jobs: List[dict] with keys job_id[int], title[str], company_name[str], location[str], salary_min[int], salary_max[int]
- **Navigation:**
  - browse-jobs-button -> url_for('job_listings_page')
  - my-applications-button -> url_for('application_tracking_page')
  - companies-button -> url_for('companies_directory_page')

### 2. templates/job_listings.html
- **Page Title:** Job Listings
- **Element IDs:**
  - listings-page (div): Container.
  - search-input (input): Search field.
  - category-filter (select): Category dropdown.
  - location-filter (select): Location dropdown.
  - jobs-grid (div): Grid displaying job cards.
  - view-job-button-{{ job.job_id }} (button): View job details for each job.
- **Context Variables:**
  - jobs: List[dict] with keys job_id[int], title[str], company_name[str], location[str], salary_min[int], salary_max[int], category[str]
  - categories: List[str]
  - locations: List[str] (Remote, On-site, Hybrid)
  - selected_category: Optional[str]
  - selected_location: Optional[str]
  - search_query: Optional[str]
- **Navigation:**
  - view-job-button-{{ job.job_id }} -> url_for('job_details_page', job_id=job.job_id)

### 3. templates/job_details.html
- **Page Title:** Job Details
- **Element IDs:**
  - job-details-page (div): Container.
  - job-title (h1): Job title display.
  - company-name (div): Company name display.
  - job-description (div): Detailed description.
  - salary-range (div): Salary range display.
  - apply-now-button (button): Apply for job.
- **Context Variables:**
  - job: dict with keys job_id[int], title[str], company_name[str], description[str], salary_min[int], salary_max[int], location[str], category[str], posted_date[str]
- **Navigation:**
  - apply-now-button -> url_for('application_form_page', job_id=job.job_id)

### 4. templates/application_form.html
- **Page Title:** Submit Application
- **Element IDs:**
  - application-form-page (div): Container.
  - applicant-name (input): Applicant name.
  - applicant-email (input): Applicant email.
  - resume-upload (input, type=file): Resume file upload.
  - cover-letter (textarea): Cover letter text.
  - submit-application-button (button): Submit application.
- **Context Variables:**
  - job: dict with job_id[int], title[str]
- **Navigation:**
  - Form submission posts to same route /apply/<job_id>

### 5. templates/applications_tracking.html
- **Page Title:** My Applications
- **Element IDs:**
  - tracking-page (div): Container.
  - applications-table (table): Table of applications.
  - status-filter (select): Status filter dropdown.
  - view-application-button-{{ application.application_id }} (button): View application details.
  - back-to-dashboard (button): Return to dashboard.
- **Context Variables:**
  - applications: List[dict] with keys application_id[int], job_title[str], company_name[str], status[str], applied_date[str]
  - status_filter_options: List[str] = ["All", "Applied", "Under Review", "Interview", "Rejected"]
  - selected_status_filter: Optional[str]
- **Navigation:**
  - view-application-button-{{ application.application_id }} -> url_for('application_details_page', application_id=application.application_id)
  - back-to-dashboard -> url_for('dashboard_page')

### 6. templates/application_details.html
- **Page Title:** Application Details
- **Element IDs:**
  - application-details-page (div): Container.
  - application-id (div): Displays application ID.
  - job-title (div): Job title.
  - company-name (div): Company name.
  - applicant-name (div): Applicant name.
  - applicant-email (div): Applicant email.
  - status (div): Application status.
  - applied-date (div): Date applied.
  - resume-filename (div): Resume filename.
  - cover-letter (div): Cover letter content.
  - back-to-applications (button): Navigate back to applications tracking.
- **Context Variables:**
  - application: dict with application_id[int], job_title[str], company_name[str], applicant_name[str], applicant_email[str], status[str], applied_date[str], resume_filename[str], cover_letter[str]
- **Navigation:**
  - back-to-applications -> url_for('application_tracking_page')

### 7. templates/companies_directory.html
- **Page Title:** Company Directory
- **Element IDs:**
  - companies-page (div): Container.
  - companies-list (div): List of company cards.
  - search-company-input (input): Search companies by name or industry.
  - view-company-button-{{ company.company_id }} (button): View company profile.
  - back-to-dashboard (button): Navigate back to dashboard.
- **Context Variables:**
  - companies: List[dict] with company_id[int], company_name[str], industry[str], employee_count[int]
  - search_query: Optional[str]
- **Navigation:**
  - view-company-button-{{ company.company_id }} -> url_for('company_profile_page', company_id=company.company_id)
  - back-to-dashboard -> url_for('dashboard_page')

### 8. templates/company_profile.html
- **Page Title:** Company Profile
- **Element IDs:**
  - company-profile-page (div): Container.
  - company-info (div): Displays company_name, industry, location, description.
  - company-jobs (div): Lists all open jobs of the company.
  - jobs-list (div): Container for job cards.
  - view-job-button-{{ job.job_id }} (button): View job details for jobs listed.
  - back-to-companies (button): Back to companies directory.
- **Context Variables:**
  - company: dict with company_id[int], company_name[str], industry[str], location[str], employee_count[int], description[str]
  - jobs: List[dict] with job_id[int], title[str], status[str]
- **Navigation:**
  - view-job-button-{{ job.job_id }} -> url_for('job_details_page', job_id=job.job_id)
  - back-to-companies -> url_for('companies_directory_page')

### 9. templates/resumes.html
- **Page Title:** My Resumes
- **Element IDs:**
  - resume-page (div): Container.
  - resumes-list (div): List of resumes.
  - upload-resume-button (button): User triggers file input.
  - resume-file-input (input, type=file, hidden): Hidden file input.
  - delete-resume-button-{{ resume.resume_id }} (button): Delete specific resume.
  - back-to-dashboard (button): Navigate back to dashboard.
- **Context Variables:**
  - resumes: List[dict] with resume_id[int], applicant_name[str], applicant_email[str], filename[str], upload_date[str], summary[str]
- **Navigation:**
  - back-to-dashboard -> url_for('dashboard_page')

### 10. templates/search_results.html
- **Page Title:** Search Results
- **Element IDs:**
  - search-results-page (div): Container.
  - search-query-display (div): Shows search query text.
  - results-tabs (div): Tabs for jobs and companies results.
  - job-results (div): List of job search results.
  - company-results (div): List of company search results.
  - no-results-message (div): Display if no results found.
- **Context Variables:**
  - query: str
  - job_results: List[dict] with job_id[int], title[str], company_name[str], location[str], salary_min[int], salary_max[int]
  - company_results: List[dict] with company_id[int], company_name[str], industry[str], employee_count[int]
- **Navigation:** N/A

---

## Section 3: Data File Schemas

1. **jobs.txt** (data/jobs.txt)
- Fields: job_id|title|company_id|location|salary_min|salary_max|category|description|posted_date
- Stores: Job postings information.
- Example Rows:
  - 1|Senior Python Developer|1|Remote|80000|120000|Technology|Experienced Python developer for web applications|2025-01-15
  - 2|Data Analyst|2|New York, NY|60000|85000|Finance|Analyze financial data and create reports|2025-01-16
  - 3|Healthcare Administrator|3|Los Angeles, CA|50000|70000|Healthcare|Manage hospital operations and patient records|2025-01-14

2. **companies.txt** (data/companies.txt)
- Fields: company_id|company_name|industry|location|employee_count|description
- Stores: Registered companies details.
- Example Rows:
  - 1|TechCorp|Technology|San Francisco, CA|500|Leading software solutions provider
  - 2|FinanceHub|Finance|New York, NY|300|Innovative financial services company
  - 3|MediCare|Healthcare|Los Angeles, CA|200|Premier healthcare management organization

3. **categories.txt** (data/categories.txt)
- Fields: category_id|category_name|description
- Stores: Job categories.
- Example Rows:
  - 1|Technology|Software, IT, and tech-related positions
  - 2|Finance|Banking, accounting, and finance positions
  - 3|Healthcare|Medical and healthcare industry positions

4. **applications.txt** (data/applications.txt)
- Fields: application_id|job_id|applicant_name|applicant_email|status|applied_date|resume_id
- Stores: Submitted job applications.
- Example Rows:
  - 1|1|John Doe|john@email.com|Under Review|2025-01-17|1
  - 2|2|Jane Smith|jane@email.com|Applied|2025-01-16|2
  - 3|3|Robert Johnson|robert@email.com|Interview|2025-01-15|3

5. **resumes.txt** (data/resumes.txt)
- Fields: resume_id|applicant_name|applicant_email|filename|upload_date|summary
- Stores: Uploaded resumes metadata.
- Example Rows:
  - 1|John Doe|john@email.com|john_resume.pdf|2025-01-17|Senior developer with 8 years experience
  - 2|Jane Smith|jane@email.com|jane_resume.pdf|2025-01-16|Data analyst with financial background
  - 3|Robert Johnson|robert@email.com|robert_resume.pdf|2025-01-15|Healthcare administrator with 5 years experience

6. **job_categories.txt** (data/job_categories.txt)
- Fields: mapping_id|job_id|category_id
- Stores: Mapping of jobs to categories.
- Example Rows:
  - 1|1|1
  - 2|2|2
  - 3|3|3

---


This design specification defines all routes, templates, context variables, element IDs, and data schemas for the JobBoard application as per the requirements document.