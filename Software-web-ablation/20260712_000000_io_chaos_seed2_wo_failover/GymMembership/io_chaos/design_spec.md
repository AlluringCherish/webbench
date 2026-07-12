# GymMembership Web Application Design Specification

---

## Section 1: Flask Routes Specification

| Route Path                 | Function Name             | HTTP Methods | Template File         | Context Variables (name: type)                                                                                      |
|----------------------------|---------------------------|--------------|-----------------------|--------------------------------------------------------------------------------------------------------------------|
| `/`                        | root_redirect             | GET          | Redirect to `/dashboard` | None                                                                                                                |
| `/dashboard`               | dashboard                 | GET          | dashboard.html        | None                                                                                                               |
| `/memberships`             | memberships               | GET          | memberships.html       | memberships: list of dict {membership_id: int, plan_name: str, price: float, billing_cycle: str, features: str, max_classes: str} |
| `/plan/<int:plan_id>`       | plan_details              | GET          | plan_details.html      | plan: dict {membership_id: int, plan_name: str, price: float, billing_cycle: str, features: str, max_classes: str}
|                             |                           |              |                       | plan_reviews: list of dict {reviewer_name: str, review_text: str} (if reviews are modeled)
| `/schedule`                | class_schedule            | GET          | schedule.html          | classes: list of dict {class_id: int, class_name: str, trainer_id: int, class_type: str, schedule_day: str, schedule_time: str, capacity: int, duration: int} |
| `/trainers`                | trainers_profiles         | GET          | trainers.html          | trainers: list of dict {trainer_id: int, name: str, specialty: str, certifications: str, experience_years: int, bio: str}                                                                       |
| `/trainer/<int:trainer_id>` | trainer_detail            | GET          | trainer_detail.html    | trainer: dict {trainer_id: int, name: str, specialty: str, certifications: str, experience_years: int, bio: str}
|                             |                           |              |                       | trainer_reviews: list of dict {reviewer_name: str, review_text: str} (if reviews are modeled)
| `/book-pt`                 | pt_booking                | GET, POST    | booking.html           | GET: trainers: list of dict {trainer_id: int, name: str}
|                             |                           |              |                       | POST: form data to book a session, feedback messages (success/failure)                                              |
| `/workouts`                | workout_records           | GET          | workouts.html          | workouts: list of dict {workout_id: int, member_name: str, workout_type: str, workout_date: str, duration_minutes: int, calories_burned: int, notes: str}                              |
| `/log-workout`             | log_workout               | GET, POST    | log_workout.html       | GET: None
|                             |                           |              |                       | POST: form submission results (success/failure)                                                                    |


### Notes:
- Root route `/` redirects to `/dashboard` using Flask's `redirect(url_for('dashboard'))`.
- For dynamic routes `/plan/<int:plan_id>` and `/trainer/<int:trainer_id>`, function parameters are `plan_id` and `trainer_id` respectively.
- POST methods exist on `/book-pt` and `/log-workout` for handling form submissions.
- Context variables are named for clarity and must be passed exactly to templates.

---

## Section 2: HTML Template Specifications

### 1. dashboard.html
- **Page Title:** Gym Membership Dashboard
- **Element IDs:**
  - `dashboard-page` (Div): Container for the whole page.
  - `member-welcome` (Div): Welcome message with member status.
  - `browse-membership-button` (Button): Navigates to memberships page (`url_for('memberships')`).
  - `view-schedule-button` (Button): Navigates to schedule page (`url_for('class_schedule')`).
  - `book-trainer-button` (Button): Navigates to PT booking page (`url_for('pt_booking')`).
- **Context Variables:** None
- **Navigation:** Buttons with IDs navigate to respective pages.

### 2. memberships.html
- **Page Title:** Membership Plans
- **Element IDs:**
  - `membership-page` (Div): Container for the membership plans page.
  - `plan-filter` (Dropdown): Filter by membership type (Basic, Premium, Elite).
  - `plans-grid` (Div): Grid of membership plan cards.
  - `view-details-button-{{plan.membership_id}}` (Button): View details for each plan.
  - `back-to-dashboard` (Button): Navigate back to dashboard (`url_for('dashboard')`).
- **Context Variables:**
  - `memberships`: Loop over as `{% for plan in memberships %}`
    - Access plan fields: `plan.membership_id`, `plan.plan_name`, `plan.price`, `plan.billing_cycle`, `plan.features`, `plan.max_classes`.
- **Navigation:**
  - `view-details-button-{{plan.membership_id}}` links to `url_for('plan_details', plan_id=plan.membership_id)`.
  - `back-to-dashboard` navigates to dashboard.

