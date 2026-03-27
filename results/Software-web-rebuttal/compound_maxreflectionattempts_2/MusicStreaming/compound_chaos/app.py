from flask import Flask, render_template, request, redirect, url_for, abort
import os
from datetime import datetime

app = Flask(__name__)
app.debug = True

DATA_PATH = "data"

# Helper function to load pipe-delimited data files

def load_pipe_delimited(filename, fields):
    path = os.path.join(DATA_PATH, filename)
    data = []
    if not os.path.exists(path):
        return data
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split("|")
            if len(parts) < len(fields):
                continue
            entry = {}
            for i, (field, cast) in enumerate(fields):
                try:
                    entry[field] = cast(parts[i])
                except Exception:
                    entry[field] = None
            data.append(entry)
    return data

# Helper function to save pipe-delimited data files

def save_pipe_delimited(filename, fields, data):
    path = os.path.join(DATA_PATH, filename)
    lines = []
    for entry in data:
        parts = []
        for field, _ in fields:
            val = entry.get(field)
            if val is None:
                val = ""
            else:
                val = str(val)
            parts.append(val)
        lines.append("|".join(parts))
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

# Data schema definitions
SONG_FIELDS = [
    ("song_id", int),
    ("title", str),
    ("artist_id", int),
    ("album_id", int),
    ("genre", str),
    ("duration", int),
    ("release_date", str),
    ("play_count", int),
]

ARTIST_FIELDS = [
    ("artist_id", int),
    ("name", str),
    ("genre", str),
    ("country", str),
    ("formation_year", int),
]

ALBUM_FIELDS = [
    ("album_id", int),
    ("title", str),
    ("artist_id", int),
    ("release_year", int),
    ("total_songs", int),
    ("genre", str),
]

GENRE_FIELDS = [
    ("genre_id", int),
    ("genre_name", str),
    ("description", str),
]

PLAYLIST_FIELDS = [
    ("playlist_id", int),
    ("title", str),
    ("description", str),
    ("creation_date", str),
    ("total_songs", int),
]

PLAYLIST_SONG_FIELDS = [
    ("playlist_song_id", int),
    ("playlist_id", int),
    ("song_id", int),
    ("added_date", str),
]

# Loaders

def load_songs():
    return load_pipe_delimited("songs.txt", SONG_FIELDS)

def load_artists():
    return load_pipe_delimited("artists.txt", ARTIST_FIELDS)

def load_albums():
    return load_pipe_delimited("albums.txt", ALBUM_FIELDS)

def load_genres():
    return load_pipe_delimited("genres.txt", GENRE_FIELDS)

def load_playlists():
    return load_pipe_delimited("playlists.txt", PLAYLIST_FIELDS)

def load_playlist_songs():
    return load_pipe_delimited("playlist_songs.txt", PLAYLIST_SONG_FIELDS)

# Fetch single entities by id

def get_artist_by_id(artist_id):
    for a in load_artists():
        if a["artist_id"] == artist_id:
            return a
    return None

def get_album_by_id(album_id):
    for a in load_albums():
        if a["album_id"] == album_id:
            return a
    return None

def get_song_by_id(song_id):
    for s in load_songs():
        if s["song_id"] == song_id:
            return s
    return None

def get_playlist_by_id(playlist_id):
    for p in load_playlists():
        if p["playlist_id"] == playlist_id:
            return p
    return None

def get_playlist_songs_by_playlist_id(playlist_id):
    playlist_songs = load_playlist_songs()
    songs = []
    for ps in playlist_songs:
        if ps["playlist_id"] == playlist_id:
            song = get_song_by_id(ps["song_id"])
            if song:
                songs.append(song)
    return songs

@app.route("/")
def redirect_to_dashboard():
    return redirect(url_for("dashboard_page"))

