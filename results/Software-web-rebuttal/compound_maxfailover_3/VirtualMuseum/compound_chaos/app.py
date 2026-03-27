from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

def read_file_lines(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        return []

# Helper to safely parse int
def safe_int(val, default=0):
    try:
        return int(val)
    except Exception:
        return default

# Helper to safely parse float
def safe_float(val, default=0.0):
    try:
        return float(val)
    except Exception:
        return default

# --------- Data Loading Functions ---------

def load_exhibitions():
    # exhibition_id|title|description|gallery_id|exhibition_type|start_date|end_date|curator_name|created_by
    lines = read_file_lines('data/exhibitions.txt')
    exhibitions = []
    for line in lines:
        parts = line.split('|')
        if len(parts) != 9:
            continue
        try:
            exhibitions.append({
                'exhibition_id': safe_int(parts[0]),
                'title': parts[1],
                'description': parts[2],
                'gallery_id': safe_int(parts[3]),
                'exhibition_type': parts[4],
                'start_date': parts[5],
                'end_date': parts[6],
                'curator_name': parts[7],
                'created_by': parts[8]
            })
        except Exception:
            continue
    return exhibitions


def load_artifacts():
    # artifact_id|artifact_name|period|origin|description|exhibition_id|storage_location|acquisition_date|added_by
    lines = read_file_lines('data/artifacts.txt')
    artifacts = []
    for line in lines:
        parts = line.split('|')
        if len(parts) != 9:
            continue
        try:
            artifacts.append({
                'artifact_id': safe_int(parts[0]),
                'artifact_name': parts[1],
                'period': parts[2],
                'origin': parts[3],
                'description': parts[4],
                'exhibition_id': safe_int(parts[5]) if parts[5] else None,
                'storage_location': parts[6],
                'acquisition_date': parts[7],
                'added_by': parts[8]
            })
        except Exception:
            continue
    return artifacts


def load_galleries():
    # gallery_id|gallery_name|floor|capacity|theme|status
    lines = read_file_lines('data/galleries.txt')
    galleries = []
    for line in lines:
        parts = line.split('|')
        if len(parts) != 6:
            continue
        try:
            galleries.append({
                'gallery_id': safe_int(parts[0]),
                'gallery_name': parts[1],
                'floor': parts[2],
                'capacity': safe_int(parts[3]),
                'theme': parts[4],
                'status': parts[5]
            })
        except Exception:
            continue
    return galleries


def load_audioguides():
    # guide_id|exhibit_number|title|language|duration|script|narrator|created_by
    lines = read_file_lines('data/audioguides.txt')
    audioguides = []
    for line in lines:
        parts = line.split('|')
        if len(parts) != 8:
            continue
        try:
            audioguides.append({
                'guide_id': safe_int(parts[0]),
                'exhibit_number': safe_int(parts[1]),
                'title': parts[2],
                'language': parts[3],
                'duration': safe_int(parts[4]),
                'script': parts[5],
                'narrator': parts[6],
                'created_by': parts[7]
            })
        except Exception:
            continue
    return audioguides


def load_tickets():
    # ticket_id|username|ticket_type|visit_date|visit_time|number_of_tickets|price|visitor_name|visitor_email|purchase_date
    lines = read_file_lines('data/tickets.txt')
    tickets = []
    for line in lines:
        parts = line.split('|')
        if len(parts) != 10:
            continue
        try:
            tickets.append({
                'ticket_id': safe_int(parts[0]),
                'username': parts[1],
                'ticket_type': parts[2],
                'visit_date': parts[3],
                'visit_time': parts[4],
                'number_of_tickets': safe_int(parts[5]),
                'price': safe_float(parts[6]),
                'visitor_name': parts[7],
                'visitor_email': parts[8],
                'purchase_date': parts[9]
            })
        except Exception:
            continue
    return tickets


def load_events():
    # event_id|title|date|time|event_type|speaker|capacity|description|created_by
    lines = read_file_lines('data/events.txt')
    events = []
    for line in lines:
        parts = line.split('|')
        if len(parts) != 9:
            continue
        try:
            events.append({
                'event_id': safe_int(parts[0]),
                'title': parts[1],
                'date': parts[2],
                'time': parts[3],
                'event_type': parts[4],
                'speaker': parts[5],
                'capacity': safe_int(parts[6]),
                'description': parts[7],
                'created_by': parts[8]
            })
        except Exception:
            continue
    return events


def load_event_registrations():
    # registration_id|event_id|username|registration_date
    lines = read_file_lines('data/event_registrations.txt')
    registrations = []
    for line in lines:
        parts = line.split('|')
        if len(parts) != 4:
            continue
        try:
            registrations.append({
                'registration_id': safe_int(parts[0]),
                'event_id': safe_int(parts[1]),
                'username': parts[2],
                'registration_date': parts[3]
            })
        except Exception:
            continue
    return registrations


def save_tickets(tickets):
    # Save tickets list to file
    lines = []
    for t in tickets:
        # Fields: ticket_id|username|ticket_type|visit_date|visit_time|number_of_tickets|price|visitor_name|visitor_email|purchase_date
        line = f"{t['ticket_id']}|{t['username']}|{t['ticket_type']}|{t['visit_date']}|{t['visit_time']}|{t['number_of_tickets']}|{t['price']}|{t['visitor_name']}|{t['visitor_email']}|{t['purchase_date']}"
        lines.append(line)
    try:
        with open('data/tickets.txt', 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
    except Exception:
        pass


def save_event_registrations(registrations):
    # Save registrations list to file
    lines = []
    for r in registrations:
        # Fields: registration_id|event_id|username|registration_date
        line = f"{r['registration_id']}|{r['event_id']}|{r['username']}|{r['registration_date']}"
        lines.append(line)
    try:
        with open('data/event_registrations.txt', 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
    except Exception:
        pass


# -------------------------------------

@app.route('/')
def root():
    # Redirect to /dashboard
    return redirect(url_for('dashboard_page'))


@app.route('/dashboard')
def dashboard_page():
    exhibitions = load_exhibitions()
    total_exhibitions = len(exhibitions)
    # Active defined as current date between start_date and end_date inclusive
    active_exhibitions = 0
    try:
        today = datetime.utcnow().date()
    except Exception:
        today = None

    for ex in exhibitions:
        try:
            start = datetime.strptime(ex['start_date'], '%Y-%m-%d').date()
            end = datetime.strptime(ex['end_date'], '%Y-%m-%d').date()
            if today and start <= today <= end:
                active_exhibitions += 1
        except Exception:
            continue

    return render_template('dashboard.html', total_exhibitions=total_exhibitions, active_exhibitions=active_exhibitions)


@app.route('/artifact-catalog')
def artifact_catalog_page():
    artifacts = load_artifacts()
    exhibitions = load_exhibitions()
    exhibition_map = {ex['exhibition_id']: ex['title'] for ex in exhibitions}

    # Prepare artifact dicts for context with specified keys
    artifact_list = []
    for a in artifacts:
        ex_title = exhibition_map.get(a['exhibition_id']) if a['exhibition_id'] else None
        artifact_list.append({
            'artifact_id': a['artifact_id'],
            'artifact_name': a['artifact_name'],
            'period': a['period'],
            'origin': a['origin'],
            'exhibition': ex_title
        })

    return render_template('artifact_catalog.html', artifacts=artifact_list, search_query='', filters={})


@app.route('/artifact-catalog/filter', methods=['POST'])
def apply_artifact_filter():
    artifacts = load_artifacts()
    exhibitions = load_exhibitions()
    exhibition_map = {ex['exhibition_id']: ex['title'] for ex in exhibitions}

    search_query = request.form.get('search_artifact', '').strip()

    filtered_artifacts = []
    for a in artifacts:
        if search_query.lower() in a['artifact_name'].lower():
            ex_title = exhibition_map.get(a['exhibition_id']) if a['exhibition_id'] else None
            filtered_artifacts.append({
                'artifact_id': a['artifact_id'],
                'artifact_name': a['artifact_name'],
                'period': a['period'],
                'origin': a['origin'],
                'exhibition': ex_title
            })

    filters = {'search_artifact': search_query}

    return render_template('artifact_catalog.html', artifacts=filtered_artifacts, search_query=search_query, filters=filters)


@app.route('/exhibitions')
def exhibitions_page():
    exhibitions = load_exhibitions()
    filter_type = request.args.get('filter_type', '')

    filtered_exhibitions = []
    if filter_type and filter_type.strip():
        for ex in exhibitions:
            if ex['exhibition_type'].lower() == filter_type.strip().lower():
                filtered_exhibitions.append(ex)
    else:
        filtered_exhibitions = exhibitions

    return render_template('exhibitions.html', exhibitions=filtered_exhibitions, filter_type=filter_type)


@app.route('/exhibitions/filter', methods=['POST'])
def apply_exhibition_filter():
    filter_type = request.form.get('filter-exhibition-type', '').strip()
    exhibitions = load_exhibitions()

    filtered_exhibitions = []
    if filter_type:
        for ex in exhibitions:
            if ex['exhibition_type'].lower() == filter_type.lower():
                filtered_exhibitions.append(ex)
    else:
        filtered_exhibitions = exhibitions

    return render_template('exhibitions.html', exhibitions=filtered_exhibitions, filter_type=filter_type)


@app.route('/exhibition/<int:exhibition_id>')
def exhibition_details_page(exhibition_id: int):
    exhibitions = load_exhibitions()
    artifacts = load_artifacts()

    exhibition = None
    for ex in exhibitions:
        if ex['exhibition_id'] == exhibition_id:
            exhibition = ex
            break

    if not exhibition:
        # Not found, render with empty data
        exhibition = {
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

    # Collect artifacts belonging to this exhibition
    artifacts_list = []
    for a in artifacts:
        if a['exhibition_id'] == exhibition_id:
            artifacts_list.append({
                'artifact_id': a['artifact_id'],
                'artifact_name': a['artifact_name'],
                'period': a['period'],
                'origin': a['origin'],
                'description': a['description'],
                'exhibition_id': a['exhibition_id'],
                'storage_location': a['storage_location'],
                'acquisition_date': a['acquisition_date'],
                'added_by': a['added_by']
            })

    return render_template('exhibition_details.html', exhibition=exhibition, artifacts=artifacts_list)


@app.route('/visitor-tickets')
def visitor_tickets_page():
    # For demonstration, use a default username
    username = request.args.get('username', 'visitor_mary')
    tickets = load_tickets()

    user_tickets = []
    for t in tickets:
        if t['username'] == username:
            user_tickets.append(t)

    return render_template('visitor_tickets.html', tickets=user_tickets, username=username)


@app.route('/visitor-tickets/purchase', methods=['POST'])
def purchase_ticket():
    username = request.form.get('username', 'visitor_mary').strip()
    ticket_type = request.form.get('ticket_type', '').strip()
    number_of_tickets_raw = request.form.get('number_of_tickets', '0')

    purchase_success = False
    purchase_error = None

    # Minimal validation
    try:
        number_of_tickets = int(number_of_tickets_raw)
    except Exception:
        number_of_tickets = 0

    if not ticket_type:
        purchase_error = 'Ticket type is required.'
    elif number_of_tickets <= 0:
        purchase_error = 'Number of tickets must be positive.'

    visit_date = request.form.get('visit_date', '').strip()
    visit_time = request.form.get('visit_time', '').strip()
    visitor_name = request.form.get('visitor_name', '').strip()
    visitor_email = request.form.get('visitor_email', '').strip()

    # Use fixed prices for demonstration (could be improved if pricing data provided)
    ticket_prices = {
        'Standard': 15.0,
        'VIP': 25.0,
        'Student': 7.5
    }

    price_per_ticket = ticket_prices.get(ticket_type, 10.0)

    # Validate required fields
    if not visit_date:
        purchase_error = 'Visit date is required.'
    if not visit_time:
        purchase_error = 'Visit time is required.'
    if not visitor_name:
        purchase_error = 'Visitor name is required.'
    if not visitor_email:
        purchase_error = 'Visitor email is required.'

    if purchase_error is None:
        # Load existing tickets
        tickets = load_tickets()
        max_ticket_id = max([t['ticket_id'] for t in tickets], default=0)
        new_ticket_id = max_ticket_id + 1

        purchase_date_str = datetime.utcnow().strftime('%Y-%m-%d')
        price = price_per_ticket * number_of_tickets

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
            'purchase_date': purchase_date_str
        }

        tickets.append(new_ticket)
        try:
            save_tickets(tickets)
            purchase_success = True
        except Exception:
            purchase_error = 'Failed to save ticket data.'

    # Load updated tickets for user
    all_tickets = load_tickets()
    user_tickets = [t for t in all_tickets if t['username'] == username]

    return render_template('visitor_tickets.html', tickets=user_tickets, username=username,
                           purchase_success=purchase_success, purchase_error=purchase_error)


@app.route('/virtual-events')
def virtual_events_page():
    username = request.args.get('username', 'visitor_mary')
    events = load_events()
    registrations = load_event_registrations()

    user_registrations = [r for r in registrations if r['username'] == username]

    return render_template('virtual_events.html', events=events, registrations=user_registrations, username=username)


@app.route('/virtual-events/register/<int:event_id>', methods=['POST'])
def register_event(event_id):
    username = request.form.get('username', 'visitor_mary')
    registrations = load_event_registrations()
    events = load_events()

    # Check if event exists
    event = next((e for e in events if e['event_id'] == event_id), None)
    if not event:
        # redirect back with no changes
        return redirect(url_for('virtual_events_page'))

    # Check if user is already registered
    already_registered = any(r['event_id'] == event_id and r['username'] == username for r in registrations)
    if not already_registered:
        max_reg_id = max([r['registration_id'] for r in registrations], default=0)
        new_reg_id = max_reg_id + 1
        reg_date = datetime.utcnow().strftime('%Y-%m-%d')
        new_registration = {
            'registration_id': new_reg_id,
            'event_id': event_id,
            'username': username,
            'registration_date': reg_date
        }
        registrations.append(new_registration)
        try:
            save_event_registrations(registrations)
        except Exception:
            pass

    return redirect(url_for('virtual_events_page'))


@app.route('/virtual-events/cancel/<int:registration_id>', methods=['POST'])
def cancel_registration(registration_id):
    username = request.form.get('username', 'visitor_mary')
    registrations = load_event_registrations()

    # Remove registration with matching id and username
    registrations = [r for r in registrations if not (r['registration_id'] == registration_id and r['username'] == username)]

    try:
        save_event_registrations(registrations)
    except Exception:
        pass

    return redirect(url_for('virtual_events_page'))


@app.route('/audio-guides')
def audio_guides_page():
    audioguides = load_audioguides()
    filter_language = request.args.get('filter_language', '').strip()

    if filter_language:
        filtered_guides = [g for g in audioguides if g['language'].lower() == filter_language.lower()]
    else:
        filtered_guides = audioguides

    return render_template('audio_guides.html', audioguides=filtered_guides, filter_language=filter_language)


@app.route('/audio-guides/filter', methods=['POST'])
def apply_language_filter():
    filter_language = request.form.get('filter-language', '').strip()
    audioguides = load_audioguides()

    if filter_language:
        filtered_guides = [g for g in audioguides if g['language'].lower() == filter_language.lower()]
    else:
        filtered_guides = audioguides

    return render_template('audio_guides.html', audioguides=filtered_guides, filter_language=filter_language)


if __name__ == '__main__':
    app.run(port=5000, debug=True)
