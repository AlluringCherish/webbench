# GymMembership Web Application Design Specification

---

# Section 1: Flask Routes Specification

| Route Path                 | Function Name           | HTTP Methods | Template File        | Context Variables (name: type)                                                                                      |
|----------------------------|-------------------------|--------------|----------------------|---------------------------------------------------------------------------------------------------------------------|
| `/`                        | root                    | GET          | N/A (redirect)       | None                                                                                                                |
| `/dashboard`               | dashboard               | GET          | dashboard.html       | None                                                                                                                |
| `/memberships`             | memberships             | GET          | memberships.html     | `plans`: List[Dict] with keys membership_id (int), plan_name (str), price (str), billing_cycle (str), features (str), max_classes (str or int) |
| `/plan/<int:plan_id>`      | plan_details            | GET          | plan_details.html    | `plan`: Dict with fields membership_id (int), plan_name (str), price (str), billing_cycle (str), features (str), max_classes (str or int)
`reviews`: List[Dict] (can be empty or omitted)                   |
| `/classes`                | class_schedule          | GET          | class_schedule.html  | `classes`: List[Dict] with keys class_id (int), class_name (str), trainer_id (int), class_type (str), schedule_day (str), schedule_time (str), capacity (int), duration (int) |
| `/trainers`               | trainers                | GET          | trainers.html        | `trainers`: List[Dict] with keys trainer_id (int), name (str), specialty (str), certifications (str), experience_years (int), bio (str)      |
| `/trainer/<int:trainer_id>` | trainer_detail         | GET          | trainer_detail.html  | `trainer`: Dict with fields trainer_id (int), name (str), specialty (str), certifications (str), experience_years (int), bio (str)
`reviews`: List[Dict] (optional)                          |
| `/booking`                | pt_booking              | GET, POST    | booking.html         | GET: `trainers`: List[Dict] with trainer_id (int), name (str)
POST: handles form submission, no context returned                 |
| `/workouts`               | workout_records         | GET          | workouts.html        | `workouts`: List[Dict] with workout_id (int), member_name (str), workout_type (str), workout_date (str), duration_minutes (int), calories_burned (int), notes (str) |
| `/log-workout`            | log_workout             | GET, POST    | log_workout.html     | GET: None
POST: handles form submission, no context returned                                                          |


---

# Section 2: HTML Template Specifications

## 1. dashboard.html
- Page Title: Gym Membership Dashboard
- Element IDs:
  - `dashboard-page` (div): main container
  - `member-welcome` (div): welcome section
  - `browse-membership-button` (button): navigates to `/memberships` (`url_for('memberships')`)
  - `view-schedule-button` (button): navigates to `/classes` (`url_for('class_schedule')`)
  - `book-trainer-button` (button): navigates to `/booking` (`url_for('pt_booking')`)
- Context Variables: None

## 2. memberships.html
- Page Title: Membership Plans
- Element IDs:
  - `membership-page` (div): main container
  - `plan-filter` (dropdown): filter by membership type (Basic, Premium, Elite)
  - `plans-grid` (div): contains membership plan cards
  - `view-details-button-{plan_id}` (button): each with dynamic `plan_id`, links to `/plan/<plan_id>` via `url_for('plan_details', plan_id=plan_id)`
  - `back-to-dashboard` (button): navigate to `/dashboard` (`url_for('dashboard')`)
- Context Variables:
  - `plans`: list of dicts with membership plan data

## 3. plan_details.html
- Page Title: Plan Details
- Element IDs:
  - `plan-details-page` (div): main container
  - `plan-title` (h1): displays plan name
  - `plan-price` (div): displays plan price and billing cycle
  - `plan-features` (div): displays features of the plan
  - `enroll-plan-button` (button): enroll button (no specific action defined)
  - `plan-reviews` (div): section for member reviews
- Context Variables:
  - `plan`: dict with plan details
  - `reviews`: list of review dicts

## 4. class_schedule.html
- Page Title: Class Schedule
- Element IDs:
  - `schedule-page` (div): container
  - `schedule-search` (input): search input
  - `schedule-filter` (dropdown): filters for class type
  - `classes-grid` (div): grid containing class cards
  - `enroll-class-button-{class_id}` (button): each with dynamic ID, enrolls in class
- Context Variables:
  - `classes`: list of class dicts

## 5. trainers.html
- Page Title: Trainer Profiles
- Element IDs:
  - `trainers-page` (div): container
  - `trainer-search` (input): search input
  - `specialty-filter` (dropdown): filters by specialty
  - `trainers-grid` (div): grid of trainer cards
  - `view-trainer-button-{trainer_id}` (button): each with dynamic ID, links to trainer detail
- Context Variables:
  - `trainers`: list of trainer dicts

## 6. trainer_detail.html
- Page Title: Trainer Profile
- Element IDs:
  - `trainer-detail-page` (div): container
  - `trainer-name` (h1): trainer's name
  - `trainer-bio` (div): biography and experience
  - `trainer-certifications` (div): certifications
  - `book-session-button` (button): book session button
  - `trainer-reviews` (div): client reviews
- Context Variables:
  - `trainer`: dict
  - `reviews`: list

