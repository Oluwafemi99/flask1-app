import os
from flask import Flask
from dotenv import load_dotenv
from app.auth.routes import auth_bp
from app.main.routes import main_bp
from app.extensions import db, login_manager, csrf, migrate

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

    # Initialize extensions with the app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # protect against CSRF attacks
    csrf.init_app(app)

    # Set the login view for the login manager
    login_manager.login_view = 'auth.login' # type: ignore

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    from app.models import Users

    with app.app_context():
        db.create_all()
        print("Database created successfully")
        
    return app
