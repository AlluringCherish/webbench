# EventPlanning Web Application Design Specification

## Section 1: Page Layout and Element IDs

### 1. Dashboard Page
- **Page Title:** Event Planning Dashboard
- **Overview:** Main hub with upcoming events, featured venues, and quick navigation.
- **Elements:**
  - Div: `dashboard-page` (container for the whole page)
  - Div: `featured-events` (display featured event recommendations)
  - Button: `browse-events-button` (navigate to Events Listing page)
  - Button: `view-tickets-button` (navigate to Bookings Summary page)
  - Button: `venues-button` (navigate to Venue Information page)
  - Button: `participants-button` (navigate to Participants Management page)
  - Button: `schedules-button` (navigate to Event Schedules page)

### 2. Events Listing Page
- **Page Title:** Events Catalog
- **Overview:** Display all available events with search and filter functionality.
- **Elements:**
  - Div: `events-page` (container)
  - Input (text): `event-search-input` (search by name, location, or date)
  - Dropdown: `event-category-filter` (filter by category: Conference, Concert, Sports, Workshop, Social)
  - Div: `events-grid` (grid layout for event cards)
  - Button on each event card: `view-event-button-{event_id}` (view event details)

### 3. Event Details Page
- **Page Title:** Event Details
- **Overview:** Detailed info about a specific event.
- **Elements:**
  - Div: `event-details-page` (container)
  - H1: `event-title`
  - Div: `event-date` (date and time)
  - Div: `event-location`
  - Div: `event-description`
  - Button: `book-ticket-button` (navigate to Ticket Booking for this event)

### 4. Ticket Booking Page
- **Page Title:** Book Your Tickets
- **Overview:** Select and book tickets.
- **Elements:**
  - Div: `ticket-booking-page` (container)
  - Dropdown: `select-event-dropdown` (select event)
  - Input (number): `ticket-quantity-input` (ticket quantity)
  - Dropdown: `ticket-type-select` (ticket type: General, VIP, Early Bird)
  - Button: `book-now-button` (submit booking)
  - Div: `booking-confirmation` (show booking confirmation details)

### 5. Participants Management Page
- **Page Title:** Participants Management
- **Overview:** Manage event participants.
- **Elements:**
  - Div: `participants-page` (container)
  - Table: `participants-table` (columns: name, email, event, status)
  - Button: `add-participant-button` (add new participant)
  - Input (text): `search-participant-input` (search participants by name or email)
  - Dropdown: `participant-status-filter` (filter status: Registered, Confirmed, Attended)

### 6. Venue Information Page
- **Page Title:** Venues
- **Overview:** List and details of venues.
- **Elements:**
  - Div: `venues-page` (container)
  - Input (text): `venue-search-input` (search by name or location)
  - Dropdown: `venue-capacity-filter` (filter capacity: Small, Medium, Large)
  - Div: `venues-grid` (venue cards)
  - Button on each venue card: `view-venue-details-{venue_id}` (view venue details)

### 7. Event Schedules Page
- **Page Title:** Event Schedules
- **Overview:** Timelines and agenda of events.
- **Elements:**
  - Div: `schedules-page` (container)
  - Input (date): `schedule-filter-date` (filter schedules by date)
  - Dropdown: `schedule-filter-event` (filter by event)
  - Div: `schedules-timeline` (timeline of sessions)
  - Button: `export-schedule-button` (export schedule data)

### 8. Bookings Summary Page
- **Page Title:** My Bookings
- **Overview:** User's bookings information.
- **Elements:**
  - Div: `bookings-page` (container)
  - Input (text): `booking-search-input` (search by event name or booking id)
  - Table: `bookings-table` (columns: event, date, ticket count, status)
  - Button on each booking row: `cancel-booking-button-{booking_id}` (cancel booking)
  - Button: `back-to-dashboard` (navigate back to Dashboard)

## Section 2: Navigation Flow

