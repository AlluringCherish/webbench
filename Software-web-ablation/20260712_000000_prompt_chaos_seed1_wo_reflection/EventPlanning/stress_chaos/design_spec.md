# Design Specification Document for EventPlanning Web Application

---

## Section 1: Flask Routes Specification

| Route Path             | Function Name           | HTTP Methods     | Template File              | Context Variables                                                                                 |
|------------------------|-------------------------|------------------|----------------------------|-------------------------------------------------------------------------------------------------|
| /                      | root_redirect           | GET              | None (redirect)             | None                                                                                            |
| /dashboard             | dashboard_page          | GET              | dashboard.html             | featured_events: List[Dict] (each dict with event_id:int, event_name:str, date:str, etc.)         |
| /events                | events_page             | GET              | events.html                | events: List[Dict] (event_id:int, event_name:str, category:str, date:str, location:str)          |
| /events/search         | events_search           | POST             | events.html                | events: List[Dict] (filtered events list same structure as above)                               |
| /event/<int:event_id>  | event_details           | GET              | event_details.html         | event: Dict (event_id:int, event_name:str, category:str, date:str, time:str, location:str,
|                        |                         |                  |                            | description:str, venue_id:int, capacity:int)                                                   |
| /book_ticket           | book_ticket_page        | GET              | book_ticket.html           | events: List[Dict] (event_id:int, event_name:str)                                                |
| /book_ticket           | book_ticket_submit      | POST             | book_ticket.html           | booking_confirmation: Dict (confirmation message details) or error message                      |
| /participants          | participants_page       | GET              | participants.html          | participants: List[Dict] (participant_id:int, event_id:int, name:str, email:str, booking_id:int, status:str, registration_date:str) |
| /participants/add      | add_participant         | POST             | participants.html          | success or error message (redirect or inline)                                                  |
| /venues                | venues_page             | GET              | venues.html                | venues: List[Dict] (venue_id:int, venue_name:str, location:str, capacity:int, amenities:str)      |
| /venue/<int:venue_id>  | venue_details           | GET              | venue_details.html (if applicable)  | venue: Dict (venue_id:int, venue_name:str, location:str, capacity:int, amenities:str, contact:str) |
| /schedules             | schedules_page          | GET              | schedules.html             | schedules: List[Dict] (schedule_id:int, event_id:int, session_title:str, session_time:str, duration_minutes:int, speaker:str, venue_id:int) |
| /schedules/filter      | schedules_filter        | POST             | schedules.html             | schedules: List[Dict] (filtered as per date/event)                                              |
| /bookings              | bookings_page           | GET              | bookings.html              | bookings: List[Dict] (booking_id:int, event_id:int, customer_name:str, booking_date:str, ticket_count:int, ticket_type:str, total_amount:float, status:str) |
| /booking/cancel/<int:booking_id> | cancel_booking  | POST             | bookings.html              | success or error message, updated bookings list                                                |

Notes:
- Root ('/') redirects to '/dashboard'.
- Booking and participant addition are handled via POST routes.
- Filtering and searching use POST when applicable.
- Some detailed views for event and venue details are via parameterized routes.

## Section 2: HTML Template Specifications

### 1. Dashboard Page
- Template file path: templates/dashboard.html
- Page title: <title>Event Planning Dashboard</title>
- Header: <h1 id="dashboard-page">Event Planning Dashboard</h1>
- Element IDs:
  - dashboard-page (Div): Container for dashboard page
  - featured-events (Div): Display featured event recommendations
  - browse-events-button (Button): Navigate to events listing (/events)
  - view-tickets-button (Button): Navigate to bookings page (/bookings)
  - venues-button (Button): Navigate to venues page (/venues)
- Context variables:
  - featured_events: List of dicts with key details to display featured events
- Navigation buttons:
  - browse-events-button -> url_for('events_page')
  - view-tickets-button -> url_for('bookings_page')
  - venues-button -> url_for('venues_page')

