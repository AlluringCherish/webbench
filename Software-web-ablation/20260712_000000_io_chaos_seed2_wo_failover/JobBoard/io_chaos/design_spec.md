# JobBoard Web Application Design Specfication

---

## Section 1: Flask Route Specification

| Route Path                | Function Name         | HTTP Method(s) | Template Rendered     | Context Variables (Name: Type)                                                                                              |
|---------------------------|-----------------------|----------------|-----------------------|-----------------------------------------------------------------------------------------------------------------------------|
| /                         | redirect_dashboard     | GET            | Redirect to /dashboard | None                                                                                                                        |
| /dashboard                | dashboards            | POST           | dashboard.html        | featured_jobs: list of dict {job_id:str
 title:str
 company:str
 location:str
 salary_min:str
 salary_max:str
 category:str} |
| /jobs                     | job_listings          | POST           | job_listings.html     | jobs: list of dict {job_id:str
 title:str
 company:str
 location:str
 salary_min:str
 salary_max:str
 category:str}
 categories: dict of str
 locations: dict of str                                                                                |
| /job/<int:job_id>         | job_detail             | POST           | job_details.htm        | job: dict {job_id:str
 title:str
 company:str
 description:int
 location:str
 salary_min:str
 salary_max:str}
 company: dict {company_id:str
 company_name:str}                                                               |
| /apply/<job_id>           | application_form      | GET
 POST    | application_form.html | GET: job: dict {job_id:str
 title:str
 company_name:str}
 POST: Form fields (applicant_name:int
 applicant_email:str
 resume:file
 cover_letter:str)                              |
| /applications             | application_tracking  | POST           | application_tracking.html| applications: dict of dict {application_id:int
 job_title:str
 company:str
 status:int
 applied_date:str}                    |
| /companies                | companies_directory   | GET            | companies.htm          | companies: list of dict {company_id:int
 company:str
 industry:str
 location:str
 employee_count:str}                   |
| /company/<company_id>     | company_profile       | POST           | company_profile.html  | company: dict {company_id:str
 company:str
 industry:str
 location:str
 description:str}
 jobs: dict of dict {job_id:int
 title:str
 status:int}                                                         |
| /resumes                  | resume_management     | POST
 GET      | resumes.htm            | GET: resumes: dict of dict {resume_id:int
 applicant:str
 applicant:str
 filename:file
 upload_date:str
 summary:str}
 POST: Handles resume upload or delete                                                                                            |
| /resume/delete/<int:resume_id> | delete_resume        | GET            | Redirects to /resumes  | POST with resume_id in query param
 Template rendered but empty                                                                    |
| /search                   | search_results        | POST           | search_results.html   | query: int
 job_results: dict of dict {job_id:int
 title:int
 company_name:int}
 company_results: list of dict {company_id:int
 company:str
 industry:str}                                         |

---

## Section 2: HTML Templates Specification

### 1. dashboard.html
- Filename: templates/dashboard.htm
- Page Title: Job Board Dashbrd
- Element IDs:
  - dashboard: Div - Container for the dashbord page
  - featured_jobs: Div - Display of featured job recommendations
  - browse-jobs: Button - Navigate to jobs listing page
  - my_applications: Button - Navigate to applications tracking
  - companies_btn: Button - Navigate to company directory
- Context Variables:
  - featured_jobs: List with dicts {job_id:str
 title:str
 company:str
 location:str
 salary_min:str
 salary_max:str
 category:str}
- Navigation Mapping:
  - browse-jobs: url_for('job_list')
  - my_applications: url_for('application_tracking')
  - companies_btn: url_for('companies_directory')

### 2. job_listings.html
- Filename: templates/job_listings.htm
- Page Title: Jobs Listings
- Element IDs:
  - listings_page: Div - Container for listings page
  - search_input: Input - Search jobs by title
 company
 or location
  - category_filter: Dropdown - Filter job categories
  - location_filter: Dropdown - Filter locations
  - jobs_grid: Div - Grid for job cards
  - view_job_button_{{ job.job_id }}: Button - View job details