### 3. plan_details.html
- **Page Title:** Plan Details
- **Element IDs:**
  - `plan-details-page` (Div): Container for plan details.
  - `plan-title` (H1): Shows plan name (`{{ plan.plan_name }}`).
  - `plan-price` (Div): Shows price and billing cycle (`{{ plan.price }}`, `{{ plan.billing_cycle }}`).
  - `plan-features` (Div): Shows features (`{{ plan.features }}`).
  - `enroll-plan-button` (Button): Button to enroll in plan.
  - `plan-reviews` (Div): Display list of reviews if available.
- **Context Variables:**
  - `plan`: Dict with plan info.
  - `plan_reviews`: Optional list for reviews, loop as `{% for review in plan_reviews %}`.

### 4. schedule.html
- **Page Title:** Class Schedule
- **Element IDs:**
  - `schedule-page` (Div): Container for schedule page.
  - `schedule-search` (Input): Text input for searching classes or trainers.
  - `schedule-filter` (Dropdown): Filter by class type.
  - `classes-grid` (Div): Grid of class cards.
  - `enroll-class-button-{{class.class_id}}` (Button): Button to enroll in each class.
- **Context Variables:**
  - `classes`: Loop as `{% for class in classes %}`
    - Access fields: `class.class_id`, `class.class_name`, `class.trainer_id`, `class.class_type`, `class.schedule_day`, `class.schedule_time`, `class.capacity`, `class.duration`.
- **Navigation:** None specific.

### 5. trainers.html
- **Page Title:** Trainer Profiles
- **Element IDs:**
  - `trainers-page` (Div): Container for trainers page.
  - `trainer-search` (Input): Search trainers by name or specialty.
  - `specialty-filter` (Dropdown): Filter by specialty.
  - `trainers-grid` (Div): Grid of trainer cards.
  - `view-trainer-button-{{trainer.trainer_id}}` (Button): View individual trainer profile.
- **Context Variables:**
  - `trainers`: Loop as `{% for trainer in trainers %}`
    - Access fields: `trainer.trainer_id`, `trainer.name`, `trainer.specialty`, `trainer.certifications`, `trainer.experience_years`, `trainer.bio`.
- **Navigation:**
  - `view-trainer-button-{{trainer.trainer_id}}` links to `url_for('trainer_detail', trainer_id=trainer.trainer_id)`.

### 6. trainer_detail.html
- **Page Title:** Trainer Profile
- **Element IDs:**
  - `trainer-detail-page` (Div): Container for trainer details.
  - `trainer-name` (H1): Displays trainer name (`{{ trainer.name }}`).
  - `trainer-bio` (Div): Displays bio (`{{ trainer.bio }}`).
  - `trainer-certifications` (Div): Displays certifications (`{{ trainer.certifications }}`).
  - `book-session-button` (Button): Book a session with this trainer.
  - `trainer-reviews` (Div): Section for client reviews if available.
- **Context Variables:**
  - `trainer`: Dict with trainer info.
  - `trainer_reviews`: Optional list, loop as `{% for review in trainer_reviews %}`.

### 7. booking.html
- **Page Title:** Book Personal Training
- **Element IDs:**
  - `booking-page` (Div): Container for booking page.
  - `select-trainer` (Dropdown): Trainer selection.
  - `session-date` (Input date): Date selection.
  - `session-time` (Dropdown): Time slot selection.
  - `session-duration` (Dropdown): Duration selection.
  - `confirm-booking-button` (Button): Confirm booking.
- **Context Variables:**
  - `trainers`: Loop as `{% for trainer in trainers %}`, access `trainer.trainer_id`, `trainer.name`.

### 8. workouts.html
- **Page Title:** My Workout Records
- **Element IDs:**
  - `workouts-page` (Div): Container for workouts page.
  - `workouts-table` (Table): Table for workout history.
  - `filter-by-type` (Dropdown): Filter workouts by type.
  - `log-workout-button` (Button): Button to navigate to log workout page.
  - `back-to-dashboard` (Button): Navigate back to dashboard.
- **Context Variables:**
  - `workouts`: Loop as `{% for workout in workouts %}`, access fields: `workout.workout_id`, `workout.member_name`, `workout.workout_type`, `workout.workout_date`, `workout.duration_minutes`, `workout.calories_burned`, `workout.notes`.
- **Navigation:**
  - `log-workout-button` links to `url_for('log_workout')`.
  - `back-to-dashboard` links to `url_for('dashboard')`.

