# Design Specification Document for 'EventPlanning' Web Application

---

## Section 1: Flask Routes Specification

| Route Path             | Function Name          | HTTP Methods       | Template File           | Context Variables
|------------------------|------------------------|--------------------|-------------------------|------------------
| /                      | root_redirect          | GET                | redirects to /dashboard | None
| /dashboard             | dashboard_page         | GET                | dashboard.html          | featured_events (list of dicts: {event_id:int, event_name:str, date:str, location:str}), featured_venues (list of dicts: {venue_id:int, venue_name:str, location:str})
| /events                | events_listing         | GET                | events.html             | events (list of dicts: {event_id:int, event_name:str, category:str, date:str, time:str, location:str}), categories (list of str)
| /event/<int:event_id>  | event_details          | GET                | event_details.html      | event (dict: {event_id:int, event_name:str, category:str, date:str, time:str, location:str, description:str}), venue (dict: {venue_id:int, venue_name:str, location:str})
| /book_ticket           | book_ticket            | GET, POST          | book_ticket.html        | On GET: events (list of dicts: {event_id:int, event_name:str}), On POST: booking_confirmation (dict: {booking_id:int, event_name:str, ticket_count:int, ticket_type:str, total_amount:float})
| /participants          | participants_management| GET, POST          | participants.html       | On GET: participants (list of dicts: {participant_id:int, name:str, email:str, event_name:str, status:str}), statuses (list of str)
| /venues                | venues_page            | GET                | venues.html             | venues (list of dicts: {venue_id:int, venue_name:str, location:str, capacity:int, amenities:str})
| /event_schedules       | event_schedules        | GET                | schedules.html          | schedules (list of dicts: {schedule_id:int, event_id:int, session_title:str, session_time:str, duration:int, speaker:str, venue_name:str}), events (list of dicts: {event_id:int, event_name:str})
| /bookings             | bookings_summary        | GET                | bookings.html           | bookings (list of dicts: {booking_id:int, event_name:str, date:str, ticket_count:int, status:str})
| /cancel_booking/<int:booking_id> | cancel_booking   | POST               | redirects to /bookings  | None

---

## Section 2: HTML Template Specifications

### 1. Dashboard Page
- Template file path: templates/dashboard.html
- Page title: Event Planning Dashboard
- Title & H1: "Event Planning Dashboard"
- Element IDs:
  - dashboard-page (Div) - Container for the dashboard page
  - featured-events (Div) - Display of featured event recommendations
  - browse-events-button (Button) - Navigate to /events
  - view-tickets-button (Button) - Navigate to /bookings
  - venues-button (Button) - Navigate to /venues
- Context variables:
  - featured_events: List of dicts with fields: event_id, event_name, date, location
  - featured_venues: List of dicts with fields: venue_id, venue_name, location
- Navigation buttons target routes:
  - browse-events-button: url_for('events_listing')
  - view-tickets-button: url_for('bookings_summary')
  - venues-button: url_for('venues_page')

---

### 2. Events Listing Page
- Template file path: templates/events.html
- Page title: Events Catalog
- Title & H1: "Events Catalog"
- Element IDs:
  - events-page (Div) - Container for the events listing page
  - event-search-input (Input) - Search events by name, location, or date
  - event-category-filter (Dropdown) - Filter by category
  - events-grid (Div) - Grid of event cards
  - view-event-button-{event_id} (Button) - Button on each event card to view details
- Context variables:
  - events: list of dicts with fields: event_id, event_name, category, date, time, location
  - categories: list of strings ["Conference", "Concert", "Sports", "Workshop", "Social"]
- Navigation buttons:
  - Each view-event-button-{event_id} links to url_for('event_details', event_id=event_id)

Rendering dynamic IDs example in Jinja2:
```
{% for event in events %}
  <button id="view-event-button-{{ event.event_id }}">View Details</button>
{% endfor %}
```

---

