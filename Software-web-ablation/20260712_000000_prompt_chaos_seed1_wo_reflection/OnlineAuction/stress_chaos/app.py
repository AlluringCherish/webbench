import os
import threading
import logging
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Thread lock for file writes to prevent concurrency issues
file_write_lock = threading.Lock()

# Data loading utility with error handling
def load_data_from_file(filepath, expected_field_count):
    result = []
    if not os.path.exists(filepath):
        logging.warning(f"Data file {filepath} does not exist.")
        return result
    with open(filepath, 'r', encoding='utf-8') as f:
        for lineno, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != expected_field_count:
                logging.warning(f"File {filepath} line {lineno}: Expected {expected_field_count} fields but got {len(parts)}. Skipping line.")
                continue
            result.append(parts)
    return result

# Loading various data files
categories = {cid: cname for cid, cname in load_data_from_file('data/categories.txt', 2)}
items = {item_id: {'category_id': cat_id, 'name': name} for item_id, cat_id, name in load_data_from_file('data/items.txt', 3)}

auctions = {}
for auction_id, item_id, start_price, current_price, end_time, status in load_data_from_file('data/auctions.txt', 6):
    try:
        auctions[auction_id] = {
            'item_id': item_id,
            'start_price': float(start_price),
            'current_price': float(current_price),
            'end_time': end_time,
            'status': status
        }
    except ValueError as e:
        logging.warning(f"Parsing auction {auction_id}: {e}")

users = {}
for user_id, username, email in load_data_from_file('data/users.txt', 3):
    users[user_id] = {'username': username, 'email': email}

bids = {}
for bid_id, auction_id, user_id, bid_amount, bid_time in load_data_from_file('data/bids.txt', 5):
    try:
        bids[bid_id] = {
            'auction_id': auction_id,
            'user_id': user_id,
            'bid_amount': float(bid_amount),
            'bid_time': bid_time
        }
    except ValueError as e:
        logging.warning(f"Parsing bid {bid_id}: {e}")

bid_history = {}
for history_id, auction_id, user_id, bid_amount, bid_time in load_data_from_file('data/bid_history.txt', 5):
    try:
        bid_history[history_id] = {
            'auction_id': auction_id,
            'user_id': user_id,
            'bid_amount': float(bid_amount),
            'bid_time': bid_time
        }
    except ValueError as e:
        logging.warning(f"Parsing bid history {history_id}: {e}")

winners = {}
for auction_id, user_id, bid_amount in load_data_from_file('data/winners.txt', 3):
    try:
        winners[auction_id] = {
            'user_id': user_id,
            'bid_amount': float(bid_amount)
        }
    except ValueError as e:
        logging.warning(f"Parsing winner {auction_id}: {e}")

trending = {}
for auction_id, trend_score in load_data_from_file('data/trending.txt', 2):
    try:
        trending[auction_id] = float(trend_score)
    except ValueError as e:
        logging.warning(f"Parsing trending {auction_id}: {e}")

# Helper: Get auction info including item name and category
def get_auction_info(auction_id):
    auction = auctions.get(auction_id)
    if not auction:
        return None
    item = items.get(auction['item_id'], {'name': 'Unknown', 'category_id': None})
    category_name = categories.get(item['category_id'], 'Unknown Category')
    return {
        'auction_id': auction_id,
        'item_name': item['name'],
        'category_name': category_name,
        'start_price': auction['start_price'],
        'current_price': auction['current_price'],
        'end_time': auction['end_time'],
        'status': auction['status']
    }

# Routes
@app.route('/')
def dashboard():
    active_auctions = [get_auction_info(aid) for aid in auctions if auctions[aid]['status'] == 'active']
    active_auctions = [a for a in active_auctions if a]
    active_auctions.sort(key=lambda a: a['end_time'])
    featured_auctions = active_auctions[:3]
    return render_template('dashboard.html', active_auctions=active_auctions, featured_auctions=featured_auctions)

@app.route('/catalog')
def catalog():
    all_auctions = [get_auction_info(aid) for aid in auctions]
    all_auctions = [a for a in all_auctions if a]
    return render_template('catalog.html', auctions=all_auctions)

@app.route('/auction/<auction_id>')
def auction_details(auction_id):
    auction = auctions.get(auction_id)
    if not auction:
        return "Auction not found", 404
    item = items.get(auction['item_id'], {'name': 'Unknown'})
    category_name = categories.get(item.get('category_id', ''), 'Unknown Category')
    bids_for_auction = [b for b in bids.values() if b['auction_id'] == auction_id]
    bids_for_auction.sort(key=lambda b: b['bid_amount'], reverse=True)
    return render_template('auction.html', auction=auction, item_name=item['name'], category_name=category_name, bids=bids_for_auction, users=users, auction_id=auction_id)

@app.route('/auction/<auction_id>/bid', methods=['POST'])
def place_bid(auction_id):
    auction = auctions.get(auction_id)
    if not auction:
        return "Auction not found", 404

    user_id = request.form.get('user_id')
    bid_amount_str = request.form.get('bid_amount')

    if not user_id or user_id not in users:
        logging.info(f"Bid attempt by invalid user: {user_id}")
        return "Invalid user", 400

    try:
        bid_amount = float(bid_amount_str)
    except (TypeError, ValueError):
        logging.info(f"Invalid bid amount submitted: {bid_amount_str}")
        return "Invalid bid amount", 400

    min_bid = max(auction['current_price'], auction['start_price'])
    if bid_amount <= min_bid:
        logging.info(f"Bid too low: {bid_amount} <= {min_bid} for auction {auction_id}")
        return f"Bid must be higher than current highest bid ({min_bid})", 400

    # Critical section to prevent concurrency problems with file writes
    with file_write_lock:
        new_bid_id = str(len(bids) + 1)
        bids[new_bid_id] = {
            'auction_id': auction_id,
            'user_id': user_id,
            'bid_amount': bid_amount,
            'bid_time': ''
        }
        auction['current_price'] = bid_amount

        # Write bid to bids.txt and bid_history.txt
        try:
            with open('data/bids.txt', 'a', encoding='utf-8') as f_bid:
                f_bid.write(f"{new_bid_id}|{auction_id}|{user_id}|{bid_amount}|\n")
            with open('data/bid_history.txt', 'a', encoding='utf-8') as f_hist:
                f_hist.write(f"{new_bid_id}|{auction_id}|{user_id}|{bid_amount}|\n")
        except Exception as e:
            logging.error(f"Failed to save bid {new_bid_id} to file: {e}")
            return "Internal server error", 500

    logging.info(f"User {user_id} placed a bid of {bid_amount} on auction {auction_id}")
    return redirect(url_for('auction_details', auction_id=auction_id))

@app.route('/categories')
def list_categories():
    return render_template('categories.html', categories=categories)

# Additional routes can be implemented similarly...

if __name__ == '__main__':
    app.run(debug=True)
