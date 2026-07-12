# GymMembership Web Application Design Specification

---

## Section 1: Flask Routes Specification

| Route Path                    | Function Name                | HTTP Method(s) | Template File           | Context Variables                                          |
|-------------------------------|------------------------------|----------------|-------------------------|------------------------------------------------------------|
| /                             | root_redirect                | GET            | None (redirect to /dashboard) |
| /dashboard                   | dashboard_page              | GET            | dashboard.html          | member_welcome_msg (str), featured_classes (list of dict), quick_nav_links (list of dict) |
| /memberships                 | membership_plans            | GET            | memberships.html        | plans (list of dict), membership_types (list of str)         |
| /plan/<int:plan_id>          | plan_details                | GET            | plan_details.html       | plan (dict), plan_reviews (list of dict)                    |
| /schedule                   | class_schedule             | GET            | schedule.html           | classes (list of dict), class_types (list of str)            |
| /trainers                   | trainer_profiles           | GET            | trainers.html           | trainers (list of dict), specialties (list of str)           |
| /trainer/<int:trainer_id>   | trainer_detail             | GET            | trainer_detail.html     | trainer (dict), trainer_reviews (list of dict)               |
| /book-training              | pt_booking                 | GET, POST      | booking.html            | trainers (list of dict), booking_status (str, optional)      |
| /workouts                  | workout_records            | GET            | workouts.html           | workouts (list of dict), workout_types (list of str)         |
| /log-workout               | log_workout                | GET, POST      | log_workout.html        | workout_types (list of str), submission_status (str, optional) |

### Notes:
- The root route `/` will issue an HTTP redirect to `/dashboard`.
- POST methods only apply for routes where form submissions occur: `/book-training` and `/log-workout`.
- Dynamic route parameters: `plan_id` for plan details and `trainer_id` for trainer details.

---

## Section 2: HTML Template Specifications

### 1. dashboard.html
- Page Title: Gym Membership Dashboard
- Element IDs:
  - dashboard-page (Div): Container for the dashboard page.
  - member-welcome (Div): Welcome section with member status information.
  - browse-membership-button (Button): Navigates to membership plans page (/memberships).
  - view-schedule-button (Button): Navigates to class schedule page (/schedule).
  - book-trainer-button (Button): Navigates to PT booking page (/book-training).
- Context Variables:
  - `member_welcome_msg` (str)
  - `featured_classes` (list of dict with keys: class_id, class_name, schedule_day, schedule_time)
  - `quick_nav_links` (list of dict with keys: label, route) - For navigation if used
- Navigation Elements:
  - browse-membership-button -> url_for('membership_plans')
  - view-schedule-button -> url_for('class_schedule')
  - book-trainer-button -> url_for('pt_booking')

### 2. memberships.html
- Page Title: Membership Plans
- Element IDs:
  - membership-page (Div): Container for the membership plans page.
  - plan-filter (Dropdown): Filter by membership type (Basic, Premium, Elite).
  - plans-grid (Div): Grid displaying membership plan cards.
  - view-details-button-{plan_id} (Button): Button for each plan card to view details.
  - back-to-dashboard (Button): Navigates back to dashboard (/dashboard).
- Context Variables:
  - `plans` (list of dict with membership plan details: membership_id, plan_name, price, billing_cycle, features, max_classes)
  - `membership_types` (list of str): ["Basic", "Premium", "Elite"]
- Navigation Elements:
  - back-to-dashboard -> url_for('dashboard_page')
  - view-details-button-{plan_id} -> url_for('plan_details', plan_id=plan_id)

### 3. plan_details.html
- Page Title: Plan Details
- Element IDs:
  - plan-details-page (Div): Container
  - plan-title (H1): Display plan name.
  - plan-price (Div): Display plan price and billing cycle.
  - plan-features (Div): Display all features.
  - enroll-plan-button (Button): Enroll in the plan.
  - plan-reviews (Div): Member reviews section.