### 9. log_workout.html
- **Page Title:** Log Workout
- **Element IDs:**
  - `log-workout-page` (Div): Container for log workout page.
  - `workout-type` (Dropdown): Select workout type.
  - `workout-duration` (Input number): Enter duration minutes.
  - `calories-burned` (Input number): Enter calories burned.
  - `workout-notes` (Textarea): Notes field.
  - `submit-workout-button` (Button): Submit workout record.
- **Context Variables:** None for GET; feedback messages may be shown after POST.


---

## Section 3: Data File Schemas

### 1. Memberships Data
- **File Path:** data/memberships.txt
- **Field Order:** membership_id|plan_name|price|billing_cycle|features|max_classes
- **Field Names and Types:**
  - membership_id: int
  - plan_name: str
  - price: float
  - billing_cycle: str
  - features: str
  - max_classes: str (could be number or "unlimited")
- **Description:** Contains available membership plans with pricing, features, and class limits.
- **Example Rows:**
  ```
  1|Basic|29.99|monthly|Gym access, 2 classes per week|8
  2|Premium|59.99|monthly|Gym access, 5 classes per week, 2 PT sessions|20
  3|Elite|99.99|monthly|Unlimited gym access, unlimited classes, 4 PT sessions, nutrition coaching|unlimited
  ```

### 2. Classes Data
- **File Path:** data/classes.txt
- **Field Order:** class_id|class_name|trainer_id|class_type|schedule_day|schedule_time|capacity|duration
- **Field Names and Types:**
  - class_id: int
  - class_name: str
  - trainer_id: int
  - class_type: str
  - schedule_day: str
  - schedule_time: str (HH:MM)
  - capacity: int
  - duration: int (minutes)
- **Description:** Fitness classes scheduled with trainer assignments and capacity.
- **Example Rows:**
  ```
  1|Morning Yoga|1|Yoga|Monday|06:00|20|60
  2|CrossFit Bootcamp|2|CrossFit|Tuesday|18:00|15|45
  3|Pilates Core|3|Pilates|Wednesday|10:00|18|50
  ```

### 3. Trainers Data
- **File Path:** data/trainers.txt
- **Field Order:** trainer_id|name|specialty|certifications|experience_years|bio
- **Field Names and Types:**
  - trainer_id: int
  - name: str
  - specialty: str
  - certifications: str
  - experience_years: int
  - bio: str
- **Description:** Trainer profiles with specializations, certifications, experience, and biography.
- **Example Rows:**
  ```
  1|Sarah Johnson|Yoga & Flexibility|Certified Yoga Instructor, CPR|8|Expert in mind-body wellness and injury prevention
  2|Mike Thompson|Strength & Conditioning|NASM-CPT, CrossFit Level 2|10|Specializes in powerlifting and functional fitness
  3|Emma Davis|Pilates|Pilates Method Alliance Certified|6|Focus on core strength and postural alignment
  ```

### 4. Bookings Data
- **File Path:** data/bookings.txt
- **Field Order:** booking_id|member_name|trainer_id|booking_date|booking_time|duration_minutes|status
- **Field Names and Types:**
  - booking_id: int
  - member_name: str
  - trainer_id: int
  - booking_date: str (YYYY-MM-DD)
  - booking_time: str (HH:MM)
  - duration_minutes: int
  - status: str
- **Description:** Personal training session bookings with member and booking details.
- **Example Rows:**
  ```
  1|John Doe|1|2025-01-20|10:00|60|Confirmed
  2|Jane Smith|2|2025-01-21|14:00|45|Confirmed
  3|Alex Johnson|3|2025-01-22|16:00|60|Pending
  ```

### 5. Workouts Data
- **File Path:** data/workouts.txt
- **Field Order:** workout_id|member_name|workout_type|workout_date|duration_minutes|calories_burned|notes
- **Field Names and Types:**
  - workout_id: int
  - member_name: str
  - workout_type: str
  - workout_date: str (YYYY-MM-DD)
  - duration_minutes: int
  - calories_burned: int
  - notes: str
- **Description:** Records of individual workouts logged by members.
- **Example Rows:**
  ```
  1|John Doe|Cardio|2025-01-15|45|350|Morning run on treadmill
  2|Jane Smith|Strength|2025-01-16|60|420|Upper body weight training with trainer
  3|Alex Johnson|Class|2025-01-17|50|380|CrossFit Bootcamp session
  ```


---

**CRITICAL SUCCESS CRITERIA**
- Backend developers have complete route specs with context variables and template names.
- Frontend developers have full template specs with IDs and navigation details.
- Data schemas detail exact file structure making data parsing exact.
- IDs and variable names are consistent and exact.
- Root route redirects to dashboard.
- No additional features beyond requirements.

---

End of GymMembership Design Specification.
