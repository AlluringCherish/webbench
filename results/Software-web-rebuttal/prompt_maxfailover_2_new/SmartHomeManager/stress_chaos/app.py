from flask import Flask, render_template, redirect, url_for, request
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_PATH = 'data'

# Assumed logged in user (since no auth specified)
CURRENT_USER = 'john_doe'

# Helper functions to load and save data

def load_users():
    users = []
    try:
        with open(os.path.join(DATA_PATH, 'users.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 2:
                    user = {'username': parts[0], 'email': parts[1]}
                    users.append(user)
    except FileNotFoundError:
        pass
    return users


def load_devices(username):
    devices = []
    try:
        with open(os.path.join(DATA_PATH, 'devices.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 13:
                    (
                        u, d_id, d_name, d_type, room, brand,
                        model, status, power, brightness,
                        temperature, mode, schedule_time
                    ) = parts
                    if u == username:
                        device = {
                            'username': u,
                            'device_id': int(d_id),
                            'device_name': d_name,
                            'device_type': d_type,
                            'room': room,
                            'brand': brand,
                            'model': model,
                            'status': status,
                            'power': power,
                            'brightness': int(brightness) if brightness.isdigit() else None,
                            'temperature': int(temperature) if temperature.isdigit() else None,
                            'mode': mode,
                            'schedule_time': schedule_time if schedule_time else None
                        }
                        devices.append(device)
    except FileNotFoundError:
        pass
    return devices


def save_devices(devices):
    try:
        with open(os.path.join(DATA_PATH, 'devices.txt'), 'w', encoding='utf-8') as f:
            for d in devices:
                brightness = str(d['brightness']) if d['brightness'] is not None else ''
                temperature = str(d['temperature']) if d['temperature'] is not None else ''
                schedule_time = d['schedule_time'] if d['schedule_time'] is not None else ''
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
                    schedule_time
                ])
                f.write(line + '\n')
    except Exception as e:
        pass


def load_rooms(username):
    rooms = []
    try:
        with open(os.path.join(DATA_PATH, 'rooms.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 3:
                    u, room_id, room_name = parts
                    if u == username:
                        rooms.append({'username': u, 'room_id': int(room_id), 'room_name': room_name})
    except FileNotFoundError:
        pass
    return rooms


def load_automation_rules(username):
    rules = []
    try:
        with open(os.path.join(DATA_PATH, 'automation_rules.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 9:
                    (
                        u, rule_id, rule_name, trigger_type, trigger_value,
                        action_device_id, action_type, action_value, enabled
                    ) = parts
                    if u == username:
                        rule = {
                            'username': u,
                            'rule_id': int(rule_id),
                            'rule_name': rule_name,
                            'trigger_type': trigger_type,
                            'trigger_value': trigger_value,
                            'action_device_id': int(action_device_id),
                            'action_type': action_type,
                            'action_value': action_value,
                            'enabled': True if enabled.lower() == 'true' else False
                        }
                        rules.append(rule)
    except FileNotFoundError:
        pass
    return rules


def save_automation_rules(rules):
    try:
        with open(os.path.join(DATA_PATH, 'automation_rules.txt'), 'w', encoding='utf-8') as f:
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
    except Exception:
        pass


def load_energy_logs(username):
    logs = []
    try:
        with open(os.path.join(DATA_PATH, 'energy_logs.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 4:
                    u, device_id, date, consumption_kwh = parts
                    if u == username:
                        log = {
                            'username': u,
                            'device_id': int(device_id),
                            'date': date,
                            'consumption_kwh': float(consumption_kwh)
                        }
                        logs.append(log)
    except FileNotFoundError:
        pass
    return logs


def load_activity_logs(username):
    activities = []
    try:
        with open(os.path.join(DATA_PATH, 'activity_logs.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 5:
                    u, timestamp, device_id, action, details = parts
                    if u == username:
                        activity = {
                            'username': u,
                            'timestamp': timestamp,
                            'device_id': int(device_id),
                            'action': action,
                            'details': details
                        }
                        activities.append(activity)
    except FileNotFoundError:
        pass
    return activities


# Routes

@app.route('/')
def redirect_to_dashboard():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    username = CURRENT_USER
    devices = load_devices(username)
    
    # Build summary info for dashboard
    total_devices = len(devices)
    active_devices = sum(1 for d in devices if d['status'] == 'Online')
    offline_devices = total_devices - active_devices

    rooms = load_rooms(username)
    
    # Count devices by room
    room_counts = {}
    for room in rooms:
        count = sum(1 for d in devices if d['room'] == room['room_name'])
        room_counts[room['room_name']] = count

    # devices list to pass is devices of user
    return render_template('dashboard.html', username=username, devices=devices, 
                           total_devices=total_devices, active_devices=active_devices, offline_devices=offline_devices, room_counts=room_counts)


@app.route('/devices')
def device_list():
    username = CURRENT_USER
    devices = load_devices(username)
    return render_template('device_list_page.html', username=username, devices=devices)


@app.route('/add-device', methods=['GET', 'POST'])
def add_device():
    username = CURRENT_USER
    if request.method == 'POST':
        # Extract form data
        device_name = request.form.get('device-name', '').strip()
        device_type = request.form.get('device-type', '').strip()
        device_room = request.form.get('device-room', '').strip()

        # Validate required fields (device_name and device_type and device_room must be present)
        if not device_name or not device_type or not device_room:
            # Render page again with error or just silently redisplay
            return render_template('add_device_page.html', username=username)

        devices = load_devices(username)
        # Determine new device_id
        if devices:
            max_id = max(d['device_id'] for d in devices)
        else:
            max_id = 0

        # New device defaults
        new_device = {
            'username': username,
            'device_id': max_id + 1,
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
            'schedule_time': None
        }

        devices.append(new_device)
        save_devices(devices)
        return redirect(url_for('device_list'))

    # GET
    return render_template('add_device_page.html', username=username)


@app.route('/device/<int:device_id>', methods=['GET', 'POST'])
def device_control(device_id):
    username = CURRENT_USER
    devices = load_devices(username)
    device = next((d for d in devices if d['device_id'] == device_id), None)
    if not device:
        # Not found device returns 404
        return "Device not found", 404

    if request.method == 'POST':
        # Only support toggling power and saving settings (power, brightness, temperature, mode, schedule_time)
        power = request.form.get('power')
        brightness = request.form.get('brightness')
        temperature = request.form.get('temperature')
        mode = request.form.get('mode')
        schedule_time = request.form.get('schedule_time')

        if power in ('on', 'off'):
            device['power'] = power
        if brightness is not None and brightness.isdigit():
            device['brightness'] = int(brightness)
        if temperature is not None and temperature.isdigit():
            device['temperature'] = int(temperature)
        if mode is not None:
            device['mode'] = mode
        if schedule_time:
            device['schedule_time'] = schedule_time
        else:
            device['schedule_time'] = None

        save_devices(devices)
        # POST after save redirect to self GET
        return redirect(url_for('device_control', device_id=device_id))

    return render_template('device_control_page.html', username=username, device=device)


@app.route('/automation-rules', methods=['GET', 'POST'])
def automation_rules():
    username = CURRENT_USER
    rules = load_automation_rules(username)
    devices = load_devices(username)

    if request.method == 'POST':
        # Gather form data
        rule_name = request.form.get('rule-name', '').strip()
        trigger_type = request.form.get('trigger-type', '').strip()
        trigger_value = request.form.get('trigger-value', '').strip()
        action_device_id = request.form.get('action-device', '').strip()
        action_type = request.form.get('action-type', '').strip()

        # Validate required fields
        if not rule_name or not trigger_type or not action_device_id or not action_type:
            return render_template('automation_rules.html', username=username, rules=rules)

        try:
            action_device_id = int(action_device_id)
        except ValueError:
            return render_template('automation_rules.html', username=username, rules=rules)

        # Determine new rule_id
        if rules:
            max_rule_id = max(r['rule_id'] for r in rules)
        else:
            max_rule_id = 0

        # action_value optional depending on action_type
        action_value = request.form.get('action-value', '').strip()

        new_rule = {
            'username': username,
            'rule_id': max_rule_id + 1,
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

    return render_template('automation_rules.html', username=username, rules=rules)


@app.route('/energy-report')
def energy_report():
    username = CURRENT_USER
    energy_logs = load_energy_logs(username)
    devices = load_devices(username)

    # Compose energy summary: total consumption and cost (let's assume cost $0.12 per kWh)
    # Filter by date if date-filter present in query args
    filter_date = request.args.get('date-filter')
    if filter_date:
        filtered_logs = [log for log in energy_logs if log['date'] == filter_date]
    else:
        filtered_logs = energy_logs

    total_consumption = sum(log['consumption_kwh'] for log in filtered_logs)
    cost_per_kwh = 0.12
    total_cost = total_consumption * cost_per_kwh

    energy_summary = {
        'total_consumption': round(total_consumption, 2),
        'total_cost': round(total_cost, 2)
    }

    # Show logs filtered
    return render_template('energy_report_page.html', username=username, energy_summary=energy_summary, energy_logs=filtered_logs)


@app.route('/activity-logs')
def activity_logs():
    username = CURRENT_USER
    activities = load_activity_logs(username)

    search_filter = request.args.get('search-activity', '').strip()
    if search_filter:
        filtered_activities = [a for a in activities if search_filter.lower() in a['action'].lower() or search_filter.lower() in a['details'].lower()]
    else:
        filtered_activities = activities

    return render_template('activity_logs_page.html', username=username, activities=filtered_activities, search_filter=search_filter)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
