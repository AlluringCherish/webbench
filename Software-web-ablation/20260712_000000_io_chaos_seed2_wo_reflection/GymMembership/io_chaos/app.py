from flask import Flask, render_template, redirect, url_for, request
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Helper functions to load data

def load_memberships():
    filepath = os.path.join(DATA_DIR, 'memberships.txt')
    memberships = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 6:
                    membership = {
                        'membership_id': int(parts[0]),
                        'plan_name': parts[1],
                        'price': parts[2],  # keep as str
                        'billing_cycle': parts[3],
                        'features': parts[4],
                        'max_classes': parts[5]
                    }
                    memberships.append(membership)
    except Exception as e:
        memberships = []
    return memberships


def load_classes():
    filepath = os.path.join(DATA_DIR, 'classes.txt')
    classes = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 8:
                    class_item = {
                        'class_id': int(parts[0]),
                        'class_name': parts[1],
                        'trainer_id': int(parts[2]),
                        'class_type': parts[3],
                        'schedule_day': parts[4],
                        'schedule_time': parts[5],
                        'capacity': int(parts[6]),
                        'duration': int(parts[7])
                    }
                    classes.append(class_item)
    except Exception as e:
        classes = []
    return classes


def load_trainers():
    filepath = os.path.join(DATA_DIR, 'trainers.txt')
    trainers = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 6:
                    trainer = {
                        'trainer_id': int(parts[0]),
                        'name': parts[1],
                        'specialty': parts[2],
                        'certifications': parts[3],
                        'experience_years': int(parts[4]),
                        'bio': parts[5]
                    }
                    trainers.append(trainer)
    except Exception as e:
        trainers = []
    return trainers


def load_bookings():
    filepath = os.path.join(DATA_DIR, 'bookings.txt')
    bookings = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
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
                        'status': parts[6]
                    }
                    bookings.append(booking)
    except Exception as e:
        bookings = []
    return bookings


def load_workouts():
    filepath = os.path.join(DATA_DIR, 'workouts.txt')
    workouts = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
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
                        'notes': parts[6]
                    }
                    workouts.append(workout)
    except Exception as e:
        workouts = []
    return workouts


def save_booking(new_booking):
    filepath = os.path.join(DATA_DIR, 'bookings.txt')
    try:
        # Determine next booking_id
        bookings = load_bookings()
        next_id = max([b['booking_id'] for b in bookings], default=0) + 1
        line = f"{next_id}|{new_booking['member_name']}|{new_booking['trainer_id']}|{new_booking['booking_date']}|{new_booking['booking_time']}|{new_booking['duration_minutes']}|Confirmed\n"
        with open(filepath, 'a', encoding='utf-8') as f:
            f.write(line)
        return True
    except Exception as e:
        return False


def save_workout(new_workout):
    filepath = os.path.join(DATA_DIR, 'workouts.txt')
    try:
        workouts = load_workouts()
        next_id = max([w['workout_id'] for w in workouts], default=0) + 1
        line = f"{next_id}|{new_workout['member_name']}|{new_workout['workout_type']}|{new_workout['workout_date']}|{new_workout['duration_minutes']}|{new_workout['calories_burned']}|{new_workout['notes']}\n"
        with open(filepath, 'a', encoding='utf-8') as f:
            f.write(line)
        return True
    except Exception as e:
        return False


# Route Definitions

@app.route('/')
def root():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    # For demo, member_status hardcoded
    member_status = "Welcome to Gym! Enjoy your membership."

    # Featured classes could be first 3 from classes
    classes = load_classes()
    featured_classes = classes[:3] if classes else []

    navigation_routes = {
        'memberships': url_for('memberships'),
        'schedule': url_for('class_schedule'),
        'booking': url_for('pt_booking')
    }

    return render_template('dashboard.html', member_status=member_status, featured_classes=featured_classes, navigation_routes=navigation_routes)


