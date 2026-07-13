from flask import Flask, render_template, request, redirect, url_for
from typing import List, Dict, Optional
import os
from datetime import datetime

app = Flask(__name__)
DATA_DIR = 'data'

# Helper functions for file operations

def read_pipe_delimited_file(filename: str, fieldnames: List[str]) -> List[Dict[str, str]]:
    filepath = os.path.join(DATA_DIR, filename)
    records = []
    if not os.path.exists(filepath):
        return records
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != len(fieldnames):
                continue  # skip malformed lines
            record = {fieldnames[i]: parts[i] for i in range(len(fieldnames))}
            records.append(record)
    return records


def write_pipe_delimited_file(filename: str, fieldnames: List[str], records: List[Dict[str, str]]) -> None:
    filepath = os.path.join(DATA_DIR, filename)
    os.makedirs(DATA_DIR, exist_ok=True)  # Ensure data directory exists before writing
    with open(filepath, 'w', encoding='utf-8') as f:
        for record in records:
            line = '|'.join(record.get(field, '') for field in fieldnames)
            f.write(line + '\n')


# Route: / -> root_redirect
@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))


# Route: /dashboard -> dashboard
@app.route('/dashboard')
def dashboard():
    member_status = "Welcome back, valued member! Enjoy your workout."
    return render_template('dashboard.html', member_status=member_status)


# Route: /memberships -> membership_plans
@app.route('/memberships')
def membership_plans():
    filter_type = request.args.get('filter_type')
    memberships = read_pipe_delimited_file('memberships.txt', [
        'membership_id', 'plan_name', 'price', 'billing_cycle', 'features', 'max_classes'
    ])
    if filter_type:
        filter_type = filter_type.strip()
        memberships = [m for m in memberships if filter_type.lower() in m['plan_name'].lower()]
    else:
        filter_type = None
    return render_template('membership_plans.html', memberships=memberships, filter_type=filter_type)


# Route: /membership/<plan_id> -> plan_details
@app.route('/membership/<plan_id>')
def plan_details(plan_id):
    memberships = read_pipe_delimited_file('memberships.txt', [
        'membership_id', 'plan_name', 'price', 'billing_cycle', 'features', 'max_classes'
    ])
    plan = None
    for m in memberships:
        if m['membership_id'] == plan_id:
            plan = m
            break
    if plan is None:
        return "Plan not found", 404

    reviews = [
        {"reviewer": "Alice", "comment": "Great value for the price!"},
        {"reviewer": "Bob", "comment": "Loved the personal training sessions included."}
    ]
    return render_template('plan_details.html', plan=plan, reviews=reviews)


# Route: /classes -> class_schedule
@app.route('/classes')
def class_schedule():
    class_filter = request.args.get('class_filter')
    search_query = request.args.get('search_query')

    classes = read_pipe_delimited_file('classes.txt', [
        'class_id', 'class_name', 'trainer_id', 'class_type', 'schedule_day', 'schedule_time', 'capacity', 'duration'
    ])

    if class_filter:
        classes = [c for c in classes if c['class_type'].lower() == class_filter.lower()]
    else:
        class_filter = None

    if search_query:
        sq = search_query.lower()
        classes = [c for c in classes if sq in c['class_name'].lower() or sq in c['trainer_id'].lower()]
    else:
        search_query = None

    return render_template('class_schedule.html', classes=classes, class_filter=class_filter, search_query=search_query)


# Route: /trainers -> trainer_profiles
@app.route('/trainers')
def trainer_profiles():
    specialty_filter = request.args.get('specialty_filter')
    search_query = request.args.get('search_query')

    trainers = read_pipe_delimited_file('trainers.txt', [
        'trainer_id', 'name', 'specialty', 'certifications', 'experience_years', 'bio'
    ])

    if specialty_filter:
        sf = specialty_filter.lower()
        trainers = [t for t in trainers if sf in t['specialty'].lower()]
    else:
        specialty_filter = None

    if search_query:
        sq = search_query.lower()
        trainers = [t for t in trainers if sq in t['name'].lower() or sq in t['specialty'].lower()]
    else:
        search_query = None

    return render_template('trainer_profiles.html', trainers=trainers, specialty_filter=specialty_filter, search_query=search_query)


