# OnlineCourse Application Design Specification

---

## Section 1: Flask Routes Specification (For Backend Developer)

| Route Path                      | Function Name             | HTTP Method | Template File            | Context Variables                                                                                                   |
|--------------------------------|---------------------------|-------------|--------------------------|---------------------------------------------------------------------------------------------------------------------|
| /                              | root_redirect             | GET         | None (redirect)          | None                                                                                                                |
| /dashboard                     | dashboard                 | GET         | dashboard.html           | username (str), fullname (str), enrolled_courses (list of dict: course_id, title, progress (int %)), 
|                                |                           |             |                          | user_enrolled_course_ids (list of int)                                                                             |
| /catalog                      | course_catalog            | GET         | catalog.html             | courses (list of dict: course_id, title, description, category, level, duration, status)                           |
| /course/<int:course_id>        | course_details            | GET         | course_details.html      | course (dict: course_id, title, description, category, level, duration, status),
|                                |                           |             |                          | enrolled (bool), enrollment_date (str or None)                                                                     |
| /course/<int:course_id>/enroll | enroll_course             | POST        | course_details.html      | course (dict), enrolled (bool), enrollment_date (str or None), enroll_success (bool), error_message (str or None)  |
| /my-courses                   | my_courses                | GET         | my_courses.html          | enrolled_courses (list of dict: course_id, title, progress (int %)), username (str)                                |
| /learning/<int:course_id>      | course_learning           | GET         | course_learning.html     | course (dict), lessons (list of dict: lesson_id, title, content), current_lesson (dict or None), 
|                                |                           |             |                          | progress (int %), lesson_index (int)                                                                             |
| /learning/<int:course_id>/mark_complete | mark_lesson_complete     | POST        | course_learning.html     | course (dict), lessons (list of dict), current_lesson (dict), progress (int), mark_success (bool), error_message (str or None) |
| /assignments                  | my_assignments            | GET         | assignments.html         | assignments (list of dict: assignment_id, course_id, title, description, due_date, max_points), username (str),
|                                |                           |             |                          | submissions_status (dict keyed by assignment_id: "Submitted" or "Pending")                                     |
| /assignment/<int:assignment_id>/submit | submit_assignment         | GET         | submit_assignment.html   | assignment (dict), submission_text (str or empty)                                                                  |
| /assignment/<int:assignment_id>/submit | submit_assignment_post    | POST        | submit_assignment.html   | assignment (dict), submit_success (bool), error_message (str or None)                                              |
| /certificates                 | certificates              | GET         | certificates.html        | certificates (list of dict: certificate_id, course_id, title, issue_date), username (str)                          |
| /profile                      | profile                   | GET         | profile.html             | username (str), email (str), fullname (str)                                                                        |
| /profile/update               | update_profile            | POST        | profile.html             | update_success (bool), error_message (str or None), username (str), email (str), fullname (str)                    |

Notes:
- Root route '/' redirects to '/dashboard' after login.
- Enrollment POST route creates enrollment entry with 0% progress and current date.
- Progress updated on marking lessons completed; certificates created on 100% completion.
- Assignment submissions POST route adds entries with status "Submitted" and submit date.
- Certificate list shown only for completed courses.

---

## Section 2: HTML Template Specifications (For Frontend Developer)

### templates/dashboard.html
- Page Title: Learning Dashboard
- <title> and <h1>: "Learning Dashboard"
- Element IDs:
  - dashboard-page (Div)
  - welcome-message (H1) - Displays "Welcome, {{ fullname }}"
  - enrolled-courses (Div) - List of enrolled courses each with title, progress %
  - browse-courses-button (Button) - Navigates to course_catalog
  - my-courses-button (Button) - Navigates to my_courses
- Context Variables:
  - username (str)
  - fullname (str)
  - enrolled_courses (list of dict {course_id, title, progress (int)})
  - user_enrolled_course_ids (list of ints)
- Navigation url_for Mappings:
  - browse-courses-button: url_for('course_catalog')
  - my-courses-button: url_for('my_courses')

---

### templates/catalog.html
- Page Title: Available Courses
- <title> and <h1>: "Available Courses"
- Element IDs:
  - catalog-page (Div)
  - search-input (Input)
  - course-grid (Div) - Contains buttons for each course
  - view-course-button-{{ course.course_id }} (Button) - View course details
  - back-to-dashboard (Button) - Navigates back to dashboard
- Context Variables:
  - courses (list of dict)
- Navigation url_for Mappings:
  - view-course-button-{{ course.course_id }}: url_for('course_details', course_id=course.course_id)
  - back-to-dashboard: url_for('dashboard')

---

### templates/course_details.html
- Page Title: Course Details
- <title> and <h1>: "Course Details"
- Element IDs:
  - course-details-page (Div)
  - course-title (H1) - Displays {{ course.title }}
  - course-description (Div) - Displays {{ course.description }}
  - enroll-button (Button) - Shows "Enroll" or "Already Enrolled" disabled if enrolled
  - back-to-catalog (Button) - Navigates back to catalog
- Context Variables:
  - course (dict)
  - enrolled (bool)
  - enrollment_date (str or None)
  - enroll_success (bool)
  - error_message (str or None)
- Navigation url_for Mappings:
  - enroll-button (POST form): action="{{ url_for('enroll_course', course_id=course.course_id) }}"
  - back-to-catalog: url_for('course_catalog')
- Form Fields:
  - enroll-button is a form button submitting POST request to enroll_course route

---

