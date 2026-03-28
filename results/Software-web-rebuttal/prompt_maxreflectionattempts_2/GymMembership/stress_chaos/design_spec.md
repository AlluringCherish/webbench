# GymMembership Web Application Design Specification

---

## Section 1: Flask Routes Specification

| Route Path             | Function Name           | HTTP Method(s) | Template Filename     | Context Variables (name: type)                                       | Description                                     |
|------------------------|-------------------------|----------------|-----------------------|---------------------------------------------------------------------|-------------------------------------------------|
| `/`                    | root_redirect            | GET            | Redirect (no template) | None                                                                | Redirects to dashboard page                      |
| `/dashboard`           | dashboard               | GET            | dashboard.html        | member_status: str, featured_classes: list of dict, quick_nav_links: dict | Main hub with member highlights, featured classes, navigation buttons |
| `/memberships`         | memberships             | GET            | memberships.html      | plans: list of dict                                               | Shows all membership plans                       |
| `/plan/<int:plan_id>`  | plan_details            | GET            | plan_details.html     | plan: dict, reviews: list of dict                                 | Detailed info about selected membership plan    |
| `/schedule`            | class_schedule          | GET            | class_schedule.html   | classes: list of dict, class_types: list of str, search_query: str (optional), filter_type: str (optional) | Displays fitness classes schedule                |
| `/trainers`            | trainer_profiles        | GET            | trainer_profiles.html | trainers: list of dict, specialties: list of str, search_query: str (optional), filter_specialty: str (optional) | Displays trainers with expertise and filter     |
| `/trainer/<int:trainer_id>` | trainer_detail      | GET            | trainer_detail.html   | trainer: dict, reviews: list of dict                             | Detailed trainer profile                         |
| `/booking`             | pt_booking              | GET, POST     | booking.html          | trainers: list of dict (GET); booking_result: str (POST)          | Book personal training sessions                  |
| `/workouts`            | workout_records         | GET            | workout_records.html  | workouts: list of dict, workout_types: list of str, filter_type: str (optional) | User's workout history and filters                |
| `/log_workout`         | log_workout             | GET, POST     | log_workout.html      | log_result: str (POST)                                            | Log new workout record                            |

---

### Detailed Explanation of Routes:

- `/` :
  - Redirects (HTTP 302) to the Dashboard page `/dashboard`.

- `/dashboard` (dashboard):
  - Method: GET
  - Template: `dashboard.html`
  - Context variables:
    - `member_status` (str): Status message or name to display in welcome section.
    - `featured_classes` (list of dict): Each dict includes keys like `class_name` (str), `schedule_time` (str), `trainer_name` (str).
    - `quick_nav_links` (dict): Dict of action names to route path strings to use in navigation buttons.

- `/memberships` (memberships):
  - Method: GET
  - Template: `memberships.html`
  - Context variables:
    - `plans` (list of dict): Each dict includes `membership_id` (int), `plan_name` (str), `price` (float), `billing_cycle` (str), `features` (str), `max_classes` (str or int).

- `/plan/<int:plan_id>` (plan_details):
  - Method: GET
  - Template: `plan_details.html`
  - Context variables:
    - `plan` (dict): Detailed membership plan data matching a single membership.
    - `reviews` (list of dict): Reviews related to the plan if any (empty list if none).

- `/schedule` (class_schedule):
  - Method: GET
  - Template: `class_schedule.html`
  - Context variables:
    - `classes` (list of dict): List of class info dicts with keys like `class_id` (int), `class_name` (str), `trainer_id` (int), `class_type` (str), `schedule_day` (str), `schedule_time` (str), `capacity` (int), `duration` (int).
    - `class_types` (list of str): List of all class types for filtering.
    - `search_query` (str, optional): Query string for searching classes.
    - `filter_type` (str, optional): Selected class filter type.

- `/trainers` (trainer_profiles):
  - Method: GET
  - Template: `trainer_profiles.html`
  - Context variables:
    - `trainers` (list of dict): List of trainers with keys `trainer_id` (int), `name` (str), `specialty` (str), `certifications` (str), `experience_years` (int), `bio` (str).
    - `specialties` (list of str): List for specialty filter dropdown.
    - `search_query` (str, optional): Search term for trainers.
    - `filter_specialty` (str, optional): Selected specialty filter.

- `/trainer/<int:trainer_id>` (trainer_detail):
  - Method: GET
  - Template: `trainer_detail.html`
  - Context variables:
    - `trainer` (dict): Selected trainer's detailed info.
    - `reviews` (list of dict): Reviews about this trainer.

