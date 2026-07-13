from flask import Flask, render_template, request, jsonify, redirect, url_for
from datetime import datetime
import os

app = Flask(__name__)
DATA_DIR = 'data'

# Utility functions to read and write data files

def read_songs():
    '''Reads songs.txt and returns list of song dicts.'''
    songs_path = os.path.join(DATA_DIR, 'songs.txt')
    songs = []
    if not os.path.exists(songs_path):
        return songs
    with open(songs_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 8:
                continue
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
    return songs


def write_songs(songs):
    '''Writes list of song dicts back to songs.txt.'''
    songs_path = os.path.join(DATA_DIR, 'songs.txt')
    with open(songs_path, 'w', encoding='utf-8') as f:
        for s in songs:
            line = f"{s['song_id']}|{s['title']}|{s['artist_id']}|{s['album_id']}|{s['genre']}|{s['duration']}|{s['release_date']}|{s['play_count']}\n"
            f.write(line)


def read_artists():
    '''Reads artists.txt and returns list of artist dicts.'''
    artists_path = os.path.join(DATA_DIR, 'artists.txt')
    artists = []
    if not os.path.exists(artists_path):
        return artists
    with open(artists_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 5:
                continue
            artist = {
                'artist_id': int(parts[0]),
                'name': parts[1],
                'genre': parts[2],
                'country': parts[3],
                'formation_year': int(parts[4])
            }
            artists.append(artist)
    return artists


def read_albums():
    '''Reads albums.txt and returns list of album dicts.'''
    albums_path = os.path.join(DATA_DIR, 'albums.txt')
    albums = []
    if not os.path.exists(albums_path):
        return albums
    with open(albums_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 6:
                continue
            album = {
                'album_id': int(parts[0]),
                'title': parts[1],
                'artist_id': int(parts[2]),
                'release_year': int(parts[3]),
                'total_songs': int(parts[4]),
                'genre': parts[5]
            }
            albums.append(album)
    return albums


def read_genres():
    '''Reads genres.txt and returns list of genre dicts.'''
    genres_path = os.path.join(DATA_DIR, 'genres.txt')
    genres = []
    if not os.path.exists(genres_path):
        return genres
    with open(genres_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 3:
                continue
            genre = {
                'genre_id': int(parts[0]),
                'genre_name': parts[1],
                'description': parts[2]
            }
            genres.append(genre)
    return genres


def read_playlists():
    '''Reads playlists.txt and returns list of playlist dicts.'''
    playlists_path = os.path.join(DATA_DIR, 'playlists.txt')
    playlists = []
    if not os.path.exists(playlists_path):
        return playlists
    with open(playlists_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 5:
                continue
            playlist = {
                'playlist_id': int(parts[0]),
                'title': parts[1],
                'description': parts[2],
                'creation_date': parts[3],
                'total_songs': int(parts[4])
            }
            playlists.append(playlist)
    return playlists


def write_playlists(playlists):
    '''Writes playlists list back to playlists.txt.'''
    playlists_path = os.path.join(DATA_DIR, 'playlists.txt')
    with open(playlists_path, 'w', encoding='utf-8') as f:
        for p in playlists:
            line = f"{p['playlist_id']}|{p['title']}|{p['description']}|{p['creation_date']}|{p['total_songs']}\n"
            f.write(line)


def read_playlist_songs():
    '''Reads playlist_songs.txt and returns list of playlist_song dicts.'''
    pls_path = os.path.join(DATA_DIR, 'playlist_songs.txt')
    plsongs = []
    if not os.path.exists(pls_path):
        return plsongs
    with open(pls_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 4:
                continue
            pls = {
                'playlist_song_id': int(parts[0]),
                'playlist_id': int(parts[1]),
                'song_id': int(parts[2]),
                'added_date': parts[3]
            }
            plsongs.append(pls)
    return plsongs


def write_playlist_songs(plsongs):
    '''Writes playlist_songs list back to playlist_songs.txt.'''
    pls_path = os.path.join(DATA_DIR, 'playlist_songs.txt')
    with open(pls_path, 'w', encoding='utf-8') as f:
        for pls in plsongs:
            line = f"{pls['playlist_song_id']}|{pls['playlist_id']}|{pls['song_id']}|{pls['added_date']}\n"
            f.write(line)


# Helper functions

def get_song_by_id(song_id, songs=None):
    '''Returns song dict by song_id or None if not found.'''
    if songs is None:
        songs = read_songs()
    for s in songs:
        if s['song_id'] == song_id:
            return s
    return None


def get_artist_by_id(artist_id, artists=None):
    '''Returns artist dict by artist_id or None if not found.'''
    if artists is None:
        artists = read_artists()
    for a in artists:
        if a['artist_id'] == artist_id:
            return a
    return None


def get_album_by_id(album_id, albums=None):
    '''Returns album dict by album_id or None if not found.'''
    if albums is None:
        albums = read_albums()
    for a in albums:
        if a['album_id'] == album_id:
            return a
    return None


def get_genre_by_id(genre_id, genres=None):
    '''Returns genre dict by genre_id or None if not found.'''
    if genres is None:
        genres = read_genres()
    for g in genres:
        if g['genre_id'] == genre_id:
            return g
    return None


def get_genre_by_name(genre_name, genres=None):
    '''Returns genre dict by genre_name case-insensitive or None if not found.'''
    if genres is None:
        genres = read_genres()
    lname = genre_name.lower()
    for g in genres:
        if g['genre_name'].lower() == lname:
            return g
    return None


def next_playlist_id(playlists=None):
    '''Returns next playlist_id integer for new playlist.'''
    if playlists is None:
        playlists = read_playlists()
    if not playlists:
        return 1
    return max(p['playlist_id'] for p in playlists) + 1


def next_playlist_song_id(plsongs=None):
    '''Returns next playlist_song_id integer.'''
    if plsongs is None:
        plsongs = read_playlist_songs()
    if not plsongs:
        return 1
    return max(p['playlist_song_id'] for p in plsongs) + 1


# Section 1 Routes Implementation

@app.route('/dashboard', methods=['GET'])
def dashboard():
    '''Render the dashboard page with featured songs and trending artists.'''
    songs = read_songs()
    artists = read_artists()

    # Featured songs: for demo, top 5 songs by play count descending
    featured_songs = sorted(songs, key=lambda s: s['play_count'], reverse=True)[:5]

    # Add artist_name to each featured song for template
    artist_lookup = {a['artist_id']: a['name'] for a in artists}
    for song in featured_songs:
        song['artist_name'] = artist_lookup.get(song['artist_id'], 'Unknown Artist')

    # Trending artists: top 5 artists with most songs or just first 5 as placeholder
    artist_song_count = {a['artist_id']: 0 for a in artists}
    for s in songs:
        if s['artist_id'] in artist_song_count:
            artist_song_count[s['artist_id']] += 1
    # Sort artists by song count descending
    trending_artists = sorted(artists, key=lambda a: artist_song_count.get(a['artist_id'], 0), reverse=True)[:5]

    return render_template('dashboard.html', featured_songs=featured_songs, trending_artists=trending_artists)


@app.route('/songs', methods=['GET'])
def song_catalog():
    '''Song Catalog with optional search and genre filtering.'''
    search = request.args.get('search', '').strip().lower()
    genre_filter = request.args.get('genre', '').strip().lower()

    songs = read_songs()
    genres = read_genres()

    filtered_songs = songs

    if search:
        filtered_songs = [s for s in filtered_songs if search in s['title'].lower()]

    if genre_filter:
        # genre_filter matches song['genre'] (case-insensitive)
        filtered_songs = [s for s in filtered_songs if s['genre'].lower() == genre_filter]

    # Add artist_name to songs for template
    artists = read_artists()
    artist_lookup = {a['artist_id']: a['name'] for a in artists}
    for song in filtered_songs:
        song['artist_name'] = artist_lookup.get(song['artist_id'], 'Unknown Artist')

    return render_template('catalog.html', songs=filtered_songs, genres=genres)


@app.route('/songs/<int:song_id>', methods=['GET'])
def song_details(song_id):
    '''Show details of a single song.'''
    song = get_song_by_id(song_id)
    if not song:
        return "Song not found", 404
    artist = get_artist_by_id(song['artist_id'])
    album = get_album_by_id(song['album_id'])
    return render_template('song_details.html', song=song, artist=artist, album=album)


@app.route('/playlists', methods=['GET'])
def playlists():
    '''Display all playlists.'''
    playlists_list = read_playlists()
    return render_template('playlists.html', playlists=playlists_list)


@app.route('/playlists/<int:playlist_id>', methods=['GET'])
def playlist_details(playlist_id):
    '''Display playlist details and songs.'''
    playlists_list = read_playlists()
    playlist = None
    for p in playlists_list:
        if p['playlist_id'] == playlist_id:
            playlist = p
            break
    if not playlist:
        return "Playlist not found", 404

    playlist_songs = read_playlist_songs()
    songs = read_songs()

    # Find songs in this playlist
    songs_in_playlist = []
    artist_lookup = {a['artist_id']: a['name'] for a in read_artists()}
    for pls in playlist_songs:
        if pls['playlist_id'] == playlist_id:
            song = get_song_by_id(pls['song_id'], songs)
            if song:
                # Add artist_name to song for template
                song['artist_name'] = artist_lookup.get(song['artist_id'], 'Unknown Artist')
                songs_in_playlist.append(song)

    return render_template('playlist_details.html', playlist=playlist, songs=songs_in_playlist)


@app.route('/playlists/create', methods=['GET', 'POST'])
def create_playlist():
    '''GET: show create playlist form; POST: create new playlist and redirect.'''
    if request.method == 'GET':
        return render_template('create_playlist.html')
    else:
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()

        if not title:
            return render_template('create_playlist.html', error='Title is required.')

        playlists_list = read_playlists()
        new_id = next_playlist_id(playlists_list)

        creation_date = datetime.now().strftime('%Y-%m-%d')

        new_playlist = {
            'playlist_id': new_id,
            'title': title,
            'description': description,
            'creation_date': creation_date,
            'total_songs': 0
        }

        playlists_list.append(new_playlist)
        write_playlists(playlists_list)
        return redirect(url_for('playlists'))


@app.route('/albums', methods=['GET'])
def albums():
    '''Album browse page with optional search and sorting.'''
    search = request.args.get('search', '').strip().lower()
    sort = request.args.get('sort', '').strip().lower()

    albums_list = read_albums()
    artists_list = read_artists()

    # Filter albums by search in album title or artist name
    if search:
        filtered = []
        for alb in albums_list:
            artist = get_artist_by_id(alb['artist_id'], artists_list)
            artist_name = artist['name'].lower() if artist else ''
            if search in alb['title'].lower() or search in artist_name:
                filtered.append(alb)
        albums_list = filtered

    # Sort albums by criteria
    if sort == 'title':
        albums_list.sort(key=lambda a: a['title'].lower())
    elif sort == 'artist':
        albums_list.sort(key=lambda a: (get_artist_by_id(a['artist_id'], artists_list)['name'].lower() if get_artist_by_id(a['artist_id'], artists_list) else ''))
    elif sort == 'year':
        albums_list.sort(key=lambda a: a['release_year'])

    # Add artist_name to albums for template
    artist_lookup = {a['artist_id']: a['name'] for a in artists_list}
    for album in albums_list:
        album['artist_name'] = artist_lookup.get(album['artist_id'], 'Unknown Artist')

    return render_template('albums.html', albums=albums_list)


@app.route('/albums/<int:album_id>', methods=['GET'])
def album_details(album_id):
    '''Show album details and its songs.'''
    albums_list = read_albums()
    album = None
    for a in albums_list:
        if a['album_id'] == album_id:
            album = a
            break
    if not album:
        return "Album not found", 404

    artist = get_artist_by_id(album['artist_id'])
    songs = read_songs()

    album_songs = [s for s in songs if s['album_id'] == album_id]

    # Add artist_name to each song for template
    artist_lookup = {a['artist_id']: a['name'] for a in read_artists()}
    for song in album_songs:
        song['artist_name'] = artist_lookup.get(song['artist_id'], 'Unknown Artist')

    return render_template('album_details.html', album=album, artist=artist, songs=album_songs)


@app.route('/artists', methods=['GET'])
def artists():
    '''Artist listing with optional search and sorting.'''
    search = request.args.get('search', '').strip().lower()
    sort = request.args.get('sort', '').strip().lower()

    artists_list = read_artists()

    if search:
        artists_list = [a for a in artists_list if search in a['name'].lower()]

    if sort == 'name':
        artists_list.sort(key=lambda a: a['name'].lower())
    elif sort == 'genre':
        artists_list.sort(key=lambda a: a['genre'].lower())

    return render_template('artists.html', artists=artists_list)


@app.route('/artists/<int:artist_id>', methods=['GET'])
def artist_profile(artist_id):
    '''Show individual artist profile, songs, and albums.'''
    artists_list = read_artists()
    artist = get_artist_by_id(artist_id, artists_list)
    if not artist:
        return "Artist not found", 404

    songs_list = read_songs()
    albums_list = read_albums()

    artist_songs = [s for s in songs_list if s['artist_id'] == artist_id]
    artist_albums = [a for a in albums_list if a['artist_id'] == artist_id]

    # Add artist_name to songs (not strictly necessary here but keep consistent)
    for song in artist_songs:
        song['artist_name'] = artist['name']

    return render_template('artist_profile.html', artist=artist, songs=artist_songs, albums=artist_albums)


@app.route('/genres', methods=['GET'])
def genres():
    '''Show genre exploration page, filter songs and artists if genre_id given.'''
    genres_list = read_genres()
    genre_id = request.args.get('genre_id')

    genre = None
    genre_songs = []
    genre_artists = []
    if genre_id:
        try:
            gid = int(genre_id)
            genre = get_genre_by_id(gid, genres_list)
            if genre:
                # Filter songs and artists by genre name
                all_songs = read_songs()
                all_artists = read_artists()

                genre_name_lower = genre['genre_name'].lower()
                genre_songs = [s for s in all_songs if s['genre'].lower() == genre_name_lower]
                genre_artists = [a for a in all_artists if a['genre'].lower() == genre_name_lower]
        except ValueError:
            genre = None

    # Add artist_name to genre_songs for template
    artist_lookup = {a['artist_id']: a['name'] for a in read_artists()}
    for song in genre_songs:
        song['artist_name'] = artist_lookup.get(song['artist_id'], 'Unknown Artist')

    return render_template('genres.html', genres=genres_list, genre=genre, songs=genre_songs, artists=genre_artists)


# Section 2 API Endpoints

@app.route('/playlists/<int:playlist_id>/add_song', methods=['POST'])
def add_song_to_playlist(playlist_id):
    '''Add a song to a playlist.'''
    data = request.get_json() or {}
    song_id = data.get('song_id')
    if not isinstance(song_id, int):
        return jsonify({'success': False, 'message': 'Invalid or missing song_id'}), 400

    playlists_list = read_playlists()
    playlist = None
    for p in playlists_list:
        if p['playlist_id'] == playlist_id:
            playlist = p
            break
    if not playlist:
        return jsonify({'success': False, 'message': 'Playlist not found'}), 404

    song = get_song_by_id(song_id)
    if not song:
        return jsonify({'success': False, 'message': 'Song not found'}), 404

    playlist_songs = read_playlist_songs()
    # Check if song already in playlist
    for pls in playlist_songs:
        if pls['playlist_id'] == playlist_id and pls['song_id'] == song_id:
            return jsonify({'success': False, 'message': 'Song already in playlist'}), 400

    new_pls_id = next_playlist_song_id(playlist_songs)
    added_date = datetime.now().strftime('%Y-%m-%d')
    playlist_songs.append({
        'playlist_song_id': new_pls_id,
        'playlist_id': playlist_id,
        'song_id': song_id,
        'added_date': added_date
    })

    # Update playlist total_songs
    playlist['total_songs'] += 1

    # Write updates
    write_playlist_songs(playlist_songs)
    write_playlists(playlists_list)

    return jsonify({'success': True, 'playlist': playlist})


@app.route('/playlists/<int:playlist_id>/remove_song', methods=['POST'])
def remove_song_from_playlist(playlist_id):
    '''Remove a song from a playlist.'''
    data = request.get_json() or {}
    song_id = data.get('song_id')
    if not isinstance(song_id, int):
        return jsonify({'success': False, 'message': 'Invalid or missing song_id'}), 400

    playlists_list = read_playlists()
    playlist = None
    for p in playlists_list:
        if p['playlist_id'] == playlist_id:
            playlist = p
            break
    if not playlist:
        return jsonify({'success': False, 'message': 'Playlist not found'}), 404

    playlist_songs = read_playlist_songs()

    found = False
    # Remove the song from playlist songs
    new_plsongs = []
    for pls in playlist_songs:
        if pls['playlist_id'] == playlist_id and pls['song_id'] == song_id:
            found = True
            continue
        new_plsongs.append(pls)

    if not found:
        return jsonify({'success': False, 'message': 'Song not found in playlist'}), 404

    # Update total_songs
    playlist['total_songs'] = max(playlist['total_songs'] - 1, 0)

    write_playlist_songs(new_plsongs)
    write_playlists(playlists_list)

    return jsonify({'success': True, 'playlist': playlist})


@app.route('/playlists/<int:playlist_id>/delete', methods=['POST'])
def delete_playlist(playlist_id):
    '''Delete a playlist and its songs.'''
    playlists_list = read_playlists()
    playlist = None
    for p in playlists_list:
        if p['playlist_id'] == playlist_id:
            playlist = p
            break
    if not playlist:
        return jsonify({'success': False, 'message': 'Playlist not found'}), 404

    # Remove playlist entry
    playlists_list = [p for p in playlists_list if p['playlist_id'] != playlist_id]

    playlist_songs = read_playlist_songs()
    playlist_songs = [ps for ps in playlist_songs if ps['playlist_id'] != playlist_id]

    write_playlists(playlists_list)
    write_playlist_songs(playlist_songs)

    return jsonify({'success': True, 'message': 'Playlist deleted'})


@app.route('/songs/<int:song_id>/play', methods=['POST'])
def increment_song_play_count(song_id):
    '''Increment play count for a song.'''
    songs = read_songs()
    song = None
    for s in songs:
        if s['song_id'] == song_id:
            song = s
            break
    if not song:
        return jsonify({'success': False, 'message': 'Song not found'}), 404

    song['play_count'] += 1
    write_songs(songs)

    return jsonify({'success': True, 'play_count': song['play_count']})


if __name__ == '__main__':
    app.run(debug=True)
