from flask import Flask, render_template, redirect, url_for, request
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# --- Utility functions for data loading and saving --- #

def load_users():
    users = {}
    path = os.path.join(DATA_DIR, 'users.txt')
    try:
        with open(path, 'r') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                username, email = line.split('|')
                users[username] = {'username': username, 'email': email}
    except FileNotFoundError:
        pass
    return users


def load_devices(username=None):
    devices = []
    path = os.path.join(DATA_DIR, 'devices.txt')
    try:
        with open(path, 'r') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                # 13 fields expected
                (dev_username, device_id, device_name, device_type, room, brand, model, status, power, brightness,
                 temperature, mode, schedule_time) = parts
                if username and dev_username != username:
                    continue
                brightness_int = int(brightness) if brightness.isdigit() else None
                temperature_int = int(temperature) if temperature.isdigit() else None
                device = {
                    'username': dev_username,
                    'device_id': int(device_id),
                    'device_name': device_name,
                    'device_type': device_type,
                    'room': room,
                    'brand': brand,
                    'model': model,
                    'status': status,
                    'power': power,
                    'brightness': brightness_int,
                    'temperature': temperature_int,
                    'mode': mode,
                    'schedule_time': schedule_time
                }
                devices.append(device)
    except FileNotFoundError:
        pass
    return devices


def save_devices(devices):
    path = os.path.join(DATA_DIR, 'devices.txt')
    lines = []
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
        lines.append(line)
    with open(path, 'w') as f:
        f.write('\n'.join(lines))


def load_rooms(username=None):
    rooms = []
    path = os.path.join(DATA_DIR, 'rooms.txt')
    try:
        with open(path, 'r') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                room_username, room_id, room_name = parts
                if username and room_username != username:
                    continue
                room = {
                    'username': room_username,
                    'room_id': int(room_id),
                    'room_name': room_name
                }
                rooms.append(room)
    except FileNotFoundError:
        pass
    return rooms


def save_automation_rules(rules):
    path = os.path.join(DATA_DIR, 'automation_rules.txt')
    lines = []
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
        lines.append(line)
    with open(path, 'w') as f:
        f.write('\n'.join(lines))


def load_automation_rules(username=None):
    rules = []
    path = os.path.join(DATA_DIR, 'automation_rules.txt')
    try:
        with open(path, 'r') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                (rule_username, rule_id, rule_name, trigger_type, trigger_value, action_device_id,
                 action_type, action_value, enabled) = parts
                if username and rule_username != username:
                    continue
                rule = {
                    'username': rule_username,
                    'rule_id': int(rule_id),
                    'rule_name': rule_name,
                    'trigger_type': trigger_type,
                    'trigger_value': trigger_value,
                    'action_device_id': int(action_device_id),
                    'action_type': action_type,
                    'action_value': action_value,
                    'enabled': (enabled.lower() == 'true')
                }
                rules.append(rule)
    except FileNotFoundError:
        pass
    return rules


def load_energy_logs(username=None):
    energy_data = []
    path = os.path.join(DATA_DIR, 'energy_logs.txt')
    try:
        with open(path, 'r') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                (log_username, device_id, date, consumption_kwh) = line.split('|')
                if username and log_username != username:
                    continue
                energy = {
                    'username': log_username,
                    'device_id': int(device_id),
                    'date': date,
                    'consumption_kwh': float(consumption_kwh)
                }
                energy_data.append(energy)
    except FileNotFoundError:
        pass
    return energy_data


def load_activity_logs(username=None):
    activities = []
    path = os.path.join(DATA_DIR, 'activity_logs.txt')
    try:
        with open(path, 'r') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                (log_username, timestamp, device_id, action, details) = line.split('|')
                if username and log_username != username:
                    continue
                activity = {
                    'username': log_username,
                    'timestamp': timestamp,
                    'device_id': int(device_id),
                    'action': action,
                    'details': details
                }
                activities.append(activity)
    except FileNotFoundError:
        pass
    return activities


# For this app and given no user auth detail, assume a default user for demo
DEFAULT_USER = 'john_doe'

# --- Routes --- #

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    # Load devices and rooms for DEFAULT_USER
    devices = load_devices(username=DEFAULT_USER)
    rooms = load_rooms(username=DEFAULT_USER)

    # Compute devices summary
    total_devices = len(devices)
    active_devices = sum(1 for d in devices if d['status'].lower() == 'online')
    offline_devices = total_devices - active_devices
    devices_summary = {
        'total_devices': total_devices,
        'active_devices': active_devices,
        'offline_devices': offline_devices
    }

    # Compute rooms summary with device counts
    room_counts = {}
    for room in rooms:
        room_counts[room['room_name']] = 0
    for d in devices:
        if d['room'] in room_counts:
            room_counts[d['room']] += 1

    rooms_summary = room_counts

    return render_template('dashboard.html', devices_summary=devices_summary, rooms_summary=rooms_summary)


@app.route('/devices')
def device_list():
    devices = load_devices(username=DEFAULT_USER)
    user = DEFAULT_USER
    return render_template('device_list.html', devices=devices, user=user)


