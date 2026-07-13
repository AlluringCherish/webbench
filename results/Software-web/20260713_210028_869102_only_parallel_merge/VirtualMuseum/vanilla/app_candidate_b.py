from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)
DATA_DIR = 'data'

# Utility functions to read data from files

def read_users():
    path = os.path.join(DATA_DIR, 'users.txt')
    if not os.path.exists(path):
        return []
    with open(path, 'r', encoding='utf-8') as f:
        users = [line.strip() for line in f.readlines() if line.strip()]
    return users


def read_galleries():
    path = os.path.join(DATA_DIR, 'galleries.txt')
    galleries = []
    if not os.path.exists(path):
        return galleries
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                gallery_id, gallery_name, floor, capacity, theme, status = line.strip().split('|')
                galleries.append({
                    'gallery_id': gallery_id,
                    'gallery_name': gallery_name,
                    'floor': floor,
                    'capacity': capacity,
                    'theme': theme,
                    'status': status
                })
    return galleries


def read_exhibitions():
    path = os.path.join(DATA_DIR, 'exhibitions.txt')
    exhibitions = []
    if not os.path.exists(path):
        return exhibitions
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                parts = line.strip().split('|')
                if len(parts) == 9:
                    exhibition_id, title, description, gallery_id, exhibition_type, start_date, end_date, curator_name, created_by = parts
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


def read_artifacts():
    path = os.path.join(DATA_DIR, 'artifacts.txt')
    artifacts = []
    if not os.path.exists(path):
        return artifacts
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                parts = line.strip().split('|')
                if len(parts) == 9:
                    artifact_id, artifact_name, period, origin, description, exhibition_id, storage_location, acquisition_date, added_by = parts
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


def read_audioguides():
    path = os.path.join(DATA_DIR, 'audioguides.txt')
    guides = []
    if not os.path.exists(path):
        return guides
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                parts = line.strip().split('|')
                if len(parts) == 8:
                    guide_id, exhibit_number, title, language, duration, script, narrator, created_by = parts
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


def read_tickets():
    path = os.path.join(DATA_DIR, 'tickets.txt')
    tickets = []
    if not os.path.exists(path):
        return tickets
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                parts = line.strip().split('|')
                if len(parts) == 10:
                    ticket_id, username, ticket_type, visit_date, visit_time, number_of_tickets, price, visitor_name, visitor_email, purchase_date = parts
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


def read_events():
    path = os.path.join(DATA_DIR, 'events.txt')
    events = []
    if not os.path.exists(path):
        return events
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                parts = line.strip().split('|')
                if len(parts) == 9:
                    event_id, title, date, time_, event_type, speaker, capacity, description, created_by = parts
                    events.append({
                        'event_id': event_id,
                        'title': title,
                        'date': date,
                        'time': time_,
                        'event_type': event_type,
                        'speaker': speaker,
                        'capacity': capacity,
                        'description': description,
                        'created_by': created_by
                    })
    return events


def read_event_registrations():
    path = os.path.join(DATA_DIR, 'event_registrations.txt')
    registrations = []
    if not os.path.exists(path):
        return registrations
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                parts = line.strip().split('|')
                if len(parts) == 4:
                    registration_id, event_id, username, registration_date = parts
                    registrations.append({
                        'registration_id': registration_id,
                        'event_id': event_id,
                        'username': username,
                        'registration_date': registration_date
                    })
    return registrations


@app.route('/')
def dashboard():
    exhibitions = read_exhibitions()
    total_exhibitions = len(exhibitions)
    today = datetime.today().date()
    active_exhibitions = 0
    for ex in exhibitions:
        try:
            start = datetime.strptime(ex['start_date'], '%Y-%m-%d').date()
            end = datetime.strptime(ex['end_date'], '%Y-%m-%d').date()
            if start <= today <= end:
                active_exhibitions += 1
        except:
            continue
    artifacts = read_artifacts()
    total_artifacts = len(artifacts)
    return render_template('dashboard.html',
                           total_exhibitions=total_exhibitions,
                           active_exhibitions=active_exhibitions,
                           total_artifacts=total_artifacts)


