# GymMembership Flask Application Design Candidate B

---

## 1. Application Overview
- The application is a Flask web app named "GymMembership" that manages membership plans, classes, trainers, bookings, and workout records.
- All data is stored in local text files under a `data` directory.
- No user authentication is implemented; all users have direct access.
- The starting page is the Dashboard (`/dashboard`).

---

## 2. Flask Routes and Page Specifications

### 2.1 Dashboard Page
- **Route Path:** `/dashboard`
- **Page Title:** "Gym Membership Dashboard"
- **Template:** `dashboard.html`
- **Elements:**
  - `dashboard-page` (div container)
  - `member-welcome` (div for member welcome and status)
  - Navigation Buttons:
    - `browse-membership-button` → navigates to `/memberships`
    - `view-schedule-button` → navigates to `/schedule`
    - `book-trainer-button` → navigates to `/book-training`

### 2.2 Membership Plans Page
- **Route Path:** `/memberships`
- **Page Title:** "Membership Plans"
- **Template:** `memberships.html`
- **Elements:**
  - `membership-page` (div container)
  - `plan-filter` (dropdown to filter plans by type: Basic, Premium, Elite)
  - `plans-grid` (div grid containing membership plan cards)
  - Each plan card has:
    - `view-details-button-{plan_id}` (button) to view details on `/memberships/<plan_id>`
  - `back-to-dashboard` (button) navigates back to `/dashboard`
- **Data Source:** `data/memberships.txt` read and parsed for plans

### 2.3 Plan Details Page
- **Route Path:** `/memberships/<int:plan_id>`
- **Page Title:** "Plan Details"
- **Template:** `plan_details.html`
- **Elements:**
  - `plan-details-page` (div container)
  - `plan-title` (h1 showing plan name)
  - `plan-price` (div for price and billing cycle)
  - `plan-features` (div with list of features)
  - `enroll-plan-button` (button to enroll - action can be stubbed since no auth)
  - `plan-reviews` (div for member reviews - can be static or pulled from a file if extended)
- **Data Source:** from `memberships.txt` entry matching `plan_id`

### 2.4 Class Schedule Page
- **Route Path:** `/schedule`
- **Page Title:** "Class Schedule"
- **Template:** `schedule.html`
- **Elements:**
  - `schedule-page` (div container)
  - `schedule-search` (input text to search class by name or trainer)
  - `schedule-filter` (dropdown to filter classes by type like Yoga, CrossFit,...)
  - `classes-grid` (div grid listing class cards)
  - Each class card has `enroll-class-button-{class_id}` button to enroll (action can be mocked)
- **Data Sources:**
  - `data/classes.txt` for classes
  - `data/trainers.txt` to map trainer_id to trainer name for display

### 2.5 Trainer Profiles Page
- **Route Path:** `/trainers`
- **Page Title:** "Trainer Profiles"
- **Template:** `trainers.html`
- **Elements:**
  - `trainers-page` (div container)
  - `trainer-search` (input text to search trainers by name or specialty)
  - `specialty-filter` (dropdown filter for Strength, Cardio, Flexibility, Weight Loss)
  - `trainers-grid` (div grid of trainer cards)
  - Each trainer card has `view-trainer-button-{trainer_id}` button to view profile `/trainers/<trainer_id>`
- **Data Source:** `data/trainers.txt`

### 2.6 Trainer Detail Page
- **Route Path:** `/trainers/<int:trainer_id>`
- **Page Title:** "Trainer Profile"
- **Template:** `trainer_detail.html`
- **Elements:**
  - `trainer-detail-page` (div container)
  - `trainer-name` (h1)
  - `trainer-bio` (div)
  - `trainer-certifications` (div)
  - `book-session-button` (button to book session - navigates to `/book-training` with trainer selected)
  - `trainer-reviews` (div for client reviews, can be static or extended)
- **Data Source:** `data/trainers.txt` entry matching `trainer_id`

### 2.7 PT Booking Page
- **Route Path:** `/book-training`
- **Page Title:** "Book Personal Training"
- **Template:** `booking.html`
- **Elements:**
  - `booking-page` (div container)
  - `select-trainer` (dropdown to select trainer; populated from `trainers.txt`)
  - `session-date` (input date picker)
  - `session-time` (dropdown for time slots, e.g. formatted on frontend or static)
  - `session-duration` (dropdown: 30, 60, 90 minutes)
  - `confirm-booking-button` (button to confirm booking; on submit writes to `bookings.txt`)
