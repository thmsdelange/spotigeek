from functools import wraps
from flask import session, flash, redirect, url_for
from time import time
from spotigeek.app.main.functions import create_spotify_oauth

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
