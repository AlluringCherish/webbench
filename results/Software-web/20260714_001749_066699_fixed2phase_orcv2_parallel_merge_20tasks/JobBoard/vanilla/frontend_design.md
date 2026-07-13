# Frontend Design Specification for JobBoard

---

## 1. Dashboard Page

### Page Title
- Job Board Dashboard

### Container Div
- **ID:** dashboard-page
  - Type: Div
  - Role: Main container for the dashboard page

### Elements
- **ID:** featured-jobs
  - Type: Div
  - Role: Displays featured job recommendations

- **ID:** browse-jobs-button
  - Type: Button
  - Role: Navigates to Job Listings page
  - Text: "Browse Jobs"

- **ID:** my-applications-button
  - Type: Button
  - Role: Navigates to Application Tracking page
  - Text: "My Applications"

- **ID:** companies-button
  - Type: Button
  - Role: Navigates to Companies Directory page
  - Text: "Companies"

### Layout Structure
- `dashboard-page` is the main wrapper
- `featured-jobs` section prominently displayed
- Navigation buttons grouped logically (e.g., in a nav div or section)

### Navigation Flow
- browse-jobs-button -> Job Listings Page
- my-applications-button -> Application Tracking Page
- companies-button -> Companies Directory Page

---

## 2. Job Listings Page

### Page Title
- Job Listings

### Container Div
- **ID:** listings-page
  - Type: Div
  - Role: Main container

### Elements
- **ID:** search-input
  - Type: Input (text)
  - Role: Search by job title, company, or location

- **ID:** category-filter
  - Type: Dropdown
  - Role: Filter jobs by category (e.g., Technology, Finance, Healthcare)

- **ID:** location-filter
  - Type: Dropdown
  - Role: Filter jobs by location (Remote, On-site, Hybrid)

- **ID:** jobs-grid
  - Type: Div (flex/grid layout)
  - Role: Container for job cards

- **ID pattern:** view-job-button-{job_id}
  - Type: Button
  - Role: Trigger viewing job details
  - Dynamic per job card

### Layout Structure
- Search and filter controls aligned top
- `jobs-grid` below filters showing card summaries
- Each job card is a sub-container with job info and a view button

### Navigation Flow
- view-job-button-{job_id} -> Job Details Page

---

## 3. Job Details Page

### Page Title
- Job Details

### Container Div
- **ID:** job-details-page
  - Type: Div
  - Role: Main container for job detail content

### Elements
- **ID:** job-title
  - Type: H1
  - Role: Display the job title

- **ID:** company-name
  - Type: Div
  - Role: Display company name

- **ID:** job-description
  - Type: Div
  - Role: Detailed job description and requirements

- **ID:** salary-range
  - Type: Div
  - Role: Salary range display

- **ID:** apply-now-button
  - Type: Button
  - Role: Opens Application Form Page
  - Text: "Apply Now"

### Layout Structure
- Vertical stack: title at top, company below, description and salary, then apply button

### Navigation Flow
- apply-now-button -> Application Form Page

---

## 4. Application Form Page

### Page Title
- Submit Application

### Container Div
- **ID:** application-form-page
  - Type: Div
  - Role: Container for application form

### Elements
- **ID:** applicant-name
  - Type: Input (text)
  - Role: Enter applicant's full name

- **ID:** applicant-email
  - Type: Input (email)
  - Role: Enter applicant's email address

- **ID:** resume-upload
  - Type: File Input
  - Role: Upload resume file

- **ID:** cover-letter
  - Type: Textarea
  - Role: Enter cover letter text

- **ID:** submit-application-button
  - Type: Button
  - Role: Submit application
  - Text: "Submit Application"

### Layout Structure
- Form layout with labels and input fields grouped logically

---

## 5. Application Tracking Page

### Page Title
- My Applications

### Container Div
- **ID:** tracking-page
  - Type: Div
  - Role: Main container for applications tracking

### Elements
- **ID:** status-filter
  - Type: Dropdown
  - Role: Filter applications by status (All, Applied, Under Review, Interview, Rejected)

- **ID:** applications-table
  - Type: Table
  - Role: Displays applications with columns for job title, company, status, applied date

- **ID pattern:** view-application-button-{app_id}
  - Type: Button
  - Role: View application details

- **ID:** back-to-dashboard
  - Type: Button
  - Role: Navigate back to Dashboard
  - Text: "Back to Dashboard"

### Layout Structure
- Filter dropdown above table
- Table rows for each application with a view button
- Back to Dashboard button positioned accessibly

