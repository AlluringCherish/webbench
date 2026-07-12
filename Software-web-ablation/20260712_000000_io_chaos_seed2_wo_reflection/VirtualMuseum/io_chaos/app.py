from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Helper functions to read and write data files

def read_users():
    users = []
    try:
        with open(os.path.join(DATA_DIR, 'users.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                username = line.strip()
                if username:
                    users.append(username)
    except FileNotFoundError:
        pass
    return users


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
                        'floor': parts[2],
                        'capacity': parts[3],
                        'theme': parts[4],
                        'status': parts[5]
                    }
    except FileNotFoundError:
        pass
    return galleries


def read_exhibitions():
    exhibitions = []
    try:
        with open(os.path.join(DATA_DIR, 'exhibitions.txt'), 'r', encoding='utf-8') as f:
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
                        'created_by': parts[8]
                    })
    except FileNotFoundError:
        pass
    return exhibitions


def read_artifacts():
    artifacts = []
    try:
        with open(os.path.join(DATA_DIR, 'artifacts.txt'), 'r', encoding='utf-8') as f:
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
    except FileNotFoundError:
        pass
    return artifacts


def read_audioguides():
    guides = []
    try:
        with open(os.path.join(DATA_DIR, 'audioguides.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 8:
                    guides.append({
                        'guide_id': int(parts[0]),
                        'exhibit_number': parts[1],
                        'title': parts[2],
                        'language': parts[3],
                        'duration': parts[4],
                        'script': parts[5],
                        'narrator': parts[6],
                        'created_by': parts[7]
                    })
    except FileNotFoundError:
        pass
    return guides


def read_tickets():
    tickets = []
    try:
        with open(os.path.join(DATA_DIR, 'tickets.txt'), 'r', encoding='utf-8') as f:
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
    except FileNotFoundError:
        pass
    return tickets


def read_events():
    events = []
    try:
        with open(os.path.join(DATA_DIR, 'events.txt'), 'r', encoding='utf-8') as f:
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
    except FileNotFoundError:
        pass
    return events


def read_event_registrations():
    regs = []
    try:
        with open(os.path.join(DATA_DIR, 'event_registrations.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 4:
                    regs.append({
                        'registration_id': int(parts[0]),
                        'event_id': int(parts[1]),
                        'username': parts[2],
                        'registration_date': parts[3]
                    })
    except FileNotFoundError:
        pass
    return regs


def write_tickets(tickets):
    try:
        with open(os.path.join(DATA_DIR, 'tickets.txt'), 'w', encoding='utf-8') as f:
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
                f.write(line + '\n')
    except Exception:
        pass


def write_event_registrations(registrations):
    try:
        with open(os.path.join(DATA_DIR, 'event_registrations.txt'), 'w', encoding='utf-8') as f:
            for r in registrations:
                line = '|'.join([
                    str(r['registration_id']),
                    str(r['event_id']),
                    r['username'],
                    r['registration_date']
                ])
                f.write(line + '\n')
    except Exception:
        pass


# Helper to resolve gallery name by id

def get_gallery_name(gallery_id, galleries=None):
    if galleries is None:
        galleries = read_galleries()
    gallery = galleries.get(gallery_id)
    return gallery['gallery_name'] if gallery else 'Unknown'

# Helper to derive status for exhibitions
from datetime import date

def derive_exhibition_status(exhibition, gallery_status):
    # If gallery status is Renovation, exhibition status is 'Closed'
    if gallery_status.lower() == 'renovation':
        return 'Closed'
    # Otherwise, check dates
    today = date.today()
    try:
        start = datetime.strptime(exhibition['start_date'], '%Y-%m-%d').date()
        end = datetime.strptime(exhibition['end_date'], '%Y-%m-%d').date()
    except Exception:
        return 'Unknown'

    if start <= today <= end:
        return 'Active'
    elif today < start:
        return 'Upcoming'
    else:
        return 'Ended'


# Dummy user session simulation (for demonstration purpose assume fixed user)
# In real app, would use Flask-Login or similar

CURRENT_USER = 'visitor_mary'


@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    exhibitions = read_exhibitions()
    # Summary counts: total and active
    galleries = read_galleries()
    total = len(exhibitions)
    active_count = 0

    for ex in exhibitions:
        gallery = galleries.get(ex['gallery_id'])
        gallery_status = gallery['status'] if gallery else ''
        status = derive_exhibition_status(ex, gallery_status)
        if status == 'Active':
            active_count += 1

    exhibitions_overview = {
        'total': total,
        'active': active_count
    }

    return render_template('dashboard.html', exhibitions_overview=exhibitions_overview)


@app.route('/artifacts', methods=['GET', 'POST'])
def artifact_catalog():
    artifacts = read_artifacts()
    exhibitions = read_exhibitions()
    exhibition_map = {ex['exhibition_id']: ex['title'] for ex in exhibitions}

    search_query = ''
    if request.method == 'POST':
        search_query = request.form.get('search_query', '').strip()
    
    filtered_artifacts = []
    if search_query:
        search_lower = search_query.lower()
        for art in artifacts:
            if (search_lower in art['artifact_name'].lower()) or (search_lower in str(art['artifact_id'])):
                filtered_artifacts.append(art)
    else:
        filtered_artifacts = artifacts

    # Prepare artifacts list with required fields and resolved exhibition_name
    artifacts_for_template = []
    for art in filtered_artifacts:
        artifacts_for_template.append({
            'artifact_id': art['artifact_id'],
            'artifact_name': art['artifact_name'],
            'period': art['period'],
            'origin': art['origin'],
            'exhibition_name': exhibition_map.get(art['exhibition_id'], 'Unknown')
        })

    return render_template('artifact_catalog.html', artifacts=artifacts_for_template, search_query=search_query)


@app.route('/exhibitions', methods=['GET', 'POST'])
def exhibitions():
    exhibitions_list = read_exhibitions()
    galleries = read_galleries()

    filter_type = ''
    if request.method == 'POST':
        filter_type = request.form.get('filter_type', '').strip()

    filtered_exhibitions = []

    for ex in exhibitions_list:
        if filter_type:
            if ex['exhibition_type'].lower() != filter_type.lower():
                continue
        gallery_name = get_gallery_name(ex['gallery_id'], galleries)
        gallery_status = galleries[ex['gallery_id']]['status'] if ex['gallery_id'] in galleries else 'Unknown'
        status = derive_exhibition_status(ex, gallery_status)

        filtered_exhibitions.append({
            'exhibition_id': ex['exhibition_id'],
            'title': ex['title'],
            'exhibition_type': ex['exhibition_type'],
            'start_date': ex['start_date'],
            'end_date': ex['end_date'],
            'gallery_name': gallery_name,
            'status': status
        })

    return render_template('exhibitions.html', exhibitions=filtered_exhibitions, filter_type=filter_type)


@app.route('/exhibition/<int:exhibition_id>')
def exhibition_details(exhibition_id):
    exhibitions_list = read_exhibitions()
    artifacts = read_artifacts()

    # Find exhibition
    exhibition = None
    for ex in exhibitions_list:
        if ex['exhibition_id'] == exhibition_id:
            exhibition = ex
            break

    if exhibition is None:
        return "Exhibition not found", 404

    # Filter artifacts by exhibition_id
    exhibition_artifacts = []
    for art in artifacts:
        if art['exhibition_id'] == exhibition_id:
            exhibition_artifacts.append(art)

    return render_template('exhibition_details.html', exhibition=exhibition, artifacts=exhibition_artifacts)


@app.route('/tickets', methods=['GET', 'POST'])
def visitor_tickets():
    tickets = read_tickets()
    user = CURRENT_USER
    purchase_status = ''

    # Filter tickets by current user
    user_tickets = [t for t in tickets if t['username'] == user]

    if request.method == 'POST':
        # Process ticket purchase
        ticket_type = request.form.get('ticket_type', '').strip()
        number_of_tickets = request.form.get('number_of_tickets', '').strip()
        visitor_name = request.form.get('visitor_name', '').strip() or user
        visitor_email = request.form.get('visitor_email', '').strip()
        visit_date = request.form.get('visit_date', '').strip()
        visit_time = request.form.get('visit_time', '').strip()

        if not (ticket_type and number_of_tickets.isdigit() and visitor_email and visit_date and visit_time):
            purchase_status = 'Invalid input. Please fill all required fields correctly.'
        else:
            number_of_tickets = int(number_of_tickets)
            # price calculation dummy (set fixed prices for each ticket type)
            price_map = {
                'Standard': 15.0,
                'Student': 10.0,
                'Senior': 12.0,
                'Family': 40.0,
                'VIP': 50.0
            }
            price = price_map.get(ticket_type, 0) * number_of_tickets

            # Generate new ticket_id
            max_id = max([t['ticket_id'] for t in tickets], default=0)
            new_id = max_id + 1

            purchase_date = datetime.now().strftime('%Y-%m-%d')

            new_ticket = {
                'ticket_id': new_id,
                'username': user,
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
            try:
                with open(os.path.join(DATA_DIR, 'tickets.txt'), 'w', encoding='utf-8') as f:
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
                        f.write(line + '\n')
                purchase_status = 'Purchase successful.'
                # Refresh user tickets with new ticket
                user_tickets = [t for t in tickets if t['username'] == user]
            except Exception:
                purchase_status = 'Failed to save ticket. Please try again.'

    return render_template('visitor_tickets.html', tickets=user_tickets, purchase_status=purchase_status, user=user)


@app.route('/events', methods=['GET', 'POST'])
def virtual_events():
    events = read_events()
    registrations = read_event_registrations()
    user = CURRENT_USER

    # Filter user's registrations
    user_registrations = [r for r in registrations if r['username'] == user]

    return render_template('virtual_events.html', events=events, registrations=user_registrations)


@app.route('/events/register/<int:event_id>', methods=['POST'])
def register_event(event_id):
    user = CURRENT_USER
    registrations = read_event_registrations()
    events = read_events()

    # Check if event exists
    event_exists = any(e['event_id'] == event_id for e in events)
    if not event_exists:
        return redirect(url_for('virtual_events'))

    # Check if user already registered for event
    for reg in registrations:
        if reg['event_id'] == event_id and reg['username'] == user:
            # Already registered
            return redirect(url_for('virtual_events'))

    # Add new registration
    max_reg_id = max([r['registration_id'] for r in registrations], default=0)
    new_reg_id = max_reg_id + 1
    reg_date = datetime.now().strftime('%Y-%m-%d')

    new_registration = {
        'registration_id': new_reg_id,
        'event_id': event_id,
        'username': user,
        'registration_date': reg_date
    }

    registrations.append(new_registration)

    try:
        with open(os.path.join(DATA_DIR, 'event_registrations.txt'), 'w', encoding='utf-8') as f:
            for r in registrations:
                line = '|'.join([
                    str(r['registration_id']),
                    str(r['event_id']),
                    r['username'],
                    r['registration_date']
                ])
                f.write(line + '\n')
    except Exception:
        pass

    return redirect(url_for('virtual_events'))


@app.route('/events/cancel/<int:registration_id>', methods=['POST'])
def cancel_registration(registration_id):
    user = CURRENT_USER
    registrations = read_event_registrations()

    # Remove registration for user and registration_id
    new_regs = [r for r in registrations if not (r['registration_id'] == registration_id and r['username'] == user)]

    try:
        with open(os.path.join(DATA_DIR, 'event_registrations.txt'), 'w', encoding='utf-8') as f:
            for r in new_regs:
                line = '|'.join([
                    str(r['registration_id']),
                    str(r['event_id']),
                    r['username'],
                    r['registration_date']
                ])
                f.write(line + '\n')
    except Exception:
        pass

    return redirect(url_for('virtual_events'))


@app.route('/audioguides', methods=['GET', 'POST'])
def audio_guides():
    guides = read_audioguides()

    filter_language = ''
    if request.method == 'POST':
        filter_language = request.form.get('filter_language', '').strip()

    if filter_language:
        filtered_guides = [g for g in guides if g['language'].lower() == filter_language.lower()]
    else:
        filtered_guides = guides

    return render_template('audio_guides.html', guides=filtered_guides, filter_language=filter_language)


if __name__ == '__main__':
    app.run(port=5000, debug=True)