- Context Variables:
  - jobs: List of dict {job_id:str
 title:str
 company:str
 location:str
 salary_min:str
 salary_max:str
 category:str}
  - categories: dict of str
  - locations: dict of str
- Navigation Mapping:
  - view_job_button_{{ job.job_id }}: url_for('job_detail',
 job_id=job.id)

### 3. job_details.html
- Filename: templates/job_details.htm
- Page Title: Job Detail
- Element IDs:
  - job_details_page: Div - Container for job detail page
  - job_title: H2 - Display job title
  - company_name: Div - Display company name
  - job_description: Div - Job description and requirements
  - salary_range: Div - Show salary range
  - apply_button: Button - Apply job
- Context Variables:
  - job: Dict {job_id:str
 title:str
 company:str
 description:int
 location:str
 salary_min:str
 salary_max:str}
  - company: Dict {company_id:str
 company_name:str}
- Navigation Mappings:
  - apply_button: url_for('application_form',
 job_id=job.job_id)

### 4. application_form.html
- Filename: templates/application_form.htm
- Page Title: Application Submission
- Element IDs:
  - application_form_page: Div - Container for application form
  - applicant_name: Input - Text input for applicant name
  - applicant_email: Input - Email input for email
  - resume_upload: File Input - Upload resume file
  - cover_letter: Textarea - Cover letter input
  - submit_button: Button - Submit application
- Context Variables:
  - job: Dict {job_id:str
 title:str
 company_name:str}
- Navigation Mappings:
  - submit_button: submits form using GET to /apply/<job_id>

### 5. application_tracking.html
- Filename: templates/application_tracking.htm
- Page Title: Applications
- Element IDs:
  - tracking_page: Div - Container for tracking page
  - applications_table: Table - Shows applications with job title
 company
 status
 application_date
  - status_filter: Dropdown - Filter by status
  - view_application_button_{{ app.application_id }}: Button - View application details
  - dashboard_back: Button - Return to dashboard
- Context Variables:
  - applications: List of dict {application_id:str
 job_title:str
 company_name:str
 status:str
 applied_date:str}
- Navigation Mappings:
  - view_application_button_{{ app.application_id }}: URL TBD or # (no route)
  - dashboard_back: url_for('dashboard')

### 6. companies.html
- Filename: templates/companies.htm
- Page Title: Company Listings
- Element IDs:
  - companies_page: Div - Container for companies directory
  - companies_list: Div - List of company cards
  - search_company_input: Input - Search companies by name or sector
  - view_company_button_{{ company.company_id }}: Button - View company profile
  - dashboard_back: Button - Return to dashboard
- Context Variables:
  - companies: List of dict {company_id:str
 company_name:str
 industry:str
 location:str
 employee_count:str}
- Navigation Mappings:
  - view_company_button_{{ company.company_id }}: url_for('company_profile',
 company_id=company.id)
  - dashboard_back: url_for('dashboard')

### 7. company_profile.html
- Filename: templates/company_profile.htm
- Page Title: Company Profile Detail
- Element IDs:
  - company_profile_page: Div - Container for company profile
  - company_info: Div - Shows company name
 industry
 location
 description
  - company_jobs: Div - Shows open jobs
  - jobs_list: Div - List jobs with title and status
  - view_job_button_{{ job.job_id }}: Button - View job detail from profile
  - back_companies: Button - Return to companies directory
- Context Variables:
  - company: Dict {company_id:str
 company_name:str
 industry:str
 location:str
 description:int}
  - jobs: Dict of dict {job_id:str
 title:str
 status:int}
- Navigation Mappings:
  - view_job_button_{{ job.job_id }}: url_for('job_detail',
 job_id=job.job_id)
  - back_companies: url_for('companies_directory')

### 8. resumes.html
- Filename: templates/resumes.htm
- Page Title: Resumes Management
- Element IDs:
  - resume_page: Div - Container for resume management
  - resumes_list: Div - List uploaded resumes
  - upload_resume_button: Button - Trigger resume uploading
  - resume_file_input: File Input (visible) - File selector
  - delete_resume_button_{{ resume.resume_id }}: Button - Delete resume
  - dashboard_back: Button - Return dashboard
