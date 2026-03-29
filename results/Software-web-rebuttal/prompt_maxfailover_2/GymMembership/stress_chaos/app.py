from flask import Flask, render_template, request, redirect, url_for, abort

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

# Helper function to load memberships data

def load_memberships():
    memberships = []
    try:
        with open('data/memberships.txt', 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 6:
                    continue
                membership = {
                    'membership_id': int(parts[0]),
                    'plan_name': parts[1],
                    'price': float(parts[2]),
                    'billing_cycle': parts[3],
                    'features': parts[4],
                    'max_classes': parts[5],
                }
                memberships.append(membership)
    except Exception:
        memberships = []
    return memberships

# Helper to find membership by id

def get_membership_by_id(membership_id):
    memberships = load_memberships()
    for m in memberships:
        if m['membership_id'] == membership_id:
            return m
    return None

# Helper function to load classes data

def load_classes():
    classes = []
    try:
        with open('data/classes.txt', 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 8:
                    continue
                cls = {
                    'class_id': int(parts[0]),
                    'class_name': parts[1],
                    'trainer_id': int(parts[2]),
                    'class_type': parts[3],
                    'schedule_day': parts[4],
                    'schedule_time': parts[5],
                    'capacity': int(parts[6]),
                    'duration': int(parts[7]),
                }
                classes.append(cls)
    except Exception:
        classes = []
    return classes

# Helper function to load trainers data

def load_trainers():
    trainers = []
    try:
        with open('data/trainers.txt', 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 6:
                    continue
                trainer = {
                    'trainer_id': int(parts[0]),
                    'name': parts[1],
                    'specialty': parts[2],
                    'certifications': parts[3],
                    'experience_years': int(parts[4]),
                    'bio': parts[5],
                }
                trainers.append(trainer)
    except Exception:
        trainers = []
    return trainers

# Helper to find trainer by id

def get_trainer_by_id(trainer_id):
    trainers = load_trainers()
    for t in trainers:
        if t['trainer_id'] == trainer_id:
            return t
    return None

# Helper function to load bookings data

def load_bookings():
    bookings = []
    try:
        with open('data/bookings.txt', 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 7:
                    continue
                booking = {
                    'booking_id': int(parts[0]),
                    'member_name': parts[1],
                    'trainer_id': int(parts[2]),
                    'booking_date': parts[3],
                    'booking_time': parts[4],
                    'duration_minutes': int(parts[5]),
                    'status': parts[6],
                }
                bookings.append(booking)
    except Exception:
        bookings = []
    return bookings

# Helper function to load workouts data

def load_workouts():
    workouts = []
    try:
        with open('data/workouts.txt', 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 7:
                    continue
                workout = {
                    'workout_id': int(parts[0]),
                    'member_name': parts[1],
                    'workout_type': parts[2],
                    'workout_date': parts[3],
                    'duration_minutes': int(parts[4]),
                    'calories_burned': int(parts[5]),
                    'notes': parts[6],
                }
                workouts.append(workout)
    except Exception:
        workouts = []
    return workouts

# Save booking - append new booking to file

def save_booking(booking_data):
    try:
        all_bookings = load_bookings()
        max_id = max((b['booking_id'] for b in all_bookings), default=0)
        new_id = max_id + 1
        booking_data['booking_id'] = new_id
        line = '|'.join([
            str(booking_data['booking_id']),
            booking_data['member_name'],
            str(booking_data['trainer_id']),
            booking_data['booking_date'],
            booking_data['booking_time'],
            str(booking_data['duration_minutes']),
            booking_data['status']
        ])
        with open('data/bookings.txt', 'a', encoding='utf-8') as f:
            f.write(line + '\n')
        return True
    except Exception:
        return False

# Save workout - append new workout to file

def save_workout(workout_data):
    try:
        all_workouts = load_workouts()
        max_id = max((w['workout_id'] for w in all_workouts), default=0)
        new_id = max_id + 1
        workout_data['workout_id'] = new_id
        line = '|'.join([
            str(workout_data['workout_id']),
            workout_data['member_name'],
            workout_data['workout_type'],
            workout_data['workout_date'],
            str(workout_data['duration_minutes']),
            str(workout_data['calories_burned']),
            workout_data['notes']
        ])
        with open('data/workouts.txt', 'a', encoding='utf-8') as f:
            f.write(line + '\n')
        return True
    except Exception:
        return False

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    # Static content no context variables
    return render_template('dashboard.html')

@app.route('/memberships')
def memberships():
    plans = load_memberships()
    return render_template('memberships.html', plans=plans)

@app.route('/plan/<int:plan_id>')
def plan_details(plan_id):
    plan = get_membership_by_id(plan_id)
    if not plan:
        abort(404)
    reviews = []  # No reviews support specified
    return render_template('plan_details.html', plan=plan, reviews=reviews)

@app.route('/schedule')
def class_schedule():
    classes = load_classes()
    return render_template('class_schedule.html', classes=classes)

@app.route('/trainers')
def trainers():
    trainers_list = load_trainers()
    return render_template('trainers.html', trainers=trainers_list)

@app.route('/trainer/<int:trainer_id>')
def trainer_detail(trainer_id):
    trainer = get_trainer_by_id(trainer_id)
    if not trainer:
        abort(404)
    reviews = []  # Placeholder for reviews
    return render_template('trainer_detail.html', trainer=trainer, reviews=reviews)

@app.route('/booking', methods=['GET', 'POST'])
def booking():
    trainers_list = load_trainers()
    if request.method == 'POST':
        try:
            select_trainer = int(request.form.get('select_trainer', ''))
            session_date = request.form.get('session_date', '').strip()
            session_time = request.form.get('session_time', '').strip()
            session_duration = int(request.form.get('session_duration', ''))
            # Validate inputs
            if not session_date or not session_time or session_duration <= 0:
                return render_template('booking.html', trainers=trainers_list, feedback='Invalid input. Please fill all fields.')
            # Save booking data
            booking_data = {
                'member_name': 'Member',  # Placeholder, as member info not specified
                'trainer_id': select_trainer,
                'booking_date': session_date,
                'booking_time': session_time,
                'duration_minutes': session_duration,
                'status': 'Pending',
            }
            success = save_booking(booking_data)
            if success:
                return render_template('booking.html', trainers=trainers_list, feedback='Booking submitted successfully.')
            else:
                return render_template('booking.html', trainers=trainers_list, feedback='Failed to save booking.')
        except Exception:
            return render_template('booking.html', trainers=trainers_list, feedback='Invalid form data.')
    else:
        # GET
        return render_template('booking.html', trainers=trainers_list)

@app.route('/workouts')
def workout_records():
    workouts = load_workouts()
    return render_template('workouts.html', workouts=workouts)

@app.route('/log_workout', methods=['GET', 'POST'])
def log_workout():
    if request.method == 'POST':
        workout_type = request.form.get('workout_type', '').strip()
        try:
            workout_duration = int(request.form.get('workout_duration', '0'))
            calories_burned = int(request.form.get('calories_burned', '0'))
        except ValueError:
            workout_duration = 0
            calories_burned = 0
        workout_notes = request.form.get('workout_notes', '').strip()

        # Placeholder member_name
        member_name = 'Member'

        if not workout_type or workout_duration <= 0:
            return render_template('log_workout.html', feedback='Please provide valid workout type and duration.')

        workout_data = {
            'member_name': member_name,
            'workout_type': workout_type,
            'workout_date': '',  # No date provided in form, no spec for date support; could be today? Leave empty.
            'duration_minutes': workout_duration,
            'calories_burned': calories_burned,
            'notes': workout_notes,
        }
        success = save_workout(workout_data)
        if success:
            return render_template('log_workout.html', feedback='Workout logged successfully.')
        else:
            return render_template('log_workout.html', feedback='Failed to log workout.')
    else:
        # GET
        return render_template('log_workout.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
