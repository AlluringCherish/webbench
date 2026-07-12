# GymMembership Web Application Design Specification

---

## Section 1: Flask Routes Specification

### General Note
- The root route `/` redirects to the Dashboard page.
- All page templates are rendered via GET methods except where form submissions are required (POST).

---

### 1. Root Route
- **Route Path:** `/`
- **Function Name:** root_redirect
- **HTTP Methods:** GET
- **Template:** None (redirect)
- **Behavior:** Redirects to `/dashboard` route.

### 2. Dashboard Page
- **Route Path:** `/dashboard`
- **Function Name:** dashboard
- **HTTP Methods:** GET
- **Template:** `dashboard.html`
- **Context Variables:**
  - `member_status` (str): Current member's status or welcome message.
  - `featured_classes` (list of dict): Example classes shown on dashboard.

### 3. Membership Plans Page
- **Route Path:** `/memberships`
- **Function Name:** memberships
- **HTTP Methods:** GET
- **Template:** `memberships.html`
- **Context Variables:**
  - `plans` (list of dict): List of membership plans loaded from `data/memberships.txt`.
  - `membership_types` (list of str): Membership types for filtering (e.g., ["Basic", "Premium", "Elite"]).

### 4. Plan Details Page
- **Route Path:** `/plan/<int:plan_id>`
- **Function Name:** plan_details
- **HTTP Methods:** GET
- **Template:** `plan_details.html`
- **Context Variables:**
  - `plan` (dict): The membership plan detail matching `plan_id`.
  - `plan_reviews` (list of dict): Reviews associated with the plan, if any (empty list if none).

### 5. Class Schedule Page
- **Route Path:** `/schedule`
- **Function Name:** class_schedule
- **HTTP Methods:** GET
- **Template:** `schedule.html`
- **Context Variables:**
  - `classes` (list of dict): List of classes loaded from `data/classes.txt`.
  - `class_types` (list of str): Unique class types for filtering.

### 6. Trainer Profiles Page
- **Route Path:** `/trainers`
- **Function Name:** trainers
- **HTTP Methods:** GET
- **Template:** `trainers.html`
- **Context Variables:**
  - `trainers` (list of dict): List of trainers loaded from `data/trainers.txt`.
  - `specialties` (list of str): Unique specialties for filtering.

### 7. Trainer Detail Page
- **Route Path:** `/trainer/<int:trainer_id>`
- **Function Name:** trainer_detail
- **HTTP Methods:** GET
- **Template:** `trainer_detail.html`
- **Context Variables:**
  - `trainer` (dict): Detailed trainer info matching `trainer_id`.
  - `trainer_reviews` (list of dict): Reviews or testimonials related to this trainer.

### 8. PT Booking Page
- **Route Path:** `/booking`
- **Function Name:** book_personal_training
- **HTTP Methods:** GET, POST
- **Template:** `booking.html`
- **Context Variables:**
  - `trainers` (list of dict): List of trainers for dropdown selection.
  - `time_slots` (list of str): Available session time slots.

- **POST Data:**
  - `trainer_id` (int)
  - `session_date` (str, yyyy-mm-dd)
  - `session_time` (str, time hh:mm)
  - `duration` (int, minutes)

### 9. Workout Records Page
- **Route Path:** `/workouts`
- **Function Name:** workout_records
- **HTTP Methods:** GET
- **Template:** `workouts.html`
- **Context Variables:**
  - `workouts` (list of dict): User's workout history from `data/workouts.txt`.
  - `workout_types` (list of str): Types for filtering workouts.

### 10. Log Workout Page
- **Route Path:** `/log-workout`
- **Function Name:** log_workout
- **HTTP Methods:** GET, POST
- **Template:** `log_workout.html`
- **Context Variables:** None (GET) or Confirmation message after POST

- **POST Data:**
  - `workout_type` (str)
  - `duration_minutes` (int)
  - `calories_burned` (int)
  - `notes` (str)

---

## Section 2: HTML Template Specifications

