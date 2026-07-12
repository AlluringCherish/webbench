# HTML Templates Specification for GymMembership Web Application

## 1. Dashboard (`dashboard.html`)
- Layout: Main page highlighting member features and quick navigation.
- Elements:
  - **Member Highlights** (ID: `member-info`) - Display logged member info.
  - **Featured Classes** (ID: `featured-classes`) - Show popular classes.
  - **Navigation Buttons:**
    - View Schedule Button (ID: `view-schedule-button`)
    - Book Trainer Button (ID: `book-trainer-button`)


## 2. Membership Plans List (`plans.html`)
- Layout: List all available membership plans.
- Elements:
  - Container Div (ID: `plans-container`)
  - Each Plan Div (ID: `plan-{plan_id}`):
    - Plan Name (ID: `plan-name-{plan_id}`)
    - Plan Price (ID: `plan-price-{plan_id}`)
    - View Details Button (ID: `view-details-button-{plan_id}`)
  - Back to Dashboard Button (ID: `back-to-dashboard`)

- Dynamic Data:
  - Loop over plans list to render all plans.


## 3. Membership Plan Detail (`plan_detail.html`)
- Layout: Show detailed plan information and reviews.
- Elements:
  - Plan Title (ID: `plan-title`)
  - Price (ID: `plan-price`)
  - Description (ID: `plan-description`)
  - Reviews Section (ID: `plan-reviews`)


## 4. Class Schedule (`schedule.html`)
- Layout: Shows schedule with search and filters.
- Elements:
  - Schedule Container (ID: `schedule-page`)
  - Search Input (ID: `schedule-search`)
  - Category Dropdown (ID: `schedule-category-filter`)
  - Classes Grid (ID: `classes-grid`)


## 5. Trainers List (`trainers.html`)
- Layout: Shows list of trainers with filters.
- Elements:
  - Trainers Container (ID: `trainers-page`)
  - Search by Name Field (ID: `trainer-search-name`)
  - Filter by Specialty Dropdown (ID: `trainer-specialty-filter`)
  - Trainers Grid (ID: `trainers-grid`)
  - View Trainer Profile Button (ID: `view-trainer-button-{trainer_id}`)


## 6. Trainer Profile (`trainer_detail.html`)
- Layout: Detailed trainer profile with bio, certifications, and booking button.
- Elements:
  - Trainer Name (ID: `trainer-name`)
  - Biography (ID: `trainer-biography`)
  - Certifications (ID: `trainer-certifications`)
  - Book Session Button (ID: `book-session-button`)
  - Reviews Section (ID: `trainer-reviews`)


## 7. Booking Page (`booking.html`)
- Layout: Form to book personal training sessions.
- Elements:
  - Trainer Select Dropdown (ID: `select-trainer`)
  - Session Date Picker (ID: `session-date`)
  - Session Time Dropdown (ID: `session-time`)
  - Session Duration Dropdown (ID: `session-duration`)
  - Submit Button (ID: `submit-booking-button`)


## 8. Workout Records (`workouts.html`)
- Layout: List of recorded workouts and filter option.
- Elements:
  - Workouts Table (ID: `workouts-table`)
  - Filter by Type Dropdown (ID: `filter-by-type`)
  - Log Workout Button (ID: `log-workout-button`)


## 9. Log Workout (`log_workout.html`)
- Layout: Form to input details of a workout log.
- Elements:
  - Workout Type Dropdown (ID: `workout-type`)
  - Duration Input (ID: `workout-duration`)
  - Calories Burned Input (ID: `calories-burned`)
  - Notes Textarea (ID: `workout-notes`)
  - Submit Button (ID: `submit-workout-button`)


---

Each template uses Jinja2 syntax for dynamic content rendering and Flask routes for navigation links.