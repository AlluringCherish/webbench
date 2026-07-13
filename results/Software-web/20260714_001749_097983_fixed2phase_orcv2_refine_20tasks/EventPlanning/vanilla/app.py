from flask import Flask, render_template, request, redirect, url_for, flash
import os
import datetime

app = Flask(__name__)
app.secret_key = 'some_secret_key_for_sessions'

DATA_DIR = 'data'

# Utility functions to load and save data from text files

def load_events():
    events = []
    file_path = os.path.join(DATA_DIR, 'events.txt')
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if line:
                    parts = line.split('|')
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
    except FileNotFoundError:
        pass
    return events


def load_venues():
    venues = []
    file_path = os.path.join(DATA_DIR, 'venues.txt')
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if line:
                    parts = line.split('|')
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


def load_tickets():
    tickets = []
    file_path = os.path.join(DATA_DIR, 'tickets.txt')
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if line:
                    parts = line.split('|')
                    ticket = {
                        'ticket_id': parts[0],
                        'event_id': parts[1],
                        'ticket_type': parts[2],
                        'price': float(parts[3]),
                        'available_count': int(parts[4]),
                        'sold_count': int(parts[5])
                    }
                    tickets.append(ticket)
    except FileNotFoundError:
        pass
    return tickets


def load_bookings():
    bookings = []
    file_path = os.path.join(DATA_DIR, 'bookings.txt')
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if line:
                    parts = line.split('|')
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
    except FileNotFoundError:
        pass
    return bookings


def load_participants():
    participants = []
    file_path = os.path.join(DATA_DIR, 'participants.txt')
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if line:
                    parts = line.split('|')
                    participant = {
                        'participant_id': parts[0],
                        'event_id': parts[1],
                        'name': parts[2],
                        'email': parts[3],
                        'booking_id': parts[4],
                        'status': parts[5],
                        'registration_date': parts[6],
                    }
                    participants.append(participant)
    except FileNotFoundError:
        pass
    return participants


def load_schedules():
    schedules = []
    file_path = os.path.join(DATA_DIR, 'schedules.txt')
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if line:
                    parts = line.split('|')
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
    except FileNotFoundError:
        pass
    return schedules


def save_booking(new_booking):
    file_path = os.path.join(DATA_DIR, 'bookings.txt')
    try:
        bookings = load_bookings()
        max_id = 0
        for booking in bookings:
            try:
                bid = int(booking['booking_id'])
                if bid > max_id:
                    max_id = bid
            except:
                pass
        new_id = max_id + 1
        new_booking['booking_id'] = str(new_id)
        line = '|'.join([
            new_booking['booking_id'],
            new_booking['event_id'],
            new_booking['customer_name'],
            new_booking['booking_date'],
            str(new_booking['ticket_count']),
            new_booking['ticket_type'],
            f"{new_booking['total_amount']:.2f}",
            new_booking['status']
        ])
        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(line + '\n')
        return True
    except Exception as e:
        print('Error saving booking:', e)
        return False


def save_participant(new_participant):
    file_path = os.path.join(DATA_DIR, 'participants.txt')
    try:
        participants = load_participants()
        max_id = 0
        for part in participants:
            try:
                pid = int(part['participant_id'])
                if pid > max_id:
                    max_id = pid
            except:
                pass
        new_id = max_id + 1
        new_participant['participant_id'] = str(new_id)
        line = '|'.join([
            new_participant['participant_id'],
            new_participant['event_id'],
            new_participant['name'],
            new_participant['email'],
            new_participant['booking_id'],
            new_participant['status'],
            new_participant['registration_date']
        ])
        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(line + '\n')
        return True
    except Exception as e:
        print('Error saving participant:', e)
        return False


def save_bookings_all(bookings):
    file_path = os.path.join(DATA_DIR, 'bookings.txt')
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            for booking in bookings:
                line = '|'.join([
                    booking['booking_id'],
                    booking['event_id'],
                    booking['customer_name'],
                    booking['booking_date'],
                    str(booking['ticket_count']),
                    booking['ticket_type'],
                    f"{booking['total_amount']:.2f}",
                    booking['status']
                ])
                f.write(line + '\n')
        return True
    except Exception as e:
        print('Error saving all bookings:', e)
        return False


