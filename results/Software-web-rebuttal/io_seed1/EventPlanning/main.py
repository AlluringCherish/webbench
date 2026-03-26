'''
Main backend Flask application for EventPlanning web application.
Defines routes for all pages starting with '/' as Dashboard.
Ensures all frontend navigation uses routing URLs consistent with backend routes.
'''
from flask import Flask, render_template, request, redirect, url_for
import os
import datetime
app = Flask(__name__)
DATA_DIR = 'data'
def read_events():
    events = []
    try:
        with open(os.path.join(DATA_DIR, 'events.txt'), 'r', encoding='utf-8') as f:
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
                    if len(parts) == 6:
                        ticket = {
                            'ticket_id': parts[0],
                            'event_id': parts[1],
                            'ticket_type': parts[2],
                            'price': parts[3],
                            'available_count': int(parts[4]),
                            'sold_count': int(parts[5])
                        }
                        tickets.append(ticket)
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
                    if len(parts) == 8:
                        booking = {
                            'booking_id': parts[0],
                            'event_id': parts[1],
                            'customer_name': parts[2],
                            'booking_date': parts[3],
                            'ticket_count': parts[4],
                            'ticket_type': parts[5],
                            'total_amount': parts[6],
                            'status': parts[7]
                        }
                        bookings.append(booking)
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
                    if len(parts) == 7:
                        schedule = {
                            'schedule_id': parts[0],
                            'event_id': parts[1],
                            'session_title': parts[2],
                            'session_time': parts[3],
                            'duration_minutes': parts[4],
                            'speaker': parts[5],
                            'venue_id': parts[6]
                        }
                        schedules.append(schedule)
    except FileNotFoundError:
        pass
    return schedules
@app.route('/')
def dashboard():
    events = read_events()
    venues = read_venues()
    # For featured events, pick first 3 upcoming events sorted by date
    upcoming_events = sorted(events, key=lambda e: e['date'])[:3]
    # For featured venues, pick first 3 venues
    featured_venues = venues[:3]
    return render_template('dashboard.html', events=upcoming_events, venues=featured_venues)
@app.route('/events')
def events_listing():
    events = read_events()
    category_filter = request.args.get('category', '')
    search_query = request.args.get('search', '').lower()
    filtered_events = events
    if category_filter:
        filtered_events = [e for e in filtered_events if e['category'].lower() == category_filter.lower()]
    if search_query:
        filtered_events = [e for e in filtered_events if search_query in e['event_name'].lower() or search_query in e['location'].lower() or search_query in e['date']]
    return render_template('events.html', events=filtered_events, category_filter=category_filter, search_query=search_query)
@app.route('/event/<event_id>')
def event_details(event_id):
    events = read_events()
    event = next((e for e in events if e['event_id'] == event_id), None)
    if not event:
        return "Event not found", 404
    return render_template('event_details.html', event=event)
@app.route('/tickets', methods=['GET', 'POST'])
def ticket_booking():
    events = read_events()
    tickets = read_tickets()
    booking_confirmation = None
    if request.method == 'POST':
        event_id = request.form.get('select-event-dropdown')
        ticket_quantity = request.form.get('ticket-quantity-input')
        ticket_type = request.form.get('ticket-type-select')
        customer_name = request.form.get('customer-name-input', 'Guest')
        try:
            ticket_quantity = int(ticket_quantity)
            if ticket_quantity <= 0:
                raise ValueError
        except (ValueError, TypeError):
            return render_template('tickets.html', events=events, booking_confirmation="Invalid ticket quantity.")
        # Find ticket info
        ticket_info = next((t for t in tickets if t['event_id'] == event_id and t['ticket_type'] == ticket_type), None)
        if not ticket_info:
            return render_template('tickets.html', events=events, booking_confirmation="Ticket type not available for selected event.")
        if ticket_info['available_count'] < ticket_quantity:
            return render_template('tickets.html', events=events, booking_confirmation="Not enough tickets available.")
        # Calculate total amount
        total_amount = float(ticket_info['price']) * ticket_quantity
        # Generate new booking_id
        bookings = read_bookings()
        if bookings:
            max_booking_id = max(int(b['booking_id']) for b in bookings)
        else:
            max_booking_id = 0
        new_booking_id = str(max_booking_id + 1)
        booking_date = datetime.date.today().isoformat()
        new_booking = f"{new_booking_id}|{event_id}|{customer_name}|{booking_date}|{ticket_quantity}|{ticket_type}|{total_amount:.2f}|Confirmed\n"
        # Append booking to bookings.txt
        with open(os.path.join(DATA_DIR, 'bookings.txt'), 'a', encoding='utf-8') as f:
            f.write(new_booking)
        # Update tickets.txt sold_count and available_count
        updated_tickets = []
        for t in tickets:
            if t['ticket_id'] == ticket_info['ticket_id']:
                t['sold_count'] += ticket_quantity
                t['available_count'] -= ticket_quantity
            updated_tickets.append(t)
        with open(os.path.join(DATA_DIR, 'tickets.txt'), 'w', encoding='utf-8') as f:
            for t in updated_tickets:
                line = f"{t['ticket_id']}|{t['event_id']}|{t['ticket_type']}|{t['price']}|{t['available_count']}|{t['sold_count']}\n"
                f.write(line)
        booking_confirmation = f"Booking confirmed! Booking ID: {new_booking_id}, Total Amount: ${total_amount:.2f}"
    return render_template('tickets.html', events=events, booking_confirmation=booking_confirmation)
