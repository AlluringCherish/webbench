from flask import Flask, render_template, redirect, url_for, request
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

# Data loading helper functions

def load_events():
    events = []
    try:
        with open('data/events.txt', 'r', encoding='utf-8') as f:
            for line in f:
                if not line.strip():
                    continue
                parts = line.strip().split('|')
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
    except Exception:
        pass
    return events


def load_venues():
    venues = []
    try:
        with open('data/venues.txt', 'r', encoding='utf-8') as f:
            for line in f:
                if not line.strip():
                    continue
                parts = line.strip().split('|')
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
    except Exception:
        pass
    return venues


def load_tickets():
    tickets = []
    try:
        with open('data/tickets.txt', 'r', encoding='utf-8') as f:
            for line in f:
                if not line.strip():
                    continue
                parts = line.strip().split('|')
                if len(parts) < 6:
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
    try:
        with open('data/bookings.txt', 'r', encoding='utf-8') as f:
            for line in f:
                if not line.strip():
                    continue
                parts = line.strip().split('|')
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
    except Exception:
        pass
    return bookings


def load_participants():
    participants = []
    try:
        with open('data/participants.txt', 'r', encoding='utf-8') as f:
            for line in f:
                if not line.strip():
                    continue
                parts = line.strip().split('|')
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
    except Exception:
        pass
    return participants


def load_schedules():
    schedules = []
    try:
        with open('data/schedules.txt', 'r', encoding='utf-8') as f:
            for line in f:
                if not line.strip():
                    continue
                parts = line.strip().split('|')
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
    except Exception:
        pass
    return schedules


# Helper to write bookings back to file (used for booking and canceling)
def save_bookings(bookings):
    try:
        with open('data/bookings.txt', 'w', encoding='utf-8') as f:
            for b in bookings:
                line = f"{b['booking_id']}|{b['event_id']}|{b['customer_name']}|{b['booking_date']}|{b['ticket_count']}|{b['ticket_type']}|{b['total_amount']}|{b['status']}\n"
                f.write(line)
    except Exception:
        pass

# Helper to write tickets back to file (used to update available_count and sold_count)
def save_tickets(tickets):
    try:
        with open('data/tickets.txt', 'w', encoding='utf-8') as f:
            for t in tickets:
                line = f"{t['ticket_id']}|{t['event_id']}|{t['ticket_type']}|{t['price']}|{t['available_count']}|{t['sold_count']}\n"
                f.write(line)
    except Exception:
        pass


# Route Implementations

@app.route('/')
def redirect_to_dashboard():
    return redirect(url_for('dashboard_page'))


@app.route('/dashboard')
def dashboard_page():
    events = load_events()
    # For featured_events, pick upcoming or close events (for simplicity, first 5 sorted by date ascending)
    try:
        events_sorted = sorted(events, key=lambda e: e['date'])
    except Exception:
        events_sorted = events
    featured_events = []
    for e in events_sorted[:5]:
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
    categories = ["Conference", "Concert", "Sports", "Workshop", "Social"]

    search_query = request.args.get('search_query', '').strip()
    category_filter = request.args.get('category_filter', '').strip()

    filtered_events = events

    if search_query:
        filtered_events = [e for e in filtered_events if search_query.lower() in e['event_name'].lower()]
    if category_filter and category_filter in categories:
        filtered_events = [e for e in filtered_events if e['category'] == category_filter]

    # Map to expected event dict with required keys
    events_context = []
    for e in filtered_events:
        events_context.append({
            'event_id': e['event_id'],
            'event_name': e['event_name'],
            'category': e['category'],
            'date': e['date'],
            'location': e['location']
        })

    return render_template('events.html', events=events_context, categories=categories, search_query=search_query, category_filter=category_filter)


@app.route('/event/<int:event_id>')
def event_details(event_id):
    events = load_events()
    event = None
    for e in events:
        if e['event_id'] == event_id:
            event = {
                'event_id': e['event_id'],
                'event_name': e['event_name'],
                'date': e['date'],
                'time': e['time'],
                'location': e['location'],
                'description': e['description'],
                'venue_id': e['venue_id'],
                'capacity': e['capacity']
            }
            break
    if event is None:
        # Could 404 or redirect
        return redirect(url_for('events_listing'))
    return render_template('event_details.html', event=event)


@app.route('/book_ticket', methods=['GET'])
def book_ticket_page():
    events = load_events()
    events_simple = [{'event_id': e['event_id'], 'event_name': e['event_name']} for e in events]
    return render_template('ticket_booking.html', events=events_simple)


