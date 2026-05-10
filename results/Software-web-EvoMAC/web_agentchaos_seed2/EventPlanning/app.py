'''
Main backend Python application for the EventPlanning web application.
Implements all routing, data reading/writing, user input processing, and rendering
of templates for the eight pages as specified in the requirements.
Uses Flask framework and local text files in 'data' directory for data storage.
No authentication is required; all features are directly accessible.
'''
from flask import Flask, render_template, request, redirect, url_for, flash
import os
import datetime
app = Flask(__name__)
app.secret_key = 'evomac-eventplanning-secret'  # Needed for flashing messages
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
# Utility functions for reading and writing data files
def read_events():
    events = []
    path = os.path.join(DATA_DIR, 'events.txt')
    if not os.path.exists(path):
        return events
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 9:
                continue
            event = {
                'event_id': parts[0],
                'event_name': parts[1],
                'category': parts[2],
                'date': parts[3],
                'time': parts[4],
                'location': parts[5],
                'description': parts[6],
                'venue_id': parts[7],
                'capacity': int(parts[8])
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
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 6:
                continue
            venue = {
                'venue_id': parts[0],
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
    if not os.path.exists(path):
        return tickets
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 6:
                continue
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
def write_tickets(tickets):
    path = os.path.join(DATA_DIR, 'tickets.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for t in tickets:
            line = '|'.join([
                t['ticket_id'],
                t['event_id'],
                t['ticket_type'],
                f"{t['price']:.2f}",
                str(t['available_count']),
                str(t['sold_count'])
            ])
            f.write(line + '\n')
def read_bookings():
    bookings = []
    path = os.path.join(DATA_DIR, 'bookings.txt')
    if not os.path.exists(path):
        return bookings
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 8:
                continue
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
def write_bookings(bookings):
    path = os.path.join(DATA_DIR, 'bookings.txt')
    with open(path, 'w', encoding='utf-8') as f:
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
def read_participants():
    participants = []
    path = os.path.join(DATA_DIR, 'participants.txt')
    if not os.path.exists(path):
        return participants
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 7:
                continue
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
def write_participants(participants):
    path = os.path.join(DATA_DIR, 'participants.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for p in participants:
            line = '|'.join([
                p['participant_id'],
                p['event_id'],
                p['name'],
                p['email'],
                p['booking_id'],
                p['status'],
                p['registration_date']
            ])
            f.write(line + '\n')
def read_schedules():
    schedules = []
    path = os.path.join(DATA_DIR, 'schedules.txt')
    if not os.path.exists(path):
        return schedules
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 7:
                continue
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
# Helper to get next ID for new entries
def get_next_id(items, id_key):
    max_id = 0
    for item in items:
        try:
            val = int(item[id_key])
            if val > max_id:
                max_id = val
        except:
            continue
    return str(max_id + 1)
# Route: Dashboard page ("/")
@app.route('/')
def dashboard():
    events = read_events()
    venues = read_venues()
    # Featured events: pick upcoming events sorted by date ascending, limit 3
    today = datetime.date.today()
    upcoming_events = [e for e in events if datetime.datetime.strptime(e['date'], '%Y-%m-%d').date() >= today]
    upcoming_events.sort(key=lambda e: e['date'])
    featured_events = upcoming_events[:3]
    # Featured venues: pick first 3 venues (could be improved)
    featured_venues = venues[:3]
    return render_template('dashboard.html',
                           featured_events=featured_events,
                           featured_venues=featured_venues)
# Route: Events Listing page
@app.route('/events', methods=['GET', 'POST'])
def events_listing():
    events = read_events()
    search_query = request.args.get('search', '').strip().lower()
    category_filter = request.args.get('category', '').strip()
    filtered_events = events
    # Filter by search query (name, location, date)
    if search_query:
        filtered_events = [e for e in filtered_events if
                           search_query in e['event_name'].lower() or
                           search_query in e['location'].lower() or
                           search_query in e['date']]
    # Filter by category
    if category_filter and category_filter != 'All':
        filtered_events = [e for e in filtered_events if e['category'].lower() == category_filter.lower()]
    # Sort by date ascending
    filtered_events.sort(key=lambda e: e['date'])
    categories = ['All', 'Conference', 'Concert', 'Sports', 'Workshop', 'Social']
    return render_template('events_listing.html',
                           events=filtered_events,
                           search_query=search_query,
                           category_filter=category_filter,
                           categories=categories)
# Route: Event Details page
@app.route('/event/<event_id>')
def event_details(event_id):
    events = read_events()
    event = next((e for e in events if e['event_id'] == event_id), None)
    if not event:
        flash('Event not found.', 'error')
        return redirect(url_for('events_listing'))
    return render_template('event_details.html', event=event)
# Route: Ticket Booking page
@app.route('/book_ticket', methods=['GET', 'POST'])
def ticket_booking():
    events = read_events()
    tickets = read_tickets()
    if request.method == 'POST':
        event_id = request.form.get('select-event-dropdown')
        ticket_quantity_str = request.form.get('ticket-quantity-input')
        ticket_type = request.form.get('ticket-type-select')
        customer_name = request.form.get('customer-name', '').strip()
        # Validate inputs
        if not event_id or not ticket_quantity_str or not ticket_type or not customer_name:
            flash('Please fill in all booking fields.', 'error')
            return redirect(url_for('ticket_booking'))
        try:
            ticket_quantity = int(ticket_quantity_str)
            if ticket_quantity <= 0:
                raise ValueError
        except ValueError:
            flash('Ticket quantity must be a positive integer.', 'error')
            return redirect(url_for('ticket_booking'))
        # Find ticket info for event and ticket_type
        ticket = next((t for t in tickets if t['event_id'] == event_id and t['ticket_type'].lower() == ticket_type.lower()), None)
        if not ticket:
            flash('Selected ticket type not available for this event.', 'error')
            return redirect(url_for('ticket_booking'))
        # Check availability
        available = ticket['available_count'] - ticket['sold_count']
        if ticket_quantity > available:
            flash(f'Only {available} tickets available for selected type.', 'error')
            return redirect(url_for('ticket_booking'))
        # Calculate total amount
        total_amount = ticket_quantity * ticket['price']
        # Create new booking
        bookings = read_bookings()
        new_booking_id = get_next_id(bookings, 'booking_id')
        booking_date = datetime.date.today().strftime('%Y-%m-%d')
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
        write_bookings(bookings)
        # Update tickets sold_count
        for t in tickets:
            if t['ticket_id'] == ticket['ticket_id']:
                t['sold_count'] += ticket_quantity
                break
        write_tickets(tickets)
        # Add participants for each ticket booked (participant info not collected here, so add placeholder participants)
        participants = read_participants()
        for i in range(ticket_quantity):
            new_participant_id = get_next_id(participants, 'participant_id')
            participant = {
                'participant_id': new_participant_id,
                'event_id': event_id,
                'name': customer_name,  # Since no participant name input, use customer name
                'email': '',  # No email collected here
                'booking_id': new_booking_id,
                'status': 'Registered',
                'registration_date': booking_date
            }
            participants.append(participant)
        write_participants(participants)
        confirmation = {
            'booking_id': new_booking_id,
            'event_id': event_id,
            'customer_name': customer_name,
            'ticket_count': ticket_quantity,
            'ticket_type': ticket_type,
            'total_amount': total_amount,
            'status': 'Confirmed'
        }
        return render_template('ticket_booking.html',
                               events=events,
                               confirmation=confirmation)
    # GET request: show booking form
    return render_template('ticket_booking.html', events=events, confirmation=None)
# Route: Participants Management page
@app.route('/participants', methods=['GET', 'POST'])
def participants_management():
    participants = read_participants()
    events = read_events()
    search_query = request.args.get('search', '').strip().lower()
    status_filter = request.args.get('status', '').strip()
    filtered_participants = participants
    # Filter by search query (name or email)
    if search_query:
        filtered_participants = [p for p in filtered_participants if
                                 search_query in p['name'].lower() or
                                 search_query in p['email'].lower()]
    # Filter by status
    if status_filter and status_filter != 'All':
        filtered_participants = [p for p in filtered_participants if p['status'].lower() == status_filter.lower()]
    # For display, enrich participants with event name
    event_dict = {e['event_id']: e['event_name'] for e in events}
    for p in filtered_participants:
        p['event_name'] = event_dict.get(p['event_id'], 'Unknown')
    statuses = ['All', 'Registered', 'Confirmed', 'Attended']
    # Handle adding new participant (POST)
    if request.method == 'POST':
        name = request.form.get('participant-name', '').strip()
        email = request.form.get('participant-email', '').strip()
        event_id = request.form.get('participant-event-id', '').strip()
        booking_id = request.form.get('participant-booking-id', '').strip()
        status = request.form.get('participant-status', 'Registered').strip()
        registration_date = datetime.date.today().strftime('%Y-%m-%d')
        if not name or not email or not event_id:
            flash('Name, email, and event are required to add a participant.', 'error')
            return redirect(url_for('participants_management'))
        # Generate new participant_id
        new_participant_id = get_next_id(participants, 'participant_id')
        new_participant = {
            'participant_id': new_participant_id,
            'event_id': event_id,
            'name': name,
            'email': email,
            'booking_id': booking_id if booking_id else '',
            'status': status,
            'registration_date': registration_date
        }
        participants.append(new_participant)
        write_participants(participants)
        flash('Participant added successfully.', 'success')
        return redirect(url_for('participants_management'))
    return render_template('participants_management.html',
                           participants=filtered_participants,
                           search_query=search_query,
                           status_filter=status_filter,
                           statuses=statuses,
                           events=events)
# Route: Venues Information page
@app.route('/venues')
def venues_page():
    venues = read_venues()
    search_query = request.args.get('search', '').strip().lower()
    capacity_filter = request.args.get('capacity', '').strip()
    filtered_venues = venues
    # Filter by search query (name or location)
    if search_query:
        filtered_venues = [v for v in filtered_venues if
                           search_query in v['venue_name'].lower() or
                           search_query in v['location'].lower()]
    # Filter by capacity
    if capacity_filter and capacity_filter != 'All':
        def capacity_category(cap):
            if cap <= 500:
                return 'Small'
            elif cap <= 2000:
                return 'Medium'
            else:
                return 'Large'
        filtered_venues = [v for v in filtered_venues if capacity_category(v['capacity']) == capacity_filter]
    capacities = ['All', 'Small', 'Medium', 'Large']
    return render_template('venues.html',
                           venues=filtered_venues,
                           search_query=search_query,
                           capacity_filter=capacity_filter,
                           capacities=capacities)
# Route: Venue Details page (optional, not explicitly required but button exists)
@app.route('/venue/<venue_id>')
def venue_details(venue_id):
    venues = read_venues()
    venue = next((v for v in venues if v['venue_id'] == venue_id), None)
    if not venue:
        flash('Venue not found.', 'error')
        return redirect(url_for('venues_page'))
    return render_template('venue_details.html', venue=venue)
# Route: Event Schedules page
@app.route('/schedules', methods=['GET'])
def event_schedules():
    schedules = read_schedules()
    events = read_events()
    filter_date = request.args.get('date', '').strip()
    filter_event = request.args.get('event', '').strip()
    filtered_schedules = schedules
    # Filter by date
    if filter_date:
        filtered_schedules = [s for s in filtered_schedules if s['session_time'].startswith(filter_date)]
    # Filter by event
    if filter_event and filter_event != 'All':
        filtered_schedules = [s for s in filtered_schedules if s['event_id'] == filter_event]
    # Sort schedules by session_time ascending
    filtered_schedules.sort(key=lambda s: s['session_time'])
    event_options = ['All'] + [e['event_id'] for e in events]
    # Enrich schedules with event name and venue name
    event_dict = {e['event_id']: e['event_name'] for e in events}
    venues = read_venues()
    venue_dict = {v['venue_id']: v['venue_name'] for v in venues}
    for s in filtered_schedules:
        s['event_name'] = event_dict.get(s['event_id'], 'Unknown')
        s['venue_name'] = venue_dict.get(s['venue_id'], 'Unknown')
    return render_template('event_schedules.html',
                           schedules=filtered_schedules,
                           filter_date=filter_date,
                           filter_event=filter_event,
                           event_options=event_options)
# Route: Export schedule data (simple CSV download)
@app.route('/export_schedule')
def export_schedule():
    schedules = read_schedules()
    events = read_events()
    event_dict = {e['event_id']: e['event_name'] for e in events}
    venues = read_venues()
    venue_dict = {v['venue_id']: v['venue_name'] for v in venues}
    # Prepare CSV content
    lines = ['schedule_id,event_name,session_title,session_time,duration_minutes,speaker,venue_name']
    for s in schedules:
        event_name = event_dict.get(s['event_id'], 'Unknown')
        venue_name = venue_dict.get(s['venue_id'], 'Unknown')
        line = ','.join([
            s['schedule_id'],
            f'"{event_name}"',
            f'"{s["session_title"]}"',
            s['session_time'],
            str(s['duration_minutes']),
            f'"{s["speaker"]}"',
            f'"{venue_name}"'
        ])
        lines.append(line)
    csv_content = '\n'.join(lines)
    from flask import Response
    return Response(
        csv_content,
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment;filename=event_schedules.csv'}
    )
# Route: Bookings Summary page
@app.route('/bookings', methods=['GET', 'POST'])
def bookings_summary():
    bookings = read_bookings()
    events = read_events()
    event_dict = {e['event_id']: e['event_name'] for e in events}
    search_query = request.args.get('search', '').strip().lower()
    filtered_bookings = bookings
    # Filter by event name or booking ID
    if search_query:
        filtered_bookings = [b for b in filtered_bookings if
                             search_query in event_dict.get(b['event_id'], '').lower() or
                             search_query in b['booking_id']]
    # Enrich bookings with event name
    for b in filtered_bookings:
        b['event_name'] = event_dict.get(b['event_id'], 'Unknown')
    # Handle cancellation (POST)
    if request.method == 'POST':
        cancel_id = request.form.get('cancel_booking_id')
        if cancel_id:
            booking = next((b for b in bookings if b['booking_id'] == cancel_id), None)
            if booking:
                if booking['status'].lower() == 'cancelled':
                    flash('Booking already cancelled.', 'info')
                else:
                    booking['status'] = 'Cancelled'
                    write_bookings(bookings)
                    flash(f'Booking {cancel_id} cancelled successfully.', 'success')
            else:
                flash('Booking not found.', 'error')
            return redirect(url_for('bookings_summary'))
    return render_template('bookings_summary.html',
                           bookings=filtered_bookings,
                           search_query=search_query)
# Route: Back to dashboard button handler (redirect)
@app.route('/back_to_dashboard')
def back_to_dashboard():
    return redirect(url_for('dashboard'))
if __name__ == '__main__':
    app.run(port=5000, debug=True)