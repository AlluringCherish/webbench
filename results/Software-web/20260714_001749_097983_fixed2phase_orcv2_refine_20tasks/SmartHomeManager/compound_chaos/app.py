from flask import Flask, render_template, request, redirect, url_for
import os
import uuid
from datetime import datetime

app = Flask(__name__)

# Data directory
DATA_DIR = 'data'
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# Data files
USERS_FILE = os.path.join(DATA_DIR, 'users.txt')
DEVICES_FILE = os.path.join(DATA_DIR, 'devices.txt')
ROOMS_FILE = os.path.join(DATA_DIR, 'rooms.txt')
AUTOMATION_FILE = os.path.join(DATA_DIR, 'automation_rules.txt')
ENERGY_FILE = os.path.join(DATA_DIR, 'energy_logs.txt')
ACTIVITY_FILE = os.path.join(DATA_DIR, 'activity_logs.txt')

# For simplification, assume single user login: john_doe
CURRENT_USER = 'john_doe'

# Utility functions for reading/writing data files

def read_users():
    users = {}
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 2:
                    users[parts[0]] = {'username': parts[0], 'email': parts[1]}
    return users

def read_devices(username):
    devices = []
    if os.path.exists(DEVICES_FILE):
        with open(DEVICES_FILE, 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 13 and parts[0] == username:
                    device = {
                        'username': parts[0],
                        'device_id': parts[1],
                        'device_name': parts[2],
                        'device_type': parts[3],
                        'room': parts[4],
                        'brand': parts[5],
                        'model': parts[6],
                        'status': parts[7], # Online or Offline
                        'power': parts[8],   # on or off
                        'brightness': parts[9], # optional
                        'temperature': parts[10], # optional
                        'mode': parts[11],    # optional
                        'schedule_time': parts[12] # optional
                    }
                    devices.append(device)
    return devices

def write_devices(username, devices):
    lines = []
    # Read all devices from file, then overwrite only current user's devices
    other_lines = []
    if os.path.exists(DEVICES_FILE):
        with open(DEVICES_FILE, 'r') as f:
            for line in f:
                if not line.startswith(username + '|'):
                    other_lines.append(line.strip())
    # Write all devices for this user freshly
    for d in devices:
        line = '|'.join([
            d['username'], d['device_id'], d['device_name'], d['device_type'], d['room'],
            d['brand'], d['model'], d['status'], d['power'], d['brightness'], d['temperature'],
            d['mode'], d['schedule_time']
        ])
        lines.append(line)
    all_lines = other_lines + lines
    with open(DEVICES_FILE, 'w') as f:
        f.write('\n'.join(all_lines))


def read_rooms(username):
    rooms = []
    if os.path.exists(ROOMS_FILE):
        with open(ROOMS_FILE, 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 3 and parts[0] == username:
                    room = {
                        'username': parts[0],
                        'room_id': parts[1],
                        'room_name': parts[2]
                    }
                    rooms.append(room)
    return rooms

def read_automation_rules(username):
    rules = []
    if os.path.exists(AUTOMATION_FILE):
        with open(AUTOMATION_FILE, 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 9 and parts[0] == username:
                    rule = {
                        'username': parts[0],
                        'rule_id': parts[1],
                        'rule_name': parts[2],
                        'trigger_type': parts[3],
                        'trigger_value': parts[4],
                        'action_device_id': parts[5],
                        'action_type': parts[6],
                        'action_value': parts[7],
                        'enabled': parts[8] == 'true'
                    }
                    rules.append(rule)
    return rules

def write_automation_rules(username, rules):
    lines = []
    other_lines = []
    if os.path.exists(AUTOMATION_FILE):
        with open(AUTOMATION_FILE, 'r') as f:
            for line in f:
                if not line.startswith(username + '|'):
                    other_lines.append(line.strip())
    for r in rules:
        line = '|'.join([
            r['username'], r['rule_id'], r['rule_name'], r['trigger_type'], r['trigger_value'],
            r['action_device_id'], r['action_type'], r['action_value'], 'true' if r['enabled'] else 'false'
        ])
        lines.append(line)
    all_lines = other_lines + lines
    with open(AUTOMATION_FILE, 'w') as f:
        f.write('\n'.join(all_lines))


def read_energy_logs(username):
    logs = []
    if os.path.exists(ENERGY_FILE):
        with open(ENERGY_FILE, 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 4 and parts[0] == username:
                    log = {
                        'username': parts[0],
                        'device_id': parts[1],
                        'date': parts[2],
                        'consumption_kwh': float(parts[3])
                    }
                    logs.append(log)
    return logs


def read_activity_logs(username):
    logs = []
    if os.path.exists(ACTIVITY_FILE):
        with open(ACTIVITY_FILE, 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 5 and parts[0] == username:
                    log = {
                        'username': parts[0],
                        'timestamp': parts[1],
                        'device_id': parts[2],
                        'action': parts[3],
                        'details': parts[4]
                    }
                    logs.append(log)
    return logs


def write_activities(username, logs):
    lines = []
    other_lines = []
    if os.path.exists(ACTIVITY_FILE):
        with open(ACTIVITY_FILE, 'r') as f:
            for line in f:
                if not line.startswith(username + '|'):
                    other_lines.append(line.strip())
    for l in logs:
        line = '|'.join([
            l['username'], l['timestamp'], l['device_id'], l['action'], l['details']
        ])
        lines.append(line)
    all_lines = other_lines + lines
    with open(ACTIVITY_FILE, 'w') as f:
        f.write('\n'.join(all_lines))


# Routes implementation

@app.route('/')
def root():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    devices = read_devices(CURRENT_USER)
    rooms = read_rooms(CURRENT_USER)
    total_devices = len(devices)
    active_devices = len([d for d in devices if d['status'] == 'Online'])
    offline_devices = len([d for d in devices if d['status'] == 'Offline'])

    # Room device counts
    room_counts = {}
    for room in rooms:
        room_counts[room['room_name']] = len([d for d in devices if d['room'] == room['room_name']])

    return render_template('dashboard.html',
                           total_devices=total_devices,
                           active_devices=active_devices,
                           offline_devices=offline_devices,
                           rooms=rooms,
                           room_counts=room_counts)

@app.route('/devices')
def devices():
    devices = read_devices(CURRENT_USER)
    return render_template('device_list.html', devices=devices)

@app.route('/add-device', methods=['GET', 'POST'])
def add_device():
    if request.method == 'POST':
        device_name = request.form.get('device-name')
        device_type = request.form.get('device-type')
        device_room = request.form.get('device-room')
        # For simplicity, brand and model default
        brand = 'Generic'
        model = 'Standard'

        # Generate new device_id
        devices = read_devices(CURRENT_USER)
        existing_ids = {int(d['device_id']) for d in devices}
        new_id = str(max(existing_ids) + 1 if existing_ids else 1)

        new_device = {
            'username': CURRENT_USER,
            'device_id': new_id,
            'device_name': device_name,
            'device_type': device_type,
            'room': device_room,
            'brand': brand,
            'model': model,
            'status': 'Online',
            'power': 'off',
            'brightness': '',
            'temperature': '',
            'mode': '',
            'schedule_time': ''
        }
        devices.append(new_device)
        write_devices(CURRENT_USER, devices)
        return redirect(url_for('devices'))

    # GET
    return render_template('add_device.html')

@app.route('/device-control/<device_id>', methods=['GET', 'POST'])
def device_control(device_id):
    devices = read_devices(CURRENT_USER)
    device = next((d for d in devices if d['device_id'] == device_id), None)
    if not device:
        return "Device not found", 404

    if request.method == 'POST':
        if 'power-toggle' in request.form:
            # Toggle power
            device['power'] = 'off' if device['power'] == 'on' else 'on'
            # Change status accordingly
            device['status'] = 'Online' if device['power'] == 'on' else 'Offline'

            # Log activity
            logs = read_activity_logs(CURRENT_USER)
            logs.append({
                'username': CURRENT_USER,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'device_id': device_id,
                'action': 'Power Toggle',
                'details': 'Power turned ' + device['power']
            })
            write_activities(CURRENT_USER, logs)

        elif 'save-settings-button' in request.form:
            if device['device_type'] == 'Light':
                brightness = request.form.get('brightness')
                device['brightness'] = brightness if brightness else ''
            elif device['device_type'] == 'Thermostat':
                temperature = request.form.get('temperature')
                mode = request.form.get('mode')
                schedule_time = request.form.get('schedule_time')
                device['temperature'] = temperature if temperature else ''
                device['mode'] = mode if mode else ''
                device['schedule_time'] = schedule_time if schedule_time else ''

            # Log activity
            logs = read_activity_logs(CURRENT_USER)
            logs.append({
                'username': CURRENT_USER,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'device_id': device_id,
                'action': 'Settings Changed',
                'details': 'Device settings updated'
            })
            write_activities(CURRENT_USER, logs)

        # Save devices
        write_devices(CURRENT_USER, devices)
        return redirect(url_for('device_control', device_id=device_id))

    # GET
    return render_template('device_control.html', device=device)

@app.route('/automation', methods=['GET', 'POST'])
def automation():
    devices = read_devices(CURRENT_USER)
    rules = read_automation_rules(CURRENT_USER)
    if request.method == 'POST':
        rule_name = request.form.get('rule-name')
        trigger_type = request.form.get('trigger-type')
        trigger_value = request.form.get('trigger-value')
        action_device_id = request.form.get('action-device')
        action_type = request.form.get('action-type')

        # Generate new rule_id
        existing_ids = {int(r['rule_id']) for r in rules}
        new_rule_id = str(max(existing_ids) + 1 if existing_ids else 1)

        new_rule = {
            'username': CURRENT_USER,
            'rule_id': new_rule_id,
            'rule_name': rule_name,
            'trigger_type': trigger_type,
            'trigger_value': trigger_value,
            'action_device_id': action_device_id,
            'action_type': action_type,
            'action_value': '',
            'enabled': True
        }
        rules.append(new_rule)
        write_automation_rules(CURRENT_USER, rules)
        return redirect(url_for('automation'))

    return render_template('automation.html', rules=rules, devices=devices)

@app.route('/energy', methods=['GET', 'POST'])
def energy():
    devices = read_devices(CURRENT_USER)
    logs = read_energy_logs(CURRENT_USER)
    filtered_logs = logs
    date_filter = ''
    if request.method == 'POST':
        date_filter = request.form.get('date-filter')
        if date_filter:
            filtered_logs = [log for log in logs if log['date'] == date_filter]

    # Calculate total energy and cost estimate
    total_kwh = sum(log['consumption_kwh'] for log in filtered_logs)
    cost_per_kwh = 0.12 # assume
    total_cost = total_kwh * cost_per_kwh

    # Add device name to each log
    for log in filtered_logs:
        device = next((d for d in devices if d['device_id'] == log['device_id']), None)
        log['device_name'] = device['device_name'] if device else 'Unknown'

    return render_template('energy.html', energy_logs=filtered_logs, total_kwh=total_kwh, total_cost=total_cost, date_filter=date_filter)

@app.route('/activity', methods=['GET', 'POST'])
def activity():
    devices = read_devices(CURRENT_USER)
    logs = read_activity_logs(CURRENT_USER)
    search_term = ''
    filtered_logs = logs
    if request.method == 'POST':
        search_term = request.form.get('search-activity')
        if search_term:
            filtered_logs = [l for l in logs if search_term.lower() in l['action'].lower() or search_term.lower() in l['details'].lower()]

    # Add device name
    for log in filtered_logs:
        device = next((d for d in devices if d['device_id'] == log['device_id']), None)
        log['device_name'] = device['device_name'] if device else 'Unknown'

    return render_template('activity.html', activity_logs=filtered_logs, search_term=search_term)

if __name__ == '__main__':
    app.run(debug=True)
