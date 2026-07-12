# GymMembership Web Application Design Specification

---

# Section 1: Flask Routes Specification

| Route Path                  | Function Name           | HTTP Method(s) | Template File       | Context Variables (Name : Type)                                                                                  |
|-----------------------------|-------------------------|----------------|---------------------|-----------------------------------------------------------------------------------------------------------------|
| `/`                         | root_redirect           | GET            | None (redirect)      | None                                                                                                            |
| `/dashboard`                | dashboard               | GET            | dashboard.html      | None                                                                                                            |
| `/memberships`              | memberships             | GET            | memberships.html    | `plans: list[dict]` (membership_id:int, plan_name:str, price:str, billing_cycle:str, features:str, max_classes:str) |
| `/plan/<int:plan_id>`       | plan_details            | GET            | plan_details.html   | `plan: dict` (membership_id:int, plan_name:str, price:str, billing_cycle:str, features:str, max_classes:str), `reviews: list[str]` (optional) |
| `/classes`                  | class_schedule          | GET            | classes.html        | `classes: list[dict]` (class_id:int, class_name:str, trainer_id:int, class_type:str, schedule_day:str, schedule_time:str, capacity:int, duration:int) |
| `/trainers`                 | trainers                | GET            | trainers.html       | `trainers: list[dict]` (trainer_id:int, name:str, specialty:str, certifications:str, experience_years:int, bio:str) |
| `/trainer/<int:trainer_id>` | trainer_detail          | GET            | trainer_detail.html | `trainer: dict` (trainer_id:int, name:str, specialty:str, certifications:str, experience_years:int, bio:str), `reviews: list[str]` (optional) |
| `/pt_booking`               | pt_booking              | GET            | pt_booking.html     | `trainers: list[dict]` (trainer_id:int, name:str, specialty:str, certifications:str, experience_years:int, bio:str) |
| `/pt_booking`               | pt_booking_submit       | POST           | None (redirect/render) | Form data submitted for booking confirmation                                                                   |
| `/workouts`                 | workout_records         | GET            | workouts.html       | `workouts: list[dict]` (workout_id:int, member_name:str, workout_type:str, workout_date:str, duration_minutes:int, calories_burned:int, notes:str) |
| `/log_workout`              | log_workout             | GET            | log_workout.html    | None                                                                                                            |
| `/log_workout`              | log_workout_submit      | POST           | None (redirect/render) | Form data submitted for logging workout                                                                        |

---

# Section 2: HTML Template Specifications

## 1. dashboard.html
- Page Title: Gym Membership Dashboard
- Elements:
  - `dashboard-page` (Div): Main container
  - `member-welcome` (Div): Shows welcome message and member status
  - `browse-membership-button` (Button): Navigates to membership plans (`url_for('memberships')`)
  - `view-schedule-button` (Button): Navigates to class schedule (`url_for('class_schedule')`)
  - `book-trainer-button` (Button): Navigates to PT booking (`url_for('pt_booking')`)
- Context Variables: None

## 2. memberships.html
- Page Title: Membership Plans
- Elements:
  - `membership-page` (Div): Container for membership plans list
  - `plan-filter` (Dropdown): Filter plans by Basic, Premium, Elite
  - `plans-grid` (Div): Plan cards container
  - `view-details-button-{{ plan.membership_id }}` (Button): Button to view individual plan details
  - `back-to-dashboard` (Button): Navigates back to dashboard (`url_for('dashboard')`)
- Context Variables:
  - `plans`: List of membership plan dicts
  - Accessible through Jinja2: `{% for plan in plans %}` loop

## 3. plan_details.html
- Page Title: Plan Details
- Elements:
  - `plan-details-page` (Div): Container for plan details
  - `plan-title` (H1): Plan name display
  - `plan-price` (Div): Price and billing cycle
  - `plan-features` (Div): Features list
  - `enroll-plan-button` (Button): Enroll in selected plan
  - `plan-reviews` (Div): Member reviews section
- Context Variables:
  - `plan`: dict with plan details
  - `reviews`: optional list of review strings

## 4. classes.html
- Page Title: Class Schedule
- Elements:
  - `schedule-page` (Div): Container for schedule
  - `schedule-search` (Input): Search box for classes by name or trainer
  - `schedule-filter` (Dropdown): Filter classes by type
  - `classes-grid` (Div): Grid display of class cards
  - `enroll-class-button-{{ class.class_id }}` (Button): Button to enroll in class
- Context Variables:
  - `classes`: List of class dicts
  - Use `{% for class in classes %}` to iterate

## 5. trainers.html
- Page Title: Trainer Profiles
- Elements:
  - `trainers-page` (Div): Container for trainers listing
  - `trainer-search` (Input): Search trainers by name or specialty
  - `specialty-filter` (Dropdown): Filter trainers by specialty
  - `trainers-grid` (Div): Grid of trainer cards
  - `view-trainer-button-{{ trainer.trainer_id }}` (Button): Button to view trainer details
- Context Variables:
  - `trainers`: List of trainer dicts

## 6. trainer_detail.html
- Page Title: Trainer Profile
- Elements:
  - `trainer-detail-page` (Div): Container for profile details
  - `trainer-name` (H1): Trainer full name
  - `trainer-bio` (Div): Biography and experience
  - `trainer-certifications` (Div): Certifications list
  - `book-session-button` (Button): Book session with trainer
  - `trainer-reviews` (Div): Client reviews section
