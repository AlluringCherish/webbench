from flask import Flask, render_template, request
import os

app = Flask(__name__)

def load_data(filename):
    data = []
    filepath = os.path.join('data', filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) > 1:
                data.append(parts)
    return data

@app.route('/')
def index():
    auctions = load_data('auctions.txt')
    # auctions fields: auction_id|title|description
    auctions_list = [{'id': a[0], 'title': a[1], 'description': a[2]} for a in auctions]
    return render_template('index.html', auctions=auctions_list)

@app.route('/auction/<auction_id>')
def auction_detail(auction_id):
    auctions = load_data('auctions.txt')
    auction = next((a for a in auctions if a[0] == auction_id), None)
    if not auction:
        return "Auction not found", 404

    auction_detail = {'id': auction[0], 'title': auction[1], 'description': auction[2]}

    bids = load_data('bids.txt')
    # bids fields: bid_id|auction_id|bidder|amount
    auction_bids = [
        {'bid_id': b[0], 'auction_id': b[1], 'bidder': b[2], 'amount': float(b[3])}
        for b in bids if b[1] == auction_id
    ]

    return render_template('auction.html', auction=auction_detail, bids=auction_bids)

@app.route('/bid', methods=['POST'])
def place_bid():
    auction_id = request.form.get('auction_id')
    bidder = request.form.get('bidder')
    amount = request.form.get('amount')

    if not auction_id or not bidder or not amount:
        return "Missing data", 400

    try:
        amount_val = float(amount)
    except ValueError:
        return "Invalid bid amount", 400

    # Validate auction exists
    auctions = load_data('auctions.txt')
    if not any(a[0] == auction_id for a in auctions):
        return "Auction not found", 404

    # Load current bids for auction to check if new bid is higher
    bids = load_data('bids.txt')
    auction_bids = [b for b in bids if b[1] == auction_id]
    if auction_bids:
        max_bid = max(float(b[3]) for b in auction_bids)
        if amount_val <= max_bid:
            return "Bid must be higher than current highest bid", 400

    # Add new bid
    new_bid_id = str(len(bids) + 1)
    new_bid_line = f"{new_bid_id}|{auction_id}|{bidder}|{amount_val}\n"
    with open(os.path.join('data', 'bids.txt'), 'a', encoding='utf-8') as f:
        f.write(new_bid_line)

    return "Bid placed successfully", 200

if __name__ == '__main__':
    app.run(debug=True)
