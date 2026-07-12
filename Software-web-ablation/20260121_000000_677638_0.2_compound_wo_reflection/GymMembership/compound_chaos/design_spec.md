# Design Specification for GymMembership Web Application

---

## 1. Flask Routes Specification

| Route Path                 | Function Name           | HTTP Methods | Template Filename        | Context Variables (name: type)                                                                                  |
|----------------------------|------------------------|--------------|--------------------------|-----------------------------------------------------------------------------------------------------------------|
| `/`                        | root_redirect          | GET          | None (redirect)           | None                                                                                                            |
| `/dashboard`               | dashboard_page         | GET          | dashboard.html           | None                                                                                                            |
| `/memberships`             | membership_plans       | GET          | memberships.html         | memberships: list of dicts (membership_id: int, plan_name: str, price: str, billing_cycle: str, features: str, max_classes: str) |
| `/plan/<int:plan_id>`      | plan_details           | GET          | plan_details.html        | plan: dict (membership_id: int, plan_name: str, price: str, billing_cycle: str, features: str, max_classes: str)     |
| `/classes`                 | class_schedule         | GET          | classes.html             | classes: list of dicts (class_id: int, class_name: str, trainer_id: int, class_type: str, schedule_day: str, schedule_time: str, capacity: int, duration: int) |
| `/trainers`                | trainer_profiles       | GET          | trainers.html            | trainers: list of dicts (trainer_id: int, name: str, specialty: str, certifications: str, experience_years: int, bio: str) |
| `/trainer/<int:trainer_id>`| trainer_detail         | GET          | trainer_detail.html      | trainer: dict (trainer_id: int, name: str, specialty: str, certifications: str, experience_years: int, bio: str)        |
| `/booking`                 | pt_booking             | GET          | booking.html             | trainers: list of dicts (trainer_id: int, name: str)                                                             |
| `/booking/confirm`         | confirm_booking        | POST         | None (redirect or response) | booking_data: dict (member_name: str, trainer_id: int, booking_date: str, booking_time: str, duration_minutes: int) |
| `/workouts`                | workout_records        | GET          | workouts.html            | workouts: list of dicts (workout_id: int, member_name: str, workout_type: str, workout_date: str, duration_minutes: int, calories_burned: int, notes: str) |
| `/workouts/log`            | log_workout            | GET          | log_workout.html         | None                                                                                                            |
| `/workouts/log/submit`     | submit_workout         | POST         | None (redirect or response) | workout_log: dict (workout_type: str, workout_duration: int, calories_burned: int, workout_notes: str)               |

#### Notes:
- Root route (`/`) redirects to `/dashboard`.
- GET methods for page views; POST only for booking and workout log submissions.

---

## 2. HTML Template Specifications

### 1. dashboard.html
- **Page Title**: Gym Membership Dashboard
- **Element IDs:**
  - `dashboard-page`: Div - container for dashboard page.
  - `member-welcome`: Div - displays welcome message and membership status.
  - `browse-membership-button`: Button - navigates to Membership Plans page.
  - `view-schedule-button`: Button - navigates to Class Schedule page.
  - `book-trainer-button`: Button - navigates to PT Booking page.
- **Context Variables:** None
- **Navigation Buttons:**
  - `browse-membership-button`: url_for('membership_plans')
  - `view-schedule-button`: url_for('class_schedule')
  - `book-trainer-button`: url_for('pt_booking')

### 2. memberships.html
- **Page Title**: Membership Plans
- **Element IDs:**
  - `membership-page`: Div - container for membership plans page.
  - `plan-filter`: Dropdown - filter memberships by type (Basic, Premium, Elite).
  - `plans-grid`: Div - grid to display membership plan cards.
  - `view-details-button-<plan_id>`: Button - to view plan details for each plan card.
  - `back-to-dashboard`: Button - navigate back to dashboard.
- **Context Variables:**
  - `memberships`: list of dicts with keys: membership_id, plan_name, price, billing_cycle, features, max_classes.
- **Jinja2 usage:**
  ```jinja2
  {% for plan in memberships %}
    <div id="plan-card-{{ plan.membership_id }}">
      <h2>{{ plan.plan_name }}</h2>
      <p>Price: {{ plan.price }} / {{ plan.billing_cycle }}</p>
      <p>Features: {{ plan.features }}</p>
      <button id="view-details-button-{{ plan.membership_id }}" ...>View Details</button>
    </div>
  {% endfor %}
  ```
- **Navigation Buttons:**
  - `back-to-dashboard`: url_for('dashboard_page')

### 3. plan_details.html
- **Page Title**: Plan Details
- **Element IDs:**
  - `plan-details-page`: Div - container for the plan details page.
  - `plan-title`: H1 - plan name.
  - `plan-price`: Div - price and billing cycle.
  - `plan-features`: Div - features string.
  - `enroll-plan-button`: Button - enroll in plan.
  - `plan-reviews`: Div - member reviews section.
- **Context Variables:**
  - `plan`: dict with membership_id, plan_name, price, billing_cycle, features, max_classes.
