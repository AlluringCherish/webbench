from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a secure secret key

DATA_DIR = 'data'

# --- Helper Functions for File Operations and Data Loading ---

def get_file_path(filename):
    return os.path.join(DATA_DIR, filename)

# Generic function to read pipe-delimited files with headers
# Returns list of dicts

def read_pipe_delimited_file(filename, fieldnames):
    path = get_file_path(filename)
    data = []
    if not os.path.exists(path):
        return data
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != len(fieldnames):
                continue  # skip malformed lines
            entry = {fieldnames[i]: parts[i] for i in range(len(fieldnames))}
            data.append(entry)
    return data

# Writing entire list of dicts back to file

def write_pipe_delimited_file(filename, fieldnames, data):
    path = get_file_path(filename)
    with open(path, 'w', encoding='utf-8') as f:
        for entry in data:
            line = '|'.join(str(entry[field]) for field in fieldnames)
            f.write(line + '\n')

# Append a single dict entry to file

def append_to_pipe_delimited_file(filename, fieldnames, entry):
    path = get_file_path(filename)
    with open(path, 'a', encoding='utf-8') as f:
        line = '|'.join(str(entry[field]) for field in fieldnames)
        f.write(line + '\n')

# User Authentication Check

def is_authenticated():
    username = session.get('username')
    if not username:
        return False
    users = read_pipe_delimited_file('users.txt', ['username'])
    return any(u['username'] == username for u in users)

# --- Data Schema Fieldnames ---
USERS_FIELDS = ['username']
GALLERIES_FIELDS = ['gallery_id', 'gallery_name', 'floor', 'capacity', 'theme', 'status']
EXHIBITIONS_FIELDS = ['exhibition_id', 'title', 'description', 'gallery_id', 'exhibition_type', 'start_date', 'end_date', 'curator_name', 'created_by']
ARTIFACTS_FIELDS = ['artifact_id', 'artifact_name', 'period', 'origin', 'description', 'exhibition_id', 'storage_location', 'acquisition_date', 'added_by']
AUDIOGUIDES_FIELDS = ['guide_id', 'exhibit_number', 'title', 'language', 'duration', 'script', 'narrator', 'created_by']
TICKETS_FIELDS = ['ticket_id', 'username', 'ticket_type', 'visit_date', 'visit_time', 'number_of_tickets', 'price', 'visitor_name', 'visitor_email', 'purchase_date']
EVENTS_FIELDS = ['event_id', 'title', 'date', 'time', 'event_type', 'speaker', 'capacity', 'description', 'created_by']
EVENT_REGISTRATIONS_FIELDS = ['registration_id', 'event_id', 'username', 'registration_date']
COLLECTION_LOGS_FIELDS = ['log_id', 'artifact_id', 'activity_type', 'date', 'notes', 'condition', 'curator']

# --- Utils ---

def parse_int(value, default=0):
    try:
        return int(value)
    except:
        return default

def parse_float(value, default=0.0):
    try:
        return float(value)
    except:
        return default

def parse_date(value, default=None):
    try:
        return datetime.datetime.strptime(value, '%Y-%m-%d').date()
    except:
        return default

# Get current date

def current_date():
    return datetime.date.today()

# Get exhibitions active on current date or any given date

def get_active_exhibitions(exhibitions, on_date=None):
    if on_date is None:
        on_date = current_date()
    active = []
    for ex in exhibitions:
        start = parse_date(ex['start_date'])
        end = parse_date(ex['end_date'])
        if start and end and start <= on_date <= end:
            active.append(ex)
    return active

# --- Route Implementations ---

# 1. Dashboard Page
@app.route('/')
def dashboard():
    exhibitions = read_pipe_delimited_file('exhibitions.txt', EXHIBITIONS_FIELDS)
    artifacts = read_pipe_delimited_file('artifacts.txt', ARTIFACTS_FIELDS)

    total_exhibitions = len(exhibitions)
    active_exhibitions = len(get_active_exhibitions(exhibitions))
    artifact_count = len(artifacts)
    return render_template('dashboard.html', total_exhibitions=total_exhibitions, active_exhibitions=active_exhibitions, artifact_count=artifact_count)

