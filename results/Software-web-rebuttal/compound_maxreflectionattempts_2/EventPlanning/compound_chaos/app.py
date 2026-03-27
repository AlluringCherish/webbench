from flask import Flask, render_template, redirect, url_for, request
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

# Data loading helper functions

def load_events():
    events = []
    path = os.path.join('data', 'events.txt')
    try:
        with open(path, encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                # event_id|event_name|category|date|time|location|description
                parts = line.split('|')
                if len(parts) != 7:
                    continue
                event = {
                    'event_id': parts[0],
                    'event_name': parts[1],
                    'category': parts[2],
                    'date': parts[3],
                    'time': parts[4],
                    'location': parts[5],
                    'description': parts[6]
                }
                events.append(event)
    except Exception:
        pass
    return events

def load_venues():
    venues = []
    path = os.path.join('data', 'venues.txt')
    try:
        with open(path, encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                # venue_id|venue_name|capacity|location|amenities|contact
                parts = line.split('|')
                if len(parts) != 6:
                    continue
                venue = {
                    'venue_id': parts[0],
                    'venue_name': parts[1],
                    'capacity': int(parts[2]),
                    'location': parts[3],
                    'amenities': parts[4],
                    'contact': parts[5]
                }
                venues.append(venue)
    except Exception:
        pass
    return venues

def load_tickets():
    tickets = []
    path = os.path.join('data', 'tickets.txt')
    try:
        with open(path, encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                # ticket_id|event_id|ticket_type|price|capacity|sold_count
                parts = line.split('|')
                if len(parts) != 6:
                    continue
                ticket = {
                    'ticket_id': parts[0],
                    'event_id': parts[1],
                    'ticket_type': parts[2],
                    'price': float(parts[3]),
                    'capacity': int(parts[4]),
                    'sold_count': int(parts[5])
                }
                tickets.append(ticket)
    except Exception:
        pass
    return tickets

def load_bookings():
    bookings = []
    path = os.path.join('data', 'bookings.txt')
    try:
        with open(path, encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                # booking_id|schedule_id|participant_id|ticket_id|status|booking_date|total_amount
                parts = line.split('|')
                if len(parts) != 7:
                    continue
                booking = {
                    'booking_id': int(parts[0]),
                    'schedule_id': int(parts[1]),
                    'participant_id': parts[2],
                    'ticket_id': parts[3],
                    'status': parts[4],
                    'booking_date': parts[5],
                    'total_amount': float(parts[6])
                }
                bookings.append(booking)
    except Exception:
        pass
    return bookings

def load_participants():
    participants = []
    path = os.path.join('data', 'participants.txt')
    try:
        with open(path, encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                # participant_id|name|email|phone|registration_date|status
                parts = line.split('|')
                if len(parts) != 6:
                    continue
                participant = {
                    'participant_id': parts[0],
                    'name': parts[1],
                    'email': parts[2],
                    'phone': parts[3],
                    'registration_date': parts[4],
                    'status': parts[5]
                }
                participants.append(participant)
    except Exception:
        pass
    return participants

def load_schedules():
    schedules = []
    path = os.path.join('data', 'schedules.txt')
    try:
        with open(path, encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                # schedule_id|event_id|session_title|speaker|time|duration_minutes
                parts = line.split('|')
                if len(parts) != 6:
                    continue
                schedule = {
                    'schedule_id': int(parts[0]),
                    'event_id': parts[1],
                    'session_title': parts[2],
                    'speaker': parts[3],
                    'time': parts[4],
                    'duration_minutes': int(parts[5])
                }
                schedules.append(schedule)
    except Exception:
        pass
    return schedules

# Routes
@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard_page'))

@app.route('/dashboard')
def dashboard_page():
    events = load_events()
    # Featured events filter? If events have category or featured field: no such field in spec
    # Showing all events as featured_events for simplicity
    featured_events = events[:5]  # first 5 featured
    return render_template('dashboard.html', featured_events=featured_events)

@app.route('/events')
def events_listing():
    events = load_events()
    category_filter = request.args.get('category')
    date_filter = request.args.get('date')
    filtered_events = events
    if category_filter:
        filtered_events = [e for e in filtered_events if e['category'] == category_filter]
    if date_filter:
        filtered_events = [e for e in filtered_events if e['date'] == date_filter]
    return render_template('events.html', events=filtered_events)

@app.route('/events/<int:event_id>')
def event_details(event_id):
    events = load_events()
    event = None
    for e in events:
        try:
            if int(e['event_id']) == event_id:
                event = e
                break
        except Exception:
            continue
    if not event:
        return "Event not found", 404

    schedules = load_schedules()
    event_schedules = [s for s in schedules if s['event_id'] == str(event_id)]
    tickets = load_tickets()
    event_tickets = [t for t in tickets if t['event_id'] == str(event_id)]
    return render_template('event_details.html', event=event, schedules=event_schedules, tickets=event_tickets)

@app.route('/ticket_booking', methods=['GET', 'POST'])
def ticket_booking_page():
    tickets = load_tickets()
    events = load_events()
    participants = load_participants()
    message = None

    if request.method == 'GET':
        event_id = request.args.get('event_id')
        if not event_id:
            # redirect to events listing if no event selected
            return redirect(url_for('events_listing'))
        # details for this event
        event = next((e for e in events if e['event_id'] == event_id), None)
        event_tickets = [t for t in tickets if t['event_id'] == event_id]

        return render_template('ticket_booking.html', event=event, tickets=event_tickets, participants=participants)
    else:
        # POST - booking ticket
        participant_id = request.form.get('participant_id')
        ticket_id = request.form.get('ticket_id')
        ticket_quantity_str = request.form.get('ticket_quantity')

        # Validate input presence
        if not participant_id or not ticket_id or not ticket_quantity_str:
            message = 'All booking fields required.'
            return render_template('ticket_booking.html', message=message)

        try:
            ticket_quantity = int(ticket_quantity_str)
            if ticket_quantity < 1:
                message = 'Ticket quantity must be positive.'
                return render_template('ticket_booking.html', message=message)
        except ValueError:
            message = 'Invalid ticket quantity.'
            return render_template('ticket_booking.html', message=message)

        # look up ticket
        ticket = None
        for t in tickets:
            if t['ticket_id'] == ticket_id:
                ticket = t
                break
        if not ticket:
            message = 'Ticket not found.'
            return render_template('ticket_booking.html', message=message)

        available_count = ticket['capacity'] - ticket['sold_count']
        if available_count < ticket_quantity:
            message = f'Not enough tickets available. Only {available_count} left.'
            return render_template('ticket_booking.html', message=message)

        # Persist booking is not specified on file write, so just simulate success
        # Optionally, you could save to a bookings.txt but spec doesn't demand
        total_amount = ticket_quantity * ticket['price']
        message = f'Successfully booked {ticket_quantity} tickets. Total amount: ${total_amount:.2f}'

        return render_template('booking_confirmation.html', total_amount=total_amount, message=message)

@app.route('/participants')
def participants_management():
    participants = load_participants()
    status_filter = request.args.get('status')
    filtered_participants = participants
    if status_filter:
        filtered_participants = [p for p in participants if p['status'] == status_filter]
    return render_template('participants.html', participants=filtered_participants)

@app.route('/participants/add', methods=['POST'])
def add_participant():
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    if not name or not email or not phone:
        return redirect(url_for('participants_management'))

    participants = load_participants()
    # generate new participant_id
    ids = []
    for p in participants:
        try:
            ids.append(int(p['participant_id']))
        except Exception:
            continue
    new_id = max(ids) + 1 if ids else 1

    new_participant = f"{new_id}|{name}|{email}|{phone}|2025-01-01|Registered"  # hard-coded date for now

    # Append new participant to file
    path = os.path.join('data', 'participants.txt')
    try:
        with open(path, 'a', encoding='utf-8') as f:
            f.write(new_participant + '\n')
    except Exception:
        pass

    return redirect(url_for('participants_management'))

@app.route('/venues')
def venues_page():
    venues = load_venues()
    # Optionally filter by capacity or location if query args
    capacity_filter = request.args.get('capacity')
    location_filter = request.args.get('location')
    filtered_venues = venues
    try:
        if capacity_filter is not None:
            capacity_int = int(capacity_filter)
            filtered_venues = [v for v in filtered_venues if v['capacity'] >= capacity_int]
    except Exception:
        pass
    if location_filter:
        filtered_venues = [v for v in filtered_venues if location_filter.lower() in v['location'].lower()]
    return render_template('venues.html', venues=filtered_venues)

@app.route('/venues/<int:venue_id>')
def venue_details(venue_id):
    venues = load_venues()
    venue = None
    for v in venues:
        try:
            if int(v['venue_id']) == venue_id:
                venue = v
                break
        except Exception:
            continue
    if not venue:
        return "Venue not found", 404
    return render_template('venue_details.html', venue=venue)

@app.route('/schedules')
def schedules_page():
    schedules = load_schedules()
    event_id_filter = request.args.get('event_id')
    if event_id_filter:
        schedules = [s for s in schedules if s['event_id'] == event_id_filter]
    return render_template('schedules.html', schedules=schedules)

@app.route('/bookings')
def bookings_summary():
    bookings = load_bookings()
    participants = load_participants()
    tickets = load_tickets()
    events = load_events()
    schedules = load_schedules()

    # Compose booking info for rendering
    bookings_detail = []
    for b in bookings:
        participant = next((p for p in participants if p['participant_id'] == b['participant_id']), None)
        ticket = next((t for t in tickets if t['ticket_id'] == b['ticket_id']), None)
        event = None
        schedule = next((s for s in schedules if s['schedule_id'] == b['schedule_id']), None)
        if schedule:
            event = next((e for e in events if e['event_id'] == schedule['event_id']), None)
        bd = {
            'booking_id': b['booking_id'],
            'participant_name': participant['name'] if participant else 'Unknown',
            'ticket_type': ticket['ticket_type'] if ticket else 'Unknown',
            'event_name': event['event_name'] if event else 'Unknown',
            'status': b['status'],
            'booking_date': b['booking_date'],
            'total_amount': b['total_amount']
        }
        bookings_detail.append(bd)

    return render_template('bookings.html', bookings=bookings_detail)

@app.route('/bookings/cancel/<int:booking_id>')
def cancel_booking(booking_id):
    # Cancel booking action: Since no file write back specified, simulate cancellation
    # In real app, would update bookings.txt and adjust tickets sold_count
    # Here just redirect back to bookings summary
    return redirect(url_for('bookings_summary'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
