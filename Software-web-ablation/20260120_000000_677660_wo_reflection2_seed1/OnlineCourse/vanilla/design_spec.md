# OnlineCourse Application Design Specification

---

## Section 1: Flask Routes Specification (For Backend Developer)

| Route Path                      | Function Name           | HTTP Method | Template File            | Context Variables                                                                                                   |
|--------------------------------|-------------------------|-------------|--------------------------|---------------------------------------------------------------------------------------------------------------------|
| /                              | root_redirect           | GET         | None (redirect)          | None                                                                                                                |
| /dashboard                     | show_dashboard          | GET         | dashboard.html           | username (str), fullname (str), enrolled_courses (list of dicts with keys: course_id (str), title (str), progress (int)) |
| /catalog                      | show_catalog            | GET         | course_catalog.html      | courses (list of dicts with keys: course_id (str), title (str), description (str), category (str), level (str), duration (str), status (str)) |
| /catalog/search               | search_courses          | POST        | course_catalog.html      | courses (list of dicts, same as above), search_term (str)                                                           |
| /course/<course_id>           | show_course_details     | GET         | course_details.html      | course (dict with keys: course_id, title, description, category, level, duration, status), enrolled (bool)           |
| /course/<course_id>/enroll    | enroll_course           | POST        | course_details.html      | course (dict), enrolled (bool), enrollment_success (bool), enrollment_date (str)                                    |
| /my-courses                   | show_my_courses         | GET         | my_courses.html          | username (str), courses (list of dicts with keys: course_id (str), title (str), progress (int))                     |
| /learning/<course_id>         | learn_course            | GET         | course_learning.html     | course (dict), lessons (list of dicts with keys: lesson_id (str), title (str), content (str), order (int)),
                                         completed_lessons (list of lesson_ids), progress (int)                                             |
| /learning/<course_id>/complete| complete_lesson         | POST        | course_learning.html     | course (dict), lessons (list), completed_lessons (list), progress (int), lesson_completed (bool), certificate_generated (bool) |
| /assignments                 | show_assignments        | GET         | my_assignments.html      | username (str), assignments (list of dicts with keys: assignment_id (str), course_id (str), title (str), description (str), due_date (str), max_points (int)), submissions (dict keyed by assignment_id with submission info if any) |
| /assignments/<assignment_id> /submit| show_submit_assignment | GET         | submit_assignment.html   | assignment (dict with keys: assignment_id, course_id, title, description, due_date, max_points)                    |
| /assignments/<assignment_id>/submit | submit_assignment_post | POST        | submit_assignment.html   | assignment (dict), submission_success (bool), confirmation_message (str)                                          |
| /certificates                | show_certificates       | GET         | certificates.html        | username (str), certificates (list of dicts with keys: certificate_id, course_id, issue_date, course_title (str))    |
| /profile                    | show_profile            | GET         | user_profile.html        | username (str), email (str), fullname (str)                                                                       |
| /profile/update             | update_profile          | POST        | user_profile.html        | username (str), email (str), fullname (str), update_success (bool), errors (list of str)                           |

---

## Section 2: HTML Template Specifications (For Frontend Developer)

### 1. dashboard.html
- File Path: templates/dashboard.html
- Page Title (<title> and <h1>): Learning Dashboard
- Element IDs:
  - dashboard-page (Div)
  - welcome-message (H1)
  - enrolled-courses (Div)
  - browse-courses-button (Button)
  - my-courses-button (Button)
- Context Variables:
  - username (str)
  - fullname (str)
  - enrolled_courses (list of dicts)
- Dynamic Elements:
  - For each enrolled course in enrolled_courses, display course with progress.
- Navigation:
  - browse-courses-button: url_for('show_catalog')
  - my-courses-button: url_for('show_my_courses')

### 2. course_catalog.html
- File Path: templates/course_catalog.html
- Page Title: Available Courses
- Element IDs:
  - catalog-page (Div)
  - search-input (Input)
  - course-grid (Div)
  - view-course-button-{course_id} (Button, dynamic)
  - back-to-dashboard (Button)
- Context Variables:
  - courses (list of dicts)
- Dynamic Elements:
  - For each course in courses, a button with ID 'view-course-button-{{ course.course_id }}'
- Navigation:
  - view-course-button-{course_id}: url_for('show_course_details', course_id=course.course_id)
  - back-to-dashboard: url_for('show_dashboard')
- Notes:
  - Search form POSTs to /catalog/search

### 3. course_details.html
- File Path: templates/course_details.html
- Page Title: Course Details
- Element IDs:
  - course-details-page (Div)
  - course-title (H1)
  - course-description (Div)
  - enroll-button (Button)
  - back-to-catalog (Button)
- Context Variables:
  - course (dict)
  - enrolled (bool)
- Navigation:
  - enroll-button (POST to /course/<course_id>/enroll)
  - back-to-catalog: url_for('show_catalog')
- Notes:
  - enroll-button disabled if enrolled is True; text "Already Enrolled"

### 4. my_courses.html
- File Path: templates/my_courses.html
- Page Title: My Courses
- Element IDs:
  - my-courses-page (Div)
  - courses-list (Div)
  - continue-learning-button-{course_id} (Button, dynamic)
  - back-to-dashboard (Button)
- Context Variables:
  - username (str)
  - courses (list of dicts)
