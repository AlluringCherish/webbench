from flask import Flask, render_template, redirect, url_for, request
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# --- Helper Functions to load data files ---

def load_restaurants():
    """Load restaurants from restaurants.txt"""
    restaurants = []
    path = os.path.join(DATA_DIR, 'restaurants.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 8:
                    continue
                rest = {
                    'restaurant_id': int(parts[0]),
                    'name': parts[1],
                    'cuisine': parts[2],
                    'address': parts[3],
                    'phone': parts[4],
                    'rating': float(parts[5]),
                    'delivery_time': int(parts[6]),
                    'min_order': float(parts[7])
                }
                restaurants.append(rest)
    except FileNotFoundError:
        print(f"Error: {path} not found.")
    except Exception as e:
        print(f"Error loading restaurants: {e}")
    return restaurants


def load_menus():
    """Load menu items from menus.txt"""
    menus = []
    path = os.path.join(DATA_DIR, 'menus.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 7:
                    continue
                item = {
                    'item_id': int(parts[0]),
                    'restaurant_id': int(parts[1]),
                    'item_name': parts[2],
                    'category': parts[3],
                    'description': parts[4],
                    'price': float(parts[5]),
                    'availability': int(parts[6])
                }
                menus.append(item)
    except FileNotFoundError:
        print(f"Error: {path} not found.")
    except Exception as e:
        print(f"Error loading menus: {e}")
    return menus


def load_cart():
    """Load shopping cart from cart.txt"""
    cart_items = []
    path = os.path.join(DATA_DIR, 'cart.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 5:
                    continue
                cart_item = {
                    'cart_id': int(parts[0]),
                    'item_id': int(parts[1]),
                    'restaurant_id': int(parts[2]),
                    'quantity': int(parts[3]),
                    'added_date': parts[4]
                }
                cart_items.append(cart_item)
    except FileNotFoundError:
        print(f"Error: {path} not found.")
    except Exception as e:
        print(f"Error loading cart: {e}")
    return cart_items


def load_orders():
    """Load orders from orders.txt"""
    orders = []
    path = os.path.join(DATA_DIR, 'orders.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 8:
                    continue
                order = {
                    'order_id': int(parts[0]),
                    'customer_name': parts[1],
                    'restaurant_id': int(parts[2]),
                    'order_date': parts[3],  # YYYY-MM-DD
                    'total_amount': float(parts[4]),
                    'status': parts[5],
                    'delivery_address': parts[6],
                    'phone_number': parts[7]
                }
                orders.append(order)
    except FileNotFoundError:
        print(f"Error: {path} not found.")
    except Exception as e:
        print(f"Error loading orders: {e}")
    return orders


def load_order_items():
    """Load order_items from order_items.txt"""
    order_items = []
    path = os.path.join(DATA_DIR, 'order_items.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 5:
                    continue
                oi = {
                    'order_item_id': int(parts[0]),
                    'order_id': int(parts[1]),
                    'item_id': int(parts[2]),
                    'quantity': int(parts[3]),
                    'price': float(parts[4])
                }
                order_items.append(oi)
    except FileNotFoundError:
        print(f"Error: {path} not found.")
    except Exception as e:
        print(f"Error loading order items: {e}")
    return order_items


def load_deliveries():
    """Load delivery info from deliveries.txt"""
    deliveries = []
    path = os.path.join(DATA_DIR, 'deliveries.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 7:
                    continue
                delivery = {
                    'delivery_id': int(parts[0]),
                    'order_id': int(parts[1]),
                    'driver_name': parts[2],
                    'driver_phone': parts[3],
                    'vehicle_info': parts[4],
                    'status': parts[5],
                    'estimated_time': parts[6]  # YYYY-MM-DD HH:MM
                }
                deliveries.append(delivery)
    except FileNotFoundError:
        print(f"Error: {path} not found.")
    except Exception as e:
        print(f"Error loading deliveries: {e}")
    return deliveries


def load_reviews():
    """Load reviews from reviews.txt"""
    reviews = []
    path = os.path.join(DATA_DIR, 'reviews.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 6:
                    continue
                review = {
                    'review_id': int(parts[0]),
                    'restaurant_id': int(parts[1]),
                    'customer_name': parts[2],
                    'rating': int(parts[3]),
                    'review_text': parts[4],
                    'review_date': parts[5]
                }
                reviews.append(review)
    except FileNotFoundError:
        print(f"Error: {path} not found.")
    except Exception as e:
        print(f"Error loading reviews: {e}")
    return reviews


# --- Routes Implementation ---

@app.route('/')
def root_redirect():
    # Redirect root to dashboard
    return redirect(url_for('dashboard_page'))


@app.route('/dashboard')
def dashboard_page():
    # Load restaurants
    restaurants = load_restaurants()
    # Select featured restaurants: top 3 by rating
    featured_restaurants = sorted(restaurants, key=lambda r: r['rating'], reverse=True)[:3]

    # Extract popular cuisines (unique, sorted) - for simplicity, get top cuisines by count
    cuisine_count = {}
    for r in restaurants:
        cuisine_count[r['cuisine']] = cuisine_count.get(r['cuisine'], 0) + 1
    popular_cuisines = sorted(cuisine_count.keys())

    return render_template('dashboard.html',
                           featured_restaurants=featured_restaurants,
                           popular_cuisines=popular_cuisines)


@app.route('/restaurants')
def browse_restaurants():
    restaurants = load_restaurants()
    # Extract unique cuisines
    cuisines_set = set()
    for r in restaurants:
        cuisines_set.add(r['cuisine'])
    cuisines = sorted(list(cuisines_set))

    return render_template('restaurants.html',
                           restaurants=restaurants,
                           cuisines=cuisines)


@app.route('/menu/<int:restaurant_id>')
def restaurant_menu(restaurant_id):
    restaurants = load_restaurants()
    menus = load_menus()
    # Get restaurant details
    restaurant = next((r for r in restaurants if r['restaurant_id'] == restaurant_id), None)
    if not restaurant:
        return f"Restaurant with id {restaurant_id} not found.", 404
    # Get menu items for restaurant, only available items
    menu_items = [m for m in menus if m['restaurant_id'] == restaurant_id and m['availability'] == 1]

    return render_template('menu.html', restaurant=restaurant, menu_items=menu_items)


@app.route('/item/<int:item_id>')
def item_details(item_id):
    menus = load_menus()
    item = next((m for m in menus if m['item_id'] == item_id), None)
    if not item:
        return f"Item with id {item_id} not found.", 404

    quantity_default = 1
    return render_template('item_details.html', item=item, quantity_default=quantity_default)


@app.route('/cart', methods=['GET', 'POST'])
def shopping_cart():
    # Load cart and menu to display cart items with details
    cart_items_data = load_cart()
    menus = load_menus()

    if request.method == 'POST':
        form = request.form

        # First, handle add-to-cart submission from menu or item details
        if 'item_id' in form and 'quantity' in form:
            try:
                item_id = int(form.get('item_id'))
                quantity = int(form.get('quantity'))
                if quantity < 1:
                    quantity = 1
            except Exception:
                return "Invalid item ID or quantity.", 400

            # Load item info
            menu_item = next((m for m in menus if m['item_id'] == item_id), None)
            if not menu_item:
                return f"Menu item with id {item_id} not found.", 404

            # Check if item is already in cart
            existing_cart_item = next((ci for ci in cart_items_data if ci['item_id'] == item_id), None)
            if existing_cart_item:
                # Update quantity
                existing_cart_item['quantity'] += quantity
            else:
                # Add new cart item
                if cart_items_data:
                    new_cart_id = max(ci['cart_id'] for ci in cart_items_data) + 1
                else:
                    new_cart_id = 1
                # for restaurant_id get from menu item
                rest_id = menu_item['restaurant_id']
                added_date = datetime.now().strftime('%Y-%m-%d')
                new_cart_item = {
                    'cart_id': new_cart_id,
                    'item_id': item_id,
                    'restaurant_id': rest_id,
                    'quantity': quantity,
                    'added_date': added_date
                }
                cart_items_data.append(new_cart_item)

            # Save updated cart
            try:
                path = os.path.join(DATA_DIR, 'cart.txt')
                with open(path, 'w', encoding='utf-8') as f:
                    for ci in cart_items_data:
                        line = f"{ci['cart_id']}|{ci['item_id']}|{ci['restaurant_id']}|{ci['quantity']}|{ci['added_date']}\n"
                        f.write(line)
            except Exception as e:
                return f"Error saving cart: {e}", 500

            return redirect(url_for('shopping_cart'))

        # Handle update quantities and removal - fix to match frontend form field names
        updated = False
        for key in form:
            if key.startswith('quantity-'):
                try:
                    item_id = int(key[len('quantity-'):])
                    new_qty = int(form[key])
                    if new_qty < 0:
                        continue
                    for ci in cart_items_data:
                        if ci['item_id'] == item_id:
                            if new_qty == 0:
                                cart_items_data.remove(ci)
                            else:
                                ci['quantity'] = new_qty
                            updated = True
                            break
                except Exception:
                    pass
            elif key == 'remove-item':
                try:
                    item_id = int(form[key])
                    cart_items_data = [ci for ci in cart_items_data if ci['item_id'] != item_id]
                    updated = True
                except Exception:
                    pass

        if updated:
            try:
                path = os.path.join(DATA_DIR, 'cart.txt')
                with open(path, 'w', encoding='utf-8') as f:
                    for ci in cart_items_data:
                        line = f"{ci['cart_id']}|{ci['item_id']}|{ci['restaurant_id']}|{ci['quantity']}|{ci['added_date']}\n"
                        f.write(line)
            except Exception as e:
                return f"Error saving cart: {e}", 500

            return redirect(url_for('shopping_cart'))

    # Compute cart_items with item_name, price, subtotal
    cart_items = []
    total_amount = 0.0
    for ci in cart_items_data:
        menu_item = next((m for m in menus if m['item_id'] == ci['item_id']), None)
        if menu_item:
            price = menu_item['price']
            quantity = ci['quantity']
            subtotal = price * quantity
            total_amount += subtotal
            cart_items.append({
                'item_id': ci['item_id'],
                'item_name': menu_item['item_name'],
                'quantity': quantity,
                'price': price,
                'subtotal': subtotal
            })

    return render_template('cart.html', cart_items=cart_items, total_amount=total_amount)


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'GET':
        return render_template('checkout.html')
    # On POST process form data
    form = request.form
    customer_name = form.get('customer_name', '').strip()
    delivery_address = form.get('delivery_address', '').strip()
    phone_number = form.get('phone_number', '').strip()
    payment_method = form.get('payment_method', '').strip()

    # Basic validation
    if not (customer_name and delivery_address and phone_number and payment_method):
        return "Missing required checkout fields.", 400

    # Load cart
    cart_items_data = load_cart()
    if not cart_items_data:
        return "Shopping cart is empty.", 400

    # Calculate total amount
    menus = load_menus()
    total_amount = 0.0
    for ci in cart_items_data:
        menu_item = next((m for m in menus if m['item_id'] == ci['item_id']), None)
        if menu_item:
            total_amount += menu_item['price'] * ci['quantity']

    # Load orders to assign new order_id
    orders = load_orders()
    if orders:
        new_order_id = max(o['order_id'] for o in orders) + 1
    else:
        new_order_id = 1

    # Load restaurants to validate
    restaurants = load_restaurants()

    # We associate order to all involved restaurants?
    # Spec expects restaurant_id per order: simplification - assign to restaurant_id of first item
    if cart_items_data:
        restaurant_id = cart_items_data[0]['restaurant_id']
    else:
        restaurant_id = None

    order_date = datetime.now().strftime('%Y-%m-%d')

    # Append new order
    new_order = {
        'order_id': new_order_id,
        'customer_name': customer_name,
        'restaurant_id': restaurant_id,
        'order_date': order_date,
        'total_amount': total_amount,
        'status': 'Preparing',
        'delivery_address': delivery_address,
        'phone_number': phone_number
    }

    try:
        # Save new order to orders.txt
        path_orders = os.path.join(DATA_DIR, 'orders.txt')
        with open(path_orders, 'a', encoding='utf-8') as f:
            line = f"{new_order['order_id']}|{new_order['customer_name']}|{new_order['restaurant_id']}|{new_order['order_date']}|" \
                   f"{new_order['total_amount']:.2f}|{new_order['status']}|{new_order['delivery_address']}|{new_order['phone_number']}\n"
            f.write(line)

        # Save to order_items.txt:
        order_items = load_order_items()
        if order_items:
            new_order_item_id = max(oi['order_item_id'] for oi in order_items) + 1
        else:
            new_order_item_id = 1

        path_order_items = os.path.join(DATA_DIR, 'order_items.txt')
        with open(path_order_items, 'a', encoding='utf-8') as f:
            for ci in cart_items_data:
                menu_item = next((m for m in menus if m['item_id'] == ci['item_id']), None)
                if menu_item:
                    line = f"{new_order_item_id}|{new_order_id}|{ci['item_id']}|{ci['quantity']}|{menu_item['price']:.2f}\n"
                    f.write(line)
                    new_order_item_id += 1

        # Clear cart after order
        path_cart = os.path.join(DATA_DIR, 'cart.txt')
        with open(path_cart, 'w', encoding='utf-8') as f:
            pass

    except Exception as e:
        return f"Error processing order: {e}", 500

    return redirect(url_for('active_orders'))


@app.route('/orders/active')
def active_orders():
    orders = load_orders()
    restaurants = load_restaurants()

    # Filter active orders (status not Delivered)
    active_orders = [o for o in orders if o['status'].lower() != 'delivered']

    # Attach restaurant_name to each order
    for o in active_orders:
        rest = next((r for r in restaurants if r['restaurant_id'] == o['restaurant_id']), None)
        o['restaurant_name'] = rest['name'] if rest else 'Unknown'

    return render_template('active_orders.html', active_orders=active_orders)


@app.route('/order/track/<int:order_id>')
def order_tracking(order_id):
    orders = load_orders()
    restaurants = load_restaurants()
    order_items_all = load_order_items()
    deliveries = load_deliveries()

    order = next((o for o in orders if o['order_id'] == order_id), None)
    if not order:
        return f"Order with id {order_id} not found.", 404

    # Get delivery info
    delivery = next((d for d in deliveries if d['order_id'] == order_id), None)
    if not delivery:
        delivery_info = {'driver_name': '', 'driver_phone': '', 'vehicle_info': ''}
        estimated_time = ''
    else:
        delivery_info = {
            'driver_name': delivery['driver_name'],
            'driver_phone': delivery['driver_phone'],
            'vehicle_info': delivery['vehicle_info']
        }
        # Format estimated_time nicely
        estimated_time = delivery['estimated_time']

    # Get items in the order with name, quantity, price
    items_list = []
    for oi in order_items_all:
        if oi['order_id'] == order_id:
            menu_item = next((m for m in load_menus() if m['item_id'] == oi['item_id']), None)
            if menu_item:
                items_list.append({
                    'item_name': menu_item['item_name'],
                    'quantity': oi['quantity'],
                    'price': oi['price']
                })

    return render_template('track_order.html',
                           order_details=order,
                           delivery_info=delivery_info,
                           estimated_time=estimated_time,
                           order_items=items_list)


@app.route('/reviews')
def reviews_page():
    reviews = load_reviews()
    # Filter ratings options
    filter_ratings = ['All', '5 stars', '4 stars', '3 stars', '2 stars', '1 star']
    return render_template('reviews.html', reviews=reviews, filter_ratings=filter_ratings)


@app.route('/reviews/write', methods=['GET', 'POST'])
def write_review():
    if request.method == 'GET':
        return render_template('write_review.html')

    form = request.form
    restaurant_id_str = form.get('restaurant_id', '').strip()
    customer_name = form.get('customer_name', '').strip()
    rating_str = form.get('rating', '').strip()
    review_text = form.get('review_text', '').strip()

    # Validate inputs
    if not (restaurant_id_str and customer_name and rating_str and review_text):
        return "Missing review fields.", 400
    try:
        restaurant_id = int(restaurant_id_str)
        rating = int(rating_str)
    except ValueError:
        return "Invalid restaurant ID or rating.", 400
    if rating < 1 or rating > 5:
        return "Rating must be between 1 and 5.", 400

    # Load reviews to determine new review_id
    reviews = load_reviews()
    if reviews:
        new_review_id = max(r['review_id'] for r in reviews) + 1
    else:
        new_review_id = 1

    review_date = datetime.now().strftime('%Y-%m-%d')

    # Append new review to reviews.txt
    try:
        path = os.path.join(DATA_DIR, 'reviews.txt')
        with open(path, 'a', encoding='utf-8') as f:
            line = f"{new_review_id}|{restaurant_id}|{customer_name}|{rating}|{review_text}|{review_date}\n"
            f.write(line)
    except Exception as e:
        return f"Error saving review: {e}", 500

    return redirect(url_for('reviews_page'))


if __name__ == '__main__':
    app.run(debug=True, port=5000)
