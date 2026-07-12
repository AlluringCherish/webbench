from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

# Helper methods to load and save data from pipe-delimited files
DATA_DIR = 'data'


# Utility to read generic pipe-delimited file into list of dicts given fields
# Returns list of dicts
# No header in file
# If file does not exist, returns empty list
# fields: list of field names
# converter: optional dict of field_name: conversion function

def read_data_file(filename, fields, converter=None):
    path = os.path.join(DATA_DIR, filename)
    entries = []
    if converter is None:
        converter = {}
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != len(fields):
                    continue  # skip malformed line
                entry = {}
                for i, field in enumerate(fields):
                    value = parts[i]
                    if field in converter:
                        try:
                            value = converter[field](value)
                        except Exception:
                            value = None
                    entry[field] = value
                entries.append(entry)
    except FileNotFoundError:
        # Return empty list if file not found
        pass
    except IOError:
        pass
    return entries


# Utility to save list of dicts to pipe-delimited file
# Overwrites existing file
# entries: list of dicts
# fields: list of field names in order
# All values are converted to string

def save_data_file(filename, entries, fields):
    path = os.path.join(DATA_DIR, filename)
    with open(path, 'w', encoding='utf-8') as f:
        for entry in entries:
            line = '|'.join(str(entry.get(field, '')) for field in fields)
            f.write(line + '\n')


# Data schema field lists
users_fields = ['username']
galleries_fields = ['gallery_id', 'gallery_name', 'floor', 'capacity', 'theme', 'status']
exhibitions_fields = ['exhibition_id', 'title', 'description', 'gallery_id', 'exhibition_type', 'start_date', 'end_date', 'curator_name', 'created_by']
artifacts_fields = ['artifact_id', 'artifact_name', 'period', 'origin', 'description', 'exhibition_id', 'storage_location', 'acquisition_date', 'added_by']
audioguides_fields = ['guide_id', 'exhibit_number', 'title', 'language', 'duration', 'script', 'narrator', 'created_by']
tickets_fields = ['ticket_id', 'username', 'ticket_type', 'visit_date', 'visit_time', 'number_of_tickets', 'price', 'visitor_name', 'visitor_email', 'purchase_date']
events_fields = ['event_id', 'title', 'date', 'time', 'event_type', 'speaker', 'capacity', 'description', 'created_by']
event_registrations_fields = ['registration_id', 'event_id', 'username', 'registration_date']
collection_logs_fields = ['log_id', 'artifact_id', 'activity_type', 'date', 'notes', 'condition', 'curator']

# Converters for field types
# For integer fields, convert to int
# For date fields, keep as string (no date operations needed)
# For fields treated as int, convert

exhibitions_converter = {
    'exhibition_id': int,
    'gallery_id': int
}

artifacts_converter = {
    'artifact_id': int,
    'exhibition_id': int
}

audioguides_converter = {
    'guide_id': int,
    'exhibit_number': int,
    'duration': int
}

tickets_converter = {
    'ticket_id': int,
    'number_of_tickets': int,
    'price': float
}

events_converter = {
    'event_id': int,
    'capacity': int
}

event_registrations_converter = {
    'registration_id': int,
    'event_id': int
}

collection_logs_converter = {
    'log_id': int,
    'artifact_id': int
}

galleries_converter = {
    'gallery_id': int,
    'floor': int,
    'capacity': int
}

# Helper: Read all exhibitions

def load_exhibitions():
    return read_data_file('exhibitions.txt', exhibitions_fields, exhibitions_converter)

# Helper: Read all artifacts

def load_artifacts():
    return read_data_file('artifacts.txt', artifacts_fields, artifacts_converter)

# Helper: Read all tickets

def load_tickets():
    return read_data_file('tickets.txt', tickets_fields, tickets_converter)

# Helper: save tickets

def save_tickets(tickets):
    save_data_file('tickets.txt', tickets, tickets_fields)

# Helper: Read all events

def load_events():
    return read_data_file('events.txt', events_fields, events_converter)

# Helper: Read all registrations

