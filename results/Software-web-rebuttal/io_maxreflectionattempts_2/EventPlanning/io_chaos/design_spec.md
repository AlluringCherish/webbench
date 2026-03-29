# EventPlanning Application Design Specification

---

## Section 1: Flask Routes Specification

| Route Path                     | Function Name           | HTTP Methods | Template File               | Context Variables                                                                                                                              |
|-------------------------------|------------------------|--------------|-----------------------------|------------------------------------------------------------------------------------------------------------------------------------------------|
| /                             | root_redirect          | GET          | -                           | None (redirects to /dashboard)                                                                                                                  |
| /dashboard                    | dashboard_page         | GET          | dashboard.html              | featured_events: List[dict] with keys: event_id (int), event_name (str), date (str), location (str)
venues: List[dict] with keys: venue_id (int), venue_name (str), location (str)              |
| /events                      | events_listing_page    | GET, POST    | events.html                 | events: List[dict] with keys: event_id (int), event_name (str), category (str), date (str), location (str). POST supports filtered events list   |
| /event/<int:event_id>         | event_details_page     | GET          | event_details.html          | event: dict with keys event_id (int), event_name (str), category (str), date (str), time (str), location (str), description (str), venue_id (int), capacity (int) |
| /book_ticket                 | ticket_booking_page    | GET          | ticket_booking.html         | events: List[dict] with keys event_id (int), event_name (str)                                                                                  |
| /book_ticket                 | book_ticket_action     | POST         | ticket_booking.html         | booking_confirmation: dict with keys booking_id (int), event_name (str), ticket_count (int), ticket_type (str), total_amount (float), status (str)  |
| /participants                | participants_page      | GET, POST    | participants.html           | participants: List[dict] with keys participant_id (int), name (str), email (str), event_name (str), status (str). POST supports filtered participants  |
| /venues                     | venues_page            | GET, POST    | venues.html                 | venues: List[dict] with keys venue_id (int), venue_name (str), location (str), capacity (int), amenities (str). POST supports filtered venues       |
| /schedules                  | event_schedules_page   | GET, POST    | event_schedules.html        | schedules: List[dict] with keys schedule_id (int), event_id (int), session_title (str), session_time (str), duration_minutes (int), speaker (str), venue_id (int). POST supports filtered schedules |
| /bookings                  | bookings_summary_page  | GET          | bookings_summary.html       | bookings: List[dict] with keys booking_id (int), event_name (str), date (str), ticket_count (int), status (str)                                   |
| /cancel_booking/<int:booking_id> | cancel_booking_action | POST         | bookings_summary.html       | bookings: List[dict], updated after cancellation                                                                                               |

---

## Section 2: HTML Template Specifications

### 1. Dashboard Page
- Template file: templates/dashboard.html
- Page title: "Event Planning Dashboard"
- <h1> content: "Event Planning Dashboard"
- Element IDs:
  - dashboard-page (Div): Container for the dashboard page.
  - featured-events (Div): Display of featured event recommendations.
  - browse-events-button (Button): Navigate to /events.
  - view-tickets-button (Button): Navigate to /bookings.
  - venues-button (Button): Navigate to /venues.
- Context Variables:
  - featured_events: List[dict] with event_id, event_name, date, location
  - venues: List[dict] with venue_id, venue_name, location
- Navigation buttons:
  - browse-events-button -> `url_for('events_listing_page')`
  - view-tickets-button -> `url_for('bookings_summary_page')`
  - venues-button -> `url_for('venues_page')`

### 2. Events Listing Page
- Template file: templates/events.html
- Page title: "Events Catalog"
- <h1> content: "Events Catalog"
- Element IDs:
  - events-page (Div): Container for the events listing page.
  - event-search-input (Input): Search by event name, location, or date.
  - event-category-filter (Dropdown): Filter by category (Conference, Concert, Sports, Workshop, Social).
  - events-grid (Div): Grid showing event cards with image, title, date, and location.
  - view-event-button-{event_id} (Button): Button to view event details for each event.
- Context Variables:
  - events: List[dict] with event_id, event_name, category, date, location.
