from flask import Flask, render_template, redirect, url_for, request
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Helper functions to load data for each data file

def load_memberships():
    memberships = []
    path = os.path.join(DATA_DIR, 'memberships.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 6:
                    membership = {
                        'membership_id': int(parts[0]),
                        'plan_name': parts[1],
                        'price': float(parts[2]),
                        'billing_cycle': parts[3],
                        'features': parts[4],
                        'max_classes': parts[5],
                    }
                    memberships.append(membership)
    except Exception:
        pass
    return memberships


def load_classes():
    classes = []
    path = os.path.join(DATA_DIR, 'classes.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 8:
                    try:
                        class_entry = {
                            'class_id': int(parts[0]),
                            'class_name': parts[1],
                            'trainer_id': int(parts[2]),
                            'class_type': parts[3],
                            'schedule_day': parts[4],
                            'schedule_time': parts[5],
                            'capacity': int(parts[6]),
                            'duration': int(parts[7])
                        }
                        classes.append(class_entry)
                    except ValueError:
                        continue
    except Exception:
        pass
    return classes


def load_trainers():
    trainers = []
    path = os.path.join(DATA_DIR, 'trainers.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 6:
                    try:
                        trainer = {
                            'trainer_id': int(parts[0]),
                            'name': parts[1],
                            'specialty': parts[2],
                            'certifications': parts[3],
                            'experience_years': int(parts[4]),
                            'bio': parts[5],
                        }
                        trainers.append(trainer)
                    except ValueError:
                        continue
    except Exception:
        pass
    return trainers


def load_bookings():
    bookings = []
    path = os.path.join(DATA_DIR, 'bookings.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 7:
                    try:
                        booking = {
                            'booking_id': int(parts[0]),
                            'member_name': parts[1],
                            'trainer_id': int(parts[2]),
                            'booking_date': parts[3],
                            'booking_time': parts[4],
                            'duration_minutes': int(parts[5]),
                            'status': parts[6],
                        }
                        bookings.append(booking)
                    except ValueError:
                        continue
    except Exception:
        pass
    return bookings


def save_booking(booking_data):
    # booking_data: dict with keys matching booking file schema
    path = os.path.join(DATA_DIR, 'bookings.txt')
    try:
        # Append new booking to file
        with open(path, 'a', encoding='utf-8') as f:
            f.write(f"{booking_data['booking_id']}|{booking_data['member_name']}|{booking_data['trainer_id']}|{booking_data['booking_date']}|{booking_data['booking_time']}|{booking_data['duration_minutes']}|{booking_data['status']}\n")
        return True
    except Exception:
        return False


def load_workouts():
    workouts = []
    path = os.path.join(DATA_DIR, 'workouts.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 7:
                    try:
                        workout = {
                            'workout_id': int(parts[0]),
                            'member_name': parts[1],
                            'workout_type': parts[2],
                            'workout_date': parts[3],
                            'duration_minutes': int(parts[4]),
                            'calories_burned': int(parts[5]),
                            'notes': parts[6],
                        }
                        workouts.append(workout)
                    except ValueError:
                        continue
    except Exception:
        pass
    return workouts


def save_workout(workout_data):
    # workout_data: dict with keys matching workouts file schema
    path = os.path.join(DATA_DIR, 'workouts.txt')
    try:
        # Append new workout
        with open(path, 'a', encoding='utf-8') as f:
            f.write(f"{workout_data['workout_id']}|{workout_data['member_name']}|{workout_data['workout_type']}|{workout_data['workout_date']}|{workout_data['duration_minutes']}|{workout_data['calories_burned']}|{workout_data['notes']}\n")
        return True
    except Exception:
        return False


@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    # No context variables
    return render_template('dashboard.html')


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
    # No reviews modeled, pass empty list
    plan_reviews = []
    return render_template('plan_details.html', plan=plan, plan_reviews=plan_reviews)


@app.route('/schedule')
def class_schedule():
    classes = load_classes()
    return render_template('schedule.html', classes=classes)


@app.route('/trainers')
def trainers_profiles():
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
    trainer_reviews = []  # No reviews modeled
    return render_template('trainer_detail.html', trainer=trainer, trainer_reviews=trainer_reviews)


@app.route('/book-pt', methods=['GET', 'POST'])
def pt_booking():
    trainers = load_trainers()
    feedback = None

    if request.method == 'POST':
        member_name = request.form.get('member_name', '').strip()
        trainer_id_str = request.form.get('trainer_id', '').strip()
        booking_date = request.form.get('booking_date', '').strip()
        booking_time = request.form.get('booking_time', '').strip()
        duration_minutes_str = request.form.get('duration_minutes', '').strip()

        # Validate inputs
        if not member_name or not trainer_id_str or not booking_date or not booking_time or not duration_minutes_str:
            feedback = 'All fields are required.'
        else:
            try:
                trainer_id = int(trainer_id_str)
                duration_minutes = int(duration_minutes_str)
            except ValueError:
                feedback = 'Invalid trainer ID or duration.'
            else:
                # Create a new booking ID
                bookings = load_bookings()
                max_id = max([b['booking_id'] for b in bookings], default=0)
                new_booking = {
                    'booking_id': max_id + 1,
                    'member_name': member_name,
                    'trainer_id': trainer_id,
                    'booking_date': booking_date,
                    'booking_time': booking_time,
                    'duration_minutes': duration_minutes,
                    'status': 'Pending',
                }
                success = save_booking(new_booking)
                if success:
                    feedback = 'Booking submitted successfully.'
                else:
                    feedback = 'Failed to save booking.'

    return render_template('booking.html', trainers=[{'trainer_id': t['trainer_id'], 'name': t['name']} for t in trainers], feedback=feedback)


@app.route('/workouts')
def workout_records():
    workouts = load_workouts()
    return render_template('workouts.html', workouts=workouts)


@app.route('/log-workout', methods=['GET', 'POST'])
def log_workout():
    feedback = None
    if request.method == 'POST':
        member_name = request.form.get('member_name', '').strip()  # Member name needed to log workout
        workout_type = request.form.get('workout_type', '').strip()
        workout_date = request.form.get('workout_date', '').strip()  # Should be a date string
        duration_minutes_str = request.form.get('duration_minutes', '').strip()
        calories_burned_str = request.form.get('calories_burned', '').strip()
        notes = request.form.get('notes', '').strip()

        if not member_name or not workout_type or not workout_date or not duration_minutes_str or not calories_burned_str:
            feedback = 'All fields are required.'
        else:
            try:
                duration_minutes = int(duration_minutes_str)
                calories_burned = int(calories_burned_str)
            except ValueError:
                feedback = 'Duration and calories burned must be numbers.'
            else:
                workouts = load_workouts()
                max_id = max([w['workout_id'] for w in workouts], default=0)
                new_workout = {
                    'workout_id': max_id + 1,
                    'member_name': member_name,
                    'workout_type': workout_type,
                    'workout_date': workout_date,
                    'duration_minutes': duration_minutes,
                    'calories_burned': calories_burned,
                    'notes': notes
                }
                success = save_workout(new_workout)
                if success:
                    feedback = 'Workout logged successfully.'
                else:
                    feedback = 'Failed to log workout.'

    return render_template('log_workout.html', feedback=feedback)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
