from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'

# Paths to data files
DATA_DIR = 'data'
EVENTS_FILE = os.path.join(DATA_DIR, 'events.txt')
VENUES_FILE = os.path.join(DATA_DIR, 'venues.txt')
TICKETS_FILE = os.path.join(DATA_DIR, 'tickets.txt')
BOOKINGS_FILE = os.path.join(DATA_DIR, 'bookings.txt')
PARTICIPANTS_FILE = os.path.join(DATA_DIR, 'participants.txt')
SCHEDULES_FILE = os.path.join(DATA_DIR, 'schedules.txt')

# Constants
EVENT_CATEGORIES = ['Conference', 'Concert', 'Sports', 'Workshop', 'Social']

# Helper functions to load and save data

def load_events():
    events = []
    if not os.path.isfile(EVENTS_FILE):
        return events
    try:
        with open(EVENTS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
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
                except ValueError:
                    continue
    except Exception:
        pass
    return events


def load_venues():
    venues = []
    if not os.path.isfile(VENUES_FILE):
        return venues
    try:
        with open(VENUES_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
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
                except ValueError:
                    continue
    except Exception:
        pass
    return venues


def load_tickets():
    tickets = []
    if not os.path.isfile(TICKETS_FILE):
        return tickets
    try:
        with open(TICKETS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
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
                except ValueError:
                    continue
    except Exception:
        pass
    return tickets


def save_tickets(tickets):
    try:
        with open(TICKETS_FILE, 'w', encoding='utf-8') as f:
            for t in tickets:
                line = f"{t['ticket_id']}|{t['event_id']}|{t['ticket_type']}|{t['price']:.2f}|{t['available_count']}|{t['sold_count']}"
                f.write(line + '\n')
    except Exception:
        pass


def load_bookings():
    bookings = []
    if not os.path.isfile(BOOKINGS_FILE):
        return bookings
    try:
        with open(BOOKINGS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) !=8:
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
                except ValueError:
                    continue
    except Exception:
        pass
    return bookings


def save_bookings(bookings):
    try:
        with open(BOOKINGS_FILE, 'w', encoding='utf-8') as f:
            for b in bookings:
                line = f"{b['booking_id']}|{b['event_id']}|{b['customer_name']}|{b['booking_date']}|{b['ticket_count']}|{b['ticket_type']}|{b['total_amount']:.2f}|{b['status']}"
                f.write(line+'\n')
    except Exception:
        pass


def load_participants():
    participants = []
    if not os.path.isfile(PARTICIPANTS_FILE):
        return participants
    try:
        with open(PARTICIPANTS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) !=7:
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
                except ValueError:
                    continue
    except Exception:
        pass
    return participants


def save_participants(participants):
    try:
        with open(PARTICIPANTS_FILE, 'w', encoding='utf-8') as f:
            for p in participants:
                line = f"{p['participant_id']}|{p['event_id']}|{p['name']}|{p['email']}|{p['booking_id']}|{p['status']}|{p['registration_date']}"
                f.write(line+'\n')
    except Exception:
        pass


def load_schedules():
    schedules = []
    if not os.path.isfile(SCHEDULES_FILE):
        return schedules
    try:
        with open(SCHEDULES_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
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
                except ValueError:
                    continue
    except Exception:
        pass
    return schedules


# Flask routes

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    events = load_events()
    featured_events = []
    for e in events:
        featured_events.append({
            'event_id': e['event_id'],
            'event_name': e['event_name'],
            'date': e['date'],
            'location': e['location']
        })
    return render_template('dashboard.html', featured_events=featured_events)


@app.route('/events')
def events_listing():
    events = load_events()
    categories = EVENT_CATEGORIES
    return render_template('events.html', events=events, categories=categories)


@app.route('/events/search', methods=['POST'])
def search_events():
    search_term = request.form.get('search_term', '').strip().lower()
    category = request.form.get('category_filter', '')
    events = load_events()
    categories = EVENT_CATEGORIES

    filtered_events = []
    for e in events:
        matches_search = True
        if search_term:
            matches_search = search_term in e['event_name'].lower()
        matches_category = True
        if category and category != 'All':
            matches_category = e['category'] == category
        if matches_search and matches_category:
            filtered_events.append(e)

    return render_template('events.html', events=filtered_events, categories=categories)


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


@app.route('/book_ticket', methods=['GET', 'POST'])
def book_ticket():
    if request.method == 'GET':
        events = load_events()
        event_list = [{'event_id': e['event_id'], 'event_name': e['event_name']} for e in events]
        return render_template('ticket_booking.html', events=event_list)

    # POST method
    try:
        event_id = int(request.form.get('event_id', '0'))
        ticket_type = request.form.get('ticket_type', '').strip()
        ticket_count = int(request.form.get('ticket_count', '0'))
        customer_name = request.form.get('customer_name', '').strip()
    except Exception:
        return render_template('ticket_booking.html', confirmation={'booking_status': 'Invalid input'})

    if event_id <= 0 or not ticket_type or ticket_count <= 0 or not customer_name:
        return render_template('ticket_booking.html', confirmation={'booking_status': 'Invalid booking details'})

    events = load_events()
    event = next((e for e in events if e['event_id'] == event_id), None)
    if not event:
        return render_template('ticket_booking.html', confirmation={'booking_status': 'Event not found'})

    tickets = load_tickets()
    ticket = next((t for t in tickets if t['event_id'] == event_id and t['ticket_type'].lower() == ticket_type.lower()), None)
    if not ticket:
        return render_template('ticket_booking.html', confirmation={'booking_status': 'Ticket type not found'})

    if ticket['available_count'] < ticket_count:
        return render_template('ticket_booking.html', confirmation={'booking_status': 'Not enough tickets available'})

    total_amount = ticket['price'] * ticket_count

    bookings = load_bookings()
    new_booking_id = 1
    if bookings:
        new_booking_id = max(b['booking_id'] for b in bookings) + 1

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
    save_bookings(bookings)

    # Update ticket availability
    ticket['available_count'] -= ticket_count
    ticket['sold_count'] += ticket_count
    save_tickets(tickets)

    confirmation = {
        'event_name': event['event_name'],
        'ticket_count': ticket_count,
        'ticket_type': ticket_type,
        'total_amount': total_amount,
        'booking_status': 'Confirmed'
    }

    return render_template('ticket_booking.html', confirmation=confirmation)


@app.route('/participants', methods=['GET', 'POST'])
def participants_management():
    events = load_events()
    event_names = {e['event_id']: e['event_name'] for e in events}

    if request.method == 'GET':
        participants = load_participants()
        for p in participants:
            p['event_name'] = event_names.get(p['event_id'], 'Unknown')
        return render_template('participants.html', participants=participants)
    else:
        participants = load_participants()
        form = request.form
        changed = False
        for p in participants:
            status_key = f"status_{p['participant_id']}"
            if status_key in form:
                new_status = form.get(status_key)
                if new_status and new_status != p['status']:
                    p['status'] = new_status
                    changed = True
        if changed:
            save_participants(participants)
        for p in participants:
            p['event_name'] = event_names.get(p['event_id'], 'Unknown')
        return render_template('participants.html', participants=participants)


@app.route('/venues')
def venues():
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
    for b in bookings:
        b['event_name'] = events_map.get(b['event_id'], 'Unknown')
    return render_template('bookings.html', bookings=bookings)


@app.route('/booking/cancel/<int:booking_id>', methods=['POST'])
def cancel_booking(booking_id):
    bookings = load_bookings()
    changed = False
    for b in bookings:
        if b['booking_id'] == booking_id:
            b['status'] = 'Cancelled'
            changed = True
            break
    if changed:
        save_bookings(bookings)
    return redirect(url_for('bookings_summary'))


if __name__ == '__main__':
    app.run(debug=True, port=5000)
