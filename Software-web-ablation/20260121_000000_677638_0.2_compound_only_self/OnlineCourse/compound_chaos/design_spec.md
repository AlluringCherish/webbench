# OnlineCourse Application Design Specification

---

## 1. Flask Routes Specification (for Backend Developer)

| Route Path                      | Function Name             | HTTP Method | Template File           | Context Variables                                 |
|--------------------------------|---------------------------|-------------|------------------------|--------------------------------------------------|
| /                              | home_redirect              | GET         | None                   | None (Redirects to Dashboard)                     |
| /dashboard                     | dashboard                 | GET         | dashboard.html          | username (str), fullname (str), enrolled_courses (list of dict) |
| /catalog                      | course_catalog            | GET         | catalog.html            | courses (list of dict), search_query (str, optional)          |
| /course/<int:course_id>       | course_details            | GET, POST  | course_details.html     | course (dict), already_enrolled (bool)           |
| /my-courses                   | my_courses                | GET         | my_courses.html         | enrolled_courses (list of dict)                   |
| /learning/<int:course_id>     | course_learning           | GET, POST  | learning.html           | course (dict), lessons (list of dict), current_lesson (dict), progress (int), can_mark_complete (bool) |
| /assignments                 | my_assignments            | GET         | assignments.html        | assignments (list of dict)                         |
| /submit-assignment/<int:assignment_id> | submit_assignment         | GET, POST  | submit_assignment.html  | assignment (dict), submission_status (str, optional), confirmation (str, optional) |
| /certificates                | certificates              | GET         | certificates.html       | certificates (list of dict)                       |
| /profile                     | user_profile              | GET, POST  | profile.html            | user_profile (dict), update_status (str, optional)            |

---

### Notes on Critical Logic

- **Enrollment:** POST on `/course/<course_id>` route to enroll user. Creates a new entry in `enrollments.txt` with 0% progress, `In Progress` status, and current date.
- **Progress Updates:** POST on `/learning/<course_id>` when marking lesson complete increments progress ((completed lessons / total lessons) * 100) and updates `enrollments.txt` progress field.
- **Sequential Lesson Completion:** Lessons must be completed in order. The `can_mark_complete` context variable is set accordingly to disable/enable the "Mark Complete" button.
- **Assignment Submissions:** POST on `/submit-assignment/<assignment_id>` stores submission in `submissions.txt` with status "Submitted", records current submission date.
- **Certificate Generation:** Upon reaching 100% progress, a certificate entry is generated in `certificates.txt` with current date.

---

## 2. HTML Template Specifications (for Frontend Developer)

---

### dashboard.html
- File Path: templates/dashboard.html
- Page Title: Learning Dashboard
- <title>: Learning Dashboard
- <h1 id="welcome-message">: Welcome, {{ fullname }}
- Element IDs:
  - dashboard-page
  - welcome-message
  - enrolled-courses
  - browse-courses-button
  - my-courses-button
- Context Variables:
  - username (str)
  - fullname (str)
  - enrolled_courses (list of dict with keys: course_id (int), title (str), progress (int))
- Navigation Using Flask's url_for:
  - browse-courses-button: url_for('course_catalog')
  - my-courses-button: url_for('my_courses')

---

### catalog.html
- File Path: templates/catalog.html
- Page Title: Available Courses
- <title>: Available Courses
- <h1>: Available Courses
- Element IDs:
  - catalog-page
  - search-input
  - course-grid
  - back-to-dashboard
  - {% raw %}{% for course in courses %} view-course-button-{{ course.course_id }} {% endfor %}{% endraw %} (dynamic)
- Context Variables:
  - courses (list of dict with keys: course_id (int), title (str), description (str), category (str), level (str), duration (str), status (str))
  - search_query (str, optional)
- Navigation:
  - back-to-dashboard: url_for('dashboard')
  - view-course-button-{{ course.course_id }}: url_for('course_details', course_id=course.course_id)

---

