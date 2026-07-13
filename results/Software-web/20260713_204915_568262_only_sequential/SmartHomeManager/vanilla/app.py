from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

# Since no login system is specified, use a fixed username for demo
CURRENT_USERNAME = 'john_doe'

DATA_DIR = 'data'

DEVICE_TYPES = ['Light', 'Thermostat', 'Camera', 'Lock', 'Sensor', 'Appliance']
ROOMS = ['Living Room', 'Bedroom', 'Kitchen', 'Bathroom', 'Garage']

# Utility functions for file handling

def safe_read_file_lines(filepath):
    if not os.path.exists(filepath):
        return []
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.read().strip()
        if not lines:
            return []
        return lines.split('\n')

def safe_write_file_lines(filepath, lines):
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

def parse_pipe_line(line):
    return line.split('|')

def join_pipe_line(fields):
    return '|'.join(fields)

# Data loaders and savers for each data type

def load_devices(username):
    path = os.path.join(DATA_DIR, 'devices.txt')
    devices = []
    for line in safe_read_file_lines(path):
        parts = parse_pipe_line(line)
        if len(parts) < 13:
            continue
        if parts[0] == username:
            devices.append({
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
            })
    return devices

def save_devices(username, devices):
    path = os.path.join(DATA_DIR, 'devices.txt')
    # We replace all lines for this user
    all_lines = safe_read_file_lines(path)
    new_lines = []
    for line in all_lines:
        parts = parse_pipe_line(line)
        if parts[0] != username:
            new_lines.append(line)
    # Add updated devices
    for d in devices:
        fields = [d['username'], d['device_id'], d['device_name'], d['device_type'], d['room'], d['brand'], d['model'], d['status'], d['power'], d['brightness'], d['temperature'], d['mode'], d['schedule_time']]
        new_lines.append(join_pipe_line(fields))
    safe_write_file_lines(path, new_lines)


def load_rooms(username):
    path = os.path.join(DATA_DIR, 'rooms.txt')
    rooms = []
    for line in safe_read_file_lines(path):
        parts = parse_pipe_line(line)
        if len(parts) < 3:
            continue
        if parts[0] == username:
            rooms.append({
                'username': parts[0],
                'room_id': parts[1],
                'room_name': parts[2]
            })
    return rooms

# Automation Rules

def load_automation_rules(username):
    path = os.path.join(DATA_DIR, 'automation_rules.txt')
    rules = []
    for line in safe_read_file_lines(path):
        parts = parse_pipe_line(line)
        if len(parts) < 9:
            continue
        if parts[0] == username:
            rules.append({
                'username': parts[0],
                'rule_id': parts[1],
                'rule_name': parts[2],
                'trigger_type': parts[3],
                'trigger_value': parts[4],
                'action_device_id': parts[5],
                'action_type': parts[6],
                'action_value': parts[7],
                'enabled': parts[8] == 'true'
            })
    return rules

def save_automation_rules(username, rules):
    path = os.path.join(DATA_DIR, 'automation_rules.txt')
    all_lines = safe_read_file_lines(path)
    new_lines = []
    for line in all_lines:
        parts = parse_pipe_line(line)
        if parts[0] != username:
            new_lines.append(line)
    for r in rules:
        fields = [r['username'], r['rule_id'], r['rule_name'], r['trigger_type'], r['trigger_value'], r['action_device_id'], r['action_type'], r['action_value'], 'true' if r['enabled'] else 'false']
        new_lines.append(join_pipe_line(fields))
    safe_write_file_lines(path, new_lines)

# Energy Logs

def load_energy_logs(username):
    path = os.path.join(DATA_DIR, 'energy_logs.txt')
    logs = []
    for line in safe_read_file_lines(path):
        parts = parse_pipe_line(line)
        if len(parts) < 4:
            continue
        if parts[0] == username:
            try:
                consumption = float(parts[3])
            except ValueError:
                consumption = 0.0
            logs.append({
                'username': parts[0],
                'device_id': parts[1],
                'date': parts[2],
                'consumption_kwh': consumption
            })
    return logs

# Activity Logs

def load_activity_logs(username):
    path = os.path.join(DATA_DIR, 'activity_logs.txt')
    logs = []
    for line in safe_read_file_lines(path):
        parts = parse_pipe_line(line)
        if len(parts) < 5:
            continue
        if parts[0] == username:
            logs.append({
                'username': parts[0],
                'timestamp': parts[1],
                'device_id': parts[2],
                'action': parts[3],
                'details': parts[4],
            })
    return logs

# Routes

@app.route('/')
def root():
    return redirect(url_for('dashboard_page'))

# 1. Dashboard Page
@app.route('/dashboard')
def dashboard_page():
    devices = load_devices(CURRENT_USERNAME)
    rooms = load_rooms(CURRENT_USERNAME)

    total_devices = len(devices)
    active_devices = sum(1 for d in devices if d['status'].lower() == 'online')
    offline_devices = total_devices - active_devices

    # Count devices per room
    room_device_counts = {}
    for room in rooms:
        room_device_counts[room['room_name']] = 0
    for d in devices:
        if d['room'] in room_device_counts:
            room_device_counts[d['room']] += 1

    return render_template('dashboard.html',
                           total_devices=total_devices,
                           active_devices=active_devices,
                           offline_devices=offline_devices,
                           rooms=rooms,
                           room_device_counts=room_device_counts)

