from flask import Flask, render_template, redirect, url_for, request, abort
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

data_dir = 'data'

# Utility functions to load data from pipe-delimited files

# Load all restaurants
# restaurant_id|name|cuisine|address|phone|rating|delivery_time|min_order
# types: int,string,string,string,string,float,int,float

def load_restaurants():
    restaurants = []
    path = os.path.join(data_dir, 'restaurants.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 8:
                    continue
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
    except FileNotFoundError:
        pass
    return restaurants

# Load all menu items
# item_id|restaurant_id|item_name|category|description|price|availability
# item_id,int

def load_menus():
    menus = []
    path = os.path.join(data_dir, 'menus.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 7:
                    continue
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
    except FileNotFoundError:
        pass
    return menus

# Load cart items
# cart_id|item_id|restaurant_id|quantity|added_date

from datetime import datetime

def load_cart():
    carts = []
    path = os.path.join(data_dir, 'cart.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 5:
                    continue
                try:
                    cart_item = {
                        'cart_id': int(parts[0]),
                        'item_id': int(parts[1]),
                        'restaurant_id': int(parts[2]),
                        'quantity': int(parts[3]),
                        'added_date': parts[4]  # as string, format YYYY-MM-DD
                    }
                    carts.append(cart_item)
                except ValueError:
                    continue
    except FileNotFoundError:
        pass
    return carts

# Load orders
# order_id|customer_name|restaurant_id|order_date|total_amount|status|delivery_address|phone_number

def load_orders():
    orders = []
    path = os.path.join(data_dir, 'orders.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 8:
                    continue
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
    except FileNotFoundError:
        pass
    return orders

# Load order items
# order_item_id|order_id|item_id|quantity|price

def load_order_items():
    order_items = []
    path = os.path.join(data_dir, 'order_items.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 5:
                    continue
                try:
                    oi = {
                        'order_item_id': int(parts[0]),
                        'order_id': int(parts[1]),
                        'item_id': int(parts[2]),
                        'quantity': int(parts[3]),
                        'price': float(parts[4])
                    }
                    order_items.append(oi)
                except ValueError:
                    continue
    except FileNotFoundError:
        pass
    return order_items

# Load deliveries
# delivery_id|order_id|driver_name|driver_phone|vehicle_info|status|estimated_time

def load_deliveries():
    deliveries = []
    path = os.path.join(data_dir, 'deliveries.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 7:
                    continue
                delivery = {
                    'delivery_id': int(parts[0]),
                    'order_id': int(parts[1]),
                    'driver_name': parts[2],
                    'driver_phone': parts[3],
                    'vehicle_info': parts[4],
                    'status': parts[5],
                    'estimated_time': parts[6]
                }
                deliveries.append(delivery)
    except FileNotFoundError:
        pass
    return deliveries

# Load reviews
# review_id|restaurant_id|customer_name|rating|review_text|review_date

def load_reviews():
    reviews = []
    path = os.path.join(data_dir, 'reviews.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 6:
                    continue
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
    except FileNotFoundError:
        pass
    return reviews

# --- Flask Routes Implementation ---

# Root redirect to /dashboard
@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard_page'))

# /dashboard GET
@app.route('/dashboard')
def dashboard_page():
    restaurants = load_restaurants()
    # featured restaurants: top 3 by rating descending
    featured_restaurants = sorted(restaurants, key=lambda r: r['rating'], reverse=True)[:3]

    # popular cuisines: top 5 cuisines by count of restaurants
    cuisine_count = {}
    for r in restaurants:
        cuisine_count[r['cuisine']] = cuisine_count.get(r['cuisine'], 0) + 1
    popular_cuisines = sorted(cuisine_count.keys(), key=lambda c: cuisine_count[c], reverse=True)[:5]

    return render_template('dashboard.html', featured_restaurants=featured_restaurants, popular_cuisines=popular_cuisines)

# /restaurants GET
@app.route('/restaurants')
def restaurant_listing():
    restaurants = load_restaurants()
    cuisine_filter_options = sorted(list(set(r['cuisine'] for r in restaurants)))

    # Optional query params
    selected_cuisine = request.args.get('cuisine', '')
    search_query = request.args.get('search', '')

    filtered_restaurants = restaurants

    if selected_cuisine:
        filtered_restaurants = [r for r in filtered_restaurants if r['cuisine'].lower() == selected_cuisine.lower()]

    if search_query:
        sq = search_query.lower()
        filtered_restaurants = [r for r in filtered_restaurants if sq in r['name'].lower()]

    return render_template('restaurants.html',
                           restaurants=filtered_restaurants,
                           cuisine_filter_options=cuisine_filter_options,
                           selected_cuisine=selected_cuisine,
                           search_query=search_query)

# /menu/<int:restaurant_id> GET
@app.route('/menu/<int:restaurant_id>')
def restaurant_menu(restaurant_id):
    restaurants = load_restaurants()
    menus = load_menus()

    restaurant = next((r for r in restaurants if r['restaurant_id'] == restaurant_id), None)
    if not restaurant:
        abort(404)

    menu_items = [item for item in menus if item['restaurant_id'] == restaurant_id and item['availability'] == 1]

    return render_template('menu.html', restaurant=restaurant, menu_items=menu_items)

# /item/<int:item_id> GET
@app.route('/item/<int:item_id>')
def item_details(item_id):
    menus = load_menus()
    item = next((i for i in menus if i['item_id'] == item_id), None)
    if not item:
        abort(404)
    return render_template('item_details.html', item=item)

# /cart GET, POST
@app.route('/cart', methods=['GET', 'POST'])
def shopping_cart():
    carts = load_cart()
    menus = load_menus()

    # Build cart items with details
    cart_items = []
    total_amount = 0.0
    for c in carts:
        menu_item = next((m for m in menus if m['item_id'] == c['item_id']), None)
        if menu_item:
            total_price = menu_item['price'] * c['quantity']
            total_amount += total_price
            cart_items.append({
                'cart_id': c['cart_id'],
                'item_id': c['item_id'],
                'restaurant_id': c['restaurant_id'],
                'item_name': menu_item['item_name'],
                'price': menu_item['price'],
                'quantity': c['quantity'],
                'total_price': total_price
            })

    return render_template('cart.html', cart_items=cart_items, total_amount=total_amount)

# /cart/update POST
@app.route('/cart/update', methods=['POST'])
def update_cart():
    # form data expected:
    # action=update or remove
    # cart_id
    # quantity (if updating)
    
    action = request.form.get('action')
    cart_id_str = request.form.get('cart_id')

    if not cart_id_str or not cart_id_str.isdigit():
        return redirect(url_for('shopping_cart'))
    cart_id = int(cart_id_str)

    carts = load_cart()

    # Find cart line to modify
    line = next((c for c in carts if c['cart_id'] == cart_id), None)
    if not line:
        return redirect(url_for('shopping_cart'))

    if action == 'update':
        quantity_str = request.form.get('quantity')
        if not quantity_str or not quantity_str.isdigit():
            return redirect(url_for('shopping_cart'))
        quantity = int(quantity_str)
        if quantity < 1:
            # Remove item if quantity less than 1
            action = 'remove'
        else:
            line['quantity'] = quantity

    if action == 'remove':
        # Remove line from cart
        carts = [c for c in carts if c['cart_id'] != cart_id]

    if action == 'update':
        # update the quantity line in carts data
        for idx, c in enumerate(carts):
            if c['cart_id'] == cart_id:
                carts[idx] = line

    # Save updated carts to file
    save_cart(carts)

    return redirect(url_for('shopping_cart'))

# Save cart data back to cart.txt
# cart_id|item_id|restaurant_id|quantity|added_date

def save_cart(carts):
    path = os.path.join(data_dir, 'cart.txt')
    try:
        with open(path, 'w', encoding='utf-8') as f:
            for c in carts:
                line = f"{c['cart_id']}|{c['item_id']}|{c['restaurant_id']}|{c['quantity']}|{c['added_date']}\n"
                f.write(line)
    except Exception:
        pass

# /checkout GET, POST
@app.route('/checkout', methods=['GET', 'POST'])
def checkout_page():
    if request.method == 'GET':
        # Just show page
        return render_template('checkout.html')

    # POST - process order placement
    form_submission_status = {}

    customer_name = request.form.get('customer_name', '').strip()
    delivery_address = request.form.get('delivery_address', '').strip()
    phone_number = request.form.get('phone_number', '').strip()
    payment_method = request.form.get('payment_method', '').strip()

    # Basic validation
    if not customer_name:
        form_submission_status['error'] = 'Customer name is required.'
    elif not delivery_address:
        form_submission_status['error'] = 'Delivery address is required.'
    elif not phone_number:
        form_submission_status['error'] = 'Phone number is required.'
    elif not payment_method:
        form_submission_status['error'] = 'Payment method is required.'

    carts = load_cart()
    menus = load_menus()

    if not form_submission_status:
        if not carts:
            form_submission_status['error'] = 'Your cart is empty. Please add items before checkout.'

    if form_submission_status:
        return render_template('checkout.html', form_submission_status=form_submission_status)

    # Group cart items by restaurant - assuming one restaurant per order
    # However, from spec: orders.txt stores restaurant_id, so all cart items must be same restaurant to proceed
    restaurant_ids = set(c['restaurant_id'] for c in carts)
    if len(restaurant_ids) != 1:
        form_submission_status['error'] = 'All items in cart must be from the same restaurant to place an order.'
        return render_template('checkout.html', form_submission_status=form_submission_status)

    restaurant_id = restaurant_ids.pop()

    # Calculate total amount
    total_amount = 0.0
    for c in carts:
        menu_item = next((m for m in menus if m['item_id'] == c['item_id']), None)
        if menu_item:
            total_amount += menu_item['price'] * c['quantity']

    # Generate new order id
    orders = load_orders()
    new_order_id = max((o['order_id'] for o in orders), default=0) + 1

    order_date_str = datetime.today().strftime('%Y-%m-%d')

    # Append order to orders.txt
    new_order = {
        'order_id': new_order_id,
        'customer_name': customer_name,
        'restaurant_id': restaurant_id,
        'order_date': order_date_str,
        'total_amount': total_amount,
        'status': 'Preparing',
        'delivery_address': delivery_address,
        'phone_number': phone_number
    }

    try:
        orders_path = os.path.join(data_dir, 'orders.txt')
        with open(orders_path, 'a', encoding='utf-8') as f:
            line = f"{new_order['order_id']}|{new_order['customer_name']}|{new_order['restaurant_id']}|{new_order['order_date']}|{new_order['total_amount']:.2f}|{new_order['status']}|{new_order['delivery_address']}|{new_order['phone_number']}\n"
            f.write(line)
    except Exception:
        form_submission_status['error'] = 'Failed to save order. Please try again later.'
        return render_template('checkout.html', form_submission_status=form_submission_status)

    # Append order items to order_items.txt
    order_items = load_order_items()
    new_order_item_id = max((oi['order_item_id'] for oi in order_items), default=0) + 1

    try:
        order_items_path = os.path.join(data_dir, 'order_items.txt')
        with open(order_items_path, 'a', encoding='utf-8') as f:
            for c in carts:
                menu_item = next((m for m in menus if m['item_id'] == c['item_id']), None)
                if menu_item:
                    line = f"{new_order_item_id}|{new_order_id}|{menu_item['item_id']}|{c['quantity']}|{menu_item['price']:.2f}\n"
                    f.write(line)
                    new_order_item_id += 1
    except Exception:
        form_submission_status['error'] = 'Failed to save order items. Please try again later.'
        return render_template('checkout.html', form_submission_status=form_submission_status)

    # Clear cart after successful order
    save_cart([])

    form_submission_status['success'] = f'Order placed successfully! Your order ID is {new_order_id}.'
    return render_template('checkout.html', form_submission_status=form_submission_status)

# /orders/active GET
@app.route('/orders/active')
def active_orders():
    orders = load_orders()
    status_filter_options = sorted(list(set(o['status'] for o in orders)))

    selected_status = request.args.get('status', '')

    filtered_orders = orders
    if selected_status:
        filtered_orders = [o for o in filtered_orders if o['status'].lower() == selected_status.lower()]

    return render_template('active_orders.html', orders=filtered_orders, status_filter_options=status_filter_options, selected_status=selected_status)

# /order/track/<int:order_id> GET
@app.route('/order/track/<int:order_id>')
def order_tracking(order_id):
    orders = load_orders()
    order_details = next((o for o in orders if o['order_id'] == order_id), None)
    if not order_details:
        abort(404)

    deliveries = load_deliveries()
    delivery_driver_info = next((d for d in deliveries if d['order_id'] == order_id), None)

    order_items = load_order_items()
    menus = load_menus()

    # Get items for the order
    items = []
    for oi in order_items:
        if oi['order_id'] == order_id:
            menu_item = next((m for m in menus if m['item_id'] == oi['item_id']), None)
            if menu_item:
                items.append({
                    'item_name': menu_item['item_name'],
                    'quantity': oi['quantity'],
                    'price': oi['price']
                })

    return render_template('track_order.html', order_details=order_details, delivery_driver_info=delivery_driver_info or {}, order_items=items)

# /reviews GET
@app.route('/reviews')
def reviews_page():
    reviews = load_reviews()
    rating_filter_options = ['1', '2', '3', '4', '5']
    selected_rating = request.args.get('rating', '')
    filtered_reviews = reviews
    if selected_rating and selected_rating in rating_filter_options:
        rating_val = int(selected_rating)
        filtered_reviews = [r for r in reviews if r['rating'] == rating_val]
    return render_template('reviews.html', reviews=filtered_reviews, rating_filter_options=rating_filter_options, selected_rating=selected_rating)

# /reviews/write GET, POST
@app.route('/reviews/write', methods=['GET', 'POST'])
def write_review_page():
    if request.method == 'GET':
        return render_template('write_review.html')

    form_result = {}

    # Read form fields
    restaurant_id_str = request.form.get('restaurant_id', '').strip()
    customer_name = request.form.get('customer_name', '').strip()
    rating_str = request.form.get('rating', '').strip()
    review_text = request.form.get('review_text', '').strip()

    # Validate
    try:
        restaurant_id = int(restaurant_id_str)
    except ValueError:
        form_result['error'] = 'Invalid restaurant id.'
        return render_template('write_review.html', result=form_result)

    if not customer_name:
        form_result['error'] = 'Customer name is required.'
        return render_template('write_review.html', result=form_result)

    try:
        rating = int(rating_str)
        if rating < 1 or rating > 5:
            raise ValueError
    except ValueError:
        form_result['error'] = 'Rating must be an integer between 1 and 5.'
        return render_template('write_review.html', result=form_result)

    if not review_text:
        form_result['error'] = 'Review text is required.'
        return render_template('write_review.html', result=form_result)

    # Load existing reviews
    reviews = load_reviews()

    new_review_id = max((r['review_id'] for r in reviews), default=0) + 1
    review_date = datetime.today().strftime('%Y-%m-%d')

    # Append new review
    try:
        reviews_path = os.path.join(data_dir, 'reviews.txt')
        with open(reviews_path, 'a', encoding='utf-8') as f:
            line = f"{new_review_id}|{restaurant_id}|{customer_name}|{rating}|{review_text}|{review_date}\n"
            f.write(line)
    except Exception:
        form_result['error'] = 'Failed to save review. Please try again later.'
        return render_template('write_review.html', result=form_result)

    form_result['success'] = 'Review submitted successfully.'
    return render_template('write_review.html', result=form_result)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
