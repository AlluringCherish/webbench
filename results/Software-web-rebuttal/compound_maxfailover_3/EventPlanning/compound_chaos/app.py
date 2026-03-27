from flask import Flask, render_template, redirect, url_for, request
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

# Data file paths
EVENTS_FILE = 'data/events.txt'
VENUES_FILE = 'data/venues.txt'
TICKETS_FILE = 'data/tickets.txt'
BOOKINGS_FILE = 'data/bookings.txt'
PARTICIPANTS_FILE = 'data/participants.txt'
SCHEDULES_FILE = 'data/schedules.txt'

# Helper functions to load data

def load_events():
    events = []
    if not os.path.exists(EVENTS_FILE):
        return events
    with open(EVENTS_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            # event_id|event_name|category|date|time|location|description|venue_id|capacity
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


def load_venues():
    venues = []
    if not os.path.exists(VENUES_FILE):
        return venues
    with open(VENUES_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            # venue_id|venue_name|location|capacity|amenities|contact
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


def load_tickets():
    tickets = []
    if not os.path.exists(TICKETS_FILE):
        return tickets
    with open(TICKETS_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            # ticket_id|event_id|ticket_type|price|available_count|sold_count
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


def load_bookings():
    bookings = []
    if not os.path.exists(BOOKINGS_FILE):
        return bookings
    with open(BOOKINGS_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            # booking_id|event_id|customer_name|booking_date|ticket_count|ticket_type|total_amount|status
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


def load_participants():
    participants = []
    if not os.path.exists(PARTICIPANTS_FILE):
        return participants
    with open(PARTICIPANTS_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            # participant_id|event_id|name|email|booking_id|status|registration_date
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


def load_schedules():
    schedules = []
    if not os.path.exists(SCHEDULES_FILE):
        return schedules
    with open(SCHEDULES_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            # schedule_id|event_id|session_title|session_time|duration_minutes|speaker|venue_id
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


# Route: /
@app.route('/')
def dashboard_page():
    # featured_events: subset of events marked featured
    # design spec doesn't specify how to mark featured events, so we will arbitrarily consider the first 3 events as featured
    events = load_events()
    featured_events = events[:3]  # take first 3 as featured
    return render_template('dashboard.html', featured_events=featured_events)


# Route: /events
@app.route('/events')
def events_listing_page():
    events = load_events()
    return render_template('events.html', events=events)


# Route: /event/<int:event_id>
@app.route('/event/<int:event_id>')
def event_details_page(event_id):
    events = load_events()
    event = next((e for e in events if e['event_id'] == event_id), None)
    if not event:
        return "Event not found", 404
    return render_template('event_details.html', event=event)


# Route: /book_ticket GET, POST
@app.route('/book_ticket', methods=['GET', 'POST'])
def ticket_booking_page():
    if request.method == 'GET':
        # Provide events list and tickets for the form
        events = load_events()
        tickets_raw = load_tickets()
        # We need tickets per event, but tickets context is list of dicts {ticket_type:str, price:float} as per spec
        # The spec is underspecified on what tickets to show here, so we will show unique ticket types with prices ignoring event filtering
        # but as frontend needs events to pick event and tickets too, maybe show all ticket types for all events?

        # To align with spec, let's just show union of tickets types with price (lowest price if multiple) ignoring event_id filter
        ticket_types_map = {}
        for t in tickets_raw:
            tt = t['ticket_type']
            price = t['price']
            if tt not in ticket_types_map or price < ticket_types_map[tt]:
                ticket_types_map[tt] = price
        tickets = [{'ticket_type': k, 'price': v} for k, v in sorted(ticket_types_map.items())]

        return render_template('ticket_booking.html', events=events, tickets=tickets)

    if request.method == 'POST':
        form = request.form
        event_id_str = form.get('event_id')
        ticket_type = form.get('ticket_type')
        ticket_quantity_str = form.get('ticket_quantity')

        # validate inputs
        if not event_id_str or not ticket_type or not ticket_quantity_str:
            return "Missing booking information", 400

        try:
            event_id = int(event_id_str)
            ticket_quantity = int(ticket_quantity_str)
            if ticket_quantity <= 0:
                return "Invalid ticket quantity", 400
        except ValueError:
            return "Invalid numeric values", 400

        # Load data
        tickets_raw = load_tickets()
        events = load_events()
        bookings = load_bookings()

        # Check if event exists
        event = next((e for e in events if e['event_id'] == event_id), None)
        if not event:
            return "Event not found", 404

        # Find the ticket for this event and ticket_type
        ticket = next((t for t in tickets_raw if t['event_id'] == event_id and t['ticket_type'] == ticket_type), None)
        if not ticket:
            return "Ticket type not available for this event", 404

        # Check availability
        if ticket['available_count'] < ticket_quantity:
            return "Not enough tickets available", 400

        # If all good, create new booking
        # Determine new booking_id
        new_booking_id = 1
        if bookings:
            new_booking_id = max(b['booking_id'] for b in bookings) + 1

        # Append to bookings.txt
        import datetime
        booking_date = datetime.date.today().isoformat()
        total_amount = round(ticket['price'] * ticket_quantity, 2)
        customer_name = "Anonymous"  # No input from form for name as per spec, use anonymous or could be improved
        status = "Confirmed"

        new_booking_line = f"{new_booking_id}|{event_id}|{customer_name}|{booking_date}|{ticket_quantity}|{ticket_type}|{total_amount}|{status}\n"

        try:
            with open(BOOKINGS_FILE, 'a', encoding='utf-8') as f:
                f.write(new_booking_line)
        except Exception as e:
            return "Failed to save booking", 500

        # Update tickets.txt available_count and sold_count
        # This requires rewriting tickets.txt
        for t in tickets_raw:
            if t['ticket_id'] == ticket['ticket_id']:
                t['available_count'] -= ticket_quantity
                t['sold_count'] += ticket_quantity
                break

        try:
            with open(TICKETS_FILE, 'w', encoding='utf-8') as f:
                for t in tickets_raw:
                    line = f"{t['ticket_id']}|{t['event_id']}|{t['ticket_type']}|{t['price']:.2f}|{t['available_count']}|{t['sold_count']}\n"
                    f.write(line)
        except Exception as e:
            return "Failed to update tickets data", 500

        # After booking redirect to bookings page or show confirmation
        return redirect(url_for('bookings_summary_page'))


# Route: /participants
@app.route('/participants')
def participants_management():
    participants = load_participants()
    return render_template('participants.html', participants=participants)


# Route: /venues
@app.route('/venues')
def venues_page():
    venues = load_venues()
    return render_template('venues.html', venues=venues)


# Route: /schedules
@app.route('/schedules')
def schedules_page():
    schedules = load_schedules()
    events = load_events()
    return render_template('schedules.html', schedules=schedules, events=events)


# Route: /bookings
@app.route('/bookings')
def bookings_summary_page():
    bookings = load_bookings()
    return render_template('bookings.html', bookings=bookings)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
