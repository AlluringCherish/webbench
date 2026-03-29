from flask import Flask, render_template, redirect, url_for, request
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = "data"

# Helper functions to load data

def load_events():
    events = []
    path = os.path.join(DATA_DIR, "events.txt")
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    fields = line.split("|")
                    # Fields order:
                    # 1. event_id (int)
                    # 2. event_name (str)
                    # 3. category (str)
                    # 4. date (str, YYYY-MM-DD)
                    # 5. time (str, HH:MM)
                    # 6. location (str)
                    # 7. description (str)
                    # 8. venue_id (int)
                    # 9. capacity (int)
                    try:
                        event = {
                            "event_id": int(fields[0]),
                            "event_name": fields[1],
                            "category": fields[2],
                            "date": fields[3],
                            "time": fields[4],
                            "location": fields[5],
                            "description": fields[6],
                            "venue_id": int(fields[7]),
                            "capacity": int(fields[8])
                        }
                        events.append(event)
                    except (IndexError, ValueError):
                        continue
    except Exception:
        pass
    return events


def load_venues():
    venues = []
    path = os.path.join(DATA_DIR, "venues.txt")
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    fields = line.split("|")
                    # Fields order:
                    # 1. venue_id (int)
                    # 2. venue_name (str)
                    # 3. location (str)
                    # 4. capacity (int)
                    # 5. amenities (str)
                    # 6. contact (str)
                    try:
                        venue = {
                            "venue_id": int(fields[0]),
                            "venue_name": fields[1],
                            "location": fields[2],
                            "capacity": int(fields[3]),
                            "amenities": fields[4],
                            "contact": fields[5]
                        }
                        venues.append(venue)
                    except (IndexError, ValueError):
                        continue
    except Exception:
        pass
    return venues


def load_tickets():
    tickets = []
    path = os.path.join(DATA_DIR, "tickets.txt")
    try:
        with open(path,"r", encoding="utf-8") as f:
            for line in f:
                line=line.strip()
                if line:
                    fields = line.split("|")
                    # 1. ticket_id (int)
                    # 2. event_id (int)
                    # 3. ticket_type (str)
                    # 4. price (float)
                    # 5. available_count (int)
                    # 6. sold_count (int)
                    try:
                        ticket = {
                            "ticket_id": int(fields[0]),
                            "event_id": int(fields[1]),
                            "ticket_type": fields[2],
                            "price": float(fields[3]),
                            "available_count": int(fields[4]),
                            "sold_count": int(fields[5])
                        }
                        tickets.append(ticket)
                    except (IndexError, ValueError):
                        continue
    except Exception:
        pass
    return tickets


def load_bookings():
    bookings = []
    path = os.path.join(DATA_DIR, "bookings.txt")
    try:
        with open(path,"r", encoding="utf-8") as f:
            for line in f:
                line=line.strip()
                if line:
                    fields = line.split("|")
                    # 1. booking_id (int)
                    # 2. event_id (int)
                    # 3. customer_name (str)
                    # 4. booking_date (str, YYYY-MM-DD)
                    # 5. ticket_count (int)
                    # 6. ticket_type (str)
                    # 7. total_amount (float)
                    # 8. status (str)
                    try:
                        booking = {
                            "booking_id": int(fields[0]),
                            "event_id": int(fields[1]),
                            "customer_name": fields[2],
                            "booking_date": fields[3],
                            "ticket_count": int(fields[4]),
                            "ticket_type": fields[5],
                            "total_amount": float(fields[6]),
                            "status": fields[7]
                        }
                        bookings.append(booking)
                    except (IndexError, ValueError):
                        continue
    except Exception:
        pass
    return bookings


def load_participants():
    participants = []
    path = os.path.join(DATA_DIR, "participants.txt")
    try:
        with open(path,"r", encoding="utf-8") as f:
            for line in f:
                line=line.strip()
                if line:
                    fields = line.split("|")
                    # 1. participant_id (int)
                    # 2. event_id (int)
                    # 3. name (str)
                    # 4. email (str)
                    # 5. booking_id (int)
                    # 6. status (str)
                    # 7. registration_date (str, YYYY-MM-DD)
                    try:
                        participant = {
                            "participant_id": int(fields[0]),
                            "event_id": int(fields[1]),
                            "name": fields[2],
                            "email": fields[3],
                            "booking_id": int(fields[4]),
                            "status": fields[5],
                            "registration_date": fields[6]
                        }
                        participants.append(participant)
                    except (IndexError, ValueError):
                        continue
    except Exception:
        pass
    return participants


