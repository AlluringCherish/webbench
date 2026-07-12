# Design Specification Document for 'EventPlanning' Web Application

---

## Section 1: Flask Routes Specification

| Route Path           | Function Name          | HTTP Methods | Template File            | Context Variables Description                                                                                                                                                   |
|----------------------|------------------------|--------------|--------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| /                    | root_redirect           | GET          | None (redirect)           | None (redirects to /dashboard)                                                                                                                                                   |
| /dashboard           | dashboard_page          | GET          | dashboard.html           | featured_events: List[Dict] with keys: event_id (int), event_name (str), date (str), location (str) – featured event recommendations                                            |
| /events              | events_listing          | GET          | events.html              | events: List[Dict], each dict has event_id (int), event_name (str), category (str), date (str), location (str), description (str), venue_id (int), capacity (int)                 |
| /events/search       | events_search           | POST         | events.html              | filtered_events: List[Dict] same structure as events; search_category (str), search_text (str)                                                                                     |
| /event/<int:event_id>| event_details           | GET          | event_details.html       | event: Dict with event_id (int), event_name (str), category (str), date (str), time (str), location (str), description (str), venue_id (int), capacity (int)                      |
| /book_ticket         | book_ticket             | GET, POST    | book_ticket.html         | GET: events: List[Dict] (as above);
POST: booking_confirmation: Dict with booking details (str fields: confirmation_message, event_name, ticket_type str, ticket_quantity int etc.)|
| /participants        | participants_management | GET          | participants.html        | participants: List[Dict], each dict with participant_id (int), event_id (int), name (str), email (str), booking_id (int), status (str), registration_date (str)                     |
| /participants/search | participants_search     | POST         | participants.html        | filtered_participants: List[Dict] same as participants; search_text (str); status_filter (str)                                                                                     |
| /venues              | venues_page             | GET          | venues.html              | venues: List[Dict], each dict with venue_id (int), venue_name (str), location (str), capacity (int), amenities (str), contact (str)                                                |
| /event_schedules     | event_schedules         | GET          | schedules.html           | schedules: List[Dict], each dict with schedule_id (int), event_id (int), session_title (str), session_time (str), duration_minutes (int), speaker (str), venue_id (int)             |
| /bookings           | bookings_summary         | GET          | bookings.html            | bookings: List[Dict], each dict with booking_id (int), event_id (int), customer_name (str), booking_date (str), ticket_count (int), ticket_type (str), total_amount (float), status (str) |
| /cancel_booking/<int:booking_id> | cancel_booking | POST         | None (redirect to /bookings)                                                        | Success or failure message handled in redirect context or flash messages                                                                                                       |

---

## Section 2: HTML Template Specifications

### 1. Dashboard Page
- Template File Path: templates/dashboard.html
- Page Title: "Event Planning Dashboard"
- <title> tag content: "Event Planning Dashboard"
- <h1> tag content: "Event Planning Dashboard"
- Element IDs:
  - dashboard-page (Div): Container for the dashboard page.
  - featured-events (Div): Display of featured event recommendations.
  - browse-events-button (Button): Button to navigate to events listing page.
  - view-tickets-button (Button): Button to navigate to tickets page.
  - venues-button (Button): Button to navigate to venues page.
- Context Variables:
  - featured_events: List of dicts with keys event_id(int), event_name(str), date(str), location(str)
- Navigation Buttons:
  - browse-events-button: url_for('events_listing')
  - view-tickets-button: url_for('bookings_summary')
  - venues-button: url_for('venues_page')

### 2. Events Listing Page
- Template File Path: templates/events.html
- Page Title: "Events Catalog"
- <title> and <h1>: "Events Catalog"
- Element IDs:
  - events-page (Div): Container for the events listing page.
  - event-search-input (Input): Field to search events by name, location, or date.
  - event-category-filter (Dropdown Select): Filter by category (Conference, Concert, Sports, Workshop, Social).
  - events-grid (Div): Grid displaying event cards.
  - view-event-button-{event_id} (Button): Dynamic button per event to view details.

- Context Variables:
  - events: List of dicts with event_id(int), event_name(str), category(str), date(str), location(str), description(str), venue_id(int), capacity(int)

- Navigation Buttons:
  - Back to dashboard: url_for('dashboard_page') (if needed)