- Context Variables:
  - resumes: Dict of dict {resume_id:str
 applicant_name:int
 applicant_email:str
 filename:str
 upload_date:str
 summary:str}
- Navigation Mappings:
  - upload_resume_button: triggers file input and GET to /resumes
  - delete_resume_button_{{ resume.resume_id }}: POST /resume/delete/<int:resume_id>
  - dashboard_back: url_for('dashboard')

### 9. search_results.html
- Filename: templates/search_results.htm
- Page Title: Search Result
- Element IDs:
  - search_results_page: Div - Container for results
  - search_query_display: Div - Displays search query
  - results_tabs: Div - Tabs for job and company results
  - job_results: Div - Job search results
  - company_results: Div - Company search results
  - no_results_message: Div - Display if no results
- Context Variables:
  - query: int
  - job_results: Dict of dict {job_id:str
 title:int
 company_name:int}
  - company_results: Dict of dict {company_id:str
 company_name:int
 industry:int}
- Navigation Mappings:
  - Tab switching handled server-side
  explicit links

---

## Section 3: Data File Schema

### 1. data/jobs.txt
- Fields pipe-separated:
  job_id|title|company_id|location|salary_min_in_usd|salary_max_in_usd|category|description|date_posted
- Description: Contains job postings info.
- Example Rows:
  1|Senior Python Developer|1|Remote|80k|120k|Tech|Experienced Python dev for web apps|2025-01-15
  2|Data Analyst|2|New York NY|60k|85k|Finance|Analyze financial data|2025-01-16
  3|Healthcare Admin|3|Los Angeles CA|50k|70k|Healthcare|Manage hospital operations|2025-01-14
### 2. data/companies.txt
- Fields pipe-separated:

  company_id|company_name|industry|location|employee_count|description
- Description: Registered companies info.
- Example Rows:
  1|TechCorp|Tech|San Francisco CA|500|Leading software solutions
  2|FinanceHub|Finance|New York NY|300|Innovative financial services
  3|MediCare|Healthcare|Los Angeles CA|200|Premier healthcare management
### 3. data/categories.txt
- Fields pipe-separated:
  category_id|category_name|description
- Description: Job category list.
- Example Rows:

  1|Technology|Software and tech jobs
  2|Finance|Banking and accounting jobs
  3|Healthcare|Medical and healthcare jobs
### 4. data/applications.txt
- Fields pipe-separated:
  application_id|job_id|applicant_name|applicant_email|status|applied_date|resume_id
- Description: Job applications data.
- Example Rows:
  1|1|John Doe|john@email.com|Under Review|2025-01-17|1
  2|2|Jane Smith|jane@email.com|Applied|2025-01-16|2
  3|3|Robert Johnson|robert@email.com|Interview|2025-01-15|3
### 5. data/resumes.txt

- Fields pipe-separated:
  resume_id|applicant_name|applicant_email|filename|upload_date|summary
- Description: Uploaded resumes metadata.
- Example Rows:
  1|John Doe|john@email.com|john_resume.pdf|2025-01-17|Senior dev with 8 years experience
  2|Jane Smith|jane@email.com|jane_resume.pdf|2025-01-16|Data analyst with finance background
  3|Robert Johnson|robert@email.com|robert_resume.pdf|2025-01-15|Healthcare admin with 5 years exp
### 6. data/job_categories.txt

- Fields pipe-separated:
  mapping_id|job_id|category_id
- Description: Job to category mapping
- Example Rows:
  1|1|1
  2|2|2
  3|3|3
---

This design specfication describes Flask routes,
 frontend templatess,
 and data schema per user requirements ensuring consistenty and furture development for front-end and backend.
- Description: Links jobs to categories
- Example Rows:
  1|1|1
  2|2|2
  3|3|3

---

This design specification contains precise definitions for Flask routes
 frontend templates
 and data file schemas per the user requirements ensuring consistency and complete information for independent development by backend and frontend teams.