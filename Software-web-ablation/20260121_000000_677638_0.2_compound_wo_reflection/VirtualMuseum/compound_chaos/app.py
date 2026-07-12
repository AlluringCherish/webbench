from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_FOLDER = 'data'

# Helper functions to read and write data files

def read_file_lines(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
        return lines
    except FileNotFoundError:
        return []
    except IOError:
        return []

def write_file_lines(filename, lines):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            for line in lines:
                f.write(line + '\n')
        return True
    except IOError:
        return False

# Users

def get_users():
    path = os.path.join(DATA_FOLDER, 'users.txt')
    return read_file_lines(path)

# Galleries

def get_galleries_dict():
    # Return dictionary keyed by gallery_id (int)
    path = os.path.join(DATA_FOLDER, 'galleries.txt')
    galleries = {}
    lines = read_file_lines(path)
    for line in lines:
        parts = line.split('|')
        if len(parts) != 6:
            continue
        gallery_id, gallery_name, floor, capacity, theme, status = parts
        try:
            gid = int(gallery_id)
            galleries[gid] = {
                'gallery_id': gid,
                'gallery_name': gallery_name,
                'floor': floor,
                'capacity': capacity,
                'theme': theme,
                'status': status
            }
        except:
            continue
    return galleries

# Exhibitions

def get_exhibitions():
    path = os.path.join(DATA_FOLDER, 'exhibitions.txt')
    exhibitions = []
    lines = read_file_lines(path)
    for line in lines:
        parts = line.split('|')
        if len(parts) != 9:
            continue
        exhibition_id, title, description, gallery_id, exhibition_type, start_date, end_date, curator_name, created_by = parts
        try:
            exhibitions.append({
                'exhibition_id': int(exhibition_id),
                'title': title,
                'description': description,
                'gallery_id': int(gallery_id),
                'exhibition_type': exhibition_type,
                'start_date': start_date,
                'end_date': end_date,
                'curator_name': curator_name,
                'created_by': created_by
            })
        except:
            continue
    return exhibitions

# Artifacts

def get_artifacts():
    path = os.path.join(DATA_FOLDER, 'artifacts.txt')
    artifacts = []
    lines = read_file_lines(path)
    for line in lines:
        parts = line.split('|')
        if len(parts) != 9:
            continue
        (artifact_id, artifact_name, period, origin, description, exhibition_id,
         storage_location, acquisition_date, added_by) = parts
        try:
            artifacts.append({
                'artifact_id': int(artifact_id),
                'artifact_name': artifact_name,
                'period': period,
                'origin': origin,
                'description': description,
                'exhibition_id': int(exhibition_id),
                'storage_location': storage_location,
                'acquisition_date': acquisition_date,
                'added_by': added_by
            })
        except:
            continue
    return artifacts

# Audioguides

def get_audioguides():
    path = os.path.join(DATA_FOLDER, 'audioguides.txt')
    audioguides = []
    lines = read_file_lines(path)
    for line in lines:
        parts = line.split('|')
        if len(parts) != 8:
            continue
        guide_id, exhibit_number, title, language, duration, script, narrator, created_by = parts
        try:
            audioguides.append({
                'guide_id': int(guide_id),
                'exhibit_number': int(exhibit_number),
                'title': title,
                'language': language,
                'duration': int(duration),
                'script': script,
                'narrator': narrator,
                'created_by': created_by
            })
        except:
            continue
    return audioguides

# Tickets

def get_tickets():
    path = os.path.join(DATA_FOLDER, 'tickets.txt')
    tickets = []
    lines = read_file_lines(path)
    for line in lines:
        parts = line.split('|')
        if len(parts) != 10:
            continue
        (ticket_id, username, ticket_type, visit_date, visit_time, number_of_tickets, price,
         visitor_name, visitor_email, purchase_date) = parts
        try:
            tickets.append({
                'ticket_id': int(ticket_id),
                'username': username,
                'ticket_type': ticket_type,
                'visit_date': visit_date,
                'visit_time': visit_time,
                'number_of_tickets': int(number_of_tickets),
                'price': float(price),
                'visitor_name': visitor_name,
                'visitor_email': visitor_email,
                'purchase_date': purchase_date
            })
        except:
            continue
    return tickets

def save_tickets(tickets):
    path = os.path.join(DATA_FOLDER, 'tickets.txt')
    lines = []
    for t in tickets:
        line = f"{t['ticket_id']}|{t['username']}|{t['ticket_type']}|{t['visit_date']}|{t['visit_time']}|{t['number_of_tickets']}|{t['price']}|{t['visitor_name']}|{t['visitor_email']}|{t['purchase_date']}"
        lines.append(line)
    return write_file_lines(path, lines)

# Events

def get_events():
    path = os.path.join(DATA_FOLDER, 'events.txt')
    events = []
    lines = read_file_lines(path)
    for line in lines:
        parts = line.split('|')
        if len(parts) != 9:
            continue
        event_id, title, date, time, event_type, speaker, capacity, description, created_by = parts
        try:
            events.append({
                'event_id': int(event_id),
                'title': title,
                'date': date,
                'time': time,
                'event_type': event_type,
                'speaker': speaker,
                'capacity': int(capacity),
                'description': description,
                'created_by': created_by
            })
        except:
            continue
    return events

# Event registrations

def get_event_registrations():
    path = os.path.join(DATA_FOLDER, 'event_registrations.txt')
    registrations = []
    lines = read_file_lines(path)
    for line in lines:
        parts = line.split('|')
        if len(parts) != 4:
            continue
        registration_id, event_id, username, registration_date = parts
        try:
            registrations.append({
                'registration_id': int(registration_id),
                'event_id': int(event_id),
                'username': username,
                'registration_date': registration_date
            })
        except:
            continue
    return registrations

def save_event_registrations(registrations):
    path = os.path.join(DATA_FOLDER, 'event_registrations.txt')
    lines = []
    for r in registrations:
        line = f"{r['registration_id']}|{r['event_id']}|{r['username']}|{r['registration_date']}"
        lines.append(line)
    return write_file_lines(path, lines)

# Routes

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))

