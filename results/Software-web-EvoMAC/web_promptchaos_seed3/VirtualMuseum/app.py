'''
Main backend application for VirtualMuseum web application.
Implements Flask web server with routing for all seven pages:
Dashboard, Artifact Catalog, Exhibitions, Exhibition Details,
Visitor Tickets, Virtual Events, Audio Guides.
Manages reading and writing to local text files in 'data' directory,
implements business logic including filtering, searching, ticket purchasing,
event registration, and audio guide playback.
Website starts from Dashboard page at route '/'.
'''
from flask import Flask, render_template, request, redirect, url_for, flash
import os
from datetime import datetime
app = Flask(__name__)
app.secret_key = 'virtualmuseum_secret_key'  # Needed for flash messages
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
def generate_new_id(lines):
    # lines are full lines from file, first field is id (int)
    max_id = 0
    for line in lines:
        parts = line.split('|')
        try:
            id_ = int(parts[0])
            if id_ > max_id:
                max_id = id_
        except (ValueError, IndexError):
            continue
    return max_id + 1
# --- ROUTES ---
@app.route('/')
def dashboard():
    '''
    Dashboard page showing overview of exhibitions and navigation buttons.
    '''
    exhibitions_lines = read_file_lines('exhibitions.txt')
    total_exhibitions = len(exhibitions_lines)
    active_exhibitions = 0
    today = datetime.today().date()
    for line in exhibitions_lines:
        parts = parse_pipe_line(line, 9)
        if not parts:
            continue
        # exhibition_id|title|description|gallery_id|exhibition_type|start_date|end_date|curator_name|created_by
        start_date_str = parts[5]
        end_date_str = parts[6]
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            if start_date <= today <= end_date:
                active_exhibitions += 1
        except ValueError:
            continue
    # Get username from query param, default to None
    username = request.args.get('username', None)
    return render_template('dashboard.html',
                           total_exhibitions=total_exhibitions,
                           active_exhibitions=active_exhibitions,
                           username=username)
@app.route('/artifact_catalog', methods=['GET', 'POST'])
def artifact_catalog():
    '''
    Artifact Catalog page with search and filter capabilities.
    '''
    artifacts_lines = read_file_lines('artifacts.txt')
    exhibitions_lines = read_file_lines('exhibitions.txt')
    exhibitions_dict = {}
    for line in exhibitions_lines:
        parts = parse_pipe_line(line, 9)
        if parts:
            exhibitions_dict[parts[0]] = parts[1]  # exhibition_id: title
    # Get search and filter parameters
    search_query = ''
    filtered_artifacts = []
    if request.method == 'POST':
        search_query = request.form.get('search-artifact', '').strip().lower()
        # Filter artifacts by name or ID containing search_query
        for line in artifacts_lines:
            parts = parse_pipe_line(line, 9)
            if not parts:
                continue
            artifact_id = parts[0]
            artifact_name = parts[1].lower()
            if search_query in artifact_id.lower() or search_query in artifact_name:
                filtered_artifacts.append(parts)
    else:
        # GET: show all artifacts
        for line in artifacts_lines:
            parts = parse_pipe_line(line, 9)
            if parts:
                filtered_artifacts.append(parts)
    # Prepare data for template: artifact_id, name, period, origin, exhibition title, actions (view/edit not specified)
    artifacts_display = []
    for art in filtered_artifacts:
        exhibition_title = exhibitions_dict.get(art[5], 'N/A')
        artifacts_display.append({
            'artifact_id': art[0],
            'artifact_name': art[1],
            'period': art[2],
            'origin': art[3],
            'exhibition': exhibition_title
        })
    username = request.args.get('username', None)
    return render_template('artifact_catalog.html',
                           artifacts=artifacts_display,
                           search_query=search_query,
                           username=username)
@app.route('/exhibitions', methods=['GET', 'POST'])
def exhibitions():
    '''
    Exhibitions page with filtering by exhibition type.
    '''
    exhibitions_lines = read_file_lines('exhibitions.txt')
    galleries_lines = read_file_lines('galleries.txt')
    galleries_dict = {}
    for line in galleries_lines:
        parts = parse_pipe_line(line, 6)
        if parts:
            galleries_dict[parts[0]] = parts[1]  # gallery_id: gallery_name
    filter_type = ''
    filtered_exhibitions = []
    if request.method == 'POST':
        filter_type = request.form.get('filter-exhibition-type', '')
        for line in exhibitions_lines:
            parts = parse_pipe_line(line, 9)
            if not parts:
                continue
            exhibition_type = parts[4]
            if filter_type == '' or exhibition_type == filter_type:
                filtered_exhibitions.append(parts)
    else:
        # GET: show all exhibitions
        for line in exhibitions_lines:
            parts = parse_pipe_line(line, 9)
            if parts:
                filtered_exhibitions.append(parts)
    # Prepare data for template: title, type, dates, gallery name, status (gallery status)
    exhibitions_display = []
    for ex in filtered_exhibitions:
        gallery_name = galleries_dict.get(ex[3], 'N/A')
        # Determine status from gallery status if possible
        gallery_status = 'Unknown'
        for line in galleries_lines:
            parts = parse_pipe_line(line, 6)
            if parts and parts[0] == ex[3]:
                gallery_status = parts[5]
                break
        exhibitions_display.append({
            'exhibition_id': ex[0],
            'title': ex[1],
            'exhibition_type': ex[4],
            'start_date': ex[5],
            'end_date': ex[6],
            'gallery_name': gallery_name,
            'status': gallery_status
        })
    username = request.args.get('username', None)
    return render_template('exhibitions.html',
                           exhibitions=exhibitions_display,
                           filter_type=filter_type,
                           username=username)
