from flask import Flask, render_template, request, redirect, url_for
import os
import csv
from datetime import datetime, date, timedelta

app = Flask(__name__, template_folder='templates')

data_path = 'data'

# Utility functions to load and parse pipe delimited data files

def parse_pipe_delimited_file(filename, fieldnames):
    filepath = os.path.join(data_path, filename)
    data = []
    if not os.path.exists(filepath):
        return data
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='|', fieldnames=fieldnames)
        for row in reader:
            clean_row = {k: (v.strip() if v is not None else '') for k,v in row.items()}
            data.append(clean_row)
    return data

# Load all events

def load_all_events():
    fieldnames = ['event_id','event_name','category','date','time','location','description','venue_id','capacity']
    events = parse_pipe_delimited_file('events.txt', fieldnames)
    for e in events:
        try:
            e['event_id'] = int(e['event_id'])
        except:
            e['event_id'] = None
        try:
            e['capacity'] = int(e['capacity'])
        except:
            e['capacity'] = 0
    return [e for e in events if e['event_id'] is not None]

# Load featured events - upcoming 3 events within 90 days from now

def load_featured_events():
    events = load_all_events()
    def parse_date(e):
        try:
            return datetime.strptime(e['date'], '%Y-%m-%d')
        except:
            return datetime.min

    now = datetime.now()
    upcoming_events = [e for e in events if parse_date(e) >= now and parse_date(e) <= now + timedelta(days=90)]
    upcoming_events.sort(key=parse_date)
    return upcoming_events[:3]

# Load all venues

def load_all_venues():
    fieldnames = ['venue_id','venue_name','location','capacity','amenities','contact']
    venues = parse_pipe_delimited_file('venues.txt', fieldnames)
    for v in venues:
        try:
            v['venue_id'] = int(v['venue_id'])
        except:
            v['venue_id'] = None
        try:
            v['capacity'] = int(v['capacity'])
        except:
            v['capacity'] = 0
    return [v for v in venues if v['venue_id'] is not None]

# Load featured venues - top 3 by capacity descending

def load_featured_venues():
    venues = load_all_venues()
    venues.sort(key=lambda x: x['capacity'], reverse=True)
    return venues[:3]

# Filter events by search query and category

def filter_events(events, search_query, category_filter):
    filtered = []
    sq = search_query.lower() if search_query else ''
    cf = category_filter.lower() if category_filter else ''
    for e in events:
        match_cat = (e['category'].lower() == cf) if cf else True
        match_search = (sq in e['event_name'].lower() or sq in e['location'].lower() or sq in e['date'].lower()) if sq else True
        if match_cat and match_search:
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
    fieldnames = ['ticket_id','event_id','ticket_type','price','available_count','sold_count']
    tickets = parse_pipe_delimited_file('tickets.txt', fieldnames)
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
    return [t for t in tickets if t['ticket_id'] is not None]

# Update tickets.txt sold_count

