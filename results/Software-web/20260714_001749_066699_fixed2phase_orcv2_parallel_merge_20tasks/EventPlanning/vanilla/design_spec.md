# EventPlanning Application Design Specification

---

## Section 1: Flask Backend Design

### Routes Specification

1. **Dashboard Page**
   - Route URL: `/`
   - HTTP Method: GET
   - Route Function: `dashboard()`
   - Template: `dashboard.html`
   - Template Context Variables:
     - `featured_events`: List of featured event dicts (event_id, event_name, date, location, description)
     - `featured_venues`: List of featured venue dicts (venue_id, venue_name, location, capacity, amenities)
   - Data Access: Read from `data/events.txt` and `data/venues.txt`.

2. **Events Listing Page**
   - Route URL: `/events`
   - HTTP Method: GET
   - Route Function: `events_listing()`
   - Template: `events.html`
   - Template Context Variables:
     - `events`: List of all event dicts (event_id, event_name, category, date, time, location, description, venue_id, capacity)
     - `categories`: ["Conference", "Concert", "Sports", "Workshop", "Social"]
     - Optional Query Params: `search`, `category` for filtering
   - Data Access: Read from `data/events.txt`.

3. **Event Details Page**
   - Route URL: `/events/<int:event_id>`
   - HTTP Method: GET
   - Route Function: `event_details(event_id)`
   - Template: `event_details.html`
   - Template Context Variables:
     - `event`: event dict matching `event_id` with all event fields
     - `venue`: venue dict linked by `venue_id`
   - Data Access: Read from `data/events.txt` and `data/venues.txt`.

4. **Ticket Booking Page**
   - Route URL: `/bookings/new`
   - HTTP Methods: GET, POST
   - Route Functions:
     - GET: `ticket_booking_form()` - returns booking form
     - POST: `process_booking()` - processes booking submission
   - Template: `ticket_booking.html`
   - Template Context Variables (GET):
     - `events`: list of all events (event_id, event_name)
     - `ticket_types`: ["General", "VIP", "Early Bird"]
   - Data Access:
     - Read `data/events.txt` for event list
     - Read `data/tickets.txt` for ticket availability
   - POST Processing:
     - Validate ticket availability from `tickets.txt`
     - Write new booking entry to `data/bookings.txt` (assign next available booking_id)
     - Update `tickets.txt` sold_count accordingly

5. **Participants Management Page**
   - Route URL: `/participants`
   - HTTP Method: GET
   - Route Function: `participants_management()`
   - Template: `participants.html`
   - Template Context Variables:
     - `participants`: list of participant dicts (participant_id, event_id, name, email, booking_id, status, registration_date)
     - `status_options`: ["Registered", "Confirmed", "Attended"]
     - Optional Query Params: `search`, `status` for filtering
   - Data Access: Read from `data/participants.txt`.

6. **Venue Information Page**
   - Route URL: `/venues`
   - HTTP Method: GET
   - Route Function: `venues_listing()`
   - Template: `venues.html`
   - Template Context Variables:
     - `venues`: list of venue dicts (venue_id, venue_name, location, capacity, amenities, contact)
     - `capacity_filters`: ["Small", "Medium", "Large"]
     - Optional Query Params: `search`, `capacity` for filtering
   - Data Access: Read from `data/venues.txt`.

7. **Event Schedules Page**
   - Route URL: `/schedules`
   - HTTP Method: GET
   - Route Function: `schedules_page()`
   - Template: `schedules.html`
   - Template Context Variables:
     - `schedules`: list of schedule dicts (schedule_id, event_id, session_title, session_time, duration_minutes, speaker, venue_id)
     - `events`: list of event dicts (event_id, event_name) for filtering
     - Optional Query Params: `date`, `event_id` for filtering
   - Data Access: Read from `data/schedules.txt` and `data/events.txt`.

8. **Bookings Summary Page**
   - Route URL: `/bookings`
   - HTTP Method: GET
   - Route Function: `bookings_summary()`
   - Template: `bookings.html`
   - Template Context Variables:
     - `bookings`: list of booking records (booking_id, event_id, customer_name, booking_date, ticket_count, ticket_type, total_amount, status)
     - `search_query`: optional string for filtering bookings by event name or booking id
   - Data Access: Read from `data/bookings.txt` and `data/events.txt`.
   - Optional POST route for canceling booking at `/bookings/cancel/<int:booking_id>` (not detailed but possible).

---

## Section 2: Frontend Template Design

### Templates, Titles, and Key Elements

