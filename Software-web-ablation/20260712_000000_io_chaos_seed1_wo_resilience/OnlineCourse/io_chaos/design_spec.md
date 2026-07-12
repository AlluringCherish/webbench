# OnlineCourse Application Design Specifications

---

## Section 1: Flask Routes Specification (For Backend Developer)

| Route Path                          | Function Name              | HTTP Method | Template File         | Context Variables                              |
|-----------------------------------|----------------------------|-------------|-----------------------|-----------------------------------------------|
| /                                 | root_redirect              | GET         | None (redirect)        | None                                          |
| /dashboard                        | dashboard                  | GET         | dashboard.html         | username (str), fullname (str), enrolled_courses (list of dict {course_id, title, progress(float)}) |
| /catalog                         | course_catalog             | GET         | catalog.html           | courses (list of dict {course_id, title, description, category, level, duration, status}), search_query (str) |
| /course/<int:course_id>          | course_details             | GET, POST   | course_details.html    | course (dict {course_id, title, description, category, level, duration, status}), enrolled (bool) |
| /my-courses                     | my_courses                 | GET         | my_courses.html        | username (str), enrolled_courses (list of dict {course_id, title, progress(float)}) |
| /learning/<int:course_id>        | course_learning            | GET, POST   | course_learning.html   | course (dict), lessons (list of dict {lesson_id, title, content}), current_lesson (dict), progress (float), enrollment_id (int) |
| /assignments                    | my_assignments             | GET         | assignments.html       | username (str), assignments (list of dict {assignment_id, title, description, due_date, max_points, status(str)}) |
| /submit-assignment/<int:assignment_id> | submit_assignment           | GET, POST   | submit_assignment.html | assignment (dict), submission_status (str), confirmation_message (str or None) |
| /certificates                  | certificates_page          | GET         | certificates.html      | username (str), certificates (list of dict {certificate_id, course_id, title, issue_date}) |
| /profile                      | user_profile               | GET, POST   | profile.html           | user (dict: username, email, fullname), update_status (str or None) |

**Logic Notes:**
- Enrollment POST updates enrollments.txt with new enrollment_id, username, course_id, current date, progress 0, status 'In Progress'. If already enrolled, disables button.
- Progress update POST on course_learning marks lesson complete, updates enrollments.txt progress (percent completion), status updated to 'Completed' if progress 100%, triggers certificate creation if completed.
- Assignment submission POST adds entry in submissions.txt with status "Submitted" and submit_date recorded.
- Certificate generation occurs automatically on course completion.

---

## Section 2: HTML Template Specifications (For Frontend Developer)

### templates/dashboard.html
- Page Title: Learning Dashboard
- <title> and <h1> text exactly: "Learning Dashboard"
- Elements:
  - #dashboard-page (Div container)
  - #welcome-message (H1) - Displays user's full name using {{ fullname }}
  - #enrolled-courses (Div) - Iterates over enrolled_courses for display
  - #browse-courses-button (Button) - onClick navigates to url_for('course_catalog')
  - #my-courses-button (Button) - onClick navigates to url_for('my_courses')
- Context Variables:
  - username (str)
  - fullname (str)
  - enrolled_courses (list of dict with course_id, title, progress (float))

### templates/catalog.html
- Page Title: Available Courses
- <title> and <h1>: "Available Courses"
- Elements:
  - #catalog-page (Div container)
  - #search-input (Input text for search)
  - #course-grid (Div) - iterates over courses to display cards
  - #view-course-button-{{ course.course_id }} (Button) for each course
  - #back-to-dashboard (Button) - navigates to url_for('dashboard')
- Context Variables:
  - courses (list of dict: course_id, title, description, category, level, duration, status)
  - search_query (str)

### templates/course_details.html
- Page Title: Course Details
- <title> and <h1>: "Course Details"
- Elements:
  - #course-details-page (Div container)
  - #course-title (H1) - {{ course.title }}
  - #course-description (Div) - {{ course.description }}
  - #enroll-button (Button)
    - Disabled and text "Already Enrolled" if enrolled == True
    - Enabled with text "Enroll" if enrolled == False
  - #back-to-catalog (Button) - navigates to url_for('course_catalog')
- Context Variables:
  - course (dict: course_id, title, description, category, level, duration, status)
  - enrolled (bool)
- POST form on #enroll-button posts to same route /course/<course_id>

### templates/my_courses.html
- Page Title: My Courses
- <title> and <h1>: "My Courses"
- Elements:
  - #my-courses-page (Div container)
  - #courses-list (Div) - iterates over enrolled_courses
  - #continue-learning-button-{{ course.course_id }} (Button) for each enrolled course
  - #back-to-dashboard (Button) - navigates to url_for('dashboard')
- Context Variables:
  - username (str)
  - enrolled_courses (list of dict with course_id, title, progress(float))

### templates/course_learning.html
- Page Title: Course Learning
- <title> and <h1>: "Course Learning"
- Elements:
  - #learning-page (Div container)
  - #lessons-list (Div) - list of lessons
  - #lesson-content (Div) - shows current lesson content
  - #mark-complete-button (Button) - to mark lesson complete
  - #back-to-my-courses (Button) - navigates to url_for('my_courses')
