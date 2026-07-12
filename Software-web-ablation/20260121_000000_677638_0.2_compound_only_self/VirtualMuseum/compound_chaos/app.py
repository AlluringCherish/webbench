import os
from flask import Flask, redirect, url_for, request, render_template, abort
from datetime import datetime

app = Flask(__name__)
app.secret_key = "secret-key-virtualmuseum"

DATA_DIR = "data"

# File paths
USERS_FILE = os.path.join(DATA_DIR, "users.txt")
GALLERIES_FILE = os.path.join(DATA_DIR, "galleries.txt")
EXHIBITIONS_FILE = os.path.join(DATA_DIR, "exhibitions.txt")
ARTIFACTS_FILE = os.path.join(DATA_DIR, "artifacts.txt")
AUDIO_GUIDES_FILE = os.path.join(DATA_DIR, "audioguides.txt")
TICKETS_FILE = os.path.join(DATA_DIR, "tickets.txt")
EVENTS_FILE = os.path.join(DATA_DIR, "events.txt")
EVENT_REGS_FILE = os.path.join(DATA_DIR, "event_registrations.txt")


def read_pipe_delimited(filepath):
    if not os.path.exists(filepath):
        return []
    with open(filepath, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]
    return [line.split("|") for line in lines]


def write_pipe_delimited(filepath, rows):
    with open(filepath, "w", encoding="utf-8") as f:
        for row in rows:
            f.write("|".join(row)+"\n")


@app.route("/")
def root_redirect():
    return redirect(url_for("dashboard"))


@app.route("/dashboard")
def dashboard():
    exhibitions = read_pipe_delimited(EXHIBITIONS_FILE)
    total_exhibitions = len(exhibitions)
    active_exhibitions = 0
    today = datetime.today().date()
    for ex in exhibitions:
        if len(ex) >= 7:
            try:
                end_date = datetime.strptime(ex[6], "%Y-%m-%d").date()
                if end_date >= today:
                    active_exhibitions += 1
            except Exception:
                pass
    return render_template("dashboard.html", total_exhibitions=total_exhibitions, active_exhibitions=active_exhibitions)


@app.route("/artifacts", methods=["GET", "POST"])
def artifact_catalog():
    search_query = ""
    filters = {}
    if request.method == "POST":
        search_query = request.form.get("search_query", "").strip()
    else:
        search_query = request.args.get("search_query", "").strip()
    for k,v in request.args.items():
        if k != "search_query":
            filters[k] = v
    rows = read_pipe_delimited(ARTIFACTS_FILE)
    artifacts = []
    # artifact_id|artifact_name|period|origin|description|exhibition_id|storage_location|acquisition_date|added_by
    for r in rows:
        if len(r) < 9:
            continue
        if search_query:
            sq = search_query.lower()
            if sq not in r[1].lower() and sq not in r[0].lower():
                continue
        artifacts.append({
            "artifact_id": r[0],
            "artifact_name": r[1],
            "period": r[2],
            "origin": r[3],
            "description": r[4],
            "exhibition_id": r[5],
            "storage_location": r[6],
            "acquisition_date": r[7],
            "added_by": r[8]
        })
    return render_template("artifact_catalog.html", artifacts=artifacts, search_query=search_query, filters=filters)


@app.route("/exhibitions", methods=["GET", "POST"])
def exhibitions():
    rows = read_pipe_delimited(EXHIBITIONS_FILE)
    if request.method == "GET":
        filter_type = request.args.get("filter_type", "").strip()
        exhibitions = []
        for r in rows:
            if len(r) < 9:
                continue
            if filter_type and r[4].lower() != filter_type.lower():
                continue
            exhibitions.append({
                "exhibition_id": int(r[0]),
                "title": r[1],
                "description": r[2],
                "gallery_id": r[3],
                "exhibition_type": r[4],
                "start_date": r[5],
                "end_date": r[6],
                "curator_name": r[7],
                "created_by": r[8]
            })
        return render_template("exhibitions.html", exhibitions=exhibitions, filter_type=filter_type)
    else:
        exhibition_id_s = request.form.get("exhibition_id", "")
        if not exhibition_id_s.isdigit():
            abort(400)
        exhibition_id = int(exhibition_id_s)
        exhibition = None
        for r in rows:
            if len(r) < 9:
                continue
            if int(r[0]) == exhibition_id:
                exhibition = {
                    "exhibition_id": int(r[0]),
                    "title": r[1],
                    "description": r[2],
                    "gallery_id": r[3],
                    "exhibition_type": r[4],
                    "start_date": r[5],
                    "end_date": r[6],
                    "curator_name": r[7],
                    "created_by": r[8],
                }
                break
        if exhibition is None:
            abort(404)
        artifacts_rows = read_pipe_delimited(ARTIFACTS_FILE)
        artifacts = []
        for art in artifacts_rows:
            if len(art) < 9:
                continue
            if art[5] == str(exhibition_id):
                artifacts.append({
                    "artifact_id": art[0],
                    "artifact_name": art[1],
                    "period": art[2],
                    "origin": art[3],
                    "description": art[4],
                    "storage_location": art[6],
                    "acquisition_date": art[7],
                    "added_by": art[8]
                })
        return render_template("exhibition_details.html", exhibition=exhibition, artifacts=artifacts)


