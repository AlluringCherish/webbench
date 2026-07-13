# Unified Design Specification for OnlineCourse Web Application

---

# Section 1: Integrated Flask Routes and API Contracts

### 1. `/dashboard`
- **Methods:** GET
- **Description:** Loads the Learning Dashboard page.
- **Request Parameters:** Uses session to identify current logged-in user.
- **Response:** JSON including:
  - `username` (string): current user's username
  - `fullname` (string): full name for welcome message
  - `enrolled_courses` (list): each course with fields { `course_id`, `title`, `progress` (0-100) }
- **Frontend Template:** dashboard.html
- **Frontend Elements:** 
  - `dashboard-page` (Div) container
  - `welcome-message` (H1) display user's fullname
  - `enrolled-courses` (Div) shows user's enrolled courses and progress
  - Navigation buttons: `browse-courses-button` (to `/courses/catalog`), `my-courses-button` (to `/my-courses`)

---

### 2. `/courses/catalog`
- **Methods:** GET
- **Request Parameters:** Optional query string `search` for filtering courses by title or category
- **Response:** JSON list of active courses matching the query, each with fields { `course_id`, `title`, `description`, `category`, `level`, `duration` }
- **Frontend Template:** catalog.html
- **Frontend Elements:** 
  - `catalog-page` (Div) container
  - `search-input` (Input) for user to enter search filter
  - `course-grid` (Div) to display multiple course cards
  - Each course card includes `view-course-button-{course_id}` (Button) to navigate to course details
  - `back-to-dashboard` (Button) to navigate back to dashboard

---

### 3. `/courses/<int:course_id>`
- **Methods:** GET
- **Request Parameters:** None
- **Response:** JSON with detailed course info:
  - `course_id`, `title`, `description`, `syllabus` (placeholder, can be empty or static text)
- **Frontend Template:** course_details.html
- **Frontend Elements:**
  - `course-details-page` (Div) container
  - `course-title` (H1)
  - `course-description` (Div)
  - `enroll-button` (Button): Enabled if not enrolled, else disabled and showing "Already Enrolled"
  - `back-to-catalog` (Button) to return to course catalog
- **POST Endpoint:** `/courses/<int:course_id>/enroll`
  - Enrolls user in course
  - Request uses session username
  - Response JSON: { status: "success" or error message }
  - Enrollment creates new record in enrollments.txt

---

### 4. `/my-courses`
- **Methods:** GET
- **Request Parameters:** Uses session username
- **Response:** JSON list of enrolled courses, each with { `course_id`, `title`, `progress` }
- **Frontend Template:** my_courses.html
- **Frontend Elements:** 
  - `my-courses-page` (Div) container
  - `courses-list` (Div) displaying courses with progress
  - For each enrolled course, button `continue-learning-button-{course_id}` to start or continue learning
  - `back-to-dashboard` (Button)

---

### 5. `/course/<int:course_id>/learning`
- **Methods:** GET
- **Request Parameters:** Uses session username
- **Response:** JSON object containing:
  - `lessons` (list): Each lesson with number and title
  - `completed_lessons` (list of lesson numbers completed)
  - `current_lesson` content
- **Frontend Template:** course_learning.html
- **Frontend Elements:** 
  - `learning-page` (Div) container
  - `lessons-list` (Div) showing all lessons
  - `lesson-content` (Div) showing current lesson content
  - `mark-complete-button` (Button): Enabled only if previous lessons completed
  - `back-to-my-courses` (Button)

### POST Endpoint: `/course/<int:course_id>/learning/mark-complete`
- **Methods:** POST
- **Request Parameters:** uses session username, body param `lesson_number` (int)
- **Response:** { status: "success" or error, updated_progress: int }
- **Business Logic:** :
  - Validates sequential completion
  - Updates enrollments.txt progress value
  - If progress == 100%, status updated to "Completed" in enrollments.txt
  - Triggers certificate creation in certificates.txt if none exists

---

### 6. `/assignments`
- **Methods:** GET
- **Request Parameters:** Uses session username
- **Response:** JSON list assignments for enrolled courses with submission status
- **Frontend Template:** my_assignments.html
- **Frontend Elements:** 
  - `assignments-page` (Div) container
  - `assignments-table` (Table) showing all assignments
  - For each assignment: `submit-assignment-button-{assignment_id}` (Button) to submit
  - `back-to-dashboard` (Button)

---

### 7. `/assignments/<int:assignment_id>/submit`
- **Methods:** POST
- **Request Parameters:** uses session username; body param `submission_text` (string)
- **Response:** { status: "success" or error }
- **Frontend Template:** submit_assignment.html
- **Frontend Elements:**
  - `submit-page` (Div) container
  - `assignment-info` (Div): displays assignment title and description
  - `submission-text` (Textarea) for input
  - `submit-button` (Button) to submit
  - `back-to-assignments` (Button)
