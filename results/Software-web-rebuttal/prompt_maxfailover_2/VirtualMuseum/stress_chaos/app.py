from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

data_dir = 'data'

# Utility functions for reading and writing data files

def read_galleries():
    path = os.path.join(data_dir, 'galleries.txt')
    galleries = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 6:
                    galleries.append({
                        'gallery_id': int(parts[0]),
                        'gallery_name': parts[1],
                        'floor': int(parts[2]),
                        'capacity': int(parts[3]),
                        'theme': parts[4],
                        'status': parts[5],
                    })
    except FileNotFoundError:
        pass
    return galleries


def read_exhibitions():
    path = os.path.join(data_dir, 'exhibitions.txt')
    exhibitions = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
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
                        'created_by': parts[8],
                    })
    except FileNotFoundError:
        pass
    return exhibitions


def write_exhibitions(exhibitions):
    path = os.path.join(data_dir, 'exhibitions.txt')
    try:
        with open(path, 'w', encoding='utf-8') as f:
            for e in exhibitions:
                line = '|'.join([
                    str(e['exhibition_id']),
                    e['title'],
                    e['description'],
                    str(e['gallery_id']),
                    e['exhibition_type'],
                    e['start_date'],
                    e['end_date'],
                    e['curator_name'],
                    e['created_by']
                ])
                f.write(line + '\n')
    except IOError:
        pass


def read_artifacts():
    path = os.path.join(data_dir, 'artifacts.txt')
    artifacts = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
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
                        'added_by': parts[8],
                    })
    except FileNotFoundError:
        pass
    return artifacts


def write_artifacts(artifacts):
    path = os.path.join(data_dir, 'artifacts.txt')
    try:
        with open(path, 'w', encoding='utf-8') as f:
            for a in artifacts:
                line = '|'.join([
                    str(a['artifact_id']),
                    a['artifact_name'],
                    a['period'],
                    a['origin'],
                    a['description'],
                    str(a['exhibition_id']),
                    a['storage_location'],
                    a['acquisition_date'],
                    a['added_by']
                ])
                f.write(line + '\n')
    except IOError:
        pass


def read_audioguides():
    path = os.path.join(data_dir, 'audioguides.txt')
    audio_guides = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 8:
                    try:
                        duration = int(parts[4])
                    except:
                        duration = 0
                    audio_guides.append({
                        'guide_id': int(parts[0]),
                        'exhibit_number': parts[1],
                        'title': parts[2],
                        'language': parts[3],
                        'duration': duration,
                        'script': parts[5],
                        'narrator': parts[6],
                        'created_by': parts[7],
                    })
    except FileNotFoundError:
        pass
    return audio_guides


def write_audioguides(audio_guides):
    path = os.path.join(data_dir, 'audioguides.txt')
    try:
        with open(path, 'w', encoding='utf-8') as f:
            for ag in audio_guides:
                line = '|'.join([
                    str(ag['guide_id']),
                    ag['exhibit_number'],
                    ag['title'],
                    ag['language'],
                    str(ag['duration']),
                    ag['script'],
                    ag['narrator'],
                    ag['created_by']
                ])
                f.write(line + '\n')
    except IOError:
        pass


def read_tickets():
    path = os.path.join(data_dir, 'tickets.txt')
    tickets = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 10:
                    try:
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
                            'purchase_date': parts[9],
                        })
                    except:
                        continue
    except FileNotFoundError:
        pass
    return tickets


def write_tickets(tickets):
    path = os.path.join(data_dir, 'tickets.txt')
    try:
        with open(path, 'w', encoding='utf-8') as f:
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
                f.write(line + '\n')
    except IOError:
        pass


def read_events():
    path = os.path.join(data_dir, 'events.txt')
    events = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 9:
                    try:
                        events.append({
                            'event_id': int(parts[0]),
                            'title': parts[1],
                            'date': parts[2],
                            'time': parts[3],
                            'event_type': parts[4],
                            'speaker': parts[5],
                            'capacity': int(parts[6]),
                            'description': parts[7],
                            'created_by': parts[8],
                        })
                    except:
                        continue
    except FileNotFoundError:
        pass
    return events


def write_events(events):
    path = os.path.join(data_dir, 'events.txt')
    try:
        with open(path, 'w', encoding='utf-8') as f:
            for e in events:
                line = '|'.join([
                    str(e['event_id']),
                    e['title'],
                    e['date'],
                    e['time'],
                    e['event_type'],
                    e['speaker'],
                    str(e['capacity']),
                    e['description'],
                    e['created_by']
                ])
                f.write(line + '\n')
    except IOError:
        pass


def read_event_registrations():
    path = os.path.join(data_dir, 'event_registrations.txt')
    regs = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 4:
                    try:
                        regs.append({
                            'registration_id': int(parts[0]),
                            'event_id': int(parts[1]),
                            'username': parts[2],
                            'registration_date': parts[3],
                        })
                    except:
                        continue
    except FileNotFoundError:
        pass
    return regs


