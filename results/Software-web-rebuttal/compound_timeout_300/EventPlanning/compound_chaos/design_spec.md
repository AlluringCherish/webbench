# EventPlanning Application Design Specification

---

## Section 1: Flask Routes Specification

| Route Path                   | Function Name           | HTTP Methods | Template File           | Context Variables                                                                                                   |
|------------------------------|-------------------------|--------------|-------------------------|--------------------------------------------------------------------------------------------------------------------|
| /                            | root_redirect           | GET          | None (redirect to /dashboard) | None                                                                                                             |
| /dashboard                   | dashboard_page          | GET          | dashboard.html           | featured_events: List[dict] with keys event_id (int), event_name (str), date (str), location (str)                 |
| /events                      | events_listing          | GET          | events.html              | events: List[dict] with keys event_id (int), event_name (str), category (str), date (str), time (str), location (str), description (str), venue_id (int), capacity (int) |
| /events/filter               | filter_events           | POST         | events.html              | events: List[dict] filtered by search and/or category, fields as above                                          |
| /event/<int:event_id>        | event_details           | GET          | event_details.html       | event: dict with fields as per events                                                                              |
| /ticket_booking              | ticket_booking_page     | GET, POST    | ticket_booking.html      | GET: events for dropdown (List[dict] with event_id:int, event_name:str), POST: confirmation dict or message (str)   |
| /book_ticket                 | book_ticket             | POST         | ticket_booking.html      | confirmation dict or message (str)                                                                                  |
| /participants                | participants_management | GET          | participants.html        | participants: List[dict] with participant_id (int), event_id (int), name (str), email (str), booking_id (int), status (str), registration_date (str) |
| /participants/add            | add_participant         | POST         | participants.html        | updated participants list or error message                                                                       |
| /venues                     | venues_page             | GET          | venues.html              | venues: List[dict] with venue_id (int), venue_name (str), location (str), capacity (int), amenities (str), contact (str) |
| /venues/filter              | filter_venues           | POST         | venues.html              | venues: List[dict] filtered by search criteria, fields as above                                                  |
| /venue/<int:venue_id>        | venue_details           | GET          | venue_details.html       | venue: dict with fields as per venues                                                                              |
| /schedules                   | schedules_page          | GET          | schedules.html           | schedules: List[dict] with schedule_id (int), event_id (int), session_title (str), session_time (str), duration_minutes (int), speaker (str), venue_id (int); events: List[dict] for filters |
| /bookings                   | bookings_summary        | GET          | bookings.html            | bookings: List[dict] with booking_id (int), event_id (int), customer_name (str), booking_date (str), ticket_count (int), ticket_type (str), total_amount (float), status (str) |
| /bookings/cancel/<int:booking_id> | cancel_booking    | POST         | bookings.html            | updated bookings list or error message                                                                             |
| /back_to_dashboard          | back_to_dashboard       | GET          | None (redirect to /dashboard) | None                                                                                                             |

---

## Section 2: HTML Template Specifications

### 1. Dashboard Page
- Template file path: templates/dashboard.html
- Page Title: Event Planning Dashboard
- Elements:
  - dashboard-page (Div): Container for dashboard
  - featured-events (Div): Featured event recommendations display
  - browse-events-button (Button): Navigate to /events
  - view-tickets-button (Button): Navigate to /bookings
  - venues-button (Button): Navigate to /venues
- Context Variables:
  - featured_events: List[dict] with event_id:int, event_name:str, date:str, location:str
- Navigation Buttons:
  - browse-events-button → url_for('events_listing')
  - view-tickets-button → url_for('bookings_summary')
  - venues-button → url_for('venues_page')

### 2. Events Listing Page
- Template file path: templates/events.html
- Page Title: Events Catalog
- Elements:
  - events-page (Div): Container for events listing
  - event-search-input (Input): Search field
  - event-category-filter (Dropdown): Filter by category
  - events-grid (Div): Grid for event cards
  - view-event-button-{event_id} (Button): Button on each event card to view details
- Context Variables:
  - events: List[dict] with event_id:int, event_name:str, category:str, date:str, time:str, location:str, description:str, venue_id:int, capacity:int
- Navigation Buttons: None
- Dynamic IDs:
  - view-event-button-{{ event.event_id }} with Jinja2 loop

### 3. Event Details Page
- Template file path: templates/event_details.html
- Page Title: Event Details
- Elements:
  - event-details-page (Div): Container
  - event-title (H1): Event title
  - event-date (Div): Event date and time
  - event-location (Div): Event location
  - event-description (Div): Event description
  - book-ticket-button (Button): Button to book ticket
- Context Variables:
  - event: dict with fields matching event
- Navigation Buttons:
  - book-ticket-button → url_for('ticket_booking_page', event_id=event.event_id)

### 4. Ticket Booking Page
- Template file path: templates/ticket_booking.html
- Page Title: Book Your Tickets
- Elements:
  - ticket-booking-page (Div): Container
  - select-event-dropdown (Dropdown): Select event
  - ticket-quantity-input (Input number): Quantity input
  - ticket-type-select (Dropdown): Ticket type select (General, VIP, Early Bird)
  - book-now-button (Button): Submit booking
  - booking-confirmation (Div): Display booking confirmation
- Context Variables:
  - events: List[dict] with event_id:int, event_name:str
  - confirmation: dict or str (optional)
- Navigation Buttons: None

### 5. Participants Management Page
- Template file path: templates/participants.html
- Page Title: Participants Management
- Elements:
  - participants-page (Div): Container
  - participants-table (Table): Participants list
  - add-participant-button (Button): Add participant
  - search-participant-input (Input): Search field
  - participant-status-filter (Dropdown): Filter by status
