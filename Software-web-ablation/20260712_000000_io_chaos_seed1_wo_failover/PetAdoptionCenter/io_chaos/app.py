from flask import Flask, render_template, redirect, url_for, request
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# -------- Helper Functions for Data Handling -------- #

def _read_file_lines(filename):
    path = os.path.join(DATA_DIR, filename)
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.readlines()
    except FileNotFoundError:
        return []

def _write_file_lines(filename, lines):
    path = os.path.join(DATA_DIR, filename)
    try:
        with open(path, 'w', encoding='utf-8') as f:
            for line in lines:
                f.write(line.rstrip('\n') + '\n')
        return True
    except Exception as e:
        return False

# ---- Users ---- #
def load_users():
    users = []
    lines = _read_file_lines('users.txt')
    for line in lines:
        fields = line.strip().split('|')
        if len(fields) == 4:
            users.append({
                'username': fields[0],
                'email': fields[1],
                'phone': fields[2],
                'address': fields[3]
            })
    return users

def get_user_by_username(username):
    users = load_users()
    for user in users:
        if user['username'] == username:
            return user
    return None

def update_user_email(username, new_email):
    users = load_users()
    updated = False
    for user in users:
        if user['username'] == username:
            user['email'] = new_email
            updated = True
            break
    if updated:
        lines = ['|'.join([u['username'], u['email'], u['phone'], u['address']]) for u in users]
        _write_file_lines('users.txt', lines)
    return updated

# ---- Pets ---- #
def load_pets():
    pets = []
    lines = _read_file_lines('pets.txt')
    for line in lines:
        fields = line.strip().split('|')
        if len(fields) == 11:
            try:
                pet_id = int(fields[0])
                shelter_id = int(fields[8])
                pets.append({
                    'pet_id': pet_id,
                    'name': fields[1],
                    'species': fields[2],
                    'breed': fields[3],
                    'age': fields[4],
                    'gender': fields[5],
                    'size': fields[6],
                    'description': fields[7],
                    'shelter_id': shelter_id,
                    'status': fields[9],
                    'date_added': fields[10]
                })
            except ValueError:
                continue
    return pets

def get_pet_by_id(pet_id):
    pets = load_pets()
    for pet in pets:
        if pet['pet_id'] == pet_id:
            return pet
    return None

def add_new_pet(pet_data):
    pets = load_pets()
    max_id = max([p['pet_id'] for p in pets], default=0)
    new_id = max_id + 1
    new_pet = {
        'pet_id': new_id,
        'name': pet_data['name'],
        'species': pet_data['species'],
        'breed': pet_data['breed'],
        'age': pet_data['age'],
        'gender': pet_data['gender'],
        'size': pet_data['size'],
        'description': pet_data['description'],
        'shelter_id': 1,  # Default shelter_id as 1
        'status': 'Available',
        'date_added': datetime.now().strftime('%Y-%m-%d')
    }
    pets.append(new_pet)
    lines = []
    for pet in pets:
        line = '|'.join([
            str(pet['pet_id']),
            pet['name'],
            pet['species'],
            pet['breed'],
            pet['age'],
            pet['gender'],
            pet['size'],
            pet['description'],
            str(pet['shelter_id']),
            pet['status'],
            pet['date_added']
        ])
        lines.append(line)
    success = _write_file_lines('pets.txt', lines)
    return success

# ---- Applications ---- #
def load_applications():
    applications = []
    lines = _read_file_lines('applications.txt')
    for line in lines:
        fields = line.strip().split('|')
        if len(fields) == 13:
            try:
                application_id = int(fields[0])
                pet_id = int(fields[2])
                applications.append({
                    'application_id': application_id,
                    'username': fields[1],
                    'pet_id': pet_id,
                    'applicant_name': fields[3],
                    'phone': fields[4],
                    'address': fields[5],
                    'housing_type': fields[6],
                    'has_yard': fields[7],
                    'other_pets': fields[8],
                    'experience': fields[9],
                    'reason': fields[10],
                    'status': fields[11],
                    'date_submitted': fields[12]
                })
            except ValueError:
                continue
    return applications

def get_application_by_id(application_id):
    applications = load_applications()
    for app in applications:
        if app['application_id'] == application_id:
            return app
    return None

