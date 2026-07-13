from flask import Flask, render_template, request, redirect, url_for, abort
import os
from datetime import datetime

app = Flask(__name__)
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')

# --- Helper functions to read/write data files ---

def read_memberships():
    memberships = []
    try:
        with open(os.path.join(DATA_DIR, 'memberships.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 6:
                    continue
                membership_id = int(parts[0])
                plan_name = parts[1]
                try:
                    price = float(parts[2])
                except ValueError:
                    price = 0.0
                billing_cycle = parts[3]
                features = [f.strip() for f in parts[4].split(',')] if parts[4].strip() else []
                max_classes = parts[5]
                try:
                    if max_classes.lower() != 'unlimited':
                        max_classes = int(max_classes)
                except:
                    pass
                memberships.append({
                    'id': membership_id,
                    'plan_name': plan_name,
                    'price': price,
                    'billing_cycle': billing_cycle,
                    'features': features,
                    'max_classes': max_classes
                })
    except FileNotFoundError:
        pass
    return memberships

def read_classes():
    classes = []
    try:
        with open(os.path.join(DATA_DIR, 'classes.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 8:
                    continue
                class_id = int(parts[0])
                class_name = parts[1]
                trainer_id = int(parts[2])
                class_type = parts[3]
                schedule_day = parts[4]
                schedule_time = parts[5]
                try:
                    capacity = int(parts[6])
                except:
                    capacity = 0
                try:
                    duration = int(parts[7])
                except:
                    duration = 0
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
    except FileNotFoundError:
        pass
    return classes

def read_trainers():
    trainers = []
    try:
        with open(os.path.join(DATA_DIR, 'trainers.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 6:
                    continue
                trainer_id = int(parts[0])
                name = parts[1]
                specialty = parts[2]
                certifications = parts[3]
                try:
                    experience_years = int(parts[4])
                except:
                    experience_years = 0
                bio = parts[5]
                trainers.append({
                    'trainer_id': trainer_id,
                    'name': name,
                    'specialty': specialty,
                    'certifications': certifications,
                    'experience_years': experience_years,
                    'bio': bio
                })
    except FileNotFoundError:
        pass
    return trainers


def read_bookings():
    bookings = []
    try:
        with open(os.path.join(DATA_DIR, 'bookings.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 7:
                    continue
                try:
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
                except:
                    continue
    except FileNotFoundError:
        pass
    return bookings


def read_workouts():
    workouts = []
    try:
        with open(os.path.join(DATA_DIR, 'workouts.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 7:
                    continue
                try:
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
                except:
                    continue
    except FileNotFoundError:
        pass
    return workouts


def append_booking(booking):
    # booking dict keys: booking_id, member_name, trainer_id, booking_date, booking_time, duration_minutes, status
    with open(os.path.join(DATA_DIR, 'bookings.txt'), 'a', encoding='utf-8') as f:
        line = f"{booking['booking_id']}|{booking['member_name']}|{booking['trainer_id']}|{booking['booking_date']}|{booking['booking_time']}|{booking['duration_minutes']}|{booking['status']}\n"
        f.write(line)


def append_workout(workout):
    # workout dict keys: workout_id, member_name, workout_type, workout_date, duration_minutes, calories_burned, notes
    with open(os.path.join(DATA_DIR, 'workouts.txt'), 'a', encoding='utf-8') as f:
        line = f"{workout['workout_id']}|{workout['member_name']}|{workout['workout_type']}|{workout['workout_date']}|{workout['duration_minutes']}|{workout['calories_burned']}|{workout['notes']}\n"
        f.write(line)


# --- Routes ---

@app.route('/')
def dashboard():
    # Load member highlights (static for now)
    member_status = "Active Basic Member"

    # Load featured classes for dashboard - get few classes and their trainer names
    classes = read_classes()
    trainers = {t['trainer_id']: t['name'] for t in read_trainers()}
    featured_classes = []
    for cls in classes[:3]:
        featured_classes.append({
            'class_id': cls['class_id'],
            'class_name': cls['class_name'],
            'trainer_name': trainers.get(cls['trainer_id'], "Unknown"),
            'schedule_day': cls['schedule_day'],
            'schedule_time': cls['schedule_time']
        })

    # Add class_type to featured classes to match frontend display
    for featured in featured_classes:
        # find matching class
        for cls in classes:
            if cls['class_id'] == featured['class_id']:
                featured['class_type'] = cls['class_type']
                break

    return render_template('dashboard.html', member_status=member_status, featured_classes=featured_classes)


@app.route('/memberships')
def membership_plans():
    filter_options = ["Basic", "Premium", "Elite"]
    selected_type = request.args.get('type')

    memberships = read_memberships()
    if selected_type and selected_type in filter_options:
        filtered = [plan for plan in memberships if selected_type.lower() in plan['plan_name'].lower()]
        memberships = filtered
    else:
        selected_type = None

    return render_template('membership_plans.html', membership_plans=memberships, filter_options=filter_options, selected_type=selected_type)


@app.route('/membership/<int:membership_id>')
def plan_details(membership_id):
    memberships = read_memberships()
    plan = next((p for p in memberships if p['id'] == membership_id), None)
    if plan is None:
        abort(404)

    reviews = []
    return render_template('plan_details.html', plan=plan, reviews=reviews)


@app.route('/classes')
def class_schedule():
    classes = read_classes()
    trainers = {t['trainer_id']: t for t in read_trainers()}

    search_term = request.args.get('search', '').strip()
    selected_type = request.args.get('type')

    class_types_set = set(c['class_type'] for c in classes)
    class_types = sorted(class_types_set)

    filtered_classes = []
    for cls in classes:
        trainer = trainers.get(cls['trainer_id'], {})
        trainer_name = trainer.get('name', "Unknown")

        if search_term:
            if search_term.lower() not in cls['class_name'].lower() and search_term.lower() not in trainer_name.lower():
                continue

        if selected_type and selected_type != '' and cls['class_type'] != selected_type:
            continue

        filtered_classes.append({
            'class_id': cls['class_id'],
            'class_name': cls['class_name'],
            'trainer_name': trainer_name,
            'class_type': cls['class_type'],
            'schedule_day': cls['schedule_day'],
            'schedule_time': cls['schedule_time'],
            'capacity': cls['capacity'],
            'duration': cls['duration']
        })

    return render_template('class_schedule.html', classes=filtered_classes, search_term=search_term, selected_type=selected_type, class_types=class_types)


@app.route('/trainers')
def trainer_profiles():
    trainers = read_trainers()

    search_term = request.args.get('search', '').strip()
    selected_specialty = request.args.get('specialty')

    specialty_options = ["Strength", "Cardio", "Flexibility", "Weight Loss"]

    filtered_trainers = []
    for tr in trainers:
        if search_term:
            if search_term.lower() not in tr['name'].lower() and search_term.lower() not in tr['specialty'].lower():
                continue
        if selected_specialty and selected_specialty != '' and tr['specialty'] != selected_specialty:
            continue
        filtered_trainers.append(tr)

    return render_template('trainer_profiles.html', trainers=filtered_trainers, search_term=search_term, selected_specialty=selected_specialty, specialty_options=specialty_options)


@app.route('/trainer/<int:trainer_id>')
def trainer_detail(trainer_id):
    trainers = read_trainers()
    trainer = next((t for t in trainers if t['trainer_id'] == trainer_id), None)
    if trainer is None:
        abort(404)

    certifications = [c.strip() for c in trainer['certifications'].split(',')] if trainer['certifications'] else []
    trainer['certifications'] = certifications

    reviews = []

    return render_template('trainer_detail.html', trainer=trainer, reviews=reviews)


@app.route('/booking', methods=['GET', 'POST'])
def pt_booking():
    if request.method == 'GET':
        trainers = read_trainers()
        trainers_simple = [{'trainer_id': t['trainer_id'], 'name': t['name']} for t in trainers]

        available_timeslots = ["08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00"]
        session_durations = [30, 60, 90]

        try:
            preselected_trainer_id = int(request.args.get('preselected_trainer_id'))
        except (TypeError, ValueError):
            preselected_trainer_id = None

        return render_template('pt_booking.html', trainers=trainers_simple, available_timeslots=available_timeslots, session_durations=session_durations, preselected_trainer_id=preselected_trainer_id)

    elif request.method == 'POST':
        member_name = request.form.get('member_name', '').strip()
        trainer_id_str = request.form.get('trainer_id')
        session_date = request.form.get('session_date')
        session_time = request.form.get('session_time')
        session_duration_str = request.form.get('session_duration')

        errors = []

        if not member_name:
            errors.append('Member name is required.')
        try:
            trainer_id = int(trainer_id_str)
        except:
            errors.append('Invalid trainer selected.')
        if not session_date:
            errors.append('Session date is required.')
        else:
            try:
                datetime.strptime(session_date, '%Y-%m-%d')
            except:
                errors.append('Invalid session date format.')
        if not session_time:
            errors.append('Session time is required.')
        else:
            try:
                datetime.strptime(session_time, '%H:%M')
            except:
                errors.append('Invalid session time format.')
        try:
            session_duration = int(session_duration_str)
            if session_duration not in [30,60,90]:
                errors.append('Invalid session duration.')
        except:
            errors.append('Invalid session duration.')

        if errors:
            return abort(400, ', '.join(errors))

        bookings = read_bookings()
        if bookings:
            max_id = max(b['booking_id'] for b in bookings)
            new_id = max_id + 1
        else:
            new_id = 1

        new_booking = {
            'booking_id': new_id,
            'member_name': member_name,
            'trainer_id': trainer_id,
            'booking_date': session_date,
            'booking_time': session_time,
            'duration_minutes': session_duration,
            'status': 'Pending'
        }

        append_booking(new_booking)

        return redirect(url_for('dashboard'))


@app.route('/workouts')
def workout_records():
    workouts = read_workouts()
    selected_type = request.args.get('type')

    workout_type_filters = ["Class", "PT Session", "Personal"]

    if selected_type and selected_type in workout_type_filters:
        filtered = [w for w in workouts if w['workout_type'] == selected_type]
    else:
        filtered = workouts
        selected_type = None

    return render_template('workout_records.html', workouts=filtered, selected_type=selected_type, workout_type_filters=workout_type_filters)


@app.route('/log-workout', methods=['GET', 'POST'])
def log_workout():
    workout_types = ["Cardio", "Strength", "Flexibility", "Sports"]
    if request.method == 'GET':
        return render_template('log_workout.html', workout_types=workout_types)
    elif request.method == 'POST':
        member_name = request.form.get('member_name', '').strip()
        workout_type = request.form.get('workout_type')
        workout_duration_str = request.form.get('workout_duration')
        calories_burned_str = request.form.get('calories_burned')
        workout_notes = request.form.get('workout_notes', '').strip()
        workout_date = request.form.get('workout_date')

        errors = []
        if not member_name:
            errors.append('Member name is required.')
        if not workout_type or workout_type not in workout_types:
            errors.append('Invalid workout type.')
        try:
            workout_duration = int(workout_duration_str)
            if workout_duration <= 0:
                errors.append('Workout duration must be positive.')
        except:
            errors.append('Invalid workout duration.')
        try:
            calories_burned = int(calories_burned_str)
            if calories_burned < 0:
                errors.append('Calories burned cannot be negative.')
        except:
            errors.append('Invalid calories burned.')

        if workout_date:
            try:
                datetime.strptime(workout_date, '%Y-%m-%d')
            except:
                errors.append('Invalid workout date format.')
        else:
            workout_date = datetime.now().strftime('%Y-%m-%d')

        if errors:
            return abort(400, ', '.join(errors))

        workouts = read_workouts()
        if workouts:
            max_id = max(w['workout_id'] for w in workouts)
            new_id = max_id + 1
        else:
            new_id = 1

        new_workout = {
            'workout_id': new_id,
            'member_name': member_name,
            'workout_type': workout_type,
            'workout_date': workout_date,
            'duration_minutes': workout_duration,
            'calories_burned': calories_burned,
            'notes': workout_notes
        }

        append_workout(new_workout)
        return redirect(url_for('workout_records'))


if __name__ == '__main__':
    app.run(debug=True)
