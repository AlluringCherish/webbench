from flask import Flask, render_template, redirect, url_for, request
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Utility functions to load data from files

def load_memberships():
    memberships = []
    try:
        with open(os.path.join(DATA_DIR, 'memberships.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 6:
                    continue
                membership = {
                    'membership_id': int(parts[0]),
                    'plan_name': parts[1],
                    'price': parts[2],
                    'billing_cycle': parts[3],
                    'features': parts[4],
                    'max_classes': parts[5]
                }
                memberships.append(membership)
    except Exception:
        # Could log or print error
        pass
    return memberships


def load_membership_by_id(plan_id):
    memberships = load_memberships()
    for m in memberships:
        if m['membership_id'] == plan_id:
            return m
    return None


def load_classes():
    classes = []
    try:
        with open(os.path.join(DATA_DIR, 'classes.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 8:
                    continue
                cls = {
                    'class_id': int(parts[0]),
                    'class_name': parts[1],
                    'trainer_id': int(parts[2]),
                    'class_type': parts[3],
                    'schedule_day': parts[4],
                    'schedule_time': parts[5],
                    'capacity': int(parts[6]),
                    'duration': int(parts[7])
                }
                classes.append(cls)
    except Exception:
        pass
    return classes


def load_trainers():
    trainers = []
    try:
        with open(os.path.join(DATA_DIR, 'trainers.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) !=6:
                    continue
                trainer = {
                    'trainer_id': int(parts[0]),
                    'name': parts[1],
                    'specialty': parts[2],
                    'certifications': parts[3],
                    'experience_years': int(parts[4]),
                    'bio': parts[5]
                }
                trainers.append(trainer)
    except Exception:
        pass
    return trainers


def load_trainer_by_id(trainer_id):
    trainers = load_trainers()
    for t in trainers:
        if t['trainer_id'] == trainer_id:
            return t
    return None


def load_bookings():
    bookings = []
    try:
        with open(os.path.join(DATA_DIR, 'bookings.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 7:
                    continue
                booking = {
                    'booking_id': int(parts[0]),
                    'member_name': parts[1],
                    'trainer_id': int(parts[2]),
                    'booking_date': parts[3],
                    'booking_time': parts[4],
                    'duration_minutes': int(parts[5]),
                    'status': parts[6]
                }
                bookings.append(booking)
    except Exception:
        pass
    return bookings


def save_booking(member_name, trainer_id, booking_date, booking_time, duration_minutes, status='Confirmed'):
    bookings = load_bookings()
    next_id = 1
    if bookings:
        next_id = max(b['booking_id'] for b in bookings) + 1
    new_booking_line = f"{next_id}|{member_name}|{trainer_id}|{booking_date}|{booking_time}|{duration_minutes}|{status}\n"
    try:
        with open(os.path.join(DATA_DIR, 'bookings.txt'), 'a', encoding='utf-8') as f:
            f.write(new_booking_line)
        return True
    except Exception:
        return False


def load_workouts():
    workouts = []
    try:
        with open(os.path.join(DATA_DIR, 'workouts.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 7:
                    continue
                workout = {
                    'workout_id': int(parts[0]),
                    'member_name': parts[1],
                    'workout_type': parts[2],
                    'workout_date': parts[3],
                    'duration_minutes': int(parts[4]),
                    'calories_burned': int(parts[5]),
                    'notes': parts[6]
                }
                workouts.append(workout)
    except Exception:
        pass
    return workouts


def save_workout_log(member_name, workout_type, workout_date, duration_minutes, calories_burned, notes):
    workouts = load_workouts()
    next_id = 1
    if workouts:
        next_id = max(w['workout_id'] for w in workouts) + 1
    new_workout_line = f"{next_id}|{member_name}|{workout_type}|{workout_date}|{duration_minutes}|{calories_burned}|{notes}\n"
    try:
        with open(os.path.join(DATA_DIR, 'workouts.txt'), 'a', encoding='utf-8') as f:
            f.write(new_workout_line)
        return True
    except Exception:
        return False

# Routes

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard_page'))


@app.route('/dashboard')
def dashboard_page():
    return render_template('dashboard.html')


@app.route('/memberships')
def membership_plans():
    memberships = load_memberships()
    return render_template('memberships.html', memberships=memberships)


@app.route('/plan/<int:plan_id>')
def plan_details(plan_id):
    plan = load_membership_by_id(plan_id)
    if not plan:
        # Could return 404 or similar
        return "Plan not found", 404
    return render_template('plan_details.html', plan=plan)


@app.route('/classes')
def class_schedule():
    classes = load_classes()
    return render_template('classes.html', classes=classes)


@app.route('/trainers')
def trainer_profiles():
    trainers = load_trainers()
    return render_template('trainers.html', trainers=trainers)


@app.route('/trainer/<int:trainer_id>')
def trainer_detail(trainer_id):
    trainer = load_trainer_by_id(trainer_id)
    if not trainer:
        return "Trainer not found", 404
    return render_template('trainer_detail.html', trainer=trainer)


@app.route('/booking')
def pt_booking():
    trainers = load_trainers()
    # Provide minimal info: trainer_id and name only
    minimal_trainers = [{'trainer_id': t['trainer_id'], 'name': t['name']} for t in trainers]
    return render_template('booking.html', trainers=minimal_trainers)


@app.route('/booking/confirm', methods=['POST'])
def confirm_booking():
    # Expect member_name, trainer_id, booking_date, booking_time, duration_minutes from form
    form = request.form
    member_name = form.get('member_name', '').strip()
    trainer_id = form.get('trainer_id', '').strip()
    booking_date = form.get('booking_date', '').strip()
    booking_time = form.get('booking_time', '').strip()
    duration_minutes = form.get('duration_minutes', '').strip()

    if not member_name or not trainer_id or not booking_date or not booking_time or not duration_minutes:
        return "Missing booking form data", 400

    try:
        trainer_id = int(trainer_id)
        duration_minutes = int(duration_minutes)
    except ValueError:
        return "Invalid data type for trainer ID or duration minutes", 400

    success = save_booking(member_name, trainer_id, booking_date, booking_time, duration_minutes, status='Confirmed')
    if success:
        # Redirect to dashboard after booking
        return redirect(url_for('dashboard_page'))
    else:
        return "Failed to save booking", 500


@app.route('/workouts')
def workout_records():
    workouts = load_workouts()
    return render_template('workouts.html', workouts=workouts)


@app.route('/workouts/log')
def log_workout():
    return render_template('log_workout.html')


@app.route('/workouts/log/submit', methods=['POST'])
def submit_workout():
    form = request.form
    workout_type = form.get('workout_type', '').strip()
    workout_duration = form.get('workout_duration', '').strip()
    calories_burned = form.get('calories_burned', '').strip()
    workout_notes = form.get('workout_notes', '').strip()

    if not workout_type or not workout_duration or not calories_burned:
        return "Missing workout log data", 400

    try:
        workout_duration = int(workout_duration)
        calories_burned = int(calories_burned)
    except ValueError:
        return "Invalid data type for duration or calories", 400

    # We do not have authenticated member_name from spec, so use a placeholder or form member_name
    # Spec doesn't specify member_name input for workout log, so we can use a default "Member" string
    member_name = "Member"

    from datetime import datetime
    workout_date = datetime.now().strftime('%Y-%m-%d')

    success = save_workout_log(member_name, workout_type, workout_date, workout_duration, calories_burned, workout_notes)
    if success:
        return redirect(url_for('workout_records'))
    else:
        return "Failed to save workout log", 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