@app.route('/dashboard', methods=['GET'])
def dashboard():
    exhibitions = get_exhibitions()
    total_exhibitions = len(exhibitions)
    # Active exhibitions: current date between start_date and end_date (inclusive)
    today = datetime.today().date()
    active_cnt = 0
    for e in exhibitions:
        try:
            sd = datetime.strptime(e['start_date'], '%Y-%m-%d').date()
            ed = datetime.strptime(e['end_date'], '%Y-%m-%d').date()
            if sd <= today <= ed:
                active_cnt += 1
        except:
            continue
    exhibitions_summary = {
        'total_exhibitions': total_exhibitions,
        'active_exhibitions': active_cnt
    }
    user = None  # Optional current user, specification allows optional
    return render_template('dashboard.html', exhibitions_summary=exhibitions_summary, user=user)

@app.route('/artifact_catalog', methods=['GET', 'POST'])
def artifact_catalog():
    artifacts = get_artifacts()
    exhibitions = get_exhibitions()
    exhibition_map = {e['exhibition_id']: e['title'] for e in exhibitions}

    search_query = ""
    filters_applied = False

    if request.method == 'POST':
        search_query = request.form.get('search-artifact', '').strip()
        if search_query:
            filters_applied = True
            # Filter artifacts by search_query case-insensitive match in artifact_name
            artifacts = [a for a in artifacts if search_query.lower() in a['artifact_name'].lower()]

    # prepare artifacts list for template fields as per spec
    artifacts_for_display = []
    for a in artifacts:
        exhibition_title = exhibition_map.get(a['exhibition_id'], '')
        artifacts_for_display.append({
            'artifact_id': a['artifact_id'],
            'artifact_name': a['artifact_name'],
            'period': a['period'],
            'origin': a['origin'],
            'exhibition_title': exhibition_title
        })

    return render_template('artifact_catalog.html', artifacts=artifacts_for_display, search_query=search_query, filters_applied=filters_applied)