def load_schedules():
    schedules = []
    path = os.path.join(DATA_DIR, "schedules.txt")
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line=line.strip()
                if line:
                    fields = line.split("|")
                    # 1. schedule_id (int)
                    # 2. event_id (int)
                    # 3. session_title (str)
                    # 4. session_time (str, YYYY-MM-DD HH:MM)
                    # 5. duration_minutes (int)
                    # 6. speaker (str)
                    # 7. venue_id (int)
                    try:
                        schedule = {
                            "schedule_id": int(fields[0]),
                            "event_id": int(fields[1]),
                            "session_title": fields[2],
                            "session_time": fields[3],
                            "duration_minutes": int(fields[4]),
                            "speaker": fields[5],
                            "venue_id": int(fields[6])
                        }
                        schedules.append(schedule)
                    except (IndexError, ValueError):
                        continue
    except Exception:
        pass
    return schedules

# Helper function: write bookings.txt updated content

def save_bookings(bookings):
    path = os.path.join(DATA_DIR, "bookings.txt")
    try:
        with open(path, "w", encoding="utf-8") as f:
            for b in bookings:
                line = f"{b['booking_id']}|{b['event_id']}|{b['customer_name']}|{b['booking_date']}|{b['ticket_count']}|{b['ticket_type']}|{b['total_amount']}|{b['status']}\n"
                f.write(line)
    except Exception:
        pass


# Helper function: write tickets.txt updated content

def save_tickets(tickets):
    path = os.path.join(DATA_DIR, "tickets.txt")
    try:
        with open(path, "w", encoding="utf-8") as f:
            for t in tickets:
                line = f"{t['ticket_id']}|{t['event_id']}|{t['ticket_type']}|{t['price']}|{t['available_count']}|{t['sold_count']}\n"
                f.write(line)
    except Exception:
        pass


@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard_page'))


@app.route('/dashboard')
def dashboard_page():
    events = load_events()
    venues = load_venues()

    # For featured_events, we can pick the first 5 events sorted by date ascending
    featured_events = sorted(events, key=lambda e: e['date'])[:5]
    # context featured_events needs keys: event_id, event_name, date, location
    featured_events = [{"event_id": e["event_id"], "event_name": e["event_name"], "date": e["date"], "location": e["location"]} for e in featured_events]

    # venues keys: venue_id, venue_name, location
    venues_context = [{"venue_id": v["venue_id"], "venue_name": v["venue_name"], "location": v["location"]} for v in venues]

    return render_template('dashboard.html', featured_events=featured_events, venues=venues_context)


@app.route('/events', methods=['GET', 'POST'])
def events_listing_page():
    events = load_events()

    if request.method == 'POST':
        # Filtering based on: name substr, location substr, date, category
        search_query = request.form.get('search', '').strip().lower()
        category_filter = request.form.get('category', '').strip().lower()

        filtered_events = []
        for e in events:
            # Check search query on event_name, location, date
            match_search = (search_query == '' or (search_query in e['event_name'].lower() or search_query in e['location'].lower() or search_query in e['date']))
            # Check category filter
            match_category = (category_filter == '' or e['category'].lower() == category_filter)
            if match_search and match_category:
                filtered_events.append(e)
        events = filtered_events

    # Send context keys: event_id, event_name, category, date, location
    events_context = [{"event_id": e["event_id"], "event_name": e["event_name"], "category": e["category"], "date": e["date"], "location": e["location"]} for e in events]

    return render_template('events.html', events=events_context)


@app.route('/event/<int:event_id>')
def event_details_page(event_id):
    events = load_events()
    event = next((e for e in events if e['event_id'] == event_id), None)
    if not event:
        # Not found, redirect to events listing
        return redirect(url_for('events_listing_page'))

    # context keys: event_id, event_name, category, date, time, location, description, venue_id, capacity
    event_context = {
        "event_id": event["event_id"],
        "event_name": event["event_name"],
        "category": event["category"],
        "date": event["date"],
        "time": event["time"],
        "location": event["location"],
        "description": event["description"],
        "venue_id": event["venue_id"],
        "capacity": event["capacity"]
    }

    return render_template('event_details.html', event=event_context)


