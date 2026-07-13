# EventPlanning Web Application - Design Candidate A

## 1. Flask Routes and Methods

```python
from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)

# Dashboard Page
@app.route('/', methods=['GET'])
def dashboard():
    # Load data for featured events and venues
    # Data loaded from events.txt, venues.txt
    featured_events = load_featured_events()  # e.g., list of dicts
    featured_venues = load_featured_venues()  # e.g., list of dicts
    return render_template('dashboard.html', 
                           featured_events=featured_events, 
                           featured_venues=featured_venues)

# Events Listing Page
@app.route('/events', methods=['GET'])
def events_listing():
    # Load all events to display
    events = load_all_events()  # list of dicts
    categories = ["Conference", "Concert", "Sports", "Workshop", "Social"]
    
    # Accept optional query parameters for search & filter
    search_query = request.args.get('search', '')
    category_filter = request.args.get('category', '')
    
    # Filter logic outside template
    filtered_events = filter_events(events, search_query, category_filter)
    
    return render_template('events.html', 
                           events=filtered_events, 
                           categories=categories, 
                           search_query=search_query,
                           category_filter=category_filter)

# Event Details Page
@app.route('/events/<int:event_id>', methods=['GET'])
def event_details(event_id):
    # Fetch event detail by event_id
    event = get_event_by_id(event_id)
    if not event:
        return "Event not found", 404
    return render_template('event_details.html', event=event)

# Ticket Booking Page
@app.route('/book_ticket', methods=['GET', 'POST'])
def book_ticket():
    events = load_all_events()  # For select-event-dropdown
    ticket_types = ["General", "VIP", "Early Bird"]
    confirmation = None

    if request.method == 'POST':
        # Retrieve form data
        selected_event_id = int(request.form['select-event-dropdown'])
        ticket_quantity = int(request.form['ticket-quantity-input'])
        ticket_type = request.form['ticket-type-select']

        # Process booking and prepare confirmation message
        confirmation = process_booking(selected_event_id, ticket_quantity, ticket_type)

    return render_template('book_ticket.html', 
                           events=events, 
                           ticket_types=ticket_types, 
                           confirmation=confirmation)

# Participants Management Page
@app.route('/participants', methods=['GET'])
def participants_management():
    participants = load_all_participants()  # list of dicts
    statuses = ["Registered", "Confirmed", "Attended"]

    # Search and filter query parameters
    search_query = request.args.get('search', '')
    status_filter = request.args.get('status', '')

    filtered_participants = filter_participants(participants, search_query, status_filter)

    return render_template('participants.html', 
                           participants=filtered_participants,
                           statuses=statuses,
                           search_query=search_query,
                           status_filter=status_filter)

# Venue Information Page
@app.route('/venues', methods=['GET'])
def venues_page():
    venues = load_all_venues()
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
    schedules = load_all_schedules()  # list of dicts
    events = load_all_events()  # for filter

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
    bookings = load_all_bookings()

    search_query = request.args.get('search', '')

    filtered_bookings = filter_bookings(bookings, search_query)

    return render_template('bookings.html', 
                           bookings=filtered_bookings,
                           search_query=search_query)

@app.route('/cancel_booking/<int:booking_id>', methods=['POST'])
def cancel_booking(booking_id):
    # Cancel the booking by booking_id
    success = cancel_booking_by_id(booking_id)
    return redirect(url_for('bookings_summary'))

@app.route('/back_to_dashboard', methods=['GET'])
def back_to_dashboard():
    return redirect(url_for('dashboard'))

# Note: Helper functions load_all_events, filter_events, etc., are assumed to parse local text files as specified.
```

---

## 2. Templates and Element IDs

