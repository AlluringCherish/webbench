# EventPlanning Application Design Specification

---

## Section 1: Flask Routes Specification

| Route Path              | Function Name           | HTTP Methods | Template File           | Context Variables                                                                                                                                                                      |
|-------------------------|-------------------------|--------------|-------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| /                       | root_redirect            | GET          | None                    | None. Redirects to `/dashboard`.                                                                                                               |
| /dashboard              | dashboard_page          | GET          | dashboard.html          | featured_events: List[Dict] - List of featured event dicts with keys: event_id (int), event_name (str), date (str), location (str)                                                      |
| /events                 | events_listing_page     | GET          | events.html             | events: List[Dict] - All event dicts with keys: event_id (int), event_name (str), category (str), date (str), time (str), location (str)                                                |
|                         |                         |              |                         |  description (str), venue_id (int), capacity (int)                                                                                                   |
| /events/search          | events_search           | POST         | events.html             | events: List[Dict] - Filtered events list, same structure as above                                                                                                                      |
| /event/<int:event_id>   | event_details_page      | GET          | event_details.html      | event: Dict - Event dict with keys: event_id, event_name, category, date, time, location, description, venue_id, capacity                                                                |
| /book_ticket            | book_ticket_page        | GET, POST    | book_ticket.html        | GET: events: List[Dict] - All events for dropdown selection (event_id, event_name)                                                                                                      |
|                         |                         |              |                         | POST: booking_confirmation: Dict - Details of booking confirmation with keys: event_name, ticket_count, ticket_type, total_amount, status                                             |
| /participants           | participants_page       | GET          | participants.html       | participants: List[Dict] - Participants with participant_id (int), event_id (int), name (str), email (str), booking_id (int), status (str), registration_date (str)                      |
| /participants/add       | add_participant         | POST         | participants.html       | participants: List[Dict] - Updated list after adding participant (same structure as above)                                                                                                |
| /participants/search    | search_participants     | POST         | participants.html       | participants: List[Dict] - Filtered list by search/filter criteria                                                                                                                      |
| /venues                 | venues_page             | GET          | venues.html             | venues: List[Dict] - Venues with venue_id (int), venue_name (str), location (str), capacity (int), amenities (str), contact (str)                                                      |
| /venues/search          | venues_search           | POST         | venues.html             | venues: List[Dict] - Filtered venues based on search/filter                                                                                                                             |
| /event_schedules        | event_schedules_page    | GET          | schedules.html          | schedules: List[Dict] - Schedules with schedule_id (int), event_id (int), session_title (str), session_time (str), duration_minutes (int), speaker (str), venue_id (int)                 |
| /event_schedules/filter | filter_schedules        | POST         | schedules.html          | filtered_schedules: List[Dict] - Filtered schedules list (structure same as above)                                                                                                       |
| /bookings               | bookings_page           | GET          | bookings.html           | bookings: List[Dict] - Bookings with booking_id (int), event_id (int), customer_name (str), booking_date (str), ticket_count (int), ticket_type (str), total_amount (float), status (str)|
| /bookings/cancel/<int:booking_id> | cancel_booking    | POST         | bookings.html           | bookings: List[Dict] - Updated bookings list after cancellation (same structure as above)                                                                                                |


---

## Section 2: HTML Template Specifications

### 1. Dashboard Page
- Template File Path: templates/dashboard.html
- Page Title (both <title> and <h1>): Event Planning Dashboard
- Element IDs:
  - dashboard-page (Div): Container for the dashboard page.
  - featured-events (Div): Display of featured event recommendations.
  - browse-events-button (Button): Navigate to /events.
  - view-tickets-button (Button): Navigate to /bookings.
  - venues-button (Button): Navigate to /venues.
- Context Variables:
  - featured_events: List[Dict] with keys: event_id, event_name, date, location
- Navigation Buttons:
  - browse-events-button → url_for('events_listing_page')
  - view-tickets-button → url_for('bookings_page')
  - venues-button → url_for('venues_page')

