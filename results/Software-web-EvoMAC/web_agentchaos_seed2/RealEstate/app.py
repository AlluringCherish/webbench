'''
Main application file for the RealEstate web application.
Uses Flask to serve pages and handle user interactions.
Data is stored and managed through local text files in the 'data' directory.
'''
from flask import Flask, render_template, request, redirect, url_for
import os
import datetime
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
                'bedrooms': bedrooms,
                'bathrooms': bathrooms,
                'square_feet': square_feet,
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
        for i in inquiries:
            line = '|'.join([
                i['inquiry_id'],
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
                fav['favorite_id'],
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
                'properties_sold': properties_sold
            })
    return agents
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
    return str(max_id + 1)
# Routes
@app.route('/')
def dashboard():
    properties = read_properties()
    # Featured properties: show first 3 available properties
    featured = [p for p in properties if p['status'].lower() == 'available'][:3]
    recent = sorted(properties, key=lambda x: int(x['property_id']), reverse=True)[:5]
    return render_template('dashboard.html', featured_properties=featured, recent_listings=recent)
@app.route('/search', methods=['GET', 'POST'])
def property_search():
    properties = read_properties()
    locations = list(set(p['location'] for p in properties))
    property_types = ['House', 'Apartment', 'Condo', 'Land']
    # Filters
    location_filter = request.args.get('location', '').strip()
    price_min = request.args.get('price_min', '')
    price_max = request.args.get('price_max', '')
    property_type_filter = request.args.get('property_type', '')
    filtered = properties
    if location_filter:
        filtered = [p for p in filtered if p['location'].lower() == location_filter.lower()]
    if price_min.isdigit():
        filtered = [p for p in filtered if p['price'] >= int(price_min)]
    if price_max.isdigit():
        filtered = [p for p in filtered if p['price'] <= int(price_max)]
    if property_type_filter and property_type_filter in property_types:
        filtered = [p for p in filtered if p['property_type'] == property_type_filter]
    return render_template('search.html',
                           properties=filtered,
                           locations=locations,
                           property_types=property_types,
                           location_filter=location_filter,
                           price_min=price_min,
                           price_max=price_max,
                           property_type_filter=property_type_filter)
@app.route('/property/<property_id>')
def property_details(property_id):
    properties = read_properties()
    property_obj = next((p for p in properties if p['property_id'] == property_id), None)
    if not property_obj:
        return "Property not found", 404
    favorites = read_favorites()
    is_favorite = any(fav['property_id'] == property_id for fav in favorites)
    return render_template('property_details.html', property=property_obj, is_favorite=is_favorite)
@app.route('/add_favorite/<property_id>', methods=['POST'])
def add_favorite(property_id):
    favorites = read_favorites()
    if any(fav['property_id'] == property_id for fav in favorites):
        # Already favorite
        return redirect(url_for('property_details', property_id=property_id))
    new_id = get_next_id(favorites, 'favorite_id')
    today = datetime.date.today().isoformat()
    favorites.append({'favorite_id': new_id, 'property_id': property_id, 'added_date': today})
    write_favorites(favorites)
    return redirect(url_for('property_details', property_id=property_id))
@app.route('/remove_favorite/<property_id>', methods=['POST'])
def remove_favorite(property_id):
    favorites = read_favorites()
    favorites = [fav for fav in favorites if fav['property_id'] != property_id]
    write_favorites(favorites)
    return redirect(url_for('my_favorites'))
@app.route('/inquiry', methods=['GET', 'POST'])
def property_inquiry():
    properties = read_properties()
    if request.method == 'POST':
        property_id = request.form.get('select_property')
        name = request.form.get('inquiry_name', '').strip()
        email = request.form.get('inquiry_email', '').strip()
        phone = request.form.get('inquiry_phone', '').strip()
        message = request.form.get('inquiry_message', '').strip()
        if not (property_id and name and email and message):
            error = "Please fill in all required fields."
            return render_template('inquiry.html', properties=properties, error=error,
                                   form_data=request.form)
        inquiries = read_inquiries()
        new_id = get_next_id(inquiries, 'inquiry_id')
        today = datetime.date.today().isoformat()
        inquiries.append({
            'inquiry_id': new_id,
            'property_id': property_id,
            'customer_name': name,
            'customer_email': email,
            'customer_phone': phone,
            'message': message,
            'inquiry_date': today,
            'status': 'Pending'
        })
        write_inquiries(inquiries)
        return redirect(url_for('my_inquiries'))
    return render_template('inquiry.html', properties=properties)
@app.route('/my_inquiries', methods=['GET', 'POST'])
def my_inquiries():
    inquiries = read_inquiries()
    properties = {p['property_id']: p for p in read_properties()}
    status_filter = request.args.get('status', 'All')
    if status_filter != 'All':
        inquiries = [inq for inq in inquiries if inq['status'] == status_filter]
    if request.method == 'POST':
        # Delete inquiry
        delete_id = request.form.get('delete_inquiry_id')
        if delete_id:
            inquiries = [inq for inq in inquiries if inq['inquiry_id'] != delete_id]
            write_inquiries(inquiries)
            return redirect(url_for('my_inquiries', status=status_filter))
    return render_template('my_inquiries.html', inquiries=inquiries, properties=properties, status_filter=status_filter)
@app.route('/my_favorites')
def my_favorites():
    favorites = read_favorites()
    properties = {p['property_id']: p for p in read_properties()}
    favorite_properties = []
    for fav in favorites:
        prop = properties.get(fav['property_id'])
        if prop:
            favorite_properties.append(prop)
    return render_template('my_favorites.html', favorites=favorite_properties)
@app.route('/agents')
def agents():
    agents = read_agents()
    search_name = request.args.get('search_name', '').strip().lower()
    if search_name:
        agents = [a for a in agents if search_name in a['agent_name'].lower()]
    return render_template('agents.html', agents=agents, search_name=search_name)
@app.route('/locations')
def locations():
    locations = read_locations()
    sort_by = request.args.get('sort_by', 'By Name')
    if sort_by == 'By Name':
        locations.sort(key=lambda x: x['location_name'])
    elif sort_by == 'By Properties Count':
        locations.sort(key=lambda x: x['property_count'], reverse=True)
    elif sort_by == 'By Average Price':
        locations.sort(key=lambda x: x['average_price'], reverse=True)
    return render_template('locations.html', locations=locations, sort_by=sort_by)
@app.route('/location/<location_id>')
def view_location(location_id):
    locations = read_locations()
    location_obj = next((loc for loc in locations if loc['location_id'] == location_id), None)
    if not location_obj:
        return "Location not found", 404
    properties = read_properties()
    location_properties = [p for p in properties if p['location'].lower() == location_obj['location_name'].lower()]
    return render_template('location_properties.html', location=location_obj, properties=location_properties)
@app.route('/contact_agent/<agent_id>', methods=['GET', 'POST'])
def contact_agent(agent_id):
    agents = read_agents()
    agent = next((a for a in agents if a['agent_id'] == agent_id), None)
    if not agent:
        return "Agent not found", 404
    if request.method == 'POST':
        # For simplicity, just redirect back to agents page after "contact"
        return redirect(url_for('agents'))
    return render_template('contact_agent.html', agent=agent)
@app.route('/back_to_dashboard')
def back_to_dashboard():
    return redirect(url_for('dashboard'))
if __name__ == '__main__':
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    app.run(debug=True)