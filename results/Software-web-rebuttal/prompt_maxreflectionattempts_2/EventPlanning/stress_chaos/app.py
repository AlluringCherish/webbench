from flask import Flask, render_template, redirect, url_for, request
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Utility functions to load data

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
                event_name = parts[1]
                category = parts[2]
                date = parts[3]
                time = parts[4]
                location = parts[5]
                description = parts[6]
                venue_id = int(parts[7])
                capacity = int(parts[8])
                events.append({
                    'event_id': event_id,
                    'event_name': event_name,
                    'category': category,
                    'date': date,
                    'time': time,
                    'location': location,
                    'description': description,
                    'venue_id': venue_id,
                    'capacity': capacity
                })
    except Exception:
        # Fail silently
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
                venue_id = int(parts[0])
                venue_name = parts[1]
                location = parts[2]
                capacity = int(parts[3])
                amenities = parts[4]
                contact = parts[5]
                venues.append({
                    'venue_id': venue_id,
                    'venue_name': venue_name,
                    'location': location,
                    'capacity': capacity,
                    'amenities': amenities,
                    'contact': contact
                })
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
                parts = line.split('|')
                if len(parts) != 6:
                    continue
                ticket_id = int(parts[0])
                event_id = int(parts[1])
                ticket_type = parts[2]
                price = float(parts[3])
                available_count = int(parts[4])
                sold_count = int(parts[5])
                tickets.append({
                    'ticket_id': ticket_id,
                    'event_id': event_id,
                    'ticket_type': ticket_type,
                    'price': price,
                    'available_count': available_count,
                    'sold_count': sold_count
                })
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
                parts = line.split('|')
                if len(parts) != 8:
                    continue
                booking_id = int(parts[0])
                event_id = int(parts[1])
                customer_name = parts[2]
                booking_date = parts[3]
                ticket_count = int(parts[4])
                ticket_type = parts[5]
                total_amount = float(parts[6])
                status = parts[7]
                bookings.append({
                    'booking_id': booking_id,
                    'event_id': event_id,
                    'customer_name': customer_name,
                    'booking_date': booking_date,
                    'ticket_count': ticket_count,
                    'ticket_type': ticket_type,
                    'total_amount': total_amount,
                    'status': status
                })
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
                parts = line.split('|')
                if len(parts) != 7:
                    continue
                participant_id = int(parts[0])
                event_id = int(parts[1])
                name = parts[2]
                email = parts[3]
                booking_id = int(parts[4])
                status = parts[5]
                registration_date = parts[6]
                participants.append({
                    'participant_id': participant_id,
                    'event_id': event_id,
                    'name': name,
                    'email': email,
                    'booking_id': booking_id,
                    'status': status,
                    'registration_date': registration_date
                })
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
                parts = line.split('|')
                if len(parts) != 7:
                    continue
                schedule_id = int(parts[0])
                event_id = int(parts[1])
                session_title = parts[2]
                session_time = parts[3]  # datetime string YYYY-MM-DD HH:MM
                duration_minutes = int(parts[4])
                speaker = parts[5]
                venue_id = int(parts[6])
                schedules.append({
                    'schedule_id': schedule_id,
                    'event_id': event_id,
                    'session_title': session_title,
                    'session_time': session_time,
                    'duration_minutes': duration_minutes,
                    'speaker': speaker,
                    'venue_id': venue_id
                })
    except Exception:
        pass
    return schedules


# Route: /
@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))


# Route: /dashboard
@app.route('/dashboard')
def dashboard():
    events = load_events()

    # For featured_events, provide event_id, event_name, category, date, location
    # Let's take first 5 events as featured (or all if less)
    featured_events = []
    for e in events[:5]:
        featured_events.append({
            'event_id': e['event_id'],
            'event_name': e['event_name'],
            'category': e['category'],
            'date': e['date'],
            'location': e['location']
        })

    return render_template('dashboard.html',
                           featured_events=featured_events)


# Route: /events
@app.route('/events')
def events():
    events_list = load_events()

    # Get query parameters for filtering
    search_query = request.args.get('event-search-input', '').strip()
    selected_category = request.args.get('event-category-filter', '').strip()

    # Filter events by search and category
    filtered_events = []
    for e in events_list:
        match_search = True
        match_category = True
        if search_query:
            if search_query.lower() not in e['event_name'].lower():
                match_search = False
        if selected_category:
            if e['category'] != selected_category:
                match_category = False
        if match_search and match_category:
            filtered_events.append(e)

    return render_template('events.html',
                           events=filtered_events,
                           search_query=search_query,
                           selected_category=selected_category)


