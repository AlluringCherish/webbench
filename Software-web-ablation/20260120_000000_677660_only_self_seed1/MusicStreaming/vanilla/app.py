from flask import Flask, render_template, request, redirect, url_for, abort
from datetime import date
import os

app = Flask(__name__)

# Data directory
DATA_DIR = 'data'

# ----- Helper Functions to Load Data -----

def load_songs():
    songs = []
    filepath = os.path.join(DATA_DIR, 'songs.txt')
    if not os.path.exists(filepath):
        return songs
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if line == '':
                continue
            fields = line.split('|')
            # Fields: song_id|title|artist_id|album_id|genre|duration|release_date|play_count
            try:
                song = {
                    'song_id': int(fields[0]),
                    'title': fields[1],
                    'artist_id': int(fields[2]),
                    'album_id': int(fields[3]),
                    'genre': fields[4].strip(),
                    'duration': int(fields[5]),
                    'release_date': fields[6],
                    'play_count': int(fields[7])
                }
                songs.append(song)
            except (IndexError, ValueError):
                continue
    return songs


def load_artists():
    artists = []
    filepath = os.path.join(DATA_DIR, 'artists.txt')
    if not os.path.exists(filepath):
        return artists
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if line == '':
                continue
            fields = line.split('|')
            # Fields: artist_id|name|genre|country|formation_year
            try:
                artist = {
                    'artist_id': int(fields[0]),
                    'name': fields[1],
                    'genre': fields[2],
                    'country': fields[3],
                    'formation_year': int(fields[4])
                }
                artists.append(artist)
            except (IndexError, ValueError):
                continue
    return artists


def load_albums():
    albums = []
    filepath = os.path.join(DATA_DIR, 'albums.txt')
    if not os.path.exists(filepath):
        return albums
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if line == '':
                continue
            fields = line.split('|')
            # Fields: album_id|title|artist_id|release_year|total_songs|genre
            try:
                album = {
                    'album_id': int(fields[0]),
                    'title': fields[1],
                    'artist_id': int(fields[2]),
                    'release_year': int(fields[3]),
                    'total_songs': int(fields[4]),
                    'genre': fields[5].strip()
                }
                albums.append(album)
            except (IndexError, ValueError):
                continue
    return albums


def load_genres():
    genres = []
    filepath = os.path.join(DATA_DIR, 'genres.txt')
    if not os.path.exists(filepath):
        return genres
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if line == '':
                continue
            fields = line.split('|')
            # Fields: genre_id|genre_name|description
            try:
                genre = {
                    'genre_id': int(fields[0]),
                    'genre_name': fields[1],
                    'description': fields[2]
                }
                genres.append(genre)
            except (IndexError, ValueError):
                continue
    return genres


def load_playlists():
    playlists = []
    filepath = os.path.join(DATA_DIR, 'playlists.txt')
    if not os.path.exists(filepath):
        return playlists
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if line == '':
                continue
            fields = line.split('|')
            # Fields: playlist_id|title|description|creation_date|total_songs
            try:
                playlist = {
                    'playlist_id': int(fields[0]),
                    'title': fields[1],
                    'description': fields[2],
                    'creation_date': fields[3],
                    'total_songs': int(fields[4])
                }
                playlists.append(playlist)
            except (IndexError, ValueError):
                continue
    return playlists


def load_playlist_songs():
    playlist_songs = []
    filepath = os.path.join(DATA_DIR, 'playlist_songs.txt')
    if not os.path.exists(filepath):
        return playlist_songs
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if line == '':
                continue
            fields = line.split('|')
            # Fields: playlist_song_id|playlist_id|song_id|added_date
            try:
                pls = {
                    'playlist_song_id': int(fields[0]),
                    'playlist_id': int(fields[1]),
                    'song_id': int(fields[2]),
                    'added_date': fields[3]
                }
                playlist_songs.append(pls)
            except (IndexError, ValueError):
                continue
    return playlist_songs

# ----- Helper Functions to Save Data -----

def save_playlists(playlists):
    filepath = os.path.join(DATA_DIR, 'playlists.txt')
    with open(filepath, 'w', encoding='utf-8') as f:
        for p in playlists:
            line = f"{p['playlist_id']}|{p['title']}|{p['description']}|{p['creation_date']}|{p['total_songs']}\n"
            f.write(line)


def save_playlist_songs(playlist_songs):
    filepath = os.path.join(DATA_DIR, 'playlist_songs.txt')
    with open(filepath, 'w', encoding='utf-8') as f:
        for pls in playlist_songs:
            line = f"{pls['playlist_song_id']}|{pls['playlist_id']}|{pls['song_id']}|{pls['added_date']}\n"
            f.write(line)


# ----- Route Implementations -----

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard_page'))


