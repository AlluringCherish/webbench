from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)
DATA_DIR = 'data'
CURRENT_USER = 'john_doe'  # Fixed for demo purpose

# Utility functions to read data files with pipe delimiter

def read_users():
    path = os.path.join(DATA_DIR, 'users.txt')
    users = []
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if line:
                    parts = line.split('|')
                    if len(parts) == 2:
                        users.append({'username': parts[0], 'email': parts[1]})
    return users


def read_devices():
    path = os.path.join(DATA_DIR, 'devices.txt')
    devices = []
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if line:
                    parts = line.split('|')
                    if len(parts) == 13:
                        devices.append({
                            'username': parts[0],
                            'device_id': parts[1],
                            'device_name': parts[2],
                            'device_type': parts[3],
                            'room': parts[4],
                            'brand': parts[5],
                            'model': parts[6],
                            'status': parts[7],
                            'power': parts[8],
                            'brightness': parts[9],
                            'temperature': parts[10],
                            'mode': parts[11],
                            'schedule_time': parts[12]
                        })
    return devices


def read_rooms():
    path = os.path.join(DATA_DIR, 'rooms.txt')
    rooms = []
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if line:
                    parts = line.split('|')
                    if len(parts) == 3:
                        rooms.append({'username': parts[0], 'room_id': parts[1], 'room_name': parts[2]})
    return rooms


def read_automation_rules():
    path = os.path.join(DATA_DIR, 'automation_rules.txt')
    rules = []
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if line:
                    parts = line.split('|')
                    if len(parts) == 9:
                        rules.append({
                            'username': parts[0],
                            'rule_id': parts[1],
                            'rule_name': parts[2],
                            'trigger_type': parts[3],
                            'trigger_value': parts[4],
                            'action_device_id': parts[5],
                            'action_type': parts[6],
                            'action_value': parts[7],
                            'enabled': parts[8].lower() == 'true'
                        })
    return rules


def read_energy_logs():
    path = os.path.join(DATA_DIR, 'energy_logs.txt')
    energy_logs = []
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if line:
                    parts = line.split('|')
                    if len(parts) == 4:
                        energy_logs.append({
                            'username': parts[0],
                            'device_id': parts[1],
                            'date': parts[2],
                            'consumption_kwh': float(parts[3]) if parts[3] else 0.0
                        })
    return energy_logs


def read_activity_logs():
    path = os.path.join(DATA_DIR, 'activity_logs.txt')
    activity_logs = []
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if line:
                    parts = line.split('|')
                    if len(parts) == 5:
                        activity_logs.append({
                            'username': parts[0],
                            'timestamp': parts[1],
                            'device_id': parts[2],
                            'action': parts[3],
                            'details': parts[4]
                        })
    return activity_logs


