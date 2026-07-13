# EventPlanning Web Application Design Specification

---

## Section 1: Page Layout and Element IDs

### 1. Dashboard Page
- Page Title: Event Planning Dashboard
- Overview: Main hub displaying upcoming events, featured venues, and quick navigation to functionalities.
- Elements:
  - ID: dashboard-page (Div): Container for the dashboard page.
  - ID: featured-events (Div): Display of featured event recommendations.
  - ID: featured-venues (Div): Display of featured venues.
  - ID: browse-events-button (Button): Navigate to Events Listing page.
  - ID: view-tickets-button (Button): Navigate to Bookings Summary page.
  - ID: venues-button (Button): Navigate to Venue Information page.
  - ID: participants-button (Button): Navigate to Participants Management page.
  - ID: schedules-button (Button): Navigate to Event Schedules page.

### 2. Events Listing Page
- Page Title: Events Catalog
- Overview: Displays all events with search and filter capabilities.
- Elements:
  - ID: events-page (Div): Container for events listing.
  - ID: event-search-input (Input, text): Search events by name, location, or date.
  - ID: event-category-filter (Dropdown): Filter by category (Conference, Concert, Sports, Workshop, Social).
  - ID: events-grid (Div): Grid displaying event cards.
    - Each event card contains:
      - ID: view-event-button-{event_id} (Button): View event details.

### 3. Event Details Page
- Page Title: Event Details
- Overview: Display detailed information for a specific event.
- Elements:
  - ID: event-details-page (Div): Container for event details.
  - ID: event-title (H1): Event title.
  - ID: event-date (Div): Event date and time.
  - ID: event-location (Div): Event location.
  - ID: event-description (Div): Event detailed description.
  - ID: book-ticket-button (Button): Book ticket for this event.

### 4. Ticket Booking Page
- Page Title: Book Your Tickets
- Overview: Users select and book tickets for events.
- Elements:
  - ID: ticket-booking-page (Div): Container for ticket booking.
  - ID: select-event-dropdown (Dropdown): Select event to book tickets.
  - ID: ticket-quantity-input (Input, number): Enter number of tickets.
  - ID: ticket-type-select (Dropdown): Select ticket type (General, VIP, Early Bird).
  - ID: book-now-button (Button): Proceed with ticket booking.
  - ID: booking-confirmation (Div): Display booking confirmation details.

### 5. Participants Management Page
- Page Title: Participants Management
- Overview: Manage event participants and attendee lists.
- Elements:
  - ID: participants-page (Div): Container for participants management.
  - ID: participants-table (Table): Columns - Name, Email, Event, Status.
  - ID: add-participant-button (Button): Add new participant.
  - ID: search-participant-input (Input, text): Search participants by name or email.
  - ID: participant-status-filter (Dropdown): Filter by status (Registered, Confirmed, Attended).

### 6. Venue Information Page
- Page Title: Venues
- Overview: Display venues with detailed info.
- Elements:
  - ID: venues-page (Div): Container for venue information.
  - ID: venues-grid (Div): Grid displaying venue cards.
    - Each venue card contains:
      - ID: view-venue-details-{venue_id} (Button): View venue details.
  - ID: venue-search-input (Input, text): Search venues by name or location.
  - ID: venue-capacity-filter (Dropdown): Filter by capacity (Small, Medium, Large).

### 7. Event Schedules Page
- Page Title: Event Schedules
- Overview: Display event schedules, timelines, agenda.
- Elements:
  - ID: schedules-page (Div): Container for schedules.
  - ID: schedules-timeline (Div): Timeline view of events/sessions.
  - ID: schedule-filter-date (Input, date): Filter schedules by date.
  - ID: schedule-filter-event (Dropdown): Filter schedules by event.
  - ID: export-schedule-button (Button): Export schedule data.

### 8. Bookings Summary Page
- Page Title: My Bookings
- Overview: Display user bookings with ticket and status info.
- Elements:
  - ID: bookings-page (Div): Container for bookings summary.
  - ID: bookings-table (Table): Columns - Event, Date, Ticket Count, Status.
  - ID: booking-search-input (Input, text): Search bookings by event name or booking ID.
  - ID: cancel-booking-button-{booking_id} (Button): Cancel booking.
  - ID: back-to-dashboard (Button): Navigate back to Dashboard page.

