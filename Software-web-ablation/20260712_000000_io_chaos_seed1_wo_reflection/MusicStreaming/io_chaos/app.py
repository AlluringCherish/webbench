from flask import Flask, render_template, redirect, url_for, request, abort
from datetime import datetime
import os

app = Flask(__name__)

# Paths for data files
DATA_DIR = "data"
SONGS_FILE = os.path.join(DATA_DIR, "songs.txt")
ARTISTS_FILE = os.path.join(DATA_DIR, "artists.txt")
ALBUMS_FILE = os.path.join(DATA_DIR, "albums.txt")
GENRES_FILE = os.path.join(DATA_DIR, "genres.txt")
PLAYLISTS_FILE = os.path.join(DATA_DIR, "playlists.txt")
PLAYLIST_SONGS_FILE = os.path.join(DATA_DIR, "playlist_songs.txt")

# Helper functions to load data

def load_songs():
    songs = []
    try:
        with open(SONGS_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 8:
                    continue
                song = {
                    "song_id": int(parts[0]),
                    "title": parts[1],
                    "artist_id": int(parts[2]),
                    "album_id": int(parts[3]),
                    "genre": parts[4],
                    "duration": int(parts[5]),
                    "release_date": parts[6],
                    "play_count": int(parts[7])
                }
                songs.append(song)
    except FileNotFoundError:
        pass
    return songs


def load_artists():
    artists = []
    try:
        with open(ARTISTS_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 5:
                    continue
                artist = {
                    "artist_id": int(parts[0]),
                    "name": parts[1],
                    "genre": parts[2],
                    "country": parts[3],
                    "formation_year": int(parts[4])
                }
                artists.append(artist)
    except FileNotFoundError:
        pass
    return artists


def load_albums():
    albums = []
    try:
        with open(ALBUMS_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 6:
                    continue
                album = {
                    "album_id": int(parts[0]),
                    "title": parts[1],
                    "artist_id": int(parts[2]),
                    "release_year": int(parts[3]),
                    "total_songs": int(parts[4]),
                    "genre": parts[5]
                }
                albums.append(album)
    except FileNotFoundError:
        pass
    return albums


def load_genres():
    genres = []
    try:
        with open(GENRES_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 3:
                    continue
                genre = {
                    "genre_id": int(parts[0]),
                    "genre_name": parts[1],
                    "description": parts[2]
                }
                genres.append(genre)
    except FileNotFoundError:
        pass
    return genres


def load_playlists():
    playlists = []
    try:
        with open(PLAYLISTS_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 5:
                    continue
                playlist = {
                    "playlist_id": int(parts[0]),
                    "title": parts[1],
                    "description": parts[2],
                    "creation_date": parts[3],
                    "total_songs": int(parts[4])
                }
                playlists.append(playlist)
    except FileNotFoundError:
        pass
    return playlists


def load_playlist_songs():
    playlist_songs = []
    try:
        with open(PLAYLIST_SONGS_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 4:
                    continue
                pls = {
                    "playlist_song_id": int(parts[0]),
                    "playlist_id": int(parts[1]),
                    "song_id": int(parts[2]),
                    "added_date": parts[3]
                }
                playlist_songs.append(pls)
    except FileNotFoundError:
        pass
    return playlist_songs


# Save functions for playlists and playlist_songs

def save_playlists(playlists):
    lines = []
    for p in playlists:
        line = f"{p['playlist_id']}|{p['title']}|{p['description']}|{p['creation_date']}|{p['total_songs']}"
        lines.append(line)
    with open(PLAYLISTS_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + ("\n" if lines else ""))


def save_playlist_songs(playlist_songs):
    lines = []
    for pls in playlist_songs:
        line = f"{pls['playlist_song_id']}|{pls['playlist_id']}|{pls['song_id']}|{pls['added_date']}"
        lines.append(line)
    with open(PLAYLIST_SONGS_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + ("\n" if lines else ""))


# Helper to generate next unique id

def next_id(items, key):
    if not items:
        return 1
    return max(item[key] for item in items) + 1


# -------- ROUTES -------- #

@app.route('/')
def root_redirect():
    # Redirect to dashboard page
    return redirect(url_for('dashboard_page'))


@app.route('/dashboard')
def dashboard_page():
    # Featured songs: choice - for simplicity pick top 10 songs by play_count descending
    songs = load_songs()
    artists = {a['artist_id']: a['name'] for a in load_artists()}

    # Sort songs by play_count desc
    songs_sorted = sorted(songs, key=lambda s: s['play_count'], reverse=True)
    featured_songs = []
    for song in songs_sorted[:10]:
        featured_songs.append({
            'song_id': song['song_id'],
            'title': song['title'],
            'artist_name': artists.get(song['artist_id'], "Unknown"),
            'duration': song['duration']
        })

    # Trending artists: top 5 by sum of play_counts of their songs
    artist_play_counts = {}
    for song in songs:
        artist_play_counts[song['artist_id']] = artist_play_counts.get(song['artist_id'], 0) + song['play_count']
    trending_sorted = sorted(artist_play_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    artists_data = load_artists()
    trending_artists = []
    artist_dict = {a['artist_id']: a for a in artists_data}
    for artist_id, _ in trending_sorted:
        a = artist_dict.get(artist_id)
        if a:
            trending_artists.append({'artist_id': a['artist_id'], 'name': a['name']})

    return render_template('dashboard.html', featured_songs=featured_songs, trending_artists=trending_artists)


@app.route('/songs', methods=['GET', 'POST'])
def song_catalog_page():
    songs = load_songs()
    artists = {a['artist_id']: a['name'] for a in load_artists()}
    albums = {al['album_id']: al['title'] for al in load_albums()}

    filter_genre = None
    search_query = None

    if request.method == 'POST':
        # As per spec, adding songs to playlists is triggered by buttons on this page
        # But spec doesn't mention details about the playlist selection or adding mechanics
        # So no actual adding in this POST handler
        # We keep it here for expandability
        pass

    # Query args for filtering and searching
    filter_genre = request.args.get('genre')
    if filter_genre == '':
        filter_genre = None
    search_query = request.args.get('search')
    if search_query == '':
        search_query = None

    filtered_songs = []
    for song in songs:
        if filter_genre and song['genre'] != filter_genre:
            continue
        if search_query and search_query.lower() not in song['title'].lower():
            continue
        filtered_songs.append({
            'song_id': song['song_id'],
            'title': song['title'],
            'artist_name': artists.get(song['artist_id'], "Unknown"),
            'album_name': albums.get(song['album_id'], "Unknown"),
            'genre': song['genre'],
            'duration': song['duration']
        })

    return render_template('song_catalog.html', songs=filtered_songs, filter_genre=filter_genre, search_query=search_query)


@app.route('/songs/<int:song_id>')
def song_details_page(song_id):
    songs = load_songs()
    artists = {a['artist_id']: a for a in load_artists()}
    albums = {al['album_id']: al for al in load_albums()}

    song = next((s for s in songs if s['song_id'] == song_id), None)
    if not song:
        abort(404)

    artist = artists.get(song['artist_id'])
    album = albums.get(song['album_id'])

    song_dict = {
        'song_id': song['song_id'],
        'title': song['title'],
        'artist_id': artist['artist_id'] if artist else None,
        'artist_name': artist['name'] if artist else "Unknown",
        'album_id': album['album_id'] if album else None,
        'album_name': album['title'] if album else "Unknown",
        'genre': song['genre'],
        'duration': song['duration']
    }

    return render_template('song_details.html', song=song_dict)


@app.route('/playlists')
def playlists_page():
    playlists = load_playlists()
    playlists_context = []
    for p in playlists:
        playlists_context.append({
            'playlist_id': p['playlist_id'],
            'title': p['title'],
            'song_count': p['total_songs']
        })
    return render_template('playlists.html', playlists=playlists_context)


@app.route('/playlists/create', methods=['GET', 'POST'])
def create_playlist_page():
    if request.method == 'POST':
        title = request.form.get('playlist_name')
        description = request.form.get('playlist_description')
        if not title:
            # Re-render create_playlist.html with some error (not specified in spec, so just ignore)
            return render_template('create_playlist.html')

        playlists = load_playlists()
        new_id = next_id(playlists, 'playlist_id')
        creation_date = datetime.now().strftime('%Y-%m-%d')
        new_playlist = {
            'playlist_id': new_id,
            'title': title,
            'description': description if description else "",
            'creation_date': creation_date,
            'total_songs': 0
        }
        playlists.append(new_playlist)
        save_playlists(playlists)

        return redirect(url_for('playlists_page'))

    # GET
    return render_template('create_playlist.html')


@app.route('/playlists/<int:playlist_id>', methods=['GET', 'POST'])
def playlist_details_page(playlist_id):
    playlists = load_playlists()
    playlist = next((p for p in playlists if p['playlist_id'] == playlist_id), None)
    if not playlist:
        abort(404)

    songs = load_songs()
    artists = {a['artist_id']: a['name'] for a in load_artists()}
    playlist_songs = load_playlist_songs()

    # Handle POST for remove song and delete playlist
    if request.method == 'POST':
        # Check if removing a song
        remove_song_id = request.form.get('remove_song_id')
        if remove_song_id:
            try:
                remove_song_id = int(remove_song_id)
            except:
                remove_song_id = None
            if remove_song_id is not None:
                # Filter out this song from playlist_songs
                original_count = len(playlist_songs)
                playlist_songs = [ps for ps in playlist_songs if not (ps['playlist_id'] == playlist_id and ps['song_id'] == remove_song_id)]
                if len(playlist_songs) < original_count:
                    # Update playlist total songs
                    playlist['total_songs'] = max(playlist['total_songs'] - 1, 0)
                    save_playlist_songs(playlist_songs)
                    save_playlists(playlists)
                    return redirect(url_for('playlist_details_page', playlist_id=playlist_id))

        # Check if deleting playlist
        if 'delete_playlist' in request.form:
            # Remove playlist
            playlists = [p for p in playlists if p['playlist_id'] != playlist_id]
            # Remove all playlist songs entries for this playlist
            playlist_songs = [ps for ps in playlist_songs if ps['playlist_id'] != playlist_id]
            save_playlists(playlists)
            save_playlist_songs(playlist_songs)
            return redirect(url_for('playlists_page'))

    # For GET or no changes, prepare data for template

    # Songs in this playlist
    songs_in_playlist = []
    for pls in playlist_songs:
        if pls['playlist_id'] == playlist_id:
            song = next((s for s in songs if s['song_id'] == pls['song_id']), None)
            if song:
                songs_in_playlist.append({
                    'song_id': song['song_id'],
                    'title': song['title'],
                    'artist_name': artists.get(song['artist_id'], "Unknown"),
                    'duration': song['duration']
                })

    return render_template('playlist_details.html', playlist=playlist, songs_in_playlist=songs_in_playlist)


@app.route('/albums')
def albums_page():
    albums = load_albums()
    artists = {a['artist_id']: a['name'] for a in load_artists()}

    albums_context = []
    for album in albums:
        albums_context.append({
            'album_id': album['album_id'],
            'title': album['title'],
            'artist_name': artists.get(album['artist_id'], "Unknown"),
            'year': album['release_year']
        })

    return render_template('albums.html', albums=albums_context)


@app.route('/albums/<int:album_id>')
def album_details_page(album_id):
    albums = load_albums()
    album = next((a for a in albums if a['album_id'] == album_id), None)
    if not album:
        abort(404)

    artists = {a['artist_id']: a['name'] for a in load_artists()}
    songs = load_songs()

    album_songs = [s for s in songs if s['album_id'] == album_id]
    songs_in_album = []
    for s in album_songs:
        songs_in_album.append({
            'song_id': s['song_id'],
            'title': s['title'],
            'duration': s['duration']
        })

    album_context = {
        'album_id': album['album_id'],
        'title': album['title'],
        'artist_name': artists.get(album['artist_id'], "Unknown"),
        'year': album['release_year']
    }

    return render_template('album_details.html', album=album_context, songs_in_album=songs_in_album)


@app.route('/artists')
def artists_page():
    artists = load_artists()

    artists_context = []
    for artist in artists:
        artists_context.append({
            'artist_id': artist['artist_id'],
            'name': artist['name'],
            'genre': artist['genre']
        })

    return render_template('artists.html', artists=artists_context)


@app.route('/artists/<int:artist_id>')
def artist_profile_page(artist_id):
    artists = load_artists()
    artist = next((a for a in artists if a['artist_id'] == artist_id), None)
    if not artist:
        abort(404)

    songs = load_songs()
    albums = {al['album_id']: al['title'] for al in load_albums()}

    artist_songs = []
    for s in songs:
        if s['artist_id'] == artist_id:
            artist_songs.append({
                'song_id': s['song_id'],
                'title': s['title'],
                'album_name': albums.get(s['album_id'], "Unknown")
            })

    return render_template('artist_profile.html', artist=artist, artist_songs=artist_songs)


@app.route('/genres')
def genre_exploration_page():
    genres = load_genres()
    songs = load_songs()
    artists = load_artists()

    # Get selected genre from query parameter
    selected_genre = request.args.get('genre')
    if selected_genre == '':
        selected_genre = None

    genre_songs = []
    genre_artists_set = set()

    if selected_genre:
        for s in songs:
            if s['genre'] == selected_genre:
                # Append song with needed info
                artist_name = next((a['name'] for a in artists if a['artist_id'] == s['artist_id']), "Unknown")
                genre_songs.append({
                    'song_id': s['song_id'],
                    'title': s['title'],
                    'artist_name': artist_name
                })
        for a in artists:
            if a['genre'] == selected_genre:
                genre_artists_set.add((a['artist_id'], a['name']))

    genre_artists = [{'artist_id': aid, 'name': name} for (aid, name) in sorted(genre_artists_set, key=lambda x: x[1])]

    return render_template('genres.html', genres=genres, selected_genre=selected_genre, genre_songs=genre_songs, genre_artists=genre_artists)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
