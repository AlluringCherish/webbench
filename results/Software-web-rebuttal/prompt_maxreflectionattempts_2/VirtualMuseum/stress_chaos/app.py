from flask import Flask, redirect, url_for, render_template, request, abort
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Utility to read simple line-based file (e.g., users.txt)
def read_lines(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip()]
    except IOError:
        return []

# Utility to parse pipe-delimited file with expected field count

def parse_pipe_file(path, expected_fields):
    rows = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != expected_fields:
                    continue
                rows.append(parts)
    except IOError:
        pass
    return rows

# Load functions for all data files

def load_users():
    return read_lines(os.path.join(DATA_DIR, 'users.txt'))

def load_galleries():
    rows = parse_pipe_file(os.path.join(DATA_DIR, 'galleries.txt'), 6)
    galleries = []
    for r in rows:
        galleries.append({
            'gallery_id': int(r[0]),
            'gallery_name': r[1],
            'floor': r[2],
            'capacity': int(r[3]),
            'theme': r[4],
            'status': r[5]
        })
    return galleries

def load_exhibitions():
    rows = parse_pipe_file(os.path.join(DATA_DIR, 'exhibitions.txt'), 9)
    exhibitions = []
    for r in rows:
        exhibitions.append({
            'exhibition_id': int(r[0]),
            'title': r[1],
            'description': r[2],
            'gallery_id': int(r[3]),
            'exhibition_type': r[4],
            'start_date': r[5],
            'end_date': r[6],
            'curator_name': r[7],
            'created_by': r[8]
        })
    return exhibitions

def load_artifacts():
    rows = parse_pipe_file(os.path.join(DATA_DIR, 'artifacts.txt'), 9)
    artifacts = []
    for r in rows:
        artifacts.append({
            'artifact_id': int(r[0]),
            'artifact_name': r[1],
            'period': r[2],
            'origin': r[3],
            'description': r[4],
            'exhibition_id': int(r[5]),
            'storage_location': r[6],
            'acquisition_date': r[7],
            'added_by': r[8]
        })
    return artifacts

def load_audioguides():
    rows = parse_pipe_file(os.path.join(DATA_DIR, 'audioguides.txt'), 8)
    guides = []
    for r in rows:
        guides.append({
            'guide_id': int(r[0]),
            'exhibit_number': r[1],
            'title': r[2],
            'language': r[3],
            'duration': r[4],
            'script': r[5],
            'narrator': r[6],
            'created_by': r[7]
        })
    return guides

def load_tickets():
    rows = parse_pipe_file(os.path.join(DATA_DIR, 'tickets.txt'), 10)
    tickets = []
    for r in rows:
        tickets.append({
            'ticket_id': int(r[0]),
            'username': r[1],
            'ticket_type': r[2],
            'visit_date': r[3],
            'visit_time': r[4],
            'number_of_tickets': int(r[5]),
            'price': r[6],
            'visitor_name': r[7],
            'visitor_email': r[8],
            'purchase_date': r[9]
        })
    return tickets

def load_events():
    rows = parse_pipe_file(os.path.join(DATA_DIR, 'events.txt'), 9)
    events = []
    for r in rows:
        events.append({
            'event_id': int(r[0]),
            'title': r[1],
            'date': r[2],
            'time': r[3],
            'event_type': r[4],
            'speaker': r[5],
            'capacity': int(r[6]),
            'description': r[7],
            'created_by': r[8]
        })
    return events

def load_registrations():
    rows = parse_pipe_file(os.path.join(DATA_DIR, 'event_registrations.txt'), 4)
    regs = []
    for r in rows:
        regs.append({
            'registration_id': int(r[0]),
            'event_id': int(r[1]),
            'username': r[2],
            'registration_date': r[3]
        })
    return regs

# Save event registrations

def save_registrations(registrations):
    filepath = os.path.join(DATA_DIR, 'event_registrations.txt')
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            for r in registrations:
                line = f"{r['registration_id']}|{r['event_id']}|{r['username']}|{r['registration_date']}\n"
                f.write(line)
    except IOError:
        pass