@app.route('/exhibition_details/<exhibition_id>')
def exhibition_details(exhibition_id):
    '''
    Exhibition Details page showing detailed info and artifacts in the exhibition.
    '''
    exhibitions_lines = read_file_lines('exhibitions.txt')
    exhibition = None
    for line in exhibitions_lines:
        parts = parse_pipe_line(line, 9)
        if parts and parts[0] == exhibition_id:
            exhibition = parts
            break
    if not exhibition:
        flash('Exhibition not found.', 'error')
        username = request.args.get('username', None)
        return redirect(url_for('exhibitions', username=username) if username else url_for('exhibitions'))
    # exhibition_id|title|description|gallery_id|exhibition_type|start_date|end_date|curator_name|created_by
    exhibition_title = exhibition[1]
    exhibition_description = exhibition[2]
    exhibition_dates = f"{exhibition[5]} to {exhibition[6]}"
    # Get artifacts in this exhibition
    artifacts_lines = read_file_lines('artifacts.txt')
    exhibition_artifacts = []
    for line in artifacts_lines:
        parts = parse_pipe_line(line, 9)
        if parts and parts[5] == exhibition_id:
            exhibition_artifacts.append({
                'artifact_id': parts[0],
                'artifact_name': parts[1],
                'period': parts[2],
                'origin': parts[3],
                'description': parts[4],
                'storage_location': parts[6],
                'acquisition_date': parts[7],
                'added_by': parts[8]
            })
    username = request.args.get('username', None)
    return render_template('exhibition_details.html',
                           exhibition_title=exhibition_title,
                           exhibition_description=exhibition_description,
                           exhibition_dates=exhibition_dates,
                           artifacts=exhibition_artifacts,
                           username=username)
