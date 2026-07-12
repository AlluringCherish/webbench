from flask import Flask, render_template, redirect, url_for, request, abort
from datetime import datetime
import os

app = Flask(__name__)

DATA_DIR = 'data'

# Helper functions to read/write data

def read_songs():
    songs = []
    path = os.path.join(DATA_DIR, 'songs.txt')
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            fields = line.split('|')
            if len(fields) != 8:
                continue
            song = {}
            try:
                song['song_id'] = int(fields[0])
                song['title'] = fields[1]
                song['artist_id'] = int(fields[2])
                song['album_id'] = int(fields[3])
                song['genre'] = fields[4]
                song['duration'] = int(fields[5])
                song['release_date'] = fields[6]
                song['play_count'] = int(fields[7])
                songs.append(song)
            except ValueError:
                continue
    return songs


def read_artists():
    artists = []
    path = os.path.join(DATA_DIR, 'artists.txt')
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            fields = line.split('|')
            if len(fields) != 5:
                continue
            artist = {}
            try:
                artist['artist_id'] = int(fields[0])
                artist['name'] = fields[1]
                artist['genre'] = fields[2]
                artist['country'] = fields[3]
                artist['formation_year'] = int(fields[4])
                artists.append(artist)
            except ValueError:
                continue
    return artists


def read_albums():
    albums = []
    path = os.path.join(DATA_DIR, 'albums.txt')
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            fields = line.split('|')
            if len(fields) != 6:
                continue
            album = {}
            try:
                album['album_id'] = int(fields[0])
                album['title'] = fields[1]
                album['artist_id'] = int(fields[2])
                album['release_year'] = int(fields[3])
                album['total_songs'] = int(fields[4])
                album['genre'] = fields[5]
                albums.append(album)
            except ValueError:
                continue
    return albums


def read_genres():
    genres = []
    path = os.path.join(DATA_DIR, 'genres.txt')
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            fields = line.split('|')
            if len(fields) != 3:
                continue
            genre = {}
            try:
                genre['genre_id'] = int(fields[0])
                genre['genre_name'] = fields[1]
                genre['description'] = fields[2]
                genres.append(genre)
            except ValueError:
                continue
    return genres


def read_playlists():
    playlists = []
    path = os.path.join(DATA_DIR, 'playlists.txt')
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            fields = line.split('|')
            if len(fields) != 5:
                continue
            playlist = {}
            try:
                playlist['playlist_id'] = int(fields[0])
                playlist['title'] = fields[1]
                playlist['description'] = fields[2]
                playlist['creation_date'] = fields[3]
                playlist['total_songs'] = int(fields[4])
                playlists.append(playlist)
            except ValueError:
                continue
    return playlists


def read_playlist_songs():
    playlist_songs = []
    path = os.path.join(DATA_DIR, 'playlist_songs.txt')
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            fields = line.split('|')
            if len(fields) != 4:
                continue
            pls = {}
            try:
                pls['playlist_song_id'] = int(fields[0])
                pls['playlist_id'] = int(fields[1])
                pls['song_id'] = int(fields[2])
                pls['added_date'] = fields[3]
                playlist_songs.append(pls)
            except ValueError:
                continue
    return playlist_songs


def write_playlists(playlists):
    path = os.path.join(DATA_DIR, 'playlists.txt')
    lines = []
    for p in playlists:
        line = f"{p['playlist_id']}|{p['title']}|{p['description']}|{p['creation_date']}|{p['total_songs']}"
        lines.append(line)
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))


def write_playlist_songs(playlist_songs):
    path = os.path.join(DATA_DIR, 'playlist_songs.txt')
    lines = []
    for pls in playlist_songs:
        line = f"{pls['playlist_song_id']}|{pls['playlist_id']}|{pls['song_id']}|{pls['added_date']}"
        lines.append(line)
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))


