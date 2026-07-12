from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Helper functions to read data files

def read_galleries():
    galleries = {}
    try:
        with open(os.path.join(DATA_DIR, 'galleries.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 6:
                    gallery_id = int(parts[0])
                    galleries[gallery_id] = {
                        'gallery_id': gallery_id,
                        'gallery_name': parts[1],
                        'floor': int(parts[2]),
                        'capacity': int(parts[3]),
                        'theme': parts[4],
                        'status': parts[5]
                    }
    except Exception:
        pass
    return galleries


def read_exhibitions():
    exhibitions = []
    try:
        with open(os.path.join(DATA_DIR, 'exhibitions.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 9:
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
        pass
    return exhibitions


def read_artifacts():
    artifacts = []
    try:
        with open(os.path.join(DATA_DIR, 'artifacts.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 9:
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
        pass
    return artifacts


def read_users():
    users = []
    try:
        with open(os.path.join(DATA_DIR, 'users.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                username = line.strip()
                if username:
                    users.append(username)
    except Exception:
        pass
    return users


def read_audioguides():
    audioguides = []
    try:
        with open(os.path.join(DATA_DIR, 'audioguides.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 8:
                    try:
                        exhibit_number = int(parts[1])
                    except ValueError:
                        exhibit_number = parts[1]
                    guide = {
                        'guide_id': int(parts[0]),
                        'exhibit_number': exhibit_number,
                        'title': parts[2],
                        'language': parts[3],
                        'duration': int(parts[4]),
                        'script': parts[5],
                        'narrator': parts[6],
                        'created_by': parts[7]
                    }
                    audioguides.append(guide)
    except Exception:
        pass
    return audioguides


def read_tickets():
    tickets = []
    try:
        with open(os.path.join(DATA_DIR, 'tickets.txt'),'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 10:
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
        pass
    return tickets


def read_events():
    events = []
    try:
        with open(os.path.join(DATA_DIR, 'events.txt'),'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 9:
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
        pass
    return events


def read_event_registrations():
    registrations = []
    try:
        with open(os.path.join(DATA_DIR, 'event_registrations.txt'),'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 4:
                    registration = {
                        'registration_id': int(parts[0]),
                        'event_id': int(parts[1]),
                        'username': parts[2],
                        'registration_date': parts[3]
                    }
                    registrations.append(registration)
    except Exception:
        pass
    return registrations

# Helpers to write tickets and event registrations
from functions import write_text_file

def write_tickets(tickets):
    lines = []
    for t in tickets:
        line = '|'.join([
            str(t['ticket_id']),
            t['username'],
            t['ticket_type'],
            t['visit_date'],
            t['visit_time'],
            str(t['number_of_tickets']),
            f'{t["price"]:.2f}',
            t['visitor_name'],
            t['visitor_email'],
            t['purchase_date']
        ])
        lines.append(line)
    content = '\n'.join(lines)
    write_text_file(filename=os.path.join(DATA_DIR, 'tickets.txt'), content=content)


def write_event_registrations(registrations):
    lines = []
    for r in registrations:
        line = '|'.join([
            str(r['registration_id']),
            str(r['event_id']),
            r['username'],
            r['registration_date']
        ])
        lines.append(line)
    content = '\n'.join(lines)
    write_text_file(filename=os.path.join(DATA_DIR, 'event_registrations.txt'), content=content)


@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard_page'))


@app.route('/dashboard')
def dashboard_page():
    exhibitions = read_exhibitions()
    # Calculate summary: total exhibitions and active exhibitions
    total_exhibitions = len(exhibitions)
    today = datetime.now().date()
    active_count = 0
    for ex in exhibitions:
        try:
            start = datetime.strptime(ex['start_date'], '%Y-%m-%d').date()
            end = datetime.strptime(ex['end_date'], '%Y-%m-%d').date()
            if start <= today <= end:
                active_count += 1
        except Exception:
            pass
    exhibitions_summary = {
        'total_exhibitions': total_exhibitions,
        'active_exhibitions': active_count
    }
    
    return render_template('dashboard.html', exhibitions_summary=exhibitions_summary)


@app.route('/artifacts', methods=['GET', 'POST'])
def artifact_catalog_page():
    artifacts = read_artifacts()
    exhibitions = read_exhibitions()
    exhibition_map = {ex['exhibition_id']: ex['title'] for ex in exhibitions}
    
    search_query = ''
    # For POST, filter by search query
    if request.method == 'POST':
        search_query = request.form.get('search-artifact', '').strip()
        if search_query:
            filtered = []
            sq_lower = search_query.lower()
            for a in artifacts:
                if (sq_lower in a['artifact_name'].lower()) or (sq_lower in a['period'].lower()) or (sq_lower in a['origin'].lower()):
                    filtered.append(a)
            artifacts = filtered

    # Prepare artifacts list with exhibition_title or None
    artifacts_display = []
    for a in artifacts:
        exhibition_title = exhibition_map.get(a['exhibition_id'])
        artifacts_display.append({
            'artifact_id': a['artifact_id'],
            'artifact_name': a['artifact_name'],
            'period': a['period'],
            'origin': a['origin'],
            'exhibition_title': exhibition_title
        })

    return render_template('artifact_catalog.html', artifacts=artifacts_display, search_query=search_query)


@app.route('/exhibitions')
def exhibitions_page():
    exhibitions = read_exhibitions()
    galleries = read_galleries()

    selected_filter = request.args.get('filter')
    filtered_list = []
    if selected_filter in ['Permanent', 'Temporary', 'Virtual']:
        for ex in exhibitions:
            if ex['exhibition_type'] == selected_filter:
                filtered_list.append(ex)
    else:
        filtered_list = exhibitions

    # Prepare context exhibitions data with gallery_name and status
    exhibitions_display = []
    for ex in filtered_list:
        gallery_name = galleries.get(ex['gallery_id'], {}).get('gallery_name', 'Unknown')
        # Determine status: we can use end_date to set status
        status = ''
        try:
            today = datetime.now().date()
            start = datetime.strptime(ex['start_date'], '%Y-%m-%d').date()
            end = datetime.strptime(ex['end_date'], '%Y-%m-%d').date()
            if today < start:
                status = 'Upcoming'
            elif start <= today <= end:
                status = 'Ongoing'
            else:
                status = 'Ended'
        except Exception:
            status = 'Unknown'

        exhibitions_display.append({
            'exhibition_id': ex['exhibition_id'],
            'title': ex['title'],
            'exhibition_type': ex['exhibition_type'],
            'start_date': ex['start_date'],
            'end_date': ex['end_date'],
            'gallery_name': gallery_name,
            'status': status
        })

    return render_template('exhibitions.html', exhibitions=exhibitions_display, selected_filter=selected_filter)


@app.route('/exhibition/<int:exhibition_id>')
def exhibition_details_page(exhibition_id):
    exhibitions = read_exhibitions()
    exhibition = None
    for ex in exhibitions:
        if ex['exhibition_id'] == exhibition_id:
            exhibition = ex
            break
    if exhibition is None:
        # Exhibition not found, return 404 or redirect
        return redirect(url_for('exhibitions_page'))

    artifacts = read_artifacts()
    artifacts_display = []
    for a in artifacts:
        if a['exhibition_id'] == exhibition_id:
            artifacts_display.append({
                'artifact_id': a['artifact_id'],
                'artifact_name': a['artifact_name'],
                'period': a['period'],
                'origin': a['origin']
            })

    # Prepare exhibition dict per context
    exhibition_context = {
        'exhibition_id': exhibition['exhibition_id'],
        'title': exhibition['title'],
        'description': exhibition['description'],
        'start_date': exhibition['start_date'],
        'end_date': exhibition['end_date']
    }

    return render_template('exhibition_details.html', exhibition=exhibition_context, artifacts=artifacts_display)


@app.route('/visitor_tickets', methods=['GET', 'POST'])
def visitor_tickets_page():
    tickets = read_tickets()
    purchase_success = None

    if request.method == 'POST':
        ticket_type = request.form.get('ticket-type')
        visit_date = request.form.get('visit-date')
        visit_time = request.form.get('visit-time')
        number_of_tickets_str = request.form.get('number-of-tickets')
        visitor_name = request.form.get('visitor-name')
        visitor_email = request.form.get('visitor-email')
        username = request.form.get('username')  # assuming username might be submitted or use visitor_name lower

        # Basic validations
        error = False
        try:
            number_of_tickets = int(number_of_tickets_str)
            if number_of_tickets <= 0:
                error = True
        except Exception:
            error = True

        if not ticket_type or not visit_date or not visit_time or not visitor_name or not visitor_email:
            error = True

        # For pricing, let's define prices per type
        price_map = {
            'Standard': 15.0,
            'Student': 10.0,
            'Senior': 12.0,
            'Family': 40.0,
            'VIP': 50.0
        }

        price_per_ticket = price_map.get(ticket_type, None)
        if price_per_ticket is None:
            error = True

        if not error:
            # Compute price
            total_price = price_per_ticket * number_of_tickets

            # Generate new ticket_id
            new_ticket_id = 1
            if tickets:
                new_ticket_id = max(t['ticket_id'] for t in tickets) + 1

            # Use visitor_name lowercase as username if no username given
            if not username:
                username = visitor_name.lower().replace(' ', '_')

            purchase_date = datetime.now().strftime('%Y-%m-%d')

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
            write_tickets(tickets)

            purchase_success = True

    # Prepare tickets list for context excluding username, visitor_email, purchase_date (not required in context)
    tickets_display = []
    for t in tickets:
        tickets_display.append({
            'ticket_id': t['ticket_id'],
            'ticket_type': t['ticket_type'],
            'visit_date': t['visit_date'],
            'visit_time': t['visit_time'],
            'number_of_tickets': t['number_of_tickets'],
            'price': t['price'],
            'visitor_name': t['visitor_name']
        })

    return render_template('visitor_tickets.html', tickets=tickets_display, purchase_success=purchase_success)


@app.route('/virtual_events')
def virtual_events_page():
    events = read_events()
    registrations = read_event_registrations()
    # For demonstration, assume username is hardcoded visitor_mary
    current_user = 'visitor_mary'

    # Determine registration_status for each event
    for event in events:
        reg = None
        for r in registrations:
            if r['event_id'] == event['event_id'] and r['username'] == current_user:
                reg = r
                break
        event['registration_status'] = {
            'registered': reg is not None,
            'registration_id': reg['registration_id'] if reg else None
        }

    return render_template('virtual_events.html', events=events)


@app.route('/register_event/<int:event_id>', methods=['POST'])
def register_event(event_id):
    registrations = read_event_registrations()
    events = read_events()
    current_user = 'visitor_mary'  # Hardcoded user

    # Check if event exists
    event_exists = any(e['event_id'] == event_id for e in events)
    if not event_exists:
        return redirect(url_for('virtual_events_page'))

    # Check if already registered
    for r in registrations:
        if r['event_id'] == event_id and r['username'] == current_user:
            return redirect(url_for('virtual_events_page'))

    # Generate new registration_id
    new_reg_id = 1
    if registrations:
        new_reg_id = max(r['registration_id'] for r in registrations) + 1

    registration_date = datetime.now().strftime('%Y-%m-%d')
    new_registration = {
        'registration_id': new_reg_id,
        'event_id': event_id,
        'username': current_user,
        'registration_date': registration_date
    }
    registrations.append(new_registration)
    write_event_registrations(registrations)

    return redirect(url_for('virtual_events_page'))


@app.route('/cancel_registration/<int:registration_id>', methods=['POST'])
def cancel_registration(registration_id):
    registrations = read_event_registrations()
    current_user = 'visitor_mary'  # Hardcoded user

    # Filter out registration to remove if it belongs to current_user
    registrations = [r for r in registrations if not (r['registration_id'] == registration_id and r['username'] == current_user)]

    write_event_registrations(registrations)

    return redirect(url_for('virtual_events_page'))


@app.route('/audio_guides', methods=['GET'])
def audio_guides_page():
    audioguides = read_audioguides()

    selected_language = request.args.get('filter-language')
    if selected_language in ['English', 'Spanish', 'French']:
        audioguides = [ag for ag in audioguides if ag['language'] == selected_language]
    else:
        selected_language = None

    # Prepare audioguides display dict with specified keys
    audioguides_display = []
    for ag in audioguides:
        audioguides_display.append({
            'guide_id': ag['guide_id'],
            'exhibit_number': ag['exhibit_number'],
            'title': ag['title'],
            'language': ag['language'],
            'duration': ag['duration'],
            'narrator': ag['narrator']
        })

    return render_template('audio_guides.html', audioguides=audioguides_display, selected_language=selected_language)


if __name__ == "__main__":
    app.run(port=5000, debug=True)
