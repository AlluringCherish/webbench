# EventPlanning Web Application Design Specification

---

## Section 1: Flask Routes Specification

| Route Path                | Function Name          | HTTP Methods | Template File          | Context Variables                                                                                                                                                                    |
|---------------------------|------------------------|--------------|------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `/`                       | `root_redirect`         | GET          | N/A (redirect)          | N/A                                                                                                                                                                                 |
| `/dashboard`              | `dashboard`             | GET          | `dashboard.html`        | `featured_events` (List[dict]): List of featured events with keys: `event_id`(int), `event_name`(str), `date`(str), `location`(str), `category`(str)                                                                 |
| `/events`                 | `list_events`           | GET          | `events.html`           | `events` (List[dict]): List of all event dicts with keys: `event_id`(int), `event_name`(str), `category`(str), `date`(str), `time`(str), `location`(str), `description`(str), `venue_id`(int), `capacity`(int)
`categories` (List[str]): Fixed list ["Conference", "Concert", "Sports", "Workshop", "Social"]                                           |
| `/event/<int:event_id>`   | `event_details`         | GET          | `event_details.html`    | `event`(dict): Single event with keys: `event_id`(int), `event_name`(str), `category`(str), `date`(str), `time`(str), `location`(str), `description`(str), `venue_id`(int), `capacity`(int)                                                     |
| `/book_ticket`            | `book_ticket_page`      | GET          | `ticket_booking.html`   | `events` (List[dict]): List of all events (same structure as above)                                                                                                               |
| `/book_ticket`            | `submit_ticket_booking` | POST         | `ticket_booking.html`   | `booking_confirmation` (dict, optional): Dict containing booking confirmation details with keys: `booking_id`(int), `event_name`(str), `ticket_count`(int), `ticket_type`(str), `total_amount`(float), `status`(str) (if booking success) |
| `/participants`           | `participants_management`| GET         | `participants.html`     | `participants` (List[dict]): List of participants with keys: `participant_id`(int), `event_id`(int), `name`(str), `email`(str), `booking_id`(int), `status`(str), `registration_date`(str)
`statuses` (List[str]): Fixed list ["Registered", "Confirmed", "Attended"]                                                      |
| `/add_participant`        | `add_participant`       | POST         | Redirect or render `participants.html` | Typically returns redirect or updated page; no specified template or context variables                                                                                      |
| `/venues`                 | `venues_page`           | GET          | `venues.html`           | `venues` (List[dict]): List of venue dicts with keys: `venue_id`(int), `venue_name`(str), `location`(str), `capacity`(int), `amenities`(str), `contact`(str)                                                                              |
| `/event_schedules`        | `event_schedules`       | GET          | `schedules.html`        | `schedules` (List[dict]): List of schedule dicts with keys: `schedule_id`(int), `event_id`(int), `session_title`(str), `session_time`(str), `duration_minutes`(int), `speaker`(str), `venue_id`(int)
`events` (List[dict]): List of all events (for filter dropdown)                                                |
| `/bookings`               | `bookings_summary`      | GET          | `bookings.html`         | `bookings` (List[dict]): List of bookings with keys: `booking_id`(int), `event_id`(int), `customer_name`(str), `booking_date`(str), `ticket_count`(int), `ticket_type`(str), `total_amount`(float), `status`(str)
`events_map` (Dict[int, str]): Mapping from event_id to event_name (for display in table)                                                |
| `/cancel_booking/<int:booking_id>` | `cancel_booking`      | POST         | Redirect (to `/bookings`) | N/A                                                                                                                                                                              |


---

## Section 2: HTML Template Specifications

### 1. Dashboard Page
- Template File Path: `templates/dashboard.html`
- Page Title: `Event Planning Dashboard`
- Elements with IDs:
  - `dashboard-page` (Div): Container for the dashboard page
  - `featured-events` (Div): Display of featured event recommendations
  - `browse-events-button` (Button): Button to navigate to Events Listing page
  - `view-tickets-button` (Button): Button to navigate to Bookings Summary page
  - `venues-button` (Button): Button to navigate to Venues Information page
- Context Variables:
  - `featured_events`: List of event dicts with fields `event_id`, `event_name`, `date`, `location`, and `category`
