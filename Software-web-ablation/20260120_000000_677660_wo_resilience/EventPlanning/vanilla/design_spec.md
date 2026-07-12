# EventPlanning Web Application Design Specification

---

## Section 1: Flask Routes Specification

| Route Path                | Function Name          | HTTP Methods | Template File          | Context Variables                                                                                                                                                                    |
|---------------------------|------------------------|--------------|------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `/`                       | `root_redirect`         | GET          | N/A                    | None. Redirects to `/dashboard`                                                                                                                                                      |
| `/dashboard`              | `dashboard`             | GET          | `dashboard.html`       | **featured_events**: List[Dict]: Each dict with keys: `event_id` (int), `event_name` (str), `category` (str), `date` (str, YYYY-MM-DD), `time` (str, HH:MM), `location` (str)           |
|                           |                        |              |                        | Used to show featured event recommendations on dashboard.                                                                                                                           |
| `/events`                 | `events_listing`        | GET          | `events.html`          | **events**: List[Dict]: Each dict with keys: `event_id` (int), `event_name` (str), `category` (str), `date` (str), `time` (str), `location` (str), `description` (str)                 |
|                           |                        |              |                        | Used to display all events; supports search and filter on frontend.                                                                                                                 |
| `/events/<int:event_id>`  | `event_details`         | GET          | `event_details.html`   | **event**: Dict with keys: `event_id` (int), `event_name` (str), `category` (str), `date` (str), `time` (str), `location` (str), `description` (str), `venue_id` (int), `capacity` (int) |
| `/book_ticket`            | `book_ticket`           | GET, POST   | `ticket_booking.html`  | GET: `events_list`: List[Dict] (each dict with `event_id`, `event_name`) for dropdown selection<br>POST: On success, re-render with `booking_confirmation` dict with booking summary   |
| `/participants`           | `participants_management`| GET          | `participants.html`    | **participants**: List[Dict] with keys: `participant_id` (int), `event_id` (int), `name` (str), `email` (str), `booking_id` (int), `status` (str), `registration_date` (str)             |
| `/participants/add`       | `add_participant`       | POST         | N/A                    | Accepts participant data from form submission; returns JSON or redirects depending on frontend implementation                                                                      |
| `/venues`                 | `venues_info`           | GET          | `venues.html`          | **venues**: List[Dict] with keys: `venue_id` (int), `venue_name` (str), `location` (str), `capacity` (int), `amenities` (str), `contact` (str)                                         |
| `/venues/<int:venue_id>`  | `venue_details`         | GET          | `venue_details.html` * | Not specified in requirement but assumed similar to events; omitted due to no extra page requirement                                                                               |
| `/schedules`              | `event_schedules`       | GET          | `schedules.html`       | **schedules**: List[Dict] with keys: `schedule_id` (int), `event_id` (int), `session_title` (str), `session_time` (str), `duration_minutes` (int), `speaker` (str), `venue_id` (int)    |
| `/bookings`               | `bookings_summary`      | GET          | `bookings.html`        | **bookings**: List[Dict] with keys: `booking_id` (int), `event_id` (int), `customer_name` (str), `booking_date` (str), `ticket_count` (int), `ticket_type` (str), `total_amount` (float or str), `status` (str) |
| `/bookings/cancel/<int:booking_id>` | `cancel_booking` | POST         | N/A                    | Performs booking cancellation; redirects or returns status after cancellation                                                                                                       |


*Note*: `/venues/<int:venue_id>` is not explicitly required according to the requirements document and thus omitted to avoid assumptions.

---

## Section 2: HTML Template Specifications

---
### 1. Dashboard Page
- **Template file path:** `templates/dashboard.html`
- **Page title:** `Event Planning Dashboard` (set in `<title>` and `<h1>`)
- **Element IDs:**
  - `dashboard-page` (Div) - Main page container
  - `featured-events` (Div) - Container for featured event recommendations
  - `browse-events-button` (Button) - Navigate to `/events`
  - `view-tickets-button` (Button) - Navigate to `/bookings`
  - `venues-button` (Button) - Navigate to `/venues`
- **Context variables:**
  - `featured_events`: List[Dict] with keys `event_id`, `event_name`, `category`, `date`, `time`, `location`.
- **Navigation Buttons:**
  - `browse-events-button` triggers `url_for('events_listing')`
  - `view-tickets-button` triggers `url_for('bookings_summary')`
  - `venues-button` triggers `url_for('venues_info')`

---
### 2. Events Listing Page
- **Template file path:** `templates/events.html`
- **Page title:** `Events Catalog` (set in `<title>` and `<h1>`)
- **Element IDs:**
  - `events-page` (Div) - Container
  - `event-search-input` (Input) - Search field for events by name, location, date
  - `event-category-filter` (Dropdown) - Categories: Conference, Concert, Sports, Workshop, Social
  - `events-grid` (Div) - Grid that lists event cards
  - Dynamic: `view-event-button-{{ event.event_id }}` (Button) on each event card to view details
