from flask import Flask, render_template, redirect, url_for, request
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Utility functions to load and save data from/to files

def load_users():
    users = []
    filepath = os.path.join(DATA_DIR, 'users.txt')
    if not os.path.exists(filepath):
        return users
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                parts = line.strip().split('|')
                if len(parts) >= 4:
                    username, email, phone, address = parts
                    users.append({
                        'username': username,
                        'email': email,
                        'phone': phone,
                        'address': address
                    })
    return users


def load_pets():
    pets = []
    filepath = os.path.join(DATA_DIR, 'pets.txt')
    if not os.path.exists(filepath):
        return pets
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                parts = line.strip().split('|')
                if len(parts) >= 11:
                    pet_id = int(parts[0])
                    name = parts[1]
                    species = parts[2]
                    breed = parts[3]
                    age = parts[4]
                    gender = parts[5]
                    size = parts[6]
                    description = parts[7]
                    shelter_id = int(parts[8])
                    status = parts[9]
                    date_added = parts[10]
                    pets.append({
                        'pet_id': pet_id,
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
                    })
    return pets


def save_pets(pets):
    filepath = os.path.join(DATA_DIR, 'pets.txt')
    lines = []
    for pet in pets:
        line = f"{pet['pet_id']}|{pet['name']}|{pet['species']}|{pet['breed']}|{pet['age']}|{pet['gender']}|{pet['size']}|{pet['description']}|{pet['shelter_id']}|{pet['status']}|{pet['date_added']}"
        lines.append(line)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))


def load_applications():
    applications = []
    filepath = os.path.join(DATA_DIR, 'applications.txt')
    if not os.path.exists(filepath):
        return applications
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                parts = line.strip().split('|')
                if len(parts) >= 13:
                    application_id = int(parts[0])
                    username = parts[1]
                    pet_id = int(parts[2])
                    applicant_name = parts[3]
                    phone = parts[4]
                    address = parts[5]
                    housing_type = parts[6]
                    has_yard = parts[7]
                    other_pets = parts[8]
                    experience = parts[9]
                    reason = parts[10]
                    status = parts[11]
                    date_submitted = parts[12]
                    applications.append({
                        'application_id': application_id,
                        'username': username,
                        'pet_id': pet_id,
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
    return applications


def save_applications(applications):
    filepath = os.path.join(DATA_DIR, 'applications.txt')
    lines = []
    for app in applications:
        line = f"{app['application_id']}|{app['username']}|{app['pet_id']}|{app['applicant_name']}|{app['phone']}|{app['address']}|{app['housing_type']}|{app['has_yard']}|{app['other_pets']}|{app['experience']}|{app['reason']}|{app['status']}|{app['date_submitted']}"
        lines.append(line)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))


def load_favorites():
    favorites = []
    filepath = os.path.join(DATA_DIR, 'favorites.txt')
    if not os.path.exists(filepath):
        return favorites
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                parts = line.strip().split('|')
                if len(parts) >= 3:
                    username = parts[0]
                    pet_id = int(parts[1])
                    date_added = parts[2]
                    favorites.append({
                        'username': username,
                        'pet_id': pet_id,
                        'date_added': date_added
                    })
    return favorites


def save_favorites(favorites):
    filepath = os.path.join(DATA_DIR, 'favorites.txt')
    lines = []
    for fav in favorites:
        line = f"{fav['username']}|{fav['pet_id']}|{fav['date_added']}"
        lines.append(line)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))


def load_messages():
    messages = []
    filepath = os.path.join(DATA_DIR, 'messages.txt')
    if not os.path.exists(filepath):
        return messages
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                parts = line.strip().split('|')
                if len(parts) >= 7:
                    message_id = int(parts[0])
                    sender_username = parts[1]
                    recipient_username = parts[2]
                    subject = parts[3]
                    content = parts[4]
                    timestamp = parts[5]
                    is_read = parts[6]
                    messages.append({
                        'message_id': message_id,
                        'sender_username': sender_username,
                        'recipient_username': recipient_username,
                        'subject': subject,
                        'content': content,
                        'timestamp': timestamp,
                        'is_read': True if is_read.lower() == 'true' else False
                    })
    return messages


def save_messages(messages):
    filepath = os.path.join(DATA_DIR, 'messages.txt')
    lines = []
    for msg in messages:
        line = f"{msg['message_id']}|{msg['sender_username']}|{msg['recipient_username']}|{msg['subject']}|{msg['content']}|{msg['timestamp']}|{'true' if msg['is_read'] else 'false'}"
        lines.append(line)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))