@app.route('/')
def dashboard():
    events = load_events()
    # For featured events, pick upcoming next 3 events sorted by date
    today = datetime.date.today()
    upcoming_events = sorted(
        [e for e in events if e['date'] >= today.isoformat()],
        key=lambda x: x['date']
    )[:3]

    venues = load_venues()
    # For featured venues, pick first 3
    featured_venues = venues[:3]

    return render_template('dashboard.html',
                           featured_events=upcoming_events,
                           featured_venues=featured_venues)


@app.route('/events')
def events_listing():
    events = load_events()
    search_query = request.args.get('search', '').strip().lower()
    category_filter = request.args.get('category', '').strip()

    filtered_events = events

    if search_query:
        filtered_events = [e for e in filtered_events if
                           search_query in e['event_name'].lower() or
                           search_query in e['location'].lower() or
                           search_query in e['date']]
    if category_filter and category_filter != 'All':
        filtered_events = [e for e in filtered_events if e['category'] == category_filter]

    return render_template('events.html', events=filtered_events, search_query=search_query, category_filter=category_filter)


@app.route('/events/<event_id>')
def event_details(event_id):
    events = load_events()
    event = next((e for e in events if e['event_id'] == event_id), None)
    if not event:
        flash('Event not found.')
        return redirect(url_for('events_listing'))
    return render_template('event_details.html', event=event)


@app.route('/booking', methods=['GET', 'POST'])
def ticket_booking():
    events = load_events()
    tickets = load_tickets()

    selected_event_id = request.args.get('event_id', '')

    if request.method == 'POST':
        event_id = request.form.get('select-event-dropdown', '')
        ticket_type = request.form.get('ticket-type-select', '')
        quantity_str = request.form.get('ticket-quantity-input', '0')
        customer_name = request.form.get('customer-name-input', '').strip()

        try:
            quantity = int(quantity_str)
            if quantity <= 0:
                raise ValueError('Ticket quantity must be positive.')
        except ValueError:
            flash('Invalid ticket quantity.')
            quantity = 0
            return render_template('ticket_booking.html', events=events, selected_event_id=selected_event_id, booking_confirmation=None)

        # Find ticket price for type and event
        ticket_list = [t for t in tickets if t['event_id'] == event_id and t['ticket_type'] == ticket_type]
        if not ticket_list:
            flash('Ticket type not available for selected event.')
            return render_template('ticket_booking.html', events=events, selected_event_id=selected_event_id, booking_confirmation=None)
        ticket = ticket_list[0]

        # Check availability
        if quantity > (ticket['available_count'] - ticket['sold_count']):
            flash('Not enough tickets available.')
            return render_template('ticket_booking.html', events=events, selected_event_id=selected_event_id, booking_confirmation=None)

        # Calculate total amount
        total_amount = quantity * ticket['price']

        # Save booking
        new_booking = {
            'event_id': event_id,
            'customer_name': customer_name if customer_name else 'Guest',
            'booking_date': datetime.date.today().isoformat(),
            'ticket_count': quantity,
            'ticket_type': ticket_type,
            'total_amount': total_amount,
            'status': 'Confirmed'
        }
        success = save_booking(new_booking)

        if success:
            confirmation = {
                'event_name': next((e['event_name'] for e in events if e['event_id'] == event_id), ''),
                'ticket_type': ticket_type,
                'quantity': quantity,
                'total_amount': f"{total_amount:.2f}"
            }
            return render_template('ticket_booking.html', events=events, selected_event_id=event_id, booking_confirmation=confirmation)
        else:
            flash('Failed to save booking.')

    return render_template('ticket_booking.html', events=events, selected_event_id=selected_event_id, booking_confirmation=None)


