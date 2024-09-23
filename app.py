from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from config import setting
from services import app_service
app = Flask(__name__)
app.config.from_object(setting.Config)

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
            if int(user.status) == 1:
                flash('your account does not exist!', 'warning')
                return render_template('front/login.html')
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
        user.pic = setting.default_user_image
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please login.')
        return redirect(url_for('login'))
    return render_template('front/register.html')

@app.route('/')
def home():
    if current_user.is_authenticated:
        events = app_service.get_all_events(current_user.id)  # Fetch all events to display on the homepage
        my_events= app_service.get_my_events(current_user.id)
        my_favorite = app_service.get_my_favorite(current_user.id)
        return render_template('front/home.html', events=events,my_events=my_events,my_favorite=my_favorite)
    else:
        events = app_service.get_all_events_visit()
        return render_template('front/home.html', events=events)

@app.route('/profile/', methods=['GET', 'POST'])
@login_required
def profile():
    user = app_service.get_user(current_user.id)
    if request.method == 'POST':
       
        name= request.form['name']
        password=request.form['password']
        role=request.form['role']
        status=request.form['status']
        pic=request.files['pic']
        description=request.form['description']
        image = request.form['image']

        if pic:
            image_path = 'static/images/user/' + pic.filename
            pic.save(image_path)
            image_name = '/static/images/user/' + pic.filename
        else:
            image_name = image

        app_service.update_user(current_user.id,name,password,role,status,description,image_name)
        flash("update user successfule")
        return redirect(url_for('user.users_management'))
    return render_template("admin/users/edit_user.html",user=user)

@app.route('/event_dashboard')
def event_dashboard():
    events = app_service.get_all_events()
    return render_template('event_dashboard.html', events=events)

@app.route('/contact')
def contact ():
    return render_template('front/help/contact.html')


@app.route('/about')
def about ():
    return render_template('front/help/about.html')


if __name__ == "__main__":
    app.run()
