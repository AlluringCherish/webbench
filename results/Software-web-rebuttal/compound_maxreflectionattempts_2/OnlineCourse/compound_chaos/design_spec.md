# OnlineCourse Application Design Specification

---

## 1. Flask Routes Specification (Backend Focus)

| Route Path                       | Function Name          | HTTP Method | Template File           | Context Variables (name: type)                                                                                             |
|---------------------------------|------------------------|-------------|------------------------|----------------------------------------------------------------------------------------------------------------------------|
| /                               | root_redirect          | GET         | -                      | - (Redirects to /dashboard)                                                                                                |
| /dashboard                      | dashboard              | GET         | dashboard.html          | username: str, fullname: str, enrolled_courses: List[Dict{course_id: str, title: str, progress: int}]                       |
| /courses/catalog                | course_catalog         | GET         | course_catalog.html     | courses: List[Dict{course_id: str, title: str, description: str, category: str, level: str, duration: str, status: str}]    |
| /courses/<course_id>            | course_details         | GET         | course_details.html     | course: Dict{course_id: str, title: str, description: str}, enrolled: bool                                                   |
| /courses/<course_id>/enroll    | enroll_course          | POST        | course_details.html     | course: Dict{course_id: str, title: str, description: str}, enrolled: bool, enrollment_success: bool or None (on POST)      |
| /my-courses                    | my_courses             | GET         | my_courses.html         | enrolled_courses: List[Dict{course_id: str, title: str, progress: int}]                                                     |
| /my-courses/<course_id>        | course_learning        | GET         | course_learning.html    | course_id: str, course_title: str, lessons: List[Dict{lesson_id: str, title: str}], current_lesson: Dict{lesson_id: str, title: str, content: str}, completed_lessons_ids: Set[str], progress: int |
| /my-courses/<course_id>/mark-complete | mark_lesson_complete  | POST        | course_learning.html    | course_id: str, progress: int, lesson_completed: bool, certificate_generated: bool                                          |
| /assignments                  | my_assignments         | GET         | my_assignments.html     | assignments: List[Dict{assignment_id: str, course_id: str, title: str, description: str, due_date: str, max_points: int}]    |
| /assignments/<assignment_id>  | submit_assignment      | GET         | submit_assignment.html  | assignment: Dict{assignment_id: str, title: str, description: str}                                                         |
| /assignments/<assignment_id>/submit | submit_assignment_post | POST        | submit_assignment.html  | assignment: Dict{assignment_id: str, title: str, description: str}, submission_success: bool or None                       |
| /certificates                 | certificates           | GET         | certificates.html       | certificates: List[Dict{certificate_id: str, username: str, course_id: str, issue_date: str, course_title: str}]            |
| /profile                     | user_profile           | GET         | user_profile.html       | username: str, email: str, fullname: str                                                                                   |
| /profile/update              | update_profile         | POST        | user_profile.html       | username: str, email: str, fullname: str, update_success: bool or None                                                     |


### Logic Notes:
- Root path `/` redirects permanently (HTTP 302) to `/dashboard`.
- Enrollment POST at `/courses/<course_id>/enroll` adds entry in enrollments.txt with current date, 0% progress, status "In Progress".
- Enrollment button disabled if user already enrolled.
- Progress tracking calculated from lessons completed divided by total lessons.
- Lessons must be marked complete in sequence; mark complete POST updates enrollments.txt progress.
- Upon 100% progress, certificate entry is created with current date in certificates.txt.
- Assignment submission POST adds entry to submissions.txt with status "Submitted" and current date.
- Certificates page fetches certificates only for current user.

---

## 2. HTML Template Specifications (Frontend Focus)

### templates/dashboard.html
- Title: "Learning Dashboard"
- H1 (ID: welcome-message): "Welcome, {{ fullname }}!"
- Container Div ID: dashboard-page
- Elements:
  - Div ID: enrolled-courses — Lists enrolled courses ({{ enrolled_courses }})
  - Button ID: browse-courses-button — Navigates to `course_catalog` (GET)
  - Button ID: my-courses-button — Navigates to `my_courses` (GET)

- Navigation:
  - browse-courses-button → url_for('course_catalog')
  - my-courses-button → url_for('my_courses')


