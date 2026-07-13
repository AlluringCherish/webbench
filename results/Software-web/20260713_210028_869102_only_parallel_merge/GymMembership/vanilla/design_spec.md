# GymMembership Web Application Design Specification

---

## 1. Flask Routes and Pages

| Route Path               | Function Name        | HTTP Methods | Template File          | Page Title                | Description                                           |
|--------------------------|---------------------|--------------|------------------------|---------------------------|-------------------------------------------------------|
| `/` or `/dashboard`      | dashboard           | GET          | dashboard.html         | Gym Membership Dashboard  | Main hub with member highlights and navigation buttons|
| `/memberships`           | membership_plans    | GET          | memberships.html       | Membership Plans           | Displays all membership plans with filter and details |
| `/memberships/<int:plan_id>` | plan_details         | GET          | plan_details.html      | Plan Details               | Detailed info on a specific membership plan           |
| `/schedule`              | class_schedule       | GET          | schedule.html          | Class Schedule             | Displays class schedules with search/filter and enroll |
| `/trainers`              | trainer_profiles     | GET          | trainers.html          | Trainer Profiles          | List of trainers with search/filter and profile views  |
| `/trainers/<int:trainer_id>` | trainer_detail       | GET          | trainer_detail.html    | Trainer Profile           | Detailed info on a specific trainer profile             |
| `/book-training`         | pt_booking           | GET, POST    | booking.html           | Book Personal Training    | Booking page for personal training sessions            |
| `/workouts`              | workout_records      | GET          | workouts.html          | My Workout Records        | Displays workout history and filter with log button    |
| `/log-workout`           | log_workout          | GET, POST    | log_workout.html       | Log Workout               | Page to log a new workout record                        |

---

## 2. UI Elements and IDs with Actions

### 2.1 Dashboard Page (`/dashboard`)
- Container Div: **ID: `dashboard-page`**
- Member welcome info Div: **ID: `member-welcome`**
- Buttons:
  - **ID: `browse-membership-button`**: Navigates to `/memberships`
  - **ID: `view-schedule-button`**: Navigates to `/schedule`
  - **ID: `book-trainer-button`**: Navigates to `/book-training`

### 2.2 Membership Plans Page (`/memberships`)
- Container Div: **ID: `membership-page`**
- Dropdown Filter: **ID: `plan-filter`** (filter by membership type: Basic, Premium, Elite)
- Plans Grid Div: **ID: `plans-grid`**
- Within each plan card:
  - Button: **ID: `view-details-button-{plan_id}`** navigates to `/memberships/<plan_id>`
- Button: **ID: `back-to-dashboard`** navigates back to `/dashboard`

### 2.3 Plan Details Page (`/memberships/<int:plan_id>`)
- Container Div: **ID: `plan-details-page`**
- Heading H1: **ID: `plan-title`**
- Price Div: **ID: `plan-price`** (includes price and billing cycle)
- Features Div: **ID: `plan-features`**
- Button: **ID: `enroll-plan-button`** (action: enroll in plan - to be simulated or logged)
- Reviews Div: **ID: `plan-reviews`** (displays member reviews, can be static)

### 2.4 Class Schedule Page (`/schedule`)
- Container Div: **ID: `schedule-page`**
- Search Input: **ID: `schedule-search`** (search by class name or trainer)
- Dropdown Filter: **ID: `schedule-filter`** (filter by class type: Yoga, CrossFit, Pilates, Boxing, etc.)
- Classes Grid Div: **ID: `classes-grid`**
- Each class card includes:
  - Button: **ID: `enroll-class-button-{class_id}`** (action: enroll in class, no navigation)

### 2.5 Trainer Profiles Page (`/trainers`)
- Container Div: **ID: `trainers-page`**
- Search Input: **ID: `trainer-search`** (search by name or specialty)
- Dropdown Filter: **ID: `specialty-filter`** (filter by specialty: Strength, Cardio, Flexibility, Weight Loss)
- Trainers Grid Div: **ID: `trainers-grid`**
- Each trainer card:
  - Button: **ID: `view-trainer-button-{trainer_id}`** navigates to `/trainers/<trainer_id>`

### 2.6 Trainer Detail Page (`/trainers/<int:trainer_id>`)
- Container Div: **ID: `trainer-detail-page`**
- Heading H1: **ID: `trainer-name`**
- Biography Div: **ID: `trainer-bio`**
- Certifications Div: **ID: `trainer-certifications`**
- Button: **ID: `book-session-button`** navigates to `/book-training` with pre-selected trainer
- Reviews Div: **ID: `trainer-reviews`** (client reviews, static or extendable)

### 2.7 PT Booking Page (`/book-training`)
- Container Div: **ID: `booking-page`**
- Dropdown: **ID: `select-trainer`** (list of trainers populated from `trainers.txt`)
- Date Input: **ID: `session-date`**
- Time Dropdown: **ID: `session-time`** (available time slots)
- Duration Dropdown: **ID: `session-duration`** (options: 30, 60, 90 minutes)
- Button: **ID: `confirm-booking-button`** (confirms and saves booking)

### 2.8 Workout Records Page (`/workouts`)
- Container Div: **ID: `workouts-page`**
- Table: **ID: `workouts-table`** (columns: date, type, duration, calories burned)
- Dropdown Filter: **ID: `filter-by-type`** (filter by workout type: Class, PT Session, Personal)
- Button: **ID: `log-workout-button`** navigates to `/log-workout`
- Button: **ID: `back-to-dashboard`** navigates to `/dashboard`