@app.route('/memberships')
def memberships():
    plans = load_memberships()
    # Extract unique membership types from plans' plan_name or features? Spec says membership_types e.g. Basic, Premium, Elite
    membership_types = sorted(set(plan['plan_name'] for plan in plans))
    return render_template('memberships.html', plans=plans, membership_types=membership_types)


@app.route('/plan/<int:plan_id>')
def plan_details(plan_id):
    plans = load_memberships()
    plan = next((p for p in plans if p['membership_id'] == plan_id), None)
    # Reviews not defined in spec explicitly; pass empty list
    reviews = []
    return render_template('plan_details.html', plan=plan, reviews=reviews)


@app.route('/schedule')
def class_schedule():
    classes = load_classes()
    class_types = sorted(set(c['class_type'] for c in classes)) if classes else []
    return render_template('schedule.html', classes=classes, class_types=class_types)


@app.route('/trainers')
def trainers():
    trainers_list = load_trainers()
    specialties = sorted(set(t['specialty'] for t in trainers_list)) if trainers_list else []
    return render_template('trainers.html', trainers=trainers_list, specialties=specialties)


@app.route('/trainer/<int:trainer_id>')
def trainer_detail(trainer_id):
    trainers_list = load_trainers()
    trainer = next((t for t in trainers_list if t['trainer_id'] == trainer_id), None)
    reviews = []  # No reviews data defined
    return render_template('trainer_detail.html', trainer=trainer, reviews=reviews)


@app.route('/booking', methods=['GET', 'POST'])
def pt_booking():
    trainers_list = load_trainers()
    available_times = [
        '06:00', '07:00', '08:00', '09:00', '10:00', '11:00',
        '12:00', '13:00', '14:00', '15:00', '16:00', '17:00',
        '18:00', '19:00', '20:00'
    ]
    durations = [30, 60, 90]

    if request.method == 'POST':
        try:
            trainer_id = int(request.form['trainer_id'])
            session_date = request.form['session_date']
            session_time = request.form['session_time']
            session_duration = int(request.form['session_duration'])
            # member_name may be hardcoded as no user system
            member_name = "Guest"

            new_booking = {
                'member_name': member_name,
                'trainer_id': trainer_id,
                'booking_date': session_date,
                'booking_time': session_time,
                'duration_minutes': session_duration
            }
            saved = save_booking(new_booking)
            if saved:
                return redirect(url_for('dashboard'))
            else:
                # fallback: reload booking form with error
                return render_template('booking.html', trainers=trainers_list, available_times=available_times, durations=durations, error="Failed to save booking.")
        except Exception:
            return render_template('booking.html', trainers=trainers_list, available_times=available_times, durations=durations, error="Invalid form data.")
    else:
        return render_template('booking.html', trainers=trainers_list, available_times=available_times, durations=durations)


@app.route('/workouts')
def workout_records():
    workouts = load_workouts()
    workout_types = sorted(set(w['workout_type'] for w in workouts)) if workouts else []
    return render_template('workouts.html', workouts=workouts, workout_types=workout_types)


@app.route('/log_workout', methods=['GET', 'POST'])
def log_workout():
    workout_types = sorted(set(w['workout_type'] for w in load_workouts()))

    if request.method == 'POST':
        try:
            workout_type = request.form['workout_type']
            workout_duration = int(request.form['workout_duration'])
            calories_burned = int(request.form['calories_burned'])
            workout_notes = request.form['workout_notes']
            # member_name hardcoded
            member_name = "Guest"
            from datetime import datetime
            workout_date = datetime.now().strftime('%Y-%m-%d')
            new_workout = {
                'member_name': member_name,
                'workout_type': workout_type,
                'workout_date': workout_date,
                'duration_minutes': workout_duration,
                'calories_burned': calories_burned,
                'notes': workout_notes
            }
            saved = save_workout(new_workout)
            if saved:
                return redirect(url_for('workout_records'))
            else:
                return render_template('log_workout.html', workout_types=workout_types, error="Failed to save workout.")
        except Exception:
            return render_template('log_workout.html', workout_types=workout_types, error="Invalid form data.")
    else:
        return render_template('log_workout.html', workout_types=workout_types)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
