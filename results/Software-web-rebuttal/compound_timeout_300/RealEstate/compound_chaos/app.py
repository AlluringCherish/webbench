from flask import Flask, render_template, redirect, url_for, request
from datetime import date

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

# Data loading and saving utility functions

def load_properties():
    props = []
    try:
        with open('data/properties.txt', 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 11:
                    continue
                try:
                    prop = {
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
                    props.append(prop)
                except Exception:
                    continue
    except FileNotFoundError:
        pass
    return props


def load_locations():
    locs = []
    try:
        with open('data/locations.txt', 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 6:
                    continue
                try:
                    loc = {
                        'location_id': int(parts[0]),
                        'location_name': parts[1],
                        'region': parts[2],
                        'average_price': float(parts[3]),
                        'property_count': int(parts[4]),
                        'description': parts[5]
                    }
                    locs.append(loc)
                except Exception:
                    continue
    except FileNotFoundError:
        pass
    return locs


def load_inquiries():
    inqs = []
    try:
        with open('data/inquiries.txt', 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 8:
                    continue
                try:
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
                    inqs.append(inq)
                except Exception:
                    continue
    except FileNotFoundError:
        pass
    return inqs


def save_inquiries(inquiries):
    try:
        with open('data/inquiries.txt', 'w', encoding='utf-8') as f:
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
    except IOError:
        pass


def load_favorites():
    favs = []
    try:
        with open('data/favorites.txt', 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 3:
                    continue
                try:
                    fav = {
                        'favorite_id': int(parts[0]),
                        'property_id': int(parts[1]),
                        'added_date': parts[2]
                    }
                    favs.append(fav)
                except Exception:
                    continue
    except FileNotFoundError:
        pass
    return favs


def save_favorites(favorites):
    try:
        with open('data/favorites.txt', 'w', encoding='utf-8') as f:
            for fav in favorites:
                line = '|'.join([
                    str(fav['favorite_id']),
                    str(fav['property_id']),
                    fav['added_date']
                ])
                f.write(line + '\n')
    except IOError:
        pass


def load_agents():
    agents = []
    try:
        with open('data/agents.txt', 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 6:
                    continue
                try:
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
                    continue
    except FileNotFoundError:
        pass
    return agents


# Root route
@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard_page'))


# Dashboard Page
@app.route('/dashboard')
def dashboard_page():
    properties = load_properties()
    featured_properties = [p for p in properties if p['status'] == 'Available'][:3]
    recent_listings = sorted([p for p in properties if p['status'] == 'Available'], key=lambda x: x['property_id'], reverse=True)[:5]
    featured_properties_ctx = [{
        'property_id': p['property_id'],
        'address': p['address'],
        'price': p['price'],
        'bedrooms': p['bedrooms'],
        'bathrooms': p['bathrooms']
    } for p in featured_properties]
    recent_listings_ctx = [{
        'property_id': p['property_id'],
        'address': p['address'],
        'price': p['price'],
        'bedrooms': p['bedrooms'],
        'bathrooms': p['bathrooms']
    } for p in recent_listings]
    return render_template('dashboard.html', featured_properties=featured_properties_ctx, recent_listings=recent_listings_ctx)


# Property Search
@app.route('/search')
def property_search():
    properties = load_properties()
    available_properties = [p for p in properties if p['status'] == 'Available']
    properties_ctx = [{
        'property_id': p['property_id'],
        'address': p['address'],
        'location': p['location'],
        'price': p['price'],
        'property_type': p['property_type'],
        'bedrooms': p['bedrooms'],
        'bathrooms': p['bathrooms'],
        'square_feet': p['square_feet']
    } for p in available_properties]
    property_types = ['House', 'Apartment', 'Condo', 'Land']
    return render_template('search.html', properties=properties_ctx, property_types=property_types)


# Property Details
@app.route('/property/<int:property_id>')
def property_details(property_id):
    properties = load_properties()
    prop = next((p for p in properties if p['property_id'] == property_id), None)
    if not prop:
        return redirect(url_for('property_search'))
    property_ctx = {
        'property_id': prop['property_id'],
        'address': prop['address'],
        'price': prop['price'],
        'description': prop['description'],
        'bedrooms': prop['bedrooms'],
        'bathrooms': prop['bathrooms'],
        'square_feet': prop['square_feet']
    }
    return render_template('property_details.html', property=property_ctx)


# Property Inquiry GET
@app.route('/inquiry', methods=['GET'])
def property_inquiry():
    properties = load_properties()
    available = [p for p in properties if p['status'] == 'Available']
    properties_ctx = [{'property_id': p['property_id'], 'address': p['address']} for p in available]
    return render_template('inquiry.html', properties=properties_ctx)


# Property Inquiry POST
@app.route('/inquiry', methods=['POST'])
def submit_inquiry():
    property_id_raw = request.form.get('property_id')
    inquiry_name = request.form.get('inquiry_name', '').strip()
    inquiry_email = request.form.get('inquiry_email', '').strip()
    inquiry_phone = request.form.get('inquiry_phone', '').strip()
    inquiry_message = request.form.get('inquiry_message', '').strip()

    try:
        property_id = int(property_id_raw)
    except (TypeError, ValueError):
        property_id = None

    properties = load_properties()
    valid_property = any(p['property_id'] == property_id and p['status'] == 'Available' for p in properties)
    if not (property_id and valid_property and inquiry_name and inquiry_email and inquiry_phone and inquiry_message):
        # Re-render inquiry with properties on failure
        available = [p for p in properties if p['status'] == 'Available']
        properties_ctx = [{'property_id': p['property_id'], 'address': p['address']} for p in available]
        return render_template('inquiry.html', properties=properties_ctx)

    inquiries = load_inquiries()
    next_id = max((i['inquiry_id'] for i in inquiries), default=0) + 1
    today = date.today().isoformat()
    new_inquiry = {
        'inquiry_id': next_id,
        'property_id': property_id,
        'customer_name': inquiry_name,
        'customer_email': inquiry_email,
        'customer_phone': inquiry_phone,
        'message': inquiry_message,
        'inquiry_date': today,
        'status': 'Pending'
    }
    inquiries.append(new_inquiry)
    save_inquiries(inquiries)
    return redirect(url_for('my_inquiries_page'))


# My Inquiries page
@app.route('/my-inquiries')
def my_inquiries_page():
    status_filter = request.args.get('status_filter', 'All')
    inquiries = load_inquiries()
    properties = load_properties()
    property_address_map = {p['property_id']: p['address'] for p in properties}

    if status_filter != 'All':
        filtered_inquiries = [i for i in inquiries if i['status'] == status_filter]
    else:
        filtered_inquiries = inquiries

    inquiries_ctx = [{
        'inquiry_id': i['inquiry_id'],
        'property_id': i['property_id'],
        'property_address': property_address_map.get(i['property_id'], 'Unknown'),
        'inquiry_date': i['inquiry_date'],
        'status': i['status'],
        'customer_name': i['customer_name'],
        'customer_email': i['customer_email'],
        'customer_phone': i['customer_phone']
    } for i in filtered_inquiries]

    return render_template('my_inquiries.html', inquiries=inquiries_ctx, status_filter=status_filter)


# Delete Inquiry POST
@app.route('/my-inquiries/delete/<int:inquiry_id>', methods=['POST'])
def delete_inquiry(inquiry_id):
    inquiries = load_inquiries()
    inquiries = [i for i in inquiries if i['inquiry_id'] != inquiry_id]
    save_inquiries(inquiries)
    return redirect(url_for('my_inquiries_page'))


# My Favorites Page
@app.route('/my-favorites')
def my_favorites_page():
    favorites = load_favorites()
    properties = load_properties()
    property_map = {p['property_id']: p for p in properties}

    favorites_ctx = []
    for fav in favorites:
        prop = property_map.get(fav['property_id'])
        if prop and prop['status'] == 'Available':
            favorites_ctx.append({
                'property_id': prop['property_id'],
                'address': prop['address'],
                'price': prop['price'],
                'bedrooms': prop['bedrooms'],
                'bathrooms': prop['bathrooms']
            })

    return render_template('my_favorites.html', favorites=favorites_ctx)


# Remove Favorite POST
@app.route('/my-favorites/remove/<int:property_id>', methods=['POST'])
def remove_favorite(property_id):
    favorites = load_favorites()
    favorites = [f for f in favorites if f['property_id'] != property_id]
    save_favorites(favorites)
    return redirect(url_for('my_favorites_page'))


# Agents Directory
@app.route('/agents')
def agent_directory():
    agents = load_agents()
    agents_ctx = [{
        'agent_id': a['agent_id'],
        'agent_name': a['agent_name'],
        'specialization': a['specialization'],
        'email': a['email'],
        'phone': a['phone']
    } for a in agents]
    return render_template('agents.html', agents=agents_ctx)


# Locations Page
@app.route('/locations')
def locations_page():
    locations = load_locations()
    return render_template('locations.html', locations=locations)


if __name__ == '__main__':
    app.run(debug=True)
