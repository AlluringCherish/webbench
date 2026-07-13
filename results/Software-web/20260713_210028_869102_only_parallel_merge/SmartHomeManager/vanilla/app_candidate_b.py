from flask import Flask, render_template, redirect, url_for, request
import os
from datetime import datetime

app = Flask(__name__)
DATA_DIR = 'data'

CURRENT_USER = 'john_doe'  # For demo, fixed user

# Data loading utilities

def load_users():
    path = os.path.join(DATA_DIR, 'users.txt')
    users = {}
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                if not line.strip():
                    continue
                username, email = line.strip().split('|')
                users[username] = {'username': username, 'email': email}
    except FileNotFoundError:
        pass
    return users


def load_devices(username):
    path = os.path.join(DATA_DIR, 'devices.txt')
    devices = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                if not line.strip():
                    continue
                fields = line.strip().split('|')
                if len(fields) < 13:
                    continue
                (uname, device_id, device_name, device_type, room, brand, model, status,
                 power, brightness, temperature, mode, schedule_time) = fields
                if uname != username:
                    continue
                device = {
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
                    'schedule_time': schedule_time,
                }
                devices.append(device)
    except FileNotFoundError:
        pass
    return devices


def load_rooms(username):
    path = os.path.join(DATA_DIR, 'rooms.txt')
    rooms = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                if not line.strip():
                    continue
                uname, room_id, room_name = line.strip().split('|')
                if uname == username:
                    rooms.append({'room_id': room_id, 'room_name': room_name})
    except FileNotFoundError:
        pass
    return rooms


def load_automation_rules(username):
    path = os.path.join(DATA_DIR, 'automation_rules.txt')
    rules = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                if not line.strip():
                    continue
                (uname, rule_id, rule_name, trigger_type, trigger_value, action_device_id,
                 action_type, action_value, enabled) = line.strip().split('|')
                if uname != username:
                    continue
                rule = {
                    'rule_id': rule_id,
                    'rule_name': rule_name,
                    'trigger_type': trigger_type,
                    'trigger_value': trigger_value,
                    'action_device_id': action_device_id,
                    'action_type': action_type,
                    'action_value': action_value,
                    'enabled': enabled.lower() == 'true',
                }
                rules.append(rule)
    except FileNotFoundError:
        pass
    return rules


def load_energy_logs(username):
    path = os.path.join(DATA_DIR, 'energy_logs.txt')
    logs = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                if not line.strip():
                    continue
                uname, device_id, date_str, consumption_kwh = line.strip().split('|')
                if uname != username:
                    continue
                logs.append({'device_id': device_id, 'date': date_str, 'consumption_kwh': float(consumption_kwh)})
    except FileNotFoundError:
        pass
    return logs


def load_activity_logs(username):
    path = os.path.join(DATA_DIR, 'activity_logs.txt')
    logs = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                if not line.strip():
                    continue
                uname, timestamp, device_id, action, details = line.strip().split('|')
                if uname != username:
                    continue
                logs.append({'timestamp': timestamp, 'device_id': device_id, 'action': action, 'details': details})
    except FileNotFoundError:
        pass
    return logs


def find_device_by_id(devices, device_id):
    for d in devices:
        if d['device_id'] == device_id:
            return d
    return None


# Helper for device status summary

def summarize_devices(devices):
    total = len(devices)
    active = sum(1 for d in devices if d['status'].lower() == 'online')
    offline = total - active
    return {'total': total, 'active': active, 'offline': offline}


# Routes

@app.route('/')
def dashboard():
    devices = load_devices(CURRENT_USER)
    rooms = load_rooms(CURRENT_USER)
    device_summary = summarize_devices(devices)

    # Calculate device counts by room
    room_counts = {}
    for room in rooms:
        count = sum(1 for d in devices if d['room'] == room['room_name'])
        room_counts[room['room_name']] = count

    return render_template('dashboard.html',
                           devices=devices,
                           rooms=rooms,
                           device_summary=device_summary,
                           room_counts=room_counts)


@app.route('/devices')
def device_list():
    devices = load_devices(CURRENT_USER)
    return render_template('device_list.html', devices=devices)


@app.route('/devices/add', methods=['GET', 'POST'])
def add_device():
    # Device types and rooms fixed as per spec
    device_types = ['Light', 'Thermostat', 'Camera', 'Lock', 'Sensor', 'Appliance']
    rooms = ['Living Room', 'Bedroom', 'Kitchen', 'Bathroom', 'Garage']

    if request.method == 'POST':
        device_name = request.form.get('device-name', '').strip()
        device_type = request.form.get('device-type', '')
        device_room = request.form.get('device-room', '')

        if device_name and device_type in device_types and device_room in rooms:
            devices = load_devices(CURRENT_USER)
            # Generate new device_id
            try:
                new_id = str(max(int(d['device_id']) for d in devices) + 1)
            except ValueError:
                new_id = '1'

            # Append new device with default fields
            new_device_line = f"{CURRENT_USER}|{new_id}|{device_name}|{device_type}|{device_room}|Unknown|Unknown|Offline|off|||Auto|"

            path = os.path.join(DATA_DIR, 'devices.txt')
            with open(path, 'a', encoding='utf-8') as f:
                f.write(new_device_line + '\n')

            # Also add room if new room not in rooms.txt?
            # According to spec, rooms are fixed, so do not add new rooms file entries.

            return redirect(url_for('device_list'))

    return render_template('add_device.html', device_types=device_types, rooms=rooms)


