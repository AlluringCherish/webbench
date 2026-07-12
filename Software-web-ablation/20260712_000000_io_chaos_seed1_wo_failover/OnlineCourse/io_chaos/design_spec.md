# OnlineCourse Application Design Specifications

---

## Section 1: Flask Routes Specification (For Backend Developer)

| Route Path                         | Function Name             | HTTP Method | Template File           | Context Variables                                            |
|----------------------------------|---------------------------|-------------|-------------------------|-------------------------------------------------------------|
| /                                | root_redirect             | GET         | None                    | None (redirects to dashboard)                               |
| /dashboard                       | dashboard                 | GET         | dashboard.html          | username (str), fullname (str), enrolled_courses (list of dicts with course_id (str), title (str), progress (int)) |
| /courses                        | course_catalog            | GET         | course_catalog.html     | courses (list of dict with course_id (str), title (str), description (str), category (str), level (str), duration (str), status (str)), search_query (str, optional) |
| /course/<course_id>             | course_details            | GET         | course_details.html     | course (dict with course_id (str), title (str), description (str), category (str), level (str), duration (str), status (str)), enrolled (bool) |
| /course/<course_id>/enroll      | enroll_course             | POST        | None (redirects to course details or my courses) | username (str, from session or form data)                  |
| /my-courses                    | my_courses                | GET         | my_courses.html          | username (str), enrolled_courses (list of dicts with course_id (str), title (str), progress (int)) |
| /learn/<course_id>             | course_learning           | GET         | course_learning.html     | username (str), course (dict), lessons (list of dicts with lesson_id (str), title (str), content (str)), current_lesson (dict), progress (int) |
| /learn/<course_id>/complete_lesson| complete_lesson          | POST        | None (redirects back to course learning) | username (str), lesson_id (str), course_id (str)           |
| /assignments                  | my_assignments            | GET         | my_assignments.html      | username (str), assignments (list of dicts with assignment_id (str), course_id (str), title (str), description (str), due_date (str), max_points (int), submission_status (str)) |
| /assignment/<assignment_id>     | submit_assignment_form    | GET         | submit_assignment.html  | assignment (dict), username (str), submission_text (str, optional) |
| /assignment/<assignment_id>/submit | submit_assignment         | POST        | None (redirects to my assignments)              | username (str), assignment_id (str), submission_text (str) |
| /certificates                 | my_certificates           | GET         | certificates.html        | username (str), certificates (list of dict with certificate_id (str), course_title (str), issue_date (str)) |
| /profile                      | user_profile              | GET         | profile.html             | username (str), email (str), fullname (str)                |
| /profile/update               | update_profile            | POST        | None (redirects to profile)                      | username (str), updated_email (str), updated_fullname (str) |

Notes:
- Enrollment creates a new enrollments.txt entry with 0% progress and current date.
- Completing a lesson updates enrollments.txt progress field and enforces sequential completion.
- Completing all lessons (100% progress) triggers certificate generation and adds to certificates.txt.
- Submitting assignment adds entry to submissions.txt with status "Submitted" and current date.

---

## Section 2: HTML Template Specifications (For Frontend Developer)

### templates/dashboard.html
- Page Title: Learning Dashboard
- <title> and <h1>: "Learning Dashboard"
- Container Div ID: dashboard-page
- Elements:
  - H1 with ID "welcome-message" showing user's fullname
  - Div with ID "enrolled-courses" listing enrolled courses (each course with course_id, title, and progress)
  - Button with ID "browse-courses-button" navigating to course_catalog
  - Button with ID "my-courses-button" navigating to my_courses
- Context Variables:
  - username (str)
  - fullname (str)
  - enrolled_courses (list of dict {course_id (str), title (str), progress (int)})
- Navigation:
  - browse-courses-button: url_for('course_catalog')
  - my-courses-button: url_for('my_courses')

