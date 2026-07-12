from flask import Flask, render_template, redirect, url_for, request
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

# Helper functions to load data from files

def load_events():
    events = []
    try:
        with open(os.path.join(DATA_DIR, 'events.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 9:
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
    try:
        with open(os.path.join(DATA_DIR, 'venues.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 6:
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
    try:
        with open(os.path.join(DATA_DIR, 'tickets.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 6:
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
    try:
        with open(os.path.join(DATA_DIR, 'bookings.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 8:
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
    try:
        with open(os.path.join(DATA_DIR, 'participants.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 7:
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
    try:
        with open(os.path.join(DATA_DIR, 'schedules.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 7:
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


# We do not write back to data files for persistence; booking will be simulated in memory for POST

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    events = load_events()
    # Define featured_events: a subset of events with keys: event_id, event_name, date, location
    featured_events = []
    for event in events[:5]:  # Example: first 5 events
        feat = {
            'event_id': event['event_id'],
            'event_name': event['event_name'],
            'date': event['date'],
            'location': event['location']
        }
        featured_events.append(feat)
    return render_template('dashboard.html', featured_events=featured_events)


@app.route('/events')
def events_listing():
    events = load_events()
    # add optional image_url key - not specified in data, so skipped
    categories = ["Conference", "Concert", "Sports", "Workshop", "Social"]
    return render_template('events.html', events=events, categories=categories)


@app.route('/event/<int:event_id>')
def event_details(event_id):
    events = load_events()
    event = next((e for e in events if e['event_id'] == event_id), None)
    if not event:
        return "Event not found", 404
    # event dict keys as required
    return render_template('event_details.html', event=event)


@app.route('/book_ticket', methods=['GET'])
def book_ticket_get():
    events = load_events()
    minimal_events = [{'event_id': e['event_id'], 'event_name': e['event_name']} for e in events]
    
    return render_template('ticket_booking.html', events=minimal_events)


@app.route('/book_ticket', methods=['POST'])
def book_ticket_post():
    # Get form data
    event_id = request.form.get('event_id')
    ticket_quantity = request.form.get('ticket_quantity')
    ticket_type = request.form.get('ticket_type')
    customer_name = request.form.get('customer_name', 'Anonymous')  # not specified but needed

    # Validate and convert
    try:
        event_id = int(event_id)
        ticket_quantity = int(ticket_quantity)
    except Exception:
        return "Invalid input", 400

    # Load tickets and find matching ticket
    tickets = load_tickets()
    ticket = None
    for t in tickets:
        if t['event_id'] == event_id and t['ticket_type'].lower() == ticket_type.lower():
            ticket = t
            break

    if not ticket:
        return "Ticket type not found for event", 404

    if ticket['available_count'] < ticket_quantity:
        return "Not enough tickets available", 400

    # Calculate total price
    total_price = ticket['price'] * ticket_quantity

    # Load existing bookings to generate new booking_id
    bookings = load_bookings()
    if bookings:
        max_booking_id = max(b['booking_id'] for b in bookings)
    else:
        max_booking_id = 0
    new_booking_id = max_booking_id + 1

    # Simulate saving booking (in real app, would write to file or DB)
    # Just return confirmation

    booking_confirmation = {
        'booking_id': new_booking_id,
        'event_id': event_id,
        'event_name': next((e['event_name'] for e in load_events() if e['event_id'] == event_id), 'Unknown'),
        'ticket_quantity': ticket_quantity,
        'ticket_type': ticket_type,
        'total_price': total_price,
        'status': 'Confirmed'
    }

    # Return the template with confirmation
    return render_template('ticket_booking.html', booking_confirmation=booking_confirmation)


@app.route('/participants')
def participants_management():
    participants = load_participants()
    events = load_events()

    # Attach event_name to each participant
    events_dict = {e['event_id']: e['event_name'] for e in events}

    participants_list = []
    for p in participants:
        participants_list.append({
            'participant_id': p['participant_id'],
            'name': p['name'],
            'email': p['email'],
            'event_name': events_dict.get(p['event_id'], 'Unknown'),
            'status': p['status']
        })

    return render_template('participants.html', participants=participants_list)


@app.route('/add_participant', methods=['POST'])
def add_participant_post():
    # Get form data for new participant
    name = request.form.get('name')
    email = request.form.get('email')
    event_id = request.form.get('event_id')
    booking_id = request.form.get('booking_id')
    status = request.form.get('status', 'Pending')
    registration_date = request.form.get('registration_date')

    # Validate event_id, booking_id and name, email, registration_date
    try:
        event_id = int(event_id)
        booking_id = int(booking_id) if booking_id else 0
    except Exception:
        return "Invalid input", 400

    # Since persistent data writing not required, just redirect
    # In real app, would append to participants.txt

    return redirect(url_for('participants_management'))


@app.route('/venues')
def venues_page():
    venues = load_venues()
    # Return venues with keys: venue_id, venue_name, location, capacity, amenities
    venues_list = []
    for v in venues:
        venues_list.append({
            'venue_id': v['venue_id'],
            'venue_name': v['venue_name'],
            'location': v['location'],
            'capacity': v['capacity'],
            'amenities': v['amenities']
        })
    return render_template('venues.html', venues=venues_list)


@app.route('/venue/<int:venue_id>')
def venue_details(venue_id):
    venues = load_venues()
    venue = next((v for v in venues if v['venue_id'] == venue_id), None)
    if not venue:
        return "Venue not found", 404
    # Keys as required plus contact
    return render_template('venue_details.html', venue=venue)


@app.route('/schedules')
def event_schedules():
    schedules = load_schedules()
    events = load_events()
    # Minimal events for filter dropdown
    minimal_events = [{'event_id': e['event_id'], 'event_name': e['event_name']} for e in events]

    return render_template('schedules.html', schedules=schedules, events=minimal_events)


@app.route('/bookings')
def bookings_summary():
    bookings = load_bookings()
    events = load_events()
    events_dict = {e['event_id']: e for e in events}

    bookings_list = []
    for b in bookings:
        event = events_dict.get(b['event_id'])
        bookings_list.append({
            'booking_id': b['booking_id'],
            'event_name': event['event_name'] if event else 'Unknown',
            'date': event['date'] if event else '',
            'ticket_count': b['ticket_count'],
            'status': b['status']
        })

    return render_template('bookings.html', bookings=bookings_list)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
