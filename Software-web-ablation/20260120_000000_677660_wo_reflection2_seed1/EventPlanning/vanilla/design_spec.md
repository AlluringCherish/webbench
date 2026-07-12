# EventPlanning Web Application Design Specification

---

## Section 1: Flask Routes Specification

| Route Path                | Function Name          | HTTP Methods | Template File          | Context Variables                                                                                                                                                                    |
|---------------------------|------------------------|--------------|------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `/`                       | `root_redirect`         | GET          | None (redirect)         | None                                                                                                                                                                                |
| `/dashboard`              | `dashboard`             | GET          | `dashboard.html`        | `featured_events` (List[Dict]): List of event dicts with keys: `event_id` (int), `event_name` (str), `date` (str, YYYY-MM-DD), and `location` (str).
|
| `/events`                 | `events_listing`        | GET          | `events.html`           | `events` (List[Dict]): Each dict has `event_id` (int), `event_name` (str), `category` (str), `date` (str), `time` (str), `location` (str).
`categories` (List[str]): Fixed categories list for filter.
|
| `/event/<int:event_id>`   | `event_details`         | GET          | `event_details.html`    | `event` (Dict): Includes `event_id` (int), `event_name` (str), `date` (str), `time` (str), `location` (str), `description` (str).
|
| `/book_ticket`            | `ticket_booking`        | GET, POST    | `ticket_booking.html`   | On GET: `events` (List[Dict]): Each dict with `event_id`, `event_name`.
On POST: `confirmation` (Dict) on success with confirmation details or `error` (str).
|
| `/participants`           | `participants_management`| GET, POST   | `participants.html`     | On GET: `participants` (List[Dict]): Each dict with `participant_id`, `name`, `email`, `event_name` (str), `status` (str).
`statuses` (List[str]): List of statuses.
On POST: post results (usually redirect or confirmation).
|
| `/venues`                 | `venues`                | GET          | `venues.html`           | `venues` (List[Dict]): Each dict with `venue_id` (int), `venue_name` (str), `location` (str), `capacity` (int), `amenities` (str).
`capacity_filters` (List[str]): Fixed list ["Small", "Medium", "Large"].
|
| `/venue/<int:venue_id>`   | `venue_details`         | GET          | `venue_details.html` (if applicable, else could be integrated) | `venue` (Dict): venue details including `venue_name`, `location`, `capacity`, `amenities`, `contact`.
|
| `/schedules`              | `event_schedules`       | GET          | `schedules.html`        | `schedules` (List[Dict]): Each dict with `schedule_id`, `event_name` (str), `session_title` (str), `session_time` (str), `duration_minutes` (int), `speaker` (str).
`events` (List[Dict]): List of events for filter.
|
| `/bookings`               | `bookings_summary`      | GET          | `bookings.html`         | `bookings` (List[Dict]): Each dict has `booking_id`, `event_name` (str), `date` (str), `ticket_count` (int), `status` (str).
|
| `/book_ticket/submit`     | `submit_ticket_booking` | POST         | None (redirect or JSON response) | Receives booking details from form POST, processes booking.
|
| `/participants/add`       | `add_participant`       | POST         | None (redirect or JSON response) | Receives participant info to add.
|
| `/booking/cancel/<int:booking_id>` | `cancel_booking`  | POST         | None (redirect or JSON response) | Cancels a booking identified by booking_id.

### Detailed Route Descriptions:

- `/`: Redirects to `/dashboard`.
- `/dashboard`: Displays main dashboard with `featured_events` list.
- `/events`: Shows all events, supports search/filter on client side; passes `events` list and fixed categories.
- `/event/<event_id>`: Shows detailed info about event.
- `/book_ticket`: On GET, displays ticket booking form listing all events; POST processes ticket booking; confirmation or error shown.
- `/participants`: Shows participants management; POST to add new participant.
- `/venues`: Shows venues list.
- `/venue/<venue_id>`: (Optional) shows detailed venue info if required.
- `/schedules`: Shows event schedules and filters.
- `/bookings`: Shows user's bookings.
- Additional POST routes for booking submissions, participant add, and booking cancellations.

---

## Section 2: HTML Template Specifications

### 1. Dashboard Page
- Template file path: `templates/dashboard.html`
- Page title (in `<title>` and `<h1>`): "Event Planning Dashboard"
- Element IDs:
  - `dashboard-page` (Div): Container for dashboard page
  - `featured-events` (Div): Shows featured event recommendations
  - `browse-events-button` (Button): Navigates to `/events`
  - `view-tickets-button` (Button): Navigates to `/bookings`
  - `venues-button` (Button): Navigates to `/venues`
