# GymMembership Application Design Specification

---

# Section 1: Flask Routes Specification

| Route Path                  | Function Name              | HTTP Methods | Template File        | Context Variables (Name : Type)                                         |
|-----------------------------|----------------------------|--------------|----------------------|------------------------------------------------------------------------|
| `/`                         | root_redirect              | GET          | N/A (redirect)       | None                                                                   |
| `/dashboard`                | dashboard                 | GET          | dashboard.html       | member_welcome_msg : str, featured_classes : list, (Optional) quick_links : dict|
| `/memberships`              | memberships               | GET          | memberships.html     | plans : list of dict ({'membership_id': int, 'plan_name': str, 'price': float, 'billing_cycle': str, 'features': str, 'max_classes': str|int})              |
| `/plan/<int:plan_id>`       | plan_details              | GET          | plan_details.html    | plan : dict (keys: membership_id:int, plan_name:str, price:float, billing_cycle:str, features:str, max_classes:int/str), reviews : list(dict) |
| `/classes`                  | class_schedule            | GET          | class_schedule.html  | classes : list of dict ({class_id:int, class_name:str, trainer_name:str, class_type:str, schedule_day:str, schedule_time:str, capacity:int, duration:int}) |
| `/trainers`                 | trainer_profiles          | GET          | trainer_profiles.html| trainers : list of dict ({trainer_id:int, name:str, specialty:str, certifications:str, experience_years:int})                                  |
| `/trainer/<int:trainer_id>` | trainer_detail            | GET          | trainer_detail.html  | trainer : dict (trainer_id:int, name:str, specialty:str, certifications:str, experience_years:int, bio:str), reviews : list(dict)             |
| `/booking`                  | pt_booking                | GET          | pt_booking.html      | trainers : list of dict ({trainer_id:int, name:str})                                                        |
| `/booking`                  | confirm_booking           | POST         | N/A                  | Expects form data: trainer_id:int, session_date:str (YYYY-MM-DD), session_time:str (HH:MM), session_duration:int (30,60,90) | 
| `/workouts`                 | workout_records           | GET          | workout_records.html | workouts : list of dict ({workout_id:int, member_name:str, workout_type:str, workout_date:str (YYYY-MM-DD), duration_minutes:int, calories_burned:int, notes:str})           |
| `/log-workout`              | log_workout               | GET          | log_workout.html     | None                                                                   |
| `/log-workout`              | submit_workout            | POST         | N/A                  | Expects form data: workout_type:str, workout_duration:int, calories_burned:int, workout_notes:str                          |

* Notes:
  - The root route `/` redirects to `/dashboard`.
  - POST routes for `/booking` and `/log-workout` handle form submissions.
  - All GET routes render the specified template with context variables matching backend data structures.
  - Dynamic routes `/plan/<int:plan_id>` and `/trainer/<int:trainer_id>` use integer parameter names exactly as specified.

---

# Section 2: HTML Template Specifications

## 1. dashboard.html
- Page Title: Gym Membership Dashboard
- Elements and IDs:
  - `dashboard-page` (Div): Container for the entire dashboard page.
  - `member-welcome` (Div): Shows member welcome/status information.
  - `browse-membership-button` (Button): Navigates to Membership Plans page (`url_for('memberships')`).
  - `view-schedule-button` (Button): Navigates to Class Schedule page (`url_for('class_schedule')`).
  - `book-trainer-button` (Button): Navigates to Personal Training Booking page (`url_for('pt_booking')`).
- Context Variables:
  - `member_welcome_msg` (str): The welcome/status message.
  - `featured_classes` (list): List of featured classes (each a dict with keys like `class_name`, `trainer_name`, etc.) Optional for display.
  - `quick_links` (dict): Optional quick navigation references.
- Navigation:
  - Buttons with IDs link to respective pages via Flask's `url_for()`.

## 2. memberships.html
- Page Title: Membership Plans
- Elements and IDs:
  - `membership-page` (Div): Container for the membership plans page.
  - `plan-filter` (Dropdown): Filter membership plans by type (Basic, Premium, Elite).
  - `plans-grid` (Div): Displays all plan cards.
    - Each card includes a `view-details-button-{plan_id}` (Button) to view details.
  - `back-to-dashboard` (Button): Navigates back to Dashboard (`url_for('dashboard')`).
- Context Variables:
  - `plans` (list of dict): Each dict with keys - `membership_id`, `plan_name`, `price`, `billing_cycle`, `features`, `max_classes`.