- Dynamic IDs:
  - Render buttons inside a Jinja2 loop:
  ```jinja
  {% for event in events %}
    <button id="view-event-button-{{ event.event_id }}">View Details</button>
  {% endfor %}
  ```

### 3. Event Details Page
- Template File Path: templates/event_details.html
- Page Title: "Event Details"
- <title> and <h1>: "Event Details"
- Element IDs:
  - event-details-page (Div)
  - event-title (H1): Event title
  - event-date (Div): Event date and time
  - event-location (Div): Event location
  - event-description (Div): Detailed description
  - book-ticket-button (Button): Button to book ticket
- Context Variables:
  - event: Dict with event_id(int), event_name(str), category(str), date(str), time(str), location(str), description(str), venue_id(int), capacity(int)
- Navigation Buttons:
  - book-ticket-button: url_for('book_ticket') with event selection if handled

### 4. Ticket Booking Page
- Template File Path: templates/book_ticket.html
- Page Title: "Book Your Tickets"
- <title> and <h1>: "Book Your Tickets"
- Element IDs:
  - ticket-booking-page (Div)
  - select-event-dropdown (Dropdown Select)
  - ticket-quantity-input (Input type=number)
  - ticket-type-select (Dropdown Select): Options: General, VIP, Early Bird
  - book-now-button (Button)
  - booking-confirmation (Div): Shows booking confirmation details
- Context Variables:
  - GET request:
    - events: List of dicts similar to in events listing
  - POST request (after booking):
    - booking_confirmation: Dict with confirmation_message (str), event_name (str), ticket_type (str), ticket_quantity (int), total_amount (float)
- Navigation Buttons:
  - Back to dashboard: url_for('dashboard_page')

### 5. Participants Management Page
- Template File Path: templates/participants.html
- Page Title: "Participants Management"
- <title> and <h1>: "Participants Management"
- Element IDs:
  - participants-page (Div)
  - participants-table (Table)
  - add-participant-button (Button)
  - search-participant-input (Input)
  - participant-status-filter (Dropdown Select): Options: Registered, Confirmed, Attended
- Context Variables:
  - participants: List of dicts, each with participant_id (int), event_id (int), name (str), email (str), booking_id (int), status (str), registration_date (str)
- Navigation Buttons:
  - Back to dashboard: url_for('dashboard_page')

### 6. Venue Information Page
- Template File Path: templates/venues.html
- Page Title: "Venues"
- <title> and <h1>: "Venues"
- Element IDs:
  - venues-page (Div)
  - venues-grid (Div)
  - venue-search-input (Input)
  - venue-capacity-filter (Dropdown Select): Options: Small, Medium, Large
  - view-venue-details-{venue_id} (Button): Dynamic buttons for each venue card
- Context Variables:
  - venues: List of dicts, each with venue_id (int), venue_name (str), location (str), capacity (int), amenities (str), contact (str)
- Navigation Buttons:
  - Back to dashboard: url_for('dashboard_page')
- Dynamic IDs:
  - Render buttons inside Jinja2 loop:
  ```jinja
  {% for venue in venues %}
    <button id="view-venue-details-{{ venue.venue_id}}">View Details</button>
  {% endfor %}
  ```

### 7. Event Schedules Page
- Template File Path: templates/schedules.html
- Page Title: "Event Schedules"
- <title> and <h1>: "Event Schedules"
- Element IDs:
  - schedules-page (Div)
  - schedules-timeline (Div)
  - schedule-filter-date (Input type=date)
  - schedule-filter-event (Dropdown Select)
  - export-schedule-button (Button)
- Context Variables:
  - schedules: List of dicts with schedule_id(int), event_id(int), session_title(str), session_time(str), duration_minutes(int), speaker(str), venue_id(int)
- Navigation Buttons:
  - Back to dashboard: url_for('dashboard_page')

### 8. Bookings Summary Page
- Template File Path: templates/bookings.html
- Page Title: "My Bookings"
- <title> and <h1>: "My Bookings"
- Element IDs:
  - bookings-page (Div)
  - bookings-table (Table)
  - booking-search-input (Input)
  - cancel-booking-button-{booking_id} (Button): Dynamic
  - back-to-dashboard (Button)
- Context Variables:
  - bookings: List of dicts with booking_id (int), event_id (int), customer_name (str), booking_date (str), ticket_count (int), ticket_type (str), total_amount (float), status (str)
- Navigation Buttons:
  - back-to-dashboard: url_for('dashboard_page')
