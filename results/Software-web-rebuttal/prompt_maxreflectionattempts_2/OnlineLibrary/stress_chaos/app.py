from flask import Flask, render_template, request, redirect, url_for, flash, session
import os
from datetime import datetime, timedelta

app = Flask("OnlineLibrary")
app.secret_key = "secret"

DATA_DIR = "data"

# Utility functions

def parse_pipe_delimited_file(filename):
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as file:
        lines = file.read().strip().split("\n")
    data = []
    for line in lines:
        if not line.strip():
            continue
        fields = line.split("|")
        data.append(fields)
    return data

def write_pipe_delimited_file(filename, records):
    path = os.path.join(DATA_DIR, filename)
    lines = []
    for rec in records:
        line = "|".join(str(field) if field is not None else "" for field in rec)
        lines.append(line)
    with open(path, "w", encoding="utf-8") as file:
        file.write("\n".join(lines))

# Read users.txt
# username|email|phone|address

def get_users():
    records = parse_pipe_delimited_file("users.txt")
    users = []
    for r in records:
        if len(r) < 4:
            continue
        users.append({
            "username": r[0],
            "email": r[1],
            "phone": r[2],
            "address": r[3]
        })
    return users

# Read books.txt
# book_id|title|author|isbn|genre|publisher|year|description|status|avg_rating

def get_books():
    records = parse_pipe_delimited_file("books.txt")
    books = []
    for r in records:
        if len(r) < 10:
            continue
        books.append({
            "book_id": int(r[0]),
            "title": r[1],
            "author": r[2],
            "isbn": r[3],
            "genre": r[4],
            "publisher": r[5],
            "year": int(r[6]),
            "description": r[7],
            "status": r[8],
            "avg_rating": float(r[9])
        })
    return books

# Write books.txt with full fields including avg_rating
# Because avg_rating is updated by reviews, but we keep data unmodified as per spec no updates on books.txt needed

# Read borrowings.txt
# borrow_id|username|book_id|borrow_date|due_date|return_date|status|fine_amount

def get_borrowings():
    records = parse_pipe_delimited_file("borrowings.txt")
    borrowings = []
    for r in records:
        if len(r) < 8:
            continue
        borrowings.append({
            "borrow_id": int(r[0]),
            "username": r[1],
            "book_id": int(r[2]),
            "borrow_date": r[3],
            "due_date": r[4],
            "return_date": r[5] if r[5] else None,
            "status": r[6],
            "fine_amount": float(r[7])
        })
    return borrowings

# Write borrowings.txt

def write_borrowings(borrowings):
    records = []
    for b in borrowings:
        records.append([
            b["borrow_id"],
            b["username"],
            b["book_id"],
            b["borrow_date"],
            b["due_date"],
            b["return_date"] if b["return_date"] else "",
            b["status"],
            f"{b['fine_amount']:.2f}"
        ])
    write_pipe_delimited_file("borrowings.txt", records)

# Read reservations.txt
# reservation_id|username|book_id|reservation_date|status

def get_reservations():
    records = parse_pipe_delimited_file("reservations.txt")
    reservations = []
    for r in records:
        if len(r) < 5:
            continue
        reservations.append({
            "reservation_id": int(r[0]),
            "username": r[1],
            "book_id": int(r[2]),
            "reservation_date": r[3],
            "status": r[4]
        })
    return reservations

# Write reservations.txt

def write_reservations(reservations):
    records = []
    for r in reservations:
        records.append([
            r["reservation_id"],
            r["username"],
            r["book_id"],
            r["reservation_date"],
            r["status"]
        ])
    write_pipe_delimited_file("reservations.txt", records)

# Read reviews.txt
# review_id|username|book_id|rating|review_text|review_date

def get_reviews():
    records = parse_pipe_delimited_file("reviews.txt")
    reviews = []
    for r in records:
        if len(r) < 6:
            continue
        reviews.append({
            "review_id": int(r[0]),
            "username": r[1],
            "book_id": int(r[2]),
            "rating": int(r[3]),
            "review_text": r[4],
            "review_date": r[5]
        })
    return reviews

# Write reviews.txt

