'''
Main backend Python application for the VirtualMuseum web application.
Implements the web server and all routing logic using Flask.
Handles reading from and writing to local text files in the 'data' directory.
Implements business logic for Dashboard, Artifact Catalog, Exhibitions, Exhibition Details,
Visitor Tickets, Virtual Events, and Audio Guides pages.
Manages navigation, filtering, searching, and CRUD operations as required.
'''
from flask import Flask, render_template, request, redirect, url_for, flash
import os
import datetime
app = Flask(__name__)
app.secret_key = 'virtualmuseum_secret_key'  # Needed for flash messages
DATA_DIR = 'data'
# Utility functions for reading and writing pipe-delimited text files
def read_lines(filename):
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        return []
    with open(path, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]
    return lines
def write_lines(filename, lines):
    path = os.path.join(DATA_DIR, filename)
    with open(path, 'w', encoding='utf-8') as f:
        for line in lines:
            f.write(line + '\n')
def parse_pipe_line(line, fields_count=None):
    parts = line.split('|')
    if fields_count is not None and len(parts) != fields_count:
        # If line does not have expected number of fields, ignore or handle gracefully
        return None
    return parts
def format_pipe_line(parts):
    return '|'.join(str(p) for p in parts)
# ========== Data Loaders ==========
def load_users():
    lines = read_lines('users.txt')
    return lines  # list of usernames
def load_galleries():
    lines = read_lines('galleries.txt')
    galleries = []
    for line in lines:
        parts = parse_pipe_line(line, 6)
        if parts:
            gallery = {
                'gallery_id': parts[0],
                'gallery_name': parts[1],
                'floor': parts[2],
                'capacity': parts[3],
                'theme': parts[4],
                'status': parts[5]
            }
            galleries.append(gallery)
    return galleries
def load_exhibitions():
    lines = read_lines('exhibitions.txt')
    exhibitions = []
    for line in lines:
        parts = parse_pipe_line(line, 9)
        if parts:
            exhibition = {
                'exhibition_id': parts[0],
                'title': parts[1],
                'description': parts[2],
                'gallery_id': parts[3],
                'exhibition_type': parts[4],
                'start_date': parts[5],
                'end_date': parts[6],
                'curator_name': parts[7],
                'created_by': parts[8]
            }
            exhibitions.append(exhibition)
    return exhibitions
def load_artifacts():
    lines = read_lines('artifacts.txt')
    artifacts = []
    for line in lines:
        parts = parse_pipe_line(line, 9)
        if parts:
            artifact = {
                'artifact_id': parts[0],
                'artifact_name': parts[1],
                'period': parts[2],
                'origin': parts[3],
                'description': parts[4],
                'exhibition_id': parts[5],
                'storage_location': parts[6],
                'acquisition_date': parts[7],
                'added_by': parts[8]
            }
            artifacts.append(artifact)
    return artifacts
def load_audioguides():
    lines = read_lines('audioguides.txt')
    guides = []
    for line in lines:
        parts = parse_pipe_line(line, 8)
        if parts:
            guide = {
                'guide_id': parts[0],
                'exhibit_number': parts[1],
                'title': parts[2],
                'language': parts[3],
                'duration': parts[4],
                'script': parts[5],
                'narrator': parts[6],
                'created_by': parts[7]
            }
            guides.append(guide)
    return guides
def load_tickets():
    lines = read_lines('tickets.txt')
    tickets = []
    for line in lines:
        parts = parse_pipe_line(line, 10)
        if parts:
            try:
                number_of_tickets = int(parts[5])
            except:
                number_of_tickets = 0
            try:
                price = float(parts[6])
            except:
                price = 0.0
            ticket = {
                'ticket_id': parts[0],
                'username': parts[1],
                'ticket_type': parts[2],
                'visit_date': parts[3],
                'visit_time': parts[4],
                'number_of_tickets': number_of_tickets,
                'price': price,
                'visitor_name': parts[7],
                'visitor_email': parts[8],
                'purchase_date': parts[9]
            }
            tickets.append(ticket)
    return tickets
