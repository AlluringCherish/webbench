from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_PATH = 'data/'

# Helper functions to load data from files

def load_users():
    users = []
    try:
        with open(DATA_PATH + 'users.txt', 'r', encoding='utf-8') as f:
            for line in f:
                username, email = line.strip().split('|')
                users.append({'username': username, 'email': email})
    except FileNotFoundError:
        pass
    return users


def load_devices():
    devices = []
    try:
        with open(DATA_PATH + 'devices.txt', 'r', encoding='utf-8') as f:
            for line in f:
                data = line.strip().split('|')
                if len(data) != 13:
                    continue
                username = data[0]
                device_id = int(data[1])
                device_name = data[2]
                device_type = data[3]
                room = data[4]
                brand = data[5]
                model = data[6]
                status = data[7]
                power = data[8]

                brightness = None
                if data[9] != '':
                    try:
                        brightness = int(data[9])
                    except ValueError:
                        brightness = None

                temperature = None
                if data[10] != '':
                    try:
                        temperature = int(data[10])
                    except ValueError:
                        temperature = None

                mode = data[11]
                schedule_time = data[12]

                devices.append({
                    'username': username,
                    'device_id': device_id,
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
                })
    except FileNotFoundError:
        pass
    return devices


def load_rooms():
    rooms = []
    try:
        with open(DATA_PATH + 'rooms.txt', 'r', encoding='utf-8') as f:
            for line in f:
                data = line.strip().split('|')
                if len(data) != 3:
                    continue
                username = data[0]
                room_id = int(data[1])
                room_name = data[2]
                rooms.append({'username': username, 'room_id': room_id, 'room_name': room_name})
    except FileNotFoundError:
        pass
    return rooms


def load_automation_rules():
    rules = []
    try:
        with open(DATA_PATH + 'automation_rules.txt', 'r', encoding='utf-8') as f:
            for line in f:
                data = line.strip().split('|')
                if len(data) != 9:
                    continue
                username = data[0]
                rule_id = int(data[1])
                rule_name = data[2]
                trigger_type = data[3]
                trigger_value = data[4]
                action_device_id = int(data[5])
                action_type = data[6]
                action_value = data[7]
                enabled = data[8].lower() == 'true'
                rules.append({
                    'username': username,
                    'rule_id': rule_id,
                    'rule_name': rule_name,
                    'trigger_type': trigger_type,
                    'trigger_value': trigger_value,
                    'action_device_id': action_device_id,
                    'action_type': action_type,
                    'action_value': action_value,
                    'enabled': enabled
                })
    except FileNotFoundError:
        pass
    return rules


def load_energy_logs():
    energy_logs = []
    try:
        with open(DATA_PATH + 'energy_logs.txt', 'r', encoding='utf-8') as f:
            for line in f:
                data = line.strip().split('|')
                if len(data) != 4:
                    continue
                username = data[0]
                device_id = int(data[1])
                date = data[2]
                try:
                    consumption_kwh = float(data[3])
                except ValueError:
                    consumption_kwh = 0.0
                energy_logs.append({'username': username, 'device_id': device_id, 'date': date, 'consumption_kwh': consumption_kwh})
    except FileNotFoundError:
        pass
    return energy_logs


def load_activity_logs():
    activities = []
    try:
        with open(DATA_PATH + 'activity_logs.txt', 'r', encoding='utf-8') as f:
            for line in f:
                data = line.strip().split('|')
                if len(data) != 5:
                    continue
                username = data[0]
                timestamp = data[1]
                device_id = int(data[2])
                action = data[3]
                details = data[4]
                activities.append({'username': username, 'timestamp': timestamp, 'device_id': device_id, 'action': action, 'details': details})
    except FileNotFoundError:
        pass
    return activities


# Helper function to save devices (overwrite entire file)

def save_devices(devices):
    lines = []
    for d in devices:
        brightness_str = str(d['brightness']) if d['brightness'] is not None else ''
        temperature_str = str(d['temperature']) if d['temperature'] is not None else ''
        stime = d['schedule_time'] if d['schedule_time'] else ''
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
            brightness_str,
            temperature_str,
            d['mode'],
            stime
        ])
        lines.append(line)
    with open(DATA_PATH + 'devices.txt', 'w', encoding='utf-8') as f:
        for line in lines:
            f.write(line + '\n')


