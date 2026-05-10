'''
Main backend application for EventPlanning web application.
Handles routing, reading/writing data from local text files,
searching, booking, and persistence.
No authentication required; all features are directly accessible.
The website starts from the Dashboard page at route '/'.
'''
import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Needed for flash messages
DATA_DIR = 'data'
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
def write_schedules(schedules):
    path = os.path.join(DATA_DIR, 'schedules.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for s in schedules:
            line = '|'.join([
                s['schedule_id'],
                s['event_id'],
                s['session_title'],
                s['session_time'],
                str(s['duration_minutes']),
                s['speaker'],
                s['venue_id']
            ])
            f.write(line + '\n')
def get_next_id(items, id_key):
    max_id = 0
    for item in items:
        try:
            current_id = int(item[id_key])
            if current_id > max_id:
                max_id = current_id
        except ValueError:
            continue
    return str(max_id + 1)
@app.route('/')
def dashboard():
    events = read_events()
    venues = read_venues()
    # Filter upcoming events (date >= today), sort by date ascending, select top 3
    today = datetime.now().date()
    upcoming_events = sorted(
        [e for e in events if datetime.strptime(e['date'], '%Y-%m-%d').date() >= today],
        key=lambda x: x['date']
    )[:3]
    # Select featured venues (top 3 by capacity descending)
    featured_venues = sorted(venues, key=lambda x: x['capacity'], reverse=True)[:3]
    return render_template('dashboard.html', events=upcoming_events, venues=featured_venues, page_title='Event Planning Dashboard')
@app.route('/events', methods=['GET'])
def events_listing():
    events = read_events()
    search_query = request.args.get('search', '').strip().lower()
    category_filter = request.args.get('category', 'All')
    filtered_events = events
    if search_query:
        filtered_events = [e for e in filtered_events if
                           search_query in e['event_name'].lower() or
                           search_query in e['location'].lower() or
                           search_query in e['date']]
    if category_filter and category_filter != 'All':
        filtered_events = [e for e in filtered_events if e['category'].lower() == category_filter.lower()]
    return render_template('events_listing.html', events=filtered_events, search_query=request.args.get('search', ''), category_filter=category_filter, page_title='Events Catalog')
@app.route('/event/<event_id>')
def event_details(event_id):
    events = read_events()
    event = next((e for e in events if e['event_id'] == event_id), None)
    if not event:
        flash('Event not found.', 'error')
        return redirect(url_for('events_listing'))
    return render_template('event_details.html', event=event, page_title='Event Details')
@app.route('/book-tickets', methods=['GET', 'POST'])
def ticket_booking():
    events = read_events()
    tickets = read_tickets()
    booking_confirmation = None
    if request.method == 'POST':
        event_id = request.form.get('select-event-dropdown')
        ticket_quantity_str = request.form.get('ticket-quantity-input')
        ticket_type = request.form.get('ticket-type-select')
        customer_name = request.form.get('customer-name-input', '').strip()
        if not event_id or not ticket_quantity_str or not ticket_type or not customer_name:
            flash('Please fill in all required fields.', 'error')
            return redirect(url_for('ticket_booking'))
        try:
            ticket_quantity = int(ticket_quantity_str)
            if ticket_quantity <= 0:
                flash('Ticket quantity must be a positive number.', 'error')
                return redirect(url_for('ticket_booking'))
        except ValueError:
            flash('Invalid ticket quantity.', 'error')
            return redirect(url_for('ticket_booking'))
        # Find ticket info for event and ticket type
        ticket = next((t for t in tickets if t['event_id'] == event_id and t['ticket_type'].lower() == ticket_type.lower()), None)
        if not ticket:
            flash('Selected ticket type not available for this event.', 'error')
            return redirect(url_for('ticket_booking'))
        if ticket_quantity > ticket['available_count']:
            flash(f'Only {ticket["available_count"]} tickets available for selected type.', 'error')
            return redirect(url_for('ticket_booking'))
        # Calculate total amount
        total_amount = ticket['price'] * ticket_quantity
        bookings = read_bookings()
        new_booking_id = get_next_id(bookings, 'booking_id')
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
        write_bookings(bookings)
        # Update ticket counts
        for t in tickets:
            if t['ticket_id'] == ticket['ticket_id']:
                t['available_count'] -= ticket_quantity
                t['sold_count'] += ticket_quantity
                break
        write_tickets(tickets)
        booking_confirmation = new_booking
        return render_template('ticket_booking.html', booking_confirmation=booking_confirmation, page_title='Book Your Tickets')
    else:
        # GET request
        return render_template('ticket_booking.html', events=events, booking_confirmation=None, page_title='Book Your Tickets')
@app.route('/participants', methods=['GET', 'POST'])
def participants_management():
    participants = read_participants()
    events = read_events()
    bookings = read_bookings()
    search_query = request.args.get('search', '').strip().lower()
    status_filter = request.args.get('status', 'All')
    filtered_participants = participants
    if search_query:
        filtered_participants = [p for p in filtered_participants if search_query in p['name'].lower() or search_query in p['email'].lower()]
    if status_filter and status_filter != 'All':
        filtered_participants = [p for p in filtered_participants if p['status'] == status_filter]
    if request.method == 'POST':
        name = request.form.get('participant-name', '').strip()
        email = request.form.get('participant-email', '').strip()
        event_id = request.form.get('participant-event-id', '').strip()
        booking_id = request.form.get('participant-booking-id', '').strip()
        status = request.form.get('participant-status', '').strip()
        if not name or not email or not event_id or not booking_id or not status:
            flash('Please fill in all fields to add a participant.', 'error')
            return redirect(url_for('participants_management'))
        # Validate event exists
        if not any(e['event_id'] == event_id for e in events):
            flash('Selected event does not exist.', 'error')
            return redirect(url_for('participants_management'))
        # Validate booking exists
        if not any(b['booking_id'] == booking_id for b in bookings):
            flash('Booking ID does not exist.', 'error')
            return redirect(url_for('participants_management'))
        new_participant_id = get_next_id(participants, 'participant_id')
        registration_date = datetime.now().strftime('%Y-%m-%d')
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
        flash('Participant added successfully.', 'success')
        return redirect(url_for('participants_management'))
    return render_template('participants_management.html', participants=filtered_participants, events=events, search_query=request.args.get('search', ''), status_filter=status_filter, page_title='Participants Management')
@app.route('/venues', methods=['GET'])
def venues():
    venues = read_venues()
    search_query = request.args.get('search', '').strip().lower()
    capacity_filter = request.args.get('capacity', 'All')
    filtered_venues = venues
    if search_query:
        filtered_venues = [v for v in filtered_venues if search_query in v['venue_name'].lower() or search_query in v['location'].lower()]
    if capacity_filter and capacity_filter != 'All':
        def capacity_category(cap):
            if cap <= 500:
                return 'Small'
            elif cap <= 2000:
                return 'Medium'
            else:
                return 'Large'
        filtered_venues = [v for v in filtered_venues if capacity_category(v['capacity']) == capacity_filter]
    return render_template('venues.html', venues=filtered_venues, search_query=request.args.get('search', ''), capacity_filter=capacity_filter, page_title='Venues')
@app.route('/schedules', methods=['GET'])
def event_schedules():
    schedules = read_schedules()
    events = read_events()
    venues = read_venues()
    filter_date = request.args.get('date', '').strip()
    filter_event = request.args.get('event', 'All')
    filtered_schedules = schedules
    if filter_date:
        filtered_schedules = [s for s in filtered_schedules if s['session_time'].startswith(filter_date)]
    if filter_event and filter_event != 'All':
        filtered_schedules = [s for s in filtered_schedules if s['event_id'] == filter_event]
    filtered_schedules = sorted(filtered_schedules, key=lambda s: s['session_time'])
    return render_template('event_schedules.html', schedules=filtered_schedules, events=events, venues=venues, filter_date=filter_date, filter_event=filter_event, page_title='Event Schedules')
@app.route('/export-schedule')
def export_schedule():
    schedules = read_schedules()
    lines = []
    for s in schedules:
        line = '|'.join([
            s['schedule_id'],
            s['event_id'],
            s['session_title'],
            s['session_time'],
            str(s['duration_minutes']),
            s['speaker'],
            s['venue_id']
        ])
        lines.append(line)
    content = '\n'.join(lines)
    from flask import Response
    return Response(
        content,
        mimetype='text/plain',
        headers={'Content-Disposition': 'attachment;filename=schedules_export.txt'}
    )
@app.route('/bookings', methods=['GET', 'POST'])
def bookings_summary():
    bookings = read_bookings()
    events = read_events()
    search_query = request.args.get('search', '').strip().lower()
    filtered_bookings = bookings
    if search_query:
        filtered_bookings = [b for b in filtered_bookings if
                             search_query in b['booking_id'].lower() or
                             any(e['event_id'] == b['event_id'] and search_query in e['event_name'].lower() for e in events)]
    if request.method == 'POST':
        cancel_booking_id = request.form.get('cancel-booking-id')
        if not cancel_booking_id:
            flash('No ID provided for cancellation.', 'error')
            return redirect(url_for('bookings_summary'))
        booking = next((b for b in bookings if b['booking_id'] == cancel_booking_id), None)
        if not booking:
            flash('Booking ID not found.', 'error')
            return redirect(url_for('bookings_summary'))
        if booking['status'].lower() == 'cancelled':
            flash('Booking already cancelled.', 'info')
            return redirect(url_for('bookings_summary'))
        # Update booking status
        booking['status'] = 'Cancelled'
        # Update tickets sold and available counts accordingly
        tickets = read_tickets()
        for t in tickets:
            if t['event_id'] == booking['event_id'] and t['ticket_type'].lower() == booking['ticket_type'].lower():
                t['available_count'] += booking['ticket_count']
                t['sold_count'] -= booking['ticket_count']
                break
        write_tickets(tickets)
        write_bookings(bookings)
        flash(f'Booking {cancel_booking_id} cancelled successfully.', 'success')
        return redirect(url_for('bookings_summary'))
    return render_template('bookings_summary.html', bookings=filtered_bookings, events=events, search_query=request.args.get('search', ''), page_title='My Bookings')
if __name__ == '__main__':
    app.run(debug=True)