@app.route('/devices/<int:device_id>', methods=['GET', 'POST'])
def device_control(device_id):
    devices = load_devices(username=DEFAULT_USER)
    device = next((d for d in devices if d['device_id'] == device_id), None)
    if not device:
        return "Device not found", 404

    if request.method == 'POST':
        # Handle power toggle and save settings
        # Form keys might be power_toggle or save_settings; process accordingly

        # Toggle power
        if 'power_toggle' in request.form:
            device['power'] = 'off' if device['power'] == 'on' else 'on'
            # Optionally update status if needed (not specified)

        # Save settings (brightness, temperature, mode, schedule_time)
        if 'save_settings' in request.form:
            # brightness
            brightness_str = request.form.get('brightness', '').strip()
            if brightness_str.isdigit():
                brightness_val = int(brightness_str)
                brightness_val = max(0, min(100, brightness_val))
                device['brightness'] = brightness_val
            else:
                device['brightness'] = None

            # temperature
            temperature_str = request.form.get('temperature', '').strip()
            if temperature_str.isdigit():
                device['temperature'] = int(temperature_str)
            else:
                device['temperature'] = None

            # mode
            mode_val = request.form.get('mode', '').strip()
            device['mode'] = mode_val

            # schedule_time
            schedule_time_val = request.form.get('schedule_time', '').strip()
            device['schedule_time'] = schedule_time_val

        # Save back devices
        save_devices(devices)

    return render_template('device_control.html', device=device)


@app.route('/devices/add', methods=['GET', 'POST'])
def add_device():
    rooms = [r['room_name'] for r in load_rooms(username=DEFAULT_USER)]
    device_types = ['Light', 'Thermostat', 'Camera', 'Lock', 'Sensor', 'Appliance']
    errors = {}

    if request.method == 'POST':
        device_name = request.form.get('device_name', '').strip()
        device_type = request.form.get('device_type', '').strip()
        device_room = request.form.get('device_room', '').strip()

        # Validate input
        if not device_name:
            errors['device_name'] = 'Device name is required.'
        if device_type not in device_types:
            errors['device_type'] = 'Invalid device type selected.'
        if device_room not in rooms:
            errors['device_room'] = 'Invalid room selected.'

        if not errors:
            # Find max device_id for this user
            devices = load_devices(username=DEFAULT_USER)
            if devices:
                max_id = max(d['device_id'] for d in devices)
            else:
                max_id = 0
            new_id = max_id + 1

            # Default values for new device
            new_device = {
                'username': DEFAULT_USER,
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
            return redirect(url_for('device_list'))

    return render_template('add_device.html', rooms=rooms, device_types=device_types, errors=errors)


@app.route('/automation', methods=['GET', 'POST'])
def automation_rules():
    devices = load_devices(username=DEFAULT_USER)
    rules = load_automation_rules(username=DEFAULT_USER)
    errors = {}

    if request.method == 'POST':
        rule_name = request.form.get('rule_name', '').strip()
        trigger_type = request.form.get('trigger_type', '').strip()
        trigger_value = request.form.get('trigger_value', '').strip()
        action_device_id_str = request.form.get('action_device', '').strip()
        action_type = request.form.get('action_type', '').strip()

        valid_trigger_types = ['Time', 'Motion', 'Temperature']
        valid_action_types = ['Turn On', 'Turn Off', 'Set Brightness', 'Set Temperature']

        # Validate inputs
        if not rule_name:
            errors['rule_name'] = 'Rule name is required.'
        if trigger_type not in valid_trigger_types:
            errors['trigger_type'] = 'Invalid trigger type.'
        if not trigger_value:
            errors['trigger_value'] = 'Trigger value is required.'
        try:
            action_device_id = int(action_device_id_str)
        except ValueError:
            errors['action_device'] = 'Invalid device selected.'
        else:
            if not any(d['device_id'] == action_device_id for d in devices):
                errors['action_device'] = 'Selected device does not exist.'

        if action_type not in valid_action_types:
            errors['action_type'] = 'Invalid action type.'

        if not errors:
            # Find max rule_id
            if rules:
                max_rule_id = max(r['rule_id'] for r in rules)
            else:
                max_rule_id = 0
            new_rule_id = max_rule_id + 1

            # Determine action_value from form if needed
            action_value = ''
            if action_type in ['Set Brightness', 'Set Temperature']:
                action_value = request.form.get('action_value', '').strip()

            new_rule = {
                'username': DEFAULT_USER,
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
            save_automation_rules(rules)
            return redirect(url_for('automation_rules'))

    return render_template('automation.html', rules=rules, devices=devices, errors=errors)


@app.route('/energy', methods=['GET', 'POST'])
def energy_report():
    energy_data = load_energy_logs(username=DEFAULT_USER)
    filter_date = ''

    if request.method == 'POST':
        filter_date = request.form.get('filter_date', '').strip()
        if filter_date:
            energy_data = [e for e in energy_data if e['date'] == filter_date]

    # Summarize energy consumption and cost (cost estimate $0.12 per kWh assumed)
    total_consumption = sum(e['consumption_kwh'] for e in energy_data)
    total_cost = total_consumption * 0.12
    energy_summary = {
        'total_consumption': round(total_consumption, 3),
        'total_cost': round(total_cost, 2)
    }

    return render_template('energy.html', energy_data=energy_data, energy_summary=energy_summary, filter_date=filter_date)


@app.route('/activity', methods=['GET', 'POST'])
def activity_logs():
    activities = load_activity_logs(username=DEFAULT_USER)
    search_query = ''

    if request.method == 'POST':
        search_query = request.form.get('search_query', '').strip().lower()
        if search_query:
            activities = [a for a in activities if search_query in a['action'].lower() or search_query in a['details'].lower()]

    return render_template('activity_logs.html', activities=activities, search_query=search_query)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
