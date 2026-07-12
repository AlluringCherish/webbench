# OnlineCourse Application Design Specification

---

## Section 1: Flask Routes Specification (For Backend Developer)

| Route Path                   | Function Name             | HTTP Method | Template File          | Context Variables                                                                             |
|-----------------------------|---------------------------|-------------|------------------------|-----------------------------------------------------------------------------------------------|
| /                           | root                      | GET         | N/A (redirect)          | N/A (Redirects to /dashboard)                                                                 |
| /dashboard                  | dashboard_page            | GET         | dashboard.html          | username (str), fullname (str), enrolled_courses (list of dicts with course info and progress) |
| /catalog                   | course_catalog            | GET         | catalog.html            | courses (list of dicts: course_id(str), title(str), description(str), category(str), level(str), duration(str), status(str)) |
| /course/<course_id>         | course_details            | GET         | course_details.html     | course_id (str), course (dict), is_enrolled (bool)                                            |
| /course/<course_id>/enroll  | enroll_course             | POST        | course_details.html     | course_id (str), course (dict), enrollment_success (bool), is_enrolled (bool), error_message (str, optional) |
| /my_courses                | my_courses_page           | GET         | my_courses.html         | username (str), enrolled_courses (list of dicts: course info, progress)                        |
| /course/<course_id>/learn   | course_learning           | GET         | course_learning.html    | course_id (str), lessons (list of dicts: lesson_id, title, content), current_lesson (dict), progress (int), is_completed (bool) |
| /course/<course_id>/learn/mark_complete | mark_lesson_complete      | POST        | course_learning.html    | course_id (str), progress (int), is_completed (bool)                                          |
| /assignments               | my_assignments            | GET         | assignments.html        | assignments (list of dicts with assignment info and user submission status)                   |
| /assignment/<assignment_id>/submit | submit_assignment_page     | GET         | submit_assignment.html  | assignment (dict), submission_status (str, e.g. "Not Submitted" or "Submitted")             |
| /assignment/<assignment_id>/submit | submit_assignment          | POST        | submit_assignment.html  | submission_success (bool), assignment (dict), error_message (str optional)                    |
| /certificates              | certificates_page         | GET         | certificates.html       | certificates (list of dicts), username (str)                                                  |
| /profile                   | user_profile_page         | GET         | profile.html            | username (str), email (str), fullname (str)                                                  |
| /profile/update            | update_profile            | POST        | profile.html            | update_success (bool), username (str), email (str), fullname (str), error_message (str optional) |

**Notes on Route Behaviors:**
- Root route "/" redirects to the dashboard page.
- Enrollment POST route adds entry in enrollments.txt with 0% progress and current date.
- Mark lesson complete POST route updates enrollments.txt progress; generates certificate automatically at 100%.
- Assignment submission POST route writes to submissions.txt with status "Submitted" and submission date.
- Certificate generation adds entry to certificates.txt with current date when course completed.

---

## Section 2: HTML Template Specifications (For Frontend Developer)

### 1. templates/dashboard.html
- Page Title: Learning Dashboard
- Container ID: dashboard-page
- Elements:
  - ID: welcome-message (H1) - Displays user's fullname
  - ID: enrolled-courses (Div) - Lists enrolled courses with progress
  - ID: browse-courses-button (Button) - Navigates to course_catalog (url_for('course_catalog'))
  - ID: my-courses-button (Button) - Navigates to my_courses_page (url_for('my_courses_page'))
- Context Variables:
  - username (str)
  - fullname (str)
  - enrolled_courses (list of dicts) each with: course_id (str), title (str), progress (int)

### 2. templates/catalog.html
- Page Title: Available Courses
- Container ID: catalog-page
- Elements:
  - ID: search-input (Input text) - Used for course filtering
  - ID: course-grid (Div) - Grid display of course cards
  - Dynamic Button IDs: view-course-button-{{ course.course_id }} (Button) - View course details
  - ID: back-to-dashboard (Button) - Navigates to dashboard_page (url_for('dashboard_page'))
- Context Variables:
  - courses (list of dicts) with fields: course_id (str), title (str), description (str), category (str), level (str), duration (str), status (str)

### 3. templates/course_details.html
- Page Title: Course Details
- Container ID: course-details-page
- Elements:
  - ID: course-title (H1) - Course title
  - ID: course-description (Div) - Course description
  - ID: enroll-button (Button) - Enroll in course or disabled with "Already Enrolled" text
  - ID: back-to-catalog (Button) - Navigates to course_catalog (url_for('course_catalog'))
- Context Variables:
  - course_id (str)
  - course (dict)
  - is_enrolled (bool)
- Navigation:
  - enroll-button POST submits to enroll_course route with course_id parameter

### 4. templates/my_courses.html
- Page Title: My Courses
- Container ID: my-courses-page
- Elements:
  - ID: courses-list (Div) - List enrolled courses with progress
  - Dynamic Button IDs: continue-learning-button-{{ course.course_id }} (Button) - Continue learning
  - ID: back-to-dashboard (Button) - Navigates to dashboard_page (url_for('dashboard_page'))
