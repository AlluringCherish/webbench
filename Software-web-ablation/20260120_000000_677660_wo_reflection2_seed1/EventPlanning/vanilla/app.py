from flask import Flask, render_template, redirect, url_for, request
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'


# Helper functions to load data from files

def load_events():
    events = []
    path = os.path.join(DATA_DIR, 'events.txt')
    if not os.path.exists(path):
        return events
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) < 9:
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
                'capacity': int(parts[8]),
            }
            events.append(event)
    return events


def load_venues():
    venues = []
    path = os.path.join(DATA_DIR, 'venues.txt')
    if not os.path.exists(path):
        return venues
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) < 6:
                continue
            venue = {
                'venue_id': int(parts[0]),
                'venue_name': parts[1],
                'location': parts[2],
                'capacity': int(parts[3]),
                'amenities': parts[4],
                'contact': parts[5],
            }
            venues.append(venue)
    return venues


def load_tickets():
    tickets = []
    path = os.path.join(DATA_DIR, 'tickets.txt')
    if not os.path.exists(path):
        return tickets
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) < 6:
                continue
            ticket = {
                'ticket_id': int(parts[0]),
                'event_id': int(parts[1]),
                'ticket_type': parts[2],
                'price': float(parts[3]),
                'available_count': int(parts[4]),
                'sold_count': int(parts[5]),
            }
            tickets.append(ticket)
    return tickets


def load_bookings():
    bookings = []
    path = os.path.join(DATA_DIR, 'bookings.txt')
    if not os.path.exists(path):
        return bookings
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) < 8:
                continue
            booking = {
                'booking_id': int(parts[0]),
                'event_id': int(parts[1]),
                'customer_name': parts[2],
                'booking_date': parts[3],
                'ticket_count': int(parts[4]),
                'ticket_type': parts[5],
                'total_amount': float(parts[6]),
                'status': parts[7],
            }
            bookings.append(booking)
    return bookings


def load_participants():
    participants = []
    path = os.path.join(DATA_DIR, 'participants.txt')
    if not os.path.exists(path):
        return participants
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) < 7:
                continue
            participant = {
                'participant_id': int(parts[0]),
                'event_id': int(parts[1]),
                'name': parts[2],
                'email': parts[3],
                'booking_id': int(parts[4]),
                'status': parts[5],
                'registration_date': parts[6],
            }
            participants.append(participant)
    return participants


def load_schedules():
    schedules = []
    path = os.path.join(DATA_DIR, 'schedules.txt')
    if not os.path.exists(path):
        return schedules
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) < 7:
                continue
            schedule = {
                'schedule_id': int(parts[0]),
                'event_id': int(parts[1]),
                'session_title': parts[2],
                'session_time': parts[3],
                'duration_minutes': int(parts[4]),
                'speaker': parts[5],
                'venue_id': int(parts[6]),
            }
            schedules.append(schedule)
    return schedules


# Helper function: save bookings back to file

