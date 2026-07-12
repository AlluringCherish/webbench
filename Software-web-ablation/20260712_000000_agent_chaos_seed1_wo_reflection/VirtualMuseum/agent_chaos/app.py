from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'
CURRENT_USER = 'visitor_mary'  # Assuming a fixed current user for the scope of this app

# Helper function to safely read pipe-delimited files

def read_pipe_delimited_file(filename, num_fields=None):
    filepath = os.path.join(DATA_DIR, filename)
    data = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if num_fields is not None and len(parts) != num_fields:
                    continue  # Skip malformed lines
                data.append(parts)
    except FileNotFoundError:
        # Return empty list if file not found
        return []
    return data

# Helper to write pipe-delimited file from list of lists

def write_pipe_delimited_file(filename, records):
    filepath = os.path.join(DATA_DIR, filename)
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            for record in records:
                f.write('|'.join(str(field) for field in record) + '\n')
        return True
    except Exception:
        return False

# Parse exhibition record list to dict with proper types

def parse_exhibition(row):
    return {
        'exhibition_id': int(row[0]),
        'title': row[1],
        'description': row[2],
        'gallery_id': int(row[3]),
        'exhibition_type': row[4],
        'start_date': row[5],
        'end_date': row[6],
        'curator_name': row[7],
        'created_by': row[8]
    }

# Parse artifact record

def parse_artifact(row):
    return {
        'artifact_id': int(row[0]),
        'artifact_name': row[1],
        'period': row[2],
        'origin': row[3],
        'description': row[4],
        'exhibition_id': int(row[5]),
        'storage_location': row[6],
        'acquisition_date': row[7],
        'added_by': row[8]
    }

# Parse ticket record

def parse_ticket(row):
    return {
        'ticket_id': int(row[0]),
        'username': row[1],
        'ticket_type': row[2],
        'visit_date': row[3],
        'visit_time': row[4],
        'number_of_tickets': int(row[5]),
        'price': float(row[6]),
        'visitor_name': row[7],
        'visitor_email': row[8],
        'purchase_date': row[9]
    }

# Parse event record

def parse_event(row):
    return {
        'event_id': int(row[0]),
        'title': row[1],
        'date': row[2],
        'time': row[3],
        'event_type': row[4],
        'speaker': row[5],
        'capacity': int(row[6]),
        'description': row[7],
        'created_by': row[8]
    }

# Parse event registration record

def parse_registration(row):
    return {
        'registration_id': int(row[0]),
        'event_id': int(row[1]),
        'username': row[2],
        'registration_date': row[3]
    }

# Parse audio guide record

def parse_audio_guide(row):
    return {
        'guide_id': int(row[0]),
        'exhibit_number': int(row[1]),
        'title': row[2],
        'language': row[3],
        'duration': int(row[4]),
        'script': row[5],
        'narrator': row[6],
        'created_by': row[7]
    }

# ROUTE 1: Root redirect
@app.route('/', methods=['GET'])
def root_redirect():
    return redirect(url_for('dashboard'))

# ROUTE 2: Dashboard page
@app.route('/dashboard', methods=['GET'])
def dashboard():
    exhibition_rows = read_pipe_delimited_file('exhibitions.txt', 9)
    exhibitions = [parse_exhibition(row) for row in exhibition_rows]
    total_exhibitions = len(exhibitions)
    today_str = datetime.now().strftime('%Y-%m-%d')
    active_exhibitions = 0
    for exh in exhibitions:
        if exh['start_date'] <= today_str <= exh['end_date']:
            active_exhibitions += 1
    return render_template('dashboard.html', total_exhibitions=total_exhibitions, active_exhibitions=active_exhibitions)

# ROUTE 3: Artifact catalog page
@app.route('/artifacts', methods=['GET', 'POST'])
def artifact_catalog():
    artifacts_rows = read_pipe_delimited_file('artifacts.txt', 9)
    artifacts = [parse_artifact(row) for row in artifacts_rows]
    search_query = ''
    filter_applied = False

    if request.method == 'POST':
        search_query = request.form.get('search_artifact', '').strip()

    if search_query:
        filter_applied = True
        search_lower = search_query.lower()
        artifacts = [a for a in artifacts if
                     (search_lower in a['artifact_name'].lower() or
                      search_lower in a['period'].lower() or
                      search_lower in a['origin'].lower() or
                      search_lower in a['description'].lower())]

    return render_template('artifact_catalog.html', artifacts=artifacts, search_query=search_query, filter_applied=filter_applied)

# ROUTE 4: Exhibitions page
@app.route('/exhibitions', methods=['GET', 'POST'])
def exhibitions():
    exhibition_rows = read_pipe_delimited_file('exhibitions.txt', 9)
    exhibitions_list = [parse_exhibition(row) for row in exhibition_rows]
    filter_type = ''

    if request.method == 'POST':
        filter_type = request.form.get('filter_type', '').strip()

    if filter_type and filter_type in ('Permanent', 'Temporary', 'Virtual'):
        exhibitions_list = [e for e in exhibitions_list if e['exhibition_type'] == filter_type]

    return render_template('exhibitions.html', exhibitions=exhibitions_list, filter_type=filter_type)

