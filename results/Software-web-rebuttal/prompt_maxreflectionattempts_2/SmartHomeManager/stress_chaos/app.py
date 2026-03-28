from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

# -------- Helpers to load and save data ----------
import os

DATA_DIR = 'data'

# Use a hardcoded user for demo context
CURRENT_USER = 'john_doe'

# --- Users ---
def load_users():
    users = []
    try:
        with open(os.path.join(DATA_DIR, 'users.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                username, email = line.split('|')
                users.append({'username': username, 'email': email})
    except FileNotFoundError:
        pass
    return users

# --- Devices ---
def load_devices(username=None):
    devices = []
    try:
        with open(os.path.join(DATA_DIR, 'devices.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                fields = line.split('|')
                if len(fields) < 13:
                    continue
                (
                    u_name, device_id_str, device_name, device_type, room, brand, model,
                    status, power, brightness_str, temperature_str, mode, schedule_time
                ) = fields
                if username and u_name != username:
                    continue
                device = {
                    'username': u_name,
                    'device_id': int(device_id_str),
                    'device_name': device_name,
                    'device_type': device_type,
                    'room': room,
                    'brand': brand,
                    'model': model,
                    'status': status,
                    'power': power,
                    'brightness': int(brightness_str) if brightness_str.isdigit() else None,
                    'temperature': int(temperature_str) if temperature_str.isdigit() else None,
                    'mode': mode,
                    'schedule_time': schedule_time
                }
                devices.append(device)
    except FileNotFoundError:
        pass
    return devices

def save_devices(devices):
    # devices is a list of dict for current user only
    lines = []
    try:
        all_devices = []
        filepath = os.path.join(DATA_DIR, 'devices.txt')
        # Load all devices (including others)
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                fields = line.split('|')
                if len(fields) < 13:
                    continue
                u_name = fields[0]
                if u_name != CURRENT_USER:
                    all_devices.append(line)  # keep others intact
    except FileNotFoundError:
        all_devices = []
    # Add current user's devices
    for d in devices:
        brightness = str(d['brightness']) if d['brightness'] is not None else ''
        temperature = str(d['temperature']) if d['temperature'] is not None else ''
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
            brightness,
            temperature,
            d['mode'],
            d['schedule_time']
        ])
        all_devices.append(line)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(all_devices) + ('\n' if all_devices else ''))

# --- Rooms ---
def load_rooms(username=None):
    rooms = []
    try:
        with open(os.path.join(DATA_DIR, 'rooms.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                u_name, room_id_str, room_name = line.split('|')
                if username and u_name != username:
                    continue
                rooms.append({'username': u_name, 'room_id': int(room_id_str), 'room_name': room_name})
    except FileNotFoundError:
        pass
    return rooms

# --- Automation Rules ---
def load_automation_rules(username=None):
    rules = []
    try:
        with open(os.path.join(DATA_DIR, 'automation_rules.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                fields = line.split('|')
                if len(fields) < 9:
                    continue
                (
                    u_name, rule_id_str, rule_name, trigger_type, trigger_value, action_device_id_str,
                    action_type, action_value, enabled_str
                ) = fields
                if username and u_name != username:
                    continue
                rule = {
                    'username': u_name,
                    'rule_id': int(rule_id_str),
                    'rule_name': rule_name,
                    'trigger_type': trigger_type,
                    'trigger_value': trigger_value,
                    'action_device_id': int(action_device_id_str),
                    'action_type': action_type,
                    'action_value': action_value,
                    'enabled': True if enabled_str.lower() == 'true' else False
                }
                rules.append(rule)
    except FileNotFoundError:
        pass
    return rules

def save_automation_rules(rules):
    lines = []
    try:
        all_rules = []
        filepath = os.path.join(DATA_DIR, 'automation_rules.txt')
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                fields = line.split('|')
                u_name = fields[0]
                if u_name != CURRENT_USER:
                    all_rules.append(line)
    except FileNotFoundError:
        all_rules = []
    for r in rules:
        enabled_str = 'true' if r['enabled'] else 'false'
        line = '|'.join([
            r['username'],
            str(r['rule_id']),
            r['rule_name'],
            r['trigger_type'],
            r['trigger_value'],
            str(r['action_device_id']),
            r['action_type'],
            r['action_value'],
            enabled_str
        ])
        all_rules.append(line)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(all_rules) + ('\n' if all_rules else ''))

# --- Energy Logs ---
def load_energy_logs(username=None):
    logs = []
    try:
        with open(os.path.join(DATA_DIR, 'energy_logs.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                username_l, device_id_str, date, consumption_kwh_str = line.split('|')
                if username and username_l != username:
                    continue
                logs.append({
                    'username': username_l,
                    'device_id': int(device_id_str),
                    'date': date,
                    'consumption_kwh': float(consumption_kwh_str)
                })
    except FileNotFoundError:
        pass
    return logs

# --- Activity Logs ---
def load_activity_logs(username=None):
    logs = []
    try:
        with open(os.path.join(DATA_DIR, 'activity_logs.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                username_l, timestamp, device_id_str, action, details = line.split('|')
                if username and username_l != username:
                    continue
                logs.append({
                    'username': username_l,
                    'timestamp': timestamp,
                    'device_id': int(device_id_str),
                    'action': action,
                    'details': details
                })
    except FileNotFoundError:
        pass
    return logs

# --- Misc helpers ---
def get_next_device_id(devices):
    if not devices:
        return 1
    return max(d['device_id'] for d in devices) + 1

def get_next_rule_id(rules):
    if not rules:
        return 1
    return max(r['rule_id'] for r in rules) + 1

# --- Device types ---
# Extracted from devices.txt device_type fields known or fixed enum
# Since no explicit list given, infer from loaded devices
# But we provide a fallback list if none found
FALLBACK_DEVICE_TYPES = ['Light', 'Thermostat', 'Camera', 'Sensor', 'Switch', 'Plug']

def get_device_types(username):
    devices = load_devices(username)
    types = set(d['device_type'] for d in devices)
    if types:
        return sorted(types)
    return FALLBACK_DEVICE_TYPES


# -------- Routes ----------

@app.route('/')
def redirect_to_dashboard():
    return redirect(url_for('dashboard_page'))


@app.route('/dashboard')
def dashboard_page():
    # Aggregate device counts
    devices = load_devices(CURRENT_USER)
    total = len(devices)
    active = sum(1 for d in devices if d['status'].lower() == 'online')
    offline = total - active

    device_counts = {
        'total': total,
        'active': active,
        'offline': offline
    }
    rooms = [room['room_name'] for room in load_rooms(CURRENT_USER)]
    user = CURRENT_USER
    return render_template('dashboard.html', device_counts=device_counts, rooms=rooms, user=user)


@app.route('/devices')
def list_devices():
    devices = load_devices(CURRENT_USER)
    user = CURRENT_USER
    return render_template('devices/list.html', devices=devices, user=user)


@app.route('/devices/add', methods=['GET', 'POST'])
def add_device():
    user = CURRENT_USER
    rooms = [room['room_name'] for room in load_rooms(user)]
    device_types = get_device_types(user)

    if request.method == 'POST':
        device_name = request.form.get('device_name', '').strip()
        device_type = request.form.get('device_type', '').strip()
        device_room = request.form.get('device_room', '').strip()

        if not device_name or not device_type or not device_room:
            # For simplicity, just render page again with current data
            return render_template('devices/add.html', rooms=rooms, device_types=device_types, user=user)

        devices = load_devices(user)
        new_id = get_next_device_id(devices)

        # Create new device with minimal default values
        new_device = {
            'username': user,
            'device_id': new_id,
            'device_name': device_name,
            'device_type': device_type,
            'room': device_room,
            'brand': '',
            'model': '',
            'status': 'Offline',
            'power': 'off',
            'brightness': None,
            'temperature': None,
            'mode': '',
            'schedule_time': ''
        }
        devices.append(new_device)
        save_devices(devices)

        return redirect(url_for('list_devices'))

    return render_template('devices/add.html', rooms=rooms, device_types=device_types, user=user)


@app.route('/devices/<int:device_id>', methods=['GET', 'POST'])
def control_device(device_id):
    user = CURRENT_USER
    devices = load_devices(user)
    device = None
    for d in devices:
        if d['device_id'] == device_id:
            device = d
            break
    if device is None:
        # Device not found, redirect to devices page
        return redirect(url_for('list_devices'))

    if request.method == 'POST':
        # Possible updates: power toggle, brightness, temperature, mode, schedule_time
        # We'll update fields safely if present

        power = request.form.get('power')
        if power in ['on', 'off']:
            device['power'] = power
            device['status'] = 'Online' if power == 'on' else 'Offline'

        brightness_str = request.form.get('brightness')
        if brightness_str and brightness_str.isdigit():
            device['brightness'] = int(brightness_str)

        temperature_str = request.form.get('temperature')
        if temperature_str and temperature_str.isdigit():
            device['temperature'] = int(temperature_str)

        mode = request.form.get('mode')
        if mode is not None:
            device['mode'] = mode

        schedule_time = request.form.get('schedule_time')
        if schedule_time is not None:
            device['schedule_time'] = schedule_time

        # Save changes
        save_devices(devices)

        return redirect(url_for('control_device', device_id=device_id))

    return render_template('devices/control.html', device=device, user=user)


@app.route('/automation', methods=['GET', 'POST'])
def automation_page():
    user = CURRENT_USER
    rules = load_automation_rules(user)
    devices = load_devices(user)

    if request.method == 'POST':
        # Add a new rule
        rule_name = request.form.get('rule_name', '').strip()
        trigger_type = request.form.get('trigger_type', '').strip()
        trigger_value = request.form.get('trigger_value', '').strip()
        action_device_id_str = request.form.get('action_device')
        action_type = request.form.get('action_type', '').strip()

        if not rule_name or not trigger_type or not action_type or not action_device_id_str:
            return render_template('automation.html', rules=rules, devices=devices, user=user)
        try:
            action_device_id = int(action_device_id_str)
        except ValueError:
            return render_template('automation.html', rules=rules, devices=devices, user=user)

        new_rule_id = get_next_rule_id(rules)

        new_rule = {
            'username': user,
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

        return redirect(url_for('automation_page'))

    return render_template('automation.html', rules=rules, devices=devices, user=user)


@app.route('/reports')
def reports_page():
    user = CURRENT_USER
    energy_logs = load_energy_logs(user)
    devices = load_devices(user)

    # Summarize energy consumption
    energy_summary = {}
    for log in energy_logs:
        device_id = log['device_id']
        energy_summary[device_id] = energy_summary.get(device_id, 0) + log['consumption_kwh']

    return render_template('reports.html', energy_summary=energy_summary, energy_logs=energy_logs, user=user)


@app.route('/activity')
def activity_page():
    user = CURRENT_USER
    activities = load_activity_logs(user)
    return render_template('activity.html', activities=activities, user=user)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