- `/booking` (pt_booking):
  - Methods: GET, POST
  - Template: `booking.html`
  - Context variables:
    - GET: `trainers` (list of dict) for dropdown selection.
    - POST: `booking_result` (str) success or error message.

- `/workouts` (workout_records):
  - Method: GET
  - Template: `workout_records.html`
  - Context variables:
    - `workouts` (list of dict): User workout records.
    - `workout_types` (list of str): Workout type filters.
    - `filter_type` (str, optional): Selected filter.

- `/log_workout` (log_workout):
  - Methods: GET, POST
  - Template: `log_workout.html`
  - Context variables:
    - POST: `log_result` (str) message about submission success or failure.

---

## Section 2: HTML Template Specifications

### 1. dashboard.html
- Page Title: Gym Membership Dashboard
- Elements:
  - `dashboard-page` (Div): Container for dashboard page
  - `member-welcome` (Div): Welcome section with member status
  - `browse-membership-button` (Button): Link to memberships page (`url_for('memberships')`)
  - `view-schedule-button` (Button): Link to schedule page (`url_for('class_schedule')`)
  - `book-trainer-button` (Button): Link to booking page (`url_for('pt_booking')`)
- Context:
  - `member_status` (str): Display in `member-welcome`
  - `featured_classes` (list of dict): Loop to show featured classes
  - Navigation buttons use provided IDs and Flask `url_for` functions.

### 2. memberships.html
- Page Title: Membership Plans
- Elements:
  - `membership-page` (Div): Container
  - `plan-filter` (Dropdown): Filter plans by type [Basic, Premium, Elite]
  - `plans-grid` (Div): Container displaying membership cards
  - For each plan:
    - `view-details-button-{plan_id}` (Button): Link to `/plan/<plan_id>`
  - `back-to-dashboard` (Button): Link to dashboard page (`url_for('dashboard')`)
- Context:
  - `plans` (list of dict): Loop to generate plan cards

### 3. plan_details.html
- Page Title: Plan Details
- Elements:
  - `plan-details-page` (Div): Container
  - `plan-title` (H1): Show plan's `plan_name`
  - `plan-price` (Div): Show price and billing_cycle
  - `plan-features` (Div): Show features
  - `enroll-plan-button` (Button): Enroll action (no route specified)
  - `plan-reviews` (Div): Loop reviews if any
- Context:
  - `plan` (dict): Access fields like `plan_name`, `price`, `billing_cycle`, `features`
  - `reviews` (list of dict): Access review data for display

### 4. class_schedule.html
- Page Title: Class Schedule
- Elements:
  - `schedule-page` (Div): Container
  - `schedule-search` (Input text): Search classes by name or trainer
  - `schedule-filter` (Dropdown): Filter by class_type
  - `classes-grid` (Div): Display class cards
  - For each class:
    - `enroll-class-button-{class_id}` (Button): Enroll in class
- Context:
  - `classes` (list of dict): Loop to display each class
  - `class_types` (list of str): Populate filter dropdown
  - `search_query` (str), `filter_type` (str) optional for search/filter states

### 5. trainer_profiles.html
- Page Title: Trainer Profiles
- Elements:
  - `trainers-page` (Div): Container
  - `trainer-search` (Input text): Search trainers
  - `specialty-filter` (Dropdown): Filter trainers by specialty
  - `trainers-grid` (Div): Show trainer cards
  - For each trainer:
    - `view-trainer-button-{trainer_id}` (Button): Link to trainer detail
- Context:
  - `trainers` (list of dict): Loop for trainer display
  - `specialties` (list of str): Populate specialty filter
  - `search_query` (str), `filter_specialty` (str) optional

### 6. trainer_detail.html
- Page Title: Trainer Profile
- Elements:
  - `trainer-detail-page` (Div): Container
  - `trainer-name` (H1): Trainer's name
  - `trainer-bio` (Div): Bio and experience
  - `trainer-certifications` (Div): Certifications
  - `book-session-button` (Button): Book session
  - `trainer-reviews` (Div): Client reviews
- Context:
  - `trainer` (dict): Use keys like `name`, `bio`, `certifications`
  - `reviews` (list of dict): Display reviews

### 7. booking.html
- Page Title: Book Personal Training
- Elements:
  - `booking-page` (Div): Container
  - `select-trainer` (Dropdown): List of trainers
  - `session-date` (Input date): Select date
  - `session-time` (Dropdown): Select time slot
  - `session-duration` (Dropdown): Select 30, 60, 90 min
  - `confirm-booking-button` (Button): Confirm booking