- Navigation:
  - `back-to-dashboard` button linked to `url_for('dashboard')`.
  - `view-details-button-{plan_id}` buttons linked to `url_for('plan_details', plan_id=plan_id)`.

## 3. plan_details.html
- Page Title: Plan Details
- Elements and IDs:
  - `plan-details-page` (Div): Container for plan details page.
  - `plan-title` (H1): Displays plan name.
  - `plan-price` (Div): Displays plan price and billing cycle.
  - `plan-features` (Div): Displays plan features.
  - `enroll-plan-button` (Button): Button to enroll.
  - `plan-reviews` (Div): Displays reviews related to the plan.
- Context Variables:
  - `plan` (dict): Keys - `membership_id`, `plan_name`, `price`, `billing_cycle`, `features`, `max_classes`.
  - `reviews` (list of dict): Reviews for this plan.
- Navigation:
  - `enroll-plan-button` can link to any enrollment handling route (not specified).

## 4. class_schedule.html
- Page Title: Class Schedule
- Elements and IDs:
  - `schedule-page` (Div): Container for class schedule.
  - `schedule-search` (Input): Text input to search classes by name or trainer.
  - `schedule-filter` (Dropdown): Filter by class type (Yoga, CrossFit, Pilates, Boxing, etc.).
  - `classes-grid` (Div): Displays class cards.
    - Each card has `enroll-class-button-{class_id}` (Button) to enroll.
- Context Variables:
  - `classes` (list of dict): Each dict includes `class_id`, `class_name`, `trainer_name`, `class_type`, `schedule_day`, `schedule_time`, `capacity`, `duration`.
- Navigation:
  - `enroll-class-button-{class_id}` buttons to trigger enroll action (link or JS handled).

## 5. trainer_profiles.html
- Page Title: Trainer Profiles
- Elements and IDs:
  - `trainers-page` (Div): Container for trainers page.
  - `trainer-search` (Input): Search trainers by name or specialty.
  - `specialty-filter` (Dropdown): Filter by specialty (Strength, Cardio, Flexibility, Weight Loss).
  - `trainers-grid` (Div): Displays trainer cards.
    - Each card has `view-trainer-button-{trainer_id}` (Button) to view trainer details.
- Context Variables:
  - `trainers` (list of dict): Each with keys `trainer_id`, `name`, `specialty`, `certifications`, `experience_years`.
- Navigation:
  - `view-trainer-button-{trainer_id}` buttons linked to `url_for('trainer_detail', trainer_id=trainer_id)`.

## 6. trainer_detail.html
- Page Title: Trainer Profile
- Elements and IDs:
  - `trainer-detail-page` (Div): Container for trainer detail.
  - `trainer-name` (H1): Displays trainer name.
  - `trainer-bio` (Div): Shows biography and experience.
  - `trainer-certifications` (Div): Shows certifications.
  - `book-session-button` (Button): To book a session with this trainer.
  - `trainer-reviews` (Div): Shows client reviews.
- Context Variables:
  - `trainer` (dict): Keys `trainer_id`, `name`, `specialty`, `certifications`, `experience_years`, `bio`.
  - `reviews` (list of dict): Reviews from clients.
- Navigation:
  - `book-session-button` can link to booking page with pre-selected trainer.

## 7. pt_booking.html
- Page Title: Book Personal Training
- Elements and IDs:
  - `booking-page` (Div): Container for booking page.
  - `select-trainer` (Dropdown): Select trainer from available trainers.
  - `session-date` (Input - date): Select session date.
  - `session-time` (Dropdown): Select session time slot.
  - `session-duration` (Dropdown): Select session duration (30, 60, 90 minutes).
  - `confirm-booking-button` (Button): Confirm the booking submission.
- Context Variables:
  - `trainers` (list of dict): Each dict with keys `trainer_id`, `name`.
- Navigation:
  - `confirm-booking-button` triggers POST to `/booking`.

## 8. workout_records.html
- Page Title: My Workout Records
- Elements and IDs:
  - `workouts-page` (Div): Container for workout records.
  - `workouts-table` (Table): Displays workout history with columns for date, type, duration, calories burned.
  - `filter-by-type` (Dropdown): Filter workouts by type (Class, PT Session, Personal).
  - `log-workout-button` (Button): Navigates to Log Workout page (`url_for('log_workout')`).
  - `back-to-dashboard` (Button): Navigate back to dashboard (`url_for('dashboard')`).