### 1. dashboard.html
- **Page Title:** Gym Membership Dashboard
- **Element IDs:**
  - `dashboard-page` (Div): Container for dashboard
  - `member-welcome` (Div): Welcome and member status
  - `browse-membership-button` (Button): Navigates to memberships route (`url_for('memberships')`)
  - `view-schedule-button` (Button): Navigates to schedule route (`url_for('class_schedule')`)
  - `book-trainer-button` (Button): Navigates to booking route (`url_for('book_personal_training')`)
- **Context Variables:**
  - `member_status` (str)
  - `featured_classes` (list of dict)

### 2. memberships.html
- **Page Title:** Membership Plans
- **Element IDs:**
  - `membership-page` (Div): Container
  - `plan-filter` (Dropdown): Options from `membership_types`
  - `plans-grid` (Div): Displays membership plan cards
  - `view-details-button-{plan_id}` (Button): View details for each plan
  - `back-to-dashboard` (Button): Navigates back to dashboard (`url_for('dashboard')`)
- **Context Variables:**
  - `plans` (list of dict)
  - `membership_types` (list of str)

### 3. plan_details.html
- **Page Title:** Plan Details
- **Element IDs:**
  - `plan-details-page` (Div): Container
  - `plan-title` (H1): Plan name
  - `plan-price` (Div): Price and billing cycle
  - `plan-features` (Div): Features
  - `enroll-plan-button` (Button): Button to enroll (dummy link or action)
  - `plan-reviews` (Div): Member reviews
- **Context Variables:**
  - `plan` (dict) accessed by keys e.g., `plan['plan_name']`
  - `plan_reviews` (list of dict)

### 4. schedule.html
- **Page Title:** Class Schedule
- **Element IDs:**
  - `schedule-page` (Div): Container
  - `schedule-search` (Input): Search classes by name or trainer
  - `schedule-filter` (Dropdown): Options from `class_types`
  - `classes-grid` (Div): Display class cards
  - `enroll-class-button-{class_id}` (Button): Enroll in class
- **Context Variables:**
  - `classes` (list of dict)
  - `class_types` (list of str)

### 5. trainers.html
- **Page Title:** Trainer Profiles
- **Element IDs:**
  - `trainers-page` (Div): Container
  - `trainer-search` (Input): Search trainers
  - `specialty-filter` (Dropdown): Options from `specialties`
  - `trainers-grid` (Div): Display trainer cards
  - `view-trainer-button-{trainer_id}` (Button): View trainer detail
- **Context Variables:**
  - `trainers` (list of dict)
  - `specialties` (list of str)

### 6. trainer_detail.html
- **Page Title:** Trainer Profile
- **Element IDs:**
  - `trainer-detail-page` (Div): Container
  - `trainer-name` (H1): Trainer name
  - `trainer-bio` (Div): Bio/experience
  - `trainer-certifications` (Div): Certifications
  - `book-session-button` (Button): Book session with trainer
  - `trainer-reviews` (Div): Client reviews
- **Context Variables:**
  - `trainer` (dict)
  - `trainer_reviews` (list of dict)

### 7. booking.html
- **Page Title:** Book Personal Training
- **Element IDs:**
  - `booking-page` (Div): Container
  - `select-trainer` (Dropdown): Select trainer
  - `session-date` (Input date): Choose date
  - `session-time` (Dropdown): Session time slots
  - `session-duration` (Dropdown): Session duration options
  - `confirm-booking-button` (Button): Confirm booking
- **Context Variables:**
  - `trainers` (list of dict)
  - `time_slots` (list of str)

### 8. workouts.html
- **Page Title:** My Workout Records
- **Element IDs:**
  - `workouts-page` (Div): Container
  - `workouts-table` (Table): Workout history
  - `filter-by-type` (Dropdown): Filter by workout types
  - `log-workout-button` (Button): Navigate to log workout
  - `back-to-dashboard` (Button): Navigate to dashboard
- **Context Variables:**
  - `workouts` (list of dict)
  - `workout_types` (list of str)

