# GymMembership Flask Application Design Specification

---

## 1. Flask Routes

| URL Path                    | Handler Function Name       | HTTP Methods | Template File            | Context Variables (name: type)                                                                                     |
|-----------------------------|-----------------------------|--------------|--------------------------|------------------------------------------------------------------------------------------------------------------|
| /                           | root_redirect               | GET          | None (redirect to /dashboard) | None                                                                                                              |
| /dashboard                  | dashboard                  | GET          | dashboard.html           | member_status: str                                                                                                 |
| /memberships                | membership_plans           | GET          | membership_plans.html    | memberships: List[Dict] (membership_id: str, plan_name: str, price: str, billing_cycle: str, features: str, max_classes: str), filter_type: Optional[str] |
| /membership/<plan_id>       | plan_details               | GET          | plan_details.html        | plan: Dict (membership_id: str, plan_name: str, price: str, billing_cycle: str, features: str, max_classes: str), reviews: List[Dict] (structure not defined)   |
| /classes                   | class_schedule             | GET          | class_schedule.html      | classes: List[Dict] (class_id: str, class_name: str, trainer_id: str, class_type: str, schedule_day: str, schedule_time: str, capacity: str, duration: str), class_filter: Optional[str], search_query: Optional[str] |
| /trainers                  | trainer_profiles           | GET          | trainer_profiles.html    | trainers: List[Dict] (trainer_id: str, name: str, specialty: str, certifications: str, experience_years: str, bio: str), specialty_filter: Optional[str], search_query: Optional[str] |
| /trainer/<trainer_id>       | trainer_detail             | GET          | trainer_detail.html      | trainer: Dict (trainer_id: str, name: str, specialty: str, certifications: str, experience_years: str, bio: str), reviews: List[Dict] (structure not defined)           |
| /booking                   | pt_booking                | GET, POST   | booking.html             | trainers: List[Dict] (trainer_id: str, name: str), booking_confirmation: Optional[str] (POST result)                 |
| /workouts                  | workout_records            | GET          | workouts.html            | workouts: List[Dict] (workout_id: str, member_name: str, workout_type: str, workout_date: str, duration_minutes: str, calories_burned: str, notes: str), workout_filter: Optional[str]   |
| /workouts/log              | log_workout                | GET, POST   | log_workout.html         | submission_status: Optional[str] (POST result)                                                                     |

---

## 2. HTML Templates

### 1. dashboard.html
- Title: Gym Membership Dashboard
- Element IDs:
  - dashboard-page (Div)
  - member-welcome (Div)
  - browse-membership-button (Button) - Navigates to `membership_plans` route
  - view-schedule-button (Button) - Navigates to `class_schedule` route
  - book-trainer-button (Button) - Navigates to `pt_booking` route

### 2. membership_plans.html
- Title: Membership Plans
- Element IDs:
  - membership-page (Div)
  - plan-filter (Dropdown)
  - plans-grid (Div) - Displays membership plan cards
  - view-details-button-{plan_id} (Button) - One per plan card, links to `plan_details` with plan_id
  - back-to-dashboard (Button) - Navigates to `dashboard` route

### 3. plan_details.html
- Title: Plan Details
- Element IDs:
  - plan-details-page (Div)
  - plan-title (H1) - Displays `plan['plan_name']`
  - plan-price (Div) - Displays `plan['price']` and `plan['billing_cycle']`
  - plan-features (Div) - Displays `plan['features']`
  - enroll-plan-button (Button)
  - plan-reviews (Div) - Shows reviews passed in context variable

### 4. class_schedule.html
- Title: Class Schedule
- Element IDs:
  - schedule-page (Div)
  - schedule-search (Input)
  - schedule-filter (Dropdown)
  - classes-grid (Div) - Displays class cards
  - enroll-class-button-{class_id} (Button) - One per class card

### 5. trainer_profiles.html
- Title: Trainer Profiles
- Element IDs:
  - trainers-page (Div)
  - trainer-search (Input)
  - specialty-filter (Dropdown)
  - trainers-grid (Div) - Displays trainer cards
  - view-trainer-button-{trainer_id} (Button) - One per trainer card

### 6. trainer_detail.html
- Title: Trainer Profile
- Element IDs:
  - trainer-detail-page (Div)
  - trainer-name (H1)
  - trainer-bio (Div)
  - trainer-certifications (Div)
  - book-session-button (Button)
  - trainer-reviews (Div)

### 7. booking.html
- Title: Book Personal Training
- Element IDs:
  - booking-page (Div)
  - select-trainer (Dropdown)
  - session-date (Input date)
  - session-time (Dropdown)
  - session-duration (Dropdown)
  - confirm-booking-button (Button)

### 8. workouts.html
- Title: My Workout Records
- Element IDs:
  - workouts-page (Div)
  - workouts-table (Table)
  - filter-by-type (Dropdown)
  - log-workout-button (Button)
  - back-to-dashboard (Button)

### 9. log_workout.html
- Title: Log Workout
- Element IDs:
  - log-workout-page (Div)
  - workout-type (Dropdown)
  - workout-duration (Input number)
  - calories-burned (Input number)
  - workout-notes (Textarea)
  - submit-workout-button (Button)

---

## 3. Navigation Mappings (Button ID -> Route Handler)

| Source Page           | Button ID                  | Destination Route Function |
|-----------------------|----------------------------|----------------------------|
| Dashboard             | browse-membership-button   | membership_plans           |
| Dashboard             | view-schedule-button       | class_schedule             |
| Dashboard             | book-trainer-button        | pt_booking                 |
| Membership Plans      | back-to-dashboard          | dashboard                  |
| Workout Records       | back-to-dashboard          | dashboard                  |

