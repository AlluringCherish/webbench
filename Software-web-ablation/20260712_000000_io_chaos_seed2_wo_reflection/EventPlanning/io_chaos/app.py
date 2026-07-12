from flask import Flask, render_template, redirect, url_for, request
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Helper functions to load and parse data files

def load_events():
    events = []
    path = os.path.join(DATA_DIR, 'events.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 9:
                    continue
                event = {
                    'event_id': int(parts[0]),
                    'event_name': parts[1],
                    'category': parts[2],
                    'date': parts[3],
                    'time': parts[4],
                    'location': parts[5],
                    'description': parts[6],
                    'venue_id': int(parts[7]),
                    'capacity': int(parts[8])
                }
                events.append(event)
    except Exception:
        pass
    return events


def load_venues():
    venues = []
    path = os.path.join(DATA_DIR, 'venues.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 6:
                    continue
                venue = {
                    'venue_id': int(parts[0]),
                    'venue_name': parts[1],
                    'location': parts[2],
                    'capacity': int(parts[3]),
                    'amenities': parts[4],
                    'contact': parts[5]
                }
                venues.append(venue)
    except Exception:
        pass
    return venues


def load_tickets():
    tickets = []
    path = os.path.join(DATA_DIR, 'tickets.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 6:
                    continue
                ticket = {
                    'ticket_id': int(parts[0]),
                    'event_id': int(parts[1]),
                    'ticket_type': parts[2],
                    'price': float(parts[3]),
                    'available_count': int(parts[4]),
                    'sold_count': int(parts[5])
                }
                tickets.append(ticket)
    except Exception:
        pass
    return tickets


def load_bookings():
    bookings = []
    path = os.path.join(DATA_DIR, 'bookings.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 8:
                    continue
                booking = {
                    'booking_id': int(parts[0]),
                    'event_id': int(parts[1]),
                    'customer_name': parts[2],
                    'booking_date': parts[3],
                    'ticket_count': int(parts[4]),
                    'ticket_type': parts[5],
                    'total_amount': float(parts[6]),
                    'status': parts[7]
                }
                bookings.append(booking)
    except Exception:
        pass
    return bookings


def load_participants():
    participants = []
    path = os.path.join(DATA_DIR, 'participants.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 7:
                    continue
                participant = {
                    'participant_id': int(parts[0]),
                    'event_id': int(parts[1]),
                    'name': parts[2],
                    'email': parts[3],
                    'booking_id': int(parts[4]),
                    'status': parts[5],
                    'registration_date': parts[6]
                }
                participants.append(participant)
    except Exception:
        pass
    return participants


def load_schedules():
    schedules = []
    path = os.path.join(DATA_DIR, 'schedules.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 7:
                    continue
                schedule = {
                    'schedule_id': int(parts[0]),
                    'event_id': int(parts[1]),
                    'session_title': parts[2],
                    'session_time': parts[3],
                    'duration_minutes': int(parts[4]),
                    'speaker': parts[5],
                    'venue_id': int(parts[6])
                }
                schedules.append(schedule)
    except Exception:
        pass
    return schedules


# Utility to save bookings.txt after changes
# We'll create a helper to write bookings (not required for others from spec)
def save_bookings(bookings):
    path = os.path.join(DATA_DIR, 'bookings.txt')
    try:
        with open(path, 'w', encoding='utf-8') as f:
            for b in bookings:
                line = f"{b['booking_id']}|{b['event_id']}|{b['customer_name']}|{b['booking_date']}|{b['ticket_count']}|{b['ticket_type']}|{b['total_amount']:.2f}|{b['status']}\n"
                f.write(line)
    except Exception:
        pass


# Utility to save tickets.txt after updating ticket availability
# We must update available_count and sold_count
# According to spec: booking logic updates ticket availability and booking storage

def save_tickets(tickets):
    path = os.path.join(DATA_DIR, 'tickets.txt')
    try:
        with open(path, 'w', encoding='utf-8') as f:
            for t in tickets:
                line = f"{t['ticket_id']}|{t['event_id']}|{t['ticket_type']}|{t['price']:.2f}|{t['available_count']}|{t['sold_count']}\n"
                f.write(line)
    except Exception:
        pass


@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard_page'))


@app.route('/dashboard')
def dashboard_page():
    events = load_events()
    # featured_events according to spec: list of dicts with event_id (int), event_name (str), date (str), location (str)
    # We can consider featured events as first 5 upcoming events sorted by date for demonstration
    try:
        sorted_events = sorted(events, key=lambda e: e['date'])
    except Exception:
        sorted_events = events
    featured_events = []
    for e in sorted_events[:5]:
        featured_events.append({
            'event_id': e['event_id'],
            'event_name': e['event_name'],
            'date': e['date'],
            'location': e['location']
        })
    return render_template('dashboard.html', featured_events=featured_events)


@app.route('/events', methods=['GET', 'POST'])
def events_listing_page():
    events = load_events()

    if request.method == 'POST':
        # Filtering logic based on search and category
        search_term = request.form.get('search_term', '').lower()
        category_filter = request.form.get('category_filter', '')
        filtered_events = []
        for e in events:
            match_search = (search_term in e['event_name'].lower()
                            or search_term in e['location'].lower()
                            or search_term in e['date'])
            match_category = (category_filter == '' or e['category'] == category_filter)
            if match_search and match_category:
                filtered_events.append(e)
        events = filtered_events

    # GET method just show all events
    return render_template('events.html', events=events)


@app.route('/event/<int:event_id>')
def event_details_page(event_id):
    events = load_events()
    event = next((e for e in events if e['event_id'] == event_id), None)
    if not event:
        # Not found, redirect to events listing
        return redirect(url_for('events_listing_page'))
    return render_template('event_details.html', event=event)


@app.route('/book_ticket', methods=['GET', 'POST'])
def ticket_booking_page():
    events = load_events()
    selectable_events = [{'event_id': e['event_id'], 'event_name': e['event_name']} for e in events]

    if request.method == 'GET':
        return render_template('book_ticket.html', events=selectable_events)

    # POST handling booking
    event_id = request.form.get('event_id')
    customer_name = request.form.get('customer_name', '').strip()
    ticket_type = request.form.get('ticket_type')
    ticket_count_str = request.form.get('ticket_count')
    try:
        event_id = int(event_id)
        ticket_count = int(ticket_count_str)
    except Exception:
        # invalid entry
        booking_confirmation = {
            'booking_id': None,
            'event_name': '',
            'ticket_count': 0,
            'total_amount': 0.0,
            'status': 'Failed - Invalid input'
        }
        return render_template('book_ticket.html', booking_confirmation=booking_confirmation)

    # Load tickets and events
    tickets = load_tickets()
    events = load_events()
    event = next((e for e in events if e['event_id'] == event_id), None)
    if not event:
        booking_confirmation = {
            'booking_id': None,
            'event_name': '',
            'ticket_count': 0,
            'total_amount': 0.0,
            'status': 'Failed - Event not found'
        }
        return render_template('book_ticket.html', booking_confirmation=booking_confirmation)

    # Find ticket for event and ticket_type
    ticket = next((t for t in tickets if t['event_id'] == event_id and t['ticket_type'] == ticket_type), None)
    if not ticket:
        booking_confirmation = {
            'booking_id': None,
            'event_name': event['event_name'],
            'ticket_count': ticket_count,
            'total_amount': 0.0,
            'status': 'Failed - Ticket type not found'
        }
        return render_template('book_ticket.html', booking_confirmation=booking_confirmation)

    if ticket_count > ticket['available_count']:
        booking_confirmation = {
            'booking_id': None,
            'event_name': event['event_name'],
            'ticket_count': ticket_count,
            'total_amount': 0.0,
            'status': 'Failed - Not enough tickets available'
        }
        return render_template('book_ticket.html', booking_confirmation=booking_confirmation)

    # All good, create booking
    bookings = load_bookings()
    new_booking_id = 1 if not bookings else max(b['booking_id'] for b in bookings) + 1
    total_amount = ticket_count * ticket['price']
    booking_date = datetime.today().strftime('%Y-%m-%d')
    new_booking = {
        'booking_id': new_booking_id,
        'event_id': event_id,
        'customer_name': customer_name or 'Anonymous',
        'booking_date': booking_date,
        'ticket_count': ticket_count,
        'ticket_type': ticket_type,
        'total_amount': total_amount,
        'status': 'Confirmed'
    }
    bookings.append(new_booking)
    # Update tickets availability
    ticket['available_count'] -= ticket_count
    ticket['sold_count'] += ticket_count

    # Save updated data
    save_bookings(bookings)
    save_tickets(tickets)

    booking_confirmation = {
        'booking_id': new_booking_id,
        'event_name': event['event_name'],
        'ticket_count': ticket_count,
        'total_amount': total_amount,
        'status': 'Confirmed'
    }

    return render_template('book_ticket.html', booking_confirmation=booking_confirmation)


@app.route('/participants', methods=['GET'])
def participants_page():
    participants = load_participants()
    status_options = ['Registered', 'Confirmed', 'Attended']

    # Support filtering by status or searching by name/email
    search_term = request.args.get('search_term', '').lower()
    status_filter = request.args.get('status_filter', '')

    filtered_participants = []
    for p in participants:
        match_search = (search_term in p['name'].lower() or search_term in p['email'].lower()) if search_term else True
        match_status = (status_filter == '' or p['status'] == status_filter)
        if match_search and match_status:
            filtered_participants.append(p)

    return render_template('participants.html', participants=filtered_participants, status_options=status_options)


@app.route('/participants/add', methods=['POST'])
def add_participant():
    # Adding participant requires participant_id, event_id, name, email, booking_id, status, registration_date
    # We will parse from form
    try:
        participant_id = request.form.get('participant_id')
        event_id = request.form.get('event_id')
        name = request.form.get('name')
        email = request.form.get('email')
        booking_id = request.form.get('booking_id')
        status = request.form.get('status')
        registration_date = request.form.get('registration_date')

        # Validate required
        if not (participant_id and event_id and name and email and booking_id and status and registration_date):
            return redirect(url_for('participants_page'))

        participant_id = int(participant_id)
        event_id = int(event_id)
        booking_id = int(booking_id)

        participants = load_participants()
        # Check duplication of participant_id
        if any(p['participant_id'] == participant_id for p in participants):
            return redirect(url_for('participants_page'))

        new_participant = {
            'participant_id': participant_id,
            'event_id': event_id,
            'name': name,
            'email': email,
            'booking_id': booking_id,
            'status': status,
            'registration_date': registration_date
        }
        participants.append(new_participant)

        path = os.path.join(DATA_DIR, 'participants.txt')
        try:
            with open(path, 'w', encoding='utf-8') as f:
                for p in participants:
                    line = f"{p['participant_id']}|{p['event_id']}|{p['name']}|{p['email']}|{p['booking_id']}|{p['status']}|{p['registration_date']}\n"
                    f.write(line)
        except Exception:
            pass
    except Exception:
        pass
    return redirect(url_for('participants_page'))


@app.route('/venues', methods=['GET'])
def venues_page():
    venues = load_venues()

    # Support optional filtering by name/location search and capacity category
    search_term = request.args.get('search_term', '').lower()
    capacity_filter = request.args.get('capacity_filter', '')  # Small, Medium, Large

    filtered_venues = []
    for v in venues:
        match_search = (search_term in v['venue_name'].lower() or search_term in v['location'].lower()) if search_term else True
        if capacity_filter == 'Small':
            match_capacity = v['capacity'] < 500
        elif capacity_filter == 'Medium':
            match_capacity = 500 <= v['capacity'] < 2000
        elif capacity_filter == 'Large':
            match_capacity = v['capacity'] >= 2000
        else:
            match_capacity = True

        if match_search and match_capacity:
            filtered_venues.append(v)

    return render_template('venues.html', venues=filtered_venues)


@app.route('/event_schedules', methods=['GET'])
def event_schedules_page():
    schedules = load_schedules()
    events = load_events()

    # Filter by date and event if provided
    filter_date = request.args.get('filter_date', '')  # YYYY-MM-DD
    filter_event_id = request.args.get('filter_event_id', '')

    filtered_schedules = schedules

    if filter_date:
        filtered_schedules = [s for s in filtered_schedules if s['session_time'].startswith(filter_date)]

    if filter_event_id:
        try:
            filter_event_id_int = int(filter_event_id)
            filtered_schedules = [s for s in filtered_schedules if s['event_id'] == filter_event_id_int]
        except Exception:
            pass

    events_simple = [{'event_id': e['event_id'], 'event_name': e['event_name']} for e in events]

    return render_template('schedules.html', schedules=filtered_schedules, events=events_simple)


@app.route('/bookings', methods=['GET'])
def bookings_summary_page():
    bookings = load_bookings()
    events = load_events()

    # Enrich bookings with event_name
    event_map = {e['event_id']: e['event_name'] for e in events}
    bookings_enriched = []
    search_term = request.args.get('search_term', '').lower()

    for b in bookings:
        event_name = event_map.get(b['event_id'], '')
        if search_term:
            if search_term not in event_name.lower() and search_term not in str(b['booking_id']):
                continue
        b_copy = b.copy()
        b_copy['event_name'] = event_name
        bookings_enriched.append(b_copy)

    return render_template('bookings.html', bookings=bookings_enriched)


@app.route('/bookings/cancel/<int:booking_id>', methods=['POST'])
def cancel_booking(booking_id):
    bookings = load_bookings()
    updated = False
    for b in bookings:
        if b['booking_id'] == booking_id:
            if b['status'] != 'Cancelled':
                b['status'] = 'Cancelled'
                updated = True
            break

    if updated:
        save_bookings(bookings)

    return redirect(url_for('bookings_summary_page'))


if __name__ == '__main__':
    app.run(debug=True, port=5000)
