# Requirements Analysis for OnlineCourse Web Application

---

## 1. Pages and UI Elements

### 1. Dashboard Page
- **Page Title**: Learning Dashboard
- **Elements:**
  - `dashboard-page` (Div) - Container for the dashboard content.
  - `welcome-message` (H1) - Displays user's welcome message including their name.
  - `enrolled-courses` (Div) - Shows list or summary of user's enrolled courses.
  - `browse-courses-button` (Button) - Navigates user to Course Catalog Page.
  - `my-courses-button` (Button) - Navigates user to My Courses Page.

---

### 2. Course Catalog Page
- **Page Title**: Available Courses
- **Elements:**
  - `catalog-page` (Div) - Container for the catalog.
  - `search-input` (Input) - Text field for searching courses (filter functionality expected).
  - `course-grid` (Div) - Displays course cards.
  - `view-course-button-{course_id}` (Button) [Repeated] - Button on each course card to view course details.
  - `back-to-dashboard` (Button) - Navigates back to Dashboard Page.

---

### 3. Course Details Page
- **Page Title**: Course Details
- **Elements:**
  - `course-details-page` (Div) - Container for course detail content.
  - `course-title` (H1) - Displays course title.
  - `course-description` (Div) - Full course description.
  - `enroll-button` (Button) - Enroll into course or shows "Already Enrolled" and disabled if enrolled.
  - `back-to-catalog` (Button) - Navigates back to Course Catalog Page.

---

### 4. My Courses Page
- **Page Title**: My Courses
- **Elements:**
  - `my-courses-page` (Div) - Container.
  - `courses-list` (Div) - List of enrolled courses with progress.
  - `continue-learning-button-{course_id}` (Button) [Repeated] - Button to continue course learning.
  - `back-to-dashboard` (Button) - Navigates back to Dashboard Page.

---

### 5. Course Learning Page
- **Page Title**: Course Learning
- **Elements:**
  - `learning-page` (Div) - Container for course learning.
  - `lessons-list` (Div) - Lists lessons.
  - `lesson-content` (Div) - Shows current lesson material.
  - `mark-complete-button` (Button) - Marks current lesson completed.
  - `back-to-my-courses` (Button) - Navigates back to My Courses Page.

---

### 6. My Assignments Page
- **Page Title**: My Assignments
- **Elements:**
  - `assignments-page` (Div) - Container.
  - `assignments-table` (Table) - Shows assignments.
  - `submit-assignment-button-{assignment_id}` (Button) [Repeated] - Button for submitting assignment.
  - `back-to-dashboard` (Button) - Back to Dashboard.

---

### 7. Submit Assignment Page
- **Page Title**: Submit Assignment
- **Elements:**
  - `submit-page` (Div) - Container.
  - `assignment-info` (Div) - Shows assignment title and description.
  - `submission-text` (Textarea) - Input area for assignment submission text.
  - `submit-button` (Button) - Submits the assignment.
  - `back-to-assignments` (Button) - Back to My Assignments Page.

---

### 8. Certificates Page
- **Page Title**: My Certificates
- **Elements:**
  - `certificates-page` (Div) - Container.
  - `certificates-grid` (Div) - Displays certificates.
  - `back-to-dashboard` (Button) - Back to Dashboard.

---

### 9. User Profile Page
- **Page Title**: My Profile
- **Elements:**
  - `profile-page` (Div) - Container.
  - `profile-email` (Input) - Email field.
  - `profile-fullname` (Input) - Full name field.
  - `update-profile-button` (Button) - Save profile changes.
  - `back-to-dashboard` (Button) - Back to Dashboard.


---

## 2. Navigation Flow

