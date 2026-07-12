from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

# Data file paths
MEMBERSHIPS_FILE = 'data/memberships.txt'
CLASSES_FILE = 'data/classes.txt'
TRAINERS_FILE = 'data/trainers.txt'
BOOKINGS_FILE = 'data/bookings.txt'
WORKOUTS_FILE = 'data/workouts.txt'

# Helper functions to load data

def load_memberships():
    plans = []
    try:
        with open(MEMBERSHIPS_FILE, 'r', encoding='utf-8') as file:
            for line in file:
                parts = line.strip().split('|')
                if len(parts) == 6:
                    plan = {
                        'membership_id': int(parts[0]),
                        'plan_name': parts[1],
                        'price': parts[2],
                        'billing_cycle': parts[3],
                        'features': parts[4],
                        'max_classes': parts[5]
                    }
                    plans.append(plan)
    except Exception:
        # In case file is missing or corrupted, return empty list
        pass
    return plans


def load_plan_reviews(plan_id):
    # Not specified from where to load plan reviews in spec.
    # Spec only provides plan_reviews context variable but no data source.
    # We'll return empty list as no source given.
    return []


def load_classes():
    classes = []
    try:
        with open(CLASSES_FILE, 'r', encoding='utf-8') as file:
            for line in file:
                parts = line.strip().split('|')
                if len(parts) == 8:
                    cl = {
                        'class_id': int(parts[0]),
                        'class_name': parts[1],
                        'trainer_id': int(parts[2]),
                        'class_type': parts[3],
                        'schedule_day': parts[4],
                        'schedule_time': parts[5],
                        'capacity': int(parts[6]),
                        'duration': int(parts[7])
                    }
                    classes.append(cl)
    except Exception:
        pass
    return classes


def load_trainers():
    trainers = []
    try:
        with open(TRAINERS_FILE, 'r', encoding='utf-8') as file:
            for line in file:
                parts = line.strip().split('|')
                if len(parts) == 6:
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


def load_trainer_reviews(trainer_id):
    # Not specified from where to load trainer reviews in spec.
    # Spec only provides trainer_reviews context variable but no data source.
    # We'll return empty list as no source given.
    return []


def load_bookings():
    bookings = []
    try:
        with open(BOOKINGS_FILE, 'r', encoding='utf-8') as file:
            for line in file:
                parts = line.strip().split('|')
                if len(parts) == 7:
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


def save_booking(member_name, trainer_id, booking_date, booking_time, duration_minutes, status='Pending'):
    try:
        bookings = load_bookings()
        booking_ids = [b['booking_id'] for b in bookings]
        new_id = max(booking_ids) + 1 if booking_ids else 1
        new_booking = [str(new_id), member_name, str(trainer_id), booking_date, booking_time, str(duration_minutes), status]
        with open(BOOKINGS_FILE, 'a', encoding='utf-8') as file:
            file.write('|'.join(new_booking) + '\n')
        return True
    except Exception:
        return False


