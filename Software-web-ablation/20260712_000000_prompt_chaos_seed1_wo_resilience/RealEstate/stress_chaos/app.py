from flask import Flask, render_template, redirect, url_for, request
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Utility functions for loading data from files according to schema

def load_properties():
    properties = []
    path = os.path.join(DATA_DIR, 'properties.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 11:
                    property_dict = {
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
                    properties.append(property_dict)
    except FileNotFoundError:
        pass
    return properties


def load_locations():
    locations = []
    path = os.path.join(DATA_DIR, 'locations.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 6:
                    location_dict = {
                        'location_id': int(parts[0]),
                        'location_name': parts[1],
                        'region': parts[2],
                        'average_price': int(parts[3]),
                        'property_count': int(parts[4]),
                        'description': parts[5]
                    }
                    locations.append(location_dict)
    except FileNotFoundError:
        pass
    return locations


def load_inquiries():
    inquiries = []
    path = os.path.join(DATA_DIR, 'inquiries.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 8:
                    inquiry_dict = {
                        'inquiry_id': int(parts[0]),
                        'property_id': int(parts[1]),
                        'customer_name': parts[2],
                        'customer_email': parts[3],
                        'customer_phone': parts[4],
                        'message': parts[5],
                        'inquiry_date': parts[6],  # YYYY-MM-DD
                        'status': parts[7]
                    }
                    inquiries.append(inquiry_dict)
    except FileNotFoundError:
        pass
    return inquiries


def save_inquiries(inquiries):
    path = os.path.join(DATA_DIR, 'inquiries.txt')
    lines = []
    for inquiry in inquiries:
        line = f"{inquiry['inquiry_id']}|{inquiry['property_id']}|{inquiry['customer_name']}|{inquiry['customer_email']}|{inquiry['customer_phone']}|{inquiry['message']}|{inquiry['inquiry_date']}|{inquiry['status']}"
        lines.append(line)
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))


def load_favorites():
    favorites = []
    path = os.path.join(DATA_DIR, 'favorites.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 3:
                    favorite_dict = {
                        'favorite_id': int(parts[0]),
                        'property_id': int(parts[1]),
                        'added_date': parts[2]
                    }
                    favorites.append(favorite_dict)
    except FileNotFoundError:
        pass
    return favorites


def save_favorites(favorites):
    path = os.path.join(DATA_DIR, 'favorites.txt')
    lines = []
    for fav in favorites:
        line = f"{fav['favorite_id']}|{fav['property_id']}|{fav['added_date']}"
        lines.append(line)
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))


def load_agents():
    agents = []
    path = os.path.join(DATA_DIR, 'agents.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 6:
                    agent_dict = {
                        'agent_id': int(parts[0]),
                        'agent_name': parts[1],
                        'specialization': parts[2],
                        'email': parts[3],
                        'phone': parts[4],
                        'properties_sold': int(parts[5])
                    }
                    agents.append(agent_dict)
    except FileNotFoundError:
        pass
    return agents


# ROUTES

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard_page'))


@app.route('/dashboard')
def dashboard_page():
    properties = load_properties()
    # Featured properties: for example, pick those that are Available and of lowest property_id (as sample logic)
    featured_properties = [p for p in properties if p['status'] == 'Available']
    featured_properties = sorted(featured_properties, key=lambda x: x['property_id'])[:5]

    # Recent listings: properties sorted by property_id descending (simulate recency)
    recent_listings = sorted(properties, key=lambda x: x['property_id'], reverse=True)[:5]

    return render_template('dashboard.html', featured_properties=featured_properties, recent_listings=recent_listings)


@app.route('/properties/search', methods=['GET', 'POST'])
def property_search_page():
    properties = load_properties()
    if request.method == 'POST':
        # Retrieve form data
        location = request.form.get('location', '').strip()
        price_min = request.form.get('price_min', '')
        price_max = request.form.get('price_max', '')
        property_type = request.form.get('property_type', '').strip()

        # Convert prices to int or None
        try:
            price_min_val = int(price_min) if price_min else None
        except ValueError:
            price_min_val = None
        try:
            price_max_val = int(price_max) if price_max else None
        except ValueError:
            price_max_val = None

        # Filter properties
        filtered_properties = []
        for p in properties:
            if p['status'] != 'Available':
                continue
            if location and location.lower() not in p['location'].lower():
                continue
            if property_type and property_type.lower() != p['property_type'].lower():
                continue
            if (price_min_val is not None and p['price'] < price_min_val):
                continue
            if (price_max_val is not None and p['price'] > price_max_val):
                continue
            filtered_properties.append(p)

        search_filters = {
            'location': location,
            'price_min': price_min,
            'price_max': price_max,
            'property_type': property_type
        }

        return render_template('property_search.html', properties=properties, filtered_properties=filtered_properties, search_filters=search_filters)
    else:
        return render_template('property_search.html', properties=properties)


@app.route('/properties/<int:property_id>')
def property_details_page(property_id):
    properties = load_properties()
    property_match = next((p for p in properties if p['property_id'] == property_id), None)
    if not property_match:
        # Could return 404 or render a not found page; here redirect to search
        return redirect(url_for('property_search_page'))
    return render_template('property_details.html', property=property_match)


@app.route('/inquiries/new', methods=['GET', 'POST'])
def property_inquiry_page():
    properties = load_properties()
    if request.method == 'POST':
        try:
            property_id = int(request.form['property_id'])
            customer_name = request.form['customer_name'].strip()
            customer_email = request.form['customer_email'].strip()
            customer_phone = request.form['customer_phone'].strip()
            message = request.form['message'].strip()

            # Validate property exists
            if not any(p['property_id'] == property_id for p in properties):
                return render_template('property_inquiry.html', properties=properties, error='Invalid property selected.')

            # Prepare new inquiry
            inquiries = load_inquiries()
            max_id = max((inq['inquiry_id'] for inq in inquiries), default=0)
            new_inquiry = {
                'inquiry_id': max_id + 1,
                'property_id': property_id,
                'customer_name': customer_name,
                'customer_email': customer_email,
                'customer_phone': customer_phone,
                'message': message,
                'inquiry_date': datetime.now().strftime('%Y-%m-%d'),
                'status': 'Pending'
            }
            inquiries.append(new_inquiry)
            save_inquiries(inquiries)

            return redirect(url_for('inquiries_page'))
        except (KeyError, ValueError):
            return render_template('property_inquiry.html', properties=properties, error='Invalid form submission.')
    else:
        return render_template('property_inquiry.html', properties=properties)


@app.route('/inquiries')
def inquiries_page():
    inquiries = load_inquiries()
    inquiry_status_filter = request.args.get('inquiry_status_filter', 'All')

    if inquiry_status_filter != 'All':
        inquiries = [inq for inq in inquiries if inq['status'] == inquiry_status_filter]

    return render_template('inquiries.html', inquiries=inquiries, inquiry_status_filter=inquiry_status_filter)


@app.route('/inquiries/delete/<int:inquiry_id>', methods=['POST'])
def delete_inquiry(inquiry_id):
    inquiries = load_inquiries()
    inquiries = [inq for inq in inquiries if inq['inquiry_id'] != inquiry_id]
    save_inquiries(inquiries)
    return redirect(url_for('inquiries_page'))


@app.route('/favorites')
def favorites_page():
    favorites = load_favorites()
    properties = load_properties()

    # Match favorite properties details
    favorite_properties = []
    prop_dict = {p['property_id']: p for p in properties}
    for fav in favorites:
        prop = prop_dict.get(fav['property_id'])
        if prop:
            favorite_properties.append(prop)

    return render_template('favorites.html', favorites=favorites, favorite_properties=favorite_properties)


@app.route('/favorites/add/<int:property_id>', methods=['POST'])
def add_to_favorites(property_id):
    favorites = load_favorites()

    if not any(fav['property_id'] == property_id for fav in favorites):
        max_id = max((fav['favorite_id'] for fav in favorites), default=0)
        new_fav = {
            'favorite_id': max_id + 1,
            'property_id': property_id,
            'added_date': datetime.now().strftime('%Y-%m-%d')
        }
        favorites.append(new_fav)
        save_favorites(favorites)

    return redirect(url_for('favorites_page'))


@app.route('/favorites/remove/<int:property_id>', methods=['POST'])
def remove_from_favorites(property_id):
    favorites = load_favorites()
    favorites = [fav for fav in favorites if fav['property_id'] != property_id]
    save_favorites(favorites)
    return redirect(url_for('favorites_page'))


@app.route('/agents')
def agents_page():
    agents = load_agents()
    return render_template('agents.html', agents=agents)


@app.route('/locations')
def locations_page():
    locations = load_locations()
    sort_option = request.args.get('sort_option', 'name')

    if sort_option == 'name':
        locations = sorted(locations, key=lambda l: l['location_name'].lower())
    elif sort_option == 'count':
        locations = sorted(locations, key=lambda l: l['property_count'], reverse=True)
    elif sort_option == 'average price':
        locations = sorted(locations, key=lambda l: l['average_price'], reverse=True)

    return render_template('locations.html', locations=locations, sort_option=sort_option)


if __name__ == '__main__':
    app.run(debug=True)
