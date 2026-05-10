'''
Main backend Python application for the RealEstate web application.
Handles routing, data reading/writing from/to local text files in the data/ directory,
and serves the HTML templates for all eight pages.
'''
from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime
app = Flask(__name__)
DATA_DIR = 'data'
# Utility functions to read and write data files
def read_properties():
    properties = []
    path = os.path.join(DATA_DIR, 'properties.txt')
    if not os.path.exists(path):
        return properties
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 11:
                continue
            property_id, address, location, price, property_type, bedrooms, bathrooms, square_feet, description, agent_id, status = parts
            properties.append({
                'property_id': property_id,
                'address': address,
                'location': location,
                'price': int(price),
                'property_type': property_type,
                'bedrooms': float(bedrooms),
                'bathrooms': float(bathrooms),
                'square_feet': int(square_feet),
                'description': description,
                'agent_id': agent_id,
                'status': status
            })
    return properties
def write_properties(properties):
    path = os.path.join(DATA_DIR, 'properties.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for p in properties:
            line = '|'.join([
                str(p['property_id']),
                p['address'],
                p['location'],
                str(p['price']),
                p['property_type'],
                str(p['bedrooms']),
                str(p['bathrooms']),
                str(p['square_feet']),
                p['description'],
                p['agent_id'],
                p['status']
            ])
            f.write(line + '\n')
def read_locations():
    locations = []
    path = os.path.join(DATA_DIR, 'locations.txt')
    if not os.path.exists(path):
        return locations
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 6:
                continue
            location_id, location_name, region, average_price, property_count, description = parts
            locations.append({
                'location_id': location_id,
                'location_name': location_name,
                'region': region,
                'average_price': int(average_price),
                'property_count': int(property_count),
                'description': description
            })
    return locations
def write_locations(locations):
    path = os.path.join(DATA_DIR, 'locations.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for loc in locations:
            line = '|'.join([
                str(loc['location_id']),
                loc['location_name'],
                loc['region'],
                str(loc['average_price']),
                str(loc['property_count']),
                loc['description']
            ])
            f.write(line + '\n')
def read_inquiries():
    inquiries = []
    path = os.path.join(DATA_DIR, 'inquiries.txt')
    if not os.path.exists(path):
        return inquiries
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 8:
                continue
            inquiry_id, property_id, customer_name, customer_email, customer_phone, message, inquiry_date, status = parts
            inquiries.append({
                'inquiry_id': inquiry_id,
                'property_id': property_id,
                'customer_name': customer_name,
                'customer_email': customer_email,
                'customer_phone': customer_phone,
                'message': message,
                'inquiry_date': inquiry_date,
                'status': status
            })
    return inquiries
def write_inquiries(inquiries):
    path = os.path.join(DATA_DIR, 'inquiries.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for inq in inquiries:
            line = '|'.join([
                str(inq['inquiry_id']),
                inq['property_id'],
                inq['customer_name'],
                inq['customer_email'],
                inq['customer_phone'],
                inq['message'],
                inq['inquiry_date'],
                inq['status']
            ])
            f.write(line + '\n')
def read_favorites():
    favorites = []
    path = os.path.join(DATA_DIR, 'favorites.txt')
    if not os.path.exists(path):
        return favorites
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 3:
                continue
            favorite_id, property_id, added_date = parts
            favorites.append({
                'favorite_id': favorite_id,
                'property_id': property_id,
                'added_date': added_date
            })
    return favorites
def write_favorites(favorites):
    path = os.path.join(DATA_DIR, 'favorites.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for fav in favorites:
            line = '|'.join([
                str(fav['favorite_id']),
                fav['property_id'],
                fav['added_date']
            ])
            f.write(line + '\n')
def read_agents():
    agents = []
    path = os.path.join(DATA_DIR, 'agents.txt')
    if not os.path.exists(path):
        return agents
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 6:
                continue
            agent_id, agent_name, specialization, email, phone, properties_sold = parts
            agents.append({
                'agent_id': agent_id,
                'agent_name': agent_name,
                'specialization': specialization,
                'email': email,
                'phone': phone,
                'properties_sold': int(properties_sold)
            })
    return agents
def write_agents(agents):
    path = os.path.join(DATA_DIR, 'agents.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for ag in agents:
            line = '|'.join([
                str(ag['agent_id']),
                ag['agent_name'],
                ag['specialization'],
                ag['email'],
                ag['phone'],
                str(ag['properties_sold'])
            ])
            f.write(line + '\n')
# Helper to get next ID for inquiries and favorites
def get_next_id(items, id_key):
    max_id = 0
    for item in items:
        try:
            val = int(item[id_key])
            if val > max_id:
                max_id = val
        except:
            continue
    return max_id + 1
# ROUTES
@app.route('/')
def dashboard():
    # Dashboard page: featured properties, recent listings, quick navigation
    properties = read_properties()
    # Featured properties: pick first 3 available properties sorted by price descending
    featured = [p for p in properties if p['status'].lower() == 'available']
    featured.sort(key=lambda x: x['price'], reverse=True)
    featured = featured[:3]
    # Recent listings: last 5 properties by property_id descending (assuming higher id = newer)
    recent = sorted(properties, key=lambda x: int(x['property_id']), reverse=True)[:5]
    return render_template('dashboard.html',
                           featured_properties=featured,
                           recent_listings=recent)
@app.route('/property_search', methods=['GET', 'POST'])
def property_search():
    properties = read_properties()
    locations = set(p['location'] for p in properties)
    property_types = ['House', 'Apartment', 'Condo', 'Land']
    # Filters from query parameters or form
    location_filter = request.args.get('location', '').strip()
    price_min = request.args.get('price_min', '')
    price_max = request.args.get('price_max', '')
    property_type_filter = request.args.get('property_type', '')
    # Convert price filters to int if possible
    try:
        price_min_val = int(price_min) if price_min else None
    except:
        price_min_val = None
    try:
        price_max_val = int(price_max) if price_max else None
    except:
        price_max_val = None
    filtered_properties = []
    for p in properties:
        if p['status'].lower() != 'available':
            continue
        if location_filter and location_filter.lower() not in p['location'].lower():
            continue
        if property_type_filter and property_type_filter != 'All' and p['property_type'] != property_type_filter:
            continue
        if price_min_val is not None and p['price'] < price_min_val:
            continue
        if price_max_val is not None and p['price'] > price_max_val:
            continue
        filtered_properties.append(p)
    return render_template('property_search.html',
                           properties=filtered_properties,
                           location_input=location_filter,
                           price_range_min=price_min,
                           price_range_max=price_max,
                           property_type_filter=property_type_filter,
                           property_types=property_types)
@app.route('/property_details/<property_id>')
def property_details(property_id):
    properties = read_properties()
    agents = read_agents()
    property_obj = None
    for p in properties:
        if p['property_id'] == property_id:
            property_obj = p
            break
    if not property_obj:
        return "Property not found", 404
    # Find agent info
    agent = None
    for a in agents:
        if a['agent_id'] == property_obj['agent_id']:
            agent = a
            break
    # Check if property is in favorites
    favorites = read_favorites()
    is_favorite = any(fav['property_id'] == property_id for fav in favorites)
    return render_template('property_details.html',
                           property=property_obj,
                           agent=agent,
                           is_favorite=is_favorite)
@app.route('/property_inquiry', methods=['GET', 'POST'])
def property_inquiry():
    properties = read_properties()
    if request.method == 'POST':
        # Process inquiry submission
        property_id = request.form.get('select-property', '').strip()
        customer_name = request.form.get('inquiry-name', '').strip()
        customer_email = request.form.get('inquiry-email', '').strip()
        customer_phone = request.form.get('inquiry-phone', '').strip()
        message = request.form.get('inquiry-message', '').strip()
        if not property_id or not customer_name or not customer_email or not message:
            error = "Please fill in all required fields."
            return render_template('property_inquiry.html', properties=properties, error=error,
                                   form_data=request.form)
        inquiries = read_inquiries()
        new_id = get_next_id(inquiries, 'inquiry_id')
        inquiry_date = datetime.now().strftime('%Y-%m-%d')
        new_inquiry = {
            'inquiry_id': str(new_id),
            'property_id': property_id,
            'customer_name': customer_name,
            'customer_email': customer_email,
            'customer_phone': customer_phone,
            'message': message,
            'inquiry_date': inquiry_date,
            'status': 'Pending'
        }
        inquiries.append(new_inquiry)
        write_inquiries(inquiries)
        return redirect(url_for('my_inquiries'))
    # GET request
    return render_template('property_inquiry.html', properties=properties)
@app.route('/my_inquiries', methods=['GET', 'POST'])
def my_inquiries():
    inquiries = read_inquiries()
    properties = {p['property_id']: p for p in read_properties()}
    # Filter by status
    status_filter = request.args.get('status', 'All')
    filtered_inquiries = []
    for inq in inquiries:
        if status_filter != 'All' and inq['status'] != status_filter:
            continue
        filtered_inquiries.append(inq)
    # Handle deletion of inquiry if POST with delete inquiry id
    if request.method == 'POST':
        delete_id = request.form.get('delete_inquiry_id')
        if delete_id:
            inquiries = [inq for inq in inquiries if inq['inquiry_id'] != delete_id]
            write_inquiries(inquiries)
            return redirect(url_for('my_inquiries', status=status_filter))
    return render_template('my_inquiries.html',
                           inquiries=filtered_inquiries,
                           properties=properties,
                           inquiry_status_filter=status_filter)
@app.route('/my_favorites', methods=['GET', 'POST'])
def my_favorites():
    favorites = read_favorites()
    properties = {p['property_id']: p for p in read_properties()}
    # Handle removal of favorite property
    if request.method == 'POST':
        remove_property_id = request.form.get('remove_property_id')
        if remove_property_id:
            favorites = [fav for fav in favorites if fav['property_id'] != remove_property_id]
            write_favorites(favorites)
            return redirect(url_for('my_favorites'))
    # Build list of favorite properties with details
    favorite_properties = []
    for fav in favorites:
        prop = properties.get(fav['property_id'])
        if prop:
            favorite_properties.append(prop)
    return render_template('my_favorites.html',
                           favorites_list=favorite_properties)
@app.route('/add_to_favorites/<property_id>', methods=['POST'])
def add_to_favorites(property_id):
    favorites = read_favorites()
    # Check if already in favorites
    if any(fav['property_id'] == property_id for fav in favorites):
        # Already favorite, redirect back to property details
        return redirect(url_for('property_details', property_id=property_id))
    new_id = get_next_id(favorites, 'favorite_id')
    added_date = datetime.now().strftime('%Y-%m-%d')
    favorites.append({
        'favorite_id': str(new_id),
        'property_id': property_id,
        'added_date': added_date
    })
    write_favorites(favorites)
    return redirect(url_for('property_details', property_id=property_id))
@app.route('/agents', methods=['GET'])
def agents():
    agents = read_agents()
    search_name = request.args.get('search_name', '').strip().lower()
    if search_name:
        filtered_agents = [a for a in agents if search_name in a['agent_name'].lower()]
    else:
        filtered_agents = agents
    return render_template('agents.html',
                           agents_list=filtered_agents,
                           agent_search=search_name)
@app.route('/locations', methods=['GET'])
def locations():
    locations = read_locations()
    sort_by = request.args.get('sort_by', 'By Name')
    if sort_by == 'By Name':
        locations.sort(key=lambda x: x['location_name'].lower())
    elif sort_by == 'By Properties Count':
        locations.sort(key=lambda x: x['property_count'], reverse=True)
    elif sort_by == 'By Average Price':
        locations.sort(key=lambda x: x['average_price'], reverse=True)
    return render_template('locations.html',
                           locations_list=locations,
                           location_sort=sort_by)
@app.route('/view_location/<location_id>')
def view_location(location_id):
    # Fix: Map location_id to location_name, then filter properties by location_name
    locations = read_locations()
    location_name = None
    for loc in locations:
        if loc['location_id'] == location_id:
            location_name = loc['location_name']
            break
    if not location_name:
        return "Location not found", 404
    properties = read_properties()
    filtered_properties = [p for p in properties if p['location'] == location_name and p['status'].lower() == 'available']
    property_types = ['House', 'Apartment', 'Condo', 'Land']
    return render_template('property_search.html',
                           properties=filtered_properties,
                           location_input=location_name,
                           price_range_min='',
                           price_range_max='',
                           property_type_filter='',
                           property_types=property_types)
# Back to dashboard route for buttons
@app.route('/back_to_dashboard')
def back_to_dashboard():
    return redirect(url_for('dashboard'))
if __name__ == '__main__':
    app.run(port=5000, debug=True)