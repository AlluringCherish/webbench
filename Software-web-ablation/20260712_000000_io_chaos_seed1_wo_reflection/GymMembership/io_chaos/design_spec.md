# GymMembership Web Application Design Specification

---

## Section 1: Flask Routes Specification

| Route Path              | Function Name           | HTTP Method(s) | Template File         | Context Variables Passed to Template                                           |
|-------------------------|------------------------|----------------|-----------------------|-------------------------------------------------------------------------------|
| /                       | root_redirect           | GET            | None (Redirect)       | None (Redirects to /dashboard)                                                |
| /dashboard              | dashboard_page          | GET            | dashboard.html        | None                                                                          |
| /memberships            | memberships_page        | GET            | memberships.html      | memberships: list of dict (each membership plan with all fields)             |
| /plan/<int:plan_id>     | plan_details_page       | GET            | plan_details.html     | plan: dict (membership plan details), reviews: list of dict (plan reviews)   |
| /classes                | class_schedule_page     | GET            | class_schedule.html   | classes: list of dict (all class entries), filter_types: list of str          |
| /trainers               | trainer_profiles_page   | GET            | trainer_profiles.html | trainers: list of dict (all trainers), specialties: list of str               |
| /trainer/<int:trainer_id>| trainer_detail_page    | GET            | trainer_detail.html   | trainer: dict (trainer details), reviews: list of dict (trainer client reviews)|
| /booking                | pt_booking_page         | GET, POST      | booking.html          | GET: trainers: list of dict (all trainers)
POST: booking_status: str (success/fail message) |
| /workouts               | workout_records_page    | GET            | workouts.html         | workouts: list of dict (user workout records), workout_types: list of str     |
| /logworkout             | log_workout_page        | GET, POST      | log_workout.html      | GET: None
POST: workout_log_status: str (success/fail message)                     |

### Details:
- Root route `/` redirects (HTTP 302) to `/dashboard`.
- `plan_details_page` dynamic route with parameter `plan_id` int.
- `trainer_detail_page` dynamic route with parameter `trainer_id` int.
- `booking_page` supports GET (to render booking form) and POST (to submit booking).
- `log_workout_page` supports GET (form display) and POST (form submission).


## Section 2: HTML Template Specifications

### 1. Dashboard Page
- Filename: `dashboard.html`
- Page Title: Gym Membership Dashboard
- Elements:
  - ID: dashboard-page (Div) - Container for dashboard
  - ID: member-welcome (Div) - Member welcome/status
  - ID: browse-membership-button (Button) - Navigate to `/memberships`
  - ID: view-schedule-button (Button) - Navigate to `/classes`
  - ID: book-trainer-button (Button) - Navigate to `/booking`
- Context Variables: None
- Navigation and Buttons:
  - Buttons use Flask `url_for()` with endpoints: `memberships_page`, `class_schedule_page`, `pt_booking_page`

### 2. Membership Plans Page
- Filename: `memberships.html`
- Page Title: Membership Plans
- Elements:
  - ID: membership-page (Div) - Container
  - ID: plan-filter (Dropdown) - Filter by membership type ['Basic', 'Premium', 'Elite']
  - ID: plans-grid (Div) - Grid of membership plan cards
  - ID pattern: view-details-button-{plan_id} (Button) - View plan details
  - ID: back-to-dashboard (Button) - Navigate to `/dashboard`
- Context Variables:
  - memberships: list of dict, each with keys: membership_id (int), plan_name (str), price (str), billing_cycle (str), features (str), max_classes (str/int)
- Navigation:
  - back-to-dashboard button: `url_for('dashboard_page')`
  - view-details-button-{plan_id}: links to `url_for('plan_details_page', plan_id=plan_id)`

### 3. Plan Details Page
- Filename: `plan_details.html`
- Page Title: Plan Details
- Elements:
  - ID: plan-details-page (Div) - Container
  - ID: plan-title (H1) - Plan name
  - ID: plan-price (Div) - Plan price and billing cycle
  - ID: plan-features (Div) - Features list
  - ID: enroll-plan-button (Button) - Enroll in plan (link or action)
  - ID: plan-reviews (Div) - Member reviews of plan
