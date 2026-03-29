from flask import Flask, render_template, redirect, url_for, request
import os
from datetime import date

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Helper functions to load data from text files following exact field orders

def load_memberships():
    memberships = []
    try:
        with open(os.path.join(DATA_DIR, 'memberships.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 6:
                    continue
                membership_id = int(parts[0])
                plan_name = parts[1]
                price = float(parts[2])
                billing_cycle = parts[3]
                features = parts[4]
                max_classes_raw = parts[5]
                try:
                    max_classes = int(max_classes_raw)
                except ValueError:
                    max_classes = max_classes_raw
                memberships.append({
                    'membership_id': membership_id,
                    'plan_name': plan_name,
                    'price': price,
                    'billing_cycle': billing_cycle,
                    'features': features,
                    'max_classes': max_classes
                })
    except Exception:
        memberships = []
    return memberships


def load_classes():
    classes = []
    try:
        with open(os.path.join(DATA_DIR, 'classes.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 8:
                    continue
                class_id = int(parts[0])
                class_name = parts[1]
                trainer_id = int(parts[2])
                class_type = parts[3]
                schedule_day = parts[4]
                schedule_time = parts[5]
                capacity = int(parts[6])
                duration = int(parts[7])
                classes.append({
                    'class_id': class_id,
                    'class_name': class_name,
                    'trainer_id': trainer_id,
                    'class_type': class_type,
                    'schedule_day': schedule_day,
                    'schedule_time': schedule_time,
                    'capacity': capacity,
                    'duration': duration
                })
    except Exception:
        classes = []
    return classes


def load_trainers():
    trainers = []
    try:
        with open(os.path.join(DATA_DIR, 'trainers.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 6:
                    continue
                trainer_id = int(parts[0])
                name = parts[1]
                specialty = parts[2]
                certifications = parts[3]
                experience_years = int(parts[4])
                bio = parts[5]
                trainers.append({
                    'trainer_id': trainer_id,
                    'name': name,
                    'specialty': specialty,
                    'certifications': certifications,
                    'experience_years': experience_years,
                    'bio': bio
                })
    except Exception:
        trainers = []
    return trainers


def load_bookings():
    bookings = []
    try:
        with open(os.path.join(DATA_DIR, 'bookings.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 7:
                    continue
                booking_id = int(parts[0])
                member_name = parts[1]
                trainer_id = int(parts[2])
                booking_date = parts[3]
                booking_time = parts[4]
                duration_minutes = int(parts[5])
                status = parts[6]
                bookings.append({
                    'booking_id': booking_id,
                    'member_name': member_name,
                    'trainer_id': trainer_id,
                    'booking_date': booking_date,
                    'booking_time': booking_time,
                    'duration_minutes': duration_minutes,
                    'status': status
                })
    except Exception:
        bookings = []
    return bookings


def save_booking(booking_data):
    try:
        bookings = load_bookings()
        max_id = max((b['booking_id'] for b in bookings), default=0)
        new_id = max_id + 1
        line = f"{new_id}|{booking_data['member_name']}|{booking_data['trainer_id']}|{booking_data['booking_date']}|{booking_data['booking_time']}|{booking_data['duration_minutes']}|{booking_data['status']}\n"
        with open(os.path.join(DATA_DIR, 'bookings.txt'), 'a', encoding='utf-8') as f:
            f.write(line)
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
                workout_id = int(parts[0])
                member_name = parts[1]
                workout_type = parts[2]
                workout_date = parts[3]
                duration_minutes = int(parts[4])
                calories_burned = int(parts[5])
                notes = parts[6]
                workouts.append({
                    'workout_id': workout_id,
                    'member_name': member_name,
                    'workout_type': workout_type,
                    'workout_date': workout_date,
                    'duration_minutes': duration_minutes,
                    'calories_burned': calories_burned,
                    'notes': notes
                })
    except Exception:
        workouts = []
    return workouts


def save_workout(workout_data):
    try:
        workouts = load_workouts()
        max_id = max((w['workout_id'] for w in workouts), default=0)
        new_id = max_id + 1
        line = f"{new_id}|{workout_data['member_name']}|{workout_data['workout_type']}|{workout_data['workout_date']}|{workout_data['duration_minutes']}|{workout_data['calories_burned']}|{workout_data['notes']}\n"
        with open(os.path.join(DATA_DIR, 'workouts.txt'), 'a', encoding='utf-8') as f:
            f.write(line)
        return True
    except Exception:
        return False


# Flask Route Implementations

@app.route('/')
def root_redirect():
    # Redirect root URL to /dashboard
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    member_status = 'Welcome to your Gym Membership Dashboard!'
    return render_template('dashboard.html', member_status=member_status)


@app.route('/memberships')
def memberships():
    membership_plans = load_memberships()
    return render_template('memberships.html', membership_plans=membership_plans)


@app.route('/plan/<int:plan_id>')
def plan_details(plan_id):
    membership_plans = load_memberships()
    plan = next((p for p in membership_plans if p['membership_id'] == plan_id), None)
    if plan is None:
        plan = {}
    return render_template('plan_details.html', plan=plan)


@app.route('/schedule')
def class_schedule():
    classes = load_classes()
    trainers = load_trainers()
    trainer_names = {t['trainer_id']: t['name'] for t in trainers}
    # Add trainer name to each class dict
    for c in classes:
        c['trainer_name'] = trainer_names.get(c['trainer_id'], 'Unknown')
    class_types = sorted(set(c['class_type'] for c in classes))
    return render_template('class_schedule.html', classes=classes, class_types=class_types)


@app.route('/trainers')
def trainers():
    trainers_list = load_trainers()
    specialties = sorted(set(t['specialty'] for t in trainers_list))
    return render_template('trainers.html', trainers_list=trainers_list, specialties=specialties)


@app.route('/trainer/<int:trainer_id>')
def trainer_detail(trainer_id):
    trainers_list = load_trainers()
    trainer = next((t for t in trainers_list if t['trainer_id'] == trainer_id), None)
    if trainer is None:
        trainer = {}
    return render_template('trainer_detail.html', trainer=trainer)


@app.route('/booking', methods=['GET', 'POST'])
def booking():
    trainers_list = load_trainers()
    booking_success = None

    if request.method == 'POST':
        member_name = request.form.get('member_name', '').strip()
        trainer_id_str = request.form.get('trainer_id', '').strip()
        booking_date = request.form.get('booking_date', '').strip()
        booking_time = request.form.get('booking_time', '').strip()
        duration_str = request.form.get('duration', '').strip()

        try:
            trainer_id = int(trainer_id_str)
            duration_minutes = int(duration_str)
        except ValueError:
            booking_success = False
        else:
            if member_name and booking_date and booking_time and duration_minutes > 0:
                booking_data = {
                    'member_name': member_name,
                    'trainer_id': trainer_id,
                    'booking_date': booking_date,
                    'booking_time': booking_time,
                    'duration_minutes': duration_minutes,
                    'status': 'Pending'
                }
                booking_success = save_booking(booking_data)
            else:
                booking_success = False
        return render_template('booking.html', booking_success=booking_success, trainers_list=trainers_list)

    # GET request
    return render_template('booking.html', trainers_list=trainers_list)


@app.route('/workouts')
def workouts():
    workouts = load_workouts()
    workout_types = sorted(set(w['workout_type'] for w in workouts))
    return render_template('workouts.html', workouts=workouts, workout_types=workout_types)


@app.route('/log_workout', methods=['GET', 'POST'])
def log_workout():
    log_success = False
    if request.method == 'POST':
        workout_type = request.form.get('workout_type', '').strip()
        workout_duration_str = request.form.get('workout_duration', '').strip()
        calories_burned_str = request.form.get('calories_burned', '').strip()
        workout_notes = request.form.get('workout_notes', '').strip()

        try:
            workout_duration = int(workout_duration_str)
            calories_burned = int(calories_burned_str)
        except ValueError:
            log_success = False
        else:
            if workout_type and workout_duration > 0 and calories_burned >= 0:
                workout_data = {
                    'member_name': 'Current User',
                    'workout_type': workout_type,
                    'workout_date': date.today().isoformat(),
                    'duration_minutes': workout_duration,
                    'calories_burned': calories_burned,
                    'notes': workout_notes
                }
                log_success = save_workout(workout_data)

    return render_template('log_workout.html', log_success=log_success)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