# ROUTE 5: Exhibition details page
@app.route('/exhibitions/<int:exhibition_id>', methods=['GET'])
def exhibition_details(exhibition_id):
    exhibition_rows = read_pipe_delimited_file('exhibitions.txt', 9)
    exhibitions_list = [parse_exhibition(row) for row in exhibition_rows]
    exhibition = next((e for e in exhibitions_list if e['exhibition_id'] == exhibition_id), None)
    if exhibition is None:
        # Exhibition not found, redirect to exhibitions page
        return redirect(url_for('exhibitions'))

    artifacts_rows = read_pipe_delimited_file('artifacts.txt', 9)
    artifacts_list = [parse_artifact(row) for row in artifacts_rows]
    linked_artifacts = [a for a in artifacts_list if a['exhibition_id'] == exhibition_id]

    return render_template('exhibition_details.html', exhibition=exhibition, artifacts=linked_artifacts)

# ROUTE 6: Visitor tickets page
@app.route('/tickets', methods=['GET', 'POST'])
def visitor_tickets():
    tickets_rows = read_pipe_delimited_file('tickets.txt', 10)
    user_tickets = [parse_ticket(row) for row in tickets_rows if row[1] == CURRENT_USER]
    purchase_success = None

    if request.method == 'POST':
        # Extract form data
        ticket_type = request.form.get('ticket_type', '').strip()
        visit_date = request.form.get('visit_date', '').strip()
        visit_time = request.form.get('visit_time', '').strip()
        number_of_tickets_str = request.form.get('number_of_tickets', '').strip()
        visitor_name = request.form.get('visitor_name', '').strip()
        visitor_email = request.form.get('visitor_email', '').strip()

        # Validate required fields
        if not (ticket_type and visit_date and visit_time and number_of_tickets_str and visitor_name and visitor_email):
            purchase_success = False
        else:
            try:
                number_of_tickets = int(number_of_tickets_str)
                if number_of_tickets <= 0:
                    purchase_success = False
                else:
                    # Generate new ticket_id
                    max_ticket_id = max([t['ticket_id'] for t in user_tickets] + [0])
                    new_ticket_id = max_ticket_id + 1
                    # Set price based on ticket type (assumed example prices)
                    price_table = {
                        'Standard': 15,
                        'Student': 10,
                        'Senior': 12,
                        'Family': 25,
                        'VIP': 50
                    }
                    price = price_table.get(ticket_type, 15) * number_of_tickets
                    purchase_date = datetime.now().strftime('%Y-%m-%d')
                    new_ticket = [new_ticket_id, CURRENT_USER, ticket_type, visit_date, visit_time, number_of_tickets, price, visitor_name, visitor_email, purchase_date]
                    # Append new ticket to file
                    all_tickets_rows = read_pipe_delimited_file('tickets.txt', 10)
                    all_tickets_records = all_tickets_rows
                    all_tickets_records.append([str(field) for field in new_ticket])
                    # Write back
                    if write_pipe_delimited_file('tickets.txt', all_tickets_records):
                        purchase_success = True
                        # Update user_tickets list
                        user_tickets.append(parse_ticket([str(f) for f in new_ticket]))
                    else:
                        purchase_success = False
            except Exception:
                purchase_success = False

    return render_template('visitor_tickets.html', user_tickets=user_tickets, purchase_success=purchase_success)

# ROUTE 7: Virtual Events page
@app.route('/events', methods=['GET', 'POST'])
def virtual_events():
    events_rows = read_pipe_delimited_file('events.txt', 9)
    all_events = [parse_event(row) for row in events_rows]
    registrations_rows = read_pipe_delimited_file('event_registrations.txt', 4)
    all_registrations = [parse_registration(row) for row in registrations_rows]

    user_registrations = [r for r in all_registrations if r['username'] == CURRENT_USER]

    if request.method == 'POST':
        action = request.form.get('action', '').strip()
        if action == 'register':
            event_id_str = request.form.get('event_id', '').strip()
            try:
                event_id = int(event_id_str)
                # Check if already registered
                already_registered = any(r['event_id'] == event_id and r['username'] == CURRENT_USER for r in all_registrations)
                if not already_registered:
                    new_reg_id = max([r['registration_id'] for r in all_registrations] + [0]) + 1
                    registration_date = datetime.now().strftime('%Y-%m-%d')
                    new_registration = [new_reg_id, event_id, CURRENT_USER, registration_date]
                    all_registrations.append([str(f) for f in new_registration])
                    # Save back
                    write_pipe_delimited_file('event_registrations.txt', all_registrations)
                    # Refresh user_registrations
                    user_registrations = [r for r in all_registrations if r['username'] == CURRENT_USER]
            except Exception:
                pass
        elif action == 'cancel':
            registration_id_str = request.form.get('registration_id', '').strip()
            try:
                registration_id = int(registration_id_str)
                # Remove registration matching ID and current user
                all_registrations = [r for r in all_registrations if not (r['registration_id'] == registration_id and r['username'] == CURRENT_USER)]
                # Save back
                write_pipe_delimited_file('event_registrations.txt', all_registrations)
                # Refresh user_registrations
                user_registrations = [r for r in all_registrations if r['username'] == CURRENT_USER]
            except Exception:
                pass

    return render_template('virtual_events.html', events=all_events, user_registrations=user_registrations)

# ROUTE 8: Audio guides page
@app.route('/audioguides', methods=['GET', 'POST'])
def audio_guides():
    audio_guides_rows = read_pipe_delimited_file('audioguides.txt', 8)
    audio_guides_list = [parse_audio_guide(row) for row in audio_guides_rows]
    language_filter = ''

    if request.method == 'POST':
        language_filter = request.form.get('language_filter', '').strip()

    if language_filter and language_filter in ("English", "Spanish", "French"):
        audio_guides_list = [g for g in audio_guides_list if g['language'] == language_filter]

    return render_template('audio_guides.html', audio_guides=audio_guides_list, language_filter=language_filter)


if __name__ == "__main__":
    app.run(port=5000, debug=True)
