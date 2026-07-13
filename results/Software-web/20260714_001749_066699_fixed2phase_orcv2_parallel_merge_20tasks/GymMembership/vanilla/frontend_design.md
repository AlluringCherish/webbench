# GymMembership Frontend Design Specification

---

## Section 1: Template Structure and Elements

### 1. Dashboard Page
- **Template Path:** templates/dashboard.html
- **Page Title:** Gym Membership Dashboard
- **Main Container:**
  - ID: `dashboard-page` - Div
- **Elements:**
  - ID: `member-welcome` - Div (displays welcome message and member status info)
  - ID: `browse-membership-button` - Button (Navigate to Membership Plans page)
  - ID: `view-schedule-button` - Button (Navigate to Class Schedule page)
  - ID: `book-trainer-button` - Button (Navigate to PT Booking page)

---

### 2. Membership Plans Page
- **Template Path:** templates/membership_plans.html
- **Page Title:** Membership Plans
- **Main Container:**
  - ID: `membership-page` - Div
- **Elements:**
  - ID: `plan-filter` - Dropdown (Filter membership plans by type: Basic, Premium, Elite)
  - ID: `plans-grid` - Div (Grid container for plan cards)
  - ID Pattern: `view-details-button-{plan_id}` - Button (View detailed info of specific plan)
  - ID: `back-to-dashboard` - Button (Navigate back to Dashboard page)

---

### 3. Plan Details Page
- **Template Path:** templates/plan_details.html
- **Page Title:** Plan Details
- **Main Container:**
  - ID: `plan-details-page` - Div
- **Elements:**
  - ID: `plan-title` - H1 (Display plan name)
  - ID: `plan-price` - Div (Display price and billing cycle)
  - ID: `plan-features` - Div (Enumerate all features)
  - ID: `enroll-plan-button` - Button (Enroll in this plan)
  - ID: `plan-reviews` - Div (Show member reviews)

---

### 4. Class Schedule Page
- **Template Path:** templates/class_schedule.html
- **Page Title:** Class Schedule
- **Main Container:**
  - ID: `schedule-page` - Div
- **Elements:**
  - ID: `schedule-search` - Input (Search classes by name or trainer)
  - ID: `schedule-filter` - Dropdown (Filter classes by type, e.g., Yoga, CrossFit, etc.)
  - ID: `classes-grid` - Div (Grid for class cards)
  - ID Pattern: `enroll-class-button-{class_id}` - Button (Enroll in class)

---

### 5. Trainer Profiles Page
- **Template Path:** templates/trainer_profiles.html
- **Page Title:** Trainer Profiles
- **Main Container:**
  - ID: `trainers-page` - Div
- **Elements:**
  - ID: `trainer-search` - Input (Search trainers by name or specialty)
  - ID: `specialty-filter` - Dropdown (Filter trainers by specialty: Strength, Cardio, Flexibility, Weight Loss)
  - ID: `trainers-grid` - Div (Grid for trainer cards)
  - ID Pattern: `view-trainer-button-{trainer_id}` - Button (View trainer profile)

---

### 6. Trainer Detail Page
- **Template Path:** templates/trainer_detail.html
- **Page Title:** Trainer Profile
- **Main Container:**
  - ID: `trainer-detail-page` - Div
- **Elements:**
  - ID: `trainer-name` - H1 (Trainer full name)
  - ID: `trainer-bio` - Div (Biography and experience)
  - ID: `trainer-certifications` - Div (Certifications list)
  - ID: `book-session-button` - Button (Book personal training session with this trainer)
  - ID: `trainer-reviews` - Div (Client reviews section)

---

### 7. PT Booking Page
- **Template Path:** templates/pt_booking.html
- **Page Title:** Book Personal Training
- **Main Container:**
  - ID: `booking-page` - Div
- **Elements:**
  - ID: `select-trainer` - Dropdown (Select trainer for session)
  - ID: `session-date` - Input (date) (Choose date for session)
  - ID: `session-time` - Dropdown (Select time slot for session)
  - ID: `session-duration` - Dropdown (Select session duration: 30, 60, 90 minutes)
  - ID: `confirm-booking-button` - Button (Confirm the booking)

---

### 8. Workout Records Page
- **Template Path:** templates/workout_records.html
- **Page Title:** My Workout Records
- **Main Container:**
  - ID: `workouts-page` - Div
