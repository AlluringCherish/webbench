# OnlineCourse Application Design Specification

This document provides detailed design specifications for the "OnlineCourse" Flask web application. It covers Flask Routes, HTML Template Specifications, and Data Schemas to enable independent backend and frontend development.

---

# Section 1: Flask Routes Specifications

| Route URL                  | Function Name            | HTTP Method | Template File               | Context Variables                                                                                                    | Notes on Business Logic                                                                                          |
|----------------------------|--------------------------|-------------|-----------------------------|---------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------|
| `/`                        | `root`                   | GET         | None (redirect)              | None                                                                                                                | Redirects to `/dashboard`                                                                                       |
| `/dashboard`               | `dashboard`              | GET         | `dashboard.html`             | `user_name` (str)<br>`enrollments` (list of dict with `course_title` (str), `progress` (int))                      | Displays user's enrolled courses and progress                                                                  |
| `/courses`                 | `available_courses`      | GET         | `available_courses.html`     | `courses` (list of dict with `course_id` (int), `title` (str), `description` (str))                                 | Shows list of all active available courses                                                                      |
| `/course/<int:course_id>` | `course_details`         | GET         | `course_details.html`        | `course` (dict with keys: `course_id`, `title`, `description`)<br>`enrolled` (bool)<br>`enrollment_date` (str) <br>`progress` (int) | Shows details for one course; enroll button enabled if not enrolled; shows enrollment info if enrolled         |
| `/enroll/<int:course_id>` | `enroll`                 | POST        | Redirect to `/dashboard`     | None                                                                                                                | Enrolls user in the course; creates enrollment entry with 0% progress and current date                           |
| `/my-courses`             | `my_courses`             | GET         | `my_courses.html`            | `my_courses` (list of dict with `course_id`, `title`, `progress` (int))                                           | Lists enrolled courses with progress, each with continue button                                                |
| `/learning/<int:course_id>`| `learning_page`           | GET         | `learning_page.html`         | `course_id` (int)<br>`lessons` (list of dict with `lesson_id`, `title`, `completed` (bool))<br>`current_lesson` (dict with `title`, `content`) | Displays lessons, marks lesson complete button, progress updated, must complete lessons in sequence            |
| `/mark-lesson-completed/<int:course_id>/<int:lesson_id>` | `mark_lesson_completed` | POST        | Redirect to `/learning/<course_id>` | None                                                                                                                | Updates lesson completion and enrollment progress; triggers certificate if progress = 100%                    |
| `/assignments`            | `assignments`            | GET         | `assignments.html`           | `assignments` (list of dict with `assignment_id`, `title`, `due_date`, `status`)                                  | Shows assignments table; submit button enabled for pending assignments                                         |
| `/submit-assignment/<int:assignment_id>` | `submit_assignment`       | GET, POST   | `assignment_submission.html` | GET: `assignment` (dict with `title`, `description`)<br>POST: None                                                   | GET: shows submission form; POST: records submission, grade, feedback, and submit date                         |
| `/certificates`          | `certificates`           | GET         | `certificates.html`          | `certificates` (list of dict with `certificate_id`, `username`, `course_title`, `issue_date`)                       | Shows earned certificates grid                                                                                  |
| `/profile`               | `user_profile`           | GET         | `user_profile.html`           | `user` (dict with `email`, `name`)                                                                                | Displays and allows editing of user profile                                                                     |
| `/profile/update`        | `update_profile`         | POST        | Redirect to `/profile`        | Form data: `email`, `name`                                                                                        | Updates user profile data                                                                                        |

---

# Section 2: HTML Template Specifications

Each template is described with exact element IDs, context variables, and navigation.

### 1. dashboard.html
- **Page Title**: Learning Dashboard
- **Container ID**: `dashboard-page` (div)
- Elements:
  - `welcome-message` (h1): "Welcome, {{ user_name }}!"
  - `enrolled-courses` (div): Lists enrolled courses, each displaying course title and progress
  - `browse-courses-button` (button): Navigates to `url_for('available_courses')`
  - `my-courses-button` (button): Navigates to `url_for('my_courses')`
- Context Variables: `user_name` (str), `enrollments` (list of dict)


### 2. available_courses.html
- **Page Title**: Available Courses
- **Container ID**: `catalog-page` (div)
- Elements:
  - `search-input` (input text) for searching courses
  - `course-grid` (div) containing course cards
  - Each course card has a button with id `view-course-button-{{ course_id }}` linking to `url_for('course_details', course_id=course_id)`
  - `back-to-dashboard` (button) linking to `url_for('dashboard')`
- Context Variables: `courses` (list of dict)


### 3. course_details.html
- **Page Title**: Course Details
- **Container ID**: `course-details-page` (div)
- Elements:
  - `course-title` (h1)
  - `course-description` (div)
  - `enroll-button` (button): Disabled and labeled "Already Enrolled" if user enrolled
  - `back-to-catalog` (button) linking to `url_for('available_courses')`