- **Data Source:** `data/trainers.txt`

### 2.8 Workout Records Page
- **Route Path:** `/workouts`
- **Page Title:** "My Workout Records"
- **Template:** `workouts.html`
- **Elements:**
  - `workouts-page` (div container)
  - `workouts-table` (table showing workout history: date, type, duration, calories burned)
  - `filter-by-type` (dropdown filter: Class, PT Session, Personal)
  - `log-workout-button` (button navigates to `/log-workout`)
  - `back-to-dashboard` (button navigates to `/dashboard`)
- **Data Source:** `data/workouts.txt` parsed by current user name (or all if no auth)

### 2.9 Log Workout Page
- **Route Path:** `/log-workout`
- **Page Title:** "Log Workout"
- **Template:** `log_workout.html`
- **Elements:**
  - `log-workout-page` (div container)
  - `workout-type` (dropdown: Cardio, Strength, Flexibility, Sports)
  - `workout-duration` (input number for minutes)
  - `calories-burned` (input number)
  - `workout-notes` (textarea)
  - `submit-workout-button` (button to submit and write to `workouts.txt`)

---

## 3. Navigation Button IDs and Behaviors
- Dashboard:
  - `browse-membership-button` → `/memberships`
  - `view-schedule-button` → `/schedule`
  - `book-trainer-button` → `/book-training`

- Membership Plans:
  - `view-details-button-{plan_id}` → `/memberships/<plan_id>`
  - `back-to-dashboard` → `/dashboard`

- Class Schedule:
  - `enroll-class-button-{class_id}` (enroll action, no navigation)

- Trainer Profiles:
  - `view-trainer-button-{trainer_id}` → `/trainers/<trainer_id>`

- Trainer Detail:
  - `book-session-button` → `/book-training` (trainer pre-selected)

- Booking Page:
  - `confirm-booking-button` → submits booking to `bookings.txt`

- Workout Records:
  - `log-workout-button` → `/log-workout`
  - `back-to-dashboard` → `/dashboard`

- Log Workout:
  - `submit-workout-button` → submits workout record to `workouts.txt`

---

## 4. Data File Integration and Formats

### 4.1 Directory Structure
- All data stored under `data/` in app root.

### 4.2 Memberships Data
- File: `data/memberships.txt`
- Format (pipe `|` separated):
  `membership_id|plan_name|price|billing_cycle|features|max_classes`
- Usage:
  - Read all entries to list plans on Membership Plans page.
  - Lookup by `membership_id` for Plan Details.

### 4.3 Classes Data
- File: `data/classes.txt`
- Format:
  `class_id|class_name|trainer_id|class_type|schedule_day|schedule_time|capacity|duration`
- Usage:
  - Display classes on Class Schedule page.
  - Join trainer info from `trainers.txt` by `trainer_id`.

### 4.4 Trainers Data
- File: `data/trainers.txt`
- Format:
  `trainer_id|name|specialty|certifications|experience_years|bio`
- Usage:
  - Populate Trainers page list and filters.
  - Fetch details for Trainer Detail page.
  - Populate dropdown for booking trainers selection.

### 4.5 Bookings Data
- File: `data/bookings.txt`
- Format:
  `booking_id|member_name|trainer_id|booking_date|booking_time|duration_minutes|status`
- Usage:
  - Store new bookings from Booking Page.
  - No direct page to display bookings (can be extended later).

### 4.6 Workouts Data
- File: `data/workouts.txt`
- Format:
  `workout_id|member_name|workout_type|workout_date|duration_minutes|calories_burned|notes`
- Usage:
  - Display user workouts on Workout Records page.
  - Allow adding new records on Log Workout page.

---

## 5. Summary
This design provides all routes, page titles, UI element IDs, navigation behaviors, and file data formats needed for independent Flask app implementation. The no-auth user flow starts from the dashboard, with comprehensive browsing and management of workout and training resources supported by text file data integration.

All template files mentioned (e.g., `dashboard.html`, `memberships.html`, `plan_details.html`, etc.) will incorporate the specified IDs and UI components to achieve the defined user experience and data bindings.

---

End of design_candidate_b.md
