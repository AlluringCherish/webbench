from flask import Flask, render_template, redirect, url_for, request
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

CURRENT_USERNAME = 'john_doe'
DATA_DIR = 'data'

USERS_FILE = os.path.join(DATA_DIR, 'users.txt')
DEVICES_FILE = os.path.join(DATA_DIR, 'devices.txt')
ROOMS_FILE = os.path.join(DATA_DIR, 'rooms.txt')
AUTOMATION_RULES_FILE = os.path.join(DATA_DIR, 'automation_rules.txt')
ENERGY_LOGS_FILE = os.path.join(DATA_DIR, 'energy_logs.txt')
ACTIVITY_LOGS_FILE = os.path.join(DATA_DIR, 'activity_logs.txt')

DEVICE_TYPES = ['Light', 'Thermostat', 'Camera', 'Lock', 'Sensor', 'Appliance']
ROOM_NAMES = ['Living Room', 'Bedroom', 'Kitchen', 'Bathroom', 'Garage']


def safe_int(value, default=None):
    try:
        return int(value)
    except (ValueError, TypeError):
        return default


def safe_float(value, default=None):
    try:
        return float(value)
    except (ValueError, TypeError):
        return default


def safe_bool(value):
    if isinstance(value, str):
        return value.lower() == 'true'
    return False


def load_devices(username):
    devices = []
    try:
        with open(DEVICES_FILE, 'r', encoding='utf-8') as file:
            for line in file:
                fields = line.strip().split('|')
                if len(fields) != 13:
                    continue
                (
                    uname, device_id, device_name, device_type, room, brand, model, status, power, brightness,
                    temperature, mode, schedule_time
                ) = fields
                if uname != username:
                    continue
                devices.append({
                    'username': uname,
                    'device_id': safe_int(device_id),
                    'device_name': device_name,
                    'device_type': device_type,
                    'room': room,
                    'brand': brand,
                    'model': model,
                    'status': status,
                    'power': power,
                    'brightness': safe_int(brightness) if brightness else None,
                    'temperature': safe_int(temperature) if temperature else None,
                    'mode': mode if mode else None,
                    'schedule_time': schedule_time if schedule_time else None
                })
    except FileNotFoundError:
        pass
    return devices


def save_devices(username, devices):
    all_devices = []
    try:
        with open(DEVICES_FILE, 'r', encoding='utf-8') as file:
            for line in file:
                fields = line.strip().split('|')
                if len(fields) != 13:
                    continue
                all_devices.append(fields)
    except FileNotFoundError:
        all_devices = []

    filtered_devices = [d for d in all_devices if d[0] != username]

    for d in devices:
        dev_line = [
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
        ]
        filtered_devices.append(dev_line)

    with open(DEVICES_FILE, 'w', encoding='utf-8') as file:
        for d in filtered_devices:
            file.write('|'.join(d) + '\n')


def load_rooms(username):
    rooms = []
    try:
        with open(ROOMS_FILE, 'r', encoding='utf-8') as file:
            for line in file:
                fields = line.strip().split('|')
                if len(fields) != 3:
                    continue
                uname, room_id, room_name = fields
                if uname != username:
                    continue
                rooms.append({'username': uname, 'room_id': safe_int(room_id), 'room_name': room_name})
    except FileNotFoundError:
        pass
    return rooms


def load_automation_rules(username):
    rules = []
    try:
        with open(AUTOMATION_RULES_FILE, 'r', encoding='utf-8') as file:
            for line in file:
                fields = line.strip().split('|')
                if len(fields) != 9:
                    continue
                (
                    uname, rule_id, rule_name, trigger_type, trigger_value, action_device_id, action_type, action_value, enabled
                ) = fields
                if uname != username:
                    continue
                rules.append({
                    'username': uname,
                    'rule_id': safe_int(rule_id),
                    'rule_name': rule_name,
                    'trigger_type': trigger_type,
                    'trigger_value': trigger_value,
                    'action_device_id': safe_int(action_device_id),
                    'action_type': action_type,
                    'action_value': action_value if action_value else None,
                    'enabled': safe_bool(enabled)
                })
    except FileNotFoundError:
        pass
    return rules