### 2. Events Listing Page
- Template File Path: templates/events.html
- Page Title: Events Catalog
- Element IDs:
  - events-page (Div): Container for the events listing page.
  - event-search-input (Input): Search field for events.
  - event-category-filter (Dropdown): Filter by category.
  - events-grid (Div): Grid displaying event cards.
  - view-event-button-{event_id} (Button): Button to view event details.
- Context Variables:
  - events: List[Dict] each with keys:
    - event_id, event_name, category, date, time, location, description, venue_id, capacity
- Navigation Buttons:
  - None explicitly defined but should include browse back if needed
- Dynamic IDs:
  - For each event in `events`, create button with id="view-event-button-{{ event.event_id }}"

### 3. Event Details Page
- Template File Path: templates/event_details.html
- Page Title: Event Details
- Element IDs:
  - event-details-page (Div)
  - event-title (H1): event.event_name
  - event-date (Div): event.date and event.time
  - event-location (Div): event.location
  - event-description (Div): event.description
  - book-ticket-button (Button): Navigate to /book_ticket with event preselected
- Context Variables:
  - event: Dict with keys as above
- Navigation Buttons:
  - book-ticket-button → url_for('book_ticket_page') (with event preselected parameter passed via query string or form)

### 4. Ticket Booking Page
- Template File Path: templates/book_ticket.html
- Page Title: Book Your Tickets
- Element IDs:
  - ticket-booking-page (Div)
  - select-event-dropdown (Dropdown): List of events for selection.
  - ticket-quantity-input (Input number)
  - ticket-type-select (Dropdown): Options General, VIP, Early Bird
  - book-now-button (Button): Submit booking
  - booking-confirmation (Div): Show confirmation after POST
- Context Variables:
  - GET: events (List[Dict]) with event_id, event_name
  - POST: booking_confirmation (Dict) with keys: event_name, ticket_count, ticket_type, total_amount, status
- Navigation Buttons:
  - None explicit, but can have back navigation to event details or dashboard

### 5. Participants Management Page
- Template File Path: templates/participants.html
- Page Title: Participants Management
- Element IDs:
  - participants-page (Div)
  - participants-table (Table): Columns - name, email, event, status
  - add-participant-button (Button)
  - search-participant-input (Input)
  - participant-status-filter (Dropdown): Registered, Confirmed, Attended
- Context Variables:
  - participants: List[Dict] with keys participant_id, event_id, name, email, booking_id, status, registration_date
- Navigation Buttons:
  - None explicit

### 6. Venue Information Page
- Template File Path: templates/venues.html
- Page Title: Venues
- Element IDs:
  - venues-page (Div)
  - venues-grid (Div): Venue cards display
  - venue-search-input (Input)
  - venue-capacity-filter (Dropdown): Small, Medium, Large
  - view-venue-details-{venue_id} (Button)
- Context Variables:
  - venues: List[Dict] with keys venue_id, venue_name, location, capacity, amenities, contact
- Navigation Buttons:
  - None explicit
- Dynamic IDs:
  - For each venue, button id="view-venue-details-{{ venue.venue_id }}"

### 7. Event Schedules Page
- Template File Path: templates/schedules.html
- Page Title: Event Schedules
- Element IDs:
  - schedules-page (Div)
  - schedules-timeline (Div)
  - schedule-filter-date (Input date)
  - schedule-filter-event (Dropdown)
  - export-schedule-button (Button)
- Context Variables:
  - schedules: List[Dict] with schedule_id, event_id, session_title, session_time, duration_minutes, speaker, venue_id
- Navigation Buttons:
  - None explicit

### 8. Bookings Summary Page
- Template File Path: templates/bookings.html
- Page Title: My Bookings
- Element IDs:
  - bookings-page (Div)
  - bookings-table (Table): Columns event, date, ticket count, status
  - booking-search-input (Input)
  - cancel-booking-button-{booking_id} (Button)
  - back-to-dashboard (Button)
