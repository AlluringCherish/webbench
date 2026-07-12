from flask import Flask, render_template, redirect, url_for, request
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Helper functions for loading data from files following the specified data schemas

def load_memberships():
    plans = []
    filepath = os.path.join(DATA_DIR, 'memberships.txt')
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 6:
                    continue
                try:
                    membership_id = int(parts[0])
                    plan_name = parts[1]
                    price = parts[2]
                    billing_cycle = parts[3]
                    features = parts[4]
                    max_classes_raw = parts[5]
                    if max_classes_raw == 'unlimited':
                        max_classes = 'unlimited'
                    else:
                        max_classes = int(max_classes_raw)
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
                    continue
    except FileNotFoundError:
        pass
    return plans


def load_plan_by_id(plan_id):
    plans = load_memberships()
    for plan in plans:
        if plan['membership_id'] == plan_id:
            return plan
    return None


def load_reviews_for_plan(plan_id):
    # Specification states reviews can be empty or omitted,
    # no file or data schema specified for reviews, so return empty list
    return []


def load_classes():
    classes = []
    filepath = os.path.join(DATA_DIR, 'classes.txt')
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) !=8:
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
                    cls = {
                        'class_id': class_id,
                        'class_name': class_name,
                        'trainer_id': trainer_id,
                        'class_type': class_type,
                        'schedule_day': schedule_day,
                        'schedule_time': schedule_time,
                        'capacity': capacity,
                        'duration': duration
                    }
                    classes.append(cls)
                except Exception:
                    continue
    except FileNotFoundError:
        pass
    return classes


def load_trainers():
    trainers = []
    filepath = os.path.join(DATA_DIR, 'trainers.txt')
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) !=6:
                    continue
                try:
                    trainer_id = int(parts[0])
                    name = parts[1]
                    specialty = parts[2]
                    certifications = parts[3]
                    experience_years = int(parts[4])
                    bio = parts[5]
                    trainer = {
                        'trainer_id': trainer_id,
                        'name': name,
                        'specialty': specialty,
                        'certifications': certifications,
                        'experience_years': experience_years,
                        'bio': bio
                    }
                    trainers.append(trainer)
                except Exception:
                    continue
    except FileNotFoundError:
        pass
    return trainers


def load_trainer_by_id(trainer_id):
    trainers = load_trainers()
    for trainer in trainers:
        if trainer['trainer_id'] == trainer_id:
            return trainer
    return None


def load_reviews_for_trainer(trainer_id):
    # Specification says reviews optional; no file or data specified
    return []


def load_workouts():
    workouts = []
    filepath = os.path.join(DATA_DIR, 'workouts.txt')
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 7:
                    continue
                try:
                    workout_id = int(parts[0])
                    member_name = parts[1]
                    workout_type = parts[2]
                    workout_date = parts[3]
                    duration_minutes = int(parts[4])
                    calories_burned = int(parts[5])
                    notes = parts[6]
                    workout = {
                        'workout_id': workout_id,
                        'member_name': member_name,
                        'workout_type': workout_type,
                        'workout_date': workout_date,
                        'duration_minutes': duration_minutes,
                        'calories_burned': calories_burned,
                        'notes': notes
                    }
                    workouts.append(workout)
                except Exception:
                    continue
    except FileNotFoundError:
        pass
    return workouts


def load_bookings():
    bookings = []
    filepath = os.path.join(DATA_DIR, 'bookings.txt')
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) !=7:
                    continue
                try:
                    booking_id = int(parts[0])
                    member_name = parts[1]
                    trainer_id = int(parts[2])
                    booking_date = parts[3]
                    booking_time = parts[4]
                    duration_minutes = int(parts[5])
                    status = parts[6]
                    booking = {
                        'booking_id': booking_id,
                        'member_name': member_name,
                        'trainer_id': trainer_id,
                        'booking_date': booking_date,
                        'booking_time': booking_time,
                        'duration_minutes': duration_minutes,
                        'status': status
                    }
                    bookings.append(booking)
                except Exception:
                    continue
    except FileNotFoundError:
        pass
    return bookings


# Routes as per design_spec

@app.route('/', methods=['GET'])
def root():
    return redirect(url_for('dashboard'))


@app.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template('dashboard.html')


@app.route('/memberships', methods=['GET'])
def memberships():
    plans = load_memberships()
    return render_template('memberships.html', plans=plans)


@app.route('/plan/<int:plan_id>', methods=['GET'])
def plan_details(plan_id):
    plan = load_plan_by_id(plan_id)
    if plan is None:
        return "Plan not found", 404
    reviews = load_reviews_for_plan(plan_id)
    return render_template('plan_details.html', plan=plan, reviews=reviews)


