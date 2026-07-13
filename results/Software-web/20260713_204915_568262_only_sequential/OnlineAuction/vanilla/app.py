from flask import Flask, render_template, redirect, url_for, request
import os
from datetime import datetime

app = Flask(__name__)

# Data directory
DATA_DIR = 'data'

# Helper functions to load data

def load_auctions():
    auctions = []
    path = os.path.join(DATA_DIR, 'auctions.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                fields = line.split('|')
                if len(fields) < 9:
                    continue
                auction = {
                    'auction_id': int(fields[0]),
                    'item_name': fields[1],
                    'description': fields[2],
                    'category': fields[3],
                    'starting_bid': float(fields[4]),
                    'current_bid': float(fields[5]),
                    'end_time': fields[6],
                    'status': fields[7],
                    'image_url': fields[8]
                }
                auctions.append(auction)
    return auctions


def load_categories():
    categories = []
    path = os.path.join(DATA_DIR, 'categories.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                fields = line.split('|')
                if len(fields) < 4:
                    continue
                category = {
                    'category_id': int(fields[0]),
                    'category_name': fields[1],
                    'description': fields[2],
                    'item_count': int(fields[3])
                }
                categories.append(category)
    return categories


def load_bids():
    bids = []
    path = os.path.join(DATA_DIR, 'bids.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                fields = line.split('|')
                if len(fields) < 5:
                    continue
                bid = {
                    'bid_id': int(fields[0]),
                    'auction_id': int(fields[1]),
                    'bidder_name': fields[2],
                    'bid_amount': float(fields[3]),
                    'bid_timestamp': fields[4]
                }
                bids.append(bid)
    return bids


def load_winners():
    winners = []
    path = os.path.join(DATA_DIR, 'winners.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                fields = line.split('|')
                if len(fields) < 6:
                    continue
                winner = {
                    'winner_id': int(fields[0]),
                    'auction_id': int(fields[1]),
                    'item_name': fields[2],
                    'winner_name': fields[3],
                    'winning_bid': float(fields[4]),
                    'win_date': fields[5]
                }
                winners.append(winner)
    return winners


def load_bid_history():
    bid_history = []
    path = os.path.join(DATA_DIR, 'bid_history.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                fields = line.split('|')
                if len(fields) < 6:
                    continue
                history = {
                    'history_id': int(fields[0]),
                    'auction_id': int(fields[1]),
                    'auction_name': fields[2],
                    'bidder_name': fields[3],
                    'bid_amount': float(fields[4]),
                    'bid_timestamp': fields[5]
                }
                bid_history.append(history)
    return bid_history


def load_trending():
    trending_auctions = []
    path = os.path.join(DATA_DIR, 'trending.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                fields = line.split('|')
                if len(fields) < 6:
                    continue
                trending = {
                    'auction_id': int(fields[0]),
                    'item_name': fields[1],
                    'bid_count': int(fields[2]),
                    'current_bid': float(fields[3]),
                    'trending_rank': int(fields[4]),
                    'time_period': fields[5]
                }
                trending_auctions.append(trending)
    return trending_auctions


# ROUTES
@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    auctions = load_auctions()
    featured_auctions = [a for a in auctions if a['status'] == 'Active'][:3]
    return render_template('dashboard.html', featured_auctions=featured_auctions)


@app.route('/catalog')
def auction_catalog():
    auctions = load_auctions()
    categories = load_categories()

    search_query = request.args.get('search', '').strip()
    selected_category = request.args.get('category', '').strip()

    filtered_auctions = auctions

    if search_query:
        filtered_auctions = [a for a in filtered_auctions if (search_query.lower() in a['item_name'].lower() or
                                                               search_query.lower() in a['description'].lower() or
                                                               search_query == str(a['auction_id']))]

    if selected_category:
        category_name = ''
        for c in categories:
            if str(c['category_id']) == selected_category:
                category_name = c['category_name']
                break
        if category_name:
            filtered_auctions = [a for a in filtered_auctions if a['category'] == category_name]

    return render_template('catalog.html', auctions=filtered_auctions, categories=categories, selected_category=selected_category, search_query=search_query)


@app.route('/auction/<int:auction_id>')
def auction_details(auction_id):
    auctions = load_auctions()
    bid_history_all = load_bid_history()

    auction = None
    for a in auctions:
        if a['auction_id'] == auction_id:
            auction = a
            break

    if not auction:
        return f'Auction with id {auction_id} not found.', 404

    bid_history = [bh for bh in bid_history_all if bh['auction_id'] == auction_id]
    bid_history.sort(key=lambda x: x['bid_timestamp'], reverse=True)

    return render_template('auction_details.html', auction=auction, bid_history=bid_history)


@app.route('/place_bid/<int:auction_id>', methods=['GET', 'POST'])
def place_bid(auction_id):
    auctions = load_auctions()
    auction = None
    for a in auctions:
        if a['auction_id'] == auction_id:
            auction = a
            break

    if not auction:
        return f'Auction with id {auction_id} not found.', 404

    errors = {}

    if request.method == 'POST':
        bidder_name = request.form.get('bidder-name', '').strip()
        bid_amount_str = request.form.get('bid-amount', '').strip()

        if not bidder_name:
            errors['bidder_name'] = 'Bidder name is required.'

        try:
            bid_amount = float(bid_amount_str)
            if bid_amount <= auction['current_bid']:
                errors['bid_amount'] = f'Bid amount must be greater than current bid ({auction["current_bid"]}).'
        except ValueError:
            errors['bid_amount'] = 'Invalid bid amount.'

        if not errors:
            bids = load_bids()
            if bids:
                new_bid_id = max(b['bid_id'] for b in bids) + 1
            else:
                new_bid_id = 1

            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')

            new_bid_line = f'{new_bid_id}|{auction_id}|{bidder_name}|{bid_amount:.2f}|{timestamp}\n'

            with open(os.path.join(DATA_DIR, 'bids.txt'), 'a', encoding='utf-8') as f:
                f.write(new_bid_line)

            history = load_bid_history()
            if history:
                new_history_id = max(h['history_id'] for h in history) + 1
            else:
                new_history_id = 1

            new_history_line = f'{new_history_id}|{auction_id}|{auction["item_name"]}|{bidder_name}|{bid_amount:.2f}|{timestamp}\n'
            with open(os.path.join(DATA_DIR, 'bid_history.txt'), 'a', encoding='utf-8') as f:
                f.write(new_history_line)

            all_auctions = load_auctions()
            with open(os.path.join(DATA_DIR, 'auctions.txt'), 'w', encoding='utf-8') as f:
                for auc in all_auctions:
                    if auc['auction_id'] == auction_id:
                        auc['current_bid'] = bid_amount
                    line = f"{auc['auction_id']}|{auc['item_name']}|{auc['description']}|{auc['category']}|{auc['starting_bid']:.2f}|{auc['current_bid']:.2f}|{auc['end_time']}|{auc['status']}|{auc['image_url']}\n"
                    f.write(line)

            return redirect(url_for('auction_details', auction_id=auction_id))

    minimum_bid = auction['current_bid'] + 0.01

    return render_template('place_bid.html', auction={'auction_id': auction['auction_id'], 'item_name': auction['item_name'], 'minimum_bid': minimum_bid}, errors=errors)


@app.route('/bid_history')
def bid_history():
    bids = load_bids()
    auctions = load_auctions()

    selected_auction_id = request.args.get('auction_id', '').strip()
    sort_order_amount = request.args.get('sort_by_amount', 'false').lower() == 'true'

    filtered_bids = bids

    if selected_auction_id:
        try:
            sel_id = int(selected_auction_id)
            filtered_bids = [b for b in bids if b['auction_id'] == sel_id]
        except ValueError:
            pass

    if sort_order_amount:
        filtered_bids = sorted(filtered_bids, key=lambda x: x['bid_amount'], reverse=True)

    return render_template('bid_history.html', bids=filtered_bids, auctions=auctions, selected_auction_id=selected_auction_id, sort_order_amount=sort_order_amount)


@app.route('/categories')
def auction_categories():
    categories = load_categories()
    return render_template('categories.html', categories=categories)


@app.route('/winners')
def winners():
    winners_list = load_winners()
    filter_name = request.args.get('filter_name', '').strip().lower()

    if filter_name:
        winners_list = [w for w in winners_list if filter_name in w['winner_name'].lower()]

    return render_template('winners.html', winners=winners_list, filter_name=filter_name)


@app.route('/trending')
def trending_auctions():
    trending_list = load_trending()
    time_range = request.args.get('time_range', 'This Week')

    filtered_list = [t for t in trending_list if t['time_period'] == time_range]

    return render_template('trending.html', trending_auctions=filtered_list, selected_time_range=time_range)


@app.route('/status')
def auction_status():
    auctions = load_auctions()
    status_filter = request.args.get('status', 'All')

    filtered_auctions = auctions
    if status_filter != 'All':
        filtered_auctions = [a for a in auctions if a['status'] == status_filter]

    # Calculate time_remaining (as string) for each auction
    for a in filtered_auctions:
        try:
            end_time_dt = datetime.strptime(a['end_time'], '%Y-%m-%d %H:%M')
            now = datetime.now()
            delta = end_time_dt - now
            if delta.days < 0:
                a['time_remaining'] = 'Ended'
            else:
                hours, remainder = divmod(delta.seconds, 3600)
                minutes = remainder // 60
                a['time_remaining'] = f'{delta.days}d {hours}h {minutes}m'
        except Exception:
            a['time_remaining'] = 'Unknown'

    return render_template('status.html', auctions=filtered_auctions, status_filter=status_filter)


if __name__ == '__main__':
    app.run(debug=True)
