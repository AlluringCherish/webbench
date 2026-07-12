# GymMembership Application Design Specification

---

# Section 1: Flask Routes Specification

| Route Path                  | Function Name              | HTTP Methods | Template File        | Context Variables (Name : Type)                                         |
|-----------------------------|----------------------------|--------------|----------------------|------------------------------------------------------------------------|
| `/`                         | root_redirect              | GET          | N/A (redirect)       | None                                                                   |
| `/dashboard`                | dashboard                 | GET          | dashboard.html       | member_welcome_msg : str, featured_classes : list of dict, quick_links : dict[str:str] |
| `/memberships`              | memberships               | GET          | memberships.html     | membership_plans : list of dict with keys {membership_id:int, plan_name:str, price:float, billing_cycle:str, features:str, max_classes:str} |
| `/plan/<int:plan_id>`       | plan_details              | GET          | plan_details.html    | plan : dict with keys {membership_id:int, plan_name:str, price:float, billing_cycle:str, features:str, max_classes:str},
                                                                                                  plan_reviews : list of dict[str:str]                  |
| `/classes`                  | class_schedule            | GET          | class_schedule.html  | classes : list of dict with keys {class_id:int, class_name:str, trainer_id:int, class_type:str, schedule_day:str, schedule_time:str, capacity:int, duration:int} |
| `/trainers`                 | trainers                  | GET          | trainers.html        | trainers_list : list of dict with keys {trainer_id:int, name:str, specialty:str, certifications:str, experience_years:int, bio:str} |
| `/trainer/<int:trainer_id>` | trainer_detail            | GET          | trainer_detail.html  | trainer : dict with keys {trainer_id:int, name:str, specialty:str, certifications:str, experience_years:int, bio:str},
                                                                                                  trainer_reviews : list of dict[str:str]                  |
| `/booking`                  | pt_booking                | GET, POST   | pt_booking.html      | (GET) trainers : list of dict with keys {trainer_id:int, name:str},
                                                                             (POST) booking_confirmation : str or dict |
| `/workouts`                 | workout_records           | GET          | workout_records.html | workouts : list of dict with keys {workout_id:int, member_name:str, workout_type:str, workout_date:str, duration_minutes:int, calories_burned:int, notes:str} |
| `/log_workout`              | log_workout               | GET, POST    | log_workout.html     | (GET) None,
                                                                           (POST) log_confirmation : str or dict  |


## Details

- **Root Route (`/`):** Redirects to `/dashboard`.

- **Dashboard (`/dashboard`)**
  - Renders `dashboard.html`.
  - Context Variables:
    - `member_welcome_msg` (str): Welcome message for the member.
    - `featured_classes` (list of dict): Each dict includes keys such as `class_name` (str), `schedule_day` (str), `schedule_time` (str), `trainer_name` (str).
    - `quick_links` (dict[str:str]): A map from button ids to route endpoint names or URLs.

- **Membership Plans (`/memberships`):**
  - Renders `memberships.html`.
  - Context:
    - `membership_plans` (list of dict) where each dict corresponds to membership plan data, keys:
      - `membership_id` (int)
      - `plan_name` (str)
      - `price` (float)
      - `billing_cycle` (str)
      - `features` (str)
      - `max_classes` (str, e.g. "8" or "unlimited")

- **Plan Details (`/plan/<int:plan_id>`):**
  - Renders `plan_details.html`.
  - Context:
    - `plan` (dict) - Membership plan data for given `plan_id`.
    - `plan_reviews` (list of dict[str:str]) list of review entries (e.g., reviewer name, comment).

- **Class Schedule (`/classes`):**
  - Renders `class_schedule.html`.
  - Context:
    - `classes` (list of dict) with class data including:
      - `class_id` (int)
      - `class_name` (str)
      - `trainer_id` (int)
      - `class_type` (str)
      - `schedule_day` (str)
      - `schedule_time` (str)
      - `capacity` (int)
      - `duration` (int)

- **Trainer Profiles (`/trainers`):**
  - Renders `trainers.html`.
  - Context:
    - `trainers_list` (list of dict) with trainer details:
      - `trainer_id` (int)
      - `name` (str)
      - `specialty` (str)
      - `certifications` (str)
      - `experience_years` (int)
      - `bio` (str)

- **Trainer Detail (`/trainer/<int:trainer_id>`):**
  - Renders `trainer_detail.html`.
  - Context:
    - `trainer` (dict) - Trainer details for given ID.
    - `trainer_reviews` (list of dict[str:str]) - Reviews from clients.

- **PT Booking (`/booking`):**
  - GET: Show booking form. POST: Submit booking.
  - Renders `pt_booking.html`.
  - Context:
    - GET: `trainers` (list of dict) each with `trainer_id` and `name`.
    - POST: Confirmation message or error.

