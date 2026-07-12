from flask import Flask, render_template, redirect, url_for, request
import os
from datetime import date

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Helper functions to load data from files

def load_properties():
    properties = []
    filepath = os.path.join(DATA_DIR, 'properties.txt')
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 11:
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
    except IOError:
        # File not found or other IO error
        pass
    return properties


def load_locations():
    locations = []
    filepath = os.path.join(DATA_DIR, 'locations.txt')
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 6:
                    loc = {
                        'location_id': int(parts[0]),
                        'location_name': parts[1],
                        'region': parts[2],
                        'average_price': int(parts[3]),
                        'property_count': int(parts[4]),
                        'description': parts[5]
                    }
                    locations.append(loc)
    except IOError:
        pass
    return locations


def load_inquiries():
    inquiries = []
    filepath = os.path.join(DATA_DIR, 'inquiries.txt')
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 8:
                    inquiry = {
                        'inquiry_id': int(parts[0]),
                        'property_id': int(parts[1]),
                        'customer_name': parts[2],
                        'customer_email': parts[3],
                        'customer_phone': parts[4],
                        'message': parts[5],
                        'inquiry_date': parts[6],
                        'status': parts[7]
                    }
                    inquiries.append(inquiry)
    except IOError:
        pass
    return inquiries


def save_inquiries(inquiries):
    filepath = os.path.join(DATA_DIR, 'inquiries.txt')
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            for inquiry in inquiries:
                line = f"{inquiry['inquiry_id']}|{inquiry['property_id']}|{inquiry['customer_name']}|{inquiry['customer_email']}|{inquiry['customer_phone']}|{inquiry['message']}|{inquiry['inquiry_date']}|{inquiry['status']}\n"
                f.write(line)
    except IOError:
        pass


def load_favorites():
    favorites = []
    filepath = os.path.join(DATA_DIR, 'favorites.txt')
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 3:
                    fav = {
                        'favorite_id': int(parts[0]),
                        'property_id': int(parts[1]),
                        'added_date': parts[2]
                    }
                    favorites.append(fav)
    except IOError:
        pass
    return favorites


def save_favorites(favorites):
    filepath = os.path.join(DATA_DIR, 'favorites.txt')
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            for fav in favorites:
                line = f"{fav['favorite_id']}|{fav['property_id']}|{fav['added_date']}\n"
                f.write(line)
    except IOError:
        pass


def load_agents():
    agents = []
    filepath = os.path.join(DATA_DIR, 'agents.txt')
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 6:
                    agent = {
                        'agent_id': int(parts[0]),
                        'agent_name': parts[1],
                        'specialization': parts[2],
                        'email': parts[3],
                        'phone': parts[4],
                        'properties_sold': int(parts[5])
                    }
                    agents.append(agent)
    except IOError:
        pass
    return agents


# Routes

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    # featured_properties: let's define as first 3 properties with status 'Available'
    properties = load_properties()
    featured_properties = [p for p in properties if p['status'] == 'Available'][:3]
    # recent_listings: all properties sorted by property_id desc, first 5
    recent_listings = sorted(properties, key=lambda x: x['property_id'], reverse=True)[:5]
    return render_template('dashboard.html', featured_properties=featured_properties, recent_listings=recent_listings)


@app.route('/search')
def property_search():
    properties = load_properties()

    # Extract filters from query string
    location_filter = request.args.get('location_filter', '')
    price_min = request.args.get('price_min', '')
    price_max = request.args.get('price_max', '')
    property_type_filter = request.args.get('property_type_filter', '')

    # Convert filters
    try:
        price_min = int(price_min) if price_min != '' else None
    except ValueError:
        price_min = None
    try:
        price_max = int(price_max) if price_max != '' else None
    except ValueError:
        price_max = None
    if property_type_filter == '':
        property_type_filter = None

    # Filtering
    filtered_properties = []
    for p in properties:
        if location_filter and p['location'] != location_filter:
            continue
        if price_min is not None and p['price'] < price_min:
            continue
        if price_max is not None and p['price'] > price_max:
            continue
        if property_type_filter and p['property_type'] != property_type_filter:
            continue
        filtered_properties.append(p)

    return render_template('search.html', properties=filtered_properties,
                           location_filter=location_filter, price_min=price_min,
                           price_max=price_max, property_type_filter=property_type_filter)


