# OnlineCourse Application Design Specifications

---

## Section 1: Flask Routes Specification (For Backend Developer)

| Route Path | Function Name | HTTP Method | Template File | Context Variables |
| --- | --- | --- | --- | --- |
| / | root_redirect | GET | None (redirect) | None |
| /dashboard | dashboard | GET | dashboard.html | username (str), fullname (str), enrolled_courses (List[Dict: course_id(str), title(str), progress(int)]) |
| /catalog | course_catalog | GET | course_catalog.html | username (str), courses (List[Dict: course_id(str), title(str), description(str), category(str), level(str), duration(str), status(str)]) |
| /catalog/<course_id> | course_details | GET | course_details.html | username (str), course (Dict: course_id(str), title(str), description(str)), enrolled (bool) |
| /catalog/<course_id>/enroll | enroll_course | POST | course_details.html | username (str), course (Dict), enrolled (bool), enroll_success (bool, optional), error_msg (str, optional) |
| /my-courses | my_courses | GET | my_courses.html | username (str), courses (List[Dict: course_id(str), title(str), progress(int)]) |
| /learning/<course_id> | course_learning | GET | course_learning.html | username (str), course (Dict: title(str)), lessons (List[Dict: lesson_id(str), title(str), content(str)]), current_lesson_id (str), completed_lessons (List[str]), progress (int) |
| /learning/<course_id>/mark-complete | mark_lesson_complete | POST | course_learning.html | username (str), course (Dict), lessons (List), current_lesson_id (str), completed_lessons (List[str]), progress (int), completion_certificate_generated (bool, optional) |
| /assignments | my_assignments | GET | my_assignments.html | username (str), assignments (List[Dict: assignment_id(str), title(str), description(str), due_date(str), max_points(int), status(str)]) |
| /assignments/<assignment_id>/submit | submit_assignment_page | GET | submit_assignment.html | username (str), assignment (Dict: assignment_id(str), title(str), description(str)) |
| /assignments/<assignment_id>/submit | submit_assignment | POST | submit_assignment.html | username (str), assignment (Dict), submission_success (bool), error_msg (str, optional) |
| /certificates | my_certificates | GET | certificates.html | username (str), certificates (List[Dict: course_id(str), title(str), issue_date(str)] ) |
| /profile | user_profile | GET | user_profile.html | username (str), email (str), fullname (str) |
| /profile/update | update_profile | POST | user_profile.html | username (str), email (str), fullname (str), update_success (bool), error_msg (str, optional) |

---

### Logic Notes:
- Enrollment adds entry to enrollments.txt with enrollment_date as current date and initial progress 0, status 'In Progress'. Duplicate enrollments are prevented.
- Progress updates in enrollments.txt when lessons are marked complete; progress = (completed lessons / total lessons) * 100.
- Upon 100% progress, a certificate record is generated in certificates.txt with issue_date as current date.
- Assignment submissions create entries in submissions.txt with status 'Submitted' and submit_date as current date.
- Profile updates modify users.txt.

---

## Section 2: HTML Template Specifications (For Frontend Developer)

### templates/dashboard.html
- Page Title: Learning Dashboard
- <title> and <h1> text: "Learning Dashboard"
- Elements:
  - Div id="dashboard-page"
  - H1 id="welcome-message" (displays user fullname with welcome message)
  - Div id="enrolled-courses" (lists enrolled courses, each with title and progress)
  - Button id="browse-courses-button" (navigates to course_catalog)
  - Button id="my-courses-button" (navigates to my_courses)
- Context Variables:
  - username (str)
  - fullname (str)
  - enrolled_courses (List of Dicts with keys: course_id(str), title(str), progress(int))
- Navigation:
  - browse-courses-button: url_for('course_catalog')
  - my-courses-button: url_for('my_courses')

---

### templates/course_catalog.html
- Page Title: Available Courses
- <title> and <h1> text: "Available Courses"
- Elements:
  - Div id="catalog-page"
  - Input id="search-input" (for course search)
  - Div id="course-grid"
  - Button id pattern: "view-course-button-{{ course.course_id }}" in a loop over courses
  - Button id="back-to-dashboard" (navigates to dashboard)
- Context Variables:
  - username (str)
  - courses (List of Dicts: course_id(str), title(str), description(str), category(str), level(str), duration(str), status(str))
- Navigation:
  - view-course-button-{{ course.course_id }}: url_for('course_details', course_id=course.course_id)
  - back-to-dashboard: url_for('dashboard')

---

### templates/course_details.html
- Page Title: Course Details
- <title> and <h1> text: "Course Details"
- Elements:
  - Div id="course-details-page"
  - H1 id="course-title" (displays course title)
  - Div id="course-description" (displays course description)
  - Button id="enroll-button"
  - Button id="back-to-catalog" (navigates to course_catalog)
- Context Variables:
  - username (str)
  - course (Dict: course_id(str), title(str), description(str))
  - enrolled (bool)
- Functionality Notes:
  - If enrolled, enroll-button shows "Already Enrolled" and is disabled.
  - POST form submission for enrollment points to '/catalog/<course_id>/enroll'
- Navigation:
  - back-to-catalog: url_for('course_catalog')

---

### templates/my_courses.html
- Page Title: My Courses
- <title> and <h1> text: "My Courses"
- Elements:
  - Div id="my-courses-page"
  - Div id="courses-list"
  - Button id pattern: "continue-learning-button-{{ course.course_id }}" in loop
  - Button id="back-to-dashboard" (navigates to dashboard)
- Context Variables:
  - username (str)
  - courses (List of Dicts: course_id(str), title(str), progress(int))
