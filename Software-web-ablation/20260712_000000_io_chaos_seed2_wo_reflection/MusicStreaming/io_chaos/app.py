from flask import Flask, render_template, redirect, url_for, request, abort
from datetime import datetime
import os

app = Flask(__name__)

DATA_DIR = "data"

# --- Data loading helpers ---

def read_songs():
    songs = []
    path = os.path.join(DATA_DIR, "songs.txt")
    if not os.path.exists(path):
        return songs
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 8:
                continue
            try:
                song_id = int(parts[0])
                title = parts[1]
                artist_id = int(parts[2])
                album_id = int(parts[3])
                genre = parts[4]
                duration = int(parts[5])
                release_date = parts[6]
                play_count = int(parts[7])
                songs.append({
                    "song_id": song_id,
                    "title": title,
                    "artist_id": artist_id,
                    "album_id": album_id,
                    "genre": genre,
                    "duration": duration,
                    "release_date": release_date,
                    "play_count": play_count
                })
            except ValueError:
                continue
    return songs

def read_artists():
    artists = []
    path = os.path.join(DATA_DIR, "artists.txt")
    if not os.path.exists(path):
        return artists
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 5:
                continue
            try:
                artist_id = int(parts[0])
                name = parts[1]
                genre = parts[2]
                country = parts[3]
                formation_year = int(parts[4])
                artists.append({
                    "artist_id": artist_id,
                    "name": name,
                    "genre": genre,
                    "country": country,
                    "formation_year": formation_year
                })
            except ValueError:
                continue
    return artists

def read_albums():
    albums = []
    path = os.path.join(DATA_DIR, "albums.txt")
    if not os.path.exists(path):
        return albums
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 6:
                continue
            try:
                album_id = int(parts[0])
                title = parts[1]
                artist_id = int(parts[2])
                release_year = int(parts[3])
                total_songs = int(parts[4])
                genre = parts[5]
                albums.append({
                    "album_id": album_id,
                    "title": title,
                    "artist_id": artist_id,
                    "release_year": release_year,
                    "total_songs": total_songs,
                    "genre": genre
                })
            except ValueError:
                continue
    return albums

def read_genres():
    genres = []
    path = os.path.join(DATA_DIR, "genres.txt")
    if not os.path.exists(path):
        return genres
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 3:
                continue
            try:
                genre_id = int(parts[0])
                genre_name = parts[1]
                description = parts[2]
                genres.append({
                    "genre_id": genre_id,
                    "genre_name": genre_name,
                    "description": description
                })
            except ValueError:
                continue
    return genres

def read_playlists():
    playlists = []
    path = os.path.join(DATA_DIR, "playlists.txt")
    if not os.path.exists(path):
        return playlists
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 5:
                continue
            try:
                playlist_id = int(parts[0])
                title = parts[1]
                description = parts[2]
                creation_date = parts[3]
                total_songs = int(parts[4])
                playlists.append({
                    "playlist_id": playlist_id,
                    "title": title,
                    "description": description,
                    "creation_date": creation_date,
                    "total_songs": total_songs
                })
            except ValueError:
                continue
    return playlists

def read_playlist_songs():
    playlist_songs = []
    path = os.path.join(DATA_DIR, "playlist_songs.txt")
    if not os.path.exists(path):
        return playlist_songs
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 4:
                continue
            try:
                playlist_song_id = int(parts[0])
                playlist_id = int(parts[1])
                song_id = int(parts[2])
                added_date = parts[3]
                playlist_songs.append({
                    "playlist_song_id": playlist_song_id,
                    "playlist_id": playlist_id,
                    "song_id": song_id,
                    "added_date": added_date
                })
            except ValueError:
                continue
    return playlist_songs

# --- Data writing helpers ---
from functions import write_text_file

def write_playlists(playlists):
    lines = []
    for p in playlists:
        line = f"{p['playlist_id']}|{p['title']}|{p['description']}|{p['creation_date']}|{p['total_songs']}"
        lines.append(line)
    content = "\n".join(lines)
    filename = os.path.join(DATA_DIR, "playlists.txt")
    # Use provided write_text_file tool
    write_text_file(filename=filename, content=content)


def write_playlist_songs(playlist_songs):
    lines = []
    for ps in playlist_songs:
        line = f"{ps['playlist_song_id']}|{ps['playlist_id']}|{ps['song_id']}|{ps['added_date']}"
        lines.append(line)
    content = "\n".join(lines)
    filename = os.path.join(DATA_DIR, "playlist_songs.txt")
    write_text_file(filename=filename, content=content)

