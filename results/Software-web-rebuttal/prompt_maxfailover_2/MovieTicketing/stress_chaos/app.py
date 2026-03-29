from flask import Flask, render_template, redirect, url_for, request, abort
import os
from typing import List, Dict
from datetime import datetime

app = Flask(__name__)
app.secret_key = "your_secret_key"

DATA_DIR = "data"
MOVIES_FILE = os.path.join(DATA_DIR, "movies.txt")
THEATERS_FILE = os.path.join(DATA_DIR, "theaters.txt")
SHOWTIMES_FILE = os.path.join(DATA_DIR, "showtimes.txt")
SEATS_FILE = os.path.join(DATA_DIR, "seats.txt")
BOOKINGS_FILE = os.path.join(DATA_DIR, "bookings.txt")
GENRES_FILE = os.path.join(DATA_DIR, "genres.txt")


def load_pipe_delimited(filepath: str, expected_columns: int) -> List[List[str]]:
    rows = []
    if not os.path.exists(filepath):
        return rows
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split("|")
                if len(parts) == expected_columns:
                    rows.append(parts)
        return rows
    except Exception:
        return []


def load_movies() -> List[Dict]:
    # movie_id|title|director|genre|rating|duration|description|release_date
    raw = load_pipe_delimited(MOVIES_FILE, 8)
    movies = []
    for r in raw:
        try:
            movies.append({
                "movie_id": int(r[0]),
                "title": r[1],
                "director": r[2],
                "genre": r[3],
                "rating": float(r[4]),
                "duration": int(r[5]),
                "description": r[6],
                "release_date": r[7]
            })
        except Exception:
            continue
    return movies


def load_theaters() -> List[Dict]:
    # theater_id|theater_name|location|city|screens|facilities
    raw = load_pipe_delimited(THEATERS_FILE, 6)
    theaters = []
    for r in raw:
        try:
            theaters.append({
                "theater_id": int(r[0]),
                "theater_name": r[1],
                "location": r[2],
                "city": r[3],
                "screens": int(r[4]),
                "facilities": r[5]  # raw string like: "3D, Premium Parking"
            })
        except Exception:
            continue
    return theaters


def load_showtimes() -> List[Dict]:
    # showtime_id|movie_id|theater_id|showtime_date|showtime_time|price|available_seats
    raw = load_pipe_delimited(SHOWTIMES_FILE, 7)
    showtimes = []
    for r in raw:
        try:
            showtimes.append({
                "showtime_id": int(r[0]),
                "movie_id": int(r[1]),
                "theater_id": int(r[2]),
                "date": r[3],
                "time": r[4],
                "price": float(r[5]),
                "available_seats": int(r[6])
            })
        except Exception:
            continue
    return showtimes


def load_seats() -> List[Dict]:
    # seat_id|theater_id|screen_id|row|column|seat_type|status
    raw = load_pipe_delimited(SEATS_FILE, 7)
    seats = []
    for r in raw:
        try:
            seats.append({
                "seat_id": int(r[0]),
                "theater_id": int(r[1]),
                "screen_id": int(r[2]),
                "row": r[3],
                "column": int(r[4]),
                "seat_type": r[5],
                "status": r[6]  # Available or Booked
            })
        except Exception:
            continue
    return seats


def save_seats(seats: List[Dict]):
    try:
        with open(SEATS_FILE, "w", encoding="utf-8") as f:
            for seat in seats:
                line = f"{seat['seat_id']}|{seat['theater_id']}|{seat['screen_id']}|{seat['row']}|{seat['column']}|{seat['seat_type']}|{seat['status']}\n"
                f.write(line)
        return True
    except Exception:
        return False


def load_bookings() -> List[Dict]:
    # booking_id|showtime_id|customer_name|customer_email|booking_date|total_price|status|seats_booked
    raw = load_pipe_delimited(BOOKINGS_FILE, 8)
    bookings = []
    for r in raw:
        try:
            bookings.append({
                "booking_id": int(r[0]),
                "showtime_id": int(r[1]),
                "customer_name": r[2],
                "customer_email": r[3],
                "booking_date": r[4],
                "total_price": float(r[5]),
                "status": r[6],
                "seats_booked": r[7].split(",") if r[7] else []
            })
        except Exception:
            continue
    return bookings


def save_bookings(bookings: List[Dict]) -> bool:
    try:
        with open(BOOKINGS_FILE, "w", encoding="utf-8") as f:
            for b in bookings:
                seats_str = ",".join(b["seats_booked"])
                line = f"{b['booking_id']}|{b['showtime_id']}|{b['customer_name']}|{b['customer_email']}|{b['booking_date']}|{b['total_price']:.2f}|{b['status']}|{seats_str}\n"
                f.write(line)
        return True
    except Exception:
        return False


