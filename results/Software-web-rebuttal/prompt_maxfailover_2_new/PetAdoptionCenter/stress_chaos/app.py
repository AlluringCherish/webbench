from flask import Flask, render_template, redirect, url_for, request
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')

# Helper functions for reading and writing data

def read_users():
    users = []
    filepath = os.path.join(DATA_DIR, 'users.txt')
    if not os.path.exists(filepath):
        return users
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) != 4:
                continue
            user = {
                'username': parts[0],
                'email': parts[1],
                'phone': parts[2],
                'address': parts[3],
            }
            users.append(user)
    return users


def write_users(users):
    filepath = os.path.join(DATA_DIR, 'users.txt')
    with open(filepath, 'w', encoding='utf-8') as f:
        for user in users:
            line = '|'.join([
                user['username'],
                user['email'],
                user['phone'],
                user['address']
            ])
            f.write(line + '\n')


def read_pets():
    pets = []
    filepath = os.path.join(DATA_DIR, 'pets.txt')
    if not os.path.exists(filepath):
        return pets
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) != 11:
                continue
            try:
                pet = {
                    'pet_id': int(parts[0]),
                    'name': parts[1],
                    'species': parts[2],
                    'breed': parts[3],
                    'age': parts[4],
                    'gender': parts[5],
                    'size': parts[6],
                    'description': parts[7],
                    'shelter_id': int(parts[8]),
                    'status': parts[9],
                    'date_added': parts[10]
                }
                pets.append(pet)
            except:
                continue
    return pets


def write_pets(pets):
    filepath = os.path.join(DATA_DIR, 'pets.txt')
    with open(filepath, 'w', encoding='utf-8') as f:
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
            f.write(line + '\n')


def read_applications():
    applications = []
    filepath = os.path.join(DATA_DIR, 'applications.txt')
    if not os.path.exists(filepath):
        return applications
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) != 13:
                continue
            try:
                application = {
                    'application_id': int(parts[0]),
                    'username': parts[1],
                    'pet_id': int(parts[2]),
                    'applicant_name': parts[3],
                    'phone': parts[4],
                    'address': parts[5],
                    'housing_type': parts[6],
                    'has_yard': parts[7],
                    'other_pets': parts[8],
                    'experience': parts[9],
                    'reason': parts[10],
                    'status': parts[11],
                    'date_submitted': parts[12],
                }
                applications.append(application)
            except:
                continue
    return applications


def write_applications(applications):
    filepath = os.path.join(DATA_DIR, 'applications.txt')
    with open(filepath, 'w', encoding='utf-8') as f:
        for app in applications:
            line = '|'.join([
                str(app['application_id']),
                app['username'],
                str(app['pet_id']),
                app['applicant_name'],
                app['phone'],
                app['address'],
                app['housing_type'],
                app['has_yard'],
                app['other_pets'],
                app['experience'],
                app['reason'],
                app['status'],
                app['date_submitted']
            ])
            f.write(line + '\n')


def read_favorites():
    favorites = []
    filepath = os.path.join(DATA_DIR, 'favorites.txt')
    if not os.path.exists(filepath):
        return favorites
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) != 3:
                continue
            try:
                favorite = {
                    'username': parts[0],
                    'pet_id': int(parts[1]),
                    'date_added': parts[2],
                }
                favorites.append(favorite)
            except:
                continue
    return favorites


def write_favorites(favorites):
    filepath = os.path.join(DATA_DIR, 'favorites.txt')
    with open(filepath, 'w', encoding='utf-8') as f:
        for fav in favorites:
            line = '|'.join([
                fav['username'],
                str(fav['pet_id']),
                fav['date_added']
            ])
            f.write(line + '\n')


