from flask import Flask, request, render_template, redirect, url_for, abort
from datetime import datetime
import os

app = Flask(__name__)

DATA_DIR = 'data'

# Helper functions to read and write data files with specified schema

def read_events():
    events = []
    path = os.path.join(DATA_DIR, 'events.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 9:
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


def read_venues():
    venues = []
    path = os.path.join(DATA_DIR, 'venues.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 6:
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


def read_tickets():
    tickets = []
    path = os.path.join(DATA_DIR, 'tickets.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 6:
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
    return tickets


def write_tickets(tickets):
    path = os.path.join(DATA_DIR, 'tickets.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for t in tickets:
            line = f"{t['ticket_id']}|{t['event_id']}|{t['ticket_type']}|{t['price']}|{t['available_count']}|{t['sold_count']}\n"
            f.write(line)


def read_bookings():
    bookings = []
    path = os.path.join(DATA_DIR, 'bookings.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 8:
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


def write_bookings(bookings):
    path = os.path.join(DATA_DIR, 'bookings.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for b in bookings:
            line = f"{b['booking_id']}|{b['event_id']}|{b['customer_name']}|{b['booking_date']}|{b['ticket_count']}|{b['ticket_type']}|{b['total_amount']}|{b['status']}\n"
            f.write(line)


def read_participants():
    participants = []
    path = os.path.join(DATA_DIR, 'participants.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 7:
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


def read_schedules():
    schedules = []
    path = os.path.join(DATA_DIR, 'schedules.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 7:
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


# Section 1: Flask Backend Routes

# 1. Dashboard Page
@app.route('/')
def dashboard():
    events = read_events()
    venues = read_venues()
    # Featured events - let's take first 5 sorted by date ascending
    sorted_events = sorted(events, key=lambda e: e['date'])
    featured_events = [{
        'event_id': e['event_id'],
        'event_name': e['event_name'],
        'date': e['date'],
        'location': e['location'],
        'description': e['description']
    } for e in sorted_events[:5]]

    # Featured venues - first 5 by capacity descending
    sorted_venues = sorted(venues, key=lambda v: v['capacity'], reverse=True)
    featured_venues = [{
        'venue_id': v['venue_id'],
        'venue_name': v['venue_name'],
        'location': v['location'],
        'capacity': v['capacity'],
        'amenities': v['amenities']
    } for v in sorted_venues[:5]]

    return render_template('dashboard.html', featured_events=featured_events, featured_venues=featured_venues)


# 2. Events Listing Page
@app.route('/events')
def events_listing():
    events = read_events()
    categories = ["Conference", "Concert", "Sports", "Workshop", "Social"]

    search = request.args.get('search', '').strip().lower()
    category_filter = request.args.get('category', '').strip()

    filtered_events = events

    if search:
        filtered_events = [e for e in filtered_events if search in e['event_name'].lower() or search in e['location'].lower() or search in e['date']]

    if category_filter and category_filter in categories:
        filtered_events = [e for e in filtered_events if e['category'] == category_filter]

    return render_template('events.html', events=filtered_events, categories=categories)


# 3. Event Details Page
@app.route('/events/<int:event_id>')
def event_details(event_id):
    events = read_events()
    venues = read_venues()

    event = next((e for e in events if e['event_id'] == event_id), None)
    if event is None:
        abort(404)

    venue = next((v for v in venues if v['venue_id'] == event['venue_id']), None)

    return render_template('event_details.html', event=event, venue=venue)


# 4. Ticket Booking Page
@app.route('/bookings/new', methods=['GET', 'POST'])
def ticket_booking_form():
    if request.method == 'GET':
        events = read_events()
        tickets = read_tickets()
        events_simple = [{'event_id': e['event_id'], 'event_name': e['event_name']} for e in events]
        ticket_types = ["General", "VIP", "Early Bird"]
        return render_template('ticket_booking.html', events=events_simple, ticket_types=ticket_types)

    elif request.method == 'POST':
        form = request.form
        try:
            event_id = int(form.get('event_id', ''))
            ticket_type = form.get('ticket_type', '')
            ticket_count = int(form.get('ticket_count', ''))
            customer_name = form.get('customer_name', '').strip()
        except Exception:
            return 'Invalid input data', 400

        if ticket_count < 1:
            return 'Ticket count must be at least 1', 400

        if not customer_name:
            return 'Customer name is required', 400

        # Validate event
        events = read_events()
        event = next((e for e in events if e['event_id'] == event_id), None)
        if event is None:
            return 'Event not found', 404

        # Validate ticket_type
        ticket_types = ["General", "VIP", "Early Bird"]
        if ticket_type not in ticket_types:
            return 'Invalid ticket type', 400

        # Check ticket availability
        tickets = read_tickets()
        ticket = next((t for t in tickets if t['event_id'] == event_id and t['ticket_type'] == ticket_type), None)
        if ticket is None:
            return 'Ticket type not available for this event', 400

        available_remaining = ticket['available_count'] - ticket['sold_count']
        if ticket_count > available_remaining:
            return f'Not enough tickets available. Only {available_remaining} left.', 400

        # Proceed with booking
        bookings = read_bookings()
        next_booking_id = max((b['booking_id'] for b in bookings), default=0) + 1

        total_amount = ticket_count * ticket['price']
        booking_date = datetime.now().strftime('%Y-%m-%d')

        new_booking = {
            'booking_id': next_booking_id,
            'event_id': event_id,
            'customer_name': customer_name,
            'booking_date': booking_date,
            'ticket_count': ticket_count,
            'ticket_type': ticket_type,
            'total_amount': total_amount,
            'status': 'Confirmed'
        }

        bookings.append(new_booking)

        # Update sold_count in tickets
        for t in tickets:
            if t['ticket_id'] == ticket['ticket_id']:
                t['sold_count'] += ticket_count
                break

        write_bookings(bookings)
        write_tickets(tickets)

        # Show confirmation on the same page after POST (template expected to handle confirmation display)
        events_simple = [{'event_id': e['event_id'], 'event_name': e['event_name']} for e in events]
        ticket_types = ["General", "VIP", "Early Bird"]
        confirmation_msg = f"Booking successful! Booking ID: {next_booking_id}, Total Amount: ${total_amount:.2f}"
        return render_template('ticket_booking.html', events=events_simple, ticket_types=ticket_types, booking_confirmation=confirmation_msg)


# 5. Participants Management Page
@app.route('/participants')
def participants_management():
    participants = read_participants()
    status_options = ["Registered", "Confirmed", "Attended"]

    search = request.args.get('search', '').strip().lower()
    status_filter = request.args.get('status', '')

    filtered_participants = participants
    if search:
        filtered_participants = [p for p in filtered_participants if search in p['name'].lower() or search in p['email'].lower()]

    if status_filter and status_filter in status_options:
        filtered_participants = [p for p in filtered_participants if p['status'] == status_filter]

    return render_template('participants.html', participants=filtered_participants, status_options=status_options)


# 6. Venue Information Page
@app.route('/venues')
def venues_listing():
    venues = read_venues()
    capacity_filters = ['Small', 'Medium', 'Large']

    search = request.args.get('search', '').strip().lower()
    capacity_filter = request.args.get('capacity', '')

    filtered_venues = venues

    if search:
        filtered_venues = [v for v in filtered_venues if search in v['venue_name'].lower() or search in v['location'].lower()]

    if capacity_filter:
        if capacity_filter == 'Small':
            filtered_venues = [v for v in filtered_venues if v['capacity'] < 100]
        elif capacity_filter == 'Medium':
            filtered_venues = [v for v in filtered_venues if 100 <= v['capacity'] <= 500]
        elif capacity_filter == 'Large':
            filtered_venues = [v for v in filtered_venues if v['capacity'] > 500]

    return render_template('venues.html', venues=filtered_venues, capacity_filters=capacity_filters)


# 7. Event Schedules Page
@app.route('/schedules')
def schedules_page():
    schedules = read_schedules()
    events = read_events()

    date_filter = request.args.get('date', '').strip()
    event_id_filter = request.args.get('event_id', '').strip()

    filtered_schedules = schedules

    if date_filter:
        filtered_schedules = [s for s in filtered_schedules if s['session_time'].startswith(date_filter)]

    if event_id_filter.isdigit():
        event_id_f = int(event_id_filter)
        filtered_schedules = [s for s in filtered_schedules if s['event_id'] == event_id_f]

    events_simple = [{'event_id': e['event_id'], 'event_name': e['event_name']} for e in events]

    return render_template('schedules.html', schedules=filtered_schedules, events=events_simple)


# 8. Bookings Summary Page
@app.route('/bookings')
def bookings_summary():
    bookings = read_bookings()
    events = read_events()
    search_query = request.args.get('search', '').strip().lower()

    # Join bookings with event names
    events_dict = {e['event_id']: e['event_name'].lower() for e in events}

    filtered_bookings = bookings
    if search_query:
        filtered_bookings = [b for b in filtered_bookings if search_query in events_dict.get(b['event_id'], '') or search_query in str(b['booking_id'])]

    return render_template('bookings.html', bookings=filtered_bookings, search_query=search_query)


# Optional POST route for canceling a booking
@app.route('/bookings/cancel/<int:booking_id>', methods=['POST'])
def cancel_booking(booking_id):
    bookings = read_bookings()
    booking = next((b for b in bookings if b['booking_id'] == booking_id), None)
    if not booking:
        return 'Booking not found', 404

    if booking['status'] == 'Cancelled':
        return 'Booking is already cancelled', 400

    booking['status'] = 'Cancelled'

    # Optionally, decrement sold_count in tickets for the canceled booking
    tickets = read_tickets()
    for t in tickets:
        if t['event_id'] == booking['event_id'] and t['ticket_type'] == booking['ticket_type']:
            t['sold_count'] = max(0, t['sold_count'] - booking['ticket_count'])
            break

    write_bookings(bookings)
    write_tickets(tickets)

    return redirect(url_for('bookings_summary'))


if __name__ == '__main__':
    app.run(debug=True)
