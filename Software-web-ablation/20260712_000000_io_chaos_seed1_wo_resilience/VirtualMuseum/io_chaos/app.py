from flask import Flask, render_template, request, redirect, url_for
from datetime import date
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Helper functions for reading and writing data files

def read_users():
    users_path = os.path.join(DATA_DIR, 'users.txt')
    try:
        with open(users_path, 'r', encoding='utf-8') as f:
            users = [line.strip() for line in f if line.strip()]
        return users
    except Exception:
        return []


def read_galleries():
    path = os.path.join(DATA_DIR, 'galleries.txt')
    galleries = []
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
                    galleries.append({
                        'gallery_id': gallery_id,
                        'gallery_name': gallery_name,
                        'floor': floor,
                        'capacity': capacity,
                        'theme': theme,
                        'status': status
                    })
        return galleries
    except Exception:
        return []


def read_exhibitions():
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
        return exhibitions
    except Exception:
        return []


def read_artifacts():
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
        return artifacts
    except Exception:
        return []


def read_audioguides():
    path = os.path.join(DATA_DIR, 'audioguides.txt')
    guides = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 8:
                    guide_id = int(parts[0])
                    exhibit_number = int(parts[1])
                    title = parts[2]
                    language = parts[3]
                    duration = int(parts[4])
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
        return guides
    except Exception:
        return []


def read_tickets():
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
                    price = float(parts[6])
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
        return tickets
    except Exception:
        return []


def read_events():
    path = os.path.join(DATA_DIR, 'events.txt')
    events = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 9:
                    event_id = int(parts[0])
                    title = parts[1]
                    date_str = parts[2]
                    time_str = parts[3]
                    event_type = parts[4]
                    speaker = parts[5]
                    capacity = int(parts[6])
                    description = parts[7]
                    created_by = parts[8]
                    events.append({
                        'event_id': event_id,
                        'title': title,
                        'date': date_str,
                        'time': time_str,
                        'event_type': event_type,
                        'speaker': speaker,
                        'capacity': capacity,
                        'description': description,
                        'created_by': created_by
                    })
        return events
    except Exception:
        return []


def read_event_registrations():
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
        return registrations
    except Exception:
        return []


def write_file(filepath, lines):
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            for line in lines:
                f.write(line + '\n')
        return True
    except Exception:
        return False


# ========== ROUTES ===========

@app.route('/')
def root_redirect():
    # Redirect root to dashboard
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    exhibitions = read_exhibitions()
    artifacts = read_artifacts()
    galleries = {g['gallery_id']: g for g in read_galleries()}

    # Compute exhibitions_summary
    total_exhibitions = len(exhibitions)
    today = date.today().isoformat()
    active_exhibitions = 0
    for ex in exhibitions:
        if ex['start_date'] <= today <= ex['end_date']:
            active_exhibitions += 1

    # Compute artifacts_summary
    total_artifacts = len(artifacts)

    exhibitions_summary = {'total': total_exhibitions, 'active': active_exhibitions}
    artifacts_summary = {'total': total_artifacts}

    # No authentication specified, user is optional None
    user = None

    return render_template('dashboard.html', exhibitions_summary=exhibitions_summary, artifacts_summary=artifacts_summary, user=user)


@app.route('/artifacts', methods=['GET', 'POST'])
def artifact_catalog():
    artifacts_all = read_artifacts()
    exhibitions = {ex['exhibition_id']: ex for ex in read_exhibitions()}

    # We will enrich artifact with exhibition_title
    enriched_artifacts = []
    for art in artifacts_all:
        exhibition_title = exhibitions.get(art['exhibition_id'], {}).get('title', 'Unknown')
        enriched_artifacts.append({
            'artifact_id': art['artifact_id'],
            'artifact_name': art['artifact_name'],
            'period': art['period'],
            'origin': art['origin'],
            'exhibition_title': exhibition_title
        })

    search_query = ''
    if request.method == 'POST':
        # filter by artifact_name containing search_query (case insensitive)
        search_query = request.form.get('search_query', '').strip()
        if search_query:
            enriched_artifacts = [a for a in enriched_artifacts if search_query.lower() in a['artifact_name'].lower()]

    elif request.method == 'GET':
        # Optionally get search from query param
        search_query = request.args.get('search_query', '').strip()
        if search_query:
            enriched_artifacts = [a for a in enriched_artifacts if search_query.lower() in a['artifact_name'].lower()]

    return render_template('artifact_catalog.html', artifacts=enriched_artifacts, search_query=search_query)


