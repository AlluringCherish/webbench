# Backend Design Document for OnlineCourse Web Application

---

## Section 1: Flask Routes Specification

### 1. `/dashboard`
- **Methods:** GET
- **Description:** Loads the Learning Dashboard page.
- **Request Parameters:** Uses session to identify current logged-in user.
- **Response:** JSON containing user's name, list of enrolled courses with progress.
- **Behavior:** Returns data needed to render dashboard including welcome message and enrolled courses.

---

### 2. `/courses/catalog`
- **Methods:** GET
- **Request Parameters:** Optional query parameter `search` for filtering courses by title or category.
- **Response:** JSON list of active courses matching search query.
- **Behavior:** Fetches all active courses from courses.txt. Filters if search present.

---

### 3. `/courses/<int:course_id>`
- **Methods:** GET
- **Request Parameters:** None
- **Response:** JSON with detailed information of the course (title, description, syllabus placeholder).
- **Behavior:** Retrieves course details from courses.txt.

---

### 4. `/courses/<int:course_id>/enroll`
- **Methods:** POST
- **Request Parameters:** Uses session username to create enrollment.
- **Response:** JSON with status (success or error message).
- **Behavior:** 
  - Checks if user already enrolled.
  - If not, creates a new enrollment in enrollments.txt with progress 0, status 'In Progress', and enrollment_date as current date.
  - If already enrolled, returns error "Already enrolled".

---

### 5. `/my-courses`
- **Methods:** GET
- **Request Parameters:** Uses session username.
- **Response:** JSON list of all courses the user is enrolled in, including progress.
- **Behavior:** Reads enrollments.txt filtered by username, fetches course info for each enrolled course.

---

### 6. `/course/<int:course_id>/learning`
- **Methods:** GET
- **Request Parameters:** Uses session username.
- **Response:** JSON object containing lessons list, completed lessons flags, current lesson content.
- **Behavior:** Reads course lessons (assumed stored somewhere or hardcoded), reads progress from enrollments.txt.

---

### 7. `/course/<int:course_id>/learning/mark-complete`
- **Methods:** POST
- **Request Parameters:** Uses session username; body param `lesson_number` (int).
- **Response:** JSON { status: success/error, updated progress percentage }.
- **Behavior:** 
  - Ensures lessons are completed in order.
  - Updates enrollment progress based on completed lessons.
  - If progress reaches 100%, updates status to 'Completed' and triggers certificate creation.

---

### 8. `/assignments`
- **Methods:** GET
- **Request Parameters:** Uses session username.
- **Response:** JSON list of assignments for courses user enrolled in and submission status.
- **Behavior:** Fetches applicable assignments plus submission history from submissions.txt.

---

### 9. `/assignments/<int:assignment_id>/submit`
- **Methods:** POST
- **Request Parameters:** Uses session username; body param `submission_text` (string).
- **Response:** JSON { status: success/error message }.
- **Behavior:** Creates new submission entry in submissions.txt with status "Submitted", current date.

---

### 10. `/certificates`
- **Methods:** GET
- **Request Parameters:** Uses session username.
- **Response:** JSON list of certificates for completed courses.
- **Behavior:** Fetches certificates.txt entries for user.

---

### 11. `/profile`
- **Methods:** GET, POST
  - GET: Returns user profile data.
  - POST: Updates profile fields (email, fullname).
- **Request Parameters:** Uses session username.
- **Response:** JSON { status: success/error } with updated profile data.
- **Behavior:** Reads and updates users.txt.

---

### Session and Authentication Assumptions
- All routes assume a logged-in user with `username` stored in session.
- If not logged in, routes return error or redirect (implementation details out of scope).

---

## Section 2: Data File Schemas

All files are pipe `|` delimited text files, stored under `data/` directory.

### 1. users.txt
- **Fields:**
  1. username (string) - unique user id
  2. email (string) - user email address
  3. fullname (string) - user full name
