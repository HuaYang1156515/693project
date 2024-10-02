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
    
    return redirect(url_for('event_management'))

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
   

@admin_bp.route('/event_management', methods=['GET'])
def event_management():
    # 获取当前页码
    page = request.args.get('page', 1, type=int)
    per_page = 10  # 每页显示10条记录

    # 构建查询语句
    event_sql = "SELECT * FROM events where status = 0"
    total_sql = "SELECT COUNT(*) AS total_count FROM events where status = 0"

    # 使用分页函数获取数据和分页信息
    events, pagination = admin_service.paginate_results(total_sql, event_sql, page, per_page)

    # 获取所有分类
    categories = admin_service.get_all_categories()

    # 渲染模板，并将分页数据传递给模板
    return render_template("admin/event/event_list.html", events=events, categories=categories, pagination=pagination)


@admin_bp.route('/cancel_event', methods=['POST'])
def cancel_event():
    data = request.json
    event_id = data.get('event_id')
    status = data.get('status')
    admin_service.cancel_event(event_id,status)
   
    return jsonify({"message": "Event status updated successfully"}), 200


@admin_bp.route('/filter_events', methods=['GET', 'POST'])
def filter_events():
    page = request.args.get('page', 1, type=int)  # 获取当前页码
    per_page = 10  # 每页显示的记录数
    
    search = request.form.get('search')
    filter_type = request.form.get('filter')
    category = request.form.get('category')

    # 构建查询语句
    query = "SELECT * FROM events WHERE 1=1 and status = 0 "
    
    if search:
        if filter_type == 'location':
            query += f" AND location LIKE '%{search}%'"
        elif filter_type == 'date':
            query += f" AND date LIKE '%{search}%'"
    
    if category:
        query += f" AND category_id = '{category}'"

    # 获取总记录数的SQL
    total_sql = "SELECT COUNT(*) AS total_count FROM events WHERE 1=1 and status = 0 "
    if search:
        if filter_type == 'location':
            total_sql += f" AND location LIKE '%{search}%'"
        elif filter_type == 'date':
            total_sql += f" AND date LIKE '%{search}%'"
    
    if category:
        total_sql += f" AND category_id = '{category}'"
    
    # 调用分页函数
    events, pagination = admin_service.paginate_results(total_sql, query, page, per_page)
    
    categories = admin_service.get_all_categories()
    
    return render_template('admin/event/event_list.html', 
                           events=events, 
                           categories=categories, 
                           pagination=pagination)


@admin_bp.route('/event_detail/<int:id>', methods=(['GET','POST']))
def event_detail(id):
    event_detail = admin_service.get_event(id)
    return render_template('admin/event/event_detail.html', event=event_detail)


@admin_bp.route('/edit_event/<int:id>', methods=['GET','POST'])
def edit_event(id):
    categories = admin_service.get_all_categories()
    event = admin_service.get_event(id)
    if request.method == 'POST':
        name = request.form['name']
        description=request.form['description']
        location=request.form['location']
        date=request.form['date']
        end_date=request.form['end_date']
        intro = request.form['intro']
        category_id=request.form['category_id']
        image = request.files['images']
        img = request.form['image']
        if image:
            image.save('static/images/event/' + image.filename)
            image_name= '/static/images/event/'+ image.filename
        else:
            image_name = img
        admin_service.edit_event(id,name, description, location, date,end_date,category_id,intro,image_name)
        flash("Created event successful")
        return redirect(url_for('admin.event_management'))
    return render_template("admin/event/edit_event.html",categories=categories,event=event)