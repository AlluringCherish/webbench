from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Helper functions to load and save data

def load_exhibitions():
    path = os.path.join(DATA_DIR, 'exhibitions.txt')
    exhibitions = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                fields = line.strip().split('|')
                if len(fields) != 9:
                    continue
                exhibition = {
                    'exhibition_id': int(fields[0]),
                    'title': fields[1],
                    'description': fields[2],
                    'gallery_id': int(fields[3]),
                    'exhibition_type': fields[4],
                    'start_date': fields[5],
                    'end_date': fields[6],
                    'curator_name': fields[7],
                    'created_by': fields[8]
                }
                exhibitions.append(exhibition)
    except FileNotFoundError:
        pass
    return exhibitions


def load_artifacts():
    path = os.path.join(DATA_DIR, 'artifacts.txt')
    artifacts = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                fields = line.strip().split('|')
                if len(fields) != 9:
                    continue
                artifact = {
                    'artifact_id': int(fields[0]),
                    'artifact_name': fields[1],
                    'period': fields[2],
                    'origin': fields[3],
                    'description': fields[4],
                    'exhibition_id': int(fields[5]),
                    'storage_location': fields[6],
                    'acquisition_date': fields[7],
                    'added_by': fields[8]
                }
                artifacts.append(artifact)
    except FileNotFoundError:
        pass
    return artifacts


def load_galleries():
    path = os.path.join(DATA_DIR, 'galleries.txt')
    galleries = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                fields = line.strip().split('|')
                if len(fields) != 6:
                    continue
                gallery = {
                    'gallery_id': int(fields[0]),
                    'gallery_name': fields[1],
                    'floor': int(fields[2]),
                    'capacity': int(fields[3]),
                    'theme': fields[4],
                    'status': fields[5]
                }
                galleries.append(gallery)
    except FileNotFoundError:
        pass
    return galleries


def load_ticket_types():
    # From specification Section 2 Visitor Tickets page
    return ['Standard', 'Student', 'Senior', 'Family', 'VIP']


def load_tickets():
    path = os.path.join(DATA_DIR, 'tickets.txt')
    tickets = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                fields = line.strip().split('|')
                if len(fields) != 10:
                    continue
                ticket = {
                    'ticket_id': int(fields[0]),
                    'username': fields[1],
                    'ticket_type': fields[2],
                    'visit_date': fields[3],
                    'visit_time': fields[4],
                    'number_of_tickets': int(fields[5]),
                    'price': float(fields[6]),
                    'visitor_name': fields[7],
                    'visitor_email': fields[8],
                    'purchase_date': fields[9]
                }
                tickets.append(ticket)
    except FileNotFoundError:
        pass
    return tickets


def save_tickets(tickets):
    path = os.path.join(DATA_DIR, 'tickets.txt')
    try:
        with open(path, 'w', encoding='utf-8') as f:
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
    except Exception:
        pass


def load_events():
    path = os.path.join(DATA_DIR, 'events.txt')
    events = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                fields = line.strip().split('|')
                if len(fields) != 9:
                    continue
                event = {
                    'event_id': int(fields[0]),
                    'title': fields[1],
                    'date': fields[2],
                    'time': fields[3],
                    'event_type': fields[4],
                    'speaker': fields[5],
                    'capacity': int(fields[6]),
                    'description': fields[7],
                    'created_by': fields[8]
                }
                events.append(event)
    except FileNotFoundError:
        pass
    return events


def load_event_registrations():
    path = os.path.join(DATA_DIR, 'event_registrations.txt')
    registrations = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                fields = line.strip().split('|')
                if len(fields) != 4:
                    continue
                reg = {
                    'registration_id': int(fields[0]),
                    'event_id': int(fields[1]),
                    'username': fields[2],
                    'registration_date': fields[3]
                }
                registrations.append(reg)
    except FileNotFoundError:
        pass
    return registrations


def save_event_registrations(registrations):
    path = os.path.join(DATA_DIR, 'event_registrations.txt')
    try:
        with open(path, 'w', encoding='utf-8') as f:
            for r in registrations:
                line = '|'.join([
                    str(r['registration_id']),
                    str(r['event_id']),
                    r['username'],
                    r['registration_date']
                ])
                f.write(line + '\n')
    except Exception:
        pass


