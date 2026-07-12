from flask import Flask, render_template, redirect, url_for, request
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

# Data files paths
DATA_PATH = 'data'
EVENTS_FILE = os.path.join(DATA_PATH, 'events.txt')
VENUES_FILE = os.path.join(DATA_PATH, 'venues.txt')
TICKETS_FILE = os.path.join(DATA_PATH, 'tickets.txt')
BOOKINGS_FILE = os.path.join(DATA_PATH, 'bookings.txt')
PARTICIPANTS_FILE = os.path.join(DATA_PATH, 'participants.txt')
SCHEDULES_FILE = os.path.join(DATA_PATH, 'schedules.txt')

# Helper functions to load data

def load_events():
    events = []
    try:
        with open(EVENTS_FILE, 'r') as f:
            for line in f:
                # Fields order and names: event_id|name|date|venue_id|description
                parts = line.strip().split('|')
                if len(parts) == 5:
                    event = {
                        'event_id': parts[0],
                        'name': parts[1],
                        'date': parts[2],
                        'venue_id': parts[3],
                        'description': parts[4]
                    }
                    events.append(event)
    except Exception:
        pass
    return events


def load_venues():
    venues = []
    try:
        with open(VENUES_FILE, 'r') as f:
            for line in f:
                # Fields order: venue_id|name|address|capacity
                parts = line.strip().split('|')
                if len(parts) == 4:
                    venue = {
                        'venue_id': parts[0],
                        'name': parts[1],
                        'address': parts[2],
                        'capacity': int(parts[3])
                    }
                    venues.append(venue)
    except Exception:
        pass
    return venues


def load_tickets():
    tickets = []
    try:
        with open(TICKETS_FILE, 'r') as f:
            for line in f:
                # Fields order: ticket_id|event_id|type|price|available
                parts = line.strip().split('|')
                if len(parts) == 5:
                    ticket = {
                        'ticket_id': parts[0],
                        'event_id': parts[1],
                        'type': parts[2],
                        'price': float(parts[3]),
                        'available': int(parts[4])
                    }
                    tickets.append(ticket)
    except Exception:
        pass
    return tickets


def load_bookings():
    bookings = []
    try:
        with open(BOOKINGS_FILE, 'r') as f:
            for line in f:
                # Fields order: booking_id|ticket_id|participant_id|quantity
                parts = line.strip().split('|')
                if len(parts) == 4:
                    booking = {
                        'booking_id': parts[0],
                        'ticket_id': parts[1],
                        'participant_id': parts[2],
                        'quantity': int(parts[3])
                    }
                    bookings.append(booking)
    except Exception:
        pass
    return bookings


def load_participants():
    participants = []
    try:
        with open(PARTICIPANTS_FILE, 'r') as f:
            for line in f:
                # Fields order: participant_id|name|email
                parts = line.strip().split('|')
                if len(parts) == 3:
                    participant = {
                        'participant_id': parts[0],
                        'name': parts[1],
                        'email': parts[2]
                    }
                    participants.append(participant)
    except Exception:
        pass
    return participants


def load_schedules():
    schedules = []
    try:
        with open(SCHEDULES_FILE, 'r') as f:
            for line in f:
                # Fields order: schedule_id|event_id|time|activity
                parts = line.strip().split('|')
                if len(parts) == 4:
                    schedule = {
                        'schedule_id': parts[0],
                        'event_id': parts[1],
                        'time': parts[2],
                        'activity': parts[3]
                    }
                    schedules.append(schedule)
    except Exception:
        pass
    return schedules

# Routes

@app.route('/')
def root():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    # Dashboard shows overview, e.g., count of events, participants, bookings
    events = load_events()
    participants = load_participants()
    bookings = load_bookings()
    tickets = load_tickets()
    venues = load_venues()

    context = {
        'total_events': len(events),
        'total_participants': len(participants),
        'total_bookings': sum(b['quantity'] for b in bookings),
        'total_venues': len(venues),
        'total_tickets_available': sum(t['available'] for t in tickets)
    }
    return render_template('dashboard.html', **context)

