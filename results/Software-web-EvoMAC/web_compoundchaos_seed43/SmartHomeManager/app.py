'''
Main Flask application for SmartHomeManager web application.
Includes routing for all pages with root URL '/' serving the Dashboard page.
All frontend navigation uses Flask routing URLs for consistent navigation.
Handles device management, automation rules, activity logs, and energy reports
with data stored in local text files under the 'data' directory.
'''
from flask import Flask, render_template, request, redirect, url_for
import os
app = Flask(__name__)
# Directory where data files are stored
DATA_DIR = 'data'
# Ensure data directory exists
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)
# Helper function to read devices from devices.txt
def load_devices():
    devices = []
    devices_file = os.path.join(DATA_DIR, 'devices.txt')
    if os.path.exists(devices_file):
        with open(devices_file, 'r') as f:
            for line in f:
                # Each line format:
                # username|device_id|device_name|device_type|room|brand|model|status|power|brightness|temperature|mode|schedule_time
                parts = line.strip().split('|')
                if len(parts) >= 13:
                    device = {
                        'username': parts[0],
                        'device_id': int(parts[1]),
                        'device_name': parts[2],
                        'device_type': parts[3],
                        'room': parts[4],
                        'brand': parts[5],
                        'model': parts[6],
                        'status': parts[7],  # Online/Offline
                        'power': parts[8],   # on/off
                        'brightness': parts[9],
                        'temperature': parts[10],
                        'mode': parts[11],
                        'schedule_time': parts[12]
                    }
                    devices.append(device)
    return devices
# Helper function to read rooms from rooms.txt
def load_rooms():
    rooms = []
    rooms_file = os.path.join(DATA_DIR, 'rooms.txt')
    if os.path.exists(rooms_file):
        with open(rooms_file, 'r') as f:
            for line in f:
                # Format: username|room_id|room_name
                parts = line.strip().split('|')
                if len(parts) >= 3:
                    room = {
                        'username': parts[0],
                        'room_id': int(parts[1]),
                        'room_name': parts[2]
                    }
                    rooms.append(room)
    return rooms
# Helper function to read automation rules from automation_rules.txt
def load_automation_rules():
    rules = []
    rules_file = os.path.join(DATA_DIR, 'automation_rules.txt')
    if os.path.exists(rules_file):
        with open(rules_file, 'r') as f:
            for line in f:
                # Format:
                # username|rule_id|rule_name|trigger_type|trigger_value|action_device_id|action_type|action_value|enabled
                parts = line.strip().split('|')
                if len(parts) >= 9:
                    rule = {
                        'username': parts[0],
                        'rule_id': int(parts[1]),
                        'rule_name': parts[2],
                        'trigger_type': parts[3],
                        'trigger_value': parts[4],
                        'action_device_id': int(parts[5]),
                        'action_type': parts[6],
                        'action_value': parts[7],
                        'enabled': parts[8].lower() == 'true'
                    }
                    rules.append(rule)
    return rules
# Helper function to save automation rules to file
def save_automation_rules(rules):
    rules_file = os.path.join(DATA_DIR, 'automation_rules.txt')
    with open(rules_file, 'w') as f:
        for r in rules:
            line = '|'.join([
                r['username'],
                str(r['rule_id']),
                r['rule_name'],
                r['trigger_type'],
                r['trigger_value'],
                str(r['action_device_id']),
                r['action_type'],
                r['action_value'],
                'true' if r['enabled'] else 'false'
            ])
            f.write(line + '\n')
# Helper function to read activity logs from activity_logs.txt
def load_activity_logs():
    logs = []
    logs_file = os.path.join(DATA_DIR, 'activity_logs.txt')
    if os.path.exists(logs_file):
        with open(logs_file, 'r') as f:
            for line in f:
                # Format: username|timestamp|device_id|action|details
                parts = line.strip().split('|')
                if len(parts) >= 5:
                    log = {
                        'username': parts[0],
                        'timestamp': parts[1],
                        'device_id': int(parts[2]),
                        'action': parts[3],
                        'details': parts[4]
                    }
                    logs.append(log)
    return logs
