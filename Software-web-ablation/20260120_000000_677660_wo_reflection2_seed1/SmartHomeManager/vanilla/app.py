from flask import Flask, render_template, redirect, url_for, request
import os
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

# Data file paths
DATA_DIR = 'data'
USERS_FILE = os.path.join(DATA_DIR, 'users.txt')
DEVICES_FILE = os.path.join(DATA_DIR, 'devices.txt')
ROOMS_FILE = os.path.join(DATA_DIR, 'rooms.txt')
AUTOMATION_RULES_FILE = os.path.join(DATA_DIR, 'automation_rules.txt')
ENERGY_LOGS_FILE = os.path.join(DATA_DIR, 'energy_logs.txt')
ACTIVITY_LOGS_FILE = os.path.join(DATA_DIR, 'activity_logs.txt')

# Constants
DEVICE_TYPES = ["Light", "Thermostat", "Camera", "Lock", "Sensor", "Appliance"]
ROOM_OPTIONS = ["Living Room", "Bedroom", "Kitchen", "Bathroom", "Garage"]
TRIGGER_TYPES = ["Time", "Motion", "Temperature"]
ACTION_TYPES = ["Turn On", "Turn Off", "Set Brightness", "Set Temperature"]

# Helper functions to load and save data

def load_users():
    users = []
    try:
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 2:
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
                if len(parts) == 13:
                    device_username = parts[0]
                    if username is None or device_username == username:
                        device = {
                            'username': device_username,
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
                            'schedule_time': parts[12]
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
                ])
                f.write(line + '\n')
    except Exception:
        pass


