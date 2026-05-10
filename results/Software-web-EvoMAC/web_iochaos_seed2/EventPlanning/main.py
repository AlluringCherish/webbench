'''
Main backend application for EventPlanning web application.
Defines all routes corresponding to the eight pages as per requirements.
Ensures root URL '/' serves the Dashboard page.
Uses Flask framework and renders templates with data loaded from local text files.
'''
from flask import Flask, render_template, request, redirect, url_for
import os
import datetime
app = Flask(__name__)
DATA_DIR = 'data'
def read_events():
    events = []
    path = os.path.join(DATA_DIR, 'events.txt')
    if not os.path.exists(path):
        return events
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split('|')
                if len(parts) == 9:
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
    return events
def read_venues():
    venues = []
    path = os.path.join(DATA_DIR, 'venues.txt')
    if not os.path.exists(path):
        return venues
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split('|')
                if len(parts) == 6:
                    venue = {
                        'venue_id': parts[0],
                        'venue_name': parts[1],
                        'location': parts[2],
                        'capacity': parts[3],
                        'amenities': parts[4],
                        'contact': parts[5]
                    }
                    venues.append(venue)
    return venues
def read_tickets():
    tickets = []
    path = os.path.join(DATA_DIR, 'tickets.txt')
    if not os.path.exists(path):
        return tickets
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split('|')
                if len(parts) == 6:
                    ticket = {
                        'ticket_id': parts[0],
                        'event_id': parts[1],
                        'ticket_type': parts[2],
                        'price': float(parts[3]),
                        'available_count': int(parts[4]),
                        'sold_count': int(parts[5])
                    }
                    tickets.append(ticket)
    return tickets
def read_bookings():
    bookings = []
    path = os.path.join(DATA_DIR, 'bookings.txt')
    if not os.path.exists(path):
        return bookings
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split('|')
                if len(parts) == 8:
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
    return bookings
def read_participants():
    participants = []
    path = os.path.join(DATA_DIR, 'participants.txt')
    if not os.path.exists(path):
        return participants
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split('|')
                if len(parts) == 7:
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
    return participants
def read_schedules():
    schedules = []
    path = os.path.join(DATA_DIR, 'schedules.txt')
    if not os.path.exists(path):
        return schedules
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split('|')
                if len(parts) == 7:
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
    return schedules
@app.route('/')
def dashboard():
    events = read_events()
    venues = read_venues()
    # For featured events, pick first 3 upcoming events sorted by date and time
    def event_datetime(e):
        return e['date'] + ' ' + e['time']
    upcoming_events = sorted(events, key=event_datetime)[:3]
    # For featured venues, pick first 3 venues
    featured_venues = venues[:3]
    return render_template('dashboard.html',
                           events=upcoming_events,
                           venues=featured_venues)
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
    return render_template('events.html',
                           events=filtered_events,
                           categories=categories,
                           selected_category=category_filter,
                           search_query=search_query)
@app.route('/events/<event_id>')
def event_details(event_id):
    events = read_events()
    event = next((e for e in events if e['event_id'] == event_id), None)
    if not event:
        return "Event not found", 404
    return render_template('event_details.html', event=event)
