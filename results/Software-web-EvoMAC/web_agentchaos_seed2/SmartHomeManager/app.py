'''
Main backend Python application for SmartHomeManager web application using Flask.
Handles routing for all seven pages, manages reading/writing local text files in 'data' directory,
and implements business logic for device management, automation rules, energy consumption monitoring,
and activity logging.
'''
import os
from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
app = Flask(__name__)
app.secret_key = 'smart_home_secret_key'  # Needed for flashing messages
DATA_DIR = 'data'
# Utility functions for file operations and data parsing
def read_file_lines(filename):
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        return []
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.read().strip().split('\n')
        return [line for line in lines if line.strip() != '']
def write_file_lines(filename, lines):
    path = os.path.join(DATA_DIR, filename)
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n' if lines else '')
def parse_devices(username):
    lines = read_file_lines('devices.txt')
    devices = []
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
    lines = read_file_lines('rooms.txt')
    rooms = []
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
    lines = read_file_lines('automation_rules.txt')
    rules = []
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
    lines = read_file_lines('energy_logs.txt')
    logs = []
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
    lines = read_file_lines('activity_logs.txt')
    logs = []
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
def get_next_id(items, id_key):
    max_id = 0
    for item in items:
        try:
            current_id = int(item[id_key])
            if current_id > max_id:
                max_id = current_id
        except ValueError:
            continue
    return str(max_id + 1)