- Context:
  - GET: `trainers` (list of dict) for dropdown
  - POST: `booking_result` (str) message

### 8. workout_records.html
- Page Title: My Workout Records
- Elements:
  - `workouts-page` (Div): Container
  - `workouts-table` (Table): Columns for date, type, duration, calories
  - `filter-by-type` (Dropdown): Filter workouts by type
  - `log-workout-button` (Button): Link to log workout page
  - `back-to-dashboard` (Button): Link to dashboard
- Context:
  - `workouts` (list of dict): Loop for table rows
  - `workout_types` (list of str): Populate filter
  - `filter_type` (str) optional

### 9. log_workout.html
- Page Title: Log Workout
- Elements:
  - `log-workout-page` (Div): Container
  - `workout-type` (Dropdown): Select workout type
  - `workout-duration` (Input number): Duration minutes
  - `calories-burned` (Input number): Calories burned
  - `workout-notes` (Textarea): Notes
  - `submit-workout-button` (Button): Submit workout
- Context:
  - POST: `log_result` (str) message

---

## Section 3: Data File Schemas

### 1. Memberships Data File
- File Path: `data/memberships.txt`
- Field Order (pipe-delimited):
  - membership_id (int)
  - plan_name (str)
  - price (float)
  - billing_cycle (str)
  - features (str)
  - max_classes (str or int)
- Description: Stores all membership plan details including features and limitations.
- Example Rows:
    ```
    1|Basic|29.99|monthly|Gym access, 2 classes per week|8
    2|Premium|59.99|monthly|Gym access, 5 classes per week, 2 PT sessions|20
    3|Elite|99.99|monthly|Unlimited gym access, unlimited classes, 4 PT sessions, nutrition coaching|unlimited
    ```

### 2. Classes Data File
- File Path: `data/classes.txt`
- Field Order (pipe-delimited):
  - class_id (int)
  - class_name (str)
  - trainer_id (int)
  - class_type (str)
  - schedule_day (str)
  - schedule_time (str, HH:MM 24hr format)
  - capacity (int)
  - duration (int, minutes)
- Description: Contains scheduled fitness classes information.
- Example Rows:
    ```
    1|Morning Yoga|1|Yoga|Monday|06:00|20|60
    2|CrossFit Bootcamp|2|CrossFit|Tuesday|18:00|15|45
    3|Pilates Core|3|Pilates|Wednesday|10:00|18|50
    ```

### 3. Trainers Data File
- File Path: `data/trainers.txt`
- Field Order (pipe-delimited):
  - trainer_id (int)
  - name (str)
  - specialty (str)
  - certifications (str)
  - experience_years (int)
  - bio (str)
- Description: Stores profile info for all trainers.
- Example Rows:
    ```
    1|Sarah Johnson|Yoga & Flexibility|Certified Yoga Instructor, CPR|8|Expert in mind-body wellness and injury prevention
    2|Mike Thompson|Strength & Conditioning|NASM-CPT, CrossFit Level 2|10|Specializes in powerlifting and functional fitness
    3|Emma Davis|Pilates|Pilates Method Alliance Certified|6|Focus on core strength and postural alignment
    ```

### 4. Bookings Data File
- File Path: `data/bookings.txt`
- Field Order (pipe-delimited):
  - booking_id (int)
  - member_name (str)
  - trainer_id (int)
  - booking_date (str, YYYY-MM-DD)
  - booking_time (str, HH:MM 24hr format)
  - duration_minutes (int)
  - status (str)
- Description: Records personal training session bookings.
- Example Rows:
    ```
    1|John Doe|1|2025-01-20|10:00|60|Confirmed
    2|Jane Smith|2|2025-01-21|14:00|45|Confirmed
    3|Alex Johnson|3|2025-01-22|16:00|60|Pending
    ```

### 5. Workouts Data File
- File Path: `data/workouts.txt`
- Field Order (pipe-delimited):
  - workout_id (int)
  - member_name (str)
  - workout_type (str)
  - workout_date (str, YYYY-MM-DD)
  - duration_minutes (int)
  - calories_burned (int)
  - notes (str)
- Description: Logs user's workout sessions and details.
- Example Rows:
    ```
    1|John Doe|Cardio|2025-01-15|45|350|Morning run on treadmill
    2|Jane Smith|Strength|2025-01-16|60|420|Upper body weight training with trainer
    3|Alex Johnson|Class|2025-01-17|50|380|CrossFit Bootcamp session
    ```

---

# End of Design Specification
