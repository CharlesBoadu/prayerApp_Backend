from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return 'Welcome to Backend Development using Python Flask!'