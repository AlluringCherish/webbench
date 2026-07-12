from flask import Flask, render_template, redirect, url_for, request
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

# Data file paths
EVENTS_FILE = 'data/events.txt'
VENUES_FILE = 'data/venues.txt'
TICKETS_FILE = 'data/tickets.txt'
BOOKINGS_FILE = 'data/bookings.txt'
PARTICIPANTS_FILE = 'data/participants.txt'
SCHEDULES_FILE = 'data/schedules.txt'

# Fixed constants
EVENT_CATEGORIES = ["Conference", "Concert", "Sports", "Workshop", "Social"]
PARTICIPANT_STATUSES = ["Registered", "Confirmed", "Attended"]

# Helper functions for loading data files

def load_events():
    events = []
    if not os.path.exists(EVENTS_FILE):
        return events
    with open(EVENTS_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 9:
                continue
            try:
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
                continue
    return events


def load_venues():
    venues = []
    if not os.path.exists(VENUES_FILE):
        return venues
    with open(VENUES_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 6:
                continue
            try:
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
                continue
    return venues


def load_tickets():
    tickets = []
    if not os.path.exists(TICKETS_FILE):
        return tickets
    with open(TICKETS_FILE, 'r', encoding='utf-8') as f:
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
                    'available_count': int(parts[4]),
                    'sold_count': int(parts[5])
                }
                tickets.append(ticket)
            except Exception:
                continue
    return tickets


def load_bookings():
    bookings = []
    if not os.path.exists(BOOKINGS_FILE):
        return bookings
    with open(BOOKINGS_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 8:
                continue
            try:
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
                continue
    return bookings


def load_participants():
    participants = []
    if not os.path.exists(PARTICIPANTS_FILE):
        return participants
    with open(PARTICIPANTS_FILE, 'r', encoding='utf-8') as f:
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
                    'booking_id': int(parts[4]),
                    'status': parts[5],
                    'registration_date': parts[6]
                }
                participants.append(participant)
            except Exception:
                continue
    return participants


def load_schedules():
    schedules = []
    if not os.path.exists(SCHEDULES_FILE):
        return schedules
    with open(SCHEDULES_FILE, 'r', encoding='utf-8') as f:
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
                    'session_title': parts[2],
                    'session_time': parts[3],
                    'duration_minutes': int(parts[4]),
                    'speaker': parts[5],
                    'venue_id': int(parts[6])
                }
                schedules.append(schedule)
            except Exception:
                continue
    return schedules


# Save updated tickets data
# Overwrites the tickets.txt file with the current tickets list

def save_tickets(tickets):
    try:
        with open(TICKETS_FILE, 'w', encoding='utf-8') as f:
            for t in tickets:
                row = f"{t['ticket_id']}|{t['event_id']}|{t['ticket_type']}|{t['price']}|{t['available_count']}|{t['sold_count']}\n"
                f.write(row)
        return True
    except Exception:
        return False

# Save updated bookings data
# Overwrites the bookings.txt file with current bookings list

def save_bookings(bookings):
    try:
        with open(BOOKINGS_FILE, 'w', encoding='utf-8') as f:
            for b in bookings:
                row = f"{b['booking_id']}|{b['event_id']}|{b['customer_name']}|{b['booking_date']}|{b['ticket_count']}|{b['ticket_type']}|{b['total_amount']}|{b['status']}\n"
                f.write(row)
        return True
    except Exception:
        return False


# Route Implementations

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    events = load_events()
    # Featured events: Let's pick upcoming events sorted by date ascending, limit 5
    # We'll sort by date then time
    def event_sort_key(e):
        try:
            dt = datetime.strptime(e['date'] + ' ' + e['time'], '%Y-%m-%d %H:%M')
        except Exception:
            dt = datetime.max
        return dt

    upcoming_events = sorted(events, key=event_sort_key)[:5]
    featured_events = []
    for e in upcoming_events:
        featured_events.append({
            'event_id': e['event_id'],
            'event_name': e['event_name'],
            'date': e['date'],
            'location': e['location'],
            'category': e['category']
        })
    return render_template('dashboard.html', featured_events=featured_events)


@app.route('/events')
def list_events():
    events = load_events()
    return render_template('events.html', events=events, categories=EVENT_CATEGORIES)


@app.route('/event/<int:event_id>')
def event_details(event_id):
    events = load_events()
    event = None
    for e in events:
        if e['event_id'] == event_id:
            event = e
            break
    if not event:
        return "Event not found", 404
    return render_template('event_details.html', event=event)


@app.route('/book_ticket', methods=['GET'])
def book_ticket_page():
    events = load_events()
    return render_template('ticket_booking.html', events=events)


