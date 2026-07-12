# GymMembership Web Application Design Specification

---

## Section 1: Flask Routes Specification

### 1. Root Route
- **Route Path:** `/`
- **Function Name:** root_redirect
- **HTTP Methods:** GET
- **Action:** Redirects to `/dashboard`
- **Template:** None (redirect)
- **Context Variables:** None

### 2. Dashboard Page
- **Route Path:** `/dashboard`
- **Function Name:** dashboard
- **HTTP Methods:** GET
- **Template:** `dashboard.html`
- **Context Variables:**
  - `member_status` (str): Display member welcome/status info
  - Optional example context: featured_classes (list of dict), member_highlights (list of str)

### 3. Membership Plans Page
- **Route Path:** `/memberships`
- **Function Name:** memberships
- **HTTP Methods:** GET
- **Template:** `memberships.html`
- **Context Variables:**
  - `memberships` (list of dict): Each dict with keys - `membership_id` (int), `plan_name` (str), `price` (str), `billing_cycle` (str), `features` (str), `max_classes` (str or int)
  - `filter_options` (list of str): Membership types -- e.g. ["Basic", "Premium", "Elite"] for filter dropdown

### 4. Plan Details Page
- **Route Path:** `/plan/<int:plan_id>`
- **Function Name:** plan_details
- **HTTP Methods:** GET
- **Template:** `plan_details.html`
- **Context Variables:**
  - `plan` (dict): Detailed membership plan info with keys - `membership_id` (int), `plan_name` (str), `price` (str), `billing_cycle` (str), `features` (str), `max_classes` (str or int)
  - `reviews` (list of dict): Member reviews related to the plan (if applicable) with fields like `review_text` (str), `member_name` (str)

### 5. Class Schedule Page
- **Route Path:** `/schedule`
- **Function Name:** class_schedule
- **HTTP Methods:** GET
- **Template:** `schedule.html`
- **Context Variables:**
  - `classes` (list of dict): Each dict representing a class with keys - `class_id` (int), `class_name` (str), `trainer_id` (int), `class_type` (str), `schedule_day` (str), `schedule_time` (str), `capacity` (int), `duration` (int)
  - `class_types` (list of str): Options for class type filter (e.g., Yoga, CrossFit, Pilates, Boxing)

### 6. Trainer Profiles Page
- **Route Path:** `/trainers`
- **Function Name:** trainers
- **HTTP Methods:** GET
- **Template:** `trainers.html`
- **Context Variables:**
  - `trainers` (list of dict): Each dict with keys - `trainer_id` (int), `name` (str), `specialty` (str), `certifications` (str), `experience_years` (int), `bio` (str)
  - `specialties` (list of str): Filter options for specialties (e.g. Strength, Cardio, Flexibility, Weight Loss)

### 7. Trainer Detail Page
- **Route Path:** `/trainer/<int:trainer_id>`
- **Function Name:** trainer_detail
- **HTTP Methods:** GET
- **Template:** `trainer_detail.html`
- **Context Variables:**
  - `trainer` (dict): Detailed trainer info with keys - `trainer_id` (int), `name` (str), `specialty` (str), `certifications` (str), `experience_years` (int), `bio` (str)
  - `reviews` (list of dict): Reviews for that trainer with fields like `review_text` (str), `client_name` (str)

### 8. Personal Training Booking Page
- **Route Path:** `/booking`
- **Function Name:** booking
- **HTTP Methods:** GET, POST
- **Template:** `booking.html`
- **Context Variables:**
  - GET: 
    - `trainers` (list of dict): Each dict with keys - `trainer_id` (int), `name` (str)
  - POST: Processes booking form submission (trainer selection, date, time, duration), redirects or returns status

### 9. Workout Records Page
- **Route Path:** `/workouts`
- **Function Name:** workouts
- **HTTP Methods:** GET
- **Template:** `workouts.html`
- **Context Variables:**
  - `workouts` (list of dict): Each dict with keys - `workout_id` (int), `member_name` (str), `workout_type` (str), `workout_date` (str), `duration_minutes` (int), `calories_burned` (int), `notes` (str)
  - `workout_types` (list of str): Filter options (Class, PT Session, Personal)

### 10. Log Workout Page
- **Route Path:** `/log_workout`
- **Function Name:** log_workout
- **HTTP Methods:** GET, POST
- **Template:** `log_workout.html`
- **Context Variables:**
  - GET: None or minimal data to populate dropdown for workout types
  - POST: Processes form submission, adds new workout record

---

## Section 2: HTML Template Specifications