- Context Variables:
  - `workouts` (list of dict): Each with keys `workout_id`, `member_name`, `workout_type`, `workout_date`, `duration_minutes`, `calories_burned`, `notes`.
- Navigation:
  - `log-workout-button` linked to `url_for('log_workout')`.
  - `back-to-dashboard` linked to `url_for('dashboard')`.

## 9. log_workout.html
- Page Title: Log Workout
- Elements and IDs:
  - `log-workout-page` (Div): Container for the log workout page.
  - `workout-type` (Dropdown): Options Cardio, Strength, Flexibility, Sports.
  - `workout-duration` (Input - number): Input duration in minutes.
  - `calories-burned` (Input - number): Input calories burned.
  - `workout-notes` (Textarea): Notes about the workout.
  - `submit-workout-button` (Button): Submit workout record.
- Context Variables:
  - None (static form).
- Navigation:
  - `submit-workout-button` triggers POST to `/log-workout`.

---

# Section 3: Data File Schemas

## 1. Memberships Data
- File Path: data/memberships.txt
- Format (pipe-delimited fields):
  1. membership_id (int)
  2. plan_name (str)
  3. price (float)
  4. billing_cycle (str) - e.g., "monthly"
  5. features (str) - comma-separated textual features
  6. max_classes (int or str)

- Description: Contains membership plans details including pricing and benefits.

- Example Data:
  ```
  1|Basic|29.99|monthly|Gym access, 2 classes per week|8
  2|Premium|59.99|monthly|Gym access, 5 classes per week, 2 PT sessions|20
  3|Elite|99.99|monthly|Unlimited gym access, unlimited classes, 4 PT sessions, nutrition coaching|unlimited
  ```

## 2. Classes Data
- File Path: data/classes.txt
- Format:
  1. class_id (int)
  2. class_name (str)
  3. trainer_id (int)
  4. class_type (str)
  5. schedule_day (str) - e.g., Monday, Tuesday
  6. schedule_time (str) - 24h format HH:MM
  7. capacity (int)
  8. duration (int) - in minutes

- Description: Details for fitness classes including schedule and capacity.

- Example Data:
  ```
  1|Morning Yoga|1|Yoga|Monday|06:00|20|60
  2|CrossFit Bootcamp|2|CrossFit|Tuesday|18:00|15|45
  3|Pilates Core|3|Pilates|Wednesday|10:00|18|50
  ```

## 3. Trainers Data
- File Path: data/trainers.txt
- Format:
  1. trainer_id (int)
  2. name (str)
  3. specialty (str)
  4. certifications (str) - comma-separated
  5. experience_years (int)
  6. bio (str)

- Description: Trainer profile information including expertise and biography.

- Example Data:
  ```
  1|Sarah Johnson|Yoga & Flexibility|Certified Yoga Instructor, CPR|8|Expert in mind-body wellness and injury prevention
  2|Mike Thompson|Strength & Conditioning|NASM-CPT, CrossFit Level 2|10|Specializes in powerlifting and functional fitness
  3|Emma Davis|Pilates|Pilates Method Alliance Certified|6|Focus on core strength and postural alignment
  ```

## 4. Bookings Data
- File Path: data/bookings.txt
- Format:
  1. booking_id (int)
  2. member_name (str)
  3. trainer_id (int)
  4. booking_date (str) - YYYY-MM-DD
  5. booking_time (str) - HH:MM
  6. duration_minutes (int)
  7. status (str) - e.g., Confirmed, Pending

- Description: Personal training session bookings details.

- Example Data:
  ```
  1|John Doe|1|2025-01-20|10:00|60|Confirmed
  2|Jane Smith|2|2025-01-21|14:00|45|Confirmed
  3|Alex Johnson|3|2025-01-22|16:00|60|Pending
  ```

## 5. Workouts Data
- File Path: data/workouts.txt
- Format:
  1. workout_id (int)
  2. member_name (str)
  3. workout_type (str)
  4. workout_date (str) - YYYY-MM-DD
  5. duration_minutes (int)
  6. calories_burned (int)
  7. notes (str)

- Description: Records of personal workout sessions and progress tracking.

- Example Data:
  ```
  1|John Doe|Cardio|2025-01-15|45|350|Morning run on treadmill
  2|Jane Smith|Strength|2025-01-16|60|420|Upper body weight training with trainer
  3|Alex Johnson|Class|2025-01-17|50|380|CrossFit Bootcamp session
  ```

---

End of GymMembership Design Specification
