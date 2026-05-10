'''
Main backend application for OnlineAuction web app.
Defines routes for all pages with URL paths matching frontend navigation.
Ensures '/' route serves the Dashboard page as the starting page.
Loads data from local text files in 'data' directory for rendering templates.
'''
from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime
app = Flask(__name__)
DATA_DIR = 'data'
def read_auctions():
    auctions = []
    path = os.path.join(DATA_DIR, 'auctions.txt')
    if not os.path.exists(path):
        return auctions
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split('|')
                if len(parts) == 9:
                    auction = {
                        'auction_id': parts[0],
                        'item_name': parts[1],
                        'description': parts[2],
                        'category': parts[3],
                        'starting_bid': float(parts[4]),
                        'current_bid': float(parts[5]),
                        'end_time': parts[6],
                        'status': parts[7],
                        'image_url': parts[8]
                    }
                    auctions.append(auction)
    return auctions
def read_categories():
    categories = []
    path = os.path.join(DATA_DIR, 'categories.txt')
    if not os.path.exists(path):
        return categories
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split('|')
                if len(parts) == 4:
                    category = {
                        'category_id': parts[0],
                        'category_name': parts[1],
                        'description': parts[2],
                        'item_count': int(parts[3])
                    }
                    categories.append(category)
    return categories
def read_bids():
    bids = []
    path = os.path.join(DATA_DIR, 'bids.txt')
    if not os.path.exists(path):
        return bids
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split('|')
                if len(parts) == 5:
                    bid = {
                        'bid_id': parts[0],
                        'auction_id': parts[1],
                        'bidder_name': parts[2],
                        'bid_amount': float(parts[3]),
                        'bid_timestamp': parts[4]
                    }
                    bids.append(bid)
    return bids
def read_winners():
    winners = []
    path = os.path.join(DATA_DIR, 'winners.txt')
    if not os.path.exists(path):
        return winners
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split('|')
                if len(parts) == 6:
                    winner = {
                        'winner_id': parts[0],
                        'auction_id': parts[1],
                        'item_name': parts[2],
                        'winner_name': parts[3],
                        'winning_bid': float(parts[4]),
                        'win_date': parts[5]
                    }
                    winners.append(winner)
    return winners
def read_bid_history():
    history = []
    path = os.path.join(DATA_DIR, 'bid_history.txt')
    if not os.path.exists(path):
        return history
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split('|')
                if len(parts) == 6:
                    record = {
                        'history_id': parts[0],
                        'auction_id': parts[1],
                        'auction_name': parts[2],
                        'bidder_name': parts[3],
                        'bid_amount': float(parts[4]),
                        'bid_timestamp': parts[5]
                    }
                    history.append(record)
    return history
def read_trending():
    trending = []
    path = os.path.join(DATA_DIR, 'trending.txt')
    if not os.path.exists(path):
        return trending
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split('|')
                if len(parts) == 6:
                    item = {
                        'auction_id': parts[0],
                        'item_name': parts[1],
                        'bid_count': int(parts[2]),
                        'current_bid': float(parts[3]),
                        'trending_rank': int(parts[4]),
                        'time_period': parts[5]
                    }
                    trending.append(item)
    return trending
@app.route('/')
def dashboard():
    '''
    Route for Dashboard page - the starting page of the website.
    Loads featured auctions and trending auctions for display.
    '''
    auctions = read_auctions()
    trending = read_trending()
    # For featured auctions, pick first 3 active auctions as example
    featured = [a for a in auctions if a['status'].lower() == 'active'][:3]
    return render_template('dashboard.html', featured_auctions=featured, trending_auctions=trending)
@app.route('/auction-catalog')
def auction_catalog():
    '''
    Route for Auction Catalog page.
    Supports optional search and category filter via query parameters.
    '''
    auctions = read_auctions()
    categories = [c['category_name'] for c in read_categories()]
    search_query = request.args.get('search', '').lower()
    category_filter = request.args.get('category', '')
    filtered_auctions = auctions
    if search_query:
        filtered_auctions = [a for a in filtered_auctions if search_query in a['item_name'].lower() or search_query in a['description'].lower() or search_query in a['auction_id']]
    if category_filter and category_filter in categories:
        filtered_auctions = [a for a in filtered_auctions if a['category'] == category_filter]
    return render_template('auction_catalog.html', auctions=filtered_auctions, categories=categories, selected_category=category_filter, search_query=search_query)