def update_ticket_sold_count(ticket_id, sold_increment):
    tickets_file = os.path.join(data_path, 'tickets.txt')
    if not os.path.exists(tickets_file):
        return
    lines = []
    with open(tickets_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    updated_lines = []
    for line in lines:
        parts = line.strip().split('|')
        if len(parts) < 6:
            updated_lines.append(line)
            continue
        try:
            tid = int(parts[0])
        except:
            updated_lines.append(line)
            continue
        if tid == ticket_id:
            try:
                current_sold = int(parts[5])
            except:
                current_sold = 0
            new_sold = current_sold + sold_increment
            if new_sold > int(parts[4]):
                new_sold = int(parts[4])
            parts[5] = str(new_sold)
            new_line = '|'.join(parts) + '\n'
            updated_lines.append(new_line)
        else:
            updated_lines.append(line)
    with open(tickets_file, 'w', encoding='utf-8') as f:
        f.writelines(updated_lines)

# Process booking

def process_booking(selected_event_id, ticket_quantity, ticket_type):
    if ticket_quantity <= 0:
        return {'error': 'Ticket quantity must be at least 1.'}
    tickets = load_all_tickets()
    matching_tickets = [t for t in tickets if t['event_id'] == selected_event_id and t['ticket_type'].lower() == ticket_type.lower()]
    if not matching_tickets:
        return {'error': 'Selected ticket type not available for this event.'}
    ticket_info = matching_tickets[0]
    available = ticket_info['available_count'] - ticket_info['sold_count']
    if ticket_quantity > available:
        return {'error': f'Only {available} tickets are available for the selected type.'}
    total_amount = ticket_info['price'] * ticket_quantity
    bookings = load_all_bookings()
    max_booking_id = max([b['booking_id'] for b in bookings], default=0)
    new_booking_id = max_booking_id + 1
    customer_name = 'Guest'
    booking_date = date.today().strftime('%Y-%m-%d')

    new_booking_line = f"{new_booking_id}|{selected_event_id}|{customer_name}|{booking_date}|{ticket_quantity}|{ticket_type}|{total_amount:.2f}|Confirmed\n"
    bookings_file = os.path.join(data_path, 'bookings.txt')
    try:
        with open(bookings_file, 'a', encoding='utf-8') as f:
            f.write(new_booking_line)
    except Exception:
        return {'error': 'Failed to save booking. Please try again later.'}

    update_ticket_sold_count(ticket_info['ticket_id'], ticket_quantity)

    return {
        'booking_id': new_booking_id,
        'event_name': get_event_by_id(selected_event_id)['event_name'],
        'ticket_quantity': ticket_quantity,
        'ticket_type': ticket_type,
        'total_amount': total_amount,
        'status': 'Confirmed'
    }

# Load all participants

def load_all_participants():
    fieldnames = ['participant_id','event_id','name','email','booking_id','status','registration_date']
    participants = parse_pipe_delimited_file('participants.txt', fieldnames)
    for p in participants:
        try:
            p['participant_id'] = int(p['participant_id'])
        except:
            p['participant_id'] = None
        try:
            p['event_id'] = int(p['event_id'])
        except:
            p['event_id'] = None
    return [p for p in participants if p['participant_id'] is not None]

# Filter participants

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

# Load all bookings

def load_all_bookings():
    fieldnames = ['booking_id','event_id','customer_name','booking_date','ticket_count','ticket_type','total_amount','status']
    bookings = parse_pipe_delimited_file('bookings.txt', fieldnames)
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
    # Attach event_name
    events = load_all_events()
    event_map = {e['event_id']: e['event_name'] for e in events}
    filtered_bookings = []
    for b in bookings:
        if b['booking_id'] is None:
            continue
        b['event_name'] = event_map.get(b['event_id'], 'Unknown')
        filtered_bookings.append(b)
    return filtered_bookings

# Filter bookings

def filter_bookings(bookings, search_query):
    sq = search_query.lower() if search_query else ''
    filtered = []
    for b in bookings:
        if sq and sq not in b['event_name'].lower() and sq not in str(b['booking_id']):
            continue
        filtered.append(b)
    return filtered

# Cancel booking

def cancel_booking_by_id(booking_id):
    bookings_file = os.path.join(data_path, 'bookings.txt')
    if not os.path.exists(bookings_file):
        return False
    lines = []
    with open(bookings_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    changed = False
    new_lines = []
    for line in lines:
        parts = line.strip().split('|')
        if len(parts) < 8:
            new_lines.append(line)
            continue
        try:
            bkid = int(parts[0])
        except:
            new_lines.append(line)
            continue
        if bkid == booking_id:
            if parts[7].lower() != 'cancelled':
                parts[7] = 'Cancelled'
                changed = True
            new_line = '|'.join(parts) + '\n'
            new_lines.append(new_line)
        else:
            new_lines.append(line)
    if changed:
        with open(bookings_file, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
            return True
    return False

# Load all schedules

def load_all_schedules():
    fieldnames = ['schedule_id','event_id','session_title','session_time','duration_minutes','speaker','venue_id']
    schedules = parse_pipe_delimited_file('schedules.txt', fieldnames)
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
    return [s for s in schedules if s['schedule_id'] is not None]

# Filter schedules

def filter_schedules(schedules, filter_date, filter_event):
    filtered = []
    fd = filter_date.strip() if filter_date else ''
    fe = filter_event.strip().lower() if filter_event else ''
    for s in schedules:
        match_date = True
        match_event = True
        if fd:
            try:
                date_part = s['session_time'].split()[0]
                if date_part != fd:
                    match_date = False
            except:
                match_date = False
        if fe:
            if fe.isdigit():
                match_event = (str(s['event_id']) == fe)
            else:
                event = get_event_by_id(s['event_id'])
                match_event = fe in event['event_name'].lower() if event else False
        if match_date and match_event:
            filtered.append(s)
    return filtered


# Filter venues

def filter_venues(venues, search_query, capacity_filter):
    filtered = []
    sq = search_query.lower() if search_query else ''
    cf = capacity_filter.lower() if capacity_filter else ''
    capacity_ranges = {
        'small': (0, 100),
        'medium': (101, 500),
        'large': (501, 10000)
    }
    for v in venues:
        match_search = (sq in v['venue_name'].lower() or sq in v['location'].lower()) if sq else True
        match_capacity = True
        if cf:
            crange = capacity_ranges.get(cf)
            if crange:
                match_capacity = crange[0] <= v['capacity'] <= crange[1]
        if match_search and match_capacity:
            filtered.append(v)
    return filtered


# Flask Routes

@ app.route('/', methods=['GET'])
def dashboard():
    featured_events = load_featured_events()
    featured_venues = load_featured_venues()
    return render_template('dashboard.html', featured_events=featured_events, featured_venues=featured_venues)

@ app.route('/events', methods=['GET'])
def events_listing():
    events = load_all_events()
    categories = ["Conference", "Concert", "Sports", "Workshop", "Social"]
    search_query = request.args.get('search', '')
    category_filter = request.args.get('category', '')
    filtered_events = filter_events(events, search_query, category_filter)
    return render_template('events.html', events=filtered_events, categories=categories, search_query=search_query, category_filter=category_filter)

@ app.route('/events/<int:event_id>', methods=['GET'])
def event_details(event_id):
    event = get_event_by_id(event_id)
    if not event:
        return "Event not found", 404
    return render_template('event_details.html', event=event)

@ app.route('/bookings/book', methods=['GET', 'POST'])
def book_tickets():
    events = load_all_events()
    ticket_types = ["General", "VIP", "Early Bird"]
    booking_confirmation = None
    selected_event_id = request.args.get('event_id', type=int)

    if request.method == 'POST':
        try:
            selected_event_id = int(request.form['select-event-dropdown'])
            ticket_quantity = int(request.form['ticket-quantity-input'])
            ticket_type = request.form['ticket-type-select']
        except Exception:
            booking_confirmation = {'error': 'Invalid form data submitted.'}
        else:
            booking_confirmation = process_booking(selected_event_id, ticket_quantity, ticket_type)

    return render_template('ticket_booking.html', events=events, ticket_types=ticket_types, selected_event_id=selected_event_id, booking_confirmation=booking_confirmation)

@ app.route('/participants', methods=['GET'])
def participants_management():
    participants_raw = load_all_participants()
    status_options = ["Registered", "Confirmed", "Attended"]
    search_query = request.args.get('search', '')
    status_filter = request.args.get('status', '')
    filtered_participants = filter_participants(participants_raw, search_query, status_filter)
    events = load_all_events()
    event_map = {e['event_id']: e['event_name'] for e in events}
    for p in filtered_participants:
        p['event_name'] = event_map.get(p['event_id'], 'Unknown')
    return render_template('participants.html', participants=filtered_participants, status_options=status_options, search_query=search_query, status_filter=status_filter)

@ app.route('/venues', methods=['GET'])
def venues_page():
    venues = load_all_venues()
    capacities = ["Small", "Medium", "Large"]
    search_query = request.args.get('search', '')
    capacity_filter = request.args.get('capacity', '')
    filtered_venues = filter_venues(venues, search_query, capacity_filter)
    return render_template('venues.html', venues=filtered_venues, capacities=capacities, search_query=search_query, capacity_filter=capacity_filter)

@ app.route('/schedules', methods=['GET'])
def event_schedules():
    schedules = load_all_schedules()
    events = load_all_events()
    filter_date = request.args.get('date', '')
    filter_event = request.args.get('event', '')
    filtered_schedules = filter_schedules(schedules, filter_date, filter_event)
    return render_template('schedules.html', schedules=filtered_schedules, events=events, filter_date=filter_date, filter_event=filter_event)

@ app.route('/bookings', methods=['GET'])
def bookings_summary():
    bookings = load_all_bookings()
    search_query = request.args.get('search', '')
    filtered_bookings = filter_bookings(bookings, search_query)
    return render_template('bookings.html', bookings=filtered_bookings, search_query=search_query)

@ app.route('/cancel_booking/<int:booking_id>', methods=['POST'])
def cancel_booking(booking_id):
    cancel_booking_by_id(booking_id)
    return redirect(url_for('bookings_summary'))

@ app.route('/back_to_dashboard', methods=['GET'])
def back_to_dashboard():
    return redirect(url_for('dashboard'))


if __name__ == '__main__':
    app.run(debug=True)
