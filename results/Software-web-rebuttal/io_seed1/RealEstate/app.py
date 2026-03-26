'''
Main backend Python application for the RealEstate web application.
Handles routing, data reading/writing from/to local text files in the data/ directory,
and business logic for all eight pages:
Dashboard, Property Search, Property Details, Property Inquiry, My Inquiries,
My Favorites, Agent Directory, and Locations.
Uses Flask framework and Jinja2 templating engine.
'''
from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime
app = Flask(__name__)
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
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
# Helper functions
def get_property_by_id(property_id):
    properties = read_properties()
    for p in properties:
        if p['property_id'] == str(property_id):
            return p
    return None
def get_agent_by_id(agent_id):
    agents = read_agents()
    for a in agents:
        if a['agent_id'] == str(agent_id):
            return a
    return None
def get_location_by_id(location_id):
    locations = read_locations()
    for loc in locations:
        if loc['location_id'] == str(location_id):
            return loc
    return None
def get_next_id(items, id_key):
    max_id = 0
    for item in items:
        try:
            cur_id = int(item[id_key])
            if cur_id > max_id:
                max_id = cur_id
        except:
            continue
    return max_id + 1
# Routes
@app.route('/')
def dashboard():
    properties = read_properties()
    # Featured properties: pick first 3 available properties sorted by price descending
    featured = [p for p in properties if p['status'].lower() == 'available']
    featured = sorted(featured, key=lambda x: x['price'], reverse=True)[:3]
    # Recent listings: last 5 properties by property_id descending (assuming higher id = newer)
    recent = sorted(properties, key=lambda x: int(x['property_id']), reverse=True)[:5]
    return render_template('dashboard.html',
                           featured_properties=featured,
                           recent_listings=recent)
@app.route('/property_search', methods=['GET', 'POST'])
def property_search():
    properties = read_properties()
    locations = set(p['location'] for p in properties)
    filtered_properties = properties
    # Filters
    location_filter = request.args.get('location', '').strip()
    price_min = request.args.get('price_min', '').strip()
    price_max = request.args.get('price_max', '').strip()
    property_type_filter = request.args.get('property_type', '').strip()
    # Apply filters
    if location_filter:
        filtered_properties = [p for p in filtered_properties if p['location'].lower() == location_filter.lower()]
    if price_min:
        try:
            min_val = int(price_min)
            filtered_properties = [p for p in filtered_properties if p['price'] >= min_val]
        except:
            pass
    if price_max:
        try:
            max_val = int(price_max)
            filtered_properties = [p for p in filtered_properties if p['price'] <= max_val]
        except:
            pass
    if property_type_filter and property_type_filter.lower() != 'all':
        filtered_properties = [p for p in filtered_properties if p['property_type'].lower() == property_type_filter.lower()]
    # Only show available properties
    filtered_properties = [p for p in filtered_properties if p['status'].lower() == 'available']
    return render_template('property_search.html',
                           properties=filtered_properties,
                           location_input=location_filter,
                           price_range_min=price_min,
                           price_range_max=price_max,
                           property_type_filter=property_type_filter,
                           property_types=['House', 'Apartment', 'Condo', 'Land'])
@app.route('/property_details/<property_id>')
def property_details(property_id):
    property_obj = get_property_by_id(property_id)
    if not property_obj:
        return "Property not found", 404
    agent = get_agent_by_id(property_obj['agent_id'])
    return render_template('property_details.html',
                           property=property_obj,
                           agent=agent)
@app.route('/property_inquiry', methods=['GET', 'POST'])
def property_inquiry():
    properties = read_properties()
    if request.method == 'POST':
        property_id = request.form.get('select-property')
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
    return render_template('property_inquiry.html', properties=properties)