### 1. dashboard.html
- **Page Title:** Gym Membership Dashboard
- **Element IDs:**
  - `dashboard-page` (Div): Container for dashboard content
  - `member-welcome` (Div): Member status/welcome message
  - `browse-membership-button` (Button): Navigate to memberships page (`url_for('memberships')`)
  - `view-schedule-button` (Button): Navigate to schedule page (`url_for('class_schedule')`)
  - `book-trainer-button` (Button): Navigate to booking page (`url_for('booking')`)
- **Context Variables:**
  - `member_status` (str)
  - Optional featured classes or highlights can be shown
- **Navigation:** Buttons with IDs linked to routes as above

### 2. memberships.html
- **Page Title:** Membership Plans
- **Element IDs:**
  - `membership-page` (Div): Container
  - `plan-filter` (Dropdown): Filter membership plans by type; options from `filter_options`
  - `plans-grid` (Div): Grid containing membership plan cards
  - `view-details-button-{plan_id}` (Button): For each plan card, navigates to plan details page for that plan
  - `back-to-dashboard` (Button): Navigates back to dashboard
- **Context Variables:**
  - `memberships` (list of dict): Loop to display cards
  - `filter_options` (list of str)
- **Navigation:**
  - Back button links to `url_for('dashboard')`
  - View details buttons link to `url_for('plan_details', plan_id=plan.membership_id)`

### 3. plan_details.html
- **Page Title:** Plan Details
- **Element IDs:**
  - `plan-details-page` (Div): Container
  - `plan-title` (H1): Displays `plan.plan_name`
  - `plan-price` (Div): Displays price and billing cycle
  - `plan-features` (Div): Displays `plan.features`
  - `enroll-plan-button` (Button): Button for enrollment (no backend logic specified)
  - `plan-reviews` (Div): Displays reviews loop
- **Context Variables:**
  - `plan` (dict)
  - `reviews` (list of dict)
- **Navigation:**
  - Enroll button (no route specified, likely client-side or future implementation)

### 4. schedule.html
- **Page Title:** Class Schedule
- **Element IDs:**
  - `schedule-page` (Div)
  - `schedule-search` (Input): Search by class name or trainer
  - `schedule-filter` (Dropdown): Filter by class type; options from `class_types`
  - `classes-grid` (Div): Grid to display class cards
  - `enroll-class-button-{class_id}` (Button): For each class card, to enroll (no backend enrollment logic specified)
- **Context Variables:**
  - `classes` (list of dict)
  - `class_types` (list of str)
- **Navigation:**
  - Enroll buttons can trigger JavaScript or form submission

### 5. trainers.html
- **Page Title:** Trainer Profiles
- **Element IDs:**
  - `trainers-page` (Div)
  - `trainer-search` (Input): Search trainers
  - `specialty-filter` (Dropdown): Filter by specialty from `specialties`
  - `trainers-grid` (Div): Grid for trainer cards
  - `view-trainer-button-{trainer_id}` (Button): View trainer detail page
- **Context Variables:**
  - `trainers` (list of dict)
  - `specialties` (list of str)
- **Navigation:**
  - View trainer buttons link to `url_for('trainer_detail', trainer_id=trainer.trainer_id)`

### 6. trainer_detail.html
- **Page Title:** Trainer Profile
- **Element IDs:**
  - `trainer-detail-page` (Div)
  - `trainer-name` (H1)
  - `trainer-bio` (Div)
  - `trainer-certifications` (Div)
  - `book-session-button` (Button): To book session with this trainer, links to booking page possibly with trainer preselected
  - `trainer-reviews` (Div): Displays client reviews
- **Context Variables:**
  - `trainer` (dict)
  - `reviews` (list of dict)
- **Navigation:**
  - Book session button links to `url_for('booking')` with optional query parameter for trainer

### 7. booking.html
- **Page Title:** Book Personal Training
- **Element IDs:**
  - `booking-page` (Div)
  - `select-trainer` (Dropdown): Options from trainers
  - `session-date` (Input, date)
  - `session-time` (Dropdown): Preset time slots (e.g., 6:00, 7:00, etc.)
  - `session-duration` (Dropdown): Options (30, 60, 90)
  - `confirm-booking-button` (Button): Submit booking form
- **Context Variables:**
  - `trainers` (list of dict)
- **Navigation:**
  - Confirm button triggers POST to same route

### 8. workouts.html
- **Page Title:** My Workout Records
- **Element IDs:**
  - `workouts-page` (Div)
  - `workouts-table` (Table): Displays workout history with columns for date, type, duration, calories
  - `filter-by-type` (Dropdown): Filter workouts by type from `workout_types`
  - `log-workout-button` (Button): Navigate to log workout page
  - `back-to-dashboard` (Button): Navigate to dashboard
- **Context Variables:**
  - `workouts` (list of dict)
  - `workout_types` (list of str)
