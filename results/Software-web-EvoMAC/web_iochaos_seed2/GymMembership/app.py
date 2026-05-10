'''
Main backend application for GymMembership web app using Flask.
Handles routing, data reading/writing from/to local text files in the data/ directory,
and serves HTML templates for all nine pages.
No authentication required; all features directly accessible.
'''
from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime
app = Flask(__name__)
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
# Utility functions for reading and writing data files
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
                'price': float(price),
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
                'capacity': int(capacity),
                'duration': int(duration)
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
                'experience_years': int(experience_years),
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
                'duration_minutes': int(duration_minutes),
                'status': status
            })
    return bookings
def write_booking(new_booking):
    path = os.path.join(DATA_DIR, 'bookings.txt')
    # Determine next booking_id
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
    line = f"{new_id}|{new_booking['member_name']}|{new_booking['trainer_id']}|{new_booking['booking_date']}|{new_booking['booking_time']}|{new_booking['duration_minutes']}|{new_booking['status']}\n"
    with open(path, 'a', encoding='utf-8') as f:
        f.write(line)
    return new_id
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
                'duration_minutes': int(duration_minutes),
                'calories_burned': int(calories_burned),
                'notes': notes
            })
    return workouts
def write_workout(new_workout):
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
    line = f"{new_id}|{new_workout['member_name']}|{new_workout['workout_type']}|{new_workout['workout_date']}|{new_workout['duration_minutes']}|{new_workout['calories_burned']}|{new_workout['notes']}\n"
    with open(path, 'a', encoding='utf-8') as f:
        f.write(line)
    return new_id
# Helper to get trainer by id
def get_trainer_by_id(trainer_id):
    trainers = read_trainers()
    for t in trainers:
        if t['trainer_id'] == str(trainer_id):
            return t
    return None
# Helper to get membership plan by id
def get_membership_by_id(plan_id):
    memberships = read_memberships()
    for m in memberships:
        if m['membership_id'] == str(plan_id):
            return m
    return None
# Helper to get class by id
def get_class_by_id(class_id):
    classes = read_classes()
    for c in classes:
        if c['class_id'] == str(class_id):
            return c
    return None
# --- Routes ---
@app.route('/')
def dashboard():
    # For member highlights and featured classes, we can show some sample data
    memberships = read_memberships()
    classes = read_classes()
    trainers = read_trainers()
    # Featured classes: pick first 3 classes
    featured_classes = classes[:3]
    # Member welcome: since no auth, show generic welcome and highlight Basic plan as example
    member_status = "Welcome to GymMembership! Explore our plans and classes."
    return render_template('dashboard.html',
                           page_title="Gym Membership Dashboard",
                           member_status=member_status,
                           featured_classes=featured_classes,
                           memberships=memberships,
                           trainers=trainers)
@app.route('/membership-plans', methods=['GET'])
def membership_plans():
    memberships = read_memberships()
    filter_type = request.args.get('filter', None)
    if filter_type:
        memberships = [m for m in memberships if m['plan_name'].lower() == filter_type.lower()]
    return render_template('membership_plans.html',
                           page_title="Membership Plans",
                           memberships=memberships,
                           filter_type=filter_type)
@app.route('/plan-details/<plan_id>', methods=['GET'])
def plan_details(plan_id):
    plan = get_membership_by_id(plan_id)
    if not plan:
        return "Membership plan not found", 404
    # For plan reviews, since no data file specified, show empty or sample reviews
    # We'll show empty list for now
    plan_reviews = []
    return render_template('plan_details.html',
                           page_title="Plan Details",
                           plan=plan,
                           plan_reviews=plan_reviews)
@app.route('/class-schedule', methods=['GET'])
def class_schedule():
    classes = read_classes()
    trainers = read_trainers()
    # Get search and filter parameters
    search_query = request.args.get('search', '').strip().lower()
    filter_type = request.args.get('filter', '').strip().lower()
    # Filter classes by search (class name or trainer name)
    if search_query:
        filtered_classes = []
        for c in classes:
            trainer = get_trainer_by_id(c['trainer_id'])
            trainer_name = trainer['name'].lower() if trainer else ''
            if search_query in c['class_name'].lower() or search_query in trainer_name:
                filtered_classes.append(c)
        classes = filtered_classes
    # Filter by class type
    if filter_type:
        classes = [c for c in classes if c['class_type'].lower() == filter_type]
    # Attach trainer name to each class for display
    for c in classes:
        trainer = get_trainer_by_id(c['trainer_id'])
        c['trainer_name'] = trainer['name'] if trainer else "Unknown"
    return render_template('class_schedule.html',
                           page_title="Class Schedule",
                           classes=classes,
                           search_query=search_query,
                           filter_type=filter_type)
@app.route('/trainer-profiles', methods=['GET'])
def trainer_profiles():
    trainers = read_trainers()
    search_query = request.args.get('search', '').strip().lower()
    specialty_filter = request.args.get('filter', '').strip().lower()
    if search_query:
        trainers = [t for t in trainers if search_query in t['name'].lower() or search_query in t['specialty'].lower()]
    if specialty_filter:
        trainers = [t for t in trainers if specialty_filter in t['specialty'].lower()]
    return render_template('trainer_profiles.html',
                           page_title="Trainer Profiles",
                           trainers=trainers,
                           search_query=search_query,
                           specialty_filter=specialty_filter)
