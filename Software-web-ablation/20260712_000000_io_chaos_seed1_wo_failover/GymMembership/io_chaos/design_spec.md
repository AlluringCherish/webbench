# Design Specification for GymMembership Web Application

---

## Section 1: Flask Routes Specification

| Route Path               | Function Name            | HTTP Method(s) | Template Rendered       | Context Variables (name: type)                                       |
|--------------------------|--------------------------|----------------|------------------------|---------------------------------------------------------------------|
| `/`                      | root_redirect            | GET            | Redirect to `/dashboard`| None                                                                |
| `/dashboard`             | dashboard_page           | GET            | dashboard.html          | None                                                                |
| `/memberships`           | memberships_page         | GET            | memberships.html        | plans: list of dict {membership_id: int, plan_name: str, price: float or str, billing_cycle: str, features: str, max_classes: str/int} |
| `/plan/<int:plan_id>`    | plan_details             | GET            | plan_details.html       | plan: dict {membership_id: int, plan_name: str, price: float or str, billing_cycle: str, features: str, max_classes: str/int},
                                                                   reviews: list of dict (if reviews exist, else empty list) (not explicitly defined in requirements but can be empty) |
| `/schedule`              | class_schedule           | GET            | class_schedule.html     | classes: list of dict {class_id: int, class_name: str, trainer_id: int, class_type: str, schedule_day: str, schedule_time: str, capacity: int, duration: int} |
| `/trainers`              | trainers_page            | GET            | trainers.html           | trainers: list of dict {trainer_id: int, name: str, specialty: str, certifications: str, experience_years: int, bio: str} |
| `/trainer/<int:trainer_id>`| trainer_detail          | GET            | trainer_detail.html     | trainer: dict {trainer_id: int, name: str, specialty: str, certifications: str, experience_years: int, bio: str},
                                                                      reviews: list of dict (if reviews exist, else empty list) |
| `/book`                  | pt_booking_page          | GET, POST     | booking.html            | trainers: list of dict (same as trainers data)
                                                                   (POST: form data, respond with success or error message) |
| `/workouts`              | workouts_page            | GET            | workouts.html           | workouts: list of dict {workout_id: int, member_name: str, workout_type: str, workout_date: str, duration_minutes: int, calories_burned: int, notes: str} |
| `/log_workout`           | log_workout_page         | GET, POST     | log_workout.html        | (GET: None)
                                                                   (POST: form data, confirmation or error response) |

**Notes:**
- The root `/` route will redirect users immediately to `/dashboard`.
- POST methods apply for submitting PT booking and logging workouts.
- Context variables are prepared by backend reading and parsing the respective data files.

---

## Section 2: HTML Template Specifications

### 1. dashboard.html
- Page Title: "Gym Membership Dashboard"
- Element IDs:
  - dashboard-page: Div container for dashboard page
  - member-welcome: Div for welcome message and member status
  - browse-membership-button: Button to navigate to memberships (`url_for('memberships_page')`)
  - view-schedule-button: Button to navigate to class schedule (`url_for('class_schedule')`)
  - book-trainer-button: Button to navigate to PT booking (`url_for('pt_booking_page')`)
- Navigation:
  - Buttons trigger navigation using their respective Flask route function names.
- Context variables: None

### 2. memberships.html
- Page Title: "Membership Plans"
- Element IDs:
  - membership-page: Div container
  - plan-filter: Dropdown to filter plans (Basic, Premium, Elite)
  - plans-grid: Div container displaying membership plan cards
  - view-details-button-{plan_id}: Buttons in each card to view details of plan with id `plan_id` (e.g., `view-details-button-1`)
  - back-to-dashboard: Button navigating back to dashboard
- Context Variables:
  - `plans`: Loop over with `{% for plan in plans %}`
    - Access each plan's fields by `plan.membership_id`, `plan.plan_name`, `plan.price`, `plan.billing_cycle`, `plan.features`, `plan.max_classes`
- Navigation:
  - view-details-button-{plan_id}: Links to `url_for('plan_details', plan_id=plan.membership_id)`
  - back-to-dashboard navigates to `url_for('dashboard_page')`

