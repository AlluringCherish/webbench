from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

# Data file paths
USERS_FILE = 'data/users.txt'
DEVICES_FILE = 'data/devices.txt'
ROOMS_FILE = 'data/rooms.txt'
AUTOMATION_RULES_FILE = 'data/automation_rules.txt'
ENERGY_LOGS_FILE = 'data/energy_logs.txt'
ACTIVITY_LOGS_FILE = 'data/activity_logs.txt'

# The username is assumed for demo as no auth is specified
CURRENT_USER = 'john_doe'


# Utility functions to load data

def load_devices(username):
    devices = []
    try:
        with open(DEVICES_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if parts[0] == username:
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
                        'brightness': int(parts[9]) if parts[9].isdigit() else None,
                        'temperature': int(parts[10]) if parts[10].isdigit() else None,
                        'mode': parts[11] if parts[11] != '' else None,
                        'schedule_time': parts[12] if parts[12] != '' else None
                    }
                    devices.append(device)
    except Exception:
        pass
    return devices


def load_rooms(username):
    rooms = []
    try:
        with open(ROOMS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if parts[0] == username:
                    room = {
                        'username': parts[0],
                        'room_id': int(parts[1]),
                        'room_name': parts[2]
                    }
                    rooms.append(room)
    except Exception:
        pass
    return rooms


def load_automation_rules(username):
    rules = []
    try:
        with open(AUTOMATION_RULES_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if parts[0] == username:
                    rule = {
                        'username': parts[0],
                        'rule_id': int(parts[1]),
                        'rule_name': parts[2],
                        'trigger_type': parts[3],
                        'trigger_value': parts[4],
                        'action_device_id': int(parts[5]),
                        'action_type': parts[6],
                        'action_value': parts[7] if parts[7] != '' else None,
                        'enabled': parts[8].lower() == 'true'
                    }
                    rules.append(rule)
    except Exception:
        pass
    return rules


def load_energy_logs(username):
    energy_logs = []
    try:
        with open(ENERGY_LOGS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if parts[0] == username:
                    log = {
                        'username': parts[0],
                        'device_id': int(parts[1]),
                        'date': parts[2],
                        'consumption_kwh': float(parts[3])
                    }
                    energy_logs.append(log)
    except Exception:
        pass
    return energy_logs


def load_activity_logs(username):
    activity_logs = []
    try:
        with open(ACTIVITY_LOGS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if parts[0] == username:
                    log = {
                        'username': parts[0],
                        'timestamp': parts[1],
                        'device_id': int(parts[2]),
                        'action': parts[3],
                        'details': parts[4]
                    }
                    activity_logs.append(log)
    except Exception:
        pass
    return activity_logs


def save_devices(devices, username):
    # Save devices to DEVICES_FILE overwriting all devices of username and appending other users
    lines_other_users = []
    try:
        with open(DEVICES_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                if not line.startswith(username + '|'):
                    lines_other_users.append(line.strip())
    except Exception:
        pass

    new_lines = []
    for d in devices:
        brightness_str = str(d['brightness']) if d['brightness'] is not None else ''
        temperature_str = str(d['temperature']) if d['temperature'] is not None else ''
        mode_str = d['mode'] if d['mode'] is not None else ''
        schedule_time_str = d['schedule_time'] if d['schedule_time'] is not None else ''

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
            mode_str,
            schedule_time_str
        ])
        new_lines.append(line)

    try:
        with open(DEVICES_FILE, 'w', encoding='utf-8') as f:
            for line in lines_other_users + new_lines:
                f.write(line + '\n')
    except Exception:
        pass


def save_automation_rules(rules, username):
    # Save automation rules to AUTOMATION_RULES_FILE overwriting all rules of username and append others
    lines_other_users = []
    try:
        with open(AUTOMATION_RULES_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                if not line.startswith(username + '|'):
                    lines_other_users.append(line.strip())
    except Exception:
        pass

    new_lines = []
    for r in rules:
        action_value_str = r['action_value'] if r['action_value'] is not None else ''
        enabled_str = 'true' if r['enabled'] else 'false'
        line = '|'.join([
            r['username'],
            str(r['rule_id']),
            r['rule_name'],
            r['trigger_type'],
            r['trigger_value'],
            str(r['action_device_id']),
            r['action_type'],
            action_value_str,
            enabled_str
        ])
        new_lines.append(line)

    try:
        with open(AUTOMATION_RULES_FILE, 'w', encoding='utf-8') as f:
            for line in lines_other_users + new_lines:
                f.write(line + '\n')
    except Exception:
        pass


def get_next_device_id(devices):
    if not devices:
        return 1
    return max(d['device_id'] for d in devices) + 1


def get_next_rule_id(rules):
    if not rules:
        return 1
    return max(r['rule_id'] for r in rules) + 1


@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard_page'))


@app.route('/dashboard')
def dashboard_page():
    devices = load_devices(CURRENT_USER)
    rooms = load_rooms(CURRENT_USER)

    total_devices = len(devices)
    active_devices = sum(1 for d in devices if d['status'].lower() == 'online')
    offline_devices = total_devices - active_devices

    # Prepare rooms with device counts
    room_counts = []
    for room in rooms:
        count = sum(1 for d in devices if d['room'] == room['room_name'])
        room_counts.append({'room_name': room['room_name'], 'device_count': count})

    devices_summary = {
        'total': total_devices,
        'active': active_devices,
        'offline': offline_devices
    }

    return render_template('dashboard.html', devices_summary=devices_summary, rooms=room_counts)


@app.route('/devices')
def device_list_page():
    devices = load_devices(CURRENT_USER)
    devices_for_render = []
    for d in devices:
        devices_for_render.append({
            'device_id': d['device_id'],
            'device_name': d['device_name'],
            'device_type': d['device_type'],
            'room': d['room'],
            'status': d['status']
        })
    return render_template('devices.html', devices=devices_for_render)


@app.route('/devices/<int:device_id>', methods=['GET'])
def device_control_page(device_id):
    devices = load_devices(CURRENT_USER)
    device = None
    for d in devices:
        if d['device_id'] == device_id:
            device = d
            break
    if device is None:
        return "Device not found", 404

    # Provide device dict with all required keys
    device_data = {
        'device_id': device['device_id'],
        'device_name': device['device_name'],
        'status': device['status'],
        'power': device['power'],
        'brightness': device['brightness'],
        'temperature': device['temperature'],
        'mode': device['mode'],
        'schedule_time': device['schedule_time'],
        'device_type': device['device_type'],
        'room': device['room'],
        'brand': device['brand'],
        'model': device['model']
    }

    return render_template('device_control.html', device=device_data)


@app.route('/devices/<int:device_id>', methods=['POST'])
def save_device_settings(device_id):
    devices = load_devices(CURRENT_USER)
    device = None
    for d in devices:
        if d['device_id'] == device_id:
            device = d
            break
    if device is None:
        return "Device not found", 404

    # Update device fields from form if present
    power = request.form.get('power')
    brightness = request.form.get('brightness')
    temperature = request.form.get('temperature')
    mode = request.form.get('mode')
    schedule_time = request.form.get('schedule_time')

    if power in ['on', 'off']:
        device['power'] = power

    if brightness is not None and brightness.isdigit():
        device['brightness'] = int(brightness)
    else:
        device['brightness'] = None

    if temperature is not None and temperature.isdigit():
        device['temperature'] = int(temperature)
    else:
        device['temperature'] = None

    device['mode'] = mode if mode != '' else None
    device['schedule_time'] = schedule_time if schedule_time != '' else None

    save_devices(devices, CURRENT_USER)

    # Redirect to device control page after saving
    return redirect(url_for('device_control_page', device_id=device_id))


@app.route('/devices/add', methods=['GET'])
def add_device_page():
    return render_template('add_device.html')


@app.route('/devices/add', methods=['POST'])
def submit_new_device():
    devices = load_devices(CURRENT_USER)
    next_id = get_next_device_id(devices)

    device_name = request.form.get('device_name', '').strip()
    device_type = request.form.get('device_type', '').strip()
    room = request.form.get('device_room', '').strip()  # Note: form field device-room per design

    # For new device, brand, model, status as default and other defaults
    brand = "Unknown"
    model = "Unknown"
    status = "Offline"
    power = "off"
    brightness = None
    temperature = None
    mode = None
    schedule_time = None

    # Validate required fields
    if not device_name or not device_type or not room:
        # If validation fails, re-render add device page (ideal to flash message, but not specified)
        return render_template('add_device.html')

    new_device = {
        'username': CURRENT_USER,
        'device_id': next_id,
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

    devices.append(new_device)
    save_devices(devices, CURRENT_USER)

    return redirect(url_for('device_list_page'))


@app.route('/automation')
def automation_rules_page():
    rules = load_automation_rules(CURRENT_USER)
    devices = load_devices(CURRENT_USER)

    devices_summary = [{'device_id': d['device_id'], 'device_name': d['device_name']} for d in devices]
    rules_summary = []
    for r in rules:
        rules_summary.append({
            'rule_id': r['rule_id'],
            'rule_name': r['rule_name'],
            'trigger_type': r['trigger_type'],
            'trigger_value': r['trigger_value'],
            'action_device_id': r['action_device_id'],
            'action_type': r['action_type'],
            'enabled': r['enabled']
        })

    return render_template('automation.html', rules=rules_summary, devices=devices_summary)


@app.route('/automation/add', methods=['POST'])
def add_automation_rule():
    rules = load_automation_rules(CURRENT_USER)
    devices = load_devices(CURRENT_USER)
    next_rule_id = get_next_rule_id(rules)

    rule_name = request.form.get('rule_name', '').strip()
    trigger_type = request.form.get('trigger_type', '').strip()
    trigger_value = request.form.get('trigger_value', '').strip()
    action_device_id_str = request.form.get('action_device', '').strip()
    action_type = request.form.get('action_type', '').strip()

    if not rule_name or not trigger_type or not trigger_value or not action_device_id_str or not action_type:
        # Missing required fields, reload with current data
        return automation_rules_page()

    try:
        action_device_id = int(action_device_id_str)
    except ValueError:
        return automation_rules_page()

    # To keep simple, no validation of action_type values here

    new_rule = {
        'username': CURRENT_USER,
        'rule_id': next_rule_id,
        'rule_name': rule_name,
        'trigger_type': trigger_type,
        'trigger_value': trigger_value,
        'action_device_id': action_device_id,
        'action_type': action_type,
        'action_value': None,
        'enabled': True
    }

    rules.append(new_rule)
    save_automation_rules(rules, CURRENT_USER)

    return redirect(url_for('automation_rules_page'))


@app.route('/energy')
def energy_report_page():
    energy_logs = load_energy_logs(CURRENT_USER)
    devices = load_devices(CURRENT_USER)

    total_kwh = sum(log['consumption_kwh'] for log in energy_logs)
    cost_estimate = total_kwh * 0.12  # assume $0.12 per kwh for estimate

    energy_summary = {
        'total_kwh': total_kwh,
        'cost_estimate': cost_estimate
    }

    # Reduced fields for energy_logs context
    energy_logs_display = []
    for log in energy_logs:
        energy_logs_display.append({
            'device_id': log['device_id'],
            'date': log['date'],
            'consumption_kwh': log['consumption_kwh']
        })

    return render_template('energy.html', energy_summary=energy_summary, energy_logs=energy_logs_display)


@app.route('/energy/filter', methods=['POST'])
def apply_energy_filter():
    filter_date = request.form.get('date', '').strip()

    energy_logs = load_energy_logs(CURRENT_USER)

    filtered_logs = []
    for log in energy_logs:
        if filter_date == '' or log['date'] == filter_date:
            filtered_logs.append({
                'device_id': log['device_id'],
                'date': log['date'],
                'consumption_kwh': log['consumption_kwh']
            })

    # Recalculate summary for filtered logs
    total_kwh = sum(log['consumption_kwh'] for log in filtered_logs)
    cost_estimate = total_kwh * 0.12
    energy_summary = {
        'total_kwh': total_kwh,
        'cost_estimate': cost_estimate
    }

    return render_template('energy.html', energy_summary=energy_summary, energy_logs=filtered_logs)


@app.route('/activity')
def activity_logs_page():
    activity_logs = load_activity_logs(CURRENT_USER)

    activity_logs_display = []
    for log in activity_logs:
        activity_logs_display.append({
            'timestamp': log['timestamp'],
            'device_id': log['device_id'],
            'action': log['action'],
            'details': log['details']
        })

    return render_template('activity.html', activity_logs=activity_logs_display)


@app.route('/activity/search', methods=['POST'])
def apply_activity_search():
    search_query = request.form.get('search_query', '').strip().lower()

    activity_logs = load_activity_logs(CURRENT_USER)

    filtered_logs = []
    for log in activity_logs:
        if (search_query in log['action'].lower()) or (search_query in log['details'].lower()):
            filtered_logs.append({
                'timestamp': log['timestamp'],
                'device_id': log['device_id'],
                'action': log['action'],
                'details': log['details']
            })

    return render_template('activity.html', activity_logs=filtered_logs, search_query=search_query)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