@app.route('/auction-details/<auction_id>')
def auction_details(auction_id):
    '''
    Route for Auction Details page for a specific auction item.
    Displays detailed info and bid history.
    '''
    auctions = read_auctions()
    bids = read_bids()
    auction = next((a for a in auctions if a['auction_id'] == auction_id), None)
    if not auction:
        return "Auction not found", 404
    auction_bids = [b for b in bids if b['auction_id'] == auction_id]
    auction_bids.sort(key=lambda x: x['bid_timestamp'], reverse=True)
    return render_template('auction_details.html', auction=auction, bid_history=auction_bids)
@app.route('/place-bid/<auction_id>', methods=['GET', 'POST'])
def place_bid(auction_id):
    '''
    Route for Place Bid page.
    GET: Show form to place bid.
    POST: Process bid submission and update bids and bid_history files.
    '''
    auctions = read_auctions()
    auction = next((a for a in auctions if a['auction_id'] == auction_id), None)
    if not auction:
        return "Auction not found", 404
    if request.method == 'POST':
        bidder_name = request.form.get('bidder_name', '').strip()
        bid_amount_str = request.form.get('bid_amount', '').strip()
        if not bidder_name or not bid_amount_str:
            error = "Bidder name and bid amount are required."
            return render_template('place_bid.html', auction=auction, minimum_bid=auction['current_bid'], error=error)
        try:
            bid_amount = float(bid_amount_str)
        except ValueError:
            error = "Invalid bid amount."
            return render_template('place_bid.html', auction=auction, minimum_bid=auction['current_bid'], error=error)
        if bid_amount <= auction['current_bid']:
            error = f"Bid amount must be greater than current bid ({auction['current_bid']})."
            return render_template('place_bid.html', auction=auction, minimum_bid=auction['current_bid'], error=error)
        # Append new bid to bids.txt
        bids = read_bids()
        new_bid_id = str(max([int(b['bid_id']) for b in bids], default=0) + 1)
        now_str = datetime.now().strftime('%Y-%m-%d %H:%M')
        new_bid_line = f"{new_bid_id}|{auction_id}|{bidder_name}|{bid_amount:.2f}|{now_str}\n"
        with open(os.path.join(DATA_DIR, 'bids.txt'), 'a', encoding='utf-8') as f:
            f.write(new_bid_line)
        # Append to bid_history.txt
        bid_history = read_bid_history()
        new_history_id = str(max([int(h['history_id']) for h in bid_history], default=0) + 1)
        new_history_line = f"{new_history_id}|{auction_id}|{auction['item_name']}|{bidder_name}|{bid_amount:.2f}|{now_str}\n"
        with open(os.path.join(DATA_DIR, 'bid_history.txt'), 'a', encoding='utf-8') as f:
            f.write(new_history_line)
        # Update current_bid in auctions.txt
        updated_auctions = []
        for a in auctions:
            if a['auction_id'] == auction_id:
                a['current_bid'] = bid_amount
            updated_auctions.append(a)
        with open(os.path.join(DATA_DIR, 'auctions.txt'), 'w', encoding='utf-8') as f:
            for a in updated_auctions:
                line = '|'.join([
                    a['auction_id'],
                    a['item_name'],
                    a['description'],
                    a['category'],
                    f"{a['starting_bid']:.2f}",
                    f"{a['current_bid']:.2f}",
                    a['end_time'],
                    a['status'],
                    a['image_url']
                ])
                f.write(line + '\n')
        return redirect(url_for('auction_details', auction_id=auction_id))
    # GET request
    return render_template('place_bid.html', auction=auction, minimum_bid=auction['current_bid'])
