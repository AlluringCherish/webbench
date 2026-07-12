# GymMembership Web Application Design Specification

---

## Section 1: Flask Routes Specification

### 1. Root Route
- **Route Path**: `/`
- **Function Name**: `root_redirect`
- **HTTP Methods**: GET
- **Template**: None (Redirect)
- **Description**: Redirects to the Dashboard page (`/dashboard`).

### 2. Dashboard Page
- **Route Path**: `/dashboard`
- **Function Name**: `dashboard`
- **HTTP Methods**: GET
- **Template**: `dashboard.html`
- **Context Variables**:
  - `member_status` (str): Member status or welcome message displayed in `member-welcome`.
  - `featured_classes` (list of dict): List containing featured class info to show highlights (optional for frontend display).

### 3. Membership Plans Page
- **Route Path**: `/memberships`
- **Function Name**: `memberships`
- **HTTP Methods**: GET
- **Template**: `memberships.html`
- **Context Variables**:
  - `plans` (list of dict): List of membership plans loaded from `memberships.txt`.
  - Each plan dict contains: `membership_id` (int), `plan_name` (str), `price` (str), `billing_cycle` (str), `features` (str), `max_classes` (str|int).

### 4. Plan Details Page
- **Route Path**: `/plan/<int:plan_id>`
- **Function Name**: `plan_details`
- **HTTP Methods**: GET
- **Template**: `plan_details.html`
- **Context Variables**:
  - `plan` (dict): Dictionary containing plan details for given `plan_id` (keys as above).
  - `reviews` (list of dict): List of member reviews for this plan (if any, else empty list).

### 5. Class Schedule Page
- **Route Path**: `/schedule`
- **Function Name**: `class_schedule`
- **HTTP Methods**: GET
- **Template**: `class_schedule.html`
- **Context Variables**:
  - `classes` (list of dict): List of fitness classes from `classes.txt`.
  - Each class dict contains: `class_id` (int), `class_name` (str), `trainer_id` (int), `class_type` (str), `schedule_day` (str), `schedule_time` (str), `capacity` (int), `duration` (int).

### 6. Trainer Profiles Page
- **Route Path**: `/trainers`
- **Function Name**: `trainer_profiles`
- **HTTP Methods**: GET
- **Template**: `trainer_profiles.html`
- **Context Variables**:
  - `trainers` (list of dict): List of trainers from `trainers.txt`.
  - Each trainer dict contains: `trainer_id` (int), `name` (str), `specialty` (str), `certifications` (str), `experience_years` (int), `bio` (str).

### 7. Trainer Detail Page
- **Route Path**: `/trainer/<int:trainer_id>`
- **Function Name**: `trainer_detail`
- **HTTP Methods**: GET
- **Template**: `trainer_detail.html`
- **Context Variables**:
  - `trainer` (dict): Dictionary of trainer details for the given `trainer_id`.
  - `reviews` (list of dict): List of client reviews for this trainer (empty list if none).

### 8. PT Booking Page
- **Route Path**: `/booking`
- **Function Name**: `pt_booking`
- **HTTP Methods**: GET, POST
- **Template**: `booking.html`
- **Context Variables** (GET):
  - `trainers` (list of dict): List of trainers for dropdown selection.
- **POST Payload**:
  - `trainer_id` (int): Selected trainer ID.
  - `session_date` (str, YYYY-MM-DD): Date selected.
  - `session_time` (str): Time slot selected.
  - `session_duration` (int): Duration in minutes.
- **Response**:
  - On success: Redirect or confirmation message.

### 9. Workout Records Page
- **Route Path**: `/workouts`
- **Function Name**: `workout_records`
- **HTTP Methods**: GET
- **Template**: `workout_records.html`
- **Context Variables**:
  - `workouts` (list of dict): List of workout records from `workouts.txt`.
  - Each workout dict contains: `workout_id` (int), `member_name` (str), `workout_type` (str), `workout_date` (str), `duration_minutes` (int), `calories_burned` (int), `notes` (str).

### 10. Log Workout Page
- **Route Path**: `/log_workout`
- **Function Name**: `log_workout`
- **HTTP Methods**: GET, POST
- **Template**: `log_workout.html`
- **Context Variables**: None on GET
- **POST Payload**:
  - `workout_type` (str)
  - `workout_duration` (int)
  - `calories_burned` (int)
  - `workout_notes` (str)
- **Response**:
  - On success: Redirect back to workout records or confirmation.

---

## Section 2: HTML Template Specifications

