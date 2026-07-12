# EventPlanning Application Design Specification

---

## Section 1: Flask Routes Specification

| Route Path           | Function Name          | HTTP Methods   | Template File           | Context Variables Description                                           |
|----------------------|------------------------|----------------|-------------------------|------------------------------------------------------------------------|
| /                    | root_redirect           | GET            | None                    | None, redirects to `/dashboard`                                        |
| /dashboard           | dashboard_page          | GET            | dashboard.html          | featured_events: List of dicts, each with keys: event_id (int), event_name (str), date (str), location (str) |
| /events              | events_listing_page     | GET            | events.html             | events: List of dicts with keys: event_id (int), event_name, category, date (YYYY-MM-DD), time (HH:MM), location, description, venue_id (int), capacity (int) |
| /events              | events_search_filter    | POST           | events.html             | events: filtered list same as above based on search and category       |
| /event/<int:event_id>| event_details_page      | GET            | event_details.html      | event: dict as above for single event details                         |
| /book_ticket         | ticket_booking_page     | GET, POST      | book_ticket.html        | GET: events: list (event_id, event_name)
POST: booking_confirmation: dict with keys booking_id, event_name, ticket_count, total_amount (float), status (str) |
| /participants        | participants_page       | GET            | participants.html       | participants: List of dicts with participant_id, event_id, name, email, booking_id, status, registration_date
status_options: List[str] for filter dropdown |
| /participants/add    | add_participant         | POST           | redirects to /participants | None                                                                    |
| /venues              | venues_page             | GET            | venues.html             | venues: List of dicts with keys: venue_id (int), venue_name, location, capacity (int), amenities (str), contact (str) |
| /event_schedules     | event_schedules_page    | GET            | schedules.html          | schedules: List of dicts with schedule_id, event_id, session_title, session_time (YYYY-MM-DD HH:MM), duration_minutes (int), speaker, venue_id
events: list (event_id, event_name) for filter dropdown |
| /bookings           | bookings_summary_page   | GET            | bookings.html           | bookings: List of dicts with booking_id, event_id, event_name, booking_date, ticket_count, ticket_type, total_amount, status |
| /bookings/cancel/<int:booking_id> | cancel_booking  | POST           | redirects to /bookings    | None                                                                    |

---

## Section 2: HTML Template Specifications

### 1. Dashboard Page
- Template Path: `templates/dashboard.html`
- Page Title: "Event Planning Dashboard" (both <title> and <h1>)
- Element IDs:
  - dashboard-page (Div) - container for the dashboard
  - featured-events (Div) - displays featured event recommendations
  - browse-events-button (Button) - navigates to `/events`
  - view-tickets-button (Button) - navigates to `/bookings`
  - venues-button (Button) - navigates to `/venues`
- Context Variables:
  - featured_events: List of dicts; each dict: event_id (int), event_name (str), date (str), location (str)
- Navigation Buttons:
  - browse-events-button -> url_for('events_listing_page')
  - view-tickets-button -> url_for('bookings_summary_page')
  - venues-button -> url_for('venues_page')

---

### 2. Events Listing Page
- Template Path: `templates/events.html`
- Page Title: "Events Catalog" (both <title> and <h1>)
- Element IDs:
  - events-page (Div) - container
  - event-search-input (Input) - search by name, location, date
  - event-category-filter (Dropdown) - filter by category (Conference, Concert, Sports, Workshop, Social)
  - events-grid (Div) - grid of event cards
  - view-event-button-{event_id} (Button) - view details for each event, dynamic IDs
- Context Variables:
  - events: list of dicts (event_id, event_name, category, date, time, location, description, venue_id, capacity)
- Navigation Buttons:
  - None, navigation from dashboard or individual event details
- Dynamic IDs:
  - Render event cards in Jinja2 loop:
    ```jinja
    {% for event in events %}
      <button id="view-event-button-{{ event.event_id }}" ...>View</button>
    {% endfor %}
    ```

---

### 3. Event Details Page
- Template Path: `templates/event_details.html`
- Page Title: "Event Details" (both <title> and <h1> to match event-title content)
- Element IDs:
  - event-details-page (Div) - container
  - event-title (H1) - event name
  - event-date (Div) - date and time
  - event-location (Div) - location
  - event-description (Div) - full description
  - book-ticket-button (Button) - proceed to ticket booking
