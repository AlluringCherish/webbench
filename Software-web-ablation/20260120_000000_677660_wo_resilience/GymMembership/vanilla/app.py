from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

import os

DATA_DIR = 'data'

# Helper functions for data loading and saving

def load_memberships():
    memberships = []
    try:
        with open(os.path.join(DATA_DIR, 'memberships.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 6:
                    membership_id = int(parts[0])
                    plan_name = parts[1]
                    price = float(parts[2])
                    billing_cycle = parts[3]
                    features = parts[4]
                    max_classes = parts[5]
                    memberships.append({
                        'membership_id': membership_id,
                        'plan_name': plan_name,
                        'price': price,
                        'billing_cycle': billing_cycle,
                        'features': features,
                        'max_classes': max_classes
                    })
    except Exception:
        pass
    return memberships


def load_classes():
    classes = []
    try:
        with open(os.path.join(DATA_DIR, 'classes.txt'), 'r', encoding='utf-8') as f:
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
        pass
    return classes


def load_trainers():
    trainers = []
    try:
        with open(os.path.join(DATA_DIR, 'trainers.txt'), 'r', encoding='utf-8') as f:
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
        pass
    return trainers


def load_bookings():
    bookings = []
    try:
        with open(os.path.join(DATA_DIR, 'bookings.txt'), 'r', encoding='utf-8') as f:
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
        pass
    return bookings


def save_booking(booking):
    # booking is a dict with keys matching bookings.txt fields except booking_id
    bookings = load_bookings()
    max_id = max([b['booking_id'] for b in bookings], default=0)
    new_id = max_id + 1
    try:
        with open(os.path.join(DATA_DIR, 'bookings.txt'), 'a', encoding='utf-8') as f:
            line = f"{new_id}|{booking['member_name']}|{booking['trainer_id']}|{booking['booking_date']}|{booking['booking_time']}|{booking['duration_minutes']}|{booking['status']}\n"
            f.write(line)
        return True
    except Exception:
        return False


def load_workouts():
    workouts = []
    try:
        with open(os.path.join(DATA_DIR, 'workouts.txt'), 'r', encoding='utf-8') as f:
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
        pass
    return workouts


def save_workout(workout):
    # workout is a dict with keys matching workouts.txt fields except workout_id
    workouts = load_workouts()
    max_id = max([w['workout_id'] for w in workouts], default=0)
    new_id = max_id + 1
    try:
        with open(os.path.join(DATA_DIR, 'workouts.txt'), 'a', encoding='utf-8') as f:
            line = f"{new_id}|{workout['member_name']}|{workout['workout_type']}|{workout['workout_date']}|{workout['duration_minutes']}|{workout['calories_burned']}|{workout['notes']}\n"
            f.write(line)
        return True
    except Exception:
        return False


# Additional utility functions

def get_membership_by_id(plan_id):
    memberships = load_memberships()
    for plan in memberships:
        if plan['membership_id'] == plan_id:
            return plan
    return None


def get_trainer_by_id(trainer_id):
    trainers = load_trainers()
    for trainer in trainers:
        if trainer['trainer_id'] == trainer_id:
            return trainer
    return None


def load_plan_reviews(plan_id):
    reviews = []
    path = os.path.join(DATA_DIR, f'plan_{plan_id}_reviews.txt')
    if os.path.isfile(path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                for line in f:
                    parts = line.strip().split('|')
                    if len(parts) >= 2:
                        reviewer = parts[0]
                        comment = parts[1]
                        reviews.append({'reviewer': reviewer, 'comment': comment})
        except Exception:
            pass
    return reviews


def load_trainer_reviews(trainer_id):
    reviews = []
    path = os.path.join(DATA_DIR, f'trainer_{trainer_id}_reviews.txt')
    if os.path.isfile(path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                for line in f:
                    parts = line.strip().split('|')
                    if len(parts) >= 2:
                        reviewer = parts[0]
                        comment = parts[1]
                        reviews.append({'reviewer': reviewer, 'comment': comment})
        except Exception:
            pass
    return reviews


# Routes

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    member_welcome_msg = "Welcome to your gym membership dashboard!"

    classes_list = load_classes()
    trainers_map = {t['trainer_id']: t['name'] for t in load_trainers()}

    featured_classes = []
    # Select first 3 classes as featured - can be all classes if less
    for cls in classes_list[:3]:
        trainer_name = trainers_map.get(cls['trainer_id'], 'Unknown')
        featured_classes.append({
            'class_name': cls['class_name'],
            'schedule_day': cls['schedule_day'],
            'schedule_time': cls['schedule_time'],
            'trainer_name': trainer_name
        })

    quick_links = {
        'browse-membership-button': url_for('memberships'),
        'view-schedule-button': url_for('class_schedule'),
        'book-trainer-button': url_for('pt_booking')
    }

    return render_template('dashboard.html', member_welcome_msg=member_welcome_msg, featured_classes=featured_classes, quick_links=quick_links)


@app.route('/memberships')
def memberships():
    membership_plans = load_memberships()
    return render_template('memberships.html', membership_plans=membership_plans)


@app.route('/plan/<int:plan_id>')
def plan_details(plan_id):
    plan = get_membership_by_id(plan_id)
    if plan is None:
        # Simple 404 fallback
        return "Plan not found", 404

    plan_reviews = load_plan_reviews(plan_id)
    return render_template('plan_details.html', plan=plan, plan_reviews=plan_reviews)


@app.route('/classes')
def class_schedule():
    classes = load_classes()
    return render_template('class_schedule.html', classes=classes)


@app.route('/trainers')
def trainers():
    trainers_list = load_trainers()
    return render_template('trainers.html', trainers_list=trainers_list)


@app.route('/trainer/<int:trainer_id>')
def trainer_detail(trainer_id):
    trainer = get_trainer_by_id(trainer_id)
    if trainer is None:
        return "Trainer not found", 404

    trainer_reviews = load_trainer_reviews(trainer_id)
    return render_template('trainer_detail.html', trainer=trainer, trainer_reviews=trainer_reviews)


@app.route('/booking', methods=['GET', 'POST'])
def pt_booking():
    trainers = [{'trainer_id': t['trainer_id'], 'name': t['name']} for t in load_trainers()]
    if request.method == 'GET':
        return render_template('pt_booking.html', trainers=trainers)
    else:
        # POST handling
        member_name = request.form.get('member_name', '').strip()
        trainer_id = request.form.get('trainer_id', '').strip()
        booking_date = request.form.get('booking_date', '').strip()
        booking_time = request.form.get('booking_time', '').strip()
        duration_minutes = request.form.get('duration_minutes', '').strip()

        if not member_name or not trainer_id or not booking_date or not booking_time or not duration_minutes:
            return render_template('pt_booking.html', trainers=trainers, booking_confirmation='Error: All fields are required.')

        try:
            trainer_id = int(trainer_id)
            duration_minutes = int(duration_minutes)
        except ValueError:
            return render_template('pt_booking.html', trainers=trainers, booking_confirmation='Error: Invalid number format for trainer id or duration.')

        booking = {
            'member_name': member_name,
            'trainer_id': trainer_id,
            'booking_date': booking_date,
            'booking_time': booking_time,
            'duration_minutes': duration_minutes,
            'status': 'Pending'
        }

        success = save_booking(booking)
        if success:
            confirmation_msg = f"Booking request submitted successfully for {member_name} on {booking_date} at {booking_time}."
            return render_template('pt_booking.html', trainers=trainers, booking_confirmation=confirmation_msg)
        else:
            return render_template('pt_booking.html', trainers=trainers, booking_confirmation='Error: Could not save booking. Please try again.')


@app.route('/workouts')
def workout_records():
    workouts = load_workouts()
    return render_template('workout_records.html', workouts=workouts)


@app.route('/log_workout', methods=['GET', 'POST'])
def log_workout():
    if request.method == 'GET':
        return render_template('log_workout.html')
    else:
        member_name = request.form.get('member_name', '').strip()
        workout_type = request.form.get('workout_type', '').strip()
        workout_date = request.form.get('workout_date', '').strip()
        duration_minutes = request.form.get('workout_duration', '').strip()
        calories_burned = request.form.get('calories_burned', '').strip()
        notes = request.form.get('workout_notes', '').strip()

        if not member_name or not workout_type or not workout_date or not duration_minutes or not calories_burned:
            return render_template('log_workout.html', log_confirmation='Error: All fields except notes are required.')

        try:
            duration_minutes = int(duration_minutes)
            calories_burned = int(calories_burned)
        except ValueError:
            return render_template('log_workout.html', log_confirmation='Error: Duration and calories must be numbers.')

        workout = {
            'member_name': member_name,
            'workout_type': workout_type,
            'workout_date': workout_date,
            'duration_minutes': duration_minutes,
            'calories_burned': calories_burned,
            'notes': notes
        }

        success = save_workout(workout)
        if success:
            confirmation_msg = f"Workout logged successfully for {member_name} on {workout_date}."
            return render_template('log_workout.html', log_confirmation=confirmation_msg)
        else:
            return render_template('log_workout.html', log_confirmation='Error: Could not save workout. Please try again.')


if __name__ == '__main__':
    app.run(debug=True, port=5000)