- Navigation buttons: None explicit.
- Dynamic element IDs:
  - Use Jinja2 syntax: `id="view-event-button-{{ event.event_id }}`

### 3. Event Details Page
- Template file: templates/event_details.html
- Page title: "Event Details"
- <h1> content: {{ event.event_name }}
- Element IDs:
  - event-details-page (Div): Container for the event details page.
  - event-title (H1): Displays event title.
  - event-date (Div): Event date and time.
  - event-location (Div): Event location.
  - event-description (Div): Event description.
  - book-ticket-button (Button): Button to book ticket for the event.
- Context Variables:
  - event: dict with event_id, event_name, category, date, time, location, description, venue_id, capacity.
- Navigation buttons:
  - book-ticket-button -> `url_for('ticket_booking_page')` with event pre-selection if supported.

### 4. Ticket Booking Page
- Template file: templates/ticket_booking.html
- Page title: "Book Your Tickets"
- <h1> content: "Book Your Tickets"
- Element IDs:
  - ticket-booking-page (Div): Container for booking page.
  - select-event-dropdown (Dropdown): Select event to book tickets.
  - ticket-quantity-input (Input number): Number of tickets.
  - ticket-type-select (Dropdown): Ticket type - General, VIP, Early Bird.
  - book-now-button (Button): Button to proceed booking.
  - booking-confirmation (Div): Shows booking confirmation.
- Context Variables:
  - events: List[dict] with event_id, event_name.
  - booking_confirmation: dict with booking_id, event_name, ticket_count, ticket_type, total_amount, status (optional, after booking).
- Navigation buttons: None explicit.

### 5. Participants Management Page
- Template file: templates/participants.html
- Page title: "Participants Management"
- <h1> content: "Participants Management"
- Element IDs:
  - participants-page (Div): Container.
  - participants-table (Table): Participant name, email, event, status.
  - add-participant-button (Button): Button to add participant.
  - search-participant-input (Input): Search participants by name/email.
  - participant-status-filter (Dropdown): Filter by status (Registered, Confirmed, Attended).
- Context Variables:
  - participants: List[dict] with participant_id, name, email, event_name, status.
- Navigation buttons:
  - add-participant-button possibly linked to add participant form or modal (no route specified).

### 6. Venue Information Page
- Template file: templates/venues.html
- Page title: "Venues"
- <h1> content: "Venues"
- Element IDs:
  - venues-page (Div): Container.
  - venues-grid (Div): Venue cards grid.
  - venue-search-input (Input): Search venues by name/location.
  - venue-capacity-filter (Dropdown): Filter by capacity (Small, Medium, Large).
  - view-venue-details-{venue_id} (Button): View details per venue.
- Context Variables:
  - venues: List[dict] with venue_id, venue_name, location, capacity, amenities.
- Navigation buttons: None explicit.
- Dynamic element IDs:
  - Jinja2 syntax: `id="view-venue-details-{{ venue.venue_id }}"`

### 7. Event Schedules Page
- Template file: templates/event_schedules.html
- Page title: "Event Schedules"
- <h1> content: "Event Schedules"
- Element IDs:
  - schedules-page (Div): Container.
  - schedules-timeline (Div): Timeline of upcoming events and sessions.
  - schedule-filter-date (Input date): Filter schedules by date.
  - schedule-filter-event (Dropdown): Filter schedules by event.
  - export-schedule-button (Button): Export schedule data.
- Context Variables:
  - schedules: List[dict] with schedule_id, event_id, session_title, session_time, duration_minutes, speaker, venue_id.
- Navigation buttons: None explicit.

### 8. Bookings Summary Page
- Template file: templates/bookings_summary.html
- Page title: "My Bookings"
- <h1> content: "My Bookings"
- Element IDs:
  - bookings-page (Div): Container.
  - bookings-table (Table): Displays bookings with event, date, ticket count, status.
  - booking-search-input (Input): Search bookings.
  - cancel-booking-button-{booking_id} (Button): Cancel booking per booking.
  - back-to-dashboard (Button): Navigate to dashboard.
- Context Variables:
  - bookings: List[dict] with booking_id, event_name, date, ticket_count, status.
- Navigation buttons:
  - back-to-dashboard -> `url_for('dashboard_page')`
