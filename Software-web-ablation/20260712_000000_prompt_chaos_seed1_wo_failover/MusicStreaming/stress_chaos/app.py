from flask import Flask, render_template, request, redirect, url_for, abort
import os
from datetime import date

app = Flask(__name__)

DATA_DIR = 'data'

# Utility functions to load data from files

def load_songs():
    songs = []
    try:
        with open(os.path.join(DATA_DIR, 'songs.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 8:
                    continue
                song_id = int(parts[0])
                title = parts[1]
                artist_id = int(parts[2])
                album_id = int(parts[3])
                genre = parts[4]
                duration = int(parts[5])
                release_date = parts[6]
                play_count = int(parts[7])
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
    except FileNotFoundError:
        pass
    return songs


def load_artists():
    artists = []
    try:
        with open(os.path.join(DATA_DIR, 'artists.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 5:
                    continue
                artist_id = int(parts[0])
                name = parts[1]
                genre = parts[2]
                country = parts[3]
                formation_year = int(parts[4])
                artists.append({
                    'artist_id': artist_id,
                    'name': name,
                    'genre': genre,
                    'country': country,
                    'formation_year': formation_year
                })
    except FileNotFoundError:
        pass
    return artists


def load_albums():
    albums = []
    try:
        with open(os.path.join(DATA_DIR, 'albums.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 6:
                    continue
                album_id = int(parts[0])
                title = parts[1]
                artist_id = int(parts[2])
                release_year = int(parts[3])
                total_songs = int(parts[4])
                genre = parts[5]
                albums.append({
                    'album_id': album_id,
                    'title': title,
                    'artist_id': artist_id,
                    'release_year': release_year,
                    'total_songs': total_songs,
                    'genre': genre
                })
    except FileNotFoundError:
        pass
    return albums


def load_genres():
    genres = []
    try:
        with open(os.path.join(DATA_DIR, 'genres.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 3:
                    continue
                genre_id = int(parts[0])
                genre_name = parts[1]
                description = parts[2]
                genres.append({
                    'genre_id': genre_id,
                    'genre_name': genre_name,
                    'description': description
                })
    except FileNotFoundError:
        pass
    return genres


def load_playlists():
    playlists = []
    try:
        with open(os.path.join(DATA_DIR, 'playlists.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 5:
                    continue
                playlist_id = int(parts[0])
                title = parts[1]
                description = parts[2]
                creation_date = parts[3]
                total_songs = int(parts[4])
                playlists.append({
                    'playlist_id': playlist_id,
                    'title': title,
                    'description': description,
                    'creation_date': creation_date,
                    'total_songs': total_songs
                })
    except FileNotFoundError:
        pass
    return playlists


def load_playlist_songs():
    playlist_songs = []
    try:
        with open(os.path.join(DATA_DIR, 'playlist_songs.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 4:
                    continue
                playlist_song_id = int(parts[0])
                playlist_id = int(parts[1])
                song_id = int(parts[2])
                added_date = parts[3]
                playlist_songs.append({
                    'playlist_song_id': playlist_song_id,
                    'playlist_id': playlist_id,
                    'song_id': song_id,
                    'added_date': added_date
                })
    except FileNotFoundError:
        pass
    return playlist_songs


def save_playlists(playlists):
    try:
        with open(os.path.join(DATA_DIR, 'playlists.txt'), 'w', encoding='utf-8') as f:
            for p in playlists:
                line = f"{p['playlist_id']}|{p['title']}|{p['description']}|{p['creation_date']}|{p['total_songs']}\n"
                f.write(line)
    except Exception:
        pass


def save_playlist_songs(playlist_songs):
    try:
        with open(os.path.join(DATA_DIR, 'playlist_songs.txt'), 'w', encoding='utf-8') as f:
            for ps in playlist_songs:
                line = f"{ps['playlist_song_id']}|{ps['playlist_id']}|{ps['song_id']}|{ps['added_date']}\n"
                f.write(line)
    except Exception:
        pass


def get_artist_by_id(artist_id):
    artists = load_artists()
    for artist in artists:
        if artist['artist_id'] == artist_id:
            return artist
    return None


def get_album_by_id(album_id):
    albums = load_albums()
    for album in albums:
        if album['album_id'] == album_id:
            return album
    return None


def get_song_by_id(song_id):
    songs = load_songs()
    for song in songs:
        if song['song_id'] == song_id:
            return song
    return None


def get_genre_by_name(genre_name):
    genres = load_genres()
    for genre in genres:
        if genre['genre_name'].lower() == genre_name.lower():
            return genre
    return None


@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard_page'))


@app.route('/dashboard')
def dashboard_page():
    # featured_songs: list of dict {song_id: int, title: str, artist_name: str, album_name: str, duration: int}
    # trending_artists: list of dict {artist_id: int, name: str}
    songs = load_songs()
    artists = load_artists()
    albums = load_albums()

    # Let's pick featured songs as first 5 songs for simplicity
    featured_songs = []
    for song in songs[:5]:
        artist = get_artist_by_id(song['artist_id'])
        album = get_album_by_id(song['album_id'])
        if artist and album:
            featured_songs.append({
                'song_id': song['song_id'],
                'title': song['title'],
                'artist_name': artist['name'],
                'album_name': album['title'],
                'duration': song['duration']
            })

    # Trending artists - choose artists with highest total play counts of their songs (top 5)
    artist_play_count = {}
    for song in songs:
        artist_play_count[song['artist_id']] = artist_play_count.get(song['artist_id'], 0) + song['play_count']

    trending_artists_sorted = sorted(artist_play_count.items(), key=lambda x: x[1], reverse=True)[:5]
    trending_artists = []
    for artist_id, _ in trending_artists_sorted:
        artist = get_artist_by_id(artist_id)
        if artist:
            trending_artists.append({'artist_id': artist['artist_id'], 'name': artist['name']})

    return render_template('dashboard.html', featured_songs=featured_songs, trending_artists=trending_artists)


@app.route('/songs', methods=['GET', 'POST'])
def song_catalog_page():
    songs = load_songs()
    artists = load_artists()
    albums = load_albums()
    genres = [genre['genre_name'] for genre in load_genres()]

    search_query = ''
    selected_genre = None

    if request.method == 'POST':
        search_query = request.form.get('search', '').strip()
        selected_genre = request.form.get('genre', None)
    else:
        search_query = request.args.get('search', '').strip()
        selected_genre = request.args.get('genre', None)

    # Filter songs by search_query and genre
    filtered_songs = []
    for song in songs:
        artist = get_artist_by_id(song['artist_id'])
        album = get_album_by_id(song['album_id'])
        if not artist or not album:
            continue
        # Filter genre if selected
        if selected_genre and selected_genre != '' and song['genre'].lower() != selected_genre.lower():
            continue
        # Filter by search
        if search_query:
            if search_query.lower() not in song['title'].lower() and search_query.lower() not in artist['name'].lower() and search_query.lower() not in album['title'].lower():
                continue
        filtered_songs.append({
            'song_id': song['song_id'],
            'title': song['title'],
            'artist_name': artist['name'],
            'album_name': album['title'],
            'duration': song['duration'],
            'genre': song['genre']
        })

    return render_template('song_catalog.html', songs=filtered_songs, genres=genres, search_query=search_query, selected_genre=selected_genre)


@app.route('/songs/<int:song_id>')
def song_details_page(song_id):
    song = get_song_by_id(song_id)
    if not song:
        abort(404)
    artist = get_artist_by_id(song['artist_id'])
    album = get_album_by_id(song['album_id'])
    if not artist or not album:
        abort(404)

    song_dict = {
        'song_id': song['song_id'],
        'title': song['title'],
        'artist_id': artist['artist_id'],
        'artist_name': artist['name'],
        'album_id': album['album_id'],
        'album_name': album['title'],
        'duration': song['duration'],
        'genre': song['genre'],
        'release_date': song['release_date'],
        'play_count': song['play_count']
    }
    return render_template('song_details.html', song=song_dict)


@app.route('/playlists')
def playlists_page():
    playlists = load_playlists()
    # total_songs is available in playlists data already
    playlists_summaries = []
    for p in playlists:
        playlists_summaries.append({
            'playlist_id': p['playlist_id'],
            'title': p['title'],
            'description': p['description'],
            'total_songs': p['total_songs']
        })
    return render_template('playlists.html', playlists=playlists_summaries)


@app.route('/playlists/<int:playlist_id>')
def playlist_details_page(playlist_id):
    playlists = load_playlists()
    playlist = None
    for p in playlists:
        if p['playlist_id'] == playlist_id:
            playlist = p
            break
    if not playlist:
        abort(404)

    playlist_songs_all = load_playlist_songs()
    songs_in_playlist = []
    songs = load_songs()
    artists = load_artists()
    songs_dict = {song['song_id']: song for song in songs}
    artists_dict = {artist['artist_id']: artist for artist in artists}

    for pls in playlist_songs_all:
        if pls['playlist_id'] == playlist_id:
            song = songs_dict.get(pls['song_id'])
            if not song:
                continue
            artist = artists_dict.get(song['artist_id'])
            if not artist:
                continue
            songs_in_playlist.append({
                'song_id': song['song_id'],
                'title': song['title'],
                'artist_name': artist['name'],
                'duration': song['duration']
            })

    playlist_summary = {
        'playlist_id': playlist['playlist_id'],
        'title': playlist['title'],
        'description': playlist['description']
    }

    return render_template('playlist_details.html', playlist=playlist_summary, songs_in_playlist=songs_in_playlist)


@app.route('/playlists/create', methods=['GET', 'POST'])
def create_playlist_page():
    if request.method == 'POST':
        playlist_name = request.form.get('playlist_name', '').strip()
        playlist_description = request.form.get('playlist_description', '').strip()

        if not playlist_name:
            # We reload page with previous input to show form inputs
            return render_template('create_playlist.html', playlist_name=playlist_name, playlist_description=playlist_description)

        playlists = load_playlists()
        new_id = 1
        if playlists:
            new_id = max(p['playlist_id'] for p in playlists) + 1

        today_str = date.today().isoformat()
        new_playlist = {
            'playlist_id': new_id,
            'title': playlist_name,
            'description': playlist_description,
            'creation_date': today_str,
            'total_songs': 0
        }

        playlists.append(new_playlist)
        save_playlists(playlists)

        return redirect(url_for('playlists_page'))

    # GET request
    return render_template('create_playlist.html')


@app.route('/albums', methods=['GET', 'POST'])
def albums_page():
    albums = load_albums()
    artists = load_artists()

    search_query = ''
    sort_option = ''

    if request.method == 'POST':
        search_query = request.form.get('search', '').strip()
        sort_option = request.form.get('sort', '')
    else:
        search_query = request.args.get('search', '').strip()
        sort_option = request.args.get('sort', '')

    # Filter albums by search_query
    artists_dict = {artist['artist_id']: artist for artist in artists}
    filtered_albums = []
    for album in albums:
        artist = artists_dict.get(album['artist_id'])
        if not artist:
            continue
        if search_query:
            if search_query.lower() not in album['title'].lower() and search_query.lower() not in artist['name'].lower():
                continue
        filtered_albums.append({
            'album_id': album['album_id'],
            'title': album['title'],
            'artist_name': artist['name'],
            'release_year': album['release_year'],
            'genre': album['genre']
        })

    # Sort filtered albums by sort_option
    if sort_option.lower() == 'title':
        filtered_albums.sort(key=lambda x: x['title'].lower())
    elif sort_option.lower() == 'artist':
        filtered_albums.sort(key=lambda x: x['artist_name'].lower())
    elif sort_option.lower() == 'year':
        filtered_albums.sort(key=lambda x: x['release_year'])

    return render_template('albums.html', albums=filtered_albums, search_query=search_query, sort_option=sort_option)


@app.route('/albums/<int:album_id>')
def album_details_page(album_id):
    album = None
    albums = load_albums()
    for a in albums:
        if a['album_id'] == album_id:
            album = a
            break
    if not album:
        abort(404)

    artist = get_artist_by_id(album['artist_id'])
    if not artist:
        abort(404)

    songs = load_songs()
    songs_in_album = []
    for song in songs:
        if song['album_id'] == album_id:
            songs_in_album.append({
                'song_id': song['song_id'],
                'title': song['title'],
                'duration': song['duration']
            })

    album_info = {
        'album_id': album['album_id'],
        'title': album['title'],
        'artist_name': artist['name'],
        'release_year': album['release_year']
    }

    return render_template('album_details.html', album=album_info, songs_in_album=songs_in_album)


@app.route('/artists', methods=['GET', 'POST'])
def artists_page():
    artists = load_artists()

    search_query = ''
    sort_option = ''

    if request.method == 'POST':
        search_query = request.form.get('search', '').strip()
        sort_option = request.form.get('sort', '')
    else:
        search_query = request.args.get('search', '').strip()
        sort_option = request.args.get('sort', '')

    filtered_artists = []
    for artist in artists:
        if search_query:
            if search_query.lower() not in artist['name'].lower() and search_query.lower() not in artist['genre'].lower():
                continue
        filtered_artists.append(artist)

    if sort_option.lower() == 'name':
        filtered_artists.sort(key=lambda x: x['name'].lower())
    elif sort_option.lower() == 'genre':
        filtered_artists.sort(key=lambda x: x['genre'].lower())

    return render_template('artists.html', artists=filtered_artists, search_query=search_query, sort_option=sort_option)


@app.route('/artists/<int:artist_id>')
def artist_profile_page(artist_id):
    artist = get_artist_by_id(artist_id)
    if not artist:
        abort(404)

    songs_all = load_songs()
    songs_by_artist = []
    albums = load_albums()
    albums_dict = {album['album_id']: album for album in albums}
    for song in songs_all:
        if song['artist_id'] == artist_id:
            album_title = albums_dict.get(song['album_id'], {}).get('title', '')
            songs_by_artist.append({
                'song_id': song['song_id'],
                'title': song['title'],
                'album_name': album_title,
                'duration': song['duration']
            })

    return render_template('artist_profile.html', artist=artist, songs_by_artist=songs_by_artist)


@app.route('/genres', methods=['GET', 'POST'])
def genres_page():
    genres = load_genres()
    songs = load_songs()
    artists = load_artists()

    selected_genre = None

    if request.method == 'POST':
        selected_genre = request.form.get('select_genre', None)
    else:
        selected_genre = request.args.get('select_genre', None)

    genre_songs = []
    genre_artists = []

    if selected_genre:
        # Find genre object case-insensitive
        selected_genre_obj = None
        for g in genres:
            if g['genre_name'].lower() == selected_genre.lower():
                selected_genre_obj = g
                break

        if selected_genre_obj:
            # Filter songs in genre
            for song in songs:
                if song['genre'].lower() == selected_genre_obj['genre_name'].lower():
                    artist = get_artist_by_id(song['artist_id'])
                    if artist:
                        genre_songs.append({
                            'song_id': song['song_id'],
                            'title': song['title'],
                            'artist_name': artist['name'],
                            'duration': song['duration']
                        })
            # Filter artists in genre
            for artist in artists:
                if artist['genre'].lower() == selected_genre_obj['genre_name'].lower():
                    genre_artists.append({
                        'artist_id': artist['artist_id'],
                        'name': artist['name']
                    })

    return render_template('genres.html', genres=genres, selected_genre=selected_genre,
                           genre_songs=genre_songs, genre_artists=genre_artists)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
