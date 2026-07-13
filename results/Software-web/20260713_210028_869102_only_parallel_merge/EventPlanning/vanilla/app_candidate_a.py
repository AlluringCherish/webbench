from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__, template_folder='templates_candidate_a')

data_path = 'data'

# Utility functions to parse pipe delimited text files

# Return list of dicts based on keys
# Skip malformed lines
# Provide fallback empty list if file missing
# Trim whitespace

def parse_pipe_delimited_file(filename, keys):
    records = []
    filepath = os.path.join(data_path, filename)
    if not os.path.isfile(filepath):
        return records
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) < len(keys):
                continue
            record = {k: v.strip() for k, v in zip(keys, parts)}
            records.append(record)
    return records

# Load data functions

def load_all_events():
    keys = ['event_id','event_name','category','date','time','location','description','venue_id','capacity']
    events = parse_pipe_delimited_file('events.txt', keys)
    # event_id,capacity => int
    for e in events:
        try:
            e['event_id'] = int(e['event_id'])
        except:
            e['event_id'] = None
        try:
            e['capacity'] = int(e['capacity'])
        except:
            e['capacity'] = 0
    return events

def load_featured_events():
    # For simplicity, featured events = those occurring in future within 90 days (from now date), sorted by date ascending, top 3
    events = load_all_events()
    # parse date
    def parse_date(e):
        try:
            return datetime.strptime(e['date'], '%Y-%m-%d')
        except:
            return datetime.min

    from datetime import datetime, timedelta
    now = datetime.now()
    upcoming_events = [e for e in events if parse_date(e) >= now and parse_date(e) <= now+timedelta(days=90)]
    upcoming_events.sort(key=parse_date)
    featured = upcoming_events[:3]
    return [{ 'event_id': e['event_id'], 'event_name': e['event_name'], 'date': e['date'], 'location': e['location'], 'description': e['description'], 'venue_id': e['venue_id']} for e in featured]


def load_all_venues():
    keys = ['venue_id','venue_name','location','capacity','amenities','contact']
    venues = parse_pipe_delimited_file('venues.txt', keys)
    # venue_id, capacity => int
    for v in venues:
        try:
            v['venue_id'] = int(v['venue_id'])
        except:
            v['venue_id'] = None
        try:
            v['capacity'] = int(v['capacity'])
        except:
            v['capacity'] = 0
    return venues


def load_featured_venues():
    venues = load_all_venues()
    # Define featured venues arbitrarily as top 3 by capacity descending
    venues.sort(key=lambda x: x['capacity'], reverse=True)
    featured = venues[:3]
    # return keys as per spec
    return [{ 'venue_id': v['venue_id'], 'venue_name': v['venue_name'], 'location': v['location'], 'capacity': v['capacity'], 'amenities': v['amenities']} for v in featured]

# Filter events by search query and category
# Search by event_name, location or date substring (case insensitive)
def filter_events(events, search_query, category_filter):
    filtered = []
    sq = search_query.lower() if search_query else ''
    cat = category_filter.lower() if category_filter else ''
    for e in events:
        match_search = (sq in e['event_name'].lower() or sq in e['location'].lower() or sq in e['date'].lower()) if sq else True
        match_cat = (e['category'].lower() == cat) if cat else True
        if match_search and match_cat:
            filtered.append(e)
    return filtered

# Get event by id

def get_event_by_id(event_id):
    events = load_all_events()
    for e in events:
        if e['event_id'] == event_id:
            return e
    return None

# Load tickets

def load_all_tickets():
    keys = ['ticket_id','event_id','ticket_type','price','available_count','sold_count']
    tickets = parse_pipe_delimited_file('tickets.txt', keys)
    for t in tickets:
        try:
            t['ticket_id'] = int(t['ticket_id'])
        except:
            t['ticket_id'] = None
        try:
            t['event_id'] = int(t['event_id'])
        except:
            t['event_id'] = None
        try:
            t['price'] = float(t['price'])
        except:
            t['price'] = 0.0
        try:
            t['available_count'] = int(t['available_count'])
        except:
            t['available_count'] = 0
        try:
            t['sold_count'] = int(t['sold_count'])
        except:
            t['sold_count'] = 0
    return tickets

