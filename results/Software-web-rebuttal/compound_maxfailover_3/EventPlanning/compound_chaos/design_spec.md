# EventPlanning - Design Specification Document

---

## Section 1: Flask Routes Specification

| Route Path                  | Function Name           | HTTP Methods | Template Files           | Context Variables                                               |
|-----------------------------|-------------------------|--------------|--------------------------|----------------------------------------------------------------|
| /                           | dashboard_page          | GET          | dashboard.html           | featured_events: list of dicts {event_id:int, event_name:str, category:str, date:str, time:str, location:str, description:str, venue_id:int, capacity:int}
|                             |                         |              |                          | (subset of events marked featured)
|                             |                         |              |                          | - No additional vars specified for buttons
| /events                     | events_listing_page     | GET          | events.html              | events: list of dicts {event_id:int, event_name:str, category:str, date:str, time:str, location:str, description:str, venue_id:int, capacity:int}
|                             |                         |              |                          | - Used to show event cards
| /event/<int:event_id>        | event_details_page      | GET          | event_details.html       | event: dict {event_id:int, event_name:str, category:str, date:str, time:str, location:str, description:str, venue_id:int, capacity:int}
|                             |                         |              |                          | - Detailed event info
| /book_ticket                 | ticket_booking_page     | GET, POST    | ticket_booking.html      | GET:
|                             |                         |              |                          | events: list of dicts (id, name)
|                             |                         |              |                          | tickets: list of dicts {ticket_type:str, price:float}
|                             |                         | POST:
|                             |                         |                          | form data: event_id, ticket_type, ticket_quantity (processed server-side)
| /participants               | participants_management | GET          | participants.html        | participants: list of dicts {participant_id:int, event_id:int, name:str, email:str, booking_id:int, status:str, registration_date:str}
| /venues                     | venues_page             | GET          | venues.html              | venues: list of dicts {venue_id:int, venue_name:str, location:str, capacity:int, amenities:str, contact:str}
| /schedules                  | schedules_page          | GET          | schedules.html           | schedules: list of dicts {schedule_id:int, event_id:int, session_title:str, session_time:str, duration_minutes:int, speaker:str, venue_id:int}
|                             |                         |              |                          | events: list of dicts for filtering
| /bookings                  | bookings_summary_page   | GET          | bookings.html            | bookings: list of dicts {booking_id:int, event_id:int, customer_name:str, booking_date:str, ticket_count:int, ticket_type:str, total_amount:float, status:str}



---

## Section 2: HTML Template Specifications

### 1. Dashboard Page
- Template File: templates/dashboard.html
- Page Title: "Event Planning Dashboard"
- Elements:
  - div#dashboard-page : main container
  - div#featured-events : display featured event cards (content dynamic)
  - button#browse-events-button : navigates to /events
  - button#view-tickets-button : navigates to /bookings
  - button#venues-button : navigates to /venues
- Context Variables:
  - featured_events: list of dict with event fields as per events.txt
- Navigation Buttons:
  - browse-events-button -> url_for('events_listing_page')
  - view-tickets-button -> url_for('bookings_summary_page')
  - venues-button -> url_for('venues_page')


### 2. Events Listing Page
- Template File: templates/events.html
- Page Title: "Events Catalog"
- Elements:
  - div#events-page : main container
  - input#event-search-input : text input for filtering events
  - select#event-category-filter : dropdown with options [Conference, Concert, Sports, Workshop, Social]
  - div#events-grid : grid containing event cards
    - Each card includes:
      - button#view-event-button-{{ event_id }} : to view event details
- Context Variables:
  - events: list of dict with all event fields
- Navigation:
  - view-event-button-{event_id} -> url_for('event_details_page', event_id=event_id)


### 3. Event Details Page
- Template File: templates/event_details.html
- Page Title: "Event Details"
- Elements:
  - div#event-details-page : container
  - h1#event-title : event title
  - div#event-date : event date and time
  - div#event-location : event location
  - div#event-description : detailed description
  - button#book-ticket-button : navigates to ticket booking, passes event_id
- Context Variables:
  - event: dict representing event
- Navigation:
  - book-ticket-button -> url_for('ticket_booking_page') plus event_id parameter


### 4. Ticket Booking Page
- Template File: templates/ticket_booking.html
- Page Title: "Book Your Tickets"
- Elements:
  - div#ticket-booking-page : container
  - select#select-event-dropdown : dropdown to select event
  - input#ticket-quantity-input : number input for ticket quantity
  - select#ticket-type-select : dropdown for ticket type (General, VIP, Early Bird)
  - button#book-now-button : submits booking
  - div#booking-confirmation : to show confirmation details on booking success
- Context Variables:
  - events: list of events for select menu
  - tickets: list of ticket types for selected event
- Navigation:
  - book-now-button POSTs data to /book_ticket


### 5. Participants Management Page
- Template File: templates/participants.html
- Page Title: "Participants Management"
- Elements:
  - div#participants-page : container
  - table#participants-table : displaying columns name, email, event, status
  - button#add-participant-button : adds new participant
  - input#search-participant-input : search field
  - select#participant-status-filter : filter dropdown with [Registered, Confirmed, Attended]