@app.route('/book_ticket', methods=['GET', 'POST'])
def ticket_booking_page():
    events = load_events()
    # context: events with keys event_id, event_name
    events_context = [{"event_id": e["event_id"], "event_name": e["event_name"]} for e in events]

    if request.method == 'POST':
        # form fields: event_id, customer_name, ticket_count, ticket_type
        try:
            event_id = int(request.form.get('event_id'))
            customer_name = request.form.get('customer_name', '').strip()
            ticket_count = int(request.form.get('ticket_count', '0'))
            ticket_type = request.form.get('ticket_type', '')
        except Exception:
            # invalid form data, re-display page without confirmation
            return render_template('ticket_booking.html', events=events_context)

        if ticket_count <= 0 or customer_name == '' or ticket_type == '':
            # invalid parameters
            return render_template('ticket_booking.html', events=events_context)

        tickets = load_tickets()
        # find ticket info for event_id and ticket_type
        ticket_info = next((t for t in tickets if t['event_id'] == event_id and t['ticket_type'].lower() == ticket_type.lower()), None)
        if not ticket_info or ticket_info['available_count'] < ticket_count:
            # not enough tickets
            return render_template('ticket_booking.html', events=events_context)

        # Calculate total amount
        total_amount = ticket_info['price'] * ticket_count

        bookings = load_bookings()
        next_booking_id = (max((b['booking_id'] for b in bookings), default=0) + 1) if bookings else 1

        current_date_str = datetime.now().strftime('%Y-%m-%d')

        new_booking = {
            "booking_id": next_booking_id,
            "event_id": event_id,
            "customer_name": customer_name,
            "booking_date": current_date_str,
            "ticket_count": ticket_count,
            "ticket_type": ticket_type,
            "total_amount": total_amount,
            "status": "Confirmed"
        }

        bookings.append(new_booking)

        # Update tickets availability
        ticket_info['available_count'] -= ticket_count
        ticket_info['sold_count'] += ticket_count

        # Save bookings and tickets
        save_bookings(bookings)
        save_tickets(tickets)

        # Find event name
        event_name = next((e['event_name'] for e in events if e['event_id'] == event_id), '')

        booking_confirmation = {
            "booking_id": next_booking_id,
            "event_name": event_name,
            "ticket_count": ticket_count,
            "ticket_type": ticket_type,
            "total_amount": total_amount,
            "status": "Confirmed"
        }

        return render_template('ticket_booking.html', events=events_context, booking_confirmation=booking_confirmation)

    # GET method
    return render_template('ticket_booking.html', events=events_context)


@app.route('/participants', methods=['GET', 'POST'])
def participants_page():
    participants = load_participants()
    events = load_events()
    # Map event_id to event_name for convenience
    event_id_to_name = {e['event_id']: e['event_name'] for e in events}

    if request.method == 'POST':
        search_query = request.form.get('search', '').strip().lower()
        status_filter = request.form.get('status', '').strip().lower()

        filtered_participants = []
        for p in participants:
            name_email = p['name'].lower() + ' ' + p['email'].lower()
            event_name_lower = event_id_to_name.get(p['event_id'], '').lower()

            match_search = (search_query == '' or search_query in name_email or search_query in event_name_lower)
            match_status = (status_filter == '' or p['status'].lower() == status_filter)

            if match_search and match_status:
                filtered_participants.append(p)
        participants = filtered_participants

    # context keys: participant_id, name, email, event_name, status
    participants_context = []
    for p in participants:
        participants_context.append({
            "participant_id": p["participant_id"],
            "name": p["name"],
            "email": p["email"],
            "event_name": event_id_to_name.get(p["event_id"], ""),
            "status": p["status"]
        })

    return render_template('participants.html', participants=participants_context)