def write_event_registrations(regs):
    path = os.path.join(data_dir, 'event_registrations.txt')
    try:
        with open(path, 'w', encoding='utf-8') as f:
            for r in regs:
                line = '|'.join([
                    str(r['registration_id']),
                    str(r['event_id']),
                    r['username'],
                    r['registration_date'],
                ])
                f.write(line + '\n')
    except IOError:
        pass


def read_users():
    path = os.path.join(data_dir, 'users.txt')
    users = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                username = line.strip()
                if username:
                    users.append(username)
    except FileNotFoundError:
        pass
    return users

# Route implementations

@app.route('/', methods=['GET'])
def root_redirect():
    return redirect(url_for('dashboard'))

@app.route('/dashboard', methods=['GET'])
def dashboard():
    exhibitions = read_exhibitions()
    total_exhibitions = len(exhibitions)
    # active exhibitions: current date between start_date and end_date inclusive
    active_exhibitions = 0
    today_str = datetime.today().strftime('%Y-%m-%d')
    for ex in exhibitions:
        if ex['start_date'] <= today_str <= ex['end_date']:
            active_exhibitions += 1
    exhibition_summary = {'total_exhibitions': total_exhibitions, 'active_exhibitions': active_exhibitions}
    return render_template('dashboard.html', exhibition_summary=exhibition_summary)

@app.route('/artifact_catalog', methods=['GET', 'POST'])
def artifact_catalog():
    artifacts = read_artifacts()
    search_query = ''
    filter_applied = False
    if request.method == 'POST':
        search_query = request.form.get('search-artifact', '').strip()
        if search_query:
            filter_applied = True
            lowered_query = search_query.lower()
            filtered_artifacts = []
            for art in artifacts:
                # Search in artifact_name, period, origin, exhibition
                # We must map exhibition_id to exhibition title for exhibition field
                exhibition_title = ''
                exhibitions = read_exhibitions()
                exhibition_dict = {e['exhibition_id']: e['title'] for e in exhibitions}
                exhibition_title = exhibition_dict.get(art['exhibition_id'], '')
                if (lowered_query in art['artifact_name'].lower() or
                    lowered_query in art['period'].lower() or
                    lowered_query in art['origin'].lower() or
                    lowered_query in exhibition_title.lower()):
                    filtered_artifacts.append({
                        'artifact_id': art['artifact_id'],
                        'artifact_name': art['artifact_name'],
                        'period': art['period'],
                        'origin': art['origin'],
                        'exhibition': exhibition_title
                    })
            return render_template('artifact_catalog.html', artifacts=filtered_artifacts, search_query=search_query, filter_applied=filter_applied)

    # For GET and if no filtering, show all artifacts with exhibition title
    exhibitions = read_exhibitions()
    exhibition_dict = {e['exhibition_id']: e['title'] for e in exhibitions}
    artifact_list = []
    for art in artifacts:
        ex_title = exhibition_dict.get(art['exhibition_id'], '')
        artifact_list.append({
            'artifact_id': art['artifact_id'],
            'artifact_name': art['artifact_name'],
            'period': art['period'],
            'origin': art['origin'],
            'exhibition': ex_title
        })
    return render_template('artifact_catalog.html', artifacts=artifact_list, search_query='', filter_applied=False)

@app.route('/exhibitions', methods=['GET', 'POST'])
def exhibitions():
    exhibitions_all = read_exhibitions()
    exhibition_types = ['Permanent', 'Temporary', 'Virtual']
    selected_type = None
    filtered_exhibitions = exhibitions_all

    if request.method == 'POST':
        selected_type = request.form.get('filter-exhibition-type', '').strip()
        if selected_type and selected_type in exhibition_types:
            filtered_exhibitions = [ex for ex in exhibitions_all if ex['exhibition_type'] == selected_type]

    return render_template('exhibitions.html', exhibitions=filtered_exhibitions, exhibition_types=exhibition_types, selected_type=selected_type)

@app.route('/exhibition/<int:exhibition_id>', methods=['GET'])
def exhibition_details(exhibition_id):
    exhibitions = read_exhibitions()
    exhibition = None
    for ex in exhibitions:
        if ex['exhibition_id'] == exhibition_id:
            exhibition = ex
            break
    if exhibition is None:
        # Exhibition not found, could return 404 or a render with no data
        exhibition = {
            'exhibition_id': exhibition_id,
            'title': 'Unknown Exhibition',
            'description': '',
            'start_date': '',
            'end_date': ''
        }

    artifacts = read_artifacts()
    # Filter artifacts belonging to exhibition
    filtered_artifacts = []
    for art in artifacts:
        if art['exhibition_id'] == exhibition_id:
            filtered_artifacts.append({
                'artifact_id': art['artifact_id'],
                'artifact_name': art['artifact_name'],
                'period': art['period'],
                'origin': art['origin'],
                'description': art['description']
            })

    return render_template('exhibition_details.html', exhibition=exhibition, artifacts=filtered_artifacts)

