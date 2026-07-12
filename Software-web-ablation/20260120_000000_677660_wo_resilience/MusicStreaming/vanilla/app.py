from flask import Flask, render_template, request, redirect, url_for, abort
import os
from datetime import datetime

app = Flask(__name__)

# Data file paths
SONGS_FILE = 'data/songs.txt'
ARTISTS_FILE = 'data/artists.txt'
ALBUMS_FILE = 'data/albums.txt'
GENRES_FILE = 'data/genres.txt'
PLAYLISTS_FILE = 'data/playlists.txt'
PLAYLIST_SONGS_FILE = 'data/playlist_songs.txt'


# Utility functions to load data from files

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
            except:
                continue
    return songs


def save_songs(songs):
    with open(SONGS_FILE, 'w', encoding='utf-8') as f:
        for s in songs:
            line = f"{s['song_id']}|{s['title']}|{s['artist_id']}|{s['album_id']}|{s['genre']}|{s['duration']}|{s['release_date']}|{s['play_count']}"
            f.write(line + '\n')


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
            except:
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
            except:
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
                genre_id = int(parts[0])
                genre_name = parts[1]
                description = parts[2]
                genres.append({
                    'genre_id': genre_id,
                    'genre_name': genre_name,
                    'description': description
                })
            except:
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
            except:
                continue
    return playlists


def save_playlists(playlists):
    with open(PLAYLISTS_FILE, 'w', encoding='utf-8') as f:
        for p in playlists:
            line = f"{p['playlist_id']}|{p['title']}|{p['description']}|{p['creation_date']}|{p['total_songs']}"
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
            except:
                continue
    return playlist_songs


def save_playlist_songs(playlist_songs):
    with open(PLAYLIST_SONGS_FILE, 'w', encoding='utf-8') as f:
        for ps in playlist_songs:
            line = f"{ps['playlist_song_id']}|{ps['playlist_id']}|{ps['song_id']}|{ps['added_date']}"
            f.write(line + '\n')


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


def get_playlist_by_id(playlist_id):
    playlists = load_playlists()
    for playlist in playlists:
        if playlist['playlist_id'] == playlist_id:
            return playlist
    return None


def get_next_playlist_id():
    playlists = load_playlists()
    if not playlists:
        return 1
    return max(p['playlist_id'] for p in playlists) + 1


def get_next_playlist_song_id():
    playlist_songs = load_playlist_songs()
    if not playlist_songs:
        return 1
    return max(ps['playlist_song_id'] for ps in playlist_songs) + 1


# Section 1: Flask Routes Implementation

@app.route('/')
def root_redirect():
    # Redirect to dashboard page
    return redirect(url_for('dashboard_page'))


