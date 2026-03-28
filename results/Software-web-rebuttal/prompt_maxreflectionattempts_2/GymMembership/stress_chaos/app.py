from flask import Flask, render_template, redirect, url_for, request
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Helper functions to load data from text files

def load_memberships():
    memberships = []
    path = os.path.join(DATA_DIR, 'memberships.txt')
    if not os.path.isfile(path):
        return memberships
    with open(path, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split('|')
            if len(parts) == 6:
                membership_id = int(parts[0])
                plan_name = parts[1]
                try:
                    price = float(parts[2])
                except ValueError:
                    price = 0.0
                billing_cycle = parts[3]
                features = parts[4]
                max_classes = parts[5]
                # max_classes may be int or str 'unlimited'
                try:
                    max_classes_val = int(max_classes)
                except:
                    max_classes_val = max_classes
                memberships.append({
                    'membership_id': membership_id,
                    'plan_name': plan_name,
                    'price': price,
                    'billing_cycle': billing_cycle,
                    'features': features,
                    'max_classes': max_classes_val
                })
    return memberships


def load_classes():
    classes = []
    path = os.path.join(DATA_DIR, 'classes.txt')
    if not os.path.isfile(path):
        return classes
    with open(path, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split('|')
            if len(parts) == 8:
                class_id = int(parts[0])
                class_name = parts[1]
                trainer_id = int(parts[2])
                class_type = parts[3]
                schedule_day = parts[4]
                schedule_time = parts[5]
                capacity = int(parts[6])
                duration = int(parts[7])
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


def load_trainers():
    trainers = []
    path = os.path.join(DATA_DIR, 'trainers.txt')
    if not os.path.isfile(path):
        return trainers
    with open(path, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split('|')
            if len(parts) == 6:
                trainer_id = int(parts[0])
                name = parts[1]
                specialty = parts[2]
                certifications = parts[3]
                try:
                    experience_years = int(parts[4])
                except ValueError:
                    experience_years = 0
                bio = parts[5]
                trainers.append({
                    'trainer_id': trainer_id,
                    'name': name,
                    'specialty': specialty,
                    'certifications': certifications,
                    'experience_years': experience_years,
                    'bio': bio
                })
    return trainers


def load_bookings():
    bookings = []
    path = os.path.join(DATA_DIR, 'bookings.txt')
    if not os.path.isfile(path):
        return bookings
    with open(path, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split('|')
            if len(parts) == 7:
                try:
                    booking_id = int(parts[0])
                    member_name = parts[1]
                    trainer_id = int(parts[2])
                    booking_date = parts[3]
                    booking_time = parts[4]
                    duration_minutes = int(parts[5])
                    status = parts[6]
                    bookings.append({
                        'booking_id': booking_id,
                        'member_name': member_name,
                        'trainer_id': trainer_id,
                        'booking_date': booking_date,
                        'booking_time': booking_time,
                        'duration_minutes': duration_minutes,
                        'status': status
                    })
                except ValueError:
                    continue
    return bookings


def save_bookings(bookings):
    path = os.path.join(DATA_DIR, 'bookings.txt')
    try:
        with open(path, 'w', encoding='utf-8') as file:
            for b in bookings:
                # booking_id|member_name|trainer_id|booking_date|booking_time|duration_minutes|status
                line = f"{b['booking_id']}|{b['member_name']}|{b['trainer_id']}|{b['booking_date']}|{b['booking_time']}|{b['duration_minutes']}|{b['status']}\n"
                file.write(line)
    except Exception:
        pass


def load_workouts():
    workouts = []
    path = os.path.join(DATA_DIR, 'workouts.txt')
    if not os.path.isfile(path):
        return workouts
    with open(path, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split('|')
            if len(parts) == 7:
                try:
                    workout_id = int(parts[0])
                    member_name = parts[1]
                    workout_type = parts[2]
                    workout_date = parts[3]
                    duration_minutes = int(parts[4])
                    calories_burned = int(parts[5])
                    notes = parts[6]
                    workouts.append({
                        'workout_id': workout_id,
                        'member_name': member_name,
                        'workout_type': workout_type,
                        'workout_date': workout_date,
                        'duration_minutes': duration_minutes,
                        'calories_burned': calories_burned,
                        'notes': notes
                    })
                except ValueError:
                    continue
    return workouts


def save_workouts(workouts):
    path = os.path.join(DATA_DIR, 'workouts.txt')
    try:
        with open(path, 'w', encoding='utf-8') as file:
            for w in workouts:
                # workout_id|member_name|workout_type|workout_date|duration_minutes|calories_burned|notes
                line = f"{w['workout_id']}|{w['member_name']}|{w['workout_type']}|{w['workout_date']}|{w['duration_minutes']}|{w['calories_burned']}|{w['notes']}\n"
                file.write(line)
    except Exception:
        pass


# Placeholder for member_status, could be extended later
member_status_global = "Active Member - Welcome back!"
member_name_global = "John Doe"  # Fixed member name for logged in user context in workouts and booking


@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    # member_status: str
    member_status = member_status_global

    # featured_classes: list of dict
    classes = load_classes()
    trainers = load_trainers()

    # Select some featured classes, e.g. first 3
    featured_classes = []
    for c in classes[:3]:
        trainer_name = next((t['name'] for t in trainers if t['trainer_id'] == c['trainer_id']), 'Unknown')
        featured_classes.append({
            'class_name': c['class_name'],
            'schedule_time': f"{c['schedule_day']} {c['schedule_time']}",
            'trainer_name': trainer_name
        })

    # quick_nav_links: dict
    quick_nav_links = {
        'Browse Memberships': url_for('memberships'),
        'View Schedule': url_for('class_schedule'),
        'Book Trainer': url_for('pt_booking')
    }

    return render_template('dashboard.html', 
                           member_status=member_status, 
                           featured_classes=featured_classes, 
                           quick_nav_links=quick_nav_links)


@app.route('/memberships')
def memberships():
    plans = load_memberships()
    return render_template('memberships.html', plans=plans)


@app.route('/plan/<int:plan_id>')
def plan_details(plan_id):
    plans = load_memberships()
    plan = next((p for p in plans if p['membership_id'] == plan_id), None)

    # No reviews data file specified, so reviews always empty list
    reviews = []

    return render_template('plan_details.html', plan=plan, reviews=reviews)


@app.route('/schedule')
def class_schedule():
    classes = load_classes()

    # Extract unique class_types
    class_types = sorted(set(c['class_type'] for c in classes))

    search_query = request.args.get('search_query', '').strip()
    filter_type = request.args.get('filter_type', '').strip()

    filtered_classes = classes

    # Apply search (search class_name or trainer_name)
    if search_query:
        trainers = load_trainers()
        filtered_classes = []
        for c in classes:
            trainer_name = next((t['name'] for t in trainers if t['trainer_id'] == c['trainer_id']), '')
            if search_query.lower() in c['class_name'].lower() or search_query.lower() in trainer_name.lower():
                filtered_classes.append(c)

    # Apply filter by type
    if filter_type:
        filtered_classes = [c for c in filtered_classes if c['class_type'] == filter_type]

    return render_template('class_schedule.html', 
                           classes=filtered_classes, 
                           class_types=class_types, 
                           search_query=search_query or None, 
                           filter_type=filter_type or None)


@app.route('/trainers')
def trainer_profiles():
    trainers = load_trainers()

    specialties = sorted(set(t['specialty'] for t in trainers))

    search_query = request.args.get('search_query', '').strip()
    filter_specialty = request.args.get('filter_specialty', '').strip()

    filtered_trainers = trainers

    if search_query:
        filtered_trainers = [t for t in filtered_trainers if search_query.lower() in t['name'].lower()]

    if filter_specialty:
        filtered_trainers = [t for t in filtered_trainers if t['specialty'] == filter_specialty]

    return render_template('trainer_profiles.html', 
                           trainers=filtered_trainers, 
                           specialties=specialties, 
                           search_query=search_query or None, 
                           filter_specialty=filter_specialty or None)


@app.route('/trainer/<int:trainer_id>')
def trainer_detail(trainer_id):
    trainers = load_trainers()
    trainer = next((t for t in trainers if t['trainer_id'] == trainer_id), None)

    # No trainer reviews file specified, reviews always empty list
    reviews = []

    return render_template('trainer_detail.html', 
                           trainer=trainer, 
                           reviews=reviews)


@app.route('/booking', methods=['GET', 'POST'])
def pt_booking():
    if request.method == 'GET':
        trainers = load_trainers()
        return render_template('booking.html', trainers=trainers)
    else:
        # POST - Booking submission
        member_name = member_name_global
        try:
            trainer_id = int(request.form.get('trainer_id', ''))
            booking_date = request.form.get('session_date', '')
            booking_time = request.form.get('session_time', '')
            duration = int(request.form.get('session_duration', ''))
        except ValueError:
            booking_result = "Invalid input data."
            return render_template('booking.html', booking_result=booking_result)

        # Validate date format YYYY-MM-DD
        try:
            datetime.strptime(booking_date, '%Y-%m-%d')
        except ValueError:
            booking_result = "Invalid date format. Use YYYY-MM-DD."
            return render_template('booking.html', booking_result=booking_result)

        # Validate time format HH:MM
        try:
            datetime.strptime(booking_time, '%H:%M')
        except ValueError:
            booking_result = "Invalid time format. Use HH:MM 24hr."
            return render_template('booking.html', booking_result=booking_result)

        # Load existing bookings
        bookings = load_bookings()

        # Generate new booking_id
        new_id = max((b['booking_id'] for b in bookings), default=0) + 1

        # Add new booking with Pending status
        new_booking = {
            'booking_id': new_id,
            'member_name': member_name,
            'trainer_id': trainer_id,
            'booking_date': booking_date,
            'booking_time': booking_time,
            'duration_minutes': duration,
            'status': 'Pending'
        }
        bookings.append(new_booking)

        # Save bookings
        save_bookings(bookings)

        booking_result = f"Booking submitted successfully for {booking_date} at {booking_time}."
        return render_template('booking.html', booking_result=booking_result)


@app.route('/workouts')
def workout_records():
    workouts = load_workouts()

    workout_types = sorted(set(w['workout_type'] for w in workouts))

    filter_type = request.args.get('filter_type', '').strip()

    filtered_workouts = workouts

    if filter_type:
        filtered_workouts = [w for w in filtered_workouts if w['workout_type'] == filter_type]

    return render_template('workout_records.html', 
                           workouts=filtered_workouts, 
                           workout_types=workout_types, 
                           filter_type=filter_type or None)


@app.route('/log_workout', methods=['GET', 'POST'])
def log_workout():
    if request.method == 'GET':
        return render_template('log_workout.html')
    else:
        member_name = member_name_global

        workout_type = request.form.get('workout_type','').strip()
        workout_duration_raw = request.form.get('workout_duration','').strip()
        calories_burned_raw = request.form.get('calories_burned','').strip()
        workout_notes = request.form.get('workout_notes','').strip()

        if not workout_type or not workout_duration_raw or not calories_burned_raw:
            log_result = "Please fill in all required fields."
            return render_template('log_workout.html', log_result=log_result)

        try:
            workout_duration = int(workout_duration_raw)
            calories_burned = int(calories_burned_raw)
        except ValueError:
            log_result = "Duration and Calories Burned must be numbers."
            return render_template('log_workout.html', log_result=log_result)

        workouts = load_workouts()

        new_id = max((w['workout_id'] for w in workouts), default=0) + 1

        today_date = datetime.now().strftime('%Y-%m-%d')

        new_workout = {
            'workout_id': new_id,
            'member_name': member_name,
            'workout_type': workout_type,
            'workout_date': today_date,
            'duration_minutes': workout_duration,
            'calories_burned': calories_burned,
            'notes': workout_notes
        }

        workouts.append(new_workout)

        save_workouts(workouts)

        log_result = "Workout logged successfully."
        return render_template('log_workout.html', log_result=log_result)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
