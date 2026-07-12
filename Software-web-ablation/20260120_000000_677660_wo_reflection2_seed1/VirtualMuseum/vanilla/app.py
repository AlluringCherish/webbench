from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

data_dir = 'data'

# Helper functions to read and write pipe-delimited files

def read_users():
    path = os.path.join(data_dir, 'users.txt')
    users = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                username = line.strip()
                if username:
                    users.append(username)
    except Exception:
        pass
    return users

def read_galleries():
    path = os.path.join(data_dir, 'galleries.txt')
    galleries = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 6:
                    gallery_id, gallery_name, floor, capacity, theme, status = parts
                    galleries.append({
                        'gallery_id': int(gallery_id),
                        'gallery_name': gallery_name,
                        'floor': floor,
                        'capacity': int(capacity),
                        'theme': theme,
                        'status': status
                    })
    except Exception:
        pass
    return galleries


def read_exhibitions():
    path = os.path.join(data_dir, 'exhibitions.txt')
    exhibitions = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 9:
                    exhibition_id, title, description, gallery_id, exhibition_type, start_date, end_date, curator_name, created_by = parts
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
    except Exception:
        pass
    return exhibitions


def read_artifacts():
    path = os.path.join(data_dir, 'artifacts.txt')
    artifacts = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 9:
                    artifact_id, artifact_name, period, origin, description, exhibition_id, storage_location, acquisition_date, added_by = parts
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
    except Exception:
        pass
    return artifacts


def read_audioguides():
    path = os.path.join(data_dir, 'audioguides.txt')
    guides = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 8:
                    guide_id, exhibit_number, title, language, duration, script, narrator, created_by = parts
                    guides.append({
                        'guide_id': int(guide_id),
                        'exhibit_number': exhibit_number,
                        'title': title,
                        'language': language,
                        'duration': duration,
                        'script': script,
                        'narrator': narrator,
                        'created_by': created_by
                    })
    except Exception:
        pass
    return guides


def read_tickets():
    path = os.path.join(data_dir, 'tickets.txt')
    tickets = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 10:
                    ticket_id, username, ticket_type, visit_date, visit_time, number_of_tickets, price, visitor_name, visitor_email, purchase_date = parts
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
    except Exception:
        pass
    return tickets


def write_tickets(tickets):
    path = os.path.join(data_dir, 'tickets.txt')
    try:
        with open(path, 'w', encoding='utf-8') as f:
            for t in tickets:
                line = '|'.join([
                    str(t['ticket_id']),
                    t['username'],
                    t['ticket_type'],
                    t['visit_date'],
                    t['visit_time'],
                    str(t['number_of_tickets']),
                    f"{t['price']:.2f}",
                    t['visitor_name'],
                    t['visitor_email'],
                    t['purchase_date']
                ])
                f.write(line + '\n')
    except Exception:
        pass


def read_events():
    path = os.path.join(data_dir, 'events.txt')
    events = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 9:
                    event_id, title, date, time, event_type, speaker, capacity, description, created_by = parts
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
    except Exception:
        pass
    return events


def read_event_registrations():
    path = os.path.join(data_dir, 'event_registrations.txt')
    regs = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 4:
                    registration_id, event_id, username, registration_date = parts
                    regs.append({
                        'registration_id': int(registration_id),
                        'event_id': int(event_id),
                        'username': username,
                        'registration_date': registration_date
                    })
    except Exception:
        pass
    return regs


def write_event_registrations(registrations):
    path = os.path.join(data_dir, 'event_registrations.txt')
    try:
        with open(path, 'w', encoding='utf-8') as f:
            for r in registrations:
                line = '|'.join([
                    str(r['registration_id']),
                    str(r['event_id']),
                    r['username'],
                    r['registration_date']
                ])
                f.write(line + '\n')
    except Exception:
        pass


# Utility to find next id for tickets and registrations

def get_next_ticket_id(tickets):
    if not tickets:
        return 1
    return max(t['ticket_id'] for t in tickets) + 1

def get_next_registration_id(registrations):
    if not registrations:
        return 1
    return max(r['registration_id'] for r in registrations) + 1


def get_current_user():
    # For simplicity and since no auth specified, user is None
    # This can be enhanced later
    return None


@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    # Read exhibitions
    exhibitions = read_exhibitions()
    total_exhibitions = len(exhibitions)
    # Active exhibitions based on current date inside range
    active_exhibitions = 0
    today = datetime.today().date()
    for ex in exhibitions:
        try:
            sd = datetime.strptime(ex['start_date'], '%Y-%m-%d').date()
            ed = datetime.strptime(ex['end_date'], '%Y-%m-%d').date()
            if sd <= today <= ed:
                active_exhibitions += 1
        except Exception:
            pass

    # Artifacts total count
    artifacts = read_artifacts()
    total_artifacts = len(artifacts)

    # Get user (always None here)
    user = get_current_user()

    exhibitions_summary = {'total': total_exhibitions, 'active': active_exhibitions}
    artifacts_summary = {'total': total_artifacts}

    return render_template('dashboard.html',
                           exhibitions_summary=exhibitions_summary,
                           artifacts_summary=artifacts_summary,
                           user=user)


@app.route('/artifacts', methods=['GET', 'POST'])
def artifact_catalog():
    user = get_current_user()
    artifacts = read_artifacts()

    search_term = ''
    if request.method == 'POST':
        search_term = request.form.get('search_term', '').strip()

    if search_term:
        filtered_artifacts = []
        for art in artifacts:
            if (search_term.lower() in art['artifact_name'].lower() or
                search_term.lower() in art['period'].lower() or
                search_term.lower() in art['origin'].lower() or
                search_term.lower() in art['description'].lower()):
                filtered_artifacts.append(art)
        artifacts = filtered_artifacts

    filters = {'search_term': search_term}

    return render_template('artifact_catalog.html', artifacts=artifacts, filters=filters, user=user)


