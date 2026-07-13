# Alternative Design Candidate B for OnlineCourse Web Application

---

## 1. Overview
This alternative design candidate outlines a comprehensive blueprint for the OnlineCourse application, meeting all functionality described in the user requirements in an independent and fresh way. The app is structured around nine main pages with routes, and a set of UI elements identified by IDs. Data persistence utilizes local text files.

The design emphasizes clear user flows, consistent naming conventions, and detailed specifications of page elements, navigation, data handling, and functional constraints.

---

## 2. Routes and Page Layouts

### 2.1 Dashboard Page
- **Route:** `/dashboard`
- **Page Title:** Learning Dashboard
- **Purpose:** Main hub displaying greeting, enrolled courses, and navigation options.
- **Page Container ID:** `dashboard-page`

**Elements:**
- `welcome-message` (H1): Displays "Welcome, {fullname}".
- `enrolled-courses` (Div): Shows a concise list or cards of courses the logged-in user is enrolled in, including their progress percentages.
- `browse-courses-button` (Button): Navigates to Course Catalog (`/courses/catalog`).
- `my-courses-button` (Button): Navigates to My Courses (`/courses/mine`).

**Behavior:**
- On load, read `enrollments.txt` filtering by current `username`, then cross-reference with `courses.txt` to retrieve course titles and progress.
- If no enrollments, display a message "You have not enrolled in any courses yet."

---

### 2.2 Course Catalog Page
- **Route:** `/courses/catalog`
- **Page Title:** Available Courses
- **Page Container ID:** `catalog-page`

**Elements:**
- `search-input` (Input): Text input for filtering courses by title or category.
- `course-grid` (Div): Grid container featuring course cards.
- Each course card includes:
  - Title and category display.
  - `view-course-button-{course_id}` (Button): To view full course details.
- `back-to-dashboard` (Button): To return to `/dashboard`.

**Behavior:**
- On entering, read all courses from `courses.txt` with status `Active`.
- Filter courses dynamically as user types in `search-input`.
- Clicking `view-course-button-{course_id}` routes to `/courses/details/{course_id}`.

---

### 2.3 Course Details Page
- **Route:** `/courses/details/{course_id}`
- **Page Title:** Course Details
- **Page Container ID:** `course-details-page`

**Elements:**
- `course-title` (H1): Displays course title.
- `course-description` (Div): Full course description.
- `enroll-button` (Button): If user already enrolled, shows "Already Enrolled" disabled; otherwise "Enroll Now" enabled.
- `back-to-catalog` (Button): Returns to `/courses/catalog`.

**Behavior:**
- On load, read course by `course_id` from `courses.txt`.
- Check enrollment status by reading `enrollments.txt` for current user and course.
- If enrolling:
  - Append new record with unique enrollment_id, username, course_id, current date (YYYY-MM-DD), 0 progress, and status "In Progress".
- After enrollment, update `enroll-button` state to disabled.

---

### 2.4 My Courses Page
- **Route:** `/courses/mine`
- **Page Title:** My Courses
- **Page Container ID:** `my-courses-page`

**Elements:**
- `courses-list` (Div): List or cards of user's enrolled courses.
- For each course:
  - Displays course title, progress percentage, and status.
  - `continue-learning-button-{course_id}` (Button): Navigates to course learning page for this course.
- `back-to-dashboard` (Button): Returns to `/dashboard`.

**Behavior:**
- On load, read enrollments for user from `enrollments.txt`.
- Display all enrolled courses with progress.
- If no courses, show "No enrolled courses found."

---

### 2.5 Course Learning Page
- **Route:** `/courses/learn/{course_id}`
- **Page Title:** Course Learning
- **Page Container ID:** `learning-page`

**Elements:**
- `lessons-list` (Div): List all lessons sequentially with completion status indicators.
- `lesson-content` (Div): Displays content for the currently selected lesson.
- `mark-complete-button` (Button): Enables marking the current lesson complete.
- `back-to-my-courses` (Button): Returns to `/courses/mine`.

**Behavior:**
- Lessons for courses are implied as ordered units. Since lessons details are not in dataset, assume course lessons file in data may be part of extended design.
- On load, display lesson 1 content if no progress, otherwise first incomplete lesson.
- Marking lesson complete increments progress as `(completed lessons / total lessons) * 100`. Save updated progress in `enrollments.txt`.
- Lessons must be completed sequentially, so `mark-complete-button` is disabled unless current lesson is the next in sequence.
- When progress reaches 100%, update enrollment status to "Completed" and add certificate entry to `certificates.txt` with unique certificate_id, username, course_id, and current date.

---

### 2.6 My Assignments Page
- **Route:** `/assignments`
- **Page Title:** My Assignments
- **Page Container ID:** `assignments-page`

**Elements:**
- `assignments-table` (Table): Columns for assignment ID, title, due date, status (pending/submitted), and submission grade if any.
- `submit-assignment-button-{assignment_id}` (Button): Available for pending assignments to submit work.
- `back-to-dashboard` (Button): Returns to `/dashboard`.

