from flask import Flask, render_template, redirect, url_for, request, abort
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

# File paths
USERS_FILE = 'data/users.txt'
DEVICES_FILE = 'data/devices.txt'
ROOMS_FILE = 'data/rooms.txt'
AUTOMATION_FILE = 'data/automation_rules.txt'
ENERGY_LOGS_FILE = 'data/energy_logs.txt'
ACTIVITY_LOGS_FILE = 'data/activity_logs.txt'

# Utility function to read pipe-delimited files
# Optionally verifies exact number of fields to parse correctly as schema demands

def read_pipe_file(filename, expected_fields=None):
    entries = []
    if not os.path.exists(filename):
        return entries
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if expected_fields is not None and len(parts) != expected_fields:
                continue
            entries.append(parts)
    return entries

# Utility function to write pipe-delimited files (overwrites)
def write_pipe_file(filename, entries):
    with open(filename, 'w', encoding='utf-8') as f:
        for entry in entries:
            line = '|'.join(entry)
            f.write(line + '\n')


@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    devices = read_pipe_file(DEVICES_FILE, expected_fields=13)
    rooms_count = {}
    devices_summary = {
        'total': 0,
        'active': 0,
        'offline': 0
    }
    devices_list = []
    for d in devices:
        try:
            # fields per spec:
            # username|device_id|device_name|device_type|room|brand|model|status|power|brightness|temperature|mode|schedule_time
            username = d[0]
            device_id = int(d[1])
            device_name = d[2]
            device_type = d[3]
            room = d[4]
            brand = d[5] # unused here
            model = d[6] # unused here
            status = d[7]  # Online or Offline
            power = d[8] # unused here
            brightness = d[9] # unused here
            temperature = d[10] # unused here
            mode = d[11] # unused here
            schedule_time = d[12] # unused here

            devices_summary['total'] += 1
            if status == 'Online':
                devices_summary['active'] += 1
            else:
                devices_summary['offline'] += 1

            rooms_count[room] = rooms_count.get(room, 0) + 1

            devices_list.append({
                'device_id': device_id,
                'device_name': device_name,
                'device_type': device_type,
                'room': room,
                'status': status
            })
        except Exception:
            continue

    rooms_summary = []
    for room_name, device_count in rooms_count.items():
        rooms_summary.append({'room_name': room_name, 'device_count': device_count})

    return render_template('dashboard.html', devices_summary=devices_summary, rooms_summary=rooms_summary)

@app.route('/devices')
def device_list():
    devices = read_pipe_file(DEVICES_FILE, expected_fields=13)
    devices_out = []
    for d in devices:
        try:
            device_id = int(d[1])
            device_name = d[2]
            device_type = d[3]
            room = d[4]
            status = d[7]
            devices_out.append({
                'device_id': device_id,
                'device_name': device_name,
                'device_type': device_type,
                'room': room,
                'status': status
            })
        except Exception:
            continue
    return render_template('device_list.html', devices=devices_out)

@app.route('/device/<int:device_id>')
def device_control(device_id):
    devices = read_pipe_file(DEVICES_FILE, expected_fields=13)
    device = None
    for d in devices:
        try:
            did = int(d[1])
            if did == device_id:
                # Parse fields
                power = d[8]
                brightness = d[9]
                temperature = d[10]
                mode = d[11]

                device = {
                    'device_id': did,
                    'device_name': d[2],
                    'status': d[7],
                    'power': power,
                    'brightness': int(brightness) if brightness.isdigit() else None if brightness == '' else None,
                    'temperature': int(temperature) if temperature.isdigit() else None if temperature == '' else None,
                    'mode': mode
                }
                break
        except Exception:
            continue
    if device is None:
        abort(404)
    return render_template('device_control.html', device=device)

