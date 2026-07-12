# OnlineCourse Application Design Specification

---

## Section 1: Flask Routes Specification (For Backend Developer)

| Route Path                              | Function Name             | HTTP Method | Template File            | Context Variables                                                                                                  |
|---------------------------------------|---------------------------|-------------|--------------------------|-------------------------------------------------------------------------------------------------------------------|
| /                                     | root_redirect             | GET         | None                     | None (Redirects to /dashboard)                                                                                     |
| /dashboard                           | dashboard                 | GET         | dashboard.html           | username: str, fullname: str, enrolled_courses: List[Dict] (each with course_id, title, progress: int)             |
| /catalog                             | course_catalog            | GET         | catalog.html             | courses: List[Dict] (each with course_id, title, description, category, level, duration, status)                    |
| /course/<int:course_id>               | course_details            | GET         | course_details.html      | course: Dict (course_id, title, description, category, level, duration, status), is_enrolled: bool                 |
| /course/<int:course_id>/enroll         | enroll_course             | POST        | course_details.html      | course: Dict, is_enrolled: bool, message: str (enrollment success/fail message)                                   |
| /my-courses                         | my_courses                | GET         | my_courses.html          | enrolled_courses: List[Dict] (course_id, title, progress)                                                         |
| /learning/<int:course_id>            | course_learning           | GET         | course_learning.html     | course: Dict, lessons: List[Dict] (lesson_id, title, content), current_lesson_id: int, completed_lessons: List[int], progress: int |
| /learning/<int:course_id>/complete-lesson | complete_lesson           | POST        | course_learning.html     | course: Dict, lessons: List[Dict], current_lesson_id: int, completed_lessons: List[int], progress: int, message: str|
| /assignments                       | my_assignments            | GET         | assignments.html         | assignments: List[Dict] (assignment_id, course_id, title, description, due_date, max_points), submissions: List[Dict] (assignment_id, username, status) |
| /submit-assignment/<int:assignment_id>| submit_assignment         | GET         | submit_assignment.html   | assignment: Dict (assignment_id, course_id, title, description, due_date, max_points), username: str, message: str  |
| /submit-assignment/<int:assignment_id>| submit_assignment_post    | POST        | submit_assignment.html   | assignment: Dict, username: str, message: str                                                                       |
| /certificates                      | certificates              | GET         | certificates.html        | certificates: List[Dict] (certificate_id, course_id, title, issue_date)                                           |
| /profile                          | profile                   | GET         | profile.html             | username: str, email: str, fullname: str                                                                          |
| /profile/update                   | update_profile            | POST        | profile.html             | username: str, email: str, fullname: str, message: str                                                            |

### Route Notes:
- `/` redirects to `/dashboard`.
- Enrollment POST at `/course/<course_id>/enroll` adds an entry to `enrollments.txt` with current date, progress=0%, status='In Progress'. If user already enrolled, no duplicate allowed.
- Progress updating at `/learning/<course_id>/complete-lesson` checks lesson sequence, updates `enrollments.txt`, and if progress reaches 100%, adds certificate entry in `certificates.txt`.
- Assignment submission POST `/submit-assignment/<assignment_id>` adds entry to `submissions.txt` with status 'Submitted' and current date.
- Profile update POST `/profile/update` updates user's email and fullname in `users.txt`.

---

## Section 2: HTML Template Specifications (For Frontend Developer)

### templates/dashboard.html
- **Page Title**: Learning Dashboard
- **Root Container ID**: `dashboard-page`
- **H1 ID**: `welcome-message` (displays "Welcome, {{ fullname }}")
- **Div ID**: `enrolled-courses` (lists courses user enrolled with progress % shown)
- **Buttons:**
  - `browse-courses-button` navigates to `url_for('course_catalog')`
  - `my-courses-button` navigates to `url_for('my_courses')`