def load_adoption_history():
    history = []
    filepath = os.path.join(DATA_DIR, 'adoption_history.txt')
    if not os.path.exists(filepath):
        return history
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                parts = line.strip().split('|')
                if len(parts) >= 6:
                    history_id = int(parts[0])
                    username = parts[1]
                    pet_id = int(parts[2])
                    pet_name = parts[3]
                    adoption_date = parts[4]
                    shelter_id = int(parts[5])
                    history.append({
                        'history_id': history_id,
                        'username': username,
                        'pet_id': pet_id,
                        'pet_name': pet_name,
                        'adoption_date': adoption_date,
                        'shelter_id': shelter_id
                    })
    return history


def load_shelters():
    shelters = []
    filepath = os.path.join(DATA_DIR, 'shelters.txt')
    if not os.path.exists(filepath):
        return shelters
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                parts = line.strip().split('|')
                if len(parts) >= 5:
                    shelter_id = int(parts[0])
                    name = parts[1]
                    address = parts[2]
                    phone = parts[3]
                    email = parts[4]
                    shelters.append({
                        'shelter_id': shelter_id,
                        'name': name,
                        'address': address,
                        'phone': phone,
                        'email': email
                    })
    return shelters

# Helper functions

def get_user(username):
    users = load_users()
    for user in users:
        if user['username'] == username:
            return user
    return None


def get_pet_by_id(pet_id):
    pets = load_pets()
    for pet in pets:
        if pet['pet_id'] == pet_id:
            return pet
    return None


def get_shelter_by_id(shelter_id):
    shelters = load_shelters()
    for shelter in shelters:
        if shelter['shelter_id'] == shelter_id:
            return shelter
    return None


# Route: /
@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard_page'))


# Route: /dashboard
@app.route('/dashboard')
def dashboard_page():
    pets = load_pets()
    # Let's consider featured_pets as the 3 newest pets with status 'Available'
    featured_pets_raw = sorted([p for p in pets if p['status'] == 'Available'],
                               key=lambda x: x['date_added'], reverse=True)[:3]
    featured_pets = []
    for pet in featured_pets_raw:
        featured_pets.append({
            'pet_id': pet['pet_id'],
            'name': pet['name'],
            'species': pet['species'],
            'age': pet['age'],
            'photo_url': f'/static/images/pets/{pet["pet_id"]}.jpg'  # assuming images by pet_id.jpg
        })

    # recent_activities: Show last 5 application statuses changes - summarize as strings
    applications = load_applications()
    applications_sorted = sorted(applications, key=lambda a: a['date_submitted'], reverse=True)[:5]
    recent_activities = []
    for app in applications_sorted:
        recent_activities.append(f"Application {app['application_id']} for {get_pet_by_id(app['pet_id'])['name']} is {app['status']}")

    return render_template('dashboard.html', featured_pets=featured_pets, recent_activities=recent_activities)


# Route: /pets
@app.route('/pets')
def pet_listings_page():
    species_filter_options = ['All', 'Dog', 'Cat', 'Bird', 'Rabbit', 'Other']
    selected_species = request.args.get('species', 'All')
    search_query = request.args.get('search', '').strip()

    pets = load_pets()

    filtered_pets = []
    for pet in pets:
        if pet['status'] != 'Available':
            continue
        if selected_species != 'All':
            if pet['species'] == 'Dog' and selected_species != 'Dog':
                if selected_species == 'Other':
                    if pet['species'] in ['Dog', 'Cat', 'Bird', 'Rabbit']:
                        continue
                else:
                    continue
            elif pet['species'] != selected_species:
                # Special case for Other
                if selected_species == 'Other':
                    if pet['species'] in ['Dog', 'Cat', 'Bird', 'Rabbit']:
                        continue
                else:
                    continue

        if search_query:
            if search_query.lower() not in pet['name'].lower():
                continue

        filtered_pets.append(pet)

    # Format pet listings
    pets_for_display = []
    for pet in filtered_pets:
        pets_for_display.append({
            'pet_id': pet['pet_id'],
            'name': pet['name'],
            'species': pet['species'],
            'age': pet['age'],
            'photo_url': f'/static/images/pets/{pet["pet_id"]}.jpg'
        })

    return render_template('pet_listings.html', pets=pets_for_display,
                           species_filter_options=species_filter_options,
                           selected_species=selected_species,
                           search_query=search_query)