- Context Variables:
  - participants: List[dict] with participant_id:int, event_id:int, name:str, email:str, booking_id:int, status:str, registration_date:str
- Navigation Buttons:
  - add-participant-button triggers participant addition

### 6. Venue Information Page
- Template file path: templates/venues.html
- Page Title: Venues
- Elements:
  - venues-page (Div): Container
  - venues-grid (Div): Venue cards grid
  - venue-search-input (Input): Search field
  - venue-capacity-filter (Dropdown): Filter by capacity (Small, Medium, Large)
  - view-venue-details-{venue_id} (Button): Button per venue to view details
- Context Variables:
  - venues: List[dict] with venue_id:int, venue_name:str, location:str, capacity:int, amenities:str, contact:str
- Navigation Buttons: None
- Dynamic IDs:
  - view-venue-details-{{ venue.venue_id }} with Jinja2 loop

### 7. Event Schedules Page
- Template file path: templates/schedules.html
- Page Title: Event Schedules
- Elements:
  - schedules-page (Div): Container
  - schedules-timeline (Div): Timeline of events and sessions
  - schedule-filter-date (Input date): Date filter
  - schedule-filter-event (Dropdown): Event filter
  - export-schedule-button (Button): Export schedule button
- Context Variables:
  - schedules: List[dict] with schedule_id:int, event_id:int, session_title:str, session_time:str, duration_minutes:int, speaker:str, venue_id:int
  - events: List[dict] for filter dropdown
- Navigation Buttons:
  - export-schedule-button triggers export functionality

### 8. Bookings Summary Page
- Template file path: templates/bookings.html
- Page Title: My Bookings
- Elements:
  - bookings-page (Div): Container
  - bookings-table (Table): List of bookings
  - booking-search-input (Input): Search field
  - cancel-booking-button-{booking_id} (Button): Cancel booking button
  - back-to-dashboard (Button): Back to dashboard button
- Context Variables:
  - bookings: List[dict] with booking_id:int, event_id:int, customer_name:str, booking_date:str, ticket_count:int, ticket_type:str, total_amount:float, status:str
- Navigation Buttons:
  - back-to-dashboard → url_for('dashboard_page')
- Dynamic IDs:
  - cancel-booking-button-{{ booking.booking_id }} with Jinja2 loop

---

## Section 3: Data File Schemas

### 1. Events Data
- File path: data/events.txt
- Fields (pipe-delimited): event_id|event_name|category|date|time|location|description|venue_id|capacity
- Description: Stores event details
- Examples:
  ```
  1|Tech Conference 2025|Conference|2025-03-15|09:00|Convention Center, San Francisco|Annual technology conference discussing latest innovations|1|500
  2|Summer Music Festival|Concert|2025-06-20|18:00|Central Park, New York|Three-day music festival with international artists|2|5000
  3|Marathon Championship|Sports|2025-04-10|07:00|Downtown Loop, Chicago|Annual city marathon event for all skill levels|3|1000
  ```
- No header; numeric fields as integers.

### 2. Venues Data
- File path: data/venues.txt
- Fields: venue_id|venue_name|location|capacity|amenities|contact
- Description: Venue details including amenities
- Examples:
  ```
  1|Convention Center|San Francisco, CA|500|WiFi, Parking, Catering|contact@convention.com
  2|Central Park|New York, NY|5000|Outdoor Space, Restrooms, Food Vendors|info@centralparkevents.org
  3|Downtown Loop|Chicago, IL|1000|Paved Surface, Water Stations, Medical Support|events@downtown.com
  ```
- No header; venue_id and capacity as integers.

### 3. Tickets Data
- File path: data/tickets.txt
- Fields: ticket_id|event_id|ticket_type|price|available_count|sold_count
- Description: Ticket types and availability
- Examples:
  ```
  1|1|General|49.99|500|150
  2|1|VIP|99.99|100|45
  3|2|Early Bird|39.99|1000|750
  ```
- Numeric fields as appropriate.

### 4. Bookings Data
- File path: data/bookings.txt
- Fields: booking_id|event_id|customer_name|booking_date|ticket_count|ticket_type|total_amount|status
- Description: Booking records
- Examples:
  ```
  1|1|Alice Johnson|2025-02-01|2|General|99.98|Confirmed
  2|2|Bob Williams|2025-02-05|4|Early Bird|159.96|Confirmed
  3|1|Carol Davis|2025-02-10|1|VIP|99.99|Pending
  ```
- Numeric fields as appropriate.

### 5. Participants Data
- File path: data/participants.txt
- Fields: participant_id|event_id|name|email|booking_id|status|registration_date
- Description: Event participants
- Examples:
  ```
  1|1|Alice Johnson|alice@email.com|1|Confirmed|2025-02-01
  2|1|Michael Johnson|michael@email.com|1|Confirmed|2025-02-01
  3|2|Bob Williams|bob@email.com|2|Attended|2025-02-05
  ```
- Numeric fields as appropriate.

### 6. Schedules Data
- File path: data/schedules.txt
- Fields: schedule_id|event_id|session_title|session_time|duration_minutes|speaker|venue_id
- Description: Event session schedules
- Examples:
  ```
  1|1|Opening Keynote|2025-03-15 09:00|60|John Smith|1
  2|1|Panel Discussion|2025-03-15 10:30|90|Expert Panel|1
  3|2|Headliner Performance|2025-06-20 20:00|120|International Artist|2
  ```
- Numeric fields as appropriate.

---

This comprehensive design specification enables backend and frontend developers to build the EventPlanning application accurately according to all given requirements, without assumptions or omissions.