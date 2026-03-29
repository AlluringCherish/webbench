# GymMembership Web Application Design Specification

---

## Section 1: Flask Routes Specification

| Route Path             | Function Name           | HTTP Method(s) | Template Filename     | Context Variables                                                                                      |
|------------------------|-------------------------|----------------|-----------------------|------------------------------------------------------------------------------------------------------|
| /                      | root_redirect            | GET            | None (Redirect to /dashboard) | None                                                                                                 |
| /dashboard             | dashboard               | GET            | dashboard.html         | None (static content except navigation buttons)                                                     |
| /memberships           | memberships             | GET            | memberships.html       | plans: list of dict {membership_id (int), plan_name (str), price (float), billing_cycle (str), features (str), max_classes (str|int)} |
| /plan/<int:plan_id>    | plan_details            | GET            | plan_details.html      | plan: dict {membership_id (int), plan_name (str), price (float), billing_cycle (str), features (str), max_classes (str|int)}
|                        |                         |                |                       | reviews: list of dict (optional, if review feature is supported; but user requirements specify only display; assume empty list)     |
| /schedule              | class_schedule          | GET            | class_schedule.html    | classes: list of dict {class_id (int), class_name (str), trainer_id (int), class_type (str), schedule_day (str), schedule_time (str), capacity (int), duration (int)} |
| /trainers              | trainers                | GET            | trainers.html          | trainers: list of dict {trainer_id (int), name (str), specialty (str), certifications (str), experience_years (int), bio (str)}     |
| /trainer/<int:trainer_id> | trainer_detail      | GET            | trainer_detail.html    | trainer: dict {trainer_id (int), name (str), specialty (str), certifications (str), experience_years (int), bio (str)}
|                        |                         |                |                       | reviews: list of dict (optional; user requirement mentions client reviews section; assume empty or external source)                 |
| /booking               | booking                 | GET, POST      | booking.html           | GET: trainers: list of dict (as above)
|                        |                         |                |                       | POST: form data: select_trainer(int), session_date(str), session_time(str), session_duration(int)
|                        |                         |                |                       | POST: confirmation status (bool or str message) to template for feedback if re-rendering
| /workouts              | workout_records         | GET            | workouts.html          | workouts: list of dict {workout_id (int), member_name (str), workout_type (str), workout_date(str), duration_minutes(int), calories_burned(int), notes(str)}              |
| /log_workout           | log_workout             | GET, POST      | log_workout.html       | GET: None
|                        |                         |                |                       | POST: form data: workout_type(str), workout_duration(int), calories_burned(int), workout_notes(str)
|                        |                         |                |                       | POST: submission status feedback (bool or str message) if re-rendering

Notes:
- The root route `/` redirects to `/dashboard` as per specification.
- POST method is defined only on pages that require form submissions: booking and log workout.
- Each detail page uses dynamic route parameters for plan_id and trainer_id.


---

## Section 2: HTML Template Specifications

### 1. dashboard.html
- Page Title: Gym Membership Dashboard
- Container Div ID: dashboard-page
- Elements:
  - Div ID: member-welcome (Welcome section with member status information)
  - Button ID: browse-membership-button (Navigate to /memberships)
  - Button ID: view-schedule-button (Navigate to /schedule)
  - Button ID: book-trainer-button (Navigate to /booking)
- Navigation Buttons:
  - browse-membership-button → url_for('memberships')
  - view-schedule-button → url_for('class_schedule')
  - book-trainer-button → url_for('booking')
- Context Variables: None (static content)


### 2. memberships.html
- Page Title: Membership Plans
- Container Div ID: membership-page
- Elements:
  - Dropdown ID: plan-filter (filter by membership type: Basic, Premium, Elite)
  - Div ID: plans-grid (grid displaying membership plan cards)
  - Each Plan Card:
    - Button ID: view-details-button-{{ plan.membership_id }} (link to /plan/<plan_id>)
  - Button ID: back-to-dashboard (navigate back to /dashboard)
- Navigation Buttons:
  - back-to-dashboard → url_for('dashboard')
