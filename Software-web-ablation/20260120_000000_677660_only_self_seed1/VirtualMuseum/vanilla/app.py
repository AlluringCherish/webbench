from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

data_folder = 'data'

# Utility functions for reading and writing files

def read_file_lines(filename):
    try:
        with open(os.path.join(data_folder, filename), 'r', encoding='utf-8') as f:
            return f.readlines()
    except FileNotFoundError:
        return []

# Helper for reading exhibitions
# Fields:
# exhibition_id (int), title (str), description (str), gallery_id (int), exhibition_type (str),
# start_date (date), end_date (date), curator_name (str), created_by (str)
def load_exhibitions():
    exhibitions = []
    lines = read_file_lines('exhibitions.txt')
    for line in lines:
        parts = line.strip().split('|')
        if len(parts) < 9:
            continue
        try:
            exhibition = {
                'exhibition_id': int(parts[0]),
                'title': parts[1],
                'description': parts[2],
                'gallery_id': int(parts[3]),
                'exhibition_type': parts[4],
                'start_date': parts[5],
                'end_date': parts[6],
                'curator_name': parts[7],
                'created_by': parts[8],
            }
            exhibitions.append(exhibition)
        except Exception:
            continue
    return exhibitions

# Helper for reading artifacts
# Fields:
# artifact_id (int), artifact_name (str), period (str), origin (str), description (str),
# exhibition_id (int), storage_location (str), acquisition_date (date), added_by (str)
def load_artifacts():
    artifacts = []
    lines = read_file_lines('artifacts.txt')
    for line in lines:
        parts = line.strip().split('|')
        if len(parts) < 9:
            continue
        try:
            artifact = {
                'artifact_id': int(parts[0]),
                'artifact_name': parts[1],
                'period': parts[2],
                'origin': parts[3],
                'description': parts[4],
                'exhibition_id': int(parts[5]),
                'storage_location': parts[6],
                'acquisition_date': parts[7],
                'added_by': parts[8],
            }
            artifacts.append(artifact)
        except Exception:
            continue
    return artifacts

# Helper for reading tickets
# Fields:
# ticket_id (int), username (str), ticket_type (str), visit_date (date), visit_time (str), number_of_tickets (int),
# price (float), visitor_name (str), visitor_email (str), purchase_date (date)
def load_tickets():
    tickets = []
    lines = read_file_lines('tickets.txt')
    for line in lines:
        parts = line.strip().split('|')
        if len(parts) < 10:
            continue
        try:
            ticket = {
                'ticket_id': int(parts[0]),
                'username': parts[1],
                'ticket_type': parts[2],
                'visit_date': parts[3],
                'visit_time': parts[4],
                'number_of_tickets': int(parts[5]),
                'price': float(parts[6]),
                'visitor_name': parts[7],
                'visitor_email': parts[8],
                'purchase_date': parts[9],
            }
            tickets.append(ticket)
        except Exception:
            continue
    return tickets

def save_tickets(tickets):
    try:
        with open(os.path.join(data_folder, 'tickets.txt'), 'w', encoding='utf-8') as f:
            for t in tickets:
                line = '|'.join([
                    str(t['ticket_id']),
                    t['username'],
                    t['ticket_type'],
                    t['visit_date'],
                    t['visit_time'],
                    str(t['number_of_tickets']),
                    str(t['price']),
                    t['visitor_name'],
                    t['visitor_email'],
                    t['purchase_date']
                ])
                f.write(line + '\n')
        return True
    except Exception:
        return False

# Helper for reading events
# Fields:
# event_id (int), title (str), date (date), time (str), event_type (str), speaker (str), capacity (int), description (str), created_by (str)
def load_events():
    events = []
    lines = read_file_lines('events.txt')
    for line in lines:
        parts = line.strip().split('|')
        if len(parts) < 9:
            continue
        try:
            event = {
                'event_id': int(parts[0]),
                'title': parts[1],
                'date': parts[2],
                'time': parts[3],
                'event_type': parts[4],
                'speaker': parts[5],
                'capacity': int(parts[6]),
                'description': parts[7],
                'created_by': parts[8],
            }
            events.append(event)
        except Exception:
            continue
    return events

