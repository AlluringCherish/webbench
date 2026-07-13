from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)
DATA_DIR = 'data'
CURRENT_USER = 'john_doe'

# Helper functions for file operations and parsing

def read_file_lines(filename):
    if not os.path.exists(filename):
        return []
    with open(filename, 'r') as f:
        return [line.strip() for line in f.readlines() if line.strip()]


def write_file_lines(filename, lines):
    with open(filename, 'w') as f:
        f.write('\n'.join(lines) + ('\n' if lines else ''))


def generate_id_from_lines(lines):
    if not lines:
        return 1
    max_id = 0
    for line in lines:
        parts = line.split('|')
        if len(parts) > 1:
            try:
                id_val = int(parts[1])
                if id_val > max_id:
                    max_id = id_val
            except:
                continue
    return max_id + 1

# Devices Related

def load_devices(username):
    devices = []
    lines = read_file_lines(os.path.join(DATA_DIR, 'devices.txt'))
    for line in lines:
        parts = line.split('|')
        if parts[0] == username and len(parts) >= 13:  # corrected to 13
            device = {
                'username': parts[0], 'device_id': parts[1], 'device_name': parts[2], 'device_type': parts[3], 'room': parts[4],
                'brand': parts[5], 'model': parts[6], 'status': parts[7], 'power': parts[8], 'brightness': parts[9],
                'temperature': parts[10], 'mode': parts[11], 'schedule_time': parts[12]
            }
            devices.append(device)
    return devices


def save_devices(username, devices):
    all_lines = read_file_lines(os.path.join(DATA_DIR, 'devices.txt'))
    new_lines = []
    # Remove user's old devices
    for line in all_lines:
        if not line.startswith(username + '|'):
            new_lines.append(line)
    # Add updated devices
    for d in devices:
        line = f"{username}|{d['device_id']}|{d['device_name']}|{d['device_type']}|{d['room']}|{d['brand']}|{d['model']}|{d['status']}|{d['power']}|{d['brightness']}|{d['temperature']}|{d['mode']}|{d.get('schedule_time','')}"
        new_lines.append(line)
    write_file_lines(os.path.join(DATA_DIR, 'devices.txt'), new_lines)


def get_device(username, device_id):
    devices = load_devices(username)
    for d in devices:
        if d['device_id'] == str(device_id):
            return d
    return None

# Rooms Related

def load_rooms(username):
    rooms = []
    lines = read_file_lines(os.path.join(DATA_DIR, 'rooms.txt'))
    for line in lines:
        parts = line.split('|')
        if parts[0] == username and len(parts) >= 3:
            room = {'username': parts[0], 'room_id': parts[1], 'room_name': parts[2]}
            rooms.append(room)
    return rooms

# Automation Rules

def load_rules(username):
    rules = []
    lines = read_file_lines(os.path.join(DATA_DIR, 'automation_rules.txt'))
    for line in lines:
        parts = line.split('|')
        if parts[0] == username and len(parts) >= 9:
            rule = {
                'username': parts[0], 'rule_id': parts[1], 'rule_name': parts[2], 'trigger_type': parts[3], 'trigger_value': parts[4],
                'action_device_id': parts[5], 'action_type': parts[6], 'action_value': parts[7], 'enabled': parts[8]
            }
            rules.append(rule)
    return rules


def save_rules(username, rules):
    all_lines = read_file_lines(os.path.join(DATA_DIR, 'automation_rules.txt'))
    new_lines = []
    # Remove user's old rules
    for line in all_lines:
        if not line.startswith(username + '|'):
            new_lines.append(line)
    # Add updated rules
    for r in rules:
        line = f"{username}|{r['rule_id']}|{r['rule_name']}|{r['trigger_type']}|{r['trigger_value']}|{r['action_device_id']}|{r['action_type']}|{r['action_value']}|{r['enabled']}"
        new_lines.append(line)
    write_file_lines(os.path.join(DATA_DIR, 'automation_rules.txt'), new_lines)

# Energy Logs

def load_energy_logs(username):
    logs = []
    lines = read_file_lines(os.path.join(DATA_DIR, 'energy_logs.txt'))
    for line in lines:
        parts = line.split('|')
        if parts[0] == username and len(parts) == 4:
            log = {'username': parts[0], 'device_id': parts[1], 'date': parts[2], 'consumption_kwh': parts[3]}
            logs.append(log)
    return logs

# Activity Logs

def load_activity_logs(username):
    logs = []
    lines = read_file_lines(os.path.join(DATA_DIR, 'activity_logs.txt'))
    for line in lines:
        parts = line.split('|')
        if parts[0] == username and len(parts) >= 5:
            # rest joined for details (in case details can contain |)
            details = '|'.join(parts[4:])
            log = {'username': parts[0], 'timestamp': parts[1], 'device_id': parts[2], 'action': parts[3], 'details': details}
            logs.append(log)
    return logs