---

## 4. Data File Schemas and Handling

All data files are stored in `data/` directory and use pipe (`|`) as delimiter. All fields are strings when loaded.

### 4.1 memberships.txt
- Fields (pipe-delimited order):
  1. membership_id
  2. plan_name
  3. price
  4. billing_cycle
  5. features
  6. max_classes
- Usage:
  - Read all lines to load membership plans list.
  - Parse each line into dict matching fields order.
  - When writing, overwrite file replacing all lines with updated pipe delimited strings.
- Example:
  ```
  1|Basic|29.99|monthly|Gym access, 2 classes per week|8
  2|Premium|59.99|monthly|Gym access, 5 classes per week, 2 PT sessions|20
  3|Elite|99.99|monthly|Unlimited gym access, unlimited classes, 4 PT sessions, nutrition coaching|unlimited
  ```

### 4.2 classes.txt
- Fields (pipe-delimited order):
  1. class_id
  2. class_name
  3. trainer_id
  4. class_type
  5. schedule_day
  6. schedule_time
  7. capacity
  8. duration
- Usage:
  - Read all lines to load classes list.
  - Parse to dict list per field order.
  - Write back by overwriting file line-by-line.
- Example:
  ```
  1|Morning Yoga|1|Yoga|Monday|06:00|20|60
  2|CrossFit Bootcamp|2|CrossFit|Tuesday|18:00|15|45
  3|Pilates Core|3|Pilates|Wednesday|10:00|18|50
  ```

### 4.3 trainers.txt
- Fields (pipe-delimited order):
  1. trainer_id
  2. name
  3. specialty
  4. certifications
  5. experience_years
  6. bio
- Usage:
  - Read all lines into trainers list.
  - Parse fields to dict.
  - Write back by overwrite all lines.
- Example:
  ```
  1|Sarah Johnson|Yoga & Flexibility|Certified Yoga Instructor, CPR|8|Expert in mind-body wellness and injury prevention
  2|Mike Thompson|Strength & Conditioning|NASM-CPT, CrossFit Level 2|10|Specializes in powerlifting and functional fitness
  3|Emma Davis|Pilates|Pilates Method Alliance Certified|6|Focus on core strength and postural alignment
  ```

### 4.4 bookings.txt
- Fields (pipe-delimited order):
  1. booking_id
  2. member_name
  3. trainer_id
  4. booking_date
  5. booking_time
  6. duration_minutes
  7. status
- Usage:
  - Read all lines to load bookings.
  - Parse to dict.
  - Write updates by overwrite.
- Example:
  ```
  1|John Doe|1|2025-01-20|10:00|60|Confirmed
  2|Jane Smith|2|2025-01-21|14:00|45|Confirmed
  3|Alex Johnson|3|2025-01-22|16:00|60|Pending
  ```

### 4.5 workouts.txt
- Fields (pipe-delimited order):
  1. workout_id
  2. member_name
  3. workout_type
  4. workout_date
  5. duration_minutes
  6. calories_burned
  7. notes
- Usage:
  - Read all lines to load workouts.
  - Parse to dict.
  - Write back by overwrite.
- Example:
  ```
  1|John Doe|Cardio|2025-01-15|45|350|Morning run on treadmill
  2|Jane Smith|Strength|2025-01-16|60|420|Upper body weight training with trainer
  3|Alex Johnson|Class|2025-01-17|50|380|CrossFit Bootcamp session
  ```

---

## 5. Context Variable Contracts

### 5.1 dashboard route
- member_status: `str` - Information about logged-in member's status (for display in member-welcome div).

### 5.2 membership_plans route
- memberships: `List[Dict]` with keys:
  - membership_id: str
  - plan_name: str
  - price: str
  - billing_cycle: str
  - features: str
  - max_classes: str
- filter_type: `Optional[str]` - Currently applied filter for plan types (Basic, Premium, Elite) or None

### 5.3 plan_details route
- plan: Dict with the membership plan fields matching membership record structure
- reviews: List of review objects for the plan (structure unspecified, pass as suitable list)

### 5.4 class_schedule route
- classes: List[Dict] with keys:
  - class_id: str
  - class_name: str
  - trainer_id: str
  - class_type: str
  - schedule_day: str
  - schedule_time: str
  - capacity: str
  - duration: str
- class_filter: Optional[str] - Current class type filter or None
- search_query: Optional[str] - Current search keywords or None

### 5.5 trainer_profiles route
- trainers: List[Dict] with keys:
  - trainer_id: str
  - name: str
  - specialty: str
  - certifications: str
  - experience_years: str
  - bio: str
- specialty_filter: Optional[str] - Current specialty filter or None
- search_query: Optional[str] - Search query string or None

### 5.6 trainer_detail route
- trainer: Dict with keys matching trainer record fields
- reviews: List of review objects (structure unspecified) for the trainer

### 5.7 pt_booking route
- trainers: List[Dict] with minimal keys:
  - trainer_id: str
  - name: str
- booking_confirmation: Optional[str] - Confirmation message or error after booking attempt

### 5.8 workout_records route
- workouts: List[Dict] with keys:
  - workout_id: str
  - member_name: str
  - workout_type: str
  - workout_date: str
  - duration_minutes: str
  - calories_burned: str
  - notes: str
- workout_filter: Optional[str] - Currently applied workout type filter or None

### 5.9 log_workout route
- submission_status: Optional[str] - Success or error message after workout log submission

---

This design specification document fully maps the requirements and formalizes routes, template files with elements, navigation buttons, data file schemas, and context variable interfaces to enable independent backend and frontend development for the GymMembership Flask app.