@app.route('/visitor_tickets', methods=['GET', 'POST'])
def visitor_tickets():
    ticket_types = ['Standard', 'Student', 'Senior', 'Family', 'VIP']
    tickets = read_tickets()
    # We do not have user login, so show all tickets for now
    purchased_tickets = tickets

    if request.method == 'POST':
        # Form fields expected:
        # ticket-type, number-of-tickets, visit-date, visit-time, visitor-name, visitor-email
        form = request.form
        ticket_type = form.get('ticket-type', '').strip()
        number_of_tickets_str = form.get('number-of-tickets', '').strip()
        visit_date = form.get('visit-date', '').strip() if 'visit-date' in form else ''
        visit_time = form.get('visit-time', '').strip() if 'visit-time' in form else ''
        visitor_name = form.get('visitor-name', '').strip() if 'visitor-name' in form else ''
        visitor_email = form.get('visitor-email', '').strip() if 'visitor-email' in form else ''

        # Validate ticket_type
        if ticket_type not in ticket_types:
            return redirect(url_for('visitor_tickets'))

        # Validate number_of_tickets
        try:
            number_of_tickets = int(number_of_tickets_str)
            if number_of_tickets < 1:
                return redirect(url_for('visitor_tickets'))
        except ValueError:
            return redirect(url_for('visitor_tickets'))

        # Validate visit_date format
        try:
            datetime.strptime(visit_date, '%Y-%m-%d')
        except Exception:
            return redirect(url_for('visitor_tickets'))

        # Validate other fields presence
        if not visit_time or not visitor_name or not visitor_email:
            return redirect(url_for('visitor_tickets'))

        # Calculate price based on ticket_type and number_of_tickets
        # Pricing assumptions (not given specifically, so we assume): Standard=15, Student=10, Senior=12, Family=40, VIP=50
        price_map = {'Standard':15, 'Student':10, 'Senior':12, 'Family':40, 'VIP':50}
        price = price_map.get(ticket_type, 15) * number_of_tickets

        # Determine purchase_date as today
        purchase_date = datetime.today().strftime('%Y-%m-%d')

        # Determine new ticket_id (max existing + 1)
        new_ticket_id = 1
        if tickets:
            new_ticket_id = max(t['ticket_id'] for t in tickets) + 1

        # Username is not specified in form; as we do not have user auth, store visitor_name as username
        username = visitor_name

        new_ticket = {
            'ticket_id': new_ticket_id,
            'username': username,
            'ticket_type': ticket_type,
            'visit_date': visit_date,
            'visit_time': visit_time,
            'number_of_tickets': number_of_tickets,
            'price': float(price),
            'visitor_name': visitor_name,
            'visitor_email': visitor_email,
            'purchase_date': purchase_date
        }

        tickets.append(new_ticket)
        write_tickets(tickets)
        purchased_tickets = tickets

    return render_template('visitor_tickets.html', ticket_types=ticket_types, purchased_tickets=purchased_tickets)

@app.route('/virtual_events', methods=['GET', 'POST'])
def virtual_events():
    # To simulate a logged-in user for this route, hardcode username
    user_name = 'visitor_mary'

    events = read_events()
    registrations = read_event_registrations()
    user_registrations = [reg for reg in registrations if reg['username'] == user_name]

    if request.method == 'POST':
        form = request.form
        # Determine if a register or cancel action occurs
        # Register form field: 'register-event-id'
        # Cancel form field: 'cancel-registration-id'

        register_event_id_str = form.get('register-event-id')
        cancel_registration_id_str = form.get('cancel-registration-id')

        if register_event_id_str:
            try:
                event_id = int(register_event_id_str)
            except:
                event_id = None

            # Check if user already registered for event
            if event_id is not None:
                already_registered = any((r for r in registrations if r['event_id'] == event_id and r['username'] == user_name))
                if not already_registered:
                    # Create new registration id
                    new_registration_id = 1
                    if registrations:
                        new_registration_id = max(r['registration_id'] for r in registrations) + 1
                    new_reg = {
                        'registration_id': new_registration_id,
                        'event_id': event_id,
                        'username': user_name,
                        'registration_date': datetime.today().strftime('%Y-%m-%d')
                    }
                    registrations.append(new_reg)
                    write_event_registrations(registrations)

        elif cancel_registration_id_str:
            try:
                reg_id = int(cancel_registration_id_str)
            except:
                reg_id = None
            if reg_id is not None:
                registrations = [r for r in registrations if r['registration_id'] != reg_id or r['username'] != user_name]
                write_event_registrations(registrations)

        return redirect(url_for('virtual_events'))

    return render_template('virtual_events.html', events=events, registrations=registrations, user_registrations=user_registrations, user_name=user_name)

@app.route('/audio_guides', methods=['GET', 'POST'])
def audio_guides():
    languages = ['English', 'Spanish', 'French']
    audio_guides_all = read_audioguides()
    selected_language = None

    if request.method == 'POST':
        selected_language = request.form.get('filter-language', '').strip()
        if selected_language and selected_language in languages:
            filtered_guides = [ag for ag in audio_guides_all if ag['language'] == selected_language]
            return render_template('audio_guides.html', audio_guides=filtered_guides, languages=languages, selected_language=selected_language)

    # GET or no filter
    return render_template('audio_guides.html', audio_guides=audio_guides_all, languages=languages, selected_language=None)


if __name__ == "__main__":
    app.run(port=5000, debug=True)
