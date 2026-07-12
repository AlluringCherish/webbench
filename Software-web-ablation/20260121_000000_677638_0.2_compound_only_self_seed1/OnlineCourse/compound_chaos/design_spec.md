# Design Specification for 'OnlineCourse' Flask Web Application

---

## 1. Flask Routes Specification (for Backend Developers)

| Route Path                       | Function Name           | HTTP Methods  | Template File          | Context Variables Passed (name: type)                                                                                                             | Notes                                                                                                                                                      |
|---------------------------------|-------------------------|---------------|------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `/`                             | dashboard               | GET           | dashboard.html         | username: str, enrolled_courses: list of dict {course_id:str, title:str, description:str, duration:str, status:str, progress:int}                   | Displays dashboard page showing user's enrolled courses with progress summary.                                                                           |
| `/catalog`                      | catalog                 | GET           | catalog.html           | username: str, courses: list of dict {course_id:str, title:str, description:str, category:str, level:str, duration:str, status:str}                 | Displays catalog page listing all available courses with search functionality.                                                                           |
| `/course/<course_id>`           | course_details          | GET, POST     | course_details.html    | username: str, course: dict {course_id:str, title:str, description:str, category:str, level:str, duration:str, status:str},
 enroll_status: bool, already_enrolled: bool                           | GET shows course details with enroll option. POST enrolls user if not already enrolled;
Creates entry in enrollments.txt with 0% progress and current date.
Disabled button if already enrolled.
|
| `/my-courses`                   | my_courses              | GET           | my_courses.html        | username: str, enrolled_courses: list of dict {course_id:str, title:str, progress:int, status:str}                                                 | Displays user's enrolled courses list with progress and continue learning links.                                                                          |
| `/learn/<course_id>`            | course_learning         | GET, POST     | learning.html          | username: str, course: dict, lessons: list of dict {lesson_id:str, title:str, content:str}, current_lesson_id: str, completed_lessons: set of str, progress: int, enrollment: dict                    | GET displays course lesson contents, progress.
POST marks current lesson complete, updates enrollments.txt progress.
Automatically generates certificate at 100%.
Lessons must be completed sequentially. |
| `/assignments`                  | assignments             | GET           | assignments.html       | username: str, assignments: list of dict {assignment_id:str, course_id:str, title:str, description:str, due_date:str, max_points:int}                 | Displays assignments for enrolled courses with submit buttons for pending assignments.                                                                   |
| `/submit/<assignment_id>`       | submit_assignment       | GET, POST     | submit.html            | username: str, assignment: dict, previous_submission: dict or None                                                                                   | GET shows submission form.
POST saves submission data in submissions.txt with submission date, grade/status handled externally.
Confirmation displayed after POST.|
| `/certificates`                | certificates            | GET           | certificates.html      | username: str, certificates: list of dict {certificate_id:str, course_id:str, issue_date:str, course_title:str}                                     | Displays earned certificate cards for completed courses.                                                                                                |
| `/profile`                    | profile                 | GET, POST     | profile.html           | username: str, user_email: str, user_fullname: str                                                                                                   | GET shows profile with fields.
POST saves changes into users.txt.                                                                                       |

---

## 2. HTML Template Specifications (for Frontend Developers)

### 2.1 Template: `dashboard.html`
- Page Title: "Learning Dashboard"
- Container: `<div id="dashboard-page">`
- Elements:
  - `<h1 id="welcome-message">` displays "Welcome, {{ username }}"
  - `<div id="enrolled-courses">` shows enrolled courses (list)
  - `<button id="browse-courses-button">` navigates (links to catalog)
  - `<button id="my-courses-button">` navigates (links to my courses)

### 2.2 Template: `catalog.html`
- Page Title: "Available Courses"
- Container: `<div id="catalog-page">`
- Elements:
  - `<input type="text" id="search-input" placeholder="Search courses">`
  - `<div id="course-grid">` grid of courses
  - For each course card:
    - `<button id="view-course-button-{{ course.course_id }}">` to view course details (link to course_details route)
  - `<button id="back-to-dashboard">` navigates back to dashboard

### 2.3 Template: `course_details.html`
- Page Title: "Course Details"
- Container: `<div id="course-details-page">`
- Elements:
  - `<h1 id="course-title">` course title
  - `<div id="course-description">` course full description
  - `<button id="enroll-button" {% if already_enrolled %}disabled{% endif %}>` displays "Enroll" or "Already Enrolled"
  - `<button id="back-to-catalog">` navigates back to catalog

### 2.4 Template: `my_courses.html`
- Page Title: "My Courses"
- Container: `<div id="my-courses-page">`
- Elements:
  - `<div id="courses-list">` list of enrolled courses
  - For each course:
    - `<button id="continue-learning-button-{{ course.course_id }}">` navigates to course learning page
  - `<button id="back-to-dashboard">` navigates back to dashboard