def write_reviews(reviews):
    records = []
    for r in reviews:
        records.append([
            r["review_id"],
            r["username"],
            r["book_id"],
            r["rating"],
            r["review_text"],
            r["review_date"]
        ])
    write_pipe_delimited_file("reviews.txt", records)

# Read fines.txt
# fine_id|username|borrow_id|amount|status|date_issued

def get_fines():
    records = parse_pipe_delimited_file("fines.txt")
    fines = []
    for r in records:
        if len(r) < 6:
            continue
        fines.append({
            "fine_id": int(r[0]),
            "username": r[1],
            "borrow_id": int(r[2]),
            "amount": float(r[3]),
            "status": r[4],
            "date_issued": r[5]
        })
    return fines

# Write fines.txt

def write_fines(fines):
    records = []
    for f in fines:
        records.append([
            f["fine_id"],
            f["username"],
            f["borrow_id"],
            f["amount"],
            f["status"],
            f["date_issued"]
        ])
    write_pipe_delimited_file("fines.txt", records)

# Helpers

def find_book_by_id(book_id):
    books = get_books()
    for book in books:
        if book["book_id"] == book_id:
            return book
    return None

def user_logged_in_username():
    if "username" not in session:
        session["username"] = "john_reader"
    return session["username"]

@app.route("/")
def root_redirect():
    return redirect(url_for("dashboard"))

@app.route("/dashboard")
def dashboard():
    username = user_logged_in_username()
    books = get_books()

    # featured_books with fields: book_id, title, author, status
    featured_books = []
    for book in books:
        featured_books.append({
            "book_id": book["book_id"],
            "title": book["title"],
            "author": book["author"],
            "status": book["status"]
        })

    return render_template("dashboard.html", username=username, featured_books=featured_books)

@app.route("/catalog")
def catalog():
    books = get_books()
    books_simple = []
    for book in books:
        books_simple.append({
            "book_id": book["book_id"],
            "title": book["title"],
            "author": book["author"],
            "status": book["status"]
        })
    return render_template("catalog.html", books=books_simple)

@app.route("/catalog/search", methods=["POST"])
def catalog_search():
    search_query = request.form.get("search_query", "").strip()
    books = get_books()
    filtered = []
    if search_query:
        for book in books:
            if search_query.lower() in book["title"].lower() or search_query.lower() in book["author"].lower():
                filtered.append({
                    "book_id": book["book_id"],
                    "title": book["title"],
                    "author": book["author"],
                    "status": book["status"]
                })
    else:
        for book in books:
            filtered.append({
                "book_id": book["book_id"],
                "title": book["title"],
                "author": book["author"],
                "status": book["status"]
            })
    return render_template("catalog.html", books=filtered, search_query=search_query)

@app.route("/book/<int:book_id>")
def book_details(book_id):
    book = find_book_by_id(book_id)
    if not book:
        flash("Book not found.")
        return redirect(url_for("dashboard"))

    # Gather reviews for book
    reviews_all = get_reviews()
    reviews = []
    for r in reviews_all:
        if r["book_id"] == book_id:
            reviews.append({
                "review_id": r["review_id"],
                "username": r["username"],
                "rating": r["rating"],
                "review_text": r["review_text"],
                "review_date": r["review_date"]
            })

    # Average rating is given in books.txt but to conform, recompute from reviews
    if reviews:
        avg_rating = round(sum(r["rating"] for r in reviews) / len(reviews), 2)
    else:
        avg_rating = 0.0

    book_context = {
        "book_id": book["book_id"],
        "title": book["title"],
        "author": book["author"],
        "status": book["status"],
        "description": book["description"],
        "avg_rating": avg_rating
    }

    return render_template("book_details.html", book=book_context, reviews=reviews)

@app.route("/borrow/<int:book_id>")
def borrow_confirmation(book_id):
    book = find_book_by_id(book_id)
    if not book:
        flash("Book not found.")
        return redirect(url_for("dashboard"))
    due_date = (datetime.today() + timedelta(days=14)).strftime("%Y-%m-%d")
    book_context = {
        "book_id": book["book_id"],
        "title": book["title"],
        "author": book["author"]
    }
    return render_template("borrow_confirmation.html", book=book_context, due_date=due_date)

