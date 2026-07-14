from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)

data_dir = 'data'

# Helper functions to load and save pipe-delimited data files

def load_users():
    path = os.path.join(data_dir, 'users.txt')
    if not os.path.exists(path):
        return []
    with open(path, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]

def load_galleries():
    path = os.path.join(data_dir, 'galleries.txt')
    galleries = []
    if not os.path.exists(path):
        return galleries
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) == 6:
                galleries.append({
                    'gallery_id': int(parts[0]),
                    'gallery_name': parts[1],
                    'floor': parts[2],
                    'capacity': parts[3],
                    'theme': parts[4],
                    'status': parts[5],
                })
    return galleries

def load_exhibitions():
    path = os.path.join(data_dir, 'exhibitions.txt')
    exhibitions = []
    if not os.path.exists(path):
        return exhibitions
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
    return exhibitions

def load_artifacts():
    path = os.path.join(data_dir, 'artifacts.txt')
    artifacts = []
    if not os.path.exists(path):
        return artifacts
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
    return artifacts

def load_audio_guides():
    path = os.path.join(data_dir, 'audioguides.txt')
    guides = []
    if not os.path.exists(path):
        return guides
    with open(path, 'r', encoding='utf-8') as f:
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
                    'created_by': parts[7],
                })
    return guides

def load_tickets():
    path = os.path.join(data_dir, 'tickets.txt')
    tickets = []
    if not os.path.exists(path):
        return tickets
    with open(path, 'r', encoding='utf-8') as f:
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
                    'price': parts[6],
                    'visitor_name': parts[7],
                    'visitor_email': parts[8],
                    'purchase_date': parts[9],
                })
    return tickets

def save_tickets(tickets):
    path = os.path.join(data_dir, 'tickets.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for t in tickets:
            f.write(f"{t['ticket_id']}|{t['username']}|{t['ticket_type']}|{t['visit_date']}|{t['visit_time']}|{t['number_of_tickets']}|{t['price']}|{t['visitor_name']}|{t['visitor_email']}|{t['purchase_date']}\n")

def load_events():
    path = os.path.join(data_dir, 'events.txt')
    events = []
    if not os.path.exists(path):
        return events
    with open(path, 'r', encoding='utf-8') as f:
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
                    'created_by': parts[8],
                })
    return events

def load_event_registrations():
    path = os.path.join(data_dir, 'event_registrations.txt')
    registrations = []
    if not os.path.exists(path):
        return registrations
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) == 4:
                registrations.append({
                    'registration_id': int(parts[0]),
                    'event_id': int(parts[1]),
                    'username': parts[2],
                    'registration_date': parts[3],
                })
    return registrations

