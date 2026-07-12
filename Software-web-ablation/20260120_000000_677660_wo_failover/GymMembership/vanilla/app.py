from flask import Flask, render_template, redirect, url_for, request
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Utility functions to load data from pipe-delimited files

def load_memberships():
    memberships = []
    path = os.path.join(DATA_DIR, 'memberships.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 6:
                    continue
                membership_id = int(parts[0])
                plan_name = parts[1]
                price = parts[2]
                billing_cycle = parts[3]
                features = parts[4]
                max_classes = parts[5]
                memberships.append({
                    'membership_id': membership_id,
                    'plan_name': plan_name,
                    'price': price,
                    'billing_cycle': billing_cycle,
                    'features': features,
                    'max_classes': max_classes
                })
    except IOError:
        # File not found or unable to read
        pass
    return memberships


def load_classes():
    classes = []
    path = os.path.join(DATA_DIR, 'classes.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
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
    except IOError:
        pass
    return classes


def load_trainers():
    trainers = []
    path = os.path.join(DATA_DIR, 'trainers.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 6:
                    continue
                trainer_id = int(parts[0])
                name = parts[1]
                specialty = parts[2]
                certifications = parts[3]
                try:
                    experience_years = int(parts[4])
                except ValueError:
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
    except IOError:
        pass
    return trainers


def load_bookings():
    bookings = []
    path = os.path.join(DATA_DIR, 'bookings.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 7:
                    continue
                booking_id = int(parts[0])
                member_name = parts[1]
                trainer_id = int(parts[2])
                booking_date = parts[3]
                booking_time = parts[4]
                try:
                    duration_minutes = int(parts[5])
                except ValueError:
                    duration_minutes = 0
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
    except IOError:
        pass
    return bookings


def save_booking(booking):
    # booking is dict with keys member_name, trainer_id, booking_date, booking_time, duration_minutes, status
    path = os.path.join(DATA_DIR, 'bookings.txt')
    bookings = load_bookings()
    max_id = max((b['booking_id'] for b in bookings), default=0)
    booking_id = max_id + 1
    line = f"{booking_id}|{booking['member_name']}|{booking['trainer_id']}|{booking['booking_date']}|{booking['booking_time']}|{booking['duration_minutes']}|{booking['status']}\n"
    try:
        with open(path, 'a', encoding='utf-8') as f:
            f.write(line)
        return True
    except IOError:
        return False


def load_workouts():
    workouts = []
    path = os.path.join(DATA_DIR, 'workouts.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 7:
                    continue
                workout_id = int(parts[0])
                member_name = parts[1]
                workout_type = parts[2]
                workout_date = parts[3]
                try:
                    duration_minutes = int(parts[4])
                except ValueError:
                    duration_minutes = 0
                try:
                    calories_burned = int(parts[5])
                except ValueError:
                    calories_burned = 0
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
    except IOError:
        pass
    return workouts


def save_workout(workout):
    # workout is dict with keys member_name, workout_type, workout_date, duration_minutes, calories_burned, notes
    path = os.path.join(DATA_DIR, 'workouts.txt')
    workouts = load_workouts()
    max_id = max((w['workout_id'] for w in workouts), default=0)
    workout_id = max_id + 1
    line = f"{workout_id}|{workout['member_name']}|{workout['workout_type']}|{workout['workout_date']}|{workout['duration_minutes']}|{workout['calories_burned']}|{workout['notes']}\n"
    try:
        with open(path, 'a', encoding='utf-8') as f:
            f.write(line)
        return True
    except IOError:
        return False


# Routes

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    # Compose context variables
    member_welcome_msg = "Welcome back, valued member!"

    # featured_classes: list of dict with keys class_name, schedule_day, schedule_time
    # For simplicity, pick first 3 classes from classes.txt
    classes = load_classes()
    featured_classes = []
    for c in classes[:3]:
        featured_classes.append({
            'class_name': c['class_name'],
            'schedule_day': c['schedule_day'],
            'schedule_time': c['schedule_time']
        })

    quick_links = {
        'browse-membership-button': url_for('memberships'),
        'view-schedule-button': url_for('class_schedule'),
        'book-trainer-button': url_for('pt_booking')
    }

    return render_template('dashboard.html',
                           member_welcome_msg=member_welcome_msg,
                           featured_classes=featured_classes,
                           quick_links=quick_links)


@app.route('/memberships')
def memberships():
    memberships = load_memberships()
    return render_template('memberships.html', memberships=memberships)


@app.route('/plan/<int:plan_id>')
def plan_details(plan_id):
    memberships = load_memberships()
    plan = None
    for m in memberships:
        if m['membership_id'] == plan_id:
            plan = m
            break

    if plan is None:
        # Plan not found, handle gracefully with empty data
        plan = {
            'membership_id': plan_id,
            'plan_name': 'Unknown Plan',
            'price': '',
            'billing_cycle': '',
            'features': '',
            'max_classes': ''
        }

    # No review data source specified, create empty list for reviews
    reviews = []

    return render_template('plan_details.html', plan=plan, reviews=reviews)


@app.route('/classes')
def class_schedule():
    classes = load_classes()
    return render_template('class_schedule.html', classes=classes)


@app.route('/trainers')
def trainer_profiles():
    trainers = load_trainers()
    return render_template('trainers.html', trainers=trainers)


@app.route('/trainer/<int:trainer_id>')
def trainer_detail(trainer_id):
    trainers = load_trainers()
    trainer = None
    for t in trainers:
        if t['trainer_id'] == trainer_id:
            trainer = t
            break

    if trainer is None:
        trainer = {
            'trainer_id': trainer_id,
            'name': 'Unknown Trainer',
            'specialty': '',
            'certifications': '',
            'experience_years': 0,
            'bio': ''
        }

    # No review source specified, empty list
    reviews = []

    return render_template('trainer_detail.html', trainer=trainer, reviews=reviews)


@app.route('/booking', methods=['GET', 'POST'])
def pt_booking():
    trainers = load_trainers()
    if request.method == 'POST':
        # Extract form data
        member_name = request.form.get('member_name', '').strip()
        trainer_id_str = request.form.get('trainer_id', '')
        booking_date = request.form.get('booking_date', '').strip()
        booking_time = request.form.get('booking_time', '').strip()
        duration_minutes_str = request.form.get('duration_minutes', '')

        booking_status = ''
        try:
            trainer_id = int(trainer_id_str)
            duration_minutes = int(duration_minutes_str)
        except (ValueError, TypeError):
            booking_status = 'Invalid input data.'
            return render_template('booking.html', trainers=[{'trainer_id': t['trainer_id'], 'name': t['name']} for t in trainers], booking_status=booking_status)

        if not member_name or not booking_date or not booking_time:
            booking_status = 'Please fill out all required fields.'
            return render_template('booking.html', trainers=[{'trainer_id': t['trainer_id'], 'name': t['name']} for t in trainers], booking_status=booking_status)

        # Save booking
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
            booking_status = 'Booking successfully submitted!'
        else:
            booking_status = 'Failed to save booking. Please try again later.'

        return render_template('booking.html', trainers=[{'trainer_id': t['trainer_id'], 'name': t['name']} for t in trainers], booking_status=booking_status)

    # GET request
    # Provide only required keys for trainers
    trainers_simple = [{'trainer_id': t['trainer_id'], 'name': t['name']} for t in trainers]
    return render_template('booking.html', trainers=trainers_simple)


@app.route('/workouts')
def workout_records():
    workouts = load_workouts()
    return render_template('workouts.html', workouts=workouts)


@app.route('/log_workout', methods=['GET', 'POST'])
def log_workout():
    log_status = ''
    if request.method == 'POST':
        member_name = request.form.get('member_name', '').strip()
        workout_type = request.form.get('workout_type', '').strip()
        workout_date = request.form.get('workout_date', '').strip()
        duration_str = request.form.get('workout_duration', '')
        calories_str = request.form.get('calories_burned', '')
        notes = request.form.get('workout_notes', '').strip()

        try:
            duration_minutes = int(duration_str)
            calories_burned = int(calories_str)
        except (ValueError, TypeError):
            log_status = 'Invalid input for duration or calories burned.'
            return render_template('log_workout.html', log_status=log_status)

        if not member_name or not workout_type or not workout_date:
            log_status = 'Please fill out all required fields.'
            return render_template('log_workout.html', log_status=log_status)

        workout = {
            'member_name': member_name,
            'workout_type': workout_type,
            'workout_date': workout_date,
            'duration_minutes': duration_minutes,
            'calories_burned': calories_burned,
            'notes': notes
        }
        success = save_workout(workout)
        if success:
            log_status = 'Workout log submitted successfully!'
        else:
            log_status = 'Failed to save workout log. Please try again later.'

        return render_template('log_workout.html', log_status=log_status)

    return render_template('log_workout.html')


if __name__ == '__main__':
    app.run(debug=True, port=5000)
