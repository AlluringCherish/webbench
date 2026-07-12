from flask import Flask, render_template, redirect, url_for, request
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Utility functions to load data from text files

def load_memberships():
    memberships = []
    try:
        with open(os.path.join(DATA_DIR, 'memberships.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 6:
                    membership = {
                        'membership_id': int(parts[0]),
                        'plan_name': parts[1],
                        'price': parts[2],
                        'billing_cycle': parts[3],
                        'features': parts[4],
                        'max_classes': parts[5],
                    }
                    memberships.append(membership)
    except Exception as e:
        print(f"Error loading memberships: {e}")
    return memberships


def load_classes():
    classes = []
    try:
        with open(os.path.join(DATA_DIR, 'classes.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 8:
                    class_entry = {
                        'class_id': int(parts[0]),
                        'class_name': parts[1],
                        'trainer_id': int(parts[2]),
                        'class_type': parts[3],
                        'schedule_day': parts[4],
                        'schedule_time': parts[5],
                        'capacity': int(parts[6]),
                        'duration': int(parts[7]),
                    }
                    classes.append(class_entry)
    except Exception as e:
        print(f"Error loading classes: {e}")
    return classes


def load_trainers():
    trainers = []
    try:
        with open(os.path.join(DATA_DIR, 'trainers.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 6:
                    trainer = {
                        'trainer_id': int(parts[0]),
                        'name': parts[1],
                        'specialty': parts[2],
                        'certifications': parts[3],
                        'experience_years': int(parts[4]),
                        'bio': parts[5],
                    }
                    trainers.append(trainer)
    except Exception as e:
        print(f"Error loading trainers: {e}")
    return trainers


def load_bookings():
    bookings = []
    try:
        with open(os.path.join(DATA_DIR, 'bookings.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 7:
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
    except Exception as e:
        print(f"Error loading bookings: {e}")
    return bookings


def save_booking(new_booking):
    try:
        booking_line = f"{new_booking['booking_id']}|{new_booking['member_name']}|{new_booking['trainer_id']}|{new_booking['booking_date']}|{new_booking['booking_time']}|{new_booking['duration_minutes']}|{new_booking['status']}\n"
        with open(os.path.join(DATA_DIR, 'bookings.txt'), 'a', encoding='utf-8') as f:
            f.write(booking_line)
        return True
    except Exception as e:
        print(f"Error saving booking: {e}")
        return False


def load_plan_reviews():
    # Since review format not specified, simulate empty or dummy data
    # Could be extended to read from 'data/plan_reviews.txt' (Not specified)
    return []


def load_trainer_reviews():
    # Since review format not specified, simulate empty or dummy data
    # Could be extended to read from 'data/trainer_reviews.txt' (Not specified)
    return []


def load_workouts():
    workouts = []
    try:
        with open(os.path.join(DATA_DIR, 'workouts.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 7:
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
    except Exception as e:
        print(f"Error loading workouts: {e}")
    return workouts


def save_workout(new_workout):
    try:
        workout_line = f"{new_workout['workout_id']}|{new_workout['member_name']}|{new_workout['workout_type']}|{new_workout['workout_date']}|{new_workout['duration_minutes']}|{new_workout['calories_burned']}|{new_workout['notes']}\n"
        with open(os.path.join(DATA_DIR, 'workouts.txt'), 'a', encoding='utf-8') as f:
            f.write(workout_line)
        return True
    except Exception as e:
        print(f"Error saving workout: {e}")
        return False


# Route implementations

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard_page'))


@app.route('/dashboard')
def dashboard_page():
    return render_template('dashboard.html')


@app.route('/memberships')
def memberships_page():
    memberships = load_memberships()
    return render_template('memberships.html', memberships=memberships)


@app.route('/plan/<int:plan_id>')
def plan_details_page(plan_id):
    memberships = load_memberships()
    plan = next((m for m in memberships if m['membership_id'] == plan_id), None)
    reviews = load_plan_reviews()  # no details provided, empty list
    if plan is None:
        return "Plan not found", 404
    return render_template('plan_details.html', plan=plan, reviews=reviews)


@app.route('/classes')
def class_schedule_page():
    classes = load_classes()
    # Derive filter_types from unique class_type values
    filter_types = sorted(set(c['class_type'] for c in classes))
    return render_template('class_schedule.html', classes=classes, filter_types=filter_types)


@app.route('/trainers')
def trainer_profiles_page():
    trainers = load_trainers()
    # Derive specialties from unique specialty fields
    specialties_set = set()
    for t in trainers:
        # Some trainers have specialties combined with '&', split by `&` and strip
        parts = [s.strip() for s in t['specialty'].split('&')]
        specialties_set.update(parts)
    specialties = sorted(specialties_set)
    return render_template('trainer_profiles.html', trainers=trainers, specialties=specialties)


@app.route('/trainer/<int:trainer_id>')
def trainer_detail_page(trainer_id):
    trainers = load_trainers()
    trainer = next((t for t in trainers if t['trainer_id'] == trainer_id), None)
    reviews = load_trainer_reviews()  # no details given, empty list
    if trainer is None:
        return "Trainer not found", 404
    return render_template('trainer_detail.html', trainer=trainer, reviews=reviews)


@app.route('/booking', methods=['GET', 'POST'])
def pt_booking_page():
    trainers = load_trainers()
    booking_status = None
    if request.method == 'POST':
        try:
            member_name = request.form.get('member_name', '').strip()
            trainer_id = int(request.form.get('trainer_id'))
            booking_date = request.form.get('booking_date', '').strip()
            booking_time = request.form.get('booking_time', '').strip()
            duration_minutes = int(request.form.get('duration_minutes'))

            # Generate new booking_id
            bookings = load_bookings()
            new_id = 1
            if bookings:
                new_id = max(b['booking_id'] for b in bookings) + 1

            new_booking = {
                'booking_id': new_id,
                'member_name': member_name,
                'trainer_id': trainer_id,
                'booking_date': booking_date,
                'booking_time': booking_time,
                'duration_minutes': duration_minutes,
                'status': 'Confirmed'
            }

            if save_booking(new_booking):
                booking_status = 'Booking successful!'
            else:
                booking_status = 'Failed to save booking.'
        except Exception as e:
            booking_status = f'Booking failed: {e}'

    return render_template('booking.html', trainers=trainers, booking_status=booking_status)


@app.route('/workouts')
def workout_records_page():
    workouts = load_workouts()
    # Derive workout_types from unique workout_type values
    workout_types = sorted(set(w['workout_type'] for w in workouts))
    return render_template('workouts.html', workouts=workouts, workout_types=workout_types)


@app.route('/logworkout', methods=['GET', 'POST'])
def log_workout_page():
    workout_log_status = None
    if request.method == 'POST':
        try:
            # Extract form data
            member_name = request.form.get('member_name', '').strip() or 'Anonymous'
            workout_type = request.form.get('workout_type', '').strip()
            workout_duration = int(request.form.get('workout_duration'))
            calories_burned = int(request.form.get('calories_burned'))
            workout_notes = request.form.get('workout_notes', '').strip()

            # Generate new workout_id
            workouts = load_workouts()
            new_id = 1
            if workouts:
                new_id = max(w['workout_id'] for w in workouts) + 1

            new_workout = {
                'workout_id': new_id,
                'member_name': member_name,
                'workout_type': workout_type,
                'workout_date': request.form.get('workout_date', '').strip() or '2025-01-01', # default date
                'duration_minutes': workout_duration,
                'calories_burned': calories_burned,
                'notes': workout_notes
            }

            if save_workout(new_workout):
                workout_log_status = 'Workout logged successfully!'
            else:
                workout_log_status = 'Failed to log workout.'
        except Exception as e:
            workout_log_status = f'Workout log failed: {e}'
    return render_template('log_workout.html', workout_log_status=workout_log_status)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
