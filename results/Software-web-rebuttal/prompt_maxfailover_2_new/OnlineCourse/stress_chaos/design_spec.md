# Design Specification for OnlineCourse Web Application

---

## Section 1: Flask Routes Specification (For Backend Developer)

| Route Path                      | Function Name           | HTTP Method | Template File            | Context Variables                                   |
|--------------------------------|-------------------------|-------------|--------------------------|-----------------------------------------------------|
| /                              | root                    | GET         | N/A (redirect to dashboard) | None                                                |
| /dashboard                     | dashboard               | GET         | dashboard.html           | username: str, fullname: str, enrolled_courses: list of dicts ({course_id: int, title: str, progress: int}) |
| /catalog                      | catalog                 | GET         | catalog.html             | username: str, courses: list of dicts ({course_id: int, title: str, description: str})                      |
| /course/<int:course_id>        | course_details          | GET, POST   | course_details.html      | username: str, course: dict ({course_id: int, title: str, description: str, category: str, level: str, duration: str, status: str}), already_enrolled: bool |
| /my-courses                   | my_courses              | GET         | my_courses.html          | username: str, enrolled_courses: list of dicts ({course_id: int, title: str, progress: int, status: str})   |
| /learn/<int:course_id>          | course_learning         | GET, POST   | course_learning.html     | username: str, course: dict, lessons: list of dicts ({lesson_id: int, title: str, content: str}), current_lesson: dict, progress: int, can_mark_complete: bool |
| /assignments                  | my_assignments          | GET         | assignments.html         | username: str, assignments: list of dicts ({assignment_id: int, course_id: int, title: str, description: str, due_date: str, max_points: int}), submissions: dict {assignment_id: submission dict or None} |
| /submit-assignment/<int:assignment_id> | submit_assignment       | GET, POST   | submit_assignment.html   | username: str, assignment: dict ({assignment_id: int, title: str, description: str}), submission_status: str or None |
| /certificates                 | certificates            | GET         | certificates.html        | username: str, certificates: list of dicts ({certificate_id: int, course_id: int, title: str, issue_date: str}) |
| /profile                     | profile                 | GET, POST   | profile.html             | username: str, email: str, fullname: str |

### Route Behavior Notes:
- The root route `/` redirects to `/dashboard`.
- POST `/course/<course_id>` enrolls the user if not already enrolled, updates enrollments.txt with enrollment date and 0% progress.
- POST `/learn/<course_id>` marks current lesson complete if allowed, updates progress and enrollments.txt; if progress reaches 100%, creates certificate entry.
- POST `/submit-assignment/<assignment_id>` records submission with "Submitted" status and current date in submissions.txt.
- POST `/profile` updates user's email and fullname in users.txt.

---

## Section 2: HTML Template Specifications (For Frontend Developer)

### 1. dashboard.html
- File Path: templates/dashboard.html
- Page Title: Learning Dashboard (in <title> and <h1>)
- Element IDs:
  - dashboard-page (div container)
  - welcome-message (h1 displaying: "Welcome, {{ fullname }}")
  - enrolled-courses (div for listing enrolled courses)
  - browse-courses-button (button with url_for('catalog'))
  - my-courses-button (button with url_for('my_courses'))
- Context Variables:
  - username (str)
  - fullname (str)
  - enrolled_courses (list of dicts: {course_id: int, title: str, progress: int})
- Navigation:
  - browse-courses-button -> url_for('catalog')
  - my-courses-button -> url_for('my_courses')

### 2. catalog.html
- File Path: templates/catalog.html
- Page Title: Available Courses
- Element IDs:
  - catalog-page (div container)
  - search-input (input for search)
  - course-grid (div contains course cards)
  - view-course-button-{course_id} (button repeated for each course with id using Jinja: "view-course-button-{{ course.course_id }}")
  - back-to-dashboard (button with url_for('dashboard'))
