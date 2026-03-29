# EventPlanning Application Design Specification

---

## Section 1: Flask Routes Specification

| Route Path                   | Function Name           | HTTP Methods | Template File               | Context Variables                                                                                                                                               |
|------------------------------|-------------------------|--------------|-----------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| /                            | root_redirect            | GET          | -                           | None. Redirects to `/dashboard` route.                                                                                                                         |
| /dashboard                   | dashboard_page          | GET          | dashboard.html              | featured_events: List[Dict] with keys: event_id (int), event_name (str), date (str), location (str) - featured event recommendations.                          |
| /events                     | events_listing          | GET          | events.html                 | events: List[Dict] with keys: event_id (int), event_name (str), category (str), date (str), time (str), location (str).
category_options: List[str] = [Conference, Concert, Sports, Workshop, Social].                                       |
| /events/filter               | filter_events           | POST         | events.html                 | events: List[Dict] filtered by search/filter criteria as above.
category_options: List[str] same as above.
(search and filter actions submit via POST.)                                              |
| /events/<int:event_id>       | event_details           | GET          | event_details.html          | event: Dict with keys: event_id (int), event_name (str), category (str), date (str), time (str), location (str), description (str), venue_id (int), capacity (int). |
| /book_ticket                 | book_ticket             | GET, POST    | book_ticket.html            | GET: events: List[Dict] with keys event_id (int), event_name (str) for dropdown.
POST: booking_confirmation: Dict with booking details or error message.                                      |
| /participants                | participants_management | GET          | participants.html           | participants: List[Dict] with keys participant_id (int), event_id (int), name (str), email (str), booking_id (int), status (str), registration_date (str).
status_options: List[str] = [Registered, Confirmed, Attended].                                         |
| /participants/filter         | filter_participants     | POST         | participants.html           | participants: List[Dict] filtered by search or status filter.
status_options: List[str] as above.                                                                        |
| /participants/add            | add_participant         | POST         | participants.html (redirect after post) | N/A. Participant added and redirects back to /participants page.                                                                                          |
| /venues                     | venues_page             | GET          | venues.html                 | venues: List[Dict] with keys venue_id (int), venue_name (str), location (str), capacity (int), amenities (str).
capacity_options: List[str] = [Small, Medium, Large].                                        |
| /venues/filter               | filter_venues           | POST         | venues.html                 | venues: List[Dict] filtered by search or capacity filter.
capacity_options: List[str] as above.                                                                                   |
| /venues/<int:venue_id>       | venue_details           | GET          | venue_details.html (not defined in pages, so omitted) | Not defined in requirements, no venue detail page implemented.                                                                                           |
| /schedules                  | event_schedules         | GET          | schedules.html              | schedules: List[Dict] with keys schedule_id (int), event_id (int), session_title (str), session_time (str), duration_minutes (int), speaker (str), venue_id (int).
events: List[Dict] with event_id, event_name for filter.
                                                                                      |
| /schedules/filter            | filter_schedules        | POST         | schedules.html              | schedules: List[Dict] filtered by date and/or event.
events: List[Dict] as above.                                                                                                           |
| /bookings                   | bookings_summary        | GET          | bookings.html               | bookings: List[Dict] with keys booking_id (int), event_id (int), event_name (str), date (str), ticket_count (int), status (str), ticket_type (str).
                                                                                                  |
| /bookings/cancel/<int:booking_id> | cancel_booking          | POST         | bookings.html (redirect after cancel) | N/A. Cancels booking then redirects back to /bookings page.                                                                                             |

**Notes:**
- Root `/` redirects directly to `/dashboard`.
- Ticket booking form submission handled in `/book_ticket` with GET to show form, POST to handle booking.
- Filtering of events, participants, venues, schedules done with POST actions returning same page with filtered data.
- Booking cancellation via POST to `/bookings/cancel/<booking_id>`.
- Venue detail page was suggested in venue buttons, but not specified in page design documents, so no dedicated route provided for viewing venue details.


---

## Section 2: HTML Template Specifications

### 1. Dashboard Page
- Template file path: templates/dashboard.html
- Page title: <title>Event Planning Dashboard</title>
- Heading: <h1 id="dashboard-page">Event Planning Dashboard</h1>
- Element IDs:
  - dashboard-page (div): Container for dashboard page
  - featured-events (div): Display featured event recommendations
  - browse-events-button (button): Navigate to /events
  - view-tickets-button (button): Navigate to /bookings
  - venues-button (button): Navigate to /venues
- Context variables:
  - featured_events: list of dict with keys event_id (int), event_name (str), date (str), location (str)
- Navigation Buttons:
  - browse-events-button -> url_for('events_listing')
  - view-tickets-button -> url_for('bookings_summary')
  - venues-button -> url_for('venues_page')

