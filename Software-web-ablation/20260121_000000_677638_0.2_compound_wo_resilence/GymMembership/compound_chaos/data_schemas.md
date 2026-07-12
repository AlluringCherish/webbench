# Data Schemas for GymMembership Backend

## Membership Plans (`memberships.txt`)
- Format: `plan_id|name|price|billing_period|description`
- Field Types:
  - `plan_id`: int
  - `name`: str
  - `price`: float
  - `billing_period`: str (e.g., monthly)
  - `description`: str
- Example:
  ```
  1|Basic|29.99|monthly|Gym access during staffed hours
  2|Premium|59.99|monthly|Gym access plus unlimited classes
  3|Elite|99.99|monthly|All access including personal training
  ```

## Class Schedule (`schedule.txt`)
- Format: `class_name|class_id|type|day|time|capacity|duration_minutes`
- Field Types:
  - `class_name`: str
  - `class_id`: int
  - `type`: str
  - `day`: str
  - `time`: str (HH:MM, 24-hour)
  - `capacity`: int
  - `duration_minutes`: int
- Example:
  ```
  Yoga|1|Yoga|Monday|06:00|20|60
  CrossFit Bootcamp|2|CrossFit|Tuesday|18:00|15|45
  ```

## Trainers (`trainers.txt`)
- Format: `trainer_id|name|specialty|biography|certifications`
- Field Types:
  - `trainer_id`: int
  - `name`: str
  - `specialty`: str
  - `biography`: str
  - `certifications`: str (comma-separated)
- Example:
  ```
  1|Jane Doe|Yoga|Experienced Yoga instructor.|Yoga Certification, CPR
  2|John Smith|CrossFit|Certified CrossFit Coach.|CrossFit Level 2
  ```

## Workouts (`workouts.txt`)
- Format: `workout_id|member_name|workout_type|workout_date|duration_minutes|calories_burned|notes`
- Field Types:
  - `workout_id`: int
  - `member_name`: str
  - `workout_type`: str
  - `workout_date`: date (YYYY-MM-DD)
  - `duration_minutes`: int
  - `calories_burned`: int
  - `notes`: str
- Example:
  ```
  1|John Smith|Strength|2025-01-16|60|420|Upper body training
  2|Jane Doe|Class|2025-01-17|50|380|CrossFit session
  ```

---

This schema document ensures consistent parsing and formatting of text data files used in backend storage.