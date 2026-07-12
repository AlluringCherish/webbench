from flask import Flask, render_template, redirect, url_for, request
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

# File paths
PROPERTIES_FILE = 'data/properties.txt'
LOCATIONS_FILE = 'data/locations.txt'
INQUIRIES_FILE = 'data/inquiries.txt'
FAVORITES_FILE = 'data/favorites.txt'
AGENTS_FILE = 'data/agents.txt'

# Utility functions for reading data files

def read_properties():
    properties = []
    if not os.path.exists(PROPERTIES_FILE):
        return properties
    with open(PROPERTIES_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) < 11:
                continue
            property_entry = {
                'property_id': int(parts[0]),
                'address': parts[1],
                'location': parts[2],
                'price': float(parts[3]),
                'property_type': parts[4],
                'bedrooms': float(parts[5]) if '.' in parts[5] else int(parts[5]),
                'bathrooms': float(parts[6]) if '.' in parts[6] else int(parts[6]),
                'square_feet': int(parts[7]),
                'description': parts[8],
                'agent_id': int(parts[9]),
                'status': parts[10]
            }
            properties.append(property_entry)
    return properties


def read_locations():
    locations = []
    if not os.path.exists(LOCATIONS_FILE):
        return locations
    with open(LOCATIONS_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) < 6:
                continue
            location_entry = {
                'location_id': int(parts[0]),
                'location_name': parts[1],
                'region': parts[2],
                'average_price': float(parts[3]),
                'property_count': int(parts[4]),
                'description': parts[5]
            }
            locations.append(location_entry)
    return locations


def read_inquiries():
    inquiries = []
    if not os.path.exists(INQUIRIES_FILE):
        return inquiries
    with open(INQUIRIES_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) < 8:
                continue
            inquiry_entry = {
                'inquiry_id': int(parts[0]),
                'property_id': int(parts[1]),
                'customer_name': parts[2],
                'customer_email': parts[3],
                'customer_phone': parts[4],
                'message': parts[5],
                'inquiry_date': parts[6],
                'status': parts[7]
            }
            inquiries.append(inquiry_entry)
    return inquiries


def read_favorites():
    favorites = []
    if not os.path.exists(FAVORITES_FILE):
        return favorites
    with open(FAVORITES_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) < 3:
                continue
            favorite_entry = {
                'favorite_id': int(parts[0]),
                'property_id': int(parts[1]),
                'added_date': parts[2]
            }
            favorites.append(favorite_entry)
    return favorites


def read_agents():
    agents = []
    if not os.path.exists(AGENTS_FILE):
        return agents
    with open(AGENTS_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) < 6:
                continue
            agent_entry = {
                'agent_id': int(parts[0]),
                'agent_name': parts[1],
                'specialization': parts[2],
                'email': parts[3],
                'phone': parts[4],
                'properties_sold': int(parts[5])
            }
            agents.append(agent_entry)
    return agents

# Utility functions for saving data files

def save_inquiries(inquiries):
    try:
        with open(INQUIRIES_FILE, 'w', encoding='utf-8') as f:
            for i in inquiries:
                line = '|'.join([
                    str(i['inquiry_id']),
                    str(i['property_id']),
                    i['customer_name'],
                    i['customer_email'],
                    i['customer_phone'],
                    i['message'],
                    i['inquiry_date'],
                    i['status']
                ])
                f.write(line + '\n')
    except IOError:
        # Handle error silently
        pass


def save_favorites(favorites):
    try:
        with open(FAVORITES_FILE, 'w', encoding='utf-8') as f:
            for fav in favorites:
                line = '|'.join([
                    str(fav['favorite_id']),
                    str(fav['property_id']),
                    fav['added_date']
                ])
                f.write(line + '\n')
    except IOError:
        # Handle error silently
        pass


@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard_page'))


@app.route('/dashboard', methods=['GET'])
def dashboard_page():
    properties = read_properties()
    # For the purpose of featured_properties, select 'Available' status and top 3 by price descending
    featured_properties = sorted(
        [p for p in properties if p['status'] == 'Available'],
        key=lambda x: x['price'], reverse=True
    )[:3]
    # recent_listings: sort all available by descending property_id (most recent) top 5
    recent_listings = sorted(
        [p for p in properties if p['status'] == 'Available'],
        key=lambda x: x['property_id'], reverse=True
    )[:5]
    return render_template('dashboard.html', featured_properties=featured_properties, recent_listings=recent_listings)


