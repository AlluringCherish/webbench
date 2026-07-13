# Backend Design Specification for EventPlanning Application

---

## Section 1: Flask Routes Specification

### 1. Dashboard Page
- **Route URL:** `/`
- **HTTP Method:** GET
- **Route function:** `dashboard()`
- **Template Context Variables:**
  - `featured_events`: list of featured event dictionaries (event_id, event_name, date, location, description)
  - `featured_venues`: list of featured venue dictionaries (venue_id, venue_name, location, capacity, amenities)

- **Data Access:** Read from `data/events.txt` and `data/venues.txt` for featured items.

---

### 2. Events Listing Page
- **Route URL:** `/events`
- **HTTP Method:** GET
- **Route function:** `events_listing()`
- **Template Context Variables:**
  - `events`: list of all event dictionaries (event_id, event_name, category, date, time, location, description, venue_id, capacity)
  - `categories`: list of categories ["Conference", "Concert", "Sports", "Workshop", "Social"]
  - **Optional Query Parameters:** `search`, `category` for filtering results

- **Data Access:** Read from `data/events.txt`.

---

### 3. Event Details Page
- **Route URL:** `/events/<int:event_id>`
- **HTTP Method:** GET
- **Route function:** `event_details(event_id)`
- **Template Context Variables:**
  - `event`: event dictionary matching `event_id` with all event fields
  - `venue`: venue dictionary linked by `venue_id`

- **Data Access:** Read `data/events.txt` for event, `data/venues.txt` for venue info.

---

### 4. Ticket Booking Page
- **Route URL:** `/bookings/new`
- **HTTP Methods:** GET, POST
- **Route function:** 
  - GET: `ticket_booking_form()` returns the booking form
  - POST: `process_booking()` processes booking submission
- **Template Context Variables (GET):**
  - `events`: list of all events (event_id, event_name)
  - `ticket_types`: ["General", "VIP", "Early Bird"]
- **Data Access:**
  - Read `data/events.txt` for event list
  - Read `data/tickets.txt` for ticket type availability
- **POST processing:**
  - Validate ticket availability from `tickets.txt`
  - Write new booking entry to `data/bookings.txt` (assign next available booking_id)
  - Update `tickets.txt` sold_count accordingly

---

### 5. Participants Management Page
- **Route URL:** `/participants`
- **HTTP Method:** GET
- **Route function:** `participants_management()`
- **Template Context Variables:**
  - `participants`: list of participants with fields (participant_id, event_id, name, email, booking_id, status, registration_date)
  - `status_options`: ["Registered", "Confirmed", "Attended"]
  - **Optional Query Parameters:** `search`, `status` for filtering

- **Data Access:** Read from `data/participants.txt`.

**Note:** Could provide POST routes for adding participants but not specified.

---

### 6. Venue Information Page
- **Route URL:** `/venues`
- **HTTP Method:** GET
- **Route function:** `venues_listing()`
- **Template Context Variables:**
  - `venues`: list of venue dictionaries (venue_id, venue_name, location, capacity, amenities, contact)
  - `capacity_filters`: ["Small", "Medium", "Large"]
  - **Optional Query Parameters:** `search`, `capacity` for filtering

- **Data Access:** Read from `data/venues.txt`.

---

### 7. Event Schedules Page
- **Route URL:** `/schedules`
- **HTTP Method:** GET
- **Route function:** `schedules_page()`
- **Template Context Variables:**
  - `schedules`: list of schedule dictionaries (schedule_id, event_id, session_title, session_time, duration_minutes, speaker, venue_id)
  - `events`: list of events (event_id, event_name) for filter dropdown
  - **Optional Query Parameters:** `date`, `event_id` for filtering

- **Data Access:** Read from `data/schedules.txt` and `data/events.txt`.

---

### 8. Bookings Summary Page
- **Route URL:** `/bookings`
- **HTTP Method:** GET
- **Route function:** `bookings_summary()`
- **Template Context Variables:**
  - `bookings`: list of booking records (booking_id, event_id, customer_name, booking_date, ticket_count, ticket_type, total_amount, status)
  - `search_query`: optional search string for event name or booking id

- **Data Access:** Read from `data/bookings.txt` and `data/events.txt` for event_name references.

- **Additional Post/GET:** POST route for canceling booking by booking_id could be implemented at `/bookings/cancel/<int:booking_id>` (not detailed in requirements but implied).

---

## Section 2: Data File Schemas

The application stores data locally as pipe-delimited (`|`) text files in the `data/` directory.

---

### 1. Events Data (`events.txt`)
- **Schema:**
  ```
  event_id|event_name|category|date|time|location|description|venue_id|capacity
  ```
- **Field Definitions:**
  - `event_id`: int (unique event identifier)
  - `event_name`: string
  - `category`: string (one of [Conference, Concert, Sports, Workshop, Social])
  - `date`: string date (YYYY-MM-DD)
  - `time`: string time (HH:MM)
  - `location`: string (venue address or event location)
  - `description`: string (detailed event description)
  - `venue_id`: int (reference to venue_id in venues.txt)
  - `capacity`: int (max attendees allowed)

