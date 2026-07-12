from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

# Helper functions to load data from the data files

def load_events():
    events = []
    try:
        with open('data/events.txt', 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
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
        with open('data/venues.txt', 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
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
        with open('data/tickets.txt', 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
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
        with open('data/bookings.txt', 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
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
        with open('data/participants.txt', 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
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
        with open('data/schedules.txt', 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
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


# Helper to save tickets data back

def save_tickets(tickets):
    try:
        with open('data/tickets.txt', 'w', encoding='utf-8') as f:
            for t in tickets:
                line = '|'.join([
                    str(t['ticket_id']),
                    str(t['event_id']),
                    t['ticket_type'],
                    f"{t['price']:.2f}",
                    str(t['available_count']),
                    str(t['sold_count'])
                ])
                f.write(line + '\n')
    except Exception:
        pass


# Helper to save bookings data back

def save_bookings(bookings):
    try:
        with open('data/bookings.txt', 'w', encoding='utf-8') as f:
            for b in bookings:
                line = '|'.join([
                    str(b['booking_id']),
                    str(b['event_id']),
                    b['customer_name'],
                    b['booking_date'],
                    str(b['ticket_count']),
                    b['ticket_type'],
                    f"{b['total_amount']:.2f}",
                    b['status']
                ])
                f.write(line + '\n')
    except Exception:
        pass


@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    events = load_events()
    # For featured_events, generally select first few or some criteria
    featured_events = []
    # We pick up to 5 upcoming events sorted by date ascending
    from datetime import datetime
    try:
        events_sorted = sorted(events, key=lambda e: datetime.strptime(e['date'], '%Y-%m-%d'))
        featured_events = [
            {
                'event_id': e['event_id'],
                'event_name': e['event_name'],
                'category': e['category'],
                'date': e['date'],
                'location': e['location']
            } for e in events_sorted[:5]
        ]
    except Exception:
        featured_events = []
    return render_template('dashboard.html', featured_events=featured_events)


@app.route('/events')
def events_listing():
    events = load_events()
    simple_events = [
        {
            'event_id': e['event_id'],
            'event_name': e['event_name'],
            'category': e['category'],
            'date': e['date'],
            'location': e['location']
        } for e in events
    ]
    return render_template('events.html', events=simple_events)


@app.route('/events/search', methods=['POST'])
def events_search():
    events = load_events()
    category = request.form.get('category', '').strip()
    keyword = request.form.get('keyword', '').strip().lower()

    filtered_events = []

    for e in events:
        if category and e['category'] != category:
            continue
        if keyword and keyword not in e['event_name'].lower() and keyword not in e['location'].lower():
            continue
        filtered_events.append({
            'event_id': e['event_id'],
            'event_name': e['event_name'],
            'category': e['category'],
            'date': e['date'],
            'location': e['location']
        })

    return render_template('events.html', filtered_events=filtered_events)


@app.route('/event/<int:event_id>')
def event_details(event_id):
    events = load_events()
    event = None
    for e in events:
        if e['event_id'] == event_id:
            event = e
            break
    if not event:
        # Could redirect to events or render 404
        return redirect(url_for('events_listing'))

    return render_template('event_details.html', event=event)


@app.route('/book_ticket', methods=['GET', 'POST'])
def book_ticket():
    if request.method == 'GET':
        events = load_events()
        simple_events = [{ 'event_id': e['event_id'], 'event_name': e['event_name']} for e in events]
        return render_template('ticket_booking.html', events=simple_events)

    # POST: handle booking
    errors = []
    event_id = request.form.get('event_id')
    ticket_count = request.form.get('ticket_count')
    ticket_type = request.form.get('ticket_type')
    customer_name = request.form.get('customer_name', '').strip()

    # Validate inputs
    if not event_id or not event_id.isdigit():
        errors.append('Invalid event selected.')
    else:
        event_id = int(event_id)
    if not ticket_count or not ticket_count.isdigit() or int(ticket_count) < 1:
        errors.append('Ticket count must be a positive integer.')
    else:
        ticket_count = int(ticket_count)
    if ticket_type not in ('General', 'VIP', 'Early Bird'):
        errors.append('Invalid ticket type.')
    if not customer_name:
        errors.append('Customer name is required.')

    if errors:
        events = load_events()
        simple_events = [{ 'event_id': e['event_id'], 'event_name': e['event_name']} for e in events]
        return render_template('ticket_booking.html', events=simple_events, errors=errors)

    # Find tickets for the event and ticket type
    tickets = load_tickets()
    ticket = None
    for t in tickets:
        if t['event_id'] == event_id and t['ticket_type'] == ticket_type:
            ticket = t
            break

    if not ticket:
        errors.append('Ticket type not available for this event.')

    if ticket and ticket['available_count'] < ticket_count:
        errors.append('Not enough tickets available.')

    if errors:
        events = load_events()
        simple_events = [{ 'event_id': e['event_id'], 'event_name': e['event_name']} for e in events]
        return render_template('ticket_booking.html', events=simple_events, errors=errors)

    # Calculate total amount
    total_amount = ticket_count * ticket['price']

    # Create booking_id (simple max+1)
    bookings = load_bookings()
    booking_id = max([b['booking_id'] for b in bookings], default=0) + 1

    from datetime import datetime
    booking_date = datetime.now().strftime('%Y-%m-%d')

    new_booking = {
        'booking_id': booking_id,
        'event_id': event_id,
        'customer_name': customer_name,
        'booking_date': booking_date,
        'ticket_count': ticket_count,
        'ticket_type': ticket_type,
        'total_amount': total_amount,
        'status': 'Confirmed'
    }

    # Update tickets data
    ticket['available_count'] -= ticket_count
    ticket['sold_count'] += ticket_count

    bookings.append(new_booking)

    # Save updates to files
    save_tickets(tickets)
    save_bookings(bookings)

    booking_confirmation = {
        'booking_id': booking_id,
        'event_id': event_id,
        'ticket_count': ticket_count,
        'ticket_type': ticket_type,
        'total_amount': total_amount
    }

    return render_template('ticket_booking.html', booking_confirmation=booking_confirmation)


@app.route('/participants')
def participants_management():
    participants = load_participants()
    return render_template('participants.html', participants=participants)


@app.route('/participants/add', methods=['POST'])
def add_participant():
    participants = load_participants()
    errors = []
    # Extract participant info from form
    try:
        event_id = int(request.form.get('event_id', '0'))
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        booking_id = int(request.form.get('booking_id', '0'))
        status = request.form.get('status', '').strip()
        registration_date = request.form.get('registration_date', '').strip()

        if event_id <= 0:
            errors.append('Invalid event ID.')
        if not name:
            errors.append('Name is required.')
        if not email:
            errors.append('Email is required.')
        if booking_id <= 0:
            errors.append('Invalid booking ID.')
        if status not in ('Registered', 'Confirmed', 'Attended'):
            errors.append('Invalid status.')
        if not registration_date:
            errors.append('Registration date is required.')
    except Exception:
        errors.append('Form data missing or invalid.')

    if errors:
        return render_template('participants.html', participants=participants, errors=errors)

    participant_id = max([p['participant_id'] for p in participants], default=0) + 1
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

    # Save back to file
    try:
        with open('data/participants.txt', 'w', encoding='utf-8') as f:
            for p in participants:
                line = '|'.join([
                    str(p['participant_id']),
                    str(p['event_id']),
                    p['name'],
                    p['email'],
                    str(p['booking_id']),
                    p['status'],
                    p['registration_date']
                ])
                f.write(line + '\n')
    except Exception:
        pass

    return render_template('participants.html', participants=participants)


@app.route('/venues')
def venues_listing():
    venues = load_venues()
    return render_template('venues.html', venues=venues)


@app.route('/venue/<int:venue_id>')
def venue_details(venue_id):
    venues = load_venues()
    venue = None
    for v in venues:
        if v['venue_id'] == venue_id:
            venue = v
            break
    if not venue:
        return redirect(url_for('venues_listing'))
    return render_template('venue_details.html', venue=venue)


@app.route('/schedules')
def schedules():
    schedules_list = load_schedules()
    events = load_events()
    events_simple = [{'event_id': e['event_id'], 'event_name': e['event_name']} for e in events]
    return render_template('schedules.html', schedules=schedules_list, events=events_simple)


@app.route('/bookings')
def bookings_summary():
    bookings = load_bookings()
    events = load_events()
    event_dict = {e['event_id']: e['event_name'] for e in events}

    bookings_with_names = []
    for b in bookings:
        bookings_with_names.append({
            'booking_id': b['booking_id'],
            'event_id': b['event_id'],
            'event_name': event_dict.get(b['event_id'], 'Unknown'),
            'booking_date': b['booking_date'],
            'ticket_count': b['ticket_count'],
            'ticket_type': b['ticket_type'],
            'total_amount': b['total_amount'],
            'status': b['status']
        })

    return render_template('bookings.html', bookings=bookings_with_names)


@app.route('/booking/cancel/<int:booking_id>', methods=['POST'])
def cancel_booking(booking_id):
    bookings = load_bookings()
    updated_bookings = []
    booking_found = False
    for b in bookings:
        if b['booking_id'] == booking_id:
            booking_found = True
            # Mark status as Cancelled
            if b['status'] != 'Cancelled':
                b['status'] = 'Cancelled'
        updated_bookings.append(b)

    if booking_found:
        save_bookings(updated_bookings)

    event_id = None
    for b in updated_bookings:
        if b['booking_id'] == booking_id:
            event_id = b['event_id']
            break

    return redirect(url_for('bookings_summary'))


if __name__ == '__main__':
    app.run(debug=True, port=5000)
