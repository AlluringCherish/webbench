# EventPlanning Web Application Design Specification

## Section 1: Flask Routes Specification

### Root Route
- Route Path: `/`
- Function Name: `root_redirect`
- HTTP Methods: GET
- Template: None (redirect)
- Functionality: Redirects to `/dashboard`.

---

### Dashboard Page
- Route Path: `/dashboard`
- Function Name: `dashboard`
- HTTP Methods: GET
- Template: `templates/dashboard.html`
- Context Variables:
  - `featured_events`: List[Dict] — each dict with fields:
    - `event_id` (int)
    - `event_name` (str)
    - `category` (str)
    - `date` (str, YYYY-MM-DD)
    - `location` (str)
- Navigation Buttons:
  - `browse-events-button` links to `url_for('events')`
  - `view-tickets-button` links to `url_for('tickets')`
  - `venues-button` links to `url_for('venues')`
- Page Element IDs:
  - `dashboard-page` (div container)
  - `featured-events` (div for event recommendations)
  - `browse-events-button` (button)
  - `view-tickets-button` (button)
  - `venues-button` (button)

---

### Events Listing Page
- Route Path: `/events`
- Function Name: `events`
- HTTP Methods: GET
- Template: `templates/events.html`
- Context Variables:
  - `events`: List[Dict] — each dict with keys:
    - `event_id` (int)
    - `event_name` (str)
    - `category` (str)
    - `date` (str)
    - `time` (str)
    - `location` (str)
  - `search_query`: str — current value of `event-search-input`
  - `selected_category`: str from categories (Conference, Concert, Sports, Workshop, Social)
- Page Element IDs:
  - `events-page` (div container)
  - `event-search-input` (input for search)
  - `event-category-filter` (dropdown filter)
  - `events-grid` (div listing event cards)
  - `view-event-button-{event_id}` (button on each event card, dynamic)

- Navigation Buttons:
  - Each `view-event-button-{event_id}` navigates to route `event_details(event_id=event_id)`

Example Jinja2 dynamic ID rendering:
```jinja2
{% for event in events %}
  <button id="view-event-button-{{ event.event_id }}" onclick="location.href='{{ url_for('event_details', event_id=event.event_id) }}'">View Details</button>
{% endfor %}
```

---

### Event Details Page
- Route Path: `/event/<int:event_id>`
- Function Name: `event_details`
- HTTP Methods: GET
- Template: `templates/event_details.html`
- Context Variables:
  - `event`: Dict with keys:
    - `event_id` (int)
    - `event_name` (str)
    - `category` (str)
    - `date` (str)
    - `time` (str)
    - `location` (str)
    - `description` (str)
    - `venue_id` (int)
    - `capacity` (int)
- Page Element IDs:
  - `event-details-page` (div container)
  - `event-title` (h1)
  - `event-date` (div for date/time)
  - `event-location` (div for location)
  - `event-description` (div for description)
  - `book-ticket-button` (button to book)

- Navigation Button:
  - `book-ticket-button` navigates to `/book_ticket` with event query parameter.

---

### Ticket Booking Page
- Route Path: `/book_ticket`
- Function Name: `ticket_booking`
- HTTP Methods: GET, POST
- Template: `templates/ticket_booking.html`
- Context Variables (GET):
  - `events`: List[Dict] with `event_id`, `event_name`
  - `ticket_types`: List[str] – e.g., ["General", "VIP", "Early Bird"]
- Page Element IDs:
  - `ticket-booking-page` (div container)
  - `select-event-dropdown` (dropdown to select event)
  - `ticket-quantity-input` (number input)
  - `ticket-type-select` (dropdown for ticket type)
  - `book-now-button` (button to submit booking)
  - `booking-confirmation` (div for confirmation messages)

---

### Participants Management Page
- Route Path: `/participants`
- Function Name: `participants_management`
- HTTP Methods: GET, POST
- Template: `templates/participants.html`
- Context Variables:
  - `participants`: List[Dict] with keys:
    - `participant_id` (int)
    - `event_id` (int)
    - `name` (str)
    - `email` (str)
    - `booking_id` (int)
    - `status` (str: Registered, Confirmed, Attended)
    - `registration_date` (str)
  - `search_query`: str — current value of `search-participant-input`
  - `selected_status`: str from filter options
- Page Element IDs:
  - `participants-page` (div container)
  - `participants-table` (table listing participants)
  - `add-participant-button` (button to add participant)
  - `search-participant-input` (input for searching)
  - `participant-status-filter` (dropdown for filtering by status)

---

### Venue Information Page
- Route Path: `/venues`
- Function Name: `venues`
- HTTP Methods: GET
- Template: `templates/venues.html`
- Context Variables:
  - `venues`: List[Dict] with keys:
    - `venue_id` (int)
    - `venue_name` (str)
    - `location` (str)
    - `capacity` (int)
    - `amenities` (str, comma-separated)
    - `contact` (str)
  - `search_query`: str — current value of `venue-search-input`
  - `selected_capacity_filter`: str from options (Small, Medium, Large)
