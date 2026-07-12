# OnlineCourse Web Application Design Specification

---

## Section 1: Flask Routes Specification (For Backend Developer)

| Route Path                              | Function Name             | HTTP Method | Template File             | Context Variables                                                                                                                      |
|----------------------------------------|---------------------------|-------------|---------------------------|----------------------------------------------------------------------------------------------------------------------------------------|
| /                                      | root_redirect              | GET         | N/A                       | N/A (Redirects to /dashboard)                                                                                                          |
| /dashboard                            | dashboard_page             | GET         | dashboard.html            | user_name: str, enrolled_courses: List[Dict]{course_id:str, title:str, progress:int}                                                   |
| /catalog                             | course_catalog             | GET         | course_catalog.html       | courses: List[Dict]{course_id:str, title:str, description:str, category:str, level:str, duration:str, status:str}                      |
| /course/<int:course_id>              | course_details             | GET         | course_details.html       | course: Dict{course_id:str, title:str, description:str}, is_enrolled: bool                                                             |
| /course/<int:course_id>/enroll       | enroll_course              | POST        | course_details.html       | course: Dict{course_id:str, title:str, description:str}, is_enrolled: bool, enroll_success: bool                                       |
| /mycourses                          | my_courses                 | GET         | my_courses.html           | enrolled_courses: List[Dict]{course_id:str, title:str, progress:int}                                                                    |
| /course/<int:course_id>/learn        | course_learning            | GET         | course_learning.html      | course: Dict{course_id:str, title:str}, lessons: List[Dict]{lesson_id:str, title:str, content:str}, current_lesson: Dict, progress:int  |
| /course/<int:course_id>/learn/mark_complete | mark_lesson_complete      | POST        | course_learning.html      | course: Dict, lessons: List[Dict], current_lesson: Dict, progress:int, completion_status: bool                                          |
| /assignments                       | my_assignments             | GET         | assignments.html          | assignments: List[Dict]{assignment_id:str, title:str, description:str, due_date:str, max_points:int}, submissions: Dict[assignment_id:str]|
| /assignment/<int:assignment_id>/submit | submit_assignment          | GET         | submit_assignment.html    | assignment: Dict{assignment_id:str, title:str, description:str}, submission_status: bool                                                |
| /assignment/<int:assignment_id>/submit | submit_assignment_post     | POST        | submit_assignment.html    | assignment: Dict, submission_status: bool, submission_success: bool                                                                    |
| /certificates                     | certificates_page          | GET         | certificates.html         | certificates: List[Dict]{certificate_id:str, course_title:str, issue_date:str}                                                         |
| /profile                         | user_profile               | GET         | profile.html              | user_profile: Dict{username:str, email:str, fullname:str}                                                                              |
| /profile/update                  | update_profile             | POST        | profile.html              | user_profile: Dict, update_success: bool                                                                                              |

**Notes:**
- The root route '/' immediately redirects to the Dashboard page '/dashboard'.
- Enrollment POST adds a record in enrollments.txt with 0% progress and current date as enrollment_date.
- Progress updates on marking lesson complete write back to enrollments.txt.
- Course completion (progress 100%) triggers certificate generation and record addition in certificates.txt.
- Assignment submission POST appends a record in submissions.txt with status 'Submitted' and current date.
- Profile update POST modifies users.txt user record.

---

## Section 2: HTML Template Specifications (For Frontend Developer)

### Template: templates/dashboard.html
- Page Title: Learning Dashboard
- <title> and <h1> text: "Learning Dashboard"
- Element IDs:
  - dashboard-page (div container)
  - welcome-message (h1) displays "Welcome, {{ user_name }}"
  - enrolled-courses (div) to list enrolled courses dynamically
  - browse-courses-button (button) navigates to url_for('course_catalog')
  - my-courses-button (button) navigates to url_for('my_courses')
- Context Variables:
  - user_name: string
  - enrolled_courses: list of dicts {course_id, title, progress}

### Template: templates/course_catalog.html
- Page Title: Available Courses
- <title> and <h1> text: "Available Courses"
- Element IDs:
  - catalog-page (div container)
  - search-input (input text box for search)
  - course-grid (div container for course cards)
  - view-course-button-{{ course.course_id }} (button) per course for details navigation
  - back-to-dashboard (button) navigation to url_for('dashboard_page')
- Context Variables:
  - courses: list of dicts {course_id, title, description, category, level, duration, status}

### Template: templates/course_details.html
- Page Title: Course Details
- <title> and <h1> text: "Course Details"
- Element IDs:
  - course-details-page (div container)
  - course-title (h1) displays course.title
  - course-description (div) displays course.description
  - enroll-button (button)
    - If user is enrolled, button text is "Already Enrolled" and disabled
    - Otherwise, text is "Enroll" and clickable posts to /course/<course_id>/enroll
  - back-to-catalog (button) navigation to url_for('course_catalog')
- Context Variables:
  - course: dict {course_id, title, description}
  - is_enrolled: bool
  - enroll_success: bool (only after POST)

### Template: templates/my_courses.html
- Page Title: My Courses
- <title> and <h1> text: "My Courses"
- Element IDs:
  - my-courses-page (div container)
  - courses-list (div container) listing courses
  - continue-learning-button-{{ course.course_id }} (button) per course to navigate to /course/<course_id>/learn
  - back-to-dashboard (button) navigation to url_for('dashboard_page')
- Context Variables:
  - enrolled_courses: list of dicts {course_id, title, progress}