@app.route("/dashboard")
def dashboard_page():
    songs = load_songs()
    featured_songs_raw = sorted(songs, key=lambda s: s["play_count"], reverse=True)[:5]
    featured_songs = []
    for s in featured_songs_raw:
        artist = get_artist_by_id(s["artist_id"])
        artist_name = artist["name"] if artist else "Unknown"
        featured_songs.append({"song_id": s["song_id"], "title": s["title"], "artist_name": artist_name, "duration": s["duration"]})
    artists = load_artists()
    artist_play_counts = {}
    for s in songs:
        artist_play_counts[s["artist_id"]] = artist_play_counts.get(s["artist_id"], 0) + s["play_count"]
    trending_artist_ids = sorted(artist_play_counts, key=artist_play_counts.get, reverse=True)[:5]
    trending_artists = []
    for aid in trending_artist_ids:
        artist = get_artist_by_id(aid)
        if artist:
            trending_artists.append({"artist_id": aid, "name": artist["name"]})
    return render_template("dashboard.html", featured_songs=featured_songs, trending_artists=trending_artists)

@app.route("/songs")
def song_catalog():
    songs_raw = load_songs()
    songs_list = []
    for s in songs_raw:
        artist = get_artist_by_id(s["artist_id"])
        album = get_album_by_id(s["album_id"])
        songs_list.append({
            "song_id": s["song_id"],
            "title": s["title"],
            "artist_name": artist["name"] if artist else "Unknown",
            "album_name": album["title"] if album else "Unknown",
            "genre": s["genre"],
            "duration": s["duration"],
        })
    genres_raw = load_genres()
    genres = [g["genre_name"] for g in genres_raw if g["genre_name"]]
    return render_template("song_catalog.html", songs=songs_list, genres=genres)

@app.route("/songs/<int:song_id>")
def song_details(song_id):
    s = get_song_by_id(song_id)
    if not s:
        abort(404)
    artist = get_artist_by_id(s["artist_id"])
    album = get_album_by_id(s["album_id"])
    song_context = {
        "song_id": s["song_id"],
        "title": s["title"],
        "artist_id": s["artist_id"],
        "artist_name": artist["name"] if artist else "Unknown",
        "album_id": s["album_id"],
        "album_name": album["title"] if album else "Unknown",
        "genre": s["genre"],
        "duration": s["duration"],
    }
    return render_template("song_details.html", song=song_context)

@app.route("/playlists")
def playlists_page():
    playlists_raw = load_playlists()
    playlists = []
    for p in playlists_raw:
        playlists.append({
            "playlist_id": p["playlist_id"],
            "title": p["title"],
            "description": p["description"],
            "total_songs": p["total_songs"],
        })
    return render_template("playlists.html", playlists=playlists)

@app.route("/playlists/<int:playlist_id>")
def playlist_details(playlist_id):
    playlist = get_playlist_by_id(playlist_id)
    if not playlist:
        abort(404)
    songs_in_playlist = get_playlist_songs_by_playlist_id(playlist_id)
    songs = []
    for s in songs_in_playlist:
        artist = get_artist_by_id(s["artist_id"])
        songs.append({
            "song_id": s["song_id"],
            "title": s["title"],
            "artist_name": artist["name"] if artist else "Unknown",
            "duration": s["duration"],
        })
    playlist_dict = {
        "playlist_id": playlist["playlist_id"],
        "title": playlist["title"],
        "description": playlist["description"],
    }
    return render_template("playlist_details.html", playlist=playlist_dict, songs=songs)

@app.route("/playlists/create", methods=["GET"])
def create_playlist():
    return render_template("create_playlist.html")