1. **Dashboard Page**
   - Template File: `dashboard.html`
   - Page Title: "Event Planning Dashboard"
   - Elements:
     - div#dashboard-page
     - div#featured-events
     - button#browse-events-button (navigates to `/events`)
     - button#view-tickets-button (navigates to `/bookings`)
     - button#venues-button (navigates to `/venues`)

2. **Events Listing Page**
   - Template File: `events.html`
   - Page Title: "Events Catalog"
   - Elements:
     - div#events-page
     - input#event-search-input (text input for search)
     - select#event-category-filter (options: Conference, Concert, Sports, Workshop, Social)
     - div#events-grid (grid of event cards)
     - button#view-event-button-{event_id} (per event; navigates to `/events/<event_id>`)

3. **Event Details Page**
   - Template File: `event_details.html`
   - Page Title: "Event Details"
   - Elements:
     - div#event-details-page
     - h1#event-title
     - div#event-date
     - div#event-location
     - div#event-description
     - button#book-ticket-button (navigates to `/bookings/new` with preselected event)

4. **Ticket Booking Page**
   - Template File: `ticket_booking.html`
   - Page Title: "Book Your Tickets"
   - Elements:
     - div#ticket-booking-page
     - select#select-event-dropdown (dynamic event list)
     - input#ticket-quantity-input (number input, min=1)
     - select#ticket-type-select (options: General, VIP, Early Bird)
     - button#book-now-button (triggers POST to `/bookings/new`)
     - div#booking-confirmation (shows booking confirmation)

5. **Participants Management Page**
   - Template File: `participants.html`
   - Page Title: "Participants Management"
   - Elements:
     - div#participants-page
     - table#participants-table (columns: Name, Email, Event, Status)
     - button#add-participant-button (opens add participant form/modal)
     - input#search-participant-input (search by name/email)
     - select#participant-status-filter (options: Registered, Confirmed, Attended)

6. **Venue Information Page**
   - Template File: `venues.html`
   - Page Title: "Venues"
   - Elements:
     - div#venues-page
     - input#venue-search-input (search venues by name/location)
     - select#venue-capacity-filter (options: Small, Medium, Large)
     - div#venues-grid (grid of venue cards)
     - button#view-venue-details-{venue_id} (shows venue details)

7. **Event Schedules Page**
   - Template File: `schedules.html`
   - Page Title: "Event Schedules"
   - Elements:
     - div#schedules-page
     - input#schedule-filter-date (date input)
     - select#schedule-filter-event (dynamic event list)
     - div#schedules-timeline
     - button#export-schedule-button (exports schedule data)

8. **Bookings Summary Page**
   - Template File: `bookings.html`
   - Page Title: "My Bookings"
   - Elements:
     - div#bookings-page
     - input#booking-search-input (search by event name or booking ID)
     - table#bookings-table (columns: Event, Date, Ticket Count, Status)
     - button#cancel-booking-button-{booking_id} (cancel booking button)
     - button#back-to-dashboard (navigates to `/`)

### Navigation and Interaction

- From Dashboard:
  - `#browse-events-button` → `/events`
  - `#view-tickets-button` → `/bookings`
  - `#venues-button` → `/venues`

- From Events Listing:
  - `#view-event-button-{event_id}` → `/events/<event_id>`

- From Event Details:
  - `#book-ticket-button` → `/bookings/new` with preselected event

- From Ticket Booking:
  - `#book-now-button` submits booking; confirmation shown in `#booking-confirmation`

- Participants Management:
  - `#add-participant-button` opens participant add form/modal

- Venue Information:
  - `#view-venue-details-{venue_id}` shows detailed venue info modal/page

- Event Schedules:
  - `#export-schedule-button` triggers export/download

- Bookings Summary:
  - `#cancel-booking-button-{booking_id}` cancels booking
  - `#back-to-dashboard` navigates to `/`

### Form Controls and Inputs

- `event-search-input`: Search/filter events by name, location, date
- `event-category-filter`: Filter events by category
- `select-event-dropdown`: Select event in ticket booking
- `ticket-quantity-input`: Number input for ticket count (min=1)
- `ticket-type-select`: Select ticket type
- `search-participant-input`: Search participants by name/email
- `participant-status-filter`: Filter participant status
- `venue-search-input`: Search venues by name/location
- `venue-capacity-filter`: Filter venues by capacity
- `schedule-filter-date`: Filter schedules by date
- `schedule-filter-event`: Filter schedules by event
- `booking-search-input`: Search bookings by event name or booking ID

