# Design Specification for OnlineCourse Web Application

---

## 1. Flask Routes Specification

| Route URL                 | Function Name           | HTTP Method | Template File                         | Context Variables Passed (name : type)                                |
|---------------------------|------------------------|-------------|-------------------------------------|------------------------------------------------------------------------|
| /                         | root_redirect           | GET         | Redirect to /dashboard               | None                                                                   |
| /dashboard                | dashboard              | GET         | dashboard.html                      | username: str, fullname: str, enrolled_courses: list of dict {
  course_id: str,
  title: str,
  progress: int (percentage)
}                                                                        |
| /catalog                  | course_catalog         | GET         | course_catalog.html                 | courses: list of dict {
  course_id: str,
  title: str,
  description: str,
  category: str,
  level: str,
  duration: str,
  status: str
}
|
| /course/<course_id>       | course_details         | GET         | course_details.html                 | course: dict {
  course_id: str,
  title: str,
  description: str,
  category: str,
  level: str,
  duration: str,
  status: str
},
 enrolled: bool
|
| /course/<course_id>/enroll | enroll_course          | POST        | N/A (Redirect or JSON response)    | None (Updates enrollments.txt)                                        |
| /my-courses               | my_courses             | GET         | my_courses.html                    | enrolled_courses: list of dict {
  course_id: str,
  title: str,
  progress: int (percentage),
  status: str
}
|
| /course/<course_id>/learn | course_learning        | GET         | course_learning.html               | course: dict {
  course_id: str,
  title: str,
  lessons: list of dict {
    lesson_id: str,
    title: str,
    content: str,
    completed: bool
  }
},
 current_lesson: dict {
  lesson_id: str,
  title: str,
  content: str
},
 progress: int (percentage)
|
| /course/<course_id>/learn/complete | mark_lesson_complete | POST        | N/A (Redirect or JSON response)    | None (Updates enrollments.txt and certificates.txt as needed)         |
| /assignments              | my_assignments         | GET         | my_assignments.html                | assignments: list of dict {
  assignment_id: str,
  course_id: str,
  title: str,
  description: str,
  due_date: str (YYYY-MM-DD),
  max_points: int
}
|
| /assignment/<assignment_id>/submit | submit_assignment_form | GET         | submit_assignment.html             | assignment: dict {
  assignment_id: str,
  course_id: str,
  title: str,
  description: str,
  due_date: str (YYYY-MM-DD),
  max_points: int
}
|
| /assignment/<assignment_id>/submit | submit_assignment     | POST        | N/A (Redirect or JSON response)    | None (Updates submissions.txt)                                        |
| /certificates            | certificates            | GET         | certificates.html                  | certificates: list of dict {
  certificate_id: str,
  username: str,
  course_id: str,
  issue_date: str (YYYY-MM-DD),
  course_title: str
}
|
| /profile                 | user_profile           | GET         | profile.html                      | user: dict {
  username: str,
  email: str,
  fullname: str
}
|
| /profile/update          | update_profile         | POST        | N/A (Redirect or JSON response)    | None (Updates users.txt)                                              |

---

## 2. Templates and UI Elements

### Templates folder structure
- templates/
  - dashboard.html
  - course_catalog.html
  - course_details.html
  - my_courses.html
  - course_learning.html
  - my_assignments.html
  - submit_assignment.html
  - certificates.html
  - profile.html


---

