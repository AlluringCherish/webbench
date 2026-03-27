from flask import Flask, render_template, redirect, url_for, request
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

# Constant for logged in user
LOGGED_IN_USERNAME = 'john_doe'

DATA_DIR = 'data'

# --- Helper function to read devices for given user ---
def read_devices(username):
    devices = []
    path = os.path.join(DATA_DIR, 'devices.txt')
    try:
        with open(path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                fields = line.split('|')
                if len(fields) < 13:
                    continue
                (
                    uname, device_id, device_name, device_type, room, brand,
                    model, status, power, brightness, temperature, mode, schedule_time
                ) = fields
                if uname == username:
                    device = {
                        'username': uname,
                        'device_id': int(device_id),
                        'device_name': device_name,
                        'device_type': device_type,
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
                    devices.append(device)
    except Exception:
        pass
    return devices

# --- Helper function to write devices (overwrite all) ---
def write_devices(devices, username):
    # Read all devices to keep other users unchanged
    path = os.path.join(DATA_DIR, 'devices.txt')
    lines = []
    try:
        # Read all lines to keep those not for this user
        if os.path.exists(path):
            with open(path, 'r') as f:
                for line in f:
                    if not line.strip():
                        continue
                    fields = line.strip().split('|')
                    if len(fields) < 13:
                        continue
                    if fields[0] != username:
                        lines.append(line.strip())
    except Exception:
        pass
    # Add new devices for the user
    for d in devices:
        line = '|'.join([
            d.get('username', username),
            str(d.get('device_id', '')),
            d.get('device_name', ''),
            d.get('device_type', ''),
            d.get('room', ''),
            d.get('brand', ''),
            d.get('model', ''),
            d.get('status', ''),
            d.get('power', ''),
            d.get('brightness', ''),
            d.get('temperature', ''),
            d.get('mode', ''),
            d.get('schedule_time', '')
        ])
        lines.append(line)
    try:
        with open(path, 'w') as f:
            for line in lines:
                f.write(line + '\n')
    except Exception:
        pass

# --- Helper function to read rooms for given user ---
def read_rooms(username):
    rooms = []
    path = os.path.join(DATA_DIR, 'rooms.txt')
    try:
        with open(path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                fields = line.split('|')
                if len(fields) < 3:
                    continue
                uname, room_id, room_name = fields
                if uname == username:
                    room = {
                        'username': uname,
                        'room_id': int(room_id),
                        'room_name': room_name
                    }
                    rooms.append(room)
    except Exception:
        pass
    return rooms

# --- Helper function to read automation rules ---
def read_automation_rules(username):
    rules = []
    path = os.path.join(DATA_DIR, 'automation_rules.txt')
    try:
        with open(path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                fields = line.split('|')
                if len(fields) < 9:
                    continue
                (
                    uname, rule_id, rule_name, trigger_type, trigger_value, action_device_id,
                    action_type, action_value, enabled
                ) = fields
                if uname == username:
                    rule = {
                        'username': uname,
                        'rule_id': int(rule_id),
                        'rule_name': rule_name,
                        'trigger_type': trigger_type,
                        'trigger_value': trigger_value,
                        'action_device_id': int(action_device_id),
                        'action_type': action_type,
                        'action_value': action_value,
                        'enabled': enabled.lower() == 'true'
                    }
                    rules.append(rule)
    except Exception:
        pass
    return rules

# --- Helper function to write automation rules (overwrite all) ---
def write_automation_rules(rules, username):
    path = os.path.join(DATA_DIR, 'automation_rules.txt')
    lines = []
    try:
        # Keep other users' rules
        if os.path.exists(path):
            with open(path, 'r') as f:
                for line in f:
                    if not line.strip():
                        continue
                    fields = line.strip().split('|')
                    if len(fields) < 9:
                        continue
                    if fields[0] != username:
                        lines.append(line.strip())
    except Exception:
        pass
    # Add current user's rules
    for r in rules:
        line = '|'.join([
            r.get('username', username),
            str(r.get('rule_id', '')),
            r.get('rule_name', ''),
            r.get('trigger_type', ''),
            r.get('trigger_value', ''),
            str(r.get('action_device_id', '')),
            r.get('action_type', ''),
            r.get('action_value', ''),
            'true' if r.get('enabled', False) else 'false'
        ])
        lines.append(line)
    try:
        with open(path, 'w') as f:
            for line in lines:
                f.write(line + '\n')
    except Exception:
        pass

# --- Helper function to read energy logs ---
def read_energy_logs(username):
    logs = []
    path = os.path.join(DATA_DIR, 'energy_logs.txt')
    try:
        with open(path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                fields = line.split('|')
                if len(fields) < 4:
                    continue
                uname, device_id, date, consumption_kwh = fields
                if uname == username:
                    try:
                        consumption = float(consumption_kwh)
                    except ValueError:
                        consumption = 0.0
                    log = {
                        'username': uname,
                        'device_id': int(device_id),
                        'date': date,
                        'consumption_kwh': consumption
                    }
                    logs.append(log)
    except Exception:
        pass
    return logs

# --- Helper function to read activity logs ---
def read_activity_logs(username):
    logs = []
    path = os.path.join(DATA_DIR, 'activity_logs.txt')
    try:
        with open(path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                fields = line.split('|')
                if len(fields) < 5:
                    continue
                uname, timestamp, device_id, action, details = fields
                if uname == username:
                    log = {
                        'username': uname,
                        'timestamp': timestamp,
                        'device_id': int(device_id),
                        'action': action,
                        'details': details
                    }
                    logs.append(log)
    except Exception:
        pass
    return logs

# --- Root redirect to /dashboard ---
@app.route('/', methods=['GET'])
def root_redirect():
    return redirect(url_for('dashboard_page'))

# --- Dashboard page ---
@app.route('/dashboard', methods=['GET'])
def dashboard_page():
    username = LOGGED_IN_USERNAME
    devices = read_devices(username)

    # user_devices: list of dict (each device info)
    user_devices = devices

    # rooms_summary: dict (room_name -> device counts)
    room_counts = {}
    for d in devices:
        room = d['room']
        room_counts.setdefault(room, 0)
        room_counts[room] += 1

    # device_counts: dict ({total:int, active:int, offline:int})
    total = len(devices)
    active = sum(1 for d in devices if d['status'] == 'Online')
    offline = total - active
    device_counts = {'total': total, 'active': active, 'offline': offline}

    return render_template('dashboard.html', user_devices=user_devices, rooms_summary=room_counts, device_counts=device_counts)

# --- Device list page ---
@app.route('/devices', methods=['GET'])
def device_list_page():
    username = LOGGED_IN_USERNAME
    devices = read_devices(username)

    devices_list = []
    for d in devices:
        device = {
            'id': d['device_id'],
            'name': d['device_name'],
            'type': d['device_type'],
            'room': d['room'],
            'status': d['status']
        }
        devices_list.append(device)

    return render_template('device_list.html', devices=devices_list)

# --- Add device page (GET) ---
@app.route('/device/add', methods=['GET'])
def add_device_page():
    device_types = ['Light', 'Thermostat', 'Camera', 'Lock', 'Sensor', 'Appliance']
    rooms = ['Living Room', 'Bedroom', 'Kitchen', 'Bathroom', 'Garage']
    return render_template('add_device.html', device_types=device_types, rooms=rooms)

# --- Add device submit (POST) ---
@app.route('/device/add', methods=['POST'])
def add_device_submit():
    username = LOGGED_IN_USERNAME
    device_name = request.form.get('device_name', '').strip()
    device_type = request.form.get('device_type', '').strip()
    device_room = request.form.get('device_room', '').strip()

    # Basic validation
    if not device_name or not device_type or not device_room:
        # Could ideally flash a message, but spec says no extra
        return redirect(url_for('add_device_page'))

    # Load existing devices
    devices = read_devices(username)

    # Determine a new unique device_id
    max_id = 0
    for d in devices:
        if d['device_id'] > max_id:
            max_id = d['device_id']
    new_device_id = max_id + 1

    # Set default values for other fields (brand, model, status, power, brightness, temperature, mode, schedule_time)
    new_device = {
        'username': username,
        'device_id': new_device_id,
        'device_name': device_name,
        'device_type': device_type,
        'room': device_room,
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
    write_devices(devices, username)

    return redirect(url_for('device_list_page'))

# --- Device control page ---
@app.route('/device/<int:device_id>', methods=['GET'])
def device_control_page(device_id):
    username = LOGGED_IN_USERNAME
    devices = read_devices(username)
    device = None
    for d in devices:
        if d['device_id'] == device_id:
            device = d
            break
    if device is None:
        # Device not found, redirect to device list
        return redirect(url_for('device_list_page'))

    return render_template('device_control.html', device=device)

# --- Device control submit (POST) ---
@app.route('/device/<int:device_id>/control', methods=['POST'])
def device_control_submit(device_id):
    username = LOGGED_IN_USERNAME
    devices = read_devices(username)
    device = None
    device_index = None
    for idx, d in enumerate(devices):
        if d['device_id'] == device_id:
            device = d
            device_index = idx
            break
    if device is None:
        return redirect(url_for('device_list_page'))

    # Expected form data - power toggle, brightness, temperature, mode, schedule_time
    # We proceed to update only fields present
    power = request.form.get('power')  # Expecting 'on' or 'off'
    brightness = request.form.get('brightness', '')
    temperature = request.form.get('temperature', '')
    mode = request.form.get('mode', '')
    schedule_time = request.form.get('schedule_time', '')

    if power in ('on', 'off'):
        device['power'] = power
    device['status'] = 'Online' if device['power'] == 'on' else 'Offline'

    # brightness and temperature might be empty if not applicable
    if brightness.isdigit():
        device['brightness'] = brightness
    else:
        device['brightness'] = ''

    if temperature.isdigit():
        device['temperature'] = temperature
    else:
        device['temperature'] = ''

    # mode may be auto or manual or empty
    device['mode'] = mode

    # schedule_time typically a time string e.g. 22:00
    device['schedule_time'] = schedule_time

    devices[device_index] = device
    write_devices(devices, username)

    return redirect(url_for('device_control_page', device_id=device_id))

# --- Automation rules page (GET) ---
@app.route('/automation', methods=['GET'])
def automation_rules_page():
    username = LOGGED_IN_USERNAME
    rules = read_automation_rules(username)
    devices = read_devices(username)

    # Prepare list of devices for dropdown with id and name
    devices_dropdown = [{'id': d['device_id'], 'name': d['device_name']} for d in devices]

    return render_template('automation.html', automation_rules=rules, devices=devices_dropdown)

# --- Add automation rule (POST) ---
@app.route('/automation', methods=['POST'])
def add_automation_rule():
    username = LOGGED_IN_USERNAME
    rule_name = request.form.get('rule_name', '').strip()
    trigger_type = request.form.get('trigger_type', '').strip()
    trigger_value = request.form.get('trigger_value', '').strip()
    action_device_id = request.form.get('action_device')
    action_type = request.form.get('action_type', '').strip()
    action_value = request.form.get('action_value', '').strip() if 'action_value' in request.form else ''

    # Validate required fields
    if not rule_name or not trigger_type or not trigger_value or not action_device_id or not action_type:
        return redirect(url_for('automation_rules_page'))

    try:
        action_device_id = int(action_device_id)
    except ValueError:
        return redirect(url_for('automation_rules_page'))

    rules = read_automation_rules(username)
    max_id = 0
    for r in rules:
        if r['rule_id'] > max_id:
            max_id = r['rule_id']
    new_rule_id = max_id + 1

    new_rule = {
        'username': username,
        'rule_id': new_rule_id,
        'rule_name': rule_name,
        'trigger_type': trigger_type,
        'trigger_value': trigger_value,
        'action_device_id': action_device_id,
        'action_type': action_type,
        'action_value': action_value,
        'enabled': True
    }

    rules.append(new_rule)
    write_automation_rules(rules, username)

    return redirect(url_for('automation_rules_page'))

# --- Energy report page (GET) ---
@app.route('/energy', methods=['GET'])
def energy_report_page():
    username = LOGGED_IN_USERNAME
    energy_logs = read_energy_logs(username)
    devices = read_devices(username)

    # Calculate total consumption and cost estimate
    # Let's assume cost estimate rate is 0.12 per kWh
    total_consumption = sum(log['consumption_kwh'] for log in energy_logs)
    cost_estimate = total_consumption * 0.12

    energy_summary = {'total_consumption': total_consumption, 'cost_estimate': cost_estimate}

    # energy_logs: list of dict (per device per date), add device_name for convenience
    logs_with_name = []
    device_id_to_name = {d['device_id']: d['device_name'] for d in devices}
    for log in energy_logs:
        logs_with_name.append({
            'device_id': log['device_id'],
            'device_name': device_id_to_name.get(log['device_id'], 'Unknown'),
            'date': log['date'],
            'consumption_kwh': log['consumption_kwh']
        })

    return render_template('energy_report.html', energy_summary=energy_summary, energy_logs=logs_with_name)

# --- Energy filter (POST) ---
@app.route('/energy/filter', methods=['POST'])
def energy_filter():
    filter_date = request.form.get('filter_date', '').strip()
    # Simply redirect to energy page with data filtered by date
    # Because spec says redirect usually, implement filter by saving date in session or pass param (spec doesn't detail)
    # As spec says no additional session or frontend, just redirect to energy page
    # So we ignore filter_date in controller here per spec.
    return redirect(url_for('energy_report_page'))

# --- Activity logs page (GET) ---
@app.route('/activity', methods=['GET'])
def activity_logs_page():
    username = LOGGED_IN_USERNAME
    activity_logs = read_activity_logs(username)

    # Get search query from query param (optional)
    search_query = request.args.get('search_query', '').strip()

    filtered_logs = []
    if search_query:
        # Filter logs by search query in action or details
        for log in activity_logs:
            if search_query.lower() in log['action'].lower() or search_query.lower() in log['details'].lower():
                filtered_logs.append(log)
    else:
        filtered_logs = activity_logs

    return render_template('activity_logs.html', activity_logs=filtered_logs, search_query=search_query)

# --- Activity search (POST) ---
@app.route('/activity/search', methods=['POST'])
def activity_search():
    search_query = request.form.get('search_query', '').strip()
    # Redirect to GET /activity with search_query as param
    if search_query:
        return redirect(url_for('activity_logs_page', search_query=search_query))
    else:
        return redirect(url_for('activity_logs_page'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