# Helper for reading event registrations
# Fields:
# registration_id (int), event_id (int), username (str), registration_date (date)
def load_event_registrations():
    registrations = []
    lines = read_file_lines('event_registrations.txt')
    for line in lines:
        parts = line.strip().split('|')
        if len(parts) < 4:
            continue
        try:
            registration = {
                'registration_id': int(parts[0]),
                'event_id': int(parts[1]),
                'username': parts[2],
                'registration_date': parts[3],
            }
            registrations.append(registration)
        except Exception:
            continue
    return registrations

def save_event_registrations(registrations):
    try:
        with open(os.path.join(data_folder, 'event_registrations.txt'), 'w', encoding='utf-8') as f:
            for r in registrations:
                line = '|'.join([
                    str(r['registration_id']),
                    str(r['event_id']),
                    r['username'],
                    r['registration_date']
                ])
                f.write(line + '\n')
        return True
    except Exception:
        return False

# Helper for reading audioguides
# Fields:
# guide_id (int), exhibit_number (int), title (str), language (str), duration (int), script (str), narrator (str), created_by (str)
def load_audioguides():
    guides = []
    lines = read_file_lines('audioguides.txt')
    for line in lines:
        parts = line.strip().split('|')
        if len(parts) < 8:
            continue
        try:
            guide = {
                'guide_id': int(parts[0]),
                'exhibit_number': int(parts[1]),
                'title': parts[2],
                'language': parts[3],
                'duration': int(parts[4]),
                'script': parts[5],
                'narrator': parts[6],
                'created_by': parts[7],
            }
            guides.append(guide)
        except Exception:
            continue
    return guides

# Helper for reading users.txt for user listing
# single field username
def load_users():
    users = []
    lines = read_file_lines('users.txt')
    for line in lines:
        user = line.strip()
        if user:
            users.append(user)
    return users

# Helper for reading galleries.txt
# Fields:
# gallery_id (int), gallery_name (str), floor (int), capacity (int), theme (str), status (str)
def load_galleries():
    galleries = []
    lines = read_file_lines('galleries.txt')
    for line in lines:
        parts = line.strip().split('|')
        if len(parts) < 6:
            continue
        try:
            gallery = {
                'gallery_id': int(parts[0]),
                'gallery_name': parts[1],
                'floor': int(parts[2]),
                'capacity': int(parts[3]),
                'theme': parts[4],
                'status': parts[5],
            }
            galleries.append(gallery)
        except Exception:
            continue
    return galleries

# Route / redirects to /dashboard
@app.route('/', methods=['GET'])
def root_redirect():
    return redirect(url_for('dashboard_view'))

# /dashboard route GET
@app.route('/dashboard', methods=['GET'])
def dashboard_view():
    exhibitions = load_exhibitions()
    exhibitions_count = len(exhibitions)
    # Active exhibitions are those where current date between start_date and end_date inclusive
    today_str = datetime.today().strftime('%Y-%m-%d')
    active_exhibitions_count = 0
    for ex in exhibitions:
        try:
            if ex['start_date'] <= today_str <= ex['end_date']:
                active_exhibitions_count += 1
        except Exception:
            pass
    return render_template('dashboard.html', exhibitions_count=exhibitions_count, active_exhibitions_count=active_exhibitions_count)

