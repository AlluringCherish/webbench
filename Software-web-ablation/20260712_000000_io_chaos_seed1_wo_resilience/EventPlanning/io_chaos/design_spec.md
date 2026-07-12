# EventPlanning Application Design Specification

---

## Section 1: Flask Routes Specification

| Route Path              | Function Name           | HTTP Methods | Template File           | Context Variables                                                                                                  |
|-------------------------|-------------------------|--------------|-------------------------|-------------------------------------------------------------------------------------------------------------------|
| /                       | redirect_to_dashboard    | GET          | None (Redirect)          | None                                                                                                              |
| /dashboard              | dashboard_page           | GET          | dashboard.html          | featured_events: List[Dict] - Each dict with event details (event_id:int, event_name:str, date:str, location:str) |
|                         |                         |              |                         |                                                                                                                   |
| /events                 | events_listing           | GET          | events.html             | events: List[Dict] - event_id:int, event_name:str, category:str, date:str, location:str                            |
|                         |                         |              |                         | categories: List[str] - ["Conference", "Concert", "Sports", "Workshop", "Social"]                         |
|                         |                         |              |                         | search_query: str - current search filter value (empty if none)                                                   |
|                         |                         |              |                         | category_filter: str - current selected category for filtering                                                   |
|                         |                         |              |                         |                                                                                                                   |
| /event/<int:event_id>   | event_details            | GET          | event_details.html      | event: Dict - event_id:int, event_name:str, date:str, time:str, location:str, description:str, venue_id:int       |
|                         |                         |              |                         | capacity:int                                                                                                      |
|                         |                         |              |                         |                                                                                                                   |
| /book_ticket            | book_ticket_page         | GET          | ticket_booking.html     | events: List[Dict] - event_id:int, event_name:str                                                                |
| /book_ticket            | process_ticket_booking   | POST         | ticket_booking.html     | confirmation: Dict - booking_id:int, event_name:str, ticket_count:int, ticket_type:str, total_amount:float          |
|                         |                         |              |                         | error_message: str (optional) if booking fails                                                                   |
|                         |                         |              |                         |                                                                                                                   |
| /participants           | participants_management  | GET          | participants.html       | participants: List[Dict] - participant_id:int, event_name:str, name:str, email:str, status:str                     |
|                         |                         |              |                         | status_filter: str - current status filter value                                                                   |
|                         |                         |              |                         | search_query: str - current search query for participant search                                                    |
|                         |                         |              |                         |                                                                                                                   |
| /add_participant        | add_participant          | POST         | None (Redirect or JSON) | error_message: str (optional)                                                                                     |
|                         |                         |              |                         |                                                                                                                   |
| /venues                 | venues_page              | GET          | venues.html             | venues: List[Dict] - venue_id:int, venue_name:str, location:str, capacity:int                                      |
|                         |                         |              |                         | capacity_filter: str - current capacity filter value                                                               |
|                         |                         |              |                         | search_query: str - current search query for venues                                                              |
|                         |                         |              |                         |                                                                                                                   |
| /event_schedules        | event_schedules          | GET          | schedules.html          | schedules: List[Dict] - schedule_id:int, event_name:str, session_title:str, session_time:str, duration_minutes:int |
|                         |                         |              |                         | speaker:str, venue_name:str                                                                                        |
|                         |                         |              |                         | filter_date: str - current date filter value                                                                       |
|                         |                         |              |                         | event_filter: str - current event filter value                                                                     |
|                         |                         |              |                         |                                                                                                                   |
| /bookings              | bookings_summary          | GET          | bookings.html           | bookings: List[Dict] - booking_id:int, event_name:str, date:str, ticket_count:int, status:str                      |
|                         |                         |              |                         | search_query: str - current search filter value                                                                    |
|                                                                                         |
| /cancel_booking/<int:booking_id> | cancel_booking    | POST         | None (Redirect)          | None                                                                                                              |

Notes:
- The root route `/` should redirect users to `/dashboard`.
- POST routes are used for submitting forms: ticket booking, adding participants, cancelling bookings.
- Context variables such as lists include dictionaries with relevant fields as per the data schema and required information.


---

## Section 2: HTML Template Specifications

### 1. Dashboard Page
- Template Path: templates/dashboard.html
- Page Title: "Event Planning Dashboard"
- Element IDs:
  - dashboard-page (Div): Main container
  - featured-events (Div): Featured events display
  - browse-events-button (Button): Navigate to /events
  - view-tickets-button (Button): Navigate to /bookings
  - venues-button (Button): Navigate to /venues
