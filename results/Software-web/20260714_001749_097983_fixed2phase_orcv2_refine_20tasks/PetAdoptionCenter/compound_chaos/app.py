"""
app.py - Flask backend for Pet Adoption Center
Handles pets, applications, messages, users, shelters, favorites, and navigation.
"""
from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # For session management

def read_file(filename):
    data = []
    if not os.path.exists(filename):
        return data
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                data.append(line)
    return data

def write_file(filename, data):
    with open(filename, 'w', encoding='utf-8') as f:
        for line in data:
            f.write(line + '\n')

def parse_pets():
    # pet_id|name|species|breed|age|gender|size|description|shelter_id|status|date_added
    pets_raw = read_file('data/pets.txt')
    pets = []
    for line in pets_raw:
        parts = line.split('|')
        if len(parts) == 11:
            pet = {
                'pet_id': parts[0], 'name': parts[1], 'species': parts[2], 'breed': parts[3],
                'age': parts[4], 'gender': parts[5], 'size': parts[6], 'description': parts[7],
                'shelter_id': parts[8], 'status': parts[9], 'date_added': parts[10]
            }
            pets.append(pet)
    return pets

def save_pets(pets):
    lines = []
    for pet in pets:
        line = '|'.join([pet['pet_id'], pet['name'], pet['species'], pet['breed'], pet['age'],
                         pet['gender'], pet['size'], pet['description'], pet['shelter_id'],
                         pet['status'], pet['date_added']])
        lines.append(line)
    write_file('data/pets.txt', lines)

def parse_users():
    # username|email|phone|address
    users_raw = read_file('data/users.txt')
    users = []
    for line in users_raw:
        parts = line.split('|')
        if len(parts) == 4:
            user = {'username': parts[0], 'email': parts[1], 'phone': parts[2], 'address': parts[3]}
            users.append(user)
    return users

def save_users(users):
    lines = []
    for user in users:
        line = '|'.join([user['username'], user['email'], user['phone'], user['address']])
        lines.append(line)
    write_file('data/users.txt', lines)

def parse_shelters():
    # shelter_id|name|address|phone|email
    shelters_raw = read_file('data/shelters.txt')
    shelters = []
    for line in shelters_raw:
        parts = line.split('|')
        if len(parts) == 5:
            shelter = {'shelter_id': parts[0],'name': parts[1],'address': parts[2],'phone': parts[3],'email': parts[4]}
            shelters.append(shelter)
    return shelters

def parse_applications():
    # application_id|username|pet_id|applicant_name|phone|address|housing_type|has_yard|other_pets|experience|reason|status|date_submitted
    apps_raw = read_file('data/applications.txt')
    apps = []
    for line in apps_raw:
        parts = line.split('|')
        if len(parts) == 13:
            app = {
                'application_id': parts[0], 'username': parts[1], 'pet_id': parts[2], 'applicant_name': parts[3],
                'phone': parts[4], 'address': parts[5], 'housing_type': parts[6], 'has_yard': parts[7],
                'other_pets': parts[8], 'experience': parts[9], 'reason': parts[10], 'status': parts[11],
                'date_submitted': parts[12]
            }
            apps.append(app)
    return apps

def save_applications(apps):
    lines = []
    for app in apps:
        line = '|'.join([app['application_id'], app['username'], app['pet_id'], app['applicant_name'],
                         app['phone'], app['address'], app['housing_type'], app['has_yard'], app['other_pets'],
                         app['experience'], app['reason'], app['status'], app['date_submitted']])
        lines.append(line)
    write_file('data/applications.txt', lines)

def parse_messages():
    # message_id|sender_username|recipient_username|subject|content|timestamp|is_read
    messages_raw = read_file('data/messages.txt')
    messages = []
    for line in messages_raw:
        parts = line.split('|')
        if len(parts) == 7:
            message = {
                'message_id': parts[0], 'sender_username': parts[1], 'recipient_username': parts[2],
                'subject': parts[3], 'content': parts[4], 'timestamp': parts[5], 'is_read': parts[6]
            }
            messages.append(message)
    return messages

def save_messages(messages):
    lines = []
    for msg in messages:
        line = '|'.join([msg['message_id'], msg['sender_username'], msg['recipient_username'],
                         msg['subject'], msg['content'], msg['timestamp'], msg['is_read']])
        lines.append(line)
    write_file('data/messages.txt', lines)

def parse_favorites():
    # username|pet_id|date_added
    favs_raw = read_file('data/favorites.txt')
    favs = []
    for line in favs_raw:
        parts = line.split('|')
        if len(parts) == 3:
            fav = {'username': parts[0], 'pet_id': parts[1], 'date_added': parts[2]}
            favs.append(fav)
    return favs