@app.route('/device/<int:device_id>/control', methods=['POST'])
def device_control_post(device_id):
    devices = read_pipe_file(DEVICES_FILE, expected_fields=13)
    updated_devices = []
    found = False
    for d in devices:
        try:
            did = int(d[1])
            if did == device_id:
                found = True
                # Read from form
                power = request.form.get('power', d[8]).strip()
                brightness_raw = request.form.get('brightness', d[9]).strip()
                temperature_raw = request.form.get('temperature', d[10]).strip()
                mode = request.form.get('mode', d[11]).strip()

                # Validate power
                if power not in ('on', 'off'):
                    power = d[8]

                # Validate brightness
                try:
                    brightness = str(int(brightness_raw))
                except:
                    brightness = d[9]

                # Validate temperature
                try:
                    temperature = str(int(temperature_raw))
                except:
                    temperature = d[10]

                # Compose updated line
                updated_line = [d[0], d[1], d[2], d[3], d[4], d[5], d[6], d[7], power, brightness, temperature, mode, d[12]]
                updated_devices.append(updated_line)
            else:
                updated_devices.append(d)
        except Exception:
            updated_devices.append(d)
    if not found:
        abort(404)
    write_pipe_file(DEVICES_FILE, updated_devices)
    return redirect(url_for('device_control', device_id=device_id))

@app.route('/add_device', methods=['GET'])
def add_device():
    # Rooms as per data/rooms.txt file
    rooms_data = read_pipe_file(ROOMS_FILE, expected_fields=3)
    rooms = []
    seen_rooms = set()
    for r in rooms_data:
        try:
            room_name = r[2]
            if room_name not in seen_rooms:
                rooms.append(room_name)
                seen_rooms.add(room_name)
        except:
            continue
    device_types = ['Light', 'Thermostat', 'Camera', 'Lock', 'Sensor', 'Appliance']
    return render_template('add_device.html', rooms=rooms, device_types=device_types)

@app.route('/add_device', methods=['POST'])
def add_device_post():
    device_name = request.form.get('device_name', '').strip()
    device_type = request.form.get('device_type', '').strip()
    device_room = request.form.get('device_room', '').strip()

    devices = read_pipe_file(DEVICES_FILE, expected_fields=13)
    max_id = 0
    for d in devices:
        try:
            did = int(d[1])
            if did > max_id:
                max_id = did
        except:
            continue
    new_device_id = max_id + 1

    # New device line: username default_user, new id, given name, type, room, brand empty, model empty, status Offline, power off,
    # brightness empty, temperature empty, mode Auto, schedule_time empty

    new_line = [
        'default_user',
        str(new_device_id),
        device_name,
        device_type,
        device_room,
        '',
        '',
        'Offline',
        'off',
        '',
        '',
        'Auto',
        ''
    ]

    devices.append(new_line)
    write_pipe_file(DEVICES_FILE, devices)

    return redirect(url_for('device_list'))

@app.route('/automation', methods=['GET'])
def automation_rules():
    rules = []
    rules_raw = read_pipe_file(AUTOMATION_FILE, expected_fields=9)
    for r in rules_raw:
        try:
            rules.append({
                'rule_id': int(r[1]),
                'rule_name': r[2],
                'trigger_type': r[3],
                'trigger_value': r[4],
                'action_device_id': int(r[5]),
                'action_type': r[6],
                'enabled': r[8].lower() == 'true'
            })
        except:
            continue
    devices_raw = read_pipe_file(DEVICES_FILE, expected_fields=13)
    devices = []
    for d in devices_raw:
        try:
            devices.append({'device_id': int(d[1]), 'device_name': d[2]})
        except:
            continue
    return render_template('automation.html', rules=rules, devices=devices)

