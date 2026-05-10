'''
Backend implementation for SmartHomeManager web application.
- Uses Flask to serve pages and handle routing.
- Data stored in local text files under 'data' directory with pipe-delimited format.
- Supports all required pages and their data interactions.
- Website accessible on local port 5000, starting at '/' (Dashboard).
'''
from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime
app = Flask(__name__, template_folder='templates')
DATA_DIR = 'data'
USERS_FILE = os.path.join(DATA_DIR, 'users.txt')
DEVICES_FILE = os.path.join(DATA_DIR, 'devices.txt')
ROOMS_FILE = os.path.join(DATA_DIR, 'rooms.txt')
AUTOMATION_FILE = os.path.join(DATA_DIR, 'automation_rules.txt')
ENERGY_FILE = os.path.join(DATA_DIR, 'energy_logs.txt')
ACTIVITY_FILE = os.path.join(DATA_DIR, 'activity_logs.txt')
# For simplicity, assume a fixed logged-in user for this demo
CURRENT_USER = 'john_doe'
def read_file_lines(filepath):
    if not os.path.exists(filepath):
        return []
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]
    return lines
def write_file_lines(filepath, lines):
    with open(filepath, 'w', encoding='utf-8') as f:
        for line in lines:
            f.write(line + '\n')
def parse_devices(username):
    devices = []
    lines = read_file_lines(DEVICES_FILE)
    for line in lines:
        parts = line.split('|')
        if len(parts) < 13:
            continue
        if parts[0] == username:
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
                'schedule_time': parts[12]
            }
            devices.append(device)
    return devices
def parse_rooms(username):
    rooms = []
    lines = read_file_lines(ROOMS_FILE)
    for line in lines:
        parts = line.split('|')
        if len(parts) < 3:
            continue
        if parts[0] == username:
            room = {
                'username': parts[0],
                'room_id': parts[1],
                'room_name': parts[2]
            }
            rooms.append(room)
    return rooms
def parse_automation_rules(username):
    rules = []
    lines = read_file_lines(AUTOMATION_FILE)
    for line in lines:
        parts = line.split('|')
        if len(parts) < 9:
            continue
        if parts[0] == username:
            rule = {
                'username': parts[0],
                'rule_id': parts[1],
                'rule_name': parts[2],
                'trigger_type': parts[3],
                'trigger_value': parts[4],
                'action_device_id': parts[5],
                'action_type': parts[6],
                'action_value': parts[7],
                'enabled': parts[8].lower() == 'true'
            }
            rules.append(rule)
    return rules
def parse_energy_logs(username):
    logs = []
    lines = read_file_lines(ENERGY_FILE)
    for line in lines:
        parts = line.split('|')
        if len(parts) < 4:
            continue
        if parts[0] == username:
            try:
                consumption = float(parts[3])
            except ValueError:
                consumption = 0.0
            log = {
                'username': parts[0],
                'device_id': parts[1],
                'date': parts[2],
                'consumption_kwh': consumption
            }
            logs.append(log)
    return logs
def parse_activity_logs(username):
    logs = []
    lines = read_file_lines(ACTIVITY_FILE)
    for line in lines:
        parts = line.split('|')
        if len(parts) < 5:
            continue
        if parts[0] == username:
            log = {
                'username': parts[0],
                'timestamp': parts[1],
                'device_id': parts[2],
                'action': parts[3],
                'details': parts[4]
            }
            logs.append(log)
    return logs
def save_devices(devices, username):
    # Read all lines, replace lines for username with updated devices
    all_lines = read_file_lines(DEVICES_FILE)
    new_lines = []
    # Build a dict for quick device_id lookup for this user
    device_map = {d['device_id']: d for d in devices}
    for line in all_lines:
        parts = line.split('|')
        if len(parts) < 13:
            continue
        if parts[0] == username:
            device_id = parts[1]
            if device_id in device_map:
                d = device_map[device_id]
                new_line = '|'.join([
                    d['username'], d['device_id'], d['device_name'], d['device_type'], d['room'],
                    d['brand'], d['model'], d['status'], d['power'], d['brightness'],
                    d['temperature'], d['mode'], d['schedule_time']
                ])
                new_lines.append(new_line)
                del device_map[device_id]
            # else: device removed? skip
        else:
            new_lines.append(line)
    # Add any new devices left in device_map (newly added)
    for d in device_map.values():
        new_line = '|'.join([
            d['username'], d['device_id'], d['device_name'], d['device_type'], d['room'],
            d['brand'], d['model'], d['status'], d['power'], d['brightness'],
            d['temperature'], d['mode'], d['schedule_time']
        ])
        new_lines.append(new_line)
    write_file_lines(DEVICES_FILE, new_lines)
