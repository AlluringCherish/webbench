"""
Flask web application for GymMembership system.
Provides dashboard, membership plans, class schedules, trainer profiles,
personal training booking, workout records, and workout logging.
Data is managed via text files in 'data' directory.
All URLs in frontend use Flask's url_for for consistency.
"""
import os
from flask import Flask, render_template, request, redirect, url_for
from datetime import date
app = Flask(__name__)
DATA_DIR = 'data'
def read_memberships():
    memberships = []
    path = os.path.join(DATA_DIR, 'memberships.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) == 6:
                    membership = {
                        'membership_id': parts[0],
                        'plan_name': parts[1],
                        'price': parts[2],
                        'billing_cycle': parts[3],
                        'features': parts[4],
                        'max_classes': parts[5]
                    }
                    memberships.append(membership)
    return memberships
def read_classes():
    classes = []
    path = os.path.join(DATA_DIR, 'classes.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) == 8:
                    class_item = {
                        'class_id': parts[0],
                        'class_name': parts[1],
                        'trainer_id': parts[2],
                        'class_type': parts[3],
                        'schedule_day': parts[4],
                        'schedule_time': parts[5],
                        'capacity': parts[6],
                        'duration': parts[7]
                    }
                    classes.append(class_item)
    return classes
def read_trainers():
    trainers = []
    path = os.path.join(DATA_DIR, 'trainers.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) == 6:
                    trainer = {
                        'trainer_id': parts[0],
                        'name': parts[1],
                        'specialty': parts[2],
                        'certifications': parts[3],
                        'experience_years': parts[4],
                        'bio': parts[5]
                    }
                    trainers.append(trainer)
    return trainers
def read_bookings():
    bookings = []
    path = os.path.join(DATA_DIR, 'bookings.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) == 7:
                    booking = {
                        'booking_id': parts[0],
                        'member_name': parts[1],
                        'trainer_id': parts[2],
                        'booking_date': parts[3],
                        'booking_time': parts[4],
                        'duration_minutes': parts[5],
                        'status': parts[6]
                    }
                    bookings.append(booking)
    return bookings
def read_workouts():
    workouts = []
    path = os.path.join(DATA_DIR, 'workouts.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) == 7:
                    workout = {
                        'workout_id': parts[0],
                        'member_name': parts[1],
                        'workout_type': parts[2],
                        'workout_date': parts[3],
                        'duration_minutes': parts[4],
                        'calories_burned': parts[5],
                        'notes': parts[6]
                    }
                    workouts.append(workout)
    return workouts
@app.route('/')
def dashboard():
    classes = read_classes()
    featured_classes = classes[:3] if len(classes) >= 3 else classes
    return render_template('dashboard.html', featured_classes=featured_classes)
@app.route('/memberships')
def memberships():
    memberships = read_memberships()
    filter_type = request.args.get('filter')
    if filter_type:
        memberships = [m for m in memberships if filter_type.lower() in m['plan_name'].lower()]
    return render_template('memberships.html', memberships=memberships, filter_type=filter_type)
@app.route('/plan/<plan_id>')
def plan_details(plan_id):
    memberships = read_memberships()
    plan = next((m for m in memberships if m['membership_id'] == plan_id), None)
    if not plan:
        return "Plan not found", 404
    # No reviews data as per instructions
    plan_reviews = []
    return render_template('plan_details.html', plan=plan, plan_reviews=plan_reviews)
@app.route('/classes')
def classes():
    classes = read_classes()
    trainers = read_trainers()
    search = request.args.get('search', '').strip().lower()
    filter_type = request.args.get('filter', '').strip().lower()
    # Filter by search (class name or trainer name)
    if search:
        trainer_ids = [t['trainer_id'] for t in trainers if search in t['name'].lower()]
        classes = [c for c in classes if search in c['class_name'].lower() or c['trainer_id'] in trainer_ids]
    # Filter by class type
    if filter_type:
        classes = [c for c in classes if c['class_type'].lower() == filter_type]
    # Map trainer names for display
    trainer_dict = {t['trainer_id']: t['name'] for t in trainers}
    return render_template('classes.html', classes=classes, trainer_dict=trainer_dict,
                           search=search, filter_type=filter_type)
@app.route('/trainers')
def trainers():
    trainers = read_trainers()
    search = request.args.get('search', '').strip().lower()
    filter_specialty = request.args.get('filter', '').strip().lower()
    filtered_trainers = trainers
    if search:
        filtered_trainers = [t for t in filtered_trainers if search in t['name'].lower()]
    if filter_specialty:
        filtered_trainers = [t for t in filtered_trainers if filter_specialty in t['specialty'].lower()]
    return render_template('trainers.html', trainers=filtered_trainers, search=search, filter_specialty=filter_specialty)
@app.route('/trainer/<trainer_id>', methods=['GET', 'POST'])
def trainer_detail(trainer_id):
    trainers = read_trainers()
    trainer = next((t for t in trainers if t['trainer_id'] == trainer_id), None)
    if not trainer:
        return "Trainer not found", 404
    if request.method == 'POST':
        # Handle booking form submission
        member_name = request.form.get('member_name', '').strip()
        session_date = request.form.get('session_date', '').strip()
        session_time = request.form.get('session_time', '').strip()
        session_duration = request.form.get('session_duration', '').strip()
        if not (member_name and session_date and session_time and session_duration):
            return render_template('trainer_detail.html', trainer=trainer, error="All fields are required.")
        bookings = read_bookings()
        new_id = str(max([int(b['booking_id']) for b in bookings], default=0) + 1)
        new_booking = '|'.join([new_id, member_name, trainer_id, session_date, session_time, session_duration, 'Pending'])
        path = os.path.join(DATA_DIR, 'bookings.txt')
        with open(path, 'a', encoding='utf-8') as f:
            f.write(new_booking + '\n')
        return redirect(url_for('dashboard'))
    return render_template('trainer_detail.html', trainer=trainer)
@app.route('/book_training', methods=['GET', 'POST'])
def book_training():
    trainers = read_trainers()
    if request.method == 'POST':
        member_name = request.form.get('member_name', '').strip()
        trainer_id = request.form.get('select_trainer', '').strip()
        session_date = request.form.get('session_date', '').strip()
        session_time = request.form.get('session_time', '').strip()
        session_duration = request.form.get('session_duration', '').strip()
        if not (member_name and trainer_id and session_date and session_time and session_duration):
            return render_template('book_training.html', trainers=trainers, error="All fields are required.")
        bookings = read_bookings()
        new_id = str(max([int(b['booking_id']) for b in bookings], default=0) + 1)
        new_booking = '|'.join([new_id, member_name, trainer_id, session_date, session_time, session_duration, 'Pending'])
        path = os.path.join(DATA_DIR, 'bookings.txt')
        with open(path, 'a', encoding='utf-8') as f:
            f.write(new_booking + '\n')
        return redirect(url_for('dashboard'))
    return render_template('book_training.html', trainers=trainers)
@app.route('/workouts')
def workouts():
    workouts = read_workouts()
    filter_type = request.args.get('filter', '').strip().lower()
    if filter_type:
        workouts = [w for w in workouts if w['workout_type'].lower() == filter_type]
    return render_template('workouts.html', workouts=workouts, filter_type=filter_type)
@app.route('/log_workout', methods=['GET', 'POST'])
def log_workout():
    if request.method == 'POST':
        member_name = request.form.get('member_name', '').strip()
        workout_type = request.form.get('workout_type', '').strip()
        workout_duration = request.form.get('workout_duration', '').strip()
        calories_burned = request.form.get('calories_burned', '').strip()
        workout_notes = request.form.get('workout_notes', '').strip()
        workout_date = date.today().isoformat()
        if not (member_name and workout_type and workout_duration and calories_burned):
            return render_template('log_workout.html', error="All fields except notes are required.")
        workouts = read_workouts()
        new_id = str(max([int(w['workout_id']) for w in workouts], default=0) + 1)
        new_workout = '|'.join([new_id, member_name, workout_type, workout_date,
                                workout_duration, calories_burned, workout_notes])
        path = os.path.join(DATA_DIR, 'workouts.txt')
        with open(path, 'a', encoding='utf-8') as f:
            f.write(new_workout + '\n')
        return redirect(url_for('workouts'))
    return render_template('log_workout.html')
if __name__ == '__main__':
    app.run(debug=True)