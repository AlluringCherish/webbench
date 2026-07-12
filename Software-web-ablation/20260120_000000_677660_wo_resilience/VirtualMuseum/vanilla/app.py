from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Utility functions to load data from files

def load_exhibitions():
    path = os.path.join(DATA_DIR, 'exhibitions.txt')
    exhibitions = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 9:
                    exhibition_id = int(parts[0])
                    title = parts[1]
                    description = parts[2]
                    gallery_id = int(parts[3])
                    exhibition_type = parts[4]
                    start_date = parts[5]
                    end_date = parts[6]
                    curator_name = parts[7]
                    created_by = parts[8]
                    exhibitions.append({
                        'exhibition_id': exhibition_id,
                        'title': title,
                        'description': description,
                        'gallery_id': gallery_id,
                        'exhibition_type': exhibition_type,
                        'start_date': start_date,
                        'end_date': end_date,
                        'curator_name': curator_name,
                        'created_by': created_by
                    })
    except FileNotFoundError:
        pass
    return exhibitions


def load_galleries():
    path = os.path.join(DATA_DIR, 'galleries.txt')
    galleries = {}
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 6:
                    gallery_id = int(parts[0])
                    gallery_name = parts[1]
                    floor = parts[2]
                    capacity = parts[3]
                    theme = parts[4]
                    status = parts[5]
                    galleries[gallery_id] = {
                        'gallery_id': gallery_id,
                        'gallery_name': gallery_name,
                        'floor': floor,
                        'capacity': capacity,
                        'theme': theme,
                        'status': status
                    }
    except FileNotFoundError:
        pass
    return galleries


def load_artifacts():
    path = os.path.join(DATA_DIR, 'artifacts.txt')
    artifacts = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 9:
                    artifact_id = int(parts[0])
                    artifact_name = parts[1]
                    period = parts[2]
                    origin = parts[3]
                    description = parts[4]
                    exhibition_id = int(parts[5])
                    storage_location = parts[6]
                    acquisition_date = parts[7]
                    added_by = parts[8]
                    artifacts.append({
                        'artifact_id': artifact_id,
                        'artifact_name': artifact_name,
                        'period': period,
                        'origin': origin,
                        'description': description,
                        'exhibition_id': exhibition_id,
                        'storage_location': storage_location,
                        'acquisition_date': acquisition_date,
                        'added_by': added_by
                    })
    except FileNotFoundError:
        pass
    return artifacts


def load_audioguides():
    path = os.path.join(DATA_DIR, 'audioguides.txt')
    guides = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 8:
                    guide_id = int(parts[0])
                    exhibit_number = parts[1]
                    title = parts[2]
                    language = parts[3]
                    duration = parts[4]
                    script = parts[5]
                    narrator = parts[6]
                    created_by = parts[7]
                    guides.append({
                        'guide_id': guide_id,
                        'exhibit_number': exhibit_number,
                        'title': title,
                        'language': language,
                        'duration': duration,
                        'script': script,
                        'narrator': narrator,
                        'created_by': created_by
                    })
    except FileNotFoundError:
        pass
    return guides


def load_tickets():
    path = os.path.join(DATA_DIR, 'tickets.txt')
    tickets = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 10:
                    ticket_id = int(parts[0])
                    username = parts[1]
                    ticket_type = parts[2]
                    visit_date = parts[3]
                    visit_time = parts[4]
                    number_of_tickets = int(parts[5])
                    price = parts[6]
                    visitor_name = parts[7]
                    visitor_email = parts[8]
                    purchase_date = parts[9]
                    tickets.append({
                        'ticket_id': ticket_id,
                        'username': username,
                        'ticket_type': ticket_type,
                        'visit_date': visit_date,
                        'visit_time': visit_time,
                        'number_of_tickets': number_of_tickets,
                        'price': price,
                        'visitor_name': visitor_name,
                        'visitor_email': visitor_email,
                        'purchase_date': purchase_date
                    })
    except FileNotFoundError:
        pass
    return tickets


def load_events():
    path = os.path.join(DATA_DIR, 'events.txt')
    events = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 9:
                    event_id = int(parts[0])
                    title = parts[1]
                    date = parts[2]
                    time = parts[3]
                    event_type = parts[4]
                    speaker = parts[5]
                    capacity = parts[6]
                    description = parts[7]
                    created_by = parts[8]
                    events.append({
                        'event_id': event_id,
                        'title': title,
                        'date': date,
                        'time': time,
                        'event_type': event_type,
                        'speaker': speaker,
                        'capacity': capacity,
                        'description': description,
                        'created_by': created_by
                    })
    except FileNotFoundError:
        pass
    return events


