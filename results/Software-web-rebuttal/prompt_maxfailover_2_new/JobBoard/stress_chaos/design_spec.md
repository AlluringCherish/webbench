# Design Specification Document for JobBoard Web Application

---

## Section 1: Flask Routes Specification

| Route Path                 | Function Name            | HTTP Method(s) | Template Rendered       | Context Variables (name: type)                                    | POST Input Expectations                                  |
|----------------------------|--------------------------|----------------|------------------------|------------------------------------------------------------------|----------------------------------------------------------|
| /                          | root_redirect             | GET            | Redirect to `/dashboard`| None                                                             | None                                                     |
| /dashboard                 | dashboard_page            | GET            | dashboard.html          | featured_jobs: list[dict], latest_jobs: list[dict]             | None                                                     |
| /jobs                      | job_listings_page         | GET            | job_listings.html       | jobs: list[dict], categories: list[dict], selected_category: str, selected_location: str, search_query: str | None                                                     |
| /job/<int:job_id>          | job_details_page          | GET            | job_details.html        | job: dict, company: dict                                       | None                                                     |
| /apply/<int:job_id>        | application_form_page     | GET, POST      | application_form.html   | job: dict                                                      | POST fields: applicant_name (str), applicant_email (str), resume_file (file), cover_letter (str)             |
| /applications              | application_tracking_page | GET            | application_tracking.html| applications: list[dict], status_filter: str                   | None                                                     |
| /application/<int:app_id>  | application_detail_page   | GET            | (Could be application details, not defined in requirements)    | application: dict                                            | None                                                     |
| /companies                 | companies_directory_page  | GET            | companies.html          | companies: list[dict], search_query: str                       | None                                                     |
| /company/<int:company_id>  | company_profile_page      | GET            | company_profile.html    | company: dict, jobs: list[dict]                               | None                                                     |
| /resumes                   | resume_management_page    | GET, POST      | resume_management.html  | resumes: list[dict]                                           | POST fields: resume_file (file), applicant_name (str), applicant_email (str), summary (str)                   |
| /resume/delete/<int:resume_id> | delete_resume           | POST           | Redirect back to /resumes| None                                                         | None                                                     |
| /search                    | search_results_page       | GET            | search_results.html     | query: str, job_results: list[dict], company_results: list[dict]| None                                                     |


### Detailed Route Specifications:

1. **/**
   - Function Name: `root_redirect`
   - Method: GET
   - Behavior: Redirects to `/dashboard`
   - Template: None (redirect)
   - Context: None

2. **/dashboard**
   - Function Name: `dashboard_page`
   - Method: GET
   - Template: `dashboard.html`
   - Context Variables:
     - `featured_jobs`: list of dicts, each dict contains job summary data for featured jobs.
     - `latest_jobs`: list of dicts, each dict contains job summary data for latest posted jobs.

3. **/jobs**
   - Function Name: `job_listings_page`
   - Method: GET
   - Template: `job_listings.html`
   - Context Variables:
     - `jobs`: list of dict, each with job listing data.
     - `categories`: list of dict, each with 'category_id', 'category_name', and 'description'.
     - `selected_category`: str, category filter selected (may be empty string for none).
     - `selected_location`: str, location filter selected (may be empty string).
     - `search_query`: str, the input from the search box (may be empty).

4. **/job/<int:job_id>**
   - Function Name: `job_details_page`
   - Method: GET
   - Template: `job_details.html`
   - Context Variables:
     - `job`: dict containing all job fields.
     - `company`: dict containing company details for the job.

5. **/apply/<int:job_id>**
   - Function Name: `application_form_page`
   - Methods: GET, POST
   - Template: `application_form.html`
   - GET Context Variables:
     - `job`: dict with job details.
   - POST Input Fields:
     - `applicant_name` (str): Name of the applicant.
     - `applicant_email` (str): Email of the applicant.
     - `resume_file` (file): Resume upload.
     - `cover_letter` (str): Text of cover letter.