@app.route('/devices/control/<device_id>', methods=['GET', 'POST'])
def device_control(device_id):
    devices = load_devices(CURRENT_USER)
    device = find_device_by_id(devices, device_id)
    if not device:
        return "Device not found", 404

    if request.method == 'POST':
        # Process power toggle and settings save
        # We'll simulate toggling power and saving brightness/temperature/mode/schedule
        power = device.get('power', 'off')
        new_power = request.form.get('power-toggle', None)
        if new_power:
            # Toggle power on/off
            device['power'] = 'off' if power == 'on' else 'on'

        # Save brightness, temperature, mode, schedule if provided
        brightness = request.form.get('brightness', device.get('brightness', ''))
        temperature = request.form.get('temperature', device.get('temperature', ''))
        mode = request.form.get('mode', device.get('mode', ''))
        schedule_time = request.form.get('schedule_time', device.get('schedule_time', ''))

        device['brightness'] = brightness
        device['temperature'] = temperature
        device['mode'] = mode
        device['schedule_time'] = schedule_time

        # Persist update to devices.txt
        # Read all lines, update the one matching device_id
        path = os.path.join(DATA_DIR, 'devices.txt')
        lines = []
        try:
            with open(path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except FileNotFoundError:
            lines = []

        with open(path, 'w', encoding='utf-8') as f:
            for line in lines:
                if not line.strip():
                    continue
                fields = line.strip().split('|')
                if fields[1] == device_id and fields[0] == CURRENT_USER:
                    # rebuild line
                    new_line = f"{CURRENT_USER}|{device_id}|{device['device_name']}|{device['device_type']}|{device['room']}|{device['brand']}|{device['model']}|{device['status']}|{device['power']}|{device['brightness']}|{device['temperature']}|{device['mode']}|{device['schedule_time']}|"
                    f.write(new_line + '\n')
                else:
                    f.write(line)

        return redirect(url_for('device_control', device_id=device_id))

    return render_template('device_control.html', device=device)


@app.route('/automation', methods=['GET', 'POST'])
def automation_rules():
    rules = load_automation_rules(CURRENT_USER)
    devices = load_devices(CURRENT_USER)

    device_choices = [(d['device_id'], d['device_name']) for d in devices]

    trigger_types = ['Time', 'Motion', 'Temperature']
    action_types = ['Turn On', 'Turn Off', 'Set Brightness', 'Set Temperature']

    if request.method == 'POST':
        rule_name = request.form.get('rule-name', '').strip()
        trigger_type = request.form.get('trigger-type', '')
        trigger_value = request.form.get('trigger-value', '').strip()
        action_device = request.form.get('action-device', '')
        action_type = request.form.get('action-type', '')

        if (rule_name and trigger_type in trigger_types and action_type in action_types
            and action_device in [d[0] for d in device_choices]):
            try:
                new_rule_id = str(max(int(r['rule_id']) for r in rules) + 1) if rules else '1'
            except ValueError:
                new_rule_id = '1'

            new_rule_line = f"{CURRENT_USER}|{new_rule_id}|{rule_name}|{trigger_type}|{trigger_value}|{action_device}|{action_type}||true"

            path = os.path.join(DATA_DIR, 'automation_rules.txt')
            with open(path, 'a', encoding='utf-8') as f:
                f.write(new_rule_line + '\n')

            return redirect(url_for('automation_rules'))

    return render_template('automation_rules.html', rules=rules, device_choices=device_choices,
                           trigger_types=trigger_types, action_types=action_types)


@app.route('/energy', methods=['GET', 'POST'])
def energy_report():
    energy_logs = load_energy_logs(CURRENT_USER)
    devices = load_devices(CURRENT_USER)
    filter_date = None
    filtered_logs = energy_logs

    if request.method == 'POST':
        filter_date = request.form.get('date-filter', '').strip()
        if filter_date:
            filtered_logs = [log for log in energy_logs if log['date'] == filter_date]

    # Compute total consumption and approximate cost (e.g., rate $0.12/kWh)
    total_consumption = sum(log['consumption_kwh'] for log in filtered_logs) if filtered_logs else 0.0
    total_cost = total_consumption * 0.12

    # Enrich logs with device names
    device_map = {d['device_id']: d['device_name'] for d in devices}
    for log in filtered_logs:
        log['device_name'] = device_map.get(log['device_id'], 'Unknown')

    return render_template('energy_report.html', energy_logs=filtered_logs,
                           total_consumption=total_consumption, total_cost=total_cost,
                           filter_date=filter_date)


@app.route('/activity', methods=['GET', 'POST'])
def activity_logs():
    logs = load_activity_logs(CURRENT_USER)
    devices = load_devices(CURRENT_USER)

    search_query = ''
    filtered_logs = logs

    if request.method == 'POST':
        search_query = request.form.get('search-activity', '').strip().lower()
        if search_query:
            filtered_logs = [log for log in logs if search_query in log['action'].lower() or search_query in log['details'].lower()]

    # Enrich with device names
    device_map = {d['device_id']: d['device_name'] for d in devices}
    for log in filtered_logs:
        log['device_name'] = device_map.get(log['device_id'], 'Unknown')

    return render_template('activity_logs.html', logs=filtered_logs, search_query=search_query)


if __name__ == '__main__':
    app.run(debug=True)
