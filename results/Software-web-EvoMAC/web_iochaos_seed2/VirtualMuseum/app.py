'''
Main backend application for VirtualMuseum web app using Flask.
Implements routing, data loading/saving, filtering, searching, and navigation
for all seven pages as per requirements.
Data is stored in plain text files under 'data' directory with pipe-delimited format.
'''
from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime
app = Flask(__name__)
DATA_DIR = 'data'
# Utility functions for reading and writing data files
def read_users():
    path = os.path.join(DATA_DIR, 'users.txt')
    users = []
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                username = line.strip()
                if username:
                    users.append(username)
    return users
def read_galleries():
    path = os.path.join(DATA_DIR, 'galleries.txt')
    galleries = {}
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) == 6:
                    gallery_id = parts[0]
                    galleries[gallery_id] = {
                        'gallery_id': gallery_id,
                        'gallery_name': parts[1],
                        'floor': parts[2],
                        'capacity': parts[3],
                        'theme': parts[4],
                        'status': parts[5]
                    }
    return galleries
def read_exhibitions():
    path = os.path.join(DATA_DIR, 'exhibitions.txt')
    exhibitions = []
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
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
    return exhibitions
def read_artifacts():
    path = os.path.join(DATA_DIR, 'artifacts.txt')
    artifacts = []
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
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
    return artifacts
def read_audioguides():
    path = os.path.join(DATA_DIR, 'audioguides.txt')
    guides = []
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) == 8:
                    guides.append({
                        'guide_id': parts[0],
                        'exhibit_number': parts[1],
                        'title': parts[2],
                        'language': parts[3],
                        'duration': parts[4],
                        'script': parts[5],
                        'narrator': parts[6],
                        'created_by': parts[7]
                    })
    return guides
def read_tickets():
    path = os.path.join(DATA_DIR, 'tickets.txt')
    tickets = []
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
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
    return tickets
def read_events():
    path = os.path.join(DATA_DIR, 'events.txt')
    events = []
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
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
    return events
def read_event_registrations():
    path = os.path.join(DATA_DIR, 'event_registrations.txt')
    registrations = []
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) == 4:
                    registrations.append({
                        'registration_id': parts[0],
                        'event_id': parts[1],
                        'username': parts[2],
                        'registration_date': parts[3]
                    })
    return registrations
def read_collection_logs():
    path = os.path.join(DATA_DIR, 'collection_logs.txt')
    logs = []
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
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
    return logs
