# GymMembership Application Design Specification

---

# Section 1: Flask Routes Specification

| Route Path                  | Function Name              | HTTP Methods | Template File        | Context Variables (Name : Type)                                         |
|-----------------------------|----------------------------|--------------|----------------------|------------------------------------------------------------------------|
| `/`                         | root_redirect              | GET          | N/A (redirect)       | None                                                                   |
| `/dashboard`                | dashboard                 | GET          | dashboard.html       | None (Static welcome, buttons for navigation)                         |
| `/memberships`              | memberships               | GET          | memberships.html     | plans : list of dict (membership plans loaded from memberships.txt)   |
| `/plan/<int:plan_id>`       | plan_details              | GET          | plan_details.html    | plan : dict (specific plan data), reviews : list of str (optional empty) |
| `/classes`                 | class_schedule             | GET          | class_schedule.html  | classes : list of dict (loaded from classes.txt), class_types : list of str (unique class types) |
| `/trainers`                | trainer_profiles          | GET          | trainers.html        | trainers : list of dict (loaded from trainers.txt), specialties : list of str (unique specialties) |
| `/trainer/<int:trainer_id>` | trainer_detail            | GET          | trainer_detail.html  | trainer : dict (specific trainer data), reviews : list of str (optional empty) |
| `/booking`                 | pt_booking                | GET, POST   | booking.html          | trainers : list of dict (all trainers for dropdown)                    |
| `/workouts`                | workout_records           | GET          | workouts.html        | workouts : list of dict (all workouts filtered by member if applicable), workout_types : list of str (for filter dropdown) |
| `/log_workout`             | log_workout               | GET, POST   | log_workout.html      | None or form confirmation context                                      |


Notes:
- Root `/` route must redirect to `/dashboard`. 
- Booking and Log Workout pages use POST for form submissions.
- Dynamic routes include `<int:plan_id>` and `<int:trainer_id>` to access specific records.


# Section 2: HTML Template Specifications

## 1. Dashboard Page - `dashboard.html`
- **Page Title**: Gym Membership Dashboard
- **Element IDs and Types**:
  - `dashboard-page` (Div): Container for the dashboard page.
  - `member-welcome` (Div): Welcome section with member status.
  - `browse-membership-button` (Button): Navigate to memberships page.
  - `view-schedule-button` (Button): Navigate to class schedule page.
  - `book-trainer-button` (Button): Navigate to personal training booking page.
- **Navigation Buttons**:
  - `browse-membership-button`: URL via `url_for('memberships')`
  - `view-schedule-button`: URL via `url_for('class_schedule')`
  - `book-trainer-button`: URL via `url_for('pt_booking')`
- **Context Variables**: None.

## 2. Membership Plans Page - `memberships.html`
- **Page Title**: Membership Plans
- **Element IDs and Types**:
  - `membership-page` (Div): Container for the memberships page.
  - `plan-filter` (Dropdown): Filter plans by membership type (Basic, Premium, Elite).
  - `plans-grid` (Div): Grid displaying membership plan cards.
  - `view-details-button-{plan_id}` (Button): Button on each plan card to view details.
  - `back-to-dashboard` (Button): Button to return to dashboard.
- **Context Variables**:
  - `plans`: list of dict with keys `membership_id` (int), `plan_name` (str), `price` (str), `billing_cycle` (str), `features` (str), and `max_classes` (str/int).
  - Loop over `plans` to create cards. Use plan_id for dynamic IDs.
- **Navigation Buttons**:
  - `back-to-dashboard`: URL via `url_for('dashboard')`

## 3. Plan Details Page - `plan_details.html`
- **Page Title**: Plan Details
- **Element IDs and Types**:
  - `plan-details-page` (Div): Container for plan details.
  - `plan-title` (H1): Display plan name.
  - `plan-price` (Div): Display plan price and billing cycle.
  - `plan-features` (Div): Display all features included.
  - `enroll-plan-button` (Button): Button to enroll in plan.
  - `plan-reviews` (Div): Display member reviews.
- **Context Variables**:
  - `plan`: dict with keys as in memberships data.
  - `reviews`: list of str (can be empty).
