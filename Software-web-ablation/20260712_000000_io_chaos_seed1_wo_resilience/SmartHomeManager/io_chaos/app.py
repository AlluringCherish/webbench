from flask import Flask, render_template, redirect, url_for, request
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

# Define current user for demo purposes
CURRENT_USER = 'john_doe'

DATA_DIR = 'data'

# Utility functions for reading data files

def read_devices(username):
    devices = []
    devices_path = os.path.join(DATA_DIR, 'devices.txt')
    if os.path.exists(devices_path):
        with open(devices_path, 'r', encoding='utf-8') as f:
            for line in f:
                if not line.strip():
                    continue
                fields = line.strip().split('|')
                if len(fields) < 13:
                    continue
                user, device_id, device_name, device_type, room, brand, model, status, power, brightness, temperature, mode, schedule_time = fields
                if user != username:
                    continue
                brightness_val = int(brightness) if brightness.isdigit() else None
                temperature_val = int(temperature) if temperature.isdigit() else None
                devices.append({
                    'device_id': int(device_id),
                    'device_name': device_name,
                    'device_type': device_type,
                    'room': room,
                    'brand': brand,
                    'model': model,
                    'status': status,
                    'power': power,
                    'brightness': brightness_val,
                    'temperature': temperature_val,
                    'mode': mode,
                    'schedule_time': schedule_time
                })
    return devices

def write_devices(username, devices):
    devices_path = os.path.join(DATA_DIR, 'devices.txt')
    all_lines = []
    # Read all devices to retain other users
    if os.path.exists(devices_path):
        with open(devices_path, 'r', encoding='utf-8') as f:
            for line in f:
                if not line.strip():
                    continue
                fields = line.strip().split('|')
                user = fields[0]
                if user != username:
                    all_lines.append(line.strip())
    # Add current user's devices
    for d in devices:
        brightness_str = str(d['brightness']) if d['brightness'] is not None else ''
        temperature_str = str(d['temperature']) if d['temperature'] is not None else ''
        line = '|'.join([
            username,
            str(d['device_id']),
            d['device_name'],
            d['device_type'],
            d['room'],
            d.get('brand', ''),
            d.get('model', ''),
            d['status'],
            d['power'],
            brightness_str,
            temperature_str,
            d['mode'],
            d['schedule_time']
        ])
        all_lines.append(line)
    with open(devices_path, 'w', encoding='utf-8') as f:
        for line in all_lines:
            f.write(line + '\n')


def read_rooms(username):
    rooms_path = os.path.join(DATA_DIR, 'rooms.txt')
    rooms = []
    if os.path.exists(rooms_path):
        with open(rooms_path, 'r', encoding='utf-8') as f:
            for line in f:
                if not line.strip():
                    continue
                fields = line.strip().split('|')
                if len(fields) < 3:
                    continue
                user, room_id, room_name = fields
                if user != username:
                    continue
                rooms.append({'room_id': int(room_id), 'room_name': room_name})
    return rooms


def read_automation_rules(username):
    rules = []
    rules_path = os.path.join(DATA_DIR, 'automation_rules.txt')
    if os.path.exists(rules_path):
        with open(rules_path, 'r', encoding='utf-8') as f:
            for line in f:
                if not line.strip():
                    continue
                fields = line.strip().split('|')
                if len(fields) < 9:
                    continue
                user, rule_id, rule_name, trigger_type, trigger_value, action_device_id, action_type, action_value, enabled = fields
                if user != username:
                    continue
                rules.append({
                    'rule_id': int(rule_id),
                    'rule_name': rule_name,
                    'trigger_type': trigger_type,
                    'trigger_value': trigger_value,
                    'action_device_id': int(action_device_id),
                    'action_type': action_type,
                    'action_value': action_value if action_value != '' else None,
                    'enabled': enabled.lower() == 'true'
                })
    return rules


def write_automation_rules(username, rules):
    rules_path = os.path.join(DATA_DIR, 'automation_rules.txt')
    all_lines = []
    if os.path.exists(rules_path):
        with open(rules_path, 'r', encoding='utf-8') as f:
            for line in f:
                if not line.strip():
                    continue
                fields = line.strip().split('|')
                user = fields[0]
                if user != username:
                    all_lines.append(line.strip())
    # Add current user's rules
    for r in rules:
        enabled_str = 'true' if r['enabled'] else 'false'
        action_value_str = r['action_value'] if r['action_value'] is not None else ''
        line = '|'.join([
            username,
            str(r['rule_id']),
            r['rule_name'],
            r['trigger_type'],
            r['trigger_value'],
            str(r['action_device_id']),
            r['action_type'],
            action_value_str,
            enabled_str
        ])
        all_lines.append(line)
    with open(rules_path, 'w', encoding='utf-8') as f:
        for line in all_lines:
            f.write(line + '\n')