### templates/course_catalog.html
- Title: "Available Courses"
- H1: None
- Container Div ID: catalog-page
- Elements:
  - Input ID: search-input (text field for searching)
  - Div ID: course-grid — Displays course cards for each course, each with:
    - Button ID pattern: view-course-button-{{ course.course_id }} — Navigates to course_details with course_id param
  - Button ID: back-to-dashboard — Navigates to `dashboard` (GET)

- Navigation:
  - view-course-button-{course_id} → url_for('course_details', course_id=course_id)
  - back-to-dashboard → url_for('dashboard')


### templates/course_details.html
- Title: "Course Details"
- H1 (ID: course-title): "{{ course.title }}"
- Container Div ID: course-details-page
- Elements:
  - Div ID: course-description — Displays course.description
  - Button ID: enroll-button — POST form submits to enroll_course for this course
    - If enrolled is True, button text: "Already Enrolled", disabled
    - Else button text: "Enroll"
  - Button ID: back-to-catalog — Navigates to `course_catalog` (GET)

- Navigation:
  - back-to-catalog → url_for('course_catalog')

- Form:
  - enroll-button submits POST to url_for('enroll_course', course_id=course.course_id)


### templates/my_courses.html
- Title: "My Courses"
- H1: None
- Container Div ID: my-courses-page
- Elements:
  - Div ID: courses-list — Lists enrolled courses (with progress shown)
    - Each course has Button ID pattern: continue-learning-button-{{ course.course_id }} — navigates to course_learning with course_id
  - Button ID: back-to-dashboard — Navigates to `dashboard` (GET)

- Navigation:
  - continue-learning-button-{course_id} → url_for('course_learning', course_id=course_id)
  - back-to-dashboard → url_for('dashboard')


### templates/course_learning.html
- Title: "Course Learning"
- H1: None
- Container Div ID: learning-page
- Elements:
  - Div ID: lessons-list — Lists all lessons in order with completed lessons marked
  - Div ID: lesson-content — Displays current lesson content
  - Button ID: mark-complete-button — POST form to mark the current lesson complete
  - Button ID: back-to-my-courses — Navigates to `my_courses` (GET)

- Navigation:
  - back-to-my-courses → url_for('my_courses')

- Form:
  - mark-complete-button submits POST to url_for('mark_lesson_complete', course_id=course_id)

- Button State:
  - mark-complete-button enabled only if current lesson is next to complete (else disabled)


### templates/my_assignments.html
- Title: "My Assignments"
- H1: None
- Container Div ID: assignments-page
- Elements:
  - Table ID: assignments-table — Displays assignments with columns: title, description, due date, max points
  - Button ID pattern: submit-assignment-button-{{ assignment.assignment_id }} — navigates to submit_assignment
  - Button ID: back-to-dashboard — Navigates to `dashboard` (GET)

- Navigation:
  - submit-assignment-button-{assignment_id} → url_for('submit_assignment', assignment_id=assignment_id)
  - back-to-dashboard → url_for('dashboard')


### templates/submit_assignment.html
- Title: "Submit Assignment"
- H1: None
- Container Div ID: submit-page
- Elements:
  - Div ID: assignment-info — Shows assignment title and description
  - Textarea ID: submission-text — For entering text response
  - Button ID: submit-button — POST form to submit submission
  - Button ID: back-to-assignments — Navigates back to `my_assignments` (GET)

- Navigation:
  - back-to-assignments → url_for('my_assignments')

- Form:
  - submit-button submits POST to url_for('submit_assignment_post', assignment_id=assignment.assignment_id)


### templates/certificates.html
- Title: "My Certificates"
- H1: None
- Container Div ID: certificates-page
- Elements:
  - Div ID: certificates-grid — Grid of certificate cards showing course title and issue date
  - Button ID: back-to-dashboard — Navigates to `dashboard` (GET)

- Navigation:
  - back-to-dashboard → url_for('dashboard')


### templates/user_profile.html
- Title: "My Profile"
- H1: None
- Container Div ID: profile-page
- Elements:
  - Input ID: profile-email — Email input field with current email value
  - Input ID: profile-fullname — Full name input field with current full name
  - Button ID: update-profile-button — POST form to update profile
  - Button ID: back-to-dashboard — Navigates to `dashboard` (GET)

