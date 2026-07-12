from flask import Flask, render_template, redirect, url_for, request
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Helper functions to load and save data files

def load_users():
    users = []
    path = os.path.join(DATA_DIR, 'users.txt')
    if not os.path.exists(path):
        return users
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) != 7:
                continue
            user = {
                'username': parts[0],
                'email': parts[1],
                'phone': parts[2],
                'address': parts[3],
                'housing_type': parts[4],
                'has_pets': parts[5],
                'pets_description': parts[6]
            }
            users.append(user)
    return users

def save_users(users):
    path = os.path.join(DATA_DIR, 'users.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for u in users:
            line = '|'.join([
                u['username'], u['email'], u['phone'], u['address'],
                u['housing_type'], u['has_pets'], u['pets_description']
            ])
            f.write(line + '\n')

def load_pets():
    pets = []
    path = os.path.join(DATA_DIR, 'pets.txt')
    if not os.path.exists(path):
        return pets
    with open(path, 'r', encoding='utf-8') as f:
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
            except ValueError:
                continue
            pets.append(pet)
    return pets

def save_pets(pets):
    path = os.path.join(DATA_DIR, 'pets.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for p in pets:
            line = '|'.join([
                str(p['pet_id']), p['name'], p['species'], p['breed'], p['age'], p['gender'],
                p['size'], p['description'], str(p['shelter_id']), p['status'], p['date_added']
            ])
            f.write(line + '\n')

def load_applications():
    applications = []
    path = os.path.join(DATA_DIR, 'applications.txt')
    if not os.path.exists(path):
        return applications
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) != 6:
                continue
            try:
                application = {
                    'application_id': int(parts[0]),
                    'username': parts[1],
                    'pet_id': int(parts[2]),
                    'pet_name': parts[3],
                    'status': parts[4],
                    'application_date': parts[5]
                }
            except ValueError:
                continue
            applications.append(application)
    return applications

def save_applications(applications):
    path = os.path.join(DATA_DIR, 'applications.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for a in applications:
            line = '|'.join([
                str(a['application_id']), a['username'], str(a['pet_id']), a['pet_name'],
                a['status'], a['application_date']
            ])
            f.write(line + '\n')

def load_favorites():
    favorites = []
    path = os.path.join(DATA_DIR, 'favorites.txt')
    if not os.path.exists(path):
        return favorites
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) != 3:
                continue
            try:
                favorite = {
                    'username': parts[0],
                    'pet_id': int(parts[1]),
                    'date_added': parts[2]
                }
            except ValueError:
                continue
            favorites.append(favorite)
    return favorites

def save_favorites(favorites):
    path = os.path.join(DATA_DIR, 'favorites.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for fav in favorites:
            line = '|'.join([
                fav['username'], str(fav['pet_id']), fav['date_added']
            ])
            f.write(line + '\n')

def load_messages():
    messages = []
    path = os.path.join(DATA_DIR, 'messages.txt')
    if not os.path.exists(path):
        return messages
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) != 5:
                continue
            try:
                message = {
                    'message_id': int(parts[0]),
                    'sender': parts[1],
                    'receiver': parts[2],
                    'message': parts[3],
                    'date_sent': parts[4]
                }
            except ValueError:
                continue
            messages.append(message)
    return messages

def save_messages(messages):
    path = os.path.join(DATA_DIR, 'messages.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for m in messages:
            line = '|'.join([
                str(m['message_id']), m['sender'], m['receiver'], m['message'], m['date_sent']
            ])
            f.write(line + '\n')

def load_history():
    history = []
    path = os.path.join(DATA_DIR, 'history.txt')
    if not os.path.exists(path):
        return history
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) != 6:
                continue
            try:
                h = {
                    'history_id': int(parts[0]),
                    'username': parts[1],
                    'pet_id': int(parts[2]),
                    'pet_name': parts[3],
                    'adoption_date': parts[4],
                    'shelter_id': int(parts[5])
                }
            except ValueError:
                continue
            history.append(h)
    return history

def save_history(history):
    path = os.path.join(DATA_DIR, 'history.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for h in history:
            line = '|'.join([
                str(h['history_id']), h['username'], str(h['pet_id']), h['pet_name'],
                h['adoption_date'], str(h['shelter_id'])
            ])
            f.write(line + '\n')

def load_shelters():
    shelters = []
    path = os.path.join(DATA_DIR, 'shelters.txt')
    if not os.path.exists(path):
        return shelters
    with open(path, 'r', encoding='utf-8') as f:
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
            except ValueError:
                continue
            shelters.append(shelter)
    return shelters


# Since user identification/authentication is not specified in design, assume a default current user for demo purpose
# In real app, authentication mechanism would supply current username
CURRENT_USERNAME = 'john_doe'


@app.route('/')
def dashboard_page():
    # Show featured pets, activities and navigation
    pets = load_pets()
    # Definition of featured pets not specified, assume status == 'Available' and most recently added (limit 5)
    featured_pets = [p for p in pets if p['status'].lower() == 'available']
    featured_pets = sorted(featured_pets, key=lambda x: x['date_added'], reverse=True)[:5]
    return render_template('dashboard.html', featured_pets=featured_pets)


@app.route('/listings')
def listings_page():
    # Display all available pets, with filtering by species if provided as query parameter
    pets = load_pets()
    species_filter = request.args.get('species')
    filtered_pets = pets
    if species_filter and species_filter.strip():
        filtered_pets = [p for p in pets if p['species'].lower() == species_filter.lower() and p['status'].lower() == 'available']
    else:
        filtered_pets = [p for p in pets if p['status'].lower() == 'available']
    return render_template('listings.html', pets=filtered_pets, selected_species=species_filter if species_filter else '')


@app.route('/pet/<int:pet_id>')
def pet_details(pet_id: int):
    pets = load_pets()
    pet = next((p for p in pets if p['pet_id'] == pet_id), None)
    if pet is None:
        # Pet not found, redirect to listings
        return redirect(url_for('listings_page'))
    return render_template('pet_details.html', pet=pet)


@app.route('/add-pet', methods=['GET'])
def add_pet_page():
    # Render add pet page
    return render_template('add_pet.html')


@app.route('/add-pet', methods=['POST'])
def submit_new_pet():
    pets = load_pets()
    data = request.form
    # Required fields: pet-name-input, species-select, age-input, breed-input, size-select, description-input
    pet_name = data.get('pet-name-input', '').strip()
    species = data.get('species-select', '').strip()
    age = data.get('age-input', '').strip()
    breed = data.get('breed-input', '').strip()
    size = data.get('size-select', '').strip()
    description = data.get('description-input', '').strip()

    if not all([pet_name, species, age, breed, size, description]):
        # Missing one or more required fields, return to add-pet page
        return render_template('add_pet.html', error='All fields are required.')

    # Generate new pet_id
    max_id = max([p['pet_id'] for p in pets], default=0)
    pet_id = max_id + 1

    # We don't have gender input in form, so default to Unknown
    gender = 'Unknown'

    # Assume shelter_id = 1 (default shelter)
    shelter_id = 1

    # Status is 'Available' for new pets
    status = 'Available'

    date_added = datetime.now().strftime('%Y-%m-%d')

    new_pet = {
        'pet_id': pet_id,
        'name': pet_name,
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
    save_pets(pets)

    return redirect(url_for('listings_page'))


@app.route('/adoption-application', methods=['GET'])
def adoption_application_page():
    # Load pet_id from query parameter to prefill if passed
    pet_id = request.args.get('pet_id', type=int)
    pets = load_pets()
    pet = None
    if pet_id:
        pet = next((p for p in pets if p['pet_id'] == pet_id), None)
    return render_template('adoption_application.html', pet=pet)


@app.route('/adoption-application', methods=['POST'])
def submit_adoption_application():
    data = request.form
    applicant_name = data.get('applicant-name', '').strip()
    applicant_phone = data.get('applicant-phone', '').strip()
    housing_type = data.get('housing-type', '').strip()
    reason = data.get('reason', '').strip()
    pet_id_str = data.get('pet_id', '').strip()

    if not all([applicant_name, applicant_phone, housing_type, reason, pet_id_str]):
        # missing fields
        return render_template('adoption_application.html', error='All fields are required.')

    try:
        pet_id = int(pet_id_str)
    except ValueError:
        return render_template('adoption_application.html', error='Invalid pet ID.')

    pets = load_pets()
    pet = next((p for p in pets if p['pet_id'] == pet_id), None)
    if pet is None:
        return render_template('adoption_application.html', error='Pet not found.')

    applications = load_applications()
    max_id = max([a['application_id'] for a in applications], default=0)
    application_id = max_id + 1

    application_date = datetime.now().strftime('%Y-%m-%d')

    # Use CURRENT_USERNAME as username
    username = CURRENT_USERNAME

    # Create new application with status Pending
    new_application = {
        'application_id': application_id,
        'username': username,
        'pet_id': pet_id,
        'pet_name': pet['name'],
        'status': 'Pending',
        'application_date': application_date
    }

    applications.append(new_application)
    save_applications(applications)

    return redirect(url_for('my_applications_page'))


@app.route('/my-applications')
def my_applications_page():
    # Show current user's adoption applications with optional filter by status
    applications = load_applications()
    user_apps = [a for a in applications if a['username'] == CURRENT_USERNAME]

    status_filter = request.args.get('status', '').strip()
    if status_filter and status_filter.lower() != 'all':
        user_apps = [a for a in user_apps if a['status'].lower() == status_filter.lower()]

    return render_template('my_applications.html', applications=user_apps, selected_status=status_filter)


@app.route('/favorites')
def favorites_page():
    favorites = load_favorites()
    pets = load_pets()
    user_favs = [f for f in favorites if f['username'] == CURRENT_USERNAME]

    # Build list of favorite pets details
    favorite_pets = []
    for fav in user_favs:
        pet = next((p for p in pets if p['pet_id'] == fav['pet_id']), None)
        if pet:
            favorite_pets.append(pet)

    return render_template('favorites.html', favorite_pets=favorite_pets)


@app.route('/messages')
def messages_page():
    messages = load_messages()
    # For simplicity, show all messages where current user is sender or receiver
    user_msgs = [m for m in messages if m['sender'] == CURRENT_USERNAME or m['receiver'] == CURRENT_USERNAME]
    return render_template('messages.html', messages=user_msgs)


@app.route('/send-message', methods=['POST'])
def send_message():
    data = request.form
    receiver = data.get('receiver', '').strip()
    message_text = data.get('message', '').strip()

    if not receiver or not message_text:
        return redirect(url_for('messages_page'))

    messages = load_messages()
    max_id = max([m['message_id'] for m in messages], default=0)
    message_id = max_id + 1

    date_sent = datetime.now().strftime('%Y-%m-%d')

    new_message = {
        'message_id': message_id,
        'sender': CURRENT_USERNAME,
        'receiver': receiver,
        'message': message_text,
        'date_sent': date_sent
    }

    messages.append(new_message)
    save_messages(messages)

    return redirect(url_for('messages_page'))


@app.route('/profile')
def profile_page():
    users = load_users()
    user = next((u for u in users if u['username'] == CURRENT_USERNAME), None)
    return render_template('profile.html', user=user)


@app.route('/profile', methods=['POST'])
def update_profile():
    data = request.form
    email = data.get('email', '').strip()
    phone = data.get('phone', '').strip()
    address = data.get('address', '').strip()
    housing_type = data.get('housing_type', '').strip()
    has_pets = data.get('has_pets', '').strip()
    pets_description = data.get('pets_description', '').strip()

    users = load_users()
    for u in users:
        if u['username'] == CURRENT_USERNAME:
            if email:
                u['email'] = email
            if phone:
                u['phone'] = phone
            if address:
                u['address'] = address
            if housing_type:
                u['housing_type'] = housing_type
            if has_pets:
                u['has_pets'] = has_pets
            if pets_description:
                u['pets_description'] = pets_description
            break
    else:
        # User not found, create new user entry with minimum info
        new_user = {
            'username': CURRENT_USERNAME,
            'email': email,
            'phone': phone,
            'address': address,
            'housing_type': housing_type,
            'has_pets': has_pets,
            'pets_description': pets_description
        }
        users.append(new_user)

    save_users(users)

    return redirect(url_for('profile_page'))


@app.route('/admin')
def admin_dashboard():
    # Show pending applications and all pets
    applications = load_applications()
    pending_apps = [a for a in applications if a['status'].lower() == 'pending']
    pets = load_pets()
    return render_template('admin_dashboard.html', pending_applications=pending_apps, all_pets=pets)


@app.route('/admin/approve/<int:application_id>', methods=['POST'])
def approve_application(application_id: int):
    applications = load_applications()
    pets = load_pets()
    updated = False

    # Approve application
    for app_entry in applications:
        if app_entry['application_id'] == application_id:
            app_entry['status'] = 'Approved'
            # Update pet status to Adopted
            for pet in pets:
                if pet['pet_id'] == app_entry['pet_id']:
                    pet['status'] = 'Adopted'
                    break
            updated = True
            break

    if updated:
        save_applications(applications)
        save_pets(pets)

    return redirect(url_for('admin_dashboard'))


@app.route('/admin/reject/<int:application_id>', methods=['POST'])
def reject_application(application_id: int):
    applications = load_applications()
    updated = False

    for app_entry in applications:
        if app_entry['application_id'] == application_id:
            app_entry['status'] = 'Rejected'
            updated = True
            break

    if updated:
        save_applications(applications)

    return redirect(url_for('admin_dashboard'))


if __name__ == '__main__':
    app.run(debug=True)
