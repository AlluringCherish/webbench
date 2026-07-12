from flask import Flask, render_template, redirect, url_for, request
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

USERS_FILE = os.path.join(DATA_DIR, 'users.txt')
DEVICES_FILE = os.path.join(DATA_DIR, 'devices.txt')
ROOMS_FILE = os.path.join(DATA_DIR, 'rooms.txt')
AUTOMATION_RULES_FILE = os.path.join(DATA_DIR, 'automation_rules.txt')
ENERGY_LOGS_FILE = os.path.join(DATA_DIR, 'energy_logs.txt')
ACTIVITY_LOGS_FILE = os.path.join(DATA_DIR, 'activity_logs.txt')

# Helper functions

def load_users():
    users = []
    try:
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 2:
                    continue
                users.append({'username': parts[0], 'email': parts[1]})
    except FileNotFoundError:
        pass
    return users


def load_devices(username=None):
    devices = []
    try:
        with open(DEVICES_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 13:
                    continue
                owner = parts[0]
                if username is not None and owner != username:
                    continue
                try:
                    device_id = int(parts[1])
                except ValueError:
                    continue
                brightness = int(parts[9]) if parts[9].isdigit() else None
                temperature = int(parts[10]) if parts[10].isdigit() else None
                mode = parts[11] if parts[11] else None
                schedule_time = parts[12] if parts[12] else None
                device = {
                    'username': owner,
                    'device_id': device_id,
                    'device_name': parts[2],
                    'device_type': parts[3],
                    'room': parts[4],
                    'brand': parts[5],
                    'model': parts[6],
                    'status': parts[7],
                    'power': parts[8],
                    'brightness': brightness,
                    'temperature': temperature,
                    'mode': mode,
                    'schedule_time': schedule_time
                }
                devices.append(device)
    except FileNotFoundError:
        pass
    return devices


def save_devices(devices):
    try:
        with open(DEVICES_FILE, 'w', encoding='utf-8') as f:
            for d in devices:
                line = '|'.join([
                    d.get('username', ''),
                    str(d.get('device_id', '')),
                    d.get('device_name', ''),
                    d.get('device_type', ''),
                    d.get('room', ''),
                    d.get('brand', ''),
                    d.get('model', ''),
                    d.get('status', ''),
                    d.get('power', ''),
                    str(d.get('brightness')) if d.get('brightness') is not None else '',
                    str(d.get('temperature')) if d.get('temperature') is not None else '',
                    d.get('mode') if d.get('mode') is not None else '',
                    d.get('schedule_time') if d.get('schedule_time') is not None else ''
                ]) + '\n'
                f.write(line)
    except Exception:
        pass


def load_rooms(username=None):
    rooms = []
    try:
        with open(ROOMS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 3:
                    continue
                owner = parts[0]
                if username is not None and owner != username:
                    continue
                try:
                    room_id = int(parts[1])
                except ValueError:
                    continue
                rooms.append({'username': owner, 'room_id': room_id, 'room_name': parts[2]})
    except FileNotFoundError:
        pass
    return rooms


def load_automation_rules(username=None):
    rules = []
    try:
        with open(AUTOMATION_RULES_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 9:
                    continue
                owner = parts[0]
                if username is not None and owner != username:
                    continue
                try:
                    rule_id = int(parts[1])
                    action_device_id = int(parts[5])
                except ValueError:
                    continue
                enabled = True if parts[8].lower() == 'true' else False
                action_value = parts[7] if parts[7] else None
                rule = {
                    'username': owner,
                    'rule_id': rule_id,
                    'rule_name': parts[2],
                    'trigger_type': parts[3],
                    'trigger_value': parts[4],
                    'action_device_id': action_device_id,
                    'action_type': parts[6],
                    'action_value': action_value,
                    'enabled': enabled
                }
                rules.append(rule)
    except FileNotFoundError:
        pass
    return rules


def save_automation_rules(rules):
    try:
        with open(AUTOMATION_RULES_FILE, 'w', encoding='utf-8') as f:
            for r in rules:
                line = '|'.join([
                    r.get('username', ''),
                    str(r.get('rule_id', '')),
                    r.get('rule_name', ''),
                    r.get('trigger_type', ''),
                    r.get('trigger_value', ''),
                    str(r.get('action_device_id', '')),
                    r.get('action_type', ''),
                    r.get('action_value') if r.get('action_value') is not None else '',
                    'true' if r.get('enabled') else 'false'
                ]) + '\n'
                f.write(line)
    except Exception:
        pass


def load_energy_logs(username=None, filter_date=None):
    energy_logs = []
    try:
        with open(ENERGY_LOGS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 4:
                    continue
                owner = parts[0]
                if username is not None and owner != username:
                    continue
                date = parts[2]
                if filter_date is not None and date != filter_date:
                    continue
                try:
                    device_id = int(parts[1])
                    consumption_kwh = float(parts[3])
                except ValueError:
                    continue
                energy_logs.append({
                    'username': owner,
                    'device_id': device_id,
                    'date': date,
                    'consumption_kwh': consumption_kwh
                })
    except FileNotFoundError:
        pass
    return energy_logs


def load_activity_logs(username=None, search_query=None):
    activities = []
    try:
        with open(ACTIVITY_LOGS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 5:
                    continue
                owner = parts[0]
                if username is not None and owner != username:
                    continue
                action = parts[3]
                details = parts[4]
                if search_query is not None and search_query.lower() not in action.lower() and search_query.lower() not in details.lower():
                    continue
                try:
                    device_id = int(parts[2])
                except ValueError:
                    continue
                activities.append({
                    'username': owner,
                    'timestamp': parts[1],
                    'device_id': device_id,
                    'action': action,
                    'details': details
                })
    except FileNotFoundError:
        pass
    return activities


# ID generation helpers

def get_next_device_id(devices):
    if not devices:
        return 1
    return max(d['device_id'] for d in devices) + 1


def get_next_rule_id(rules):
    if not rules:
        return 1
    return max(r['rule_id'] for r in rules) + 1


# For demo, hardcode username
CURRENT_USERNAME = 'john_doe'


@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    devices = load_devices(username=CURRENT_USERNAME)
    rooms = load_rooms(username=CURRENT_USERNAME)

    total_devices = len(devices)
    active_devices = sum(1 for d in devices if d['status'].lower() == 'online')
    offline_devices = total_devices - active_devices
    device_summary = {'total': total_devices, 'active': active_devices, 'offline': offline_devices}

    devices_for_template = [{k:v for k,v in d.items() if k != 'username'} for d in devices]
    rooms_for_template = [{k:v for k,v in r.items() if k != 'username'} for r in rooms]

    return render_template('dashboard.html', devices=devices_for_template, rooms=rooms_for_template, device_summary=device_summary)


@app.route('/devices')
def device_list():
    devices = load_devices(username=CURRENT_USERNAME)
    devices_for_template = [{k:v for k,v in d.items() if k != 'username'} for d in devices]
    return render_template('devices.html', devices=devices_for_template)


@app.route('/devices/add', methods=['GET', 'POST'])
def add_device():
    form_errors = {}
    rooms = load_rooms(username=CURRENT_USERNAME)
    rooms_for_template = [{k:v for k,v in r.items() if k != 'username'} for r in rooms]
    device_types = ['Light', 'Thermostat', 'Camera', 'Lock', 'Sensor', 'Appliance']

    if request.method == 'POST':
        device_name = request.form.get('device-name', '').strip()
        device_type = request.form.get('device-type', '').strip()
        device_room = request.form.get('device-room', '').strip()

        # Validate inputs
        if not device_name:
            form_errors['device_name'] = 'Device name is required.'
        if device_type not in device_types:
            form_errors['device_type'] = 'Invalid device type selected.'
        if not any(r['room_name'] == device_room for r in rooms):
            form_errors['device_room'] = 'Invalid room selected.'

        if form_errors:
            return render_template('add_device.html', rooms=rooms_for_template, device_types=device_types, form_errors=form_errors)

        devices = load_devices(username=None)  # Load all devices to find next ID
        new_device_id = get_next_device_id(devices)

        # Add new device values carefully - brand and model not in form so set empty
        new_device = {
            'username': CURRENT_USERNAME,
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
            'mode': None,
            'schedule_time': None
        }

        devices.append(new_device)
        save_devices(devices)

        return redirect(url_for('device_list'))

    return render_template('add_device.html', rooms=rooms_for_template, device_types=device_types, form_errors=form_errors)


@app.route('/device/<int:device_id>', methods=['GET', 'POST'])
def control_device(device_id):
    devices = load_devices(username=None)
    device = next((d for d in devices if d['device_id'] == device_id), None)
    if device is None or device['username'] != CURRENT_USERNAME:
        return "Device not found", 404

    status = device['status']

    if request.method == 'POST':
        power = request.form.get('power-toggle', '').lower()
        if power in ['on', 'off']:
            device['power'] = power
            device['status'] = 'Online' if power == 'on' else 'Offline'

        if device['device_type'] == 'Light':
            brightness_s = request.form.get('brightness', '')
            if brightness_s.isdigit():
                brightness = int(brightness_s)
                if 0 <= brightness <= 100:
                    device['brightness'] = brightness

        elif device['device_type'] == 'Thermostat':
            temperature_s = request.form.get('temperature', '')
            mode = request.form.get('mode', '').strip()
            schedule_time = request.form.get('schedule_time', '').strip()

            if temperature_s.isdigit():
                device['temperature'] = int(temperature_s)

            if mode:
                device['mode'] = mode
            else:
                device['mode'] = None

            if schedule_time:
                device['schedule_time'] = schedule_time
            else:
                device['schedule_time'] = None

        save_devices(devices)
        status = device['status']

    device_for_template = {k:v for k,v in device.items() if k != 'username'}

    return render_template('device_control.html', device=device_for_template, status=status)


@app.route('/automation', methods=['GET', 'POST'])
def automation_rules():
    rules = load_automation_rules(username=CURRENT_USERNAME)
    devices = load_devices(username=CURRENT_USERNAME)
    form_errors = {}

    if request.method == 'POST':
        rule_name = request.form.get('rule-name', '').strip()
        trigger_type = request.form.get('trigger-type', '').strip()
        trigger_value = request.form.get('trigger-value', '').strip()
        action_device_id_s = request.form.get('action-device', '').strip()
        action_type = request.form.get('action-type', '').strip()

        if not rule_name:
            form_errors['rule_name'] = 'Rule name is required.'
        if trigger_type not in ['Time', 'Motion', 'Temperature']:
            form_errors['trigger_type'] = 'Invalid trigger type.'
        if not trigger_value:
            form_errors['trigger_value'] = 'Trigger value is required.'
        try:
            action_device_id = int(action_device_id_s)
            if not any(d['device_id'] == action_device_id for d in devices):
                form_errors['action_device'] = 'Invalid target device.'
        except ValueError:
            form_errors['action_device'] = 'Invalid target device.'
        if action_type not in ['Turn On', 'Turn Off', 'Set Brightness', 'Set Temperature']:
            form_errors['action_type'] = 'Invalid action type.'

        # Determine action_value for Set Brightness or Set Temperature
        action_value = ''
        if action_type in ['Set Brightness', 'Set Temperature']:
            action_value = request.form.get('action-value', '').strip()
            if not action_value:
                form_errors['action_value'] = 'Action value is required for the selected action type.'

        if form_errors:
            rules_for_template = [{k:v for k,v in r.items() if k != 'username'} for r in rules]
            devices_for_template = [{k:v for k,v in d.items() if k != 'username'} for d in devices]
            return render_template('automation.html', rules=rules_for_template, devices=devices_for_template, form_errors=form_errors)

        new_rule_id = get_next_rule_id(rules)
        new_rule = {
            'username': CURRENT_USERNAME,
            'rule_id': new_rule_id,
            'rule_name': rule_name,
            'trigger_type': trigger_type,
            'trigger_value': trigger_value,
            'action_device_id': action_device_id,
            'action_type': action_type,
            'action_value': action_value if action_value else None,
            'enabled': True
        }

        rules.append(new_rule)
        save_automation_rules(rules)

        return redirect(url_for('automation_rules'))

    rules_for_template = [{k:v for k,v in r.items() if k != 'username'} for r in rules]
    devices_for_template = [{k:v for k,v in d.items() if k != 'username'} for d in devices]
    return render_template('automation.html', rules=rules_for_template, devices=devices_for_template, form_errors=form_errors)


@app.route('/energy', methods=['GET', 'POST'])
def energy_report():
    filter_date = None
    if request.method == 'POST':
        filter_date = request.form.get('date-filter', '').strip()
        if not filter_date:
            filter_date = None

    energy_logs = load_energy_logs(username=CURRENT_USERNAME, filter_date=filter_date)

    total_consumption = sum(e['consumption_kwh'] for e in energy_logs)
    total_cost = round(total_consumption * 0.12, 2)  # Assuming $0.12/kWh

    energy_summary = {'total_consumption': total_consumption, 'total_cost': total_cost}

    filter_date_str = filter_date if filter_date else ''

    return render_template('energy.html', energy_logs=energy_logs, energy_summary=energy_summary, filter_date=filter_date_str)


@app.route('/activity', methods=['GET', 'POST'])
def activity_logs():
    search_query = None
    if request.method == 'POST':
        search_query = request.form.get('search-activity', '').strip()
        if not search_query:
            search_query = None

    activities = load_activity_logs(username=CURRENT_USERNAME, search_query=search_query)

    return render_template('activity.html', activities=activities, search_query=search_query if search_query else '')


if __name__ == '__main__':
    app.run(debug=True, port=5000)