@app.route('/visitor_tickets', methods=['GET', 'POST'])
def visitor_tickets():
    '''
    Visitor Tickets page for purchasing tickets and viewing user's tickets.
    '''
    # For simplicity, assume username is passed as query param or default visitor
    username = request.args.get('username', 'visitor_mary')
    ticket_types = ['Standard', 'Student', 'Senior', 'Family', 'VIP']
    tickets_lines = read_file_lines('tickets.txt')
    # Filter tickets for this user
    user_tickets = []
    for line in tickets_lines:
        parts = parse_pipe_line(line, 10)
        if parts and parts[1] == username:
            user_tickets.append({
                'ticket_id': parts[0],
                'ticket_type': parts[2],
                'visit_date': parts[3],
                'visit_time': parts[4],
                'number_of_tickets': parts[5],
                'price': parts[6],
                'visitor_name': parts[7],
                'visitor_email': parts[8],
                'purchase_date': parts[9]
            })
    if request.method == 'POST':
        # Process ticket purchase
        ticket_type = request.form.get('ticket-type', '')
        number_of_tickets_str = request.form.get('number-of-tickets', '0')
        visitor_name = request.form.get('visitor-name', '').strip()
        visitor_email = request.form.get('visitor-email', '').strip()
        visit_date = request.form.get('visit-date', '').strip()
        visit_time = request.form.get('visit-time', '').strip()
        # Validate inputs
        error = None
        if ticket_type not in ticket_types:
            error = 'Invalid ticket type selected.'
        try:
            number_of_tickets = int(number_of_tickets_str)
            if number_of_tickets <= 0:
                error = 'Number of tickets must be positive.'
        except ValueError:
            error = 'Number of tickets must be a number.'
        if not visitor_name:
            error = 'Visitor name is required.'
        if not visitor_email or '@' not in visitor_email:
            error = 'Valid visitor email is required.'
        if not visit_date:
            error = 'Visit date is required.'
        if not visit_time:
            error = 'Visit time is required.'
        if error:
            flash(error, 'error')
            return redirect(url_for('visitor_tickets', username=username))
        # Determine price per ticket (example pricing)
        price_map = {
            'Standard': 15,
            'Student': 10,
            'Senior': 12,
            'Family': 40,
            'VIP': 50
        }
        price_per_ticket = price_map.get(ticket_type, 15)
        total_price = price_per_ticket * number_of_tickets
        # Generate new ticket_id
        new_ticket_id = generate_new_id(tickets_lines)
        purchase_date = datetime.today().strftime('%Y-%m-%d')
        new_ticket_line = '|'.join([
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
        tickets_lines.append(new_ticket_line)
        write_file_lines('tickets.txt', tickets_lines)
        flash(f'Tickets purchased successfully! Total price: ${total_price}', 'success')
        return redirect(url_for('visitor_tickets', username=username))
    return render_template('visitor_tickets.html',
                           ticket_types=ticket_types,
                           user_tickets=user_tickets,
                           username=username)
@app.route('/virtual_events', methods=['GET', 'POST'])
def virtual_events():
    '''
    Virtual Events page to view and manage event registrations.
    '''
    # For simplicity, assume username is passed as query param or default visitor
    username = request.args.get('username', 'visitor_mary')
    events_lines = read_file_lines('events.txt')
    registrations_lines = read_file_lines('event_registrations.txt')
    # Build event registrations dict: event_id -> list of usernames
    event_registrations = {}
    registration_id_map = {}  # (event_id, username) -> registration_id
    for line in registrations_lines:
        parts = parse_pipe_line(line, 4)
        if parts:
            reg_id, event_id, reg_username, _ = parts
            event_registrations.setdefault(event_id, []).append(reg_username)
            registration_id_map[(event_id, reg_username)] = reg_id
    # Handle registration and cancellation POST actions
    if request.method == 'POST':
        action = request.form.get('action')
        event_id = request.form.get('event_id')
        if action == 'register':
            # Check if already registered
            if (event_id, username) in registration_id_map:
                flash('You are already registered for this event.', 'error')
            else:
                # Check capacity
                event = None
                for line in events_lines:
                    parts = parse_pipe_line(line, 9)
                    if parts and parts[0] == event_id:
                        event = parts
                        break
                if not event:
                    flash('Event not found.', 'error')
                else:
                    capacity = int(event[6])
                    current_registrations = len(event_registrations.get(event_id, []))
                    if current_registrations >= capacity:
                        flash('Event is full. Cannot register.', 'error')
                    else:
                        # Add registration
                        new_reg_id = generate_new_id(registrations_lines)
                        registration_date = datetime.today().strftime('%Y-%m-%d')
                        new_reg_line = '|'.join([
                            str(new_reg_id),
                            event_id,
                            username,
                            registration_date
                        ])
                        registrations_lines.append(new_reg_line)
                        write_file_lines('event_registrations.txt', registrations_lines)
                        flash('Successfully registered for the event.', 'success')
        elif action == 'cancel':
            reg_id = request.form.get('registration_id')
            # Remove registration by reg_id if belongs to user
            found = False
            new_registrations = []
            for line in registrations_lines:
                parts = parse_pipe_line(line, 4)
                if parts and parts[0] == reg_id and parts[2] == username:
                    found = True
                    continue  # skip this line to remove
                new_registrations.append(line)
            if found:
                write_file_lines('event_registrations.txt', new_registrations)
                flash('Registration cancelled successfully.', 'success')
            else:
                flash('Registration not found or unauthorized.', 'error')
        return redirect(url_for('virtual_events', username=username))
    # Prepare events display with registration status for current user
    events_display = []
    for line in events_lines:
        parts = parse_pipe_line(line, 9)
        if not parts:
            continue
        event_id = parts[0]
        registered = username in event_registrations.get(event_id, [])
        # Find registration_id if registered
        reg_id = registration_id_map.get((event_id, username), None)
        events_display.append({
            'event_id': event_id,
            'title': parts[1],
            'date': parts[2],
            'time': parts[3],
            'event_type': parts[4],
            'speaker': parts[5],
            'capacity': parts[6],
            'description': parts[7],
            'registered': registered,
            'registration_id': reg_id
        })
    return render_template('virtual_events.html',
                           events=events_display,
                           username=username)
@app.route('/audio_guides', methods=['GET', 'POST'])
def audio_guides():
    '''
    Audio Guides page to browse and access audio guides with language filtering.
    '''
    audioguides_lines = read_file_lines('audioguides.txt')
    filter_language = ''
    filtered_guides = []
    if request.method == 'POST':
        filter_language = request.form.get('filter-language', '')
        for line in audioguides_lines:
            parts = parse_pipe_line(line, 8)
            if not parts:
                continue
            language = parts[3]
            if filter_language == '' or language == filter_language:
                filtered_guides.append(parts)
    else:
        # GET: show all guides
        for line in audioguides_lines:
            parts = parse_pipe_line(line, 8)
            if parts:
                filtered_guides.append(parts)
    # Prepare data for template: guide_id, exhibit_number, title, language, duration
    guides_display = []
    for guide in filtered_guides:
        guides_display.append({
            'guide_id': guide[0],
            'exhibit_number': guide[1],
            'title': guide[2],
            'language': guide[3],
            'duration': guide[4]
        })
    username = request.args.get('username', None)
    return render_template('audio_guides.html',
                           audio_guides=guides_display,
                           filter_language=filter_language,
                           username=username)
# Run the app on local port 5000
if __name__ == '__main__':
    # Ensure data directory exists
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    app.run(host='0.0.0.0', port=5000, debug=True)