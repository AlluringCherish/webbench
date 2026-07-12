from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

# Helper functions to load data

def load_memberships():
    plans = []
    try:
        with open('data/memberships.txt', 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 6:
                    membership_id = int(parts[0])
                    plan_name = parts[1]
                    price_raw = parts[2]
                    # Convert price if possible
                    try:
                        price = float(price_raw)
                    except ValueError:
                        price = price_raw  # e.g. 'unlimited'
                    billing_cycle = parts[3]
                    features = parts[4]
                    max_classes_raw = parts[5]
                    try:
                        max_classes = int(max_classes_raw)
                    except ValueError:
                        max_classes = max_classes_raw
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


def load_membership_by_id(plan_id):
    plans = load_memberships()
    for plan in plans:
        if plan['membership_id'] == plan_id:
            return plan
    return None


def load_classes():
    classes = []
    try:
        with open('data/classes.txt', 'r', encoding='utf-8') as f:
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
    trainers = []
    try:
        with open('data/trainers.txt', 'r', encoding='utf-8') as f:
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


def load_trainer_by_id(trainer_id):
    trainers = load_trainers()
    for trainer in trainers:
        if trainer['trainer_id'] == trainer_id:
            return trainer
    return None


def load_bookings():
    bookings = []
    try:
        with open('data/bookings.txt', 'r', encoding='utf-8') as f:
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


def save_booking(member_name, trainer_id, booking_date, booking_time, duration_minutes):
    # Generate booking_id as max existing +1
    bookings = load_bookings()
    existing_ids = [b['booking_id'] for b in bookings]
    new_id = max(existing_ids) + 1 if existing_ids else 1
    new_booking_line = f"{new_id}|{member_name}|{trainer_id}|{booking_date}|{booking_time}|{duration_minutes}|Pending"
    try:
        with open('data/bookings.txt', 'a', encoding='utf-8') as f:
            f.write(new_booking_line + "\n")
        return True
    except Exception:
        return False


def load_workouts():
    workouts = []
    try:
        with open('data/workouts.txt', 'r', encoding='utf-8') as f:
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


def save_workout(member_name, workout_type, workout_date, duration_minutes, calories_burned, notes):
    workouts = load_workouts()
    existing_ids = [w['workout_id'] for w in workouts]
    new_id = max(existing_ids) + 1 if existing_ids else 1
    new_line = f"{new_id}|{member_name}|{workout_type}|{workout_date}|{duration_minutes}|{calories_burned}|{notes}"
    try:
        with open('data/workouts.txt', 'a', encoding='utf-8') as f:
            f.write(new_line + "\n")
        return True
    except Exception:
        return False


# Root route redirects to /dashboard
@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard_page'))


# /dashboard route
@app.route('/dashboard')
def dashboard_page():
    return render_template('dashboard.html')


# /memberships route
@app.route('/memberships')
def memberships_page():
    plans = load_memberships()
    return render_template('memberships.html', plans=plans)


# /plan/<int:plan_id> route
@app.route('/plan/<int:plan_id>')
def plan_details(plan_id):
    plan = load_membership_by_id(plan_id)
    reviews = []  # Not defined, so empty list
    if plan is None:
        # Optionally could 404 or show empty
        plan = {}
    return render_template('plan_details.html', plan=plan, reviews=reviews)


# /schedule route
@app.route('/schedule')
def class_schedule():
    classes = load_classes()
    return render_template('class_schedule.html', classes=classes)


# /trainers route
@app.route('/trainers')
def trainers_page():
    trainers = load_trainers()
    return render_template('trainers.html', trainers=trainers)


# /trainer/<int:trainer_id> route
@app.route('/trainer/<int:trainer_id>')
def trainer_detail(trainer_id):
    trainer = load_trainer_by_id(trainer_id)
    reviews = []  # Not defined, so empty list
    if trainer is None:
        trainer = {}
    return render_template('trainer_detail.html', trainer=trainer, reviews=reviews)


# /book route GET and POST
@app.route('/book', methods=['GET', 'POST'])
def pt_booking_page():
    trainers = load_trainers()
    message = None
    if request.method == 'POST':
        # Extract form data
        member_name = request.form.get('member_name', '').strip()
        trainer_id = request.form.get('trainer_id')
        booking_date = request.form.get('session_date', '').strip()
        booking_time = request.form.get('session_time', '').strip()
        duration_minutes = request.form.get('session_duration')

        # Validate inputs
        try:
            trainer_id = int(trainer_id)
            duration_minutes = int(duration_minutes)
        except (TypeError, ValueError):
            message = 'Invalid trainer or duration.'
            return render_template('booking.html', trainers=trainers, message=message)

        if not member_name or not booking_date or not booking_time:
            message = 'All fields are required.'
            return render_template('booking.html', trainers=trainers, message=message)

        # Save booking
        success = save_booking(member_name, trainer_id, booking_date, booking_time, duration_minutes)
        if success:
            message = 'Booking submitted successfully and is pending confirmation.'
        else:
            message = 'Failed to save booking. Please try again later.'

    return render_template('booking.html', trainers=trainers, message=message)


# /workouts route
@app.route('/workouts')
def workouts_page():
    workouts = load_workouts()
    return render_template('workouts.html', workouts=workouts)


# /log_workout route GET and POST
from datetime import date

@app.route('/log_workout', methods=['GET', 'POST'])
def log_workout_page():
    message = None
    if request.method == 'POST':
        # Extract form data
        member_name = request.form.get('member_name', '').strip()
        workout_type = request.form.get('workout_type', '').strip()
        workout_duration = request.form.get('workout_duration')
        calories_burned = request.form.get('calories_burned')
        workout_notes = request.form.get('workout_notes', '').strip()

        # Validate inputs
        try:
            workout_duration = int(workout_duration)
            calories_burned = int(calories_burned)
        except (TypeError, ValueError):
            message = 'Duration and calories burned must be valid numbers.'
            return render_template('log_workout.html', message=message)

        if not member_name or not workout_type:
            message = 'Member name and workout type are required.'
            return render_template('log_workout.html', message=message)

        workout_date = date.today().isoformat()

        success = save_workout(member_name, workout_type, workout_date, workout_duration, calories_burned, workout_notes)
        if success:
            message = 'Workout logged successfully.'
        else:
            message = 'Failed to log workout. Please try again later.'

    return render_template('log_workout.html', message=message)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
