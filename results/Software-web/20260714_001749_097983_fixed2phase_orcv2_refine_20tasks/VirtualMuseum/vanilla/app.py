from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
import datetime

app = Flask(__name__)

DATA_DIR = 'data'
AUDIO_DIR = 'audio'

# Utility functions for file I/O

def read_pipe_separated_file(filename):
    path = os.path.join(DATA_DIR, filename)
    data = []
    if not os.path.exists(path):
        return data
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                data.append(line.split('|'))
    return data

def write_pipe_separated_file(filename, data):
    path = os.path.join(DATA_DIR, filename)
    with open(path, 'w', encoding='utf-8') as f:
        for record in data:
            f.write('|'.join(record) + '\n')

# Load data helpers

def load_exhibitions():
    exhibitions = read_pipe_separated_file('exhibitions.txt')
    exhibitions_dict = {}
    for e in exhibitions:
        exhibitions_dict[e[0]] = {
            'id': e[0],
            'name': e[1],
            'description': e[2],
            'gallery_id': e[3]
        }
    return exhibitions_dict

def load_artifacts():
    artifacts = read_pipe_separated_file('artifacts.txt')
    artifacts_list = []
    for a in artifacts:
        artifacts_list.append({
            'id': a[0],
            'name': a[1],
            'description': a[2],
            'exhibition_id': a[3]
        })
    return artifacts_list

def load_audioguides():
    guides = read_pipe_separated_file('audioguides.txt')
    audioguides_list = []
    for a in guides:
        audioguides_list.append({
            'id': a[0],
            'artifact_id': a[1],
            'audio_file_path': a[2]
        })
    return audioguides_list

def load_tickets():
    tickets = read_pipe_separated_file('tickets.txt')
    tickets_list = []
    for t in tickets:
        tickets_list.append({
            'id': t[0],
            'visitor_name': t[1],
            'exhibition_id': t[2],
            'date': t[3]
        })
    return tickets_list

def load_events():
    events = read_pipe_separated_file('events.txt')
    events_list = []
    for e in events:
        events_list.append({
            'id': e[0],
            'name': e[1],
            'description': e[2],
            'date': e[3],
            'time': e[4]
        })
    return events_list

def load_event_registrations():
    regs = read_pipe_separated_file('event_registrations.txt')
    regs_list = []
    for r in regs:
        regs_list.append({
            'id': r[0],
            'event_id': r[1],
            'visitor_name': r[2]
        })
    return regs_list

# Generate new unique id

def generate_new_id(data_list, id_index=0):
    max_id = 0
    for record in data_list:
        try:
            rid = int(record[id_index])
            if rid > max_id:
                max_id = rid
        except ValueError:
            pass
    return str(max_id + 1)

# Routes

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

# Artifact Catalog Page
@app.route('/artifact-catalog')
def artifact_catalog():
    artifacts = load_artifacts()
    exhibitions = load_exhibitions()
    return render_template('artifact_catalog.html', artifacts=artifacts, exhibitions=exhibitions)

# Exhibitions Page
@app.route('/exhibitions')
def exhibitions():
    exhibitions = load_exhibitions()
    return render_template('exhibitions.html', exhibitions=exhibitions)

# Exhibition Details Page
@app.route('/exhibition-details/<exhibition_id>')
def exhibition_details(exhibition_id):
    exhibitions = load_exhibitions()
    exhibition = exhibitions.get(exhibition_id)
    if not exhibition:
        return "Exhibition not found", 404
    artifacts = [a for a in load_artifacts() if a['exhibition_id'] == exhibition_id]
    return render_template('exhibition_details.html', exhibition=exhibition, artifacts=artifacts)

# Visitor Tickets Page
@app.route('/visitor-tickets', methods=['GET', 'POST'])
def visitor_tickets():
    exhibitions = load_exhibitions()
    message = ''
    if request.method == 'POST':
        visitor_name = request.form.get('visitor_name', '').strip()
        exhibition_id = request.form.get('exhibition_id')
        date = request.form.get('date')
        if visitor_name and exhibition_id and date:
            tickets = read_pipe_separated_file('tickets.txt')
            new_id = generate_new_id(tickets)
            tickets.append([new_id, visitor_name, exhibition_id, date])
            write_pipe_separated_file('tickets.txt', tickets)
            message = 'Ticket purchased successfully.'
        else:
            message = 'Please fill in all fields.'
    return render_template('visitor_tickets.html', exhibitions=exhibitions, message=message)

# Virtual Events Page
@app.route('/virtual-events', methods=['GET', 'POST'])
def virtual_events():
    events = load_events()
    registrations = load_event_registrations()
    message = ''
    if request.method == 'POST':
        visitor_name = request.form.get('visitor_name', '').strip()
        event_id = request.form.get('event_id')
        if visitor_name and event_id:
            event_regs = read_pipe_separated_file('event_registrations.txt')
            new_id = generate_new_id(event_regs)
            event_regs.append([new_id, event_id, visitor_name])
            write_pipe_separated_file('event_registrations.txt', event_regs)
            message = 'Registration successful.'
        else:
            message = 'Please fill in all fields.'
    return render_template('virtual_events.html', events=events, message=message)

# Audio Guides Page
@app.route('/audio-guides')
def audio_guides():
    audioguides = load_audioguides()
    artifacts = {a['id']: a for a in load_artifacts()}
    return render_template('audio_guides.html', audioguides=audioguides, artifacts=artifacts)

# API route to get exhibition by artifact id
@app.route('/api/exhibition-by-artifact/<artifact_id>')
def exhibition_by_artifact(artifact_id):
    artifacts = load_artifacts()
    exhibitions = load_exhibitions()
    found_artifact = next((a for a in artifacts if a['id'] == artifact_id), None)
    if not found_artifact:
        return jsonify({'error': 'Artifact not found'}), 404
    exhibition_id = found_artifact['exhibition_id']
    exhibition = exhibitions.get(exhibition_id)
    if not exhibition:
        return jsonify({'error': 'Exhibition not found'}), 404
    return jsonify({'exhibition_id': exhibition['id'], 'exhibition_name': exhibition['name']})

# API route to get tickets
@app.route('/api/tickets')
def api_tickets():
    tickets = load_tickets()
    return jsonify(tickets)

# Run app
if __name__ == '__main__':
    app.run(debug=True)
