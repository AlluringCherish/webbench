from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

import os

# Utility functions to load data from files

def load_memberships():
    memberships = []
    try:
        with open('data/memberships.txt', 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 6:
                    continue
                membership = {
                    'membership_id': int(parts[0]),
                    'plan_name': parts[1],
                    'price': parts[2],
                    'billing_cycle': parts[3],
                    'features': parts[4],
                    'max_classes': parts[5]
                }
                memberships.append(membership)
    except Exception:
        pass
    return memberships


def load_classes():
    classes = []
    try:
        with open('data/classes.txt', 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 8:
                    continue
                class_item = {
                    'class_id': int(parts[0]),
                    'class_name': parts[1],
                    'trainer_id': int(parts[2]),
                    'class_type': parts[3],
                    'schedule_day': parts[4],
                    'schedule_time': parts[5],
                    'capacity': int(parts[6]),
                    'duration': int(parts[7])
                }
                classes.append(class_item)
    except Exception:
        pass
    return classes


def load_trainers():
    trainers = []
    try:
        with open('data/trainers.txt', 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 6:
                    continue
                trainer = {
                    'trainer_id': int(parts[0]),
                    'name': parts[1],
                    'specialty': parts[2],
                    'certifications': parts[3],
                    'experience_years': int(parts[4]),
                    'bio': parts[5]
                }
                trainers.append(trainer)
    except Exception:
        pass
    return trainers


def load_bookings():
    bookings = []
    try:
        with open('data/bookings.txt', 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 7:
                    continue
                booking = {
                    'booking_id': int(parts[0]),
                    'member_name': parts[1],
                    'trainer_id': int(parts[2]),
                    'booking_date': parts[3],
                    'booking_time': parts[4],
                    'duration_minutes': int(parts[5]),
                    'status': parts[6]
                }
                bookings.append(booking)
    except Exception:
        pass
    return bookings


# We will save bookings by appending new lines

def save_booking(new_booking):
    # new_booking is a dict with keys matching order:
    # booking_id, member_name, trainer_id, booking_date, booking_time, duration_minutes, status
    line = f"{new_booking['booking_id']}|{new_booking['member_name']}|{new_booking['trainer_id']}|{new_booking['booking_date']}|{new_booking['booking_time']}|{new_booking['duration_minutes']}|{new_booking['status']}\n"
    try:
        with open('data/bookings.txt', 'a', encoding='utf-8') as f:
            f.write(line)
        return True
    except Exception:
        return False


def load_workouts():
    workouts = []
    try:
        with open('data/workouts.txt', 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 7:
                    continue
                workout = {
                    'workout_id': int(parts[0]),
                    # member_name not needed for context but part of data
                    'member_name': parts[1],
                    'workout_type': parts[2],
                    'workout_date': parts[3],
                    'duration_minutes': int(parts[4]),
                    'calories_burned': int(parts[5]),
                    'notes': parts[6]
                }
                workouts.append(workout)
    except Exception:
        pass
    return workouts


def save_workout(new_workout):
    # new_workout dict keys:
    # workout_id, member_name, workout_type, workout_date, duration_minutes, calories_burned, notes
    line = f"{new_workout['workout_id']}|{new_workout['member_name']}|{new_workout['workout_type']}|{new_workout['workout_date']}|{new_workout['duration_minutes']}|{new_workout['calories_burned']}|{new_workout['notes']}\n"
    try:
        with open('data/workouts.txt', 'a', encoding='utf-8') as f:
            f.write(line)
        return True
    except Exception:
        return False


# Hardcoded sample data for plan reviews per plan_id
# Since no reviews file is specified, we will use sample placeholders
plan_reviews_data = {
    1: [
        {'review_text': 'Good value for beginners.', 'reviewer': 'Alice'},
        {'review_text': 'Could increase class variety.', 'reviewer': 'Bob'}
    ],
    2: [
        {'review_text': 'Great for intermediate users.', 'reviewer': 'Charlie'},
        {'review_text': 'Loved the PT sessions included.', 'reviewer': 'Diana'}
    ],
    3: [
        {'review_text': 'Best membership I have had!', 'reviewer': 'Ed'},
        {'review_text': 'Highly recommend the nutrition coaching.', 'reviewer': 'Fiona'}
    ]
}

# Hardcoded sample data for trainer reviews per trainer_id
trainer_reviews_data = {
    1: [
        {'review_text': 'Sarah is amazing and really helped my flexibility.', 'reviewer': 'John'},
        {'review_text': 'Very patient and knowledgeable.', 'reviewer': 'Rebecca'}
    ],
    2: [
        {'review_text': 'Mike pushes you to your max!', 'reviewer': 'Simon'},
        {'review_text': 'Excellent strength training guidance.', 'reviewer': 'Nina'}
    ],
    3: [
        {'review_text': 'Emma helped me improve my core strength.', 'reviewer': 'Laura'},
        {'review_text': 'Highly skilled Pilates instructor.', 'reviewer': 'Mark'}
    ]
}


@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard_page'))


@app.route('/dashboard')
def dashboard_page():
    # For member_status: simple welcome message
    member_status = "Welcome back to your Gym Dashboard!"

    # featured_classes: we will pick first 3 classes from classes.txt as a summary
    classes = load_classes()
    featured_classes = []
    for c in classes[:3]:
        featured_classes.append({
            'name': c['class_name'],
            'time': f"{c['schedule_day']} {c['schedule_time']}",
            'trainer': None
        })

    # To get trainer names for featured classes
    trainers = load_trainers()
    trainer_map = {t['trainer_id']: t['name'] for t in trainers}
    for fc in featured_classes:
        # find trainer name by matching class_name's trainer_id
        for c in classes:
            if c['class_name'] == fc['name']:
                fc['trainer'] = trainer_map.get(c['trainer_id'], None)
                break

    return render_template('dashboard.html', member_status=member_status, featured_classes=featured_classes)


@app.route('/memberships')
def membership_plans_page():
    membership_plans = load_memberships()
    return render_template('memberships.html', membership_plans=membership_plans)


@app.route('/plan/<int:plan_id>')
def plan_details_page(plan_id):
    membership_plans = load_memberships()
    plan = next((p for p in membership_plans if p['membership_id'] == plan_id), None)
    if not plan:
        return "Plan not found", 404

    plan_reviews = plan_reviews_data.get(plan_id, [])

    return render_template('plan_details.html', plan=plan, plan_reviews=plan_reviews)


@app.route('/schedule')
def class_schedule_page():
    classes = load_classes()
    return render_template('schedule.html', classes=classes)


@app.route('/trainers')
def trainer_profiles_page():
    trainers = load_trainers()
    return render_template('trainers.html', trainers=trainers)


@app.route('/trainer/<int:trainer_id>')
def trainer_detail_page(trainer_id):
    trainers = load_trainers()
    trainer = next((t for t in trainers if t['trainer_id'] == trainer_id), None)
    if not trainer:
        return "Trainer not found", 404

    trainer_reviews = trainer_reviews_data.get(trainer_id, [])

    return render_template('trainer_detail.html', trainer=trainer, trainer_reviews=trainer_reviews)


@app.route('/booking', methods=['GET', 'POST'])
def personal_training_booking_page():
    trainers = load_trainers()
    available_times = [
        "08:00", "09:00", "10:00", "11:00", "13:00", "14:00", "15:00", "16:00", "17:00"
    ]
    session_durations = [30, 60, 90]

    if request.method == 'POST':
        member_name = request.form.get('member_name', '').strip()
        trainer_id_str = request.form.get('trainer_id', '').strip()
        booking_date = request.form.get('booking_date', '').strip()
        booking_time = request.form.get('booking_time', '').strip()
        duration_str = request.form.get('duration', '').strip()

        # Validate presence
        if not member_name or not trainer_id_str or not booking_date or not booking_time or not duration_str:
            return render_template('booking.html', trainers=[{'trainer_id': t['trainer_id'], 'name': t['name']} for t in trainers], available_times=available_times, session_durations=session_durations, error_message="All fields are required.")

        try:
            trainer_id = int(trainer_id_str)
            duration_minutes = int(duration_str)
        except ValueError:
            return render_template('booking.html', trainers=[{'trainer_id': t['trainer_id'], 'name': t['name']} for t in trainers], available_times=available_times, session_durations=session_durations, error_message="Invalid trainer or duration.")

        # Determine new booking_id
        bookings = load_bookings()
        max_id = max((b['booking_id'] for b in bookings), default=0)
        new_booking_id = max_id + 1

        new_booking = {
            'booking_id': new_booking_id,
            'member_name': member_name,
            'trainer_id': trainer_id,
            'booking_date': booking_date,
            'booking_time': booking_time,
            'duration_minutes': duration_minutes,
            'status': 'Pending'
        }

        if save_booking(new_booking):
            # On success, redirect to booking page or display success message
            return redirect(url_for('personal_training_booking_page'))
        else:
            return render_template('booking.html', trainers=[{'trainer_id': t['trainer_id'], 'name': t['name']} for t in trainers], available_times=available_times, session_durations=session_durations, error_message="Failed to save booking. Please try again.")

    # GET
    return render_template('booking.html', trainers=[{'trainer_id': t['trainer_id'], 'name': t['name']} for t in trainers], available_times=available_times, session_durations=session_durations)


@app.route('/workouts')
def workout_records_page():
    workouts = load_workouts()

    # Only keep needed fields per spec (omit member_name for context)
    workouts_context = []
    for w in workouts:
        workouts_context.append({
            'workout_id': w['workout_id'],
            'workout_type': w['workout_type'],
            'workout_date': w['workout_date'],
            'duration_minutes': w['duration_minutes'],
            'calories_burned': w['calories_burned'],
            'notes': w['notes']
        })

    filter_types = ['Class', 'PT Session', 'Personal']

    return render_template('workouts.html', workouts=workouts_context, filter_types=filter_types)


@app.route('/log-workout', methods=['GET', 'POST'])
def log_workout_page():
    workout_types = ['Cardio', 'Strength', 'Flexibility', 'Sports']

    if request.method == 'POST':
        member_name = request.form.get('member_name', '').strip()
        workout_type = request.form.get('workout_type', '').strip()
        workout_date = request.form.get('workout_date', '').strip()
        duration_str = request.form.get('duration_minutes', '').strip()
        calories_str = request.form.get('calories_burned', '').strip()
        notes = request.form.get('notes', '').strip()

        if not member_name or not workout_type or not workout_date or not duration_str or not calories_str:
            return render_template('log_workout.html', workout_types=workout_types, error_message="All fields except notes are required.")

        try:
            duration_minutes = int(duration_str)
            calories_burned = int(calories_str)
        except ValueError:
            return render_template('log_workout.html', workout_types=workout_types, error_message="Duration and calories must be numbers.")

        workouts = load_workouts()
        max_id = max((w['workout_id'] for w in workouts), default=0)
        new_workout_id = max_id + 1

        new_workout = {
            'workout_id': new_workout_id,
            'member_name': member_name,
            'workout_type': workout_type,
            'workout_date': workout_date,
            'duration_minutes': duration_minutes,
            'calories_burned': calories_burned,
            'notes': notes
        }

        if save_workout(new_workout):
            return redirect(url_for('workout_records_page'))
        else:
            return render_template('log_workout.html', workout_types=workout_types, error_message="Failed to save workout. Please try again.")

    # GET
    return render_template('log_workout.html', workout_types=workout_types)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
