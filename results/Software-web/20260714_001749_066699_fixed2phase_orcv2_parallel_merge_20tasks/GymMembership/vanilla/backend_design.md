# GymMembership Backend Design Specification

---

## Section 1: Flask Routes Specification

### 1. Dashboard Page
- **Route:** `/`
- **Methods:** GET
- **Behavior:**
  - Load member highlights (can be static or dynamic data if applicable).
  - Load some featured classes and recent activity summaries.
  - Render template: `dashboard.html`
- **Context Variables:**
  - `member_status` (str): Basic welcome/status message (e.g., "Welcome, guest user!")
  - `featured_classes` (list of dict): Sample classes info for dashboard display.

---

### 2. Membership Plans Page
- **Route:** `/memberships`
- **Methods:** GET
- **Behavior:**
  - Read all membership plans from `data/memberships.txt`.
  - Optional query param: `type` to filter by membership type (Basic, Premium, Elite).
  - Render template: `memberships.html`
- **Context Variables:**
  - `plans` (list of dict): Each dict representing a membership plan with keys:
    - `membership_id` (int)
    - `plan_name` (str)
    - `price` (float)
    - `billing_cycle` (str)
    - `features` (str)
    - `max_classes` (int or str)
  - `selected_type` (str or None): Current filter value

---

### 3. Plan Details Page
- **Route:** `/membership/<int:membership_id>`
- **Methods:** GET
- **Behavior:**
  - Read all plans from `memberships.txt`.
  - Find plan matching `membership_id`.
  - Load reviews if implemented (static or file based - reviews not specified in requirements so may be omitted or placeholder).
  - Render template: `plan_details.html`
- **Context Variables:**
  - `plan` (dict): Plan details same structure as in Memberships page.
  - `reviews` (list of dict): Each dict with keys like `reviewer`, `comment`. (Optional placeholder)

---

### 4. Class Schedule Page
- **Route:** `/classes`
- **Methods:** GET
- **Behavior:**
  - Read all classes from `data/classes.txt`.
  - Accept optional query params:
    - `search` to filter by class name or trainer name (requires cross data lookup with trainers).
    - `type` to filter by class type.
  - Join with trainer data (from `trainers.txt`) to get trainer names.
  - Render template: `classes.html`
- **Context Variables:**
  - `classes` (list of dict): Each dict with keys:
    - `class_id` (int)
    - `class_name` (str)
    - `trainer_id` (int)
    - `trainer_name` (str)
    - `class_type` (str)
    - `schedule_day` (str)
    - `schedule_time` (str)
    - `capacity` (int)
    - `duration` (int)
  - `search_term` (str): Current search term used
  - `selected_type` (str or None): Current class type filter

---

### 5. Trainer Profiles Page
- **Route:** `/trainers`
- **Methods:** GET
- **Behavior:**
  - Read all trainers from `data/trainers.txt`.
  - Optional filters:
    - `search` to filter by trainer name or specialty.
    - `specialty` to filter by specialty.
  - Render template: `trainers.html`
- **Context Variables:**
  - `trainers` (list of dict): Each dict with keys:
    - `trainer_id` (int)
    - `name` (str)
    - `specialty` (str)
    - `certifications` (str)
    - `experience_years` (int)
    - `bio` (str)
  - `search_term` (str)
  - `selected_specialty` (str or None)

---

### 6. Trainer Detail Page
- **Route:** `/trainer/<int:trainer_id>`
- **Methods:** GET
- **Behavior:**
  - Read trainer details from `trainers.txt`.
  - Load reviews if implemented (not specified, placeholder or empty list).
  - Render template: `trainer_detail.html`
- **Context Variables:**
  - `trainer` (dict): Single trainer info
  - `reviews` (list of dict): Reviews for trainer (empty or placeholder)

---

### 7. PT Booking Page
- **Route:** `/booking`
- **Methods:** GET, POST
- **Behavior:**
  - GET:
    - Load all trainers from `trainers.txt` for dropdown.
    - Render template: `booking.html`
  - POST:
    - Receive form data:
      - `member_name` (string) [Since no authentication, user inputs name]
      - `trainer_id` (int)
      - `session_date` (YYYY-MM-DD string)
      - `session_time` (HH:MM string)
      - `session_duration` (int, e.g., 30, 60, 90)
    - Validate inputs.
    - Generate a new `booking_id` (max existing + 1 or 1 if none).
    - Append booking record to `data/bookings.txt` with status `Pending`.
    - Redirect or render confirmation.
- **Context Variables for GET:**
  - `trainers` (list of dict): List of trainers with `trainer_id` and `name`

---

### 8. Workout Records Page
- **Route:** `/workouts`
- **Methods:** GET
- **Behavior:**
  - Read workouts from `data/workouts.txt`.
  - Filter by workout type query param (optional).
  - Render template: `workouts.html`
