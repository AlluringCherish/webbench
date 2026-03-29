# GymMembership Web Application Design Specification

---

## Section 1: Flask Routes Specification

| Route Path             | Function Name           | HTTP Method(s) | Template Filename     | Context Variables (name: type) |
|------------------------|------------------------|----------------|-----------------------|--------------------------------|
| /                      | root_redirect           | GET            | None (Redirect)        | None                           |
| /dashboard             | dashboard_page          | GET            | dashboard.html         | None                           |
| /memberships           | memberships_page        | GET            | memberships.html       | plans: list of dict             |
| /plan/<int:plan_id>    | plan_details_page       | GET            | plan_details.html      | plan: dict, reviews: list of dict |
| /schedule              | class_schedule_page     | GET            | class_schedule.html    | classes: list of dict          |
| /trainers              | trainer_profiles_page   | GET            | trainer_profiles.html  | trainers: list of dict         |
| /trainer/<int:trainer_id> | trainer_detail_page   | GET            | trainer_detail.html    | trainer: dict, reviews: list of dict |
| /book-trainer          | pt_booking_page         | GET, POST     | pt_booking.html         | trainers: list of dict (GET), booking_result: str (POST, optional) |
| /workouts              | workout_records_page    | GET            | workouts.html          | workouts: list of dict         |
| /log-workout           | log_workout_page        | GET, POST     | log_workout.html         | submission_result: str (POST, optional) |

**Route Details:**

- **/**
  - Redirects to `/dashboard`.
  - Function: `root_redirect`
  - Method: GET

- **/dashboard**
  - Displays main dashboard.
  - Function: `dashboard_page`
  - Method: GET
  - Template: `dashboard.html`
  - Context Variables:
    - None (static content for welcome and buttons)

- **/memberships**
  - Lists all membership plans with filtering handled client-side.
  - Function: `memberships_page`
  - Method: GET
  - Template: `memberships.html`
  - Context Variables:
    - `plans`: list of dictionaries, each dict contains:
      - `membership_id` (int)
      - `plan_name` (str)
      - `price` (float)
      - `billing_cycle` (str)
      - `features` (str)
      - `max_classes` (str, could be numeric or 'unlimited')

- **/plan/<int:plan_id>**
  - Shows detail info of a specific membership plan.
  - Function: `plan_details_page`
  - Method: GET
  - Template: `plan_details.html`
  - Context Variables:
    - `plan`: dictionary with same fields as in `plans`
    - `reviews`: list of review dicts (if applicable, else empty list) - note: reviews are mentioned in UI but no separate data file provided, assume an empty list or mock data

- **/schedule**
  - Displays class schedules with filtering and search on client side.
  - Function: `class_schedule_page`
  - Method: GET
  - Template: `class_schedule.html`
  - Context Variables:
    - `classes`: list of dictionaries with fields:
      - `class_id` (int)
      - `class_name` (str)
      - `trainer_id` (int)
      - `class_type` (str)
      - `schedule_day` (str)
      - `schedule_time` (str, HH:MM)
      - `capacity` (int)
      - `duration` (int, minutes)

- **/trainers**
  - Shows all trainers with search and filter on client side.
  - Function: `trainer_profiles_page`
  - Method: GET
  - Template: `trainer_profiles.html`
  - Context Variables:
    - `trainers`: list of dictionaries, each dict has:
      - `trainer_id` (int)
      - `name` (str)
      - `specialty` (str)
      - `certifications` (str)
      - `experience_years` (int)
      - `bio` (str)

- **/trainer/<int:trainer_id>**
  - Shows detailed trainer profile.
  - Function: `trainer_detail_page`
  - Method: GET
  - Template: `trainer_detail.html`
  - Context Variables:
    - `trainer`: dict same structure as in trainers list
    - `reviews`: list of dicts (similar note as plan reviews, mock or empty list)

- **/book-trainer**
  - GET: Show booking form.
  - POST: Process booking submission.
  - Function: `pt_booking_page`
  - Methods: GET, POST
  - Template: `pt_booking.html`
  - Context Variables:
    - GET:
      - `trainers`: list of trainer dicts as above
    - POST:
      - `booking_result`: str (success or error message)

- **/workouts**
  - Shows user workout history.
  - Function: `workout_records_page`
  - Method: GET
  - Template: `workouts.html`
  - Context Variables:
    - `workouts`: list of dictionaries with fields:
      - `workout_id` (int)
      - `member_name` (str)
      - `workout_type` (str)
      - `workout_date` (str, YYYY-MM-DD)
      - `duration_minutes` (int)
      - `calories_burned` (int)
      - `notes` (str)

- **/log-workout**
  - GET: Show form to log a workout.
  - POST: Process workout submission.
  - Function: `log_workout_page`
  - Methods: GET, POST
  - Template: `log_workout.html`
  - Context Variables:
    - POST:
      - `submission_result`: str (success or error message)