@app.route('/bid-history')
def bid_history():
    '''
    Route for Bid History page.
    Supports filtering by auction and sorting by amount.
    '''
    bids = read_bids()
    auctions = read_auctions()
    auction_map = {a['auction_id']: a['item_name'] for a in auctions}
    filter_auction = request.args.get('auction', '')
    sort_by_amount = request.args.get('sort', '') == 'amount'
    filtered_bids = bids
    if filter_auction:
        filtered_bids = [b for b in filtered_bids if b['auction_id'] == filter_auction]
    if sort_by_amount:
        filtered_bids = sorted(filtered_bids, key=lambda x: x['bid_amount'], reverse=True)
    else:
        filtered_bids = sorted(filtered_bids, key=lambda x: x['bid_timestamp'], reverse=True)
    auction_options = [(a['auction_id'], a['item_name']) for a in auctions]
    return render_template('bid_history.html', bids=filtered_bids, auction_options=auction_options, selected_auction=filter_auction, sort_by_amount=sort_by_amount)
@app.route('/auction-categories')
def auction_categories():
    '''
    Route for Auction Categories page.
    Displays all categories with descriptions and item counts.
    '''
    categories = read_categories()
    return render_template('auction_categories.html', categories=categories)
@app.route('/category-items/<category_id>')
def category_items(category_id):
    '''
    Route to view items in a specific category.
    '''
    categories = read_categories()
    category = next((c for c in categories if c['category_id'] == category_id), None)
    if not category:
        return "Category not found", 404
    auctions = read_auctions()
    category_auctions = [a for a in auctions if a['category'] == category['category_name']]
    return render_template('category_items.html', category=category, auctions=category_auctions)
@app.route('/winners')
def winners():
    '''
    Route for Winners page.
    Supports filtering winners by name.
    '''
    winners = read_winners()
    filter_name = request.args.get('winner', '').lower()
    if filter_name:
        filtered_winners = [w for w in winners if filter_name in w['winner_name'].lower()]
    else:
        filtered_winners = winners
    return render_template('winners.html', winners=filtered_winners, filter_name=filter_name)
@app.route('/trending-auctions')
def trending_auctions():
    '''
    Route for Trending Auctions page.
    Supports filtering by time range.
    '''
    trending = read_trending()
    time_range = request.args.get('time_range', 'This Week')
    filtered_trending = [t for t in trending if t['time_period'] == time_range]
    filtered_trending.sort(key=lambda x: x['trending_rank'])
    time_ranges = ['Last 24 Hours', 'This Week', 'All Time']
    return render_template('trending_auctions.html', trending_list=filtered_trending, time_ranges=time_ranges, selected_time_range=time_range)
@app.route('/auction-status')
def auction_status():
    '''
    Route for Auction Status page.
    Supports filtering by status.
    '''
    auctions = read_auctions()
    status_filter = request.args.get('status', 'All')
    if status_filter != 'All':
        filtered_auctions = [a for a in auctions if a['status'] == status_filter]
    else:
        filtered_auctions = auctions
    # Calculate time remaining for active and upcoming auctions
    now = datetime.now()
    for a in filtered_auctions:
        try:
            end_dt = datetime.strptime(a['end_time'], '%Y-%m-%d %H:%M')
            delta = end_dt - now
            if delta.total_seconds() > 0:
                days = delta.days
                hours = delta.seconds // 3600
                minutes = (delta.seconds % 3600) // 60
                a['time_remaining'] = f"{days}d {hours}h {minutes}m"
            else:
                a['time_remaining'] = "Ended"
        except Exception:
            a['time_remaining'] = "Unknown"
    statuses = ['All', 'Active', 'Closed', 'Upcoming']
    return render_template('auction_status.html', auctions=filtered_auctions, statuses=statuses, selected_status=status_filter)
@app.route('/back-to-dashboard')
def back_to_dashboard():
    '''
    Redirect route to Dashboard page.
    '''
    return redirect(url_for('dashboard'))
if __name__ == '__main__':
    app.run(debug=True)