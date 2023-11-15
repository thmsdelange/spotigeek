from flask import url_for, jsonify
from spotipy import SpotifyOAuth
from time import gmtime, strftime
import os

def create_spotify_oauth():
    return SpotifyOAuth(
            client_id=os.environ.get("SPOTIFY_CLIENT_ID"),
            client_secret=os.environ.get("SPOTIFY_CLIENT_SECRET"),
            redirect_uri=url_for('main.callback', _external=True),
            scope='playlist-read-private user-read-private user-read-currently-playing user-library-read user-top-read')

def get_now_playing(spotify):
    now_playing = spotify.current_user_playing_track()
    if now_playing:   
        item = now_playing['item']
        album = item['album']
        album_tracks_items = spotify.album_tracks(album['id'])
        return jsonify(track_name = item['name'],
                        track_external_url= item['external_urls']['spotify'],
                        track_number = item['track_number'],
                        album_name = album['name'],
                        album_img = album['images'][0]['url'],
                        album_artists = ", ".join([artist['name'] for artist in album['artists']]),
                        album_tracks = {album_track['track_number']: 
                                        {'name': album_track['name'], 
                                        'duration': ms_to_min_sec(album_track['duration_ms']),
                                        'artists': ", ".join(artist['name'] for artist in album_track['artists']),
                                        'explicit': album_track['explicit']
                                        } for album_track in album_tracks_items['items']},
                        album_release_year = album['release_date'][:4],
                        album_total_tracks = album['total_tracks'])
    else:
        return jsonify(error= "no data")

def ms_to_min_sec(ms):
    return strftime("%M:%S", gmtime(ms/1000))