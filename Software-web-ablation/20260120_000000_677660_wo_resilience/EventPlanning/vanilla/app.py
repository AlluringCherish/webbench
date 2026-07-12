from flask import Flask, render_template, redirect, url_for, request, jsonify
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'


# Helper functions for loading data

def load_events():
    events = []
    filepath = os.path.join(DATA_DIR, 'events.txt')
    if not os.path.exists(filepath):
        return events
    with open(filepath, 'r', encoding='utf-8') as f:
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
    filepath = os.path.join(DATA_DIR, 'venues.txt')
    if not os.path.exists(filepath):
        return venues
    with open(filepath, 'r', encoding='utf-8') as f:
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
    filepath = os.path.join(DATA_DIR, 'tickets.txt')
    if not os.path.exists(filepath):
        return tickets
    with open(filepath, 'r', encoding='utf-8') as f:
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


def write_tickets(tickets):
    filepath = os.path.join(DATA_DIR, 'tickets.txt')
    with open(filepath, 'w', encoding='utf-8') as f:
        for t in tickets:
            line = f"{t['ticket_id']}|{t['event_id']}|{t['ticket_type']}|{t['price']}|{t['available_count']}|{t['sold_count']}\n"
            f.write(line)


def load_bookings():
    bookings = []
    filepath = os.path.join(DATA_DIR, 'bookings.txt')
    if not os.path.exists(filepath):
        return bookings
    with open(filepath, 'r', encoding='utf-8') as f:
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


def write_bookings(bookings):
    filepath = os.path.join(DATA_DIR, 'bookings.txt')
    with open(filepath, 'w', encoding='utf-8') as f:
        for b in bookings:
            line = f"{b['booking_id']}|{b['event_id']}|{b['customer_name']}|{b['booking_date']}|{b['ticket_count']}|{b['ticket_type']}|{b['total_amount']}|{b['status']}\n"
            f.write(line)


def load_participants():
    participants = []
    filepath = os.path.join(DATA_DIR, 'participants.txt')
    if not os.path.exists(filepath):
        return participants
    with open(filepath, 'r', encoding='utf-8') as f:
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


def write_participants(participants):
    filepath = os.path.join(DATA_DIR, 'participants.txt')
    with open(filepath, 'w', encoding='utf-8') as f:
        for p in participants:
            line = f"{p['participant_id']}|{p['event_id']}|{p['name']}|{p['email']}|{p['booking_id']}|{p['status']}|{p['registration_date']}\n"
            f.write(line)


def load_schedules():
    schedules = []
    filepath = os.path.join(DATA_DIR, 'schedules.txt')
    if not os.path.exists(filepath):
        return schedules
    with open(filepath, 'r', encoding='utf-8') as f:
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


# Route implementations

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    # Load events
    events = load_events()
    # For featured events, select up to 5 upcoming events sorted by date (ascending), only future or ongoing dates
    today = datetime.today().strftime('%Y-%m-%d')
    featured_events = [e for e in events if e['date'] >= today]
    # Sort by date ascending then time ascending
    featured_events.sort(key=lambda x: (x['date'], x['time']))
    featured_events = featured_events[:5]

    # Map keys for featured_events as per spec (event_id, event_name, category, date, time, location)
    context_featured_events = []
    for e in featured_events:
        context_featured_events.append({
            'event_id': e['event_id'],
            'event_name': e['event_name'],
            'category': e['category'],
            'date': e['date'],
            'time': e['time'],
            'location': e['location']
        })
    return render_template('dashboard.html', featured_events=context_featured_events)


@app.route('/events')
def events_listing():
    events = load_events()
    # Map keys exactly as required (includes description)
    # events is a list of dicts already as required
    return render_template('events.html', events=events)


@app.route('/events/<int:event_id>')
def event_details(event_id):
    events = load_events()
    event = next((e for e in events if e['event_id'] == event_id), None)
    if not event:
        # If event not found, could return 404 or redirect to events page
        return redirect(url_for('events_listing'))
    return render_template('event_details.html', event=event)