- Context Variables:
  - event: dict with keys as above
- Navigation Buttons:
  - book-ticket-button -> url_for('ticket_booking_page') with pre-selected event id handled via query param or session

---

### 4. Ticket Booking Page
- Template Path: `templates/book_ticket.html`
- Page Title: "Book Your Tickets" (both <title> and <h1>)
- Element IDs:
  - ticket-booking-page (Div) - container
  - select-event-dropdown (Dropdown) - select event
  - ticket-quantity-input (Input number) - enter number tickets
  - ticket-type-select (Dropdown) - ticket type (General, VIP, Early Bird)
  - book-now-button (Button) - submit booking
  - booking-confirmation (Div) - show booking confirmation after POST
- Context Variables:
  - GET: events: list of dicts (event_id, event_name)
  - POST (after submission): booking_confirmation: dict with booking_id (int), event_name (str), ticket_count (int), total_amount (float), status (str)
- Navigation Buttons:
  - None explicit, typically user returns via navigation

---

### 5. Participants Management Page
- Template Path: `templates/participants.html`
- Page Title: "Participants Management" (both <title> and <h1>)
- Element IDs:
  - participants-page (Div) - container
  - participants-table (Table) - shows participant rows with columns: name, email, event, status
  - add-participant-button (Button) - to add new participant
  - search-participant-input (Input) - search by name or email
  - participant-status-filter (Dropdown) - filter by status (Registered, Confirmed, Attended)
- Context Variables:
  - participants: list of dicts (participant_id, event_id, name, email, booking_id, status, registration_date)
  - status_options: list of strings for dropdown
- Navigation Buttons:
  - add-participant-button posts or redirects to add participant functionality

---

### 6. Venue Information Page
- Template Path: `templates/venues.html`
- Page Title: "Venues" (both <title> and <h1>)
- Element IDs:
  - venues-page (Div) - container
  - venues-grid (Div) - cards for each venue
  - venue-search-input (Input) - filter by name/location
  - venue-capacity-filter (Dropdown) - filter by capacity (Small, Medium, Large)
  - view-venue-details-{venue_id} (Button) - each venue's details, dynamic IDs
- Context Variables:
  - venues: list of dicts (venue_id, venue_name, location, capacity, amenities, contact)
- Navigation Buttons:
  - None explicit, navigation typically on dashboard or elsewhere
- Dynamic IDs:
  - Render venue cards in Jinja2 loop:
    ```jinja
    {% for venue in venues %}
      <button id="view-venue-details-{{ venue.venue_id }}" ...>View Details</button>
    {% endfor %}
    ```

---

### 7. Event Schedules Page
- Template Path: `templates/schedules.html`
- Page Title: "Event Schedules" (both <title> and <h1>)
- Element IDs:
  - schedules-page (Div) - container
  - schedules-timeline (Div) - timeline view
  - schedule-filter-date (Input date) - filter by date
  - schedule-filter-event (Dropdown) - filter by event
  - export-schedule-button (Button) - export schedules
- Context Variables:
  - schedules: list of dicts (schedule_id, event_id, session_title, session_time, duration_minutes, speaker, venue_id)
  - events: list of dicts (event_id, event_name) for event filter dropdown
- Navigation Buttons:
  - None explicit

---

### 8. Bookings Summary Page
- Template Path: `templates/bookings.html`
- Page Title: "My Bookings" (both <title> and <h1>)
- Element IDs:
  - bookings-page (Div) - container
  - bookings-table (Table) - rows with event, date, ticket count, status
  - booking-search-input (Input) - search bookings by event name or booking ID
  - cancel-booking-button-{booking_id} (Button) - cancel specific booking, dynamic IDs
  - back-to-dashboard (Button) - navigate to dashboard
- Context Variables:
  - bookings: list of dicts (booking_id, event_id, event_name, booking_date, ticket_count, ticket_type, total_amount, status)
- Navigation Buttons:
  - back-to-dashboard -> url_for('dashboard_page')