def add_application(app_data):
    applications = load_applications()
    max_id = max([a['application_id'] for a in applications], default=0)
    new_id = max_id + 1
    username = app_data.get('username', '')
    new_app = {
        'application_id': new_id,
        'username': username,
        'pet_id': app_data['pet_id'],
        'applicant_name': app_data['applicant_name'],
        'phone': app_data.get('phone', ''),
        'address': app_data.get('address', ''),
        'housing_type': app_data['housing_type'],
        'has_yard': app_data.get('has_yard', 'No'),  # default No if not provided
        'other_pets': app_data.get('other_pets', ''),
        'experience': app_data.get('experience', ''),
        'reason': app_data['reason'],
        'status': 'Pending',
        'date_submitted': datetime.now().strftime('%Y-%m-%d')
    }
    applications.append(new_app)
    lines = []
    for a in applications:
        line = '|'.join([
            str(a['application_id']), 
            a['username'], 
            str(a['pet_id']), 
            a['applicant_name'], 
            a['phone'], 
            a['address'], 
            a['housing_type'], 
            a['has_yard'], 
            a['other_pets'], 
            a['experience'], 
            a['reason'], 
            a['status'], 
            a['date_submitted']
        ])
        lines.append(line)
    success = _write_file_lines('applications.txt', lines)
    return success

def update_application_status(application_id, new_status):
    applications = load_applications()
    updated = False
    for app in applications:
        if app['application_id'] == application_id:
            app['status'] = new_status
            updated = True
            break
    if updated:
        lines = []
        for a in applications:
            line = '|'.join([
                str(a['application_id']),
                a['username'],
                str(a['pet_id']),
                a['applicant_name'],
                a['phone'],
                a['address'],
                a['housing_type'],
                a['has_yard'],
                a['other_pets'],
                a['experience'],
                a['reason'],
                a['status'],
                a['date_submitted']
            ])
            lines.append(line)
        _write_file_lines('applications.txt', lines)
    return updated

# ---- Favorites ---- #
def load_favorites():
    favorites = []
    lines = _read_file_lines('favorites.txt')
    for line in lines:
        fields = line.strip().split('|')
        if len(fields) == 3:
            try:
                pet_id = int(fields[1])
                favorites.append({
                    'username': fields[0],
                    'pet_id': pet_id,
                    'date_added': fields[2]
                })
            except ValueError:
                continue
    return favorites

def load_favorites_by_username(username):
    all_favorites = load_favorites()
    return [fav for fav in all_favorites if fav['username'] == username]

# ---- Messages ---- #
def load_messages():
    messages = []
    lines = _read_file_lines('messages.txt')
    for line in lines:
        fields = line.strip().split('|')
        if len(fields) == 7:
            try:
                message_id = int(fields[0])
                is_read = fields[6].lower() == 'true'
                messages.append({
                    'message_id': message_id,
                    'sender_username': fields[1],
                    'recipient_username': fields[2],
                    'subject': fields[3],
                    'content': fields[4],
                    'timestamp': fields[5],
                    'is_read': is_read
                })
            except ValueError:
                continue
    return messages

def add_message(message_data):
    messages = load_messages()
    max_id = max([m['message_id'] for m in messages], default=0)
    new_id = max_id + 1
    new_message = {
        'message_id': new_id,
        'sender_username': message_data['sender_username'],
        'recipient_username': message_data['recipient_username'],
        'subject': message_data['subject'],
        'content': message_data['content'],
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'is_read': False
    }
    messages.append(new_message)
    lines = []
    for m in messages:
        line = '|'.join([
            str(m['message_id']),
            m['sender_username'],
            m['recipient_username'],
            m['subject'],
            m['content'],
            m['timestamp'],
            'true' if m['is_read'] else 'false'
        ])
        lines.append(line)
    success = _write_file_lines('messages.txt', lines)
    return success

# ---- Shelters ---- #
def load_shelters():
    shelters = []
    lines = _read_file_lines('shelters.txt')
    for line in lines:
        fields = line.strip().split('|')
        if len(fields) == 5:
            try:
                shelter_id = int(fields[0])
                shelters.append({
                    'shelter_id': shelter_id,
                    'name': fields[1],
                    'address': fields[2],
                    'phone': fields[3],
                    'email': fields[4]
                })
            except ValueError:
                continue
    return shelters