@app.route('/participants', methods=['GET', 'POST'])
def participants_management():
    participants = load_participants()
    events = load_events()

    search_query = request.args.get('search', '').strip().lower()
    status_filter = request.args.get('status', '')

    filtered_participants = participants
    if search_query:
        filtered_participants = [p for p in filtered_participants if
                                 search_query in p['name'].lower() or
                                 search_query in p['email'].lower()]
    if status_filter and status_filter != 'All':
        filtered_participants = [p for p in filtered_participants if p['status'] == status_filter]

    if request.method == 'POST':
        # Adding new participant
        name = request.form.get('participant-name', '').strip()
        email = request.form.get('participant-email', '').strip()
        event_id = request.form.get('participant-event', '')
        status = request.form.get('participant-status', 'Registered')

        if not (name and email and event_id):
            flash('Please fill all the participant fields.')
        else:
            # Create booking_id as empty string since we do not have a booking here
            new_participant = {
                'event_id': event_id,
                'name': name,
                'email': email,
                'booking_id': '',
                'status': status,
                'registration_date': datetime.date.today().isoformat()
            }
            if save_participant(new_participant):
                flash('Participant added successfully.')
                return redirect(url_for('participants_management'))
            else:
                flash('Failed to save participant.')

    return render_template('participants.html', participants=filtered_participants, events=events, search_query=search_query, status_filter=status_filter)


@app.route('/venues')
def venues_page():
    venues = load_venues()
    search_query = request.args.get('search', '').strip().lower()
    capacity_filter = request.args.get('capacity', '')

    filtered_venues = venues
    if search_query:
        filtered_venues = [v for v in filtered_venues if
                           search_query in v['venue_name'].lower() or
                           search_query in v['location'].lower()]
    if capacity_filter and capacity_filter != 'All':
        cap_map = {'Small': 1, 'Medium': 2, 'Large': 3}
        def capacity_size(cap_str):
            try:
                cap = int(cap_str)
                # define small < 1000, medium 1000-3000, large > 3000
                if cap < 1000:
                    return 1
                elif cap <= 3000:
                    return 2
                else:
                    return 3
            except:
                return 0
        filtered_venues = [v for v in filtered_venues if capacity_size(v['capacity']) == cap_map.get(capacity_filter, 0)]

    return render_template('venues.html', venues=filtered_venues, search_query=search_query, capacity_filter=capacity_filter)


@app.route('/schedules')
def schedules_page():
    schedules = load_schedules()
    events = load_events()

    filter_date = request.args.get('date', '')
    filter_event = request.args.get('event', '')

    filtered_schedules = schedules
    if filter_date:
        filtered_schedules = [s for s in filtered_schedules if s['session_time'].startswith(filter_date)]
    if filter_event and filter_event != 'All':
        filtered_schedules = [s for s in filtered_schedules if s['event_id'] == filter_event]

    return render_template('schedules.html', schedules=filtered_schedules, events=events, filter_date=filter_date, filter_event=filter_event)


@app.route('/bookings', methods=['GET', 'POST'])
def bookings_summary():
    bookings = load_bookings()
    events = load_events()

    search_query = request.args.get('search', '').strip().lower()

    filtered_bookings = bookings
    if search_query:
        filtered_bookings = [b for b in filtered_bookings if
                             search_query in b['booking_id'] or
                             search_query in next((e['event_name'].lower() for e in events if e['event_id'] == b['event_id']), '')]

    if request.method == 'POST':
        # Cancel booking request
        cancel_id = request.form.get('cancel_booking_id', '')
        if cancel_id:
            for booking in filtered_bookings:
                if booking['booking_id'] == cancel_id and booking['status'] != 'Canceled':
                    booking['status'] = 'Canceled'
                    if save_bookings_all(bookings):
                        flash('Booking cancelled successfully.')
                    else:
                        flash('Error cancelling booking.')
                    return redirect(url_for('bookings_summary'))

    return render_template('bookings.html', bookings=filtered_bookings, events=events, search_query=search_query)


if __name__ == '__main__':
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    app.run(debug=True)
