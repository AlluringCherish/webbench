# Design Specification for 'OnlineCourse' Python Web Application

---

## Section 1: UI Pages and Element IDs

### 1. Dashboard Page
- **Page Title**: Learning Dashboard
- **Purpose**: Main hub displaying the user's enrolled courses and progress.
- **Elements**:
  - `dashboard-page` (Div): Container for the dashboard page.
  - `welcome-message` (H1): Welcome message displaying the user's name.
  - `enrolled-courses` (Div): Display area for enrolled courses overview.
  - `browse-courses-button` (Button): Navigates to Course Catalog page.
  - `my-courses-button` (Button): Navigates to My Courses page.
  - `my-assignments-button` (Button): Navigates to My Assignments page.
  - `my-certificates-button` (Button): Navigates to My Certificates page.

### 2. Course Catalog Page
- **Page Title**: Available Courses
- **Purpose**: Allows users to browse all available courses.
- **Elements**:
  - `catalog-page` (Div): Container for course catalog page.
  - `search-input` (Input): Search field to filter courses.
  - `course-grid` (Div): Grid layout for course cards.
  - Dynamic repeated elements: `view-course-button-{course_id}` (Button): View details for specific course.
  - `back-to-dashboard` (Button): Navigates back to Dashboard.

### 3. Course Details Page
- **Page Title**: Course Details
- **Purpose**: Show detailed info of selected course with enrollment option.
- **Elements**:
  - `course-details-page` (Div): Container.
  - `course-title` (H1): Shows course name/title.
  - `course-description` (Div): Full course description.
  - `enroll-button` (Button): Enroll in course.
  - `back-to-catalog` (Button): Back to Course Catalog.
- **Functionality**:
  - Enroll button creates an enrollment entry with 0% progress.
  - If already enrolled, button changes to "Already Enrolled" and disables.
  - Enrollment date is recorded as current date.

### 4. My Courses Page
- **Page Title**: My Courses
- **Purpose**: Shows a list of user's enrolled courses and progress.
- **Elements**:
  - `my-courses-page` (Div): Container.
  - `courses-list` (Div): List of enrolled courses with progress.
  - Dynamic repeated buttons: `continue-learning-button-{course_id}` (Button): Continue learning specific course.
  - `back-to-dashboard` (Button): Back to Dashboard.

### 5. Course Learning Page
- **Page Title**: Course Learning
- **Purpose**: View course content, lessons, and track progress.
- **Elements**:
  - `learning-page` (Div): Container.
  - `lessons-list` (Div): List of lessons.
  - `lesson-content` (Div): Show current lesson materials.
  - `mark-complete-button` (Button): Mark current lesson complete.
  - `back-to-my-courses` (Button): Back to My Courses.
- **Functionality**:
  - Progress calculated as (completed lessons / total lessons) * 100.
  - Marking complete updates progress in `enrollments.txt`.
  - Lessons must be completed sequentially.
  - Reaching 100% progress auto-generates certificate.

### 6. My Assignments Page
- **Page Title**: My Assignments
- **Purpose**: View and submit assignments.
- **Elements**:
  - `assignments-page` (Div): Container.
  - `assignments-table` (Table): Displays assignment list.
  - Dynamic repeated buttons: `submit-assignment-button-{assignment_id}` (Button): Submit pending assignment.
  - `back-to-dashboard` (Button): Back to Dashboard.

### 7. Submit Assignment Page
- **Page Title**: Submit Assignment
- **Purpose**: Submission of assignment work with textual input.
- **Elements**:
  - `submit-page` (Div): Container.
  - `assignment-info` (Div): Shows assignment title and description.
  - `submission-text` (Textarea): Input field for submission.
  - `submit-button` (Button): Submit assignment.
  - `back-to-assignments` (Button): Back to My Assignments.
- **Functionality**:
  - Submission writes entry into `submissions.txt` with status "Submitted".
  - Submit date recorded for late submission check.
  - Shows confirmation message upon success.

### 8. Certificates Page
- **Page Title**: My Certificates
- **Purpose**: View earned course completion certificates.
- **Elements**:
  - `certificates-page` (Div): Container.
  - `certificates-grid` (Div): Grid display of certificate cards.
  - `back-to-dashboard` (Button): Back to Dashboard.
- **Functionality**:
  - Certificates auto-generated when course progress reaches 100%.
  - Certificate entry added to `certificates.txt` with current issue date.
  - Only completed courses shown.