def load_events():
    lines = read_lines('events.txt')
    events = []
    for line in lines:
        parts = parse_pipe_line(line, 9)
        if parts:
            try:
                capacity = int(parts[6])
            except:
                capacity = 0
            event = {
                'event_id': parts[0],
                'title': parts[1],
                'date': parts[2],
                'time': parts[3],
                'event_type': parts[4],
                'speaker': parts[5],
                'capacity': capacity,
                'description': parts[7],
                'created_by': parts[8]
            }
            events.append(event)
    return events
def load_event_registrations():
    lines = read_lines('event_registrations.txt')
    registrations = []
    for line in lines:
        parts = parse_pipe_line(line, 4)
        if parts:
            registration = {
                'registration_id': parts[0],
                'event_id': parts[1],
                'username': parts[2],
                'registration_date': parts[3]
            }
            registrations.append(registration)
    return registrations
def load_collection_logs():
    lines = read_lines('collection_logs.txt')
    logs = []
    for line in lines:
        parts = parse_pipe_line(line, 7)
        if parts:
            log = {
                'log_id': parts[0],
                'artifact_id': parts[1],
                'activity_type': parts[2],
                'date': parts[3],
                'notes': parts[4],
                'condition': parts[5],
                'curator': parts[6]
            }
            logs.append(log)
    return logs
# ========== Data Writers ==========
def save_exhibitions(exhibitions):
    lines = []
    for ex in exhibitions:
        line = format_pipe_line([
            ex['exhibition_id'], ex['title'], ex['description'], ex['gallery_id'],
            ex['exhibition_type'], ex['start_date'], ex['end_date'], ex['curator_name'], ex['created_by']
        ])
        lines.append(line)
    write_lines('exhibitions.txt', lines)
def save_artifacts(artifacts):
    lines = []
    for art in artifacts:
        line = format_pipe_line([
            art['artifact_id'], art['artifact_name'], art['period'], art['origin'], art['description'],
            art['exhibition_id'], art['storage_location'], art['acquisition_date'], art['added_by']
        ])
        lines.append(line)
    write_lines('artifacts.txt', lines)
def save_tickets(tickets):
    lines = []
    for t in tickets:
        line = format_pipe_line([
            t['ticket_id'], t['username'], t['ticket_type'], t['visit_date'], t['visit_time'],
            str(t['number_of_tickets']), f"{t['price']:.2f}", t['visitor_name'], t['visitor_email'], t['purchase_date']
        ])
        lines.append(line)
    write_lines('tickets.txt', lines)
def save_event_registrations(registrations):
    lines = []
    for r in registrations:
        line = format_pipe_line([
            r['registration_id'], r['event_id'], r['username'], r['registration_date']
        ])
        lines.append(line)
    write_lines('event_registrations.txt', lines)
# ========== Helper Functions ==========
def get_next_id(items, id_field):
    max_id = 0
    for item in items:
        try:
            val = int(item[id_field])
            if val > max_id:
                max_id = val
        except:
            continue
    return str(max_id + 1)
def parse_date(date_str):
    try:
        return datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
    except:
        return None
def parse_datetime(date_str, time_str):
    try:
        dt_str = f"{date_str} {time_str}"
        return datetime.datetime.strptime(dt_str, '%Y-%m-%d %I:%M %p')
    except:
        return None
def is_exhibition_active(exhibition):
    today = datetime.date.today()
    start = parse_date(exhibition['start_date'])
    end = parse_date(exhibition['end_date'])
    if start and end:
        return start <= today <= end
    return False
def get_gallery_name(gallery_id, galleries):
    for g in galleries:
        if g['gallery_id'] == gallery_id:
            return g['gallery_name']
    return 'Unknown'
def get_exhibition_title(exhibition_id, exhibitions):
    for ex in exhibitions:
        if ex['exhibition_id'] == exhibition_id:
            return ex['title']
    return 'Unknown'