# -------- Flask Routes Implementation -------- #

# Route: / (root_redirect) GET
@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard_page'))

# Route: /dashboard (dashboard_page) GET
@app.route('/dashboard')
def dashboard_page():
    pets = load_pets()
    # featured_pets: select first 5 available pets sorted by date_added desc
    available_pets = [p for p in pets if p['status'] == 'Available']

    # Sort by date_added descending
    available_pets_sorted = sorted(available_pets, key=lambda p: p['date_added'], reverse=True)
    featured_pets = []
    for p in available_pets_sorted[:5]:
        featured_pets.append({
            'pet_id': p['pet_id'],
            'name': p['name'],
            'species': p['species'],
            'age': p['age'],
            'photo_url': ''  # No photo_url field in pets.txt - here we just set empty string
        })

    # recent_activities can be recent application statuses or messages or adoptions, for simplicity, recent applications
    applications = load_applications()
    recent_activities = []
    # Sort applications by date_submitted descending
    applications_sorted = sorted(applications, key=lambda a: a['date_submitted'], reverse=True)
    for app in applications_sorted[:5]:
        recent_activities.append(f"Application for {app['applicant_name']} - Status: {app['status']}")

    return render_template('dashboard.html', featured_pets=featured_pets, recent_activities=recent_activities)

# Route: /pets (pet_listings_page) GET
@app.route('/pets')
def pet_listings_page():
    filter_species = request.args.get('species', 'All')
    pets = load_pets()
    filtered_pets = []
    for pet in pets:
        if filter_species == 'All' or pet['species'] == filter_species:
            filtered_pets.append({
                'pet_id': pet['pet_id'],
                'name': pet['name'],
                'species': pet['species'],
                'age': pet['age'],
                'photo_url': ''
            })
    return render_template('pet_listings.html', pets=filtered_pets, filter_species=filter_species)

# Route: /pets/search (pet_search) POST
@app.route('/pets/search', methods=['POST'])
def pet_search():
    species = request.form.get('species', 'All')
    # Redirect to /pets with species filter (species in query string)
    if species not in ['All', 'Dog', 'Cat', 'Bird', 'Rabbit', 'Other']:
        species = 'All'
    return redirect(url_for('pet_listings_page', species=species))

# Route: /pets/<int:pet_id> (pet_details_page) GET
@app.route('/pets/<int:pet_id>')
def pet_details_page(pet_id):
    pet = get_pet_by_id(pet_id)
    if pet is None:
        return "Pet not found", 404
    return render_template('pet_details.html', pet=pet)

# Route: /pets/add GET (add_pet_page)
@app.route('/pets/add', methods=['GET'])
def add_pet_page():
    return render_template('add_pet.html')

# Route: /pets/add POST (submit_new_pet)
@app.route('/pets/add', methods=['POST'])
def submit_new_pet():
    pet_name = request.form.get('pet_name', '').strip()
    pet_species = request.form.get('pet_species', '').strip()
    pet_breed = request.form.get('pet_breed', '').strip()
    pet_age = request.form.get('pet_age', '').strip()
    pet_gender = request.form.get('pet_gender', '').strip()
    pet_size = request.form.get('pet_size', '').strip()
    pet_description = request.form.get('pet_description', '').strip()

    errors = []
    if not pet_name:
        errors.append('Pet name is required.')
    if pet_species not in ['Dog', 'Cat', 'Bird', 'Rabbit', 'Other']:
        errors.append('Invalid species.')
    if not pet_breed:
        errors.append('Breed is required.')
    if not pet_age:
        errors.append('Age is required.')
    if pet_gender not in ['Male', 'Female']:
        errors.append('Invalid gender.')
    if pet_size not in ['Small', 'Medium', 'Large']:
        errors.append('Invalid size.')
    if not pet_description:
        errors.append('Description is required.')

    if errors:
        # Show errors on add_pet.html
        return render_template('add_pet.html', errors=errors,
                               form_data=request.form)

    new_pet_data = {
        'name': pet_name,
        'species': pet_species,
        'breed': pet_breed,
        'age': pet_age,
        'gender': pet_gender,
        'size': pet_size,
        'description': pet_description
    }
    success = add_new_pet(new_pet_data)
    if success:
        return redirect(url_for('pet_listings_page'))
    else:
        errors.append('Failed to add new pet.')
        return render_template('add_pet.html', errors=errors, form_data=request.form)