### templates/my_courses.html
- Page Title: My Courses
- <title> and <h1>: "My Courses"
- Element IDs:
  - my-courses-page (Div)
  - courses-list (Div) - List of courses with progress
  - continue-learning-button-{{ course.course_id }} (Button) - Continue learning
  - back-to-dashboard (Button) - Navigate back to dashboard
- Context Variables:
  - enrolled_courses (list of dict)
  - username (str)
- Navigation url_for Mappings:
  - continue-learning-button-{{ course.course_id }}: url_for('course_learning', course_id=course.course_id)
  - back-to-dashboard: url_for('dashboard')

---

### templates/course_learning.html
- Page Title: Course Learning
- <title> and <h1>: "Course Learning"
- Element IDs:
  - learning-page (Div)
  - lessons-list (Div) - List lessons with titles
  - lesson-content (Div) - Current lesson content
  - mark-complete-button (Button) - Mark current lesson complete
  - back-to-my-courses (Button) - Navigate back to my courses
- Context Variables:
  - course (dict)
  - lessons (list of dict)
  - current_lesson (dict)
  - progress (int)
  - lesson_index (int)
  - mark_success (bool)
  - error_message (str or None)
- Navigation url_for Mappings:
  - mark-complete-button (POST form): action="{{ url_for('mark_lesson_complete', course_id=course.course_id) }}"
  - back-to-my-courses: url_for('my_courses')
- Notes:
  - Lessons must be completed sequentially
  - Progress updated on marking complete

---

### templates/assignments.html
- Page Title: My Assignments
- <title> and <h1>: "My Assignments"
- Element IDs:
  - assignments-page (Div)
  - assignments-table (Table) - Lists assignments
  - submit-assignment-button-{{ assignment.assignment_id }} (Button) - Submit assignment
  - back-to-dashboard (Button) - Navigate back to dashboard
- Context Variables:
  - assignments (list of dict)
  - username (str)
  - submissions_status (dict keyed by assignment_id: str status)
- Navigation url_for Mappings:
  - submit-assignment-button-{{ assignment.assignment_id }}: url_for('submit_assignment', assignment_id=assignment.assignment_id)
  - back-to-dashboard: url_for('dashboard')

---

### templates/submit_assignment.html
- Page Title: Submit Assignment
- <title> and <h1>: "Submit Assignment"
- Element IDs:
  - submit-page (Div)
  - assignment-info (Div) - Title and description
  - submission-text (Textarea)
  - submit-button (Button)
  - back-to-assignments (Button)
- Context Variables:
  - assignment (dict)
  - submission_text (str)
  - submit_success (bool)
  - error_message (str or None)
- Navigation url_for Mappings:
  - submit-button (POST form): action="{{ url_for('submit_assignment_post', assignment_id=assignment.assignment_id) }}"
  - back-to-assignments: url_for('my_assignments')

---

### templates/certificates.html
- Page Title: My Certificates
- <title> and <h1>: "My Certificates"
- Element IDs:
  - certificates-page (Div)
  - certificates-grid (Div) - Grid of certificate cards
  - back-to-dashboard (Button)
- Context Variables:
  - certificates (list of dict)
  - username (str)
- Navigation url_for Mappings:
  - back-to-dashboard: url_for('dashboard')

---

### templates/profile.html
- Page Title: My Profile
- <title> and <h1>: "My Profile"
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
- Navigation url_for Mappings:
  - update-profile-button (POST form): action="{{ url_for('update_profile') }}"
  - back-to-dashboard: url_for('dashboard')

---

## Section 3: Data File Schemas (For Backend Developer)

### data/users.txt
- Fields (pipe-delimited): username|email|fullname
- Description: Stores user login and profile information.
- Examples:
  john|john@student.com|John Student
  alice|alice@instructor.com|Alice Professor
  jane|jane@student.com|Jane Learner

---

### data/courses.txt
- Fields (pipe-delimited): course_id|title|description|category|level|duration|status
- Description: Contains course metadata and status.
- Examples:
  1|Python Programming|Learn Python from scratch|Programming|Beginner|40 hours|Active
  2|Web Development|Build modern websites|Web|Intermediate|60 hours|Active
  3|Data Science|Introduction to data analysis|Data|Advanced|80 hours|Active

---

### data/enrollments.txt
- Fields (pipe-delimited): enrollment_id|username|course_id|enrollment_date|progress|status
- Description: Tracks which users are enrolled in which courses, progress and status.
- Examples:
  1|john|1|2024-11-01|75|In Progress
  2|jane|1|2024-10-15|100|Completed
  3|john|2|2024-11-10|25|In Progress

---

### data/assignments.txt
- Fields (pipe-delimited): assignment_id|course_id|title|description|due_date|max_points
- Description: Lists assignments associated with courses.
- Examples:
  1|1|Python Basics Quiz|Complete the quiz on variables and data types|2024-12-01|100
  2|1|Final Project|Build a calculator application|2024-12-15|200

---

### data/submissions.txt
- Fields (pipe-delimited): submission_id|assignment_id|username|submission_text|submit_date|grade|feedback
- Description: Stores student assignment submissions and grading info.
- Examples:
  1|1|john|My answers are...|2024-11-25|85|Good work!
  2|2|jane|Here is my project...|2024-11-20|95|Excellent!

---

### data/certificates.txt
- Fields (pipe-delimited): certificate_id|username|course_id|issue_date
- Description: Records certificate issuance on course completion.
- Examples:
  1|jane|1|2024-11-22

