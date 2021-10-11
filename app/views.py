from app import app
from flask import redirect, url_for, request, render_template, flash
import os
from dotenv import load_dotenv
from spotipy import SpotifyOAuth

def create_spotify_oauth():
    return SpotifyOAuth(
            client_id=os.environ.get("SPOTIFY_CLIENT_ID"),
            client_secret=os.environ.get("SPOTIFY_CLIENT_SECRET"),
            redirect_uri=url_for('redirect_auth', _external=True),
            scope="user-library-read")

@app.route('/')
def login():
    print(app.config)
    spotify_oauth = create_spotify_oauth()
    auth_url = spotify_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/callback')
def redirect_auth():
    return 'Redirected'