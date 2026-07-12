from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


# Mock data for demonstration
featured_pets = [
    {
        'pet_id': 1,
        'name': 'Buddy',
        'species': 'Dog',
        'breed': 'Golden Retriever',
        'age': 3,
        'gender': 'Male',
        'size': 'Large',
        'status': 'Available',
        'description': 'Friendly and energetic dog.',
        'photo_url': '/static/images/buddy.jpg',
        'date_added': '2024-11-01'
    }
]

all_pets = [
    {
        'pet_id': 1,
        'name': 'Buddy',
        'species': 'Dog',
        'breed': 'Golden Retriever',
        'age': 3,
        'gender': 'Male',
        'size': 'Large',
        'status': 'Available',
        'description': 'Friendly and energetic dog.',
        'photo_url': '/static/images/buddy.jpg',
        'date_added': '2024-11-01'
    },
    {
        'pet_id': 2,
        'name': 'Whiskers',
        'species': 'Cat',
        'breed': 'Siamese',
        'age': 2,
        'gender': 'Female',
        'size': 'Small',
        'status': 'Available',
        'description': 'Calm and affectionate cat.',
        'photo_url': '/static/images/whiskers.jpg',
        'date_added': '2024-10-15'
    }
]

@app.route('/dashboard')
def dashboard():
    # Context variables
    page_title = "Pet Adoption Dashboard"
    username = request.args.get('username', 'Guest')
    is_admin = False  # example condition
    context = {
        'page_title': page_title,
        'username': username,
        'featured_pets': featured_pets,
        'all_pets': all_pets,
        'is_admin': is_admin
    }
    return render_template('dashboard.html', **context)

# Additional route placeholders for navigation URLs
@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))

@app.route('/pets')
def pet_listings():
    # just redirect or render placeholder
    return "Pet Listings Page"

@app.route('/applications')
def applications():
    return "Applications Page"

@app.route('/favorites')
def favorites():
    return "Favorites Page"

@app.route('/messages')
def messages():
    return "Messages Page"

@app.route('/profile')
def profile():
    return "User Profile Page"

@app.route('/admin')
def admin_panel():
    return "Admin Panel Page"

@app.route('/pets/<int:pet_id>')
def pet_details(pet_id):
    return f"Details of pet {pet_id}"

@app.route('/applications/new/<int:pet_id>')
def adoption_application_page(pet_id):
    return f"Adoption application page for pet {pet_id}"

if __name__ == '__main__':
    app.run(debug=True)
