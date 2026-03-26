from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_PATH = 'data'

# Helper functions for file reading and writing

def read_pipe_delimited_file(filename):
    file_path = os.path.join(DATA_PATH, filename)
    data = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if line:
                    data.append(line.split('|'))
    except FileNotFoundError:
        # No file means empty data
        pass
    except IOError:
        pass
    return data


def write_pipe_delimited_file(filename, data):
    file_path = os.path.join(DATA_PATH, filename)
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            for row in data:
                file.write('|'.join(str(item) for item in row) + '\n')
    except IOError:
        pass


def parse_date(date_str):
    try:
        return datetime.strptime(date_str, '%Y-%m-%d').date()
    except Exception:
        return None


def today_date():
    return datetime.today().date()


# Section: Root Route
@app.route('/', methods=['GET'])
def root_redirect():
    return redirect(url_for('dashboard'))


# Section: Dashboard /dashboard
@app.route('/dashboard', methods=['GET'])
def dashboard():
    # Load exhibitions from exhibitions.txt
    exhibitions_raw = read_pipe_delimited_file('exhibitions.txt')

    total_exhibitions = 0
    active_exhibitions_count = 0
    today = today_date()

    for row in exhibitions_raw:
        if len(row) < 9:
            continue
        # Fields according to Section 3: exhibition_id(int), title(str), description(str), gallery_id(int), exhibition_type(str), start_date(str YYYY-MM-DD), end_date(str YYYY-MM-DD), curator_name(str), created_by(str)
        exhibition_id = int(row[0])
        title = row[1]
        description = row[2]
        gallery_id = row[3]
        exhibition_type = row[4]
        start_date_str = row[5]
        end_date_str = row[6]
        curator_name = row[7]
        created_by = row[8]

        total_exhibitions += 1

        start_date = parse_date(start_date_str)
        end_date = parse_date(end_date_str)
        if start_date and end_date and start_date <= today <= end_date:
            active_exhibitions_count += 1

    return render_template('dashboard.html', total_exhibitions=total_exhibitions, active_exhibitions_count=active_exhibitions_count)


# Section: Artifact Catalog /artifacts GET,POST
@app.route('/artifacts', methods=['GET', 'POST'])
def artifact_catalog():
    # Get search_query from POST (form) or GET (args) parameter
    search_query = ''
    if request.method == 'POST':
        search_query = request.form.get('search_query', '').strip()
    else:
        search_query = request.args.get('search_query', '').strip()

    # Load all artifacts
    artifacts_raw = read_pipe_delimited_file('artifacts.txt')

    # Load exhibitions to map exhibition_id to title
    exhibitions_raw = read_pipe_delimited_file('exhibitions.txt')
    exhibition_id_title_map = {}
    for row in exhibitions_raw:
        if len(row) < 9:
            continue
        try:
            exhibition_id = int(row[0])
            title = row[1]
            exhibition_id_title_map[exhibition_id] = title
        except Exception:
            continue

    filtered_artifacts = []
    for row in artifacts_raw:
        if len(row) < 9:
            continue
        try:
            artifact_id = int(row[0])
            artifact_name = row[1]
            period = row[2]
            origin = row[3]
            # artifact description row[4], not needed here
            exhibition_id = int(row[5])
            exhibition_title = exhibition_id_title_map.get(exhibition_id, None) if exhibition_id != 0 else None

            # Filtering: if search_query non empty, case-insensitive substring in artifact_name, period, origin
            if search_query:
                sq_lower = search_query.lower()
                if (sq_lower in artifact_name.lower() or sq_lower in period.lower() or sq_lower in origin.lower()):
                    filtered_artifacts.append({
                        'artifact_id': artifact_id,
                        'artifact_name': artifact_name,
                        'period': period,
                        'origin': origin,
                        'exhibition_title': exhibition_title
                    })
            else:
                filtered_artifacts.append({
                    'artifact_id': artifact_id,
                    'artifact_name': artifact_name,
                    'period': period,
                    'origin': origin,
                    'exhibition_title': exhibition_title
                })
        except Exception:
            continue

    return render_template('artifact_catalog.html', artifacts_list=filtered_artifacts, search_query=search_query)


