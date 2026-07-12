from flask import Flask, render_template, request, redirect, url_for, flash
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

# Filenames for data storage
BOOKING_FILE = 'booking_data.txt'
INSURANCE_FILE = 'insurance_data.txt'

# Utility functions to read and write pipe-delimited data

def read_pipe_delimited_file(filename, expected_fields):
    records = []
    if not os.path.exists(filename):
        return records
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) == expected_fields:
                records.append(parts)
    return records


def write_pipe_delimited_file(filename, fields):
    with open(filename, 'a') as f:
        f.write('|'.join(fields) + '\n')


@app.route('/')
def index():
    # Redirect to main booking page
    return redirect(url_for('booking'))


@app.route('/booking', methods=['GET', 'POST'])
def booking():
    """
    Booking form route.
    Fields (assumed from spec, example): first_name, last_name, email, phone, date, time
    Validate all fields are non-empty; email format not implemented here explicitly.
    On POST, save booking data to file.
    On GET, show the form.
    """
    if request.method == 'POST':
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        date = request.form.get('date', '').strip()
        time = request.form.get('time', '').strip()

        errors = []
        if not first_name:
            errors.append('First name is required.')
        if not last_name:
            errors.append('Last name is required.')
        if not email:
            errors.append('Email is required.')
        if not phone:
            errors.append('Phone is required.')
        if not date:
            errors.append('Date is required.')
        if not time:
            errors.append('Time is required.')

        if errors:
            for e in errors:
                flash(e, 'error')
            return render_template('booking.html',
                                   first_name=first_name,
                                   last_name=last_name,
                                   email=email,
                                   phone=phone,
                                   date=date,
                                   time=time)

        # Save booking record
        write_pipe_delimited_file(BOOKING_FILE, [first_name, last_name, email, phone, date, time])

        # Redirect to insurance page (workflow)
        return redirect(url_for('insurance'))
    else:
        return render_template('booking.html')


@app.route('/insurance', methods=['GET', 'POST'])
def insurance():
    """
    Insurance selection form.
    Assume fields: policy_number, provider, coverage_type
    Validate non-empty.
    Save to file on POST.
    """
    if request.method == 'POST':
        policy_number = request.form.get('policy_number', '').strip()
        provider = request.form.get('provider', '').strip()
        coverage_type = request.form.get('coverage_type', '').strip()

        errors = []
        if not policy_number:
            errors.append('Policy number is required.')
        if not provider:
            errors.append('Provider is required.')
        if not coverage_type:
            errors.append('Coverage type is required.')

        if errors:
            for e in errors:
                flash(e, 'error')
            return render_template('insurance.html',
                                   policy_number=policy_number,
                                   provider=provider,
                                   coverage_type=coverage_type)

        # Save insurance record
        write_pipe_delimited_file(INSURANCE_FILE, [policy_number, provider, coverage_type])

        # Redirect or render thanks or next step
        return render_template('insurance_success.html', policy_number=policy_number)

    else:
        return render_template('insurance.html')


if __name__ == '__main__':
    app.run(debug=True)
