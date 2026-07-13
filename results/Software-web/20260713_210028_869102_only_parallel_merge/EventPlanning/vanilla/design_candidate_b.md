# design_candidate_b.md

## Flask Routes and Templates for EventPlanning Web Application

---

### 1. Dashboard Page
- **Route:** `/`
- **Methods:** [`GET`]
- **Function Name:** `dashboard()`
- **Template:** `dashboard.html`
- **Context Variables:**
  - `featured_events` (list of dicts): Each dict with keys: `event_id`, `event_name`, `date`, `location`, `description`, `venue_id`
  - `featured_venues` (list of dicts): Each dict with keys: `venue_id`, `venue_name`, `location`, `capacity`, `amenities`

- **Template Structure & Element IDs:**
  - `<div id="dashboard-page">` - main container
  - `<div id="featured-events">` - display featured event recommendations
  - `<button id="browse-events-button">` - Navigates to `/events`
  - `<button id="view-tickets-button">` - Navigates to `/bookings`
  - `<button id="venues-button">` - Navigates to `/venues`

- **Interactions:**
  - Clicking `browse-events-button` redirects to Events Listing Page (`/events`)
  - Clicking `view-tickets-button` redirects to Bookings Summary Page (`/bookings`)
  - Clicking `venues-button` redirects to Venue Information Page (`/venues`)

---

### 2. Events Listing Page
- **Route:** `/events`
- **Methods:** [`GET`]
- **Function Name:** `events_listing()`
- **Template:** `events.html`
- **Context Variables:**
  - `events` (list of dicts): Each dict with keys:
    - `event_id`, `event_name`, `category`, `date`, `time`, `location`

- **Template Structure & Element IDs:**
  - `<div id="events-page">`
  - `<input id="event-search-input" type="text" placeholder="Search events...">` for client-side search
  - `<select id="event-category-filter">` with options: Conference, Concert, Sports, Workshop, Social
  - `<div id="events-grid">` - container for event cards
  - For each event card:
    - Use `<button id="view-event-button-{event_id}">View Details</button>`

- **Interactions:**
  - Event search and category filter are client-side filters
  - Clicking `view-event-button-{event_id}` navigates to `/events/{event_id}`

---

### 3. Event Details Page
- **Route:** `/events/<int:event_id>`
- **Methods:** [`GET`]
- **Function Name:** `event_details(event_id)`
- **Template:** `event_details.html`
- **Context Variables:**
  - `event` (dict) with keys: `event_id`, `event_name`, `date`, `time`, `location`, `description`, `venue_id`, `capacity`

- **Template Structure & Element IDs:**
  - `<div id="event-details-page">`
  - `<h1 id="event-title">` - event name
  - `<div id="event-date">` - event date and time
  - `<div id="event-location">` - event location
  - `<div id="event-description">` - event detailed description
  - `<button id="book-ticket-button">Book Ticket</button>`

- **Interactions:**
  - Clicking `book-ticket-button` redirects to Ticket Booking Page with event preselected `/bookings/book?event_id={event_id}`

---

### 4. Ticket Booking Page
- **Route:** `/bookings/book`
- **Methods:** [`GET`, `POST`]
- **Function Name:** `book_tickets()`
- **Template:** `ticket_booking.html`
- **Context Variables (GET):**
  - `events` (list of dicts) with `event_id`, `event_name`
  - `selected_event_id` (int or None) from query parameter `event_id` if present
  - `ticket_types` (list of str): ["General", "VIP", "Early Bird"]
- **Context Variables (POST):**
  - `booking_confirmation` (dict) with booking details: `event_name`, `ticket_count`, `ticket_type`, `total_amount`, `status`

- **Template Structure & Element IDs:**
  - `<div id="ticket-booking-page">`
  - `<select id="select-event-dropdown">` - selecting event
  - `<input id="ticket-quantity-input" type="number" min="1">` for number of tickets
  - `<select id="ticket-type-select">` selecting ticket type
  - `<button id="book-now-button">` to submit booking form
  - `<div id="booking-confirmation">` - shows booking confirmation after POST

