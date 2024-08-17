from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from config.setting import Config

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
from models.event_model import Event
from models.category_model import Category
from models.event_registration_model import EventRegistration
from models.favorite_model import Favorite  

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
    return render_template('login.html')

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
    return render_template('register.html')

@app.route('/')
def home():
    events = Event.query.all()  # Fetch all events to display on the homepage
    return render_template('home.html', events=events)

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
    return render_template('profile.html')

@app.route('/event_dashboard')
def event_dashboard():
    events = Event.query.all()
    return render_template('event_dashboard.html', events=events)

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        flash('You are not authorized to view this page.')
        return redirect(url_for('home'))
    events = Event.query.all()
    return render_template('admin_dashboard.html', events=events)

# Event detail route
@app.route('/event/<int:event_id>')
def event_detail(event_id):
    event = Event.query.get_or_404(event_id)
    return render_template('event_detail.html', event=event)

# Create event route
@app.route('/event/create', methods=['GET', 'POST'])
@login_required
def create_event():
    if current_user.role != 'admin':
        flash('You are not authorized to create events.')
        return redirect(url_for('home'))
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        location = request.form['location']
        date = request.form['date']
        category_id = request.form['category_id']
        event = Event(name=name, description=description, location=location, date=date, created_by=current_user.id, category_id=category_id)
        db.session.add(event)
        db.session.commit()
        flash('Event created successfully!')
        return redirect(url_for('home'))
    categories = Category.query.all()
    return render_template('create_event.html', categories=categories)

# Edit event route
@app.route('/event/edit/<int:event_id>', methods=['GET', 'POST'])
@login_required
def edit_event(event_id):
    event = Event.query.get_or_404(event_id)
    if current_user.role != 'admin':
        flash('You are not authorized to edit this event.')
        return redirect(url_for('home'))
    if request.method == 'POST':
        event.name = request.form['name']
        event.description = request.form['description']
        event.location = request.form['location']
        event.date = request.form['date']
        event.category_id = request.form['category_id']
        db.session.commit()
        flash('Event updated successfully!')
        return redirect(url_for('admin_dashboard'))
    categories = Category.query.all()
    return render_template('edit_event.html', event=event, categories=categories)

# Delete event route
@app.route('/event/delete/<int:event_id>')
@login_required
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    if current_user.role != 'admin':
        flash('You are not authorized to delete this event.')
        return redirect(url_for('home'))
    db.session.delete(event)
    db.session.commit()
    flash('Event deleted successfully!')
    return redirect(url_for('admin_dashboard'))

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)