@app.route('/book_ticket', methods=['POST'])
def submit_ticket_booking():
    events = load_events()
    tickets = load_tickets()
    bookings = load_bookings()

    # Read form data
    event_id_str = request.form.get('event_id')
    customer_name = request.form.get('customer_name', '').strip()  # Not specified but needed
    ticket_count_str = request.form.get('ticket_count')
    ticket_type = request.form.get('ticket_type')

    # Validate required fields
    if not event_id_str or not ticket_count_str or not ticket_type or not customer_name:
        # Re-render with no confirmation if missing
        return render_template('ticket_booking.html', events=events)

    try:
        event_id = int(event_id_str)
        ticket_count = int(ticket_count_str)
    except ValueError:
        return render_template('ticket_booking.html', events=events)

    # Find the event for event name
    event = next((e for e in events if e['event_id']==event_id), None)
    if not event:
        return render_template('ticket_booking.html', events=events)

    # Find the ticket info for matching event and type
    ticket = next((t for t in tickets if t['event_id']==event_id and t['ticket_type']==ticket_type), None)
    if not ticket:
        # Ticket type for event not found
        return render_template('ticket_booking.html', events=events)

    # Check availability
    if ticket_count <= 0 or ticket_count > ticket['available_count']:
        # Not enough tickets
        return render_template('ticket_booking.html', events=events)

    # Create new booking_id
    max_booking_id = max([b['booking_id'] for b in bookings], default=0)
    new_booking_id = max_booking_id + 1

    # Calculate total amount
    total_amount = round(ticket['price'] * ticket_count, 2)

    # Create booking entry
    booking_date = datetime.now().strftime('%Y-%m-%d')
    new_booking = {
        'booking_id': new_booking_id,
        'event_id': event_id,
        'customer_name': customer_name,
        'booking_date': booking_date,
        'ticket_count': ticket_count,
        'ticket_type': ticket_type,
        'total_amount': total_amount,
        'status': 'Confirmed'
    }
    bookings.append(new_booking)

    # Update ticket available and sold counts
    ticket['available_count'] -= ticket_count
    ticket['sold_count'] += ticket_count

    # Save updated tickets and bookings
    save_tickets(tickets)
    save_bookings(bookings)

    booking_confirmation = {
        'booking_id': new_booking_id,
        'event_name': event['event_name'],
        'ticket_count': ticket_count,
        'ticket_type': ticket_type,
        'total_amount': total_amount,
        'status': 'Confirmed'
    }

    return render_template('ticket_booking.html', events=events, booking_confirmation=booking_confirmation)


@app.route('/participants')
def participants_management():
    participants = load_participants()
    return render_template('participants.html', participants=participants, statuses=PARTICIPANT_STATUSES)


@app.route('/add_participant', methods=['POST'])
def add_participant():
    participants = load_participants()

    # Extract form data
    try:
        event_id = int(request.form.get('event_id', ''))
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        booking_id = int(request.form.get('booking_id', ''))
        status = request.form.get('status', '').strip()
    except Exception:
        # Invalid or missing data
        return redirect(url_for('participants_management'))

    # Validate
    if not name or not email or status not in PARTICIPANT_STATUSES:
        return redirect(url_for('participants_management'))

    # Find max participant_id
    max_pid = max([p['participant_id'] for p in participants], default=0)
    registration_date = datetime.now().strftime('%Y-%m-%d')

    new_participant = {
        'participant_id': max_pid + 1,
        'event_id': event_id,
        'name': name,
        'email': email,
        'booking_id': booking_id,
        'status': status,
        'registration_date': registration_date
    }
    participants.append(new_participant)

    # Save back participants file
    try:
        with open(PARTICIPANTS_FILE, 'w', encoding='utf-8') as f:
            for p in participants:
                row = f"{p['participant_id']}|{p['event_id']}|{p['name']}|{p['email']}|{p['booking_id']}|{p['status']}|{p['registration_date']}\n"
                f.write(row)
    except Exception:
        pass

    return redirect(url_for('participants_management'))


@app.route('/venues')
def venues_page():
    venues = load_venues()
    return render_template('venues.html', venues=venues)


@app.route('/event_schedules')
def event_schedules():
    schedules = load_schedules()
    events = load_events()
    return render_template('schedules.html', schedules=schedules, events=events)


@app.route('/bookings')
def bookings_summary():
    bookings = load_bookings()
    events = load_events()
    events_map = {e['event_id']: e['event_name'] for e in events}
    return render_template('bookings.html', bookings=bookings, events_map=events_map)


@app.route('/cancel_booking/<int:booking_id>', methods=['POST'])
def cancel_booking(booking_id):
    bookings = load_bookings()
    tickets = load_tickets()

    # Find booking by id
    booking = None
    for b in bookings:
        if b['booking_id'] == booking_id:
            booking = b
            break
    if not booking:
        return redirect(url_for('bookings_summary'))

    # Only if status is Confirmed or Pending can we cancel
    if booking['status'] not in ['Confirmed', 'Pending']:
        return redirect(url_for('bookings_summary'))

    # Set status to Cancelled
    booking['status'] = 'Cancelled'

    # Return tickets availability back
    for t in tickets:
        if t['event_id'] == booking['event_id'] and t['ticket_type'] == booking['ticket_type']:
            t['available_count'] += booking['ticket_count']
            t['sold_count'] -= booking['ticket_count']
            break

    save_bookings(bookings)
    save_tickets(tickets)

    return redirect(url_for('bookings_summary'))


if __name__ == '__main__':
    app.run(debug=True, port=5000)