# 2. Device List Page
@app.route('/devices')
def device_list_page():
    devices = load_devices(CURRENT_USERNAME)
    return render_template('device_list.html', devices=devices)

# 3. Add Device Page
@app.route('/devices/add', methods=['GET', 'POST'])
def add_device_page():
    if request.method == 'POST':
        device_name = request.form.get('device-name', '').strip()
        device_type = request.form.get('device-type', '')
        device_room = request.form.get('device-room', '')

        if device_name and device_type in DEVICE_TYPES and device_room in ROOMS:
            devices = load_devices(CURRENT_USERNAME)

            existing_ids = [int(d['device_id']) for d in devices if d['device_id'].isdigit()]
            new_id = str(max(existing_ids, default=0) + 1)

            new_device = {
                'username': CURRENT_USERNAME,
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
            save_devices(CURRENT_USERNAME, devices)

            return redirect(url_for('device_list_page'))

    return render_template('add_device.html', device_types=DEVICE_TYPES, rooms=ROOMS)

# 4. Device Control Page
@app.route('/devices/control/<device_id>', methods=['GET', 'POST'])
def device_control_page(device_id):
    devices = load_devices(CURRENT_USERNAME)
    device = next((d for d in devices if d['device_id'] == device_id), None)
    if not device:
        return "Device not found", 404

    if request.method == 'POST':
        # Toggle power button submits 'power-toggle' with current power state
        if 'power-toggle' in request.form:
            # Toggle power
            device['power'] = 'off' if device.get('power') == 'on' else 'on'

        # Save settings button
        if 'save-settings-button' in request.form:
            # Save any settings depending on device type
            # For simplicity, we only update brightness or temperature for relevant devices
            if device['device_type'] == 'Light':
                brightness = request.form.get('brightness', '')
                device['brightness'] = brightness if brightness.isdigit() else device.get('brightness', '')
            elif device['device_type'] == 'Thermostat':
                temperature = request.form.get('temperature', '')
                device['temperature'] = temperature if temperature.isdigit() else device.get('temperature', '')

        save_devices(CURRENT_USERNAME, devices)

    # Prepare data for display
    device_name = device.get('device_name', '')
    device_status = device.get('status', 'Offline')
    power_state = device.get('power', 'off')
    brightness = device.get('brightness', '')
    temperature = device.get('temperature', '')

    return render_template('device_control.html', device=device, device_name=device_name, device_status=device_status, power_state=power_state, brightness=brightness, temperature=temperature)

# 5. Automation Rules Page
@app.route('/automation', methods=['GET', 'POST'])
def automation_page():
    devices = load_devices(CURRENT_USERNAME)
    rules = load_automation_rules(CURRENT_USERNAME)

    if request.method == 'POST':
        rule_name = request.form.get('rule-name', '').strip()
        trigger_type = request.form.get('trigger-type', '')
        trigger_value = request.form.get('trigger-value', '').strip()
        action_device_id = request.form.get('action-device', '')
        action_type = request.form.get('action-type', '')

        if rule_name and trigger_type and action_device_id and action_type:
            existing_rule_ids = [int(r['rule_id']) for r in rules if r['rule_id'].isdigit()]
            new_rule_id = str(max(existing_rule_ids, default=0) + 1)
            new_rule = {
                'username': CURRENT_USERNAME,
                'rule_id': new_rule_id,
                'rule_name': rule_name,
                'trigger_type': trigger_type,
                'trigger_value': trigger_value,
                'action_device_id': action_device_id,
                'action_type': action_type,
                'action_value': '',
                'enabled': True
            }
            rules.append(new_rule)
            save_automation_rules(CURRENT_USERNAME, rules)

            return redirect(url_for('automation_page'))

    return render_template('automation.html', rules=rules, devices=devices)

# 6. Energy Report Page
@app.route('/energy', methods=['GET', 'POST'])
def energy_page():
    devices = load_devices(CURRENT_USERNAME)
    logs = load_energy_logs(CURRENT_USERNAME)

    filtered_date = None
    filtered_logs = logs

    if request.method == 'POST':
        filtered_date = request.form.get('date-filter', '').strip()
        if filtered_date:
            filtered_logs = [log for log in logs if log['date'] == filtered_date]

    # Calculate total consumption and cost estimate (assume $0.12 per kWh)
    total_consumption = sum(log['consumption_kwh'] for log in filtered_logs)
    total_cost = total_consumption * 0.12

    # Map device_id to device_name for display
    device_id_to_name = {d['device_id']: d['device_name'] for d in devices}

    return render_template('energy.html', energy_logs=filtered_logs, total_consumption=total_consumption, total_cost=total_cost, device_id_to_name=device_id_to_name, filtered_date=filtered_date)

# 7. Activity Logs Page
@app.route('/activity', methods=['GET', 'POST'])
def activity_page():
    devices = load_devices(CURRENT_USERNAME)
    logs = load_activity_logs(CURRENT_USERNAME)

    search_filter = ''
    filtered_logs = logs

    if request.method == 'POST':
        search_filter = request.form.get('search-activity', '').strip().lower()
        if search_filter:
            filtered_logs = [log for log in logs if search_filter in log['action'].lower() or search_filter in log['details'].lower()]

    device_id_to_name = {d['device_id']: d['device_name'] for d in devices}

    return render_template('activity.html', activity_logs=filtered_logs, device_id_to_name=device_id_to_name, search_filter=search_filter)

if __name__ == '__main__':
    os.makedirs(DATA_DIR, exist_ok=True)
    app.run(debug=True)
