'''
Flask backend application for VirtualMuseum web application.
Implements all required routes and logic to serve pages and handle data from local text files.
Ensures data loading, error handling, and template rendering according to requirements.
'''
import os
from flask import Flask, render_template, request, redirect, url_for, flash, abort
app = Flask(__name__)
app.secret_key = 'virtualmuseum_secret_key'  # Needed for flashing messages
DATA_DIR = 'data'
def read_file_lines(filename):
    filepath = os.path.join(DATA_DIR, filename)
    if not os.path.exists(filepath):
        return None
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.read().strip().split('\n')
    return lines
def parse_pipe_delimited(lines, expected_fields):
    '''
    Parses lines of pipe-delimited text into list of dicts with keys from expected_fields.
    Returns list of dicts.
    '''
    data = []
    for line in lines:
        parts = line.split('|')
        if len(parts) != len(expected_fields):
            continue  # skip malformed lines
        entry = dict(zip(expected_fields, parts))
        data.append(entry)
    return data
@app.route('/')
def dashboard():
    # Load exhibitions to show summary
    lines = read_file_lines('exhibitions.txt')
    if lines is None:
        flash("Exhibition data file is missing.", "error")
        exhibitions = []
    else:
        exhibitions = parse_pipe_delimited(lines, ['exhibition_id','title','description','gallery_id','exhibition_type','start_date','end_date','curator_name','created_by'])
    total_exhibitions = len(exhibitions)
    # Count active exhibitions (current date between start_date and end_date)
    from datetime import datetime
    today = datetime.today().date()
    active_exhibitions = 0
    for ex in exhibitions:
        try:
            start = datetime.strptime(ex['start_date'], '%Y-%m-%d').date()
            end = datetime.strptime(ex['end_date'], '%Y-%m-%d').date()
            if start <= today <= end:
                active_exhibitions += 1
        except Exception:
            continue
    return render_template('dashboard.html',
                           total_exhibitions=total_exhibitions,
                           active_exhibitions=active_exhibitions)
@app.route('/artifact_catalog', methods=['GET', 'POST'])
def artifact_catalog():
    lines = read_file_lines('artifacts.txt')
    if lines is None:
        flash("Artifact data file is missing.", "error")
        artifacts = []
    else:
        artifacts = parse_pipe_delimited(lines, ['artifact_id','artifact_name','period','origin','description','exhibition_id','storage_location','acquisition_date','added_by'])
    # Load exhibitions for exhibition name mapping
    ex_lines = read_file_lines('exhibitions.txt')
    exhibitions = []
    if ex_lines:
        exhibitions = parse_pipe_delimited(ex_lines, ['exhibition_id','title','description','gallery_id','exhibition_type','start_date','end_date','curator_name','created_by'])
    exhibition_map = {ex['exhibition_id']: ex['title'] for ex in exhibitions}
    search_query = ''
    filtered_artifacts = artifacts
    if request.method == 'POST':
        search_query = request.form.get('search-artifact', '').strip().lower()
        if search_query:
            filtered_artifacts = [a for a in artifacts if search_query in a['artifact_name'].lower() or search_query == a['artifact_id']]
    return render_template('artifact_catalog.html',
                           artifacts=filtered_artifacts,
                           exhibition_map=exhibition_map,
                           search_query=search_query)
@app.route('/exhibitions', methods=['GET', 'POST'])
def exhibitions():
    lines = read_file_lines('exhibitions.txt')
    if lines is None:
        flash("Exhibition data file is missing.", "error")
        exhibitions = []
    else:
        exhibitions = parse_pipe_delimited(lines, ['exhibition_id','title','description','gallery_id','exhibition_type','start_date','end_date','curator_name','created_by'])
    # Load galleries for gallery name mapping
    gallery_lines = read_file_lines('galleries.txt')
    galleries = []
    if gallery_lines:
        galleries = parse_pipe_delimited(gallery_lines, ['gallery_id','gallery_name','floor','capacity','theme','status'])
    gallery_map = {g['gallery_id']: g['gallery_name'] for g in galleries}
    filter_type = ''
    filtered_exhibitions = exhibitions
    if request.method == 'POST':
        filter_type = request.form.get('filter-exhibition-type', '')
        if filter_type and filter_type != 'All':
            filtered_exhibitions = [ex for ex in exhibitions if ex['exhibition_type'].lower() == filter_type.lower()]
    return render_template('exhibitions.html',
                           exhibitions=filtered_exhibitions,
                           gallery_map=gallery_map,
                           filter_type=filter_type)
