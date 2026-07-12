# GymMembership Web Application Design Specifications

---

## Section 1: Flask Routes Specification

### 1. Root Route
- **Path**: `/`
- **Function Name**: `root`
- **HTTP Method**: GET
- **Action**: Redirect to Dashboard page route `/dashboard`
- **Template**: None
- **Context Variables**: None

### 2. Dashboard Page
- **Path**: `/dashboard`
- **Function Name**: `dashboard`
- **HTTP Method**: GET
- **Template**: `dashboard.html`
- **Context Variables**:
  - `member_status` (str): A string showing member status or welcome message.
  - `featured_classes` (list of dict): List of featured class data dictionaries.
  - `navigation_routes` (dict): Dictionary of route names for navigation buttons.

### 3. Membership Plans Page
- **Path**: `/memberships`
- **Function Name**: `memberships`
- **HTTP Method**: GET
- **Template**: `memberships.html`
- **Context Variables**:
  - `plans` (list of dict): List of membership plans with keys matching data fields.
  - `membership_types` (list of str): List of membership types for filtering (e.g., Basic, Premium, Elite).

### 4. Plan Details Page
- **Path**: `/plan/<int:plan_id>`
- **Function Name**: `plan_details`
- **HTTP Method**: GET
- **Template**: `plan_details.html`
- **Context Variables**:
  - `plan` (dict): Dictionary representing the membership plan details.
  - `reviews` (list of dict): List of reviews for the given plan (if applicable).

### 5. Class Schedule Page
- **Path**: `/schedule`
- **Function Name**: `class_schedule`
- **HTTP Method**: GET
- **Template**: `schedule.html`
- **Context Variables**:
  - `classes` (list of dict): List of available classes.
  - `class_types` (list of str): List of class types for filtering.

### 6. Trainer Profiles Page
- **Path**: `/trainers`
- **Function Name**: `trainers`
- **HTTP Method**: GET
- **Template**: `trainers.html`
- **Context Variables**:
  - `trainers` (list of dict): List of trainer profiles.
  - `specialties` (list of str): List of specialties for filtering.

### 7. Trainer Detail Page
- **Path**: `/trainer/<int:trainer_id>`
- **Function Name**: `trainer_detail`
- **HTTP Method**: GET
- **Template**: `trainer_detail.html`
- **Context Variables**:
  - `trainer` (dict): Trainer detail information.
  - `reviews` (list of dict): List of reviews for the trainer.

### 8. PT Booking Page
- **Path**: `/booking`
- **Function Name**: `pt_booking`
- **HTTP Methods**: GET, POST
- **Template**: `booking.html`
- **Context Variables (GET)**:
  - `trainers` (list of dict): List of trainers for dropdown selection.
  - `available_times` (list of str): List of time slots for session time dropdown.
  - `durations` (list of int): List of session durations available.
- **POST**:
  - Accepts form data for booking: `trainer_id` (int), `session_date` (str), `session_time` (str), `session_duration` (int), and member_name (may be hardcoded or input, unspecified).
  - On success, redirect to booking confirmation or dashboard (not specified).

### 9. Workout Records Page
- **Path**: `/workouts`
- **Function Name**: `workout_records`
- **HTTP Method**: GET
- **Template**: `workouts.html`
- **Context Variables**:
  - `workouts` (list of dict): List of workout history records.
  - `workout_types` (list of str): List of workout types for filtering.

### 10. Log Workout Page
- **Path**: `/log_workout`
- **Function Name**: `log_workout`
- **HTTP Methods**: GET, POST
- **Template**: `log_workout.html`
- **Context Variables (GET)**:
  - `workout_types` (list of str): List of workout types for dropdown.
- **POST**:
  - Accepts form data: `workout_type` (str), `workout_duration` (int), `calories_burned` (int), `workout_notes` (str).
  - On success, redirect to workouts page.

---

## Section 2: HTML Template Specifications

### 1. `dashboard.html`
- **Page Title**: Gym Membership Dashboard
- **Element IDs and Descriptions**:
  - `dashboard-page` (Div): Container for entire dashboard page.
  - `member-welcome` (Div): Welcome and member status information.
  - `browse-membership-button` (Button): Navigates to `/memberships`.
  - `view-schedule-button` (Button): Navigates to `/schedule`.
  - `book-trainer-button` (Button): Navigates to `/booking`.
- **Context Variables**:
  - `member_status` (str): Displayed inside `member-welcome`.
  - `featured_classes` (list of dict): Could be used to show highlights.
- **Navigation Elements**:
  - Buttons with IDs above use `url_for('memberships')`, `url_for('class_schedule')`, `url_for('pt_booking')` respectively.

### 2. `memberships.html`
- **Page Title**: Membership Plans
- **Element IDs and Descriptions**:
  - `membership-page` (Div): Container for the membership plans.
  - `plan-filter` (Dropdown): For selecting membership type filter.
  - `plans-grid` (Div): Contains plan cards.
  - `view-details-button-{plan_id}` (Button): Each plan card has a button with this dynamic ID to view details.
  - `back-to-dashboard` (Button): Navigates back to `/dashboard`.
