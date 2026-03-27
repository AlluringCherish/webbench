# GymMembership Design Specification Document

---

## 1. Flask Routes Specification

| Route Path | Function Name | HTTP Methods | Template Filename | Context Variables (Name : Data Type) |
|------------|---------------|--------------|-------------------|-------------------------------------|
| / | root_redirect | GET | None (Redirect) | None |
| /dashboard | dashboard | GET | dashboard.html | member_status: str, featured_classes: List[Dict], quick_links: List[Dict] |
| /memberships | memberships | GET | memberships.html | memberships_list: List[Dict], membership_types: List[str] |
| /memberships/<int:plan_id> | plan_details | GET | plan_details.html | plan: Dict, reviews: List[Dict] |
| /classes | classes | GET | classes.html | classes_list: List[Dict], class_types: List[str] |
| /trainers | trainers | GET | trainers.html | trainers_list: List[Dict], specialties: List[str] |
| /trainer/<int:trainer_id> | trainer_detail | GET | trainer_detail.html | trainer: Dict, reviews: List[Dict] |
| /booking | booking | GET, POST | booking.html | trainers_list: List[Dict], available_times: List[str], booking_success: bool (POST) |
| /workouts | workouts | GET | workouts.html | workouts_list: List[Dict], workout_types: List[str] |
| /log_workout | log_workout | GET, POST | log_workout.html | workout_types: List[str], log_success: bool (POST) |

**Notes:**
- The root route `/` redirects to `/dashboard`.
- POST methods are used in `/booking` and `/log_workout` routes for forms submission.
- Context variable data types marked as List[Dict] represent lists of dictionaries with relevant data fields.

---

## 2. HTML Template Specifications

### Template: dashboard.html
- **Page Title:** Gym Membership Dashboard
- **Element IDs:**
  - `dashboard-page`: Div container for the dashboard.
  - `member-welcome`: Div displaying member status information.
  - `browse-membership-button`: Button navigating to `/memberships`.
  - `view-schedule-button`: Button navigating to `/classes`.
  - `book-trainer-button`: Button navigating to `/booking`.
