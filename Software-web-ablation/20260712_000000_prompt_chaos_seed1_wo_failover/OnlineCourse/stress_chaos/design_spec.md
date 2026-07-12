# OnlineCourse Web Application Design Specifications

---

## Section 1: Flask Routes Specification (For Backend Developer)

| Route Path                     | Function Name           | HTTP Method | Template File           | Context Variables                                                                              |
|-------------------------------|------------------------|-------------|-------------------------|------------------------------------------------------------------------------------------------|
| /                             | root_redirect           | GET         | -                       | - Redirects to /dashboard                                                                      |
| /dashboard                    | dashboard_view         | GET         | dashboard.html          | username: str, fullname: str, enrolled_courses: list of dicts (course_id, title, progress)      |
| /catalog                     | course_catalog_view    | GET         | catalog.html            | username: str, courses: list of dicts (course_id, title, description)                          |
| /course/<int:course_id>      | course_details_view    | GET         | course_details.html     | username: str, course: dict (course_id, title, description, enrollment_status: bool)          |
| /course/<int:course_id>/enroll | enroll_course         | POST        | course_details.html     | username: str, course: dict, enrollment_status: bool (updates)                                 |
| /my-courses                  | my_courses_view        | GET         | my_courses.html         | username: str, enrolled_courses: list of dicts (course_id, title, progress)                    |
| /learning/<int:course_id>    | course_learning_view   | GET         | course_learning.html    | username: str, course: dict, lessons: list of dicts (lesson_id, title, content, is_completed: bool), progress: int |
| /learning/<int:course_id>/complete | mark_lesson_complete | POST        | course_learning.html    | username: str, course: dict, lessons: list, progress: int (updated)                            |
| /assignments                | my_assignments_view    | GET         | assignments.html        | username: str, assignments: list of dicts (assignment_id, title, description, due_date, status) |
| /assignment/<int:assignment_id>/submit | submit_assignment_view | GET  | submit_assignment.html  | username: str, assignment: dict (assignment_id, title, description)                           |
| /assignment/<int:assignment_id>/submit | submit_assignment_post | POST | submit_assignment.html | username: str, assignment: dict, confirmation_msg: str (on success)                           |
| /certificates              | certificates_view      | GET         | certificates.html       | username: str, certificates: list of dicts (certificate_id, course_title, issue_date)          |
| /profile                   | profile_view           | GET         | profile.html            | username: str, email: str, fullname: str                                                     |
| /profile/update            | update_profile         | POST        | profile.html            | username: str, email: str, fullname: str, update_status: str                                  |

Notes:
- Enrollment creates a new enrollments.txt record with 0% progress and current date.
- Marking lesson complete updates progress in enrollments.txt and can trigger certificate generation.
- Assignment submissions add an entry to submissions.txt with status "Submitted" and current date.
- Certificates are generated automatically when progress reaches 100%.
- Dashboard, My Courses, and My Assignments show user-specific data.

---

## Section 2: HTML Template Specifications (For Frontend Developer)

### Template: templates/dashboard.html
- **Page Title**: Learning Dashboard
- **Page <title> and <h1>**: Learning Dashboard, &lt;h1 id="welcome-message"&gt;Welcome, {{ fullname }}&lt;/h1&gt;
- **Element IDs:**
  - dashboard-page
  - welcome-message
  - enrolled-courses
  - browse-courses-button
  - my-courses-button
- **Context Variables:**
  - username (str)
  - fullname (str)
  - enrolled_courses (list of dicts with course_id (int), title (str), progress (int))
- **Navigation:**
  - #browse-courses-button: url_for('course_catalog_view')
  - #my-courses-button: url_for('my_courses_view')

---

### Template: templates/catalog.html
- **Page Title**: Available Courses
- **Page <title> and <h1>:** Available Courses
- **Element IDs:**
  - catalog-page
  - search-input
  - course-grid
  - back-to-dashboard
  - Dynamic IDs for course cards: view-course-button-{{ course.course_id }}
- **Context Variables:**
  - username (str)
  - courses (list of dicts with course_id (int), title (str), description (str))
- **Navigation:**
  - #view-course-button-{{ course.course_id }}: url_for('course_details_view', course_id=course.course_id)
  - #back-to-dashboard: url_for('dashboard_view')

---

### Template: templates/course_details.html
- **Page Title**: Course Details
- **Page <title> and <h1>:** Course Details
- **Element IDs:**
  - course-details-page
  - course-title
  - course-description
  - enroll-button
  - back-to-catalog
- **Context Variables:**
  - username (str)
  - course (dict): course_id (int), title (str), description (str), enrollment_status (bool)
- **Navigation:**
  - #enroll-button: form POST to url_for('enroll_course', course_id=course.course_id)
  - #back-to-catalog: url_for('course_catalog_view')
- **Button states:**
  - enroll-button disabled and text "Already Enrolled" if enrollment_status is True

---

### Template: templates/my_courses.html
- **Page Title**: My Courses
- **Page <title> and <h1>:** My Courses
- **Element IDs:**
  - my-courses-page
  - courses-list
  - back-to-dashboard
  - Dynamic IDs: continue-learning-button-{{ course.course_id }}
- **Context Variables:**
  - username (str)
  - enrolled_courses (list of dicts with course_id (int), title (str), progress (int))
- **Navigation:**
  - #continue-learning-button-{{ course.course_id }}: url_for('course_learning_view', course_id=course.course_id)
  - #back-to-dashboard: url_for('dashboard_view')

---