# Route: /event/<int:event_id>
@app.route('/event/<int:event_id>')
def event_details(event_id):
    events_list = load_events()
    event = None
    for e in events_list:
        if e['event_id'] == event_id:
            event = e
            break
    if event is None:
        # Return not found page or redirect to events
        return redirect(url_for('events'))

    return render_template('event_details.html', event=event)


# Route: /book_ticket
@app.route('/book_ticket', methods=['GET', 'POST'])
def ticket_booking():
    events_list = load_events()
    ticket_types = ["General", "VIP", "Early Bird"]  # as example

    if request.method == 'GET':
        # just render with events and ticket_types
        events_for_dropdown = [{'event_id': e['event_id'], 'event_name': e['event_name']} for e in events_list]
        return render_template('ticket_booking.html',
                               events=events_for_dropdown,
                               ticket_types=ticket_types)
    else:
        # POST: process booking
        event_id_str = request.form.get('select-event-dropdown', '')
        ticket_type = request.form.get('ticket-type-select', '')
        ticket_quantity_str = request.form.get('ticket-quantity-input', '')

        booking_confirmation = None
        error_message = None

        try:
            event_id = int(event_id_str)
            ticket_quantity = int(ticket_quantity_str)
            if ticket_quantity <= 0:
                error_message = "Please enter a valid ticket quantity."
        except Exception:
            error_message = "Invalid input for event or ticket quantity."

        if not error_message:
            # Check if event exists
            event = next((e for e in events_list if e['event_id'] == event_id), None)
            if event is None:
                error_message = "Selected event does not exist."

        if not error_message:
            # Check if ticket_type valid
            if ticket_type not in ticket_types:
                error_message = "Invalid ticket type selected."

        if not error_message:
            # Load tickets to check availability and price
            tickets = load_tickets()
            ticket_info = next((t for t in tickets if t['event_id'] == event_id and t['ticket_type'] == ticket_type), None)
            if ticket_info is None:
                error_message = "Ticket type not available for selected event."

        if not error_message:
            if ticket_quantity > ticket_info['available_count']:
                error_message = "Not enough tickets available."

        if error_message:
            # Render the form with error message
            events_for_dropdown = [{'event_id': e['event_id'], 'event_name': e['event_name']} for e in events_list]
            return render_template('ticket_booking.html',
                                   events=events_for_dropdown,
                                   ticket_types=ticket_types,
                                   booking_confirmation=error_message)

        # Calculate total
        total_amount = ticket_quantity * ticket_info['price']

        # Assign a new booking_id
        bookings = load_bookings()
        new_booking_id = 1
        if bookings:
            new_booking_id = max(b['booking_id'] for b in bookings) + 1

        # Add new booking to bookings.txt
        try:
            booking_date = datetime.now().strftime("%Y-%m-%d")
            booking_line = f"{new_booking_id}|{event_id}|Anonymous|{booking_date}|{ticket_quantity}|{ticket_type}|{total_amount:.2f}|Confirmed"
            with open(os.path.join(DATA_DIR, 'bookings.txt'), 'a', encoding='utf-8') as f:
                f.write(booking_line + '\n')

            # Update tickets.txt to reduce available_count and increase sold_count
            # Load all tickets from file lines
            tickets_lines = []
            with open(os.path.join(DATA_DIR, 'tickets.txt'), 'r', encoding='utf-8') as f:
                tickets_lines = f.readlines()

            new_lines = []
            for line in tickets_lines:
                parts = line.strip().split('|')
                if len(parts) == 6:
                    tid = int(parts[0])
                    teid = int(parts[1])
                    ttype = parts[2]
                    price = parts[3]
                    avail = int(parts[4])
                    sold = int(parts[5])
                    if teid == event_id and ttype == ticket_type:
                        avail -= ticket_quantity
                        sold += ticket_quantity
                        if avail < 0:
                            avail = 0  # avoid negative
                        new_line = f"{tid}|{teid}|{ttype}|{price}|{avail}|{sold}"
                        new_lines.append(new_line + '\n')
                    else:
                        new_lines.append(line)
                else:
                    new_lines.append(line)

            with open(os.path.join(DATA_DIR, 'tickets.txt'), 'w', encoding='utf-8') as f:
                f.writelines(new_lines)

            booking_confirmation = f"Booking confirmed! Booking ID: {new_booking_id}, Total: ${total_amount:.2f}"

        except Exception as e:
            booking_confirmation = "Failed to complete booking. Please try again later."

        events_for_dropdown = [{'event_id': e['event_id'], 'event_name': e['event_name']} for e in events_list]
        return render_template('ticket_booking.html',
                               events=events_for_dropdown,
                               ticket_types=ticket_types,
                               booking_confirmation=booking_confirmation)


