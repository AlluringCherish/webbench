from flask import Flask, render_template, redirect, url_for, request, abort
import os
from datetime import date

app = Flask(__name__)

DATA_DIR = 'data'

# Utility data loading functions

def load_songs():
    songs = []
    path = os.path.join(DATA_DIR, 'songs.txt')
    if not os.path.exists(path):
        return songs
    with open(path, encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) == 8:
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
    path = os.path.join(DATA_DIR, 'artists.txt')
    if not os.path.exists(path):
        return artists
    with open(path, encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) == 5:
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
    path = os.path.join(DATA_DIR, 'albums.txt')
    if not os.path.exists(path):
        return albums
    with open(path, encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) == 6:
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
    path = os.path.join(DATA_DIR, 'genres.txt')
    if not os.path.exists(path):
        return genres
    with open(path, encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) >= 2:
                genre_name = parts[1]
                genres.append(genre_name)
    return genres


def load_playlists():
    playlists = []
    path = os.path.join(DATA_DIR, 'playlists.txt')
    if not os.path.exists(path):
        return playlists
    with open(path, encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) == 5:
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


def load_playlist_songs():
    playlist_songs = []
    path = os.path.join(DATA_DIR, 'playlist_songs.txt')
    if not os.path.exists(path):
        return playlist_songs
    with open(path, encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) == 4:
                try:
                    entry = {
                        'playlist_song_id': int(parts[0]),
                        'playlist_id': int(parts[1]),
                        'song_id': int(parts[2]),
                        'added_date': parts[3]
                    }
                    playlist_songs.append(entry)
                except ValueError:
                    continue
    return playlist_songs


def save_playlists(playlists):
    path = os.path.join(DATA_DIR, 'playlists.txt')
    lines = []
    for p in playlists:
        line = f"{p['playlist_id']}|{p['title']}|{p['description']}|{p['creation_date']}|{p['total_songs']}"
        lines.append(line)
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))


def save_playlist_songs(playlist_songs):
    path = os.path.join(DATA_DIR, 'playlist_songs.txt')
    lines = []
    for ps in playlist_songs:
        line = f"{ps['playlist_song_id']}|{ps['playlist_id']}|{ps['song_id']}|{ps['added_date']}"
        lines.append(line)
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))


# Helper functions for data lookups

def find_artist_by_id(artists, artist_id):
    for artist in artists:
        if artist['artist_id'] == artist_id:
            return artist
    return None


def find_album_by_id(albums, album_id):
    for album in albums:
        if album['album_id'] == album_id:
            return album
    return None


def find_playlist_by_id(playlists, playlist_id):
    for p in playlists:
        if p['playlist_id'] == playlist_id:
            return p
    return None


def find_song_by_id(songs, song_id):
    for song in songs:
        if song['song_id'] == song_id:
            return song
    return None


def get_next_playlist_id(playlists):
    if not playlists:
        return 1
    return max(p['playlist_id'] for p in playlists) + 1


def get_next_playlist_song_id(playlist_songs):
    if not playlist_songs:
        return 1
    return max(ps['playlist_song_id'] for ps in playlist_songs) + 1


# Section 1: Flask Routes

@app.route('/')
def root_redirect():
    # Redirect to /dashboard
    return redirect(url_for('dashboard_page'))


@app.route('/dashboard')
def dashboard_page():
    songs = load_songs()
    artists = load_artists()

    # Featured songs: Let's assume featured means top 5 by play_count descending
    songs_sorted = sorted(songs, key=lambda s: s['play_count'], reverse=True)
    featured_songs = []
    for s in songs_sorted[:5]:
        artist = find_artist_by_id(artists, s['artist_id'])
        artist_name = artist['name'] if artist else 'Unknown'
        featured_songs.append({
            'song_id': s['song_id'],
            'title': s['title'],
            'artist_name': artist_name,
            'duration': s['duration']
        })

    # Trending artists: top 5 artists with most total plays across their songs
    artist_plays = {}
    for s in songs:
        artist_plays[s['artist_id']] = artist_plays.get(s['artist_id'], 0) + s['play_count']
    artists_sorted = sorted(artists, key=lambda a: artist_plays.get(a['artist_id'], 0), reverse=True)
    trending_artists = []
    for a in artists_sorted[:5]:
        trending_artists.append({
            'artist_id': a['artist_id'],
            'name': a['name']
        })

    navigation_buttons = {
        'browse_songs_button': url_for('song_catalog_page'),
        'my_playlists_button': url_for('playlists_page'),
        'trending_artists_button': url_for('artists_page')
    }

    return render_template('dashboard.html', featured_songs=featured_songs,
                           trending_artists=trending_artists,
                           navigation_buttons=navigation_buttons)