# Route: /pets/<int:pet_id>
@app.route('/pets/<int:pet_id>')
def pet_details_page(pet_id):
    pet = get_pet_by_id(pet_id)
    if not pet:
        return "Pet not found", 404

    shelter = get_shelter_by_id(pet['shelter_id'])
    shelter_info = {
        'shelter_id': shelter['shelter_id'],
        'name': shelter['name'],
        'phone': shelter['phone'],
        'email': shelter['email']
    } if shelter else None

    pet_info = {
        'pet_id': pet['pet_id'],
        'name': pet['name'],
        'species': pet['species'],
        'breed': pet['breed'],
        'age': pet['age'],
        'gender': pet['gender'],
        'size': pet['size'],
        'description': pet['description'],
        'status': pet['status']
    }

    return render_template('pet_details.html', pet=pet_info, shelter_info=shelter_info)


# Route: /pets/add
@app.route('/pets/add', methods=['GET', 'POST'])
def add_pet_page():
    if request.method == 'POST':
        # Extract form data
        pet_name = request.form.get('pet-name-input', '').strip()
        pet_species = request.form.get('pet-species-input', '').strip()
        pet_breed = request.form.get('pet-breed-input', '').strip()
        pet_age = request.form.get('pet-age-input', '').strip()
        pet_gender = request.form.get('pet-gender-input', '').strip()
        pet_size = request.form.get('pet-size-input', '').strip()
        pet_description = request.form.get('pet-description-input', '').strip()

        if not pet_name or not pet_species or not pet_breed:
            # Minimal validation
            return render_template('add_pet.html', error='Pet Name, Species, and Breed are required.')

        pets = load_pets()
        pet_ids = [pet['pet_id'] for pet in pets]
        new_pet_id = max(pet_ids) + 1 if pet_ids else 1

        # Assign shelter_id 1 by default here
        shelter_id = 1
        date_added = datetime.now().strftime('%Y-%m-%d')

        new_pet = {
            'pet_id': new_pet_id,
            'name': pet_name,
            'species': pet_species,
            'breed': pet_breed,
            'age': pet_age,
            'gender': pet_gender,
            'size': pet_size,
            'description': pet_description,
            'shelter_id': shelter_id,
            'status': 'Available',
            'date_added': date_added
        }

        pets.append(new_pet)
        save_pets(pets)

        return redirect(url_for('pet_listings_page'))
    else:
        # GET
        return render_template('add_pet.html')


# Route: /applications/apply/<int:pet_id>
@app.route('/applications/apply/<int:pet_id>', methods=['GET', 'POST'])
def adoption_application_page(pet_id):
    pet = get_pet_by_id(pet_id)
    if not pet:
        return "Pet not found", 404

    if request.method == 'POST':
        applicant_name = request.form.get('applicant-name', '').strip()
        applicant_phone = request.form.get('applicant-phone', '').strip()
        housing_type = request.form.get('housing-type', '').strip()
        reason = request.form.get('reason', '').strip()

        # Simulate current username (in real app, get from session or auth)
        current_username = 'guest_user'

        if not applicant_name or not applicant_phone or not housing_type or not reason:
            return render_template('adoption_application.html', pet={'pet_id': pet['pet_id'], 'name': pet['name']}, error='All fields are required.')

        applications = load_applications()
        application_ids = [app['application_id'] for app in applications]
        new_application_id = max(application_ids) + 1 if application_ids else 1

        date_submitted = datetime.now().strftime('%Y-%m-%d')

        # Address is unknown here, other fields defaulted per schema
        new_application = {
            'application_id': new_application_id,
            'username': current_username,
            'pet_id': pet_id,
            'applicant_name': applicant_name,
            'phone': applicant_phone,
            'address': '',
            'housing_type': housing_type,
            'has_yard': 'No',
            'other_pets': '',
            'experience': '',
            'reason': reason,
            'status': 'Pending',
            'date_submitted': date_submitted
        }

        applications.append(new_application)
        save_applications(applications)

        return redirect(url_for('my_applications_page'))
    else:
        # GET
        return render_template('adoption_application.html', pet={'pet_id': pet['pet_id'], 'name': pet['name']})


# Route: /applications/my
@app.route('/applications/my')
def my_applications_page():
    # Simulate current user
    current_username = 'guest_user'

    status_filter_options = ['All', 'Pending', 'Approved', 'Rejected']
    selected_status = request.args.get('status', 'All')

    applications = load_applications()
    pets = load_pets()

    user_apps_filtered = []
    for app in applications:
        if app['username'] == current_username:
            if selected_status == 'All' or app['status'] == selected_status:
                pet_name = next((p['name'] for p in pets if p['pet_id'] == app['pet_id']), 'Unknown')
                user_apps_filtered.append({
                    'application_id': app['application_id'],
                    'pet_name': pet_name,
                    'date': app['date_submitted'],
                    'status': app['status']
                })

    return render_template('my_applications.html', 
                           applications=user_apps_filtered, 
                           status_filter_options=status_filter_options,
                           selected_status=selected_status)


