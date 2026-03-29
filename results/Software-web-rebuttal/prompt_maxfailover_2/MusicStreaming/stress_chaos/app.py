from flask import Flask, render_template, redirect, url_for, request, abort
from datetime import datetime
import os

app = Flask(__name__)

DATA_DIR = 'data'

# Ensure data directory exists before any writes
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# Helper functions to load data

def load_songs():
    songs = []
    filename = os.path.join(DATA_DIR, 'songs.txt')
    if not os.path.exists(filename):
        return songs
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) < 8:
                continue
            try:
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
            except ValueError:
                continue
    return songs

def load_artists():
    artists = []
    filename = os.path.join(DATA_DIR, 'artists.txt')
    if not os.path.exists(filename):
        return artists
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) < 5:
                continue
            try:
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
            except ValueError:
                continue
    return artists

def load_albums():
    albums = []
    filename = os.path.join(DATA_DIR, 'albums.txt')
    if not os.path.exists(filename):
        return albums
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) < 6:
                continue
            try:
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
            except ValueError:
                continue
    return albums

def load_genres():
    genres = []
    filename = os.path.join(DATA_DIR, 'genres.txt')
    if not os.path.exists(filename):
        return genres
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) < 3:
                continue
            try:
                genre_id = int(parts[0])
                genre_name = parts[1]
                description = parts[2]
                genres.append({
                    'genre_id': genre_id,
                    'genre_name': genre_name,
                    'description': description
                })
            except ValueError:
                continue
    return genres

def load_playlists():
    playlists = []
    filename = os.path.join(DATA_DIR, 'playlists.txt')
    if not os.path.exists(filename):
        return playlists
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) < 5:
                continue
            try:
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
            except ValueError:
                continue
    return playlists

def load_playlist_songs():
    playlist_songs = []
    filename = os.path.join(DATA_DIR, 'playlist_songs.txt')
    if not os.path.exists(filename):
        return playlist_songs
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) < 4:
                continue
            try:
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
            except ValueError:
                continue
    return playlist_songs


# Save functions for playlists and playlist_songs (for create, update, delete)
def save_playlists(playlists):
    filename = os.path.join(DATA_DIR, 'playlists.txt')
    # Ensure data directory exists before writing
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    with open(filename, 'w', encoding='utf-8') as f:
        for p in playlists:
            line = f"{p['playlist_id']}|{p['title']}|{p['description']}|{p['creation_date']}|{p['total_songs']}\n"
            f.write(line)

def save_playlist_songs(playlist_songs):
    filename = os.path.join(DATA_DIR, 'playlist_songs.txt')
    # Ensure data directory exists before writing
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    with open(filename, 'w', encoding='utf-8') as f:
        for ps in playlist_songs:
            line = f"{ps['playlist_song_id']}|{ps['playlist_id']}|{ps['song_id']}|{ps['added_date']}\n"
            f.write(line)


def root_redirect():
    return redirect(url_for('dashboard_page'))

app.add_url_rule('/', 'root_redirect', root_redirect, methods=['GET'])

@app.route('/dashboard', methods=['GET'])
def dashboard_page():
    songs = load_songs()
    artists = load_artists()

    # Featured songs: select top 5 songs by play_count descending
    sorted_songs = sorted(songs, key=lambda s: s.get('play_count', 0), reverse=True)[:5]
    featured_songs = []
    artists_dict = {a['artist_id']: a for a in artists}
    for s in sorted_songs:
        artist_name = artists_dict.get(s['artist_id'], {}).get('name', 'Unknown Artist')
        featured_songs.append({
            'song_id': s['song_id'],
            'title': s['title'],
            'artist_name': artist_name,
            'duration': s['duration']
        })

    # Trending artists: select top 5 artists by total play counts of their songs
    artist_play_counts = {a['artist_id']: 0 for a in artists}
    for s in songs:
        artist_play_counts[s['artist_id']] = artist_play_counts.get(s['artist_id'], 0) + s.get('play_count', 0)
    sorted_artists = sorted(artists, key=lambda a: artist_play_counts.get(a['artist_id'], 0), reverse=True)[:5]
    trending_artists = []
    for a in sorted_artists:
        trending_artists.append({
            'artist_id': a['artist_id'],
            'name': a['name'],
            'genre': a['genre']
        })

    return render_template('dashboard.html', featured_songs=featured_songs, trending_artists=trending_artists)

