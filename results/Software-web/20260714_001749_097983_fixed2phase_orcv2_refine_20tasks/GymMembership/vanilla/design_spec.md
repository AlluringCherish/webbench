# GymMembership Web Application Design Specification

## Section 1: Page and UI Element Design

### 1. Dashboard Page
- **Page Title**: Gym Membership Dashboard
- **Overview**: Main hub with member highlights, featured classes, and quick links.
- **Elements**:
  - `dashboard-page` (Div): Container for the dashboard content.
  - `member-welcome` (Div): Welcome message and member status.
  - `browse-membership-button` (Button): Navigate to Membership Plans page.
  - `view-schedule-button` (Button): Navigate to Class Schedule page.
  - `book-trainer-button` (Button): Navigate to Personal Training Booking page.

### 2. Membership Plans Page
- **Page Title**: Membership Plans
- **Overview**: Display all membership plans with filtering and details.
- **Elements**:
  - `membership-page` (Div): Container for the membership plans.
  - `plan-filter` (Dropdown): Filter plans by type (Basic, Premium, Elite).
  - `plans-grid` (Div): Grid of membership plan cards.
  - `view-details-button-{plan_id}` (Button): View details of a specific plan.
  - `back-to-dashboard` (Button): Return to Dashboard.

### 3. Plan Details Page
- **Page Title**: Plan Details
- **Overview**: Detailed information about a selected membership plan.
- **Elements**:
  - `plan-details-page` (Div): Container for plan details.
  - `plan-title` (H1): Name of the plan.
  - `plan-price` (Div): Price and billing cycle display.
  - `plan-features` (Div): Features listing.
  - `enroll-plan-button` (Button): Enroll in this plan.
  - `plan-reviews` (Div): Member reviews section.

### 4. Class Schedule Page
- **Page Title**: Class Schedule
- **Overview**: List of fitness classes with search and filters.
- **Elements**:
  - `schedule-page` (Div): Container for schedule content.
  - `schedule-search` (Input): Search field for classes by name or trainer.
  - `schedule-filter` (Dropdown): Filter by class types (Yoga, CrossFit, Pilates, Boxing, etc.).
  - `classes-grid` (Div): Grid of class cards.
  - `enroll-class-button-{class_id}` (Button): Enroll in a class.

### 5. Trainer Profiles Page
- **Page Title**: Trainer Profiles
- **Overview**: Display trainers with expertise and specialties.
- **Elements**:
  - `trainers-page` (Div): Container for trainer profiles.
  - `trainer-search` (Input): Search trainers by name or specialty.
  - `specialty-filter` (Dropdown): Filter trainers by specialty (Strength, Cardio, Flexibility, Weight Loss).
  - `trainers-grid` (Div): Grid displaying trainer cards.
  - `view-trainer-button-{trainer_id}` (Button): View individual trainer profile.

### 6. Trainer Detail Page
- **Page Title**: Trainer Profile
- **Overview**: Detailed page for a specific trainer.
- **Elements**:
  - `trainer-detail-page` (Div): Container for trainer details.
  - `trainer-name` (H1): Trainer's full name.
  - `trainer-bio` (Div): Biography and experience.
  - `trainer-certifications` (Div): Certifications display.
  - `book-session-button` (Button): Book personal training session.
  - `trainer-reviews` (Div): Client reviews.

### 7. PT Booking Page
- **Page Title**: Book Personal Training
- **Overview**: Schedule personal training sessions.
- **Elements**:
  - `booking-page` (Div): Container for booking interface.
  - `select-trainer` (Dropdown): Choose trainer.
  - `session-date` (Input - date): Select session date.
  - `session-time` (Dropdown): Select time slot.
  - `session-duration` (Dropdown): Select duration (30, 60, 90 minutes).
  - `confirm-booking-button` (Button): Confirm booking submission.

### 8. Workout Records Page
- **Page Title**: My Workout Records
- **Overview**: Show user's workout history and tracking.
- **Elements**:
  - `workouts-page` (Div): Container for workouts.
  - `workouts-table` (Table): Workout history showing date, type, duration, calories.
  - `filter-by-type` (Dropdown): Filter workouts by type (Class, PT Session, Personal).
  - `log-workout-button` (Button): Navigate to log workout page.
  - `back-to-dashboard` (Button): Return to Dashboard.

