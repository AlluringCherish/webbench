# Design Specification for 'EventPlanning' Web Application

---

## 1. Flask Routes

| Route Path                  | Function Name             | HTTP Methods  | Template Filename           | Context Variables
|-----------------------------|---------------------------|---------------|-----------------------------|------------------|
| /                           | dashboard_page            | GET           | dashboard.html              | featured_events  |
| /events                     | events_listing_page       | GET           | events_listing.html         | events, categories, filters |
| /events/<int:event_id>      | event_details_page        | GET           | event_details.html          | event             |
| /booking                    | ticket_booking_page       | GET, POST     | ticket_booking.html         | events, booking_confirmation|
| /participants               | participants_management   | GET, POST     | participants_management.html| participants, search_filter, status_filter|
| /venues                     | venues_information_page   | GET           | venues.html                 | venues, capacity_filter |
| /venues/<int:venue_id>      | venue_details_page        | GET           | venue_details.html          | venue             |
| /schedules                  | event_schedules_page      | GET           | event_schedules.html        | schedules, filter_date, filter_event |
| /schedules/export           | export_schedules          | POST          | N/A (trigger export)         | N/A               |
| /bookings                  | bookings_summary_page     | GET, POST     | bookings_summary.html       | bookings, search_filter  |
| /bookings/cancel/<int:booking_id> | cancel_booking          | POST          | N/A (redirect)               | N/A               |

Notes:
- The ticket booking page supports POST to submit booking and updates booking_confirmation context.
- Participants page POST is assumed to handle adding new participants.
- Export schedules is triggered via POST to /schedules/export.
- Cancel booking is a POST to /bookings/cancel/<booking_id>.

---

## 2. HTML Templates

### 1. dashboard.html
- Page Title: "Event Planning Dashboard"
- Element IDs:
  - `dashboard-page` (Div) - Container
  - `featured-events` (Div) - Featured event recommendations
  - `browse-events-button` (Button) - Navigates to `/events`
  - `view-tickets-button` (Button) - Navigates to `/bookings`
  - `venues-button` (Button) - Navigates to `/venues`

### 2. events_listing.html
- Page Title: "Events Catalog"
- Element IDs:
  - `events-page` (Div) - Container
  - `event-search-input` (Input) - Search input
  - `event-category-filter` (Dropdown) - Category filter
  - `events-grid` (Div) - Grid of event cards
  - `view-event-button-{event_id}` (Button) - Navigate to `/events/<event_id>`

### 3. event_details.html
- Page Title: "Event Details"
- Element IDs:
  - `event-details-page` (Div) - Container
  - `event-title` (H1) - Event Title
  - `event-date` (Div) - Date and time
  - `event-location` (Div) - Location
  - `event-description` (Div) - Description
  - `book-ticket-button` (Button) - Navigate to `/booking` with selected event

### 4. ticket_booking.html
- Page Title: "Book Your Tickets"
- Element IDs:
  - `ticket-booking-page` (Div) - Container
  - `select-event-dropdown` (Dropdown) - List of events
  - `ticket-quantity-input` (Input number) - Number of tickets
  - `ticket-type-select` (Dropdown) - Ticket type select
  - `book-now-button` (Button) - Submit booking form
  - `booking-confirmation` (Div) - Show booking confirmation after successful POST

### 5. participants_management.html
- Page Title: "Participants Management"
- Element IDs:
  - `participants-page` (Div) - Container
  - `participants-table` (Table) - Participant records
  - `add-participant-button` (Button) - Trigger add participant workflow
  - `search-participant-input` (Input) - Search field
  - `participant-status-filter` (Dropdown) - Status filter

### 6. venues.html
- Page Title: "Venues"
- Element IDs:
  - `venues-page` (Div) - Container
  - `venues-grid` (Div) - Venue cards grid
  - `venue-search-input` (Input) - Search venues
  - `venue-capacity-filter` (Dropdown) - Capacity filter
  - `view-venue-details-{venue_id}` (Button) - Navigate to `/venues/<venue_id>`