- **Context Variables:**
  - `username`: str
  - `fullname`: str
  - `enrolled_courses`: list of dict with keys: course_id (int), title (str), progress (int)

### templates/catalog.html
- **Page Title**: Available Courses
- **Root Container ID**: `catalog-page`
- **Input ID**: `search-input` (text input for searching courses)
- **Div ID**: `course-grid` (grid of course cards)
- **Buttons:**
  - `view-course-button-{{ course.course_id }}` for each course iterated via Jinja2 loop
  - `back-to-dashboard` navigates to `url_for('dashboard')`

- **Context Variables:**
  - `courses`: list of dict with fields course_id (int), title (str), description (str), category (str), level (str), duration (str), status (str)

### templates/course_details.html
- **Page Title**: Course Details
- **Root Container ID**: `course-details-page`
- **H1 ID**: `course-title` (displays course.title)
- **Div ID**: `course-description` (displays course.description)
- **Buttons:**
  - `enroll-button` (disabled and text "Already Enrolled" if `is_enrolled` true; otherwise enabled with text "Enroll")
  - `back-to-catalog` navigates to `url_for('course_catalog')`

- **Context Variables:**
  - `course`: dict
  - `is_enrolled`: bool

- **Form:** POST to `/course/{{ course.course_id }}/enroll` on clicking enroll button