### 2.5 Template: `learning.html`
- Page Title: "Course Learning"
- Container: `<div id="learning-page">`
- Elements:
  - `<div id="lessons-list">` lessons list
  - `<div id="lesson-content">` current lesson
  - `<button id="mark-complete-button" {% if progress == 100 %}disabled{% endif %}>` marks current lesson complete
  - `<button id="back-to-my-courses">` navigates back

### 2.6 Template: `assignments.html`
- Page Title: "My Assignments"
- Container: `<div id="assignments-page">`
- Elements:
  - `<table id="assignments-table">` list of assignments
  - For each assignment:
    - `<button id="submit-assignment-button-{{ assignment.assignment_id }}">` submit button
  - `<button id="back-to-dashboard">` navigates back

### 2.7 Template: `submit.html`
- Page Title: "Submit Assignment"
- Container: `<div id="submit-page">`
- Elements:
  - `<div id="assignment-info">` assignment title & description
  - `<textarea id="submission-text">` input text
  - `<button id="submit-button">` submit
  - `<button id="back-to-assignments">` back

### 2.8 Template: `certificates.html`
- Page Title: "My Certificates"
- Container: `<div id="certificates-page">`
- Elements:
  - `<div id="certificates-grid">` grid of certificate cards
  - For each certificate:
    - display course title and issue date
  - `<button id="back-to-dashboard">` back

### 2.9 Template: `profile.html`
- Page Title: "My Profile"
- Container: `<div id="profile-page">`
- Elements:
  - `<input type="email" id="profile-email" value="{{ user_email }}">`
  - `<input type="text" id="profile-fullname" value="{{ user_fullname }}">`
  - `<button id="update-profile-button">` save
  - `<button id="back-to-dashboard">` back

---

## 3. Data File Schemas (for Backend Developers)

### 3.1 `users.txt`
- Format: `username|email|fullname`
- Example:
  ```
  john|john@student.com|John Student
  alice|alice@instructor.com|Alice Professor
  jane|jane@student.com|Jane Learner
  ```
- Notes: Unique `username`. Email valid format. `fullname` string.

### 3.2 `courses.txt`
- Format: `course_id|title|description|category|level|duration|status`
- Example:
  ```
  1|Python Programming|Learn Python from scratch|Programming|Beginner|40 hours|Active
  2|Web Development|Build modern websites|Web|Intermediate|60 hours|Active
  3|Data Science|Introduction to data analysis|Data|Advanced|80 hours|Active
  ```
- Notes: Unique `course_id`. `duration` includes unit string (e.g., "40 hours"). `status` mostly "Active".

### 3.3 `enrollments.txt`
- Format: `enrollment_id|username|course_id|enrollment_date|progress|status`
- Example:
  ```
  1|john|1|2024-11-01|75|In Progress
  2|jane|1|2024-10-15|100|Completed
  3|john|2|2024-11-10|25|In Progress
  ```
- Notes: `progress` integer 0-100. `status` either "In Progress" or "Completed".

### 3.4 `assignments.txt`
- Format: `assignment_id|course_id|title|description|due_date|max_points`
- Example:
  ```
  1|1|Python Basics Quiz|Complete the quiz on variables and data types|2024-12-01|100
  2|1|Final Project|Build a calculator application|2024-12-15|200
  ```
- Notes: Date format `YYYY-MM-DD`. `max_points` integer.

### 3.5 `submissions.txt`
- Format: `submission_id|assignment_id|username|submission_text|submit_date|grade|feedback`
- Example:
  ```
  1|1|john|My answers are...|2024-11-25|85|Good work!
  2|2|jane|Here is my project...|2024-11-20|95|Excellent!
  ```
- Notes: `grade` integer. Date format `YYYY-MM-DD`.

### 3.6 `certificates.txt`
- Format: `certificate_id|username|course_id|issue_date`
- Example:
  ```
  1|jane|1|2024-11-22
  ```
- Notes: Date format `YYYY-MM-DD`.

---

# Additional Notes

- Dynamic element IDs must match exactly as `view-course-button-{course_id}`, `continue-learning-button-{course_id}`, `submit-assignment-button-{assignment_id}`.
- All navigation buttons should use Flask's `url_for` passing correct function names and parameters.
- POST routes must handle form submissions with validation and provide appropriate redirects or confirmation messages.
- Dates are stored in ISO 8601 format: `YYYY-MM-DD`.
- Status field values are constrained and documented per data schema.
- Frontend and backend developers must use this specification exclusively for parallel implementation.