# Route: /trainer/<trainer_id> -> trainer_detail
@app.route('/trainer/<trainer_id>')
def trainer_detail(trainer_id):
    trainers = read_pipe_delimited_file('trainers.txt', [
        'trainer_id', 'name', 'specialty', 'certifications', 'experience_years', 'bio'
    ])
    trainer = None
    for t in trainers:
        if t['trainer_id'] == trainer_id:
            trainer = t
            break
    if trainer is None:
        return "Trainer not found", 404

    reviews = [
        {"reviewer": "Client1", "comment": "Very motivating and professional."},
        {"reviewer": "Client2", "comment": "Helped me improve my form drastically!"}
    ]
    return render_template('trainer_detail.html', trainer=trainer, reviews=reviews)


# Route: /booking -> pt_booking
@app.route('/booking', methods=['GET', 'POST'])
def pt_booking():
    trainers = read_pipe_delimited_file('trainers.txt', ['trainer_id', 'name', 'specialty', 'certifications', 'experience_years', 'bio'])
    minimal_trainers = [{"trainer_id": t['trainer_id'], "name": t['name']} for t in trainers]
    booking_confirmation = None

    if request.method == 'POST':
        member_name = "Guest Member"
        trainer_id = request.form.get('select_trainer')
        booking_date = request.form.get('session_date')
        booking_time = request.form.get('session_time')
        duration = request.form.get('session_duration')

        if not trainer_id or not booking_date or not booking_time or not duration:
            booking_confirmation = "Please fill in all booking fields."
        else:
            bookings = read_pipe_delimited_file('bookings.txt', [
                'booking_id', 'member_name', 'trainer_id', 'booking_date', 'booking_time', 'duration_minutes', 'status'
            ])
            new_id = 1
            if bookings:
                existing_ids = [int(b['booking_id']) for b in bookings if b['booking_id'].isdigit()]
                if existing_ids:
                    new_id = max(existing_ids) + 1

            new_booking = {
                'booking_id': str(new_id),
                'member_name': member_name,
                'trainer_id': trainer_id,
                'booking_date': booking_date,
                'booking_time': booking_time,
                'duration_minutes': duration,
                'status': 'Pending'
            }
            write_pipe_delimited_file('bookings.txt', [
                'booking_id', 'member_name', 'trainer_id', 'booking_date', 'booking_time', 'duration_minutes', 'status'
            ], bookings + [new_booking])
            booking_confirmation = f"Booking confirmed for {booking_date} at {booking_time}."

    return render_template('booking.html', trainers=minimal_trainers, booking_confirmation=booking_confirmation)


# Route: /workouts -> workout_records
@app.route('/workouts')
def workout_records():
    workout_filter = request.args.get('workout_filter')
    workouts = read_pipe_delimited_file('workouts.txt', [
        'workout_id', 'member_name', 'workout_type', 'workout_date', 'duration_minutes', 'calories_burned', 'notes'
    ])
    if workout_filter:
        workouts = [w for w in workouts if w['workout_type'].lower() == workout_filter.lower()]
    else:
        workout_filter = None
    return render_template('workouts.html', workouts=workouts, workout_filter=workout_filter)


# Route: /workouts/log -> log_workout
@app.route('/workouts/log', methods=['GET', 'POST'])
def log_workout():
    submission_status = None
    if request.method == 'POST':
        member_name = "Guest Member"
        workout_type = request.form.get('workout_type')
        duration = request.form.get('workout_duration')
        calories = request.form.get('calories_burned')
        notes = request.form.get('workout_notes')

        if not workout_type or not duration or not calories:
            submission_status = "Please fill in all required fields."
        else:
            workouts = read_pipe_delimited_file('workouts.txt', [
                'workout_id', 'member_name', 'workout_type', 'workout_date', 'duration_minutes', 'calories_burned', 'notes'
            ])
            new_id = 1
            if workouts:
                existing_ids = [int(w['workout_id']) for w in workouts if w['workout_id'].isdigit()]
                if existing_ids:
                    new_id = max(existing_ids) + 1

            workout_date = datetime.now().strftime('%Y-%m-%d')

            new_workout = {
                'workout_id': str(new_id),
                'member_name': member_name,
                'workout_type': workout_type,
                'workout_date': workout_date,
                'duration_minutes': duration,
                'calories_burned': calories,
                'notes': notes if notes else ''
            }
            write_pipe_delimited_file('workouts.txt', [
                'workout_id', 'member_name', 'workout_type', 'workout_date', 'duration_minutes', 'calories_burned', 'notes'
            ], workouts + [new_workout])
            submission_status = "Workout logged successfully."
    return render_template('log_workout.html', submission_status=submission_status)


if __name__ == '__main__':
    app.run(debug=True)
