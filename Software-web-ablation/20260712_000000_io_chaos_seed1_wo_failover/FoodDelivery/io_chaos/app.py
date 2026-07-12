from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Utility functions to load data from text files

def load_restaurants():
    restaurants = {}
    try:
        with open(os.path.join(DATA_DIR, 'restaurants.txt'), encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 8:
                    r_id, name, cuisine, address, phone, rating, delivery_time, min_order = parts
                    restaurants[int(r_id)] = {
                        'restaurant_id': int(r_id),
                        'name': name,
                        'cuisine': cuisine,
                        'address': address,
                        'phone': phone,
                        'rating': float(rating),
                        'delivery_time': int(delivery_time),
                        'min_order': float(min_order)
                    }
    except Exception as e:
        pass
    return restaurants

def load_menus():
    menus = {}
    try:
        with open(os.path.join(DATA_DIR, 'menus.txt'), encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 7:
                    item_id, r_id, item_name, category, description, price, availability = parts
                    menus[int(item_id)] = {
                        'item_id': int(item_id),
                        'restaurant_id': int(r_id),
                        'item_name': item_name,
                        'category': category,
                        'description': description,
                        'price': float(price),
                        'availability': availability == '1'
                    }
    except Exception as e:
        pass
    return menus

def load_cart():
    cart = {}
    try:
        with open(os.path.join(DATA_DIR, 'cart.txt'), encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 5:
                    cart_id, item_id, r_id, quantity, added_date = parts
                    cart[int(item_id)] = {
                        'cart_id': int(cart_id),
                        'item_id': int(item_id),
                        'restaurant_id': int(r_id),
                        'quantity': int(quantity),
                        'added_date': added_date
                    }
    except Exception as e:
        pass
    return cart

def save_cart(cart):
    try:
        with open(os.path.join(DATA_DIR, 'cart.txt'), 'w', encoding='utf-8') as f:
            for item in cart.values():
                f.write(f"{item['cart_id']}|{item['item_id']}|{item['restaurant_id']}|{item['quantity']}|{item['added_date']}\n")
    except Exception as e:
        pass

def load_orders():
    orders = {}
    try:
        with open(os.path.join(DATA_DIR, 'orders.txt'), encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 8:
                    order_id, customer_name, restaurant_id, order_date, total_amount, status, delivery_address, phone_number = parts
                    orders[int(order_id)] = {
                        'order_id': int(order_id),
                        'customer_name': customer_name,
                        'restaurant_id': int(restaurant_id),
                        'order_date': order_date,
                        'total_amount': float(total_amount),
                        'status': int(status),
                        'delivery_address': delivery_address,
                        'phone_number': phone_number
                    }
    except Exception as e:
        pass
    return orders

def load_order_items():
    order_items = {}
    try:
        with open(os.path.join(DATA_DIR, 'order_items.txt'), encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 5:
                    order_item_id, order_id, item_id, quantity, price = parts
                    order_id_i = int(order_id)
                    if order_id_i not in order_items:
                        order_items[order_id_i] = []
                    order_items[order_id_i].append({
                        'order_item_id': int(order_item_id),
                        'item_id': int(item_id),
                        'quantity': int(quantity),
                        'price': float(price)
                    })
    except Exception as e:
        pass
    return order_items

def load_deliveries():
    deliveries = {}
    try:
        with open(os.path.join(DATA_DIR, 'deliveries.txt'), encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 7:
                    delivery_id, order_id, driver_name, driver_phone, vehicle_info, status, estimated_time = parts
                    deliveries[int(order_id)] = {
                        'delivery_id': int(delivery_id),
                        'order_id': int(order_id),
                        'driver_name': driver_name,
                        'driver_phone': driver_phone,
                        'vehicle_info': vehicle_info,
                        'status': status,
                        'estimated_time': estimated_time
                    }
    except Exception as e:
        pass
    return deliveries

def load_reviews():
    reviews = {}
    try:
        with open(os.path.join(DATA_DIR, 'reviews.txt'), encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 6:
                    review_id, restaurant_id, customer_name, rating, review_text, review_date = parts
                    rid = int(restaurant_id)
                    if rid not in reviews:
                        reviews[rid] = []
                    reviews[rid].append({
                        'review_id': int(review_id),
                        'customer_name': customer_name,
                        'rating': int(rating),
                        'review_text': review_text,
                        'review_date': review_date
                    })
    except Exception as e:
        pass
    return reviews

@app.route('/')
def dashboard():
    restaurants = load_restaurants()
    # Featured restaurants by rating descending top 3
    featured_restaurants = sorted(restaurants.values(), key=lambda r: r['rating'], reverse=True)[:3]
    return render_template('dashboard.html', featured_restaurants=featured_restaurants)

@app.route('/restaurants')
def browse_restaurants():
    restaurants = load_restaurants()
    cuisines = set(r['cuisine'] for r in restaurants.values())
    # unique cuisines for filter
    cuisine_list = [{'id': idx+1, 'name': c} for idx, c in enumerate(sorted(cuisines))]

    search_query = request.args.get('search_query', '').lower()
    selected_cuisine = request.args.get('cuisinefilter', '')

    filtered_restaurants = []
    for r in restaurants.values():
        if search_query in r['name'].lower() or search_query in r['cuisine'].lower():
            if selected_cuisine == '' or r['cuisine'] == next((c['name'] for c in cuisine_list if str(c['id'])==selected_cuisine), ''):
                filtered_restaurants.append(r)
    if not search_query and selected_cuisine == '':
        filtered_restaurants = list(restaurants.values())

    return render_template('restaurants.html', restaurants=filtered_restaurants, cuisines=cuisine_list, search_query=search_query)

@app.route('/menu/<int:restaurant_id>')
def restaurant_menu(restaurant_id):
    restaurants = load_restaurants()
    menus = load_menus()

    restaurant = restaurants.get(restaurant_id)
    if not restaurant:
        return "Restaurant not found", 404

    menu_items = [item for item in menus.values() if item['restaurant_id'] == restaurant_id and item['availability']]

    return render_template('menu.html', restaurant=restaurant, menu_item=menu_items)

@app.route('/item/<int:item_id>')
def item_details(item_id):
    menus = load_menus()
    item = menus.get(item_id)
    if not item:
        return "Item not found", 404
    return render_template('item_detail.html', item=item)

@app.route('/cart')
def shopping_cart():
    cart = load_cart()
    menus = load_menus()

    cart_items = []
    total_amount = 0.0
    for item in cart.values():
        menu_item = menus.get(item['item_id'])
        if menu_item:
            amount = menu_item['price'] * item['quantity']
            cart_items.append({
                'item_id': item['item_id'],
                'name': menu_item['item_name'],
                'quantity': item['quantity'],
                'price': amount
            })
            total_amount += amount

    return render_template('cart.html', cart_items=cart_items, total_amount=round(total_amount, 2))

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        # Validate form data
        customer_name = request.form.get('customer_name', '').strip()
        delivery_address = request.form.get('delivery_address', '').strip()
        phone_number = request.form.get('phone_number', '').strip()
        payment_method = request.form.get('payment_method', '').strip()

        if not (customer_name and delivery_address and phone_number and payment_method):
            return "All fields are required", 400

        # Load cart
        cart = load_cart()
        if not cart:
            return "Cart is empty", 400

        # Create order
        orders = load_orders()
        order_items = load_order_items()
        menus = load_menus()

        new_order_id = max(orders.keys(), default=0) + 1
        total_amount = 0.0
        for item in cart.values():
            menu_item = menus.get(item['item_id'])
            if menu_item:
                total_amount += menu_item['price'] * item['quantity']

        order_date = datetime.now().strftime('%Y-%m-%d')

        # Append order to orders.txt
        try:
            with open(os.path.join(DATA_DIR, 'orders.txt'), 'a', encoding='utf-8') as f:
                status = 1  # Assuming '1' = Pending
                f.write(f"{new_order_id}|{customer_name}|{item['restaurant_id']}|{order_date}|{total_amount}|{status}|{delivery_address}|{phone_number}\n")

            with open(os.path.join(DATA_DIR, 'order_items.txt'), 'a', encoding='utf-8') as f:
                order_item_id_base = max([oi['order_item_id'] for ois in order_items.values() for oi in ois], default=0)
                count = 1
                for item in cart.values():
                    menu_item = menus.get(item['item_id'])
                    if menu_item:
                        f.write(f"{order_item_id_base + count}|{new_order_id}|{menu_item['item_id']}|{item['quantity']}|{menu_item['price']}\n")
                        count += 1
        except Exception as e:
            return "Failed to save order", 500

        # Clear cart
        with open(os.path.join(DATA_DIR, 'cart.txt'), 'w', encoding='utf-8') as f:
            pass  # emptied

        return redirect(url_for('dashboard'))

    return render_template('checkout.html')

@app.route('/orders/active')
def active_orders():
    orders = load_orders()
    deliveries = load_deliveries()

    status_filter = request.args.get('status_filter', '')
    filtered_orders = []

    status_mapping = {1: 'Pending', 2: 'On the Way', 3: 'Delivered'}

    for order in orders.values():
        if not status_filter or str(order['status']) == status_filter:
            status_text = status_mapping.get(order['status'], 'Unknown')
            active_order = {
                'order_id': order['order_id'],
                'status_text': status_text
            }
            filtered_orders.append(active_order)

    return render_template('active_orders.html', active_orders=filtered_orders, status_filter=int(status_filter) if status_filter else '')

@app.route('/orders/track/<int:order_id>')
def order_track(order_id):
    orders = load_orders()
    deliveries = load_deliveries()
    order_items_all = load_order_items()
    menus = load_menus()

    order = orders.get(order_id)
    if not order:
        return "Order not found", 404

    delivery_driver = deliveries.get(order_id, {
        'driver_name': 'N/A',
        'driver_phone': 'N/A',
        'estimated_time': 'N/A'
    })

    order_items = []
    for oi in order_items_all.get(order_id, []):
        menu_item = menus.get(oi['item_id'])
        if menu_item:
            order_items.append({'name': menu_item['item_name'], 'quantity': oi['quantity']})

    return render_template('track_order.html', order=order, delivery_driver=delivery_driver, order_items=order_items)

@app.route('/reviews')
def reviews():
    reviews_data = load_reviews()
    restaurants = load_restaurants()

    filter_rating_raw = request.args.get('filter_rating', '')
    filter_rating = int(filter_rating_raw) if filter_rating_raw.isdigit() else None

    filtered_reviews = []
    for rest_id, revs in reviews_data.items():
        for rev in revs:
            if not filter_rating or rev['rating'] == filter_rating:
                rev_copy = rev.copy()
                rev_copy['restaurant_name'] = restaurants.get(rest_id, {}).get('name', 'Unknown')
                filtered_reviews.append(rev_copy)

    return render_template('reviews.html', reviews=filtered_reviews, filter_rating=filter_rating)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