@app.route('/automation', methods=['POST'])
def add_automation_rule():
    rule_name = request.form.get('rule_name', '').strip()
    trigger_type = request.form.get('trigger_type', '').strip()
    trigger_value = request.form.get('trigger_value', '').strip()
    action_device_id_str = request.form.get('action_device_id', '').strip()
    action_type = request.form.get('action_type', '').strip()
    enabled_raw = request.form.get('enabled', '')
    enabled = enabled_raw.lower() == 'on' or enabled_raw.lower() == 'true'

    try:
        action_device_id = int(action_device_id_str)
    except:
        action_device_id = 0

    rules = read_pipe_file(AUTOMATION_FILE, expected_fields=9)
    max_id = 0
    for r in rules:
        try:
            rid = int(r[1])
            if rid > max_id:
                max_id = rid
        except:
            continue
    new_rule_id = max_id + 1

    # action_value is empty string for now
    new_line = [
        'default_user',
        str(new_rule_id),
        rule_name,
        trigger_type,
        trigger_value,
        str(action_device_id),
        action_type,
        '',
        'true' if enabled else 'false'
    ]

    rules.append(new_line)
    write_pipe_file(AUTOMATION_FILE, rules)

    return redirect(url_for('automation_rules'))

@app.route('/energy', methods=['GET'])
def energy_report():
    energy_logs_raw = read_pipe_file(ENERGY_LOGS_FILE, expected_fields=4)
    energy_logs = []
    total_kwh = 0.0
    for e in energy_logs_raw:
        try:
            device_id = int(e[1])
            device_name = e[0]
            date = e[2]
            consumption_kwh = float(e[3])
            total_kwh += consumption_kwh
            energy_logs.append({
                'device_id': device_id,
                'device_name': device_name,
                'date': date,
                'consumption_kwh': consumption_kwh
            })
        except:
            continue
    energy_summary = {
        'total_kwh': total_kwh,
        'estimated_cost': round(total_kwh * 0.12, 2)  # Example cost estimation
    }
    return render_template('energy_report.html', energy_summary=energy_summary, energy_logs=energy_logs, filter_date=None)

@app.route('/energy/filter', methods=['POST'])
def energy_filter_post():
    filter_date = request.form.get('filter_date', '').strip()
    try:
        datetime.strptime(filter_date, '%Y-%m-%d')
    except Exception:
        return render_template('error.html', message='Invalid date format')
    energy_logs_raw = read_pipe_file(ENERGY_LOGS_FILE, expected_fields=4)
    energy_logs = []
    total_kwh = 0.0
    for e in energy_logs_raw:
        if e[2] == filter_date:
            try:
                device_id = int(e[1])
                device_name = e[0]
                date = e[2]
                consumption_kwh = float(e[3])
                total_kwh += consumption_kwh
                energy_logs.append({
                    'device_id': device_id,
                    'device_name': device_name,
                    'date': date,
                    'consumption_kwh': consumption_kwh
                })
            except:
                continue
    energy_summary = {
        'total_kwh': total_kwh,
        'estimated_cost': round(total_kwh * 0.12, 2)
    }
    return render_template('energy_report.html', energy_summary=energy_summary, energy_logs=energy_logs, filter_date=filter_date)

@app.route('/activity')
def activity_logs():
    search_text = request.args.get('search_text', '').strip().lower()
    activity_raw = read_pipe_file(ACTIVITY_LOGS_FILE, expected_fields=5)
    devices_raw = read_pipe_file(DEVICES_FILE, expected_fields=13)

    device_map = {}
    for d in devices_raw:
        try:
            device_map[int(d[1])] = d[2]  # device_name per spec position 2
        except:
            continue

    activities = []
    for a in activity_raw:
        try:
            timestamp = a[1]
            device_id = int(a[2])
            action = a[3]
            details = a[4]
            device_name = device_map.get(device_id, '')
            if search_text:
                if search_text not in action.lower() and search_text not in details.lower():
                    continue
            activities.append({
                'timestamp': timestamp,
                'device_id': device_id,
                'device_name': device_name,
                'action': action,
                'details': details
            })
        except:
            continue

    return render_template('activity_logs.html', activities=activities, search_text=search_text if search_text else None)

@app.route('/activity/search', methods=['POST'])
def activity_search_post():
    search_text = request.form.get('search_text', '').strip()
    return redirect(url_for('activity_logs', search_text=search_text))


if __name__ == '__main__':
    app.run(debug=True, port=5000)
