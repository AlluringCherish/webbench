from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

data_dir = 'data'

# Utility functions to read and write data with pipe delimiter

def read_file_lines(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip()]
    except IOError:
        return []


def write_file_lines(filename, lines):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.writelines(line + '\n' for line in lines)
        return True
    except IOError:
        return False

# Reading users (not used in routes but loaded if needed)
def load_users():
    lines = read_file_lines(os.path.join(data_dir, 'users.txt'))
    return [line for line in lines]  # username list

# Galleries
# Fields: gallery_id|gallery_name|floor|capacity|theme|status
# gallery_id:int, floor:int, capacity:int
# Return list of dict

def load_galleries():
    lines = read_file_lines(os.path.join(data_dir, 'galleries.txt'))
    galleries = []
    for line in lines:
        parts = line.split('|')
        if len(parts) == 6:
            galleries.append({
                'gallery_id': int(parts[0]),
                'gallery_name': parts[1],
                'floor': int(parts[2]),
                'capacity': int(parts[3]),
                'theme': parts[4],
                'status': parts[5]
            })
    return galleries

# Exhibitions
# Fields: exhibition_id|title|description|gallery_id|exhibition_type|start_date|end_date|curator_name|created_by
# exhibition_id:int, gallery_id:int

def load_exhibitions():
    lines = read_file_lines(os.path.join(data_dir, 'exhibitions.txt'))
    exhibitions = []
    for line in lines:
        parts = line.split('|')
        if len(parts) == 9:
            exhibitions.append({
                'exhibition_id': int(parts[0]),
                'title': parts[1],
                'description': parts[2],
                'gallery_id': int(parts[3]),
                'exhibition_type': parts[4],
                'start_date': parts[5],
                'end_date': parts[6],
                'curator_name': parts[7],
                'created_by': parts[8]
            })
    return exhibitions

# Artifacts
# Fields: artifact_id|artifact_name|period|origin|description|exhibition_id|storage_location|acquisition_date|added_by
# artifact_id:int, exhibition_id:int

def load_artifacts():
    lines = read_file_lines(os.path.join(data_dir, 'artifacts.txt'))
    artifacts = []
    for line in lines:
        parts = line.split('|')
        if len(parts) == 9:
            artifacts.append({
                'artifact_id': int(parts[0]),
                'artifact_name': parts[1],
                'period': parts[2],
                'origin': parts[3],
                'description': parts[4],
                'exhibition_id': int(parts[5]),
                'storage_location': parts[6],
                'acquisition_date': parts[7],
                'added_by': parts[8]
            })
    return artifacts

# Audio Guides
# Fields: guide_id|exhibit_number|title|language|duration|script|narrator|created_by
# guide_id:int, exhibit_number:int, duration:int

def load_audio_guides():
    lines = read_file_lines(os.path.join(data_dir, 'audioguides.txt'))
    guides = []
    for line in lines:
        parts = line.split('|')
        if len(parts) == 8:
            try:
                duration_val = int(parts[4])
            except ValueError:
                duration_val = 0
            guides.append({
                'guide_id': int(parts[0]),
                'exhibit_number': int(parts[1]),
                'title': parts[2],
                'language': parts[3],
                'duration': duration_val,
                'script': parts[5],
                'narrator': parts[6],
                'created_by': parts[7]
            })
    return guides

# Tickets
# Fields: ticket_id|username|ticket_type|visit_date|visit_time|number_of_tickets|price|visitor_name|visitor_email|purchase_date
# ticket_id:int, number_of_tickets:int, price:int

def load_tickets():
    lines = read_file_lines(os.path.join(data_dir, 'tickets.txt'))
    tickets = []
    for line in lines:
        parts = line.split('|')
        if len(parts) == 10:
            tickets.append({
                'ticket_id': int(parts[0]),
                'username': parts[1],
                'ticket_type': parts[2],
                'visit_date': parts[3],
                'visit_time': parts[4],
                'number_of_tickets': int(parts[5]),
                'price': int(parts[6]),
                'visitor_name': parts[7],
                'visitor_email': parts[8],
                'purchase_date': parts[9]
            })
    return tickets

# Events
# Fields: event_id|title|date|time|event_type|speaker|capacity|description|created_by
# event_id:int, capacity:int

