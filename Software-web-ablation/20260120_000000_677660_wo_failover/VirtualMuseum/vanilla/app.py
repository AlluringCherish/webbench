from flask import Flask, render_template, request, redirect, url_for
from datetime import date
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

data_dir = 'data'

# Helper functions to read and write data files

def read_exhibitions():
    exhibitions = []
    try:
        with open(os.path.join(data_dir, 'exhibitions.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 9:
                    exhibition_id = int(parts[0])
                    title = parts[1]
                    description = parts[2]
                    gallery_id = int(parts[3])
                    exhibition_type = parts[4]
                    start_date = parts[5]
                    end_date = parts[6]
                    curator_name = parts[7]
                    created_by = parts[8]
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
    except IOError:
        pass
    return exhibitions


def write_exhibitions(exhibitions):
    lines = []
    for ex in exhibitions:
        line = '|'.join([
            str(ex['exhibition_id']),
            ex['title'],
            ex['description'],
            str(ex['gallery_id']),
            ex['exhibition_type'],
            ex['start_date'],
            ex['end_date'],
            ex['curator_name'],
            ex['created_by']
        ])
        lines.append(line)
    try:
        with open(os.path.join(data_dir, 'exhibitions.txt'), 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines) + '\n' if lines else '')
    except IOError:
        pass


def read_artifacts():
    artifacts = []
    try:
        with open(os.path.join(data_dir, 'artifacts.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
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
    except IOError:
        pass
    return artifacts


def read_galleries():
    galleries = []
    try:
        with open(os.path.join(data_dir, 'galleries.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 6:
                    galleries.append({
                        'gallery_id': int(parts[0]),
                        'gallery_name': parts[1],
                        'floor': int(parts[2]),
                        'capacity': int(parts[3]),
                        'theme': parts[4],
                        'status': parts[5]
                    })
    except IOError:
        pass
    return galleries


def read_tickets():
    tickets = []
    try:
        with open(os.path.join(data_dir, 'tickets.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 10:
                    tickets.append({
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
                    })
    except IOError:
        pass
    return tickets


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
            f"{t['price']:.2f}",
            t['visitor_name'],
            t['visitor_email'],
            t['purchase_date']
        ])
        lines.append(line)
    try:
        with open(os.path.join(data_dir, 'tickets.txt'), 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines) + '\n' if lines else '')
    except IOError:
        pass


def read_events():
    events = []
    try:
        with open(os.path.join(data_dir, 'events.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 9:
                    events.append({
                        'event_id': int(parts[0]),
                        'title': parts[1],
                        'date': parts[2],
                        'time': parts[3],
                        'event_type': parts[4],
                        'speaker': parts[5],
                        'capacity': int(parts[6]),
                        'description': parts[7],
                        'created_by': parts[8]
                    })
    except IOError:
        pass
    return events


def read_event_registrations():
    regs = []
    try:
        with open(os.path.join(data_dir, 'event_registrations.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 4:
                    regs.append({
                        'registration_id': int(parts[0]),
                        'event_id': int(parts[1]),
                        'username': parts[2],
                        'registration_date': parts[3]
                    })
    except IOError:
        pass
    return regs


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
    try:
        with open(os.path.join(data_dir, 'event_registrations.txt'), 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines) + '\n' if lines else '')
    except IOError:
        pass


def read_audio_guides():
    guides = []
    try:
        with open(os.path.join(data_dir, 'audioguides.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 8:
                    guides.append({
                        'guide_id': int(parts[0]),
                        'exhibit_number': parts[1],
                        'title': parts[2],
                        'language': parts[3],
                        'duration': int(parts[4]),
                        'script': parts[5],
                        'narrator': parts[6],
                        'created_by': parts[7]
                    })
    except IOError:
        pass
    return guides

# Helper to read users

def read_users():
    users = []
    try:
        with open(os.path.join(data_dir, 'users.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                username = line.strip()
                if username:
                    users.append(username)
    except IOError:
        pass
    return users


@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    exhibitions = read_exhibitions()
    total_exhibitions = len(exhibitions)
    active_exhibitions = 0
    today_str = date.today().isoformat()
    for ex in exhibitions:
        if ex['start_date'] <= today_str <= ex['end_date']:
            active_exhibitions += 1
    exhibitions_summary = {
        'total_exhibitions': total_exhibitions,
        'active_exhibitions': active_exhibitions
    }
    # user string optional, no authentication specified, so None
    user = None
    return render_template('dashboard.html', exhibitions_summary=exhibitions_summary, user=user)


@app.route('/artifact_catalog', methods=['GET', 'POST'])
def artifact_catalog():
    artifacts = read_artifacts()
    exhibitions = {ex['exhibition_id']: ex['title'] for ex in read_exhibitions()}
    search_query = ''
    filters_applied = False

    if request.method == 'POST':
        search_query = request.form.get('search_query', '').strip()
        if search_query:
            filters_applied = True
            filtered = []
            for a in artifacts:
                if search_query.isdigit():
                    if str(a['artifact_id']) == search_query:
                        filtered.append(a)
                if search_query.lower() in a['artifact_name'].lower():
                    if a not in filtered:
                        filtered.append(a)
            artifacts = filtered

    # Prepare artifacts context list of dicts with exhibition_title
    context_artifacts = []
    for a in artifacts:
        context_artifacts.append({
            'artifact_id': a['artifact_id'],
            'artifact_name': a['artifact_name'],
            'period': a['period'],
            'origin': a['origin'],
            'exhibition_title': exhibitions.get(a['exhibition_id'], '')
        })

    return render_template('artifact_catalog.html', artifacts=context_artifacts, search_query=search_query, filters_applied=filters_applied)


@app.route('/exhibitions', methods=['GET', 'POST'])
def exhibitions():
    exhibitions = read_exhibitions()
    filter_type = None
    filters_applied = False

    if request.method == 'POST':
        filter_type = request.form.get('filter_type', '')
        if filter_type in ('Permanent', 'Temporary', 'Virtual'):
            filters_applied = True
            exhibitions = [ex for ex in exhibitions if ex['exhibition_type'] == filter_type]
        else:
            filter_type = None

    # Prepare the context list with correct keys for template (including status from gallery status)
    galleries = {g['gallery_id']: g for g in read_galleries()}
    context_exhibitions = []
    for ex in exhibitions:
        gallery = galleries.get(ex['gallery_id'], {})
        status = gallery.get('status', '')
        context_exhibitions.append({
            'exhibition_id': ex['exhibition_id'],
            'title': ex['title'],
            'exhibition_type': ex['exhibition_type'],
            'start_date': ex['start_date'],
            'end_date': ex['end_date'],
            'gallery_name': gallery.get('gallery_name', ''),
            'status': status
        })

    return render_template('exhibitions.html', exhibitions=context_exhibitions, filter_type=filter_type, filters_applied=filters_applied)


@app.route('/exhibition/<int:exhibition_id>')
def exhibition_details(exhibition_id):
    exhibitions = read_exhibitions()
    artifacts = read_artifacts()

    exhibition = None
    for ex in exhibitions:
        if ex['exhibition_id'] == exhibition_id:
            exhibition = {
                'exhibition_id': ex['exhibition_id'],
                'title': ex['title'],
                'description': ex['description'],
                'start_date': ex['start_date'],
                'end_date': ex['end_date']
            }
            break

    if exhibition is None:
        # Show a simple 404 by aborting
        from flask import abort
        abort(404)

    filtered_artifacts = []
    for a in artifacts:
        if a['exhibition_id'] == exhibition_id:
            filtered_artifacts.append({
                'artifact_id': a['artifact_id'],
                'artifact_name': a['artifact_name'],
                'period': a['period'],
                'origin': a['origin']
            })

    return render_template('exhibition_details.html', exhibition=exhibition, artifacts=filtered_artifacts)


@app.route('/visitor_tickets', methods=['GET', 'POST'])
def visitor_tickets():
    tickets = read_tickets()
    purchase_success = False
    purchase_errors = []

    if request.method == 'POST':
        ticket_type = request.form.get('ticket_type', '').strip()
        visit_date = request.form.get('visit_date', '').strip()
        visit_time = request.form.get('visit_time', '').strip()
        number_of_tickets_str = request.form.get('number_of_tickets', '').strip()
        visitor_name = request.form.get('visitor_name', '').strip()
        visitor_email = request.form.get('visitor_email', '').strip()

        # Validate
        valid_ticket_types = ['Standard', 'Student', 'Senior', 'Family', 'VIP']
        if ticket_type not in valid_ticket_types:
            purchase_errors.append('Invalid ticket type.')

        # Validate date format YYYY-MM-DD
        try:
            year, month, day = map(int, visit_date.split('-'))
        except Exception:
            purchase_errors.append('Invalid visit date format.')

        # Validate number_of_tickets
        try:
            number_of_tickets = int(number_of_tickets_str)
            if number_of_tickets <= 0:
                raise ValueError()
        except Exception:
            purchase_errors.append('Number of tickets must be a positive integer.')

        if not visitor_name:
            purchase_errors.append('Visitor name is required.')

        if not visitor_email or '@' not in visitor_email:
            purchase_errors.append('Valid visitor email is required.')

        if not purchase_errors:
            # Determine price per ticket (example logic: Standard=15, Student=10, Senior=12, Family=40, VIP=50)
            price_map = {
                'Standard': 15.0,
                'Student': 10.0,
                'Senior': 12.0,
                'Family': 40.0,
                'VIP': 50.0
            }
            price = price_map.get(ticket_type, 0.0) * number_of_tickets

            # Assign ticket_id (max existing + 1)
            max_id = max([t['ticket_id'] for t in tickets], default=0)
            new_ticket_id = max_id + 1
            username = None  # No auth context specified

            purchase_date = date.today().isoformat()

            new_ticket = {
                'ticket_id': new_ticket_id,
                'username': username or '',
                'ticket_type': ticket_type,
                'visit_date': visit_date,
                'visit_time': visit_time,
                'number_of_tickets': number_of_tickets,
                'price': price,
                'visitor_name': visitor_name,
                'visitor_email': visitor_email,
                'purchase_date': purchase_date
            }

            tickets.append(new_ticket)
            write_tickets(tickets)
            purchase_success = True

    # Prepare tickets context for template
    context_tickets = []
    for t in tickets:
        context_tickets.append({
            'ticket_id': t['ticket_id'],
            'ticket_type': t['ticket_type'],
            'visit_date': t['visit_date'],
            'number_of_tickets': t['number_of_tickets'],
            'price': t['price']
        })

    return render_template('visitor_tickets.html', tickets=context_tickets, purchase_success=purchase_success, purchase_errors=purchase_errors)


@app.route('/virtual_events', methods=['GET', 'POST'])
def virtual_events():
    events = read_events()
    registrations = read_event_registrations()

    registration_success = False
    cancellation_success = False

    # Here we assume a default username visitor_mary (no auth implemented)
    current_username = 'visitor_mary'

    if request.method == 'POST':
        # Possible form params are event_id to register or registration_id to cancel
        event_id = request.form.get('event_id')
        registration_id = request.form.get('registration_id')

        if event_id:
            try:
                event_id = int(event_id)
                # Check if already registered
                already_registered = any(r['event_id'] == event_id and r['username'] == current_username for r in registrations)
                if not already_registered:
                    new_id = max([r['registration_id'] for r in registrations], default=0) + 1
                    today_str = date.today().isoformat()
                    registrations.append({
                        'registration_id': new_id,
                        'event_id': event_id,
                        'username': current_username,
                        'registration_date': today_str
                    })
                    write_event_registrations(registrations)
                    registration_success = True
            except ValueError:
                pass

        elif registration_id:
            try:
                registration_id = int(registration_id)
                reg_index = next((i for i, r in enumerate(registrations) if r['registration_id'] == registration_id and r['username'] == current_username), None)
                if reg_index is not None:
                    del registrations[reg_index]
                    write_event_registrations(registrations)
                    cancellation_success = True
            except ValueError:
                pass

    # Build events with is_registered flag for current user
    events_with_reg = []
    registered_event_ids = {r['event_id'] for r in registrations if r['username'] == current_username}
    for ev in events:
        events_with_reg.append({
            'event_id': ev['event_id'],
            'title': ev['title'],
            'date': ev['date'],
            'time': ev['time'],
            'event_type': ev['event_type'],
            'is_registered': ev['event_id'] in registered_event_ids
        })

    return render_template('virtual_events.html',
                           events=events_with_reg,
                           registrations=registrations,
                           registration_success=registration_success if registration_success else None,
                           cancellation_success=cancellation_success if cancellation_success else None)


@app.route('/audio_guides', methods=['GET', 'POST'])
def audio_guides():
    audio_guides = read_audio_guides()
    filter_language = None

    if request.method == 'POST':
        filter_language = request.form.get('filter_language', '').strip()
        if filter_language not in ('English', 'Spanish', 'French'):
            filter_language = None

    if filter_language:
        filtered_guides = [g for g in audio_guides if g['language'] == filter_language]
    else:
        filtered_guides = audio_guides

    # Prepare context list
    context_guides = []
    for g in filtered_guides:
        context_guides.append({
            'guide_id': g['guide_id'],
            'exhibit_number': g['exhibit_number'],
            'title': g['title'],
            'language': g['language'],
            'duration': g['duration']
        })

    return render_template('audio_guides.html', audio_guides=context_guides, filter_language=filter_language)


if __name__ == "__main__":
    app.run(port=5000, debug=True)
