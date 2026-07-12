# Design Specification for EventPlanning Flask Application

## Section 1: Flask Routes Specification

| URL Path           | Description                          | Handler Function       | Methods    | Template                       | Notes                                            |
|--------------------|----------------------------------|---------------------|----------|-------------------------------|--------------------------------------------------|
| /                  | Dashboard page - start page       | dashboard            | GET      | dashboard.html                | Includes upcoming events, featured events block |
| /events            | Events overview page               | events               | GET      | events.html                   | Search/filter events by location/category       |
| /events/<event_id>  | Event details page                 | event_details        | GET, POST| event_details.html            | Display event info, book ticket functionality    |
| /tickets           | Ticket selection/booking page      | tickets              | GET, POST| tickets.html                  | Select tickets for events                        |
| /participants       | Participants management page       | participants         | GET, POST| participants.html              | Manage event participants                        |
| /venues             | Venues information page            | venues               | GET      | venues.html                   | Search/filter venues                             |
| /schedules          | Event schedules page               | schedules            | GET      | schedules.html                | Filter schedules by date/event                   |
| /bookings          | Booking summary page               | bookings             | GET, POST| bookings.html                 | Manage and view bookings                          |


## Section 2: Template Specifications

### 1. dashboard.html
- Page title: "Dashboard"
- Elements:
  - Div with id="dashboard-page": container for dashboard
  - Section id="featured-events": display of featured events
  - Button id="upcoming-events-button": navigate to /events
  - Div id="tickets-info": summary display

### 2. events.html
- Page title: "Events"
- Elements:
  - Div id="events-overview": container for events list
  - Input id="search-location": text input to filter events by location/date
  - Dropdown id="category-filter": filter events by category
  - Div id="events-grid": grid displaying event cards
  - Button ids="view-event-button-<event_id>": buttons to view event details

### 3. event_details.html
- Page title: "Event Details"
- Elements:
  - Div id="event-details-page": container for details
  - H1 id="event-title": event name
  - Div id="event-location": event location
  - Div id="event-description": event description
  - Button id="book-ticket-button": book ticket for event

### 4. tickets.html
- Page title: "Your Tickets"
- Elements:
  - Div id="ticket-page": container for ticket booking UI
  - Dropdown id="ticket-type-select": select ticket type
  - Input id="ticket-quantity-input": select quantity
  - Div id="confirmation-details": display booking confirmation

### 5. participants.html
- Page title: "Participants Management"
- Elements:
  - Div id="participants-page": container
  - Table id="participants-table": list of participants with columns including status
  - Input id="search-participant-input": search field
  - Dropdown id="participant-status-filter": filter by status
  - Button id="add-participant-button": add new participant

### 6. venues.html
- Page title: "Venues"
- Elements:
  - Div id="venues-container": container for venues list
  - Input id="search-venue-location": search venues by location or attributes
  - Dropdown id="venue-type-filter": filter venues by type
  - Div id="venues-grid": grid of venue cards
  - Button ids="view-venue-details-<venue_id>": view venue details

### 7. schedules.html
- Page title: "Event Schedules"
- Elements:
  - Div id="schedules-overview": container for schedules
  - Input id="schedule-date-filter": filter schedules by date
  - Dropdown id="schedule-event-filter": filter schedules by event
  - Button id="refresh-schedules-button": refresh schedule list

### 8. bookings.html
- Page title: "Booking Summary"
- Elements:
  - Table id="bookings-table": list of bookings
  - Input id="booking-search-input": search bookings
  - Button ids="cancel-booking-button-<booking_id>": cancel booking
  - Button id="back-to-dashboard": navigate back to dashboard


## Section 3: Data File Specifications

### 1. events.txt
- Fields (pipe '|' delimited): event_id (int), event_name (str), location (str), description (str), category_id (int), max_tickets (int)
- Example:
  ```
  1|Conference|San Francisco|Annual conference on latest innovations|1|500
  2|Festival|New York|International artists festival|2|5000
  3|Marathon|Chicago|Loop event with community run|3|1500
  ```

### 2. venues.txt
- Fields: venue_id, name, location, capacity, amenities (comma-separated), contact_email
- Example:
  ```
  1|Central Park|New York, NY|5000|Outdoor Space, Restrooms, Food Vendors|info@centralparkevents.org
  3|Downtown Loop|Chicago|3000|Surface, Medical
  ```

### 3. tickets.txt
- Fields: ticket_id, event_id, ticket_type, price, quantity_available, min_purchase
- Example:
  ```
  1|1|General|49.99|500|150
  3|2|Early Bird|39.99|200|100
  ```

### 4. bookings.txt
- Fields: participant_name, booking_date, ticket_quantity, ticket_type, total_price, status
- Example:
  ```
  Alice Johnson|2025-02-01|2|General|99.98|Confirmed
  Bob Williams|2025-02-05|4|Early Bird|159.96|Confirmed
  ```

### 5. participants.txt
- Fields: participant_id, event_id, name, email, booking_id, status, registration_date
- Example:
  ```
  1|1|Alice Johnson|alice@email.com|1|Confirmed|2025-02-01
  2|1|Bob Williams|bob@email.com|2|Attended|2025-02-05
  ```

### 6. schedules.txt
- Fields: schedule_id, event_id, session_name, start_datetime, duration_minutes, speaker_name, session_room
- Example:
  ```
  1|1|Opening Keynote|2025-03-15 09:00|60|John Smith|Room 1
  2|1|Panel Discussion|2025-03-15 10:15|45|Panelists|Room 1
  ```


## Notes
- All IDs and fields are to be handled exactly as specified.
- Use consistent naming conventions for Flask route handlers and HTML file names.
- Use Flask's url_for for URL generation in Jinja2 templates.
- POST methods used for actions like booking tickets or adding participants where required.
- No undocumented fields or routes; all must match requirements exactly.
