from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'virtual_museum_secret'
DATA_DIR = 'data'

# Utility functions to load data from pipe-delimited files

def load_users():
    users = []
    try:
        with open(os.path.join(DATA_DIR, 'users.txt'), 'r', encoding='utf-8') as f:
            users = [line.strip() for line in f if line.strip()]
    except Exception:
        pass
    return users


def load_galleries():
    galleries = []
    try:
        with open(os.path.join(DATA_DIR, 'galleries.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 6:
                    galleries.append({
                        'gallery_id': parts[0],
                        'gallery_name': parts[1],
                        'floor': parts[2],
                        'capacity': parts[3],
                        'theme': parts[4],
                        'status': parts[5]
                    })
    except Exception:
        pass
    return galleries


def load_exhibitions():
    exhibitions = []
    try:
        with open(os.path.join(DATA_DIR, 'exhibitions.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 9:
                    exhibitions.append({
                        'exhibition_id': parts[0],
                        'title': parts[1],
                        'description': parts[2],
                        'gallery_id': parts[3],
                        'exhibition_type': parts[4],
                        'start_date': parts[5],
                        'end_date': parts[6],
                        'curator_name': parts[7],
                        'created_by': parts[8]
                    })
    except Exception:
        pass
    return exhibitions


def load_artifacts():
    artifacts = []
    try:
        with open(os.path.join(DATA_DIR, 'artifacts.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 9:
                    artifacts.append({
                        'artifact_id': parts[0],
                        'artifact_name': parts[1],
                        'period': parts[2],
                        'origin': parts[3],
                        'description': parts[4],
                        'exhibition_id': parts[5],
                        'storage_location': parts[6],
                        'acquisition_date': parts[7],
                        'added_by': parts[8]
                    })
    except Exception:
        pass
    return artifacts


def load_audio_guides():
    audio_guides = []
    try:
        with open(os.path.join(DATA_DIR, 'audioguides.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 8:
                    audio_guides.append({
                        'guide_id': parts[0],
                        'exhibit_number': parts[1],
                        'title': parts[2],
                        'language': parts[3],
                        'duration': parts[4],
                        'script': parts[5],
                        'narrator': parts[6],
                        'created_by': parts[7]
                    })
    except Exception:
        pass
    return audio_guides


def load_tickets():
    tickets = []
    try:
        with open(os.path.join(DATA_DIR, 'tickets.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 10:
                    tickets.append({
                        'ticket_id': parts[0],
                        'username': parts[1],
                        'ticket_type': parts[2],
                        'visit_date': parts[3],
                        'visit_time': parts[4],
                        'number_of_tickets': parts[5],
                        'price': parts[6],
                        'visitor_name': parts[7],
                        'visitor_email': parts[8],
                        'purchase_date': parts[9]
                    })
    except Exception:
        pass
    return tickets


def load_events():
    events = []
    try:
        with open(os.path.join(DATA_DIR, 'events.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 9:
                    events.append({
                        'event_id': parts[0],
                        'title': parts[1],
                        'date': parts[2],
                        'time': parts[3],
                        'event_type': parts[4],
                        'speaker': parts[5],
                        'capacity': parts[6],
                        'description': parts[7],
                        'created_by': parts[8]
                    })
    except Exception:
        pass
    return events


def load_event_registrations():
    registrations = []
    try:
        with open(os.path.join(DATA_DIR, 'event_registrations.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 4:
                    registrations.append({
                        'registration_id': parts[0],
                        'event_id': parts[1],
                        'username': parts[2],
                        'registration_date': parts[3]
                    })
    except Exception:
        pass
    return registrations


def load_collection_logs():
    logs = []
    try:
        with open(os.path.join(DATA_DIR, 'collection_logs.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 7:
                    logs.append({
                        'log_id': parts[0],
                        'artifact_id': parts[1],
                        'activity_type': parts[2],
                        'date': parts[3],
                        'notes': parts[4],
                        'condition': parts[5],
                        'curator': parts[6]
                    })
    except Exception:
        pass
    return logs


# Route: Dashboard Page
@app.route('/')
def dashboard():
    exhibitions = load_exhibitions()
    artifacts = load_artifacts()

    total_exhibitions = len(exhibitions)
    active_exhibitions = 0
    today = datetime.today().date()
    for ex in exhibitions:
        try:
            start = datetime.strptime(ex['start_date'], '%Y-%m-%d').date()
            end = datetime.strptime(ex['end_date'], '%Y-%m-%d').date()
            if start <= today <= end:
                active_exhibitions += 1
        except Exception:
            pass

    total_artifacts = len(artifacts)

    return render_template('dashboard.html',
                           total_exhibitions=total_exhibitions,
                           active_exhibitions=active_exhibitions,
                           total_artifacts=total_artifacts)


# Route: Artifact Catalog Page
@app.route('/artifacts', methods=['GET', 'POST'])
def artifacts():
    artifacts = load_artifacts()
    exhibitions = load_exhibitions()
    exhibition_dict = {ex['exhibition_id']: ex['title'] for ex in exhibitions}

    # Collect distinct periods and origins
    periods = sorted(set([art['period'] for art in artifacts]))
    origins = sorted(set([art['origin'] for art in artifacts]))

    search_term = ''
    filter_period = ''
    filter_origin = ''

    filtered_artifacts = artifacts

    if request.method == 'POST':
        search_term = request.form.get('search-artifact', '').strip().lower()
        filter_period = request.form.get('filter-period', '')
        filter_origin = request.form.get('filter-origin', '')

        def artifact_matches(a):
            in_search = True
            if search_term:
                in_search = (search_term in a['artifact_name'].lower()) or (search_term == a['artifact_id'])
            in_period = True
            if filter_period:
                in_period = (a['period'] == filter_period)
            in_origin = True
            if filter_origin:
                in_origin = (a['origin'] == filter_origin)
            return in_search and in_period and in_origin

        filtered_artifacts = [a for a in artifacts if artifact_matches(a)]

    return render_template('artifact_catalog.html',
                           artifacts=filtered_artifacts,
                           exhibition_dict=exhibition_dict,
                           periods=periods,
                           origins=origins,
                           search_term=search_term,
                           filter_period=filter_period,
                           filter_origin=filter_origin)


# Route: Exhibitions Page
@app.route('/exhibitions', methods=['GET', 'POST'])
def exhibitions():
    exhibitions = load_exhibitions()
    galleries = load_galleries()
    gallery_dict = {g['gallery_id']: g for g in galleries}

    filter_type = ''
    filter_gallery = ''

    filtered_exhibitions = exhibitions

    if request.method == 'POST':
        filter_type = request.form.get('filter-exhibition-type', '')
        filter_gallery = request.form.get('filter-gallery', '')

        def exhibition_matches(e):
            match_type = True
            if filter_type:
                match_type = (e['exhibition_type'] == filter_type)
            match_gallery = True
            if filter_gallery:
                match_gallery = (e['gallery_id'] == filter_gallery)
            return match_type and match_gallery

        filtered_exhibitions = [e for e in exhibitions if exhibition_matches(e)]

    return render_template('exhibitions.html',
                           exhibitions=filtered_exhibitions,
                           galleries=galleries,
                           filter_type=filter_type,
                           filter_gallery=filter_gallery)


# Route: Exhibition Details Page
@app.route('/exhibitions/<exhibition_id>')
def exhibition_details(exhibition_id):
    exhibitions = load_exhibitions()
    exhibition = None
    for ex in exhibitions:
        if ex['exhibition_id'] == exhibition_id:
            exhibition = ex
            break
    if not exhibition:
        return "Exhibition not found", 404

    galleries = load_galleries()
    gallery_name = ''
    for g in galleries:
        if g['gallery_id'] == exhibition['gallery_id']:
            gallery_name = g['gallery_name']
            break

    artifacts = load_artifacts()
    exhibition_artifacts = [a for a in artifacts if a['exhibition_id'] == exhibition_id]

    return render_template('exhibition_details.html',
                           exhibition=exhibition,
                           gallery_name=gallery_name,
                           artifacts=exhibition_artifacts)


# Route: Visitor Tickets Page
@app.route('/visitor-tickets', methods=['GET', 'POST'])
def visitor_tickets():
    # No user login mechanism specified, so not filtering by username
    tickets = load_tickets()

    ticket_types = ['Standard', 'Student', 'Senior', 'Family', 'VIP']

    purchase_msg = ''

    if request.method == 'POST':
        ticket_type = request.form.get('ticket-type', '')
        visit_date = request.form.get('visit-date', '')
        visit_time = request.form.get('visit-time', '')
        number_of_tickets = request.form.get('number-of-tickets', '')
        visitor_name = request.form.get('visitor-name', '')
        visitor_email = request.form.get('visitor-email', '')

        # Minimal validation
        if not (ticket_type and visit_date and visit_time and number_of_tickets and visitor_name and visitor_email):
            purchase_msg = 'Please fill in all fields.'
        else:
            try:
                number_of_tickets_int = int(number_of_tickets)
                if number_of_tickets_int <= 0:
                    purchase_msg = 'Number of tickets must be positive.'
                else:
                    # Generate new ticket ID
                    max_id = 0
                    for t in tickets:
                        try:
                            tid = int(t['ticket_id'])
                            if tid > max_id:
                                max_id = tid
                        except Exception:
                            continue
                    new_ticket_id = str(max_id + 1)
                    purchase_date = datetime.now().strftime('%Y-%m-%d')
                    price = 0  # Price logic not specified

                    new_ticket_entry = f"{new_ticket_id}|anonymous_user|{ticket_type}|{visit_date}|{visit_time}|{number_of_tickets}|{price}|{visitor_name}|{visitor_email}|{purchase_date}\n"
                    with open(os.path.join(DATA_DIR, 'tickets.txt'), 'a', encoding='utf-8') as f:
                        f.write(new_ticket_entry)
                    purchase_msg = 'Ticket purchase successful.'
                    # Refresh tickets list after purchase
                    tickets = load_tickets()
            except Exception:
                purchase_msg = 'Invalid number of tickets.'

    # Show all tickets without user filter as no auth specified
    return render_template('visitor_tickets.html',
                           tickets=tickets,
                           ticket_types=ticket_types,
                           purchase_msg=purchase_msg)


# Route: Virtual Events Page
@app.route('/virtual-events', methods=['GET', 'POST'])
def virtual_events():
    events = load_events()
    registrations = load_event_registrations()

    filter_event_type = ''
    if request.method == 'POST':
        filter_event_type = request.form.get('filter-event-type', '')

    filtered_events = events
    if filter_event_type:
        filtered_events = [e for e in events if e['event_type'] == filter_event_type]

    # For simplicity, assume username anonymous_user for registration management
    username = 'anonymous_user'

    event_regs_dict = { (reg['event_id'], reg['username']): reg for reg in registrations }

    return render_template('virtual_events.html',
                           events=filtered_events,
                           registrations=registrations,
                           username=username,
                           filter_event_type=filter_event_type)


# Route: Audio Guides Page
@app.route('/audio-guides', methods=['GET', 'POST'])
def audio_guides():
    audio_guides = load_audio_guides()

    filter_language = ''
    if request.method == 'POST':
        filter_language = request.form.get('filter-language', '')

    filtered_guides = audio_guides
    if filter_language:
        filtered_guides = [g for g in audio_guides if g['language'] == filter_language]

    languages = ['English', 'Spanish', 'French']

    return render_template('audio_guides.html',
                           audio_guides=filtered_guides,
                           filter_language=filter_language,
                           languages=languages)


if __name__ == '__main__':
    app.run(debug=True)
