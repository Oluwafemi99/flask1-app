from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .forms import RegisterForm, LoginForm
from .models import User
from . import db, login_manager

# Create a Blueprint for the authentication routes
auth = Blueprint('auth', __name__)

# Loads a user from the database using their ID
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



# Renders the homepage
@auth.route('/')
def home():
    return render_template('home.html')

# Displays the registration form
@auth.route('/register', methods=['GET', 'POST'])
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
@auth.route('/login', methods=['GET', 'POST'])
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
@auth.route('/dashboard')
@login_required
def dashboard():
    return render_template('home.html', user=current_user)
    
# Displays the admin page for users with the 'Admin' role
@auth.route('/admin')
@login_required
def admin():
    if current_user.role != 'Admin':
        flash('Access denied.')
        return redirect(url_for('auth.dashboard'))
    return render_template('home.html', user=current_user)
    
# Logs out the current user and redirects to the homepage
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.home'))
