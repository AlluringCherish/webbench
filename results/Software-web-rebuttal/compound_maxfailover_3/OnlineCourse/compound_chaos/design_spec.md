# OnlineCourse Application Design Specification

---

## Section 1: Flask Routes Specification (For Backend Developer)

| Route Path                           | Function Name           | HTTP Method | Template File           | Context Variables                                                                                                           |
|------------------------------------|-------------------------|-------------|-------------------------|----------------------------------------------------------------------------------------------------------------------------|
| /                                  | root                    | GET         | N/A                     | N/A (Redirects to /dashboard)                                                                                              |
| /dashboard                        | dashboard               | GET         | dashboard.html          | username (str), fullname (str), enrolled_courses (list of dict {course_id (str), title (str), progress (int)})              |
| /catalog                          | course_catalog          | GET         | catalog.html            | courses (list of dict {course_id (str), title (str), description (str), category (str), level (str), duration (str), status (str)}) |
| /catalog/search                  | course_catalog_search   | POST        | catalog.html            | courses (list of dict as above) - filtered by search query                                                                |
| /course/<course_id>               | course_details          | GET         | course_details.html     | course (dict {course_id (str), title (str), description (str), category (str), level (str), duration (str), status (str)}),
                                              already_enrolled (bool)                                                                                                   |
| /course/<course_id>/enroll       | enroll_course           | POST        | course_details.html     | course (dict as above), already_enrolled (bool), enrollment_success (bool)                                                |
| /my-courses                      | my_courses              | GET         | my_courses.html         | enrolled_courses (list of dict {course_id (str), title (str), progress (int)})                                            |
| /my-courses/learn/<course_id>    | course_learning         | GET         | course_learning.html    | course (dict {course_id (str), title (str)}), lessons (list of dict {lesson_id (str), title (str), content (str)}),
                                              current_lesson_id (str), progress (int)                                                                                     |
| /my-courses/learn/<course_id>/complete | mark_lesson_complete    | POST        | course_learning.html    | course (dict), lessons (list), current_lesson_id (str), progress (int), completion_certificate (dict or None)              |
| /assignments                    | my_assignments          | GET         | assignments.html        | assignments (list of dict {assignment_id (str), course_id (str), title (str), description (str), due_date (str), max_points (int), submission_status (str)}) |
| /assignments/submit/<assignment_id> | submit_assignment       | GET         | submit_assignment.html  | assignment (dict {assignment_id (str), title (str), description (str)})                                                    |
| /assignments/submit/<assignment_id> | submit_assignment_post  | POST        | submit_assignment.html  | assignment (dict), submission_success (bool), error_message (str or None)                                                 |
| /certificates                  | my_certificates         | GET         | certificates.html       | certificates (list of dict {certificate_id (str), course_id (str), title (str), issue_date (str)})                          |
| /profile                       | user_profile            | GET         | profile.html            | username (str), email (str), fullname (str)                                                                               |
| /profile/update                | update_profile          | POST        | profile.html            | username (str), email (str), fullname (str), update_success (bool)                                                        |


**Behavior and Logic Notes:**

- Root route `/` redirects to `/dashboard`.
- Enrollment (POST to `/course/<course_id>/enroll`) creates a new enrollment in `enrollments.txt` with progress=0 and status="In Progress".
- Enrollment date is recorded as current date in ISO format.
- Progress updates happen by marking lessons complete in sequence (POST to `/my-courses/learn/<course_id>/complete`). Progress is calculated as (completed lessons / total lessons) * 100.
- Upon 100% progress, status changes to "Completed" in enrollments.txt, and a certificate entry is added to certificates.txt with current date.
- Assignment submission POST to `/assignments/submit/<assignment_id>` adds or updates entry in submissions.txt with status "Submitted" and submit date, plus stores submission text.
- User profile updates POST to `/profile/update` update users.txt accordingly.

---

## Section 2: HTML Template Specifications (For Frontend Developer)

### templates/dashboard.html
- Page title: "Learning Dashboard"
- Container ID: dashboard-page
- H1 ID: welcome-message, text: "Welcome, {{ fullname }}!"
- Div ID: enrolled-courses, iterates over `enrolled_courses` context variable (list of dicts) displaying course title and progress as percentage
- Button ID: browse-courses-button, navigates via url_for('course_catalog')
- Button ID: my-courses-button, navigates via url_for('my_courses')
- Context variables:
  - username (str)
  - fullname (str)
  - enrolled_courses (list of dict {course_id (str), title (str), progress (int)})

### templates/catalog.html
- Page title: "Available Courses"
- Container ID: catalog-page
- Input ID: search-input
- Div ID: course-grid
- Repeated Button IDs pattern: view-course-button-{{ course.course_id }}
- Back Button ID: back-to-dashboard, navigates via url_for('dashboard')
- Context variables:
  - courses (list of dict with keys: course_id, title, description, category, level, duration, status)