- Context Variables:
  - username (str)
  - courses (list of dicts: {course_id: int, title: str, description: str})
- Navigation:
  - view-course-button-{course_id} -> url_for('course_details', course_id=course.course_id)
  - back-to-dashboard -> url_for('dashboard')

### 3. course_details.html
- File Path: templates/course_details.html
- Page Title: Course Details
- Element IDs:
  - course-details-page (div container)
  - course-title (h1 showing course.title)
  - course-description (div showing course.description)
  - enroll-button (button)
  - back-to-catalog (button with url_for('catalog'))
- Context Variables:
  - username (str)
  - course (dict with course data fields)
  - already_enrolled (bool)
- Navigation & Button State:
  - enroll-button -> POST to url_for('course_details', course_id=course.course_id)
  - enroll-button text: "Enroll" if not enrolled, "Already Enrolled" if enrolled
  - enroll-button disabled if already_enrolled == True
  - back-to-catalog -> url_for('catalog')

### 4. my_courses.html
- File Path: templates/my_courses.html
- Page Title: My Courses
- Element IDs:
  - my-courses-page (div container)
  - courses-list (div listing enrolled courses)
  - continue-learning-button-{course_id} (button repeated; id="continue-learning-button-{{ course.course_id }}")
  - back-to-dashboard (button with url_for('dashboard'))
- Context Variables:
  - username (str)
  - enrolled_courses (list of dicts with course_id, title, progress, status)
- Navigation:
  - continue-learning-button-{course_id} -> url_for('course_learning', course_id=course.course_id)
  - back-to-dashboard -> url_for('dashboard')

### 5. course_learning.html
- File Path: templates/course_learning.html
- Page Title: Course Learning
- Element IDs:
  - learning-page (div container)
  - lessons-list (div listing lessons)
  - lesson-content (div showing current lesson content)
  - mark-complete-button (button)
  - back-to-my-courses (button with url_for('my_courses'))
- Context Variables:
  - username (str)
  - course (dict)
  - lessons (list of dicts with lesson_id:int, title:str, content:str)
  - current_lesson (dict with lesson_id, title, content)
  - progress (int)
  - can_mark_complete (bool)
- Navigation & Button State:
  - mark-complete-button -> POST to url_for('course_learning', course_id=course.course_id)
  - mark-complete-button disabled if can_mark_complete == False
  - back-to-my-courses -> url_for('my_courses')

### 6. assignments.html
- File Path: templates/assignments.html
- Page Title: My Assignments
- Element IDs:
  - assignments-page (div container)
  - assignments-table (table containing assignments)
  - submit-assignment-button-{assignment_id} (button repeated; id="submit-assignment-button-{{ assignment.assignment_id }}")
  - back-to-dashboard (button with url_for('dashboard'))
- Context Variables:
  - username (str)
  - assignments (list of dicts: assignment_id, course_id, title, description, due_date, max_points)
  - submissions (dict with assignment_id keys, values: submission dict or None)
- Navigation:
  - submit-assignment-button-{assignment_id} -> url_for('submit_assignment', assignment_id=assignment.assignment_id)
  - back-to-dashboard -> url_for('dashboard')
- Button State:
  - submit-assignment-button is enabled only if assignment submission is not done yet or is late

### 7. submit_assignment.html
- File Path: templates/submit_assignment.html
- Page Title: Submit Assignment
- Element IDs:
  - submit-page (div container)
  - assignment-info (div showing assignment title and description)
  - submission-text (textarea input)
  - submit-button (button to submit form)
  - back-to-assignments (button with url_for('my_assignments'))
- Context Variables:
  - username (str)
  - assignment (dict: assignment_id, title, description)
  - submission_status (str or None for confirmation)
- Form:
  - POST form to url_for('submit_assignment', assignment_id=assignment.assignment_id)

### 8. certificates.html
- File Path: templates/certificates.html
- Page Title: My Certificates
- Element IDs:
  - certificates-page (div container)
  - certificates-grid (div grid of certificates)
  - back-to-dashboard (button with url_for('dashboard'))