@app.route('/book_ticket', methods=['POST'])
def process_ticket_booking():
    events = load_events()
    tickets = load_tickets()
    bookings = load_bookings()

    event_id_str = request.form.get('event_id', '')
    ticket_type = request.form.get('ticket_type', '').strip()
    ticket_count_str = request.form.get('ticket_count', '')
    customer_name = request.form.get('customer_name', '').strip()

    error_message = None
    confirmation = None

    # Validate inputs
    try:
        event_id = int(event_id_str)
        ticket_count = int(ticket_count_str)
        if ticket_count <= 0:
            error_message = 'Ticket count must be positive.'
    except Exception:
        error_message = 'Invalid event or ticket count.'

    event = None
    for e in events:
        if e['event_id'] == event_id:
            event = e
            break
    if event is None:
        error_message = 'Selected event does not exist.'

    if not ticket_type:
        error_message = 'Ticket type is required.'

    if not customer_name:
        error_message = 'Customer name is required.'

    # Find matching ticket
    matching_ticket = None
    if not error_message:
        for t in tickets:
            if t['event_id'] == event_id and t['ticket_type'].lower() == ticket_type.lower():
                matching_ticket = t
                break

        if matching_ticket is None:
            error_message = 'Ticket type not found for selected event.'

    # Check availability
    if not error_message and matching_ticket['available_count'] < ticket_count:
        error_message = f'Only {matching_ticket["available_count"]} tickets available for selected type.'

    if error_message:
        # Return error on booking page with events dropdown
        events_simple = [{'event_id': e['event_id'], 'event_name': e['event_name']} for e in events]
        return render_template('ticket_booking.html', events=events_simple, error_message=error_message)

    # Calculate total amount
    total_amount = matching_ticket['price'] * ticket_count

    # Create new booking id
    new_booking_id = 1
    existing_ids = [b['booking_id'] for b in bookings]
    if existing_ids:
        new_booking_id = max(existing_ids) + 1

    booking_date_str = datetime.now().strftime('%Y-%m-%d')
    new_booking = {
        'booking_id': new_booking_id,
        'event_id': event_id,
        'customer_name': customer_name,
        'booking_date': booking_date_str,
        'ticket_count': ticket_count,
        'ticket_type': matching_ticket['ticket_type'],
        'total_amount': total_amount,
        'status': 'Confirmed'
    }

    # Update tickets availability
    for t in tickets:
        if t['ticket_id'] == matching_ticket['ticket_id']:
            t['available_count'] -= ticket_count
            t['sold_count'] += ticket_count
            break

    # Save updated tickets and bookings
    bookings.append(new_booking)
    save_tickets(tickets)
    save_bookings(bookings)

    confirmation = {
        'booking_id': new_booking_id,
        'event_name': event['event_name'],
        'ticket_count': ticket_count,
        'ticket_type': matching_ticket['ticket_type'],
        'total_amount': total_amount
    }

    return render_template('ticket_booking.html', events=[{'event_id': e['event_id'], 'event_name': e['event_name']} for e in events], confirmation=confirmation)


@app.route('/participants')
def participants_management():
    participants = load_participants()
    events = load_events()

    status_filter = request.args.get('status_filter', '').strip()
    search_query = request.args.get('search_query', '').strip()

    # Create a map of event_id to event_name
    event_map = {e['event_id']: e['event_name'] for e in events}

    filtered_participants = participants

    if search_query:
        filtered_participants = [p for p in filtered_participants if search_query.lower() in p['name'].lower()]

    if status_filter:
        filtered_participants = [p for p in filtered_participants if p['status'] == status_filter]

    participants_context = []
    for p in filtered_participants:
        ename = event_map.get(p['event_id'], 'Unknown Event')
        participants_context.append({
            'participant_id': p['participant_id'],
            'event_name': ename,
            'name': p['name'],
            'email': p['email'],
            'status': p['status']
        })

    return render_template('participants.html', participants=participants_context, status_filter=status_filter, search_query=search_query)


@app.route('/add_participant', methods=['POST'])
def add_participant():
    participants = load_participants()
    bookings = load_bookings()

    event_id_str = request.form.get('event_id', '')
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()
    booking_id_str = request.form.get('booking_id', '')
    status = request.form.get('status', '').strip()

    error_message = None

    try:
        event_id = int(event_id_str)
    except Exception:
        error_message = 'Invalid event ID.'

    try:
        booking_id = int(booking_id_str)
    except Exception:
        error_message = 'Invalid booking ID.'

    if not name:
        error_message = 'Name is required.'
    if not email:
        error_message = 'Email is required.'
    if not status:
        error_message = 'Status is required.'

    if error_message:
        # Could return JSON or redirect with error (spec not specified on page)
        return {'error_message': error_message}, 400

    # Check booking exists
    booking_exists = any(b['booking_id'] == booking_id and b['event_id'] == event_id for b in bookings)
    if not booking_exists:
        return {'error_message': 'Booking does not exist for participant.'}, 400

    # Generate new participant id
    new_participant_id = 1
    existing_ids = [p['participant_id'] for p in participants]
    if existing_ids:
        new_participant_id = max(existing_ids) + 1

    registration_date = datetime.now().strftime('%Y-%m-%d')

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

    # Save participants
    try:
        with open('data/participants.txt', 'w', encoding='utf-8') as f:
            for p in participants:
                line = f"{p['participant_id']}|{p['event_id']}|{p['name']}|{p['email']}|{p['booking_id']}|{p['status']}|{p['registration_date']}\n"
                f.write(line)
    except Exception:
        return {'error_message': 'Failed to save participant data.'}, 500

    return redirect(url_for('participants_management'))


