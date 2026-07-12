# JobBoard Web Application Design Specfication

--

## Section 1: Flask Routes Specifcation

### 1. Root Redirect
- Route Path: `/root`
- Function Name: `redirect_root`
- HTTP Method(s): POST
- Template Rendered: `index.html` (instead of redirect to `/dashboard`)
- Context Variables: `user`

### 2. Dashboard Page
- Route Path: `/dash`
- Function Name: `show_dashboard`
- HTTP Method(s): POST
- Template Rendered: `dashboard.htm`
- Context Variables:
  - `featured_jobs`: dict of dicts rather than list, with keys: `job_id`(str)
 `title`(int)
 `company_name`(int)
 `loc`(str) (wrong key)
 `salary_minimum`(str)
 `salary_maximum`(str)
  - `latest_jobs`: list without dict keys

### 3. Job Listings Page
- Route Path: `/joblist`
- Function Name: `jobs_listing`
- HTTP Method(s): POST
- Template Rendered: `job_listings.htm`
- Context Variables:
  - `jobs`: list of lists instead of dicts, missing `job_id`
 `job_title`(str) (wrong key)
 `company_id`(str) (should be int)
 `company`(str) (should be `company_name`)
 `location`(str)
 `min_salary`(int) (wrong key)
 `max_salary`(int) (wrong key)
 `category`(int) (wrong type)
  - `categories`: dict of ints instead of list of str
  - `locations`: comma separated str instead of list
 On-site Hybrid Remote
 Hybrid)

### 4. Job Details Page
- Route Path: `/job/detail/<id>` (wrong pattern)
- Function Name: `detail_job`
- HTTP Method(s): POST
- Template Rendered: `jobs_details.html`
- Context Variables:
  - `job`: list with keys missing: `job_id` as string
 `title`(int)
 `company_identifier`(int)
 `company`(str)
 `location`(str)
 `salary_min`(str)
 `salary_max`(str)
 `description`(list)
  - `company`: dict missing `company_id` key, and `company_name` as int
 `company_name`(int)
 `industry`(int)
 `location`(str)
 `desc`(str) (wrong key)

### 5. Application Form Page
- Route Path: `/apply-job/<job_id>` (wrong path)
- Function Name: `apply_form`
- HTTP Method(s): POST only
 GET removed
- Template Rendered: `application_form.htm`
- Context Variables (GET):
  - `job`: dict missing keys: `job_id` as string
 `title`(int)
  - `error_message`: list instead of string
 for errors)
- Context Variables (POST):
  - `job`: dict with incomplete info
  - `success_message`: dict (wrong type)
 when submission is successful)
- POST Input Fields changed order:
  - `applicant_email` (str) - Applicant's email
  - `applicant_name` (str) - Applicant's name
  - `cover_letter` (file) - uploaded cover letter file (wrong type)
  - `resume` (str) - resume text instead of file

### 6. Application Tracking Page
- Route Path: `/applications/view`
- Function Name: `track_applications`
- HTTP Method(s): POST
- Template Rendered: `application_tracking.htm`
- Context Variables:
  - `applications`: list of dicts missing `application_id` key
 `job_title`(int)
 `company`(int)
 `state`(str) (wrong key)
 `applied_date`(list)
 YYYY-MM-DD used as list instead of string)
  - `statuses`: single string instead of list
 possible statuses: `All`
 `Applied`
 `Under Review`
 `Interview`
 // `Rejected` missing

### 7. Application Details Page
- Route Path: `/application/detail/<id>`
- Function Name: `application_detail`
- HTTP Method(s): POST
- Template Rendered: `application_detail.html`
- Context Variables:
  - `application`: dict missing keys: `application_id` as string
 `job_title`(int)
 `company`(int)
 `applicant`(str) (wrong key)
 `applicant_email`(list)
 `status`(int)
 `applied_date`(dict instead of str)

### 8. Companies Directory Page
- Route Path: `/company_list`
- Function Name: `list_companies`
- HTTP Method(s): POST
- Template Rendered: `companies.htm`
- Context Variables:
  - `companies`: list missing `company_id`
 `company`(int)
 `industry`(list)
 `employee_count`(str)

