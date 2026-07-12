from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

DATA_DIR = 'data'

# Utility functions for reading and writing data

def read_users():
    users = []
    try:
        with open(os.path.join(DATA_DIR, 'users.txt'), 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) >= 4:
                    users.append({
                        'user_id': parts[0],
                        'username': parts[1],
                        'email': parts[2],
                        'password': parts[3]
                    })
    except FileNotFoundError:
        pass
    return users


def read_auctions():
    auctions = []
    try:
        with open(os.path.join(DATA_DIR, 'auctions.txt'), 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                # Expected 9 parts: id|title|description|category|starting_bid|current_bid|end_time|status|image_url
                if len(parts) >= 9:
                    auctions.append({
                        'auction_id': parts[0],
                        'title': parts[1],
                        'description': parts[2],
                        'category': parts[3],
                        'starting_bid': float(parts[4]),
                        'current_bid': float(parts[5]),
                        'end_time': parts[6],
                        'status': parts[7],
                        'image_url': parts[8]
                    })
    except FileNotFoundError:
        pass
    return auctions


def read_bids():
    bids = []
    try:
        with open(os.path.join(DATA_DIR, 'bids.txt'), 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) >= 4:
                    bids.append({
                        'bid_id': parts[0],
                        'auction_id': parts[1],
                        'bidder': parts[2],
                        'bid_amount': float(parts[3])
                    })
    except FileNotFoundError:
        pass
    return bids


def read_bid_history():
    bid_history = []
    try:
        with open(os.path.join(DATA_DIR, 'bid_history.txt'), 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) >= 5:
                    bid_history.append({
                        'history_id': parts[0],
                        'bid_id': parts[1],
                        'auction_id': parts[2],
                        'bidder': parts[3],
                        'bid_amount': float(parts[4])
                    })
    except FileNotFoundError:
        pass
    return bid_history


def write_users(users):
    with open(os.path.join(DATA_DIR, 'users.txt'), 'w') as f:
        for user in users:
            f.write(f"{user[\"user_id\"]}|{user[\"username\"]}|{user[\"email\"]}|{user[\"password\"]}\n")


def write_auctions(auctions):
    with open(os.path.join(DATA_DIR, 'auctions.txt'), 'w') as f:
        for auction in auctions:
            f.write(
                f"{auction[\"auction_id\"]}|{auction[\"title\"]}|{auction[\"description\"]}|{auction[\"category\"]}|"
                f"{auction[\"starting_bid\"]:.2f}|{auction[\"current_bid\"]:.2f}|{auction[\"end_time\"]}|{auction[\"status\"]}|{auction[\"image_url\"]}\n"
            )


def write_bids(bids):
    with open(os.path.join(DATA_DIR, 'bids.txt'), 'w') as f:
        for bid in bids:
            f.write(
                f"{bid[\"bid_id\"]}|{bid[\"auction_id\"]}|{bid[\"bidder\"]}|{bid[\"bid_amount\"]:.2f}\n"
            )


def write_bid_history(bid_history):
    with open(os.path.join(DATA_DIR, 'bid_history.txt'), 'w') as f:
        for h in bid_history:
            f.write(
                f"{h[\"history_id\"]}|{h[\"bid_id\"]}|{h[\"auction_id\"]}|{h[\"bidder\"]}|{h[\"bid_amount\"]:.2f}\n"
            )


# Routes and views

@app.route('/')
def index():
    auctions = read_auctions()
    return render_template('index.html', auctions=auctions)


@app.route('/auction/<auction_id>')
def auction_details(auction_id):
    auctions = read_auctions()
    auction = next((a for a in auctions if a['auction_id'] == auction_id), None)
    if not auction:
        return 'Auction not found', 404
    bids = [b for b in read_bids() if b['auction_id'] == auction_id]
    return render_template('auction.html', auction=auction, bids=bids)


@app.route('/bid', methods=['POST'])
def place_bid():
    auction_id = request.form.get('auction_id')
    bidder = request.form.get('bidder')
    bid_amount = request.form.get('bid_amount')

    try:
        bid_amount = float(bid_amount)
    except (ValueError, TypeError):
        return 'Invalid bid amount', 400

    auctions = read_auctions()
    bids = read_bids()
    auction = next((a for a in auctions if a['auction_id'] == auction_id), None)

    if not auction:
        return 'Auction not found', 404

    if bid_amount <= auction['current_bid']:
        return 'Bid amount must be higher than current bid', 400

    # Add new bid
    new_bid_id = str(len(bids) + 1)
    new_bid = {
        'bid_id': new_bid_id,
        'auction_id': auction_id,
        'bidder': bidder,
        'bid_amount': bid_amount
    }
    bids.append(new_bid)
    write_bids(bids)

    # Update auction current bid
    for a in auctions:
        if a['auction_id'] == auction_id:
            a['current_bid'] = bid_amount
            break
    write_auctions(auctions)

    return redirect(url_for('auction_details', auction_id=auction_id))


if __name__ == '__main__':
    app.run(debug=True)