def read_energy_logs(username):
    energy_path = os.path.join(DATA_DIR, 'energy_logs.txt')
    energy_data = []
    if os.path.exists(energy_path):
        with open(energy_path, 'r', encoding='utf-8') as f:
            for line in f:
                if not line.strip():
                    continue
                fields = line.strip().split('|')
                if len(fields) < 4:
                    continue
                user, device_id, date, consumption_kwh = fields
                if user != username:
                    continue
                energy_data.append({
                    'device_id': int(device_id),
                    'date': date,
                    'consumption_kwh': float(consumption_kwh)
                })
    return energy_data


def read_activity_logs(username):
    activity_path = os.path.join(DATA_DIR, 'activity_logs.txt')
    activities = []
    if os.path.exists(activity_path):
        with open(activity_path, 'r', encoding='utf-8') as f:
            for line in f:
                if not line.strip():
                    continue
                fields = line.strip().split('|')
                if len(fields) < 5:
                    continue
                user, timestamp, device_id, action, details = fields
                if user != username:
                    continue
                activities.append({
                    'timestamp': timestamp,
                    'device_id': int(device_id),
                    'action': action,
                    'details': details
                })
    return activities

# Routes

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    devices = read_devices(CURRENT_USER)
    # Summary counts
    total = len(devices)
    active = sum(1 for d in devices if d['status'].lower() == 'online')
    offline = total - active

    # Rooms with device counts
    rooms = read_rooms(CURRENT_USER)
    room_device_counts = []
    for room in rooms:
        count = sum(1 for d in devices if d['room'] == room['room_name'])
        room_device_counts.append({'room_name': room['room_name'], 'device_count': count})

    devices_summary = {'total': total, 'active': active, 'offline': offline}
    return render_template('dashboard.html', devices_summary=devices_summary, rooms=room_device_counts)

@app.route('/devices')
def device_list():
    devices = read_devices(CURRENT_USER)
    # Provide devices list with required fields
    device_list_view = []
    for d in devices:
        device_list_view.append({
            'device_id': d['device_id'],
            'device_name': d['device_name'],
            'device_type': d['device_type'],
            'room': d['room'],
            'status': d['status']
        })
    return render_template('devices.html', devices=device_list_view)

@app.route('/device/add', methods=['GET', 'POST'])
def add_device():
    device_types = ['Light', 'Thermostat', 'Camera', 'Lock', 'Sensor', 'Appliance']
    rooms = [r['room_name'] for r in read_rooms(CURRENT_USER)]
    error = None
    if request.method == 'POST':
        device_name = request.form.get('device_name', '').strip()
        device_type = request.form.get('device_type', '').strip()
        device_room = request.form.get('device_room', '').strip()

        if not device_name:
            error = 'Device name is required.'
        elif device_type not in device_types:
            error = 'Invalid device type.'
        elif device_room not in rooms:
            error = 'Invalid room selected.'

        if error is None:
            devices = read_devices(CURRENT_USER)
            max_id = max((d['device_id'] for d in devices), default=0)
            new_device_id = max_id + 1
            # Add new device with default fields
            new_device = {
                'device_id': new_device_id,
                'device_name': device_name,
                'device_type': device_type,
                'room': device_room,
                'brand': '',
                'model': '',
                'status': 'Offline',
                'power': 'off',
                'brightness': None,
                'temperature': None,
                'mode': 'Manual',
                'schedule_time': ''
            }
            devices.append(new_device)
            write_devices(CURRENT_USER, devices)
            return redirect(url_for('device_list'))

    return render_template('add_device.html', device_types=device_types, rooms=rooms, error=error)

@app.route('/device/<int:device_id>', methods=['GET', 'POST'])
def device_control(device_id):
    devices = read_devices(CURRENT_USER)
    device = next((d for d in devices if d['device_id'] == device_id), None)
    if device is None:
        return "Device not found", 404

    error = None
    if request.method == 'POST':
        # Handle updates: status, power, brightness, temperature, mode, schedule_time
        power = request.form.get('power', device['power'])
        brightness = request.form.get('brightness')
        temperature = request.form.get('temperature')
        mode = request.form.get('mode', device['mode'])
        schedule_time = request.form.get('schedule_time', device['schedule_time'])

        # Validate brightness and temperature if applicable
        brightness_val = None
        if brightness:
            try:
                brightness_val = int(brightness)
                if brightness_val < 0 or brightness_val > 100:
                    error = 'Brightness must be between 0 and 100'
            except ValueError:
                error = 'Brightness must be an integer'

        temperature_val = None
        if temperature:
            try:
                temperature_val = int(temperature)
            except ValueError:
                error = 'Temperature must be an integer'

        if error is None:
            device['power'] = power
            device['brightness'] = brightness_val
            device['temperature'] = temperature_val
            device['mode'] = mode
            device['schedule_time'] = schedule_time
            write_devices(CURRENT_USER, devices)
            # reload device data to reflect changes
            device = next((d for d in devices if d['device_id'] == device_id), None)

    # Prepare context device dict with required fields
    context_device = {
        'device_id': device['device_id'],
        'device_name': device['device_name'],
        'status': device['status'],
        'power': device['power'],
        'brightness': device['brightness'],
        'temperature': device['temperature'],
        'mode': device['mode'],
        'schedule_time': device['schedule_time']
    }
    return render_template('device_control.html', device=context_device, error=error)

