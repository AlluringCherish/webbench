from flask import Flask, render_template, redirect, url_for, request
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'
# For demonstration, assume a fixed username (single user scenario)
CURRENT_USER = 'john_doe'

# Utility functions to load data from files

def load_devices(username):
    devices = []
    filepath = os.path.join(DATA_DIR, 'devices.txt')
    if not os.path.exists(filepath):
        return devices
    with open(filepath, 'r') as f:
        for line in f:
            fields = line.strip().split('|')
            if len(fields) >= 13 and fields[0] == username:
                device = {
                    'username': fields[0],
                    'device_id': int(fields[1]),
                    'device_name': fields[2],
                    'device_type': fields[3],
                    'room': fields[4],
                    'brand': fields[5],
                    'model': fields[6],
                    'status': fields[7],
                    'power': fields[8],
                    'brightness': int(fields[9]) if fields[9].isdigit() else None,
                    'temperature': int(fields[10]) if fields[10].isdigit() else None,
                    'mode': fields[11] if fields[11] != '' else None,
                    'schedule_time': fields[12] if fields[12] != '' else None
                }
                devices.append(device)
    return devices

def load_rooms(username):
    rooms = []
    filepath = os.path.join(DATA_DIR, 'rooms.txt')
    if not os.path.exists(filepath):
        return rooms
    with open(filepath, 'r') as f:
        for line in f:
            fields = line.strip().split('|')
            if len(fields) >= 3 and fields[0] == username:
                room = {
                    'username': fields[0],
                    'room_id': int(fields[1]),
                    'room_name': fields[2]
                }
                rooms.append(room)
    return rooms

def load_automation_rules(username):
    rules = []
    filepath = os.path.join(DATA_DIR, 'automation_rules.txt')
    if not os.path.exists(filepath):
        return rules
    with open(filepath, 'r') as f:
        for line in f:
            fields = line.strip().split('|')
            if len(fields) >= 9 and fields[0] == username:
                rule = {
                    'username': fields[0],
                    'rule_id': int(fields[1]),
                    'rule_name': fields[2],
                    'trigger_type': fields[3],
                    'trigger_value': fields[4],
                    'action_device_id': int(fields[5]),
                    'action_type': fields[6],
                    'action_value': fields[7] if fields[7] != '' else None,
                    'enabled': fields[8].lower() == 'true'
                }
                rules.append(rule)
    return rules

def load_energy_logs(username):
    logs = []
    filepath = os.path.join(DATA_DIR, 'energy_logs.txt')
    if not os.path.exists(filepath):
        return logs
    with open(filepath, 'r') as f:
        for line in f:
            fields = line.strip().split('|')
            if len(fields) >= 4 and fields[0] == username:
                try:
                    log = {
                        'username': fields[0],
                        'device_id': int(fields[1]),
                        'date': fields[2],
                        'consumption_kwh': float(fields[3])
                    }
                    logs.append(log)
                except ValueError:
                    pass
    return logs

def load_activity_logs(username):
    activities = []
    filepath = os.path.join(DATA_DIR, 'activity_logs.txt')
    if not os.path.exists(filepath):
        return activities
    with open(filepath, 'r') as f:
        for line in f:
            fields = line.strip().split('|')
            if len(fields) >= 5 and fields[0] == username:
                activity = {
                    'username': fields[0],
                    'timestamp': fields[1],
                    'device_id': int(fields[2]),
                    'action': fields[3],
                    'details': fields[4]
                }
                activities.append(activity)
    return activities

# Saving devices back to devices.txt
from threading import Lock
file_lock = Lock()

def save_devices(devices):
    filepath = os.path.join(DATA_DIR, 'devices.txt')
    with file_lock:
        with open(filepath, 'w') as f:
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
                    str(d['brightness']) if d['brightness'] is not None else '',
                    str(d['temperature']) if d['temperature'] is not None else '',
                    d['mode'] if d['mode'] is not None else '',
                    d['schedule_time'] if d['schedule_time'] is not None else ''
                ])
                f.write(line + '\n')