- Context Variables:
  - participants: list of participant dicts
- Navigation:
  - add-participant-button triggers participant addition UI


### 6. Venue Information Page
- Template File: templates/venues.html
- Page Title: "Venues"
- Elements:
  - div#venues-page : container
  - div#venues-grid : venue cards
    - button#view-venue-details-{{ venue_id }} : view venue details
  - input#venue-search-input : search venues
  - select#venue-capacity-filter : dropdown with [Small, Medium, Large]
- Context Variables:
  - venues: list of venue dicts
- Navigation:
  - view-venue-details-{venue_id} navigates to venue detail route (if implemented)


### 7. Event Schedules Page
- Template File: templates/schedules.html
- Page Title: "Event Schedules"
- Elements:
  - div#schedules-page : container
  - div#schedules-timeline : timeline view
  - input#schedule-filter-date : date input filter
  - select#schedule-filter-event : event dropdown filter
  - button#export-schedule-button : exports schedule data
- Context Variables:
  - schedules: list of schedule dicts
  - events: list of events for filtering
- Navigation:
  - export-schedule-button triggers schedule export


### 8. Bookings Summary Page
- Template File: templates/bookings.html
- Page Title: "My Bookings"
- Elements:
  - div#bookings-page : container
  - table#bookings-table : columns for event, date, ticket count, status
    - button#cancel-booking-button-{{ booking_id }} : cancel booking
  - input#booking-search-input : search bookings
  - button#back-to-dashboard : navigate back to dashboard
- Context Variables:
  - bookings: list of booking dicts
- Navigation:
  - cancel-booking-button-{booking_id} triggers booking cancellation
  - back-to-dashboard -> url_for('dashboard_page')


---

## Section 3: Data File Schemas

### 1. events.txt
- File path: data/events.txt
- Fields (pipe-delimited):
  event_id|event_name|category|date|time|location|description|venue_id|capacity
- Description: Stores data for each event.
- Example Rows (no header):
  1|Tech Conference 2025|Conference|2025-03-15|09:00|Convention Center, San Francisco|Annual technology conference discussing latest innovations|1|500
  2|Summer Music Festival|Concert|2025-06-20|18:00|Central Park, New York|Three-day music festival with international artists|2|5000
  3|Marathon Championship|Sports|2025-04-10|07:00|Downtown Loop, Chicago|Annual city marathon event for all skill levels|3|1000

### 2. venues.txt
- File path: data/venues.txt
- Fields (pipe-delimited):
  venue_id|venue_name|location|capacity|amenities|contact
- Description: Stores venue information.
- Example Rows (no header):
  1|Convention Center|San Francisco, CA|500|WiFi, Parking, Catering|contact@convention.com
  2|Central Park|New York, NY|5000|Outdoor Space, Restrooms, Food Vendors|info@centralparkevents.org
  3|Downtown Loop|Chicago, IL|1000|Paved Surface, Water Stations, Medical Support|events@downtown.com

### 3. tickets.txt
- File path: data/tickets.txt
- Fields (pipe-delimited):
  ticket_id|event_id|ticket_type|price|available_count|sold_count
- Description: Stores ticket data for each event.
- Example Rows (no header):
  1|1|General|49.99|500|150
  2|1|VIP|99.99|100|45
  3|2|Early Bird|39.99|1000|750

### 4. bookings.txt
- File path: data/bookings.txt
- Fields (pipe-delimited):
  booking_id|event_id|customer_name|booking_date|ticket_count|ticket_type|total_amount|status
- Description: Stores user bookings.
- Example Rows (no header):
  1|1|Alice Johnson|2025-02-01|2|General|99.98|Confirmed
  2|2|Bob Williams|2025-02-05|4|Early Bird|159.96|Confirmed
  3|1|Carol Davis|2025-02-10|1|VIP|99.99|Pending

### 5. participants.txt
- File path: data/participants.txt
- Fields (pipe-delimited):
  participant_id|event_id|name|email|booking_id|status|registration_date
- Description: Stores event participants data.
- Example Rows (no header):
  1|1|Alice Johnson|alice@email.com|1|Confirmed|2025-02-01
  2|1|Michael Johnson|michael@email.com|1|Confirmed|2025-02-01
  3|2|Bob Williams|bob@email.com|2|Attended|2025-02-05

### 6. schedules.txt
- File path: data/schedules.txt
- Fields (pipe-delimited):
  schedule_id|event_id|session_title|session_time|duration_minutes|speaker|venue_id
- Description: Stores schedules and sessions data.
- Example Rows (no header):
  1|1|Opening Keynote|2025-03-15 09:00|60|John Smith|1
  2|1|Panel Discussion|2025-03-15 10:30|90|Expert Panel|1
  3|2|Headliner Performance|2025-06-20 20:00|120|International Artist|2

---

# End of Design Specification
