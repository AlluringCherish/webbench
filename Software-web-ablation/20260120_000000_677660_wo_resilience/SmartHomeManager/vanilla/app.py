from flask import Flask, render_template, redirect, url_for, request
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

# Utility data file paths
USERS_FILE = 'data/users.txt'
DEVICES_FILE = 'data/devices.txt'
ROOMS_FILE = 'data/rooms.txt'
AUTOMATION_RULES_FILE = 'data/automation_rules.txt'
ENERGY_LOGS_FILE = 'data/energy_logs.txt'
ACTIVITY_LOGS_FILE = 'data/activity_logs.txt'

# Helper functions to load and save data

def load_users():
    users = []
    if not os.path.exists(USERS_FILE):
        return users
    with open(USERS_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) != 2:
                continue
            user = {
                'username': parts[0],
                'email': parts[1]
            }
            users.append(user)
    return users


def load_devices(username_filter=None):
    devices = []
    if not os.path.exists(DEVICES_FILE):
        return devices
    with open(DEVICES_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) != 13:
                continue
            username = parts[0]
            if username_filter and username != username_filter:
                continue
            try:
                device_id = int(parts[1])
            except ValueError:
                continue
            device_name = parts[2]
            device_type = parts[3]
            room = parts[4]
            brand = parts[5]
            model = parts[6]
            status = parts[7]
            power = parts[8]
            brightness = parts[9]
            brightness_val = int(brightness) if brightness.isdigit() else None
            temperature = parts[10]
            temperature_val = int(temperature) if temperature.isdigit() else None
            mode = parts[11]
            schedule_time = parts[12]
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
                'brightness': brightness_val,
                'temperature': temperature_val,
                'mode': mode,
                'schedule_time': schedule_time
            })
    return devices


def save_devices(devices):
    with open(DEVICES_FILE, 'w', encoding='utf-8') as f:
        for d in devices:
            brightness_str = str(d['brightness']) if d['brightness'] is not None else ''
            temperature_str = str(d['temperature']) if d['temperature'] is not None else ''
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
                d['schedule_time']
            ])
            f.write(line + '\n')


def load_rooms(username_filter=None):
    rooms = []
    if not os.path.exists(ROOMS_FILE):
        return rooms
    with open(ROOMS_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) != 3:
                continue
            username = parts[0]
            if username_filter and username != username_filter:
                continue
            try:
                room_id = int(parts[1])
            except ValueError:
                continue
            room_name = parts[2]
            rooms.append({
                'username': username,
                'room_id': room_id,
                'room_name': room_name
            })
    return rooms


def load_automation_rules(username_filter=None):
    rules = []
    if not os.path.exists(AUTOMATION_RULES_FILE):
        return rules
    with open(AUTOMATION_RULES_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) != 9:
                continue
            username = parts[0]
            if username_filter and username != username_filter:
                continue
            try:
                rule_id = int(parts[1])
            except ValueError:
                continue
            rule_name = parts[2]
            trigger_type = parts[3]
            trigger_value = parts[4]
            try:
                action_device_id = int(parts[5])
            except ValueError:
                continue
            action_type = parts[6]
            action_value = parts[7]
            enabled_raw = parts[8].lower()
            enabled = True if enabled_raw == 'true' else False
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
    return rules


def save_automation_rules(rules):
    with open(AUTOMATION_RULES_FILE, 'w', encoding='utf-8') as f:
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
            f.write(line + '\n')


def load_energy_logs(username_filter=None, date_filter=None):
    logs = []
    if not os.path.exists(ENERGY_LOGS_FILE):
        return logs
    with open(ENERGY_LOGS_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) != 4:
                continue
            username = parts[0]
            if username_filter and username != username_filter:
                continue
            try:
                device_id = int(parts[1])
            except ValueError:
                continue
            date = parts[2]
            if date_filter and date != date_filter:
                continue
            try:
                consumption_kwh = float(parts[3])
            except ValueError:
                continue
            logs.append({
                'username': username,
                'device_id': device_id,
                'date': date,
                'consumption_kwh': consumption_kwh
            })
    return logs


