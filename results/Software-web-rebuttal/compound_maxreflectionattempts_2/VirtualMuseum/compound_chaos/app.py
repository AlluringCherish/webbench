from flask import Flask, render_template, request, redirect, url_for, abort
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'


# Helper functions for reading and writing pipe-delimited files

def read_lines(filename):
    try:
        with open(os.path.join(DATA_DIR, filename), 'r', encoding='utf-8') as f:
            lines = f.readlines()
        return [line.strip() for line in lines if line.strip()]
    except FileNotFoundError:
        return []
    except IOError:
        return []


def write_lines(filename, lines):
    try:
        with open(os.path.join(DATA_DIR, filename), 'w', encoding='utf-8') as f:
            for line in lines:
                f.write(line + '\n')
        return True
    except IOError:
        return False


# ========== Root Route ===========
@app.route('/')
def root():
    return redirect(url_for('dashboard'))


# ========== Dashboard Route ===========
@app.route('/dashboard')
def dashboard():
    # Read exhibitions data
    exhibition_lines = read_lines('exhibitions.txt')
    total_exhibitions = len(exhibition_lines)

    # active exhibitions = today between start_date and end_date inclusive
    active_exhibitions = 0
    today = datetime.now().date()

    for line in exhibition_lines:
        parts = line.split('|')
        if len(parts) < 9:
            continue
        try:
            start_date = datetime.strptime(parts[5], '%Y-%m-%d').date()
            end_date = datetime.strptime(parts[6], '%Y-%m-%d').date()
            if start_date <= today <= end_date:
                active_exhibitions += 1
        except Exception:
            continue

    exhibitions_summary = {
        'total_exhibitions': total_exhibitions,
        'active_exhibitions': active_exhibitions
    }

    # Optional user for authentication - not specified means no auth, so pass None
    user = None

    return render_template('dashboard.html', exhibitions_summary=exhibitions_summary, user=user)


# ========== Artifacts Route ===========
@app.route('/artifacts', methods=['GET', 'POST'])
def artifact_catalog():
    # Read artifacts file
    artifact_lines = read_lines('artifacts.txt')
    artifacts = []

    for line in artifact_lines:
        parts = line.split('|')
        if len(parts) < 9:
            continue
        try:
            artifact = {
                'artifact_id': int(parts[0]),
                'artifact_name': parts[1],
                'period': parts[2],
                'origin': parts[3],
                'description': parts[4],
                'exhibition_id': int(parts[5]),
                'storage_location': parts[6],
                'acquisition_date': parts[7],
                'added_by': parts[8]
            }
            artifacts.append(artifact)
        except Exception:
            continue

    filtered = False

    if request.method == 'POST':
        search = request.form.get('search-artifact', '').strip()
        if search:
            filtered = True
            filtered_artifacts = []
            # Try to match by artifact_id (int) or artifact_name (str case insensitive)
            try:
                search_id = int(search)
            except ValueError:
                search_id = None
            search_lower = search.lower()

            for a in artifacts:
                if search_id is not None and a['artifact_id'] == search_id:
                    filtered_artifacts.append(a)
                    continue
                if search_lower in a['artifact_name'].lower():
                    filtered_artifacts.append(a)
            artifacts = filtered_artifacts
    
    return render_template('artifacts.html', artifacts=artifacts, filtered=filtered)


# ========== Exhibitions Route ===========
@app.route('/exhibitions', methods=['GET', 'POST'])
def exhibitions_list():
    exhibition_lines = read_lines('exhibitions.txt')
    exhibitions = []

    for line in exhibition_lines:
        parts = line.split('|')
        if len(parts) < 9:
            continue
        try:
            exhibition = {
                'exhibition_id': int(parts[0]),
                'title': parts[1],
                'description': parts[2],
                'gallery_id': int(parts[3]),
                'exhibition_type': parts[4],
                'start_date': parts[5],
                'end_date': parts[6],
                'curator_name': parts[7],
                'created_by': parts[8]
            }
            exhibitions.append(exhibition)
        except Exception:
            continue

    filter_type = ''
    if request.method == 'POST':
        filter_type = request.form.get('filter-exhibition-type', '')
        if filter_type:
            exhibitions = [e for e in exhibitions if e['exhibition_type'] == filter_type]

    return render_template('exhibitions.html', exhibitions=exhibitions, filter_type=filter_type)