@app.route('/songs')
def song_catalog_page():
    songs = load_songs()
    artists = load_artists()
    albums = load_albums()
    genres = load_genres()

    search_query = request.args.get('search_query', '').strip()
    selected_genre = request.args.get('selected_genre', '').strip()

    # Filter songs by search and genre
    filtered_songs = []
    for song in songs:
        artist = find_artist_by_id(artists, song['artist_id'])
        album = find_album_by_id(albums, song['album_id'])
        if not artist or not album:
            continue
        if search_query:
            if search_query.lower() not in song['title'].lower() and search_query.lower() not in artist['name'].lower():
                continue
        if selected_genre and selected_genre != '' and song['genre'] != selected_genre:
            continue
        filtered_songs.append({
            'song_id': song['song_id'],
            'title': song['title'],
            'artist_name': artist['name'],
            'album_name': album['title'],
            'genre': song['genre'],
            'duration': song['duration']
        })

    context = {
        'songs': filtered_songs,
        'genres': genres,
        'search_query': search_query,
        'selected_genre': selected_genre
    }
    return render_template('song_catalog.html', **context)


@app.route('/songs/<int:song_id>')
def song_details_page(song_id):
    songs = load_songs()
    artists = load_artists()
    albums = load_albums()

    song = find_song_by_id(songs, song_id)
    if not song:
        abort(404)

    artist = find_artist_by_id(artists, song['artist_id'])
    album = find_album_by_id(albums, song['album_id'])

    artist_name = artist['name'] if artist else 'Unknown'
    album_name = album['title'] if album else 'Unknown'

    artist_profile_url = url_for('artist_profile_page', artist_id=song['artist_id'])

    song_dict = {
        'song_id': song['song_id'],
        'title': song['title'],
        'artist_id': song['artist_id'],
        'artist_name': artist_name,
        'album_id': song['album_id'],
        'album_name': album_name,
        'genre': song['genre'],
        'duration': song['duration'],
        'release_date': song['release_date'],
        'play_count': song['play_count']
    }

    return render_template('song_details.html', song=song_dict, artist_profile_url=artist_profile_url)


@app.route('/playlists')
def playlists_page():
    playlists = load_playlists()

    # Add total_songs already available from file
    navigation_buttons = {
        'create_playlist_button': url_for('create_playlist_page'),
        'back_to_dashboard': url_for('dashboard_page')
    }

    # total_songs is directly from playlists
    return render_template('playlists.html', playlists=playlists, navigation_buttons=navigation_buttons)


@app.route('/playlists/create', methods=['GET'])
def create_playlist_page():
    return render_template('create_playlist.html')


@app.route('/playlists/create', methods=['POST'])
def create_playlist_submit():
    playlist_name = request.form.get('playlist_name', '').strip()
    playlist_description = request.form.get('playlist_description', '').strip()

    if not playlist_name:
        # Invalid data, redirect back to create page or show error
        return redirect(url_for('create_playlist_page'))

    playlists = load_playlists()
    new_id = get_next_playlist_id(playlists)
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


