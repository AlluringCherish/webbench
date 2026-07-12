from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

import os

DATA_DIR = 'data'

# Utility functions to load data from pipe delimited files

def load_events():
    events = []
    path = os.path.join(DATA_DIR, 'events.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
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
                    'capacity': int(parts[8]),
                }
                events.append(event)
    except Exception:
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
                parts = line.split('|')
                venue = {
                    'venue_id': int(parts[0]),
                    'venue_name': parts[1],
                    'location': parts[2],
                    'capacity': int(parts[3]),
                    'amenities': parts[4],
                    'contact': parts[5],
                }
                venues.append(venue)
    except Exception:
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
                parts = line.split('|')
                ticket = {
                    'ticket_id': int(parts[0]),
                    'event_id': int(parts[1]),
                    'ticket_type': parts[2],
                    'price': float(parts[3]),
                    'available_count': int(parts[4]),
                    'sold_count': int(parts[5]),
                }
                tickets.append(ticket)
    except Exception:
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
                parts = line.split('|')
                booking = {
                    'booking_id': int(parts[0]),
                    'event_id': int(parts[1]),
                    'customer_name': parts[2],
                    'booking_date': parts[3],
                    'ticket_count': int(parts[4]),
                    'ticket_type': parts[5],
                    'total_amount': float(parts[6]),
                    'status': parts[7],
                }
                bookings.append(booking)
    except Exception:
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
                parts = line.split('|')
                participant = {
                    'participant_id': int(parts[0]),
                    'event_id': int(parts[1]),
                    'name': parts[2],
                    'email': parts[3],
                    'booking_id': int(parts[4]),
                    'status': parts[5],
                    'registration_date': parts[6],
                }
                participants.append(participant)
    except Exception:
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
                parts = line.split('|')
                schedule = {
                    'schedule_id': int(parts[0]),
                    'event_id': int(parts[1]),
                    'session_title': parts[2],
                    'session_time': parts[3],
                    'duration_minutes': int(parts[4]),
                    'speaker': parts[5],
                    'venue_id': int(parts[6]),
                }
                schedules.append(schedule)
    except Exception:
        pass
    return schedules


def save_bookings(bookings):
    path = os.path.join(DATA_DIR, 'bookings.txt')
    try:
        with open(path, 'w', encoding='utf-8') as f:
            for b in bookings:
                line = '|'.join([
                    str(b['booking_id']),
                    str(b['event_id']),
                    b['customer_name'],
                    b['booking_date'],
                    str(b['ticket_count']),
                    b['ticket_type'],
                    f"{b['total_amount']:.2f}",
                    b['status'],
                ])
                f.write(line + '\n')
        return True
    except Exception:
        return False


def save_tickets(tickets):
    path = os.path.join(DATA_DIR, 'tickets.txt')
    try:
        with open(path, 'w', encoding='utf-8') as f:
            for t in tickets:
                line = '|'.join([
                    str(t['ticket_id']),
                    str(t['event_id']),
                    t['ticket_type'],
                    f"{t['price']:.2f}",
                    str(t['available_count']),
                    str(t['sold_count']),
                ])
                f.write(line + '\n')
        return True
    except Exception:
        return False


# 1. Root route: redirect to dashboard
@app.route('/')
def redirect_to_dashboard():
    return redirect(url_for('dashboard_page'))


# 2. Dashboard Route
@app.route('/dashboard')
def dashboard_page():
    events = load_events()
    # For featured events: pick first 5 upcoming events sorted by date (simple pick by date string ascending)
    featured_events = sorted(events, key=lambda e: e['date'])[:5]
    # For each event, only send: event_id, event_name, date, location
    featured_events = [{
        'event_id': e['event_id'],
        'event_name': e['event_name'],
        'date': e['date'],
        'location': e['location'],
    } for e in featured_events]

    user_navigation = {
        'browse_events': url_for('events_listing_page'),
        'view_tickets': url_for('bookings_page'),
        'venues': url_for('venues_page'),
    }

    return render_template('dashboard.html', featured_events=featured_events, user_navigation=user_navigation)


# 3. Events Listing
@app.route('/events')
def events_listing_page():
    events = load_events()
    # Only event_id, event_name, category, date, location
    events_summary = [{
        'event_id': e['event_id'],
        'event_name': e['event_name'],
        'category': e['category'],
        'date': e['date'],
        'location': e['location'],
    } for e in events]

    categories = ['Conference', 'Concert', 'Sports', 'Workshop', 'Social']

    return render_template('events.html', events=events_summary, categories=categories)


# 4. Event Details
@app.route('/event/<int:event_id>')
def event_details_page(event_id):
    events = load_events()
    event = next((e for e in events if e['event_id'] == event_id), None)
    if event is None:
        # Could render a 404 page or redirect
        return redirect(url_for('events_listing_page'))
    # Pass the event dict as required
    return render_template('event_details.html', event=event)


