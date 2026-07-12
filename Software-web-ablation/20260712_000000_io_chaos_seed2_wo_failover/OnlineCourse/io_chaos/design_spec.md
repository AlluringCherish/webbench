# OnlineCourse Web Application Design Specification

---

## Section 1: Flask Routes Specification (For Backend Developer)

| Route Path                     | Function Name             | HTTP Method | Template File           | Context Variables                                                                                       |
|-------------------------------|---------------------------|-------------|------------------------|-------------------------------------------------------------------------------------------------------|
| /                             | root_redirect             | GET         | -                      | - Redirects to /dashboard                                                                              |
| /dashboard                    | dashboard                 | GET         | dashboard.html          | username (str), fullname (str), enrolled_courses (list of dicts with course_id, title, progress (int)) |
| /catalog                     | course_catalog            | GET         | course_catalog.html     | username (str), courses (list of dicts with course_id, title, description, category, level, duration, status) |
| /course/<int:course_id>       | course_details            | GET, POST   | course_details.html     | username (str), course (dict: course_id, title, description, category, level, duration, status), enrolled (bool), enrollment_date (str or None) |
| /my-courses                  | my_courses                | GET         | my_courses.html         | username (str), enrolled_courses (list of dicts with course_id, title, progress (int))                |
| /learn/<int:course_id>        | course_learning           | GET, POST   | course_learning.html    | username (str), course (dict), lessons (list of dicts: lesson_id, title, content),
  current_lesson (dict), completed_lessons (list of lesson_ids), progress (int), can_mark_complete (bool) |
| /assignments                 | my_assignments            | GET         | my_assignments.html     | username (str), assignments (list of dicts: assignment_id, course_id, title, description, due_date, max_points),
  submissions (dict keyed by assignment_id with submission status and data)                             |
| /submit-assignment/<int:assignment_id> | submit_assignment         | GET, POST   | submit_assignment.html  | username (str), assignment (dict: assignment_id, course_id, title, description, due_date, max_points),
  submission_status (str or None)                                                                         |
| /certificates                | certificates              | GET         | certificates.html       | username (str), certificates (list of dicts with certificate_id, course_id, issue_date, course_title)  |
| /profile                     | user_profile              | GET, POST   | profile.html            | username (str), email (str), fullname (str), update_status (str or None)                              |

Notes on POST behavior:
- /course/<course_id> POST: enroll user if not enrolled, record enrollment_date as current date, set progress 0, status "In Progress".
- /learn/<course_id> POST: form submits marking current lesson complete; updates progress; if progress 100%, generate certificate and update enrollment status to "Completed".
- /submit-assignment/<assignment_id> POST: saves submission text, records submit_date, sets submission status "Submitted".
- /profile POST: updates user's email and fullname.

---

## Section 2: HTML Template Specifications (For Frontend Developer)

### templates/dashboard.html
- Page Title: Learning Dashboard
- <title>: Learning Dashboard
- <h1 id="welcome-message">: "Welcome, {{ fullname }}"
- Element IDs:
  - dashboard-page (Div container)
  - welcome-message (H1)
  - enrolled-courses (Div) - iterates over enrolled_courses
  - browse-courses-button (Button) - navigates to course_catalog route
  - my-courses-button (Button) - navigates to my_courses route
- Context Variables:
  - username (str)
  - fullname (str)
  - enrolled_courses (list of dicts: course_id (int), title (str), progress (int))
- Navigation:
  - #browse-courses-button -> url_for('course_catalog')
  - #my-courses-button -> url_for('my_courses')

### templates/course_catalog.html
- Page Title: Available Courses
- <title>: Available Courses
- <h1>: "Available Courses"
- Element IDs:
  - catalog-page (Div container)
  - search-input (Input)
  - course-grid (Div) - iterates over courses
  - view-course-button-{{ course.course_id }} (Button)
  - back-to-dashboard (Button) - navigates to dashboard