def load_events():
    lines = read_file_lines(os.path.join(data_dir, 'events.txt'))
    events = []
    for line in lines:
        parts = line.split('|')
        if len(parts) == 9:
            try:
                capacity_val = int(parts[6])
            except ValueError:
                capacity_val = 0
            events.append({
                'event_id': int(parts[0]),
                'title': parts[1],
                'date': parts[2],
                'time': parts[3],
                'event_type': parts[4],
                'speaker': parts[5],
                'capacity': capacity_val,
                'description': parts[7],
                'created_by': parts[8]
            })
    return events

# Event Registrations
# Fields: registration_id|event_id|username|registration_date
# registration_id:int, event_id:int

def load_event_registrations():
    lines = read_file_lines(os.path.join(data_dir, 'event_registrations.txt'))
    registrations = []
    for line in lines:
        parts = line.split('|')
        if len(parts) == 4:
            registrations.append({
                'registration_id': int(parts[0]),
                'event_id': int(parts[1]),
                'username': parts[2],
                'registration_date': parts[3]
            })
    return registrations

# Save tickets
# ticket fields as per schema in Section 3

def save_tickets(tickets):
    lines = []
    for t in tickets:
        line = f"{t['ticket_id']}|{t['username']}|{t['ticket_type']}|{t['visit_date']}|{t['visit_time']}|{t['number_of_tickets']}|{t['price']}|{t['visitor_name']}|{t['visitor_email']}|{t['purchase_date']}"
        lines.append(line)
    return write_file_lines(os.path.join(data_dir, 'tickets.txt'), lines)

# Save event registrations
# registration fields as per schema in Section 3

def save_event_registrations(registrations):
    lines = []
    for r in registrations:
        line = f"{r['registration_id']}|{r['event_id']}|{r['username']}|{r['registration_date']}"
        lines.append(line)
    return write_file_lines(os.path.join(data_dir, 'event_registrations.txt'), lines)

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard_page'))

@app.route('/dashboard')
def dashboard_page():
    exhibitions = load_exhibitions()
    total_exhibitions = len(exhibitions)
    # active exhibitions - current date within start and end
    active_exhibitions = 0
    now = datetime.now().date()
    for ex in exhibitions:
        try:
            start = datetime.strptime(ex['start_date'], '%Y-%m-%d').date()
            end = datetime.strptime(ex['end_date'], '%Y-%m-%d').date()
            if start <= now <= end:
                active_exhibitions += 1
        except Exception:
            continue
    return render_template('dashboard.html', total_exhibitions=total_exhibitions, active_exhibitions=active_exhibitions)

@app.route('/artifacts', methods=['GET', 'POST'])
def artifact_catalog_page():
    artifacts = load_artifacts()
    filtered_artifacts = artifacts
    if request.method == 'POST':
        search_term = request.form.get('search_artifact', '').strip().lower()
        if search_term:
            filtered_artifacts = []
            for a in artifacts:
                if search_term in str(a['artifact_id']).lower() or search_term in a['artifact_name'].lower():
                    filtered_artifacts.append(a)
    return render_template('artifact_catalog.html', artifacts=artifacts, filtered_artifacts=filtered_artifacts)

@app.route('/exhibitions', methods=['GET', 'POST'])
def exhibitions_page():
    exhibitions = load_exhibitions()
    filtered_exhibitions = exhibitions
    filter_type = ''
    if request.method == 'POST':
        filter_type = request.form.get('filter_exhibition_type', '')
        if filter_type:
            filtered_exhibitions = [ex for ex in exhibitions if ex['exhibition_type'] == filter_type]
    return render_template('exhibitions.html', exhibitions=exhibitions, filtered_exhibitions=filtered_exhibitions, filter_type=filter_type)

@app.route('/exhibition/<int:exhibition_id>')
def exhibition_details_page(exhibition_id):
    exhibitions = load_exhibitions()
    exhibition = next((ex for ex in exhibitions if ex['exhibition_id'] == exhibition_id), None)
    if exhibition is None:
        return "Exhibition not found", 404
    artifacts = [a for a in load_artifacts() if a['exhibition_id'] == exhibition_id]
    return render_template('exhibition_details.html', exhibition=exhibition, artifacts=artifacts)