### templates/course_details.html
- Page title: "Course Details"
- Container ID: course-details-page
- H1 ID: course-title displaying course.title
- Div ID: course-description displaying course.description
- Button ID: enroll-button
  - Disabled if already_enrolled is True
  - Text "Enroll" if not enrolled, "Already Enrolled" and disabled if enrolled
- Back Button ID: back-to-catalog, navigates via url_for('course_catalog')
- Context variables:
  - course (dict as above)
  - already_enrolled (bool)
  - enrollment_success (bool, optional, only on POST)

### templates/my_courses.html
- Page title: "My Courses"
- Container ID: my-courses-page
- Div ID: courses-list
- Repeated Button IDs pattern: continue-learning-button-{{ course.course_id }}
- Back Button ID: back-to-dashboard, navigates via url_for('dashboard')
- Context variables:
  - enrolled_courses (list of dict {course_id, title, progress})

### templates/course_learning.html
- Page title: "Course Learning"
- Container ID: learning-page
- Div ID: lessons-list
- Div ID: lesson-content
- Button ID: mark-complete-button
- Back Button ID: back-to-my-courses, navigates via url_for('my_courses')
- Context variables:
  - course (dict {course_id, title})
  - lessons (list of dict {lesson_id, title, content})
  - current_lesson_id (str)
  - progress (int)
  - completion_certificate (dict or None, includes certificate_id and issue_date if present)

### templates/assignments.html
- Page title: "My Assignments"
- Container ID: assignments-page
- Table ID: assignments-table
- Repeated Button IDs pattern: submit-assignment-button-{{ assignment.assignment_id }}
- Back Button ID: back-to-dashboard, navigates via url_for('dashboard')
- Context variables:
  - assignments (list of dict {assignment_id, course_id, title, description, due_date, max_points, submission_status})

### templates/submit_assignment.html
- Page title: "Submit Assignment"
- Container ID: submit-page
- Div ID: assignment-info
- Textarea ID: submission-text
- Button ID: submit-button
- Back Button ID: back-to-assignments, navigates via url_for('my_assignments')
- Context variables:
  - assignment (dict {assignment_id, title, description})
  - submission_success (bool, optional)
  - error_message (str or None, optional)
- Form POST target: url_for('submit_assignment_post', assignment_id=assignment.assignment_id)

### templates/certificates.html
- Page title: "My Certificates"
- Container ID: certificates-page
- Div ID: certificates-grid
- Back Button ID: back-to-dashboard, navigates via url_for('dashboard')
- Context variables:
  - certificates (list of dict {certificate_id, course_id, title, issue_date})

### templates/profile.html
- Page title: "My Profile"
- Container ID: profile-page
- Input ID: profile-email (type email)
- Input ID: profile-fullname (type text)
- Button ID: update-profile-button
- Back Button ID: back-to-dashboard, navigates via url_for('dashboard')
- Context variables:
  - username (str)
  - email (str)
  - fullname (str)
- Form POST target: url_for('update_profile')

---

## Section 3: Data File Schemas (For Backend Developer)

### data/users.txt
- Fields (pipe-delimited): username|email|fullname
- Description: Stores all registered users' basic information.
- Examples:
  john|john@student.com|John Student
  alice|alice@instructor.com|Alice Professor
  jane|jane@student.com|Jane Learner

### data/courses.txt
- Fields: course_id|title|description|category|level|duration|status
- Description: Stores details about courses offered.
- Examples:
  1|Python Programming|Learn Python from scratch|Programming|Beginner|40 hours|Active
  2|Web Development|Build modern websites|Web|Intermediate|60 hours|Active
  3|Data Science|Introduction to data analysis|Data|Advanced|80 hours|Active

### data/enrollments.txt
- Fields: enrollment_id|username|course_id|enrollment_date|progress|status
- Description: Tracks user enrollments, progress percentage, and status in courses.
- Examples:
  1|john|1|2024-11-01|75|In Progress
  2|jane|1|2024-10-15|100|Completed
  3|john|2|2024-11-10|25|In Progress

### data/assignments.txt
- Fields: assignment_id|course_id|title|description|due_date|max_points
- Description: Stores all assignments related to courses.
- Examples:
  1|1|Python Basics Quiz|Complete the quiz on variables and data types|2024-12-01|100
  2|1|Final Project|Build a calculator application|2024-12-15|200

### data/submissions.txt
- Fields: submission_id|assignment_id|username|submission_text|submit_date|grade|feedback
- Description: Stores assignment submissions with grades and feedback.
- Examples:
  1|1|john|My answers are...|2024-11-25|85|Good work!
  2|2|jane|Here is my project...|2024-11-20|95|Excellent!

### data/certificates.txt
- Fields: certificate_id|username|course_id|issue_date
- Description: Stores certificates issued to users for course completions.
- Examples:
  1|jane|1|2024-11-22