- **Start Page:** Dashboard Page (`dashboard-page`)
- From Dashboard:
  - `browse-events-button` ➔ Events Listing Page
  - `view-tickets-button` ➔ Bookings Summary Page
  - `venues-button` ➔ Venue Information Page
  - `participants-button` ➔ Participants Management Page
  - `schedules-button` ➔ Event Schedules Page

- From Events Listing:
  - `view-event-button-{event_id}` ➔ Event Details Page
  - Navigation back to Dashboard possible via header or breadcrumb (not explicitly listed)

- From Event Details:
  - `book-ticket-button` ➔ Ticket Booking Page (event pre-selected)
  - Navigation back to Events Listing or Dashboard

- From Ticket Booking:
  - After booking via `book-now-button`, show confirmation in `booking-confirmation`
  - Navigation back to Event Details or Dashboard

- From Participants Management:
  - Navigation back to Dashboard

- From Venue Information:
  - `view-venue-details-{venue_id}` ➔ Venue detail view (if implemented), else modal
  - Navigation back to Dashboard

- From Event Schedules:
  - Navigation back to Dashboard

- From Bookings Summary:
  - `cancel-booking-button-{booking_id}` cancels booking
  - `back-to-dashboard` returns to Dashboard

## Section 3: Local Data File Structures

### 1. events.txt
- Format: `event_id|event_name|category|date|time|location|description|venue_id|capacity`
- Example:
  ```
  1|Tech Conference 2025|Conference|2025-03-15|09:00|Convention Center, San Francisco|Annual technology conference discussing latest innovations|1|500
  2|Summer Music Festival|Concert|2025-06-20|18:00|Central Park, New York|Three-day music festival with international artists|2|5000
  3|Marathon Championship|Sports|2025-04-10|07:00|Downtown Loop, Chicago|Annual city marathon event for all skill levels|3|1000
  ```

### 2. venues.txt
- Format: `venue_id|venue_name|location|capacity|amenities|contact`
- Example:
  ```
  1|Convention Center|San Francisco, CA|500|WiFi, Parking, Catering|contact@convention.com
  2|Central Park|New York, NY|5000|Outdoor Space, Restrooms, Food Vendors|info@centralparkevents.org
  3|Downtown Loop|Chicago, IL|1000|Paved Surface, Water Stations, Medical Support|events@downtown.com
  ```

### 3. tickets.txt
- Format: `ticket_id|event_id|ticket_type|price|available_count|sold_count`
- Example:
  ```
  1|1|General|49.99|500|150
  2|1|VIP|99.99|100|45
  3|2|Early Bird|39.99|1000|750
  ```

### 4. bookings.txt
- Format: `booking_id|event_id|customer_name|booking_date|ticket_count|ticket_type|total_amount|status`
- Example:
  ```
  1|1|Alice Johnson|2025-02-01|2|General|99.98|Confirmed
  2|2|Bob Williams|2025-02-05|4|Early Bird|159.96|Confirmed
  3|1|Carol Davis|2025-02-10|1|VIP|99.99|Pending
  ```

### 5. participants.txt
- Format: `participant_id|event_id|name|email|booking_id|status|registration_date`
- Example:
  ```
  1|1|Alice Johnson|alice@email.com|1|Confirmed|2025-02-01
  2|1|Michael Johnson|michael@email.com|1|Confirmed|2025-02-01
  3|2|Bob Williams|bob@email.com|2|Attended|2025-02-05
  ```

### 6. schedules.txt
- Format: `schedule_id|event_id|session_title|session_time|duration_minutes|speaker|venue_id`
- Example:
  ```
  1|1|Opening Keynote|2025-03-15 09:00|60|John Smith|1
  2|1|Panel Discussion|2025-03-15 10:30|90|Expert Panel|1
  3|2|Headliner Performance|2025-06-20 20:00|120|International Artist|2
  ```

---

This design specification fully covers the required pages, element IDs, navigation flow, and data file structures as per the user task description.