- **Example:**
  ```
  1|Tech Conference 2025|Conference|2025-03-15|09:00|Convention Center, San Francisco|Annual technology conference discussing latest innovations|1|500
  2|Summer Music Festival|Concert|2025-06-20|18:00|Central Park, New York|Three-day music festival with international artists|2|5000
  3|Marathon Championship|Sports|2025-04-10|07:00|Downtown Loop, Chicago|Annual city marathon event for all skill levels|3|1000
  ```
- **File Handling:**
  - Read all lines to load events.
  - Write updates on event entries (if needed).

---

### 2. Venues Data (`venues.txt`)
- **Schema:**
  ```
  venue_id|venue_name|location|capacity|amenities|contact
  ```
- **Field Definitions:**
  - `venue_id`: int (unique venue identifier)
  - `venue_name`: string
  - `location`: string (venue address)
  - `capacity`: int
  - `amenities`: string (comma-separated list of amenities)
  - `contact`: string (contact email or phone)

- **Example:**
  ```
  1|Convention Center|San Francisco, CA|500|WiFi, Parking, Catering|contact@convention.com
  2|Central Park|New York, NY|5000|Outdoor Space, Restrooms, Food Vendors|info@centralparkevents.org
  3|Downtown Loop|Chicago, IL|1000|Paved Surface, Water Stations, Medical Support|events@downtown.com
  ```
- **File Handling:**
  - Read all venues from file.
  - Write operations when venue data updates occur.

---

### 3. Tickets Data (`tickets.txt`)
- **Schema:**
  ```
  ticket_id|event_id|ticket_type|price|available_count|sold_count
  ```
- **Field Definitions:**
  - `ticket_id`: int (unique ticket type identifier)
  - `event_id`: int (references event_id from events.txt)
  - `ticket_type`: string (e.g. General, VIP, Early Bird)
  - `price`: float (ticket price)
  - `available_count`: int (initial total available)
  - `sold_count`: int (tickets sold so far)

- **Example:**
  ```
  1|1|General|49.99|500|150
  2|1|VIP|99.99|100|45
  3|2|Early Bird|39.99|1000|750
  ```
- **File Handling:**
  - Read for ticket availability during booking.
  - Update sold_count on successful booking.

---

### 4. Bookings Data (`bookings.txt`)
- **Schema:**
  ```
  booking_id|event_id|customer_name|booking_date|ticket_count|ticket_type|total_amount|status
  ```
- **Field Definitions:**
  - `booking_id`: int (unique booking identifier)
  - `event_id`: int
  - `customer_name`: string
  - `booking_date`: string date (YYYY-MM-DD)
  - `ticket_count`: int
  - `ticket_type`: string
  - `total_amount`: float
  - `status`: string (e.g. Confirmed, Pending, Cancelled)

- **Example:**
  ```
  1|1|Alice Johnson|2025-02-01|2|General|99.98|Confirmed
  2|2|Bob Williams|2025-02-05|4|Early Bird|159.96|Confirmed
  3|1|Carol Davis|2025-02-10|1|VIP|99.99|Pending
  ```
- **File Handling:**
  - Append new bookings on new ticket bookings.
  - Update booking status on cancellation.

---

### 5. Participants Data (`participants.txt`)
- **Schema:**
  ```
  participant_id|event_id|name|email|booking_id|status|registration_date
  ```
- **Field Definitions:**
  - `participant_id`: int (unique participant identifier)
  - `event_id`: int
  - `name`: string
  - `email`: string
  - `booking_id`: int (references booking_id from bookings.txt)
  - `status`: string (Registered, Confirmed, Attended)
  - `registration_date`: string date (YYYY-MM-DD)

- **Example:**
  ```
  1|1|Alice Johnson|alice@email.com|1|Confirmed|2025-02-01
  2|1|Michael Johnson|michael@email.com|1|Confirmed|2025-02-01
  3|2|Bob Williams|bob@email.com|2|Attended|2025-02-05
  ```
- **File Handling:**
  - Manage reading and filtering participant records.
  - Write on participant additions or status updates.

---

### 6. Schedules Data (`schedules.txt`)
- **Schema:**
  ```
  schedule_id|event_id|session_title|session_time|duration_minutes|speaker|venue_id
  ```
- **Field Definitions:**
  - `schedule_id`: int (unique schedule identifier)
  - `event_id`: int
  - `session_title`: string
  - `session_time`: string datetime (YYYY-MM-DD HH:MM)
  - `duration_minutes`: int
  - `speaker`: string
  - `venue_id`: int

- **Example:**
  ```
  1|1|Opening Keynote|2025-03-15 09:00|60|John Smith|1
  2|1|Panel Discussion|2025-03-15 10:30|90|Expert Panel|1
  3|2|Headliner Performance|2025-06-20 20:00|120|International Artist|2
  ```
- **File Handling:**
  - Read schedules for display and filtering.
  - Write when schedules are added or modified.

---

# End of Backend Design