### 2. Events Listing Page
- Template file path: templates/events.html
- Page title: <title>Events Catalog</title>
- Header: <h1 id="events-page">Events Catalog</h1>
- Element IDs:
  - events-page (Div): Container for page
  - event-search-input (Input): Search input for name/location/date
  - event-category-filter (Dropdown): Filter by category
  - events-grid (Div): Grid of event cards
  - view-event-button-{event_id} (Button): Dynamic button for details per event
- Context variables:
  - events: List of event dicts (event_id, event_name, category, date, location)
- Navigation:
  - None specific except possibly back to dashboard
- Dynamic element ID handling:
  - In Jinja2 loop over events:
    ```jinja
    <button id="view-event-button-{{ event.event_id }}">View Details</button>
    ```

### 3. Event Details Page
- Template file path: templates/event_details.html
- Page title: <title>Event Details</title>
- Header: <h1 id="event-title">{{ event.event_name }}</h1>
- Element IDs:
  - event-details-page (Div): Container
  - event-title (H1): Event title
  - event-date (Div): Date and time
  - event-location (Div): Location
  - event-description (Div): Event description
  - book-ticket-button (Button): Book ticket for event
- Context variables:
  - event: Dict with fields (event_id, event_name, category, date, time, location, description, venue_id, capacity)
- Navigation:
  - book-ticket-button -> url_for('book_ticket_page') with event preselected by passing event_id (via query param or form)

### 4. Ticket Booking Page
- Template file path: templates/book_ticket.html
- Page title: <title>Book Your Tickets</title>
- Header: <h1 id="ticket-booking-page">Book Your Tickets</h1>
- Element IDs:
  - ticket-booking-page (Div): Container
  - select-event-dropdown (Dropdown): Select event
  - ticket-quantity-input (Input Number): Enter number of tickets
  - ticket-type-select (Dropdown): Select ticket type
  - book-now-button (Button): Proceed booking
  - booking-confirmation (Div): Show confirmation details
- Context variables:
  - events: List of dicts with event_id, event_name
  - booking_confirmation: Dict with confirmation info or None
- Navigation:
  - None specific required

### 5. Participants Management Page
- Template file path: templates/participants.html
- Page title: <title>Participants Management</title>
- Header: <h1 id="participants-page">Participants Management</h1>
- Element IDs:
  - participants-page (Div): Container
  - participants-table (Table): Table of participants
  - add-participant-button (Button): Add new participant
  - search-participant-input (Input): Search field
  - participant-status-filter (Dropdown): Filter by participant status
- Context variables:
  - participants: List of dicts (participant_id, event_id, name, email, booking_id, status, registration_date)
- Navigation:
  - add-participant-button triggers POST to add participant route

### 6. Venue Information Page
- Template file path: templates/venues.html
- Page title: <title>Venues</title>
- Header: <h1 id="venues-page">Venues</h1>
- Element IDs:
  - venues-page (Div): Container
  - venues-grid (Div): Grid of venue cards
  - venue-search-input (Input): Search venues by name/location
  - venue-capacity-filter (Dropdown): Filter by capacity
  - view-venue-details-{venue_id} (Button): Dynamic button for venue details
- Context variables:
  - venues: List of dicts (venue_id, venue_name, location, capacity, amenities)
- Navigation:
  - Dynamic buttons use:
    ```jinja
    <button id="view-venue-details-{{ venue.venue_id }}">View Details</button>
    ```

### 7. Event Schedules Page
- Template file path: templates/schedules.html
- Page title: <title>Event Schedules</title>
- Header: <h1 id="schedules-page">Event Schedules</h1>
- Element IDs:
  - schedules-page (Div): Container
  - schedules-timeline (Div): Timeline display
  - schedule-filter-date (Input Date): Filter by date
  - schedule-filter-event (Dropdown): Filter by event
  - export-schedule-button (Button): Export data
- Context variables:
  - schedules: List of dicts (schedule_id, event_id, session_title, session_time, duration_minutes, speaker, venue_id)
- Navigation:
  - None specific

