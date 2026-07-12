# OnlineCourse Web Application Design Specification

---

## Section 1: Flask Routes Specification (For Backend Developer)

| Route Path | Function Name | HTTP Method | Template File | Context Variables |
|------------|---------------|-------------|---------------|------------------|
| / | root_redirect | GET | None (redirect) | None |
| /dashboard | dashboard | GET | dashboard.html | username (str), fullname (str), enrolled_courses (list of dict: {course_id (str), title (str), progress (int)}) |
| /catalog | catalog | GET | course_catalog.html | courses (list of dict: {course_id (str), title (str), description (str), category (str), level (str), duration (str), status (str)}) |
| /catalog/course/<course_id> | course_details | GET | course_details.html | course (dict: {course_id (str), title (str), description (str), category (str), level (str), duration (str), status (str)}), is_enrolled (bool) |
| /catalog/course/<course_id>/enroll | enroll_course | POST | course_details.html | course (dict), is_enrolled (bool), enrollment_success (bool or None) |
| /my-courses | my_courses | GET | my_courses.html | enrolled_courses (list of dict: {course_id (str), title (str), progress (int)}) |
| /my-courses/course/<course_id> | course_learning | GET | course_learning.html | course (dict), lessons (list of dict: {lesson_id (str), title (str), content (str)}), completed_lessons_count (int), total_lessons (int), progress (int) |
| /my-courses/course/<course_id>/mark-complete | mark_lesson_complete | POST | course_learning.html | course (dict), lessons (list of dict), completed_lessons_count (int), total_lessons (int), progress (int), certificate_generated (bool) |
| /assignments | assignments | GET | my_assignments.html | assignments (list of dict: {assignment_id (str), course_id (str), title (str), description (str), due_date (str), max_points (int), status (str)}) |
| /assignments/submit/<assignment_id> | submit_assignment | GET, POST | submit_assignment.html | assignment (dict: {assignment_id (str), course_id (str), title (str), description (str), due_date (str), max_points (int)}), submission_status (str or None), confirmation_message (str or None) |
| /certificates | certificates | GET | certificates.html | certificates (list of dict: {certificate_id (str), username (str), course_id (str), issue_date (str), course_title (str)}) |
| /profile | profile | GET, POST | profile.html | username (str), email (str), fullname (str), update_success (bool or None) |


**Behavior and Logic Notes:**
- Root route `/` redirects to `/dashboard`.
- Dashboard displays user full name and list of enrolled courses with progress.
- Catalog shows all active courses.
- Course Details shows course info and enroll option; POST enroll creates entry in enrollments.txt and initializes progress at 0%, enrollment_date is current date; if already enrolled, enroll button is disabled.
- My Courses lists enrolled courses; selecting a course leads to learning page.
- Learning page lists lessons (assumed available via other means, e.g., a lessons data structure); marking lesson complete updates enrollment progress in enrollments.txt, enforces sequential completion.
- When progress reaches 100%, a certificate is generated and added to certificates.txt with current date.
- Assignments list all for user; submit assignment page allows text submission, writes to submissions.txt with status "Submitted" and submit_date.
- Certificates page shows all certificates for user with course titles.
- Profile page GET shows user info, POST updates email and fullname.
- All POST routes handle form submissions and redirect or re-render template with status context.

---

## Section 2: HTML Template Specifications (For Frontend Developer)

### templates/dashboard.html
- Page Title: "Learning Dashboard"
- <h1> welcome message uses ID: welcome-message, content: "Welcome, {{ fullname }}!"
- Container Div ID: dashboard-page
- Button ID: browse-courses-button, navigates to url_for('catalog')
- Button ID: my-courses-button, navigates to url_for('my_courses')
- Div ID: enrolled-courses, iterates over `enrolled_courses` context variable (list of dict)
- For each enrolled course:
  - Display course title and progress percentage

### templates/course_catalog.html
- Page Title: "Available Courses"
- Container Div ID: catalog-page
- Input ID: search-input, type="text" (search functionality is backend optional)
- Div ID: course-grid, iterates over `courses` context variable
- For each course:
  - Button ID pattern: view-course-button-{{ course.course_id }}, navigates to url_for('course_details', course_id=course.course_id)
- Button ID: back-to-dashboard, navigates to url_for('dashboard')