def read_messages():
    messages = []
    filepath = os.path.join(DATA_DIR, 'messages.txt')
    if not os.path.exists(filepath):
        return messages
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) != 7:
                continue
            try:
                message = {
                    'message_id': int(parts[0]),
                    'sender_username': parts[1],
                    'recipient_username': parts[2],
                    'subject': parts[3],
                    'content': parts[4],
                    'timestamp': parts[5],
                    'is_read': parts[6].lower() == 'true'
                }
                messages.append(message)
            except:
                continue
    return messages


def write_messages(messages):
    filepath = os.path.join(DATA_DIR, 'messages.txt')
    with open(filepath, 'w', encoding='utf-8') as f:
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
            f.write(line + '\n')


def read_adoption_history():
    history = []
    filepath = os.path.join(DATA_DIR, 'adoption_history.txt')
    if not os.path.exists(filepath):
        return history
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) != 6:
                continue
            try:
                rec = {
                    'history_id': int(parts[0]),
                    'username': parts[1],
                    'pet_id': int(parts[2]),
                    'pet_name': parts[3],
                    'adoption_date': parts[4],
                    'shelter_id': int(parts[5])
                }
                history.append(rec)
            except:
                continue
    return history


def write_adoption_history(history):
    filepath = os.path.join(DATA_DIR, 'adoption_history.txt')
    with open(filepath, 'w', encoding='utf-8') as f:
        for rec in history:
            line = '|'.join([
                str(rec['history_id']),
                rec['username'],
                str(rec['pet_id']),
                rec['pet_name'],
                rec['adoption_date'],
                str(rec['shelter_id'])
            ])
            f.write(line + '\n')


def read_shelters():
    shelters = []
    filepath = os.path.join(DATA_DIR, 'shelters.txt')
    if not os.path.exists(filepath):
        return shelters
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) != 5:
                continue
            try:
                shelter = {
                    'shelter_id': int(parts[0]),
                    'name': parts[1],
                    'address': parts[2],
                    'phone': parts[3],
                    'email': parts[4]
                }
                shelters.append(shelter)
            except:
                continue
    return shelters

# For current user simulation
# Since no auth system defined, we use a fixed username.
CURRENT_USERNAME = 'john_doe'


@app.route('/', methods=['GET'])
def root_redirect():
    return redirect(url_for('dashboard'))


@app.route('/dashboard', methods=['GET'])
def dashboard():
    pets = read_pets()
    featured_pets = []
    # Select max 5 featured pets (Available and recent by date_added descending)
    available_pets = [p for p in pets if p['status'] == 'Available']
    # Sort by date_added descending
    available_pets.sort(key=lambda x: x['date_added'], reverse=True)
    for p in available_pets[:5]:
        featured_pets.append({
            'pet_id': p['pet_id'],
            'name': p['name'],
            'species': p['species'],
            'age': p['age'],
        })
    return render_template('dashboard.html', featured_pets=featured_pets)


@app.route('/pets', methods=['GET'])
def pet_listings():
    pets = read_pets()
    # Get filter parameters
    species_filter = request.args.get('species', 'All')
    search_query = request.args.get('search', '').strip()

    # Filter by species if not "All"
    filtered_pets = []
    for pet in pets:
        if pet['status'] != 'Available':
            continue
        if species_filter != 'All' and pet['species'] != species_filter:
            continue
        if search_query and search_query.lower() not in pet['name'].lower():
            continue
        filtered_pets.append({
            'pet_id': pet['pet_id'],
            'name': pet['name'],
            'species': pet['species'],
            'age': pet['age'],
        })

    return render_template('pet_listings.html', pets=filtered_pets, selected_species=species_filter, search_query=search_query)


@app.route('/pets/<int:pet_id>', methods=['GET'])
def pet_details(pet_id):
    pets = read_pets()
    pet = None
    for p in pets:
        if p['pet_id'] == pet_id:
            pet = p
            break
    if pet is None:
        # Pet not found; handle gracefully by rendering pet_details with None or redirect
        return render_template('pet_details.html', pet=None)

    return render_template('pet_details.html', pet=pet)


