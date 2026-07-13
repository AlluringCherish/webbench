from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)
DATA_PATH = 'data'

# Utility functions for file operations

def read_pipe_delimited_file(filename, fieldnames):
    """Read a pipe-delimited file into a list of dicts with specified fieldnames."""
    filepath = os.path.join(DATA_PATH, filename)
    entries = []
    if not os.path.exists(filepath):
        return entries
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) < len(fieldnames):
                continue  # Skip malformed line
            entry = dict(zip(fieldnames, parts))
            entries.append(entry)
    return entries


def write_pipe_delimited_file(filename, fieldnames, entries):
    """Write a list of dicts to a pipe-delimited file with specified fieldnames."""
    filepath = os.path.join(DATA_PATH, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        for entry in entries:
            line = '|'.join(str(entry.get(field, '')) for field in fieldnames)
            f.write(line + '\n')


def read_users():
    filepath = os.path.join(DATA_PATH, 'users.txt')
    if not os.path.exists(filepath):
        return []
    with open(filepath, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]


def read_galleries():
    fieldnames = ['gallery_id', 'gallery_name', 'floor', 'capacity', 'theme', 'status']
    return read_pipe_delimited_file('galleries.txt', fieldnames)


def read_exhibitions():
    fieldnames = ['exhibition_id', 'title', 'description', 'gallery_id', 'exhibition_type', 'start_date', 'end_date', 'curator_name', 'created_by']
    return read_pipe_delimited_file('exhibitions.txt', fieldnames)


def read_artifacts():
    fieldnames = ['artifact_id', 'artifact_name', 'period', 'origin', 'description', 'exhibition_id', 'storage_location', 'acquisition_date', 'added_by']
    return read_pipe_delimited_file('artifacts.txt', fieldnames)


def read_audioguides():
    fieldnames = ['guide_id', 'exhibit_number', 'title', 'language', 'duration', 'script', 'narrator', 'created_by']
    return read_pipe_delimited_file('audioguides.txt', fieldnames)


def read_tickets():
    fieldnames = ['ticket_id', 'username', 'ticket_type', 'visit_date', 'visit_time', 'number_of_tickets', 'price', 'visitor_name', 'visitor_email', 'purchase_date']
    return read_pipe_delimited_file('tickets.txt', fieldnames)


def write_tickets(tickets):
    fieldnames = ['ticket_id', 'username', 'ticket_type', 'visit_date', 'visit_time', 'number_of_tickets', 'price', 'visitor_name', 'visitor_email', 'purchase_date']
    write_pipe_delimited_file('tickets.txt', fieldnames, tickets)


def read_events():
    fieldnames = ['event_id', 'title', 'date', 'time', 'event_type', 'speaker', 'capacity', 'description', 'created_by']
    return read_pipe_delimited_file('events.txt', fieldnames)


def read_event_registrations():
    fieldnames = ['registration_id', 'event_id', 'username', 'registration_date']
    return read_pipe_delimited_file('event_registrations.txt', fieldnames)


def write_event_registrations(registrations):
    fieldnames = ['registration_id', 'event_id', 'username', 'registration_date']
    write_pipe_delimited_file('event_registrations.txt', fieldnames, registrations)


def read_collection_logs():
    fieldnames = ['log_id', 'artifact_id', 'activity_type', 'date', 'notes', 'condition', 'curator']
    return read_pipe_delimited_file('collection_logs.txt', fieldnames)


@app.route('/')
def root_redirect():
    """Redirect root to dashboard."""
    return redirect(url_for('dashboard_page'))


@app.route('/dashboard')
def dashboard_page():
    """Render dashboard with exhibition summary."""
    exhibitions = read_exhibitions()
    total_exhibitions = len(exhibitions)
    # Active exhibitions: current date between start and end date inclusive
    today = datetime.today().date()
    active_exhibitions = 0
    for ex in exhibitions:
        try:
            start = datetime.strptime(ex['start_date'], '%Y-%m-%d').date()
            end = datetime.strptime(ex['end_date'], '%Y-%m-%d').date()
            if start <= today <= end:
                active_exhibitions += 1
        except ValueError:
            continue
    exhibition_summary = {'total_exhibitions': total_exhibitions, 'active_exhibitions': active_exhibitions}
    # Render dashboard.html with context
    return render_template('dashboard.html', exhibition_summary=exhibition_summary)


@app.route('/artifact-catalog', methods=['GET', 'POST'])
def artifact_catalog_page():
    """Display artifacts with optional search/filter."""
    artifacts = read_artifacts()
    search_query = ''
    if request.method == 'POST':
        search_query = request.form.get('search_artifact', '').strip()
        if search_query:
            artifacts = [a for a in artifacts if search_query.lower() in a['artifact_name'].lower() or search_query == a['artifact_id']]
    # Render artifact_catalog.html
    return render_template('artifact_catalog.html', artifacts=artifacts, search_query=search_query)


@app.route('/exhibitions', methods=['GET', 'POST'])
def exhibitions_page():
    """Display exhibitions with optional filter by type."""
    exhibitions = read_exhibitions()
    filter_type = ''
    if request.method == 'POST':
        filter_type = request.form.get('filter_exhibition_type', '').strip()
        if filter_type:
            exhibitions = [ex for ex in exhibitions if ex['exhibition_type'].lower() == filter_type.lower()]
    # Render exhibitions.html
    return render_template('exhibitions.html', exhibitions=exhibitions, filter_type=filter_type)


@app.route('/exhibition/<int:exhibition_id>')
def exhibition_details_page(exhibition_id):
    """Display details for an exhibition and its artifacts."""
    exhibitions = read_exhibitions()
    exhibition = next((ex for ex in exhibitions if int(ex['exhibition_id']) == exhibition_id), None)
    if exhibition is None:
        # Exhibition not found, redirect to exhibitions page
        return redirect(url_for('exhibitions_page'))
    artifacts = read_artifacts()
    artifacts_in_exhibition = [a for a in artifacts if a['exhibition_id'] == str(exhibition_id)]
    # Render exhibition_details.html
    return render_template('exhibition_details.html', exhibition=exhibition, artifacts=artifacts_in_exhibition)


@app.route('/visitor-tickets', methods=['GET', 'POST'])
def visitor_tickets_page():
    """Display visitor tickets and handle ticket purchase."""
    # For demo purposes, assume a current username (simulate logged in user)
    current_username = 'visitor_mary'
    tickets = read_tickets()
    user_tickets = [t for t in tickets if t['username'] == current_username]

    form_data = {}

    if request.method == 'POST':
        # Extract form data
        ticket_type = request.form.get('ticket_type', '')
        number_of_tickets = request.form.get('number_of_tickets', '1')
        visit_date = request.form.get('visit_date', '')  # This field not specified in design but required for data
        visit_time = request.form.get('visit_time', '')  # This field not specified but needed to complete record
        visitor_name = request.form.get('visitor_name', '')
        visitor_email = request.form.get('visitor_email', '')

        form_data = {
            'ticket_type': ticket_type,
            'number_of_tickets': number_of_tickets,
            'visit_date': visit_date,
            'visit_time': visit_time,
            'visitor_name': visitor_name,
            'visitor_email': visitor_email
        }

        # Validate essential fields
        if not (ticket_type and visit_date and visit_time and visitor_name and visitor_email):
            # Render page with existing data and error message (not implemented here)
            return render_template('visitor_tickets.html', tickets=user_tickets, form_data=form_data)

        # Assign a new ticket_id
        try:
            max_id = max(int(t['ticket_id']) for t in tickets) if tickets else 0
        except ValueError:
            max_id = 0
        new_ticket_id = max_id + 1

        # Calculate price based on ticket_type and number_of_tickets
        # Simple pricing example
        pricing = {
            'Standard': 15,
            'Student': 10,
            'Senior': 12,
            'Family': 40,
            'VIP': 50
        }
        price_per_ticket = pricing.get(ticket_type, 15)
        try:
            num_tickets_int = int(number_of_tickets)
        except ValueError:
            num_tickets_int = 1
        total_price = price_per_ticket * num_tickets_int

        purchase_date = datetime.today().strftime('%Y-%m-%d')

        new_ticket = {
            'ticket_id': str(new_ticket_id),
            'username': current_username,
            'ticket_type': ticket_type,
            'visit_date': visit_date,
            'visit_time': visit_time,
            'number_of_tickets': str(num_tickets_int),
            'price': str(total_price),
            'visitor_name': visitor_name,
            'visitor_email': visitor_email,
            'purchase_date': purchase_date
        }

        tickets.append(new_ticket)
        write_tickets(tickets)

        # Refresh the user's tickets list
        user_tickets.append(new_ticket)
        form_data = {}

    return render_template('visitor_tickets.html', tickets=user_tickets, form_data=form_data)


@app.route('/virtual-events', methods=['GET'])
def virtual_events_page():
    """Display virtual events with user registrations."""
    current_username = 'visitor_mary'  # Simulated logged in user
    events = read_events()
    registrations = read_event_registrations()
    user_registrations = [r for r in registrations if r['username'] == current_username]
    # Render virtual_events.html
    return render_template('virtual_events.html', events=events, registrations=user_registrations)


@app.route('/virtual-events/register/<int:event_id>', methods=['POST'])
def register_for_event(event_id):
    """Register current user for a virtual event."""
    current_username = 'visitor_mary'
    registrations = read_event_registrations()
    # Check if already registered
    for r in registrations:
        if r['event_id'] == str(event_id) and r['username'] == current_username:
            return redirect(url_for('virtual_events_page'))
    try:
        max_id = max(int(r['registration_id']) for r in registrations) if registrations else 0
    except ValueError:
        max_id = 0
    new_id = max_id + 1
    registration_date = datetime.today().strftime('%Y-%m-%d')
    new_registration = {
        'registration_id': str(new_id),
        'event_id': str(event_id),
        'username': current_username,
        'registration_date': registration_date
    }
    registrations.append(new_registration)
    write_event_registrations(registrations)
    return redirect(url_for('virtual_events_page'))


@app.route('/virtual-events/cancel/<int:registration_id>', methods=['POST'])
def cancel_event_registration(registration_id):
    """Cancel a user's virtual event registration."""
    current_username = 'visitor_mary'
    registrations = read_event_registrations()
    updated_registrations = [r for r in registrations if not (r['registration_id'] == str(registration_id) and r['username'] == current_username)]
    if len(updated_registrations) < len(registrations):
        write_event_registrations(updated_registrations)
    return redirect(url_for('virtual_events_page'))


@app.route('/audio-guides', methods=['GET', 'POST'])
def audio_guides_page():
    """Display audio guides with optional language filter."""
    audio_guides = read_audioguides()
    filter_language = ''
    if request.method == 'POST':
        filter_language = request.form.get('filter_language', '').strip()
        if filter_language:
            audio_guides = [g for g in audio_guides if g['language'].lower() == filter_language.lower()]
    return render_template('audio_guides.html', audio_guides=audio_guides, filter_language=filter_language)


if __name__ == '__main__':
    app.run(debug=True)