- Navigation:
  - back-to-dashboard → url_for('dashboard')

- Form:
  - update-profile-button submits POST to url_for('update_profile')

---

## 3. Data File Schemas (Backend Focus)

### users.txt
- Filename: users.txt
- Fields (pipe-delimited): username|email|fullname
- Field Descriptions:
  - username: unique user identifier (string, no pipes)
  - email: valid email string
  - fullname: user's full name (string)

- Example Lines:
  - john|john@student.com|John Student
  - alice|alice@instructor.com|Alice Professor
  - jane|jane@student.com|Jane Learner


### courses.txt
- Filename: courses.txt
- Fields (pipe-delimited): course_id|title|description|category|level|duration|status
- Field Descriptions:
  - course_id: unique identifier (string, numeric ID in examples)
  - title: course title (string)
  - description: detailed course description (string)
  - category: course category (string)
  - level: difficulty level (e.g., Beginner, Intermediate, Advanced)
  - duration: course length description (string)
  - status: course status (e.g., Active)

- Example Lines:
  - 1|Python Programming|Learn Python from scratch|Programming|Beginner|40 hours|Active
  - 2|Web Development|Build modern websites|Web|Intermediate|60 hours|Active
  - 3|Data Science|Introduction to data analysis|Data|Advanced|80 hours|Active


### enrollments.txt
- Filename: enrollments.txt
- Fields (pipe-delimited): enrollment_id|username|course_id|enrollment_date|progress|status
- Field Descriptions:
  - enrollment_id: unique enrollment ID (string)
  - username: user identifier (string)
  - course_id: course identifier (string)
  - enrollment_date: date in YYYY-MM-DD format
  - progress: integer progress percentage (0 to 100)
  - status: enrollment status (e.g., In Progress, Completed)

- Example Lines:
  - 1|john|1|2024-11-01|75|In Progress
  - 2|jane|1|2024-10-15|100|Completed
  - 3|john|2|2024-11-10|25|In Progress


### assignments.txt
- Filename: assignments.txt
- Fields (pipe-delimited): assignment_id|course_id|title|description|due_date|max_points
- Field Descriptions:
  - assignment_id: unique ID for the assignment (string)
  - course_id: related course ID (string)
  - title: assignment title (string)
  - description: assignment description (string)
  - due_date: date in YYYY-MM-DD format
  - max_points: integer maximum score possible

- Example Lines:
  - 1|1|Python Basics Quiz|Complete the quiz on variables and data types|2024-12-01|100
  - 2|1|Final Project|Build a calculator application|2024-12-15|200


### submissions.txt
- Filename: submissions.txt
- Fields (pipe-delimited): submission_id|assignment_id|username|submission_text|submit_date|grade|feedback
- Field Descriptions:
  - submission_id: unique submission ID (string)
  - assignment_id: related assignment ID (string)
  - username: submitting user's username (string)
  - submission_text: text response
  - submit_date: date in YYYY-MM-DD format
  - grade: integer or empty if not graded
  - feedback: textual feedback or empty

- Example Lines:
  - 1|1|john|My answers are...|2024-11-25|85|Good work!
  - 2|2|jane|Here is my project...|2024-11-20|95|Excellent!


### certificates.txt
- Filename: certificates.txt
- Fields (pipe-delimited): certificate_id|username|course_id|issue_date
- Field Descriptions:
  - certificate_id: unique certificate ID (string)
  - username: user's username (string)
  - course_id: course identifier (string)
  - issue_date: date in YYYY-MM-DD format

- Example Lines:
  - 1|jane|1|2024-11-22

---

# Assumptions:
- The user authentication and current logged-in user context are assumed handled outside the scope here.
- Lesson content and structure are stored and retrieved within the backend; lesson data file(s) are not specified hence lessons are assumed fetched from in-memory or other source.
- Button IDs for repeated elements include the relevant unique IDs as suffix for the frontend to use.
- Date formats for all date fields follow ISO YYYY-MM-DD.
- Progress field is integer percent between 0 and 100.

---

End of Design Specification
