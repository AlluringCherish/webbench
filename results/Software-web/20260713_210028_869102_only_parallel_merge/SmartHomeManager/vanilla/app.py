from flask import Flask, render_template, request, redirect, url_for, flash
import os

app = Flask(__name__)
app.secret_key = 'somesecretkey'  # Needed for flashing messages
DATA_DIR = 'data'
CURRENT_USER = 'john_doe'  # Fixed user for demo

# --------- Data Reading Utilities ---------

def read_pipe_delimited_file(filepath, expected_fields):
    result = []
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) == expected_fields:
                    result.append(parts)
    return result


def read_users():
    lines = read_pipe_delimited_file(os.path.join(DATA_DIR, 'users.txt'), 2)
    users = [{'username': p[0], 'email': p[1]} for p in lines]
    return users


def read_devices():
    lines = read_pipe_delimited_file(os.path.join(DATA_DIR, 'devices.txt'), 13)
    devices = []
    for p in lines:
        devices.append({
            'username': p[0],
            'device_id': p[1],
            'device_name': p[2],
            'device_type': p[3],
            'room': p[4],
            'brand': p[5],
            'model': p[6],
            'status': p[7],
            'power': p[8],
            'brightness': p[9],
            'temperature': p[10],
            'mode': p[11],
            'schedule_time': p[12]
        })
    return devices


def read_rooms():
    lines = read_pipe_delimited_file(os.path.join(DATA_DIR, 'rooms.txt'), 3)
    rooms = [{'username': p[0], 'room_id': p[1], 'room_name': p[2]} for p in lines]
    return rooms


def read_automation_rules():
    lines = read_pipe_delimited_file(os.path.join(DATA_DIR, 'automation_rules.txt'), 9)
    rules = []
    for p in lines:
        rules.append({
            'username': p[0],
            'rule_id': p[1],
            'rule_name': p[2],
            'trigger_type': p[3],
            'trigger_value': p[4],
            'action_device_id': p[5],
            'action_type': p[6],
            'action_value': p[7],
            'enabled': p[8].lower() == 'true'
        })
    return rules


def read_energy_logs():
    lines = read_pipe_delimited_file(os.path.join(DATA_DIR, 'energy_logs.txt'), 4)
    logs = []
    for p in lines:
        try:
            consumption = float(p[3])
        except ValueError:
            consumption = 0.0
        logs.append({
            'username': p[0],
            'device_id': p[1],
            'date': p[2],
            'consumption_kwh': consumption
        })
    return logs


def read_activity_logs():
    lines = read_pipe_delimited_file(os.path.join(DATA_DIR, 'activity_logs.txt'), 5)
    logs = []
    for p in lines:
        logs.append({
            'username': p[0],
            'timestamp': p[1],
            'device_id': p[2],
            'action': p[3],
            'details': p[4]
        })
    return logs


# --------- Data Writing Utilities ---------