- Navigation Buttons:
  - `browse-events-button`: Navigates to `url_for('list_events')`
  - `view-tickets-button`: Navigates to `url_for('bookings_summary')`
  - `venues-button`: Navigates to `url_for('venues_page')`

### 2. Events Listing Page
- Template File Path: `templates/events.html`
- Page Title: `Events Catalog`
- Elements with IDs:
  - `events-page` (Div): Container for events listing page
  - `event-search-input` (Input): Search field
  - `event-category-filter` (Dropdown): Filter dropdown with fixed categories
  - `events-grid` (Div): Grid displaying event cards
  - `view-event-button-{event_id}` (Button): Button to view detail for each event, dynamic ID pattern
- Context Variables:
  - `events`: List of event dicts with all event fields
  - `categories`: List of category strings
- Navigation Buttons:
  None specified
- Dynamic IDs Handling:
  - Use a Jinja2 for loop over `events`:
    ```jinja2
    {% for event in events %}
      <button id="view-event-button-{{ event.event_id }}">View Event</button>
    {% endfor %}
    ```

### 3. Event Details Page
- Template File Path: `templates/event_details.html`
- Page Title: `Event Details`
- Elements with IDs:
  - `event-details-page` (Div): Container
  - `event-title` (H1): Event title
  - `event-date` (Div): Event date and time
  - `event-location` (Div): Event location
  - `event-description` (Div): Event description
  - `book-ticket-button` (Button): Button to book ticket for this event
- Context Variables:
  - `event`: Dict with full event details
- Navigation Buttons:
  - `book-ticket-button` should navigate (likely via form or link) to `url_for('book_ticket_page')` passing the selected event

### 4. Ticket Booking Page
- Template File Path: `templates/ticket_booking.html`
- Page Title: `Book Your Tickets`
- Elements with IDs:
  - `ticket-booking-page` (Div): Container
  - `select-event-dropdown` (Dropdown): Select event to book tickets
  - `ticket-quantity-input` (Input number): Number of tickets
  - `ticket-type-select` (Dropdown): Ticket type selection (General, VIP, Early Bird)
  - `book-now-button` (Button): Submit booking
  - `booking-confirmation` (Div): Display booking confirmation details (conditionally rendered)
- Context Variables:
  - `events`: List of event dicts for dropdown
  - Optional `booking_confirmation`: Dict with keys `booking_id`, `event_name`, `ticket_count`, `ticket_type`, `total_amount`, `status`
- Navigation Buttons:
  None specified
- Dynamic IDs:
  None

### 5. Participants Management Page
- Template File Path: `templates/participants.html`
- Page Title: `Participants Management`
- Elements with IDs:
  - `participants-page` (Div): Container
  - `participants-table` (Table): Displays participants with columns: name, email, event, status
  - `add-participant-button` (Button): Add new participant
  - `search-participant-input` (Input): Search participants
  - `participant-status-filter` (Dropdown): Filter by status
- Context Variables:
  - `participants`: List of participant dicts with fields as defined
  - `statuses`: List of status strings
- Navigation Buttons:
  None specified

### 6. Venue Information Page
- Template File Path: `templates/venues.html`
- Page Title: `Venues`
- Elements with IDs:
  - `venues-page` (Div): Container
  - `venues-grid` (Div): Grid with venue cards
  - `venue-search-input` (Input): Search field
  - `venue-capacity-filter` (Dropdown): Filter by capacity (Small, Medium, Large)
  - `view-venue-details-{venue_id}` (Button): Button to view venue details, dynamic ID pattern
- Context Variables:
  - `venues`: List of venue dicts
- Navigation Buttons:
  None specified
- Dynamic IDs Handling:
  - Use a Jinja2 for loop over `venues`:
    ```jinja2
    {% for venue in venues %}
      <button id="view-venue-details-{{ venue.venue_id }}">View Venue Details</button>
    {% endfor %}
    ```

### 7. Event Schedules Page
- Template File Path: `templates/schedules.html`
- Page Title: `Event Schedules`
- Elements with IDs:
  - `schedules-page` (Div): Container
  - `schedules-timeline` (Div): Timeline view
  - `schedule-filter-date` (Input date): Date filter
  - `schedule-filter-event` (Dropdown): Filter by event
  - `export-schedule-button` (Button): Export schedule
- Context Variables:
  - `schedules`: List of schedule dicts
  - `events`: List of event dicts (for filter dropdown)
