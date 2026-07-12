from flask import Flask, render_template, redirect, url_for, request
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Utility loading functions

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
                'capacity': int(parts[8])
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
                'contact': parts[5]
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
                "event_id": int(parts[1]),
                "ticket_type": parts[2],
                "price": float(parts[3]),
                "available_count": int(parts[4]),
                "sold_count": int(parts[5])
            }
            tickets.append(ticket)
    return tickets


def save_tickets(tickets):
    path = os.path.join(DATA_DIR, 'tickets.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for t in tickets:
            line = f"{t['ticket_id']}|{t['event_id']}|{t['ticket_type']}|{t['price']}|{t['available_count']}|{t['sold_count']}\n"
            f.write(line)


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
                'status': parts[7]
            }
            bookings.append(booking)
    return bookings


def save_bookings(bookings):
    path = os.path.join(DATA_DIR, 'bookings.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for b in bookings:
            line = f"{b['booking_id']}|{b['event_id']}|{b['customer_name']}|{b['booking_date']}|{b['ticket_count']}|{b['ticket_type']}|{b['total_amount']}|{b['status']}\n"
            f.write(line)


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
                'registration_date': parts[6]
            }
            participants.append(participant)
    return participants


def save_participants(participants):
    path = os.path.join(DATA_DIR, 'participants.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for p in participants:
            line = f"{p['participant_id']}|{p['event_id']}|{p['name']}|{p['email']}|{p['booking_id']}|{p['status']}|{p['registration_date']}\n"
            f.write(line)


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
                'venue_id': int(parts[6])
            }
            schedules.append(schedule)
    return schedules


# Routes implementations

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard_page'))


@app.route('/dashboard')
def dashboard_page():
    # As per specs, featured_events structure with keys event_id:int, event_name:str, date:str, etc.
    events = load_events()
    # Considering featured_events as first some events, or those with soonest date
    # Sort by date ascending to pick featured events
    featured_events = sorted(events, key=lambda e: e['date'])[:5]
    return render_template('dashboard.html', featured_events=featured_events)


@app.route('/events')
def events_page():
    events = load_events()
    # events context as list of dicts (event_id, event_name, category, date, location) per spec
    simple_events = [
        {
            'event_id': ev['event_id'],
            'event_name': ev['event_name'],
            'category': ev['category'],
            'date': ev['date'],
            'location': ev['location']
        } for ev in events
    ]
    return render_template('events.html', events=simple_events)


@app.route('/events/search', methods=['POST'])
def events_search():
    search_term = request.form.get('search', '').strip().lower()
    category_filter = request.form.get('category', '').strip().lower()

    events = load_events()
    filtered = []
    for ev in events:
        # Filter by search_term in event_name or location or date
        matches_search = (search_term in ev['event_name'].lower() or
                          search_term in ev['location'].lower() or
                          search_term in ev['date'].lower()) if search_term else True
        # Filter by category
        matches_category = (ev['category'].lower() == category_filter) if category_filter else True

        if matches_search and matches_category:
            filtered.append({
                'event_id': ev['event_id'],
                'event_name': ev['event_name'],
                'category': ev['category'],
                'date': ev['date'],
                'location': ev['location']
            })
    return render_template('events.html', events=filtered)


@app.route('/event/<int:event_id>')
def event_details(event_id):
    events = load_events()
    event = next((ev for ev in events if ev['event_id'] == event_id), None)
    if event is None:
        return "Event not found", 404
    return render_template('event_details.html', event=event)


@app.route('/book_ticket', methods=['GET'])
def book_ticket_page():
    events = load_events()
    # Provide minimal event info (event_id, event_name)
    simple_events = [{'event_id': ev['event_id'], 'event_name': ev['event_name']} for ev in events]
    return render_template('book_ticket.html', events=simple_events, booking_confirmation=None)


@app.route('/book_ticket', methods=['POST'])
def book_ticket_submit():
    events = load_events()
    tickets = load_tickets()
    bookings = load_bookings()

    # fetch form data
    event_id_str = request.form.get('event_id')
    customer_name = request.form.get('customer_name', '').strip()
    ticket_count_str = request.form.get('ticket_count', '').strip()
    ticket_type = request.form.get('ticket_type', '').strip()

    error_message = None
    booking_confirmation = None

    # Validate
    try:
        event_id = int(event_id_str)
    except (ValueError, TypeError):
        error_message = "Invalid event selected." 
        event_id = None

    try:
        ticket_count = int(ticket_count_str)
        if ticket_count <= 0:
            error_message = "Ticket count must be a positive integer."
    except (ValueError, TypeError):
        ticket_count = 0
        error_message = "Invalid ticket count."

    if not customer_name:
        error_message = "Customer name is required."

    if not ticket_type:
        error_message = "Ticket type is required."

    # Check event exists
    event = next((ev for ev in events if ev['event_id'] == event_id), None) if event_id else None
    if not event:
        error_message = "Selected event not found."

    # Check ticket availability
    ticket_info = None
    if event_id and ticket_type:
        ticket_info = next((t for t in tickets if t['event_id'] == event_id and t['ticket_type'].lower() == ticket_type.lower()), None)
        if not ticket_info:
            error_message = f"Ticket type '{ticket_type}' not available for this event."

    if ticket_info and ticket_info['available_count'] < ticket_count:
        error_message = f"Not enough tickets available. Currently available: {ticket_info['available_count']}"

    if error_message:
        simple_events = [{'event_id': ev['event_id'], 'event_name': ev['event_name']} for ev in events]
        return render_template('book_ticket.html', events=simple_events, booking_confirmation={'error': error_message})

    # Process booking
    # Create new booking_id
    new_booking_id = 1
    if bookings:
        new_booking_id = max(b['booking_id'] for b in bookings) + 1

    total_amount = round(ticket_info['price'] * ticket_count, 2)
    import datetime
    booking_date = datetime.date.today().isoformat()
    new_booking = {
        'booking_id': new_booking_id,
        'event_id': event_id,
        'customer_name': customer_name,
        'booking_date': booking_date,
        'ticket_count': ticket_count,
        'ticket_type': ticket_info['ticket_type'],
        'total_amount': total_amount,
        'status': 'Confirmed'
    }
    bookings.append(new_booking)
    # Update tickets availability
    ticket_info['available_count'] -= ticket_count
    ticket_info['sold_count'] += ticket_count

    # Save back
    save_bookings(bookings)
    save_tickets(tickets)

    confirmation_message = {
        'message': f"Booking confirmed for {customer_name}.",
        'booking_id': new_booking_id,
        'event_name': event['event_name'],
        'ticket_type': ticket_info['ticket_type'],
        'ticket_count': ticket_count,
        'total_amount': total_amount
    }
    simple_events = [{'event_id': ev['event_id'], 'event_name': ev['event_name']} for ev in events]
    return render_template('book_ticket.html', events=simple_events, booking_confirmation=confirmation_message)


