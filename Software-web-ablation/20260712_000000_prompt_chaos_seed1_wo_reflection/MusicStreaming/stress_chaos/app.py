from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_for_flash_messages'

DATA_DIR = 'data'

# Utility functions to load data from files

def load_songs():
    songs = []
    path = os.path.join(DATA_DIR, 'songs.txt')
    if not os.path.exists(path):
        return songs
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) < 8:
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
            except Exception:
                continue
    return songs


def load_artists():
    artists = []
    path = os.path.join(DATA_DIR, 'artists.txt')
    if not os.path.exists(path):
        return artists
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) < 5:
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
            except Exception:
                continue
    return artists


def load_albums():
    albums = []
    path = os.path.join(DATA_DIR, 'albums.txt')
    if not os.path.exists(path):
        return albums
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) < 6:
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
            except Exception:
                continue
    return albums


def load_genres():
    genres = []
    path = os.path.join(DATA_DIR, 'genres.txt')
    if not os.path.exists(path):
        return genres
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) < 3:
                continue
            try:
                genre = {
                    'genre_id': int(parts[0]),
                    'genre_name': parts[1],
                    'description': parts[2]
                }
                genres.append(genre)
            except Exception:
                continue
    return genres


def load_playlists():
    playlists = []
    path = os.path.join(DATA_DIR, 'playlists.txt')
    if not os.path.exists(path):
        return playlists
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) < 5:
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
            except Exception:
                continue
    return playlists


def load_playlist_songs():
    playlist_songs = []
    path = os.path.join(DATA_DIR, 'playlist_songs.txt')
    if not os.path.exists(path):
        return playlist_songs
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) < 4:
                continue
            try:
                psong = {
                    'playlist_song_id': int(parts[0]),
                    'playlist_id': int(parts[1]),
                    'song_id': int(parts[2]),
                    'added_date': parts[3]
                }
                playlist_songs.append(psong)
            except Exception:
                continue
    return playlist_songs


def save_playlists(playlists):
    path = os.path.join(DATA_DIR, 'playlists.txt')
    lines = []
    for pl in playlists:
        line = f"{pl['playlist_id']}|{pl['title']}|{pl['description']}|{pl['creation_date']}|{pl['total_songs']}"
        lines.append(line)
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n')


def save_playlist_songs(playlist_songs):
    path = os.path.join(DATA_DIR, 'playlist_songs.txt')
    lines = []
    for pls in playlist_songs:
        line = f"{pls['playlist_song_id']}|{pls['playlist_id']}|{pls['song_id']}|{pls['added_date']}"
        lines.append(line)
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n')


# Helper functions

def get_artist_by_id(artist_id, artists):
    for artist in artists:
        if artist['artist_id'] == artist_id:
            return artist
    return None


def get_album_by_id(album_id, albums):
    for album in albums:
        if album['album_id'] == album_id:
            return album
    return None


def get_song_by_id(song_id, songs):
    for song in songs:
        if song['song_id'] == song_id:
            return song
    return None


def get_playlist_by_id(playlist_id, playlists):
    for pl in playlists:
        if pl['playlist_id'] == playlist_id:
            return pl
    return None


def get_next_id(items, key):
    if not items:
        return 1
    return max(item[key] for item in items) + 1


# Routes implementation

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard_page'))