- **Jinja2 usage:**
  - `{{ plan.plan_name }}`, `{{ plan.price }}`, etc.
- **Navigation Buttons:**
  - `enroll-plan-button`: (Assumed leads to enroll or confirmation page, if implemented)

### 4. classes.html
- **Page Title**: Class Schedule
- **Element IDs:**
  - `schedule-page`: Div - container for class schedule page.
  - `schedule-search`: Input - search classes by name or trainer.
  - `schedule-filter`: Dropdown - filter by class type (Yoga, CrossFit, Pilates, Boxing, etc.).
  - `classes-grid`: Div - grid showing class cards.
  - `enroll-class-button-<class_id>`: Button - enroll in class.
- **Context Variables:**
  - `classes`: list of dicts with class_id, class_name, trainer_id, class_type, schedule_day, schedule_time, capacity, duration.
- **Jinja2 usage:**
  ```jinja2
  {% for cls in classes %}
    <div id="class-card-{{ cls.class_id }}">
      <h3>{{ cls.class_name }}</h3>
      <p>Trainer ID: {{ cls.trainer_id }}</p>
      <p>Type: {{ cls.class_type }}</p>
      <button id="enroll-class-button-{{ cls.class_id }}">Enroll</button>
    </div>
  {% endfor %}
  ```
- **Navigation Buttons:** None specified.

### 5. trainers.html
- **Page Title**: Trainer Profiles
- **Element IDs:**
  - `trainers-page`: Div - container for trainers page.
  - `trainer-search`: Input - search trainers by name or specialty.
  - `specialty-filter`: Dropdown - filter by specialty.
  - `trainers-grid`: Div - grid for trainer cards.
  - `view-trainer-button-<trainer_id>`: Button - view trainer profile.
- **Context Variables:**
  - `trainers`: list of dicts with trainer_id, name, specialty, certifications, experience_years, bio.
- **Jinja2 usage:**
  ```jinja2
  {% for trainer in trainers %}
    <div id="trainer-card-{{ trainer.trainer_id }}">
      <h3>{{ trainer.name }}</h3>
      <p>Specialty: {{ trainer.specialty }}</p>
      <button id="view-trainer-button-{{ trainer.trainer_id }}">View Profile</button>
    </div>
  {% endfor %}
  ```
- **Navigation Buttons:** None specified.

### 6. trainer_detail.html
- **Page Title**: Trainer Profile
- **Element IDs:**
  - `trainer-detail-page`: Div - container for trainer detail page.
  - `trainer-name`: H1 - trainer's full name.
  - `trainer-bio`: Div - biography and experience.
  - `trainer-certifications`: Div - certifications list.
  - `book-session-button`: Button - book session with trainer.
  - `trainer-reviews`: Div - reviews section.
- **Context Variables:**
  - `trainer`: dict with trainer_id, name, specialty, certifications, experience_years, bio.
- **Jinja2 usage:**
  - Direct variable insertion with `{{ trainer.name }}`, etc.
- **Navigation Buttons:**
  - `book-session-button`: url_for('pt_booking') or if booking with specific trainer, could pass trainer_id as parameter.

### 7. booking.html
- **Page Title**: Book Personal Training
- **Element IDs:**
  - `booking-page`: Div - container for booking page.
  - `select-trainer`: Dropdown - select trainer.
  - `session-date`: Input (date) - select session date.
  - `session-time`: Dropdown - select session time slot.
  - `session-duration`: Dropdown - select duration (30, 60, 90).
  - `confirm-booking-button`: Button - submit booking.
- **Context Variables:**
  - `trainers`: list of dicts with trainer_id, name.
- **Jinja2 usage:**
  ```jinja2
  <select id="select-trainer">
    {% for t in trainers %}
      <option value="{{ t.trainer_id }}">{{ t.name }}</option>
    {% endfor %}
  </select>
  ```
- **Navigation Buttons:** None specified.

### 8. workouts.html
- **Page Title**: My Workout Records
- **Element IDs:**
  - `workouts-page`: Div - container for workouts page.
  - `workouts-table`: Table - displays workout history.
  - `filter-by-type`: Dropdown - filter workouts by type.
  - `log-workout-button`: Button - navigate to Log Workout page.
  - `back-to-dashboard`: Button - navigate back to dashboard.
- **Context Variables:**
  - `workouts`: list of dicts with workout_id, member_name, workout_type, workout_date, duration_minutes, calories_burned, notes.
- **Jinja2 usage:**
  ```jinja2
  <table id="workouts-table">
    <thead>
      <tr>
        <th>Date</th><th>Type</th><th>Duration (min)</th><th>Calories Burned</th><th>Notes</th></tr>
    </thead>
    <tbody>
    {% for w in workouts %}
      <tr>
        <td>{{ w.workout_date }}</td>
        <td>{{ w.workout_type }}</td>
        <td>{{ w.duration_minutes }}</td>
        <td>{{ w.calories_burned }}</td>
        <td>{{ w.notes }}</td>
      </tr>
    {% endfor %}
    </tbody>
  </table>
  ```