# Section: Exhibitions /exhibitions GET,POST
@app.route('/exhibitions', methods=['GET', 'POST'])
def exhibitions():
    filter_type = ''
    if request.method == 'POST':
        filter_type = request.form.get('filter_type', '').strip()
    else:
        filter_type = request.args.get('filter_type', '').strip()

    exhibitions_raw = read_pipe_delimited_file('exhibitions.txt')
    galleries_raw = read_pipe_delimited_file('galleries.txt')

    # Map gallery_id to gallery status and gallery_name
    gallery_status_map = {}
    gallery_name_map = {}
    for row in galleries_raw:
        if len(row) < 6:
            continue
        try:
            gallery_id = int(row[0])
            gallery_name = row[1]
            status = row[5]
            gallery_status_map[gallery_id] = status
            gallery_name_map[gallery_id] = gallery_name
        except Exception:
            continue

    exhibitions_list = []
    today = today_date()
    for row in exhibitions_raw:
        if len(row) < 9:
            continue
        try:
            exhibition_id = int(row[0])
            title = row[1]
            description = row[2]
            gallery_id = int(row[3])
            exhibition_type = row[4]
            start_date_str = row[5]
            end_date_str = row[6]
            curator_name = row[7]
            created_by = row[8]

            # Apply filter if filter_type selected and not empty
            if filter_type and exhibition_type != filter_type:
                continue

            start_date = parse_date(start_date_str)
            end_date = parse_date(end_date_str)

            # Derive status: if gallery status is not 'Open' then exhibition status is that
            # else if today < start_date: Upcoming
            # else if today > end_date: Past
            # else: Ongoing
            gallery_status = gallery_status_map.get(gallery_id, 'Open')
            if gallery_status != 'Open':
                status = gallery_status
            else:
                if start_date and today < start_date:
                    status = 'Upcoming'
                elif end_date and today > end_date:
                    status = 'Past'
                else:
                    status = 'Ongoing'

            exhibitions_list.append({
                'exhibition_id': exhibition_id,
                'title': title,
                'exhibition_type': exhibition_type,
                'start_date': start_date_str,
                'end_date': end_date_str,
                'gallery_name': gallery_name_map.get(gallery_id, ''),
                'status': status
            })
        except Exception:
            continue

    return render_template('exhibitions.html', exhibitions_list=exhibitions_list, filter_type=filter_type)


# Section: Exhibition Details /exhibition/<int:exhibition_id> GET
@app.route('/exhibition/<int:exhibition_id>', methods=['GET'])
def exhibition_details(exhibition_id):
    exhibitions_raw = read_pipe_delimited_file('exhibitions.txt')
    artifacts_raw = read_pipe_delimited_file('artifacts.txt')

    exhibition = None
    for row in exhibitions_raw:
        if len(row) < 9:
            continue
        try:
            eid = int(row[0])
            if eid == exhibition_id:
                exhibition = {
                    'exhibition_id': eid,
                    'title': row[1],
                    'description': row[2],
                    'start_date': row[5],
                    'end_date': row[6]
                }
                break
        except Exception:
            continue

    if not exhibition:
        # Exhibition not found, redirect to exhibitions page
        return redirect(url_for('exhibitions'))

    # Find artifacts belonging to this exhibition
    artifacts_in_exhibition = []
    for row in artifacts_raw:
        if len(row) < 9:
            continue
        try:
            a_exhibition_id = int(row[5])
            if a_exhibition_id == exhibition_id:
                artifacts_in_exhibition.append({
                    'artifact_id': int(row[0]),
                    'artifact_name': row[1],
                    'period': row[2],
                    'origin': row[3]
                })
        except Exception:
            continue

    return render_template('exhibition_details.html', exhibition=exhibition, artifacts_in_exhibition=artifacts_in_exhibition)


