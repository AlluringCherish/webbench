# EventPlanning Web Application - Consolidated Design Specification

---

## 1. Flask Routes and Methods

```python
from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)

# Dashboard Page
@app.route('/', methods=['GET'])
def dashboard():
    # Load data for featured events and venues
    # Data loaded from events.txt, venues.txt
    featured_events = load_featured_events()  # list of dicts with keys: event_id, event_name, date, location, description, venue_id
    featured_venues = load_featured_venues()  # list of dicts with keys: venue_id, venue_name, location, capacity, amenities
    return render_template('dashboard.html', 
                           featured_events=featured_events, 
                           featured_venues=featured_venues)

# Events Listing Page
@app.route('/events', methods=['GET'])
def events_listing():
    # Load all events
    events = load_all_events()  # list of dicts with keys: event_id, event_name, category, date, time, location
    categories = ["Conference", "Concert", "Sports", "Workshop", "Social"]

    # Optional query parameters for search and filter
    search_query = request.args.get('search', '')
    category_filter = request.args.get('category', '')

    # Filter events according to search and category
    filtered_events = filter_events(events, search_query, category_filter)

    return render_template('events.html', 
                           events=filtered_events, 
                           categories=categories, 
                           search_query=search_query, 
                           category_filter=category_filter)

# Event Details Page
@app.route('/events/<int:event_id>', methods=['GET'])
def event_details(event_id):
    event = get_event_by_id(event_id)  # dict with keys: event_id, event_name, date, time, location, description, venue_id, capacity
    if not event:
        return "Event not found", 404
    return render_template('event_details.html', event=event)

# Ticket Booking Page
@app.route('/bookings/book', methods=['GET', 'POST'])
def book_tickets():
    events = load_all_events()  # for select-event-dropdown, list of dicts with event_id, event_name
    ticket_types = ["General", "VIP", "Early Bird"]
    booking_confirmation = None
    selected_event_id = request.args.get('event_id', type=int)

    if request.method == 'POST':
        selected_event_id = int(request.form['select-event-dropdown'])
        ticket_quantity = int(request.form['ticket-quantity-input'])
        ticket_type = request.form['ticket-type-select']

        booking_confirmation = process_booking(selected_event_id, ticket_quantity, ticket_type)

    return render_template('ticket_booking.html', 
                           events=events, 
                           ticket_types=ticket_types, 
                           selected_event_id=selected_event_id, 
                           booking_confirmation=booking_confirmation)

# Participants Management Page
@app.route('/participants', methods=['GET'])
def participants_management():
    participants = load_all_participants()  # list of dicts with participant_id, name, email, event_name, status
    status_options = ["Registered", "Confirmed", "Attended"]

    search_query = request.args.get('search', '')
    status_filter = request.args.get('status', '')

    filtered_participants = filter_participants(participants, search_query, status_filter)

    return render_template('participants.html', 
                           participants=filtered_participants, 
                           status_options=status_options, 
                           search_query=search_query, 
                           status_filter=status_filter)

# Venue Information Page
@app.route('/venues', methods=['GET'])
def venues_page():
    venues = load_all_venues()  # list of dicts with venue_id, venue_name, location, capacity, amenities
    capacities = ["Small", "Medium", "Large"]

    search_query = request.args.get('search', '')
    capacity_filter = request.args.get('capacity', '')

    filtered_venues = filter_venues(venues, search_query, capacity_filter)

    return render_template('venues.html', 
                           venues=filtered_venues, 
                           capacities=capacities, 
                           search_query=search_query, 
                           capacity_filter=capacity_filter)

# Event Schedules Page
@app.route('/schedules', methods=['GET'])
def event_schedules():
    schedules = load_all_schedules()  # list of dicts with schedule_id, event_id, event_name, session_title, session_time, duration_minutes, speaker, venue_id
    events = load_all_events()  # for schedule filter

    filter_date = request.args.get('date', '')
    filter_event = request.args.get('event', '')

    filtered_schedules = filter_schedules(schedules, filter_date, filter_event)

    return render_template('schedules.html', 
                           schedules=filtered_schedules, 
                           events=events, 
                           filter_date=filter_date, 
                           filter_event=filter_event)

# Bookings Summary Page
@app.route('/bookings', methods=['GET'])
def bookings_summary():
    bookings = load_all_bookings()  # list of dicts with booking_id, event_name, date, ticket_count, ticket_type, status

    search_query = request.args.get('search', '')

    filtered_bookings = filter_bookings(bookings, search_query)

    return render_template('bookings.html', 
                           bookings=filtered_bookings, 
                           search_query=search_query)

# Cancel Booking
@app.route('/cancel_booking/<int:booking_id>', methods=['POST'])
def cancel_booking(booking_id):
    success = cancel_booking_by_id(booking_id)
    return redirect(url_for('bookings_summary'))

# Back to Dashboard
@app.route('/back_to_dashboard', methods=['GET'])
def back_to_dashboard():
    return redirect(url_for('dashboard'))

# Note: Helper functions load_all_events, filter_events, process_booking, etc., parse local text files as specified in requirements.
```

---

## 2. Page Titles and Container IDs