# Utility function to write devices data (overwrite file)
def write_devices(devices):
    path = os.path.join(DATA_DIR, 'devices.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for d in devices:
            line = '|'.join([
                d['username'], d['device_id'], d['device_name'], d['device_type'], d['room'], d['brand'], d['model'],
                d['status'], d['power'], d['brightness'], d['temperature'], d['mode'], d['schedule_time']
            ])
            f.write(line + '\n')


# Utility function to write automation rules data (overwrite file)
def write_automation_rules(rules):
    path = os.path.join(DATA_DIR, 'automation_rules.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for r in rules:
            line = '|'.join([
                r['username'], r['rule_id'], r['rule_name'], r['trigger_type'], r['trigger_value'], r['action_device_id'],
                r['action_type'], r['action_value'], 'true' if r['enabled'] else 'false'
            ])
            f.write(line + '\n')


# Dashboard page
@app.route('/')
def dashboard():
    devices = [d for d in read_devices() if d['username'] == CURRENT_USER]
    rooms = [r for r in read_rooms() if r['username'] == CURRENT_USER]

    total_devices = len(devices)
    active_devices = sum(1 for d in devices if d['status'].lower() == 'online')
    offline_devices = total_devices - active_devices

    # Count devices per room
    room_device_counts = {}
    for room in rooms:
        count = sum(1 for d in devices if d['room'] == room['room_name'])
        room_device_counts[room['room_name']] = count

    return render_template('templates_candidate_a/dashboard.html',
                           total_devices=total_devices,
                           active_devices=active_devices,
                           offline_devices=offline_devices,
                           room_device_counts=room_device_counts,
                           rooms=rooms)


# Device List page
@app.route('/devices')
def device_list():
    devices = [d for d in read_devices() if d['username'] == CURRENT_USER]
    return render_template('templates_candidate_a/device_list.html', devices=devices)


# Add Device page
@app.route('/devices/add', methods=['GET', 'POST'])
def add_device():
    rooms = [r['room_name'] for r in read_rooms() if r['username'] == CURRENT_USER]
    device_types = ['Light', 'Thermostat', 'Camera', 'Lock', 'Sensor', 'Appliance']

    if request.method == 'POST':
        device_name = request.form.get('device-name', '').strip()
        device_type = request.form.get('device-type', '')
        device_room = request.form.get('device-room', '')

        if device_name and device_type and device_room:
            devices = read_devices()
            # Generate new device_id unique for CURRENT_USER, max+1
            existing_ids = [int(d['device_id']) for d in devices if d['username'] == CURRENT_USER]
            new_id = str(max(existing_ids) + 1 if existing_ids else 1)
            new_device = {
                'username': CURRENT_USER,
                'device_id': new_id,
                'device_name': device_name,
                'device_type': device_type,
                'room': device_room,
                'brand': '',
                'model': '',
                'status': 'Offline',  # New device initially offline
                'power': 'off',
                'brightness': '',
                'temperature': '',
                'mode': '',
                'schedule_time': ''
            }
            devices.append(new_device)
            write_devices(devices)
            return redirect(url_for('device_list'))

    return render_template('templates_candidate_a/add_device.html', rooms=rooms, device_types=device_types)


# Device Control page
@app.route('/devices/control/<device_id>', methods=['GET', 'POST'])
def device_control(device_id):
    devices = read_devices()
    device = None
    for d in devices:
        if d['username'] == CURRENT_USER and d['device_id'] == device_id:
            device = d
            break
    if device is None:
        return redirect(url_for('device_list'))

    if request.method == 'POST':
        # Toggle power
        power = request.form.get('power')
        brightness = request.form.get('brightness')
        temperature = request.form.get('temperature')

        # Update device power
        if power == 'on':
            device['power'] = 'on'
            device['status'] = 'Online'
        elif power == 'off':
            device['power'] = 'off'
            device['status'] = 'Offline'

        # Update brightness and temperature if applicable
        if brightness is not None:
            device['brightness'] = brightness
        if temperature is not None:
            device['temperature'] = temperature

        # Save updated devices
        write_devices(devices)
        return redirect(url_for('device_control', device_id=device_id))

    return render_template('templates_candidate_a/device_control.html', device=device)


# Automation Rules page
@app.route('/automation', methods=['GET', 'POST'])
def automation_rules():
    rules = [r for r in read_automation_rules() if r['username'] == CURRENT_USER]
    devices = [d for d in read_devices() if d['username'] == CURRENT_USER]

    if request.method == 'POST':
        rule_name = request.form.get('rule-name', '').strip()
        trigger_type = request.form.get('trigger-type')
        trigger_value = request.form.get('trigger-value', '').strip()
        action_device_id = request.form.get('action-device')
        action_type = request.form.get('action-type')

        if rule_name and trigger_type and trigger_value and action_device_id and action_type:
            # Generate new rule_id max+1
            existing_ids = [int(r['rule_id']) for r in rules]
            new_id = str(max(existing_ids) + 1 if existing_ids else 1)
            new_rule = {
                'username': CURRENT_USER,
                'rule_id': new_id,
                'rule_name': rule_name,
                'trigger_type': trigger_type,
                'trigger_value': trigger_value,
                'action_device_id': action_device_id,
                'action_type': action_type,
                'action_value': '',
                'enabled': True
            }
            rules.append(new_rule)
            write_automation_rules(rules)
            return redirect(url_for('automation_rules'))

    return render_template('templates_candidate_a/automation_rules.html', rules=rules, devices=devices)


# Energy Report page
@app.route('/energy', methods=['GET', 'POST'])
def energy_report():
    energy_logs = [e for e in read_energy_logs() if e['username'] == CURRENT_USER]
    devices = {d['device_id']: d for d in read_devices() if d['username'] == CURRENT_USER}

    filter_date = None
    if request.method == 'POST':
        filter_date = request.form.get('date-filter')

    filtered_logs = []
    total_consumption = 0.0
    total_cost = 0.0

    for log in energy_logs:
        if filter_date and log['date'] != filter_date:
            continue
        filtered_logs.append(log)
        total_consumption += log['consumption_kwh']

    # Estimate cost: assume 0.12 per kWh
    total_cost = total_consumption * 0.12

    return render_template('templates_candidate_a/energy_report.html',
                           energy_logs=filtered_logs,
                           devices=devices,
                           total_consumption=total_consumption,
                           total_cost=total_cost,
                           filter_date=filter_date)


# Activity Logs page
@app.route('/activity', methods=['GET', 'POST'])
def activity_logs():
    logs = [l for l in read_activity_logs() if l['username'] == CURRENT_USER]
    devices = {d['device_id']: d for d in read_devices() if d['username'] == CURRENT_USER}

    search_term = None
    if request.method == 'POST':
        search_term = request.form.get('search-activity', '').strip().lower()

    filtered_logs = []
    if search_term:
        for log in logs:
            device_name = devices.get(log['device_id'], {}).get('device_name', '') if log['device_id'] else ''
            if (search_term in log['timestamp'].lower() or search_term in log['action'].lower() or
                search_term in log['details'].lower() or search_term in device_name.lower()):
                filtered_logs.append(log)
    else:
        filtered_logs = logs

    filtered_logs.sort(key=lambda x: x['timestamp'], reverse=True)

    return render_template('templates_candidate_a/activity_logs.html', logs=filtered_logs, devices=devices, search_term=search_term)


if __name__ == '__main__':
    app.run(debug=True)
