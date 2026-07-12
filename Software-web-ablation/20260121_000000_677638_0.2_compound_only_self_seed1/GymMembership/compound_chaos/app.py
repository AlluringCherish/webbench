from flask import Flask, render_template, redirect, url_for, request
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'


# Utility functions for reading and writing data

def read_memberships():
    plans = []
    try:
        with open('data/memberships.txt', 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts)!=6:
                    continue
                try:
                    membership_id = int(parts[0])
                    plan_name = parts[1]
                    price = parts[2]
                    billing_cycle = parts[3]
                    features = parts[4]
                    max_classes = parts[5]
                    plans.append({
                        'membership_id': membership_id,
                        'plan_name': plan_name,
                        'price': price,
                        'billing_cycle': billing_cycle,
                        'features': features,
                        'max_classes': max_classes
                    })
                except Exception:
                    continue
    except Exception:
        pass
    return plans


def read_membership_by_id(plan_id):
    plans = read_memberships()
    for plan in plans:
        if plan['membership_id'] == plan_id:
            return plan
    return None


def read_classes():
    classes = []
    try:
        with open('data/classes.txt', 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts)!=8:
                    continue
                try:
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
                    continue
    except Exception:
        pass
    return classes


def read_trainers():
    trainers = []
    try:
        with open('data/trainers.txt', 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts)!=6:
                    continue
                try:
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
                    continue
    except Exception:
        pass
    return trainers


def read_trainer_by_id(trainer_id):
    trainers = read_trainers()
    for t in trainers:
        if t['trainer_id'] == trainer_id:
            return t
    return None


def read_bookings():
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
                except Exception:
                    continue
    except Exception:
        pass
    return bookings


def write_booking(booking):
    try:
        bookings = read_bookings()
        max_id = 0
        for b in bookings:
            if b['booking_id'] > max_id:
                max_id = b['booking_id']
        booking_id = max_id + 1
        booking['booking_id'] = booking_id
        dirname = os.path.dirname('data/bookings.txt')
        if dirname and not os.path.exists(dirname):
            os.makedirs(dirname)
        with open('data/bookings.txt', 'a', encoding='utf-8') as f:
            line = f"{booking_id}|{booking['member_name']}|{booking['trainer_id']}|{booking['booking_date']}|{booking['booking_time']}|{booking['duration_minutes']}|{booking['status']}\n"
            f.write(line)
        return True
    except Exception:
        return False


def read_workouts():
    workouts = []
    try:
        with open('data/workouts.txt', 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts)!=7:
                    continue
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
                except Exception:
                    continue
    except Exception:
        pass
    return workouts


def write_workout(workout):
    try:
        workouts = read_workouts()
        max_id = 0
        for w in workouts:
            if w['workout_id'] > max_id:
                max_id = w['workout_id']
        workout_id = max_id + 1
        workout['workout_id'] = workout_id
        dirname = os.path.dirname('data/workouts.txt')
        if dirname and not os.path.exists(dirname):
            os.makedirs(dirname)
        with open('data/workouts.txt', 'a', encoding='utf-8') as f:
            line = f"{workout_id}|{workout['member_name']}|{workout['workout_type']}|{workout['workout_date']}|{workout['duration_minutes']}|{workout['calories_burned']}|{workout['notes']}\n"
            f.write(line)
        return True
    except Exception:
        return False


# Flask route implementations

@app.route('/', methods=['GET'])
def root_redirect():
    return redirect(url_for('dashboard'))


@app.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template('dashboard.html')


@app.route('/memberships', methods=['GET'])
def memberships():
    plans = read_memberships()
    return render_template('memberships.html', plans=plans)


@app.route('/plan/<int:plan_id>', methods=['GET'])
def plan_details(plan_id):
    plan = read_membership_by_id(plan_id)
    if plan is None:
        return "Plan not found", 404
    reviews = []  # Optional reviews list empty - no data source
    return render_template('plan_details.html', plan=plan, reviews=reviews)