def load_event_registrations():
    return read_data_file('event_registrations.txt', event_registrations_fields, event_registrations_converter)

# Helper: Save event registrations

def save_event_registrations(registrations):
    save_data_file('event_registrations.txt', registrations, event_registrations_fields)

# Helper: Read all audio guides

def load_audio_guides():
    return read_data_file('audioguides.txt', audioguides_fields, audioguides_converter)

# Helper: Read all users

def load_users():
    return [u['username'] for u in read_data_file('users.txt', users_fields)]

# Helper: Read all galleries

def load_galleries():
    return read_data_file('galleries.txt', galleries_fields, galleries_converter)

# Root redirect route
@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard_page'))

# Dashboard route
@app.route('/dashboard')
def dashboard_page():
    exhibitions = load_exhibitions()
    total_exhibitions = len(exhibitions)
    # Count active exhibitions: where current date is between start_date and end_date
    today = datetime.now().date()
    active_exhibitions = 0
    for ex in exhibitions:
        try:
            start = datetime.strptime(ex['start_date'], '%Y-%m-%d').date()
            end = datetime.strptime(ex['end_date'], '%Y-%m-%d').date()
            if start <= today <= end:
                active_exhibitions += 1
        except Exception:
            continue

    return render_template('dashboard.html', total_exhibitions=total_exhibitions, active_exhibitions=active_exhibitions)

# Artifacts catalog route with GET and POST
@app.route('/artifacts', methods=['GET', 'POST'])
def artifact_catalog():
    artifacts = load_artifacts()
    filter_query = ''
    if request.method == 'POST':
        filter_query = request.form.get('filter_query', '').strip()

    if filter_query:
        filtered = []
        lower_filter = filter_query.lower()
        for artifact in artifacts:
            # Filter on artifact_name or period or origin or description case insensitive match
            if (lower_filter in artifact['artifact_name'].lower()
                or lower_filter in artifact['period'].lower()
                or lower_filter in artifact['origin'].lower()
                or lower_filter in artifact['description'].lower()):
                filtered.append(artifact)
        artifacts = filtered

    return render_template('artifact_catalog.html', artifacts=artifacts, filter_query=filter_query)

# Exhibitions list route GET/POST
@app.route('/exhibitions', methods=['GET', 'POST'])
def exhibitions_list():
    exhibitions = load_exhibitions()
    filter_type = ''
    if request.method == 'POST':
        filter_type = request.form.get('filter_type', '').strip()

    if filter_type:
        exhibitions = [ex for ex in exhibitions if ex['exhibition_type'].lower() == filter_type.lower()]
    return render_template('exhibitions.html', exhibitions=exhibitions, filter_type=filter_type)

# Exhibition details route GET
@app.route('/exhibition/<int:exhibition_id>')
def exhibition_details(exhibition_id):
    exhibitions = load_exhibitions()
    exhibition = None
    for ex in exhibitions:
        if ex['exhibition_id'] == exhibition_id:
            exhibition = ex
            break
    if not exhibition:
        # Redirect to exhibitions list if exhibition not found
        return redirect(url_for('exhibitions_list'))

    artifacts = load_artifacts()
    exhibition_artifacts = [a for a in artifacts if a['exhibition_id'] == exhibition_id]

    return render_template('exhibition_details.html', exhibition=exhibition, artifacts=exhibition_artifacts)