# 5. Ticket Booking GET
@app.route('/book_ticket', methods=['GET'])
def ticket_booking_page():
    events = load_events()
    events_brief = [{'event_id': e['event_id'], 'event_name': e['event_name']} for e in events]
    return render_template('book_ticket.html', events=events_brief)


# 6. Ticket Booking POST (process_ticket_booking)
from datetime import datetime

@app.route('/book_ticket', methods=['POST'])
def process_ticket_booking():
    events = load_events()
    tickets = load_tickets()
    bookings = load_bookings()

    # Expecting form fields: event_id, customer_name, ticket_count, ticket_type
    try:
        event_id = int(request.form.get('event_id', ''))
        customer_name = request.form.get('customer_name', '').strip()
        ticket_count = int(request.form.get('ticket_count', ''))
        ticket_type = request.form.get('ticket_type', '').strip()
    except Exception:
        error = "Invalid form data. Please check and submit again."
        return render_template('book_ticket.html', events=[{'event_id': e['event_id'], 'event_name': e['event_name']} for e in events], booking_confirmation=error)

    if not customer_name or ticket_count <= 0 or not ticket_type:
        error = "All fields are required and ticket count must be positive."
        return render_template('book_ticket.html', events=[{'event_id': e['event_id'], 'event_name': e['event_name']} for e in events], booking_confirmation=error)

    # Check event exists
    event = next((e for e in events if e['event_id'] == event_id), None)
    if event is None:
        error = "Selected event not found."
        return render_template('book_ticket.html', events=[{'event_id': e['event_id'], 'event_name': e['event_name']} for e in events], booking_confirmation=error)

    # Check ticket availability
    ticket = next((t for t in tickets if t['event_id'] == event_id and t['ticket_type'] == ticket_type), None)
    if ticket is None:
        error = "Selected ticket type not found for event."
        return render_template('book_ticket.html', events=[{'event_id': e['event_id'], 'event_name': e['event_name']} for e in events], booking_confirmation=error)

    if ticket['available_count'] < ticket_count:
        error = f"Not enough tickets available. Only {ticket['available_count']} left."
        return render_template('book_ticket.html', events=[{'event_id': e['event_id'], 'event_name': e['event_name']} for e in events], booking_confirmation=error)

    # Generate new booking_id (max existing +1 or 1)
    max_booking_id = max([b['booking_id'] for b in bookings], default=0)
    new_booking_id = max_booking_id + 1

    # Calculate total amount
    total_amount = ticket['price'] * ticket_count

    # Booking date as today
    booking_date = datetime.now().strftime('%Y-%m-%d')

    # New booking dictionary
    new_booking = {
        'booking_id': new_booking_id,
        'event_id': event_id,
        'customer_name': customer_name,
        'booking_date': booking_date,
        'ticket_count': ticket_count,
        'ticket_type': ticket_type,
        'total_amount': total_amount,
        'status': 'Confirmed',
    }

    # Update ticket availability
    ticket['available_count'] -= ticket_count
    ticket['sold_count'] += ticket_count

    # Append and save bookings and tickets
    bookings.append(new_booking)
    bookings_saved = save_bookings(bookings)
    tickets_saved = save_tickets(tickets)

    if not (bookings_saved and tickets_saved):
        error = "Failed to save booking data, please try again later."
        return render_template('book_ticket.html', events=[{'event_id': e['event_id'], 'event_name': e['event_name']} for e in events], booking_confirmation=error)

    booking_confirmation = {
        'booking_id': new_booking_id,
        'event_name': event['event_name'],
        'ticket_count': ticket_count,
        'ticket_type': ticket_type,
        'total_amount': total_amount,
        'status': 'Confirmed',
    }

    return render_template('book_ticket.html', events=[{'event_id': e['event_id'], 'event_name': e['event_name']} for e in events], booking_confirmation=booking_confirmation)


# 7. Participants Page GET
@app.route('/participants')
def participants_page():
    participants = load_participants()
    filter_options = {'statuses': ['Registered', 'Confirmed', 'Attended']}
    return render_template('participants.html', participants=participants, filter_options=filter_options)