# /artifact-catalog GET, POST
@app.route('/artifact-catalog', methods=['GET', 'POST'])
def artifact_catalog_view():
    artifacts = load_artifacts()
    if request.method == 'POST':
        search_query = request.form.get('search_query', '').strip()
        filtered_artifacts = []
        if search_query:
            lowered = search_query.lower()
            for art in artifacts:
                # match id or name case-insensitive
                if (str(art['artifact_id']) == search_query) or (lowered in art['artifact_name'].lower()):
                    filtered_artifacts.append(art)
        else:
            filtered_artifacts = artifacts[:]  # no filter means all
        return render_template('artifact_catalog.html', artifacts=artifacts, filtered_artifacts=filtered_artifacts, search_query=search_query)
    else:
        # GET
        return render_template('artifact_catalog.html', artifacts=artifacts, filtered_artifacts=[], search_query='')

# /exhibitions GET, POST
@app.route('/exhibitions', methods=['GET', 'POST'])
def exhibitions_view():
    exhibition_types = ["Permanent", "Temporary", "Virtual"]
    exhibitions = load_exhibitions()
    filtered_exhibitions = []
    if request.method == 'POST':
        filter_type = request.form.get('filter_type', '').strip()
        if filter_type and filter_type in exhibition_types:
            filtered_exhibitions = [ex for ex in exhibitions if ex['exhibition_type'] == filter_type]
        else:
            filtered_exhibitions = exhibitions[:]
    else:
        filtered_exhibitions = exhibitions[:]
    return render_template('exhibitions.html', exhibitions=exhibitions, filtered_exhibitions=filtered_exhibitions, exhibition_types=exhibition_types)

# /exhibition/<int:exhibition_id> GET
@app.route('/exhibition/<int:exhibition_id>', methods=['GET'])
def exhibition_details_view(exhibition_id):
    exhibitions = load_exhibitions()
    exhibition = None
    for ex in exhibitions:
        if ex['exhibition_id'] == exhibition_id:
            exhibition = ex
            break
    if exhibition is None:
        return f"Exhibition with id {exhibition_id} not found", 404
    artifacts = load_artifacts()
    related_artifacts = [art for art in artifacts if art['exhibition_id'] == exhibition_id]
    return render_template('exhibition_details.html', exhibition=exhibition, artifacts=related_artifacts)

# /visitor-tickets GET, POST
@app.route('/visitor-tickets', methods=['GET', 'POST'])
def visitor_tickets_view():
    # We'll assume a fixed current user for demo, since no auth specified
    current_username = 'visitor_mary'
    tickets = load_tickets()
    user_tickets = [t for t in tickets if t['username'] == current_username]
    ticket_types = ["Standard", "Student", "Senior", "Family", "VIP"]
    purchase_result = None

    if request.method == 'POST':
        # Process ticket purchase
        ticket_type = request.form.get('ticket_type', '').strip()
        number_of_tickets = request.form.get('number_of_tickets', '').strip()
        visitor_name = request.form.get('visitor_name', '').strip()
        visitor_email = request.form.get('visitor_email', '').strip()
        visit_date = request.form.get('visit_date', '').strip()
        visit_time = request.form.get('visit_time', '').strip()

        # Validate inputs
        if ticket_type not in ticket_types:
            purchase_result = 'Invalid ticket type selected.'
        else:
            try:
                number_of_tickets_int = int(number_of_tickets)
                if number_of_tickets_int <= 0:
                    raise ValueError
                datetime.strptime(visit_date, '%Y-%m-%d')
                if not visitor_name or not visitor_email or not visit_time:
                    raise ValueError

                # In a real app, price would be computed differently, for now just base price per ticket type (fixed)
                base_prices = {
                    "Standard": 15,
                    "Student": 10,
                    "Senior": 12,
                    "Family": 35,
                    "VIP": 50
                }
                price = base_prices.get(ticket_type, 15) * number_of_tickets_int

                # Get new ticket_id
                max_ticket_id = max([t['ticket_id'] for t in tickets], default=0)
                new_id = max_ticket_id + 1
                purchase_date = datetime.today().strftime('%Y-%m-%d')

                new_ticket = {
                    'ticket_id': new_id,
                    'username': current_username,
                    'ticket_type': ticket_type,
                    'visit_date': visit_date,
                    'visit_time': visit_time,
                    'number_of_tickets': number_of_tickets_int,
                    'price': price,
                    'visitor_name': visitor_name,
                    'visitor_email': visitor_email,
                    'purchase_date': purchase_date
                }

                tickets.append(new_ticket)
                if save_tickets(tickets):
                    purchase_result = 'Ticket purchase successful.'
                    user_tickets.append(new_ticket)
                else:
                    purchase_result = 'Failed to save ticket purchase.'
            except Exception:
                purchase_result = 'Invalid input data for ticket purchase.'

    return render_template('visitor_tickets.html', tickets=user_tickets, ticket_types=ticket_types, purchase_result=purchase_result)

