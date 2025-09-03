import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv
from app.auth.routes import auth_bp
from app.main.routes import main_bp

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

    # Initialize extensions with the app
    db.init_app(app)
    login_manager.init_app(app)

    # protect against CSRF attacks
    csrf.init_app(app)

    # Set the login view for the login manager
    login_manager.login_view = 'auth.login' # type: ignore

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    with app.app_context():
        db.create_all()

    return app
