'''
Main backend Python application file for GymMembership web application.
Handles routing for all nine pages, reads and writes data to local text files in the data/ directory,
processes user inputs, and renders HTML templates with dynamic content.
No authentication required; all features directly accessible.
'''
from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime
app = Flask(__name__)
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
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
    if bookings:
        max_id = max(int(b['booking_id']) for b in bookings)
        next_id = max_id + 1
    else:
        next_id = 1
    line = f"{next_id}|{new_booking['member_name']}|{new_booking['trainer_id']}|{new_booking['booking_date']}|{new_booking['booking_time']}|{new_booking['duration_minutes']}|{new_booking['status']}\n"
    with open(path, 'a', encoding='utf-8') as f:
        f.write(line)
    return next_id
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
    if workouts:
        max_id = max(int(w['workout_id']) for w in workouts)
        next_id = max_id + 1
    else:
        next_id = 1
    line = f"{next_id}|{new_workout['member_name']}|{new_workout['workout_type']}|{new_workout['workout_date']}|{new_workout['duration_minutes']}|{new_workout['calories_burned']}|{new_workout['notes']}\n"
    with open(path, 'a', encoding='utf-8') as f:
        f.write(line)
    return next_id
# Since no authentication, we use a fixed member name for demonstration
DEFAULT_MEMBER_NAME = "Guest User"
# Route: Dashboard page (start page)
@app.route('/')
def dashboard():
    # For member highlights, we can show a welcome message and some featured classes (e.g. first 3 classes)
    classes = read_classes()
    featured_classes = classes[:3] if len(classes) >= 3 else classes
    memberships = read_memberships()
    # For member status info, since no login, just show default message
    member_status = "Welcome, Guest! Explore our gym membership plans and classes."
    return render_template('dashboard.html',
                           member_status=member_status,
                           featured_classes=featured_classes)
# Route: Membership Plans page
@app.route('/membership_plans', methods=['GET'])
def membership_plans():
    memberships = read_memberships()
    filter_type = request.args.get('filter', None)
    if filter_type:
        filtered = [m for m in memberships if m['plan_name'].lower() == filter_type.lower()]
    else:
        filtered = memberships
    return render_template('membership_plans.html',
                           memberships=filtered,
                           filter_type=filter_type)
# Route: Plan Details page
@app.route('/plan_details/<plan_id>', methods=['GET', 'POST'])
def plan_details(plan_id):
    memberships = read_memberships()
    plan = next((m for m in memberships if m['membership_id'] == plan_id), None)
    if not plan:
        return "Plan not found", 404
    # For simplicity, no real enrollment logic, just a confirmation message on POST
    enrolled = False
    if request.method == 'POST':
        # Enrollment simulated
        enrolled = True
    # No reviews data provided in requirements, so empty list
    plan_reviews = []
    return render_template('plan_details.html',
                           plan=plan,
                           enrolled=enrolled,
                           plan_reviews=plan_reviews)
# Route: Class Schedule page
@app.route('/class_schedule', methods=['GET'])
def class_schedule():
    classes = read_classes()
    trainers = read_trainers()
    # Build a dict for trainer_id to name for display
    trainer_dict = {t['trainer_id']: t['name'] for t in trainers}
    search_query = request.args.get('search', '').strip().lower()
    filter_type = request.args.get('filter', '').strip().lower()
    filtered_classes = classes
    if search_query:
        filtered_classes = [c for c in filtered_classes if search_query in c['class_name'].lower() or
                            trainer_dict.get(c['trainer_id'], '').lower().find(search_query) != -1]
    if filter_type:
        filtered_classes = [c for c in filtered_classes if c['class_type'].lower() == filter_type]
    return render_template('class_schedule.html',
                           classes=filtered_classes,
                           trainer_dict=trainer_dict,
                           search_query=search_query,
                           filter_type=filter_type)
