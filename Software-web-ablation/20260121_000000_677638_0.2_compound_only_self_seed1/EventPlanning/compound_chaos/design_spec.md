# EventPlanning Application Design Specification

---

## Section 1: Flask Routes Specification

| Route Path               | Function Name           | HTTP Methods | Template File           | Context Variables (Type and Structure)                                                                                                    |
|--------------------------|-------------------------|--------------|-------------------------|-------------------------------------------------------------------------------------------------------------------------------------------|
| /                        | root_redirect            | GET          | None (redirect)          | None                                                                                                                                      |
| /dashboard               | dashboard_page           | GET          | dashboard.html          | featured_events (List of EventDict)
  - EventDict: {event_id: int, event_name: str, category: str, date: str (YYYY-MM-DD), time: str (HH:MM), location: str, description: str, venue_id: int, capacity: int}
  featured_venues (List of VenueDict)
  - VenueDict: {venue_id: int, venue_name: str, location: str, capacity: int, amenities: str, contact: str}                                     |
| /events                 | events_listing           | GET          | events.html             | events (List[EventDict])
  categories (List[str]) = ['Conference', 'Concert', 'Sports', 'Workshop', 'Social']                                                        |
| /event/<int:event_id>    | event_details            | GET          | event_details.html      | event (EventDict)
  tickets (List[TicketDict])
  - TicketDict: {ticket_id: int, event_id: int, ticket_type: str, price: float, available_count: int, sold_count: int}                         |
| /book_ticket             | ticket_booking           | GET, POST    | ticket_booking.html     | GET:
    events (List[EventDict])
  POST:
    booking_confirmation (Dict): {booking_id: int, event_id: int, customer_name: str, booking_date: str (YYYY-MM-DD), ticket_count: int, ticket_type: str, total_amount: float, status: str}
    or error_message (str)
| /participants            | participants_management  | GET, POST    | participants.html       | participants (List[ParticipantDict])
  - ParticipantDict: {participant_id: int, event_id: int, name: str, email: str, booking_id: int, status: str, registration_date: str}
  filters:
    search_query (str, optional)
    status_filter (str, optional: Registered, Confirmed, Attended)                 |
| /venues                 | venues_page              | GET          | venues.html             | venues (List[VenueDict])
  capacity_filters (List[str]) = ['Small', 'Medium', 'Large']                                                                             |
| /venue/<int:venue_id>    | venue_details            | GET          | venue_details.html      | venue (VenueDict)                                                                                                                        |
| /schedules              | event_schedules          | GET          | schedules.html          | schedules (List[ScheduleDict])
  - ScheduleDict: {schedule_id: int, event_id: int, session_title: str, session_time: str (YYYY-MM-DD HH:MM), duration_minutes: int, speaker: str, venue_id: int}
  events (List[EventDict])                                                                                      |
| /bookings               | bookings_summary         | GET          | bookings.html           | bookings (List[BookingDict])
  - BookingDict: {booking_id: int, event_id: int, customer_name: str, booking_date: str (YYYY-MM-DD), ticket_count: int, ticket_type: str, total_amount: float, status: str}             |

---

## Section 2: HTML Template Specifications

### 1. Dashboard Page
- Template file path: templates/dashboard.html
- Page Title for <title> and <h1>: "Event Planning Dashboard"
- Element IDs:
  - dashboard-page (Div): Container for the dashboard page
  - featured-events (Div): Display of featured event recommendations
  - browse-events-button (Button): Button to navigate to events listing page
  - view-tickets-button (Button): Button to navigate to bookings summary page
  - venues-button (Button): Button to navigate to venues page
- Context variables:
  - featured_events (List of EventDict as defined in Section 1)
  - featured_venues (List of VenueDict as defined in Section 1)
- Navigation buttons:
  - browse-events-button calls url_for('events_listing')
  - view-tickets-button calls url_for('bookings_summary')
  - venues-button calls url_for('venues_page')