@app.route('/songs', methods=['GET'])
def song_catalog():
    songs = load_songs()
    artists = load_artists()
    albums = load_albums()
    genres_data = load_genres()

    genres = [g['genre_name'] for g in genres_data]
    selected_genre = request.args.get('genre')
    search_query = request.args.get('search', '').strip()

    # Filter songs by genre if selected
    filtered_songs = songs
    if selected_genre and selected_genre in genres:
        filtered_songs = [s for s in filtered_songs if s['genre'] == selected_genre]
    elif selected_genre and selected_genre not in genres:
        # if genre provided but invalid, treat as no filter
        selected_genre = None

    # Filter songs by search query (title contains, case-insensitive)
    if search_query:
        filtered_songs = [s for s in filtered_songs if search_query.lower() in s['title'].lower()]

    # Prepare context songs list
    artists_dict = {a['artist_id']: a for a in artists}
    albums_dict = {a['album_id']: a for a in albums}

    context_songs = []
    for s in filtered_songs:
        artist_name = artists_dict.get(s['artist_id'], {}).get('name', 'Unknown Artist')
        album_name = albums_dict.get(s['album_id'], {}).get('title', 'Unknown Album')
        context_songs.append({
            'song_id': s['song_id'],
            'title': s['title'],
            'artist_name': artist_name,
            'album_name': album_name,
            'genre': s['genre'],
            'duration': s['duration']
        })

    return render_template('song_catalog.html', songs=context_songs, genres=genres, selected_genre=selected_genre, search_query=search_query)

@app.route('/songs/<int:song_id>', methods=['GET'])
def song_details(song_id):
    songs = load_songs()
    artists = load_artists()
    albums = load_albums()

    song = next((s for s in songs if s['song_id'] == song_id), None)
    if not song:
        abort(404)

    artist = next((a for a in artists if a['artist_id'] == song['artist_id']), None)
    album = next((a for a in albums if a['album_id'] == song['album_id']), None)

    context_song = {
        'song_id': song['song_id'],
        'title': song['title'],
        'artist_id': artist['artist_id'] if artist else None,
        'artist_name': artist['name'] if artist else 'Unknown Artist',
        'album_id': album['album_id'] if album else None,
        'album_name': album['title'] if album else 'Unknown Album',
        'duration': song['duration'],
        'genre': song['genre']
    }

    return render_template('song_details.html', song=context_song)

@app.route('/playlists', methods=['GET'])
def playlists_page():
    playlists = load_playlists()

    playlists_context = []
    for p in playlists:
        playlists_context.append({
            'playlist_id': p['playlist_id'],
            'title': p['title'],
            'total_songs': p['total_songs']
        })

    return render_template('playlists.html', playlists=playlists_context)

@app.route('/playlists/<int:playlist_id>', methods=['GET'])
def playlist_details(playlist_id):
    playlists = load_playlists()
    playlist_songs = load_playlist_songs()
    songs = load_songs()
    artists = load_artists()

    playlist = next((p for p in playlists if p['playlist_id'] == playlist_id), None)
    if not playlist:
        abort(404)

    # Find songs in playlist
    ps_for_playlist = [ps for ps in playlist_songs if ps['playlist_id'] == playlist_id]

    songs_in_playlist = []
    artists_dict = {a['artist_id']: a for a in artists}
    songs_dict = {s['song_id']: s for s in songs}

    for ps in ps_for_playlist:
        s = songs_dict.get(ps['song_id'])
        if s:
            artist_name = artists_dict.get(s['artist_id'], {}).get('name', 'Unknown Artist')
            songs_in_playlist.append({
                'song_id': s['song_id'],
                'title': s['title'],
                'artist_name': artist_name,
                'duration': s['duration']
            })

    playlist_context = {
        'playlist_id': playlist['playlist_id'],
        'title': playlist['title'],
        'description': playlist['description']
    }

    return render_template('playlist_details.html', playlist=playlist_context, songs_in_playlist=songs_in_playlist)

@app.route('/playlists/delete/<int:playlist_id>', methods=['POST'])
def delete_playlist(playlist_id):
    playlists = load_playlists()
    playlist_songs = load_playlist_songs()

    playlist = next((p for p in playlists if p['playlist_id'] == playlist_id), None)
    if not playlist:
        abort(404)

    # Remove the playlist
    playlists = [p for p in playlists if p['playlist_id'] != playlist_id]

    # Remove all songs for this playlist
    playlist_songs = [ps for ps in playlist_songs if ps['playlist_id'] != playlist_id]

    save_playlists(playlists)
    save_playlist_songs(playlist_songs)

    return redirect(url_for('playlists_page'))

@app.route('/playlists/create', methods=['GET'])
def create_playlist_page():
    return render_template('create_playlist.html')

@app.route('/playlists/create', methods=['POST'])
def create_playlist_submit():
    playlist_name = request.form.get('playlist_name', '').strip()
    playlist_description = request.form.get('playlist_description', '').strip()

    if not playlist_name:
        # For simplicity, just redirect back to create page
        return redirect(url_for('create_playlist_page'))

    playlists = load_playlists()

    # Generate new unique playlist_id
    if playlists:
        new_playlist_id = max(p['playlist_id'] for p in playlists) + 1
    else:
        new_playlist_id = 1

    creation_date = datetime.now().strftime('%Y-%m-%d')

    new_playlist = {
        'playlist_id': new_playlist_id,
        'title': playlist_name,
        'description': playlist_description,
        'creation_date': creation_date,
        'total_songs': 0
    }

    playlists.append(new_playlist)
    save_playlists(playlists)

    return redirect(url_for('playlist_details', playlist_id=new_playlist_id))

