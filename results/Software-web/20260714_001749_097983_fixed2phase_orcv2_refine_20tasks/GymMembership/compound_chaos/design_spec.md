# GymMembership Web Application Design Specification

## Section 1: Page and UI Element Design

### 1. Dashboard Page
- Page Title: Gym Membership Dashboard
- Overview: Main hub showing member highlights, featured classes, and navigation buttons to other functionalities.
- Elements:
  - `dashboard-page` (Div): Container for the dashboard.
  - `member-welcome` (Div): Section showing the welcome message and member status.
  - `browse-membership-button` (Button): Navigates to Membership Plans page.
  - `view-schedule-button` (Button): Navigates to Class Schedule page.
  - `book-trainer-button` (Button): Navigates to PT Booking page.

### 2. Membership Plans Page
- Page Title: Membership Plans
- Overview: Displays membership plans available, filterable by type.
- Elements:
  - `membership-page` (Div): Container for the page.
  - `plan-filter` (Dropdown): Filter plans by type (Basic, Premium, Elite).
  - `plans-grid` (Div): Grid showing each membership plan card.
  - `view-details-button-{plan_id}` (Button): For each plan card, navigate to Plan Details page for that plan.
  - `back-to-dashboard` (Button): Navigates back to Dashboard.

### 3. Plan Details Page
- Page Title: Plan Details
- Overview: Shows detailed information of a specific membership plan.
- Elements:
  - `plan-details-page` (Div): Container.
  - `plan-title` (H1): Displays plan name.
  - `plan-price` (Div): Shows price and billing cycle.
  - `plan-features` (Div): Lists plan features.
  - `enroll-plan-button` (Button): Enrolls user in this plan.
  - `plan-reviews` (Div): Shows member reviews of the plan.

### 4. Class Schedule Page
- Page Title: Class Schedule
- Overview: Lists fitness classes with schedule and instructor info.
- Elements:
  - `schedule-page` (Div): Container.
  - `schedule-search` (Input): Search field for classes by name or trainer.
  - `schedule-filter` (Dropdown): Filter by class type (Yoga, CrossFit, Pilates, Boxing, etc.).
  - `classes-grid` (Div): Displays class cards.
  - `enroll-class-button-{class_id}` (Button): Enroll in a class.

### 5. Trainer Profiles Page
- Page Title: Trainer Profiles
- Overview: Lists all trainers with search and filter.
- Elements:
  - `trainers-page` (Div): Container.
  - `trainer-search` (Input): Search trainers by name or specialty.
  - `specialty-filter` (Dropdown): Filter by specialty (Strength, Cardio, Flexibility, Weight Loss).
  - `trainers-grid` (Div): Trainer cards with photo, name, expertise.
  - `view-trainer-button-{trainer_id}` (Button): View detailed trainer profile.

### 6. Trainer Detail Page
- Page Title: Trainer Profile
- Overview: Detailed info of a trainer.
- Elements:
  - `trainer-detail-page` (Div): Container.
  - `trainer-name` (H1): Trainer's full name.
  - `trainer-bio` (Div): Biography and experience.
  - `trainer-certifications` (Div): Certifications list.
  - `book-session-button` (Button): Book a session with this trainer.
  - `trainer-reviews` (Div): Client reviews section.

### 7. PT Booking Page
- Page Title: Book Personal Training
- Overview: Schedule a personal training session.
- Elements:
  - `booking-page` (Div): Container.
  - `select-trainer` (Dropdown): Select trainer.
  - `session-date` (Input date): Choose session date.
  - `session-time` (Dropdown): Choose session time slot.
  - `session-duration` (Dropdown): Duration options (30, 60, 90 minutes).
  - `confirm-booking-button` (Button): Confirm and save booking.

### 8. Workout Records Page
- Page Title: My Workout Records
- Overview: Displays user's workout history.
- Elements:
  - `workouts-page` (Div): Container.
  - `workouts-table` (Table): Date, workout type, duration, calories burned.
  - `filter-by-type` (Dropdown): Filter workouts by type (Class, PT Session, Personal).
  - `log-workout-button` (Button): Navigate to Log Workout page.
  - `back-to-dashboard` (Button): Navigate back to Dashboard.