# --- Helper to get next ID ---
def get_next_id(records, id_field):
    if not records:
        return 1
    max_id = max(r[id_field] for r in records)
    return max_id + 1

# --- Routes Implementation ---

@app.route('/')
def root_redirect():
    # Redirect to /dashboard
    return redirect(url_for('dashboard_page'))

@app.route('/dashboard')
def dashboard_page():
    songs = read_songs()
    artists = read_artists()

    # Featured songs: Choose top 5 songs by play_count
    sorted_songs = sorted(songs, key=lambda x: x.get('play_count', 0), reverse=True)
    featured_songs_raw = sorted_songs[:5]

    # Prepare featured_songs context: {song_id, title, artist, duration}
    # Need artist name for each song
    artist_dict = {a['artist_id']: a['name'] for a in artists}
    featured_songs = []
    for s in featured_songs_raw:
        artist_name = artist_dict.get(s['artist_id'], "Unknown Artist")
        featured_songs.append({
            "song_id": s['song_id'],
            "title": s['title'],
            "artist": artist_name,
            "duration": s['duration']
        })

    # Trending artists: Choose top 5 artists by sum of play_counts of their songs
    artist_play_counts = {}
    for s in songs:
        artist_play_counts[s['artist_id']] = artist_play_counts.get(s['artist_id'], 0) + s.get('play_count', 0)
    artist_play_counts_sorted = sorted(artist_play_counts.items(), key=lambda x: x[1], reverse=True)
    trending_artist_ids = [aid for aid, _ in artist_play_counts_sorted[:5]]

    trending_artists = []
    for aid in trending_artist_ids:
        artist = next((a for a in artists if a['artist_id'] == aid), None)
        if artist:
            trending_artists.append({"artist_id": artist['artist_id'], "name": artist['name']})

    return render_template("dashboard.html", featured_songs=featured_songs, trending_artists=trending_artists)

@app.route('/songs')
def song_catalog_page():
    songs = read_songs()
    artists = read_artists()
    albums = read_albums()
    genres_data = read_genres()

    # Map ids to names
    artist_dict = {a['artist_id']: a['name'] for a in artists}
    album_dict = {a['album_id']: a['title'] for a in albums}
    genres = [g['genre_name'] for g in genres_data]

    # Construct songs list for context
    songs_context = []
    for s in songs:
        songs_context.append({
            "song_id": s['song_id'],
            "title": s['title'],
            "artist": artist_dict.get(s['artist_id'], "Unknown Artist"),
            "album": album_dict.get(s['album_id'], "Unknown Album"),
            "genre": s['genre'],
            "duration": s['duration']
        })

    return render_template("song_catalog.html", songs=songs_context, genres=genres)

@app.route('/songs/<int:song_id>')
def song_details_page(song_id):
    songs = read_songs()
    artists = read_artists()
    albums = read_albums()

    song = next((s for s in songs if s['song_id'] == song_id), None)
    if not song:
        abort(404)

    artist = next((a for a in artists if a['artist_id'] == song['artist_id']), None)
    album = next((al for al in albums if al['album_id'] == song['album_id']), None)

    if not artist:
        artist_info = {"artist_id": 0, "name": "Unknown Artist"}
    else:
        artist_info = {"artist_id": artist['artist_id'], "name": artist['name']}

    song_info = {
        "song_id": song['song_id'],
        "title": song['title'],
        "artist": artist['name'] if artist else "Unknown Artist",
        "album": album['title'] if album else "Unknown Album",
        "duration": song['duration']
    }

    return render_template("song_details.html", song=song_info, artist=artist_info)

@app.route('/playlists')
def playlists_page():
    playlists = read_playlists()

    # For each playlist get song_count
    playlists_context = []
    for p in playlists:
        playlists_context.append({
            "playlist_id": p['playlist_id'],
            "title": p['title'],
            "song_count": p['total_songs']
        })

    return render_template("playlists.html", playlists=playlists_context)

@app.route('/playlists/create', methods=['GET', 'POST'])
def create_playlist_page():
    if request.method == 'GET':
        # Render form
        return render_template("create_playlist.html")
    else:
        # Handle form submission
        title = request.form.get('playlist_name', '').strip()  # Fixed key to match frontend
        description = request.form.get('playlist_description', '').strip()  # Fixed key
        if not title:
            # Must have title, simple validation
            return render_template("create_playlist.html", error="Title is required")

        playlists = read_playlists()
        next_id = get_next_id(playlists, 'playlist_id')
        creation_date = datetime.today().strftime('%Y-%m-%d')

        new_playlist = {
            "playlist_id": next_id,
            "title": title,
            "description": description,
            "creation_date": creation_date,
            "total_songs": 0
        }

        playlists.append(new_playlist)
        # Save playlists
        write_playlists(playlists)

        return redirect(url_for('playlists_page'))

