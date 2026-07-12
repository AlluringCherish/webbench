from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

data_dir = 'data'

# Utility functions to read and write pipe-delimited data files

def read_file_lines(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        return []

def parse_pipe_line(line, expected_fields=None):
    parts = line.split('|')
    if expected_fields is not None and len(parts) != expected_fields:
        return None
    return parts

def write_file_lines(filename, lines):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.writelines(line + '\n' for line in lines)
        return True
    except Exception:
        return False

# --- Section 1: Flask Route Implementations ---

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    # Load exhibitions to compute summary
    exhibitions_path = os.path.join(data_dir, 'exhibitions.txt')
    lines = read_file_lines(exhibitions_path)

    total_exhibitions = 0
    active_exhibitions = 0
    # Active means current date between start_date and end_date
    today = datetime.today().date()

    for line in lines:
        data = parse_pipe_line(line, 9)
        if not data:
            continue
        exhibition_id, title, description, gallery_id, exhibition_type, start_date, end_date, curator_name, created_by = data
        total_exhibitions += 1
        try:
            start_dt = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_dt = datetime.strptime(end_date, '%Y-%m-%d').date()
            if start_dt <= today <= end_dt:
                active_exhibitions += 1
        except ValueError:
            # Ignore invalid date formats
            pass

    exhibitions_summary = {
        'total_exhibitions': total_exhibitions,
        'active_exhibitions': active_exhibitions
    }

    # No user context specified
    user = None
    return render_template('dashboard.html', exhibitions_summary=exhibitions_summary, user=user)

@app.route('/artifact_catalog', methods=['GET', 'POST'])
def artifact_catalog():
    search_query = None
    if request.method == 'POST':
        search_query = request.form.get('search_query', '').strip()

    artifacts_path = os.path.join(data_dir, 'artifacts.txt')
    artifact_lines = read_file_lines(artifacts_path)
    artifacts = []

    for line in artifact_lines:
        data = parse_pipe_line(line, 9)
        if not data:
            continue
        artifact_id, artifact_name, period, origin, description, exhibition_id, storage_location, acquisition_date, added_by = data

        # If search_query given, filter by artifact_id or artifact_name case-insensitive
        if search_query:
            if (search_query.lower() not in artifact_name.lower() and
                search_query != artifact_id):
                continue

        artifact = {
            'artifact_id': int(artifact_id),
            'artifact_name': artifact_name,
            'period': period,
            'origin': origin,
            'description': description,
            'exhibition_id': int(exhibition_id),
            'storage_location': storage_location,
            'acquisition_date': acquisition_date,
            'added_by': added_by
        }
        artifacts.append(artifact)

    return render_template('artifact_catalog.html', artifacts=artifacts, search_query=search_query)

@app.route('/exhibitions', methods=['GET', 'POST'])
def exhibitions():
    selected_filter = None
    if request.method == 'POST':
        selected_filter = request.form.get('exhibition_type_filter', '').strip()

    exhibitions_path = os.path.join(data_dir, 'exhibitions.txt')
    exhibition_lines = read_file_lines(exhibitions_path)
    exhibitions = []

    for line in exhibition_lines:
        data = parse_pipe_line(line, 9)
        if not data:
            continue
        exhibition_id, title, description, gallery_id, exhibition_type, start_date, end_date, curator_name, created_by = data

        if selected_filter and exhibition_type != selected_filter:
            continue

        exhibition = {
            'exhibition_id': int(exhibition_id),
            'title': title,
            'description': description,
            'gallery_id': int(gallery_id),
            'exhibition_type': exhibition_type,
            'start_date': start_date,
            'end_date': end_date,
            'curator_name': curator_name,
            'created_by': created_by
        }
        exhibitions.append(exhibition)

    return render_template('exhibitions.html', exhibitions=exhibitions, selected_filter=selected_filter)

@app.route('/exhibition/<int:exhibition_id>')
def exhibition_details(exhibition_id):
    exhibitions_path = os.path.join(data_dir, 'exhibitions.txt')
    exhibition_lines = read_file_lines(exhibitions_path)
    exhibition = None

    for line in exhibition_lines:
        data = parse_pipe_line(line, 9)
        if not data:
            continue
        ex_id, title, description, gallery_id, exhibition_type, start_date, end_date, curator_name, created_by = data
        if int(ex_id) == exhibition_id:
            exhibition = {
                'exhibition_id': int(ex_id),
                'title': title,
                'description': description,
                'gallery_id': int(gallery_id),
                'exhibition_type': exhibition_type,
                'start_date': start_date,
                'end_date': end_date,
                'curator_name': curator_name,
                'created_by': created_by
            }
            break

    if exhibition is None:
        # Exhibition not found, redirect to exhibitions list
        return redirect(url_for('exhibitions'))

    artifacts_path = os.path.join(data_dir, 'artifacts.txt')
    artifact_lines = read_file_lines(artifacts_path)
    artifacts = []
    for line in artifact_lines:
        data = parse_pipe_line(line, 9)
        if not data:
            continue
        artifact_id, artifact_name, period, origin, description, ex_id_str, storage_location, acquisition_date, added_by = data
        if int(ex_id_str) == exhibition_id:
            artifact = {
                'artifact_id': int(artifact_id),
                'artifact_name': artifact_name,
                'period': period,
                'origin': origin,
                'description': description
            }
            artifacts.append(artifact)

    return render_template('exhibition_details.html', exhibition=exhibition, artifacts=artifacts)

@app.route('/visitor_tickets', methods=['GET', 'POST'])
def visitor_tickets():
    tickets_path = os.path.join(data_dir, 'tickets.txt')
    tickets_lines = read_file_lines(tickets_path)
    tickets = []

    purchase_status = None

    # POST handles ticket purchase submission
    if request.method == 'POST':
        ticket_type = request.form.get('ticket_type', '').strip()
        number_of_tickets_str = request.form.get('number_of_tickets', '').strip()
        visitor_name = request.form.get('visitor_name', '').strip()
        visitor_email = request.form.get('visitor_email', '').strip()
        visit_date = request.form.get('visit_date', '').strip()
        visit_time = request.form.get('visit_time', '').strip()

        # Validate inputs minimally
        if (not ticket_type or not number_of_tickets_str.isdigit() or int(number_of_tickets_str) < 1 or
            not visitor_name or not visitor_email or not visit_date or not visit_time):
            purchase_status = 'Invalid input for ticket purchase.'
        else:
            number_of_tickets = int(number_of_tickets_str)
            # Price setting example (could be fixed per ticket type)
            prices = {
                'Standard': 15,
                'Student': 10,
                'Senior': 12,
                'Family': 40,
                'VIP': 50
            }
            price_per_ticket = prices.get(ticket_type, 15)
            total_price = price_per_ticket * number_of_tickets

            # New ticket_id generation
            max_ticket_id = 0
            for line in tickets_lines:
                data = parse_pipe_line(line, 10)
                if not data:
                    continue
                tid_str = data[0]
                try:
                    tid = int(tid_str)
                    if tid > max_ticket_id:
                        max_ticket_id = tid
                except ValueError:
                    continue

            new_ticket_id = max_ticket_id + 1
            # No user context logged in, so username blank
            username = ''
            purchase_date = datetime.today().strftime('%Y-%m-%d')

            new_ticket_record = '|'.join([
                str(new_ticket_id),
                username,
                ticket_type,
                visit_date,
                visit_time,
                str(number_of_tickets),
                str(total_price),
                visitor_name,
                visitor_email,
                purchase_date
            ])

            tickets_lines.append(new_ticket_record)
            success = write_file_lines(tickets_path, tickets_lines)
            if success:
                purchase_status = 'Ticket purchase successful!'
            else:
                purchase_status = 'Failed to save ticket purchase.'

    # Load tickets to display
    tickets = []
    for line in tickets_lines:
        data = parse_pipe_line(line, 10)
        if not data:
            continue
        ticket_id, username, ticket_type, visit_date, visit_time, number_of_tickets, price, visitor_name, visitor_email, purchase_date = data

        ticket = {
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
        }
        tickets.append(ticket)

    return render_template('visitor_tickets.html', tickets=tickets, purchase_status=purchase_status)

@app.route('/virtual_events', methods=['GET', 'POST'])
def virtual_events():
    events_path = os.path.join(data_dir, 'events.txt')
    registrations_path = os.path.join(data_dir, 'event_registrations.txt')

    events_lines = read_file_lines(events_path)
    registrations_lines = read_file_lines(registrations_path)

    registration_status = None

    # POST handles event registration or cancellation
    if request.method == 'POST':
        action = request.form.get('action', '').strip()
        event_id_str = request.form.get('event_id', '').strip()
        username = request.form.get('username', '').strip()  # in reality from user session but here optional

        if not event_id_str.isdigit():
            registration_status = 'Invalid event ID.'
        else:
            event_id = int(event_id_str)

            # Registration handling
            if action == 'register':
                # Check if already registered
                already_registered = any(
                    parse_pipe_line(reg, 4)[1] == str(event_id) and parse_pipe_line(reg, 4)[2] == username
                    for reg in registrations_lines
                )
                if already_registered:
                    registration_status = 'Already registered for this event.'
                else:
                    # New registration_id
                    max_reg_id = 0
                    for reg_line in registrations_lines:
                        data = parse_pipe_line(reg_line, 4)
                        if not data:
                            continue
                        try:
                            rid = int(data[0])
                            if rid > max_reg_id:
                                max_reg_id = rid
                        except ValueError:
                            continue
                    new_reg_id = max_reg_id + 1
                    reg_date = datetime.today().strftime('%Y-%m-%d')
                    new_reg_line = '|'.join([str(new_reg_id), str(event_id), username, reg_date])
                    registrations_lines.append(new_reg_line)
                    success = write_file_lines(registrations_path, registrations_lines)
                    if success:
                        registration_status = 'Successfully registered for event.'
                    else:
                        registration_status = 'Failed to save registration.'

            elif action == 'cancel':
                # Remove registration
                new_regs = []
                canceled = False
                for reg_line in registrations_lines:
                    data = parse_pipe_line(reg_line, 4)
                    if not data:
                        continue
                    rid, eid_str, uname, reg_date = data
                    if eid_str == str(event_id) and uname == username:
                        canceled = True
                        continue
                    new_regs.append(reg_line)
                if canceled:
                    success = write_file_lines(registrations_path, new_regs)
                    if success:
                        registration_status = 'Successfully canceled registration.'
                    else:
                        registration_status = 'Failed to cancel registration.'
                else:
                    registration_status = 'No registration found to cancel.'

            else:
                registration_status = 'Unknown action.'

    # Load all events
    events = []
    for line in events_lines:
        data = parse_pipe_line(line, 9)
        if not data:
            continue
        event_id, title, date, time, event_type, speaker, capacity, description, created_by = data
        event = {
            'event_id': int(event_id),
            'title': title,
            'date': date,
            'time': time,
            'event_type': event_type,
            'speaker': speaker,
            'capacity': int(capacity),
            'description': description,
            'created_by': created_by
        }
        events.append(event)

    # Load registrations
    registrations = []
    for line in registrations_lines:
        data = parse_pipe_line(line, 4)
        if not data:
            continue
        registration_id, event_id_str, username, registration_date = data
        reg = {
            'registration_id': int(registration_id),
            'event_id': int(event_id_str),
            'username': username,
            'registration_date': registration_date
        }
        registrations.append(reg)

    return render_template('virtual_events.html', events=events, registrations=registrations, registration_status=registration_status)

@app.route('/audio_guides', methods=['GET', 'POST'])
def audio_guides():
    selected_language = None
    if request.method == 'POST':
        selected_language = request.form.get('language_filter', '').strip()

    audio_guides_path = os.path.join(data_dir, 'audioguides.txt')
    audio_lines = read_file_lines(audio_guides_path)
    audioguides = []

    for line in audio_lines:
        data = parse_pipe_line(line, 8)
        if not data:
            continue
        guide_id, exhibit_number, title, language, duration, script, narrator, created_by = data

        if selected_language and language != selected_language:
            continue

        guide = {
            'guide_id': int(guide_id),
            'exhibit_number': exhibit_number,
            'title': title,
            'language': language,
            'duration': duration,
            'script': script,
            'narrator': narrator,
            'created_by': created_by
        }
        audioguides.append(guide)

    return render_template('audio_guides.html', audioguides=audioguides, selected_language=selected_language)


if __name__ == '__main__':
    app.run(port=5000, debug=True)
