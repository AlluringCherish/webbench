from flask import Flask, render_template, redirect, url_for, request
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'


# Utility loading functions

def load_events():
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
                event_id = int(parts[0])
                event = {
                    'event_id': event_id,
                    'event_name': parts[1],
                    'category': parts[2],
                    'date': parts[3],
                    'time': parts[4],
                    'location': parts[5],
                    'description': parts[6],
                    'venue_id': int(parts[7]),
                    'capacity': int(parts[8])
                }
                events.append(event)
    except Exception:
        pass
    return events


def load_venues():
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
                venue = {
                    'venue_id': int(parts[0]),
                    'venue_name': parts[1],
                    'location': parts[2],
                    'capacity': int(parts[3]),
                    'amenities': parts[4],
                    'contact': parts[5]
                }
                venues.append(venue)
    except Exception:
        pass
    return venues


def load_tickets():
    tickets = []
    try:
        with open(os.path.join(DATA_DIR, 'tickets.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts=line.split('|')
                if len(parts)!=6:
                    continue
                ticket = {
                    'ticket_id': int(parts[0]),
                    'event_id': int(parts[1]),
                    'ticket_type': parts[2],
                    'price': float(parts[3]),
                    'available_count': int(parts[4]),
                    'sold_count': int(parts[5])
                }
                tickets.append(ticket)
    except Exception:
        pass
    return tickets


def load_bookings():
    bookings = []
    try:
        with open(os.path.join(DATA_DIR, 'bookings.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts=line.split('|')
                if len(parts)!=8:
                    continue
                booking = {
                    'booking_id': int(parts[0]),
                    'event_id': int(parts[1]),
                    'customer_name': parts[2],
                    'booking_date': parts[3],
                    'ticket_count': int(parts[4]),
                    'ticket_type': parts[5],
                    'total_amount': float(parts[6]),
                    'status': parts[7]
                }
                bookings.append(booking)
    except Exception:
        pass
    return bookings


def load_participants():
    participants = []
    try:
        with open(os.path.join(DATA_DIR, 'participants.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts=line.split('|')
                if len(parts)!=7:
                    continue
                participant = {
                    'participant_id': int(parts[0]),
                    'event_id': int(parts[1]),
                    'name': parts[2],
                    'email': parts[3],
                    'booking_id': int(parts[4]),
                    'status': parts[5],
                    'registration_date': parts[6]
                }
                participants.append(participant)
    except Exception:
        pass
    return participants


def load_schedules():
    schedules = []
    try:
        with open(os.path.join(DATA_DIR, 'schedules.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts=line.split('|')
                if len(parts)!=7:
                    continue
                schedule = {
                    'schedule_id': int(parts[0]),
                    'event_id': int(parts[1]),
                    'session_title': parts[2],
                    'session_time': parts[3],
                    'duration': int(parts[4]),
                    'speaker': parts[5],
                    'venue_id': int(parts[6])
                }
                schedules.append(schedule)
    except Exception:
        pass
    return schedules


# Helper lookup functions

def find_event(event_id):
    events = load_events()
    for e in events:
        if e['event_id'] == event_id:
            return e
    return None


def find_venue(venue_id):
    venues = load_venues()
    for v in venues:
        if v['venue_id'] == venue_id:
            return v
    return None


def find_ticket(event_id, ticket_type):
    tickets = load_tickets()
    for t in tickets:
        if t['event_id'] == event_id and t['ticket_type'] == ticket_type:
            return t
    return None


def max_booking_id(bookings):
    if not bookings:
        return 0
    return max(b['booking_id'] for b in bookings)


def save_bookings(bookings):
    try:
        with open(os.path.join(DATA_DIR, 'bookings.txt'), 'w', encoding='utf-8') as f:
            for b in bookings:
                line = '|'.join([
                    str(b['booking_id']),
                    str(b['event_id']),
                    b['customer_name'],
                    b['booking_date'],
                    str(b['ticket_count']),
                    b['ticket_type'],
                    f"{b['total_amount']:.2f}",
                    b['status']
                ])
                f.write(line + '\n')
    except Exception:
        pass


def save_tickets(tickets):
    try:
        with open(os.path.join(DATA_DIR, 'tickets.txt'), 'w', encoding='utf-8') as f:
            for t in tickets:
                line = '|'.join([
                    str(t['ticket_id']),
                    str(t['event_id']),
                    t['ticket_type'],
                    f"{t['price']:.2f}",
                    str(t['available_count']),
                    str(t['sold_count'])
                ])
                f.write(line + '\n')
    except Exception:
        pass


# Routes

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard_page'))


@app.route('/dashboard')
def dashboard_page():
    events = load_events()
    venues = load_venues()

    # For featured events: pick first 5 by date ascending
    sorted_events = sorted(events, key=lambda e: e['date'])
    featured_events = []
    for e in sorted_events[:5]:
        featured_events.append({
            'event_id': e['event_id'],
            'event_name': e['event_name'],
            'date': e['date'],
            'location': e['location']
        })

    # For featured venues: pick first 5 by venue_name ascending
    sorted_venues = sorted(venues, key=lambda v: v['venue_name'])
    featured_venues = []
    for v in sorted_venues[:5]:
        featured_venues.append({
            'venue_id': v['venue_id'],
            'venue_name': v['venue_name'],
            'location': v['location']
        })

    return render_template('dashboard.html', featured_events=featured_events, featured_venues=featured_venues)


@app.route('/events')
def events_listing():
    events = load_events()
    categories = ["Conference", "Concert", "Sports", "Workshop", "Social"]
    return render_template('events.html', events=events, categories=categories)


@app.route('/event/<int:event_id>')
def event_details(event_id):
    event = find_event(event_id)
    if not event:
        return redirect(url_for('events_listing'))

    venue = find_venue(event['venue_id'])
    # Context:
    # event: dict fields including description
    # venue: dict fields
    return render_template('event_details.html', event=event, venue=venue)


@app.route('/book_ticket', methods=['GET', 'POST'])
def book_ticket():
    if request.method == 'GET':
        events = load_events()
        events_list = [{'event_id': e['event_id'], 'event_name': e['event_name']} for e in events]
        return render_template('book_ticket.html', events=events_list)

    if request.method == 'POST':
        form = request.form
        try:
            event_id = int(form.get('event_id'))
            ticket_count = int(form.get('ticket_count'))
            ticket_type = form.get('ticket_type')
            customer_name = form.get('customer_name', 'Guest')
        except Exception:
            # Render GET with error maybe, but specification says nothing, so just re-render GET
            events = load_events()
            events_list = [{'event_id': e['event_id'], 'event_name': e['event_name']} for e in events]
            return render_template('book_ticket.html', events=events_list)

        event = find_event(event_id)
        if not event:
            events = load_events()
            events_list = [{'event_id': e['event_id'], 'event_name': e['event_name']} for e in events]
            return render_template('book_ticket.html', events=events_list)

        ticket = find_ticket(event_id, ticket_type)
        if not ticket or ticket['available_count'] < ticket_count or ticket_count <= 0:
            events = load_events()
            events_list = [{'event_id': e['event_id'], 'event_name': e['event_name']} for e in events]
            return render_template('book_ticket.html', events=events_list)

        # Process booking
        bookings = load_bookings()
        new_booking_id = max_booking_id(bookings) + 1
        booking_date = datetime.now().strftime('%Y-%m-%d')
        total_amount = ticket_count * ticket['price']

        new_booking = {
            'booking_id': new_booking_id,
            'event_id': event_id,
            'customer_name': customer_name,
            'booking_date': booking_date,
            'ticket_count': ticket_count,
            'ticket_type': ticket_type,
            'total_amount': total_amount,
            'status': 'Confirmed'
        }

        bookings.append(new_booking)

        # Update tickets data (reduce available_count, increase sold_count)
        tickets = load_tickets()
        for t in tickets:
            if t['event_id'] == event_id and t['ticket_type'] == ticket_type:
                t['available_count'] -= ticket_count
                t['sold_count'] += ticket_count
                break

        save_bookings(bookings)
        save_tickets(tickets)

        booking_confirmation = {
            'booking_id': new_booking_id,
            'event_name': event['event_name'],
            'ticket_count': ticket_count,
            'ticket_type': ticket_type,
            'total_amount': total_amount
        }
        return render_template('book_ticket.html', booking_confirmation=booking_confirmation)


@app.route('/participants', methods=['GET', 'POST'])
def participants_management():
    participants = load_participants()
    events = load_events()
    event_dict = {e['event_id']: e['event_name'] for e in events}

    # Map event_name to each participant
    for p in participants:
        p['event_name'] = event_dict.get(p['event_id'], 'Unknown')

    statuses = ["Registered", "Confirmed", "Attended"]

    if request.method == 'POST':
        # Add participant logic (not specified precisely)
        form = request.form
        name = form.get('name')
        email = form.get('email')
        event_id = form.get('event_id')
        status = form.get('status')

        if not (name and email and event_id and status):
            # just re-render GET view
            return render_template('participants.html', participants=participants, statuses=statuses)

        # convert event_id to int
        try:
            event_id = int(event_id)
        except ValueError:
            return render_template('participants.html', participants=participants, statuses=statuses)

        # We do not have a participant_id generating scheme from spec. We'll generate max id + 1
        max_participant_id = max([p['participant_id'] for p in participants], default=0)
        new_participant_id = max_participant_id + 1
        registration_date = datetime.now().strftime('%Y-%m-%d')

        # No booking_id on adding participant interactively by spec, we set to 0
        new_participant = {
            'participant_id': new_participant_id,
            'event_id': event_id,
            'name': name,
            'email': email,
            'booking_id': 0,
            'status': status,
            'registration_date': registration_date
        }

        participants.append(new_participant)

        # Save participants back
        try:
            with open(os.path.join(DATA_DIR, 'participants.txt'), 'w', encoding='utf-8') as f:
                for p in participants:
                    line = '|'.join([
                        str(p['participant_id']),
                        str(p['event_id']),
                        p['name'],
                        p['email'],
                        str(p['booking_id']),
                        p['status'],
                        p['registration_date']
                    ])
                    f.write(line + '\n')
        except Exception:
            pass

        return redirect(url_for('participants_management'))

    return render_template('participants.html', participants=participants, statuses=statuses)


@app.route('/venues')
def venues_page():
    venues = load_venues()
    return render_template('venues.html', venues=venues)


@app.route('/event_schedules')
def event_schedules():
    schedules = load_schedules()
    events = load_events()
    venues = load_venues()
    venue_dict = {v['venue_id']: v['venue_name'] for v in venues}

    # Map venue_name to each schedule
    for s in schedules:
        s['venue_name'] = venue_dict.get(s['venue_id'], 'Unknown')

    # Filter schedules by optional date and event_id if query parameters provided
    filter_date = request.args.get('schedule-filter-date')
    filter_event_id = request.args.get('schedule-filter-event', type=int)

    if filter_date:
        filtered_schedules = []
        for sch in schedules:
            # Compare date part only (YYYY-MM-DD) of session_time
            sess_date = sch['session_time'].split(' ')[0]
            if sess_date == filter_date:
                filtered_schedules.append(sch)
        schedules = filtered_schedules

    if filter_event_id:
        schedules = [s for s in schedules if s['event_id'] == filter_event_id]

    # Prepare events list
    events_list = [{'event_id': e['event_id'], 'event_name': e['event_name']} for e in events]

    return render_template('schedules.html', schedules=schedules, events=events_list)


@app.route('/bookings')
def bookings_summary():
    bookings = load_bookings()
    events = load_events()
    event_dict = {e['event_id']: e['event_name'] for e in events}

    # Map event_name and date (from event) for context
    bookings_context = []
    for b in bookings:
        event_name = event_dict.get(b['event_id'], 'Unknown')
        event_date = ''
        event_obj = find_event(b['event_id'])
        if event_obj:
            event_date = event_obj['date']

        bookings_context.append({
            'booking_id': b['booking_id'],
            'event_name': event_name,
            'date': event_date,
            'ticket_count': b['ticket_count'],
            'status': b['status']
        })

    return render_template('bookings.html', bookings=bookings_context)


@app.route('/cancel_booking/<int:booking_id>', methods=['POST'])
def cancel_booking(booking_id):
    bookings = load_bookings()
    tickets = load_tickets()
    updated = False

    for b in bookings:
        if b['booking_id'] == booking_id:
            if b['status'] != 'Cancelled':
                b['status'] = 'Cancelled'

                # Return tickets to available_count and decrease sold_count
                for t in tickets:
                    if t['event_id'] == b['event_id'] and t['ticket_type'] == b['ticket_type']:
                        t['available_count'] += b['ticket_count']
                        t['sold_count'] -= b['ticket_count']
                        break

                updated = True
            break

    if updated:
        save_bookings(bookings)
        save_tickets(tickets)

    return redirect(url_for('bookings_summary'))


if __name__ == '__main__':
    app.run(debug=True, port=5000)