### 2. Events Listing Page
- Template file path: templates/events.html
- Page title: <title>Events Catalog</title>
- Heading: <h1 id="events-page">Events Catalog</h1>
- Element IDs:
  - events-page (div): Container for events listing
  - event-search-input (input): Text input for searching events
  - event-category-filter (dropdown/select): Dropdown for category filter
  - events-grid (div): Container grid for event cards
  - view-event-button-{event_id} (button): Button on each event card to view event details
- Context variables:
  - events: list of dict with keys event_id, event_name, category, date, time, location
  - category_options: list of strings [Conference, Concert, Sports, Workshop, Social]
- Navigation Buttons:
  - Each view-event-button-{event_id} -> url_for('event_details', event_id=event_id)
- Dynamic ID:
  - view-event-button-{{ event.event_id }} inside loop over events

### 3. Event Details Page
- Template file path: templates/event_details.html
- Page title: <title>Event Details</title>
- Heading: <h1 id="event-title">{{ event.event_name }}</h1>
- Element IDs:
  - event-details-page (div): Container for event details
  - event-title (h1): Event title
  - event-date (div): Display event date and time
  - event-location (div): Display event location
  - event-description (div): Detailed event description
  - book-ticket-button (button): Navigate to /book_ticket page
- Context variables:
  - event: dict with keys event_id, event_name, category, date, time, location, description, venue_id, capacity
- Navigation Buttons:
  - book-ticket-button -> url_for('book_ticket')

### 4. Ticket Booking Page
- Template file path: templates/book_ticket.html
- Page title: <title>Book Your Tickets</title>
- Heading: <h1 id="ticket-booking-page">Book Your Tickets</h1>
- Element IDs:
  - ticket-booking-page (div): Container for ticket booking
  - select-event-dropdown (select): Dropdown to select event
  - ticket-quantity-input (input number): Input for ticket quantity
  - ticket-type-select (select): Dropdown for ticket type (General, VIP, Early Bird)
  - book-now-button (button): Submit booking form
  - booking-confirmation (div): Displays booking confirmation details or errors
- Context variables:
  - events: list of dict with event_id, event_name
  - booking_confirmation: dict or None, includes success messages or error text after POST
- Navigation Buttons:
  - None specified (assumed form submission handled at /book_ticket)

### 5. Participants Management Page
- Template file path: templates/participants.html
- Page title: <title>Participants Management</title>
- Heading: <h1 id="participants-page">Participants Management</h1>
- Element IDs:
  - participants-page (div): Container
  - participants-table (table): Table listing participants
  - add-participant-button (button): Button to add new participant (triggers form or redirect)
  - search-participant-input (input): Search input
  - participant-status-filter (dropdown): Filter by participant status
- Context variables:
  - participants: list of dict with participant_id, event_id, name, email, booking_id, status, registration_date
  - status_options: list of strings [Registered, Confirmed, Attended]
- Navigation Buttons:
  - add-participant-button -> form post to /participants/add or redirect

### 6. Venue Information Page
- Template file path: templates/venues.html
- Page title: <title>Venues</title>
- Heading: <h1 id="venues-page">Venues</h1>
- Element IDs:
  - venues-page (div): Container
  - venues-grid (div): Grid with venue cards
  - venue-search-input (input): Search input
  - venue-capacity-filter (dropdown): Capacity filter
  - view-venue-details-{venue_id} (button): Button to view venue details (dynamic id)
- Context variables:
  - venues: list of dict with venue_id, venue_name, location, capacity, amenities
  - capacity_options: list of strings [Small, Medium, Large]
- Navigation Buttons:
  - Each view-venue-details-{venue_id} -> No route defined (no venue details page per requirements)
- Dynamic ID:
  - view-venue-details-{{ venue.venue_id }} inside loop over venues

### 7. Event Schedules Page
- Template file path: templates/schedules.html
- Page title: <title>Event Schedules</title>
- Heading: <h1 id="schedules-page">Event Schedules</h1>
- Element IDs:
  - schedules-page (div): Container
  - schedules-timeline (div): Timeline of events and sessions
  - schedule-filter-date (input date): Filter by date
  - schedule-filter-event (dropdown): Filter by event
  - export-schedule-button (button): Button to export schedule
- Context variables:
  - schedules: list of dict with schedule_id, event_id, session_title, session_time, duration_minutes, speaker, venue_id
  - events: list of dict with event_id, event_name
- Navigation Buttons:
  - export-schedule-button -> route to export schedule (not defined, assumed handled through JavaScript or backend)

### 8. Bookings Summary Page
- Template file path: templates/bookings.html
- Page title: <title>My Bookings</title>
- Heading: <h1 id="bookings-page">My Bookings</h1>
- Element IDs:
  - bookings-page (div): Container
  - bookings-table (table): Table listing bookings
  - booking-search-input (input): Search bookings
  - cancel-booking-button-{booking_id} (button): Button to cancel booking (dynamic id)
  - back-to-dashboard (button): Button to navigate back to dashboard