def save_bookings(bookings):
    path = os.path.join(DATA_DIR, 'bookings.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for b in bookings:
            line = '{}|{}|{}|{}|{}|{}|{}|{}'.format(
                b['booking_id'], b['event_id'], b['customer_name'], b['booking_date'],
                b['ticket_count'], b['ticket_type'], b['total_amount'], b['status'])
            f.write(line + '\n')


# Helper function: save participants

def save_participants(participants):
    path = os.path.join(DATA_DIR, 'participants.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for p in participants:
            line = '{}|{}|{}|{}|{}|{}|{}'.format(
                p['participant_id'], p['event_id'], p['name'], p['email'],
                p['booking_id'], p['status'], p['registration_date'])
            f.write(line + '\n')


# Helper function: save tickets

def save_tickets(tickets):
    path = os.path.join(DATA_DIR, 'tickets.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for t in tickets:
            line = '{}|{}|{}|{:.2f}|{}|{}'.format(
                t['ticket_id'], t['event_id'], t['ticket_type'], t['price'],
                t['available_count'], t['sold_count'])
            f.write(line + '\n')


# Root redirect
@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))


# Dashboard route
@app.route('/dashboard')
def dashboard():
    events = load_events()
    # For featured_events, pick first 5 upcoming events sorted by date
    today = datetime.now().date()
    upcoming = [e for e in events if datetime.strptime(e['date'], '%Y-%m-%d').date() >= today]
    sorted_events = sorted(upcoming, key=lambda x: x['date'])
    featured_events = []
    for e in sorted_events[:5]:
        featured_events.append({
            'event_id': e['event_id'],
            'event_name': e['event_name'],
            'date': e['date'],
            'location': e['location'],
        })
    return render_template('dashboard.html', featured_events=featured_events)


# Events listing
@app.route('/events')
def events_listing():
    events = load_events()
    categories = ["Conference", "Concert", "Sports", "Workshop", "Social"]
    return render_template('events.html', events=events, categories=categories)


# Event details
@app.route('/event/<int:event_id>')
def event_details(event_id):
    events = load_events()
    event = next((e for e in events if e['event_id'] == event_id), None)
    if event is None:
        return "Event not found", 404
    event_detail = {
        'event_id': event['event_id'],
        'event_name': event['event_name'],
        'date': event['date'],
        'time': event['time'],
        'location': event['location'],
        'description': event['description'],
    }
    return render_template('event_details.html', event=event_detail)


# Ticket booking GET and POST
@app.route('/book_ticket', methods=['GET', 'POST'])
def ticket_booking():
    if request.method == 'GET':
        events = load_events()
        events_list = [{'event_id': e['event_id'], 'event_name': e['event_name']} for e in events]
        return render_template('ticket_booking.html', events=events_list)

    # POST process booking
    else:
        events = load_events()
        tickets = load_tickets()
        bookings = load_bookings()
        form = request.form
        try:
            event_id = int(form.get('event_id', ''))
            customer_name = form.get('customer_name', '').strip()
            ticket_count = int(form.get('ticket_count', ''))
            ticket_type = form.get('ticket_type', '')

            if not customer_name:
                return render_template('ticket_booking.html', error="Customer name is required.")

            if ticket_count <= 0:
                return render_template('ticket_booking.html', error="Ticket count must be positive.")

            event = next((e for e in events if e['event_id'] == event_id), None)
            if not event:
                return render_template('ticket_booking.html', error="Selected event is invalid.")

            ticket = next((t for t in tickets if t['event_id']==event_id and t['ticket_type']==ticket_type), None)
            if not ticket:
                return render_template('ticket_booking.html', error="Ticket type not available for selected event.")

            if ticket['available_count'] < ticket_count:
                return render_template('ticket_booking.html', error="Not enough tickets available.")

            # Calculate total
            total_amount = ticket_count * ticket['price']
            # Generate new booking_id
            max_booking_id = max((b['booking_id'] for b in bookings), default=0)
            new_booking_id = max_booking_id + 1
            booking_date = datetime.now().strftime('%Y-%m-%d')

            # Create booking dict
            new_booking = {
                'booking_id': new_booking_id,
                'event_id': event_id,
                'customer_name': customer_name,
                'booking_date': booking_date,
                'ticket_count': ticket_count,
                'ticket_type': ticket_type,
                'total_amount': total_amount,
                'status': 'Pending',
            }

            bookings.append(new_booking)

            # Update ticket availability
            ticket['available_count'] -= ticket_count
            ticket['sold_count'] += ticket_count

            # Save bookings and tickets
            save_bookings(bookings)
            save_tickets(tickets)

            confirmation = {
                'booking_id': new_booking_id,
                'event_name': event['event_name'],
                'customer_name': customer_name,
                'ticket_count': ticket_count,
                'ticket_type': ticket_type,
                'total_amount': total_amount,
                'booking_date': booking_date,
                'status': 'Pending',
            }

            return render_template('ticket_booking.html', confirmation=confirmation)

        except Exception as e:
            return render_template('ticket_booking.html', error="Failed to process booking. " + str(e))


# Submit ticket booking form POST route
@app.route('/book_ticket/submit', methods=['POST'])
def submit_ticket_booking():
    # This endpoint expects form POST, will process booking same as above
    # We can delegate to ticket_booking post if wanted but routes are separate
    form = request.form
    # To avoid code duplication, we simulate POST call to ticket_booking
    with app.test_request_context('/book_ticket', method='POST', data=form):
        return ticket_booking()


# Participants management GET and POST
@app.route('/participants', methods=['GET', 'POST'])
def participants_management():
    participants = load_participants()
    events = load_events()
    event_dict = {e['event_id']: e['event_name'] for e in events}
    statuses = ["Registered", "Confirmed", "Attended"]

    if request.method == 'GET':
        # Enrich participants with event_name
        enriched = []
        for p in participants:
            event_name = event_dict.get(p['event_id'], "Unknown")
            part = {
                'participant_id': p['participant_id'],
                'name': p['name'],
                'email': p['email'],
                'event_name': event_name,
                'status': p['status'],
            }
            enriched.append(part)
        return render_template('participants.html', participants=enriched, statuses=statuses)

    # POST add new participant
    else:
        form = request.form
        try:
            name = form.get('name', '').strip()
            email = form.get('email', '').strip()
            event_id = int(form.get('event_id', ''))
            status = form.get('status', 'Registered')
            
            if not name or not email:
                # Usually redirect with error or render with error
                # Here just render with error on same page
                enriched = []
                for p in participants:
                    event_name = event_dict.get(p['event_id'], "Unknown")
                    part = {
                        'participant_id': p['participant_id'],
                        'name': p['name'],
                        'email': p['email'],
                        'event_name': event_name,
                        'status': p['status'],
                    }
                    enriched.append(part)
                return render_template('participants.html', participants=enriched, statuses=statuses, error="Name and Email required.")

            # Get max participant_id
            max_pid = max((p['participant_id'] for p in participants), default=0)
            new_pid = max_pid + 1

            # Try to find a booking for event and participant - we just assign booking_id 0 if none
            booking_id = 0

            # registration_date is today
            registration_date = datetime.now().strftime('%Y-%m-%d')

            new_participant = {
                'participant_id': new_pid,
                'event_id': event_id,
                'name': name,
                'email': email,
                'booking_id': booking_id,
                'status': status,
                'registration_date': registration_date
            }
            participants.append(new_participant)
            save_participants(participants)

            return redirect(url_for('participants_management'))

        except Exception as e:
            return render_template('participants.html', participants=participants, statuses=statuses, error="Failed to add participant. " + str(e))


# Venues
@app.route('/venues')
def venues():
    venues = load_venues()
    capacity_filters = ["Small", "Medium", "Large"]
    return render_template('venues.html', venues=venues, capacity_filters=capacity_filters)


# Venue details
@app.route('/venue/<int:venue_id>')
def venue_details(venue_id):
    venues = load_venues()
    venue = next((v for v in venues if v['venue_id'] == venue_id), None)
    if not venue:
        return "Venue not found", 404
    # We provide all venue details including contact
    return render_template('venue_details.html', venue=venue)


# Event schedules
@app.route('/schedules')
def event_schedules():
    schedules = load_schedules()
    events = load_events()
    # Enrich schedules with event_name
    event_dict = {e['event_id']: e['event_name'] for e in events}
    enriched = []
    for s in schedules:
        en = event_dict.get(s['event_id'], "Unknown")
        ent = {
            'schedule_id': s['schedule_id'],
            'event_name': en,
            'session_title': s['session_title'],
            'session_time': s['session_time'],
            'duration_minutes': s['duration_minutes'],
            'speaker': s['speaker'],
        }
        enriched.append(ent)

    return render_template('schedules.html', schedules=enriched, events=events)


# Bookings summary
@app.route('/bookings')
def bookings_summary():
    bookings = load_bookings()
    events = load_events()
    event_dict = {e['event_id']: e['event_name'] for e in events}
    enriched = []
    for b in bookings:
        event_name = event_dict.get(b['event_id'], "Unknown")
        ent = {
            'booking_id': b['booking_id'],
            'event_name': event_name,
            'date': None,
            'ticket_count': b['ticket_count'],
            'status': b['status'],
        }
        # date extracted as booking_date or event date?
        # Specification says bookings has `date` (str), we interpret as event date
        event = next((e for e in events if e['event_id'] == b['event_id']), None)
        if event:
            ent['date'] = event['date']

        enriched.append(ent)

    return render_template('bookings.html', bookings=enriched)


# Cancel booking
@app.route('/booking/cancel/<int:booking_id>', methods=['POST'])
def cancel_booking(booking_id):
    bookings = load_bookings()
    booking = next((b for b in bookings if b['booking_id'] == booking_id), None)
    if not booking:
        return "Booking not found", 404

    # Update booking status to 'Cancelled'
    booking['status'] = 'Cancelled'

    # Possibly update tickets availability
    tickets = load_tickets()
    ticket = next((t for t in tickets if t['event_id'] == booking['event_id'] and t['ticket_type'] == booking['ticket_type']), None)
    if ticket:
        ticket['available_count'] += booking['ticket_count']
        ticket['sold_count'] = max(0, ticket['sold_count'] - booking['ticket_count'])

    save_bookings(bookings)
    save_tickets(tickets)

    return redirect(url_for('bookings_summary'))


if __name__ == '__main__':
    app.run(debug=True, port=5000)
