from flask import Flask, render_template, abort
import os

app = Flask(__name__)
DATA_DIR = 'data'

# Helper function to verify existence of required data files

def load_file_lines(filename):
    filepath = os.path.join(DATA_DIR, filename)
    if not os.path.isfile(filepath):
        return None
    lines = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                clean_line = line.strip()
                if clean_line:
                    lines.append(clean_line)
    except Exception:
        return None
    return lines


def load_auctions():
    lines = load_file_lines('auction.txt')
    if lines is None:
        # Return empty so app won't break
        return []
    auctions = []
    for line in lines:
        parts = line.split('|')
        if len(parts) < 5:
            continue
        auction_id, title, description, starting_bid, seller = parts
        try:
            starting_bid_val = float(starting_bid)
        except ValueError:
            starting_bid_val = 0.0
        auctions.append({
            'auction_id': auction_id,
            'title': title,
            'description': description,
            'starting_bid': starting_bid_val,
            'seller': seller
        })
    return auctions


def load_users():
    lines = load_file_lines('users.txt')
    if lines is None:
        return []
    users = []
    for line in lines:
        parts = line.split('|')
        if len(parts) < 3:
            continue
        user_id, username, email = parts
        users.append({
            'user_id': user_id,
            'username': username,
            'email': email
        })
    return users


def load_bids():
    lines = load_file_lines('bids.txt')
    if lines is None:
        return []
    bids = []
    for line in lines:
        parts = line.split('|')
        if len(parts) < 4:
            continue
        bid_id, auction_id, user_id, amount = parts
        try:
            amount_val = float(amount)
        except ValueError:
            amount_val = 0.0
        bids.append({
            'bid_id': bid_id,
            'auction_id': auction_id,
            'user_id': user_id,
            'amount': amount_val
        })
    return bids


@app.route('/')
def index():
    auctions = load_auctions()
    if not auctions:
        return "Error: required data file 'auction.txt' missing or empty.", 500
    return render_template('index.html', auctions=auctions)


@app.route('/auction/<auction_id>')
def auction_detail(auction_id):
    auctions = load_auctions()
    if not auctions:
        return "Error: required data file 'auction.txt' missing or empty.", 500
    auction = next((a for a in auctions if a['auction_id'] == auction_id), None)
    if not auction:
        return "Auction not found", 404

    bids = load_bids()
    users = load_users()
    if not users:
        return "Error: required data file 'users.txt' missing or empty.", 500
    auction_bids = [b for b in bids if b['auction_id'] == auction_id]

    user_lookup = {u['user_id']: u for u in users}

    for bid in auction_bids:
        bid['user'] = user_lookup.get(bid['user_id'], {'username': 'Unknown'})

    return render_template('auction_detail.html', auction=auction, bids=auction_bids)


@app.route('/user/<user_id>')
def user_profile(user_id):
    users = load_users()
    if not users:
        return "Error: required data file 'users.txt' missing or empty.", 500
    user = next((u for u in users if u['user_id'] == user_id), None)
    if not user:
        return "User not found", 404

    bids = load_bids()
    auctions = load_auctions()
    if not auctions:
        return "Error: required data file 'auction.txt' missing or empty.", 500
    user_bids = [b for b in bids if b['user_id'] == user_id]

    auction_lookup = {a['auction_id']: a for a in auctions}
    for bid in user_bids:
        bid['auction'] = auction_lookup.get(bid['auction_id'], {'title': 'Unknown'})

    return render_template('user_profile.html', user=user, bids=user_bids)


if __name__ == '__main__':
    app.run(debug=True)