### 3. Event Details Page
- Template file path: templates/event_details.html
- Page title: Event Details
- Title & H1: "Event Details"
- Element IDs:
  - event-details-page (Div) - Container for event details
  - event-title (H1) - Display event title
  - event-date (Div) - Display event date and time
  - event-location (Div) - Display event location
  - event-description (Div) - Display event description
  - book-ticket-button (Button) - Button to book ticket for this event
- Context variables:
  - event: dict with fields: event_id, event_name, category, date, time, location, description
  - venue: dict with fields: venue_id, venue_name, location
- Navigation buttons:
  - book-ticket-button navigates to url_for('book_ticket') with event_id parameter (sent via form or query)

---

### 4. Ticket Booking Page
- Template file path: templates/book_ticket.html
- Page title: Book Your Tickets
- Title & H1: "Book Your Tickets"
- Element IDs:
  - ticket-booking-page (Div) - Container for ticket booking page
  - select-event-dropdown (Dropdown) - Select event to book
  - ticket-quantity-input (Input number) - Enter number of tickets
  - ticket-type-select (Dropdown) - Select ticket type (General, VIP, Early Bird)
  - book-now-button (Button) - Proceed with booking
  - booking-confirmation (Div) - Display booking confirmation details (shown after POST)
- Context variables:
  - On GET: events (list of dicts): fields: event_id, event_name
  - On POST: booking_confirmation (dict): booking_id, event_name, ticket_count, ticket_type, total_amount
- Navigation buttons:
  - None specified

---

### 5. Participants Management Page
- Template file path: templates/participants.html
- Page title: Participants Management
- Title & H1: "Participants Management"
- Element IDs:
  - participants-page (Div) - Container for participants management page
  - participants-table (Table) - Display participant data: name, email, event, status
  - add-participant-button (Button) - Button to add participant
  - search-participant-input (Input) - Search participants by name or email
  - participant-status-filter (Dropdown) - Filter by participant status (Registered, Confirmed, Attended)
- Context variables:
  - participants: list of dicts with participant_id, name, email, event_name, status
  - statuses: list of strings ["Registered", "Confirmed", "Attended"]
- Navigation buttons:
  - None specified

---

### 6. Venue Information Page
- Template file path: templates/venues.html
- Page title: Venues
- Title & H1: "Venues"
- Element IDs:
  - venues-page (Div) - Container for venues page
  - venues-grid (Div) - Grid displaying venue cards
  - venue-search-input (Input) - Search venues by name or location
  - venue-capacity-filter (Dropdown) - Filter by capacity (Small, Medium, Large)
  - view-venue-details-{venue_id} (Button) - Button to view venue details on each card
- Context variables:
  - venues: list of dicts with venue_id, venue_name, location, capacity, amenities
- Navigation buttons:
  - Each view-venue-details-{venue_id} button links to venue detail route if any (not specified, assume none)

Rendering dynamic IDs example in Jinja2:
```
{% for venue in venues %}
  <button id="view-venue-details-{{ venue.venue_id }}">View Details</button>
{% endfor %}
```

---

### 7. Event Schedules Page
- Template file path: templates/schedules.html
- Page title: Event Schedules
- Title & H1: "Event Schedules"
- Element IDs:
  - schedules-page (Div) - Container for schedules page
  - schedules-timeline (Div) - Timeline of events and sessions
  - schedule-filter-date (Input date) - Filter schedules by date
  - schedule-filter-event (Dropdown) - Filter by event
  - export-schedule-button (Button) - Export schedule data
- Context variables:
  - schedules: list of dicts with schedule_id, event_id, session_title, session_time, duration, speaker, venue_name
  - events: list of dicts with event_id, event_name
- Navigation buttons:
  - None specified

---

### 8. Bookings Summary Page
- Template file path: templates/bookings.html
- Page title: My Bookings
- Title & H1: "My Bookings"
- Element IDs:
  - bookings-page (Div) - Container for bookings page
  - bookings-table (Table) - Show bookings columns: event, date, ticket count, status
  - booking-search-input (Input) - Search bookings by event name or booking ID
  - cancel-booking-button-{booking_id} (Button) - Cancel booking button for each booking
  - back-to-dashboard (Button) - Navigate back to dashboard