def save_devices(devices):
    lines = []
    for d in devices:
        line = '|'.join([
            d['username'],
            d['device_id'],
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
    write_file_lines('devices.txt', lines)
def save_automation_rules(rules):
    lines = []
    for r in rules:
        line = '|'.join([
            r['username'],
            r['rule_id'],
            r['rule_name'],
            r['trigger_type'],
            r['trigger_value'],
            r['action_device_id'],
            r['action_type'],
            r['action_value'],
            'true' if r['enabled'] else 'false'
        ])
        lines.append(line)
    write_file_lines('automation_rules.txt', lines)
def save_activity_log(username, device_id, action, details):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    line = '|'.join([username, timestamp, device_id, action, details])
    path = os.path.join(DATA_DIR, 'activity_logs.txt')
    with open(path, 'a', encoding='utf-8') as f:
        f.write(line + '\n')
# For simplicity, assume a fixed logged-in user for this demo
# In real app, implement authentication and session management
LOGGED_IN_USER = 'john_doe'
# ROUTES
@app.route('/')
def dashboard():
    username = LOGGED_IN_USER
    devices = parse_devices(username)
    rooms = parse_rooms(username)
    total_devices = len(devices)
    active_devices = sum(1 for d in devices if d['status'].lower() == 'online')
    offline_devices = total_devices - active_devices
    # Count devices per room
    room_device_counts = {}
    for room in rooms:
        count = sum(1 for d in devices if d['room'] == room['room_name'])
        room_device_counts[room['room_name']] = count
    return render_template('dashboard.html',
                           page_id='dashboard-page',
                           page_title='Smart Home Dashboard',
                           total_devices=total_devices,
                           active_devices=active_devices,
                           offline_devices=offline_devices,
                           room_device_counts=room_device_counts)
@app.route('/devices')
def device_list():
    username = LOGGED_IN_USER
    devices = parse_devices(username)
    return render_template('device_list.html',
                           page_id='device-list-page',
                           page_title='My Devices',
                           devices=devices)
@app.route('/devices/control/<device_id>', methods=['GET', 'POST'])
def device_control(device_id):
    username = LOGGED_IN_USER
    devices = parse_devices(username)
    device = next((d for d in devices if d['device_id'] == device_id), None)
    if not device:
        flash('Device not found.', 'error')
        return redirect(url_for('device_list'))
    if request.method == 'POST':
        # Handle power toggle and settings save
        power = request.form.get('power')
        brightness = request.form.get('brightness', '')
        temperature = request.form.get('temperature', '')
        mode = request.form.get('mode', '')
        schedule_time = request.form.get('schedule_time', '')
        # Update device info
        device['power'] = power if power in ['on', 'off'] else device['power']
        device['brightness'] = brightness if brightness.isdigit() else device['brightness']
        device['temperature'] = temperature if temperature.isdigit() else device['temperature']
        device['mode'] = mode if mode else device['mode']
        device['schedule_time'] = schedule_time if schedule_time else device['schedule_time']
        # Update status based on power
        device['status'] = 'Online' if device['power'] == 'on' else 'Offline'
        # Save devices back
        save_devices(devices)
        # Log activity
        save_activity_log(username, device_id, 'Settings Changed',
                          f"Power: {device['power']}, Brightness: {device['brightness']}, Temperature: {device['temperature']}, Mode: {device['mode']}, Schedule: {device['schedule_time']}")
        flash('Device settings saved.', 'success')
        return redirect(url_for('device_control', device_id=device_id))
    return render_template('device_control.html',
                           page_id='device-control-page',
                           page_title='Device Control',
                           device=device)
@app.route('/devices/control/<device_id>/toggle_power', methods=['POST'])
def toggle_power(device_id):
    username = LOGGED_IN_USER
    devices = parse_devices(username)
    device = next((d for d in devices if d['device_id'] == device_id), None)
    if not device:
        flash('Device not found.', 'error')
        return redirect(url_for('device_list'))
    # Toggle power
    new_power = 'off' if device['power'] == 'on' else 'on'
    device['power'] = new_power
    device['status'] = 'Online' if new_power == 'on' else 'Offline'
    save_devices(devices)
    save_activity_log(username, device_id, 'Power ' + ('On' if new_power == 'on' else 'Off'), 'Manual toggle')
    flash(f'Device power turned {new_power}.', 'success')
    return redirect(url_for('device_control', device_id=device_id))
@app.route('/devices/add', methods=['GET', 'POST'])
def add_device():
    username = LOGGED_IN_USER
    rooms = parse_rooms(username)
    devices = parse_devices(username)
    device_types = ['Light', 'Thermostat', 'Camera', 'Lock', 'Sensor', 'Appliance']
    room_names = [room['room_name'] for room in rooms]
    if not room_names:
        # If no rooms exist, provide default rooms as per requirements
        room_names = ['Living Room', 'Bedroom', 'Kitchen', 'Bathroom', 'Garage']
    if request.method == 'POST':
        device_name = request.form.get('device_name', '').strip()
        device_type = request.form.get('device_type', '')
        device_room = request.form.get('device_room', '')
        brand = request.form.get('brand', '').strip()
        model = request.form.get('model', '').strip()
        if not device_name or device_type not in device_types or device_room not in room_names:
            flash('Please fill all required fields correctly.', 'error')
            return render_template('add_device.html',
                                   page_id='add-device-page',
                                   page_title='Add New Device',
                                   device_types=device_types,
                                   room_names=room_names,
                                   device_name=device_name,
                                   device_type=device_type,
                                   device_room=device_room,
                                   brand=brand,
                                   model=model)
        # Assign new device_id
        new_device_id = get_next_id(devices, 'device_id')
        # Default values for new device
        status = 'Offline'
        power = 'off'
        brightness = ''
        temperature = ''
        mode = ''
        schedule_time = ''
        new_device = {
            'username': username,
            'device_id': new_device_id,
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
        save_devices(devices)
        flash('New device added successfully.', 'success')
        return redirect(url_for('device_list'))
    return render_template('add_device.html',
                           page_id='add-device-page',
                           page_title='Add New Device',
                           device_types=device_types,
                           room_names=room_names)
@app.route('/automation', methods=['GET', 'POST'])
def automation_rules():
    username = LOGGED_IN_USER
    rules = parse_automation_rules(username)
    devices = parse_devices(username)
    if request.method == 'POST':
        rule_name = request.form.get('rule_name', '').strip()
        trigger_type = request.form.get('trigger_type', '')
        trigger_value = request.form.get('trigger_value', '').strip()
        action_device_id = request.form.get('action_device', '')
        action_type = request.form.get('action_type', '')
        action_value = request.form.get('action_value', '').strip()
        trigger_types = ['Time', 'Motion', 'Temperature']
        action_types = ['Turn On', 'Turn Off', 'Set Brightness', 'Set Temperature']
        # Validate inputs
        if (not rule_name or trigger_type not in trigger_types or
            not trigger_value or action_device_id == '' or
            action_type not in action_types):
            flash('Please fill all required fields correctly.', 'error')
            return render_template('automation_rules.html',
                                   page_id='automation-page',
                                   page_title='Automation Rules',
                                   rules=rules,
                                   devices=devices)
        # Check if action_device_id exists for user
        if not any(d['device_id'] == action_device_id for d in devices):
            flash('Selected action device does not exist.', 'error')
            return render_template('automation_rules.html',
                                   page_id='automation-page',
                                   page_title='Automation Rules',
                                   rules=rules,
                                   devices=devices)
        new_rule_id = get_next_id(rules, 'rule_id')
        new_rule = {
            'username': username,
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
        flash('New automation rule added.', 'success')
        return redirect(url_for('automation_rules'))
    return render_template('automation_rules.html',
                           page_id='automation-page',
                           page_title='Automation Rules',
                           rules=rules,
                           devices=devices)
@app.route('/energy', methods=['GET', 'POST'])
def energy_report():
    username = LOGGED_IN_USER
    energy_logs = parse_energy_logs(username)
    devices = parse_devices(username)
    filter_date = None
    if request.method == 'POST':
        filter_date = request.form.get('date-filter', '').strip()
        if filter_date == '':
            filter_date = None
    # Filter logs by date if filter_date is set
    filtered_logs = []
    if filter_date:
        filtered_logs = [log for log in energy_logs if log['date'] == filter_date]
    else:
        filtered_logs = energy_logs
    # Calculate total consumption and cost estimate (assume cost per kWh = $0.12)
    total_consumption = sum(log['consumption_kwh'] for log in filtered_logs)
    cost_per_kwh = 0.12
    total_cost = total_consumption * cost_per_kwh
    # Prepare data for table: enrich with device name
    device_dict = {d['device_id']: d['device_name'] for d in devices}
    for log in filtered_logs:
        log['device_name'] = device_dict.get(log['device_id'], 'Unknown Device')
    return render_template('energy_report.html',
                           page_id='energy-page',
                           page_title='Energy Report',
                           energy_summary={
                               'total_consumption': round(total_consumption, 2),
                               'total_cost': round(total_cost, 2)
                           },
                           energy_logs=filtered_logs,
                           filter_date=filter_date)
@app.route('/activity', methods=['GET', 'POST'])
def activity_logs():
    username = LOGGED_IN_USER
    logs = parse_activity_logs(username)
    devices = parse_devices(username)
    search_term = ''
    if request.method == 'POST':
        search_term = request.form.get('search-activity', '').strip().lower()
    filtered_logs = []
    if search_term:
        for log in logs:
            # Search in device name, action, details
            device_name = next((d['device_name'] for d in devices if d['device_id'] == log['device_id']), '')
            if (search_term in device_name.lower() or
                search_term in log['action'].lower() or
                search_term in log['details'].lower()):
                filtered_logs.append(log)
    else:
        filtered_logs = logs
    # Enrich logs with device name
    device_dict = {d['device_id']: d['device_name'] for d in devices}
    for log in filtered_logs:
        log['device_name'] = device_dict.get(log['device_id'], 'Unknown Device')
    # Sort logs by timestamp descending
    filtered_logs.sort(key=lambda x: x['timestamp'], reverse=True)
    return render_template('activity_logs.html',
                           page_id='activity-page',
                           page_title='Activity Logs',
                           activity_logs=filtered_logs,
                           search_term=search_term)
# Run the app on local port 5000
if __name__ == '__main__':
    # Ensure data directory exists
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    app.run(host='0.0.0.0', port=5000, debug=True)