@app.route('/exhibitions', methods=['GET', 'POST'])
def exhibitions():
    exhibitions_all = read_exhibitions()
    galleries = {g['gallery_id']: g for g in read_galleries()}

    filter_type = ''
    if request.method == 'POST':
        filter_type = request.form.get('filter_type', '').strip()
    elif request.method == 'GET':
        filter_type = request.args.get('filter_type', '').strip()

    # Apply filter if valid
    filtered_exhibitions = []
    for ex in exhibitions_all:
        if filter_type in ['Permanent', 'Temporary', 'Virtual']:
            if ex['exhibition_type'] == filter_type:
                filtered_exhibitions.append(ex)
        else:
            filtered_exhibitions.append(ex)

    # Add gallery_name and status derived from gallery
    enriched_exhibitions = []
    for ex in filtered_exhibitions:
        gallery = galleries.get(ex['gallery_id'])
        gallery_name = gallery['gallery_name'] if gallery else 'Unknown'
        status = gallery['status'] if gallery else 'Unknown'
        enriched_exhibitions.append({
            'exhibition_id': ex['exhibition_id'],
            'title': ex['title'],
            'exhibition_type': ex['exhibition_type'],
            'start_date': ex['start_date'],
            'end_date': ex['end_date'],
            'gallery_name': gallery_name,
            'status': status
        })

    return render_template('exhibitions.html', exhibitions=enriched_exhibitions, filter_type=filter_type)


@app.route('/exhibition/<int:id>')
def exhibition_details(id):
    exhibitions_all = read_exhibitions()
    artifacts_all = read_artifacts()

    exhibition = None
    for ex in exhibitions_all:
        if ex['exhibition_id'] == id:
            exhibition = {
                'exhibition_id': ex['exhibition_id'],
                'title': ex['title'],
                'description': ex['description'],
                'start_date': ex['start_date'],
                'end_date': ex['end_date']
            }
            break
    if not exhibition:
        return "Exhibition not found", 404

    # Get artifacts belonging to this exhibition
    exhibition_artifacts = []
    for art in artifacts_all:
        if art['exhibition_id'] == id:
            exhibition_artifacts.append({
                'artifact_id': art['artifact_id'],
                'artifact_name': art['artifact_name'],
                'period': art['period'],
                'origin': art['origin']
            })

    return render_template('exhibition_details.html', exhibition=exhibition, artifacts=exhibition_artifacts)