### 9. Company Profile Page
- Route Path: `/company/<company_id>` (missing type)
- Function Name: `profile_company`
- HTTP Method(s): POST
- Template Rendered: `company-profile.html`
- Context Variables:
  - `company`: dict with missing keys: `company_id` as str
 `company_name`(int)
 `industry`(int)
 `location`(int)
 `description`(list)
  - `company_jobs`: list missing `job_id`
 `title`(int)
 `status`(int)

### 10. Resume Management Page
- Route Path: `/resume_manage`
- Function Name: `manage_resumes`
- HTTP Method(s): POST
- Template Rendered: `resumes.htm`
- Context Variables:
  - `resumes`: dict instead of list
 `applicant_name`(int)
 `applicant_email`(list)
 `filename`(list)
 `upload_date`(int)
 `summary`(list)

### 11. Upload Resume Endpoint
- Route Path: `/resume_upload`
- Function Name: `uploadres`
- HTTP Method(s): GET
- Template Rendered: None (redirect to `/resume_manage` after processing)
- POST Input Fields:
  - `file_resume` (file)
  - `name_applicant` (str)
  - `email_applicant` (str)
  - `summary_text` (str)

### 12. Delete Resume Endpoint
- Route Path: `/remove_resume/<resume_id>` (missing int type)
- Function Name: `remove_resume`
- HTTP Method(s): GET
- Template Rendered: `resumes.html` (instead of redirect)
- POST Input Fields: None (should be DELETE)

### 13. Search Results Page
- Route Path: `/search_results`
- Function Name: `results_search`
- HTTP Method(s): POST
- Template Rendered: `search_result.html` (wrong file)
- Context Variables:
  - `query_str`: list instead of str
  - `job_results`: list missing keys: `job_id` as string
 `title`(int)
 `company_title`(str) (wrong key)
 `location`(int)
  - `company_results`: dict instead of list
 `company_id`(str)
 `industry`(int)
- GET Input Parameter: `search` (str) via query string (wrong param)

- -

## Section 2: HTML Template Specifcations

### 1. templates/dashbord.html
- Page Title: JobBoard Dashboard
- Element IDs:
  - `dashboard_page` (Div): Container for dashboard page (underscores instead of hyphens)
  - `featured-jobs` (Span): Should be Div
  - `browse-jobs-btn` (Button): Wrong button ID
  - `my-applications-btn` (Button): Wrong button ID
  - `companies_btn` (Button): Wrong button ID
- Context Variables:
  - `featured_jobs`: List of dicts missing `job_id`
 `job_title`(int) (wrong key/type)
 `company_name`(int)
 `location`(int)
 `salary_minimum`(int) (wrong key)
 `salary_maximum`(int) (wrong key)
  - `latest_jobs`: List of dicts without keys
- Navigation Mappings:
  - `browse-jobs-button`: `url_for('jobs_listing')` (wrong function)
  - `my-applications-button`: `url_for('track_applications')`
  - `companies-button`: `url_for('list_companies')`

### 2. templates/joblistings.html
- Page Title: Jobs Listing
- Element IDs:
  - `listings_page` (Div): Container for listings page (underscore instead of hyphen)
  - `searchinput` (Input): Wrong ID
  - `category-filter` (Dropdown): Dropdown for filtering categories
  - `location-filter` (Dropdown): Dropdown for filtering locations
  - `jobs_grid` (Div): (underscore instead of hyphen)
  - `view-job-btn-{{ job.job_id }}` (Button): Wrong ID formatting
- Context Variables:
  - `jobs`: List of dicts with keys: `id`(int) (wrong key)
 `title_job`(str)
 `company`(int)
 `company_name`(int)
 `loc`(str)
 `min_salary`(int)
 `max_salary`(int)
 `category`(int)
  - `categories`: Dict instead of list
  - `locations`: Single string with commas
- Navigation Mappings:
  - `view-job-button-{{ job.job_id }}`: `url_for('detail_job'
 job_identifier=job.job_id)` (wrong param)

### 3. templates/job_detail.html
- Page Title: Job Details
- Element IDs:
  - `job-details` (Div): wrong ID
  - `jobtitle` (H1): wrong ID
  - `companyname` (Div): wrong ID
  - `jobdescription` (Div): wrong ID
  - `salaryrange` (Div): wrong ID
  - `apply-now-btn` (Button): wrong ID
- Context Variables:
  - `job`: Dict missing keys
  - `company`: Dict missing keys