- **Business Logic:** Validates enrollment, creates submission in submissions.txt

---

### 8. `/certificates`
- **Methods:** GET
- **Request Parameters:** Uses session username
- **Response:** JSON list of certificates for courses completed
- **Frontend Template:** certificates.html
- **Frontend Elements:**
  - `certificates-page` (Div) container
  - `certificates-grid` (Div) with earned certificates
  - `back-to-dashboard` (Button)

---

### 9. `/profile`
- **Methods:** GET, POST
  - GET: Returns user profile data
  - POST: Updates user profile (email, fullname)
- **Request Parameters:** Uses session username
- **Response:** JSON { status: "success" or "error", profile data }
- **Frontend Template:** profile.html
- **Frontend Elements:**
  - `profile-page` (Div) container
  - `profile-email` (Input)
  - `profile-fullname` (Input)
  - `update-profile-button` (Button)
  - `back-to-dashboard` (Button)

---

### Session and Authorization
- All routes require logged-in user with `username` in session
- Unauthorized access redirects or returns errors (implementation detail)

---

# Section 2: Combined HTML Template Specifications

### 1. Dashboard Page (dashboard.html)
- Container Div: `dashboard-page`
- Header H1: `welcome-message` displays user's full name
- Div `enrolled-courses` lists enrolled courses with progress bars or numeric progress
- Buttons:
  - `browse-courses-button`: navigates to `/courses/catalog`
  - `my-courses-button`: navigates to `/my-courses`

### 2. Course Catalog Page (catalog.html)
- Container Div: `catalog-page`
- Input: `search-input` for filtering courses
- Div: `course-grid` showing course cards (title, short description)
- Each course card includes button with id `view-course-button-{course_id}` to view details
- Button: `back-to-dashboard` returns to dashboard

### 3. Course Details Page (course_details.html)
- Container Div: `course-details-page`
- H1: `course-title`
- Div: `course-description` with full course description and syllabus placeholder
- Button: `enroll-button` to enroll (enabled if not enrolled, else disabled with label "Already Enrolled")
- Button: `back-to-catalog` returns to catalog

### 4. My Courses Page (my_courses.html)
- Container Div: `my-courses-page`
- Div: `courses-list` listing courses with progress
- Each course entry includes button `continue-learning-button-{course_id}` to enter course learning
- Button: `back-to-dashboard`

### 5. Course Learning Page (course_learning.html)
- Container Div: `learning-page`
- Div: `lessons-list` showing all lessons with indicators of completion
- Div: `lesson-content` showing current lesson content
- Button: `mark-complete-button` enabled only if prerequisite lessons completed
- Button: `back-to-my-courses`

### 6. My Assignments Page (my_assignments.html)
- Container Div: `assignments-page`
- Table: `assignments-table` listing assignments with due dates, status
- Each assignment row may have button `submit-assignment-button-{assignment_id}` if submission pending
- Button: `back-to-dashboard`

### 7. Submit Assignment Page (submit_assignment.html)
- Container Div: `submit-page`
- Div: `assignment-info` with assignment title and description
- Textarea: `submission-text`
- Button: `submit-button`
- Button: `back-to-assignments`

### 8. Certificates Page (certificates.html)
- Container Div: `certificates-page`
- Div: `certificates-grid` listing earned certificates by course and issue date
- Button: `back-to-dashboard`

### 9. User Profile Page (profile.html)
- Container Div: `profile-page`
- Inputs:
  - `profile-email` (email input)
  - `profile-fullname` (text input)
- Button: `update-profile-button`
- Button: `back-to-dashboard`

---

# Section 3: Data Schemas and Business Logic Summary

## Data File Schemas (pipe-delimited)

1. users.txt:
```
username|email|fullname
```

2. courses.txt:
```
course_id|title|description|category|level|duration|status
```

3. enrollments.txt:
```
enrollment_id|username|course_id|enrollment_date|progress|status
```

4. assignments.txt:
```
assignment_id|course_id|title|description|due_date|max_points
```

5. submissions.txt:
```
submission_id|assignment_id|username|submission_text|submit_date|grade|feedback
```

6. certificates.txt:
```
certificate_id|username|course_id|issue_date
```

## Business Logic

- Enrollment:
  - Prevent duplicate enrollments
  - On enrollment, add record with progress=0, status="In Progress", enrollment_date=current date

- Course Progress:
  - Completion of lessons must be sequential
  - Updating lessons updates progress percentage
  - On reaching 100%, mark enrollment status "Completed" and generate certificate if none exists

- Assignment Submission:
  - User can only submit assignments for courses they are enrolled in
  - New submission has submission_date current date, grade and feedback empty

- Certificates:
  - Created when course completed
  - Listed in certificates page

---

**End of Unified Design Specification**
