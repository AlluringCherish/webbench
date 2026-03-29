# GymMembership Web Application Design Specification

---

## Section 1: Flask Routes Specification

| Page Name             | Route Path                    | Function Name               | HTTP Method(s) | Template Rendered          | Context Variables (name: type)                                   |
|-----------------------|-------------------------------|-----------------------------|----------------|----------------------------|----------------------------------------------------------------|
| Root                  | `/`                           | root_redirect                | GET            | Redirect to `/dashboard`   | None                                                           |
| Dashboard             | `/dashboard`                  | dashboard                   | GET            | dashboard.html             | member_status: str                                              |
| Membership Plans      | `/memberships`                | memberships                 | GET            | memberships.html           | membership_plans: list of dict                                  |
| Plan Details          | `/plan/<int:plan_id>`         | plan_details                | GET            | plan_details.html          | plan: dict                                                     |
| Class Schedule        | `/schedule`                   | class_schedule              | GET            | class_schedule.html        | classes: list of dict, class_types: list of str                |
| Trainer Profiles      | `/trainers`                   | trainers                   | GET            | trainers.html              | trainers_list: list of dict, specialties: list of str          |
| Trainer Detail        | `/trainer/<int:trainer_id>`   | trainer_detail             | GET            | trainer_detail.html        | trainer: dict                                                  |
| PT Booking            | `/booking`                   | booking                    | GET, POST      | booking.html               | trainers_list: list of dict, booking_success: bool (POST only) |
| Workout Records       | `/workouts`                   | workouts                   | GET            | workouts.html              | workouts: list of dict, workout_types: list of str             |
| Log Workout           | `/log_workout`                | log_workout                | GET, POST      | log_workout.html           | log_success: bool (POST only)                                 |

---

### Route Details

1. **Root Route**
   - Path: `/`
   - Function: `root_redirect`
   - Method: GET
   - Behavior: Redirects to `/dashboard` route.
   - Template: None (redirect)
   - Context: None

2. **Dashboard Page**
   - Path: `/dashboard`
   - Function: `dashboard`
   - Method: GET
   - Template: `dashboard.html`
   - Context:
     - `member_status` (str): A string with member status or welcome message.

3. **Membership Plans Page**
   - Path: `/memberships`
   - Function: `memberships`
   - Method: GET
   - Template: `memberships.html`
   - Context:
     - `membership_plans` (list of dict): Each dict contains keys matching membership fields (membership_id:int, plan_name:str, price:float, billing_cycle:str, features:str, max_classes:str/int).

4. **Plan Details Page**
   - Path: `/plan/<int:plan_id>`
   - Function: `plan_details`
   - Method: GET
   - Template: `plan_details.html`
   - Context:
     - `plan` (dict): Single membership plan data with similar keys as in membership_plans.

5. **Class Schedule Page**
   - Path: `/schedule`
   - Function: `class_schedule`
   - Method: GET
   - Template: `class_schedule.html`
   - Context:
     - `classes` (list of dict): Each dict includes fields matching classes.txt data.
     - `class_types` (list of str): Unique class types used for filter dropdown.

6. **Trainer Profiles Page**
   - Path: `/trainers`
   - Function: `trainers`
   - Method: GET
   - Template: `trainers.html`
   - Context:
     - `trainers_list` (list of dict): Each dict contains trainers.txt fields.
     - `specialties` (list of str): List of distinct specialties for filter dropdown.

7. **Trainer Detail Page**
   - Path: `/trainer/<int:trainer_id>`
   - Function: `trainer_detail`
   - Method: GET
   - Template: `trainer_detail.html`
   - Context:
     - `trainer` (dict): Detailed information of a single trainer.

8. **PT Booking Page**
   - Path: `/booking`
   - Function: `booking`
   - Method: GET, POST
   - Template: `booking.html`
   - Context (GET):
     - `trainers_list` (list of dict): List of trainers available for booking.
   - Context (POST):
     - `booking_success` (bool): True if booking was successful, else False.
     - `trainers_list` (list of dict): To repopulate dropdown in case of error.

9. **Workout Records Page**
   - Path: `/workouts`
   - Function: `workouts`
   - Method: GET
   - Template: `workouts.html`
   - Context:
     - `workouts` (list of dict): User workout records.
     - `workout_types` (list of str): List of workout types for filter dropdown.

10. **Log Workout Page**
    - Path: `/log_workout`
    - Function: `log_workout`
    - Method: GET, POST
    - Template: `log_workout.html`
    - Context (POST):
      - `log_success` (bool): True if workout logged successfully.

---

## Section 2: HTML Template Specifications