@app.route('/classes', methods=['GET'])
def class_schedule():
    classes = read_classes()
    return render_template('classes.html', classes=classes)


@app.route('/trainers', methods=['GET'])
def trainers():
    trainers_list = read_trainers()
    return render_template('trainers.html', trainers=trainers_list)


@app.route('/trainer/<int:trainer_id>', methods=['GET'])
def trainer_detail(trainer_id):
    trainer = read_trainer_by_id(trainer_id)
    if trainer is None:
        return "Trainer not found", 404
    reviews = []  # Optional reviews list empty - no data source
    return render_template('trainer_detail.html', trainer=trainer, reviews=reviews)


@app.route('/pt_booking', methods=['GET'])
def pt_booking():
    trainers_list = read_trainers()
    return render_template('pt_booking.html', trainers=trainers_list)


@app.route('/pt_booking', methods=['POST'])
def pt_booking_submit():
    member_name = request.form.get('member_name', '').strip()
    trainer_id_str = request.form.get('trainer_id', '').strip()
    booking_date = request.form.get('booking_date', '').strip()
    booking_time = request.form.get('booking_time', '').strip()
    duration_minutes_str = request.form.get('duration_minutes', '').strip()

    if not (member_name and trainer_id_str and booking_date and booking_time and duration_minutes_str):
        trainers_list = read_trainers()
        error = "All fields are required."
        return render_template('pt_booking.html', trainers=trainers_list, error=error)

    try:
        trainer_id = int(trainer_id_str)
        duration_minutes = int(duration_minutes_str)
    except Exception:
        trainers_list = read_trainers()
        error = "Invalid input for trainer id or duration."
        return render_template('pt_booking.html', trainers=trainers_list, error=error)

    trainer = read_trainer_by_id(trainer_id)
    if trainer is None:
        trainers_list = read_trainers()
        error = "Selected trainer not found."
        return render_template('pt_booking.html', trainers=trainers_list, error=error)

    booking = {
        'member_name': member_name,
        'trainer_id': trainer_id,
        'booking_date': booking_date,
        'booking_time': booking_time,
        'duration_minutes': duration_minutes,
        'status': 'Pending'
    }

    if not write_booking(booking):
        trainers_list = read_trainers()
        error = "Failed to save booking. Please try again later."
        return render_template('pt_booking.html', trainers=trainers_list, error=error)

    return redirect(url_for('dashboard'))


@app.route('/workouts', methods=['GET'])
def workout_records():
    workouts = read_workouts()
    return render_template('workouts.html', workouts=workouts)


@app.route('/log_workout', methods=['GET'])
def log_workout():
    return render_template('log_workout.html')


@app.route('/log_workout', methods=['POST'])
def log_workout_submit():
    member_name = request.form.get('member_name', '').strip()
    workout_type = request.form.get('workout_type', '').strip()
    workout_date = request.form.get('workout_date', '').strip()
    duration_minutes_str = request.form.get('duration_minutes', '').strip()
    calories_burned_str = request.form.get('calories_burned', '').strip()
    notes = request.form.get('notes', '').strip()

    if not (member_name and workout_type and workout_date and duration_minutes_str and calories_burned_str):
        error = "All fields except notes are required."
        return render_template('log_workout.html', error=error)

    try:
        duration_minutes = int(duration_minutes_str)
        calories_burned = int(calories_burned_str)
    except Exception:
        error = "Duration and Calories Burned must be valid integers."
        return render_template('log_workout.html', error=error)

    workout = {
        'member_name': member_name,
        'workout_type': workout_type,
        'workout_date': workout_date,
        'duration_minutes': duration_minutes,
        'calories_burned': calories_burned,
        'notes': notes
    }

    if not write_workout(workout):
        error = "Failed to save workout record. Please try again later."
        return render_template('log_workout.html', error=error)

    return redirect(url_for('workout_records'))


if __name__ == '__main__':
    app.run(debug=True, port=5000)