- Context variables:
  - bookings: list of dicts with booking_id, event_name, date, ticket_count, status
- Navigation buttons:
  - cancel-booking-button-{booking_id} triggers POST to /cancel_booking/<booking_id>
  - back-to-dashboard button links to url_for('dashboard_page')

Rendering dynamic IDs example in Jinja2:
```
{% for booking in bookings %}
  <button id="cancel-booking-button-{{ booking.booking_id }}">Cancel Booking</button>
{% endfor %}
```

---

## Section 3: Data File Schemas

### 1. Events Data
- File path: data/events.txt
- Pipe-delimited fields:
  event_id|event_name|category|date|time|location|description|venue_id|capacity
- Description: Stores details of each event, linked to venues
- Example rows:
  1|Tech Conference 2025|Conference|2025-03-15|09:00|Convention Center, San Francisco|Annual technology conference discussing latest innovations|1|500
  2|Summer Music Festival|Concert|2025-06-20|18:00|Central Park, New York|Three-day music festival with international artists|2|5000
  3|Marathon Championship|Sports|2025-04-10|07:00|Downtown Loop, Chicago|Annual city marathon event for all skill levels|3|1000

### 2. Venues Data
- File path: data/venues.txt
- Pipe-delimited fields:
  venue_id|venue_name|location|capacity|amenities|contact
- Description: Information about venues including amenities
- Example rows:
  1|Convention Center|San Francisco, CA|500|WiFi, Parking, Catering|contact@convention.com
  2|Central Park|New York, NY|5000|Outdoor Space, Restrooms, Food Vendors|info@centralparkevents.org
  3|Downtown Loop|Chicago, IL|1000|Paved Surface, Water Stations, Medical Support|events@downtown.com

### 3. Tickets Data
- File path: data/tickets.txt
- Pipe-delimited fields:
  ticket_id|event_id|ticket_type|price|available_count|sold_count
- Description: Ticket types and availability for events
- Example rows:
  1|1|General|49.99|500|150
  2|1|VIP|99.99|100|45
  3|2|Early Bird|39.99|1000|750

### 4. Bookings Data
- File path: data/bookings.txt
- Pipe-delimited fields:
  booking_id|event_id|customer_name|booking_date|ticket_count|ticket_type|total_amount|status
- Description: Records of user bookings and their status
- Example rows:
  1|1|Alice Johnson|2025-02-01|2|General|99.98|Confirmed
  2|2|Bob Williams|2025-02-05|4|Early Bird|159.96|Confirmed
  3|1|Carol Davis|2025-02-10|1|VIP|99.99|Pending

### 5. Participants Data
- File path: data/participants.txt
- Pipe-delimited fields:
  participant_id|event_id|name|email|booking_id|status|registration_date
- Description: Participants attending events with booking reference
- Example rows:
  1|1|Alice Johnson|alice@email.com|1|Confirmed|2025-02-01
  2|1|Michael Johnson|michael@email.com|1|Confirmed|2025-02-01
  3|2|Bob Williams|bob@email.com|2|Attended|2025-02-05

### 6. Schedules Data
- File path: data/schedules.txt
- Pipe-delimited fields:
  schedule_id|event_id|session_title|session_time|duration_minutes|speaker|venue_id
- Description: Schedule details for event sessions
- Example rows:
  1|1|Opening Keynote|2025-03-15 09:00|60|John Smith|1
  2|1|Panel Discussion|2025-03-15 10:30|90|Expert Panel|1
  3|2|Headliner Performance|2025-06-20 20:00|120|International Artist|2

---

This completes the comprehensive design specification for the 'EventPlanning' application, covering all Flask routes, HTML templates, and data file schemas exactly as specified in the requirements document. This specification enables backend and frontend developers to work independently and implement all features without ambiguity or assumptions.