### Template: templates/course_learning.html
- **Page Title**: Course Learning
- **Page <title> and <h1>:** Course Learning
- **Element IDs:**
  - learning-page
  - lessons-list
  - lesson-content
  - mark-complete-button
  - back-to-my-courses
- **Context Variables:**
  - username (str)
  - course (dict) with course_id, title
  - lessons (list of dicts with lesson_id (int), title (str), content (str), is_completed (bool))
  - progress (int)
- **Navigation:**
  - #mark-complete-button: form POST to url_for('mark_lesson_complete', course_id=course.course_id)
  - #back-to-my-courses: url_for('my_courses_view')
- **Notes:**
  - Lessons must be completed sequentially
  - mark-complete-button disabled if current lesson incomplete sequence violated

---

### Template: templates/assignments.html
- **Page Title**: My Assignments
- **Page <title> and <h1>:** My Assignments
- **Element IDs:**
  - assignments-page
  - assignments-table
  - back-to-dashboard
  - Dynamic IDs: submit-assignment-button-{{ assignment.assignment_id }}
- **Context Variables:**
  - username (str)
  - assignments (list of dicts with assignment_id (int), title (str), description (str), due_date (str), status (str))
- **Navigation:**
  - #submit-assignment-button-{{ assignment.assignment_id }}: url_for('submit_assignment_view', assignment_id=assignment.assignment_id)
  - #back-to-dashboard: url_for('dashboard_view')

---

### Template: templates/submit_assignment.html
- **Page Title**: Submit Assignment
- **Page <title> and <h1>:** Submit Assignment
- **Element IDs:**
  - submit-page
  - assignment-info
  - submission-text
  - submit-button
  - back-to-assignments
- **Context Variables:**
  - username (str)
  - assignment (dict with assignment_id (int), title (str), description (str))
- **Navigation:**
  - #submit-button: form POST to url_for('submit_assignment_post', assignment_id=assignment.assignment_id)
  - #back-to-assignments: url_for('my_assignments_view')
- **Notes:**
  - submission-text: textarea input

---

### Template: templates/certificates.html
- **Page Title**: My Certificates
- **Page <title> and <h1>:** My Certificates
- **Element IDs:**
  - certificates-page
  - certificates-grid
  - back-to-dashboard
- **Context Variables:**
  - username (str)
  - certificates (list of dicts with certificate_id (int), course_title (str), issue_date (str))
- **Navigation:**
  - #back-to-dashboard: url_for('dashboard_view')

---

### Template: templates/profile.html
- **Page Title**: My Profile
- **Page <title> and <h1>:** My Profile
- **Element IDs:**
  - profile-page
  - profile-email
  - profile-fullname
  - update-profile-button
  - back-to-dashboard
- **Context Variables:**
  - username (str)
  - email (str)
  - fullname (str)
- **Navigation:**
  - #update-profile-button: form POST to url_for('update_profile')
  - #back-to-dashboard: url_for('dashboard_view')
- **Notes:**
  - profile-email, profile-fullname: input fields

---

## Section 3: Data File Schemas (For Backend Developer)

### 1. users.txt
- **File path:** data/users.txt
- **Fields:** username | email | fullname
- **Description:** User login name, email address, and full name of user.
- **Examples:**
  ```
  john|john@student.com|John Student
  alice|alice@instructor.com|Alice Professor
  jane|jane@student.com|Jane Learner
  ```

---

### 2. courses.txt
- **File path:** data/courses.txt
- **Fields:** course_id | title | description | category | level | duration | status
- **Description:** Unique course identifier, title, detailed description, course category, difficulty level, total duration, and current status.
- **Examples:**
  ```
  1|Python Programming|Learn Python from scratch|Programming|Beginner|40 hours|Active
  2|Web Development|Build modern websites|Web|Intermediate|60 hours|Active
  3|Data Science|Introduction to data analysis|Data|Advanced|80 hours|Active
  ```

---

### 3. enrollments.txt
- **File path:** data/enrollments.txt
- **Fields:** enrollment_id | username | course_id | enrollment_date | progress | status
- **Description:** Unique enrollment ID, username, course enrolled, enrollment date (YYYY-MM-DD), completion progress as percentage, enrollment status.
- **Examples:**
  ```
  1|john|1|2024-11-01|75|In Progress
  2|jane|1|2024-10-15|100|Completed
  3|john|2|2024-11-10|25|In Progress
  ```

---

### 4. assignments.txt
- **File path:** data/assignments.txt
- **Fields:** assignment_id | course_id | title | description | due_date | max_points
- **Description:** Unique assignment ID, linked course ID, assignment title, description, due date (YYYY-MM-DD), and maximum attainable points.
- **Examples:**
  ```
  1|1|Python Basics Quiz|Complete the quiz on variables and data types|2024-12-01|100
  2|1|Final Project|Build a calculator application|2024-12-15|200
  ```

---

### 5. submissions.txt
- **File path:** data/submissions.txt
- **Fields:** submission_id | assignment_id | username | submission_text | submit_date | grade | feedback
- **Description:** Unique submission ID, assignment linked, submitting user, textual submission, submission date (YYYY-MM-DD), assigned grade, and instructor feedback.
- **Examples:**
  ```
  1|1|john|My answers are...|2024-11-25|85|Good work!
  2|2|jane|Here is my project...|2024-11-20|95|Excellent!
  ```

---

### 6. certificates.txt
- **File path:** data/certificates.txt
- **Fields:** certificate_id | username | course_id | issue_date
- **Description:** Unique certificate ID, user who earned it, course completed, and issue date (YYYY-MM-DD).
- **Examples:**
  ```
  1|jane|1|2024-11-22
  ```