### 9. Log Workout Page
- **Page Title**: Log Workout
- **Overview**: Input form to record workout details.
- **Elements**:
  - `log-workout-page` (Div): Container for logging workout.
  - `workout-type` (Dropdown): Select workout category (Cardio, Strength, Flexibility, Sports).
  - `workout-duration` (Input - number): Duration in minutes.
  - `calories-burned` (Input - number): Calories burned estimation.
  - `workout-notes` (Textarea): Notes about workout session.
  - `submit-workout-button` (Button): Submit workout record.

## Navigation Flow
- Dashboard buttons navigate to Membership Plans (`browse-membership-button`), Class Schedule (`view-schedule-button`), PT Booking (`book-trainer-button`).
- Membership Plans page can navigate to Plan Details with `view-details-button-{plan_id}` and back to Dashboard via `back-to-dashboard`.
- Plan Details page can enroll in plan or navigate back (navigation back assumed).
- Class Schedule page enroll buttons `enroll-class-button-{class_id}` trigger enrollment.
- Trainer Profiles page view buttons `view-trainer-button-{trainer_id}` navigate to Trainer Detail page.
- Trainer Detail page has `book-session-button` to navigate to PT Booking.
- PT Booking page confirms bookings.
- Workout Records page navigation includes `log-workout-button` to Log Workout Page and `back-to-dashboard`.
- Log Workout page submits workout and navigates back to Workout Records.

## Section 2: Local Data Storage Format

Stored in `data` directory with these files and formats:

### 1. Memberships (`memberships.txt`)
- Format: `membership_id|plan_name|price|billing_cycle|features|max_classes`
- Example:
  `1|Basic|29.99|monthly|Gym access, 2 classes per week|8`
  `2|Premium|59.99|monthly|Gym access, 5 classes per week, 2 PT sessions|20`
  `3|Elite|99.99|monthly|Unlimited gym access, unlimited classes, 4 PT sessions, nutrition coaching|unlimited`

### 2. Classes (`classes.txt`)
- Format: `class_id|class_name|trainer_id|class_type|schedule_day|schedule_time|capacity|duration`
- Example:
  `1|Morning Yoga|1|Yoga|Monday|06:00|20|60`
  `2|CrossFit Bootcamp|2|CrossFit|Tuesday|18:00|15|45`
  `3|Pilates Core|3|Pilates|Wednesday|10:00|18|50`

### 3. Trainers (`trainers.txt`)
- Format: `trainer_id|name|specialty|certifications|experience_years|bio`
- Example:
  `1|Sarah Johnson|Yoga & Flexibility|Certified Yoga Instructor, CPR|8|Expert in mind-body wellness and injury prevention`
  `2|Mike Thompson|Strength & Conditioning|NASM-CPT, CrossFit Level 2|10|Specializes in powerlifting and functional fitness`
  `3|Emma Davis|Pilates|Pilates Method Alliance Certified|6|Focus on core strength and postural alignment`

### 4. Bookings (`bookings.txt`)
- Format: `booking_id|member_name|trainer_id|booking_date|booking_time|duration_minutes|status`
- Example:
  `1|John Doe|1|2025-01-20|10:00|60|Confirmed`
  `2|Jane Smith|2|2025-01-21|14:00|45|Confirmed`
  `3|Alex Johnson|3|2025-01-22|16:00|60|Pending`

### 5. Workouts (`workouts.txt`)
- Format: `workout_id|member_name|workout_type|workout_date|duration_minutes|calories_burned|notes`
- Example:
  `1|John Doe|Cardio|2025-01-15|45|350|Morning run on treadmill`
  `2|Jane Smith|Strength|2025-01-16|60|420|Upper body weight training with trainer`
  `3|Alex Johnson|Class|2025-01-17|50|380|CrossFit Bootcamp session`

## Section 3: Data and Navigation Consistency

- All element IDs correspond exactly to the specified page elements.
- Navigation buttons connect pages as defined in the navigation flow above.
- Data files formats match the fields displayed or modified in the UI pages.
- For dynamic elements with IDs using {plan_id}, {class_id}, {trainer_id}, the IDs consistently correspond to those used in the data files.

This completes the comprehensive design specification document for the GymMembership web application.