- **Navigation Buttons**:
  - `enroll-plan-button`: (May link to a post or just show for now - no extra route defined)

## 4. Class Schedule Page - `class_schedule.html`
- **Page Title**: Class Schedule
- **Element IDs and Types**:
  - `schedule-page` (Div): Container for schedule.
  - `schedule-search` (Input): Search field for class name or trainer.
  - `schedule-filter` (Dropdown): Filter by class type.
  - `classes-grid` (Div): Grid displaying class cards.
  - `enroll-class-button-{class_id}` (Button): Button on each class card to enroll.
- **Context Variables**:
  - `classes`: list of dict with keys: `class_id` (int), `class_name` (str), `trainer_id` (int), `class_type` (str), `schedule_day` (str), `schedule_time` (str), `capacity` (int), `duration` (int)
  - `class_types`: list of str (unique class types for filter dropdown)
- **Navigation Buttons**:
  - (No specific navigation buttons described here)

## 5. Trainer Profiles Page - `trainers.html`
- **Page Title**: Trainer Profiles
- **Element IDs and Types**:
  - `trainers-page` (Div): Container for trainers.
  - `trainer-search` (Input): Search trainers by name or specialty.
  - `specialty-filter` (Dropdown): Filter by specialty.
  - `trainers-grid` (Div): Grid of trainer cards.
  - `view-trainer-button-{trainer_id}` (Button): Button on trainer card to view profile.
- **Context Variables**:
  - `trainers`: list of dict with keys: `trainer_id` (int), `name` (str), `specialty` (str), `certifications` (str), `experience_years` (int), `bio` (str)
  - `specialties`: list of str (unique specialties from trainers data)
- **Navigation Buttons**:
  - (No additional navigation buttons specified)

## 6. Trainer Detail Page - `trainer_detail.html`
- **Page Title**: Trainer Profile
- **Element IDs and Types**:
  - `trainer-detail-page` (Div): Container for trainer detail.
  - `trainer-name` (H1): Display trainer name.
  - `trainer-bio` (Div): Trainer biography and experience.
  - `trainer-certifications` (Div): Certifications.
  - `book-session-button` (Button): Book a session with trainer.
  - `trainer-reviews` (Div): Section showing client reviews.
- **Context Variables**:
  - `trainer`: dict as in trainers data.
  - `reviews`: list of str (client reviews, may be empty)
- **Navigation Buttons**:
  - `book-session-button`: URL via `url_for('pt_booking')`

## 7. PT Booking Page - `booking.html`
- **Page Title**: Book Personal Training
- **Element IDs and Types**:
  - `booking-page` (Div): Container for booking.
  - `select-trainer` (Dropdown): Select a trainer.
  - `session-date` (Input, date): Select session date.
  - `session-time` (Dropdown): Select time slot.
  - `session-duration` (Dropdown): Session duration (30, 60, 90 mins).
  - `confirm-booking-button` (Button): Confirm booking.
- **Context Variables**:
  - `trainers`: list of dict with keys as trainer profiles for dropdown.
- **Form Submission**:
  - Submits POST to `/booking` route.

## 8. Workout Records Page - `workouts.html`
- **Page Title**: My Workout Records
- **Element IDs and Types**:
  - `workouts-page` (Div): Container for workouts.
  - `workouts-table` (Table): Displays workout history columns: date, type, duration, calories.
  - `filter-by-type` (Dropdown): Filter workout type (Class, PT Session, Personal).
  - `log-workout-button` (Button): Button to log a new workout.
  - `back-to-dashboard` (Button): Return to dashboard.
- **Context Variables**:
  - `workouts`: list of dict with keys: `workout_id` (int), `member_name` (str), `workout_type` (str), `workout_date` (str), `duration_minutes` (int), `calories_burned` (int), `notes` (str).
  - `workout_types`: list of str for filter dropdown.
- **Navigation Buttons**:
  - `log-workout-button`: URL via `url_for('log_workout')`
  - `back-to-dashboard`: URL via `url_for('dashboard')`

