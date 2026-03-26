# Design Specification for GymMembership Web Application

---

## 1. Flask Routes Specification

### Root Route
- **Route Path:** `/`
- **Function Name:** `dashboard`
- **HTTP Method:** GET
- **Description:** Redirects to the Dashboard Page.
- **Redirects To:** `/dashboard`

### Dashboard Page
- **Route Path:** `/dashboard`
- **Function Name:** `dashboard`
- **HTTP Method:** GET
- **Template:** `dashboard.html`
- **Context Variables:**
  - `member_status` (str): Welcome or status information for the member
  - `membership_plans` (list of dict): List of membership plan summaries
  - `featured_classes` (list of dict): List of featured fitness classes
  - `trainers` (list of dict): List of available trainers for quick access

### Membership Plans Page
- **Route Path:** `/memberships`
- **Function Name:** `membership_plans_page`
- **HTTP Method:** GET
- **Template:** `memberships.html`
- **Context Variables:**
  - `membership_plans` (list of dict): List of all membership plans
  - `filter_types` (list of str): List of membership types for filtering (e.g., Basic, Premium, Elite)

### Plan Details Page
- **Route Path:** `/plan/<int:plan_id>`
- **Function Name:** `plan_details_page`
- **HTTP Method:** GET
- **Template:** `plan_details.html`
- **Context Variables:**
  - `plan` (dict): Detailed info for the plan identified by `plan_id`
  - `reviews` (list of dict): Reviews related to the plan
- **Route Parameter:**
  - `plan_id` (int): Identifier for the membership plan

### Class Schedule Page
- **Route Path:** `/schedule`
- **Function Name:** `class_schedule_page`
- **HTTP Method:** GET
- **Template:** `schedule.html`
- **Context Variables:**
  - `classes` (list of dict): List of all classes
  - `class_types` (list of str): Filter options for class types
  - `search_query` (str): Optional search query string

### Trainer Profiles Page
- **Route Path:** `/trainers`
- **Function Name:** `trainers_page`
- **HTTP Method:** GET
- **Template:** `trainers.html`
- **Context Variables:**
  - `trainers` (list of dict): List of all trainers
  - `specialties` (list of str): List of specialties for filtering
  - `search_query` (str): Optional search query string

### Trainer Detail Page
- **Route Path:** `/trainer/<int:trainer_id>`
- **Function Name:** `trainer_detail_page`
- **HTTP Method:** GET
- **Template:** `trainer_detail.html`
- **Context Variables:**
  - `trainer` (dict): Detailed info for the trainer identified by `trainer_id`
  - `reviews` (list of dict): Reviews from clients about the trainer
- **Route Parameter:**
  - `trainer_id` (int): Identifier for the trainer

### PT Booking Page
- **Route Path:** `/booking`
- **Function Name:** `pt_booking_page`
- **HTTP Methods:** GET, POST
- **Template:** `booking.html` (GET); On POST may redirect to confirmation or success page
- **Context Variables (GET):**
  - `trainers` (list of dict): Available trainers for dropdown selection
  - `available_times` (list of str): Time slots for sessions
  - `session_durations` (list of int): Duration options (e.g., 30, 60, 90)

### Workout Records Page
- **Route Path:** `/workouts`
- **Function Name:** `workout_records_page`
- **HTTP Method:** GET
- **Template:** `workouts.html`
- **Context Variables:**
  - `workouts` (list of dict): User's workout history
  - `workout_types` (list of str): Filter options for workout types

### Log Workout Page
- **Route Path:** `/log-workout`
- **Function Name:** `log_workout_page`
- **HTTP Methods:** GET, POST
- **Template:** `log_workout.html` (GET); On POST may redirect or update workout list
- **Context Variables (GET):**
  - `workout_types` (list of str): Options for workout type dropdown

---

## 2. HTML Template Specifications

### 1. Dashboard Page
- **Template Filename:** `dashboard.html`
- **Page Title:** Gym Membership Dashboard
- **Element IDs:**
  - `dashboard-page` (Div): Root container
  - `member-welcome` (Div): Welcome message and member info
  - `browse-membership-button` (Button): Navigates to Membership Plans page (`url_for('membership_plans_page')`)
  - `view-schedule-button` (Button): Navigates to Class Schedule page (`url_for('class_schedule_page')`)
  - `book-trainer-button` (Button): Navigates to PT Booking page (`url_for('pt_booking_page')`)