- Dynamic IDs:
  - In Jinja2 loop:
    ```jinja
    {% for booking in bookings %}
      <button id="cancel-booking-button-{{ booking.booking_id }}">Cancel</button>
    {% endfor %}
    ```

---

## Section 3: Data File Schemas

### 1. Events Data
- File Path: `data/events.txt`
- Fields (pipe-delimited):
  - event_id (int)
  - event_name (str)
  - category (str) [Conference, Concert, Sports, Workshop, Social]
  - date (str, YYYY-MM-DD)
  - time (str, HH:MM)
  - location (str)
  - description (str)
  - venue_id (int)
  - capacity (int)
- Description: Stores all event details.
- Example Rows:
  ```
  1|Tech Conference 2025|Conference|2025-03-15|09:00|Convention Center, San Francisco|Annual technology conference discussing latest innovations|1|500
  2|Summer Music Festival|Concert|2025-06-20|18:00|Central Park, New York|Three-day music festival with international artists|2|5000
  3|Marathon Championship|Sports|2025-04-10|07:00|Downtown Loop, Chicago|Annual city marathon event for all skill levels|3|1000
  ```

---

### 2. Venues Data
- File Path: `data/venues.txt`
- Fields:
  - venue_id (int)
  - venue_name (str)
  - location (str)
  - capacity (int)
  - amenities (str) comma separated
  - contact (str) email or info
- Description: Stores venue information details.
- Example Rows:
  ```
  1|Convention Center|San Francisco, CA|500|WiFi, Parking, Catering|contact@convention.com
  2|Central Park|New York, NY|5000|Outdoor Space, Restrooms, Food Vendors|info@centralparkevents.org
  3|Downtown Loop|Chicago, IL|1000|Paved Surface, Water Stations, Medical Support|events@downtown.com
  ```

---

### 3. Tickets Data
- File Path: `data/tickets.txt`
- Fields:
  - ticket_id (int)
  - event_id (int)
  - ticket_type (str) [General, VIP, Early Bird]
  - price (float)
  - available_count (int)
  - sold_count (int)
- Description: Details of ticket types and availability.
- Example Rows:
  ```
  1|1|General|49.99|500|150
  2|1|VIP|99.99|100|45
  3|2|Early Bird|39.99|1000|750
  ```

---

### 4. Bookings Data
- File Path: `data/bookings.txt`
- Fields:
  - booking_id (int)
  - event_id (int)
  - customer_name (str)
  - booking_date (str, YYYY-MM-DD)
  - ticket_count (int)
  - ticket_type (str)
  - total_amount (float)
  - status (str) [Confirmed, Pending, Cancelled]
- Description: Stores booking records.
- Example Rows:
  ```
  1|1|Alice Johnson|2025-02-01|2|General|99.98|Confirmed
  2|2|Bob Williams|2025-02-05|4|Early Bird|159.96|Confirmed
  3|1|Carol Davis|2025-02-10|1|VIP|99.99|Pending
  ```

---

### 5. Participants Data
- File Path: `data/participants.txt`
- Fields:
  - participant_id (int)
  - event_id (int)
  - name (str)
  - email (str)
  - booking_id (int)
  - status (str) [Registered, Confirmed, Attended]
  - registration_date (str, YYYY-MM-DD)
- Description: Stores participants linked to bookings.
- Example Rows:
  ```
  1|1|Alice Johnson|alice@email.com|1|Confirmed|2025-02-01
  2|1|Michael Johnson|michael@email.com|1|Confirmed|2025-02-01
  3|2|Bob Williams|bob@email.com|2|Attended|2025-02-05
  ```

---

### 6. Schedules Data
- File Path: `data/schedules.txt`
- Fields:
  - schedule_id (int)
  - event_id (int)
  - session_title (str)
  - session_time (str, YYYY-MM-DD HH:MM)
  - duration_minutes (int)
  - speaker (str)
  - venue_id (int)
- Description: Stores session and schedule information for events.
- Example Rows:
  ```
  1|1|Opening Keynote|2025-03-15 09:00|60|John Smith|1
  2|1|Panel Discussion|2025-03-15 10:30|90|Expert Panel|1
  3|2|Headliner Performance|2025-06-20 20:00|120|International Artist|2
  ```

---

# End of Design Specification