# Helper function to save automation rules (overwrite entire file)

def save_automation_rules(rules):
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
    with open(DATA_PATH + 'automation_rules.txt', 'w', encoding='utf-8') as f:
        for line in lines:
            f.write(line + '\n')


# Helper function to save energy logs (overwrite entire file)

def save_energy_logs(energy_logs):
    lines = []
    for e in energy_logs:
        line = '|'.join([
            e['username'],
            str(e['device_id']),
            e['date'],
            f"{e['consumption_kwh']:.2f}"
        ])
        lines.append(line)
    with open(DATA_PATH + 'energy_logs.txt', 'w', encoding='utf-8') as f:
        for line in lines:
            f.write(line + '\n')


# Helper function to save activity logs (overwrite entire file)

def save_activity_logs(activities):
    lines = []
    for a in activities:
        line = '|'.join([
            a['username'],
            a['timestamp'],
            str(a['device_id']),
            a['action'],
            a['details']
        ])
        lines.append(line)
    with open(DATA_PATH + 'activity_logs.txt', 'w', encoding='utf-8') as f:
        for line in lines:
            f.write(line + '\n')


# Helper to generate next device_id for a user

def next_device_id(username):
    devices = load_devices()
    user_devices = [d for d in devices if d['username'] == username]
    if not user_devices:
        return 1
    return max(d['device_id'] for d in user_devices) + 1


# Helper to generate next rule_id for a user

def next_rule_id(username):
    rules = load_automation_rules()
    user_rules = [r for r in rules if r['username'] == username]
    if not user_rules:
        return 1
    return max(r['rule_id'] for r in user_rules) + 1


@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard_page'))


@app.route('/dashboard')
def dashboard_page():
    # For the sake of example, assume a fixed user to display: 'john_doe'
    user = 'john_doe'
    devices = load_devices()
    rooms = load_rooms()

    user_devices = [d for d in devices if d['username'] == user]
    user_rooms = [r for r in rooms if r['username'] == user]

    # Devices summary
    total_devices = len(user_devices)
    active_devices = sum(1 for d in user_devices if d['status'] == 'Online')
    offline_devices = total_devices - active_devices
    devices_summary = {
        'total': total_devices,
        'active': active_devices,
        'offline': offline_devices
    }

    # Rooms overview - count devices per room
    rooms_overview = []
    for room in user_rooms:
        count = sum(1 for d in user_devices if d['room'] == room['room_name'])
        rooms_overview.append({'room_name': room['room_name'], 'device_count': count})

    return render_template('dashboard.html', devices_summary=devices_summary, rooms_overview=rooms_overview)


@app.route('/devices')
def device_list_page():
    # Assume fixed user 'john_doe'
    user = 'john_doe'
    devices = [d for d in load_devices() if d['username'] == user]
    return render_template('devices.html', devices=devices, user=user)


@app.route('/device/add', methods=['GET', 'POST'])
def add_device_page():
    user = 'john_doe'
    device_types = ['Light', 'Thermostat', 'Camera', 'Lock', 'Sensor', 'Appliance']
    rooms = [r['room_name'] for r in load_rooms() if r['username'] == user]
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
        if device_room not in rooms:
            form_errors['device_room'] = 'Invalid room selected.'

        if not form_errors:
            devices = load_devices()
            new_device_id = next_device_id(user)
            new_device = {
                'username': user,
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
                'mode': '',
                'schedule_time': ''
            }
            devices.append(new_device)
            save_devices(devices)
            return redirect(url_for('device_list_page'))

    return render_template('add_device.html', device_types=device_types, rooms=rooms, form_errors=form_errors)


