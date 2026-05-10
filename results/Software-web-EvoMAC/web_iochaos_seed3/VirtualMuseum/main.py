'''
Main backend application for VirtualMuseum web application.
Implements all routing, data handling, and business logic using Flask.
Data is stored and managed in local text files under the 'data' directory.
'''
from flask import Flask, render_template, request, redirect, url_for, flash
import os
from datetime import datetime
app = Flask(__name__)
app.secret_key = 'virtualmuseum_secret_key'  # Needed for flashing messages
DATA_DIR = 'data'
# Utility functions for reading and writing pipe-delimited text files
def read_file_lines(filename):
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        return []
    with open(path, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]
    return lines
def write_file_lines(filename, lines):
    path = os.path.join(DATA_DIR, filename)
    with open(path, 'w', encoding='utf-8') as f:
        for line in lines:
            f.write(line + '\n')
def parse_pipe_line(line, expected_fields):
    parts = line.split('|')
    if len(parts) != expected_fields:
        return None
    return parts
def parse_int(value, default=0):
    try:
        return int(value)
    except Exception:
        return default
def parse_date(date_str):
    try:
        return datetime.strptime(date_str, '%Y-%m-%d').date()
    except Exception:
        return None
def parse_datetime(date_str, time_str):
    try:
        dt_str = f"{date_str} {time_str}"
        return datetime.strptime(dt_str, '%Y-%m-%d %I:%M %p')
    except Exception:
        return None
def format_date(date_obj):
    if not date_obj:
        return ''
    return date_obj.strftime('%Y-%m-%d')
def format_datetime(dt_obj):
    if not dt_obj:
        return ''
    return dt_obj.strftime('%Y-%m-%d %I:%M %p')
# --- Data loading functions ---
def load_users():
    lines = read_file_lines('users.txt')
    return lines  # list of usernames
def load_galleries():
    lines = read_file_lines('galleries.txt')
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
    lines = read_file_lines('exhibitions.txt')
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
    lines = read_file_lines('artifacts.txt')
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
    lines = read_file_lines('audioguides.txt')
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
    lines = read_file_lines('tickets.txt')
    tickets = []
    for line in lines:
        parts = parse_pipe_line(line, 10)
        if parts:
            ticket = {
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
            }
            tickets.append(ticket)
    return tickets
def load_events():
    lines = read_file_lines('events.txt')
    events = []
    for line in lines:
        parts = parse_pipe_line(line, 9)
        if parts:
            event = {
                'event_id': parts[0],
                'title': parts[1],
                'date': parts[2],
                'time': parts[3],
                'event_type': parts[4],
                'speaker': parts[5],
                'capacity': parts[6],
                'description': parts[7],
                'created_by': parts[8]
            }
            events.append(event)
    return events
def load_event_registrations():
    lines = read_file_lines('event_registrations.txt')
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
    lines = read_file_lines('collection_logs.txt')
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
# --- Save functions for tickets and event registrations (write operations) ---
def save_tickets(tickets):
    lines = []
    for t in tickets:
        line = '|'.join([
            str(t['ticket_id']),
            t['username'],
            t['ticket_type'],
            t['visit_date'],
            t['visit_time'],
            str(t['number_of_tickets']),
            str(t['price']),
            t['visitor_name'],
            t['visitor_email'],
            t['purchase_date']
        ])
        lines.append(line)
    write_file_lines('tickets.txt', lines)
def save_event_registrations(registrations):
    lines = []
    for r in registrations:
        line = '|'.join([
            str(r['registration_id']),
            r['event_id'],
            r['username'],
            r['registration_date']
        ])
        lines.append(line)
    write_file_lines('event_registrations.txt', lines)
# --- Helper functions ---
def get_next_id(items, id_key):
    max_id = 0
    for item in items:
        try:
            item_id = int(item[id_key])
            if item_id > max_id:
                max_id = item_id
        except Exception:
            continue
    return max_id + 1
def is_exhibition_active(exhibition):
    today = datetime.today().date()
    start = parse_date(exhibition['start_date'])
    end = parse_date(exhibition['end_date'])
    if start and end:
        return start <= today <= end
    return False
def calculate_ticket_price(ticket_type, number_of_tickets):
    # Prices per ticket type (example prices)
    prices = {
        'Standard': 15,
        'Student': 10,
        'Senior': 12,
        'Family': 40,
        'VIP': 50
    }
    price_per_ticket = prices.get(ticket_type, 15)
    return price_per_ticket * number_of_tickets