def load_event_registrations():
    path = os.path.join(DATA_DIR, 'event_registrations.txt')
    registrations = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 4:
                    registration_id = int(parts[0])
                    event_id = int(parts[1])
                    username = parts[2]
                    registration_date = parts[3]
                    registrations.append({
                        'registration_id': registration_id,
                        'event_id': event_id,
                        'username': username,
                        'registration_date': registration_date
                    })
    except FileNotFoundError:
        pass
    return registrations


def save_tickets(tickets):
    path = os.path.join(DATA_DIR, 'tickets.txt')
    try:
        with open(path, 'w', encoding='utf-8') as f:
            for t in tickets:
                # Write all fields in order
                line = f"{t['ticket_id']}|{t['username']}|{t['ticket_type']}|{t['visit_date']}|{t['visit_time']}|{t['number_of_tickets']}|{t['price']}|{t['visitor_name']}|{t['visitor_email']}|{t['purchase_date']}\n"
                f.write(line)
    except Exception:
        pass


def save_event_registrations(registrations):
    path = os.path.join(DATA_DIR, 'event_registrations.txt')
    try:
        with open(path, 'w', encoding='utf-8') as f:
            for r in registrations:
                line = f"{r['registration_id']}|{r['event_id']}|{r['username']}|{r['registration_date']}\n"
                f.write(line)
    except Exception:
        pass


def get_username():
    # For demonstration, we assume a static username. In real apps this comes from authentication.
    # We'll use 'visitor_mary' as default user for tickets and event registrations.
    return 'visitor_mary'


@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    exhibitions = load_exhibitions()

    total_exhibitions = len(exhibitions)
    active_exhibitions = 0
    now_str = datetime.now().strftime('%Y-%m-%d')
    for ex in exhibitions:
        if ex['start_date'] <= now_str <= ex['end_date']:
            active_exhibitions += 1

    exhibitions_summary = {
        'total_exhibitions': total_exhibitions,
        'active_exhibitions': active_exhibitions
    }

    return render_template('dashboard.html', exhibitions_summary=exhibitions_summary)


@app.route('/artifacts', methods=['GET', 'POST'])
def artifact_catalog():
    artifacts = load_artifacts()
    exhibitions = load_exhibitions()
    exhibition_title_map = {ex['exhibition_id']: ex['title'] for ex in exhibitions}

    search_query = ''
    if request.method == 'POST':
        search_query = request.form.get('search_query', '').strip()
    else:
        search_query = request.args.get('search_query', '').strip()

    # Filter artifacts by search query if provided
    filtered_artifacts = []
    if search_query:
        # Search by artifact_name or artifact_id (as string)
        for a in artifacts:
            if (search_query.lower() in a['artifact_name'].lower()) or (search_query == str(a['artifact_id'])):
                filtered_artifacts.append(a)
    else:
        filtered_artifacts = artifacts

    result_artifacts = []
    for a in filtered_artifacts:
        exhibition_title = exhibition_title_map.get(a['exhibition_id'], '')
        result_artifacts.append({
            'artifact_id': a['artifact_id'],
            'artifact_name': a['artifact_name'],
            'period': a['period'],
            'origin': a['origin'],
            'exhibition_title': exhibition_title
        })

    return render_template('artifact_catalog.html', artifacts=result_artifacts, search_query=search_query)


@app.route('/exhibitions', methods=['GET', 'POST'])
def exhibitions_list():
    exhibitions = load_exhibitions()
    galleries = load_galleries()

    filter_type = ''
    if request.method == 'POST':
        filter_type = request.form.get('filter_type', '')
    else:
        filter_type = request.args.get('filter_type', '')

    filtered_exhibitions = []
    if filter_type in ['Permanent', 'Temporary', 'Virtual']:
        filtered_exhibitions = [ex for ex in exhibitions if ex['exhibition_type'] == filter_type]
    else:
        filtered_exhibitions = exhibitions

    result_exhibitions = []
    for ex in filtered_exhibitions:
        gallery_name = galleries.get(ex['gallery_id'], {}).get('gallery_name', '')
        # Determine status from gallery status field, fallback to 'Closed'
        gallery_status = galleries.get(ex['gallery_id'], {}).get('status', 'Closed')
        status = 'Open' if gallery_status == 'Open' else 'Closed'
        result_exhibitions.append({
            'exhibition_id': ex['exhibition_id'],
            'title': ex['title'],
            'exhibition_type': ex['exhibition_type'],
            'start_date': ex['start_date'],
            'end_date': ex['end_date'],
            'gallery_name': gallery_name,
            'status': status
        })

    return render_template('exhibitions.html', exhibitions=result_exhibitions, filter_type=filter_type)