@app.route('/pets/add', methods=['GET'])
def add_pet_form():
    return render_template('add_pet.html')


@app.route('/pets/add', methods=['POST'])
def submit_new_pet():
    pets = read_pets()

    # Extract form data
    name = request.form.get('pet-name-input', '').strip()
    species = request.form.get('pet-species-input', '').strip()
    breed = request.form.get('pet-breed-input', '').strip()
    age = request.form.get('pet-age-input', '').strip()
    gender = request.form.get('pet-gender-input', '').strip()
    size = request.form.get('pet-size-input', '').strip()
    description = request.form.get('pet-description-input', '').strip()

    if not name or not species or not breed or not age or not gender or not size or not description:
        # Missing required fields; ideally flash a message, but specification does not include
        return redirect(url_for('add_pet_form'))

    # Generate new pet_id
    max_id = max([p['pet_id'] for p in pets], default=0)
    new_pet_id = max_id + 1

    # Assign shelter_id (unknown from form; use 1 as default here)
    shelter_id = 1
    # Set status as 'Available'
    status = 'Available'
    date_added = datetime.today().strftime('%Y-%m-%d')

    new_pet = {
        'pet_id': new_pet_id,
        'name': name,
        'species': species,
        'breed': breed,
        'age': age,
        'gender': gender,
        'size': size,
        'description': description,
        'shelter_id': shelter_id,
        'status': status,
        'date_added': date_added
    }

    pets.append(new_pet)
    write_pets(pets)

    return redirect(url_for('dashboard'))


@app.route('/applications/adopt/<int:pet_id>', methods=['GET'])
def adoption_application_form(pet_id):
    pets = read_pets()
    pet_name = None
    for p in pets:
        if p['pet_id'] == pet_id:
            pet_name = p['name']
            break
    if pet_name is None:
        # Pet not found
        pet_name = ''

    return render_template('adoption_application.html', pet_id=pet_id, pet_name=pet_name)


@app.route('/applications/adopt/<int:pet_id>', methods=['POST'])
def submit_adoption_application(pet_id):
    applications = read_applications()
    pets = read_pets()
    pet_name = ''
    for p in pets:
        if p['pet_id'] == pet_id:
            pet_name = p['name']
            break

    # Extract form fields
    applicant_name = request.form.get('applicant-name', '').strip()
    applicant_phone = request.form.get('applicant-phone', '').strip()
    housing_type = request.form.get('housing-type', '').strip()
    reason = request.form.get('reason', '').strip()

    if not applicant_name or not applicant_phone or not housing_type or not reason:
        # Required fields missing; redirect back to form
        return redirect(url_for('adoption_application_form', pet_id=pet_id))

    # We don't have address or other info in form spec; so fill minimal required fields
    # For missing fields use empty string
    address = ''
    has_yard = 'No'
    other_pets = ''
    experience = ''

    # Generate new application_id
    max_id = max([app['application_id'] for app in applications], default=0)
    new_id = max_id + 1
    date_submitted = datetime.today().strftime('%Y-%m-%d')

    # Username is CURRENT_USERNAME
    new_application = {
        'application_id': new_id,
        'username': CURRENT_USERNAME,
        'pet_id': pet_id,
        'applicant_name': applicant_name,
        'phone': applicant_phone,
        'address': address,
        'housing_type': housing_type,
        'has_yard': has_yard,
        'other_pets': other_pets,
        'experience': experience,
        'reason': reason,
        'status': 'Pending',
        'date_submitted': date_submitted
    }

    applications.append(new_application)
    write_applications(applications)

    return redirect(url_for('pet_details', pet_id=pet_id))