### templates/course_catalog.html
- Page Title: Available Courses
- <title> and <h1>: "Available Courses"
- Container Div ID: catalog-page
- Elements:
  - Input with ID "search-input" for filtering courses
  - Div with ID "course-grid" containing multiple buttons with IDs "view-course-button-{{ course.course_id }}" for each course
  - Button with ID "back-to-dashboard" navigating to dashboard
- Context Variables:
  - courses (list of dicts {course_id, title, description, category, level, duration, status})
- Navigation:
  - view-course-button-{{ course.course_id }}: url_for('course_details', course_id=course.course_id)
  - back-to-dashboard: url_for('dashboard')

### templates/course_details.html
- Page Title: Course Details
- <title> and <h1>: "Course Details"
- Container Div ID: course-details-page
- Elements:
  - H1 with ID "course-title" showing course.title
  - Div with ID "course-description" showing course.description
  - Button with ID "enroll-button" which shows "Enroll" if not enrolled, or "Already Enrolled" and disabled if user enrolled
  - Button with ID "back-to-catalog" navigating to course_catalog
- Context Variables:
  - course (dict with course_id, title, description, category, level, duration, status)
  - enrolled (bool)
- Navigation:
  - enroll-button: POST to url_for('enroll_course', course_id=course.course_id)
  - back-to-catalog: url_for('course_catalog')

### templates/my_courses.html
- Page Title: My Courses
- <title> and <h1>: "My Courses"
- Container Div ID: my-courses-page
- Elements:
  - Div with ID "courses-list" showing enrolled courses with progress
  - For each course: Button with ID "continue-learning-button-{{ course.course_id }}" linking to learning page
  - Button with ID "back-to-dashboard" navigating to dashboard
- Context Variables:
  - enrolled_courses (list of dicts {course_id, title, progress})
- Navigation:
  - continue-learning-button-{{ course.course_id }}: url_for('course_learning', course_id=course.course_id)
  - back-to-dashboard: url_for('dashboard')

### templates/course_learning.html
- Page Title: Course Learning
- <title> and <h1>: "Course Learning"
- Container Div ID: learning-page
- Elements:
  - Div with ID "lessons-list" showing list of lessons with statuses
  - Div with ID "lesson-content" showing current lesson content
  - Button with ID "mark-complete-button" for marking lesson complete
  - Button with ID "back-to-my-courses" linking back to my_courses
- Context Variables:
  - course (dict)
  - lessons (list of dict {lesson_id, title, content})
  - current_lesson (dict {lesson_id, title, content})
  - progress (int)
- Navigation:
  - mark-complete-button: POST to url_for('complete_lesson', course_id=course.course_id)
  - back-to-my-courses: url_for('my_courses')

### templates/my_assignments.html
- Page Title: My Assignments
- <title> and <h1>: "My Assignments"
- Container Div ID: assignments-page
- Elements:
  - Table with ID "assignments-table" listing assignments
  - For each assignment: Button with ID "submit-assignment-button-{{ assignment.assignment_id }}" linking to submit form
  - Button with ID "back-to-dashboard" linking to dashboard
- Context Variables:
  - assignments (list of dict {assignment_id, course_id, title, description, due_date, max_points, submission_status})
- Navigation:
  - submit-assignment-button-{{ assignment.assignment_id }}: url_for('submit_assignment_form', assignment_id=assignment.assignment_id)
  - back-to-dashboard: url_for('dashboard')

### templates/submit_assignment.html
- Page Title: Submit Assignment
- <title> and <h1>: "Submit Assignment"
- Container Div ID: submit-page
- Elements:
  - Div with ID "assignment-info" showing title and description
  - Textarea with ID "submission-text" for input
  - Button with ID "submit-button" to submit form
  - Button with ID "back-to-assignments" navigating to my_assignments
- Context Variables:
  - assignment (dict)
- Navigation:
  - submit-button: POST to url_for('submit_assignment', assignment_id=assignment.assignment_id)
  - back-to-assignments: url_for('my_assignments')

