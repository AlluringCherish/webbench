from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

# Helper function to load device data for a given username
# Returns list of device dicts

def load_devices(username):
    devices = []
    try:
        with open('data/devices.txt', 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                fields = line.split('|')
                if len(fields) != 13:
                    continue
                (user, device_id, device_name, device_type, room, brand, model, status, power,
                 brightness, temperature, mode, schedule_time) = fields
                if user != username:
                    continue
                device = {
                    'username': user,
                    'device_id': int(device_id),
                    'device_name': device_name,
                    'device_type': device_type,
                    'room': room,
                    'brand': brand,
                    'model': model,
                    'status': status,
                    'power': power,
                    'brightness': int(brightness) if brightness.isdigit() else None,
                    'temperature': int(temperature) if temperature.isdigit() else None,
                    'mode': mode,
                    'schedule_time': schedule_time
                }
                devices.append(device)
    except FileNotFoundError:
        devices = []
    return devices

# Helper to load rooms data
# Returns list of room dicts

def load_rooms(username):
    rooms = []
    try:
        with open('data/rooms.txt', 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                fields = line.split('|')
                if len(fields) != 3:
                    continue
                user, room_id, room_name = fields
                if user != username:
                    continue
                room = {
                    'username': user,
                    'room_id': int(room_id),
                    'room_name': room_name
                }
                rooms.append(room)
    except FileNotFoundError:
        rooms = []
    return rooms

# Helper to load automation rules
# Returns list of rule dicts

def load_automation_rules(username):
    rules = []
    try:
        with open('data/automation_rules.txt', 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                fields = line.split('|')
                if len(fields) != 9:
                    continue
                (user, rule_id, rule_name, trigger_type, trigger_value,
                 action_device_id, action_type, action_value, enabled) = fields
                if user != username:
                    continue
                rule = {
                    'username': user,
                    'rule_id': int(rule_id),
                    'rule_name': rule_name,
                    'trigger_type': trigger_type,
                    'trigger_value': trigger_value,
                    'action_device_id': int(action_device_id),
                    'action_type': action_type,
                    'action_value': action_value,
                    'enabled': enabled.lower() == 'true'
                }
                rules.append(rule)
    except FileNotFoundError:
        rules = []
    return rules

# Helper to load energy logs
# Returns list of energy record dicts

def load_energy_logs(username):
    energy_records = []
    try:
        with open('data/energy_logs.txt', 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                fields = line.split('|')
                if len(fields) != 4:
                    continue
                user, device_id, date, consumption_kwh = fields
                if user != username:
                    continue
                try:
                    consumption = float(consumption_kwh)
                except ValueError:
                    consumption = 0.0
                record = {
                    'username': user,
                    'device_id': int(device_id),
                    'date': date,
                    'consumption_kwh': consumption
                }
                energy_records.append(record)
    except FileNotFoundError:
        energy_records = []
    return energy_records

# Helper to load activity logs
# Returns list of activity dicts

def load_activity_logs(username):
    activities = []
    try:
        with open('data/activity_logs.txt', 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                fields = line.split('|')
                if len(fields) != 5:
                    continue
                user, timestamp, device_id, action, details = fields
                if user != username:
                    continue
                activity = {
                    'username': user,
                    'timestamp': timestamp,
                    'device_id': int(device_id),
                    'action': action,
                    'details': details
                }
                activities.append(activity)
    except FileNotFoundError:
        activities = []
    return activities

# Helper to save devices list back to file

def save_devices(devices, username):
    try:
        with open('data/devices.txt', 'w', encoding='utf-8') as f:
            for d in devices:
                if d['username'] != username:
                    continue
                brightness_str = str(d['brightness']) if d['brightness'] is not None else ''
                temperature_str = str(d['temperature']) if d['temperature'] is not None else ''
                line = '|'.join([
                    d['username'],
                    str(d['device_id']),
                    d['device_name'],
                    d['device_type'],
                    d['room'],
                    d['brand'],
                    d['model'],
                    d['status'],
                    d['power'],
                    brightness_str,
                    temperature_str,
                    d['mode'],
                    d['schedule_time']
                ])
                f.write(line + '\n')
    except Exception:
        pass

# Helper to save automation rules

def save_automation_rules(rules, username):
    try:
        with open('data/automation_rules.txt', 'w', encoding='utf-8') as f:
            for r in rules:
                if r['username'] != username:
                    continue
                enabled_str = 'true' if r['enabled'] else 'false'
                line = '|'.join([
                    r['username'],
                    str(r['rule_id']),
                    r['rule_name'],
                    r['trigger_type'],
                    r['trigger_value'],
                    str(r['action_device_id']),
                    r['action_type'],
                    r['action_value'],
                    enabled_str
                ])
                f.write(line + '\n')
    except Exception:
        pass

# CURRENT USER (hardcoded for demonstration)
CURRENT_USERNAME = 'john_doe'

from flask import abort

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard_page'))

@app.route('/dashboard')
def dashboard_page():
    username = CURRENT_USERNAME
    devices = load_devices(username)
    rooms = load_rooms(username)

    total_devices = len(devices)
    active_devices = sum(1 for d in devices if d['status'].lower() == 'online')
    offline_devices = total_devices - active_devices

    # Prepare rooms list with device counts
    room_list = []
    for room in rooms:
        count = sum(1 for d in devices if d['room'] == room['room_name'])
        room_list.append({'room_id': room['room_id'], 'room_name': room['room_name'], 'device_count': count})

    return render_template('dashboard.html', total_devices=total_devices, active_devices=active_devices, offline_devices=offline_devices, rooms=room_list)

@app.route('/devices')
def device_list_page():
    username = CURRENT_USERNAME
    devices = load_devices(username)
    return render_template('device_list.html', devices=devices)

from flask import flash

@app.route('/devices/add', methods=['GET', 'POST'])
def add_device_page():
    username = CURRENT_USERNAME
    form_submission_result = ''
    if request.method == 'POST':
        device_name = request.form.get('device_name', '').strip()
        device_type = request.form.get('device_type', '').strip()
        room = request.form.get('device_room', '').strip()

        valid_types = ['Light', 'Thermostat', 'Camera', 'Lock', 'Sensor', 'Appliance']
        valid_rooms = ['Living Room', 'Bedroom', 'Kitchen', 'Bathroom', 'Garage']

        if not device_name:
            form_submission_result = 'Device name is required.'
        elif device_type not in valid_types:
            form_submission_result = 'Invalid device type.'
        elif room not in valid_rooms:
            form_submission_result = 'Invalid room selection.'
        else:
            devices = load_devices(username)
            new_id = 1
            if devices:
                new_id = max(d['device_id'] for d in devices) + 1
            # Add new device with default specs
            new_device = {
                'username': username,
                'device_id': new_id,
                'device_name': device_name,
                'device_type': device_type,
                'room': room,
                'brand': '',
                'model': '',
                'status': 'Offline',
                'power': 'off',
                'brightness': None,
                'temperature': None,
                'mode': 'Auto',
                'schedule_time': ''
            }
            # Append to devices list
            devices.append(new_device)
            # Save back file (including all devices)
            try:
                with open('data/devices.txt', 'w', encoding='utf-8') as f:
                    for d in devices:
                        brightness_str = str(d['brightness']) if d['brightness'] is not None else ''
                        temperature_str = str(d['temperature']) if d['temperature'] is not None else ''
                        line = '|'.join([
                            d['username'],
                            str(d['device_id']),
                            d['device_name'],
                            d['device_type'],
                            d['room'],
                            d['brand'],
                            d['model'],
                            d['status'],
                            d['power'],
                            brightness_str,
                            temperature_str,
                            d['mode'],
                            d['schedule_time']
                        ])
                        f.write(line + '\n')
                form_submission_result = 'Device added successfully.'
            except Exception:
                form_submission_result = 'Failed to add device.'

    return render_template('add_device.html', form_submission_result=form_submission_result)

@app.route('/devices/control/<int:device_id>', methods=['GET', 'POST'])
def device_control_page(device_id):
    username = CURRENT_USERNAME
    devices = load_devices(username)
    device = None
    for d in devices:
        if d['device_id'] == device_id:
            device = d
            break
    if not device:
        return abort(404)

    if request.method == 'POST':
        # Example: toggle power or update settings from form
        power = request.form.get('power')
        brightness = request.form.get('brightness')
        temperature = request.form.get('temperature')

        if power in ('on', 'off'):
            device['power'] = power
            # Update status accordingly
            device['status'] = 'Online' if power == 'on' else 'Offline'

        # Only update brightness and temperature if applicable for device type
        if brightness is not None and brightness.isdigit() and 0 <= int(brightness) <= 100:
            device['brightness'] = int(brightness)

        if temperature is not None:
            try:
                temp_val = int(temperature)
                device['temperature'] = temp_val
            except (ValueError, TypeError):
                pass

        save_devices(devices, username)

    return render_template('device_control.html', device=device)

@app.route('/automation', methods=['GET', 'POST'])
def automation_rules_page():
    username = CURRENT_USERNAME
    form_result = ''
    rules = load_automation_rules(username)
    devices = load_devices(username)

    if request.method == 'POST':
        # Add new automation rule
        rule_name = request.form.get('rule_name', '').strip()
        trigger_type = request.form.get('trigger_type', '').strip()
        trigger_value = request.form.get('trigger_value', '').strip()
        action_device_id = request.form.get('action_device')
        action_type = request.form.get('action_type', '').strip()

        # Validate
        valid_trigger_types = ['Time', 'Motion', 'Temperature']
        valid_action_types = ['Turn On', 'Turn Off', 'Set Brightness', 'Set Temperature']

        if not rule_name:
            form_result = 'Rule name is required.'
        elif trigger_type not in valid_trigger_types:
            form_result = 'Invalid trigger type.'
        elif not trigger_value:
            form_result = 'Trigger value is required.'
        elif not action_device_id or not action_device_id.isdigit() or not any(d['device_id'] == int(action_device_id) for d in devices):
            form_result = 'Invalid action device.'
        elif action_type not in valid_action_types:
            form_result = 'Invalid action type.'
        else:
            new_id = 1
            if rules:
                new_id = max(r['rule_id'] for r in rules) + 1

            new_rule = {
                'username': username,
                'rule_id': new_id,
                'rule_name': rule_name,
                'trigger_type': trigger_type,
                'trigger_value': trigger_value,
                'action_device_id': int(action_device_id),
                'action_type': action_type,
                'action_value': '',  # no specific action value to set here
                'enabled': True
            }
            rules.append(new_rule)
            save_automation_rules(rules, username)
            form_result = 'New automation rule added.'

    return render_template('automation_rules.html', rules=rules, devices=devices, form_result=form_result)

@app.route('/energy', methods=['GET', 'POST'])
def energy_report_page():
    username = CURRENT_USERNAME
    energy_records = load_energy_logs(username)
    filter_date = ''

    if request.method == 'POST':
        filter_date = request.form.get('date_filter', '')
        if filter_date:
            energy_records = [rec for rec in energy_records if rec['date'] == filter_date]

    total_consumption = sum(r['consumption_kwh'] for r in energy_records)
    cost_per_kwh = 0.12  # example cost estimate per kWh
    cost_estimate = total_consumption * cost_per_kwh

    return render_template('energy_report.html', energy_records=energy_records, total_consumption=total_consumption, cost_estimate=cost_estimate, filter_date=filter_date)

@app.route('/activity', methods=['GET', 'POST'])
def activity_logs_page():
    username = CURRENT_USERNAME
    activities = load_activity_logs(username)
    search_query = ''

    if request.method == 'POST':
        search_query = request.form.get('search_query', '').strip().lower()
        if search_query:
            activities = [a for a in activities if
                          search_query in a['action'].lower() or search_query in a['details'].lower()]

    return render_template('activity_logs.html', activities=activities, search_query=search_query)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
