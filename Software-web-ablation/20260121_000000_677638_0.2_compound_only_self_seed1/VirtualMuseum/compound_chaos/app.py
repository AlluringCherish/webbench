from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Helper functions to read and write data files with pipe delimiter

def read_file_rows(filename):
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        return []
    with open(path, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]

def write_file_rows(filename, rows):
    path = os.path.join(DATA_DIR, filename)
    with open(path, 'w', encoding='utf-8') as f:
        for row in rows:
            f.write('|'.join(row) + '\n')

### Load Data Functions

# users.txt
# Fields: username
# Example: curator_john

def load_users():
    lines = read_file_rows('users.txt')
    users = [line for line in lines]
    return users

# galleries.txt
# Fields: gallery_id|gallery_name|floor|capacity|theme|status

def load_galleries():
    lines = read_file_rows('galleries.txt')
    galleries = []
    for line in lines:
        parts = line.split('|')
        if len(parts) != 6:
            continue
        gallery = {
            'gallery_id': int(parts[0]),
            'gallery_name': parts[1],
            'floor': int(parts[2]),
            'capacity': int(parts[3]),
            'theme': parts[4],
            'status': parts[5]
        }
        galleries.append(gallery)
    return galleries

# exhibitions.txt
# Fields: exhibition_id|title|description|gallery_id|exhibition_type|start_date|end_date|curator_name|created_by

def load_exhibitions():
    lines = read_file_rows('exhibitions.txt')
    exhibitions = []
    for line in lines:
        parts = line.split('|')
        if len(parts) != 9:
            continue
        exhibition = {
            'exhibition_id': int(parts[0]),
            'title': parts[1],
            'description': parts[2],
            'gallery_id': int(parts[3]),
            'exhibition_type': parts[4],
            'start_date': parts[5],
            'end_date': parts[6],
            'curator_name': parts[7],
            'created_by': parts[8]
        }
        exhibitions.append(exhibition)
    return exhibitions

# artifacts.txt
# Fields: artifact_id|artifact_name|period|origin|description|exhibition_id|storage_location|acquisition_date|added_by

def load_artifacts():
    lines = read_file_rows('artifacts.txt')
    artifacts = []
    for line in lines:
        parts = line.split('|')
        if len(parts) != 9:
            continue
        artifact = {
            'artifact_id': int(parts[0]),
            'artifact_name': parts[1],
            'period': parts[2],
            'origin': parts[3],
            'description': parts[4],
            'exhibition_id': int(parts[5]),
            'storage_location': parts[6],
            'acquisition_date': parts[7],
            'added_by': parts[8]
        }
        artifacts.append(artifact)
    return artifacts

# audioguides.txt
# Fields: guide_id|exhibit_number|title|language|duration|script|narrator|created_by

def load_audio_guides():
    lines = read_file_rows('audioguides.txt')
    guides = []
    for line in lines:
        parts = line.split('|')
        if len(parts) != 8:
            continue
        guide = {
            'guide_id': int(parts[0]),
            'exhibit_number': parts[1],
            'title': parts[2],
            'language': parts[3],
            'duration': parts[4],
            'script': parts[5],
            'narrator': parts[6],
            'created_by': parts[7]
        }
        guides.append(guide)
    return guides

# tickets.txt
# Fields: ticket_id|username|ticket_type|visit_date|visit_time|number_of_tickets|price|visitor_name|visitor_email|purchase_date

def load_tickets():
    lines = read_file_rows('tickets.txt')
    tickets = []
    for line in lines:
        parts = line.split('|')
        if len(parts) != 10:
            continue
        ticket = {
            'ticket_id': int(parts[0]),
            'username': parts[1],
            'ticket_type': parts[2],
            'visit_date': parts[3],
            'visit_time': parts[4],
            'number_of_tickets': int(parts[5]),
            'price': parts[6],
            'visitor_name': parts[7],
            'visitor_email': parts[8],
            'purchase_date': parts[9]
        }
        tickets.append(ticket)
    return tickets

def save_tickets(tickets):
    rows = []
    for t in tickets:
        rows.append([
            str(t['ticket_id']),
            t['username'],
            t['ticket_type'],
            t['visit_date'],
            t['visit_time'],
            str(t['number_of_tickets']),
            t['price'],
            t['visitor_name'],
            t['visitor_email'],
            t['purchase_date']
        ])
    write_file_rows('tickets.txt', rows)

