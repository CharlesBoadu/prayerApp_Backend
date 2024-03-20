from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'Welcome to the Prayer Application Backend!'

from app.controllers.v1 import login