def write_devices(devices):
    path = os.path.join(DATA_DIR, 'devices.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for d in devices:
            line = '|'.join([
                d['username'], d['device_id'], d['device_name'], d['device_type'], d['room'], d['brand'], d['model'],
                d['status'], d['power'], d['brightness'], d['temperature'], d['mode'], d['schedule_time']
            ])
            f.write(line + '\n')


def write_automation_rules(rules):
    path = os.path.join(DATA_DIR, 'automation_rules.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for r in rules:
            line = '|'.join([
                r['username'], r['rule_id'], r['rule_name'], r['trigger_type'], r['trigger_value'], r['action_device_id'],
                r['action_type'], r['action_value'], 'true' if r['enabled'] else 'false'
            ])
            f.write(line + '\n')


# --------- Flask Routes ---------

@app.route('/')
def dashboard():
    devices = [d for d in read_devices() if d['username'] == CURRENT_USER]
    rooms = [r for r in read_rooms() if r['username'] == CURRENT_USER]

    total_devices = len(devices)
    active_devices = sum(1 for d in devices if d['status'].lower() == 'online')
    offline_devices = total_devices - active_devices

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


@app.route('/devices')
def device_list():
    devices = [d for d in read_devices() if d['username'] == CURRENT_USER]
    return render_template('device_list.html', devices=devices)


@app.route('/devices/add', methods=['GET', 'POST'])
def add_device():
    rooms = ['Living Room', 'Bedroom', 'Kitchen', 'Bathroom', 'Garage']
    device_types = ['Light', 'Thermostat', 'Camera', 'Lock', 'Sensor', 'Appliance']

    if request.method == 'POST':
        device_name = request.form.get('device-name', '').strip()
        device_type = request.form.get('device-type', '')
        device_room = request.form.get('device-room', '')

        if device_name and device_type in device_types and device_room in rooms:
            devices = read_devices()
            # Validate device_room against existing rooms for user
            user_rooms = [r['room_name'] for r in read_rooms() if r['username'] == CURRENT_USER]
            if device_room not in user_rooms:
                flash('Invalid room selected.')
                return redirect(url_for('add_device'))

            existing_ids = [int(d['device_id']) for d in devices if d['username'] == CURRENT_USER]
            new_id = str(max(existing_ids) + 1 if existing_ids else 1)
            new_device = {
                'username': CURRENT_USER,
                'device_id': new_id,
                'device_name': device_name,
                'device_type': device_type,
                'room': device_room,
                'brand': 'Unknown',
                'model': 'Unknown',
                'status': 'Offline',
                'power': 'off',
                'brightness': '',
                'temperature': '',
                'mode': 'Auto',
                'schedule_time': ''
            }
            devices.append(new_device)
            write_devices(devices)
            return redirect(url_for('device_list'))
        else:
            flash('Please fill all fields correctly.')

    return render_template('add_device.html', rooms=rooms, device_types=device_types)


@app.route('/devices/control/<device_id>', methods=['GET', 'POST'])
def device_control(device_id):
    devices = read_devices()
    device = None
    for d in devices:
        if d['username'] == CURRENT_USER and d['device_id'] == device_id:
            device = d
            break
    if not device:
        flash('Device not found.')
        return redirect(url_for('device_list'))

    if request.method == 'POST':
        power_val = request.form.get('power-toggle')
        if power_val == 'on':
            device['power'] = 'on'
            device['status'] = 'Online'
        elif power_val == 'off':
            device['power'] = 'off'
            device['status'] = 'Offline'

        brightness = request.form.get('brightness')
        temperature = request.form.get('temperature')
        mode = request.form.get('mode')
        schedule_time = request.form.get('schedule_time')

        if brightness is not None:
            device['brightness'] = brightness
        if temperature is not None:
            device['temperature'] = temperature
        if mode is not None:
            device['mode'] = mode
        if schedule_time is not None:
            device['schedule_time'] = schedule_time

        write_devices(devices)
        return redirect(url_for('device_control', device_id=device_id))

    return render_template('device_control.html', device=device)


@app.route('/automation', methods=['GET', 'POST'])
def automation_rules():
    rules = [r for r in read_automation_rules() if r['username'] == CURRENT_USER]
    devices = [d for d in read_devices() if d['username'] == CURRENT_USER]

    if request.method == 'POST':
        rule_name = request.form.get('rule-name', '').strip()
        trigger_type = request.form.get('trigger-type')
        trigger_value = request.form.get('trigger-value', '').strip()
        action_device_id = request.form.get('action-device')
        action_type = request.form.get('action-type')

        if rule_name and trigger_type and trigger_value and action_device_id and action_type:
            existing_ids = [int(r['rule_id']) for r in rules]
            new_id = str(max(existing_ids) + 1 if existing_ids else 1)
            new_rule = {
                'username': CURRENT_USER,
                'rule_id': new_id,
                'rule_name': rule_name,
                'trigger_type': trigger_type,
                'trigger_value': trigger_value,
                'action_device_id': action_device_id,
                'action_type': action_type,
                'action_value': '',
                'enabled': True
            }
            rules.append(new_rule)
            write_automation_rules(rules)
            return redirect(url_for('automation_rules'))
        else:
            flash('Please fill all fields correctly.')

    return render_template('automation_rules.html', rules=rules, devices=devices)


@app.route('/energy', methods=['GET', 'POST'])
def energy_report():
    energy_logs = [e for e in read_energy_logs() if e['username'] == CURRENT_USER]
    devices_list = [d for d in read_devices() if d['username'] == CURRENT_USER]

    filter_date = None
    if request.method == 'POST':
        filter_date = request.form.get('date-filter')

    filtered_logs = []
    total_consumption = 0.0
    for log in energy_logs:
        if filter_date and log['date'] != filter_date:
            continue
        filtered_logs.append(log)
        total_consumption += log['consumption_kwh']

    total_cost = total_consumption * 0.12

    device_map = {d['device_id']: d['device_name'] for d in devices_list}
    for log in filtered_logs:
        log['device_name'] = device_map.get(log['device_id'], 'Unknown')

    return render_template('energy_report.html',
                           energy_logs=filtered_logs,
                           total_consumption=total_consumption,
                           total_cost=total_cost,
                           filter_date=filter_date)


@app.route('/activity', methods=['GET', 'POST'])
def activity_logs():
    logs = [l for l in read_activity_logs() if l['username'] == CURRENT_USER]
    devices_list = [d for d in read_devices() if d['username'] == CURRENT_USER]

    search_term = None
    if request.method == 'POST':
        search_term = request.form.get('search-activity', '').strip().lower()

    filtered_logs = []
    if search_term:
        for log in logs:
            device_name = ''
            for d in devices_list:
                if d['device_id'] == log['device_id']:
                    device_name = d['device_name']
                    break
            if (search_term in log['timestamp'].lower() or
                search_term in log['action'].lower() or
                search_term in log['details'].lower() or
                search_term in device_name.lower()):
                filtered_logs.append(log)
    else:
        filtered_logs = logs

    filtered_logs.sort(key=lambda x: x['timestamp'], reverse=True)

    device_map = {d['device_id']: d for d in devices_list}
    return render_template('activity_logs.html', logs=filtered_logs, devices=device_map, search_term=search_term)


if __name__ == '__main__':
    app.run(debug=True)
