from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

data_dir = 'data'

# Utility functions to load and save data files

def load_users():
    users = []
    try:
        with open(os.path.join(data_dir, 'users.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                username = line.strip()
                if username:
                    users.append(username)
    except FileNotFoundError:
        pass
    return users


def load_galleries():
    galleries = []
    try:
        with open(os.path.join(data_dir, 'galleries.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 6:
                    galleries.append({
                        'gallery_id': int(parts[0]),
                        'gallery_name': parts[1],
                        'floor': parts[2],
                        'capacity': parts[3],
                        'theme': parts[4],
                        'status': parts[5]
                    })
    except FileNotFoundError:
        pass
    return galleries


def load_exhibitions():
    exhibitions = []
    try:
        with open(os.path.join(data_dir, 'exhibitions.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 9:
                    exhibitions.append({
                        'exhibition_id': int(parts[0]),
                        'title': parts[1],
                        'description': parts[2],
                        'gallery_id': int(parts[3]),
                        'exhibition_type': parts[4],
                        'start_date': parts[5],
                        'end_date': parts[6],
                        'curator_name': parts[7],
                        'created_by': parts[8]
                    })
    except FileNotFoundError:
        pass
    return exhibitions


def load_artifacts():
    artifacts = []
    try:
        with open(os.path.join(data_dir, 'artifacts.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 9:
                    artifacts.append({
                        'artifact_id': int(parts[0]),
                        'artifact_name': parts[1],
                        'period': parts[2],
                        'origin': parts[3],
                        'description': parts[4],
                        'exhibition_id': int(parts[5]),
                        'storage_location': parts[6],
                        'acquisition_date': parts[7],
                        'added_by': parts[8]
                    })
    except FileNotFoundError:
        pass
    return artifacts


def load_audioguides():
    audio_guides = []
    try:
        with open(os.path.join(data_dir, 'audioguides.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 8:
                    audio_guides.append({
                        'guide_id': int(parts[0]),
                        'exhibit_number': parts[1],
                        'title': parts[2],
                        'language': parts[3],
                        'duration': parts[4],
                        'script': parts[5],
                        'narrator': parts[6],
                        'created_by': parts[7]
                    })
    except FileNotFoundError:
        pass
    return audio_guides


def load_tickets():
    tickets = []
    try:
        with open(os.path.join(data_dir, 'tickets.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 10:
                    tickets.append({
                        'ticket_id': int(parts[0]),
                        'username': parts[1],
                        'ticket_type': parts[2],
                        'visit_date': parts[3],
                        'visit_time': parts[4],
                        'number_of_tickets': int(parts[5]),
                        'price': float(parts[6]),
                        'visitor_name': parts[7],
                        'visitor_email': parts[8],
                        'purchase_date': parts[9]
                    })
    except FileNotFoundError:
        pass
    return tickets


def load_events():
    events = []
    try:
        with open(os.path.join(data_dir, 'events.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 9:
                    events.append({
                        'event_id': int(parts[0]),
                        'title': parts[1],
                        'date': parts[2],
                        'time': parts[3],
                        'event_type': parts[4],
                        'speaker': parts[5],
                        'capacity': int(parts[6]),
                        'description': parts[7],
                        'created_by': parts[8]
                    })
    except FileNotFoundError:
        pass
    return events


def load_event_registrations():
    registrations = []
    try:
        with open(os.path.join(data_dir, 'event_registrations.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 4:
                    registrations.append({
                        'registration_id': int(parts[0]),
                        'event_id': int(parts[1]),
                        'username': parts[2],
                        'registration_date': parts[3]
                    })
    except FileNotFoundError:
        pass
    return registrations


# File write helpers

def save_tickets(tickets):
    try:
        with open(os.path.join(data_dir, 'tickets.txt'), 'w', encoding='utf-8') as f:
            for t in tickets:
                line = f"{t['ticket_id']}|{t['username']}|{t['ticket_type']}|{t['visit_date']}|{t['visit_time']}|{t['number_of_tickets']}|{t['price']}|{t['visitor_name']}|{t['visitor_email']}|{t['purchase_date']}\n"
                f.write(line)
    except Exception:
        pass


def save_event_registrations(registrations):
    try:
        with open(os.path.join(data_dir, 'event_registrations.txt'), 'w', encoding='utf-8') as f:
            for r in registrations:
                line = f"{r['registration_id']}|{r['event_id']}|{r['username']}|{r['registration_date']}\n"
                f.write(line)
    except Exception:
        pass


@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    exhibitions = load_exhibitions()
    total_exhibitions = len(exhibitions)
    # Count active exhibitions: current date in range [start_date, end_date]
    active_exhibitions = 0
    now_date = datetime.now().date()
    for e in exhibitions:
        try:
            start = datetime.strptime(e['start_date'], '%Y-%m-%d').date()
            end = datetime.strptime(e['end_date'], '%Y-%m-%d').date()
            if start <= now_date <= end:
                active_exhibitions += 1
        except Exception:
            pass
    exhibition_summary = {
        'total_exhibitions': total_exhibitions,
        'active_exhibitions': active_exhibitions
    }
    username = 'curator_john'  # Default username or could be from session (not specified)
    other_overview_data = {}  # Not specified details
    return render_template('dashboard.html', exhibition_summary=exhibition_summary, username=username, other_overview_data=other_overview_data)


@app.route('/artifacts', methods=['GET', 'POST'])
def artifact_catalog():
    artifacts = load_artifacts()
    search_query = ''
    filters = {}

    if request.method == 'POST':
        search_query = request.form.get('search_query', '').strip()
        # Filters are not specified in detail, keep whole filters dict empty or with keys if found
        # For now assume no complex filters implemented
        # We could filter by artifact_name containing search_query or artifact_id matching search_query

    # Filter artifacts by search_query
    if search_query:
        filtered = []
        for a in artifacts:
            if (search_query.lower() in a['artifact_name'].lower() or
                search_query == str(a['artifact_id'])):
                filtered.append(a)
        artifacts = filtered

    return render_template('artifact_catalog.html', artifacts=artifacts, search_query=search_query, filters=filters)


@app.route('/exhibitions', methods=['GET', 'POST'])
def exhibitions():
    exhibitions_list = load_exhibitions()
    filter_type = ''
    if request.method == 'POST':
        filter_type = request.form.get('filter_type', '').strip()

    if filter_type:
        exhibitions_list = [e for e in exhibitions_list if e['exhibition_type'].lower() == filter_type.lower()]

    return render_template('exhibitions.html', exhibitions=exhibitions_list, filter_type=filter_type)


@app.route('/exhibition/<int:exhibition_id>')
def exhibition_details(exhibition_id):
    exhibitions_list = load_exhibitions()
    exhibition = None
    for e in exhibitions_list:
        if e['exhibition_id'] == exhibition_id:
            exhibition = e
            break
    if not exhibition:
        exhibition = {  # fallback empty
            'exhibition_id': exhibition_id,
            'title': 'Unknown Exhibition',
            'description': '',
            'gallery_id': None,
            'exhibition_type': '',
            'start_date': '',
            'end_date': '',
            'curator_name': '',
            'created_by': ''
        }
    artifacts = [a for a in load_artifacts() if a['exhibition_id'] == exhibition_id]
    return render_template('exhibition_details.html', exhibition=exhibition, artifacts=artifacts)


@app.route('/tickets', methods=['GET', 'POST'])
def visitor_tickets():
    ticket_types = ['Standard', 'Student', 'Senior', 'Family', 'VIP']
    tickets = load_tickets()
    username = 'visitor_mary'  # Default user for demonstration

    if request.method == 'POST':
        # Purchase ticket form
        ticket_type = request.form.get('ticket_type', '')
        visit_date = request.form.get('visit_date', '')
        visit_time = request.form.get('visit_time', '')
        number_of_tickets = request.form.get('number_of_tickets', '1')
        visitor_name = request.form.get('visitor_name', '')
        visitor_email = request.form.get('visitor_email', '')

        try:
            number_of_tickets = int(number_of_tickets)
        except ValueError:
            number_of_tickets = 1

        # Price setting simple logic, not specified, assume:
        price_map = {
            'Standard': 15.0,
            'Student': 10.0,
            'Senior': 12.0,
            'Family': 40.0,
            'VIP': 50.0
        }
        price = price_map.get(ticket_type, 15.0) * number_of_tickets

        # Assign new ticket_id
        max_id = 0
        for t in tickets:
            if t['ticket_id'] > max_id:
                max_id = t['ticket_id']
        new_ticket_id = max_id + 1

        purchase_date = datetime.now().strftime('%Y-%m-%d')

        ticket_entry = {
            'ticket_id': new_ticket_id,
            'username': username,
            'ticket_type': ticket_type,
            'visit_date': visit_date,
            'visit_time': visit_time,
            'number_of_tickets': number_of_tickets,
            'price': price,
            'visitor_name': visitor_name,
            'visitor_email': visitor_email,
            'purchase_date': purchase_date
        }

        tickets.append(ticket_entry)
        save_tickets(tickets)

    # Show tickets for the current user
    user_tickets = [t for t in tickets if t['username'] == 'visitor_mary']

    return render_template('visitor_tickets.html', tickets=user_tickets, ticket_types=ticket_types)


@app.route('/events', methods=['GET', 'POST'])
def virtual_events():
    events_list = load_events()
    registrations = load_event_registrations()
    username = 'visitor_mary'

    user_registrations = [r for r in registrations if r['username'] == username]

    if request.method == 'POST':
        # No detailed POST form processing specified for /events POST, so assume no action or support filter (not detailed)
        pass

    return render_template('virtual_events.html', events=events_list, registrations=registrations, user_registrations=user_registrations)


@app.route('/register_event/<int:event_id>', methods=['POST'])
def register_event(event_id):
    registrations = load_event_registrations()
    username = 'visitor_mary'
    max_reg_id = 0
    for r in registrations:
        if r['registration_id'] > max_reg_id:
            max_reg_id = r['registration_id']

    # Check if user already registered for event
    for r in registrations:
        if r['event_id'] == event_id and r['username'] == username:
            return redirect(url_for('virtual_events'))  # Already registered, no duplicate

    new_registration_id = max_reg_id + 1
    registration_date = datetime.now().strftime('%Y-%m-%d')

    new_registration = {
        'registration_id': new_registration_id,
        'event_id': event_id,
        'username': username,
        'registration_date': registration_date
    }
    registrations.append(new_registration)
    save_event_registrations(registrations)

    return redirect(url_for('virtual_events'))


@app.route('/cancel_registration/<int:registration_id>', methods=['POST'])
def cancel_registration(registration_id):
    registrations = load_event_registrations()
    username = 'visitor_mary'
    new_registrations = [r for r in registrations if not (r['registration_id'] == registration_id and r['username'] == username)]
    if len(new_registrations) != len(registrations):
        save_event_registrations(new_registrations)
    return redirect(url_for('virtual_events'))


@app.route('/audio_guides', methods=['GET', 'POST'])
def audio_guides():
    audio_guides_list = load_audioguides()
    filter_language = ''
    if request.method == 'POST':
        filter_language = request.form.get('filter_language', '').strip()

    if filter_language:
        audio_guides_list = [g for g in audio_guides_list if g['language'].lower() == filter_language.lower()]

    return render_template('audio_guides.html', audio_guides=audio_guides_list, filter_language=filter_language)


if __name__ == "__main__":
    app.run(port=5000, debug=True)
