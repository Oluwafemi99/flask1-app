from flask import Flask, render_template, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from flask_login import LoginManager
from models import db, User
from forms import RegisterForm
import os

# Initializes the Flask app and sets a secret key for session and CSRF protection.
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
#Configures SQLite as the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# Enables CSRF protection for all forms
app.config['WTF_CSRF_ENABLED'] = True

# Initializes the database
db.init_app(app)

# Initializes Flask-Login and sets the login view for unauthorized users
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login' # type: ignore

# telling flask how to load a user from the database using their ID
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Create database tables within the application context
with app.app_context():
    db.create_all()

# Renders the homepage
@app.route('/')
def home():
    return render_template('home.html')

# Displays the registration form
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_pw = generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful. Please log in.')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