---

## Section 2: HTML Template Specifications

### 1. dashboard.html
- **Page Title:** Gym Membership Dashboard
- **Element IDs:**
  - `dashboard-page` (Div): Container for the page
  - `member-welcome` (Div): Welcome section with member status info
  - `browse-membership-button` (Button): Navigates to `/memberships` using `url_for('memberships_page')`
  - `view-schedule-button` (Button): Navigates to `/schedule` using `url_for('class_schedule_page')`
  - `book-trainer-button` (Button): Navigates to `/book-trainer` using `url_for('pt_booking_page')`
- **Context Variables:** None
- **Navigation Buttons:** Buttons trigger navigation via Flask endpoints.

### 2. memberships.html
- **Page Title:** Membership Plans
- **Element IDs:**
  - `membership-page` (Div): Container
  - `plan-filter` (Dropdown): Filter by membership type (Basic, Premium, Elite)
  - `plans-grid` (Div): Grid container for plan cards
  - `view-details-button-{{ plan.membership_id }}` (Button): Button in each plan card linking to `/plan/<plan_id>`
  - `back-to-dashboard` (Button): Navigates to `/dashboard` using `url_for('dashboard_page')`
- **Context Variables:**
  - `plans`: loop as `{% for plan in plans %}` with fields `membership_id`, `plan_name`, `price`, `billing_cycle`, `features`, `max_classes`

### 3. plan_details.html
- **Page Title:** Plan Details
- **Element IDs:**
  - `plan-details-page` (Div): Container
  - `plan-title` (H1): Displays `plan['plan_name']`
  - `plan-price` (Div): Displays `plan['price']` and `plan['billing_cycle']`
  - `plan-features` (Div): Displays `plan['features']`
  - `enroll-plan-button` (Button): Enroll action (no submission functionality specified)
  - `plan-reviews` (Div): Section for plan member reviews, loop over `reviews`
- **Context Variables:**
  - `plan`: dict with membership plan details
  - `reviews`: list of review dicts (e.g. member name and comment, if any)

### 4. class_schedule.html
- **Page Title:** Class Schedule
- **Element IDs:**
  - `schedule-page` (Div): Container
  - `schedule-search` (Input): Search classes by name or trainer
  - `schedule-filter` (Dropdown): Filter by class type (Yoga, CrossFit, Pilates, Boxing, etc.)
  - `classes-grid` (Div): Grid showing class cards
  - `enroll-class-button-{{ class.class_id }}` (Button): Enroll in class button for each class card
- **Context Variables:**
  - `classes`: loop as `{% for class in classes %}` with fields as specified

### 5. trainer_profiles.html
- **Page Title:** Trainer Profiles
- **Element IDs:**
  - `trainers-page` (Div): Container
  - `trainer-search` (Input): Search trainers by name or specialty
  - `specialty-filter` (Dropdown): Filter by specialty (Strength, Cardio, Flexibility, Weight Loss)
  - `trainers-grid` (Div): Grid of trainer cards
  - `view-trainer-button-{{ trainer.trainer_id }}` (Button): View detail button for each trainer card
- **Context Variables:**
  - `trainers`: loop as `{% for trainer in trainers %}` with fields as specified

### 6. trainer_detail.html
- **Page Title:** Trainer Profile
- **Element IDs:**
  - `trainer-detail-page` (Div): Container
  - `trainer-name` (H1): Displays `trainer['name']`
  - `trainer-bio` (Div): Biography text
  - `trainer-certifications` (Div): Certification information
  - `book-session-button` (Button): Book a session with this trainer
  - `trainer-reviews` (Div): Section for client reviews, loop over `reviews`
- **Context Variables:**
  - `trainer`: detailed dict
  - `reviews`: list of review dicts

### 7. pt_booking.html
- **Page Title:** Book Personal Training
- **Element IDs:**
  - `booking-page` (Div): Container
  - `select-trainer` (Dropdown): Select trainer by name, option value is `trainer_id`
  - `session-date` (Input type=date): Select date
  - `session-time` (Dropdown): Select time slot
  - `session-duration` (Dropdown): Options 30, 60, 90 minutes
  - `confirm-booking-button` (Button): Submit booking
- **Context Variables:**
  - On GET:
    - `trainers`: list of trainer dicts
  - On POST:
    - `booking_result`: string (success or error message)

### 8. workouts.html
- **Page Title:** My Workout Records
- **Element IDs:**
  - `workouts-page` (Div): Container
  - `workouts-table` (Table): Displays workout history rows
  - `filter-by-type` (Dropdown): Filter workouts by type (Class, PT Session, Personal)
  - `log-workout-button` (Button): Navigate to `/log-workout` using `url_for('log_workout_page')`
  - `back-to-dashboard` (Button): Navigate to `/dashboard` using `url_for('dashboard_page')`