- Page Element IDs:
  - `venues-page` (div container)
  - `venues-grid` (div grid with venue cards)
  - `venue-search-input` (input for search)
  - `venue-capacity-filter` (dropdown for capacity filter)
  - `view-venue-details-{venue_id}` (button on each venue card, dynamic)

- Example of dynamic ID rendering in Jinja2:
```jinja2
{% for venue in venues %}
  <button id="view-venue-details-{{ venue.venue_id }}" onclick="location.href='{{ url_for('venue_details', venue_id=venue.venue_id) }}'">View Details</button>
{% endfor %}
```

---

### Event Schedules Page
- Route Path: `/schedules`
- Function Name: `event_schedules`
- HTTP Methods: GET
- Template: `templates/schedules.html`
- Context Variables:
  - `schedules`: List[Dict] with keys:
    - `schedule_id` (int)
    - `event_id` (int)
    - `session_title` (str)
    - `session_time` (str, datetime format)
    - `duration_minutes` (int)
    - `speaker` (str)
    - `venue_id` (int)
  - `filter_date`: str (optional)
  - `filter_event_id`: int (optional)
- Page Element IDs:
  - `schedules-page` (div container)
  - `schedules-timeline` (div timeline view)
  - `schedule-filter-date` (date input)
  - `schedule-filter-event` (dropdown)
  - `export-schedule-button` (button to export data)

---

### Bookings Summary Page
- Route Path: `/bookings`
- Function Name: `bookings_summary`
- HTTP Methods: GET
- Template: `templates/bookings.html`
- Context Variables:
  - `bookings`: List[Dict] with keys:
    - `booking_id` (int)
    - `event_name` (str)
    - `date` (str)
    - `ticket_count` (int)
    - `ticket_type` (str)
    - `status` (str)
- Page Element IDs:
  - `bookings-page` (div container)
  - `bookings-table` (table for bookings)
  - `booking-search-input` (input for searching bookings)
  - `cancel-booking-button-{booking_id}` (button per booking to cancel, dynamic)
  - `back-to-dashboard` (button to navigate to `/dashboard`)

Example dynamic ID with Jinja2:
```jinja2
{% for booking in bookings %}
  <button id="cancel-booking-button-{{ booking.booking_id }}">Cancel Booking</button>
{% endfor %}
```

---

## Section 2: HTML Template Specifications

Each HTML template is located under `templates/` directory.

### 2.1 Dashboard Page
- Template Path: `templates/dashboard.html`
- Page Title: "Event Planning Dashboard"
- Top-level container div ID: `dashboard-page`
- Elements:
  - Div `featured-events`: displays list of featured events
  - Buttons:
    - `browse-events-button`: navigate to events page (`url_for('events')`)
    - `view-tickets-button`: navigate to tickets page (`url_for('tickets')`)
    - `venues-button`: navigate to venues page (`url_for('venues')`)

### 2.2 Events Listing Page
- Template Path: `templates/events.html`
- Page Title: "Events Catalog"
- Elements:
  - Div `events-page`
  - Input `event-search-input` for search
  - Dropdown `event-category-filter` for category
  - Div `events-grid`, displays event cards
  - Buttons `view-event-button-{event_id}`, dynamic per event

**Jinja2 Example for dynamic buttons:**
```jinja2
{% for event in events %}
  <button id="view-event-button-{{ event.event_id }}" onclick="location.href='{{ url_for('event_details', event_id=event.event_id) }}'">{{ event.event_name }}</button>
{% endfor %}
```

### 2.3 Event Details Page
- Template Path: `templates/event_details.html`
- Page Title: "Event Details"
- Elements:
  - Div `event-details-page`
  - H1 `event-title`
  - Divs: `event-date`, `event-location`, `event-description`
  - Button `book-ticket-button` links to ticket booking page for the event

### 2.4 Ticket Booking Page
- Template Path: `templates/ticket_booking.html`
- Page Title: "Book Your Tickets"
- Elements:
  - Div `ticket-booking-page`
  - Dropdowns: `select-event-dropdown` (events), `ticket-type-select` (ticket types)
  - Input Number: `ticket-quantity-input`
  - Button `book-now-button` (submits booking)
  - Div `booking-confirmation` (confirmation details)

### 2.5 Participants Management Page
- Template Path: `templates/participants.html`
- Page Title: "Participants Management"
- Elements:
  - Div `participants-page`
  - Table `participants-table` listing participants
  - Button `add-participant-button`
  - Input `search-participant-input`
  - Dropdown `participant-status-filter`

### 2.6 Venue Information Page
- Template Path: `templates/venues.html`
- Page Title: "Venues"
- Elements:
  - Div `venues-page`
  - Div `venues-grid` for venue cards
  - Input `venue-search-input`
  - Dropdown `venue-capacity-filter`
  - Buttons `view-venue-details-{venue_id}`, dynamic

