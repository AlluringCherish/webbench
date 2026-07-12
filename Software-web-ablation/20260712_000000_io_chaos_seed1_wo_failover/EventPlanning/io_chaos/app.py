from flask import Flask, render_template, redirect, url_for, request
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Helper functions to load data

def load_events():
    events = []
    try:
        with open(os.path.join(DATA_DIR, 'events.txt'), 'r', encoding='utf-8') as f:
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
    except Exception:
        # Fail gracefully
        pass
    return events


def load_venues():
    venues = []
    try:
        with open(os.path.join(DATA_DIR, 'venues.txt'), 'r', encoding='utf-8') as f:
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
    except Exception:
        pass
    return venues


def load_tickets():
    tickets = []
    try:
        with open(os.path.join(DATA_DIR, 'tickets.txt'), 'r', encoding='utf-8') as f:
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
    except Exception:
        pass
    return tickets


def load_bookings():
    bookings = []
    try:
        with open(os.path.join(DATA_DIR, 'bookings.txt'), 'r', encoding='utf-8') as f:
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
    except Exception:
        pass
    return bookings


def load_participants():
    participants = []
    try:
        with open(os.path.join(DATA_DIR, 'participants.txt'), 'r', encoding='utf-8') as f:
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
    except Exception:
        pass
    return participants


def load_schedules():
    schedules = []
    try:
        with open(os.path.join(DATA_DIR, 'schedules.txt'), 'r', encoding='utf-8') as f:
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
    except Exception:
        pass
    return schedules


# Root redirect route
@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard_page'))


# Dashboard page route
@app.route('/dashboard')
def dashboard_page():
    events = load_events()
    featured_events = []
    # Let's pick some featured events: first 5 upcoming (sorted by date ascending)
    try:
        # parse date for sorting
        events_sorted = sorted(events, key=lambda e: datetime.strptime(e['date'], '%Y-%m-%d'))
        for ev in events_sorted[:5]:
            featured_events.append({
                'event_id': ev['event_id'],
                'event_name': ev['event_name'],
                'date': ev['date'],
                'location': ev['location']
            })
    except Exception:
        featured_events = []

    return render_template('dashboard.html', featured_events=featured_events)


# Events listing page
@app.route('/events')
def events_listing():
    events = load_events()
    return render_template('events.html', events=events)


# Events search POST
@app.route('/events/search', methods=['POST'])
def events_search():
    search_category = request.form.get('search_category', '').strip()
    search_text = request.form.get('search_text', '').strip().lower()

    events = load_events()
    filtered_events = []

    # Filter events based on category and search text (searching in event_name, location, or date)
    for event in events:
        # Check category filter if specified and not 'All'
        if search_category and search_category != 'All' and event['category'] != search_category:
            continue
        # Check search_text in event_name or location or date
        if search_text:
            if (search_text not in event['event_name'].lower() and
                search_text not in event['location'].lower() and
                search_text not in event['date']):
                continue
        filtered_events.append(event)

    return render_template('events.html', filtered_events=filtered_events, search_category=search_category, search_text=request.form.get('search_text', ''))


# Event details route
@app.route('/event/<int:event_id>')
def event_details(event_id):
    events = load_events()
    event = None
    for e in events:
        if e['event_id'] == event_id:
            event = e
            break
    if not event:
        # Not found - redirect to events page
        return redirect(url_for('events_listing'))

    return render_template('event_details.html', event=event)