# ========== Exhibition Details Route ===========
@app.route('/exhibition/<int:exhibition_id>', methods=['GET'])
def exhibition_details(exhibition_id):
    # Read exhibitions
    exhibition_lines = read_lines('exhibitions.txt')
    exhibition = None

    for line in exhibition_lines:
        parts = line.split('|')
        if len(parts) < 9:
            continue
        try:
            eid = int(parts[0])
            if eid == exhibition_id:
                exhibition = {
                    'exhibition_id': eid,
                    'title': parts[1],
                    'description': parts[2],
                    'gallery_id': int(parts[3]),
                    'exhibition_type': parts[4],
                    'start_date': parts[5],
                    'end_date': parts[6],
                    'curator_name': parts[7],
                    'created_by': parts[8]
                }
                break
        except Exception:
            continue

    if exhibition is None:
        abort(404)

    # Read artifacts belonging to exhibition
    artifact_lines = read_lines('artifacts.txt')
    artifacts = []
    for line in artifact_lines:
        parts = line.split('|')
        if len(parts) < 9:
            continue
        try:
            if int(parts[5]) == exhibition_id:
                artifact = {
                    'artifact_id': int(parts[0]),
                    'artifact_name': parts[1],
                    'period': parts[2],
                    'origin': parts[3],
                    'description': parts[4],
                    'exhibition_id': int(parts[5]),
                    'storage_location': parts[6],
                    'acquisition_date': parts[7],
                    'added_by': parts[8]
                }
                artifacts.append(artifact)
        except Exception:
            continue

    return render_template('exhibition_details.html', exhibition=exhibition, artifacts=artifacts)


# ========== Visitor Tickets Route ===========
@app.route('/tickets', methods=['GET', 'POST'])
def visitor_tickets():
    # Read tickets
    ticket_lines = read_lines('tickets.txt')
    tickets = []

    for line in ticket_lines:
        parts = line.split('|')
        if len(parts) < 10:
            continue
        try:
            ticket = {
                'ticket_id': int(parts[0]),
                'username': parts[1],
                'ticket_type': parts[2],
                'visit_date': parts[3],
                'visit_time': parts[4],
                'number_of_tickets': int(parts[5]),
                'price': float(parts[6]),
                'visitor_name': parts[7],
                'visitor_email': parts[8],
                'purchase_date': parts[9]
            }
            tickets.append(ticket)
        except Exception:
            continue

    current_user = None

    # POST to buy tickets
    if request.method == 'POST':
        # We expect form fields: ticket_type, visit_date, visit_time, number_of_tickets, visitor_name, visitor_email
        ticket_type = request.form.get('ticket-type', '').strip()
        visit_date = request.form.get('visit-date', '').strip()
        visit_time = request.form.get('visit-time', '').strip()
        number_of_tickets_str = request.form.get('number-of-tickets', '').strip()
        visitor_name = request.form.get('visitor-name', '').strip()
        visitor_email = request.form.get('visitor-email', '').strip()
        # For simplicity, assume fixed prices per ticket_type (not specified in spec)
        ticket_prices = {
            'Standard': 15.0,
            'Student': 10.0,
            'Senior': 12.0,
            'Family': 40.0,
            'VIP': 50.0
        }
        # Validate input
        try:
            number_of_tickets = int(number_of_tickets_str)
        except ValueError:
            number_of_tickets = 0

        price_per_ticket = ticket_prices.get(ticket_type, 0.0)
        total_price = price_per_ticket * number_of_tickets

        if not ticket_type or not visit_date or not visit_time or number_of_tickets <= 0 or not visitor_name or not visitor_email:
            # invalid input, no purchase
            return redirect(url_for('visitor_tickets'))

        # Determine new ticket_id
        next_ticket_id = 1
        if tickets:
            next_ticket_id = max(t['ticket_id'] for t in tickets) + 1

        purchase_date = datetime.now().strftime('%Y-%m-%d')

        new_ticket_line = f"{next_ticket_id}|{visitor_email.split('@')[0]}|{ticket_type}|{visit_date}|{visit_time}|{number_of_tickets}|{total_price}|{visitor_name}|{visitor_email}|{purchase_date}"

        # Append to tickets.txt
        try:
            with open(os.path.join(DATA_DIR, 'tickets.txt'), 'a', encoding='utf-8') as f:
                f.write(new_ticket_line + '\n')
        except Exception:
            # fail silently
            pass

        return redirect(url_for('visitor_tickets'))

    # Show tickets for all users, but current user from referrer? Since no auth, set current_user=None
    current_user = None

    return render_template('visitor_tickets.html', tickets=tickets, current_user=current_user)


