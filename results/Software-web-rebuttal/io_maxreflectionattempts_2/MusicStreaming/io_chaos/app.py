from flask import Flask, render_template, redirect, url_for, request, abort
from datetime import datetime
import os

app = Flask(__name__)

DATA_DIR = 'data'

# Utility functions to load data from files according to schema

def load_file_lines(filepath):
    if not os.path.exists(filepath):
        # Return empty list when file missing to prevent errors
        return []
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.readlines()


def load_songs():
    songs = []
    path = os.path.join(DATA_DIR, 'songs.txt')
    lines = load_file_lines(path)
    for line in lines:
        parts = line.strip().split('|')
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
    path = os.path.join(DATA_DIR, 'artists.txt')
    lines = load_file_lines(path)
    for line in lines:
        parts = line.strip().split('|')
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
    path = os.path.join(DATA_DIR, 'albums.txt')
    lines = load_file_lines(path)
    for line in lines:
        parts = line.strip().split('|')
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
    path = os.path.join(DATA_DIR, 'genres.txt')
    lines = load_file_lines(path)
    for line in lines:
        parts = line.strip().split('|')
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
    path = os.path.join(DATA_DIR, 'playlists.txt')
    lines = load_file_lines(path)
    for line in lines:
        parts = line.strip().split('|')
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

def load_playlist_songs():
    playlist_songs = []
    path = os.path.join(DATA_DIR, 'playlist_songs.txt')
    lines = load_file_lines(path)
    for line in lines:
        parts = line.strip().split('|')
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

# Utility functions to save playlists and playlist songs

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

# Utility functions for lookup

def find_artist_by_id(artists, artist_id):
    for a in artists:
        if a['artist_id'] == artist_id:
            return a
    return None

def find_album_by_id(albums, album_id):
    for a in albums:
        if a['album_id'] == album_id:
            return a
    return None

def find_genre_by_id(genres, genre_id):
    for g in genres:
        if g['genre_id'] == genre_id:
            return g
    return None

def find_song_by_id(songs, song_id):
    for s in songs:
        if s['song_id'] == song_id:
            return s
    return None

def find_playlist_by_id(playlists, playlist_id):
    for p in playlists:
        if p['playlist_id'] == playlist_id:
            return p
    return None

# Helper for filtering

def filter_songs_by_genre(songs, genre_name):
    return [s for s in songs if s['genre'].lower() == genre_name.lower()]

def filter_songs_by_search_term(songs, term):
    term = term.lower()
    return [s for s in songs if term in s['title'].lower()]

def filter_albums_by_search_term(albums, term):
    term = term.lower()
    return [a for a in albums if term in a['title'].lower()]

def filter_artists_by_search_term(artists, term):
    term = term.lower()
    return [a for a in artists if term in a['name'].lower()]

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard_page'))

@app.route('/dashboard')
def dashboard_page():
    songs = load_songs()
    artists = load_artists()
    albums = load_albums()

    # featured_songs: list of dict {song_id, title, artist_name, album_name, duration}
    # Pick top 5 songs by play_count as featured
    songs_sorted_by_play = sorted(songs, key=lambda x: x['play_count'], reverse=True)
    featured_songs = []
    artists_map = {a['artist_id']: a for a in artists}
    albums_map = {a['album_id']: a for a in albums}
    for s in songs_sorted_by_play[:5]:
        artist_name = artists_map.get(s['artist_id'], {}).get('name', 'Unknown Artist')
        album_name = albums_map.get(s['album_id'], {}).get('title', 'Unknown Album')
        featured_songs.append({
            'song_id': s['song_id'],
            'title': s['title'],
            'artist_name': artist_name,
            'album_name': album_name,
            'duration': s['duration']
        })

    # trending_artists: list of dict {artist_id, name, genre}
    # Pick top 5 artists by sum of play_count of their songs

    artist_play_counts = {}
    for s in songs:
        artist_play_counts[s['artist_id']] = artist_play_counts.get(s['artist_id'], 0) + s['play_count']
    top_artists_ids = sorted(artist_play_counts.items(), key=lambda x: x[1], reverse=True)[:5]

    trending_artists = []
    for aid, _ in top_artists_ids:
        artist = artists_map.get(aid)
        if artist:
            trending_artists.append({
                'artist_id': artist['artist_id'],
                'name': artist['name'],
                'genre': artist['genre']
            })

    return render_template('dashboard.html', featured_songs=featured_songs, trending_artists=trending_artists)

