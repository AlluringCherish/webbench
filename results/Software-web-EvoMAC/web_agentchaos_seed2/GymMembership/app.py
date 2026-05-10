'''
Main backend application for GymMembership web app.
Defines routes for all pages starting from '/' as Dashboard.
Ensures all frontend navigation URLs use backend routes.
'''
from flask import Flask, render_template, request, redirect, url_for
import os
app = Flask(__name__)
DATA_DIR = 'data'
# Utility functions to read data from text files
def read_memberships():
    memberships = []
    path = os.path.join(DATA_DIR, 'memberships.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
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
                if line:
                    parts = line.split('|')
                    if len(parts) == 8:
                        cls = {
                            'class_id': parts[0],
                            'class_name': parts[1],
                            'trainer_id': parts[2],
                            'class_type': parts[3],
                            'schedule_day': parts[4],
                            'schedule_time': parts[5],
                            'capacity': parts[6],
                            'duration': parts[7]
                        }
                        classes.append(cls)
    return classes
def read_trainers():
    trainers = []
    path = os.path.join(DATA_DIR, 'trainers.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
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
                if line:
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
                if line:
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
# Route for Dashboard page - starting page '/'
@app.route('/')
def dashboard():
    # For demo, show some highlights: first membership plan, first class, first trainer
    memberships = read_memberships()
    classes = read_classes()
    trainers = read_trainers()
    member_status = "Welcome to GymMembership! Explore our plans and classes."
    featured_class = classes[0] if classes else None
    featured_trainer = trainers[0] if trainers else None
    return render_template('dashboard.html',
                           member_status=member_status,
                           featured_class=featured_class,
                           featured_trainer=featured_trainer)
# Route for Membership Plans page
@app.route('/memberships')
def memberships():
    memberships = read_memberships()
    filter_type = request.args.get('filter', None)
    if filter_type:
        memberships = [m for m in memberships if m['plan_name'].lower() == filter_type.lower()]
    return render_template('memberships.html', memberships=memberships, filter_type=filter_type)
# Route for Plan Details page
@app.route('/plan/<plan_id>')
def plan_details(plan_id):
    memberships = read_memberships()
    plan = next((m for m in memberships if m['membership_id'] == plan_id), None)
    if not plan:
        return "Plan not found", 404
    # For simplicity, no real reviews data, show placeholder
    plan_reviews = [
        {"member": "John Doe", "review": "Great value and facilities."},
        {"member": "Jane Smith", "review": "Loved the classes included."}
    ]
    return render_template('plan_details.html', plan=plan, plan_reviews=plan_reviews)
# Route for Class Schedule page
@app.route('/schedule')
def schedule():
    classes = read_classes()
    trainers = read_trainers()
    search_query = request.args.get('search', '').lower()
    filter_type = request.args.get('filter', None)
    # Filter by search query (class name or trainer name)
    if search_query:
        filtered_classes = []
        for c in classes:
            trainer = next((t for t in trainers if t['trainer_id'] == c['trainer_id']), None)
            trainer_name = trainer['name'].lower() if trainer else ''
            if search_query in c['class_name'].lower() or search_query in trainer_name:
                filtered_classes.append(c)
        classes = filtered_classes
    # Filter by class type
    if filter_type:
        classes = [c for c in classes if c['class_type'].lower() == filter_type.lower()]
    # Attach trainer name to each class for display
    for c in classes:
        trainer = next((t for t in trainers if t['trainer_id'] == c['trainer_id']), None)
        c['trainer_name'] = trainer['name'] if trainer else 'Unknown'
    return render_template('schedule.html', classes=classes, search_query=search_query, filter_type=filter_type)
# Route for Trainer Profiles page
@app.route('/trainers')
def trainers():
    trainers = read_trainers()
    search_query = request.args.get('search', '').lower()
    filter_specialty = request.args.get('filter', None)
    if search_query:
        trainers = [t for t in trainers if search_query in t['name'].lower() or search_query in t['specialty'].lower()]
    if filter_specialty:
        trainers = [t for t in trainers if filter_specialty.lower() in t['specialty'].lower()]
    return render_template('trainers.html', trainers=trainers, search_query=search_query, filter_specialty=filter_specialty)
# Route for Trainer Detail page
@app.route('/trainer/<trainer_id>')
def trainer_detail(trainer_id):
    trainers = read_trainers()
    trainer = next((t for t in trainers if t['trainer_id'] == trainer_id), None)
    if not trainer:
        return "Trainer not found", 404
    # Placeholder reviews
    trainer_reviews = [
        {"client": "Alex Johnson", "review": "Very knowledgeable and motivating."},
        {"client": "Emily Clark", "review": "Helped me improve my flexibility greatly."}
    ]
    return render_template('trainer_detail.html', trainer=trainer, trainer_reviews=trainer_reviews)
# Route for PT Booking page
@app.route('/booking', methods=['GET', 'POST'])
def booking():
    trainers = read_trainers()
    if request.method == 'POST':
        # Process booking form submission
        member_name = request.form.get('member_name', 'Guest')
        trainer_id = request.form.get('select_trainer')
        booking_date = request.form.get('session_date')
        booking_time = request.form.get('session_time')
        duration = request.form.get('session_duration')
        # Generate new booking_id
        bookings = read_bookings()
        new_id = str(int(bookings[-1]['booking_id']) + 1) if bookings else '1'
        new_booking = f"{new_id}|{member_name}|{trainer_id}|{booking_date}|{booking_time}|{duration}|Pending\n"
        with open(os.path.join(DATA_DIR, 'bookings.txt'), 'a', encoding='utf-8') as f:
            f.write(new_booking)
        return redirect(url_for('booking_confirmation', booking_id=new_id))
    # GET request: show booking form
    # Provide time slots and durations
    time_slots = ['06:00', '07:00', '08:00', '09:00', '10:00', '14:00', '15:00', '16:00', '17:00', '18:00']
    durations = ['30', '60', '90']
    return render_template('booking.html', trainers=trainers, time_slots=time_slots, durations=durations)
# Booking confirmation page
@app.route('/booking/confirmation/<booking_id>')
def booking_confirmation(booking_id):
    bookings = read_bookings()
    booking = next((b for b in bookings if b['booking_id'] == booking_id), None)
    if not booking:
        return "Booking not found", 404
    trainers = read_trainers()
    trainer = next((t for t in trainers if t['trainer_id'] == booking['trainer_id']), None)
    return render_template('booking_confirmation.html', booking=booking, trainer=trainer)
# Route for Workout Records page
@app.route('/workouts')
def workouts():
    workouts = read_workouts()
    filter_type = request.args.get('filter', None)
    if filter_type:
        workouts = [w for w in workouts if w['workout_type'].lower() == filter_type.lower()]
    return render_template('workouts.html', workouts=workouts, filter_type=filter_type)
# Route for Log Workout page
@app.route('/log-workout', methods=['GET', 'POST'])
def log_workout():
    if request.method == 'POST':
        member_name = request.form.get('member_name', 'Guest')
        workout_type = request.form.get('workout_type')
        workout_duration = request.form.get('workout_duration')
        calories_burned = request.form.get('calories_burned')
        workout_notes = request.form.get('workout_notes')
        # Generate new workout_id
        workouts = read_workouts()
        new_id = str(int(workouts[-1]['workout_id']) + 1) if workouts else '1'
        from datetime import date
        today = date.today().isoformat()
        new_workout = f"{new_id}|{member_name}|{workout_type}|{today}|{workout_duration}|{calories_burned}|{workout_notes}\n"
        with open(os.path.join(DATA_DIR, 'workouts.txt'), 'a', encoding='utf-8') as f:
            f.write(new_workout)
        return redirect(url_for('workouts'))
    # GET request: show log workout form
    workout_types = ['Cardio', 'Strength', 'Flexibility', 'Sports']
    return render_template('log_workout.html', workout_types=workout_types)
if __name__ == '__main__':
    app.run(debug=True)