# ========== Routes ==========
@app.route('/')
def dashboard():
    exhibitions = load_exhibitions()
    artifacts = load_artifacts()
    galleries = load_galleries()
    total_exhibitions = len(exhibitions)
    active_exhibitions = sum(1 for ex in exhibitions if is_exhibition_active(ex))
    return render_template('dashboard.html',
                           exhibition_summary={'total': total_exhibitions, 'active': active_exhibitions},
                           galleries=galleries,
                           artifacts=artifacts)
# -------- Artifact Catalog --------
@app.route('/artifact_catalog', methods=['GET', 'POST'])
def artifact_catalog():
    artifacts = load_artifacts()
    exhibitions = load_exhibitions()
    search_query = ''
    filtered_artifacts = artifacts
    if request.method == 'POST':
        search_query = request.form.get('search-artifact', '').strip().lower()
        if search_query:
            filtered_artifacts = [a for a in artifacts if search_query in a['artifact_name'].lower() or search_query == a['artifact_id']]
        else:
            filtered_artifacts = artifacts
    # For each artifact, get exhibition title for display
    for art in filtered_artifacts:
        art['exhibition_title'] = get_exhibition_title(art['exhibition_id'], exhibitions)
    return render_template('artifact_catalog.html',
                           artifacts=filtered_artifacts,
                           search_query=search_query)
# -------- Exhibitions --------
@app.route('/exhibitions', methods=['GET', 'POST'])
def exhibitions():
    exhibitions = load_exhibitions()
    galleries = load_galleries()
    filter_type = ''
    filtered_exhibitions = exhibitions
    if request.method == 'POST':
        filter_type = request.form.get('filter-exhibition-type', '')
        if filter_type and filter_type != 'All':
            filtered_exhibitions = [ex for ex in exhibitions if ex['exhibition_type'].lower() == filter_type.lower()]
        else:
            filtered_exhibitions = exhibitions
    # Add gallery name and status for display
    for ex in filtered_exhibitions:
        ex['gallery_name'] = get_gallery_name(ex['gallery_id'], galleries)
        ex['status'] = 'Active' if is_exhibition_active(ex) else 'Inactive'
    return render_template('exhibitions.html',
                           exhibitions=filtered_exhibitions,
                           filter_type=filter_type)
# -------- Exhibition Details --------
@app.route('/exhibition_details/<exhibition_id>')
def exhibition_details(exhibition_id):
    exhibitions = load_exhibitions()
    artifacts = load_artifacts()
    exhibition = next((ex for ex in exhibitions if ex['exhibition_id'] == exhibition_id), None)
    if not exhibition:
        flash('Exhibition not found.', 'error')
        return redirect(url_for('exhibitions'))
    # Get artifacts belonging to this exhibition
    exhibition_artifacts = [a for a in artifacts if a['exhibition_id'] == exhibition_id]
    return render_template('exhibition_details.html',
                           exhibition=exhibition,
                           artifacts=exhibition_artifacts)