- **Context variables:**
  - `events`: List[Dict], each dict includes keys: `event_id`, `event_name`, `category`, `date`, `time`, `location`, `description`
- **Navigation Buttons:**
  - Each event card's `view-event-button-{{ event.event_id }}` uses `url_for('event_details', event_id=event.event_id)`

---
### 3. Event Details Page
- **Template file path:** `templates/event_details.html`
- **Page title:** `Event Details`
- **Element IDs:**
  - `event-details-page` (Div) - Container
  - `event-title` (H1) - Displays `event.event_name`
  - `event-date` (Div) - Displays formatted `event.date` and `event.time`
  - `event-location` (Div) - Displays `event.location`
  - `event-description` (Div) - Displays `event.description`
  - `book-ticket-button` (Button) - Navigates to `/book_ticket` preselecting this event
- **Context variables:**
  - `event`: Dict with keys: `event_id`, `event_name`, `category`, `date`, `time`, `location`, `description`, `venue_id`, `capacity`
- **Navigation Buttons:**
  - `book-ticket-button` triggers `url_for('book_ticket')` with selected `event_id` as GET param if implemented

---
### 4. Ticket Booking Page
- **Template file path:** `templates/ticket_booking.html`
- **Page title:** `Book Your Tickets`
- **Element IDs:**
  - `ticket-booking-page` (Div) - Container
  - `select-event-dropdown` (Dropdown) - Options generated from `events_list`; each option value is `event_id`
  - `ticket-quantity-input` (Input, number) - Input for number of tickets
  - `ticket-type-select` (Dropdown) - Options: General, VIP, Early Bird
  - `book-now-button` (Button) - Submit booking form
  - `booking-confirmation` (Div) - Displays booking confirmation details after booking
- **Context variables:**
  - GET: `events_list`: List[Dict] with `event_id`, `event_name`
  - POST: `booking_confirmation`: Dict with summary fields such as `booking_id`, `event_name`, `ticket_count`, `ticket_type`, `total_amount`, `status`
- **Navigation Buttons:**
  - None explicitly defined, assumed form submission posts to `/book_ticket`

---
### 5. Participants Management Page
- **Template file path:** `templates/participants.html`
- **Page title:** `Participants Management`
- **Element IDs:**
  - `participants-page` (Div) - Container
  - `participants-table` (Table) - Displays participant rows with fields: name, email, event, status
  - `add-participant-button` (Button) - Opens add participant form
  - `search-participant-input` (Input) - Search participants by name or email
  - `participant-status-filter` (Dropdown) - Filter by status: Registered, Confirmed, Attended
- **Context variables:**
  - `participants`: List[Dict] keys: `participant_id`, `event_id`, `name`, `email`, `booking_id`, `status`, `registration_date`
- **Navigation Buttons:**
  - None specified

---
### 6. Venue Information Page
- **Template file path:** `templates/venues.html`
- **Page title:** `Venues`
- **Element IDs:**
  - `venues-page` (Div) - Container
  - `venues-grid` (Div) - Grid of venue cards
  - `venue-search-input` (Input) - Search by name or location
  - `venue-capacity-filter` (Dropdown) - Filter by capacity: Small, Medium, Large
  - Dynamic: `view-venue-details-{{ venue.venue_id }}` (Button) per venue card
- **Context variables:**
  - `venues`: List[Dict] with keys: `venue_id`, `venue_name`, `location`, `capacity`, `amenities`, `contact`
- **Navigation Buttons:**
  - Each venue card's button `view-venue-details-{{ venue.venue_id }}` should link to venue details if page exists (not required here)

---
### 7. Event Schedules Page
- **Template file path:** `templates/schedules.html`
- **Page title:** `Event Schedules`
- **Element IDs:**
  - `schedules-page` (Div) - Container
  - `schedules-timeline` (Div) - Timeline view listing schedules
  - `schedule-filter-date` (Input, date) - Filter schedules by date
  - `schedule-filter-event` (Dropdown) - Filter by event
  - `export-schedule-button` (Button) - Export schedule data
- **Context variables:**
  - `schedules`: List[Dict] with keys: `schedule_id`, `event_id`, `session_title`, `session_time`, `duration_minutes`, `speaker`, `venue_id`
- **Navigation Buttons:**
  - None specifically defined

---
### 8. Bookings Summary Page
- **Template file path:** `templates/bookings.html`
- **Page title:** `My Bookings`
- **Element IDs:**
  - `bookings-page` (Div) - Container
  - `bookings-table` (Table) - Displays bookings with event, date, ticket count, status columns
  - `booking-search-input` (Input) - Search by event name or booking ID
  - Dynamic: `cancel-booking-button-{{ booking.booking_id }}` (Button) per booking row
  - `back-to-dashboard` (Button) - Navigate back to dashboard
