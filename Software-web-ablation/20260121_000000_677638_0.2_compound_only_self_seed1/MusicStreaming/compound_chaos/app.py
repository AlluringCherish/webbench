from flask import Flask, render_template, request, redirect, url_for, abort
import os
import datetime

app = Flask(__name__)

# Data file paths
SONGS_FILE = 'data/songs.txt'
ARTISTS_FILE = 'data/artists.txt'
ALBUMS_FILE = 'data/albums.txt'
GENRES_FILE = 'data/genres.txt'
PLAYLISTS_FILE = 'data/playlists.txt'
PLAYLIST_SONGS_FILE = 'data/playlist_songs.txt'

# --- Helper functions to load and save data ---

def load_songs():
    songs = []
    if not os.path.exists(SONGS_FILE):
        return songs
    with open(SONGS_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 8:
                continue
            try:
                song = {
                    'song_id': int(parts[0]),
                    'title': parts[1],
                    'artist_id': int(parts[2]),
                    'album_id': int(parts[3]),
                    'genre': parts[4],
                    'duration': int(parts[5]),
                    'release_date': parts[6],
                    'play_count': int(parts[7])
                }
                songs.append(song)
            except ValueError:
                continue
    return songs


def load_artists():
    artists = []
    if not os.path.exists(ARTISTS_FILE):
        return artists
    with open(ARTISTS_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 5:
                continue
            try:
                artist = {
                    'artist_id': int(parts[0]),
                    'name': parts[1],
                    'genre': parts[2],
                    'country': parts[3],
                    'formation_year': int(parts[4])
                }
                artists.append(artist)
            except ValueError:
                continue
    return artists


def load_albums():
    albums = []
    if not os.path.exists(ALBUMS_FILE):
        return albums
    with open(ALBUMS_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 6:
                continue
            try:
                album = {
                    'album_id': int(parts[0]),
                    'title': parts[1],
                    'artist_id': int(parts[2]),
                    'release_year': int(parts[3]),
                    'total_songs': int(parts[4]),
                    'genre': parts[5]
                }
                albums.append(album)
            except ValueError:
                continue
    return albums


def load_genres():
    genres = []
    if not os.path.exists(GENRES_FILE):
        return genres
    with open(GENRES_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 3:
                continue
            try:
                genre = {
                    'genre_id': int(parts[0]),
                    'genre_name': parts[1],
                    'description': parts[2]
                }
                genres.append(genre)
            except ValueError:
                continue
    return genres


def load_playlists():
    playlists = []
    if not os.path.exists(PLAYLISTS_FILE):
        return playlists
    with open(PLAYLISTS_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 5:
                continue
            try:
                playlist = {
                    'playlist_id': int(parts[0]),
                    'title': parts[1],
                    'description': parts[2],
                    'creation_date': parts[3],
                    'total_songs': int(parts[4])
                }
                playlists.append(playlist)
            except ValueError:
                continue
    return playlists


def save_playlists(playlists):
    with open(PLAYLISTS_FILE, 'w', encoding='utf-8') as f:
        for pl in playlists:
            line = f"{pl['playlist_id']}|{pl['title']}|{pl['description']}|{pl['creation_date']}|{pl['total_songs']}"
            f.write(line + '\n')


def load_playlist_songs():
    playlist_songs = []
    if not os.path.exists(PLAYLIST_SONGS_FILE):
        return playlist_songs
    with open(PLAYLIST_SONGS_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 4:
                continue
            try:
                ps = {
                    'playlist_song_id': int(parts[0]),
                    'playlist_id': int(parts[1]),
                    'song_id': int(parts[2]),
                    'added_date': parts[3]
                }
                playlist_songs.append(ps)
            except ValueError:
                continue
    return playlist_songs


def save_playlist_songs(playlist_songs):
    with open(PLAYLIST_SONGS_FILE, 'w', encoding='utf-8') as f:
        for ps in playlist_songs:
            line = f"{ps['playlist_song_id']}|{ps['playlist_id']}|{ps['song_id']}|{ps['added_date']}"
            f.write(line + '\n')


# --- Utility find functions ---

def find_artist_by_id(artist_id):
    artists = load_artists()
    for artist in artists:
        if artist['artist_id'] == artist_id:
            return artist
    return None


def find_album_by_id(album_id):
    albums = load_albums()
    for album in albums:
        if album['album_id'] == album_id:
            return album
    return None


def find_song_by_id(song_id):
    songs = load_songs()
    for song in songs:
        if song['song_id'] == song_id:
            return song
    return None


def find_playlist_by_id(playlist_id):
    playlists = load_playlists()
    for pl in playlists:
        if pl['playlist_id'] == playlist_id:
            return pl
    return None


def get_next_playlist_id(playlists):
    return max([pl['playlist_id'] for pl in playlists], default=0) + 1


def get_next_playlist_song_id(playlist_songs):
    return max([ps['playlist_song_id'] for ps in playlist_songs], default=0) + 1


def get_artist_name(artist_id):
    artist = find_artist_by_id(artist_id)
    if artist:
        return artist['name']
    return ''


def get_album_name(album_id):
    album = find_album_by_id(album_id)
    if album:
        return album['title']
    return ''

# --- Flask Routes ---

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    songs = load_songs()
    artists = load_artists()

    # Featured songs: top 5 by play_count
    featured_songs_raw = sorted(songs, key=lambda x: x['play_count'], reverse=True)[:5]
    featured_songs = []
    for s in featured_songs_raw:
        featured_songs.append({
            'song_id': s['song_id'],
            'title': s['title'],
            'artist_name': get_artist_name(s['artist_id']),
            'duration': s['duration']
        })

    # Trending artists: top 5 by total play_count across songs
    artist_play_counts = {}
    for a in artists:
        artist_play_counts[a['artist_id']] = 0
    for s in songs:
        artist_play_counts[s['artist_id']] = artist_play_counts.get(s['artist_id'], 0) + s['play_count']
    trending_artists_raw = sorted(artists, key=lambda x: artist_play_counts.get(x['artist_id'], 0), reverse=True)[:5]
    trending_artists = []
    for a in trending_artists_raw:
        trending_artists.append({
            'artist_id': a['artist_id'],
            'name': a['name']
        })

    return render_template('dashboard.html', featured_songs=featured_songs, trending_artists=trending_artists)


@app.route('/songs')
def song_catalog():
    songs = load_songs()
    artists = load_artists()
    albums = load_albums()
    genres = load_genres()

    artist_dict = {a['artist_id']: a['name'] for a in artists}
    album_dict = {al['album_id']: al['title'] for al in albums}
    genres_list = [g['genre_name'] for g in genres]

    songs_context = []
    for s in songs:
        songs_context.append({
            'song_id': s['song_id'],
            'title': s['title'],
            'artist_name': artist_dict.get(s['artist_id'], ''),
            'album_name': album_dict.get(s['album_id'], ''),
            'genre': s['genre'],
            'duration': s['duration']
        })

    return render_template('song_catalog.html', songs=songs_context, genres=genres_list)


@app.route('/songs/search', methods=['POST'])
def song_search_filter():
    search_input = request.form.get('search_input', '').strip().lower()
    genre_filter = request.form.get('genre_filter', '').strip()

    songs = load_songs()
    artists = load_artists()
    albums = load_albums()
    genres = load_genres()

    artist_dict = {a['artist_id']: a['name'] for a in artists}
    album_dict = {al['album_id']: al['title'] for al in albums}
    genres_list = [g['genre_name'] for g in genres]

    filtered_songs = []
    for s in songs:
        title_match = search_input in s['title'].lower() if search_input else True
        genre_match = s['genre'] == genre_filter if genre_filter and genre_filter != 'All' else True
        if title_match and genre_match:
            filtered_songs.append({
                'song_id': s['song_id'],
                'title': s['title'],
                'artist_name': artist_dict.get(s['artist_id'], ''),
                'album_name': album_dict.get(s['album_id'], ''),
                'genre': s['genre'],
                'duration': s['duration']
            })

    return render_template('song_catalog.html', songs=filtered_songs, genres=genres_list)


@app.route('/songs/<int:song_id>')
def song_details(song_id):
    song = find_song_by_id(song_id)
    if not song:
        abort(404)
    artist = find_artist_by_id(song['artist_id'])
    album = find_album_by_id(song['album_id'])

    song_context = {
        'song_id': song['song_id'],
        'title': song['title'],
        'artist_id': artist['artist_id'] if artist else None,
        'artist_name': artist['name'] if artist else '',
        'album_id': album['album_id'] if album else None,
        'album_name': album['title'] if album else '',
        'genre': song['genre'],
        'duration': song['duration']
    }
    return render_template('song_details.html', song=song_context)


@app.route('/playlists')
def playlists():
    playlists = load_playlists()

    playlists_context = []
    for pl in playlists:
        playlists_context.append({
            'playlist_id': pl['playlist_id'],
            'title': pl['title'],
            'description': pl['description'],
            'total_songs': pl['total_songs']
        })

    return render_template('playlists.html', playlists=playlists_context)


@app.route('/playlists/create', methods=['GET'])
def create_playlist():
    return render_template('create_playlist.html')


@app.route('/playlists/create', methods=['POST'])
def create_playlist_post():
    title = request.form.get('playlist-name-input', '').strip()
    description = request.form.get('playlist-description-input', '').strip()

    if not title:
        return redirect(url_for('create_playlist'))

    playlists = load_playlists()
    new_id = get_next_playlist_id(playlists)
    creation_date = datetime.datetime.now().strftime('%Y-%m-%d')

    new_playlist = {
        'playlist_id': new_id,
        'title': title,
        'description': description,
        'creation_date': creation_date,
        'total_songs': 0
    }

    playlists.append(new_playlist)
    save_playlists(playlists)

    return redirect(url_for('playlists'))


@app.route('/playlists/<int:playlist_id>')
def playlist_details(playlist_id):
    playlist = find_playlist_by_id(playlist_id)
    if not playlist:
        abort(404)

    playlist_songs = load_playlist_songs()
    songs = load_songs()
    artists = load_artists()
    artist_dict = {a['artist_id']: a['name'] for a in artists}

    songs_in_playlist = []
    for ps in playlist_songs:
        if ps['playlist_id'] == playlist_id:
            song = next((s for s in songs if s['song_id'] == ps['song_id']), None)
            if song:
                songs_in_playlist.append({
                    'song_id': song['song_id'],
                    'title': song['title'],
                    'artist_name': artist_dict.get(song['artist_id'], ''),
                    'duration': song['duration']
                })

    playlist_context = {
        'playlist_id': playlist['playlist_id'],
        'title': playlist['title'],
        'description': playlist['description']
    }

    return render_template('playlist_details.html', playlist=playlist_context, songs=songs_in_playlist)


@app.route('/playlists/<int:playlist_id>/delete', methods=['POST'])
def delete_playlist(playlist_id):
    playlists = load_playlists()
    playlist_songs = load_playlist_songs()

    playlists = [pl for pl in playlists if pl['playlist_id'] != playlist_id]
    save_playlists(playlists)

    playlist_songs = [ps for ps in playlist_songs if ps['playlist_id'] != playlist_id]
    save_playlist_songs(playlist_songs)

    return redirect(url_for('playlists'))


@app.route('/playlists/<int:playlist_id>/remove_song/<int:song_id>', methods=['POST'])
def remove_song_from_playlist(playlist_id, song_id):
    playlist_songs = load_playlist_songs()
    playlists = load_playlists()

    playlist_songs = [ps for ps in playlist_songs if not (ps['playlist_id'] == playlist_id and ps['song_id'] == song_id)]
    save_playlist_songs(playlist_songs)

    for pl in playlists:
        if pl['playlist_id'] == playlist_id:
            pl['total_songs'] = sum(1 for ps in playlist_songs if ps['playlist_id'] == playlist_id)
            break
    save_playlists(playlists)

    return redirect(url_for('playlist_details', playlist_id=playlist_id))


@app.route('/albums')
def albums_browse():
    albums = load_albums()
    artists = load_artists()
    artist_dict = {a['artist_id']: a['name'] for a in artists}

    albums_context = []
    for al in albums:
        albums_context.append({
            'album_id': al['album_id'],
            'title': al['title'],
            'artist_name': artist_dict.get(al['artist_id'], ''),
            'year': al['release_year']
        })

    sort_options = ["By Title", "By Artist", "By Year"]

    return render_template('albums.html', albums=albums_context, sort_options=sort_options)


@app.route('/albums/search', methods=['POST'])
def albums_search_sort():
    search_album = request.form.get('search-albums', '').strip().lower()
    sort_albums = request.form.get('sort-albums', '').strip()

    albums = load_albums()
    artists = load_artists()
    artist_dict = {a['artist_id']: a['name'] for a in artists}

    filtered_albums = []
    for al in albums:
        if not search_album or search_album in al['title'].lower():
            filtered_albums.append(al)

    albums_context = []
    for al in filtered_albums:
        albums_context.append({
            'album_id': al['album_id'],
            'title': al['title'],
            'artist_name': artist_dict.get(al['artist_id'], ''),
            'year': al['release_year']
        })

    if sort_albums == "By Title":
        albums_context.sort(key=lambda x: x['title'])
    elif sort_albums == "By Artist":
        albums_context.sort(key=lambda x: x['artist_name'])
    elif sort_albums == "By Year":
        albums_context.sort(key=lambda x: x['year'])

    sort_options = ["By Title", "By Artist", "By Year"]

    return render_template('albums.html', albums=albums_context, sort_options=sort_options)


@app.route('/albums/<int:album_id>')
def album_details(album_id):
    album = find_album_by_id(album_id)
    if not album:
        abort(404)

    artist = find_artist_by_id(album['artist_id'])
    songs = load_songs()

    songs_in_album = []
    for s in songs:
        if s['album_id'] == album_id:
            songs_in_album.append({
                'song_id': s['song_id'],
                'title': s['title'],
                'duration': s['duration']
            })

    album_context = {
        'album_id': album['album_id'],
        'title': album['title'],
        'artist_name': artist['name'] if artist else '',
        'release_year': album['release_year']
    }

    return render_template('album_details.html', album=album_context, songs=songs_in_album)


@app.route('/albums/<int:album_id>/add_to_playlist', methods=['POST'])
def add_album_to_playlist(album_id):
    playlist_id_str = request.form.get('playlist-id', '')
    try:
        playlist_id = int(playlist_id_str)
    except:
        return redirect(url_for('album_details', album_id=album_id))

    playlist = find_playlist_by_id(playlist_id)
    if not playlist:
        return redirect(url_for('album_details', album_id=album_id))

    songs = load_songs()
    playlist_songs = load_playlist_songs()

    album_song_ids = [s['song_id'] for s in songs if s['album_id'] == album_id]
    existing_song_ids = {ps['song_id'] for ps in playlist_songs if ps['playlist_id'] == playlist_id}

    next_id = get_next_playlist_song_id(playlist_songs)
    today = datetime.datetime.now().strftime('%Y-%m-%d')

    for song_id in album_song_ids:
        if song_id not in existing_song_ids:
            playlist_songs.append({
                'playlist_song_id': next_id,
                'playlist_id': playlist_id,
                'song_id': song_id,
                'added_date': today
            })
            next_id += 1

    save_playlist_songs(playlist_songs)

    playlists = load_playlists()
    for pl in playlists:
        if pl['playlist_id'] == playlist_id:
            pl['total_songs'] = sum(1 for ps in playlist_songs if ps['playlist_id'] == playlist_id)
            break
    save_playlists(playlists)

    return redirect(url_for('album_details', album_id=album_id))


@app.route('/artists')
def artists_page():
    artists = load_artists()

    sort_options = ["By Name", "By Genre"]

    artists_sorted = sorted(artists, key=lambda x: x['name'])
    artists_context = []
    for a in artists_sorted:
        artists_context.append({
            'artist_id': a['artist_id'],
            'name': a['name'],
            'genre': a['genre']
        })

    return render_template('artists.html', artists=artists_context, sort_options=sort_options)


@app.route('/artists/search_sort', methods=['POST'])
def artists_search_sort():
    search_artists = request.form.get('search-artists', '').strip().lower()
    artists_sort = request.form.get('artists-sort', '').strip()

    artists = load_artists()

    filtered = []
    for a in artists:
        if not search_artists or search_artists in a['name'].lower():
            filtered.append(a)

    if artists_sort == "By Name":
        filtered.sort(key=lambda x: x['name'])
    elif artists_sort == "By Genre":
        filtered.sort(key=lambda x: x['genre'])

    artists_context = []
    for a in filtered:
        artists_context.append({
            'artist_id': a['artist_id'],
            'name': a['name'],
            'genre': a['genre']
        })

    sort_options = ["By Name", "By Genre"]

    return render_template('artists.html', artists=artists_context, sort_options=sort_options)


@app.route('/artists/<int:artist_id>')
def artist_profile(artist_id):
    artist = find_artist_by_id(artist_id)
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

    if not genres:
        return render_template('genres.html', genres=[], songs=[], artists=[])

    selected_genre = genres[0]['genre_name']

    songs_filtered = [
        {
            'song_id': s['song_id'],
            'title': s['title'],
            'artist_name': get_artist_name(s['artist_id'])
        } for s in songs if s['genre'] == selected_genre
    ]

    artists_filtered = [
        {
            'artist_id': a['artist_id'],
            'name': a['name']
        } for a in artists if a['genre'] == selected_genre
    ]

    return render_template('genres.html', genres=genres, songs=songs_filtered, artists=artists_filtered)


@app.route('/genres/select', methods=['POST'])
def select_genre():
    genres = load_genres()
    songs = load_songs()
    artists = load_artists()

    selected_genre = request.form.get('select-genre', '')
    if not selected_genre:
        if genres:
            selected_genre = genres[0]['genre_name']

    songs_filtered = [
        {
            'song_id': s['song_id'],
            'title': s['title'],
            'artist_name': get_artist_name(s['artist_id'])
        } for s in songs if s['genre'] == selected_genre
    ]

    artists_filtered = [
        {
            'artist_id': a['artist_id'],
            'name': a['name']
        } for a in artists if a['genre'] == selected_genre
    ]

    return render_template('genres.html', genres=genres, songs=songs_filtered, artists=artists_filtered)


if __name__ == '__main__':
    app.run(port=5000, debug=True)
