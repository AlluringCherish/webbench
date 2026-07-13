from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import os

app = Flask(__name__)
DATA_DIR = 'data'

# Utility functions to read and write data files

def load_auctions():
    auctions = []
    filepath = os.path.join(DATA_DIR, 'auctions.txt')
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 9:
                    auction = {
                        'auction_id': int(parts[0]),
                        'item_name': parts[1],
                        'description': parts[2],
                        'category': parts[3],
                        'starting_bid': float(parts[4]),
                        'current_bid': float(parts[5]),
                        'end_time': datetime.strptime(parts[6], '%Y-%m-%d %H:%M'),
                        'status': parts[7],
                        'image_url': parts[8]
                    }
                    auctions.append(auction)
    return auctions

def save_auctions(auctions):
    filepath = os.path.join(DATA_DIR, 'auctions.txt')
    with open(filepath, 'w', encoding='utf-8') as f:
        for a in auctions:
            line = '|'.join([
                str(a['auction_id']),
                a['item_name'],
                a['description'],
                a['category'],
                f"{a['starting_bid']:.2f}",
                f"{a['current_bid']:.2f}",
                a['end_time'].strftime('%Y-%m-%d %H:%M'),
                a['status'],
                a['image_url']
            ])
            f.write(line + '\n')


def load_categories():
    categories = []
    filepath = os.path.join(DATA_DIR, 'categories.txt')
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 4:
                    category = {
                        'category_id': int(parts[0]),
                        'category_name': parts[1],
                        'description': parts[2],
                        'item_count': int(parts[3])
                    }
                    categories.append(category)
    return categories


def load_bids():
    bids = []
    filepath = os.path.join(DATA_DIR, 'bids.txt')
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 5:
                    bid = {
                        'bid_id': int(parts[0]),
                        'auction_id': int(parts[1]),
                        'bidder_name': parts[2],
                        'bid_amount': float(parts[3]),
                        'bid_timestamp': datetime.strptime(parts[4], '%Y-%m-%d %H:%M')
                    }
                    bids.append(bid)
    return bids


def save_bids(bids):
    filepath = os.path.join(DATA_DIR, 'bids.txt')
    with open(filepath, 'w', encoding='utf-8') as f:
        for b in bids:
            line = '|'.join([
                str(b['bid_id']),
                str(b['auction_id']),
                b['bidder_name'],
                f"{b['bid_amount']:.2f}",
                b['bid_timestamp'].strftime('%Y-%m-%d %H:%M')
            ])
            f.write(line + '\n')


def load_winners():
    winners = []
    filepath = os.path.join(DATA_DIR, 'winners.txt')
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 6:
                    winner = {
                        'winner_id': int(parts[0]),
                        'auction_id': int(parts[1]),
                        'item_name': parts[2],
                        'winner_name': parts[3],
                        'winning_bid': float(parts[4]),
                        'win_date': parts[5]
                    }
                    winners.append(winner)
    return winners


def load_bid_history():
    bid_history = []
    filepath = os.path.join(DATA_DIR, 'bid_history.txt')
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 6:
                    history = {
                        'history_id': int(parts[0]),
                        'auction_id': int(parts[1]),
                        'auction_name': parts[2],
                        'bidder_name': parts[3],
                        'bid_amount': float(parts[4]),
                        'bid_timestamp': datetime.strptime(parts[5], '%Y-%m-%d %H:%M')
                    }
                    bid_history.append(history)
    return bid_history


def save_bid_history(bid_history):
    filepath = os.path.join(DATA_DIR, 'bid_history.txt')
    with open(filepath, 'w', encoding='utf-8') as f:
        for h in bid_history:
            line = '|'.join([
                str(h['history_id']),
                str(h['auction_id']),
                h['auction_name'],
                h['bidder_name'],
                f"{h['bid_amount']:.2f}",
                h['bid_timestamp'].strftime('%Y-%m-%d %H:%M')
            ])
            f.write(line + '\n')


def load_trending():
    trending = []
    filepath = os.path.join(DATA_DIR, 'trending.txt')
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 6:
                    entry = {
                        'auction_id': int(parts[0]),
                        'item_name': parts[1],
                        'bid_count': int(parts[2]),
                        'current_bid': float(parts[3]),
                        'trending_rank': int(parts[4]),
                        'time_period': parts[5]
                    }
                    trending.append(entry)
    return trending


@app.route('/')
def dashboard():
    auctions = load_auctions()
    # Display some featured auctions - choose top 3 by current_bid descending
    featured = sorted(auctions, key=lambda x: x['current_bid'], reverse=True)[:3]
    return render_template('dashboard.html', featured_auctions=featured)


@app.route('/catalog')
def catalog():
    auctions = load_auctions()
    categories = load_categories()

    search_query = request.args.get('search', '').lower()
    category_filter = request.args.get('category', '')

    filtered = auctions
    if search_query:
        filtered = [a for a in filtered if 
                    search_query in a['item_name'].lower() or
                    search_query in a['description'].lower() or
                    search_query in str(a['auction_id'])]
    if category_filter and category_filter != 'All':
        filtered = [a for a in filtered if a['category'] == category_filter]

    return render_template('catalog.html', auctions=filtered, categories=categories, selected_category=category_filter, search_query=search_query)


