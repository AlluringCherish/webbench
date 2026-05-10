'''
Utility functions for BookstoreOnline web application.
Handles reading and writing data from/to text files.
'''
import os
import datetime
DATA_DIR = 'data'
def read_books():
    books = []
    path = os.path.join(DATA_DIR, 'books.txt')
    if not os.path.exists(path):
        return books
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) < 8:
                continue
            book = {
                'book_id': int(parts[0]),
                'title': parts[1],
                'author': parts[2],
                'isbn': parts[3],
                'category': parts[4],
                'price': float(parts[5]),
                'stock': int(parts[6]),
                'description': parts[7]
            }
            books.append(book)
    return books
def read_categories():
    categories = []
    path = os.path.join(DATA_DIR, 'categories.txt')
    if not os.path.exists(path):
        return categories
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) < 3:
                continue
            category = {
                'category_id': int(parts[0]),
                'category_name': parts[1],
                'description': parts[2]
            }
            categories.append(category)
    return categories
def read_cart():
    cart_items = []
    path = os.path.join(DATA_DIR, 'cart.txt')
    if not os.path.exists(path):
        return cart_items
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) < 4:
                continue
            cart_item = {
                'cart_id': int(parts[0]),
                'book_id': int(parts[1]),
                'quantity': int(parts[2]),
                'added_date': parts[3]
            }
            cart_items.append(cart_item)
    return cart_items
def update_cart_item(cart_id, quantity):
    cart_items = read_cart()
    updated = False
    for item in cart_items:
        if item['cart_id'] == cart_id:
            if quantity <= 0:
                # Remove item if quantity zero or less
                cart_items.remove(item)
            else:
                item['quantity'] = quantity
            updated = True
            break
    if updated:
        write_cart(cart_items)
def remove_cart_item(cart_id):
    cart_items = read_cart()
    cart_items = [item for item in cart_items if item['cart_id'] != cart_id]
    write_cart(cart_items)
def write_cart(cart_items):
    path = os.path.join(DATA_DIR, 'cart.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for item in cart_items:
            line = f"{item['cart_id']}|{item['book_id']}|{item['quantity']}|{item['added_date']}\n"
            f.write(line)
def calculate_cart_total(cart_items):
    books = read_books()
    total = 0.0
    for item in cart_items:
        book = next((b for b in books if b['book_id'] == item['book_id']), None)
        if book:
            total += book['price'] * item['quantity']
    return round(total, 2)
def add_to_cart(book_id, quantity):
    cart_items = read_cart()
    # Check if book already in cart
    for item in cart_items:
        if item['book_id'] == book_id:
            item['quantity'] += quantity
            write_cart(cart_items)
            return
    # Add new cart item
    new_id = max([item['cart_id'] for item in cart_items], default=0) + 1
    added_date = datetime.date.today().isoformat()
    cart_items.append({'cart_id': new_id, 'book_id': book_id, 'quantity': quantity, 'added_date': added_date})
    write_cart(cart_items)
def read_orders():
    orders = []
    path = os.path.join(DATA_DIR, 'orders.txt')
    if not os.path.exists(path):
        return orders
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) < 6:
                continue
            order = {
                'order_id': int(parts[0]),
                'customer_name': parts[1],
                'order_date': parts[2],
                'total_amount': float(parts[3]),
                'status': parts[4],
                'shipping_address': parts[5]
            }
            orders.append(order)
    return orders
def place_order(customer_name, shipping_address, payment_method):
    cart_items = read_cart()
    if not cart_items:
        return None
    books = read_books()
    total_amount = 0.0
    for item in cart_items:
        book = next((b for b in books if b['book_id'] == item['book_id']), None)
        if book:
            total_amount += book['price'] * item['quantity']
    total_amount = round(total_amount, 2)
    orders = read_orders()
    new_order_id = max([o['order_id'] for o in orders], default=0) + 1
    order_date = datetime.date.today().isoformat()
    status = 'Pending'
    # Append new order
    path_orders = os.path.join(DATA_DIR, 'orders.txt')
    with open(path_orders, 'a', encoding='utf-8') as f:
        line = f"{new_order_id}|{customer_name}|{order_date}|{total_amount}|{status}|{shipping_address}\n"
        f.write(line)
    # Append order items
    path_order_items = os.path.join(DATA_DIR, 'order_items.txt')
    order_items = []
    if os.path.exists(path_order_items):
        with open(path_order_items, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    order_items.append(line)
    new_order_item_id = 1
    if order_items:
        last_line = order_items[-1]
        last_id = int(last_line.split('|')[0])
        new_order_item_id = last_id + 1
    with open(path_order_items, 'a', encoding='utf-8') as f:
        for item in cart_items:
            book = next((b for b in books if b['book_id'] == item['book_id']), None)
            if book:
                line = f"{new_order_item_id}|{new_order_id}|{book['book_id']}|{item['quantity']}|{book['price']}\n"
                f.write(line)
                new_order_item_id += 1
    return new_order_id
def clear_cart():
    path = os.path.join(DATA_DIR, 'cart.txt')
    if os.path.exists(path):
        os.remove(path)
def read_reviews(book_id=None):
    reviews = []
    path = os.path.join(DATA_DIR, 'reviews.txt')
    if not os.path.exists(path):
        return reviews
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) < 6:
                continue
            review = {
                'review_id': int(parts[0]),
                'book_id': int(parts[1]),
                'customer_name': parts[2],
                'rating': int(parts[3]),
                'review_text': parts[4],
                'review_date': parts[5]
            }
            if book_id is None or review['book_id'] == book_id:
                reviews.append(review)
    return reviews
def add_review(book_id, customer_name, rating, review_text):
    reviews = read_reviews()
    new_review_id = max([r['review_id'] for r in reviews], default=0) + 1
    review_date = datetime.date.today().isoformat()
    path = os.path.join(DATA_DIR, 'reviews.txt')
    with open(path, 'a', encoding='utf-8') as f:
        line = f"{new_review_id}|{book_id}|{customer_name}|{rating}|{review_text}|{review_date}\n"
        f.write(line)
def read_bestsellers(period='This Month'):
    bestsellers = []
    path = os.path.join(DATA_DIR, 'bestsellers.txt')
    if not os.path.exists(path):
        return bestsellers
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) < 3:
                continue
            if parts[2] == period:
                bestsellers.append({
                    'book_id': int(parts[0]),
                    'sales_count': int(parts[1]),
                    'period': parts[2]
                })
    # Sort descending by sales_count
    bestsellers.sort(key=lambda x: x['sales_count'], reverse=True)
    return bestsellers