from flask import Flask, render_template, redirect, url_for, request
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Helper functions for reading data files

def read_memberships():
    memberships_path = os.path.join(DATA_DIR, 'memberships.txt')
    plans = []
    try:
        with open(memberships_path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 6:
                    continue
                membership_id = int(parts[0])
                plan_name = parts[1]
                price = float(parts[2])
                billing_cycle = parts[3]
                features = parts[4]
                max_classes = parts[5]
                plan = {
                    'membership_id': membership_id,
                    'plan_name': plan_name,
                    'price': price,
                    'billing_cycle': billing_cycle,
                    'features': features,
                    'max_classes': max_classes
                }
                plans.append(plan)
    except Exception:
        # Return empty list if error
        plans = []
    return plans


def read_classes():
    classes_path = os.path.join(DATA_DIR, 'classes.txt')
    classes = []
    try:
        with open(classes_path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 8:
                    continue
                class_id = int(parts[0])
                class_name = parts[1]
                trainer_id = int(parts[2])
                class_type = parts[3]
                schedule_day = parts[4]
                schedule_time = parts[5]
                capacity = int(parts[6])
                duration = int(parts[7])
                c = {
                    'class_id': class_id,
                    'class_name': class_name,
                    'trainer_id': trainer_id,
                    'class_type': class_type,
                    'schedule_day': schedule_day,
                    'schedule_time': schedule_time,
                    'capacity': capacity,
                    'duration': duration
                }
                classes.append(c)
    except Exception:
        classes = []
    return classes


def read_trainers():
    trainers_path = os.path.join(DATA_DIR, 'trainers.txt')
    trainers = []
    try:
        with open(trainers_path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 6:
                    continue
                trainer_id = int(parts[0])
                name = parts[1]
                specialty = parts[2]
                certifications = parts[3]
                experience_years = int(parts[4])
                bio = parts[5]
                t = {
                    'trainer_id': trainer_id,
                    'name': name,
                    'specialty': specialty,
                    'certifications': certifications,
                    'experience_years': experience_years,
                    'bio': bio
                }
                trainers.append(t)
    except Exception:
        trainers = []
    return trainers


def read_bookings():
    bookings_path = os.path.join(DATA_DIR, 'bookings.txt')
    bookings = []
    try:
        with open(bookings_path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 7:
                    continue
                booking_id = int(parts[0])
                member_name = parts[1]
                trainer_id = int(parts[2])
                booking_date = parts[3]
                booking_time = parts[4]
                duration_minutes = int(parts[5])
                status = parts[6]
                b = {
                    'booking_id': booking_id,
                    'member_name': member_name,
                    'trainer_id': trainer_id,
                    'booking_date': booking_date,
                    'booking_time': booking_time,
                    'duration_minutes': duration_minutes,
                    'status': status
                }
                bookings.append(b)
    except Exception:
        bookings = []
    return bookings


def save_booking(booking_dict):
    bookings = read_bookings()
    next_id = 1
    if bookings:
        next_id = max(b['booking_id'] for b in bookings) + 1
    # booking_dict keys: member_name, trainer_id, booking_date, booking_time, duration_minutes, status
    new_booking_line = f"{next_id}|{booking_dict['member_name']}|{booking_dict['trainer_id']}|{booking_dict['booking_date']}|{booking_dict['booking_time']}|{booking_dict['duration_minutes']}|{booking_dict['status']}" + "\n"
    try:
        with open(os.path.join(DATA_DIR, 'bookings.txt'), 'a', encoding='utf-8') as f:
            f.write(new_booking_line)
        return True
    except Exception:
        return False


def read_workouts():
    workouts_path = os.path.join(DATA_DIR, 'workouts.txt')
    workouts = []
    try:
        with open(workouts_path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 7:
                    continue
                workout_id = int(parts[0])
                member_name = parts[1]
                workout_type = parts[2]
                workout_date = parts[3]
                duration_minutes = int(parts[4])
                calories_burned = int(parts[5])
                notes = parts[6]
                w = {
                    'workout_id': workout_id,
                    'member_name': member_name,
                    'workout_type': workout_type,
                    'workout_date': workout_date,
                    'duration_minutes': duration_minutes,
                    'calories_burned': calories_burned,
                    'notes': notes
                }
                workouts.append(w)
    except Exception:
        workouts = []
    return workouts


def save_workout(workout_dict):
    workouts = read_workouts()
    next_id = 1
    if workouts:
        next_id = max(w['workout_id'] for w in workouts) + 1
    # workout_dict keys: member_name, workout_type, workout_date, duration_minutes, calories_burned, notes
    new_workout_line = f"{next_id}|{workout_dict['member_name']}|{workout_dict['workout_type']}|{workout_dict['workout_date']}|{workout_dict['duration_minutes']}|{workout_dict['calories_burned']}|{workout_dict['notes']}" + "\n"
    try:
        with open(os.path.join(DATA_DIR, 'workouts.txt'), 'a', encoding='utf-8') as f:
            f.write(new_workout_line)
        return True
    except Exception:
        return False

# Route Implementations

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard_page'))


@app.route('/dashboard')
def dashboard_page():
    return render_template('dashboard.html')


@app.route('/memberships')
def memberships_page():
    plans = read_memberships()
    return render_template('memberships.html', plans=plans)


@app.route('/plan/<int:plan_id>')
def plan_details_page(plan_id):
    plans = read_memberships()
    plan = None
    for p in plans:
        if p['membership_id'] == plan_id:
            plan = p
            break
    if plan is None:
        # if not found, maybe 404 or redirect back
        return redirect(url_for('memberships_page'))
    # reviews not provided in data files, pass empty list
    reviews = []
    return render_template('plan_details.html', plan=plan, reviews=reviews)


@app.route('/schedule')
def class_schedule_page():
    classes = read_classes()
    return render_template('class_schedule.html', classes=classes)


@app.route('/trainers')
def trainer_profiles_page():
    trainers = read_trainers()
    return render_template('trainer_profiles.html', trainers=trainers)


@app.route('/trainer/<int:trainer_id>')
def trainer_detail_page(trainer_id):
    trainers = read_trainers()
    trainer = None
    for t in trainers:
        if t['trainer_id'] == trainer_id:
            trainer = t
            break
    if trainer is None:
        return redirect(url_for('trainer_profiles_page'))
    reviews = []  # no data provided, send empty list
    return render_template('trainer_detail.html', trainer=trainer, reviews=reviews)


@app.route('/book-trainer', methods=['GET', 'POST'])
def pt_booking_page():
    trainers = read_trainers()
    if request.method == 'POST':
        # get form data
        member_name = request.form.get('member_name','').strip()
        trainer_id = request.form.get('trainer_id')
        booking_date = request.form.get('booking_date','').strip()
        booking_time = request.form.get('booking_time','').strip()
        duration = request.form.get('duration')

        # Validate inputs
        error = None
        if not member_name:
            error = 'Member name is required.'
        try:
            trainer_id_int = int(trainer_id)
        except:
            error = 'Invalid trainer selection.'
        if not booking_date:
            error = 'Booking date is required.'
        if not booking_time:
            error = 'Booking time is required.'
        try:
            duration_int = int(duration)
            if duration_int not in [30, 60, 90]:
                error = 'Invalid duration selected.'
        except:
            error = 'Invalid duration.'

        if error:
            return render_template('pt_booking.html', trainers=trainers, booking_result=error)

        # Save booking with status Pending
        booking_dict = {
            'member_name': member_name,
            'trainer_id': trainer_id_int,
            'booking_date': booking_date,
            'booking_time': booking_time,
            'duration_minutes': duration_int,
            'status': 'Pending'
        }
        success = save_booking(booking_dict)
        if success:
            result_msg = "Booking submitted successfully!"
        else:
            result_msg = "Error saving booking. Please try again later."
        return render_template('pt_booking.html', trainers=trainers, booking_result=result_msg)

    # GET
    return render_template('pt_booking.html', trainers=trainers)


@app.route('/workouts')
def workout_records_page():
    workouts = read_workouts()
    return render_template('workouts.html', workouts=workouts)


@app.route('/log-workout', methods=['GET', 'POST'])
def log_workout_page():
    if request.method == 'POST':
        member_name = request.form.get('member_name','').strip()
        workout_type = request.form.get('workout_type','').strip()
        workout_date = request.form.get('workout_date','').strip()
        duration_minutes = request.form.get('duration_minutes','').strip()
        calories_burned = request.form.get('calories_burned','').strip()
        notes = request.form.get('notes','').strip()

        error = None
        if not member_name:
            error = 'Member name is required.'
        if not workout_type:
            error = 'Workout type is required.'
        if not workout_date:
            error = 'Workout date is required.'
        try:
            duration_int = int(duration_minutes)
            if duration_int <= 0:
                error = 'Duration must be positive.'
        except:
            error = 'Invalid duration.'
        try:
            calories_int = int(calories_burned)
            if calories_int < 0:
                error = 'Calories burned cannot be negative.'
        except:
            error = 'Invalid calories burned.'

        if error:
            return render_template('log_workout.html', submission_result=error)

        # Save workout
        workout_dict = {
            'member_name': member_name,
            'workout_type': workout_type,
            'workout_date': workout_date,
            'duration_minutes': duration_int,
            'calories_burned': calories_int,
            'notes': notes
        }
        success = save_workout(workout_dict)
        if success:
            result_msg = 'Workout logged successfully!'
        else:
            result_msg = 'Error saving workout. Please try again later.'
        return render_template('log_workout.html', submission_result=result_msg)

    # GET
    return render_template('log_workout.html')


if __name__ == '__main__':
    app.run(debug=True, port=5000)
