from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

# Helper functions to load data from text files

def load_memberships():
    plans = []
    try:
        with open('data/memberships.txt', 'r', encoding='utf-8') as file:
            for line in file:
                parts = line.strip().split('|')
                if len(parts) == 6:
                    plan = {
                        'membership_id': int(parts[0]),
                        'plan_name': parts[1],
                        'price': parts[2],
                        'billing_cycle': parts[3],
                        'features': parts[4],
                        'max_classes': parts[5],
                    }
                    plans.append(plan)
    except Exception as e:
        print(f"Error loading memberships: {e}")
    return plans


def load_classes():
    classes = []
    try:
        with open('data/classes.txt', 'r', encoding='utf-8') as file:
            for line in file:
                parts = line.strip().split('|')
                if len(parts) == 8:
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
    except Exception as e:
        print(f"Error loading classes: {e}")
    return classes


def load_trainers():
    trainers = []
    try:
        with open('data/trainers.txt', 'r', encoding='utf-8') as file:
            for line in file:
                parts = line.strip().split('|')
                if len(parts) == 6:
                    trainer = {
                        'trainer_id': int(parts[0]),
                        'name': parts[1],
                        'specialty': parts[2],
                        'certifications': parts[3],
                        'experience_years': int(parts[4]),
                        'bio': parts[5],
                    }
                    trainers.append(trainer)
    except Exception as e:
        print(f"Error loading trainers: {e}")
    return trainers


def load_bookings():
    bookings = []
    try:
        with open('data/bookings.txt', 'r', encoding='utf-8') as file:
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
                        'status': parts[6],
                    }
                    bookings.append(booking)
    except Exception as e:
        print(f"Error loading bookings: {e}")
    return bookings


def load_workouts():
    workouts = []
    try:
        with open('data/workouts.txt', 'r', encoding='utf-8') as file:
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
                        'notes': parts[6],
                    }
                    workouts.append(workout)
    except Exception as e:
        print(f"Error loading workouts: {e}")
    return workouts


def save_booking(new_booking):
    # Append new booking to data/bookings.txt with correct format
    try:
        # Determine next booking_id
        bookings = load_bookings()
        next_id = max([b['booking_id'] for b in bookings], default=0) + 1
        booking_line = f"{next_id}|{new_booking['member_name']}|{new_booking['trainer_id']}|{new_booking['booking_date']}|{new_booking['booking_time']}|{new_booking['duration_minutes']}|Confirmed\n"
        with open('data/bookings.txt', 'a', encoding='utf-8') as file:
            file.write(booking_line)
        return True
    except Exception as e:
        print(f"Error saving booking: {e}")
        return False


def save_workout(new_workout):
    # Append new workout to data/workouts.txt with correct format
    try:
        workouts = load_workouts()
        next_id = max([w['workout_id'] for w in workouts], default=0) + 1
        workout_line = f"{next_id}|{new_workout['member_name']}|{new_workout['workout_type']}|{new_workout['workout_date']}|{new_workout['duration_minutes']}|{new_workout['calories_burned']}|{new_workout['notes']}\n"
        with open('data/workouts.txt', 'a', encoding='utf-8') as file:
            file.write(workout_line)
        return True
    except Exception as e:
        print(f"Error saving workout: {e}")
        return False


# Routes implementing design_spec.md Section 1

# 1. Root Route
@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))


# 2. Dashboard Page
@app.route('/dashboard')
def dashboard():
    # For simplicity just mock member_status and featured_classes
    member_status = "Welcome back, valued member!"
    featured_classes = [
        {'class_id': 1, 'class_name': 'Morning Yoga', 'schedule_day': 'Monday', 'schedule_time': '06:00'},
        {'class_id': 2, 'class_name': 'CrossFit Bootcamp', 'schedule_day': 'Tuesday', 'schedule_time': '18:00'},
        {'class_id': 3, 'class_name': 'Pilates Core', 'schedule_day': 'Wednesday', 'schedule_time': '10:00'},
    ]
    return render_template('dashboard.html', member_status=member_status, featured_classes=featured_classes)


# 3. Membership Plans Page
@app.route('/memberships')
def memberships():
    plans = load_memberships()
    membership_types = ["Basic", "Premium", "Elite"]
    return render_template('memberships.html', plans=plans, membership_types=membership_types)


