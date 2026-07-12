# EventPlanning Web Application Design Specification

---

## Section 1: Flask Routes Specification

| Route Path                    | Function Name               | HTTP Methods | Template File            | Context Variables                                                                                                                                                               |
|-------------------------------|-----------------------------|--------------|--------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `/`                           | `root_redirect`              | GET          | None (redirect)           | None                                                                                                                                                                           |
| `/dashboard`                  | `dashboard`                  | GET          | `dashboard.html`          | `featured_events`: List[Dict] with keys `event_id` (int), `event_name` (str), `date` (str), `location` (str)                                                                  |
| `/events`                    | `events_listing`             | GET          | `events.html`             | `events`: List[Dict] with keys `event_id` (int), `event_name` (str), `category` (str), `date` (str), `location` (str), `description` (str), `venue_id` (int), `capacity` (int)
|                               |                             |              |                          | `categories`: List[str] with event category strings (Conference, Concert, Sports, Workshop, Social)                                                                           |
| `/events/search`              | `search_events`              | POST         | `events.html`             | Same as `/events` with filtered `events` list and `categories`                                                                                                               |
| `/event/<int:event_id>`       | `event_details`              | GET          | `event_details.html`      | `event`: Dict with keys `event_id` (int), `event_name` (str), `category` (str), `date` (str), `time` (str), `location` (str), `description` (str), `venue_id` (int), `capacity` (int) |
| `/book_ticket`               | `book_ticket`                | GET, POST    | `ticket_booking.html`     | GET: `events`: List[Dict] with `event_id` (int), `event_name` (str)
POST: `confirmation`: Dict with keys `event_name` (str), `ticket_count` (int), `ticket_type` (str), `total_amount` (float), `booking_status` (str)                          |
| `/participants`              | `participants_management`    | GET, POST    | `participants.html`       | `participants`: List[Dict] with keys `participant_id` (int), `name` (str), `email` (str), `event_name` (str), `status` (str)
POST reflects updated participants list                                                                                 |
| `/venues`                    | `venues`                    | GET          | `venues.html`             | `venues`: List[Dict] with keys `venue_id` (int), `venue_name` (str), `location` (str), `capacity` (int), `amenities` (str), `contact` (str)                                    |
| `/event_schedules`           | `event_schedules`            | GET          | `schedules.html`          | `schedules`: List[Dict] with keys `schedule_id` (int), `event_id` (int), `session_title` (str), `session_time` (str), `duration_minutes` (int), `speaker` (str), `venue_id` (int)
`events`: List[Dict] with `event_id` (int), `event_name` (str) for filtering                                                 |
| `/bookings`                  | `bookings_summary`           | GET          | `bookings.html`           | `bookings`: List[Dict] with keys `booking_id` (int), `event_name` (str), `date` (str), `ticket_count` (int), `status` (str)                                                  |
| `/booking/cancel/<int:booking_id>` | `cancel_booking`            | POST         | None (redirect)           | Redirects to `/bookings` after booking cancellation; no context variables                                                                                                   |

---

## Section 2: HTML Template Specifications

### 1. Dashboard Page
- Template File: `templates/dashboard.html`
- Page Title: "Event Planning Dashboard" (both `<title>` and `<h1>`)
- Element IDs:
  - `dashboard-page` (Div): main container
  - `featured-events` (Div): displays featured events
  - `browse-events-button` (Button): navigate to `/events`
  - `view-tickets-button` (Button): navigate to `/bookings`
  - `venues-button` (Button): navigate to `/venues`
- Context Variables:
  - `featured_events`: List[Dict] with `event_id`, `event_name`, `date`, `location`
- Navigation buttons:
  - `browse-events-button`: `url_for('events_listing')`
  - `view-tickets-button`: `url_for('bookings_summary')`
  - `venues-button`: `url_for('venues')`

### 2. Events Listing Page
- Template File: `templates/events.html`
- Page Title: "Events Catalog"
- Element IDs:
  - `events-page` (Div)
  - `event-search-input` (Input): search box
  - `event-category-filter` (Dropdown): category filter
  - `events-grid` (Div): container for event cards
  - dynamic `view-event-button-{{ event.event_id }}` (Button) for each event
- Context Variables:
  - `events`: List[Dict] each with full event details
  - `categories`: List[str] of categories
- Navigation buttons:
  - event detail via `url_for('event_details', event_id=event.event_id)`
- Rendering:
  - Jinja2 loop `{% for event in events %}` to render event cards
  - dynamic button id as `view-event-button-{{ event.event_id }}`

### 3. Event Details Page
- Template File: `templates/event_details.html`
- Page Title: "Event Details"
- Element IDs:
  - `event-details-page` (Div)
  - `event-title` (H1): event name
  - `event-date` (Div)
  - `event-location` (Div)
  - `event-description` (Div)
  - `book-ticket-button` (Button)
- Context Variables:
  - `event` Dict with event data
- Navigation:
  - `book-ticket-button` should link to `/book_ticket` possibly preselecting the event

### 4. Ticket Booking Page
- Template File: `templates/ticket_booking.html`
- Page Title: "Book Your Tickets"
- Element IDs:
  - `ticket-booking-page` (Div)
  - `select-event-dropdown` (Dropdown): select event
  - `ticket-quantity-input` (Input number)
  - `ticket-type-select` (Dropdown): ticket types (General, VIP, Early Bird)
  - `book-now-button` (Button)
  - `booking-confirmation` (Div)
- Context Variables:
  - GET: `events` List[Dict] with `event_id`, `event_name`
  - POST: `confirmation` Dict with booking info