- Context Variables:
  - plan: dict with keys membership_id (int), plan_name (str), price (str), billing_cycle (str), features (str), max_classes (str/int)
  - reviews: list of dict (content format not specified but assumed list of review strings or dicts)
- Navigation:
  - enroll-plan-button: may trigger POST or redirect (implementation detail, no explicit route given)

### 4. Class Schedule Page
- Filename: `class_schedule.html`
- Page Title: Class Schedule
- Elements:
  - ID: schedule-page (Div) - Container
  - ID: schedule-search (Input) - Search classes by name or trainer
  - ID: schedule-filter (Dropdown) - Filter by class type
  - ID: classes-grid (Div) - Grid of class cards
  - ID pattern: enroll-class-button-{class_id} (Button) - Enroll in class
- Context Variables:
  - classes: list of dict with keys: class_id (int), class_name (str), trainer_id (int), class_type (str), schedule_day (str), schedule_time (str), capacity (int), duration (int)
  - filter_types: list of str for dropdown options (e.g. Yoga, CrossFit, Pilates, Boxing, etc.)
- Navigation:
  - enroll-class-button-{class_id} buttons: action to enroll (no explicit route defined, presumably POST or client action)

### 5. Trainer Profiles Page
- Filename: `trainer_profiles.html`
- Page Title: Trainer Profiles
- Elements:
  - ID: trainers-page (Div) - Container
  - ID: trainer-search (Input) - Search by name or specialty
  - ID: specialty-filter (Dropdown) - Filter by specialty type
  - ID: trainers-grid (Div) - Grid of trainer cards
  - ID pattern: view-trainer-button-{trainer_id} (Button) - View trainer profile
- Context Variables:
  - trainers: list of dict with keys: trainer_id (int), name (str), specialty (str), certifications (str), experience_years (int), bio (str)
  - specialties: list of str - e.g. ['Strength', 'Cardio', 'Flexibility', 'Weight Loss']
- Navigation:
  - view-trainer-button-{trainer_id} links to `url_for('trainer_detail_page', trainer_id=trainer_id)`

### 6. Trainer Detail Page
- Filename: `trainer_detail.html`
- Page Title: Trainer Profile
- Elements:
  - ID: trainer-detail-page (Div) - Container
  - ID: trainer-name (H1) - Trainer name
  - ID: trainer-bio (Div) - Biography and experience
  - ID: trainer-certifications (Div) - Certifications
  - ID: book-session-button (Button) - Book session with trainer
  - ID: trainer-reviews (Div) - Client reviews
- Context Variables:
  - trainer: dict with keys: trainer_id (int), name (str), specialty (str), certifications (str), experience_years (int), bio (str)
  - reviews: list of dict (review content format not explicitly defined)
- Navigation:
  - book-session-button: link to `url_for('pt_booking_page')` with possibly pre-selected trainer (implementation detail)

### 7. PT Booking Page
- Filename: `booking.html`
- Page Title: Book Personal Training
- Elements:
  - ID: booking-page (Div) - Container
  - ID: select-trainer (Dropdown) - Select a trainer
  - ID: session-date (Input date) - Date picker
  - ID: session-time (Dropdown) - Time slot selection
  - ID: session-duration (Dropdown) - Duration selection (30, 60, 90 minutes)
  - ID: confirm-booking-button (Button) - Confirm booking
- Context Variables:
  - trainers: list of dict (trainer_id, name, potentially other fields)
  - booking_status (POST response): str indicating result
- Navigation:
  - confirm-booking-button triggers POST to `/booking`

### 8. Workout Records Page
- Filename: `workouts.html`
- Page Title: My Workout Records
- Elements:
  - ID: workouts-page (Div) - Container
  - ID: workouts-table (Table) - Workout history (columns: date, type, duration, calories)
  - ID: filter-by-type (Dropdown) - Filter by workout type
  - ID: log-workout-button (Button) - Navigate to `/logworkout`
  - ID: back-to-dashboard (Button) - Navigate to `/dashboard`
- Context Variables:
  - workouts: list of dict with keys: workout_id (int), member_name (str), workout_type (str), workout_date (str), duration_minutes (int), calories_burned (int), notes (str)
  - workout_types: list of str e.g. ['Class', 'PT Session', 'Personal']
- Navigation:
  - log-workout-button: `url_for('log_workout_page')`
  - back-to-dashboard button: `url_for('dashboard_page')`

