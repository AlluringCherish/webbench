# GymMembership Application Design Specification

---

# Section 1: Flask Routes Specification

| Route Path                  | Function Name              | HTTP Methods | Template File        | Context Variables (Name : Type)                                         |
|-----------------------------|----------------------------|--------------|---------------------|------------------------------------------------------------------------|
| `/`                         | root_redirect              | GET          | N/A (redirect)      | None                                                                   |
| `/dashboard`                | dashboard                 | GET          | dashboard.html      | member_welcome_msg : str, featured_classes : list of dict, quick_links : dict[str:str] |
| `/memberships`              | memberships               | GET          | memberships.html    | memberships : list of dict (membership_id:int, plan_name:str, price:str, billing_cycle:str, features:str, max_classes:str) |
| `/plan/<int:plan_id>`       | plan_details              | GET          | plan_details.html   | plan : dict (membership_id:int, plan_name:str, price:str, billing_cycle:str, features:str, max_classes:str), reviews : list of dict (review_text:str, member_name:str) |
| `/classes`                 | class_schedule            | GET          | class_schedule.html | classes : list of dict (class_id:int, class_name:str, trainer_id:int, class_type:str, schedule_day:str, schedule_time:str, capacity:int, duration:int) |
| `/trainers`                | trainer_profiles          | GET          | trainers.html       | trainers : list of dict (trainer_id:int, name:str, specialty:str, certifications:str, experience_years:int, bio:str) |
| `/trainer/<int:trainer_id>` | trainer_detail            | GET          | trainer_detail.html | trainer : dict (trainer_id:int, name:str, specialty:str, certifications:str, experience_years:int, bio:str), reviews : list of dict (review_text:str, client_name:str) |
| `/booking`                 | pt_booking                | GET, POST   | booking.html        | trainers : list of dict (trainer_id:int, name:str), booking_status : str (only POST response after submission) |
| `/workouts`                | workout_records           | GET          | workouts.html       | workouts : list of dict (workout_id:int, member_name:str, workout_type:str, workout_date:str, duration_minutes:int, calories_burned:int, notes:str) |
| `/log_workout`             | log_workout               | GET, POST   | log_workout.html    | log_status : str (only POST response after submission)                |


**Route Details:**

- Root route `/` redirects (HTTP 302) to `/dashboard`.
- Dynamic routes `/plan/<int:plan_id>` and `/trainer/<int:trainer_id>` include numeric parameters named `plan_id` and `trainer_id` respectively.
- POST methods required on `/booking` and `/log_workout` for form submissions.
- Context variables are precisely named and typed to enable data rendering.

---

# Section 2: HTML Template Specifications

## 1. dashboard.html
- Page Title: "Gym Membership Dashboard"
- Element IDs and Types:
  - `dashboard-page`: Div - main container
  - `member-welcome`: Div - welcome message for member
  - `browse-membership-button`: Button - navigate to memberships page (url_for('memberships'))
  - `view-schedule-button`: Button - navigate to class schedule page (url_for('class_schedule'))
  - `book-trainer-button`: Button - navigate to booking page (url_for('pt_booking'))
- Context Variables:
  - `member_welcome_msg` (str) - displayed inside `member-welcome`
  - `featured_classes` (list of dict) - each dict includes keys: class_name, schedule_day, schedule_time
  - `quick_links` (dict[str:str]) - mapping button IDs to routes for navigation (used internally or for logic)

## 2. memberships.html
- Page Title: "Membership Plans"
- Element IDs and Types:
  - `membership-page`: Div - container
  - `plan-filter`: Dropdown - filter by membership type
  - `plans-grid`: Div - grid containing membership plan cards
  - `view-details-button-{plan_id}`: Button - view details for each plan card
  - `back-to-dashboard`: Button - navigate back to dashboard (url_for('dashboard'))
- Context Variables:
  - `memberships` (list of dict) - keys: membership_id, plan_name, price, billing_cycle, features, max_classes
- Dynamic IDs example: `view-details-button-{{ plan.membership_id }}`

## 3. plan_details.html
- Page Title: "Plan Details"
- Element IDs and Types:
  - `plan-details-page`: Div - container
  - `plan-title`: H1 - plan name
  - `plan-price`: Div - price and billing cycle
  - `plan-features`: Div - features list
  - `enroll-plan-button`: Button - enroll action
  - `plan-reviews`: Div - list of member reviews
- Context Variables:
  - `plan` (dict)
  - `reviews` (list of dict) - each dict: review_text, member_name

## 4. class_schedule.html
- Page Title: "Class Schedule"
- Element IDs and Types:
  - `schedule-page`: Div - container
  - `schedule-search`: Input (text) - search classes by name or trainer
  - `schedule-filter`: Dropdown - filter by class type
  - `classes-grid`: Div - grid of classes
  - `enroll-class-button-{class_id}`: Button - enroll in class
- Context Variables:
  - `classes` (list of dict) - keys: class_id, class_name, trainer_id, class_type, schedule_day, schedule_time, capacity, duration
- Dynamic IDs example: `enroll-class-button-{{ class.class_id }}`

## 5. trainers.html
- Page Title: "Trainer Profiles"
- Element IDs and Types:
  - `trainers-page`: Div - container
  - `trainer-search`: Input (text) - search trainers
  - `specialty-filter`: Dropdown - filter by specialty
  - `trainers-grid`: Div - grid
  - `view-trainer-button-{trainer_id}`: Button - view trainer profile
- Context Variables:
  - `trainers` (list of dict) - keys: trainer_id, name, specialty, certifications, experience_years, bio
