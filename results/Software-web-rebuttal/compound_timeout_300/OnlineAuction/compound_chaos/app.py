from flask import Flask, render_template, request, redirect, url_for, abort, flash
import os

app = Flask(__name__)
app.secret_key = 'replace_with_secure_key'

DATA_DIR = 'data'

# Load auctions from text file

def load_auctions():
    auctions = {}
    try:
        with open(os.path.join(DATA_DIR, 'auctions.txt'), 'r', encoding='utf-8') as file:
            for line in file:
                parts = line.strip().split('|')
                if len(parts) != 7:
                    continue
                auction_id, title, starting_price, category_id, status, seller, description = parts
                auctions[auction_id] = {
                    'id': auction_id,
                    'title': title,
                    'starting_price': float(starting_price),
                    'category_id': category_id,
                    'status': status,
                    'seller': seller,
                    'description': description,
                    'bids': []
                }
    except Exception:
        pass
    return auctions

# Load categories from file

def load_categories():
    categories = {}
    try:
        with open(os.path.join(DATA_DIR, 'categories.txt'), 'r', encoding='utf-8') as file:
            for line in file:
                parts = line.strip().split('|')
                if len(parts) != 2:
                    continue
                category_id, category_name = parts
                categories[category_id] = category_name
    except Exception:
        pass
    return categories

# Load bids from file

def load_bids():
    bids = []
    try:
        with open(os.path.join(DATA_DIR, 'bids.txt'), 'r', encoding='utf-8') as file:
            for line in file:
                parts = line.strip().split('|')
                if len(parts) != 4:
                    continue
                bid_id, auction_id, bidder, amount_str = parts
                try:
                    amount = float(amount_str)
                except ValueError:
                    continue
                bids.append({
                    'id': bid_id,
                    'auction_id': auction_id,
                    'bidder': bidder,
                    'amount': amount
                })
    except Exception:
        pass
    return bids


# Load data on startup
auctions = load_auctions()
categories = load_categories()
bids = load_bids()

# Assign bids to auctions
for bid in bids:
    auction = auctions.get(bid['auction_id'])
    if auction:
        auction['bids'].append(bid)


@app.route('/')
def index():
    return render_template('index.html', auctions=auctions.values(), categories=categories)


@app.route('/auction/<auction_id>')
def auction_detail(auction_id):
    auction = auctions.get(auction_id)
    if not auction:
        abort(404, description='Auction not found')
    return render_template('auction_detail.html', auction=auction, categories=categories)


@app.route('/auction/<auction_id>/place_bid', methods=['GET', 'POST'])
def place_bid(auction_id):
    auction = auctions.get(auction_id)
    if not auction:
        abort(404, description='Auction not found')

    if auction['status'].lower() != 'open':
        flash('This auction is not open for bidding.')
        return redirect(url_for('auction_detail', auction_id=auction_id))

    if request.method == 'POST':
        bidder = request.form.get('bidder', '').strip()
        amount_str = request.form.get('amount', '').strip()

        if not bidder:
            flash('Bidder name is required.')
            return render_template('place_bid.html', auction=auction)

        try:
            amount = float(amount_str)
        except ValueError:
            flash('Invalid bid amount.')
            return render_template('place_bid.html', auction=auction)

        current_max = max((bid['amount'] for bid in auction['bids']), default=auction['starting_price'])
        if amount <= current_max:
            flash(f'Bid must be higher than the current highest bid ({current_max}).')
            return render_template('place_bid.html', auction=auction)

        new_bid_id = str(len(bids) + 1)
        new_bid = {
            'id': new_bid_id,
            'auction_id': auction_id,
            'bidder': bidder,
            'amount': amount
        }

        bids.append(new_bid)
        auction['bids'].append(new_bid)

        try:
            with open(os.path.join(DATA_DIR, 'bids.txt'), 'a', encoding='utf-8') as file:
                file.write(f"{new_bid_id}|{auction_id}|{bidder}|{amount}\n")
        except Exception:
            bids.pop()
            auction['bids'].pop()
            flash('Failed to save bid. Please try again later.')
            return render_template('place_bid.html', auction=auction)

        return redirect(url_for('auction_detail', auction_id=auction_id))

    return render_template('place_bid.html', auction=auction)


@app.route('/categories')
def categories():
    return render_template('categories.html', categories=categories)


@app.route('/category/<category_id>')
def auctions_by_category(category_id):
    if category_id not in categories:
        abort(404, description='Category not found')
    filtered_auctions = [a for a in auctions.values() if a['category_id'] == category_id]
    return render_template('category_auctions.html', auctions=filtered_auctions, category=categories[category_id])


@app.route('/bid/history')
def bid_history():
    try:
        sorted_bids = sorted(bids, key=lambda b: int(b['id']))
    except Exception:
        sorted_bids = bids
    return render_template('bid_history.html', bids=sorted_bids, auctions=auctions)


@app.route('/winners')
def winners():
    winners_list = []
    for auction in auctions.values():
        if auction['status'].lower() == 'closed' and auction['bids']:
            highest_bid = max(auction['bids'], key=lambda b: b['amount'])
            winners_list.append({'auction': auction, 'winner_bid': highest_bid})
    return render_template('winners.html', winners=winners_list)


@app.route('/trending')
def trending():
    sorted_auctions = sorted(auctions.values(), key=lambda a: len(a['bids']), reverse=True)
    return render_template('trending.html', auctions=sorted_auctions[:10])


@app.route('/status/<status_filter>')
def status_filter(status_filter):
    filtered_auctions = [a for a in auctions.values() if a['status'].lower() == status_filter.lower()]
    return render_template('status.html', auctions=filtered_auctions, status=status_filter)


@app.errorhandler(404)
def error_404(error):
    message = getattr(error, 'description', 'Resource not found')
    return render_template('404.html', message=message), 404


if __name__ == '__main__':
    app.run(debug=True)