# Dashboard Route
@app.route('/')
@app.route('/dashboard')
def dashboard():
    devices = load_devices(CURRENT_USER)
    rooms = load_rooms(CURRENT_USER)

    # Prepare device summary data
    total_devices = len(devices)
    online_devices = len([d for d in devices if d['status'] == 'Online'])
    offline_devices = total_devices - online_devices

    # Room list with device counts
    room_counts = {}
    for room in rooms:
        count = sum(1 for d in devices if d['room'] == room['room_name'])
        room_counts[room['room_name']] = count

    return render_template('dashboard.html', total_devices=total_devices, online_devices=online_devices,
                           offline_devices=offline_devices, room_counts=room_counts)

# Device List Route
@app.route('/devices')
def device_list():
    devices = load_devices(CURRENT_USER)
    return render_template('device_list.html', devices=devices)

# Add Device Route
@app.route('/devices/add', methods=['GET', 'POST'])
def add_device():
    if request.method == 'POST':
        name = request.form.get('device-name')
        dev_type = request.form.get('device-type')
        room = request.form.get('device-room')
        # For this implementation, brand, model can be static or empty
        brand = ''
        model = ''
        status = 'Online'
        power = 'off'
        brightness = ''
        temperature = ''
        mode = ''
        schedule_time = ''

        devices_lines = read_file_lines(os.path.join(DATA_DIR, 'devices.txt'))
        device_id = str(generate_id_from_lines(devices_lines))

        devices = load_devices(CURRENT_USER)

        new_device = {
            'device_id': device_id,
            'device_name': name,
            'device_type': dev_type,
            'room': room,
            'brand': brand,
            'model': model,
            'status': status,
            'power': power,
            'brightness': brightness,
            'temperature': temperature,
            'mode': mode,
            'schedule_time': schedule_time
        }
        devices.append(new_device)
        save_devices(CURRENT_USER, devices)
        return redirect(url_for('device_list'))
    return render_template('add_device.html')

# Device Control Route
@app.route('/devices/<device_id>/control', methods=['GET', 'POST'])
def device_control(device_id):
    device = get_device(CURRENT_USER, device_id)
    if not device:
        return "Device not found", 404

    if request.method == 'POST':
        # Toggle power button or save settings
        power = request.form.get('power')
        brightness = request.form.get('brightness', '')
        temperature = request.form.get('temperature', '')

        devices = load_devices(CURRENT_USER)
        for d in devices:
            if d['device_id'] == device_id:
                d['power'] = power if power else d['power']
                d['brightness'] = brightness
                d['temperature'] = temperature
                break
        save_devices(CURRENT_USER, devices)
        return redirect(url_for('device_list'))

    return render_template('device_control.html', device=device)

# Automation Rules Route
@app.route('/automation', methods=['GET', 'POST'])
def automation():
    rules_lines = read_file_lines(os.path.join(DATA_DIR, 'automation_rules.txt'))
    rules = load_rules(CURRENT_USER)
    devices = load_devices(CURRENT_USER)

    if request.method == 'POST':
        rule_name = request.form.get('rule-name')
        trigger_type = request.form.get('trigger-type')
        trigger_value = request.form.get('trigger-value')
        action_device_id = request.form.get('action-device')
        action_type = request.form.get('action-type')
        action_value = ''  # For extensibility, not used currently
        enabled = 'true'

        rule_id = str(generate_id_from_lines(rules_lines))
        new_rule = {
            'rule_id': rule_id,
            'rule_name': rule_name,
            'trigger_type': trigger_type,
            'trigger_value': trigger_value,
            'action_device_id': action_device_id,
            'action_type': action_type,
            'action_value': action_value,
            'enabled': enabled
        }
        rules.append(new_rule)
        save_rules(CURRENT_USER, rules)
        return redirect(url_for('automation'))

    return render_template('automation.html', rules=rules, devices=devices)

# Energy Report Route
@app.route('/energy', methods=['GET', 'POST'])
def energy():
    logs = load_energy_logs(CURRENT_USER)
    devices = load_devices(CURRENT_USER)
    filtered_logs = logs

    date_filter = ''
    if request.method == 'POST':
        date_filter = request.form.get('date-filter') or ''
        if date_filter:
            filtered_logs = [log for log in logs if log['date'] == date_filter]

    # Prepare summary total kWh
    total_kwh = sum(float(log['consumption_kwh']) for log in filtered_logs) if filtered_logs else 0

    # Map device names
    device_map = {d['device_id']: d['device_name'] for d in devices}

    return render_template('energy.html', energy_logs=filtered_logs, total_kwh=total_kwh, device_map=device_map, date_filter=date_filter)

# Activity Logs Route
@app.route('/activity', methods=['GET', 'POST'])
def activity():
    logs = load_activity_logs(CURRENT_USER)
    devices = load_devices(CURRENT_USER)
    search_term = ''
    filtered_logs = logs

    if request.method == 'POST':
        search_term = request.form.get('search-activity') or ''
        if search_term:
            filtered_logs = [log for log in logs if (search_term.lower() in (log['action'].lower() + ' ' + log['details'].lower()))]

    device_map = {d['device_id']: d['device_name'] for d in devices}

    return render_template('activity.html', logs=filtered_logs, device_map=device_map, search_term=search_term)

if __name__ == '__main__':
    os.makedirs(DATA_DIR, exist_ok=True)
    app.run(debug=True)