@app.route('/playlists/<int:playlist_id>')
def playlist_details_page(playlist_id):
    playlists = load_playlists()
    playlist = find_playlist_by_id(playlists, playlist_id)
    if not playlist:
        abort(404)

    playlist_songs = load_playlist_songs()
    songs = load_songs()
    artists = load_artists()

    # Find songs in this playlist
    song_entries = []
    for ps in playlist_songs:
        if ps['playlist_id'] == playlist_id:
            song = find_song_by_id(songs, ps['song_id'])
            if not song:
                continue
            artist = find_artist_by_id(artists, song['artist_id'])
            song_entries.append({
                'song_id': song['song_id'],
                'title': song['title'],
                'artist_name': artist['name'] if artist else 'Unknown',
                'duration': song['duration']
            })

    total_songs_count = len(song_entries)

    return render_template('playlist_details.html', playlist=playlist, songs=song_entries, total_songs=total_songs_count)


@app.route('/playlists/<int:playlist_id>/delete', methods=['POST'])
def delete_playlist(playlist_id):
    playlists = load_playlists()
    playlist_songs = load_playlist_songs()

    # Remove playlist if exists
    playlists = [p for p in playlists if p['playlist_id'] != playlist_id]
    # Remove all playlist songs for this playlist
    playlist_songs = [ps for ps in playlist_songs if ps['playlist_id'] != playlist_id]

    save_playlists(playlists)
    save_playlist_songs(playlist_songs)

    return redirect(url_for('playlists_page'))


@app.route('/playlists/<int:playlist_id>/remove_song/<int:song_id>', methods=['POST'])
def remove_song_from_playlist(playlist_id, song_id):
    playlist_songs = load_playlist_songs()
    playlists = load_playlists()

    # Remove the song entry for this playlist
    playlist_songs = [ps for ps in playlist_songs if not (ps['playlist_id'] == playlist_id and ps['song_id'] == song_id)]

    # Save updated playlist_songs
    save_playlist_songs(playlist_songs)

    # Update total_songs in playlists
    for p in playlists:
        if p['playlist_id'] == playlist_id:
            p['total_songs'] = sum(1 for ps in playlist_songs if ps['playlist_id'] == playlist_id)

    save_playlists(playlists)

    return redirect(url_for('playlist_details_page', playlist_id=playlist_id))


@app.route('/albums')
def albums_page():
    albums = load_albums()
    artists = load_artists()

    search_query = request.args.get('search_query', '').strip()
    sort_by = request.args.get('sort_by', '').strip()  # e.g., title, year

    filtered_albums = []
    for album in albums:
        artist = find_artist_by_id(artists, album['artist_id'])
        if not artist:
            continue
        if search_query and search_query.lower() not in album['title'].lower():
            continue
        filtered_albums.append({
            'album_id': album['album_id'],
            'title': album['title'],
            'artist_name': artist['name'],
            'year': album['release_year']
        })

    if sort_by == 'title':
        filtered_albums.sort(key=lambda a: a['title'].lower())
    elif sort_by == 'year':
        filtered_albums.sort(key=lambda a: a['year'])

    return render_template('albums.html', albums=filtered_albums, search_query=search_query, sort_by=sort_by)


@app.route('/albums/<int:album_id>')
def album_details_page(album_id):
    albums = load_albums()
    artists = load_artists()
    songs = load_songs()

    album = find_album_by_id(albums, album_id)
    if not album:
        abort(404)

    artist = find_artist_by_id(artists, album['artist_id'])
    if not artist:
        abort(404)

    # Get songs in album
    album_songs = [s for s in songs if s['album_id'] == album_id]

    song_list = []
    for s in album_songs:
        song_list.append({
            'song_id': s['song_id'],
            'title': s['title'],
            'duration': s['duration']
        })

    album_dict = {
        'album_id': album['album_id'],
        'title': album['title'],
        'artist_id': artist['artist_id'],
        'artist_name': artist['name'],
        'release_year': album['release_year'],
        'total_songs': album['total_songs'],
        'genre': album['genre']
    }

    return render_template('album_details.html', album=album_dict, songs=song_list)


