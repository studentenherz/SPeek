'''
	Run the application with gunicorn speek:app
'''

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
from flask_bcrypt import Bcrypt
from flask_socketio import SocketIO

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
socketio = SocketIO()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = os.getenv('SPEEK_KEY', 'default_secret_key_not_very_secret')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
bcrypt.init_app(app)
socketio.init_app(app)

login_manager.init_app(app)
login_manager.login_view = 'auth.login'


from .main import main as main_blueprint
app.register_blueprint(main_blueprint)

from .auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)