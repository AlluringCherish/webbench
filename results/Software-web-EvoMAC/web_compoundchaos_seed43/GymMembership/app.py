'''
Backend implementation for the GymMembership web application.
Provides routing and data handling for all pages as specified.
Data is stored and read from local text files in the 'data' directory.
The app runs on local port 5000 and starts from the Dashboard page at '/'.
'''
from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime
app = Flask(__name__)
DATA_DIR = 'data'
# Utility functions to read data files
def read_memberships():
    memberships = []
    path = os.path.join(DATA_DIR, 'memberships.txt')
    if not os.path.exists(path):
        return memberships
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 6:
                continue
            membership_id, plan_name, price, billing_cycle, features, max_classes = parts
            memberships.append({
                'membership_id': membership_id,
                'plan_name': plan_name,
                'price': price,
                'billing_cycle': billing_cycle,
                'features': features,
                'max_classes': max_classes
            })
    return memberships
def read_classes():
    classes = []
    path = os.path.join(DATA_DIR, 'classes.txt')
    if not os.path.exists(path):
        return classes
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 8:
                continue
            class_id, class_name, trainer_id, class_type, schedule_day, schedule_time, capacity, duration = parts
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
    return classes
def read_trainers():
    trainers = []
    path = os.path.join(DATA_DIR, 'trainers.txt')
    if not os.path.exists(path):
        return trainers
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 6:
                continue
            trainer_id, name, specialty, certifications, experience_years, bio = parts
            trainers.append({
                'trainer_id': trainer_id,
                'name': name,
                'specialty': specialty,
                'certifications': certifications,
                'experience_years': experience_years,
                'bio': bio
            })
    return trainers
def read_bookings():
    bookings = []
    path = os.path.join(DATA_DIR, 'bookings.txt')
    if not os.path.exists(path):
        return bookings
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 7:
                continue
            booking_id, member_name, trainer_id, booking_date, booking_time, duration_minutes, status = parts
            bookings.append({
                'booking_id': booking_id,
                'member_name': member_name,
                'trainer_id': trainer_id,
                'booking_date': booking_date,
                'booking_time': booking_time,
                'duration_minutes': duration_minutes,
                'status': status
            })
    return bookings
def read_workouts():
    workouts = []
    path = os.path.join(DATA_DIR, 'workouts.txt')
    if not os.path.exists(path):
        return workouts
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 7:
                continue
            workout_id, member_name, workout_type, workout_date, duration_minutes, calories_burned, notes = parts
            workouts.append({
                'workout_id': workout_id,
                'member_name': member_name,
                'workout_type': workout_type,
                'workout_date': workout_date,
                'duration_minutes': duration_minutes,
                'calories_burned': calories_burned,
                'notes': notes
            })
    return workouts
def write_booking(booking):
    path = os.path.join(DATA_DIR, 'bookings.txt')
    bookings = read_bookings()
    max_id = 0
    for b in bookings:
        try:
            bid = int(b['booking_id'])
            if bid > max_id:
                max_id = bid
        except:
            continue
    new_id = max_id + 1
    line = f"{new_id}|{booking['member_name']}|{booking['trainer_id']}|{booking['booking_date']}|{booking['booking_time']}|{booking['duration_minutes']}|{booking['status']}\n"
    with open(path, 'a', encoding='utf-8') as f:
        f.write(line)
    return new_id
def write_workout(workout):
    path = os.path.join(DATA_DIR, 'workouts.txt')
    workouts = read_workouts()
    max_id = 0
    for w in workouts:
        try:
            wid = int(w['workout_id'])
            if wid > max_id:
                max_id = wid
        except:
            continue
    new_id = max_id + 1
    line = f"{new_id}|{workout['member_name']}|{workout['workout_type']}|{workout['workout_date']}|{workout['duration_minutes']}|{workout['calories_burned']}|{workout['notes']}\n"
    with open(path, 'a', encoding='utf-8') as f:
        f.write(line)
    return new_id
# Dummy member name for all operations (no authentication)
DEFAULT_MEMBER_NAME = "Guest User"
# Routes
@app.route('/')
def dashboard():
    # For member highlights and featured classes, we can show some sample data
    memberships = read_memberships()
    classes = read_classes()
    trainers = read_trainers()
    # For simplicity, show first 3 classes as featured
    featured_classes = classes[:3]
    # Member status: no authentication, so just a welcome message
    member_status = "Welcome, Guest User! Explore our gym membership options and classes."
    return render_template('dashboard.html',
                           member_status=member_status,
                           featured_classes=featured_classes,
                           memberships=memberships,
                           trainers=trainers)
@app.route('/memberships')
def membership_plans():
    memberships = read_memberships()
    filter_type = request.args.get('filter', None)
    if filter_type:
        memberships = [m for m in memberships if m['plan_name'].lower() == filter_type.lower()]
    return render_template('membership_plans.html', memberships=memberships, filter_type=filter_type)