# events.txt
# Fields: event_id|title|date|time|event_type|speaker|capacity|description|created_by

def load_events():
    lines = read_file_rows('events.txt')
    events = []
    for line in lines:
        parts = line.split('|')
        if len(parts) != 9:
            continue
        event = {
            'event_id': int(parts[0]),
            'title': parts[1],
            'date': parts[2],
            'time': parts[3],
            'event_type': parts[4],
            'speaker': parts[5],
            'capacity': int(parts[6]),
            'description': parts[7],
            'created_by': parts[8]
        }
        events.append(event)
    return events

# event_registrations.txt
# Fields: registration_id|event_id|username|registration_date

def load_event_registrations():
    lines = read_file_rows('event_registrations.txt')
    regs = []
    for line in lines:
        parts = line.split('|')
        if len(parts) != 4:
            continue
        reg = {
            'registration_id': int(parts[0]),
            'event_id': int(parts[1]),
            'username': parts[2],
            'registration_date': parts[3]
        }
        regs.append(reg)
    return regs


def save_event_registrations(registrations):
    rows = []
    for r in registrations:
        rows.append([
            str(r['registration_id']),
            str(r['event_id']),
            r['username'],
            r['registration_date']
        ])
    write_file_rows('event_registrations.txt', rows)


# Root redirect
@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))


# Dashboard route
@app.route('/dashboard')
def dashboard():
    exhibitions = load_exhibitions()
    total_exhibitions = len(exhibitions)
    # active exhibitions: check if current date is between start and end dates
    today = datetime.today().date()
    active_exhibitions = 0
    for ex in exhibitions:
        try:
            start = datetime.strptime(ex['start_date'], '%Y-%m-%d').date()
            end = datetime.strptime(ex['end_date'], '%Y-%m-%d').date()
            if start <= today <= end:
                active_exhibitions += 1
        except Exception:
            continue
    exhibitions_summary = {
        'total_exhibitions': total_exhibitions,
        'active_exhibitions': active_exhibitions
    }
    return render_template('dashboard.html', exhibitions_summary=exhibitions_summary)


# Artifact Catalog route
@app.route('/artifact-catalog', methods=['GET', 'POST'])
def artifact_catalog():
    artifacts = load_artifacts()
    search_query = ''
    filters = {}

    if request.method == 'POST':
        search_query = request.form.get('search-artifact', '').strip()
    else:
        search_query = request.args.get('search-artifact', '').strip()

    if search_query:
        search_lower = search_query.lower()
        filtered = []
        for art in artifacts:
            # Search by artifact_name or artifact_id
            if search_lower in art['artifact_name'].lower() or str(art['artifact_id']) == search_query:
                filtered.append(art)
        artifacts = filtered

    return render_template('artifact_catalog.html', artifacts=artifacts, search_query=search_query, filters=filters)


# Exhibitions route
@app.route('/exhibitions', methods=['GET', 'POST'])
def exhibitions():
    exhibitions = load_exhibitions()
    filter_type = ''
    if request.method == 'POST':
        filter_type = request.form.get('filter-exhibition-type', '').strip()
    else:
        filter_type = request.args.get('filter-exhibition-type', '').strip()
    if filter_type in ['Permanent', 'Temporary', 'Virtual']:
        exhibitions = [ex for ex in exhibitions if ex['exhibition_type'] == filter_type]
    else:
        filter_type = ''
    return render_template('exhibitions.html', exhibitions=exhibitions, filter_type=filter_type)


# Exhibition Details route
@app.route('/exhibition/<int:exhibition_id>')
def exhibition_details(exhibition_id):
    exhibitions = load_exhibitions()
    exhibition = next((ex for ex in exhibitions if ex['exhibition_id'] == exhibition_id), None)
    if not exhibition:
        # Could handle 404 better, but just empty
        exhibition = None
        artifacts = []
    else:
        artifacts_all = load_artifacts()
        artifacts = [a for a in artifacts_all if a['exhibition_id'] == exhibition_id]

    return render_template('exhibition_details.html', exhibition=exhibition, artifacts=artifacts)