@app.route('/albums/<int:album_id>/add_to_playlist', methods=['POST'])
def add_album_to_playlist(album_id):
    target_playlist_id = request.form.get('target_playlist_id', '').strip()
    if target_playlist_id == '' or not target_playlist_id.isdigit():
        # Invalid playlist id, redirect back to album details
        return redirect(url_for('album_details_page', album_id=album_id))
    target_playlist_id = int(target_playlist_id)

    playlists = load_playlists()
    playlist = find_playlist_by_id(playlists, target_playlist_id)
    if not playlist:
        # Playlist not found
        return redirect(url_for('album_details_page', album_id=album_id))

    songs = load_songs()
    playlist_songs = load_playlist_songs()

    # Get all songs for album
    album_songs = [s for s in songs if s['album_id'] == album_id]

    # Add songs to playlist_songs if not already present
    existing_song_ids = {ps['song_id'] for ps in playlist_songs if ps['playlist_id'] == target_playlist_id}
    next_ps_id = get_next_playlist_song_id(playlist_songs)
    today_str = date.today().isoformat()
    added_count = 0

    for song in album_songs:
        if song['song_id'] not in existing_song_ids:
            playlist_songs.append({
                'playlist_song_id': next_ps_id,
                'playlist_id': target_playlist_id,
                'song_id': song['song_id'],
                'added_date': today_str
            })
            next_ps_id += 1
            added_count += 1

    # Update playlist total_songs
    for p in playlists:
        if p['playlist_id'] == target_playlist_id:
            p['total_songs'] = sum(1 for ps in playlist_songs if ps['playlist_id'] == target_playlist_id)

    save_playlist_songs(playlist_songs)
    save_playlists(playlists)

    return redirect(url_for('album_details_page', album_id=album_id))


@app.route('/artists')
def artists_page():
    artists = load_artists()

    search_query = request.args.get('search_query', '').strip()
    sort_by = request.args.get('sort_by', '').strip()

    filtered_artists = []
    for artist in artists:
        if search_query and search_query.lower() not in artist['name'].lower():
            continue
        filtered_artists.append(artist)

    if sort_by == 'name':
        filtered_artists.sort(key=lambda a: a['name'].lower())
    elif sort_by == 'genre':
        filtered_artists.sort(key=lambda a: a['genre'].lower())
    elif sort_by == 'country':
        filtered_artists.sort(key=lambda a: a['country'].lower())

    return render_template('artists.html', artists=filtered_artists, search_query=search_query, sort_by=sort_by)


@app.route('/artists/<int:artist_id>')
def artist_profile_page(artist_id):
    artists = load_artists()
    songs = load_songs()
    albums = load_albums()

    artist = find_artist_by_id(artists, artist_id)
    if not artist:
        abort(404)

    artist_songs = []
    for song in songs:
        if song['artist_id'] == artist_id:
            album = find_album_by_id(albums, song['album_id'])
            album_name = album['title'] if album else 'Unknown'
            artist_songs.append({
                'song_id': song['song_id'],
                'title': song['title'],
                'album_name': album_name,
                'duration': song['duration']
            })

    return render_template('artist_profile.html', artist=artist, songs=artist_songs)


@app.route('/genres')
def genre_exploration_page():
    genres = load_genres()
    selected_genre = request.args.get('selected_genre', '').strip()

    songs = load_songs()
    artists = load_artists()

    genre_songs = []
    genre_artists = []

    if selected_genre:
        # Get songs for this genre
        genre_songs_raw = [s for s in songs if s['genre'] == selected_genre]

        # Map songs to required dict format
        for s in genre_songs_raw:
            artist = find_artist_by_id(artists, s['artist_id'])
            artist_name = artist['name'] if artist else 'Unknown'
            genre_songs.append({
                'song_id': s['song_id'],
                'title': s['title'],
                'artist_name': artist_name,
                'duration': s['duration']
            })

        # Get unique artists for this genre
        artist_ids = set(s['artist_id'] for s in genre_songs_raw)
        for aid in artist_ids:
            artist = find_artist_by_id(artists, aid)
            if artist:
                genre_artists.append({
                    'artist_id': artist['artist_id'],
                    'name': artist['name']
                })

    navigation_buttons = {
        'back_to_dashboard': url_for('dashboard_page')
    }

    return render_template('genres.html', genres=genres, selected_genre=selected_genre,
                           genre_songs=genre_songs, genre_artists=genre_artists,
                           navigation_buttons=navigation_buttons)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
