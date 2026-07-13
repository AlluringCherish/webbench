from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Utility functions for reading data files

def read_events():
    events = []
    filepath = os.path.join(DATA_DIR, 'events.txt')
    if not os.path.exists(filepath):
        return events
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            fields = line.split('|')
            try:
                event = {
                    'event_id': int(fields[0]),
                    'event_name': fields[1],
                    'category': fields[2],
                    'date': fields[3],
                    'time': fields[4],
                    'location': fields[5],
                    'description': fields[6],
                    'venue_id': int(fields[7]),
                    'capacity': int(fields[8])
                }
                events.append(event)
            except (IndexError, ValueError):
                continue
    return events


def read_venues():
    venues = []
    filepath = os.path.join(DATA_DIR, 'venues.txt')
    if not os.path.exists(filepath):
        return venues
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            fields = line.split('|')
            try:
                venue = {
                    'venue_id': int(fields[0]),
                    'venue_name': fields[1],
                    'location': fields[2],
                    'capacity': int(fields[3]),
                    'amenities': fields[4],
                    'contact': fields[5]
                }
                venues.append(venue)
            except (IndexError, ValueError):
                continue
    return venues


def read_tickets():
    tickets = []
    filepath = os.path.join(DATA_DIR, 'tickets.txt')
    if not os.path.exists(filepath):
        return tickets
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            fields = line.split('|')
            try:
                ticket = {
                    'ticket_id': int(fields[0]),
                    'event_id': int(fields[1]),
                    'ticket_type': fields[2],
                    'price': float(fields[3]),
                    'available_count': int(fields[4]),
                    'sold_count': int(fields[5])
                }
                tickets.append(ticket)
            except (IndexError, ValueError):
                continue
    return tickets


def write_tickets(tickets):
    filepath = os.path.join(DATA_DIR, 'tickets.txt')
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            for t in tickets:
                line = f"{t['ticket_id']}|{t['event_id']}|{t['ticket_type']}|{t['price']}|{t['available_count']}|{t['sold_count']}\n"
                f.write(line)
    except Exception:
        pass


def read_bookings():
    bookings = []
    filepath = os.path.join(DATA_DIR, 'bookings.txt')
    if not os.path.exists(filepath):
        return bookings
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            fields = line.split('|')
            try:
                booking = {
                    'booking_id': int(fields[0]),
                    'event_id': int(fields[1]),
                    'customer_name': fields[2],
                    'booking_date': fields[3],
                    'ticket_count': int(fields[4]),
                    'ticket_type': fields[5],
                    'total_amount': float(fields[6]),
                    'status': fields[7]
                }
                bookings.append(booking)
            except (IndexError, ValueError):
                continue
    return bookings


def write_bookings(bookings):
    filepath = os.path.join(DATA_DIR, 'bookings.txt')
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            for b in bookings:
                line = f"{b['booking_id']}|{b['event_id']}|{b['customer_name']}|{b['booking_date']}|{b['ticket_count']}|{b['ticket_type']}|{b['total_amount']}|{b['status']}\n"
                f.write(line)
    except Exception:
        pass


def read_participants():
    participants = []
    filepath = os.path.join(DATA_DIR, 'participants.txt')
    if not os.path.exists(filepath):
        return participants
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            fields = line.split('|')
            try:
                part = {
                    'participant_id': int(fields[0]),
                    'event_id': int(fields[1]),
                    'name': fields[2],
                    'email': fields[3],
                    'booking_id': int(fields[4]),
                    'status': fields[5],
                    'registration_date': fields[6]
                }
                participants.append(part)
            except (IndexError, ValueError):
                continue
    return participants


def write_participants(participants):
    filepath = os.path.join(DATA_DIR, 'participants.txt')
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            for p in participants:
                line = f"{p['participant_id']}|{p['event_id']}|{p['name']}|{p['email']}|{p['booking_id']}|{p['status']}|{p['registration_date']}\n"
                f.write(line)
    except Exception:
        pass