- Navigation Buttons:
  None specified

### 8. Bookings Summary Page
- Template File Path: `templates/bookings.html`
- Page Title: `My Bookings`
- Elements with IDs:
  - `bookings-page` (Div): Container
  - `bookings-table` (Table): Booking details with event, date, ticket count, status
  - `booking-search-input` (Input): Search bookings
  - `cancel-booking-button-{booking_id}` (Button): Cancel booking button, dynamic ID pattern
  - `back-to-dashboard` (Button): Button to navigate back to dashboard
- Context Variables:
  - `bookings`: List of booking dicts
  - `events_map`: Dict mapping `event_id` to `event_name` for display
- Navigation Buttons:
  - `back-to-dashboard` navigates to `url_for('dashboard')`
- Dynamic IDs:
  - For each booking in `bookings`:
    ```jinja2
    <button id="cancel-booking-button-{{ booking.booking_id }}">Cancel Booking</button>
    ```

---

## Section 3: Data File Schemas

### 1. Events Data
- File Path: `data/events.txt`
- Field Order (pipe-delimited):
  `event_id|event_name|category|date|time|location|description|venue_id|capacity`
- Description: Stores event details including category, schedule, location and venue association
- Example Data Rows:
  ```
  1|Tech Conference 2025|Conference|2025-03-15|09:00|Convention Center, San Francisco|Annual technology conference discussing latest innovations|1|500
  2|Summer Music Festival|Concert|2025-06-20|18:00|Central Park, New York|Three-day music festival with international artists|2|5000
  3|Marathon Championship|Sports|2025-04-10|07:00|Downtown Loop, Chicago|Annual city marathon event for all skill levels|3|1000
  ```

### 2. Venues Data
- File Path: `data/venues.txt`
- Field Order:
  `venue_id|venue_name|location|capacity|amenities|contact`
- Description: Stores venue details including capacity, amenities and contact info
- Example Data Rows:
  ```
  1|Convention Center|San Francisco, CA|500|WiFi, Parking, Catering|contact@convention.com
  2|Central Park|New York, NY|5000|Outdoor Space, Restrooms, Food Vendors|info@centralparkevents.org
  3|Downtown Loop|Chicago, IL|1000|Paved Surface, Water Stations, Medical Support|events@downtown.com
  ```

### 3. Tickets Data
- File Path: `data/tickets.txt`
- Field Order:
  `ticket_id|event_id|ticket_type|price|available_count|sold_count`
- Description: Stores ticket types, pricing and availability per event
- Example Data Rows:
  ```
  1|1|General|49.99|500|150
  2|1|VIP|99.99|100|45
  3|2|Early Bird|39.99|1000|750
  ```

### 4. Bookings Data
- File Path: `data/bookings.txt`
- Field Order:
  `booking_id|event_id|customer_name|booking_date|ticket_count|ticket_type|total_amount|status`
- Description: Stores booking transactions including status
- Example Data Rows:
  ```
  1|1|Alice Johnson|2025-02-01|2|General|99.98|Confirmed
  2|2|Bob Williams|2025-02-05|4|Early Bird|159.96|Confirmed
  3|1|Carol Davis|2025-02-10|1|VIP|99.99|Pending
  ```

### 5. Participants Data
- File Path: `data/participants.txt`
- Field Order:
  `participant_id|event_id|name|email|booking_id|status|registration_date`
- Description: Stores event participants linked to bookings
- Example Data Rows:
  ```
  1|1|Alice Johnson|alice@email.com|1|Confirmed|2025-02-01
  2|1|Michael Johnson|michael@email.com|1|Confirmed|2025-02-01
  3|2|Bob Williams|bob@email.com|2|Attended|2025-02-05
  ```

### 6. Schedules Data
- File Path: `data/schedules.txt`
- Field Order:
  `schedule_id|event_id|session_title|session_time|duration_minutes|speaker|venue_id`
- Description: Stores event session schedules with timings and speakers
- Example Data Rows:
  ```
  1|1|Opening Keynote|2025-03-15 09:00|60|John Smith|1
  2|1|Panel Discussion|2025-03-15 10:30|90|Expert Panel|1
  3|2|Headliner Performance|2025-06-20 20:00|120|International Artist|2
  ```

---

***End of Design Specification Document***
