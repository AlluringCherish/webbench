import os
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'
USERS_FILE = os.path.join(DATA_DIR, 'users.txt')
DEVICES_FILE = os.path.join(DATA_DIR, 'devices.txt')
ROOMS_FILE = os.path.join(DATA_DIR, 'rooms.txt')
AUTOMATION_RULES_FILE = os.path.join(DATA_DIR, 'automation_rules.txt')
ENERGY_LOGS_FILE = os.path.join(DATA_DIR, 'energy_logs.txt')
ACTIVITY_LOGS_FILE = os.path.join(DATA_DIR, 'activity_logs.txt')

# Helper functions to load and save data

def load_users():
    users = []
    try:
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 2:
                    continue
                username, email = parts
                users.append({'username': username, 'email': email})
    except FileNotFoundError:
        pass
    return users


def load_devices(username):
    devices = []
    try:
        with open(DEVICES_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 13:
                    continue
                (u, device_id, device_name, device_type, room, brand, model, status, power,
                 brightness, temperature, mode, schedule_time) = parts
                if u != username:
                    continue
                try:
                    device_id_i = int(device_id)
                except ValueError:
                    continue
                devices.append({
                    'username': u,
                    'device_id': device_id_i,
                    'device_name': device_name,
                    'device_type': device_type,
                    'room': room,
                    'brand': brand,
                    'model': model,
                    'status': status,
                    'power': power,
                    'brightness': brightness if brightness != '' else None,
                    'temperature': temperature if temperature != '' else None,
                    'mode': mode,
                    'schedule_time': schedule_time if schedule_time != '' else None
                })
    except FileNotFoundError:
        pass
    return devices


def save_devices(username, devices):
    all_devices = []
    try:
        with open(DEVICES_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 13:
                    continue
                all_devices.append(parts)
    except FileNotFoundError:
        pass

    # Remove devices of the user
    all_devices = [d for d in all_devices if d[0] != username]

    for d in devices:
        all_devices.append([
            d['username'],
            str(d['device_id']),
            d['device_name'],
            d['device_type'],
            d['room'],
            d['brand'],
            d['model'],
            d['status'],
            d['power'],
            d['brightness'] if d['brightness'] is not None else '',
            d['temperature'] if d['temperature'] is not None else '',
            d['mode'],
            d['schedule_time'] if d['schedule_time'] is not None else ''
        ])

    try:
        with open(DEVICES_FILE, 'w', encoding='utf-8') as f:
            for d in all_devices:
                f.write('|'.join(d) + '\n')
    except Exception:
        pass


def load_rooms(username):
    rooms = []
    try:
        with open(ROOMS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 3:
                    continue
                u, room_id, room_name = parts
                if u != username:
                    continue
                try:
                    room_id_i = int(room_id)
                except ValueError:
                    continue
                rooms.append({'username': u, 'room_id': room_id_i, 'room_name': room_name})
    except FileNotFoundError:
        pass
    return rooms


def load_automation_rules(username):
    rules = []
    try:
        with open(AUTOMATION_RULES_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 9:
                    continue
                (u, rule_id, rule_name, trigger_type, trigger_value, action_device_id, action_type, action_value, enabled) = parts
                if u != username:
                    continue
                try:
                    rule_id_i = int(rule_id)
                    action_device_id_i = int(action_device_id)
                    enabled_bool = True if enabled.lower() == 'true' else False
                except ValueError:
                    continue
                rules.append({
                    'username': u,
                    'rule_id': rule_id_i,
                    'rule_name': rule_name,
                    'trigger_type': trigger_type,
                    'trigger_value': trigger_value,
                    'action_device_id': action_device_id_i,
                    'action_type': action_type,
                    'action_value': action_value if action_value != '' else None,
                    'enabled': enabled_bool
                })
    except FileNotFoundError:
        pass
    return rules


def load_energy_logs(username):
    energy_entries = []
    try:
        with open(ENERGY_LOGS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 4:
                    continue
                u, device_id, date, consumption_kwh = parts
                if u != username:
                    continue
                try:
                    device_id_i = int(device_id)
                    consumption_f = float(consumption_kwh)
                except ValueError:
                    continue
                energy_entries.append({
                    'username': u,
                    'device_id': device_id_i,
                    'date': date,
                    'consumption_kwh': consumption_f
                })
    except FileNotFoundError:
        pass
    return energy_entries


def load_activity_logs(username):
    logs = []
    try:
        with open(ACTIVITY_LOGS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 5:
                    continue
                u, timestamp, device_id, action, details = parts
                if u != username:
                    continue
                try:
                    device_id_i = int(device_id)
                except ValueError:
                    continue
                logs.append({
                    'username': u,
                    'timestamp': timestamp,
                    'device_id': device_id_i,
                    'action': action,
                    'details': details
                })
    except FileNotFoundError:
        pass
    return logs


CURRENT_USERNAME = 'john_doe'


@app.route('/')
def root():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    rooms = load_rooms(CURRENT_USERNAME)
    devices = load_devices(CURRENT_USERNAME)

    total_devices = len(devices)
    active_devices = sum(1 for d in devices if d['status'].lower() == 'online')
    offline_devices = total_devices - active_devices

    device_summary = {
        'total': total_devices,
        'active': active_devices,
        'offline': offline_devices
    }

    room_list = []
    for room in rooms:
        count = sum(1 for d in devices if d['room'] == room['room_name'])
        room_list.append({'room_name': room['room_name'], 'device_count': count})

    return render_template('dashboard.html', device_summary=device_summary, rooms=room_list)


@app.route('/devices')
def devices():
    devices_list = load_devices(CURRENT_USERNAME)
    return render_template('devices.html', devices=devices_list)


@app.route('/device/<int:device_id>', methods=['GET', 'POST'])
def device_control(device_id):
    devices_list = load_devices(CURRENT_USERNAME)
    device = next((d for d in devices_list if d['device_id'] == device_id), None)

    if device is None:
        return "Device not found", 404

    if request.method == 'POST':
        power = request.form.get('power')
        brightness = request.form.get('brightness')
        temperature = request.form.get('temperature')
        mode = request.form.get('mode')
        schedule_time = request.form.get('schedule_time')

        if power in ('on', 'off'):
            device['power'] = power

        device['brightness'] = brightness.strip() if brightness and brightness.strip() else None
        device['temperature'] = temperature.strip() if temperature and temperature.strip() else None

        if mode is not None:
            device['mode'] = mode

        device['schedule_time'] = schedule_time.strip() if schedule_time and schedule_time.strip() else None

        save_devices(CURRENT_USERNAME, devices_list)

        return redirect(url_for('device_control', device_id=device_id))

    return render_template('device_control.html', device=device)


@app.route('/add_device', methods=['GET', 'POST'])
def add_device():
    rooms_list = load_rooms(CURRENT_USERNAME)
    devices_list = load_devices(CURRENT_USERNAME)

    if request.method == 'POST':
        device_name = request.form.get('device_name', '').strip()
        device_type = request.form.get('device_type', '').strip()
        room = request.form.get('device_room', '').strip()

        if device_name and device_type and room:
            existing_ids = {d['device_id'] for d in devices_list}
            next_id = 1
            while next_id in existing_ids:
                next_id += 1

            new_device = {
                'username': CURRENT_USERNAME,
                'device_id': next_id,
                'device_name': device_name,
                'device_type': device_type,
                'room': room,
                'brand': '',
                'model': '',
                'status': 'Offline',
                'power': 'off',
                'brightness': None,
                'temperature': None,
                'mode': '',
                'schedule_time': None
            }

            devices_list.append(new_device)
            save_devices(CURRENT_USERNAME, devices_list)
            return redirect(url_for('devices'))

    return render_template('add_device.html', rooms=rooms_list)


@app.route('/automation')
def automation_rules():
    rules = load_automation_rules(CURRENT_USERNAME)
    devices_list = load_devices(CURRENT_USERNAME)
    return render_template('automation.html', rules=rules, devices=devices_list)


@app.route('/energy_report', methods=['GET', 'POST'])
def energy_report():
    energy_entries = load_energy_logs(CURRENT_USERNAME)
    devices_list = load_devices(CURRENT_USERNAME)

    filter_date = None
    if request.method == 'POST':
        date_str = request.form.get('date_filter')
        if date_str:
            try:
                datetime.strptime(date_str, '%Y-%m-%d')
                filter_date = date_str
            except ValueError:
                filter_date = None

    if filter_date:
        filtered_entries = [e for e in energy_entries if e['date'] == filter_date]
    else:
        filtered_entries = energy_entries

    total_consumption = sum(e['consumption_kwh'] for e in filtered_entries)

    energy_summary = {
        'total_consumption': total_consumption,
        'date': filter_date
    }

    return render_template('energy_report.html', energy_summary=energy_summary, energy_entries=filtered_entries)


@app.route('/activity_logs')
def activity_logs():
    logs = load_activity_logs(CURRENT_USERNAME)
    return render_template('activity.html', activity_logs=logs)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