- **Context Variables:**
  - `member_status` (str): Displayed in `member-welcome`.
  - `featured_classes` (list of dict): Each class displayed in a featured section (not explicitly id'ed here).
  - `quick_links` (list of dict): Used for additional navigation elements (if any).
- **Navigation Buttons:**
  - `browse-membership-button` -> `url_for('memberships')`
  - `view-schedule-button` -> `url_for('classes')`
  - `book-trainer-button` -> `url_for('booking')`

---

### Template: memberships.html
- **Page Title:** Membership Plans
- **Element IDs:**
  - `membership-page`: Div container for the page.
  - `plan-filter`: Dropdown to filter by membership type (Basic, Premium, Elite).
  - `plans-grid`: Div that contains membership plan cards.
  - `view-details-button-{{ plan.membership_id }}`: Button to view plan details.
  - `back-to-dashboard`: Button to return to `/dashboard`.
- **Context Variables:**
  - `memberships_list` (list of dict): Each dict includes membership_id, plan_name, price, billing_cycle, features, max_classes.
  - `membership_types` (list of str): Membership types for filter dropdown.
- **Navigation Buttons:**
  - `view-details-button-{{ plan.membership_id }}` -> `url_for('plan_details', plan_id=plan.membership_id)`
  - `back-to-dashboard` -> `url_for('dashboard')`

---

### Template: plan_details.html
- **Page Title:** Plan Details
- **Element IDs:**
  - `plan-details-page`: Div container.
  - `plan-title`: H1 for plan name.
  - `plan-price`: Div displaying price and billing cycle.
  - `plan-features`: Div listing features.
  - `enroll-plan-button`: Button to enroll (could be a form POST target).
  - `plan-reviews`: Div showing member reviews.
- **Context Variables:**
  - `plan` (dict): Contains plan details.
  - `reviews` (list of dict): Reviews associated with the plan.
- **Navigation Buttons:**
  - `enroll-plan-button` triggers form POST to enroll (endpoint not specified, implicit).

---

### Template: classes.html
- **Page Title:** Class Schedule
- **Element IDs:**
  - `schedule-page`: Div container.
  - `schedule-search`: Input field to search classes.
  - `schedule-filter`: Dropdown filter by class type.
  - `classes-grid`: Div containing class cards.
  - `enroll-class-button-{{ class.class_id }}`: Button to enroll in a class.
- **Context Variables:**
  - `classes_list` (list of dict): Class info with class_id, class_name, trainer_id, class_type, schedule_day, schedule_time, capacity, duration.
  - `class_types` (list of str): Used in filter dropdown.
- **Navigation Buttons:**
  - `enroll-class-button-{{ class.class_id }}` -> POST or GET endpoint (not specified), assumed handled via JS or form.

---

### Template: trainers.html
- **Page Title:** Trainer Profiles
- **Element IDs:**
  - `trainers-page`: Div container.
  - `trainer-search`: Input to search trainers.
  - `specialty-filter`: Dropdown to filter by specialty.
  - `trainers-grid`: Div for trainer cards.
  - `view-trainer-button-{{ trainer.trainer_id }}`: Button to view trainer profile.
- **Context Variables:**
  - `trainers_list` (list of dict): Trainer info including trainer_id, name, specialty, certifications, experience_years, bio.
  - `specialties` (list of str): Used in filter dropdown.
- **Navigation Buttons:**
  - `view-trainer-button-{{ trainer.trainer_id }}` -> `url_for('trainer_detail', trainer_id=trainer.trainer_id)`

---

### Template: trainer_detail.html
- **Page Title:** Trainer Profile
- **Element IDs:**
  - `trainer-detail-page`: Div container.
  - `trainer-name`: H1 for trainer's name.
  - `trainer-bio`: Div for biography and experience.
  - `trainer-certifications`: Div with certifications.
  - `book-session-button`: Button to book a session (link to booking page with trainer preselected).
  - `trainer-reviews`: Div with client reviews.
- **Context Variables:**
  - `trainer` (dict): Trainer details.
  - `reviews` (list of dict): Client reviews.
- **Navigation Buttons:**
  - `book-session-button` -> `url_for('booking')` with query parameter (not specified exactly but expected).

---

### Template: booking.html
- **Page Title:** Book Personal Training
- **Element IDs:**
  - `booking-page`: Div container.
  - `select-trainer`: Dropdown to select trainer.
  - `session-date`: Input type date for session date.
  - `session-time`: Dropdown for time slots.
  - `session-duration`: Dropdown for duration (30, 60, 90 mins).
  - `confirm-booking-button`: Button to confirm booking submission.
- **Context Variables:**
  - `trainers_list` (list of dict): List of trainers.
  - `available_times` (list of str): Time slots for session.
  - `booking_success` (bool): Status message after POST submission.
- **Navigation Buttons:**
  - Confirm button triggers POST to booking route.

---

### Template: workouts.html
- **Page Title:** My Workout Records
- **Element IDs:**
  - `workouts-page`: Div container.
  - `workouts-table`: Table displaying workout logs.
  - `filter-by-type`: Dropdown to filter workout types.
  - `log-workout-button`: Button linking to `/log_workout`.
  - `back-to-dashboard`: Button linking to `/dashboard`.
- **Context Variables:**
  - `workouts_list` (list of dict): Contains workout records.
  - `workout_types` (list of str): For filtering.
- **Navigation Buttons:**
  - `log-workout-button` -> `url_for('log_workout')`
  - `back-to-dashboard` -> `url_for('dashboard')`

---

### Template: log_workout.html
- **Page Title:** Log Workout
- **Element IDs:**
  - `log-workout-page`: Div container.
  - `workout-type`: Dropdown to select workout type.
  - `workout-duration`: Number input for duration.
  - `calories-burned`: Number input for calories.
  - `workout-notes`: Textarea for notes.
  - `submit-workout-button`: Button to submit form.
- **Context Variables:**
  - `workout_types` (list of str): Options for workout types.
  - `log_success` (bool): Message after submission.
- **Navigation Buttons:**
  - Submit button triggers POST to log_workout route.

---

## 3. Data File Schemas

### 1. Memberships Data
- **File Path:** data/memberships.txt
- **Field Order and Types:**
  - membership_id (int)
  - plan_name (str)
  - price (float)
  - billing_cycle (str)
  - features (str)
  - max_classes (str; can be numeric or 'unlimited')
- **Description:** Stores details of all membership plans.
- **Example Rows:**
  ```
  1|Basic|29.99|monthly|Gym access, 2 classes per week|8
  2|Premium|59.99|monthly|Gym access, 5 classes per week, 2 PT sessions|20
  3|Elite|99.99|monthly|Unlimited gym access, unlimited classes, 4 PT sessions, nutrition coaching|unlimited
  ```

---

### 2. Classes Data
- **File Path:** data/classes.txt
- **Field Order and Types:**
  - class_id (int)
  - class_name (str)
  - trainer_id (int)
  - class_type (str)
  - schedule_day (str)
  - schedule_time (str, HH:MM 24hr format)
  - capacity (int)
  - duration (int, minutes)
- **Description:** Represents fitness classes schedule and details.
- **Example Rows:**
  ```
  1|Morning Yoga|1|Yoga|Monday|06:00|20|60
  2|CrossFit Bootcamp|2|CrossFit|Tuesday|18:00|15|45
  3|Pilates Core|3|Pilates|Wednesday|10:00|18|50
  ```

---

### 3. Trainers Data
- **File Path:** data/trainers.txt
- **Field Order and Types:**
  - trainer_id (int)
  - name (str)
  - specialty (str)
  - certifications (str)  
  - experience_years (int)
  - bio (str)
- **Description:** Contains profiles of all trainers.
- **Example Rows:**
  ```
  1|Sarah Johnson|Yoga & Flexibility|Certified Yoga Instructor, CPR|8|Expert in mind-body wellness and injury prevention
  2|Mike Thompson|Strength & Conditioning|NASM-CPT, CrossFit Level 2|10|Specializes in powerlifting and functional fitness
  3|Emma Davis|Pilates|Pilates Method Alliance Certified|6|Focus on core strength and postural alignment
  ```

---

### 4. Bookings Data
- **File Path:** data/bookings.txt
- **Field Order and Types:**
  - booking_id (int)
  - member_name (str)
  - trainer_id (int)
  - booking_date (str, YYYY-MM-DD)
  - booking_time (str, HH:MM 24hr)
  - duration_minutes (int)
  - status (str)
- **Description:** Stores personal training session bookings.
- **Example Rows:**
  ```
  1|John Doe|1|2025-01-20|10:00|60|Confirmed
  2|Jane Smith|2|2025-01-21|14:00|45|Confirmed
  3|Alex Johnson|3|2025-01-22|16:00|60|Pending
  ```

---

### 5. Workouts Data
- **File Path:** data/workouts.txt
- **Field Order and Types:**
  - workout_id (int)
  - member_name (str)
  - workout_type (str)
  - workout_date (str, YYYY-MM-DD)
  - duration_minutes (int)
  - calories_burned (int)
  - notes (str)
- **Description:** Stores user's workout history and progress logs.
- **Example Rows:**
  ```
  1|John Doe|Cardio|2025-01-15|45|350|Morning run on treadmill
  2|Jane Smith|Strength|2025-01-16|60|420|Upper body weight training with trainer
  3|Alex Johnson|Class|2025-01-17|50|380|CrossFit Bootcamp session
  ```