# Section: Visitor Tickets /visitor-tickets GET,POST
@app.route('/visitor-tickets', methods=['GET', 'POST'])
def visitor_tickets():
    # For this implementation, the "current user" is hardcoded or passed in query? Specification does not say.
    # We assume a query parameter 'username' for simpilicity; if not present, fallback to first user in users.txt.

    username = request.args.get('username', '').strip()
    if not username:
        # Try reading first user from users.txt
        users_raw = read_pipe_delimited_file('users.txt')
        if users_raw:
            username = users_raw[0][0]

    ticket_types = ['Standard', 'Student', 'Senior', 'Family', 'VIP']

    # Load tickets
    tickets_raw = read_pipe_delimited_file('tickets.txt')

    user_tickets = []
    for row in tickets_raw:
        if len(row) < 10:
            continue
        try:
            ticket_id = int(row[0])
            t_username = row[1]
            ticket_type = row[2]
            visit_date = row[3]
            visit_time = row[4]
            number_of_tickets = int(row[5])
            price = float(row[6])
            visitor_name = row[7]
            visitor_email = row[8]
            purchase_date = row[9]

            if t_username == username:
                user_tickets.append({
                    'ticket_id': ticket_id,
                    'ticket_type': ticket_type,
                    'visit_date': visit_date,
                    'visit_time': visit_time,
                    'number_of_tickets': number_of_tickets,
                    'price': price,
                    'visitor_name': visitor_name,
                    'visitor_email': visitor_email,
                    'purchase_date': purchase_date
                })
        except Exception:
            continue

    if request.method == 'POST':
        # Process ticket purchase
        ticket_type_form = request.form.get('ticket_type', '').strip()
        visit_date_form = request.form.get('visit_date', '').strip()
        visit_time_form = request.form.get('visit_time', '').strip()
        number_of_tickets_form = request.form.get('number_of_tickets', '').strip()
        visitor_name_form = request.form.get('visitor_name', '').strip()
        visitor_email_form = request.form.get('visitor_email', '').strip()

        # Validate inputs (basic)
        if (ticket_type_form in ticket_types and visit_date_form and visit_time_form and
                number_of_tickets_form.isdigit() and int(number_of_tickets_form) > 0 and
                visitor_name_form and visitor_email_form and username):

            # Calculate price based on ticket type and count
            price_per_ticket = {
                'Standard': 15.0,
                'Student': 10.0,
                'Senior': 12.0,
                'Family': 40.0,
                'VIP': 50.0
            }
            price_total = price_per_ticket[ticket_type_form] * int(number_of_tickets_form)
            
            # Generate new ticket_id
            max_ticket_id = 0
            for row in tickets_raw:
                try:
                    tid = int(row[0])
                    if tid > max_ticket_id:
                        max_ticket_id = tid
                except Exception:
                    continue
            new_ticket_id = max_ticket_id + 1

            purchase_date_str = datetime.now().strftime('%Y-%m-%d')

            new_row = [
                new_ticket_id,
                username,
                ticket_type_form,
                visit_date_form,
                visit_time_form,
                int(number_of_tickets_form),
                price_total,
                visitor_name_form,
                visitor_email_form,
                purchase_date_str
            ]

            # Append new ticket
            tickets_raw.append([str(i) if not isinstance(i, str) else i for i in new_row])
            write_pipe_delimited_file('tickets.txt', tickets_raw)

            return redirect(url_for('visitor_tickets', username=username))

    return render_template('visitor_tickets.html', user_tickets=user_tickets, ticket_types=ticket_types)


