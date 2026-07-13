from flask import Flask, render_template, request, redirect, url_for, flash, session
import os
import datetime
import re

app = Flask(__name__)
app.secret_key = 'supersecretkey'

DATA_DIR = 'data'

# Utility functions to read/write pipe-delimited files

def read_data_file(filename):
    filepath = os.path.join(DATA_DIR, filename)
    if not os.path.exists(filepath):
        return []
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]
    return lines


def write_data_file(filename, lines):
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n' if lines else '')


def read_pets():
    pets = []
    for line in read_data_file('pets.txt'):
        parts = line.split('|')
        if len(parts) == 11:
            pets.append({
                'pet_id': parts[0],
                'name': parts[1],
                'species': parts[2],
                'breed': parts[3],
                'age': parts[4],
                'gender': parts[5],
                'size': parts[6],
                'description': parts[7],
                'shelter_id': parts[8],
                'status': parts[9],
                'date_added': parts[10]
            })
    return pets


def write_pets(pets):
    lines = []
    for pet in pets:
        lines.append('|'.join([
            pet['pet_id'],
            pet['name'],
            pet['species'],
            pet['breed'],
            pet['age'],
            pet['gender'],
            pet['size'],
            pet['description'],
            pet['shelter_id'],
            pet['status'],
            pet['date_added']
        ]))
    write_data_file('pets.txt', lines)


def read_users():
    users = []
    for line in read_data_file('users.txt'):
        parts = line.split('|')
        if len(parts) == 4:
            users.append({
                'username': parts[0],
                'email': parts[1],
                'phone': parts[2],
                'address': parts[3]
            })
    return users


def write_users(users):
    lines = []
    for user in users:
        lines.append('|'.join([
            user['username'],
            user['email'],
            user['phone'],
            user['address']
        ]))
    write_data_file('users.txt', lines)


def read_applications():
    applications = []
    for line in read_data_file('applications.txt'):
        parts = line.split('|')
        if len(parts) == 13:
            applications.append({
                'application_id': parts[0],
                'username': parts[1],
                'pet_id': parts[2],
                'applicant_name': parts[3],
                'phone': parts[4],
                'address': parts[5],
                'housing_type': parts[6],
                'has_yard': parts[7],
                'other_pets': parts[8],
                'experience': parts[9],
                'reason': parts[10],
                'status': parts[11],
                'date_submitted': parts[12]
            })
    return applications


def write_applications(applications):
    lines = []
    for app in applications:
        lines.append('|'.join([
            app['application_id'],
            app['username'],
            app['pet_id'],
            app['applicant_name'],
            app['phone'],
            app['address'],
            app['housing_type'],
            app['has_yard'],
            app['other_pets'],
            app['experience'],
            app['reason'],
            app['status'],
            app['date_submitted'],
        ]))
    write_data_file('applications.txt', lines)


def read_favorites():
    favorites = []
    for line in read_data_file('favorites.txt'):
        parts = line.split('|')
        if len(parts) == 3:
            favorites.append({
                'username': parts[0],
                'pet_id': parts[1],
                'date_added': parts[2]
            })
    return favorites


def write_favorites(favorites):
    lines = []
    for fav in favorites:
        lines.append('|'.join([
            fav['username'],
            fav['pet_id'],
            fav['date_added'],
        ]))
    write_data_file('favorites.txt', lines)


def read_messages():
    messages = []
    for line in read_data_file('messages.txt'):
        parts = line.split('|')
        if len(parts) == 7:
            messages.append({
                'message_id': parts[0],
                'sender_username': parts[1],
                'recipient_username': parts[2],
                'subject': parts[3],
                'content': parts[4],
                'timestamp': parts[5],
                'is_read': parts[6] == 'true'
            })
    return messages


def write_messages(messages):
    lines = []
    for msg in messages:
        lines.append('|'.join([
            msg['message_id'],
            msg['sender_username'],
            msg['recipient_username'],
            msg['subject'],
            msg['content'],
            msg['timestamp'],
            'true' if msg['is_read'] else 'false'
        ]))
    write_data_file('messages.txt', lines)


def read_shelters():
    shelters = []
    for line in read_data_file('shelters.txt'):
        parts = line.split('|')
        if len(parts) == 5:
            shelters.append({
                'shelter_id': parts[0],
                'name': parts[1],
                'address': parts[2],
                'phone': parts[3],
                'email': parts[4]
            })
    return shelters


