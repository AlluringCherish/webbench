'''
Main SmartHomeManager web application routing with Flask.
Handles all frontend navigation URLs defined in the specification.
Implements dashboard (with POST), energy_report, activity_logs, device_list,
add_device, device_control, and automation_rules routes.
Loads and saves data from/to local files in 'data' directory.
Renders corresponding HTML templates.
Creates 'data' directory if it does not exist.
'''
from flask import Flask, render_template, request, redirect, url_for
import os
import datetime
app = Flask(__name__)
DATA_DIR = 'data'
USERS_FILE = os.path.join(DATA_DIR, 'users.txt')
DEVICES_FILE = os.path.join(DATA_DIR, 'devices.txt')
AUTOMATION_FILE = os.path.join(DATA_DIR, 'automation_rules.txt')
ENERGY_LOGS_FILE = os.path.join(DATA_DIR, 'energy_logs.txt')
ACTIVITY_LOGS_FILE = os.path.join(DATA_DIR, 'activity_logs.txt')
ROOMS_FILE = os.path.join(DATA_DIR, 'rooms.txt')
def ensure_data_dir():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
def load_users():
    users = []
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            for line in f:
                line=line.strip()
                if line:
                    parts = line.split('|')
                    if len(parts) >= 2:
                        users.append({'username': parts[0], 'email': parts[1]})
    return users
def load_devices():
    devices = []
    if os.path.exists(DEVICES_FILE):
        with open(DEVICES_FILE, 'r') as f:
            for line in f:
                line=line.strip()
                if line:
                    parts = line.split('|')
                    # Expected format:
                    # username|device_id|device_name|device_type|room|brand|model|status|power|brightness|temperature|mode|schedule_time
                    if len(parts) >= 13:
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
def load_rooms():
    rooms = []
    if os.path.exists(ROOMS_FILE):
        with open(ROOMS_FILE, 'r') as f:
            for line in f:
                line=line.strip()
                if line:
                    parts = line.split('|')
                    if len(parts) >= 3:
                        rooms.append({
                            'username': parts[0],
                            'room_id': parts[1],
                            'room_name': parts[2]
                        })
    return rooms
def load_automation_rules():
    rules = []
    if os.path.exists(AUTOMATION_FILE):
        with open(AUTOMATION_FILE, 'r') as f:
            for line in f:
                line=line.strip()
                if line:
                    parts = line.split('|')
                    # username|rule_id|rule_name|trigger_type|trigger_value|action_device_id|action_type|action_value|enabled
                    if len(parts) >= 9:
                        rules.append({
                            'username': parts[0],
                            'rule_id': parts[1],
                            'rule_name': parts[2],
                            'trigger_type': parts[3],
                            'trigger_value': parts[4],
                            'action_device_id': parts[5],
                            'action_type': parts[6],
                            'action_value': parts[7],
                            'enabled': parts[8]
                        })
    return rules
def load_energy_logs():
    energy_logs = []
    if os.path.exists(ENERGY_LOGS_FILE):
        with open(ENERGY_LOGS_FILE, 'r') as f:
            for line in f:
                line=line.strip()
                if line:
                    parts = line.split('|')
                    # username|device_id|date|consumption_kwh
                    if len(parts) == 4:
                        try:
                            consumption = float(parts[3])
                        except ValueError:
                            consumption = 0.0
                        energy_logs.append({
                            'username': parts[0],
                            'device_id': parts[1],
                            'date': parts[2],
                            'consumption_kwh': consumption
                        })
    return energy_logs
def load_activity_logs():
    activity_logs = []
    if os.path.exists(ACTIVITY_LOGS_FILE):
        with open(ACTIVITY_LOGS_FILE, 'r') as f:
            for line in f:
                line=line.strip()
                if line:
                    parts = line.split('|')
                    # username|timestamp|device_id|action|details
                    if len(parts) == 5:
                        activity_logs.append({
                            'username': parts[0],
                            'timestamp': parts[1],
                            'device_id': parts[2],
                            'action': parts[3],
                            'details': parts[4]
                        })
    return activity_logs
def save_devices(devices):
    with open(DEVICES_FILE, 'w') as f:
        for d in devices:
            line = '|'.join([
                d.get('username',''),
                d.get('device_id',''),
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
                d.get('schedule_time','')
            ])
            f.write(line + '\n')