- **Workout Records (`/workouts`):**
  - Renders `workout_records.html`.
  - Context:
    - `workouts` (list of dict) each with:
      - `workout_id` (int)
      - `member_name` (str)
      - `workout_type` (str)
      - `workout_date` (str)
      - `duration_minutes` (int)
      - `calories_burned` (int)
      - `notes` (str)

- **Log Workout (`/log_workout`):**
  - GET: Show form, POST: Submit workout log.
  - Renders `log_workout.html`.
  - Context:
    - GET: None
    - POST: Confirmation or error message.

---

# Section 2: HTML Template Specifications

## 1. dashboard.html
- **Page Title**: Gym Membership Dashboard
- **Element IDs and Types:**
  - `dashboard-page` (Div): Container for dashboard page.
  - `member-welcome` (Div): Section showing member welcome/status.
  - `browse-membership-button` (Button): Navigates to memberships page.
  - `view-schedule-button` (Button): Navigates to class schedule page.
  - `book-trainer-button` (Button): Navigates to PT booking page.
- **Context Variables:**
  - `member_welcome_msg` (str): Displayed inside `member-welcome` div.
  - `featured_classes` (list of dict): Loop to display featured classes in summary (optional divs inside dashboard).
  - `quick_links` (dict): Used to link buttons with Flask `url_for` routes.
- **Navigation Elements:**
  - Buttons with ids `browse-membership-button`, `view-schedule-button`, and `book-trainer-button` linked to `memberships`, `class_schedule`, and `pt_booking` routes respectively.

## 2. memberships.html
- Title: Membership Plans
- IDs:
  - `membership-page` (Div): Container for membership plans.
  - `plan-filter` (Dropdown): Filters plans by membership type.
  - `plans-grid` (Div): Grid layout containing plan cards.
  - `view-details-button-{plan_id}` (Button): Details button for each plan card.
  - `back-to-dashboard` (Button): Returns to dashboard.
- Context:
  - `membership_plans`: Loop over each plan to display name, price, features.
- Navigation:
  - `view-details-button-{plan_id}` buttons link to `plan_details` route with plan_id.
  - `back-to-dashboard` button links to `dashboard` route.

## 3. plan_details.html
- Title: Plan Details
- IDs:
  - `plan-details-page` (Div): Container page.
  - `plan-title` (H1): Shows plan name.
  - `plan-price` (Div): Shows plan price and billing cycle.
  - `plan-features` (Div): Details features.
  - `enroll-plan-button` (Button): Enroll in plan.
  - `plan-reviews` (Div): Section for member reviews.
- Context:
  - `plan`: Access fields like plan_name, price, billing_cycle, features.
  - `plan_reviews`: Loop reviews.
- Navigation:
  - `enroll-plan-button`: Could trigger enrollment action (no extra route).

## 4. class_schedule.html
- Title: Class Schedule
- IDs:
  - `schedule-page` (Div): Container for schedule.
  - `schedule-search` (Input text): Search classes.
  - `schedule-filter` (Dropdown): Filter by class type.
  - `classes-grid` (Div): Grid of class cards.
  - `enroll-class-button-{class_id}` (Button): Enroll button per class card.
- Context:
  - `classes`: Loop classes.
- Navigation:
  - `enroll-class-button-{class_id}` buttons link to enrollment process (No route specified, possibly POST handled in backend).

## 5. trainers.html
- Title: Trainer Profiles
- IDs:
  - `trainers-page` (Div)
  - `trainer-search` (Input text)
  - `specialty-filter` (Dropdown)
  - `trainers-grid` (Div)
  - `view-trainer-button-{trainer_id}` (Button)
- Context:
  - `trainers_list`: Loop over trainers.
- Navigation:
  - `view-trainer-button-{trainer_id}` buttons link to `trainer_detail` route with trainer_id.

## 6. trainer_detail.html
- Title: Trainer Profile
- IDs:
  - `trainer-detail-page` (Div)
  - `trainer-name` (H1)
  - `trainer-bio` (Div)
  - `trainer-certifications` (Div)
  - `book-session-button` (Button)
  - `trainer-reviews` (Div)
- Context:
  - `trainer`: Access trainer's details.
  - `trainer_reviews`: Loop to show reviews.
- Navigation:
  - `book-session-button` links to `pt_booking` route, with context of selected trainer.

## 7. pt_booking.html
- Title: Book Personal Training
- IDs:
  - `booking-page` (Div)
  - `select-trainer` (Dropdown)
  - `session-date` (Input date)
  - `session-time` (Dropdown)
  - `session-duration` (Dropdown)
  - `confirm-booking-button` (Button)
- Context:
  - `trainers`: List of trainers for dropdown.
- Navigation:
  - Form submits POST to `/booking` route.

## 8. workout_records.html
- Title: My Workout Records
- IDs:
  - `workouts-page` (Div)
  - `workouts-table` (Table)
  - `filter-by-type` (Dropdown)
  - `log-workout-button` (Button)
  - `back-to-dashboard` (Button)
