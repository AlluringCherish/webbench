from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = '.'  # Assume data files are in current directory

# Helper function to read and parse pipe-delimited files given a filename and expected field count
# Returns list of records as lists of strings

def read_data_file(filename, expected_fields):
    filepath = os.path.join(DATA_DIR, filename)
    records = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) == expected_fields:
                    records.append(parts)
    except FileNotFoundError:
        # File missing; consider empty data
        pass
    except Exception as e:
        # In case of other errors, consider no data but could log
        pass
    return records

# 1. Load restaurants
# Fields: restaurant_id|name|cuisine|address|phone|rating|delivery_time|min_order

def load_restaurants():
    records = read_data_file('restaurants.txt', 8)
    restaurants = []
    for r in records:
        try:
            restaurant = {
                'restaurant_id': int(r[0]),
                'name': r[1],
                'cuisine': r[2],
                'address': r[3],
                'phone': r[4],
                'rating': float(r[5]),
                'delivery_time': int(r[6]),
                'min_order': float(r[7])
            }
            restaurants.append(restaurant)
        except Exception:
            # Skip invalid rows
            continue
    return restaurants

# 2. Load menus
# Fields: item_id|restaurant_id|item_name|category|description|price|availability

def load_menu_items():
    records = read_data_file('menus.txt',7)
    items = []
    for r in records:
        try:
            item = {
                'item_id': int(r[0]),
                'restaurant_id': int(r[1]),
                'item_name': r[2],
                'category': r[3],
                'description': r[4],
                'price': float(r[5]),
                'availability': int(r[6])
            }
            items.append(item)
        except Exception:
            continue
    return items

# 3. Load cart
# Fields: cart_id|item_id|restaurant_id|quantity|added_date

def load_cart_items():
    records = read_data_file('cart.txt', 5)
    cart_items = []
    for r in records:
        try:
            cart_item = {
                'cart_id': int(r[0]),
                'item_id': int(r[1]),
                'restaurant_id': int(r[2]),
                'quantity': int(r[3]),
                'added_date': r[4]
            }
            cart_items.append(cart_item)
        except Exception:
            continue
    return cart_items

# 4. Load orders
# Fields: order_id|customer_name|restaurant_id|order_date|total_amount|status|delivery_address|phone_number

def load_orders():
    records = read_data_file('orders.txt',8)
    orders = []
    for r in records:
        try:
            order = {
                'order_id': int(r[0]),
                'customer_name': r[1],
                'restaurant_id': int(r[2]),
                'order_date': r[3],
                'total_amount': float(r[4]),
                'status': r[5],
                'delivery_address': r[6],
                'phone_number': r[7]
            }
            orders.append(order)
        except Exception:
            continue
    return orders

# 5. Load order items
# Fields: order_item_id|order_id|item_id|quantity|price

def load_order_items():
    records = read_data_file('order_items.txt',5)
    order_items = []
    for r in records:
        try:
            oi = {
                'order_item_id': int(r[0]),
                'order_id': int(r[1]),
                'item_id': int(r[2]),
                'quantity': int(r[3]),
                'price': float(r[4])
            }
            order_items.append(oi)
        except Exception:
            continue
    return order_items

# 6. Load deliveries
# Fields: delivery_id|order_id|driver_name|driver_phone|vehicle_info|status|estimated_time

def load_deliveries():
    records = read_data_file('deliveries.txt',7)
    deliveries = []
    for r in records:
        try:
            d = {
                'delivery_id': int(r[0]),
                'order_id': int(r[1]),
                'driver_name': r[2],
                'driver_phone': r[3],
                'vehicle_info': r[4],
                'status': r[5],
                'estimated_time': r[6]
            }
            deliveries.append(d)
        except Exception:
            continue
    return deliveries

# 7. Load reviews
# Fields: review_id|restaurant_id|customer_name|rating|review_text|review_date

def load_reviews():
    records = read_data_file('reviews.txt', 6)
    reviews = []
    for r in records:
        try:
            rev = {
                'review_id': int(r[0]),
                'restaurant_id': int(r[1]),
                'customer_name': r[2],
                'rating': int(r[3]),
                'review_text': r[4],
                'review_date': r[5]
            }
            reviews.append(rev)
        except Exception:
            continue
    return reviews

# Specific Loaders that filter by key

def get_restaurant_by_id(restaurant_id):
    for r in load_restaurants():
        if r['restaurant_id'] == restaurant_id:
            return r
    return None


def get_menu_items_by_restaurant(restaurant_id):
    all_items = load_menu_items()
    return [item for item in all_items if item['restaurant_id'] == restaurant_id and item['availability'] == 1]