@app.route('/albums', methods=['GET'])
def albums_page():
    albums = load_albums()
    artists = load_artists()

    search_query = request.args.get('search', '').strip()
    sort_option = request.args.get('sort', 'By Title')

    # Filter albums by search query (title contains, case-insensitive)
    filtered_albums = albums
    if search_query:
        filtered_albums = [a for a in albums if search_query.lower() in a['title'].lower()]

    # Sort albums by option
    if sort_option == 'By Title':
        filtered_albums = sorted(filtered_albums, key=lambda x: x['title'].lower())
    elif sort_option == 'By Artist':
        artists_dict = {a['artist_id']: a for a in artists}
        filtered_albums = sorted(filtered_albums, key=lambda x: artists_dict.get(x['artist_id'], {}).get('name', '').lower())
    elif sort_option == 'By Year':
        filtered_albums = sorted(filtered_albums, key=lambda x: x['release_year'])

    artists_dict = {a['artist_id']: a for a in artists}

    context_albums = []
    for a in filtered_albums:
        artist_name = artists_dict.get(a['artist_id'], {}).get('name', 'Unknown Artist')
        context_albums.append({
            'album_id': a['album_id'],
            'title': a['title'],
            'artist_name': artist_name,
            'release_year': a['release_year']
        })

    return render_template('albums.html', albums=context_albums, search_query=search_query, sort_option=sort_option)

@app.route('/albums/<int:album_id>', methods=['GET'])
def album_details(album_id):
    albums = load_albums()
    artists = load_artists()
    songs = load_songs()

    album = next((a for a in albums if a['album_id'] == album_id), None)
    if not album:
        abort(404)

    artist = next((a for a in artists if a['artist_id'] == album['artist_id']), None)

    album_songs = [
        {'song_id': s['song_id'], 'title': s['title'], 'duration': s['duration']}
        for s in songs if s['album_id'] == album_id
    ]

    context_album = {
        'album_id': album['album_id'],
        'title': album['title'],
        'artist_id': artist['artist_id'] if artist else None,
        'artist_name': artist['name'] if artist else 'Unknown Artist',
        'release_year': album['release_year'],
        'genre': album['genre']
    }

    return render_template('album_details.html', album=context_album, album_songs=album_songs)

@app.route('/artists', methods=['GET'])
def artists_page():
    artists = load_artists()

    search_query = request.args.get('search', '').strip()
    sort_option = request.args.get('sort', 'By Name')

    # Filter artists by search query (name contains, case-insensitive)
    filtered_artists = artists
    if search_query:
        filtered_artists = [a for a in artists if search_query.lower() in a['name'].lower()]

    # Sort artists by option
    if sort_option == 'By Name':
        filtered_artists = sorted(filtered_artists, key=lambda x: x['name'].lower())
    elif sort_option == 'By Genre':
        filtered_artists = sorted(filtered_artists, key=lambda x: x['genre'].lower())

    return render_template('artists.html', artists=filtered_artists, search_query=search_query, sort_option=sort_option)

@app.route('/artists/<int:artist_id>', methods=['GET'])
def artist_profile(artist_id):
    artists = load_artists()
    songs = load_songs()
    albums = load_albums()

    artist = next((a for a in artists if a['artist_id'] == artist_id), None)
    if not artist:
        abort(404)

    artist_songs = []
    artist_albums = []

    albums_dict = {a['album_id']: a for a in albums}

    for s in songs:
        if s['artist_id'] == artist_id:
            album_name = albums_dict.get(s['album_id'], {}).get('title', 'Unknown Album')
            artist_songs.append({
                'song_id': s['song_id'],
                'title': s['title'],
                'album_name': album_name,
                'duration': s['duration']
            })

    for a in albums:
        if a['artist_id'] == artist_id:
            artist_albums.append({
                'album_id': a['album_id'],
                'title': a['title'],
                'release_year': a['release_year']
            })

    return render_template('artist_profile.html', artist=artist, artist_songs=artist_songs, artist_albums=artist_albums)

@app.route('/genres', methods=['GET'])
def genre_exploration_page():
    genres = load_genres()
    artists = load_artists()
    songs = load_songs()

    genre_id_str = request.args.get('genre_id')
    selected_genre_id = None
    for g in genres:
        if str(g['genre_id']) == genre_id_str:
            selected_genre_id = g['genre_id']
            break

    selected_genre_name = None
    if selected_genre_id is not None:
        for g in genres:
            if g['genre_id'] == selected_genre_id:
                selected_genre_name = g['genre_name']
                break

    genre_songs = []
    genre_artists = []

    if selected_genre_name:
        # Songs with this genre
        genre_songs = [
            {
                'song_id': s['song_id'],
                'title': s['title'],
                'artist_name': next((a['name'] for a in artists if a['artist_id'] == s['artist_id']), 'Unknown Artist'),
                'duration': s['duration']
            }
            for s in songs if s['genre'] == selected_genre_name
        ]
        # Artists with this genre
        genre_artists = [
            a for a in artists if a['genre'] == selected_genre_name
        ]

    return render_template('genres.html', genres=genres, selected_genre_id=selected_genre_id,
                           genre_songs=genre_songs, genre_artists=genre_artists)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
