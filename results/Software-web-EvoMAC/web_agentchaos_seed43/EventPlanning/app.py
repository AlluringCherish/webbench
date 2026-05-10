'''
Backend Flask application for EventPlanning web application.
Defines all necessary routes including root '/' serving the Dashboard page.
Ensures route names correspond exactly to frontend navigation URLs.
'''
from flask import Flask, render_template, request, redirect, url_for
import os
import datetime
app = Flask(__name__)
DATA_DIR = 'data'
# Utility functions to read data from text files
def read_events():
    events = []
    try:
        with open(os.path.join(DATA_DIR, 'events.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split('|')
                    if len(parts) != 9:
                        continue  # skip malformed line
                    event = {
                        'event_id': parts[0],
                        'event_name': parts[1],
                        'category': parts[2],
                        'date': parts[3],
                        'time': parts[4],
                        'location': parts[5],
                        'description': parts[6],
                        'venue_id': parts[7],
                        'capacity': parts[8]
                    }
                    events.append(event)
    except FileNotFoundError:
        pass
    return events
def read_venues():
    venues = []
    try:
        with open(os.path.join(DATA_DIR, 'venues.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split('|')
                    if len(parts) != 6:
                        continue  # skip malformed line
                    venue = {
                        'venue_id': parts[0],
                        'venue_name': parts[1],
                        'location': parts[2],
                        'capacity': parts[3],
                        'amenities': parts[4],
                        'contact': parts[5]
                    }
                    venues.append(venue)
    except FileNotFoundError:
        pass
    return venues
def read_tickets():
    tickets = []
    try:
        with open(os.path.join(DATA_DIR, 'tickets.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split('|')
                    if len(parts) != 6:
                        continue  # skip malformed line
                    try:
                        ticket = {
                            'ticket_id': parts[0],
                            'event_id': parts[1],
                            'ticket_type': parts[2],
                            'price': float(parts[3]),
                            'available_count': int(parts[4]),
                            'sold_count': int(parts[5])
                        }
                        tickets.append(ticket)
                    except ValueError:
                        continue  # skip malformed numeric data
    except FileNotFoundError:
        pass
    return tickets
def read_bookings():
    bookings = []
    try:
        with open(os.path.join(DATA_DIR, 'bookings.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split('|')
                    if len(parts) != 8:
                        continue  # skip malformed line
                    try:
                        booking = {
                            'booking_id': parts[0],
                            'event_id': parts[1],
                            'customer_name': parts[2],
                            'booking_date': parts[3],
                            'ticket_count': int(parts[4]),
                            'ticket_type': parts[5],
                            'total_amount': float(parts[6]),
                            'status': parts[7]
                        }
                        bookings.append(booking)
                    except ValueError:
                        continue  # skip malformed numeric data
    except FileNotFoundError:
        pass
    return bookings
def read_participants():
    participants = []
    try:
        with open(os.path.join(DATA_DIR, 'participants.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split('|')
                    if len(parts) != 7:
                        continue  # skip malformed line
                    participant = {
                        'participant_id': parts[0],
                        'event_id': parts[1],
                        'name': parts[2],
                        'email': parts[3],
                        'booking_id': parts[4],
                        'status': parts[5],
                        'registration_date': parts[6]
                    }
                    participants.append(participant)
    except FileNotFoundError:
        pass
    return participants
def read_schedules():
    schedules = []
    try:
        with open(os.path.join(DATA_DIR, 'schedules.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split('|')
                    if len(parts) != 7:
                        continue  # skip malformed line
                    try:
                        schedule = {
                            'schedule_id': parts[0],
                            'event_id': parts[1],
                            'session_title': parts[2],
                            'session_time': parts[3],
                            'duration_minutes': int(parts[4]),
                            'speaker': parts[5],
                            'venue_id': parts[6]
                        }
                        schedules.append(schedule)
                    except ValueError:
                        continue  # skip malformed numeric data
    except FileNotFoundError:
        pass
    return schedules
# Route for root '/' serving Dashboard page
@app.route('/')
def dashboard():
    events = read_events()
    venues = read_venues()
    # For featured events, pick first 3 upcoming events sorted by date
    upcoming_events = sorted(events, key=lambda e: e['date'])[:3]
    # For featured venues, pick first 3 venues
    featured_venues = venues[:3]
    return render_template('dashboard.html', events=upcoming_events, venues=featured_venues)
# Route for Events Listing page
@app.route('/events')
def events_listing():
    events = read_events()
    category_filter = request.args.get('category', '')
    search_query = request.args.get('search', '').lower()
    filtered_events = []
    for event in events:
        if category_filter and event['category'].lower() != category_filter.lower():
            continue
        if search_query:
            if (search_query not in event['event_name'].lower() and
                search_query not in event['location'].lower() and
                search_query not in event['date']):
                continue
        filtered_events.append(event)
    categories = ['Conference', 'Concert', 'Sports', 'Workshop', 'Social']
    return render_template('events.html', events=filtered_events, categories=categories, selected_category=category_filter, search_query=search_query)
# Route for Event Details page
@app.route('/events/<event_id>')
def event_details(event_id):
    events = read_events()
    event = next((e for e in events if e['event_id'] == event_id), None)
    if not event:
        return "Event not found", 404
    return render_template('event_details.html', event=event)
# Route for Ticket Booking page
@app.route('/tickets', methods=['GET', 'POST'])
def ticket_booking():
    events = read_events()
    tickets = read_tickets()
    booking_confirmation = None
    if request.method == 'POST':
        event_id = request.form.get('select-event-dropdown')
        ticket_quantity = int(request.form.get('ticket-quantity-input', 0))
        ticket_type = request.form.get('ticket-type-select')
        customer_name = request.form.get('customer-name', 'Guest')
        # Find ticket info
        ticket_info = next((t for t in tickets if t['event_id'] == event_id and t['ticket_type'] == ticket_type), None)
        if not ticket_info:
            booking_confirmation = "Selected ticket type not available."
        elif ticket_quantity <= 0:
            booking_confirmation = "Please enter a valid ticket quantity."
        elif ticket_quantity > (ticket_info['available_count'] - ticket_info['sold_count']):
            booking_confirmation = "Not enough tickets available."
        else:
            # Calculate total amount
            total_amount = ticket_quantity * ticket_info['price']
            # Generate new booking_id
            bookings = read_bookings()
            new_booking_id = str(max([int(b['booking_id']) for b in bookings], default=0) + 1)
            booking_date = datetime.date.today().isoformat()
            # Append booking to bookings.txt
            booking_line = '|'.join([
                new_booking_id,
                event_id,
                customer_name,
                booking_date,
                str(ticket_quantity),
                ticket_type,
                f"{total_amount:.2f}",
                'Confirmed'
            ])
            with open(os.path.join(DATA_DIR, 'bookings.txt'), 'a', encoding='utf-8') as f:
                f.write(booking_line + '\n')
            # Update tickets sold_count
            updated_tickets = []
            for t in tickets:
                if t['ticket_id'] == ticket_info['ticket_id']:
                    t['sold_count'] += ticket_quantity
                updated_tickets.append(t)
            with open(os.path.join(DATA_DIR, 'tickets.txt'), 'w', encoding='utf-8') as f:
                for t in updated_tickets:
                    line = '|'.join([
                        t['ticket_id'],
                        t['event_id'],
                        t['ticket_type'],
                        f"{t['price']:.2f}",
                        str(t['available_count']),
                        str(t['sold_count'])
                    ])
                    f.write(line + '\n')
            booking_confirmation = f"Booking confirmed! Booking ID: {new_booking_id}, Total Amount: ${total_amount:.2f}"
    return render_template('ticket_booking.html', events=events, tickets=tickets, booking_confirmation=booking_confirmation)
# Route for Participants Management page
@app.route('/participants')
def participants_management():
    participants = read_participants()
    events = read_events()
    search_query = request.args.get('search', '').lower()
    status_filter = request.args.get('status', '')
    filtered_participants = []
    for p in participants:
        if status_filter and p['status'].lower() != status_filter.lower():
            continue
        if search_query:
            if (search_query not in p['name'].lower() and search_query not in p['email'].lower()):
                continue
        filtered_participants.append(p)
    statuses = ['Registered', 'Confirmed', 'Attended']
    # Map event names for participants
    event_dict = {e['event_id']: e['event_name'] for e in events}
    return render_template('participants.html', participants=filtered_participants, statuses=statuses, selected_status=status_filter, search_query=search_query, event_dict=event_dict)
# Route for Venue Information page
@app.route('/venues')
def venues_page():
    venues = read_venues()
    search_query = request.args.get('search', '').lower()
    capacity_filter = request.args.get('capacity', '')
    filtered_venues = []
    for v in venues:
        if capacity_filter:
            try:
                cap = int(v['capacity'])
            except ValueError:
                continue  # skip malformed capacity
            if capacity_filter == 'Small' and cap > 1000:
                continue
            elif capacity_filter == 'Medium' and (cap <= 1000 or cap > 3000):
                continue
            elif capacity_filter == 'Large' and cap <= 3000:
                continue
        if search_query:
            if (search_query not in v['venue_name'].lower() and search_query not in v['location'].lower()):
                continue
        filtered_venues.append(v)
    capacities = ['Small', 'Medium', 'Large']
    return render_template('venues.html', venues=filtered_venues, capacities=capacities, selected_capacity=capacity_filter, search_query=search_query)
# Route for Venue Details page
@app.route('/venues/<venue_id>')
def venue_details(venue_id):
    venues = read_venues()
    venue = next((v for v in venues if v['venue_id'] == venue_id), None)
    if not venue:
        return "Venue not found", 404
    return render_template('venue_details.html', venue=venue)
# Route for Event Schedules page
@app.route('/schedules')
def schedules_page():
    schedules = read_schedules()
    events = read_events()
    filter_date = request.args.get('date', '')
    filter_event = request.args.get('event', '')
    filtered_schedules = []
    for s in schedules:
        if filter_date and not s['session_time'].startswith(filter_date):
            continue
        if filter_event and s['event_id'] != filter_event:
            continue
        filtered_schedules.append(s)
    event_dict = {e['event_id']: e['event_name'] for e in events}
    return render_template('schedules.html', schedules=filtered_schedules, events=events, filter_date=filter_date, filter_event=filter_event, event_dict=event_dict)
# Route for Bookings Summary page
@app.route('/bookings')
def bookings_page():
    bookings = read_bookings()
    events = read_events()
    search_query = request.args.get('search', '').lower()
    filtered_bookings = []
    for b in bookings:
        event_name = next((e['event_name'] for e in events if e['event_id'] == b['event_id']), '')
        if search_query:
            if (search_query not in event_name.lower() and search_query not in b['booking_id']):
                continue
        filtered_bookings.append(b)
    event_dict = {e['event_id']: e['event_name'] for e in events}
    return render_template('bookings.html', bookings=filtered_bookings, event_dict=event_dict, search_query=search_query)
# Route to cancel booking
@app.route('/bookings/cancel/<booking_id>', methods=['POST'])
def cancel_booking(booking_id):
    bookings = read_bookings()
    booking_found = False
    for b in bookings:
        if b['booking_id'] == booking_id:
            b['status'] = 'Cancelled'
            booking_found = True
            break
    if booking_found:
        with open(os.path.join(DATA_DIR, 'bookings.txt'), 'w', encoding='utf-8') as f:
            for b in bookings:
                line = '|'.join([
                    b['booking_id'],
                    b['event_id'],
                    b['customer_name'],
                    b['booking_date'],
                    str(b['ticket_count']),
                    b['ticket_type'],
                    f"{b['total_amount']:.2f}",
                    b['status']
                ])
                f.write(line + '\n')
    return redirect(url_for('bookings_page'))
if __name__ == '__main__':
    app.run(debug=True)