from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'Welcome to the Prayer Application Backend! 🙏🏽'

if __name__ == '__main__':
    app.run(debug=True)


from app.controllers.v1 import login
from app.controllers.v1 import register
from app.controllers.v1 import reset_password