# /virtual-events GET, POST
@app.route('/virtual-events', methods=['GET', 'POST'])
def virtual_events_view():
    # Assume user visitor_mary
    current_username = 'visitor_mary'
    events = load_events()
    registrations = load_event_registrations()
    user_registrations = set(r['registration_id'] for r in registrations if r['username'] == current_username)

    filtered_events = events[:]
    filter_type = ''
    if request.method == 'POST':
        filter_type = request.form.get('filter_event_type', '').strip()
        if filter_type:
            filtered_events = [e for e in events if e['event_type'] == filter_type]

    return render_template('virtual_events.html', events=events, event_registrations=registrations, user_registrations=user_registrations, filter_type=filter_type)

# /audio-guides GET, POST
@app.route('/audio-guides', methods=['GET', 'POST'])
def audio_guides_view():
    audioguides = load_audioguides()
    filter_language = ''
    filtered_guides = []
    if request.method == 'POST':
        filter_language = request.form.get('filter_language', '').strip()
        if filter_language:
            filtered_guides = [g for g in audioguides if g['language'] == filter_language]
        else:
            filtered_guides = audioguides[:]
    else:
        filtered_guides = []
    return render_template('audio_guides.html', audioguides=audioguides, filter_language=filter_language, filtered_guides=filtered_guides)

# /register-event/<int:event_id> POST
@app.route('/register-event/<int:event_id>', methods=['POST'])
def register_event(event_id):
    current_username = 'visitor_mary'
    events = load_events()
    event = None
    for e in events:
        if e['event_id'] == event_id:
            event = e
            break
    if event is None:
        return "Event not found", 404

    registrations = load_event_registrations()
    # Check if user already registered
    for r in registrations:
        if r['event_id'] == event_id and r['username'] == current_username:
            # Already registered
            return redirect(url_for('virtual_events_view'))

    # Check capacity
    current_reg_count = sum(1 for r in registrations if r['event_id'] == event_id)
    if current_reg_count >= event['capacity']:
        # No capacity
        return redirect(url_for('virtual_events_view'))

    max_reg_id = max([r['registration_id'] for r in registrations], default=0)
    new_reg_id = max_reg_id + 1
    registration_date = datetime.today().strftime('%Y-%m-%d')
    new_registration = {
        'registration_id': new_reg_id,
        'event_id': event_id,
        'username': current_username,
        'registration_date': registration_date
    }
    registrations.append(new_registration)
    save_event_registrations(registrations)
    return redirect(url_for('virtual_events_view'))

# /cancel-registration/<int:registration_id> POST
@app.route('/cancel-registration/<int:registration_id>', methods=['POST'])
def cancel_registration(registration_id):
    current_username = 'visitor_mary'
    registrations = load_event_registrations()
    filtered_regs = [r for r in registrations if not (r['registration_id'] == registration_id and r['username'] == current_username)]
    if len(filtered_regs) == len(registrations):
        # not found or not owned, just redirect
        return redirect(url_for('virtual_events_view'))
    # saved filtered
    save_event_registrations(filtered_regs)
    return redirect(url_for('virtual_events_view'))

if __name__ == "__main__":
    app.run(port=5000, debug=True)
