from flask import Flask, render_template, request, redirect, url_for, flash
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Data directory
DATA_DIR = '.'

# ------------------------------
# File Reading/Writing Utilities
# ------------------------------

def read_events():
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
                events.append({
                    'event_id': parts[0],
                    'event_name': parts[1],
                    'category': parts[2],
                    'date': parts[3],
                    'time': parts[4],
                    'location': parts[5],
                    'description': parts[6],
                    'venue_id': parts[7],
                    'capacity': int(parts[8])
                })
    except FileNotFoundError:
        pass
    return events

def read_venues():
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
                venues.append({
                    'venue_id': parts[0],
                    'venue_name': parts[1],
                    'location': parts[2],
                    'capacity': int(parts[3]),
                    'amenities': parts[4],
                    'contact': parts[5]
                })
    except FileNotFoundError:
        pass
    return venues

def read_tickets():
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
                tickets.append({
                    'ticket_id': parts[0],
                    'event_id': parts[1],
                    'ticket_type': parts[2],
                    'price': float(parts[3]),
                    'available_count': int(parts[4]),
                    'sold_count': int(parts[5])
                })
    except FileNotFoundError:
        pass
    return tickets

def write_tickets(tickets):
    try:
        with open(os.path.join(DATA_DIR, 'tickets.txt'), 'w', encoding='utf-8') as f:
            for t in tickets:
                line = '|'.join([
                    t['ticket_id'], t['event_id'], t['ticket_type'],
                    f"{t['price']:.2f}", str(t['available_count']), str(t['sold_count'])])
                f.write(line + '\n')
    except Exception as e:
        print('Error writing tickets.txt:', e)


def read_bookings():
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
                bookings.append({
                    'booking_id': parts[0],
                    'event_id': parts[1],
                    'customer_name': parts[2],
                    'booking_date': parts[3],
                    'ticket_count': int(parts[4]),
                    'ticket_type': parts[5],
                    'total_amount': float(parts[6]),
                    'status': parts[7]
                })
    except FileNotFoundError:
        pass
    return bookings

def write_bookings(bookings):
    try:
        with open(os.path.join(DATA_DIR, 'bookings.txt'), 'w', encoding='utf-8') as f:
            for b in bookings:
                line = '|'.join([
                    b['booking_id'], b['event_id'], b['customer_name'],
                    b['booking_date'], str(b['ticket_count']), b['ticket_type'],
                    f"{b['total_amount']:.2f}", b['status']])
                f.write(line + '\n')
    except Exception as e:
        print('Error writing bookings.txt:', e)


def read_participants():
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
                participants.append({
                    'participant_id': parts[0],
                    'event_id': parts[1],
                    'name': parts[2],
                    'email': parts[3],
                    'booking_id': parts[4],
                    'status': parts[5],
                    'registration_date': parts[6]
                })
    except FileNotFoundError:
        pass
    return participants

def write_participants(participants):
    try:
        with open(os.path.join(DATA_DIR, 'participants.txt'), 'w', encoding='utf-8') as f:
            for p in participants:
                line = '|'.join([
                    p['participant_id'], p['event_id'], p['name'], p['email'],
                    p['booking_id'], p['status'], p['registration_date']])
                f.write(line + '\n')
    except Exception as e:
        print('Error writing participants.txt:', e)


def read_schedules():
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
                schedules.append({
                    'schedule_id': parts[0],
                    'event_id': parts[1],
                    'session_title': parts[2],
                    'session_time': parts[3],
                    'duration_minutes': int(parts[4]),
                    'speaker': parts[5],
                    'venue_id': parts[6]
                })
    except FileNotFoundError:
        pass
    return schedules


def find_event(event_id):
    for e in read_events():
        if e['event_id'] == event_id:
            return e
    return None

def find_venue(venue_id):
    for v in read_venues():
        if v['venue_id'] == venue_id:
            return v
    return None

# Helper: convert capacity filter string to actual range function

def capacity_to_class(cap):
    # Map capacity string to numeric ranges
    if cap == 'Small':
        return lambda x: x['capacity'] <= 100
    elif cap == 'Medium':
        return lambda x: 101 <= x['capacity'] <= 500
    elif cap == 'Large':
        return lambda x: x['capacity'] > 500
    else:
        return lambda x: True


# ------------------------------
# Routes
# ------------------------------

@app.route('/')
def dashboard():
    events = read_events()
    today = datetime.today().date()
    upcoming_events = [e for e in events if datetime.strptime(e['date'], '%Y-%m-%d').date() >= today]
    featured_events = sorted(upcoming_events, key=lambda e: e['date'])[:3]
    return render_template('dashboard.html', featured_events=featured_events)


@app.route('/events')
def events_listing():
    events = read_events()
    search = request.args.get('search', '').lower().strip()
    category_filter = request.args.get('category', '')
    filtered_events = events
    # Apply search filter
    if search:
        filtered_events = [e for e in filtered_events if (search in e['event_name'].lower() or search in e['location'].lower() or search in e['date'])]
    # Apply category filter
    if category_filter and category_filter != 'All':
        filtered_events = [e for e in filtered_events if e['category'] == category_filter]
    return render_template('events.html', events=filtered_events, search=search, category_filter=category_filter)