def save_automation_rules(rules):
    with open(AUTOMATION_FILE, 'w') as f:
        for r in rules:
            line = '|'.join([
                r.get('username',''),
                r.get('rule_id',''),
                r.get('rule_name',''),
                r.get('trigger_type',''),
                r.get('trigger_value',''),
                r.get('action_device_id',''),
                r.get('action_type',''),
                r.get('action_value',''),
                r.get('enabled','')
            ])
            f.write(line + '\n')
@app.route('/', methods=['GET', 'POST'])
def dashboard():
    ensure_data_dir()
    users = load_users()
    devices = load_devices()
    rooms = load_rooms()
    # For demo, assume single user 'john_doe'
    username = 'john_doe'
    user_devices = [d for d in devices if d['username'] == username]
    total_devices = len(user_devices)
    online_devices = sum(1 for d in user_devices if d['status'].lower() == 'online')
    offline_devices = total_devices - online_devices
    # Prepare room list with device counts
    user_rooms = [r for r in rooms if r['username'] == username]
    room_list = []
    for room in user_rooms:
        count = sum(1 for d in user_devices if d['room'] == room['room_name'])
        room_list.append({'room_name': room['room_name'], 'device_count': count})
    # POST can be used for filtering or other dashboard actions if needed
    if request.method == 'POST':
        # For now, no specific POST action defined in spec
        pass
    return render_template('dashboard.html',
                           total_devices=total_devices,
                           online_devices=online_devices,
                           offline_devices=offline_devices,
                           username=username,
                           rooms=room_list)
@app.route('/devices', methods=['GET'])
def device_list():
    ensure_data_dir()
    devices = load_devices()
    username = 'john_doe'  # demo user
    user_devices = [d for d in devices if d['username'] == username]
    return render_template('device_list.html', devices=user_devices)