def get_item_by_id(item_id):
    for item in load_menu_items():
        if item['item_id'] == item_id:
            return item
    return None


def get_cart_items_with_details():
    cart_list = load_cart_items()
    cart_items = []
    total = 0.0
    for cart_item in cart_list:
        item = get_item_by_id(cart_item['item_id'])
        if not item or item['availability'] != 1:
            continue
        amount = item['price'] * cart_item['quantity']
        total += amount
        cart_items.append({
            'cart_id': cart_item['cart_id'],
            'item_id': item['item_id'],
            'item_name': item['item_name'],
            'category': item['category'],
            'description': item['description'],
            'price': item['price'],
            'quantity': cart_item['quantity'],
            'amount': amount
        })
    return cart_items, total


def get_orders_filtered(status_filter=None):
    orders = load_orders()
    if status_filter:
        orders = [o for o in orders if o['status'] == status_filter]
    return orders


def get_delivery_by_order(order_id):
    deliveries = load_deliveries()
    for d in deliveries:
        if d['order_id'] == order_id:
            return d
    return None


def get_order_items(order_id):
    order_items = load_order_items()
    items = []
    all_menu_items = load_menu_items()
    all_menu_items_dict = {item['item_id']: item for item in all_menu_items}
    for oi in order_items:
        if oi['order_id'] == order_id:
            menu_item = all_menu_items_dict.get(oi['item_id'])
            if not menu_item:
                continue
            items.append({
                'order_item_id': oi['order_item_id'],
                'item_id': oi['item_id'],
                'item_name': menu_item['item_name'],
                'quantity': oi['quantity'],
                'price': oi['price']
            })
    return items

# Order timeline stub (empty for now as no timeline data provided in spec)
def get_order_timeline(order_id):
    # For the sake of completeness, an empty list
    return []

# Filter reviews by restaurant

def get_reviews_for_restaurant(restaurant_id):
    reviews = load_reviews()
    return [r for r in reviews if r['restaurant_id'] == restaurant_id]

# Add a new review: append to reviews.txt

def add_review(restaurant_id, customer_name, rating, review_text):
    # Generate new review_id
    reviews = load_reviews()
    max_id = max((r['review_id'] for r in reviews), default=0)
    review_id = max_id + 1
    review_date = datetime.now().strftime('%Y-%m-%d')
    line = f"{review_id}|{restaurant_id}|{customer_name}|{rating}|{review_text}|{review_date}\n"
    try:
        with open(os.path.join(DATA_DIR, 'reviews.txt'), 'a', encoding='utf-8') as f:
            f.write(line)
        return True
    except Exception:
        return False

# New helper to get restaurant by id with safe fallback for tracking page
# We'll combine order info and delivery info

def get_order_and_delivery_details(order_id):
    orders = load_orders()
    deliveries = load_deliveries()
    order = None
    delivery = None
    for o in orders:
        if o['order_id'] == order_id:
            order = o
            break
    for d in deliveries:
        if d['order_id'] == order_id:
            delivery = d
            break
    # Compose combined dict for template
    details = {}
    if order:
        details['order_id'] = order['order_id']
        details['customer_name'] = order['customer_name']
        details['status'] = order['status']
        details['delivery_address'] = order['delivery_address']
        details['phone_number'] = order['phone_number']
    else:
        details['order_id'] = ''
        details['customer_name'] = ''
        details['status'] = ''
        details['delivery_address'] = ''
        details['phone_number'] = ''
    if delivery:
        details['driver_name'] = delivery['driver_name']
        details['driver_phone'] = delivery['driver_phone']
        details['vehicle_info'] = delivery['vehicle_info']
        details['estimated_time'] = delivery['estimated_time']
    else:
        details['driver_name'] = ''
        details['driver_phone'] = ''
        details['vehicle_info'] = ''
        details['estimated_time'] = ''
    return details

# Flask Routes

@app.route('/')
def redirect_dashboard():
    return redirect(url_for('dashboard_page'))

@app.route('/dashboard')
def dashboard_page():
    # featured_restaurants: Let's assume all restaurants with rating >=4.5
    restaurants = load_restaurants()
    featured = [r for r in restaurants if r['rating'] >= 4.5]
    return render_template('dashboard.html', featured_restaurants=featured)

@app.route('/restaurants')
def restaurants_page():
    # Provide all restaurants and no filter by default
    restaurants = load_restaurants()
    filter_type = request.args.get('filter_type', None)
    if filter_type:
        restaurants = [r for r in restaurants if r['cuisine'].lower() == filter_type.lower()]
    return render_template('restaurants.html', restaurant_list=restaurants, filter_type=filter_type)

