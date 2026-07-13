from flask import Flask, request, redirect, url_for, render_template
import os
from datetime import datetime

app = Flask(__name__)

DATA_DIR = 'data'
USER = 'john_doe'  # Fixed user for this implementation

# File paths
USERS_FILE = os.path.join(DATA_DIR, 'users.txt')
DEVICES_FILE = os.path.join(DATA_DIR, 'devices.txt')
ROOMS_FILE = os.path.join(DATA_DIR, 'rooms.txt')
AUTOMATION_RULES_FILE = os.path.join(DATA_DIR, 'automation_rules.txt')
ENERGY_LOGS_FILE = os.path.join(DATA_DIR, 'energy_logs.txt')
ACTIVITY_LOGS_FILE = os.path.join(DATA_DIR, 'activity_logs.txt')

# Device types and room names (validations as per spec)
DEVICE_TYPES = ['Light', 'Thermostat', 'Camera', 'Lock', 'Sensor', 'Appliance']
ROOM_NAMES = ['Living Room', 'Bedroom', 'Kitchen', 'Bathroom', 'Garage']

# Utility functions for reading and writing pipe-delimited data

def read_data_file(filepath):
    if not os.path.exists(filepath):
        return []
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.read().strip().split('\n')
        if not lines or lines == ['']:
            return []
        data = [line.strip() for line in lines if line.strip()]
        return data

def write_data_file(filepath, lines):
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n')

def get_devices(username):
    lines = read_data_file(DEVICES_FILE)
    devices = []
    for line in lines:
        if not line:
            continue
        parts = line.split('|')
        if len(parts) != 13:
            continue
        if parts[0] != username:
            continue
        device = {
            'username': parts[0],
            'device_id': parts[1],
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
            'schedule_time': parts[12],
        }
        devices.append(device)
    return devices

def write_devices(devices):
    lines = []
    for d in devices:
        line = '|'.join([
            d.get('username',''),
            str(d.get('device_id','')),
            d.get('device_name',''),
            d.get('device_type',''),
            d.get('room',''),
            d.get('brand',''),
            d.get('model',''),
            d.get('status',''),
            d.get('power',''),
            d.get('brightness',''),
            d.get('temperature',''),
            d.get('mode',''),
            d.get('schedule_time',''),
        ])
        lines.append(line)
    write_data_file(DEVICES_FILE, lines)

def get_rooms(username):
    lines = read_data_file(ROOMS_FILE)
    rooms = []
    for line in lines:
        if not line:
            continue
        parts = line.split('|')
        if len(parts) != 3:
            continue
        if parts[0] != username:
            continue
        rooms.append({'username': parts[0], 'room_id': parts[1], 'room_name': parts[2]})
    return rooms

def get_automation_rules(username):
    lines = read_data_file(AUTOMATION_RULES_FILE)
    rules = []
    for line in lines:
        if not line:
            continue
        parts = line.split('|')
        if len(parts) != 9:
            continue
        if parts[0] != username:
            continue
        rule = {
            'username': parts[0],
            'rule_id': parts[1],
            'rule_name': parts[2],
            'trigger_type': parts[3],
            'trigger_value': parts[4],
            'action_device_id': parts[5],
            'action_type': parts[6],
            'action_value': parts[7],
            'enabled': parts[8],
        }
        rules.append(rule)
    return rules

def write_automation_rules(rules):
    lines = []
    for r in rules:
        line = '|'.join([
            r.get('username',''),
            str(r.get('rule_id','')),
            r.get('rule_name',''),
            r.get('trigger_type',''),
            r.get('trigger_value',''),
            str(r.get('action_device_id','')),
            r.get('action_type',''),
            r.get('action_value',''),
            r.get('enabled',''),
        ])
        lines.append(line)
    write_data_file(AUTOMATION_RULES_FILE, lines)

def get_energy_logs(username):
    lines = read_data_file(ENERGY_LOGS_FILE)
    logs = []
    for line in lines:
        if not line:
            continue
        parts = line.split('|')
        if len(parts) != 4:
            continue
        if parts[0] != username:
            continue
        log = {
            'username': parts[0],
            'device_id': parts[1],
            'date': parts[2],
            'consumption_kwh': parts[3],
        }
        logs.append(log)
    return logs

def get_activity_logs(username):
    lines = read_data_file(ACTIVITY_LOGS_FILE)
    logs = []
    for line in lines:
        if not line:
            continue
        parts = line.split('|')
        if len(parts) != 5:
            continue
        if parts[0] != username:
            continue
        log = {
            'username': parts[0],
            'timestamp': parts[1],
            'device_id': parts[2],
            'action': parts[3],
            'details': parts[4],
        }
        logs.append(log)
    return logs

