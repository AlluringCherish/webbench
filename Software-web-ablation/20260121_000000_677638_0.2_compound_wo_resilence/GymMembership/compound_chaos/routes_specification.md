# Routes Specification for GymMembership Backend

This document describes the routes, their functions and necessary parameters for the GymMembership web application backend.

## Routes Overview

1. **Dashboard Route**
   - URL: `/` 
   - Function: `dashboard()`
   - Purpose: Displays the Gym Membership homepage with member highlights, featured classes, and quick navigation links.

2. **Membership Plans Route**
   - URL: `/plans` 
   - Function: `list_plans()`
   - Purpose: Display available membership plans with brief details and buttons to view details.

3. **Membership Plan Details Route**
   - URL: `/plan/<int:plan_id>` 
   - Function: `view_plan(plan_id)`
   - Purpose: Show detailed information about a specific membership plan including reviews.

4. **Class Schedule Route**
   - URL: `/schedule` 
   - Function: `view_schedule()`
   - Purpose: Display the class schedule, filterable by type or trainer.

5. **Trainers List Route**
   - URL: `/trainers` 
   - Function: `list_trainers()`
   - Purpose: Display list of trainers with filter options by name and specialty.

6. **Trainer Profile Route**
   - URL: `/trainer/<int:trainer_id>` 
   - Function: `view_trainer(trainer_id)`
   - Purpose: Show detailed profile of a specific trainer with biography, certifications, and reviews.

7. **Booking Page Route**
   - URL: `/book` 
   - Function: `book_session()`
   - Purpose: Page for users to book a personal training session with selectable trainer, date, time, and duration.

8. **Workout Records Route**
   - URL: `/workouts` 
   - Function: `workout_records()`
   - Purpose: Display user's workout records with filtering options and ability to log new workouts.

9. **Log Workout Route**
   - URL: `/log-workout` 
   - Function: `log_workout()`
   - Purpose: Page to log workout details such as type, duration, calories burned, and notes.


## Navigation

- Pages are interlinked with buttons and links using Flask's `url_for()` function with route names.

## Request & Response Details

- Membership Plan views (list and details) respond with plan data parsed from `memberships.txt`.
- Schedule data parsed from `schedule.txt`.
- Trainer data parsed from `trainers.txt`.
- Workout logs parsed and saved to `workouts.txt`.