### 1. dashboard.html
- Title: Gym Membership Dashboard
- Elements:
  - `dashboard-page` (Div): Container for dashboard page.
  - `member-welcome` (Div): Displays welcome message/status using `member_status`.
  - `browse-membership-button` (Button): On click, navigate to `memberships` route.
  - `view-schedule-button` (Button): Navigate to `schedule` route.
  - `book-trainer-button` (Button): Navigate to `booking` route.
- Navigation Buttons IDs and linked routes:
  - `browse-membership-button` => url_for('memberships')
  - `view-schedule-button` => url_for('class_schedule')
  - `book-trainer-button` => url_for('booking')

---

### 2. memberships.html
- Title: Membership Plans
- Elements:
  - `membership-page` (Div): Container for memberships page.
  - `plan-filter` (Dropdown): Options: Basic, Premium, Elite (can be inferred from data or hardcoded).
  - `plans-grid` (Div): Container looping over `membership_plans`.
    - For each plan in `membership_plans`:
      - Display plan_name, price, features.
      - Button with ID `view-details-button-{plan.membership_id}` to navigate to plan details page.
  - `back-to-dashboard` (Button): Navigates back to dashboard.
- Navigation Buttons:
  - `back-to-dashboard` => url_for('dashboard')
  - `view-details-button-{plan_id}` => url_for('plan_details', plan_id=plan_id)
- Context access:
  - Loop: `{% for plan in membership_plans %}`

---

### 3. plan_details.html
- Title: Plan Details
- Elements:
  - `plan-details-page` (Div): Container for plan details.
  - `plan-title` (H1): Displays `plan.plan_name`.
  - `plan-price` (Div): Displays `plan.price` and `plan.billing_cycle`.
  - `plan-features` (Div): Displays `plan.features`.
  - `enroll-plan-button` (Button): Button to enroll (could be non-functional as no auth).
  - `plan-reviews` (Div): Section for member reviews (static or empty).
- Context Variables:
  - `plan` object accessed as `plan.plan_name` etc.
- Navigation:
  - No explicit back button specified but can include link to memberships or dashboard.

---

### 4. class_schedule.html
- Title: Class Schedule
- Elements:
  - `schedule-page` (Div): Container.
  - `schedule-search` (Input): Text input for searching classes by name or trainer.
  - `schedule-filter` (Dropdown): Options from `class_types` context variable.
  - `classes-grid` (Div): Loop over `classes`:
    - Display class_name, schedule_day, schedule_time, trainer name, capacity, duration.
    - Button with ID `enroll-class-button-{class_id}` to enroll.
- Navigation:
  - Filter dropdown with options from `class_types`.
  - Enroll button links or actions assigned.

---

### 5. trainers.html
- Title: Trainer Profiles
- Elements:
  - `trainers-page` (Div): Container.
  - `trainer-search` (Input): Search by name or specialty.
  - `specialty-filter` (Dropdown): Options from `specialties`.
  - `trainers-grid` (Div): Loop over `trainers_list`:
    - Show photo placeholder (if any), name, expertise (specialty).
    - Button `view-trainer-button-{trainer_id}` to view detailed profile.
- Navigation:
  - Specialty filter dropdown from `specialties`.

---

### 6. trainer_detail.html
- Title: Trainer Profile
- Elements:
  - `trainer-detail-page` (Div): Container.
  - `trainer-name` (H1): `trainer.name`
  - `trainer-bio` (Div): `trainer.bio`
  - `trainer-certifications` (Div): `trainer.certifications`
  - `book-session-button` (Button): Book session with trainer.
  - `trainer-reviews` (Div): Client reviews section (can be static or empty).
- Navigation:
  - Button `book-session-button` to link or form to `/booking` (trainer pre-selected optional).

---

### 7. booking.html
- Title: Book Personal Training
- Elements:
  - `booking-page` (Div): Container.
  - `select-trainer` (Dropdown): Options from `trainers_list` using `trainer_id` and `name`.
  - `session-date` (Input date): Select date.
  - `session-time` (Dropdown): Predefined time slots (e.g., 06:00, 07:00,...).
  - `session-duration` (Dropdown): Options 30, 60, 90 minutes.
  - `confirm-booking-button` (Button): Submit booking.
- Navigation:
  - Upon POST success, display confirmation message.
- Context:
  - `trainers_list` used to populate trainer dropdown.
  - `booking_success` bool to show success message.

---

### 8. workouts.html
- Title: My Workout Records
- Elements:
  - `workouts-page` (Div): Container.
  - `workouts-table` (Table): Columns: date, type, duration, calories burned.
  - `filter-by-type` (Dropdown): Options from `workout_types`.
  - `log-workout-button` (Button): Navigate to `/log_workout`.
  - `back-to-dashboard` (Button): Navigate back to dashboard.