### 1. `dashboard.html`
- **Page Title**: Gym Membership Dashboard
- **Element IDs and Descriptions**:
  - `dashboard-page`: Div container for dashboard.
  - `member-welcome`: Div for welcome and member status.
  - `browse-membership-button`: Button to navigate to Membership Plans (`memberships` route).
  - `view-schedule-button`: Button to navigate to Class Schedule (`class_schedule` route).
  - `book-trainer-button`: Button to navigate to PT Booking (`pt_booking` route).
- **Context Variables**:
  - `member_status` (str)
  - `featured_classes` (list of dict, optional)
- **Navigation/Buttons**:
  - Buttons use `url_for('memberships')`, `url_for('class_schedule')`, `url_for('pt_booking')`.

### 2. `memberships.html`
- **Page Title**: Membership Plans
- **Element IDs and Descriptions**:
  - `membership-page`: Div container.
  - `plan-filter`: Dropdown for filtering by plan type.
  - `plans-grid`: Div displaying cards for each plan.
  - `view-details-button-{{ plan.membership_id }}`: Button on each card.
  - `back-to-dashboard`: Button to navigate back to Dashboard.
- **Context Variables**:
  - `plans`: Loop with e.g. `{% for plan in plans %}`.
- **Navigation/Buttons**:
  - `view-details-button-{{ plan.membership_id }}` links to `url_for('plan_details', plan_id=plan.membership_id)`.
  - `back-to-dashboard` links to `url_for('dashboard')`.

### 3. `plan_details.html`
- **Page Title**: Plan Details
- **Element IDs and Descriptions**:
  - `plan-details-page`: Div container.
  - `plan-title`: H1 with plan name.
  - `plan-price`: Div with price and billing cycle.
  - `plan-features`: Div listing features.
  - `enroll-plan-button`: Button to enroll.
  - `plan-reviews`: Div section for member reviews.
- **Context Variables**:
  - `plan` (dict)
  - `reviews` (list of dict)
- **Navigation/Buttons**:
  - `enroll-plan-button`: (Functionality optional, no additional route specified)
  - Possibly back navigation via browser or custom button if added.

### 4. `class_schedule.html`
- **Page Title**: Class Schedule
- **Element IDs and Descriptions**:
  - `schedule-page`: Div container.
  - `schedule-search`: Input field for class or trainer search.
  - `schedule-filter`: Dropdown to filter by class type.
  - `classes-grid`: Div grid showing class cards.
  - `enroll-class-button-{{ class.class_id }}`: Button to enroll.
- **Context Variables**:
  - `classes` (list of dict)
- **Navigation/Buttons**:
  - Enroll buttons can be designed for future POST or modal (not specified).

### 5. `trainer_profiles.html`
- **Page Title**: Trainer Profiles
- **Element IDs and Descriptions**:
  - `trainers-page`: Div container.
  - `trainer-search`: Input for searching trainers.
  - `specialty-filter`: Dropdown for specialty filtering.
  - `trainers-grid`: Div grid with trainer cards.
  - `view-trainer-button-{{ trainer.trainer_id }}`: Button on each trainer card.
- **Context Variables**:
  - `trainers` (list of dict)
- **Navigation/Buttons**:
  - Each `view-trainer-button-{{ trainer.trainer_id }}` links to `url_for('trainer_detail', trainer_id=trainer.trainer_id)`.

### 6. `trainer_detail.html`
- **Page Title**: Trainer Profile
- **Element IDs and Descriptions**:
  - `trainer-detail-page`: Div container.
  - `trainer-name`: H1 with trainer name.
  - `trainer-bio`: Div with biography and experience.
  - `trainer-certifications`: Div listing certifications.
  - `book-session-button`: Button to book session.
  - `trainer-reviews`: Div for client reviews.
- **Context Variables**:
  - `trainer` (dict)
  - `reviews` (list of dict)
- **Navigation/Buttons**:
  - `book-session-button` links to `url_for('pt_booking')` with trainer preselection if feasible.

### 7. `booking.html`
- **Page Title**: Book Personal Training
- **Element IDs and Descriptions**:
  - `booking-page`: Div container.
  - `select-trainer`: Dropdown to select trainer.
  - `session-date`: Input (date) for session date.
  - `session-time`: Dropdown for time slot selection.
  - `session-duration`: Dropdown for session duration.
  - `confirm-booking-button`: Button to submit booking.
- **Context Variables**:
  - `trainers` (list of dict)
- **Navigation/Buttons**:
  - Form posts to `/booking` route.

### 8. `workout_records.html`
- **Page Title**: My Workout Records
- **Element IDs and Descriptions**:
  - `workouts-page`: Div container.
  - `workouts-table`: Table showing workout history.
  - `filter-by-type`: Dropdown to filter workouts.
  - `log-workout-button`: Button to navigate to log workout page.
  - `back-to-dashboard`: Button to return to Dashboard.