def load_rooms(username=None):
    rooms = []
    try:
        with open(ROOMS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 3:
                    room_username = parts[0]
                    if username is None or room_username == username:
                        room = {
                            'username': room_username,
                            'room_id': int(parts[1]),
                            'room_name': parts[2]
                        }
                        rooms.append(room)
    except FileNotFoundError:
        pass
    return rooms


def load_automation_rules(username=None):
    rules = []
    try:
        with open(AUTOMATION_RULES_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 9:
                    rule_username = parts[0]
                    if username is None or rule_username == username:
                        rule = {
                            'username': rule_username,
                            'rule_id': int(parts[1]),
                            'rule_name': parts[2],
                            'trigger_type': parts[3],
                            'trigger_value': parts[4],
                            'action_device_id': int(parts[5]),
                            'action_type': parts[6],
                            'action_value': parts[7],
                            'enabled': parts[8] == 'true'
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
                    r['username'],
                    str(r['rule_id']),
                    r['rule_name'],
                    r['trigger_type'],
                    r['trigger_value'],
                    str(r['action_device_id']),
                    r['action_type'],
                    r['action_value'],
                    'true' if r['enabled'] else 'false'
                ])
                f.write(line + '\n')
    except Exception:
        pass


def load_energy_logs(username=None):
    logs = []
    try:
        with open(ENERGY_LOGS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 4:
                    log_username = parts[0]
                    if username is None or log_username == username:
                        try:
                            consumption = float(parts[3])
                        except ValueError:
                            consumption = 0.0
                        log = {
                            'username': log_username,
                            'device_id': int(parts[1]),
                            'date': parts[2],
                            'consumption_kwh': consumption
                        }
                        logs.append(log)
    except FileNotFoundError:
        pass
    return logs


def load_activity_logs(username=None):
    logs = []
    try:
        with open(ACTIVITY_LOGS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 5:
                    log_username = parts[0]
                    if username is None or log_username == username:
                        log = {
                            'username': log_username,
                            'timestamp': parts[1],
                            'device_id': int(parts[2]),
                            'action': parts[3],
                            'details': parts[4]
                        }
                        logs.append(log)
    except FileNotFoundError:
        pass
    return logs


# We will use a fixed user for demonstration since no user login is specified
# Default user
DEFAULT_USERNAME = 'john_doe'

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard_page'))

@app.route('/dashboard')
def dashboard_page():
    username = DEFAULT_USERNAME
    devices = load_devices(username)
    rooms = load_rooms(username)

    # Device summary
    total_devices = len(devices)
    active_devices = sum(1 for d in devices if d['status'] == 'Online')
    offline_devices = sum(1 for d in devices if d['status'] != 'Online')

    device_summary = {
        'total_devices': total_devices,
        'active_devices': active_devices,
        'offline_devices': offline_devices
    }

    # For rooms, also count devices per room
    room_list = []
    for room in rooms:
        count = sum(1 for d in devices if d['room'] == room['room_name'])
        room_list.append({'room_name': room['room_name'], 'device_count': count})

    return render_template('dashboard.html', 
                           devices=devices, 
                           rooms=room_list, 
                           device_summary=device_summary)

@app.route('/devices')
def device_list_page():
    username = DEFAULT_USERNAME
    devices = load_devices(username)
    return render_template('devices.html', devices=devices)

@app.route('/device/add', methods=['GET'])
def add_device_form():
    # Provide lists of device types and rooms
    return render_template('add_device.html', device_types=DEVICE_TYPES, rooms=ROOM_OPTIONS)

@app.route('/device/add', methods=['POST'])
def add_device_submit():
    username = DEFAULT_USERNAME
    # Read form data
    device_name = request.form.get('device-name', '').strip()
    device_type = request.form.get('device-type', '')
    device_room = request.form.get('device-room', '')

    # Basic validation
    if device_name == '' or device_type not in DEVICE_TYPES or device_room not in ROOM_OPTIONS:
        # On invalid input, redirect back to add page
        return redirect(url_for('add_device_form'))

    devices = load_devices(username)
    # Generate new device_id unique for this user
    existing_ids = [d['device_id'] for d in devices]
    new_id = max(existing_ids) + 1 if existing_ids else 1

    # For this implementation, use fixed placeholders for brand, model, status, power, etc.
    new_device = {
        'username': username,
        'device_id': new_id,
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
    save_devices(devices)

    return redirect(url_for('device_list_page'))

@app.route('/device/<int:device_id>')
def device_control_page(device_id):
    username = DEFAULT_USERNAME
    devices = load_devices(username)
    device = next((d for d in devices if d['device_id'] == device_id), None)
    if not device:
        return redirect(url_for('device_list_page'))

    return render_template('device_control.html', device=device)

@app.route('/device/<int:device_id>/control', methods=['POST'])
def control_device_submit(device_id):
    username = DEFAULT_USERNAME
    devices = load_devices(username)
    device = next((d for d in devices if d['device_id'] == device_id), None)
    if not device:
        return redirect(url_for('device_list_page'))

    # Read form data to control the device
    # Possible control: toggle power or save settings like brightness, temperature, mode, schedule_time

    # Toggle power button may send a form field 'power_toggle' with 'on' or 'off'
    power = request.form.get('power')
    brightness = request.form.get('brightness')
    temperature = request.form.get('temperature')
    mode = request.form.get('mode')
    schedule_time = request.form.get('schedule_time')

    # Update device properties as appropriate
    if power in ['on', 'off']:
        device['power'] = power
        # Update status accordingly
        device['status'] = 'Online' if power == 'on' else 'Offline'

    # Only update brightness if device supports it (size > 0 brightness and string not empty for allowed device types)
    if device['device_type'] in ['Light', 'Appliance']:
        if brightness is not None:
            brightness = brightness.strip()
            device['brightness'] = brightness if brightness else ''
    # Thermostat supports temperature
    if device['device_type'] == 'Thermostat':
        if temperature is not None:
            temperature = temperature.strip()
            device['temperature'] = temperature if temperature else ''
    # Mode update for devices supporting mode
    if mode is not None:
        mode = mode.strip()
        device['mode'] = mode if mode else ''

    # Schedule time update
    if schedule_time is not None:
        schedule_time = schedule_time.strip()
        device['schedule_time'] = schedule_time if schedule_time else ''

    save_devices(devices)

    # Redirect back to device control page
    return redirect(url_for('device_control_page', device_id=device_id))

@app.route('/automation')
def automation_rules_page():
    username = DEFAULT_USERNAME
    rules = load_automation_rules(username)
    devices = load_devices(username)
    return render_template('automation.html', automation_rules=rules, devices=devices)

@app.route('/automation/add', methods=['POST'])
def add_automation_rule():
    username = DEFAULT_USERNAME
    # Read form data
    rule_name = request.form.get('rule-name', '').strip()
    trigger_type = request.form.get('trigger-type', '')
    trigger_value = request.form.get('trigger-value', '').strip()
    action_device_id_str = request.form.get('action-device')
    action_type = request.form.get('action-type', '')
    action_value = request.form.get('action-value', '').strip()

    # Validate inputs
    # Convert action_device_id to int if possible
    try:
        action_device_id = int(action_device_id_str)
    except (ValueError, TypeError):
        action_device_id = None

    if (rule_name == '' or 
        trigger_type not in TRIGGER_TYPES or 
        action_device_id is None or 
        action_type not in ACTION_TYPES):
        return redirect(url_for('automation_rules_page'))

    rules = load_automation_rules(username)

    existing_ids = [r['rule_id'] for r in rules]
    new_rule_id = max(existing_ids) + 1 if existing_ids else 1

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

    save_automation_rules(rules)

    return redirect(url_for('automation_rules_page'))

@app.route('/energy')
def energy_report_page():
    username = DEFAULT_USERNAME
    energy_logs = load_energy_logs(username)

    total_consumption = sum(log['consumption_kwh'] for log in energy_logs)
    # Cost estimate: Assume $0.12 per kWh for example
    total_cost = total_consumption * 0.12

    return render_template('energy.html', energy_logs=energy_logs, total_consumption=total_consumption, total_cost=total_cost)

@app.route('/energy/filter', methods=['POST'])
def apply_energy_filter():
    username = DEFAULT_USERNAME
    date_filter = request.form.get('date-filter')  # expected format YYYY-MM-DD

    energy_logs = load_energy_logs(username)

    if date_filter:
        filtered_logs = [log for log in energy_logs if log['date'] == date_filter]
    else:
        filtered_logs = energy_logs

    total_consumption = sum(log['consumption_kwh'] for log in filtered_logs)
    total_cost = total_consumption * 0.12

    return render_template('energy.html', energy_logs=filtered_logs, total_consumption=total_consumption, total_cost=total_cost)

@app.route('/activity')
def activity_logs_page():
    username = DEFAULT_USERNAME
    activity_logs = load_activity_logs(username)
    return render_template('activity.html', activity_logs=activity_logs)

@app.route('/activity/search', methods=['POST'])
def search_activity_logs():
    username = DEFAULT_USERNAME
    search_string = request.form.get('search-activity', '').strip().lower()
    activity_logs = load_activity_logs(username)

    if search_string:
        filtered_logs = [log for log in activity_logs if 
                         search_string in log['action'].lower() or
                         search_string in log['details'].lower()]
    else:
        filtered_logs = activity_logs

    return render_template('activity.html', activity_logs=filtered_logs)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