@app.route('/songs')
def song_catalog_page():
    songs = load_songs()
    artists = load_artists()
    albums = load_albums()
    genres = load_genres()

    genres_names = [g['genre_name'] for g in genres]

    artists_map = {a['artist_id']: a for a in artists}
    albums_map = {a['album_id']: a for a in albums}

    songs_full = []
    for s in songs:
        artist = artists_map.get(s['artist_id'], {'name': 'Unknown Artist'})
        album = albums_map.get(s['album_id'], {'title': 'Unknown Album'})
        songs_full.append({
            'song_id': s['song_id'],
            'title': s['title'],
            'artist_name': artist['name'],
            'album_name': album['title'],
            'genre': s['genre'],
            'duration': s['duration']
        })

    return render_template('song_catalog.html', songs=songs_full, genres=genres_names)

@app.route('/songs/search', methods=['POST'])
def song_search():
    songs = load_songs()
    artists = load_artists()
    albums = load_albums()
    genres = load_genres()

    genres_names = [g['genre_name'] for g in genres]

    search_term = request.form.get('search_input', '').strip()
    genre_filter = request.form.get('genre_filter', '').strip()

    filtered = songs

    if search_term:
        filtered = filter_songs_by_search_term(filtered, search_term)
    if genre_filter and genre_filter in genres_names:
        filtered = filter_songs_by_genre(filtered, genre_filter)

    artists_map = {a['artist_id']: a for a in artists}
    albums_map = {a['album_id']: a for a in albums}

    songs_full = []
    for s in filtered:
        artist = artists_map.get(s['artist_id'], {'name': 'Unknown Artist'})
        album = albums_map.get(s['album_id'], {'title': 'Unknown Album'})
        songs_full.append({
            'song_id': s['song_id'],
            'title': s['title'],
            'artist_name': artist['name'],
            'album_name': album['title'],
            'genre': s['genre'],
            'duration': s['duration']
        })

    return render_template('song_catalog.html', songs=songs_full, genres=genres_names), 200

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

    song_detail = {
        'song_id': song['song_id'],
        'title': song['title'],
        'artist_id': artist['artist_id'] if artist else None,
        'artist_name': artist['name'] if artist else 'Unknown Artist',
        'album_id': album['album_id'] if album else None,
        'album_name': album['title'] if album else 'Unknown Album',
        'duration': song['duration'],
        'genre': song['genre'],
        'release_date': song['release_date'],
        'play_count': song['play_count']
    }

    # Add required UI element IDs for frontend compliance
    song_detail['add_to_playlist_button_id'] = f"add-to-playlist-button-{song['song_id']}"
    song_detail['play_button_id'] = f"play-button-{song['song_id']}"

    return render_template('song_details.html', song=song_detail)

@app.route('/playlists')
def playlists_page():
    playlists = load_playlists()
    return render_template('playlists.html', playlists=playlists)

@app.route('/playlists/create', methods=['GET'])
def create_playlist_page():
    return render_template('create_playlist.html')

@app.route('/playlists/create', methods=['POST'])
def create_playlist_post():
    title = request.form.get('title', '').strip()
    description = request.form.get('description', '').strip()

    if not title:
        # Redirect back with 302 when invalid
        return redirect(url_for('create_playlist_page'))

    playlists = load_playlists()
    new_id = max([p['playlist_id'] for p in playlists], default=0) + 1
    creation_date = datetime.now().strftime('%Y-%m-%d')
    new_playlist = {
        'playlist_id': new_id,
        'title': title,
        'description': description,
        'creation_date': creation_date,
        'total_songs': 0
    }
    playlists.append(new_playlist)
    save_playlists(playlists)

    # After saving, redirect properly to playlists page, 302 default
    return redirect(url_for('playlists_page'))

@app.route('/playlists/<int:playlist_id>')
def playlist_details_page(playlist_id):
    playlists = load_playlists()
    if not playlists:
        abort(404)
    playlist = find_playlist_by_id(playlists, playlist_id)
    if not playlist:
        abort(404)

    songs = load_songs()
    artists = load_artists()
    playlist_songs = load_playlist_songs()

    artists_map = {a['artist_id']: a for a in artists}
    songs_map = {s['song_id']: s for s in songs}

    # Only playlist_song entries for this playlist
    playlist_song_entries = [ps for ps in playlist_songs if ps['playlist_id'] == playlist_id]

    songs_in_playlist = []
    for ps_entry in playlist_song_entries:
        song = songs_map.get(ps_entry['song_id'])
        if not song:
            continue
        artist_name = artists_map.get(song['artist_id'], {'name': 'Unknown Artist'})['name']
        songs_in_playlist.append({
            'song_id': song['song_id'],
            'title': song['title'],
            'artist_name': artist_name,
            'duration': song['duration'],
            # Add dynamic remove button ID
            'remove_button_id': f"remove-song-button-{playlist_id}-{song['song_id']}"
        })

    # Add playlist edit button ID
    playlist_edit_button_id = f"edit-playlist-button-{playlist_id}"

    return render_template('playlist_details.html', playlist=playlist, songs_in_playlist=songs_in_playlist, playlist_edit_button_id=playlist_edit_button_id)

