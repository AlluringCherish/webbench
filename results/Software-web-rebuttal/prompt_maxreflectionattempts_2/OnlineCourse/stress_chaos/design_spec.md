# OnlineCourse Application Design Specification

---

## Section 1: Flask Routes Specification (For Backend Developer)

| Route Path                           | Function Name           | HTTP Method | Template File           | Context Variables                                                                                                           |
|------------------------------------|-------------------------|-------------|-------------------------|----------------------------------------------------------------------------------------------------------------------------|
| /                                  | root                    | GET         | N/A                     | N/A (Redirects to /dashboard)                                                                                              |
| /dashboard                        | dashboard               | GET         | dashboard.html          | username (str), fullname (str), enrolled_courses (list of dict {course_id (str), title (str), progress (int)} )             |
| /catalog                          | course_catalog          | GET         | catalog.html            | courses (list of dict {course_id (str), title (str), description (str), category (str), level (str), duration (str), status (str)}) |
| /catalog/search                  | course_catalog_search   | POST        | catalog.html            | courses (list of dict as above) - filtered by search query                                                                |
| /course/<course_id>               | course_details          | GET         | course_details.html     | course (dict {course_id (str), title (str), description (str), category (str), level (str), duration (str), status (str)}),
                                              already_enrolled (bool)                                                                                                   |
| /course/<course_id>/enroll       | enroll_course           | POST        | course_details.html     | course (dict as above), already_enrolled (bool), enrollment_success (bool)                                                |
| /my-courses                      | my_courses              | GET         | my_courses.html         | enrolled_courses (list of dict {course_id (str), title (str), progress (int)})                                            |
| /course/<course_id>/learn        | course_learning         | GET         | course_learning.html    | course (dict as above), lessons (list of dict {lesson_id (str), title (str), content (str)}),
                                              current_lesson_index (int), completed_lessons (list of int)                                                          |
| /course/<course_id>/learn/complete | mark_lesson_complete    | POST        | course_learning.html    | course (dict as above), lessons (list as above), current_lesson_index (int), progress (int), certificate_generated (bool)   |
| /assignments                    | my_assignments          | GET         | assignments.html        | assignments (list of dict {assignment_id (str), course_id (str), title (str), description (str), due_date (str), max_points (int)}), submissions (list of dict {submission_id (str), assignment_id (str), username (str), submission_text (str), submit_date (str), grade (int or None), feedback (str or None)}) |
| /assignments/<assignment_id>/submit | submit_assignment       | GET         | submit_assignment.html  | assignment (dict {assignment_id (str), course_id (str), title (str), description (str), due_date (str), max_points (int)})    |
| /assignments/<assignment_id>/submit | post_assignment        | POST        | submit_assignment.html  | assignment (dict as above), submission_success (bool)                                                                       |
| /certificates                   | certificates            | GET         | certificates.html       | certificates (list of dict {certificate_id (str), username (str), course_id (str), issue_date (str)}), courses (dict mapping course_id to title) |
| /profile                       | user_profile            | GET         | profile.html            | user (dict {username (str), email (str), fullname (str)})                                                                   |
| /profile/update                | update_profile          | POST        | profile.html            | user (dict as above), update_success (bool)                                                                                |


---

## Section 2: HTML Template Specifications (For Frontend Developer)

### templates/dashboard.html
- Page Title: Learning Dashboard
- &lt;title&gt; and &lt;h1&gt;: "Learning Dashboard"
- Element IDs:
  - dashboard-page: Div container for the dashboard
  - welcome-message: H1 displaying "Welcome, {{ fullname }}"
  - enrolled-courses: Div listing enrolled courses with each showing title and progress
  - browse-courses-button: Button to navigate to course_catalog (url_for('course_catalog'))
  - my-courses-button: Button to navigate to my_courses (url_for('my_courses'))
- Context variables:
  - username (str)
  - fullname (str)
  - enrolled_courses (list of dict {course_id (str), title (str), progress (int)})
- Notes:
  - Display message "Welcome, {{ fullname }}" in welcome-message
  - Each enrolled course can be listed with title and progress percentage

### templates/catalog.html
- Page Title: Available Courses
- &lt;title&gt; and &lt;h1&gt;: "Available Courses"
- Element IDs:
  - catalog-page: Div container
  - search-input: Input field for search query
  - course-grid: Div containing all course cards
  - view-course-button-{{ course.course_id }}: Button for each course to view details
  - back-to-dashboard: Button linking back to dashboard
- Context variables:
  - courses (list of dict)
- Navigation mappings:
  - view-course-button: url_for('course_details', course_id=course.course_id)
  - back-to-dashboard: url_for('dashboard')
- Notes:
  - Search form submits to /catalog/search via POST

### templates/course_details.html
- Page Title: Course Details
- &lt;title&gt; and &lt;h1&gt;: "Course Details"
- Element IDs:
  - course-details-page: Div container
  - course-title: H1 showing course.title
  - course-description: Div showing course.description
  - enroll-button: Button to POST to /course/&lt;course_id&gt;/enroll
    - Disabled and text "Already Enrolled" if already_enrolled is True
  - back-to-catalog: Button linking back to course_catalog
- Context variables:
  - course (dict)
  - already_enrolled (bool)
  - enrollment_success (bool, optional) - to show confirmation
- Navigation mappings:
  - back-to-catalog: url_for('course_catalog')
- Notes:
  - The enroll-button is a POST form submission to enroll_course route