@app.route('/trainer-detail/<trainer_id>', methods=['GET'])
def trainer_detail(trainer_id):
    trainer = get_trainer_by_id(trainer_id)
    if not trainer:
        return "Trainer not found", 404
    # For trainer reviews, no data file specified, show empty list
    trainer_reviews = []
    return render_template('trainer_detail.html',
                           page_title="Trainer Profile",
                           trainer=trainer,
                           trainer_reviews=trainer_reviews)
@app.route('/pt-booking', methods=['GET', 'POST'])
def pt_booking():
    trainers = read_trainers()
    if request.method == 'POST':
        member_name = request.form.get('member_name', '').strip()
        trainer_id = request.form.get('select_trainer', '').strip()
        session_date = request.form.get('session_date', '').strip()
        session_time = request.form.get('session_time', '').strip()
        session_duration = request.form.get('session_duration', '').strip()
        # Basic validation
        if not member_name or not trainer_id or not session_date or not session_time or not session_duration:
            error = "All fields are required."
            return render_template('pt_booking.html',
                                   page_title="Book Personal Training",
                                   trainers=trainers,
                                   error=error,
                                   form_data=request.form)
        # Validate date format
        try:
            datetime.strptime(session_date, '%Y-%m-%d')
        except ValueError:
            error = "Invalid date format. Use YYYY-MM-DD."
            return render_template('pt_booking.html',
                                   page_title="Book Personal Training",
                                   trainers=trainers,
                                   error=error,
                                   form_data=request.form)
        # Validate session_duration as int and allowed values
        try:
            duration_int = int(session_duration)
            if duration_int not in (30, 60, 90):
                raise ValueError
        except ValueError:
            error = "Invalid session duration."
            return render_template('pt_booking.html',
                                   page_title="Book Personal Training",
                                   trainers=trainers,
                                   error=error,
                                   form_data=request.form)
        # Save booking with status Pending
        new_booking = {
            'member_name': member_name,
            'trainer_id': trainer_id,
            'booking_date': session_date,
            'booking_time': session_time,
            'duration_minutes': duration_int,
            'status': 'Pending'
        }
        write_booking(new_booking)
        success_message = "Booking request submitted successfully."
        return render_template('pt_booking.html',
                               page_title="Book Personal Training",
                               trainers=trainers,
                               success=success_message)
    # GET request
    return render_template('pt_booking.html',
                           page_title="Book Personal Training",
                           trainers=trainers)
@app.route('/workout-records', methods=['GET'])
def workout_records():
    workouts = read_workouts()
    filter_type = request.args.get('filter', '').strip().lower()
    # Since no authentication, show all workouts or filtered by type
    if filter_type:
        workouts = [w for w in workouts if w['workout_type'].lower() == filter_type]
    # Sort workouts by date descending
    workouts.sort(key=lambda w: w['workout_date'], reverse=True)
    return render_template('workout_records.html',
                           page_title="My Workout Records",
                           workouts=workouts,
                           filter_type=filter_type)
@app.route('/log-workout', methods=['GET', 'POST'])
def log_workout():
    if request.method == 'POST':
        member_name = request.form.get('member_name', '').strip()
        workout_type = request.form.get('workout_type', '').strip()
        workout_duration = request.form.get('workout_duration', '').strip()
        calories_burned = request.form.get('calories_burned', '').strip()
        workout_notes = request.form.get('workout_notes', '').strip()
        workout_date = request.form.get('workout_date', '').strip()
        # Basic validation
        if not member_name or not workout_type or not workout_duration or not calories_burned or not workout_date:
            error = "Please fill in all required fields."
            return render_template('log_workout.html',
                                   page_title="Log Workout",
                                   error=error,
                                   form_data=request.form)
        # Validate numeric fields
        try:
            duration_int = int(workout_duration)
            calories_int = int(calories_burned)
        except ValueError:
            error = "Duration and calories burned must be numbers."
            return render_template('log_workout.html',
                                   page_title="Log Workout",
                                   error=error,
                                   form_data=request.form)
        # Validate date format
        try:
            datetime.strptime(workout_date, '%Y-%m-%d')
        except ValueError:
            error = "Invalid date format. Use YYYY-MM-DD."
            return render_template('log_workout.html',
                                   page_title="Log Workout",
                                   error=error,
                                   form_data=request.form)
        new_workout = {
            'member_name': member_name,
            'workout_type': workout_type,
            'workout_date': workout_date,
            'duration_minutes': duration_int,
            'calories_burned': calories_int,
            'notes': workout_notes
        }
        write_workout(new_workout)
        success_message = "Workout logged successfully."
        return render_template('log_workout.html',
                               page_title="Log Workout",
                               success=success_message)
    # GET request
    # Provide today's date as default for workout_date
    today_str = datetime.today().strftime('%Y-%m-%d')
    return render_template('log_workout.html',
                           page_title="Log Workout",
                           today=today_str)
if __name__ == '__main__':
    app.run(port=5000, debug=True)