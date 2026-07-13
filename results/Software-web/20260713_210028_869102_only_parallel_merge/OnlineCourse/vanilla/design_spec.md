# Merged Design Specification for OnlineCourse Web Application

---

## 1. General Overview
- The OnlineCourse web application uses local text files stored in the `data/` directory for data persistence.
- User authentication is assumed; the current logged-in username is available for data lookups.
- Dynamic element IDs that reference specific courses, assignments, or other entities use patterns with entity IDs embedded.
- The application has nine main pages with clearly defined routes and UI elements.

---

## 2. Page Routes, Titles, and Element IDs

| Page                 | Route URL Pattern                 | Page Title          | Main Container ID           |
|----------------------|---------------------------------|---------------------|-----------------------------|
| Dashboard            | /dashboard                      | Learning Dashboard  | dashboard-page               |
| Course Catalog       | /courses/catalog                | Available Courses   | catalog-page                 |
| Course Details       | /courses/details/{course_id}   | Course Details      | course-details-page         |
| My Courses           | /courses/mine                  | My Courses          | my-courses-page             |
| Course Learning      | /courses/learn/{course_id}     | Course Learning     | learning-page               |
| My Assignments       | /assignments                   | My Assignments      | assignments-page            |
| Submit Assignment    | /assignments/submit/{assignment_id} | Submit Assignment   | submit-page                 |
| Certificates         | /certificates                  | My Certificates     | certificates-page           |
| User Profile         | /profile                      | My Profile          | profile-page                |

---

### 2.1 Dashboard Page (/dashboard)
- **Elements and IDs:**
  - `dashboard-page` (div): Container for entire dashboard page.
  - `welcome-message` (h1): Displays "Welcome, {fullname}" where fullname is from `users.txt` based on current username.
  - `enrolled-courses` (div): Displays list or cards of user's enrolled courses with progress summaries.
  - `browse-courses-button` (button): Label "Browse Courses"; navigates to `/courses/catalog`.
  - `my-courses-button` (button): Label "My Courses"; navigates to `/courses/mine`.

- **Data Handling:**
  - Reads `enrollments.txt` filtered by username.
  - Reads `courses.txt` for course titles and details.
  - If no enrollments, display message "You have not enrolled in any courses yet."

- **Navigation:**
  - `browse-courses-button` -> Course Catalog `/courses/catalog`
  - `my-courses-button` -> My Courses `/courses/mine`


### 2.2 Course Catalog Page (/courses/catalog)
- **Elements and IDs:**
  - `catalog-page` (div): Container for catalog.
  - `search-input` (input text): Search field for filtering courses by title or category.
  - `course-grid` (div): Grid displaying course cards.
  - `view-course-button-{course_id}` (button): Button to view course details for each course.
  - `back-to-dashboard` (button): Navigates back to `/dashboard`.

- **Data Handling:**
  - Reads `courses.txt` filtering to include only courses with status `Active`.
  - Dynamically filters based on `search-input` content.

- **Navigation:**
  - Clicking `view-course-button-{course_id}` -> Course Details `/courses/details/{course_id}`
  - Clicking `back-to-dashboard` -> Dashboard `/dashboard`


### 2.3 Course Details Page (/courses/details/{course_id})
- **Elements and IDs:**
  - `course-details-page` (div): Container for course details.
  - `course-title` (h1): Shows course title.
  - `course-description` (div): Full course description.
  - `enroll-button` (button): Label "Enroll Now" if not enrolled; "Already Enrolled" and disabled if enrolled.
  - `back-to-catalog` (button): Navigates back to `/courses/catalog`.

- **Data Handling and Functionality:**
  - Reads course data by `course_id` from `courses.txt`.
  - Checks enrollment status from `enrollments.txt`.
  - On enroll button click when not enrolled:
    - Generates unique `enrollment_id` (max+1).
    - Appends to `enrollments.txt`: `enrollment_id|username|course_id|current_date|0|In Progress`.
    - Updates button to disabled state with text "Already Enrolled".

- **Navigation:**
  - `back-to-catalog` -> `/courses/catalog`


### 2.4 My Courses Page (/courses/mine)
- **Elements and IDs:**
  - `my-courses-page` (div): Container for My Courses page.
  - `courses-list` (div): Lists enrolled courses with progress bars and status.
  - `continue-learning-button-{course_id}` (button): For each enrolled course, navigates to learning page.
  - `back-to-dashboard` (button): Returns to dashboard.

- **Data Handling:**
  - Reads `enrollments.txt` filtered for current user.
  - Reads `courses.txt` for course metadata.
  - If no enrolled courses, display message "No enrolled courses found."

- **Navigation:**
  - `continue-learning-button-{course_id}` -> Course Learning `/courses/learn/{course_id}`
  - `back-to-dashboard` -> `/dashboard`


### 2.5 Course Learning Page (/courses/learn/{course_id})
- **Elements and IDs:**
  - `learning-page` (div): Container for learning page.
  - `lessons-list` (div): Displays sequenced lessons with completion indicators.
  - `lesson-content` (div): Shows content for current lesson.
  - `mark-complete-button` (button): Marks current lesson as completed.
  - `back-to-my-courses` (button): Returns to `/courses/mine`.

- **Data Handling and Functionality:**
  - Lessons assumed ordered; details possibly part of extended course syllabus data.
  - Load lessons list; show first incomplete lesson if any, else last completed.
  - Progress = (completed lessons / total lessons) * 100.
  - On marking complete:
    - Update enrollment progress in `enrollments.txt`.
    - Enforce sequential completion only; button disabled if lesson not next in order.
    - When progress reaches 100%, update enrollment status to "Completed".
    - Append certificate entry to `certificates.txt` if not already exists:
      `certificate_id|username|course_id|current_date`.

