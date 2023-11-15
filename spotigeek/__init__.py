from flask import Flask
from config import get_config
from spotigeek.app.main.views import main
from spotigeek.app.test.views import test

import os
from dotenv import load_dotenv
load_dotenv()

def create_app():
    app = Flask(__name__)
    flask_env = os.environ.get("FLASK_ENV")
    app.config.from_object(get_config(flask_env))
    
    app.register_blueprint(main)
    app.register_blueprint(test, url_prefix='/test')
    return app