- Context Variables: `course` (dict), `enrolled` (bool), `enrollment_date` (str), `progress` (int)


### 4. my_courses.html
- **Page Title**: My Courses
- **Container ID**: `my-courses-page` (div)
- Elements:
  - `courses-list` (div): List of enrolled courses with progress
  - Each course has a button with id `continue-learning-button-{{ course_id }}` linking to `url_for('learning_page', course_id=course_id)`
  - `back-to-dashboard` (button) linking to `url_for('dashboard')`
- Context Variables: `my_courses` (list of dict)


### 5. learning_page.html
- **Page Title**: Course Learning
- **Container ID**: `learning-page` (div)
- Elements:
  - `lessons-list` (div): List of lessons
  - Each lesson has id `lesson-{{ lesson_id }}` and a button `mark-complete-button`
  - `lesson-content` (div): Display current lesson
  - `mark-complete-button` (button): Marks lesson complete
  - `back-to-my-courses` (button) linking to `url_for('my_courses')`
- Context Variables: `lessons` (list), `current_lesson` (dict), `course_id` (int)


### 6. assignments.html
- **Page Title**: My Assignments
- **Container ID**: `assignments-page` (div)
- Elements:
  - `assignments-table` (table) listing assignments
  - Submission button per assignment with ID `submit-assignment-button-{{ assignment_id }}`
  - `back-to-dashboard` (button) linking to `url_for('dashboard')`
- Context Variables: `assignments` (list)


### 7. assignment_submission.html
- **Page Title**: Submit Assignment
- **Container ID**: `submit-page` (div)
- Elements:
  - `assignment-info` (div) showing assignment title and description
  - `submission-text` (textarea) for text input
  - `submit-button` (button) to POST submission
  - `back-to-assignments` (button) linking to `url_for('assignments')`
- Context Variables: `assignment` (dict)


### 8. certificates.html
- **Page Title**: My Certificates
- **Container ID**: `certificates-page` (div)
- Elements:
  - `certificates-grid` (div) displaying earned certificate cards
  - `back-to-dashboard` (button) linking to `url_for('dashboard')`
- Context Variables: `certificates` (list)


### 9. user_profile.html
- **Page Title**: My Profile
- **Container ID**: `profile-page` (div)
- Elements:
  - `profile-email` (input type="email")
  - `profile-fullname` (input type="text")
  - `update-profile-button` (button) to submit form
  - `back-to-dashboard` (button) linking to `url_for('dashboard')`
- Context Variables: `user` (dict)

---

# Section 3: Data Schemas

All data is stored in the `data/` directory with pipe-delimited text files.

### 1. users.txt
- Path: `data/users.txt`
- Format: `username|email|fullname`
- Purpose: Stores user login and profile info
- Examples:
  ```
  john|john@student.com|John Student
  alice|alice@instructor.com|Alice Professor
  jane|jane@student.com|Jane Learner
  ```

### 2. courses.txt
- Path: `data/courses.txt`
- Format: `course_id|title|description|category|level|duration|status`
- Purpose: Stores course metadata
- Examples:
  ```
  1|Python Programming|Learn Python from scratch|Programming|Beginner|40 hours|Active
  2|Web Development|Build modern websites|Web|Intermediate|60 hours|Active
  3|Data Science|Introduction to data analysis|Data|Advanced|80 hours|Active
  ```

### 3. enrollments.txt
- Path: `data/enrollments.txt`
- Format: `enrollment_id|username|course_id|enrollment_date|progress|status`
- Purpose: Records user course enrollments and progress
- Examples:
  ```
  1|john|1|2024-11-01|75|In Progress
  2|jane|1|2024-10-15|100|Completed
  3|john|2|2024-11-10|25|In Progress
  ```

### 4. assignments.txt
- Path: `data/assignments.txt`
- Format: `assignment_id|course_id|title|description|due_date|max_points`
- Purpose: Stores assignments metadata
- Examples:
  ```
  1|1|Python Basics Quiz|Complete the quiz on variables and data types|2024-12-01|100
  2|1|Final Project|Build a calculator application|2024-12-15|200
  ```

### 5. submissions.txt
- Path: `data/submissions.txt`
- Format: `submission_id|assignment_id|username|submission_text|submit_date|grade|feedback`
- Purpose: Stores user assignment submissions and grading
- Examples:
  ```
  1|1|john|My answers are...|2024-11-25|85|Good work!
  2|2|jane|Here is my project...|2024-11-20|95|Excellent!
  ```

### 6. certificates.txt
- Path: `data/certificates.txt`
- Format: `certificate_id|username|course_id|issue_date`
- Purpose: Records issued course completion certificates
- Examples:
  ```
  1|jane|1|2024-11-22
  ```

---

# End of Design Specification