**Jinja2 Buttons Example:**
```jinja2
{% for venue in venues %}
  <button id="view-venue-details-{{ venue.venue_id }}" onclick="location.href='{{ url_for('venue_details', venue_id=venue.venue_id) }}'">View Details</button>
{% endfor %}
```

### 2.7 Event Schedules Page
- Template Path: `templates/schedules.html`
- Page Title: "Event Schedules"
- Elements:
  - Div `schedules-page`
  - Div `schedules-timeline`
  - Input date `schedule-filter-date`
  - Dropdown `schedule-filter-event`
  - Button `export-schedule-button`

### 2.8 Bookings Summary Page
- Template Path: `templates/bookings.html`
- Page Title: "My Bookings"
- Elements:
  - Div `bookings-page`
  - Table `bookings-table`
  - Input `booking-search-input`
  - Buttons `cancel-booking-button-{booking_id}`, dynamic
  - Button `back-to-dashboard`

**Dynamic Cancel Button Jinja2 Example:**
```jinja2
{% for booking in bookings %}
  <button id="cancel-booking-button-{{ booking.booking_id }}" onclick="cancelBooking('{{ booking.booking_id }}')">Cancel Booking</button>
{% endfor %}
```


## Section 3: Data File Schemas

### 3.1 `data/events.txt`
- Fields (pipe-separated):
  - `event_id` (int)
  - `event_name` (str)
  - `category` (str)
  - `date` (str, YYYY-MM-DD)
  - `time` (str, HH:MM)
  - `location` (str)
  - `description` (str)
  - `venue_id` (int)
  - `capacity` (int)
- Description: Stores event details.

**Examples:**
```
1|Tech Conference 2025|Conference|2025-03-15|09:00|Convention Center, San Francisco|Annual technology conference discussing latest innovations|1|500
2|Summer Music Festival|Concert|2025-06-20|18:00|Central Park, New York|Three-day music festival with international artists|2|5000
3|Marathon Championship|Sports|2025-04-10|07:00|Downtown Loop, Chicago|Annual city marathon event for all skill levels|3|1000
```

---

### 3.2 `data/venues.txt`
- Fields:
  - `venue_id` (int)
  - `venue_name` (str)
  - `location` (str)
  - `capacity` (int)
  - `amenities` (str, comma-separated)
  - `contact` (str)
- Description: Stores venue information.

**Examples:**
```
1|Convention Center|San Francisco, CA|500|WiFi, Parking, Catering|contact@convention.com
2|Central Park|New York, NY|5000|Outdoor Space, Restrooms, Food Vendors|info@centralparkevents.org
3|Downtown Loop|Chicago, IL|1000|Paved Surface, Water Stations, Medical Support|events@downtown.com
```

---

### 3.3 `data/tickets.txt`
- Fields:
  - `ticket_id` (int)
  - `event_id` (int)
  - `ticket_type` (str)
  - `price` (float)
  - `available_count` (int)
  - `sold_count` (int)
- Description: Stores available ticket types and stock per event.

**Examples:**
```
1|1|General|49.99|500|150
2|1|VIP|99.99|100|45
3|2|Early Bird|39.99|1000|750
```

---

### 3.4 `data/bookings.txt`
- Fields:
  - `booking_id` (int)
  - `event_id` (int)
  - `customer_name` (str)
  - `booking_date` (str, YYYY-MM-DD)
  - `ticket_count` (int)
  - `ticket_type` (str)
  - `total_amount` (float)
  - `status` (str)
- Description: Stores user bookings.

**Examples:**
```
1|1|Alice Johnson|2025-02-01|2|General|99.98|Confirmed
2|2|Bob Williams|2025-02-05|4|Early Bird|159.96|Confirmed
3|1|Carol Davis|2025-02-10|1|VIP|99.99|Pending
```

---

### 3.5 `data/participants.txt`
- Fields:
  - `participant_id` (int)
  - `event_id` (int)
  - `name` (str)
  - `email` (str)
  - `booking_id` (int)
  - `status` (str)
  - `registration_date` (str)
- Description: Stores participant data.

**Examples:**
```
1|1|Alice Johnson|alice@email.com|1|Confirmed|2025-02-01
2|1|Michael Johnson|michael@email.com|1|Confirmed|2025-02-01
3|2|Bob Williams|bob@email.com|2|Attended|2025-02-05
```

---

### 3.6 `data/schedules.txt`
- Fields:
  - `schedule_id` (int)
  - `event_id` (int)
  - `session_title` (str)
  - `session_time` (str, datetime YYYY-MM-DD HH:MM)
  - `duration_minutes` (int)
  - `speaker` (str)
  - `venue_id` (int)
- Description: Stores event schedule sessions.

**Examples:**
```
1|1|Opening Keynote|2025-03-15 09:00|60|John Smith|1
2|1|Panel Discussion|2025-03-15 10:30|90|Expert Panel|1
3|2|Headliner Performance|2025-06-20 20:00|120|International Artist|2
```

---

## End of Design Specification
