from flask import Flask, render_template, redirect, url_for, request
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Utility functions to load data from pipe-delimited files

def load_events():
    events = []
    try:
        with open(os.path.join(DATA_DIR, 'events.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 9:
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
    except IOError:
        pass
    return events


def load_venues():
    venues = []
    try:
        with open(os.path.join(DATA_DIR, 'venues.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 6:
                    venue = {
                        'venue_id': int(parts[0]),
                        'venue_name': parts[1],
                        'location': parts[2],
                        'capacity': int(parts[3]),
                        'amenities': parts[4],
                        'contact': parts[5]
                    }
                    venues.append(venue)
    except IOError:
        pass
    return venues


def load_tickets():
    tickets = []
    try:
        with open(os.path.join(DATA_DIR, 'tickets.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 6:
                    ticket = {
                        'ticket_id': int(parts[0]),
                        'event_id': int(parts[1]),
                        'ticket_type': parts[2],
                        'price': float(parts[3]),
                        'available_count': int(parts[4]),
                        'sold_count': int(parts[5])
                    }
                    tickets.append(ticket)
    except IOError:
        pass
    return tickets


def load_bookings():
    bookings = []
    try:
        with open(os.path.join(DATA_DIR, 'bookings.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 8:
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
    except IOError:
        pass
    return bookings


def load_participants():
    participants = []
    try:
        with open(os.path.join(DATA_DIR, 'participants.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 7:
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
    except IOError:
        pass
    return participants


def load_schedules():
    schedules = []
    try:
        with open(os.path.join(DATA_DIR, 'schedules.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 7:
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
    except IOError:
        pass
    return schedules


# Route implementations

@app.route('/')
def root_redirect():
    # Redirect to dashboard
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    events = load_events()
    # Pick featured events as a list of dict with event_id, event_name, date
    # Let's assume featured are the first 5 upcoming events sorted by date
    featured_events = sorted(events, key=lambda e: e['date'])[:5]
    simple_featured = [{'event_id': e['event_id'], 'event_name': e['event_name'], 'date': e['date']} for e in featured_events]
    return render_template('dashboard.html', featured_events=simple_featured)


@app.route('/events')
def events_listing():
    events = load_events()
    # Return full event info needed for listing
    return render_template('events.html', events=events)


@app.route('/event/<int:event_id>')
def event_details(event_id):
    events = load_events()
    event = next((e for e in events if e['event_id'] == event_id), None)
    if event is None:
        # Could handle with error page or redirect to events
        return redirect(url_for('events_listing'))
    return render_template('event_details.html', event=event)


@app.route('/book_ticket', methods=['GET', 'POST'])
def book_ticket():
    if request.method == 'GET':
        events = load_events()
        return render_template('ticket_booking.html', events=events)
    else:
        # POST: Process booking form
        # Expecting form data: event_id, ticket_type, ticket_quantity, customer_name
        event_id = request.form.get('event_id')
        ticket_type = request.form.get('ticket_type')
        ticket_quantity = request.form.get('ticket_quantity')
        customer_name = request.form.get('customer_name')

        error_message = None
        if not event_id or not ticket_type or not ticket_quantity or not customer_name:
            error_message = 'All fields are required.'
        else:
            try:
                event_id = int(event_id)
                ticket_quantity = int(ticket_quantity)
            except ValueError:
                error_message = 'Invalid event ID or ticket quantity.'

        events = load_events()
        tickets = load_tickets()
        matching_tickets = [t for t in tickets if t['event_id'] == event_id and t['ticket_type'] == ticket_type]
        if not matching_tickets:
            error_message = 'Selected ticket type not available for the event.'
        else:
            ticket_info = matching_tickets[0]
            if error_message is None and ticket_quantity > ticket_info['available_count']:
                error_message = 'Not enough tickets available.'

        if error_message:
            # Render page with error and events for selection
            return render_template('ticket_booking.html', events=events, error=error_message)

        # If no error, create booking
        bookings = load_bookings()
        max_booking_id = max([b['booking_id'] for b in bookings], default=0)
        new_booking_id = max_booking_id + 1

        total_amount = ticket_quantity * ticket_info['price']
        from datetime import datetime
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

        # Append new booking to bookings.txt
        try:
            with open(os.path.join(DATA_DIR, 'bookings.txt'), 'a', encoding='utf-8') as f:
                f.write(f"{new_booking['booking_id']}|{new_booking['event_id']}|{new_booking['customer_name']}|{new_booking['booking_date']}|{new_booking['ticket_count']}|{new_booking['ticket_type']}|{new_booking['total_amount']:.2f}|{new_booking['status']}\n")
        except IOError:
            return render_template('ticket_booking.html', events=events, error='Failed to save booking.')

        # Update ticket availability
        # Reload tickets and update counts
        updated_tickets = []
        try:
            with open(os.path.join(DATA_DIR, 'tickets.txt'), 'r', encoding='utf-8') as f:
                for line in f:
                    parts = line.strip().split('|')
                    if len(parts) == 6:
                        tid = int(parts[0])
                        eid = int(parts[1])
                        ttype = parts[2]
                        price = parts[3]
                        avail = int(parts[4])
                        sold = int(parts[5])
                        if eid == event_id and ttype == ticket_type:
                            avail -= ticket_quantity
                            sold += ticket_quantity
                        updated_tickets.append(f"{tid}|{eid}|{ttype}|{price}|{avail}|{sold}\n")
            with open(os.path.join(DATA_DIR, 'tickets.txt'), 'w', encoding='utf-8') as f:
                f.writelines(updated_tickets)
        except IOError:
            # Ignore ticket update failure but inform user maybe
            pass

        booking_confirmation = {
            'booking_id': new_booking_id,
            'status': 'Confirmed',
            'event_id': event_id,
            'customer_name': customer_name,
            'ticket_count': ticket_quantity,
            'ticket_type': ticket_type,
            'total_amount': total_amount
        }
        return render_template('ticket_booking.html', booking_confirmation=booking_confirmation)


@app.route('/participants')
def participants_management():
    participants = load_participants()
    events = load_events()
    # Augment participants with event_name from event_id
    event_map = {e['event_id']: e['event_name'] for e in events}
    participants_out = []
    for p in participants:
        p_out = p.copy()
        p_out['event_name'] = event_map.get(p['event_id'], 'Unknown')
        participants_out.append(p_out)
    return render_template('participants.html', participants=participants_out)


@app.route('/add_participant', methods=['POST'])
def add_participant():
    # Expecting form data: name, email, event_id, status
    name = request.form.get('name')
    email = request.form.get('email')
    event_id = request.form.get('event_id')
    status = request.form.get('status')

    if not name or not email or not event_id or not status:
        # Simply redirect back
        return redirect(url_for('participants_management'))
    try:
        event_id = int(event_id)
    except ValueError:
        return redirect(url_for('participants_management'))

    participants = load_participants()
    max_participant_id = max([p['participant_id'] for p in participants], default=0)
    new_participant_id = max_participant_id + 1

    # Booking_id is not provided in form, set 0 or None
    # Use registration_date as today
    from datetime import datetime
    registration_date = datetime.now().strftime('%Y-%m-%d')

    new_participant = {
        'participant_id': new_participant_id,
        'event_id': event_id,
        'name': name,
        'email': email,
        'booking_id': 0,
        'status': status,
        'registration_date': registration_date
    }

    try:
        with open(os.path.join(DATA_DIR, 'participants.txt'), 'a', encoding='utf-8') as f:
            f.write(f"{new_participant['participant_id']}|{new_participant['event_id']}|{new_participant['name']}|{new_participant['email']}|{new_participant['booking_id']}|{new_participant['status']}|{new_participant['registration_date']}\n")
    except IOError:
        pass

    return redirect(url_for('participants_management'))


@app.route('/venues')
def venues():
    venues = load_venues()
    return render_template('venues.html', venues=venues)


@app.route('/schedules')
def event_schedules():
    schedules = load_schedules()
    return render_template('schedules.html', schedules=schedules)


@app.route('/bookings')
def bookings_summary():
    bookings = load_bookings()
    events = load_events()
    event_map = {e['event_id']: e['event_name'] for e in events}
    bookings_out = []
    for b in bookings:
        b_out = b.copy()
        b_out['event_name'] = event_map.get(b['event_id'], 'Unknown')
        bookings_out.append(b_out)
    return render_template('bookings.html', bookings=bookings_out)


@app.route('/cancel_booking/<int:booking_id>', methods=['POST'])
def cancel_booking(booking_id):
    # Cancel booking by setting status to 'Cancelled'
    bookings = load_bookings()
    updated_bookings = []
    found = False
    for b in bookings:
        if b['booking_id'] == booking_id:
            b['status'] = 'Cancelled'
            found = True
        updated_bookings.append(b)

    if found:
        # Save back
        try:
            with open(os.path.join(DATA_DIR, 'bookings.txt'), 'w', encoding='utf-8') as f:
                for b in updated_bookings:
                    f.write(f"{b['booking_id']}|{b['event_id']}|{b['customer_name']}|{b['booking_date']}|{b['ticket_count']}|{b['ticket_type']}|{b['total_amount']:.2f}|{b['status']}\n")
        except IOError:
            pass

    return redirect(url_for('bookings_summary'))


if __name__ == '__main__':
    app.run(debug=True, port=5000)