- Context:
  - `workouts`: Loop over workout records for table rows.
- Navigation:
  - `log-workout-button` links to `/log_workout` route.
  - `back-to-dashboard` links back to `/dashboard`.

## 9. log_workout.html
- Title: Log Workout
- IDs:
  - `log-workout-page` (Div)
  - `workout-type` (Dropdown)
  - `workout-duration` (Input number)
  - `calories-burned` (Input number)
  - `workout-notes` (Textarea)
  - `submit-workout-button` (Button)
- Context:
  - No context needed for GET.
- Navigation:
  - Form submits POST to `/log_workout`.

---

# Section 3: Data File Schemas

## 1. Memberships Data
- File Path: data/memberships.txt
- Fields (pipe | delimited):
  1. `membership_id` (int)
  2. `plan_name` (str)
  3. `price` (float)
  4. `billing_cycle` (str)
  5. `features` (str)
  6. `max_classes` (str) - Sometimes "unlimited"
- Description: Contains all membership plans' details, pricing, features, and max classes allowed.
- Example Rows:
  ```
  1|Basic|29.99|monthly|Gym access, 2 classes per week|8
  2|Premium|59.99|monthly|Gym access, 5 classes per week, 2 PT sessions|20
  3|Elite|99.99|monthly|Unlimited gym access, unlimited classes, 4 PT sessions, nutrition coaching|unlimited
  ```

## 2. Classes Data
- File Path: data/classes.txt
- Fields (pipe | delimited):
  1. `class_id` (int)
  2. `class_name` (str)
  3. `trainer_id` (int)
  4. `class_type` (str)
  5. `schedule_day` (str)
  6. `schedule_time` (str, HH:MM format)
  7. `capacity` (int)
  8. `duration` (int, minutes)
- Description: Details all fitness classes including schedule and trainer.
- Examples:
  ```
  1|Morning Yoga|1|Yoga|Monday|06:00|20|60
  2|CrossFit Bootcamp|2|CrossFit|Tuesday|18:00|15|45
  3|Pilates Core|3|Pilates|Wednesday|10:00|18|50
  ```

## 3. Trainers Data
- File Path: data/trainers.txt
- Fields (pipe | delimited):
  1. `trainer_id` (int)
  2. `name` (str)
  3. `specialty` (str)
  4. `certifications` (str)
  5. `experience_years` (int)
  6. `bio` (str)
- Description: Contains all trainers' profiles including specialties and bios.
- Examples:
  ```
  1|Sarah Johnson|Yoga & Flexibility|Certified Yoga Instructor, CPR|8|Expert in mind-body wellness and injury prevention
  2|Mike Thompson|Strength & Conditioning|NASM-CPT, CrossFit Level 2|10|Specializes in powerlifting and functional fitness
  3|Emma Davis|Pilates|Pilates Method Alliance Certified|6|Focus on core strength and postural alignment
  ```

## 4. Bookings Data
- File Path: data/bookings.txt
- Fields (pipe | delimited):
  1. `booking_id` (int)
  2. `member_name` (str)
  3. `trainer_id` (int)
  4. `booking_date` (str, YYYY-MM-DD)
  5. `booking_time` (str, HH:MM)
  6. `duration_minutes` (int)
  7. `status` (str)
- Description: Stores bookings for personal training sessions.
- Examples:
  ```
  1|John Doe|1|2025-01-20|10:00|60|Confirmed
  2|Jane Smith|2|2025-01-21|14:00|45|Confirmed
  3|Alex Johnson|3|2025-01-22|16:00|60|Pending
  ```

## 5. Workouts Data
- File Path: data/workouts.txt
- Fields (pipe | delimited):
  1. `workout_id` (int)
  2. `member_name` (str)
  3. `workout_type` (str)
  4. `workout_date` (str, YYYY-MM-DD)
  5. `duration_minutes` (int)
  6. `calories_burned` (int)
  7. `notes` (str)
- Description: Records workout sessions and progress.
- Examples:
  ```
  1|John Doe|Cardio|2025-01-15|45|350|Morning run on treadmill
  2|Jane Smith|Strength|2025-01-16|60|420|Upper body weight training with trainer
  3|Alex Johnson|Class|2025-01-17|50|380|CrossFit Bootcamp session
  ```

---

# Notes
- All context variable names, route function names, template filenames, and element IDs are case sensitive and must match exactly.
- Navigation buttons must use Flask `url_for` with the function names specified.
- Dynamic IDs follow pattern: `view-details-button-{plan_id}`, `enroll-class-button-{class_id}`, etc., and should be rendered in Jinja2 loops as `view-details-button-{{ plan.membership_id }}`.
- Form POST routes are `/booking` and `/log_workout`.
- No user authentication or authorization flows are included.

---