- Context Variables:
  - username (str)
  - certificates (list of dicts: certificate_id, course_id, title, issue_date)
- Navigation:
  - back-to-dashboard -> url_for('dashboard')

### 9. profile.html
- File Path: templates/profile.html
- Page Title: My Profile
- Element IDs:
  - profile-page (div container)
  - profile-email (input for email)
  - profile-fullname (input for full name)
  - update-profile-button (button to save changes)
  - back-to-dashboard (button with url_for('dashboard'))
- Context Variables:
  - username (str)
  - email (str)
  - fullname (str)
- Form:
  - POST form to url_for('profile')

---

## Section 3: Data File Schemas (For Backend Developer)

### 1. users.txt
- File Path: data/users.txt
- Format: username|email|fullname
- Fields:
  - username: user's unique login name
  - email: user email address
  - fullname: full name of user
- Example Lines:
  john|john@student.com|John Student
  alice|alice@instructor.com|Alice Professor
  jane|jane@student.com|Jane Learner

### 2. courses.txt
- File Path: data/courses.txt
- Format: course_id|title|description|category|level|duration|status
- Fields:
  - course_id: unique course identifier (int)
  - title: course title
  - description: full course description
  - category: course category (e.g., Programming, Web, Data)
  - level: difficulty level (e.g., Beginner, Intermediate, Advanced)
  - duration: estimated course duration (e.g., "40 hours")
  - status: current course status (e.g., Active)
- Example Lines:
  1|Python Programming|Learn Python from scratch|Programming|Beginner|40 hours|Active
  2|Web Development|Build modern websites|Web|Intermediate|60 hours|Active
  3|Data Science|Introduction to data analysis|Data|Advanced|80 hours|Active

### 3. enrollments.txt
- File Path: data/enrollments.txt
- Format: enrollment_id|username|course_id|enrollment_date|progress|status
- Fields:
  - enrollment_id: unique enrollment identifier (int)
  - username: user login
  - course_id: course identifier
  - enrollment_date: ISO format date (YYYY-MM-DD)
  - progress: integer percentage (0-100)
  - status: enrollment status (e.g., In Progress, Completed)
- Example Lines:
  1|john|1|2024-11-01|75|In Progress
  2|jane|1|2024-10-15|100|Completed
  3|john|2|2024-11-10|25|In Progress

### 4. assignments.txt
- File Path: data/assignments.txt
- Format: assignment_id|course_id|title|description|due_date|max_points
- Fields:
  - assignment_id: unique assignment identifier (int)
  - course_id: related course identifier
  - title: assignment title
  - description: detailed description
  - due_date: ISO date for submission deadline
  - max_points: maximum points achievable (int)
- Example Lines:
  1|1|Python Basics Quiz|Complete the quiz on variables and data types|2024-12-01|100
  2|1|Final Project|Build a calculator application|2024-12-15|200

### 5. submissions.txt
- File Path: data/submissions.txt
- Format: submission_id|assignment_id|username|submission_text|submit_date|grade|feedback
- Fields:
  - submission_id: unique submission identifier (int)
  - assignment_id: assignment identifier
  - username: submitting user
  - submission_text: text response submitted
  - submit_date: ISO date of submission
  - grade: numeric grade (int or empty)
  - feedback: text feedback (empty if none)
- Example Lines:
  1|1|john|My answers are...|2024-11-25|85|Good work!
  2|2|jane|Here is my project...|2024-11-20|95|Excellent!

### 6. certificates.txt
- File Path: data/certificates.txt
- Format: certificate_id|username|course_id|issue_date
- Fields:
  - certificate_id: unique certificate identifier (int)
  - username: user who earned certificate
  - course_id: course identifier
  - issue_date: ISO date certificate was issued
- Example Lines:
  1|jane|1|2024-11-22
