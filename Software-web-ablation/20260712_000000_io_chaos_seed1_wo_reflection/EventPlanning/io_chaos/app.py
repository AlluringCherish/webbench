from flask import Flask, render_template, redirect, url_for, request
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Helper functions to load data files

def load_events():
    events = []
    try:
        with open(os.path.join(DATA_DIR, 'events.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 9:
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
        # ignore file errors
        pass
    return events


def load_venues():
    venues = []
    try:
        with open(os.path.join(DATA_DIR, 'venues.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 6:
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
        with open(os.path.join(DATA_DIR, 'tickets.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 6:
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
        with open(os.path.join(DATA_DIR, 'bookings.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 8:
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
        with open(os.path.join(DATA_DIR, 'participants.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 7:
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
        with open(os.path.join(DATA_DIR, 'schedules.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 7:
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


# Save bookings back to file

def save_bookings(bookings):
    try:
        with open(os.path.join(DATA_DIR, 'bookings.txt'), 'w', encoding='utf-8') as f:
            for b in bookings:
                line = f"{b['booking_id']}|{b['event_id']}|{b['customer_name']}|{b['booking_date']}|{b['ticket_count']}|{b['ticket_type']}|{b['total_amount']}|{b['status']}\n"
                f.write(line)
    except Exception:
        pass


# Save participants back to file

def save_participants(participants):
    try:
        with open(os.path.join(DATA_DIR, 'participants.txt'), 'w', encoding='utf-8') as f:
            for p in participants:
                line = f"{p['participant_id']}|{p['event_id']}|{p['name']}|{p['email']}|{p['booking_id']}|{p['status']}|{p['registration_date']}\n"
                f.write(line)
    except Exception:
        pass


# Save tickets back to file

def save_tickets(tickets):
    try:
        with open(os.path.join(DATA_DIR, 'tickets.txt'), 'w', encoding='utf-8') as f:
            for t in tickets:
                line = f"{t['ticket_id']}|{t['event_id']}|{t['ticket_type']}|{t['price']}|{t['available_count']}|{t['sold_count']}\n"
                f.write(line)
    except Exception:
        pass


# Root redirect
@app.route('/')
def redirect_to_dashboard():
    return redirect(url_for('dashboard_page'))


# Dashboard
@app.route('/dashboard')
def dashboard_page():
    events = load_events()
    # Featured events could be the first 5 sorted by date
    featured_events = []
    # Sort by date ascending
    events_sorted = sorted(events, key=lambda e: e['date'])
    for e in events_sorted[:5]:
        featured_events.append({
            'event_id': e['event_id'],
            'event_name': e['event_name'],
            'date': e['date'],
            'location': e['location']
        })
    return render_template('dashboard.html', featured_events=featured_events)


# Events Listing
@app.route('/events', methods=['GET'])
def events_listing():
    events = load_events()
    # Provide list of events with specified keys
    events_list = []
    for ev in events:
        events_list.append({
            'event_id': ev['event_id'],
            'event_name': ev['event_name'],
            'category': ev['category'],
            'date': ev['date'],
            'time': ev['time'],
            'location': ev['location']
        })
    return render_template('events.html', events=events_list)


# Events Search
@app.route('/events/search', methods=['POST'])
def events_search():
    search_term = request.form.get('search_term', '').strip().lower()
    category_filter = request.form.get('category_filter', '').strip()

    events = load_events()
    filtered_events = []

    for ev in events:
        # Filter by category if given and non-empty, else accept
        category_match = (category_filter == '' or ev['category'].lower() == category_filter.lower())

        # Search term in name, location or date
        search_match = (search_term == '' or
                        search_term in ev['event_name'].lower() or
                        search_term in ev['location'].lower() or
                        search_term in ev['date'].lower())

        if category_match and search_match:
            filtered_events.append({
                'event_id': ev['event_id'],
                'event_name': ev['event_name'],
                'category': ev['category'],
                'date': ev['date'],
                'time': ev['time'],
                'location': ev['location']
            })

    return render_template('events.html', events=filtered_events)


# Event Details View
@app.route('/event/<int:event_id>', methods=['GET'])
def event_details(event_id):
    events = load_events()
    event = None
    for ev in events:
        if ev['event_id'] == event_id:
            event = {
                'event_id': ev['event_id'],
                'event_name': ev['event_name'],
                'category': ev['category'],
                'date': ev['date'],
                'time': ev['time'],
                'location': ev['location'],
                'description': ev['description']
            }
            break
    if event is None:
        return "Event not found", 404
    return render_template('event_details.html', event=event)


# Ticket Booking
@app.route('/book_ticket', methods=['GET', 'POST'])
def ticket_booking():
    events = load_events()
    tickets = load_tickets()
    if request.method == 'GET':
        # Provide event_id and event_name for dropdown
        events_list = [{'event_id': e['event_id'], 'event_name': e['event_name']} for e in events]
        return render_template('ticket_booking.html', events=events_list)

    if request.method == 'POST':
        event_id = int(request.form.get('event_id', 0))
        ticket_type = request.form.get('ticket_type', '')
        ticket_count = int(request.form.get('ticket_count', 1))
        customer_name = request.form.get('customer_name', '').strip()

        # Find event by event_id
        event = next((e for e in events if e['event_id'] == event_id), None)
        if event is None:
            return "Invalid event selected", 400

        # Find corresponding ticket
        ticket = next((t for t in tickets if t['event_id'] == event_id and t['ticket_type'] == ticket_type), None)
        if ticket is None:
            return "Ticket type not found for selected event", 400

        # Check availability
        if ticket['available_count'] < ticket_count:
            return "Not enough tickets available", 400

        # Calculate total
        total_amount = ticket_count * ticket['price']

        # Load bookings to assign new booking_id
        bookings = load_bookings()
        new_booking_id = 1
        if bookings:
            new_booking_id = max(b['booking_id'] for b in bookings) + 1

        # Booking date (current date) - simulate as fixed for now
        import datetime
        booking_date = datetime.datetime.now().strftime('%Y-%m-%d')

        # Create booking record
        booking = {
            'booking_id': new_booking_id,
            'event_id': event_id,
            'customer_name': customer_name,
            'booking_date': booking_date,
            'ticket_count': ticket_count,
            'ticket_type': ticket_type,
            'total_amount': total_amount,
            'status': 'Confirmed'
        }
        bookings.append(booking)

        # Update tickets sold and available counts
        ticket['available_count'] -= ticket_count
        ticket['sold_count'] += ticket_count

        # Save updated bookings and tickets
        save_bookings(bookings)
        save_tickets(tickets)

        confirmation = {
            'confirmation_number': new_booking_id,
            'event_name': event['event_name'],
            'ticket_count': ticket_count,
            'ticket_type': ticket_type
        }

        return render_template('ticket_booking.html', confirmation=confirmation)


# Participants Management
@app.route('/participants', methods=['GET', 'POST'])
def participants_management():
    participants = load_participants()
    events = load_events()
    event_names_by_id = {e['event_id']: e['event_name'] for e in events}

    if request.method == 'GET':
        participants_list = []
        for p in participants:
            participants_list.append({
                'participant_id': p['participant_id'],
                'name': p['name'],
                'email': p['email'],
                'event': event_names_by_id.get(p['event_id'], 'Unknown'),
                'status': p['status']
            })
        return render_template('participants.html', participants=participants_list)

    if request.method == 'POST':
        # Add or update participant
        participant_id = request.form.get('participant_id')
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        event_name = request.form.get('event', '').strip()
        status = request.form.get('status', '').strip()

        # Find event_id from name
        event_id = None
        for e in events:
            if e['event_name'] == event_name:
                event_id = e['event_id']
                break
        if event_id is None:
            return "Event not found", 400

        # Load bookings because participant has booking_id - for new participant, we can't assign booking_id reliably, assign 0
        bookings = load_bookings()

        participants_list = participants.copy()
        if participant_id:  # update existing
            try:
                pid = int(participant_id)
                updated = False
                for p in participants_list:
                    if p['participant_id'] == pid:
                        p['name'] = name
                        p['email'] = email
                        p['event_id'] = event_id
                        p['status'] = status
                        updated = True
                        break
                if not updated:
                    # add new if not found
                    pass
            except:
                pass
        else:  # add new participant
            new_id = 1
            if participants_list:
                new_id = max(p['participant_id'] for p in participants_list) + 1
            # registration date simulate current date
            import datetime
            registration_date = datetime.datetime.now().strftime('%Y-%m-%d')
            participant = {
                'participant_id': new_id,
                'event_id': event_id,
                'name': name,
                'email': email,
                'booking_id': 0,
                'status': status,
                'registration_date': registration_date
            }
            participants_list.append(participant)

        save_participants(participants_list)

        # Reload participants list for display
        participants = load_participants()
        participants_list = []
        for p in participants:
            participants_list.append({
                'participant_id': p['participant_id'],
                'name': p['name'],
                'email': p['email'],
                'event': event_names_by_id.get(p['event_id'], 'Unknown'),
                'status': p['status']
            })

        return render_template('participants.html', participants=participants_list)


# Venues Page
@app.route('/venues', methods=['GET'])
def venues_page():
    venues = load_venues()
    venues_list = []
    for v in venues:
        venues_list.append({
            'venue_id': v['venue_id'],
            'venue_name': v['venue_name'],
            'location': v['location'],
            'capacity': v['capacity'],
            'amenities': v['amenities']
        })
    return render_template('venues.html', venues=venues_list)


# Event Schedules
@app.route('/event_schedules', methods=['GET'])
def event_schedules():
    schedules = load_schedules()
    # Only keys required
    schedules_list = []
    for s in schedules:
        schedules_list.append({
            'schedule_id': s['schedule_id'],
            'event_id': s['event_id'],
            'session_title': s['session_title'],
            'session_time': s['session_time'],
            'duration_minutes': s['duration_minutes'],
            'speaker': s['speaker']
        })
    return render_template('schedules.html', schedules=schedules_list)


# Bookings Summary
@app.route('/bookings', methods=['GET'])
def bookings_summary():
    bookings = load_bookings()
    events = load_events()
    event_names_by_id = {e['event_id']: e['event_name'] for e in events}

    bookings_list = []
    for b in bookings:
        bookings_list.append({
            'booking_id': b['booking_id'],
            'event': event_names_by_id.get(b['event_id'], 'Unknown'),
            'date': b['booking_date'],
            'ticket_count': b['ticket_count'],
            'status': b['status']
        })
    return render_template('bookings.html', bookings=bookings_list)


# Cancel Booking
@app.route('/cancel_booking/<int:booking_id>', methods=['POST'])
def cancel_booking(booking_id):
    bookings = load_bookings()
    updated = False
    for b in bookings:
        if b['booking_id'] == booking_id:
            if b['status'] != 'Cancelled':
                b['status'] = 'Cancelled'
                updated = True
                break
    if updated:
        save_bookings(bookings)

    # Return updated bookings list
    events = load_events()
    event_names_by_id = {e['event_id']: e['event_name'] for e in events}
    bookings_list = []
    for b in bookings:
        bookings_list.append({
            'booking_id': b['booking_id'],
            'event': event_names_by_id.get(b['event_id'], 'Unknown'),
            'date': b['booking_date'],
            'ticket_count': b['ticket_count'],
            'status': b['status']
        })
    return render_template('bookings.html', bookings=bookings_list)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