### 8. Bookings Summary Page
- Template file path: templates/bookings.html
- Page title: <title>My Bookings</title>
- Header: <h1 id="bookings-page">My Bookings</h1>
- Element IDs:
  - bookings-page (Div): Container
  - bookings-table (Table): Bookings list
  - booking-search-input (Input): Search bookings
  - cancel-booking-button-{booking_id} (Button): Dynamic cancel button
  - back-to-dashboard (Button): Navigate back to dashboard
- Context variables:
  - bookings: List of dicts (booking_id, event_id, customer_name, booking_date, ticket_count, ticket_type, total_amount, status)
- Navigation:
  - back-to-dashboard -> url_for('dashboard_page')
  - Cancel buttons:
    ```jinja
    <button id="cancel-booking-button-{{ booking.booking_id }}">Cancel Booking</button>
    ```

## Section 3: Data File Schemas

### 1. Events Data
- File path: data/events.txt
- Field order:
  event_id|event_name|category|date|time|location|description|venue_id|capacity
- Description: Stores information about each event including schedule, description, venue reference, and capacity.
- Example rows:
  ```
  1|Tech Conference 2025|Conference|2025-03-15|09:00|Convention Center, San Francisco|Annual technology conference discussing latest innovations|1|500
  2|Summer Music Festival|Concert|2025-06-20|18:00|Central Park, New York|Three-day music festival with international artists|2|5000
  3|Marathon Championship|Sports|2025-04-10|07:00|Downtown Loop, Chicago|Annual city marathon event for all skill levels|3|1000
  ```

### 2. Venues Data
- File path: data/venues.txt
- Field order:
  venue_id|venue_name|location|capacity|amenities|contact
- Description: Contains data about venues including amenities and contact information.
- Example rows:
  ```
  1|Convention Center|San Francisco, CA|500|WiFi, Parking, Catering|contact@convention.com
  2|Central Park|New York, NY|5000|Outdoor Space, Restrooms, Food Vendors|info@centralparkevents.org
  3|Downtown Loop|Chicago, IL|1000|Paved Surface, Water Stations, Medical Support|events@downtown.com
  ```

### 3. Tickets Data
- File path: data/tickets.txt
- Field order:
  ticket_id|event_id|ticket_type|price|available_count|sold_count
- Description: Tracks ticket types, pricing, availability, and sales per event.
- Example rows:
  ```
  1|1|General|49.99|500|150
  2|1|VIP|99.99|100|45
  3|2|Early Bird|39.99|1000|750
  ```

### 4. Bookings Data
- File path: data/bookings.txt
- Field order:
  booking_id|event_id|customer_name|booking_date|ticket_count|ticket_type|total_amount|status
- Description: Contains records of bookings with customer and ticket details.
- Example rows:
  ```
  1|1|Alice Johnson|2025-02-01|2|General|99.98|Confirmed
  2|2|Bob Williams|2025-02-05|4|Early Bird|159.96|Confirmed
  3|1|Carol Davis|2025-02-10|1|VIP|99.99|Pending
  ```

### 5. Participants Data
- File path: data/participants.txt
- Field order:
  participant_id|event_id|name|email|booking_id|status|registration_date
- Description: Maintains participant details linked to events and bookings.
- Example rows:
  ```
  1|1|Alice Johnson|alice@email.com|1|Confirmed|2025-02-01
  2|1|Michael Johnson|michael@email.com|1|Confirmed|2025-02-01
  3|2|Bob Williams|bob@email.com|2|Attended|2025-02-05
  ```

### 6. Schedules Data
- File path: data/schedules.txt
- Field order:
  schedule_id|event_id|session_title|session_time|duration_minutes|speaker|venue_id
- Description: Details scheduling of event sessions, including timing, speakers, and venue references.
- Example rows:
  ```
  1|1|Opening Keynote|2025-03-15 09:00|60|John Smith|1
  2|1|Panel Discussion|2025-03-15 10:30|90|Expert Panel|1
  3|2|Headliner Performance|2025-06-20 20:00|120|International Artist|2
  ```

---

This design specification document provides all necessary details for backend route implementation, frontend template construction, and data file parsing to ensure consistent and accurate development of the 'EventPlanning' application.