### templates/certificates.html
- Page Title: My Certificates
- <title> and <h1>: "My Certificates"
- Container Div ID: certificates-page
- Elements:
  - Div with ID "certificates-grid" showing earned certificates
  - Button with ID "back-to-dashboard" navigating to dashboard
- Context Variables:
  - certificates (list of dict {certificate_id, course_title, issue_date})
- Navigation:
  - back-to-dashboard: url_for('dashboard')

### templates/profile.html
- Page Title: My Profile
- <title> and <h1>: "My Profile"
- Container Div ID: profile-page
- Elements:
  - Input with ID "profile-email" for email
  - Input with ID "profile-fullname" for full name
  - Button with ID "update-profile-button" to submit changes
  - Button with ID "back-to-dashboard" to navigate back
- Context Variables:
  - email (str)
  - fullname (str)
- Navigation:
  - update-profile-button: POST to url_for('update_profile')
  - back-to-dashboard: url_for('dashboard')

---

## Section 3: Data File Schemas (For Backend Developer)

### data/users.txt
- Format: `username|email|fullname`
- Fields:
  - username: str, unique user ID
  - email: str, user email address
  - fullname: str, user full name
- Example lines:
  - john|john@student.com|John Student
  - alice|alice@instructor.com|Alice Professor
  - jane|jane@student.com|Jane Learner

### data/courses.txt
- Format: `course_id|title|description|category|level|duration|status`
- Fields:
  - course_id: str, unique course identifier
  - title: str, course title
  - description: str, detailed course description
  - category: str, course category
  - level: str, difficulty level
  - duration: str, estimated hours (e.g., "40 hours")
  - status: str, course status (e.g., Active)
- Example lines:
  - 1|Python Programming|Learn Python from scratch|Programming|Beginner|40 hours|Active
  - 2|Web Development|Build modern websites|Web|Intermediate|60 hours|Active
  - 3|Data Science|Introduction to data analysis|Data|Advanced|80 hours|Active

### data/enrollments.txt
- Format: `enrollment_id|username|course_id|enrollment_date|progress|status`
- Fields:
  - enrollment_id: str, unique enrollment record
  - username: str, user identifier
  - course_id: str, course identifier
  - enrollment_date: str, ISO date (YYYY-MM-DD)
  - progress: str or int, percentage progress (0-100)
  - status: str, e.g., In Progress, Completed
- Example lines:
  - 1|john|1|2024-11-01|75|In Progress
  - 2|jane|1|2024-10-15|100|Completed
  - 3|john|2|2024-11-10|25|In Progress

### data/assignments.txt
- Format: `assignment_id|course_id|title|description|due_date|max_points`
- Fields:
  - assignment_id: str, unique assignment ID
  - course_id: str, related course
  - title: str, assignment title
  - description: str, assignment details
  - due_date: str, ISO date
  - max_points: int, points possible
- Example lines:
  - 1|1|Python Basics Quiz|Complete the quiz on variables and data types|2024-12-01|100
  - 2|1|Final Project|Build a calculator application|2024-12-15|200

### data/submissions.txt
- Format: `submission_id|assignment_id|username|submission_text|submit_date|grade|feedback`
- Fields:
  - submission_id: str, unique submission record
  - assignment_id: str
  - username: str
  - submission_text: str, text response
  - submit_date: str, ISO date
  - grade: int or empty if ungraded
  - feedback: str or empty
- Example lines:
  - 1|1|john|My answers are...|2024-11-25|85|Good work!
  - 2|2|jane|Here is my project...|2024-11-20|95|Excellent!

### data/certificates.txt
- Format: `certificate_id|username|course_id|issue_date`
- Fields:
  - certificate_id: str, unique certificate
  - username: str
  - course_id: str
  - issue_date: str, ISO date
- Example lines:
  - 1|jane|1|2024-11-22

---

_End of design_spec.md_