- **Interactions:**
  - Form submission triggers POST to same route
  - On success, display booking confirmation

---

### 5. Participants Management Page
- **Route:** `/participants`
- **Methods:** [`GET`]
- **Function Name:** `participants_management()`
- **Template:** `participants.html`
- **Context Variables:**
  - `participants` (list of dicts): each with keys: `participant_id`, `name`, `email`, `event_name`, `status`
  - `status_options` (list of str): ["Registered", "Confirmed", "Attended"]

- **Template Structure & Element IDs:**
  - `<div id="participants-page">`
  - `<table id="participants-table">` with columns: Name, Email, Event, Status
  - `<button id="add-participant-button">` - to add participant (maybe opens modal or navigates to add participant page)
  - `<input id="search-participant-input" type="text" placeholder="Search participants...">`
  - `<select id="participant-status-filter">` with status options

- **Interactions:**
  - Searching and filtering is client-side or server-side
  - Add participant button might navigate to participant add interface

---

### 6. Venue Information Page
- **Route:** `/venues`
- **Methods:** [`GET`]
- **Function Name:** `venues_page()`
- **Template:** `venues.html`
- **Context Variables:**
  - `venues` (list of dicts): keys: `venue_id`, `venue_name`, `location`, `capacity`, `amenities`

- **Template Structure & Element IDs:**
  - `<div id="venues-page">`
  - `<input id="venue-search-input" type="text" placeholder="Search venues...">`
  - `<select id="venue-capacity-filter">` with options: Small, Medium, Large
  - `<div id="venues-grid">` containing venue cards
  - Each venue card has `<button id="view-venue-details-{venue_id}">View Details</button>`

- **Interactions:**
  - Search and capacity filter apply client-side or server-side filtering
  - Clicking view venue details redirects to `/venues/{venue_id}` (the venue detail page can be added if needed, but per requirements not explicitly listed)

---

### 7. Event Schedules Page
- **Route:** `/schedules`
- **Methods:** [`GET`]
- **Function Name:** `event_schedules()`
- **Template:** `schedules.html`
- **Context Variables:**
  - `schedules` (list of dicts): with keys: `schedule_id`, `event_id`, `event_name`, `session_title`, `session_time`, `duration_minutes`, `speaker`, `venue_id`
  - `events` (list of dicts): to populate schedule filter dropdown with `event_id`, `event_name`

- **Template Structure & Element IDs:**
  - `<div id="schedules-page">`
  - `<div id="schedules-timeline">` displays timeline of sessions
  - `<input id="schedule-filter-date" type="date">`
  - `<select id="schedule-filter-event">` with event options
  - `<button id="export-schedule-button">` for exporting schedules

- **Interactions:**
  - Filtering schedules by date and event
  - Export button triggers schedule data export

---

### 8. Bookings Summary Page
- **Route:** `/bookings`
- **Methods:** [`GET`]
- **Function Name:** `bookings_summary()`
- **Template:** `bookings.html`
- **Context Variables:**
  - `bookings` (list of dicts): with keys: `booking_id`, `event_name`, `date`, `ticket_count`, `ticket_type`, `status`

- **Template Structure & Element IDs:**
  - `<div id="bookings-page">`
  - `<input id="booking-search-input" type="text" placeholder="Search bookings...">`
  - `<table id="bookings-table">` columns: Event, Date, Ticket Count, Ticket Type, Status
  - Each booking row has `<button id="cancel-booking-button-{booking_id}">Cancel Booking</button>`
  - `<button id="back-to-dashboard">Back to Dashboard</button>`

- **Interactions:**
  - Cancel button triggers cancellation (could be POST or AJAX, confirm prompt)
  - Search input for filtering bookings client-side
  - Back button navigates to `/`

---

## Summary Notes:
- All context variables fully map to data files as described. For example, `events` loaded from `events.txt` parsed into dicts etc.
- Dynamic element IDs follow exact naming conventions provided.
- Routes provide clear navigations for all user interactions.
- POST only used for ticket booking submission; cancel booking could also be POST if implemented.

This completes the independent design_candidate_b.md for EventPlanning application.