- **Elements:**
  - ID: `workouts-table` - Table (Display workout history with columns: Date, Type, Duration, Calories burned)
  - ID: `filter-by-type` - Dropdown (Filter workouts by type: Class, PT Session, Personal)
  - ID: `log-workout-button` - Button (Navigate to Log Workout page)
  - ID: `back-to-dashboard` - Button (Navigate back to Dashboard page)

---

### 9. Log Workout Page
- **Template Path:** templates/log_workout.html
- **Page Title:** Log Workout
- **Main Container:**
  - ID: `log-workout-page` - Div
- **Elements:**
  - ID: `workout-type` - Dropdown (Select workout type: Cardio, Strength, Flexibility, Sports)
  - ID: `workout-duration` - Input (number) (Input duration in minutes)
  - ID: `calories-burned` - Input (number) (Input estimated calories burned)
  - ID: `workout-notes` - Textarea (Add notes for workout details)
  - ID: `submit-workout-button` - Button (Submit workout record)

---

## Navigation Flows

- **From Dashboard:**
  - `browse-membership-button` -> Membership Plans page
  - `view-schedule-button` -> Class Schedule page
  - `book-trainer-button` -> PT Booking page

- **From Membership Plans Page:**
  - Clicking any `view-details-button-{plan_id}` -> Plan Details page
  - `back-to-dashboard` -> Dashboard page

- **From Plan Details Page:**
  - `enroll-plan-button` may trigger enrollment logic (stay on page or navigate)

- **From Class Schedule Page:**
  - Clicking any `enroll-class-button-{class_id}` registers enrollment (feedback via UI)

- **From Trainer Profiles Page:**
  - Clicking any `view-trainer-button-{trainer_id}` -> Trainer Detail page

- **From Trainer Detail Page:**
  - `book-session-button` -> PT Booking page with trainer pre-selected

- **From PT Booking Page:**
  - `confirm-booking-button` submits booking, may display confirmation or redirect

- **From Workout Records Page:**
  - `log-workout-button` -> Log Workout page
  - `back-to-dashboard` -> Dashboard page

- **From Log Workout Page:**
  - `submit-workout-button` submits workout and may navigate back to Workout Records page

---

## Section 2: Context Variables Specification

### Dashboard Page (`dashboard.html`)
- `member_status` : String (e.g. "Active Basic Member")
- `featured_classes`: List of classes to highlight (optional for UI)

### Membership Plans Page (`membership_plans.html`)
- `membership_plans`: List of dicts with keys:
  - `id`, `plan_name`, `price`, `billing_cycle`, `features` (List or comma-separated str)
- `filter_options`: List of plan types (Basic, Premium, Elite)

### Plan Details Page (`plan_details.html`)
- `plan`: Dict with keys:
  - `id`, `plan_name`, `price`, `billing_cycle`, `features` (List of strings)
- `reviews`: List of dicts with review details (member name, rating, comment)

### Class Schedule Page (`class_schedule.html`)
- `classes`: List of dicts with keys:
  - `class_id`, `class_name`, `trainer_name`, `class_type`, `schedule_day`, `schedule_time`, `capacity`, `duration`
- `class_types`: List of available class type strings for filter dropdown

### Trainer Profiles Page (`trainer_profiles.html`)
- `trainers`: List of dicts with keys:
  - `trainer_id`, `name`, `specialty`, `photo_url` (optional), `certifications` (optional)
- `specialty_options`: List of strings for specialties filter

### Trainer Detail Page (`trainer_detail.html`)
- `trainer`: Dict with keys:
  - `trainer_id`, `name`, `bio`, `certifications` (List or Str), `experience_years`
- `reviews`: List of dicts (client reviews)

### PT Booking Page (`pt_booking.html`)
- `trainers`: List of available trainers as dicts with `trainer_id`, `name`
- `available_timeslots`: List of strings for session times
- `session_durations`: List of integers [30, 60, 90]
- Optional: `preselected_trainer_id` (to preselect trainer when coming from trainer detail)

### Workout Records Page (`workout_records.html`)
- `workouts`: List of dicts with keys:
  - `workout_date`, `workout_type`, `duration_minutes`, `calories_burned`, `notes`
- `workout_type_filters`: List of strings ["Class", "PT Session", "Personal"]

### Log Workout Page (`log_workout.html`)
- `workout_types`: List of strings ["Cardio", "Strength", "Flexibility", "Sports"]

---

## Summary

This specification defines a complete front-end structure with explicit HTML element IDs, page navigation flows, and expected dynamic data context variables for all nine pages of the GymMembership web application. The frontend developer can implement all templates and interactive elements according to this spec, ensuring consistent UI behavior and navigation.