@app.route('/events/<event_id>')
def event_details(event_id):
    event = find_event(event_id)
    if not event:
        flash('Event not found')
        return redirect(url_for('events_listing'))
    return render_template('event_details.html', event=event)


@app.route('/book_ticket', methods=['GET', 'POST'])
def book_ticket():
    events = read_events()
    tickets = read_tickets()
    booking_confirmation = None
    event_name = ''

    selected_event_id = request.args.get('event_id', '')

    if request.method == 'POST':
        event_id = request.form.get('select-event-dropdown', '')
        ticket_quantity = request.form.get('ticket-quantity-input', '')
        ticket_type = request.form.get('ticket-type-select', '')
        customer_name = request.form.get('customer_name', '').strip()

        if not event_id or not ticket_quantity or not ticket_type or not customer_name:
            flash('Please fill all required fields.')
            return redirect(request.url)

        try:
            ticket_quantity = int(ticket_quantity)
            if ticket_quantity <= 0:
                flash('Ticket quantity must be positive integer.')
                return redirect(request.url)
        except ValueError:
            flash('Invalid ticket quantity.')
            return redirect(request.url)

        # Find ticket info
        ticket_info = next((t for t in tickets if t['event_id'] == event_id and t['ticket_type'] == ticket_type), None)
        if not ticket_info:
            flash('Selected ticket type not available for this event.')
            return redirect(request.url)

        if ticket_info['available_count'] < ticket_quantity:
            flash('Not enough tickets available.')
            return redirect(request.url)

        total_amount = ticket_info['price'] * ticket_quantity

        # Generate new booking_id
        bookings = read_bookings()
        max_id = max([int(b['booking_id']) for b in bookings], default=0)
        new_booking_id = str(max_id + 1)

        booking_date = datetime.today().strftime('%Y-%m-%d')

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

        # Update tickets
        for t in tickets:
            if t['event_id'] == event_id and t['ticket_type'] == ticket_type:
                t['available_count'] -= ticket_quantity
                t['sold_count'] += ticket_quantity

        write_bookings(bookings)
        write_tickets(tickets)

        booking_confirmation = new_booking

    # Obtain event_name for confirmation display
    if booking_confirmation:
        ev = find_event(booking_confirmation['event_id'])
        event_name = ev['event_name'] if ev else booking_confirmation['event_id']

    return render_template('book_ticket.html', events=events, booking_confirmation=booking_confirmation, selected_event_id=selected_event_id, event_name=event_name)


@app.route('/participants')
def participants_page():
    participants = read_participants()
    search = request.args.get('search', '').lower().strip()
    status_filter = request.args.get('status', '')

    filtered = participants
    if search:
        filtered = [p for p in filtered if search in p['name'].lower() or search in p['email'].lower()]
    if status_filter and status_filter != 'All':
        filtered = [p for p in filtered if p['status'] == status_filter]

    # Prepare event_name for each participant
    events_map = {e['event_id']: e['event_name'] for e in read_events()}
    for p in filtered:
        p['event_name'] = events_map.get(p['event_id'], 'Unknown Event')

    return render_template('participants.html', participants=filtered, search=search, status_filter=status_filter)


@app.route('/venues')
def venues_page():
    venues = read_venues()
    search_term = request.args.get('search', '').lower().strip()
    capacity_filter = request.args.get('capacity', '')

    filtered = venues
    if search_term:
        filtered = [v for v in filtered if search_term in v['venue_name'].lower() or search_term in v['location'].lower()]

    if capacity_filter and capacity_filter != 'All':
        filter_func = capacity_to_class(capacity_filter)
        filtered = list(filter(filter_func, filtered))

    return render_template('venues.html', venues=filtered, search=search_term, capacity_filter=capacity_filter)


@app.route('/schedules')
def schedules_page():
    schedules = read_schedules()
    events = read_events()

    filter_date = request.args.get('date', '')
    filter_event = request.args.get('event', '')

    filtered = schedules
    if filter_date:
        filtered = [s for s in filtered if s['session_time'].startswith(filter_date)]
    if filter_event and filter_event != 'All':
        filtered = [s for s in filtered if s['event_id'] == filter_event]

    return render_template('schedules.html', schedules=filtered, events=events, filter_date=filter_date, filter_event=filter_event)


@app.route('/bookings')
def bookings_page():
    bookings = read_bookings()
    events = {e['event_id']: e for e in read_events()}
    search = request.args.get('search', '').lower().strip()

    filtered = bookings
    if search:
        filtered = [b for b in filtered if (b['booking_id'] == search or search in events.get(b['event_id'], {}).get('event_name', '').lower())]

    return render_template('bookings.html', bookings=filtered, events=events, search=search)


@app.route('/cancel_booking/<booking_id>', methods=['POST'])
def cancel_booking(booking_id):
    bookings = read_bookings()
    canceled = False
    for b in bookings:
        if b['booking_id'] == booking_id and b['status'] != 'Cancelled':
            b['status'] = 'Cancelled'
            canceled = True
            break
    if canceled:
        write_bookings(bookings)
        flash(f'Booking {booking_id} cancelled.')
    else:
        flash('Booking not found or already cancelled.')
    return redirect(url_for('bookings_page'))


if __name__ == '__main__':
    app.run(debug=True)