### 9. log_workout.html
- **Page Title:** Log Workout
- **Element IDs:**
  - `log-workout-page` (Div): Container
  - `workout-type` (Dropdown): Select workout type
  - `workout-duration` (Input number): Duration minutes
  - `calories-burned` (Input number): Calories burned
  - `workout-notes` (Textarea): Notes
  - `submit-workout-button` (Button): Submit workout
- **Context Variables:** None

---

## Section 3: Data File Schemas

### 1. Memberships Data
- **File Path:** `data/memberships.txt`
- **Field Order (pipe-delimited):**
  - membership_id (int)
  - plan_name (str)
  - price (float as str)
  - billing_cycle (str)
  - features (str)
  - max_classes (str or int: number or 'unlimited')
- **Description:** Contains membership plans with pricing and features.
- **Example Rows:**
  ```
  1|Basic|29.99|monthly|Gym access, 2 classes per week|8
  2|Premium|59.99|monthly|Gym access, 5 classes per week, 2 PT sessions|20
  3|Elite|99.99|monthly|Unlimited gym access, unlimited classes, 4 PT sessions, nutrition coaching|unlimited
  ```

### 2. Classes Data
- **File Path:** `data/classes.txt`
- **Field Order (pipe-delimited):**
  - class_id (int)
  - class_name (str)
  - trainer_id (int)
  - class_type (str)
  - schedule_day (str)
  - schedule_time (str, HH:MM 24hr)
  - capacity (int)
  - duration (int minutes)
- **Description:** Contains fitness classes scheduled with trainer info.
- **Example Rows:**
  ```
  1|Morning Yoga|1|Yoga|Monday|06:00|20|60
  2|CrossFit Bootcamp|2|CrossFit|Tuesday|18:00|15|45
  3|Pilates Core|3|Pilates|Wednesday|10:00|18|50
  ```

### 3. Trainers Data
- **File Path:** `data/trainers.txt`
- **Field Order (pipe-delimited):**
  - trainer_id (int)
  - name (str)
  - specialty (str)
  - certifications (str)
  - experience_years (int)
  - bio (str)
- **Description:** Details about trainers including expertise and experience.
- **Example Rows:**
  ```
  1|Sarah Johnson|Yoga & Flexibility|Certified Yoga Instructor, CPR|8|Expert in mind-body wellness and injury prevention
  2|Mike Thompson|Strength & Conditioning|NASM-CPT, CrossFit Level 2|10|Specializes in powerlifting and functional fitness
  3|Emma Davis|Pilates|Pilates Method Alliance Certified|6|Focus on core strength and postural alignment
  ```

### 4. Bookings Data
- **File Path:** `data/bookings.txt`
- **Field Order (pipe-delimited):**
  - booking_id (int)
  - member_name (str)
  - trainer_id (int)
  - booking_date (str, yyyy-mm-dd)
  - booking_time (str, HH:MM 24hr)
  - duration_minutes (int)
  - status (str)
- **Description:** Records personal training session bookings.
- **Example Rows:**
  ```
  1|John Doe|1|2025-01-20|10:00|60|Confirmed
  2|Jane Smith|2|2025-01-21|14:00|45|Confirmed
  3|Alex Johnson|3|2025-01-22|16:00|60|Pending
  ```

### 5. Workouts Data
- **File Path:** `data/workouts.txt`
- **Field Order (pipe-delimited):**
  - workout_id (int)
  - member_name (str)
  - workout_type (str)
  - workout_date (str, yyyy-mm-dd)
  - duration_minutes (int)
  - calories_burned (int)
  - notes (str)
- **Description:** User workout history and progress notes.
- **Example Rows:**
  ```
  1|John Doe|Cardio|2025-01-15|45|350|Morning run on treadmill
  2|Jane Smith|Strength|2025-01-16|60|420|Upper body weight training with trainer
  3|Alex Johnson|Class|2025-01-17|50|380|CrossFit Bootcamp session
  ```

---

# End of Design Specification
