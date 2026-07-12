# EventPlanning Web Application Design Specification

---

## Section 1: Flask Routes Specification

| Route Path                | Function Name          | HTTP Methods | Template File          | Context Variables                                                                                                                                                                    |
|---------------------------|------------------------|--------------|------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `/`                       | `root_redirect`         | GET          | N/A (redirect)          | N/A - redirects to `/dashboard`
| `/dashboard`              | `dashboard`             | GET          | `dashboard.html`       | **featured_events**: List[Dict]: Each dict with keys: `event_id` (int), `event_name` (str), `date` (str, YYYY-MM-DD), `location` (str)
| `/events`                 | `events_listing`        | GET          | `events.html`          | **events**: List[Dict]: Each dict with keys: `event_id` (int), `event_name` (str), `category` (str), `date` (str), `location` (str), `image_url` (str, optional)
|                           |                        |              |                        | **categories**: List[str]: List of categories for filter dropdown ("Conference", "Concert", "Sports", "Workshop", "Social")
| `/event/<int:event_id>`   | `event_details`         | GET          | `event_details.html`   | **event**: Dict with keys: `event_id` (int), `event_name` (str), `date` (str), `time` (str), `location` (str), `description` (str), `venue_id` (int), `capacity` (int)
| `/book_ticket`            | `book_ticket_get`       | GET          | `ticket_booking.html`  | **events**: List[Dict] with minimal keys for dropdown: `event_id` (int), `event_name` (str)
| `/book_ticket`            | `book_ticket_post`      | POST         | `ticket_booking.html`  | **booking_confirmation**: Dict with keys: `booking_id` (int), `event_id` (int), `event_name` (str), `ticket_quantity` (int), `ticket_type` (str), `total_price` (float), `status` (str)
| `/participants`           | `participants_management`| GET          | `participants.html`    | **participants**: List[Dict]: Each dict with keys: `participant_id` (int), `name` (str), `email` (str), `event_name` (str), `status` (str)
| `/add_participant`        | `add_participant_post`  | POST         | N/A                    | N/A - after posting, redirect back to participants page
| `/venues`                 | `venues_page`           | GET          | `venues.html`          | **venues**: List[Dict]: Each dict with keys: `venue_id` (int), `venue_name` (str), `location` (str), `capacity` (int), `amenities` (str)
| `/venue/<int:venue_id>`   | `venue_details`         | GET          | `venue_details.html`   | **venue**: Dict with keys: `venue_id` (int), `venue_name` (str), `location` (str), `capacity` (int), `amenities` (str), `contact` (str)
| `/schedules`              | `event_schedules`       | GET          | `schedules.html`       | **schedules**: List[Dict]: Each dict with keys: `schedule_id` (int), `event_id` (int), `session_title` (str), `session_time` (str), `duration_minutes` (int), `speaker` (str), `venue_id` (int)
|                           |                        |              |                        | **events**: List[Dict] Minimal `event_id` and `event_name` for filter dropdown
| `/bookings`               | `bookings_summary`      | GET          | `bookings.html`        | **bookings**: List[Dict]: Each dict with keys: `booking_id` (int), `event_name` (str), `date` (str), `ticket_count` (int), `status` (str)

---

## Section 2: HTML Template Specifications

### 1. Dashboard Page
- Template file path: `templates/dashboard.html`
- Page title (`<title>` and `<h1>`): "Event Planning Dashboard"
- Element IDs:
  - `dashboard-page` (Div) - Container for the dashboard page
  - `featured-events` (Div) - Display of featured event recommendations
  - `browse-events-button` (Button) - Navigate to `/events`
  - `view-tickets-button` (Button) - Navigate to `/bookings`
  - `venues-button` (Button) - Navigate to `/venues`
- Context variables:
  - `featured_events`: List of event dicts with: `event_id` (int), `event_name` (str), `date` (str), `location` (str)
- Navigation buttons use `url_for`:
  - `browse-events-button`: `url_for('events_listing')`
  - `view-tickets-button`: `url_for('bookings_summary')`
  - `venues-button`: `url_for('venues_page')`

### 2. Events Listing Page
- Template file path: `templates/events.html`
- Page title: "Events Catalog"
- Element IDs:
  - `events-page` (Div) - Container
  - `event-search-input` (Input) - Search field
  - `event-category-filter` (Dropdown) - Filter by category
  - `events-grid` (Div) - Grid of event cards
  - `view-event-button-{event_id}` (Button) on each event card - View event details
