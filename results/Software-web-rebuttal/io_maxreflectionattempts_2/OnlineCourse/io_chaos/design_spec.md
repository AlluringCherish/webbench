# OnlineCourse Application Design Specification

---

## Section 1: Flask Routes Specification (For Backend Developer)

| Route Path                           | Function Name           | HTTP Method | Template File           | Context Variables                                                                                                           |
|------------------------------------|-------------------------|-------------|-------------------------|----------------------------------------------------------------------------------------------------------------------------|
| /                                  | root                    | GET         | N/A                     | N/A (Redirects to /dashboard)                                                                                              |
| /dashboard                        | dashboard               | GET         | dashboard.html          | username (str), fullname (str), enrolled_courses (list of dict {course_id (str), title (str), progress (int)})              |
| /catalog                          | course_catalog          | GET         | catalog.html            | courses (list of dict {course_id (str), title (str), description (str), category (str), level (str), duration (str), status (str)}) |
| /catalog/search                  | course_catalog_search   | POST        | catalog.html            | courses (list of dict as above) - filtered by search query                                                                |
| /course/<course_id>               | course_details          | GET         | course_details.html     | course (dict {course_id (str), title (str), description (str), category (str), level (str), duration (str), status (str)}),
                                              already_enrolled (bool)                                                                                                   |
| /course/<course_id>/enroll       | enroll_course           | POST        | course_details.html     | course (dict as above), already_enrolled (bool), enrollment_success (bool)                                                |
| /my-courses                      | my_courses              | GET         | my_courses.html         | enrolled_courses (list of dict {course_id (str), title (str), progress (int)})                                            |
| /course/<course_id>/learn        | course_learning         | GET         | course_learning.html    | course (dict as above), lessons (list of dict {lesson_id (str), title (str), content (str)}),
                                              current_lesson_index (int), completed_lessons (list of int)                                                          |
| /course/<course_id>/learn/complete | mark_lesson_complete    | POST        | course_learning.html    | course (dict as above), lessons (list as above), current_lesson_index (int), progress (int), certificate_generated (bool)  |
| /assignments                    | my_assignments          | GET         | assignments.html        | assignments (list of dict {assignment_id (str), course_id (str), title (str), description (str), due_date (str), max_points (int)}), submissions (list of dict {assignment_id (str), username (str)}) |
| /assignment/<assignment_id>/submit | submit_assignment       | GET         | submit_assignment.html  | assignment (dict {assignment_id (str), course_id (str), title (str), description (str), due_date (str), max_points (int)})   |
| /assignment/<assignment_id>/submit | submit_assignment_post  | POST        | submit_assignment.html  | assignment (dict as above), submission_success (bool)                                                                      |
| /certificates                   | certificates_page       | GET         | certificates.html       | certificates (list of dict {certificate_id (str), username (str), course_id (str), issue_date (str)}), courses (dict of course_id to title)              |
| /profile                       | user_profile            | GET         | user_profile.html       | user (dict {username (str), email (str), fullname (str)})                                                                  |
| /profile/update                | update_profile          | POST        | user_profile.html       | user (dict as above), update_success (bool)                                                                                |

---

## Section 2: HTML Template Specifications (For Frontend Developer)

### templates/dashboard.html
- Page Title: Learning Dashboard
- Main container ID: dashboard-page (div)
- Elements:
  - welcome-message (h1) - displays user's full name: "Welcome, {{ fullname }}"
  - enrolled-courses (div) - list of enrolled courses (iterate enrolled_courses)
  - browse-courses-button (button) - navigates to course_catalog
  - my-courses-button (button) - navigates to my_courses
- Context Variables:
  - username (str)
  - fullname (str)
  - enrolled_courses (list of dict) with keys: course_id (str), title (str), progress (int)
- Navigation:
  - browse-courses-button: url_for('course_catalog')
  - my-courses-button: url_for('my_courses')

### templates/catalog.html
- Page Title: Available Courses
- Main container ID: catalog-page (div)
- Elements:
  - search-input (input, text) - for course search
  - course-grid (div) - grid of course cards
  - view-course-button-{course_id} (button) - repeated for each course
  - back-to-dashboard (button) - navigates back to dashboard
- Context Variables:
  - courses (list of dict): course_id, title, description, category, level, duration, status
- Navigation:
  - view-course-button-{course_id}: url_for('course_details', course_id=course.course_id)
  - back-to-dashboard: url_for('dashboard')
- Form:
  - search input submits to route 'course_catalog_search' via POST

### templates/course_details.html
- Page Title: Course Details
- Main container ID: course-details-page (div)
- Elements:
  - course-title (h1) - display course.title
  - course-description (div) - course.description
  - enroll-button (button) - shows "Enroll" if not enrolled, else "Already Enrolled" disabled
  - back-to-catalog (button)