# Route: /participants
@app.route('/participants', methods=['GET', 'POST'])
def participants_management():
    participants = load_participants()

    search_query = ''
    selected_status = ''

    if request.method == 'POST':
        search_query = request.form.get('search-participant-input', '').strip()
        selected_status = request.form.get('participant-status-filter', '').strip()
    else:
        search_query = request.args.get('search-participant-input', '').strip()
        selected_status = request.args.get('participant-status-filter', '').strip()

    filtered_participants = []

    for p in participants:
        matches_search = True
        matches_status = True

        if search_query:
            if search_query.lower() not in p['name'].lower() and search_query.lower() not in p['email'].lower():
                matches_search = False

        if selected_status:
            if p['status'] != selected_status:
                matches_status = False

        if matches_search and matches_status:
            filtered_participants.append(p)

    return render_template('participants.html',
                           participants=filtered_participants,
                           search_query=search_query,
                           selected_status=selected_status)


# Route: /venues
@app.route('/venues')
def venues():
    venues_list = load_venues()

    search_query = request.args.get('venue-search-input', '').strip()
    selected_capacity_filter = request.args.get('venue-capacity-filter', '').strip()

    # capacity filter can be Small, Medium, Large
    # We assume Small < 1000, Medium 1000~4999, Large >=5000
    def capacity_category(cap):
        if cap < 1000:
            return 'Small'
        elif 1000 <= cap < 5000:
            return 'Medium'
        else:
            return 'Large'

    filtered_venues = []
    for v in venues_list:
        matches_search = True
        matches_capacity = True

        if search_query:
            if search_query.lower() not in v['venue_name'].lower() and search_query.lower() not in v['location'].lower():
                matches_search = False

        if selected_capacity_filter and selected_capacity_filter != "":
            if capacity_category(v['capacity']) != selected_capacity_filter:
                matches_capacity = False

        if matches_search and matches_capacity:
            filtered_venues.append(v)

    return render_template('venues.html',
                           venues=filtered_venues,
                           search_query=search_query,
                           selected_capacity_filter=selected_capacity_filter)


# Route: /schedules
@app.route('/schedules')
def event_schedules():
    schedules = load_schedules()
    events_list = load_events()

    filter_date = request.args.get('schedule-filter-date', '').strip()
    filter_event_id_str = request.args.get('schedule-filter-event', '').strip()
    filter_event_id = None
    try:
        filter_event_id = int(filter_event_id_str) if filter_event_id_str else None
    except Exception:
        filter_event_id = None

    filtered_schedules = []

    for s in schedules:
        matches_date = True
        matches_event = True

        if filter_date:
            # Compare date part of session_time with filter_date
            session_date = s['session_time'].split(' ')[0]
            if session_date != filter_date:
                matches_date = False
        if filter_event_id is not None:
            if s['event_id'] != filter_event_id:
                matches_event = False

        if matches_date and matches_event:
            filtered_schedules.append(s)

    return render_template('schedules.html',
                           schedules=filtered_schedules,
                           filter_date=filter_date,
                           filter_event_id=filter_event_id)


# Route: /bookings
@app.route('/bookings')
def bookings_summary():
    bookings = load_bookings()
    events_list = load_events()

    # Build mapping event_id -> event_name
    event_id_to_name = {e['event_id']: e['event_name'] for e in events_list}

    # Collect bookings with event_name added
    bookings_with_event_name = []

    # Get search query
    search_query = request.args.get('booking-search-input', '').strip().lower()

    for b in bookings:
        event_name = event_id_to_name.get(b['event_id'], "Unknown Event")
        if search_query:
            if (search_query not in event_name.lower() and
                search_query not in b['status'].lower() and
                search_query not in b['customer_name'].lower() and
                search_query not in str(b['booking_id'])):
                continue

        bookings_with_event_name.append({
            'booking_id': b['booking_id'],
            'event_name': event_name,
            'date': b['booking_date'],
            'ticket_count': b['ticket_count'],
            'ticket_type': b['ticket_type'],
            'status': b['status']
        })

    # Note: Removing cancel booking functionality from here because no POST or other methods specified or implemented in design_spec

    return render_template('bookings.html',
                           bookings=bookings_with_event_name,
                           search_query=search_query)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