@app.route('/participants', methods=['GET'])
def participants_page():
    participants = load_participants()
    return render_template('participants.html', participants=participants)


@app.route('/participants/add', methods=['POST'])
def add_participant():
    participants = load_participants()
    # Extract form data
    event_id_str = request.form.get('event_id')
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()
    booking_id_str = request.form.get('booking_id')
    status = request.form.get('status', '').strip()
    registration_date = request.form.get('registration_date', '').strip()

    error_message = None

    try:
        event_id = int(event_id_str)
    except (ValueError, TypeError):
        error_message = "Invalid event ID."

    try:
        booking_id = int(booking_id_str)
    except (ValueError, TypeError):
        booking_id = None
        error_message = "Invalid booking ID."

    if not name or not email or not status or not registration_date:
        error_message = "All fields are required."

    if error_message:
        participants = load_participants()
        return render_template('participants.html', participants=participants, error=error_message)

    new_participant_id = 1
    if participants:
        new_participant_id = max(p['participant_id'] for p in participants) + 1

    new_participant = {
        'participant_id': new_participant_id,
        'event_id': event_id,
        'name': name,
        'email': email,
        'booking_id': booking_id if booking_id is not None else 0,
        'status': status,
        'registration_date': registration_date
    }

    participants.append(new_participant)
    save_participants(participants)

    # After adding redirect to participants page
    return redirect(url_for('participants_page'))


@app.route('/venues')
def venues_page():
    venues = load_venues()
    simple_venues = [{
        'venue_id': v['venue_id'],
        'venue_name': v['venue_name'],
        'location': v['location'],
        'capacity': v['capacity'],
        'amenities': v['amenities']
    } for v in venues]
    return render_template('venues.html', venues=simple_venues)


@app.route('/venue/<int:venue_id>')
def venue_details(venue_id):
    venues = load_venues()
    venue = next((v for v in venues if v['venue_id'] == venue_id), None)
    if venue is None:
        return "Venue not found", 404
    return render_template('venue_details.html', venue=venue)


@app.route('/schedules', methods=['GET'])
def schedules_page():
    schedules = load_schedules()
    return render_template('schedules.html', schedules=schedules)


@app.route('/schedules/filter', methods=['POST'])
def schedules_filter():
    filter_date = request.form.get('date', '').strip()
    filter_event_id_str = request.form.get('event_id', '').strip()
    filter_event_id = None
    try:
        filter_event_id = int(filter_event_id_str)
    except (ValueError, TypeError):
        filter_event_id = None

    schedules = load_schedules()
    filtered = []
    for sched in schedules:
        matches_date = filter_date == '' or (filter_date in sched['session_time'])
        matches_event = filter_event_id is None or sched['event_id'] == filter_event_id
        if matches_date and matches_event:
            filtered.append(sched)
    return render_template('schedules.html', schedules=filtered)


@app.route('/bookings', methods=['GET'])
def bookings_page():
    bookings = load_bookings()
    return render_template('bookings.html', bookings=bookings)


@app.route('/booking/cancel/<int:booking_id>', methods=['POST'])
def cancel_booking(booking_id):
    bookings = load_bookings()
    booking = next((b for b in bookings if b['booking_id'] == booking_id), None)
    if booking is None:
        error_message = "Booking not found."
        bookings = load_bookings()
        return render_template('bookings.html', bookings=bookings, error=error_message)

    # Only cancel if status not already cancelled
    if booking['status'].lower() == 'cancelled':
        error_message = "Booking already cancelled."
        bookings = load_bookings()
        return render_template('bookings.html', bookings=bookings, error=error_message)

    booking['status'] = 'Cancelled'
    save_bookings(bookings)

    bookings = load_bookings()  # Reload updated list
    success_message = f"Booking {booking_id} has been cancelled."
    return render_template('bookings.html', bookings=bookings, success=success_message)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
