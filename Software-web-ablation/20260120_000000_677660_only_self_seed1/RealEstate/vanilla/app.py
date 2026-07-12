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


# Utility functions for loading data

def load_properties():
    properties = []
    if not os.path.exists(PROPERTIES_FILE):
        return properties
    try:
        with open(PROPERTIES_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 11:
                    prop = {
                        'property_id': int(parts[0]),
                        'address': parts[1],
                        'location': parts[2],
                        'price': float(parts[3]),
                        'property_type': parts[4],
                        'bedrooms': int(parts[5]),
                        'bathrooms': float(parts[6]),
                        'square_feet': int(parts[7]),
                        'description': parts[8],
                        'agent_id': int(parts[9]),
                        'status': parts[10]
                    }
                    properties.append(prop)
    except Exception:
        # On read error, return empty list
        properties = []
    return properties


def load_locations():
    locations = []
    if not os.path.exists(LOCATIONS_FILE):
        return locations
    try:
        with open(LOCATIONS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 6:
                    loc = {
                        'location_id': int(parts[0]),
                        'location_name': parts[1],
                        'region': parts[2],
                        'average_price': float(parts[3]),
                        'property_count': int(parts[4]),
                        'description': parts[5]
                    }
                    locations.append(loc)
    except Exception:
        locations = []
    return locations


def load_inquiries():
    inquiries = []
    if not os.path.exists(INQUIRIES_FILE):
        return inquiries
    try:
        with open(INQUIRIES_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 8:
                    inq = {
                        'inquiry_id': int(parts[0]),
                        'property_id': int(parts[1]),
                        'customer_name': parts[2],
                        'customer_email': parts[3],
                        'customer_phone': parts[4],
                        'message': parts[5],
                        'inquiry_date': parts[6],
                        'status': parts[7]
                    }
                    inquiries.append(inq)
    except Exception:
        inquiries = []
    return inquiries


def load_favorites():
    favorites = []
    if not os.path.exists(FAVORITES_FILE):
        return favorites
    try:
        with open(FAVORITES_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 3:
                    fav = {
                        'favorite_id': int(parts[0]),
                        'property_id': int(parts[1]),
                        'added_date': parts[2]
                    }
                    favorites.append(fav)
    except Exception:
        favorites = []
    return favorites


def load_agents():
    agents = []
    if not os.path.exists(AGENTS_FILE):
        return agents
    try:
        with open(AGENTS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 6:
                    ag = {
                        'agent_id': int(parts[0]),
                        'agent_name': parts[1],
                        'specialization': parts[2],
                        'email': parts[3],
                        'phone': parts[4],
                        'properties_sold': int(parts[5])
                    }
                    agents.append(ag)
    except Exception:
        agents = []
    return agents


# Utility functions for saving data

def save_inquiries(inquiries):
    try:
        with open(INQUIRIES_FILE, 'w', encoding='utf-8') as f:
            for inq in inquiries:
                line = f"{inq['inquiry_id']}|{inq['property_id']}|{inq['customer_name']}|{inq['customer_email']}|{inq['customer_phone']}|{inq['message']}|{inq['inquiry_date']}|{inq['status']}\n"
                f.write(line)
        return True
    except Exception:
        return False


def save_favorites(favorites):
    try:
        with open(FAVORITES_FILE, 'w', encoding='utf-8') as f:
            for fav in favorites:
                line = f"{fav['favorite_id']}|{fav['property_id']}|{fav['added_date']}\n"
                f.write(line)
        return True
    except Exception:
        return False


# Routes implementation

# 1. Root Redirect
@app.route('/', methods=['GET'])
def root_redirect():
    return redirect(url_for('dashboard_page'))


# 2. Dashboard Page
@app.route('/dashboard', methods=['GET'])
def dashboard_page():
    properties = load_properties()
    # Featured properties: let's pick first 3 Available properties
    featured_properties = [p for p in properties if p['status'] == 'Available'][:3]
    # Recent listings: sorted by property_id descending, get top 3 (if status Available)
    recent_listings = sorted([p for p in properties if p['status'] == 'Available'], key=lambda x: x['property_id'], reverse=True)[:3]
    return render_template('dashboard.html', featured_properties=featured_properties, recent_listings=recent_listings)


# 3. Property Search Page
@app.route('/properties/search', methods=['GET'])
def property_search():
    properties = [p for p in load_properties() if p['status'] == 'Available']
    # Extract distinct property types for filter dropdown
    property_types_set = set(p['property_type'] for p in properties)
    filter_options = {'property_types': sorted(property_types_set)}
    return render_template('property_search.html', properties=properties, filter_options=filter_options)


@app.route('/properties/search', methods=['POST'])
def property_search_filter():
    properties = [p for p in load_properties() if p['status'] == 'Available']
    try:
        location_input = request.form.get('location_input', '').strip()
        price_range_min = request.form.get('price_range_min', '').strip()
        price_range_max = request.form.get('price_range_max', '').strip()
        property_type_filter = request.form.get('property_type_filter', '').strip()

        # Convert price inputs to float if valid, else None
        min_price = float(price_range_min) if price_range_min else None
        max_price = float(price_range_max) if price_range_max else None

    except Exception:
        # In case of conversion error, ignore filters
        location_input = ''
        min_price = None
        max_price = None
        property_type_filter = ''

    # Filter by location input (case insensitive substring match)
    if location_input:
        properties = [p for p in properties if location_input.lower() in p['location'].lower()]

    # Filter by price range
    if min_price is not None:
        properties = [p for p in properties if p['price'] >= min_price]
    if max_price is not None:
        properties = [p for p in properties if p['price'] <= max_price]

    # Filter by property type
    if property_type_filter:
        properties = [p for p in properties if p['property_type'] == property_type_filter]

    # Extract distinct property types for filter dropdown
    all_properties = [p for p in load_properties() if p['status'] == 'Available']
    property_types_set = set(p['property_type'] for p in all_properties)
    filter_options = {'property_types': sorted(property_types_set)}

    return render_template('property_search.html', properties=properties, filter_options=filter_options)


# 4. Property Details Page
@app.route('/property/<int:property_id>', methods=['GET'])
def property_details(property_id):
    properties = load_properties()
    agents = load_agents()
    property_item = None
    agent_item = None
    for p in properties:
        if p['property_id'] == property_id:
            property_item = p
            break
    if property_item:
        for a in agents:
            if a['agent_id'] == property_item['agent_id']:
                agent_item = a
                break
    return render_template('property_details.html', property=property_item, agent=agent_item)


# 5. Property Inquiry Page
@app.route('/property/inquiry', methods=['GET'])
def property_inquiry_form():
    properties = load_properties()
    # Show only available properties for dropdown
    properties = [p for p in properties if p['status'] == 'Available']
    return render_template('property_inquiry.html', properties=properties, submission_status=None)


@app.route('/property/inquiry', methods=['POST'])
def submit_property_inquiry():
    properties = load_properties()
    properties = [p for p in properties if p['status'] == 'Available']

    # Get form data
    try:
        select_property = int(request.form.get('select_property', 0))
        inquiry_name = request.form.get('inquiry_name', '').strip()
        inquiry_email = request.form.get('inquiry_email', '').strip()
        inquiry_phone = request.form.get('inquiry_phone', '').strip()
        inquiry_message = request.form.get('inquiry_message', '').strip()
    except Exception:
        select_property = 0
        inquiry_name = inquiry_email = inquiry_phone = inquiry_message = ''

    # Validate inputs
    if (select_property == 0 or
        inquiry_name == '' or
        inquiry_email == '' or
        inquiry_phone == '' or
        inquiry_message == ''):
        submission_status = 'Error: All fields are required.'
        return render_template('property_inquiry.html', properties=properties, submission_status=submission_status)

    # Check if selected property exists and is available
    chosen_property = next((p for p in properties if p['property_id'] == select_property), None)
    if chosen_property is None:
        submission_status = 'Error: Selected property is not available.'
        return render_template('property_inquiry.html', properties=properties, submission_status=submission_status)

    # Load existing inquiries
    inquiries = load_inquiries()

    # Generate new inquiry_id (max existing + 1)
    new_id = 1
    if inquiries:
        new_id = max(inq['inquiry_id'] for inq in inquiries) + 1

    inquiry_date = datetime.now().strftime('%Y-%m-%d')

    new_inquiry = {
        'inquiry_id': new_id,
        'property_id': select_property,
        'customer_name': inquiry_name,
        'customer_email': inquiry_email,
        'customer_phone': inquiry_phone,
        'message': inquiry_message,
        'inquiry_date': inquiry_date,
        'status': 'Pending'
    }

    inquiries.append(new_inquiry)

    # Save updated inquiries
    saved = save_inquiries(inquiries)

    if saved:
        submission_status = 'Inquiry submitted successfully.'
    else:
        submission_status = 'Failed to submit inquiry. Please try again later.'

    return render_template('property_inquiry.html', properties=properties, submission_status=submission_status)


# 6. My Inquiries Page
@app.route('/inquiries', methods=['GET'])
def my_inquiries():
    inquiries = load_inquiries()
    status_filter_options = ['All', 'Pending', 'Contacted', 'Resolved']
    return render_template('my_inquiries.html', inquiries=inquiries, status_filter_options=status_filter_options)


# 7. Inquiries Filter POST Route
@app.route('/inquiries/filter', methods=['POST'])
def filter_inquiries():
    inquiry_status_filter = request.form.get('inquiry_status_filter', 'All')
    inquiries = load_inquiries()
    status_filter_options = ['All', 'Pending', 'Contacted', 'Resolved']

    if inquiry_status_filter != 'All':
        filtered = [inq for inq in inquiries if inq['status'] == inquiry_status_filter]
    else:
        filtered = inquiries

    return render_template('my_inquiries.html', inquiries=filtered, status_filter_options=status_filter_options, applied_filter=inquiry_status_filter)


# 8. Delete Inquiry POST Route
@app.route('/inquiries/delete/<int:inquiry_id>', methods=['POST'])
def delete_inquiry(inquiry_id):
    inquiries = load_inquiries()
    filtered = [inq for inq in inquiries if inq['inquiry_id'] != inquiry_id]
    save_inquiries(filtered)
    return redirect(url_for('my_inquiries'))


# 9. My Favorites Page
@app.route('/favorites', methods=['GET'])
def my_favorites():
    favorites = load_favorites()
    properties = load_properties()

    # Map property_id to property dict for quick lookup
    prop_map = {p['property_id']: p for p in properties}

    # Build list of favorite properties with details
    favorite_properties = []
    for fav in favorites:
        prop = prop_map.get(fav['property_id'])
        if prop and prop['status'] == 'Available':
            favorite_properties.append(prop)

    return render_template('my_favorites.html', favorite_properties=favorite_properties)


# 10. Remove Favorite POST Route
@app.route('/favorites/remove/<int:property_id>', methods=['POST'])
def remove_favorite(property_id):
    favorites = load_favorites()
    favorites = [fav for fav in favorites if fav['property_id'] != property_id]
    save_favorites(favorites)
    return redirect(url_for('my_favorites'))


# 11. Agent Directory Page
@app.route('/agents', methods=['GET'])
def agent_directory():
    agents = load_agents()
    return render_template('agents.html', agents=agents)


# 12. Locations Page
@app.route('/locations', methods=['GET'])
def locations_page():
    locations = load_locations()
    sort_options = ['By Name', 'By Properties Count', 'By Average Price']
    return render_template('locations.html', locations=locations, sort_options=sort_options)


if __name__ == '__main__':
    app.run(debug=True)