### 3. plan_details.html
- Page Title: "Plan Details"
- Element IDs:
  - plan-details-page: Div container
  - plan-title: H1 to display the plan name
  - plan-price: Div to show price and billing cycle
  - plan-features: Div to show plan features
  - enroll-plan-button: Button to enroll in the plan
  - plan-reviews: Div to show member reviews
- Context Variables:
  - `plan`: Dictionary with plan details
  - `reviews`: List of review dictionaries (if applicable)
- Navigation:
  - enroll-plan-button: Could trigger enrollment action (no route defined in requirements)

### 4. class_schedule.html
- Page Title: "Class Schedule"
- Element IDs:
  - schedule-page: Div container
  - schedule-search: Input field to search classes by name or trainer
  - schedule-filter: Dropdown to filter by class type (Yoga, CrossFit, Pilates, Boxing, etc.)
  - classes-grid: Div container displaying classes
  - enroll-class-button-{class_id}: Button for enrolling in class `class_id`
- Context Variables:
  - `classes`: Loop over `{% for cls in classes %}`
    - Fields accessible: `cls.class_id`, `cls.class_name`, `cls.trainer_id`, `cls.class_type`, `cls.schedule_day`, `cls.schedule_time`, `cls.capacity`, `cls.duration`
- Navigation:
  - enroll-class-button-{class_id} can submit enrollment request (no POST route specified, so hypothetical)

### 5. trainers.html
- Page Title: "Trainer Profiles"
- Element IDs:
  - trainers-page: Div container
  - trainer-search: Input to search by name or specialty
  - specialty-filter: Dropdown to filter by specialty (Strength, Cardio, Flexibility, Weight Loss)
  - trainers-grid: Div container holding trainer cards
  - view-trainer-button-{trainer_id}: Button to view trainer profile
- Context Variables:
  - `trainers`: Loop over `{% for trainer in trainers %}`
    - Fields: `trainer.trainer_id`, `trainer.name`, `trainer.specialty`, `trainer.certifications`, `trainer.experience_years`, `trainer.bio`
- Navigation:
  - view-trainer-button-{trainer_id} links to `url_for('trainer_detail', trainer_id=trainer.trainer_id)`

### 6. trainer_detail.html
- Page Title: "Trainer Profile"
- Element IDs:
  - trainer-detail-page: Div container
  - trainer-name: H1 to show trainer name
  - trainer-bio: Div to show bio and experience
  - trainer-certifications: Div for certifications
  - book-session-button: Button to book session with trainer
  - trainer-reviews: Div for client reviews
- Context Variables:
  - `trainer`: Dictionary with trainer details
  - `reviews`: List of review dicts
- Navigation:
  - book-session-button might link to booking page with trainer selected (no explicit route given)

### 7. booking.html
- Page Title: "Book Personal Training"
- Element IDs:
  - booking-page: Div container
  - select-trainer: Dropdown to select trainer
  - session-date: Input (date) to select date
  - session-time: Dropdown to select time slot
  - session-duration: Dropdown for duration (30, 60, 90 minutes)
  - confirm-booking-button: Button to confirm booking
- Context Variables:
  - `trainers`: Loop over trainers to populate select
- Navigation:
  - confirm-booking-button submits booking form POST to `/book`

### 8. workouts.html
- Page Title: "My Workout Records"
- Element IDs:
  - workouts-page: Div container
  - workouts-table: Table displaying workout history
  - filter-by-type: Dropdown to filter by workout type (Class, PT Session, Personal)
  - log-workout-button: Button to open log workout form/page
  - back-to-dashboard: Button to go back to dashboard
- Context Variables:
  - `workouts`: Loop over `{% for workout in workouts %}` with fields `workout.workout_id`, `workout.member_name`, `workout.workout_type`, `workout.workout_date`, `workout.duration_minutes`, `workout.calories_burned`, `workout.notes`
- Navigation:
  - log-workout-button links to `url_for('log_workout_page')`
  - back-to-dashboard links to `url_for('dashboard_page')`