@app.route('/book_ticket', methods=['GET', 'POST'])
def book_ticket():
    if request.method == 'GET':
        events = load_events()
        events_list = [{'event_id': e['event_id'], 'event_name': e['event_name']} for e in events]
        return render_template('ticket_booking.html', events_list=events_list)

    # POST method: process booking
    # Extract form data
    form = request.form
    try:
        event_id = int(form.get('event_id', 0))
        customer_name = form.get('customer_name', '').strip()
        ticket_count = int(form.get('ticket_count', 0))
        ticket_type = form.get('ticket_type', '').strip()
    except Exception:
        # Invalid data
        events = load_events()
        events_list = [{'event_id': e['event_id'], 'event_name': e['event_name']} for e in events]
        return render_template('ticket_booking.html', events_list=events_list)

    if event_id <= 0 or ticket_count <= 0 or not customer_name or not ticket_type:
        events = load_events()
        events_list = [{'event_id': e['event_id'], 'event_name': e['event_name']} for e in events]
        return render_template('ticket_booking.html', events_list=events_list)

    # Load tickets to check availability and price
    tickets = load_tickets()
    ticket = next((t for t in tickets if t['event_id'] == event_id and t['ticket_type'].lower() == ticket_type.lower()), None)
    if not ticket or ticket['available_count'] < ticket_count:
        # Not enough tickets available, show error or remain on form
        events = load_events()
        events_list = [{'event_id': e['event_id'], 'event_name': e['event_name']} for e in events]
        return render_template('ticket_booking.html', events_list=events_list)

    # Update tickets availability
    ticket['available_count'] -= ticket_count
    ticket['sold_count'] += ticket_count
    write_tickets(tickets)

    # Load bookings to add new booking
    bookings = load_bookings()
    new_booking_id = (max((b['booking_id'] for b in bookings), default=0) + 1) if bookings else 1

    # Compute total amount
    total_amount = ticket_count * ticket['price']

    # Booking date today
    booking_date = datetime.today().strftime('%Y-%m-%d')

    # Add booking record
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
    write_bookings(bookings)

    # Prepare confirmation dictionary as per spec
    event_name = next((e['event_name'] for e in load_events() if e['event_id'] == event_id), 'Unknown Event')
    booking_confirmation = {
        'booking_id': new_booking_id,
        'event_name': event_name,
        'ticket_count': ticket_count,
        'ticket_type': ticket_type,
        'total_amount': total_amount,
        'status': 'Confirmed'
    }
    return render_template('ticket_booking.html', booking_confirmation=booking_confirmation)


@app.route('/participants')
def participants_management():
    participants = load_participants()
    return render_template('participants.html', participants=participants)


@app.route('/participants/add', methods=['POST'])
def add_participant():
    form = request.form
    try:
        event_id = int(form.get('event_id', 0))
        name = form.get('name', '').strip()
        email = form.get('email', '').strip()
        booking_id = int(form.get('booking_id', 0))
        status = form.get('status', 'Registered').strip()
        registration_date = form.get('registration_date', datetime.today().strftime('%Y-%m-%d'))
    except Exception:
        return jsonify({'success': False, 'message': 'Invalid data'}), 400

    if event_id <= 0 or not name or not email or booking_id <= 0:
        return jsonify({'success': False, 'message': 'Missing required data'}), 400

    participants = load_participants()
    new_participant_id = (max((p['participant_id'] for p in participants), default=0) + 1) if participants else 1

    new_participant = {
        'participant_id': new_participant_id,
        'event_id': event_id,
        'name': name,
        'email': email,
        'booking_id': booking_id,
        'status': status,
        'registration_date': registration_date
    }
    participants.append(new_participant)
    write_participants(participants)

    # Not specified frontend interaction; here we choose to return JSON success
    return jsonify({'success': True, 'participant_id': new_participant_id})


@app.route('/venues')
def venues_info():
    venues = load_venues()
    return render_template('venues.html', venues=venues)


@app.route('/schedules')
def event_schedules():
    schedules = load_schedules()
    return render_template('schedules.html', schedules=schedules)


@app.route('/bookings')
def bookings_summary():
    bookings = load_bookings()
    return render_template('bookings.html', bookings=bookings)


@app.route('/bookings/cancel/<int:booking_id>', methods=['POST'])
def cancel_booking(booking_id):
    bookings = load_bookings()
    booking = next((b for b in bookings if b['booking_id'] == booking_id), None)
    if not booking:
        # Booking not found, redirect back
        return redirect(url_for('bookings_summary'))

    if booking['status'].lower() != 'cancelled':
        # Update booking status
        booking['status'] = 'Cancelled'
        write_bookings(bookings)
    return redirect(url_for('bookings_summary'))


if __name__ == '__main__':
    app.run(debug=True, port=5000)
