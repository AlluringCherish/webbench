# Requirements Analysis for 'EventPlanning' Web Application

---

## 1. Page Specifications

### 1. Dashboard Page
- **Page Title:** Event Planning Dashboard
- **Elements:**
  - ID: `dashboard-page` (Div) - Container for dashboard page.
  - ID: `featured-events` (Div) - Displays featured event recommendations.
  - ID: `browse-events-button` (Button) - Navigates to Events Listing Page.
  - ID: `view-tickets-button` (Button) - Navigates to Bookings Summary Page.
  - ID: `venues-button` (Button) - Navigates to Venue Information Page.

### 2. Events Listing Page
- **Page Title:** Events Catalog
- **Elements:**
  - ID: `events-page` (Div) - Container for events listing.
  - ID: `event-search-input` (Input) - Search events by name, location, or date.
  - ID: `event-category-filter` (Dropdown) - Filter events by category (Conference, Concert, Sports, Workshop, Social).
  - ID: `events-grid` (Div) - Grid of event cards with image, title, date, location.
  - ID: `view-event-button-{event_id}` (Button) - View details for a specific event.

### 3. Event Details Page
- **Page Title:** Event Details
- **Elements:**
  - ID: `event-details-page` (Div) - Container for event details.
  - ID: `event-title` (H1) - Displays event title.
  - ID: `event-date` (Div) - Displays event date and time.
  - ID: `event-location` (Div) - Displays event location.
  - ID: `event-description` (Div) - Detailed event description.
  - ID: `book-ticket-button` (Button) - Initiates booking process for the event.

### 4. Ticket Booking Page
- **Page Title:** Book Your Tickets
- **Elements:**
  - ID: `ticket-booking-page` (Div) - Container for ticket booking.
  - ID: `select-event-dropdown` (Dropdown) - Select event for booking.
  - ID: `ticket-quantity-input` (Input number) - Enter ticket quantity.
  - ID: `ticket-type-select` (Dropdown) - Select ticket type (General, VIP, Early Bird).
  - ID: `book-now-button` (Button) - Confirm booking.
  - ID: `booking-confirmation` (Div) - Displays booking confirmation details.

### 5. Participants Management Page
- **Page Title:** Participants Management
- **Elements:**
  - ID: `participants-page` (Div) - Container for participant management.
  - ID: `participants-table` (Table) - Displays participants with columns: name, email, event, status.
  - ID: `add-participant-button` (Button) - Add new participant.
  - ID: `search-participant-input` (Input) - Search participants by name/email.
  - ID: `participant-status-filter` (Dropdown) - Filter by status (Registered, Confirmed, Attended).

### 6. Venue Information Page
- **Page Title:** Venues
- **Elements:**
  - ID: `venues-page` (Div) - Container for venues.
  - ID: `venues-grid` (Div) - Grid of venue cards with name, capacity, amenities.
  - ID: `venue-search-input` (Input) - Search venues by name or location.
  - ID: `venue-capacity-filter` (Dropdown) - Filter by capacity (Small, Medium, Large).
  - ID: `view-venue-details-{venue_id}` (Button) - View details of a specific venue.

### 7. Event Schedules Page
- **Page Title:** Event Schedules
- **Elements:**
  - ID: `schedules-page` (Div) - Container for schedules.
  - ID: `schedules-timeline` (Div) - Timeline view of upcoming events and sessions.
  - ID: `schedule-filter-date` (Input date) - Filter schedules by date.
  - ID: `schedule-filter-event` (Dropdown) - Filter schedules by event.
  - ID: `export-schedule-button` (Button) - Export schedule data.

### 8. Bookings Summary Page
- **Page Title:** My Bookings
- **Elements:**
  - ID: `bookings-page` (Div) - Container for bookings.
  - ID: `bookings-table` (Table) - Displays bookings with columns: event, date, ticket count, status.
  - ID: `booking-search-input` (Input) - Search bookings by event name or booking ID.
  - ID: `cancel-booking-button-{booking_id}` (Button) - Cancel a specific booking.
  - ID: `back-to-dashboard` (Button) - Navigates back to Dashboard.

---

## 2. Navigation Flows

- From **Dashboard Page**:
  - `browse-events-button` -> Events Listing Page
  - `view-tickets-button` -> Bookings Summary Page
  - `venues-button` -> Venue Information Page

- From **Events Listing Page**:
  - `view-event-button-{event_id}` -> Event Details Page (specific event)

- From **Event Details Page**:
  - `book-ticket-button` -> Ticket Booking Page

- From **Ticket Booking Page**:
  - After booking success, display confirmation in `booking-confirmation`

- From **Participants Management Page**:
  - `add-participant-button` triggers participant addition workflow (form/modal assumed)