def read_schedules():
    schedules = []
    filepath = os.path.join(DATA_DIR, 'schedules.txt')
    if not os.path.exists(filepath):
        return schedules
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            fields = line.split('|')
            try:
                schedule = {
                    'schedule_id': int(fields[0]),
                    'event_id': int(fields[1]),
                    'session_title': fields[2],
                    'session_time': fields[3],
                    'duration_minutes': int(fields[4]),
                    'speaker': fields[5],
                    'venue_id': int(fields[6])
                }
                schedules.append(schedule)
            except (IndexError, ValueError):
                continue
    return schedules


# Route: / (Dashboard Page)
@app.route('/')
def dashboard_page():
    events = read_events()
    # For featured events, choose some upcoming events (e.g., next 3)
    today_str = datetime.now().strftime('%Y-%m-%d')
    featured_events = [e for e in events if e['date'] >= today_str]
    featured_events = sorted(featured_events, key=lambda x: x['date'])[:3]
    return render_template('dashboard.html', featured_events=featured_events)


# Route: /events (Events Listing Page)
@app.route('/events')
def events_listing_page():
    events = read_events()
    categories = sorted(set(e['category'] for e in events))
    filters = {
        'category': request.args.get('category', ''),
        'search': request.args.get('search', '')
    }
    filtered_events = events
    # Filter by category
    if filters['category']:
        filtered_events = [e for e in filtered_events if e['category'] == filters['category']]
    # Search filter
    search_term = filters['search'].lower()
    if search_term:
        filtered_events = [e for e in filtered_events if 
                           search_term in e['event_name'].lower() or
                           search_term in e['location'].lower() or
                           search_term in e['date'].lower()]
    return render_template('events_listing.html', events=filtered_events, categories=categories, filters=filters)


# Route: /events/<int:event_id> (Event Details Page)
@app.route('/events/<int:event_id>')
def event_details_page(event_id):
    events = read_events()
    event = next((e for e in events if e['event_id'] == event_id), None)
    if not event:
        return "Event not found", 404
    return render_template('event_details.html', event=event)


# Route: /booking (Ticket Booking Page)
@app.route('/booking', methods=['GET', 'POST'])
def ticket_booking_page():
    events = read_events()
    booking_confirmation = None
    if request.method == 'POST':
        # Extract form data
        try:
            event_id = int(request.form.get('select-event-dropdown'))
            ticket_quantity = int(request.form.get('ticket-quantity-input'))
            ticket_type = request.form.get('ticket-type-select')
            customer_name = request.form.get('customer-name-input', 'Guest')  # optional field
        except (ValueError, TypeError):
            return render_template('ticket_booking.html', events=events, booking_confirmation='Invalid input')

        # Fetch tickets for event and type
        tickets = read_tickets()
        ticket = None
        for t in tickets:
            if t['event_id'] == event_id and t['ticket_type'] == ticket_type:
                ticket = t
                break
        if not ticket:
            return render_template('ticket_booking.html', events=events, booking_confirmation='Selected ticket type not available')

        if ticket['available_count'] < ticket_quantity:
            return render_template('ticket_booking.html', events=events, booking_confirmation='Not enough tickets available')

        # Calculate total amount
        total_amount = ticket_quantity * ticket['price']

        # Read existing bookings to assign booking_id
        bookings = read_bookings()
        if bookings:
            new_booking_id = max(b['booking_id'] for b in bookings) + 1
        else:
            new_booking_id = 1

        booking_date = datetime.now().strftime('%Y-%m-%d')
        new_booking = {
            'booking_id': new_booking_id,
            'event_id': event_id,
            'customer_name': customer_name,
            'booking_date': booking_date,
            'ticket_count': ticket_quantity,
            'ticket_type': ticket_type,
            'total_amount': total_amount,
            'status': 'Confirmed'
        }

        bookings.append(new_booking)

        # Update tickets availability
        for t in tickets:
            if t['ticket_id'] == ticket['ticket_id']:
                t['available_count'] -= ticket_quantity
                t['sold_count'] += ticket_quantity
                break
        write_bookings(bookings)
        write_tickets(tickets)

        booking_confirmation = f"Booking Confirmed! Booking ID: {new_booking_id}, Total: ${total_amount:.2f}"

    return render_template('ticket_booking.html', events=events, booking_confirmation=booking_confirmation)