# 2. Artifact Catalog Page
@app.route('/artifacts')
def artifact_catalog():
    search = request.args.get('search', '').strip().lower()
    artifacts = read_pipe_delimited_file('artifacts.txt', ARTIFACTS_FIELDS)
    exhibitions = read_pipe_delimited_file('exhibitions.txt', EXHIBITIONS_FIELDS)
    exhibition_map = {ex['exhibition_id']: ex['title'] for ex in exhibitions}

    filtered_artifacts = []
    for artifact in artifacts:
        if search:
            if search in artifact['artifact_name'].lower() or search == artifact['artifact_id'].lower():
                filtered_artifacts.append(artifact)
        else:
            filtered_artifacts.append(artifact)

    # Add exhibition names to artifacts for template
    for art in filtered_artifacts:
        art['exhibition_name'] = exhibition_map.get(art['exhibition_id'], 'Unknown')

    return render_template('artifact_catalog.html', artifacts=filtered_artifacts, search=search)

# 3. Exhibitions Page
@app.route('/exhibitions')
def exhibitions_page():
    filter_type = request.args.get('type', '').strip()
    exhibitions = read_pipe_delimited_file('exhibitions.txt', EXHIBITIONS_FIELDS)
    galleries = read_pipe_delimited_file('galleries.txt', GALLERIES_FIELDS)
    gallery_map = {g['gallery_id']: g['gallery_name'] for g in galleries}

    filtered_exhibitions = []
    for ex in exhibitions:
        if filter_type:
            if ex['exhibition_type'].lower() != filter_type.lower():
                continue
        ex['gallery_name'] = gallery_map.get(ex['gallery_id'], 'Unknown')
        filtered_exhibitions.append(ex)

    return render_template('exhibitions.html', exhibitions=filtered_exhibitions, filter_type=filter_type)

# 4. Exhibition Details Page
@app.route('/exhibitions/<exhibition_id>')
def exhibition_details(exhibition_id):
    exhibitions = read_pipe_delimited_file('exhibitions.txt', EXHIBITIONS_FIELDS)
    artifacts = read_pipe_delimited_file('artifacts.txt', ARTIFACTS_FIELDS)

    exhibition = None
    for ex in exhibitions:
        if ex['exhibition_id'] == str(exhibition_id):
            exhibition = ex
            break
    if exhibition is None:
        return "Exhibition not found", 404

    # Get artifacts for this exhibition
    exhibition_artifacts = [a for a in artifacts if a['exhibition_id'] == str(exhibition_id)]

    return render_template('exhibition_details.html', exhibition=exhibition, artifacts=exhibition_artifacts)

# 5. Visitor Tickets Page
@app.route('/tickets', methods=['GET', 'POST'])
def tickets():
    if not is_authenticated():
        flash('You must be logged in to view tickets.')
        return redirect(url_for('dashboard'))
    username = session.get('username')

    ticket_types = {
        'Standard': 20.0,
        'Student': 10.0,
        'Senior': 15.0,
        'Family': 40.0,
        'VIP': 100.0
    }

    if request.method == 'POST':
        ticket_type = request.form.get('ticket_type')
        number_of_tickets = request.form.get('number_of_tickets')
        visit_date = request.form.get('visit_date')
        visit_time = request.form.get('visit_time')
        visitor_name = request.form.get('visitor_name')
        visitor_email = request.form.get('visitor_email')

        # Validate inputs
        if ticket_type not in ticket_types:
            flash('Invalid ticket type.')
            return redirect(url_for('tickets'))
        try:
            number_of_tickets = int(number_of_tickets)
            if number_of_tickets <= 0:
                raise ValueError
        except:
            flash('Number of tickets must be a positive integer.')
            return redirect(url_for('tickets'))

        visit_date_obj = parse_date(visit_date)
        if not visit_date_obj:
            flash('Invalid visit date format.')
            return redirect(url_for('tickets'))

        if not visit_time:
            flash('Visit time required.')
            return redirect(url_for('tickets'))

        if not visitor_name or not visitor_email:
            flash('Visitor name and email are required.')
            return redirect(url_for('tickets'))

        tickets_data = read_pipe_delimited_file('tickets.txt', TICKETS_FIELDS)

        # Generate new unique ticket_id
        max_ticket_id = 0
        for t in tickets_data:
            tid = parse_int(t['ticket_id'])
            if tid > max_ticket_id:
                max_ticket_id = tid
        new_ticket_id = max_ticket_id + 1

        price = ticket_types[ticket_type] * number_of_tickets
        purchase_date_str = current_date().strftime('%Y-%m-%d')

        new_ticket = {
            'ticket_id': str(new_ticket_id),
            'username': username,
            'ticket_type': ticket_type,
            'visit_date': visit_date,
            'visit_time': visit_time,
            'number_of_tickets': str(number_of_tickets),
            'price': f'{price:.2f}',
            'visitor_name': visitor_name,
            'visitor_email': visitor_email,
            'purchase_date': purchase_date_str
        }

        append_to_pipe_delimited_file('tickets.txt', TICKETS_FIELDS, new_ticket)
        flash('Ticket purchase successful.')
        return redirect(url_for('tickets'))

    else:
        # GET method
        tickets_data = read_pipe_delimited_file('tickets.txt', TICKETS_FIELDS)
        user_tickets = [t for t in tickets_data if t['username'] == username]
        return render_template('visitor_tickets.html', tickets=user_tickets, ticket_types=ticket_types)

