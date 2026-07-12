# OnlineCourse Design Specification Document

---

## Section 1: Flask Routes Specification (Backend Developer)

| Route Path                   | Function Name         | HTTP Method | Template File         | Context Variables (Name: Type)                                  |
|-----------------------------|-----------------------|-------------|-----------------------|----------------------------------------------------------------|
| /                           | root_redirect          | GET         | N/A                   | None (redirects to /dashboard)                                 |
| /dashboard                  | dashboard             | GET         | dashboard.html         | username: str, fullname: str, enrolled_courses: list of dicts (each dict: course_id: int, title: str, progress: int)
|                             |                       |             |                       |                                                                  |
| /courses                   | course_catalog         | GET         | course_catalog.html    | courses: list of dicts (each dict: course_id: int, title: str, description: str, category: str, level: str, duration: str, status: str)
|                             |                       |             |                       |                                                                  |
| /courses/<int:course_id>    | course_details         | GET         | course_details.html    | course: dict (course_id: int, title: str, description: str, category: str, level: str, duration: str, status: str),
|                             |                       |             |                       | already_enrolled: bool                                            |
| /courses/<int:course_id>/enroll | enroll_course         | POST        | N/A                   | Form data: username: str,
|                             |                       |             |                       | Logic: adds enrollment entry with 0% progress and current date  |
| /mycourses                 | my_courses             | GET         | my_courses.html        | username: str, enrolled_courses: list of dicts (each dict: course_id: int, title: str, progress: int)
| /learn/<int:course_id>      | course_learning        | GET         | course_learning.html   | course: dict (course_id: int, title: str, lessons: list of dicts (lesson_id: int, title: str, content: str)),
|                             |                       |             |                       | username: str, completed_lessons: list of int, progress: int    |
| /learn/<int:course_id>/mark_complete | mark_lesson_complete | POST        | N/A                   | Form data: username: str, lesson_id: int,
|                             |                       |             |                       | Logic: update progress in enrollments.txt; generate certificate if progress=100%|
| /assignments               | my_assignments         | GET         | my_assignments.html    | username: str, assignments: list of dicts (assignment_id: int, title: str, description: str, due_date: str, max_points: int, status: str)
| /assignments/<int:assignment_id>/submit | submit_assignment     | GET         | submit_assignment.html | assignment: dict (assignment_id: int, title: str, description: str, due_date: str), username: str |
| /assignments/<int:assignment_id>/submit | submit_assignment_post | POST        | N/A                   | Form data: username: str, submission_text: str,
|                             |                       |             |                       | Logic: add submission with status "Submitted" and submit date|
| /certificates              | certificates           | GET         | certificates.html      | username: str, certificates: list of dicts (certificate_id: int, course_id: int, course_title: str, issue_date: str)
| /profile                   | user_profile           | GET         | profile.html           | username: str, email: str, fullname: str
| /profile/update            | update_profile         | POST        | N/A                   | Form data: username: str, email: str, fullname: str,
|                             |                       |             |                       | Logic: update users.txt with new info

---

Notes on important logic:
- Enrollment POST creates enrollment entry in enrollments.txt with 0% progress and current date.
- Progress updates during lesson completion POST; progress is percentage of completed lessons.
- Certificate generation adds entry in certificates.txt when progress equals 100%.
- Assignment submissions create entries in submissions.txt with status "Submitted" and current date.

---

## Section 2: HTML Template Specifications (Frontend Developer)

### 1. dashboard.html
- File Path: templates/dashboard.html
- Page Titles:
  - <title>: Learning Dashboard
  - <h1 id="welcome-message">: Displays "Welcome, {{ fullname }}"
- Element IDs:
  - dashboard-page (Div container)
  - welcome-message (H1)
  - enrolled-courses (Div) - displays list of enrolled courses with title and progress
  - browse-courses-button (Button) - URL: url_for('course_catalog')
  - my-courses-button (Button) - URL: url_for('my_courses')
- Context Variables:
  - username: str
  - fullname: str
  - enrolled_courses: list of dicts {course_id: int, title: str, progress: int}