# Route: /participants (Participants Management Page)
@app.route('/participants', methods=['GET', 'POST'])
def participants_management():
    participants = read_participants()
    search_filter = request.args.get('search', '').lower()
    status_filter = request.args.get('status', '')

    if request.method == 'POST':
        # Add a new participant from form (simulate with minimal data, normally more validation needed)
        try:
            name = request.form.get('participant-name')
            email = request.form.get('participant-email')
            event_id = int(request.form.get('participant-event-id'))
            booking_id = int(request.form.get('participant-booking-id'))
            status = request.form.get('participant-status')
            registration_date = datetime.now().strftime('%Y-%m-%d')
        except (ValueError, TypeError):
            return render_template('participants_management.html', participants=participants, search_filter=search_filter, status_filter=status_filter, error='Invalid participant data')

        if participants:
            new_participant_id = max(p['participant_id'] for p in participants) + 1
        else:
            new_participant_id = 1

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
        write_participants(participants)

    # Apply filters
    filtered_participants = participants
    if search_filter:
        filtered_participants = [p for p in filtered_participants if search_filter in p['name'].lower() or search_filter in p['email'].lower()]
    if status_filter:
        filtered_participants = [p for p in filtered_participants if p['status'] == status_filter]

    return render_template('participants_management.html', participants=filtered_participants, search_filter=search_filter, status_filter=status_filter)


# Route: /venues (Venue Information Page)
@app.route('/venues')
def venues_information_page():
    venues = read_venues()
    capacity_filter = request.args.get('capacity', '')
    filtered_venues = venues
    if capacity_filter:
        if capacity_filter == 'Small':
            filtered_venues = [v for v in filtered_venues if v['capacity'] < 500]
        elif capacity_filter == 'Medium':
            filtered_venues = [v for v in filtered_venues if 500 <= v['capacity'] < 2000]
        elif capacity_filter == 'Large':
            filtered_venues = [v for v in filtered_venues if v['capacity'] >= 2000]

    return render_template('venues.html', venues=filtered_venues, capacity_filter=capacity_filter)


# Route: /venues/<int:venue_id> (Venue Details Page)
@app.route('/venues/<int:venue_id>')
def venue_details_page(venue_id):
    venues = read_venues()
    venue = next((v for v in venues if v['venue_id'] == venue_id), None)
    if not venue:
        return "Venue not found", 404
    return render_template('venue_details.html', venue=venue)


# Route: /schedules (Event Schedules Page)
@app.route('/schedules')
def event_schedules_page():
    schedules = read_schedules()
    events = read_events()
    filter_date = request.args.get('date', '')
    filter_event = request.args.get('event', '')

    filtered_schedules = schedules

    if filter_date:
        filtered_schedules = [s for s in filtered_schedules if s['session_time'].startswith(filter_date)]

    if filter_event:
        try:
            filter_event_id = int(filter_event)
            filtered_schedules = [s for s in filtered_schedules if s['event_id'] == filter_event_id]
        except ValueError:
            pass

    return render_template('event_schedules.html', schedules=filtered_schedules, filter_date=filter_date, filter_event=filter_event, events=events)


# Route: /schedules/export (Export schedules POST)
@app.route('/schedules/export', methods=['POST'])
def export_schedules():
    # Dummy implementation for export, just redirect back
    return redirect(url_for('event_schedules_page'))


# Route: /bookings (Bookings Summary Page)
@app.route('/bookings', methods=['GET', 'POST'])
def bookings_summary_page():
    bookings = read_bookings()
    search_filter = request.args.get('search', '').lower()
    if search_filter:
        bookings = [b for b in bookings if search_filter in str(b['booking_id']).lower() or search_filter in b['customer_name'].lower()]

    if request.method == 'POST':
        # Could be filters or other actions - for now no state changes
        pass

    return render_template('bookings_summary.html', bookings=bookings, search_filter=search_filter)


# Route: /bookings/cancel/<int:booking_id> (Cancel booking POST)
@app.route('/bookings/cancel/<int:booking_id>', methods=['POST'])
def cancel_booking(booking_id):
    bookings = read_bookings()
    updated = False
    for b in bookings:
        if b['booking_id'] == booking_id:
            b['status'] = 'Cancelled'
            updated = True
            break
    if updated:
        write_bookings(bookings)
    return redirect(url_for('bookings_summary_page'))


if __name__ == '__main__':
    app.run(debug=True)
