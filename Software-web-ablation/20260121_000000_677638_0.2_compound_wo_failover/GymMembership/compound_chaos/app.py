from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

# Data file paths
clients_file = 'data/clients.txt'
trainers_file = 'data/trainers.txt'
sessions_file = 'data/sessions.txt'
bookings_file = 'data/bookings.txt'
workouts_file = 'data/workouts.txt'

#===============================
# Helper functions to load and save data
#===============================

def load_clients():
    clients = []
    try:
        with open(clients_file, 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 3:
                    continue
                client = {
                    'client_id': parts[0],
                    'name': parts[1],
                    'email': parts[2]
                }
                clients.append(client)
    except IOError:
        pass
    return clients


def load_trainers():
    trainers = []
    try:
        with open(trainers_file, 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 3:
                    continue
                trainer = {
                    'trainer_id': parts[0],
                    'name': parts[1],
                    'specialty': parts[2]
                }
                trainers.append(trainer)
    except IOError:
        pass
    return trainers


def load_sessions():
    sessions = []
    try:
        with open(sessions_file, 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 4:
                    continue
                session = {
                    'session_id': parts[0],
                    'trainer_id': parts[1],
                    'date': parts[2],
                    'time': parts[3]
                }
                sessions.append(session)
    except IOError:
        pass
    return sessions


def load_bookings():
    bookings = []
    try:
        with open(bookings_file, 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 4:
                    continue
                booking = {
                    'booking_id': parts[0],
                    'client_id': parts[1],
                    'session_id': parts[2],
                    'status': parts[3]
                }
                bookings.append(booking)
    except IOError:
        pass
    return bookings


def save_booking(booking_id, client_id, session_id, status):
    try:
        with open(bookings_file, 'a') as f:
            line = f'{booking_id}|{client_id}|{session_id}|{status}\n'
            f.write(line)
        return True
    except IOError:
        return False


def load_workouts():
    workouts = []
    try:
        with open(workouts_file, 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 5:
                    continue
                workout = {
                    'workout_id': parts[0],
                    'client_id': parts[1],
                    'trainer_id': parts[2],
                    'date': parts[3],
                    'description': parts[4]
                }
                workouts.append(workout)
    except IOError:
        pass
    return workouts


def save_workout(workout_id, client_id, trainer_id, date, description):
    try:
        with open(workouts_file, 'a') as f:
            line = f'{workout_id}|{client_id}|{trainer_id}|{date}|{description}\n'
            f.write(line)
        return True
    except IOError:
        return False


#===============================
# Routes
#===============================

@app.route('/')
def root():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    clients = load_clients()
    trainers = load_trainers()
    sessions = load_sessions()
    bookings = load_bookings()
    workouts = load_workouts()
    # Pass counts of each
    context = {
        'num_clients': len(clients),
        'num_trainers': len(trainers),
        'num_sessions': len(sessions),
        'num_bookings': len(bookings),
        'num_workouts': len(workouts)
    }
    return render_template('dashboard.html', **context)


@app.route('/clients')
def clients():
    clients = load_clients()
    return render_template('clients.html', clients=clients)


@app.route('/trainers')
def trainers():
    trainers = load_trainers()
    return render_template('trainers.html', trainers=trainers)


@app.route('/sessions')
def sessions():
    sessions = load_sessions()
    trainers = load_trainers()
    # enrich sessions with trainer name for display
    for session in sessions:
        trainer = next((t for t in trainers if t['trainer_id'] == session['trainer_id']), None)
        session['trainer_name'] = trainer['name'] if trainer else 'Unknown'
    return render_template('sessions.html', sessions=sessions)


@app.route('/bookings', methods=['GET', 'POST'])
def bookings():
    if request.method == 'POST':
        client_id = request.form.get('client_id', '').strip()
        session_id = request.form.get('session_id', '').strip()
        if not client_id or not session_id:
            # Missing data - simply reload bookings page
            clients = load_clients()
            sessions_ = load_sessions()
            return render_template('bookings.html', bookings=load_bookings(), clients=clients, sessions=sessions_, error='Client and Session must be selected')
        # Generate booking_id (max existing + 1)
        bookings_list = load_bookings()
        max_id = 0
        for b in bookings_list:
            try:
                bid = int(b['booking_id'])
                if bid > max_id:
                    max_id = bid
            except ValueError:
                continue
        new_booking_id = str(max_id + 1)
        success = save_booking(new_booking_id, client_id, session_id, 'booked')
        if success:
            return redirect(url_for('bookings'))
        else:
            clients = load_clients()
            sessions_ = load_sessions()
            return render_template('bookings.html', bookings=load_bookings(), clients=clients, sessions=sessions_, error='Failed to save booking')

    # GET
    clients = load_clients()
    sessions_ = load_sessions()
    bookings_list = load_bookings()
    return render_template('bookings.html', bookings=bookings_list, clients=clients, sessions=sessions_)


@app.route('/workouts', methods=['GET', 'POST'])
def workouts():
    if request.method == 'POST':
        client_id = request.form.get('client_id', '').strip()
        trainer_id = request.form.get('trainer_id', '').strip()
        date = request.form.get('date', '').strip()
        description = request.form.get('description', '').strip()

        if not (client_id and trainer_id and date and description):
            # Missing data - reload with error
            clients = load_clients()
            trainers = load_trainers()
            return render_template('workouts.html', workouts=load_workouts(), clients=clients, trainers=trainers, error='All fields are required')

        # Generate workout_id (max existing + 1)
        workouts_list = load_workouts()
        max_id = 0
        for w in workouts_list:
            try:
                wid = int(w['workout_id'])
                if wid > max_id:
                    max_id = wid
            except ValueError:
                continue
        new_workout_id = str(max_id + 1)
        success = save_workout(new_workout_id, client_id, trainer_id, date, description)
        if success:
            return redirect(url_for('workouts'))
        else:
            clients = load_clients()
            trainers = load_trainers()
            return render_template('workouts.html', workouts=load_workouts(), clients=clients, trainers=trainers, error='Failed to save workout')

    # GET
    clients = load_clients()
    trainers = load_trainers()
    workouts_list = load_workouts()
    return render_template('workouts.html', workouts=workouts_list, clients=clients, trainers=trainers)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
