import os
from flask import Flask, render_template, request, redirect, url_for, jsonify, abort

app = Flask(__name__)

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

# Utility functions to load data from text files

def load_users():
    users = {}
    try:
        with open(os.path.join(DATA_DIR, 'users.txt')) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                user_id, username, email = line.split(',')
                users[user_id] = {'id': user_id, 'username': username, 'email': email}
    except Exception as e:
        print(f"Error loading users: {e}")
    return users


def load_items():
    items = {}
    try:
        with open(os.path.join(DATA_DIR, 'items.txt')) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                parts = line.split(',')
                # Expected format: item_id, name, description, starting_price
                if len(parts) < 4:
                    continue
                item_id, name, description, starting_price = parts[0], parts[1], parts[2], parts[3]
                items[item_id] = {'id': item_id, 'name': name, 'description': description, 'starting_price': float(starting_price)}
    except Exception as e:
        print(f"Error loading items: {e}")
    return items


def load_bids():
    bids = {}
    try:
        with open(os.path.join(DATA_DIR, 'bids.txt')) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                parts = line.split(',')
                # Expected format: bid_id, item_id, user_id, bid_amount
                if len(parts) < 4:
                    continue
                bid_id, item_id, user_id, bid_amount = parts[0], parts[1], parts[2], parts[3]
                bid_amount = float(bid_amount)
                if item_id not in bids:
                    bids[item_id] = []
                bids[item_id].append({'bid_id': bid_id, 'item_id': item_id, 'user_id': user_id, 'bid_amount': bid_amount})
    except Exception as e:
        print(f"Error loading bids: {e}")
    return bids


# Routes
@app.route('/')
def index():
    items = load_items()
    return render_template('index.html', items=items.values())


@app.route('/item/<item_id>')
def item_detail(item_id):
    items = load_items()
    users = load_users()
    bids = load_bids()

    item = items.get(item_id)
    if not item:
        abort(404, description="Item not found")

    item_bids = bids.get(item_id, [])
    # Sort bids descending by bid_amount
    item_bids = sorted(item_bids, key=lambda b: b['bid_amount'], reverse=True)
    # Enhance bid info with user info
    for bid in item_bids:
        bid['user'] = users.get(bid['user_id'], {'username': 'Unknown'})

    return render_template('item_detail.html', item=item, bids=item_bids)


@app.route('/bid', methods=['POST'])
def place_bid():
    item_id = request.form.get('item_id')
    user_id = request.form.get('user_id')
    bid_amount = request.form.get('bid_amount')

    if not item_id or not user_id or not bid_amount:
        return jsonify({'error': 'Missing required parameters'}), 400

    try:
        bid_amount = float(bid_amount)
    except ValueError:
        return jsonify({'error': 'Invalid bid amount'}), 400

    items = load_items()
    users = load_users()
    bids = load_bids()

    if item_id not in items:
        return jsonify({'error': 'Invalid item id'}), 400
    if user_id not in users:
        return jsonify({'error': 'Invalid user id'}), 400

    # Check if bid is higher than current highest bid or starting_price
    current_bids = bids.get(item_id, [])
    highest_bid_amount = max([b['bid_amount'] for b in current_bids], default=items[item_id]['starting_price'])
    if bid_amount <= highest_bid_amount:
        return jsonify({'error': f'Bid must be higher than current highest bid ({highest_bid_amount})'}), 400

    # Add new bid to bids.txt
    try:
        # Generate new unique bid id
        existing_bid_ids = set()
        for b_list in bids.values():
            for b in b_list:
                existing_bid_ids.add(int(b['bid_id']))
        new_bid_id = str(max(existing_bid_ids) + 1 if existing_bid_ids else 1)

        with open(os.path.join(DATA_DIR, 'bids.txt'), 'a') as f:
            # Save bid as: bid_id,item_id,user_id,bid_amount
            f.write(f"{new_bid_id},{item_id},{user_id},{bid_amount}\n")
    except Exception as e:
        return jsonify({'error': f'Failed to save bid: {e}'}), 500

    return redirect(url_for('item_detail', item_id=item_id))


if __name__ == '__main__':
    app.run(debug=True)