@app.route('/exhibitions', methods=['GET', 'POST'])
def exhibitions():
    user = get_current_user()
    exhibitions = read_exhibitions()

    selected_type_filter = ''
    if request.method == 'POST':
        selected_type_filter = request.form.get('type_filter', '').strip()

    if selected_type_filter and selected_type_filter != 'All':
        exhibitions = [ex for ex in exhibitions if ex['exhibition_type'] == selected_type_filter]

    return render_template('exhibitions.html',
                           exhibitions=exhibitions,
                           selected_type_filter=selected_type_filter,
                           user=user)


@app.route('/exhibition/<int:exhibition_id>')
def exhibition_details(exhibition_id):
    user = get_current_user()
    exhibitions = read_exhibitions()
    artifacts = read_artifacts()

    exhibition = None
    for ex in exhibitions:
        if ex['exhibition_id'] == exhibition_id:
            exhibition = ex
            break

    if exhibition is None:
        # Exhibition not found, redirect to exhibitions page
        return redirect(url_for('exhibitions'))

    # Filter artifacts in this exhibition
    exhibition_artifacts = [a for a in artifacts if a['exhibition_id'] == exhibition_id]

    return render_template('exhibition_details.html',
                           exhibition=exhibition,
                           artifacts=exhibition_artifacts,
                           user=user)


@app.route('/tickets', methods=['GET', 'POST'])
def visitor_tickets():
    # For tickets, we must have a user; simulate user as None or use a fixed username
    # For implementation, assume user is None, no tickets shown or processed
    # But spec says user (str) optional, so we can simulate as None or some user
    # For this implementation, let's assume user 'visitor_mary' to demonstrate
    user = 'visitor_mary'  # fixed for demo

    tickets = read_tickets()
    user_tickets = [t for t in tickets if t['username'] == user]

    ticket_types = ['Standard', 'Student', 'Senior', 'Family', 'VIP']

    if request.method == 'POST':
        ticket_type = request.form.get('ticket_type', '')
        visit_date = request.form.get('visit_date', '')
        visit_time = request.form.get('visit_time', '')
        number_of_tickets = request.form.get('number_of_tickets', '1')
        visitor_name = request.form.get('visitor_name', '')
        visitor_email = request.form.get('visitor_email', '')

        # Validate required fields
        if (ticket_type in ticket_types and visit_date and visit_time and visitor_name and visitor_email):
            try:
                number_of_tickets_int = int(number_of_tickets)
                if number_of_tickets_int < 1:
                    number_of_tickets_int = 1
            except Exception:
                number_of_tickets_int = 1

            # Price: for simplicity, some prices assigned
            price_map = {
                'Standard': 15,
                'Student': 10,
                'Senior': 12,
                'Family': 40,
                'VIP': 50
            }
            price_base = price_map.get(ticket_type, 15)
            total_price = price_base * number_of_tickets_int

            # Generate ticket_id
            next_ticket_id = get_next_ticket_id(tickets)

            purchase_date = datetime.today().date().isoformat()

            new_ticket = {
                'ticket_id': next_ticket_id,
                'username': user,
                'ticket_type': ticket_type,
                'visit_date': visit_date,
                'visit_time': visit_time,
                'number_of_tickets': number_of_tickets_int,
                'price': float(total_price),
                'visitor_name': visitor_name,
                'visitor_email': visitor_email,
                'purchase_date': purchase_date
            }

            tickets.append(new_ticket)
            write_tickets(tickets)

            return redirect(url_for('visitor_tickets'))

    return render_template('visitor_tickets.html',
                           tickets=user_tickets,
                           ticket_types=ticket_types,
                           user=user)


@app.route('/events', methods=['GET', 'POST'])
def virtual_events():
    user = 'visitor_mary'  # fixed for demo user
    events = read_events()
    registrations = read_event_registrations()

    user_regs = [r for r in registrations if r['username'] == user]

    if request.method == 'POST':
        # Determine if registering or canceling by form data
        form_action = request.form.get('action', '')

        if form_action == 'register':
            event_id_str = request.form.get('event_id', '')
            if event_id_str.isdigit():
                event_id = int(event_id_str)
                # Check if already registered
                already_registered = any(r['username'] == user and r['event_id'] == event_id for r in registrations)
                if not already_registered:
                    new_reg_id = get_next_registration_id(registrations)
                    reg_date = datetime.today().date().isoformat()
                    new_reg = {
                        'registration_id': new_reg_id,
                        'event_id': event_id,
                        'username': user,
                        'registration_date': reg_date
                    }
                    registrations.append(new_reg)
                    write_event_registrations(registrations)

        elif form_action == 'cancel':
            registration_id_str = request.form.get('registration_id', '')
            if registration_id_str.isdigit():
                reg_id = int(registration_id_str)
                registrations = [r for r in registrations if not (r['registration_id'] == reg_id and r['username'] == user)]
                write_event_registrations(registrations)

        return redirect(url_for('virtual_events'))

    return render_template('virtual_events.html',
                           events=events,
                           registrations=user_regs,
                           user=user)


@app.route('/audio-guides', methods=['GET', 'POST'])
def audio_guides():
    user = 'visitor_mary'  # fixed for demo user
    guides = read_audioguides()

    selected_language = ''
    if request.method == 'POST':
        selected_language = request.form.get('language_filter', '').strip()

    if selected_language and selected_language != 'All':
        guides = [g for g in guides if g['language'] == selected_language]

    return render_template('audio_guides.html',
                           audio_guides=guides,
                           selected_language=selected_language,
                           user=user)


if __name__ == '__main__':
    app.run(port=5000, debug=True)