@app.route('/add_device', methods=['GET', 'POST'])
def add_device():
    ensure_data_dir()
    devices = load_devices()
    rooms = load_rooms()
    username = 'john_doe'  # demo user
    user_rooms = [r for r in rooms if r['username'] == username]
    if request.method == 'POST':
        device_name = request.form.get('device_name')
        device_type = request.form.get('device_type')
        device_room = request.form.get('device_room')
        if not (device_name and device_type and device_room):
            # Missing data, reload form with error (simple approach)
            return render_template('add_device.html', rooms=user_rooms, error="All fields are required.")
        # Generate new device_id (max existing + 1)
        user_devices = [d for d in devices if d['username'] == username]
        max_id = 0
        for d in user_devices:
            try:
                did = int(d['device_id'])
                if did > max_id:
                    max_id = did
            except ValueError:
                continue
        new_device_id = str(max_id + 1)
        # Default values for new device
        new_device = {
            'username': username,
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
        devices.append(new_device)
        save_devices(devices)
        return redirect(url_for('device_list'))
    return render_template('add_device.html', rooms=user_rooms)
@app.route('/device_control/<device_id>', methods=['GET', 'POST'])
def device_control(device_id):
    ensure_data_dir()
    devices = load_devices()
    username = 'john_doe'  # demo user
    device = None
    for d in devices:
        if d['username'] == username and d['device_id'] == device_id:
            device = d
            break
    if not device:
        return "Device not found", 404
    if request.method == 'POST':
        # Handle power toggle
        if 'power_toggle' in request.form:
            if device['power'] == 'on':
                device['power'] = 'off'
                device['status'] = 'Offline'
            else:
                device['power'] = 'on'
                device['status'] = 'Online'
        # Handle settings save
        if 'save-settings-button' in request.form or 'brightness' in request.form or 'temperature' in request.form:
            if device['device_type'] == 'Light':
                brightness = request.form.get('brightness')
                if brightness is not None:
                    try:
                        b_val = int(brightness)
                        if 0 <= b_val <= 100:
                            device['brightness'] = str(b_val)
                    except ValueError:
                        pass
            elif device['device_type'] == 'Thermostat':
                temperature = request.form.get('temperature')
                if temperature is not None:
                    try:
                        t_val = int(temperature)
                        device['temperature'] = str(t_val)
                    except ValueError:
                        pass
        save_devices(devices)
        return redirect(url_for('device_control', device_id=device_id))
    return render_template('device_control.html', device=device)
@app.route('/automation', methods=['GET', 'POST'])
def automation_rules():
    ensure_data_dir()
    rules = load_automation_rules()
    devices = load_devices()
    username = 'john_doe'  # demo user
    user_rules = [r for r in rules if r['username'] == username]
    user_devices = [d for d in devices if d['username'] == username]
    if request.method == 'POST':
        rule_name = request.form.get('rule_name')
        trigger_type = request.form.get('trigger_type')
        trigger_value = request.form.get('trigger_value')
        action_device = request.form.get('action_device')
        action_type = request.form.get('action_type')
        if not (rule_name and trigger_type and trigger_value and action_device and action_type):
            # Missing data, reload with error
            return render_template('automation_rules.html', rules=user_rules, devices=user_devices, error="All fields are required.")
        # Generate new rule_id (max existing + 1)
        max_id = 0
        for r in user_rules:
            try:
                rid = int(r['rule_id'])
                if rid > max_id:
                    max_id = rid
            except ValueError:
                continue
        new_rule_id = str(max_id + 1)
        # Determine action_value for Set Brightness or Set Temperature, else empty
        action_value = ''
        if action_type in ['Set Brightness', 'Set Temperature']:
            action_value = request.form.get('action_value', '')
            # If action_value not provided in form, try to get from trigger_value or empty
            if not action_value:
                action_value = ''
        new_rule = {
            'username': username,
            'rule_id': new_rule_id,
            'rule_name': rule_name,
            'trigger_type': trigger_type,
            'trigger_value': trigger_value,
            'action_device_id': action_device,
            'action_type': action_type,
            'action_value': action_value,
            'enabled': 'true'
        }
        rules.append(new_rule)
        save_automation_rules(rules)
        return redirect(url_for('automation_rules'))
    return render_template('automation_rules.html', rules=user_rules, devices=user_devices)
@app.route('/energy', methods=['GET', 'POST'])
def energy_report():
    ensure_data_dir()
    energy_logs = load_energy_logs()
    devices = load_devices()
    username = 'john_doe'  # demo user
    user_energy_logs = [log for log in energy_logs if log['username'] == username]
    # Filter by date if POST with date filter
    filter_date = None
    if request.method == 'POST':
        filter_date = request.form.get('date_filter')
        if filter_date:
            user_energy_logs = [log for log in user_energy_logs if log['date'] == filter_date]
    # Aggregate total consumption and cost (assuming cost per kWh = 0.15)
    total_consumption = sum(log['consumption_kwh'] for log in user_energy_logs)
    total_cost = total_consumption * 0.15
    # Map device_id to device_name for display
    device_map = {d['device_id']: d['device_name'] for d in devices if d['username'] == username}
    # Prepare logs with device names
    logs_with_names = []
    for log in user_energy_logs:
        logs_with_names.append({
            'device_name': device_map.get(log['device_id'], 'Unknown'),
            'date': log['date'],
            'consumption_kwh': log['consumption_kwh']
        })
    return render_template('energy_report.html',
                           energy_logs=logs_with_names,
                           total_consumption=total_consumption,
                           total_cost=total_cost,
                           filter_date=filter_date)
@app.route('/activity', methods=['GET', 'POST'])
def activity_logs():
    ensure_data_dir()
    activity_logs = load_activity_logs()
    devices = load_devices()
    username = 'john_doe'  # demo user
    user_activity_logs = [log for log in activity_logs if log['username'] == username]
    search_filter = None
    if request.method == 'POST':
        search_filter = request.form.get('search_filter')
        if search_filter:
            search_filter_lower = search_filter.lower()
            user_activity_logs = [log for log in user_activity_logs if
                                  search_filter_lower in log['action'].lower() or
                                  search_filter_lower in log['details'].lower()]
    # Map device_id to device_name for display
    device_map = {d['device_id']: d['device_name'] for d in devices if d['username'] == username}
    logs_with_names = []
    for log in user_activity_logs:
        logs_with_names.append({
            'timestamp': log['timestamp'],
            'device_name': device_map.get(log['device_id'], 'Unknown'),
            'action': log['action'],
            'details': log['details']
        })
    return render_template('activity_logs.html',
                           activity_logs=logs_with_names,
                           search_filter=search_filter)
if __name__ == '__main__':
    ensure_data_dir()
    app.run(debug=True, port=5000)