def load_audio_guides():
    path = os.path.join(DATA_DIR, 'audioguides.txt')
    guides = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                fields = line.strip().split('|')
                if len(fields) != 8:
                    continue
                guide = {
                    'guide_id': int(fields[0]),
                    'exhibit_number': fields[1],
                    'title': fields[2],
                    'language': fields[3],
                    'duration': fields[4],
                    'script': fields[5],
                    'narrator': fields[6],
                    'created_by': fields[7]
                }
                guides.append(guide)
    except FileNotFoundError:
        pass
    return guides

# Root redirect
@app.route('/', methods=['GET'])
def root_redirect():
    return redirect(url_for('dashboard'))

# Dashboard
@app.route('/dashboard', methods=['GET'])
def dashboard():
    exhibitions = load_exhibitions()
    total_exhibitions = len(exhibitions)
    # Active exhibitions: current date between start_date and end_date inclusive
    today = datetime.now().date()
    active_count = 0
    for ex in exhibitions:
        try:
            start = datetime.strptime(ex['start_date'], '%Y-%m-%d').date()
            end = datetime.strptime(ex['end_date'], '%Y-%m-%d').date()
            if start <= today <= end:
                active_count += 1
        except Exception:
            continue
    exhibition_summary = {
        'total_exhibitions': total_exhibitions,
        'active_exhibitions': active_count
    }
    return render_template('dashboard.html', exhibition_summary=exhibition_summary)

# Artifact Catalog
@app.route('/artifact_catalog', methods=['GET', 'POST'])
def artifact_catalog():
    artifacts = load_artifacts()
    search_query = None
    filter_applied = False
    if request.method == 'POST':
        search_query = request.form.get('search-artifact')
        if search_query and search_query.strip():
            search_query = search_query.strip()
            # Search artifacts by artifact_name or artifact_id
            filtered = []
            for art in artifacts:
                if search_query.lower() in art['artifact_name'].lower():
                    filtered.append(art)
                    continue
                try:
                    if int(search_query) == art['artifact_id']:
                        filtered.append(art)
                except Exception:
                    pass
            artifacts = filtered
            filter_applied = True
    return render_template('artifact_catalog.html', artifacts=artifacts, search_query=search_query, filter_applied=filter_applied)

# Exhibitions
@app.route('/exhibitions', methods=['GET', 'POST'])
def exhibitions():
    exhibitions = load_exhibitions()
    exhibition_types = ['Permanent', 'Temporary', 'Virtual']
    selected_type = None
    if request.method == 'POST':
        selected_type = request.form.get('filter-exhibition-type')
        if selected_type and selected_type in exhibition_types:
            exhibitions = [ex for ex in exhibitions if ex['exhibition_type'] == selected_type]
    return render_template('exhibitions.html', exhibitions=exhibitions, exhibition_types=exhibition_types, selected_type=selected_type)

# Exhibition Details
@app.route('/exhibition/<int:exhibition_id>', methods=['GET'])
def exhibition_details(exhibition_id):
    exhibitions = load_exhibitions()
    exhibition = None
    for ex in exhibitions:
        if ex['exhibition_id'] == exhibition_id:
            exhibition = ex
            break
    if not exhibition:
        return "Exhibition not found", 404
    artifacts = load_artifacts()
    exhibition_artifacts = [art for art in artifacts if art['exhibition_id'] == exhibition_id]
    return render_template('exhibition_details.html', exhibition=exhibition, artifacts=exhibition_artifacts)

