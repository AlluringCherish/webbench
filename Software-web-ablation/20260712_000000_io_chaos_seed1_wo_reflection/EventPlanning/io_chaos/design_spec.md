# EventPlanning Application Design Specification

---

## Section 1: Flask Routes Specification

| Route Path             | Function Name           | HTTP Methods | Template File             | Context Variables                                                                                         |
|------------------------|-------------------------|--------------|---------------------------|----------------------------------------------------------------------------------------------------------|
| /                      | redirect_to_dashboard   | GET          | -                         | - Redirects to `/dashboard`                                                                              |
| /dashboard             | dashboard_page          | GET          | dashboard.html            | `featured_events` (List[Dict]): List of featured event dicts with keys: event_id, event_name, date, location
|                        |                         |              |                           |  (str types for event_name, date, location etc.)                                                         |
| /events                | events_listing          | GET          | events.html               | `events` (List[Dict]): Each dict with keys: event_id (int), event_name (str), category (str), date (str),
|                        |                         |              |                           | time (str), location (str)                                                                                 |
| /events/search          | events_search           | POST         | events.html               | Same as /events, with filtered `events` list                                                             |
| /event/<int:event_id>   | event_details           | GET          | event_details.html        | `event` (Dict): event detail with keys: event_id (int), event_name (str), category (str), date (str), time (str),
|                        |                         |              |                           | location (str), description (str)                                                                         |
| /book_ticket           | ticket_booking          | GET, POST    | ticket_booking.html       | On GET: `events` (List[Dict]) for event dropdown; On POST: `confirmation` (Dict) booking confirmation details|
| /participants          | participants_management | GET, POST    | participants.html         | On GET: `participants` (List[Dict]) with keys: participant_id (int), name (str), email (str), event (str), status (str)
|                        |                         |              |                           | On POST: updated participants list                                                                        |
| /venues                | venues_page             | GET          | venues.html               | `venues` (List[Dict]): venue dicts with keys: venue_id (int), venue_name (str), location (str), capacity (int), amenities (str) |
| /event_schedules       | event_schedules         | GET          | schedules.html            | `schedules` (List[Dict]): schedule_id (int), event_id (int), session_title (str), session_time (str), duration_minutes (int), speaker (str) |
| /bookings             | bookings_summary         | GET          | bookings.html             | `bookings` (List[Dict]): booking dicts with keys booking_id (int), event (str), date (str), ticket_count (int), status (str) |
| /cancel_booking/<int:booking_id> | cancel_booking     | POST         | bookings.html             | Returns updated bookings list                                                                             |

### Notes on HTTP methods and Templates
- Root `/` redirects to `/dashboard`.
- `/book_ticket` supports GET for form display and POST for submitting booking.
- Participants management supports GET for listing and POST for adding/updating.
- Cancel booking is a POST action.


---

## Section 2: HTML Template Specifications

### 1. Dashboard Page
- **Template File:** templates/dashboard.html
- **Page Title:** Event Planning Dashboard
- **Element IDs:**
  - `dashboard-page` (Div): Container
  - `featured-events` (Div): Featured events display
  - `browse-events-button` (Button): Navigate to /events
  - `view-tickets-button` (Button): Navigate to /bookings
  - `venues-button` (Button): Navigate to /venues
- **Context Variables:**
  - `featured_events` (List[Dict]): Each dict has `event_id`, `event_name`, `date`, `location` (all str except event_id int)
- **Navigation Buttons:**
  - `/events` - Browsing events
  - `/bookings` - Viewing tickets
  - `/venues` - Venues information

---

### 2. Events Listing Page
- **Template File:** templates/events.html
- **Page Title:** Events Catalog
- **Element IDs:**
  - `events-page` (Div): Container
  - `event-search-input` (Input): Search events by name, location or date
  - `event-category-filter` (Dropdown): Filter by category (Conference, Concert, Sports, Workshop, Social)
  - `events-grid` (Div): Grid with event cards
  - `view-event-button-{{ event.event_id }}` (Button): View details for each event card (rendered in a loop)
- **Context Variables:**
  - `events` (List[Dict]): Each dict has keys: `event_id` (int), `event_name` (str), `category` (str), `date` (str), `time` (str), `location` (str)
