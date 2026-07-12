# Design Specification Document for 'EventPlanning' Web Application

---

## Section 1: Flask Routes Specification

| Route Path               | Function Name         | HTTP Methods     | Template File             | Context Variables                                                                                                      |
|--------------------------|-----------------------|------------------|---------------------------|------------------------------------------------------------------------------------------------------------------------|
| /                        | root_redirect          | GET              | -                         | - Redirects to /dashboard                                                                                                |
| /dashboard               | dashboard             | GET              | dashboard.html            | featured_events: List of event dicts (event_id:int, event_name:str, category:str, date:str, location:str)               |
| /events                  | events_listing        | GET              | events.html               | events: List of event dicts (event_id:int, event_name:str, category:str, date:str, location:str)                        |
| /events/search            | events_search         | POST             | events.html               | filtered_events: List of event dicts as above                                                                        |
| /event/<int:event_id>    | event_details         | GET              | event_details.html        | event: dict (event_id:int, event_name:str, category:str, date:str, time:str, location:str, description:str, venue_id:int, capacity:int) |
| /book_ticket             | book_ticket           | GET, POST        | ticket_booking.html       | GET: events: List of event dicts (event_id:int, event_name:str)
POST: booking_confirmation: dict (booking_id:int, event_id:int, ticket_count:int, ticket_type:str, total_amount:float)
errors: List[str] if validation errors |
| /participants            | participants_management| GET              | participants.html         | participants: List of participant dicts (participant_id:int, event_id:int, name:str, email:str, booking_id:int, status:str, registration_date:str) |
| /participants/add         | add_participant       | POST             | participants.html         | participants: updated list as above, add errors if needed                                                              |
| /venues                  | venues_listing        | GET              | venues.html               | venues: List of venue dicts (venue_id:int, venue_name:str, location:str, capacity:int, amenities:str, contact:str)      |
| /venue/<int:venue_id>    | venue_details         | GET              | venue_details.html        | venue: dict (venue_id:int, venue_name:str, location:str, capacity:int, amenities:str, contact:str)                       |
| /schedules               | schedules             | GET              | schedules.html            | schedules: List of schedule dicts (schedule_id:int,event_id:int,session_title:str,session_time:str,duration_minutes:int,speaker:str,venue_id:int),
events: List[event_id:int,event_name:str] for filter dropdown                                                             |
| /bookings                | bookings_summary      | GET              | bookings.html             | bookings: List of booking dicts (booking_id:int,event_id:int,event_name:str,booking_date:str,ticket_count:int,ticket_type:str,total_amount:float,status:str) |
| /booking/cancel/<int:booking_id> | cancel_booking    | POST             | bookings.html             | bookings: updated list after cancellation                                                                              |


---

## Section 2: HTML Template Specifications

### 1. Dashboard Page
- Template file path: templates/dashboard.html
- Page title: Event Planning Dashboard
- IDs and elements:
  - dashboard-page (Div): Container for the dashboard page
  - featured-events (Div): Display of featured event recommendations
  - browse-events-button (Button): Navigate to /events
  - view-tickets-button (Button): Navigate to /bookings
  - venues-button (Button): Navigate to /venues
- Context variables:
  - featured_events: List of event objects with fields event_id, event_name, category, date, location
- Navigation:
  - browse-events-button -> url_for('events_listing')
  - view-tickets-button -> url_for('bookings_summary')
  - venues-button -> url_for('venues_listing')

### 2. Events Listing Page
- Template file path: templates/events.html
- Page title: Events Catalog
- IDs and elements:
  - events-page (Div): Container
  - event-search-input (Input)
  - event-category-filter (Dropdown) with options: Conference, Concert, Sports, Workshop, Social
  - events-grid (Div): Grid displaying event cards
  - view-event-button-{event_id} (Button): Button for each event card, dynamic IDs with event_id
- Context variables:
  - events: List of event objects (event_id, event_name, category, date, location)
- Navigation:
  - Back or other nav buttons as applicable
- Dynamic elements:
  - In Jinja2 loop, assign button ID as "view-event-button-{{ event.event_id }}"

### 3. Event Details Page
- Template file path: templates/event_details.html
- Page title: Event Details
- IDs and elements:
  - event-details-page (Div)
  - event-title (H1)
  - event-date (Div)
  - event-location (Div)
  - event-description (Div)
  - book-ticket-button (Button): Navigate to /book_ticket
- Context variables:
  - event: dict with event fields as per schema
- Navigation:
  - book-ticket-button -> url_for('book_ticket')

### 4. Ticket Booking Page
- Template file path: templates/ticket_booking.html
- Page title: Book Your Tickets
- IDs and elements:
  - ticket-booking-page (Div)
  - select-event-dropdown (Dropdown): event selection
  - ticket-quantity-input (Input number)
  - ticket-type-select (Dropdown): options General, VIP, Early Bird
  - book-now-button (Button)
  - booking-confirmation (Div): to show confirmation details after booking
- Context variables:
  - GET: events list with event_id and event_name
  - POST (after booking): booking_confirmation dict with booking info
  - errors: list of error strings if validation fails
- Navigation:
  - Use form submission to /book_ticket POST

### 5. Participants Management Page
- Template file path: templates/participants.html
- Page title: Participants Management
- IDs and elements:
  - participants-page (Div)
  - participants-table (Table): columns for name, email, event, status
  - add-participant-button (Button)
  - search-participant-input (Input)
  - participant-status-filter (Dropdown) options: Registered, Confirmed, Attended