def load_genres() -> List[Dict]:
    # genre_id|genre_name|description
    raw = load_pipe_delimited(GENRES_FILE, 3)
    genres = []
    for r in raw:
        try:
            genres.append({
                "genre_id": int(r[0]),
                "genre_name": r[1],
                "description": r[2]
            })
        except Exception:
            continue
    return genres


@app.route("/", methods=["GET"])
def root_redirect():
    return redirect(url_for("dashboard_page"))


@app.route("/dashboard", methods=["GET"])
def dashboard_page():
    movies = load_movies()
    # Featured movies: top rated (top 5) by rating descending
    movies_sorted = sorted(movies, key=lambda m: m["rating"], reverse=True)
    featured_movies = [{"movie_id": m["movie_id"], "title": m["title"], "rating": m["rating"]} for m in movies_sorted[:5]]

    # Upcoming releases: sort by release_date ascending, next 5 upcoming from today (simple filter)
    today_str = datetime.now().strftime("%Y-%m-%d")
    upcoming = [m for m in movies if m["release_date"] >= today_str]
    upcoming_releases_sorted = sorted(upcoming, key=lambda m: m["release_date"])
    upcoming_releases = [{"movie_id": m["movie_id"], "title": m["title"], "release_date": m["release_date"]} for m in upcoming_releases_sorted[:5]]

    return render_template("dashboard.html", featured_movies=featured_movies, upcoming_releases=upcoming_releases)


@app.route("/movies", methods=["GET"])
def movie_catalog():
    movies = load_movies()
    genres = load_genres()
    # Add poster_url as static path /static/posters/{movie_id}.jpg
    movies_context = []
    for m in movies:
        movies_context.append({
            "movie_id": m["movie_id"],
            "title": m["title"],
            "genre": m["genre"],
            "rating": m["rating"],
            "duration": m["duration"],
            "poster_url": url_for('static', filename=f"posters/{m['movie_id']}.jpg")
        })
    return render_template("movie_catalog.html", movies=movies_context, genres=genres)


@app.route("/movies/<int:movie_id>", methods=["GET"])
def movie_details(movie_id: int):
    movies = load_movies()
    movie = next((m for m in movies if m["movie_id"] == movie_id), None)
    if not movie:
        abort(404)
    return render_template("movie_details.html", movie=movie)


@app.route("/movies/<int:movie_id>/showtimes", methods=["GET"])
def showtime_selection(movie_id: int):
    theaters = load_theaters()
    showtimes_all = load_showtimes()

    # Filters
    filter_theater_id = request.args.get("filter_theater_id", type=int)
    filter_date = request.args.get("filter_date", default=None, type=str)

    # Filter showtimes for given movie
    showtimes_filtered = [s for s in showtimes_all if s["movie_id"] == movie_id]

    if filter_theater_id is not None:
        showtimes_filtered = [s for s in showtimes_filtered if s["theater_id"] == filter_theater_id]
    if filter_date:
        showtimes_filtered = [s for s in showtimes_filtered if s["date"] == filter_date]

    # Build list of showtime dicts with theater_name
    theater_map = {t["theater_id"]: t for t in theaters}
    showtimes_context = []
    for s in showtimes_filtered:
        t = theater_map.get(s["theater_id"])
        if not t:
            continue
        showtimes_context.append({
            "showtime_id": s["showtime_id"],
            "date": s["date"],
            "time": s["time"],
            "theater_name": t["theater_name"],
            "price": s["price"]
        })

    theaters_context = [{"theater_id": t["theater_id"], "theater_name": t["theater_name"]} for t in theaters]

    return render_template("showtime_selection.html", showtimes=showtimes_context, theaters=theaters_context,
                           filter_theater_id=filter_theater_id, filter_date=filter_date)


@app.route("/showtimes/select/<int:showtime_id>", methods=["POST"])
def select_showtime(showtime_id: int):
    # Redirect to seat selection page
    return redirect(url_for("seat_selection", showtime_id=showtime_id))