- **Context Variables**:
  - `plans` (list of dict): Loop over `plans` to render each card.
  - `membership_types` (list of str): Used to populate `plan-filter` dropdown.
- **Navigation Elements**:
  - `back-to-dashboard` button calls `url_for('dashboard')`.
  - `view-details-button-{plan_id}` triggers route `url_for('plan_details', plan_id=plan_id)`.

### 3. `plan_details.html`
- **Page Title**: Plan Details
- **Element IDs and Descriptions**:
  - `plan-details-page` (Div): Container for plan details.
  - `plan-title` (H1): Displays the plan name.
  - `plan-price` (Div): Shows price and billing cycle.
  - `plan-features` (Div): Lists features included.
  - `enroll-plan-button` (Button): Enrolls user in plan.
  - `plan-reviews` (Div): Section showing reviews.
- **Context Variables**:
  - `plan` (dict): Access by `plan['plan_name']`, `plan['price']`, etc.
  - `reviews` (list of dict): Loop to render reviews.
- **Navigation Elements**:
  - Enroll button (`enroll-plan-button`) can POST or link as per further implementation.

### 4. `schedule.html`
- **Page Title**: Class Schedule
- **Element IDs and Descriptions**:
  - `schedule-page` (Div): Container for schedule.
  - `schedule-search` (Input): Text input for searching classes.
  - `schedule-filter` (Dropdown): Filter classes by `class_type`.
  - `classes-grid` (Div): Displays class cards.
  - `enroll-class-button-{class_id}` (Button): Enroll in specific class.
- **Context Variables**:
  - `classes` (list of dict): Loop to render classes.
  - `class_types` (list of str): Populate filter dropdown.
- **Navigation Elements**:
  - Enroll buttons link to enroll functionality (not described in requirements; can be placeholders).

### 5. `trainers.html`
- **Page Title**: Trainer Profiles
- **Element IDs and Descriptions**:
  - `trainers-page` (Div): Container for trainers.
  - `trainer-search` (Input): Search trainers by name or specialty.
  - `specialty-filter` (Dropdown): Filter by specialty.
  - `trainers-grid` (Div): Displays trainer cards.
  - `view-trainer-button-{trainer_id}` (Button): View detailed profile.
- **Context Variables**:
  - `trainers` (list of dict): Trainer data.
  - `specialties` (list of str): Populate specialty filter.
- **Navigation Elements**:
  - View trainer buttons link to `url_for('trainer_detail', trainer_id=trainer_id)`.

### 6. `trainer_detail.html`
- **Page Title**: Trainer Profile
- **Element IDs and Descriptions**:
  - `trainer-detail-page` (Div): Container for trainer detail.
  - `trainer-name` (H1): Trainer name.
  - `trainer-bio` (Div): Biography text.
  - `trainer-certifications` (Div): Certifications.
  - `book-session-button` (Button): Book session with trainer.
  - `trainer-reviews` (Div): Client reviews.
- **Context Variables**:
  - `trainer` (dict): Access attributes such as `trainer['name']`, `trainer['bio']`.
  - `reviews` (list of dict): Loop for reviews.
- **Navigation Elements**:
  - Book session button routes to `/booking` with pre-selected trainer (implementation detail).

### 7. `booking.html`
- **Page Title**: Book Personal Training
- **Element IDs and Descriptions**:
  - `booking-page` (Div): Container for booking.
  - `select-trainer` (Dropdown): Select trainer for session.
  - `session-date` (Input, date): Select the date.
  - `session-time` (Dropdown): Select session time slot.
  - `session-duration` (Dropdown): Select duration (30, 60, 90).
  - `confirm-booking-button` (Button): Confirm booking.
- **Context Variables**:
  - `trainers` (list of dict): To build `select-trainer` options.
  - `available_times` (list of str): To build `session-time` options.
  - `durations` (list of int): To build session-duration dropdown.
- **Navigation Elements**:
  - Booking form submission handled by POST to same route.

### 8. `workouts.html`
- **Page Title**: My Workout Records
- **Element IDs and Descriptions**:
  - `workouts-page` (Div): Container for workouts.
  - `workouts-table` (Table): Displays workout history rows.
  - `filter-by-type` (Dropdown): Filter workouts by type.
  - `log-workout-button` (Button): Navigate to log workout page.
  - `back-to-dashboard` (Button): Navigate back to dashboard.
- **Context Variables**:
  - `workouts` (list of dict): Workout records to display.
  - `workout_types` (list of str): Populate filter dropdown.
- **Navigation Elements**:
  - Log workout button links to `url_for('log_workout')`.
  - Back to dashboard button links to `url_for('dashboard')`.

