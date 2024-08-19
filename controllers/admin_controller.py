from flask import Blueprint, request, jsonify,render_template,redirect,flash,url_for
from services.admin_service import get_admin_by_id, create_admin, update_admin, delete_admin
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from services import admin_service

admin_bp = Blueprint('admin', __name__)
# Import models
from models.user_model import User
from models.event_model import Event
from models.category_model import Category
from models.event_registration_model import EventRegistration
from models.favorite_model import Favorite  


@admin_bp.route('/')
@login_required
def home():
    if current_user.role != 'admin':
        flash('You are not authorized to view this page.')
        return redirect(url_for('home'))
    events = Event.query.all()
    return render_template('admin/admin_dashboard.html', events=events)

@admin_bp.route('/admin/<int:admin_id>', methods=['GET'])
def get_admin(admin_id):
    admin = get_admin_by_id(admin_id)
    if admin:
        return jsonify(admin), 200
    return jsonify({"error": "Admin not found"}), 404

@admin_bp.route('/admin/add_admin', methods=['POST'])
def add_admin():
    data = request.json
    new_admin = create_admin(data['name'], data['login'], data['password'])
    return jsonify(new_admin), 201

@admin_bp.route('/admin/<int:admin_id>', methods=['PUT'])
def update_admin_info(admin_id):
    data = request.json
    updated_admin = update_admin(
        admin_id,
        name=data.get('name'),
        login=data.get('login'),
        password=data.get('password'),
        status=data.get('status')
    )
    if updated_admin:
        return jsonify(updated_admin), 200
    return jsonify({"error": "Admin not found"}), 404

@admin_bp.route('/admin/<int:admin_id>', methods=['DELETE'])
def delete_admin_info(admin_id):
    deleted_admin = delete_admin(admin_id)
    if deleted_admin:
        return jsonify({"message": "Admin deleted successfully"}), 200
    return jsonify({"error": "Admin not found"}), 404


@admin_bp.route('/calendar_events')
def calendar_events():
    rows = admin_service.query_workshop_cal()
    
    resp = jsonify({'success' : 1, 'result' : rows })	# 转化为，，，便于数据展示
    resp.status_code = 200
    return resp
   