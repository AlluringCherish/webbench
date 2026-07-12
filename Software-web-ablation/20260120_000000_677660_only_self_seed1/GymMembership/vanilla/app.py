from flask import Flask, render_template, redirect, url_for, request, abort
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Utility functions to load data from files

def load_memberships():
    memberships = []
    filepath = os.path.join(DATA_DIR, 'memberships.txt')
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 6:
                    membership_id = int(parts[0])
                    plan_name = parts[1]
                    price = float(parts[2])
                    billing_cycle = parts[3]
                    features = parts[4]
                    max_classes_raw = parts[5]
                    max_classes = int(max_classes_raw) if max_classes_raw.isdigit() else max_classes_raw
                    plan = {
                        'membership_id': membership_id,
                        'plan_name': plan_name,
                        'price': price,
                        'billing_cycle': billing_cycle,
                        'features': features,
                        'max_classes': max_classes
                    }
                    memberships.append(plan)
    except FileNotFoundError:
        pass
    return memberships


def load_classes():
    classes = []
    filepath = os.path.join(DATA_DIR, 'classes.txt')
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 8:
                    class_id = int(parts[0])
                    class_name = parts[1]
                    trainer_id = int(parts[2])
                    class_type = parts[3]
                    schedule_day = parts[4]
                    schedule_time = parts[5]
                    capacity = int(parts[6])
                    duration = int(parts[7])
                    cls = {
                        'class_id': class_id,
                        'class_name': class_name,
                        'trainer_id': trainer_id,
                        'class_type': class_type,
                        'schedule_day': schedule_day,
                        'schedule_time': schedule_time,
                        'capacity': capacity,
                        'duration': duration
                    }
                    classes.append(cls)
    except FileNotFoundError:
        pass
    return classes


def load_trainers():
    trainers = []
    filepath = os.path.join(DATA_DIR, 'trainers.txt')
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 6:
                    trainer_id = int(parts[0])
                    name = parts[1]
                    specialty = parts[2]
                    certifications = parts[3]
                    experience_years = int(parts[4])
                    bio = parts[5]
                    trainer = {
                        'trainer_id': trainer_id,
                        'name': name,
                        'specialty': specialty,
                        'certifications': certifications,
                        'experience_years': experience_years,
                        'bio': bio
                    }
                    trainers.append(trainer)
    except FileNotFoundError:
        pass
    return trainers


def load_bookings():
    bookings = []
    filepath = os.path.join(DATA_DIR, 'bookings.txt')
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 7:
                    booking_id = int(parts[0])
                    member_name = parts[1]
                    trainer_id = int(parts[2])
                    booking_date = parts[3]
                    booking_time = parts[4]
                    duration_minutes = int(parts[5])
                    status = parts[6]
                    booking = {
                        'booking_id': booking_id,
                        'member_name': member_name,
                        'trainer_id': trainer_id,
                        'booking_date': booking_date,
                        'booking_time': booking_time,
                        'duration_minutes': duration_minutes,
                        'status': status
                    }
                    bookings.append(booking)
    except FileNotFoundError:
        pass
    return bookings


def save_booking(member_name, trainer_id, booking_date, booking_time, duration_minutes):
    filepath = os.path.join(DATA_DIR, 'bookings.txt')
    bookings = load_bookings()
    new_id = 1
    if bookings:
        new_id = max(b['booking_id'] for b in bookings) + 1
    new_booking_line = f"{new_id}|{member_name}|{trainer_id}|{booking_date}|{booking_time}|{duration_minutes}|Pending"
    try:
        with open(filepath, 'a', encoding='utf-8') as f:
            f.write(new_booking_line + "\n")
        return True
    except Exception:
        return False


def load_workouts():
    workouts = []
    filepath = os.path.join(DATA_DIR, 'workouts.txt')
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 7:
                    workout_id = int(parts[0])
                    member_name = parts[1]
                    workout_type = parts[2]
                    workout_date = parts[3]
                    duration_minutes = int(parts[4])
                    calories_burned = int(parts[5])
                    notes = parts[6]
                    workout = {
                        'workout_id': workout_id,
                        'member_name': member_name,
                        'workout_type': workout_type,
                        'workout_date': workout_date,
                        'duration_minutes': duration_minutes,
                        'calories_burned': calories_burned,
                        'notes': notes
                    }
                    workouts.append(workout)
    except FileNotFoundError:
        pass
    return workouts


def save_workout(member_name, workout_type, workout_date, duration_minutes, calories_burned, notes):
    filepath = os.path.join(DATA_DIR, 'workouts.txt')
    workouts = load_workouts()
    new_id = 1
    if workouts:
        new_id = max(w['workout_id'] for w in workouts) + 1
    new_workout_line = f"{new_id}|{member_name}|{workout_type}|{workout_date}|{duration_minutes}|{calories_burned}|{notes}"
    try:
        with open(filepath, 'a', encoding='utf-8') as f:
            f.write(new_workout_line + "\n")
        return True
    except Exception:
        return False