# Assume current user to simulate login (for demo and UI purposes), fixed
CURRENT_USER = 'john_doe'

@app.before_request
def load_user():
    session['username'] = CURRENT_USER

# Helper functions for validation

def validate_age(age):
    return re.match(r'^\d+ years$', age) is not None

def validate_phone(phone):
    return re.match(r'^\d{3}-\d{4}$', phone) or re.match(r'^\d{3}-\d{3}-\d{4}$', phone)

def validate_email(email):
    return re.match(r'^\S+@\S+\.\S+$', email) is not None

# Helper functions to generate unique IDs

def generate_new_pet_id(pets):
    max_id = 0
    for pet in pets:
        try:
            pid = int(pet['pet_id'])
            if pid > max_id:
                max_id = pid
        except:
            pass
    return str(max_id + 1)

def generate_new_application_id(applications):
    max_id = 0
    for app in applications:
        try:
            aid = int(app['application_id'])
            if aid > max_id:
                max_id = aid
        except:
            pass
    return str(max_id + 1)

def generate_new_message_id(messages):
    max_id = 0
    for msg in messages:
        try:
            mid = int(msg['message_id'])
            if mid > max_id:
                max_id = mid
        except:
            pass
    return str(max_id + 1)

# Routes

# 1. Dashboard
@app.route('/dashboard')
def dashboard():
    pets = read_pets()
    featured_pets = [pet for pet in pets if pet['status'] == 'Available'][:5]
    return render_template('dashboard.html', page_title='Pet Adoption Dashboard', featured_pets=featured_pets)

# 2. Pet Listings
@app.route('/pets', methods=['GET'])
def pet_listings():
    pets = read_pets()
    search = request.args.get('search', '').strip().lower()
    filter_species = request.args.get('species', 'All')
    filtered_pets = []
    for pet in pets:
        if pet['status'] != 'Available':
            continue
        if filter_species != 'All' and pet['species'] != filter_species:
            continue
        if search and search not in pet['name'].lower():
            continue
        filtered_pets.append(pet)

    return render_template('pets.html', page_title='Available Pets', pets=filtered_pets, search=search, filter_species=filter_species)

# 3. Pet Details
@app.route('/pets/<pet_id>', methods=['GET', 'POST'])
def pet_details(pet_id):
    pets = read_pets()
    favorites = read_favorites()
    username = session.get('username')
    pet = next((p for p in pets if p['pet_id'] == pet_id), None)
    if not pet:
        flash('Pet not found.', 'error')
        return redirect(url_for('pet_listings'))

    is_favorite = any(f['username'] == username and f['pet_id'] == pet_id for f in favorites)

    if request.method == 'POST':
        action = request.form.get('favorite_action')
        if action == 'add' and not is_favorite:
            favorites.append({'username': username, 'pet_id': pet_id, 'date_added': datetime.date.today().isoformat()})
            write_favorites(favorites)
            flash('Pet added to favorites.', 'success')
        elif action == 'remove' and is_favorite:
            favorites = [f for f in favorites if not (f['username'] == username and f['pet_id'] == pet_id)]
            write_favorites(favorites)
            flash('Pet removed from favorites.', 'success')
        return redirect(url_for('pet_details', pet_id=pet_id))

    return render_template('pet_details.html', page_title='Pet Details', pet=pet, is_favorite=is_favorite)