@app.route('/device/control/<int:device_id>', methods=['GET', 'POST'])
def device_control_page(device_id):
    user = 'john_doe'
    devices = load_devices()
    device = None
    for d in devices:
        if d['username'] == user and d['device_id'] == device_id:
            device = d
            break

    if not device:
        return "Device not found", 404

    form_errors = {}

    if request.method == 'POST':
        # Handling power toggle or settings update
        new_power = request.form.get('power')
        new_brightness = request.form.get('brightness')
        new_temperature = request.form.get('temperature')
        new_mode = request.form.get('mode')

        # Validate and apply changes based on device type
        if new_power:
            if new_power.lower() in ['on', 'off']:
                device['power'] = new_power.lower()
            else:
                form_errors['power'] = 'Invalid power value.'

        if device['device_type'] == 'Light' and new_brightness is not None:
            try:
                brightness_val = int(new_brightness)
                if 0 <= brightness_val <= 100:
                    device['brightness'] = brightness_val
                else:
                    form_errors['brightness'] = 'Brightness must be between 0 and 100.'
            except ValueError:
                form_errors['brightness'] = 'Brightness must be an integer.'

        if device['device_type'] == 'Thermostat' and new_temperature is not None:
            try:
                temp_val = int(new_temperature)
                device['temperature'] = temp_val
            except ValueError:
                form_errors['temperature'] = 'Temperature must be an integer.'

        if new_mode is not None:
            device['mode'] = new_mode

        if not form_errors:
            save_devices(devices)
            return redirect(url_for('device_control_page', device_id=device_id))

    return render_template('device_control.html', device=device, form_errors=form_errors)


@app.route('/automation', methods=['GET', 'POST'])
def automation_rules_page():
    user = 'john_doe'
    rules = [r for r in load_automation_rules() if r['username'] == user]
    devices = [d for d in load_devices() if d['username'] == user]
    form_errors = {}

    if request.method == 'POST':
        rule_name = request.form.get('rule_name', '').strip()
        trigger_type = request.form.get('trigger_type')
        trigger_value = request.form.get('trigger_value', '').strip()
        action_device_id_str = request.form.get('action_device')
        action_type = request.form.get('action_type')

        # Validate inputs
        if not rule_name:
            form_errors['rule_name'] = 'Rule name is required.'
        if trigger_type not in ['Time', 'Motion', 'Temperature']:
            form_errors['trigger_type'] = 'Invalid trigger type.'
        if not trigger_value:
            form_errors['trigger_value'] = 'Trigger value is required.'

        try:
            action_device_id = int(action_device_id_str)
            if not any(d['device_id'] == action_device_id for d in devices):
                form_errors['action_device'] = 'Selected device does not exist.'
        except (ValueError, TypeError):
            form_errors['action_device'] = 'Invalid device selected.'

        action_types_valid = ['Turn On', 'Turn Off', 'Set Brightness', 'Set Temperature']
        if action_type not in action_types_valid:
            form_errors['action_type'] = 'Invalid action type.'

        action_value = request.form.get('action_value', '').strip()

        if action_type in ['Set Brightness', 'Set Temperature'] and not action_value:
            form_errors['action_value'] = 'Action value is required for this action type.'

        if not form_errors:
            rules = load_automation_rules()
            new_rule_id = next_rule_id(user)
            new_rule = {
                'username': user,
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

    return render_template('automation.html', rules=rules, devices=devices, form_errors=form_errors)


@app.route('/energy', methods=['GET', 'POST'])
def energy_report_page():
    user = 'john_doe'
    energy_logs = [e for e in load_energy_logs() if e['username'] == user]
    devices = [d for d in load_devices() if d['username'] == user]

    filter_date = ''
    if request.method == 'POST':
        filter_date = request.form.get('date_filter', '').strip()
        if filter_date:
            energy_logs = [e for e in energy_logs if e['date'] == filter_date]

    # Summarize energy consumption
    total_consumption = sum(e['consumption_kwh'] for e in energy_logs)
    # Assume cost estimate 0.12 currency per kWh
    cost_estimate = total_consumption * 0.12

    energy_summary = {
        'total_consumption': round(total_consumption, 2),
        'cost_estimate': round(cost_estimate, 2)
    }

    return render_template('energy.html', energy_data=energy_logs, energy_summary=energy_summary, filter_date=filter_date)


@app.route('/activity', methods=['GET', 'POST'])
def activity_logs_page():
    user = 'john_doe'
    activities = [a for a in load_activity_logs() if a['username'] == user]

    search_query = ''
    if request.method == 'POST':
        search_query = request.form.get('search_query', '').strip().lower()
        if search_query:
            activities = [a for a in activities if
                          search_query in a['action'].lower() or
                          search_query in a['details'].lower()]

    return render_template('activity.html', activities=activities, search_query=search_query)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
