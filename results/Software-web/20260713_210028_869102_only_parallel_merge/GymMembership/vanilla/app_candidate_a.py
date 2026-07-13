from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)

data_dir = 'data'

# Utility functions to read and write data

def read_memberships():
    memberships = []
    path = os.path.join(data_dir, 'memberships.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split('|')
                    if len(parts) == 6:
                        membership = {
                            'membership_id': int(parts[0]),
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
    path = os.path.join(data_dir, 'classes.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
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
    return classes

def read_trainers():
    trainers = []
    path = os.path.join(data_dir, 'trainers.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
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
    return trainers

def read_bookings():
    bookings = []
    path = os.path.join(data_dir, 'bookings.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
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
    return bookings

def write_bookings(bookings):
    path = os.path.join(data_dir, 'bookings.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for b in bookings:
            line = f"{b['booking_id']}|{b['member_name']}|{b['trainer_id']}|{b['booking_date']}|{b['booking_time']}|{b['duration_minutes']}|{b['status']}\n"
            f.write(line)

def read_workouts():
    workouts = []
    path = os.path.join(data_dir, 'workouts.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
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
    return workouts

def write_workouts(workouts):
    path = os.path.join(data_dir, 'workouts.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for w in workouts:
            line = f"{w['workout_id']}|{w['member_name']}|{w['workout_type']}|{w['workout_date']}|{w['duration_minutes']}|{w['calories_burned']}|{w['notes']}\n"
            f.write(line)

# DASHBOARD
@app.route('/')
@app.route('/dashboard')
def dashboard():
    # For simulation, member name and status hardcoded
    member_name = "John Doe"
    member_status = "Premium Member"
    return render_template('dashboard.html', member_name=member_name, member_status=member_status)

# MEMBERSHIP PLANS
@app.route('/memberships')
def membership_plans():
    memberships = read_memberships()
    # Get filter query param
    plan_filter = request.args.get('filter', None)
    if plan_filter:
        memberships = [m for m in memberships if m['plan_name'].lower() == plan_filter.lower()]
    return render_template('memberships.html', memberships=memberships, selected_filter=plan_filter)

# PLAN DETAILS
@app.route('/memberships/<int:plan_id>')
def plan_details(plan_id):
    memberships = read_memberships()
    plan = next((m for m in memberships if m['membership_id'] == plan_id), None)
    if not plan:
        return "Plan not found", 404
    # Static reviews
    reviews = [
        {'reviewer':'Alice', 'comment':'Great value plan!'},
        {'reviewer':'Bob', 'comment':'Helps me stay fit and motivated.'},
        {'reviewer':'Charlie', 'comment':'Perfect for my busy schedule.'}
    ]
    return render_template('plan_details.html', plan=plan, reviews=reviews)

# CLASS SCHEDULE
@app.route('/schedule')
def class_schedule():
    classes = read_classes()
    trainers = read_trainers()
    # Compose trainer dict for lookup
    trainer_dict = {t['trainer_id']: t for t in trainers}

    # Filters and search
    search_term = request.args.get('search', '').lower()
    class_type_filter = request.args.get('filter', '').lower()

    filtered_classes = []
    for c in classes:
        # Match search: class name or trainer name
        trainer_name = trainer_dict.get(c['trainer_id'], {}).get('name','').lower()
        if search_term and (search_term not in c['class_name'].lower() and search_term not in trainer_name):
            continue
        # Filter by class type
        if class_type_filter and class_type_filter != c['class_type'].lower():
            continue
        filtered_classes.append(c)

    return render_template('schedule.html', classes=filtered_classes, trainers=trainer_dict.values(),
                           selected_filter=class_type_filter, search_term=search_term)

# TRAINER PROFILES
@app.route('/trainers')
def trainer_profiles():
    trainers = read_trainers()
    search_term = request.args.get('search', '').lower()
    specialty_filter = request.args.get('filter', '').lower()

    filtered_trainers = []
    for t in trainers:
        if search_term and (search_term not in t['name'].lower() and search_term not in t['specialty'].lower()):
            continue
        if specialty_filter and specialty_filter not in t['specialty'].lower():
            continue
        filtered_trainers.append(t)

    return render_template('trainers.html', trainers=filtered_trainers, selected_filter=specialty_filter, search_term=search_term)

# TRAINER DETAIL
@app.route('/trainers/<int:trainer_id>')
def trainer_detail(trainer_id):
    trainers = read_trainers()
    trainer = next((t for t in trainers if t['trainer_id'] == trainer_id), None)
    if not trainer:
        return "Trainer not found", 404
    # Static reviews
    reviews = [
        {'client':'Dave', 'comment':'Very knowledgeable and supportive.'},
        {'client':'Eva', 'comment':'Helped me achieve my fitness goals.'},
        {'client':'Frank', 'comment':'Great training sessions and tips.'}
    ]
    return render_template('trainer_detail.html', trainer=trainer, reviews=reviews)

# PT BOOKING
@app.route('/book-training', methods=['GET', 'POST'])
def pt_booking():
    trainers = read_trainers()
    preselected_trainer_id = request.args.get('trainer_id')
    message = None
    if request.method == 'POST':
        member_name = "John Doe"  # Simulate logged-in member
        trainer_id = int(request.form.get('select-trainer'))
        session_date = request.form.get('session-date')
        session_time = request.form.get('session-time')
        duration = int(request.form.get('session-duration'))

        # Validate inputs (simple)
        if not (trainer_id and session_date and session_time and duration):
            message = "Please fill all fields correctly."
        else:
            # Read existing bookings
            bookings = read_bookings()
            new_id = max([b['booking_id'] for b in bookings], default=0) + 1
            new_booking = {
                'booking_id': new_id,
                'member_name': member_name,
                'trainer_id': trainer_id,
                'booking_date': session_date,
                'booking_time': session_time,
                'duration_minutes': duration,
                'status': 'Pending'
            }
            bookings.append(new_booking)
            write_bookings(bookings)
            message = f"Booking confirmed for {session_date} at {session_time}."

    return render_template('booking.html', trainers=trainers, preselected_trainer_id=preselected_trainer_id, message=message)

# WORKOUT RECORDS
@app.route('/workouts')
def workout_records():
    workouts = read_workouts()
    member_name = "John Doe"  # Simulated member
    filter_type = request.args.get('filter', '').lower()
    filtered_workouts = []
    for w in workouts:
        if w['member_name'] != member_name:
            continue
        if filter_type and filter_type != w['workout_type'].lower():
            continue
        filtered_workouts.append(w)
    return render_template('workouts.html', workouts=filtered_workouts, filter_type=filter_type)

# LOG WORKOUT
@app.route('/log-workout', methods=['GET', 'POST'])
def log_workout():
    message = None
    if request.method == 'POST':
        member_name = "John Doe"  # Simulated member
        workout_type = request.form.get('workout-type')
        duration = request.form.get('workout-duration')
        calories = request.form.get('calories-burned')
        notes = request.form.get('workout-notes', '').replace('|','-')

        if not (workout_type and duration and calories):
            message = "Please fill all required fields."
        else:
            try:
                duration = int(duration)
                calories = int(calories)
            except:
                message = "Duration and calories must be numbers."

        if not message:
            workouts = read_workouts()
            new_id = max([w['workout_id'] for w in workouts], default=0) + 1
            workout_date = datetime.now().strftime('%Y-%m-%d')
            new_workout = {
                'workout_id': new_id,
                'member_name': member_name,
                'workout_type': workout_type,
                'workout_date': workout_date,
                'duration_minutes': duration,
                'calories_burned': calories,
                'notes': notes
            }
            workouts.append(new_workout)
            write_workouts(workouts)
            message = "Workout logged successfully."

    return render_template('log_workout.html', message=message)

if __name__ == '__main__':
    app.run(debug=True)
