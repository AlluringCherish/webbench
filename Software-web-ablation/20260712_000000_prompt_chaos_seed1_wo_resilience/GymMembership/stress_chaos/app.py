from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

# Helper functions to load data

def load_memberships():
    memberships = []
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
                    max_classes = parts[5]  # could be int or 'unlimited'
                    try:
                        max_classes = int(max_classes)
                    except ValueError:
                        pass
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
        pass
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
        pass
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
        pass
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
        pass
    return workouts


def save_booking(booking):
    # booking dict keys: booking_id, member_name, trainer_id, booking_date, booking_time, duration_minutes, status
    try:
        with open('data/bookings.txt', 'a', encoding='utf-8') as f:
            line = "{}|{}|{}|{}|{}|{}|{}\n".format(
                booking['booking_id'], booking['member_name'], booking['trainer_id'],
                booking['booking_date'], booking['booking_time'], booking['duration_minutes'], booking['status'])
            f.write(line)
        return True
    except Exception:
        return False


def save_workout(workout):
    # workout dict keys: workout_id, member_name, workout_type, workout_date, duration_minutes, calories_burned, notes
    try:
        with open('data/workouts.txt', 'a', encoding='utf-8') as f:
            line = "{}|{}|{}|{}|{}|{}|{}\n".format(
                workout['workout_id'], workout['member_name'], workout['workout_type'],
                workout['workout_date'], workout['duration_minutes'], workout['calories_burned'], workout['notes'])
            f.write(line)
        return True
    except Exception:
        return False


@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    # For demo, let's set a fixed member_status
    member_status = "Welcome, valued member! Your membership is active."

    # Optional demo featured_classes and member_highlights
    featured_classes = [
        {'class_name': 'Morning Yoga', 'schedule_day': 'Monday', 'schedule_time': '06:00'},
        {'class_name': 'CrossFit Bootcamp', 'schedule_day': 'Tuesday', 'schedule_time': '18:00'},
    ]
    member_highlights = [
        "John improved his deadlift by 20kg",
        "Jane completed 30 consecutive days of yoga"
    ]

    return render_template('dashboard.html', member_status=member_status,
                           featured_classes=featured_classes, member_highlights=member_highlights)


@app.route('/memberships')
def memberships():
    memberships = load_memberships()
    filter_options = ["Basic", "Premium", "Elite"]
    return render_template('memberships.html', memberships=memberships, filter_options=filter_options)


@app.route('/plan/<int:plan_id>')
def plan_details(plan_id):
    memberships = load_memberships()
    plan = next((m for m in memberships if m['membership_id'] == plan_id), None)

    # No reviews file specified, assume no reviews or empty
    reviews = []

    return render_template('plan_details.html', plan=plan, reviews=reviews)


@app.route('/schedule')
def class_schedule():
    classes = load_classes()
    class_types = list({c['class_type'] for c in classes})
    class_types.sort()
    return render_template('schedule.html', classes=classes, class_types=class_types)


@app.route('/trainers')
def trainers():
    trainers = load_trainers()
    specialties = list({t['specialty'] for t in trainers})
    specialties.sort()
    return render_template('trainers.html', trainers=trainers, specialties=specialties)


@app.route('/trainer/<int:trainer_id>')
def trainer_detail(trainer_id):
    trainers = load_trainers()
    trainer = next((t for t in trainers if t['trainer_id'] == trainer_id), None)

    # No separate reviews file specified, so empty list
    reviews = []

    return render_template('trainer_detail.html', trainer=trainer, reviews=reviews)


from datetime import datetime

@app.route('/booking', methods=['GET', 'POST'])
def booking():
    trainers = load_trainers()
    if request.method == 'POST':
        # Form data keys expected: member_name (assumed), trainer_id, booking_date, booking_time, session_duration
        member_name = request.form.get('member_name', 'Anonymous')
        trainer_id = request.form.get('trainer_id')
        booking_date = request.form.get('booking_date')
        booking_time = request.form.get('booking_time')
        session_duration = request.form.get('session_duration')

        # Validate and process
        try:
            trainer_id = int(trainer_id)
            session_duration = int(session_duration)
        except (ValueError, TypeError):
            # Invalid form data
            return render_template('booking.html', trainers=trainers, error="Invalid input")

        # Generate new booking_id
        bookings = load_bookings()
        booking_id = max((b['booking_id'] for b in bookings), default=0) + 1

        new_booking = {
            'booking_id': booking_id,
            'member_name': member_name,
            'trainer_id': trainer_id,
            'booking_date': booking_date,
            'booking_time': booking_time,
            'duration_minutes': session_duration,
            'status': 'Pending'
        }

        if save_booking(new_booking):
            return redirect(url_for('booking'))
        else:
            return render_template('booking.html', trainers=trainers, error="Failed to save booking")

    # GET request
    return render_template('booking.html', trainers=trainers)


@app.route('/workouts')
def workouts():
    workouts = load_workouts()
    workout_types = ["Class", "PT Session", "Personal"]
    return render_template('workouts.html', workouts=workouts, workout_types=workout_types)


@app.route('/log_workout', methods=['GET', 'POST'])
def log_workout():
    workout_options = ["Cardio", "Strength", "Flexibility", "Sports"]
    if request.method == 'POST':
        # Form data keys expected: member_name, workout_type, workout_date, workout_duration, calories_burned, workout_notes
        member_name = request.form.get('member_name', 'Anonymous')
        workout_type = request.form.get('workout_type')
        workout_date = request.form.get('workout_date')
        workout_duration = request.form.get('workout_duration')
        calories_burned = request.form.get('calories_burned')
        workout_notes = request.form.get('workout_notes', '')

        try:
            workout_duration = int(workout_duration)
            calories_burned = int(calories_burned)
        except (ValueError, TypeError):
            return render_template('log_workout.html', error="Invalid input for duration or calories burned.")

        workouts = load_workouts()
        workout_id = max((w['workout_id'] for w in workouts), default=0) + 1

        new_workout = {
            'workout_id': workout_id,
            'member_name': member_name,
            'workout_type': workout_type,
            'workout_date': workout_date,
            'duration_minutes': workout_duration,
            'calories_burned': calories_burned,
            'notes': workout_notes
        }

        if save_workout(new_workout):
            return redirect(url_for('workouts'))
        else:
            return render_template('log_workout.html', error="Failed to save workout.")

    # GET request
    return render_template('log_workout.html', workout_types=workout_options)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