def save_favorites(favs):
    lines = []
    for fav in favs:
        line = '|'.join([fav['username'], fav['pet_id'], fav['date_added']])
        lines.append(line)
    write_file('data/favorites.txt', lines)

def parse_adoption_history():
    # history_id|username|pet_id|pet_name|adoption_date|shelter_id
    history_raw = read_file('data/adoption_history.txt')
    history = []
    for line in history_raw:
        parts = line.split('|')
        if len(parts) == 6:
            rec = {'history_id': parts[0], 'username': parts[1], 'pet_id': parts[2], 'pet_name': parts[3],
                   'adoption_date': parts[4], 'shelter_id': parts[5]}
            history.append(rec)
    return history

def save_adoption_history(history):
    lines = []
    for h in history:
        line = '|'.join([h['history_id'], h['username'], h['pet_id'], h['pet_name'], h['adoption_date'], h['shelter_id']])
        lines.append(line)
    write_file('data/adoption_history.txt', lines)

@app.route('/')
@app.route('/dashboard')
def dashboard():
    """Render dashboard page showing stats and navigation."""
    pets = parse_pets()
    users = parse_users()
    shelters = parse_shelters()
    applications = parse_applications()
    favorites = parse_favorites()
    messages = parse_messages()
    adoption_history = parse_adoption_history()
    # Summarize some stats
    total_pets = len(pets)
    total_users = len(users)
    total_shelters = len(shelters)
    pending_applications = len([a for a in applications if a['status'] == 'Pending'])
    return render_template('dashboard.html', total_pets=total_pets, total_users=total_users,
                           total_shelters=total_shelters, pending_applications=pending_applications)

@app.route('/pet-listings')
def pet_listings():
    """List all pets with optional filters."""
    species_filter = request.args.get('species', '')
    status_filter = request.args.get('status', '')
    pets = parse_pets()
    if species_filter:
        pets = [p for p in pets if p['species'].lower() == species_filter.lower()]
    if status_filter:
        pets = [p for p in pets if p['status'].lower() == status_filter.lower()]
    shelters = parse_shelters()
    return render_template('pet_listings.html', pets=pets, shelters=shelters,
                           species_filter=species_filter, status_filter=status_filter)

@app.route('/pet-details/<pet_id>')
def pet_details(pet_id):
    """Show detailed info about a specific pet."""
    pets = parse_pets()
    pet = next((p for p in pets if p['pet_id'] == pet_id), None)
    shelters = parse_shelters()
    shelter = next((s for s in shelters if s['shelter_id'] == pet['shelter_id']), None) if pet else None
    return render_template('pet_details.html', pet=pet, shelter=shelter)

@app.route('/add-pet', methods=['GET', 'POST'])
def add_pet():
    """Add a new pet (admin only)."""
    if request.method == 'POST':
        pets = parse_pets()
        # collect form data
        new_id = str(max([int(p['pet_id']) for p in pets] + [0]) + 1)
        new_pet = {
            'pet_id': new_id,
            'name': request.form['name'],
            'species': request.form['species'],
            'breed': request.form['breed'],
            'age': request.form['age'],
            'gender': request.form['gender'],
            'size': request.form['size'],
            'description': request.form['description'],
            'shelter_id': request.form['shelter_id'],
            'status': 'Available',
            'date_added': datetime.now().strftime('%Y-%m-%d')
        }
        pets.append(new_pet)
        save_pets(pets)
        flash('Pet added successfully!')
        return redirect(url_for('pet_listings'))
    shelters = parse_shelters()
    return render_template('add_pet.html', shelters=shelters)

@app.route('/edit-pet/<pet_id>', methods=['GET', 'POST'])
def edit_pet(pet_id):
    """Edit an existing pet's details."""
    pets = parse_pets()
    pet = next((p for p in pets if p['pet_id'] == pet_id), None)
    if not pet:
        flash('Pet not found.')
        return redirect(url_for('pet_listings'))
    if request.method == 'POST':
        pet['name'] = request.form['name']
        pet['species'] = request.form['species']
        pet['breed'] = request.form['breed']
        pet['age'] = request.form['age']
        pet['gender'] = request.form['gender']
        pet['size'] = request.form['size']
        pet['description'] = request.form['description']
        pet['shelter_id'] = request.form['shelter_id']
        pet['status'] = request.form['status']
        save_pets(pets)
        flash('Pet updated successfully!')
        return redirect(url_for('pet_details', pet_id=pet_id))
    shelters = parse_shelters()
    return render_template('edit_pet.html', pet=pet, shelters=shelters)

@app.route('/delete-pet/<pet_id>', methods=['POST'])
def delete_pet(pet_id):
    """Delete a pet (admin only)."""
    pets = parse_pets()
    pets = [p for p in pets if p['pet_id'] != pet_id]
    save_pets(pets)
    flash('Pet deleted successfully!')
    return redirect(url_for('pet_listings'))