@app.route('/applications/my', methods=['GET'])
def my_applications():
    applications = read_applications()
    pets = read_pets()
    selected_status = request.args.get('status', 'All')

    filtered_apps = []
    # Filter to applications of CURRENT_USERNAME
    for app in applications:
        if app['username'] != CURRENT_USERNAME:
            continue
        if selected_status != 'All' and app['status'] != selected_status:
            continue
        pet_name = ''
        for p in pets:
            if p['pet_id'] == app['pet_id']:
                pet_name = p['name']
                break
        filtered_apps.append({
            'application_id': app['application_id'],
            'pet_name': pet_name,
            'date_submitted': app['date_submitted'],
            'status': app['status'],
        })

    return render_template('my_applications.html', applications=filtered_apps, selected_status=selected_status)


@app.route('/favorites', methods=['GET'])
def favorites():
    favorites = read_favorites()
    pets = read_pets()

    favorite_pets = []
    # Filter favorites of CURRENT_USERNAME
    pet_map = {p['pet_id']: p for p in pets}
    for fav in favorites:
        if fav['username'] != CURRENT_USERNAME:
            continue
        p = pet_map.get(fav['pet_id'])
        if p and p['status'] == 'Available':
            favorite_pets.append({
                'pet_id': p['pet_id'],
                'name': p['name'],
                'species': p['species'],
                'age': p['age']
            })

    return render_template('favorites.html', favorite_pets=favorite_pets)


@app.route('/messages', methods=['GET'])
def messages():
    messages = read_messages()

    # Show conversations - messages for or from CURRENT_USERNAME
    conversations = []
    for msg in messages:
        if msg['sender_username'] == CURRENT_USERNAME or msg['recipient_username'] == CURRENT_USERNAME:
            conversations.append(msg)

    return render_template('messages.html', conversations=conversations)


@app.route('/messages/send', methods=['POST'])
def send_message():
    messages = read_messages()

    # Extract from form
    recipient_username = request.form.get('recipient-username', '').strip()
    subject = request.form.get('subject', '').strip()
    content = request.form.get('content', '').strip()

    if not recipient_username or not subject or not content:
        # Missing fields redirect back
        return redirect(url_for('messages'))

    # Generate new message_id
    max_id = max([m['message_id'] for m in messages], default=0)
    new_id = max_id + 1
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    new_message = {
        'message_id': new_id,
        'sender_username': CURRENT_USERNAME,
        'recipient_username': recipient_username,
        'subject': subject,
        'content': content,
        'timestamp': timestamp,
        'is_read': False
    }

    messages.append(new_message)
    write_messages(messages)

    return redirect(url_for('messages'))


@app.route('/profile', methods=['GET'])
def profile():
    users = read_users()
    username = CURRENT_USERNAME
    email = ''
    for u in users:
        if u['username'] == username:
            email = u['email']
            break

    return render_template('profile.html', username=username, email=email)


@app.route('/profile/update', methods=['POST'])
def update_profile():
    users = read_users()
    username = CURRENT_USERNAME
    new_email = request.form.get('email', '').strip()

    updated = False
    for u in users:
        if u['username'] == username:
            if new_email:
                u['email'] = new_email
                updated = True
            break

    if updated:
        write_users(users)

    return redirect(url_for('profile'))


@app.route('/admin', methods=['GET'])
def admin_panel():
    applications = read_applications()
    pets = read_pets()

    pending_applications = []
    for app in applications:
        if app['status'] == 'Pending':
            pet_name = ''
            for p in pets:
                if p['pet_id'] == app['pet_id']:
                    pet_name = p['name']
                    break
            pending_applications.append({
                'application_id': app['application_id'],
                'applicant_name': app['applicant_name'],
                'pet_name': pet_name,
                'date_submitted': app['date_submitted']
            })

    all_pets = []
    for p in pets:
        all_pets.append({
            'pet_id': p['pet_id'],
            'name': p['name'],
            'status': p['status']
        })

    return render_template('admin_panel.html', pending_applications=pending_applications, all_pets=all_pets)


if __name__ == '__main__':
    app.run(debug=True)