### Page Container Div IDs
- #dashboard-page
- #events-page
- #event-details-page
- #ticket-booking-page
- #participants-page
- #venues-page
- #schedules-page
- #bookings-page

---

## Section 3: Data File Schema Alignment

### 1. Events Data (`events.txt`)
- Schema:
  ```
  event_id|event_name|category|date|time|location|description|venue_id|capacity
  ```
- Fields:
  - `event_id`: int
  - `event_name`: string
  - `category`: string (Conference, Concert, Sports, Workshop, Social)
  - `date`: YYYY-MM-DD
  - `time`: HH:MM
  - `location`: string
  - `description`: string
  - `venue_id`: int
  - `capacity`: int
- Example:
  ```
  1|Tech Conference 2025|Conference|2025-03-15|09:00|Convention Center, San Francisco|Annual technology conference discussing latest innovations|1|500
  2|Summer Music Festival|Concert|2025-06-20|18:00|Central Park, New York|Three-day music festival with international artists|2|5000
  3|Marathon Championship|Sports|2025-04-10|07:00|Downtown Loop, Chicago|Annual city marathon event for all skill levels|3|1000
  ```

### 2. Venues Data (`venues.txt`)
- Schema:
  ```
  venue_id|venue_name|location|capacity|amenities|contact
  ```
- Fields:
  - `venue_id`: int
  - `venue_name`: string
  - `location`: string
  - `capacity`: int
  - `amenities`: comma-separated string
  - `contact`: string
- Example:
  ```
  1|Convention Center|San Francisco, CA|500|WiFi, Parking, Catering|contact@convention.com
  2|Central Park|New York, NY|5000|Outdoor Space, Restrooms, Food Vendors|info@centralparkevents.org
  3|Downtown Loop|Chicago, IL|1000|Paved Surface, Water Stations, Medical Support|events@downtown.com
  ```

### 3. Tickets Data (`tickets.txt`)
- Schema:
  ```
  ticket_id|event_id|ticket_type|price|available_count|sold_count
  ```
- Fields:
  - `ticket_id`: int
  - `event_id`: int
  - `ticket_type`: string (General, VIP, Early Bird)
  - `price`: float
  - `available_count`: int
  - `sold_count`: int
- Example:
  ```
  1|1|General|49.99|500|150
  2|1|VIP|99.99|100|45
  3|2|Early Bird|39.99|1000|750
  ```

### 4. Bookings Data (`bookings.txt`)
- Schema:
  ```
  booking_id|event_id|customer_name|booking_date|ticket_count|ticket_type|total_amount|status
  ```
- Fields:
  - `booking_id`: int
  - `event_id`: int
  - `customer_name`: string
  - `booking_date`: YYYY-MM-DD
  - `ticket_count`: int
  - `ticket_type`: string
  - `total_amount`: float
  - `status`: string (Confirmed, Pending, Cancelled)
- Example:
  ```
  1|1|Alice Johnson|2025-02-01|2|General|99.98|Confirmed
  2|2|Bob Williams|2025-02-05|4|Early Bird|159.96|Confirmed
  3|1|Carol Davis|2025-02-10|1|VIP|99.99|Pending
  ```

### 5. Participants Data (`participants.txt`)
- Schema:
  ```
  participant_id|event_id|name|email|booking_id|status|registration_date
  ```
- Fields:
  - `participant_id`: int
  - `event_id`: int
  - `name`: string
  - `email`: string
  - `booking_id`: int
  - `status`: string (Registered, Confirmed, Attended)
  - `registration_date`: YYYY-MM-DD
- Example:
  ```
  1|1|Alice Johnson|alice@email.com|1|Confirmed|2025-02-01
  2|1|Michael Johnson|michael@email.com|1|Confirmed|2025-02-01
  3|2|Bob Williams|bob@email.com|2|Attended|2025-02-05
  ```

### 6. Schedules Data (`schedules.txt`)
- Schema:
  ```
  schedule_id|event_id|session_title|session_time|duration_minutes|speaker|venue_id
  ```
- Fields:
  - `schedule_id`: int
  - `event_id`: int
  - `session_title`: string
  - `session_time`: YYYY-MM-DD HH:MM
  - `duration_minutes`: int
  - `speaker`: string
  - `venue_id`: int
- Example:
  ```
  1|1|Opening Keynote|2025-03-15 09:00|60|John Smith|1
  2|1|Panel Discussion|2025-03-15 10:30|90|Expert Panel|1
  3|2|Headliner Performance|2025-06-20 20:00|120|International Artist|2
  ```

---

# End of Design Specification
