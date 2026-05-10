'''
Main backend application for the RealEstate web application.
Handles routing, data reading/writing from/to local text files in the data/ directory,
and business logic for browsing properties, searching, viewing details,
submitting inquiries, managing favorites, and displaying agents and locations.
No authentication is required; all features are directly accessible.
'''
from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime
app = Flask(__name__)
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
# Utility functions to read/write data files
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
                str(inq['property_id']),
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
                str(fav['property_id']),
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
# Helper to get next ID for inquiries and favorites
def get_next_id(items, id_key):
    if not items:
        return 1
    max_id = max(int(item[id_key]) for item in items)
    return max_id + 1
# ROUTES
@app.route('/')
def dashboard():
    properties = read_properties()
    # Featured properties: pick first 3 available properties sorted by price descending
    featured = [p for p in properties if p['status'].lower() == 'available']
    featured = sorted(featured, key=lambda x: x['price'], reverse=True)[:3]
    # Recent listings: last 3 properties by property_id descending (assuming higher id = newer)
    recent = sorted(properties, key=lambda x: int(x['property_id']), reverse=True)[:3]
    return render_template('dashboard.html',
                           featured_properties=featured,
                           recent_listings=recent)
@app.route('/property_search', methods=['GET', 'POST'])
def property_search():
    properties = read_properties()
    filtered_properties = properties
    # Get filters from query parameters or form
    location_filter = request.args.get('location', '').strip()
    price_min = request.args.get('price_min', '').strip()
    price_max = request.args.get('price_max', '').strip()
    property_type_filter = request.args.get('property_type', '').strip()
    # Filtering logic
    if location_filter:
        filtered_properties = [p for p in filtered_properties if location_filter.lower() in p['location'].lower()]
    if price_min.isdigit():
        filtered_properties = [p for p in filtered_properties if p['price'] >= int(price_min)]
    if price_max.isdigit():
        filtered_properties = [p for p in filtered_properties if p['price'] <= int(price_max)]
    if property_type_filter and property_type_filter.lower() != 'all':
        filtered_properties = [p for p in filtered_properties if p['property_type'].lower() == property_type_filter.lower()]
    # Only show available properties
    filtered_properties = [p for p in filtered_properties if p['status'].lower() == 'available']
    return render_template('property_search.html',
                           properties=filtered_properties,
                           location_filter=location_filter,
                           price_min=price_min,
                           price_max=price_max,
                           property_type_filter=property_type_filter)
@app.route('/property_details/<property_id>')
def property_details(property_id):
    properties = read_properties()
    property_item = next((p for p in properties if p['property_id'] == property_id), None)
    if not property_item:
        return "Property not found", 404
    favorites = read_favorites()
    is_favorite = any(fav['property_id'] == property_id for fav in favorites)
    return render_template('property_details.html',
                           property=property_item,
                           is_favorite=is_favorite)
@app.route('/add_to_favorites/<property_id>', methods=['POST'])
def add_to_favorites(property_id):
    favorites = read_favorites()
    # Check if already favorite
    if any(fav['property_id'] == property_id for fav in favorites):
        # Already favorite, redirect back
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
@app.route('/remove_from_favorites/<property_id>', methods=['POST'])
def remove_from_favorites(property_id):
    favorites = read_favorites()
    favorites = [fav for fav in favorites if fav['property_id'] != property_id]
    write_favorites(favorites)
    return redirect(url_for('my_favorites'))
@app.route('/property_inquiry', methods=['GET', 'POST'])
def property_inquiry():
    properties = read_properties()
    if request.method == 'POST':
        property_id = request.form.get('select-property', '').strip()
        customer_name = request.form.get('inquiry-name', '').strip()
        customer_email = request.form.get('inquiry-email', '').strip()
        customer_phone = request.form.get('inquiry-phone', '').strip()
        message = request.form.get('inquiry-message', '').strip()
        if not (property_id and customer_name and customer_email and message):
            error = "Please fill in all required fields (property, name, email, message)."
            return render_template('property_inquiry.html', properties=properties, error=error,
                                   form_data=request.form)
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
        return redirect(url_for('my_inquiries'))
    else:
        return render_template('property_inquiry.html', properties=properties)
@app.route('/my_inquiries', methods=['GET', 'POST'])
def my_inquiries():
    inquiries = read_inquiries()
    properties = {p['property_id']: p for p in read_properties()}
    status_filter = request.args.get('status', 'All')
    # Filter inquiries by status if not 'All'
    if status_filter and status_filter != 'All':
        inquiries = [inq for inq in inquiries if inq['status'].lower() == status_filter.lower()]
    if request.method == 'POST':
        # Handle deletion of inquiry
        delete_id = request.form.get('delete_inquiry_id')
        if delete_id:
            inquiries = [inq for inq in inquiries if inq['inquiry_id'] != delete_id]
            write_inquiries(inquiries)
            return redirect(url_for('my_inquiries', status=status_filter))
    return render_template('my_inquiries.html',
                           inquiries=inquiries,
                           properties=properties,
                           status_filter=status_filter)
@app.route('/my_favorites')
def my_favorites():
    favorites = read_favorites()
    properties = {p['property_id']: p for p in read_properties()}
    # Build list of favorite properties with details
    favorite_properties = []
    for fav in favorites:
        prop = properties.get(fav['property_id'])
        if prop:
            favorite_properties.append(prop)
    return render_template('my_favorites.html',
                           favorites_list=favorite_properties)
@app.route('/agents')
def agents():
    agents_list = read_agents()
    search_query = request.args.get('search', '').strip().lower()
    if search_query:
        agents_list = [agent for agent in agents_list if search_query in agent['agent_name'].lower()]
    return render_template('agents.html',
                           agents_list=agents_list,
                           search_query=search_query)
@app.route('/locations')
def locations():
    locations_list = read_locations()
    sort_by = request.args.get('sort', 'By Name')
    if sort_by == 'By Name':
        locations_list.sort(key=lambda x: x['location_name'].lower())
    elif sort_by == 'By Properties Count':
        locations_list.sort(key=lambda x: x['property_count'], reverse=True)
    elif sort_by == 'By Average Price':
        locations_list.sort(key=lambda x: x['average_price'], reverse=True)
    return render_template('locations.html',
                           locations_list=locations_list,
                           sort_by=sort_by)
@app.route('/view_location/<location_id>')
def view_location(location_id):
    # Show properties in the selected location
    properties = read_properties()
    location_name = get_location_name_by_id(location_id)
    location_properties = [p for p in properties if p['location'] == location_name and p['status'].lower() == 'available']
    return render_template('property_search.html',
                           properties=location_properties,
                           location_filter=location_name,
                           price_min='',
                           price_max='',
                           property_type_filter='')
def get_location_name_by_id(location_id):
    locations = read_locations()
    for loc in locations:
        if loc['location_id'] == location_id:
            return loc['location_name']
    return ''
# Run the app
if __name__ == '__main__':
    app.run(port=5000, debug=True)