def save_automation_rules(rules):
    filepath = os.path.join(DATA_DIR, 'automation_rules.txt')
    with file_lock:
        with open(filepath, 'w') as f:
            for r in rules:
                line = '|'.join([
                    r['username'],
                    str(r['rule_id']),
                    r['rule_name'],
                    r['trigger_type'],
                    r['trigger_value'],
                    str(r['action_device_id']),
                    r['action_type'],
                    r['action_value'] if r['action_value'] is not None else '',
                    'true' if r['enabled'] else 'false'
                ])
                f.write(line + '\n')

# Helper to get next device id
def next_device_id(devices):
    if not devices:
        return 1
    return max(d['device_id'] for d in devices) + 1

# Helper to get next rule id
def next_rule_id(rules):
    if not rules:
        return 1
    return max(r['rule_id'] for r in rules) + 1


@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard_page'))


@app.route('/dashboard')
def dashboard_page():
    devices = load_devices(CURRENT_USER)
    rooms = load_rooms(CURRENT_USER)

    # devices_summary: total, active, offline
    total = len(devices)
    active = sum(1 for d in devices if d['status'].lower() == 'online')
    offline = total - active
    devices_summary = {'total': total, 'active': active, 'offline': offline}

    # rooms_summary: list of dict {room_name, device_count}
    room_counts = {}
    for d in devices:
        room_counts[d['room']] = room_counts.get(d['room'], 0) + 1
    rooms_summary = []
    for room in rooms:
        count = room_counts.get(room['room_name'], 0)
        rooms_summary.append({'room_name': room['room_name'], 'device_count': count})

    return render_template('dashboard.html', devices_summary=devices_summary, rooms_summary=rooms_summary)


@app.route('/devices')
def device_list_page():
    devices = load_devices(CURRENT_USER)
    rooms = load_rooms(CURRENT_USER)
    user_rooms = [room['room_name'] for room in rooms]
    return render_template('devices.html', devices=devices, user_rooms=user_rooms)


@app.route('/device/add', methods=['GET', 'POST'])
def add_device_page():
    rooms = load_rooms(CURRENT_USER)
    device_types = ['Light', 'Thermostat', 'Camera', 'Lock', 'Sensor', 'Appliance']
    form_errors = {}

    if request.method == 'POST':
        name = request.form.get('device_name', '').strip()
        dtype = request.form.get('device_type', '')
        room = request.form.get('device_room', '')

        # Validate
        if not name:
            form_errors['device_name'] = 'Device name is required.'
        if dtype not in device_types:
            form_errors['device_type'] = 'Invalid device type selected.'
        room_names = [r['room_name'] for r in rooms]
        if room not in room_names:
            form_errors['device_room'] = 'Invalid room selected.'

        if form_errors:
            return render_template('add_device.html', rooms=room_names, device_types=device_types, form_errors=form_errors)

        # Add device
        devices = load_devices(CURRENT_USER)
        new_id = next_device_id(devices)
        new_device = {
            'username': CURRENT_USER,
            'device_id': new_id,
            'device_name': name,
            'device_type': dtype,
            'room': room,
            'brand': '',
            'model': '',
            'status': 'Offline',
            'power': 'off',
            'brightness': None,
            'temperature': None,
            'mode': None,
            'schedule_time': None
        }
        devices.append(new_device)
        save_devices(devices)
        return redirect(url_for('device_list_page'))

    # GET
    room_names = [r['room_name'] for r in rooms]
    return render_template('add_device.html', rooms=room_names, device_types=device_types, form_errors=form_errors)