### course_details.html
- File Path: templates/course_details.html
- Page Title: Course Details
- <title>: Course Details
- <h1 id="course-title">: {{ course.title }}
- Element IDs:
  - course-details-page
  - course-title
  - course-description
  - enroll-button
  - back-to-catalog
- Context Variables:
  - course (dict with keys: course_id (int), title (str), description (str), category (str), level (str), duration (str), status (str))
  - already_enrolled (bool)
- Navigation:
  - back-to-catalog: url_for('course_catalog')
- Button States:
  - enroll-button: disabled if already_enrolled is True, otherwise enabled
- Form Submission:
  - POST to same route `/course/<course_id>` to enroll

---

### my_courses.html
- File Path: templates/my_courses.html
- Page Title: My Courses
- <title>: My Courses
- <h1>: My Courses
- Element IDs:
  - my-courses-page
  - courses-list
  - back-to-dashboard
  - {% raw %}{% for course in enrolled_courses %} continue-learning-button-{{ course.course_id }} {% endfor %}{% endraw %} (dynamic)
- Context Variables:
  - enrolled_courses (list of dict with keys: course_id (int), title (str), progress (int))
- Navigation:
  - back-to-dashboard: url_for('dashboard')
  - continue-learning-button-{{ course.course_id }}: url_for('course_learning', course_id=course.course_id)

---

### learning.html
- File Path: templates/learning.html
- Page Title: Course Learning
- <title>: Course Learning
- <h1>: {{ course.title }}
- Element IDs:
  - learning-page
  - lessons-list
  - lesson-content
  - mark-complete-button
  - back-to-my-courses
- Context Variables:
  - course (dict with keys: course_id (int), title (str), description (str), category (str), level (str), duration (str), status (str))
  - lessons (list of dict with keys: lesson_number (int), title (str), content (str))
  - current_lesson (dict with keys: lesson_number (int), title (str), content (str))
  - progress (int)
  - can_mark_complete (bool)
- Navigation:
  - back-to-my-courses: url_for('my_courses')
- Button States:
  - mark-complete-button: disabled if can_mark_complete is False, otherwise enabled
- Form Submission:
  - POST to same route `/learning/<course_id>` to mark lesson complete

---

### assignments.html
- File Path: templates/assignments.html
- Page Title: My Assignments
- <title>: My Assignments
- <h1>: My Assignments
- Element IDs:
  - assignments-page
  - assignments-table
  - back-to-dashboard
  - {% raw %}{% for assignment in assignments %} submit-assignment-button-{{ assignment.assignment_id }} {% endfor %}{% endraw %} (dynamic)
- Context Variables:
  - assignments (list of dict with keys: assignment_id (int), course_id (int), title (str), description (str), due_date (str), max_points (int))
- Navigation:
  - back-to-dashboard: url_for('dashboard')
  - submit-assignment-button-{{ assignment.assignment_id }}: url_for('submit_assignment', assignment_id=assignment.assignment_id)

---

### submit_assignment.html
- File Path: templates/submit_assignment.html
- Page Title: Submit Assignment
- <title>: Submit Assignment
- <h1>: Submit Assignment
- Element IDs:
  - submit-page
  - assignment-info
  - submission-text
  - submit-button
  - back-to-assignments
- Context Variables:
  - assignment (dict with keys: assignment_id (int), course_id (int), title (str), description (str), due_date (str), max_points (int))
  - submission_status (str, optional)
  - confirmation (str, optional)
- Navigation:
  - back-to-assignments: url_for('my_assignments')
- Button States:
  - submit-button: enabled always
- Form Submission:
  - POST to same route `/submit-assignment/<assignment_id>`

---

### certificates.html
- File Path: templates/certificates.html
- Page Title: My Certificates
- <title>: My Certificates
- <h1>: My Certificates
- Element IDs:
  - certificates-page
  - certificates-grid
  - back-to-dashboard
- Context Variables:
  - certificates (list of dict with keys: certificate_id (int), username (str), course_id (int), issue_date (str))
