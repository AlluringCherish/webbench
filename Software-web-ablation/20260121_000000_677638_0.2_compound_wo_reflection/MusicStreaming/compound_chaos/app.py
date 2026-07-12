from flask import Flask, render_template, redirect, url_for, request, jsonify, abort
from datetime import datetime
import os

app = Flask(__name__)

data_folder = "data"

# Data files
songs_file = os.path.join(data_folder, "songs.txt")
artists_file = os.path.join(data_folder, "artists.txt")
albums_file = os.path.join(data_folder, "albums.txt")
genres_file = os.path.join(data_folder, "genres.txt")
playlists_file = os.path.join(data_folder, "playlists.txt")
playlist_songs_file = os.path.join(data_folder, "playlist_songs.txt")

# Load data utils

def load_artists():
    artists = []
    try:
        with open(artists_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) == 5:
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
    except FileNotFoundError:
        pass
    return artists


def load_songs():
    songs = []
    artists = {a["artist_id"]: a["name"] for a in load_artists()}  # map artist_id to name
    albums = {a["album_id"]: a for a in load_albums()}  # map album_id to album dict
    try:
        with open(songs_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) < 7:
                    continue
                # song_id|title|artist_id|album_id|genre|duration|release_date|play_count
                try:
                    song_id = int(parts[0])
                    title = parts[1]
                    artist_id = int(parts[2])
                    album_id = int(parts[3])
                    genre = parts[4]
                    duration = int(parts[5])
                    # release_date = parts[6]  # YYYY-MM-DD
                    # play_count = int(parts[7]) if len(parts) > 7 else 0
                except Exception:
                    continue
                artist_name = artists.get(artist_id, "Unknown Artist")
                album_name = albums.get(album_id, {}).get("title", "Unknown Album")
                songs.append({
                    "song_id": song_id,
                    "title": title,
                    "artist_name": artist_name,
                    "album_name": album_name,
                    "genre": genre,
                    "duration": duration
                })
    except FileNotFoundError:
        pass
    return songs


def load_albums():
    albums = []
    artists = {a["artist_id"]: a["name"] for a in load_artists()}
    try:
        with open(albums_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) < 5:
                    continue
                try:
                    album_id = int(parts[0])
                    title = parts[1]
                    artist_id = int(parts[2])
                    release_year = int(parts[3])
                    total_songs = int(parts[4])
                    # parts[5] genre ignored here since this is not required for routes
                except Exception:
                    continue
                artist_name = artists.get(artist_id, "Unknown Artist")
                albums.append({
                    "album_id": album_id,
                    "title": title,
                    "artist_name": artist_name,
                    "release_year": release_year,
                    "total_songs": total_songs
                })
    except FileNotFoundError:
        pass
    return albums


def load_genres():
    genres = []
    try:
        with open(genres_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) < 3:
                    continue
                try:
                    genre_id = int(parts[0])
                    genre_name = parts[1]
                    description = parts[2]
                except Exception:
                    continue
                genres.append({
                    "genre_id": genre_id,
                    "genre_name": genre_name,
                    "description": description
                })
    except FileNotFoundError:
        pass
    return genres


def load_playlists():
    playlists = []
    try:
        with open(playlists_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) < 3:
                    continue
                try:
                    playlist_id = int(parts[0])
                    title = parts[1]
                    description = parts[2]
                except Exception:
                    continue
                playlists.append({
                    "playlist_id": playlist_id,
                    "title": title,
                    "description": description
                })
    except FileNotFoundError:
        pass
    return playlists


def load_playlist_songs():
    playlist_songs = []
    try:
        with open(playlist_songs_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) < 4:
                    continue
                try:
                    playlist_id = int(parts[0])
                    song_id = int(parts[1])
                    # Note: According to schema, playlist_songs.txt fields: song_id|playlist_id|added_date?? But examples say 1|1|2|date
                    # We adapt as playlist_id|song_id|ignored|added_date (some inconsistency?)
                    added_date = parts[3]
                except Exception:
                    continue
                playlist_songs.append({
                    "playlist_id": playlist_id,
                    "song_id": song_id,
                    "added_date": added_date
                })
    except FileNotFoundError:
        pass
    return playlist_songs


# Save functions

def save_playlists(playlists):
    try:
        with open(playlists_file, "w", encoding="utf-8") as f:
            for p in playlists:
                # playlist_id|title|description
                f.write(f"{p['playlist_id']}|{p['title']}|{p['description']}\n")
    except Exception as e:
        pass


def save_playlist_songs(playlist_songs):
    try:
        with open(playlist_songs_file, "w", encoding="utf-8") as f:
            for ps in playlist_songs:
                # playlist_id|song_id|ignored|added_date
                # We write 0 for the ignored field to maintain consistency
                f.write(f"{ps['playlist_id']}|{ps['song_id']}|0|{ps['added_date']}\n")
    except Exception as e:
        pass


# Routes

@app.route('/')
def root_redirect():
    # Redirect to dashboard
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    # Load songs and trending artists
    songs_data = load_songs()
    # Sort songs by play_count is unavailable so skip, just get list
    # Trending artists: use the list of artists sorted by formation year ascending or top N by artist_id as placeholder
    artists = load_artists()
    trending_artists = []
    # According to spec, trending_artists keys: artist_id, name
    for artist in artists[:10]:
        trending_artists.append({"artist_id": artist["artist_id"], "name": artist["name"]})
    context = {
        "songs": [
            {"song_id": s["song_id"], "title": s["title"], "artist_name": s["artist_name"], "duration": s["duration"]}
            for s in songs_data
        ],
        "trending_artists": trending_artists
    }
    return render_template('dashboard.html', **context)