- Context variables:
  - bookings: list of dict with booking_id, event_id, event_name, date, ticket_count, status, ticket_type
- Navigation Buttons:
  - cancel-booking-button-{{ booking.booking_id }} -> url_for('cancel_booking', booking_id=booking.booking_id)
  - back-to-dashboard -> url_for('dashboard_page')

---

## Section 3: Data File Schemas

### 1. Events Data
- File path: data/events.txt
- Fields (pipe-delimited):
  1. event_id (int)
  2. event_name (str)
  3. category (str)
  4. date (YYYY-MM-DD, str)
  5. time (HH:MM, str)
  6. location (str)
  7. description (str)
  8. venue_id (int)
  9. capacity (int)
- Description: Stores all event information including scheduling and venue reference.
- Example rows:
  ```
  1|Tech Conference 2025|Conference|2025-03-15|09:00|Convention Center, San Francisco|Annual technology conference discussing latest innovations|1|500
  2|Summer Music Festival|Concert|2025-06-20|18:00|Central Park, New York|Three-day music festival with international artists|2|5000
  3|Marathon Championship|Sports|2025-04-10|07:00|Downtown Loop, Chicago|Annual city marathon event for all skill levels|3|1000
  ```

### 2. Venues Data
- File path: data/venues.txt
- Fields (pipe-delimited):
  1. venue_id (int)
  2. venue_name (str)
  3. location (str)
  4. capacity (int)
  5. amenities (str)
  6. contact (str)
- Description: Stores venue details for event locations.
- Example rows:
  ```
  1|Convention Center|San Francisco, CA|500|WiFi, Parking, Catering|contact@convention.com
  2|Central Park|New York, NY|5000|Outdoor Space, Restrooms, Food Vendors|info@centralparkevents.org
  3|Downtown Loop|Chicago, IL|1000|Paved Surface, Water Stations, Medical Support|events@downtown.com
  ```

### 3. Tickets Data
- File path: data/tickets.txt
- Fields (pipe-delimited):
  1. ticket_id (int)
  2. event_id (int)
  3. ticket_type (str)
  4. price (float)
  5. available_count (int)
  6. sold_count (int)
- Description: Stores ticket types, pricing, and availability per event.
- Example rows:
  ```
  1|1|General|49.99|500|150
  2|1|VIP|99.99|100|45
  3|2|Early Bird|39.99|1000|750
  ```

### 4. Bookings Data
- File path: data/bookings.txt
- Fields (pipe-delimited):
  1. booking_id (int)
  2. event_id (int)
  3. customer_name (str)
  4. booking_date (YYYY-MM-DD, str)
  5. ticket_count (int)
  6. ticket_type (str)
  7. total_amount (float)
  8. status (str)
- Description: Stores individual bookings with status tracking.
- Example rows:
  ```
  1|1|Alice Johnson|2025-02-01|2|General|99.98|Confirmed
  2|2|Bob Williams|2025-02-05|4|Early Bird|159.96|Confirmed
  3|1|Carol Davis|2025-02-10|1|VIP|99.99|Pending
  ```

### 5. Participants Data
- File path: data/participants.txt
- Fields (pipe-delimited):
  1. participant_id (int)
  2. event_id (int)
  3. name (str)
  4. email (str)
  5. booking_id (int)
  6. status (str)
  7. registration_date (YYYY-MM-DD, str)
- Description: Stores participants linked to bookings and event attendance status.
- Example rows:
  ```
  1|1|Alice Johnson|alice@email.com|1|Confirmed|2025-02-01
  2|1|Michael Johnson|michael@email.com|1|Confirmed|2025-02-01
  3|2|Bob Williams|bob@email.com|2|Attended|2025-02-05
  ```

### 6. Schedules Data
- File path: data/schedules.txt
- Fields (pipe-delimited):
  1. schedule_id (int)
  2. event_id (int)
  3. session_title (str)
  4. session_time (YYYY-MM-DD HH:MM, str)
  5. duration_minutes (int)
  6. speaker (str)
  7. venue_id (int)
- Description: Stores detailed schedule of event sessions and speakers.
- Example rows:
  ```
  1|1|Opening Keynote|2025-03-15 09:00|60|John Smith|1
  2|1|Panel Discussion|2025-03-15 10:30|90|Expert Panel|1
  3|2|Headliner Performance|2025-06-20 20:00|120|International Artist|2
  ```

---

This design specification provides comprehensive and precise instructions for backend route implementation and frontend templates development with exact element IDs and context variables. The data file schemas enable reliable backend data management and parsing.

No assumptions beyond this specification should be made during development.