@app.route('/artifacts', methods=['GET', 'POST'])
def artifact_catalog():
    artifacts = read_artifacts()
    exhibitions = read_exhibitions()
    exhibition_map = {ex['exhibition_id']: ex['title'] for ex in exhibitions}
    periods = sorted(set([art['period'] for art in artifacts]))
    origins = sorted(set([art['origin'] for art in artifacts]))

    filtered_artifacts = artifacts

    if request.method == 'POST':
        search_term = request.form.get('search-artifact', '').strip().lower()
        filter_period = request.form.get('filter-period', '')
        filter_origin = request.form.get('filter-origin', '')

        def artifact_matches(art):
            matches_search = (search_term in art['artifact_name'].lower()) or (search_term in art['artifact_id'])
            matches_period = (filter_period == '') or (art['period'] == filter_period)
            matches_origin = (filter_origin == '') or (art['origin'] == filter_origin)
            return matches_search and matches_period and matches_origin

        filtered_artifacts = [art for art in artifacts if artifact_matches(art)]

    return render_template('artifact_catalog.html',
                           artifacts=filtered_artifacts,
                           exhibitions=exhibition_map,
                           periods=periods,
                           origins=origins)


@app.route('/exhibitions', methods=['GET', 'POST'])
def exhibitions():
    exhibitions = read_exhibitions()
    galleries = read_galleries()
    gallery_map = {g['gallery_id']: g['gallery_name'] for g in galleries}

    filter_type = ''
    filter_gallery = ''

    filtered_exhibitions = exhibitions

    if request.method == 'POST':
        filter_type = request.form.get('filter-exhibition-type', '')
        filter_gallery = request.form.get('filter-gallery', '')

        def exhibition_matches(ex):
            matches_type = (filter_type == '') or (ex['exhibition_type'] == filter_type)
            matches_gallery = (filter_gallery == '') or (ex['gallery_id'] == filter_gallery)
            return matches_type and matches_gallery

        filtered_exhibitions = [ex for ex in exhibitions if exhibition_matches(ex)]

    return render_template('exhibitions.html',
                           exhibitions=filtered_exhibitions,
                           galleries=galleries,
                           gallery_map=gallery_map,
                           filter_type=filter_type,
                           filter_gallery=filter_gallery)


@app.route('/exhibitions/<exhibition_id>')
def exhibition_details(exhibition_id):
    exhibitions = read_exhibitions()
    galleries = read_galleries()
    artifacts = read_artifacts()
    exhibition = next((ex for ex in exhibitions if ex['exhibition_id'] == exhibition_id), None)
    if exhibition is None:
        return "Exhibition not found", 404

    gallery = next((g for g in galleries if g['gallery_id'] == exhibition['gallery_id']), None)

    exhibition_artifacts = [art for art in artifacts if art['exhibition_id'] == exhibition_id]

    # Format dates human readable
    try:
        start_date = datetime.strptime(exhibition['start_date'], '%Y-%m-%d').strftime('%B %d, %Y')
        end_date = datetime.strptime(exhibition['end_date'], '%Y-%m-%d').strftime('%B %d, %Y')
        exhibition_dates = f"{start_date} - {end_date}"
    except:
        exhibition_dates = f"{exhibition['start_date']} - {exhibition['end_date']}"

    return render_template('exhibition_details.html',
                           exhibition=exhibition,
                           exhibition_dates=exhibition_dates,
                           gallery=gallery,
                           artifacts=exhibition_artifacts)