- Context variables:
  - `events`: List of dicts each with keys: `event_id` (int), `event_name` (str), `category` (str), `date` (str), `location` (str), optional `image_url` (str)
  - `categories`: List[str] (fixed: "Conference", "Concert", "Sports", "Workshop", "Social")
- Navigation buttons:
  - Each `view-event-button-{event_id}` links to `url_for('event_details', event_id=event_id)`
- Dynamic IDs:
  - Use Jinja2 loop:
    ```jinja
    {% for event in events %}
       <button id="view-event-button-{{ event.event_id }}">...</button>
    {% endfor %}
    ```

### 3. Event Details Page
- Template file path: `templates/event_details.html`
- Page title: "Event Details"
- Element IDs:
  - `event-details-page` (Div) - Container
  - `event-title` (H1) - Event title
  - `event-date` (Div) - Event date and time
  - `event-location` (Div) - Event location
  - `event-description` (Div) - Event description
  - `book-ticket-button` (Button) - Book ticket
- Context variables:
  - `event`: Dict with keys: `event_id` (int), `event_name` (str), `date` (str), `time` (str), `location` (str), `description` (str), `venue_id` (int), `capacity` (int)
- Navigation buttons:
  - `book-ticket-button`: `url_for('book_ticket_get')` with event selected (usually via form or query param)

### 4. Ticket Booking Page
- Template file path: `templates/ticket_booking.html`
- Page title: "Book Your Tickets"
- Element IDs:
  - `ticket-booking-page` (Div) - Container
  - `select-event-dropdown` (Dropdown) - Select event
  - `ticket-quantity-input` (Input number) - Number of tickets
  - `ticket-type-select` (Dropdown) - Ticket type (General, VIP, Early Bird)
  - `book-now-button` (Button) - Proceed booking
  - `booking-confirmation` (Div) - Show confirmation details after POST
- Context variables (GET):
  - `events`: List[Dict] with `event_id` (int), `event_name` (str)
- Context variables (POST success):
  - `booking_confirmation`: Dict with booking details
- Navigation buttons: None specified

### 5. Participants Management Page
- Template file path: `templates/participants.html`
- Page title: "Participants Management"
- Element IDs:
  - `participants-page` (Div) - Container
  - `participants-table` (Table) - Shows participants info
  - `add-participant-button` (Button) - Add new participant
  - `search-participant-input` (Input) - Search participants
  - `participant-status-filter` (Dropdown) - Filter by status
- Context variables:
  - `participants`: List[Dict] with keys: `participant_id` (int), `name` (str), `email` (str), `event_name` (str), `status` (str)
- Navigation buttons:
  - `add-participant-button`: POST action to `/add_participant`

### 6. Venue Information Page
- Template file path: `templates/venues.html`
- Page title: "Venues"
- Element IDs:
  - `venues-page` (Div) - Container
  - `venues-grid` (Div) - Grid of venue cards
  - `venue-search-input` (Input) - Search venues
  - `venue-capacity-filter` (Dropdown) - Filter by capacity
  - `view-venue-details-{venue_id}` (Button) each venue card
- Context variables:
  - `venues`: List[Dict] each with keys: `venue_id` (int), `venue_name` (str), `location` (str), `capacity` (int), `amenities` (str)
- Navigation buttons:
  - Each `view-venue-details-{venue_id}` links to `url_for('venue_details', venue_id=venue_id)`
- Dynamic IDs:
  - Jinja2 loop:
    ```jinja
    {% for venue in venues %}
      <button id="view-venue-details-{{ venue.venue_id }}">...</button>
    {% endfor %}
    ```

### 7. Event Schedules Page
- Template file path: `templates/schedules.html`
- Page title: "Event Schedules"
- Element IDs:
  - `schedules-page` (Div) - Container
  - `schedules-timeline` (Div) - Timeline view
  - `schedule-filter-date` (Input date) - Filter by date
  - `schedule-filter-event` (Dropdown) - Filter by event
  - `export-schedule-button` (Button) - Export schedule data
