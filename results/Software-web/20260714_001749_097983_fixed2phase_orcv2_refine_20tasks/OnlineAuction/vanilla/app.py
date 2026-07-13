from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)
DATA_DIR = 'data'

# Utility functions for loading and saving data

def load_auctions():
    auctions = []
    try:
        with open(os.path.join(DATA_DIR, 'auctions.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) < 9:
                    continue
                auction = {
                    'auction_id': parts[0],
                    'item_name': parts[1],
                    'description': parts[2],
                    'category': parts[3],
                    'starting_bid': float(parts[4]),
                    'current_bid': float(parts[5]),
                    'end_time': parts[6],
                    'status': parts[7],
                    'image_url': parts[8],
                }
                auctions.append(auction)
    except FileNotFoundError:
        pass
    return auctions


def save_auctions(auctions):
    with open(os.path.join(DATA_DIR, 'auctions.txt'), 'w', encoding='utf-8') as f:
        for a in auctions:
            line = '|'.join([a['auction_id'], a['item_name'], a['description'], a['category'], 
                             str(a['starting_bid']), f"{a['current_bid']:.2f}", a['end_time'], a['status'], a['image_url']])
            f.write(line + '\n')


def load_categories():
    categories = []
    try:
        with open(os.path.join(DATA_DIR, 'categories.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) < 4:
                    continue
                category = {
                    'category_id': parts[0],
                    'category_name': parts[1],
                    'description': parts[2],
                    'item_count': int(parts[3]),
                }
                categories.append(category)
    except FileNotFoundError:
        pass
    return categories


def load_bids():
    bids = []
    try:
        with open(os.path.join(DATA_DIR, 'bids.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts=line.split('|')
                if len(parts) <5:
                    continue
                bid = {
                    'bid_id': parts[0],
                    'auction_id': parts[1],
                    'bidder_name': parts[2],
                    'bid_amount': float(parts[3]),
                    'bid_timestamp': parts[4],
                }
                bids.append(bid)
    except FileNotFoundError:
        pass
    return bids


def save_bids(bids):
    with open(os.path.join(DATA_DIR, 'bids.txt'), 'w', encoding='utf-8') as f:
        for b in bids:
            line = '|'.join([b['bid_id'], b['auction_id'], b['bidder_name'], f"{b['bid_amount']:.2f}", b['bid_timestamp']])
            f.write(line + '\n')


def load_winners():
    winners = []
    try:
        with open(os.path.join(DATA_DIR, 'winners.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts=line.split('|')
                if len(parts) < 6:
                    continue
                winner = {
                    'winner_id': parts[0],
                    'auction_id': parts[1],
                    'item_name': parts[2],
                    'winner_name': parts[3],
                    'winning_bid': float(parts[4]),
                    'win_date': parts[5],
                }
                winners.append(winner)
    except FileNotFoundError:
        pass
    return winners


def load_bid_history():
    history = []
    try:
        with open(os.path.join(DATA_DIR, 'bid_history.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts=line.split('|')
                if len(parts) < 6:
                    continue
                entry = {
                    'history_id': parts[0],
                    'auction_id': parts[1],
                    'auction_name': parts[2],
                    'bidder_name': parts[3],
                    'bid_amount': float(parts[4]),
                    'bid_timestamp': parts[5],
                }
                history.append(entry)
    except FileNotFoundError:
        pass
    return history


def save_bid_history(history):
    with open(os.path.join(DATA_DIR, 'bid_history.txt'), 'w', encoding='utf-8') as f:
        for h in history:
            line = '|'.join([h['history_id'], h['auction_id'], h['auction_name'], h['bidder_name'], f"{h['bid_amount']:.2f}", h['bid_timestamp']])
            f.write(line + '\n')


def load_trending():
    trending = []
    try:
        with open(os.path.join(DATA_DIR, 'trending.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts=line.split('|')
                if len(parts) < 6:
                    continue
                t = {
                    'auction_id': parts[0],
                    'item_name': parts[1],
                    'bid_count': int(parts[2]),
                    'current_bid': float(parts[3]),
                    'trending_rank': int(parts[4]),
                    'time_period': parts[5],
                }
                trending.append(t)
    except FileNotFoundError:
        pass
    return trending


# Route: Dashboard Page
@app.route('/')
def dashboard():
    auctions = load_auctions()
    # Featured auctions as first 3 active auctions
    featured = [a for a in auctions if a['status'].lower() == 'active'][:3]
    trending = load_trending()
    return render_template('dashboard.html', featured_auctions=featured, trending_auctions=trending)


# Route: Auction Catalog Page
@app.route('/catalog')
def catalog():
    auctions = load_auctions()
    categories = load_categories()

    search_term = request.args.get('search', '').lower()
    category_filter = request.args.get('filter', '')

    filtered_auctions = auctions
    if search_term:
        filtered_auctions = [a for a in filtered_auctions if 
                             search_term in a['item_name'].lower() or 
                             search_term in a['description'].lower() or 
                             search_term in a['auction_id']]
    if category_filter and category_filter != 'All':
        filtered_auctions = [a for a in filtered_auctions if a['category'] == category_filter]

    return render_template('catalog.html', auctions=filtered_auctions, categories=categories, 
                           selected_category=category_filter, search_term=search_term)


# Route: Auction Details Page
@app.route('/auction/<auction_id>')
def auction_details(auction_id):
    auctions = load_auctions()
    bids = load_bids()

    auction = next((a for a in auctions if a['auction_id'] == auction_id), None)
    if not auction:
        return "Auction not found", 404

    auction_bids = [b for b in bids if b['auction_id'] == auction_id]
    auction_bids.sort(key=lambda x: datetime.strptime(x['bid_timestamp'], '%Y-%m-%d %H:%M'))

    return render_template('auction_details.html', auction=auction, bids=auction_bids)


# Route: Place Bid Page
@app.route('/auction/<auction_id>/place-bid', methods=['GET', 'POST'])
def place_bid(auction_id):
    auctions = load_auctions()
    bids = load_bids()

    auction = next((a for a in auctions if a['auction_id'] == auction_id), None)
    if not auction:
        return "Auction not found", 404

    if request.method == 'POST':
        bidder_name = request.form.get('bidder_name', '').strip()
        bid_amount = request.form.get('bid_amount', '').strip()

        try:
            bid_amount = float(bid_amount)
        except ValueError:
            error = 'Invalid bid amount.'
            return render_template('place_bid.html', auction=auction, minimum_bid=auction['current_bid'] + 0.01, error=error)

        minimum_bid = auction['current_bid'] + 0.01
        if bid_amount < minimum_bid:
            error = f'Bid must be at least {minimum_bid:.2f}.'
            return render_template('place_bid.html', auction=auction, minimum_bid=minimum_bid, error=error)

        # New bid ID generation
        new_bid_id = str(max([int(b['bid_id']) for b in bids], default=0) + 1)
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')

        new_bid = {
            'bid_id': new_bid_id,
            'auction_id': auction_id,
            'bidder_name': bidder_name,
            'bid_amount': bid_amount,
            'bid_timestamp': timestamp
        }

        bids.append(new_bid)
        save_bids(bids)

        # Update auction current bid
        for a in auctions:
            if a['auction_id'] == auction_id:
                a['current_bid'] = bid_amount
                break
        save_auctions(auctions)

        # Append to bid_history.txt
        history = load_bid_history()
        new_history_id = str(max([int(h['history_id']) for h in history], default=0) + 1)
        new_history_entry = {
            'history_id': new_history_id,
            'auction_id': auction_id,
            'auction_name': auction['item_name'],
            'bidder_name': bidder_name,
            'bid_amount': bid_amount,
            'bid_timestamp': timestamp
        }
        history.append(new_history_entry)
        save_bid_history(history)

        return redirect(url_for('auction_details', auction_id=auction_id))

    minimum_bid = auction['current_bid'] + 0.01
    return render_template('place_bid.html', auction=auction, minimum_bid=minimum_bid)


# Route: Bid History Page
@app.route('/bid-history')
def bid_history():
    bids = load_bids()
    auctions = load_auctions()

    filter_auction = request.args.get('filter', '')
    sort_amount = request.args.get('sort', '')

    filtered_bids = bids
    if filter_auction:
        filtered_bids = [b for b in filtered_bids if b['auction_id'] == filter_auction]

    if sort_amount == 'amount':
        filtered_bids = sorted(filtered_bids, key=lambda x: x['bid_amount'], reverse=True)
    else:
        filtered_bids = sorted(filtered_bids, key=lambda x: datetime.strptime(x['bid_timestamp'], '%Y-%m-%d %H:%M'), reverse=True)

    auction_dict = {a['auction_id']: a['item_name'] for a in auctions}

    return render_template('bid_history.html', bids=filtered_bids, auctions=auctions, filter_auction=filter_auction, sort_amount=sort_amount, auction_dict=auction_dict)


# Route: Auction Categories Page
@app.route('/categories')
def categories():
    categories = load_categories()
    return render_template('categories.html', categories=categories)


# Route: Auctions in Category
@app.route('/categories/<category_id>')
def auctions_in_category(category_id):
    auctions = load_auctions()
    categories = load_categories()

    category = next((c for c in categories if c['category_id'] == category_id), None)
    if not category:
        return "Category not found", 404

    filtered_auctions = [a for a in auctions if a['category'] == category['category_name']]

    return render_template('catalog.html', auctions=filtered_auctions, categories=categories, selected_category=category['category_name'], search_term='')


# Route: Winners Page
@app.route('/winners')
def winners():
    winners = load_winners()
    filter_winner = request.args.get('filter', '').lower()

    if filter_winner:
        filtered_winners = [w for w in winners if filter_winner in w['winner_name'].lower()]
    else:
        filtered_winners = winners

    return render_template('winners.html', winners=filtered_winners, filter_winner=filter_winner)


# Route: Trending Auctions Page
@app.route('/trending')
def trending():
    trending = load_trending()
    time_filter = request.args.get('time_range', 'All Time')

    if time_filter != 'All Time':
        trending = [t for t in trending if t['time_period'] == time_filter]

    trending.sort(key=lambda x: x['trending_rank'])

    return render_template('trending.html', trending=trending, time_filter=time_filter)


# Route: Auction Status Page
@app.route('/status')
def status():
    auctions = load_auctions()
    status_filter = request.args.get('filter', 'All')

    filtered_auctions = auctions
    if status_filter != 'All':
        filtered_auctions = [a for a in auctions if a['status'] == status_filter]

    # Calculate time_remaining for active auctions
    for a in filtered_auctions:
        if a['status'] == 'Active':
            end_time_dt = datetime.strptime(a['end_time'], '%Y-%m-%d %H:%M')
            now_dt = datetime.now()
            delta = end_time_dt - now_dt
            if delta.total_seconds() > 0:
                days = delta.days
                hours = delta.seconds // 3600
                minutes = (delta.seconds // 60) % 60
                if days > 0:
                    a['time_remaining'] = f"{days} days"
                else:
                    a['time_remaining'] = f"{hours} hours {minutes} minutes"
            else:
                a['time_remaining'] = '0 minutes'
        else:
            a['time_remaining'] = 'N/A'

    return render_template('status.html', auctions=filtered_auctions, status_filter=status_filter)


# POST route to refresh status data
@app.route('/refresh-status', methods=['POST'])
def refresh_status():
    # In this simplified example, just redirect to the status page
    return redirect(url_for('status'))


if __name__ == '__main__':
    app.run(debug=True, port=5000)