@app.route('/exhibitions', methods=['GET', 'POST'])
def exhibitions_list():
    filter_type = ""
    exhibitions = get_exhibitions()
    filter_type = ""

    if request.method == 'POST':
        filter_type = request.form.get('filter-exhibition-type', '').strip()
        if filter_type:
            exhibitions = [e for e in exhibitions if e['exhibition_type'] == filter_type]

    exhibitions_for_display = []
    galleries_dict = get_galleries_dict()

    for e in exhibitions:
        gallery_name = galleries_dict.get(e['gallery_id'], {}).get('gallery_name', '')
        status = 'Active'
        # Determine status based on dates (active if current date within start and end)
        try:
            today = datetime.today().date()
            start_date = datetime.strptime(e['start_date'], '%Y-%m-%d').date()
            end_date = datetime.strptime(e['end_date'], '%Y-%m-%d').date()
            if start_date <= today <= end_date:
                status = 'Active'
            else:
                status = 'Inactive'
        except:
            status = 'Inactive'

        exhibitions_for_display.append({
            'exhibition_id': e['exhibition_id'],
            'title': e['title'],
            'exhibition_type': e['exhibition_type'],
            'start_date': e['start_date'],
            'end_date': e['end_date'],
            'gallery_name': gallery_name,
            'status': status
        })

    return render_template('exhibitions.html', exhibitions=exhibitions_for_display, filter_type=filter_type)

@app.route('/exhibition/<int:exhibition_id>', methods=['GET'])
def exhibition_details(exhibition_id):
    exhibitions = get_exhibitions()
    exhibition = next((e for e in exhibitions if e['exhibition_id'] == exhibition_id), None)
    if not exhibition:
        # Exhibition not found, show 404 or redirect
        return "Exhibition not found", 404

    artifacts = get_artifacts()
    related_artifacts = []
    for a in artifacts:
        if a['exhibition_id'] == exhibition_id:
            related_artifacts.append({
                'artifact_id': a['artifact_id'],
                'artifact_name': a['artifact_name'],
                'period': a['period'],
                'origin': a['origin']
            })

    # Prepare exhibition dict as per spec
    exhibition_data = {
        'exhibition_id': exhibition['exhibition_id'],
        'title': exhibition['title'],
        'description': exhibition['description'],
        'start_date': exhibition['start_date'],
        'end_date': exhibition['end_date']
    }

    return render_template('exhibition_details.html', exhibition=exhibition_data, artifacts=related_artifacts)

@app.route('/visitor_tickets', methods=['GET', 'POST'])
def visitor_tickets():
    # We don't have session or login, simulate current user as "visitor_mary" for demonstration
    current_user = 'visitor_mary'
    tickets = get_tickets()
    user_tickets = [t for t in tickets if t['username'] == current_user]

    purchase_status = None

    if request.method == 'POST':
        ticket_type = request.form.get('ticket-type', '').strip()
        visit_date = request.form.get('visit-date', '').strip()
        visit_time = request.form.get('visit-time', '').strip()
        number_of_tickets_str = request.form.get('number-of-tickets', '').strip()
        visitor_name = request.form.get('visitor-name', '').strip()
        visitor_email = request.form.get('visitor-email', '').strip()

        # Validate inputs minimally
        try:
            number_of_tickets = int(number_of_tickets_str)
            if number_of_tickets <= 0:
                raise ValueError
        except:
            purchase_status = 'Failure: Invalid number of tickets.'
            return render_template('visitor_tickets.html', tickets=user_tickets, purchase_status=purchase_status)

        # Simple price logic: set prices per type
        price_map = {'Standard': 15.0, 'VIP': 50.0, 'Student': 10.0}
        price_per_ticket = price_map.get(ticket_type, 15.0)
        total_price = price_per_ticket * number_of_tickets

        # Assign ticket_id
        max_ticket_id = max([t['ticket_id'] for t in tickets], default=0)
        new_ticket_id = max_ticket_id + 1

        purchase_date = datetime.today().strftime('%Y-%m-%d')

        new_ticket = {
            'ticket_id': new_ticket_id,
            'username': current_user,
            'ticket_type': ticket_type,
            'visit_date': visit_date,
            'visit_time': visit_time,
            'number_of_tickets': number_of_tickets,
            'price': total_price,
            'visitor_name': visitor_name,
            'visitor_email': visitor_email,
            'purchase_date': purchase_date
        }

        tickets.append(new_ticket)
        if save_tickets(tickets):
            purchase_status = 'Success: Ticket purchased.'
            user_tickets.append(new_ticket)
        else:
            purchase_status = 'Failure: Could not save ticket purchase.'

    return render_template('visitor_tickets.html', tickets=user_tickets, purchase_status=purchase_status)

