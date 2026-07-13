from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import date

app = Flask(__name__)

DATA_DIR = 'data'

# Helper functions to read and write data

def read_properties():
    props = []
    try:
        with open(os.path.join(DATA_DIR, 'properties.txt'), 'r') as f:
            for line in f:
                fields = line.strip().split('|')
                if len(fields) == 11:
                    prop = {
                        'property_id': int(fields[0]),
                        'address': fields[1],
                        'location': fields[2],
                        'price': int(fields[3]),
                        'property_type': fields[4],
                        'bedrooms': int(fields[5]),
                        'bathrooms': float(fields[6]),
                        'square_feet': int(fields[7]),
                        'description': fields[8],
                        'agent_id': int(fields[9]),
                        'status': fields[10]
                    }
                    props.append(prop)
    except FileNotFoundError:
        pass
    return props


def read_locations():
    locs = []
    try:
        with open(os.path.join(DATA_DIR, 'locations.txt'), 'r') as f:
            for line in f:
                fields = line.strip().split('|')
                if len(fields) == 6:
                    loc = {
                        'location_id': int(fields[0]),
                        'location_name': fields[1],
                        'region': fields[2],
                        'average_price': int(fields[3]),
                        'property_count': int(fields[4]),
                        'description': fields[5]
                    }
                    locs.append(loc)
    except FileNotFoundError:
        pass
    return locs


def read_inquiries():
    inquiries = []
    try:
        with open(os.path.join(DATA_DIR, 'inquiries.txt'), 'r') as f:
            for line in f:
                fields = line.strip().split('|')
                if len(fields) == 8:
                    inq = {
                        'inquiry_id': int(fields[0]),
                        'property_id': int(fields[1]),
                        'customer_name': fields[2],
                        'customer_email': fields[3],
                        'customer_phone': fields[4],
                        'message': fields[5],
                        'inquiry_date': fields[6],
                        'status': fields[7]
                    }
                    inquiries.append(inq)
    except FileNotFoundError:
        pass
    return inquiries


def read_favorites():
    favorites = []
    try:
        with open(os.path.join(DATA_DIR, 'favorites.txt'), 'r') as f:
            for line in f:
                fields = line.strip().split('|')
                if len(fields) == 3:
                    fav = {
                        'favorite_id': int(fields[0]),
                        'property_id': int(fields[1]),
                        'added_date': fields[2]
                    }
                    favorites.append(fav)
    except FileNotFoundError:
        pass
    return favorites


def read_agents():
    agents = []
    try:
        with open(os.path.join(DATA_DIR, 'agents.txt'), 'r') as f:
            for line in f:
                fields = line.strip().split('|')
                if len(fields) == 6:
                    agent = {
                        'agent_id': int(fields[0]),
                        'agent_name': fields[1],
                        'specialization': fields[2],
                        'email': fields[3],
                        'phone': fields[4],
                        'properties_sold': int(fields[5])
                    }
                    agents.append(agent)
    except FileNotFoundError:
        pass
    return agents

# Writing functions

def write_inquiries(inquiries):
    with open(os.path.join(DATA_DIR, 'inquiries.txt'), 'w') as f:
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


def write_favorites(favorites):
    with open(os.path.join(DATA_DIR, 'favorites.txt'), 'w') as f:
        for fav in favorites:
            line = '|'.join([
                str(fav['favorite_id']),
                str(fav['property_id']),
                fav['added_date']
            ])
            f.write(line + '\n')

# Routes

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard_page'))


@app.route('/dashboard')
def dashboard_page():
    # For demo, featured properties can be ones with status Available and price descending
    properties = read_properties()
    featured_properties = sorted(
        [p for p in properties if p['status'].lower() == 'available'],
        key=lambda x: x['price'], reverse=True
    )[:5]
    return render_template('dashboard.html', featured_properties=featured_properties)


@app.route('/properties/search', methods=['GET', 'POST'])
def property_search_page():
    properties = read_properties()
    filters = {
        'location': '',
        'price_min': '',
        'price_max': '',
        'property_type': ''
    }
    filtered_props = properties
    if request.method == 'POST':
        location = request.form.get('location-input', '').strip().lower()
        price_min = request.form.get('price-range-min', '').strip()
        price_max = request.form.get('price-range-max', '').strip()
        property_type = request.form.get('property-type-filter', '').strip()

        filters['location'] = location
        filters['price_min'] = price_min
        filters['price_max'] = price_max
        filters['property_type'] = property_type

        def matches(p):
            if location and location not in p['location'].lower():
                return False
            if property_type and property_type.lower() != p['property_type'].lower():
                return False
            if price_min:
                try:
                    if p['price'] < int(price_min):
                        return False
                except:
                    pass
            if price_max:
                try:
                    if p['price'] > int(price_max):
                        return False
                except:
                    pass
            if p['status'].lower() != 'available':
                return False
            return True

        filtered_props = [p for p in properties if matches(p)]

    return render_template('property_search.html', properties=filtered_props, filters=filters)