- **Context Variables:**
  - `workouts` (list of dict): Each dict includes:
    - `workout_id` (int)
    - `member_name` (string)
    - `workout_type` (string)
    - `workout_date` (string, YYYY-MM-DD)
    - `duration_minutes` (int)
    - `calories_burned` (int)
    - `notes` (string)
  - `selected_type` (str or None)

---

### 9. Log Workout Page
- **Route:** `/log-workout`
- **Methods:** GET, POST
- **Behavior:**
  - GET:
    - Render `log_workout.html` template
  - POST:
    - Receive form data:
      - `member_name` (string)
      - `workout_type` (string)
      - `workout_duration` (int)
      - `calories_burned` (int)
      - `workout_notes` (string)
      - `workout_date` (optional, default to current date if not provided)
    - Generate new workout_id.
    - Append workout record to `data/workouts.txt`.
    - Redirect to workouts page or confirm logging.
- **Context Variables for GET:** None (blank form)

---

## Section 2: Data Storage and File Formats

The application stores all data files in the `data/` directory (relative to the Flask app root). Text files use pipe character `|` as a delimiter. Each file represents one entity type with one record per line.

---

### 1. Memberships Data
- **File:** `data/memberships.txt`
- **Format:**
  ```
  membership_id|plan_name|price|billing_cycle|features|max_classes
  ```
- **Field Types:**
  - `membership_id`: int
  - `plan_name`: str
  - `price`: float
  - `billing_cycle`: str
  - `features`: str (comma separated list in one string)
  - `max_classes`: int or str (e.g., "unlimited")
- **Example Line:**
  ```
  1|Basic|29.99|monthly|Gym access, 2 classes per week|8
  ```
- **Reading Logic:**
  - Split line by `|` into fields
  - Convert membership_id and price appropriately
  - Convert max_classes to int; if "unlimited", keep as string

---

### 2. Classes Data
- **File:** `data/classes.txt`
- **Format:**
  ```
  class_id|class_name|trainer_id|class_type|schedule_day|schedule_time|capacity|duration
  ```
- **Field Types:**
  - `class_id`: int
  - `class_name`: str
  - `trainer_id`: int
  - `class_type`: str
  - `schedule_day`: str
  - `schedule_time`: str (HH:MM)
  - `capacity`: int
  - `duration`: int (minutes)
- **Example Line:**
  ```
  1|Morning Yoga|1|Yoga|Monday|06:00|20|60
  ```

---

### 3. Trainers Data
- **File:** `data/trainers.txt`
- **Format:**
  ```
  trainer_id|name|specialty|certifications|experience_years|bio
  ```
- **Field Types:**
  - `trainer_id`: int
  - `name`: str
  - `specialty`: str
  - `certifications`: str
  - `experience_years`: int
  - `bio`: str
- **Example Line:**
  ```
  1|Sarah Johnson|Yoga & Flexibility|Certified Yoga Instructor, CPR|8|Expert in mind-body wellness and injury prevention
  ```

---

### 4. Bookings Data
- **File:** `data/bookings.txt`
- **Format:**
  ```
  booking_id|member_name|trainer_id|booking_date|booking_time|duration_minutes|status
  ```
- **Field Types:**
  - `booking_id`: int
  - `member_name`: str
  - `trainer_id`: int
  - `booking_date`: str (YYYY-MM-DD)
  - `booking_time`: str (HH:MM)
  - `duration_minutes`: int
  - `status`: str (e.g., "Pending", "Confirmed")
- **Example Line:**
  ```
  1|John Doe|1|2025-01-20|10:00|60|Confirmed
  ```
- **Read Logic:**
  - Parse fields, convert types.
- **Update Logic:**
  - For new bookings: append a new line with generated booking_id.
  - For updating status (if feature extended): read all, modify line, rewrite file.

---

### 5. Workouts Data
- **File:** `data/workouts.txt`
- **Format:**
  ```
  workout_id|member_name|workout_type|workout_date|duration_minutes|calories_burned|notes
  ```
- **Field Types:**
  - `workout_id`: int
  - `member_name`: str
  - `workout_type`: str
  - `workout_date`: str (YYYY-MM-DD)
  - `duration_minutes`: int
  - `calories_burned`: int
  - `notes`: str
- **Example Line:**
  ```
  1|John Doe|Cardio|2025-01-15|45|350|Morning run on treadmill
  ```
- **Read Logic:**
  - Parse line and convert fields.
- **Update Logic:**
  - Append new workout record line on workout log.

---

## Summary
This backend design specifies each route needed to fulfill frontend navigation and functional requirements for the GymMembership app, with detailed context variables for templates.

Data is fully managed via parsing/updating pipe-delimited text files in the `data` directory.

No authentication or user accounts; all features operate with minimal user identification input.

This design document enables a backend developer to implement `app.py` independently with clear file I/O and routing requirements.

---

*End of backend_design.md*