@app.route('/dashboard')
def dashboard_page():
    # featured_songs: list of dict {song_id: int, title: str, artist_name: str, duration: int}
    # trending_artists: list of dict {artist_id: int, name: str}
    songs = load_songs()
    artists = load_artists()

    # For featured songs, we pick top 5 songs by play_count
    top_songs = sorted(songs, key=lambda s: s['play_count'], reverse=True)[:5]
    featured_songs = []
    for s in top_songs:
        artist = get_artist_by_id(s['artist_id'])
        artist_name = artist['name'] if artist else 'Unknown Artist'
        featured_songs.append({
            'song_id': s['song_id'],
            'title': s['title'],
            'artist_name': artist_name,
            'duration': s['duration']
        })

    # For trending artists, top 5 artists by total play counts of their songs
    artist_play_counts = {}
    for s in songs:
        artist_play_counts[s['artist_id']] = artist_play_counts.get(s['artist_id'], 0) + s['play_count']
    sorted_artist_counts = sorted(artist_play_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    trending_artists = []
    for artist_id, _ in sorted_artist_counts:
        artist = get_artist_by_id(artist_id)
        if artist:
            trending_artists.append({'artist_id': artist_id, 'name': artist['name']})

    return render_template('dashboard.html', featured_songs=featured_songs, trending_artists=trending_artists)


@app.route('/songs', methods=['GET', 'POST'])
def song_catalog():
    songs = load_songs()
    artists = load_artists()
    albums = load_albums()

    songs_lookup = {s['song_id']: s for s in songs}
    artists_lookup = {a['artist_id']: a for a in artists}
    albums_lookup = {al['album_id']: al for al in albums}

    filter_genre = None
    search_query = None

    # POST method may be used for add to playlist action, but spec says add-to-playlist is a function (likely AJAX or form), no route specified to handle adding to playlist here
    # So here, only implement GET for displaying filtered songs
    if request.method == 'POST':
        # See if any form inputs for filtering or search
        filter_genre = request.form.get('filter_genre') or request.args.get('filter_genre')
        if not filter_genre:
            filter_genre = None
        search_query = request.form.get('search_query') or request.args.get('search_query')
        if search_query:
            search_query = search_query.strip().lower()
        else:
            search_query = None

    else:
        filter_genre = request.args.get('filter_genre')
        if filter_genre == '':
            filter_genre = None
        search_query = request.args.get('search_query')
        if search_query:
            search_query = search_query.strip().lower()
        else:
            search_query = None

    filtered_songs = []
    for s in songs:
        genre_match = True
        if filter_genre is not None:
            genre_match = (s['genre'].lower() == filter_genre.lower())
        search_match = True
        if search_query is not None:
            search_match = (search_query in s['title'].lower()) or (search_query in artists_lookup.get(s['artist_id'], {}).get('name', '').lower())

        if genre_match and search_match:
            artist_name = artists_lookup.get(s['artist_id'], {}).get('name', 'Unknown Artist')
            album_name = albums_lookup.get(s['album_id'], {}).get('title', 'Unknown Album')
            filtered_songs.append({
                'song_id': s['song_id'],
                'title': s['title'],
                'artist_name': artist_name,
                'album_name': album_name,
                'genre': s['genre'],
                'duration': s['duration']
            })

    return render_template('song_catalog.html', songs=filtered_songs, filter_genre=filter_genre, search_query=search_query)


@app.route('/songs/<int:song_id>')
def song_details(song_id):
    song = get_song_by_id(song_id)
    if not song:
        abort(404)
    artist = get_artist_by_id(song['artist_id'])
    album = get_album_by_id(song['album_id'])
    if artist is None:
        artist = {'artist_id': 0, 'name': 'Unknown Artist'}
    if album is None:
        album = {'album_id':0, 'title': 'Unknown Album'}

    song_context = {
        'song_id': song['song_id'],
        'title': song['title'],
        'artist_id': artist['artist_id'],
        'artist_name': artist['name'],
        'album_id': album['album_id'],
        'album_name': album['title'],
        'genre': song['genre'],
        'duration': song['duration']
    }
    release_date = song['release_date']
    play_count = song['play_count']
    return render_template('song_details.html', song=song_context, release_date=release_date, play_count=play_count)


@app.route('/playlists')
def playlists():
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


@app.route('/playlists/<int:playlist_id>', methods=['GET', 'POST'])
def playlist_details(playlist_id):
    # GET: show playlist and songs
    # POST: expect form to remove songs or delete playlist
    playlist = get_playlist_by_id(playlist_id)
    if not playlist:
        abort(404)

    if request.method == 'POST':
        # Determine if removing song or deleting playlist
        if 'remove_song_id' in request.form:
            remove_song_id = request.form.get('remove_song_id')
            try:
                remove_song_id = int(remove_song_id)
            except:
                remove_song_id = None

            if remove_song_id is not None:
                playlist_songs = load_playlist_songs()
                # Remove the record linking this song and playlist
                new_playlist_songs = [ps for ps in playlist_songs if not (ps['playlist_id'] == playlist_id and ps['song_id'] == remove_song_id)]
                if len(new_playlist_songs) != len(playlist_songs):
                    save_playlist_songs(new_playlist_songs)

                    # Update playlist total songs count
                    playlists = load_playlists()
                    for p in playlists:
                        if p['playlist_id'] == playlist_id:
                            p['total_songs'] = max(0, p['total_songs'] - 1)
                    save_playlists(playlists)

            return redirect(url_for('playlist_details', playlist_id=playlist_id))

        elif 'delete_playlist' in request.form:
            # Delete playlist and all its songs
            playlist_id_to_delete = playlist_id
            playlists = load_playlists()
            playlists = [p for p in playlists if p['playlist_id'] != playlist_id_to_delete]
            save_playlists(playlists)

            playlist_songs = load_playlist_songs()
            playlist_songs = [ps for ps in playlist_songs if ps['playlist_id'] != playlist_id_to_delete]
            save_playlist_songs(playlist_songs)

            return redirect(url_for('playlists'))

    # GET method
    playlist_context = {
        'playlist_id': playlist['playlist_id'],
        'title': playlist['title'],
        'description': playlist['description']
    }

    playlist_songs = load_playlist_songs()
    songs = load_songs()
    artists = load_artists()
    artists_lookup = {a['artist_id']: a for a in artists}
    songs_in_playlist = []
    for ps in playlist_songs:
        if ps['playlist_id'] == playlist_id:
            song = next((s for s in songs if s['song_id'] == ps['song_id']), None)
            if song:
                artist_name = artists_lookup.get(song['artist_id'], {}).get('name', 'Unknown Artist')
                songs_in_playlist.append({
                    'song_id': song['song_id'],
                    'title': song['title'],
                    'artist_name': artist_name,
                    'duration': song['duration']
                })

    return render_template('playlist_details.html', playlist=playlist_context, songs=songs_in_playlist)


@app.route('/playlists/create', methods=['GET', 'POST'])
def create_playlist():
    if request.method == 'GET':
        return render_template('create_playlist.html')

    # POST method: create new playlist
    title = request.form.get('playlist-name-input', '').strip()
    description = request.form.get('playlist-description-input', '').strip()

    if not title:
        # Could add flash message, but spec does not mention error messages
        return render_template('create_playlist.html')

    playlists = load_playlists()
    new_playlist_id = get_next_playlist_id()
    creation_date = datetime.now().strftime('%Y-%m-%d')
    new_playlist = {
        'playlist_id': new_playlist_id,
        'title': title,
        'description': description,
        'creation_date': creation_date,
        'total_songs': 0
    }
    playlists.append(new_playlist)
    save_playlists(playlists)

    return redirect(url_for('playlists'))


@app.route('/albums')
def albums():
    albums = load_albums()
    artists = load_artists()
    artists_lookup = {a['artist_id']: a for a in artists}

    albums_context = []
    for al in albums:
        artist_name = artists_lookup.get(al['artist_id'], {}).get('name', 'Unknown Artist')
        albums_context.append({
            'album_id': al['album_id'],
            'title': al['title'],
            'artist_name': artist_name,
            'release_year': al['release_year'],
            'genre': al['genre']
        })
    return render_template('albums.html', albums=albums_context)


@app.route('/albums/<int:album_id>')
def album_details(album_id):
    album = get_album_by_id(album_id)
    if not album:
        abort(404)
    songs = load_songs()
    album_songs = [s for s in songs if s['album_id'] == album_id]

    album_context = {
        'album_id': album['album_id'],
        'title': album['title'],
        'artist_name': get_artist_by_id(album['artist_id'])['name'] if get_artist_by_id(album['artist_id']) else 'Unknown Artist',
        'release_year': album['release_year']
    }
    songs_context = []
    for s in album_songs:
        songs_context.append({
            'song_id': s['song_id'],
            'title': s['title'],
            'duration': s['duration']
        })
    return render_template('album_details.html', album=album_context, songs=songs_context)


@app.route('/artists')
def artists():
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
    artist = get_artist_by_id(artist_id)
    if not artist:
        abort(404)

    songs = load_songs()
    artist_songs = []
    albums = load_albums()
    albums_lookup = {al['album_id']: al for al in albums}

    for s in songs:
        if s['artist_id'] == artist_id:
            album_name = albums_lookup.get(s['album_id'], {}).get('title', 'Unknown Album')
            artist_songs.append({
                'song_id': s['song_id'],
                'title': s['title'],
                'album_name': album_name
            })

    artist_context = {
        'artist_id': artist['artist_id'],
        'name': artist['name'],
        'genre': artist['genre'],
        'country': artist['country'],
        'formation_year': artist['formation_year']
    }

    return render_template('artist_profile.html', artist=artist_context, songs=artist_songs)


@app.route('/genres')
def genres():
    genres = load_genres()

    # Parse selected genre id
    selected_genre_id = request.args.get('selected_genre_id')
    try:
        selected_genre_id = int(selected_genre_id) if selected_genre_id is not None else None
    except:
        selected_genre_id = None

    genre_songs = []
    genre_artists = []

    if selected_genre_id is not None:
        genre_obj = next((g for g in genres if g['genre_id'] == selected_genre_id), None)
        if genre_obj is not None:
            selected_genre_name = genre_obj['genre_name']
            songs = load_songs()
            artists = load_artists()

            # Filter songs with this genre
            genre_songs_filtered = [s for s in songs if s['genre'].lower() == selected_genre_name.lower()]

            artist_ids_set = set()
            for s in genre_songs_filtered:
                genre_songs.append({
                    'song_id': s['song_id'],
                    'title': s['title']
                })
                artist_ids_set.add(s['artist_id'])

            for a in artists:
                if a['artist_id'] in artist_ids_set:
                    genre_artists.append({
                        'artist_id': a['artist_id'],
                        'name': a['name']
                    })
    else:
        selected_genre_id = None

    return render_template('genres.html', genres=genres, selected_genre_id=selected_genre_id, genre_songs=genre_songs, genre_artists=genre_artists)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