@app.route('/venues', methods=['GET', 'POST'])
def venues_page():
    venues = load_venues()

    if request.method == 'POST':
        search_query = request.form.get('search', '').strip().lower()
        capacity_filter = request.form.get('capacity', '').strip().lower()

        filtered_venues = []
        for v in venues:
            name_location = v['venue_name'].lower() + ' ' + v['location'].lower()

            match_search = (search_query == '' or search_query in name_location)

            size_label = ''
            # capacity filter checking
            if capacity_filter == 'small':
                size_label = 'small'
            elif capacity_filter == 'medium':
                size_label = 'medium'
            elif capacity_filter == 'large':
                size_label = 'large'

            capacity = v['capacity']
            match_capacity = True
            if size_label == 'small':
                match_capacity = capacity < 501
            elif size_label == 'medium':
                match_capacity = 501 <= capacity <= 2000
            elif size_label == 'large':
                match_capacity = capacity > 2000

            if match_search and match_capacity:
                filtered_venues.append(v)
        venues = filtered_venues

    # context keys: venue_id, venue_name, location, capacity, amenities
    venues_context = [{
        "venue_id": v["venue_id"],
        "venue_name": v["venue_name"],
        "location": v["location"],
        "capacity": v["capacity"],
        "amenities": v["amenities"]
    } for v in venues]

    return render_template('venues.html', venues=venues_context)


@app.route('/schedules', methods=['GET', 'POST'])
def event_schedules_page():
    schedules = load_schedules()
    events = load_events()
    event_id_to_name = {e['event_id']: e['event_name'] for e in events}

    if request.method == 'POST':
        filter_date = request.form.get('date', '').strip()
        filter_event = request.form.get('event', '').strip()

        filtered_schedules = []
        for s in schedules:
            # filter by date = date part of session_time
            session_date = s['session_time'].split(' ')[0]
            match_date = (filter_date == '' or filter_date == session_date)
            match_event = (filter_event == '' or str(s['event_id']) == filter_event)

            if match_date and match_event:
                filtered_schedules.append(s)
        schedules = filtered_schedules

    # context keys: schedule_id, event_id, session_title, session_time, duration_minutes, speaker, venue_id
    schedules_context = []
    for s in schedules:
        schedules_context.append({
            "schedule_id": s["schedule_id"],
            "event_id": s["event_id"],
            "session_title": s["session_title"],
            "session_time": s["session_time"],
            "duration_minutes": s["duration_minutes"],
            "speaker": s["speaker"],
            "venue_id": s["venue_id"]
        })

    return render_template('event_schedules.html', schedules=schedules_context)


@app.route('/bookings')
def bookings_summary_page():
    bookings = load_bookings()
    events = load_events()
    event_id_to_name = {e['event_id']: e['event_name'] for e in events}

    bookings_context = []
    for b in bookings:
        event_name = event_id_to_name.get(b['event_id'], '')
        # Find event date
        event_date = ''
        matched_event = next((e for e in events if e['event_id'] == b['event_id']), None)
        if matched_event:
            event_date = matched_event['date']

        bookings_context.append({
            "booking_id": b["booking_id"],
            "event_name": event_name,
            "date": event_date,
            "ticket_count": b["ticket_count"],
            "status": b["status"]
        })

    return render_template('bookings_summary.html', bookings=bookings_context)


@app.route('/cancel_booking/<int:booking_id>', methods=['POST'])
def cancel_booking_action(booking_id):
    bookings = load_bookings()
    tickets = load_tickets()
    booking = next((b for b in bookings if b['booking_id'] == booking_id), None)
    if booking and booking['status'].lower() != 'cancelled':
        # Update booking status
        booking['status'] = 'Cancelled'

        # Update tickets: increase available_count, decrease sold_count accordingly
        ticket_info = next((t for t in tickets if t['event_id'] == booking['event_id'] and t['ticket_type'].lower() == booking['ticket_type'].lower()), None)
        if ticket_info:
            ticket_info['available_count'] += booking['ticket_count']
            ticket_info['sold_count'] -= booking['ticket_count']
            if ticket_info['sold_count'] < 0:
                ticket_info['sold_count'] = 0

        # Save updates
        save_bookings(bookings)
        save_tickets(tickets)

    # Refresh and show updated bookings
    return redirect(url_for('bookings_summary_page'))


if __name__ == '__main__':
    app.run(debug=True, port=5000)