- Context Variables:
  - username (str)
  - courses (list of dicts with course_id, title, description, category, level, duration, status)
- Navigation:
  - #view-course-button-{{ course.course_id }} -> url_for('course_details', course_id=course.course_id)
  - #back-to-dashboard -> url_for('dashboard')

### templates/course_details.html
- Page Title: Course Details
- <title>: Course Details
- <h1 id="course-title">: displays {{ course.title }}
- Element IDs:
  - course-details-page (Div container)
  - course-title (H1)
  - course-description (Div)
  - enroll-button (Button) - disabled and text "Already Enrolled" if enrolled==True
  - back-to-catalog (Button) - navigates to course_catalog
- Context Variables:
  - username (str)
  - course (dict with course attributes)
  - enrolled (bool)
  - enrollment_date (str or None)
- Navigation:
  - #enroll-button POSTs to /course/<course_id>
  - #back-to-catalog -> url_for('course_catalog')

### templates/my_courses.html
- Page Title: My Courses
- <title>: My Courses
- <h1>: "My Courses"
- Element IDs:
  - my-courses-page (Div container)
  - courses-list (Div) - iterates over enrolled_courses
  - continue-learning-button-{{ course.course_id }} (Button)
  - back-to-dashboard (Button) - navigates to dashboard
- Context Variables:
  - username (str)
  - enrolled_courses (list of dicts with course_id, title, progress)
- Navigation:
  - #continue-learning-button-{{ course.course_id }} -> url_for('course_learning', course_id=course.course_id)
  - #back-to-dashboard -> url_for('dashboard')

### templates/course_learning.html
- Page Title: Course Learning
- <title>: Course Learning
- <h1>: "Course Learning: {{ course.title }}"
- Element IDs:
  - learning-page (Div container)
  - lessons-list (Div) - list of lesson titles
  - lesson-content (Div) - current lesson content
  - mark-complete-button (Button) - disabled if cannot mark complete
  - back-to-my-courses (Button) - navigates to my_courses
- Context Variables:
  - username (str)
  - course (dict)
  - lessons (list of dicts: lesson_id, title, content)
  - current_lesson (dict: lesson_id, title, content)
  - completed_lessons (list of lesson_id)
  - progress (int)
  - can_mark_complete (bool)
- Navigation:
  - #mark-complete-button POSTs to /learn/<course_id>
  - #back-to-my-courses -> url_for('my_courses')

### templates/my_assignments.html
- Page Title: My Assignments
- <title>: My Assignments
- <h1>: "My Assignments"
- Element IDs:
  - assignments-page (Div container)
  - assignments-table (Table) - rows for each assignment
  - submit-assignment-button-{{ assignment.assignment_id }} (Button)
  - back-to-dashboard (Button) - navigates to dashboard
- Context Variables:
  - username (str)
  - assignments (list of dicts: assignment_id, course_id, title, description, due_date, max_points)
  - submissions (dict keyed by assignment_id with submission details)
- Navigation:
  - #submit-assignment-button-{{ assignment.assignment_id }} -> url_for('submit_assignment', assignment_id=assignment.assignment_id)
  - #back-to-dashboard -> url_for('dashboard')

### templates/submit_assignment.html
- Page Title: Submit Assignment
- <title>: Submit Assignment
- <h1>: "Submit Assignment"
- Element IDs:
  - submit-page (Div container)
  - assignment-info (Div) - shows assignment title & description
  - submission-text (Textarea)
  - submit-button (Button)
  - back-to-assignments (Button) - navigates to my_assignments
- Context Variables:
  - username (str)
  - assignment (dict with assignment details)
  - submission_status (str or None)
- Navigation:
  - #submit-button POSTs to /submit-assignment/<assignment_id>
  - #back-to-assignments -> url_for('my_assignments')

