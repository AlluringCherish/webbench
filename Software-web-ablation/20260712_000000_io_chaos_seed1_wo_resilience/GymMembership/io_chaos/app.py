from flask import Flask, render_template, redirect, url_for, request
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

# Helper functions to load data from files

def load_memberships():
    plans = []
    try:
        with open('data/memberships.txt', 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 6:
                    membership_id = int(parts[0])
                    plan_name = parts[1]
                    price = parts[2]
                    billing_cycle = parts[3]
                    features = parts[4]
                    max_classes = parts[5]
                    if max_classes.isdigit():
                        max_classes = int(max_classes)
                    plans.append({
                        'membership_id': membership_id,
                        'plan_name': plan_name,
                        'price': price,
                        'billing_cycle': billing_cycle,
                        'features': features,
                        'max_classes': max_classes
                    })
    except Exception:
        # If error, just return empty
        plans = []
    return plans


def load_classes():
    classes = []
    try:
        with open('data/classes.txt', 'r', encoding='utf-8') as f:
            for line in f:
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
    except Exception:
        classes = []
    return classes


def load_trainers():
    trainers = []
    try:
        with open('data/trainers.txt', 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 6:
                    trainer_id = int(parts[0])
                    name = parts[1]
                    specialty = parts[2]
                    certifications = parts[3]
                    experience_years = int(parts[4])
                    bio = parts[5]
                    trainers.append({
                        'trainer_id': trainer_id,
                        'name': name,
                        'specialty': specialty,
                        'certifications': certifications,
                        'experience_years': experience_years,
                        'bio': bio
                    })
    except Exception:
        trainers = []
    return trainers


def load_bookings():
    bookings = []
    try:
        with open('data/bookings.txt', 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 7:
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
    except Exception:
        bookings = []
    return bookings


def load_workouts():
    workouts = []
    try:
        with open('data/workouts.txt', 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 7:
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
    except Exception:
        workouts = []
    return workouts


def load_reviews_for_plan(plan_id):
    # Placeholder: No data file specified for reviews for plans, return empty list
    return []


def load_reviews_for_trainer(trainer_id):
    # Placeholder: No data file specified for trainer reviews, return empty list
    return []


def save_booking(member_name, trainer_id, booking_date, booking_time, duration_minutes, status='Pending'):
    bookings = load_bookings()
    max_id = max([b['booking_id'] for b in bookings], default=0)
    new_id = max_id + 1
    new_booking = [str(new_id), member_name, str(trainer_id), booking_date, booking_time, str(duration_minutes), status]
    try:
        with open('data/bookings.txt', 'a', encoding='utf-8') as f:
            f.write('|'.join(new_booking) + '\n')
        return True
    except Exception:
        return False


def save_workout(member_name, workout_type, workout_date, duration_minutes, calories_burned, notes):
    workouts = load_workouts()
    max_id = max([w['workout_id'] for w in workouts], default=0)
    new_id = max_id + 1
    # Use member_name as fixed 'Guest' since member auth not specified
    new_workout = [str(new_id), member_name, workout_type, workout_date, str(duration_minutes), str(calories_burned), notes]
    try:
        with open('data/workouts.txt', 'a', encoding='utf-8') as f:
            f.write('|'.join(new_workout) + '\n')
        return True
    except Exception:
        return False


# 1. Root Route
@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))


# 2. Dashboard Page
@app.route('/dashboard')
def dashboard():
    # For illustration, member_status could be a simple welcome message
    member_status = "Welcome, valued member!"
    featured_classes = []  # Optional, empty list
    return render_template('dashboard.html', member_status=member_status, featured_classes=featured_classes)


# 3. Membership Plans Page
@app.route('/memberships')
def memberships():
    plans = load_memberships()
    return render_template('memberships.html', plans=plans)


# 4. Plan Details Page
@app.route('/plan/<int:plan_id>')
def plan_details(plan_id):
    plans = load_memberships()
    plan = next((p for p in plans if p['membership_id'] == plan_id), None)
    if not plan:
        return "Plan not found.", 404
    reviews = load_reviews_for_plan(plan_id)  # Empty list as no data file provided
    return render_template('plan_details.html', plan=plan, reviews=reviews)


# 5. Class Schedule Page
@app.route('/schedule')
def class_schedule():
    classes = load_classes()
    return render_template('class_schedule.html', classes=classes)


# 6. Trainer Profiles Page
@app.route('/trainers')
def trainer_profiles():
    trainers = load_trainers()
    return render_template('trainer_profiles.html', trainers=trainers)


# 7. Trainer Detail Page
@app.route('/trainer/<int:trainer_id>')
def trainer_detail(trainer_id):
    trainers = load_trainers()
    trainer = next((t for t in trainers if t['trainer_id'] == trainer_id), None)
    if not trainer:
        return "Trainer not found.", 404
    reviews = load_reviews_for_trainer(trainer_id)  # Empty list as no data file provided
    return render_template('trainer_detail.html', trainer=trainer, reviews=reviews)


# 8. PT Booking Page
@app.route('/booking', methods=['GET', 'POST'])
def pt_booking():
    if request.method == 'GET':
        trainers = load_trainers()
        return render_template('booking.html', trainers=trainers)
    else:
        # POST
        try:
            trainer_id = int(request.form.get('trainer_id', '0'))
            session_date = request.form.get('session_date', '')
            session_time = request.form.get('session_time', '')
            session_duration = int(request.form.get('session_duration', '0'))
            # Use fixed member_name since no auth, e.g. 'Guest'
            member_name = 'Guest'
            # Save booking - status Pending as default
            saved = save_booking(member_name, trainer_id, session_date, session_time, session_duration, status='Pending')
            if saved:
                return redirect(url_for('pt_booking'))
            else:
                return "Failed to save booking.", 500
        except Exception:
            return "Invalid booking data.", 400


# 9. Workout Records Page
@app.route('/workouts')
def workout_records():
    workouts = load_workouts()
    return render_template('workout_records.html', workouts=workouts)


# 10. Log Workout Page
@app.route('/log_workout', methods=['GET', 'POST'])
def log_workout():
    if request.method == 'GET':
        return render_template('log_workout.html')
    else:
        try:
            workout_type = request.form.get('workout_type', '')
            workout_duration = int(request.form.get('workout_duration', '0'))
            calories_burned = int(request.form.get('calories_burned', '0'))
            workout_notes = request.form.get('workout_notes', '')
            member_name = 'Guest'  # Fixed member name
            from datetime import datetime
            workout_date = datetime.now().strftime('%Y-%m-%d')
            saved = save_workout(member_name, workout_type, workout_date, workout_duration, calories_burned, workout_notes)
            if saved:
                return redirect(url_for('workout_records'))
            else:
                return "Failed to save workout.", 500
        except Exception:
            return "Invalid workout data.", 400


if __name__ == '__main__':
    app.run(debug=True, port=5000)