# Visitor Tickets route
@app.route('/visitor-tickets', methods=['GET', 'POST'])
def visitor_tickets():
    # For this design, no login system; assume single user for demonstration
    current_username = 'visitor_mary'
    ticket_types = ["Standard", "Student", "Senior", "Family", "VIP"]
    my_tickets = []
    tickets = load_tickets()
    my_tickets = [t for t in tickets if t['username'] == current_username]
    
    return render_template('visitor_tickets.html', ticket_types=ticket_types, my_tickets=my_tickets)


# Virtual Events route
@app.route('/virtual-events', methods=['GET', 'POST'])
def virtual_events():
    current_username = 'visitor_mary'
    events = load_events()
    registrations = load_event_registrations()
    user_regs = [r for r in registrations if r['username'] == current_username]
    return render_template('virtual_events.html', events=events, registrations=user_regs)


# Audio Guides route
@app.route('/audio-guides', methods=['GET', 'POST'])
def audio_guides():
    filter_language = ''
    if request.method == 'POST':
        filter_language = request.form.get('filter-language', '').strip()
    else:
        filter_language = request.args.get('filter-language', '').strip()

    guides = load_audio_guides()
    if filter_language in ['English', 'Spanish', 'French']:
        guides = [g for g in guides if g['language'] == filter_language]
    else:
        filter_language = ''

    return render_template('audio_guides.html', audio_guides=guides, filter_language=filter_language)


# Register event route
@app.route('/virtual-events/register/<int:event_id>', methods=['POST'])
def register_event(event_id):
    current_username = 'visitor_mary'
    registrations = load_event_registrations()
    events = load_events()

    # Check if event exists
    event = next((ev for ev in events if ev['event_id'] == event_id), None)
    if not event:
        return redirect(url_for('virtual_events'))

    # Check if user already registered
    already_reg = any(r['event_id'] == event_id and r['username'] == current_username for r in registrations)
    if not already_reg:
        # Add new registration
        max_reg_id = max([r['registration_id'] for r in registrations], default=0)
        new_reg = {
            'registration_id': max_reg_id + 1,
            'event_id': event_id,
            'username': current_username,
            'registration_date': datetime.today().strftime('%Y-%m-%d')
        }
        registrations.append(new_reg)
        save_event_registrations(registrations)
    return redirect(url_for('virtual_events'))


# Cancel registration route
@app.route('/virtual-events/cancel/<int:registration_id>', methods=['POST'])
def cancel_registration(registration_id):
    current_username = 'visitor_mary'
    registrations = load_event_registrations()
    registrations = [r for r in registrations if not (r['registration_id'] == registration_id and r['username'] == current_username)]
    save_event_registrations(registrations)
    return redirect(url_for('virtual_events'))


# Purchase ticket route
@app.route('/purchase-ticket', methods=['POST'])
def purchase_ticket():
    # Inputs: ticket_type, visit_date, visit_time, number_of_tickets, price, visitor_name, visitor_email
    current_username = 'visitor_mary'
    ticket_type = request.form.get('ticket-type', '').strip()
    visit_date = request.form.get('visit-date', '').strip()
    visit_time = request.form.get('visit-time', '').strip()
    number_of_tickets = request.form.get('number-of-tickets', '').strip()
    price = request.form.get('price', '').strip()
    visitor_name = request.form.get('visitor-name', '').strip()
    visitor_email = request.form.get('visitor-email', '').strip()

    # Validation basic
    try:
        number_of_tickets = int(number_of_tickets)
        if number_of_tickets <= 0:
            raise ValueError
    except Exception:
        number_of_tickets = 1

    # Load existing tickets
    tickets = load_tickets()
    max_ticket_id = max([t['ticket_id'] for t in tickets], default=0)

    new_ticket = {
        'ticket_id': max_ticket_id + 1,
        'username': current_username,
        'ticket_type': ticket_type,
        'visit_date': visit_date,
        'visit_time': visit_time,
        'number_of_tickets': number_of_tickets,
        'price': price,
        'visitor_name': visitor_name,
        'visitor_email': visitor_email,
        'purchase_date': datetime.today().strftime('%Y-%m-%d')
    }
    tickets.append(new_ticket)
    save_tickets(tickets)

    return redirect(url_for('visitor_tickets'))


if __name__ == "__main__":
    app.run(port=5000, debug=True)
