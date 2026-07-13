from flask import Flask, render_template, request, redirect, url_for
import os
import datetime

app = Flask(__name__)

# Constants
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
MEMBER_NAME = "John Doe"  # Simulated member name for usage in bookings and workouts

# Utility functions to read and write data files

def read_memberships():
    memberships = []
    path = os.path.join(DATA_DIR, 'memberships.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) == 6:
                    memberships.append({
                        'membership_id': int(parts[0]),
                        'plan_name': parts[1],
                        'price': parts[2],
                        'billing_cycle': parts[3],
                        'features': parts[4],
                        'max_classes': parts[5]
                    })
    return memberships

def read_classes():
    classes = []
    path = os.path.join(DATA_DIR, 'classes.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) == 8:
                    classes.append({
                        'class_id': int(parts[0]),
                        'class_name': parts[1],
                        'trainer_id': int(parts[2]),
                        'class_type': parts[3],
                        'schedule_day': parts[4],
                        'schedule_time': parts[5],
                        'capacity': int(parts[6]),
                        'duration': int(parts[7])
                    })
    return classes

def read_trainers():
    trainers = []
    path = os.path.join(DATA_DIR, 'trainers.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) == 6:
                    trainers.append({
                        'trainer_id': int(parts[0]),
                        'name': parts[1],
                        'specialty': parts[2],
                        'certifications': parts[3],
                        'experience_years': int(parts[4]),
                        'bio': parts[5]
                    })
    return trainers

def read_bookings():
    bookings = []
    path = os.path.join(DATA_DIR, 'bookings.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) == 7:
                    bookings.append({
                        'booking_id': int(parts[0]),
                        'member_name': parts[1],
                        'trainer_id': int(parts[2]),
                        'booking_date': parts[3],
                        'booking_time': parts[4],
                        'duration_minutes': int(parts[5]),
                        'status': parts[6]
                    })
    return bookings

def write_booking(new_booking):
    bookings = read_bookings()
    max_id = max([b['booking_id'] for b in bookings], default=0)
    new_id = max_id + 1
    new_booking_line = f"{new_id}|{new_booking['member_name']}|{new_booking['trainer_id']}|{new_booking['booking_date']}|{new_booking['booking_time']}|{new_booking['duration_minutes']}|Confirmed"
    path = os.path.join(DATA_DIR, 'bookings.txt')
    with open(path, 'a', encoding='utf-8') as f:
        f.write(new_booking_line + "\n")

def read_workouts():
    workouts = []
    path = os.path.join(DATA_DIR, 'workouts.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) == 7:
                    workouts.append({
                        'workout_id': int(parts[0]),
                        'member_name': parts[1],
                        'workout_type': parts[2],
                        'workout_date': parts[3],
                        'duration_minutes': int(parts[4]),
                        'calories_burned': int(parts[5]),
                        'notes': parts[6]
                    })
    return workouts

def write_workout(new_workout):
    workouts = read_workouts()
    max_id = max([w['workout_id'] for w in workouts], default=0)
    new_id = max_id + 1
    line = f"{new_id}|{new_workout['member_name']}|{new_workout['workout_type']}|{new_workout['workout_date']}|{new_workout['duration_minutes']}|{new_workout['calories_burned']}|{new_workout['notes']}"
    path = os.path.join(DATA_DIR, 'workouts.txt')
    with open(path, 'a', encoding='utf-8') as f:
        f.write(line + "\n")

# Helper functions

def get_trainer_by_id(trainer_id):
    trainers = read_trainers()
    for t in trainers:
        if t['trainer_id'] == trainer_id:
            return t
    return None

def get_membership_by_id(plan_id):
    memberships = read_memberships()
    for m in memberships:
        if m['membership_id'] == plan_id:
            return m
    return None

def get_class_by_id(class_id):
    classes = read_classes()
    for c in classes:
        if c['class_id'] == class_id:
            return c
    return None

# ROUTES

@app.route('/')
@app.route('/dashboard')
def dashboard():
    member_status = f"Welcome, {MEMBER_NAME}! You're a valued member."
    return render_template('dashboard.html', member_status=member_status, member_name=MEMBER_NAME)

@app.route('/memberships')
def membership_plans():
    memberships = read_memberships()
    plan_types = sorted(set(m['plan_name'] for m in memberships))
    filter_type = request.args.get('filter')
    if filter_type:
        memberships = [m for m in memberships if m['plan_name'] == filter_type]
    return render_template('memberships.html', memberships=memberships, plan_types=plan_types, selected_filter=filter_type)

@app.route('/memberships/<int:plan_id>')
def plan_details(plan_id):
    plan = get_membership_by_id(plan_id)
    if plan is None:
        return "Plan not found", 404
    # Combined static reviews
    reviews = [
        "Great value for the price!",
        "I love the flexibility of this plan.",
        "Customer service is excellent.",
        "Great value plan!",
        "Helps me stay fit and motivated.",
        "Perfect for my busy schedule."
    ]
    return render_template('plan_details.html', plan=plan, reviews=reviews)

@app.route('/schedule')
def class_schedule():
    search = request.args.get('search', '').lower()
    filter_type = request.args.get('filter')
    classes = read_classes()
    trainers_list = read_trainers()
    trainers = {t['trainer_id']: t for t in trainers_list}

    def class_matches(c):
        if search:
            by_name = search in c['class_name'].lower()
            trainer_name = trainers.get(c['trainer_id'], {}).get('name', '').lower()
            by_trainer = search in trainer_name
            if not (by_name or by_trainer):
                return False
        if filter_type and filter_type != 'All':
            if c['class_type'] != filter_type:
                return False
        return True

    filtered_classes = [c for c in classes if class_matches(c)]

    class_types = sorted(set(c['class_type'] for c in classes))
    return render_template('schedule.html', classes=filtered_classes, class_types=class_types, selected_filter=filter_type or 'All', search_term=search, trainers=trainers)

@app.route('/trainers')
def trainer_profiles():
    search = request.args.get('search', '').lower()
    filter_specialty = request.args.get('filter')
    trainers = read_trainers()

    def trainer_matches(t):
        if search:
            by_name = search in t['name'].lower()
            by_specialty = search in t['specialty'].lower()
            if not (by_name or by_specialty):
                return False
        if filter_specialty and filter_specialty != 'All':
            if filter_specialty not in t['specialty']:
                return False
        return True

    filtered_trainers = [t for t in trainers if trainer_matches(t)]

    specialty_options = sorted(set(s for t in trainers for s in t['specialty'].split(', ')))
    return render_template('trainers.html', trainers=filtered_trainers, specialty_options=specialty_options, selected_filter=filter_specialty or 'All', search_term=search)

@app.route('/trainers/<int:trainer_id>')
def trainer_detail(trainer_id):
    trainer = get_trainer_by_id(trainer_id)
    if not trainer:
        return "Trainer not found", 404
    reviews = [
        "Very knowledgeable and motivating.",
        "Helped me achieve my fitness goals.",
        "Highly recommend for personalized plans.",
        "Very knowledgeable and supportive.",
        "Helped me achieve my fitness goals.",
        "Great training sessions and tips."
    ]
    return render_template('trainer_detail.html', trainer=trainer, reviews=reviews)

@app.route('/book-training', methods=['GET', 'POST'])
def pt_booking():
    trainers = read_trainers()
    preselect_trainer_id = request.args.get('trainer_id', type=int)

    if request.method == 'POST':
        selected_trainer = request.form.get('select-trainer', type=int)
        session_date = request.form.get('session-date')
        session_time = request.form.get('session-time')
        session_duration = request.form.get('session-duration', type=int)

        if not (selected_trainer and session_date and session_time and session_duration):
            error = "Please fill in all fields."
            return render_template('booking.html', trainers=trainers, error=error, preselect_trainer_id=preselect_trainer_id)

        # Validate date format
        try:
            datetime.datetime.strptime(session_date, '%Y-%m-%d')
        except ValueError:
            error = "Invalid date format."
            return render_template('booking.html', trainers=trainers, error=error, preselect_trainer_id=preselect_trainer_id)

        # Save booking
        new_booking = {
            'member_name': MEMBER_NAME,
            'trainer_id': selected_trainer,
            'booking_date': session_date,
            'booking_time': session_time,
            'duration_minutes': session_duration
        }
        write_booking(new_booking)
        return redirect(url_for('pt_booking') + '?success=1')

    time_slots = ['06:00', '07:00', '08:00', '09:00', '10:00', '11:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00']
    durations = [30, 60, 90]
    success = request.args.get('success') == '1'

    return render_template('booking.html', trainers=trainers, time_slots=time_slots, durations=durations, success=success, preselect_trainer_id=preselect_trainer_id)

@app.route('/workouts')
def workout_records():
    workouts = read_workouts()
    filter_type = request.args.get('filter')
    if filter_type:
        workouts = [w for w in workouts if w['workout_type'] == filter_type]
    workouts = sorted(workouts, key=lambda w: w['workout_date'], reverse=True)
    workout_types = ['Class', 'PT Session', 'Personal']
    return render_template('workouts.html', workouts=workouts, workout_types=workout_types, selected_filter=filter_type)

@app.route('/log-workout', methods=['GET', 'POST'])
def log_workout():
    error = None
    if request.method == 'POST':
        workout_type = request.form.get('workout-type')
        duration = request.form.get('workout-duration')
        calories = request.form.get('calories-burned')
        notes = request.form.get('workout-notes', '').replace('|','-')

        if not (workout_type and duration and calories):
            error = "Please fill all required fields."
        else:
            try:
                duration = int(duration)
                calories = int(calories)
            except Exception:
                error = "Duration and calories must be numbers."

        if not error:
            new_workout = {
                'member_name': MEMBER_NAME,
                'workout_type': workout_type,
                'workout_date': datetime.datetime.now().strftime('%Y-%m-%d'),
                'duration_minutes': duration,
                'calories_burned': calories,
                'notes': notes
            }
            write_workout(new_workout)
            return redirect(url_for('workout_records'))

    return render_template('log_workout.html', error=error)


if __name__ == '__main__':
    app.run(debug=True)
