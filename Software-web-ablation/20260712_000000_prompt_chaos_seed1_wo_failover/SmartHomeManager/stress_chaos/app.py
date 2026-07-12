from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

# Assuming a single logged in user for scope, using 'john_doe' as current user
CURRENT_USER = 'john_doe'

# File paths
USERS_FILE = 'data/users.txt'
DEVICES_FILE = 'data/devices.txt'
ROOMS_FILE = 'data/rooms.txt'
AUTOMATION_RULES_FILE = 'data/automation_rules.txt'
ENERGY_LOGS_FILE = 'data/energy_logs.txt'
ACTIVITY_LOGS_FILE = 'data/activity_logs.txt'

# Utility functions for reading and writing data

def read_devices(username):
    devices = []
    try:
        with open(DEVICES_FILE, 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) >= 13 and parts[0] == username:
                    device = {
                        'username': parts[0],
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


def write_devices(devices):
    lines = []
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
        lines.append(line)
    with open(DEVICES_FILE, 'w') as f:
        f.write('\n'.join(lines) + '\n' if lines else '')


def read_rooms(username):
    rooms = []
    try:
        with open(ROOMS_FILE, 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) >= 3 and parts[0] == username:
                    room = {
                        'username': parts[0],
                        'room_id': int(parts[1]),
                        'room_name': parts[2]
                    }
                    rooms.append(room)
    except FileNotFoundError:
        pass
    return rooms


def read_automation_rules(username):
    rules = []
    try:
        with open(AUTOMATION_RULES_FILE, 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) >= 9 and parts[0] == username:
                    rule = {
                        'username': parts[0],
                        'rule_id': int(parts[1]),
                        'rule_name': parts[2],
                        'trigger_type': parts[3],
                        'trigger_value': parts[4],
                        'action_device_id': int(parts[5]),
                        'action_type': parts[6],
                        'action_value': parts[7],
                        'enabled': parts[8]
                    }
                    rules.append(rule)
    except FileNotFoundError:
        pass
    return rules


def write_automation_rules(rules):
    lines = []
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
            r['enabled']
        ])
        lines.append(line)
    with open(AUTOMATION_RULES_FILE, 'w') as f:
        f.write('\n'.join(lines) + '\n' if lines else '')


def read_energy_logs(username):
    logs = []
    try:
        with open(ENERGY_LOGS_FILE, 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) >= 4 and parts[0] == username:
                    log = {
                        'username': parts[0],
                        'device_id': int(parts[1]),
                        'date': parts[2],
                        'consumption_kwh': float(parts[3])
                    }
                    logs.append(log)
    except FileNotFoundError:
        pass
    return logs


def read_activity_logs(username):
    activities = []
    try:
        with open(ACTIVITY_LOGS_FILE, 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) >= 5 and parts[0] == username:
                    activity = {
                        'username': parts[0],
                        'timestamp': parts[1],
                        'device_id': int(parts[2]),
                        'action': parts[3],
                        'details': parts[4]
                    }
                    activities.append(activity)
    except FileNotFoundError:
        pass
    return activities


# Route implementations

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    devices = read_devices(CURRENT_USER)
    rooms = read_rooms(CURRENT_USER)
    # Prepare devices_summary dict
    total_devices = len(devices)
    active_devices = sum(1 for d in devices if d['status'] == 'Online')
    offline_devices = total_devices - active_devices

    devices_summary = {
        'total': total_devices,
        'active': active_devices,
        'offline': offline_devices
    }

    # Prepare list of rooms with device counts
    # room_name: count
    room_counts = {}
    for room in rooms:
        room_name = room['room_name']
        count = sum(1 for d in devices if d['room'] == room_name)
        room_counts[room_name] = count

    # Room list as list of dicts: {room_name: str, device_count:int}
    room_list = [{'room_name': r['room_name'], 'device_count': room_counts.get(r['room_name'], 0)} for r in rooms]

    return render_template('dashboard.html', devices_summary=devices_summary, rooms=room_list)


@app.route('/devices')
def device_list():
    devices = read_devices(CURRENT_USER)
    return render_template('devices.html', devices=devices)