- Context Variables:
  - `trainer`: Dict with trainer data
  - `reviews`: Optional list of strings

## 7. pt_booking.html
- Page Title: Book Personal Training
- Elements:
  - `booking-page` (Div): Main container
  - `select-trainer` (Dropdown): Dropdown listing trainers
  - `session-date` (Input, date): Date picker
  - `session-time` (Dropdown): Time slot selector
  - `session-duration` (Dropdown): Duration choices (30, 60, 90 minutes)
  - `confirm-booking-button` (Button): Confirm booking
- Context Variables:
  - `trainers`: List of trainer dicts

## 8. workouts.html
- Page Title: My Workout Records
- Elements:
  - `workouts-page` (Div): Container for workout records
  - `workouts-table` (Table): Display workout history records
  - `filter-by-type` (Dropdown): Filter workouts by type
  - `log-workout-button` (Button): Navigate to log workout page (`url_for('log_workout')`)
  - `back-to-dashboard` (Button): Navigate to dashboard (`url_for('dashboard')`)
- Context Variables:
  - `workouts`: List of workout dicts

## 9. log_workout.html
- Page Title: Log Workout
- Elements:
  - `log-workout-page` (Div): Container
  - `workout-type` (Dropdown): Select workout type
  - `workout-duration` (Input, number): Duration input
  - `calories-burned` (Input, number): Calories burned input
  - `workout-notes` (Textarea): Notes field
  - `submit-workout-button` (Button): Submit workout record
- Context Variables: None

---

# Section 3: Data File Schemas

### 1. Memberships Data
- File Path: `data/memberships.txt`
- Pipe-delimited Fields:
  1. membership_id (int)
  2. plan_name (str)
  3. price (str) (e.g., "29.99")
  4. billing_cycle (str) (e.g., "monthly")
  5. features (str) (comma-separated values)
  6. max_classes (str) (number or "unlimited")
- Description: List of all gym membership plans with pricing and features.
- Example Rows:
```
1|Basic|29.99|monthly|Gym access, 2 classes per week|8
2|Premium|59.99|monthly|Gym access, 5 classes per week, 2 PT sessions|20
3|Elite|99.99|monthly|Unlimited gym access, unlimited classes, 4 PT sessions, nutrition coaching|unlimited
```

### 2. Classes Data
- File Path: `data/classes.txt`
- Pipe-delimited Fields:
  1. class_id (int)
  2. class_name (str)
  3. trainer_id (int)
  4. class_type (str)
  5. schedule_day (str) (e.g., "Monday")
  6. schedule_time (str) (e.g., "06:00")
  7. capacity (int)
  8. duration (int) (minutes)
- Description: Scheduled fitness classes and their details.
- Example Rows:
```
1|Morning Yoga|1|Yoga|Monday|06:00|20|60
2|CrossFit Bootcamp|2|CrossFit|Tuesday|18:00|15|45
3|Pilates Core|3|Pilates|Wednesday|10:00|18|50
```

### 3. Trainers Data
- File Path: `data/trainers.txt`
- Pipe-delimited Fields:
  1. trainer_id (int)
  2. name (str)
  3. specialty (str)
  4. certifications (str) (comma-separated)
  5. experience_years (int)
  6. bio (str)
- Description: Information about trainers including expertise and background.
- Example Rows:
```
1|Sarah Johnson|Yoga & Flexibility|Certified Yoga Instructor, CPR|8|Expert in mind-body wellness and injury prevention
2|Mike Thompson|Strength & Conditioning|NASM-CPT, CrossFit Level 2|10|Specializes in powerlifting and functional fitness
3|Emma Davis|Pilates|Pilates Method Alliance Certified|6|Focus on core strength and postural alignment
```

### 4. Bookings Data
- File Path: `data/bookings.txt`
- Pipe-delimited Fields:
  1. booking_id (int)
  2. member_name (str)
  3. trainer_id (int)
  4. booking_date (str) (YYYY-MM-DD)
  5. booking_time (str) (HH:MM)
  6. duration_minutes (int)
  7. status (str) (e.g., "Confirmed", "Pending")
- Description: Records of personal training session bookings.
- Example Rows:
```
1|John Doe|1|2025-01-20|10:00|60|Confirmed
2|Jane Smith|2|2025-01-21|14:00|45|Confirmed
3|Alex Johnson|3|2025-01-22|16:00|60|Pending
```

### 5. Workouts Data
- File Path: `data/workouts.txt`
- Pipe-delimited Fields:
  1. workout_id (int)
  2. member_name (str)
  3. workout_type (str)
  4. workout_date (str) (YYYY-MM-DD)
  5. duration_minutes (int)
  6. calories_burned (int)
  7. notes (str)
- Description: User workout records including dates, types and notes.
- Example Rows:
```
1|John Doe|Cardio|2025-01-15|45|350|Morning run on treadmill
2|Jane Smith|Strength|2025-01-16|60|420|Upper body weight training with trainer
3|Alex Johnson|Class|2025-01-17|50|380|CrossFit Bootcamp session
```

---

*This specification ensures clarity and precision, enabling backend and frontend developers to implement the GymMembership application independently and consistently.*

*The root route (`/`) redirects to `/dashboard` as required.*

*All element IDs and context variable names are strictly consistent across all sections.*

*No additional fields or features have been added beyond user requirements.*

---
