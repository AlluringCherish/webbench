from flask import Flask, render_template, redirect, url_for, request
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

# Current user for demo purpose
CURRENT_USER = 'john_doe'

# Helper function to read pipe-delimited file and return list of dict
# Specific loaders for each data file based on schema

def load_devices(username):
    devices = []
    filepath = os.path.join('data', 'devices.txt')
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 13:
                    continue
                (user, device_id, device_name, device_type, room, brand, model,
                 status, power, brightness, temperature, mode, schedule_time) = parts
                if user != username:
                    continue
                devices.append({
                    'username': user,
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
                })
    except Exception:
        pass
    return devices


def load_rooms(username):
    rooms = []
    filepath = os.path.join('data', 'rooms.txt')
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 3:
                    continue
                user, room_id, room_name = parts
                if user != username:
                    continue
                rooms.append(room_name)
    except Exception:
        pass
    return rooms


def load_automation_rules(username):
    rules = []
    filepath = os.path.join('data', 'automation_rules.txt')
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 9:
                    continue
                (user, rule_id, rule_name, trigger_type, trigger_value, action_device_id,
                 action_type, action_value, enabled) = parts
                if user != username:
                    continue
                rules.append({
                    'username': user,
                    'rule_id': int(rule_id),
                    'rule_name': rule_name,
                    'trigger_type': trigger_type,
                    'trigger_value': trigger_value,
                    'action_device_id': int(action_device_id),
                    'action_type': action_type,
                    'action_value': action_value,
                    'enabled': enabled
                })
    except Exception:
        pass
    return rules


def load_energy_logs(username):
    logs = []
    filepath = os.path.join('data', 'energy_logs.txt')
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 4:
                    continue
                user, device_id, date, consumption_kwh = parts
                if user != username:
                    continue
                logs.append({
                    'username': user,
                    'device_id': int(device_id),
                    'date': date,
                    'consumption_kwh': float(consumption_kwh)
                })
    except Exception:
        pass
    return logs


def load_activity_logs(username):
    logs = []
    filepath = os.path.join('data', 'activity_logs.txt')
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 5:
                    continue
                user, timestamp, device_id, action, details = parts
                if user != username:
                    continue
                logs.append({
                    'username': user,
                    'timestamp': timestamp,
                    'device_id': int(device_id),
                    'action': action,
                    'details': details
                })
    except Exception:
        pass
    return logs


# Root route redirect
@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard_page'))


# Dashboard page
@app.route('/dashboard')
def dashboard_page():
    devices = load_devices(CURRENT_USER)

    # Build rooms summary dictionary {room_name: device_count}
    rooms_summary = {}
    for d in devices:
        room = d['room']
        rooms_summary[room] = rooms_summary.get(room, 0) + 1

    context = {
        'devices': devices,
        'rooms_summary': rooms_summary
    }
    return render_template('dashboard.html', **context)


# Devices list page
@app.route('/devices')
def device_list_page():
    devices = load_devices(CURRENT_USER)
    return render_template('devices.html', devices=devices)


# Device control page
@app.route('/devices/<int:device_id>')
def device_control_page(device_id):
    devices = load_devices(CURRENT_USER)
    device = None
    for d in devices:
        if d['device_id'] == device_id:
            device = d
            break
    if device is None:
        # If device not found, respond with 404
        return "Device not found", 404
    return render_template('device_control.html', device=device)


# Add device page GET
@app.route('/add-device', methods=['GET'])
def add_device_page():
    device_types = ["Light", "Thermostat", "Camera", "Lock", "Sensor", "Appliance"]
    rooms = ["Living Room", "Bedroom", "Kitchen", "Bathroom", "Garage"]
    return render_template('add_device.html', device_types=device_types, rooms=rooms)


