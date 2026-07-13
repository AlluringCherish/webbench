# Design Specification Document for OnlineCourse Python Web Application

---

## Section 1: UI Pages and Element IDs

### 1. Dashboard Page
- **Page Title**: Learning Dashboard
- **Purpose**: Main hub displaying enrolled courses and progress summarization.
- **Elements:**
  - `dashboard-page` (Div) - Container for the entire dashboard page.
  - `welcome-message` (H1) - Displays a personalized welcome message with the user's name.
  - `enrolled-courses` (Div) - Displays currently enrolled courses list or cards with progress bars.
  - `browse-courses-button` (Button) - Navigates user to Course Catalog page.
  - `my-courses-button` (Button) - Navigates user to My Courses page.
  - `my-assignments-button` (Button) - Navigates user to My Assignments page.
  - `certificates-button` (Button) - Navigates user to Certificates page.
  - `profile-button` (Button) - Navigates user to User Profile page.

### 2. Course Catalog Page
- **Page Title**: Available Courses
- **Purpose**: Allows browsing/searching all available courses.
- **Elements:**
  - `catalog-page` (Div) - Container for the catalog page.
  - `search-input` (Input) - Text input field for course searching/filtering.
  - `course-grid` (Div) - Grid container displaying multiple course cards.
  - `view-course-button-{course_id}` (Button) - Button for each course card to view detailed course info; dynamic with course_id.
  - `back-to-dashboard` (Button) - Returns user back to Dashboard page.

### 3. Course Details Page
- **Page Title**: Course Details
- **Purpose**: Display detailed info about a single course, syllabus, enrollment options.
- **Elements:**
  - `course-details-page` (Div) - Container for the details page.
  - `course-title` (H1) - Course title display.
  - `course-description` (Div) - Detailed text about the course contents.
  - `enroll-button` (Button) - Enroll in the course, disables and changes text if already enrolled.
  - `back-to-catalog` (Button) - Navigates back to the course catalog.

### 4. My Courses Page
- **Page Title**: My Courses
- **Purpose**: Show all courses the user is enrolled in with progress info.
- **Elements:**
  - `my-courses-page` (Div) - Container for My Courses page.
  - `courses-list` (Div) - Lists enrolled courses with progress bars or percentage.
  - `continue-learning-button-{course_id}` (Button) - Button for each enrolled course to continue learning; dynamic with course_id.
  - `back-to-dashboard` (Button) - Navigates back to Dashboard.

### 5. Course Learning Page
- **Page Title**: Course Learning
- **Purpose**: Display course lessons, content, and allow marking lessons complete.
- **Elements:**
  - `learning-page` (Div) - Container for the learning content page.
  - `lessons-list` (Div) - List all lessons for the current course.
  - `lesson-content` (Div) - Show current lesson materials.
  - `mark-complete-button` (Button) - Button to mark current lesson as completed.
  - `back-to-my-courses` (Button) - Navigate back to My Courses page.

### 6. My Assignments Page
- **Page Title**: My Assignments
- **Purpose**: Display assignments available and submitted by the user.
- **Elements:**
  - `assignments-page` (Div) - Container for assignments page.
  - `assignments-table` (Table) - Table listing all assignments relevant to user.
  - `submit-assignment-button-{assignment_id}` (Button) - Submit assignment button per assignment; dynamic with assignment_id.
  - `back-to-dashboard` (Button) - Navigate back to Dashboard.

### 7. Submit Assignment Page
- **Page Title**: Submit Assignment
- **Purpose**: Interface for entering and submitting assignment text response.
- **Elements:**
  - `submit-page` (Div) - Container for submission page.
  - `assignment-info` (Div) - Displays assignment title and description.
  - `submission-text` (Textarea) - Input area for user text submission.
  - `submit-button` (Button) - Submits the assignment.
  - `back-to-assignments` (Button) - Returns to assignments page.

### 8. Certificates Page
- **Page Title**: My Certificates
- **Purpose**: Display user-earned certificates.
- **Elements:**
  - `certificates-page` (Div) - Container for certificates page.
  - `certificates-grid` (Div) - Grid showing certificates cards.
  - `back-to-dashboard` (Button) - Returns to Dashboard.

### 9. User Profile Page
- **Page Title**: My Profile
- **Purpose**: View and edit user profile information.
- **Elements:**
  - `profile-page` (Div) - Container for profile page.
  - `profile-email` (Input) - Email editing input.
  - `profile-fullname` (Input) - Full name editing input.
  - `update-profile-button` (Button) - Saves profile changes.
  - `back-to-dashboard` (Button) - Returns to Dashboard.

---