6. **/applications**
   - Function Name: `application_tracking_page`
   - Method: GET
   - Template: `application_tracking.html`
   - Context Variables:
     - `applications`: list of dict, each with application details joined with job title and company name.
     - `status_filter`: str, filter selected (e.g., 'All', 'Applied', 'Under Review', etc.)

7. **/application/<int:app_id>** (Optional extension; not explicitly in requirements but noted for completeness)
   - Function Name: `application_detail_page`
   - Method: GET
   - Template: could be a detailed application view, not specified - possibly omitted.
   - Context Variables:
     - `application`: dict with all details of single application.

8. **/companies**
   - Function Name: `companies_directory_page`
   - Method: GET
   - Template: `companies.html`
   - Context Variables:
     - `companies`: list of dict each containing company details.
     - `search_query`: str input for filtering company list.

9. **/company/<int:company_id>**
   - Function Name: `company_profile_page`
   - Method: GET
   - Template: `company_profile.html`
   - Context Variables:
     - `company`: dict with company details.
     - `jobs`: list of dict with all open jobs for this company.

10. **/resumes**
    - Function Name: `resume_management_page`
    - Methods: GET, POST
    - Template: `resume_management.html`
    - GET Context Variables:
      - `resumes`: list of dict containing uploaded resumes.
    - POST Input Fields:
      - `resume_file` (file): Resume file upload.
      - `applicant_name` (str): Name of applicant.
      - `applicant_email` (str): Email of applicant.
      - `summary` (str): Text summary of resume.

11. **/resume/delete/<int:resume_id>**
    - Function Name: `delete_resume`
    - Method: POST
    - Template: None (redirect)
    - Context Variables: None
    - Input: No form fields; action triggered by button.

12. **/search**
    - Function Name: `search_results_page`
    - Method: GET
    - Template: `search_results.html`
    - Context Variables:
      - `query`: str, the search query entered.
      - `job_results`: list of dict for job search results.
      - `company_results`: list of dict for company search results.

---

## Section 2: HTML Template Specifications

### 1. dashboard.html
- Filename: templates/dashboard.html
- Page Title: Job Board Dashboard
- Element IDs:
  - `dashboard-page`: Div container for dashboard page.
  - `featured-jobs`: Div displaying featured job recommendations.
  - `browse-jobs-button`: Button; navigates to `/jobs` using url_for('job_listings_page').
  - `my-applications-button`: Button; navigates to `/applications` using url_for('application_tracking_page').
  - `companies-button`: Button; navigates to `/companies` using url_for('companies_directory_page').
- Context Variables:
  - `featured_jobs`: list of dict with job summaries (fields: at least job_id:int, title:str, company_name:str, location:str, salary_min:int, salary_max:int).
  - `latest_jobs`: list of dict similar to featured_jobs (optional display).
- Navigation Mappings:
  - `browse-jobs-button`: url_for('job_listings_page')
  - `my-applications-button`: url_for('application_tracking_page')
  - `companies-button`: url_for('companies_directory_page')

---

### 2. job_listings.html
- Filename: templates/job_listings.html
- Page Title: Job Listings
- Element IDs:
  - `listings-page`: Div container for the listings page.
  - `search-input`: Input field for job search (by title, company, location).
  - `category-filter`: Dropdown to select job category filter.
  - `location-filter`: Dropdown to select location filter.
  - `jobs-grid`: Div grid displaying job card elements.
  - `view-job-button-{{job.job_id}}`: Button for each job card to view job details.
- Context Variables:
  - `jobs`: list of dict with job details.
  - `categories`: list of dict with category_id, category_name, description.
  - `selected_category`: str for the current category filter.
  - `selected_location`: str for current location filter.
  - `search_query`: str for the current search input.
- Navigation Mappings:
  - For each `view-job-button-{{job.job_id}}`: url_for('job_details_page', job_id=job.job_id)

---