def save_automation_rules(rules, username):
    all_lines = read_file_lines(AUTOMATION_FILE)
    new_lines = []
    rule_map = {r['rule_id']: r for r in rules}
    for line in all_lines:
        parts = line.split('|')
        if len(parts) < 9:
            continue
        if parts[0] == username:
            rule_id = parts[1]
            if rule_id in rule_map:
                r = rule_map[rule_id]
                new_line = '|'.join([
                    r['username'], r['rule_id'], r['rule_name'], r['trigger_type'], r['trigger_value'],
                    r['action_device_id'], r['action_type'], r['action_value'], 'true' if r['enabled'] else 'false'
                ])
                new_lines.append(new_line)
                del rule_map[rule_id]
        else:
            new_lines.append(line)
    for r in rule_map.values():
        new_line = '|'.join([
            r['username'], r['rule_id'], r['rule_name'], r['trigger_type'], r['trigger_value'],
            r['action_device_id'], r['action_type'], r['action_value'], 'true' if r['enabled'] else 'false'
        ])
        new_lines.append(new_line)
    write_file_lines(AUTOMATION_FILE, new_lines)
@app.route('/')
def dashboard():
    # Gather device summary and room list with device counts
    devices = parse_devices(CURRENT_USER)
    total_devices = len(devices)
    active_devices = sum(1 for d in devices if d['status'].lower() == 'online')
    offline_devices = total_devices - active_devices
    rooms = parse_rooms(CURRENT_USER)
    # Count devices per room
    room_counts = {}
    for room in rooms:
        room_counts[room['room_name']] = 0
    for d in devices:
        if d['room'] in room_counts:
            room_counts[d['room']] += 1
        else:
            # In case device room not in rooms.txt, count anyway
            room_counts[d['room']] = 1
    return render_template('dashboard.html',
                           total_devices=total_devices,
                           active_devices=active_devices,
                           offline_devices=offline_devices,
                           room_counts=room_counts)
@app.route('/devices')
def device_list():
    devices = parse_devices(CURRENT_USER)
    return render_template('device_list.html', devices=devices)
@app.route('/devices/control/<device_id>', methods=['GET', 'POST'])
def device_control(device_id):
    devices = parse_devices(CURRENT_USER)
    device = next((d for d in devices if d['device_id'] == device_id), None)
    if not device:
        return "Device not found", 404
    if request.method == 'POST':
        # Update device power and possibly other settings
        power = request.form.get('power')
        brightness = request.form.get('brightness')
        temperature = request.form.get('temperature')
        mode = request.form.get('mode')
        schedule_time = request.form.get('schedule_time')
        # Update device dict
        device['power'] = power if power in ['on', 'off'] else device['power']
        if brightness is not None:
            device['brightness'] = brightness
        if temperature is not None:
            device['temperature'] = temperature
        if mode is not None:
            device['mode'] = mode
        if schedule_time is not None:
            device['schedule_time'] = schedule_time
        # Save updated devices
        save_devices(devices, CURRENT_USER)
        return redirect(url_for('device_list'))
    return render_template('device_control.html', device=device)