@app.route('/auction/<int:auction_id>')
def auction_details(auction_id):
    auctions = load_auctions()
    bids = load_bids()

    auction = next((a for a in auctions if a['auction_id'] == auction_id), None)
    if not auction:
        return "Auction not found", 404

    auction_bids = [b for b in bids if b['auction_id'] == auction_id]
    auction_bids_sorted = sorted(auction_bids, key=lambda x: x['bid_timestamp'], reverse=True)

    return render_template('auction_details.html', auction=auction, bids=auction_bids_sorted)


@app.route('/auction/<int:auction_id>/place_bid', methods=['GET', 'POST'])
def place_bid(auction_id):
    auctions = load_auctions()
    bids = load_bids()
    bid_history = load_bid_history()

    auction = next((a for a in auctions if a['auction_id'] == auction_id), None)
    if not auction:
        return "Auction not found", 404

    if request.method == 'POST':
        bidder_name = request.form.get('bidder_name', '').strip()
        try:
            bid_amount = float(request.form.get('bid_amount', 0))
        except ValueError:
            bid_amount = 0

        minimum_bid = max(auction['starting_bid'], auction['current_bid']) + 0.01

        if bidder_name and bid_amount >= minimum_bid and auction['status'] == 'Active':
            # Create new bid
            new_bid_id = max([b['bid_id'] for b in bids], default=0) + 1
            now = datetime.now()
            new_bid = {
                'bid_id': new_bid_id,
                'auction_id': auction_id,
                'bidder_name': bidder_name,
                'bid_amount': bid_amount,
                'bid_timestamp': now
            }
            bids.append(new_bid)
            save_bids(bids)

            # Update auction current bid
            auction['current_bid'] = bid_amount
            save_auctions(auctions)

            # Add to bid history
            new_history_id = max([h['history_id'] for h in bid_history], default=0) + 1
            new_history = {
                'history_id': new_history_id,
                'auction_id': auction_id,
                'auction_name': auction['item_name'],
                'bidder_name': bidder_name,
                'bid_amount': bid_amount,
                'bid_timestamp': now
            }
            bid_history.append(new_history)
            save_bid_history(bid_history)

            # Redirect to bid history page after successful bid
            return redirect(url_for('bid_history'))
        else:
            error_msg = "Bid must be higher than current bid and auction must be active, and bidder name required."
            minimum_bid_value = minimum_bid
            return render_template('place_bid.html', auction=auction, error=error_msg,
                                   minimum_bid=minimum_bid_value, bidder_name=bidder_name,
                                   bid_amount=bid_amount)

    # For GET request
    minimum_bid_value = max(auction['starting_bid'], auction['current_bid']) + 0.01
    return render_template('place_bid.html', auction=auction, minimum_bid=minimum_bid_value)


@app.route('/bid_history')
def bid_history():
    bids = load_bids()
    auctions = load_auctions()

    filter_auction = request.args.get('filter_auction', '')
    sort_by_amount = request.args.get('sort_by_amount', '')

    # Filter by auction
    if filter_auction:
        try:
            filter_auction_id = int(filter_auction)
            bids = [b for b in bids if b['auction_id'] == filter_auction_id]
        except ValueError:
            pass

    # Sort by bid amount
    if sort_by_amount == 'true':
        bids = sorted(bids, key=lambda x: x['bid_amount'], reverse=True)
    else:
        bids = sorted(bids, key=lambda x: x['bid_timestamp'], reverse=True)

    # Prepare auction name lookup
    auction_names = {a['auction_id']: a['item_name'] for a in auctions}

    return render_template('bid_history.html', bids=bids, auction_names=auction_names, filter_auction=filter_auction)


@app.route('/categories')
def categories():
    categories = load_categories()
    return render_template('categories.html', categories=categories)


@app.route('/winners')
def winners():
    winners = load_winners()
    filter_winner = request.args.get('filter_winner', '').lower()
    if filter_winner:
        winners = [w for w in winners if filter_winner in w['winner_name'].lower()]
    return render_template('winners.html', winners=winners, filter_winner=filter_winner)


@app.route('/trending')
def trending():
    trending = load_trending()

    time_range_filter = request.args.get('time_range', 'All Time')
    if time_range_filter != 'All Time':
        trending = [t for t in trending if t['time_period'] == time_range_filter]

    return render_template('trending.html', trending=trending, selected_time_range=time_range_filter)


@app.route('/status')
def status():
    auctions = load_auctions()
    status_filter = request.args.get('status', 'All')

    filtered_auctions = auctions
    if status_filter != 'All':
        filtered_auctions = [a for a in auctions if a['status'] == status_filter]

    return render_template('status.html', auctions=filtered_auctions, selected_status=status_filter)


@app.route('/refresh_status')
def refresh_status():
    # For simplification, just refresh data and redirect to status page
    return redirect(url_for('status'))


@app.route('/category/<int:category_id>')
def category_items(category_id):
    categories = load_categories()
    auctions = load_auctions()
    category = next((c for c in categories if c['category_id'] == category_id), None)
    if not category:
        return "Category not found", 404

    filtered_auctions = [a for a in auctions if a['category'] == category['category_name']]

    return render_template('catalog.html', auctions=filtered_auctions, categories=categories,
                           selected_category=category['category_name'], search_query='')


if __name__ == '__main__':
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    app.run(debug=True)