- **Navigation Buttons:**
  - `/dashboard` from navigation bar or other header UI (assumed implemented elsewhere)

- **Rendering Dynamic IDs:**
  ```jinja2
  {% for event in events %}
    <button id="view-event-button-{{ event.event_id }}">View Details</button>
  {% endfor %}
  ```

---

### 3. Event Details Page
- **Template File:** templates/event_details.html
- **Page Title:** Event Details
- **Element IDs:**
  - `event-details-page` (Div): Container
  - `event-title` (H1): Event title
  - `event-date` (Div): Event date and time
  - `event-location` (Div): Event location
  - `event-description` (Div): Event detailed description
  - `book-ticket-button` (Button): Book ticket for this event
- **Context Variables:**
  - `event` (Dict): keys: `event_id` (int), `event_name` (str), `date` (str), `time` (str), `location` (str), `description` (str)
- **Navigation Buttons:**
  - `/events` to return to listing

---

### 4. Ticket Booking Page
- **Template File:** templates/ticket_booking.html
- **Page Title:** Book Your Tickets
- **Element IDs:**
  - `ticket-booking-page` (Div): Container
  - `select-event-dropdown` (Dropdown): Select event (uses `events` list)
  - `ticket-quantity-input` (Input number): Number of tickets
  - `ticket-type-select` (Dropdown): Ticket type selection (General, VIP, Early Bird)
  - `book-now-button` (Button): Submit booking
  - `booking-confirmation` (Div): Show confirmation details after booking
- **Context Variables:**
  - On GET: `events` (List[Dict]) with event_id and event_name
  - On POST: `confirmation` (Dict) with booking details: confirmation_number, event_name, ticket_count, ticket_type
- **Navigation Buttons:**
  - `/dashboard` or `/events`

---

### 5. Participants Management Page
- **Template File:** templates/participants.html
- **Page Title:** Participants Management
- **Element IDs:**
  - `participants-page` (Div): Container
  - `participants-table` (Table): Show participants data columns (name, email, event, status)
  - `add-participant-button` (Button): Add participant
  - `search-participant-input` (Input): Search by name/email
  - `participant-status-filter` (Dropdown): Filter by status (Registered, Confirmed, Attended)
- **Context Variables:**
  - `participants` (List[Dict]) with keys: participant_id (int), name (str), email (str), event (str), status (str)
- **Navigation Buttons:**
  - `/dashboard`

---

### 6. Venue Information Page
- **Template File:** templates/venues.html
- **Page Title:** Venues
- **Element IDs:**
  - `venues-page` (Div): Container
  - `venues-grid` (Div): Grid for venue cards
  - `venue-search-input` (Input): Search venues by name/location
  - `venue-capacity-filter` (Dropdown): Filter venues by capacity (Small, Medium, Large)
  - `view-venue-details-{{ venue.venue_id }}` (Button): View venue details button (dynamic id in loop)
- **Context Variables:**
  - `venues` (List[Dict]) with keys: venue_id (int), venue_name (str), location (str), capacity (int), amenities (str)
- **Navigation Buttons:**
  - `/dashboard`

- **Rendering Dynamic IDs:**
  ```jinja2
  {% for venue in venues %}
    <button id="view-venue-details-{{ venue.venue_id }}">View Details</button>
  {% endfor %}
  ```

---

### 7. Event Schedules Page
- **Template File:** templates/schedules.html
- **Page Title:** Event Schedules
- **Element IDs:**
  - `schedules-page` (Div): Container
  - `schedules-timeline` (Div): Timeline view of events and sessions
  - `schedule-filter-date` (Input date): Filter schedules by date
  - `schedule-filter-event` (Dropdown): Filter schedules by event
  - `export-schedule-button` (Button): Export schedule data
- **Context Variables:**
  - `schedules` (List[Dict]) with keys: schedule_id (int), event_id (int), session_title (str), session_time (str), duration_minutes (int), speaker (str)
- **Navigation Buttons:**
  - `/dashboard`

---

