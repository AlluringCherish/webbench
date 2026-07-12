from flask import Flask, render_template, redirect, url_for, request
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

data_folder = 'data'

# File paths
PATIENTS_FILE = os.path.join(data_folder, 'patients.txt')
DOCTORS_FILE = os.path.join(data_folder, 'doctors.txt')
APPOINTMENTS_FILE = os.path.join(data_folder, 'appointments.txt')

# Utility functions to read and write pipe-delimited files

def read_file(filepath, fields):
    data = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != len(fields):
                    continue  # skip malformed lines
                entry = dict(zip(fields, parts))
                data.append(entry)
    except FileNotFoundError:
        # File does not exist, return empty list
        pass
    except Exception as e:
        # Any other error, log or handle as needed
        print(f'Error reading {filepath}: {e}')
    return data

def write_file(filepath, data, fields):
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            for entry in data:
                line = '|'.join(entry[field] for field in fields)
                f.write(line + '\n')
        return True
    except Exception as e:
        print(f'Error writing to {filepath}: {e}')
        return False

# Data schemas
PATIENT_FIELDS = ['patient_id', 'name', 'email', 'phone']
DOCTOR_FIELDS = ['doctor_id', 'name', 'specialty', 'email']
APPOINTMENT_FIELDS = ['appointment_id', 'patient_id', 'doctor_id', 'date', 'time', 'status']

# Routes - Section 1

# 1 Root route redirects to dashboard
@app.route('/')
def root():
    return redirect(url_for('dashboard'))

# 2 Dashboard route
@app.route('/dashboard')
def dashboard():
    patients = read_file(PATIENTS_FILE, PATIENT_FIELDS)
    doctors = read_file(DOCTORS_FILE, DOCTOR_FIELDS)
    appointments = read_file(APPOINTMENTS_FILE, APPOINTMENT_FIELDS)
    return render_template('dashboard.html', patients=patients, doctors=doctors, appointments=appointments)

# 3 Patients list
@app.route('/patients')
def patients():
    patients = read_file(PATIENTS_FILE, PATIENT_FIELDS)
    return render_template('patients.html', patients=patients)

# 4 Add patient (GET and POST)
@app.route('/patients/add', methods=['GET', 'POST'])
def add_patient():
    if request.method == 'POST':
        # Extract and validate form data
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        if not name or not email or not phone:
            error = 'All fields are required.'
            return render_template('add_patient.html', error=error, name=name, email=email, phone=phone)

        # Load existing patients
        patients = read_file(PATIENTS_FILE, PATIENT_FIELDS)
        # Generate new patient_id
        max_id = 0
        for p in patients:
            try:
                pid = int(p['patient_id'])
                if pid > max_id:
                    max_id = pid
            except ValueError:
                continue
        new_id = str(max_id + 1)

        new_patient = {
            'patient_id': new_id,
            'name': name,
            'email': email,
            'phone': phone
        }
        patients.append(new_patient)
        success = write_file(PATIENTS_FILE, patients, PATIENT_FIELDS)
        if not success:
            error = 'Failed to save patient data.'
            return render_template('add_patient.html', error=error, name=name, email=email, phone=phone)

        return redirect(url_for('patients'))
    else:
        return render_template('add_patient.html')

# 5 Doctors list
@app.route('/doctors')
def doctors():
    doctors = read_file(DOCTORS_FILE, DOCTOR_FIELDS)
    return render_template('doctors.html', doctors=doctors)