| Page | Template Filename | Container Div ID | Key Elements & IDs |
|---|---|---|---|
| Dashboard | dashboard.html | dashboard-page | featured-events (div), browse-events-button (button), view-tickets-button (button), venues-button (button) |
| Events Listing | events.html | events-page | event-search-input (input), event-category-filter (dropdown), events-grid (div), view-event-button-{event_id} (button for each event) |
| Event Details | event_details.html | event-details-page | event-title (h1), event-date (div), event-location (div), event-description (div), book-ticket-button (button) |
| Ticket Booking | book_ticket.html | ticket-booking-page | select-event-dropdown (dropdown), ticket-quantity-input (number input), ticket-type-select (dropdown), book-now-button (button), booking-confirmation (div) |
| Participants Management | participants.html | participants-page | participants-table (table), add-participant-button (button), search-participant-input (input), participant-status-filter (dropdown) |
| Venue Information | venues.html | venues-page | venues-grid (div), venue-search-input (input), venue-capacity-filter (dropdown), view-venue-details-{venue_id} (button for each venue) |
| Event Schedules | schedules.html | schedules-page | schedules-timeline (div), schedule-filter-date (date input), schedule-filter-event (dropdown), export-schedule-button (button) |
| Bookings Summary | bookings.html | bookings-page | bookings-table (table), booking-search-input (input), cancel-booking-button-{booking_id} (button for each booking), back-to-dashboard (button) |

---

## 3. Context Variables and Data Files

### Dashboard Page
- Variables:
  - featured_events: list of dicts (from `events.txt`, filtered to featured)
  - featured_venues: list of dicts (from `venues.txt`, filtered to featured)

### Events Listing Page
- Variables:
  - events: list of event dicts from `events.txt` filtered by search and category
  - categories: list of available categories
  - search_query: string search term
  - category_filter: string category selected

### Event Details Page
- Variables:
  - event: dict of event data by event_id from `events.txt`

### Ticket Booking Page
- Variables:
  - events: list of all events from `events.txt` for dropdown
  - ticket_types: fixed list ["General", "VIP", "Early Bird"]
  - confirmation: dict or None with booking confirmation details after POST

### Participants Management Page
- Variables:
  - participants: list of participant dicts from `participants.txt` filtered by search and status
  - statuses: list ["Registered", "Confirmed", "Attended"]
  - search_query: string
  - status_filter: string

### Venue Information Page
- Variables:
  - venues: list of venue dicts from `venues.txt` filtered
  - capacities: list ["Small", "Medium", "Large"]
  - search_query: string
  - capacity_filter: string

### Event Schedules Page
- Variables:
  - schedules: list of schedule dicts from `schedules.txt` filtered
  - events: list of events for filter dropdown
  - filter_date: string date filter
  - filter_event: string event filter

### Bookings Summary Page
- Variables:
  - bookings: list of booking dicts from `bookings.txt` filtered
  - search_query: string

---

## 4. Interactions and Messages

### Dashboard Page
- Buttons:
  - browse-events-button: navigate to `/events`
  - view-tickets-button: navigate to `/bookings`
  - venues-button: navigate to `/venues`

### Events Listing Page
- User enters search in event-search-input, selects category in event-category-filter
- Filter triggers reload of `/events?search=...&category=...`
- Click view-event-button-{event_id}: navigate to `/events/{event_id}`

### Event Details Page
- book-ticket-button: navigate to `/book_ticket` with event preselected (can be done via query parameter)

### Ticket Booking Page
- User selects event, ticket quantity, ticket type
- book-now-button submits form POST to `/book_ticket`
- On success, booking-confirmation div shows confirmation details

### Participants Management Page
- Search-participant-input and participant-status-filter filter participants table (reload or dynamic)
- add-participant-button: navigates to a participant add form (not detailed here)

### Venue Information Page
- venue-search-input and venue-capacity-filter filter venues grid
- view-venue-details-{venue_id}: navigates to venue details page (not defined here but can be `/venues/{venue_id}`)

### Event Schedules Page
- schedule-filter-date and schedule-filter-event filter schedules timeline
- export-schedule-button: triggers export of current filtered schedule data (e.g., CSV)

### Bookings Summary Page
- booking-search-input filters bookings-table
- cancel-booking-button-{booking_id} posts to cancel booking
- back-to-dashboard button navigates `/`

---

This design candidate outlines a complete provisional architecture allowing implementation of EventPlanning with explicit routes, templates, element IDs, and data context variables aligned with the requirements document.