- Context Variables:
  - `plan` (dict): keys - membership_id (int), plan_name (str), price (str), billing_cycle (str), features (str), max_classes (str)
  - `plan_reviews` (list of dict): keys - reviewer_name (str), review_text (str), rating (int)
- Navigation Elements:
  - enroll-plan-button -> Could link to enrollment action (not specified further)

### 4. schedule.html
- Page Title: Class Schedule
- Element IDs:
  - schedule-page (Div): Container
  - schedule-search (Input): Search classes by name or trainer.
  - schedule-filter (Dropdown): Filter by class type.
  - classes-grid (Div): Grid displaying class cards.
  - enroll-class-button-{class_id} (Button): Button to enroll in classes.
- Context Variables:
  - `classes` (list of dict): keys - class_id (int), class_name (str), trainer_id (int), class_type (str), schedule_day (str), schedule_time (str), capacity (int), duration (int)
  - `class_types` (list of str)
- Navigation Elements:
  - enroll-class-button-{class_id} -> url_for('class_schedule') or a booking action (not specified)

### 5. trainers.html
- Page Title: Trainer Profiles
- Element IDs:
  - trainers-page (Div): Container
  - trainer-search (Input): Search trainers by name or specialty.
  - specialty-filter (Dropdown): Filter by specialty.
  - trainers-grid (Div): Grid with trainer cards.
  - view-trainer-button-{trainer_id} (Button): View trainer profile button.
- Context Variables:
  - `trainers` (list of dict): keys - trainer_id (int), name (str), specialty (str), certifications (str), experience_years (int), bio (str)
  - `specialties` (list of str)
- Navigation Elements:
  - view-trainer-button-{trainer_id} -> url_for('trainer_detail', trainer_id=trainer_id)

### 6. trainer_detail.html
- Page Title: Trainer Profile
- Element IDs:
  - trainer-detail-page (Div): Container
  - trainer-name (H1): Trainer name
  - trainer-bio (Div): Biography and experience
  - trainer-certifications (Div): Certifications
  - book-session-button (Button): Book session with trainer
  - trainer-reviews (Div): Client reviews
- Context Variables:
  - `trainer` (dict): trainer_id (int), name (str), specialty (str), certifications (str), experience_years (int), bio (str)
  - `trainer_reviews` (list of dict): keys - reviewer_name (str), review (str), rating (int)
- Navigation Elements:
  - book-session-button -> url_for('pt_booking')

### 7. booking.html
- Page Title: Book Personal Training
- Element IDs:
  - booking-page (Div): Container
  - select-trainer (Dropdown): Select trainer
  - session-date (Input date): Select session date
  - session-time (Dropdown): Select time slot
  - session-duration (Dropdown): Select session duration
  - confirm-booking-button (Button): Confirm booking
- Context Variables:
  - `trainers` (list of dict): trainer_id, name
  - `booking_status` (str, optional): feedback message
- Navigation Elements:
  - confirm-booking-button: Submits booking form POST

### 8. workouts.html
- Page Title: My Workout Records
- Element IDs:
  - workouts-page (Div): Container
  - workouts-table (Table): Displays workout history
  - filter-by-type (Dropdown): Filter workouts
  - log-workout-button (Button): Navigate to log workout page
  - back-to-dashboard (Button): Navigate back to dashboard
- Context Variables:
  - `workouts` (list of dict): workout_id (int), member_name (str), workout_type (str), workout_date (str), duration_minutes (int), calories_burned (int), notes (str)
  - `workout_types` (list of str)
- Navigation Elements:
  - log-workout-button -> url_for('log_workout')
  - back-to-dashboard -> url_for('dashboard_page')

### 9. log_workout.html
- Page Title: Log Workout
- Element IDs:
  - log-workout-page (Div): Container
  - workout-type (Dropdown): Select workout type
  - workout-duration (Input number): Input duration in minutes
  - calories-burned (Input number): Input calories burned
  - workout-notes (Textarea): Notes about workout
  - submit-workout-button (Button): Submit workout record