@app.route('/book-tickets', methods=['GET', 'POST'])
def book_tickets():
    events = read_events()
    tickets = read_tickets()
    booking_confirmation = None
    if request.method == 'POST':
        event_id = request.form.get('select-event-dropdown')
        ticket_quantity = request.form.get('ticket-quantity-input')
        ticket_type = request.form.get('ticket-type-select')
        customer_name = request.form.get('customer-name', 'Guest')
        try:
            ticket_quantity = int(ticket_quantity)
            if ticket_quantity <= 0:
                raise ValueError
        except:
            return render_template('ticket_booking.html',
                                   events=events,
                                   error="Invalid ticket quantity.",
                                   booking_confirmation=None)
        # Find ticket info for event and ticket_type
        ticket_info = next((t for t in tickets if t['event_id'] == event_id and t['ticket_type'].lower() == ticket_type.lower()), None)
        if not ticket_info:
            return render_template('ticket_booking.html',
                                   events=events,
                                   error="Selected ticket type not available.",
                                   booking_confirmation=None)
        if ticket_info['available_count'] < ticket_quantity:
            return render_template('ticket_booking.html',
                                   events=events,
                                   error="Not enough tickets available.",
                                   booking_confirmation=None)
        # Calculate total amount
        total_amount = ticket_info['price'] * ticket_quantity
        # Generate new booking_id
        bookings = read_bookings()
        if bookings:
            max_id = max(int(b['booking_id']) for b in bookings)
            new_booking_id = str(max_id + 1)
        else:
            new_booking_id = '1'
        booking_date = datetime.date.today().isoformat()
        new_booking = f"{new_booking_id}|{event_id}|{customer_name}|{booking_date}|{ticket_quantity}|{ticket_type}|{total_amount:.2f}|Confirmed\n"
        # Append booking to bookings.txt
        bookings_path = os.path.join(DATA_DIR, 'bookings.txt')
        with open(bookings_path, 'a', encoding='utf-8') as f:
            f.write(new_booking)
        # Update tickets.txt sold_count and available_count
        tickets_path = os.path.join(DATA_DIR, 'tickets.txt')
        updated_lines = []
        with open(tickets_path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 6:
                    if parts[1] == event_id and parts[2].lower() == ticket_type.lower():
                        available_count = int(parts[4]) - ticket_quantity
                        sold_count = int(parts[5]) + ticket_quantity
                        parts[4] = str(available_count)
                        parts[5] = str(sold_count)
                        updated_line = '|'.join(parts)
                        updated_lines.append(updated_line)
                    else:
                        updated_lines.append(line.strip())
        with open(tickets_path, 'w', encoding='utf-8') as f:
            for line in updated_lines:
                f.write(line + '\n')
        booking_confirmation = {
            'booking_id': new_booking_id,
            'event_id': event_id,
            'customer_name': customer_name,
            'booking_date': booking_date,
            'ticket_count': ticket_quantity,
            'ticket_type': ticket_type,
            'total_amount': total_amount,
            'status': 'Confirmed'
        }
        return render_template('ticket_booking.html',
                               events=events,
                               booking_confirmation=booking_confirmation,
                               error=None)
    return render_template('ticket_booking.html', events=events, booking_confirmation=None, error=None)
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
            if (search_query not in p['name'].lower() and
                search_query not in p['email'].lower()):
                continue
        filtered_participants.append(p)
    statuses = ['Registered', 'Confirmed', 'Attended']
    return render_template('participants.html',
                           participants=filtered_participants,
                           statuses=statuses,
                           selected_status=status_filter,
                           search_query=search_query,
                           events=events)
@app.route('/venues')
def venues_page():
    venues = read_venues()
    search_query = request.args.get('search', '').lower()
    capacity_filter = request.args.get('capacity', '')
    filtered_venues = []
    for v in venues:
        if capacity_filter:
            cap = v['capacity']
            if capacity_filter == 'Small' and int(cap) > 1000:
                continue
            elif capacity_filter == 'Medium' and (int(cap) <= 1000 or int(cap) > 3000):
                continue
            elif capacity_filter == 'Large' and int(cap) <= 3000:
                continue
        if search_query:
            if (search_query not in v['venue_name'].lower() and
                search_query not in v['location'].lower()):
                continue
        filtered_venues.append(v)
    capacities = ['Small', 'Medium', 'Large']
    return render_template('venues.html',
                           venues=filtered_venues,
                           capacities=capacities,
                           selected_capacity=capacity_filter,
                           search_query=search_query)
@app.route('/venues/<venue_id>')
def venue_details(venue_id):
    venues = read_venues()
    venue = next((v for v in venues if v['venue_id'] == venue_id), None)
    if not venue:
        return "Venue not found", 404
    return render_template('venue_details.html', venue=venue)
@app.route('/schedules')
def schedules_page():
    schedules = read_schedules()
    events = read_events()
    filter_date = request.args.get('date', '')
    filter_event = request.args.get('event', '')
    filtered_schedules = []
    for s in schedules:
        if filter_date:
            # session_time format: 'YYYY-MM-DD HH:MM'
            if not s['session_time'].startswith(filter_date):
                continue
        if filter_event and s['event_id'] != filter_event:
            continue
        filtered_schedules.append(s)
    return render_template('schedules.html',
                           schedules=filtered_schedules,
                           events=events,
                           filter_date=filter_date,
                           filter_event=filter_event)
@app.route('/bookings')
def bookings_summary():
    bookings = read_bookings()
    events = read_events()
    search_query = request.args.get('search', '').lower()
    filtered_bookings = []
    for b in bookings:
        event_name = next((e['event_name'] for e in events if e['event_id'] == b['event_id']), '')
        if search_query:
            if (search_query not in event_name.lower() and
                search_query not in b['booking_id']):
                continue
        b['event_name'] = event_name
        filtered_bookings.append(b)
    return render_template('bookings.html',
                           bookings=filtered_bookings,
                           search_query=search_query)
@app.route('/cancel-booking/<booking_id>', methods=['POST'])
def cancel_booking(booking_id):
    bookings = read_bookings()
    booking_found = False
    for b in bookings:
        if b['booking_id'] == booking_id:
            if b['status'].lower() == 'cancelled':
                # Already cancelled
                return redirect(url_for('bookings_summary'))
            b['status'] = 'Cancelled'
            booking_found = True
            break
    if not booking_found:
        return "Booking not found", 404
    # Write back updated bookings
    bookings_path = os.path.join(DATA_DIR, 'bookings.txt')
    with open(bookings_path, 'w', encoding='utf-8') as f:
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
    return redirect(url_for('bookings_summary'))
if __name__ == '__main__':
    app.run(debug=True)