@app.route('/exhibition_details/<exhibition_id>')
def exhibition_details(exhibition_id):
    # Load exhibition details
    ex_lines = read_file_lines('exhibitions.txt')
    if ex_lines is None:
        flash("Exhibition data file is missing.", "error")
        return redirect(url_for('exhibitions'))
    exhibitions = parse_pipe_delimited(ex_lines, ['exhibition_id','title','description','gallery_id','exhibition_type','start_date','end_date','curator_name','created_by'])
    exhibition = next((ex for ex in exhibitions if ex['exhibition_id'] == exhibition_id), None)
    if exhibition is None:
        flash(f"Exhibition with ID {exhibition_id} not found.", "error")
        return redirect(url_for('exhibitions'))
    # Load artifacts for this exhibition
    artifact_lines = read_file_lines('artifacts.txt')
    artifacts = []
    if artifact_lines:
        artifacts = parse_pipe_delimited(artifact_lines, ['artifact_id','artifact_name','period','origin','description','exhibition_id','storage_location','acquisition_date','added_by'])
    exhibition_artifacts = [a for a in artifacts if a['exhibition_id'] == exhibition_id]
    return render_template('exhibition_details.html',
                           exhibition=exhibition,
                           artifacts=exhibition_artifacts)
@app.route('/visitor_tickets', methods=['GET', 'POST'])
def visitor_tickets():
    # For simplicity, assume username is visitor_mary (in real app, would be from session)
    username = 'visitor_mary'
    # Load tickets for this user
    ticket_lines = read_file_lines('tickets.txt')
    tickets = []
    if ticket_lines:
        tickets = parse_pipe_delimited(ticket_lines, ['ticket_id','username','ticket_type','visit_date','visit_time','number_of_tickets','price','visitor_name','visitor_email','purchase_date'])
    user_tickets = [t for t in tickets if t['username'] == username]
    ticket_types = ['Standard', 'Student', 'Senior', 'Family', 'VIP']
    if request.method == 'POST':
        ticket_type = request.form.get('ticket-type', '')
        number_of_tickets = request.form.get('number-of-tickets', '')
        visitor_name = request.form.get('visitor-name', '')
        visitor_email = request.form.get('visitor-email', '')
        visit_date = request.form.get('visit-date', '')
        visit_time = request.form.get('visit-time', '')
        # Basic validation
        if not ticket_type or ticket_type not in ticket_types:
            flash("Please select a valid ticket type.", "error")
        elif not number_of_tickets.isdigit() or int(number_of_tickets) <= 0:
            flash("Please enter a valid number of tickets.", "error")
        elif not visitor_name.strip():
            flash("Please enter visitor name.", "error")
        elif not visitor_email.strip():
            flash("Please enter visitor email.", "error")
        elif not visit_date.strip():
            flash("Please enter visit date.", "error")
        elif not visit_time.strip():
            flash("Please enter visit time.", "error")
        else:
            # Calculate price (example prices)
            price_map = {'Standard':15, 'Student':10, 'Senior':12, 'Family':40, 'VIP':50}
            price = price_map.get(ticket_type, 0) * int(number_of_tickets)
            # Generate new ticket_id
            new_id = 1
            if tickets:
                try:
                    new_id = max(int(t['ticket_id']) for t in tickets) + 1
                except Exception:
                    new_id = 1
            from datetime import datetime
            purchase_date = datetime.today().strftime('%Y-%m-%d')
            new_ticket_line = f"{new_id}|{username}|{ticket_type}|{visit_date}|{visit_time}|{number_of_tickets}|{price}|{visitor_name}|{visitor_email}|{purchase_date}\n"
            # Append to tickets.txt
            try:
                with open(os.path.join(DATA_DIR, 'tickets.txt'), 'a', encoding='utf-8') as f:
                    f.write(new_ticket_line)
                flash("Ticket purchase successful.", "success")
                return redirect(url_for('visitor_tickets'))
            except Exception as e:
                flash(f"Failed to save ticket: {str(e)}", "error")
    return render_template('visitor_tickets.html',
                           tickets=user_tickets,
                           ticket_types=ticket_types)