def save_automation_rules(username, rules):
    all_rules = []
    try:
        with open(AUTOMATION_RULES_FILE, 'r', encoding='utf-8') as file:
            for line in file:
                fields = line.strip().split('|')
                if len(fields) != 9:
                    continue
                all_rules.append(fields)
    except FileNotFoundError:
        all_rules = []

    filtered_rules = [r for r in all_rules if r[0] != username]

    for r in rules:
        rule_line = [
            r['username'],
            str(r['rule_id']),
            r['rule_name'],
            r['trigger_type'],
            r['trigger_value'],
            str(r['action_device_id']),
            r['action_type'],
            r['action_value'] if r['action_value'] is not None else '',
            'true' if r['enabled'] else 'false'
        ]
        filtered_rules.append(rule_line)

    with open(AUTOMATION_RULES_FILE, 'w', encoding='utf-8') as file:
        for r in filtered_rules:
            file.write('|'.join(r) + '\n')


def load_energy_logs(username):
    logs = []
    try:
        with open(ENERGY_LOGS_FILE, 'r', encoding='utf-8') as file:
            for line in file:
                fields = line.strip().split('|')
                if len(fields) != 4:
                    continue
                uname, device_id, date, consumption_kwh = fields
                if uname != username:
                    continue
                logs.append({
                    'username': uname,
                    'device_id': safe_int(device_id),
                    'date': date,
                    'consumption_kwh': safe_float(consumption_kwh)
                })
    except FileNotFoundError:
        pass
    return logs


def load_activity_logs(username):
    logs = []
    try:
        with open(ACTIVITY_LOGS_FILE, 'r', encoding='utf-8') as file:
            for line in file:
                fields = line.strip().split('|')
                if len(fields) != 5:
                    continue
                uname, timestamp, device_id, action, details = fields
                if uname != username:
                    continue
                logs.append({
                    'username': uname,
                    'timestamp': timestamp,
                    'device_id': safe_int(device_id),
                    'action': action,
                    'details': details
                })
    except FileNotFoundError:
        pass
    return logs


def get_next_id(items, id_key):
    if not items:
        return 1
    max_id = max(item[id_key] or 0 for item in items)
    return max_id + 1


def find_device(devices, device_id):
    for d in devices:
        if d['device_id'] == device_id:
            return d
    return None


@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    devices = load_devices(CURRENT_USERNAME)
    rooms = load_rooms(CURRENT_USERNAME)

    total_devices = len(devices)
    active_devices = sum(1 for d in devices if d['status'] == 'Online')
    offline_devices = total_devices - active_devices

    room_list = []
    for room in rooms:
        count = sum(1 for d in devices if d['room'] == room['room_name'])
        room_list.append({'room_name': room['room_name'], 'device_count': count})

    devices_summary = {
        'total_devices': total_devices,
        'active_devices': active_devices,
        'offline_devices': offline_devices
    }

    return render_template('dashboard.html', devices_summary=devices_summary, rooms=room_list)


@app.route('/devices')
def device_list():
    devices = load_devices(CURRENT_USERNAME)
    return render_template('devices.html', devices=devices)