### 3. job_details.html
- Filename: templates/job_details.html
- Page Title: Job Details
- Element IDs:
  - `job-details-page`: Div container for job details page.
  - `job-title`: H1 element displaying job title.
  - `company-name`: Div displaying company name.
  - `job-description`: Div for full job description and requirements.
  - `salary-range`: Div displaying salary range.
  - `apply-now-button`: Button to navigate to application form for this job.
- Context Variables:
  - `job`: dict with all job fields.
  - `company`: dict with company details.
- Navigation Mappings:
  - `apply-now-button`: url_for('application_form_page', job_id=job.job_id)

---

### 4. application_form.html
- Filename: templates/application_form.html
- Page Title: Submit Application
- Element IDs:
  - `application-form-page`: Div container for the application form.
  - `applicant-name`: Input field for applicant name.
  - `applicant-email`: Input field for applicant email.
  - `resume-upload`: File input field for resume upload.
  - `cover-letter`: Textarea for cover letter text.
  - `submit-application-button`: Button to submit the application form.
- Context Variables:
  - `job`: dict with job details to which application is made.
- Navigation Mappings:
  - Form submits POST to url_for('application_form_page', job_id=job.job_id)

---

### 5. application_tracking.html
- Filename: templates/application_tracking.html
- Page Title: My Applications
- Element IDs:
  - `tracking-page`: Div container for tracking page.
  - `applications-table`: Table displaying applications with columns: job title, company, status, date applied.
  - `status-filter`: Dropdown to filter applications by status.
  - `view-application-button-{{app.application_id}}`: Button to view application details (optional extended feature).
  - `back-to-dashboard`: Button to navigate back to dashboard.
- Context Variables:
  - `applications`: list of dict with application details including job title and company.
  - `status_filter`: str current selected filter.
- Navigation Mappings:
  - `back-to-dashboard`: url_for('dashboard_page')

---

### 6. companies.html
- Filename: templates/companies.html
- Page Title: Company Directory
- Element IDs:
  - `companies-page`: Div container for companies page.
  - `companies-list`: Div list of company cards.
  - `search-company-input`: Input for company name or industry search.
  - `view-company-button-{{company.company_id}}`: Button to view company profiles.
  - `back-to-dashboard`: Button to navigate back to dashboard.
- Context Variables:
  - `companies`: list of dict with company details.
  - `search_query`: str for current input search.
- Navigation Mappings:
  - For each `view-company-button-{{company.company_id}}`: url_for('company_profile_page', company_id=company.company_id)
  - `back-to-dashboard`: url_for('dashboard_page')

---

### 7. company_profile.html
- Filename: templates/company_profile.html
- Page Title: Company Profile
- Element IDs:
  - `company-profile-page`: Div container for company profile page.
  - `company-info`: Div displaying company name, industry, location, and description.
  - `company-jobs`: Div showing all open jobs from this company.
  - `jobs-list`: Div listing job titles and status.
  - `view-job-button-{{job.job_id}}`: Button to view job details from company profile.
  - `back-to-companies`: Button to go back to companies directory.
- Context Variables:
  - `company`: dict with company details.
  - `jobs`: list of dict with open jobs for company.
- Navigation Mappings:
  - For each `view-job-button-{{job.job_id}}`: url_for('job_details_page', job_id=job.job_id)
  - `back-to-companies`: url_for('companies_directory_page')

---

### 8. resume_management.html
- Filename: templates/resume_management.html
- Page Title: My Resumes
- Element IDs:
  - `resume-page`: Div container for resume management.
  - `resumes-list`: Div listing all uploaded resumes with upload date.
  - `upload-resume-button`: Button to trigger resume upload.
  - `resume-file-input`: Hidden file input for upload.
  - `delete-resume-button-{{resume.resume_id}}`: Button to delete a specific resume.
  - `back-to-dashboard`: Button to navigate back to dashboard.
- Context Variables:
  - `resumes`: list of dict with resumes data (fields: resume_id, applicant_name, applicant_email, filename, upload_date, summary).