- From **Venue Information Page**:
  - `view-venue-details-{venue_id}` -> Venue detailed view (not separately defined but presumably shows venue info)

- From **Event Schedules Page**:
  - `export-schedule-button` triggers schedule export functionality

- From **Bookings Summary Page**:
  - `cancel-booking-button-{booking_id}` cancels booking
  - `back-to-dashboard` => Dashboard Page

---

## 3. Data Formats

### 1. Events Data
- **File:** `events.txt`
- **Fields and order:**
  - `event_id` (int)
  - `event_name` (string)
  - `category` (string: Conference, Concert, Sports, Workshop, Social)
  - `date` (YYYY-MM-DD)
  - `time` (HH:MM 24hr)
  - `location` (string)
  - `description` (string)
  - `venue_id` (int, foreign key to venues)
  - `capacity` (int)
- **Example:**
  ```
  1|Tech Conference 2025|Conference|2025-03-15|09:00|Convention Center, San Francisco|Annual technology conference discussing latest innovations|1|500
  ```

### 2. Venues Data
- **File:** `venues.txt`
- **Fields and order:**
  - `venue_id` (int)
  - `venue_name` (string)
  - `location` (string)
  - `capacity` (int)
  - `amenities` (string comma-separated)
  - `contact` (string email)
- **Example:**
  ```
  1|Convention Center|San Francisco, CA|500|WiFi, Parking, Catering|contact@convention.com
  ```

### 3. Tickets Data
- **File:** `tickets.txt`
- **Fields and order:**
  - `ticket_id` (int)
  - `event_id` (int)
  - `ticket_type` (string: General, VIP, Early Bird)
  - `price` (float)
  - `available_count` (int)
  - `sold_count` (int)
- **Example:**
  ```
  1|1|General|49.99|500|150
  ```

### 4. Bookings Data
- **File:** `bookings.txt`
- **Fields and order:**
  - `booking_id` (int)
  - `event_id` (int)
  - `customer_name` (string)
  - `booking_date` (YYYY-MM-DD)
  - `ticket_count` (int)
  - `ticket_type` (string)
  - `total_amount` (float)
  - `status` (string: Confirmed, Pending, Cancelled)
- **Example:**
  ```
  1|1|Alice Johnson|2025-02-01|2|General|99.98|Confirmed
  ```

### 5. Participants Data
- **File:** `participants.txt`
- **Fields and order:**
  - `participant_id` (int)
  - `event_id` (int)
  - `name` (string)
  - `email` (string)
  - `booking_id` (int)
  - `status` (string: Registered, Confirmed, Attended)
  - `registration_date` (YYYY-MM-DD)
- **Example:**
  ```
  1|1|Alice Johnson|alice@email.com|1|Confirmed|2025-02-01
  ```

### 6. Schedules Data
- **File:** `schedules.txt`
- **Fields and order:**
  - `schedule_id` (int)
  - `event_id` (int)
  - `session_title` (string)
  - `session_time` (YYYY-MM-DD HH:MM)
  - `duration_minutes` (int)
  - `speaker` (string)
  - `venue_id` (int)
- **Example:**
  ```
  1|1|Opening Keynote|2025-03-15 09:00|60|John Smith|1
  ```

---

## 4. User Actions and Expected Outcomes

### Browsing Events
- User can search/filter events on the Events Listing Page by name, location, date, and category.
- User can click `view-event-button-{event_id}` to see detailed info of the event.

### Viewing Event Details
- User sees comprehensive event info including title, date/time, location, description.
- User can proceed to book tickets via `book-ticket-button`.

### Booking Tickets
- User selects an event from `select-event-dropdown`.
- Enters desired ticket quantity in `ticket-quantity-input`.
- Chooses ticket type from `ticket-type-select`.
- Confirms booking by clicking `book-now-button`.
- System updates availability and booking records.
- Confirmation with booking details displayed in `booking-confirmation`.

### Managing Participants
- User views participant list with search and status filter on Participants Management Page.
- User can add new participants via `add-participant-button`.

### Venues Exploration
- User can search/filter venues by name, location, and capacity.
- User clicks `view-venue-details-{venue_id}` to see detailed venue info.

### Viewing Event Schedules
- User filters schedules by date and event.
- User views timeline in `schedules-timeline`.
- Can export schedules using `export-schedule-button`.

### Booking Summary Management
- User views all bookings
- Searches bookings by event or booking ID
- Cancels booking via `cancel-booking-button-{booking_id}`
- Returns to dashboard via `back-to-dashboard` button.

---

This completes the detailed requirements analysis for the 'EventPlanning' web application, structured to assist the design and development team for the subsequent phases.