# 4. Plan Details Page
@app.route('/plan/<int:plan_id>')
def plan_details(plan_id):
    plans = load_memberships()
    plan = next((p for p in plans if p['membership_id'] == plan_id), None)
    plan_reviews = []  # No reviews source specified, provide empty list
    if plan is None:
        return "Plan not found", 404
    return render_template('plan_details.html', plan=plan, plan_reviews=plan_reviews)


# 5. Class Schedule Page
@app.route('/schedule')
def class_schedule():
    classes = load_classes()
    class_types = sorted(list(set(cls['class_type'] for cls in classes)))
    return render_template('schedule.html', classes=classes, class_types=class_types)


# 6. Trainer Profiles Page
@app.route('/trainers')
def trainers():
    trainers_list = load_trainers()
    specialties = sorted(list(set(trainer['specialty'] for trainer in trainers_list)))
    return render_template('trainers.html', trainers=trainers_list, specialties=specialties)


# 7. Trainer Detail Page
@app.route('/trainer/<int:trainer_id>')
def trainer_detail(trainer_id):
    trainers_list = load_trainers()
    trainer = next((t for t in trainers_list if t['trainer_id'] == trainer_id), None)
    trainer_reviews = []  # No reviews source specified, provide empty list
    if trainer is None:
        return "Trainer not found", 404
    return render_template('trainer_detail.html', trainer=trainer, trainer_reviews=trainer_reviews)


# 8. PT Booking Page
@app.route('/booking', methods=['GET', 'POST'])
def book_personal_training():
    trainers_list = load_trainers()
    time_slots = ['06:00', '07:00', '08:00', '09:00', '10:00',
                  '11:00', '12:00', '13:00', '14:00', '15:00',
                  '16:00', '17:00', '18:00', '19:00', '20:00']
    
    if request.method == 'POST':
        try:
            trainer_id = int(request.form['trainer_id'])
            session_date = request.form['session_date']
            session_time = request.form['session_time']
            duration = int(request.form['duration'])
            
            # Optional: member_name - not specified, use placeholder
            member_name = "Current Member"

            new_booking = {
                'member_name': member_name,
                'trainer_id': trainer_id,
                'booking_date': session_date,
                'booking_time': session_time,
                'duration_minutes': duration,
            }

            if save_booking(new_booking):
                return render_template('booking.html', trainers=trainers_list, time_slots=time_slots, confirmation="Booking confirmed!")
            else:
                return render_template('booking.html', trainers=trainers_list, time_slots=time_slots, error="Failed to save booking.")
        except Exception as e:
            return render_template('booking.html', trainers=trainers_list, time_slots=time_slots, error=f"Error: {e}")

    return render_template('booking.html', trainers=trainers_list, time_slots=time_slots)


# 9. Workout Records Page
@app.route('/workouts')
def workout_records():
    workouts = load_workouts()
    workout_types = sorted(list(set(workout['workout_type'] for workout in workouts)))
    return render_template('workouts.html', workouts=workouts, workout_types=workout_types)


# 10. Log Workout Page
@app.route('/log-workout', methods=['GET', 'POST'])
def log_workout():
    if request.method == 'POST':
        try:
            workout_type = request.form['workout_type']
            duration_minutes = int(request.form['duration_minutes'])
            calories_burned = int(request.form['calories_burned'])
            notes = request.form['notes']
            
            # Placeholder member_name as spec does not provide user session
            member_name = "Current Member"
            
            from datetime import date
            workout_date = date.today().isoformat()

            new_workout = {
                'member_name': member_name,
                'workout_type': workout_type,
                'workout_date': workout_date,
                'duration_minutes': duration_minutes,
                'calories_burned': calories_burned,
                'notes': notes,
            }

            if save_workout(new_workout):
                confirmation_message = "Workout logged successfully!"
                return render_template('log_workout.html', confirmation=confirmation_message)
            else:
                error_message = "Failed to save workout."
                return render_template('log_workout.html', error=error_message)
        except Exception as e:
            return render_template('log_workout.html', error=f"Error: {e}")

    return render_template('log_workout.html')


if __name__ == '__main__':
    app.run(debug=True, port=5000)