- Navigation:
  - continue-learning-button-{course_id}: url_for('learn_course', course_id=course_id)
  - back-to-dashboard: url_for('show_dashboard')

### 5. course_learning.html
- File Path: templates/course_learning.html
- Page Title: Course Learning
- Element IDs:
  - learning-page (Div)
  - lessons-list (Div)
  - lesson-content (Div)
  - mark-complete-button (Button)
  - back-to-my-courses (Button)
- Context Variables:
  - course (dict)
  - lessons (list of dicts)
  - completed_lessons (list of str)
  - progress (int)
- Navigation:
  - mark-complete-button (POST to /learning/<course_id>/complete)
  - back-to-my-courses: url_for('show_my_courses')
- Notes:
  - Lessons must be completed in sequence
  - mark-complete-button disabled if current lesson already completed

### 6. my_assignments.html
- File Path: templates/my_assignments.html
- Page Title: My Assignments
- Element IDs:
  - assignments-page (Div)
  - assignments-table (Table)
  - submit-assignment-button-{assignment_id} (Button, dynamic)
  - back-to-dashboard (Button)
- Context Variables:
  - username (str)
  - assignments (list of dicts)
  - submissions (dict keyed by assignment_id)
- Navigation:
  - submit-assignment-button-{assignment_id}: url_for('show_submit_assignment', assignment_id=assignment_id)
  - back-to-dashboard: url_for('show_dashboard')
- Notes:
  - Disable submit button if assignment already submitted

### 7. submit_assignment.html
- File Path: templates/submit_assignment.html
- Page Title: Submit Assignment
- Element IDs:
  - submit-page (Div)
  - assignment-info (Div)
  - submission-text (Textarea)
  - submit-button (Button)
  - back-to-assignments (Button)
- Context Variables:
  - assignment (dict)
  - submission_success (bool, optional)
  - confirmation_message (str, optional)
- Navigation:
  - submit-button (POST to /assignments/<assignment_id>/submit)
  - back-to-assignments: url_for('show_assignments')

### 8. certificates.html
- File Path: templates/certificates.html
- Page Title: My Certificates
- Element IDs:
  - certificates-page (Div)
  - certificates-grid (Div)
  - back-to-dashboard (Button)
- Context Variables:
  - username (str)
  - certificates (list of dicts)
- Navigation:
  - back-to-dashboard: url_for('show_dashboard')

### 9. user_profile.html
- File Path: templates/user_profile.html
- Page Title: My Profile
- Element IDs:
  - profile-page (Div)
  - profile-email (Input)
  - profile-fullname (Input)
  - update-profile-button (Button)
  - back-to-dashboard (Button)
- Context Variables:
  - username (str)
  - email (str)
  - fullname (str)
  - update_success (bool, optional)
  - errors (list of str, optional)
- Navigation:
  - update-profile-button (POST to /profile/update)
  - back-to-dashboard: url_for('show_dashboard')

---

## Section 3: Data File Schemas (For Backend Developer)

### 1. users.txt
- Path: data/users.txt
- Format: `username|email|fullname`
- Description: Stores user credentials and profile information.
- Examples:
  ```
  john|john@student.com|John Student
  alice|alice@instructor.com|Alice Professor
  jane|jane@student.com|Jane Learner
  ```

### 2. courses.txt
- Path: data/courses.txt
- Format: `course_id|title|description|category|level|duration|status`
- Description: Contains all courses with metadata.
- Examples:
  ```
  1|Python Programming|Learn Python from scratch|Programming|Beginner|40 hours|Active
  2|Web Development|Build modern websites|Web|Intermediate|60 hours|Active
  3|Data Science|Introduction to data analysis|Data|Advanced|80 hours|Active
  ```

### 3. enrollments.txt
- Path: data/enrollments.txt
- Format: `enrollment_id|username|course_id|enrollment_date|progress|status`
- Description: Tracks user enrollments with progress and status.
- Examples:
  ```
  1|john|1|2024-11-01|75|In Progress
  2|jane|1|2024-10-15|100|Completed
  3|john|2|2024-11-10|25|In Progress
  ```
- Notes: `enrollment_date` in YYYY-MM-DD format; `progress` as integer percentage; `status` values: In Progress, Completed

### 4. assignments.txt
- Path: data/assignments.txt
- Format: `assignment_id|course_id|title|description|due_date|max_points`
- Description: Stores assignment details linked to courses.
- Examples:
  ```
  1|1|Python Basics Quiz|Complete the quiz on variables and data types|2024-12-01|100
  2|1|Final Project|Build a calculator application|2024-12-15|200
  ```
- Notes: `due_date` format YYYY-MM-DD

### 5. submissions.txt
- Path: data/submissions.txt
- Format: `submission_id|assignment_id|username|submission_text|submit_date|grade|feedback`
- Description: Records assignment submissions with grades and feedback.
- Examples:
  ```
  1|1|john|My answers are...|2024-11-25|85|Good work!
  2|2|jane|Here is my project...|2024-11-20|95|Excellent!
  ```
- Notes: `submit_date` format YYYY-MM-DD; grade as integer score

### 6. certificates.txt
- Path: data/certificates.txt
- Format: `certificate_id|username|course_id|issue_date`
- Description: Stores certificates issued to users on course completion.
- Examples:
  ```
  1|jane|1|2024-11-22
  ```
- Notes: `issue_date` format YYYY-MM-DD
