from flask import Blueprint, redirect, url_for, request, session, render_template, flash
from pandas import DataFrame
import os
from dotenv import load_dotenv
from spotipy import SpotifyOAuth, Spotify
from functools import wraps
from time import sleep, time
main = Blueprint('main', __name__, template_folder="../../templates/main")

def auth_required(f):
    """
    Checks if user has authorized spotify to access user data.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('token_data', None):
            flash("Not authorized")
            return redirect(url_for('main.auth'))
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
            spotify_oauth.refresh_access_token(token_data.get('refresh_token'))
            return redirect(url_for('main.auth'))
        return f(*args, **kwargs)
    return decorated_function

@main.route('/')
@auth_required
@check_token_expired
def index():
    spotify = Spotify(auth=session.get('token_data').get('access_token'))
    now_playing = spotify.current_user_playing_track()
    if now_playing:
        # df_np = DataFrame(now_playing)
        # print(df_np)
        np = {'album_name': now_playing['item']['album']['name'],
                'album_img': now_playing['item']['album']['images'][0]['url'],
                'artist': now_playing['item']['artists'][0]['name'],
                'song': now_playing['item']['name']}
        print(np)
        return render_template("index.html", np=np, sidebar=True)
    else:
        return "Nothing to play"

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

def create_spotify_oauth():
    return SpotifyOAuth(
            client_id=os.environ.get("SPOTIFY_CLIENT_ID"),
            client_secret=os.environ.get("SPOTIFY_CLIENT_SECRET"),
            redirect_uri=url_for('main.callback', _external=True),
            scope='playlist-read-private user-read-private user-read-currently-playing user-library-read user-top-read')