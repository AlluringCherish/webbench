# GymMembership Web Application Design Specification

---

## Section 1: Flask Routes Specification

### 1. Root Route
- **Route Path:** `/`
- **Function Name:** root_redirect
- **HTTP Methods:** GET
- **Purpose:** Redirects to the Dashboard page.
- **Template:** None (redirect)
- **Context Variables:** None

---

### 2. Dashboard Page
- **Route Path:** `/dashboard`
- **Function Name:** dashboard_page
- **HTTP Methods:** GET
- **Template:** `dashboard.html`
- **Context Variables:**
  - `member_status` (str): Status message or welcome info for member highlights.
  - `featured_classes` (list of dict): List of class summaries (name, time, trainer) for highlights.

---

### 3. Membership Plans Page
- **Route Path:** `/memberships`
- **Function Name:** membership_plans_page
- **HTTP Methods:** GET
- **Template:** `memberships.html`
- **Context Variables:**
  - `membership_plans` (list of dict): Each dict includes fields:
    - `membership_id` (int)
    - `plan_name` (str)
    - `price` (str)
    - `billing_cycle` (str)
    - `features` (str)
    - `max_classes` (str)

---

### 4. Plan Details Page (Dynamic)
- **Route Path:** `/plan/<int:plan_id>`
- **Function Name:** plan_details_page
- **HTTP Methods:** GET
- **Template:** `plan_details.html`
- **Context Variables:**
  - `plan` (dict): Detailed membership plan data with same fields as above
  - `plan_reviews` (list of dict): List of reviews for this plan; each dict with review text and reviewer info (if any)

---

### 5. Class Schedule Page
- **Route Path:** `/schedule`
- **Function Name:** class_schedule_page
- **HTTP Methods:** GET
- **Template:** `schedule.html`
- **Context Variables:**
  - `classes` (list of dict): Each dict containing:
    - `class_id` (int)
    - `class_name` (str)
    - `trainer_id` (int)
    - `class_type` (str)
    - `schedule_day` (str)
    - `schedule_time` (str)
    - `capacity` (int)
    - `duration` (int)

---

### 6. Trainer Profiles Page
- **Route Path:** `/trainers`
- **Function Name:** trainer_profiles_page
- **HTTP Methods:** GET
- **Template:** `trainers.html`
- **Context Variables:**
  - `trainers` (list of dict): Each dict containing:
    - `trainer_id` (int)
    - `name` (str)
    - `specialty` (str)
    - `certifications` (str)
    - `experience_years` (int)
    - `bio` (str)

---

### 7. Trainer Detail Page (Dynamic)
- **Route Path:** `/trainer/<int:trainer_id>`
- **Function Name:** trainer_detail_page
- **HTTP Methods:** GET
- **Template:** `trainer_detail.html`
- **Context Variables:**
  - `trainer` (dict): Detailed trainer info with all fields above
  - `trainer_reviews` (list of dict): Reviews from clients for this trainer

---

### 8. PT Booking Page
- **Route Path:** `/booking`
- **Function Name:** personal_training_booking_page
- **HTTP Methods:** GET, POST
  - GET to render page
  - POST to submit booking form
- **Template:** `booking.html`
- **Context Variables (GET):**
  - `trainers` (list of dict): For dropdown with trainer options (`trainer_id`, `name`)
  - `available_times` (list of str): Time slots available for booking
  - `session_durations` (list of int): Possible session durations [30,60,90]
- **Context Variables (POST):**
  - On successful booking, redirect or success message handled by backend

---

### 9. Workout Records Page
- **Route Path:** `/workouts`
- **Function Name:** workout_records_page
- **HTTP Methods:** GET
- **Template:** `workouts.html`
- **Context Variables:**
  - `workouts` (list of dict): Each workout record containing:
    - `workout_id` (int)
    - `workout_type` (str)
    - `workout_date` (str)
    - `duration_minutes` (int)
    - `calories_burned` (int)
    - `notes` (str)
  - `filter_types` (list of str): Workout types for filtering (Class, PT Session, Personal)

---

### 10. Log Workout Page
- **Route Path:** `/log-workout`
- **Function Name:** log_workout_page
- **HTTP Methods:** GET, POST
  - GET to render log form
  - POST to submit new workout record