@app.route('/virtual_events', methods=['GET', 'POST'])
def virtual_events():
    # Assume username visitor_mary for demo
    username = 'visitor_mary'
    event_lines = read_file_lines('events.txt')
    events = []
    if event_lines:
        events = parse_pipe_delimited(event_lines, ['event_id','title','date','time','event_type','speaker','capacity','description','created_by'])
    registration_lines = read_file_lines('event_registrations.txt')
    registrations = []
    if registration_lines:
        registrations = parse_pipe_delimited(registration_lines, ['registration_id','event_id','username','registration_date'])
    # Build registration map for current user
    user_registrations = {r['event_id']: r for r in registrations if r['username'] == username}
    if request.method == 'POST':
        # Determine if register or cancel
        for event in events:
            register_btn = f'register-event-button-{event["event_id"]}'
            cancel_btn = f'cancel-registration-button-{event["event_id"]}'
            if register_btn in request.form:
                # Register user for event
                if event['event_id'] in user_registrations:
                    flash("You are already registered for this event.", "info")
                else:
                    # Generate new registration_id
                    new_reg_id = 1
                    if registrations:
                        try:
                            new_reg_id = max(int(r['registration_id']) for r in registrations) + 1
                        except Exception:
                            new_reg_id = 1
                    from datetime import datetime
                    reg_date = datetime.today().strftime('%Y-%m-%d')
                    new_reg_line = f"{new_reg_id}|{event['event_id']}|{username}|{reg_date}\n"
                    try:
                        with open(os.path.join(DATA_DIR, 'event_registrations.txt'), 'a', encoding='utf-8') as f:
                            f.write(new_reg_line)
                        flash(f"Registered for event '{event['title']}'.", "success")
                        return redirect(url_for('virtual_events'))
                    except Exception as e:
                        flash(f"Failed to register: {str(e)}", "error")
                break
            elif cancel_btn in request.form:
                # Cancel registration
                reg_to_cancel = None
                for r in registrations:
                    if r['event_id'] == event['event_id'] and r['username'] == username:
                        reg_to_cancel = r
                        break
                if reg_to_cancel:
                    try:
                        # Remove registration line from file
                        filepath = os.path.join(DATA_DIR, 'event_registrations.txt')
                        with open(filepath, 'r', encoding='utf-8') as f:
                            lines = f.readlines()
                        with open(filepath, 'w', encoding='utf-8') as f:
                            for line in lines:
                                if not line.startswith(reg_to_cancel['registration_id'] + '|'):
                                    f.write(line)
                        flash(f"Cancelled registration for event '{event['title']}'.", "success")
                        return redirect(url_for('virtual_events'))
                    except Exception as e:
                        flash(f"Failed to cancel registration: {str(e)}", "error")
                else:
                    flash("Registration not found.", "error")
                break
    # Prepare event list with registration status for current user
    event_list = []
    for event in events:
        registered = event['event_id'] in user_registrations
        event_list.append({
            'event_id': event['event_id'],
            'title': event['title'],
            'date': event['date'],
            'time': event['time'],
            'event_type': event['event_type'],
            'registration_status': 'Registered' if registered else 'Not Registered'
        })
    return render_template('virtual_events.html', events=event_list)
@app.route('/audio_guides', methods=['GET', 'POST'])
def audio_guides():
    lines = read_file_lines('audioguides.txt')
    if lines is None:
        flash("Audio guide data file is missing.", "error")
        guides = []
    else:
        guides = parse_pipe_delimited(lines, ['guide_id','exhibit_number','title','language','duration','script','narrator','created_by'])
    filter_language = ''
    filtered_guides = guides
    if request.method == 'POST':
        filter_language = request.form.get('filter-language', '')
        if filter_language and filter_language != 'All':
            filtered_guides = [g for g in guides if g['language'].lower() == filter_language.lower()]
    return render_template('audio_guides.html',
                           guides=filtered_guides,
                           filter_language=filter_language)
# Error handlers for 404 and 500
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
@app.errorhandler(500)
def internal_error(e):
    return render_template('500.html'), 500
if __name__ == '__main__':
    # Ensure data directory exists before running
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    app.run(debug=True)