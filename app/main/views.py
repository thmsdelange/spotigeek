from flask import Blueprint, redirect, url_for, request, session, render_template, flash
import os
from dotenv import load_dotenv
from spotipy import SpotifyOAuth, Spotify
from functools import wraps
from time import time

import spotipy
main = Blueprint('main', __name__, template_folder="templates")

def auth_required(f):
    """
    Checks if user has authorized spotify to access user data.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('token_data', None):
            flash("Not authorized")
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

def check_token_expired(f):
    """
    Checks if access token needs to be refreshed and creates a new access token if necessary. Must be used after @auth_required
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token_data = session.get('token_data')
        if token_data.get('expires_at') - int(time()) < 60:
            spotify_oauth = create_spotify_oauth()
            return spotify_oauth.refresh_access_token(token_data.get('refresh_token'))
        return f(*args, **kwargs)
    return decorated_function

@main.route('/')
def index():
    return render_template("index.html")

@main.route('/authorize')
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
    return redirect(url_for('main.now_playing', _external=True))

@main.route('/now-playing')
@auth_required
@check_token_expired
def now_playing():
    spotify = Spotify(auth=session.get('token_data').get('access_token'))
    now_playing = spotify.current_user_playing_track()
    return "Now Playing: " + now_playing['item']['name']

def create_spotify_oauth():
    return SpotifyOAuth(
            client_id=os.environ.get("SPOTIFY_CLIENT_ID"),
            client_secret=os.environ.get("SPOTIFY_CLIENT_SECRET"),
            redirect_uri=url_for('main.callback', _external=True),
            scope='playlist-read-private user-read-private user-read-currently-playing user-library-read user-top-read')