- Context variables:
  - `featured_events`: List[Dict], each dict with: `event_id` (int), `event_name` (str), `date` (str), `location` (str)
- Navigation buttons:
  - `browse-events-button`: route `url_for('events_listing')`
  - `view-tickets-button`: route `url_for('bookings_summary')`
  - `venues-button`: route `url_for('venues')`

### 2. Events Listing Page
- Template file path: `templates/events.html`
- Page title: "Events Catalog"
- Element IDs:
  - `events-page` (Div): Container
  - `event-search-input` (Input): Search field
  - `event-category-filter` (Dropdown): Categories filter
  - `events-grid` (Div): Grid container for event cards
  - `view-event-button-{event_id}` (Button): Per event, button to see details
- Context variables:
  - `events`: List[Dict] with keys: `event_id`, `event_name`, `category`, `date`, `time`, `location`
  - `categories`: List[str], fixed categories ["Conference", "Concert", "Sports", "Workshop", "Social"]
- Navigation:
  - Buttons or links back to dashboard or others if needed
- Dynamic IDs:
  - Render event cards in a Jinja2 loop `{% for event in events %}`
  - Use `id="view-event-button-{{ event.event_id }}"` for each button

### 3. Event Details Page
- Template file path: `templates/event_details.html`
- Page title: "Event Details"
- Element IDs:
  - `event-details-page` (Div)
  - `event-title` (H1)
  - `event-date` (Div)
  - `event-location` (Div)
  - `event-description` (Div)
  - `book-ticket-button` (Button): navigates to `/book_ticket?event_id={{ event.event_id }}`
- Context variables:
  - `event`: Dict with `event_id`, `event_name`, `date`, `time`, `location`, `description`
- Navigation:
  - Typically back to events list or dashboard

### 4. Ticket Booking Page
- Template file path: `templates/ticket_booking.html`
- Page title: "Book Your Tickets"
- Element IDs:
  - `ticket-booking-page` (Div)
  - `select-event-dropdown` (Dropdown): options from `events`
  - `ticket-quantity-input` (Input number)
  - `ticket-type-select` (Dropdown): options ["General", "VIP", "Early Bird"]
  - `book-now-button` (Button)
  - `booking-confirmation` (Div): shows confirmation details post-booking
- Context variables:
  - On GET: `events` (List[Dict]) with `event_id`, `event_name`
  - On POST success: `confirmation` dict with booking details; on error: `error` string
- Navigation:
  - Back to dashboard or events as appropriate

### 5. Participants Management Page
- Template file path: `templates/participants.html`
- Page title: "Participants Management"
- Element IDs:
  - `participants-page` (Div)
  - `participants-table` (Table): shows participant rows
  - `add-participant-button` (Button)
  - `search-participant-input` (Input)
  - `participant-status-filter` (Dropdown): options ["Registered", "Confirmed", "Attended"]
- Context variables:
  - `participants` (List[Dict]): Each with `participant_id`, `name`, `email`, `event_name`, `status`
  - `statuses` (List[str]): ["Registered", "Confirmed", "Attended"]
- Navigation:
  - Links/buttons back to dashboard or other relevant pages

### 6. Venue Information Page
- Template file path: `templates/venues.html`
- Page title: "Venues"
- Element IDs:
  - `venues-page` (Div)
  - `venues-grid` (Div)
  - `venue-search-input` (Input)
  - `venue-capacity-filter` (Dropdown): options ["Small", "Medium", "Large"]
  - `view-venue-details-{venue_id}` (Button): per venue
- Context variables:
  - `venues` (List[Dict]): each with `venue_id`, `venue_name`, `location`, `capacity`, `amenities`
  - `capacity_filters` (List[str]): ["Small", "Medium", "Large"]
- Navigation:
  - Back to dashboard etc.
- Dynamic IDs:
  - Render venue cards with `{% for venue in venues %}` loop
  - `id="view-venue-details-{{ venue.venue_id }}"`

### 7. Event Schedules Page
- Template file path: `templates/schedules.html`
- Page title: "Event Schedules"
- Element IDs:
  - `schedules-page` (Div)
  - `schedules-timeline` (Div)
  - `schedule-filter-date` (Input date)
  - `schedule-filter-event` (Dropdown)
  - `export-schedule-button` (Button)