@app.route('/properties/search', methods=['GET'])
def property_search_page():
    # Load all properties
    properties = read_properties()
    # Gather filter options
    property_types = sorted(set(p['property_type'] for p in properties))
    filter_options = {
        'property_types': property_types,
    }
    # Render the property_search.html with all properties and filter options
    return render_template('property_search.html', properties=properties, filter_options=filter_options)


@app.route('/properties/<int:property_id>', methods=['GET'])
def property_details_page(property_id):
    properties = read_properties()
    property_data = next((p for p in properties if p['property_id'] == property_id), None)
    if property_data is None:
        # Return 404 or redirect to search page
        return redirect(url_for('property_search_page'))
    return render_template('property_details.html', property=property_data)


@app.route('/inquiries/submit', methods=['GET'])
def inquiry_form_page():
    properties = read_properties()
    # Only properties with status 'Available' should be in inquiry
    available_properties = [p for p in properties if p['status'] == 'Available']
    return render_template('inquiry_form.html', properties=available_properties)


@app.route('/inquiries/submit', methods=['POST'])
def submit_inquiry():
    # Get form data safely
    property_id = request.form.get('property_id', type=int)
    customer_name = request.form.get('customer_name', '').strip()
    customer_email = request.form.get('customer_email', '').strip()
    customer_phone = request.form.get('customer_phone', '').strip()
    inquiry_message = request.form.get('inquiry_message', '').strip()

    # Validate mandatory fields
    if not (property_id and customer_name and customer_email and customer_phone and inquiry_message):
        # Invalid submission, redirect back to form
        return redirect(url_for('inquiry_form_page'))

    # Read current inquiries
    inquiries = read_inquiries()
    # Determine new inquiry_id
    if inquiries:
        new_id = max(i['inquiry_id'] for i in inquiries) + 1
    else:
        new_id = 1

    # Current date
    inquiry_date = datetime.now().strftime('%Y-%m-%d')

    # Add new inquiry entry with status Pending
    new_inquiry = {
        'inquiry_id': new_id,
        'property_id': property_id,
        'customer_name': customer_name,
        'customer_email': customer_email,
        'customer_phone': customer_phone,
        'message': inquiry_message,
        'inquiry_date': inquiry_date,
        'status': 'Pending'
    }
    inquiries.append(new_inquiry)
    save_inquiries(inquiries)

    # Redirect to inquiries page after submission
    return redirect(url_for('my_inquiries_page'))


@app.route('/inquiries', methods=['GET'])
def my_inquiries_page():
    inquiries = read_inquiries()
    return render_template('inquiries.html', inquiries=inquiries)


@app.route('/inquiries/delete/<int:inquiry_id>', methods=['POST'])
def delete_inquiry(inquiry_id):
    inquiries = read_inquiries()
    inquiries = [inq for inq in inquiries if inq['inquiry_id'] != inquiry_id]
    save_inquiries(inquiries)
    return redirect(url_for('my_inquiries_page'))


@app.route('/favorites', methods=['GET'])
def my_favorites_page():
    favorites = read_favorites()
    properties = read_properties()
    # Map property_id to property dict
    properties_by_id = {p['property_id']: p for p in properties}
    return render_template('favorites.html', favorites=favorites, properties_by_id=properties_by_id)


@app.route('/favorites/add/<int:property_id>', methods=['POST'])
def add_to_favorites(property_id):
    favorites = read_favorites()
    # Check if already favorited
    if any(fav['property_id'] == property_id for fav in favorites):
        # Already in favorites - no duplicates
        return redirect(url_for('my_favorites_page'))

    # Determine new favorite_id
    if favorites:
        new_id = max(fav['favorite_id'] for fav in favorites) + 1
    else:
        new_id = 1

    added_date = datetime.now().strftime('%Y-%m-%d')
    new_favorite = {
        'favorite_id': new_id,
        'property_id': property_id,
        'added_date': added_date
    }
    favorites.append(new_favorite)
    save_favorites(favorites)

    return redirect(url_for('my_favorites_page'))


@app.route('/favorites/remove/<int:property_id>', methods=['POST'])
def remove_from_favorites(property_id):
    favorites = read_favorites()
    favorites = [fav for fav in favorites if fav['property_id'] != property_id]
    save_favorites(favorites)
    return redirect(url_for('my_favorites_page'))


@app.route('/agents', methods=['GET'])
def agents_directory_page():
    agents = read_agents()
    return render_template('agents.html', agents=agents)


@app.route('/locations', methods=['GET'])
def locations_page():
    locations = read_locations()
    return render_template('locations.html', locations=locations)


if __name__ == '__main__':
    app.run(debug=True)