@app.route('/tickets', methods=['GET', 'POST'])
def visitor_tickets_page():
    # For simplicity, assume current user is 'visitor_mary'
    current_user = 'visitor_mary'
    tickets = [t for t in load_tickets() if t['username'] == current_user]
    purchase_status = None
    if request.method == 'POST':
        # Fields expected from form:
        # ticket_type, visit_date, visit_time, number_of_tickets, visitor_name, visitor_email
        ticket_type = request.form.get('ticket_type', '').strip()
        visit_date = request.form.get('visit_date', '').strip()
        visit_time = request.form.get('visit_time', '').strip()
        number_of_tickets = request.form.get('number_of_tickets', '').strip()
        visitor_name = request.form.get('visitor_name', '').strip()
        visitor_email = request.form.get('visitor_email', '').strip()

        # Basic validation
        errors = []
        if not ticket_type:
            errors.append('Ticket type is required.')
        if not visit_date:
            errors.append('Visit date is required.')
        if not visit_time:
            errors.append('Visit time is required.')
        try:
            number_of_tickets_int = int(number_of_tickets)
            if number_of_tickets_int < 1:
                errors.append('Number of tickets must be at least 1.')
        except Exception:
            errors.append('Invalid number of tickets.')
        if not visitor_name:
            errors.append('Visitor name is required.')
        if not visitor_email:
            errors.append('Visitor email is required.')

        if errors:
            purchase_status = ' '.join(errors)
        else:
            tickets_all = load_tickets()
            new_ticket_id = max([t['ticket_id'] for t in tickets_all], default=0) + 1
            # Pricing example (simplified): Standard=15, Student=10, Senior=8, Family=25, VIP=50
            prices = {'Standard':15, 'Student':10, 'Senior':8, 'Family':25, 'VIP':50}
            price_per_ticket = prices.get(ticket_type, 15)
            total_price = price_per_ticket * number_of_tickets_int
            purchase_date = datetime.now().strftime('%Y-%m-%d')

            new_ticket = {
                'ticket_id': new_ticket_id,
                'username': current_user,
                'ticket_type': ticket_type,
                'visit_date': visit_date,
                'visit_time': visit_time,
                'number_of_tickets': number_of_tickets_int,
                'price': total_price,
                'visitor_name': visitor_name,
                'visitor_email': visitor_email,
                'purchase_date': purchase_date
            }
            tickets_all.append(new_ticket)
            if save_tickets(tickets_all):
                purchase_status = 'Purchase successful.'
                tickets.append(new_ticket)
            else:
                purchase_status = 'Failed to save ticket. Please try again.'

    return render_template('visitor_tickets.html', tickets=tickets, purchase_status=purchase_status)

@app.route('/events', methods=['GET', 'POST'])
def virtual_events_page():
    # For simplicity, assume current user is 'visitor_mary'
    current_user = 'visitor_mary'
    events = load_events()
    registrations = [r for r in load_event_registrations() if r['username'] == current_user]
    return render_template('virtual_events.html', events=events, registrations=registrations)

@app.route('/register_event/<int:event_id>', methods=['POST'])
def register_for_event(event_id):
    current_user = 'visitor_mary'
    registrations = load_event_registrations()
    # Check if user already registered for event
    if any(r['event_id'] == event_id and r['username'] == current_user for r in registrations):
        return redirect(url_for('virtual_events_page'))
    new_id = max([r['registration_id'] for r in registrations], default=0) + 1
    registration_date = datetime.now().strftime('%Y-%m-%d')
    registrations.append({
        'registration_id': new_id,
        'event_id': event_id,
        'username': current_user,
        'registration_date': registration_date
    })
    save_event_registrations(registrations)
    return redirect(url_for('virtual_events_page'))

@app.route('/cancel_registration/<int:registration_id>', methods=['POST'])
def cancel_event_registration(registration_id):
    current_user = 'visitor_mary'
    registrations = load_event_registrations()
    new_registrations = [r for r in registrations if not (r['registration_id'] == registration_id and r['username'] == current_user)]
    save_event_registrations(new_registrations)
    return redirect(url_for('virtual_events_page'))

@app.route('/audio_guides', methods=['GET', 'POST'])
def audio_guides_page():
    audio_guides = load_audio_guides()
    filtered_guides = audio_guides
    filter_language = ''
    if request.method == 'POST':
        filter_language = request.form.get('filter_language', '')
        if filter_language:
            filtered_guides = [g for g in audio_guides if g['language'] == filter_language]
    return render_template('audio_guides.html', audio_guides=audio_guides, filtered_guides=filtered_guides, filter_language=filter_language)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
