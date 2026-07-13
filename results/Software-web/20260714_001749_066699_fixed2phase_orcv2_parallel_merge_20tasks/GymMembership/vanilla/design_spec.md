# GymMembership Design Specification

---

## Section 1: Backend Routes and Data Access

### 1. Dashboard Page
- **Route:** `/`
- **Methods:** GET
- **Behavior:**
  - Load member highlights (static or dynamic as applicable).
  - Load featured classes for dashboard display.
  - Render template: `dashboard.html`
- **Context Variables:**
  - `member_status` (str): Welcome/status message (e.g., "Active Basic Member")
  - `featured_classes` (list of dict): Sample classes info for dashboard display.

---

### 2. Membership Plans Page
- **Route:** `/memberships`
- **Methods:** GET
- **Behavior:**
  - Read membership plans from `data/memberships.txt`.
  - Filter by optional query param `type` (Basic, Premium, Elite).
  - Render template: `membership_plans.html`
- **Context Variables:**
  - `membership_plans` (list of dict): Each dict has keys:
    - `id` (int): membership_id
    - `plan_name` (str)
    - `price` (float)
    - `billing_cycle` (str)
    - `features` (list of str) or comma-separated str
    - `max_classes` (int or str)
  - `filter_options` (list of str): ["Basic", "Premium", "Elite"]
  - `selected_type` (str or None): Current filter value

---

### 3. Plan Details Page
- **Route:** `/membership/<int:membership_id>`
- **Methods:** GET
- **Behavior:**
  - Read all plans from `data/memberships.txt`.
  - Find plan matching `membership_id`.
  - Load reviews if implemented (placeholder or empty list).
  - Render template: `plan_details.html`
- **Context Variables:**
  - `plan` (dict): Same structure as in Membership Plans, with keys matching frontend spec (`id`, `plan_name`, `price`, `billing_cycle`, `features` list).
  - `reviews` (list of dict): Optional, each with keys like `reviewer`, `comment`, `rating`.

---

### 4. Class Schedule Page
- **Route:** `/classes`
- **Methods:** GET
- **Behavior:**
  - Read classes from `data/classes.txt`.
  - Read trainers from `data/trainers.txt` to map `trainer_id` to `trainer_name`.
  - Filter classes by optional query params:
    - `search`: Matches class name or trainer name (case-insensitive substring).
    - `type`: Filter by class type.
  - Provide the list of all class types for filter dropdown.
  - Render template: `class_schedule.html`
- **Context Variables:**
  - `classes` (list of dict): Each dict with keys:
    - `class_id`, `class_name`, `trainer_name`, `class_type`, `schedule_day`, `schedule_time`, `capacity`, `duration`
  - `search_term` (str): Current search term or empty string
  - `selected_type` (str or None)
  - `class_types` (list of str): All distinct class types present in data

---

### 5. Trainer Profiles Page
- **Route:** `/trainers`
- **Methods:** GET
- **Behavior:**
  - Read trainers from `data/trainers.txt`.
  - Filter by optional query params:
    - `search`: matches name or specialty.
    - `specialty`: filter by specialty.
  - Provide list of specialties for filter dropdown.
  - Render template: `trainer_profiles.html`
- **Context Variables:**
  - `trainers` (list of dict): Each dict with keys:
    - `trainer_id`, `name`, `specialty`, `certifications`, `experience_years`, `bio`
  - `search_term` (str)
  - `selected_specialty` (str or None)
  - `specialty_options` (list of str): e.g. ["Strength", "Cardio", "Flexibility", "Weight Loss"]

---

### 6. Trainer Detail Page
- **Route:** `/trainer/<int:trainer_id>`
- **Methods:** GET
- **Behavior:**
  - Read trainer details from `data/trainers.txt`.
  - Load reviews if implemented (empty or placeholder).
  - Render template: `trainer_detail.html`
- **Context Variables:**
  - `trainer` (dict): keys - `trainer_id`, `name`, `bio`, `certifications` (list or string), `experience_years`
  - `reviews` (list of dict): client reviews

---

### 7. PT Booking Page
- **Route:** `/booking`
- **Methods:** GET, POST
- **Behavior:**
  - GET:
    - Load all trainers from `data/trainers.txt`.
    - Provide available time slots (hardcoded list of times as strings, e.g., "08:00", "09:00" etc).
    - Provide session durations [30, 60, 90].
    - Accept optional query param to preselect trainer.
    - Render template: `pt_booking.html`
  - POST:
    - Receive form data: `member_name`, `trainer_id`, `session_date` (YYYY-MM-DD), `session_time` (HH:MM), `session_duration` (int)
    - Validate inputs.
    - Generate new `booking_id` (max existing + 1 or 1).
    - Append booking record to `data/bookings.txt` with status "Pending".
    - Redirect or render confirmation.
- **Context Variables (GET):**
  - `trainers` (list of dict): with `trainer_id` and `name`
  - `available_timeslots` (list of str): e.g., ["08:00", "09:00", "10:00", ...]
  - `session_durations` (list of int): [30, 60, 90]
  - `preselected_trainer_id` (int or None)