def load_activity_logs(username_filter=None, search_query=None):
    activities = []
    if not os.path.exists(ACTIVITY_LOGS_FILE):
        return activities
    with open(ACTIVITY_LOGS_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) != 5:
                continue
            username = parts[0]
            if username_filter and username != username_filter:
                continue
            timestamp = parts[1]
            try:
                device_id = int(parts[2])
            except ValueError:
                continue
            action = parts[3]
            details = parts[4]
            # If search query provided, filter by presence in action or details (case insensitive)
            if search_query:
                sq = search_query.lower()
                if sq not in action.lower() and sq not in details.lower():
                    continue
            activities.append({
                'username': username,
                'timestamp': timestamp,
                'device_id': device_id,
                'action': action,
                'details': details
            })
    return activities

# Assumption: We pick a default user to display data for demonstration
# In real app, user management and login would determine current user
DEFAULT_USER = 'john_doe'


# Route: / redirects to /dashboard
@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard_page'))


# Route: /dashboard [GET]
@app.route('/dashboard')
def dashboard_page():
    user = DEFAULT_USER

    devices = load_devices(username_filter=user)
    rooms = load_rooms(username_filter=user)

    # Calculate device counts: total, active(online), offline
    total_devices = len(devices)
    active_devices = sum(1 for d in devices if d['status'] == 'Online')
    offline_devices = total_devices - active_devices

    # Count devices per room
    device_counts = {}
    for room in rooms:
        count = sum(1 for d in devices if d['room'] == room['room_name'])
        device_counts[room['room_name']] = count

    return render_template('dashboard.html', devices=devices, rooms=rooms, device_counts=device_counts)


# Route: /devices [GET]
@app.route('/devices')
def device_list_page():
    user = DEFAULT_USER
    devices = load_devices(username_filter=user)
    return render_template('devices.html', devices=devices, user=user)


# Route: /devices/add [GET, POST]
@app.route('/devices/add', methods=['GET', 'POST'])
def add_device_page():
    user = DEFAULT_USER
    rooms = load_rooms(username_filter=user)
    device_types = ["Light", "Thermostat", "Camera", "Lock", "Sensor", "Appliance"]

    if request.method == 'POST':
        # Read form data
        device_name = request.form.get('device-name', '').strip()
        device_type = request.form.get('device-type', '')
        device_room = request.form.get('device-room', '')

        # Validate inputs: Non-empty device_name, device_type in allowed, device_room in user's rooms
        valid_device_type = device_type in device_types
        valid_room = any(room['room_name'] == device_room for room in rooms)

        if device_name and valid_device_type and valid_room:
            # Load all devices for this user to find max device_id
            devices = load_devices(username_filter=user)
            max_device_id = max((d['device_id'] for d in devices), default=0)
            new_device_id = max_device_id + 1

            # Prepare new device record with defaults
            new_device = {
                'username': user,
                'device_id': new_device_id,
                'device_name': device_name,
                'device_type': device_type,
                'room': device_room,
                'brand': '',
                'model': '',
                'status': 'Offline',  # default offline
                'power': 'off',
                'brightness': None,
                'temperature': None,
                'mode': '',
                'schedule_time': ''
            }

            devices.append(new_device)
            save_devices(devices)

            # After adding device redirect to /devices
            return redirect(url_for('device_list_page'))

    return render_template('add_device.html', rooms=rooms, device_types=device_types, user=user)


