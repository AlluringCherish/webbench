from flask import Flask, render_template, redirect, url_for, request
import os
from typing import List, Dict

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

# Data file paths
MEMBERSHIPS_FILE = 'data/memberships.txt'
CLASSES_FILE = 'data/classes.txt'
TRAINERS_FILE = 'data/trainers.txt'
BOOKINGS_FILE = 'data/bookings.txt'
WORKOUTS_FILE = 'data/workouts.txt'

# Utility functions for reading/writing data

def read_memberships() -> List[Dict]:
    memberships = []
    try:
        with open(MEMBERSHIPS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                fields = line.split('|')
                membership_id = int(fields[0])
                plan_name = fields[1]
                price = float(fields[2])
                billing_cycle = fields[3]
                features = fields[4]
                max_classes = fields[5]
                memberships.append({
                    'membership_id': membership_id,
                    'plan_name': plan_name,
                    'price': price,
                    'billing_cycle': billing_cycle,
                    'features': features,
                    'max_classes': max_classes
                })
    except Exception as e:
        print(f"Error reading memberships file: {e}")
    return memberships


def read_classes() -> List[Dict]:
    classes = []
    try:
        with open(CLASSES_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                fields = line.split('|')
                class_id = int(fields[0])
                class_name = fields[1]
                trainer_id = int(fields[2])
                class_type = fields[3]
                schedule_day = fields[4]
                schedule_time = fields[5]
                capacity = int(fields[6])
                duration = int(fields[7])
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
    except Exception as e:
        print(f"Error reading classes file: {e}")
    return classes


def read_trainers() -> List[Dict]:
    trainers = []
    try:
        with open(TRAINERS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                fields = line.split('|')
                trainer_id = int(fields[0])
                name = fields[1]
                specialty = fields[2]
                certifications = fields[3]
                experience_years = int(fields[4])
                bio = fields[5]
                trainers.append({
                    'trainer_id': trainer_id,
                    'name': name,
                    'specialty': specialty,
                    'certifications': certifications,
                    'experience_years': experience_years,
                    'bio': bio
                })
    except Exception as e:
        print(f"Error reading trainers file: {e}")
    return trainers


def read_bookings() -> List[Dict]:
    bookings = []
    try:
        with open(BOOKINGS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                fields = line.split('|')
                booking_id = int(fields[0])
                member_name = fields[1]
                trainer_id = int(fields[2])
                booking_date = fields[3]
                booking_time = fields[4]
                duration_minutes = int(fields[5])
                status = fields[6]
                bookings.append({
                    'booking_id': booking_id,
                    'member_name': member_name,
                    'trainer_id': trainer_id,
                    'booking_date': booking_date,
                    'booking_time': booking_time,
                    'duration_minutes': duration_minutes,
                    'status': status
                })
    except Exception as e:
        print(f"Error reading bookings file: {e}")
    return bookings


def write_bookings(bookings: List[Dict]) -> None:
    try:
        with open(BOOKINGS_FILE, 'w', encoding='utf-8') as f:
            for b in bookings:
                line = f"{b['booking_id']}|{b['member_name']}|{b['trainer_id']}|{b['booking_date']}|{b['booking_time']}|{b['duration_minutes']}|{b['status']}\n"
                f.write(line)
    except Exception as e:
        print(f"Error writing bookings file: {e}")


def read_workouts() -> List[Dict]:
    workouts = []
    try:
        with open(WORKOUTS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                fields = line.split('|')
                workout_id = int(fields[0])
                member_name = fields[1]
                workout_type = fields[2]
                workout_date = fields[3]
                duration_minutes = int(fields[4])
                calories_burned = int(fields[5])
                notes = fields[6]
                workouts.append({
                    'workout_id': workout_id,
                    'member_name': member_name,
                    'workout_type': workout_type,
                    'workout_date': workout_date,
                    'duration_minutes': duration_minutes,
                    'calories_burned': calories_burned,
                    'notes': notes
                })
    except Exception as e:
        print(f"Error reading workouts file: {e}")
    return workouts


def write_workouts(workouts: List[Dict]) -> None:
    try:
        with open(WORKOUTS_FILE, 'w', encoding='utf-8') as f:
            for w in workouts:
                line = f"{w['workout_id']}|{w['member_name']}|{w['workout_type']}|{w['workout_date']}|{w['duration_minutes']}|{w['calories_burned']}|{w['notes']}\n"
                f.write(line)
    except Exception as e:
        print(f"Error writing workouts file: {e}")


# Root route redirects to dashboard
@app.route('/', methods=['GET'])
def root_redirect():
    return redirect(url_for('dashboard'))


@app.route('/dashboard', methods=['GET'])
def dashboard():
    # For demonstration, member_status is a static string; featured_classes: latest 3 classes; quick_links: static list
    member_status = "Active Member - Premium Plan"
    classes_all = read_classes()
    featured_classes = classes_all[:3] if len(classes_all) >= 3 else classes_all
    quick_links = [
        {'name': 'Memberships', 'url': url_for('memberships')},
        {'name': 'Classes', 'url': url_for('classes')},
        {'name': 'Book Trainer', 'url': url_for('booking')}
    ]
    return render_template('dashboard.html', member_status=member_status, featured_classes=featured_classes, quick_links=quick_links)


@app.route('/memberships', methods=['GET'])
def memberships():
    memberships_list = read_memberships()
    membership_types = ['Basic', 'Premium', 'Elite']
    return render_template('memberships.html', memberships_list=memberships_list, membership_types=membership_types)


@app.route('/memberships/<int:plan_id>', methods=['GET'])
def plan_details(plan_id: int):
    memberships_list = read_memberships()
    plan = next((m for m in memberships_list if m['membership_id'] == plan_id), None)

    # For reviews, no data file given - assume empty list for now
    reviews = []  # Reviews data is not specified.

    if plan is None:
        # Could 404 or redirect to memberships; safer redirect
        return redirect(url_for('memberships'))

    return render_template('plan_details.html', plan=plan, reviews=reviews)


@app.route('/classes', methods=['GET'])
def classes():
    classes_list = read_classes()
    # Extract unique class types
    class_types = sorted(list(set(c['class_type'] for c in classes_list)))
    return render_template('classes.html', classes_list=classes_list, class_types=class_types)


@app.route('/trainers', methods=['GET'])
def trainers():
    trainers_list = read_trainers()
    specialties = sorted(list(set(t['specialty'] for t in trainers_list)))
    return render_template('trainers.html', trainers_list=trainers_list, specialties=specialties)


@app.route('/trainer/<int:trainer_id>', methods=['GET'])
def trainer_detail(trainer_id: int):
    trainers_list = read_trainers()
    trainer = next((t for t in trainers_list if t['trainer_id'] == trainer_id), None)

    # Reviews not specified data file - empty list
    reviews = []

    if trainer is None:
        return redirect(url_for('trainers'))

    return render_template('trainer_detail.html', trainer=trainer, reviews=reviews)


@app.route('/booking', methods=['GET', 'POST'])
def booking():
    trainers_list = read_trainers()
    # For available_times, we define fixed slots (for example purposes)
    available_times = ["06:00", "08:00", "10:00", "12:00", "14:00", "16:00", "18:00", "20:00"]
    booking_success = False

    if request.method == 'POST':
        # Expected form fields:
        # member_name, trainer_id, booking_date (YYYY-MM-DD), booking_time (HH:MM 24hr), duration_minutes
        try:
            member_name = request.form['member_name'].strip()
            trainer_id = int(request.form['trainer_id'])
            booking_date = request.form['booking_date'].strip()
            booking_time = request.form['booking_time'].strip()
            duration_minutes = int(request.form['duration_minutes'])

            bookings = read_bookings()
            next_id = max((b['booking_id'] for b in bookings), default=0) + 1

            new_booking = {
                'booking_id': next_id,
                'member_name': member_name,
                'trainer_id': trainer_id,
                'booking_date': booking_date,
                'booking_time': booking_time,
                'duration_minutes': duration_minutes,
                'status': 'Pending'
            }

            bookings.append(new_booking)
            write_bookings(bookings)
            booking_success = True
        except Exception as e:
            print(f"Error processing booking POST: {e}")
            booking_success = False

    return render_template('booking.html', trainers_list=trainers_list, available_times=available_times, booking_success=booking_success)


@app.route('/workouts', methods=['GET'])
def workouts():
    workouts_list = read_workouts()
    workout_types = sorted(list(set(w['workout_type'] for w in workouts_list)))
    return render_template('workouts.html', workouts_list=workouts_list, workout_types=workout_types)


@app.route('/log_workout', methods=['GET', 'POST'])
def log_workout():
    workout_types = ["Cardio", "Strength", "Class", "Flexibility", "Balance", "Endurance"]
    log_success = False

    if request.method == 'POST':
        try:
            # Form fields: member_name, workout_type, workout_date, duration_minutes, calories_burned, notes
            member_name = request.form.get('member_name', '').strip()
            workout_type = request.form['workout_type']
            workout_date = request.form['workout_date'].strip() if 'workout_date' in request.form else ''
            if not workout_date:
                from datetime import date
                workout_date = date.today().isoformat()
            duration_minutes = int(request.form['duration_minutes'])
            calories_burned = int(request.form['calories_burned'])
            notes = request.form.get('notes', '').strip()

            workouts = read_workouts()
            next_id = max((w['workout_id'] for w in workouts), default=0) + 1

            new_workout = {
                'workout_id': next_id,
                'member_name': member_name,
                'workout_type': workout_type,
                'workout_date': workout_date,
                'duration_minutes': duration_minutes,
                'calories_burned': calories_burned,
                'notes': notes
            }

            workouts.append(new_workout)
            write_workouts(workouts)
            log_success = True
        except Exception as e:
            print(f"Error processing log_workout POST: {e}")
            log_success = False

    return render_template('log_workout.html', workout_types=workout_types, log_success=log_success)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
