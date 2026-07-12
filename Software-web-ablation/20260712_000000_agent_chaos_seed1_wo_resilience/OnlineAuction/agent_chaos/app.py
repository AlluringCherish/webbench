from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

DATA_DIR = "data"

class OnlineAuction:
    def __init__(self):
        self.products = {}
        self.users = {}
        self.bids = {}
        self.load_data()

    def load_data(self):
        # Load products from products.txt
        products_path = os.path.join(DATA_DIR, "products.txt")
        if os.path.exists(products_path):
            with open(products_path, "r") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        parts = line.split('|')
                        if len(parts) == 5:
                            product_id, product_name, description, start_price, start_date = parts
                            self.products[product_id] = {"product_name": product_name, "description": description, "start_price": float(start_price), "start_date": start_date}

        # Load users from users.txt
        users_path = os.path.join(DATA_DIR, "users.txt")
        if os.path.exists(users_path):
            with open(users_path, "r") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        parts = line.split('|')
                        if len(parts) == 7:
                            user_id, name, email, contact_number, address, district, city = parts
                            self.users[user_id] = {"name": name, "email": email, "contact_number": contact_number, "address": address, "district": district, "city": city}

        # Load bids from bids.txt
        bids_path = os.path.join(DATA_DIR, "bids.txt")
        if os.path.exists(bids_path):
            with open(bids_path, "r") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        parts = line.split('|')
                        if len(parts) == 4:
                            bid_id, bid_amount, user_id, product_id = parts
                            self.bids[bid_id] = {"bid_amount": float(bid_amount), "user_id": user_id, "product_id": product_id}

    def get_all_products(self):
        return self.products

    def get_product(self, product_id):
        return self.products.get(product_id)

    def get_bids_for_product(self, product_id):
        bids = [bid for bid in self.bids.values() if bid["product_id"] == product_id]
        # Sort bids by amount descending
        return sorted(bids, key=lambda x: x["bid_amount"], reverse=True)

    def get_user(self, user_id):
        return self.users.get(user_id)

auction = OnlineAuction()

@app.route("/")
def index():
    products = auction.get_all_products()
    return render_template("index.html", products=products)

@app.route("/bid/<product_id>", methods=["GET", "POST"])
def bid(product_id):
    product = auction.get_product(product_id)
    if not product:
        return "Product not found", 404

    if request.method == "POST":
        user_id = request.form.get("user_id")
        bid_amount = request.form.get("bid_amount")

        # Validate inputs
        if not user_id or not bid_amount:
            return "User ID and bid amount are required", 400

        try:
            bid_amount = float(bid_amount)
        except ValueError:
            return "Invalid bid amount", 400

        user = auction.get_user(user_id)
        if not user:
            return "User not found", 404

        # Append bid to bids.txt
        bids_path = os.path.join(DATA_DIR, "bids.txt")
        with open(bids_path, "a") as f:
            # Generate bid_id as next integer string
            bid_id = str(len(auction.bids) + 1)
            f.write(f"{bid_id}|{bid_amount}|{user_id}|{product_id}\n")

        # Update in-memory bids
        auction.bids[bid_id] = {"bid_amount": bid_amount, "user_id": user_id, "product_id": product_id}

        return redirect(url_for("bid", product_id=product_id))

    bids = auction.get_bids_for_product(product_id)
    # Attach user info for each bid
    bids_with_users = []
    for bid in bids:
        user_info = auction.get_user(bid["user_id"])
        if user_info:
            bids_with_users.append({"bid_amount": bid["bid_amount"], "user": user_info})

    return render_template("bid.html", product=product, bids=bids_with_users)

if __name__ == "__main__":
    app.run(debug=True)