# Route: /device/<int:device_id> [GET, POST]
@app.route('/device/<int:device_id>', methods=['GET', 'POST'])
def device_control_page(device_id):
    user = DEFAULT_USER
    devices = load_devices(username_filter=user)
    device = next((d for d in devices if d['device_id'] == device_id), None)

    if not device:
        # Device not found or not owned by user - could render 404 or redirect
        # We'll redirect to devices list
        return redirect(url_for('device_list_page'))

    if request.method == 'POST':
        # We expect ability to toggle power, and save settings
        # Toggle power can be done by changing 'power' field
        # Save settings can include brightness, temperature, mode, schedule_time

        # Detect toggle power button pressed or settings saved
        # We'll check form fields for new values
        power_toggle = request.form.get('power-toggle')
        if power_toggle == 'toggle':
            # Toggle power between 'on' and 'off'
            device['power'] = 'off' if device['power'] == 'on' else 'on'

        # Update other fields from form if present
        device_name = request.form.get('device-name', device['device_name']).strip()
        status = device['status']  # Status remains as is (Online/Offline) unless logic updates

        device['device_name'] = device_name if device_name else device['device_name']

        # brightness
        brightness_str = request.form.get('brightness', '')
        if brightness_str.isdigit():
            device['brightness'] = int(brightness_str)
        # temperature
        temperature_str = request.form.get('temperature', '')
        if temperature_str.isdigit():
            device['temperature'] = int(temperature_str)

        # mode
        mode = request.form.get('mode', '')
        if mode is not None:
            device['mode'] = mode

        # schedule_time
        schedule_time = request.form.get('schedule_time', '')
        if schedule_time is not None:
            device['schedule_time'] = schedule_time

        # Save updated devices data
        save_devices(devices)

        # Stay on the same page after POST
        return redirect(url_for('device_control_page', device_id=device_id))

    return render_template('device_control.html', device=device, device_id=device_id)


# Route: /automation [GET, POST]
@app.route('/automation', methods=['GET', 'POST'])
def automation_rules_page():
    user = DEFAULT_USER
    rules = load_automation_rules(username_filter=user)
    devices = load_devices(username_filter=user)

    if request.method == 'POST':
        # Add automation rule
        rule_name = request.form.get('rule-name', '').strip()
        trigger_type = request.form.get('trigger-type', '')
        trigger_value = request.form.get('trigger-value', '').strip()
        action_device_id_str = request.form.get('action-device', '')
        action_type = request.form.get('action-type', '')
        action_value = request.form.get('action-value', '') or ''

        # Validate inputs
        valid_trigger_types = ['Time', 'Motion', 'Temperature']
        valid_action_types = ['Turn On', 'Turn Off', 'Set Brightness', 'Set Temperature']
        try:
            action_device_id = int(action_device_id_str)
        except (ValueError, TypeError):
            action_device_id = None

        # Check trigger_type and action_type validity
        if (rule_name and
            trigger_type in valid_trigger_types and
            trigger_value and
            action_device_id in [d['device_id'] for d in devices] and
            action_type in valid_action_types):
            # Compute next rule_id
            max_rule_id = max((r['rule_id'] for r in rules), default=0)
            new_rule_id = max_rule_id + 1

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

    return render_template('automation.html', rules=rules, devices=devices, user=user)


# Route: /energy [GET, POST]
@app.route('/energy', methods=['GET', 'POST'])
def energy_report_page():
    user = DEFAULT_USER
    selected_date = None

    if request.method == 'POST':
        selected_date = request.form.get('date-filter', '')
        if selected_date == '':
            selected_date = None

    energy_data = load_energy_logs(username_filter=user, date_filter=selected_date)

    total_consumption = sum(entry['consumption_kwh'] for entry in energy_data)

    # For example cost calculation, assume static cost rate 0.12$/kWh
    cost_per_kwh = 0.12
    total_cost = total_consumption * cost_per_kwh

    return render_template('energy.html', energy_data=energy_data, total_consumption=total_consumption, total_cost=total_cost, user=user)


# Route: /activity [GET, POST]
@app.route('/activity', methods=['GET', 'POST'])
def activity_logs_page():
    user = DEFAULT_USER
    search_query = None
    if request.method == 'POST':
        search_query = request.form.get('search-activity', '').strip()
        if search_query == '':
            search_query = None

    activities = load_activity_logs(username_filter=user, search_query=search_query)
    return render_template('activity.html', activities=activities, user=user)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