# Load bookings

def load_all_bookings():
    keys = ['booking_id','event_id','customer_name','booking_date','ticket_count','ticket_type','total_amount','status']
    bookings = parse_pipe_delimited_file('bookings.txt', keys)
    # Convert numeric
    for b in bookings:
        try:
            b['booking_id'] = int(b['booking_id'])
        except:
            b['booking_id'] = None
        try:
            b['event_id'] = int(b['event_id'])
        except:
            b['event_id'] = None
        try:
            b['ticket_count'] = int(b['ticket_count'])
        except:
            b['ticket_count'] = 0
        try:
            b['total_amount'] = float(b['total_amount'])
        except:
            b['total_amount'] = 0.0
    # Add event_name for convenience
    events = load_all_events()
    event_map = {e['event_id']:e['event_name'] for e in events}
    for b in bookings:
        b['event_name'] = event_map.get(b['event_id'], 'Unknown')
    return bookings

# Cancel booking by id (set status to "Cancelled")
def cancel_booking_by_id(booking_id):
    if booking_id is None:
        return False
    bookings = load_all_bookings()
    changed = False
    for b in bookings:
        if b['booking_id'] == booking_id:
            if b['status'].lower() != 'cancelled':
                b['status'] = 'Cancelled'
                changed = True
            break
    if not changed:
        return False
    # Write back to bookings.txt
    lines = []
    for b in bookings:
        line = f"{b['booking_id']}|{b['event_id']}|{b['customer_name']}|{b['booking_date']}|{b['ticket_count']}|{b['ticket_type']}|{b['total_amount']:.2f}|{b['status']}"
        lines.append(line)
    filepath = os.path.join(data_path, 'bookings.txt')
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n')
    return True

# Filter bookings by search
# search by event_name or booking_id string

def filter_bookings(bookings, search_query):
    if not search_query:
        return bookings
    sq = search_query.lower()
    filtered = []
    for b in bookings:
        if sq in b['event_name'].lower() or sq in str(b['booking_id']):
            filtered.append(b)
    return filtered

# Process ticket booking
from datetime import date

def process_booking(event_id, ticket_quantity, ticket_type):
    booking_confirmation = None
    events = load_all_events()
    tickets = load_all_tickets()
    # Validate event_id valid
    event = None
    for e in events:
        if e['event_id'] == event_id:
            event = e
            break
    if not event:
        return {'error': 'Invalid event selected.'}
    # Validate ticket type available for event
    ticket_matches = [t for t in tickets if t['event_id'] == event_id and t['ticket_type'].lower() == ticket_type.lower()]
    if not ticket_matches:
        return {'error': 'Tickets for selected type not found.'}
    ticket = ticket_matches[0]
    # Validate ticket quantity positive and <= availability
    if ticket_quantity <= 0:
        return {'error': 'Ticket quantity must be positive.'}
    available = ticket['available_count'] - ticket['sold_count']
    if ticket_quantity > available:
        return {'error': f'Not enough tickets available. Only {available} left.'}

    # Create a new booking entry
    bookings = load_all_bookings()
    max_booking_id = max([b['booking_id'] for b in bookings], default=0)
    new_booking_id = max_booking_id + 1
    # For simplicity customer_name = "Guest" and booking date is today
    today_str = date.today().strftime('%Y-%m-%d')
    total_amount = ticket_quantity * ticket['price']
    new_booking = {
        'booking_id': new_booking_id,
        'event_id': event_id,
        'customer_name': 'Guest',
        'booking_date': today_str,
        'ticket_count': ticket_quantity,
        'ticket_type': ticket_type,
        'total_amount': total_amount,
        'status': 'Confirmed'
    }
    bookings.append(new_booking)
    # Write bookings back
    lines = []
    for b in bookings:
        line = f"{b['booking_id']}|{b['event_id']}|{b['customer_name']}|{b['booking_date']}|{b['ticket_count']}|{b['ticket_type']}|{b['total_amount']:.2f}|{b['status']}"
        lines.append(line)
    filepath = os.path.join(data_path, 'bookings.txt')
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n')
    # Return booking confirmation data
    booking_confirmation = {
        'booking_id': new_booking_id,
        'event_name': event['event_name'],
        'ticket_quantity': ticket_quantity,
        'ticket_type': ticket_type,
        'total_amount': total_amount,
        'status': 'Confirmed'
    }
    return booking_confirmation