@app.route('/my_inquiries', methods=['GET', 'POST'])
def my_inquiries():
    inquiries = read_inquiries()
    properties = {p['property_id']: p for p in read_properties()}
    status_filter = request.args.get('status', 'All')
    if status_filter and status_filter != 'All':
        inquiries = [i for i in inquiries if i['status'].lower() == status_filter.lower()]
    if request.method == 'POST':
        # Handle deletion of inquiry
        delete_id = request.form.get('delete_inquiry_id')
        if delete_id:
            inquiries = [i for i in inquiries if i['inquiry_id'] != delete_id]
            write_inquiries(inquiries)
            return redirect(url_for('my_inquiries', status=status_filter))
    return render_template('my_inquiries.html',
                           inquiries=inquiries,
                           properties=properties,
                           inquiry_status_filter=status_filter,
                           status_options=['All', 'Pending', 'Contacted', 'Resolved'])
@app.route('/my_favorites', methods=['GET', 'POST'])
def my_favorites():
    favorites = read_favorites()
    properties = {p['property_id']: p for p in read_properties()}
    if request.method == 'POST':
        remove_property_id = request.form.get('remove_property_id')
        if remove_property_id:
            favorites = [f for f in favorites if f['property_id'] != remove_property_id]
            write_favorites(favorites)
            return redirect(url_for('my_favorites'))
    # Sort favorites by added_date descending
    favorites_sorted = sorted(favorites, key=lambda x: x['added_date'], reverse=True)
    # Build list of favorite properties with details
    favorite_properties = []
    for fav in favorites_sorted:
        prop = properties.get(fav['property_id'])
        if prop:
            favorite_properties.append({
                'favorite_id': fav['favorite_id'],
                'property': prop,
                'added_date': fav['added_date']
            })
    return render_template('my_favorites.html',
                           favorites_list=favorite_properties)
@app.route('/add_to_favorites/<property_id>', methods=['POST'])
def add_to_favorites(property_id):
    favorites = read_favorites()
    # Check if already in favorites
    for fav in favorites:
        if fav['property_id'] == property_id:
            # Already in favorites, redirect back to property details
            return redirect(url_for('property_details', property_id=property_id))
    new_id = get_next_id(favorites, 'favorite_id')
    added_date = datetime.now().strftime('%Y-%m-%d')
    favorites.append({
        'favorite_id': str(new_id),
        'property_id': property_id,
        'added_date': added_date
    })
    write_favorites(favorites)
    return redirect(url_for('my_favorites'))
@app.route('/agent_directory')
def agent_directory():
    agents = read_agents()
    search_name = request.args.get('search_name', '').strip().lower()
    if search_name:
        agents = [a for a in agents if search_name in a['agent_name'].lower()]
    return render_template('agent_directory.html',
                           agents=agents,
                           search_name=search_name)
@app.route('/locations')
def locations():
    locations = read_locations()
    sort_by = request.args.get('sort_by', 'By Name')
    if sort_by == 'By Name':
        locations = sorted(locations, key=lambda x: x['location_name'].lower())
    elif sort_by == 'By Properties Count':
        locations = sorted(locations, key=lambda x: x['property_count'], reverse=True)
    elif sort_by == 'By Average Price':
        locations = sorted(locations, key=lambda x: x['average_price'], reverse=True)
    return render_template('locations.html',
                           locations=locations,
                           location_sort=sort_by)
@app.route('/view_location/<location_id>')
def view_location(location_id):
    # Show properties in the selected location
    location = get_location_by_id(location_id)
    if not location:
        return "Location not found", 404
    properties = read_properties()
    filtered_properties = [p for p in properties if p['location'].lower() == location['location_name'].lower() and p['status'].lower() == 'available']
    return render_template('property_search.html',
                           properties=filtered_properties,
                           location_input=location['location_name'],
                           price_range_min='',
                           price_range_max='',
                           property_type_filter='',
                           property_types=['House', 'Apartment', 'Condo', 'Land'])
# Run the app
if __name__ == '__main__':
    app.run(port=5000, debug=True)