- **Context Variables**:
  - `workouts` (list of dict)
- **Navigation/Buttons**:
  - `log-workout-button` links to `url_for('log_workout')`.
  - `back-to-dashboard` links to `url_for('dashboard')`.

### 9. `log_workout.html`
- **Page Title**: Log Workout
- **Element IDs and Descriptions**:
  - `log-workout-page`: Div container.
  - `workout-type`: Dropdown for workout type.
  - `workout-duration`: Input (number) for duration.
  - `calories-burned`: Input (number) for calories burned.
  - `workout-notes`: Textarea for notes.
  - `submit-workout-button`: Button to submit log.
- **Context Variables**: None
- **Navigation/Buttons**:
  - Form posts to `/log_workout` route.

---

## Section 3: Data File Schemas

### 1. Memberships Data
- **File Path**: `data/memberships.txt`
- **Field Order (pipe-delimited)**:
  1. `membership_id` (int)
  2. `plan_name` (str)
  3. `price` (str)
  4. `billing_cycle` (str)
  5. `features` (str)
  6. `max_classes` (str or int) - can be 'unlimited'
- **Description**: Stores membership plans with pricing, features, and usage limits.
- **Example Rows**:
  ```
  1|Basic|29.99|monthly|Gym access, 2 classes per week|8
  2|Premium|59.99|monthly|Gym access, 5 classes per week, 2 PT sessions|20
  3|Elite|99.99|monthly|Unlimited gym access, unlimited classes, 4 PT sessions, nutrition coaching|unlimited
  ```

### 2. Classes Data
- **File Path**: `data/classes.txt`
- **Field Order (pipe-delimited)**:
  1. `class_id` (int)
  2. `class_name` (str)
  3. `trainer_id` (int)
  4. `class_type` (str)
  5. `schedule_day` (str)
  6. `schedule_time` (str, HH:MM)
  7. `capacity` (int)
  8. `duration` (int, minutes)
- **Description**: Stores scheduled fitness classes.
- **Example Rows**:
  ```
  1|Morning Yoga|1|Yoga|Monday|06:00|20|60
  2|CrossFit Bootcamp|2|CrossFit|Tuesday|18:00|15|45
  3|Pilates Core|3|Pilates|Wednesday|10:00|18|50
  ```

### 3. Trainers Data
- **File Path**: `data/trainers.txt`
- **Field Order (pipe-delimited)**:
  1. `trainer_id` (int)
  2. `name` (str)
  3. `specialty` (str)
  4. `certifications` (str)
  5. `experience_years` (int)
  6. `bio` (str)
- **Description**: Stores trainer profiles and qualifications.
- **Example Rows**:
  ```
  1|Sarah Johnson|Yoga & Flexibility|Certified Yoga Instructor, CPR|8|Expert in mind-body wellness and injury prevention
  2|Mike Thompson|Strength & Conditioning|NASM-CPT, CrossFit Level 2|10|Specializes in powerlifting and functional fitness
  3|Emma Davis|Pilates|Pilates Method Alliance Certified|6|Focus on core strength and postural alignment
  ```

### 4. Bookings Data
- **File Path**: `data/bookings.txt`
- **Field Order (pipe-delimited)**:
  1. `booking_id` (int)
  2. `member_name` (str)
  3. `trainer_id` (int)
  4. `booking_date` (str, YYYY-MM-DD)
  5. `booking_time` (str, HH:MM)
  6. `duration_minutes` (int)
  7. `status` (str)
- **Description**: Stores personal training session bookings.
- **Example Rows**:
  ```
  1|John Doe|1|2025-01-20|10:00|60|Confirmed
  2|Jane Smith|2|2025-01-21|14:00|45|Confirmed
  3|Alex Johnson|3|2025-01-22|16:00|60|Pending
  ```

### 5. Workouts Data
- **File Path**: `data/workouts.txt`
- **Field Order (pipe-delimited)**:
  1. `workout_id` (int)
  2. `member_name` (str)
  3. `workout_type` (str)
  4. `workout_date` (str, YYYY-MM-DD)
  5. `duration_minutes` (int)
  6. `calories_burned` (int)
  7. `notes` (str)
- **Description**: Stores workout session records and progress.
- **Example Rows**:
  ```
  1|John Doe|Cardio|2025-01-15|45|350|Morning run on treadmill
  2|Jane Smith|Strength|2025-01-16|60|420|Upper body weight training with trainer
  3|Alex Johnson|Class|2025-01-17|50|380|CrossFit Bootcamp session
  ```

---

# End of Design Specification
