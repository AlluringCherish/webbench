from flask import Flask, render_template, request, redirect, url_for
import datetime

app = Flask(__name__)

# Data loading functions

def load_users():
    users = []
    with open('data/users.txt', 'r') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) >= 2:
                users.append({'username': parts[0], 'email': parts[1]})
    return users


def load_devices():
    devices = []
    with open('data/devices.txt', 'r') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) >= 12:
                devices.append({
                    'username': parts[0],
                    'device_id': int(parts[1]),
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
                    'schedule_time': parts[12] if len(parts) > 12 else ''
                })
    return devices


def load_rooms():
    rooms = []
    with open('data/rooms.txt', 'r') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) >= 2:
                rooms.append({
                    'room_id': int(parts[0]),
                    'room_name': parts[1]
                })
    return rooms


def load_automation_rules():
    rules = []
    with open('data/automation_rules.txt', 'r') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) >= 7:
                rules.append({
                    'username': parts[0],
                    'rule_id': int(parts[1]),
                    'rule_name': parts[2],
                    'trigger_type': parts[3],
                    'trigger_value': parts[4],
                    'action_device_id': int(parts[5]),
                    'action_type': parts[6],
                    'action_value': parts[7] if len(parts) > 7 else '',
                    'enabled': parts[8].lower() == 'true' if len(parts) > 8 else False
                })
    return rules


def load_activity_logs():
    logs = []
    with open('data/activity_logs.txt', 'r') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) >= 5:
                logs.append({
                    'username': parts[0],
                    'timestamp': parts[1],
                    'device_id': int(parts[2]),
                    'action': parts[3],
                    'details': parts[4]
                })
    return logs


def load_energy_logs():
    energy = []
    with open('data/energy_logs.txt', 'r') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) >= 4:
                energy.append({
                    'username': parts[0],
                    'date': parts[1],
                    'device_id': int(parts[2]),
                    'consumption_kwh': float(parts[3])
                })
    return energy


# Routes

@app.route('/')
@app.route('/dashboard')
def dashboard():
    devices = load_devices()
    users = load_users()
    rooms = load_rooms()
    # Aggregate energy consumption per user/device can be added
    return render_template('dashboard.html', devices=devices, users=users, rooms=rooms)


@app.route('/devices')
def devices_list():
    devices = load_devices()
    rooms = load_rooms()
    return render_template('devices_list.html', devices=devices, rooms=rooms)


@app.route('/device/<int:device_id>', methods=['GET', 'POST'])
def device_detail(device_id):
    devices = load_devices()
    device = next((d for d in devices if d['device_id'] == device_id), None)
    if device is None:
        return "Device not found", 404

    if request.method == 'POST':
        # Handle control action
        action_type = request.form.get('action_type')
        action_value = request.form.get('action_value')
        # Logic to apply action here (update device etc.)
        # For this task, just simulate success and redirect
        return redirect(url_for('device_detail', device_id=device_id))

    return render_template('device_detail.html', device=device)


@app.route('/activity')
def activity_page():
    logs = load_activity_logs()
    devices = load_devices()
    device_map = {d['device_id']: d for d in devices}
    return render_template('activity.html', logs=logs, device_map=device_map)


@app.route('/energy', methods=['GET', 'POST'])
def energy_page():
    energy_logs = load_energy_logs()
    devices = load_devices()
    filter_date = request.args.get('date', None)
    user = request.args.get('user', None)

    filtered_logs = energy_logs
    if filter_date:
        filtered_logs = [e for e in filtered_logs if e['date'] == filter_date]
    if user:
        filtered_logs = [e for e in filtered_logs if e['username'] == user]

    device_map = {d['device_id']: d for d in devices}

    return render_template('energy.html', energy_logs=filtered_logs, device_map=device_map, filter_date=filter_date, user=user)


@app.route('/automation', methods=['GET', 'POST'])
def automation_page():
    rules = load_automation_rules()
    devices = load_devices()
    if request.method == 'POST':
        # process adding or updating rules
        # Skipped for brevity
        return redirect(url_for('automation_page'))
    return render_template('automation.html', rules=rules, devices=devices)


if __name__ == '__main__':
    app.run(debug=True)