# 4. Add Pet
@app.route('/add-pet', methods=['GET', 'POST'])
def add_pet():
    species_options = ['Dog', 'Cat', 'Bird', 'Rabbit', 'Other']
    gender_options = ['Male', 'Female']
    size_options = ['Small', 'Medium', 'Large']

    if request.method == 'POST':
        name = request.form.get('pet_name_input', '').strip()
        species = request.form.get('pet_species_input', '')
        breed = request.form.get('pet_breed_input', '').strip()
        age = request.form.get('pet_age_input', '').strip()
        gender = request.form.get('pet_gender_input', '')
        size = request.form.get('pet_size_input', '')
        description = request.form.get('pet_description_input', '').strip()

        errors = []
        if not name:
            errors.append('Pet name is required.')
        if species not in species_options:
            errors.append('Invalid species selected.')
        if gender not in gender_options:
            errors.append('Invalid gender selected.')
        if size not in size_options:
            errors.append('Invalid size selected.')
        if not validate_age(age):
            errors.append('Age must be in format like "2 years".')

        if errors:
            for err in errors:
                flash(err, 'error')
            return render_template('add_pet.html', page_title='Add New Pet', form=request.form)

        pets = read_pets()
        new_id = generate_new_pet_id(pets)
        date_added = datetime.date.today().isoformat()
        new_pet = {
            'pet_id': new_id,
            'name': name,
            'species': species,
            'breed': breed,
            'age': age,
            'gender': gender,
            'size': size,
            'description': description,
            'shelter_id': '1',
            'status': 'Available',
            'date_added': date_added
        }
        pets.append(new_pet)
        write_pets(pets)
        flash('New pet added successfully.', 'success')
        return redirect(url_for('dashboard'))

    return render_template('add_pet.html', page_title='Add New Pet', form=None)

# 5. Adoption Application
@app.route('/adopt/<pet_id>', methods=['GET', 'POST'])
def adoption_application(pet_id):
    pets = read_pets()
    pet = next((p for p in pets if p['pet_id'] == pet_id), None)
    if not pet:
        flash('Pet not found.', 'error')
        return redirect(url_for('pet_listings'))

    if request.method == 'POST':
        applicant_name = request.form.get('applicant_name', '').strip()
        applicant_phone = request.form.get('applicant_phone', '').strip()
        housing_type = request.form.get('housing_type', '')
        reason = request.form.get('reason', '').strip()

        errors = []
        if not applicant_name:
            errors.append('Applicant name is required.')
        if not validate_phone(applicant_phone):
            errors.append('Phone number format is invalid. Use XXX-XXXX or XXX-XXX-XXXX.')
        if not reason:
            errors.append('Reason for adoption is required.')

        if errors:
            for err in errors:
                flash(err, 'error')
            return render_template('adoption_application.html', page_title='Adoption Application', pet=pet, applicant_name=applicant_name, applicant_phone=applicant_phone, housing_type=housing_type, reason=reason)

        applications = read_applications()
        new_id = generate_new_application_id(applications)

        username = session.get('username')
        users = read_users()
        user = next((u for u in users if u['username'] == username), None)
        address = user['address'] if user else ''

        date_submitted = datetime.date.today().isoformat()

        new_app = {
            'application_id': new_id,
            'username': username,
            'pet_id': pet_id,
            'applicant_name': applicant_name,
            'phone': applicant_phone,
            'address': address,
            'housing_type': housing_type,
            'has_yard': 'No',
            'other_pets': '',
            'experience': '',
            'reason': reason,
            'status': 'Pending',
            'date_submitted': date_submitted
        }
        applications.append(new_app)
        write_applications(applications)
        flash('Application submitted successfully.', 'success')
        return redirect(url_for('my_applications'))

    return render_template('adoption_application.html', page_title='Adoption Application', pet=pet, form=None)

# 6. My Applications
@app.route('/my-applications', methods=['GET'])
def my_applications():
    applications = read_applications()
    pets = read_pets()
    username = session.get('username')
    # Fix filter param name to match template
    filter_status = request.args.get('status', 'All')

    user_apps = [app for app in applications if app['username'] == username]
    if filter_status != 'All':
        user_apps = [app for app in user_apps if app['status'] == filter_status]

    pet_dict = {pet['pet_id']: pet for pet in pets}
    for app in user_apps:
        pet = pet_dict.get(app['pet_id'])
        app['pet_name'] = pet['name'] if pet else 'Unknown'

    return render_template('my_applications.html', page_title='My Applications', applications=user_apps, filter_status=filter_status)

# 7. Favorites
@app.route('/favorites', methods=['GET'])
def favorites():
    username = session.get('username')
    favorites = read_favorites()
    pets = read_pets()

    fav_pets = []
    pet_dict = {pet['pet_id']: pet for pet in pets}
    for fav in favorites:
        if fav['username'] == username:
            pet = pet_dict.get(fav['pet_id'])
            if pet and pet['status'] == 'Available':
                fav_pets.append(pet)

    return render_template('favorites.html', page_title='My Favorites', pets=fav_pets)

