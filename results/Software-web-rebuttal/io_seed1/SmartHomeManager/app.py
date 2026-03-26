'''
Main backend application for SmartHomeManager web application.
Defines routes for all pages starting from the Dashboard page at '/'.
Handles data loading from local text files in 'data' directory.
Ensures all frontend navigation buttons use backend routes.
'''
from flask import Flask, render_template, request, redirect, url_for
import os
import datetime
app = Flask(__name__)
DATA_DIR = 'data'
# Utility functions to load data from text files
def load_devices(username):
    devices = []
    devices_file = os.path.join(DATA_DIR, 'devices.txt')
    if os.path.exists(devices_file):
        with open(devices_file, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) < 13:
                    continue
                (user, device_id, device_name, device_type, room, brand, model,
                 status, power, brightness, temperature, mode, schedule_time) = parts
                if user == username:
                    devices.append({
                        'device_id': device_id,
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
    return devices
def load_rooms(username):
    rooms = []
    rooms_file = os.path.join(DATA_DIR, 'rooms.txt')
    if os.path.exists(rooms_file):
        with open(rooms_file, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) < 3:
                    continue
                user, room_id, room_name = parts
                if user == username:
                    rooms.append({
                        'room_id': room_id,
                        'room_name': room_name
                    })
    return rooms
def load_automation_rules(username):
    rules = []
    rules_file = os.path.join(DATA_DIR, 'automation_rules.txt')
    if os.path.exists(rules_file):
        with open(rules_file, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) < 9:
                    continue
                (user, rule_id, rule_name, trigger_type, trigger_value,
                 action_device_id, action_type, action_value, enabled) = parts
                if user == username:
                    rules.append({
                        'rule_id': rule_id,
                        'rule_name': rule_name,
                        'trigger_type': trigger_type,
                        'trigger_value': trigger_value,
                        'action_device_id': action_device_id,
                        'action_type': action_type,
                        'action_value': action_value,
                        'enabled': enabled.lower() == 'true'
                    })
    return rules
def load_energy_logs(username):
    logs = []
    energy_file = os.path.join(DATA_DIR, 'energy_logs.txt')
    if os.path.exists(energy_file):
        with open(energy_file, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) < 4:
                    continue
                user, device_id, date_str, consumption_kwh = parts
                if user == username:
                    logs.append({
                        'device_id': device_id,
                        'date': date_str,
                        'consumption_kwh': float(consumption_kwh)
                    })
    return logs
def load_activity_logs(username):
    logs = []
    activity_file = os.path.join(DATA_DIR, 'activity_logs.txt')
    if os.path.exists(activity_file):
        with open(activity_file, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) < 5:
                    continue
                user, timestamp, device_id, action, details = parts
                if user == username:
                    logs.append({
                        'timestamp': timestamp,
                        'device_id': device_id,
                        'action': action,
                        'details': details
                    })
    return logs
# For simplicity, assume a fixed logged-in user
LOGGED_IN_USER = 'john_doe'
@app.route('/')
def dashboard():
    devices = load_devices(LOGGED_IN_USER)
    rooms = load_rooms(LOGGED_IN_USER)
    total_devices = len(devices)
    active_devices = sum(1 for d in devices if d['status'].lower() == 'online')
    offline_devices = total_devices - active_devices
    # Count devices per room
    room_counts = {}
    for room in rooms:
        room_name = room['room_name']
        count = sum(1 for d in devices if d['room'] == room_name)
        room_counts[room_name] = count
    return render_template('dashboard.html',
                           total_devices=total_devices,
                           active_devices=active_devices,
                           offline_devices=offline_devices,
                           room_counts=room_counts)
@app.route('/devices')
def device_list():
    devices = load_devices(LOGGED_IN_USER)
    return render_template('device_list.html', devices=devices)
@app.route('/add-device', methods=['GET', 'POST'])
def add_device():
    rooms = load_rooms(LOGGED_IN_USER)
    device_types = ['Light', 'Thermostat', 'Camera', 'Lock', 'Sensor', 'Appliance']
    room_names = [room['room_name'] for room in rooms]
    if request.method == 'POST':
        device_name = request.form.get('device-name', '').strip()
        device_type = request.form.get('device-type', '')
        device_room = request.form.get('device-room', '')
        if not device_name or device_type not in device_types or device_room not in room_names:
            # Invalid input, reload form with error (simple approach)
            return render_template('add_device.html', rooms=room_names, device_types=device_types,
                                   error="Please fill all fields correctly.")
        # Generate new device_id
        devices = load_devices(LOGGED_IN_USER)
        existing_ids = [int(d['device_id']) for d in devices] if devices else []
        new_id = max(existing_ids) + 1 if existing_ids else 1
        # Append new device to devices.txt
        devices_file = os.path.join(DATA_DIR, 'devices.txt')
        with open(devices_file, 'a') as f:
            # Default values for brand, model, status, power, brightness, temperature, mode, schedule_time
            brand = ''
            model = ''
            status = 'Offline'
            power = 'off'
            brightness = ''
            temperature = ''
            mode = ''
            schedule_time = ''
            line = f"{LOGGED_IN_USER}|{new_id}|{device_name}|{device_type}|{device_room}|{brand}|{model}|{status}|{power}|{brightness}|{temperature}|{mode}|{schedule_time}\n"
            f.write(line)
        return redirect(url_for('device_list'))
    return render_template('add_device.html', rooms=room_names, device_types=device_types)
@app.route('/device-control/<device_id>', methods=['GET', 'POST'])
def device_control(device_id):
    devices = load_devices(LOGGED_IN_USER)
    device = None
    for d in devices:
        if d['device_id'] == device_id:
            device = d
            break
    if not device:
        return "Device not found", 404
    if request.method == 'POST':
        # Update device settings
        power = request.form.get('power-toggle', 'off')
        brightness = request.form.get('brightness', '')
        temperature = request.form.get('temperature', '')
        mode = request.form.get('mode', '')
        schedule_time = request.form.get('schedule_time', '')
        # Update devices.txt file
        devices_file = os.path.join(DATA_DIR, 'devices.txt')
        lines = []
        with open(devices_file, 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) < 13:
                    lines.append(line)
                    continue
                user, d_id = parts[0], parts[1]
                if user == LOGGED_IN_USER and d_id == device_id:
                    # Update line with new values
                    parts[8] = power
                    parts[9] = brightness
                    parts[10] = temperature
                    parts[11] = mode
                    parts[12] = schedule_time
                    # Update status based on power
                    parts[7] = 'Online' if power == 'on' else 'Offline'
                    line = '|'.join(parts) + '\n'
                lines.append(line)
        with open(devices_file, 'w') as f:
            f.writelines(lines)
        # Log activity
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        action = 'Settings Changed'
        details = f"Power: {power}, Brightness: {brightness}, Temperature: {temperature}, Mode: {mode}, Schedule: {schedule_time}"
        activity_file = os.path.join(DATA_DIR, 'activity_logs.txt')
        with open(activity_file, 'a') as f:
            f.write(f"{LOGGED_IN_USER}|{timestamp}|{device_id}|{action}|{details}\n")
        return redirect(url_for('device_list'))
    return render_template('device_control.html', device=device)
@app.route('/automation', methods=['GET', 'POST'])
def automation_rules():
    rules = load_automation_rules(LOGGED_IN_USER)
    devices = load_devices(LOGGED_IN_USER)
    device_options = [(d['device_id'], d['device_name']) for d in devices]
    trigger_types = ['Time', 'Motion', 'Temperature']
    action_types = ['Turn On', 'Turn Off', 'Set Brightness', 'Set Temperature']
    if request.method == 'POST':
        rule_name = request.form.get('rule-name', '').strip()
        trigger_type = request.form.get('trigger-type', '')
        trigger_value = request.form.get('trigger-value', '').strip()
        action_device_id = request.form.get('action-device', '')
        action_type = request.form.get('action-type', '')
        action_value = request.form.get('action-value', '').strip()
        if not rule_name or trigger_type not in trigger_types or not action_device_id or action_type not in action_types:
            return render_template('automation.html', rules=rules, devices=device_options,
                                   trigger_types=trigger_types, action_types=action_types,
                                   error="Please fill all fields correctly.")
        # Generate new rule_id
        existing_ids = [int(r['rule_id']) for r in rules] if rules else []
        new_id = max(existing_ids) + 1 if existing_ids else 1
        # Append new rule
        rules_file = os.path.join(DATA_DIR, 'automation_rules.txt')
        with open(rules_file, 'a') as f:
            enabled = 'true'
            line = f"{LOGGED_IN_USER}|{new_id}|{rule_name}|{trigger_type}|{trigger_value}|{action_device_id}|{action_type}|{action_value}|{enabled}\n"
            f.write(line)
        return redirect(url_for('automation_rules'))
    return render_template('automation.html', rules=rules, devices=device_options,
                           trigger_types=trigger_types, action_types=action_types)
@app.route('/energy', methods=['GET', 'POST'])
def energy_report():
    energy_logs = load_energy_logs(LOGGED_IN_USER)
    devices = load_devices(LOGGED_IN_USER)
    device_dict = {d['device_id']: d['device_name'] for d in devices}
    filtered_logs = energy_logs
    filter_date = None
    if request.method == 'POST':
        filter_date = request.form.get('date-filter', '')
        if filter_date:
            filtered_logs = [log for log in energy_logs if log['date'] == filter_date]
    total_consumption = sum(log['consumption_kwh'] for log in filtered_logs)
    # Assume cost estimate $0.12 per kWh
    cost_estimate = total_consumption * 0.12
    # Add device names to logs
    for log in filtered_logs:
        log['device_name'] = device_dict.get(log['device_id'], 'Unknown')
    return render_template('energy.html',
                           energy_logs=filtered_logs,
                           total_consumption=total_consumption,
                           cost_estimate=cost_estimate,
                           filter_date=filter_date)
@app.route('/activity', methods=['GET', 'POST'])
def activity_logs():
    logs = load_activity_logs(LOGGED_IN_USER)
    devices = load_devices(LOGGED_IN_USER)
    device_dict = {d['device_id']: d['device_name'] for d in devices}
    filtered_logs = logs
    search_term = ''
    if request.method == 'POST':
        search_term = request.form.get('search-activity', '').strip().lower()
        if search_term:
            filtered_logs = [log for log in logs if
                             search_term in log['action'].lower() or
                             search_term in log['details'].lower() or
                             search_term in device_dict.get(log['device_id'], '').lower()]
    # Add device names to logs
    for log in filtered_logs:
        log['device_name'] = device_dict.get(log['device_id'], 'Unknown')
    return render_template('activity.html', logs=filtered_logs, search_term=search_term)
if __name__ == '__main__':
    app.run(debug=True)