@app.route('/playlists/<int:playlist_id>')
def playlist_details_page(playlist_id):
    playlists = read_playlists()
    playlist = next((p for p in playlists if p['playlist_id'] == playlist_id), None)
    if not playlist:
        abort(404)

    playlist_songs = read_playlist_songs()
    songs = read_songs()
    artists = read_artists()

    # Get songs in this playlist
    song_ids = [ps['song_id'] for ps in playlist_songs if ps['playlist_id'] == playlist_id]

    # Construct songs_in_playlist context: song_id, title, artist, duration
    artist_dict = {a['artist_id']: a['name'] for a in artists}
    songs_dict = {s['song_id']: s for s in songs}

    songs_in_playlist = []
    for sid in song_ids:
        s = songs_dict.get(sid)
        if s:
            songs_in_playlist.append({
                "song_id": s['song_id'],
                "title": s['title'],
                "artist": artist_dict.get(s['artist_id'], "Unknown Artist"),
                "duration": s['duration']
            })

    return render_template("playlist_details.html", playlist=playlist, songs_in_playlist=songs_in_playlist)

@app.route('/playlists/<int:playlist_id>/delete', methods=['POST'])
def delete_playlist(playlist_id):
    playlists = read_playlists()
    playlist_songs = read_playlist_songs()

    playlists = [p for p in playlists if p['playlist_id'] != playlist_id]
    playlist_songs = [ps for ps in playlist_songs if ps['playlist_id'] != playlist_id]

    # Save updated data
    write_playlists(playlists)
    write_playlist_songs(playlist_songs)

    return redirect(url_for('playlists_page'))

@app.route('/playlists/<int:playlist_id>/remove_song/<int:song_id>', methods=['POST'])
def remove_song_from_playlist(playlist_id, song_id):
    playlist_songs = read_playlist_songs()
    playlists = read_playlists()

    # Remove song from playlist_songs for given playlist and song
    playlist_songs = [ps for ps in playlist_songs if not (ps['playlist_id'] == playlist_id and ps['song_id'] == song_id)]

    # Update total_songs count on playlist
    for p in playlists:
        if p['playlist_id'] == playlist_id:
            p['total_songs'] = sum(1 for ps in playlist_songs if ps['playlist_id'] == playlist_id)
            break

    write_playlist_songs(playlist_songs)
    write_playlists(playlists)

    return redirect(url_for('playlist_details_page', playlist_id=playlist_id))

@app.route('/songs/<int:song_id>/add_to_playlist', methods=['POST'])
def add_single_song_to_playlist(song_id):
    # Expecting playlist_id from form data
    playlist_id = request.form.get('playlist_id', type=int)
    if not playlist_id:
        abort(400, description="playlist_id is required")

    playlists = read_playlists()
    playlist = next((p for p in playlists if p['playlist_id'] == playlist_id), None)
    if not playlist:
        abort(404)

    songs = read_songs()
    song = next((s for s in songs if s['song_id'] == song_id), None)
    if not song:
        abort(404)

    playlist_songs = read_playlist_songs()
    # Avoid duplication
    existing_song_ids_in_playlist = set(ps['song_id'] for ps in playlist_songs if ps['playlist_id'] == playlist_id)
    if song_id not in existing_song_ids_in_playlist:
        next_ps_id = get_next_id(playlist_songs, 'playlist_song_id')
        now_str = datetime.today().strftime('%Y-%m-%d')
        playlist_songs.append({
            "playlist_song_id": next_ps_id,
            "playlist_id": playlist_id,
            "song_id": song_id,
            "added_date": now_str
        })
        # Update total_songs count on playlist
        for p in playlists:
            if p['playlist_id'] == playlist_id:
                p['total_songs'] += 1
                break

        write_playlist_songs(playlist_songs)
        write_playlists(playlists)

    return redirect(url_for('song_details_page', song_id=song_id))

