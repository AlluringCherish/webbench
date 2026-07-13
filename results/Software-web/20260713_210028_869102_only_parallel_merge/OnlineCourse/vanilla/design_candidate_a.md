# Design Candidate A for OnlineCourse Web Application

---

## General Notes
- All pages are routed under URL schemes starting with `/`.
- The web application uses local text files stored in the `data` directory for persistence.
- User authentication is assumed and the current logged-in username is available for data lookups.
- Dynamic elements referencing specific courses, assignments, or submissions use IDs interpolated with the respective entity ID.

---

# 1. Dashboard Page

- **Route URL:** `/dashboard`
- **Page Title:** Learning Dashboard
- 
### Element IDs and Types:
- `dashboard-page` (div): Container for the entire dashboard page.
- `welcome-message` (h1): Displays "Welcome, {fullname}" where fullname is derived from `users.txt`.
- `enrolled-courses` (div): Displays the list of courses the user is currently enrolled in with progress summaries.
- `browse-courses-button` (button): Label "Browse Courses"; navigates user to `/catalog`.
- `my-courses-button` (button): Label "My Courses"; navigates user to `/my-courses`.

### Data Handling:
- Reads `enrollments.txt` for current user's enrollments.
- Reads `courses.txt` to display course titles and info for enrolled courses.

### User Interactions:
- Clicking `browse-courses-button` leads to Course Catalog Page.
- Clicking `my-courses-button` leads to My Courses Page.


# 2. Course Catalog Page

- **Route URL:** `/catalog`
- **Page Title:** Available Courses

### Element IDs and Types:
- `catalog-page` (div): Container for the entire catalog.
- `search-input` (input text): For searching/filtering courses by title or category.
- `course-grid` (div): Grid container displaying each course card.
- `view-course-button-{course_id}` (button): Each course card includes this button with ID pattern where `{course_id}` replaced by course's ID.
- `back-to-dashboard` (button): Navigates back to `/dashboard`.

### Data Handling:
- Reads `courses.txt`, filtered by search input criteria.

### User Interactions:
- User types in `search-input` to filter courses dynamically.
- Clicking on `view-course-button-{course_id}` navigates to `/course/{course_id}` (Course Details Page).
- Clicking `back-to-dashboard` returns user to Dashboard.


# 3. Course Details Page

- **Route URL:** `/course/{course_id}`
- **Page Title:** Course Details

### Element IDs and Types:
- `course-details-page` (div): Container for detailed course info.
- `course-title` (h1): Displays the course title.
- `course-description` (div): Displays the detailed course description.
- `enroll-button` (button): Label "Enroll" or "Already Enrolled" if user enrolled.
- `back-to-catalog` (button): Returns to `/catalog`.

### Data Handling:
- Reads `courses.txt` for course details.
- Reads `enrollments.txt` to check if the current user is enrolled.
- On click `enroll-button` if not enrolled:
  - Adds a new record to `enrollments.txt`: generates a new enrollment_id (incremental or max+1), stores username, course_id, current date as enrollment_date, progress=0, status="In Progress".
  - Button updates to "Already Enrolled" and disables.

### User Interactions:
- User can enroll only if not previously enrolled.
- Clicking `back-to-catalog` navigates back to Course Catalog.


# 4. My Courses Page

- **Route URL:** `/my-courses`
- **Page Title:** My Courses

### Element IDs and Types:
- `my-courses-page` (div): Container for the page.
- `courses-list` (div): Lists enrolled courses with progress bars and info.
- `continue-learning-button-{course_id}` (button): For each enrolled course, allows continuing learning in that course.
- `back-to-dashboard` (button): Returns to `/dashboard`.

### Data Handling:
- Reads `enrollments.txt` and `courses.txt` to assemble user's enrolled courses and progress.

### User Interactions:
- Clicking `continue-learning-button-{course_id}` navigates to `/learn/{course_id}` (Course Learning Page).
- Clicking `back-to-dashboard` returns to Dashboard.


# 5. Course Learning Page

- **Route URL:** `/learn/{course_id}`
- **Page Title:** Course Learning

### Element IDs and Types:
- `learning-page` (div): Container for course learning.
- `lessons-list` (div): Displays a sequenced list of lessons.
- `lesson-content` (div): Shows content/materials for the selected lesson.
- `mark-complete-button` (button): Allows user to mark the current lesson as completed.
- `back-to-my-courses` (button): Returns to `/my-courses`.

### Data Handling:
- Reads courses syllabus (lessons) from `courses.txt` or associated syllabus stored in related data (assuming course details include numbered lessons).
- Reads `enrollments.txt` for progress status.
- Marks progress as (number_of_lessons_completed / total_lessons) * 100.
- Updates enrollment progress in `enrollments.txt` upon marking a lesson complete.
- When progress reaches 100%, updates enrollment status to "Completed" and writes certificate entry in `certificates.txt` if not already existing.