@app.route('/applications')
def applications():
    """Show list of adoption applications."""
    apps = parse_applications()
    pets = parse_pets()
    return render_template('applications.html', applications=apps, pets=pets)

@app.route('/my-applications/<username>')
def my_applications(username):
    """Show applications made by the logged in user."""
    apps = parse_applications()
    pets = parse_pets()
    user_apps = [a for a in apps if a['username'] == username]
    return render_template('my_applications.html', applications=user_apps, pets=pets, username=username)

@app.route('/submit-application/<pet_id>', methods=['GET', 'POST'])
def submit_application(pet_id):
    """Submit adoption application for a pet."""
    if request.method == 'POST':
        apps = parse_applications()
        new_id = str(max([int(a['application_id']) for a in apps] + [0]) + 1)
        app_data = {
            'application_id': new_id,
            'username': session.get('username', 'anonymous'),
            'pet_id': pet_id,
            'applicant_name': request.form['applicant_name'],
            'phone': request.form['phone'],
            'address': request.form['address'],
            'housing_type': request.form['housing_type'],
            'has_yard': request.form.get('has_yard', 'No'),
            'other_pets': request.form.get('other_pets', 'No'),
            'experience': request.form['experience'],
            'reason': request.form['reason'],
            'status': 'Pending',
            'date_submitted': datetime.now().strftime('%Y-%m-%d')
        }
        apps.append(app_data)
        save_applications(apps)
        flash('Application submitted successfully')
        return redirect(url_for('pet_details', pet_id=pet_id))
    pet = next((p for p in parse_pets() if p['pet_id'] == pet_id), None)
    return render_template('submit_application.html', pet=pet)

@app.route('/favorites/<username>')
def favorites(username):
    """Show user's favorite pets."""
    favs = parse_favorites()
    pets = parse_pets()
    user_favs = [f for f in favs if f['username'] == username]
    fav_pets = [p for p in pets if any(f['pet_id'] == p['pet_id'] for f in user_favs)]
    return render_template('favorites.html', pets=fav_pets, username=username)

@app.route('/add-favorite/<username>/<pet_id>', methods=['POST'])
def add_favorite(username, pet_id):
    """Add pet to user's favorites."""
    favs = parse_favorites()
    if not any(f['username'] == username and f['pet_id'] == pet_id for f in favs):
        favs.append({'username': username, 'pet_id': pet_id, 'date_added': datetime.now().strftime('%Y-%m-%d')})
        save_favorites(favs)
    return redirect(url_for('favorites', username=username))

@app.route('/remove-favorite/<username>/<pet_id>', methods=['POST'])
def remove_favorite(username, pet_id):
    """Remove pet from user's favorites."""
    favs = parse_favorites()
    favs = [f for f in favs if not (f['username'] == username and f['pet_id'] == pet_id)]
    save_favorites(favs)
    return redirect(url_for('favorites', username=username))

@app.route('/messages/<username>')
def messages(username):
    """Show messages for the user."""
    msgs = parse_messages()
    user_msgs = [m for m in msgs if m['recipient_username'] == username]
    return render_template('messages.html', messages=user_msgs, username=username)

@app.route('/send-message/<sender>/<recipient>', methods=['GET', 'POST'])
def send_message(sender, recipient):
    """Send a message from sender to recipient."""
    if request.method == 'POST':
        msgs = parse_messages()
        new_id = str(max([int(m['message_id']) for m in msgs] + [0]) + 1)
        msg = {
            'message_id': new_id,
            'sender_username': sender,
            'recipient_username': recipient,
            'subject': request.form['subject'],
            'content': request.form['content'],
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'is_read': 'false'
        }
        msgs.append(msg)
        save_messages(msgs)
        flash('Message sent successfully')
        return redirect(url_for('messages', username=recipient))
    return render_template('send_message.html', sender=sender, recipient=recipient)

@app.route('/profile/<username>', methods=['GET', 'POST'])
def profile(username):
    """Show and update user profile."""
    users = parse_users()
    user = next((u for u in users if u['username'] == username), None)
    if not user:
        flash('User not found')
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        user['email'] = request.form['email']
        user['phone'] = request.form['phone']
        user['address'] = request.form['address']
        save_users(users)
        flash('Profile updated successfully!')
        return redirect(url_for('profile', username=username))
    return render_template('profile.html', user=user)

@app.route('/admin')
def admin_panel():
    """Admin panel - manage users and shelters."""
    users = parse_users()
    shelters = parse_shelters()
    return render_template('admin_panel.html', users=users, shelters=shelters)

if __name__ == '__main__':
    app.run(debug=True)
