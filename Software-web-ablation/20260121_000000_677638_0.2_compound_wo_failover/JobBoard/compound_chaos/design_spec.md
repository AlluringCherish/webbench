# JobBoard Application Design Specification

## Overview
This document details the Flask web application 'JobBoard' which enables users to browse jobs, view companies, track their applications, and manage resumes in a healthcare, technology, and finance job market environment. The app employs multiple templates rendered via Jinja2 and follows strict naming conventions and UI element IDs to facilitate developers.

---

## 1. Data Files (TXT Format)
The data files reside in a local 'data/' directory and use pipe-delimited formats for storage:

- `jobs.txt`: Stores job postings with fields:
  - `job_id|title|company_id|location|salary_min|salary_max|category|description|posted_date`

- `companies.txt`: Stores companies with fields:
  - `company_id|company_name|industry|location|employee_count|description`

- `categories.txt`: Stores job categories with fields:
  - `category_id|category_name|description`

- `applications.txt`: Tracks user applications with fields:
  - `application_id|job_id|applicant_name|applicant_email|status|applied_date|resume_id`

- `resumes.txt`: Stores resumes uploaded by users:
  - `resume_id|applicant_name|applicant_email|filename|upload_date|summary`

All files use straight pipe delimiter `|`. Dates format: `YYYY-MM-DD`.

---

## 2. Flask Routes and HTTP Methods

### Frontend Routes

- `/` [GET]
  - Renders the **dashboard.html** page showing summary widgets and navigation buttons.
  - Context variables:
    - `jobs` (list of job dicts),
    - `companies` (list of company dicts),
    - `applications` (list of application dicts),
    - `resumes` (list of resume dicts)

- `/jobs` [GET]
  - Renders **jobs-list.html** page.
  - Context variables:
    - `jobs` (filtered or all),
    - `categories` (all job categories),
    - `selected_category` (optional, int or None),
    - `location_filter` (optional string)

- `/job/<int:job_id>` [GET]
  - Renders **job-details-page.html**.
  - Context variables:
    - `job` (single job dict),
    - `company` (dict of associated company),
    - `category` (category dict)

- `/companies` [GET]
  - Renders **companies-page.html**.
  - Context variables:
    - `companies` (list of companies)

- `/company/<int:company_id>` [GET]
  - Renders **company-profile-page.html**.
  - Context variables:
    - `company` (dict),
    - `jobs` (list of job dict for company)

- `/applications` [GET]
  - Renders **applications-list.html**.
  - Context variables:
    - `applications` (all applications for user),
    - `jobs` (dict keyed by job_id),
    - `resumes` (dict keyed by resume_id)

- `/application/<int:application_id>` [GET]
  - Renders **application-details-page.html**.
  - Context variables:
    - `application` (dict),
    - `job` (dict),
    - `resume` (dict)

- `/resumes` [GET]
  - Renders **resumes-list.html**.
  - Context variables:
    - `resumes` (list of resumes)

- `/upload_resume` [POST]
  - Handles resume file upload form submission.

- `/apply/<int:job_id>` [POST]
  - Handles job application submission.

- `/delete_resume/<int:resume_id>` [POST]
  - Deletes resume specified.


## 3. Navigation Elements and IDs

The app uses a consistent set of container IDs and button/element IDs in HTML templates to facilitate frontend manipulation and backend referencing.

### Navigation Buttons

- `back-to-dashboard` (Button): Returns to dashboard `/`
- `browse-jobs-button` (Button): Navigate to `/jobs`
- `companies-button` (Button): Navigate to `/companies`
- `my-applications-button` (Button): Navigate to `/applications`
- `upload-resume-button` (Button): Opens resume upload form

### Search and Filters

- `search-input` (Input text): Keyword search for jobs or companies
- `category-filter` (Dropdown select): Filters jobs by category
- `location-filter` (Input text): Filter jobs by location
- `status-filter` (Dropdown select): Filter applications by status

### Listings and Tables

- `jobs-list` (Container Div): Holds grid/list of job cards
- `job-results` (Div): Detailed job search results container
- `companies-list` (Div): List companies
- `applications-table` (Table): Lists all user applications
- `resumes-list` (Table or Div): Lists resumes for user

### Dynamic Buttons (Each render)

- `view-job-button-{job_id}` (Button): View details of a specific job
- `apply-now-button-{job_id}` (Button): Submit application for job
- `view-company-button-{company_id}` (Button): View company profile
- `view-application-button-{application_id}` (Button): View application details
- `delete-resume-button-{resume_id}` (Button): Deletes the given resume


## 4. HTML Templates Spec (File, Title, IDs, Context Variables)

### 4.1 dashboard.html
- Title: "JobBoard Dashboard"
- H1: "Dashboard"
- IDs:
  - Container: `dashboard-page`
  - Buttons: `browse-jobs-button`, `companies-button`, `my-applications-button`, `upload-resume-button`, `back-to-dashboard`
  - Display Divs: e.g., summary widgets (IDs optional, e.g., `featured-jobs` etc.)
- Context:
  - `jobs`: List[dict], 
  - `companies`: List[dict],
  - `applications`: List[dict],
  - `resumes`: List[dict]
- Navigation:
  - Buttons use url_for linked to `jobs_list`, `companies_list`, `applications_list`, and upload handlers.

### 4.2 jobs-list.html
- Title: "Job Listings"
- H1: "Available Jobs"
- IDs:
  - `search-input` (Input text),
  - `category-filter` (Dropdown),
  - `location-filter` (Input text),
  - `jobs-list` (Div container for job cards),
  - Dynamic buttons: `view-job-button-{{ job.job_id }}`, `apply-now-button-{{ job.job_id }}`