- **Context Variables and Access:**
  - `member_status`: String showing welcome or current membership status
  - `membership_plans`: Loop to display brief info about plans
  - `featured_classes`: Loop for featured fitness classes info
  - `trainers`: Loop for some quick trainer info

### 2. Membership Plans Page
- **Template Filename:** `memberships.html`
- **Page Title:** Membership Plans
- **Element IDs:**
  - `membership-page` (Div): Root container
  - `plan-filter` (Dropdown): Filter membership plans by type
  - `plans-grid` (Div): Grid container for membership cards
  - `view-details-button-{plan_id}` (Button): Button in each plan card to view full details (`url_for('plan_details_page', plan_id=plan_id)`)
  - `back-to-dashboard` (Button): Navigates back to dashboard (`url_for('dashboard')`)
- **Context Variables and Access:**
  - `membership_plans`: Loop of membership plans with attributes
  - `filter_types`: List of membership types to populate `plan-filter` dropdown

### 3. Plan Details Page
- **Template Filename:** `plan_details.html`
- **Page Title:** Plan Details
- **Element IDs:**
  - `plan-details-page` (Div): Root container
  - `plan-title` (H1): Membership plan name
  - `plan-price` (Div): Shows price and billing cycle
  - `plan-features` (Div): Lists included features
  - `enroll-plan-button` (Button): Button to enroll in the displayed plan
  - `plan-reviews` (Div): Section showing member reviews
- **Context Variables and Access:**
  - `plan`: Dict with plan details
  - `reviews`: List of review dicts

### 4. Class Schedule Page
- **Template Filename:** `schedule.html`
- **Page Title:** Class Schedule
- **Element IDs:**
  - `schedule-page` (Div): Root container
  - `schedule-search` (Input): Text input to search classes by name or trainer
  - `schedule-filter` (Dropdown): Filter by class type
  - `classes-grid` (Div): Grid container holding class cards
  - `enroll-class-button-{class_id}` (Button): Enroll button in each class card
- **Context Variables and Access:**
  - `classes`: List of class dicts with schedule and trainer details
  - `class_types`: List of class type strings
  - `search_query`: String used to filter/search classes

### 5. Trainer Profiles Page
- **Template Filename:** `trainers.html`
- **Page Title:** Trainer Profiles
- **Element IDs:**
  - `trainers-page` (Div): Root container
  - `trainer-search` (Input): Text input to search by name or specialty
  - `specialty-filter` (Dropdown): Filter trainers by specialty
  - `trainers-grid` (Div): Grid for trainer cards
  - `view-trainer-button-{trainer_id}` (Button): Button to trainer profile page
- **Context Variables and Access:**
  - `trainers`: List of trainers with profile info
  - `specialties`: List of specialties for filtering
  - `search_query`: Current search string

### 6. Trainer Detail Page
- **Template Filename:** `trainer_detail.html`
- **Page Title:** Trainer Profile
- **Element IDs:**
  - `trainer-detail-page` (Div): Root container
  - `trainer-name` (H1): Trainer full name
  - `trainer-bio` (Div): Biography and experience
  - `trainer-certifications` (Div): List of certifications
  - `book-session-button` (Button): Button to book a session with trainer
  - `trainer-reviews` (Div): Section showing client reviews
- **Context Variables and Access:**
  - `trainer`: Dictionary with trainer details
  - `reviews`: List of reviews

### 7. PT Booking Page
- **Template Filename:** `booking.html`
- **Page Title:** Book Personal Training
- **Element IDs:**
  - `booking-page` (Div): Root container
  - `select-trainer` (Dropdown): Trainer selector
  - `session-date` (Input, date): Date input
  - `session-time` (Dropdown): Time slot selection
  - `session-duration` (Dropdown): Duration options
  - `confirm-booking-button` (Button): Submit booking
- **Context Variables and Access:**
  - `trainers`: Trainers available
  - `available_times`: List of string time slots
  - `session_durations`: List of int durations

### 8. Workout Records Page
- **Template Filename:** `workouts.html`
- **Page Title:** My Workout Records
- **Element IDs:**
  - `workouts-page` (Div): Root container
  - `workouts-table` (Table): Table showing past workouts
  - `filter-by-type` (Dropdown): Filter workouts by type
  - `log-workout-button` (Button): Button to navigate to log workout page
  - `back-to-dashboard` (Button): Navigation back to dashboard