## 7. booking.html
- Page Title: Book Personal Training
- Element IDs:
  - `booking-page` (div): container
  - `select-trainer` (dropdown): list of trainers
  - `session-date` (input date): date selector
  - `session-time` (dropdown): session time options
  - `session-duration` (dropdown): options 30, 60, 90 minutes
  - `confirm-booking-button` (button): confirm booking
- Context Variables:
  - `trainers`: list of dicts with `trainer_id`, `name`

## 8. workouts.html
- Page Title: My Workout Records
- Element IDs:
  - `workouts-page` (div): container
  - `workouts-table` (table): displays date, type, duration, calories
  - `filter-by-type` (dropdown): filters workout types
  - `log-workout-button` (button): navigates to `/log-workout` (`url_for('log_workout')`)
  - `back-to-dashboard` (button): navigates to `/dashboard` (`url_for('dashboard')`)
- Context Variables:
  - `workouts`: list of workout dicts

## 9. log_workout.html
- Page Title: Log Workout
- Element IDs:
  - `log-workout-page` (div): container
  - `workout-type` (dropdown): workout type selector
  - `workout-duration` (input number): duration input
  - `calories-burned` (input number): calories input
  - `workout-notes` (textarea): notes
  - `submit-workout-button` (button): submission button
- Context Variables: None


Note: All dynamic IDs use Jinja2 syntax, e.g., `view-details-button-{{ plan.membership_id }}`.
Navigation buttons use Flask's `url_for()` with exact function names.

---

# Section 3: Data File Schemas

## 1. Memberships Data
- File: `data/memberships.txt`
- Format:
  ```
  membership_id|plan_name|price|billing_cycle|features|max_classes
  ```
- Fields:
  - membership_id (int): Unique ID
  - plan_name (str): Plan name
  - price (str): Price
  - billing_cycle (str): Billing cycle
  - features (str): Features description
  - max_classes (str or int): Max allowed classes, integer or "unlimited"
- Examples:
  ```
  1|Basic|29.99|monthly|Gym access, 2 classes per week|8
  2|Premium|59.99|monthly|Gym access, 5 classes per week, 2 PT sessions|20
  3|Elite|99.99|monthly|Unlimited gym access, unlimited classes, 4 PT sessions, nutrition coaching|unlimited
  ```

## 2. Classes Data
- File: `data/classes.txt`
- Format:
  ```
  class_id|class_name|trainer_id|class_type|schedule_day|schedule_time|capacity|duration
  ```
- Fields:
  - class_id (int): unique
  - class_name (str)
  - trainer_id (int)
  - class_type (str)
  - schedule_day (str)
  - schedule_time (str) (HH:MM)
  - capacity (int)
  - duration (int) (minutes)
- Examples:
  ```
  1|Morning Yoga|1|Yoga|Monday|06:00|20|60
  2|CrossFit Bootcamp|2|CrossFit|Tuesday|18:00|15|45
  3|Pilates Core|3|Pilates|Wednesday|10:00|18|50
  ```

## 3. Trainers Data
- File: `data/trainers.txt`
- Format:
  ```
  trainer_id|name|specialty|certifications|experience_years|bio
  ```
- Fields:
  - trainer_id (int)
  - name (str)
  - specialty (str)
  - certifications (str)
  - experience_years (int)
  - bio (str)
- Examples:
  ```
  1|Sarah Johnson|Yoga & Flexibility|Certified Yoga Instructor, CPR|8|Expert in mind-body wellness and injury prevention
  2|Mike Thompson|Strength & Conditioning|NASM-CPT, CrossFit Level 2|10|Specializes in powerlifting and functional fitness
  3|Emma Davis|Pilates|Pilates Method Alliance Certified|6|Focus on core strength and postural alignment
  ```

## 4. Bookings Data
- File: `data/bookings.txt`
- Format:
  ```
  booking_id|member_name|trainer_id|booking_date|booking_time|duration_minutes|status
  ```
- Fields:
  - booking_id (int)
  - member_name (str)
  - trainer_id (int)
  - booking_date (str) (YYYY-MM-DD)
  - booking_time (str) (HH:MM)
  - duration_minutes (int)
  - status (str)
- Examples:
  ```
  1|John Doe|1|2025-01-20|10:00|60|Confirmed
  2|Jane Smith|2|2025-01-21|14:00|45|Confirmed
  3|Alex Johnson|3|2025-01-22|16:00|60|Pending
  ```

## 5. Workouts Data
- File: `data/workouts.txt`
- Format:
  ```
  workout_id|member_name|workout_type|workout_date|duration_minutes|calories_burned|notes
  ```
- Fields:
  - workout_id (int)
  - member_name (str)
  - workout_type (str)
  - workout_date (str) (YYYY-MM-DD)
  - duration_minutes (int)
  - calories_burned (int)
  - notes (str)
- Examples:
  ```
  1|John Doe|Cardio|2025-01-15|45|350|Morning run on treadmill
  2|Jane Smith|Strength|2025-01-16|60|420|Upper body weight training with trainer
  3|Alex Johnson|Class|2025-01-17|50|380|CrossFit Bootcamp session
  ```

---

End of Design Specification.