### 2. Events Listing Page
- Template file path: templates/events.html
- Page Title for <title> and <h1>: "Events Catalog"
- Element IDs:
  - events-page (Div): Container for events listing
  - event-search-input (Input): Text input to search events by name, location, or date
  - event-category-filter (Dropdown): Dropdown to filter by category
  - events-grid (Div): Grid displaying event cards
  - view-event-button-{{event.event_id}} (Button): Button on each event card to view event details
- Context variables:
  - events (List of EventDict)
  - categories (List[str]) = ['Conference', 'Concert', 'Sports', 'Workshop', 'Social']
- Navigation buttons:
  - view-event-button-{{event.event_id}} calls url_for('event_details', event_id=event.event_id)

### 3. Event Details Page
- Template file path: templates/event_details.html
- Page Title for <title> and <h1>: "Event Details"
- Element IDs:
  - event-details-page (Div): Container for event details page
  - event-title (H1): Display event title
  - event-date (Div): Display event date and time
  - event-location (Div): Display event location
  - event-description (Div): Display detailed event description
  - book-ticket-button (Button): Button to book ticket for this event
- Context variables:
  - event (EventDict)
  - tickets (List of TicketDict)
- Navigation buttons:
  - book-ticket-button calls url_for('ticket_booking')

### 4. Ticket Booking Page
- Template file path: templates/ticket_booking.html
- Page Title for <title> and <h1>: "Book Your Tickets"
- Element IDs:
  - ticket-booking-page (Div): Container for ticket booking page
  - select-event-dropdown (Dropdown): Dropdown to select event
  - ticket-quantity-input (Input number): Field to enter number of tickets
  - ticket-type-select (Dropdown): Dropdown to select ticket type
  - book-now-button (Button): Button to proceed with ticket booking
  - booking-confirmation (Div): Div to display booking confirmation details
- Context variables:
  - GET: events (List of EventDict)
  - POST: booking_confirmation (Dict) or error_message (str)
- Navigation buttons:
  - None (booking submission handled by form POST)

### 5. Participants Management Page
- Template file path: templates/participants.html
- Page Title for <title> and <h1>: "Participants Management"
- Element IDs:
  - participants-page (Div): Container for participants management
  - participants-table (Table): Table displaying participants with columns: name, email, event, status
  - add-participant-button (Button): Button to add new participant
  - search-participant-input (Input): Input field to search participants by name or email
  - participant-status-filter (Dropdown): Dropdown to filter by status
- Context variables:
  - participants (List of ParticipantDict)
- Navigation buttons:
  - add-participant-button (Button) intended for participant addition form (not detailed)

### 6. Venue Information Page
- Template file path: templates/venues.html
- Page Title for <title> and <h1>: "Venues"
- Element IDs:
  - venues-page (Div): Container for the venues page
  - venues-grid (Div): Grid displaying venue cards
  - venue-search-input (Input): Input to search venues by name or location
  - venue-capacity-filter (Dropdown): Filter venues by capacity
  - view-venue-details-{{venue.venue_id}} (Button): Button to view venue details
- Context variables:
  - venues (List of VenueDict)
- Navigation buttons:
  - view-venue-details-{{venue.venue_id}} calls url_for('venue_details', venue_id=venue.venue_id)

### 7. Event Schedules Page
- Template file path: templates/schedules.html
- Page Title for <title> and <h1>: "Event Schedules"
- Element IDs:
  - schedules-page (Div): Container for schedules page
  - schedules-timeline (Div): Timeline view of upcoming events and sessions
  - schedule-filter-date (Input date): Field to filter schedules by date
  - schedule-filter-event (Dropdown): Dropdown to filter by event
  - export-schedule-button (Button): Button to export schedule data
- Context variables:
  - schedules (List of ScheduleDict)
  - events (List of EventDict)
