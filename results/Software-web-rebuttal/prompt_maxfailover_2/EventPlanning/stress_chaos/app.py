from flask import Flask, render_template, redirect, url_for, request
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Utility functions to load data files

def load_events():
    events = []
    path = os.path.join(DATA_DIR, 'events.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
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
    except FileNotFoundError:
        pass
    return events


def load_venues():
    venues = []
    path = os.path.join(DATA_DIR, 'venues.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts=line.split('|')
                if len(parts)!=6:
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
    except FileNotFoundError:
        pass
    return venues


def load_tickets():
    tickets = []
    path = os.path.join(DATA_DIR, 'tickets.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts=line.split('|')
                if len(parts)!=6:
                    continue
                ticket={
                    'ticket_id': int(parts[0]),
                    'event_id': int(parts[1]),
                    'ticket_type': parts[2],
                    'price': float(parts[3]),
                    'available_count': int(parts[4]),
                    'sold_count': int(parts[5])
                }
                tickets.append(ticket)
    except FileNotFoundError:
        pass
    return tickets


def load_bookings():
    bookings = []
    path = os.path.join(DATA_DIR, 'bookings.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts=line.split('|')
                if len(parts)!=8:
                    continue
                booking={
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
    except FileNotFoundError:
        pass
    return bookings


def load_participants():
    participants = []
    path = os.path.join(DATA_DIR, 'participants.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts=line.split('|')
                if len(parts)!=7:
                    continue
                participant={
                    'participant_id': int(parts[0]),
                    'event_id': int(parts[1]),
                    'name': parts[2],
                    'email': parts[3],
                    'booking_id': int(parts[4]),
                    'status': parts[5],
                    'registration_date': parts[6]
                }
                participants.append(participant)
    except FileNotFoundError:
        pass
    return participants


def load_schedules():
    schedules = []
    path = os.path.join(DATA_DIR, 'schedules.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts=line.split('|')
                if len(parts)!=7:
                    continue
                schedule={
                    'schedule_id': int(parts[0]),
                    'event_id': int(parts[1]),
                    'session_title': parts[2],
                    'session_time': parts[3],
                    'duration_minutes': int(parts[4]),
                    'speaker': parts[5],
                    'venue_id': int(parts[6])
                }
                schedules.append(schedule)
    except FileNotFoundError:
        pass
    return schedules


# Helper to write back to tickets.txt (used to update availability in booking)
def save_tickets(tickets):
    path = os.path.join(DATA_DIR, 'tickets.txt')
    try:
        with open(path, 'w', encoding='utf-8') as f:
            for t in tickets:
                line = f"{t['ticket_id']}|{t['event_id']}|{t['ticket_type']}|{t['price']}|{t['available_count']}|{t['sold_count']}\n"
                f.write(line)
    except Exception:
        pass

# Helper to write back bookings.txt (for booking add or status update)
def save_bookings(bookings):
    path = os.path.join(DATA_DIR, 'bookings.txt')
    try:
        with open(path, 'w', encoding='utf-8') as f:
            for b in bookings:
                line = f"{b['booking_id']}|{b['event_id']}|{b['customer_name']}|{b['booking_date']}|{b['ticket_count']}|{b['ticket_type']}|{b['total_amount']}|{b['status']}\n"
                f.write(line)
    except Exception:
        pass

# Helper to write back participants.txt (add participant)
def save_participants(participants):
    path = os.path.join(DATA_DIR, 'participants.txt')
    try:
        with open(path, 'w', encoding='utf-8') as f:
            for p in participants:
                line = f"{p['participant_id']}|{p['event_id']}|{p['name']}|{p['email']}|{p['booking_id']}|{p['status']}|{p['registration_date']}\n"
                f.write(line)
    except Exception:
        pass


# Root redirect
@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard_page'))


# /dashboard
@app.route('/dashboard')
def dashboard_page():
    events = load_events()
    # featured_events: subset or first 3 events with selected keys
    featured_events = []
    for e in events[:3]:
        featured_events.append({
            'event_id': e['event_id'],
            'event_name': e['event_name'],
            'date': e['date'],
            'location': e['location']
        })
    return render_template('dashboard.html', featured_events=featured_events)


# /events GET
@app.route('/events', methods=['GET'])
def events_listing():
    events = load_events()
    category_options = ['Conference', 'Concert', 'Sports', 'Workshop', 'Social']
    # Pass all events as is
    events_filtered = [
        {
            'event_id': e['event_id'],
            'event_name': e['event_name'],
            'category': e['category'],
            'date': e['date'],
            'time': e['time'],
            'location': e['location']
        }
        for e in events
    ]
    return render_template('events.html', events=events_filtered, category_options=category_options)


# /events/filter POST
@app.route('/events/filter', methods=['POST'])
def filter_events():
    # Get filter criteria
    search = request.form.get('event_search_input', '').strip().lower()
    category = request.form.get('event_category_filter', '').strip()
    events = load_events()
    category_options = ['Conference', 'Concert', 'Sports', 'Workshop', 'Social']

    filtered = []
    for e in events:
        if category and category != '':
            if e['category'].lower() != category.lower():
                continue
        if search and search != '':
            if search not in e['event_name'].lower() and search not in e['location'].lower():
                continue
        filtered.append({
            'event_id': e['event_id'],
            'event_name': e['event_name'],
            'category': e['category'],
            'date': e['date'],
            'time': e['time'],
            'location': e['location']
        })
    return render_template('events.html', events=filtered, category_options=category_options)


# /events/<int:event_id> GET
@app.route('/events/<int:event_id>', methods=['GET'])
def event_details(event_id):
    events = load_events()
    event = next((e for e in events if e['event_id'] == event_id), None)
    if not event:
        return "Event not found", 404
    return render_template('event_details.html', event=event)


# /book_ticket GET,POST
@app.route('/book_ticket', methods=['GET', 'POST'])
def book_ticket():
    events = load_events()
    events_simple = [{'event_id': e['event_id'], 'event_name': e['event_name']} for e in events]

    if request.method == 'GET':
        return render_template('book_ticket.html', events=events_simple, booking_confirmation=None)

    if request.method == 'POST':
        # Process booking form
        event_id_str = request.form.get('event_id')
        customer_name = request.form.get('customer_name', '').strip()
        ticket_count_str = request.form.get('ticket_count', '').strip()
        ticket_type = request.form.get('ticket_type', '').strip()

        booking_confirmation = {}
        # Validate inputs
        if not event_id_str or not event_id_str.isdigit():
            booking_confirmation['error'] = 'Invalid event selected.'
            return render_template('book_ticket.html', events=events_simple, booking_confirmation=booking_confirmation)
        event_id = int(event_id_str)

        event = next((e for e in events if e['event_id'] == event_id), None)
        if not event:
            booking_confirmation['error'] = 'Event not found.'
            return render_template('book_ticket.html', events=events_simple, booking_confirmation=booking_confirmation)

        if not customer_name:
            booking_confirmation['error'] = 'Customer name required.'
            return render_template('book_ticket.html', events=events_simple, booking_confirmation=booking_confirmation)

        if not ticket_count_str or not ticket_count_str.isdigit():
            booking_confirmation['error'] = 'Invalid ticket count.'
            return render_template('book_ticket.html', events=events_simple, booking_confirmation=booking_confirmation)
        ticket_count = int(ticket_count_str)
        if ticket_count < 1:
            booking_confirmation['error'] = 'Ticket count must be at least 1.'
            return render_template('book_ticket.html', events=events_simple, booking_confirmation=booking_confirmation)

        if ticket_type not in ['General', 'VIP', 'Early Bird']:
            booking_confirmation['error'] = 'Invalid ticket type selected.'
            return render_template('book_ticket.html', events=events_simple, booking_confirmation=booking_confirmation)

        tickets = load_tickets()
        # Find matching ticket
        ticket = next((t for t in tickets if t['event_id'] == event_id and t['ticket_type'] == ticket_type), None)
        if not ticket:
            booking_confirmation['error'] = 'Selected ticket type not available for this event.'
            return render_template('book_ticket.html', events=events_simple, booking_confirmation=booking_confirmation)

        if ticket['available_count'] < ticket_count:
            booking_confirmation['error'] = f'Only {ticket["available_count"]} tickets available for selected type.'
            return render_template('book_ticket.html', events=events_simple, booking_confirmation=booking_confirmation)

        # Calculate total
        total_amount = ticket['price'] * ticket_count

        bookings = load_bookings()
        new_booking_id = max([b['booking_id'] for b in bookings], default=0) + 1

        today_str = datetime.now().strftime('%Y-%m-%d')

        new_booking = {
            'booking_id': new_booking_id,
            'event_id': event_id,
            'customer_name': customer_name,
            'booking_date': today_str,
            'ticket_count': ticket_count,
            'ticket_type': ticket_type,
            'total_amount': total_amount,
            'status': 'Confirmed'
        }

        bookings.append(new_booking)

        # Update ticket availability
        for t in tickets:
            if t['ticket_id'] == ticket['ticket_id']:
                t['available_count'] -= ticket_count
                t['sold_count'] += ticket_count
                break

        save_bookings(bookings)
        save_tickets(tickets)

        booking_confirmation = {
            'success': True,
            'booking_id': new_booking_id,
            'event_name': event['event_name'],
            'customer_name': customer_name,
            'ticket_count': ticket_count,
            'ticket_type': ticket_type,
            'total_amount': total_amount
        }

        return render_template('book_ticket.html', events=events_simple, booking_confirmation=booking_confirmation)


# /participants GET
@app.route('/participants', methods=['GET'])
def participants_management():
    participants = load_participants()
    status_options = ['Registered', 'Confirmed', 'Attended']

    participants_simple = [
        {
            'participant_id': p['participant_id'],
            'event_id': p['event_id'],
            'name': p['name'],
            'email': p['email'],
            'booking_id': p['booking_id'],
            'status': p['status'],
            'registration_date': p['registration_date']
        }
        for p in participants
    ]
    return render_template('participants.html', participants=participants_simple, status_options=status_options)


# /participants/filter POST
@app.route('/participants/filter', methods=['POST'])
def filter_participants():
    search = request.form.get('search_participant_input', '').strip().lower()
    status_filter = request.form.get('participant_status_filter', '').strip()

    participants = load_participants()
    status_options = ['Registered', 'Confirmed', 'Attended']

    filtered = []
    for p in participants:
        if status_filter and status_filter != '':
            if p['status'].lower() != status_filter.lower():
                continue
        if search and search != '':
            if search not in p['name'].lower() and search not in p['email'].lower():
                continue
        filtered.append({
            'participant_id': p['participant_id'],
            'event_id': p['event_id'],
            'name': p['name'],
            'email': p['email'],
            'booking_id': p['booking_id'],
            'status': p['status'],
            'registration_date': p['registration_date']
        })
    return render_template('participants.html', participants=filtered, status_options=status_options)


# /participants/add POST
@app.route('/participants/add', methods=['POST'])
def add_participant():
    # Expect form data: event_id, name, email, booking_id, status
    try:
        event_id_str = request.form.get('event_id')
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        booking_id_str = request.form.get('booking_id')
        status = request.form.get('status', '').strip()

        if not event_id_str or not event_id_str.isdigit():
            return redirect(url_for('participants_management'))
        event_id = int(event_id_str)

        if not booking_id_str or not booking_id_str.isdigit():
            booking_id = 0  # Set 0 if invalid
        else:
            booking_id = int(booking_id_str)

        if not name or not email or not status:
            return redirect(url_for('participants_management'))

        participants = load_participants()
        new_id = max([p['participant_id'] for p in participants], default=0) + 1
        registration_date = datetime.now().strftime('%Y-%m-%d')

        new_participant = {
            'participant_id': new_id,
            'event_id': event_id,
            'name': name,
            'email': email,
            'booking_id': booking_id,
            'status': status,
            'registration_date': registration_date
        }

        participants.append(new_participant)
        save_participants(participants)
    except Exception:
        # Fail silently and redirect
        pass
    return redirect(url_for('participants_management'))


# /venues GET
@app.route('/venues', methods=['GET'])
def venues_page():
    venues = load_venues()
    capacity_options = ['Small', 'Medium', 'Large']
    venues_simple = [
        {
            'venue_id': v['venue_id'],
            'venue_name': v['venue_name'],
            'location': v['location'],
            'capacity': v['capacity'],
            'amenities': v['amenities']
        }
        for v in venues
    ]
    return render_template('venues.html', venues=venues_simple, capacity_options=capacity_options)


# /venues/filter POST
@app.route('/venues/filter', methods=['POST'])
def filter_venues():
    search = request.form.get('venue_search_input', '').strip().lower()
    capacity_filter = request.form.get('venue_capacity_filter', '').strip()

    venues = load_venues()
    capacity_options = ['Small', 'Medium', 'Large']

    # Define capacity ranges (assume Small: <=500, Medium: >500 and <=1000, Large: >1000) for filtering
    def capacity_category(cap):
        if cap <= 500:
            return 'Small'
        elif cap <= 1000:
            return 'Medium'
        else:
            return 'Large'

    filtered = []
    for v in venues:
        if capacity_filter and capacity_filter != '':
            if capacity_category(v['capacity']).lower() != capacity_filter.lower():
                continue
        if search and search != '':
            if search not in v['venue_name'].lower() and search not in v['location'].lower():
                continue
        filtered.append({
            'venue_id': v['venue_id'],
            'venue_name': v['venue_name'],
            'location': v['location'],
            'capacity': v['capacity'],
            'amenities': v['amenities']
        })
    return render_template('venues.html', venues=filtered, capacity_options=capacity_options)


# /schedules GET
@app.route('/schedules', methods=['GET'])
def event_schedules():
    schedules = load_schedules()
    events = load_events()

    # Prepare schedules with required keys
    schedules_simple = [
        {
            'schedule_id': s['schedule_id'],
            'event_id': s['event_id'],
            'session_title': s['session_title'],
            'session_time': s['session_time'],
            'duration_minutes': s['duration_minutes'],
            'speaker': s['speaker'],
            'venue_id': s['venue_id']
        }
        for s in schedules
    ]

    events_simple = [{'event_id': e['event_id'], 'event_name': e['event_name']} for e in events]

    return render_template('schedules.html', schedules=schedules_simple, events=events_simple)


# /schedules/filter POST
@app.route('/schedules/filter', methods=['POST'])
def filter_schedules():
    date_filter = request.form.get('schedule_filter_date', '').strip()
    event_filter = request.form.get('schedule_filter_event', '').strip()

    schedules = load_schedules()
    events = load_events()

    filtered = []

    for s in schedules:
        # Check event id filter
        if event_filter:
            try:
                event_filter_int = int(event_filter)
                if s['event_id'] != event_filter_int:
                    continue
            except:
                # ignore invalid
                pass

        # Check date filter (YYYY-MM-DD) matches session_time date portion
        if date_filter:
            try:
                session_date = s['session_time'].split(' ')[0]
                if session_date != date_filter:
                    continue
            except:
                pass

        filtered.append({
            'schedule_id': s['schedule_id'],
            'event_id': s['event_id'],
            'session_title': s['session_title'],
            'session_time': s['session_time'],
            'duration_minutes': s['duration_minutes'],
            'speaker': s['speaker'],
            'venue_id': s['venue_id']
        })

    events_simple = [{'event_id': e['event_id'], 'event_name': e['event_name']} for e in events]

    return render_template('schedules.html', schedules=filtered, events=events_simple)


# /bookings GET
@app.route('/bookings', methods=['GET'])
def bookings_summary():
    bookings = load_bookings()
    events = load_events()

    # Enhance bookings with event_name and date
    events_dict = {e['event_id']: e for e in events}

    bookings_list = []
    for b in bookings:
        event = events_dict.get(b['event_id'])
        if not event:
            continue
        bookings_list.append({
            'booking_id': b['booking_id'],
            'event_id': b['event_id'],
            'event_name': event['event_name'],
            'date': event['date'],
            'ticket_count': b['ticket_count'],
            'status': b['status'],
            'ticket_type': b['ticket_type']
        })

    return render_template('bookings.html', bookings=bookings_list)


# /bookings/cancel/<int:booking_id> POST
@app.route('/bookings/cancel/<int:booking_id>', methods=['POST'])
def cancel_booking(booking_id):
    bookings = load_bookings()
    tickets = load_tickets()

    booking_to_cancel = next((b for b in bookings if b['booking_id'] == booking_id), None)
    if not booking_to_cancel:
        return redirect(url_for('bookings_summary'))

    # Only cancel if status is not already cancelled
    if booking_to_cancel['status'].lower() != 'cancelled':
        # Update status
        booking_to_cancel['status'] = 'Cancelled'

        # Update tickets availability to add back the cancelled count
        for t in tickets:
            if t['event_id'] == booking_to_cancel['event_id'] and t['ticket_type'] == booking_to_cancel['ticket_type']:
                t['available_count'] += booking_to_cancel['ticket_count']
                t['sold_count'] -= booking_to_cancel['ticket_count']
                if t['sold_count'] < 0:
                    t['sold_count'] = 0
                break

        save_bookings(bookings)
        save_tickets(tickets)

    return redirect(url_for('bookings_summary'))


if __name__ == '__main__':
    app.run(debug=True, port=5000)