# -------- Visitor Tickets --------
@app.route('/visitor_tickets', methods=['GET', 'POST'])
def visitor_tickets():
    tickets = load_tickets()
    # For demonstration, assume username is visitor_mary (no auth implemented)
    username = 'visitor_mary'
    user_tickets = [t for t in tickets if t['username'] == username]
    if request.method == 'POST':
        ticket_type = request.form.get('ticket-type', '')
        number_of_tickets = request.form.get('number-of-tickets', '')
        visitor_name = request.form.get('visitor-name', '').strip()
        visitor_email = request.form.get('visitor-email', '').strip()
        visit_date = request.form.get('visit-date', '').strip()
        visit_time = request.form.get('visit-time', '').strip()
        # Validate inputs
        error = None
        if not ticket_type:
            error = 'Ticket type is required.'
        elif not number_of_tickets.isdigit() or int(number_of_tickets) <= 0:
            error = 'Number of tickets must be a positive integer.'
        elif not visitor_name:
            error = 'Visitor name is required.'
        elif not visitor_email:
            error = 'Visitor email is required.'
        elif not visit_date:
            error = 'Visit date is required.'
        elif not visit_time:
            error = 'Visit time is required.'
        if error:
            flash(error, 'error')
        else:
            number_of_tickets = int(number_of_tickets)
            # Pricing logic (example prices)
            price_map = {
                'Standard': 15,
                'Student': 10,
                'Senior': 12,
                'Family': 40,
                'VIP': 50
            }
            price_per_ticket = price_map.get(ticket_type, 15)
            total_price = price_per_ticket * number_of_tickets
            tickets = load_tickets()
            new_ticket_id = get_next_id(tickets, 'ticket_id')
            purchase_date = datetime.date.today().strftime('%Y-%m-%d')
            new_ticket = {
                'ticket_id': new_ticket_id,
                'username': username,
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
            save_tickets(tickets)
            flash('Ticket purchase successful.', 'success')
            return redirect(url_for('visitor_tickets'))
    return render_template('visitor_tickets.html',
                           tickets=user_tickets)
# -------- Virtual Events --------
@app.route('/virtual_events', methods=['GET', 'POST'])
def virtual_events():
    events = load_events()
    registrations = load_event_registrations()
    # For demonstration, assume username is visitor_mary (no auth implemented)
    username = 'visitor_mary'
    # Build registration map for quick lookup: event_id -> registration
    user_registrations = {r['event_id']: r for r in registrations if r['username'] == username}
    if request.method == 'POST':
        action = request.form.get('action')
        event_id = request.form.get('event_id')
        if action == 'register':
            # Check if already registered
            if event_id in user_registrations:
                flash('You are already registered for this event.', 'error')
            else:
                # Check capacity
                event = next((e for e in events if e['event_id'] == event_id), None)
                if not event:
                    flash('Event not found.', 'error')
                else:
                    # Count current registrations for this event
                    current_count = sum(1 for r in registrations if r['event_id'] == event_id)
                    if current_count >= event['capacity']:
                        flash('Event capacity reached.', 'error')
                    else:
                        new_reg_id = get_next_id(registrations, 'registration_id')
                        registration_date = datetime.date.today().strftime('%Y-%m-%d')
                        new_registration = {
                            'registration_id': new_reg_id,
                            'event_id': event_id,
                            'username': username,
                            'registration_date': registration_date
                        }
                        registrations.append(new_registration)
                        save_event_registrations(registrations)
                        flash('Successfully registered for the event.', 'success')
                        # Update user_registrations map
                        user_registrations[event_id] = new_registration
        elif action == 'cancel':
            registration_id = request.form.get('registration_id')
            registration = next((r for r in registrations if r['registration_id'] == registration_id and r['username'] == username), None)
            if registration:
                registrations.remove(registration)
                save_event_registrations(registrations)
                flash('Registration cancelled.', 'success')
                user_registrations.pop(registration['event_id'], None)
            else:
                flash('Registration not found or unauthorized.', 'error')
        return redirect(url_for('virtual_events'))
    # Prepare event list with registration status for this user
    event_list = []
    for e in events:
        reg = user_registrations.get(e['event_id'])
        registration_status = 'Registered' if reg else 'Not Registered'
        event_list.append({
            'event_id': e['event_id'],
            'title': e['title'],
            'date': e['date'],
            'time': e['time'],
            'event_type': e['event_type'],
            'registration_status': registration_status,
            'registration_id': reg['registration_id'] if reg else None
        })
    return render_template('virtual_events.html',
                           events=event_list)
# -------- Audio Guides --------
@app.route('/audio_guides', methods=['GET', 'POST'])
def audio_guides():
    guides = load_audioguides()
    filter_language = ''
    filtered_guides = guides
    if request.method == 'POST':
        filter_language = request.form.get('filter-language', '')
        if filter_language and filter_language != 'All':
            filtered_guides = [g for g in guides if g['language'].lower() == filter_language.lower()]
        else:
            filtered_guides = guides
    return render_template('audio_guides.html',
                           audio_guides=filtered_guides,
                           filter_language=filter_language)
# ========== Run Server ==========
if __name__ == '__main__':
    # Ensure data directory exists
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    app.run(host='0.0.0.0', port=5000, debug=True)