- **Context variables:**
  - `bookings`: List[Dict] keys: `booking_id`, `event_id`, `customer_name`, `booking_date`, `ticket_count`, `ticket_type`, `total_amount`, `status`
- **Navigation Buttons:**
  - `back-to-dashboard` triggers `url_for('dashboard')`

---

## Section 3: Data File Schemas

---
### 1. Events Data
- **File path:** `data/events.txt`
- **Field order:**
  - `event_id` (int)
  - `event_name` (str)
  - `category` (str) - One of Conference, Concert, Sports, Workshop, Social
  - `date` (str) - Format YYYY-MM-DD
  - `time` (str) - Format HH:MM
  - `location` (str)
  - `description` (str)
  - `venue_id` (int)
  - `capacity` (int)
- **Description:** Stores all event information including scheduling and venue association.
- **Examples:**
  ```
  1|Tech Conference 2025|Conference|2025-03-15|09:00|Convention Center, San Francisco|Annual technology conference discussing latest innovations|1|500
  2|Summer Music Festival|Concert|2025-06-20|18:00|Central Park, New York|Three-day music festival with international artists|2|5000
  3|Marathon Championship|Sports|2025-04-10|07:00|Downtown Loop, Chicago|Annual city marathon event for all skill levels|3|1000
  ```

---
### 2. Venues Data
- **File path:** `data/venues.txt`
- **Field order:**
  - `venue_id` (int)
  - `venue_name` (str)
  - `location` (str)
  - `capacity` (int)
  - `amenities` (str) - Comma separated list
  - `contact` (str)
- **Description:** Stores venue details including capacity and amenities.
- **Examples:**
  ```
  1|Convention Center|San Francisco, CA|500|WiFi, Parking, Catering|contact@convention.com
  2|Central Park|New York, NY|5000|Outdoor Space, Restrooms, Food Vendors|info@centralparkevents.org
  3|Downtown Loop|Chicago, IL|1000|Paved Surface, Water Stations, Medical Support|events@downtown.com
  ```

---
### 3. Tickets Data
- **File path:** `data/tickets.txt`
- **Field order:**
  - `ticket_id` (int)
  - `event_id` (int)
  - `ticket_type` (str) - E.g., General, VIP, Early Bird
  - `price` (float)
  - `available_count` (int)
  - `sold_count` (int)
- **Description:** Ticket types and availability per event.
- **Examples:**
  ```
  1|1|General|49.99|500|150
  2|1|VIP|99.99|100|45
  3|2|Early Bird|39.99|1000|750
  ```

---
### 4. Bookings Data
- **File path:** `data/bookings.txt`
- **Field order:**
  - `booking_id` (int)
  - `event_id` (int)
  - `customer_name` (str)
  - `booking_date` (str) - Format YYYY-MM-DD
  - `ticket_count` (int)
  - `ticket_type` (str)
  - `total_amount` (float)
  - `status` (str) - E.g., Confirmed, Pending, Cancelled
- **Description:** Stores all ticket bookings and statuses.
- **Examples:**
  ```
  1|1|Alice Johnson|2025-02-01|2|General|99.98|Confirmed
  2|2|Bob Williams|2025-02-05|4|Early Bird|159.96|Confirmed
  3|1|Carol Davis|2025-02-10|1|VIP|99.99|Pending
  ```

---
### 5. Participants Data
- **File path:** `data/participants.txt`
- **Field order:**
  - `participant_id` (int)
  - `event_id` (int)
  - `name` (str)
  - `email` (str)
  - `booking_id` (int)
  - `status` (str) - Values include Registered, Confirmed, Attended
  - `registration_date` (str) - Format YYYY-MM-DD
- **Description:** Stores participants linked to bookings and events with status.
- **Examples:**
  ```
  1|1|Alice Johnson|alice@email.com|1|Confirmed|2025-02-01
  2|1|Michael Johnson|michael@email.com|1|Confirmed|2025-02-01
  3|2|Bob Williams|bob@email.com|2|Attended|2025-02-05
  ```

---
### 6. Schedules Data
- **File path:** `data/schedules.txt`
- **Field order:**
  - `schedule_id` (int)
  - `event_id` (int)
  - `session_title` (str)
  - `session_time` (str) - Format YYYY-MM-DD HH:MM
  - `duration_minutes` (int)
  - `speaker` (str)
  - `venue_id` (int)
- **Description:** Stores detailed schedule info including sessions and speakers.
- **Examples:**
  ```
  1|1|Opening Keynote|2025-03-15 09:00|60|John Smith|1
  2|1|Panel Discussion|2025-03-15 10:30|90|Expert Panel|1
  3|2|Headliner Performance|2025-06-20 20:00|120|International Artist|2
  ```

---

# End of Design Specification
