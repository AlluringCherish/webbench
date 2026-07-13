from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)
DATA_DIR = 'data'

# Utility functions to read and write pipe-separated data files

def read_data_file(filename):
    filepath = os.path.join(DATA_DIR, filename)
    data = []
    if not os.path.exists(filepath):
        return data
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                data.append(line.split('|'))
    return data


def write_data_file(filename, data):
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        for row in data:
            f.write('|'.join(row) + '\n')


# Dashboard Page
@app.route('/')
def dashboard():
    return render_template('dashboard.html')


# Artifact Catalog Page
@app.route('/catalog')
def catalog():
    artifacts = read_data_file('artifacts.dat')
    # Prepare artifact dicts
    artifact_objs = []
    for art in artifacts:
        if len(art) >= 7:
            artifact_objs.append({
                'artifact_id': art[0],
                'exhibition_id': art[1],
                'name': art[2],
                'description': art[3],
                'origin': art[4],
                'year': art[5],
                'image_filename': art[6]
            })
    return render_template('catalog.html', artifacts=artifact_objs)


# Exhibitions Page
@app.route('/exhibitions')
def exhibitions():
    exhibitions = read_data_file('exhibitions.dat')
    exhibition_objs = []
    for ex in exhibitions:
        if len(ex) >= 6:
            exhibition_objs.append({
                'exhibition_id': ex[0],
                'gallery_id': ex[1],
                'title': ex[2],
                'description': ex[3],
                'start_date': ex[4],
                'end_date': ex[5]
            })

    return render_template('exhibitions.html', exhibitions=exhibition_objs)


# Exhibition Details Page
@app.route('/exhibitions/<exhibition_id>')
def exhibition_details(exhibition_id):
    exhibitions = read_data_file('exhibitions.dat')
    exhibition = None
    for ex in exhibitions:
        if ex[0] == exhibition_id:
            exhibition = {
                'exhibition_id': ex[0],
                'gallery_id': ex[1],
                'title': ex[2],
                'description': ex[3],
                'start_date': ex[4],
                'end_date': ex[5]
            }
            break
    if not exhibition:
        return "Exhibition not found", 404

    # Get artifacts for this exhibition
    artifacts = read_data_file('artifacts.dat')
    exhibition_artifacts = []
    for art in artifacts:
        if len(art) >= 7 and art[1] == exhibition_id:
            exhibition_artifacts.append({
                'artifact_id': art[0],
                'name': art[2],
                'description': art[3],
                'origin': art[4],
                'year': art[5],
                'image_filename': art[6]
            })

    return render_template('exhibition_details.html', exhibition=exhibition, artifacts=exhibition_artifacts)


# Visitor Tickets Page
@app.route('/tickets')
def tickets():
    tickets = read_data_file('tickets.dat')
    ticket_objs = []

    for t in tickets:
        if len(t) >= 5:
            ticket_objs.append({
                'ticket_id': t[0],
                'user_id': t[1],
                'exhibition_id': t[2],
                'purchase_date': t[3],
                'seat_number': t[4]
            })

    return render_template('tickets.html', tickets=ticket_objs)


# Virtual Events Page
@app.route('/events')
def events():
    events = read_data_file('events.dat')
    event_objs = []
    for ev in events:
        if len(ev) >= 6:
            event_objs.append({
                'event_id': ev[0],
                'title': ev[1],
                'description': ev[2],
                'event_date': ev[3],
                'start_time': ev[4],
                'end_time': ev[5]
            })
    return render_template('events.html', events=event_objs)


# Audio Guides Page
@app.route('/audio-guides')
def audio_guides():
    guides_data = read_data_file('audioguides.dat')
    guides = []
    for g in guides_data:
        if len(g) >= 5:
            guides.append({
                'audio_id': g[0],
                'artifact_id': g[1],
                'title': g[2],
                'audio_filename': g[3],
                'duration_seconds': g[4]
            })
    return render_template('audio_guides.html', guides=guides)


if __name__ == '__main__':
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    app.run(debug=True)
