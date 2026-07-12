# EventPlanning Web Application Design Specification

---

## Section 1: Flask Routes Specification

| Route Path              | Function Name           | HTTP Methods | Template File         | Context Variables Description                                                                                             |
|-------------------------|-------------------------|--------------|-----------------------|--------------------------------------------------------------------------------------------------------------------------|
| `/`                     | `root_redirect`          | GET          | None (redirect)        | No variables. Redirects to `/dashboard`.                                                                                  |
| `/dashboard`            | `dashboard`              | GET          | `dashboard.html`       | `featured_events`: List of dicts with event summary data (event_id: int, event_name: str, date: str), representing featured events to display on dashboard. |
| `/events`               | `events_listing`         | GET          | `events.html`          | `events`: List of event dicts with full event info (event_id:int, event_name:str, category:str, date:str, location:str). Categories used for filtering in front-end as well.           |
| `/event/<int:event_id>` | `event_details`          | GET          | `event_details.html`   | `event`: Dict with detailed event data (event_id:int, event_name:str, date:str, time:str, location:str, description:str, venue_id:int, capacity:int).  |
| `/book_ticket`          | `book_ticket`            | GET, POST   | `ticket_booking.html`  | GET: `events` (list of dicts): all events for dropdown. POST: `booking_confirmation` (dict): Confirmation details with booking info (booking_id:str/int, status:str). Errors may be handled on page.    |
| `/participants`         | `participants_management`| GET          | `participants.html`    | `participants`: List of dicts with participant info (participant_id:int, name:str, email:str, event_id:int, event_name:str, status:str). Filters available client-side by status etc.         |
| `/add_participant`      | `add_participant`        | POST         | None (redirect)        | Processes participant add form data; redirects back to `/participants` with updated list. No direct template rendered.      |
| `/venues`               | `venues`                 | GET          | `venues.html`          | `venues`: List of dicts with venue details (venue_id:int, venue_name:str, location:str, capacity:int, amenities:str), for display and filtering.                       |
| `/venue/<int:venue_id>` | `venue_details`          | GET          | `venue_details.html`*  | Not specified in user doc, no separate page detailed for venue details, so this route excluded as per instructions.        |
| `/schedules`            | `event_schedules`        | GET          | `schedules.html`       | `schedules`: List of dicts with schedule info (schedule_id:int, event_id:int, session_title:str, session_time:str, duration_minutes:int, speaker:str, venue_id:int).  | Filters applied in UI using date and event dropdown.  |
| `/bookings`             | `bookings_summary`       | GET          | `bookings.html`        | `bookings`: List of dicts with booking info (booking_id:int, event_id:int, event_name:str, date:str, ticket_count:int, status:str).                                     |
| `/cancel_booking/<int:booking_id>` | `cancel_booking` | POST         | None (redirect)        | Processes booking cancellation; redirects to `/bookings`. No direct template rendered.                                     |

*Note: Venue details page route is not explicitly required in the given specification hence it is omitted.

---

## Section 2: HTML Template Specifications

### 1. Dashboard Page
- Template file: `templates/dashboard.html`
- Page Title: `Event Planning Dashboard`
- Element IDs:
  - `dashboard-page` (Div): container for dashboard page
  - `featured-events` (Div): displays featured event recommendations
  - `browse-events-button` (Button): navigates to `/events`
  - `view-tickets-button` (Button): navigates to `/bookings`
  - `venues-button` (Button): navigates to `/venues`
- Context Variables:
  - `featured_events`: List of dicts each with `event_id` (int), `event_name` (str), `date` (str)
- Navigation Buttons:
  - `browse-events-button`: url_for('events_listing')
  - `view-tickets-button`: url_for('bookings_summary')
  - `venues-button`: url_for('venues')

---

### 2. Events Listing Page
- Template file: `templates/events.html`
- Page Title: `Events Catalog`
- Element IDs:
  - `events-page` (Div): container for events listing
  - `event-search-input` (Input): search field for events
  - `event-category-filter` (Dropdown): filter events by category (Conference, Concert, Sports, Workshop, Social)
  - `events-grid` (Div): grid displaying event cards
  - `view-event-button-{event_id}` (Button): each event card's button to view details; dynamic ID uses Jinja2 loop variable