- Context Variables:
  - featured_events: List of event dicts with keys: event_id, event_name, date, location
- Navigation:
  - browse-events-button => `url_for('events_listing')`
  - view-tickets-button => `url_for('bookings_summary')`
  - venues-button => `url_for('venues_page')`

### 2. Events Listing Page
- Template Path: templates/events.html
- Page Title: "Events Catalog"
- Element IDs:
  - events-page (Div): Container
  - event-search-input (Input): Search field
  - event-category-filter (Dropdown): Category filter
  - events-grid (Div): Grid containing event cards
  - view-event-button-{{ event.event_id }} (Button): View details button per event
- Context Variables:
  - events: List of dicts with event_id, event_name, category, date, location
  - categories: List of strings of categories
  - search_query: Current string in search input
  - category_filter: Current selected category
- Navigation:
  - Event detail buttons: `url_for('event_details', event_id=event.event_id)`

- Dynamic Elements Handling:
  - Loop over events to render each event card containing button with id `view-event-button-{{ event.event_id }}`

### 3. Event Details Page
- Template Path: templates/event_details.html
- Page Title: "Event Details"
- Element IDs:
  - event-details-page (Div): Container
  - event-title (H1): Event title
  - event-date (Div): Event date and time
  - event-location (Div): Event location
  - event-description (Div): Detailed description
  - book-ticket-button (Button): Navigate to ticket booking
- Context Variables:
  - event: dict with keys event_id, event_name, date, time, location, description, venue_id, capacity
- Navigation:
  - book-ticket-button => `url_for('book_ticket_page')`

### 4. Ticket Booking Page
- Template Path: templates/ticket_booking.html
- Page Title: "Book Your Tickets"
- Element IDs:
  - ticket-booking-page (Div): Container
  - select-event-dropdown (Dropdown): Select event
  - ticket-quantity-input (Input number): Number of tickets
  - ticket-type-select (Dropdown): Ticket type
  - book-now-button (Button): Submit booking
  - booking-confirmation (Div): Display confirmation details
- Context Variables:
  - events: List of dicts with event_id, event_name for dropdown
  - confirmation (optional): dict with booking_id, event_name, ticket_count, ticket_type, total_amount
  - error_message (optional): string indicating booking error
- Navigation:
  - N/A

### 5. Participants Management Page
- Template Path: templates/participants.html
- Page Title: "Participants Management"
- Element IDs:
  - participants-page (Div): Container
  - participants-table (Table): Table with columns Name, Email, Event, Status
  - add-participant-button (Button): Button to add new participant
  - search-participant-input (Input): Search participants
  - participant-status-filter (Dropdown): Filter by participant status
- Context Variables:
  - participants: List of dicts with participant_id, event_name, name, email, status
  - status_filter: Current filter string
  - search_query: Current participant search string
- Navigation:
  - add-participant-button triggers POST to add participant route

### 6. Venue Information Page
- Template Path: templates/venues.html
- Page Title: "Venues"
- Element IDs:
  - venues-page (Div): Container
  - venues-grid (Div): Grid with venue cards
  - venue-search-input (Input): Search venues
  - venue-capacity-filter (Dropdown): Filter by capacity
  - view-venue-details-{{ venue.venue_id }} (Button): View venue details per venue
- Context Variables:
  - venues: List of dicts with venue_id, venue_name, location, capacity
  - capacity_filter: Current filter string
  - search_query: Current search string
- Navigation:
  - Venue detail buttons: `url_for('venue_details', venue_id=venue.venue_id)` (Note: venue details page not specified, if needed could be an extension)

- Dynamic Elements Handling:
  - Loop through venues to render each venue card with button id: `view-venue-details-{{ venue.venue_id }}`

### 7. Event Schedules Page
- Template Path: templates/schedules.html
- Page Title: "Event Schedules"
- Element IDs:
  - schedules-page (Div): Container
  - schedules-timeline (Div): Timeline of events/sessions
  - schedule-filter-date (Input date): Date filter
  - schedule-filter-event (Dropdown): Event filter
  - export-schedule-button (Button): Export schedule data
- Context Variables:
  - schedules: List of dicts with schedule_id, event_name, session_title, session_time, duration_minutes, speaker, venue_name
  - filter_date: Current date string filter
  - event_filter: Current event selection