@app.route('/device/<int:device_id>', methods=['GET', 'POST'])
def device_control_page(device_id):
    devices = load_devices(CURRENT_USER)
    device = next((d for d in devices if d['device_id'] == device_id), None)
    form_errors = {}

    if not device:
        # Device not found
        return "Device not found", 404

    if request.method == 'POST':
        # Example control: toggle power or update brightness, temperature
        power = request.form.get('power')
        brightness = request.form.get('brightness')
        temperature = request.form.get('temperature')
        mode = request.form.get('mode')
        schedule_time = request.form.get('schedule_time')
        
        # Validate power
        if power and power not in ['on', 'off']:
            form_errors['power'] = 'Power must be "on" or "off".'
        # Validate brightness
        if brightness:
            try:
                bval = int(brightness)
                if bval < 0 or bval > 100:
                    form_errors['brightness'] = 'Brightness must be between 0 and 100.'
            except ValueError:
                form_errors['brightness'] = 'Brightness must be an integer.'
        else:
            bval = None
        # Validate temperature
        if temperature:
            try:
                tval = int(temperature)
            except ValueError:
                form_errors['temperature'] = 'Temperature must be an integer.'
        else:
            tval = None
        # Validate mode - optional
        if mode == '':
            mode_val = None
        else:
            mode_val = mode
        # Validate schedule_time - optional
        if schedule_time == '':
            sched_val = None
        else:
            sched_val = schedule_time

        if form_errors:
            return render_template('device_control.html', device=device, status=device['status'], form_errors=form_errors)

        # Update device
        for d in devices:
            if d['device_id'] == device_id:
                if power:
                    d['power'] = power
                    # Simulate status change if power off device is offline
                    d['status'] = 'Online' if power == 'on' else 'Offline'
                d['brightness'] = bval
                d['temperature'] = tval
                d['mode'] = mode_val
                d['schedule_time'] = sched_val

        save_devices(devices)
        return redirect(url_for('device_control_page', device_id=device_id))

    # GET
    return render_template('device_control.html', device=device, status=device['status'], form_errors=form_errors)


@app.route('/automation', methods=['GET', 'POST'])
def automation_rules_page():
    rules = load_automation_rules(CURRENT_USER)
    devices = load_devices(CURRENT_USER)
    form_errors = {}

    if request.method == 'POST':
        # Add new rule
        name = request.form.get('rule_name', '').strip()
        trigger_type = request.form.get('trigger_type', '')
        trigger_value = request.form.get('trigger_value', '').strip()
        try:
            action_device_id = int(request.form.get('action_device', '0'))
        except ValueError:
            action_device_id = 0
        action_type = request.form.get('action_type', '')

        # Validate
        if not name:
            form_errors['rule_name'] = 'Rule name is required.'
        if trigger_type not in ['Time', 'Motion', 'Temperature']:
            form_errors['trigger_type'] = 'Invalid trigger type.'
        if not trigger_value:
            form_errors['trigger_value'] = 'Trigger value is required.'
        if action_device_id not in [d['device_id'] for d in devices]:
            form_errors['action_device'] = 'Invalid action device selected.'
        if action_type not in ['Turn On', 'Turn Off', 'Set Brightness', 'Set Temperature']:
            form_errors['action_type'] = 'Invalid action type.'

        if form_errors:
            return render_template('automation_rules.html', rules=rules, devices=devices, form_errors=form_errors)

        # Add rule
        new_id = next_rule_id(rules)
        new_rule = {
            'username': CURRENT_USER,
            'rule_id': new_id,
            'rule_name': name,
            'trigger_type': trigger_type,
            'trigger_value': trigger_value,
            'action_device_id': action_device_id,
            'action_type': action_type,
            'action_value': None,
            'enabled': True
        }
        rules.append(new_rule)
        save_automation_rules(rules)
        return redirect(url_for('automation_rules_page'))

    return render_template('automation_rules.html', rules=rules, devices=devices, form_errors=form_errors)


@app.route('/energy', methods=['GET', 'POST'])
def energy_report_page():
    energy_logs = load_energy_logs(CURRENT_USER)
    filter_date = ''
    if request.method == 'POST':
        filter_date = request.form.get('date_filter', '')

    # Apply date filter
    if filter_date:
        filtered_logs = [log for log in energy_logs if log['date'] == filter_date]
    else:
        filtered_logs = energy_logs

    total_kwh = sum(log['consumption_kwh'] for log in filtered_logs)
    # Estimate cost assuming fixed price 0.12 per kWh
    cost_estimate = total_kwh * 0.12
    summary = {'total_kwh': round(total_kwh, 2), 'cost_estimate': round(cost_estimate, 2)}

    return render_template('energy_report.html', energy_logs=filtered_logs, summary=summary, filter_date=filter_date)


@app.route('/activity', methods=['GET', 'POST'])
def activity_logs_page():
    activities = load_activity_logs(CURRENT_USER)
    search_term = ''
    if request.method == 'POST':
        search_term = request.form.get('search_term', '').strip()

    if search_term:
        filtered = []
        for act in activities:
            if (search_term.lower() in act['action'].lower() or
                search_term.lower() in act['details'].lower()):
                filtered.append(act)
        activities = filtered

    return render_template('activity_logs.html', activities=activities, search_term=search_term)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