# 6. Virtual Events Page
@app.route('/events', methods=['GET', 'POST'])
def virtual_events():
    if not is_authenticated():
        flash('You must be logged in to view events.')
        return redirect(url_for('dashboard'))
    username = session.get('username')

    events = read_pipe_delimited_file('events.txt', EVENTS_FIELDS)
    registrations = read_pipe_delimited_file('event_registrations.txt', EVENT_REGISTRATIONS_FIELDS)

    if request.method == 'POST':
        action = request.form.get('action')
        event_id = request.form.get('event_id')

        if action not in ['register', 'cancel']:
            flash('Invalid action.')
            return redirect(url_for('virtual_events'))

        # Check event exists
        event = next((e for e in events if e['event_id'] == str(event_id)), None)
        if not event:
            flash('Event not found.')
            return redirect(url_for('virtual_events'))

        # Count current registrations for event
        current_count = sum(1 for r in registrations if r['event_id'] == event_id)
        user_registered = any(r['event_id'] == event_id and r['username'] == username for r in registrations)

        if action == 'register':
            # Enforce capacity
            capacity = parse_int(event['capacity'])
            if user_registered:
                flash('You are already registered for this event.')
                return redirect(url_for('virtual_events'))
            if current_count >= capacity:
                flash('Event is full.')
                return redirect(url_for('virtual_events'))
            # Generate new registration id
            max_reg_id = 0
            for r in registrations:
                rid = parse_int(r['registration_id'])
                if rid > max_reg_id:
                    max_reg_id = rid
            new_reg_id = max_reg_id + 1
            reg_date = current_date().strftime('%Y-%m-%d')
            new_registration = {
                'registration_id': str(new_reg_id),
                'event_id': str(event_id),
                'username': username,
                'registration_date': reg_date
            }
            append_to_pipe_delimited_file('event_registrations.txt', EVENT_REGISTRATIONS_FIELDS, new_registration)
            flash('Registration successful.')
            return redirect(url_for('virtual_events'))

        elif action == 'cancel':
            if not user_registered:
                flash('You are not registered for this event.')
                return redirect(url_for('virtual_events'))
            # Remove registration
            registrations = [r for r in registrations if not (r['event_id'] == event_id and r['username'] == username)]
            write_pipe_delimited_file('event_registrations.txt', EVENT_REGISTRATIONS_FIELDS, registrations)
            flash('Registration cancelled.')
            return redirect(url_for('virtual_events'))

    else:
        # GET
        # Prepare registration status map
        user_registration_ids = set(r['registration_id'] for r in registrations if r['username'] == username)
        reg_events_ids = set(r['event_id'] for r in registrations if r['username'] == username)

        # Build events list with registration status
        event_data = []
        for e in events:
            current_count = sum(1 for r in registrations if r['event_id'] == e['event_id'])
            is_registered = e['event_id'] in reg_events_ids
            event_data.append({
                'event': e,
                'registered': is_registered,
                'current_count': current_count
            })
        return render_template('virtual_events.html', events=event_data)

# 7. Audio Guides Page
@app.route('/audioguides')
def audio_guides():
    language_filter = request.args.get('language', '').strip()
    audioguides = read_pipe_delimited_file('audioguides.txt', AUDIOGUIDES_FIELDS)

    filtered_guides = []
    for guide in audioguides:
        if language_filter:
            if guide['language'].lower() == language_filter.lower():
                filtered_guides.append(guide)
        else:
            filtered_guides.append(guide)

    return render_template('audio_guides.html', audioguides=filtered_guides, language_filter=language_filter)

# --- Minimal User Login Handling (for session) ---

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        users = read_pipe_delimited_file('users.txt', USERS_FIELDS)
        if any(u['username'] == username for u in users):
            session['username'] = username
            flash('Logged in successfully.')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username.')
            return redirect(url_for('login'))
    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Logged out.')
    return redirect(url_for('dashboard'))


if __name__ == '__main__':
    # Create data folder if not exists
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    app.run(debug=True)