- Context Variables:
  - `workout_types` (list of str)
  - `submission_status` (str, optional): feedback message
- Navigation Elements:
  - submit-workout-button: Submits workout form POST

---

## Section 3: Data File Schemas

### 1. Memberships Data
- File Path: data/memberships.txt
- Field Order & Names (pipe-delimited):
  1. membership_id (int)
  2. plan_name (str)
  3. price (str)
  4. billing_cycle (str)
  5. features (str)
  6. max_classes (str)
- Description: Contains all membership plans available along with their pricing and features.
- Example Rows:
  - 1|Basic|29.99|monthly|Gym access, 2 classes per week|8
  - 2|Premium|59.99|monthly|Gym access, 5 classes per week, 2 PT sessions|20
  - 3|Elite|99.99|monthly|Unlimited gym access, unlimited classes, 4 PT sessions, nutrition coaching|unlimited

### 2. Classes Data
- File Path: data/classes.txt
- Field Order & Names (pipe-delimited):
  1. class_id (int)
  2. class_name (str)
  3. trainer_id (int)
  4. class_type (str)
  5. schedule_day (str)
  6. schedule_time (str)
  7. capacity (int)
  8. duration (int)
- Description: Contains schedules and details of all fitness classes.
- Example Rows:
  - 1|Morning Yoga|1|Yoga|Monday|06:00|20|60
  - 2|CrossFit Bootcamp|2|CrossFit|Tuesday|18:00|15|45
  - 3|Pilates Core|3|Pilates|Wednesday|10:00|18|50

### 3. Trainers Data
- File Path: data/trainers.txt
- Field Order & Names (pipe-delimited):
  1. trainer_id (int)
  2. name (str)
  3. specialty (str)
  4. certifications (str)
  5. experience_years (int)
  6. bio (str)
- Description: Contains detailed profiles for gym trainers.
- Example Rows:
  - 1|Sarah Johnson|Yoga & Flexibility|Certified Yoga Instructor, CPR|8|Expert in mind-body wellness and injury prevention
  - 2|Mike Thompson|Strength & Conditioning|NASM-CPT, CrossFit Level 2|10|Specializes in powerlifting and functional fitness
  - 3|Emma Davis|Pilates|Pilates Method Alliance Certified|6|Focus on core strength and postural alignment

### 4. Bookings Data
- File Path: data/bookings.txt
- Field Order & Names (pipe-delimited):
  1. booking_id (int)
  2. member_name (str)
  3. trainer_id (int)
  4. booking_date (str, yyyy-mm-dd)
  5. booking_time (str, hh:mm)
  6. duration_minutes (int)
  7. status (str)
- Description: Records all personal training session bookings.
- Example Rows:
  - 1|John Doe|1|2025-01-20|10:00|60|Confirmed
  - 2|Jane Smith|2|2025-01-21|14:00|45|Confirmed
  - 3|Alex Johnson|3|2025-01-22|16:00|60|Pending

### 5. Workouts Data
- File Path: data/workouts.txt
- Field Order & Names (pipe-delimited):
  1. workout_id (int)
  2. member_name (str)
  3. workout_type (str)
  4. workout_date (str, yyyy-mm-dd)
  5. duration_minutes (int)
  6. calories_burned (int)
  7. notes (str)
- Description: Stores user's workout history and progress notes.
- Example Rows:
  - 1|John Doe|Cardio|2025-01-15|45|350|Morning run on treadmill
  - 2|Jane Smith|Strength|2025-01-16|60|420|Upper body weight training with trainer
  - 3|Alex Johnson|Class|2025-01-17|50|380|CrossFit Bootcamp session

---

This completes the detailed design specification for the GymMembership web application, enabling fully parallel backend and frontend development.