# Book ticket route GET and POST
@app.route('/book_ticket', methods=['GET', 'POST'])
def book_ticket():
    if request.method == 'GET':
        events = load_events()
        return render_template('book_ticket.html', events=events)
    else:
        # POST booking submission
        event_id_str = request.form.get('event_id')
        ticket_type = request.form.get('ticket_type')
        ticket_quantity_str = request.form.get('ticket_quantity')
        customer_name = request.form.get('customer_name', '').strip()

        try:
            event_id = int(event_id_str)
            ticket_quantity = int(ticket_quantity_str)
        except (ValueError, TypeError):
            return render_template('book_ticket.html', events=load_events(), booking_confirmation={'confirmation_message': 'Invalid input. Please enter correct values.', 'event_name': '', 'ticket_type': '', 'ticket_quantity': 0, 'total_amount': 0.0})

        if ticket_quantity <= 0 or not customer_name or not ticket_type:
            return render_template('book_ticket.html', events=load_events(), booking_confirmation={'confirmation_message': 'Please fill in all booking details correctly.', 'event_name': '', 'ticket_type': '', 'ticket_quantity': 0, 'total_amount': 0.0})

        events = load_events()
        event = None
        for e in events:
            if e['event_id'] == event_id:
                event = e
                break
        if not event:
            return render_template('book_ticket.html', events=events, booking_confirmation={'confirmation_message': 'Selected event not found.', 'event_name': '', 'ticket_type': '', 'ticket_quantity': 0, 'total_amount': 0.0})

        tickets = load_tickets()
        ticket = None
        for t in tickets:
            if t['event_id'] == event_id and t['ticket_type'] == ticket_type:
                ticket = t
                break

        if not ticket:
            return render_template('book_ticket.html', events=events, booking_confirmation={'confirmation_message': 'Selected ticket type not available.', 'event_name': event['event_name'], 'ticket_type': ticket_type, 'ticket_quantity': ticket_quantity, 'total_amount': 0.0})

        if ticket['available_count'] < ticket_quantity:
            return render_template('book_ticket.html', events=events, booking_confirmation={'confirmation_message': 'Not enough tickets available.', 'event_name': event['event_name'], 'ticket_type': ticket_type, 'ticket_quantity': ticket_quantity, 'total_amount': 0.0})

        # Calculate total amount
        total_amount = ticket['price'] * ticket_quantity

        # Update tickets.txt: decrement available_count, increment sold_count
        # Also add a new booking in bookings.txt
        try:
            tickets_updated = []
            for t in tickets:
                if t['ticket_id'] == ticket['ticket_id']:
                    t['available_count'] -= ticket_quantity
                    t['sold_count'] += ticket_quantity
                tickets_updated.append(t)

            # Write back tickets.txt
            with open(os.path.join(DATA_DIR, 'tickets.txt'), 'w', encoding='utf-8') as f:
                for t in tickets_updated:
                    line = f"{t['ticket_id']}|{t['event_id']}|{t['ticket_type']}|{t['price']}|{t['available_count']}|{t['sold_count']}\n"
                    f.write(line)

            # Load current bookings and append new booking
            bookings = load_bookings()
            max_booking_id = max((b['booking_id'] for b in bookings), default=0)
            new_booking_id = max_booking_id + 1
            booking_date = datetime.now().strftime('%Y-%m-%d')
            new_booking_line = f"{new_booking_id}|{event_id}|{customer_name}|{booking_date}|{ticket_quantity}|{ticket_type}|{total_amount}|Confirmed\n"

            with open(os.path.join(DATA_DIR, 'bookings.txt'), 'a', encoding='utf-8') as f:
                f.write(new_booking_line)

            confirmation_message = f"Booking confirmed for {customer_name}."

            booking_confirmation = {
                'confirmation_message': confirmation_message,
                'event_name': event['event_name'],
                'ticket_type': ticket_type,
                'ticket_quantity': ticket_quantity,
                'total_amount': total_amount
            }
            return render_template('book_ticket.html', booking_confirmation=booking_confirmation)

        except Exception:
            return render_template('book_ticket.html', events=load_events(), booking_confirmation={'confirmation_message': 'Error processing booking. Please try again.', 'event_name': event['event_name'], 'ticket_type': ticket_type, 'ticket_quantity': ticket_quantity, 'total_amount': 0.0})


# Participants management page
@app.route('/participants')
def participants_management():
    participants = load_participants()
    return render_template('participants.html', participants=participants)


# Participants search POST
@app.route('/participants/search', methods=['POST'])
def participants_search():
    search_text = request.form.get('search_text', '').strip().lower()
    status_filter = request.form.get('status_filter', '').strip()

    participants = load_participants()
    filtered_participants = []

    for p in participants:
        if search_text and search_text not in p['name'].lower() and search_text not in p['email'].lower():
            continue
        if status_filter and status_filter != 'All' and p['status'] != status_filter:
            continue
        filtered_participants.append(p)

    return render_template('participants.html', filtered_participants=filtered_participants, search_text=request.form.get('search_text', ''), status_filter=status_filter)


# Venues page
@app.route('/venues')
def venues_page():
    venues = load_venues()
    return render_template('venues.html', venues=venues)


# Event schedules page
@app.route('/event_schedules')
def event_schedules():
    schedules = load_schedules()
    return render_template('schedules.html', schedules=schedules)


# Bookings summary page
@app.route('/bookings')
def bookings_summary():
    bookings = load_bookings()
    return render_template('bookings.html', bookings=bookings)


# Cancel booking POST
@app.route('/cancel_booking/<int:booking_id>', methods=['POST'])
def cancel_booking(booking_id):
    # Load bookings
    bookings = load_bookings()
    booking_found = False
    for b in bookings:
        if b['booking_id'] == booking_id:
            booking_found = True
            # Change status to Cancelled only if not already
            if b['status'] != 'Cancelled':
                b['status'] = 'Cancelled'
            break

    if booking_found:
        try:
            # Write back updated bookings
            with open(os.path.join(DATA_DIR, 'bookings.txt'), 'w', encoding='utf-8') as f:
                for b in bookings:
                    line = f"{b['booking_id']}|{b['event_id']}|{b['customer_name']}|{b['booking_date']}|{b['ticket_count']}|{b['ticket_type']}|{b['total_amount']}|{b['status']}\n"
                    f.write(line)
        except Exception:
            pass

    return redirect(url_for('bookings_summary'))


if __name__ == '__main__':
    app.run(debug=True, port=5000)