### Template: templates/course_learning.html
- Page Title: Course Learning
- <title> and <h1> text: "Course Learning"
- Element IDs:
  - learning-page (div container)
  - lessons-list (div container) list all lessons with indication of current
  - lesson-content (div) show current lesson content
  - mark-complete-button (button) to post marking lesson complete
  - back-to-my-courses (button) navigation to url_for('my_courses')
- Context Variables:
  - course: dict {course_id, title}
  - lessons: list of dicts {lesson_id, title, content}
  - current_lesson: dict {lesson_id, title, content}
  - progress: int (0-100 percent)
  - completion_status: bool (True if completed)

### Template: templates/assignments.html
- Page Title: My Assignments
- <title> and <h1> text: "My Assignments"
- Element IDs:
  - assignments-page (div container)
  - assignments-table (table) with assignment rows
  - submit-assignment-button-{{ assignment.assignment_id }} (button) when assignment is pending submission
  - back-to-dashboard (button) navigation to url_for('dashboard_page')
- Context Variables:
  - assignments: list of dicts {assignment_id, title, description, due_date, max_points}
  - submissions: dict keyed by assignment_id with submission info

### Template: templates/submit_assignment.html
- Page Title: Submit Assignment
- <title> and <h1> text: "Submit Assignment"
- Element IDs:
  - submit-page (div container)
  - assignment-info (div) displaying assignment.title and assignment.description
  - submission-text (textarea) for user input
  - submit-button (button) posts to /assignment/<assignment_id>/submit
  - back-to-assignments (button) navigation to url_for('my_assignments')
- Context Variables:
  - assignment: dict {assignment_id, title, description}
  - submission_status: bool (indicates if already submitted)
  - submission_success: bool (true after successful post)

### Template: templates/certificates.html
- Page Title: My Certificates
- <title> and <h1> text: "My Certificates"
- Element IDs:
  - certificates-page (div container)
  - certificates-grid (div container) listing certificate cards
  - back-to-dashboard (button) navigation to url_for('dashboard_page')
- Context Variables:
  - certificates: list of dicts {certificate_id, course_title, issue_date}

### Template: templates/profile.html
- Page Title: My Profile
- <title> and <h1> text: "My Profile"
- Element IDs:
  - profile-page (div container)
  - profile-email (input email field)
  - profile-fullname (input text field)
  - update-profile-button (button) posts to /profile/update
  - back-to-dashboard (button) navigation to url_for('dashboard_page')
- Context Variables:
  - user_profile: dict {username, email, fullname}
  - update_success: bool (true after profile update post)

---

## Section 3: Data File Schemas (For Backend Developer)

### 1. users.txt
- File Path: data/users.txt
- Fields order: username | email | fullname
- Field descriptions:
  - username: unique user id string
  - email: user email address
  - fullname: full name of user
- Example lines:
  john|john@student.com|John Student
  alice|alice@instructor.com|Alice Professor
  jane|jane@student.com|Jane Learner

### 2. courses.txt
- File Path: data/courses.txt
- Fields order: course_id | title | description | category | level | duration | status
- Field descriptions:
  - course_id: numeric string unique course identifier
  - title: course title
  - description: detailed course description
  - category: course category string
  - level: course difficulty level string
  - duration: expected course length string
  - status: current status (e.g. Active)
- Example lines:
  1|Python Programming|Learn Python from scratch|Programming|Beginner|40 hours|Active
  2|Web Development|Build modern websites|Web|Intermediate|60 hours|Active
  3|Data Science|Introduction to data analysis|Data|Advanced|80 hours|Active

### 3. enrollments.txt
- File Path: data/enrollments.txt
- Fields order: enrollment_id | username | course_id | enrollment_date | progress | status
- Field descriptions:
  - enrollment_id: unique numeric string
  - username: user id string
  - course_id: course numeric string
  - enrollment_date: date string in YYYY-MM-DD
  - progress: integer percent (0-100)
  - status: progress status string (e.g. In Progress, Completed)
- Example lines:
  1|john|1|2024-11-01|75|In Progress
  2|jane|1|2024-10-15|100|Completed
  3|john|2|2024-11-10|25|In Progress

### 4. assignments.txt
- File Path: data/assignments.txt
- Fields order: assignment_id | course_id | title | description | due_date | max_points
- Field descriptions:
  - assignment_id: unique numeric string
  - course_id: numeric string
  - title: assignment title
  - description: assignment detailed description
  - due_date: due date string in YYYY-MM-DD
  - max_points: numeric max score
- Example lines:
  1|1|Python Basics Quiz|Complete the quiz on variables and data types|2024-12-01|100
  2|1|Final Project|Build a calculator application|2024-12-15|200

### 5. submissions.txt
- File Path: data/submissions.txt
- Fields order: submission_id | assignment_id | username | submission_text | submit_date | grade | feedback
- Field descriptions:
  - submission_id: unique numeric string
  - assignment_id: numeric string
  - username: user id string
  - submission_text: text response from user
  - submit_date: submission date string YYYY-MM-DD
  - grade: numeric score
  - feedback: instructor comments
- Example lines:
  1|1|john|My answers are...|2024-11-25|85|Good work!
  2|2|jane|Here is my project...|2024-11-20|95|Excellent!

### 6. certificates.txt
- File Path: data/certificates.txt
- Fields order: certificate_id | username | course_id | issue_date
- Field descriptions:
  - certificate_id: unique numeric string
  - username: user id string
  - course_id: numeric string
  - issue_date: date string YYYY-MM-DD
- Example lines:
  1|jane|1|2024-11-22

---

**End of Design Specification**
