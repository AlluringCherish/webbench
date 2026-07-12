from flask import Flask, render_template, redirect, url_for, request, abort
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Utility functions for loading and saving data files

def load_users():
    users = []
    try:
        with open(os.path.join(DATA_DIR, 'users.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                fields = line.split('|')
                if len(fields) != 2:
                    continue
                user = {
                    'username': fields[0],
                    'email': fields[1],
                }
                users.append(user)
    except FileNotFoundError:
        pass
    return users


def load_devices():
    devices = []
    try:
        with open(os.path.join(DATA_DIR, 'devices.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                fields = line.split('|')
                if len(fields) != 13:
                    continue
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
                    'mode': fields[11],
                    'schedule_time': fields[12],
                }
                devices.append(device)
    except FileNotFoundError:
        pass
    return devices


def save_devices(devices):
    try:
        with open(os.path.join(DATA_DIR, 'devices.txt'), 'w', encoding='utf-8') as f:
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
                    d['mode'],
                    d['schedule_time'],
                ])
                f.write(line + '\n')
    except Exception:
        pass


def load_rooms():
    rooms = []
    try:
        with open(os.path.join(DATA_DIR, 'rooms.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                fields = line.split('|')
                if len(fields) != 3:
                    continue
                room = {
                    'username': fields[0],
                    'room_id': int(fields[1]),
                    'room_name': fields[2],
                }
                rooms.append(room)
    except FileNotFoundError:
        pass
    return rooms


def load_automation_rules():
    rules = []
    try:
        with open(os.path.join(DATA_DIR, 'automation_rules.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                fields = line.split('|')
                if len(fields) != 9:
                    continue
                rule = {
                    'username': fields[0],
                    'rule_id': int(fields[1]),
                    'rule_name': fields[2],
                    'trigger_type': fields[3],
                    'trigger_value': fields[4],
                    'action_device_id': int(fields[5]),
                    'action_type': fields[6],
                    'action_value': fields[7],
                    'enabled': True if fields[8].lower() == 'true' else False,
                }
                rules.append(rule)
    except FileNotFoundError:
        pass
    return rules


def save_automation_rules(rules):
    try:
        with open(os.path.join(DATA_DIR, 'automation_rules.txt'), 'w', encoding='utf-8') as f:
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
                    'true' if r['enabled'] else 'false',
                ])
                f.write(line + '\n')
    except Exception:
        pass


def load_energy_logs():
    energy_logs = []
    try:
        with open(os.path.join(DATA_DIR, 'energy_logs.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                fields = line.split('|')
                if len(fields) != 4:
                    continue
                log = {
                    'username': fields[0],
                    'device_id': int(fields[1]),
                    'date': fields[2],
                    'consumption_kwh': float(fields[3]),
                }
                energy_logs.append(log)
    except FileNotFoundError:
        pass
    return energy_logs


def load_activity_logs():
    activities = []
    try:
        with open(os.path.join(DATA_DIR, 'activity_logs.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                fields = line.split('|')
                if len(fields) != 5:
                    continue
                act = {
                    'username': fields[0],
                    'timestamp': fields[1],
                    'device_id': int(fields[2]),
                    'action': fields[3],
                    'details': fields[4],
                }
                activities.append(act)
    except FileNotFoundError:
        pass
    return activities


# Hardcoded current user
# Since no user authentication specified, use 'john_doe' as default user for all pages

CURRENT_USER = 'john_doe'


@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard_page'))


@app.route('/dashboard')
def dashboard_page():
    devices = [d for d in load_devices() if d['username'] == CURRENT_USER]
    rooms = [r for r in load_rooms() if r['username'] == CURRENT_USER]

    # Count devices
    total_devices = len(devices)
    active_devices = sum(1 for d in devices if d['status'] == 'Online')
    offline_devices = sum(1 for d in devices if d['status'] == 'Offline')

    # Device counts per room
    device_counts = {}
    for room in rooms:
        device_counts[room['room_name']] = sum(1 for d in devices if d['room'] == room['room_name'])

    return render_template(
        'dashboard.html',
        devices=devices,
        rooms=rooms,
        device_counts=device_counts
    )


@app.route('/devices')
def device_list_page():
    devices = [d for d in load_devices() if d['username'] == CURRENT_USER]

    return render_template('devices.html', devices=devices, user=CURRENT_USER)


@app.route('/devices/add', methods=['GET', 'POST'])
def add_device_page():
    rooms = [r for r in load_rooms() if r['username'] == CURRENT_USER]
    device_types = ['Light', 'Thermostat', 'Camera', 'Lock', 'Sensor', 'Appliance']

    if request.method == 'POST':
        # Process form data
        dname = request.form.get('device-name', '').strip()
        dtype = request.form.get('device-type', '').strip()
        droom = request.form.get('device-room', '').strip()

        # Validate required fields
        if not dname or not dtype or not droom:
            # Could flash or pass error, but spec does not mention, so we just re-render
            return render_template('add_device.html', rooms=rooms, device_types=device_types, user=CURRENT_USER)

        devices = load_devices()
        # Find max device_id for user to assign new unique ID
        user_devices = [d for d in devices if d['username'] == CURRENT_USER]
        max_id = max((d['device_id'] for d in user_devices), default=0)
        new_id = max_id + 1

        # Add new device with defaults
        new_device = {
            'username': CURRENT_USER,
            'device_id': new_id,
            'device_name': dname,
            'device_type': dtype,
            'room': droom,
            'brand': '',
            'model': '',
            'status': 'Offline',  # default status
            'power': 'off',
            'brightness': None,
            'temperature': None,
            'mode': '',
            'schedule_time': '',
        }

        devices.append(new_device)
        save_devices(devices)
        return redirect(url_for('device_list_page'))

    # GET
    return render_template('add_device.html', rooms=rooms, device_types=device_types, user=CURRENT_USER)


@app.route('/device/<int:device_id>', methods=['GET', 'POST'])
def device_control_page(device_id):
    devices = load_devices()
    device = next((d for d in devices if d['username'] == CURRENT_USER and d['device_id'] == device_id), None)
    if device is None:
        abort(404)

    if request.method == 'POST':
        form = request.form

        # Handle power toggle
        if 'power-toggle' in form:
            # Toggle power
            device['power'] = 'off' if device['power'] == 'on' else 'on'
            # Update status accordingly (assuming if power on then status online)
            device['status'] = 'Online' if device['power'] == 'on' else 'Offline'

        # Handle saving settings
        if 'save-settings-button' in form:
            # Save settings depending on device type
            # Brightness
            bright_val = form.get('brightness')
            if bright_val and bright_val.isdigit():
                device['brightness'] = int(bright_val)
            else:
                device['brightness'] = None

            # Temperature
            temp_val = form.get('temperature')
            if temp_val and temp_val.isdigit():
                device['temperature'] = int(temp_val)
            else:
                device['temperature'] = None

            # Mode
            mode_val = form.get('mode', '')
            device['mode'] = mode_val

            # Schedule Time
            schedule_val = form.get('schedule_time', '')
            device['schedule_time'] = schedule_val

        save_devices(devices)
        return redirect(url_for('device_control_page', device_id=device_id))

    # GET
    return render_template('device_control.html', device=device, user=CURRENT_USER)


@app.route('/automation', methods=['GET', 'POST'])
def automation_rules_page():
    rules = [r for r in load_automation_rules() if r['username'] == CURRENT_USER]
    devices = [d for d in load_devices() if d['username'] == CURRENT_USER]

    if request.method == 'POST':
        # Add new rule
        rname = request.form.get('rule-name', '').strip()
        trig_type = request.form.get('trigger-type', '').strip()
        trig_val = request.form.get('trigger-value', '').strip()
        action_device_id_str = request.form.get('action-device', '').strip()
        action_type = request.form.get('action-type', '').strip()

        if not rname or not trig_type or not trig_val or not action_device_id_str.isdigit() or not action_type:
            # Missing data, just re-render with existing context
            return render_template('automation.html', rules=rules, devices=devices, user=CURRENT_USER)

        action_device_id = int(action_device_id_str)

        # Generate new rule_id
        max_rule_id = max((r['rule_id'] for r in rules), default=0)
        new_rule_id = max_rule_id + 1

        new_rule = {
            'username': CURRENT_USER,
            'rule_id': new_rule_id,
            'rule_name': rname,
            'trigger_type': trig_type,
            'trigger_value': trig_val,
            'action_device_id': action_device_id,
            'action_type': action_type,
            'action_value': '',
            'enabled': True,
        }

        rules.append(new_rule)
        save_automation_rules(rules)

        return redirect(url_for('automation_rules_page'))

    # GET
    return render_template('automation.html', rules=rules, devices=devices, user=CURRENT_USER)


@app.route('/energy', methods=['GET', 'POST'])
def energy_report_page():
    energy_logs = [log for log in load_energy_logs() if log['username'] == CURRENT_USER]
    devices = [d for d in load_devices() if d['username'] == CURRENT_USER]

    date_filter = None
    if request.method == 'POST':
        date_filter = request.form.get('date-filter', '').strip()
        if date_filter:
            # Filter energy_logs by date
            energy_logs = [log for log in energy_logs if log['date'] == date_filter]

    total_consumption = sum(log['consumption_kwh'] for log in energy_logs)
    total_cost = total_consumption * 0.12  # Assume 0.12 $/kWh cost for example

    return render_template('energy.html', energy_logs=energy_logs, total_consumption=total_consumption,
                           total_cost=total_cost, user=CURRENT_USER)


@app.route('/activity', methods=['GET', 'POST'])
def activity_logs_page():
    activities = [a for a in load_activity_logs() if a['username'] == CURRENT_USER]

    if request.method == 'POST':
        search = request.form.get('search-activity', '').strip().lower()
        if search:
            activities = [a for a in activities 
                          if search in a['action'].lower() 
                          or search in a['details'].lower()]

    return render_template('activity.html', activities=activities, user=CURRENT_USER)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
