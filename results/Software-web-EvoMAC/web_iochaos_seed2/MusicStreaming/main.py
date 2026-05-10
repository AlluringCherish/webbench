'''
Main backend application for MusicStreaming web app.
Defines the root route '/' to serve the Dashboard page as required.
Loads featured songs and trending artists from data files and renders dashboard.html.
'''
from flask import Flask, render_template, url_for
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
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 8:
                    continue
                song = {
                    'song_id': parts[0],
                    'title': parts[1],
                    'artist_id': parts[2],
                    'album_id': parts[3],
                    'genre': parts[4],
                    'duration': int(parts[5]),
                    'release_date': parts[6],
                    'play_count': int(parts[7])
                }
                songs.append(song)
    except FileNotFoundError:
        pass
    return songs
def load_artists():
    artists = {}
    try:
        with open(os.path.join(DATA_DIR, 'artists.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 5:
                    continue
                artist = {
                    'artist_id': parts[0],
                    'name': parts[1],
                    'genre': parts[2],
                    'country': parts[3],
                    'formation_year': parts[4]
                }
                artists[artist['artist_id']] = artist
    except FileNotFoundError:
        pass
    return artists
def load_featured_songs():
    # For simplicity, featured songs are top 5 by play_count
    songs = load_songs()
    songs_sorted = sorted(songs, key=lambda s: s['play_count'], reverse=True)
    featured = songs_sorted[:5]
    artists = load_artists()
    # Add artist name to each song
    for song in featured:
        artist = artists.get(song['artist_id'])
        song['artist_name'] = artist['name'] if artist else 'Unknown Artist'
    return featured
def load_trending_artists():
    # For simplicity, trending artists are top 5 by total play_count of their songs
    songs = load_songs()
    artists = load_artists()
    play_counts = {}
    for song in songs:
        aid = song['artist_id']
        play_counts[aid] = play_counts.get(aid, 0) + song['play_count']
    trending = sorted(play_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    trending_artists = []
    for aid, count in trending:
        artist = artists.get(aid)
        if artist:
            trending_artists.append({
                'artist_id': aid,
                'name': artist['name'],
                'genre': artist['genre'],
                'play_count': count
            })
    return trending_artists
@app.route('/')
def dashboard():
    featured_songs = load_featured_songs()
    trending_artists = load_trending_artists()
    return render_template('dashboard.html', featured_songs=featured_songs, trending_artists=trending_artists)
# Additional routes would be defined here for other pages...
if __name__ == '__main__':
    app.run(debug=True)