## Navigation Flows
- Dashboard acts as the home starting page.
- From Dashboard user can go to Course Catalog, My Courses, My Assignments, Certificates, or Profile.
- Course Catalog allows viewing details or returning to dashboard.
- Course Details allows enrollment and navigation back to catalog.
- My Courses allows continuing learning which opens Course Learning page.
- Course Learning allows marking lessons complete and returning to My Courses.
- My Assignments allows submitting assignments which lead to Submit Assignment page.
- Certificates and Profile both link back to Dashboard.

---

## Section 2: Data Storage Formats

All data files reside in local `data/` directory. Each file is a UTF-8 encoded text file using `|` as the delimiter.

### 1. users.txt
- Format: `username|email|fullname`
- Example:
  ```
  john|john@student.com|John Student
  alice|alice@instructor.com|Alice Professor
  jane|jane@student.com|Jane Learner
  ```

### 2. courses.txt
- Format: `course_id|title|description|category|level|duration|status`
- Example:
  ```
  1|Python Programming|Learn Python from scratch|Programming|Beginner|40 hours|Active
  2|Web Development|Build modern websites|Web|Intermediate|60 hours|Active
  3|Data Science|Introduction to data analysis|Data|Advanced|80 hours|Active
  ```

### 3. enrollments.txt
- Format: `enrollment_id|username|course_id|enrollment_date|progress|status`
- Fields:
  - `enrollment_id`: unique numeric ID
  - `username`: enrolled user
  - `course_id`: course identifier
  - `enrollment_date`: ISO date string `YYYY-MM-DD`
  - `progress`: integer percent (0-100)
  - `status`: String, either "In Progress" or "Completed"
- Example:
  ```
  1|john|1|2024-11-01|75|In Progress
  2|jane|1|2024-10-15|100|Completed
  3|john|2|2024-11-10|25|In Progress
  ```

### 4. assignments.txt
- Format: `assignment_id|course_id|title|description|due_date|max_points`
- Fields:
  - `assignment_id`: unique numeric
  - `course_id`: numeric course
  - `title`: string
  - `description`: string
  - `due_date`: ISO date `YYYY-MM-DD`
  - `max_points`: integer
- Example:
  ```
  1|1|Python Basics Quiz|Complete the quiz on variables and data types|2024-12-01|100
  2|1|Final Project|Build a calculator application|2024-12-15|200
  ```

### 5. submissions.txt
- Format: `submission_id|assignment_id|username|submission_text|submit_date|grade|feedback`
- Fields:
  - `submission_id`: unique numeric
  - `assignment_id`: numeric
  - `username`: string
  - `submission_text`: string
  - `submit_date`: ISO date
  - `grade`: integer or empty if not graded
  - `feedback`: string or empty
- Example:
  ```
  1|1|john|My answers are...|2024-11-25|85|Good work!
  2|2|jane|Here is my project...|2024-11-20|95|Excellent!
  ```

### 6. certificates.txt
- Format: `certificate_id|username|course_id|issue_date`
- Fields:
  - `certificate_id`: unique numeric
  - `username`: string
  - `course_id`: numeric
  - `issue_date`: ISO date
- Example:
  ```
  1|jane|1|2024-11-22
  ```

---

## Section 3: Functional Workflows

### Enrollment Workflow
- User sees Course Details page.
- If not enrolled, "Enroll" button is enabled.
- User clicks "Enroll", entry added to `enrollments.txt`:
  - Unique enrollment_id assigned
  - Username and course_id recorded
  - Enrollment date set to current date
  - Progress initialized to 0
  - Status set to "In Progress"
- Button text changes to "Already Enrolled" and disables.

### Course Progress Tracking
- On Course Learning page, lessons are listed.
- User must complete lessons in order.
- Clicking "Mark Complete" updates lesson completion state.
- Progress recalculated as (completed lessons / total lessons) * 100.
- Progress updated in `enrollments.txt` for the user and course.
- When progress reaches 100%, status becomes "Completed".
- Certificate is automatically generated with:
  - New certificate_id
  - Username and course_id
  - Issue date of completion
- Certificate saved to `certificates.txt`.

### Assignment Submission
- User accesses My Assignments page to view pending/graded assignments.
- Clicking "Submit" for an assignment opens Submit Assignment page.
- User enters text and submits.
- Submission entry created in `submissions.txt`:
  - Unique submission_id
  - Assignment and user details
  - Submission text
  - Submission date as current date
  - Grade and feedback initially empty
- Confirmation message is displayed post-submission.

### Navigation and Button State Logic
- Buttons for navigation have consistent IDs and return user to intended pages.
- Enroll button changes state based on enrollment status.
- Continue Learning buttons only show on enrolled courses.
- Submit buttons only show for assignments that are pending submission.

### Certificate Display
- Certificates page lists only completed courses.
- Each certificate card represents a course certificate.

### Profile Update
- User can update email and fullname.
- Clicking "Update Profile" saves changes back to `users.txt` after validation.

---

This design spec covers all user interface elements, data file formats, and workflows required for the 'OnlineCourse' Python web application.