### 9. User Profile Page
- **Page Title**: My Profile
- **Purpose**: View and edit user profile details.
- **Elements**:
  - `profile-page` (Div): Container.
  - `profile-email` (Input): Email address field.
  - `profile-fullname` (Input): Full name field.
  - `update-profile-button` (Button): Save profile changes.
  - `back-to-dashboard` (Button): Back to Dashboard.

---

## Section 2: Data Storage Formats

All data files are stored in the `data/` directory, encoded in UTF-8, and fields separated by pipe `|` symbol.

### 1. Users Data: `users.txt`
- Format: `username|email|fullname`
- Example:
  ```
  john|john@student.com|John Student
  alice|alice@instructor.com|Alice Professor
  jane|jane@student.com|Jane Learner
  ```

### 2. Courses Data: `courses.txt`
- Format: `course_id|title|description|category|level|duration|status`
- Example:
  ```
  1|Python Programming|Learn Python from scratch|Programming|Beginner|40 hours|Active
  2|Web Development|Build modern websites|Web|Intermediate|60 hours|Active
  3|Data Science|Introduction to data analysis|Data|Advanced|80 hours|Active
  ```

### 3. Enrollments Data: `enrollments.txt`
- Format: `enrollment_id|username|course_id|enrollment_date|progress|status`
- Example:
  ```
  1|john|1|2024-11-01|75|In Progress
  2|jane|1|2024-10-15|100|Completed
  3|john|2|2024-11-10|25|In Progress
  ```

### 4. Assignments Data: `assignments.txt`
- Format: `assignment_id|course_id|title|description|due_date|max_points`
- Example:
  ```
  1|1|Python Basics Quiz|Complete the quiz on variables and data types|2024-12-01|100
  2|1|Final Project|Build a calculator application|2024-12-15|200
  ```

### 5. Submissions Data: `submissions.txt`
- Format: `submission_id|assignment_id|username|submission_text|submit_date|grade|feedback`
- Example:
  ```
  1|1|john|My answers are...|2024-11-25|85|Good work!
  2|2|jane|Here is my project...|2024-11-20|95|Excellent!
  ```

### 6. Certificates Data: `certificates.txt`
- Format: `certificate_id|username|course_id|issue_date`
- Example:
  ```
  1|jane|1|2024-11-22
  ```

---

## Section 3: Functional Workflows

### Enrollment Workflow
- User browses courses on the Course Catalog Page.
- When clicking "Enroll", system checks if user already enrolled:
  - If not enrolled:
    - Adds an entry to `enrollments.txt` with progress 0, status "In Progress", and current date.
    - Updates button to "Already Enrolled" and disables it.

### Course Learning Workflow
- User selects a course from My Courses and navigates to Course Learning Page.
- Lessons listed, user views lesson content.
- User must complete lessons in order:
  - Before marking a lesson complete, the prior lesson must be completed.
- When clicking "Mark Complete":
  - The system updates progress as ratio of completed lessons to total lessons.
  - Updates `enrollments.txt` progress field.
  - Once progress reaches 100%:
    - Marks enrollment status as "Completed".
    - Generates a certificate entry in `certificates.txt` with issue date.

### Assignment Submission Workflow
- User views My Assignments page for pending or completed assignments.
- Clicking "Submit" navigates to Submit Assignment Page.
- User inputs text and submits.
- On submission:
  - New record is saved to `submissions.txt` with status "Submitted" and current date.
  - Confirmation shown to user.

### Progress Tracking and Certificates
- Progress displayed as a percentage on My Courses and Dashboard.
- Certificates only appear in Certificates Page for completed courses.
- Certificates auto-generate on 100% progress completion.

### Navigation Flow
- Dashboard is the start page.
- From Dashboard:
  - Browse Courses 127 Course Catalog Page
  - My Courses 127 My Courses Page
  - My Assignments 127 My Assignments Page
  - My Certificates 127 Certificates Page
  - My Profile 127 Profile Page
- Course Catalog 127 Course Details or back to Dashboard
- Course Details 127 back to Catalog or enroll
- My Courses 127 Course Learning or back to Dashboard
- Course Learning 127 back to My Courses
- My Assignments 127 Submit Assignment or back to Dashboard
- Submit Assignment 127 back to My Assignments
- Certificates 127 back to Dashboard
- Profile 127 back to Dashboard

---

This completes the comprehensive design specification for the 'OnlineCourse' Python web application, fulfilling all the required features, UI design, data storage formats, and workflows as per user requirements.