## 9. Log Workout Page - `log_workout.html`
- **Page Title**: Log Workout
- **Element IDs and Types**:
  - `log-workout-page` (Div): Container for this page.
  - `workout-type` (Dropdown): Select workout type (Cardio, Strength, Flexibility, Sports).
  - `workout-duration` (Input, number): Input duration in minutes.
  - `calories-burned` (Input, number): Input estimated calories burned.
  - `workout-notes` (Textarea): Notes about workout.
  - `submit-workout-button` (Button): Submit the workout record.
- **Context Variables**: None mandatory; optionally success messages on submission.
- **Form Submission**:
  - POST to `/log_workout` route.


# Section 3: Data File Schemas

## 1. Memberships Data - `data/memberships.txt`
- **Fields:**
  1. membership_id : int
  2. plan_name : str
  3. price : str (decimal format as string)
  4. billing_cycle : str
  5. features : str (comma-separated features)
  6. max_classes : str or int (e.g., number or 'unlimited')
- **Description:** Stores membership plan details.
- **Example Rows:**
  ```
  1|Basic|29.99|monthly|Gym access, 2 classes per week|8
  2|Premium|59.99|monthly|Gym access, 5 classes per week, 2 PT sessions|20
  3|Elite|99.99|monthly|Unlimited gym access, unlimited classes, 4 PT sessions, nutrition coaching|unlimited
  ```

## 2. Classes Data - `data/classes.txt`
- **Fields:**
  1. class_id : int
  2. class_name : str
  3. trainer_id : int
  4. class_type : str
  5. schedule_day : str
  6. schedule_time : str (HH:MM)
  7. capacity : int
  8. duration : int (minutes)
- **Description:** Details about fitness classes.
- **Example Rows:**
  ```
  1|Morning Yoga|1|Yoga|Monday|06:00|20|60
  2|CrossFit Bootcamp|2|CrossFit|Tuesday|18:00|15|45
  3|Pilates Core|3|Pilates|Wednesday|10:00|18|50
  ```

## 3. Trainers Data - `data/trainers.txt`
- **Fields:**
  1. trainer_id : int
  2. name : str
  3. specialty : str
  4. certifications : str
  5. experience_years : int
  6. bio : str
- **Description:** Information about trainers.
- **Example Rows:**
  ```
  1|Sarah Johnson|Yoga & Flexibility|Certified Yoga Instructor, CPR|8|Expert in mind-body wellness and injury prevention
  2|Mike Thompson|Strength & Conditioning|NASM-CPT, CrossFit Level 2|10|Specializes in powerlifting and functional fitness
  3|Emma Davis|Pilates|Pilates Method Alliance Certified|6|Focus on core strength and postural alignment
  ```

## 4. Bookings Data - `data/bookings.txt`
- **Fields:**
  1. booking_id : int
  2. member_name : str
  3. trainer_id : int
  4. booking_date : str (YYYY-MM-DD)
  5. booking_time : str (HH:MM)
  6. duration_minutes : int
  7. status : str
- **Description:** User personal training session bookings.
- **Example Rows:**
  ```
  1|John Doe|1|2025-01-20|10:00|60|Confirmed
  2|Jane Smith|2|2025-01-21|14:00|45|Confirmed
  3|Alex Johnson|3|2025-01-22|16:00|60|Pending
  ```

## 5. Workouts Data - `data/workouts.txt`
- **Fields:**
  1. workout_id : int
  2. member_name : str
  3. workout_type : str
  4. workout_date : str (YYYY-MM-DD)
  5. duration_minutes : int
  6. calories_burned : int
  7. notes : str
- **Description:** Records of user workouts.
- **Example Rows:**
  ```
  1|John Doe|Cardio|2025-01-15|45|350|Morning run on treadmill
  2|Jane Smith|Strength|2025-01-16|60|420|Upper body weight training with trainer
  3|Alex Johnson|Class|2025-01-17|50|380|CrossFit Bootcamp session
  ```

---

This specification ensures backend developers can implement all Flask routes and data handling exactly, and frontend developers can create all specified pages and UI elements with consistent IDs and working navigation.