# 8. Messages
@app.route('/messages', methods=['GET', 'POST'])
def messages():
    username = session.get('username')
    messages = read_messages()
    interlocutors = set()
    conversations = {}

    for msg in messages:
        if msg['sender_username'] == username:
            interlocutors.add(msg['recipient_username'])
        elif msg['recipient_username'] == username:
            interlocutors.add(msg['sender_username'])

    for interlocutor in interlocutors:
        conv_msgs = [m for m in messages if (m['sender_username'] == username and m['recipient_username'] == interlocutor) or (m['sender_username'] == interlocutor and m['recipient_username'] == username)]
        conv_msgs.sort(key=lambda x: x['timestamp'])
        conversations[interlocutor] = conv_msgs

    selected = request.args.get('conversation')
    selected_conv = []
    if selected and selected in conversations:
        selected_conv = conversations[selected]
        changed = False
        for msg in selected_conv:
            if msg['recipient_username'] == username and not msg['is_read']:
                msg['is_read'] = True
                changed = True
        if changed:
            write_messages(messages)
    else:
        selected = None

    if request.method == 'POST':
        recipient = request.form.get('recipient_username', '').strip()
        subject = request.form.get('subject', '').strip()
        content = request.form.get('message_input', '').strip()

        if not recipient:
            flash('Recipient username is required.', 'error')
        elif not content:
            flash('Message content cannot be empty.', 'error')
        else:
            new_id = generate_new_message_id(messages)
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            sender = username
            new_msg = {
                'message_id': new_id,
                'sender_username': sender,
                'recipient_username': recipient,
                'subject': subject if subject else 'No Subject',
                'content': content,
                'timestamp': timestamp,
                'is_read': False
            }
            messages.append(new_msg)
            write_messages(messages)
            flash('Message sent successfully.', 'success')
            return redirect(url_for('messages', conversation=recipient))

    return render_template('messages.html', page_title='Messages', conversations=conversations, selected_conversation=selected, selected_conv=selected_conv)

# 9. User Profile
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    username = session.get('username')
    users = read_users()
    user = next((u for u in users if u['username'] == username), None)
    if not user:
        user = {'username': username, 'email': '', 'phone': '', 'address': ''}

    if request.method == 'POST':
        email = request.form.get('profile_email', '').strip()
        if not validate_email(email):
            flash('Invalid email format.', 'error')
        else:
            user['email'] = email
            new_users = [u for u in users if u['username'] != username]
            new_users.append(user)
            write_users(new_users)
            flash('Profile updated successfully.', 'success')
            return redirect(url_for('profile'))

    return render_template('profile.html', page_title='My Profile', user=user)

# 10. Admin Panel
@app.route('/admin-panel', methods=['GET', 'POST'])
def admin_panel():
    pets = read_pets()
    applications = read_applications()

    username = session.get('username')
    if username != 'admin_user':
        flash('Access denied. Admins only.', 'error')
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        action = request.form.get('action')
        application_id = request.form.get('application_id')
        if action in ['approve', 'reject'] and application_id:
            applications = read_applications()
            app_found = False
            for app in applications:
                if app['application_id'] == application_id and app['status'] == 'Pending':
                    app_found = True
                    if action == 'approve':
                        app['status'] = 'Approved'
                        for pet in pets:
                            if pet['pet_id'] == app['pet_id']:
                                pet['status'] = 'Pending'
                                break
                    elif action == 'reject':
                        app['status'] = 'Rejected'
                    break
            if app_found:
                write_applications(applications)
                write_pets(pets)
                flash('Application status updated.', 'success')
            else:
                flash('Application not found or already processed.', 'error')
            return redirect(url_for('admin_panel'))

        pet_del_id = request.form.get('delete_pet_id')
        if pet_del_id:
            pets = [pet for pet in pets if pet['pet_id'] != pet_del_id]
            write_pets(pets)
            flash('Pet deleted successfully.', 'success')
            return redirect(url_for('admin_panel'))

    pending_apps = [app for app in applications if app['status'] == 'Pending']

    return render_template('admin_panel.html', page_title='Admin Panel', pending_applications=pending_apps, pets=pets)

# Root redirect
@app.route('/')
def root():
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    app.run(debug=True)
