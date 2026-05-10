'''
Flask backend for SmartHomeManager web application.
Defines routes for all pages with '/' as the Dashboard page.
Ensures all navigation uses Flask routing for consistent URL structure.
Loads data from local text files in 'data' directory.
'''
from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime
app = Flask(__name__)
DATA_DIR = 'data'
def read_devices(username):
    devices = []
    filepath = os.path.join(DATA_DIR, 'devices.txt')
    if not os.path.exists(filepath):
        return devices
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
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
def read_rooms(username):
    rooms = []
    filepath = os.path.join(DATA_DIR, 'rooms.txt')
    if not os.path.exists(filepath):
        return rooms
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if parts[0] == username:
                room = {
                    'username': parts[0],
                    'room_id': parts[1],
                    'room_name': parts[2]
                }
                rooms.append(room)
    return rooms
def read_automation_rules(username):
    rules = []
    filepath = os.path.join(DATA_DIR, 'automation_rules.txt')
    if not os.path.exists(filepath):
        return rules
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
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
def read_energy_logs(username):
    logs = []
    filepath = os.path.join(DATA_DIR, 'energy_logs.txt')
    if not os.path.exists(filepath):
        return logs
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if parts[0] == username:
                log = {
                    'username': parts[0],
                    'device_id': parts[1],
                    'date': parts[2],
                    'consumption_kwh': float(parts[3])
                }
                logs.append(log)
    return logs
def read_activity_logs(username):
    logs = []
    filepath = os.path.join(DATA_DIR, 'activity_logs.txt')
    if not os.path.exists(filepath):
        return logs
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
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
def write_devices(devices):
    filepath = os.path.join(DATA_DIR, 'devices.txt')
    lines = []
    for d in devices:
        line = '|'.join([
            d['username'], d['device_id'], d['device_name'], d['device_type'], d['room'],
            d['brand'], d['model'], d['status'], d['power'], d['brightness'],
            d['temperature'], d['mode'], d['schedule_time']
        ])
        lines.append(line)
    with open(filepath, 'w') as f:
        f.write('\n'.join(lines) + '\n')
def write_automation_rules(rules):
    filepath = os.path.join(DATA_DIR, 'automation_rules.txt')
    lines = []
    for r in rules:
        line = '|'.join([
            r['username'], r['rule_id'], r['rule_name'], r['trigger_type'], r['trigger_value'],
            r['action_device_id'], r['action_type'], r['action_value'], 'true' if r['enabled'] else 'false'
        ])
        lines.append(line)
    with open(filepath, 'w') as f:
        f.write('\n'.join(lines) + '\n')
@app.route('/')
def dashboard():
    # For demo, use a fixed username
    username = 'john_doe'
    devices = read_devices(username)
    rooms = read_rooms(username)
    total_devices = len(devices)
    active_devices = sum(1 for d in devices if d['status'].lower() == 'online')
    offline_devices = total_devices - active_devices
    # Count devices per room
    room_counts = {}
    for room in rooms:
        room_counts[room['room_name']] = 0
    for d in devices:
        if d['room'] in room_counts:
            room_counts[d['room']] += 1
    return render_template('dashboard.html',
                           username=username,
                           total_devices=total_devices,
                           active_devices=active_devices,
                           offline_devices=offline_devices,
                           room_counts=room_counts)
@app.route('/devices')
def device_list():
    username = 'john_doe'
    devices = read_devices(username)
    return render_template('device_list.html', devices=devices, username=username)
@app.route('/devices/control/<device_id>', methods=['GET', 'POST'])
def device_control(device_id):
    username = 'john_doe'
    devices = read_devices(username)
    device = None
    for d in devices:
        if d['device_id'] == device_id:
            device = d
            break
    if not device:
        return "Device not found", 404
    if request.method == 'POST':
        # Update device power status
        power = request.form.get('power')
        # Only update brightness if device type is Light
        if device['device_type'] == 'Light':
            brightness = request.form.get('brightness', '')
            device['brightness'] = brightness
            # Clear temperature if any
            device['temperature'] = ''
        # Only update temperature if device type is Thermostat
        elif device['device_type'] == 'Thermostat':
            temperature = request.form.get('temperature', '')
            device['temperature'] = temperature
            # Clear brightness if any
            device['brightness'] = ''
        else:
            # For other device types, clear brightness and temperature
            device['brightness'] = ''
            device['temperature'] = ''
        mode = request.form.get('mode', '')
        schedule_time = request.form.get('schedule_time', '')
        device['power'] = power if power in ['on', 'off'] else device['power']
        device['mode'] = mode
        device['schedule_time'] = schedule_time
        # Save changes
        write_devices(devices)
        # Log activity
        log_activity(username, device_id, 'Settings Changed', f'Power: {device["power"]}, Brightness: {device["brightness"]}, Temperature: {device["temperature"]}, Mode: {mode}, Schedule: {schedule_time}')
        return redirect(url_for('device_list'))
    return render_template('device_control.html', device=device, username=username)