# Participants

def load_all_participants():
    keys = ['participant_id','event_id','name','email','booking_id','status','registration_date']
    participants = parse_pipe_delimited_file('participants.txt', keys)
    # Convert numeric IDs
    for p in participants:
        try:
            p['participant_id'] = int(p['participant_id'])
        except:
            p['participant_id'] = None
        try:
            p['event_id'] = int(p['event_id'])
        except:
            p['event_id'] = None
        try:
            p['booking_id'] = int(p['booking_id'])
        except:
            p['booking_id'] = None
    # Map event name
    events = load_all_events()
    event_map = {e['event_id']:e['event_name'] for e in events}
    for p in participants:
        p['event_name'] = event_map.get(p['event_id'], 'Unknown')
    return participants

# Filter participants
# Search by name or email substring
# Filter by status exact

def filter_participants(participants, search_query, status_filter):
    sq = search_query.lower() if search_query else ''
    sf = status_filter.lower() if status_filter else ''
    filtered = []
    for p in participants:
        match_search = (sq in p['name'].lower() or sq in p['email'].lower()) if sq else True
        match_status = (p['status'].lower() == sf) if sf else True
        if match_search and match_status:
            filtered.append(p)
    return filtered

# Filter venues
# Search by name or location substring (case insensitive)
# Filter by capacity category: Small(<=1000), Medium(1001-3000), Large(>3000)
def filter_venues(venues, search_query, capacity_filter):
    sq = search_query.lower() if search_query else ''
    cf = capacity_filter.lower() if capacity_filter else ''
    filtered = []
    for v in venues:
        match_search = (sq in v['venue_name'].lower() or sq in v['location'].lower()) if sq else True
        if cf == 'small':
            match_capacity = v['capacity'] <= 1000
        elif cf == 'medium':
            match_capacity = 1001 <= v['capacity'] <= 3000
        elif cf == 'large':
            match_capacity = v['capacity'] > 3000
        else:
            match_capacity = True
        if match_search and match_capacity:
            filtered.append(v)
    return filtered

# Load all schedules

def load_all_schedules():
    keys = ['schedule_id','event_id','session_title','session_time','duration_minutes','speaker','venue_id']
    schedules = parse_pipe_delimited_file('schedules.txt', keys)
    # Convert numeric id's and duration
    for s in schedules:
        try:
            s['schedule_id'] = int(s['schedule_id'])
        except:
            s['schedule_id'] = None
        try:
            s['event_id'] = int(s['event_id'])
        except:
            s['event_id'] = None
        try:
            s['duration_minutes'] = int(s['duration_minutes'])
        except:
            s['duration_minutes'] = 0
        try:
            s['venue_id'] = int(s['venue_id'])
        except:
            s['venue_id'] = None
    # Map event name
    events = load_all_events()
    event_map = {e['event_id']:e['event_name'] for e in events}
    for s in schedules:
        s['event_name'] = event_map.get(s['event_id'], 'Unknown')
    return schedules

# Filter schedules
# date filter matches session_time date portion
# event filter matches event_id or event_name

def filter_schedules(schedules, filter_date, filter_event):
    filtered = []
    fdate = filter_date.strip() if filter_date else ''
    fevent = filter_event.strip().lower() if filter_event else ''
    for s in schedules:
        match_date = True
        match_event = True
        if fdate:
            # session_time format example: 2025-03-15 09:00
            try:
                date_part = s['session_time'].split()[0]
                if date_part != fdate:
                    match_date = False
            except:
                match_date = False
        if fevent:
            if fevent.isdigit():
                match_event = (str(s['event_id']) == fevent)
            else:
                match_event = (fevent in s['event_name'].lower())
        if match_date and match_event:
            filtered.append(s)
    return filtered