# Route implementations

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    member_welcome_msg = "Welcome back, valued member!"
    featured_classes = []
    # Optional quick_links included as None if not available
    quick_links = None

    # For demo, add first three classes as featured if any
    classes = load_classes()
    if classes:
        featured_classes = classes[:3]

    return render_template('dashboard.html', member_welcome_msg=member_welcome_msg, featured_classes=featured_classes, quick_links=quick_links)


@app.route('/memberships')
def memberships():
    plans = load_memberships()
    return render_template('memberships.html', plans=plans)


@app.route('/plan/<int:plan_id>')
def plan_details(plan_id):
    plans = load_memberships()
    plan = next((p for p in plans if p['membership_id'] == plan_id), None)
    if not plan:
        abort(404)

    # For reviews, use bookings.txt status Pending/Confirmed might not correspond to reviews - no review data file given
    # Use empty list for reviews as not specified
    reviews = []

    return render_template('plan_details.html', plan=plan, reviews=reviews)


@app.route('/classes')
def class_schedule():
    classes = load_classes()
    # We omit trainer_name here; we can map trainer_id to name
    trainers = load_trainers()
    trainer_dict = {t['trainer_id']: t['name'] for t in trainers}
    classes_render = []
    for c in classes:
        c_dict = {
            'class_id': c['class_id'],
            'class_name': c['class_name'],
            'trainer_name': trainer_dict.get(c['trainer_id'], 'Unknown'),
            'class_type': c['class_type'],
            'schedule_day': c['schedule_day'],
            'schedule_time': c['schedule_time'],
            'capacity': c['capacity'],
            'duration': c['duration']
        }
        classes_render.append(c_dict)
    return render_template('class_schedule.html', classes=classes_render)


@app.route('/trainers')
def trainer_profiles():
    trainers = load_trainers()
    # We supply only subset of keys excluding bio for this list
    trainers_list = []
    for t in trainers:
        trainers_list.append({
            'trainer_id': t['trainer_id'],
            'name': t['name'],
            'specialty': t['specialty'],
            'certifications': t['certifications'],
            'experience_years': t['experience_years']
        })
    return render_template('trainer_profiles.html', trainers=trainers_list)


@app.route('/trainer/<int:trainer_id>')
def trainer_detail(trainer_id):
    trainers = load_trainers()
    trainer = next((t for t in trainers if t['trainer_id'] == trainer_id), None)
    if not trainer:
        abort(404)

    # No specific review data given, provide empty list
    reviews = []
    return render_template('trainer_detail.html', trainer=trainer, reviews=reviews)


@app.route('/booking', methods=['GET'])
def pt_booking():
    trainers = load_trainers()
    # Provide only trainer_id and name
    trainers_list = [{'trainer_id': t['trainer_id'], 'name': t['name']} for t in trainers]
    return render_template('pt_booking.html', trainers=trainers_list)


@app.route('/booking', methods=['POST'])
def confirm_booking():
    # Expected form data: trainer_id:int, session_date:str, session_time:str, session_duration:int
    trainer_id = request.form.get('trainer_id')
    session_date = request.form.get('session_date')
    session_time = request.form.get('session_time')
    session_duration = request.form.get('session_duration')

    # Validate presence and conversion
    if not trainer_id or not session_date or not session_time or not session_duration:
        abort(400)
    try:
        trainer_id = int(trainer_id)
        session_duration = int(session_duration)
        if session_duration not in [30, 60, 90]:
            abort(400)
    except ValueError:
        abort(400)

    # For this implementation, member_name is fixed as 'John Doe' (not specified how to get logged in member)
    member_name = 'John Doe'

    # Save booking with status 'Pending'
    saved = save_booking(member_name, trainer_id, session_date, session_time, session_duration)
    if not saved:
        abort(500)

    # After booking, redirect to dashboard
    return redirect(url_for('dashboard'))


@app.route('/workouts')
def workout_records():
    workouts = load_workouts()
    return render_template('workout_records.html', workouts=workouts)


@app.route('/log-workout', methods=['GET'])
def log_workout():
    return render_template('log_workout.html')


@app.route('/log-workout', methods=['POST'])
def submit_workout():
    # Expects form data: workout_type:str, workout_duration:int, calories_burned:int, workout_notes:str
    workout_type = request.form.get('workout_type')
    workout_duration = request.form.get('workout_duration')
    calories_burned = request.form.get('calories_burned')
    workout_notes = request.form.get('workout_notes', '')

    if not workout_type or not workout_duration or not calories_burned:
        abort(400)

    try:
        workout_duration = int(workout_duration)
        calories_burned = int(calories_burned)
    except ValueError:
        abort(400)

    # Member name assumed static as John Doe
    member_name = 'John Doe'

    from datetime import date
    workout_date = date.today().isoformat()

    saved = save_workout(member_name, workout_type, workout_date, workout_duration, calories_burned, workout_notes)
    if not saved:
        abort(500)

    return redirect(url_for('workout_records'))


if __name__ == '__main__':
    app.run(debug=True, port=5000)