# Helper function to read energy logs from energy_logs.txt
def load_energy_logs():
    energy_data = []
    energy_file = os.path.join(DATA_DIR, 'energy_logs.txt')
    if os.path.exists(energy_file):
        with open(energy_file, 'r') as f:
            for line in f:
                # Format: username|device_id|date|consumption_kwh
                parts = line.strip().split('|')
                if len(parts) >= 4:
                    try:
                        record = {
                            'username': parts[0],
                            'device_id': int(parts[1]),
                            'date': parts[2],
                            'consumption_kwh': float(parts[3])
                        }
                        energy_data.append(record)
                    except ValueError:
                        # Skip malformed lines
                        continue
    return energy_data
# Route: Home dashboard page
@app.route('/')
def dashboard():
    devices = load_devices()
    rooms = load_rooms()
    # Calculate device summary counts
    total_devices = len(devices)
    active_devices = sum(1 for d in devices if d['status'].lower() == 'online')
    offline_devices = total_devices - active_devices
    # Count devices per room
    room_device_counts = {}
    for room in rooms:
        count = sum(1 for d in devices if d['room'] == room['room_name'])
        room_device_counts[room['room_name']] = count
    return render_template('dashboard.html',
                           total_devices=total_devices,
                           active_devices=active_devices,
                           offline_devices=offline_devices,
                           room_device_counts=room_device_counts,
                           rooms=rooms)
# Route: List all devices for the user
@app.route('/device_list')
def device_list():
    devices = load_devices()
    return render_template('device_list.html', devices=devices)
# Route: Control a specific device by device_id
@app.route('/device_control/<int:device_id>', methods=['GET', 'POST'])
def device_control(device_id):
    devices = load_devices()
    device = next((d for d in devices if d['device_id'] == device_id), None)
    if not device:
        return "Device not found", 404
    if request.method == 'POST':
        # Process control commands from form submission
        power = request.form.get('power')
        brightness = request.form.get('brightness')
        temperature = request.form.get('temperature')
        mode = request.form.get('mode')
        # Update device data in devices.txt
        updated_devices = []
        for d in devices:
            if d['device_id'] == device_id:
                d['power'] = power if power is not None else d['power']
                d['brightness'] = brightness if brightness is not None else d['brightness']
                d['temperature'] = temperature if temperature is not None else d['temperature']
                d['mode'] = mode if mode is not None else d['mode']
            updated_devices.append(d)
        devices_file = os.path.join(DATA_DIR, 'devices.txt')
        with open(devices_file, 'w') as f:
            for d in updated_devices:
                line = '|'.join([
                    d['username'], str(d['device_id']), d['device_name'], d['device_type'],
                    d['room'], d['brand'], d['model'], d['status'], d['power'],
                    d['brightness'], d['temperature'], d['mode'], d['schedule_time']
                ])
                f.write(line + '\n')
        return redirect(url_for('device_control', device_id=device_id))
    # GET request: render device control page
    return render_template('device_control.html', device=device)
# Route: View and manage automation rules
@app.route('/automation_rules', methods=['GET', 'POST'])
def automation_rules():
    rules = load_automation_rules()
    devices = load_devices()
    if request.method == 'POST':
        # Extract form data for new rule
        username = request.form.get('username', 'default_user')
        rule_name = request.form.get('rule_name')
        trigger_type = request.form.get('trigger_type')
        trigger_value = request.form.get('trigger_value')
        action_device_id = request.form.get('action_device')
        action_type = request.form.get('action_type')
        action_value = request.form.get('action_value', '')
        enabled = request.form.get('enabled', 'true').lower() == 'true'
        # Validate and convert action_device_id and generate new rule_id
        try:
            action_device_id = int(action_device_id)
        except (ValueError, TypeError):
            action_device_id = 0
        if rules:
            new_rule_id = max(r['rule_id'] for r in rules) + 1
        else:
            new_rule_id = 1
        # Create new rule dictionary
        new_rule = {
            'username': username,
            'rule_id': new_rule_id,
            'rule_name': rule_name,
            'trigger_type': trigger_type,
            'trigger_value': trigger_value,
            'action_device_id': action_device_id,
            'action_type': action_type,
            'action_value': action_value,
            'enabled': enabled
        }
        # Append and save rules
        rules.append(new_rule)
        save_automation_rules(rules)
        return redirect(url_for('automation_rules'))
    return render_template('automation_rules.html', rules=rules, devices=devices)