### 9. `log_workout.html`
- **Page Title**: Log Workout
- **Element IDs and Descriptions**:
  - `log-workout-page` (Div): Container for log workout.
  - `workout-type` (Dropdown): Select workout type.
  - `workout-duration` (Input, number): Input workout duration in minutes.
  - `calories-burned` (Input, number): Input estimated calories burned.
  - `workout-notes` (Textarea): Notes about workout.
  - `submit-workout-button` (Button): Submit workout log.
- **Context Variables**:
  - `workout_types` (list of str): Populate workout-type dropdown.
- **Navigation Elements**:
  - Form submission handled by POST to same route.

---

## Section 3: Data File Schemas

### 1. Memberships Data
- **File Path**: `data/memberships.txt`
- **Fields (pipe-delimited order)**:
  1. `membership_id` (int)
  2. `plan_name` (str)
  3. `price` (float, string format)
  4. `billing_cycle` (str)
  5. `features` (str) - comma-separated features list as one string
  6. `max_classes` (str or int) - number limit or "unlimited"
- **Description**: Stores gym membership plan details including pricing and features.
- **Example Rows**:
  ```
  1|Basic|29.99|monthly|Gym access, 2 classes per week|8
  2|Premium|59.99|monthly|Gym access, 5 classes per week, 2 PT sessions|20
  3|Elite|99.99|monthly|Unlimited gym access, unlimited classes, 4 PT sessions, nutrition coaching|unlimited
  ```

### 2. Classes Data
- **File Path**: `data/classes.txt`
- **Fields (pipe-delimited order)**:
  1. `class_id` (int)
  2. `class_name` (str)
  3. `trainer_id` (int)
  4. `class_type` (str)
  5. `schedule_day` (str)
  6. `schedule_time` (str) - 24h format HH:MM
  7. `capacity` (int)
  8. `duration` (int, minutes)
- **Description**: Stores fitness class schedules including trainer and timing.
- **Example Rows**:
  ```
  1|Morning Yoga|1|Yoga|Monday|06:00|20|60
  2|CrossFit Bootcamp|2|CrossFit|Tuesday|18:00|15|45
  3|Pilates Core|3|Pilates|Wednesday|10:00|18|50
  ```

### 3. Trainers Data
- **File Path**: `data/trainers.txt`
- **Fields (pipe-delimited order)**:
  1. `trainer_id` (int)
  2. `name` (str)
  3. `specialty` (str)
  4. `certifications` (str) - comma-separated list
  5. `experience_years` (int)
  6. `bio` (str)
- **Description**: Stores trainer profiles with credentials and bio.
- **Example Rows**:
  ```
  1|Sarah Johnson|Yoga & Flexibility|Certified Yoga Instructor, CPR|8|Expert in mind-body wellness and injury prevention
  2|Mike Thompson|Strength & Conditioning|NASM-CPT, CrossFit Level 2|10|Specializes in powerlifting and functional fitness
  3|Emma Davis|Pilates|Pilates Method Alliance Certified|6|Focus on core strength and postural alignment
  ```

### 4. Bookings Data
- **File Path**: `data/bookings.txt`
- **Fields (pipe-delimited order)**:
  1. `booking_id` (int)
  2. `member_name` (str)
  3. `trainer_id` (int)
  4. `booking_date` (str) - YYYY-MM-DD
  5. `booking_time` (str) - HH:MM 24h format
  6. `duration_minutes` (int)
  7. `status` (str) - e.g., Confirmed, Pending
- **Description**: Stores personal training booking details.
- **Example Rows**:
  ```
  1|John Doe|1|2025-01-20|10:00|60|Confirmed
  2|Jane Smith|2|2025-01-21|14:00|45|Confirmed
  3|Alex Johnson|3|2025-01-22|16:00|60|Pending
  ```

### 5. Workouts Data
- **File Path**: `data/workouts.txt`
- **Fields (pipe-delimited order)**:
  1. `workout_id` (int)
  2. `member_name` (str)
  3. `workout_type` (str)
  4. `workout_date` (str) - YYYY-MM-DD
  5. `duration_minutes` (int)
  6. `calories_burned` (int)
  7. `notes` (str)
- **Description**: Stores user workout session records.
- **Example Rows**:
  ```
  1|John Doe|Cardio|2025-01-15|45|350|Morning run on treadmill
  2|Jane Smith|Strength|2025-01-16|60|420|Upper body weight training with trainer
  3|Alex Johnson|Class|2025-01-17|50|380|CrossFit Bootcamp session
  ```

---

### Notes:
- All dynamic element IDs with parameters (e.g., `view-details-button-{plan_id}`) use Jinja2 syntax in templates for ID construction.
- Context variable names are consistent throughout for ease of implementation.
- Navigation uses Flask `url_for()` referencing function names from Section 1.
- POST forms for booking and workout logging follow standard Flask form submission patterns to the same route.

This design specification enables backend and frontend teams to independently build a complete GymMembership application.
