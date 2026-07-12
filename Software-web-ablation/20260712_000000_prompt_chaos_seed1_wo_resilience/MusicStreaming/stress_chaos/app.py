from flask import Flask, render_template, redirect, url_for, request
from datetime import date
import os

app = Flask(__name__)
DATA_DIR = 'data'

# Utility functions to load data

def load_songs():
    songs = []
    path = os.path.join(DATA_DIR, 'songs.txt')
    if not os.path.exists(path):
        return songs
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            fields = line.split('|')
            # 1. song_id (int), 2. title (str), 3. artist_id (int), 4. album_id (int), 5. genre (str), 6. duration (int), 7. release_date (str), 8. play_count (int)
            if len(fields) != 8:
                continue
            try:
                song_id = int(fields[0])
                title = fields[1]
                artist_id = int(fields[2])
                album_id = int(fields[3])
                genre = fields[4]
                duration = int(fields[5])
                release_date = fields[6]
                play_count = int(fields[7])
            except ValueError:
                continue
            songs.append({
                'song_id': song_id,
                'title': title,
                'artist_id': artist_id,
                'album_id': album_id,
                'genre': genre,
                'duration': duration,
                'release_date': release_date,
                'play_count': play_count
            })
    return songs


def load_artists():
    artists = []
    path = os.path.join(DATA_DIR, 'artists.txt')
    if not os.path.exists(path):
        return artists
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            fields = line.split('|')
            # 1. artist_id (int), 2. name (str), 3. genre (str), 4. country (str), 5. formation_year (int)
            if len(fields) != 5:
                continue
            try:
                artist_id = int(fields[0])
                name = fields[1]
                genre = fields[2]
                country = fields[3]
                formation_year = int(fields[4])
            except ValueError:
                continue
            artists.append({
                'artist_id': artist_id,
                'name': name,
                'genre': genre,
                'country': country,
                'formation_year': formation_year
            })
    return artists


def load_albums():
    albums = []
    path = os.path.join(DATA_DIR, 'albums.txt')
    if not os.path.exists(path):
        return albums
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            fields = line.split('|')
            # 1. album_id (int), 2. title (str), 3. artist_id (int), 4. release_year (int), 5. total_songs (int), 6. genre (str)
            if len(fields) != 6:
                continue
            try:
                album_id = int(fields[0])
                title = fields[1]
                artist_id = int(fields[2])
                release_year = int(fields[3])
                total_songs = int(fields[4])
                genre = fields[5]
            except ValueError:
                continue
            albums.append({
                'album_id': album_id,
                'title': title,
                'artist_id': artist_id,
                'release_year': release_year,
                'total_songs': total_songs,
                'genre': genre
            })
    return albums


def load_genres():
    genres = []
    path = os.path.join(DATA_DIR, 'genres.txt')
    if not os.path.exists(path):
        return genres
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            fields = line.split('|')
            # 1. genre_id (int), 2. genre_name (str), 3. description (str)
            if len(fields) != 3:
                continue
            try:
                genre_id = int(fields[0])
                genre_name = fields[1]
                description = fields[2]
            except ValueError:
                continue
            genres.append({
                'genre_id': genre_id,
                'genre_name': genre_name,
                'description': description
            })
    return genres


def load_playlists():
    playlists = []
    path = os.path.join(DATA_DIR, 'playlists.txt')
    if not os.path.exists(path):
        return playlists
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            fields = line.split('|')
            # 1. playlist_id (int), 2. title (str), 3. description (str), 4. creation_date (str), 5. total_songs (int)
            if len(fields) != 5:
                continue
            try:
                playlist_id = int(fields[0])
                title = fields[1]
                description = fields[2]
                creation_date = fields[3]
                total_songs = int(fields[4])
            except ValueError:
                continue
            playlists.append({
                'playlist_id': playlist_id,
                'title': title,
                'description': description,
                'creation_date': creation_date,
                'total_songs': total_songs
            })
    return playlists