- Navigation:
  - export-schedule-button triggers export action (route not specified, assumed handled on same page)

### 8. Bookings Summary Page
- Template Path: templates/bookings.html
- Page Title: "My Bookings"
- Element IDs:
  - bookings-page (Div): Container
  - bookings-table (Table): Table with columns event, date, ticket count, status
  - booking-search-input (Input): Search bookings
  - cancel-booking-button-{{ booking.booking_id }} (Button): Cancel button per booking
  - back-to-dashboard (Button): Navigate back to dashboard
- Context Variables:
  - bookings: List of dicts with booking_id, event_name, date, ticket_count, status
  - search_query: Current search string
- Navigation:
  - cancel-booking buttons submit POST to `/cancel_booking/<booking_id>`
  - back-to-dashboard => `url_for('dashboard_page')`

- Dynamic Elements Handling:
  - Loop through bookings to render cancel buttons with id: `cancel-booking-button-{{ booking.booking_id }}`

---

## Section 3: Data File Schemas

### 1. Events Data
- File Path: data/events.txt
- Field Order (pipe-delimited):
  ```
  event_id|event_name|category|date|time|location|description|venue_id|capacity
  ```
- Description: Stores all event details including scheduling and venue.
- Example Rows:
  ```
  1|Tech Conference 2025|Conference|2025-03-15|09:00|Convention Center, San Francisco|Annual technology conference discussing latest innovations|1|500
  2|Summer Music Festival|Concert|2025-06-20|18:00|Central Park, New York|Three-day music festival with international artists|2|5000
  3|Marathon Championship|Sports|2025-04-10|07:00|Downtown Loop, Chicago|Annual city marathon event for all skill levels|3|1000
  ```

### 2. Venues Data
- File Path: data/venues.txt
- Field Order:
  ```
  venue_id|venue_name|location|capacity|amenities|contact
  ```
- Description: Stores details about venues such as capacity and contact info.
- Example Rows:
  ```
  1|Convention Center|San Francisco, CA|500|WiFi, Parking, Catering|contact@convention.com
  2|Central Park|New York, NY|5000|Outdoor Space, Restrooms, Food Vendors|info@centralparkevents.org
  3|Downtown Loop|Chicago, IL|1000|Paved Surface, Water Stations, Medical Support|events@downtown.com
  ```

### 3. Tickets Data
- File Path: data/tickets.txt
- Field Order:
  ```
  ticket_id|event_id|ticket_type|price|available_count|sold_count
  ```
- Description: Ticket types and availability per event.
- Example Rows:
  ```
  1|1|General|49.99|500|150
  2|1|VIP|99.99|100|45
  3|2|Early Bird|39.99|1000|750
  ```

### 4. Bookings Data
- File Path: data/bookings.txt
- Field Order:
  ```
  booking_id|event_id|customer_name|booking_date|ticket_count|ticket_type|total_amount|status
  ```
- Description: Customer bookings for tickets with status.
- Example Rows:
  ```
  1|1|Alice Johnson|2025-02-01|2|General|99.98|Confirmed
  2|2|Bob Williams|2025-02-05|4|Early Bird|159.96|Confirmed
  3|1|Carol Davis|2025-02-10|1|VIP|99.99|Pending
  ```

### 5. Participants Data
- File Path: data/participants.txt
- Field Order:
  ```
  participant_id|event_id|name|email|booking_id|status|registration_date
  ```
- Description: Records participants registered for events.
- Example Rows:
  ```
  1|1|Alice Johnson|alice@email.com|1|Confirmed|2025-02-01
  2|1|Michael Johnson|michael@email.com|1|Confirmed|2025-02-01
  3|2|Bob Williams|bob@email.com|2|Attended|2025-02-05
  ```

### 6. Schedules Data
- File Path: data/schedules.txt
- Field Order:
  ```
  schedule_id|event_id|session_title|session_time|duration_minutes|speaker|venue_id
  ```
- Description: Schedule sessions associated with events.
- Example Rows:
  ```
  1|1|Opening Keynote|2025-03-15 09:00|60|John Smith|1
  2|1|Panel Discussion|2025-03-15 10:30|90|Expert Panel|1
  3|2|Headliner Performance|2025-06-20 20:00|120|International Artist|2
  ```

---

*End of Design Specification Document*
