# OnlineCourse Web Application Design Specification

---

## Section 1: Flask Routes Specification (For Backend Developer)

| Route Path | Function Name | HTTP Method | Template File | Context Variables |
|------------|---------------|-------------|---------------|-------------------|
| / | root_redirect | GET | None (redirect) | None |
| /dashboard | dashboard | GET | dashboard.html | username: str, fullname: str, enrolled_courses: list of dict {course_id:int, title:str, progress:int} |
| /catalog | course_catalog | GET | catalog.html | courses: list of dict {course_id:int, title:str, category:str, level:str, duration:str, status:str} |
| /course/<int:course_id> | course_details | GET, POST | course_details.html | course: dict {course_id:int, title:str, description:str, category:str, level:str, duration:str, status:str}, is_enrolled: bool |
| /my-courses | my_courses | GET | my_courses.html | enrolled_courses: list of dict {course_id:int, title:str, progress:int} |
| /learn/<int:course_id> | course_learning | GET, POST | course_learning.html | course: dict {course_id:int, title:str, lessons: list of dict {lesson_number:int, lesson_title:str, lesson_content:str}}, current_lesson_number: int, completed_lessons: set of ints, progress: int, can_mark_complete: bool |
| /assignments | my_assignments | GET | assignments.html | assignments: list of dict {assignment_id:int, title:str, due_date:str, status:str} |  
| /submit-assignment/<int:assignment_id> | submit_assignment | GET, POST | submit_assignment.html | assignment: dict {assignment_id:int, title:str, description:str}, confirmation_message: str or None |
| /certificates | certificates | GET | certificates.html | certificates: list of dict {certificate_id:int, course_title:str, issue_date:str} |
| /profile | profile | GET, POST | profile.html | username: str, email: str, fullname: str |