# --- Routes ---
@app.route('/')
def dashboard():
    exhibitions = load_exhibitions()
    total_exhibitions = len(exhibitions)
    active_exhibitions = sum(1 for e in exhibitions if is_exhibition_active(e))
    return render_template('dashboard.html',
                           exhibition_summary={
                               'total': total_exhibitions,
                               'active': active_exhibitions
                           })
@app.route('/artifact_catalog', methods=['GET', 'POST'])
def artifact_catalog():
    artifacts = load_artifacts()
    exhibitions = load_exhibitions()
    exhibition_dict = {e['exhibition_id']: e['title'] for e in exhibitions}
    search_query = ''
    filtered_artifacts = artifacts
    if request.method == 'POST':
        search_query = request.form.get('search-artifact', '').strip().lower()
        if search_query:
            filtered_artifacts = []
            for artifact in artifacts:
                if (search_query in artifact['artifact_name'].lower()) or (search_query == artifact['artifact_id']):
                    filtered_artifacts.append(artifact)
    # Add exhibition title to each artifact for display
    for artifact in filtered_artifacts:
        artifact['exhibition_title'] = exhibition_dict.get(artifact['exhibition_id'], 'N/A')
    return render_template('artifact_catalog.html',
                           artifacts=filtered_artifacts,
                           search_query=search_query)
@app.route('/exhibitions', methods=['GET', 'POST'])
def exhibitions():
    exhibitions = load_exhibitions()
    galleries = load_galleries()
    gallery_dict = {g['gallery_id']: g['gallery_name'] for g in galleries}
    filter_type = ''
    filtered_exhibitions = exhibitions
    if request.method == 'POST':
        filter_type = request.form.get('filter-exhibition-type', '')
        if filter_type and filter_type != 'All':
            filtered_exhibitions = [
                e for e in exhibitions if e['exhibition_type'].lower() == filter_type.lower()]
    # Add gallery name and status for display
    for exhibition in filtered_exhibitions:
        exhibition['gallery_name'] = gallery_dict.get(exhibition['gallery_id'], 'N/A')
        # Determine status based on current date and exhibition dates
        today = datetime.today().date()
        start = parse_date(exhibition['start_date'])
        end = parse_date(exhibition['end_date'])
        if start and end:
            if start <= today <= end:
                exhibition['status'] = 'Active'
            elif today < start:
                exhibition['status'] = 'Upcoming'
            else:
                exhibition['status'] = 'Ended'
        else:
            exhibition['status'] = 'Unknown'
    return render_template('exhibitions.html',
                           exhibitions=filtered_exhibitions,
                           filter_type=filter_type)
@app.route('/exhibition_details/<exhibition_id>')
def exhibition_details(exhibition_id):
    exhibitions = load_exhibitions()
    artifacts = load_artifacts()
    exhibition = next(
        (e for e in exhibitions if e['exhibition_id'] == exhibition_id), None)
    if not exhibition:
        flash('Exhibition not found.', 'error')
        return redirect(url_for('exhibitions'))
    exhibition_artifacts = [
        a for a in artifacts if a['exhibition_id'] == exhibition_id]
    return render_template('exhibition_details.html',
                           exhibition=exhibition,
                           artifacts=exhibition_artifacts)