| From Page           | UI Element ID                      | Destination Page        | Notes                          |
|---------------------|----------------------------------|------------------------|--------------------------------|
| Dashboard           | `browse-courses-button`           | Course Catalog          |                                   |
| Dashboard           | `my-courses-button`               | My Courses               |                                   |
| Course Catalog      | `view-course-button-{course_id}`  | Course Details ({course_id})  | Parameterized course view         |
| Course Catalog      | `back-to-dashboard`               | Dashboard                |                                   |
| Course Details      | `enroll-button`                   | Updates enrollments.txt | Enrollment action; no page change|
| Course Details      | `back-to-catalog`                 | Course Catalog            |                                   |
| My Courses          | `continue-learning-button-{course_id}` | Course Learning ({course_id}) | Parameterized continuation         |
| My Courses          | `back-to-dashboard`               | Dashboard                |                                   |
| Course Learning     | `mark-complete-button`            | Updates enrollments.txt | Progress update; certificate issuance |
| Course Learning     | `back-to-my-courses`              | My Courses                |                                   |
| My Assignments      | `submit-assignment-button-{assignment_id}` | Submit Assignment ({assignment_id}) | Parameterized submission start     |
| My Assignments      | `back-to-dashboard`               | Dashboard                |                                   |
| Submit Assignment   | `submit-button`                   | Updates submissions.txt   | Submission save; confirmation      |
| Submit Assignment   | `back-to-assignments`             | My Assignments            |                                   |
| Certificates        | `back-to-dashboard`               | Dashboard                |                                   |
| User Profile        | `update-profile-button`           | Updates users.txt        | Profile information update         |
| User Profile        | `back-to-dashboard`               | Dashboard                |                                   |

---

## 3. Functional Behavior

### Enrollment
- When user clicks `enroll-button` on Course Details Page:
  - Check if enrollment exists in `enrollments.txt` for that user and course.
  - If not enrolled, create new enrollment record:
    - Fields: enrollment_id (unique), username, course_id, enrollment_date (current date), progress=0, status='In Progress'
  - If already enrolled, the button displays "Already Enrolled" and is disabled.

### Course Progress and Completion
- In Course Learning Page:
  - Lessons must be completed sequentially.
  - Clicking `mark-complete-button` marks current lesson completed.
  - Progress is recalculated as `(completed lessons / total lessons) * 100` and saved to `enrollments.txt`.
  - When progress reaches 100%, update status to 'Completed' in enrollments.txt.
  - Automatically generate a certificate entry in `certificates.txt` with:
    - New certificate_id, username, course_id, and current date as issue_date.

### Assignment Submission
- On Submit Assignment Page:
  - Submit button saves a new record in `submissions.txt`:
    - Fields: submission_id (unique), assignment_id, username, submission_text, submit_date (current date), grade (empty initially), feedback (empty initially)
  - Status "Submitted" tracked implicitly by new entry.
  - Display confirmation message on successful submission.

### Profile Update
- On User Profile Page:
  - Clicking `update-profile-button` updates user details in `users.txt`.
  - Fields updated: email and fullname for the logged-in username.

### Certificate Display
- Certificates Page shows certificates only for courses where enrollment progress is 100%.
- Certificates data is loaded from `certificates.txt`.

## 4. Data Schemas

### users.txt
- Fields: `username|email|fullname`
- Example:
  ```
  john|john@student.com|John Student
  alice|alice@instructor.com|Alice Professor
  jane|jane@student.com|Jane Learner
  ```

### courses.txt
- Fields: `course_id|title|description|category|level|duration|status`
- Example:
  ```
  1|Python Programming|Learn Python from scratch|Programming|Beginner|40 hours|Active
  2|Web Development|Build modern websites|Web|Intermediate|60 hours|Active
  3|Data Science|Introduction to data analysis|Data|Advanced|80 hours|Active
  ```

### enrollments.txt
- Fields: `enrollment_id|username|course_id|enrollment_date|progress|status`
- Example:
  ```
  1|john|1|2024-11-01|75|In Progress
  2|jane|1|2024-10-15|100|Completed
  3|john|2|2024-11-10|25|In Progress
  ```

### assignments.txt
- Fields: `assignment_id|course_id|title|description|due_date|max_points`
- Example:
  ```
  1|1|Python Basics Quiz|Complete the quiz on variables and data types|2024-12-01|100
  2|1|Final Project|Build a calculator application|2024-12-15|200
  ```

### submissions.txt
- Fields: `submission_id|assignment_id|username|submission_text|submit_date|grade|feedback`
- Example:
  ```
  1|1|john|My answers are...|2024-11-25|85|Good work!
  2|2|jane|Here is my project...|2024-11-20|95|Excellent!
  ```

### certificates.txt
- Fields: `certificate_id|username|course_id|issue_date`
- Example:
  ```
  1|jane|1|2024-11-22
  ```

---

This document captures all UI elements, navigation flows, functional behaviors, and data file schemas needed to fully implement the OnlineCourse application.