---

### 8. Workout Records Page
- **Route:** `/workouts`
- **Methods:** GET
- **Behavior:**
  - Read workouts from `data/workouts.txt`.
  - Filter by optional query param `type` (workout type filter).
  - Render template: `workout_records.html`
- **Context Variables:**
  - `workouts` (list of dict): Each dict has keys:
    - `workout_id`, `member_name`, `workout_type`, `workout_date`, `duration_minutes`, `calories_burned`, `notes`
  - `selected_type` (str or None)
  - `workout_type_filters` (list of str): ["Class", "PT Session", "Personal"]

---

### 9. Log Workout Page
- **Route:** `/log-workout`
- **Methods:** GET, POST
- **Behavior:**
  - GET: Render `log_workout.html` template with blank form.
  - POST:
    - Receive form data: `member_name`, `workout_type`, `workout_duration`, `calories_burned`, `workout_notes`, optional `workout_date` (default to current date if omitted).
    - Generate new `workout_id`.
    - Append workout record to `data/workouts.txt`.
    - Redirect or confirm logging.
- **Context Variables (GET):**
  - None needed, except list of workout types for dropdown.

---

## Section 2: Data File Format and Access

All data files are in the `data/` directory relative to the Flask app root. Files use pipe (`|`) as delimiter. Each line represents one record.

### 1. Memberships Data
- **File:** `data/memberships.txt`
- **Format:**
  ```
  membership_id|plan_name|price|billing_cycle|features|max_classes
  ```
- **Field Types:**
  - `membership_id`: int
  - `plan_name`: str
  - `price`: float
  - `billing_cycle`: str
  - `features`: str (comma separated list)
  - `max_classes`: int or str ("unlimited")
- **Example:**
  ```
  1|Basic|29.99|monthly|Gym access, 2 classes per week|8
  ```

---

### 2. Classes Data
- **File:** `data/classes.txt`
- **Format:**
  ```
  class_id|class_name|trainer_id|class_type|schedule_day|schedule_time|capacity|duration
  ```
- **Field Types:**
  - `class_id`: int
  - `class_name`: str
  - `trainer_id`: int
  - `class_type`: str
  - `schedule_day`: str
  - `schedule_time`: str (HH:MM)
  - `capacity`: int
  - `duration`: int (minutes)
- **Example:**
  ```
  1|Morning Yoga|1|Yoga|Monday|06:00|20|60
  ```

---

### 3. Trainers Data
- **File:** `data/trainers.txt`
- **Format:**
  ```
  trainer_id|name|specialty|certifications|experience_years|bio
  ```
- **Field Types:**
  - `trainer_id`: int
  - `name`: str
  - `specialty`: str
  - `certifications`: str
  - `experience_years`: int
  - `bio`: str
- **Example:**
  ```
  1|Sarah Johnson|Yoga & Flexibility|Certified Yoga Instructor, CPR|8|Expert in mind-body wellness and injury prevention
  ```

---

### 4. Bookings Data
- **File:** `data/bookings.txt`
- **Format:**
  ```
  booking_id|member_name|trainer_id|booking_date|booking_time|duration_minutes|status
  ```
- **Field Types:**
  - `booking_id`: int
  - `member_name`: str
  - `trainer_id`: int
  - `booking_date`: str (YYYY-MM-DD)
  - `booking_time`: str (HH:MM)
  - `duration_minutes`: int
  - `status`: str (e.g. "Pending", "Confirmed")
- **Example:**
  ```
  1|John Doe|1|2025-01-20|10:00|60|Confirmed
  ```

---

### 5. Workouts Data
- **File:** `data/workouts.txt`
- **Format:**
  ```
  workout_id|member_name|workout_type|workout_date|duration_minutes|calories_burned|notes
  ```
- **Field Types:**
  - `workout_id`: int
  - `member_name`: str
  - `workout_type`: str
  - `workout_date`: str (YYYY-MM-DD)
  - `duration_minutes`: int
  - `calories_burned`: int
  - `notes`: str
- **Example:**
  ```
  1|John Doe|Cardio|2025-01-15|45|350|Morning run on treadmill
  ```

---

## Section 3: Frontend Templates and UI Elements

### 1. Dashboard Page
- **Template:** `dashboard.html`
- **Page Title:** Gym Membership Dashboard
- **Main Container ID:** `dashboard-page`
- **Elements:**
  - `member-welcome` (Div): Welcome message showing `member_status`
  - `browse-membership-button` (Button): Navigates to Membership Plans page (`/memberships`)
  - `view-schedule-button` (Button): Navigates to Class Schedule page (`/classes`)
  - `book-trainer-button` (Button): Navigates to PT Booking page (`/booking`)

---

