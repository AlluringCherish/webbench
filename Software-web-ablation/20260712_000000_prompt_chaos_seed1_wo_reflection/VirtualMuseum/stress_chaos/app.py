from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

data_dir = 'data'

# Utility functions to read and write data files

def read_file_lines(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        return []


def write_file_lines(filename, lines):
    with open(filename, 'w', encoding='utf-8') as f:
        for line in lines:
            f.write(line + '\n')


def parse_exhibitions():
    path = os.path.join(data_dir, 'exhibitions.txt')
    raw = read_file_lines(path)
    exhibitions = []
    for line in raw:
        parts = line.split('|')
        if len(parts) != 9:
            continue
        ex = {
            'exhibition_id': int(parts[0]),
            'title': parts[1],
            'description': parts[2],
            'gallery_id': int(parts[3]),
            'exhibition_type': parts[4],
            'start_date': parts[5],
            'end_date': parts[6],
            'curator_name': parts[7],
            'created_by': parts[8]
        }
        exhibitions.append(ex)
    return exhibitions


def save_exhibitions(exhibitions):
    lines = []
    for ex in exhibitions:
        line = f"{ex['exhibition_id']}|{ex['title']}|{ex['description']}|{ex['gallery_id']}|{ex['exhibition_type']}|{ex['start_date']}|{ex['end_date']}|{ex['curator_name']}|{ex['created_by']}"
        lines.append(line)
    write_file_lines(os.path.join(data_dir, 'exhibitions.txt'), lines)


def parse_artifacts():
    path = os.path.join(data_dir, 'artifacts.txt')
    raw = read_file_lines(path)
    artifacts = []
    for line in raw:
        parts = line.split('|')
        if len(parts) != 9:
            continue
        art = {
            'artifact_id': int(parts[0]),
            'artifact_name': parts[1],
            'period': parts[2],
            'origin': parts[3],
            'description': parts[4],
            'exhibition_id': int(parts[5]),
            'storage_location': parts[6],
            'acquisition_date': parts[7],
            'added_by': parts[8]
        }
        artifacts.append(art)
    return artifacts


def save_artifacts(artifacts):
    lines = []
    for art in artifacts:
        line = f"{art['artifact_id']}|{art['artifact_name']}|{art['period']}|{art['origin']}|{art['description']}|{art['exhibition_id']}|{art['storage_location']}|{art['acquisition_date']}|{art['added_by']}"
        lines.append(line)
    write_file_lines(os.path.join(data_dir, 'artifacts.txt'), lines)


def parse_tickets():
    path = os.path.join(data_dir, 'tickets.txt')
    raw = read_file_lines(path)
    tickets = []
    for line in raw:
        parts = line.split('|')
        if len(parts) != 10:
            continue
        t = {
            'ticket_id': int(parts[0]),
            'username': parts[1],
            'ticket_type': parts[2],
            'visit_date': parts[3],
            'visit_time': parts[4],
            'number_of_tickets': int(parts[5]),
            'price': parts[6],
            'visitor_name': parts[7],
            'visitor_email': parts[8],
            'purchase_date': parts[9]
        }
        tickets.append(t)
    return tickets


def save_tickets(tickets):
    lines = []
    for t in tickets:
        line = f"{t['ticket_id']}|{t['username']}|{t['ticket_type']}|{t['visit_date']}|{t['visit_time']}|{t['number_of_tickets']}|{t['price']}|{t['visitor_name']}|{t['visitor_email']}|{t['purchase_date']}"
        lines.append(line)
    write_file_lines(os.path.join(data_dir, 'tickets.txt'), lines)


def parse_events():
    path = os.path.join(data_dir, 'events.txt')
    raw = read_file_lines(path)
    events = []
    for line in raw:
        parts = line.split('|')
        if len(parts) != 9:
            continue
        e = {
            'event_id': int(parts[0]),
            'title': parts[1],
            'date': parts[2],
            'time': parts[3],
            'event_type': parts[4],
            'speaker': parts[5],
            'capacity': int(parts[6]),
            'description': parts[7],
            'created_by': parts[8]
        }
        events.append(e)
    return events


def save_events(events):
    lines = []
    for e in events:
        line = f"{e['event_id']}|{e['title']}|{e['date']}|{e['time']}|{e['event_type']}|{e['speaker']}|{e['capacity']}|{e['description']}|{e['created_by']}"
        lines.append(line)
    write_file_lines(os.path.join(data_dir, 'events.txt'), lines)


def parse_event_registrations():
    path = os.path.join(data_dir, 'event_registrations.txt')
    raw = read_file_lines(path)
    regs = []
    for line in raw:
        parts = line.split('|')
        if len(parts) != 4:
            continue
        r = {
            'registration_id': int(parts[0]),
            'event_id': int(parts[1]),
            'username': parts[2],
            'registration_date': parts[3]
        }
        regs.append(r)
    return regs


def save_event_registrations(regs):
    lines = []
    for r in regs:
        line = f"{r['registration_id']}|{r['event_id']}|{r['username']}|{r['registration_date']}"
        lines.append(line)
    write_file_lines(os.path.join(data_dir, 'event_registrations.txt'), lines)


def parse_audioguides():
    path = os.path.join(data_dir, 'audioguides.txt')
    raw = read_file_lines(path)
    guides = []
    for line in raw:
        parts = line.split('|')
        if len(parts) != 8:
            continue
        g = {
            'guide_id': int(parts[0]),
            'exhibit_number': parts[1],
            'title': parts[2],
            'language': parts[3],
            'duration': parts[4],
            'script': parts[5],
            'narrator': parts[6],
            'created_by': parts[7]
        }
        guides.append(g)
    return guides


def save_audioguides(guides):
    lines = []
    for g in guides:
        line = f"{g['guide_id']}|{g['exhibit_number']}|{g['title']}|{g['language']}|{g['duration']}|{g['script']}|{g['narrator']}|{g['created_by']}"
        lines.append(line)
    write_file_lines(os.path.join(data_dir, 'audioguides.txt'), lines)


def parse_users():
    path = os.path.join(data_dir, 'users.txt')
    raw = read_file_lines(path)
    users = [line for line in raw]
    return users


# Route Implementations

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    exhibitions = parse_exhibitions()
    artifacts = parse_artifacts()
    return render_template('dashboard.html', exhibitions=exhibitions, artifacts=artifacts)


@app.route('/artifacts', methods=['GET', 'POST'])
def artifact_catalog():
    artifacts = parse_artifacts()
    search_query = ''
    filtered_artifacts = artifacts

    if request.method == 'POST':
        search_query = request.form.get('search_query', '').strip()
        if search_query:
            lower_query = search_query.lower()
            filtered_artifacts = [a for a in artifacts if lower_query in a['artifact_name'].lower() or lower_query in str(a['artifact_id'])]
        else:
            filtered_artifacts = artifacts

    return render_template('artifact_catalog.html', artifacts=artifacts, search_query=search_query, filtered_artifacts=filtered_artifacts)


@app.route('/exhibitions', methods=['GET', 'POST'])
def exhibitions():
    exhibitions_list = parse_exhibitions()
    filter_type = None

    if request.method == 'POST':
        filter_type = request.form.get('filter_type', '').strip()

    if filter_type:
        filtered = [ex for ex in exhibitions_list if ex['exhibition_type'].lower() == filter_type.lower()]
        exhibitions_list = filtered

    return render_template('exhibitions.html', exhibitions=exhibitions_list, filter_type=filter_type)


@app.route('/exhibition/<int:exhibition_id>')
def exhibition_details(exhibition_id):
    exhibitions_list = parse_exhibitions()
    artifacts_list = parse_artifacts()

    exhibition = None
    for ex in exhibitions_list:
        if ex['exhibition_id'] == exhibition_id:
            exhibition = ex
            break

    if not exhibition:
        # Exhibition not found, redirect to exhibitions page
        return redirect(url_for('exhibitions'))

    artifacts_in_exhibition = [a for a in artifacts_list if a['exhibition_id'] == exhibition_id]

    return render_template('exhibition_details.html', exhibition=exhibition, artifacts=artifacts_in_exhibition)


@app.route('/tickets', methods=['GET', 'POST'])
def visitor_tickets():
    tickets_list = parse_tickets()
    ticket_types = ['Standard', 'VIP', 'Student']  # Assumed ticket types
    purchase_status = None

    if request.method == 'POST':
        # Simulate purchasing tickets
        username = request.form.get('username', '').strip()
        ticket_type = request.form.get('ticket_type', '').strip()
        visit_date = request.form.get('visit_date', '').strip()
        visit_time = request.form.get('visit_time', '').strip()
        number_of_tickets_str = request.form.get('number_of_tickets', '0').strip()
        visitor_name = request.form.get('visitor_name', '').strip()
        visitor_email = request.form.get('visitor_email', '').strip()

        try:
            number_of_tickets = int(number_of_tickets_str)
        except ValueError:
            number_of_tickets = 0

        if not (username and ticket_type and visit_date and visit_time and number_of_tickets > 0 and visitor_name and visitor_email):
            purchase_status = 'Missing or invalid fields for purchasing tickets.'
        else:
            # Create new ticket entry
            new_ticket_id = 1
            if tickets_list:
                new_ticket_id = max(t['ticket_id'] for t in tickets_list) + 1

            # Pricing logic placeholder (here we just use a fixed price)
            price_map = {'Standard': '30', 'VIP': '50', 'Student': '10'}
            price = price_map.get(ticket_type, '30')

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
            tickets_list.append(new_ticket)
            save_tickets(tickets_list)
            purchase_status = 'Tickets purchased successfully.'

    return render_template('visitor_tickets.html', tickets=tickets_list, ticket_types=ticket_types, purchase_status=purchase_status)


@app.route('/events', methods=['GET', 'POST'])
def virtual_events():
    events = parse_events()
    registrations = parse_event_registrations()
    user_registrations = []

    if request.method == 'POST':
        action = request.form.get('action', '').strip()
        username = request.form.get('username', '').strip()
        event_id_str = request.form.get('event_id', '').strip()

        try:
            event_id = int(event_id_str)
        except ValueError:
            event_id = None

        if action == 'register' and event_id and username:
            # Register the user for the event if not already registered
            already_registered = any(
                r['username'] == username and r['event_id'] == event_id for r in registrations
            )
            if not already_registered:
                new_reg_id = 1
                if registrations:
                    new_reg_id = max(r['registration_id'] for r in registrations) + 1
                new_registration = {
                    'registration_id': new_reg_id,
                    'event_id': event_id,
                    'username': username,
                    'registration_date': datetime.now().strftime('%Y-%m-%d')
                }
                registrations.append(new_registration)
                save_event_registrations(registrations)

        elif action == 'cancel' and event_id and username:
            # Cancel registration if exists
            registrations = [r for r in registrations if not (r['event_id'] == event_id and r['username'] == username)]
            save_event_registrations(registrations)

    # For demonstration, user registrations extracted by username from form or empty
    user_registrations = registrations  # Show all registrations (no logged user context specified)

    return render_template('virtual_events.html', events=events, registrations=registrations, user_registrations=user_registrations)


@app.route('/audio-guides', methods=['GET', 'POST'])
def audio_guides():
    audioguides = parse_audioguides()
    filter_language = None

    if request.method == 'POST':
        filter_language = request.form.get('filter_language', '').strip()

    if filter_language:
        filtered = [g for g in audioguides if g['language'].lower() == filter_language.lower()]
        audioguides = filtered

    return render_template('audio_guides.html', audioguides=audioguides, filter_language=filter_language)


if __name__ == '__main__':
    app.run(port=5000, debug=True)