@app.route("/borrow/<int:book_id>/confirm", methods=["POST"])
def confirm_borrow(book_id):
    username = user_logged_in_username()
    borrowings = get_borrowings()
    new_id = max([b["borrow_id"] for b in borrowings], default=0) + 1
    now = datetime.today()
    borrow_date = now.strftime("%Y-%m-%d")
    due_date = (now + timedelta(days=14)).strftime("%Y-%m-%d")
    new_borrow = {
        "borrow_id": new_id,
        "username": username,
        "book_id": book_id,
        "borrow_date": borrow_date,
        "due_date": due_date,
        "return_date": None,
        "status": "Active",
        "fine_amount": 0.0
    }
    borrowings.append(new_borrow)
    write_borrowings(borrowings)
    return redirect(url_for("my_borrowings"))

@app.route("/borrow/<int:book_id>/cancel", methods=["POST"])
def cancel_borrow(book_id):
    return redirect(url_for("book_details", book_id=book_id))

@app.route("/my_borrowings")
def my_borrowings():
    username = user_logged_in_username()
    borrowings = get_borrowings()
    books = get_books()
    filtered = []

    filter_status = request.args.get("status", "All")

    for b in borrowings:
        if b["username"] == username:
            book_title = next((bk["title"] for bk in books if bk["book_id"] == b["book_id"]), "")
            # Determine overdue status
            b_status = b["status"]
            due_date_obj = datetime.strptime(b["due_date"], "%Y-%m-%d")
            if b_status == "Active" and due_date_obj < datetime.today():
                b_status = "Overdue"

            if filter_status == "All" or b_status == filter_status:
                filtered.append({
                    "borrow_id": b["borrow_id"],
                    "title": book_title,
                    "borrow_date": b["borrow_date"],
                    "due_date": b["due_date"],
                    "status": b_status
                })

    return render_template("my_borrowings.html", borrows=filtered, filter_status=filter_status)

@app.route("/my_borrowings/return/<int:borrow_id>", methods=["POST"])
def return_book(borrow_id):
    borrowings = get_borrowings()
    found = False
    for b in borrowings:
        if b["borrow_id"] == borrow_id and b["status"] == "Active":
            b["status"] = "Returned"
            b["return_date"] = datetime.today().strftime("%Y-%m-%d")
            found = True
            break
    if found:
        write_borrowings(borrowings)
    return redirect(url_for("my_borrowings"))

@app.route("/my_reservations")
def my_reservations():
    username = user_logged_in_username()
    reservations = get_reservations()
    books = get_books()
    filtered = []
    for r in reservations:
        if r["username"] == username:
            book_title = next((bk["title"] for bk in books if bk["book_id"] == r["book_id"]), "")
            filtered.append({
                "reservation_id": r["reservation_id"],
                "title": book_title,
                "reservation_date": r["reservation_date"],
                "status": r["status"]
            })
    return render_template("my_reservations.html", reservations=filtered)

@app.route("/my_reservations/cancel/<int:reservation_id>", methods=["POST"])
def cancel_reservation(reservation_id):
    username = user_logged_in_username()
    reservations = get_reservations()
    changed = False
    for r in reservations:
        if r["reservation_id"] == reservation_id and r["username"] == username:
            r["status"] = "Cancelled"
            changed = True
            break
    if changed:
        write_reservations(reservations)
    return redirect(url_for("my_reservations"))

@app.route("/my_reviews")
def my_reviews():
    username = user_logged_in_username()
    reviews = get_reviews()
    books = get_books()
    filtered = []
    for r in reviews:
        if r["username"] == username:
            book_title = next((bk["title"] for bk in books if bk["book_id"] == r["book_id"]), "")
            filtered.append({
                "review_id": r["review_id"],
                "title": book_title,
                "rating": r["rating"],
                "review_text": r["review_text"],
                "book_id": r["book_id"]
            })
    return render_template("my_reviews.html", reviews=filtered)

@app.route("/my_reviews/delete/<int:review_id>", methods=["POST"])
def delete_review(review_id):
    username = user_logged_in_username()
    reviews = get_reviews()
    changed = False
    for i,r in enumerate(reviews):
        if r["review_id"] == review_id and r["username"] == username:
            del reviews[i]
            changed = True
            break
    if changed:
        write_reviews(reviews)
    return redirect(url_for("my_reviews"))

