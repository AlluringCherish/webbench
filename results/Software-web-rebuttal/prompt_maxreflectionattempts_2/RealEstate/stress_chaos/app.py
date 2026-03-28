from flask import Flask, render_template, redirect, url_for, request
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Utility functions to load and save data

def load_properties():
    properties = []
    try:
        with open(os.path.join(DATA_DIR, 'properties.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 11:
                    property = {
                        'property_id': int(parts[0]),
                        'address': parts[1],
                        'location': parts[2],
                        'price': float(parts[3]),
                        'property_type': parts[4],
                        'bedrooms': int(parts[5]),
                        'bathrooms': float(parts[6]),
                        'square_feet': int(parts[7]),
                        'description': parts[8],
                        'agent_id': int(parts[9]),
                        'status': parts[10]
                    }
                    properties.append(property)
    except IOError:
        pass
    return properties


def save_properties(properties):
    # Write back properties.txt if needed (not required currently) - placeholder
    pass


def load_locations():
    locations = []
    try:
        with open(os.path.join(DATA_DIR, 'locations.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 6:
                    location = {
                        'location_id': int(parts[0]),
                        'location_name': parts[1],
                        'region': parts[2],
                        'average_price': float(parts[3]),
                        'property_count': int(parts[4]),
                        'description': parts[5]
                    }
                    locations.append(location)
    except IOError:
        pass
    return locations


def load_inquiries():
    inquiries = []
    try:
        with open(os.path.join(DATA_DIR, 'inquiries.txt'), 'r', encoding='utf-8') as f:
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
    try:
        with open(os.path.join(DATA_DIR, 'inquiries.txt'), 'w', encoding='utf-8') as f:
            for iq in inquiries:
                line = f"{iq['inquiry_id']}|{iq['property_id']}|{iq['customer_name']}|{iq['customer_email']}|{iq['customer_phone']}|{iq['message']}|{iq['inquiry_date']}|{iq['status']}\n"
                f.write(line)
    except IOError:
        pass


def load_favorites():
    favorites = []
    try:
        with open(os.path.join(DATA_DIR, 'favorites.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 3:
                    favorite = {
                        'favorite_id': int(parts[0]),
                        'property_id': int(parts[1]),
                        'added_date': parts[2]
                    }
                    favorites.append(favorite)
    except IOError:
        pass
    return favorites


def save_favorites(favorites):
    try:
        with open(os.path.join(DATA_DIR, 'favorites.txt'), 'w', encoding='utf-8') as f:
            for fav in favorites:
                line = f"{fav['favorite_id']}|{fav['property_id']}|{fav['added_date']}\n"
                f.write(line)
    except IOError:
        pass


def load_agents():
    agents = []
    try:
        with open(os.path.join(DATA_DIR, 'agents.txt'), 'r', encoding='utf-8') as f:
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


@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    properties = load_properties()
    # featured_properties: let's consider featured as those Available and order by price descending top 5
    featured_properties = [p for p in properties if p['status'] == 'Available']
    featured_properties.sort(key=lambda x: x['price'], reverse=True)
    featured_properties = featured_properties[:5]

    # recent_listings: last 5 properties with status Available (assuming ordered by property_id descending as no date)
    available_properties = [p for p in properties if p['status'] == 'Available']
    available_properties.sort(key=lambda x: x['property_id'], reverse=True)
    recent_listings = available_properties[:5]

    return render_template('dashboard.html', featured_properties=featured_properties, recent_listings=recent_listings)


@app.route('/search', methods=['GET', 'POST'])
def property_search():
    properties = load_properties()
    filters = {'location': '', 'price_min': None, 'price_max': None, 'property_type': ''}

    if request.method == 'POST':
        location = request.form.get('location', '').strip()
        price_min_raw = request.form.get('price_min', '').strip()
        price_max_raw = request.form.get('price_max', '').strip()
        property_type = request.form.get('property_type', '').strip()

        # Parse price minimum
        try:
            price_min = int(price_min_raw) if price_min_raw != '' else None
        except ValueError:
            price_min = None

        # Parse price maximum
        try:
            price_max = int(price_max_raw) if price_max_raw != '' else None
        except ValueError:
            price_max = None

        filters['location'] = location
        filters['price_min'] = price_min
        filters['price_max'] = price_max
        filters['property_type'] = property_type

        filtered_properties = []
        for p in properties:
            if p['status'] != 'Available':
                continue
            if location and p['location'].lower() != location.lower():
                continue
            if price_min is not None and p['price'] < price_min:
                continue
            if price_max is not None and p['price'] > price_max:
                continue
            if property_type and p['property_type'].lower() != property_type.lower():
                continue
            filtered_properties.append(p)

        properties = filtered_properties
    else:
        # GET
        # Show all available properties default, no filters
        properties = [p for p in properties if p['status'] == 'Available']

    return render_template('search.html', properties=properties, filters=filters)


@app.route('/property/<int:property_id>')
def property_details(property_id):
    properties = load_properties()
    favorites = load_favorites()

    # Find property by id
    property = None
    for p in properties:
        if p['property_id'] == property_id:
            property = p
            break

    if property is None:
        # Not found, render with no context or 404? Spec not explicit. Let's render with None
        return render_template('property_details.html', property=None, is_favorite=False)

    is_favorite = any(f['property_id'] == property_id for f in favorites)

    return render_template('property_details.html', property=property, is_favorite=is_favorite)


@app.route('/inquiry', methods=['GET', 'POST'])
def property_inquiry():
    properties = load_properties()
    available_properties = [
        {'property_id': p['property_id'], 'address': p['address']}
        for p in properties if p['status'] == 'Available'
    ]

    if request.method == 'POST':
        try:
            property_id = int(request.form.get('property_id', ''))
            customer_name = request.form.get('customer_name', '').strip()
            customer_email = request.form.get('customer_email', '').strip()
            customer_phone = request.form.get('customer_phone', '').strip()
            message = request.form.get('message', '').strip()
            
            # Basic input validation
            if not customer_name or not customer_email or not property_id or not message:
                # Missing required fields, render page again with current
                return render_template('inquiry.html', properties=available_properties)

            inquiries = load_inquiries()
            # Create new inquiry_id
            max_id = max([iq['inquiry_id'] for iq in inquiries], default=0)
            inquiry_id = max_id + 1

            inquiry_date = datetime.now().strftime('%Y-%m-%d')
            new_inquiry = {
                'inquiry_id': inquiry_id,
                'property_id': property_id,
                'customer_name': customer_name,
                'customer_email': customer_email,
                'customer_phone': customer_phone,
                'message': message,
                'inquiry_date': inquiry_date,
                'status': 'Pending'
            }

            inquiries.append(new_inquiry)
            save_inquiries(inquiries)

            return redirect(url_for('my_inquiries'))
        except Exception:
            return render_template('inquiry.html', properties=available_properties)

    return render_template('inquiry.html', properties=available_properties)


@app.route('/inquiries', methods=['GET', 'POST'])
def my_inquiries():
    inquiries = load_inquiries()
    status_filter = ''

    if request.method == 'POST':
        # Deletion of inquiry by inquiry_id
        try:
            inquiry_id = int(request.form.get('inquiry_id', ''))
            inquiries = [iq for iq in inquiries if iq['inquiry_id'] != inquiry_id]
            save_inquiries(inquiries)
        except Exception:
            pass

    # GET and after POST - we support status filter query parameter for GET
    status_filter = request.args.get('status_filter', '')
    if status_filter:
        filtered = [iq for iq in inquiries if iq['status'].lower() == status_filter.lower()]
    else:
        filtered = inquiries

    return render_template('inquiries.html', inquiries=filtered, status_filter=status_filter)


@app.route('/favorites', methods=['GET', 'POST'])
def my_favorites():
    favorites = load_favorites()
    properties = load_properties()
    properties_map = {p['property_id']: p for p in properties}

    if request.method == 'POST':
        action = request.form.get('action', '')
        if action == 'remove':
            try:
                property_id = int(request.form.get('property_id', ''))
                favorites = [f for f in favorites if f['property_id'] != property_id]
                save_favorites(favorites)
            except Exception:
                pass

    return render_template('favorites.html', favorites=favorites, properties_map=properties_map)


@app.route('/agents')
def agent_directory():
    agents = load_agents()
    return render_template('agents.html', agents=agents)


@app.route('/locations')
def locations_page():
    locations = load_locations()
    sort_by = request.args.get('sort_by', '')

    if sort_by == 'price_asc':
        locations.sort(key=lambda x: x['average_price'])
    elif sort_by == 'price_desc':
        locations.sort(key=lambda x: x['average_price'], reverse=True)
    elif sort_by == 'count_asc':
        locations.sort(key=lambda x: x['property_count'])
    elif sort_by == 'count_desc':
        locations.sort(key=lambda x: x['property_count'], reverse=True)
    elif sort_by == 'name_asc':
        locations.sort(key=lambda x: x['location_name'].lower())
    elif sort_by == 'name_desc':
        locations.sort(key=lambda x: x['location_name'].lower(), reverse=True)

    return render_template('locations.html', locations=locations, sort_by=sort_by)


if __name__ == '__main__':
    app.run(debug=True)