def write_tickets(tickets):
    path = os.path.join(DATA_DIR, 'tickets.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for t in tickets:
            line = '|'.join([
                t['ticket_id'], t['username'], t['ticket_type'], t['visit_date'], t['visit_time'],
                t['number_of_tickets'], t['price'], t['visitor_name'], t['visitor_email'], t['purchase_date']
            ])
            f.write(line + '\n')
def write_event_registrations(registrations):
    path = os.path.join(DATA_DIR, 'event_registrations.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for r in registrations:
            line = '|'.join([
                r['registration_id'], r['event_id'], r['username'], r['registration_date']
            ])
            f.write(line + '\n')
# Helper functions
def get_next_id(items, id_key):
    max_id = 0
    for item in items:
        try:
            val = int(item[id_key])
            if val > max_id:
                max_id = val
        except:
            continue
    return str(max_id + 1)
def is_exhibition_active(exhibition):
    # Check if current date is between start_date and end_date inclusive
    today = datetime.today().date()
    try:
        start = datetime.strptime(exhibition['start_date'], '%Y-%m-%d').date()
        end = datetime.strptime(exhibition['end_date'], '%Y-%m-%d').date()
        return start <= today <= end
    except:
        return False
# Routes
@app.route('/')
def dashboard():
    exhibitions = read_exhibitions()
    total_exhibitions = len(exhibitions)
    active_exhibitions = sum(1 for e in exhibitions if is_exhibition_active(e))
    return render_template('dashboard.html',
                           page_title='Museum Dashboard',
                           total_exhibitions=total_exhibitions,
                           active_exhibitions=active_exhibitions)
# Artifact Catalog Page
@app.route('/artifact_catalog', methods=['GET', 'POST'])
def artifact_catalog():
    artifacts = read_artifacts()
    exhibitions = {e['exhibition_id']: e['title'] for e in read_exhibitions()}
    search_query = ''
    filtered_artifacts = artifacts
    if request.method == 'POST':
        search_query = request.form.get('search-artifact', '').strip().lower()
        if search_query:
            filtered_artifacts = []
            for a in artifacts:
                if (search_query in a['artifact_name'].lower()) or (search_query == a['artifact_id']):
                    filtered_artifacts.append(a)
    # Add exhibition title to each artifact for display
    for a in filtered_artifacts:
        a['exhibition_title'] = exhibitions.get(a['exhibition_id'], 'N/A')
    return render_template('artifact_catalog.html',
                           page_title='Artifact Catalog',
                           artifacts=filtered_artifacts,
                           search_query=search_query)
# Exhibitions Page
@app.route('/exhibitions', methods=['GET', 'POST'])
def exhibitions():
    exhibitions = read_exhibitions()
    galleries = read_galleries()
    filter_type = ''
    filtered_exhibitions = exhibitions
    if request.method == 'POST':
        filter_type = request.form.get('filter-exhibition-type', '')
        if filter_type:
            filtered_exhibitions = [e for e in exhibitions if e['exhibition_type'].lower() == filter_type.lower()]
    # Add gallery name and status to each exhibition for display
    for e in filtered_exhibitions:
        gallery = galleries.get(e['gallery_id'])
        e['gallery_name'] = gallery['gallery_name'] if gallery else 'N/A'
        e['gallery_status'] = gallery['status'] if gallery else 'Unknown'
    return render_template('exhibitions.html',
                           page_title='Exhibitions',
                           exhibitions=filtered_exhibitions,
                           filter_type=filter_type)
# Exhibition Details Page
@app.route('/exhibition_details/<exhibition_id>')
def exhibition_details(exhibition_id):
    exhibitions = read_exhibitions()
    exhibition = next((e for e in exhibitions if e['exhibition_id'] == exhibition_id), None)
    if not exhibition:
        return "Exhibition not found", 404
    artifacts = read_artifacts()
    exhibition_artifacts = [a for a in artifacts if a['exhibition_id'] == exhibition_id]
    return render_template('exhibition_details.html',
                           page_title='Exhibition Details',
                           exhibition=exhibition,
                           artifacts=exhibition_artifacts)
# Visitor Tickets Page
@app.route('/visitor_tickets', methods=['GET', 'POST'])
def visitor_tickets():
    tickets = read_tickets()
    # For demo, assume username is visitor_mary (in real app, would be from session)
    username = request.args.get('username', 'visitor_mary')
    user_tickets = [t for t in tickets if t['username'] == username]
    message = ''
    if request.method == 'POST':
        ticket_type = request.form.get('ticket-type', '')
        number_of_tickets = request.form.get('number-of-tickets', '1')
        visitor_name = request.form.get('visitor-name', '').strip()
        visitor_email = request.form.get('visitor-email', '').strip()
        visit_date = request.form.get('visit-date', '').strip()
        visit_time = request.form.get('visit-time', '').strip()
        # Validate inputs minimally
        if not (ticket_type and number_of_tickets.isdigit() and visitor_name and visitor_email and visit_date and visit_time):
            message = 'Please fill all required fields correctly.'
        else:
            number_of_tickets_int = int(number_of_tickets)
            # Pricing logic (example prices)
            price_map = {
                'Standard': 15,
                'Student': 10,
                'Senior': 12,
                'Family': 40,
                'VIP': 50
            }
            price_per_ticket = price_map.get(ticket_type, 15)
            total_price = price_per_ticket * number_of_tickets_int
            new_ticket_id = get_next_id(tickets, 'ticket_id')
            purchase_date = datetime.today().strftime('%Y-%m-%d')
            new_ticket = {
                'ticket_id': new_ticket_id,
                'username': username,
                'ticket_type': ticket_type,
                'visit_date': visit_date,
                'visit_time': visit_time,
                'number_of_tickets': str(number_of_tickets_int),
                'price': str(total_price),
                'visitor_name': visitor_name,
                'visitor_email': visitor_email,
                'purchase_date': purchase_date
            }
            tickets.append(new_ticket)
            write_tickets(tickets)
            message = 'Ticket purchase successful.'
            user_tickets.append(new_ticket)
    return render_template('visitor_tickets.html',
                           page_title='Visitor Tickets',
                           tickets=user_tickets,
                           message=message,
                           username=username)
# Virtual Events Page
@app.route('/virtual_events', methods=['GET', 'POST'])
def virtual_events():
    events = read_events()
    registrations = read_event_registrations()
    username = request.args.get('username', 'visitor_mary')
    message = ''
    # Handle registration and cancellation via POST
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'register':
            event_id = request.form.get('event_id')
            # Check if already registered
            already_registered = any(r for r in registrations if r['event_id'] == event_id and r['username'] == username)
            if already_registered:
                message = 'Already registered for this event.'
            else:
                new_reg_id = get_next_id(registrations, 'registration_id')
                registration_date = datetime.today().strftime('%Y-%m-%d')
                registrations.append({
                    'registration_id': new_reg_id,
                    'event_id': event_id,
                    'username': username,
                    'registration_date': registration_date
                })
                write_event_registrations(registrations)
                message = 'Registration successful.'
        elif action == 'cancel':
            registration_id = request.form.get('registration_id')
            registrations = [r for r in registrations if not (r['registration_id'] == registration_id and r['username'] == username)]
            write_event_registrations(registrations)
            message = 'Registration cancelled.'
    # Build event list with registration status for current user
    event_list = []
    for e in events:
        reg = next((r for r in registrations if r['event_id'] == e['event_id'] and r['username'] == username), None)
        event_list.append({
            'event_id': e['event_id'],
            'title': e['title'],
            'date': e['date'],
            'time': e['time'],
            'event_type': e['event_type'],
            'registration_status': 'Registered' if reg else 'Not Registered',
            'registration_id': reg['registration_id'] if reg else None
        })
    return render_template('virtual_events.html',
                           page_title='Virtual Events',
                           events=event_list,
                           message=message,
                           username=username)
# Audio Guides Page
@app.route('/audio_guides', methods=['GET', 'POST'])
def audio_guides():
    guides = read_audioguides()
    filter_language = ''
    filtered_guides = guides
    if request.method == 'POST':
        filter_language = request.form.get('filter-language', '')
        if filter_language:
            filtered_guides = [g for g in guides if g['language'].lower() == filter_language.lower()]
    return render_template('audio_guides.html',
                           page_title='Audio Guides',
                           guides=filtered_guides,
                           filter_language=filter_language)
# Run the app
if __name__ == '__main__':
    app.run(port=5000, debug=True)