- Context Variables:
  - plans: List of dicts
    - Access pattern: {% for plan in plans %} ... {{ plan.plan_name }} ... {% endfor %}


### 3. plan_details.html
- Page Title: Plan Details
- Container Div ID: plan-details-page
- Elements:
  - H1 ID: plan-title (displays plan.plan_name)
  - Div ID: plan-price (displays plan.price and plan.billing_cycle)
  - Div ID: plan-features (displays plan.features as text)
  - Button ID: enroll-plan-button (for enrolling in the plan; no POST route specified so assumed static button)
  - Div ID: plan-reviews (section for member reviews; empty or placeholder)
- Navigation Buttons:
  - None explicitly stated, can navigate via browser back or menu (not specified)
- Context Variables:
  - plan: dict
  - reviews: list (if any, else empty)


### 4. class_schedule.html
- Page Title: Class Schedule
- Container Div ID: schedule-page
- Elements:
  - Input ID: schedule-search (search field for classes by name or trainer)
  - Dropdown ID: schedule-filter (filter by class type)
  - Div ID: classes-grid (grid displaying class cards)
  - Each Class Card:
    - Button ID: enroll-class-button-{{ class.class_id }} (button to enroll in class)
- Navigation Buttons:
  - None specified
- Context Variables:
  - classes: List of dicts
    - Access pattern: {% for class in classes %} ... {{ class.class_name }} ... {{ class.schedule_day }} ... {% endfor %}


### 5. trainers.html
- Page Title: Trainer Profiles
- Container Div ID: trainers-page
- Elements:
  - Input ID: trainer-search (search trainers by name or specialty)
  - Dropdown ID: specialty-filter (filter by specialty)
  - Div ID: trainers-grid (grid of trainer cards)
  - Each Trainer Card:
    - Button ID: view-trainer-button-{{ trainer.trainer_id }} (button to view trainer profile)
- Navigation Buttons:
  - None specified
- Context Variables:
  - trainers: List of dicts
    - Access pattern: {% for trainer in trainers %} ... {{ trainer.name }} ... {{ trainer.specialty }} ... {% endfor %}


### 6. trainer_detail.html
- Page Title: Trainer Profile
- Container Div ID: trainer-detail-page
- Elements:
  - H1 ID: trainer-name (show trainer.name)
  - Div ID: trainer-bio (show trainer.bio)
  - Div ID: trainer-certifications (show trainer.certifications)
  - Button ID: book-session-button (button to book a session; linked to /booking page with pre-selected trainer if implemented frontend logic)
  - Div ID: trainer-reviews (section for client reviews; placeholder or empty)
- Navigation Buttons:
  - None specified
- Context Variables:
  - trainer: dict
  - reviews: list (if any, else empty)


### 7. booking.html
- Page Title: Book Personal Training
- Container Div ID: booking-page
- Elements:
  - Dropdown ID: select-trainer (populated with trainers list)
  - Input (date) ID: session-date
  - Dropdown ID: session-time (select time slot)
  - Dropdown ID: session-duration (options: 30, 60, 90 minutes)
  - Button ID: confirm-booking-button (submit booking form)
- Navigation Buttons:
  - None specified
- Context Variables:
  - trainers: List of dicts
    - Access pattern: {% for trainer in trainers %} ... {{ trainer.name }} ... {% endfor %}
  - POST form expects select_trainer, session_date, session_time, session_duration
  - POST feedback optionally displayed


### 8. workouts.html
- Page Title: My Workout Records
- Container Div ID: workouts-page
- Elements:
  - Table ID: workouts-table
    - Columns: Date, Type, Duration, Calories Burned
  - Dropdown ID: filter-by-type (filter workouts by type: Class, PT Session, Personal)
  - Button ID: log-workout-button (navigate to /log_workout)
  - Button ID: back-to-dashboard (navigate back to /dashboard)
- Navigation Buttons:
  - log-workout-button → url_for('log_workout')
  - back-to-dashboard → url_for('dashboard')