- Context variables:
  - participants: list of participant dicts with participant_id, event_id, name, email, booking_id, status, registration_date
- Navigation:
  - add-participant-button can open form or modal POST to /participants/add

### 6. Venue Information Page
- Template file path: templates/venues.html
- Page title: Venues
- IDs and elements:
  - venues-page (Div)
  - venues-grid (Div): venue cards
  - venue-search-input (Input)
  - venue-capacity-filter (Dropdown): options Small, Medium, Large
  - view-venue-details-{venue_id} (Button): dynamic ID per venue
- Context variables:
  - venues: list of venue dicts (venue_id, venue_name, location, capacity, amenities, contact)
- Navigation:
  - Dynamic buttons to /venue/<venue_id> route
- Dynamic IDs:
  - "view-venue-details-{{ venue.venue_id }}" in Jinja2 loops

### 7. Event Schedules Page
- Template file path: templates/schedules.html
- Page title: Event Schedules
- IDs and elements:
  - schedules-page (Div)
  - schedules-timeline (Div)
  - schedule-filter-date (Input date)
  - schedule-filter-event (Dropdown) with events
  - export-schedule-button (Button)
- Context variables:
  - schedules: list of schedule dicts (schedule_id, event_id, session_title, session_time, duration_minutes, speaker, venue_id)
  - events: list of event dicts with event_id and event_name
- Navigation:
  - export-schedule-button triggers export action

### 8. Bookings Summary Page
- Template file path: templates/bookings.html
- Page title: My Bookings
- IDs and elements:
  - bookings-page (Div)
  - bookings-table (Table): columns for event, date, ticket count, status
  - booking-search-input (Input)
  - cancel-booking-button-{booking_id} (Button): dynamic ID per booking
  - back-to-dashboard (Button): navigate to dashboard
- Context variables:
  - bookings: list of booking dicts (booking_id, event_id, event_name, booking_date, ticket_count, ticket_type, total_amount, status)
- Navigation:
  - cancel-booking-button triggers POST to /booking/cancel/<booking_id>
  - back-to-dashboard -> url_for('dashboard')
- Dynamic IDs:
  - "cancel-booking-button-{{ booking.booking_id }}" in Jinja2 loops

---

## Section 3: Data File Schemas

### 1. Events Data
- File path: data/events.txt
- Fields (pipe-delimited):
  event_id|event_name|category|date|time|location|description|venue_id|capacity
- Description: Stores all event information including schedule and venue reference
- Example rows:
  1|Tech Conference 2025|Conference|2025-03-15|09:00|Convention Center, San Francisco|Annual technology conference discussing latest innovations|1|500
  2|Summer Music Festival|Concert|2025-06-20|18:00|Central Park, New York|Three-day music festival with international artists|2|5000
  3|Marathon Championship|Sports|2025-04-10|07:00|Downtown Loop, Chicago|Annual city marathon event for all skill levels|3|1000

### 2. Venues Data
- File path: data/venues.txt
- Fields (pipe-delimited):
  venue_id|venue_name|location|capacity|amenities|contact
- Description: Venue details with capacity and amenities
- Example rows:
  1|Convention Center|San Francisco, CA|500|WiFi, Parking, Catering|contact@convention.com
  2|Central Park|New York, NY|5000|Outdoor Space, Restrooms, Food Vendors|info@centralparkevents.org
  3|Downtown Loop|Chicago, IL|1000|Paved Surface, Water Stations, Medical Support|events@downtown.com

### 3. Tickets Data
- File path: data/tickets.txt
- Fields (pipe-delimited):
  ticket_id|event_id|ticket_type|price|available_count|sold_count
- Description: Tickets available per event and their counts
- Example rows:
  1|1|General|49.99|500|150
  2|1|VIP|99.99|100|45
  3|2|Early Bird|39.99|1000|750

### 4. Bookings Data
- File path: data/bookings.txt
- Fields (pipe-delimited):
  booking_id|event_id|customer_name|booking_date|ticket_count|ticket_type|total_amount|status
- Description: Booking records including status
- Example rows:
  1|1|Alice Johnson|2025-02-01|2|General|99.98|Confirmed
  2|2|Bob Williams|2025-02-05|4|Early Bird|159.96|Confirmed
  3|1|Carol Davis|2025-02-10|1|VIP|99.99|Pending

### 5. Participants Data
- File path: data/participants.txt
- Fields(pipe-delimited):
  participant_id|event_id|name|email|booking_id|status|registration_date
- Description: Participants registered for events with statuses
- Example rows:
  1|1|Alice Johnson|alice@email.com|1|Confirmed|2025-02-01
  2|1|Michael Johnson|michael@email.com|1|Confirmed|2025-02-01
  3|2|Bob Williams|bob@email.com|2|Attended|2025-02-05

### 6. Schedules Data
- File path: data/schedules.txt
- Fields(pipe-delimited):
  schedule_id|event_id|session_title|session_time|duration_minutes|speaker|venue_id
- Description: Event sessions and their schedules
- Example rows:
  1|1|Opening Keynote|2025-03-15 09:00|60|John Smith|1
  2|1|Panel Discussion|2025-03-15 10:30|90|Expert Panel|1
  3|2|Headliner Performance|2025-06-20 20:00|120|International Artist|2

---

*End of Design Specification Document*