from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import Users
from app.extensions import db
from .forms import RegisterForm, LoginForm

auth_bp = Blueprint('auth', __name__)

# Registration route
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.username.data and form.password.data:
            # Check if username already exists
            existing_user = Users.query.filter_by(username=form.username.data).first()
            if existing_user:
                flash('Username already taken. Please choose another one.', 'error')
                return render_template('register.html', form=form)

            # Hash password and create new user
            hashed_pw = generate_password_hash(form.password.data)
            new_user = Users(username=form.username.data, password=hashed_pw)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful. Please log in.', 'success')
            return redirect(url_for('auth.login'))

    return render_template('register.html', form=form)

    
# login route
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user and form.password.data and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('main.dashboard'))
        flash('Invalid username or password.')
    return render_template('login.html', form=form)

@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