@app.route('/virtual_events', methods=['GET', 'POST'])
def virtual_events():
    # Simulate current user
    current_user = 'visitor_mary'
    events = get_events()
    registrations = get_event_registrations()

    registration_message = None

    if request.method == 'POST':
        # Register or cancel registration:
        action = request.form.get('action')
        event_id_str = request.form.get('event_id')
        if not event_id_str or not event_id_str.isdigit():
            registration_message = 'Failure: Invalid event ID.'
        else:
            event_id = int(event_id_str)
            if action == 'register':
                # Already registered?
                already_registered = any(r for r in registrations if r['event_id'] == event_id and r['username'] == current_user)
                if already_registered:
                    registration_message = 'You are already registered for this event.'
                else:
                    max_reg_id = max([r['registration_id'] for r in registrations], default=0)
                    new_reg_id = max_reg_id + 1
                    today_str = datetime.today().strftime('%Y-%m-%d')
                    new_reg = {
                        'registration_id': new_reg_id,
                        'event_id': event_id,
                        'username': current_user,
                        'registration_date': today_str
                    }
                    registrations.append(new_reg)
                    if save_event_registrations(registrations):
                        registration_message = 'Registration successful.'
                    else:
                        registration_message = 'Failed to save registration.'
            elif action == 'cancel':
                reg_to_remove = next((r for r in registrations if r['event_id'] == event_id and r['username'] == current_user), None)
                if reg_to_remove:
                    registrations.remove(reg_to_remove)
                    if save_event_registrations(registrations):
                        registration_message = 'Registration cancelled.'
                    else:
                        registration_message = 'Failed to cancel registration.'
                else:
                    registration_message = 'No existing registration found to cancel.'

    # Prepare events list with registration_status dict
    events_for_display = []
    for e in events:
        reg = next((r for r in registrations if r['event_id'] == e['event_id'] and r['username'] == current_user), None)
        reg_status = {
            'registered': False,
            'registration_id': None
        }
        if reg:
            reg_status['registered'] = True
            reg_status['registration_id'] = reg['registration_id']

        events_for_display.append({
            'event_id': e['event_id'],
            'title': e['title'],
            'date': e['date'],
            'time': e['time'],
            'event_type': e['event_type'],
            'registration_status': reg_status
        })

    return render_template('virtual_events.html', events=events_for_display, registration_message=registration_message)

@app.route('/audio_guides', methods=['GET', 'POST'])
def audio_guides():
    audioguides = get_audioguides()
    filter_language = ""

    if request.method == 'POST':
        filter_language = request.form.get('filter-language', '').strip()
        if filter_language:
            audioguides = [a for a in audioguides if a['language'].lower() == filter_language.lower()]

    audioguides_for_display = []
    for a in audioguides:
        audioguides_for_display.append({
            'guide_id': a['guide_id'],
            'exhibit_number': a['exhibit_number'],
            'title': a['title'],
            'language': a['language'],
            'duration': a['duration']
        })

    return render_template('audio_guides.html', audioguides=audioguides_for_display, filter_language=filter_language)


if __name__ == "__main__":
    app.run(port=5000, debug=True)
