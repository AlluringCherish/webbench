from flask import Flask, render_template, redirect, url_for, request
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Helper functions to load memberships from memberships.txt

def load_memberships():
    memberships = []
    path = os.path.join(DATA_DIR, 'memberships.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 6:
                    membership_id = int(parts[0])
                    plan_name = parts[1]
                    price = float(parts[2])
                    billing_cycle = parts[3]
                    features = parts[4].split(', ')
                    max_classes_raw = parts[5]
                    max_classes = int(max_classes_raw) if max_classes_raw.isdigit() else max_classes_raw
                    memberships.append({
                        'membership_id': membership_id,
                        'plan_name': plan_name,
                        'price': price,
                        'billing_cycle': billing_cycle,
                        'features': features,
                        'max_classes': max_classes
                    })
    except FileNotFoundError:
        # File missing means empty list
        pass
    return memberships

# Load classes from classes.txt
 def load_classes():
    classes = []
    path = os.path.join(DATA_DIR, 'classes.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
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
        pass
    return classes

# Load trainers from trainers.txt

def load_trainers():
    trainers = []
    path = os.path.join(DATA_DIR, 'trainers.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 6:
                    trainer_id = int(parts[0])
                    name = parts[1]
                    specialty = parts[2]
                    certifications = parts[3].split(', ')
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
        pass
    return trainers

# Load bookings from bookings.txt

def load_bookings():
    bookings = []
    path = os.path.join(DATA_DIR, 'bookings.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
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
        pass
    return bookings

# Save a booking to bookings.txt

def save_booking(booking):
    bookings = load_bookings()
    max_id = max([b['booking_id'] for b in bookings], default=0)
    new_id = max_id + 1
    path = os.path.join(DATA_DIR, 'bookings.txt')
    try:
        with open(path, 'a', encoding='utf-8') as f:
            line = f"{new_id}|{booking['member_name']}|{booking['trainer_id']}|{booking['booking_date']}|{booking['booking_time']}|{booking['duration_minutes']}|{booking['status']}\n"
            f.write(line)
            return new_id
    except Exception:
        return None

# Load workouts from workouts.txt

def load_workouts():
    workouts = []
    path = os.path.join(DATA_DIR, 'workouts.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
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
        pass
    return workouts

# Save workout to workouts.txt

def save_workout(workout):
    workouts = load_workouts()
    max_id = max([w['workout_id'] for w in workouts], default=0)
    new_id = max_id + 1
    path = os.path.join(DATA_DIR, 'workouts.txt')
    try:
        with open(path, 'a', encoding='utf-8') as f:
            line = f"{new_id}|{workout['member_name']}|{workout['workout_type']}|{workout['workout_date']}|{workout['duration_minutes']}|{workout['calories_burned']}|{workout['notes']}\n"
            f.write(line)
            return new_id
    except Exception:
        return None

# Root route redirects to dashboard
@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))

# Dashboard page
@app.route('/dashboard', methods=['GET'])
def dashboard():
    member_status = "Welcome to Gym Membership Dashboard!"
    memberships = load_memberships()
    membership_plans = [
        { 'membership_id': m['membership_id'], 'plan_name': m['plan_name'], 'price': m['price'], 'billing_cycle': m['billing_cycle'] }
        for m in memberships
    ]
    featured_classes = load_classes()[:3]
    trainers = load_trainers()[:4]
    return render_template('dashboard.html', member_status=member_status, membership_plans=membership_plans, featured_classes=featured_classes, trainers=trainers)

# Membership plans page
@app.route('/memberships', methods=['GET'])
def membership_plans_page():
    membership_plans = load_memberships()
    filter_types = sorted({mp['plan_name'] for mp in membership_plans})
    return render_template('memberships.html', membership_plans=membership_plans, filter_types=filter_types)

# Plan details page
@app.route('/plan/<int:plan_id>', methods=['GET'])
def plan_details_page(plan_id):
    membership_plans = load_memberships()
    plan = next((p for p in membership_plans if p['membership_id'] == plan_id), None)
    reviews = []  # No review data source specified
    return render_template('plan_details.html', plan=plan, reviews=reviews)

# Class schedule page
@app.route('/schedule', methods=['GET'])
def class_schedule_page():
    classes = load_classes()
    class_types = sorted({c['class_type'] for c in classes})
    search_query = request.args.get('search_query', '')
    return render_template('schedule.html', classes=classes, class_types=class_types, search_query=search_query)

# Trainer profiles page
@app.route('/trainers', methods=['GET'])
def trainers_page():
    trainers = load_trainers()
    specialties = sorted({t['specialty'] for t in trainers})
    search_query = request.args.get('search_query', '')
    return render_template('trainers.html', trainers=trainers, specialties=specialties, search_query=search_query)

# Trainer detail page
@app.route('/trainer/<int:trainer_id>', methods=['GET'])
def trainer_detail_page(trainer_id):
    trainers = load_trainers()
    trainer = next((t for t in trainers if t['trainer_id'] == trainer_id), None)
    reviews = []  # No review data source specified
    return render_template('trainer_detail.html', trainer=trainer, reviews=reviews)

# PT booking page
@app.route('/booking', methods=['GET', 'POST'])
def pt_booking_page():
    trainers = load_trainers()
    available_times = [
        "06:00", "07:00", "08:00", "09:00", "10:00", "11:00", "12:00",
        "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00"
    ]
    session_durations = [30, 60, 90]

    if request.method == 'POST':
        member_name = request.form.get('member_name', '').strip()
        trainer_id = request.form.get('trainer_id', type=int)
        booking_date = request.form.get('booking_date', '').strip()
        booking_time = request.form.get('booking_time', '').strip()
        duration_minutes = request.form.get('duration_minutes', type=int)

        if member_name and trainer_id and booking_date and booking_time and duration_minutes:
            booking = {
                'member_name': member_name,
                'trainer_id': trainer_id,
                'booking_date': booking_date,
                'booking_time': booking_time,
                'duration_minutes': duration_minutes,
                'status': 'Pending'
            }
            save_booking(booking)
            return redirect(url_for('pt_booking_page'))

    return render_template('booking.html', trainers=trainers, available_times=available_times, session_durations=session_durations)

# Workout records page
@app.route('/workouts', methods=['GET'])
def workout_records_page():
    workouts = load_workouts()
    workout_types = sorted({w['workout_type'] for w in workouts})
    return render_template('workouts.html', workouts=workouts, workout_types=workout_types)

# Log workout page
@app.route('/log-workout', methods=['GET', 'POST'])
def log_workout_page():
    workout_types = ["Cardio", "Strength", "Class", "Flexibility", "Balance"]
    if request.method == 'POST':
        member_name = request.form.get('member_name', '').strip()
        workout_type = request.form.get('workout_type', '').strip()
        workout_date = request.form.get('workout_date', '').strip()
        duration_minutes = request.form.get('duration_minutes', type=int)
        calories_burned = request.form.get('calories_burned', type=int)
        notes = request.form.get('notes', '').strip()

        if member_name and workout_type and workout_date and duration_minutes is not None and calories_burned is not None:
            workout = {
                'member_name': member_name,
                'workout_type': workout_type,
                'workout_date': workout_date,
                'duration_minutes': duration_minutes,
                'calories_burned': calories_burned,
                'notes': notes
            }
            save_workout(workout)
            return redirect(url_for('workout_records_page'))

    return render_template('log_workout.html', workout_types=workout_types)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