- Context Variables:
  - course (dict)
  - already_enrolled (bool)
  - enrollment_success (bool) (optional for POST feedback)
- Navigation:
  - enroll-button (POST to '/course/<course_id>/enroll')
  - back-to-catalog: url_for('course_catalog')

### templates/my_courses.html
- Page Title: My Courses
- Main container ID: my-courses-page (div)
- Elements:
  - courses-list (div)
  - continue-learning-button-{course_id} (button)
  - back-to-dashboard (button)
- Context Variables:
  - enrolled_courses (list of dict with course_id, title, progress)
- Navigation:
  - continue-learning-button-{course_id}: url_for('course_learning', course_id=course_id)
  - back-to-dashboard: url_for('dashboard')

### templates/course_learning.html
- Page Title: Course Learning
- Main container ID: learning-page (div)
- Elements:
  - lessons-list (div)
  - lesson-content (div)
  - mark-complete-button (button)
  - back-to-my-courses (button)
- Context Variables:
  - course (dict)
  - lessons (list of dict with lesson_id, title, content)
  - current_lesson_index (int)
- Navigation:
  - back-to-my-courses: url_for('my_courses')
- Form:
  - mark-complete-button posts to '/course/<course_id>/learn/complete'

### templates/assignments.html
- Page Title: My Assignments
- Main container ID: assignments-page (div)
- Elements:
  - assignments-table (table)
  - submit-assignment-button-{assignment_id} (button)
  - back-to-dashboard (button)
- Context Variables:
  - assignments (list of dict with assignment_id, course_id, title, description, due_date, max_points)
  - submissions (list of dict with assignment_id, username)
- Navigation:
  - submit-assignment-button-{assignment_id}: url_for('submit_assignment', assignment_id=assignment_id)
  - back-to-dashboard: url_for('dashboard')

### templates/submit_assignment.html
- Page Title: Submit Assignment
- Main container ID: submit-page (div)
- Elements:
  - assignment-info (div)
  - submission-text (textarea)
  - submit-button (button)
  - back-to-assignments (button)
- Context Variables:
  - assignment (dict with assignment_id, course_id, title, description, due_date, max_points)
  - submission_success (bool) optional
- Navigation:
  - back-to-assignments: url_for('my_assignments')
- Form:
  - submission-text textarea posts to '/assignment/<assignment_id>/submit'

### templates/certificates.html
- Page Title: My Certificates
- Main container ID: certificates-page (div)
- Elements:
  - certificates-grid (div)
  - back-to-dashboard (button)
- Context Variables:
  - certificates (list of dict with certificate_id, username, course_id, issue_date)
  - courses (dict with course_id as key, title as value)
- Navigation:
  - back-to-dashboard: url_for('dashboard')

### templates/user_profile.html
- Page Title: My Profile
- Main container ID: profile-page (div)
- Elements:
  - profile-email (input)
  - profile-fullname (input)
  - update-profile-button (button)
  - back-to-dashboard (button)
- Context Variables:
  - user (dict with username, email, fullname)
- Navigation:
  - back-to-dashboard: url_for('dashboard')
- Form:
  - update-profile-button posts to '/profile/update'

---

## Section 3: Data File Schemas (For Backend Developer)

### data/users.txt
- Fields: username|email|fullname
- Description: Stores user credentials and profile information
- Examples:
  john|john@student.com|John Student
  alice|alice@instructor.com|Alice Professor
  jane|jane@student.com|Jane Learner

### data/courses.txt
- Fields: course_id|title|description|category|level|duration|status
- Description: Information about courses offered in the platform
- Examples:
  1|Python Programming|Learn Python from scratch|Programming|Beginner|40 hours|Active
  2|Web Development|Build modern websites|Web|Intermediate|60 hours|Active
  3|Data Science|Introduction to data analysis|Data|Advanced|80 hours|Active

### data/enrollments.txt
- Fields: enrollment_id|username|course_id|enrollment_date|progress|status
- Description: Records of user enrollments and progress
- Examples:
  1|john|1|2024-11-01|75|In Progress
  2|jane|1|2024-10-15|100|Completed
  3|john|2|2024-11-10|25|In Progress

### data/assignments.txt
- Fields: assignment_id|course_id|title|description|due_date|max_points
- Description: Assignments linked to courses
- Examples:
  1|1|Python Basics Quiz|Complete the quiz on variables and data types|2024-12-01|100
  2|1|Final Project|Build a calculator application|2024-12-15|200

### data/submissions.txt
- Fields: submission_id|assignment_id|username|submission_text|submit_date|grade|feedback
- Description: Student submissions and grading information
- Examples:
  1|1|john|My answers are...|2024-11-25|85|Good work!
  2|2|jane|Here is my project...|2024-11-20|95|Excellent!

### data/certificates.txt
- Fields: certificate_id|username|course_id|issue_date
- Description: Records of earned course certificates
- Examples:
  1|jane|1|2024-11-22
