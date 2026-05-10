'''
Main backend application for MusicStreaming web app.
Defines routes for all ten pages as required by the specifications.
Each route loads necessary data from local text files and renders the corresponding template.
'''
from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime
app = Flask(__name__)
DATA_DIR = 'data'
def load_songs():
    songs = []
    try:
        with open(os.path.join(DATA_DIR, 'songs.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    song_id, title, artist_id, album_id, genre, duration, release_date, play_count = line.split('|')
                    songs.append({
                        'song_id': song_id,
                        'title': title,
                        'artist_id': artist_id,
                        'album_id': album_id,
                        'genre': genre,
                        'duration': int(duration),
                        'release_date': release_date,
                        'play_count': int(play_count)
                    })
    except FileNotFoundError:
        pass
    return songs
def load_artists():
    artists = []
    try:
        with open(os.path.join(DATA_DIR, 'artists.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    artist_id, name, genre, country, formation_year = line.split('|')
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
                line = line.strip()
                if line:
                    album_id, title, artist_id, release_year, total_songs, genre = line.split('|')
                    albums.append({
                        'album_id': album_id,
                        'title': title,
                        'artist_id': artist_id,
                        'release_year': release_year,
                        'total_songs': int(total_songs),
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
                line = line.strip()
                if line:
                    genre_id, genre_name, description = line.split('|')
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
                line = line.strip()
                if line:
                    playlist_id, title, description, creation_date, total_songs = line.split('|')
                    playlists.append({
                        'playlist_id': playlist_id,
                        'title': title,
                        'description': description,
                        'creation_date': creation_date,
                        'total_songs': int(total_songs)
                    })
    except FileNotFoundError:
        pass
    return playlists
def load_playlist_songs():
    playlist_songs = []
    try:
        with open(os.path.join(DATA_DIR, 'playlist_songs.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    playlist_song_id, playlist_id, song_id, added_date = line.split('|')
                    playlist_songs.append({
                        'playlist_song_id': playlist_song_id,
                        'playlist_id': playlist_id,
                        'song_id': song_id,
                        'added_date': added_date
                    })
    except FileNotFoundError:
        pass
    return playlist_songs
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
@app.route('/')
@app.route('/dashboard')
def dashboard():
    '''
    Route for the root URL '/' and '/dashboard' serving the Dashboard page.
    Loads featured songs and trending artists for display.
    '''
    songs = load_songs()
    artists = load_artists()
    # Featured songs: top 5 by play_count descending
    featured_songs = sorted(songs, key=lambda s: s['play_count'], reverse=True)[:5]
    # Trending artists: top 5 by total play_count of their songs
    artist_play_counts = {}
    for song in songs:
        artist_play_counts[song['artist_id']] = artist_play_counts.get(song['artist_id'], 0) + song['play_count']
    trending_artists = sorted(artists, key=lambda a: artist_play_counts.get(a['artist_id'], 0), reverse=True)[:5]
    # Enrich featured songs with artist and album names
    for song in featured_songs:
        artist = get_artist_by_id(song['artist_id'])
        album = get_album_by_id(song['album_id'])
        song['artist_name'] = artist['name'] if artist else 'Unknown Artist'
        song['album_name'] = album['title'] if album else 'Unknown Album'
    return render_template('dashboard.html',
                           featured_songs=featured_songs,
                           trending_artists=trending_artists)
@app.route('/songs')
def song_catalog():
    '''
    Route for Song Catalog page.
    Supports optional search and genre filter via query parameters.
    '''
    songs = load_songs()
    artists = load_artists()
    albums = load_albums()
    genres = load_genres()
    search_query = request.args.get('search', '').lower()
    genre_filter = request.args.get('genre', '').lower()
    filtered_songs = []
    for song in songs:
        artist = get_artist_by_id(song['artist_id'])
        album = get_album_by_id(song['album_id'])
        # Prepare searchable fields
        title = song['title'].lower()
        artist_name = artist['name'].lower() if artist else ''
        album_name = album['title'].lower() if album else ''
        genre = song['genre'].lower()
        # Filter by search query
        if search_query:
            if search_query not in title and search_query not in artist_name and search_query not in album_name:
                continue
        # Filter by genre
        if genre_filter and genre_filter != 'all':
            if genre != genre_filter:
                continue
        # Enrich song data
        song['artist_name'] = artist['name'] if artist else 'Unknown Artist'
        song['album_name'] = album['title'] if album else 'Unknown Album'
        filtered_songs.append(song)
    # Prepare genre list for dropdown (include 'All' option)
    genre_names = ['All'] + [g['genre_name'] for g in genres]
    return render_template('song_catalog.html',
                           songs=filtered_songs,
                           genres=genre_names,
                           selected_genre=genre_filter if genre_filter else 'all',
                           search_query=search_query)
@app.route('/song/<song_id>')
def song_details(song_id):
    '''
    Route for Song Details page.
    Displays detailed information about a specific song.
    '''
    song = get_song_by_id(song_id)
    if not song:
        return "Song not found", 404
    artist = get_artist_by_id(song['artist_id'])
    album = get_album_by_id(song['album_id'])
    song['artist_name'] = artist['name'] if artist else 'Unknown Artist'
    song['album_name'] = album['title'] if album else 'Unknown Album'
    return render_template('song_details.html', song=song)
@app.route('/playlists')
def playlists():
    '''
    Route for Playlist page.
    Displays all user-created playlists.
    '''
    playlists = load_playlists()
    return render_template('playlists.html', playlists=playlists)
@app.route('/playlist/<playlist_id>')
def playlist_details(playlist_id):
    '''
    Route for Playlist Details page.
    Displays songs in a specific playlist with management options.
    '''
    playlist = get_playlist_by_id(playlist_id)
    if not playlist:
        return "Playlist not found", 404
    playlist_songs = load_playlist_songs()
    songs = load_songs()
    artists = load_artists()
    # Filter songs in this playlist
    songs_in_playlist = []
    for ps in playlist_songs:
        if ps['playlist_id'] == playlist_id:
            song = get_song_by_id(ps['song_id'])
            if song:
                artist = get_artist_by_id(song['artist_id'])
                song['artist_name'] = artist['name'] if artist else 'Unknown Artist'
                songs_in_playlist.append(song)
    return render_template('playlist_details.html',
                           playlist=playlist,
                           songs_in_playlist=songs_in_playlist)
@app.route('/create-playlist', methods=['GET', 'POST'])
def create_playlist():
    '''
    Route for Create Playlist page.
    GET: Show form to create new playlist.
    POST: Save new playlist to playlists.txt and redirect to playlists page.
    '''
    if request.method == 'POST':
        title = request.form.get('playlist_name', '').strip()
        description = request.form.get('playlist_description', '').strip()
        if not title:
            error = "Playlist name is required."
            return render_template('create_playlist.html', error=error, title=title, description=description)
        playlists = load_playlists()
        # Generate new playlist_id
        if playlists:
            max_id = max(int(p['playlist_id']) for p in playlists)
            new_id = str(max_id + 1)
        else:
            new_id = '1'
        creation_date = datetime.now().strftime('%Y-%m-%d')
        total_songs = 0
        # Append new playlist to file
        with open(os.path.join(DATA_DIR, 'playlists.txt'), 'a', encoding='utf-8') as f:
            f.write(f"{new_id}|{title}|{description}|{creation_date}|{total_songs}\n")
        return redirect(url_for('playlists'))
    else:
        return render_template('create_playlist.html')
@app.route('/albums')
def albums():
    '''
    Route for Album Browse page.
    Supports optional search and sort via query parameters.
    '''
    albums = load_albums()
    artists = load_artists()
    search_query = request.args.get('search', '').lower()
    sort_option = request.args.get('sort', 'By Title')
    filtered_albums = []
    for album in albums:
        artist = get_artist_by_id(album['artist_id'])
        title = album['title'].lower()
        artist_name = artist['name'].lower() if artist else ''
        # Filter by search query
        if search_query:
            if search_query not in title and search_query not in artist_name:
                continue
        album['artist_name'] = artist['name'] if artist else 'Unknown Artist'
        filtered_albums.append(album)
    # Sort albums
    if sort_option == 'By Title':
        filtered_albums.sort(key=lambda a: a['title'].lower())
    elif sort_option == 'By Artist':
        filtered_albums.sort(key=lambda a: a['artist_name'].lower())
    elif sort_option == 'By Year':
        filtered_albums.sort(key=lambda a: a['release_year'])
    return render_template('albums.html',
                           albums=filtered_albums,
                           search_query=search_query,
                           sort_option=sort_option)
@app.route('/album/<album_id>')
def album_details(album_id):
    '''
    Route for Album Details page.
    Displays all songs in a specific album.
    '''
    album = get_album_by_id(album_id)
    if not album:
        return "Album not found", 404
    artist = get_artist_by_id(album['artist_id'])
    songs = load_songs()
    # Filter songs in this album
    album_songs = []
    for song in songs:
        if song['album_id'] == album_id:
            artist_song = get_artist_by_id(song['artist_id'])
            song['artist_name'] = artist_song['name'] if artist_song else 'Unknown Artist'
            album_songs.append(song)
    return render_template('album_details.html',
                           album=album,
                           artist=artist,
                           album_songs=album_songs)
@app.route('/artists')
def artists():
    '''
    Route for Artist Profile page.
    Supports optional search and sort via query parameters.
    '''
    artists = load_artists()
    search_query = request.args.get('search', '').lower()
    sort_option = request.args.get('sort', 'By Name')
    filtered_artists = []
    for artist in artists:
        name = artist['name'].lower()
        genre = artist['genre'].lower()
        if search_query:
            if search_query not in name:
                continue
        filtered_artists.append(artist)
    # Sort artists
    if sort_option == 'By Name':
        filtered_artists.sort(key=lambda a: a['name'].lower())
    elif sort_option == 'By Genre':
        filtered_artists.sort(key=lambda a: a['genre'].lower())
    return render_template('artists.html',
                           artists=filtered_artists,
                           search_query=search_query,
                           sort_option=sort_option)
@app.route('/artist/<artist_id>')
def artist_profile(artist_id):
    '''
    Route for individual Artist Profile page.
    Displays artist information and their songs.
    '''
    artist = get_artist_by_id(artist_id)
    if not artist:
        return "Artist not found", 404
    songs = load_songs()
    artist_songs = [song for song in songs if song['artist_id'] == artist_id]
    albums = load_albums()
    artist_albums = [album for album in albums if album['artist_id'] == artist_id]
    return render_template('artist_profile.html',
                           artist=artist,
                           songs=artist_songs,
                           albums=artist_albums)
@app.route('/genres')
def genres():
    '''
    Route for Genre Exploration page.
    Supports optional genre selection via query parameter.
    '''
    genres = load_genres()
    selected_genre = request.args.get('genre', '')
    songs = load_songs()
    artists = load_artists()
    genre_songs = []
    genre_artists = []
    if selected_genre:
        # Filter songs by genre
        genre_songs = [song for song in songs if song['genre'].lower() == selected_genre.lower()]
        # Filter artists by genre
        genre_artists = [artist for artist in artists if artist['genre'].lower() == selected_genre.lower()]
        # Enrich songs with artist names
        for song in genre_songs:
            artist = get_artist_by_id(song['artist_id'])
            song['artist_name'] = artist['name'] if artist else 'Unknown Artist'
    return render_template('genres.html',
                           genres=genres,
                           selected_genre=selected_genre,
                           genre_songs=genre_songs,
                           genre_artists=genre_artists)
if __name__ == '__main__':
    app.run(debug=True)