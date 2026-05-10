'''
Flask backend for GymMembership web application.
Defines routes for all pages with proper URL routing.
Dashboard page is served at '/' as the landing page.
All routes correspond to frontend navigation URLs.
'''
from flask import Flask, render_template, request, redirect, url_for
import os
app = Flask(__name__)
DATA_DIR = 'data'
# Helper functions to read data from text files
def read_memberships():
    memberships = []
    path = os.path.join(DATA_DIR, 'memberships.txt')
    if os.path.exists(path):
        with open(path, 'r') as f:
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
        with open(path, 'r') as f:
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
        with open(path, 'r') as f:
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
        with open(path, 'r') as f:
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
        with open(path, 'r') as f:
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
@app.route('/')
def dashboard():
    # For demo, show some highlights: first membership plan, first class, first trainer
    memberships = read_memberships()
    classes = read_classes()
    trainers = read_trainers()
    featured_class = classes[0] if classes else None
    featured_membership = memberships[0] if memberships else None
    featured_trainer = trainers[0] if trainers else None
    return render_template('dashboard.html',
                           featured_class=featured_class,
                           featured_membership=featured_membership,
                           featured_trainer=featured_trainer)
@app.route('/membership-plans')
def membership_plans():
    memberships = read_memberships()
    filter_type = request.args.get('filter', None)
    if filter_type:
        memberships = [m for m in memberships if m['plan_name'].lower() == filter_type.lower()]
    return render_template('membership_plans.html', memberships=memberships, filter_type=filter_type)
@app.route('/plan-details/<plan_id>')
def plan_details(plan_id):
    memberships = read_memberships()
    plan = next((m for m in memberships if m['membership_id'] == plan_id), None)
    if not plan:
        return "Plan not found", 404
    # For simplicity, no reviews implemented yet
    plan_reviews = []
    return render_template('plan_details.html', plan=plan, plan_reviews=plan_reviews)
@app.route('/class-schedule')
def class_schedule():
    classes = read_classes()
    trainers = read_trainers()
    search_query = request.args.get('search', '').lower()
    filter_type = request.args.get('filter', '').lower()
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
@app.route('/trainer-profiles')
def trainer_profiles():
    trainers = read_trainers()
    search_query = request.args.get('search', '').lower()
    filter_specialty = request.args.get('filter', '').lower()
    filtered_trainers = trainers
    if search_query:
        filtered_trainers = [t for t in filtered_trainers if search_query in t['name'].lower() or search_query in t['specialty'].lower()]
    if filter_specialty:
        filtered_trainers = [t for t in filtered_trainers if filter_specialty in t['specialty'].lower()]
    return render_template('trainer_profiles.html', trainers=filtered_trainers,
                           search_query=search_query, filter_specialty=filter_specialty)
@app.route('/trainer-detail/<trainer_id>')
def trainer_detail(trainer_id):
    trainers = read_trainers()
    trainer = next((t for t in trainers if t['trainer_id'] == trainer_id), None)
    if not trainer:
        return "Trainer not found", 404
    # For simplicity, no reviews implemented yet
    trainer_reviews = []
    return render_template('trainer_detail.html', trainer=trainer, trainer_reviews=trainer_reviews)
@app.route('/pt-booking', methods=['GET', 'POST'])
def pt_booking():
    trainers = read_trainers()
    if request.method == 'POST':
        # Process booking form submission
        member_name = request.form.get('member_name', 'Guest')
        trainer_id = request.form.get('select_trainer')
        session_date = request.form.get('session_date')
        session_time = request.form.get('session_time')
        session_duration = request.form.get('session_duration')
        # Generate booking_id
        bookings = read_bookings()
        booking_id = str(int(bookings[-1]['booking_id']) + 1) if bookings else '1'
        new_booking = f"{booking_id}|{member_name}|{trainer_id}|{session_date}|{session_time}|{session_duration}|Pending\n"
        with open(os.path.join(DATA_DIR, 'bookings.txt'), 'a') as f:
            f.write(new_booking)
        return redirect(url_for('pt_booking_confirmation', booking_id=booking_id))
    return render_template('pt_booking.html', trainers=trainers)
@app.route('/pt-booking-confirmation/<booking_id>')
def pt_booking_confirmation(booking_id):
    bookings = read_bookings()
    booking = next((b for b in bookings if b['booking_id'] == booking_id), None)
    if not booking:
        return "Booking not found", 404
    trainers = read_trainers()
    trainer = next((t for t in trainers if t['trainer_id'] == booking['trainer_id']), None)
    return render_template('pt_booking_confirmation.html', booking=booking, trainer=trainer)
@app.route('/workout-records')
def workout_records():
    workouts = read_workouts()
    filter_type = request.args.get('filter', '')
    if filter_type:
        workouts = [w for w in workouts if w['workout_type'].lower() == filter_type.lower()]
    return render_template('workout_records.html', workouts=workouts, filter_type=filter_type)
@app.route('/log-workout', methods=['GET', 'POST'])
def log_workout():
    if request.method == 'POST':
        member_name = request.form.get('member_name', 'Guest')
        workout_type = request.form.get('workout_type')
        workout_duration = request.form.get('workout_duration')
        calories_burned = request.form.get('calories_burned')
        workout_notes = request.form.get('workout_notes')
        workouts = read_workouts()
        workout_id = str(int(workouts[-1]['workout_id']) + 1) if workouts else '1'
        from datetime import date
        workout_date = date.today().isoformat()
        new_workout = f"{workout_id}|{member_name}|{workout_type}|{workout_date}|{workout_duration}|{calories_burned}|{workout_notes}\n"
        with open(os.path.join(DATA_DIR, 'workouts.txt'), 'a') as f:
            f.write(new_workout)
        return redirect(url_for('workout_records'))
    return render_template('log_workout.html')
if __name__ == '__main__':
    app.run(debug=True)