# Save tickets

def save_tickets(tickets):
    filepath = os.path.join(DATA_DIR, 'tickets.txt')
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            for t in tickets:
                line = f"{t['ticket_id']}|{t['username']}|{t['ticket_type']}|{t['visit_date']}|{t['visit_time']}|{t['number_of_tickets']}|{t['price']}|{t['visitor_name']}|{t['visitor_email']}|{t['purchase_date']}\n"
                f.write(line)
    except IOError:
        pass

# Helpers to get next ids

def next_ticket_id(tickets):
    if not tickets:
        return 1
    return max(t['ticket_id'] for t in tickets) + 1

def next_registration_id(registrations):
    if not registrations:
        return 1
    return max(r['registration_id'] for r in registrations) + 1


@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    exhibitions = load_exhibitions()
    artifacts = load_artifacts()

    today = datetime.now().date()
    total_exhibitions = len(exhibitions)
    active_exhibitions = 0

    for ex in exhibitions:
        try:
            start_date = datetime.strptime(ex['start_date'], '%Y-%m-%d').date()
            end_date = datetime.strptime(ex['end_date'], '%Y-%m-%d').date()
            if start_date <= today <= end_date:
                active_exhibitions += 1
        except Exception:
            pass

    exhibitions_summary = {
        'total_exhibitions': total_exhibitions,
        'active_exhibitions': active_exhibitions
    }

    return render_template('dashboard.html', exhibitions_summary=exhibitions_summary, exhibitions=exhibitions, artifacts=artifacts)

@app.route('/artifact-catalog', methods=['GET', 'POST'])
def artifact_catalog():
    artifacts = load_artifacts()
    search_query = ''
    filters = {}

    if request.method == 'POST':
        search_query = request.form.get('search_query','').strip()
        # Filters: collect keys except search_query
        filters = {k: v for k, v in request.form.items() if k != 'search_query'}

        if search_query:
            artifacts = [a for a in artifacts if search_query.lower() in a['artifact_name'].lower()]
        # No specific filters specified, so ignoring other filters

    return render_template('artifact_catalog.html', artifacts=artifacts, search_query=search_query, filters=filters)

@app.route('/exhibitions', methods=['GET', 'POST'])
def exhibitions():
    exhibition_types = ['Permanent', 'Temporary', 'Virtual']
    exhibitions = load_exhibitions()
    selected_exhibition_type = ''

    if request.method == 'POST':
        selected_exhibition_type = request.form.get('selected_exhibition_type','')
        if selected_exhibition_type and selected_exhibition_type in exhibition_types:
            exhibitions = [e for e in exhibitions if e['exhibition_type'] == selected_exhibition_type]

    return render_template('exhibitions.html', exhibitions=exhibitions, exhibition_types=exhibition_types, selected_exhibition_type=selected_exhibition_type)

@app.route('/exhibition/<int:exhibition_id>')
def exhibition_details(exhibition_id):
    exhibitions = load_exhibitions()
    exhibition = next((ex for ex in exhibitions if ex['exhibition_id'] == exhibition_id), None)
    if exhibition is None:
        abort(404)

    artifacts = load_artifacts()
    exhibition_artifacts = [a for a in artifacts if a['exhibition_id'] == exhibition_id]

    return render_template('exhibition_details.html', exhibition=exhibition, artifacts=exhibition_artifacts)