# ========== Virtual Events Route ===========
@app.route('/events', methods=['GET', 'POST'])
def virtual_events():
    # Read events
    event_lines = read_lines('events.txt')
    events = []

    for line in event_lines:
        parts = line.split('|')
        if len(parts) < 9:
            continue
        try:
            event = {
                'event_id': int(parts[0]),
                'title': parts[1],
                'date': parts[2],
                'time': parts[3],
                'event_type': parts[4],
                'speaker': parts[5],
                'capacity': int(parts[6]),
                'description': parts[7],
                'created_by': parts[8]
            }
            events.append(event)
        except Exception:
            continue

    # Read registrations
    reg_lines = read_lines('event_registrations.txt')
    registrations = []
    for line in reg_lines:
        parts = line.split('|')
        if len(parts) < 4:
            continue
        try:
            registration = {
                'registration_id': int(parts[0]),
                'event_id': int(parts[1]),
                'username': parts[2],
                'registration_date': parts[3]
            }
            registrations.append(registration)
        except Exception:
            continue

    current_user = None
    filter_username = None

    if request.method == 'POST':
        # No explicit form field specified for filtering or updates in spec, so no filtering applied here
        pass

    # Filter registrations for current user (if any)
    user_registrations = registrations
    if current_user:
        user_registrations = [r for r in registrations if r['username'] == current_user]

    return render_template('virtual_events.html', events=events, user_registrations=user_registrations, current_user=current_user)


# ========== Event Registration Route ===========
@app.route('/events/register/<int:event_id>', methods=['POST'])
def register_event(event_id):
    # Read events
    event_lines = read_lines('events.txt')
    event = None
    for line in event_lines:
        parts = line.split('|')
        if len(parts) < 9:
            continue
        try:
            eid = int(parts[0])
            if eid == event_id:
                event = True
                break
        except Exception:
            continue
    if not event:
        abort(404)

    # Read registrations
    reg_lines = read_lines('event_registrations.txt')
    registrations = []
    max_reg_id = 0
    for line in reg_lines:
        parts = line.split('|')
        if len(parts) < 4:
            continue
        try:
            rid = int(parts[0])
            if rid > max_reg_id:
                max_reg_id = rid
            registrations.append(parts)
        except Exception:
            continue

    # As no authentication, assume user unknown, reject adding - but spec wants redirect after process
    # So just do nothing and redirect
    return redirect(url_for('virtual_events'))


# ========== Event Cancellation Route ===========
@app.route('/events/cancel/<int:registration_id>', methods=['POST'])
def cancel_registration(registration_id):
    # Read registrations
    reg_lines = read_lines('event_registrations.txt')
    new_reg_lines = []
    for line in reg_lines:
        parts = line.split('|')
        if len(parts) < 4:
            new_reg_lines.append(line)
            continue
        try:
            rid = int(parts[0])
            if rid != registration_id:
                new_reg_lines.append(line)
        except Exception:
            new_reg_lines.append(line)

    # Write back
    write_lines('event_registrations.txt', new_reg_lines)

    return redirect(url_for('virtual_events'))


# ========== Audio Guides Route ===========
@app.route('/audioguides', methods=['GET', 'POST'])
def audio_guides():
    lines = read_lines('audioguides.txt')
    guides = []
    for line in lines:
        parts = line.split('|')
        if len(parts) < 8:
            continue
        try:
            guide = {
                'guide_id': int(parts[0]),
                'exhibit_number': int(parts[1]),
                'title': parts[2],
                'language': parts[3],
                'duration': int(parts[4]),
                'script': parts[5],
                'narrator': parts[6],
                'created_by': parts[7]
            }
            guides.append(guide)
        except Exception:
            continue

    filter_language = ''
    if request.method == 'POST':
        filter_language = request.form.get('filter-language', '')
        if filter_language:
            guides = [g for g in guides if g['language'] == filter_language]

    return render_template('audio_guides.html', audio_guides=guides, filter_language=filter_language)


if __name__ == '__main__':
    app.run(port=5000, debug=True)