- Dynamic element IDs:
  - Jinja2 syntax: `id="cancel-booking-button-{{ booking.booking_id }}"`

---

## Section 3: Data File Schemas

### 1. Events Data
- File path: data/events.txt
- Pipe-delimited fields:
  1. event_id (int)
  2. event_name (str)
  3. category (str)
  4. date (str, YYYY-MM-DD)
  5. time (str, HH:MM)
  6. location (str)
  7. description (str)
  8. venue_id (int)
  9. capacity (int)
- Description: Stores all event details including scheduling and venue association.
- Example rows (no header):
  ```
  1|Tech Conference 2025|Conference|2025-03-15|09:00|Convention Center, San Francisco|Annual technology conference discussing latest innovations|1|500
  2|Summer Music Festival|Concert|2025-06-20|18:00|Central Park, New York|Three-day music festival with international artists|2|5000
  3|Marathon Championship|Sports|2025-04-10|07:00|Downtown Loop, Chicago|Annual city marathon event for all skill levels|3|1000
  ```

### 2. Venues Data
- File path: data/venues.txt
- Pipe-delimited fields:
  1. venue_id (int)
  2. venue_name (str)
  3. location (str)
  4. capacity (int)
  5. amenities (str) - comma separated list
  6. contact (str)
- Description: Stores venue information for events.
- Example rows (no header):
  ```
  1|Convention Center|San Francisco, CA|500|WiFi, Parking, Catering|contact@convention.com
  2|Central Park|New York, NY|5000|Outdoor Space, Restrooms, Food Vendors|info@centralparkevents.org
  3|Downtown Loop|Chicago, IL|1000|Paved Surface, Water Stations, Medical Support|events@downtown.com
  ```

### 3. Tickets Data
- File path: data/tickets.txt
- Pipe-delimited fields:
  1. ticket_id (int)
  2. event_id (int)
  3. ticket_type (str)
  4. price (float)
  5. available_count (int)
  6. sold_count (int)
- Description: Stores tickets availability and pricing per event.
- Example rows (no header):
  ```
  1|1|General|49.99|500|150
  2|1|VIP|99.99|100|45
  3|2|Early Bird|39.99|1000|750
  ```

### 4. Bookings Data
- File path: data/bookings.txt
- Pipe-delimited fields:
  1. booking_id (int)
  2. event_id (int)
  3. customer_name (str)
  4. booking_date (str, YYYY-MM-DD)
  5. ticket_count (int)
  6. ticket_type (str)
  7. total_amount (float)
  8. status (str)
- Description: Stores user bookings and status.
- Example rows (no header):
  ```
  1|1|Alice Johnson|2025-02-01|2|General|99.98|Confirmed
  2|2|Bob Williams|2025-02-05|4|Early Bird|159.96|Confirmed
  3|1|Carol Davis|2025-02-10|1|VIP|99.99|Pending
  ```

### 5. Participants Data
- File path: data/participants.txt
- Pipe-delimited fields:
  1. participant_id (int)
  2. event_id (int)
  3. name (str)
  4. email (str)
  5. booking_id (int)
  6. status (str)
  7. registration_date (str, YYYY-MM-DD)
- Description: Stores participants for all events.
- Example rows (no header):
  ```
  1|1|Alice Johnson|alice@email.com|1|Confirmed|2025-02-01
  2|1|Michael Johnson|michael@email.com|1|Confirmed|2025-02-01
  3|2|Bob Williams|bob@email.com|2|Attended|2025-02-05
  ```

### 6. Schedules Data
- File path: data/schedules.txt
- Pipe-delimited fields:
  1. schedule_id (int)
  2. event_id (int)
  3. session_title (str)
  4. session_time (str, YYYY-MM-DD HH:MM)
  5. duration_minutes (int)
  6. speaker (str)
  7. venue_id (int)
- Description: Stores event schedules.
- Example rows (no header):
  ```
  1|1|Opening Keynote|2025-03-15 09:00|60|John Smith|1
  2|1|Panel Discussion|2025-03-15 10:30|90|Expert Panel|1
  3|2|Headliner Performance|2025-06-20 20:00|120|International Artist|2
  ```

---
