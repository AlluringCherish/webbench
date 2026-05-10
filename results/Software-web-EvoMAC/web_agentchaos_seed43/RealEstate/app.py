'''
Main backend application for the RealEstate web application.
Handles routing, data reading/writing from/to local text files in the data/ directory,
and serves HTML templates for all pages.
Implements all required features including:
- Dashboard with featured properties and navigation
- Property Search with filters
- Property Details with add to favorites and submit inquiry
- Property Inquiry form submission
- My Inquiries listing with status filtering and deletion
- My Favorites listing with removal and view details
- Agent Directory with search and contact buttons
- Locations page with sorting and view properties by location
No authentication required; all features directly accessible.
'''
from flask import Flask, render_template, request, redirect, url_for, flash
import os
from datetime import datetime
app = Flask(__name__)
app.secret_key = 'realestate_secret_key'  # Needed for flash messages
DATA_DIR = 'data'
# Utility functions for reading and writing data files
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
                'bedrooms': float(bedrooms) if '.' in bedrooms else int(bedrooms),
                'bathrooms': float(bathrooms) if '.' in bathrooms else int(bathrooms),
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
        for i in inquiries:
            line = '|'.join([
                str(i['inquiry_id']),
                i['property_id'],
                i['customer_name'],
                i['customer_email'],
                i['customer_phone'],
                i['message'],
                i['inquiry_date'],
                i['status']
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
        for a in agents:
            line = '|'.join([
                str(a['agent_id']),
                a['agent_name'],
                a['specialization'],
                a['email'],
                a['phone'],
                str(a['properties_sold'])
            ])
            f.write(line + '\n')
# Helper to get next ID for a given list of dicts and id key
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
    properties = read_properties()
    # Featured properties: show up to 5 available properties sorted by price descending (as example)
    featured = [p for p in properties if p['status'].lower() == 'available']
    featured.sort(key=lambda x: x['price'], reverse=True)
    featured = featured[:5]
    # Recent listings: show up to 5 most recently added properties by property_id descending (assuming higher id = newer)
    recent = sorted(properties, key=lambda x: int(x['property_id']), reverse=True)[:5]
    return render_template('dashboard.html',
                           featured_properties=featured,
                           recent_listings=recent)
@app.route('/property_search', methods=['GET', 'POST'])
def property_search():
    properties = read_properties()
    locations = sorted(set(p['location'] for p in properties))
    property_types = ['House', 'Apartment', 'Condo', 'Land']
    # Filters from query parameters or form
    location_filter = request.args.get('location', '').strip()
    price_min = request.args.get('price_min', '')
    price_max = request.args.get('price_max', '')
    property_type_filter = request.args.get('property_type', '')
    # Validate and convert price filters
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
        if location_filter and p['location'].lower() != location_filter.lower():
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
                           locations=locations,
                           property_types=property_types,
                           selected_location=location_filter,
                           price_min=price_min,
                           price_max=price_max,
                           selected_property_type=property_type_filter)
@app.route('/property_details/<property_id>', methods=['GET'])
def property_details(property_id):
    properties = read_properties()
    property_obj = next((p for p in properties if p['property_id'] == property_id), None)
    if not property_obj:
        flash('Property not found.', 'error')
        return redirect(url_for('dashboard'))
    # Check if property is in favorites
    favorites = read_favorites()
    is_favorite = any(fav['property_id'] == property_id for fav in favorites)
    return render_template('property_details.html',
                           property=property_obj,
                           is_favorite=is_favorite)
@app.route('/add_to_favorites/<property_id>', methods=['POST'])
def add_to_favorites(property_id):
    properties = read_properties()
    if not any(p['property_id'] == property_id for p in properties):
        flash('Property not found.', 'error')
        return redirect(url_for('dashboard'))
    favorites = read_favorites()
    if any(fav['property_id'] == property_id for fav in favorites):
        flash('Property already in favorites.', 'info')
        return redirect(url_for('property_details', property_id=property_id))
    new_id = get_next_id(favorites, 'favorite_id')
    added_date = datetime.now().strftime('%Y-%m-%d')
    favorites.append({
        'favorite_id': str(new_id),
        'property_id': property_id,
        'added_date': added_date
    })
    write_favorites(favorites)
    flash('Property added to favorites.', 'success')
    return redirect(url_for('property_details', property_id=property_id))
@app.route('/property_inquiry', methods=['GET', 'POST'])
def property_inquiry():
    properties = read_properties()
    if request.method == 'POST':
        property_id = request.form.get('select_property', '').strip()
        customer_name = request.form.get('inquiry_name', '').strip()
        customer_email = request.form.get('inquiry_email', '').strip()
        customer_phone = request.form.get('inquiry_phone', '').strip()
        message = request.form.get('inquiry_message', '').strip()
        # Validate required fields
        if not property_id or not customer_name or not customer_email or not message:
            flash('Please fill in all required fields.', 'error')
            return redirect(url_for('property_inquiry'))
        # Check property exists
        if not any(p['property_id'] == property_id for p in properties):
            flash('Selected property does not exist.', 'error')
            return redirect(url_for('property_inquiry'))
        inquiries = read_inquiries()
        new_id = get_next_id(inquiries, 'inquiry_id')
        inquiry_date = datetime.now().strftime('%Y-%m-%d')
        inquiries.append({
            'inquiry_id': str(new_id),
            'property_id': property_id,
            'customer_name': customer_name,
            'customer_email': customer_email,
            'customer_phone': customer_phone,
            'message': message,
            'inquiry_date': inquiry_date,
            'status': 'Pending'
        })
        write_inquiries(inquiries)
        flash('Inquiry submitted successfully.', 'success')
        return redirect(url_for('my_inquiries'))
    # GET request
    available_properties = [p for p in properties if p['status'].lower() == 'available']
    return render_template('property_inquiry.html', properties=available_properties)
@app.route('/my_inquiries', methods=['GET', 'POST'])
def my_inquiries():
    inquiries = read_inquiries()
    properties = {p['property_id']: p for p in read_properties()}
    # Filter by status
    status_filter = request.args.get('status', 'All')
    if status_filter != 'All':
        inquiries = [inq for inq in inquiries if inq['status'].lower() == status_filter.lower()]
    return render_template('my_inquiries.html',
                           inquiries=inquiries,
                           properties=properties,
                           selected_status=status_filter)
@app.route('/delete_inquiry/<inquiry_id>', methods=['POST'])
def delete_inquiry(inquiry_id):
    inquiries = read_inquiries()
    new_inquiries = [inq for inq in inquiries if inq['inquiry_id'] != inquiry_id]
    if len(new_inquiries) == len(inquiries):
        flash('Inquiry not found.', 'error')
    else:
        write_inquiries(new_inquiries)
        flash('Inquiry deleted successfully.', 'success')
    return redirect(url_for('my_inquiries'))
@app.route('/my_favorites', methods=['GET'])
def my_favorites():
    favorites = read_favorites()
    properties = {p['property_id']: p for p in read_properties()}
    # Build list of favorite properties with details
    favorite_properties = []
    for fav in favorites:
        prop = properties.get(fav['property_id'])
        if prop:
            favorite_properties.append({
                'favorite_id': fav['favorite_id'],
                'property': prop,
                'added_date': fav['added_date']
            })
    return render_template('my_favorites.html', favorites=favorite_properties)
@app.route('/remove_favorite/<property_id>', methods=['POST'])
def remove_favorite(property_id):
    favorites = read_favorites()
    new_favorites = [fav for fav in favorites if fav['property_id'] != property_id]
    if len(new_favorites) == len(favorites):
        flash('Favorite property not found.', 'error')
    else:
        write_favorites(new_favorites)
        flash('Property removed from favorites.', 'success')
    return redirect(url_for('my_favorites'))
@app.route('/agents', methods=['GET'])
def agents():
    agents = read_agents()
    search_query = request.args.get('search', '').strip().lower()
    if search_query:
        agents = [a for a in agents if search_query in a['agent_name'].lower()]
    # Pass contact agent base url for JS usage
    contact_agent_base_url = url_for('agents')  # Not used for navigation but for alert, so no URL needed
    return render_template('agents.html', agents=agents, search_query=search_query)
@app.route('/locations', methods=['GET'])
def locations():
    locations = read_locations()
    sort_by = request.args.get('sort', 'By Name')
    if sort_by == 'By Name':
        locations.sort(key=lambda x: x['location_name'].lower())
    elif sort_by == 'By Properties Count':
        locations.sort(key=lambda x: x['property_count'], reverse=True)
    elif sort_by == 'By Average Price':
        locations.sort(key=lambda x: x['average_price'], reverse=True)
    # Pass view_location base url for JS usage
    view_location_base_url = url_for('view_location', location_id='')
    return render_template('locations.html', locations=locations, selected_sort=sort_by, view_location_base_url=view_location_base_url)
@app.route('/view_location/<location_id>', methods=['GET'])
def view_location(location_id):
    locations = read_locations()
    location_obj = next((loc for loc in locations if loc['location_id'] == location_id), None)
    if not location_obj:
        flash('Location not found.', 'error')
        return redirect(url_for('locations'))
    properties = read_properties()
    # Filter properties by location and available status
    filtered_properties = [p for p in properties if p['location'].lower() == location_obj['location_name'].lower() and p['status'].lower() == 'available']
    return render_template('property_search.html',
                           properties=filtered_properties,
                           locations=[location_obj['location_name']],
                           property_types=['House', 'Apartment', 'Condo', 'Land'],
                           selected_location=location_obj['location_name'],
                           price_min='',
                           price_max='',
                           selected_property_type='')
# Run the app
if __name__ == '__main__':
    # Ensure data directory exists
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    app.run(host='0.0.0.0', port=5000, debug=True)