- Context Variables:
  - bookings: List[Dict] with booking_id, event_id, customer_name, booking_date, ticket_count, ticket_type, total_amount, status
- Navigation Buttons:
  - back-to-dashboard → url_for('dashboard_page')
- Dynamic IDs:
  - For each booking, button id="cancel-booking-button-{{ booking.booking_id }}"

---

## Section 3: Data File Schemas

### 1. Events Data
- File path: data/events.txt
- Pipe-delimited fields in order:
  event_id (int)|event_name (str)|category (str)|date (str, YYYY-MM-DD)|time (str, HH:MM)|location (str)|description (str)|venue_id (int)|capacity (int)
- Description: Stores details of all events.
- Example rows:
  ```
  1|Tech Conference 2025|Conference|2025-03-15|09:00|Convention Center, San Francisco|Annual technology conference discussing latest innovations|1|500
  2|Summer Music Festival|Concert|2025-06-20|18:00|Central Park, New York|Three-day music festival with international artists|2|5000
  3|Marathon Championship|Sports|2025-04-10|07:00|Downtown Loop, Chicago|Annual city marathon event for all skill levels|3|1000
  ```

### 2. Venues Data
- File path: data/venues.txt
- Pipe-delimited fields:
  venue_id (int)|venue_name (str)|location (str)|capacity (int)|amenities (str)|contact (str)
- Description: Stores venue information.
- Example rows:
  ```
  1|Convention Center|San Francisco, CA|500|WiFi, Parking, Catering|contact@convention.com
  2|Central Park|New York, NY|5000|Outdoor Space, Restrooms, Food Vendors|info@centralparkevents.org
  3|Downtown Loop|Chicago, IL|1000|Paved Surface, Water Stations, Medical Support|events@downtown.com
  ```

### 3. Tickets Data
- File path: data/tickets.txt
- Pipe-delimited fields:
  ticket_id (int)|event_id (int)|ticket_type (str)|price (float)|available_count (int)|sold_count (int)
- Description: Stores ticket types and availability per event.
- Example rows:
  ```
  1|1|General|49.99|500|150
  2|1|VIP|99.99|100|45
  3|2|Early Bird|39.99|1000|750
  ```

### 4. Bookings Data
- File path: data/bookings.txt
- Pipe-delimited fields:
  booking_id (int)|event_id (int)|customer_name (str)|booking_date (str, YYYY-MM-DD)|ticket_count (int)|ticket_type (str)|total_amount (float)|status (str)
- Description: Stores user bookings with ticket and status info.
- Example rows:
  ```
  1|1|Alice Johnson|2025-02-01|2|General|99.98|Confirmed
  2|2|Bob Williams|2025-02-05|4|Early Bird|159.96|Confirmed
  3|1|Carol Davis|2025-02-10|1|VIP|99.99|Pending
  ```

### 5. Participants Data
- File path: data/participants.txt
- Pipe-delimited fields:
  participant_id (int)|event_id (int)|name (str)|email (str)|booking_id (int)|status (str)|registration_date (str, YYYY-MM-DD)
- Description: Stores participants and their registration status.
- Example rows:
  ```
  1|1|Alice Johnson|alice@email.com|1|Confirmed|2025-02-01
  2|1|Michael Johnson|michael@email.com|1|Confirmed|2025-02-01
  3|2|Bob Williams|bob@email.com|2|Attended|2025-02-05
  ```

### 6. Schedules Data
- File path: data/schedules.txt
- Pipe-delimited fields:
  schedule_id (int)|event_id (int)|session_title (str)|session_time (str, YYYY-MM-DD HH:MM)|duration_minutes (int)|speaker (str)|venue_id (int)
- Description: Event sessions schedule information.
- Example rows:
  ```
  1|1|Opening Keynote|2025-03-15 09:00|60|John Smith|1
  2|1|Panel Discussion|2025-03-15 10:30|90|Expert Panel|1
  3|2|Headliner Performance|2025-06-20 20:00|120|International Artist|2
  ```
