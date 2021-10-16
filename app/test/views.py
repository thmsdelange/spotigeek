from flask import Blueprint, render_template
test = Blueprint('test', __name__, template_folder="../templates/test")

@test.route('/')
def index():
    return "<h1>Test page!</h1>"

@test.route('/test-navbar')
def test_navbar():
    return render_template("test.html")