from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import os

app = Flask(__name__)

DATA_DIR = 'data'

# Utility functions to load and save data files

def load_properties():
    properties = []
    path = os.path.join(DATA_DIR, 'properties.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) == 11:
                    property = {
                        'property_id': parts[0],
                        'address': parts[1],
                        'location': parts[2],
                        'price': int(parts[3]),
                        'property_type': parts[4],
                        'bedrooms': parts[5],
                        'bathrooms': parts[6],
                        'square_feet': parts[7],
                        'description': parts[8],
                        'agent_id': parts[9],
                        'status': parts[10]
                    }
                    properties.append(property)
    return properties


def load_locations():
    locations = []
    path = os.path.join(DATA_DIR, 'locations.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) == 6:
                    location = {
                        'location_id': parts[0],
                        'location_name': parts[1],
                        'region': parts[2],
                        'average_price': int(parts[3]),
                        'property_count': int(parts[4]),
                        'description': parts[5]
                    }
                    locations.append(location)
    return locations


def load_inquiries():
    inquiries = []
    path = os.path.join(DATA_DIR, 'inquiries.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) == 8:
                    inquiry = {
                        'inquiry_id': parts[0],
                        'property_id': parts[1],
                        'customer_name': parts[2],
                        'customer_email': parts[3],
                        'customer_phone': parts[4],
                        'message': parts[5],
                        'inquiry_date': parts[6],
                        'status': parts[7]
                    }
                    inquiries.append(inquiry)
    return inquiries


def save_inquiries(inquiries):
    path = os.path.join(DATA_DIR, 'inquiries.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for i in inquiries:
            line = '|'.join([i['inquiry_id'], i['property_id'], i['customer_name'], i['customer_email'], i['customer_phone'], i['message'], i['inquiry_date'], i['status']])
            f.write(line + '\n')


def load_favorites():
    favorites = []
    path = os.path.join(DATA_DIR, 'favorites.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) == 3:
                    favorite = {
                        'favorite_id': parts[0],
                        'property_id': parts[1],
                        'added_date': parts[2]
                    }
                    favorites.append(favorite)
    return favorites


def save_favorites(favorites):
    path = os.path.join(DATA_DIR, 'favorites.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for fav in favorites:
            line = '|'.join([fav['favorite_id'], fav['property_id'], fav['added_date']])
            f.write(line + '\n')


def load_agents():
    agents = []
    path = os.path.join(DATA_DIR, 'agents.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) == 6:
                    agent = {
                        'agent_id': parts[0],
                        'agent_name': parts[1],
                        'specialization': parts[2],
                        'email': parts[3],
                        'phone': parts[4],
                        'properties_sold': int(parts[5])
                    }
                    agents.append(agent)
    return agents


# Route: Dashboard
@app.route('/')
@app.route('/dashboard')
def dashboard():
    properties = load_properties()
    # Featured properties: just 3 available or sold properties randomly selected (could use first 3 available)
    featured = [p for p in properties if p['status'] == 'Available'][:3]  # first 3 available
    return render_template('dashboard.html', featured_properties=featured)


# Route: Property Search
@app.route('/search', methods=['GET'])
def search_properties():
    properties = load_properties()
    location = request.args.get('location', '').strip().lower()
    try:
        price_min = int(request.args.get('price_min', 0))
    except ValueError:
        price_min = 0
    try:
        price_max = int(request.args.get('price_max', 999999999))
    except ValueError:
        price_max = 999999999
    property_type = request.args.get('property_type', '')

    filtered = []
    for p in properties:
        if p['status'] != 'Available':
            continue
        if location and location not in p['location'].lower():
            continue
        if p['price'] < price_min or p['price'] > price_max:
            continue
        if property_type and property_type != '' and p['property_type'] != property_type:
            continue
        filtered.append(p)
    return render_template('search.html', properties=filtered, filter_params={'location': location, 'price_min': price_min, 'price_max': price_max, 'property_type': property_type})


# Route: Property Details
@app.route('/property/<property_id>')
def property_details(property_id):
    properties = load_properties()
    property = next((p for p in properties if p['property_id'] == property_id), None)
    if property is None:
        return "Property not found", 404
    return render_template('property_details.html', property=property)


# Route: Add to Favorites
@app.route('/add_favorite/<property_id>', methods=['POST'])
def add_favorite(property_id):
    favorites = load_favorites()
    next_id = str(max([int(f['favorite_id']) for f in favorites], default=0) + 1)
    now_str = datetime.now().strftime('%Y-%m-%d')
    # Check if already in favorites
    if any(f['property_id'] == property_id for f in favorites):
        return redirect(url_for('my_favorites'))
    favorites.append({'favorite_id': next_id, 'property_id': property_id, 'added_date': now_str})
    save_favorites(favorites)
    return redirect(url_for('my_favorites'))


# Route: Submit Property Inquiry
@app.route('/submit_inquiry', methods=['GET', 'POST'])
def submit_inquiry():
    properties = load_properties()
    if request.method == 'POST':
        property_id = request.form['select_property']
        customer_name = request.form['inquiry_name'].strip()
        customer_email = request.form['inquiry_email'].strip()
        customer_phone = request.form['inquiry_phone'].strip()
        message = request.form['inquiry_message'].strip()

        inquiries = load_inquiries()
        next_id = str(max([int(i['inquiry_id']) for i in inquiries], default=0) + 1)
        now_str = datetime.now().strftime('%Y-%m-%d')

        inquiry = {
            'inquiry_id': next_id,
            'property_id': property_id,
            'customer_name': customer_name,
            'customer_email': customer_email,
            'customer_phone': customer_phone,
            'message': message,
            'inquiry_date': now_str,
            'status': 'Pending'
        }
        inquiries.append(inquiry)
        save_inquiries(inquiries)
        return redirect(url_for('my_inquiries'))
    else:
        # Pass selected property id if provided as query param
        selected_property_id = request.args.get('property_id', '')
        return render_template('submit_inquiry.html', properties=properties, selected_property_id=selected_property_id)


# Route: My Inquiries
@app.route('/my_inquiries', methods=['GET', 'POST'])
def my_inquiries():
    inquiries = load_inquiries()
    properties = load_properties()
    status_filter = request.args.get('status', 'All')

    if status_filter != 'All':
        inquiries = [i for i in inquiries if i['status'] == status_filter]

    # Enrich inquiries with property address
    for i in inquiries:
        prop = next((p for p in properties if p['property_id'] == i['property_id']), None)
        i['property_address'] = prop['address'] if prop else 'Unknown'

    return render_template('my_inquiries.html', inquiries=inquiries, status_filter=status_filter)


# Route: Delete Inquiry
@app.route('/delete_inquiry/<inquiry_id>', methods=['POST'])
def delete_inquiry(inquiry_id):
    inquiries = load_inquiries()
    inquiries = [i for i in inquiries if i['inquiry_id'] != inquiry_id]
    save_inquiries(inquiries)
    return redirect(url_for('my_inquiries'))


# Route: My Favorites
@app.route('/my_favorites')
def my_favorites():
    favorites = load_favorites()
    properties = load_properties()
    favorite_properties = []
    for fav in favorites:
        prop = next((p for p in properties if p['property_id'] == fav['property_id']), None)
        if prop:
            favorite_properties.append(prop)
    return render_template('my_favorites.html', favorite_properties=favorite_properties)


# Route: Remove from Favorites
@app.route('/remove_favorite/<property_id>', methods=['POST'])
def remove_favorite(property_id):
    favorites = load_favorites()
    favorites = [f for f in favorites if f['property_id'] != property_id]
    save_favorites(favorites)
    return redirect(url_for('my_favorites'))


# Route: Agent Directory
@app.route('/agents')
def agents_directory():
    agents = load_agents()
    search_query = request.args.get('search', '').lower()
    if search_query:
        agents = [a for a in agents if search_query in a['agent_name'].lower()]
    return render_template('agents.html', agents=agents, search_query=search_query)


# Route: Locations Page
@app.route('/locations')
def locations_page():
    locations = load_locations()
    sort_option = request.args.get('sort', 'Name')
    # Sort locations accordingly
    if sort_option == 'Name':
        locations.sort(key=lambda l: l['location_name'])
    elif sort_option == 'Property Count':
        locations.sort(key=lambda l: l['property_count'], reverse=True)
    elif sort_option == 'Average Price':
        locations.sort(key=lambda l: l['average_price'], reverse=True)
    return render_template('locations.html', locations=locations, sort_option=sort_option)


# Route: View properties by location from Locations page (reusing search page but filtered)
@app.route('/location_properties/<location_name>')
def location_properties(location_name):
    properties = load_properties()
    filtered = [p for p in properties if p['location'].lower() == location_name.lower() and p['status'] == 'Available']
    return render_template('search.html', properties=filtered, filter_params={'location': location_name, 'price_min': 0, 'price_max': 999999999, 'property_type': ''})


# Route: Submit Inquiry from Property Details (redirect to property inquiry with selected property)
@app.route('/inquire_property/<property_id>')
def inquire_property(property_id):
    return redirect(url_for('submit_inquiry', property_id=property_id))

if __name__ == '__main__':
    app.run(debug=True)
