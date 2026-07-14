from flask import Flask, render_template, request, redirect, url_for
import os
import datetime

app = Flask(__name__)

DATA_DIR = 'data'

# Utility functions for file reading/writing

def read_pipe_file(filename):
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        return []
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.read().strip().split('\n')
    data = [line.split('|') for line in lines if line.strip() != '']
    return data

def write_pipe_file(filename, rows):
    path = os.path.join(DATA_DIR, filename)
    with open(path, 'w', encoding='utf-8') as f:
        for row in rows:
            f.write('|'.join(str(item) for item in row) + '\n')

# Reading exhibition summaries

def get_exhibitions():
    exhibitions_raw = read_pipe_file('exhibitions.txt')
    exhibitions = []
    for r in exhibitions_raw:
        if len(r) < 9:
            continue
        exhibitions.append({
            'exhibition_id': int(r[0]),
            'title': r[1],
            'description': r[2],
            'gallery_id': int(r[3]),
            'exhibition_type': r[4],
            'start_date': r[5],
            'end_date': r[6],
            'curator_name': r[7],
            'created_by': r[8]
        })
    return exhibitions

def get_active_exhibitions_count():
    exhibitions = get_exhibitions()
    today = datetime.date.today().isoformat()
    count = 0
    for ex in exhibitions:
        if ex['start_date'] <= today <= ex['end_date']:
            count += 1
    return count

def get_galleries():
    galleries_raw = read_pipe_file('galleries.txt')
    galleries = []
    for r in galleries_raw:
        if len(r) < 6:
            continue
        galleries.append({
            'gallery_id': int(r[0]),
            'gallery_name': r[1],
            'floor': r[2],
            'capacity': r[3],
            'theme': r[4],
            'status': r[5]
        })
    return galleries

def get_artifacts():
    artifacts_raw = read_pipe_file('artifacts.txt')
    artifacts = []
    exhibitions = get_exhibitions()
    exhibition_dict = {ex['exhibition_id']: ex for ex in exhibitions}
    for r in artifacts_raw:
        if len(r) < 9:
            continue
        exhibition_title = exhibition_dict.get(int(r[5]), {}).get('title', '')
        artifacts.append({
            'artifact_id': int(r[0]),
            'artifact_name': r[1],
            'period': r[2],
            'origin': r[3],
            'description': r[4],
            'exhibition_id': int(r[5]),
            'exhibition_title': exhibition_title,
            'storage_location': r[6],
            'acquisition_date': r[7],
            'added_by': r[8]
        })
    return artifacts

def get_artifacts_filtered(search_term):
    if not search_term:
        return get_artifacts()
    search_term_lower = search_term.lower()
    results = []
    for artifact in get_artifacts():
        if search_term_lower in str(artifact['artifact_id']).lower() or search_term_lower in artifact['artifact_name'].lower():
            results.append(artifact)
    return results

def get_exhibition_by_id(exhibition_id):
    exhibitions = get_exhibitions()
    for ex in exhibitions:
        if ex['exhibition_id'] == exhibition_id:
            return ex
    return None

def get_artifacts_by_exhibition(exhibition_id):
    artifacts = get_artifacts()
    return [a for a in artifacts if a['exhibition_id'] == exhibition_id]

def get_tickets(username):
    tickets_raw = read_pipe_file('tickets.txt')
    tickets = []
    for r in tickets_raw:
        if len(r) < 10:
            continue
        if r[1] == username:
            tickets.append({
                'ticket_id': int(r[0]),
                'username': r[1],
                'ticket_type': r[2],
                'visit_date': r[3],
                'visit_time': r[4],
                'number_of_tickets': int(r[5]),
                'price': r[6],
                'visitor_name': r[7],
                'visitor_email': r[8],
                'purchase_date': r[9]
            })
    return tickets

def get_events():
    events_raw = read_pipe_file('events.txt')
    events = []
    for r in events_raw:
        if len(r) < 9:
            continue
        events.append({
            'event_id': int(r[0]),
            'title': r[1],
            'date': r[2],
            'time': r[3],
            'event_type': r[4],
            'speaker': r[5],
            'capacity': int(r[6]),
            'description': r[7],
            'created_by': r[8]
        })
    return events

def get_event_registrations():
    registrations_raw = read_pipe_file('event_registrations.txt')
    registrations = []
    for r in registrations_raw:
        if len(r) < 4:
            continue
        registrations.append({
            'registration_id': int(r[0]),
            'event_id': int(r[1]),
            'username': r[2],
            'registration_date': r[3]
        })
    return registrations

# For demonstration, setting a mock current user
CURRENT_USER = 'visitor_mary'

@app.route('/')
def root():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    exhibitions = get_exhibitions()
    total_exhibitions = len(exhibitions)
    active_exhibitions = get_active_exhibitions_count()
    return render_template('dashboard.html', total_exhibitions=total_exhibitions, active_exhibitions=active_exhibitions)

@app.route('/artifacts', methods=['GET'])
def artifacts_get():
    artifacts = get_artifacts()
    return render_template('artifact_catalog.html', artifacts=artifacts)

@app.route('/artifacts/search', methods=['POST'])
def artifacts_search():
    search_term = request.form.get('search-artifact', '')
    filtered_artifacts = get_artifacts_filtered(search_term)
    return render_template('artifact_catalog.html', artifacts=filtered_artifacts)

@app.route('/exhibitions', methods=['GET'])
def exhibitions_get():
    exhibitions = get_exhibitions()
    galleries = get_galleries()
    gallery_map = {g['gallery_id']: g['gallery_name'] for g in galleries}
    today = datetime.date.today().isoformat()
    # Enrich exhibitions with gallery_name and status
    for e in exhibitions:
        e['gallery_name'] = gallery_map.get(e['gallery_id'], 'Unknown Gallery')
        try:
            if e['start_date'] <= today <= e['end_date']:
                e['status'] = 'Active'
            else:
                e['status'] = 'Inactive'
        except Exception:
            e['status'] = 'Inactive'
    return render_template('exhibitions.html', exhibitions=exhibitions)