def write_activity_logs(logs):
    lines = []
    for log in logs:
        line = '|'.join([
            log.get('username',''),
            log.get('timestamp',''),
            str(log.get('device_id','')),
            log.get('action',''),
            log.get('details',''),
        ])
        lines.append(line)
    write_data_file(ACTIVITY_LOGS_FILE, lines)

def log_activity(username, device_id, action, details):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    new_log = {
        'username': username,
        'timestamp': timestamp,
        'device_id': str(device_id),
        'action': action,
        'details': details,
    }
    logs = get_activity_logs(username)
    logs.append(new_log)
    write_activity_logs(logs)

def next_device_id(username):
    devices = get_devices(username)
    max_id = 0
    for d in devices:
        try:
            did = int(d['device_id'])
            if did > max_id:
                max_id = did
        except ValueError:
            continue
    return str(max_id + 1)

def next_rule_id(username):
    rules = get_automation_rules(username)
    max_id = 0
    for r in rules:
        try:
            rid = int(r['rule_id'])
            if rid > max_id:
                max_id = rid
        except ValueError:
            continue
    return str(max_id + 1)

@app.route('/')
@app.route('/dashboard')
def dashboard():
    devices = get_devices(USER)
    total_devices = len(devices)
    active_devices = sum(1 for d in devices if d.get('status','') == 'Online')
    offline_devices = total_devices - active_devices

    rooms = get_rooms(USER)
    room_list = []
    for room in rooms:
        room_name = room['room_name']
        count = sum(1 for d in devices if d['room'] == room_name)
        room_list.append({'room_name': room_name, 'device_count': count})

    return render_template('dashboard.html', total_devices=total_devices, active_devices=active_devices, offline_devices=offline_devices, rooms=room_list)

@app.route('/devices')
def device_list():
    devices = get_devices(USER)
    return render_template('device_list.html', devices=devices)

@app.route('/devices/add', methods=['GET', 'POST'])
def add_device():
    if request.method == 'GET':
        return render_template('add_device.html', device_types=DEVICE_TYPES, device_rooms=ROOM_NAMES)

    data = request.form
    device_name = data.get('device_name','').strip()
    device_type = data.get('device_type','').strip()
    device_room = data.get('device_room','').strip()
    brand = data.get('brand','').strip() or ''
    model = data.get('model','').strip() or ''

    if device_type not in DEVICE_TYPES:
        return "Invalid device type", 400
    if device_room not in ROOM_NAMES:
        return "Invalid device room", 400
    if not device_name:
        return "Device name is required", 400

    devices = get_devices(USER)
    new_id = next_device_id(USER)

    new_device = {
        'username': USER,
        'device_id': new_id,
        'device_name': device_name,
        'device_type': device_type,
        'room': device_room,
        'brand': brand,
        'model': model,
        'status': 'Offline',
        'power': 'off',
        'brightness': '',
        'temperature': '',
        'mode': '',
        'schedule_time': '',
    }
    devices.append(new_device)
    write_devices(devices)

    return redirect(url_for('device_list'))

@app.route('/devices/<device_id>', methods=['GET', 'POST'])
def device_control(device_id):
    devices = get_devices(USER)
    device = None
    for d in devices:
        if d['device_id'] == device_id:
            device = d
            break
    if not device:
        return "Device not found", 404

    if request.method == 'GET':
        return render_template('device_control.html', device=device)

    data = request.form

    power = data.get('power')
    brightness = data.get('brightness')
    temperature = data.get('temperature')
    mode = data.get('mode')
    schedule_time = data.get('schedule_time')

    logs_actions = []

    if power in ['on', 'off'] and device['power'] != power:
        device['power'] = power
        logs_actions.append(f'Power set to {power}')

    if brightness is not None:
        brightness = brightness.strip()
        if brightness == '':
            brightness = ''
        else:
            try:
                bri_val = int(brightness)
                if 0 <= bri_val <= 100:
                    device['brightness'] = str(bri_val)
                    logs_actions.append(f'Set brightness to {bri_val}')
                else:
                    return "Brightness must be 0-100", 400
            except ValueError:
                return "Brightness must be an integer", 400

    if temperature is not None:
        temperature = temperature.strip()
        if temperature == '':
            temperature = ''
        else:
            try:
                temp_val = int(temperature)
                device['temperature'] = str(temp_val)
                logs_actions.append(f'Set temperature to {temp_val}')
            except ValueError:
                return "Temperature must be an integer", 400

    if mode is not None:
        mode = mode.strip()
        if device['mode'] != mode:
            device['mode'] = mode
            logs_actions.append(f'Mode set to {mode}')

    if schedule_time is not None:
        schedule_time = schedule_time.strip()
        if schedule_time == '' or (len(schedule_time) == 5 and schedule_time[2] == ':'):
            device['schedule_time'] = schedule_time
            logs_actions.append(f'Schedule time set to {schedule_time}')
        else:
            return "Schedule time format must be HH:MM or empty", 400

    write_devices(devices)

    for action in logs_actions:
        log_activity(USER, device_id, 'Settings Changed', action)

    return redirect(url_for('device_list'))