@app.route('/menu/<int:restaurant_id>', methods=['GET','POST'])
def restaurant_menu_page(restaurant_id):
    restaurant_info = get_restaurant_by_id(restaurant_id)
    if not restaurant_info:
        return "Restaurant Not Found", 404

    # Handle POST to add to cart
    if request.method == 'POST':
        item_id = request.form.get('item_id')
        if item_id:
            try:
                item_id_int = int(item_id)
            except ValueError:
                return "Invalid item ID", 400
            # For demo, simulate adding to cart file (not writing actual cart in this scope)
            # Redirect back to same menu page
            return redirect(url_for('restaurant_menu_page', restaurant_id=restaurant_id))

    menu_items = get_menu_items_by_restaurant(restaurant_id)
    return render_template('menu.html', restaurant_info=restaurant_info, menu_items=menu_items)

@app.route('/item/<int:item_id>', methods=['GET','POST'])
def item_details_page(item_id):
    item_info = get_item_by_id(item_id)
    if not item_info or item_info['availability'] != 1:
        return "Item Not Found", 404

    # Handle POST to add to cart
    if request.method == 'POST':
        quantity = request.form.get('quantity')
        try:
            quantity_int = int(quantity)
            if quantity_int < 1:
                quantity_int = 1
        except (ValueError, TypeError):
            quantity_int = 1
        # For demo, simulate adding to cart file (not writing actual cart)
        # Redirect back to same item page
        return redirect(url_for('item_details_page', item_id=item_id))

    return render_template('item_details.html', item_info=item_info)

@app.route('/cart', methods=['GET', 'POST'])
def shopping_cart_page():
    # Support POST to update quantity or remove items
    if request.method == 'POST':
        # Remove item
        remove_item_id = request.form.get('remove_item_id')
        if remove_item_id:
            # Simulate removal (no persistence in this toy example)
            return redirect(url_for('shopping_cart_page'))

        # Update quantity for items
        # In real app, would update cart.txt accordingly
        # Simulate update then reload
        return redirect(url_for('shopping_cart_page'))

    cart_items, total_amount = get_cart_items_with_details()
    return render_template('cart.html', cart_items=cart_items, total_amount=total_amount)

@app.route('/checkout', methods=['GET','POST'])
def checkout_page():
    if request.method == 'POST':
        delivery_address = request.form.get('delivery_address')
        customer_name = request.form.get('customer_name')
        phone_number = request.form.get('phone_number')
        payment_method = request.form.get('payment_method')
        # No data save required per spec; redirect to orders page
        return redirect(url_for('orders_page'))
    # Get data for GET: pass empty or None
    return render_template('checkout.html', delivery_address='', customer_name='', phone_number='', payment_method='')

@app.route('/orders')
def orders_page():
    filter_status = request.args.get('filter_status', None)
    active_orders = get_orders_filtered(filter_status)
    if not active_orders:
        # Return 200 with empty list or 404 if no orders
        # To avoid 404 per feedback, return empty with message in template
        pass
    return render_template('active_orders.html', active_orders=active_orders, filter_status=filter_status)

@app.route('/tracking/<int:order_id>')
def tracking_page(order_id):
    details = get_order_and_delivery_details(order_id)
    if not details['order_id']:
        return "Order not found", 404
    order_items = get_order_items(order_id)
    estimated_time = details.get('estimated_time', '')
    order_timeline = get_order_timeline(order_id)
    return render_template('tracking.html', delivery_details=details, order_items=order_items, estimated_time=estimated_time, order_timeline=order_timeline)

@app.route('/reviews/<int:restaurant_id>', methods=['GET','POST'])
def reviews_page(restaurant_id):
    restaurant = get_restaurant_by_id(restaurant_id)
    if not restaurant:
        return "Restaurant Not Found", 404
    if request.method == 'POST':
        customer_name = request.form.get('customer_name')
        rating = request.form.get('rating')
        review_text = request.form.get('review_text')
        if not customer_name or not rating or not review_text:
            return "Missing review data", 400
        try:
            rating_int = int(rating)
            if rating_int < 1 or rating_int > 5:
                return "Invalid rating", 400
        except ValueError:
            return "Invalid rating", 400
        success = add_review(restaurant_id, customer_name, rating_int, review_text)
        if not success:
            return "Failed to add review", 500
        return redirect(url_for('reviews_page', restaurant_id=restaurant_id))
    reviews_list = get_reviews_for_restaurant(restaurant_id)
    restaurant_name = restaurant['name']
    return render_template('reviews.html', reviews_list=reviews_list, restaurant_name=restaurant_name)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