@app.route('/devices/add', methods=['GET', 'POST'])
def add_device():
    username = 'john_doe'
    rooms = read_rooms(username)
    if request.method == 'POST':
        device_name = request.form.get('device_name')
        device_type = request.form.get('device_type')
        device_room = request.form.get('device_room')
        brand = request.form.get('brand', '')
        model = request.form.get('model', '')
        devices = read_devices(username)
        # Generate new device_id
        existing_ids = [int(d['device_id']) for d in devices if d['device_id'].isdigit()]
        new_id = str(max(existing_ids) + 1 if existing_ids else 1)
        new_device = {
            'username': username,
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
            'schedule_time': ''
        }
        devices.append(new_device)
        write_devices(devices)
        # Log activity
        log_activity(username, new_id, 'Device Added', f'{device_name} ({device_type}) in {device_room}')
        return redirect(url_for('device_list'))
    device_types = ['Light', 'Thermostat', 'Camera', 'Lock', 'Sensor', 'Appliance']
    room_names = [r['room_name'] for r in rooms]
    return render_template('add_device.html', device_types=device_types, rooms=room_names, username=username)
@app.route('/automation', methods=['GET', 'POST'])
def automation_rules():
    username = 'john_doe'
    rules = read_automation_rules(username)
    devices = read_devices(username)
    if request.method == 'POST':
        rule_name = request.form.get('rule_name')
        trigger_type = request.form.get('trigger_type')
        trigger_value = request.form.get('trigger_value')
        action_device_id = request.form.get('action_device')
        action_type = request.form.get('action_type')
        action_value = request.form.get('action_value', '')
        enabled = True
        # Generate new rule_id
        existing_ids = [int(r['rule_id']) for r in rules if r['rule_id'].isdigit()]
        new_id = str(max(existing_ids) + 1 if existing_ids else 1)
        new_rule = {
            'username': username,
            'rule_id': new_id,
            'rule_name': rule_name,
            'trigger_type': trigger_type,
            'trigger_value': trigger_value,
            'action_device_id': action_device_id,
            'action_type': action_type,
            'action_value': action_value,
            'enabled': enabled
        }
        rules.append(new_rule)
        write_automation_rules(rules)
        # Log activity
        log_activity(username, action_device_id, 'Automation Rule Added', f'Rule: {rule_name}')
        return redirect(url_for('automation_rules'))
    trigger_types = ['Time', 'Motion', 'Temperature']
    action_types = ['Turn On', 'Turn Off', 'Set Brightness', 'Set Temperature']
    return render_template('automation.html', rules=rules, devices=devices,
                           trigger_types=trigger_types, action_types=action_types, username=username)
@app.route('/energy', methods=['GET', 'POST'])
def energy_report():
    username = 'john_doe'
    energy_logs = read_energy_logs(username)
    devices = read_devices(username)
    filter_date = None
    if request.method == 'POST':
        filter_date = request.form.get('date_filter')
    filtered_logs = []
    total_consumption = 0.0
    for log in energy_logs:
        if filter_date and log['date'] != filter_date:
            continue
        filtered_logs.append(log)
        total_consumption += log['consumption_kwh']
    # Assume cost estimate $0.12 per kWh
    cost_estimate = total_consumption * 0.12
    # Map device_id to device_name for display
    device_map = {d['device_id']: d['device_name'] for d in devices}
    return render_template('energy_report.html',
                           energy_logs=filtered_logs,
                           total_consumption=total_consumption,
                           cost_estimate=cost_estimate,
                           device_map=device_map,
                           filter_date=filter_date,
                           username=username)
@app.route('/activity', methods=['GET', 'POST'])
def activity_logs():
    username = 'john_doe'
    logs = read_activity_logs(username)
    devices = read_devices(username)
    search_term = None
    if request.method == 'POST':
        search_term = request.form.get('search_activity', '').lower()
    filtered_logs = []
    for log in logs:
        if search_term:
            if (search_term in log['timestamp'].lower() or
                search_term in log['action'].lower() or
                search_term in log['details'].lower()):
                filtered_logs.append(log)
        else:
            filtered_logs.append(log)
    # Map device_id to device_name for display
    device_map = {d['device_id']: d['device_name'] for d in devices}
    return render_template('activity_logs.html',
                           logs=filtered_logs,
                           device_map=device_map,
                           search_term=search_term,
                           username=username)
def log_activity(username, device_id, action, details):
    filepath = os.path.join(DATA_DIR, 'activity_logs.txt')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    line = '|'.join([username, timestamp, device_id, action, details])
    with open(filepath, 'a') as f:
        f.write(line + '\n')
if __name__ == '__main__':
    app.run(debug=True)