# Route: Energy consumption report page
@app.route('/energy_report', methods=['GET', 'POST'])
def energy_report():
    energy_data = load_energy_logs()
    devices = load_devices()
    username_filter = None
    date_filter = None
    if request.method == 'POST':
        username_filter = request.form.get('username')
        date_filter = request.form.get('date')
        if username_filter:
            energy_data = [e for e in energy_data if e['username'] == username_filter]
        if date_filter:
            energy_data = [e for e in energy_data if e['date'] == date_filter]
    # Aggregate total consumption per device
    total_consumption = {}
    for record in energy_data:
        key = (record['username'], record['device_id'])
        total_consumption[key] = total_consumption.get(key, 0) + record['consumption_kwh']
    # Calculate total energy consumption and cost estimate (example cost: $0.12 per kWh)
    total_kwh = sum(record['consumption_kwh'] for record in energy_data)
    cost_per_kwh = 0.12
    total_cost = total_kwh * cost_per_kwh
    return render_template('energy_report.html',
                           energy_data=energy_data,
                           total_consumption=total_consumption,
                           total_kwh=total_kwh,
                           total_cost=total_cost,
                           devices=devices,
                           username_filter=username_filter,
                           date_filter=date_filter)
# Route: View activity logs
@app.route('/activity_logs', methods=['GET', 'POST'])
def activity_logs():
    logs = load_activity_logs()
    username_filter = None
    date_filter = None
    search_text = None
    if request.method == 'POST':
        username_filter = request.form.get('username')
        date_filter = request.form.get('date')
        search_text = request.form.get('search_text')
        if username_filter:
            logs = [log for log in logs if log['username'] == username_filter]
        if date_filter:
            logs = [log for log in logs if log['timestamp'].startswith(date_filter)]
        if search_text:
            search_lower = search_text.lower()
            logs = [log for log in logs if search_lower in log['action'].lower() or search_lower in log['details'].lower()]
    return render_template('activity_logs.html',
                           logs=logs,
                           username_filter=username_filter,
                           date_filter=date_filter,
                           search_text=search_text)
# Route: Add a new device
@app.route('/add_device', methods=['GET', 'POST'])
def add_device():
    rooms = load_rooms()
    if request.method == 'POST':
        # Extract device info from form
        username = request.form.get('username', 'default_user')
        device_name = request.form.get('device_name')
        device_type = request.form.get('device_type')
        room = request.form.get('room')
        brand = request.form.get('brand', '')
        model = request.form.get('model', '')
        status = 'Offline'  # Default status
        power = 'off'
        brightness = ''
        temperature = ''
        mode = ''
        schedule_time = ''
        # Generate new device_id (simple increment based on existing devices)
        devices = load_devices()
        if devices:
            new_id = max(d['device_id'] for d in devices) + 1
        else:
            new_id = 1
        # Append new device to devices.txt
        devices_file = os.path.join(DATA_DIR, 'devices.txt')
        with open(devices_file, 'a') as f:
            line = '|'.join([
                username, str(new_id), device_name, device_type, room, brand, model,
                status, power, brightness, temperature, mode, schedule_time
            ])
            f.write(line + '\n')
        return redirect(url_for('device_list'))
    # GET request: render add device form
    return render_template('add_device.html', rooms=rooms)
if __name__ == '__main__':
    # Run Flask app in debug mode for development
    app.run(debug=True)