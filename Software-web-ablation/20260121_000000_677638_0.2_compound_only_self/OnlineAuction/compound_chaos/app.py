from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import os

app = Flask(__name__)
app.secret_key = 'some_secret_key'

data_dir = 'data'


def load_auctions():
    auctions = []
    filepath = os.path.join(data_dir, 'auctions.txt')
    if not os.path.exists(filepath):
        app.logger.warning(f"Auctions file missing: {filepath}")
        return auctions
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 6:
                    app.logger.warning(f"Malformed auction line skipped: {line.strip()}")
                    continue
                try:
                    auction = {
                        'id': parts[0],
                        'title': parts[1],
                        'category': parts[2],
                        'status': parts[3],  # expected: 'active', 'closed', etc.
                        'starting_price': float(parts[4]),
                        'current_price': float(parts[5])
                    }
                    auctions.append(auction)
                except ValueError:
                    app.logger.warning(f"Skipping auction with invalid values: {line.strip()}")
                    continue
    except Exception as e:
        app.logger.error(f"Failed to read auctions file: {e}")
    return auctions


def save_auctions(auctions):
    filepath = os.path.join(data_dir, 'auctions.txt')
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            for auction in auctions:
                line = '|'.join([
                    auction['id'],
                    auction['title'],
                    auction['category'],
                    auction['status'],
                    f"{auction['starting_price']:.2f}",
                    f"{auction['current_price']:.2f}"
                ])
                f.write(line + '\n')
    except Exception as e:
        app.logger.error(f"Error saving auctions: {e}")


def load_categories():
    categories = []
    filepath = os.path.join(data_dir, 'categories.txt')
    if not os.path.exists(filepath):
        app.logger.warning(f"Categories file missing: {filepath}")
        return categories
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) < 2:
                    app.logger.warning(f"Malformed category line skipped: {line.strip()}")
                    continue
                category = {
                    'id': parts[0],
                    'name': parts[1]
                }
                categories.append(category)
    except Exception as e:
        app.logger.error(f"Failed to read categories file: {e}")
    return categories


def load_trending():
    trending = []
    filepath = os.path.join(data_dir, 'trending.txt')
    if not os.path.exists(filepath):
        app.logger.warning(f"Trending file missing: {filepath}")
        return trending
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) < 2:
                    app.logger.warning(f"Malformed trending line skipped: {line.strip()}")
                    continue
                try:
                    item = {
                        'id': parts[0],
                        'rank': int(parts[1]),
                        'title': parts[2] if len(parts) > 2 else ''
                    }
                    trending.append(item)
                except ValueError:
                    app.logger.warning(f"Skipping trending item with invalid rank: {line.strip()}")
                    continue
        trending.sort(key=lambda x: x['rank'])
    except Exception as e:
        app.logger.error(f"Failed to read trending file: {e}")
    return trending


@app.route('/')
def index():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    auctions = load_auctions()
    categories = load_categories()
    trending = load_trending()

    featured_auctions = [a for a in auctions if a['status'] == 'active']
    featured_auctions.sort(key=lambda x: x['current_price'], reverse=True)

    return render_template('dashboard.html',
                           featured_auctions=featured_auctions,
                           categories=categories,
                           trending=trending)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    app.run(debug=True)