- **Template:** `log_workout.html`
- **Context Variables (GET):**
  - `workout_types` (list of str): [Cardio, Strength, Flexibility, Sports]
- **Context Variables (POST):**
  - On successful submission, handle redirect or confirmation

---

## Section 2: HTML Template Specifications

### 1. dashboard.html
- **Page Title:** Gym Membership Dashboard
- **Element IDs:**
  - `dashboard-page` (Div): Container for dashboard
  - `member-welcome` (Div): Welcome and member status
  - `browse-membership-button` (Button): Navigates to `membership_plans_page`
  - `view-schedule-button` (Button): Navigates to `class_schedule_page`
  - `book-trainer-button` (Button): Navigates to `personal_training_booking_page`
- **Context Variables:**
  - `member_status` (str): Displayed inside `member-welcome`
  - `featured_classes` (list): Loop to show featured classes summary
- **Navigation:** Buttons use `url_for('function_name')` for links

---

### 2. memberships.html
- **Page Title:** Membership Plans
- **Element IDs:**
  - `membership-page` (Div): Container
  - `plan-filter` (Dropdown): Filter plans by type
  - `plans-grid` (Div): Grid container for membership cards
  - `view-details-button-{membership_id}` (Button): Button on each plan card to view details
  - `back-to-dashboard` (Button): Navigates to dashboard_page
- **Context Variables:**
  - `membership_plans` (list): Loop through plans, each `plan` dict with plan data
- **Navigation:**
  - Filter affects displayed plans client-side
  - Buttons use `url_for()` routes

---

### 3. plan_details.html
- **Page Title:** Plan Details
- **Element IDs:**
  - `plan-details-page` (Div): Container
  - `plan-title` (H1): Displays `plan['plan_name']`
  - `plan-price` (Div): Displays `plan['price']` and `plan['billing_cycle']`
  - `plan-features` (Div): Lists features
  - `enroll-plan-button` (Button): To enroll (no backend specified for action)
  - `plan-reviews` (Div): Shows reviews looped from `plan_reviews`
- **Context Variables:**
  - `plan` (dict): Detailed plan info
  - `plan_reviews` (list): Reviews for plan

---

### 4. schedule.html
- **Page Title:** Class Schedule
- **Element IDs:**
  - `schedule-page` (Div): Container
  - `schedule-search` (Input): Text input to search classes
  - `schedule-filter` (Dropdown): Filter by class type
  - `classes-grid` (Div): Grid of class cards
  - `enroll-class-button-{class_id}` (Button): To enroll in each class
- **Context Variables:**
  - `classes` (list): Loop of class dicts
- **Navigation:**
  - Enrollment buttons linked to potential enrollment POST or placeholder

---

### 5. trainers.html
- **Page Title:** Trainer Profiles
- **Element IDs:**
  - `trainers-page` (Div): Container
  - `trainer-search` (Input): Search input
  - `specialty-filter` (Dropdown): Filter by specialty
  - `trainers-grid` (Div): Trainer cards grid
  - `view-trainer-button-{trainer_id}` (Button): Button to view trainer detail
- **Context Variables:**
  - `trainers` (list): Loop with trainer dicts

---

### 6. trainer_detail.html
- **Page Title:** Trainer Profile
- **Element IDs:**
  - `trainer-detail-page` (Div): Container
  - `trainer-name` (H1): Displays trainer.name
  - `trainer-bio` (Div): Trainer biography
  - `trainer-certifications` (Div): Certifications
  - `book-session-button` (Button): For booking session
  - `trainer-reviews` (Div): Reviews loop
- **Context Variables:**
  - `trainer` (dict): Trainer info
  - `trainer_reviews` (list): Client reviews

---

### 7. booking.html
- **Page Title:** Book Personal Training
- **Element IDs:**
  - `booking-page` (Div): Container
  - `select-trainer` (Dropdown): Select trainer
  - `session-date` (Input - date): Date picker
  - `session-time` (Dropdown): Time slot selection
  - `session-duration` (Dropdown): Duration selection
  - `confirm-booking-button` (Button): Submit booking
- **Context Variables:**
  - `trainers` (list): Loop options for trainers
  - `available_times` (list of str): Times
  - `session_durations` (list of int): [30,60,90]

---