def save_event_registrations(registrations):
    path = os.path.join(data_dir, 'event_registrations.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for r in registrations:
            f.write(f"{r['registration_id']}|{r['event_id']}|{r['username']}|{r['registration_date']}\n")

# ---- Routes ----

@app.route('/')
def root():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    exhibitions = load_exhibitions()
    total_exhibitions = len(exhibitions)
    # Active exhibitions based on current date between start and end dates (inclusive)
    today = datetime.today().date()
    active_exhibitions = 0
    for e in exhibitions:
        try:
            s = datetime.strptime(e['start_date'], '%Y-%m-%d').date()
            ed = datetime.strptime(e['end_date'], '%Y-%m-%d').date()
            if s <= today <= ed:
                active_exhibitions += 1
        except Exception:
            pass
    return render_template('dashboard.html', total_exhibitions=total_exhibitions, active_exhibitions=active_exhibitions)

@app.route('/artifacts', methods=['GET'])
def artifacts():
    artifacts = load_artifacts()
    exhibitions = load_exhibitions()
    exhibition_map = {e['exhibition_id']: e['title'] for e in exhibitions}
    for a in artifacts:
        a['exhibition_title'] = exhibition_map.get(a['exhibition_id'], 'Unknown')
    return render_template('artifact_catalog.html', artifacts=artifacts)

@app.route('/artifacts/search', methods=['POST'])
def artifact_search():
    search_term = request.form.get('search-artifact', '').strip().lower()
    artifacts = load_artifacts()
    exhibitions = load_exhibitions()
    exhibition_map = {e['exhibition_id']: e['title'] for e in exhibitions}
    filtered = []
    for a in artifacts:
        if search_term == '' or search_term in str(a['artifact_id']).lower() or search_term in a['artifact_name'].lower():
            a['exhibition_title'] = exhibition_map.get(a['exhibition_id'], 'Unknown')
            filtered.append(a)
    return render_template('artifact_catalog.html', artifacts=filtered)

@app.route('/exhibitions', methods=['GET'])
def exhibitions_view():
    exhibitions = load_exhibitions()
    galleries = load_galleries()
    gallery_map = {g['gallery_id']: g['gallery_name'] for g in galleries}
    # Determine status per gallery status (if gallery status is "Open" the exhibition is active, else maybe Renovation or closed)
    for e in exhibitions:
        gname = gallery_map.get(e['gallery_id'], 'Unknown Gallery')
        e['gallery_name'] = gname
        try:
            s = datetime.strptime(e['start_date'], '%Y-%m-%d').date()
            ed = datetime.strptime(e['end_date'], '%Y-%m-%d').date()
            today = datetime.today().date()
            status = 'Active' if s <= today <= ed else 'Inactive'
            if gname == 'Unknown Gallery':
                status = 'Inactive'
            # Reflect gallery status if not Open
            gallery_status = next((g['status'] for g in galleries if g['gallery_name'] == gname), 'Unknown')
            if gallery_status != 'Open':
                status = gallery_status
            e['status'] = status
        except Exception:
            e['status'] = 'Inactive'
    return render_template('exhibitions.html', exhibitions=exhibitions)

@app.route('/exhibitions/filter', methods=['POST'])
def exhibitions_filter():
    filter_type = request.form.get('filter-exhibition-type', '')
    exhibitions = load_exhibitions()
    galleries = load_galleries()
    gallery_map = {g['gallery_id']: g['gallery_name'] for g in galleries}
    filtered = []
    today = datetime.today().date()
    for e in exhibitions:
        if filter_type == '' or e['exhibition_type'] == filter_type:
            gname = gallery_map.get(e['gallery_id'], 'Unknown Gallery')
            e['gallery_name'] = gname
            try:
                s = datetime.strptime(e['start_date'], '%Y-%m-%d').date()
                ed = datetime.strptime(e['end_date'], '%Y-%m-%d').date()
                status = 'Active' if s <= today <= ed else 'Inactive'
                if gname == 'Unknown Gallery':
                    status = 'Inactive'
                gallery_status = next((g['status'] for g in galleries if g['gallery_name'] == gname), 'Unknown')
                if gallery_status != 'Open':
                    status = gallery_status
                e['status'] = status
            except Exception:
                e['status'] = 'Inactive'
            filtered.append(e)
    return render_template('exhibitions.html', exhibitions=filtered)

@app.route('/exhibitions/<int:exhibition_id>', methods=['GET'])
def exhibition_details(exhibition_id):
    exhibitions = load_exhibitions()
    exhibition = next((e for e in exhibitions if e['exhibition_id'] == exhibition_id), None)
    if not exhibition:
        return "Exhibition not found", 404
    artifacts = load_artifacts()
    related_artifacts = [a for a in artifacts if a['exhibition_id'] == exhibition_id]
    return render_template('exhibition_details.html', exhibition=exhibition, artifacts=related_artifacts)

@app.route('/tickets', methods=['GET'])
def visitor_tickets():
    # Simulate current user as 'visitor_mary' per examples
    current_user = 'visitor_mary'
    tickets = load_tickets()
    user_tickets = [t for t in tickets if t['username'] == current_user]
    return render_template('visitor_tickets.html', tickets=user_tickets)

@app.route('/tickets/purchase', methods=['POST'])
def purchase_ticket():
    # Simulate current user as 'visitor_mary'
    current_user = 'visitor_mary'
    ticket_type = request.form.get('ticket-type')
    number_of_tickets = request.form.get('number-of-tickets')
    visitor_name = request.form.get('visitor-name', '').strip()
    visitor_email = request.form.get('visitor-email', '').strip()
    visit_date = request.form.get('visit-date', '').strip()
    visit_time = request.form.get('visit-time', '').strip()

    if not ticket_type or not number_of_tickets or not visitor_name or not visitor_email or not visit_date or not visit_time:
        # Missing required fields - reload existing tickets
        tickets = load_tickets()
        user_tickets = [t for t in tickets if t['username'] == current_user]
        return render_template('visitor_tickets.html', tickets=user_tickets)

    try:
        number_of_tickets = int(number_of_tickets)
    except Exception:
        number_of_tickets = 1

    tickets = load_tickets()
    max_id = max((t['ticket_id'] for t in tickets), default=0)
    # Calculate price placeholder (simple flat price per type, could be extended)
    price_per_ticket = {
        'Standard': 15,
        'Student': 10,
        'Senior': 12,
        'Family': 40,
        'VIP': 50
    }.get(ticket_type, 15)

    total_price = price_per_ticket * number_of_tickets
    purchase_date = datetime.today().strftime('%Y-%m-%d')

    new_ticket = {
        'ticket_id': max_id + 1,
        'username': current_user,
        'ticket_type': ticket_type,
        'visit_date': visit_date,
        'visit_time': visit_time,
        'number_of_tickets': number_of_tickets,
        'price': total_price,
        'visitor_name': visitor_name,
        'visitor_email': visitor_email,
        'purchase_date': purchase_date,
    }

    tickets.append(new_ticket)
    save_tickets(tickets)

    user_tickets = [t for t in tickets if t['username'] == current_user]
    return render_template('visitor_tickets.html', tickets=user_tickets)

@app.route('/events', methods=['GET'])
def virtual_events():
    current_user = 'visitor_mary'
    events = load_events()
    registrations = load_event_registrations()
    event_reg_map = { (r['event_id'], r['username']): r for r in registrations }
    events_view = []
    for e in events:
        reg = event_reg_map.get((e['event_id'], current_user), None)
        e_copy = e.copy()
        e_copy['registration_status'] = 'Registered' if reg else 'Not Registered'
        if reg:
            e_copy['registration_id'] = reg['registration_id']
        events_view.append(e_copy)
    return render_template('virtual_events.html', events=events_view)

@app.route('/events/register/<int:event_id>', methods=['POST'])
def register_event(event_id):
    current_user = 'visitor_mary'
    registrations = load_event_registrations()
    events = load_events()
    # Check if already registered
    for r in registrations:
        if r['event_id'] == event_id and r['username'] == current_user:
            # Already registered
            break
    else:
        max_id = max([r['registration_id'] for r in registrations], default=0)
        new_reg = {
            'registration_id': max_id + 1,
            'event_id': event_id,
            'username': current_user,
            'registration_date': datetime.today().strftime('%Y-%m-%d'),
        }
        registrations.append(new_reg)
        save_event_registrations(registrations)
    
    # Refresh events list
    return redirect(url_for('virtual_events'))

@app.route('/events/cancel/<int:registration_id>', methods=['POST'])
def cancel_registration(registration_id):
    current_user = 'visitor_mary'
    registrations = load_event_registrations()
    registrations = [r for r in registrations if not (r['registration_id'] == registration_id and r['username'] == current_user)]
    save_event_registrations(registrations)
    return redirect(url_for('virtual_events'))

@app.route('/audio-guides', methods=['GET'])
def audio_guides():
    guides = load_audio_guides()
    return render_template('audio_guides.html', audio_guides=guides)

@app.route('/audio-guides/filter', methods=['POST'])
def audio_guides_filter():
    selected_language = request.form.get('filter-language')
    guides = load_audio_guides()
    filtered = []
    for g in guides:
        if selected_language == '' or g['language'] == selected_language:
            filtered.append(g)
    return render_template('audio_guides.html', audio_guides=filtered)

if __name__ == '__main__':
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    app.run(debug=True)