- **Context Variables:**
  - `workouts`: loop as `{% for workout in workouts %}` with fields as specified

### 9. log_workout.html
- **Page Title:** Log Workout
- **Element IDs:**
  - `log-workout-page` (Div): Container
  - `workout-type` (Dropdown): Options Cardio, Strength, Flexibility, Sports
  - `workout-duration` (Input number): Duration in minutes
  - `calories-burned` (Input number): Estimated calories burned
  - `workout-notes` (Textarea): Notes field
  - `submit-workout-button` (Button): Submit the workout log
- **Context Variables:**
  - On POST:
    - `submission_result`: string (success or error message)

---

## Section 3: Data File Schemas

### 1. Memberships Data
- **File Path:** data/memberships.txt
- **Fields (Pipe-Delimited):**
  1. membership_id (int)
  2. plan_name (str)
  3. price (float)
  4. billing_cycle (str)
  5. features (str)
  6. max_classes (str) - numeric string or "unlimited"
- **Description:** Stores all membership plans with pricing and features.
- **Examples:**
  ```
  1|Basic|29.99|monthly|Gym access, 2 classes per week|8
  2|Premium|59.99|monthly|Gym access, 5 classes per week, 2 PT sessions|20
  3|Elite|99.99|monthly|Unlimited gym access, unlimited classes, 4 PT sessions, nutrition coaching|unlimited
  ```

### 2. Classes Data
- **File Path:** data/classes.txt
- **Fields (Pipe-Delimited):**
  1. class_id (int)
  2. class_name (str)
  3. trainer_id (int)
  4. class_type (str)
  5. schedule_day (str)
  6. schedule_time (str, HH:MM format)
  7. capacity (int)
  8. duration (int, minutes)
- **Description:** Stores the schedule and details of fitness classes.
- **Examples:**
  ```
  1|Morning Yoga|1|Yoga|Monday|06:00|20|60
  2|CrossFit Bootcamp|2|CrossFit|Tuesday|18:00|15|45
  3|Pilates Core|3|Pilates|Wednesday|10:00|18|50
  ```

### 3. Trainers Data
- **File Path:** data/trainers.txt
- **Fields (Pipe-Delimited):**
  1. trainer_id (int)
  2. name (str)
  3. specialty (str)
  4. certifications (str)
  5. experience_years (int)
  6. bio (str)
- **Description:** Contains trainer profiles with specialties and experience.
- **Examples:**
  ```
  1|Sarah Johnson|Yoga & Flexibility|Certified Yoga Instructor, CPR|8|Expert in mind-body wellness and injury prevention
  2|Mike Thompson|Strength & Conditioning|NASM-CPT, CrossFit Level 2|10|Specializes in powerlifting and functional fitness
  3|Emma Davis|Pilates|Pilates Method Alliance Certified|6|Focus on core strength and postural alignment
  ```

### 4. Bookings Data
- **File Path:** data/bookings.txt
- **Fields (Pipe-Delimited):**
  1. booking_id (int)
  2. member_name (str)
  3. trainer_id (int)
  4. booking_date (str, YYYY-MM-DD)
  5. booking_time (str, HH:MM)
  6. duration_minutes (int)
  7. status (str, e.g., Confirmed, Pending)
- **Description:** Stores personal training session bookings.
- **Examples:**
  ```
  1|John Doe|1|2025-01-20|10:00|60|Confirmed
  2|Jane Smith|2|2025-01-21|14:00|45|Confirmed
  3|Alex Johnson|3|2025-01-22|16:00|60|Pending
  ```

### 5. Workouts Data
- **File Path:** data/workouts.txt
- **Fields (Pipe-Delimited):**
  1. workout_id (int)
  2. member_name (str)
  3. workout_type (str)
  4. workout_date (str, YYYY-MM-DD)
  5. duration_minutes (int)
  6. calories_burned (int)
  7. notes (str)
- **Description:** Stores user's workout logs and progress notes.
- **Examples:**
  ```
  1|John Doe|Cardio|2025-01-15|45|350|Morning run on treadmill
  2|Jane Smith|Strength|2025-01-16|60|420|Upper body weight training with trainer
  3|Alex Johnson|Class|2025-01-17|50|380|CrossFit Bootcamp session
  ```

---

**Notes:**
- Reviews are mentioned for plans and trainers UI but no explicit data files or formats are provided; backend can mock or leave empty lists.
- All element IDs must exactly match those specified to ensure frontend-backend integration.
- Button navigation links use Flask's `url_for()` with the corresponding function names.
- Filtering and searching on pages are assumed to be handled on frontend or client-side JavaScript.
- POST routes for booking and log workout must handle form submission and provide result messages to templates.

---

This completes the design specification for independent and parallel development of the GymMembership web application backend and frontend.
