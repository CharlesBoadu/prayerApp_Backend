from flask import Flask
from flask_mail import Mail
from app.config import MAIL_SERVER, MAIL_PORT, MAIL_USE_TLS, MAIL_USERNAME, MAIL_PASSWORD
from flask_cors import CORS


app = Flask(__name__)

# mail configuration
app.config['MAIL_SERVER'] = MAIL_SERVER
app.config['MAIL_PORT'] = MAIL_PORT
app.config['MAIL_USE_TLS'] = MAIL_USE_TLS
# app.config['MAIL_USE_SSL'] = MAIL_USE_SSL
app.config['MAIL_USERNAME'] = MAIL_USERNAME
app.config['MAIL_PASSWORD'] = MAIL_PASSWORD


#initializations
mail = Mail(app)
CORS(app)


@app.route('/')
def index():
    return 'Welcome to the Prayer Application Backend! 🙏🏽'

if __name__ == '__main__':
    app.run(debug=True)


from app.controllers.v1 import auth
from app.controllers.v1 import profile
from app.controllers.v1 import prayers
from app.controllers.v1 import users
from app.controllers.v1 import organization