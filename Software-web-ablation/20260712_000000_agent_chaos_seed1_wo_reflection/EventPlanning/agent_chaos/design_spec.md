# Design Specification Document for 'EventPlanning' Web Application

---

## 1. Flask Routes Specification

| Route Path              | Handler Function        | HTTP Method | HTML Template        | Context Variables Passed to Template                                                     |
|-------------------------|-------------------------|-------------|---------------------|-------------------------------------------------------------------------------------------|
| `/`                     | redirect_to_dashboard    | GET         | N/A (Redirect)       | None                                                                                      |
| `/dashboard`            | dashboard_page          | GET         | dashboard.html       | featured_events: List[Dict{event_id:int, event_name:str, date:str, location:str}],
|                         |                         |             |                     | user_navigation: Dict[str, str] (browse_events, view_tickets, venues)                      |
| `/events`               | events_listing_page     | GET         | events.html          | events: List[Dict{event_id:int, event_name:str, category:str, date:str, location:str}],
|                         |                         |             |                     | categories: List[str] (Conference, Concert, Sports, Workshop, Social)                      |
| `/event/<int:event_id>` | event_details_page      | GET         | event_details.html   | event: Dict{event_id:int, event_name:str, category:str, date:str, time:str, location:str,
|                         |                         |             |                     | description:str, venue_id:int, capacity:int}                                              |
| `/book_ticket`          | ticket_booking_page     | GET         | book_ticket.html     | events: List[Dict{event_id:int, event_name:str}]                                          |
| `/book_ticket`          | process_ticket_booking  | POST        | book_ticket.html     | booking_confirmation: Dict{booking_id:int, event_name:str, ticket_count:int, ticket_type:str, total_amount:float, status:str} OR error message string |
| `/participants`         | participants_page       | GET         | participants.html    | participants: List[Dict{participant_id:int, event_id:int, name:str, email:str, booking_id:int, status:str, registration_date:str}],
|                         |                         |             |                     | filter_options: Dict[str, List[str]] (statuses: Registered, Confirmed, Attended)           |
| `/add_participant`      | add_participant         | POST        | participants.html    | participants: Updated List (same structure as GET) OR error message string                 |
| `/venues`               | venues_page             | GET         | venues.html          | venues: List[Dict{venue_id:int, venue_name:str, location:str, capacity:int, amenities:str}]|
| `/venue/<int:venue_id>` | venue_details_page      | GET         | venue_details.html   | venue: Dict{venue_id:int, venue_name:str, location:str, capacity:int, amenities:str, contact:str} |
| `/schedules`            | schedules_page          | GET         | schedules.html       | schedules: List[Dict{schedule_id:int, event_id:int, session_title:str, session_time:str,
|                         |                         |             |                     | duration_minutes:int, speaker:str, venue_id:int}],
|                         |                         |             |                     | events: List[Dict{event_id:int, event_name:str}]                                           |
| `/bookings`             | bookings_page           | GET         | bookings.html        | bookings: List[Dict{booking_id:int, event_id:int, customer_name:str, booking_date:str,
|                         |                         |             |                     | ticket_count:int, ticket_type:str, total_amount:float, status:str}                         |
| `/cancel_booking/<int:booking_id>` | cancel_booking | POST        | bookings.html        | bookings: Updated List (same as GET) OR error message string                               |
| `/search_events`        | search_events           | POST        | events.html          | events: Filtered List (same structure as GET) based on search/filter criteria              |
| `/search_participants`  | search_participants     | POST        | participants.html    | participants: Filtered List (same structure as GET) based on search/filter criteria        |


---

## 2. HTML Template Specifications

### 1. Dashboard Page
- **Template File Path:** templates/dashboard.html
- **Page Title Text:** "Event Planning Dashboard"
- **Element IDs:**
  - `dashboard-page` (Div): Main container for the dashboard.
  - `featured-events` (Div): Section for featured event recommendations.
  - `browse-events-button` (Button): Navigates to events listing page.
  - `view-tickets-button` (Button): Navigates to bookings summary page.
  - `venues-button` (Button): Navigates to venues page.
- **Context Variables:**
  - `featured_events`: List of dictionaries each containing:
    - `event_id` (int)
    - `event_name` (str)
    - `date` (str)
    - `location` (str)
- **Navigation Buttons:**
  - `browse-events-button` => `url_for('events_listing_page')`
  - `view-tickets-button` => `url_for('bookings_page')`
  - `venues-button` => `url_for('venues_page')`

### 2. Events Listing Page
- **Template File Path:** templates/events.html
- **Page Title Text:** "Events Catalog"
- **Element IDs:**
  - `events-page` (Div): Container for events list.
  - `event-search-input` (Input): Search field.
  - `event-category-filter` (Dropdown): Filter for event category.
  - `events-grid` (Div): Grid with event cards.
  - `view-event-button-{{ event.event_id }}` (Button): Button to view details for each event.
- **Context Variables:**
  - `events`: List of event dicts with `event_id`, `event_name`, `category`, `date`, `location`.
  - `categories`: List of string categories.
- **Navigation Buttons:**
  - None explicitly defined (assumed standard nav bar links if any).
- **Dynamic Element ID Pattern:**
  - `view-event-button-{{ event.event_id }}`
    - Use Jinja2 `{% for event in events %} <button id="view-event-button-{{ event.event_id }}"> ... </button> {% endfor %}`

### 3. Event Details Page
- **Template File Path:** templates/event_details.html
- **Page Title Text:** "Event Details"
- **Element IDs:**
  - `event-details-page` (Div): Container for event details.
  - `event-title` (H1): Event name.
  - `event-date` (Div): Date and time.
  - `event-location` (Div): Location.
  - `event-description` (Div): Description.
  - `book-ticket-button` (Button): To book tickets for this event.
- **Context Variables:**
  - `event`: Dict with `event_id` (int), `event_name` (str), `category` (str), `date` (str), `time` (str), `location` (str), `description` (str), `venue_id` (int), `capacity` (int)
- **Navigation Buttons:**
  - `book-ticket-button` => `url_for('ticket_booking_page')` with event_id param passed via form or query

### 4. Ticket Booking Page
- **Template File Path:** templates/book_ticket.html
- **Page Title Text:** "Book Your Tickets"
- **Element IDs:**
  - `ticket-booking-page` (Div): Main container.
  - `select-event-dropdown` (Dropdown): Select event.
  - `ticket-quantity-input` (Input, number): Number of tickets.
  - `ticket-type-select` (Dropdown): Ticket type selection.
  - `book-now-button` (Button): Submit booking.
  - `booking-confirmation` (Div): Shows confirmation details after successful booking.
- **Context Variables:**
  - `events`: List of events with `event_id` and `event_name` only.
  - `booking_confirmation`: Optional (after POST), Dict with booking details.
- **Navigation Buttons:**
  - None explicitly stated.

### 5. Participants Management Page
- **Template File Path:** templates/participants.html
- **Page Title Text:** "Participants Management"
- **Element IDs:**
  - `participants-page` (Div): Main container.
  - `participants-table` (Table): Showing participant details.
  - `add-participant-button` (Button): To add new participant.
  - `search-participant-input` (Input): Search participants.
  - `participant-status-filter` (Dropdown): Filter participants by status.
- **Context Variables:**
  - `participants`: List of dicts with `participant_id` (int), `event_id` (int), `name` (str), `email` (str), `booking_id` (int), `status` (str), `registration_date` (str)
  - `filter_options`: Dict with statuses list: ["Registered", "Confirmed", "Attended"]
- **Navigation Buttons:**
  - None explicitly stated.

### 6. Venue Information Page
- **Template File Path:** templates/venues.html
- **Page Title Text:** "Venues"
- **Element IDs:**
  - `venues-page` (Div): Container.
  - `venues-grid` (Div): Venue cards display.
  - `venue-search-input` (Input): Search field.
  - `venue-capacity-filter` (Dropdown): Capacity filter.
  - `view-venue-details-{{ venue.venue_id }}` (Button): Button to view venue details.
- **Context Variables:**
  - `venues`: List of dicts with `venue_id` (int), `venue_name` (str), `location` (str), `capacity` (int), `amenities` (str)
- **Navigation Buttons:**
  - None explicitly stated.
- **Dynamic Element ID Pattern:**
  - `view-venue-details-{{ venue.venue_id }}`
    - Use Jinja2 `{% for venue in venues %} <button id="view-venue-details-{{ venue.venue_id }}"> ... </button> {% endfor %}`

### 7. Event Schedules Page
- **Template File Path:** templates/schedules.html
- **Page Title Text:** "Event Schedules"
- **Element IDs:**
  - `schedules-page` (Div): Main container.
  - `schedules-timeline` (Div): Timeline view.
  - `schedule-filter-date` (Input, date): Filter schedules by date.
  - `schedule-filter-event` (Dropdown): Filter schedules by event.
  - `export-schedule-button` (Button): Export schedule data.
- **Context Variables:**
  - `schedules`: List of dicts with schedule details.
  - `events`: List of dicts with event_id and event_name.
- **Navigation Buttons:**
  - None explicitly stated.

### 8. Bookings Summary Page
- **Template File Path:** templates/bookings.html
- **Page Title Text:** "My Bookings"
- **Element IDs:**
  - `bookings-page` (Div): Container.
  - `bookings-table` (Table): Displays booking info.
  - `booking-search-input` (Input): Search bookings.
  - `cancel-booking-button-{{ booking.booking_id }}` (Button): Cancel booking button.
  - `back-to-dashboard` (Button): Navigate back to dashboard.
- **Context Variables:**
  - `bookings`: List of dicts with booking_id, event_id, customer_name, booking_date, ticket_count, ticket_type, total_amount, status
- **Navigation Buttons:**
  - `back-to-dashboard` => `url_for('dashboard_page')`
- **Dynamic Element ID Pattern:**
  - `cancel-booking-button-{{ booking.booking_id }}`
    - Use Jinja2 `{% for booking in bookings %} <button id="cancel-booking-button-{{ booking.booking_id }}"> ... </button> {% endfor %}`

---

## 3. Data File Schemas

### 1. Events Data
- **File Path and Name:** data/events.txt
- **Field Order:**
  ```
  event_id|event_name|category|date|time|location|description|venue_id|capacity
  ```
- **Description:** Stores all event records with details including name, schedule, location, and capacity.
- **Example Data Rows:**
  ```
  1|Tech Conference 2025|Conference|2025-03-15|09:00|Convention Center, San Francisco|Annual technology conference discussing latest innovations|1|500
  2|Summer Music Festival|Concert|2025-06-20|18:00|Central Park, New York|Three-day music festival with international artists|2|5000
  3|Marathon Championship|Sports|2025-04-10|07:00|Downtown Loop, Chicago|Annual city marathon event for all skill levels|3|1000
  ```

### 2. Venues Data
- **File Path and Name:** data/venues.txt
- **Field Order:**
  ```
  venue_id|venue_name|location|capacity|amenities|contact
  ```
- **Description:** Stores venue details including amenities and contact info.
- **Example Data Rows:**
  ```
  1|Convention Center|San Francisco, CA|500|WiFi, Parking, Catering|contact@convention.com
  2|Central Park|New York, NY|5000|Outdoor Space, Restrooms, Food Vendors|info@centralparkevents.org
  3|Downtown Loop|Chicago, IL|1000|Paved Surface, Water Stations, Medical Support|events@downtown.com
  ```

### 3. Tickets Data
- **File Path and Name:** data/tickets.txt
- **Field Order:**
  ```
  ticket_id|event_id|ticket_type|price|available_count|sold_count
  ```
- **Description:** Stores ticket types for events with pricing and availability.
- **Example Data Rows:**
  ```
  1|1|General|49.99|500|150
  2|1|VIP|99.99|100|45
  3|2|Early Bird|39.99|1000|750
  ```

### 4. Bookings Data
- **File Path and Name:** data/bookings.txt
- **Field Order:**
  ```
  booking_id|event_id|customer_name|booking_date|ticket_count|ticket_type|total_amount|status
  ```
- **Description:** Stores all bookings with customer and status information.
- **Example Data Rows:**
  ```
  1|1|Alice Johnson|2025-02-01|2|General|99.98|Confirmed
  2|2|Bob Williams|2025-02-05|4|Early Bird|159.96|Confirmed
  3|1|Carol Davis|2025-02-10|1|VIP|99.99|Pending
  ```

### 5. Participants Data
- **File Path and Name:** data/participants.txt
- **Field Order:**
  ```
  participant_id|event_id|name|email|booking_id|status|registration_date
  ```
- **Description:** Stores participant details linked to events and bookings.
- **Example Data Rows:**
  ```
  1|1|Alice Johnson|alice@email.com|1|Confirmed|2025-02-01
  2|1|Michael Johnson|michael@email.com|1|Confirmed|2025-02-01
  3|2|Bob Williams|bob@email.com|2|Attended|2025-02-05
  ```

### 6. Schedules Data
- **File Path and Name:** data/schedules.txt
- **Field Order:**
  ```
  schedule_id|event_id|session_title|session_time|duration_minutes|speaker|venue_id
  ```
- **Description:** Stores event session schedules with timing and speaker info.
- **Example Data Rows:**
  ```
  1|1|Opening Keynote|2025-03-15 09:00|60|John Smith|1
  2|1|Panel Discussion|2025-03-15 10:30|90|Expert Panel|1
  3|2|Headliner Performance|2025-06-20 20:00|120|International Artist|2
  ```