@app.route('/visitor_tickets', methods=['GET', 'POST'])
def visitor_tickets():
    tickets = load_tickets()
    # For demonstration, assume username is visitor_mary (no auth implemented)
    current_username = 'visitor_mary'
    user_tickets = [t for t in tickets if t['username'] == current_username]
    if request.method == 'POST':
        ticket_type = request.form.get('ticket-type', '')
        number_of_tickets_str = request.form.get('number-of-tickets', '0')
        visitor_name = request.form.get('visitor-name', '').strip()
        visitor_email = request.form.get('visitor-email', '').strip()
        visit_date = request.form.get('visit-date', '').strip()
        visit_time = request.form.get('visit-time', '').strip()
        # Validate inputs
        try:
            number_of_tickets = int(number_of_tickets_str)
            if number_of_tickets <= 0:
                raise ValueError
        except Exception:
            flash('Please enter a valid number of tickets.', 'error')
            return redirect(url_for('visitor_tickets'))
        if not ticket_type:
            flash('Please select a ticket type.', 'error')
            return redirect(url_for('visitor_tickets'))
        if not visitor_name or not visitor_email:
            flash('Please enter visitor name and email.', 'error')
            return redirect(url_for('visitor_tickets'))
        if not visit_date:
            flash('Please select a visit date.', 'error')
            return redirect(url_for('visitor_tickets'))
        if not visit_time:
            flash('Please select a visit time.', 'error')
            return redirect(url_for('visitor_tickets'))
        # Calculate price
        price = calculate_ticket_price(ticket_type, number_of_tickets)
        # Generate new ticket_id
        new_ticket_id = get_next_id(tickets, 'ticket_id')
        purchase_date = datetime.today().strftime('%Y-%m-%d')
        new_ticket = {
            'ticket_id': str(new_ticket_id),
            'username': current_username,
            'ticket_type': ticket_type,
            'visit_date': visit_date,
            'visit_time': visit_time,
            'number_of_tickets': str(number_of_tickets),
            'price': str(price),
            'visitor_name': visitor_name,
            'visitor_email': visitor_email,
            'purchase_date': purchase_date
        }
        tickets.append(new_ticket)
        save_tickets(tickets)
        flash('Ticket purchase successful!', 'success')
        return redirect(url_for('visitor_tickets'))
    return render_template('visitor_tickets.html',
                           tickets=user_tickets)
@app.route('/virtual_events', methods=['GET', 'POST'])
def virtual_events():
    events = load_events()
    registrations = load_event_registrations()
    # For demonstration, assume username is visitor_mary (no auth implemented)
    current_username = 'visitor_mary'
    # Build registration lookup by event_id and username
    user_registrations = {
        r['event_id']: r for r in registrations if r['username'] == current_username}
    if request.method == 'POST':
        # Determine if register or cancel action
        action = request.form.get('action')
        event_id = request.form.get('event_id')
        if action == 'register':
            # Check if already registered
            if event_id in user_registrations:
                flash('You are already registered for this event.', 'error')
                return redirect(url_for('virtual_events'))
            # Check capacity
            event = next((e for e in events if e['event_id'] == event_id), None)
            if not event:
                flash('Event not found.', 'error')
                return redirect(url_for('virtual_events'))
            capacity = parse_int(event['capacity'], 0)
            # Count current registrations for this event
            current_reg_count = sum(
                1 for r in registrations if r['event_id'] == event_id)
            if current_reg_count >= capacity:
                flash('Event capacity reached. Cannot register.', 'error')
                return redirect(url_for('virtual_events'))
            # Add registration
            new_reg_id = get_next_id(registrations, 'registration_id')
            registration_date = datetime.today().strftime('%Y-%m-%d')
            new_registration = {
                'registration_id': str(new_reg_id),
                'event_id': event_id,
                'username': current_username,
                'registration_date': registration_date
            }
            registrations.append(new_registration)
            save_event_registrations(registrations)
            flash('Successfully registered for the event.', 'success')
            return redirect(url_for('virtual_events'))
        elif action == 'cancel':
            registration_id = request.form.get('registration_id')
            # Remove registration if exists and belongs to user
            reg_to_remove = next(
                (r for r in registrations if r['registration_id'] == registration_id and r['username'] == current_username), None)
            if reg_to_remove:
                registrations.remove(reg_to_remove)
                save_event_registrations(registrations)
                flash('Registration cancelled.', 'success')
            else:
                flash('Registration not found or unauthorized.', 'error')
            return redirect(url_for('virtual_events'))
    # Prepare event list with registration status for current user
    event_list = []
    for event in events:
        reg = next(
            (r for r in registrations if r['event_id'] == event['event_id'] and r['username'] == current_username), None)
        event_copy = event.copy()
        event_copy['registered'] = reg is not None
        event_copy['registration_id'] = reg['registration_id'] if reg else None
        event_list.append(event_copy)
    return render_template('virtual_events.html',
                           events=event_list)
@app.route('/audio_guides', methods=['GET', 'POST'])
def audio_guides():
    guides = load_audioguides()
    filter_language = ''
    filtered_guides = guides
    if request.method == 'POST':
        filter_language = request.form.get('filter-language', '')
        if filter_language and filter_language != 'All':
            filtered_guides = [
                g for g in guides if g['language'].lower() == filter_language.lower()]
    return render_template('audio_guides.html',
                           audio_guides=filtered_guides,
                           filter_language=filter_language)
# Run the app on local port 5000
if __name__ == '__main__':
    # Ensure data directory exists
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    app.run(host='0.0.0.0', port=5000, debug=True)