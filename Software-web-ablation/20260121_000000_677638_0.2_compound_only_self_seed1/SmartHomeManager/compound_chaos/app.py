from flask import Flask, render_template, redirect, url_for, request
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Data file loading and saving functions

def read_devices(username=None):
    devices = []
    path = os.path.join(DATA_DIR, 'devices.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) < 13:
                    continue
                d = {
                    'username': parts[0],
                    'device_id': int(parts[1]),
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
                    'schedule_time': parts[12],
                }
                if username is None or d['username'] == username:
                    devices.append(d)
    except FileNotFoundError:
        pass
    return devices

def save_devices(devices):
    path = os.path.join(DATA_DIR, 'devices.txt')
    try:
        with open(path, 'w', encoding='utf-8') as f:
            for d in devices:
                line = '|'.join([
                    d['username'],
                    str(d['device_id']),
                    d['device_name'],
                    d['device_type'],
                    d['room'],
                    d['brand'],
                    d['model'],
                    d['status'],
                    d['power'],
                    d['brightness'],
                    d['temperature'],
                    d['mode'],
                    d['schedule_time']
                ]) + '\n'
                f.write(line)
    except Exception:
        pass

def read_rooms(username=None):
    rooms = []
    path = os.path.join(DATA_DIR, 'rooms.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) < 3:
                    continue
                r = {
                    'username': parts[0],
                    'room_id': int(parts[1]),
                    'room_name': parts[2],
                }
                if username is None or r['username'] == username:
                    rooms.append(r)
    except FileNotFoundError:
        pass
    return rooms

def read_automation_rules(username=None):
    rules = []
    path = os.path.join(DATA_DIR, 'automation_rules.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) < 9:
                    continue
                r = {
                    'username': parts[0],
                    'rule_id': int(parts[1]),
                    'rule_name': parts[2],
                    'trigger_type': parts[3],
                    'trigger_value': parts[4],
                    'action_device_id': int(parts[5]),
                    'action_type': parts[6],
                    'action_value': parts[7],
                    'enabled': parts[8].lower() == 'true',
                }
                if username is None or r['username'] == username:
                    rules.append(r)
    except FileNotFoundError:
        pass
    return rules

def save_automation_rules(rules):
    path = os.path.join(DATA_DIR, 'automation_rules.txt')
    try:
        with open(path, 'w', encoding='utf-8') as f:
            for r in rules:
                line = '|'.join([
                    r['username'],
                    str(r['rule_id']),
                    r['rule_name'],
                    r['trigger_type'],
                    r['trigger_value'],
                    str(r['action_device_id']),
                    r['action_type'],
                    r['action_value'],
                    'true' if r['enabled'] else 'false'
                ]) + '\n'
                f.write(line)
    except Exception:
        pass

def read_energy_logs(username=None):
    records = []
    path = os.path.join(DATA_DIR, 'energy_logs.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) < 4:
                    continue
                r = {
                    'username': parts[0],
                    'device_id': int(parts[1]),
                    'date': parts[2],
                    'consumption_kwh': float(parts[3]),
                }
                if username is None or r['username'] == username:
                    records.append(r)
    except FileNotFoundError:
        pass
    return records

def read_activity_logs(username=None):
    logs = []
    path = os.path.join(DATA_DIR, 'activity_logs.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) < 5:
                    continue
                log = {
                    'username': parts[0],
                    'timestamp': parts[1],
                    'device_id': int(parts[2]),
                    'action': parts[3],
                    'details': parts[4],
                }
                if username is None or log['username'] == username:
                    logs.append(log)
    except FileNotFoundError:
        pass
    return logs

# Helpers for generating ids

def get_next_device_id(devices):
    if not devices:
        return 1
    return max(d['device_id'] for d in devices) + 1

def get_next_rule_id(rules):
    if not rules:
        return 1
    return max(r['rule_id'] for r in rules) + 1

DEFAULT_USERNAME = 'john_doe'

# 1. Root Route
@app.route('/', methods=['GET'])
def root_redirect():
    return redirect(url_for('dashboard'))

# 2. Dashboard
@app.route('/dashboard', methods=['GET'])
def dashboard():
    username = DEFAULT_USERNAME
    devices = read_devices(username)
    rooms = read_rooms(username)

    total_devices = len(devices)
    active_devices = sum(1 for d in devices if d['status'].lower() == 'online')
    offline_devices = total_devices - active_devices

    room_counts = {r['room_name']: 0 for r in rooms}
    for d in devices:
        if d['room'] in room_counts:
            room_counts[d['room']] += 1

    return render_template('dashboard.html', total_devices=total_devices, active_devices=active_devices, offline_devices=offline_devices, rooms=room_counts)

# 3. Device List
@app.route('/devices', methods=['GET'])
def device_list():
    username = DEFAULT_USERNAME
    devices_all = read_devices(username)
    devices = [{
        'device_id': d['device_id'],
        'device_name': d['device_name'],
        'device_type': d['device_type'],
        'room': d['room'],
        'status': d['status']
    } for d in devices_all]
    return render_template('device_list.html', devices=devices)

# 4. Add Device
@app.route('/device/add', methods=['GET', 'POST'])
def add_device():
    username = DEFAULT_USERNAME
    devices = read_devices(username)
    rooms = read_rooms(username)

    device_types = sorted(set(d['device_type'] for d in devices))
    room_names = sorted(set(r['room_name'] for r in rooms))

    if request.method == 'POST':
        device_name = request.form.get('device_name', '').strip()
        device_type = request.form.get('device_type', '').strip()
        room = request.form.get('device_room', '').strip()

        if not device_name or not device_type or not room:
            return render_template('add_device.html', device_types=device_types, rooms=room_names)

        new_dev_id = get_next_device_id(devices)
        new_device = {
            'username': username,
            'device_id': new_dev_id,
            'device_name': device_name,
            'device_type': device_type,
            'room': room,
            'brand': '',
            'model': '',
            'status': 'Offline',
            'power': 'off',
            'brightness': '',
            'temperature': '',
            'mode': '',
            'schedule_time': ''
        }
        devices.append(new_device)
        save_devices(devices)
        return redirect(url_for('device_list'))

    return render_template('add_device.html', device_types=device_types, rooms=room_names)

# 5. Device Control
@app.route('/device/<int:device_id>/control', methods=['GET', 'POST'])
def device_control(device_id):
    username = DEFAULT_USERNAME
    devices = read_devices(username)
    device = next((d for d in devices if d['device_id'] == device_id and d['username'] == username), None)
    if not device:
        return redirect(url_for('device_list'))

    if request.method == 'POST':
        power = request.form.get('power')
        brightness = request.form.get('brightness', '')
        temperature = request.form.get('temperature', '')
        mode = request.form.get('mode', '')
        schedule_time = request.form.get('schedule_time', '')

        if power in ['on', 'off']:
            device['power'] = power
            device['status'] = 'Online' if power == 'on' else 'Offline'

        device['brightness'] = brightness
        device['temperature'] = temperature
        device['mode'] = mode
        device['schedule_time'] = schedule_time

        save_devices(devices)
        return redirect(url_for('device_control', device_id=device_id))

    device_ctx = {
        'device_id': device['device_id'],
        'device_name': device['device_name'],
        'status': device['status'],
        'power': device['power'],
        'brightness': device['brightness'],
        'temperature': device['temperature'],
        'mode': device['mode'],
        'schedule_time': device['schedule_time'],
    }
    return render_template('device_control.html', device=device_ctx)

# 6. Automation Rules
@app.route('/automation', methods=['GET', 'POST'])
def automation():
    username = DEFAULT_USERNAME
    rules = read_automation_rules(username)
    devices = read_devices(username)

    if request.method == 'POST':
        rule_name = request.form.get('rule_name', '').strip()
        trigger_type = request.form.get('trigger_type', '').strip()
        trigger_value = request.form.get('trigger_value', '').strip()
        action_device_id_str = request.form.get('action_device', '').strip()
        action_type = request.form.get('action_type', '').strip()

        if rule_name and trigger_type and action_device_id_str.isdigit() and action_type:
            action_device_id = int(action_device_id_str)
            new_rule_id = get_next_rule_id(rules)
            new_rule = {
                'username': username,
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
            save_automation_rules(rules)
            return redirect(url_for('automation'))

    devices_for_select = [{'device_id': d['device_id'], 'device_name': d['device_name']} for d in devices]
    return render_template('automation.html', automation_rules=rules, devices=devices_for_select)

# 7. Energy Report
@app.route('/energy', methods=['GET'])
def energy():
    username = DEFAULT_USERNAME
    energy_records = read_energy_logs(username)
    devices = read_devices(username)

    device_map = {d['device_id']: d['device_name'] for d in devices}

    date_filter = request.args.get('date_filter')

    filtered_records = []
    for rec in energy_records:
        if date_filter and rec['date'] != date_filter:
            continue
        filtered_records.append({
            'username': rec['username'],
            'device_id': rec['device_id'],
            'device_name': device_map.get(rec['device_id'], ''),
            'date': rec['date'],
            'consumption_kwh': rec['consumption_kwh'],
        })

    return render_template('energy.html', energy_records=filtered_records, date_filter=date_filter)

# 8. Activity Logs
@app.route('/activity', methods=['GET', 'POST'])
def activity_logs():
    username = DEFAULT_USERNAME
    logs = read_activity_logs(username)

    search_query = None
    if request.method == 'POST':
        search_query = request.form.get('search_query', '').strip()
        if search_query:
            logs = [log for log in logs if search_query.lower() in log['action'].lower() or search_query.lower() in log['details'].lower() or search_query.lower() in log['username'].lower()]

    return render_template('activity_logs.html', logs=logs, search_query=search_query)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