### 8. Bookings Summary Page
- **Template File:** templates/bookings.html
- **Page Title:** My Bookings
- **Element IDs:**
  - `bookings-page` (Div): Container
  - `bookings-table` (Table): Booking info columns (event, date, ticket count, status)
  - `booking-search-input` (Input): Search bookings by event name or booking ID
  - `cancel-booking-button-{{ booking.booking_id }}` (Button): Cancel each booking (dynamic id)
  - `back-to-dashboard` (Button): Navigate to dashboard
- **Context Variables:**
  - `bookings` (List[Dict]) with keys: booking_id (int), event (str), date (str), ticket_count (int), status (str)
- **Navigation Buttons:**
  - `/dashboard`

- **Rendering Dynamic IDs:**
  ```jinja2
  {% for booking in bookings %}
    <button id="cancel-booking-button-{{ booking.booking_id }}">Cancel</button>
  {% endfor %}
  ```

---

## Section 3: Data File Schemas

### 1. Events Data file
- **File Path:** data/events.txt
- **Field Order:**
  `event_id|event_name|category|date|time|location|description|venue_id|capacity`
- **Description:** Contains all events with their details including venue and capacity.
- **Example Data Rows:**
  ```
  1|Tech Conference 2025|Conference|2025-03-15|09:00|Convention Center, San Francisco|Annual technology conference discussing latest innovations|1|500
  2|Summer Music Festival|Concert|2025-06-20|18:00|Central Park, New York|Three-day music festival with international artists|2|5000
  3|Marathon Championship|Sports|2025-04-10|07:00|Downtown Loop, Chicago|Annual city marathon event for all skill levels|3|1000
  ```

### 2. Venues Data file
- **File Path:** data/venues.txt
- **Field Order:**
  `venue_id|venue_name|location|capacity|amenities|contact`
- **Description:** Venue details including amenities and contact information.
- **Example Data Rows:**
  ```
  1|Convention Center|San Francisco, CA|500|WiFi, Parking, Catering|contact@convention.com
  2|Central Park|New York, NY|5000|Outdoor Space, Restrooms, Food Vendors|info@centralparkevents.org
  3|Downtown Loop|Chicago, IL|1000|Paved Surface, Water Stations, Medical Support|events@downtown.com
  ```

### 3. Tickets Data file
- **File Path:** data/tickets.txt
- **Field Order:**
  `ticket_id|event_id|ticket_type|price|available_count|sold_count`
- **Description:** Ticket types and availability per event.
- **Example Data Rows:**
  ```
  1|1|General|49.99|500|150
  2|1|VIP|99.99|100|45
  3|2|Early Bird|39.99|1000|750
  ```

### 4. Bookings Data file
- **File Path:** data/bookings.txt
- **Field Order:**
  `booking_id|event_id|customer_name|booking_date|ticket_count|ticket_type|total_amount|status`
- **Description:** Records of bookings made by customers.
- **Example Data Rows:**
  ```
  1|1|Alice Johnson|2025-02-01|2|General|99.98|Confirmed
  2|2|Bob Williams|2025-02-05|4|Early Bird|159.96|Confirmed
  3|1|Carol Davis|2025-02-10|1|VIP|99.99|Pending
  ```

### 5. Participants Data file
- **File Path:** data/participants.txt
- **Field Order:**
  `participant_id|event_id|name|email|booking_id|status|registration_date`
- **Description:** Participant details linked to events and bookings.
- **Example Data Rows:**
  ```
  1|1|Alice Johnson|alice@email.com|1|Confirmed|2025-02-01
  2|1|Michael Johnson|michael@email.com|1|Confirmed|2025-02-01
  3|2|Bob Williams|bob@email.com|2|Attended|2025-02-05
  ```

### 6. Schedules Data file
- **File Path:** data/schedules.txt
- **Field Order:**
  `schedule_id|event_id|session_title|session_time|duration_minutes|speaker|venue_id`
- **Description:** Event session and schedule information.
- **Example Data Rows:**
  ```
  1|1|Opening Keynote|2025-03-15 09:00|60|John Smith|1
  2|1|Panel Discussion|2025-03-15 10:30|90|Expert Panel|1
  3|2|Headliner Performance|2025-06-20 20:00|120|International Artist|2
  ```

---

# End of design_spec.md