@app.route('/exhibitions/filter', methods=['POST'])
def exhibitions_filter():
    filter_type = request.form.get('filter-exhibition-type')
    exhibitions = get_exhibitions()
    galleries = get_galleries()
    gallery_map = {g['gallery_id']: g['gallery_name'] for g in galleries}
    today = datetime.date.today().isoformat()
    filtered = []
    for e in exhibitions:
        if filter_type and e['exhibition_type'] != filter_type:
            continue
        e['gallery_name'] = gallery_map.get(e['gallery_id'], 'Unknown Gallery')
        try:
            if e['start_date'] <= today <= e['end_date']:
                e['status'] = 'Active'
            else:
                e['status'] = 'Inactive'
        except Exception:
            e['status'] = 'Inactive'
        filtered.append(e)
    return render_template('exhibitions.html', exhibitions=filtered)

@app.route('/exhibitions/<int:exhibition_id>', methods=['GET'])
def exhibition_details(exhibition_id):
    exhibition = get_exhibition_by_id(exhibition_id)
    if not exhibition:
        return "Exhibition not found", 404
    artifacts = get_artifacts_by_exhibition(exhibition_id)
    return render_template('exhibition_details.html', exhibition=exhibition, artifacts=artifacts)

@app.route('/tickets', methods=['GET'])
def tickets_get():
    tickets = get_tickets(CURRENT_USER)
    return render_template('visitor_tickets.html', tickets=tickets)

@app.route('/tickets/purchase', methods=['POST'])
def tickets_purchase():
    ticket_type = request.form.get('ticket-type')
    number_of_tickets = request.form.get('number-of-tickets')
    visitor_name = request.form.get('visitor-name')
    visitor_email = request.form.get('visitor-email')
    visit_date = request.form.get('visit-date')
    visit_time = request.form.get('visit-time')

    if not all([ticket_type, number_of_tickets, visitor_name, visitor_email, visit_date, visit_time]):
        tickets = get_tickets(CURRENT_USER)
        return render_template('visitor_tickets.html', tickets=tickets)

    price_map = {'Standard': 15, 'Student': 10, 'Senior': 12, 'Family': 40, 'VIP': 50}
    try:
        num_tickets = int(number_of_tickets)
        price = price_map.get(ticket_type, 15) * num_tickets
    except:
        num_tickets = 1
        price = price_map.get(ticket_type, 15)

    tickets = read_pipe_file('tickets.txt')
    new_ticket_id = 1
    if tickets:
        try:
            new_ticket_id = max(int(t[0]) for t in tickets) + 1
        except:
            new_ticket_id = 1

    purchase_date = datetime.date.today().isoformat()
    new_entry = [str(new_ticket_id), CURRENT_USER, ticket_type, visit_date, visit_time, str(num_tickets), str(price), visitor_name, visitor_email, purchase_date]
    tickets.append(new_entry)
    write_pipe_file('tickets.txt', tickets)

    updated_tickets = get_tickets(CURRENT_USER)
    return render_template('visitor_tickets.html', tickets=updated_tickets)

@app.route('/events', methods=['GET'])
def events_get():
    events = get_events()
    registrations = get_event_registrations()
    user_registrations = {reg['event_id']: reg for reg in registrations if reg['username'] == CURRENT_USER}

    events_output = []
    for event in events:
        reg_status = 'Registered' if event['event_id'] in user_registrations else 'Not Registered'
        events_output.append({**event, 'registration_status': reg_status, 'registration_id': user_registrations.get(event['event_id'], {}).get('registration_id', None)})
    return render_template('virtual_events.html', events=events_output)

@app.route('/events/register/<int:event_id>', methods=['POST'])
def event_register(event_id):
    registrations = get_event_registrations()
    existing = [r for r in registrations if r['event_id'] == event_id and r['username'] == CURRENT_USER]
    if not existing:
        new_reg_id = 1
        if registrations:
            try:
                new_reg_id = max(r['registration_id'] for r in registrations) + 1
            except:
                new_reg_id = 1
        registration_date = datetime.date.today().isoformat()
        registrations.append({'registration_id': new_reg_id, 'event_id': event_id, 'username': CURRENT_USER, 'registration_date': registration_date})
        registrations_raw = [[str(r['registration_id']), str(r['event_id']), r['username'], r['registration_date']] for r in registrations]
        write_pipe_file('event_registrations.txt', registrations_raw)
    return redirect(url_for('events_get'))

@app.route('/events/cancel/<int:registration_id>', methods=['POST'])
def event_cancel(registration_id):
    registrations = get_event_registrations()
    registrations = [r for r in registrations if r['registration_id'] != registration_id or r['username'] != CURRENT_USER]
    registrations_raw = [[str(r['registration_id']), str(r['event_id']), r['username'], r['registration_date']] for r in registrations]
    write_pipe_file('event_registrations.txt', registrations_raw)
    return redirect(url_for('events_get'))

@app.route('/audio-guides', methods=['GET'])
def audio_guides_get():
    guides = get_audio_guides()
    return render_template('audio_guides.html', audio_guides=guides)

@app.route('/audio-guides/filter', methods=['POST'])
def audio_guides_filter():
    language = request.form.get('filter-language')
    guides = get_audio_guides()
    if language:
        filtered = [g for g in guides if g['language'] == language]
    else:
        filtered = guides
    return render_template('audio_guides.html', audio_guides=filtered)

if __name__ == '__main__':
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    app.run(debug=True)