@app.route('/device/add', methods=['GET', 'POST'])
def add_device():
    device_types = ['Light', 'Thermostat', 'Camera', 'Lock', 'Sensor', 'Appliance']
    rooms = [room['room_name'] for room in read_rooms(CURRENT_USER)]
    message = ''
    if request.method == 'POST':
        # Get form data
        device_name = request.form.get('device_name', '').strip()
        device_type = request.form.get('device_type', '')
        device_room = request.form.get('device_room', '')

        # Minimal validation
        if not device_name or device_type not in device_types or device_room not in rooms:
            message = 'Invalid input data. Please fill all fields correctly.'
        else:
            devices = read_devices(CURRENT_USER)
            # Generate new device_id as max + 1 or 1 if none
            max_id = max([d['device_id'] for d in devices], default=0)
            new_id = max_id + 1
            new_device = {
                'username': CURRENT_USER,
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
            write_devices(devices)
            message = 'Device added successfully.'

    return render_template('add_device.html', device_types=device_types, rooms=rooms, message=message)


@app.route('/device/<int:device_id>', methods=['GET', 'POST'])
def device_control(device_id):
    devices = read_devices(CURRENT_USER)
    device = None
    for d in devices:
        if d['device_id'] == device_id:
            device = d
            break
    
    if device is None:
        # Device not found, redirect to device list
        return redirect(url_for('device_list'))

    message = ''
    if request.method == 'POST':
        # Update device parameters with form data
        # For simplicity we try to update power, brightness, temperature, mode, schedule_time
        power = request.form.get('power', device['power'])
        brightness = request.form.get('brightness', device.get('brightness',''))
        temperature = request.form.get('temperature', device.get('temperature',''))
        mode = request.form.get('mode', device.get('mode',''))
        schedule_time = request.form.get('schedule_time', device.get('schedule_time',''))

        # Validate power value
        if power not in ['on', 'off']:
            message = 'Invalid power state.'
        else:
            device['power'] = power
            device['brightness'] = brightness
            device['temperature'] = temperature
            device['mode'] = mode
            device['schedule_time'] = schedule_time
            # Update device status based on power
            device['status'] = 'Online' if power == 'on' else 'Offline'

            # Save devices back
            write_devices(devices)
            message = 'Device updated successfully.'

    return render_template('device_control.html', device=device, message=message)


@app.route('/automation', methods=['GET', 'POST'])
def automation_rules():
    rules = read_automation_rules(CURRENT_USER)
    devices = read_devices(CURRENT_USER)
    message = ''

    if request.method == 'POST':
        # Get form data for new rule
        rule_name = request.form.get('rule_name', '').strip()
        trigger_type = request.form.get('trigger_type', '')
        trigger_value = request.form.get('trigger_value', '').strip()
        action_device_id = request.form.get('action_device', '')
        action_type = request.form.get('action_type', '')

        valid_trigger_types = ['Time', 'Motion', 'Temperature']
        valid_action_types = ['Turn On', 'Turn Off', 'Set Brightness', 'Set Temperature']

        # Validation
        if not rule_name or trigger_type not in valid_trigger_types or action_type not in valid_action_types:
            message = 'Invalid input data. Please fill all fields correctly.'
        else:
            # Validate device id
            try:
                action_device_id_int = int(action_device_id)
            except:
                action_device_id_int = -1

            if not any(d['device_id'] == action_device_id_int for d in devices):
                message = 'Invalid device selected.'
            else:
                # Generate new rule ID
                max_id = max([r['rule_id'] for r in rules], default=0)
                new_id = max_id + 1

                new_rule = {
                    'username': CURRENT_USER,
                    'rule_id': new_id,
                    'rule_name': rule_name,
                    'trigger_type': trigger_type,
                    'trigger_value': trigger_value,
                    'action_device_id': action_device_id_int,
                    'action_type': action_type,
                    'action_value': '',
                    'enabled': 'true'
                }

                rules.append(new_rule)
                write_automation_rules(rules)
                message = 'Automation rule added successfully.'

    return render_template('automation.html', rules=rules, devices=devices, message=message)


@app.route('/energy', methods=['GET', 'POST'])
def energy_report():
    energy_logs = read_energy_logs(CURRENT_USER)
    filter_date = ''
    filtered_logs = energy_logs

    if request.method == 'POST':
        filter_date = request.form.get('date_filter', '')
        if filter_date:
            filtered_logs = [log for log in energy_logs if log['date'] == filter_date]

    # Calculate summary
    total_consumption = sum(log['consumption_kwh'] for log in filtered_logs)
    average_cost_per_kwh = 0.12  # Assuming a fixed cost for example
    total_cost = total_consumption * average_cost_per_kwh

    summary = {
        'total_consumption': total_consumption,
        'total_cost': total_cost
    }

    return render_template('energy_report.html', energy_logs=filtered_logs, summary=summary, filter_date=filter_date)


@app.route('/activity', methods=['GET', 'POST'])
def activity_logs():
    activities = read_activity_logs(CURRENT_USER)
    search_query = ''
    filtered_activities = activities

    if request.method == 'POST':
        search_query = request.form.get('search_activity', '').strip().lower()
        if search_query:
            filtered_activities = [activity for activity in activities if 
                                   search_query in activity['action'].lower() or
                                   search_query in activity['details'].lower()]

    return render_template('activity_logs.html', activities=filtered_activities, search_query=search_query)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