### templates/certificates.html
- Page Title: My Certificates
- <title>: My Certificates
- <h1>: "My Certificates"
- Element IDs:
  - certificates-page (Div container)
  - certificates-grid (Div) - iterates over certificates
  - back-to-dashboard (Button) - navigates to dashboard
- Context Variables:
  - username (str)
  - certificates (list of dicts: certificate_id, course_id, issue_date, course_title)
- Navigation:
  - #back-to-dashboard -> url_for('dashboard')

### templates/profile.html
- Page Title: My Profile
- <title>: My Profile
- <h1>: My Profile
- Element IDs:
  - profile-page (Div container)
  - profile-email (Input)
  - profile-fullname (Input)
  - update-profile-button (Button)
  - back-to-dashboard (Button)
- Context Variables:
  - username (str)
  - email (str)
  - fullname (str)
  - update_status (str or None)
- Navigation:
  - #update-profile-button POSTs to /profile
  - #back-to-dashboard -> url_for('dashboard')

---

## Section 3: Data File Schemas (For Backend Developer)

### data/users.txt
- Fields: username|email|fullname
  - username: unique user login identifier (str)
  - email: user email address (str)
  - fullname: full name of user (str)
- Example lines:
```
john|john@student.com|John Student
alice|alice@instructor.com|Alice Professor
jane|jane@student.com|Jane Learner
```

### data/courses.txt
- Fields: course_id|title|description|category|level|duration|status
  - course_id: unique numeric id (int)
  - title: course title (str)
  - description: course detailed description (str)
  - category: course category (str)
  - level: skill level (str, e.g. Beginner, Intermediate, Advanced)
  - duration: estimated time (str, e.g. "40 hours")
  - status: current course status (str, e.g. Active)
- Example lines:
```
1|Python Programming|Learn Python from scratch|Programming|Beginner|40 hours|Active
2|Web Development|Build modern websites|Web|Intermediate|60 hours|Active
3|Data Science|Introduction to data analysis|Data|Advanced|80 hours|Active
```

### data/enrollments.txt
- Fields: enrollment_id|username|course_id|enrollment_date|progress|status
  - enrollment_id: unique numeric id (int)
  - username: user login (str)
  - course_id: course id enrolled (int)
  - enrollment_date: date string YYYY-MM-DD (str)
  - progress: integer percent completed 0-100 (int)
  - status: enrollment status (str, e.g. In Progress, Completed)
- Example lines:
```
1|john|1|2024-11-01|75|In Progress
2|jane|1|2024-10-15|100|Completed
3|john|2|2024-11-10|25|In Progress
```

### data/assignments.txt
- Fields: assignment_id|course_id|title|description|due_date|max_points
  - assignment_id: unique numeric id for assignment (int)
  - course_id: associated course id (int)
  - title: assignment title (str)
  - description: details about assignment (str)
  - due_date: date string YYYY-MM-DD (str)
  - max_points: maximum points achievable (int)
- Example lines:
```
1|1|Python Basics Quiz|Complete the quiz on variables and data types|2024-12-01|100
2|1|Final Project|Build a calculator application|2024-12-15|200
```

### data/submissions.txt
- Fields: submission_id|assignment_id|username|submission_text|submit_date|grade|feedback
  - submission_id: unique numeric id (int)
  - assignment_id: assignment id submitted (int)
  - username: submitting user (str)
  - submission_text: text of submission (str)
  - submit_date: date string YYYY-MM-DD (str)
  - grade: numeric grade (int)
  - feedback: feedback comments (str)
- Example lines:
```
1|1|john|My answers are...|2024-11-25|85|Good work!
2|2|jane|Here is my project...|2024-11-20|95|Excellent!
```

### data/certificates.txt
- Fields: certificate_id|username|course_id|issue_date
  - certificate_id: unique numeric id (int)
  - username: user login (str)
  - course_id: completed course id (int)
  - issue_date: date string YYYY-MM-DD (str)
- Example lines:
```
1|jane|1|2024-11-22
```

---

End of Design Specification.