@app.route('/automation', methods=['GET', 'POST'])
def automation_rules():
    if request.method == 'GET':
        rules = get_automation_rules(USER)
        devices = get_devices(USER)
        return render_template('automation_rules.html', rules=rules, devices=devices)

    data = request.form
    rule_name = data.get('rule_name','').strip()
    trigger_type = data.get('trigger_type','').strip()
    trigger_value = data.get('trigger_value','').strip()
    action_device_id = data.get('action_device_id','').strip()
    action_type = data.get('action_type','').strip()
    action_value = data.get('action_value','').strip()
    enabled = data.get('enabled','true').strip().lower()

    if trigger_type not in ['Time', 'Motion', 'Temperature']:
        return "Invalid trigger type", 400
    if enabled not in ['true', 'false']:
        return "Invalid enabled value", 400
    if action_type not in ['Turn On', 'Turn Off', 'Set Brightness', 'Set Temperature']:
        return "Invalid action type", 400
    if not rule_name:
        return "Rule name required", 400
    devices = get_devices(USER)
    if not any(d['device_id'] == action_device_id for d in devices):
        return "Action device not found", 400

    new_rule_id = next_rule_id(USER)

    new_rule = {
        'username': USER,
        'rule_id': new_rule_id,
        'rule_name': rule_name,
        'trigger_type': trigger_type,
        'trigger_value': trigger_value,
        'action_device_id': action_device_id,
        'action_type': action_type,
        'action_value': action_value,
        'enabled': enabled,
    }

    rules = get_automation_rules(USER)
    rules.append(new_rule)
    write_automation_rules(rules)

    return redirect(url_for('automation_rules'))

@app.route('/energy')
def energy_report():
    date_filter = request.args.get('date','').strip()
    energy_logs = get_energy_logs(USER)

    filtered_logs = []
    for log in energy_logs:
        if date_filter:
            if log['date'] != date_filter:
                continue
        filtered_logs.append(log)

    total_kwh = 0.0
    device_consumption = {}
    for log in filtered_logs:
        try:
            consumption = float(log['consumption_kwh'])
        except ValueError:
            consumption = 0.0
        total_kwh += consumption
        device_id = log['device_id']
        device_consumption[device_id] = device_consumption.get(device_id, 0.0) + consumption

    cost_estimate = round(total_kwh * 0.12, 2)

    devices = get_devices(USER)
    device_dict = {d['device_id']: d for d in devices}

    for log in filtered_logs:
        log['device_name'] = device_dict.get(log['device_id'], {}).get('device_name', 'Unknown')

    return render_template('energy_report.html', total_consumption=total_kwh, estimated_cost=cost_estimate, energy_logs=filtered_logs, selected_date=date_filter)

@app.route('/activity')
def activity_logs():
    search_term = request.args.get('search','').strip()
    logs = get_activity_logs(USER)
    if search_term:
        lower_search = search_term.lower()
        logs = [log for log in logs if lower_search in log['action'].lower() or lower_search in log['details'].lower()]

    devices = get_devices(USER)
    device_dict = {d['device_id']: d for d in devices}

    for log in logs:
        log['device_name'] = device_dict.get(log['device_id'], {}).get('device_name', 'Unknown')

    return render_template('activity_logs.html', activity_logs=logs, search_term=search_term)

if __name__ == '__main__':
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    for path in [USERS_FILE, DEVICES_FILE, ROOMS_FILE, AUTOMATION_RULES_FILE, ENERGY_LOGS_FILE, ACTIVITY_LOGS_FILE]:
        if not os.path.exists(path):
            with open(path, 'w', encoding='utf-8') as f:
                f.write('')
    app.run(debug=True)
