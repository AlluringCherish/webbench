from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Utility functions to read data files

def read_events():
    events = []
    try:
        with open(os.path.join(DATA_DIR, 'events.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) !=9:
                    continue
                try:
                    event = {
                        'event_id': int(parts[0]),
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
                    continue
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
                try:
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
                    continue
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
                if len(parts) !=6:
                    continue
                try:
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
                    continue
    except FileNotFoundError:
        pass
    return tickets


def write_tickets(tickets):
    try:
        with open(os.path.join(DATA_DIR, 'tickets.txt'), 'w', encoding='utf-8') as f:
            for t in tickets:
                line = f"{t['ticket_id']}|{t['event_id']}|{t['ticket_type']}|{t['price']}|{t['available_count']}|{t['sold_count']}\n"
                f.write(line)
    except Exception:
        pass


def read_bookings():
    bookings = []
    try:
        with open(os.path.join(DATA_DIR, 'bookings.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) !=8:
                    continue
                try:
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
                    continue
    except FileNotFoundError:
        pass
    return bookings


def write_bookings(bookings):
    try:
        with open(os.path.join(DATA_DIR, 'bookings.txt'), 'w', encoding='utf-8') as f:
            for b in bookings:
                line = f"{b['booking_id']}|{b['event_id']}|{b['customer_name']}|{b['booking_date']}|{b['ticket_count']}|{b['ticket_type']}|{b['total_amount']}|{b['status']}\n"
                f.write(line)
    except Exception:
        pass


def read_participants():
    participants = []
    try:
        with open(os.path.join(DATA_DIR, 'participants.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts)!=7:
                    continue
                try:
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
                    continue
    except FileNotFoundError:
        pass
    return participants


def write_participants(participants):
    try:
        with open(os.path.join(DATA_DIR, 'participants.txt'), 'w', encoding='utf-8') as f:
            for p in participants:
                line = f"{p['participant_id']}|{p['event_id']}|{p['name']}|{p['email']}|{p['booking_id']}|{p['status']}|{p['registration_date']}\n"
                f.write(line)
    except Exception:
        pass


def read_schedules():
    schedules = []
    try:
        with open(os.path.join(DATA_DIR, 'schedules.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts)!=7:
                    continue
                try:
                    schedule = {
                        'schedule_id': int(parts[0]),
                        'event_id': int(parts[1]),
                        'session_title': parts[2],
                        'session_time': parts[3],
                        'duration_minutes': int(parts[4]),
                        'speaker': parts[5],
                        'venue_id': int(parts[6])
                    }
                    schedules.append(schedule)
                except Exception:
                    continue
    except FileNotFoundError:
        pass
    return schedules


# Routes Implementation

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard_page'))


@app.route('/dashboard')
def dashboard_page():
    events = read_events()
    # featured_events: subset with fields: event_id, event_name, date, location
    featured_events = [{'event_id': e['event_id'], 'event_name': e['event_name'], 'date': e['date'], 'location': e['location']} for e in events[:5]]
    return render_template('dashboard.html', featured_events=featured_events)


@app.route('/events')
def events_listing():
    events = read_events()
    return render_template('events.html', events=events)


@app.route('/events/filter', methods=['POST'])
def filter_events():
    search = request.form.get('search', '').strip().lower()
    category = request.form.get('category', '').strip().lower()
    events = read_events()
    filtered = []
    for e in events:
        match_search = True
        match_category = True
        if search:
            match_search = search in e['event_name'].lower() or search in e['description'].lower()
        if category:
            match_category = category == e['category'].lower()
        if match_search and match_category:
            filtered.append(e)
    return render_template('events.html', events=filtered)


@app.route('/event/<int:event_id>')
def event_details(event_id):
    events = read_events()
    event = next((e for e in events if e['event_id']==event_id), None)
    if event is None:
        return "Event not found.", 404
    return render_template('event_details.html', event=event)


@app.route('/ticket_booking', methods=['GET', 'POST'])
def ticket_booking_page():
    if request.method == 'GET':
        events = read_events()
        simple_events = [{'event_id': e['event_id'], 'event_name': e['event_name']} for e in events]
        return render_template('ticket_booking.html', events=simple_events)
    else:
        # POST should not be handled here, just redirect to /book_ticket as per design
        return redirect(url_for('book_ticket'))


@app.route('/book_ticket', methods=['POST'])
def book_ticket():
    # Expected form fields: event_id, customer_name, ticket_type, ticket_quantity, booking_date
    try:
        event_id = int(request.form.get('event_id','0'))
        customer_name = request.form.get('customer_name', '').strip()
        ticket_type = request.form.get('ticket_type', '').strip()
        ticket_quantity = int(request.form.get('ticket_quantity','0'))
        booking_date = request.form.get('booking_date', '').strip()

        if event_id<=0 or not customer_name or not ticket_type or ticket_quantity<=0 or not booking_date:
            return render_template('ticket_booking.html', confirmation='Invalid booking data provided.')

        tickets = read_tickets()
        # find ticket matching event_id and ticket_type
        ticket = next((t for t in tickets if t['event_id']==event_id and t['ticket_type'].lower() == ticket_type.lower()), None)
        if ticket is None:
            return render_template('ticket_booking.html', confirmation='Ticket type not found for the selected event.')

        if ticket['available_count'] < ticket_quantity:
            return render_template('ticket_booking.html', confirmation='Not enough tickets available.')

        bookings = read_bookings()

        # new booking_id generation: max existing +1
        max_booking_id = max((b['booking_id'] for b in bookings), default=0)
        new_booking_id = max_booking_id + 1

        total_amount = round(ticket['price'] * ticket_quantity, 2)

        # Add new booking
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

        # Update tickets data
        for t in tickets:
            if t['ticket_id'] == ticket['ticket_id']:
                t['available_count'] -= ticket_quantity
                t['sold_count'] += ticket_quantity
                break

        # Persist data
        write_bookings(bookings)
        write_tickets(tickets)

        confirmation = {
            'booking_id': new_booking_id,
            'event_id': event_id,
            'customer_name': customer_name,
            'ticket_count': ticket_quantity,
            'ticket_type': ticket_type,
            'total_amount': total_amount,
            'status': 'Confirmed'
        }
        return render_template('ticket_booking.html', confirmation=confirmation)
    except Exception:
        return render_template('ticket_booking.html', confirmation='Error processing booking request.')


@app.route('/participants')
def participants_management():
    participants = read_participants()
    return render_template('participants.html', participants=participants)


@app.route('/participants/add', methods=['POST'])
def add_participant():
    try:
        event_id = int(request.form.get('event_id','0'))
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        booking_id = int(request.form.get('booking_id','0'))
        status = request.form.get('status', '').strip()
        registration_date = request.form.get('registration_date', '').strip()

        if event_id <= 0 or not name or not email or booking_id <=0 or not status or not registration_date:
            participants = read_participants()
            return render_template('participants.html', participants=participants, message='Invalid participant data provided.')

        participants = read_participants()
        max_participant_id = max((p['participant_id'] for p in participants), default=0)
        new_participant_id = max_participant_id + 1

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

        participants = read_participants()
        return render_template('participants.html', participants=participants)
    except Exception:
        participants = read_participants()
        return render_template('participants.html', participants=participants, message='Error adding participant.')


@app.route('/venues')
def venues_page():
    venues = read_venues()
    return render_template('venues.html', venues=venues)


@app.route('/venues/filter', methods=['POST'])
def filter_venues():
    search = request.form.get('search', '').strip().lower()
    capacity_filter = request.form.get('capacity', '').strip().lower()  # Expected Small, Medium, Large
    venues = read_venues()
    filtered = []

    def capacity_category(cap):
        if cap <= 500:
            return 'small'
        elif cap <= 2000:
            return 'medium'
        else:
            return 'large'

    for v in venues:
        match_search = True
        match_capacity = True
        if search:
            match_search = search in v['venue_name'].lower() or search in v['location'].lower() or search in v['amenities'].lower()
        if capacity_filter:
            match_capacity = capacity_category(v['capacity']) == capacity_filter
        if match_search and match_capacity:
            filtered.append(v)

    return render_template('venues.html', venues=filtered)


@app.route('/venue/<int:venue_id>')
def venue_details(venue_id):
    venues = read_venues()
    venue = next((v for v in venues if v['venue_id'] == venue_id), None)
    if venue is None:
        return "Venue not found.", 404
    return render_template('venue_details.html', venue=venue)


@app.route('/schedules')
def schedules_page():
    schedules = read_schedules()
    events = read_events()
    return render_template('schedules.html', schedules=schedules, events=events)


@app.route('/bookings')
def bookings_summary():
    bookings = read_bookings()
    return render_template('bookings.html', bookings=bookings)


@app.route('/bookings/cancel/<int:booking_id>', methods=['POST'])
def cancel_booking(booking_id):
    try:
        bookings = read_bookings()
        tickets = read_tickets()
        booking = next((b for b in bookings if b['booking_id']==booking_id), None)
        if booking is None:
            bookings = read_bookings()
            return render_template('bookings.html', bookings=bookings, message='Booking not found.')

        if booking['status'].lower() == 'cancelled':
            bookings = read_bookings()
            return render_template('bookings.html', bookings=bookings, message='Booking already cancelled.')

        # Update booking status
        booking['status'] = 'Cancelled'

        # Restore ticket counts
        ticket = next((t for t in tickets if t['event_id'] == booking['event_id'] and t['ticket_type'].lower() == booking['ticket_type'].lower()), None)
        if ticket:
            ticket['available_count'] += booking['ticket_count']
            ticket['sold_count'] -= booking['ticket_count']

        write_bookings(bookings)
        write_tickets(tickets)

        bookings = read_bookings()
        return render_template('bookings.html', bookings=bookings, message='Booking cancelled successfully.')
    except Exception:
        bookings = read_bookings()
        return render_template('bookings.html', bookings=bookings, message='Error cancelling booking.')


@app.route('/back_to_dashboard')
def back_to_dashboard():
    return redirect(url_for('dashboard_page'))


if __name__ == '__main__':
    app.run(debug=True, port=5000)