- **Context Variables and Access:**
  - `workouts`: List of workout history dicts
  - `workout_types`: Filter options

### 9. Log Workout Page
- **Template Filename:** `log_workout.html`
- **Page Title:** Log Workout
- **Element IDs:**
  - `log-workout-page` (Div): Root container
  - `workout-type` (Dropdown): Workout type selection
  - `workout-duration` (Input, number): Duration in minutes
  - `calories-burned` (Input, number): Calories burned estimate
  - `workout-notes` (Textarea): Notes input
  - `submit-workout-button` (Button): Submit button
- **Context Variables and Access:**
  - `workout_types`: List of workout type strings

---

## 3. Data File Schemas

### memberships.txt
- **File Path:** `data/memberships.txt`
- **Field Order:**
  - `membership_id` (int)
  - `plan_name` (str)
  - `price` (float)
  - `billing_cycle` (str) - (monthly)
  - `features` (str) - comma separated feature list
  - `max_classes` (int or str) - max number of classes allowed, 'unlimited' as string allowed
- **Description:** Stores membership plan information including pricing and features
- **Examples:**
  ```
  1|Basic|29.99|monthly|Gym access, 2 classes per week|8
  2|Premium|59.99|monthly|Gym access, 5 classes per week, 2 PT sessions|20
  3|Elite|99.99|monthly|Unlimited gym access, unlimited classes, 4 PT sessions, nutrition coaching|unlimited
  ```

### classes.txt
- **File Path:** `data/classes.txt`
- **Field Order:**
  - `class_id` (int)
  - `class_name` (str)
  - `trainer_id` (int)
  - `class_type` (str)
  - `schedule_day` (str)
  - `schedule_time` (HH:MM in 24hr)
  - `capacity` (int)
  - `duration` (int) in minutes
- **Description:** Stores scheduled classes with timing and trainer assignments
- **Examples:**
  ```
  1|Morning Yoga|1|Yoga|Monday|06:00|20|60
  2|CrossFit Bootcamp|2|CrossFit|Tuesday|18:00|15|45
  3|Pilates Core|3|Pilates|Wednesday|10:00|18|50
  ```

### trainers.txt
- **File Path:** `data/trainers.txt`
- **Field Order:**
  - `trainer_id` (int)
  - `name` (str)
  - `specialty` (str)
  - `certifications` (str, comma separated)
  - `experience_years` (int)
  - `bio` (str)
- **Description:** Information about personal trainers including expertise and biography
- **Examples:**
  ```
  1|Sarah Johnson|Yoga & Flexibility|Certified Yoga Instructor, CPR|8|Expert in mind-body wellness and injury prevention
  2|Mike Thompson|Strength & Conditioning|NASM-CPT, CrossFit Level 2|10|Specializes in powerlifting and functional fitness
  3|Emma Davis|Pilates|Pilates Method Alliance Certified|6|Focus on core strength and postural alignment
  ```

### bookings.txt
- **File Path:** `data/bookings.txt`
- **Field Order:**
  - `booking_id` (int)
  - `member_name` (str)
  - `trainer_id` (int)
  - `booking_date` (YYYY-MM-DD)
  - `booking_time` (HH:MM)
  - `duration_minutes` (int)
  - `status` (str) e.g., Confirmed, Pending
- **Description:** Records of personal training session bookings
- **Examples:**
  ```
  1|John Doe|1|2025-01-20|10:00|60|Confirmed
  2|Jane Smith|2|2025-01-21|14:00|45|Confirmed
  3|Alex Johnson|3|2025-01-22|16:00|60|Pending
  ```

### workouts.txt
- **File Path:** `data/workouts.txt`
- **Field Order:**
  - `workout_id` (int)
  - `member_name` (str)
  - `workout_type` (str)
  - `workout_date` (YYYY-MM-DD)
  - `duration_minutes` (int)
  - `calories_burned` (int)
  - `notes` (str)
- **Description:** User workout logs and history
- **Examples:**
  ```
  1|John Doe|Cardio|2025-01-15|45|350|Morning run on treadmill
  2|Jane Smith|Strength|2025-01-16|60|420|Upper body weight training with trainer
  3|Alex Johnson|Class|2025-01-17|50|380|CrossFit Bootcamp session
  ```

---

This specification empowers backend and frontend developers to independently implement all parts of the GymMembership application with consistent data contract and UI element definitions.