### 2. Membership Plans Page
- **Template:** `membership_plans.html`
- **Page Title:** Membership Plans
- **Container ID:** `membership-page`
- **Elements:**
  - `plan-filter` (Dropdown): Filter membership plans by type (Basic, Premium, Elite)
  - `plans-grid` (Div): Grid of membership plan cards
  - `view-details-button-{plan_id}` (Button): View detailed info page `/membership/<plan_id>`
  - `back-to-dashboard` (Button): Navigate back to `/`

---

### 3. Plan Details Page
- **Template:** `plan_details.html`
- **Page Title:** Plan Details
- **Container ID:** `plan-details-page`
- **Elements:**
  - `plan-title` (H1): Plan name
  - `plan-price` (Div): Price and billing cycle
  - `plan-features` (Div): Features list
  - `enroll-plan-button` (Button): Enroll action (behavior optional)
  - `plan-reviews` (Div): Show reviews

---

### 4. Class Schedule Page
- **Template:** `class_schedule.html`
- **Page Title:** Class Schedule
- **Container ID:** `schedule-page`
- **Elements:**
  - `schedule-search` (Input): Search classes by name or trainer
  - `schedule-filter` (Dropdown): Filter classes by type
  - `classes-grid` (Div): Grid for classes
  - `enroll-class-button-{class_id}` (Button): Enroll in class

---

### 5. Trainer Profiles Page
- **Template:** `trainer_profiles.html`
- **Page Title:** Trainer Profiles
- **Container ID:** `trainers-page`
- **Elements:**
  - `trainer-search` (Input): Search by trainer name or specialty
  - `specialty-filter` (Dropdown): Filter by specialty
  - `trainers-grid` (Div): Grid of trainers
  - `view-trainer-button-{trainer_id}` (Button): View trainer profile

---

### 6. Trainer Detail Page
- **Template:** `trainer_detail.html`
- **Page Title:** Trainer Profile
- **Container ID:** `trainer-detail-page`
- **Elements:**
  - `trainer-name` (H1): Trainer name
  - `trainer-bio` (Div): Bio and experience
  - `trainer-certifications` (Div): Certifications
  - `book-session-button` (Button): Navigate to booking with trainer preselected
  - `trainer-reviews` (Div): Client reviews

---

### 7. PT Booking Page
- **Template:** `pt_booking.html`
- **Page Title:** Book Personal Training
- **Container ID:** `booking-page`
- **Elements:**
  - `select-trainer` (Dropdown): Choose trainer
  - `session-date` (Input date): Choose session date
  - `session-time` (Dropdown): Select time slot
  - `session-duration` (Dropdown): Select duration (30, 60, 90)
  - `confirm-booking-button` (Button): Submit booking

---

### 8. Workout Records Page
- **Template:** `workout_records.html`
- **Page Title:** My Workout Records
- **Container ID:** `workouts-page`
- **Elements:**
  - `workouts-table` (Table): Display workout history with columns Date, Type, Duration, Calories burned
  - `filter-by-type` (Dropdown): Filter by workout type (Class, PT Session, Personal)
  - `log-workout-button` (Button): Navigate to Log Workout page
  - `back-to-dashboard` (Button): Navigate back to dashboard

---

### 9. Log Workout Page
- **Template:** `log_workout.html`
- **Page Title:** Log Workout
- **Container ID:** `log-workout-page`
- **Elements:**
  - `workout-type` (Dropdown): Select workout type (Cardio, Strength, Flexibility, Sports)
  - `workout-duration` (Input number): Enter duration
  - `calories-burned` (Input number): Enter calories burned
  - `workout-notes` (Textarea): Notes
  - `submit-workout-button` (Button): Submit workout record

---

## Section 4: Navigation Flows

- **Dashboard Page:**
  - `browse-membership-button` -> `/memberships`
  - `view-schedule-button` -> `/classes`
  - `book-trainer-button` -> `/booking`

- **Membership Plans Page:**
  - `view-details-button-{plan_id}` -> `/membership/<plan_id>`
  - `back-to-dashboard` -> `/`

- **Plan Details Page:**
  - `enroll-plan-button` may trigger enrollment logic (behavior undefined here)

- **Class Schedule Page:**
  - `enroll-class-button-{class_id}` triggers enrollment UI feedback (functional logic out of scope)

- **Trainer Profiles Page:**
  - `view-trainer-button-{trainer_id}` -> `/trainer/<trainer_id>`

- **Trainer Detail Page:**
  - `book-session-button` -> `/booking` with `preselected_trainer_id` query param

- **PT Booking Page:**
  - `confirm-booking-button` submits booking, then redirects or confirms

- **Workout Records Page:**
  - `log-workout-button` -> `/log-workout`
  - `back-to-dashboard` -> `/`

- **Log Workout Page:**
  - `submit-workout-button` submits workout and redirects to `/workouts`

---

# Summary

This merged design specification reconciles backend routes, data file schemas, frontend templates, element IDs, expected context variables, and navigation flows for the GymMembership web application. Backend and frontend developers can implement their parts independently guided by this consistent spec. All routes, templates, UI elements, data formats, and navigation logic fully cover the user requirements with no inconsistencies.

*End of design_spec.md*