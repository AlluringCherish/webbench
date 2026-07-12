from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

data_dir = 'data'

# Utility to read pipe-delimited file into list of lists
# Ignores empty lines
# Return [] if file doesn't exist

def read_pipe_file(filename):
    filepath = os.path.join(data_dir, filename)
    data = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if line:
                    data.append(line.split('|'))
    except FileNotFoundError:
        pass
    except IOError:
        pass
    return data

# Utility to write the entire pipe-delimited content to file (overwrite)
def write_pipe_file(filename, data):
    filepath = os.path.join(data_dir, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        for row in data:
            f.write('|'.join(str(x) for x in row) + '\n')


@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    # Load exhibitions and count total and active
    exhibitions_data = read_pipe_file('exhibitions.txt')
    # Fields: exhibition_id|title|description|gallery_id|exhibition_type|start_date|end_date|curator_name|created_by

    total_exhibitions = len(exhibitions_data)
    active_exhibitions = 0
    today_str = datetime.today().strftime('%Y-%m-%d')

    for row in exhibitions_data:
        if len(row) < 7:
            continue
        start_date = row[5]
        end_date = row[6]
        if start_date <= today_str <= end_date:
            active_exhibitions += 1

    return render_template('dashboard.html', total_exhibitions=total_exhibitions, active_exhibitions=active_exhibitions)


@app.route('/artifact-catalog', methods=['GET', 'POST'])
def artifact_catalog():
    artifacts_data = read_pipe_file('artifacts.txt')
    exhibitions_data = read_pipe_file('exhibitions.txt')
    # exhibition_id to title map
    exhibition_title_map = {}
    for e in exhibitions_data:
        if len(e) < 2:
            continue
        try:
            exhibition_id_key = int(e[0])
            exhibition_title_map[exhibition_id_key] = e[1]
        except ValueError:
            continue

    artifacts = []
    # Parse all artifacts into dicts
    for row in artifacts_data:
        if len(row) < 6:
            continue
        try:
            artifact_id = int(row[0])
            artifact_name = row[1]
            period = row[2]
            origin = row[3]
            exhibition_id = int(row[5])
            exhibition_title = exhibition_title_map.get(exhibition_id, "Unknown")
            artifacts.append({
                'artifact_id': artifact_id,
                'artifact_name': artifact_name,
                'period': period,
                'origin': origin,
                'exhibition_title': exhibition_title
            })
        except ValueError:
            continue

    if request.method == 'POST':
        search_term = request.form.get('search-artifact', '').strip().lower()
        if search_term:
            filtered = []
            for a in artifacts:
                # Search by artifact_name or artifact_id (as string)
                if search_term in a['artifact_name'].lower() or search_term == str(a['artifact_id']):
                    filtered.append(a)
            artifacts = filtered

    return render_template('artifact_catalog.html', artifacts=artifacts)


@app.route('/exhibitions', methods=['GET', 'POST'])
def exhibitions():
    exhibitions_data = read_pipe_file('exhibitions.txt')
    galleries_data = read_pipe_file('galleries.txt')
    gallery_map = {}
    for g in galleries_data:
        if len(g) < 2:
            continue
        try:
            gallery_id = int(g[0])
            gallery_name = g[1]
            gallery_map[gallery_id] = gallery_name
        except ValueError:
            continue

    exhibitions = []
    for row in exhibitions_data:
        if len(row) < 9:
            continue
        try:
            exhibition_id = int(row[0])
            title = row[1]
            exhibition_type = row[4]
            start_date = row[5]
            end_date = row[6]
            gallery_id = int(row[3])
            gallery_name = gallery_map.get(gallery_id, "Unknown")
            # Determine status - active or ended or upcoming
            # For status we take from galleries.txt? No, spec says exhibition has status (?), but from data schema, 'status' is in galleries.txt only.
            # spec says status field with string (e.g. Open, Renovation) only for galleries
            # exhibitions.html: status is in exhibition dict, so we'll build status as 'Active' if today between start_date and end_date, else 'Inactive'
            today_str = datetime.today().strftime('%Y-%m-%d')
            status = "Inactive"
            if start_date <= today_str <= end_date:
                status = "Active"

            exhibitions.append({
                'exhibition_id': exhibition_id,
                'title': title,
                'exhibition_type': exhibition_type,
                'start_date': start_date,
                'end_date': end_date,
                'gallery_name': gallery_name,
                'status': status
            })
        except ValueError:
            continue

    if request.method == 'POST':
        filter_type = request.form.get('filter-exhibition-type', '').strip()
        if filter_type and filter_type in ['Permanent', 'Temporary', 'Virtual']:
            exhibitions = [e for e in exhibitions if e['exhibition_type'] == filter_type]

    return render_template('exhibitions.html', exhibitions=exhibitions)


@app.route('/exhibition/<int:exhibition_id>')
def exhibition_details(exhibition_id):
    exhibitions_data = read_pipe_file('exhibitions.txt')
    artifacts_data = read_pipe_file('artifacts.txt')

    # Find exhibition info
    exhibition = None
    for row in exhibitions_data:
        if len(row) < 4:
            continue
        try:
            eid = int(row[0])
        except ValueError:
            continue
        if eid == exhibition_id:
            exhibition = {
                'exhibition_id': eid,
                'title': row[1],
                'description': row[2],
                'start_date': row[5],
                'end_date': row[6]
            }
            break

    if exhibition is None:
        # Exhibition not found - show 404 page or redirect to exhibitions
        return redirect(url_for('exhibitions'))

    # Collect artifacts for this exhibition
    artifacts = []
    for row in artifacts_data:
        if len(row) < 6:
            continue
        try:
            artifact_id = int(row[0])
            artifact_exh_id = int(row[5])
        except ValueError:
            continue
        if artifact_exh_id == exhibition_id:
            artifacts.append({
                'artifact_id': artifact_id,
                'artifact_name': row[1],
                'period': row[2],
                'origin': row[3]
            })

    return render_template('exhibition_details.html', exhibition=exhibition, artifacts=artifacts)


@app.route('/visitor-tickets', methods=['GET', 'POST'])
def visitor_tickets():
    tickets_data = read_pipe_file('tickets.txt')
    available_ticket_types = ["Standard", "Student", "Senior", "Family", "VIP"]

    tickets = []
    # Parse existing tickets
    for row in tickets_data:
        if len(row) < 7:
            continue
        try:
            ticket_id = int(row[0])
            ticket_type = row[2]
            visit_date = row[3]
            visit_time = row[4]
            number_of_tickets = int(row[5])
            price = float(row[6])
            tickets.append({
                'ticket_id': ticket_id,
                'ticket_type': ticket_type,
                'visit_date': visit_date,
                'visit_time': visit_time,
                'number_of_tickets': number_of_tickets,
                'price': price
            })
        except ValueError:
            continue

    if request.method == 'POST':
        # We simulate adding a new ticket purchase
        # Form fields (we assume): ticket_type, visit_date, visit_time, number_of_tickets
        ticket_type = request.form.get('ticket-type', '')
        visit_date = request.form.get('visit-date', '')
        visit_time = request.form.get('visit-time', '')
        number_str = request.form.get('number-of-tickets', '0')
        try:
            number_of_tickets = int(number_str)
        except ValueError:
            number_of_tickets = 0

        if ticket_type in available_ticket_types and number_of_tickets > 0 and visit_date and visit_time:
            # Determine next ticket_id
            next_ticket_id = 1
            for t in tickets:
                if t['ticket_id'] >= next_ticket_id:
                    next_ticket_id = t['ticket_id'] + 1

            # Simple price calc: e.g. Base price Standard=15, Student=10, Senior=12, Family=40, VIP=50
            price_map = {
                "Standard": 15,
                "Student": 10,
                "Senior": 12,
                "Family": 40,
                "VIP": 50
            }
            price_per_ticket = price_map.get(ticket_type, 15)
            total_price = price_per_ticket * number_of_tickets

            # We do not have visitor info in spec, so use placeholder visitor_name and email
            visitor_name = "Unknown Visitor"
            visitor_email = "unknown@example.com"
            purchase_date = datetime.today().strftime('%Y-%m-%d')

            # Append new ticket entry to tickets.txt
            # ticket_id|username|ticket_type|visit_date|visit_time|number_of_tickets|price|visitor_name|visitor_email|purchase_date
            new_row = [
                str(next_ticket_id),
                "visitor_unknown",  # username placeholder
                ticket_type,
                visit_date,
                visit_time,
                str(number_of_tickets),
                f"{total_price:.2f}",
                visitor_name,
                visitor_email,
                purchase_date
            ]

            tickets_data.append(new_row)
            write_pipe_file('tickets.txt', tickets_data)

            # Refresh tickets list with new ticket included
            tickets.append({
                'ticket_id': next_ticket_id,
                'ticket_type': ticket_type,
                'visit_date': visit_date,
                'visit_time': visit_time,
                'number_of_tickets': number_of_tickets,
                'price': total_price
            })

    return render_template('visitor_tickets.html', tickets=tickets, available_ticket_types=available_ticket_types)


@app.route('/virtual-events')
def virtual_events():
    events_data = read_pipe_file('events.txt')
    registrations_data = read_pipe_file('event_registrations.txt')

    events = []
    for row in events_data:
        if len(row) < 9:
            continue
        try:
            event_id = int(row[0])
        except ValueError:
            continue
        # Fields: event_id|title|date|time|event_type|speaker|capacity|description|created_by
        events.append({
            'event_id': event_id,
            'title': row[1],
            'date': row[2],
            'time': row[3],
            'event_type': row[4],
            # registration_status dict with usernames keys, values boolean
            'registration_status': {}
        })

    # registrations: list of dict (registration_id: int, event_id: int)
    registrations = []
    for row in registrations_data:
        if len(row) < 4:
            continue
        try:
            registration_id = int(row[0])
            event_id_reg = int(row[1])
            username = row[2]
        except ValueError:
            continue
        registrations.append({'registration_id': registration_id, 'event_id': event_id_reg})

        # Add to event's registration_status
        for event_obj in events:
            if event_obj['event_id'] == event_id_reg:
                event_obj['registration_status'][username] = True

    return render_template('virtual_events.html', events=events, registrations=registrations)


@app.route('/virtual-events/register/<int:event_id>', methods=['POST'])
def register_event(event_id):
    registrations_data = read_pipe_file('event_registrations.txt')
    # Determine next registration_id
    next_registration_id = 1
    for row in registrations_data:
        if len(row) < 1:
            continue
        try:
            rid = int(row[0])
            if rid >= next_registration_id:
                next_registration_id = rid + 1
        except ValueError:
            continue

    # For the specification, we do not have user login info, so simulate a default user
    username = 'visitor_unknown'
    registration_date = datetime.today().strftime('%Y-%m-%d')

    # Add new registration
    new_row = [str(next_registration_id), str(event_id), username, registration_date]
    registrations_data.append(new_row)
    write_pipe_file('event_registrations.txt', registrations_data)

    return redirect(url_for('virtual_events'))


@app.route('/virtual-events/cancel/<int:registration_id>', methods=['POST'])
def cancel_event_registration(registration_id):
    registrations_data = read_pipe_file('event_registrations.txt')
    updated_registrations = []
    for row in registrations_data:
        if len(row) < 1:
            continue
        try:
            rid = int(row[0])
        except ValueError:
            continue
        if rid != registration_id:
            updated_registrations.append(row)
    write_pipe_file('event_registrations.txt', updated_registrations)

    return redirect(url_for('virtual_events'))


@app.route('/audio-guides', methods=['GET', 'POST'])
def audio_guides():
    audio_guides_data = read_pipe_file('audioguides.txt')

    audio_guides = []
    for row in audio_guides_data:
        if len(row) < 5:
            continue
        try:
            guide_id = int(row[0])
            exhibit_number = row[1]
            title = row[2]
            language = row[3]
            duration = int(row[4])
        except ValueError:
            continue
        audio_guides.append({
            'guide_id': guide_id,
            'exhibit_number': exhibit_number,
            'title': title,
            'language': language,
            'duration': duration
        })

    filter_languages = ["English", "Spanish", "French"]

    if request.method == 'POST':
        selected_language = request.form.get('filter-language', '').strip()
        if selected_language and selected_language in filter_languages:
            audio_guides = [a for a in audio_guides if a['language'] == selected_language]

    return render_template('audio_guides.html', audio_guides=audio_guides, filter_languages=filter_languages)


if __name__ == '__main__':
    app.run(port=5000, debug=True)
