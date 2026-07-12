from flask import Flask, render_template, redirect, url_for, request, abort
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Utility functions for loading data

def load_memberships():
    memberships_path = os.path.join(DATA_DIR, 'memberships.txt')
    plans = []
    try:
        with open(memberships_path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 6:
                    membership_id = int(parts[0])
                    plan_name = parts[1]
                    price = parts[2]
                    billing_cycle = parts[3]
                    features = parts[4]
                    max_classes = parts[5]
                    # max_classes can be 'unlimited' or int or str
                    plans.append({
                        'membership_id': membership_id,
                        'plan_name': plan_name,
                        'price': price,
                        'billing_cycle': billing_cycle,
                        'features': features,
                        'max_classes': max_classes
                    })
    except FileNotFoundError:
        plans = []
    return plans


def load_classes():
    classes_path = os.path.join(DATA_DIR, 'classes.txt')
    classes = []
    try:
        with open(classes_path, 'r', encoding='utf-8') as f:
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
        classes = []
    return classes


def load_trainers():
    trainers_path = os.path.join(DATA_DIR, 'trainers.txt')
    trainers = []
    try:
        with open(trainers_path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 6:
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
    except FileNotFoundError:
        trainers = []
    return trainers


def load_bookings():
    bookings_path = os.path.join(DATA_DIR, 'bookings.txt')
    bookings = []
    try:
        with open(bookings_path, 'r', encoding='utf-8') as f:
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
                    bookings.append({
                        'booking_id': booking_id,
                        'member_name': member_name,
                        'trainer_id': trainer_id,
                        'booking_date': booking_date,
                        'booking_time': booking_time,
                        'duration_minutes': duration_minutes,
                        'status': status
                    })
    except FileNotFoundError:
        bookings = []
    return bookings


def save_booking(booking):
    bookings = load_bookings()
    max_id = max((b['booking_id'] for b in bookings), default=0)
    booking_id = max_id + 1
    booking['booking_id'] = booking_id
    bookings_path = os.path.join(DATA_DIR, 'bookings.txt')
    try:
        with open(bookings_path, 'a', encoding='utf-8') as f:
            line = f"{booking['booking_id']}|{booking['member_name']}|{booking['trainer_id']}|{booking['booking_date']}|{booking['booking_time']}|{booking['duration_minutes']}|{booking['status']}\n"
            f.write(line)
        return True
    except IOError:
        return False


def load_workouts():
    workouts_path = os.path.join(DATA_DIR, 'workouts.txt')
    workouts = []
    try:
        with open(workouts_path, 'r', encoding='utf-8') as f:
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
                    workouts.append({
                        'workout_id': workout_id,
                        'member_name': member_name,
                        'workout_type': workout_type,
                        'workout_date': workout_date,
                        'duration_minutes': duration_minutes,
                        'calories_burned': calories_burned,
                        'notes': notes
                    })
    except FileNotFoundError:
        workouts = []
    return workouts


def save_workout(workout):
    workouts = load_workouts()
    max_id = max((w['workout_id'] for w in workouts), default=0)
    workout_id = max_id + 1
    workout['workout_id'] = workout_id
    workouts_path = os.path.join(DATA_DIR, 'workouts.txt')
    try:
        with open(workouts_path, 'a', encoding='utf-8') as f:
            line = f"{workout['workout_id']}|{workout['member_name']}|{workout['workout_type']}|{workout['workout_date']}|{workout['duration_minutes']}|{workout['calories_burned']}|{workout['notes']}\n"
            f.write(line)
        return True
    except IOError:
        return False


# Simulated function to get reviews for plans or trainers
# For simplicity, return empty list (no reviews)
def get_reviews_for_plan(plan_id):
    # No data source for reviews given
    return []


def get_reviews_for_trainer(trainer_id):
    # No data source for reviews given
    return []


@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@app.route('/memberships')
def memberships():
    plans = load_memberships()
    return render_template('memberships.html', plans=plans)


@app.route('/plan/<int:plan_id>')
def plan_details(plan_id):
    plans = load_memberships()
    plan = next((p for p in plans if p['membership_id'] == plan_id), None)
    if plan is None:
        abort(404)
    reviews = get_reviews_for_plan(plan_id)  # empty list
    return render_template('plan_details.html', plan=plan, reviews=reviews)


@app.route('/classes')
def class_schedule():
    classes = load_classes()
    class_types = sorted(set(c['class_type'] for c in classes))
    return render_template('class_schedule.html', classes=classes, class_types=class_types)


@app.route('/trainers')
def trainer_profiles():
    trainers = load_trainers()
    specialties = sorted(set(t['specialty'] for t in trainers))
    return render_template('trainers.html', trainers=trainers, specialties=specialties)


@app.route('/trainer/<int:trainer_id>')
def trainer_detail(trainer_id):
    trainers = load_trainers()
    trainer = next((t for t in trainers if t['trainer_id'] == trainer_id), None)
    if trainer is None:
        abort(404)
    reviews = get_reviews_for_trainer(trainer_id)  # empty list
    return render_template('trainer_detail.html', trainer=trainer, reviews=reviews)


@app.route('/booking', methods=['GET', 'POST'])
def pt_booking():
    trainers = load_trainers()
    if request.method == 'GET':
        return render_template('booking.html', trainers=trainers)
    else:
        # POST - book a session
        # Expect form fields: member_name, trainer_id, booking_date, booking_time, duration_minutes
        member_name = request.form.get('member_name', '').strip()
        trainer_id_str = request.form.get('trainer_id', '').strip()
        booking_date = request.form.get('booking_date', '').strip()
        booking_time = request.form.get('booking_time', '').strip()
        duration_minutes_str = request.form.get('duration_minutes', '').strip()

        # Validate minimal required fields
        if not member_name or not trainer_id_str or not booking_date or not booking_time or not duration_minutes_str:
            # For simplicity re-render with an error message context (not defined in spec so minimal)
            return render_template('booking.html', trainers=trainers, error='All fields are required.')

        try:
            trainer_id = int(trainer_id_str)
            duration_minutes = int(duration_minutes_str)
        except ValueError:
            return render_template('booking.html', trainers=trainers, error='Invalid numeric input.')

        # Make booking dict
        booking = {
            'member_name': member_name,
            'trainer_id': trainer_id,
            'booking_date': booking_date,
            'booking_time': booking_time,
            'duration_minutes': duration_minutes,
            'status': 'Pending'
        }

        success = save_booking(booking)
        if success:
            message = 'Booking submitted successfully.'
            return render_template('booking.html', trainers=trainers, message=message)
        else:
            return render_template('booking.html', trainers=trainers, error='Failed to save booking.')


@app.route('/workouts')
def workout_records():
    workouts = load_workouts()
    # Possible workout_types for filter dropdown:
    workout_types = sorted(set(w['workout_type'] for w in workouts))
    return render_template('workouts.html', workouts=workouts, workout_types=workout_types)


@app.route('/log_workout', methods=['GET', 'POST'])
def log_workout():
    if request.method == 'GET':
        return render_template('log_workout.html')
    else:
        # POST: form fields - member_name, workout_type, workout_duration, calories_burned, workout_notes
        # member_name is not specified in spec form but is required for data file. Since spec doesn't specify member_id input, we assume a hardcoded member or require it.
        # Spec does not specify member_name input, but workouts file requires it; Assume for simplicity member_name is hardcoded as 'Guest'
        workout_type = request.form.get('workout_type', '').strip()
        workout_duration_str = request.form.get('workout_duration', '').strip()
        calories_burned_str = request.form.get('calories_burned', '').strip()
        workout_notes = request.form.get('workout_notes', '').strip()

        if not workout_type or not workout_duration_str or not calories_burned_str:
            return render_template('log_workout.html', error='Required fields are missing.')

        try:
            workout_duration = int(workout_duration_str)
            calories_burned = int(calories_burned_str)
        except ValueError:
            return render_template('log_workout.html', error='Duration and calories must be numeric.')

        # Build workout dict
        workout = {
            'member_name': 'Guest',  # fixed, no member login defined
            'workout_type': workout_type,
            'workout_date': '',  # no date supplied in form, so use empty string or could use today - spec not defined.
            'duration_minutes': workout_duration,
            'calories_burned': calories_burned,
            'notes': workout_notes
        }

        # For workout_date, spec requires date field, but form does not have input. We'll use an ISO date string of empty or today?
        # Using empty string as not specified
        workout['workout_date'] = ''

        success = save_workout(workout)
        if success:
            return render_template('log_workout.html', message='Workout logged successfully.')
        else:
            return render_template('log_workout.html', error='Failed to save workout.')


if __name__ == '__main__':
    app.run(debug=True, port=5000)
