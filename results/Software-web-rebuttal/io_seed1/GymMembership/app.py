'''
Main backend Python application for GymMembership web application.
Handles routing for all nine pages, reads and writes data to local text files in the data/ directory,
processes user inputs, and renders HTML templates with appropriate data.
No authentication required; all features directly accessible.
'''
from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime
app = Flask(__name__)
DATA_DIR = 'data'
# Utility functions to read and write data files
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
def write_booking(new_booking):
    path = os.path.join(DATA_DIR, 'bookings.txt')
    # Determine new booking_id
    bookings = read_bookings()
    if bookings:
        max_id = max(int(b['booking_id']) for b in bookings)
        new_id = max_id + 1
    else:
        new_id = 1
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
                'duration_minutes': duration_minutes,
                'calories_burned': calories_burned,
                'notes': notes
            })
    return workouts
def write_workout(new_workout):
    path = os.path.join(DATA_DIR, 'workouts.txt')
    workouts = read_workouts()
    if workouts:
        max_id = max(int(w['workout_id']) for w in workouts)
        new_id = max_id + 1
    else:
        new_id = 1
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
# ROUTES
@app.route('/')
def dashboard():
    # For member highlights and featured classes, we can show some sample data
    memberships = read_memberships()
    classes = read_classes()
    trainers = read_trainers()
    # For simplicity, show first 3 classes as featured classes
    featured_classes = classes[:3]
    # Member welcome: since no authentication, show generic welcome
    member_status = "Welcome to Gym Membership! Explore our plans and classes."
    return render_template('dashboard.html',
                           member_status=member_status,
                           featured_classes=featured_classes,
                           memberships=memberships,
                           trainers=trainers)
# Membership Plans Page
@app.route('/memberships', methods=['GET', 'POST'])
def membership_plans():
    memberships = read_memberships()
    filter_type = request.args.get('filter', None)
    filtered_memberships = memberships
    if filter_type:
        # Filter by plan_name matching filter_type (Basic, Premium, Elite)
        filtered_memberships = [m for m in memberships if m['plan_name'].lower() == filter_type.lower()]
    return render_template('membership_plans.html',
                           memberships=filtered_memberships,
                           filter_type=filter_type)
# Plan Details Page
@app.route('/plan/<plan_id>', methods=['GET', 'POST'])
def plan_details(plan_id):
    plan = get_membership_by_id(plan_id)
    if not plan:
        return "Plan not found", 404
    # For reviews, since not specified, show empty or static placeholder
    plan_reviews = []  # Could be extended to read from a reviews file if needed
    if request.method == 'POST':
        # Enroll plan button clicked
        # Since no authentication, just redirect back to dashboard or show confirmation
        # Could extend to save enrollment if needed
        return redirect(url_for('dashboard'))
    return render_template('plan_details.html',
                           plan=plan,
                           plan_reviews=plan_reviews)
# Class Schedule Page
@app.route('/classes', methods=['GET', 'POST'])
def class_schedule():
    classes = read_classes()
    trainers = read_trainers()
    # Get search and filter parameters
    search_query = request.args.get('search', '').strip().lower()
    filter_type = request.args.get('filter', '').strip().lower()
    filtered_classes = classes
    if search_query:
        # Filter classes by class_name or trainer name containing search_query
        filtered_classes = []
        for c in classes:
            trainer = get_trainer_by_id(c['trainer_id'])
            trainer_name = trainer['name'].lower() if trainer else ''
            if search_query in c['class_name'].lower() or search_query in trainer_name:
                filtered_classes.append(c)
    if filter_type:
        filtered_classes = [c for c in filtered_classes if c['class_type'].lower() == filter_type]
    # Enrich classes with trainer name for display
    for c in filtered_classes:
        trainer = get_trainer_by_id(c['trainer_id'])
        c['trainer_name'] = trainer['name'] if trainer else 'Unknown'
    return render_template('class_schedule.html',
                           classes=filtered_classes,
                           search_query=search_query,
                           filter_type=filter_type)
# Trainer Profiles Page
@app.route('/trainers', methods=['GET', 'POST'])
def trainer_profiles():
    trainers = read_trainers()
    search_query = request.args.get('search', '').strip().lower()
    filter_specialty = request.args.get('filter', '').strip().lower()
    filtered_trainers = trainers
    if search_query:
        filtered_trainers = [t for t in filtered_trainers if search_query in t['name'].lower() or search_query in t['specialty'].lower()]
    if filter_specialty:
        filtered_trainers = [t for t in filtered_trainers if filter_specialty in t['specialty'].lower()]
    return render_template('trainer_profiles.html',
                           trainers=filtered_trainers,
                           search_query=search_query,
                           filter_specialty=filter_specialty)