### 1. dashboard.html
- Elements:
  - Div id="dashboard-page"
  - H1 id="welcome-message" (message includes user's fullname)
  - Div id="enrolled-courses" (displays a list or summary of enrolled courses with progress)
  - Button id="browse-courses-button"
  - Button id="my-courses-button"

- Context variables:
  - username: str
  - fullname: str
  - enrolled_courses: list of dict {
      course_id: str,
      title: str,
      progress: int (0-100)
    }


### 2. course_catalog.html
- Elements:
  - Div id="catalog-page"
  - Input text id="search-input" (for course search filter)
  - Div id="course-grid" (contains course cards)
  - Button(s) id="view-course-button-{course_id}" repeated for each course
  - Button id="back-to-dashboard"

- Context variables:
  - courses: list of dict {
      course_id: str,
      title: str,
      description: str,
      category: str,
      level: str,
      duration: str,
      status: str
    }


### 3. course_details.html
- Elements:
  - Div id="course-details-page"
  - H1 id="course-title"
  - Div id="course-description"
  - Button id="enroll-button" (shows "Enroll" or "Already Enrolled" disabled if enrolled)
  - Button id="back-to-catalog"

- Context variables:
  - course: dict {
      course_id: str,
      title: str,
      description: str,
      category: str,
      level: str,
      duration: str,
      status: str
    }
  - enrolled: bool


### 4. my_courses.html
- Elements:
  - Div id="my-courses-page"
  - Div id="courses-list"
  - Button(s) id="continue-learning-button-{course_id}" repeated for each enrolled course
  - Button id="back-to-dashboard"

- Context variables:
  - enrolled_courses: list of dict {
      course_id: str,
      title: str,
      progress: int (0-100),
      status: str
    }


### 5. course_learning.html
- Elements:
  - Div id="learning-page"
  - Div id="lessons-list" (list of lessons showing completion status)
  - Div id="lesson-content"
  - Button id="mark-complete-button"
  - Button id="back-to-my-courses"

- Context variables:
  - course: dict {
      course_id: str,
      title: str,
      lessons: list of dict {
        lesson_id: str,
        title: str,
        content: str,
        completed: bool
      }
    }
  - current_lesson: dict {
      lesson_id: str,
      title: str,
      content: str
    }
  - progress: int (0-100)


### 6. my_assignments.html
- Elements:
  - Div id="assignments-page"
  - Table id="assignments-table" (displays assignments list)
  - Button(s) id="submit-assignment-button-{assignment_id}" repeated for each assignment
  - Button id="back-to-dashboard"

- Context variables:
  - assignments: list of dict {
      assignment_id: str,
      course_id: str,
      title: str,
      description: str,
      due_date: str (YYYY-MM-DD),
      max_points: int
    }


### 7. submit_assignment.html
- Elements:
  - Div id="submit-page"
  - Div id="assignment-info" (shows assignment title and description)
  - Textarea id="submission-text"
  - Button id="submit-button"
  - Button id="back-to-assignments"

- Context variables:
  - assignment: dict {
      assignment_id: str,
      course_id: str,
      title: str,
      description: str,
      due_date: str,
      max_points: int
    }


### 8. certificates.html
- Elements:
  - Div id="certificates-page"
  - Div id="certificates-grid"
  - Button id="back-to-dashboard"

- Context variables:
  - certificates: list of dict {
      certificate_id: str,
      username: str,
      course_id: str,
      issue_date: str,
      course_title: str
    }


### 9. profile.html
- Elements:
  - Div id="profile-page"
  - Input id="profile-email"
  - Input id="profile-fullname"
  - Button id="update-profile-button"
  - Button id="back-to-dashboard"

- Context variables:
  - user: dict {
      username: str,
      email: str,
      fullname: str
    }


---

## 3. Navigation Mappings and Button Actions

- Dashboard Page
  - `browse-courses-button` -> route `/catalog`
  - `my-courses-button` -> route `/my-courses`

- Course Catalog Page
  - `view-course-button-{course_id}` -> route `/course/<course_id>`
  - `back-to-dashboard` -> route `/dashboard`

- Course Details Page
  - `enroll-button` -> POST `/course/<course_id>/enroll` (No page change, updates enrollments)
  - `back-to-catalog` -> route `/catalog`

- My Courses Page
  - `continue-learning-button-{course_id}` -> route `/course/<course_id>/learn`
  - `back-to-dashboard` -> route `/dashboard`

- Course Learning Page
  - `mark-complete-button` -> POST `/course/<course_id>/learn/complete` (Updates progress and certificates)
  - `back-to-my-courses` -> route `/my-courses`

- My Assignments Page
  - `submit-assignment-button-{assignment_id}` -> route `/assignment/<assignment_id>/submit`
  - `back-to-dashboard` -> route `/dashboard`

- Submit Assignment Page
  - `submit-button` -> POST `/assignment/<assignment_id>/submit` (Updates submissions)
  - `back-to-assignments` -> route `/assignments`

- Certificates Page
  - `back-to-dashboard` -> route `/dashboard`

- User Profile Page
  - `update-profile-button` -> POST `/profile/update` (Update user data)
  - `back-to-dashboard` -> route `/dashboard`

---

## 4. Data Storage Schemas

### users.txt
- Filename: `data/users.txt`
- Fields (pipe-delimited): `username|email|fullname`
- Purpose: Store user account information
- Example data:
  ```
  john|john@student.com|John Student
  alice|alice@instructor.com|Alice Professor
  jane|jane@student.com|Jane Learner
  ```

### courses.txt
- Filename: `data/courses.txt`
- Fields (pipe-delimited): `course_id|title|description|category|level|duration|status`
- Purpose: Store course details
- Example data:
  ```
  1|Python Programming|Learn Python from scratch|Programming|Beginner|40 hours|Active
  2|Web Development|Build modern websites|Web|Intermediate|60 hours|Active
  3|Data Science|Introduction to data analysis|Data|Advanced|80 hours|Active
  ```

### enrollments.txt
- Filename: `data/enrollments.txt`
- Fields (pipe-delimited): `enrollment_id|username|course_id|enrollment_date|progress|status`
- Purpose: Store user enrollments and progress
- Example data:
  ```
  1|john|1|2024-11-01|75|In Progress
  2|jane|1|2024-10-15|100|Completed
  3|john|2|2024-11-10|25|In Progress
  ```

### assignments.txt
- Filename: `data/assignments.txt`
- Fields (pipe-delimited): `assignment_id|course_id|title|description|due_date|max_points`
- Purpose: Store assignment details
- Example data:
  ```
  1|1|Python Basics Quiz|Complete the quiz on variables and data types|2024-12-01|100
  2|1|Final Project|Build a calculator application|2024-12-15|200
  ```

### submissions.txt
- Filename: `data/submissions.txt`
- Fields (pipe-delimited): `submission_id|assignment_id|username|submission_text|submit_date|grade|feedback`
- Purpose: Store assignment submissions and grading
- Example data:
  ```
  1|1|john|My answers are...|2024-11-25|85|Good work!
  2|2|jane|Here is my project...|2024-11-20|95|Excellent!
  ```

### certificates.txt
- Filename: `data/certificates.txt`
- Fields (pipe-delimited): `certificate_id|username|course_id|issue_date`
- Purpose: Store issued certificates
- Example data:
  ```
  1|jane|1|2024-11-22
  ```

---

This design specification document provides all necessary details for backend and frontend implementation of the OnlineCourse web application.