@app.route('/playlists/<int:playlist_id>/remove_song/<int:song_id>', methods=['POST'])
def remove_song_from_playlist(playlist_id, song_id):
    playlists = load_playlists()
    playlist_songs = load_playlist_songs()

    playlist = find_playlist_by_id(playlists, playlist_id)
    if not playlist:
        abort(404)

    new_playlist_songs = [ps for ps in playlist_songs if not (ps['playlist_id'] == playlist_id and ps['song_id'] == song_id)]

    if len(new_playlist_songs) < len(playlist_songs):
        playlist['total_songs'] = max(0, playlist['total_songs'] - 1)
        save_playlists([p if p['playlist_id'] != playlist_id else playlist for p in playlists])
        save_playlist_songs(new_playlist_songs)

    return redirect(url_for('playlist_details_page', playlist_id=playlist_id))

@app.route('/playlists/<int:playlist_id>/delete', methods=['POST'])
def delete_playlist(playlist_id):
    playlists = load_playlists()
    playlist_songs = load_playlist_songs()

    playlists = [p for p in playlists if p['playlist_id'] != playlist_id]
    save_playlists(playlists)

    playlist_songs = [ps for ps in playlist_songs if ps['playlist_id'] != playlist_id]
    save_playlist_songs(playlist_songs)

    return redirect(url_for('playlists_page'))

@app.route('/albums')
def albums_page():
    albums = load_albums()
    artists = load_artists()

    artists_map = {a['artist_id']: a for a in artists}

    albums_full = []
    for a in albums:
        artist = artists_map.get(a['artist_id'], {'name': 'Unknown Artist'})
        albums_full.append({
            'album_id': a['album_id'],
            'title': a['title'],
            'artist_name': artist['name'],
            'year': a['release_year'],
            'genre': a['genre']
        })

    return render_template('albums.html', albums=albums_full)

@app.route('/albums/search', methods=['POST'])
def album_search():
    albums = load_albums()
    artists = load_artists()

    search_term = request.form.get('search_albums', '').strip()

    filtered = albums
    if search_term:
        filtered = filter_albums_by_search_term(albums, search_term)

    artists_map = {a['artist_id']: a for a in artists}

    albums_full = []
    for a in filtered:
        artist = artists_map.get(a['artist_id'], {'name': 'Unknown Artist'})
        albums_full.append({
            'album_id': a['album_id'],
            'title': a['title'],
            'artist_name': artist['name'],
            'year': a['release_year'],
            'genre': a['genre']
        })

    return render_template('albums.html', albums=albums_full), 200

@app.route('/albums/<int:album_id>')
def album_details_page(album_id):
    albums = load_albums()
    artists = load_artists()
    songs = load_songs()
    
    album = find_album_by_id(albums, album_id)
    if not album:
        abort(404)

    artist = find_artist_by_id(artists, album['artist_id'])

    songs_in_album = [s for s in songs if s['album_id'] == album_id]

    songs_list = []
    for s in songs_in_album:
        songs_list.append({
            'song_id': s['song_id'],
            'title': s['title'],
            'duration': s['duration']
        })

    album_dict = {
        'album_id': album['album_id'],
        'title': album['title'],
        'artist_id': artist['artist_id'] if artist else None,
        'artist_name': artist['name'] if artist else 'Unknown Artist',
        'release_year': album['release_year'],
        'total_songs': album['total_songs'],
        'genre': album['genre']
    }

    return render_template('album_details.html', album=album_dict, songs_in_album=songs_list)

