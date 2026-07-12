Web Application Design Specification



Routes

Path Function Name HTTP | Context Passed | |

`/` | | (Redirect) None | N/A
GET (each job (int), company_name location salary_min (int), (int))
| | list (int), (str), (int), salary_max


search_query:
category_filter: str
|
`/job/<int:job_id>` | job_details | | job: with (job_id company_name (str), location (str), salary_max (int), category (str), | N/A |
| GET, | GET: job: dict
For POST: form no rendering validation Context dict success (str), resume_file (file), |
`/applications` application_tracking | GET | application_tracking.html applications: list (application_id company_name (str), applied_date
|
| | | (str), applicant_name (str), resume_id (int), cover_letter (str,
| `/companies` | | | companies.html | of (company_id (str), industry (str),
search_query: str | N/A
| | | (str), (str), employee_count (str))
list (job_id (int), (str or 'Open'))| N/A
resume_management GET resumes.html | resumes: (int), applicant_name (str), filename upload_date (str), summary
N/A (redirects error) resume_file (file (str), applicant_email
| | (redirects or |
`/search` | search_results GET | (search
of (job_id, title, company_name, location,
company_results: (company_id,
bool | N/A



# Section Template Specifications

###

Title**: Job Dashboard
- **Element IDs and
- container for
Div displaying
to to listings
- Button navigate applications page.
- to
- **Context Variables**:
dict with
(int)
- `title`
(str)
`location`
(int)
- (int)
- **Navigation
- `browse-jobs-button`:
- `my-applications-button`:




###
**Filename**: templates/job_listings.html
- **Page
- **Element IDs
- `listings-page`: Div for the listings
`search-input`: Input field to title, company, or location.
Dropdown category.
- `location-filter`:
container displaying job
Dynamic: `view-job-button-{{ job.job_id }}`: Button job job
- **Context
- of keys:
`job_id` (int)

- (str)
-
(int)
- (int)


- `locations`: List (location names)
string
- category
- `location_filter`: str
Mappings**:
- Each

---

3.
- **Filename**: templates/job_details.html
Details
- IDs
`job-details-page`: the job details page.
- job
`company-name`: displaying
Div full

to

- with
`job_id`
- (str)
- `company_name` (str)
(str)
`salary_min`
- (int)
(str)
`description`
**Navigation




4. application_form.html
**Filename**:
- Title**: Application
IDs
container
- `applicant-name`: for name.
- field
File field upload
- `cover-letter`:
`submit-application-button`: the
Variables**:
- job details as job_details.html
`errors`: field to error
- Str to
**Navigation Mappings**:
be link.




templates/application_tracking.html
-
-
`tracking-page`:
- displaying with columns: date applied.
- `status-filter`: filter
to view application
- to navigate to
- **Context
List with
`application_id`

`company_name`
`status`
yyyy-mm-dd)
`status_filter`: str indicating
- **Navigation Mappings**:
url_for('application_details', application_id=application.application_id)
url_for('dashboard')



###
templates/companies.html
- **Page Company Directory
**Element and Descriptions**:
for companies
company
- Input to search industry.
Dynamic: on company card to profile.
`back-to-dashboard`: Button to navigate dashboard.
-
`companies`: List dict with keys:
`company_id`
`company_name`

`employee_count`
str for current search query
**Navigation Mappings**:
- company_id=company.company_id)
-



7.
- **Filename**:
- Profile
Descriptions**:
Div for the company
- Div industry, and description.
for company.
- `jobs-list`: container listing with status
Button to view job
- `back-to-companies`: navigate company
**Context
with

- (str)
-
(str)
(int)

- `jobs`: List of dict with keys:
-
`title`
- (Usually
- Mappings**:
- job_id=job.job_id)




### resumes.html
- templates/resumes.html
- Title**: Resumes
IDs and
- container the
- resumes.
to file for uploading
file element upload.
Button resume.
`back-to-dashboard`: back to

-

`applicant_name`
- `applicant_email` (str)
`filename`


**Navigation
`upload-resume-button`: input POST to route
POST to route with resume_id




search_results.html
**Filename**:
**Page
**Element IDs
- `search-results-page`: Div
search string.
`results-tabs`: tabs switch between results and
results.
- `company-results`: container displaying search
- Div no found.

str search
dict with keys jobs
- List of to listing
if no
-
buttons linking url_for('job_details',
result have linking url_for('company_profile', company_id=company.company_id)

---

# 3: Data

data in Files have no lines.**

### jobs.txt
-


title (str)

location (str)
salary_min
(int)
category (str)
8. description (str)
9. posted_date (str
- Description**: Stores postings
Rows**:
```
Python for
2|Data Analyst|2|New financial and
Administrator|3|Los Angeles, hospital operations and records|2025-01-14



**File data/companies.txt
Field Order**:
1. (int)
2. (str)
3. (str)
(str)
5. employee_count (int)
(str)
**Data Stores company

```
1|TechCorp|Technology|San Francisco, solutions provider
2|FinanceHub|Finance|New York, services
Angeles, CA|200|Premier healthcare organization


###


1.

3. description
- Description**: Stores for classifying
- **Example
```
1|Technology|Software, IT,
accounting, and
and industry positions
```

applications.txt
Path**: data/applications.txt
-

2. (int)

(str)
5. status (str) [Examples: Applied, Under Interview, Rejected]
6.
(int)
**Data Description**: Stores job

```
1|1|John Review|2025-01-17|1


```

5.
- **File
Field
1. resume_id (int)
applicant_name (str)
applicant_email (str)
filename (str) - Resume name
upload_date YYYY-MM-DD)
summary qualifications
- **Data uploaded metadata.


1|John with years experience
Smith|jane@email.com|jane_resume.pdf|2025-01-16|Data with
administrator with 5
```


- Path**:
**Pipe-delimited
mapping_id (int)

(int)
- **Data Maps job for
- **Example Rows**:
```
1|1|1




---

Design Specification