@app.route('/properties/<int:property_id>', methods=['GET', 'POST'])
def property_details_page(property_id):
    properties = read_properties()
    favorites = read_favorites()
    prop = next((p for p in properties if p['property_id'] == property_id), None)
    if prop is None:
        return "Property not found", 404
    favorite_status = any(f['property_id'] == property_id for f in favorites)

    if request.method == 'POST':
        # Add to favorites
        if not favorite_status:
            max_fav_id = max([f['favorite_id'] for f in favorites], default=0)
            new_fav = {
                'favorite_id': max_fav_id + 1,
                'property_id': property_id,
                'added_date': date.today().isoformat()
            }
            favorites.append(new_fav)
            write_favorites(favorites)
            favorite_status = True
        return redirect(url_for('property_details_page', property_id=property_id))

    return render_template('property_details.html', property=prop, favorite_status=favorite_status)


@app.route('/inquiries/submit', methods=['GET', 'POST'])
def property_inquiry_page():
    properties = read_properties()
    inquiry_submitted = False
    preselected_property_id = request.args.get('property_id', type=int)

    if request.method == 'POST':
        property_id = int(request.form.get('select-property', 0))
        customer_name = request.form.get('inquiry-name', '').strip()
        customer_email = request.form.get('inquiry-email', '').strip()
        customer_phone = request.form.get('inquiry-phone', '').strip()
        message = request.form.get('inquiry-message', '').strip()

        if property_id and customer_name and customer_email and message:
            inquiries = read_inquiries()
            max_inquiry_id = max([i['inquiry_id'] for i in inquiries], default=0)
            new_inquiry = {
                'inquiry_id': max_inquiry_id + 1,
                'property_id': property_id,
                'customer_name': customer_name,
                'customer_email': customer_email,
                'customer_phone': customer_phone,
                'message': message,
                'inquiry_date': date.today().isoformat(),
                'status': 'Pending'
            }
            inquiries.append(new_inquiry)
            write_inquiries(inquiries)
            inquiry_submitted = True
        else:
            inquiry_submitted = False

    return render_template('property_inquiry.html', properties=properties, inquiry_submitted=inquiry_submitted, preselected_property_id=preselected_property_id)


@app.route('/inquiries', methods=['GET', 'POST'])
def my_inquiries_page():
    inquiries = read_inquiries()
    properties = {p['property_id']: p for p in read_properties()}
    status_filter = request.args.get('inquiry-status-filter', 'All')
    
    if request.method == 'POST':
        status_filter = request.form.get('inquiry-status-filter', 'All')

    if status_filter and status_filter != 'All':
        filtered_inquiries = [i for i in inquiries if i['status'] == status_filter]
    else:
        filtered_inquiries = inquiries

    # Augment inquiries with property address
    for inq in filtered_inquiries:
        prop = properties.get(inq['property_id'])
        inq['property_address'] = prop['address'] if prop else 'Unknown'

    return render_template('my_inquiries.html', inquiries=filtered_inquiries, status_filter=status_filter)


@app.route('/inquiries/delete/<int:inquiry_id>', methods=['POST'])
def delete_inquiry(inquiry_id):
    inquiries = read_inquiries()
    inquiries = [i for i in inquiries if i['inquiry_id'] != inquiry_id]
    write_inquiries(inquiries)
    return redirect(url_for('my_inquiries_page'))


@app.route('/favorites', methods=['GET', 'POST'])
def my_favorites_page():
    favorites = read_favorites()
    properties = {p['property_id']: p for p in read_properties()}

    if request.method == 'POST':
        # Remove from favorites handled in separate route
        pass

    fav_props = []
    for fav in favorites:
        prop = properties.get(fav['property_id'])
        if prop:
            combined = {
                'favorite_id': fav['favorite_id'],
                'property_id': fav['property_id'],
                'address': prop['address'],
                'price': prop['price']
            }
            fav_props.append(combined)

    return render_template('my_favorites.html', favorites=fav_props)


@app.route('/favorites/remove/<int:property_id>', methods=['POST'])
def remove_favorite(property_id):
    favorites = read_favorites()
    favorites = [f for f in favorites if f['property_id'] != property_id]
    write_favorites(favorites)
    return redirect(url_for('my_favorites_page'))


@app.route('/agents')
def agent_directory_page():
    agents = read_agents()
    search_query = request.args.get('agent-search', '').strip().lower()
    if search_query:
        filtered_agents = [a for a in agents if search_query in a['agent_name'].lower()]
    else:
        filtered_agents = agents
    return render_template('agents.html', agents=filtered_agents, search_query=search_query)


@app.route('/locations')
def locations_page():
    locations = read_locations()
    sort_by = request.args.get('location-sort', 'By Name')
    if sort_by == 'By Properties Count':
        locations.sort(key=lambda x: x['property_count'], reverse=True)
    elif sort_by == 'By Average Price':
        locations.sort(key=lambda x: x['average_price'], reverse=True)
    else:  # By Name default
        locations.sort(key=lambda x: x['location_name'])
    return render_template('locations.html', locations=locations, sort_by=sort_by)


@app.route('/locations/<int:location_id>/properties')
def location_properties_page(location_id):
    locations = read_locations()
    location = next((loc for loc in locations if loc['location_id'] == location_id), None)
    if location is None:
        return "Location not found", 404
    properties = [p for p in read_properties() if p['location'] == location['location_name'] and p['status'].lower() == 'available']
    return render_template('properties_by_location.html', location=location, properties=properties)


if __name__ == '__main__':
    app.run(debug=True)