### Navigation Flow
- view-application-button-{app_id} -> Application Details (not specified page, assume modal or detail view)
- back-to-dashboard -> Dashboard Page

---

## 6. Companies Directory Page

### Page Title
- Company Directory

### Container Div
- **ID:** companies-page
  - Type: Div
  - Role: Main container for company listings

### Elements
- **ID:** search-company-input
  - Type: Input (text)
  - Role: Search companies by name or industry

- **ID:** companies-list
  - Type: Div
  - Role: Container listing company cards

- **ID pattern:** view-company-button-{company_id}
  - Type: Button
  - Role: View detailed company profile

- **ID:** back-to-dashboard
  - Type: Button
  - Role: Navigate back to Dashboard
  - Text: "Back to Dashboard"

### Layout Structure
- Search input on top
- Company cards below with info and view button
- Back to Dashboard button

### Navigation Flow
- view-company-button-{company_id} -> Company Profile Page
- back-to-dashboard -> Dashboard Page

---

## 7. Company Profile Page

### Page Title
- Company Profile

### Container Div
- **ID:** company-profile-page
  - Type: Div
  - Role: Container for detailed company information

### Elements
- **ID:** company-info
  - Type: Div
  - Role: Displays company name, industry, location, and description

- **ID:** company-jobs
  - Type: Div
  - Role: Container for open job listings from this company

- **ID:** jobs-list
  - Type: Div
  - Role: List of job titles with status indicators

- **ID pattern:** view-job-button-{job_id}
  - Type: Button
  - Role: View job details

- **ID:** back-to-companies
  - Type: Button
  - Role: Navigate back to Companies Directory
  - Text: "Back to Companies"

### Layout Structure
- Company information top section
- Jobs list below company info
- Button to go back in a visible location

### Navigation Flow
- view-job-button-{job_id} -> Job Details Page
- back-to-companies -> Companies Directory Page

---

## 8. Resume Management Page

### Page Title
- My Resumes

### Container Div
- **ID:** resume-page
  - Type: Div
  - Role: Container for managing resumes

### Elements
- **ID:** resumes-list
  - Type: Div
  - Role: Displays list of uploaded resumes with upload dates

- **ID:** upload-resume-button
  - Type: Button
  - Role: Trigger file input for uploading new resume
  - Text: "Upload New Resume"

- **ID:** resume-file-input
  - Type: File Input (hidden)
  - Role: Hidden input for selecting resume file

- **ID pattern:** delete-resume-button-{resume_id}
  - Type: Button
  - Role: Delete corresponding resume

- **ID:** back-to-dashboard
  - Type: Button
  - Role: Navigate back to Dashboard
  - Text: "Back to Dashboard"

### Layout Structure
- Resumes list displayed clearly
- Upload button above or near list
- Back button accessibly placed

### Navigation Flow
- upload-resume-button triggers resume-file-input click
- delete-resume-button-{resume_id} deletes a resume
- back-to-dashboard -> Dashboard Page

---

## 9. Search Results Page

### Page Title
- Search Results

### Container Div
- **ID:** search-results-page
  - Type: Div
  - Role: Container for search results

### Elements
- **ID:** search-query-display
  - Type: Div
  - Role: Displays the user's search query

- **ID:** results-tabs
  - Type: Div
  - Role: Tabs component to switch between job results and company results

- **ID:** job-results
  - Type: Div
  - Role: Display search results for jobs

- **ID:** company-results
  - Type: Div
  - Role: Display search results for companies

- **ID:** no-results-message
  - Type: Div
  - Role: Show message when no results found

### Layout Structure
- Search query displayed at top
- Tabs below to toggle results
- Only one results div visible at a time
- No-results-message shown if no matches

---

## Accessibility and Usability Considerations

- Consistent ID naming with lowercase and hyphens.
- Dynamic IDs use curly-brace style placeholders (e.g., {job_id}) for clarity.
- All interactive elements (buttons, inputs, dropdowns) placed distinctly separated from display-only areas.
- Navigation buttons clearly labeled with descriptive text.
- Empty states like "no-results-message" must be designed for search results and filtered views.
- Use semantic HTML for titles (e.g., H1 for job-title).
- Group related controls logically per page for ease of navigation.

---

# Summary
This design specifies all pages from Dashboard to Search Results with container divs, element IDs, types, usage, and navigation flows, strictly based on the given user requirements. The UI elements and page structures are designed for straightforward frontend implementation.
