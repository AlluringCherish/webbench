# OnlineCourse Application Design Specification

---

## Section 1: Flask Routes Specification (For Backend Developer)

| Route Path                           | Function Name           | HTTP Method | Template File           | Context Variables                                                                                                           |
|------------------------------------|-------------------------|-------------|-------------------------|----------------------------------------------------------------------------------------------------------------------------|
| /                                  | root                    | GET         | N/A                     | N/A (Redirects to /dashboard)                                                                                              |
| /dashboard                         | dashboard               | GET         | dashboard.html          | username (str), fullname (str), enrolled_courses (list of dict {course_id (str), title (str), progress (int)})              |
| /catalog                          | course_catalog          | GET         | catalog.html            | courses (list of dict {course_id (str), title (str), description (str), category (str), level (str), duration (str), status (str)}) |
| /catalog/search                   | course_catalog_search   | POST        | catalog.html            | courses (list of dict) (filtered as per search)                                                                             |
| /course/<course_id>               | course_details          | GET         | course_details.html     | course (dict with keys: course_id (str), title (str), description (str), category (str), level (str), duration (str), status (str)),
|                                    |                         |             |                         | is_enrolled (bool)                                                                                                         |
| /course/<course_id>/enroll        | enroll_course           | POST        | course_details.html     | course (dict), is_enrolled (bool), success_message (str, optional), error_message (str, optional)                            |
| /my-courses                      | my_courses              | GET         | my_courses.html         | enrolled_courses (list of dict {course_id (str), title (str), progress (int)})                                              |
| /my-courses/<course_id>/learn    | course_learning         | GET         | course_learning.html    | course (dict: course_id, title, description, etc.), lessons (list of dict {lesson_id (str), title (str), content (str)}), current_lesson (dict), progress (int, 0-100)                |
| /my-courses/<course_id>/mark-complete | mark_lesson_complete | POST        | course_learning.html    | course (dict), lessons (list), current_lesson (dict), progress (int), success_message (str, optional), error_message (str, optional) |
| /assignments                    | my_assignments          | GET         | assignments.html        | assignments (list of dict {assignment_id (str), course_id (str), title (str), description (str), due_date (str), max_points (int)}) |
| /assignments/<assignment_id>/submit | submit_assignment_form | GET         | submit_assignment.html  | assignment (dict with keys: assignment_id, course_id, title, description, due_date, max_points)                              |
| /assignments/<assignment_id>/submit | submit_assignment     | POST        | submit_assignment.html  | assignment (dict), success_message (str, optional), error_message (str, optional)                                            |
| /certificates                   | certificates            | GET         | certificates.html       | certificates (list of dict {certificate_id (str), username (str), course_id (str), issue_date (str), course_title (str)})      |
| /profile                       | user_profile            | GET         | profile.html            | user (dict with keys: username (str), email (str), fullname (str))                                                          |
| /profile/update                 | update_profile          | POST        | profile.html            | user (dict), success_message (str, optional), error_message (str, optional)                                                  |

**Notes:**
- Enrollment date recorded on /course/<course_id>/enroll POST.
- Enrollment progress initialized to 0.
- Submissions posted on assignment submission page update submissions.txt.
- Marking lesson complete updates enrollments progress and may generate certificate if progress reaches 100%.
- Certificate stored with issue date when course completed.
- Course completion defined by 100% progress.

---

## Section 2: HTML Template Specifications (For Frontend Developer)

### templates/dashboard.html
- Page Title: Learning Dashboard
- <title> and <h1>: "Learning Dashboard"
- Element IDs:
  - dashboard-page (div)
  - welcome-message (h1) — Displays "Welcome, {{ fullname }}"
  - enrolled-courses (div) — Iterates over enrolled_courses with each course displaying title and progress
  - browse-courses-button (button) — Navigates to url_for('course_catalog')
  - my-courses-button (button) — Navigates to url_for('my_courses')
- Context Variables:
  - username (str)
  - fullname (str)
  - enrolled_courses (list of dict):
    - course_id (str)
    - title (str)
    - progress (int)

---

### templates/catalog.html
- Page Title: Available Courses
- <title> and <h1>: "Available Courses"
- Element IDs:
  - catalog-page (div)
  - search-input (input, text) — Form field name: "search"
  - course-grid (div)
  - view-course-button-{course_id} (button) — ID pattern: "view-course-button-{{ course.course_id }}" to view details via url_for('course_details', course_id=course.course_id)
  - back-to-dashboard (button) — url_for('dashboard')
- Context Variables:
  - courses (list of dict):
    - course_id (str)
    - title (str)
    - description (str)
    - category (str)
    - level (str)
    - duration (str)
    - status (str)
- Notes:
  - Search form POSTs to url_for('course_catalog_search')

---

### templates/course_details.html
- Page Title: Course Details
- <title> and <h1>: "Course Details"
- Element IDs:
  - course-details-page (div)
  - course-title (h1) — Displays {{ course.title }}
  - course-description (div) — Displays {{ course.description }}
  - enroll-button (button) — Disabled if {{ is_enrolled }} is True. Text: "Enroll" or "Already Enrolled"
  - back-to-catalog (button) — url_for('course_catalog')
- Context Variables:
  - course (dict)
  - is_enrolled (bool)
  - Optional: success_message (str)
  - Optional: error_message (str)
- Notes:
  - Enroll button POSTs to url_for('enroll_course', course_id=course.course_id)

---