@app.route('/dashboard')
def dashboard_page():
    songs = load_songs()
    artists = load_artists()

    # Featured songs: could be top 5 by play_count
    top_songs = sorted(songs, key=lambda x: x['play_count'], reverse=True)[:5]
    featured_songs = []
    for song in top_songs:
        artist = get_artist_by_id(song['artist_id'], artists)
        featured_songs.append({
            'song_id': song['song_id'],
            'title': song['title'],
            'artist_name': artist['name'] if artist else 'Unknown',
            'duration': song['duration']
        })

    # Trending artists: top 5 by some metric, here pick top 5 by total play_count aggregated
    artist_play_counts = {}
    for song in songs:
        artist_play_counts[song['artist_id']] = artist_play_counts.get(song['artist_id'], 0) + song['play_count']
    trending_artists_sorted = sorted(artist_play_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    trending_artists = []
    for artist_id, _ in trending_artists_sorted:
        artist = get_artist_by_id(artist_id, artists)
        if artist:
            trending_artists.append({'artist_id': artist['artist_id'], 'name': artist['name']})

    return render_template('dashboard.html', featured_songs=featured_songs, trending_artists=trending_artists)


@app.route('/songs', methods=['GET', 'POST'])
def song_catalog_page():
    songs = load_songs()
    artists = load_artists()
    albums = load_albums()
    genres_data = load_genres()
    genres = [g['genre_name'] for g in genres_data]

    search_query = ''
    selected_genre = None

    if request.method == 'POST':
        # From POST expect search_query and possibly genre filter
        search_query = request.form.get('search_query', '').strip()
        selected_genre = request.form.get('selected_genre')
    else:
        search_query = request.args.get('search_query', '').strip()
        selected_genre = request.args.get('selected_genre')

    filtered_songs = []
    for song in songs:
        artist = get_artist_by_id(song['artist_id'], artists)
        album = get_album_by_id(song['album_id'], albums)

        if selected_genre and selected_genre != '' and song['genre'] != selected_genre:
            continue
        if search_query and search_query.lower() not in song['title'].lower():
            continue

        filtered_songs.append({
            'song_id': song['song_id'],
            'title': song['title'],
            'artist_name': artist['name'] if artist else 'Unknown',
            'album_name': album['title'] if album else 'Unknown',
            'genre': song['genre'],
            'duration': song['duration']
        })

    return render_template('song_catalog.html', songs=filtered_songs, genres=genres, search_query=search_query, selected_genre=selected_genre)


@app.route('/songs/<int:song_id>')
def song_details_page(song_id):
    songs = load_songs()
    artists = load_artists()
    albums = load_albums()

    song = get_song_by_id(song_id, songs)
    if not song:
        flash('Song not found.', 'error')
        return redirect(url_for('song_catalog_page'))

    artist = get_artist_by_id(song['artist_id'], artists)
    album = get_album_by_id(song['album_id'], albums)

    context_song = {
        'song_id': song['song_id'],
        'title': song['title'],
        'artist_name': artist['name'] if artist else 'Unknown',
        'album_name': album['title'] if album else 'Unknown',
        'duration': song['duration']
    }

    artist_id = artist['artist_id'] if artist else None

    return render_template('song_details.html', song=context_song, artist_id=artist_id)


@app.route('/playlists')
def playlists_page():
    playlists = load_playlists()

    # Calculate total songs per playlist by count from playlist_songs
    playlist_songs = load_playlist_songs()
    total_songs_map = {pl['playlist_id']: 0 for pl in playlists}
    for pls in playlist_songs:
        if pls['playlist_id'] in total_songs_map:
            total_songs_map[pls['playlist_id']] += 1

    playlist_context = []
    for pl in playlists:
        playlist_context.append({
            'playlist_id': pl['playlist_id'],
            'title': pl['title'],
            'description': pl['description'],
            'total_songs': total_songs_map.get(pl['playlist_id'], 0)
        })

    return render_template('playlists.html', playlists=playlist_context)


@app.route('/playlists/create', methods=['GET', 'POST'])
def create_playlist_page():
    if request.method == 'GET':
        return render_template('create_playlist.html')

    # POST: create new playlist
    title = request.form.get('playlist_name', '').strip()
    description = request.form.get('playlist_description', '').strip()

    if not title:
        flash('Playlist name is required.', 'error')
        return redirect(url_for('create_playlist_page'))

    playlists = load_playlists()
    existing_titles = {pl['title'].lower() for pl in playlists}
    if title.lower() in existing_titles:
        flash('A playlist with that name already exists.', 'error')
        return redirect(url_for('create_playlist_page'))

    new_id = get_next_id(playlists, 'playlist_id')
    creation_date = datetime.now().strftime('%Y-%m-%d')

    new_playlist = {
        'playlist_id': new_id,
        'title': title,
        'description': description,
        'creation_date': creation_date,
        'total_songs': 0
    }

    playlists.append(new_playlist)

    # Save playlists to file
    save_playlists(playlists)

    flash('Playlist created successfully!', 'success')
    return redirect(url_for('playlists_page'))


@app.route('/playlists/<int:playlist_id>')
def playlist_details_page(playlist_id):
    playlists = load_playlists()
    playlist = get_playlist_by_id(playlist_id, playlists)
    if not playlist:
        flash('Playlist not found.', 'error')
        return redirect(url_for('playlists_page'))

    playlist_songs = load_playlist_songs()
    songs = load_songs()
    artists = load_artists()

    songs_in_playlist = []
    for pls in playlist_songs:
        if pls['playlist_id'] == playlist_id:
            song = get_song_by_id(pls['song_id'], songs)
            if song:
                artist = get_artist_by_id(song['artist_id'], artists)
                songs_in_playlist.append({
                    'song_id': song['song_id'],
                    'title': song['title'],
                    'artist_name': artist['name'] if artist else 'Unknown',
                    'duration': song['duration']
                })

    return render_template('playlist_details.html', playlist=playlist, songs_in_playlist=songs_in_playlist)


@app.route('/playlists/<int:playlist_id>/delete', methods=['POST'])
def delete_playlist(playlist_id):
    playlists = load_playlists()
    playlist_songs = load_playlist_songs()

    # Remove playlist
    playlists = [pl for pl in playlists if pl['playlist_id'] != playlist_id]

    # Remove all songs linked to this playlist
    playlist_songs = [pls for pls in playlist_songs if pls['playlist_id'] != playlist_id]

    # Save changes
    save_playlists(playlists)
    save_playlist_songs(playlist_songs)

    flash('Playlist deleted successfully.', 'success')
    return redirect(url_for('playlists_page'))


@app.route('/playlists/<int:playlist_id>/remove_song/<int:song_id>', methods=['POST'])
def remove_song_from_playlist(playlist_id, song_id):
    playlist_songs = load_playlist_songs()
    playlists = load_playlists()

    # Remove the song link from playlist_songs
    playlist_songs = [pls for pls in playlist_songs if not (pls['playlist_id'] == playlist_id and pls['song_id'] == song_id)]

    # Update total_songs in playlist
    for pl in playlists:
        if pl['playlist_id'] == playlist_id:
            pl['total_songs'] = sum(1 for pls in playlist_songs if pls['playlist_id'] == playlist_id)

    save_playlist_songs(playlist_songs)
    save_playlists(playlists)

    flash('Song removed from playlist.', 'success')
    return redirect(url_for('playlist_details_page', playlist_id=playlist_id))


@app.route('/albums')
def album_browse_page():
    albums = load_albums()
    artists = load_artists()

    search_query = request.args.get('search_query', '').strip()
    sort_option = request.args.get('sort_option', '')

    filtered_albums = []
    for album in albums:
        artist = get_artist_by_id(album['artist_id'], artists)
        if search_query and search_query.lower() not in album['title'].lower():
            continue

        filtered_albums.append({
            'album_id': album['album_id'],
            'title': album['title'],
            'artist_name': artist['name'] if artist else 'Unknown',
            'release_year': album['release_year']
        })

    # Sort based on option
    if sort_option == 'title':
        filtered_albums.sort(key=lambda x: x['title'].lower())
    elif sort_option == 'artist':
        filtered_albums.sort(key=lambda x: x['artist_name'].lower())
    elif sort_option == 'year':
        filtered_albums.sort(key=lambda x: x['release_year'])

    return render_template('albums.html', albums=filtered_albums, search_query=search_query, sort_option=sort_option)


@app.route('/albums/<int:album_id>')
def album_details_page(album_id):
    albums = load_albums()
    artists = load_artists()
    songs = load_songs()

    album = get_album_by_id(album_id, albums)
    if not album:
        flash('Album not found.', 'error')
        return redirect(url_for('album_browse_page'))

    artist = get_artist_by_id(album['artist_id'], artists)

    album_songs = []
    for song in songs:
        if song['album_id'] == album_id:
            album_songs.append({
                'song_id': song['song_id'],
                'title': song['title'],
                'duration': song['duration']
            })

    album_context = {
        'album_id': album['album_id'],
        'title': album['title'],
        'artist_name': artist['name'] if artist else 'Unknown',
        'release_year': album['release_year']
    }

    return render_template('album_details.html', album=album_context, album_songs=album_songs)


@app.route('/albums/<int:album_id>/add_to_playlist', methods=['POST'])
def add_album_to_playlist(album_id):
    # This expects a form with playlist_id to add all album songs to that playlist
    playlist_id_str = request.form.get('playlist_id')
    if not playlist_id_str or not playlist_id_str.isdigit():
        flash('Invalid playlist selection.', 'error')
        return redirect(url_for('album_details_page', album_id=album_id))

    playlist_id = int(playlist_id_str)

    playlists = load_playlists()
    playlist_songs = load_playlist_songs()
    songs = load_songs()

    playlist = get_playlist_by_id(playlist_id, playlists)
    if not playlist:
        flash('Playlist not found.', 'error')
        return redirect(url_for('album_details_page', album_id=album_id))

    # Find all songs of the album
    album_songs = [song for song in songs if song['album_id'] == album_id]

    # Determine existing song ids in playlist to avoid duplicates
    existing_song_ids = {pls['song_id'] for pls in playlist_songs if pls['playlist_id'] == playlist_id}

    # Create new playlist_song entries for songs not already in the playlist
    next_id = get_next_id(playlist_songs, 'playlist_song_id')
    added_yes = False
    for song in album_songs:
        if song['song_id'] not in existing_song_ids:
            playlist_songs.append({
                'playlist_song_id': next_id,
                'playlist_id': playlist_id,
                'song_id': song['song_id'],
                'added_date': datetime.now().strftime('%Y-%m-%d')
            })
            next_id += 1
            added_yes = True

    if added_yes:
        # Update playlist total songs
        playlist['total_songs'] = sum(1 for pls in playlist_songs if pls['playlist_id'] == playlist_id)

        save_playlist_songs(playlist_songs)
        save_playlists(playlists)

        flash(f'All songs from album added to playlist "{playlist["title"]}".', 'success')
    else:
        flash('No new songs to add; all album songs already in the playlist.', 'info')

    return redirect(url_for('album_details_page', album_id=album_id))


@app.route('/artists')
def artist_profile_page():
    artists = load_artists()

    search_query = request.args.get('search_query', '').strip()
    sort_option = request.args.get('sort_option', '')

    filtered_artists = []
    for artist in artists:
        if search_query and search_query.lower() not in artist['name'].lower():
            continue
        filtered_artists.append({
            'artist_id': artist['artist_id'],
            'name': artist['name'],
            'genre': artist['genre']
        })

    # sort
    if sort_option == 'name':
        filtered_artists.sort(key=lambda x: x['name'].lower())
    elif sort_option == 'genre':
        filtered_artists.sort(key=lambda x: x['genre'].lower())

    return render_template('artists.html', artists=filtered_artists, search_query=search_query, sort_option=sort_option)


@app.route('/artists/<int:artist_id>')
def artist_details_page(artist_id):
    artists = load_artists()
    songs = load_songs()
    albums = load_albums()

    artist = get_artist_by_id(artist_id, artists)
    if not artist:
        flash('Artist not found.', 'error')
        return redirect(url_for('artist_profile_page'))

    artist_songs = []
    for song in songs:
        if song['artist_id'] == artist_id:
            album = get_album_by_id(song['album_id'], albums)
            artist_songs.append({
                'song_id': song['song_id'],
                'title': song['title'],
                'album_name': album['title'] if album else 'Unknown',
                'duration': song['duration']
            })

    return render_template('artist_details.html', artist=artist, artist_songs=artist_songs)


@app.route('/genres')
def genre_exploration_page():
    genres = load_genres()
    songs = load_songs()
    artists = load_artists()

    selected_genre = request.args.get('selected_genre')

    genre_songs = []
    genre_artists = []
    if selected_genre:
        # Filter songs and artists by genre
        genre_songs_temp = [song for song in songs if song['genre'] == selected_genre]
        genre_songs = []
        for song in genre_songs_temp:
            artist = get_artist_by_id(song['artist_id'], artists)
            genre_songs.append({
                'song_id': song['song_id'],
                'title': song['title'],
                'artist_name': artist['name'] if artist else 'Unknown',
                'duration': song['duration']
            })

        # Extract unique artists for the genre
        artist_ids = set(song['artist_id'] for song in genre_songs_temp)
        genre_artists = []
        for aid in artist_ids:
            artist = get_artist_by_id(aid, artists)
            if artist:
                genre_artists.append({'artist_id': artist['artist_id'], 'name': artist['name']})
    else:
        selected_genre = None

    return render_template('genres.html', genres=genres, selected_genre=selected_genre, genre_songs=genre_songs, genre_artists=genre_artists)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