- Navigation buttons:
  - export-schedule-button triggers schedule export (backend implementation not defined here)

### 8. Bookings Summary Page
- Template file path: templates/bookings.html
- Page Title for <title> and <h1>: "My Bookings"
- Element IDs:
  - bookings-page (Div): Container for bookings page
  - bookings-table (Table): Table displaying bookings with columns: event, date, ticket count, booking status
  - booking-search-input (Input): Input to search bookings by event name or booking ID
  - cancel-booking-button-{{booking.booking_id}} (Button): Button to cancel booking
  - back-to-dashboard (Button): Button to navigate back to dashboard
- Context variables:
  - bookings (List of BookingDict)
- Navigation buttons:
  - cancel-booking-button-{{booking.booking_id}} calls url_for('bookings_summary') with cancel action (implementation detail)
  - back-to-dashboard calls url_for('dashboard_page')

---

## Section 3: Data File Schemas

### 1. Events Data
- File Path: data/events.txt
- Field Order (pipe-delimited): event_id|event_name|category|date|time|location|description|venue_id|capacity
- Description: Stores detailed event records.
- Examples:
  1|Tech Conference 2025|Conference|2025-03-15|09:00|Convention Center, San Francisco|Annual technology conference discussing latest innovations|1|500
  2|Summer Music Festival|Concert|2025-06-20|18:00|Central Park, New York|Three-day music festival with international artists|2|5000
  3|Marathon Championship|Sports|2025-04-10|07:00|Downtown Loop, Chicago|Annual city marathon event for all skill levels|3|1000

### 2. Venues Data
- File Path: data/venues.txt
- Field Order (pipe-delimited): venue_id|venue_name|location|capacity|amenities|contact
- Description: Stores venue detail information.
- Examples:
  1|Convention Center|San Francisco, CA|500|WiFi, Parking, Catering|contact@convention.com
  2|Central Park|New York, NY|5000|Outdoor Space, Restrooms, Food Vendors|info@centralparkevents.org
  3|Downtown Loop|Chicago, IL|1000|Paved Surface, Water Stations, Medical Support|events@downtown.com

### 3. Tickets Data
- File Path: data/tickets.txt
- Field Order (pipe-delimited): ticket_id|event_id|ticket_type|price|available_count|sold_count
- Description: Stores ticket types and availability per event.
- Examples:
  1|1|General|49.99|500|150
  2|1|VIP|99.99|100|45
  3|2|Early Bird|39.99|1000|750

### 4. Bookings Data
- File Path: data/bookings.txt
- Field Order (pipe-delimited): booking_id|event_id|customer_name|booking_date|ticket_count|ticket_type|total_amount|status
- Description: Stores user booking records.
- Examples:
  1|1|Alice Johnson|2025-02-01|2|General|99.98|Confirmed
  2|2|Bob Williams|2025-02-05|4|Early Bird|159.96|Confirmed
  3|1|Carol Davis|2025-02-10|1|VIP|99.99|Pending

### 5. Participants Data
- File Path: data/participants.txt
- Field Order (pipe-delimited): participant_id|event_id|name|email|booking_id|status|registration_date
- Description: Stores participant information linked to bookings.
- Examples:
  1|1|Alice Johnson|alice@email.com|1|Confirmed|2025-02-01
  2|1|Michael Johnson|michael@email.com|1|Confirmed|2025-02-01
  3|2|Bob Williams|bob@email.com|2|Attended|2025-02-05

### 6. Schedules Data
- File Path: data/schedules.txt
- Field Order (pipe-delimited): schedule_id|event_id|session_title|session_time|duration_minutes|speaker|venue_id
- Description: Stores event schedule sessions.
- Examples:
  1|1|Opening Keynote|2025-03-15 09:00|60|John Smith|1
  2|1|Panel Discussion|2025-03-15 10:30|90|Expert Panel|1
  3|2|Headliner Performance|2025-06-20 20:00|120|International Artist|2