- Navigation Mappings:
  - `upload-resume-button`: triggers file input `resume-file-input` (client-side JS behavior)
  - For each `delete-resume-button-{{resume.resume_id}}`: form POST to url_for('delete_resume', resume_id=resume.resume_id)
  - `back-to-dashboard`: url_for('dashboard_page')

---

### 9. search_results.html
- Filename: templates/search_results.html
- Page Title: Search Results
- Element IDs:
  - `search-results-page`: Div container for search results.
  - `search-query-display`: Div showing the user search query.
  - `results-tabs`: Div containing tabs to switch job/company results.
  - `job-results`: Div listing jobs matching search.
  - `company-results`: Div listing companies matching search.
  - `no-results-message`: Div displayed if no results found.
- Context Variables:
  - `query`: str search query.
  - `job_results`: list of dict with job info.
  - `company_results`: list of dict with company info.
- Navigation Mappings:
  - For job entries: Buttons for job detail navigation url_for('job_details_page', job_id=job.job_id)
  - For company entries: Buttons for company profile navigation url_for('company_profile_page', company_id=company.company_id)

---

## Section 3: Data File Schemas

1. **data/jobs.txt**
- Pipe-delimited fields:
  `job_id|title|company_id|location|salary_min|salary_max|category|description|posted_date`
- Description: Stores all job postings with details.
- Example rows:
  ```
  1|Senior Python Developer|1|Remote|80000|120000|Technology|Experienced Python developer for web applications|2025-01-15
  2|Data Analyst|2|New York, NY|60000|85000|Finance|Analyze financial data and create reports|2025-01-16
  3|Healthcare Administrator|3|Los Angeles, CA|50000|70000|Healthcare|Manage hospital operations and patient records|2025-01-14
  ```

2. **data/companies.txt**
- Pipe-delimited fields:
  `company_id|company_name|industry|location|employee_count|description`
- Description: Stores company profiles.
- Example rows:
  ```
  1|TechCorp|Technology|San Francisco, CA|500|Leading software solutions provider
  2|FinanceHub|Finance|New York, NY|300|Innovative financial services company
  3|MediCare|Healthcare|Los Angeles, CA|200|Premier healthcare management organization
  ```

3. **data/categories.txt**
- Pipe-delimited fields:
  `category_id|category_name|description`
- Description: Stores job categories.
- Example rows:
  ```
  1|Technology|Software, IT, and tech-related positions
  2|Finance|Banking, accounting, and finance positions
  3|Healthcare|Medical and healthcare industry positions
  ```

4. **data/applications.txt**
- Pipe-delimited fields:
  `application_id|job_id|applicant_name|applicant_email|status|applied_date|resume_id`
- Description: Stores all job applications with status tracking.
- Example rows:
  ```
  1|1|John Doe|john@email.com|Under Review|2025-01-17|1
  2|2|Jane Smith|jane@email.com|Applied|2025-01-16|2
  3|3|Robert Johnson|robert@email.com|Interview|2025-01-15|3
  ```

5. **data/resumes.txt**
- Pipe-delimited fields:
  `resume_id|applicant_name|applicant_email|filename|upload_date|summary`
- Description: Stores uploaded resumes metadata.
- Example rows:
  ```
  1|John Doe|john@email.com|john_resume.pdf|2025-01-17|Senior developer with 8 years experience
  2|Jane Smith|jane@email.com|jane_resume.pdf|2025-01-16|Data analyst with financial background
  3|Robert Johnson|robert@email.com|robert_resume.pdf|2025-01-15|Healthcare administrator with 5 years experience
  ```

6. **data/job_categories.txt**
- Pipe-delimited fields:
  `mapping_id|job_id|category_id`
- Description: Maps jobs to categories; useful for multi-category filtering if extended.
- Example rows:
  ```
  1|1|1
  2|2|2
  3|3|3
  ```

---

This specification document ensures absolute clarity and consistency for both backend and frontend developers to independently implement and integrate the JobBoard application.

All variable names, function names, template filenames, element IDs, and data schema field names must be adhered to exactly as specified.

No implementation code is included herein; only detailed design specifications to guide development.