@app.route("/playlists/create", methods=["POST"])
def create_playlist_post():
    playlist_name = request.form.get("playlist_name", "").strip()
    playlist_description = request.form.get("playlist_description", "").strip()
    if not playlist_name:
        return redirect(url_for("create_playlist"))
    playlists = load_playlists()
    new_id = 1
    if playlists:
        new_id = max(p["playlist_id"] for p in playlists) + 1
    today = datetime.today().strftime("%Y-%m-%d")
    new_playlist = {
        "playlist_id": new_id,
        "title": playlist_name,
        "description": playlist_description,
        "creation_date": today,
        "total_songs": 0,
    }
    playlists.append(new_playlist)
    save_pipe_delimited("playlists.txt", PLAYLIST_FIELDS, playlists)
    return redirect(url_for("playlists_page"))

@app.route("/albums")
def albums_page():
    albums_raw = load_albums()
    albums_list = []
    for a in albums_raw:
        artist = get_artist_by_id(a["artist_id"])
        albums_list.append({
            "album_id": a["album_id"],
            "title": a["title"],
            "artist_name": artist["name"] if artist else "Unknown",
            "release_year": a["release_year"],
        })
    return render_template("albums.html", albums=albums_list)

@app.route("/albums/<int:album_id>")
def album_details(album_id):
    album = get_album_by_id(album_id)
    if not album:
        abort(404)
    artist = get_artist_by_id(album["artist_id"])
    songs_raw = load_songs()
    songs = []
    for s in songs_raw:
        if s["album_id"] == album_id:
            songs.append({"song_id": s["song_id"], "title": s["title"], "duration": s["duration"]})
    album_context = {
        "album_id": album["album_id"],
        "title": album["title"],
        "artist_id": album["artist_id"],
        "artist_name": artist["name"] if artist else "Unknown",
        "release_year": album["release_year"],
    }
    return render_template("album_details.html", album=album_context, songs=songs)

@app.route("/artists")
def artists_page():
    artists_raw = load_artists()
    artists_list = []
    for a in artists_raw:
        artists_list.append({"artist_id": a["artist_id"], "name": a["name"], "genre": a["genre"], "country": a["country"]})
    return render_template("artists.html", artists=artists_list)

@app.route("/artists/<int:artist_id>")
def artist_profile(artist_id):
    artist = get_artist_by_id(artist_id)
    if not artist:
        abort(404)
    songs_raw = load_songs()
    songs = []
    for s in songs_raw:
        if s["artist_id"] == artist_id:
            album = get_album_by_id(s["album_id"])
            songs.append({"song_id": s["song_id"], "title": s["title"], "album_name": album["title"] if album else "Unknown", "duration": s["duration"]})
    artist_context = {
        "artist_id": artist["artist_id"],
        "name": artist["name"],
        "genre": artist["genre"],
        "country": artist["country"],
        "formation_year": artist["formation_year"],
    }
    return render_template("artist_profile.html", artist=artist_context, songs=songs)

@app.route("/genres")
def genres_page():
    genres_raw = load_genres()
    genres = []
    for g in genres_raw:
        genres.append({"genre_id": g["genre_id"], "genre_name": g["genre_name"], "description": g["description"]})

    selected_genre_id = request.args.get("selected_genre_id", type=int)
    selected_genre = None
    songs_filtered = []
    artists_filtered = []
    if selected_genre_id:
        for g in genres_raw:
            if g["genre_id"] == selected_genre_id:
                selected_genre = g
                break
        if selected_genre:
            songs_raw = load_songs()
            for s in songs_raw:
                if s["genre"].lower() == selected_genre["genre_name"].lower():
                    artist = get_artist_by_id(s["artist_id"])
                    songs_filtered.append({"song_id": s["song_id"], "title": s["title"], "artist_name": artist["name"] if artist else "Unknown", "duration": s["duration"]})
            artists_raw = load_artists()
            for a in artists_raw:
                if a["genre"].lower() == selected_genre["genre_name"].lower():
                    artists_filtered.append({"artist_id": a["artist_id"], "name": a["name"], "genre": a["genre"]})

    return render_template(
        "genres.html",
        genres=genres,
        selected_genre=selected_genre,
        songs=songs_filtered,
        artists=artists_filtered,
    )

if __name__ == "__main__":
    app.run()