- **Navigation:**
  - Log workout button links to `url_for('log_workout')`
  - Back button links to `url_for('dashboard')`

### 9. log_workout.html
- **Page Title:** Log Workout
- **Element IDs:**
  - `log-workout-page` (Div)
  - `workout-type` (Dropdown): Options include Cardio, Strength, Flexibility, Sports
  - `workout-duration` (Input, number)
  - `calories-burned` (Input, number)
  - `workout-notes` (Textarea)
  - `submit-workout-button` (Button): Submit workout record
- **Context Variables:** None or minimal for dropdown options
- **Navigation:** Submit button triggers POST

---

## Section 3: Data File Schemas

### 1. Memberships Data
- **File Path:** `data/memberships.txt`
- **Fields Order (pipe-delimited):**
  - `membership_id` (int)
  - `plan_name` (str)
  - `price` (str) - e.g., "29.99"
  - `billing_cycle` (str) - e.g., "monthly"
  - `features` (str) - comma-separated features
  - `max_classes` (int or str - "unlimited")
- **Description:** Stores available membership plans with pricing and features.
- **Example Data:**
  ```
  1|Basic|29.99|monthly|Gym access, 2 classes per week|8
  2|Premium|59.99|monthly|Gym access, 5 classes per week, 2 PT sessions|20
  3|Elite|99.99|monthly|Unlimited gym access, unlimited classes, 4 PT sessions, nutrition coaching|unlimited
  ```

### 2. Classes Data
- **File Path:** `data/classes.txt`
- **Fields Order (pipe-delimited):**
  - `class_id` (int)
  - `class_name` (str)
  - `trainer_id` (int)
  - `class_type` (str)
  - `schedule_day` (str) - e.g., "Monday"
  - `schedule_time` (str) - 24hr format, e.g., "06:00"
  - `capacity` (int)
  - `duration` (int) - minutes
- **Description:** Stores scheduled fitness classes information.
- **Example Data:**
  ```
  1|Morning Yoga|1|Yoga|Monday|06:00|20|60
  2|CrossFit Bootcamp|2|CrossFit|Tuesday|18:00|15|45
  3|Pilates Core|3|Pilates|Wednesday|10:00|18|50
  ```

### 3. Trainers Data
- **File Path:** `data/trainers.txt`
- **Fields Order (pipe-delimited):**
  - `trainer_id` (int)
  - `name` (str)
  - `specialty` (str)
  - `certifications` (str)
  - `experience_years` (int)
  - `bio` (str)
- **Description:** Stores trainer profiles and credentials.
- **Example Data:**
  ```
  1|Sarah Johnson|Yoga & Flexibility|Certified Yoga Instructor, CPR|8|Expert in mind-body wellness and injury prevention
  2|Mike Thompson|Strength & Conditioning|NASM-CPT, CrossFit Level 2|10|Specializes in powerlifting and functional fitness
  3|Emma Davis|Pilates|Pilates Method Alliance Certified|6|Focus on core strength and postural alignment
  ```

### 4. Bookings Data
- **File Path:** `data/bookings.txt`
- **Fields Order (pipe-delimited):**
  - `booking_id` (int)
  - `member_name` (str)
  - `trainer_id` (int)
  - `booking_date` (str) - ISO format YYYY-MM-DD
  - `booking_time` (str) - 24hr format HH:MM
  - `duration_minutes` (int)
  - `status` (str) - e.g., Confirmed, Pending
- **Description:** Stores personal training session bookings.
- **Example Data:**
  ```
  1|John Doe|1|2025-01-20|10:00|60|Confirmed
  2|Jane Smith|2|2025-01-21|14:00|45|Confirmed
  3|Alex Johnson|3|2025-01-22|16:00|60|Pending
  ```

### 5. Workouts Data
- **File Path:** `data/workouts.txt`
- **Fields Order (pipe-delimited):**
  - `workout_id` (int)
  - `member_name` (str)
  - `workout_type` (str)
  - `workout_date` (str) - ISO format YYYY-MM-DD
  - `duration_minutes` (int)
  - `calories_burned` (int)
  - `notes` (str)
- **Description:** Stores personal workout records.
- **Example Data:**
  ```
  1|John Doe|Cardio|2025-01-15|45|350|Morning run on treadmill
  2|Jane Smith|Strength|2025-01-16|60|420|Upper body weight training with trainer
  3|Alex Johnson|Class|2025-01-17|50|380|CrossFit Bootcamp session
  ```

---

This design specification enables backend developers to implement Flask routes and data parsing exactly, and frontend developers to build consistent HTML templates and navigation. All element IDs, variable names, and context variables are aligned for smooth parallel development.