@app.route('/dashboard')
def dashboard_page():
    songs = load_songs()
    artists = load_artists()

    # Featured songs: let's define as top 5 most played songs (by play_count)
    # Collect song with artist_name
    songs_sorted = sorted(songs, key=lambda s: s['play_count'], reverse=True)
    featured_songs_raw = songs_sorted[:5]

    # Map artist_id to artist_name
    artist_dict = {artist['artist_id']: artist['name'] for artist in artists}

    featured_songs = []
    for s in featured_songs_raw:
        featured_songs.append({
            'song_id': s['song_id'],
            'title': s['title'],
            'artist_name': artist_dict.get(s['artist_id'], 'Unknown Artist'),
            'duration': s['duration']
        })

    # Trending artists: top 5 artists by sum of play counts of their songs
    artist_play_counts = {}
    for s in songs:
        artist_play_counts[s['artist_id']] = artist_play_counts.get(s['artist_id'], 0) + s['play_count']
    artists_sorted = sorted(artists, key=lambda a: artist_play_counts.get(a['artist_id'], 0), reverse=True)
    trending_artists_raw = artists_sorted[:5]

    trending_artists = []
    for a in trending_artists_raw:
        trending_artists.append({
            'artist_id': a['artist_id'],
            'name': a['name']
        })

    return render_template('dashboard.html', featured_songs=featured_songs, trending_artists=trending_artists)


@app.route('/songs', methods=['GET', 'POST'])
def song_catalog():
    songs = load_songs()
    artists = load_artists()
    albums = load_albums()

    # Build lookup dicts
    artist_dict = {a['artist_id']: a['name'] for a in artists}
    album_dict = {al['album_id']: al['title'] for al in albums}

    filter_genre = None
    search_query = None

    if request.method == 'POST':
        filter_genre = request.form.get('genre_filter')
        search_query = request.form.get('search_query')
    else:
        filter_genre = request.args.get('genre_filter')
        search_query = request.args.get('search_query')

    # Normalize empty strings to None
    if filter_genre == '' or filter_genre is None:
        filter_genre = None
    if search_query == '' or search_query is None:
        search_query = None

    # Filter songs
    filtered_songs = songs
    if filter_genre:
        # We will do case-insensitive exact match and also strip spaces
        normalized_filter_genre = filter_genre.strip().lower()
        filtered_songs = [s for s in filtered_songs if s['genre'].strip().lower() == normalized_filter_genre]
    if search_query:
        sq_lower = search_query.lower()
        filtered_songs = [s for s in filtered_songs if sq_lower in s['title'].lower()]

    # Build songs list for context
    songs_context = []
    for s in filtered_songs:
        songs_context.append({
            'song_id': s['song_id'],
            'title': s['title'],
            'artist_name': artist_dict.get(s['artist_id'], 'Unknown Artist'),
            'album_title': album_dict.get(s['album_id'], 'Unknown Album'),
            'genre': s['genre'],
            'duration': s['duration']
        })

    # Add page_title context for template
    page_title = 'Song Catalog'

    return render_template('song_catalog.html', songs=songs_context, filter_genre=filter_genre, search_query=search_query, page_title=page_title)


@app.route('/songs/<int:song_id>')
def song_details(song_id):
    songs = load_songs()
    artists = load_artists()
    albums = load_albums()

    song = next((s for s in songs if s['song_id'] == song_id), None)
    if not song:
        abort(404)

    artist = next((a for a in artists if a['artist_id'] == song['artist_id']), None)
    album = next((al for al in albums if al['album_id'] == song['album_id']), None)

    song_context = {
        'song_id': song['song_id'],
        'title': song['title'],
        'artist_id': artist['artist_id'] if artist else None,
        'artist_name': artist['name'] if artist else 'Unknown Artist',
        'album_id': album['album_id'] if album else None,
        'album_title': album['title'] if album else 'Unknown Album',
        'duration': song['duration']
    }

    return render_template('song_details.html', song=song_context)


@app.route('/playlists')
def playlists_page():
    playlists = load_playlists()

    playlists_context = []
    for p in playlists:
        playlists_context.append({
            'playlist_id': p['playlist_id'],
            'title': p['title'],
            'description': p['description'],
            'total_songs': p['total_songs']
        })

    return render_template('playlists.html', playlists=playlists_context)


@app.route('/playlists/<int:playlist_id>')
def playlist_details(playlist_id):
    playlists = load_playlists()
    playlist_songs = load_playlist_songs()
    songs = load_songs()
    artists = load_artists()

    playlist = next((p for p in playlists if p['playlist_id'] == playlist_id), None)
    if not playlist:
        abort(404)

    # Find songs in this playlist
    plsongs_links = [pl for pl in playlist_songs if pl['playlist_id'] == playlist_id]

    songs_context = []

    # Map artist_id to artist name
    artist_dict = {artist['artist_id']: artist['name'] for artist in artists}

    # Map song_id to song for duration
    song_dict = {song['song_id']: song for song in songs}

    for link in plsongs_links:
        song_id = link['song_id']
        song = song_dict.get(song_id)
        if song:
            songs_context.append({
                'song_id': song['song_id'],
                'title': song['title'],
                'artist_name': artist_dict.get(song['artist_id'], 'Unknown Artist'),
                'duration': song['duration']
            })

    playlist_context = {
        'playlist_id': playlist['playlist_id'],
        'title': playlist['title'],
        'description': playlist['description']
    }

    return render_template('playlist_details.html', playlist=playlist_context, songs=songs_context)


