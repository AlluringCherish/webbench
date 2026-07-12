from flask import Flask, render_template, redirect, url_for, request
import os
from datetime import datetime, date

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

data_dir = 'data'

# Utility functions to read data files with pipe "|" delimited entries

def load_restaurants():
    restaurants = []
    path = os.path.join(data_dir, 'restaurants.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 8:
                    try:
                        restaurant = {
                            'restaurant_id': int(parts[0]),
                            'name': parts[1],
                            'cuisine': parts[2],
                            'address': parts[3],
                            'phone': parts[4],
                            'rating': float(parts[5]),
                            'delivery_time': int(parts[6]),
                            'min_order': float(parts[7])
                        }
                        restaurants.append(restaurant)
                    except ValueError:
                        continue
    return restaurants


def load_menus():
    menus = []
    path = os.path.join(data_dir, 'menus.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 7:
                    try:
                        menu = {
                            'item_id': int(parts[0]),
                            'restaurant_id': int(parts[1]),
                            'item_name': parts[2],
                            'category': parts[3],
                            'description': parts[4],
                            'price': float(parts[5]),
                            'availability': int(parts[6])
                        }
                        menus.append(menu)
                    except ValueError:
                        continue
    return menus


def load_cart():
    cart = []
    path = os.path.join(data_dir, 'cart.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 5:
                    try:
                        cart_item = {
                            'cart_id': int(parts[0]),
                            'item_id': int(parts[1]),
                            'restaurant_id': int(parts[2]),
                            'quantity': int(parts[3]),
                            'added_date': parts[4]
                        }
                        cart.append(cart_item)
                    except ValueError:
                        continue
    return cart


def save_cart(cart_items):
    path = os.path.join(data_dir, 'cart.txt')
    try:
        with open(path, 'w', encoding='utf-8') as f:
            for item in cart_items:
                line = f"{item['cart_id']}|{item['item_id']}|{item['restaurant_id']}|{item['quantity']}|{item['added_date']}\n"
                f.write(line)
        return True
    except Exception:
        return False


def load_orders():
    orders = []
    path = os.path.join(data_dir, 'orders.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 8:
                    try:
                        order = {
                            'order_id': int(parts[0]),
                            'customer_name': parts[1],
                            'restaurant_id': int(parts[2]),
                            'order_date': parts[3],
                            'total_amount': float(parts[4]),
                            'status': parts[5],
                            'delivery_address': parts[6],
                            'phone_number': parts[7]
                        }
                        orders.append(order)
                    except ValueError:
                        continue
    return orders


def save_orders(orders):
    path = os.path.join(data_dir, 'orders.txt')
    try:
        with open(path, 'w', encoding='utf-8') as f:
            for o in orders:
                line = f"{o['order_id']}|{o['customer_name']}|{o['restaurant_id']}|{o['order_date']}|{o['total_amount']}|{o['status']}|{o['delivery_address']}|{o['phone_number']}\n"
                f.write(line)
        return True
    except Exception:
        return False


def load_order_items():
    items = []
    path = os.path.join(data_dir, 'order_items.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 5:
                    try:
                        order_item = {
                            'order_item_id': int(parts[0]),
                            'order_id': int(parts[1]),
                            'item_id': int(parts[2]),
                            'quantity': int(parts[3]),
                            'price': float(parts[4])
                        }
                        items.append(order_item)
                    except ValueError:
                        continue
    return items


def save_order_items(order_items):
    path = os.path.join(data_dir, 'order_items.txt')
    try:
        with open(path, 'w', encoding='utf-8') as f:
            for oi in order_items:
                line = f"{oi['order_item_id']}|{oi['order_id']}|{oi['item_id']}|{oi['quantity']}|{oi['price']}\n"
                f.write(line)
        return True
    except Exception:
        return False


def load_deliveries():
    deliveries = []
    path = os.path.join(data_dir, 'deliveries.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 7:
                    try:
                        delivery = {
                            'delivery_id': int(parts[0]),
                            'order_id': int(parts[1]),
                            'driver_name': parts[2],
                            'driver_phone': parts[3],
                            'vehicle_info': parts[4],
                            'status': parts[5],
                            'estimated_time': parts[6]  # string format
                        }
                        deliveries.append(delivery)
                    except ValueError:
                        continue
    return deliveries


def load_reviews():
    reviews = []
    path = os.path.join(data_dir, 'reviews.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 6:
                    try:
                        review = {
                            'review_id': int(parts[0]),
                            'restaurant_id': int(parts[1]),
                            'customer_name': parts[2],
                            'rating': int(parts[3]),
                            'review_text': parts[4],
                            'review_date': parts[5]
                        }
                        reviews.append(review)
                    except ValueError:
                        continue
    return reviews


@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    restaurants = load_restaurants()
    # We'll consider featured_restaurants as top 3 by rating descending
    featured_restaurants = sorted(restaurants, key=lambda r: r.get('rating',0), reverse=True)[:3]
    # popular_cuisines is optional - not specifically required to provide non-None per spec
    return render_template('dashboard.html', featured_restaurants=featured_restaurants, popular_cuisines=None)


@app.route('/restaurants')
def browse_restaurants():
    restaurants = load_restaurants()
    cuisine_options = sorted(set(r['cuisine'] for r in restaurants))
    search_query = request.args.get('search_query', '').strip()
    selected_cuisine = request.args.get('selected_cuisine', '').strip()

    filtered_restaurants = restaurants
    if search_query:
        filtered_restaurants = [r for r in filtered_restaurants if search_query.lower() in r['name'].lower() or search_query.lower() in r['cuisine'].lower()]
    if selected_cuisine:
        filtered_restaurants = [r for r in filtered_restaurants if r['cuisine'].lower() == selected_cuisine.lower()]

    return render_template('restaurants.html', restaurants=filtered_restaurants, cuisine_options=cuisine_options,
                           search_query=search_query, selected_cuisine=selected_cuisine)


@app.route('/menu/<int:restaurant_id>')
def restaurant_menu(restaurant_id):
    restaurants = load_restaurants()
    menus = load_menus()
    restaurant = next((r for r in restaurants if r['restaurant_id'] == restaurant_id), None)
    if not restaurant:
        return "Restaurant not found", 404

    menu_items = [m for m in menus if m['restaurant_id'] == restaurant_id and m['availability'] == 1]

    return render_template('menu.html', restaurant=restaurant, menu_items=menu_items)


@app.route('/item/<int:item_id>', methods=['GET', 'POST'])
def item_details(item_id):
    menus = load_menus()
    item = next((m for m in menus if m['item_id'] == item_id and m['availability'] == 1), None)
    if not item:
        return "Item not found", 404

    if request.method == 'POST':
        form = request.form
        quantity_str = form.get('quantity', '1').strip()
        try:
            quantity = int(quantity_str)
            if quantity < 1:
                quantity = 1
        except ValueError:
            quantity = 1

        cart_items = load_cart()
        cart_id_counter = max((ci['cart_id'] for ci in cart_items), default=0) + 1

        # add the item to cart
        new_cart = cart_items[:]
        new_cart.append({
            'cart_id': cart_id_counter,
            'item_id': item['item_id'],
            'restaurant_id': item['restaurant_id'],
            'quantity': quantity,
            'added_date': date.today().isoformat()
        })

        success = save_cart(new_cart)
        if not success:
            return "Failed to add item to cart", 500

        return redirect(url_for('shopping_cart'))

    return render_template('item_details.html', item=item)


@app.route('/cart', methods=['GET', 'POST'])
def shopping_cart():
    cart_items = load_cart()
    menus = load_menus()

    # Build cart items details to pass to template: join cart item with menu item info
    # Calculate total_amount

    def find_menu_item(item_id):
        return next((m for m in menus if m['item_id'] == item_id), None)

    if request.method == 'POST':
        # updating quantities or removing items
        form = request.form
        # Expecting form data like quantity-{item_id} for changing quantities or remove_item_id for removals
        new_cart = []
        cart_id_counter = 1
        today_date = date.today().isoformat()

        remove_item_id = form.get('remove_item_id')
        for cart_item in cart_items:
            item_id = cart_item['item_id']

            if remove_item_id is not None and str(remove_item_id) == str(item_id):
                # remove this item
                continue

            quantity_key = f'quantity_{item_id}'
            quantity_val = form.get(quantity_key)
            try:
                quantity_val = int(quantity_val)
                if quantity_val < 1:
                    continue
            except (ValueError, TypeError):
                quantity_val = cart_item['quantity']

            new_cart.append({
                'cart_id': cart_id_counter,
                'item_id': item_id,
                'restaurant_id': cart_item['restaurant_id'],
                'quantity': quantity_val,
                'added_date': today_date
            })
            cart_id_counter += 1

        # save new cart to file
        success = save_cart(new_cart)
        if not success:
            return "Failed to update cart", 500

        # Reload updated cart
        cart_items = new_cart

    cart_detail_list = []
    total_amount = 0.0
    for ci in cart_items:
        menu_item = find_menu_item(ci['item_id'])
        if not menu_item or menu_item['availability'] != 1:
            continue
        subtotal = menu_item['price'] * ci['quantity']
        total_amount += subtotal
        cart_detail_list.append({
            'cart_id': ci['cart_id'],
            'item_id': ci['item_id'],
            'restaurant_id': ci['restaurant_id'],
            'item_name': menu_item['item_name'],
            'price': menu_item['price'],
            'quantity': ci['quantity'],
            'subtotal': subtotal
        })

    return render_template('cart.html', cart_items=cart_detail_list, total_amount=round(total_amount, 2))


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'GET':
        # Just display empty form
        return render_template('checkout.html')

    # POST - process order
    form = request.form
    customer_name = form.get('customer_name', '').strip()
    delivery_address = form.get('delivery_address', '').strip()
    phone_number = form.get('phone_number', '').strip()
    payment_method = form.get('payment_method', '').strip()

    if not all([customer_name, delivery_address, phone_number, payment_method]):
        # Missing required fields
        return render_template('checkout.html', error="Please fill all required fields")

    cart_items = load_cart()
    menus = load_menus()

    # Calculate total amount
    total_amount = 0.0
    for ci in cart_items:
        menu_item = next((m for m in menus if m['item_id'] == ci['item_id'] and m['availability'] == 1), None)
        if menu_item:
            total_amount += menu_item['price'] * ci['quantity']

    if total_amount <= 0:
        return render_template('checkout.html', error="Your cart is empty or items unavailable.")

    orders = load_orders()
    order_items = load_order_items()

    # Create new order_id
    if orders:
        new_order_id = max(o['order_id'] for o in orders) + 1
    else:
        new_order_id = 1

    # For restaurant_id in order, we assume from cart items restaurant_ids, but orders.txt schema expects one restaurant_id
    # If multiple restaurants in cart, for simplicity pick the restaurant_id of first cart item
    restaurant_id = cart_items[0]['restaurant_id'] if cart_items else None
    if not restaurant_id:
        return render_template('checkout.html', error="Cart is empty or invalid.")

    order_date = date.today().isoformat()
    status = 'Preparing'

    new_order = {
        'order_id': new_order_id,
        'customer_name': customer_name,
        'restaurant_id': restaurant_id,
        'order_date': order_date,
        'total_amount': round(total_amount, 2),
        'status': status,
        'delivery_address': delivery_address,
        'phone_number': phone_number
    }

    orders.append(new_order)

    # Create order items entries
    next_order_item_id = max((oi['order_item_id'] for oi in order_items), default=0) + 1
    for ci in cart_items:
        menu_item = next((m for m in menus if m['item_id'] == ci['item_id']), None)
        if menu_item:
            order_item = {
                'order_item_id': next_order_item_id,
                'order_id': new_order_id,
                'item_id': menu_item['item_id'],
                'quantity': ci['quantity'],
                'price': menu_item['price']
            }
            order_items.append(order_item)
            next_order_item_id += 1

    # Save order and order items
    success_orders = save_orders(orders)
    success_order_items = save_order_items(order_items)

    if not (success_orders and success_order_items):
        return render_template('checkout.html', error="Failed to save order.")

    # Clear cart after successful order
    success_clear_cart = save_cart([])

    # For simplicity, after order placed redirect to dashboard
    return redirect(url_for('dashboard'))


@app.route('/orders/active')
def active_orders():
    orders = load_orders()
    status_options = sorted(set(o['status'] for o in orders))
    selected_status = request.args.get('selected_status', '').strip()

    filtered_orders = orders
    if selected_status:
        filtered_orders = [o for o in orders if o['status'].lower() == selected_status.lower()]

    # Join restaurant name for each order for display
    restaurants = load_restaurants()
    restaurant_dict = {r['restaurant_id']: r['name'] for r in restaurants}
    for o in filtered_orders:
        o['restaurant_name'] = restaurant_dict.get(o['restaurant_id'], 'Unknown')

    return render_template('active_orders.html', active_orders=filtered_orders, status_options=status_options, selected_status=selected_status)


@app.route('/orders/track/<int:order_id>')
def track_order(order_id):
    orders = load_orders()
    order = next((o for o in orders if o['order_id'] == order_id), None)
    if not order:
        return "Order not found", 404

    deliveries = load_deliveries()
    delivery_info = next((d for d in deliveries if d['order_id'] == order_id), None)

    order_items = load_order_items()
    menus = load_menus()

    items_list = []
    for oi in order_items:
        if oi['order_id'] == order_id:
            menu_item = next((m for m in menus if m['item_id'] == oi['item_id']), None)
            if menu_item:
                items_list.append({
                    'item_name': menu_item['item_name'],
                    'quantity': oi['quantity'],
                    'price': oi['price']
                })

    return render_template('track_order.html', order=order, delivery_info=delivery_info, order_items=items_list)


@app.route('/reviews')
def reviews():
    reviews_list = load_reviews()
    rating_filter_options = ['1', '2', '3', '4', '5']
    selected_rating = request.args.get('selected_rating', '').strip()

    filtered_reviews = reviews_list
    if selected_rating and selected_rating in rating_filter_options:
        filtered_reviews = [r for r in reviews_list if str(r['rating']) == selected_rating]

    # Join restaurant name for each review for display
    restaurants = load_restaurants()
    restaurant_dict = {r['restaurant_id']: r['name'] for r in restaurants}
    for r in filtered_reviews:
        r['restaurant_name'] = restaurant_dict.get(r['restaurant_id'], 'Unknown')

    return render_template('reviews.html', reviews=filtered_reviews, rating_filter_options=rating_filter_options, selected_rating=selected_rating)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