# Route: Trainer Profiles page
@app.route('/trainer_profiles', methods=['GET'])
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
# Route: Trainer Detail page
@app.route('/trainer_detail/<trainer_id>', methods=['GET'])
def trainer_detail(trainer_id):
    trainers = read_trainers()
    trainer = next((t for t in trainers if t['trainer_id'] == trainer_id), None)
    if not trainer:
        return "Trainer not found", 404
    # No reviews data provided, so empty list
    trainer_reviews = []
    return render_template('trainer_detail.html',
                           trainer=trainer,
                           trainer_reviews=trainer_reviews)
# Route: PT Booking page
@app.route('/pt_booking', methods=['GET', 'POST'])
def pt_booking():
    trainers = read_trainers()
    if request.method == 'POST':
        member_name = request.form.get('member_name', DEFAULT_MEMBER_NAME).strip()
        trainer_id = request.form.get('select-trainer')
        session_date = request.form.get('session-date')
        session_time = request.form.get('session-time')
        session_duration = request.form.get('session-duration')
        # Basic validation
        if not (trainer_id and session_date and session_time and session_duration):
            error = "Please fill in all required fields."
            return render_template('pt_booking.html', trainers=trainers, error=error)
        # Validate date format
        try:
            datetime.strptime(session_date, '%Y-%m-%d')
        except ValueError:
            error = "Invalid date format."
            return render_template('pt_booking.html', trainers=trainers, error=error)
        # Validate duration as int
        try:
            duration_minutes = int(session_duration)
        except ValueError:
            error = "Invalid session duration."
            return render_template('pt_booking.html', trainers=trainers, error=error)
        new_booking = {
            'member_name': member_name if member_name else DEFAULT_MEMBER_NAME,
            'trainer_id': trainer_id,
            'booking_date': session_date,
            'booking_time': session_time,
            'duration_minutes': duration_minutes,
            'status': 'Pending'
        }
        booking_id = write_booking(new_booking)
        success_message = f"Booking confirmed with ID {booking_id} (status: Pending)."
        return render_template('pt_booking.html', trainers=trainers, success_message=success_message)
    # GET request
    return render_template('pt_booking.html', trainers=trainers)
# Route: Workout Records page
@app.route('/workout_records', methods=['GET'])
def workout_records():
    workouts = read_workouts()
    filter_type = request.args.get('filter', '').strip().lower()
    # Filter by workout type if specified
    filtered_workouts = workouts
    if filter_type:
        filtered_workouts = [w for w in filtered_workouts if w['workout_type'].lower() == filter_type]
    # Sort workouts by date descending
    filtered_workouts.sort(key=lambda w: w['workout_date'], reverse=True)
    return render_template('workout_records.html',
                           workouts=filtered_workouts,
                           filter_type=filter_type)
# Route: Log Workout page
@app.route('/log_workout', methods=['GET', 'POST'])
def log_workout():
    if request.method == 'POST':
        workout_type = request.form.get('workout-type')
        workout_duration = request.form.get('workout-duration')
        calories_burned = request.form.get('calories-burned')
        workout_notes = request.form.get('workout-notes', '').strip()
        member_name = request.form.get('member_name', DEFAULT_MEMBER_NAME).strip()
        # Validate required fields
        if not workout_type or not workout_duration or not calories_burned:
            error = "Please fill in all required fields."
            return render_template('log_workout.html', error=error)
        # Validate numeric inputs
        try:
            duration_minutes = int(workout_duration)
            calories = int(calories_burned)
        except ValueError:
            error = "Duration and calories burned must be numbers."
            return render_template('log_workout.html', error=error)
        workout_date = datetime.now().strftime('%Y-%m-%d')
        new_workout = {
            'member_name': member_name if member_name else DEFAULT_MEMBER_NAME,
            'workout_type': workout_type,
            'workout_date': workout_date,
            'duration_minutes': duration_minutes,
            'calories_burned': calories,
            'notes': workout_notes
        }
        workout_id = write_workout(new_workout)
        success_message = f"Workout logged successfully with ID {workout_id}."
        return render_template('log_workout.html', success_message=success_message)
    # GET request
    return render_template('log_workout.html')
# Removed redundant /back_to_dashboard route to avoid confusion
# Run the app on local port 5000
if __name__ == '__main__':
    app.run(port=5000, debug=True)