- Dynamic IDs:
  - Render cancel buttons inside Jinja2 loop:
  ```jinja
  {% for booking in bookings %}
    <button id="cancel-booking-button-{{ booking.booking_id }}">Cancel Booking</button>
  {% endfor %}
  ```

---

## Section 3: Data File Schemas

### 1. Events Data
- File Path: data/events.txt
- Fields (pipe-delimited, no header):
  - event_id (int)
  - event_name (str)
  - category (str) [Conference, Concert, Sports, Workshop, Social]
  - date (str) YYYY-MM-DD
  - time (str) HH:MM
  - location (str)
  - description (str)
  - venue_id (int)
  - capacity (int)
- Example Data:
  ```
  1|Tech Conference 2025|Conference|2025-03-15|09:00|Convention Center, San Francisco|Annual technology conference discussing latest innovations|1|500
  2|Summer Music Festival|Concert|2025-06-20|18:00|Central Park, New York|Three-day music festival with international artists|2|5000
  3|Marathon Championship|Sports|2025-04-10|07:00|Downtown Loop, Chicago|Annual city marathon event for all skill levels|3|1000
  ```
- Description: Stores all event metadata for planning and display.

### 2. Venues Data
- File Path: data/venues.txt
- Fields (pipe-delimited, no header):
  - venue_id (int)
  - venue_name (str)
  - location (str)
  - capacity (int)
  - amenities (str) - comma separated
  - contact (str)
- Example Data:
  ```
  1|Convention Center|San Francisco, CA|500|WiFi, Parking, Catering|contact@convention.com
  2|Central Park|New York, NY|5000|Outdoor Space, Restrooms, Food Vendors|info@centralparkevents.org
  3|Downtown Loop|Chicago, IL|1000|Paved Surface, Water Stations, Medical Support|events@downtown.com
  ```
- Description: Information about venues available for hosting events.

### 3. Tickets Data
- File Path: data/tickets.txt
- Fields (pipe-delimited, no header):
  - ticket_id (int)
  - event_id (int)
  - ticket_type (str) [General, VIP, Early Bird]
  - price (float)
  - available_count (int)
  - sold_count (int)
- Example Data:
  ```
  1|1|General|49.99|500|150
  2|1|VIP|99.99|100|45
  3|2|Early Bird|39.99|1000|750
  ```
- Description: Ticket categories and availability per event.

### 4. Bookings Data
- File Path: data/bookings.txt
- Fields (pipe-delimited, no header):
  - booking_id (int)
  - event_id (int)
  - customer_name (str)
  - booking_date (str) YYYY-MM-DD
  - ticket_count (int)
  - ticket_type (str)
  - total_amount (float)
  - status (str) [Pending, Confirmed, Cancelled]
- Example Data:
  ```
  1|1|Alice Johnson|2025-02-01|2|General|99.98|Confirmed
  2|2|Bob Williams|2025-02-05|4|Early Bird|159.96|Confirmed
  3|1|Carol Davis|2025-02-10|1|VIP|99.99|Pending
  ```
- Description: Customer bookings and payment status.

### 5. Participants Data
- File Path: data/participants.txt
- Fields (pipe-delimited, no header):
  - participant_id (int)
  - event_id (int)
  - name (str)
  - email (str)
  - booking_id (int)
  - status (str) [Registered, Confirmed, Attended]
  - registration_date (str) YYYY-MM-DD
- Example Data:
  ```
  1|1|Alice Johnson|alice@email.com|1|Confirmed|2025-02-01
  2|1|Michael Johnson|michael@email.com|1|Confirmed|2025-02-01
  3|2|Bob Williams|bob@email.com|2|Attended|2025-02-05
  ```
- Description: Participants information related to events and bookings.

### 6. Schedules Data
- File Path: data/schedules.txt
- Fields (pipe-delimited, no header):
  - schedule_id (int)
  - event_id (int)
  - session_title (str)
  - session_time (str) YYYY-MM-DD HH:MM
  - duration_minutes (int)
  - speaker (str)
  - venue_id (int)
- Example Data:
  ```
  1|1|Opening Keynote|2025-03-15 09:00|60|John Smith|1
  2|1|Panel Discussion|2025-03-15 10:30|90|Expert Panel|1
  3|2|Headliner Performance|2025-06-20 20:00|120|International Artist|2
  ```
- Description: Scheduled sessions and timeline details for events.

---

# End of Design Specification