- Context Variables:
  - username (str)
  - enrolled_courses (list of dicts) with fields: course_id (str), title (str), progress (int)

### 5. templates/course_learning.html
- Page Title: Course Learning
- Container ID: learning-page
- Elements:
  - ID: lessons-list (Div) - List of lessons with titles
  - ID: lesson-content (Div) - Current lesson content
  - ID: mark-complete-button (Button) - Mark current lesson complete
  - ID: back-to-my-courses (Button) - Navigate to my_courses_page (url_for('my_courses_page'))
- Context Variables:
  - course_id (str)
  - lessons (list of dicts) each with lesson_id (str), title (str), content (str)
  - current_lesson (dict)
  - progress (int)
  - is_completed (bool)
- Navigation & Form:
  - mark-complete-button POST submits to mark_lesson_complete route with course_id parameter

### 6. templates/assignments.html
- Page Title: My Assignments
- Container ID: assignments-page
- Elements:
  - ID: assignments-table (Table) - Displays assignment info and status
  - Dynamic Button IDs: submit-assignment-button-{{ assignment.assignment_id }} (Button) - Submit if pending
  - ID: back-to-dashboard (Button) - Navigate to dashboard_page (url_for('dashboard_page'))
- Context Variables:
  - assignments (list of dicts) each with assignment_id, course_id, title, description, due_date, max_points, submission_status (str)

### 7. templates/submit_assignment.html
- Page Title: Submit Assignment
- Container ID: submit-page
- Elements:
  - ID: assignment-info (Div) - Shows assignment title and description
  - ID: submission-text (Textarea) - Text input for submission
  - ID: submit-button (Button) - Submit the assignment
  - ID: back-to-assignments (Button) - Navigate to my_assignments (url_for('my_assignments'))
- Context Variables:
  - assignment (dict with assignment_id, course_id, title, description, due_date)
  - submission_status (str)
- Navigation & Form:
  - submit-button POST submits to submit_assignment route with assignment_id

### 8. templates/certificates.html
- Page Title: My Certificates
- Container ID: certificates-page
- Elements:
  - ID: certificates-grid (Div) - Grid display of certificates
  - ID: back-to-dashboard (Button) - Navigate to dashboard_page (url_for('dashboard_page'))
- Context Variables:
  - certificates (list of dicts) each with certificate_id, username, course_id, issue_date
  - username (str)

### 9. templates/profile.html
- Page Title: My Profile
- Container ID: profile-page
- Elements:
  - ID: profile-email (Input) - Email input
  - ID: profile-fullname (Input) - Full name input
  - ID: update-profile-button (Button) - Submit profile updates
  - ID: back-to-dashboard (Button) - Navigate to dashboard_page (url_for('dashboard_page'))
- Context Variables:
  - username (str)
  - email (str)
  - fullname (str)
- Navigation & Form:
  - update-profile-button POST submits to update_profile route

---

## Section 3: Data File Schemas (For Backend Developer)

### 1. data/users.txt
- Fields: username|email|fullname
- Description: Stores all user accounts including students and instructors.
- Examples:
  john|john@student.com|John Student
  alice|alice@instructor.com|Alice Professor
  jane|jane@student.com|Jane Learner

### 2. data/courses.txt
- Fields: course_id|title|description|category|level|duration|status
- Description: Contains course catalog information.
- Examples:
  1|Python Programming|Learn Python from scratch|Programming|Beginner|40 hours|Active
  2|Web Development|Build modern websites|Web|Intermediate|60 hours|Active
  3|Data Science|Introduction to data analysis|Data|Advanced|80 hours|Active

### 3. data/enrollments.txt
- Fields: enrollment_id|username|course_id|enrollment_date|progress|status
- Description: Tracks user enrollments and progress in courses.
- Examples:
  1|john|1|2024-11-01|75|In Progress
  2|jane|1|2024-10-15|100|Completed
  3|john|2|2024-11-10|25|In Progress
- Note: progress field is integer percentage 0-100, status is one of "In Progress", "Completed".

### 4. data/assignments.txt
- Fields: assignment_id|course_id|title|description|due_date|max_points
- Description: Assignment details with due date and grading max points.
- Examples:
  1|1|Python Basics Quiz|Complete the quiz on variables and data types|2024-12-01|100
  2|1|Final Project|Build a calculator application|2024-12-15|200

### 5. data/submissions.txt
- Fields: submission_id|assignment_id|username|submission_text|submit_date|grade|feedback
- Description: Stores assignment submissions with grading and feedback.
- Examples:
  1|1|john|My answers are...|2024-11-25|85|Good work!
  2|2|jane|Here is my project...|2024-11-20|95|Excellent!

### 6. data/certificates.txt
- Fields: certificate_id|username|course_id|issue_date
- Description: Records certificates awarded after course completion.
- Examples:
  1|jane|1|2024-11-22

---

**End of Design Specification**