### templates/my_courses.html
- Page Title: My Courses
- &lt;title&gt; and &lt;h1&gt;: "My Courses"
- Element IDs:
  - my-courses-page: Div container
  - courses-list: Div listing enrolled courses with progress
  - continue-learning-button-{{ course.course_id }}: Button for each course to continue learning
  - back-to-dashboard: Button linking to dashboard
- Context variables:
  - enrolled_courses (list of dict)
- Navigation mappings:
  - continue-learning-button: url_for('course_learning', course_id=course.course_id)
  - back-to-dashboard: url_for('dashboard')

### templates/course_learning.html
- Page Title: Course Learning
- &lt;title&gt; and &lt;h1&gt;: "Course Learning"
- Element IDs:
  - learning-page: Div container
  - lessons-list: Div with list of lessons
  - lesson-content: Div with current lesson content
  - mark-complete-button: Button to POST to mark lesson complete
  - back-to-my-courses: Button linking back to my_courses
- Context variables:
  - course (dict)
  - lessons (list of dict {lesson_id (str), title (str), content (str)})
  - current_lesson_index (int)
  - completed_lessons (list of int)
- Navigation mappings:
  - back-to-my-courses: url_for('my_courses')
- Notes:
  - mark-complete-button submits POST to route mark_lesson_complete for current lesson
  - Lessons must be completed in sequence

### templates/assignments.html
- Page Title: My Assignments
- &lt;title&gt; and &lt;h1&gt;: "My Assignments"
- Element IDs:
  - assignments-page: Div container
  - assignments-table: Table listing all assignments
  - submit-assignment-button-{{ assignment.assignment_id }}: Button for each assignment to submit
  - back-to-dashboard: Button linking back to dashboard
- Context variables:
  - assignments (list of dict)
  - submissions (list of dict)
- Navigation mappings:
  - submit-assignment-button: url_for('submit_assignment', assignment_id=assignment.assignment_id)
  - back-to-dashboard: url_for('dashboard')

### templates/submit_assignment.html
- Page Title: Submit Assignment
- &lt;title&gt; and &lt;h1&gt;: "Submit Assignment"
- Element IDs:
  - submit-page: Div container
  - assignment-info: Div showing assignment title and description
  - submission-text: Textarea input for answer
  - submit-button: Button to submit form
  - back-to-assignments: Button linking back to assignments list
- Context variables:
  - assignment (dict)
  - submission_success (bool, optional)
- Navigation mappings:
  - submit-button: POST to /assignments/&lt;assignment_id&gt;/submit
  - back-to-assignments: url_for('my_assignments')

### templates/certificates.html
- Page Title: My Certificates
- &lt;title&gt; and &lt;h1&gt;: "My Certificates"
- Element IDs:
  - certificates-page: Div container
  - certificates-grid: Div grid of certificates
  - back-to-dashboard: Button linking back to dashboard
- Context variables:
  - certificates (list of dict)
  - courses (dict mapping course_id to course title)
- Navigation mappings:
  - back-to-dashboard: url_for('dashboard')
- Notes:
  - Only certificates for completed courses are displayed

### templates/profile.html
- Page Title: My Profile
- &lt;title&gt; and &lt;h1&gt;: "My Profile"
- Element IDs:
  - profile-page: Div container
  - profile-email: Input field for email
  - profile-fullname: Input field for full name
  - update-profile-button: Button to submit profile update
  - back-to-dashboard: Button linking back to dashboard
- Context variables:
  - user (dict {username, email, fullname})
- Navigation mappings:
  - update-profile-button: POST to /profile/update
  - back-to-dashboard: url_for('dashboard')

---

## Section 3: Data File Schemas (For Backend Developer)

### data/users.txt
- Fields (pipe-delimited): username|email|fullname
- Description: Stores registered users with contact info
- Examples:
  - john|john@student.com|John Student
  - alice|alice@instructor.com|Alice Professor
  - jane|jane@student.com|Jane Learner

### data/courses.txt
- Fields (pipe-delimited): course_id|title|description|category|level|duration|status
- Description: Catalog of courses with metadata and availability
- Examples:
  - 1|Python Programming|Learn Python from scratch|Programming|Beginner|40 hours|Active
  - 2|Web Development|Build modern websites|Web|Intermediate|60 hours|Active
  - 3|Data Science|Introduction to data analysis|Data|Advanced|80 hours|Active

### data/enrollments.txt
- Fields (pipe-delimited): enrollment_id|username|course_id|enrollment_date|progress|status
- Description: Tracks user enrollments, progress percentage and status
- Examples:
  - 1|john|1|2024-11-01|75|In Progress
  - 2|jane|1|2024-10-15|100|Completed
  - 3|john|2|2024-11-10|25|In Progress

### data/assignments.txt
- Fields (pipe-delimited): assignment_id|course_id|title|description|due_date|max_points
- Description: Assignments including details and scoring
- Examples:
  - 1|1|Python Basics Quiz|Complete the quiz on variables and data types|2024-12-01|100
  - 2|1|Final Project|Build a calculator application|2024-12-15|200

### data/submissions.txt
- Fields (pipe-delimited): submission_id|assignment_id|username|submission_text|submit_date|grade|feedback
- Description: Stores text submissions with grading info
- Examples:
  - 1|1|john|My answers are...|2024-11-25|85|Good work!
  - 2|2|jane|Here is my project...|2024-11-20|95|Excellent!

### data/certificates.txt
- Fields (pipe-delimited): certificate_id|username|course_id|issue_date
- Description: Certificates of course completion
- Examples:
  - 1|jane|1|2024-11-22


---

*End of design_spec.md*