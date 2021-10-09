import os
from dotenv import load_dotenv
from flask import Flask, request, url_for, session, redirect

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")
app.config['SESSION_COOKIE_NAME'] = os.getenv("FLASK_SESSION_COOKIE_NAME")

@app.route('/')
def index():
    return 'Hello World'

if __name__=='__main__':
    app.run(debug=True)