@app.route('/participants')
def participants_management():
    participants = read_participants()
    events = read_events()
    search_query = request.args.get('search', '').lower()
    status_filter = request.args.get('status', '')
    filtered_participants = participants
    if status_filter:
        filtered_participants = [p for p in filtered_participants if p['status'].lower() == status_filter.lower()]
    if search_query:
        filtered_participants = [p for p in filtered_participants if search_query in p['name'].lower() or search_query in p['email'].lower()]
    # Map event names for participants
    event_dict = {e['event_id']: e['event_name'] for e in events}
    for p in filtered_participants:
        p['event_name'] = event_dict.get(p['event_id'], 'Unknown')
    return render_template('participants.html', participants=filtered_participants, search_query=search_query, status_filter=status_filter)
@app.route('/venues')
def venues_page():
    venues = read_venues()
    search_query = request.args.get('search', '').lower()
    capacity_filter = request.args.get('capacity', '')
    filtered_venues = venues
    if capacity_filter:
        if capacity_filter.lower() == 'small':
            filtered_venues = [v for v in filtered_venues if int(v['capacity']) < 500]
        elif capacity_filter.lower() == 'medium':
            filtered_venues = [v for v in filtered_venues if 500 <= int(v['capacity']) < 2000]
        elif capacity_filter.lower() == 'large':
            filtered_venues = [v for v in filtered_venues if int(v['capacity']) >= 2000]
    if search_query:
        filtered_venues = [v for v in filtered_venues if search_query in v['venue_name'].lower() or search_query in v['location'].lower()]
    return render_template('venues.html', venues=filtered_venues, search_query=search_query, capacity_filter=capacity_filter)
@app.route('/venue/<venue_id>')
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
    filtered_schedules = schedules
    if filter_date:
        filtered_schedules = [s for s in filtered_schedules if s['session_time'].startswith(filter_date)]
    if filter_event:
        filtered_schedules = [s for s in filtered_schedules if s['event_id'] == filter_event]
    # Map event names for schedules
    event_dict = {e['event_id']: e['event_name'] for e in events}
    for s in filtered_schedules:
        s['event_name'] = event_dict.get(s['event_id'], 'Unknown')
    return render_template('schedules.html', schedules=filtered_schedules, events=events, filter_date=filter_date, filter_event=filter_event)
@app.route('/export_schedule')
def export_schedule():
    # Export schedules data as CSV
    schedules = read_schedules()
    import csv
    from io import StringIO
    si = StringIO()
    cw = csv.writer(si)
    cw.writerow(['Schedule ID', 'Event ID', 'Session Title', 'Session Time', 'Duration (minutes)', 'Speaker', 'Venue ID'])
    for s in schedules:
        cw.writerow([s['schedule_id'], s['event_id'], s['session_title'], s['session_time'], s['duration_minutes'], s['speaker'], s['venue_id']])
    output = si.getvalue()
    from flask import Response
    return Response(output, mimetype="text/csv", headers={"Content-Disposition":"attachment;filename=schedules.csv"})
@app.route('/bookings')
def bookings_summary():
    bookings = read_bookings()
    events = read_events()
    search_query = request.args.get('search', '').lower()
    filtered_bookings = bookings
    if search_query:
        filtered_bookings = [b for b in filtered_bookings if search_query in b['booking_id'] or search_query in b['event_id']]
    # Map event names for bookings
    event_dict = {e['event_id']: e['event_name'] for e in events}
    for b in filtered_bookings:
        b['event_name'] = event_dict.get(b['event_id'], 'Unknown')
    return render_template('bookings.html', bookings=filtered_bookings, search_query=search_query)
@app.route('/cancel_booking/<booking_id>', methods=['POST'])
def cancel_booking(booking_id):
    bookings = read_bookings()
    booking_found = False
    for b in bookings:
        if b['booking_id'] == booking_id:
            if b['status'].lower() != 'cancelled':
                b['status'] = 'Cancelled'
                booking_found = True
            break
    if booking_found:
        with open(os.path.join(DATA_DIR, 'bookings.txt'), 'w', encoding='utf-8') as f:
            for b in bookings:
                line = f"{b['booking_id']}|{b['event_id']}|{b['customer_name']}|{b['booking_date']}|{b['ticket_count']}|{b['ticket_type']}|{b['total_amount']}|{b['status']}\n"
                f.write(line)
    return redirect(url_for('bookings_summary'))
if __name__ == '__main__':
    app.run(debug=True)