@app.route('/playlists/create', methods=['GET'])
def create_playlist():
    return render_template('create_playlist.html')


@app.route('/playlists/create', methods=['POST'])
def save_new_playlist():
    title = request.form.get('title', '').strip()
    description = request.form.get('description', '').strip()

    if title == '':
        # We could add a better message but spec requires no extra features
        return redirect(url_for('create_playlist'))

    playlists = load_playlists()

    # Generate new unique playlist_id
    max_id = max([p['playlist_id'] for p in playlists], default=0)
    new_id = max_id + 1

    creation_date = date.today().isoformat()

    new_playlist = {
        'playlist_id': new_id,
        'title': title,
        'description': description,
        'creation_date': creation_date,
        'total_songs': 0
    }

    playlists.append(new_playlist)

    save_playlists(playlists)

    return redirect(url_for('playlists_page'))


@app.route('/albums')
def albums_page():
    albums = load_albums()
    artists = load_artists()

    artist_dict = {a['artist_id']: a['name'] for a in artists}

    albums_context = []
    for al in albums:
        albums_context.append({
            'album_id': al['album_id'],
            'title': al['title'],
            'artist_name': artist_dict.get(al['artist_id'], 'Unknown Artist'),
            'release_year': al['release_year'],
            'genre': al['genre']
        })

    return render_template('albums.html', albums=albums_context)


@app.route('/albums/<int:album_id>')
def album_details(album_id):
    albums = load_albums()
    artists = load_artists()
    songs = load_songs()

    album = next((al for al in albums if al['album_id'] == album_id), None)
    if not album:
        abort(404)

    artist = next((a for a in artists if a['artist_id'] == album['artist_id']), None)

    album_context = {
        'album_id': album['album_id'],
        'title': album['title'],
        'artist_id': artist['artist_id'] if artist else None,
        'artist_name': artist['name'] if artist else 'Unknown Artist',
        'release_year': album['release_year'],
        'genre': album['genre']
    }

    album_songs = [s for s in songs if s['album_id'] == album_id]

    songs_context = []
    for s in album_songs:
        songs_context.append({
            'song_id': s['song_id'],
            'title': s['title'],
            'duration': s['duration']
        })

    return render_template('album_details.html', album=album_context, songs=songs_context)


@app.route('/artists')
def artists_page():
    artists = load_artists()

    artists_context = []
    for a in artists:
        artists_context.append({
            'artist_id': a['artist_id'],
            'name': a['name'],
            'genre': a['genre'],
            'country': a['country']
        })

    return render_template('artists.html', artists=artists_context)


@app.route('/artists/<int:artist_id>')
def artist_profile(artist_id):
    artists = load_artists()

    artist = next((a for a in artists if a['artist_id'] == artist_id), None)

    if not artist:
        abort(404)

    artist_context = {
        'artist_id': artist['artist_id'],
        'name': artist['name'],
        'genre': artist['genre'],
        'country': artist['country'],
        'formation_year': artist['formation_year']
    }

    return render_template('artist_profile.html', artist=artist_context)


@app.route('/genres')
def genres_page():
    genres = load_genres()
    songs = load_songs()
    artists = load_artists()

    selected_genre_id = None
    genre_name = None

    selected_genre_id_str = request.args.get('selected_genre_id')

    # find selected_genre_id if passed
    try:
        selected_genre_id = int(selected_genre_id_str) if selected_genre_id_str else None
    except ValueError:
        selected_genre_id = None

    # Map genre_id to genre name
    genre_dict = {g['genre_id']: g['genre_name'] for g in genres}

    if selected_genre_id and selected_genre_id in genre_dict:
        genre_name = genre_dict[selected_genre_id]

    genre_songs = []
    genre_artists = []

    if genre_name:
        # Filter songs by genre name
        genre_songs_raw = [s for s in songs if s['genre'].lower() == genre_name.lower()]

        artist_dict = {a['artist_id']: a['name'] for a in artists}

        genre_songs = [{
            'song_id': s['song_id'],
            'title': s['title'],
            'artist_name': artist_dict.get(s['artist_id'], 'Unknown Artist'),
            'duration': s['duration']
        } for s in genre_songs_raw]

        # Find distinct artists for this genre
        genre_artist_ids = set(s['artist_id'] for s in genre_songs_raw)

        genre_artists = [{
            'artist_id': a['artist_id'],
            'name': a['name']
        } for a in artists if a['artist_id'] in genre_artist_ids]

    return render_template('genres.html', 
                           genres=genres, 
                           selected_genre_id=selected_genre_id, 
                           genre_songs=genre_songs, 
                           genre_artists=genre_artists)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
