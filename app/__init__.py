# import os
# from flask import Flask
# from app.views import auth
# from flask_mail import Mail
# from dotenv import load_dotenv


# # Load environment variables from .env file
# load_dotenv()

# # # mail configuration
# # os.getenv['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
# # os.getenv['MAIL_PORT'] = os.getenv('MAIL_PORT')
# # os.getenv['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS')
# # # os.getenv['MAIL_USE_SSL'] = MAIL_USE_SSL
# # os.getenv['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
# # os.getenv['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')

# def create_app(test_config=None):
#     app = Flask(__name__)

#     #initializations
#     mail = Mail(app)


#     @app.route('/')
#     def index():
#         return 'Welcome to the Prayer Application Backend! 🙏🏽'

#     app.register_blueprint(auth.auth_bp)
#     return app