- Context:
  - `jobs`: List[dict],
  - `categories`: List[dict],
  - `selected_category`: int or None,
  - `location_filter`: str or None
- Navigation:
  - Buttons href from url_for('job_details', job_id=job.job_id)

### 4.3 job-details-page.html
- Title: "Job Details - {{ job.title }}"
- H1: "{{ job.title }}"
- IDs:
  - `job-title`, `job-description`, `company-info`,
  - Button: `apply-now-button-{{ job.job_id }}`
- Context:
  - `job`: dict,
  - `company`: dict,
  - `category`: dict
- Navigation:
  - Apply button posts to `/apply/{{ job.job_id }}`

### 4.4 companies-page.html
- Title: "Companies"
- H1: "Company Directory"
- IDs:
  - `companies-list` (Div)
  - Buttons: `view-company-button-{{ company.company_id }}` for each company
- Context:
  - `companies`: List[dict]
- Navigation:
  - Company buttons link with url_for('company_profile', company_id=company.company_id)

### 4.5 company-profile-page.html
- Title: "Company Profile - {{ company.company_name }}"
- H1: "{{ company.company_name }}"
- IDs:
  - `company-info` (Div),
  - `company-jobs` (Div) listing jobs,
  - Buttons: `view-job-button-{{ job.job_id }}` for jobs
- Context:
  - `company`: dict,
  - `jobs`: List[dict]
- Navigation:
  - Job buttons link to job details page

### 4.6 applications-list.html
- Title: "My Applications"
- H1: "Applications"
- IDs:
  - `applications-table` (Table),
  - Buttons: `view-application-button-{{ application.application_id }}`
- Context:
  - `applications`: List[dict],
  - `jobs`: Dict[job_id -> dict],
  - `resumes`: Dict[resume_id -> dict]

### 4.7 application-details-page.html
- Title: "Application Detail"
- H1: "Application for {{ job.title }}"
- IDs:
  - `application-details` (Div container),
  - Button: `back-to-dashboard`
- Context:
  - `application`: dict,
  - `job`: dict,
  - `resume`: dict

### 4.8 resumes-list.html
- Title: "My Resumes"
- H1: "Resumes"
- IDs:
  - `resumes-list` (Table or Div),
  - Buttons: `delete-resume-button-{{ resume.resume_id }}`
- Context:
  - `resumes`: List[dict]

### 4.9 application-form-page.html
- Title: "Apply for {{ job.title }}"
- H1: "Apply for {{ job.title }}"
- IDs:
  - Form fields: `resume-file-input`, `cover-letter`, `submit-application-button`
  - Dropdown/select to choose existing resumes
- Context:
  - `job`: dict,
  - `resumes`: List[dict]

---

## 5. Example Button and Link Navigation (url_for usage)

- Browse jobs button in dashboard.html:
  ```html
  <button id="browse-jobs-button" onclick="location.href='{{ url_for('jobs_list') }}'">Browse Jobs</button>
  ```

- View job button in jobs-list.html:
  ```html
  <a id="view-job-button-{{ job.job_id }}" href="{{ url_for('job_details', job_id=job.job_id) }}">View</a>
  ```

- Apply now button in job-details-page.html:
  ```html
  <form method="post" action="{{ url_for('apply_job', job_id=job.job_id) }}">
    <button id="apply-now-button-{{ job.job_id }}" type="submit">Apply Now</button>
  </form>
  ```

- View company button in companies-page.html:
  ```html
  <a id="view-company-button-{{ company.company_id }}" href="{{ url_for('company_profile', company_id=company.company_id) }}">Details</a>
  ```

- View application button in applications-list.html:
  ```html
  <a id="view-application-button-{{ application.application_id }}" href="{{ url_for('application_details', application_id=application.application_id) }}">View</a>
  ```

- Delete resume button in resumes-list.html:
  ```html
  <form method="post" action="{{ url_for('delete_resume', resume_id=resume.resume_id) }}">
    <button id="delete-resume-button-{{ resume.resume_id }}" type="submit">Delete</button>
  </form>
  ```

---

## 6. Summary Table of Element IDs and Descriptions

| ID Pattern                       | Element Type | Description                                   |
|--------------------------------|--------------|-----------------------------------------------|
| dashboard-page                 | Div Container| Main dashboard container                      |
| back-to-dashboard              | Button       | Navigate to root dashboard                     |
| browse-jobs-button            | Button       | Navigate to jobs list page                      |
| companies-button              | Button       | Navigate to companies list page                 |
| my-applications-button        | Button       | Navigate to user's applications list page     |
| upload-resume-button          | Button       | Trigger resume upload form                      |
| search-input                  | Input text   | Search query input                             |
| category-filter               | Dropdown     | Job category filter                            |
| location-filter               | Input text   | Job location filter                            |
| jobs-list                    | Div          | Container for the job cards                     |
| view-job-button-{job_id}     | Button/link  | View details page for job with job_id          |
| apply-now-button-{job_id}    | Button       | Submit application for job with job_id         |
| companies-list               | Div          | Container listing all companies                 |
| view-company-button-{company_id} | Button/link  | View company profile with company_id           |
| applications-table           | Table        | Table listing all user applications             |
| view-application-button-{application_id} | Button/link  | View application detail with application_id    |
| resumes-list                 | Div/Table    | Container listing uploaded resumes              |
| delete-resume-button-{resume_id} | Button       | Delete resume with resume_id                    |
| resume-file-input            | Input (file) | Resume file input in application form          |
| cover-letter                 | Textarea     | Cover letter input field for applications      |
| submit-application-button    | Button       | Submit application form                         |

---

This specification comprehensively covers backend routes, data schemas, page context variables, and UI element IDs for developers building or maintaining the JobBoard Flask application.