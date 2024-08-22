from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from config.setting import Config
from services import app_service
app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Import and Register Blueprints
from controllers.user_controller import user_bp
from controllers.event_controller import event_bp
from controllers.admin_controller import admin_bp
from controllers.category_controller import category_bp

app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(event_bp, url_prefix='/event')
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(category_bp, url_prefix='/category')

# Import models
from models.user_model import User


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(login=username).first()
        if user and user.password == password:  # Directly compare the plain text password
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials')
    return render_template('front/login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        role = request.form['role']  # Handle role from dropdown
        
        if password != confirm_password:
            flash('Passwords do not match.')
            return redirect(url_for('register'))
        
        existing_user = User.query.filter_by(login=username).first()
        if existing_user:
            flash('Username already exists')
            return redirect(url_for('register'))

        user = User(name=username, login=username, role=role)
        user.password = password  # Directly store the plain text password for now
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please login.')
        return redirect(url_for('login'))
    return render_template('front/register.html')

@app.route('/')
def home():
    events = app_service.get_all_events()  # Fetch all events to display on the homepage
    return render_template('front/home.html', events=events)

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        current_user.name = request.form['name']
        current_user.pic = request.form['pic']
        current_user.desc = request.form['desc']
        db.session.commit()
        flash('Profile updated successfully!')
        return redirect(url_for('profile'))
    return render_template('front/profile.html')

@app.route('/event_dashboard')
def event_dashboard():
    events = app_service.get_all_events()
    return render_template('event_dashboard.html', events=events)



if __name__ == "__main__":
    app.run()
