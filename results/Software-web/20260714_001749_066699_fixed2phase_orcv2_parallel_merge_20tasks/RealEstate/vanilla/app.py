from flask import Flask, render_template, request, jsonify, redirect, url_for
from datetime import datetime
import os

app = Flask(__name__)

# File paths for data storage
PROPERTY_FILE = 'properties.txt'
LOCATION_FILE = 'locations.txt'
INQUIRY_FILE = 'inquiries.txt'
FAVORITES_FILE = 'favorites.txt'
AGENT_FILE = 'agents.txt'

# Data parsing and loading functions

def parse_properties():
    properties = []
    if os.path.exists(PROPERTY_FILE):
        with open(PROPERTY_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    # property_id,address,location,price,property_type,bedrooms,bathrooms,square_feet,description,agent_id,status
                    parts = line.split('|')
                    if len(parts) == 11:
                        try:
                            property_dict = {
                                'property_id': int(parts[0]),
                                'address': parts[1],
                                'location': parts[2],
                                'price': float(parts[3]),
                                'property_type': parts[4],
                                'bedrooms': int(parts[5]),
                                'bathrooms': int(parts[6]),
                                'square_feet': int(parts[7]),
                                'description': parts[8],
                                'agent_id': int(parts[9]),
                                'status': parts[10]
                            }
                            properties.append(property_dict)
                        except ValueError:
                            continue
    return properties

def parse_locations():
    locations = []
    if os.path.exists(LOCATION_FILE):
        with open(LOCATION_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    # location_id,location_name,region,average_price,property_count,description
                    parts = line.split('|')
                    if len(parts) == 6:
                        try:
                            location_dict = {
                                'location_id': int(parts[0]),
                                'location_name': parts[1],
                                'region': parts[2],
                                'average_price': float(parts[3]),
                                'property_count': int(parts[4]),
                                'description': parts[5]
                            }
                            locations.append(location_dict)
                        except ValueError:
                            continue
    return locations

def parse_inquiries():
    inquiries = []
    if os.path.exists(INQUIRY_FILE):
        with open(INQUIRY_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    # inquiry_id,property_id,customer_name,customer_email,customer_phone,message,inquiry_date,status
                    parts = line.split('|')
                    if len(parts) == 8:
                        try:
                            inquiry_dict = {
                                'inquiry_id': int(parts[0]),
                                'property_id': int(parts[1]),
                                'customer_name': parts[2],
                                'customer_email': parts[3],
                                'customer_phone': parts[4],
                                'message': parts[5],
                                'inquiry_date': parts[6],
                                'status': parts[7]
                            }
                            inquiries.append(inquiry_dict)
                        except ValueError:
                            continue
    return inquiries

def parse_favorites():
    favorites = []
    if os.path.exists(FAVORITES_FILE):
        with open(FAVORITES_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    # favorite_id,property_id,added_date
                    parts = line.split('|')
                    if len(parts) == 3:
                        try:
                            favorite_dict = {
                                'favorite_id': int(parts[0]),
                                'property_id': int(parts[1]),
                                'added_date': parts[2]
                            }
                            favorites.append(favorite_dict)
                        except ValueError:
                            continue
    return favorites

def parse_agents():
    agents = []
    if os.path.exists(AGENT_FILE):
        with open(AGENT_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    # agent_id,agent_name,specialization,email,phone,properties_sold
                    parts = line.split('|')
                    if len(parts) == 6:
                        try:
                            agent_dict = {
                                'agent_id': int(parts[0]),
                                'agent_name': parts[1],
                                'specialization': parts[2],
                                'email': parts[3],
                                'phone': parts[4],
                                'properties_sold': int(parts[5])
                            }
                            agents.append(agent_dict)
                        except ValueError:
                            continue
    return agents

# Helper Functions

def save_inquiries(inquiries):
    try:
        with open(INQUIRY_FILE, 'w', encoding='utf-8') as f:
            for inquiry in inquiries:
                line = f"{inquiry['inquiry_id']}|{inquiry['property_id']}|{inquiry['customer_name']}|{inquiry['customer_email']}|{inquiry['customer_phone']}|{inquiry['message']}|{inquiry['inquiry_date']}|{inquiry['status']}\n"
                f.write(line)
        return True
    except Exception:
        return False


def save_favorites(favorites):
    try:
        with open(FAVORITES_FILE, 'w', encoding='utf-8') as f:
            for favorite in favorites:
                line = f"{favorite['favorite_id']}|{favorite['property_id']}|{favorite['added_date']}\n"
                f.write(line)
        return True
    except Exception:
        return False

# Route Implementations

# Dashboard: Featured properties and recent listings
@app.route('/')
@app.route('/dashboard')
def dashboard():
    properties = parse_properties()
    # Let's define featured properties as those with status 'featured' or just take top 5 most recent (assuming sorting by property_id desc)
    featured = [prop for prop in properties if prop['status'].lower() == 'featured']
    featured = sorted(featured, key=lambda x: x['property_id'], reverse=True)[:5]
    recent = sorted(properties, key=lambda x: x['property_id'], reverse=True)[:5]
    return render_template('dashboard.html', featured_properties=featured, recent_listings=recent)

# Property Search with filters
@app.route('/properties')
def property_search():
    properties = parse_properties()
    locations = {loc['location_name'] for loc in parse_locations()}

    # Query parameters
    location = request.args.get('location')
    price_min = request.args.get('price_min', type=float)
    price_max = request.args.get('price_max', type=float)
    property_type = request.args.get('property_type')

    filtered = []
    for prop in properties:
        if location and prop['location'].lower() != location.lower():
            continue
        if price_min is not None and prop['price'] < price_min:
            continue
        if price_max is not None and prop['price'] > price_max:
            continue
        if property_type and prop['property_type'].lower() != property_type.lower():
            continue
        filtered.append(prop)
    return render_template('property_search.html', properties=filtered, locations=locations)

# Property details with agent info
@app.route('/property/<int:property_id>')
def property_details(property_id):
    properties = parse_properties()
    agents = parse_agents()
    property_info = next((p for p in properties if p['property_id'] == property_id), None)
    if not property_info:
        return "Property not found.", 404
    agent_info = next((a for a in agents if a['agent_id'] == property_info['agent_id']), None)
    return render_template('property_details.html', property=property_info, agent=agent_info)

# Property inquiry GET shows form, POST submits inquiry
@app.route('/inquiry', methods=['GET', 'POST'])
def property_inquiry():
    if request.method == 'GET':
        return render_template('property_inquiry.html')
    else:
        # POST expect property_id, customer_name, customer_email, customer_phone, message
        try:
            property_id = int(request.form.get('property_id', ''))
            customer_name = request.form.get('customer_name', '').strip()
            customer_email = request.form.get('customer_email', '').strip()
            customer_phone = request.form.get('customer_phone', '').strip()
            message = request.form.get('message', '').strip()

            if not (property_id and customer_name and customer_email and customer_phone and message):
                return render_template('property_inquiry.html', error='All fields are required.')

            inquiries = parse_inquiries()
            new_id = (max([inq['inquiry_id'] for inq in inquiries]) + 1) if inquiries else 1
            inquiry_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            status = 'New'
            new_inquiry = {
                'inquiry_id': new_id,
                'property_id': property_id,
                'customer_name': customer_name,
                'customer_email': customer_email,
                'customer_phone': customer_phone,
                'message': message,
                'inquiry_date': inquiry_date,
                'status': status
            }
            inquiries.append(new_inquiry)
            success = save_inquiries(inquiries)
            if success:
                return render_template('property_inquiry.html', success='Inquiry submitted successfully.')
            else:
                return render_template('property_inquiry.html', error='Failed to save inquiry.')

        except ValueError:
            return render_template('property_inquiry.html', error='Invalid input data.')

# My Inquiries Page with optional status filter and deletion (POST)
@app.route('/inquiries', methods=['GET', 'POST'])
def my_inquiries():
    if request.method == 'GET':
        status_filter = request.args.get('status')
        inquiries = parse_inquiries()
        # Optionally filter by status
        if status_filter:
            inquiries = [inq for inq in inquiries if inq['status'].lower() == status_filter.lower()]
        properties = {p['property_id']: p for p in parse_properties()}
        return render_template('my_inquiries.html', inquiries=inquiries, properties=properties)
    else:
        # POST is used for deletion
        # Expect inquiry_id
        inquiry_id = request.form.get('inquiry_id')
        if not inquiry_id:
            return jsonify({'success': False, 'message': 'inquiry_id required'})
        try:
            inquiry_id = int(inquiry_id)
        except ValueError:
            return jsonify({'success': False, 'message': 'Invalid inquiry_id'})

        inquiries = parse_inquiries()
        inquiries = [inq for inq in inquiries if inq['inquiry_id'] != inquiry_id]
        success = save_inquiries(inquiries)
        if success:
            return jsonify({'success': True, 'message': 'Inquiry deleted'})
        else:
            return jsonify({'success': False, 'message': 'Failed to save data'})

# My Favorites Page joins favorites with property details
@app.route('/favorites')
def my_favorites():
    favorites = parse_favorites()
    properties = {p['property_id']: p for p in parse_properties()}

    favorites_full = []
    for fav in favorites:
        prop = properties.get(fav['property_id'])
        if prop:
            favorites_full.append({**fav, 'property': prop})

    return render_template('my_favorites.html', favorites=favorites_full)

# Add to favorites (POST)
@app.route('/favorites/add', methods=['POST'])
def add_favorite():
    property_id = request.form.get('property_id')
    if not property_id:
        return jsonify({'success': False, 'message': 'property_id required'})
    try:
        property_id = int(property_id)
    except ValueError:
        return jsonify({'success': False, 'message': 'Invalid property_id'})

    favorites = parse_favorites()
    # Avoid duplicates
    if any(fav['property_id'] == property_id for fav in favorites):
        return jsonify({'success': False, 'message': 'Property already in favorites'})

    # Check property exists
    properties = parse_properties()
    if not any(p['property_id'] == property_id for p in properties):
        return jsonify({'success': False, 'message': 'Property not found'})

    new_id = (max([fav['favorite_id'] for fav in favorites]) + 1) if favorites else 1
    added_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    new_fav = {
        'favorite_id': new_id,
        'property_id': property_id,
        'added_date': added_date
    }
    favorites.append(new_fav)
    success = save_favorites(favorites)
    if success:
        return jsonify({'success': True, 'message': 'Added to favorites'})
    else:
        return jsonify({'success': False, 'message': 'Failed to save favorites'})

# Remove from favorites (POST)
@app.route('/favorites/remove', methods=['POST'])
def remove_favorite():
    property_id = request.form.get('property_id')
    if not property_id:
        return jsonify({'success': False, 'message': 'property_id required'})
    try:
        property_id = int(property_id)
    except ValueError:
        return jsonify({'success': False, 'message': 'Invalid property_id'})

    favorites = parse_favorites()
    new_favorites = [fav for fav in favorites if fav['property_id'] != property_id]
    if len(new_favorites) == len(favorites):
        return jsonify({'success': False, 'message': 'Property not in favorites'})

    success = save_favorites(new_favorites)
    if success:
        return jsonify({'success': True, 'message': 'Removed from favorites'})
    else:
        return jsonify({'success': False, 'message': 'Failed to save favorites'})

# Agent directory with optional search
@app.route('/agents')
def agent_directory():
    agents = parse_agents()
    search = request.args.get('search')
    if search:
        search_lower = search.lower()
        agents = [a for a in agents if search_lower in a['agent_name'].lower()]
    return render_template('agent_directory.html', agents=agents)

# Locations page with optional sorting
@app.route('/locations')
def locations_page():
    locations = parse_locations()
    sort = request.args.get('sort')
    if sort == 'name':
        locations.sort(key=lambda x: x['location_name'].lower())
    elif sort == 'property_count':
        locations.sort(key=lambda x: x['property_count'], reverse=True)
    elif sort == 'average_price':
        locations.sort(key=lambda x: x['average_price'], reverse=True)
    return render_template('locations.html', locations=locations)

# View properties filtered by location id
@app.route('/locations/<int:location_id>/properties')
def properties_by_location(location_id):
    properties = parse_properties()
    locations = parse_locations()

    location = next((loc for loc in locations if loc['location_id'] == location_id), None)
    if not location:
        return "Location not found.", 404

    filtered_properties = [p for p in properties if p['location'].lower() == location['location_name'].lower()]
    return render_template('property_search.html', properties=filtered_properties, locations={loc['location_name'] for loc in locations}, active_location=location)

if __name__ == '__main__':
    app.run(debug=True)