# Route: /favorites
@app.route('/favorites')
def favorites_page():
    current_username = 'guest_user'

    favorites = load_favorites()
    pets = load_pets()

    user_favorites = []
    for fav in favorites:
        if fav['username'] == current_username:
            pet = next((p for p in pets if p['pet_id'] == fav['pet_id']), None)
            if pet and pet['status'] == 'Available':
                user_favorites.append({
                    'pet_id': pet['pet_id'],
                    'name': pet['name'],
                    'species': pet['species'],
                    'age': pet['age'],
                    'photo_url': f'/static/images/pets/{pet["pet_id"]}.jpg'
                })

    return render_template('favorites.html', favorite_pets=user_favorites)


# Route: /messages
@app.route('/messages', methods=['GET', 'POST'])
def messages_page():
    current_username = 'guest_user'
    messages = load_messages()
    users = load_users()

    if request.method == 'POST':
        recipient_username = request.form.get('recipient-username', '').strip()
        subject = request.form.get('subject', '').strip()
        content = request.form.get('content', '').strip()

        if not recipient_username or not subject or not content:
            conversations = []
            return render_template('messages.html', conversations=conversations, error='All fields are required.')

        # Validate recipient exists
        if not any(u['username'] == recipient_username for u in users):
            conversations = []
            return render_template('messages.html', conversations=conversations, error='Recipient not found.')

        # Create new message
        message_ids = [m['message_id'] for m in messages]
        new_message_id = max(message_ids) + 1 if message_ids else 1
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        new_message = {
            'message_id': new_message_id,
            'sender_username': current_username,
            'recipient_username': recipient_username,
            'subject': subject,
            'content': content,
            'timestamp': timestamp,
            'is_read': False
        }

        messages.append(new_message)
        save_messages(messages)

        return redirect(url_for('messages_page'))
    else:
        # GET: build conversations
        conv_dict = {}
        for msg in messages:
            if current_username in (msg['sender_username'], msg['recipient_username']):
                # conversation_id can be min msg id with that participant pair
                participants = tuple(sorted([msg['sender_username'], msg['recipient_username']]))
                if participants not in conv_dict:
                    conv_dict[participants] = []
                conv_dict[participants].append(msg)

        conversations = []
        conv_id_counter = 1
        for participants, msgs in conv_dict.items():
            last_msg = max(msgs, key=lambda m: m['timestamp'])
            # last message preview first 50 chars
            last_preview = last_msg['content'][:50]
            conversations.append({
                'conversation_id': conv_id_counter,
                'participants': list(participants),
                'last_message_preview': last_preview
            })
            conv_id_counter += 1

        return render_template('messages.html', conversations=conversations)


# Route: /profile
@app.route('/profile', methods=['GET', 'POST'])
def user_profile_page():
    # Simulate current user
    current_username = 'guest_user'
    users = load_users()
    user = next((u for u in users if u['username'] == current_username), None)

    if request.method == 'POST':
        new_email = request.form.get('profile-email', '').strip()

        if not new_email:
            return render_template('profile.html', user_profile=user, error='Email is required.')

        # Update user email
        if user:
            user['email'] = new_email
            # Save updated users to file
            filepath = os.path.join(DATA_DIR, 'users.txt')
            lines = []
            for u in users:
                line = f"{u['username']}|{u['email']}|{u['phone']}|{u['address']}"
                lines.append(line)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write('\n'.join(lines))
            user['email'] = new_email
            return redirect(url_for('user_profile_page'))
        else:
            return "User not found", 404
    else:
        # GET
        if user:
            return render_template('profile.html', user_profile=user)
        else:
            return "User not found", 404


# Route: /admin
@app.route('/admin')
def admin_panel_page():
    applications = load_applications()
    pets = load_pets()

    pending_applications = []
    users = load_users()
    for app in applications:
        if app['status'] == 'Pending':
            applicant = next((u for u in users if u['username'] == app['username']), None)
            pet = next((p for p in pets if p['pet_id'] == app['pet_id']), None)
            pending_applications.append({
                'application_id': app['application_id'],
                'applicant_name': app['applicant_name'],
                'pet_name': pet['name'] if pet else 'Unknown',
                'date_submitted': app['date_submitted']
            })

    all_pets = []
    for pet in pets:
        all_pets.append({
            'pet_id': pet['pet_id'],
            'name': pet['name'],
            'status': pet['status']
        })

    return render_template('admin_panel.html', pending_applications=pending_applications, all_pets=all_pets)


if __name__ == '__main__':
    app.run(debug=True)
