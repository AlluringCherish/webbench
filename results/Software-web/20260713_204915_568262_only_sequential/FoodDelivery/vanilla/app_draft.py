from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)
DATA_DIR = 'data'

# Helper functions to read data files

def read_restaurants():
    restaurants = []
    try:
        with open(os.path.join(DATA_DIR, 'restaurants.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 8:
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
    except Exception as e:
        print(f'Error reading restaurants.txt: {e}')
    return restaurants


def read_menus():
    menus = []
    try:
        with open(os.path.join(DATA_DIR, 'menus.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 7:
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
    except Exception as e:
        print(f'Error reading menus.txt: {e}')
    return menus


def read_cart():
    cart = []
    try:
        with open(os.path.join(DATA_DIR, 'cart.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 5:
                    entry = {
                        'cart_id': int(parts[0]),
                        'item_id': int(parts[1]),
                        'restaurant_id': int(parts[2]),
                        'quantity': int(parts[3]),
                        'added_date': parts[4]
                    }
                    cart.append(entry)
    except Exception as e:
        print(f'Error reading cart.txt: {e}')
    return cart


def write_cart(cart):
    try:
        with open(os.path.join(DATA_DIR, 'cart.txt'), 'w', encoding='utf-8') as f:
            for entry in cart:
                line = f"{entry['cart_id']}|{entry['item_id']}|{entry['restaurant_id']}|{entry['quantity']}|{entry['added_date']}\n"
                f.write(line)
    except Exception as e:
        print(f'Error writing cart.txt: {e}')


def read_orders():
    orders = []
    try:
        with open(os.path.join(DATA_DIR, 'orders.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 8:
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
    except Exception as e:
        print(f'Error reading orders.txt: {e}')
    return orders


def write_orders(orders):
    try:
        with open(os.path.join(DATA_DIR, 'orders.txt'), 'w', encoding='utf-8') as f:
            for order in orders:
                line = f"{order['order_id']}|{order['customer_name']}|{order['restaurant_id']}|{order['order_date']}|{order['total_amount']}|{order['status']}|{order['delivery_address']}|{order['phone_number']}\n"
                f.write(line)
    except Exception as e:
        print(f'Error writing orders.txt: {e}')


def read_order_items():
    order_items = []
    try:
        with open(os.path.join(DATA_DIR, 'order_items.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 5:
                    oi = {
                        'order_item_id': int(parts[0]),
                        'order_id': int(parts[1]),
                        'item_id': int(parts[2]),
                        'quantity': int(parts[3]),
                        'price': float(parts[4])
                    }
                    order_items.append(oi)
    except Exception as e:
        print(f'Error reading order_items.txt: {e}')
    return order_items


def write_order_items(order_items):
    try:
        with open(os.path.join(DATA_DIR, 'order_items.txt'), 'w', encoding='utf-8') as f:
            for oi in order_items:
                line = f"{oi['order_item_id']}|{oi['order_id']}|{oi['item_id']}|{oi['quantity']}|{oi['price']}\n"
                f.write(line)
    except Exception as e:
        print(f'Error writing order_items.txt: {e}')


def read_deliveries():
    deliveries = []
    try:
        with open(os.path.join(DATA_DIR, 'deliveries.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 7:
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
    except Exception as e:
        print(f'Error reading deliveries.txt: {e}')
    return deliveries


def read_reviews():
    reviews = []
    try:
        with open(os.path.join(DATA_DIR, 'reviews.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 6:
                    review = {
                        'review_id': int(parts[0]),
                        'restaurant_id': int(parts[1]),
                        'customer_name': parts[2],
                        'rating': int(parts[3]),
                        'review_text': parts[4],
                        'review_date': parts[5]
                    }
                    reviews.append(review)
    except Exception as e:
        print(f'Error reading reviews.txt: {e}')
    return reviews

# Flask Routes

# 1. Dashboard View
@app.route('/dashboard')
def dashboard_view():
    restaurants = read_restaurants()
    # We can show top 3 rated restaurants as featured
    featured = sorted(restaurants, key=lambda r: r['rating'], reverse=True)[:3]
    return render_template('templates_draft/dashboard.html', featured_restaurants=featured)

# 2. Restaurant Listing Page
@app.route('/restaurants')
def restaurant_listing_view():
    restaurants = read_restaurants()
    cuisines = sorted(set(r['cuisine'] for r in restaurants))
    search_query = request.args.get('search', '')
    cuisine_filter = request.args.get('cuisine', '')

    filtered = restaurants
    if search_query:
        filtered = [r for r in filtered if search_query.lower() in r['name'].lower() or search_query.lower() in r['cuisine'].lower()]
    if cuisine_filter and cuisine_filter.lower() != 'all':
        filtered = [r for r in filtered if r['cuisine'].lower() == cuisine_filter.lower()]

    return render_template('templates_draft/restaurants.html', restaurants=filtered, cuisines=cuisines, selected_cuisine=cuisine_filter, search_query=search_query)

# 3. Restaurant Menu Page
@app.route('/menu/<int:restaurant_id>')
def restaurant_menu_view(restaurant_id):
    restaurants = read_restaurants()
    menus = read_menus()
    restaurant = next((r for r in restaurants if r['restaurant_id'] == restaurant_id), None)
    if not restaurant:
        return "Restaurant not found", 404
    items = [m for m in menus if m['restaurant_id'] == restaurant_id and m['availability'] == 1]
    return render_template('templates_draft/menu.html', restaurant=restaurant, menu_items=items)

# 4. Item Details Page
@app.route('/item/<int:item_id>')
def item_details_view(item_id):
    menus = read_menus()
    item = next((m for m in menus if m['item_id'] == item_id), None)
    if not item:
        return "Item not found", 404
    return render_template('templates_draft/item_details.html', item=item)

# 5. Shopping Cart Page - GET and POST
@app.route('/cart', methods=['GET','POST'])
def shopping_cart_view():
    if request.method == 'POST':
        cart = read_cart()
        # Updating quantities or removing items
        for entry in cart[:]:
            item_id_str = str(entry['item_id'])
            quantity_key = f'update-quantity-{item_id_str}'
            remove_key = f'remove-item-button-{item_id_str}'

            if remove_key in request.form:
                # Remove item from cart
                cart.remove(entry)
            elif quantity_key in request.form:
                try:
                    qty = int(request.form[quantity_key])
                    if qty > 0:
                        entry['quantity'] = qty
                    else:
                        # If qty <=0 remove item
                        cart.remove(entry)
                except:
                    pass
        write_cart(cart)
        return redirect(url_for('shopping_cart_view'))
    else:
        cart = read_cart()
        menus = read_menus()
        restaurants = {r['restaurant_id']: r for r in read_restaurants()}
        # prepare cart items detail list
        cart_items = []
        total_amount = 0.0
        for c in cart:
            item = next((i for i in menus if i['item_id'] == c['item_id']), None)
            if item:
                subtotal = item['price'] * c['quantity']
                total_amount += subtotal
                cart_items.append({
                    'item_id': c['item_id'],
                    'item_name': item['item_name'],
                    'quantity': c['quantity'],
                    'price': item['price'],
                    'subtotal': subtotal
                })
        return render_template('templates_draft/cart.html', cart_items=cart_items, total_amount=total_amount)

# 6. Add to Cart endpoint
@app.route('/add-to-cart', methods=['POST'])
def add_to_cart():
    try:
        item_id = int(request.form.get('item_id'))
        quantity = int(request.form.get('quantity', 1))
    except:
        return redirect(url_for('dashboard_view'))

    menus = read_menus()
    item = next((m for m in menus if m['item_id'] == item_id), None)
    if not item or item['availability'] != 1:
        return redirect(url_for('dashboard_view'))

    cart = read_cart()

    # Check if item already in cart, increment quantity
    existing = next((c for c in cart if c['item_id'] == item_id), None)
    if existing:
        existing['quantity'] += quantity
    else:
        new_cart_id = max([c['cart_id'] for c in cart], default=0) + 1
        cart.append({
            'cart_id': new_cart_id,
            'item_id': item_id,
            'restaurant_id': item['restaurant_id'],
            'quantity': quantity,
            'added_date': datetime.now().strftime('%Y-%m-%d')
        })

    write_cart(cart)
    return redirect(url_for('shopping_cart_view'))

# 7. Checkout Page
@app.route('/checkout', methods=['GET','POST'])
def checkout_view():
    if request.method == 'POST':
        customer_name = request.form.get('customer-name', '').strip()
        delivery_address = request.form.get('delivery-address', '').strip()
        phone_number = request.form.get('phone-number', '').strip()
        payment_method = request.form.get('payment-method', '').strip()

        if not all([customer_name, delivery_address, phone_number, payment_method]):
            return "All fields are required", 400

        cart = read_cart()
        if not cart:
            return "Cart is empty", 400

        menus = read_menus()

        # Calculate total amount
        total_amount = 0.0
        for c in cart:
            item = next((i for i in menus if i['item_id'] == c['item_id']), None)
            if item:
                total_amount += item['price'] * c['quantity']

        # Create new order
        orders = read_orders()
        new_order_id = max([o['order_id'] for o in orders], default=0) + 1
        order_date = datetime.now().strftime('%Y-%m-%d')

        # Here status starts as "Preparing"
        new_order = {
            'order_id': new_order_id,
            'customer_name': customer_name,
            'restaurant_id': cart[0]['restaurant_id'] if cart else 0,
            'order_date': order_date,
            'total_amount': total_amount,
            'status': 'Preparing',
            'delivery_address': delivery_address,
            'phone_number': phone_number
        }
        orders.append(new_order)
        write_orders(orders)

        # Write order items
        order_items = read_order_items()
        # Assign order_item_id continuing
        next_order_item_id = max([oi['order_item_id'] for oi in order_items], default=0) + 1
        menus_dict = {m['item_id']: m for m in menus}
        for c in cart:
            item = menus_dict.get(c['item_id'])
            if item:
                order_items.append({
                    'order_item_id': next_order_item_id,
                    'order_id': new_order_id,
                    'item_id': c['item_id'],
                    'quantity': c['quantity'],
                    'price': item['price']
                })
                next_order_item_id += 1
        write_order_items(order_items)

        # Clear cart
        write_cart([])

        return redirect(url_for('active_orders_view'))
    else:
        return render_template('templates_draft/checkout.html')

# 8. Active Orders Page
@app.route('/active-orders')
def active_orders_view():
    orders = read_orders()
    restaurants = {r['restaurant_id']: r for r in read_restaurants()}
    status_filter = request.args.get('status', 'All')
    filtered_orders = orders
    if status_filter and status_filter.lower() != 'all':
        filtered_orders = [o for o in filtered_orders if o['status'].lower() == status_filter.lower()]

    # For each order, also fetch ETA from deliveries if available
    deliveries = read_deliveries()
    orders_info = []
    for o in filtered_orders:
        restaurant = restaurants.get(o['restaurant_id'], {})
        delivery = next((d for d in deliveries if d['order_id'] == o['order_id']), None)
        eta = delivery['estimated_time'] if delivery else 'N/A'
        orders_info.append({
            'order_id': o['order_id'],
            'restaurant_name': restaurant.get('name', ''),
            'status': o['status'],
            'eta': eta
        })
    return render_template('templates_draft/active_orders.html', orders=orders_info, selected_status=status_filter)

# 9. Order Tracking Page
@app.route('/track-order/<int:order_id>')
def order_tracking_view(order_id):
    orders = read_orders()
    order = next((o for o in orders if o['order_id'] == order_id), None)
    if not order:
        return "Order not found", 404
    restaurants = {r['restaurant_id']: r for r in read_restaurants()}
    restaurant = restaurants.get(order['restaurant_id'], {})

    order_items = [oi for oi in read_order_items() if oi['order_id'] == order_id]
    menus = {m['item_id']: m for m in read_menus()}
    detailed_items = []
    for oi in order_items:
        item = menus.get(oi['item_id'])
        if item:
            detailed_items.append({
                'item_name': item['item_name'],
                'quantity': oi['quantity'],
                'price': oi['price']
            })

    deliveries = [d for d in read_deliveries() if d['order_id'] == order_id]
    delivery_info = deliveries[0] if deliveries else None

    return render_template('templates_draft/tracking.html', order=order, restaurant=restaurant,
                           order_items=detailed_items, delivery=delivery_info)

# 10. Reviews Page
@app.route('/reviews', methods=['GET','POST'])
def reviews_view():
    if request.method == 'POST':
        # Handle new review submission
        restaurant_id = request.form.get('restaurant_id')
        customer_name = request.form.get('customer_name', '').strip()
        rating = request.form.get('rating')
        review_text = request.form.get('review_text', '').strip()

        if not all([restaurant_id, customer_name, rating, review_text]):
            return "All fields are required", 400

        try:
            restaurant_id = int(restaurant_id)
            rating = int(rating)
            if rating < 1 or rating > 5:
                return "Rating must be between 1 and 5", 400
        except:
            return "Invalid input", 400

        reviews = read_reviews()
        new_id = max([r['review_id'] for r in reviews], default=0) + 1
        new_review = {
            'review_id': new_id,
            'restaurant_id': restaurant_id,
            'customer_name': customer_name,
            'rating': rating,
            'review_text': review_text,
            'review_date': datetime.now().strftime('%Y-%m-%d')
        }
        reviews.append(new_review)

        try:
            with open(os.path.join(DATA_DIR, 'reviews.txt'), 'w', encoding='utf-8') as f:
                for r in reviews:
                    line = f"{r['review_id']}|{r['restaurant_id']}|{r['customer_name']}|{r['rating']}|{r['review_text']}|{r['review_date']}\n"
                    f.write(line)
        except Exception as e:
            print(f'Error writing reviews.txt: {e}')

        return redirect(url_for('reviews_view'))

    else:
        reviews = read_reviews()
        restaurants = {r['restaurant_id']: r for r in read_restaurants()}
        filter_rating = request.args.get('rating', 'All')

        filtered_reviews = reviews
        if filter_rating and filter_rating.lower() != 'all':
            try:
                filter_rating_int = int(filter_rating)
                filtered_reviews = [r for r in filtered_reviews if r['rating'] == filter_rating_int]
            except:
                pass

        # Attach restaurant name to review display
        display_reviews = []
        for r in filtered_reviews:
            rest = restaurants.get(r['restaurant_id'], {})
            display_reviews.append({
                'review_id': r['review_id'],
                'restaurant_name': rest.get('name', ''),
                'customer_name': r['customer_name'],
                'rating': r['rating'],
                'review_text': r['review_text'],
                'review_date': r['review_date']
            })

        return render_template('templates_draft/reviews.html', reviews=display_reviews, selected_rating=filter_rating)


if __name__ == '__main__':
    app.run(debug=True)