@app.route('/plan/<plan_id>')
def plan_details(plan_id):
    memberships = read_memberships()
    plan = next((m for m in memberships if m['membership_id'] == plan_id), None)
    if not plan:
        return "Plan not found", 404
    # No reviews data file specified, so show empty reviews section
    plan_reviews = []
    return render_template('plan_details.html', plan=plan, plan_reviews=plan_reviews)
@app.route('/classes')
def class_schedule():
    classes = read_classes()
    trainers = read_trainers()
    # Search and filter
    search_query = request.args.get('search', '').strip().lower()
    filter_type = request.args.get('filter', '').strip().lower()
    filtered_classes = classes
    if search_query:
        filtered_classes = [c for c in filtered_classes if search_query in c['class_name'].lower() or
                            any(t['trainer_id'] == c['trainer_id'] and search_query in t['name'].lower() for t in trainers)]
    if filter_type:
        filtered_classes = [c for c in filtered_classes if c['class_type'].lower() == filter_type]
    # Map trainer names for display
    trainer_dict = {t['trainer_id']: t['name'] for t in trainers}
    return render_template('class_schedule.html', classes=filtered_classes, trainer_dict=trainer_dict,
                           search_query=search_query, filter_type=filter_type)
@app.route('/trainers')
def trainer_profiles():
    trainers = read_trainers()
    search_query = request.args.get('search', '').strip().lower()
    filter_specialty = request.args.get('filter', '').strip().lower()
    filtered_trainers = trainers
    if search_query:
        filtered_trainers = [t for t in filtered_trainers if search_query in t['name'].lower() or search_query in t['specialty'].lower()]
    if filter_specialty:
        filtered_trainers = [t for t in filtered_trainers if filter_specialty in t['specialty'].lower()]
    return render_template('trainer_profiles.html', trainers=filtered_trainers,
                           search_query=search_query, filter_specialty=filter_specialty)
@app.route('/trainer/<trainer_id>')
def trainer_detail(trainer_id):
    trainers = read_trainers()
    trainer = next((t for t in trainers if t['trainer_id'] == trainer_id), None)
    if not trainer:
        return "Trainer not found", 404
    # No reviews data file specified, so show empty reviews section
    trainer_reviews = []
    return render_template('trainer_detail.html', trainer=trainer, trainer_reviews=trainer_reviews)
@app.route('/booking', methods=['GET', 'POST'])
def pt_booking():
    trainers = read_trainers()
    if request.method == 'POST':
        # Get form data
        member_name = DEFAULT_MEMBER_NAME
        trainer_id = request.form.get('select-trainer')
        session_date = request.form.get('session-date')
        session_time = request.form.get('session-time')
        session_duration = request.form.get('session-duration')
        if not (trainer_id and session_date and session_time and session_duration):
            error = "All fields are required."
            return render_template('pt_booking.html', trainers=trainers, error=error)
        # Validate date format
        try:
            datetime.strptime(session_date, '%Y-%m-%d')
        except ValueError:
            error = "Invalid date format."
            return render_template('pt_booking.html', trainers=trainers, error=error)
        # Save booking with status Pending
        booking = {
            'member_name': member_name,
            'trainer_id': trainer_id,
            'booking_date': session_date,
            'booking_time': session_time,
            'duration_minutes': session_duration,
            'status': 'Pending'
        }
        write_booking(booking)
        return redirect(url_for('dashboard'))
    else:
        # GET request
        return render_template('pt_booking.html', trainers=trainers)
@app.route('/workouts')
def workout_records():
    workouts = read_workouts()
    filter_type = request.args.get('filter', '').strip().lower()
    # Filter by member name (default guest user)
    member_name = DEFAULT_MEMBER_NAME
    filtered_workouts = [w for w in workouts if w['member_name'] == member_name]
    if filter_type:
        filtered_workouts = [w for w in filtered_workouts if w['workout_type'].lower() == filter_type]
    return render_template('workout_records.html', workouts=filtered_workouts, filter_type=filter_type)
@app.route('/log_workout', methods=['GET', 'POST'])
def log_workout():
    if request.method == 'POST':
        workout_type = request.form.get('workout-type')
        workout_duration = request.form.get('workout-duration')
        calories_burned = request.form.get('calories-burned')
        workout_notes = request.form.get('workout-notes', '').strip()
        member_name = DEFAULT_MEMBER_NAME
        if not (workout_type and workout_duration and calories_burned):
            error = "Workout type, duration, and calories burned are required."
            return render_template('log_workout.html', error=error)
        # Validate numeric inputs
        try:
            workout_duration_int = int(workout_duration)
            calories_burned_int = int(calories_burned)
        except ValueError:
            error = "Duration and calories burned must be numbers."
            return render_template('log_workout.html', error=error)
        workout_date = datetime.now().strftime('%Y-%m-%d')
        workout = {
            'member_name': member_name,
            'workout_type': workout_type,
            'workout_date': workout_date,
            'duration_minutes': str(workout_duration_int),
            'calories_burned': str(calories_burned_int),
            'notes': workout_notes
        }
        write_workout(workout)
        return redirect(url_for('workout_records'))
    else:
        return render_template('log_workout.html')
if __name__ == '__main__':
    # Ensure data directory exists
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    app.run(host='0.0.0.0', port=5000, debug=True)