# 8. Add Participant POST
@app.route('/add_participant', methods=['POST'])
def add_participant():
    participants = load_participants()
    events = load_events()

    # Expect form fields: participant_id (optional), event_id, name, email, booking_id, status, registration_date
    try:
        event_id = int(request.form.get('event_id', ''))
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        booking_id = int(request.form.get('booking_id', ''))
        status = request.form.get('status', '').strip()
        registration_date = request.form.get('registration_date', '').strip()
    except Exception:
        error = "Invalid participant data. Please check and submit again."
        filter_options = {'statuses': ['Registered', 'Confirmed', 'Attended']}
        return render_template('participants.html', participants=participants, filter_options=filter_options, error=error)

    if not name or not email or not status or not registration_date or event_id <= 0 or booking_id <= 0:
        error = "All fields are required and must be valid."
        filter_options = {'statuses': ['Registered', 'Confirmed', 'Attended']}
        return render_template('participants.html', participants=participants, filter_options=filter_options, error=error)

    # Generate new participant_id
    max_participant_id = max([p['participant_id'] for p in participants], default=0)
    new_participant_id = max_participant_id + 1

    new_participant = {
        'participant_id': new_participant_id,
        'event_id': event_id,
        'name': name,
        'email': email,
        'booking_id': booking_id,
        'status': status,
        'registration_date': registration_date,
    }

    # Append and save participants
    participants.append(new_participant)

    # Save participants to file
    path = os.path.join(DATA_DIR, 'participants.txt')
    try:
        with open(path, 'w', encoding='utf-8') as f:
            for p in participants:
                line = '|'.join([
                    str(p['participant_id']),
                    str(p['event_id']),
                    p['name'],
                    p['email'],
                    str(p['booking_id']),
                    p['status'],
                    p['registration_date'],
                ])
                f.write(line + '\n')
        filter_options = {'statuses': ['Registered', 'Confirmed', 'Attended']}
        return render_template('participants.html', participants=participants, filter_options=filter_options)
    except Exception:
        error = "Failed to save participant data. Please try again later."
        filter_options = {'statuses': ['Registered', 'Confirmed', 'Attended']}
        return render_template('participants.html', participants=participants, filter_options=filter_options, error=error)


# 9. Venues Page GET
@app.route('/venues')
def venues_page():
    venues = load_venues()
    # Only venue_id, venue_name, location, capacity, amenities
    venues_summary = [{
        'venue_id': v['venue_id'],
        'venue_name': v['venue_name'],
        'location': v['location'],
        'capacity': v['capacity'],
        'amenities': v['amenities'],
    } for v in venues]
    return render_template('venues.html', venues=venues_summary)


# 10. Venue Details GET
@app.route('/venue/<int:venue_id>')
def venue_details_page(venue_id):
    venues = load_venues()
    venue = next((v for v in venues if v['venue_id'] == venue_id), None)
    if venue is None:
        return redirect(url_for('venues_page'))
    return render_template('venue_details.html', venue=venue)


# 11. Schedules Page GET
@app.route('/schedules')
def schedules_page():
    schedules = load_schedules()
    events = load_events()
    return render_template('schedules.html', schedules=schedules, events=[{'event_id': e['event_id'], 'event_name': e['event_name']} for e in events])


# 12. Bookings Summary GET
@app.route('/bookings')
def bookings_page():
    bookings = load_bookings()
    return render_template('bookings.html', bookings=bookings)


# 13. Cancel Booking POST
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
        success = save_bookings(bookings)
        if not success:
            error = "Failed to update booking status."
            return render_template('bookings.html', bookings=bookings, error=error)
        return render_template('bookings.html', bookings=bookings)
    else:
        error = "Booking not found or already cancelled."
        return render_template('bookings.html', bookings=bookings, error=error)


# 14. Search Events POST
@app.route('/search_events', methods=['POST'])
def search_events():
    events = load_events()
    categories = ['Conference', 'Concert', 'Sports', 'Workshop', 'Social']

    # Search fields (optional): search_term, category
    search_term = request.form.get('search_term', '').lower().strip()
    category_filter = request.form.get('category', '').strip()

    filtered_events = events
    if search_term:
        filtered_events = [e for e in filtered_events if search_term in e['event_name'].lower()]
    if category_filter and category_filter in categories:
        filtered_events = [e for e in filtered_events if e['category'] == category_filter]

    filtered_summary = [{
        'event_id': e['event_id'],
        'event_name': e['event_name'],
        'category': e['category'],
        'date': e['date'],
        'location': e['location'],
    } for e in filtered_events]

    return render_template('events.html', events=filtered_summary, categories=categories)


# 15. Search Participants POST
@app.route('/search_participants', methods=['POST'])
def search_participants():
    participants = load_participants()
    filter_options = {'statuses': ['Registered', 'Confirmed', 'Attended']}

    # Search/filter fields: search_term by name or email, status
    search_term = request.form.get('search_term', '').lower().strip()
    status_filter = request.form.get('status', '').strip()

    filtered = participants
    if search_term:
        filtered = [p for p in filtered if search_term in p['name'].lower() or search_term in p['email'].lower()]
    if status_filter and status_filter in filter_options['statuses']:
        filtered = [p for p in filtered if p['status'] == status_filter]

    return render_template('participants.html', participants=filtered, filter_options=filter_options)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