- Context Variables:
  - `events`: List of dicts each with `event_id` (int), `event_name` (str), `category` (str), `date` (str), `location` (str)
- Navigation Buttons:
  - Navigation back to dashboard or others not specified, likely from page header or footer if needed.
- Dynamic ID Instructions:
  - Render `view-event-button-{{ event.event_id }}` inside the for loop over `events`.

---

### 3. Event Details Page
- Template file: `templates/event_details.html`
- Page Title: `Event Details`
- Element IDs:
  - `event-details-page` (Div): container
  - `event-title` (H1): event title display
  - `event-date` (Div): event date and time
  - `event-location` (Div): event location
  - `event-description` (Div): detailed description
  - `book-ticket-button` (Button): to proceed to ticket booking
- Context Variables:
  - `event`: dict with keys `event_id`, `event_name`, `date`, `time`, `location`, `description`, `venue_id`, `capacity`
- Navigation Buttons:
  - `book-ticket-button`: url_for('book_ticket') with event selection prefilled if passing via query param is desired

---

### 4. Ticket Booking Page
- Template file: `templates/ticket_booking.html`
- Page Title: `Book Your Tickets`
- Element IDs:
  - `ticket-booking-page` (Div): container
  - `select-event-dropdown` (Dropdown): select event to book tickets
  - `ticket-quantity-input` (Input: number): enter number of tickets
  - `ticket-type-select` (Dropdown): select ticket type (General, VIP, Early Bird)
  - `book-now-button` (Button): submit booking
  - `booking-confirmation` (Div): display confirmation message/details
- Context Variables:
  - GET: `events`: list of dicts with event_id, event_name, etc., to populate dropdown
  - POST: `booking_confirmation`: dict with booking details for confirmation display
- Navigation Buttons:
  - Typically a back to dashboard or events page may be included, but not specified explicitly.

---

### 5. Participants Management Page
- Template file: `templates/participants.html`
- Page Title: `Participants Management`
- Element IDs:
  - `participants-page` (Div): container
  - `participants-table` (Table): participants data
  - `add-participant-button` (Button): add new participant
  - `search-participant-input` (Input): search participants
  - `participant-status-filter` (Dropdown): filter by status (Registered, Confirmed, Attended)
- Context Variables:
  - `participants`: List of dicts with fields `participant_id`, `name`, `email`, `event_id`, `event_name` (can derive from event_id), `status`
- Navigation Buttons:
  - Add participant button triggers POST action to add participant endpoint

---

### 6. Venue Information Page
- Template file: `templates/venues.html`
- Page Title: `Venues`
- Element IDs:
  - `venues-page` (Div): container
  - `venues-grid` (Div): grid of venue cards
  - `venue-search-input` (Input): search venues
  - `venue-capacity-filter` (Dropdown): filter by capacity (Small, Medium, Large)
  - `view-venue-details-{venue_id}` (Button): dynamic view details button per venue
- Context Variables:
  - `venues`: List of dicts with `venue_id`, `venue_name`, `location`, `capacity`, `amenities`
- Navigation Buttons:
  - Dynamic buttons use `view-venue-details-{{ venue.venue_id }}` inside venue listing loop

---

### 7. Event Schedules Page
- Template file: `templates/schedules.html`
- Page Title: `Event Schedules`
- Element IDs:
  - `schedules-page` (Div): container
  - `schedules-timeline` (Div): timeline display
  - `schedule-filter-date` (Input: date): filter schedules by date
  - `schedule-filter-event` (Dropdown): filter schedules by event
  - `export-schedule-button` (Button): export schedule data
- Context Variables:
  - `schedules`: List of dicts with schedule details (schedule_id, event_id, session_title, session_time, duration_minutes, speaker, venue_id)
- Navigation Buttons:
  - Not explicitly specified but likely includes export and back navigation if needed

---