### 2.9 Log Workout Page (`/log-workout`)
- Container Div: **ID: `log-workout-page`**
- Dropdown: **ID: `workout-type`** (Cardio, Strength, Flexibility, Sports)
- Number Input: **ID: `workout-duration`** (minutes)
- Number Input: **ID: `calories-burned`**
- Textarea: **ID: `workout-notes`**
- Button: **ID: `submit-workout-button`** (submits workout record)

---

## 3. Data Files and Formats
Data is stored in local text files inside the `data` directory.

### 3.1 Memberships Data
- File: `data/memberships.txt`
- Format (pipe `|` separated):
  ```
  membership_id|plan_name|price|billing_cycle|features|max_classes
  ```
- Example:
  ```
  1|Basic|29.99|monthly|Gym access, 2 classes per week|8
  2|Premium|59.99|monthly|Gym access, 5 classes per week, 2 PT sessions|20
  3|Elite|99.99|monthly|Unlimited gym access, unlimited classes, 4 PT sessions, nutrition coaching|unlimited
  ```
- Usage:
  - Load all memberships for display on Membership Plans page.
  - Filter by plan_name or type for the plan-filter dropdown.
  - Show details on Plan Details page by matching `membership_id`.

### 3.2 Classes Data
- File: `data/classes.txt`
- Format:
  ```
  class_id|class_name|trainer_id|class_type|schedule_day|schedule_time|capacity|duration
  ```
- Example:
  ```
  1|Morning Yoga|1|Yoga|Monday|06:00|20|60
  2|CrossFit Bootcamp|2|CrossFit|Tuesday|18:00|15|45
  3|Pilates Core|3|Pilates|Wednesday|10:00|18|50
  ```
- Usage:
  - Display all classes on Class Schedule page.
  - Search/filter classes by name, trainer (lookup trainer_id in trainers.txt), or class_type.
  - Use class_id for enroll actions.

### 3.3 Trainers Data
- File: `data/trainers.txt`
- Format:
  ```
  trainer_id|name|specialty|certifications|experience_years|bio
  ```
- Example:
  ```
  1|Sarah Johnson|Yoga & Flexibility|Certified Yoga Instructor, CPR|8|Expert in mind-body wellness and injury prevention
  2|Mike Thompson|Strength & Conditioning|NASM-CPT, CrossFit Level 2|10|Specializes in powerlifting and functional fitness
  3|Emma Davis|Pilates|Pilates Method Alliance Certified|6|Focus on core strength and postural alignment
  ```
- Usage:
  - List trainers on Trainer Profiles page.
  - Filter/search by name or specialty.
  - Fetch trainer details for Trainer Detail page and populate booking dropdown.

### 3.4 Bookings Data
- File: `data/bookings.txt`
- Format:
  ```
  booking_id|member_name|trainer_id|booking_date|booking_time|duration_minutes|status
  ```
- Example:
  ```
  1|John Doe|1|2025-01-20|10:00|60|Confirmed
  2|Jane Smith|2|2025-01-21|14:00|45|Confirmed
  3|Alex Johnson|3|2025-01-22|16:00|60|Pending
  ```
- Usage:
  - Store bookings confirmed from PT Booking page.
  - Status may reflect booking confirmation state.

### 3.5 Workouts Data
- File: `data/workouts.txt`
- Format:
  ```
  workout_id|member_name|workout_type|workout_date|duration_minutes|calories_burned|notes
  ```
- Example:
  ```
  1|John Doe|Cardio|2025-01-15|45|350|Morning run on treadmill
  2|Jane Smith|Strength|2025-01-16|60|420|Upper body weight training with trainer
  3|Alex Johnson|Class|2025-01-17|50|380|CrossFit Bootcamp session
  ```
- Usage:
  - Show workout history on Workout Records page.
  - Allow adding new workout records from Log Workout page.

---

## 4. Navigation and Actions Summary

| From Page                | Button ID                       | Action / Navigation Target                 |
|--------------------------|--------------------------------|--------------------------------------------|
| Dashboard                | browse-membership-button         | `/memberships`                             |
| Dashboard                | view-schedule-button             | `/schedule`                               |
| Dashboard                | book-trainer-button              | `/book-training`                          |
| Membership Plans          | view-details-button-{plan_id}   | `/memberships/<plan_id>`                   |
| Membership Plans          | back-to-dashboard               | `/dashboard`                              |
| Plan Details             | enroll-plan-button              | enroll action (simulated or logged)        |
| Class Schedule            | enroll-class-button-{class_id} | enroll in class action (no navigation)    |
| Trainer Profiles          | view-trainer-button-{trainer_id}| `/trainers/<trainer_id>`                   |
| Trainer Detail            | book-session-button             | `/book-training` (with pre-selected trainer) |
| PT Booking                | confirm-booking-button          | Confirm and save booking                    |
| Workout Records           | log-workout-button              | `/log-workout`                            |
| Workout Records           | back-to-dashboard               | `/dashboard`                              |
| Log Workout               | submit-workout-button           | Submit workout record                       |

---

## 5. Additional Notes
- The application has no user authentication; all pages and actions are directly accessible.
- The dashboard page is the starting page (`/dashboard` or `/`).
- All route paths are uniquely defined with clear HTTP methods.
- Data files reside under `data/` directory relative to app root.
- Template files named consistently with route page names (e.g., `dashboard.html`, `memberships.html`, etc.)
- Element IDs are unique and clearly named; dynamic IDs include identifiers (plan_id, class_id, trainer_id) as specified.
- Button actions either navigate to routes or trigger data save actions as designated.

---

# End of GymMembership Design Specification