### 9. Log Workout Page
- Filename: `log_workout.html`
- Page Title: Log Workout
- Elements:
  - ID: log-workout-page (Div) - Container
  - ID: workout-type (Dropdown) - Select workout type ['Cardio', 'Strength', 'Flexibility', 'Sports']
  - ID: workout-duration (Input number) - Duration in minutes
  - ID: calories-burned (Input number) - Estimated calories
  - ID: workout-notes (Textarea) - Notes
  - ID: submit-workout-button (Button) - Submit workout
- Context Variables:
  - None for GET
  - 'workout_log_status': str for POST result message
- Navigation:
  - submit-workout-button triggers POST to `/logworkout`


## Section 3: Data File Schemas

### 1. Memberships Data
- File Path: `data/memberships.txt`
- Field Order (pipe-delimited):
  1. membership_id (int)
  2. plan_name (str)
  3. price (str)  # stored as string with decimal
  4. billing_cycle (str)
  5. features (str)
  6. max_classes (str or int) # "unlimited" or int
- Description: Stores all membership plan details including pricing and features.
- Example Data:
  ```
  1|Basic|29.99|monthly|Gym access, 2 classes per week|8
  2|Premium|59.99|monthly|Gym access, 5 classes per week, 2 PT sessions|20
  3|Elite|99.99|monthly|Unlimited gym access, unlimited classes, 4 PT sessions, nutrition coaching|unlimited
  ```

### 2. Classes Data
- File Path: `data/classes.txt`
- Field Order (pipe-delimited):
  1. class_id (int)
  2. class_name (str)
  3. trainer_id (int)
  4. class_type (str)
  5. schedule_day (str)
  6. schedule_time (str) # HH:MM
  7. capacity (int)
  8. duration (int) # minutes
- Description: Contains all scheduled fitness classes with trainer assignment.
- Example Data:
  ```
  1|Morning Yoga|1|Yoga|Monday|06:00|20|60
  2|CrossFit Bootcamp|2|CrossFit|Tuesday|18:00|15|45
  3|Pilates Core|3|Pilates|Wednesday|10:00|18|50
  ```

### 3. Trainers Data
- File Path: `data/trainers.txt`
- Field Order (pipe-delimited):
  1. trainer_id (int)
  2. name (str)
  3. specialty (str)
  4. certifications (str)
  5. experience_years (int)
  6. bio (str)
- Description: Contains profiles of all trainers with expertise and biography.
- Example Data:
  ```
  1|Sarah Johnson|Yoga & Flexibility|Certified Yoga Instructor, CPR|8|Expert in mind-body wellness and injury prevention
  2|Mike Thompson|Strength & Conditioning|NASM-CPT, CrossFit Level 2|10|Specializes in powerlifting and functional fitness
  3|Emma Davis|Pilates|Pilates Method Alliance Certified|6|Focus on core strength and postural alignment
  ```

### 4. Bookings Data
- File Path: `data/bookings.txt`
- Field Order (pipe-delimited):
  1. booking_id (int)
  2. member_name (str)
  3. trainer_id (int)
  4. booking_date (str) # YYYY-MM-DD
  5. booking_time (str) # HH:MM
  6. duration_minutes (int)
  7. status (str) # e.g., Confirmed, Pending
- Description: Stores personal training session bookings.
- Example Data:
  ```
  1|John Doe|1|2025-01-20|10:00|60|Confirmed
  2|Jane Smith|2|2025-01-21|14:00|45|Confirmed
  3|Alex Johnson|3|2025-01-22|16:00|60|Pending
  ```

### 5. Workouts Data
- File Path: `data/workouts.txt`
- Field Order (pipe-delimited):
  1. workout_id (int)
  2. member_name (str)
  3. workout_type (str)
  4. workout_date (str) # YYYY-MM-DD
  5. duration_minutes (int)
  6. calories_burned (int)
  7. notes (str)
- Description: Records of all user workout sessions.
- Example Data:
  ```
  1|John Doe|Cardio|2025-01-15|45|350|Morning run on treadmill
  2|Jane Smith|Strength|2025-01-16|60|420|Upper body weight training with trainer
  3|Alex Johnson|Class|2025-01-17|50|380|CrossFit Bootcamp session
  ```

---

**End of design_spec.md**