@app.route("/write_review/<int:book_id>")
def write_review(book_id):
    username = user_logged_in_username()
    book = find_book_by_id(book_id)
    if not book:
        flash("Book not found.")
        return redirect(url_for("dashboard"))

    reviews = get_reviews()
    existing_review = None
    for r in reviews:
        if r["username"] == username and r["book_id"] == book_id:
            existing_review = {
                "review_id": r["review_id"],
                "rating": r["rating"],
                "review_text": r["review_text"]
            }
            break

    book_context = {
        "book_id": book["book_id"],
        "title": book["title"],
        "author": book["author"]
    }
    return render_template("write_review.html", book=book_context, existing_review=existing_review)

@app.route("/write_review/<int:book_id>/submit", methods=["POST"])
def submit_review(book_id):
    username = user_logged_in_username()
    rating = request.form.get("rating")
    review_text = request.form.get("review_text", "").strip()

    try:
        rating_int = int(rating)
        if rating_int < 1 or rating_int > 5:
            raise ValueError()
    except Exception:
        flash("Rating must be an integer between 1 and 5.", "error")
        return redirect(url_for("write_review", book_id=book_id))

    reviews = get_reviews()
    now_str = datetime.today().strftime("%Y-%m-%d")
    found = False
    for r in reviews:
        if r["username"] == username and r["book_id"] == book_id:
            r["rating"] = rating_int
            r["review_text"] = review_text
            r["review_date"] = now_str
            found = True
            break
    if not found:
        new_id = max([r["review_id"] for r in reviews], default=0) + 1
        reviews.append({
            "review_id": new_id,
            "username": username,
            "book_id": book_id,
            "rating": rating_int,
            "review_text": review_text,
            "review_date": now_str
        })
    write_reviews(reviews)
    return redirect(url_for("book_details", book_id=book_id))

@app.route("/profile")
def profile():
    username = user_logged_in_username()
    users = get_users()
    user = next((u for u in users if u["username"] == username), None)
    email = user["email"] if user else ""

    borrowings = get_borrowings()
    books = get_books()
    borrow_history = []
    for b in borrowings:
        if b["username"] == username:
            book_title = next((bk["title"] for bk in books if bk["book_id"] == b["book_id"]), "")
            borrow_history.append({
                "title": book_title,
                "borrow_date": b["borrow_date"],
                "return_date": b["return_date"]
            })

    return render_template("profile.html", username=username, email=email, borrow_history=borrow_history)

@app.route("/profile/update", methods=["POST"])
def update_profile():
    username = user_logged_in_username()
    email = request.form.get("email", "")
    users = get_users()
    updated = False
    for u in users:
        if u["username"] == username:
            u["email"] = email
            updated = True
            break
    if updated:
        records = []
        for u in users:
            records.append([u["username"], u["email"], u["phone"], u["address"]])
        write_pipe_delimited_file("users.txt", records)
    return redirect(url_for("profile"))

@app.route("/payment/<int:fine_id>")
def payment_confirmation(fine_id):
    fines = get_fines()
    fine = next((f for f in fines if f["fine_id"] == fine_id), None)
    if not fine:
        flash("Fine not found.")
        return redirect(url_for("profile"))
    fine_context = {"fine_id": fine["fine_id"], "amount": fine["amount"]}
    return render_template("payment_confirmation.html", fine=fine_context)

@app.route("/payment/<int:fine_id>/confirm", methods=["POST"])
def confirm_payment(fine_id):
    fines = get_fines()
    changed = False
    for f in fines:
        if f["fine_id"] == fine_id:
            if f["status"] != "Paid":
                f["status"] = "Paid"
                changed = True
                break
    if changed:
        write_fines(fines)
    return redirect(url_for("profile"))

@app.route("/payment/<int:fine_id>/cancel", methods=["POST"])
def cancel_payment(fine_id):
    fines = get_fines()
    changed = False
    for f in fines:
        if f["fine_id"] == fine_id:
            if f["status"] != "Cancelled":
                f["status"] = "Cancelled"
                changed = True
                break
    if changed:
        write_fines(fines)
    return redirect(url_for("profile"))

if __name__ == "__main__":
    app.run(debug=True)