### 8. workouts.html
- **Page Title:** My Workout Records
- **Element IDs:**
  - `workouts-page` (Div): Container
  - `workouts-table` (Table): Display workout records
  - `filter-by-type` (Dropdown): Filter workouts by type
  - `log-workout-button` (Button): Navigate to log workout page
  - `back-to-dashboard` (Button): Navigate back to dashboard
- **Context Variables:**
  - `workouts` (list): Loop for table rows
  - `filter_types` (list): Dropdown options

---

### 9. log_workout.html
- **Page Title:** Log Workout
- **Element IDs:**
  - `log-workout-page` (Div): Container
  - `workout-type` (Dropdown): Select workout type
  - `workout-duration` (Input - number): Duration input
  - `calories-burned` (Input - number): Calories input
  - `workout-notes` (Textarea): Notes field
  - `submit-workout-button` (Button): Submit button
- **Context Variables:**
  - `workout_types` (list): Dropdown options

---

## Section 3: Data File Schemas

### 1. Memberships Data
- **File Path:** `data/memberships.txt`
- **Field Order:**
  1. membership_id (int)
  2. plan_name (str)
  3. price (str)  # Stored as string with decimal format
  4. billing_cycle (str)
  5. features (str)
  6. max_classes (str)  # Numeric or "unlimited"
- **Description:** Contains all membership plans available with details and limits.
- **Example Data:**
```
1|Basic|29.99|monthly|Gym access, 2 classes per week|8
2|Premium|59.99|monthly|Gym access, 5 classes per week, 2 PT sessions|20
3|Elite|99.99|monthly|Unlimited gym access, unlimited classes, 4 PT sessions, nutrition coaching|unlimited
```

---

### 2. Classes Data
- **File Path:** `data/classes.txt`
- **Field Order:**
  1. class_id (int)
  2. class_name (str)
  3. trainer_id (int)
  4. class_type (str)
  5. schedule_day (str)
  6. schedule_time (str)
  7. capacity (int)
  8. duration (int)
- **Description:** Contains all fitness classes available with schedule and instructor.
- **Example Data:**
```
1|Morning Yoga|1|Yoga|Monday|06:00|20|60
2|CrossFit Bootcamp|2|CrossFit|Tuesday|18:00|15|45
3|Pilates Core|3|Pilates|Wednesday|10:00|18|50
```

---

### 3. Trainers Data
- **File Path:** `data/trainers.txt`
- **Field Order:**
  1. trainer_id (int)
  2. name (str)
  3. specialty (str)
  4. certifications (str)
  5. experience_years (int)
  6. bio (str)
- **Description:** Contains all trainer profiles with expertise and biographies.
- **Example Data:**
```
1|Sarah Johnson|Yoga & Flexibility|Certified Yoga Instructor, CPR|8|Expert in mind-body wellness and injury prevention
2|Mike Thompson|Strength & Conditioning|NASM-CPT, CrossFit Level 2|10|Specializes in powerlifting and functional fitness
3|Emma Davis|Pilates|Pilates Method Alliance Certified|6|Focus on core strength and postural alignment
```

---

### 4. Bookings Data
- **File Path:** `data/bookings.txt`
- **Field Order:**
  1. booking_id (int)
  2. member_name (str)
  3. trainer_id (int)
  4. booking_date (str, format YYYY-MM-DD)
  5. booking_time (str, HH:MM)
  6. duration_minutes (int)
  7. status (str)
- **Description:** Contains all personal training bookings with status.
- **Example Data:**
```
1|John Doe|1|2025-01-20|10:00|60|Confirmed
2|Jane Smith|2|2025-01-21|14:00|45|Confirmed
3|Alex Johnson|3|2025-01-22|16:00|60|Pending
```

---

### 5. Workouts Data
- **File Path:** `data/workouts.txt`
- **Field Order:**
  1. workout_id (int)
  2. member_name (str)
  3. workout_type (str)
  4. workout_date (str, format YYYY-MM-DD)
  5. duration_minutes (int)
  6. calories_burned (int)
  7. notes (str)
- **Description:** Contains all logged user workout records.
- **Example Data:**
```
1|John Doe|Cardio|2025-01-15|45|350|Morning run on treadmill
2|Jane Smith|Strength|2025-01-16|60|420|Upper body weight training with trainer
3|Alex Johnson|Class|2025-01-17|50|380|CrossFit Bootcamp session
```

---

# End of Design Specification