def load_workouts():
    workouts = []
    try:
        with open(WORKOUTS_FILE, 'r', encoding='utf-8') as file:
            for line in file:
                parts = line.strip().split('|')
                if len(parts) == 7:
                    workout = {
                        'workout_id': int(parts[0]),
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


def save_workout(member_name, workout_type, workout_date, duration_minutes, calories_burned, notes):
    try:
        workouts = load_workouts()
        workout_ids = [w['workout_id'] for w in workouts]
        new_id = max(workout_ids) + 1 if workout_ids else 1
        new_workout = [str(new_id), member_name, workout_type, workout_date, str(duration_minutes), str(calories_burned), notes]
        with open(WORKOUTS_FILE, 'a', encoding='utf-8') as file:
            file.write('|'.join(new_workout) + '\n')
        return True
    except Exception:
        return False


# Extract distinct membership types as per spec
def get_membership_types():
    # As per spec: ['Basic', 'Premium', 'Elite']
    return ['Basic', 'Premium', 'Elite']


def get_class_types():
    classes = load_classes()
    types = set()
    for cl in classes:
        types.add(cl['class_type'])
    return sorted(types)


def get_specialties():
    trainers = load_trainers()
    specialties = set()
    for t in trainers:
        specialties.add(t['specialty'])
    return sorted(specialties)


def get_workout_types():
    workouts = load_workouts()
    types = set()
    for w in workouts:
        types.add(w['workout_type'])
    # To ensure we always have some types even if workouts file empty, return some common types
    default_types = ['Cardio', 'Strength', 'Class', 'Yoga', 'Pilates']
    return sorted(types) if types else default_types


@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard_page'))


@app.route('/dashboard')
def dashboard_page():
    member_welcome_msg = "Welcome to your Gym Membership Dashboard!"
    featured_classes = [
        {'class_id': 1, 'class_name': 'Morning Yoga', 'schedule_day': 'Monday', 'schedule_time': '06:00'},
        {'class_id': 2, 'class_name': 'CrossFit Bootcamp', 'schedule_day': 'Tuesday', 'schedule_time': '18:00'},
        {'class_id': 3, 'class_name': 'Pilates Core', 'schedule_day': 'Wednesday', 'schedule_time': '10:00'}
    ]
    quick_nav_links = [
        {'label': 'Membership Plans', 'route': url_for('membership_plans')},
        {'label': 'Class Schedule', 'route': url_for('class_schedule')},
        {'label': 'Book Trainer', 'route': url_for('pt_booking')}
    ]
    return render_template('dashboard.html', member_welcome_msg=member_welcome_msg, featured_classes=featured_classes, quick_nav_links=quick_nav_links)


@app.route('/memberships')
def membership_plans():
    plans = load_memberships()
    membership_types = get_membership_types()
    return render_template('memberships.html', plans=plans, membership_types=membership_types)


@app.route('/plan/<int:plan_id>')
def plan_details(plan_id):
    plans = load_memberships()
    plan = next((p for p in plans if p['membership_id'] == plan_id), None)
    if plan is None:
        return "Plan not found", 404
    plan_reviews = load_plan_reviews(plan_id)
    return render_template('plan_details.html', plan=plan, plan_reviews=plan_reviews)


@app.route('/schedule')
def class_schedule():
    classes = load_classes()
    class_types = get_class_types()
    return render_template('schedule.html', classes=classes, class_types=class_types)


@app.route('/trainers')
def trainer_profiles():
    trainers = load_trainers()
    specialties = get_specialties()
    return render_template('trainers.html', trainers=trainers, specialties=specialties)


@app.route('/trainer/<int:trainer_id>')
def trainer_detail(trainer_id):
    trainers = load_trainers()
    trainer = next((t for t in trainers if t['trainer_id'] == trainer_id), None)
    if trainer is None:
        return "Trainer not found", 404
    trainer_reviews = load_trainer_reviews(trainer_id)
    return render_template('trainer_detail.html', trainer=trainer, trainer_reviews=trainer_reviews)


@app.route('/book-training', methods=['GET', 'POST'])
def pt_booking():
    trainers = load_trainers()
    booking_status = None
    if request.method == 'POST':
        member_name = request.form.get('member_name', '').strip()
        trainer_id = request.form.get('trainer_id')
        booking_date = request.form.get('booking_date', '').strip()
        booking_time = request.form.get('booking_time', '').strip()
        duration_minutes = request.form.get('duration_minutes')
        # Validate and convert inputs
        try:
            trainer_id = int(trainer_id)
            duration_minutes = int(duration_minutes)
            if not member_name or not booking_date or not booking_time or duration_minutes <= 0:
                booking_status = "Invalid booking details provided."
            else:
                success = save_booking(member_name, trainer_id, booking_date, booking_time, duration_minutes, status='Pending')
                if success:
                    booking_status = "Booking successfully submitted and is pending confirmation."
                else:
                    booking_status = "Failed to save booking. Please try again."
        except Exception:
            booking_status = "Invalid booking input."

    # Only send IDs and names for trainer selection
    trainer_choices = [{'trainer_id': t['trainer_id'], 'name': t['name']} for t in trainers]
    return render_template('booking.html', trainers=trainer_choices, booking_status=booking_status)


@app.route('/workouts')
def workout_records():
    workouts = load_workouts()
    workout_types = get_workout_types()
    return render_template('workouts.html', workouts=workouts, workout_types=workout_types)


@app.route('/log-workout', methods=['GET', 'POST'])
def log_workout():
    workout_types = get_workout_types()
    submission_status = None
    if request.method == 'POST':
        member_name = request.form.get('member_name', '').strip()
        workout_type = request.form.get('workout_type', '').strip()
        workout_date = request.form.get('workout_date', '').strip()
        duration_minutes = request.form.get('duration_minutes')
        calories_burned = request.form.get('calories_burned')
        notes = request.form.get('notes', '').strip()
        try:
            duration_minutes = int(duration_minutes)
            calories_burned = int(calories_burned)
            if not member_name or not workout_type or not workout_date or duration_minutes <= 0 or calories_burned < 0:
                submission_status = "Invalid workout submission details."
            else:
                success = save_workout(member_name, workout_type, workout_date, duration_minutes, calories_burned, notes)
                if success:
                    submission_status = "Workout logged successfully."
                else:
                    submission_status = "Failed to save workout. Please try again."
        except Exception:
            submission_status = "Invalid workout input."
    return render_template('log_workout.html', workout_types=workout_types, submission_status=submission_status)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