- **Navigation:**
  - `back-to-my-courses` -> `/courses/mine`


### 2.6 My Assignments Page (/assignments)
- **Elements and IDs:**
  - `assignments-page` (div): Container.
  - `assignments-table` (table): Columns: assignment ID, title, due date, status, grade.
  - `submit-assignment-button-{assignment_id}` (button): Enabled if assignment pending submission.
  - `back-to-dashboard` (button): Returns to `/dashboard`.

- **Data Handling:**
  - Reads `assignments.txt` filtered for courses user enrolled in.
  - Reads `submissions.txt` filtered by username to check submission status.
  - Status: "Pending" if no submission, "Submitted" if submitted.

- **Navigation:**
  - Clicking `submit-assignment-button-{assignment_id}` -> Submit Assignment `/assignments/submit/{assignment_id}`
  - `back-to-dashboard` -> `/dashboard`


### 2.7 Submit Assignment Page (/assignments/submit/{assignment_id})
- **Elements and IDs:**
  - `submit-page` (div): Container.
  - `assignment-info` (div): Displays assignment title and description.
  - `submission-text` (textarea): Text area for assignment response.
  - `submit-button` (button): Submits the assignment.
  - `back-to-assignments` (button): Returns to `/assignments`.

- **Data Handling:**
  - Reads `assignments.txt` by `assignment_id`.
  - On submit:
    - Generate unique `submission_id` (max+1).
    - Append to `submissions.txt`:
      `submission_id|assignment_id|username|submission_text|current_date|null|""`

- **Interaction:**
  - Displays confirmation upon success.
  - `back-to-assignments` returns to My Assignments.


### 2.8 Certificates Page (/certificates)
- **Elements and IDs:**
  - `certificates-page` (div): Container.
  - `certificates-grid` (div): Displays earned certificates as cards with course title and issue date.
  - `back-to-dashboard` (button): Returns to dashboard.

- **Data Handling:**
  - Reads `certificates.txt` filtered by username.
  - Cross-reference `courses.txt` for course titles.
  - Only certificates for courses with enrollment status "Completed" appear.

- **Navigation:**
  - `back-to-dashboard` -> `/dashboard`


### 2.9 User Profile Page (/profile)
- **Elements and IDs:**
  - `profile-page` (div): Container.
  - `profile-email` (input text): Editable email field.
  - `profile-fullname` (input text): Editable full name field.
  - `update-profile-button` (button): Saves profile changes.
  - `back-to-dashboard` (button): Returns to dashboard.

- **Data Handling and Functionality:**
  - Reads user data from `users.txt` by username.
  - On update:
    - Modify line for current username preserving uniqueness.
    - Save updated email and fullname.
    - Display confirmation to user.

- **Navigation:**
  - `back-to-dashboard` -> `/dashboard`

---

## 3. Navigation Flow Summary

- The app always starts at `/dashboard` after login.
- Navigation paths:
  - Dashboard:
    - To Course Catalog `/courses/catalog`
    - To My Courses `/courses/mine`
    - To My Assignments `/assignments`
    - To Certificates `/certificates`
    - To Profile `/profile`
  - Course Catalog:
    - To Course Details `/courses/details/{course_id}`
    - Back to Dashboard
  - Course Details:
    - Enroll and stay (button disabled)
    - Back to Catalog
  - My Courses:
    - Continue Learning `/courses/learn/{course_id}`
    - Back to Dashboard
  - Course Learning:
    - Mark lesson complete (updates progress and certificates)
    - Back to My Courses
  - My Assignments:
    - Submit Assignment `/assignments/submit/{assignment_id}`
    - Back to Dashboard
  - Submit Assignment:
    - Submit text assignment
    - Back to My Assignments
  - Certificates:
    - Back to Dashboard
  - Profile:
    - Save changes
    - Back to Dashboard

All back buttons maintain consistent navigation patterns.

---

## 4. Data Files and Data Management

| File Name       | Usage                                         | Format Description                                                   |
|-----------------|-----------------------------------------------|---------------------------------------------------------------------|
| `users.txt`     | User info (username, email, fullname)        | `username|email|fullname`                                           |
| `courses.txt`   | Course metadata                               | `course_id|title|description|category|level|duration|status`        |
| `enrollments.txt`| User enrollments and progress tracking       | `enrollment_id|username|course_id|enrollment_date|progress|status` |
| `assignments.txt`| Assignments associated with courses           | `assignment_id|course_id|title|description|due_date|max_points`    |
| `submissions.txt`| Assignment submissions with statuses          | `submission_id|assignment_id|username|submission_text|submit_date|grade|feedback` |
| `certificates.txt`| Certificates issued on course completion      | `certificate_id|username|course_id|issue_date`                     |

- All files located in `data/` directory.
- Reads load full content; filters applied as needed.
- Writes are atomic: update full file or append with ID increments.

---

## 5. Dynamic IDs Patterns
- `view-course-button-{course_id}`: Button on catalog page.
- `continue-learning-button-{course_id}`: Button on My Courses page.
- `submit-assignment-button-{assignment_id}`: Button on assignments page.

---

## 6. Functional and Behavioral Constraints

- Enroll button disables and shows "Already Enrolled" if user is enrolled in the course.
- Lessons in courses must be completed sequentially, no skipping ahead.
- Progress is updated only when a lesson is marked complete.
- At 100% progress, enrollment status updates to "Completed" and certificate is generated if none exists.
- Assignment submissions record submission dates and maintain grades/feedback.
- User profile updates only affect email and fullname; username remains unchanged.

---

This merged design specification fully integrates and refines the details from both candidate designs, ensuring full alignment with the user requirements and providing a definitive implementation reference.