@app.route('/visitor-tickets', methods=['GET', 'POST'])
def visitor_tickets():
    ticket_types = ['Standard', 'Student', 'Senior', 'Family', 'VIP']
    tickets = load_tickets()
    current_user = 'visitor_mary'  # For demonstration, fixed user
    my_tickets = [t for t in tickets if t['username'] == current_user]

    error_messages = []
    form_data = {}

    if request.method == 'POST':
        ticket_type = request.form.get('ticket_type', '')
        visit_date = request.form.get('visit_date', '')
        visit_time = request.form.get('visit_time', '')
        number_of_tickets_str = request.form.get('number_of_tickets', '0')
        visitor_name = request.form.get('visitor_name', '').strip()
        visitor_email = request.form.get('visitor_email', '').strip()

        form_data = {
            'ticket_type': ticket_type,
            'visit_date': visit_date,
            'visit_time': visit_time,
            'number_of_tickets': number_of_tickets_str,
            'visitor_name': visitor_name,
            'visitor_email': visitor_email
        }

        # Validate
        if ticket_type not in ticket_types:
            error_messages.append('Invalid ticket type selected.')
        if not visit_date:
            error_messages.append('Visit date is required.')
        if not visit_time:
            error_messages.append('Visit time is required.')
        try:
            number_of_tickets = int(number_of_tickets_str)
            if number_of_tickets < 1:
                error_messages.append('Number of tickets must be at least 1.')
        except ValueError:
            error_messages.append('Number of tickets must be an integer.')
        if not visitor_name:
            error_messages.append('Visitor name is required.')
        if not visitor_email:
            error_messages.append('Visitor email is required.')

        if not error_messages:
            new_ticket_id = next_ticket_id(tickets)
            purchase_date = datetime.now().strftime('%Y-%m-%d')

            PRICE_MAP = {'Standard': 30, 'Student': 10, 'Senior': 20, 'Family': 60, 'VIP': 50}
            price_per_ticket = PRICE_MAP.get(ticket_type, 0)
            total_price = price_per_ticket * number_of_tickets

            new_ticket = {
                'ticket_id': new_ticket_id,
                'username': current_user,
                'ticket_type': ticket_type,
                'visit_date': visit_date,
                'visit_time': visit_time,
                'number_of_tickets': number_of_tickets,
                'price': str(total_price),
                'visitor_name': visitor_name,
                'visitor_email': visitor_email,
                'purchase_date': purchase_date
            }

            tickets.append(new_ticket)
            save_tickets(tickets)

            return redirect(url_for('visitor_tickets'))

    return render_template('visitor_tickets.html', ticket_types=ticket_types, my_tickets=my_tickets, error_messages=error_messages, form_data=form_data)

@app.route('/virtual-events', methods=['GET', 'POST'])
def virtual_events():
    events = load_events()
    registrations = load_registrations()
    current_user = 'visitor_mary'  # Fixed for demonstration

    user_registrations = [r for r in registrations if r['username'] == current_user]

    if request.method == 'POST':
        action = request.form.get('action', '')

        if action == 'register':
            event_id_str = request.form.get('event_id', '')
            if event_id_str.isdigit():
                event_id = int(event_id_str)
                if not any(r['event_id'] == event_id and r['username'] == current_user for r in registrations):
                    reg_id = next_registration_id(registrations)
                    reg_date = datetime.now().strftime('%Y-%m-%d')
                    registrations.append({
                        'registration_id': reg_id,
                        'event_id': event_id,
                        'username': current_user,
                        'registration_date': reg_date
                    })
                    save_registrations(registrations)

        elif action == 'cancel':
            reg_id_str = request.form.get('registration_id', '')
            if reg_id_str.isdigit():
                reg_id = int(reg_id_str)
                registrations = [r for r in registrations if not (r['registration_id'] == reg_id and r['username'] == current_user)]
                save_registrations(registrations)

        return redirect(url_for('virtual_events'))

    return render_template('virtual_events.html', events=events, registrations=registrations, user_registrations=user_registrations)

@app.route('/audio-guides', methods=['GET', 'POST'])
def audio_guides():
    languages = ['English', 'Spanish', 'French']
    audio_guides = load_audioguides()
    selected_language = ''

    if request.method == 'POST':
        selected_language = request.form.get('selected_language', '')
        if selected_language in languages:
            audio_guides = [g for g in audio_guides if g['language'] == selected_language]

    return render_template('audio_guides.html', audio_guides=audio_guides, languages=languages, selected_language=selected_language)

if __name__ == '__main__':
    app.run(debug=True)
