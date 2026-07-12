from flask import Flask, render_template, redirect, url_for, request
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Utility functions to load and save data

def read_users():
    users = []
    try:
        with open(os.path.join(DATA_DIR, 'users.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 4:
                    continue
                username, email, phone, address = parts
                users.append({
                    'username': username,
                    'email': email,
                    'phone': phone,
                    'address': address
                })
    except FileNotFoundError:
        pass
    return users


def read_pets():
    pets = []
    try:
        with open(os.path.join(DATA_DIR, 'pets.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 11:
                    continue
                pet_id, name, species, breed, age, gender, size, description, shelter_id, status, date_added = parts
                pets.append({
                    'pet_id': int(pet_id),
                    'name': name,
                    'species': species,
                    'breed': breed,
                    'age': age,
                    'gender': gender,
                    'size': size,
                    'description': description,
                    'shelter_id': int(shelter_id),
                    'status': status,
                    'date_added': date_added
                })
    except FileNotFoundError:
        pass
    return pets


def write_pets(pets):
    try:
        with open(os.path.join(DATA_DIR, 'pets.txt'), 'w', encoding='utf-8') as f:
            for pet in pets:
                line = f"{pet['pet_id']}|{pet['name']}|{pet['species']}|{pet['breed']}|{pet['age']}|{pet['gender']}|{pet['size']}|{pet['description']}|{pet['shelter_id']}|{pet['status']}|{pet['date_added']}"
                f.write(line + '\n')
    except Exception as e:
        pass


def read_applications():
    applications = []
    try:
        with open(os.path.join(DATA_DIR, 'applications.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 13:
                    continue
                application_id, username, pet_id, applicant_name, phone, address, housing_type, has_yard, other_pets, experience, reason, status, date_submitted = parts
                applications.append({
                    'application_id': int(application_id),
                    'username': username,
                    'pet_id': int(pet_id),
                    'applicant_name': applicant_name,
                    'phone': phone,
                    'address': address,
                    'housing_type': housing_type,
                    'has_yard': has_yard,
                    'other_pets': other_pets,
                    'experience': experience,
                    'reason': reason,
                    'status': status,
                    'date_submitted': date_submitted
                })
    except FileNotFoundError:
        pass
    return applications


def write_applications(applications):
    try:
        with open(os.path.join(DATA_DIR, 'applications.txt'), 'w', encoding='utf-8') as f:
            for app in applications:
                line = f"{app['application_id']}|{app['username']}|{app['pet_id']}|{app['applicant_name']}|{app['phone']}|{app['address']}|{app['housing_type']}|{app['has_yard']}|{app['other_pets']}|{app['experience']}|{app['reason']}|{app['status']}|{app['date_submitted']}"
                f.write(line + '\n')
    except Exception as e:
        pass


def read_favorites():
    favorites = []
    try:
        with open(os.path.join(DATA_DIR, 'favorites.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 3:
                    continue
                username, pet_id, date_added = parts
                favorites.append({
                    'username': username,
                    'pet_id': int(pet_id),
                    'date_added': date_added
                })
    except FileNotFoundError:
        pass
    return favorites


def read_messages():
    messages = []
    try:
        with open(os.path.join(DATA_DIR, 'messages.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 7:
                    continue
                message_id, sender_username, recipient_username, subject, content, timestamp, is_read = parts
                messages.append({
                    'message_id': int(message_id),
                    'sender_username': sender_username,
                    'recipient_username': recipient_username,
                    'subject': subject,
                    'content': content,
                    'timestamp': timestamp,
                    'is_read': is_read == 'true'
                })
    except FileNotFoundError:
        pass
    return messages


def write_messages(messages):
    try:
        with open(os.path.join(DATA_DIR, 'messages.txt'), 'w', encoding='utf-8') as f:
            for msg in messages:
                is_read_str = 'true' if msg['is_read'] else 'false'
                line = f"{msg['message_id']}|{msg['sender_username']}|{msg['recipient_username']}|{msg['subject']}|{msg['content']}|{msg['timestamp']}|{is_read_str}"
                f.write(line + '\n')
    except Exception as e:
        pass


def read_adoption_history():
    history = []
    try:
        with open(os.path.join(DATA_DIR, 'adoption_history.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 6:
                    continue
                history_id, username, pet_id, pet_name, adoption_date, shelter_id = parts
                history.append({
                    'history_id': int(history_id),
                    'username': username,
                    'pet_id': int(pet_id),
                    'pet_name': pet_name,
                    'adoption_date': adoption_date,
                    'shelter_id': int(shelter_id)
                })
    except FileNotFoundError:
        pass
    return history


def read_shelters():
    shelters = []
    try:
        with open(os.path.join(DATA_DIR, 'shelters.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 5:
                    continue
                shelter_id, name, address, phone, email = parts
                shelters.append({
                    'shelter_id': int(shelter_id),
                    'name': name,
                    'address': address,
                    'phone': phone,
                    'email': email
                })
    except FileNotFoundError:
        pass
    return shelters


def generate_new_pet_id(pets):
    if not pets:
        return 1
    return max(p['pet_id'] for p in pets) + 1


def generate_new_application_id(applications):
    if not applications:
        return 1
    return max(a['application_id'] for a in applications) + 1


def generate_new_message_id(messages):
    if not messages:
        return 1
    return max(m['message_id'] for m in messages) + 1


def generate_new_history_id(histories):
    if not histories:
        return 1
    return max(h['history_id'] for h in histories) + 1


# For the purpose of this implementation, we assume a single logged-in user 'john_doe'
LOGGED_IN_USERNAME = 'john_doe'


def root_redirect():
    return redirect(url_for('dashboard'))


@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    pets = read_pets()
    # Show featured pets (let's pick first 5 available pets for demo)
    featured_pets = []
    for pet in pets:
        if pet['status'] == 'Available':
            featured_pets.append({
                'pet_id': pet['pet_id'],
                'name': pet['name'],
                'species': pet['species'],
                'age': pet['age'],
                'photo_url': None  # No photo info given in data schema
            })
            if len(featured_pets) >= 5:
                break

    recent_activities = []  # Optional enhancement: empty list

    return render_template('dashboard.html', featured_pets=featured_pets, recent_activities=recent_activities)


@app.route('/pets')
def pet_listings():
    pets = read_pets()
    filter_species = request.args.get('filter_species', 'All')
    search_query = request.args.get('search_query', '').lower()

    filtered_pets = []
    for pet in pets:
        if filter_species != 'All' and pet['species'] != filter_species:
            continue
        if search_query and search_query not in pet['name'].lower():
            continue
        filtered_pets.append({
            'pet_id': pet['pet_id'],
            'name': pet['name'],
            'species': pet['species'],
            'age': pet['age'],
            'photo_url': None  # No photo info in data
        })

    return render_template('pet_listings.html', pets=filtered_pets, filter_species=filter_species, search_query=search_query)


@app.route('/pets/<int:pet_id>')
def pet_details(pet_id):
    pets = read_pets()
    pet = None
    for p in pets:
        if p['pet_id'] == pet_id:
            pet = p
            break
    if not pet:
        return "Pet not found", 404

    return render_template('pet_details.html', pet=pet)


@app.route('/pets/add', methods=['GET', 'POST'])
def add_pet():
    if request.method == 'POST':
        pet_name = request.form.get('pet_name', '').strip()
        pet_species = request.form.get('pet_species', '').strip()
        pet_breed = request.form.get('pet_breed', '').strip()
        pet_age = request.form.get('pet_age', '').strip()
        pet_gender = request.form.get('pet_gender', '').strip()
        pet_size = request.form.get('pet_size', '').strip()
        pet_description = request.form.get('pet_description', '').strip()

        if not pet_name or not pet_species or not pet_breed or not pet_age or not pet_gender or not pet_size:
            # could add flash messages for errors, but spec does not require
            return render_template('add_pet.html')

        pets = read_pets()
        new_id = generate_new_pet_id(pets)

        # For shelter_id, assign 1 by default as no form input provided
        shelter_id = 1
        status = 'Available'
        date_added = datetime.now().strftime('%Y-%m-%d')

        new_pet = {
            'pet_id': new_id,
            'name': pet_name,
            'species': pet_species,
            'breed': pet_breed,
            'age': pet_age,
            'gender': pet_gender,
            'size': pet_size,
            'description': pet_description,
            'shelter_id': shelter_id,
            'status': status,
            'date_added': date_added
        }

        pets.append(new_pet)
        write_pets(pets)

        return redirect(url_for('dashboard'))

    # GET request
    return render_template('add_pet.html')


@app.route('/application/<int:pet_id>', methods=['GET', 'POST'])
def adoption_application(pet_id):
    pets = read_pets()
    pet = None
    for p in pets:
        if p['pet_id'] == pet_id:
            pet = p
            break
    if not pet:
        return "Pet not found", 404

    if request.method == 'POST':
        applicant_name = request.form.get('applicant_name', '').strip()
        applicant_phone = request.form.get('applicant_phone', '').strip()
        housing_type = request.form.get('housing_type', '').strip()
        reason = request.form.get('reason', '').strip()

        if not applicant_name or not applicant_phone or not housing_type or not reason:
            # Could add flash messaging for errors, but not required
            return render_template('adoption_application.html', pet=pet)

        users = read_users()
        user = None
        for u in users:
            if u['username'] == LOGGED_IN_USERNAME:
                user = u
                break
        if not user:
            return "User not found", 404

        applications = read_applications()
        new_id = generate_new_application_id(applications)

        # Form fields required by schema but not collected in form - set defaults or empty
        has_yard = 'No'  # no form input
        other_pets = ''  # no form input
        experience = ''  # no form input

        new_app = {
            'application_id': new_id,
            'username': LOGGED_IN_USERNAME,
            'pet_id': pet['pet_id'],
            'applicant_name': applicant_name,
            'phone': applicant_phone,
            'address': user['address'],
            'housing_type': housing_type,
            'has_yard': has_yard,
            'other_pets': other_pets,
            'experience': experience,
            'reason': reason,
            'status': 'Pending',
            'date_submitted': datetime.now().strftime('%Y-%m-%d')
        }

        applications.append(new_app)
        write_applications(applications)

        return redirect(url_for('my_applications'))

    # GET request
    return render_template('adoption_application.html', pet=pet)


@app.route('/my_applications')
def my_applications():
    applications = read_applications()
    pets = read_pets()
    filter_status = request.args.get('filter_status', 'All')
    filtered_apps = []

    for app in applications:
        if app['username'] != LOGGED_IN_USERNAME:
            continue
        if filter_status != 'All' and app['status'] != filter_status:
            continue
        pet_name = next((p['name'] for p in pets if p['pet_id'] == app['pet_id']), 'Unknown')
        filtered_apps.append({
            'application_id': app['application_id'],
            'pet_name': pet_name,
            'date': app['date_submitted'],
            'status': app['status']
        })

    return render_template('my_applications.html', applications=filtered_apps, filter_status=filter_status)


@app.route('/favorites')
def favorites():
    favorites_data = read_favorites()
    pets = read_pets()

    favorite_pets = []
    for fav in favorites_data:
        if fav['username'] == LOGGED_IN_USERNAME:
            pet = next((p for p in pets if p['pet_id'] == fav['pet_id']), None)
            if pet:
                favorite_pets.append({
                    'pet_id': pet['pet_id'],
                    'name': pet['name'],
                    'species': pet['species'],
                    'age': pet['age'],
                    'photo_url': None
                })

    return render_template('favorites.html', favorite_pets=favorite_pets)


@app.route('/messages', methods=['GET', 'POST'])
def messages():
    messages_data = read_messages()

    if request.method == 'POST':
        recipient_username = request.form.get('recipient_username', '').strip()
        subject = request.form.get('subject', '').strip()
        content = request.form.get('content', '').strip()

        if recipient_username and subject and content:
            new_id = generate_new_message_id(messages_data)
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            new_message = {
                'message_id': new_id,
                'sender_username': LOGGED_IN_USERNAME,
                'recipient_username': recipient_username,
                'subject': subject,
                'content': content,
                'timestamp': timestamp,
                'is_read': False
            }
            messages_data.append(new_message)
            write_messages(messages_data)

        # Refresh page after sending
        return redirect(url_for('messages'))

    # GET request
    # Group messages by recipient_username and find last message, timestamp, and count unread from them
    conversations = {}
    for msg in messages_data:
        if msg['sender_username'] == LOGGED_IN_USERNAME:
            key = msg['recipient_username']
        elif msg['recipient_username'] == LOGGED_IN_USERNAME:
            key = msg['sender_username']
        else:
            continue

        if key not in conversations:
            conversations[key] = {
                'last_message': msg['content'],
                'last_timestamp': msg['timestamp'],
                'unread_count': 0
            }
        else:
            # Update if this message is newer
            if msg['timestamp'] > conversations[key]['last_timestamp']:
                conversations[key]['last_message'] = msg['content']
                conversations[key]['last_timestamp'] = msg['timestamp']

        # Count unread messages where logged user is recipient
        if msg['recipient_username'] == LOGGED_IN_USERNAME and not msg['is_read']:
            conversations[key]['unread_count'] += 1

    conversation_list = []
    for recipient_username, details in conversations.items():
        conversation_list.append({
            'recipient_username': recipient_username,
            'last_message': details['last_message'],
            'last_timestamp': details['last_timestamp'],
            'unread_count': details['unread_count']
        })

    # Sort conversations by last_timestamp descending
    conversation_list.sort(key=lambda x: x['last_timestamp'], reverse=True)

    return render_template('messages.html', conversations=conversation_list)


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    users = read_users()
    user = next((u for u in users if u['username'] == LOGGED_IN_USERNAME), None)
    if not user:
        return "User not found", 404

    if request.method == 'POST':
        new_email = request.form.get('email', '').strip()
        if new_email:
            user['email'] = new_email
            # Save back all users
            write_users(users)
        return redirect(url_for('profile'))

    return render_template('profile.html', username=user['username'], email=user['email'])


def write_users(users):
    try:
        with open(os.path.join(DATA_DIR, 'users.txt'), 'w', encoding='utf-8') as f:
            for u in users:
                line = f"{u['username']}|{u['email']}|{u['phone']}|{u['address']}"
                f.write(line + '\n')
    except Exception as e:
        pass


@app.route('/admin')
def admin_panel():
    applications = read_applications()
    pets = read_pets()

    pending_applications = []
    for app in applications:
        if app['status'] == 'Pending':
            pet_name = next((p['name'] for p in pets if p['pet_id'] == app['pet_id']), 'Unknown')
            pending_applications.append({
                'application_id': app['application_id'],
                'applicant_name': app['applicant_name'],
                'pet_name': pet_name,
                'date_submitted': app['date_submitted']
            })

    all_pets = []
    for pet in pets:
        all_pets.append({
            'pet_id': pet['pet_id'],
            'name': pet['name'],
            'species': pet['species'],
            'status': pet['status']
        })

    return render_template('admin_panel.html', pending_applications=pending_applications, all_pets=all_pets)


@app.route('/admin/pets/<int:pet_id>/edit', methods=['GET', 'POST'])
def edit_pet(pet_id):
    pets = read_pets()
    pet = next((p for p in pets if p['pet_id'] == pet_id), None)
    if not pet:
        return "Pet not found", 404

    if request.method == 'POST':
        pet_name = request.form.get('pet_name', '').strip()
        pet_species = request.form.get('pet_species', '').strip()
        pet_breed = request.form.get('pet_breed', '').strip()
        pet_age = request.form.get('pet_age', '').strip()
        pet_gender = request.form.get('pet_gender', '').strip()
        pet_size = request.form.get('pet_size', '').strip()
        pet_description = request.form.get('pet_description', '').strip()
        pet_status = request.form.get('pet_status', '').strip()

        if not pet_name or not pet_species or not pet_breed or not pet_age or not pet_gender or not pet_size or not pet_status:
            return render_template('edit_pet.html', pet=pet)

        pet['name'] = pet_name
        pet['species'] = pet_species
        pet['breed'] = pet_breed
        pet['age'] = pet_age
        pet['gender'] = pet_gender
        pet['size'] = pet_size
        pet['description'] = pet_description
        pet['status'] = pet_status

        write_pets(pets)
        return redirect(url_for('admin_panel'))

    return render_template('edit_pet.html', pet=pet)


@app.route('/admin/pets/<int:pet_id>/delete', methods=['POST'])
def delete_pet(pet_id):
    pets = read_pets()
    pets = [p for p in pets if p['pet_id'] != pet_id]
    write_pets(pets)
    return redirect(url_for('admin_panel'))


if __name__ == '__main__':
    app.run(debug=True)