- Dynamic IDs example: `view-trainer-button-{{ trainer.trainer_id }}`

## 6. trainer_detail.html
- Page Title: "Trainer Profile"
- Element IDs and Types:
  - `trainer-detail-page`: Div - container
  - `trainer-name`: H1
  - `trainer-bio`: Div
  - `trainer-certifications`: Div
  - `book-session-button`: Button - book session with trainer
  - `trainer-reviews`: Div - client reviews
- Context Variables:
  - `trainer` (dict)
  - `reviews` (list of dict) - each dict: review_text, client_name

## 7. booking.html
- Page Title: "Book Personal Training"
- Element IDs and Types:
  - `booking-page`: Div - container
  - `select-trainer`: Dropdown - select trainer
  - `session-date`: Input (date) - select session date
  - `session-time`: Dropdown - select session time slot
  - `session-duration`: Dropdown - select duration
  - `confirm-booking-button`: Button - confirm booking
- Context Variables:
  - `trainers` (list of dict) - keys: trainer_id, name
  - `booking_status` (str) - optional POST response message

## 8. workouts.html
- Page Title: "My Workout Records"
- Element IDs and Types:
  - `workouts-page`: Div - container
  - `workouts-table`: Table - workout history with columns date, type, duration, calories
  - `filter-by-type`: Dropdown - filter workouts
  - `log-workout-button`: Button - log new workout
  - `back-to-dashboard`: Button - back to dashboard
- Context Variables:
  - `workouts` (list of dict) - keys: workout_id, member_name, workout_type, workout_date, duration_minutes, calories_burned, notes

## 9. log_workout.html
- Page Title: "Log Workout"
- Element IDs and Types:
  - `log-workout-page`: Div - container
  - `workout-type`: Dropdown - select workout type
  - `workout-duration`: Input (number) - input minutes
  - `calories-burned`: Input (number) - input calories
  - `workout-notes`: Textarea - notes
  - `submit-workout-button`: Button - submit workout
- Context Variables:
  - `log_status` (str) - optional POST response message



# Section 3: Data File Schemas

---

## 1. Memberships Data
- File Path: `data/memberships.txt`
- Pipe-Delimited Fields (order is critical):
  - membership_id : int
  - plan_name : str
  - price : str (e.g., "29.99")
  - billing_cycle : str (e.g., "monthly")
  - features : str (comma separated features)
  - max_classes : str (can be integer as string or "unlimited")
- Description: Contains all membership plans with pricing and features.
- Example Rows:
  ```
  1|Basic|29.99|monthly|Gym access, 2 classes per week|8
  2|Premium|59.99|monthly|Gym access, 5 classes per week, 2 PT sessions|20
  3|Elite|99.99|monthly|Unlimited gym access, unlimited classes, 4 PT sessions, nutrition coaching|unlimited
  ```

## 2. Classes Data
- File Path: `data/classes.txt`
- Pipe-Delimited Fields (order is critical):
  - class_id : int
  - class_name : str
  - trainer_id : int
  - class_type : str
  - schedule_day : str
  - schedule_time : str (HH:MM)
  - capacity : int
  - duration : int (minutes)
- Description: Contains all fitness classes schedules and details.
- Example Rows:
  ```
  1|Morning Yoga|1|Yoga|Monday|06:00|20|60
  2|CrossFit Bootcamp|2|CrossFit|Tuesday|18:00|15|45
  3|Pilates Core|3|Pilates|Wednesday|10:00|18|50
  ```

## 3. Trainers Data
- File Path: `data/trainers.txt`
- Pipe-Delimited Fields (order is critical):
  - trainer_id : int
  - name : str
  - specialty : str
  - certifications : str
  - experience_years : int
  - bio : str
- Description: Contains trainer profiles with certifications and biography.
- Example Rows:
  ```
  1|Sarah Johnson|Yoga & Flexibility|Certified Yoga Instructor, CPR|8|Expert in mind-body wellness and injury prevention
  2|Mike Thompson|Strength & Conditioning|NASM-CPT, CrossFit Level 2|10|Specializes in powerlifting and functional fitness
  3|Emma Davis|Pilates|Pilates Method Alliance Certified|6|Focus on core strength and postural alignment
  ```

## 4. Bookings Data
- File Path: `data/bookings.txt`
- Pipe-Delimited Fields (order is critical):
  - booking_id : int
  - member_name : str
  - trainer_id : int
  - booking_date : str (YYYY-MM-DD)
  - booking_time : str (HH:MM)
  - duration_minutes : int
  - status : str
- Description: Contains personal training session bookings.
- Example Rows:
  ```
  1|John Doe|1|2025-01-20|10:00|60|Confirmed
  2|Jane Smith|2|2025-01-21|14:00|45|Confirmed
  3|Alex Johnson|3|2025-01-22|16:00|60|Pending
  ```

## 5. Workouts Data
- File Path: `data/workouts.txt`
- Pipe-Delimited Fields (order is critical):
  - workout_id : int
  - member_name : str
  - workout_type : str
  - workout_date : str (YYYY-MM-DD)
  - duration_minutes : int
  - calories_burned : int
  - notes : str
- Description: Contains user's workout history and progress logs.
- Example Rows:
  ```
  1|John Doe|Cardio|2025-01-15|45|350|Morning run on treadmill
  2|Jane Smith|Strength|2025-01-16|60|420|Upper body weight training with trainer
  3|Alex Johnson|Class|2025-01-17|50|380|CrossFit Bootcamp session
  ```

---

**End of Design Specification**