# Routing and business logic

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    # featured_songs: List with keys {song_id,int; title,str; artist_name,str; duration,int}
    songs = read_songs()
    artists = read_artists()
    # We define featured_songs as top 5 songs by play_count descending
    sorted_songs = sorted(songs, key=lambda x: x['play_count'], reverse=True)[:5]

    # Map artist_id to name
    artist_map = {a['artist_id']: a['name'] for a in artists}

    featured_songs = []
    for s in sorted_songs:
        featured_songs.append({
            'song_id': s['song_id'],
            'title': s['title'],
            'artist_name': artist_map.get(s['artist_id'], 'Unknown'),
            'duration': s['duration']
        })

    # trending_artists: top 5 artists with most popular songs_play_count sum
    artist_play_counts = {}
    for s in songs:
        aid = s['artist_id']
        artist_play_counts[aid] = artist_play_counts.get(aid, 0) + s['play_count']

    trending_sorted = sorted(artist_play_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    trending_artists = []
    for aid, _ in trending_sorted:
        name = artist_map.get(aid, 'Unknown')
        trending_artists.append({'artist_id': aid, 'name': name})

    return render_template('dashboard.html', featured_songs=featured_songs, trending_artists=trending_artists)


@app.route('/songs')
def song_catalog():
    songs = read_songs()
    artists = read_artists()
    albums = read_albums()
    genres = read_genres()

    artist_map = {a['artist_id']: a['name'] for a in artists}
    album_map = {al['album_id']: al['title'] for al in albums}
    genre_names = sorted(set(g['genre_name'] for g in genres))

    song_list = []
    for s in songs:
        song_list.append({
            'song_id': s['song_id'],
            'title': s['title'],
            'artist_name': artist_map.get(s['artist_id'], 'Unknown'),
            'album_name': album_map.get(s['album_id'], 'Unknown'),
            'genre': s['genre'],
            'duration': s['duration']
        })

    return render_template('song_catalog.html', songs=song_list, genres=genre_names)


@app.route('/songs/<int:song_id>')
def song_details(song_id):
    songs = read_songs()
    artists = read_artists()
    albums = read_albums()

    song = next((s for s in songs if s['song_id'] == song_id), None)
    if not song:
        abort(404)

    artist = next((a for a in artists if a['artist_id'] == song['artist_id']), None)
    album = next((al for al in albums if al['album_id'] == song['album_id']), None)

    # Compose song dictionary with all required fields
    song_dict = {
        'song_id': song['song_id'],
        'title': song['title'],
        'artist_id': artist['artist_id'] if artist else None,
        'artist_name': artist['name'] if artist else 'Unknown',
        'album_id': album['album_id'] if album else None,
        'album_name': album['title'] if album else 'Unknown',
        'duration': song['duration'],
        'genre': song['genre'],
        'release_date': song['release_date'],
        'play_count': song['play_count']
    }

    return render_template('song_details.html', song=song_dict)


@app.route('/playlists')
def playlists_page():
    playlists = read_playlists()

    # Prepare playlists list with required keys including total_songs
    playlist_list = []
    for p in playlists:
        playlist_list.append({
            'playlist_id': p['playlist_id'],
            'title': p['title'],
            'description': p['description'],
            'total_songs': p['total_songs']
        })

    return render_template('playlists.html', playlists=playlist_list)


@app.route('/playlists/create', methods=['GET', 'POST'])
def create_playlist():
    if request.method == 'GET':
        return render_template('create_playlist.html')

    # POST - create new playlist
    title = request.form.get('playlist-name-input', '').strip()
    description = request.form.get('playlist-description-input', '').strip()

    errors = []
    if not title:
        errors.append('Playlist title is required.')

    if errors:
        return render_template('create_playlist.html', errors=errors)

    playlists = read_playlists()
    if playlists:
        new_id = max(p['playlist_id'] for p in playlists) + 1
    else:
        new_id = 1

    creation_date = datetime.now().strftime('%Y-%m-%d')

    new_playlist = {
        'playlist_id': new_id,
        'title': title,
        'description': description,
        'creation_date': creation_date,
        'total_songs': 0
    }

    playlists.append(new_playlist)
    write_playlists(playlists)

    return redirect(url_for('playlists_page'))


@app.route('/playlists/<int:playlist_id>')
def playlist_details(playlist_id):
    playlists = read_playlists()
    playlist_songs = read_playlist_songs()
    songs = read_songs()
    artists = read_artists()

    playlist = next((p for p in playlists if p['playlist_id'] == playlist_id), None)
    if not playlist:
        abort(404)

    # Filter playlist songs for this playlist
    pls_songs = [pls for pls in playlist_songs if pls['playlist_id'] == playlist_id]

    artist_map = {a['artist_id']: a['name'] for a in artists}
    song_map = {s['song_id']: s for s in songs}

    songs_in_playlist = []
    for pls in pls_songs:
        song = song_map.get(pls['song_id'])
        if song:
            songs_in_playlist.append({
                'song_id': song['song_id'],
                'title': song['title'],
                'artist_name': artist_map.get(song['artist_id'], 'Unknown'),
                'duration': song['duration']
            })

    playlist_dict = {
        'playlist_id': playlist['playlist_id'],
        'title': playlist['title'],
        'description': playlist['description']
    }

    return render_template('playlist_details.html', playlist=playlist_dict, songs=songs_in_playlist)


@app.route('/albums')
def albums_page():
    albums = read_albums()
    artists = read_artists()

    artist_map = {a['artist_id']: a['name'] for a in artists}

    album_list = []
    for al in albums:
        album_list.append({
            'album_id': al['album_id'],
            'title': al['title'],
            'artist_name': artist_map.get(al['artist_id'], 'Unknown'),
            'year': al['release_year']
        })

    return render_template('albums.html', albums=album_list)


@app.route('/albums/<int:album_id>')
def album_details(album_id):
    albums = read_albums()
    songs = read_songs()
    artists = read_artists()

    album = next((al for al in albums if al['album_id'] == album_id), None)
    if not album:
        abort(404)

    artist = next((a for a in artists if a['artist_id'] == album['artist_id']), None)

    album_songs = [s for s in songs if s['album_id'] == album_id]

    album_dict = {
        'album_id': album['album_id'],
        'title': album['title'],
        'artist_id': artist['artist_id'] if artist else None,
        'artist_name': artist['name'] if artist else 'Unknown',
        'release_year': album['release_year']
    }

    songs_list = []
    for s in album_songs:
        songs_list.append({
            'song_id': s['song_id'],
            'title': s['title'],
            'duration': s['duration']
        })

    return render_template('album_details.html', album=album_dict, songs=songs_list)


@app.route('/artists')
def artists_page():
    artists = read_artists()

    artists_list = []
    for a in artists:
        artists_list.append({
            'artist_id': a['artist_id'],
            'name': a['name'],
            'genre': a['genre']
        })

    return render_template('artists.html', artists=artists_list)


@app.route('/artists/<int:artist_id>')
def artist_profile(artist_id):
    artists = read_artists()

    artist = next((a for a in artists if a['artist_id'] == artist_id), None)
    if not artist:
        abort(404)

    artist_dict = {
        'artist_id': artist['artist_id'],
        'name': artist['name'],
        'genre': artist['genre'],
        'country': artist['country'],
        'formation_year': artist['formation_year']
    }

    return render_template('artist_profile.html', artist=artist_dict)


@app.route('/genres')
def genre_exploration():
    genres = read_genres()
    songs = read_songs()
    artists = read_artists()

    selected_genre_id = request.args.get('selected_genre_id', type=int)

    genre_songs = []
    genre_artists = []

    genre_map = {g['genre_id']: g for g in genres}

    if selected_genre_id is not None and selected_genre_id in genre_map:
        selected_genre_name = genre_map[selected_genre_id]['genre_name']

        # Songs of selected genre
        for s in songs:
            if s['genre'] == selected_genre_name:
                artist_name = next((a['name'] for a in artists if a['artist_id'] == s['artist_id']), 'Unknown')
                genre_songs.append({
                    'song_id': s['song_id'],
                    'title': s['title'],
                    'artist_name': artist_name
                })

        # Artists of selected genre
        for a in artists:
            if a['genre'] == selected_genre_name:
                genre_artists.append({'artist_id': a['artist_id'], 'name': a['name']})

    else:
        selected_genre_id = None

    return render_template('genres.html', genres=genres, selected_genre_id=selected_genre_id,
                           genre_songs=genre_songs, genre_artists=genre_artists)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
