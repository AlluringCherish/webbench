from flask import Flask, render_template, redirect, url_for, request
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

# Helper functions to read data from pipe-delimited files

def load_devices(username=None):
    devices = []
    try:
        with open(os.path.join(DATA_DIR, 'devices.txt'), 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                fields = line.split('|')
                # fields order:
                # username|device_id|device_name|device_type|room|brand|model|status|power|brightness|temperature|mode|schedule_time
                if len(fields) != 13:
                    continue
                d_username = fields[0]
                if username and d_username != username:
                    continue
                device = {
                    'username': d_username,
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
                    'mode': fields[11],
                    'schedule_time': fields[12]
                }
                devices.append(device)
    except Exception:
        pass
    return devices


def load_rooms(username=None):
    rooms = []
    try:
        with open(os.path.join(DATA_DIR, 'rooms.txt'), 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                fields = line.split('|')
                if len(fields) != 3:
                    continue
                r_username = fields[0]
                if username and r_username != username:
                    continue
                room = {
                    'username': r_username,
                    'room_id': int(fields[1]),
                    'room_name': fields[2]
                }
                rooms.append(room)
    except Exception:
        pass
    return rooms


def load_automation_rules(username=None):
    rules = []
    try:
        with open(os.path.join(DATA_DIR, 'automation_rules.txt'), 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                fields = line.split('|')
                # username|rule_id|rule_name|trigger_type|trigger_value|action_device_id|action_type|action_value|enabled
                if len(fields) != 9:
                    continue
                r_username = fields[0]
                if username and r_username != username:
                    continue
                rule = {
                    'username': r_username,
                    'rule_id': int(fields[1]),
                    'rule_name': fields[2],
                    'trigger_type': fields[3],
                    'trigger_value': fields[4],
                    'action_device_id': int(fields[5]),
                    'action_type': fields[6],
                    'action_value': fields[7],
                    'enabled': fields[8].lower() == 'true'
                }
                rules.append(rule)
    except Exception:
        pass
    return rules


def load_energy_logs(username=None):
    logs = []
    try:
        with open(os.path.join(DATA_DIR, 'energy_logs.txt'), 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                fields = line.split('|')
                # username|device_id|date|consumption_kwh
                if len(fields) != 4:
                    continue
                r_username = fields[0]
                if username and r_username != username:
                    continue
                log = {
                    'username': r_username,
                    'device_id': int(fields[1]),
                    'date': fields[2],
                    'consumption_kwh': float(fields[3])
                }
                logs.append(log)
    except Exception:
        pass
    return logs


def load_activity_logs(username=None):
    logs = []
    try:
        with open(os.path.join(DATA_DIR, 'activity_logs.txt'), 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                fields = line.split('|')
                # username|timestamp|device_id|action|details
                if len(fields) != 5:
                    continue
                r_username = fields[0]
                if username and r_username != username:
                    continue
                log = {
                    'username': r_username,
                    'timestamp': fields[1],
                    'device_id': int(fields[2]),
                    'action': fields[3],
                    'details': fields[4]
                }
                logs.append(log)
    except Exception:
        pass
    return logs


def save_devices(devices, username):
    # devices is list of dicts for user only
    try:
        # Load all devices for all users first
        all_devices = []
        with open(os.path.join(DATA_DIR, 'devices.txt'), 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                fields = line.split('|')
                if len(fields) != 13:
                    continue
                d_username = fields[0]
                if d_username != username:
                    all_devices.append(line)
        # Now add updated user devices
        for d in devices:
            brightness_str = str(d['brightness']) if d['brightness'] is not None else ''
            temperature_str = str(d['temperature']) if d['temperature'] is not None else ''
            newline = '|'.join([
                username,
                str(d['device_id']),
                d['device_name'],
                d['device_type'],
                d['room'],
                d['brand'],
                d['model'],
                d['status'],
                d['power'],
                brightness_str,
                temperature_str,
                d['mode'],
                d['schedule_time']
            ])
            all_devices.append(newline)
        with open(os.path.join(DATA_DIR, 'devices.txt'), 'w') as f:
            f.write('\n'.join(all_devices) + '\n')
    except Exception:
        pass


def save_automation_rules(rules, username):
    try:
        # Load all rules for all users first
        all_rules = []
        with open(os.path.join(DATA_DIR, 'automation_rules.txt'), 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                fields = line.split('|')
                if len(fields) != 9:
                    continue
                r_username = fields[0]
                if r_username != username:
                    all_rules.append(line)
        # Add updated user rules
        for r in rules:
            enabled_str = 'true' if r['enabled'] else 'false'
            newline = '|'.join([
                username,
                str(r['rule_id']),
                r['rule_name'],
                r['trigger_type'],
                r['trigger_value'],
                str(r['action_device_id']),
                r['action_type'],
                r.get('action_value', ''),
                enabled_str
            ])
            all_rules.append(newline)
        with open(os.path.join(DATA_DIR, 'automation_rules.txt'), 'w') as f:
            f.write('\n'.join(all_rules) + '\n')
    except Exception:
        pass


# For this implementation, we assume a default user "john_doe"
DEFAULT_USER = 'john_doe'


@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard_page'))


@app.route('/dashboard')
def dashboard_page():
    # Summary of devices: total, active, offline
    devices = load_devices(DEFAULT_USER)
    total = len(devices)
    active_count = sum(1 for d in devices if d['status'] == 'Online')
    offline_count = total - active_count

    # Rooms with device counts
    rooms = load_rooms(DEFAULT_USER)
    room_data = []
    # Count devices per room
    devices_by_room = {}
    for d in devices:
        devices_by_room[d['room']] = devices_by_room.get(d['room'], 0) + 1
    for r in rooms:
        room_name = r['room_name']
        room_data.append({'room_name': room_name, 'device_count': devices_by_room.get(room_name, 0)})

    devices_summary = {'total': total, 'active': active_count, 'offline': offline_count}

    return render_template('dashboard.html', devices_summary=devices_summary, rooms=room_data)


@app.route('/devices')
def device_list_page():
    devices_full = load_devices(DEFAULT_USER)
    # Context: list of dict(device_id: int, device_name: str, device_type: str, room: str, status: str)
    devices = []
    for d in devices_full:
        devices.append({
            'device_id': d['device_id'],
            'device_name': d['device_name'],
            'device_type': d['device_type'],
            'room': d['room'],
            'status': d['status']
        })
    return render_template('device_list.html', devices=devices)


@app.route('/device/add', methods=['GET', 'POST'])
def add_device_page():
    device_types = ['Light', 'Thermostat', 'Camera', 'Lock', 'Sensor', 'Appliance']
    roomslist = [r['room_name'] for r in load_rooms(DEFAULT_USER)]
    form_errors = {}

    if request.method == 'POST':
        device_name = request.form.get('device_name', '').strip()
        device_type = request.form.get('device_type', '')
        device_room = request.form.get('device_room', '')

        # Validate inputs
        if not device_name:
            form_errors['device_name'] = 'Device name is required.'
        if device_type not in device_types:
            form_errors['device_type'] = 'Invalid device type selected.'
        if device_room not in roomslist:
            form_errors['device_room'] = 'Invalid room selected.'

        if not form_errors:
            # Add new device
            devices = load_devices(DEFAULT_USER)
            next_id = max([d['device_id'] for d in devices], default=0) + 1
            new_device = {
                'username': DEFAULT_USER,
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
                'mode': '',
                'schedule_time': ''
            }
            devices.append(new_device)
            save_devices(devices, DEFAULT_USER)
            return redirect(url_for('device_list_page'))

    return render_template('add_device.html', device_types=device_types, rooms=roomslist, form_errors=form_errors)


@app.route('/device/control/<int:device_id>', methods=['GET', 'POST'])
def device_control_page(device_id):
    devices = load_devices(DEFAULT_USER)
    device = next((d for d in devices if d['device_id'] == device_id), None)
    if not device:
        return "Device not found", 404

    if request.method == 'POST':
        # Two possible POST actions: toggle power or save settings
        if 'power_toggle' in request.form:
            # Toggle power on/off
            device['power'] = 'off' if device['power'] == 'on' else 'on'
            # If device is powered off, status might be Offline?
            # Keep status as is - not specified to toggle status
        else:
            # Save settings
            # Save brightness, temperature, mode, schedule_time if present in form
            brightness_raw = request.form.get('brightness', '')
            temperature_raw = request.form.get('temperature', '')
            mode = request.form.get('mode', device['mode'])
            schedule_time = request.form.get('schedule_time', device['schedule_time'])

            # Parse brightness and temperature if numeric, else None
            brightness = int(brightness_raw) if brightness_raw.isdigit() else None
            temperature = int(temperature_raw) if temperature_raw.isdigit() else None

            if device['device_type'] == 'Light':
                device['brightness'] = brightness
            elif device['device_type'] == 'Thermostat':
                device['temperature'] = temperature
            # Update mode and schedule_time
            device['mode'] = mode
            device['schedule_time'] = schedule_time

        # Save updated device list
        save_devices(devices, DEFAULT_USER)
        # After POST redirect to GET to avoid form resubmission
        return redirect(url_for('device_control_page', device_id=device_id))

    # GET: render device control page with device info
    device_context = {
        'device_id': device['device_id'],
        'device_name': device['device_name'],
        'status': device['status'],
        'power': device['power'],
        'brightness': device['brightness'],
        'temperature': device['temperature'],
        'mode': device['mode'],
        'schedule_time': device['schedule_time'],
    }
    return render_template('device_control.html', device=device_context)


@app.route('/automation', methods=['GET', 'POST'])
def automation_rules_page():
    rules = load_automation_rules(DEFAULT_USER)
    devices = load_devices(DEFAULT_USER)
    # POST: Add new rule
    if request.method == 'POST':
        rule_name = request.form.get('rule_name', '').strip()
        trigger_type = request.form.get('trigger_type', '')
        trigger_value = request.form.get('trigger_value', '').strip()
        action_device_id_raw = request.form.get('action_device', '')
        action_type = request.form.get('action_type', '')

        form_errors = {}

        # Validate inputs
        if not rule_name:
            form_errors['rule_name'] = 'Rule name is required.'
        if trigger_type not in ['Time', 'Motion', 'Temperature']:
            form_errors['trigger_type'] = 'Invalid trigger type.'
        if not trigger_value:
            form_errors['trigger_value'] = 'Trigger value is required.'
        try:
            action_device_id = int(action_device_id_raw)
        except Exception:
            action_device_id = None
            form_errors['action_device'] = 'Invalid device selection.'
        if action_type not in ['Turn On', 'Turn Off', 'Set Brightness', 'Set Temperature']:
            form_errors['action_type'] = 'Invalid action type.'

        if not form_errors:
            # Generate next rule_id
            next_rule_id = max([r['rule_id'] for r in rules], default=0) + 1
            new_rule = {
                'username': DEFAULT_USER,
                'rule_id': next_rule_id,
                'rule_name': rule_name,
                'trigger_type': trigger_type,
                'trigger_value': trigger_value,
                'action_device_id': action_device_id,
                'action_type': action_type,
                'action_value': '',
                'enabled': True
            }
            rules.append(new_rule)
            save_automation_rules(rules, DEFAULT_USER)
            return redirect(url_for('automation_rules_page'))

        # If errors, render page with errors
        automation_rules_context = [{
            'rule_id': r['rule_id'],
            'rule_name': r['rule_name'],
            'trigger_type': r['trigger_type'],
            'trigger_value': r['trigger_value'],
            'action_device_id': r['action_device_id'],
            'action_type': r['action_type'],
            'enabled': r['enabled']
        } for r in rules]
        devices_context = [{'device_id': d['device_id'], 'device_name': d['device_name']} for d in devices]
        return render_template('automation.html', automation_rules=automation_rules_context, devices=devices_context, form_errors=form_errors)

    # GET
    automation_rules_context = [{
        'rule_id': r['rule_id'],
        'rule_name': r['rule_name'],
        'trigger_type': r['trigger_type'],
        'trigger_value': r['trigger_value'],
        'action_device_id': r['action_device_id'],
        'action_type': r['action_type'],
        'enabled': r['enabled']
    } for r in rules]
    devices_context = [{'device_id': d['device_id'], 'device_name': d['device_name']} for d in devices]
    return render_template('automation.html', automation_rules=automation_rules_context, devices=devices_context)


@app.route('/energy', methods=['GET', 'POST'])
def energy_report_page():
    energy_logs = load_energy_logs(DEFAULT_USER)
    devices = load_devices(DEFAULT_USER)
    # Map device_id to device_name
    device_name_map = {d['device_id']: d['device_name'] for d in devices}

    filtered_logs = energy_logs

    if request.method == 'POST':
        # Filter by date
        filter_date = request.form.get('date_filter', '')
        if filter_date:
            filtered_logs = [log for log in energy_logs if log['date'] == filter_date]

    # Compose logs with device names
    energy_logs_context = []
    total_consumption = 0.0
    for log in filtered_logs:
        device_name = device_name_map.get(log['device_id'], 'Unknown')
        energy_logs_context.append({
            'device_id': log['device_id'],
            'device_name': device_name,
            'date': log['date'],
            'consumption_kwh': log['consumption_kwh']
        })
        total_consumption += log['consumption_kwh']

    # Assume cost per kWh: 0.12 (example)
    total_cost = total_consumption * 0.12

    return render_template('energy_report.html', energy_logs=energy_logs_context, total_consumption=total_consumption, total_cost=total_cost)


@app.route('/activity', methods=['GET', 'POST'])
def activity_logs_page():
    activity_logs = load_activity_logs(DEFAULT_USER)
    devices = load_devices(DEFAULT_USER)
    device_name_map = {d['device_id']: d['device_name'] for d in devices}

    filtered_logs = activity_logs

    if request.method == 'POST':
        search_term = request.form.get('search_activity', '').strip().lower()
        if search_term:
            filtered_logs = [log for log in activity_logs
                             if (search_term in log['action'].lower() or
                                 search_term in log['details'].lower() or
                                 search_term in device_name_map.get(log['device_id'], '').lower())]

    activity_logs_context = []
    for log in filtered_logs:
        activity_logs_context.append({
            'timestamp': log['timestamp'],
            'device_id': log['device_id'],
            'device_name': device_name_map.get(log['device_id'], 'Unknown'),
            'action': log['action'],
            'details': log['details']
        })

    return render_template('activity_logs.html', activity_logs=activity_logs_context)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
