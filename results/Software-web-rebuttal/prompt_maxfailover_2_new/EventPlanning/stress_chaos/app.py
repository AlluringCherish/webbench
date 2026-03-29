from flask import Flask, render_template, redirect, request, url_for
import os
from typing import List, Dict
from datetime import date

app = Flask(__name__)
DATA_DIR = "data"


def load_events() -> List[Dict]:
    events = []
    path = os.path.join(DATA_DIR, "events.txt")
    if not os.path.isfile(path):
        return events
    with open(path, encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split("|")
            # event_id(int)|event_name(str)|category(str)|date(str)|time(str)|location(str)|description(str)|venue_id(int)|capacity(int)
            if len(parts) < 9:
                continue
            try:
                event = {
                    "event_id": int(parts[0].strip()),
                    "event_name": parts[1].strip(),
                    "category": parts[2].strip(),
                    "date": parts[3].strip(),
                    "time": parts[4].strip(),
                    "location": parts[5].strip(),
                    "description": parts[6].strip(),
                    "venue_id": int(parts[7].strip()),
                    "capacity": int(parts[8].strip()),
                }
                events.append(event)
            except ValueError:
                continue
    return events


def load_venues() -> List[Dict]:
    venues = []
    path = os.path.join(DATA_DIR, "venues.txt")
    if not os.path.isfile(path):
        return venues
    with open(path, encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split("|")
            # venue_id(int)|venue_name(str)|location(str)|capacity(int)|amenities(str)|contact(str)
            if len(parts) < 6:
                continue
            try:
                venue = {
                    "venue_id": int(parts[0].strip()),
                    "venue_name": parts[1].strip(),
                    "location": parts[2].strip(),
                    "capacity": int(parts[3].strip()),
                    "amenities": parts[4].strip(),
                    "contact": parts[5].strip(),
                }
                venues.append(venue)
            except ValueError:
                continue
    return venues


def load_tickets() -> List[Dict]:
    tickets = []
    path = os.path.join(DATA_DIR, "tickets.txt")
    if not os.path.isfile(path):
        return tickets
    with open(path, encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split("|")
            # ticket_id(int)|event_id(int)|ticket_type(str)|price(float)|available_count(int)|sold_count(int)
            if len(parts) < 6:
                continue
            try:
                ticket = {
                    "ticket_id": int(parts[0].strip()),
                    "event_id": int(parts[1].strip()),
                    "ticket_type": parts[2].strip(),
                    "price": float(parts[3].strip()),
                    "available_count": int(parts[4].strip()),
                    "sold_count": int(parts[5].strip()),
                }
                tickets.append(ticket)
            except ValueError:
                continue
    return tickets


def load_bookings() -> List[Dict]:
    bookings = []
    path = os.path.join(DATA_DIR, "bookings.txt")
    if not os.path.isfile(path):
        return bookings
    with open(path, encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split("|")
            # booking_id(int)|event_id(int)|customer_name(str)|booking_date(str)|ticket_count(int)|ticket_type(str)|total_amount(float)|status(str)
            if len(parts) < 8:
                continue
            try:
                booking = {
                    "booking_id": int(parts[0].strip()),
                    "event_id": int(parts[1].strip()),
                    "customer_name": parts[2].strip(),
                    "booking_date": parts[3].strip(),
                    "ticket_count": int(parts[4].strip()),
                    "ticket_type": parts[5].strip(),
                    "total_amount": float(parts[6].strip()),
                    "status": parts[7].strip(),
                }
                bookings.append(booking)
            except ValueError:
                continue
    return bookings


def load_participants() -> List[Dict]:
    participants = []
    path = os.path.join(DATA_DIR, "participants.txt")
    if not os.path.isfile(path):
        return participants
    with open(path, encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split("|")
            # participant_id(int)|event_id(int)|name(str)|email(str)|booking_id(int)|status(str)|registration_date(str)
            if len(parts) < 7:
                continue
            try:
                participant = {
                    "participant_id": int(parts[0].strip()),
                    "event_id": int(parts[1].strip()),
                    "name": parts[2].strip(),
                    "email": parts[3].strip(),
                    "booking_id": int(parts[4].strip()),
                    "status": parts[5].strip(),
                    "registration_date": parts[6].strip(),
                }
                participants.append(participant)
            except ValueError:
                continue
    return participants


def load_schedules() -> List[Dict]:
    schedules = []
    path = os.path.join(DATA_DIR, "schedules.txt")
    if not os.path.isfile(path):
        return schedules
    with open(path, encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split("|")
            # schedule_id(int)|event_id(int)|session_title(str)|session_time(str)|duration_minutes(int)|speaker(str)|venue_id(int)
            if len(parts) < 7:
                continue
            try:
                schedule = {
                    "schedule_id": int(parts[0].strip()),
                    "event_id": int(parts[1].strip()),
                    "session_title": parts[2].strip(),
                    "session_time": parts[3].strip(),
                    "duration_minutes": int(parts[4].strip()),
                    "speaker": parts[5].strip(),
                    "venue_id": int(parts[6].strip()),
                }
                schedules.append(schedule)
            except ValueError:
                continue
    return schedules


@app.route("/")
def root_redirect():
    return redirect(url_for("dashboard_page"))


@app.route("/dashboard")
def dashboard_page():
    events = load_events()
    featured_events = sorted(events, key=lambda e: e["date"])[:5]
    # To match context keys: event_id, event_name, date, location
    feat_events_simple = [{"event_id": e["event_id"], "event_name": e["event_name"], "date": e["date"], "location": e["location"]} for e in featured_events]
    return render_template("dashboard.html", featured_events=feat_events_simple)


@app.route("/events")
def events_listing_page():
    events = load_events()
    return render_template("events.html", events=events)


@app.route("/events/search", methods=["POST"])
def events_search():
    category = request.form.get("category", "").strip()
    events = load_events()
    if category:
        filtered_events = [e for e in events if e["category"].lower() == category.lower()]
    else:
        filtered_events = events
    return render_template("events.html", events=filtered_events)


@app.route("/event/<int:event_id>")
def event_details_page(event_id: int):
    events = load_events()
    event = next((e for e in events if e["event_id"] == event_id), None)
    if not event:
        return redirect(url_for("events_listing_page"))
    return render_template("event_details.html", event=event)


@app.route("/book_ticket", methods=["GET", "POST"])
def book_ticket_page():
    events = load_events()
    if request.method == "GET":
        # Only event_id and event_name needed for dropdown
        simple_events = [{"event_id": e["event_id"], "event_name": e["event_name"]} for e in events]
        return render_template("book_ticket.html", events=simple_events)

    # POST logic
    try:
        event_id = int(request.form.get("event_id", ""))
        ticket_count = int(request.form.get("ticket_count", "0"))
        ticket_type = request.form.get("ticket_type", "")
    except (ValueError, TypeError):
        simple_events = [{"event_id": e["event_id"], "event_name": e["event_name"]} for e in events]
        error = "Invalid form submission."
        return render_template("book_ticket.html", events=simple_events, error=error)

    customer_name = request.form.get("customer_name", "").strip()
    if ticket_count <= 0 or not ticket_type or not customer_name:
        simple_events = [{"event_id": e["event_id"], "event_name": e["event_name"]} for e in events]
        error = "All fields are required with valid values."
        return render_template("book_ticket.html", events=simple_events, error=error)

    event = next((e for e in events if e["event_id"] == event_id), None)
    if not event:
        simple_events = [{"event_id": e["event_id"], "event_name": e["event_name"]} for e in events]
        error = "Selected event not found."
        return render_template("book_ticket.html", events=simple_events, error=error)

    bookings = load_bookings()
    tickets = load_tickets()
    # Calculate tickets sold for this event and ticket_type
    sold_count = 0
    for t in tickets:
        if t["event_id"] == event_id and t["ticket_type"].lower() == ticket_type.lower():
            sold_count = t["sold_count"]
            available_count = t["available_count"]
            break
    else:
        sold_count = 0
        available_count = 0

    if ticket_count > available_count - sold_count:
        simple_events = [{"event_id": e["event_id"], "event_name": e["event_name"]} for e in events]
        error = "Not enough tickets available for the selected ticket type."
        return render_template("book_ticket.html", events=simple_events, error=error)

    ticket_price = 0
    for t in tickets:
        if t["event_id"] == event_id and t["ticket_type"].lower() == ticket_type.lower():
            ticket_price = t["price"]
            break

    total_amount = ticket_price * ticket_count
    max_booking_id = max([b["booking_id"] for b in bookings], default=0)
    new_booking_id = max_booking_id + 1
    booking_date = str(date.today())

    new_booking = {
        "booking_id": new_booking_id,
        "event_id": event_id,
        "customer_name": customer_name,
        "booking_date": booking_date,
        "ticket_count": ticket_count,
        "ticket_type": ticket_type,
        "total_amount": total_amount,
        "status": "Confirmed",
    }
    line = "|".join([
        str(new_booking["booking_id"]),
        str(new_booking["event_id"]),
        new_booking["customer_name"],
        new_booking["booking_date"],
        str(new_booking["ticket_count"]),
        new_booking["ticket_type"],
        f"{new_booking['total_amount']:.2f}",
        new_booking["status"],
    ])
    with open(os.path.join(DATA_DIR, "bookings.txt"), "a", encoding="utf-8") as f:
        f.write(line + "\n")

    return render_template("book_ticket.html", booking_confirmation=new_booking)


@app.route("/participants")
def participants_page():
    participants = load_participants()
    return render_template("participants.html", participants=participants)


@app.route("/participants/add", methods=["POST"])
def add_participant():
    participants = load_participants()
    try:
        event_id = int(request.form.get("event_id", ""))
        booking_id = int(request.form.get("booking_id", ""))
    except (ValueError, TypeError):
        error = "Event ID and Booking ID must be numbers."
        return render_template("participants.html", participants=participants, error=error)

    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    status = request.form.get("status", "Registered").strip()
    registration_date = request.form.get("registration_date", "").strip()

    if not all([name, email, registration_date]):
        error = "All fields are required."
        return render_template("participants.html", participants=participants, error=error)

    max_participant_id = max([p["participant_id"] for p in participants], default=0)
    new_participant_id = max_participant_id + 1

    new_participant = {
        "participant_id": new_participant_id,
        "event_id": event_id,
        "name": name,
        "email": email,
        "booking_id": booking_id,
        "status": status,
        "registration_date": registration_date,
    }
    line = "|".join([
        str(new_participant["participant_id"]),
        str(new_participant["event_id"]),
        new_participant["name"],
        new_participant["email"],
        str(new_participant["booking_id"]),
        new_participant["status"],
        new_participant["registration_date"],
    ])
    with open(os.path.join(DATA_DIR, "participants.txt"), "a", encoding="utf-8") as f:
        f.write(line + "\n")

    updated_participants = load_participants()
    return render_template("participants.html", participants=updated_participants)


@app.route("/participants/search", methods=["POST"])
def search_participants():
    name_filter = request.form.get("name", "").strip().lower()
    status_filter = request.form.get("status", "").strip().lower()
    participants = load_participants()

    filtered = participants
    if name_filter:
        filtered = [p for p in filtered if name_filter in p["name"].lower()]
    if status_filter and status_filter in {"registered", "confirmed", "attended"}:
        filtered = [p for p in filtered if p["status"].lower() == status_filter]
    return render_template("participants.html", participants=filtered)


@app.route("/venues")
def venues_page():
    venues = load_venues()
    return render_template("venues.html", venues=venues)


@app.route("/venues/search", methods=["POST"])
def venues_search():
    capacity_filter = request.form.get("capacity", "").strip().lower()
    venues = load_venues()

    def capacity_category(cap):
        if cap < 100:
            return "small"
        elif cap < 500:
            return "medium"
        else:
            return "large"

    if capacity_filter:
        filtered_venues = [v for v in venues if capacity_category(v["capacity"]) == capacity_filter]
    else:
        filtered_venues = venues

    return render_template("venues.html", venues=filtered_venues)


@app.route("/event_schedules")
def event_schedules_page():
    schedules = load_schedules()
    return render_template("schedules.html", schedules=schedules)


@app.route("/event_schedules/filter", methods=["POST"])
def filter_schedules():
    filter_event_id_str = request.form.get("event_id", "").strip()
    filter_date = request.form.get("date", "").strip()
    schedules = load_schedules()
    filtered = schedules

    if filter_event_id_str:
        try:
            filter_event_id = int(filter_event_id_str)
            filtered = [s for s in filtered if s["event_id"] == filter_event_id]
        except ValueError:
            pass

    if filter_date:
        filtered = [s for s in filtered if s["session_time"].startswith(filter_date)]

    return render_template("schedules.html", filtered_schedules=filtered)


@app.route("/bookings")
def bookings_page():
    bookings = load_bookings()
    events = load_events()
    event_map = {e["event_id"]: e for e in events}

    enriched_bookings = []
    for b in bookings:
        event = event_map.get(b["event_id"])
        enriched = dict(b)
        enriched["event_name"] = event["event_name"] if event else "Unknown"
        enriched_bookings.append(enriched)

    return render_template("bookings.html", bookings=enriched_bookings)


@app.route("/bookings/cancel/<int:booking_id>", methods=["POST"])
def cancel_booking(booking_id: int):
    bookings = load_bookings()
    updated = False
    for b in bookings:
        if b["booking_id"] == booking_id:
            if b["status"].lower() != "cancelled":
                b["status"] = "Cancelled"
                updated = True
            break
    if updated:
        lines = []
        for b in bookings:
            line = "|".join([
                str(b["booking_id"]),
                str(b["event_id"]),
                b["customer_name"],
                b["booking_date"],
                str(b["ticket_count"]),
                b["ticket_type"],
                f"{b['total_amount']:.2f}",
                b["status"],
            ])
            lines.append(line)
        with open(os.path.join(DATA_DIR, "bookings.txt"), "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
    return redirect(url_for("bookings_page"))


if __name__ == "__main__":
    app.run(port=5000)