@app.route("/tickets", methods=["GET", "POST"])
def visitor_tickets():
    current_user = "visitor_mary"
    tickets_rows = read_pipe_delimited(TICKETS_FILE)
    tickets = []
    ticket_types = set()
    for t in tickets_rows:
        if len(t) < 10:
            continue
        if t[1] != current_user:
            continue
        tickets.append({
            "ticket_id": t[0],
            "username": t[1],
            "ticket_type": t[2],
            "visit_date": t[3],
            "visit_time": t[4],
            "number_of_tickets": t[5],
            "price": t[6],
            "visitor_name": t[7],
            "visitor_email": t[8],
            "purchase_date": t[9]
        })
        ticket_types.add(t[2])
    ticket_types = sorted(list(ticket_types))
    if request.method == "POST":
        # No ticket purchase logic defined, so ignore
        pass
    return render_template("visitor_tickets.html", tickets=tickets, ticket_types=ticket_types)


@app.route("/events", methods=["GET", "POST"])
def virtual_events():
    current_user = "visitor_mary"
    events_rows = read_pipe_delimited(EVENTS_FILE)
    regs_rows = read_pipe_delimited(EVENT_REGS_FILE)
    if request.method == "POST":
        action = request.form.get("action")
        if action == "cancel":
            registration_id = request.form.get("registration_id")
            if registration_id:
                regs_rows = [r for r in regs_rows if not (r[0] == registration_id and r[2] == current_user)]
                write_pipe_delimited(EVENT_REGS_FILE, regs_rows)
            return redirect(url_for("virtual_events"))
        else:
            abort(400)
    events = []
    for e in events_rows:
        if len(e) < 9:
            continue
        events.append({
            "event_id": int(e[0]),
            "title": e[1],
            "date": e[2],
            "time": e[3],
            "event_type": e[4],
            "speaker": e[5],
            "capacity": e[6],
            "description": e[7],
            "created_by": e[8],
        })
    registrations = []
    for r in regs_rows:
        if len(r) < 4:
            continue
        if r[2] != current_user:
            continue
        registrations.append({
            "registration_id": r[0],
            "event_id": int(r[1]),
            "username": r[2],
            "registration_date": r[3],
        })
    return render_template("virtual_events.html", events=events, registrations=registrations, user=current_user)


@app.route("/events/register/<int:event_id>", methods=["POST"])
def register_event(event_id):
    current_user = "visitor_mary"
    regs_rows = read_pipe_delimited(EVENT_REGS_FILE)
    for r in regs_rows:
        if len(r) > 2 and r[1] == str(event_id) and r[2] == current_user:
            return redirect(url_for("virtual_events"))
    reg_ids = [int(r[0]) for r in regs_rows if r[0].isdigit()]
    new_reg_id = str(max(reg_ids)+1 if reg_ids else 1)
    reg_date = datetime.today().strftime("%Y-%m-%d")
    regs_rows.append([new_reg_id, str(event_id), current_user, reg_date])
    write_pipe_delimited(EVENT_REGS_FILE, regs_rows)
    return redirect(url_for("virtual_events"))


@app.route("/events/cancel/<int:registration_id>", methods=["POST"])
def cancel_registration(registration_id):
    current_user = "visitor_mary"
    regs_rows = read_pipe_delimited(EVENT_REGS_FILE)
    regs_rows = [r for r in regs_rows if not (r[0] == str(registration_id) and r[2] == current_user)]
    write_pipe_delimited(EVENT_REGS_FILE, regs_rows)
    return redirect(url_for("virtual_events"))


@app.route("/audio-guides", methods=["GET", "POST"])
def audio_guides():
    filter_language = ""
    if request.method == "POST":
        filter_language = request.form.get("filter_language", "").strip().lower()
    else:
        filter_language = request.args.get("filter_language", "").strip().lower()
    guides_rows = read_pipe_delimited(AUDIO_GUIDES_FILE)
    audio_guides = []
    for r in guides_rows:
        if len(r) < 8:
            continue
        lang = r[3].lower()
        if filter_language and lang != filter_language:
            continue
        audio_guides.append({
            "guide_id": r[0],
            "exhibit_number": r[1],
            "title": r[2],
            "language": r[3],
            "duration": r[4],
            "script": r[5],
            "narrator": r[6],
            "created_by": r[7]
        })
    return render_template("audio_guides.html", audio_guides=audio_guides, filter_language=filter_language)


if __name__ == "__main__":
    app.run(port=5000, debug=True)