- **Navigation Buttons:**
  - `log-workout-button`: url_for('log_workout')
  - `back-to-dashboard`: url_for('dashboard_page')

### 9. log_workout.html
- **Page Title**: Log Workout
- **Element IDs:**
  - `log-workout-page`: Div - container for log workout page.
  - `workout-type`: Dropdown - select workout type (Cardio, Strength, Flexibility, Sports).
  - `workout-duration`: Input (number) - input workout duration in minutes.
  - `calories-burned`: Input (number) - input calories burned.
  - `workout-notes`: Textarea - input notes.
  - `submit-workout-button`: Button - submit workout log.
- **Context Variables:** None
- **Jinja2 usage:** static dropdown options or could be dynamically generated if needed.
- **Navigation Buttons:** None specified.

---

## 3. Data File Schemas

### 1. memberships.txt
- **Filename:** memberships.txt
- **Format:** Pipe (`|`) delimited text file
- **Fields and Data Types (in exact order):**
  1. membership_id (int)
  2. plan_name (str)
  3. price (str) - formatted as string with decimals (e.g., "29.99")
  4. billing_cycle (str) - e.g., "monthly"
  5. features (str) - comma separated list or comma with spaces
  6. max_classes (str) - numerical or "unlimited"
- **Purpose:** Stores all available membership plans, their pricing and features.
- **Examples:**
  ```text
  1|Basic|29.99|monthly|Gym access, 2 classes per week|8
  2|Premium|59.99|monthly|Gym access, 5 classes per week, 2 PT sessions|20
  3|Elite|99.99|monthly|Unlimited gym access, unlimited classes, 4 PT sessions, nutrition coaching|unlimited
  ```

### 2. classes.txt
- **Filename:** classes.txt
- **Format:** Pipe (`|`) delimited text file
- **Fields and Data Types (in exact order):**
  1. class_id (int)
  2. class_name (str)
  3. trainer_id (int)
  4. class_type (str)
  5. schedule_day (str)
  6. schedule_time (str) - 24-hour format HH:MM
  7. capacity (int)
  8. duration (int) - in minutes
- **Purpose:** Stores fitness class schedules and details.
- **Examples:**
  ```text
  1|Morning Yoga|1|Yoga|Monday|06:00|20|60
  2|CrossFit Bootcamp|2|CrossFit|Tuesday|18:00|15|45
  3|Pilates Core|3|Pilates|Wednesday|10:00|18|50
  ```

### 3. trainers.txt
- **Filename:** trainers.txt
- **Format:** Pipe (`|`) delimited text file
- **Fields and Data Types (in exact order):**
  1. trainer_id (int)
  2. name (str)
  3. specialty (str) - may contain multiple specialties separated by & or commas.
  4. certifications (str) - comma separated list.
  5. experience_years (int)
  6. bio (str) - text biography
- **Purpose:** Stores trainer profiles with expertise and credentials.
- **Examples:**
  ```text
  1|Sarah Johnson|Yoga & Flexibility|Certified Yoga Instructor, CPR|8|Expert in mind-body wellness and injury prevention
  2|Mike Thompson|Strength & Conditioning|NASM-CPT, CrossFit Level 2|10|Specializes in powerlifting and functional fitness
  3|Emma Davis|Pilates|Pilates Method Alliance Certified|6|Focus on core strength and postural alignment
  ```

### 4. bookings.txt
- **Filename:** bookings.txt
- **Format:** Pipe (`|`) delimited text file
- **Fields and Data Types (in exact order):**
  1. booking_id (int)
  2. member_name (str)
  3. trainer_id (int)
  4. booking_date (str) - YYYY-MM-DD
  5. booking_time (str) - HH:MM
  6. duration_minutes (int)
  7. status (str) - e.g. "Confirmed", "Pending"
- **Purpose:** Stores personal training session bookings.
- **Examples:**
  ```text
  1|John Doe|1|2025-01-20|10:00|60|Confirmed
  2|Jane Smith|2|2025-01-21|14:00|45|Confirmed
  3|Alex Johnson|3|2025-01-22|16:00|60|Pending
  ```

### 5. workouts.txt
- **Filename:** workouts.txt
- **Format:** Pipe (`|`) delimited text file
- **Fields and Data Types (in exact order):**
  1. workout_id (int)
  2. member_name (str)
  3. workout_type (str) - e.g. Cardio, Strength, Flexibility, Sports, Class, PT Session, Personal
  4. workout_date (str) - YYYY-MM-DD
  5. duration_minutes (int)
  6. calories_burned (int)
  7. notes (str)
- **Purpose:** Stores user workout history and logs.
- **Examples:**
  ```text
  1|John Doe|Cardio|2025-01-15|45|350|Morning run on treadmill
  2|Jane Smith|Strength|2025-01-16|60|420|Upper body weight training with trainer
  3|Alex Johnson|Class|2025-01-17|50|380|CrossFit Bootcamp session
  ```

---

**Critical:** Field order and exact field names must be strictly followed for backend data processing compatibility.

---

_End of GymMembership Design Specification._