### templates/my_courses.html
- Page Title: My Courses
- <title> and <h1>: "My Courses"
- Element IDs:
  - my-courses-page (div)
  - courses-list (div)
  - continue-learning-button-{course_id} (button) — ID pattern: "continue-learning-button-{{ course.course_id }}" links to url_for('course_learning', course_id=course.course_id)
  - back-to-dashboard (button) — url_for('dashboard')
- Context Variables:
  - enrolled_courses (list of dict):
    - course_id (str)
    - title (str)
    - progress (int)

---

### templates/course_learning.html
- Page Title: Course Learning
- <title> and <h1>: "Course Learning"
- Element IDs:
  - learning-page (div)
  - lessons-list (div) — Lists all lessons titles
  - lesson-content (div) — Content of current lesson
  - mark-complete-button (button) — POSTs to url_for('mark_lesson_complete', course_id=course.course_id)
  - back-to-my-courses (button) — url_for('my_courses')
- Context Variables:
  - course (dict)
  - lessons (list of dict):
    - lesson_id (str)
    - title (str)
    - content (str)
  - current_lesson (dict)
  - progress (int)
- Notes:
  - Mark complete button disabled if current lesson is the last and all completed
  - Lessons must be completed in sequence

---

### templates/assignments.html
- Page Title: My Assignments
- <title> and <h1>: "My Assignments"
- Element IDs:
  - assignments-page (div)
  - assignments-table (table) — Displays assignment rows
  - submit-assignment-button-{assignment_id} (button) — ID pattern: "submit-assignment-button-{{ assignment.assignment_id }}" links to url_for('submit_assignment_form', assignment_id=assignment.assignment_id)
  - back-to-dashboard (button) — url_for('dashboard')
- Context Variables:
  - assignments (list of dict):
    - assignment_id (str)
    - course_id (str)
    - title (str)
    - description (str)
    - due_date (str)
    - max_points (int)

---

### templates/submit_assignment.html
- Page Title: Submit Assignment
- <title> and <h1>: "Submit Assignment"
- Element IDs:
  - submit-page (div)
  - assignment-info (div) — Displays assignment title and description
  - submission-text (textarea)
  - submit-button (button) — POSTs to url_for('submit_assignment', assignment_id=assignment.assignment_id)
  - back-to-assignments (button) — url_for('my_assignments')
- Context Variables:
  - assignment (dict)
  - Optional: success_message (str)
  - Optional: error_message (str)
- Notes:
  - Form submission includes textarea named "submission_text"

---

### templates/certificates.html
- Page Title: My Certificates
- <title> and <h1>: "My Certificates"
- Element IDs:
  - certificates-page (div)
  - certificates-grid (div) — Lists certificates with course titles and issue dates
  - back-to-dashboard (button) — url_for('dashboard')
- Context Variables:
  - certificates (list of dict):
    - certificate_id (str)
    - username (str)
    - course_id (str)
    - issue_date (str)
    - course_title (str)

---

### templates/profile.html
- Page Title: My Profile
- <title> and <h1>: "My Profile"
- Element IDs:
  - profile-page (div)
  - profile-email (input, type=email, name=email)
  - profile-fullname (input, type=text, name=fullname)
  - update-profile-button (button) — POSTs to url_for('update_profile')
  - back-to-dashboard (button) — url_for('dashboard')
- Context Variables:
  - user (dict):
    - username (str)
    - email (str)
    - fullname (str)
- Notes:
  - Form fields with names "email" and "fullname"

---

## Section 3: Data File Schemas (For Backend Developer)

### data/users.txt
- Fields: username|email|fullname
- Description: Each user with username identifier, contact email, and full name
- Examples:
```
john|john@student.com|John Student
alice|alice@instructor.com|Alice Professor
jane|jane@student.com|Jane Learner
```

---

### data/courses.txt
- Fields: course_id|title|description|category|level|duration|status
- Description: Each course with unique ID, title, detail, category, level, total duration, and status (e.g., Active)
- Examples:
```
1|Python Programming|Learn Python from scratch|Programming|Beginner|40 hours|Active
2|Web Development|Build modern websites|Web|Intermediate|60 hours|Active
3|Data Science|Introduction to data analysis|Data|Advanced|80 hours|Active
```

---

### data/enrollments.txt
- Fields: enrollment_id|username|course_id|enrollment_date|progress|status
- Description: User enrollments with progress percentage and status
- Examples:
```
1|john|1|2024-11-01|75|In Progress
2|jane|1|2024-10-15|100|Completed
3|john|2|2024-11-10|25|In Progress
```
- Notes:
  - enrollment_date format: YYYY-MM-DD
  - progress: integer 0 to 100
  - status: "In Progress" or "Completed"

---

### data/assignments.txt
- Fields: assignment_id|course_id|title|description|due_date|max_points
- Description: Assignments per course with deadlines and points
- Examples:
```
1|1|Python Basics Quiz|Complete the quiz on variables and data types|2024-12-01|100
2|1|Final Project|Build a calculator application|2024-12-15|200
```
- Notes:
  - due_date format: YYYY-MM-DD

---

### data/submissions.txt
- Fields: submission_id|assignment_id|username|submission_text|submit_date|grade|feedback
- Description: User submissions with grading and feedback
- Examples:
```
1|1|john|My answers are...|2024-11-25|85|Good work!
2|2|jane|Here is my project...|2024-11-20|95|Excellent!
```
- Notes:
  - submit_date format: YYYY-MM-DD
  - grade: integer or empty if not graded
  - feedback: string or empty

---

### data/certificates.txt
- Fields: certificate_id|username|course_id|issue_date
- Description: Issued course completion certificates
- Examples:
```
1|jane|1|2024-11-22
```
- Notes:
  - issue_date format: YYYY-MM-DD