@app.route('/events')
def events_list():
    # Optionally filter by date or venue_id through query parameters
    events = load_events()
    venue_id = request.args.get('venue_id')
    event_date = request.args.get('date')

    if venue_id:
        events = [e for e in events if e['venue_id'] == venue_id]
    if event_date:
        events = [e for e in events if e['date'] == event_date]

    venues = load_venues()
    venue_dict = {v['venue_id']: v for v in venues}

    context = {
        'events': events,
        'venues': venue_dict
    }
    return render_template('events.html', **context)

@app.route('/events/<event_id>')
def event_detail(event_id):
    events = load_events()
    event = next((e for e in events if e['event_id'] == event_id), None)
    if not event:
        return "Event not found", 404

    venues = load_venues()
    venue = next((v for v in venues if v['venue_id'] == event['venue_id']), None)

    tickets = load_tickets()
    event_tickets = [t for t in tickets if t['event_id'] == event_id]

    schedules = load_schedules()
    event_schedules = [s for s in schedules if s['event_id'] == event_id]

    context = {
        'event': event,
        'venue': venue,
        'tickets': event_tickets,
        'schedules': event_schedules
    }
    return render_template('event_detail.html', **context)

@app.route('/book', methods=['POST'])
def book_ticket():
    ticket_id = request.form.get('ticket_id')
    participant_id = request.form.get('participant_id')
    quantity = request.form.get('quantity')

    # Validate inputs
    if not ticket_id or not participant_id or not quantity:
        return "Missing booking information", 400

    try:
        quantity = int(quantity)
    except ValueError:
        return "Invalid quantity", 400

    tickets = load_tickets()
    ticket = next((t for t in tickets if t['ticket_id'] == ticket_id), None)
    if not ticket:
        return "Ticket not found", 404

    if ticket['available'] < quantity:
        return "Not enough tickets available", 400

    participants = load_participants()
    participant = next((p for p in participants if p['participant_id'] == participant_id), None)
    if not participant:
        return "Participant not found", 404

    # Load current bookings to determine new booking_id
    bookings = load_bookings()
    booking_ids = [int(b['booking_id']) for b in bookings if b['booking_id'].isdigit()]
    next_booking_id = str(max(booking_ids) + 1 if booking_ids else 1)

    # Add new booking
    new_booking = f"{next_booking_id}|{ticket_id}|{participant_id}|{quantity}"
    try:
        with open(BOOKINGS_FILE, 'a') as f:
            f.write(new_booking + '\n')
    except Exception:
        return "Failed to save booking", 500

    # Update tickets available
    try:
        # Rewrite tickets.txt with updated availability
        for t in tickets:
            if t['ticket_id'] == ticket_id:
                t['available'] -= quantity
        with open(TICKETS_FILE, 'w') as f:
            for t in tickets:
                line = f"{t['ticket_id']}|{t['event_id']}|{t['type']}|{t['price']}|{t['available']}"
                f.write(line + '\n')
    except Exception:
        return "Failed to update ticket availability", 500

    return redirect(url_for('booking_summary'))

@app.route('/participants')
def participants_list():
    participants = load_participants()
    context = {'participants': participants}
    return render_template('participants.html', **context)

@app.route('/venues')
def venues_list():
    venues = load_venues()
    context = {'venues': venues}
    return render_template('venues.html', **context)

@app.route('/schedules')
def schedules_list():
    schedules = load_schedules()
    events = load_events()
    venues = load_venues()
    # Creating dictionary for event names
    events_dict = {e['event_id']: e for e in events}

    context = {
        'schedules': schedules,
        'events': events_dict,
        'venues': venues
    }
    return render_template('schedules.html', **context)

@app.route('/booking_summary')
def booking_summary():
    bookings = load_bookings()
    tickets = load_tickets()
    participants = load_participants()

    # For each booking, gather info
    tickets_dict = {t['ticket_id']: t for t in tickets}
    participants_dict = {p['participant_id']: p for p in participants}

    booking_details = []
    for b in bookings:
        ticket = tickets_dict.get(b['ticket_id'])
        participant = participants_dict.get(b['participant_id'])
        if ticket and participant:
            detail = {
                'booking_id': b['booking_id'],
                'participant_name': participant['name'],
                'ticket_type': ticket['type'],
                'quantity': b['quantity'],
                'event_id': ticket['event_id'],
                'price': ticket['price']
            }
            booking_details.append(detail)

    context = {'booking_details': booking_details}
    return render_template('booking_summary.html', **context)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