# Add device page POST
@app.route('/add-device', methods=['POST'])
def submit_new_device():
    # Extract form data
    device_name = request.form.get('device-name', '').strip()
    device_type = request.form.get('device-type', '').strip()
    device_room = request.form.get('device-room', '').strip()

    device_types = ["Light", "Thermostat", "Camera", "Lock", "Sensor", "Appliance"]
    rooms = ["Living Room", "Bedroom", "Kitchen", "Bathroom", "Garage"]

    # Validate inputs
    if device_name == '' or device_type not in device_types or device_room not in rooms:
        # For simplicity, just redirect back to add device page
        return redirect(url_for('add_device_page'))

    # Load existing devices to determine new device_id
    devices = load_devices(CURRENT_USER)
    existing_ids = [d['device_id'] for d in devices]
    new_device_id = max(existing_ids, default=0) + 1

    # Create new device dict with default values as per schema:
    # username|device_id|device_name|device_type|room|brand|model|status|power|brightness|temperature|mode|schedule_time
    new_device = {
        'username': CURRENT_USER,
        'device_id': new_device_id,
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

    # Append new device to devices.txt
    device_line = '|'.join([
        new_device['username'],
        str(new_device['device_id']),
        new_device['device_name'],
        new_device['device_type'],
        new_device['room'],
        new_device['brand'],
        new_device['model'],
        new_device['status'],
        new_device['power'],
        new_device['brightness'],
        new_device['temperature'],
        new_device['mode'],
        new_device['schedule_time']
    ])
    try:
        with open(os.path.join('data', 'devices.txt'), 'a', encoding='utf-8') as f:
            f.write(device_line + '\n')
    except Exception:
        # Ignore errors for now
        pass

    return redirect(url_for('device_list_page'))


# Automation rules page GET
@app.route('/automation', methods=['GET'])
def automation_rules_page():
    automation_rules = load_automation_rules(CURRENT_USER)
    devices = load_devices(CURRENT_USER)
    return render_template('automation.html', automation_rules=automation_rules, devices=devices)


# Automation rules page POST - add new rule
@app.route('/automation', methods=['POST'])
def add_automation_rule():
    rule_name = request.form.get('rule-name', '').strip()
    trigger_type = request.form.get('trigger-type', '').strip()
    trigger_value = request.form.get('trigger-value', '').strip()
    action_device_id = request.form.get('action-device', '').strip()
    action_type = request.form.get('action-type', '').strip()
    
    # Validate action_device_id is int
    try:
        action_device_id_int = int(action_device_id)
    except:
        return redirect(url_for('automation_rules_page'))

    # Validate required fields
    if not all([rule_name, trigger_type, trigger_value, action_type]):
        return redirect(url_for('automation_rules_page'))

    # Load existing rules to find new rule_id
    rules = load_automation_rules(CURRENT_USER)
    existing_ids = [r['rule_id'] for r in rules]
    new_rule_id = max(existing_ids, default=0) + 1

    # action_value can be empty - we don't have form input for it explicitly in spec
    action_value = ''

    new_rule = {
        'username': CURRENT_USER,
        'rule_id': new_rule_id,
        'rule_name': rule_name,
        'trigger_type': trigger_type,
        'trigger_value': trigger_value,
        'action_device_id': action_device_id_int,
        'action_type': action_type,
        'action_value': action_value,
        'enabled': 'true'
    }

    # Append to automation_rules.txt
    rule_line = '|'.join([
        new_rule['username'],
        str(new_rule['rule_id']),
        new_rule['rule_name'],
        new_rule['trigger_type'],
        new_rule['trigger_value'],
        str(new_rule['action_device_id']),
        new_rule['action_type'],
        new_rule['action_value'],
        new_rule['enabled']
    ])
    try:
        with open(os.path.join('data', 'automation_rules.txt'), 'a', encoding='utf-8') as f:
            f.write(rule_line + '\n')
    except Exception:
        pass

    return redirect(url_for('automation_rules_page'))


# Energy report page GET
@app.route('/energy', methods=['GET'])
def energy_report_page():
    energy_logs = load_energy_logs(CURRENT_USER)

    total_consumption = sum(log['consumption_kwh'] for log in energy_logs)
    # Assume cost per kWh = 0.12 (USD) - could be any fixed number
    total_cost = total_consumption * 0.12

    return render_template('energy_report.html', energy_logs=energy_logs,
                           total_consumption=total_consumption, total_cost=total_cost)


# Energy report page POST - apply date filter
@app.route('/energy', methods=['POST'])
def apply_energy_date_filter():
    date_filter = request.form.get('date-filter', '').strip()
    energy_logs = load_energy_logs(CURRENT_USER)

    if date_filter:
        filtered_logs = [log for log in energy_logs if log['date'] == date_filter]
    else:
        filtered_logs = energy_logs

    total_consumption = sum(log['consumption_kwh'] for log in filtered_logs)
    total_cost = total_consumption * 0.12

    return render_template('energy_report.html', energy_logs=filtered_logs,
                           total_consumption=total_consumption, total_cost=total_cost)


# Activity logs page GET
@app.route('/activity', methods=['GET'])
def activity_logs_page():
    activity_logs = load_activity_logs(CURRENT_USER)
    return render_template('activity_logs.html', activity_logs=activity_logs)


# Activity logs page POST - apply search filter
@app.route('/activity', methods=['POST'])
def apply_activity_search():
    search_term = request.form.get('search-activity', '').strip().lower()
    activity_logs = load_activity_logs(CURRENT_USER)

    if search_term:
        filtered_logs = [log for log in activity_logs if
                         search_term in log['action'].lower() or
                         search_term in log['details'].lower()]
    else:
        filtered_logs = activity_logs

    return render_template('activity_logs.html', activity_logs=filtered_logs)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