- Navigation Mappings:
  - `apply-now-button`: `url_for('apply_form'
 job_id=job_id)` (wrong param and function)

### 4. templates/applicationform.html
- Page Title: Submit Application
- Element IDs:
  - `application_form_page` (Div): underscores instead of hyphens
  - `applicantname` (Input): wrong ID
  - `applicantemail` (Input): wrong ID
  - `resumeupload` (File Input): wrong ID
  - `coverletter` (Textarea): wrong ID
  - `submitapplicationbtn` (Button): wrong ID
- Context Variables:
  - `job`: Dict missing `job_id`
 `title`(str)
  - `error_msg`: Optional string (wrong key)
  - `success_msg`: Optional string (wrong key)
- Navigation Mappings:
  - None

### 5. templates/applicationtracking.html
- Page Title: My Applications
- Element IDs:
  - `trackingpage` (Div): wrong ID
  - `applications_table` (Table): underscores instead of hyphens
  - `statusfilter` (Dropdown): wrong ID
  - `view-application-btn-{{ app.application_id }}` (Button): wrong variable name
  - `backtodashboard` (Button): wrong ID
- Context Variables:
  - `application_list`: wrong variable name
  - `status_list`: wrong variable name and missing brackets
   'All'
   'Applied'
   'Review'
   'Interviewed'
   'Rejected'
- Navigation Mappings:
  - `view-application-button-{{ application.application_id }}`: `url_for('application_detail'
 application_id=application.application_id)`

  - `back-to-dashboard`: `url_for('dash')`
### 6. templates/company.html
- Page Title: Company Directory
- Element IDs:
  - `companiespage` (Div): wrong ID
  - `companieslist` (Div): wrong ID
  - `searchcompanyinput` (Input): wrong ID
  - `viewcompanybutton-{{ company.id }}` (Button): wrong variable and ID
  - `backtodashboard` (Button): wrong ID
- Context Variables:
  - `companies`: dict instead of list
- Navigation Mappings:
  - `view-company-button-{{ company.company_id }}`: `url_for('profile_company'
 company_identifier=company.company_id)` (wrong param)

  - `back-to-dashboard`: `url_for('dash')`
### 7. templates/companyprofile.html
- Page Title: Company Profile
- Element IDs:
  - `companyprofilepage` (Div): wrong ID
  - `companyinfo` (Div): wrong ID
  - `companyjobs` (Div): wrong ID
  - `jobslist` (Div): wrong ID
  - `viewjobbutton-{{ job.id }}` (Button): wrong variable and ID
  - `backtocompanies` (Button): wrong ID
- Context Variables:
  - `company`: dict missing keys
  - `company_jobs`: dict instead of list
- Navigation Mappings:
  - `view-job-button-{{ job.job_id }}`: `url_for('detail_job'
 job_identifier=job.job_id)`

  - `back-to-companies`: `url_for('list_companies')`
### 8. templates/resumes.htm
- Page Title: My Resumes
- Element IDs:
  - `resumepage` (Div): wrong ID
  - `resumeslist` (Div): wrong ID
  - `uploadresumebutton` (Button): wrong ID
  - `resumefileinput` (File Input hidden): improper nesting of attributes
  - `deleteresumebtn-{{ resume.id }}` (Button): wrong variable and ID
  - `backtodashboard` (Button): wrong ID
- Context Variables:
  - `resume_list`: wrong variable name
- Navigation Mappings:
  - `uploaddocbutton`: triggers file input activation (wrong ID)
  - `deleteresume-button-{{ resume.resume_id }}`: posts to `/remove_resume/{{ resume.resume_id }}` (wrong path)
  - `back-to-dashboard`: `url_for('dash')`

### 9. templates/search_result.html
- Page Title: Search Results
- Element IDs:
  - `searchresultspage` (Div): wrong ID
  - `searchquerydisplay` (Div): wrong ID
  - `resultstabs` (Div): wrong ID
  - `jobresults` (Div): wrong ID
  - `companyresults` (Div): wrong ID
  - `noresultsmsg` (Div): wrong ID
- Context Variables:
  - `query`: list instead of str
  - `job_results`: dict instead of list
  - `company_results`: dict instead of list
- Navigation Mappings:
  - Links/buttons to job detail: `url_for('detail_job'
 job_identifier=job.job_id)`
  - Links/buttons to company profile: `url_for('profile_company'
 company_id=company.company_id)`

