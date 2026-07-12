from flask import Flask, render_template, redirect, url_for, request
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

# Global in-memory data stores
_events = []
_venues = []
_tickets = []
_bookings = []
_participants = []
_schedules = []

# Utility functions to load data from pipe-delimited files

def load_events():
    global _events
    _events = []
    try:
        with open('data/events.txt', 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 6:
                    continue
                try:
                    event = {
                        'event_id': int(parts[0]),
                        'event_name': parts[1],
                        'location': parts[2],
                        'description': parts[3],
                        'category_id': int(parts[4]),
                        'max_tickets': int(parts[5])
                    }
                    _events.append(event)
                except Exception:
                    continue
    except Exception:
        _events = []


def load_venues():
    global _venues
    _venues = []
    try:
        with open('data/venues.txt', 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 6:
                    continue
                try:
                    amenities_list = parts[4].split(', ') if parts[4].strip() else []
                    venue = {
                        'venue_id': int(parts[0]),
                        'name': parts[1],
                        'location': parts[2],
                        'capacity': int(parts[3]),
                        'amenities': amenities_list,
                        'contact_email': parts[5]
                    }
                    _venues.append(venue)
                except Exception:
                    continue
    except Exception:
        _venues = []


def load_tickets():
    global _tickets
    _tickets = []
    try:
        with open('data/tickets.txt', 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 6:
                    continue
                try:
                    ticket = {
                        'ticket_id': int(parts[0]),
                        'event_id': int(parts[1]),
                        'ticket_type': parts[2],
                        'price': float(parts[3]),
                        'quantity_available': int(parts[4]),
                        'min_purchase': int(parts[5])
                    }
                    _tickets.append(ticket)
                except Exception:
                    continue
    except Exception:
        _tickets = []


def load_bookings():
    global _bookings
    _bookings = []
    try:
        with open('data/bookings.txt', 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 6:
                    continue
                try:
                    booking = {
                        'participant_name': parts[0],
                        'booking_date': parts[1],  # as string in YYYY-MM-DD
                        'ticket_quantity': int(parts[2]),
                        'ticket_type': parts[3],
                        'total_price': float(parts[4]),
                        'status': parts[5]
                    }
                    _bookings.append(booking)
                except Exception:
                    continue
    except Exception:
        _bookings = []


def load_participants():
    global _participants
    _participants = []
    try:
        with open('data/participants.txt', 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 7:
                    continue
                try:
                    participant = {
                        'participant_id': int(parts[0]),
                        'event_id': int(parts[1]),
                        'name': parts[2],
                        'email': parts[3],
                        'booking_id': parts[4],  # booking id string
                        'status': parts[5],
                        'registration_date': parts[6]
                    }
                    _participants.append(participant)
                except Exception:
                    continue
    except Exception:
        _participants = []


def load_schedules():
    global _schedules
    _schedules = []
    try:
        with open('data/schedules.txt', 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 7:
                    continue
                try:
                    schedule = {
                        'schedule_id': int(parts[0]),
                        'event_id': int(parts[1]),
                        'session_name': parts[2],
                        'start_datetime': parts[3],  # string format: YYYY-MM-DD HH:mm
                        'duration_minutes': int(parts[4]),
                        'speaker_name': parts[5],
                        'session_room': parts[6]
                    }
                    _schedules.append(schedule)
                except Exception:
                    continue
    except Exception:
        _schedules = []


# Load all data at app startup
load_events()
load_venues()
load_tickets()
load_bookings()
load_participants()
load_schedules()

# Helper: find event by id

def find_event(event_id):
    for e in _events:
        if e['event_id'] == event_id:
            return e
    return None

# Helper: find ticket by event_id and ticket_type

def find_ticket(event_id, ticket_type):
    for t in _tickets:
        if t['event_id'] == event_id and t['ticket_type'] == ticket_type:
            return t
    return None

# Helper: find participant by participant_id

def find_participant(participant_id):
    for p in _participants:
        if p['participant_id'] == participant_id:
            return p
    return None

# Helper: find venue by id

def find_venue(venue_id):
    for v in _venues:
        if v['venue_id'] == venue_id:
            return v
    return None

# Helper: parse date (YYYY-MM-DD) safely

def parse_date(date_str):
    try:
        return datetime.strptime(date_str, '%Y-%m-%d')
    except Exception:
        return None


# Route: root redirects to dashboard
@app.route('/')
def dashboard_redirect():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    # As dashboard page includes upcoming events and featured events block
    # We will consider featured events as those with category_id 1 for example
    # Upcoming events = events sorted by event_id ascending (no datetime data given)
    # We'll interpret max_tickets availability as part of info

    featured_events = [event for event in _events if event['category_id'] == 1]
    upcoming_events = sorted(_events, key=lambda e: e['event_id'])

    # Tickets info summary: total tickets max and booked (based on bookings quantity)
    total_max_tickets = sum(event['max_tickets'] for event in _events)
    total_booked_tickets = 0
    for booking in _bookings:
        # Sum all ticket_quantity from all bookings
        total_booked_tickets += booking['ticket_quantity']

    tickets_info = {
        'total_max_tickets': total_max_tickets,
        'total_booked_tickets': total_booked_tickets,
        'tickets_remaining': max(total_max_tickets - total_booked_tickets, 0)
    }

    return render_template('dashboard.html',
                           featured_events=featured_events,
                           upcoming_events=upcoming_events,
                           tickets_info=tickets_info)


@app.route('/events')
def events():
    # GET Query parameters: search-location (text), category-filter (int as str)
    search_location = request.args.get('search-location', '').strip().lower()
    category_filter_raw = request.args.get('category-filter', '').strip()

    filtered_events = _events

    if search_location:
        filtered_events = [e for e in filtered_events if search_location in e['location'].lower()]

    if category_filter_raw.isdigit():
        category_filter = int(category_filter_raw)
        filtered_events = [e for e in filtered_events if e['category_id'] == category_filter]

    return render_template('events.html', events=filtered_events, search_location=search_location, category_filter=category_filter_raw)


@app.route('/events/<int:event_id>', methods=['GET', 'POST'])
def event_details(event_id):
    event = find_event(event_id)
    if event is None:
        return "Event Not Found", 404

    if request.method == 'POST':
        # Book ticket functionality
        # Expecting form with ticket_type and quantity
        ticket_type = request.form.get('ticket_type', '').strip()
        quantity_raw = request.form.get('quantity', '').strip()

        if not ticket_type or not quantity_raw.isdigit():
            return render_template('event_details.html', event=event, error='Invalid ticket type or quantity.')

        quantity = int(quantity_raw)
        ticket = find_ticket(event_id, ticket_type)
        if ticket is None:
            return render_template('event_details.html', event=event, error='Ticket type not found.')
        if quantity < ticket['min_purchase']:
            return render_template('event_details.html', event=event, error=f'Minimum purchase is {ticket["min_purchase"]} tickets.')
        if quantity > ticket['quantity_available']:
            return render_template('event_details.html', event=event, error='Not enough tickets available.')

        # Deduct ticket quantity
        ticket['quantity_available'] -= quantity

        total_price = ticket['price'] * quantity

        # Create booking record
        booking = {
            'participant_name': '',  # Empty participant by default for event_details
            'booking_date': datetime.now().strftime('%Y-%m-%d'),
            'ticket_quantity': quantity,
            'ticket_type': ticket_type,
            'total_price': total_price,
            'status': 'Confirmed'
        }
        _bookings.append(booking)

        success_msg = f'Booked {quantity} ticket(s) for {ticket_type} at total price ${total_price:.2f}'
        return render_template('event_details.html', event=event, success=success_msg)

    # GET request
    return render_template('event_details.html', event=event)


@app.route('/tickets', methods=['GET', 'POST'])
def tickets():
    if request.method == 'POST':
        # POST: book tickets with form fields: event_id, ticket_type, quantity
        event_id_raw = request.form.get('event_id', '').strip()
        ticket_type = request.form.get('ticket_type', '').strip()
        quantity_raw = request.form.get('quantity', '').strip()

        if not event_id_raw.isdigit() or not ticket_type or not quantity_raw.isdigit():
            return render_template('tickets.html', error='Invalid booking data.', tickets=_tickets)
        event_id = int(event_id_raw)
        quantity = int(quantity_raw)

        event = find_event(event_id)
        if event is None:
            return render_template('tickets.html', error='Event not found.', tickets=_tickets)

        ticket = find_ticket(event_id, ticket_type)
        if ticket is None:
            return render_template('tickets.html', error='Ticket type not found for event.', tickets=_tickets)

        if quantity < ticket['min_purchase']:
            return render_template('tickets.html', error=f'Minimum purchase is {ticket["min_purchase"]} tickets.', tickets=_tickets)

        if quantity > ticket['quantity_available']:
            return render_template('tickets.html', error='Not enough tickets available.', tickets=_tickets)

        # Deduct quantity
        ticket['quantity_available'] -= quantity

        total_price = ticket['price'] * quantity

        # Add booking with participant_name empty
        booking = {
            'participant_name': '',
            'booking_date': datetime.now().strftime('%Y-%m-%d'),
            'ticket_quantity': quantity,
            'ticket_type': ticket_type,
            'total_price': total_price,
            'status': 'Confirmed'
        }
        _bookings.append(booking)

        confirmation_details = {
            'event': event,
            'ticket_type': ticket_type,
            'quantity': quantity,
            'total_price': total_price
        }

        return render_template('tickets.html', tickets=_tickets, confirmation_details=confirmation_details)

    # GET request
    return render_template('tickets.html', tickets=_tickets)


@app.route('/participants', methods=['GET', 'POST'])
def participants():
    # Filtering criteria
    search_participant = request.args.get('search-participant-input', '').strip().lower() if request.method == 'GET' else request.form.get('search-participant-input', '').strip().lower()
    status_filter = request.args.get('participant-status-filter', '').strip() if request.method == 'GET' else request.form.get('participant-status-filter', '').strip()
    filtered_participants = _participants

    if search_participant:
        filtered_participants = [p for p in filtered_participants if search_participant in p['name'].lower() or search_participant in p['email'].lower()]

    if status_filter:
        filtered_participants = [p for p in filtered_participants if p['status'] == status_filter]

    if request.method == 'POST':
        # Add new participant
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        event_id_raw = request.form.get('event_id', '').strip()
        booking_id = request.form.get('booking_id', '').strip()
        status = request.form.get('status', '').strip()
        registration_date = datetime.now().strftime('%Y-%m-%d')

        if not name or not email or not event_id_raw.isdigit() or not booking_id or not status:
            return render_template('participants.html', participants=filtered_participants, 
                                   error='Invalid participant data.',
                                   search_participant_input=search_participant,
                                   participant_status_filter=status_filter)

        event_id = int(event_id_raw)

        max_participant_id = max((p['participant_id'] for p in _participants), default=0)
        new_participant = {
            'participant_id': max_participant_id + 1,
            'event_id': event_id,
            'name': name,
            'email': email,
            'booking_id': booking_id,
            'status': status,
            'registration_date': registration_date
        }
        _participants.append(new_participant)

        # Reload filtered participants after adding new
        filtered_participants = _participants

        # Apply filters again
        if search_participant:
            filtered_participants = [p for p in filtered_participants if search_participant in p['name'].lower() or search_participant in p['email'].lower()]

        if status_filter:
            filtered_participants = [p for p in filtered_participants if p['status'] == status_filter]

        return render_template('participants.html', participants=filtered_participants,
                               success='Participant added successfully.',
                               search_participant_input=search_participant,
                               participant_status_filter=status_filter)

    # GET request
    return render_template('participants.html', participants=filtered_participants,
                           search_participant_input=search_participant,
                           participant_status_filter=status_filter)


@app.route('/venues')
def venues():
    search_venue_location = request.args.get('search-venue-location', '').strip().lower()
    venue_type_filter = request.args.get('venue-type-filter', '').strip()

    filtered_venues = _venues

    if search_venue_location:
        filtered_venues = [v for v in filtered_venues if search_venue_location in v['location'].lower() or search_venue_location in v['name'].lower()]

    # venue_type_filter - unclear field; assuming filtering by amenities containing this type
    if venue_type_filter:
        filtered_venues = [v for v in filtered_venues if any(venue_type_filter.lower() == amen.lower() for amen in v['amenities'])]

    return render_template('venues.html', venues=filtered_venues,
                           search_venue_location=search_venue_location,
                           venue_type_filter=venue_type_filter)


@app.route('/schedules')
def schedules():
    schedule_date_filter = request.args.get('schedule-date-filter', '').strip()
    schedule_event_filter_raw = request.args.get('schedule-event-filter', '').strip()

    filtered_schedules = _schedules

    if schedule_date_filter:
        dt_filter = parse_date(schedule_date_filter)
        if dt_filter is not None:
            filtered_schedules = [s for s in filtered_schedules if s['start_datetime'].startswith(schedule_date_filter)]

    if schedule_event_filter_raw.isdigit():
        event_filter = int(schedule_event_filter_raw)
        filtered_schedules = [s for s in filtered_schedules if s['event_id'] == event_filter]

    # Pass list of events for filter dropdown
    return render_template('schedules.html', schedules=filtered_schedules, events=_events,
                           schedule_date_filter=schedule_date_filter,
                           schedule_event_filter=schedule_event_filter_raw)


@app.route('/bookings', methods=['GET', 'POST'])
def bookings():
    search_booking_input = request.args.get('booking-search-input', '').strip().lower() if request.method == 'GET' else request.form.get('booking-search-input', '').strip().lower()

    filtered_bookings = _bookings

    if search_booking_input:
        filtered_bookings = [b for b in filtered_bookings if search_booking_input in b['participant_name'].lower() or search_booking_input in b['ticket_type'].lower() or search_booking_input in b['status'].lower()]

    if request.method == 'POST':
        # Cancel booking: expecting booking id info? As bookings.txt has no explicit id, use index as id for cancel
        cancel_id_raw = request.form.get('cancel_booking_id', '').strip()
        if cancel_id_raw.isdigit():
            cancel_id = int(cancel_id_raw)
            if 0 <= cancel_id < len(_bookings):
                _bookings[cancel_id]['status'] = 'Cancelled'

    return render_template('bookings.html', bookings=filtered_bookings, booking_search_input=search_booking_input)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
