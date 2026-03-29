from flask import Flask, render_template, redirect, url_for, request
import os
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

# Data file paths (relative to this script's directory)
PROPERTIES_FILE = os.path.join('data', 'properties.txt')
LOCATIONS_FILE = os.path.join('data', 'locations.txt')
INQUIRIES_FILE = os.path.join('data', 'inquiries.txt')
FAVORITES_FILE = os.path.join('data', 'favorites.txt')
AGENTS_FILE = os.path.join('data', 'agents.txt')

# Helper functions to load data from files according to schemas

def load_properties():
    properties = []
    try:
        with open(PROPERTIES_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 11:
                    continue
                property_id, address, location, price, property_type, bedrooms, bathrooms, square_feet, description, agent_id, status = parts
                properties.append({
                    'property_id': int(property_id),
                    'address': address,
                    'location': location,
                    'price': float(price),
                    'property_type': property_type,
                    'bedrooms': int(bedrooms),
                    'bathrooms': float(bathrooms),
                    'square_feet': int(square_feet),
                    'description': description,
                    'agent_id': int(agent_id),
                    'status': status
                })
    except (FileNotFoundError, IOError):
        pass
    return properties


def load_locations():
    locations = []
    try:
        with open(LOCATIONS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 6:
                    continue
                location_id, location_name, region, average_price, property_count, description = parts
                locations.append({
                    'location_id': int(location_id),
                    'location_name': location_name,
                    'region': region,
                    'average_price': float(average_price),
                    'property_count': int(property_count),
                    'description': description
                })
    except (FileNotFoundError, IOError):
        pass
    return locations


def load_inquiries():
    inquiries = []
    try:
        with open(INQUIRIES_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 8:
                    continue
                inquiry_id, property_id, customer_name, customer_email, customer_phone, message, inquiry_date, status = parts
                inquiries.append({
                    'inquiry_id': int(inquiry_id),
                    'property_id': int(property_id),
                    'customer_name': customer_name,
                    'customer_email': customer_email,
                    'customer_phone': customer_phone,
                    'message': message,
                    'inquiry_date': inquiry_date,
                    'status': status
                })
    except (FileNotFoundError, IOError):
        pass
    return inquiries


def load_favorites():
    favorites = []
    try:
        with open(FAVORITES_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 3:
                    continue
                favorite_id, property_id, added_date = parts
                favorites.append({
                    'favorite_id': int(favorite_id),
                    'property_id': int(property_id),
                    'added_date': added_date
                })
    except (FileNotFoundError, IOError):
        pass
    return favorites


def load_agents():
    agents = []
    try:
        with open(AGENTS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 6:
                    continue
                agent_id, agent_name, specialization, email, phone, properties_sold = parts
                agents.append({
                    'agent_id': int(agent_id),
                    'agent_name': agent_name,
                    'specialization': specialization,
                    'email': email,
                    'phone': phone,
                    'properties_sold': int(properties_sold)
                })
    except (FileNotFoundError, IOError):
        pass
    return agents


def save_inquiries(inquiries):
    try:
        with open(INQUIRIES_FILE, 'w', encoding='utf-8') as f:
            for inquiry in inquiries:
                line = f"{inquiry['inquiry_id']}|{inquiry['property_id']}|{inquiry['customer_name']}|{inquiry['customer_email']}|{inquiry['customer_phone']}|{inquiry['message']}|{inquiry['inquiry_date']}|{inquiry['status']}\n"
                f.write(line)
    except (FileNotFoundError, IOError):
        pass


def save_favorites(favorites):
    try:
        with open(FAVORITES_FILE, 'w', encoding='utf-8') as f:
            for favorite in favorites:
                line = f"{favorite['favorite_id']}|{favorite['property_id']}|{favorite['added_date']}\n"
                f.write(line)
    except (FileNotFoundError, IOError):
        pass


# -------------- ROUTES IMPLEMENTATION --------------

@app.route('/', methods=['GET'])
def root_redirect():
    return redirect(url_for('dashboard'))


@app.route('/dashboard', methods=['GET'])
def dashboard():
    properties = load_properties()
    # featured_properties: let's consider properties with status Available and pick top 5 by price descending
    featured_properties = sorted(
        [p for p in properties if p['status'] == 'Available'], key=lambda x: x['price'], reverse=True)[:5]
    # recent_listings: 5 most recent by property_id descending (assuming higher id is most recent)
    recent_listings = sorted(properties, key=lambda x: x['property_id'], reverse=True)[:5]
    return render_template('dashboard.html', featured_properties=featured_properties, recent_listings=recent_listings)


@app.route('/search', methods=['GET', 'POST'])
def property_search():
    properties = load_properties()
    location_filter = ''
    price_min = None
    price_max = None
    property_type_filter = ''

    if request.method == 'POST':
        location_filter = request.form.get('location_input', '').strip()
        try:
            price_min = float(request.form.get('price_range_min', '') or 0)
        except ValueError:
            price_min = 0
        try:
            price_max = float(request.form.get('price_range_max', '') or float('inf'))
        except ValueError:
            price_max = float('inf')
        property_type_filter = request.form.get('property_type_filter', '').strip()

        filtered = []
        for p in properties:
            if p['status'] != 'Available':
                continue
            if location_filter and location_filter.lower() not in p['location'].lower():
                continue
            if p['price'] < price_min:
                continue
            if price_max != float('inf') and p['price'] > price_max:
                continue
            if property_type_filter and property_type_filter.lower() != p['property_type'].lower():
                continue
            filtered.append(p)
        properties = filtered
    else:
        # GET method: show all available properties unfiltered
        properties = [p for p in properties if p['status'] == 'Available']
        location_filter = ''
        price_min = 0
        price_max = float('inf')
        property_type_filter = ''

    return render_template('search.html', properties=properties, location_filter=location_filter, 
                           price_min=price_min if price_min is not None else 0,
                           price_max=price_max if price_max is not None else 0, 
                           property_type_filter=property_type_filter)


@app.route('/property/<int:property_id>', methods=['GET'])
def property_details(property_id):
    properties = load_properties()
    agents = load_agents()
    property_detail = None
    for p in properties:
        if p['property_id'] == property_id:
            property_detail = p
            break
    if property_detail is None:
        return "Property not found", 404
    # Find agent
    agent_detail = None
    for a in agents:
        if a['agent_id'] == property_detail['agent_id']:
            agent_detail = a
            break
    return render_template('property_details.html', property=property_detail, agent=agent_detail)


@app.route('/inquiry', methods=['GET', 'POST'])
def submit_inquiry():
    properties = load_properties()
    if request.method == 'POST':
        try:
            select_property = int(request.form.get('select_property', ''))
            inquiry_name = request.form.get('inquiry_name', '').strip()
            inquiry_email = request.form.get('inquiry_email', '').strip()
            inquiry_phone = request.form.get('inquiry_phone', '').strip()
            inquiry_message = request.form.get('inquiry_message', '').strip()

            # Validate required
            if not (select_property and inquiry_name and inquiry_email and inquiry_phone and inquiry_message):
                # Return form with error? Here just re-render
                return render_template('inquiry.html', properties=properties)

            # Check property exists and is Available or not sold
            property_found = None
            for p in properties:
                if p['property_id'] == select_property and p['status'] != 'Sold':
                    property_found = p
                    break
            if property_found is None:
                return render_template('inquiry.html', properties=properties)

            # Load inquiries
            inquiries = load_inquiries()
            # Determine next inquiry_id
            next_id = max([i['inquiry_id'] for i in inquiries], default=0) + 1
            now_str = datetime.datetime.now().strftime('%Y-%m-%d')
            new_inquiry = {
                'inquiry_id': next_id,
                'property_id': select_property,
                'customer_name': inquiry_name,
                'customer_email': inquiry_email,
                'customer_phone': inquiry_phone,
                'message': inquiry_message,
                'inquiry_date': now_str,
                'status': 'Pending'
            }
            inquiries.append(new_inquiry)
            save_inquiries(inquiries)

            # Usually redirect to inquiries page after submit
            return redirect(url_for('my_inquiries'))

        except ValueError:
            # invalid property id or parse error
            return render_template('inquiry.html', properties=properties)
    else:
        return render_template('inquiry.html', properties=properties)


@app.route('/inquiries', methods=['GET', 'POST'])
def my_inquiries():
    inquiries = load_inquiries()
    status_filter = ''

    if request.method == 'POST':
        # Form: inquiry_id for deletion
        try:
            inquiry_id = int(request.form.get('inquiry_id', ''))
            inquiries = [i for i in inquiries if i['inquiry_id'] != inquiry_id]
            save_inquiries(inquiries)
        except ValueError:
            pass

    # After possible deletion or GET, filter by status if any
    status_filter = request.args.get('status_filter', '')
    if status_filter:
        filtered = [i for i in inquiries if i['status'].lower() == status_filter.lower()]
    else:
        filtered = inquiries

    return render_template('inquiries.html', inquiries=filtered, status_filter=status_filter)


@app.route('/favorites', methods=['GET', 'POST'])
def my_favorites():
    favorites = load_favorites()
    properties = load_properties()

    if request.method == 'POST':
        # Remove favorite via property_id
        try:
            property_id = int(request.form.get('property_id', ''))
            favorites = [fav for fav in favorites if fav['property_id'] != property_id]
            save_favorites(favorites)
        except ValueError:
            pass

    # Prepare properties_map as dict property_id:int -> property dict
    properties_map = {p['property_id']: p for p in properties}

    return render_template('favorites.html', favorites=favorites, properties_map=properties_map)


@app.route('/agents', methods=['GET', 'POST'])
def agent_directory():
    agents = load_agents()
    agent_search_query = ''

    # The spec allows GET or POST for agent search
    if request.method == 'POST':
        agent_search_query = request.form.get('agent-search', '').strip()
    else:
        agent_search_query = request.args.get('agent-search', '').strip()

    if agent_search_query:
        agents = [a for a in agents if agent_search_query.lower() in a['agent_name'].lower()]

    return render_template('agents.html', agents=agents, agent_search_query=agent_search_query)


@app.route('/locations', methods=['GET', 'POST'])
def locations_page():
    locations = load_locations()
    sort_option = ''

    if request.method == 'POST':
        sort_option = request.form.get('location_sort', '').strip()
        # Sort options might be e.g. 'name_asc', 'name_desc', 'price_asc', 'price_desc', 'count_asc', 'count_desc'
        if sort_option == 'name_asc':
            locations.sort(key=lambda x: x['location_name'].lower())
        elif sort_option == 'name_desc':
            locations.sort(key=lambda x: x['location_name'].lower(), reverse=True)
        elif sort_option == 'price_asc':
            locations.sort(key=lambda x: x['average_price'])
        elif sort_option == 'price_desc':
            locations.sort(key=lambda x: x['average_price'], reverse=True)
        elif sort_option == 'count_asc':
            locations.sort(key=lambda x: x['property_count'])
        elif sort_option == 'count_desc':
            locations.sort(key=lambda x: x['property_count'], reverse=True)

    return render_template('locations.html', locations=locations, sort_option=sort_option)


if __name__ == '__main__':
    app.run(debug=True)