- Navigation:
  - show confirmation on POST submission inside `booking-confirmation`

### 5. Participants Management Page
- Template File: `templates/participants.html`
- Page Title: "Participants Management"
- Element IDs:
  - `participants-page` (Div)
  - `participants-table` (Table)
  - `add-participant-button` (Button)
  - `search-participant-input` (Input)
  - `participant-status-filter` (Dropdown)
- Context Variables:
  - `participants`: List[Dict] with participant data
- Navigation:
  - `add-participant-button` triggers adding participants

### 6. Venue Information Page
- Template File: `templates/venues.html`
- Page Title: "Venues"
- Element IDs:
  - `venues-page` (Div)
  - `venues-grid` (Div)
  - `venue-search-input` (Input)
  - `venue-capacity-filter` (Dropdown)
  - dynamic `view-venue-details-{{ venue.venue_id }}` (Button) for each venue
- Context Variables:
  - `venues`: List[Dict] with venue data
- Rendering:
  - Use Jinja2 loop `{% for venue in venues %}` to render venue cards with dynamic button IDs

### 7. Event Schedules Page
- Template File: `templates/schedules.html`
- Page Title: "Event Schedules"
- Element IDs:
  - `schedules-page` (Div)
  - `schedules-timeline` (Div)
  - `schedule-filter-date` (Input date)
  - `schedule-filter-event` (Dropdown)
  - `export-schedule-button` (Button)
- Context Variables:
  - `schedules`: List[Dict] with schedule data
  - `events`: List[Dict] for filtering

### 8. Bookings Summary Page
- Template File: `templates/bookings.html`
- Page Title: "My Bookings"
- Element IDs:
  - `bookings-page` (Div)
  - `bookings-table` (Table)
  - `booking-search-input` (Input)
  - dynamic `cancel-booking-button-{{ booking.booking_id }}` (Button) for each booking
  - `back-to-dashboard` (Button)
- Context Variables:
  - `bookings`: List[Dict] with booking data
- Navigation:
  - `back-to-dashboard` uses `url_for('dashboard')`
  - Cancel booking button submits POST to `/booking/cancel/<booking_id>`

---

## Section 3: Data File Schemas

### 1. Events Data
- File Path: `data/events.txt`
- Fields (pipe-delimited):
  ```
  event_id|event_name|category|date|time|location|description|venue_id|capacity
  ```
- Description: Stores event details with scheduling and venue link.
- Example Rows:
  ```
  1|Tech Conference 2025|Conference|2025-03-15|09:00|Convention Center, San Francisco|Annual technology conference discussing latest innovations|1|500
  2|Summer Music Festival|Concert|2025-06-20|18:00|Central Park, New York|Three-day music festival with international artists|2|5000
  3|Marathon Championship|Sports|2025-04-10|07:00|Downtown Loop, Chicago|Annual city marathon event for all skill levels|3|1000
  ```

### 2. Venues Data
- File Path: `data/venues.txt`
- Fields:
  ```
  venue_id|venue_name|location|capacity|amenities|contact
  ```
- Description: Stores venue info including amenities and contact.
- Example Rows:
  ```
  1|Convention Center|San Francisco, CA|500|WiFi, Parking, Catering|contact@convention.com
  2|Central Park|New York, NY|5000|Outdoor Space, Restrooms, Food Vendors|info@centralparkevents.org
  3|Downtown Loop|Chicago, IL|1000|Paved Surface, Water Stations, Medical Support|events@downtown.com
  ```

### 3. Tickets Data
- File Path: `data/tickets.txt`
- Fields:
  ```
  ticket_id|event_id|ticket_type|price|available_count|sold_count
  ```
- Description: Stores ticket types, pricing, availability.
- Example Rows:
  ```
  1|1|General|49.99|500|150
  2|1|VIP|99.99|100|45
  3|2|Early Bird|39.99|1000|750
  ```

### 4. Bookings Data
- File Path: `data/bookings.txt`
- Fields:
  ```
  booking_id|event_id|customer_name|booking_date|ticket_count|ticket_type|total_amount|status
  ```
- Description: Booking records with customer and status info.
- Example Rows:
  ```
  1|1|Alice Johnson|2025-02-01|2|General|99.98|Confirmed
  2|2|Bob Williams|2025-02-05|4|Early Bird|159.96|Confirmed
  3|1|Carol Davis|2025-02-10|1|VIP|99.99|Pending
  ```

### 5. Participants Data
- File Path: `data/participants.txt`
- Fields:
  ```
  participant_id|event_id|name|email|booking_id|status|registration_date
  ```
- Description: Stores participant info with status and linked booking.
- Example Rows:
  ```
  1|1|Alice Johnson|alice@email.com|1|Confirmed|2025-02-01
  2|1|Michael Johnson|michael@email.com|1|Confirmed|2025-02-01
  3|2|Bob Williams|bob@email.com|2|Attended|2025-02-05
  ```

### 6. Schedules Data
- File Path: `data/schedules.txt`
- Fields:
  ```
  schedule_id|event_id|session_title|session_time|duration_minutes|speaker|venue_id
  ```
- Description: Schedule sessions with timing, speaker, venue link.
- Example Rows:
  ```
  1|1|Opening Keynote|2025-03-15 09:00|60|John Smith|1
  2|1|Panel Discussion|2025-03-15 10:30|90|Expert Panel|1
  3|2|Headliner Performance|2025-06-20 20:00|120|International Artist|2
  ```

---

This design specification fully satisfies requirements for backend routes, frontend templates, and data files to enable independent development of the 'EventPlanning' application.