@app.route('/visitor-tickets', methods=['GET', 'POST'])
def visitor_tickets():
    # For simplification, we will assume a fixed username 'visitor_mary' as current user
    current_user = 'visitor_mary'
    ticket_types = ['Standard', 'Student', 'Senior', 'Family', 'VIP']

    tickets = read_tickets()
    user_tickets = [t for t in tickets if t['username'] == current_user]

    message = ''

    if request.method == 'POST':
        ticket_type = request.form.get('ticket-type')
        visit_date = request.form.get('visit-date')
        visit_time = request.form.get('visit-time')
        number_of_tickets = request.form.get('number-of-tickets')
        visitor_name = request.form.get('visitor-name')
        visitor_email = request.form.get('visitor-email')

        # Basic validation
        if not ticket_type or not visit_date or not visit_time or not number_of_tickets or not visitor_name or not visitor_email:
            message = 'Please fill in all fields.'
        else:
            try:
                num_tickets = int(number_of_tickets)
                if num_tickets <= 0:
                    message = 'Number of tickets must be positive.'
                else:
                    # Calculate price (dummy pricing for example)
                    prices = {'Standard': 15, 'Student': 10, 'Senior': 12, 'Family': 25, 'VIP': 50}
                    price_total = prices.get(ticket_type, 15) * num_tickets
                    # Generate new ticket_id
                    max_id = max([int(t['ticket_id']) for t in tickets], default=0)
                    new_id = max_id + 1
                    purchase_date = datetime.today().strftime('%Y-%m-%d')
                    new_ticket = f"{new_id}|{current_user}|{ticket_type}|{visit_date}|{visit_time}|{num_tickets}|{price_total}|{visitor_name}|{visitor_email}|{purchase_date}"
                    with open(os.path.join(DATA_DIR, 'tickets.txt'), 'a', encoding='utf-8') as f:
                        f.write(new_ticket + '\n')
                    message = 'Ticket purchased successfully.'
                    # Reload user tickets
                    tickets = read_tickets()
                    user_tickets = [t for t in tickets if t['username'] == current_user]
            except Exception as e:
                message = 'Invalid input.'

    return render_template('visitor_tickets.html',
                           ticket_types=ticket_types,
                           user_tickets=user_tickets,
                           message=message)


@app.route('/virtual-events', methods=['GET', 'POST'])
def virtual_events():
    current_user = 'visitor_mary'
    events = read_events()
    registrations = read_event_registrations()

    filter_event_type = ''

    if request.method == 'POST':
        filter_event_type = request.form.get('filter-event-type', '')
        if 'register-event-id' in request.form:
            event_id = request.form.get('register-event-id')
            # Check already registered
            if not any(reg['event_id'] == event_id and reg['username'] == current_user for reg in registrations):
                # Add new registration
                max_reg_id = max([int(r['registration_id']) for r in registrations], default=0)
                new_reg_id = max_reg_id + 1
                registration_date = datetime.today().strftime('%Y-%m-%d')
                new_reg_line = f"{new_reg_id}|{event_id}|{current_user}|{registration_date}"
                with open(os.path.join(DATA_DIR, 'event_registrations.txt'), 'a', encoding='utf-8') as f:
                    f.write(new_reg_line + '\n')
                registrations = read_event_registrations()
        elif 'cancel-registration-id' in request.form:
            cancel_id = request.form.get('cancel-registration-id')
            # Remove registration
            registrations = [r for r in registrations if r['registration_id'] != cancel_id]
            with open(os.path.join(DATA_DIR, 'event_registrations.txt'), 'w', encoding='utf-8') as f:
                for r in registrations:
                    line = '|'.join([r['registration_id'], r['event_id'], r['username'], r['registration_date']])
                    f.write(line + '\n')

    if filter_event_type:
        events = [e for e in events if e['event_type'] == filter_event_type]

    # Build registration lookup for current user
    user_registrations = {r['event_id']: r for r in registrations if r['username'] == current_user}

    return render_template('virtual_events.html',
                           events=events,
                           user_registrations=user_registrations,
                           filter_event_type=filter_event_type)


@app.route('/audio-guides', methods=['GET', 'POST'])
def audio_guides():
    guides = read_audioguides()
    filter_language = ''
    languages = ['English', 'Spanish', 'French']
    if request.method == 'POST':
        filter_language = request.form.get('filter-language', '')
        if filter_language:
            guides = [g for g in guides if g['language'] == filter_language]

    return render_template('audio_guides.html',
                           guides=guides,
                           filter_language=filter_language,
                           languages=languages)


if __name__ == '__main__':
    app.run(debug=True)