### 7. venue_details.html
- Page Title: "Venue Details"
- Element IDs:
  - `venue-details-page` (Div) - Container
  - Display venue name, location, capacity, amenities, contact info

### 8. event_schedules.html
- Page Title: "Event Schedules"
- Element IDs:
  - `schedules-page` (Div) - Container
  - `schedules-timeline` (Div) - Timeline of events and sessions
  - `schedule-filter-date` (Input date) - Date filter
  - `schedule-filter-event` (Dropdown) - Event filter
  - `export-schedule-button` (Button) - Trigger schedule export POST

### 9. bookings_summary.html
- Page Title: "My Bookings"
- Element IDs:
  - `bookings-page` (Div) - Container
  - `bookings-table` (Table) - Booking records
  - `booking-search-input` (Input) - Search bookings
  - `cancel-booking-button-{booking_id}` (Button) - POST cancel booking
  - `back-to-dashboard` (Button) - Navigate to `/`

---

## 3. Data Files and Backend Data Handling

### Events Data
- File: `data/events.txt`
- Fields (in order):
  - event_id (int)
  - event_name (string)
  - category (string)
  - date (YYYY-MM-DD)
  - time (HH:MM 24hr)
  - location (string)
  - description (string)
  - venue_id (int)
  - capacity (int)
- Usage: On loading events listing, event details pages, and populate event selection dropdowns in booking.

### Venues Data
- File: `data/venues.txt`
- Fields (in order):
  - venue_id (int)
  - venue_name (string)
  - location (string)
  - capacity (int)
  - amenities (string comma-separated)
  - contact (string email)
- Usage: For venue listing and venue details display, and mapping events to venues.

### Tickets Data
- File: `data/tickets.txt`
- Fields (in order):
  - ticket_id (int)
  - event_id (int)
  - ticket_type (string)
  - price (float)
  - available_count (int)
  - sold_count (int)
- Usage: To display ticket types available for booking and track availability for each event.

### Bookings Data
- File: `data/bookings.txt`
- Fields (in order):
  - booking_id (int)
  - event_id (int)
  - customer_name (string)
  - booking_date (YYYY-MM-DD)
  - ticket_count (int)
  - ticket_type (string)
  - total_amount (float)
  - status (string)
- Usage: For bookings summary page, booking confirmation, and manage cancellations.

### Participants Data
- File: `data/participants.txt`
- Fields (in order):
  - participant_id (int)
  - event_id (int)
  - name (string)
  - email (string)
  - booking_id (int)
  - status (string)
  - registration_date (YYYY-MM-DD)
- Usage: For participants management page to list, search, filter, and add participants.

### Schedules Data
- File: `data/schedules.txt`
- Fields (in order):
  - schedule_id (int)
  - event_id (int)
  - session_title (string)
  - session_time (YYYY-MM-DD HH:MM)
  - duration_minutes (int)
  - speaker (string)
  - venue_id (int)
- Usage: For showing event schedules timeline, filtering schedules, and export functionality.

---

## 4. Navigation Actions Summary

- Dashboard Page Buttons:
  - `browse-events-button` -> route `/events`
  - `view-tickets-button` -> route `/bookings`
  - `venues-button` -> route `/venues`

- Events Listing Page:
  - Each `view-event-button-{event_id}` -> route `/events/<event_id>`

- Event Details Page:
  - `book-ticket-button` -> route `/booking` (passes selected event)

- Ticket Booking Page:
  - `book-now-button` submits booking form via POST to `/booking`
  - On success, shows `booking-confirmation` div content

- Participants Management Page:
  - `add-participant-button`: triggers participant add workflow (modal/form handled in frontend)

- Venue Information Page:
  - `view-venue-details-{venue_id}` -> route `/venues/<venue_id>`

- Event Schedules Page:
  - `export-schedule-button` submits POST to `/schedules/export` to export data

- Bookings Summary Page:
  - `cancel-booking-button-{booking_id}` submits POST to `/bookings/cancel/<booking_id>` to cancel
  - `back-to-dashboard` button routes to `/`

---

This design specification ensures consistent routing, template structure, and data file access patterns to facilitate parallel frontend and backend development for the 'EventPlanning' application.