- Navigation:
  - Button `log-workout-button` => url_for('log_workout')
  - Button `back-to-dashboard` => url_for('dashboard')
- Context:
  - Loop workouts for table rows.

---

### 9. log_workout.html
- Title: Log Workout
- Elements:
  - `log-workout-page` (Div): Container.
  - `workout-type` (Dropdown): Options: Cardio, Strength, Flexibility, Sports.
  - `workout-duration` (Input number): Duration in minutes.
  - `calories-burned` (Input number): Estimated calories.
  - `workout-notes` (Textarea): Notes field.
  - `submit-workout-button` (Button): Submit log.
- Navigation:
  - Confirmation message on `log_success`.
- Context:
  - `log_success` bool to indicate successful submission.

---

## Section 3: Data File Schemas

1. **memberships.txt**
- Path: `data/memberships.txt`
- Fields (Pipe-delimited, exact order):
  1. membership_id (int)
  2. plan_name (str)
  3. price (float)
  4. billing_cycle (str)
  5. features (str)
  6. max_classes (str or int; e.g. "8" or "unlimited")
- Description: List of membership plans with pricing and features.
- Example rows:
  ```
  1|Basic|29.99|monthly|Gym access, 2 classes per week|8
  2|Premium|59.99|monthly|Gym access, 5 classes per week, 2 PT sessions|20
  3|Elite|99.99|monthly|Unlimited gym access, unlimited classes, 4 PT sessions, nutrition coaching|unlimited
  ```

2. **classes.txt**
- Path: `data/classes.txt`
- Fields (Pipe-delimited, exact order):
  1. class_id (int)
  2. class_name (str)
  3. trainer_id (int)
  4. class_type (str)
  5. schedule_day (str)
  6. schedule_time (str, HH:MM 24-hour)
  7. capacity (int)
  8. duration (int, minutes)
- Description: List of scheduled fitness classes.
- Example rows:
  ```
  1|Morning Yoga|1|Yoga|Monday|06:00|20|60
  2|CrossFit Bootcamp|2|CrossFit|Tuesday|18:00|15|45
  3|Pilates Core|3|Pilates|Wednesday|10:00|18|50
  ```

3. **trainers.txt**
- Path: `data/trainers.txt`
- Fields (Pipe-delimited, exact order):
  1. trainer_id (int)
  2. name (str)
  3. specialty (str)
  4. certifications (str)
  5. experience_years (int)
  6. bio (str)
- Description: Details about trainers.
- Example rows:
  ```
  1|Sarah Johnson|Yoga & Flexibility|Certified Yoga Instructor, CPR|8|Expert in mind-body wellness and injury prevention
  2|Mike Thompson|Strength & Conditioning|NASM-CPT, CrossFit Level 2|10|Specializes in powerlifting and functional fitness
  3|Emma Davis|Pilates|Pilates Method Alliance Certified|6|Focus on core strength and postural alignment
  ```

4. **bookings.txt**
- Path: `data/bookings.txt`
- Fields (Pipe-delimited, exact order):
  1. booking_id (int)
  2. member_name (str)
  3. trainer_id (int)
  4. booking_date (str, YYYY-MM-DD)
  5. booking_time (str, HH:MM 24-hour)
  6. duration_minutes (int)
  7. status (str)
- Description: Personal training session bookings.
- Example rows:
  ```
  1|John Doe|1|2025-01-20|10:00|60|Confirmed
  2|Jane Smith|2|2025-01-21|14:00|45|Confirmed
  3|Alex Johnson|3|2025-01-22|16:00|60|Pending
  ```

5. **workouts.txt**
- Path: `data/workouts.txt`
- Fields (Pipe-delimited, exact order):
  1. workout_id (int)
  2. member_name (str)
  3. workout_type (str)
  4. workout_date (str, YYYY-MM-DD)
  5. duration_minutes (int)
  6. calories_burned (int)
  7. notes (str)
- Description: User workout session records.
- Example rows:
  ```
  1|John Doe|Cardio|2025-01-15|45|350|Morning run on treadmill
  2|Jane Smith|Strength|2025-01-16|60|420|Upper body weight training with trainer
  3|Alex Johnson|Class|2025-01-17|50|380|CrossFit Bootcamp session
  ```

---

**Note:**
- All element IDs mentioned correspond exactly to those required in the pages.
- The context variables should be passed exactly as named for consistent template usage.
- The root route redirects to `/dashboard` ensuring app start page is dashboard.
- Dynamic routes use `<int:...>` syntax for identifying entities.
- Dropdown options and filters derive from unique values in data files or user specification.

This completes the GymMembership detailed design specification for independent Backend and Frontend development.