def load_playlist_songs():
    playlist_songs = []
    path = os.path.join(DATA_DIR, 'playlist_songs.txt')
    if not os.path.exists(path):
        return playlist_songs
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            fields = line.split('|')
            # 1. playlist_song_id (int), 2. playlist_id (int), 3. song_id (int), 4. added_date (str)
            if len(fields) != 4:
                continue
            try:
                playlist_song_id = int(fields[0])
                playlist_id = int(fields[1])
                song_id = int(fields[2])
                added_date = fields[3]
            except ValueError:
                continue
            playlist_songs.append({
                'playlist_song_id': playlist_song_id,
                'playlist_id': playlist_id,
                'song_id': song_id,
                'added_date': added_date
            })
    return playlist_songs

# Utility functions to save data

def save_playlists(playlists):
    path = os.path.join(DATA_DIR, 'playlists.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for p in playlists:
            line = f"{p['playlist_id']}|{p['title']}|{p['description']}|{p['creation_date']}|{p['total_songs']}\n"
            f.write(line)


def save_playlist_songs(playlist_songs):
    path = os.path.join(DATA_DIR, 'playlist_songs.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for ps in playlist_songs:
            line = f"{ps['playlist_song_id']}|{ps['playlist_id']}|{ps['song_id']}|{ps['added_date']}\n"
            f.write(line)

# Utility lookups

def get_artist_by_id(artist_id, artists):
    for a in artists:
        if a['artist_id'] == artist_id:
            return a
    return None


def get_album_by_id(album_id, albums):
    for a in albums:
        if a['album_id'] == album_id:
            return a
    return None


def get_playlist_by_id(playlist_id, playlists):
    for p in playlists:
        if p['playlist_id'] == playlist_id:
            return p
    return None


def get_genre_by_name(genres, name):
    for g in genres:
        if g['genre_name'].lower() == name.lower():
            return g
    return None


def get_artist_name(artist_id, artists):
    artist = get_artist_by_id(artist_id, artists)
    return artist['name'] if artist else 'Unknown Artist'


def get_album_name(album_id, albums):
    album = get_album_by_id(album_id, albums)
    return album['title'] if album else 'Unknown Album'


def get_next_playlist_id(playlists):
    if not playlists:
        return 1
    return max(p['playlist_id'] for p in playlists) + 1


def get_next_playlist_song_id(playlist_songs):
    if not playlist_songs:
        return 1
    return max(ps['playlist_song_id'] for ps in playlist_songs) + 1

# Route implementations

@app.route('/')
def root_redirect():
    # Redirect to /dashboard
    return redirect(url_for('dashboard_page'))


@app.route('/dashboard')
def dashboard_page():
    # Load data
    songs = load_songs()
    artists = load_artists()

    # Featured songs: choose top 5 by play_count descending for demo
    sorted_songs = sorted(songs, key=lambda s: s['play_count'], reverse=True)
    featured_songs = []
    for s in sorted_songs[:5]:
        artist_name = get_artist_name(s['artist_id'], artists)
        featured_songs.append({
            'song_id': s['song_id'],
            'title': s['title'],
            'artist_name': artist_name,
            'duration': s['duration']
        })

    # Trending artists: top 5 by play_count of their songs combined
    artist_play_counts = {}
    for s in songs:
        artist_play_counts[s['artist_id']] = artist_play_counts.get(s['artist_id'], 0) + s['play_count']

    sorted_artists = sorted(artists, key=lambda a: artist_play_counts.get(a['artist_id'], 0), reverse=True)
    trending_artists = []
    for a in sorted_artists[:5]:
        trending_artists.append({
            'artist_id': a['artist_id'],
            'name': a['name'],
            'genre': a['genre']
        })

    return render_template('dashboard.html', featured_songs=featured_songs, trending_artists=trending_artists)


@app.route('/songs')
def song_catalog_page():
    songs = load_songs()
    artists = load_artists()
    albums = load_albums()
    genres = [g['genre_name'] for g in load_genres()]

    # Full songs list with artist_name, album_name, genre, duration
    songs_for_display = []
    for s in songs:
        artist_name = get_artist_name(s['artist_id'], artists)
        album_name = get_album_name(s['album_id'], albums)
        songs_for_display.append({
            'song_id': s['song_id'],
            'title': s['title'],
            'artist_name': artist_name,
            'album_name': album_name,
            'genre': s['genre'],
            'duration': s['duration']
        })

    return render_template('song_catalog.html', songs=songs_for_display, genres=genres, search_query='', selected_genre=None)


@app.route('/songs/search', methods=['POST'])
def song_search():
    search_query = request.form.get('search_query', '').strip()
    selected_genre = request.form.get('selected_genre')

    songs = load_songs()
    artists = load_artists()
    albums = load_albums()
    genres_data = load_genres()
    genres = [g['genre_name'] for g in genres_data]

    filtered_songs = songs

    if search_query:
        search_lower = search_query.lower()
        filtered_songs = [s for s in filtered_songs if search_lower in s['title'].lower()]

    if selected_genre and selected_genre != '':
        # Filter songs by genre exact match
        filtered_songs = [s for s in filtered_songs if s['genre'].lower() == selected_genre.lower()]
    else:
        selected_genre = None

    songs_for_display = []
    for s in filtered_songs:
        artist_name = get_artist_name(s['artist_id'], artists)
        album_name = get_album_name(s['album_id'], albums)
        songs_for_display.append({
            'song_id': s['song_id'],
            'title': s['title'],
            'artist_name': artist_name,
            'album_name': album_name,
            'genre': s['genre'],
            'duration': s['duration']
        })

    return render_template('song_catalog.html', songs=songs_for_display, genres=genres, search_query=search_query, selected_genre=selected_genre)


@app.route('/songs/<int:song_id>')
def song_details_page(song_id):
    songs = load_songs()
    artists = load_artists()
    albums = load_albums()

    song = None
    for s in songs:
        if s['song_id'] == song_id:
            song = s
            break
    if song is None:
        return "Song not found", 404

    artist = get_artist_by_id(song['artist_id'], artists)
    album = get_album_by_id(song['album_id'], albums)

    result = {
        'song_id': song['song_id'],
        'title': song['title'],
        'artist_id': artist['artist_id'] if artist else None,
        'artist_name': artist['name'] if artist else 'Unknown Artist',
        'album_name': album['title'] if album else 'Unknown Album',
        'duration': song['duration']
    }

    return render_template('song_details.html', song=result)


@app.route('/playlists')
def playlists_page():
    playlists = load_playlists()

    # Context: playlists with total_songs included already
    return render_template('playlists.html', playlists=playlists)


@app.route('/playlists/create', methods=['GET', 'POST'])
def create_playlist_page():
    if request.method == 'GET':
        return render_template('create_playlist.html')

    # POST handler
    title = request.form.get('playlist_name', '').strip()
    description = request.form.get('playlist_description', '').strip()

    # Basic validation
    error_message = None
    success_message = None
    if not title:
        error_message = 'Playlist name is required.'
        return render_template('create_playlist.html', error_message=error_message)

    playlists = load_playlists()

    # Check for duplicate title?
    for p in playlists:
        if p['title'].lower() == title.lower():
            error_message = 'A playlist with this name already exists.'
            return render_template('create_playlist.html', error_message=error_message)

    next_id = get_next_playlist_id(playlists)
    new_playlist = {
        'playlist_id': next_id,
        'title': title,
        'description': description,
        'creation_date': date.today().isoformat(),
        'total_songs': 0
    }
    playlists.append(new_playlist)
    save_playlists(playlists)

    success_message = f'Playlist "{title}" created successfully.'
    return render_template('create_playlist.html', success_message=success_message)


@app.route('/playlists/<int:playlist_id>')
def playlist_details_page(playlist_id):
    playlists = load_playlists()
    playlist = get_playlist_by_id(playlist_id, playlists)
    if not playlist:
        return "Playlist not found", 404

    playlist_songs = load_playlist_songs()
    songs = load_songs()
    artists = load_artists()

    # get songs in this playlist
    songs_in_playlist = []
    playlist_song_ids = []
    for ps in playlist_songs:
        if ps['playlist_id'] == playlist_id:
            playlist_song_ids.append(ps['song_id'])
    for song_id in playlist_song_ids:
        song = next((s for s in songs if s['song_id'] == song_id), None)
        if not song:
            continue
        artist_name = get_artist_name(song['artist_id'], artists)
        songs_in_playlist.append({
            'song_id': song['song_id'],
            'title': song['title'],
            'artist_name': artist_name,
            'duration': song['duration']
        })

    return render_template('playlist_details.html', playlist=playlist, songs_in_playlist=songs_in_playlist)


@app.route('/playlists/<int:playlist_id>/delete', methods=['POST'])
def delete_playlist(playlist_id):
    playlists = load_playlists()
    playlist_songs = load_playlist_songs()

    playlists = [p for p in playlists if p['playlist_id'] != playlist_id]
    playlist_songs = [ps for ps in playlist_songs if ps['playlist_id'] != playlist_id]

    save_playlists(playlists)
    save_playlist_songs(playlist_songs)

    return redirect(url_for('playlists_page'))


@app.route('/playlists/<int:playlist_id>/songs/<int:song_id>/remove', methods=['POST'])
def remove_song_from_playlist(playlist_id, song_id):
    playlist_songs = load_playlist_songs()
    playlists = load_playlists()

    # Remove entry matching playlist_id and song_id
    playlist_songs = [ps for ps in playlist_songs if not(ps['playlist_id'] == playlist_id and ps['song_id'] == song_id)]

    # Update playlist total_songs field
    # Count remaining songs for this playlist
    song_count = sum(1 for ps in playlist_songs if ps['playlist_id'] == playlist_id)

    for p in playlists:
        if p['playlist_id'] == playlist_id:
            p['total_songs'] = song_count
            break

    save_playlist_songs(playlist_songs)
    save_playlists(playlists)

    return redirect(url_for('playlist_details_page', playlist_id=playlist_id))


@app.route('/albums')
def album_browse_page():
    albums = load_albums()
    artists = load_artists()

    albums_for_display = []
    for a in albums:
        artist_name = get_artist_name(a['artist_id'], artists)
        albums_for_display.append({
            'album_id': a['album_id'],
            'title': a['title'],
            'artist_name': artist_name,
            'release_year': a['release_year']
        })

    return render_template('album_browse.html', albums=albums_for_display, search_query='', sort_option='By Title')


@app.route('/albums/search', methods=['POST'])
def album_search():
    search_query = request.form.get('search_query', '').strip()
    sort_option = request.form.get('sort_option', 'By Title')

    albums = load_albums()
    artists = load_artists()

    filtered_albums = albums

    if search_query:
        search_lower = search_query.lower()
        filtered_albums = [a for a in filtered_albums if search_lower in a['title'].lower()]

    albums_for_display = []
    for a in filtered_albums:
        artist_name = get_artist_name(a['artist_id'], artists)
        albums_for_display.append({
            'album_id': a['album_id'],
            'title': a['title'],
            'artist_name': artist_name,
            'release_year': a['release_year']
        })

    if sort_option == 'By Artist':
        albums_for_display.sort(key=lambda x: x['artist_name'].lower())
    elif sort_option == 'By Year':
        albums_for_display.sort(key=lambda x: x['release_year'])
    else:
        albums_for_display.sort(key=lambda x: x['title'].lower())

    return render_template('album_browse.html', albums=albums_for_display, search_query=search_query, sort_option=sort_option)


@app.route('/albums/<int:album_id>')
def album_details_page(album_id):
    albums = load_albums()
    artists = load_artists()
    songs = load_songs()

    album = get_album_by_id(album_id, albums)
    if album is None:
        return "Album not found", 404

    artist = get_artist_by_id(album['artist_id'], artists)

    songs_in_album = []
    for s in songs:
        if s['album_id'] == album_id:
            songs_in_album.append({
                'song_id': s['song_id'],
                'title': s['title'],
                'duration': s['duration']
            })

    result_album = {
        'album_id': album['album_id'],
        'title': album['title'],
        'artist_name': artist['name'] if artist else 'Unknown Artist',
        'release_year': album['release_year']
    }

    return render_template('album_details.html', album=result_album, songs_in_album=songs_in_album)


@app.route('/albums/<int:album_id>/add_to_playlist', methods=['POST'])
def add_album_to_playlist(album_id):
    playlist_id = request.form.get('playlist_id')
    if not playlist_id:
        # No playlist_id provided
        return redirect(url_for('album_details_page', album_id=album_id))
    try:
        playlist_id = int(playlist_id)
    except ValueError:
        return redirect(url_for('album_details_page', album_id=album_id))

    playlists = load_playlists()
    playlist = get_playlist_by_id(playlist_id, playlists)
    if playlist is None:
        return redirect(url_for('album_details_page', album_id=album_id))

    songs = load_songs()
    playlist_songs = load_playlist_songs()

    # Add all songs in album to the playlist if not already added
    existing_song_ids = {ps['song_id'] for ps in playlist_songs if ps['playlist_id'] == playlist_id}

    album_song_ids = [s['song_id'] for s in songs if s['album_id'] == album_id]

    next_playlist_song_id = get_next_playlist_song_id(playlist_songs)
    date_added = date.today().isoformat()
    added_any = False
    for sid in album_song_ids:
        if sid not in existing_song_ids:
            playlist_songs.append({
                'playlist_song_id': next_playlist_song_id,
                'playlist_id': playlist_id,
                'song_id': sid,
                'added_date': date_added
            })
            next_playlist_song_id += 1
            added_any = True

    # Update total_songs for playlist
    if added_any:
        playlist['total_songs'] = sum(1 for ps in playlist_songs if ps['playlist_id'] == playlist_id)
        save_playlists(playlists)
        save_playlist_songs(playlist_songs)

    return redirect(url_for('album_details_page', album_id=album_id))


@app.route('/artists')
def artist_profile_page():
    artists = load_artists()
    return render_template('artist_profile.html', artists=artists, search_query='', sort_option='By Name')


@app.route('/artists/search', methods=['POST'])
def artist_search():
    search_query = request.form.get('search_query', '').strip()
    sort_option = request.form.get('sort_option', 'By Name')

    artists_all = load_artists()
    filtered_artists = artists_all

    if search_query:
        search_lower = search_query.lower()
        filtered_artists = [a for a in filtered_artists if search_lower in a['name'].lower()]

    if sort_option == 'By Genre':
        filtered_artists.sort(key=lambda x: x['genre'].lower())
    else:
        filtered_artists.sort(key=lambda x: x['name'].lower())

    return render_template('artist_profile.html', artists=filtered_artists, search_query=search_query, sort_option=sort_option)


@app.route('/artists/<int:artist_id>')
def artist_details_page(artist_id):
    artists = load_artists()
    songs = load_songs()
    albums = load_albums()

    artist = get_artist_by_id(artist_id, artists)
    if artist is None:
        return "Artist not found", 404

    # Songs by artist
    songs_by_artist = []
    for s in songs:
        if s['artist_id'] == artist_id:
            album_name = get_album_name(s['album_id'], albums)
            songs_by_artist.append({
                'song_id': s['song_id'],
                'title': s['title'],
                'album_name': album_name,
                'duration': s['duration']
            })

    return render_template('artist_details.html', artist=artist, songs_by_artist=songs_by_artist)


@app.route('/genres')
def genre_exploration_page():
    genres = load_genres()
    songs = load_songs()
    artists = load_artists()

    # On initial GET, no selected genre
    selected_genre = None
    songs_in_genre = []
    artists_in_genre = []

    return render_template('genre_exploration.html', genres=genres, selected_genre=selected_genre, songs_in_genre=songs_in_genre, artists_in_genre=artists_in_genre)


@app.route('/genres/filter', methods=['POST'])
def genre_filter():
    selected_genre = request.form.get('selected_genre')

    genres = load_genres()
    songs = load_songs()
    artists = load_artists()

    if not selected_genre:
        selected_genre = None

    # Filter songs and artists by selected genre (case insensitive match)
    songs_in_genre = [s for s in songs if s['genre'].lower() == selected_genre.lower()] if selected_genre else []
    artists_in_genre = [a for a in artists if a['genre'].lower() == selected_genre.lower()] if selected_genre else []

    # Format songs_in_genre as required
    songs_display = []
    for s in songs_in_genre:
        artist_name = get_artist_name(s['artist_id'], artists)
        songs_display.append({
            'song_id': s['song_id'],
            'title': s['title'],
            'artist_name': artist_name,
            'duration': s['duration']
        })

    # Format artists_in_genre as required
    artists_display = []
    for a in artists_in_genre:
        artists_display.append({
            'artist_id': a['artist_id'],
            'name': a['name'],
            'genre': a['genre']
        })

    return render_template('genre_exploration.html', genres=genres, selected_genre=selected_genre, songs_in_genre=songs_display, artists_in_genre=artists_display)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