### 9. Log Workout Page
- Page Title: Log Workout
- Overview: Record new workout details.
- Elements:
  - `log-workout-page` (Div): Container.
  - `workout-type` (Dropdown): Select type (Cardio, Strength, Flexibility, Sports).
  - `workout-duration` (Input number): Duration in minutes.
  - `calories-burned` (Input number): Estimated calories.
  - `workout-notes` (Textarea): Notes about workout.
  - `submit-workout-button` (Button): Submit workout record.

## Navigation Flow
- Dashboard's `browse-membership-button` -> Membership Plans Page
- Dashboard's `view-schedule-button` -> Class Schedule Page
- Dashboard's `book-trainer-button` -> PT Booking Page
- Membership Plans Page's `view-details-button-{plan_id}` -> Plan Details Page for the plan
- Membership Plans Page's `back-to-dashboard` -> Dashboard
- Plan Details Page's `enroll-plan-button` -> (Enroll logic, then return to Dashboard or Plans Page)
- Class Schedule Page's `enroll-class-button-{class_id}` -> (Enroll logic, stay or show confirmation)
- Trainer Profiles Page's `view-trainer-button-{trainer_id}` -> Trainer Detail Page
- Trainer Detail Page's `book-session-button` -> PT Booking Page
- PT Booking Page's `confirm-booking-button` -> (Save booking, then Dashboard or confirmation view)
- Workout Records Page's `log-workout-button` -> Log Workout Page
- Workout Records Page's `back-to-dashboard` -> Dashboard
- Log Workout Page's `submit-workout-button` -> (Save workout, then Workout Records Page)

## Section 2: Local Data Storage Format

All data files are stored in `data/` directory as UTF-8 encoded text files using pipe `|` delimiter.

### 1. Memberships Data
- File: `memberships.txt`
- Schema:
  membership_id|plan_name|price|billing_cycle|features|max_classes
- Example:
  1|Basic|29.99|monthly|Gym access, 2 classes per week|8
  2|Premium|59.99|monthly|Gym access, 5 classes per week, 2 PT sessions|20
  3|Elite|99.99|monthly|Unlimited gym access, unlimited classes, 4 PT sessions, nutrition coaching|unlimited

### 2. Classes Data
- File: `classes.txt`
- Schema:
  class_id|class_name|trainer_id|class_type|schedule_day|schedule_time|capacity|duration
- Example:
  1|Morning Yoga|1|Yoga|Monday|06:00|20|60
  2|CrossFit Bootcamp|2|CrossFit|Tuesday|18:00|15|45
  3|Pilates Core|3|Pilates|Wednesday|10:00|18|50

### 3. Trainers Data
- File: `trainers.txt`
- Schema:
  trainer_id|name|specialty|certifications|experience_years|bio
- Example:
  1|Sarah Johnson|Yoga & Flexibility|Certified Yoga Instructor, CPR|8|Expert in mind-body wellness and injury prevention
  2|Mike Thompson|Strength & Conditioning|NASM-CPT, CrossFit Level 2|10|Specializes in powerlifting and functional fitness
  3|Emma Davis|Pilates|Pilates Method Alliance Certified|6|Focus on core strength and postural alignment

### 4. Bookings Data
- File: `bookings.txt`
- Schema:
  booking_id|member_name|trainer_id|booking_date|booking_time|duration_minutes|status
- Example:
  1|John Doe|1|2025-01-20|10:00|60|Confirmed
  2|Jane Smith|2|2025-01-21|14:00|45|Confirmed
  3|Alex Johnson|3|2025-01-22|16:00|60|Pending

### 5. Workouts Data
- File: `workouts.txt`
- Schema:
  workout_id|member_name|workout_type|workout_date|duration_minutes|calories_burned|notes
- Example:
  1|John Doe|Cardio|2025-01-15|45|350|Morning run on treadmill
  2|Jane Smith|Strength|2025-01-16|60|420|Upper body weight training with trainer
  3|Alex Johnson|Class|2025-01-17|50|380|CrossFit Bootcamp session

## Section 3: Data and Navigation Consistency

- Element IDs are consistent across pages and match those used in navigation flow.
- Buttons with dynamic IDs (e.g., `view-details-button-{plan_id}`) uniquely identify target data based on available plan or class or trainer IDs.
- Navigation buttons on Dashboard and other pages link logically to target pages.
- Data storage schemas directly correspond to UI elements displaying or modifying the data, ensuring seamless read/write operations.

This design fully satisfies the GymMembership requirements, covering UI, navigation, and data storage in detail.