| Page                  | Template Filename     | Container Div ID       | Key Element IDs & Patterns                                              |
|-----------------------|----------------------|-----------------------|------------------------------------------------------------------------|
| Dashboard             | dashboard.html        | dashboard-page         | featured-events (div), browse-events-button (button), view-tickets-button (button), venues-button (button) |
| Events Listing        | events.html           | events-page            | event-search-input (input), event-category-filter (dropdown), events-grid (div), view-event-button-{event_id} (button) |
| Event Details         | event_details.html    | event-details-page     | event-title (h1), event-date (div), event-location (div), event-description (div), book-ticket-button (button) |
| Ticket Booking        | ticket_booking.html   | ticket-booking-page    | select-event-dropdown (dropdown), ticket-quantity-input (number input), ticket-type-select (dropdown), book-now-button (button), booking-confirmation (div) |
| Participants Management| participants.html     | participants-page      | participants-table (table), add-participant-button (button), search-participant-input (input), participant-status-filter (dropdown) |
| Venue Information     | venues.html           | venues-page            | venues-grid (div), venue-search-input (input), venue-capacity-filter (dropdown), view-venue-details-{venue_id} (button) |
| Event Schedules       | schedules.html        | schedules-page         | schedules-timeline (div), schedule-filter-date (date input), schedule-filter-event (dropdown), export-schedule-button (button) |
| Bookings Summary      | bookings.html         | bookings-page          | bookings-table (table), booking-search-input (input), cancel-booking-button-{booking_id} (button), back-to-dashboard (button) |

---

## 3. Context Variables and Data Files

### Dashboard Page
- `featured_events`: list of dicts loaded from `events.txt` filtered to featured events.
  Each dict keys: `event_id`, `event_name`, `date`, `location`, `description`, `venue_id`
- `featured_venues`: list of dicts loaded from `venues.txt` filtered to featured venues.
  Each dict keys: `venue_id`, `venue_name`, `location`, `capacity`, `amenities`

### Events Listing Page
- `events`: list of event dicts from `events.txt` filtered by search term and category.
- `categories`: fixed list ["Conference", "Concert", "Sports", "Workshop", "Social"]
- `search_query`: string search term from query parameter
- `category_filter`: string category selected from query parameter

### Event Details Page
- `event`: dict of event data from `events.txt` by `event_id` with keys: `event_id`, `event_name`, `date`, `time`, `location`, `description`, `venue_id`, `capacity`

### Ticket Booking Page
- `events`: list of all events from `events.txt`, each with `event_id`, `event_name`
- `ticket_types`: fixed list ["General", "VIP", "Early Bird"]
- `selected_event_id`: int or None, parsed from query parameter `event_id` in GET or form POST
- `booking_confirmation`: dict or None, showing booking details after successful POST

### Participants Management Page
- `participants`: list of dicts from `participants.txt` filtered by search and status
- `status_options`: fixed list ["Registered", "Confirmed", "Attended"]
- `search_query`: string
- `status_filter`: string

### Venue Information Page
- `venues`: list of dicts from `venues.txt` filtered by search and capacity
- `capacities`: fixed list ["Small", "Medium", "Large"]
- `search_query`: string
- `capacity_filter`: string

### Event Schedules Page
- `schedules`: list of dicts from `schedules.txt` filtered by date and event
- `events`: list of dicts from `events.txt` for filter dropdown
- `filter_date`: string date filter
- `filter_event`: string event filter

### Bookings Summary Page
- `bookings`: list of dicts from `bookings.txt` filtered by search
- `search_query`: string

---

## 4. Navigation and Interaction Details

### Dashboard Page
- `browse-events-button`: navigates to `/events`
- `view-tickets-button`: navigates to `/bookings`
- `venues-button`: navigates to `/venues`

### Events Listing Page
- Search input (`event-search-input`) and category filter dropdown (`event-category-filter`) reload page with query parameters `search` and `category`.
- Click `view-event-button-{event_id}` navigates to Event Details page `/events/{event_id}`.

### Event Details Page
- Click `book-ticket-button` navigates to Ticket Booking page `/bookings/book?event_id={event_id}` with event preselected.

### Ticket Booking Page
- User selects event, ticket quantity, and ticket type.
- Submitting form (button `book-now-button`) posts to `/bookings/book`.
- On success, shows booking confirmation in `booking-confirmation` div.

### Participants Management Page
- Search input (`search-participant-input`) and status filter (`participant-status-filter`) reload or filter participants.
- `add-participant-button` navigates or opens participant add UI.

### Venue Information Page
- Search (`venue-search-input`) and capacity filter (`venue-capacity-filter`) to filter venues.
- Clicking `view-venue-details-{venue_id}` button navigates to `/venues/{venue_id}` (venue detail page optional, can be implemented).

### Event Schedules Page
- Date filter (`schedule-filter-date`) and event filter dropdown (`schedule-filter-event`) filter schedule timeline.
- `export-schedule-button` triggers export of filtered schedule (e.g., CSV).

### Bookings Summary Page
- Booking search input (`booking-search-input`) filters bookings table.
- Cancel button `cancel-booking-button-{booking_id}` posts to `/cancel_booking/{booking_id}`.
- `back-to-dashboard` button navigates to `/` (dashboard).

---

## 5. Template Filenames
- Dashboard: `dashboard.html`
- Events Listing: `events.html`
- Event Details: `event_details.html`
- Ticket Booking: `ticket_booking.html`
- Participants Management: `participants.html`
- Venue Information: `venues.html`
- Event Schedules: `schedules.html`
- Bookings Summary: `bookings.html`

---

## 6. Data File Dependencies
- `events.txt`: stores events data
- `venues.txt`: stores venues data
- `tickets.txt`: stores ticket info (types, availability)
- `bookings.txt`: stores booking records
- `participants.txt`: stores participant info
- `schedules.txt`: stores schedule sessions


---

This consolidated design_spec.md fully merges both candidates, resolves route path inconsistencies (`/book_ticket` vs `/bookings/book` unified to `/bookings/book`), standardizes variable names, element IDs, template file names, and interaction flows exactly matching user requirements. It is ready for implementation as the definitive blueprint.