@app.route('/classes', methods=['GET'])
def class_schedule():
    classes = load_classes()
    return render_template('class_schedule.html', classes=classes)


@app.route('/trainers', methods=['GET'])
def trainers():
    trainers_list = load_trainers()
    return render_template('trainers.html', trainers=trainers_list)


@app.route('/trainer/<int:trainer_id>', methods=['GET'])
def trainer_detail(trainer_id):
    trainer = load_trainer_by_id(trainer_id)
    if trainer is None:
        return "Trainer not found", 404
    reviews = load_reviews_for_trainer(trainer_id)
    return render_template('trainer_detail.html', trainer=trainer, reviews=reviews)


@app.route('/booking', methods=['GET', 'POST'])
def pt_booking():
    if request.method == 'GET':
        trainers_list = load_trainers()
        trainers = [{'trainer_id': t['trainer_id'], 'name': t['name']} for t in trainers_list]
        return render_template('booking.html', trainers=trainers)

    if request.method == 'POST':
        member_name = request.form.get('member_name', '').strip()
        trainer_id_str = request.form.get('trainer_id', '').strip()
        booking_date = request.form.get('booking_date', '').strip()
        booking_time = request.form.get('booking_time', '').strip()
        duration_minutes_str = request.form.get('duration_minutes', '').strip()

        if not member_name or not trainer_id_str or not booking_date or not booking_time or not duration_minutes_str:
            return "Missing booking data", 400
        try:
            trainer_id = int(trainer_id_str)
            duration_minutes = int(duration_minutes_str)
        except ValueError:
            return "Invalid booking data", 400

        bookings = load_bookings()
        new_booking_id = 1
        if bookings:
            new_booking_id = max(b['booking_id'] for b in bookings) + 1

        new_booking = {
            'booking_id': new_booking_id,
            'member_name': member_name,
            'trainer_id': trainer_id,
            'booking_date': booking_date,
            'booking_time': booking_time,
            'duration_minutes': duration_minutes,
            'status': 'Pending'
        }

        filepath = os.path.join(DATA_DIR, 'bookings.txt')
        try:
            with open(filepath, 'a', encoding='utf-8') as f:
                line = f"{new_booking['booking_id']}|{new_booking['member_name']}|{new_booking['trainer_id']}|{new_booking['booking_date']}|{new_booking['booking_time']}|{new_booking['duration_minutes']}|{new_booking['status']}\n"
                f.write(line)
        except Exception as e:
            return f"Failed to save booking: {e}", 500

        return redirect(url_for('pt_booking'))


@app.route('/workouts', methods=['GET'])
def workout_records():
    workouts = load_workouts()
    return render_template('workouts.html', workouts=workouts)


@app.route('/log-workout', methods=['GET', 'POST'])
def log_workout():
    if request.method == 'GET':
        return render_template('log_workout.html')

    if request.method == 'POST':
        member_name = request.form.get('member_name', '').strip()
        workout_type = request.form.get('workout_type', '').strip()
        workout_date = request.form.get('workout_date', '').strip()
        duration_minutes_str = request.form.get('duration_minutes', '').strip()
        calories_burned_str = request.form.get('calories_burned', '').strip()
        notes = request.form.get('notes', '').strip()

        if not member_name or not workout_type or not workout_date or not duration_minutes_str or not calories_burned_str:
            return "Missing workout data", 400
        try:
            duration_minutes = int(duration_minutes_str)
            calories_burned = int(calories_burned_str)
        except ValueError:
            return "Invalid workout data", 400

        workouts = load_workouts()
        new_workout_id = 1
        if workouts:
            new_workout_id = max(w['workout_id'] for w in workouts) + 1

        new_workout = {
            'workout_id': new_workout_id,
            'member_name': member_name,
            'workout_type': workout_type,
            'workout_date': workout_date,
            'duration_minutes': duration_minutes,
            'calories_burned': calories_burned,
            'notes': notes
        }

        filepath = os.path.join(DATA_DIR, 'workouts.txt')
        try:
            with open(filepath, 'a', encoding='utf-8') as f:
                line = f"{new_workout['workout_id']}|{new_workout['member_name']}|{new_workout['workout_type']}|{new_workout['workout_date']}|{new_workout['duration_minutes']}|{new_workout['calories_burned']}|{new_workout['notes']}\n"
                f.write(line)
        except Exception as e:
            return f"Failed to save workout: {e}", 500

        return redirect(url_for('workout_records'))


if __name__ == '__main__':
    app.run(debug=True, port=5000)