# 6 Add doctor (GET and POST)
@app.route('/doctors/add', methods=['GET', 'POST'])
def add_doctor():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        specialty = request.form.get('specialty', '').strip()
        email = request.form.get('email', '').strip()
        if not name or not specialty or not email:
            error = 'All fields are required.'
            return render_template('add_doctor.html', error=error, name=name, specialty=specialty, email=email)

        doctors = read_file(DOCTORS_FILE, DOCTOR_FIELDS)
        max_id = 0
        for d in doctors:
            try:
                did = int(d['doctor_id'])
                if did > max_id:
                    max_id = did
            except ValueError:
                continue
        new_id = str(max_id + 1)

        new_doctor = {
            'doctor_id': new_id,
            'name': name,
            'specialty': specialty,
            'email': email
        }
        doctors.append(new_doctor)
        success = write_file(DOCTORS_FILE, doctors, DOCTOR_FIELDS)
        if not success:
            error = 'Failed to save doctor data.'
            return render_template('add_doctor.html', error=error, name=name, specialty=specialty, email=email)

        return redirect(url_for('doctors'))
    else:
        return render_template('add_doctor.html')

# 7 Appointments list
@app.route('/appointments')
def appointments():
    appointments = read_file(APPOINTMENTS_FILE, APPOINTMENT_FIELDS)
    patients = read_file(PATIENTS_FILE, PATIENT_FIELDS)
    doctors = read_file(DOCTORS_FILE, DOCTOR_FIELDS)
    return render_template('appointments.html', appointments=appointments, patients=patients, doctors=doctors)

# 8 Add appointment (GET and POST)
@app.route('/appointments/add', methods=['GET', 'POST'])
def add_appointment():
    if request.method == 'POST':
        patient_id = request.form.get('patient_id', '').strip()
        doctor_id = request.form.get('doctor_id', '').strip()
        date = request.form.get('date', '').strip()
        time = request.form.get('time', '').strip()
        status = request.form.get('status', '').strip()

        if not patient_id or not doctor_id or not date or not time or not status:
            error = 'All fields are required.'
            patients = read_file(PATIENTS_FILE, PATIENT_FIELDS)
            doctors = read_file(DOCTORS_FILE, DOCTOR_FIELDS)
            return render_template('add_appointment.html', error=error, patients=patients, doctors=doctors, 
                                   patient_id=patient_id, doctor_id=doctor_id, date=date, time=time, status=status)

        # Validate patient_id and doctor_id exists
        patients = read_file(PATIENTS_FILE, PATIENT_FIELDS)
        doctors = read_file(DOCTORS_FILE, DOCTOR_FIELDS)
        if not any(p['patient_id'] == patient_id for p in patients):
            error = 'Invalid patient ID.'
            return render_template('add_appointment.html', error=error, patients=patients, doctors=doctors, 
                                   patient_id=patient_id, doctor_id=doctor_id, date=date, time=time, status=status)
        if not any(d['doctor_id'] == doctor_id for d in doctors):
            error = 'Invalid doctor ID.'
            return render_template('add_appointment.html', error=error, patients=patients, doctors=doctors, 
                                   patient_id=patient_id, doctor_id=doctor_id, date=date, time=time, status=status)

        appointments = read_file(APPOINTMENTS_FILE, APPOINTMENT_FIELDS)
        max_id = 0
        for a in appointments:
            try:
                aid = int(a['appointment_id'])
                if aid > max_id:
                    max_id = aid
            except ValueError:
                continue
        new_id = str(max_id + 1)

        new_appointment = {
            'appointment_id': new_id,
            'patient_id': patient_id,
            'doctor_id': doctor_id,
            'date': date,
            'time': time,
            'status': status
        }
        appointments.append(new_appointment)
        success = write_file(APPOINTMENTS_FILE, appointments, APPOINTMENT_FIELDS)
        if not success:
            error = 'Failed to save appointment data.'
            patients = read_file(PATIENTS_FILE, PATIENT_FIELDS)
            doctors = read_file(DOCTORS_FILE, DOCTOR_FIELDS)
            return render_template('add_appointment.html', error=error, patients=patients, doctors=doctors, 
                                   patient_id=patient_id, doctor_id=doctor_id, date=date, time=time, status=status)

        return redirect(url_for('appointments'))
    else:
        patients = read_file(PATIENTS_FILE, PATIENT_FIELDS)
        doctors = read_file(DOCTORS_FILE, DOCTOR_FIELDS)
        return render_template('add_appointment.html', patients=patients, doctors=doctors)

if __name__ == '__main__':
    app.run(debug=True)