# Trainer Detail Page
@app.route('/trainer/<trainer_id>', methods=['GET', 'POST'])
def trainer_detail(trainer_id):
    trainer = get_trainer_by_id(trainer_id)
    if not trainer:
        return "Trainer not found", 404
    # For reviews, show empty or static placeholder
    trainer_reviews = []
    if request.method == 'POST':
        # Book session button clicked, redirect to booking page with trainer pre-selected
        return redirect(url_for('pt_booking', selected_trainer=trainer_id))
    return render_template('trainer_detail.html',
                           trainer=trainer,
                           trainer_reviews=trainer_reviews)
# PT Booking Page
@app.route('/booking', methods=['GET', 'POST'])
def pt_booking():
    trainers = read_trainers()
    selected_trainer = request.args.get('selected_trainer', None)
    # Define possible time slots for booking (example: 6am to 9pm every hour)
    time_slots = [f"{hour:02d}:00" for hour in range(6, 22)]
    if request.method == 'POST':
        member_name = request.form.get('member_name', '').strip()
        trainer_id = request.form.get('select_trainer')
        session_date = request.form.get('session_date')
        session_time = request.form.get('session_time')
        session_duration = request.form.get('session_duration')
        # Basic validation
        if not member_name or not trainer_id or not session_date or not session_time or not session_duration:
            error = "Please fill in all fields."
            return render_template('pt_booking.html',
                                   trainers=trainers,
                                   selected_trainer=selected_trainer,
                                   time_slots=time_slots,
                                   error=error,
                                   form_data=request.form)
        # Validate date format
        try:
            datetime.strptime(session_date, '%Y-%m-%d')
        except ValueError:
            error = "Invalid date format."
            return render_template('pt_booking.html',
                                   trainers=trainers,
                                   selected_trainer=selected_trainer,
                                   time_slots=time_slots,
                                   error=error,
                                   form_data=request.form)
        # Save booking with status 'Pending'
        new_booking = {
            'member_name': member_name,
            'trainer_id': trainer_id,
            'booking_date': session_date,
            'booking_time': session_time,
            'duration_minutes': session_duration,
            'status': 'Pending'
        }
        write_booking(new_booking)
        return redirect(url_for('dashboard'))
    return render_template('pt_booking.html',
                           trainers=trainers,
                           selected_trainer=selected_trainer,
                           time_slots=time_slots)
# Workout Records Page
@app.route('/workouts', methods=['GET', 'POST'])
def workout_records():
    workouts = read_workouts()
    filter_type = request.args.get('filter', '').strip().lower()
    filtered_workouts = workouts
    if filter_type:
        filtered_workouts = [w for w in workouts if w['workout_type'].lower() == filter_type]
    return render_template('workout_records.html',
                           workouts=filtered_workouts,
                           filter_type=filter_type)
# Log Workout Page
@app.route('/log_workout', methods=['GET', 'POST'])
def log_workout():
    workout_types = ['Cardio', 'Strength', 'Flexibility', 'Sports']
    if request.method == 'POST':
        member_name = request.form.get('member_name', '').strip()
        workout_type = request.form.get('workout_type')
        workout_duration = request.form.get('workout_duration')
        calories_burned = request.form.get('calories_burned')
        workout_notes = request.form.get('workout_notes', '').strip()
        workout_date = datetime.now().strftime('%Y-%m-%d')
        # Basic validation
        if not member_name or not workout_type or not workout_duration or not calories_burned:
            error = "Please fill in all required fields."
            return render_template('log_workout.html',
                                   workout_types=workout_types,
                                   error=error,
                                   form_data=request.form)
        # Validate numeric fields
        try:
            workout_duration_int = int(workout_duration)
            calories_burned_int = int(calories_burned)
        except ValueError:
            error = "Duration and calories burned must be numbers."
            return render_template('log_workout.html',
                                   workout_types=workout_types,
                                   error=error,
                                   form_data=request.form)
        new_workout = {
            'member_name': member_name,
            'workout_type': workout_type,
            'workout_date': workout_date,
            'duration_minutes': str(workout_duration_int),
            'calories_burned': str(calories_burned_int),
            'notes': workout_notes
        }
        write_workout(new_workout)
        return redirect(url_for('workout_records'))
    return render_template('log_workout.html',
                           workout_types=workout_types)
# Back to dashboard routes for buttons that require it
@app.route('/back_to_dashboard')
def back_to_dashboard():
    return redirect(url_for('dashboard'))
if __name__ == '__main__':
    app.run(port=5000, debug=True)