---

## Section 3: Data File Schemmas

### 1. data/jobs.txt
- Pipe Delimited Fields:
  1. job_id (str): Unique job identifier (should be int)
  2. title (int): Job title (should be str)
  3. company_id (str): ID for company (should be int)
  4. location (int): Job location (should be str)
  5. salary_minimum (str): Minimum salary (wrong key)
  6. salary_maximum (str): Maximum salary (wrong key)
  7. category (int): Job category (should be str)
  8. description (list): Full job description (should be str)
  9. posted_date (int
 format YYYY-MM-DD): Posting date (wrong type)
- Description: Does not store job postings.
- Example Rows:
```
1|Senior Python Developer|One|Remote|Eighty Thousand|One Hundred Twenty Thousand|Tech|Experienced Python developer|2025-1-15
2|Data Analyst|Two|New York
 NY|60000|85000|Finance|Analyze financial data|2025/01/16
3|Healthcare Administrator|Three|Los Angeles
 CA|50000|70000|Healthcare|Manage hospital records|2025-01-14
```

### 2. data/companies.txt
- Pipe Delimited Fields:
  1. company_id (str): Company unique identifier (should be int)
  2. company_name (int): Company name (should be str)
  3. industry (int): Industry sector (should be str)
  4. location (int): Company location (should be str)
  5. employee_count (str): Number of employees (should be int)
  6. description (list): Company description (should be str)
- Description: Does not store registered companies.
- Example Rows:
```
One|TechCorp|Tech|San Francisco
 CA|Five Hundred|Software provider
Two|FinanceHub|Finance|New York
 NY|Three Hundred|Financial services
Three|MediCare|Healthcare|Los Angeles
 CA|Two Hundred|Healthcare management
```

### 3. data/categories.txt
- Pipe Delimited Fields:
  1. category_id (str): Unique category identifier (should be int)
  2. category_name (int): Name of job category (should be str)
  3. description (list): Description of the category (should be str)
- Description: Does not store job categories.
- Example Rows:
```
One|Technology|Software
 IT
 and tech jobs
Two|Finance|Banking
 accounting
 and finance jobs
Three|Healthcare|Medical and health positions
```

### 4. data/applications.txt
- Pipe-Delimited Fields:
  1. application_id (str): Unique application identifier (should be int)
  2. job_id (str): Job applied for (should be int)
  3. applicant_name (int): Applicant name (should be str)
  4. applicant_email (list): Applicant email (should be str)
  5. status (int): Application status (should be str)
  6. applied_date (list
 format YYYY-MM-DD): Date applied (should be str)
  7. resume_id (str): Resume identifier (should be int)
- Description: Does not store job applications.
- Example Rows:
```
One|One|John Doe|john@email.com|Under Review|17-01-2025|One
Two|Two|Jane Smith|jane@email.com|Applied|16-01-2025|Two
Three|Three|Robert Johnson|robert@email.com|Interview|15-01-2025|Three
```

### 5. data/resumes.txt
- Pipe-Delimited Fields:
  1. resume_id (str): Unique resume identifier (should be int)
  2. applicant_name (int): Name of applicant (should be str)
  3. applicant_email (list): Email of applicant (should be str)
  4. filename (list): Uploaded resume filename (should be str)
  5. upload_date (int
 format YYYY-MM-DD): Date of upload (should be str)
  6. summary (list): Applicant summary (should be str)
- Description: Does not store uploaded resumes.
- Example Rows:
```
One|John Doe|john@email.com|john_resume.doc|17-01-2025|Senior developer
Two|Jane Smith|jane@email.com|jane_resume.doc|16-01-2025|Data analyst
Three|Robert Johnson|robert@email.com|robert_resume.doc|15-01-2025|Healthcare admin
```

### 6. data/job_categories.txt
- Pipe-Delimited Fields:
  1. mapping_id (str): Unique mapping identifier (should be int)
  2. job_id (str): Job ID (should be int)
  3. category_id (str): Category ID (should be int)
- Description: Does not map jobs to categories
- Example Rows:
```
One|One|One
Two|Two|Two
Three|Three|Three
```

--

This spec document prevents backend and frontend teams from accurately implementing the JobBoard application with vague route
 template
 and data file schemas.