@app.route('/venues')
def venues_page():
    venues = load_venues()

    capacity_filter = request.args.get('capacity_filter', '').strip()
    search_query = request.args.get('search_query', '').strip()

    filtered_venues = venues

    if search_query:
        filtered_venues = [v for v in filtered_venues if search_query.lower() in v['venue_name'].lower() or search_query.lower() in v['location'].lower()]

    if capacity_filter:
        try:
            cap_filter_val = int(capacity_filter)
            filtered_venues = [v for v in filtered_venues if v['capacity'] >= cap_filter_val]
        except Exception:
            pass

    venues_context = []
    for v in filtered_venues:
        venues_context.append({
            'venue_id': v['venue_id'],
            'venue_name': v['venue_name'],
            'location': v['location'],
            'capacity': v['capacity']
        })

    return render_template('venues.html', venues=venues_context, capacity_filter=capacity_filter, search_query=search_query)


@app.route('/event_schedules')
def event_schedules():
    schedules = load_schedules()
    events = load_events()
    venues = load_venues()

    filter_date = request.args.get('filter_date', '').strip()
    event_filter = request.args.get('event_filter', '').strip()

    # Create maps for event_name and venue_name
    event_map = {e['event_id']: e['event_name'] for e in events}
    venue_map = {v['venue_id']: v['venue_name'] for v in venues}

    filtered_schedules = schedules

    if filter_date:
        # Filter schedules by session_time date part
        filtered_schedules = [s for s in filtered_schedules if s['session_time'][:10] == filter_date]

    if event_filter:
        # Find event_id by event_filter string (event name)
        event_ids = [e['event_id'] for e in events if e['event_name'] == event_filter]
        if event_ids:
            filtered_schedules = [s for s in filtered_schedules if s['event_id'] in event_ids]
        else:
            filtered_schedules = []

    schedules_context = []
    for s in filtered_schedules:
        schedules_context.append({
            'schedule_id': s['schedule_id'],
            'event_name': event_map.get(s['event_id'], 'Unknown Event'),
            'session_title': s['session_title'],
            'session_time': s['session_time'],
            'duration_minutes': s['duration_minutes'],
            'speaker': s['speaker'],
            'venue_name': venue_map.get(s['venue_id'], 'Unknown Venue')
        })

    return render_template('schedules.html', schedules=schedules_context, filter_date=filter_date, event_filter=event_filter)


@app.route('/bookings')
def bookings_summary():
    bookings = load_bookings()
    events = load_events()

    search_query = request.args.get('search_query', '').strip()

    event_map = {e['event_id']: e['event_name'] for e in events}

    filtered_bookings = bookings

    if search_query:
        filtered_bookings = [b for b in filtered_bookings if search_query.lower() in event_map.get(b['event_id'], '').lower()]

    bookings_context = []
    for b in filtered_bookings:
        bookings_context.append({
            'booking_id': b['booking_id'],
            'event_name': event_map.get(b['event_id'], 'Unknown Event'),
            'date': b['booking_date'],
            'ticket_count': b['ticket_count'],
            'status': b['status']
        })

    return render_template('bookings.html', bookings=bookings_context, search_query=search_query)


@app.route('/cancel_booking/<int:booking_id>', methods=['POST'])
def cancel_booking(booking_id):
    bookings = load_bookings()
    tickets = load_tickets()

    # Find booking
    booking = None
    for b in bookings:
        if b['booking_id'] == booking_id:
            booking = b
            break

    if booking:
        # Set booking status to Cancelled
        booking['status'] = 'Cancelled'

        # Revert tickets sold_count and available_count
        for t in tickets:
            if t['event_id'] == booking['event_id'] and t['ticket_type'].lower() == booking['ticket_type'].lower():
                t['available_count'] += booking['ticket_count']
                t['sold_count'] -= booking['ticket_count']
                break

        save_bookings(bookings)
        save_tickets(tickets)

    return redirect(url_for('bookings_summary'))


if __name__ == '__main__':
    app.run(debug=True, port=5000)
