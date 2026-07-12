from flask import Flask, render_template, redirect, url_for, request
from datetime import datetime

app = Flask(__name__)

DATA_PATH = "data/"

# Utility functions to load data from files

def load_songs():
    songs = []
    with open(DATA_PATH + "songs.txt", "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) == 8:
                try:
                    song = {
                        "song_id": int(parts[0]),
                        "title": parts[1],
                        "artist_id": int(parts[2]),
                        "album_id": int(parts[3]),
                        "genre": parts[4],
                        "duration": int(parts[5]),
                        "release_date": parts[6],
                        "play_count": int(parts[7]),
                    }
                    songs.append(song)
                except ValueError:
                    # Skip malformed lines
                    continue
    return songs


def load_artists():
    artists = []
    with open(DATA_PATH + "artists.txt", "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) == 5:
                try:
                    artist = {
                        "artist_id": int(parts[0]),
                        "name": parts[1],
                        "genre": parts[2],
                        "country": parts[3],
                        "formation_year": int(parts[4]),
                    }
                    artists.append(artist)
                except ValueError:
                    continue
    return artists


def load_albums():
    albums = []
    with open(DATA_PATH + "albums.txt", "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) == 6:
                try:
                    album = {
                        "album_id": int(parts[0]),
                        "title": parts[1],
                        "artist_id": int(parts[2]),
                        "release_year": int(parts[3]),
                        "total_songs": int(parts[4]),
                        "genre": parts[5],
                    }
                    albums.append(album)
                except ValueError:
                    continue
    return albums


def load_genres():
    genres = []
    with open(DATA_PATH + "genres.txt", "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) == 3:
                try:
                    genre = {
                        "genre_id": int(parts[0]),
                        "genre_name": parts[1],
                        "description": parts[2],
                    }
                    genres.append(genre)
                except ValueError:
                    continue
    return genres


def load_playlists():
    playlists = []
    with open(DATA_PATH + "playlists.txt", "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) == 5:
                try:
                    playlist = {
                        "playlist_id": int(parts[0]),
                        "title": parts[1],
                        "description": parts[2],
                        "creation_date": parts[3],
                        "total_songs": int(parts[4]),
                    }
                    playlists.append(playlist)
                except ValueError:
                    continue
    return playlists


def load_playlist_songs():
    playlist_songs = []
    with open(DATA_PATH + "playlist_songs.txt", "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) == 4:
                try:
                    pls = {
                        "playlist_song_id": int(parts[0]),
                        "playlist_id": int(parts[1]),
                        "song_id": int(parts[2]),
                        "added_date": parts[3],
                    }
                    playlist_songs.append(pls)
                except ValueError:
                    continue
    return playlist_songs

# Utility functions to save data

def save_playlists(playlists):
    lines = []
    for p in playlists:
        line = f"{p['playlist_id']}|{p['title']}|{p['description']}|{p['creation_date']}|{p['total_songs']}"
        lines.append(line)
    with open(DATA_PATH + "playlists.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n" if lines else "")


def save_playlist_songs(playlist_songs):
    lines = []
    for pls in playlist_songs:
        line = f"{pls['playlist_song_id']}|{pls['playlist_id']}|{pls['song_id']}|{pls['added_date']}"
        lines.append(line)
    with open(DATA_PATH + "playlist_songs.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n" if lines else "")


# Helper functions for lookups

def get_artist_by_id(artist_id, artists=None):
    if artists is None:
        artists = load_artists()
    for artist in artists:
        if artist['artist_id'] == artist_id:
            return artist
    return None


def get_album_by_id(album_id, albums=None):
    if albums is None:
        albums = load_albums()
    for album in albums:
        if album['album_id'] == album_id:
            return album
    return None


def get_playlist_by_id(playlist_id, playlists=None):
    if playlists is None:
        playlists = load_playlists()
    for playlist in playlists:
        if playlist['playlist_id'] == playlist_id:
            return playlist
    return None


def get_song_by_id(song_id, songs=None):
    if songs is None:
        songs = load_songs()
    for song in songs:
        if song['song_id'] == song_id:
            return song
    return None


# Routes

@app.route('/')
def redirect_to_dashboard():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    # Featured songs: Let's pick top 5 played songs
    songs = load_songs()
    artists = load_artists()

    # sort songs by play_count descending
    featured_songs_raw = sorted(songs, key=lambda s: s['play_count'], reverse=True)[:5]

    featured_songs = []
    for s in featured_songs_raw:
        artist = get_artist_by_id(s['artist_id'], artists)
        featured_songs.append({
            "song_id": s['song_id'],
            "title": s['title'],
            "artist_name": artist['name'] if artist else "Unknown",
            "duration": s['duration'],
            "cover_art_url": "/static/images/covers/{}-{}.jpg".format(s['song_id'], s['album_id'])  # example cover art path
        })

    # Trending artists: top 5 artists by total play count of all their songs
    artist_play_counts = {}
    for s in songs:
        artist_play_counts[s['artist_id']] = artist_play_counts.get(s['artist_id'], 0) + s['play_count']

    trending_artist_ids = sorted(artist_play_counts, key=lambda aid: artist_play_counts[aid], reverse=True)[:5]
    trending_artists = []
    for aid in trending_artist_ids:
        artist = get_artist_by_id(aid, artists)
        if artist:
            trending_artists.append({
                "artist_id": artist['artist_id'],
                "name": artist['name'],
                "genre": artist['genre'],
                "photo_url": "/static/images/artists/{}.jpg".format(artist['artist_id'])
            })

    return render_template('dashboard.html', featured_songs=featured_songs, trending_artists=trending_artists)


@app.route('/songs', methods=['GET', 'POST'])
def song_catalog():
    songs = load_songs()
    artists = load_artists()
    albums = load_albums()

    search_query = ""
    selected_genre = ""

    if request.method == "POST":
        search_query = request.form.get('search_query', '').strip()
        selected_genre = request.form.get('selected_genre', '').strip()

    # Filter and search
    filtered_songs = songs

    if search_query:
        filtered_songs = [s for s in filtered_songs if search_query.lower() in s['title'].lower()]

    if selected_genre:
        filtered_songs = [s for s in filtered_songs if s['genre'].lower() == selected_genre.lower()]

    # Build result song list with artist_name and album_name
    results = []
    for s in filtered_songs:
        artist = get_artist_by_id(s['artist_id'], artists)
        album = get_album_by_id(s['album_id'], albums)
        results.append({
            "song_id": s['song_id'],
            "title": s['title'],
            "artist_name": artist['name'] if artist else "Unknown",
            "album_name": album['title'] if album else "Unknown",
            "genre": s['genre'],
            "duration": s['duration'],
        })

    return render_template('song_catalog.html', songs=results, search_query=search_query, selected_genre=selected_genre)


@app.route('/songs/<int:song_id>')
def song_details(song_id):
    songs = load_songs()
    artists = load_artists()
    albums = load_albums()

    song = get_song_by_id(song_id, songs)
    if not song:
        return "Song not found", 404

    artist = get_artist_by_id(song['artist_id'], artists)
    album = get_album_by_id(song['album_id'], albums)

    song_context = {
        "song_id": song['song_id'],
        "title": song['title'],
        "artist_id": artist['artist_id'] if artist else None,
        "artist_name": artist['name'] if artist else "Unknown",
        "album_id": album['album_id'] if album else None,
        "album_name": album['title'] if album else "Unknown",
        "genre": song['genre'],
        "duration": song['duration'],
        "release_date": song['release_date']
    }

    return render_template('song_details.html', song=song_context)


@app.route('/playlists')
def playlists():
    playlists = load_playlists()

    # Add total_songs from data itself
    playlist_list = []
    for p in playlists:
        playlist_list.append({
            "playlist_id": p['playlist_id'],
            "title": p['title'],
            "description": p['description'],
            "total_songs": p['total_songs'],
        })

    return render_template('playlists.html', playlists=playlist_list)


@app.route('/playlists/<int:playlist_id>')
def playlist_details(playlist_id):
    playlists = load_playlists()
    playlist_songs = load_playlist_songs()
    songs = load_songs()
    artists = load_artists()

    playlist = get_playlist_by_id(playlist_id, playlists)
    if not playlist:
        return "Playlist not found", 404

    # Find songs in this playlist
    playlist_song_entries = [pls for pls in playlist_songs if pls['playlist_id'] == playlist_id]

    song_list = []
    for pls in playlist_song_entries:
        song = get_song_by_id(pls['song_id'], songs)
        if song:
            artist = get_artist_by_id(song['artist_id'], artists)
            song_list.append({
                "song_id": song['song_id'],
                "title": song['title'],
                "artist_name": artist['name'] if artist else "Unknown",
                "duration": song['duration'],
            })

    return render_template('playlist_details.html', playlist=playlist, songs=song_list)


@app.route('/playlists/create', methods=['GET', 'POST'])
def create_playlist():
    if request.method == 'GET':
        return render_template('create_playlist.html')

    # POST
    title = request.form.get('playlist_name_input', '').strip()
    description = request.form.get('playlist_description_input', '').strip()

    errors = {}

    if not title:
        errors['title'] = "Title is required."
    if not description:
        errors['description'] = "Description is required."

    if errors:
        # Return form with errors and previous inputs
        return render_template('create_playlist.html', errors=errors, form_data={'title': title, 'description': description})

    playlists = load_playlists()

    # Generate new playlist_id
    max_id = max([p['playlist_id'] for p in playlists], default=0)
    new_playlist_id = max_id + 1

    new_playlist = {
        "playlist_id": new_playlist_id,
        "title": title,
        "description": description,
        "creation_date": datetime.now().strftime("%Y-%m-%d"),
        "total_songs": 0
    }

    playlists.append(new_playlist)
    save_playlists(playlists)

    return redirect(url_for('playlists'))


@app.route('/albums')
def album_browse():
    albums = load_albums()
    artists = load_artists()

    search_query = request.args.get('search_query', '').strip()
    sort_option = request.args.get('sort_option', '').strip()

    filtered_albums = albums

    if search_query:
        filtered_albums = [a for a in filtered_albums if search_query.lower() in a['title'].lower()]

    # Map artist names for filtered albums
    for a in filtered_albums:
        artist = get_artist_by_id(a['artist_id'], artists)
        a['artist_name'] = artist['name'] if artist else "Unknown"

    if sort_option == "title":
        filtered_albums.sort(key=lambda a: a['title'])
    elif sort_option == "artist":
        filtered_albums.sort(key=lambda a: a['artist_name'])
    elif sort_option == "year":
        filtered_albums.sort(key=lambda a: a['release_year'])

    return render_template('albums.html', albums=filtered_albums, search_query=search_query, sort_option=sort_option)


@app.route('/albums/<int:album_id>')
def album_details(album_id):
    albums = load_albums()
    artists = load_artists()
    songs = load_songs()

    album = get_album_by_id(album_id, albums)
    if not album:
        return "Album not found", 404

    artist = get_artist_by_id(album['artist_id'], artists)

    album_songs = [s for s in songs if s['album_id'] == album_id]

    song_list = []
    for s in album_songs:
        song_list.append({
            "song_id": s['song_id'],
            "title": s['title'],
            "duration": s['duration'],
        })

    album_context = {
        "album_id": album['album_id'],
        "title": album['title'],
        "artist_name": artist['name'] if artist else "Unknown",
        "release_year": album['release_year'],
    }

    return render_template('album_details.html', album=album_context, songs=song_list)


@app.route('/artists')
def artist_profiles():
    artists = load_artists()

    search_query = request.args.get('search_query', '').strip()
    sort_option = request.args.get('sort_option', '').strip()

    filtered_artists = artists

    if search_query:
        filtered_artists = [a for a in filtered_artists if search_query.lower() in a['name'].lower()]

    if sort_option == "name":
        filtered_artists.sort(key=lambda a: a['name'])
    elif sort_option == "genre":
        filtered_artists.sort(key=lambda a: a['genre'])

    return render_template('artists.html', artists=filtered_artists, search_query=search_query, sort_option=sort_option)


@app.route('/artists/<int:artist_id>')
def artist_profile(artist_id):
    artists = load_artists()
    songs = load_songs()
    albums = load_albums()

    artist = get_artist_by_id(artist_id, artists)
    if not artist:
        return "Artist not found", 404

    artist_songs = [s for s in songs if s['artist_id'] == artist_id]

    song_list = []
    for s in artist_songs:
        album = get_album_by_id(s['album_id'], albums)
        song_list.append({
            "song_id": s['song_id'],
            "title": s['title'],
            "album_name": album['title'] if album else "Unknown",
            "duration": s['duration'],
        })

    return render_template('artist_profile.html', artist=artist, songs=song_list)


@app.route('/genres', methods=['GET', 'POST'])
def genre_exploration():
    genres = load_genres()
    selected_genre = ""
    genre_songs = []
    genre_artists = []

    if request.method == 'POST':
        selected_genre = request.form.get('selected_genre', '').strip()

        songs = load_songs()
        artists = load_artists()

        genre_songs = [
            {
                "song_id": s['song_id'],
                "title": s['title'],
                "artist_name": get_artist_by_id(s['artist_id'], artists)['name'] if get_artist_by_id(s['artist_id'], artists) else "Unknown",
                "duration": s['duration'],
            }
            for s in songs if s['genre'].lower() == selected_genre.lower()
        ]

        genre_artists = [
            a for a in artists if a['genre'].lower() == selected_genre.lower()
        ]

    return render_template('genres.html', genres=genres, selected_genre=selected_genre, genre_songs=genre_songs, genre_artists=genre_artists)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
