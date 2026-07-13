# Frontend Design for OnlineCourse Web Application

## Section 1: HTML Template Structure

### 1. Dashboard Page
- **Template Filename**: dashboard.html
- **Page Title**: Learning Dashboard
- **Element IDs and Types:**
  - dashboard-page (Div): Container for the dashboard page
  - welcome-message (H1): Displays user welcome message with user's name
  - enrolled-courses (Div): Displays list or grid of currently enrolled courses
  - browse-courses-button (Button): Navigates to Course Catalog page
  - my-courses-button (Button): Navigates to My Courses page

### 2. Course Catalog Page
- **Template Filename**: catalog.html
- **Page Title**: Available Courses
- **Element IDs and Types:**
  - catalog-page (Div): Container for the catalog page
  - search-input (Input): Text input for searching/filtering courses
  - course-grid (Div): Grid or list container displaying multiple course cards
  - view-course-button-{course_id} (Button): Repeated button for each course to view details
  - back-to-dashboard (Button): Button to navigate back to Dashboard

### 3. Course Details Page
- **Template Filename**: course_details.html
- **Page Title**: Course Details
- **Element IDs and Types:**
  - course-details-page (Div): Container for the course details page
  - course-title (H1): Displays the title of the course
  - course-description (Div): Displays detailed description of the course
  - enroll-button (Button): Button to enroll in the course or disabled if already enrolled
  - back-to-catalog (Button): Button to return to Course Catalog

### 4. My Courses Page
- **Template Filename**: my_courses.html
- **Page Title**: My Courses
- **Element IDs and Types:**
  - my-courses-page (Div): Container for the My Courses page
  - courses-list (Div): List or grid displaying enrolled courses along with progress
  - continue-learning-button-{course_id} (Button): Repeated button for each enrolled course to continue learning
  - back-to-dashboard (Button): Navigate back to Dashboard

### 5. Course Learning Page
- **Template Filename**: course_learning.html
- **Page Title**: Course Learning
- **Element IDs and Types:**
  - learning-page (Div): Container for the course learning page
  - lessons-list (Div): List of lessons in the course
  - lesson-content (Div): Displays contents/materials of the current lesson
  - mark-complete-button (Button): Button to mark the current lesson as completed
  - back-to-my-courses (Button): Navigate back to My Courses page

### 6. My Assignments Page
- **Template Filename**: my_assignments.html
- **Page Title**: My Assignments
- **Element IDs and Types:**
  - assignments-page (Div): Container for assignments page
  - assignments-table (Table): Displays all assignments relevant to the user
  - submit-assignment-button-{assignment_id} (Button): Repeated button per assignment to submit work
  - back-to-dashboard (Button): Navigate back to Dashboard

### 7. Submit Assignment Page
- **Template Filename**: submit_assignment.html
- **Page Title**: Submit Assignment
- **Element IDs and Types:**
  - submit-page (Div): Container for the assignment submission page
  - assignment-info (Div): Displays assignment title and description
  - submission-text (Textarea): Textarea for user to input assignment response
  - submit-button (Button): Submit the assignment
  - back-to-assignments (Button): Navigate back to My Assignments page

### 8. Certificates Page
- **Template Filename**: certificates.html
- **Page Title**: My Certificates
- **Element IDs and Types:**
  - certificates-page (Div): Container for certificates page
  - certificates-grid (Div): Grid display of earned certificates
  - back-to-dashboard (Button): Navigate back to Dashboard

### 9. User Profile Page
- **Template Filename**: profile.html
- **Page Title**: My Profile
- **Element IDs and Types:**
  - profile-page (Div): Container for user profile page
  - profile-email (Input): Email input for user profile
  - profile-fullname (Input): Full name input for user profile
  - update-profile-button (Button): Button to save profile updates
  - back-to-dashboard (Button): Navigate back to Dashboard


## Section 2: Navigation and UI Behavior

### Navigation Flow
- From **Dashboard Page**:
  - browse-courses-button -> Course Catalog Page
  - my-courses-button -> My Courses Page

- From **Course Catalog Page**:
  - view-course-button-{course_id} -> Course Details Page for selected course
  - back-to-dashboard -> Dashboard Page

- From **Course Details Page**:
  - enroll-button -> Enrolls user (if not already enrolled), updates UI to "Already Enrolled" disabled
  - back-to-catalog -> Course Catalog Page

- From **My Courses Page**:
  - continue-learning-button-{course_id} -> Course Learning Page for selected course
  - back-to-dashboard -> Dashboard Page

- From **Course Learning Page**:
  - mark-complete-button -> Updates progress; if course complete, certificate generated
  - back-to-my-courses -> My Courses Page

- From **My Assignments Page**:
  - submit-assignment-button-{assignment_id} -> Submit Assignment Page for selected assignment
  - back-to-dashboard -> Dashboard Page

- From **Submit Assignment Page**:
  - submit-button -> Submits the assignment; shows confirmation message
  - back-to-assignments -> My Assignments Page

- From **Certificates Page**:
  - back-to-dashboard -> Dashboard Page

- From **User Profile Page**:
  - update-profile-button -> Saves profile changes
  - back-to-dashboard -> Dashboard Page


### UI Behavior Details
- **Enroll Button on Course Details Page**:
  - If user is not enrolled: shows "Enroll" enabled
  - If user already enrolled: button text becomes "Already Enrolled" and is disabled

- **Mark Complete Button on Course Learning Page**:
  - Disabled if current lesson is already completed
  - Enabled only if previous lessons are completed (sequential completion enforced)

- **Submit Assignment Button(s)**:
  - Shown for assignments pending submission

- **Dynamic Content Placeholders**:
  - User name displayed in welcome-message on Dashboard Page
  - Enrolled courses data displayed in enrolled-courses (Dashboard) and courses-list (My Courses) with progress info
  - Course details (title, description) displayed in course-title and course-description
  - Lessons list and content displayed in lessons-list and lesson-content
  - Assignments listed in assignments-table with submit button per assignment where needed
  - Certificates displayed in certificates-grid with certificate details
  - Profile fields populated in profile-email and profile-fullname inputs


# End of frontend_design.md