# Visitor tickets route GET and POST
@app.route('/tickets', methods=['GET', 'POST'])
def visitor_tickets():
    # Simulated current user for tickets example; user context is not described, assume visitor_mary
    CURRENT_USER = 'visitor_mary'

    tickets = load_tickets()
    user_tickets = [t for t in tickets if t['username'] == CURRENT_USER]
    ticket_types = ['Standard', 'Student', 'Senior', 'Family', 'VIP']

    if request.method == 'POST':
        ticket_type = request.form.get('ticket_type', '').strip()
        number_of_tickets = request.form.get('number_of_tickets', '').strip()
        visitor_name = request.form.get('visitor_name', '').strip() if 'visitor_name' in request.form else ''
        visitor_email = request.form.get('visitor_email', '').strip() if 'visitor_email' in request.form else ''
        # Validate inputs
        if ticket_type in ticket_types:
            try:
                number_of_tickets_i = int(number_of_tickets)
                if number_of_tickets_i > 0 and visitor_name and visitor_email:
                    # Create new ticket entry
                    new_ticket_id = 1
                    if tickets:
                        new_ticket_id = max(t['ticket_id'] for t in tickets) + 1
                    # For simplicity set visit_date to today's date string and time to '10:00 AM'
                    visit_date = datetime.now().date().strftime('%Y-%m-%d')
                    visit_time = '10:00 AM'
                    price_map = {
                        'Standard': 15,
                        'Student': 10,
                        'Senior': 12,
                        'Family': 40,
                        'VIP': 50
                    }
                    price = price_map.get(ticket_type, 15) * number_of_tickets_i
                    purchase_date = datetime.now().date().strftime('%Y-%m-%d')
                    new_ticket = {
                        'ticket_id': new_ticket_id,
                        'username': CURRENT_USER,
                        'ticket_type': ticket_type,
                        'visit_date': visit_date,
                        'visit_time': visit_time,
                        'number_of_tickets': number_of_tickets_i,
                        'price': price,
                        'visitor_name': visitor_name,
                        'visitor_email': visitor_email,
                        'purchase_date': purchase_date
                    }
                    tickets.append(new_ticket)
                    save_tickets(tickets)
                    return redirect(url_for('visitor_tickets'))
            except ValueError:
                pass

    return render_template('visitor_tickets.html', tickets=user_tickets, ticket_types=ticket_types)

# Virtual events route GET and POST
@app.route('/events', methods=['GET', 'POST'])
def virtual_events():
    # Simulated current user
    CURRENT_USER = 'visitor_mary'

    events = load_events()
    registrations = load_event_registrations()

    # Filter user's registrations
    user_registrations = [r for r in registrations if r['username'] == CURRENT_USER]

    if request.method == 'POST':
        # Determine action by presence of form keys
        # register_event_id or cancel_registration_id
        register_event_id = request.form.get('register_event_id', '').strip()
        cancel_registration_id = request.form.get('cancel_registration_id', '').strip()

        if register_event_id.isdigit():
            event_id = int(register_event_id)
            # Check if already registered
            already_registered = any(
                (r['event_id'] == event_id and r['username'] == CURRENT_USER) for r in registrations)
            if not already_registered:
                new_reg_id = 1
                if registrations:
                    new_reg_id = max(r['registration_id'] for r in registrations) + 1
                registration_date = datetime.now().date().strftime('%Y-%m-%d')
                new_registration = {
                    'registration_id': new_reg_id,
                    'event_id': event_id,
                    'username': CURRENT_USER,
                    'registration_date': registration_date
                }
                registrations.append(new_registration)
                save_event_registrations(registrations)

        elif cancel_registration_id.isdigit():
            registration_id = int(cancel_registration_id)
            # Remove user registration with id
            registrations = [r for r in registrations if not (r['registration_id'] == registration_id and r['username'] == CURRENT_USER)]
            save_event_registrations(registrations)

        return redirect(url_for('virtual_events'))

    return render_template('virtual_events.html', events=events, registrations=user_registrations)

# Audio guides route GET and POST
@app.route('/audio-guides', methods=['GET', 'POST'])
def audio_guides():
    audio_guides = load_audio_guides()
    filter_language = ''

    if request.method == 'POST':
        filter_language = request.form.get('filter_language', '').strip()

        # Check if this is a play guide request
        play_guide_id = request.form.get('play_guide_id', '').strip()
        if play_guide_id.isdigit():
            # In functional terms, no data state change needed here
            # The front-end presumably handles playback
            pass

    if filter_language:
        audio_guides = [ag for ag in audio_guides if ag['language'].lower() == filter_language.lower()]

    return render_template('audio_guides.html', audio_guides=audio_guides, filter_language=filter_language)


if __name__ == '__main__':
    app.run(port=5000, debug=True)