### templates/course_details.html
- Page Title: "Course Details"
- Container Div ID: course-details-page
- H1 ID: course-title, displays course.title
- Div ID: course-description, displays course.description
- Button ID: enroll-button, posts to url_for('enroll_course', course_id=course.course_id)
- If `is_enrolled` is True, enroll-button text is "Already Enrolled" and disabled
- Button ID: back-to-catalog, navigates to url_for('catalog')

### templates/my_courses.html
- Page Title: "My Courses"
- Container Div ID: my-courses-page
- Div ID: courses-list, iterates over `enrolled_courses`
- For each enrolled course:
  - Button ID pattern: continue-learning-button-{{ course.course_id }}, navigates to url_for('course_learning', course_id=course.course_id)
- Button ID: back-to-dashboard, navigates to url_for('dashboard')

### templates/course_learning.html
- Page Title: "Course Learning"
- Container Div ID: learning-page
- Div ID: lessons-list, iterates over `lessons` (list of dict)
- For each lesson:
  - Display lesson title
- Div ID: lesson-content, shows selected/current lesson content
- Button ID: mark-complete-button, posts to url_for('mark_lesson_complete', course_id=course.course_id)
- Button ID: back-to-my-courses, navigates to url_for('my_courses')
- Disable mark-complete-button if lesson already completed or not next in sequence

### templates/my_assignments.html
- Page Title: "My Assignments"
- Container Div ID: assignments-page
- Table ID: assignments-table, iterates over `assignments`
- For each assignment:
  - Button ID pattern: submit-assignment-button-{{ assignment.assignment_id }}, navigates to url_for('submit_assignment', assignment_id=assignment.assignment_id)
- Button ID: back-to-dashboard, navigates to url_for('dashboard')

### templates/submit_assignment.html
- Page Title: "Submit Assignment"
- Container Div ID: submit-page
- Div ID: assignment-info, shows assignment title and description
- Textarea ID: submission-text
- Button ID: submit-button, posts to url_for('submit_assignment', assignment_id=assignment.assignment_id)
- Button ID: back-to-assignments, navigates to url_for('assignments')
- On successful submission, displays confirmation message

### templates/certificates.html
- Page Title: "My Certificates"
- Container Div ID: certificates-page
- Div ID: certificates-grid, iterates over `certificates`
- For each certificate:
  - Display course_title and issue_date
- Button ID: back-to-dashboard, navigates to url_for('dashboard')

### templates/profile.html
- Page Title: "My Profile"
- Container Div ID: profile-page
- Input ID: profile-email, type="email", value from context
- Input ID: profile-fullname, type="text", value from context
- Button ID: update-profile-button, posts to url_for('profile')
- Button ID: back-to-dashboard, navigates to url_for('dashboard')
- Displays update success message if applicable

---

## Section 3: Data File Schemas (For Backend Developer)

### data/users.txt
- Fields (pipe-delimited): username|email|fullname
- Contents: Stores user credentials and full name
- Examples:
  john|john@student.com|John Student
  alice|alice@instructor.com|Alice Professor
  jane|jane@student.com|Jane Learner

### data/courses.txt
- Fields: course_id|title|description|category|level|duration|status
- Contents: Course metadata with status to filter active
- Examples:
  1|Python Programming|Learn Python from scratch|Programming|Beginner|40 hours|Active
  2|Web Development|Build modern websites|Web|Intermediate|60 hours|Active
  3|Data Science|Introduction to data analysis|Data|Advanced|80 hours|Active

### data/enrollments.txt
- Fields: enrollment_id|username|course_id|enrollment_date|progress|status
- Contents: Tracks user course enrollment, progress as integer percentage, status like "In Progress" or "Completed"
- Examples:
  1|john|1|2024-11-01|75|In Progress
  2|jane|1|2024-10-15|100|Completed
  3|john|2|2024-11-10|25|In Progress

### data/assignments.txt
- Fields: assignment_id|course_id|title|description|due_date|max_points
- Contents: Details of assignments including due date
- Examples:
  1|1|Python Basics Quiz|Complete the quiz on variables and data types|2024-12-01|100
  2|1|Final Project|Build a calculator application|2024-12-15|200

### data/submissions.txt
- Fields: submission_id|assignment_id|username|submission_text|submit_date|grade|feedback
- Contents: User assignment submissions including grading
- Examples:
  1|1|john|My answers are...|2024-11-25|85|Good work!
  2|2|jane|Here is my project...|2024-11-20|95|Excellent!

### data/certificates.txt
- Fields: certificate_id|username|course_id|issue_date
- Contents: Certificates issued for course completions
- Examples:
  1|jane|1|2024-11-22