@app.route('/tickets', methods=['GET', 'POST'])
def visitor_tickets():
    tickets_all = read_tickets()
    ticket_types = ['Standard', 'Student', 'Senior', 'Family', 'VIP']

    # No auth implemented, assume user is None or a default visitor
    user = None

    # For demonstration, filtering or adding tickets is minimal as no user input specified
    tickets = tickets_all

    if request.method == 'POST':
        # We can simulate ticket purchase by reading form data
        ticket_type = request.form.get('ticket_type')
        visit_date = request.form.get('visit_date')
        visit_time = request.form.get('visit_time')
        number_of_tickets = request.form.get('number_of_tickets')
        visitor_name = request.form.get('visitor_name')
        visitor_email = request.form.get('visitor_email')

        if not ticket_type or not visit_date or not visit_time or not number_of_tickets or not visitor_name or not visitor_email:
            # Required fields missing
            pass
        else:
            try:
                number_of_tickets = int(number_of_tickets)
                # Determine new ticket_id
                new_ticket_id = max([t['ticket_id'] for t in tickets_all], default=0) + 1
                # Price calculation (example): Standard 15, Student 10, Senior 12, Family 40, VIP 50
                price_map = {'Standard': 15, 'Student': 10, 'Senior': 12, 'Family': 40, 'VIP': 50}
                price_per_ticket = price_map.get(ticket_type, 15)
                total_price = price_per_ticket * number_of_tickets

                # username is unknown, use visitor_name simplified
                username = visitor_name.replace(' ', '_').lower()
                purchase_date = date.today().isoformat()

                # Append new ticket
                new_ticket = {
                    'ticket_id': new_ticket_id,
                    'username': username,
                    'ticket_type': ticket_type,
                    'visit_date': visit_date,
                    'visit_time': visit_time,
                    'number_of_tickets': number_of_tickets,
                    'price': float(total_price),
                    'visitor_name': visitor_name,
                    'visitor_email': visitor_email,
                    'purchase_date': purchase_date
                }

                tickets_all.append(new_ticket)

                # Save tickets
                lines = []
                for t in tickets_all:
                    line = '|'.join([
                        str(t['ticket_id']), t['username'], t['ticket_type'], t['visit_date'], t['visit_time'], 
                        str(t['number_of_tickets']), f"{t['price']:.2f}", t['visitor_name'], t['visitor_email'], t['purchase_date']
                    ])
                    lines.append(line)

                filepath = os.path.join(DATA_DIR, 'tickets.txt')
                try:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write('\n'.join(lines) + '\n')
                except Exception:
                    pass

                return redirect(url_for('visitor_tickets'))
            except Exception:
                pass

    return render_template('visitor_tickets.html', tickets=tickets, ticket_types=ticket_types, user=user)


@app.route('/virtual-events', methods=['GET', 'POST'])
def virtual_events():
    events_all = read_events()
    registrations_all = read_event_registrations()

    # Assume user session info not implemented, user is None
    user = None

    if request.method == 'POST':
        # No POST form fields specified, so just show events
        pass

    # Build user registrations event_id list
    user_registrations = [r['event_id'] for r in registrations_all if r['username'] == user]

    # Build events list with registration status for this user
    events = []
    for ev in events_all:
        registered = 'Registered' if ev['event_id'] in user_registrations else 'Not Registered'
        events.append({
            'event_id': ev['event_id'],
            'title': ev['title'],
            'date': ev['date'],
            'time': ev['time'],
            'event_type': ev['event_type'],
            'registration_status': registered
        })

    return render_template('virtual_events.html', events=events, user_registrations=user_registrations)


@app.route('/register-event/<int:id>', methods=['POST'])
def register_event(id):
    # For simplicity, user is None, so fail registration
    registration_response = 'Failure: User not logged in or unknown.'

    # We must implement registration logic if user present
    # Since no authentication is defined, just failure

    return registration_response, 400


@app.route('/cancel-registration/<int:registration_id>', methods=['POST'])
def cancel_registration(registration_id):
    # For simplicity, user is None, so fail cancellation
    cancel_response = 'Failure: User not logged in or unknown.'
    return cancel_response, 400


@app.route('/audio-guides', methods=['GET', 'POST'])
def audio_guides():
    guides_all = read_audioguides()

    filter_language = ''
    if request.method == 'POST':
        filter_language = request.form.get('filter_language', '').strip()
    elif request.method == 'GET':
        filter_language = request.args.get('filter_language', '').strip()

    filtered_guides = []
    for guide in guides_all:
        if filter_language:
            if guide['language'].lower() == filter_language.lower():
                filtered_guides.append(guide)
        else:
            filtered_guides.append(guide)

    # Prepare audio_guides list with required keys
    audio_guides_list = []
    for g in filtered_guides:
        audio_guides_list.append({
            'guide_id': g['guide_id'],
            'exhibit_number': g['exhibit_number'],
            'title': g['title'],
            'language': g['language'],
            'duration': g['duration']
        })

    return render_template('audio_guides.html', audio_guides=audio_guides_list, filter_language=filter_language)


if __name__ == '__main__':
    app.run(port=5000, debug=True)