- Context Variables:
  - workouts: List of dicts
    - Access pattern: {% for workout in workouts %} ... {{ workout.workout_date }}, {{ workout.workout_type }}, {{ workout.duration_minutes }}, {{ workout.calories_burned }} ... {% endfor %}


### 9. log_workout.html
- Page Title: Log Workout
- Container Div ID: log-workout-page
- Elements:
  - Dropdown ID: workout-type (options: Cardio, Strength, Flexibility, Sports)
  - Input (number) ID: workout-duration
  - Input (number) ID: calories-burned
  - Textarea ID: workout-notes
  - Button ID: submit-workout-button (submit workout log form)
- Navigation Buttons:
  - None specified
- Context Variables:
  - None for GET requests
  - POST form expects workout_type, workout_duration, calories_burned, workout_notes
  - POST submission feedback optionally displayed


---

## Section 3: Data File Schemas

### 1. data/memberships.txt
- Fields (pipe-delimited, exact order):
  - membership_id (int)
  - plan_name (str)
  - price (float)
  - billing_cycle (str)
  - features (str; comma separated list in one string)
  - max_classes (int or str, e.g., "unlimited")
- Description: Stores membership plan details including pricing and features.
- Example Rows:
  ```
  1|Basic|29.99|monthly|Gym access, 2 classes per week|8
  2|Premium|59.99|monthly|Gym access, 5 classes per week, 2 PT sessions|20
  3|Elite|99.99|monthly|Unlimited gym access, unlimited classes, 4 PT sessions, nutrition coaching|unlimited
  ```

### 2. data/classes.txt
- Fields (pipe-delimited, exact order):
  - class_id (int)
  - class_name (str)
  - trainer_id (int)
  - class_type (str)
  - schedule_day (str)
  - schedule_time (str, HH:MM 24-hour format)
  - capacity (int)
  - duration (int, minutes)
- Description: Stores scheduled fitness classes and details.
- Example Rows:
  ```
  1|Morning Yoga|1|Yoga|Monday|06:00|20|60
  2|CrossFit Bootcamp|2|CrossFit|Tuesday|18:00|15|45
  3|Pilates Core|3|Pilates|Wednesday|10:00|18|50
  ```

### 3. data/trainers.txt
- Fields (pipe-delimited, exact order):
  - trainer_id (int)
  - name (str)
  - specialty (str)
  - certifications (str; comma separated list in one string)
  - experience_years (int)
  - bio (str)
- Description: Stores trainers' profile details.
- Example Rows:
  ```
  1|Sarah Johnson|Yoga & Flexibility|Certified Yoga Instructor, CPR|8|Expert in mind-body wellness and injury prevention
  2|Mike Thompson|Strength & Conditioning|NASM-CPT, CrossFit Level 2|10|Specializes in powerlifting and functional fitness
  3|Emma Davis|Pilates|Pilates Method Alliance Certified|6|Focus on core strength and postural alignment
  ```

### 4. data/bookings.txt
- Fields (pipe-delimited, exact order):
  - booking_id (int)
  - member_name (str)
  - trainer_id (int)
  - booking_date (str, YYYY-MM-DD)
  - booking_time (str, HH:MM)
  - duration_minutes (int)
  - status (str; e.g., Confirmed, Pending)
- Description: Stores personal training session bookings.
- Example Rows:
  ```
  1|John Doe|1|2025-01-20|10:00|60|Confirmed
  2|Jane Smith|2|2025-01-21|14:00|45|Confirmed
  3|Alex Johnson|3|2025-01-22|16:00|60|Pending
  ```

### 5. data/workouts.txt
- Fields (pipe-delimited, exact order):
  - workout_id (int)
  - member_name (str)
  - workout_type (str)
  - workout_date (str, YYYY-MM-DD)
  - duration_minutes (int)
  - calories_burned (int)
  - notes (str)
- Description: Stores workout history records.
- Example Rows:
  ```
  1|John Doe|Cardio|2025-01-15|45|350|Morning run on treadmill
  2|Jane Smith|Strength|2025-01-16|60|420|Upper body weight training with trainer
  3|Alex Johnson|Class|2025-01-17|50|380|CrossFit Bootcamp session
  ```