- Navigation:
  - continue-learning-button-{{ course.course_id }}: url_for('course_learning', course_id=course.course_id)
  - back-to-dashboard: url_for('dashboard')

---

### templates/course_learning.html
- Page Title: Course Learning
- <title> and <h1> text: "Course Learning"
- Elements:
  - Div id="learning-page"
  - Div id="lessons-list" (lists all lessons with clickable titles to view content)
  - Div id="lesson-content" (displays current lesson materials)
  - Button id="mark-complete-button"
  - Button id="back-to-my-courses" (navigates to my_courses)
- Context Variables:
  - username (str)
  - course (Dict with title(str))
  - lessons (List of Dicts: lesson_id(str), title(str), content(str))
  - current_lesson_id (str)
  - completed_lessons (List[str])
  - progress (int)
- Navigation:
  - back-to-my-courses: url_for('my_courses')
- Functionality Notes:
  - Mark-complete-button triggers POST to '/learning/<course_id>/mark-complete'
  - Lessons completed sequentially; button disabled if current lesson is not the next in order

---

### templates/my_assignments.html
- Page Title: My Assignments
- <title> and <h1> text: "My Assignments"
- Elements:
  - Div id="assignments-page"
  - Table id="assignments-table"
  - Button id pattern: "submit-assignment-button-{{ assignment.assignment_id }}" in loop
  - Button id="back-to-dashboard" (navigates to dashboard)
- Context Variables:
  - username (str)
  - assignments (List of Dicts: assignment_id(str), title(str), description(str), due_date(str), max_points(int), status(str))
- Navigation:
  - submit-assignment-button-{{ assignment.assignment_id }}: url_for('submit_assignment_page', assignment_id=assignment.assignment_id)
  - back-to-dashboard: url_for('dashboard')

---

### templates/submit_assignment.html
- Page Title: Submit Assignment
- <title> and <h1> text: "Submit Assignment"
- Elements:
  - Div id="submit-page"
  - Div id="assignment-info" (displays assignment title and description)
  - Textarea id="submission-text"
  - Button id="submit-button"
  - Button id="back-to-assignments" (navigates to my_assignments)
- Context Variables:
  - username (str)
  - assignment (Dict: assignment_id(str), title(str), description(str))
- Navigation:
  - back-to-assignments: url_for('my_assignments')
- Forms:
  - Submission POST form targets '/assignments/<assignment_id>/submit'

---

### templates/certificates.html
- Page Title: My Certificates
- <title> and <h1> text: "My Certificates"
- Elements:
  - Div id="certificates-page"
  - Div id="certificates-grid"
  - Button id="back-to-dashboard" (navigates to dashboard)
- Context Variables:
  - username (str)
  - certificates (List of Dicts: course_id(str), title(str), issue_date(str))
- Navigation:
  - back-to-dashboard: url_for('dashboard')

---

### templates/user_profile.html
- Page Title: My Profile
- <title> and <h1> text: "My Profile"
- Elements:
  - Div id="profile-page"
  - Input id="profile-email" (value=email)
  - Input id="profile-fullname" (value=fullname)
  - Button id="update-profile-button"
  - Button id="back-to-dashboard" (navigates to dashboard)
- Context Variables:
  - username (str)
  - email (str)
  - fullname (str)
- Navigation:
  - back-to-dashboard: url_for('dashboard')
- Forms:
  - Update form POST to '/profile/update'

---

## Section 3: Data File Schemas (For Backend Developer)

---

### data/users.txt
- Fields: username|email|fullname
- Description: Stores user login name, email address, and full name.
- Examples:
  john|john@student.com|John Student
  alice|alice@instructor.com|Alice Professor
  jane|jane@student.com|Jane Learner

---

### data/courses.txt
- Fields: course_id|title|description|category|level|duration|status
- Description: Course metadata including unique ID, title, detailed description, category, experience level, expected duration, and status.
- Examples:
  1|Python Programming|Learn Python from scratch|Programming|Beginner|40 hours|Active
  2|Web Development|Build modern websites|Web|Intermediate|60 hours|Active
  3|Data Science|Introduction to data analysis|Data|Advanced|80 hours|Active

---

### data/enrollments.txt
- Fields: enrollment_id|username|course_id|enrollment_date|progress|status
- Description: Enrollment records linking users to courses with enrollment date, progress percentage, and current status.
- Date format: YYYY-MM-DD
- status values: In Progress, Completed
- Examples:
  1|john|1|2024-11-01|75|In Progress
  2|jane|1|2024-10-15|100|Completed
  3|john|2|2024-11-10|25|In Progress

---

### data/assignments.txt
- Fields: assignment_id|course_id|title|description|due_date|max_points
- Description: Assignment metadata connected to courses with due dates and point max.
- Date format: YYYY-MM-DD
- Examples:
  1|1|Python Basics Quiz|Complete the quiz on variables and data types|2024-12-01|100
  2|1|Final Project|Build a calculator application|2024-12-15|200

---

### data/submissions.txt
- Fields: submission_id|assignment_id|username|submission_text|submit_date|grade|feedback
- Description: User submissions for assignments including grading data and teacher feedback.
- Date format: YYYY-MM-DD
- Examples:
  1|1|john|My answers are...|2024-11-25|85|Good work!
  2|2|jane|Here is my project...|2024-11-20|95|Excellent!

---

### data/certificates.txt
- Fields: certificate_id|username|course_id|issue_date
- Description: Records of certificates issued upon course completion.
- Date format: YYYY-MM-DD
- Examples:
  1|jane|1|2024-11-22