- Navigation:
  - back-to-dashboard: url_for('dashboard')

---

### profile.html
- File Path: templates/profile.html
- Page Title: My Profile
- <title>: My Profile
- <h1>: My Profile
- Element IDs:
  - profile-page
  - profile-email
  - profile-fullname
  - update-profile-button
  - back-to-dashboard
- Context Variables:
  - user_profile (dict with keys: username (str), email (str), fullname (str))
  - update_status (str, optional)
- Navigation:
  - back-to-dashboard: url_for('dashboard')
- Button States:
  - update-profile-button: enabled always
- Form Submission:
  - POST to same route `/profile`

---

## 3. Data File Schemas (for Backend Developer)

---

### users.txt
- File Path: data/users.txt
- Pipe-delimited Fields:
  1. username (str): Unique user identifier
  2. email (str): User email address
  3. fullname (str): User full name
- Example Lines:
  ```
  john|john@student.com|John Student
  alice|alice@instructor.com|Alice Professor
  jane|jane@student.com|Jane Learner
  ```

---

### courses.txt
- File Path: data/courses.txt
- Pipe-delimited Fields:
  1. course_id (int): Unique course identifier
  2. title (str): Course title
  3. description (str): Detailed course description
  4. category (str): Course category
  5. level (str): Difficulty level (e.g., Beginner, Intermediate, Advanced)
  6. duration (str): Total hours (e.g., "40 hours")
  7. status (str): Current status (e.g., Active)
- Example Lines:
  ```
  1|Python Programming|Learn Python from scratch|Programming|Beginner|40 hours|Active
  2|Web Development|Build modern websites|Web|Intermediate|60 hours|Active
  3|Data Science|Introduction to data analysis|Data|Advanced|80 hours|Active
  ```

---

### enrollments.txt
- File Path: data/enrollments.txt
- Pipe-delimited Fields:
  1. enrollment_id (int): Unique enrollment identifier
  2. username (str): User enrolled
  3. course_id (int): Course identifier
  4. enrollment_date (str): Date enrolled, format YYYY-MM-DD
  5. progress (int): Percentage progress (0-100)
  6. status (str): Enrollment status ("In Progress", "Completed")
- Example Lines:
  ```
  1|john|1|2024-11-01|75|In Progress
  2|jane|1|2024-10-15|100|Completed
  3|john|2|2024-11-10|25|In Progress
  ```

---

### assignments.txt
- File Path: data/assignments.txt
- Pipe-delimited Fields:
  1. assignment_id (int): Unique assignment identifier
  2. course_id (int): Associated course identifier
  3. title (str): Assignment title
  4. description (str): Assignment details
  5. due_date (str): Due date, format YYYY-MM-DD
  6. max_points (int): Maximum points achievable
- Example Lines:
  ```
  1|1|Python Basics Quiz|Complete the quiz on variables and data types|2024-12-01|100
  2|1|Final Project|Build a calculator application|2024-12-15|200
  ```

---

### submissions.txt
- File Path: data/submissions.txt
- Pipe-delimited Fields:
  1. submission_id (int): Unique submission identifier
  2. assignment_id (int): Related assignment identifier
  3. username (str): User submitting
  4. submission_text (str): Text content of submission
  5. submit_date (str): Submission date, format YYYY-MM-DD
  6. grade (int): Grade awarded
  7. feedback (str): Instructor feedback
- Example Lines:
  ```
  1|1|john|My answers are...|2024-11-25|85|Good work!
  2|2|jane|Here is my project...|2024-11-20|95|Excellent!
  ```

---

### certificates.txt
- File Path: data/certificates.txt
- Pipe-delimited Fields:
  1. certificate_id (int): Unique certificate identifier
  2. username (str): User earning certificate
  3. course_id (int): Course completed
  4. issue_date (str): Date issued, format YYYY-MM-DD
- Example Lines:
  ```
  1|jane|1|2024-11-22
  ```

---

End of Design Specification