# Routes

@app.route('/', methods=['GET'])
def dashboard():
    featured_events = load_featured_events()
    featured_venues = load_featured_venues()
    return render_template('dashboard.html', featured_events=featured_events, featured_venues=featured_venues)

@app.route('/events', methods=['GET'])
def events_listing():
    events = load_all_events()
    categories = ["Conference", "Concert", "Sports", "Workshop", "Social"]
    search_query = request.args.get('search', '')
    category_filter = request.args.get('category', '')
    filtered_events = filter_events(events, search_query, category_filter)
    return render_template('events.html', events=filtered_events, categories=categories, search_query=search_query, category_filter=category_filter)

@app.route('/events/<int:event_id>', methods=['GET'])
def event_details(event_id):
    event = get_event_by_id(event_id)
    if not event:
        return "Event not found", 404
    return render_template('event_details.html', event=event)

@app.route('/bookings/book', methods=['GET', 'POST'])
def book_tickets():
    events = load_all_events()
    # Simplify events to event_id and event_name only
    events_simple = [{'event_id': e['event_id'], 'event_name': e['event_name']} for e in events]
    ticket_types = ["General", "VIP", "Early Bird"]
    booking_confirmation = None
    selected_event_id = request.args.get('event_id', type=int)

    if request.method == 'POST':
        try:
            selected_event_id = int(request.form['select-event-dropdown'])
            ticket_quantity = int(request.form['ticket-quantity-input'])
            ticket_type = request.form['ticket-type-select']
            booking_confirmation = process_booking(selected_event_id, ticket_quantity, ticket_type)
        except Exception as ex:
            booking_confirmation = {'error': 'An error occurred processing the booking.'}

    return render_template('ticket_booking.html', events=events_simple, ticket_types=ticket_types, selected_event_id=selected_event_id, booking_confirmation=booking_confirmation)

@app.route('/participants', methods=['GET'])
def participants_management():
    participants = load_all_participants()
    status_options = ["Registered", "Confirmed", "Attended"]
    search_query = request.args.get('search', '')
    status_filter = request.args.get('status', '')
    filtered_participants = filter_participants(participants, search_query, status_filter)
    return render_template('participants.html', participants=filtered_participants, status_options=status_options, search_query=search_query, status_filter=status_filter)

@app.route('/venues', methods=['GET'])
def venues_page():
    venues = load_all_venues()
    capacities = ["Small", "Medium", "Large"]
    search_query = request.args.get('search', '')
    capacity_filter = request.args.get('capacity', '')
    filtered_venues = filter_venues(venues, search_query, capacity_filter)
    return render_template('venues.html', venues=filtered_venues, capacities=capacities, search_query=search_query, capacity_filter=capacity_filter)

@app.route('/schedules', methods=['GET'])
def event_schedules():
    schedules = load_all_schedules()
    events = load_all_events()
    filter_date = request.args.get('date', '')
    filter_event = request.args.get('event', '')
    filtered_schedules = filter_schedules(schedules, filter_date, filter_event)
    return render_template('schedules.html', schedules=filtered_schedules, events=events, filter_date=filter_date, filter_event=filter_event)

@app.route('/bookings', methods=['GET'])
def bookings_summary():
    bookings = load_all_bookings()
    search_query = request.args.get('search', '')
    filtered_bookings = filter_bookings(bookings, search_query)
    return render_template('bookings.html', bookings=filtered_bookings, search_query=search_query)

@app.route('/cancel_booking/<int:booking_id>', methods=['POST'])
def cancel_booking(booking_id):
    cancel_booking_by_id(booking_id)
    return redirect(url_for('bookings_summary'))

@app.route('/back_to_dashboard', methods=['GET'])
def back_to_dashboard():
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