- Context Variables:
  - course (dict)
  - lessons (list of dict with lesson_id, title, content)
  - current_lesson (dict)
  - progress (float)  
  - enrollment_id (int)
- POST handled to mark completion on same route /learning/<course_id>

### templates/assignments.html
- Page Title: My Assignments
- <title> and <h1>: "My Assignments"
- Elements:
  - #assignments-page (Div container)
  - #assignments-table (Table) - lists assignments
  - #submit-assignment-button-{{ assignment.assignment_id }} (Button) for each pending assignment
  - #back-to-dashboard (Button) - navigates to url_for('dashboard')
- Context Variables:
  - username (str)
  - assignments (list of dict with assignment_id, title, description, due_date, max_points, status)

### templates/submit_assignment.html
- Page Title: Submit Assignment
- <title> and <h1>: "Submit Assignment"
- Elements:
  - #submit-page (Div container)
  - #assignment-info (Div) - shows assignment title and description
  - #submission-text (Textarea)
  - #submit-button (Button) - submits form
  - #back-to-assignments (Button) - navigates to url_for('my_assignments')
- Context Variables:
  - assignment (dict)
  - submission_status (str)
  - confirmation_message (str or None)
- Form POST to /submit-assignment/<assignment_id>

### templates/certificates.html
- Page Title: My Certificates
- <title> and <h1>: "My Certificates"
- Elements:
  - #certificates-page (Div container)
  - #certificates-grid (Div) - grids over certificates
  - #back-to-dashboard (Button) - navigates to url_for('dashboard')
- Context Variables:
  - username (str)
  - certificates (list of dict {certificate_id, course_id, title, issue_date})

### templates/profile.html
- Page Title: My Profile
- <title> and <h1>: "My Profile"
- Elements:
  - #profile-page (Div container)
  - #profile-email (Input) - input for email
  - #profile-fullname (Input) - input for full name
  - #update-profile-button (Button) - posts form
  - #back-to-dashboard (Button) - navigates to url_for('dashboard')
- Context Variables:
  - user (dict with username, email, fullname)
  - update_status (str or None)
- Form POST to /profile

---

## Section 3: Data File Schemas (For Backend Developer)

### data/users.txt
- Format: `username|email|fullname`
- Fields:
  - username: unique user login ID
  - email: user email
  - fullname: user's full name
- Examples:
  ```
  john|john@student.com|John Student
  alice|alice@instructor.com|Alice Professor
  jane|jane@student.com|Jane Learner
  ```

### data/courses.txt
- Format: `course_id|title|description|category|level|duration|status`
- Fields:
  - course_id: unique numeric ID
  - title: course title
  - description: full course description
  - category: course category (Programming, Web, Data, etc.)
  - level: difficulty level string
  - duration: string e.g. '40 hours'
  - status: course status e.g. Active
- Examples:
  ```
  1|Python Programming|Learn Python from scratch|Programming|Beginner|40 hours|Active
  2|Web Development|Build modern websites|Web|Intermediate|60 hours|Active
  3|Data Science|Introduction to data analysis|Data|Advanced|80 hours|Active
  ```

### data/enrollments.txt
- Format: `enrollment_id|username|course_id|enrollment_date|progress|status`
- Fields:
  - enrollment_id: unique numeric ID
  - username: user login ID
  - course_id: numeric course ID
  - enrollment_date: date YYYY-MM-DD
  - progress: numeric percent 0-100
  - status: string (In Progress, Completed)
- Examples:
  ```
  1|john|1|2024-11-01|75|In Progress
  2|jane|1|2024-10-15|100|Completed
  3|john|2|2024-11-10|25|In Progress
  ```

### data/assignments.txt
- Format: `assignment_id|course_id|title|description|due_date|max_points`
- Fields:
  - assignment_id: unique numeric ID
  - course_id: numeric course ID
  - title: assignment title
  - description: assignment description
  - due_date: date YYYY-MM-DD
  - max_points: numeric max score
- Examples:
  ```
  1|1|Python Basics Quiz|Complete the quiz on variables and data types|2024-12-01|100
  2|1|Final Project|Build a calculator application|2024-12-15|200
  ```

### data/submissions.txt
- Format: `submission_id|assignment_id|username|submission_text|submit_date|grade|feedback`
- Fields:
  - submission_id: unique numeric ID
  - assignment_id: numeric assignment ID
  - username: user login ID
  - submission_text: free text answer
  - submit_date: date YYYY-MM-DD
  - grade: numeric score
  - feedback: textual feedback
- Examples:
  ```
  1|1|john|My answers are...|2024-11-25|85|Good work!
  2|2|jane|Here is my project...|2024-11-20|95|Excellent!
  ```

### data/certificates.txt
- Format: `certificate_id|username|course_id|issue_date`
- Fields:
  - certificate_id: unique numeric ID
  - username: user login ID
  - course_id: numeric course ID
  - issue_date: date YYYY-MM-DD
- Examples:
  ```
  1|jane|1|2024-11-22
  ```

---

Résumé: Backend implements routing and data management with defined schemas; Frontend implements templates with detailed elements and navigation. Both can proceed independently with these specifications.