@app.route('/devices/add', methods=['GET', 'POST'])
def add_device():
    if request.method == 'POST':
        device_name = request.form.get('device-name', '').strip()
        device_type = request.form.get('device-type', '').strip()
        device_room = request.form.get('device-room', '').strip()
        if not device_name or not device_type or not device_room:
            return "Missing required fields", 400
        # Generate new device_id (max existing + 1)
        devices = parse_devices(CURRENT_USER)
        existing_ids = [int(d['device_id']) for d in devices if d['device_id'].isdigit()]
        new_id = str(max(existing_ids) + 1 if existing_ids else 1)
        # Default values for brand, model, status, power, brightness, temperature, mode, schedule_time
        brand = ''
        model = ''
        status = 'Offline'
        power = 'off'
        brightness = ''
        temperature = ''
        mode = ''
        schedule_time = ''
        new_device = {
            'username': CURRENT_USER,
            'device_id': new_id,
            'device_name': device_name,
            'device_type': device_type,
            'room': device_room,
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
        return redirect(url_for('device_list'))
    # GET method: render add device page
    return render_template('add_device.html')
@app.route('/automation', methods=['GET', 'POST'])
def automation_rules():
    rules = parse_automation_rules(CURRENT_USER)
    devices = parse_devices(CURRENT_USER)
    if request.method == 'POST':
        rule_name = request.form.get('rule-name', '').strip()
        trigger_type = request.form.get('trigger-type', '').strip()
        trigger_value = request.form.get('trigger-value', '').strip()
        action_device_id = request.form.get('action-device', '').strip()
        action_type = request.form.get('action-type', '').strip()
        if not rule_name or not trigger_type or not action_device_id or not action_type:
            return "Missing required fields", 400
        # Generate new rule_id
        existing_ids = [int(r['rule_id']) for r in rules if r['rule_id'].isdigit()]
        new_rule_id = str(max(existing_ids) + 1 if existing_ids else 1)
        # Determine action_value for Set Brightness or Set Temperature, else empty
        action_value = ''
        if action_type in ['Set Brightness', 'Set Temperature']:
            action_value = request.form.get('action-value', '').strip()
        new_rule = {
            'username': CURRENT_USER,
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
        save_automation_rules(rules, CURRENT_USER)
        return redirect(url_for('automation_rules'))
    return render_template('automation_rules.html', rules=rules, devices=devices)
@app.route('/energy', methods=['GET', 'POST'])
def energy_report():
    logs = parse_energy_logs(CURRENT_USER)
    devices = parse_devices(CURRENT_USER)
    filtered_logs = logs
    filter_date = None
    if request.method == 'POST':
        filter_date = request.form.get('date-filter', '').strip()
        if filter_date:
            filtered_logs = [log for log in logs if log['date'] == filter_date]
    # Calculate total consumption and cost estimate (assume cost $0.12 per kWh)
    total_consumption = sum(log['consumption_kwh'] for log in filtered_logs)
    cost_estimate = total_consumption * 0.12
    # Map device_id to device_name for display
    device_names = {d['device_id']: d['device_name'] for d in devices}
    return render_template('energy_report.html',
                           energy_logs=filtered_logs,
                           total_consumption=total_consumption,
                           cost_estimate=cost_estimate,
                           device_names=device_names,
                           filter_date=filter_date)
@app.route('/activity', methods=['GET', 'POST'])
def activity_logs():
    logs = parse_activity_logs(CURRENT_USER)
    devices = parse_devices(CURRENT_USER)
    filtered_logs = logs
    search_term = ''
    if request.method == 'POST':
        search_term = request.form.get('search-activity', '').strip().lower()
        if search_term:
            filtered_logs = [log for log in logs if
                             search_term in log['action'].lower() or
                             search_term in log['details'].lower() or
                             any(search_term in d for d in [log['device_id']])]
    # Map device_id to device_name for display
    device_names = {d['device_id']: d['device_name'] for d in devices}
    return render_template('activity_logs.html',
                           activity_logs=filtered_logs,
                           device_names=device_names,
                           search_term=search_term)
if __name__ == '__main__':
    # Ensure data directory exists
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    # Ensure all required data files exist (create empty if missing)
    data_files = [USERS_FILE, DEVICES_FILE, ROOMS_FILE, AUTOMATION_FILE, ENERGY_FILE, ACTIVITY_FILE]
    for file_path in data_files:
        if not os.path.exists(file_path):
            with open(file_path, 'w', encoding='utf-8') as f:
                pass  # create empty file
    app.run(host='0.0.0.0', port=5000, debug=True)