# Section: Virtual Events /virtual-events GET,POST
@app.route('/virtual-events', methods=['GET', 'POST'])
def virtual_events():
    # "Current user" as in visitor tickets route
    username = request.args.get('username', '').strip()
    if not username:
        users_raw = read_pipe_delimited_file('users.txt')
        if users_raw:
            username = users_raw[0][0]

    events_raw = read_pipe_delimited_file('events.txt')
    registrations_raw = read_pipe_delimited_file('event_registrations.txt')

    # Build events dict list
    events_list = []
    for row in events_raw:
        if len(row) < 9:
            continue
        try:
            event_id = int(row[0])
            title = row[1]
            date = row[2]
            time = row[3]
            event_type = row[4]
            speaker = row[5]
            capacity = int(row[6])
            description = row[7]
            created_by = row[8]

            # Determine registration status
            registration_status = 'Not Registered'
            for reg in registrations_raw:
                if len(reg) < 4:
                    continue
                try:
                    reg_id = int(reg[0])
                    reg_event_id = int(reg[1])
                    reg_username = reg[2]
                    if reg_event_id == event_id and reg_username == username:
                        registration_status = 'Registered'
                        break
                except Exception:
                    continue

            events_list.append({
                'event_id': event_id,
                'title': title,
                'date': date,
                'time': time,
                'event_type': event_type,
                'registration_status': registration_status
            })
        except Exception:
            continue

    user_registrations = []
    for reg in registrations_raw:
        if len(reg) < 4:
            continue
        try:
            reg_id = int(reg[0])
            reg_event_id = int(reg[1])
            reg_username = reg[2]
            if reg_username == username:
                user_registrations.append(reg_event_id)
        except Exception:
            continue

    if request.method == 'POST':
        # Need to know if user is registering or canceling.
        # We check form keys for "register_event_id" or "cancel_registration_id"

        register_event_id_str = request.form.get('register_event_id')
        cancel_registration_id_str = request.form.get('cancel_registration_id')

        changed = False
        if register_event_id_str and register_event_id_str.isdigit():
            register_event_id = int(register_event_id_str)
            # Check if already registered
            already_registered = False
            for reg in registrations_raw:
                try:
                    if int(reg[1]) == register_event_id and reg[2] == username:
                        already_registered = True
                        break
                except Exception:
                    continue

            if not already_registered:
                # Add new registration
                max_reg_id = 0
                for reg in registrations_raw:
                    try:
                        rid = int(reg[0])
                        if rid > max_reg_id:
                            max_reg_id = rid
                    except Exception:
                        continue
                new_reg_id = max_reg_id + 1
                registration_date_str = datetime.now().strftime('%Y-%m-%d')
                new_row = [
                    new_reg_id,
                    register_event_id,
                    username,
                    registration_date_str
                ]
                registrations_raw.append([str(i) if not isinstance(i, str) else i for i in new_row])
                changed = True

        elif cancel_registration_id_str and cancel_registration_id_str.isdigit():
            cancel_reg_id = int(cancel_registration_id_str)
            # Remove registration
            new_regs = []
            removed = False
            for reg in registrations_raw:
                if len(reg) < 4:
                    continue
                try:
                    rid = int(reg[0])
                    if rid == cancel_reg_id and reg[2] == username:
                        removed = True
                    else:
                        new_regs.append(reg)
                except Exception:
                    new_regs.append(reg)
            if removed:
                registrations_raw = new_regs
                changed = True

        if changed:
            write_pipe_delimited_file('event_registrations.txt', registrations_raw)
            return redirect(url_for('virtual_events', username=username))

    return render_template('virtual_events.html', events_list=events_list, user_registrations=user_registrations)


# Section: Audio Guides /audio-guides GET,POST
@app.route('/audio-guides', methods=['GET', 'POST'])
def audio_guides():
    filter_language = ''
    languages = ['English', 'Spanish', 'French']
    if request.method == 'POST':
        filter_language = request.form.get('filter_language', '').strip()
    else:
        filter_language = request.args.get('filter_language', '').strip()

    audioguides_raw = read_pipe_delimited_file('audioguides.txt')

    audio_guides_list = []
    for row in audioguides_raw:
        if len(row) < 8:
            continue
        try:
            guide_id = int(row[0])
            exhibit_number = row[1]
            title = row[2]
            language = row[3]
            duration = int(row[4])
            # script = row[5], narrator = row[6], created_by = row[7] - not used here

            if filter_language:
                if language != filter_language:
                    continue
            audio_guides_list.append({
                'guide_id': guide_id,
                'exhibit_number': exhibit_number,
                'title': title,
                'language': language,
                'duration': duration
            })
        except Exception:
            continue

    return render_template('audio_guides.html',
                           audio_guides_list=audio_guides_list,
                           filter_language=filter_language,
                           languages=languages)


if __name__ == '__main__':
    app.run(port=5000, debug=True)