### 8. Bookings Summary Page
- Template file: `templates/bookings.html`
- Page Title: `My Bookings`
- Element IDs:
  - `bookings-page` (Div): container
  - `bookings-table` (Table): bookings listing
  - `booking-search-input` (Input): search bookings
  - `cancel-booking-button-{booking_id}` (Button): dynamic cancel button per booking
  - `back-to-dashboard` (Button): button to go back to dashboard
- Context Variables:
  - `bookings`: List of dicts with `booking_id`, `event_id`, `event_name`, `date`, `ticket_count`, `status`
- Navigation Buttons:
  - `back-to-dashboard`: url_for('dashboard')
  - Dynamic cancel buttons rendered as `cancel-booking-button-{{ booking.booking_id }}` inside loop

---

## Section 3: Data File Schemas

### 1. Events Data
- File path: `data/events.txt`
- Fields (pipe-delimited):
  `event_id|event_name|category|date|time|location|description|venue_id|capacity`
- Description: Stores event details including category, scheduling, location, and venue reference.
- Example rows:
  ```
  1|Tech Conference 2025|Conference|2025-03-15|09:00|Convention Center, San Francisco|Annual technology conference discussing latest innovations|1|500
  2|Summer Music Festival|Concert|2025-06-20|18:00|Central Park, New York|Three-day music festival with international artists|2|5000
  3|Marathon Championship|Sports|2025-04-10|07:00|Downtown Loop, Chicago|Annual city marathon event for all skill levels|3|1000
  ```

### 2. Venues Data
- File path: `data/venues.txt`
- Fields (pipe-delimited):
  `venue_id|venue_name|location|capacity|amenities|contact`
- Description: Stores venue information including capacities, amenities, and contact details.
- Example rows:
  ```
  1|Convention Center|San Francisco, CA|500|WiFi, Parking, Catering|contact@convention.com
  2|Central Park|New York, NY|5000|Outdoor Space, Restrooms, Food Vendors|info@centralparkevents.org
  3|Downtown Loop|Chicago, IL|1000|Paved Surface, Water Stations, Medical Support|events@downtown.com
  ```

### 3. Tickets Data
- File path: `data/tickets.txt`
- Fields (pipe-delimited):
  `ticket_id|event_id|ticket_type|price|available_count|sold_count`
- Description: Stores ticket types for each event with pricing and availability.
- Example rows:
  ```
  1|1|General|49.99|500|150
  2|1|VIP|99.99|100|45
  3|2|Early Bird|39.99|1000|750
  ```

### 4. Bookings Data
- File path: `data/bookings.txt`
- Fields (pipe-delimited):
  `booking_id|event_id|customer_name|booking_date|ticket_count|ticket_type|total_amount|status`
- Description: Stores user booking records including ticket quantity, type, and status.
- Example rows:
  ```
  1|1|Alice Johnson|2025-02-01|2|General|99.98|Confirmed
  2|2|Bob Williams|2025-02-05|4|Early Bird|159.96|Confirmed
  3|1|Carol Davis|2025-02-10|1|VIP|99.99|Pending
  ```

### 5. Participants Data
- File path: `data/participants.txt`
- Fields (pipe-delimited):
  `participant_id|event_id|name|email|booking_id|status|registration_date`
- Description: Stores information on event participants, their status, and registration reference.
- Example rows:
  ```
  1|1|Alice Johnson|alice@email.com|1|Confirmed|2025-02-01
  2|1|Michael Johnson|michael@email.com|1|Confirmed|2025-02-01
  3|2|Bob Williams|bob@email.com|2|Attended|2025-02-05
  ```

### 6. Schedules Data
- File path: `data/schedules.txt`
- Fields (pipe-delimited):
  `schedule_id|event_id|session_title|session_time|duration_minutes|speaker|venue_id`
- Description: Stores agenda and session info for events including timing and speaker details.
- Example rows:
  ```
  1|1|Opening Keynote|2025-03-15 09:00|60|John Smith|1
  2|1|Panel Discussion|2025-03-15 10:30|90|Expert Panel|1
  3|2|Headliner Performance|2025-06-20 20:00|120|International Artist|2
  ```

---

# End of Design Specification

This specification enables independent development of backend Flask application routes, frontend HTML templates, and data file loading for the EventPlanning app with no assumptions beyond provided requirements.