@app.route('/albums')
def albums_page():
    albums = read_albums()
    artists = read_artists()

    artist_dict = {a['artist_id']: a['name'] for a in artists}

    albums_context = []
    for al in albums:
        albums_context.append({
            "album_id": al['album_id'],
            "title": al['title'],
            "artist": artist_dict.get(al['artist_id'], "Unknown Artist"),
            "year": al['release_year']
        })

    return render_template("albums.html", albums=albums_context)

@app.route('/albums/<int:album_id>')
def album_details_page(album_id):
    albums = read_albums()
    songs = read_songs()

    album = next((al for al in albums if al['album_id'] == album_id), None)
    if not album:
        abort(404)

    songs_in_album = []
    for s in songs:
        if s['album_id'] == album_id:
            songs_in_album.append({
                "song_id": s['song_id'],
                "title": s['title'],
                "duration": s['duration']
            })

    return render_template("album_details.html", album=album, songs_in_album=songs_in_album)

@app.route('/albums/<int:album_id>/add_to_playlist', methods=['POST'])
def add_album_songs_to_playlist(album_id):
    # As no playlist is specified in the route, let's assume a query param or form data with playlist_id
    playlist_id = request.form.get('playlist_id', type=int)
    if not playlist_id:
        abort(400, description="playlist_id required")

    playlists = read_playlists()
    playlist = next((p for p in playlists if p['playlist_id'] == playlist_id), None)
    if not playlist:
        abort(404)

    songs = read_songs()
    playlist_songs = read_playlist_songs()

    # Get all songs of the album
    album_songs = [s for s in songs if s['album_id'] == album_id]

    now_str = datetime.today().strftime('%Y-%m-%d')

    # Start from next playlist_song_id
    next_ps_id = get_next_id(playlist_songs, 'playlist_song_id')

    existing_song_ids_in_playlist = set(ps['song_id'] for ps in playlist_songs if ps['playlist_id'] == playlist_id)

    for s in album_songs:
        if s['song_id'] not in existing_song_ids_in_playlist:
            playlist_songs.append({
                "playlist_song_id": next_ps_id,
                "playlist_id": playlist_id,
                "song_id": s['song_id'],
                "added_date": now_str
            })
            next_ps_id += 1

    # Update total_songs count on playlist
    playlist['total_songs'] = sum(1 for ps in playlist_songs if ps['playlist_id'] == playlist_id)

    write_playlist_songs(playlist_songs)
    write_playlists(playlists)

    return redirect(url_for('album_details_page', album_id=album_id))

@app.route('/artists')
def artists_page():
    artists = read_artists()

    artists_context = []
    for a in artists:
        artists_context.append({
            "artist_id": a['artist_id'],
            "name": a['name'],
            "genre": a['genre']
        })

    return render_template("artists.html", artists=artists_context)

@app.route('/artists/<int:artist_id>')
def artist_profile_page(artist_id):
    artists = read_artists()
    songs = read_songs()
    albums = read_albums()

    artist = next((a for a in artists if a['artist_id']==artist_id), None)
    if not artist:
        abort(404)

    # Songs by artist
    artist_songs = []
    album_dict = {al['album_id']: al['title'] for al in albums}
    for s in songs:
        if s['artist_id'] == artist_id:
            artist_songs.append({
                "song_id": s['song_id'],
                "title": s['title'],
                "album": album_dict.get(s['album_id'], "Unknown Album"),
                "duration": s['duration']
            })

    artist_info = {
        "artist_id": artist['artist_id'],
        "name": artist['name'],
        "genre": artist['genre'],
        "country": artist['country'],
        "formation_year": artist['formation_year']
    }

    return render_template("artist_profile.html", artist=artist_info, artist_songs=artist_songs)

@app.route('/genres')
def genres_page():
    genres = read_genres()
    songs = read_songs()
    artists = read_artists()

    # We will pick the first genre for context lists or default empty
    selected_genre = None
    if genres:
        selected_genre = genres[0]['genre_name']

    # Songs and artists for the selected genre
    genre_songs = []
    genre_artists_ids = set()

    for s in songs:
        if s['genre'] == selected_genre:
            genre_songs.append({
                "song_id": s['song_id'],
                "title": s['title'],
                "artist": next((a['name'] for a in artists if a['artist_id'] == s['artist_id']), "Unknown Artist")
            })
            genre_artists_ids.add(s['artist_id'])

    genre_artists = []
    for a in artists:
        if a['artist_id'] in genre_artists_ids:
            genre_artists.append({"artist_id": a['artist_id'], "name": a['name']})

    return render_template("genres.html", genres=genres, genre_songs=genre_songs, genre_artists=genre_artists)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