- Context variables:
  - `schedules`: List[Dict] with keys: `schedule_id` (int), `event_id` (int), `session_title` (str), `session_time` (str), `duration_minutes` (int), `speaker` (str), `venue_id` (int)
  - `events`: List[Dict] with `event_id` (int), `event_name` (str) for filter dropdown
- Navigation buttons: None specified

### 8. Bookings Summary Page
- Template file path: `templates/bookings.html`
- Page title: "My Bookings"
- Element IDs:
  - `bookings-page` (Div) - Container
  - `bookings-table` (Table) - Bookings information
  - `booking-search-input` (Input) - Search bookings
  - `cancel-booking-button-{booking_id}` (Button) each booking
  - `back-to-dashboard` (Button) - Navigate back to dashboard
- Context variables:
  - `bookings`: List[Dict] with keys: `booking_id` (int), `event_name` (str), `date` (str), `ticket_count` (int), `status` (str)
- Navigation buttons:
  - `back-to-dashboard`: `url_for('dashboard')`
- Dynamic IDs:
  - Jinja2 loop example:
    ```jinja
    {% for booking in bookings %}
       <button id="cancel-booking-button-{{ booking.booking_id }}">Cancel</button>
    {% endfor %}
    ```

---

## Section 3: Data File Schemas

### 1. Events Data
- File: `data/events.txt`
- Pipe-delimited fields, no header row:
  `event_id|event_name|category|date|time|location|description|venue_id|capacity`
- Description: Stores event information including scheduling and venue linkage.
- Example rows:
```
1|Tech Conference 2025|Conference|2025-03-15|09:00|Convention Center, San Francisco|Annual technology conference discussing latest innovations|1|500
2|Summer Music Festival|Concert|2025-06-20|18:00|Central Park, New York|Three-day music festival with international artists|2|5000
3|Marathon Championship|Sports|2025-04-10|07:00|Downtown Loop, Chicago|Annual city marathon event for all skill levels|3|1000
```

### 2. Venues Data
- File: `data/venues.txt`
- Pipe-delimited fields, no header row:
  `venue_id|venue_name|location|capacity|amenities|contact`
- Description: Venue details including amenities and contact information.
- Example rows:
```
1|Convention Center|San Francisco, CA|500|WiFi, Parking, Catering|contact@convention.com
2|Central Park|New York, NY|5000|Outdoor Space, Restrooms, Food Vendors|info@centralparkevents.org
3|Downtown Loop|Chicago, IL|1000|Paved Surface, Water Stations, Medical Support|events@downtown.com
```

### 3. Tickets Data
- File: `data/tickets.txt`
- Pipe-delimited fields, no header row:
  `ticket_id|event_id|ticket_type|price|available_count|sold_count`
- Description: Ticket types and availability per event.
- Example rows:
```
1|1|General|49.99|500|150
2|1|VIP|99.99|100|45
3|2|Early Bird|39.99|1000|750
```

### 4. Bookings Data
- File: `data/bookings.txt`
- Pipe-delimited fields, no header row:
  `booking_id|event_id|customer_name|booking_date|ticket_count|ticket_type|total_amount|status`
- Description: Customer bookings with ticket counts and status.
- Example rows:
```
1|1|Alice Johnson|2025-02-01|2|General|99.98|Confirmed
2|2|Bob Williams|2025-02-05|4|Early Bird|159.96|Confirmed
3|1|Carol Davis|2025-02-10|1|VIP|99.99|Pending
```

### 5. Participants Data
- File: `data/participants.txt`
- Pipe-delimited fields, no header row:
  `participant_id|event_id|name|email|booking_id|status|registration_date`
- Description: Participants linked to bookings and status.
- Example rows:
```
1|1|Alice Johnson|alice@email.com|1|Confirmed|2025-02-01
2|1|Michael Johnson|michael@email.com|1|Confirmed|2025-02-01
3|2|Bob Williams|bob@email.com|2|Attended|2025-02-05
```

### 6. Schedules Data
- File: `data/schedules.txt`
- Pipe-delimited fields, no header row:
  `schedule_id|event_id|session_title|session_time|duration_minutes|speaker|venue_id`
- Description: Sessions and agenda for events.
- Example rows:
```
1|1|Opening Keynote|2025-03-15 09:00|60|John Smith|1
2|1|Panel Discussion|2025-03-15 10:30|90|Expert Panel|1
3|2|Headliner Performance|2025-06-20 20:00|120|International Artist|2
```