@app.route('/device/add', methods=['GET', 'POST'])
def add_device():
    if request.method == 'GET':
        rooms_objs = load_rooms(CURRENT_USERNAME)
        rooms = [r['room_name'] for r in rooms_objs]
        if not rooms:
            rooms = ROOM_NAMES
        device_types = DEVICE_TYPES
        return render_template('add_device.html', rooms=rooms, device_types=device_types)

    # POST
    device_name = request.form.get('device_name', '').strip()
    device_type = request.form.get('device_type', '').strip()
    device_room = request.form.get('device_room', '').strip()

    if not device_name or not device_type or not device_room:
        rooms_objs = load_rooms(CURRENT_USERNAME)
        rooms = [r['room_name'] for r in rooms_objs]
        if not rooms:
            rooms = ROOM_NAMES
        device_types = DEVICE_TYPES
        return render_template('add_device.html', rooms=rooms, device_types=device_types)

    devices = load_devices(CURRENT_USERNAME)
    next_id = get_next_id(devices, 'device_id')

    new_device = {
        'username': CURRENT_USERNAME,
        'device_id': next_id,
        'device_name': device_name,
        'device_type': device_type,
        'room': device_room,
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
    save_devices(CURRENT_USERNAME, devices)
    return redirect(url_for('device_list'))


@app.route('/device/<int:device_id>', methods=['GET', 'POST'])
def device_control(device_id):
    devices = load_devices(CURRENT_USERNAME)
    device = find_device(devices, device_id)
    if not device:
        return "Device not found", 404

    if request.method == 'GET':
        return render_template('device_control.html', device=device)

    # POST update
    power = request.form.get('power', device['power']).strip().lower()
    brightness_raw = request.form.get('brightness', '').strip()
    temperature_raw = request.form.get('temperature', '').strip()
    mode = request.form.get('mode', '').strip() or None
    schedule_time = request.form.get('schedule_time', '').strip() or None

    brightness = safe_int(brightness_raw) if brightness_raw else None
    temperature = safe_int(temperature_raw) if temperature_raw else None

    device['power'] = 'on' if power == 'on' else 'off'
    device['brightness'] = brightness
    device['temperature'] = temperature
    device['mode'] = mode
    device['schedule_time'] = schedule_time

    device['status'] = 'Online' if device['power'] == 'on' else 'Offline'

    save_devices(CURRENT_USERNAME, devices)
    return redirect(url_for('device_control', device_id=device_id))


@app.route('/automation', methods=['GET', 'POST'])
def automation_rules():
    if request.method == 'GET':
        rules = load_automation_rules(CURRENT_USERNAME)
        devices = load_devices(CURRENT_USERNAME)
        return render_template('automation.html', automation_rules=rules, devices=devices)

    rule_name = request.form.get('rule_name', '').strip()
    trigger_type = request.form.get('trigger_type', '').strip()
    trigger_value = request.form.get('trigger_value', '').strip()
    action_device_str = request.form.get('action_device', '').strip()
    action_type = request.form.get('action_type', '').strip()

    if not rule_name or not trigger_type or not action_device_str or not action_type:
        return redirect(url_for('automation_rules'))

    try:
        action_device_id = int(action_device_str)
    except ValueError:
        return redirect(url_for('automation_rules'))

    rules = load_automation_rules(CURRENT_USERNAME)
    next_id = get_next_id(rules, 'rule_id')

    new_rule = {
        'username': CURRENT_USERNAME,
        'rule_id': next_id,
        'rule_name': rule_name,
        'trigger_type': trigger_type,
        'trigger_value': trigger_value,
        'action_device_id': action_device_id,
        'action_type': action_type,
        'action_value': None,
        'enabled': True
    }
    rules.append(new_rule)
    save_automation_rules(CURRENT_USERNAME, rules)
    return redirect(url_for('automation_rules'))


@app.route('/energy', methods=['GET', 'POST'])
def energy_report():
    filter_date = None
    if request.method == 'POST':
        filter_date = request.form.get('date_filter', '').strip()
        if filter_date == '':
            filter_date = None

    energy_data_all = load_energy_logs(CURRENT_USERNAME)
    energy_data = [e for e in energy_data_all if filter_date is None or e['date'] == filter_date]

    total_consumption = sum(e['consumption_kwh'] for e in energy_data if e['consumption_kwh'] is not None)
    energy_summary = {'total_consumption': total_consumption, 'cost_estimate': round(total_consumption * 0.12, 2)}

    return render_template('energy.html', energy_data=energy_data, energy_summary=energy_summary, filter_date=filter_date)


@app.route('/activity', methods=['GET', 'POST'])
def activity_logs():
    search_query = None
    all_logs = load_activity_logs(CURRENT_USERNAME)

    if request.method == 'POST':
        search_query = request.form.get('search_query', '').strip().lower()
        if search_query:
            filtered_logs = []
            for log in all_logs:
                if (search_query in log['timestamp'].lower() or
                    search_query in str(log['device_id']) or
                    search_query in log['action'].lower() or
                    search_query in log['details'].lower()):
                    filtered_logs.append(log)
            activity_logs_to_display = filtered_logs
        else:
            activity_logs_to_display = all_logs
    else:
        activity_logs_to_display = all_logs

    return render_template('activity.html', activity_logs=activity_logs_to_display, search_query=search_query)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
