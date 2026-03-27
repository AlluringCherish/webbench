from flask import Flask, render_template, redirect, url_for, request, abort
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Constants for file paths and device types and rooms
USERS_FILE = 'data/users.txt'
DEVICES_FILE = 'data/devices.txt'
ROOMS_FILE = 'data/rooms.txt'
AUTOMATION_RULES_FILE = 'data/automation_rules.txt'
ENERGY_LOGS_FILE = 'data/energy_logs.txt'
ACTIVITY_LOGS_FILE = 'data/activity_logs.txt'

DEVICE_TYPES = ['Light', 'Thermostat', 'Camera', 'Lock', 'Sensor', 'Appliance']
DEFAULT_ROOMS = ['Living Room', 'Bedroom', 'Kitchen', 'Bathroom', 'Garage']

CURRENT_USERNAME = 'john_doe'  # For simplicity, fixed username

# Utility functions to read and write pipe delimited files

def read_devices(username):
    devices = []
    if not os.path.exists(DEVICES_FILE):
        return devices
    try:
        with open(DEVICES_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                fields = line.split('|')
                if len(fields) != 13:
                    continue
                (
                    file_username, device_id, device_name, device_type, room, brand, model,
                    status, power, brightness, temperature, mode, schedule_time
                ) = fields
                if file_username != username:
                    continue
                device = {
                    'username': file_username,
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
        # On error, return empty list
        return []
    return devices


def write_devices(username, devices):
    # Write all devices of user + others to file
    try:
        all_devices = []
        if os.path.exists(DEVICES_FILE):
            with open(DEVICES_FILE, 'r', encoding='utf-8') as f:
                for line in f:
                    line=line.strip()
                    if not line:
                        continue
                    fields = line.split('|')
                    if len(fields) != 13:
                        continue
                    file_username = fields[0]
                    if file_username != username:
                        all_devices.append(line)
        # Now add all devices for username from devices param
        with open(DEVICES_FILE, 'w', encoding='utf-8') as f:
            for line in all_devices:
                f.write(line + '\n')
            for d in devices:
                parts = [
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
                ]
                f.write('|'.join(parts) + '\n')
        return True
    except Exception:
        return False


def read_rooms(username):
    rooms = []
    if not os.path.exists(ROOMS_FILE):
        return rooms
    try:
        with open(ROOMS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                fields = line.split('|')
                if len(fields) != 3:
                    continue
                file_username, room_id, room_name = fields
                if file_username != username:
                    continue
                room = {
                    'username': file_username,
                    'room_id': int(room_id),
                    'room_name': room_name
                }
                rooms.append(room)
    except Exception:
        return []
    return rooms


def read_automation_rules(username):
    rules = []
    if not os.path.exists(AUTOMATION_RULES_FILE):
        return rules
    try:
        with open(AUTOMATION_RULES_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                fields = line.split('|')
                if len(fields) != 9:
                    continue
                (file_username, rule_id, rule_name, trigger_type, trigger_value, action_device_id, action_type, action_value, enabled) = fields
                if file_username != username:
                    continue
                rule = {
                    'username': file_username,
                    'rule_id': int(rule_id),
                    'rule_name': rule_name,
                    'trigger_type': trigger_type,
                    'trigger_value': trigger_value,
                    'action_device_id': int(action_device_id),
                    'action_type': action_type,
                    'action_value': action_value,
                    'enabled': enabled
                }
                rules.append(rule)
    except Exception:
        return []
    return rules


def write_automation_rules(username, rules):
    try:
        all_rules = []
        if os.path.exists(AUTOMATION_RULES_FILE):
            with open(AUTOMATION_RULES_FILE, 'r', encoding='utf-8') as f:
                for line in f:
                    line=line.strip()
                    if not line:
                        continue
                    fields = line.split('|')
                    if len(fields) != 9:
                        continue
                    file_username = fields[0]
                    if file_username != username:
                        all_rules.append(line)
        with open(AUTOMATION_RULES_FILE, 'w', encoding='utf-8') as f:
            for line in all_rules:
                f.write(line + '\n')
            for r in rules:
                parts = [
                    r['username'],
                    str(r['rule_id']),
                    r['rule_name'],
                    r['trigger_type'],
                    r['trigger_value'],
                    str(r['action_device_id']),
                    r['action_type'],
                    r['action_value'],
                    r['enabled']
                ]
                f.write('|'.join(parts) + '\n')
        return True
    except Exception:
        return False


def read_energy_logs(username):
    energy_logs = []
    if not os.path.exists(ENERGY_LOGS_FILE):
        return energy_logs
    try:
        with open(ENERGY_LOGS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                fields = line.split('|')
                if len(fields) != 4:
                    continue
                file_username, device_id, date, consumption_kwh = fields
                if file_username != username:
                    continue
                log = {
                    'username': file_username,
                    'device_id': int(device_id),
                    'date': date,
                    'consumption_kwh': float(consumption_kwh)
                }
                energy_logs.append(log)
    except Exception:
        return []
    return energy_logs


def read_activity_logs(username):
    activity_logs = []
    if not os.path.exists(ACTIVITY_LOGS_FILE):
        return activity_logs
    try:
        with open(ACTIVITY_LOGS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                fields = line.split('|')
                if len(fields) != 5:
                    continue
                file_username, timestamp, device_id, action, details = fields
                if file_username != username:
                    continue
                log = {
                    'username': file_username,
                    'timestamp': timestamp,
                    'device_id': int(device_id),
                    'action': action,
                    'details': details
                }
                activity_logs.append(log)
    except Exception:
        return []
    return activity_logs

# Helper to get next available device_id or rule_id

def get_next_id(items, key):
    if not items:
        return 1
    return max(item[key] for item in items) + 1

# ROUTES

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard_page'))

@app.route('/dashboard')
def dashboard_page():
    try:
        devices = read_devices(CURRENT_USERNAME)
        rooms = read_rooms(CURRENT_USERNAME)
    except Exception:
        devices = []
        rooms = []

    # Device summary: total devices, active devices (status Online), offline devices
    total_devices = len(devices)
    active_devices = sum(1 for d in devices if d.get('status') == 'Online')
    offline_devices = total_devices - active_devices

    device_summary = {
        'total_devices': total_devices,
        'active_devices': active_devices,
        'offline_devices': offline_devices
    }

    return render_template(
        'dashboard.html',
        devices=devices,
        rooms=rooms,
        device_summary=device_summary
    )

@app.route('/devices')
def device_list_page():
    try:
        devices = read_devices(CURRENT_USERNAME)
        rooms_list = read_rooms(CURRENT_USERNAME)
    except Exception:
        devices = []
        rooms_list = []

    # Create rooms dict with room_id as key and room_name
    rooms = {room['room_id']: room['room_name'] for room in rooms_list}

    return render_template('device_list.html', devices=devices, rooms=rooms)

@app.route('/devices/add', methods=['GET', 'POST'])
def add_device_page():
    form_errors = {}
    device_types = DEVICE_TYPES
    rooms = DEFAULT_ROOMS

    if request.method == 'POST':
        device_name = request.form.get('device-name', '').strip()
        device_type = request.form.get('device-type')
        device_room = request.form.get('device-room')

        # Validate inputs
        if not device_name:
            form_errors['device_name'] = 'Device name is required.'
        if device_type not in DEVICE_TYPES:
            form_errors['device_type'] = 'Invalid device type selected.'
        if device_room not in DEFAULT_ROOMS:
            form_errors['device_room'] = 'Invalid room selected.'

        if not form_errors:
            # Add new device
            devices = read_devices(CURRENT_USERNAME)
            new_id = get_next_id(devices, 'device_id')

            # Create new device dict, default values for missing fields
            new_device = {
                'username': CURRENT_USERNAME,
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

            success = write_devices(CURRENT_USERNAME, devices)
            if success:
                return redirect(url_for('device_list_page'))
            else:
                form_errors['general'] = 'Failed to save the new device. Please try again.'

    return render_template('add_device.html', device_types=device_types, rooms=rooms, form_errors=form_errors)

@app.route('/devices/<int:device_id>', methods=['GET', 'POST'])
def device_control_page(device_id):
    form_errors = {}
    devices = read_devices(CURRENT_USERNAME)
    device = None
    for d in devices:
        if d['device_id'] == device_id:
            device = d
            break
    if device is None:
        abort(404)

    if request.method == 'POST':
        # We only support toggling power and saving status
        power = request.form.get('power-toggle')
        # For simplicity, power toggle button sends 'on' or 'off'
        if power not in ('on', 'off'):
            form_errors['power'] = 'Invalid power state.'
        else:
            device['power'] = power
            device['status'] = 'Online' if power == 'on' else 'Offline'

        # Additional settings might be brightness, temperature, mode, schedule_time
        brightness = request.form.get('brightness', '').strip()
        temperature = request.form.get('temperature', '').strip()
        mode = request.form.get('mode', '').strip()
        schedule_time = request.form.get('schedule_time', '').strip()

        # Save only if no errors
        if not form_errors:
            # Validate brightness only if it's set and device supports brightness
            if device['device_type'] == 'Light' or device['device_type'] == 'Appliance':
                if brightness:
                    try:
                        bval = int(brightness)
                        if bval < 0 or bval > 100:
                            form_errors['brightness'] = 'Brightness must be between 0 and 100.'
                        else:
                            device['brightness'] = brightness
                    except ValueError:
                        form_errors['brightness'] = 'Brightness must be an integer.'
                else:
                    device['brightness'] = ''
            else:
                device['brightness'] = ''

            # Validate temperature if device supports it
            if device['device_type'] in ('Thermostat', 'Appliance'):
                if temperature:
                    try:
                        tval = int(temperature)
                        if tval < 10 or tval > 35:
                            form_errors['temperature'] = 'Temperature must be between 10 and 35.'
                        else:
                            device['temperature'] = temperature
                    except ValueError:
                        form_errors['temperature'] = 'Temperature must be an integer.'
                else:
                    device['temperature'] = ''
            else:
                device['temperature'] = ''

            # Mode and schedule_time can be set directly
            device['mode'] = mode
            device['schedule_time'] = schedule_time

        if not form_errors:
            success = write_devices(CURRENT_USERNAME, devices)
            if success:
                return redirect(url_for('device_control_page', device_id=device_id))
            else:
                form_errors['general'] = 'Failed to save device settings. Please try again.'

    return render_template('device_control.html', device=device, form_errors=form_errors)

@app.route('/automation', methods=['GET', 'POST'])
def automation_rules_page():
    form_errors = {}
    rules = read_automation_rules(CURRENT_USERNAME)
    devices = read_devices(CURRENT_USERNAME)

    if request.method == 'POST':
        rule_name = request.form.get('rule-name', '').strip()
        trigger_type = request.form.get('trigger-type')
        trigger_value = request.form.get('trigger-value', '').strip()
        action_device_id_raw = request.form.get('action-device')
        action_type = request.form.get('action-type')

        # Validate inputs
        if not rule_name:
            form_errors['rule_name'] = 'Rule name is required.'
        if trigger_type not in ('Time', 'Motion', 'Temperature'):
            form_errors['trigger_type'] = 'Invalid trigger type.'
        if not trigger_value:
            form_errors['trigger_value'] = 'Trigger value required.'

        # Validate action_device_id
        try:
            action_device_id = int(action_device_id_raw)
        except (ValueError, TypeError):
            form_errors['action_device'] = 'Invalid action device.'
            action_device_id = None

        if action_type not in ('Turn On', 'Turn Off', 'Set Brightness', 'Set Temperature'):
            form_errors['action_type'] = 'Invalid action type.'

        if not form_errors:
            # Create new rule
            new_rule_id = get_next_id(rules, 'rule_id')
            new_rule = {
                'username': CURRENT_USERNAME,
                'rule_id': new_rule_id,
                'rule_name': rule_name,
                'trigger_type': trigger_type,
                'trigger_value': trigger_value,
                'action_device_id': action_device_id,
                'action_type': action_type,
                'action_value': '',
                'enabled': 'true'
            }
            rules.append(new_rule)
            success = write_automation_rules(CURRENT_USERNAME, rules)
            if success:
                return redirect(url_for('automation_rules_page'))
            else:
                form_errors['general'] = 'Failed to save automation rule. Please try again.'

    return render_template('automation_rules.html', automation_rules=rules, devices=devices, form_errors=form_errors)

@app.route('/energy', methods=['GET', 'POST'])
def energy_report_page():
    date_filter = ''
    energy_logs = []
    energy_summary = {'total_consumption': 0.0, 'estimated_cost': 0.0}
    COST_PER_KWH = 0.12  # Assumed cost per kWh

    try:
        all_logs = read_energy_logs(CURRENT_USERNAME)
        devices = read_devices(CURRENT_USERNAME)
    except Exception:
        all_logs = []
        devices = []

    if request.method == 'POST':
        date_filter = request.form.get('date-filter', '').strip()

    # Filter logs by date if filter given
    if date_filter:
        energy_logs = [log for log in all_logs if log['date'] == date_filter]
    else:
        energy_logs = all_logs

    # Summarize total consumption
    total_consumption = sum(log['consumption_kwh'] for log in energy_logs)
    estimated_cost = total_consumption * COST_PER_KWH
    energy_summary['total_consumption'] = total_consumption
    energy_summary['estimated_cost'] = estimated_cost

    return render_template(
        'energy_report.html',
        energy_logs=energy_logs,
        energy_summary=energy_summary,
        date_filter=date_filter
    )

@app.route('/activity', methods=['GET', 'POST'])
def activity_logs_page():
    search_term = ''
    activity_logs = []

    try:
        all_logs = read_activity_logs(CURRENT_USERNAME)
    except Exception:
        all_logs = []

    if request.method == 'POST':
        search_term = request.form.get('search-activity', '').strip().lower()

    if search_term:
        activity_logs = [log for log in all_logs if
                         search_term in log['action'].lower() or
                         search_term in log['details'].lower() or
                         search_term in log['timestamp'].lower()]
    else:
        activity_logs = all_logs

    return render_template('activity_logs.html', activity_logs=activity_logs, search_term=search_term)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
