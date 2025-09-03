from flask import Flask, Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user, LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
from forms import RegisterForm, LoginForm
from models import db, User
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

# Initialize extensions with the app
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
csrf = CSRFProtect()
csrf.init_app(app)

# Create database tables within application context
with app.app_context():
    db.create_all()

# Set the login view for the login manager
login_manager.login_view = 'auth.login' # type: ignore

# Create a Blueprint for the authentication routes
auth = Blueprint('auth', __name__)

# Loads a user from the database using their ID
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# create database tables before the first request
with app.app_context():
    db.create_all()

# Renders the homepage
@auth.route('/')
def home():
    return render_template('home.html')

# Displays the registration form
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.username.data is None or form.password.data is None:
            flash("Username and password are required.")
            return render_template('register.html', form=form)
        hashed_pw = generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_pw)
        hashed_pw = generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful. Please log in.')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

# Displays the login form
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and form.password.data and check_password_hash(
            user.password,form.password.data):
            login_user(user)
            return redirect(url_for('home'))
        flash('Invalid username or password.')
    return render_template('home.html', form=form)

# Displays the dashboard for logged-in users
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('home.html', user=current_user)

# Displays the admin page for users with the 'Admin' role
@app.route('/admin')
@login_required
def admin():
    if current_user.role != 'Admin':
        flash('Access denied.')
        return redirect(url_for('dashboard'))
    return render_template('home.html', user=current_user)

# Logs out the current user and redirects to the homepage
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


app.register_blueprint(auth)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