# Route: /adoption/apply/<int:pet_id> GET (adoption_application_page)
@app.route('/adoption/apply/<int:pet_id>', methods=['GET'])
def adoption_application_page(pet_id):
    pet = get_pet_by_id(pet_id)
    if pet is None:
        return "Pet not found", 404
    return render_template('adoption_application.html', pet_id=pet_id, pet_name=pet['name'])

# Route: /adoption/apply/<int:pet_id> POST (submit_adoption_application)
@app.route('/adoption/apply/<int:pet_id>', methods=['POST'])
def submit_adoption_application(pet_id):
    pet = get_pet_by_id(pet_id)
    if pet is None:
        return "Pet not found", 404

    applicant_name = request.form.get('applicant_name', '').strip()
    applicant_phone = request.form.get('applicant_phone', '').strip()
    housing_type = request.form.get('housing_type', '').strip()
    reason = request.form.get('reason', '').strip()

    errors = []
    if not applicant_name:
        errors.append('Applicant name is required.')
    if not applicant_phone:
        errors.append('Applicant phone is required.')
    if housing_type not in ['House', 'Apartment', 'Condo', 'Other']:
        errors.append('Invalid housing type.')
    if not reason:
        errors.append('Reason for adoption is required.')

    if errors:
        return render_template('adoption_application.html', errors=errors, pet_id=pet_id, pet_name=pet['name'],
                               form_data=request.form)

    # Get username from applicant_name - lookup by matching exact applicant_name to username in users
    users = load_users()
    username = ''
    for user in users:
        if user['username'].lower() == applicant_name.lower() or user['email'].lower() == applicant_name.lower():
            username = user['username']
            break
    # In the spec, no clear user session, so store empty username if not found

    # Try to get phone and address from users if matching username found
    phone = applicant_phone
    address = ''
    if username:
        u = get_user_by_username(username)
        if u:
            phone = u['phone']
            address = u['address']

    application_data = {
        'username': username,
        'pet_id': pet_id,
        'applicant_name': applicant_name,
        'phone': phone,
        'address': address,
        'housing_type': housing_type,
        'has_yard': 'No',  # No form field for this, default No
        'other_pets': '',
        'experience': '',
        'reason': reason
    }

    success = add_application(application_data)
    if success:
        return redirect(url_for('my_applications_page'))
    else:
        errors.append('Failed to submit application.')
        return render_template('adoption_application.html', errors=errors, pet_id=pet_id, pet_name=pet['name'],
                               form_data=request.form)

# Route: /my_applications GET (my_applications_page)
@app.route('/my_applications')
def my_applications_page():
    # User context unknown, so show all applications
    applications = load_applications()
    # For each application, fetch pet_name by pet_id
    pets = load_pets()
    pet_id_to_name = {p['pet_id']: p['name'] for p in pets}
    application_list = []
    for app in applications:
        application_list.append({
            'application_id': app['application_id'],
            'pet_name': pet_id_to_name.get(app['pet_id'], 'Unknown Pet'),
            'date_submitted': app['date_submitted'],
            'status': app['status']
        })
    return render_template('my_applications.html', applications=application_list)

# Route: /favorites GET (favorites_page)
@app.route('/favorites')
def favorites_page():
    # Without login, assume username hardcoded
    username = 'john_doe'
    favorites = load_favorites_by_username(username)
    pets = load_pets()
    pet_map = {p['pet_id']: p for p in pets}
    favorites_list = []
    for fav in favorites:
        pet = pet_map.get(fav['pet_id'])
        if pet:
            favorites_list.append({
                'pet_id': pet['pet_id'],
                'name': pet['name'],
                'species': pet['species'],
                'age': pet['age']
            })
    return render_template('favorites.html', favorites=favorites_list)

# Route: /messages GET (messages_page)
@app.route('/messages')
def messages_page():
    conversations = load_messages()
    return render_template('messages.html', conversations=conversations)

