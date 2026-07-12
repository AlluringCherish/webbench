from flask import Flask, render_template, redirect, url_for, request
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

data_path = 'data'

# --- Utility functions for data handling ---

def read_file_lines(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        return lines
    except FileNotFoundError:
        return []

def write_file_lines(filename, lines):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        return True
    except Exception:
        return False

# Pets fields: id|name|species|age|description|adopted (0 or 1)
# Users fields: id|username|email|bio
# Favorites fields: user_id|pet_id
# Applications fields: id|user_id|pet_id|status
# Messages fields: id|from_user_id|to_user_id|message|timestamp

# --- Data loading functions ---

def load_pets():
    pets = []
    lines = read_file_lines(os.path.join(data_path, 'pets.txt'))
    for line in lines:
        fields = line.strip().split('|')
        if len(fields) == 6:
            pet = {
                'id': fields[0],
                'name': fields[1],
                'species': fields[2],
                'age': fields[3],
                'description': fields[4],
                'adopted': fields[5] == '1'
            }
            pets.append(pet)
    return pets

def save_pets(pets):
    lines = []
    for pet in pets:
        line = '|'.join([
            pet['id'],
            pet['name'],
            pet['species'],
            pet['age'],
            pet['description'],
            '1' if pet['adopted'] else '0'
        ]) + '\n'
        lines.append(line)
    return write_file_lines(os.path.join(data_path, 'pets.txt'), lines)


def load_users():
    users = []
    lines = read_file_lines(os.path.join(data_path, 'users.txt'))
    for line in lines:
        fields = line.strip().split('|')
        if len(fields) == 4:
            user = {
                'id': fields[0],
                'username': fields[1],
                'email': fields[2],
                'bio': fields[3]
            }
            users.append(user)
    return users


def save_users(users):
    lines = []
    for user in users:
        line = '|'.join([
            user['id'],
            user['username'],
            user['email'],
            user['bio']
        ]) + '\n'
        lines.append(line)
    return write_file_lines(os.path.join(data_path, 'users.txt'), lines)


def load_favorites():
    favorites = []
    lines = read_file_lines(os.path.join(data_path, 'favorites.txt'))
    for line in lines:
        fields = line.strip().split('|')
        if len(fields) == 2:
            favorites.append({'user_id': fields[0], 'pet_id': fields[1]})
    return favorites


def save_favorites(favorites):
    lines = []
    for fav in favorites:
        line = '|'.join([fav['user_id'], fav['pet_id']]) + '\n'
        lines.append(line)
    return write_file_lines(os.path.join(data_path, 'favorites.txt'), lines)


def load_applications():
    applications = []
    lines = read_file_lines(os.path.join(data_path, 'applications.txt'))
    for line in lines:
        fields = line.strip().split('|')
        if len(fields) == 4:
            applications.append({
                'id': fields[0],
                'user_id': fields[1],
                'pet_id': fields[2],
                'status': fields[3]
            })
    return applications


def save_applications(applications):
    lines = []
    for app in applications:
        line = '|'.join([app['id'], app['user_id'], app['pet_id'], app['status']]) + '\n'
        lines.append(line)
    return write_file_lines(os.path.join(data_path, 'applications.txt'), lines)


def load_messages():
    messages = []
    lines = read_file_lines(os.path.join(data_path, 'messages.txt'))
    for line in lines:
        fields = line.strip().split('|')
        if len(fields) == 5:
            messages.append({
                'id': fields[0],
                'from_user_id': fields[1],
                'to_user_id': fields[2],
                'message': fields[3],
                'timestamp': fields[4]
            })
    return messages


def save_messages(messages):
    lines = []
    for msg in messages:
        line = '|'.join([msg['id'], msg['from_user_id'], msg['to_user_id'], msg['message'], msg['timestamp']]) + '\n'
        lines.append(line)
    return write_file_lines(os.path.join(data_path, 'messages.txt'), lines)


# --- Route Implementations ---

@app.route('/')
def root():
    return redirect(url_for('dashboard'))

# Since design_spec.md Section 1 is not provided to me, I will implement standard routes for such an app:

@app.route('/dashboard')
def dashboard():
    pets = load_pets()
    users = load_users()
    favorites = load_favorites()
    applications = load_applications()
    messages = load_messages()
    # For dashboard, show all pets and count of applications per pet, favorites by user
    pet_app_counts = {}
    for app in applications:
        pet_app_counts[app['pet_id']] = pet_app_counts.get(app['pet_id'], 0) + 1

    context = {
        'pets': pets,
        'pet_app_counts': pet_app_counts,
        'users': users,
        'favorites': favorites,
        'applications': applications,
        'messages': messages
    }
    return render_template('dashboard.html', **context)

# Add pet
@app.route('/add_pet', methods=['GET', 'POST'])
def add_pet():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        species = request.form.get('species', '').strip()
        age = request.form.get('age', '').strip()
        description = request.form.get('description', '').strip()

        if name and species and age.isdigit():
            pets = load_pets()
            if pets:
                max_id = max(int(p['id']) for p in pets)
            else:
                max_id = 0
            new_id = str(max_id + 1)
            new_pet = {
                'id': new_id,
                'name': name,
                'species': species,
                'age': age,
                'description': description,
                'adopted': False
            }
            pets.append(new_pet)
            save_pets(pets)
            return redirect(url_for('dashboard'))
        else:
            # Data invalid, just reload form
            return render_template('add_pet.html', error='Invalid input')
    return render_template('add_pet.html')

# Submit application
@app.route('/apply', methods=['POST'])
def apply():
    user_id = request.form.get('user_id', '').strip()
    pet_id = request.form.get('pet_id', '').strip()

    if not (user_id and pet_id):
        return redirect(url_for('dashboard'))

    applications = load_applications()
    # Generate new application id
    if applications:
        max_id = max(int(app['id']) for app in applications)
    else:
        max_id = 0
    new_id = str(max_id + 1)

    # If there is already an application by this user for this pet, maybe ignore or add new anyway
    applications.append({
        'id': new_id,
        'user_id': user_id,
        'pet_id': pet_id,
        'status': 'pending'
    })
    save_applications(applications)
    return redirect(url_for('dashboard'))

# Add favorite
@app.route('/favorite', methods=['POST'])
def favorite():
    user_id = request.form.get('user_id', '').strip()
    pet_id = request.form.get('pet_id', '').strip()

    if not (user_id and pet_id):
        return redirect(url_for('dashboard'))

    favorites = load_favorites()
    # Prevent duplicate favorites
    if not any(fav['user_id'] == user_id and fav['pet_id'] == pet_id for fav in favorites):
        favorites.append({'user_id': user_id, 'pet_id': pet_id})
        save_favorites(favorites)
    return redirect(url_for('dashboard'))

# User profile - view and update
@app.route('/user/<user_id>', methods=['GET', 'POST'])
def user_profile(user_id):
    users = load_users()
    user = next((u for u in users if u['id'] == user_id), None)
    if not user:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        bio = request.form.get('bio', '').strip()

        if username and email:
            user['username'] = username
            user['email'] = email
            user['bio'] = bio
            save_users(users)
            return redirect(url_for('user_profile', user_id=user_id))
        else:
            return render_template('profile.html', user=user, error='Username and email required')

    return render_template('profile.html', user=user)

# Message sending
@app.route('/message', methods=['POST'])
def message():
    from_user_id = request.form.get('from_user_id', '').strip()
    to_user_id = request.form.get('to_user_id', '').strip()
    message_text = request.form.get('message', '').strip()
    from datetime import datetime

    if not (from_user_id and to_user_id and message_text):
        return redirect(url_for('dashboard'))

    messages = load_messages()
    if messages:
        max_id = max(int(m['id']) for m in messages)
    else:
        max_id = 0
    new_id = str(max_id + 1)
    timestamp = datetime.utcnow().isoformat() + 'Z'

    messages.append({
        'id': new_id,
        'from_user_id': from_user_id,
        'to_user_id': to_user_id,
        'message': message_text,
        'timestamp': timestamp
    })
    save_messages(messages)
    return redirect(url_for('dashboard'))


if __name__ == '__main__':
    app.run(debug=True)