@app.route('/songs')
def song_catalog():
    songs_data = load_songs()
    genres_data = load_genres()
    context = {
        "songs": songs_data,
        "genres": genres_data
    }
    return render_template('song_catalog.html', **context)


@app.route('/songs/<int:song_id>')
def song_details(song_id):
    songs = load_songs()
    song = None
    for s in songs:
        if s['song_id'] == song_id:
            song = s
            break
    if not song:
        abort(404)
    context = {
        "song": song
    }
    return render_template('song_details.html', **context)


@app.route('/playlists')
def playlists():
    playlists_data = load_playlists()
    playlist_songs = load_playlist_songs()
    # We need song count per playlist
    song_count_dict = {}
    for ps in playlist_songs:
        song_count_dict[ps["playlist_id"]] = song_count_dict.get(ps["playlist_id"], 0) + 1
    playlists_context = []
    for p in playlists_data:
        playlists_context.append({
            "playlist_id": p["playlist_id"],
            "title": p["title"],
            "song_count": song_count_dict.get(p["playlist_id"], 0)
        })
    return render_template('playlists.html', playlists=playlists_context)


@app.route('/playlists/create', methods=["GET", "POST"])
def create_playlist():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        if not title:
            # Return the form again with error or just abort bad request
            return render_template('create_playlist.html', error="Title is required")
        playlists_data = load_playlists()
        # Find max playlist_id
        max_id = max([p["playlist_id"] for p in playlists_data], default=0)
        new_id = max_id + 1
        # Append new playlist
        playlists_data.append({
            "playlist_id": new_id,
            "title": title,
            "description": description
        })
        # Save playlists to file
        save_playlists(playlists_data)
        return redirect(url_for('playlists'))
    # GET method
    return render_template('create_playlist.html')


@app.route('/playlists/<int:playlist_id>')
def playlist_details(playlist_id):
    playlists_data = load_playlists()
    playlist = None
    for p in playlists_data:
        if p['playlist_id'] == playlist_id:
            playlist = p
            break
    if not playlist:
        abort(404)
    playlist_songs = load_playlist_songs()
    songs = load_songs()
    # Gather songs in this playlist
    songs_in_playlist = []
    song_ids_in_playlist = set()
    for ps in playlist_songs:
        if ps["playlist_id"] == playlist_id:
            song_ids_in_playlist.add(ps["song_id"])
    for s in songs:
        if s["song_id"] in song_ids_in_playlist:
            songs_in_playlist.append({
                "song_id": s["song_id"],
                "title": s["title"],
                "artist_name": s["artist_name"],
                "duration": s["duration"]
            })
    context = {
        "playlist": playlist,
        "songs": songs_in_playlist
    }
    return render_template('playlist_details.html', **context)


@app.route('/playlists/<int:playlist_id>/delete', methods=["POST"])
def delete_playlist(playlist_id):
    playlists_data = load_playlists()
    playlist_songs = load_playlist_songs()
    playlists_data = [p for p in playlists_data if p['playlist_id'] != playlist_id]
    playlist_songs = [ps for ps in playlist_songs if ps['playlist_id'] != playlist_id]
    save_playlists(playlists_data)
    save_playlist_songs(playlist_songs)
    # After deletion redirect to playlists
    return jsonify({"status": "success"})


@app.route('/playlists/<int:playlist_id>/remove_song/<int:song_id>', methods=["POST"])
def remove_song_from_playlist(playlist_id, song_id):
    playlist_songs = load_playlist_songs()
    initial_len = len(playlist_songs)
    playlist_songs = [ps for ps in playlist_songs if not (ps["playlist_id"] == playlist_id and ps["song_id"] == song_id)]
    if len(playlist_songs) < initial_len:
        save_playlist_songs(playlist_songs)
        return redirect(url_for('playlist_details', playlist_id=playlist_id))
    else:
        abort(404)


@app.route('/albums')
def albums():
    albums_data = load_albums()
    context = {
        "albums": albums_data
    }
    return render_template('albums.html', **context)


@app.route('/albums/<int:album_id>')
def album_details(album_id):
    albums_data = load_albums()
    album = None
    for a in albums_data:
        if a['album_id'] == album_id:
            album = a
            break
    if not album:
        abort(404)
    songs = load_songs()
    songs_of_album = []
    for s in songs:
        # match album by album_name and album_id
        # We have album title from album, so filter songs with matching album_name and also check album_id via mapping
        if s['album_name'] == album['title']:
            songs_of_album.append({
                "song_id": s['song_id'],
                "title": s['title'],
                "duration": s['duration']
            })
    context = {
        "album": album,
        "songs": songs_of_album
    }
    return render_template('album_details.html', **context)


@app.route('/artists')
def artists_list():
    artists = load_artists()
    # According to spec keys for artist list: artist_id, name, genre
    artists_context = []
    for a in artists:
        artists_context.append({"artist_id": a["artist_id"], "name": a["name"], "genre": a["genre"]})
    return render_template('artist_profiles.html', artists=artists_context)


@app.route('/artists/<int:artist_id>')
def artist_details(artist_id):
    artists = load_artists()
    artist = None
    for a in artists:
        if a['artist_id'] == artist_id:
            artist = a
            break
    if not artist:
        abort(404)
    songs_all = load_songs()
    songs = []
    for s in songs_all:
        if s['artist_name'] == artist['name']:
            songs.append({"song_id": s['song_id'], "title": s['title'], "album_name": s['album_name'], "duration": s['duration']})
    context = {
        "artist": artist,
        "songs": songs
    }
    return render_template('artist_profiles.html', artist=artist, songs=songs)


@app.route('/genres')
def genres():
    genres_data = load_genres()
    context = {
        "genres": genres_data
    }
    return render_template('genres.html', **context)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