### templates/my_courses.html
- **Page Title**: My Courses
- **Root Container ID**: `my-courses-page`
- **Div ID**: `courses-list` (list with each course's title and progress)
- **Buttons:**
  - `continue-learning-button-{{ course.course_id }}` for each enrolled course
  - `back-to-dashboard` navigates to `url_for('dashboard')`

- **Context Variables:**
  - `enrolled_courses`: list of dict with course_id, title, progress

### templates/course_learning.html
- **Page Title**: Course Learning
- **Root Container ID**: `learning-page`
- **Div ID**: `lessons-list` (list lessons, highlighting current lesson)
- **Div ID**: `lesson-content` (displays current lesson content)
- **Buttons:**
  - `mark-complete-button` POSTs completion for current lesson
  - `back-to-my-courses` navigates to `url_for('my_courses')`

- **Context Variables:**
  - `course`: dict
  - `lessons`: list of dicts (lesson_id: int, title: str, content: str)
  - `current_lesson_id`: int
  - `completed_lessons`: list of int
  - `progress`: int

### templates/assignments.html
- **Page Title**: My Assignments
- **Root Container ID**: `assignments-page`
- **Table ID**: `assignments-table` (rows for each assignment with due date and status)
- **Buttons:**
  - `submit-assignment-button-{{ assignment.assignment_id }}` for assignments pending submission
  - `back-to-dashboard` navigates to `url_for('dashboard')`

- **Context Variables:**
  - `assignments`: list of dict (assignment_id, course_id, title, description, due_date, max_points)
  - `submissions`: list of dict (assignment_id, username, status)

### templates/submit_assignment.html
- **Page Title**: Submit Assignment
- **Root Container ID**: `submit-page`
- **Div ID**: `assignment-info` (title and description of assignment)
- **Textarea ID**: `submission-text`
- **Buttons:**
  - `submit-button` POSTs text to `/submit-assignment/{{ assignment.assignment_id }}`
  - `back-to-assignments` navigates to `url_for('my_assignments')`

- **Context Variables:**
  - `assignment`: dict
  - `username`: str
  - `message`: str (confirmation or error)

### templates/certificates.html
- **Page Title**: My Certificates
- **Root Container ID**: `certificates-page`
- **Div ID**: `certificates-grid` (grid of certificates by course)
- **Buttons:**
  - `back-to-dashboard` navigates to `url_for('dashboard')`

- **Context Variables:**
  - `certificates`: list of dict (certificate_id, course_id, title, issue_date)

### templates/profile.html
- **Page Title**: My Profile
- **Root Container ID**: `profile-page`
- **Inputs:**
  - `profile-email` (type email) prefilled with user's email
  - `profile-fullname` prefilled with user's fullname
- **Buttons:**
  - `update-profile-button` POSTs updated profile to `/profile/update`
  - `back-to-dashboard` navigates to `url_for('dashboard')`

- **Context Variables:**
  - `username`: str
  - `email`: str
  - `fullname`: str
  - `message`: str (update status)

---

## Section 3: Data File Schemas (For Backend Developer)

### 1. User Data
- File: `data/users.txt`
- Format: `username|email|fullname`
- Fields:
  - `username`: unique user identifier (str)
  - `email`: user's email address (str)
  - `fullname`: user's full name (str)

- Examples:
```
john|john@student.com|John Student
alice|alice@instructor.com|Alice Professor
jane|jane@student.com|Jane Learner
```

### 2. Courses Data
- File: `data/courses.txt`
- Format: `course_id|title|description|category|level|duration|status`
- Fields:
  - `course_id`: unique numeric course ID (int)
  - `title`: course title (str)
  - `description`: full course description (str)
  - `category`: course category (str)
  - `level`: course difficulty level (str)
  - `duration`: estimated completion time (str, e.g., "40 hours")
  - `status`: active or inactive (str)

- Examples:
```
1|Python Programming|Learn Python from scratch|Programming|Beginner|40 hours|Active
2|Web Development|Build modern websites|Web|Intermediate|60 hours|Active
3|Data Science|Introduction to data analysis|Data|Advanced|80 hours|Active
```

### 3. Enrollments Data
- File: `data/enrollments.txt`
- Format: `enrollment_id|username|course_id|enrollment_date|progress|status`
- Fields:
  - `enrollment_id`: unique numeric ID (int)
  - `username`: user identifier (str)
  - `course_id`: numeric course ID (int)
  - `enrollment_date`: ISO date string `YYYY-MM-DD` (str)
  - `progress`: completion percentage 0-100 (int)
  - `status`: enrollment status e.g., "In Progress", "Completed" (str)

- Examples:
```
1|john|1|2024-11-01|75|In Progress
2|jane|1|2024-10-15|100|Completed
3|john|2|2024-11-10|25|In Progress
```

### 4. Assignments Data
- File: `data/assignments.txt`
- Format: `assignment_id|course_id|title|description|due_date|max_points`
- Fields:
  - `assignment_id`: unique numeric ID (int)
  - `course_id`: numeric course ID (int)
  - `title`: assignment title (str)
  - `description`: assignment details (str)
  - `due_date`: ISO date string `YYYY-MM-DD` (str)
  - `max_points`: maximum points achievable (int)

- Examples:
```
1|1|Python Basics Quiz|Complete the quiz on variables and data types|2024-12-01|100
2|1|Final Project|Build a calculator application|2024-12-15|200
```

### 5. Submissions Data
- File: `data/submissions.txt`
- Format: `submission_id|assignment_id|username|submission_text|submit_date|grade|feedback`
- Fields:
  - `submission_id`: unique numeric ID (int)
  - `assignment_id`: numeric assignment ID (int)
  - `username`: user identifier (str)
  - `submission_text`: text of user's submission (str)
  - `submit_date`: ISO date string `YYYY-MM-DD` (str)
  - `grade`: numeric grade (int)
  - `feedback`: textual feedback (str)

- Examples:
```
1|1|john|My answers are...|2024-11-25|85|Good work!
2|2|jane|Here is my project...|2024-11-20|95|Excellent!
```

### 6. Certificates Data
- File: `data/certificates.txt`
- Format: `certificate_id|username|course_id|issue_date`
- Fields:
  - `certificate_id`: unique numeric ID (int)
  - `username`: user identifier (str)
  - `course_id`: numeric course ID (int)
  - `issue_date`: ISO date string `YYYY-MM-DD` (str)

- Examples:
```
1|jane|1|2024-11-22
```

---

*End of Design Specification*