### Notes on routes:
- **/** redirects to /dashboard.
- Enrollment (POST on /course/<course_id>) adds enrollment with 0% progress and current date if user not already enrolled.
- Progress updates and lesson completion (POST on /learn/<course_id>) update enrollments.txt progress.
- Course completion (progress==100) triggers automatic certificate generation.
- Assignment submission (POST on /submit-assignment/<assignment_id>) creates entry in submissions.txt.
- Profile update (POST on /profile) updates user email/fullname in users.txt.


---

## Section 2: HTML Template Specifications (For Frontend Developer)

### templates/dashboard.html
- Page Title: Learning Dashboard
- <title> and <h1 id="welcome-message"> both display: "Welcome, {{ fullname }}"
- Container div ID: dashboard-page
- Enrolled courses div ID: enrolled-courses
- Buttons with IDs:
  - browse-courses-button (navigates to 'course_catalog')
  - my-courses-button (navigates to 'my_courses')
- Context variables:
  - username: str
  - fullname: str
  - enrolled_courses: list of dict {course_id:int, title:str, progress:int}

---

### templates/catalog.html
- Page Title: Available Courses
- <title> and <h1> "Available Courses"
- Container div ID: catalog-page
- Search input field ID: search-input
- Course grid div ID: course-grid
- For each course in courses:
  - Button ID pattern: "view-course-button-{{ course.course_id }}" - navigates to 'course_details' with course_id
- Button ID: back-to-dashboard (navigates to 'dashboard')
- Context variables:
  - courses: list of dict {course_id:int, title:str, category:str, level:str, duration:str, status:str}

---

### templates/course_details.html
- Page Title: Course Details
- <title> and <h1 id="course-title"> display course title
- Container div ID: course-details-page
- Div with ID: course-description for course full description
- Button ID: enroll-button
  - Disabled and label as "Already Enrolled" if is_enrolled==True
  - Enabled with label "Enroll" if not enrolled
- Button ID: back-to-catalog (navigates to 'course_catalog')
- Context variables:
  - course: dict {course_id:int, title:str, description:str, category:str, level:str, duration:str, status:str}
  - is_enrolled: bool
- Form submission (POST) target: enroll in course

---

### templates/my_courses.html
- Page Title: My Courses
- <title> and <h1> "My Courses"
- Container div ID: my-courses-page
- Div with ID: courses-list
- For each enrolled course:
  - Button ID pattern: "continue-learning-button-{{ course.course_id }}" navigates to 'course_learning' with course_id
- Button ID: back-to-dashboard (navigates to 'dashboard')
- Context variables:
  - enrolled_courses: list of dict {course_id:int, title:str, progress:int}

---

### templates/course_learning.html
- Page Title: Course Learning
- <title> and <h1> "Course Learning"
- Container div ID: learning-page
- Div ID: lessons-list
- Div ID: lesson-content
- Button ID: mark-complete-button
  - Disabled unless can_mark_complete==True
- Button ID: back-to-my-courses (navigates to 'my_courses')
- Context variables:
  - course: dict {course_id:int, title:str, lessons: list of dict {lesson_number:int, lesson_title:str, lesson_content:str}}
  - current_lesson_number: int
  - completed_lessons: set of ints
  - progress: int
  - can_mark_complete: bool

---

### templates/assignments.html
- Page Title: My Assignments
- <title> and <h1> "My Assignments"
- Container div ID: assignments-page
- Table ID: assignments-table
- For each assignment in assignments:
  - Button ID pattern: "submit-assignment-button-{{ assignment.assignment_id }}" (only for pending assignments)
- Button ID: back-to-dashboard (navigates to 'dashboard')
- Context variables:
  - assignments: list of dict {assignment_id:int, title:str, due_date:str, status:str}

---

### templates/submit_assignment.html
- Page Title: Submit Assignment
- <title> and <h1> "Submit Assignment"
- Container div ID: submit-page
- Div ID: assignment-info (shows assignment title and description)
- Textarea ID: submission-text
- Button ID: submit-button
- Button ID: back-to-assignments (navigates to 'my_assignments')
- Context variables:
  - assignment: dict {assignment_id:int, title:str, description:str}
  - confirmation_message: str or None
- Form submits to POST on current route

---

### templates/certificates.html
- Page Title: My Certificates
- <title> and <h1> "My Certificates"
- Container div ID: certificates-page
- Div ID: certificates-grid
- For each certificate:
  - Display certificate details (no dynamic button IDs required)
- Button ID: back-to-dashboard (navigates to 'dashboard')
- Context variables:
  - certificates: list of dict {certificate_id:int, course_title:str, issue_date:str}

---

### templates/profile.html
- Page Title: My Profile
- <title> and <h1> "My Profile"
- Container div ID: profile-page
- Input IDs: profile-email, profile-fullname
- Button ID: update-profile-button
- Button ID: back-to-dashboard (navigates to 'dashboard')
- Context variables:
  - username: str
  - email: str
  - fullname: str
- Form submits POST to /profile

---

## Section 3: Data File Schemas (For Backend Developer)

### data/users.txt
- Fields: username|email|fullname
- username: unique user ID (str)
- email: user's email address (str)
- fullname: user's full name (str)
- Examples:
  john|john@student.com|John Student
  alice|alice@instructor.com|Alice Professor
  jane|jane@student.com|Jane Learner

---

### data/courses.txt
- Fields: course_id|title|description|category|level|duration|status
- course_id: integer course identifier
- title: course name
- description: full text
- category: category of course
- level: Beginner/Intermediate/Advanced
- duration: e.g., '40 hours'
- status: Active or Inactive
- Examples:
  1|Python Programming|Learn Python from scratch|Programming|Beginner|40 hours|Active
  2|Web Development|Build modern websites|Web|Intermediate|60 hours|Active
  3|Data Science|Introduction to data analysis|Data|Advanced|80 hours|Active

---

### data/enrollments.txt
- Fields: enrollment_id|username|course_id|enrollment_date|progress|status
- enrollment_id: integer
- username: user ID
- course_id: integer
- enrollment_date: YYYY-MM-DD
- progress: integer percentage 0-100
- status: In Progress, Completed
- Examples:
  1|john|1|2024-11-01|75|In Progress
  2|jane|1|2024-10-15|100|Completed
  3|john|2|2024-11-10|25|In Progress

---

### data/assignments.txt
- Fields: assignment_id|course_id|title|description|due_date|max_points
- assignment_id: integer
- course_id: integer
- title: assignment name
- description: text
- due_date: YYYY-MM-DD
- max_points: integer
- Examples:
  1|1|Python Basics Quiz|Complete the quiz on variables and data types|2024-12-01|100
  2|1|Final Project|Build a calculator application|2024-12-15|200

---

### data/submissions.txt
- Fields: submission_id|assignment_id|username|submission_text|submit_date|grade|feedback
- submission_id: integer
- assignment_id: integer
- username: user ID
- submission_text: text
- submit_date: YYYY-MM-DD
- grade: integer score
- feedback: text
- Examples:
  1|1|john|My answers are...|2024-11-25|85|Good work!
  2|2|jane|Here is my project...|2024-11-20|95|Excellent!

---

### data/certificates.txt
- Fields: certificate_id|username|course_id|issue_date
- certificate_id: integer
- username: user ID
- course_id: integer
- issue_date: YYYY-MM-DD
- Examples:
  1|jane|1|2024-11-22