- Context variables:
  - `schedules` (List[Dict]): each with `schedule_id`, `event_name`, `session_title`, `session_time`, `duration_minutes`, `speaker`
  - `events` (List[Dict]): for event filter dropdown
- Navigation:
  - Back to dashboard or others

### 8. Bookings Summary Page
- Template file path: `templates/bookings.html`
- Page title: "My Bookings"
- Element IDs:
  - `bookings-page` (Div)
  - `bookings-table` (Table): rows with booking info
  - `booking-search-input` (Input)
  - `cancel-booking-button-{booking_id}` (Button) for each booking
  - `back-to-dashboard` (Button)
- Context variables:
  - `bookings` (List[Dict]): each with `booking_id`, `event_name`, `date`, `ticket_count`, `status`
- Navigation:
  - `back-to-dashboard`: route `url_for('dashboard')`
- Dynamic IDs:
  - Use `{% for booking in bookings %}` loop
  - Buttons: `id="cancel-booking-button-{{ booking.booking_id }}"`

---

## Section 3: Data File Schemas

### 1. Events Data
- File: `data/events.txt`
- Fields (pipe-delimited):
  `event_id|event_name|category|date|time|location|description|venue_id|capacity`
- Description: Stores event details including scheduling and venue association.
- Example Rows:
  ```
  1|Tech Conference 2025|Conference|2025-03-15|09:00|Convention Center, San Francisco|Annual technology conference discussing latest innovations|1|500
  2|Summer Music Festival|Concert|2025-06-20|18:00|Central Park, New York|Three-day music festival with international artists|2|5000
  3|Marathon Championship|Sports|2025-04-10|07:00|Downtown Loop, Chicago|Annual city marathon event for all skill levels|3|1000
  ```

### 2. Venues Data
- File: `data/venues.txt`
- Fields (pipe-delimited):
  `venue_id|venue_name|location|capacity|amenities|contact`
- Description: Stores venue details including amenities and contact info.
- Example Rows:
  ```
  1|Convention Center|San Francisco, CA|500|WiFi, Parking, Catering|contact@convention.com
  2|Central Park|New York, NY|5000|Outdoor Space, Restrooms, Food Vendors|info@centralparkevents.org
  3|Downtown Loop|Chicago, IL|1000|Paved Surface, Water Stations, Medical Support|events@downtown.com
  ```

### 3. Tickets Data
- File: `data/tickets.txt`
- Fields (pipe-delimited):
  `ticket_id|event_id|ticket_type|price|available_count|sold_count`
- Description: Stores details about ticket types and availability per event.
- Example Rows:
  ```
  1|1|General|49.99|500|150
  2|1|VIP|99.99|100|45
  3|2|Early Bird|39.99|1000|750
  ```

### 4. Bookings Data
- File: `data/bookings.txt`
- Fields (pipe-delimited):
  `booking_id|event_id|customer_name|booking_date|ticket_count|ticket_type|total_amount|status`
- Description: Records customer bookings with ticket counts and status.
- Example Rows:
  ```
  1|1|Alice Johnson|2025-02-01|2|General|99.98|Confirmed
  2|2|Bob Williams|2025-02-05|4|Early Bird|159.96|Confirmed
  3|1|Carol Davis|2025-02-10|1|VIP|99.99|Pending
  ```

### 5. Participants Data
- File: `data/participants.txt`
- Fields (pipe-delimited):
  `participant_id|event_id|name|email|booking_id|status|registration_date`
- Description: Contains participant info linked to events and bookings.
- Example Rows:
  ```
  1|1|Alice Johnson|alice@email.com|1|Confirmed|2025-02-01
  2|1|Michael Johnson|michael@email.com|1|Confirmed|2025-02-01
  3|2|Bob Williams|bob@email.com|2|Attended|2025-02-05
  ```

### 6. Schedules Data
- File: `data/schedules.txt`
- Fields (pipe-delimited):
  `schedule_id|event_id|session_title|session_time|duration_minutes|speaker|venue_id`
- Description: Stores schedules of sessions within events including timing and speaker.
- Example Rows:
  ```
  1|1|Opening Keynote|2025-03-15 09:00|60|John Smith|1
  2|1|Panel Discussion|2025-03-15 10:30|90|Expert Panel|1
  3|2|Headliner Performance|2025-06-20 20:00|120|International Artist|2
  ```