### User Interactions and Constraints:
- Lessons must be completed sequentially (user can only mark the next incomplete lesson).
- `mark-complete-button` is disabled if the current lesson is already completed or if previous lessons are incomplete.
- Clicking `back-to-my-courses` returns to My Courses.


# 6. My Assignments Page

- **Route URL:** `/assignments`
- **Page Title:** My Assignments

### Element IDs and Types:
- `assignments-page` (div): Container for assignments list.
- `assignments-table` (table): Shows all assignments related to courses user is enrolled in.
- `submit-assignment-button-{assignment_id}` (button): For assignments pending submission, this button allows submission.
- `back-to-dashboard` (button): Returns to dashboard.

### Data Handling:
- Reads `assignments.txt` filtered by user's enrolled courses.
- Reads `submissions.txt` to identify submitted assignments.

### User Interactions:
- If assignment not submitted or status pending, `submit-assignment-button-{assignment_id}` is enabled.
- Clicking the button navigates to `/submit-assignment/{assignment_id}`.
- Clicking `back-to-dashboard` navigates back to dashboard.


# 7. Submit Assignment Page

- **Route URL:** `/submit-assignment/{assignment_id}`
- **Page Title:** Submit Assignment

### Element IDs and Types:
- `submit-page` (div): Container for assignment submission form.
- `assignment-info` (div): Shows title and description of assignment.
- `submission-text` (textarea): Text input for user's assignment response.
- `submit-button` (button): Submits the text response.
- `back-to-assignments` (button): Returns to assignments page.

### Data Handling:
- Reads `assignments.txt` for assignment details.
- On submit:
  - Creates new entry in `submissions.txt` with new `submission_id`, assignment_id, username, submission_text, current date, grade=null, feedback="".

### User Interactions:
- Upon successful submission, displays confirmation message.
- Clicking `back-to-assignments` goes back to My Assignments.


# 8. Certificates Page

- **Route URL:** `/certificates`
- **Page Title:** My Certificates

### Element IDs and Types:
- `certificates-page` (div): Container for certificates list.
- `certificates-grid` (div): Grid displaying certificates earned by the user.
- `back-to-dashboard` (button): Returns to dashboard.

### Data Handling:
- Reads `certificates.txt` filtered by username.
- Reads `courses.txt` to get course titles for certificates.
- Certificates generated automatically when enrollment progress reaches 100% and status="Completed" (done in Course Learning Page).

### User Interactions:
- Only completed courses with certificates appear.
- Clicking `back-to-dashboard` returns to Dashboard.


# 9. User Profile Page

- **Route URL:** `/profile`
- **Page Title:** My Profile

### Element IDs and Types:
- `profile-page` (div): Container for profile edit page.
- `profile-email` (input text): Editable email field.
- `profile-fullname` (input text): Editable full name field.
- `update-profile-button` (button): Saves changes to `users.txt`.
- `back-to-dashboard` (button): Returns to Dashboard.

### Data Handling:
- Reads current user entry from `users.txt`.
- On update, writes changes back to `users.txt` ensuring unique username remains unchanged.

### User Interactions:
- User edits email and fullname.
- After clicking update, changes are persisted.
- Clicking `back-to-dashboard` navigates back to Dashboard.


---

# Summary of Route URLs:
| Page               | URL Pattern                  |
|--------------------|-----------------------------|
| Dashboard          | /dashboard                  |
| Course Catalog     | /catalog                    |
| Course Details     | /course/{course_id}         |
| My Courses         | /my-courses                 |
| Course Learning    | /learn/{course_id}          |
| My Assignments     | /assignments                |
| Submit Assignment  | /submit-assignment/{assignment_id} |
| Certificates       | /certificates               |
| User Profile       | /profile                    |


---

# Navigation Summary
- Dashboard serves as the home and hub.
- Navigation flows:
  - Dashboard -> Catalog
  - Catalog -> Course Details
  - Course Details -> Catalog
  - Dashboard -> My Courses
  - My Courses -> Course Learning
  - Course Learning -> My Courses
  - Dashboard -> My Assignments
  - My Assignments -> Submit Assignment
  - Submit Assignment -> My Assignments
  - Dashboard -> Certificates
  - Dashboard -> Profile
  - Profile -> Dashboard


---

# Data File Summary and Responsibilities
- `users.txt`: Stores all user info, used for profile display and welcome messages.
- `courses.txt`: Stores all course metadata used for catalog and course details.
- `enrollments.txt`: Tracks user enrollments, progress, and status.
- `assignments.txt`: Stores assignments linked to courses.
- `submissions.txt`: Records assignment submissions.
- `certificates.txt`: Stores issued course completion certificates.


---

# Restrictions and Constraints
- Enroll button disabled if already enrolled.
- Lessons must be completed sequentially; user cannot jump ahead.
- Progress percentage updated only when lesson marked complete.
- Certificate created automatically upon reaching 100% progress.
- Assignment submission must be recorded with timestamp.
- Profile updates preserve username, only email and fullname editable.

---

This completes the full design candidate for the 9 pages of OnlineCourse application including routes, element IDs, navigation, data handling, and interaction logic.