- **Example:**
```
john|john@student.com|John Student
alice|alice@instructor.com|Alice Professor
jane|jane@student.com|Jane Learner
```

---

### 2. courses.txt
- **Fields:**
  1. course_id (int) - unique course identifier
  2. title (string) - course title
  3. description (string) - full course description
  4. category (string) - course category
  5. level (string) - course difficulty level (Beginner, Intermediate, Advanced)
  6. duration (string) - duration description (e.g., "40 hours")
  7. status (string) - course status (e.g., Active)
- **Example:**
```
1|Python Programming|Learn Python from scratch|Programming|Beginner|40 hours|Active
2|Web Development|Build modern websites|Web|Intermediate|60 hours|Active
3|Data Science|Introduction to data analysis|Data|Advanced|80 hours|Active
```

---

### 3. enrollments.txt
- **Fields:**
  1. enrollment_id (int) - unique enrollment identifier
  2. username (string) - user id
  3. course_id (int) - course id
  4. enrollment_date (date yyyy-mm-dd) - enrollment date
  5. progress (int 0-100) - completion percentage
  6. status (string) - status ("In Progress", "Completed")
- **Example:**
```
1|john|1|2024-11-01|75|In Progress
2|jane|1|2024-10-15|100|Completed
3|john|2|2024-11-10|25|In Progress
```

---

### 4. assignments.txt
- **Fields:**
  1. assignment_id (int) - unique assignment id
  2. course_id (int) - course id
  3. title (string) - assignment title
  4. description (string) - assignment details
  5. due_date (date yyyy-mm-dd) - due date
  6. max_points (int) - maximum points available
- **Example:**
```
1|1|Python Basics Quiz|Complete the quiz on variables and data types|2024-12-01|100
2|1|Final Project|Build a calculator application|2024-12-15|200
```

---

### 5. submissions.txt
- **Fields:**
  1. submission_id (int) - unique submission id
  2. assignment_id (int) - assignment id
  3. username (string) - user id
  4. submission_text (string) - text content of submission
  5. submit_date (date yyyy-mm-dd) - submission date
  6. grade (int or empty) - points awarded
  7. feedback (string or empty) - instructor's feedback
- **Example:**
```
1|1|john|My answers are...|2024-11-25|85|Good work!
2|2|jane|Here is my project...|2024-11-20|95|Excellent!
```

---

### 6. certificates.txt
- **Fields:**
  1. certificate_id (int) - unique certificate id
  2. username (string) - user id
  3. course_id (int) - course id
  4. issue_date (date yyyy-mm-dd) - date of certificate issuance
- **Example:**
```
1|jane|1|2024-11-22
```

---

## Section 3: Business Logic and API Contracts

### Enrollment Logic
- On enrollment:
  - Check enrollments.txt for existing record of the user and course.
  - If none, create new record with unique enrollment_id (incremental), current date as enrollment_date, progress = 0, status = "In Progress".
  - Return success status.
- If already enrolled, respond with error message.

### Progress Update Rules
- Lessons completion must be sequential; only the next uncompleted lesson can be marked complete.
- Progress is calculated as (number of completed lessons / total lessons) * 100.
- On marking a lesson complete:
  - Update enrollments.txt progress field.
  - If progress hits 100%, update status to "Completed".
  - Trigger certificate creation (if not already issued).

### Assignment Submission Flow
- Users see assignments for courses they are enrolled in.
- Submission POST:
  - Validate that assignment belongs to a course the user enrolled in.
  - Append new submission with unique submission_id (incremental), current date as submit_date, grade blank, feedback blank.
  - Status is considered "Submitted".
  - Return success confirmation.

### Certificate Generation
- When enrollment progress reaches 100%, the system:
  - Checks certificates.txt if certificate already exists for this user and course.
  - If not, create new certificate record with unique certificate_id, current date as issue_date.
  - Certificates appear in My Certificates page.

---

**End of backend_design.md**
