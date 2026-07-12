from flask import Flask, render_template, redirect, url_for, request
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

# Data file paths
PROPERTIES_FILE = 'data/properties.txt'
LOCATIONS_FILE = 'data/locations.txt'
INQUIRIES_FILE = 'data/inquiries.txt'
FAVORITES_FILE = 'data/favorites.txt'
AGENTS_FILE = 'data/agents.txt'

# Helper functions to load data

def load_properties():
    properties = []
    if not os.path.exists(PROPERTIES_FILE):
        return properties
    try:
        with open(PROPERTIES_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 11:
                    continue
                prop = {
                    'property_id': int(parts[0]),
                    'address': parts[1],
                    'location': parts[2],
                    'price': int(parts[3]),
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
        pass
    return properties


def load_locations():
    locations = []
    if not os.path.exists(LOCATIONS_FILE):
        return locations
    try:
        with open(LOCATIONS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 6:
                    continue
                loc = {
                    'location_id': int(parts[0]),
                    'location_name': parts[1],
                    'region': parts[2],
                    'average_price': int(parts[3]),
                    'property_count': int(parts[4]),
                    'description': parts[5]
                }
                locations.append(loc)
    except Exception:
        pass
    return locations


def load_inquiries():
    inquiries = []
    if not os.path.exists(INQUIRIES_FILE):
        return inquiries
    try:
        with open(INQUIRIES_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 8:
                    continue
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
        pass
    return inquiries


def load_favorites():
    favorites = []
    if not os.path.exists(FAVORITES_FILE):
        return favorites
    try:
        with open(FAVORITES_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 3:
                    continue
                fav = {
                    'favorite_id': int(parts[0]),
                    'property_id': int(parts[1]),
                    'added_date': parts[2]
                }
                favorites.append(fav)
    except Exception:
        pass
    return favorites


def load_agents():
    agents = []
    if not os.path.exists(AGENTS_FILE):
        return agents
    try:
        with open(AGENTS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 6:
                    continue
                agent = {
                    'agent_id': int(parts[0]),
                    'agent_name': parts[1],
                    'specialization': parts[2],
                    'email': parts[3],
                    'phone': parts[4],
                    'properties_sold': int(parts[5])
                }
                agents.append(agent)
    except Exception:
        pass
    return agents


# Helper function to write inquiries data
# Overwrites entire inquiries.txt file with inquiry dict list

def save_inquiries(inquiries):
    try:
        with open(INQUIRIES_FILE, 'w', encoding='utf-8') as f:
            for inq in inquiries:
                line = f"{inq['inquiry_id']}|{inq['property_id']}|{inq['customer_name']}|{inq['customer_email']}|{inq['customer_phone']}|{inq['message']}|{inq['inquiry_date']}|{inq['status']}\n"
                f.write(line)
    except Exception:
        pass

# Helper function to save favorites

def save_favorites(favorites):
    try:
        with open(FAVORITES_FILE, 'w', encoding='utf-8') as f:
            for fav in favorites:
                line = f"{fav['favorite_id']}|{fav['property_id']}|{fav['added_date']}\n"
                f.write(line)
    except Exception:
        pass


# ROUTES

@app.route('/', methods=['GET'])
def root_redirect():
    return redirect(url_for('dashboard_page'))


@app.route('/dashboard', methods=['GET'])
def dashboard_page():
    # For featured_properties: pick first 5 available properties with status 'Available'
    properties = load_properties()
    featured_properties = [p for p in properties if p['status'] == 'Available'][:5]
    # recent_listings: last 5 properties by property_id descending
    recent_listings = sorted(properties, key=lambda x: x['property_id'], reverse=True)[:5]
    return render_template('dashboard.html', featured_properties=featured_properties, recent_listings=recent_listings)


@app.route('/properties', methods=['GET', 'POST'])
def property_search():
    properties = load_properties()
    if request.method == 'POST':
        location_input = request.form.get('location_input', '').strip()
        price_min = request.form.get('price_min', '').strip()
        price_max = request.form.get('price_max', '').strip()
        property_type = request.form.get('property_type', '').strip()

        # Filtering
        filtered = properties

        if location_input:
            filtered = [p for p in filtered if location_input.lower() in p['location'].lower() or location_input.lower() in p['address'].lower()]

        if price_min.isdigit():
            price_min_val = int(price_min)
            filtered = [p for p in filtered if p['price'] >= price_min_val]

        if price_max.isdigit():
            price_max_val = int(price_max)
            filtered = [p for p in filtered if p['price'] <= price_max_val]

        if property_type and property_type in ['House', 'Apartment', 'Condo', 'Land']:
            filtered = [p for p in filtered if p['property_type'] == property_type]

        properties = filtered

    return render_template('property_search.html', properties=properties)


@app.route('/properties/<int:property_id>', methods=['GET'])
def property_details(property_id):
    properties = load_properties()
    prop = next((p for p in properties if p['property_id'] == property_id), None)
    if not prop:
        return "Property not found", 404
    return render_template('property_details.html', property=prop)


@app.route('/inquiry', methods=['GET', 'POST'])
def property_inquiry():
    properties = load_properties()
    if request.method == 'POST':
        try:
            property_id = int(request.form.get('property_id', 0))
            inquiry_name = request.form.get('inquiry_name', '').strip()
            inquiry_email = request.form.get('inquiry_email', '').strip()
            inquiry_phone = request.form.get('inquiry_phone', '').strip()
            inquiry_message = request.form.get('inquiry_message', '').strip()
            
            # Validate at minimum property id and name and email
            if property_id <= 0 or not inquiry_name or not inquiry_email or not inquiry_message:
                return render_template('inquiry.html', properties=properties, error="Please fill all required fields.")
            # Load inquiries and add new inquiry
            inquiries = load_inquiries()
            new_id = max((i['inquiry_id'] for i in inquiries), default=0) + 1
            inquiry_date = datetime.now().strftime('%Y-%m-%d')
            new_inquiry = {
                'inquiry_id': new_id,
                'property_id': property_id,
                'customer_name': inquiry_name,
                'customer_email': inquiry_email,
                'customer_phone': inquiry_phone,
                'message': inquiry_message,
                'inquiry_date': inquiry_date,
                'status': 'Pending'
            }
            inquiries.append(new_inquiry)
            save_inquiries(inquiries)
            return render_template('inquiry.html', properties=properties, success="Inquiry submitted successfully.")
        except Exception:
            return render_template('inquiry.html', properties=properties, error="Failed to submit inquiry.")

    return render_template('inquiry.html', properties=properties)


@app.route('/inquiries', methods=['GET', 'POST'])
def my_inquiries():
    inquiries = load_inquiries()
    if request.method == 'POST':
        inquiry_status_filter = request.form.get('inquiry_status_filter', 'All').strip()
        delete_inquiry_id = request.form.get('delete_inquiry_id', '').strip()

        if delete_inquiry_id.isdigit():
            delete_id = int(delete_inquiry_id)
            inquiries = [inq for inq in inquiries if inq['inquiry_id'] != delete_id]
            save_inquiries(inquiries)

        if inquiry_status_filter and inquiry_status_filter != 'All':
            inquiries = [inq for inq in inquiries if inq['status'] == inquiry_status_filter]

    return render_template('inquiries.html', inquiries=inquiries)


@app.route('/favorites', methods=['GET', 'POST'])
def my_favorites():
    favorites = load_favorites()
    properties = load_properties()
    properties_dict = {p['property_id']: p for p in properties}

    if request.method == 'POST':
        remove_property_id = request.form.get('remove_property_id', '').strip()
        if remove_property_id.isdigit():
            rid = int(remove_property_id)
            favorites = [f for f in favorites if f['property_id'] != rid]
            save_favorites(favorites)

    # Get favorite properties from favorites list using properties dict
    favorite_properties = [properties_dict[f['property_id']] for f in favorites if f['property_id'] in properties_dict]

    return render_template('favorites.html', favorite_properties=favorite_properties, properties_dict=properties_dict)


@app.route('/agents', methods=['GET'])
def agent_directory():
    agents = load_agents()
    return render_template('agents.html', agents=agents)


@app.route('/locations', methods=['GET', 'POST'])
def locations_page():
    locations = load_locations()

    if request.method == 'POST':
        location_sort = request.form.get('location_sort', 'By Name')
        if location_sort == 'By Name':
            locations.sort(key=lambda x: x['location_name'].lower())
        elif location_sort == 'By Properties Count':
            locations.sort(key=lambda x: x['property_count'], reverse=True)
        elif location_sort == 'By Average Price':
            locations.sort(key=lambda x: x['average_price'], reverse=True)

    return render_template('locations.html', locations=locations)


if __name__ == '__main__':
    app.run(debug=True)