# Route: /messages/send POST (send_message)
@app.route('/messages/send', methods=['POST'])
def send_message():
    recipient_username = request.form.get('recipient_username', '').strip()
    subject = request.form.get('subject', '').strip()
    content = request.form.get('content', '').strip()
    
    errors = []
    if not recipient_username:
        errors.append('Recipient username is required.')
    if not subject:
        errors.append('Subject is required.')
    if not content:
        errors.append('Content is required.')

    if errors:
        conversations = load_messages()
        return render_template('messages.html', conversations=conversations, errors=errors,
                               form_data=request.form)

    # Without login, sender fixed
    sender_username = 'john_doe'

    message_data = {
        'sender_username': sender_username,
        'recipient_username': recipient_username,
        'subject': subject,
        'content': content
    }

    success = add_message(message_data)
    if success:
        return redirect(url_for('messages_page'))
    else:
        errors.append('Failed to send message.')
        conversations = load_messages()
        return render_template('messages.html', conversations=conversations, errors=errors,
                               form_data=request.form)

# Route: /profile GET (user_profile_page)
@app.route('/profile')
def user_profile_page():
    # Without authentication, fixed username
    username = 'john_doe'
    user = get_user_by_username(username)
    email = user['email'] if user else ''
    return render_template('profile.html', username=username, email=email)

# Route: /profile/update POST (update_profile)
@app.route('/profile/update', methods=['POST'])
def update_profile():
    # Fixed username
    username = 'john_doe'
    email = request.form.get('email', '').strip()
    if not email:
        user = get_user_by_username(username)
        return render_template('profile.html', username=username, email=user['email'] if user else '', errors=['Email is required.'])

    success = update_user_email(username, email)
    if success:
        return redirect(url_for('user_profile_page'))
    else:
        user = get_user_by_username(username)
        return render_template('profile.html', username=username, email=user['email'] if user else '', errors=['Failed to update email.'])

# Route: /admin GET (admin_panel_page)
@app.route('/admin')
def admin_panel_page():
    applications = load_applications()
    pets = load_pets()

    pending_apps = []
    for app in applications:
        if app['status'] == 'Pending':
            pet = get_pet_by_id(app['pet_id'])
            pending_apps.append({
                'application_id': app['application_id'],
                'pet_name': pet['name'] if pet else 'Unknown',
                'applicant_name': app['applicant_name'],
                'date_submitted': app['date_submitted'],
                'status': app['status']
            })

    all_pets_list = []
    for pet in pets:
        all_pets_list.append({
            'pet_id': pet['pet_id'],
            'name': pet['name'],
            'species': pet['species'],
            'status': pet['status']
        })

    return render_template('admin_panel.html', pending_applications=pending_apps, all_pets=all_pets_list)

# Route: /admin/applications/approve/<int:application_id> POST (approve_application)
@app.route('/admin/applications/approve/<int:application_id>', methods=['POST'])
def approve_application(application_id):
    app_obj = get_application_by_id(application_id)
    if not app_obj:
        return "Application not found", 404

    # Update application status to Approved
    updated = update_application_status(application_id, 'Approved')
    if not updated:
        return "Failed to update application status", 500

    # Also update pet status to Adopted
    pets = load_pets()
    pet_updated = False
    for pet in pets:
        if pet['pet_id'] == app_obj['pet_id']:
            pet['status'] = 'Adopted'
            pet_updated = True
            break

    if pet_updated:
        lines = []
        for pet in pets:
            line = '|'.join([
                str(pet['pet_id']),
                pet['name'],
                pet['species'],
                pet['breed'],
                pet['age'],
                pet['gender'],
                pet['size'],
                pet['description'],
                str(pet['shelter_id']),
                pet['status'],
                pet['date_added']
            ])
            lines.append(line)
        _write_file_lines('pets.txt', lines)

    return redirect(url_for('admin_panel_page'))

# Route: /admin/applications/reject/<int:application_id> POST (reject_application)
@app.route('/admin/applications/reject/<int:application_id>', methods=['POST'])
def reject_application(application_id):
    app_obj = get_application_by_id(application_id)
    if not app_obj:
        return "Application not found", 404

    # Update application status to Rejected
    updated = update_application_status(application_id, 'Rejected')
    if not updated:
        return "Failed to update application status", 500

    return redirect(url_for('admin_panel_page'))


if __name__ == '__main__':
    app.run(debug=True)