### 9. log_workout.html
- Page Title: "Log Workout"
- Element IDs:
  - log-workout-page: Div container
  - workout-type: Dropdown (Cardio, Strength, Flexibility, Sports)
  - workout-duration: Input (number) for duration in minutes
  - calories-burned: Input (number) for calories
  - workout-notes: Textarea for notes
  - submit-workout-button: Button to submit
- Context Variables: None (form page)
- Navigation:
  - submit-workout-button posts workout log data to `/log_workout`

---

## Section 3: Data File Schemas

### 1. Memberships Data
- File Path: `data/memberships.txt`
- Fields (pipe-delimited in exact order):
  1. membership_id (int)
  2. plan_name (str)
  3. price (float or str for 'unlimited')
  4. billing_cycle (str)
  5. features (str - comma separated features as a single string)
  6. max_classes (int or str 'unlimited')
- Description: Stores membership plan details including pricing, billing, and features.
- Example Rows:
```
1|Basic|29.99|monthly|Gym access, 2 classes per week|8
2|Premium|59.99|monthly|Gym access, 5 classes per week, 2 PT sessions|20
3|Elite|99.99|monthly|Unlimited gym access, unlimited classes, 4 PT sessions, nutrition coaching|unlimited
```

### 2. Classes Data
- File Path: `data/classes.txt`
- Fields (pipe-delimited in exact order):
  1. class_id (int)
  2. class_name (str)
  3. trainer_id (int)
  4. class_type (str)
  5. schedule_day (str)
  6. schedule_time (str in HH:mm)
  7. capacity (int)
  8. duration (int in minutes)
- Description: Stores scheduled fitness classes details.
- Example Rows:
```
1|Morning Yoga|1|Yoga|Monday|06:00|20|60
2|CrossFit Bootcamp|2|CrossFit|Tuesday|18:00|15|45
3|Pilates Core|3|Pilates|Wednesday|10:00|18|50
```

### 3. Trainers Data
- File Path: `data/trainers.txt`
- Fields (pipe-delimited in exact order):
  1. trainer_id (int)
  2. name (str)
  3. specialty (str)
  4. certifications (str, comma separated)
  5. experience_years (int)
  6. bio (str)
- Description: Stores trainer profiles including specialties and certifications.
- Example Rows:
```
1|Sarah Johnson|Yoga & Flexibility|Certified Yoga Instructor, CPR|8|Expert in mind-body wellness and injury prevention
2|Mike Thompson|Strength & Conditioning|NASM-CPT, CrossFit Level 2|10|Specializes in powerlifting and functional fitness
3|Emma Davis|Pilates|Pilates Method Alliance Certified|6|Focus on core strength and postural alignment
```

### 4. Bookings Data
- File Path: `data/bookings.txt`
- Fields (pipe-delimited in exact order):
  1. booking_id (int)
  2. member_name (str)
  3. trainer_id (int)
  4. booking_date (str, YYYY-MM-DD)
  5. booking_time (str, HH:mm)
  6. duration_minutes (int)
  7. status (str, e.g. Confirmed, Pending)
- Description: Stores personal training bookings made by members.
- Example Rows:
```
1|John Doe|1|2025-01-20|10:00|60|Confirmed
2|Jane Smith|2|2025-01-21|14:00|45|Confirmed
3|Alex Johnson|3|2025-01-22|16:00|60|Pending
```

### 5. Workouts Data
- File Path: `data/workouts.txt`
- Fields (pipe-delimited in exact order):
  1. workout_id (int)
  2. member_name (str)
  3. workout_type (str)
  4. workout_date (str, YYYY-MM-DD)
  5. duration_minutes (int)
  6. calories_burned (int)
  7. notes (str)
- Description: Stores workout session records logged by members.
- Example Rows:
```
1|John Doe|Cardio|2025-01-15|45|350|Morning run on treadmill
2|Jane Smith|Strength|2025-01-16|60|420|Upper body weight training with trainer
3|Alex Johnson|Class|2025-01-17|50|380|CrossFit Bootcamp session
```

---

# End of Design Specification