---

## Section 2: Navigation Flow

- Initial page: Dashboard (dashboard-page).
- Dashboard navigation:
  - browse-events-button -> Events Listing page (events-page).
  - view-tickets-button -> Bookings Summary page (bookings-page).
  - venues-button -> Venue Information page (venues-page).
  - participants-button -> Participants Management page (participants-page).
  - schedules-button -> Event Schedules page (schedules-page).

- Events Listing page:
  - view-event-button-{event_id} -> Event Details page (event-details-page) for selected event.
  - Back to Dashboard via explicit or breadcrumb navigation (optional).

- Event Details page:
  - book-ticket-button -> Ticket Booking page (ticket-booking-page), pre-selected event.
  - Back to Events Listing or Dashboard via navigation.

- Ticket Booking page:
  - book-now-button -> Displays booking-confirmation on same page.
  - Option to navigate back to Event Details or Dashboard.

- Participants Management page:
  - add-participant-button -> Opens participant addition form/modal.
  - Back to Dashboard via navigation.

- Venue Information page:
  - view-venue-details-{venue_id} -> Detailed view modal or page (not defined explicitly here).
  - Back to Dashboard via navigation.

- Event Schedules page:
  - export-schedule-button -> Exports schedules data.
  - Back to Dashboard via navigation.

- Bookings Summary page:
  - cancel-booking-button-{booking_id} -> Cancel booking action.
  - back-to-dashboard -> Dashboard page.

---

## Section 3: Local Data File Structures

Data files are located in the 'data' directory.

### 1. events.txt
- Format:
  event_id|event_name|category|date|time|location|description|venue_id|capacity
- Example:
  1|Tech Conference 2025|Conference|2025-03-15|09:00|Convention Center, San Francisco|Annual technology conference discussing latest innovations|1|500
  2|Summer Music Festival|Concert|2025-06-20|18:00|Central Park, New York|Three-day music festival with international artists|2|5000
  3|Marathon Championship|Sports|2025-04-10|07:00|Downtown Loop, Chicago|Annual city marathon event for all skill levels|3|1000

### 2. venues.txt
- Format:
  venue_id|venue_name|location|capacity|amenities|contact
- Example:
  1|Convention Center|San Francisco, CA|500|WiFi, Parking, Catering|contact@convention.com
  2|Central Park|New York, NY|5000|Outdoor Space, Restrooms, Food Vendors|info@centralparkevents.org
  3|Downtown Loop|Chicago, IL|1000|Paved Surface, Water Stations, Medical Support|events@downtown.com

### 3. tickets.txt
- Format:
  ticket_id|event_id|ticket_type|price|available_count|sold_count
- Example:
  1|1|General|49.99|500|150
  2|1|VIP|99.99|100|45
  3|2|Early Bird|39.99|1000|750

### 4. bookings.txt
- Format:
  booking_id|event_id|customer_name|booking_date|ticket_count|ticket_type|total_amount|status
- Example:
  1|1|Alice Johnson|2025-02-01|2|General|99.98|Confirmed
  2|2|Bob Williams|2025-02-05|4|Early Bird|159.96|Confirmed
  3|1|Carol Davis|2025-02-10|1|VIP|99.99|Pending

### 5. participants.txt
- Format:
  participant_id|event_id|name|email|booking_id|status|registration_date
- Example:
  1|1|Alice Johnson|alice@email.com|1|Confirmed|2025-02-01
  2|1|Michael Johnson|michael@email.com|1|Confirmed|2025-02-01
  3|2|Bob Williams|bob@email.com|2|Attended|2025-02-05

### 6. schedules.txt
- Format:
  schedule_id|event_id|session_title|session_time|duration_minutes|speaker|venue_id
- Example:
  1|1|Opening Keynote|2025-03-15 09:00|60|John Smith|1
  2|1|Panel Discussion|2025-03-15 10:30|90|Expert Panel|1
  3|2|Headliner Performance|2025-06-20 20:00|120|International Artist|2

---

End of specification.
