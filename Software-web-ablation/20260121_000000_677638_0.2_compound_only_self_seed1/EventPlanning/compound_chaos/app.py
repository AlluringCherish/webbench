from flask import Flask, render_template, redirect, url_for, request
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Utility functions to load pipe-delimited data

def load_events():
    events = []
    try:
        with open(os.path.join(DATA_DIR, 'events.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 9:
                    continue
                events.append({
                    'event_id': int(parts[0]),
                    'event_name': parts[1],
                    'category': parts[2],
                    'date': parts[3],
                    'time': parts[4],
                    'location': parts[5],
                    'description': parts[6],
                    'venue_id': int(parts[7]),
                    'capacity': int(parts[8])
                })
    except Exception:
        pass
    return events

def load_venues():
    venues = []
    try:
        with open(os.path.join(DATA_DIR, 'venues.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 6:
                    continue
                venues.append({
                    'venue_id': int(parts[0]),
                    'venue_name': parts[1],
                    'location': parts[2],
                    'capacity': int(parts[3]),
                    'amenities': parts[4],
                    'contact': parts[5]
                })
    except Exception:
        pass
    return venues

def load_tickets():
    tickets = []
    try:
        with open(os.path.join(DATA_DIR, 'tickets.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 6:
                    continue
                tickets.append({
                    'ticket_id': int(parts[0]),
                    'event_id': int(parts[1]),
                    'ticket_type': parts[2],
                    'price': float(parts[3]),
                    'available_count': int(parts[4]),
                    'sold_count': int(parts[5])
                })
    except Exception:
        pass
    return tickets

def load_bookings():
    bookings = []
    try:
        with open(os.path.join(DATA_DIR, 'bookings.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 8:
                    continue
                bookings.append({
                    'booking_id': int(parts[0]),
                    'event_id': int(parts[1]),
                    'customer_name': parts[2],
                    'booking_date': parts[3],
                    'ticket_count': int(parts[4]),
                    'ticket_type': parts[5],
                    'total_amount': float(parts[6]),
                    'status': parts[7]
                })
    except Exception:
        pass
    return bookings

def load_participants():
    participants = []
    try:
        with open(os.path.join(DATA_DIR, 'participants.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 7:
                    continue
                participants.append({
                    'participant_id': int(parts[0]),
                    'event_id': int(parts[1]),
                    'name': parts[2],
                    'email': parts[3],
                    'booking_id': int(parts[4]),
                    'status': parts[5],
                    'registration_date': parts[6]
                })
    except Exception:
        pass
    return participants

def load_schedules():
    schedules = []
    try:
        with open(os.path.join(DATA_DIR, 'schedules.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 7:
                    continue
                schedules.append({
                    'schedule_id': int(parts[0]),
                    'event_id': int(parts[1]),
                    'session_title': parts[2],
                    'session_time': parts[3],
                    'duration_minutes': int(parts[4]),
                    'speaker': parts[5],
                    'venue_id': int(parts[6])
                })
    except Exception:
        pass
    return schedules


# Flask routes

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard_page'))


@app.route('/dashboard')
def dashboard_page():
    featured_events = load_events()[:5]
    featured_venues = load_venues()[:5]
    return render_template('dashboard.html', featured_events=featured_events, featured_venues=featured_venues)


@app.route('/events')
def events_listing():
    events = load_events()
    categories = ['Conference', 'Concert', 'Sports', 'Workshop', 'Social']
    search_query = request.args.get('search', '').lower()
    category_filter = request.args.get('category', '')

    filtered_events = []
    for event in events:
        matches_search = (search_query == '' or
                          search_query in event['event_name'].lower() or
                          search_query in event['location'].lower() or
                          search_query in event['date'])
        matches_category = (category_filter == '' or category_filter == event['category'])
        if matches_search and matches_category:
            filtered_events.append(event)

    return render_template('events.html', events=filtered_events, categories=categories)


@app.route('/event/<int:event_id>')
def event_details(event_id):
    events = load_events()
    event = next((e for e in events if e['event_id'] == event_id), None)
    if event is None:
        return redirect(url_for('events_listing'))
    tickets = [t for t in load_tickets() if t['event_id'] == event_id]
    return render_template('event_details.html', event=event, tickets=tickets)


@app.route('/book_ticket', methods=['GET', 'POST'])
def ticket_booking():
    events = load_events()
    if request.method == 'GET':
        return render_template('ticket_booking.html', events=events)

    form = request.form
    try:
        event_id = int(form.get('event_id', ''))
        ticket_type = form.get('ticket_type', '').strip()
        ticket_count = int(form.get('ticket_count', ''))
        customer_name = form.get('customer_name', '').strip()
    except (ValueError, TypeError):
        error_message = 'Invalid form data submitted.'
        return render_template('ticket_booking.html', events=events, error_message=error_message)

    event = next((e for e in events if e['event_id'] == event_id), None)
    if event is None:
        error_message = 'Selected event does not exist.'
        return render_template('ticket_booking.html', events=events, error_message=error_message)

    tickets = load_tickets()
    ticket = next((t for t in tickets if t['event_id'] == event_id and t['ticket_type'] == ticket_type), None)
    if ticket is None:
        error_message = 'Selected ticket type not available for this event.'
        return render_template('ticket_booking.html', events=events, error_message=error_message)

    if ticket_count <= 0:
        error_message = 'Ticket count must be a positive integer.'
        return render_template('ticket_booking.html', events=events, error_message=error_message)

    if ticket['available_count'] < ticket_count:
        error_message = f"Only {ticket['available_count']} tickets available for selected ticket type."
        return render_template('ticket_booking.html', events=events, error_message=error_message)

    bookings = load_bookings()
    new_booking_id = max((b['booking_id'] for b in bookings), default=0) + 1
    booking_date = datetime.now().strftime('%Y-%m-%d')
    total_amount = ticket_count * ticket['price']

    booking_confirmation = {
        'booking_id': new_booking_id,
        'event_id': event_id,
        'customer_name': customer_name,
        'booking_date': booking_date,
        'ticket_count': ticket_count,
        'ticket_type': ticket_type,
        'total_amount': total_amount,
        'status': 'Confirmed'
    }

    tickets_all = load_tickets()
    updated = False
    for t in tickets_all:
        if t['ticket_id'] == ticket['ticket_id']:
            t['available_count'] -= ticket_count
            t['sold_count'] += ticket_count
            updated = True
            break

    if not updated:
        error_message = 'Failed to update ticket availability.'
        return render_template('ticket_booking.html', events=events, error_message=error_message)

    try:
        with open(os.path.join(DATA_DIR, 'tickets.txt'), 'w', encoding='utf-8') as f:
            for t in tickets_all:
                f.write(f"{t['ticket_id']}|{t['event_id']}|{t['ticket_type']}|{t['price']}|{t['available_count']}|{t['sold_count']}\n")
    except Exception:
        error_message = 'Failed to save updated tickets.'
        return render_template('ticket_booking.html', events=events, error_message=error_message)

    try:
        with open(os.path.join(DATA_DIR, 'bookings.txt'), 'a', encoding='utf-8') as f:
            f.write(f"{booking_confirmation['booking_id']}|{booking_confirmation['event_id']}|{booking_confirmation['customer_name']}|{booking_confirmation['booking_date']}|{booking_confirmation['ticket_count']}|{booking_confirmation['ticket_type']}|{booking_confirmation['total_amount']}|{booking_confirmation['status']}\n")
    except Exception:
        error_message = 'Failed to save booking.'
        return render_template('ticket_booking.html', events=events, error_message=error_message)

    return render_template('ticket_booking.html', booking_confirmation=booking_confirmation)

@app.route('/participants', methods=['GET', 'POST'])
def participants_management():
    participants = load_participants()
    search_query = request.args.get('search_query', '').strip().lower()
    status_filter = request.args.get('status_filter', '').strip()

    filtered_participants = []
    for p in participants:
        matches_search = (search_query == '' or search_query in p['name'].lower() or search_query in p['email'].lower())
        matches_status = (status_filter == '' or status_filter == p['status'])
        if matches_search and matches_status:
            filtered_participants.append(p)

    return render_template('participants.html', participants=filtered_participants)

@app.route('/venues')
def venues_page():
    venues = load_venues()
    capacity_filters = ['Small', 'Medium', 'Large']
    capacity_filter = request.args.get('capacity_filter', '').strip()

    def capacity_category(cap):
        if cap < 1000:
            return 'Small'
        elif cap < 3000:
            return 'Medium'
        else:
            return 'Large'

    filtered_venues = [v for v in venues if capacity_filter == '' or capacity_category(v['capacity']) == capacity_filter]

    return render_template('venues.html', venues=filtered_venues, capacity_filters=capacity_filters)

@app.route('/venue/<int:venue_id>')
def venue_details(venue_id):
    venues = load_venues()
    venue = next((v for v in venues if v['venue_id'] == venue_id), None)
    if not venue:
        return redirect(url_for('venues_page'))
    return render_template('venue_details.html', venue=venue)

@app.route('/schedules')
def event_schedules():
    schedules = load_schedules()
    events = load_events()
    return render_template('schedules.html', schedules=schedules, events=events)

@app.route('/bookings')
def bookings_summary():
    bookings = load_bookings()

    cancel_id = request.args.get('cancel_booking_id', '').strip()
    if cancel_id.isdigit():
        cancel_id_int = int(cancel_id)
        updated = False
        for b in bookings:
            if b['booking_id'] == cancel_id_int and b['status'] != 'Cancelled':
                b['status'] = 'Cancelled'
                updated = True
                break
        if updated:
            try:
                with open(os.path.join(DATA_DIR, 'bookings.txt'), 'w', encoding='utf-8') as f:
                    for b in bookings:
                        f.write(f"{b['booking_id']}|{b['event_id']}|{b['customer_name']}|{b['booking_date']}|{b['ticket_count']}|{b['ticket_type']}|{b['total_amount']}|{b['status']}\n")
            except Exception:
                pass

    return render_template('bookings.html', bookings=bookings)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