@app.route('/exhibition/<int:exhibition_id>')
def exhibition_details(exhibition_id):
    exhibitions = load_exhibitions()
    exhibition = None
    for ex in exhibitions:
        if ex['exhibition_id'] == exhibition_id:
            exhibition = {
                'exhibition_id': ex['exhibition_id'],
                'title': ex['title'],
                'description': ex['description'],
                'start_date': ex['start_date'],
                'end_date': ex['end_date']
            }
            break

    if not exhibition:
        # Exhibition not found, return 404
        return "Exhibition not found", 404

    artifacts = load_artifacts()
    # Filter artifacts that belong to this exhibition
    filtered_artifacts = []
    for a in artifacts:
        if a['exhibition_id'] == exhibition_id:
            filtered_artifacts.append({
                'artifact_id': a['artifact_id'],
                'artifact_name': a['artifact_name'],
                'period': a['period'],
                'origin': a['origin']
            })

    return render_template('exhibition_details.html', exhibition=exhibition, artifacts=filtered_artifacts)


@app.route('/tickets', methods=['GET', 'POST'])
def visitor_tickets():
    username = get_username()
    tickets = load_tickets()

    # Filter tickets for current user
    user_tickets = [t for t in tickets if t['username'] == username]

    if request.method == 'POST':
        ticket_type = request.form.get('ticket_type', '')
        try:
            number_of_tickets = int(request.form.get('number_of_tickets', '0'))
        except ValueError:
            number_of_tickets = 0

        if ticket_type and number_of_tickets > 0:
            # Create a new ticket entry
            max_ticket_id = max([t['ticket_id'] for t in tickets], default=0)
            new_ticket_id = max_ticket_id + 1
            visit_date = datetime.now().strftime('%Y-%m-%d')
            visit_time = '10:00 AM'  # Fixed time for simplicity
            price_map = {
                'Standard': '15',
                'Student': '10',
                'Senior': '12',
                'Family': '40',
                'VIP': '50'
            }
            price = price_map.get(ticket_type, '15')

            # Per spec no visitor name/email given - default as username
            visitor_name = username
            visitor_email = f"{username}@email.com"
            purchase_date = datetime.now().strftime('%Y-%m-%d')

            new_ticket = {
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

            tickets.append(new_ticket)

            # Save tickets
            save_tickets(tickets)

            # Refresh user tickets
            user_tickets = [t for t in tickets if t['username'] == username]

    return render_template('visitor_tickets.html', tickets=user_tickets, username=username)


@app.route('/events', methods=['GET', 'POST'])
def virtual_events():
    username = get_username()
    events = load_events()
    registrations = load_event_registrations()

    user_registrations = [r['event_id'] for r in registrations if r['username'] == username]

    # Compose events with registration_status
    events_for_render = []
    for e in events:
        registration_status = e['event_id'] in user_registrations
        events_for_render.append({
            'event_id': e['event_id'],
            'title': e['title'],
            'date': e['date'],
            'time': e['time'],
            'event_type': e['event_type'],
            'registration_status': registration_status
        })

    return render_template('virtual_events.html', events=events_for_render, user_registrations=user_registrations)


@app.route('/event/register/<int:event_id>', methods=['POST'])
def register_event(event_id):
    username = get_username()
    registrations = load_event_registrations()

    # Check if already registered
    for r in registrations:
        if r['event_id'] == event_id and r['username'] == username:
            # Already registered, no action
            return redirect(url_for('virtual_events'))

    # Determine new registration_id
    max_registration_id = max([r['registration_id'] for r in registrations], default=0)
    new_registration_id = max_registration_id + 1
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


@app.route('/event/cancel/<int:registration_id>', methods=['POST'])
def cancel_event_registration(registration_id):
    username = get_username()
    registrations = load_event_registrations()

    # Remove the registration if it belongs to the user
    registrations = [r for r in registrations if not (r['registration_id'] == registration_id and r['username'] == username)]

    save_event_registrations(registrations)

    return redirect(url_for('virtual_events'))


@app.route('/audio-guides', methods=['GET', 'POST'])
def audio_guides():
    guides = load_audioguides()

    filter_language = ''
    if request.method == 'POST':
        filter_language = request.form.get('filter_language', '')
    else:
        filter_language = request.args.get('filter_language', '')

    filtered_guides = []
    if filter_language in ['English', 'Spanish', 'French']:
        filtered_guides = [g for g in guides if g['language'] == filter_language]
    else:
        filtered_guides = guides

    result_guides = []
    for g in filtered_guides:
        result_guides.append({
            'guide_id': g['guide_id'],
            'exhibit_number': g['exhibit_number'],
            'title': g['title'],
            'language': g['language'],
            'duration': g['duration']
        })

    return render_template('audio_guides.html', audio_guides=result_guides, filter_language=filter_language)


if __name__ == '__main__':
    app.run(port=5000, debug=True)