### 2. course_catalog.html
- File Path: templates/course_catalog.html
- Page Titles:
  - <title>: Available Courses
  - <h1>: "Available Courses"
- Element IDs:
  - catalog-page (Div container)
  - search-input (Input text for search)
  - course-grid (Div) - container for course cards
  - view-course-button-{{ course.course_id }} (Button) - URL: url_for('course_details', course_id=course.course_id)
  - back-to-dashboard (Button) - URL: url_for('dashboard')
- Context Variables:
  - courses: list of dicts as per courses.txt

### 3. course_details.html
- File Path: templates/course_details.html
- Page Titles:
  - <title>: Course Details
  - <h1 id="course-title">: {{ course.title }}
- Element IDs:
  - course-details-page (Div container)
  - course-title (H1)
  - course-description (Div) - {{ course.description }}
  - enroll-button (Button) - Disabled if already_enrolled is True, else enabled
  - back-to-catalog (Button) - URL: url_for('course_catalog')
- Context Variables:
  - course: dict as per courses.txt
  - already_enrolled: bool
- Forms:
  - POST form on enroll-button to url_for('enroll_course', course_id=course.course_id)

### 4. my_courses.html
- File Path: templates/my_courses.html
- Page Titles:
  - <title>: My Courses
  - <h1>: "My Courses"
- Element IDs:
  - my-courses-page (Div container)
  - courses-list (Div) - list of enrolled courses
  - continue-learning-button-{{ course.course_id }} (Button) - URL: url_for('course_learning', course_id=course.course_id)
  - back-to-dashboard (Button) - URL: url_for('dashboard')
- Context Variables:
  - username: str
  - enrolled_courses: list of dicts {course_id: int, title: str, progress: int}

### 5. course_learning.html
- File Path: templates/course_learning.html
- Page Titles:
  - <title>: Course Learning
  - <h1>: "Course Learning"
- Element IDs:
  - learning-page (Div container)
  - lessons-list (Div) - list of lessons with titles
  - lesson-content (Div) - content of the current lesson
  - mark-complete-button (Button) - POST form submitting to url_for('mark_lesson_complete', course_id=course.course_id)
  - back-to-my-courses (Button) - url_for('my_courses')
- Context Variables:
  - username: str
  - course: dict {course_id: int, title: str, lessons: list of dicts (lesson_id: int, title: str, content: str)}
  - completed_lessons: list of int
  - progress: int

### 6. my_assignments.html
- File Path: templates/my_assignments.html
- Page Titles:
  - <title>: My Assignments
  - <h1>: "My Assignments"
- Element IDs:
  - assignments-page (Div container)
  - assignments-table (Table)
  - submit-assignment-button-{{ assignment.assignment_id }} (Button) - url_for('submit_assignment', assignment_id=assignment.assignment_id)
  - back-to-dashboard (Button) - url_for('dashboard')
- Context Variables:
  - username: str
  - assignments: list of dicts {assignment_id: int, title: str, description: str, due_date: str, max_points: int, status: str}

### 7. submit_assignment.html
- File Path: templates/submit_assignment.html
- Page Titles:
  - <title>: Submit Assignment
  - <h1>: "Submit Assignment"
- Element IDs:
  - submit-page (Div container)
  - assignment-info (Div) - shows assignment title and description
  - submission-text (Textarea) - user input field
  - submit-button (Button) - submits POST form to url_for('submit_assignment_post', assignment_id=assignment.assignment_id)
  - back-to-assignments (Button) - url_for('my_assignments')
- Context Variables:
  - username: str
  - assignment: dict {assignment_id: int, title: str, description: str, due_date: str}

### 8. certificates.html
- File Path: templates/certificates.html
- Page Titles:
  - <title>: My Certificates
  - <h1>: "My Certificates"
- Element IDs:
  - certificates-page (Div container)
  - certificates-grid (Div) - grid of completed course certificates
  - back-to-dashboard (Button) - url_for('dashboard')