@app.route('/automation', methods=['GET', 'POST'])
def automation_rules():
    rules = read_automation_rules(CURRENT_USER)
    devices = read_devices(CURRENT_USER)
    device_ids = [d['device_id'] for d in devices]
    error = None
    if request.method == 'POST':
        rule_name = request.form.get('rule_name', '').strip()
        trigger_type = request.form.get('trigger_type', '').strip()
        trigger_value = request.form.get('trigger_value', '').strip()
        action_device_id_str = request.form.get('action_device', '').strip()
        action_type = request.form.get('action_type', '').strip()

        # Validate action_device_id
        try:
            action_device_id = int(action_device_id_str)
        except ValueError:
            error = 'Invalid device selected for action.'
            action_device_id = None

        if not rule_name:
            error = 'Rule name is required.'
        elif trigger_type not in ['Time', 'Motion', 'Temperature']:
            error = 'Invalid trigger type.'
        elif not trigger_value:
            error = 'Trigger value is required.'
        elif action_device_id not in device_ids:
            error = 'Invalid device selected for action.'
        elif action_type not in ['Turn On', 'Turn Off', 'Set Brightness', 'Set Temperature']:
            error = 'Invalid action type.'

        if error is None:
            max_rule_id = max((r['rule_id'] for r in rules), default=0)
            new_rule_id = max_rule_id + 1
            new_rule = {
                'rule_id': new_rule_id,
                'rule_name': rule_name,
                'trigger_type': trigger_type,
                'trigger_value': trigger_value,
                'action_device_id': action_device_id,
                'action_type': action_type,
                'action_value': None,
                'enabled': True
            }
            rules.append(new_rule)
            write_automation_rules(CURRENT_USER, rules)
            return redirect(url_for('automation_rules'))

    return render_template('automation.html', automation_rules=rules, devices=devices, error=error)

@app.route('/energy', methods=['GET', 'POST'])
def energy_report():
    energy_data = read_energy_logs(CURRENT_USER)
    devices = read_devices(CURRENT_USER)
    # Map device_id to name
    device_map = {d['device_id']: d['device_name'] for d in devices}

    filter_date = None
    if request.method == 'POST':
        filter_date = request.form.get('date', None)

    filtered_energy_data = []
    total_consumption_val = 0.0
    for e in energy_data:
        if filter_date and e['date'] != filter_date:
            continue
        d_name = device_map.get(e['device_id'], 'Unknown')
        filtered_energy_data.append({
            'device_id': e['device_id'],
            'device_name': d_name,
            'date': e['date'],
            'consumption_kwh': e['consumption_kwh']
        })
        total_consumption_val += e['consumption_kwh']

    # Assume cost per kWh (for example) is 0.12
    estimated_cost_val = total_consumption_val * 0.12

    return render_template('energy.html', energy_data=filtered_energy_data, total_consumption=total_consumption_val, estimated_cost=estimated_cost_val)

@app.route('/activity', methods=['GET', 'POST'])
def activity_logs():
    activities = read_activity_logs(CURRENT_USER)
    devices = read_devices(CURRENT_USER)
    device_map = {d['device_id']: d['device_name'] for d in devices}

    filtered_activities = []
    search_term = None

    if request.method == 'POST':
        search_term = request.form.get('search', '').strip().lower()

    for a in activities:
        if search_term:
            if (search_term not in a['action'].lower() and
                search_term not in a['details'].lower() and
                search_term not in device_map.get(a['device_id'], '').lower()):
                continue
        filtered_activities.append({
            'timestamp': a['timestamp'],
            'device_id': a['device_id'],
            'device_name': device_map.get(a['device_id'], 'Unknown'),
            'action': a['action'],
            'details': a['details']
        })

    return render_template('activity_logs.html', activities=filtered_activities)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
