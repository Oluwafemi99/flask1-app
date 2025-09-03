from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from .routes import auth
import os

# Initialize sql extensions
db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()

# Create Flask app and configure it
def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY= os.environ['SECRET_KEY'],
        SQLALCHEMY_DATABASE_URI='sqlite:///users.db',
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )

    # Initialize extensions with the app
    db.init_app(app)
    login_manager.init_app(app)
    
    # protect against CSRF attacks
    csrf.init_app(app)
    
    # Set the login view for the login manager
    login_manager.login_view = 'auth.login' # type: ignore

    app.register_blueprint(auth)

    with app.app_context():
        db.create_all()

    return app