@app.route('/albums/<int:album_id>/add_to_playlist', methods=['POST'])
def add_album_to_playlist(album_id):
    playlists = load_playlists()
    songs = load_songs()
    playlist_songs = load_playlist_songs()

    album_songs = [s for s in songs if s['album_id'] == album_id]

    if not playlists:
        return redirect(url_for('playlists_page'))
    playlist = playlists[0]

    existing_song_ids = {ps['song_id'] for ps in playlist_songs if ps['playlist_id'] == playlist['playlist_id']}

    max_ps_id = max((ps['playlist_song_id'] for ps in playlist_songs), default=0)

    added_any = False
    added_count = 0
    for song in album_songs:
        if song['song_id'] not in existing_song_ids:
            max_ps_id += 1
            playlist_songs.append({
                'playlist_song_id': max_ps_id,
                'playlist_id': playlist['playlist_id'],
                'song_id': song['song_id'],
                'added_date': datetime.now().strftime('%Y-%m-%d')
            })
            added_any = True
            added_count += 1

    if added_any:
        playlist['total_songs'] += added_count
        save_playlist_songs(playlist_songs)
        updated_playlists = []
        for p in playlists:
            if p['playlist_id'] == playlist['playlist_id']:
                updated_playlists.append(playlist)
            else:
                updated_playlists.append(p)
        save_playlists(updated_playlists)

    return redirect(url_for('playlists_page'))

@app.route('/artists')
def artists_page():
    artists = load_artists()
    return render_template('artists.html', artists=artists)

@app.route('/artists/search', methods=['POST'])
def artist_search():
    artists = load_artists()
    search_term = request.form.get('search_artists', '').strip()
    filtered = artists
    if search_term:
        filtered = filter_artists_by_search_term(artists, search_term)
    return render_template('artists.html', artists=filtered), 200

@app.route('/artists/<int:artist_id>')
def artist_profile_page(artist_id):
    artists = load_artists()
    songs = load_songs()
    albums = load_albums()

    artist = find_artist_by_id(artists, artist_id)
    if not artist:
        abort(404)

    songs_by_artist = []
    albums_map = {a['album_id']: a for a in albums}
    for s in songs:
        if s['artist_id'] == artist_id:
            album_name = albums_map.get(s['album_id'], {'title': 'Unknown Album'})['title']
            songs_by_artist.append({
                'song_id': s['song_id'],
                'title': s['title'],
                'album_name': album_name,
                'duration': s['duration']
            })

    return render_template('artist_profile.html', artist=artist, songs_by_artist=songs_by_artist)

@app.route('/genres')
def genres_page():
    genres = load_genres()
    songs = load_songs()
    artists = load_artists()

    songs_sorted = sorted(songs, key=lambda x: x['play_count'], reverse=True)[:5]
    artists_map = {a['artist_id']: a for a in artists}
    featured_songs = []
    for s in songs_sorted:
        artist_name = artists_map.get(s['artist_id'], {'name': 'Unknown Artist'})['name']
        featured_songs.append({
            'song_id': s['song_id'],
            'title': s['title'],
            'artist_name': artist_name,
            'duration': s['duration']
        })

    artist_play_counts = {}
    for s in songs:
        artist_play_counts[s['artist_id']] = artist_play_counts.get(s['artist_id'], 0) + s['play_count']

    top_artist_ids = sorted(artist_play_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    featured_artists = []
    for aid, _ in top_artist_ids:
        a = artists_map.get(aid)
        if a:
            featured_artists.append({
                'artist_id': a['artist_id'],
                'name': a['name'],
                'genre': a['genre']
            })

    return render_template('genres.html', genres=genres, featured_songs=featured_songs, featured_artists=featured_artists)

@app.route('/genres/<int:genre_id>')
def genre_detail_page(genre_id):
    genres = load_genres()
    songs = load_songs()
    artists = load_artists()

    genre = find_genre_by_id(genres, genre_id)
    if not genre:
        abort(404)

    songs_in_genre = []
    for s in songs:
        if s['genre'].lower() == genre['genre_name'].lower():
            artist = next((a for a in artists if a['artist_id'] == s['artist_id']), None)
            artist_name = artist['name'] if artist else 'Unknown Artist'
            songs_in_genre.append({
                'song_id': s['song_id'],
                'title': s['title'],
                'artist_name': artist_name,
                'duration': s['duration']
            })

    artists_in_genre = [a for a in artists if a['genre'].lower() == genre['genre_name'].lower()]

    artists_in_genre_formatted = []
    for a in artists_in_genre:
        artists_in_genre_formatted.append({
            'artist_id': a['artist_id'],
            'name': a['name'],
            'genre': a['genre']
        })

    return render_template('genres.html', genre=genre, songs_in_genre=songs_in_genre, artists_in_genre=artists_in_genre_formatted)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