**Behavior:**
- On load, read `assignments.txt` for courses user is enrolled in.
- Read `submissions.txt` filtering by username and matching assignment IDs.
- Status is "Pending" if no submission found, otherwise "Submitted".

---

### 2.7 Submit Assignment Page
- **Route:** `/assignments/submit/{assignment_id}`
- **Page Title:** Submit Assignment
- **Page Container ID:** `submit-page`

**Elements:**
- `assignment-info` (Div): Shows assignment title and description.
- `submission-text` (Textarea): For user to enter assignment answers.
- `submit-button` (Button): To submit the text response.
- `back-to-assignments` (Button): Returns to `/assignments`.

**Behavior:**
- On load, read assignment data from `assignments.txt` by `assignment_id`.
- On submit:
  - Append new record to `submissions.txt` with unique submission ID, assignment ID, username, submission text, submit date, null grade and feedback.
  - Display confirmation message.

---

### 2.8 Certificates Page
- **Route:** `/certificates`
- **Page Title:** My Certificates
- **Page Container ID:** `certificates-page`

**Elements:**
- `certificates-grid` (Div): Displays certificates as cards showing course title and issue date.
- `back-to-dashboard` (Button): Returns to `/dashboard`.

**Behavior:**
- On load, read `certificates.txt` for user’s certificates.
- Cross reference course titles via `courses.txt`.
- Display only certificates for courses with completed enrollments.

---

### 2.9 User Profile Page
- **Route:** `/profile`
- **Page Title:** My Profile
- **Page Container ID:** `profile-page`

**Elements:**
- `profile-email` (Input): Editable email field initialized from `users.txt`.
- `profile-fullname` (Input): Editable full name field from `users.txt`.
- `update-profile-button` (Button): Saves changes.
- `back-to-dashboard` (Button): Returns to `/dashboard`.

**Behavior:**
- On load, populate from `users.txt` using username.
- On updating:
  - Modify line corresponding to username in `users.txt` safely.
  - Feedback message confirms update success.

---

## 3. Navigation and Interaction Flow

- App always starts at `/dashboard` after user login.
- From Dashboard:
  - Browse available courses via `/courses/catalog`.
  - View enrolled courses at `/courses/mine`.
  - Access assignments page `/assignments`.
  - View certificates at `/certificates`.
  - Edit profile at `/profile`.
- From Catalog:
  - View details at `/courses/details/{course_id}`.
  - Back to Dashboard with `back-to-dashboard`.
- From Course Details:
  - Enroll in course updates enrollment file.
  - Back to Catalog.
- From My Courses:
  - Continue learning navigates to `/courses/learn/{course_id}`.
  - Back to Dashboard.
- From Course Learning:
  - Mark lesson complete increases progress and checks completion.
  - Back to My Courses.
- From Assignments:
  - Submit assignment navigates to `/assignments/submit/{assignment_id}`.
  - Back to Dashboard.
- From Submit Assignment:
  - Submit button saves submission data.
  - Back to Assignments.
- From Certificates:
  - Back to Dashboard.
- From Profile:
  - Save profile changes.
  - Back to Dashboard.

All "back" buttons maintain consistent navigation patterns.

---

## 4. Data Handling and State Management

- All data files are located under a `data/` directory.
- Files are read fully into memory at page load to filter/view relevant data.
- Writes (enrollments.txt, submissions.txt, users.txt, certificates.txt) are atomic updates replacing the entire file or appending when possible.
- Unique IDs (enrollment, submission, certificate) are generated by incrementing the max existing ID.
- Progress updates on enrollments are written back consistently.
- For lesson sequencing, progress counters reflect how many lessons are completed; lessons must be accessed in order.
- Certificate issuance triggers immediately when progress reaches 100%, but only one certificate per course per user.

---

## 5. Dynamic Element IDs and Patterns

- `view-course-button-{course_id}`: Dynamically generated buttons on catalog page for each course.
- `continue-learning-button-{course_id}`: On My Courses page to access learning page.
- `submit-assignment-button-{assignment_id}`: On assignments page for pending assignments.

---

## 6. Behavioral Constraints

- Lessons can only be marked complete in sequential order; subsequent lessons remain locked until previous ones complete.
- Enrollment updates start at 0% progress.
- When progress reaches 100%, enrollment status updates from "In Progress" to "Completed".
- Certificate entries are created only once per user per course.
- Assignment submissions record submission dates for potential late tracking.
- User profile updates modify the users.txt file, preserving username integrity.

---

## 7. Summary
This design candidate provides a thorough, clear, and user-centric structure for all pages, navigation, data interactions, and functional logic for the OnlineCourse application. It maintains data integrity and usability while ensuring each page and route serve clear purposes and meet the user requirements independently.

---

*End of Design Candidate B*