@app.route('/property/<int:property_id>')
def property_details(property_id):
    properties = load_properties()
    agents = load_agents()

    property_item = next((p for p in properties if p['property_id'] == property_id), None)
    if not property_item:
        return "Property not found", 404

    agent = next((a for a in agents if a['agent_id'] == property_item['agent_id']), None)

    return render_template('property_details.html', property=property_item, agent=agent)


@app.route('/property/<int:property_id>/inquiry', methods=['GET'])
def property_inquiry_form(property_id):
    properties = load_properties()
    return render_template('inquiry.html', properties=properties, selected_property_id=property_id)


@app.route('/property/<int:property_id>/inquiry', methods=['POST'])
def submit_property_inquiry(property_id):
    # Get form data
    customer_name = request.form.get('customer_name', '').strip()
    customer_email = request.form.get('customer_email', '').strip()
    customer_phone = request.form.get('customer_phone', '').strip()
    inquiry_message = request.form.get('inquiry_message', '').strip()

    # Simple validation
    if not customer_name or not customer_email or not inquiry_message:
        # Ideally should handle with flash messages, but not stated in spec
        return "Missing required fields", 400

    inquiries = load_inquiries()

    # Generate new inquiry_id
    if inquiries:
        new_inquiry_id = max(i['inquiry_id'] for i in inquiries) + 1
    else:
        new_inquiry_id = 1

    inquiry_date = date.today().isoformat()

    new_inquiry = {
        'inquiry_id': new_inquiry_id,
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

    return redirect(url_for('my_inquiries'))


@app.route('/inquiries')
def my_inquiries():
    inquiries = load_inquiries()

    status_filter = request.args.get('status_filter', '')
    if status_filter:
        inquiries = [i for i in inquiries if i['status'] == status_filter]

    return render_template('inquiries.html', inquiries=inquiries, status_filter=status_filter)


@app.route('/inquiries/delete/<int:inquiry_id>', methods=['POST'])
def delete_inquiry(inquiry_id):
    inquiries = load_inquiries()
    filtered_inquiries = [i for i in inquiries if i['inquiry_id'] != inquiry_id]

    save_inquiries(filtered_inquiries)

    return redirect(url_for('my_inquiries'))


@app.route('/favorites')
def my_favorites():
    favorites = load_favorites()
    properties = load_properties()

    properties_lookup = {p['property_id']: p for p in properties}

    return render_template('favorites.html', favorites=favorites, properties_lookup=properties_lookup)


@app.route('/favorites/add/<int:property_id>', methods=['POST'])
def add_to_favorites(property_id):
    favorites = load_favorites()

    existing_ids = [f['favorite_id'] for f in favorites]
    new_favorite_id = max(existing_ids) + 1 if existing_ids else 1

    # Check if property_id already in favorites to avoid duplicates
    if any(f['property_id'] == property_id for f in favorites):
        return redirect(url_for('my_favorites'))

    added_date = date.today().isoformat()

    new_fav = {
        'favorite_id': new_favorite_id,
        'property_id': property_id,
        'added_date': added_date
    }

    favorites.append(new_fav)
    save_favorites(favorites)

    return redirect(url_for('my_favorites'))


@app.route('/favorites/remove/<int:property_id>', methods=['POST'])
def remove_from_favorites(property_id):
    favorites = load_favorites()
    filtered_favorites = [f for f in favorites if f['property_id'] != property_id]

    save_favorites(filtered_favorites)

    return redirect(url_for('my_favorites'))


@app.route('/agents')
def agent_directory():
    agents = load_agents()
    return render_template('agents.html', agents=agents)


@app.route('/locations')
def locations_page():
    locations = load_locations()
    return render_template('locations.html', locations=locations)


if __name__ == '__main__':
    app.run(debug=True)
