from flask import Blueprint, redirect, url_for, request, session, render_template, flash, jsonify
from pandas import DataFrame
import os
from dotenv import load_dotenv
from spotipy import SpotifyOAuth, Spotify
from time import sleep, time
import json

from spotigeek.app.main.decorators import auth_required, check_token_expired
from spotigeek.app.main.functions import create_spotify_oauth, get_now_playing

main = Blueprint('main', __name__, template_folder="../../templates/main")

@main.route('/')
@auth_required
@check_token_expired
def index():
    spotify = Spotify(auth=session.get('token_data').get('access_token'))
    now_playing = get_now_playing(spotify).get_json()
    # print(now_playing)
    return render_template("index.html", sidebar=True, now_playing=now_playing)

@main.route('/authorize')
def auth():
    return render_template("auth.html", sidebar=True)

@main.route('/spotify-oauth')
def authorize():
    spotify_oauth = create_spotify_oauth()
    auth_url = spotify_oauth.get_authorize_url()
    return redirect(auth_url)

@main.route('/callback')
def callback():
    spotify_oath = create_spotify_oauth()
    session.clear()
    code = request.args.get('code')
    session['token_data'] = spotify_oath.get_access_token(code)
    return redirect(url_for('main.index', _external=True))

@main.route('/logout')
def logout():
    session.pop('token_data')
    return redirect(url_for('main.auth'))

@main.route('/top')
@auth_required
@check_token_expired
def top():
    spotify = Spotify(auth=session.get('token_data').get('access_token'))
    user_top = spotify.current_user_top_tracks(limit=50, time_range="long_term")
    return {"top": user_top['items']}

@main.route('/now-playing')
@auth_required
@check_token_expired
def now_playing():
    sp = Spotify(auth=session.get('token_data').get('access_token'))
    np = get_now_playing(sp)
    # np = sp.current_user_playing_track()
    # album = sp.album_tracks("3cLQ49Ll3nGRkw3HSSk92K")
    return np