@app.route("/seat-selection/<int:showtime_id>", methods=["GET"])
def seat_selection(showtime_id: int):
    showtimes = load_showtimes()
    st = next((s for s in showtimes if s["showtime_id"] == showtime_id), None)
    if not st:
        abort(404)

    seats = load_seats()
    # Filter seats for theater and screen of the showtime
    relevant_seats = [seat for seat in seats if seat["theater_id"] == st["theater_id"]]

    seat_map = []
    for seat in relevant_seats:
        # Compose seat dict with required fields
        seat_map.append({
            "seat_id": seat["seat_id"],
            "row": seat["row"],
            "column": seat["column"],
            "seat_type": seat["seat_type"],
            "status": seat["status"]
        })

    selected_seats = []  # Initially empty

    return render_template("seat_selection.html", seat_map=seat_map, selected_seats=selected_seats, showtime_id=showtime_id)


@app.route("/booking/confirm/<int:showtime_id>", methods=["GET", "POST"])
def booking_confirmation(showtime_id: int):
    showtimes = load_showtimes()
    theaters = load_theaters()
    movies = load_movies()

    st = next((s for s in showtimes if s["showtime_id"] == showtime_id), None)
    if not st:
        abort(404)
    theater = next((t for t in theaters if t["theater_id"] == st["theater_id"]), None)
    movie = next((m for m in movies if m["movie_id"] == st["movie_id"]), None)
    if not theater or not movie:
        abort(404)

    if request.method == "GET":
        selected_seats = request.args.getlist("selected_seats")
        total_price = st["price"] * len(selected_seats)

        showtime_context = {
            "showtime_id": showtime_id,
            "movie_title": movie["title"],
            "theater_name": theater["theater_name"],
            "date": st["date"],
            "time": st["time"],
            "price": st["price"]
        }
        return render_template("booking_confirmation.html", showtime=showtime_context,
                               selected_seats=selected_seats, total_price=total_price)
    else:
        # POST to confirm booking
        customer_name = request.form.get("customer-name", "").strip()
        customer_email = request.form.get("customer-email", "").strip()
        selected_seats = request.form.getlist("selected_seats")

        if not customer_name or not customer_email or not selected_seats:
            abort(400)

        total_price = st["price"] * len(selected_seats)
        bookings = load_bookings()
        max_booking_id = max([b["booking_id"] for b in bookings], default=0)
        new_booking_id = max_booking_id + 1
        booking_date = datetime.now().strftime("%Y-%m-%d")

        new_booking = {
            "booking_id": new_booking_id,
            "showtime_id": showtime_id,
            "customer_name": customer_name,
            "customer_email": customer_email,
            "booking_date": booking_date,
            "total_price": total_price,
            "status": "Confirmed",
            "seats_booked": selected_seats
        }

        bookings.append(new_booking)

        if not save_bookings(bookings):
            abort(500)

        # Update seat status to Booked
        seats = load_seats()
        seat_id_set = set()
        # We do not have seat_ids as strings from form, convert from IDs as str to int
        try:
            seat_id_set = set(int(s) for s in selected_seats)
        except Exception:
            abort(400)

        changed = False
        for seat in seats:
            if seat["seat_id"] in seat_id_set:
                if seat["status"] == "Available":
                    seat["status"] = "Booked"
                    changed = True

        if changed:
            if not save_seats(seats):
                # Could not save seat updates but booking saved
                pass

        return redirect(url_for("booking_history"))


@app.route("/bookings", methods=["GET"])
def booking_history():
    bookings = load_bookings()
    showtimes = load_showtimes()
    movies = load_movies()

    showtime_map = {s["showtime_id"]: s for s in showtimes}
    movie_map = {m["movie_id"]: m for m in movies}

    bookings_context = []
    for b in bookings:
        st = showtime_map.get(b["showtime_id"])
        movie_title = "Unknown"
        if st:
            movie = movie_map.get(st["movie_id"])
            if movie:
                movie_title = movie["title"]

        bookings_context.append({
            "booking_id": b["booking_id"],
            "movie_title": movie_title,
            "booking_date": b["booking_date"],
            "seats_booked": b["seats_booked"],
            "status": b["status"]
        })

    return render_template("booking_history.html", bookings=bookings_context)


@app.route("/bookings/<int:booking_id>", methods=["GET"])
def booking_details(booking_id: int):
    bookings = load_bookings()
    booking = next((b for b in bookings if b["booking_id"] == booking_id), None)
    if not booking:
        abort(404)
    return render_template("booking_details.html", booking=booking)


@app.route("/theaters", methods=["GET"])
def theater_information():
    filter_location = request.args.get("filter_location", default=None, type=str)
    theaters = load_theaters()
    if filter_location:
        theaters = [t for t in theaters if filter_location.lower() in t["location"].lower()]

    return render_template("theater_information.html", theaters=theaters, filter_location=filter_location)


if __name__ == "__main__":
    app.run()
