from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user

# Create a Blueprint for the main routes
main_bp = Blueprint('main', __name__)

# Renders the homepage
@main_bp.route('/')
def home():
    return render_template('home.html')

# Displays the dashboard for logged-in users
@main_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)

# Displays the admin page for users with the 'Admin' role
@main_bp.route('/admin')
@login_required
def admin():
    if current_user.role != 'Admin':
        flash('Access denied.')
        return redirect(url_for('main.dashboard'))
    return render_template('dashboard.html', user=current_user)