# Visitor Tickets
@app.route('/visitor_tickets', methods=['GET', 'POST'])
def visitor_tickets():
    ticket_types = load_ticket_types()
    purchased_tickets = load_tickets()
    purchase_message = None

    if request.method == 'POST':
        # Collect form data
        ticket_type = request.form.get('ticket-type')
        number_of_tickets_raw = request.form.get('number-of-tickets')
        visitor_name = request.form.get('visitor-name')
        visitor_email = request.form.get('visitor-email')
        visit_date = request.form.get('visit-date')
        visit_time = request.form.get('visit-time')
        username = request.form.get('username')

        # Validate required fields
        if not ticket_type or ticket_type not in ticket_types:
            purchase_message = "Invalid ticket type."
        else:
            try:
                number_of_tickets = int(number_of_tickets_raw)
                if number_of_tickets < 1:
                    raise ValueError()
            except Exception:
                purchase_message = "Invalid number of tickets."

        if not purchase_message:
            if not visitor_name or not visitor_email or not visit_date or not visit_time or not username:
                purchase_message = "Missing required fields."

        # Prices assignment
        ticket_prices = {
            'Standard': 15.0,
            'Student': 10.0,
            'Senior': 12.0,
            'Family': 40.0,
            'VIP': 50.0
        }

        if not purchase_message:
            price_per_ticket = ticket_prices.get(ticket_type, 0)
            total_price = price_per_ticket * number_of_tickets

            # Assign ticket_id
            max_id = max([t['ticket_id'] for t in purchased_tickets], default=0)
            ticket_id = max_id + 1
            purchase_date_str = datetime.now().strftime('%Y-%m-%d')

            new_ticket = {
                'ticket_id': ticket_id,
                'username': username,
                'ticket_type': ticket_type,
                'visit_date': visit_date,
                'visit_time': visit_time,
                'number_of_tickets': number_of_tickets,
                'price': total_price,
                'visitor_name': visitor_name,
                'visitor_email': visitor_email,
                'purchase_date': purchase_date_str
            }

            purchased_tickets.append(new_ticket)
            save_tickets(purchased_tickets)
            purchase_message = f"Successfully purchased {number_of_tickets} {ticket_type} ticket(s)."

    return render_template('visitor_tickets.html', ticket_types=ticket_types, purchased_tickets=purchased_tickets, purchase_message=purchase_message)

# Virtual Events
@app.route('/virtual_events', methods=['GET', 'POST'])
def virtual_events():
    events = load_events()
    user_registrations = load_event_registrations()
    registration_message = None

    # Assume user is identified by 'username' from form or default 'visitor_mary'
    username = request.form.get('username') if request.method == 'POST' else request.args.get('username')
    if not username:
        username = 'visitor_mary'

    if request.method == 'POST':
        action = request.form.get('action')
        event_id_raw = request.form.get('event_id')
        if not event_id_raw:
            registration_message = "No event selected."
        else:
            try:
                event_id = int(event_id_raw)
            except Exception:
                registration_message = "Invalid event ID."

        if not registration_message:
            if action == 'register':
                # Check if already registered
                already_registered = any(
                    reg['event_id'] == event_id and reg['username'] == username for reg in user_registrations
                )
                if already_registered:
                    registration_message = "Already registered for this event."
                else:
                    new_id = max([r['registration_id'] for r in user_registrations], default=0) + 1
                    new_reg = {
                        'registration_id': new_id,
                        'event_id': event_id,
                        'username': username,
                        'registration_date': datetime.now().strftime('%Y-%m-%d')
                    }
                    user_registrations.append(new_reg)
                    save_event_registrations(user_registrations)
                    registration_message = "Registration successful."
            elif action == 'cancel':
                # Find registration and remove
                found = False
                for i, reg in enumerate(user_registrations):
                    if reg['event_id'] == event_id and reg['username'] == username:
                        found = True
                        del user_registrations[i]
                        save_event_registrations(user_registrations)
                        registration_message = "Registration cancelled."
                        break
                if not found:
                    registration_message = "No registration found to cancel."
            else:
                registration_message = "Invalid action."

    # Filter user's registrations
    user_regs = [r for r in user_registrations if r['username'] == username]

    return render_template('virtual_events.html', events=events, user_registrations=user_regs, registration_message=registration_message)

# Audio Guides
@app.route('/audio_guides', methods=['GET', 'POST'])
def audio_guides():
    guides = load_audio_guides()
    languages = ['English', 'Spanish', 'French']
    selected_language = None
    if request.method == 'POST':
        selected_language = request.form.get('filter-language')
        if selected_language and selected_language in languages:
            guides = [g for g in guides if g['language'] == selected_language]
    return render_template('audio_guides.html', audio_guides=guides, languages=languages, selected_language=selected_language)


if __name__ == "__main__":
    app.run(port=5000, debug=True)