- Context Variables:
  - username: str
  - certificates: list of dicts {certificate_id: int, course_id: int, course_title: str, issue_date: str}

### 9. profile.html
- File Path: templates/profile.html
- Page Titles:
  - <title>: My Profile
  - <h1>: "My Profile"
- Element IDs:
  - profile-page (Div container)
  - profile-email (Input text) - email field
  - profile-fullname (Input text) - fullname field
  - update-profile-button (Button) - submits POST form to url_for('update_profile')
  - back-to-dashboard (Button) - url_for('dashboard')
- Context Variables:
  - username: str
  - email: str
  - fullname: str
- Form Details:
  - Email input with id="profile-email"
  - Fullname input with id="profile-fullname"
  - POST form submits to /profile/update

---

## Section 3: Data File Schemas (Backend Developer)

### 1. users.txt
- File Path: data/users.txt
- Format: username|email|fullname
- Fields:
  - username: unique user ID (str)
  - email: user email address (str)
  - fullname: full user name (str)
- Examples:
  - john|john@student.com|John Student
  - alice|alice@instructor.com|Alice Professor
  - jane|jane@student.com|Jane Learner

### 2. courses.txt
- File Path: data/courses.txt
- Format: course_id|title|description|category|level|duration|status
- Fields:
  - course_id: unique course numeric ID (int)
  - title: course title (str)
  - description: detailed description (str)
  - category: course category (str)
  - level: difficulty level (Beginner/Intermediate/Advanced) (str)
  - duration: string describing hours like "40 hours" (str)
  - status: current status (Active) (str)
- Examples:
  - 1|Python Programming|Learn Python from scratch|Programming|Beginner|40 hours|Active
  - 2|Web Development|Build modern websites|Web|Intermediate|60 hours|Active
  - 3|Data Science|Introduction to data analysis|Data|Advanced|80 hours|Active

### 3. enrollments.txt
- File Path: data/enrollments.txt
- Format: enrollment_id|username|course_id|enrollment_date|progress|status
- Fields:
  - enrollment_id: unique enrollment ID (int)
  - username: user who enrolled (str)
  - course_id: course numeric ID (int)
  - enrollment_date: date in YYYY-MM-DD format (str)
  - progress: integer 0-100 percentage (int)
  - status: "In Progress" or "Completed" (str)
- Examples:
  - 1|john|1|2024-11-01|75|In Progress
  - 2|jane|1|2024-10-15|100|Completed
  - 3|john|2|2024-11-10|25|In Progress

### 4. assignments.txt
- File Path: data/assignments.txt
- Format: assignment_id|course_id|title|description|due_date|max_points
- Fields:
  - assignment_id: unique assignment ID (int)
  - course_id: course numeric ID (int)
  - title: assignment title (str)
  - description: detailed description (str)
  - due_date: date in YYYY-MM-DD format (str)
  - max_points: maximum points possible (int)
- Examples:
  - 1|1|Python Basics Quiz|Complete the quiz on variables and data types|2024-12-01|100
  - 2|1|Final Project|Build a calculator application|2024-12-15|200

### 5. submissions.txt
- File Path: data/submissions.txt
- Format: submission_id|assignment_id|username|submission_text|submit_date|grade|feedback
- Fields:
  - submission_id: unique submission ID (int)
  - assignment_id: assignment numeric ID (int)
  - username: user who submitted (str)
  - submission_text: text of submission (str)
  - submit_date: date in YYYY-MM-DD format (str)
  - grade: numeric grade (int)
  - feedback: teacher feedback text (str)
- Examples:
  - 1|1|john|My answers are...|2024-11-25|85|Good work!
  - 2|2|jane|Here is my project...|2024-11-20|95|Excellent!

### 6. certificates.txt
- File Path: data/certificates.txt
- Format: certificate_id|username|course_id|issue_date
- Fields:
  - certificate_id: unique certificate ID (int)
  - username: user who earned certificate (str)
  - course_id: course numeric ID (int)
  - issue_date: date in YYYY-MM-DD format (str)
- Examples:
  - 1|jane|1|2024-11-22

---

End of specification.