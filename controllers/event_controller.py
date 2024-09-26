from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_required, current_user
from services import event_service 
from models.event_model import Event  
from app import db
from config import setting
from models.event_registration_model import EventRegistration

event_bp = Blueprint('event', __name__)





@event_bp.route('/event_management', methods=['GET'])
@login_required
def event_management():
    page = request.args.get('page', 1, type=int)
    category = request.args.get('category', '')
    search = request.args.get('search', '')
    filter_type = request.args.get('filter', '')
    user_id = current_user.id

    # 构建基础查询语句
    base_query = f"""
    SELECT 
    e.*,
    CASE 
        WHEN e.author_id = {user_id} THEN 1
        WHEN er.user_id = {user_id} THEN 2
        ELSE 0
    END AS if_my,
    CASE 
        WHEN f.event_id IS NOT NULL THEN 1
        ELSE 0
    END AS if_f
FROM 
    events e
LEFT JOIN 
    event_registrations er ON e.id = er.event_id AND er.user_id = {user_id}
LEFT JOIN 
    favorites f ON e.id = f.event_id AND f.user_id = {user_id}  -- 加入判断是否在favorite表中
WHERE 
    1=1 and e.status = 0
    """
    total_sql = f"SELECT COUNT(*) AS total_count FROM ({base_query}) AS total"

    # 添加搜索和过滤条件
    if search:
        if filter_type == 'location':
            base_query += " AND e.location LIKE '%{}%'".format(search)
        elif filter_type == 'date':
            base_query += " AND e.date LIKE '%{}%'".format(search)

    if category:
        base_query += " AND e.category_id = {}".format(category)

    # 添加排序条件
    base_query += " ORDER BY e.id DESC"

    # 使用分页方法
    items, pagination = event_service.paginate_results(total_sql, base_query, page, 20)

    return render_template('front/event/event_list.html', events=items, categories=event_service.get_categories(), pagination=pagination)




@event_bp.route('/event_detail/<int:id>', methods=['GET'])
def event_detail(id):
    event = event_service.get_event_by_id(id)
    return render_template("front/event/event_detail.html",event = event)


@event_bp.route('/create_event', methods=['GET','POST'])
@login_required
def create_event():
    categories = event_service.get_categories()
    if request.method == 'POST':
        name = request.form['name']
        description=request.form['description']
        location=request.form['location']
        date=request.form['date']
        end_date=request.form['end_date']
        intro = request.form['intro']
        category_id=request.form['category_id']
        image = request.files['image']
       
        if image:
            image.save('static/images/event/' + image.filename)
            image_name= '/static/images/event/'+ image.filename
        else:
            image_name = setting.default_image
        event_service.create_event(name, description, location, date,end_date,category_id,intro,image_name,current_user.id)
        flash("Created event successful")
        return redirect(url_for('event.event_management'))
    return render_template("front/event/create_event.html",categories=categories)



@event_bp.route('/edit_event/<int:id>', methods=['GET','POST'])
@login_required
def edit_event(id):
    categories = event_service.get_categories()
    event = event_service.get_event_by_id(id)
    if request.method == 'POST':
        name = request.form['name']
        description=request.form['description']
        location=request.form['location']
        date=request.form['date']
        end_date=request.form['end_date']
        intro = request.form['intro']
        category_id=request.form['category_id']
        
        image = request.files['image']
        if image:
            image.save('static/images/event/' + image.filename)
            image_name= '/static/images/event/'+ image.filename
        else:
            image_name = setting.default_image
        event_service.update_event(name, description, location, date,end_date,category_id,intro,image_name,id)
        return redirect(url_for('event.event_management'))
    return render_template("front/event/edit_event.html",event = event,categories=categories)

@event_bp.route('/event/<int:event_id>', methods=['PUT'])
def update_event_info(event_id):
    data = request.json
    updated_event = event_service.update_event(
        event_id,
        name=data.get('name'),
        description=data.get('description'),
        location=data.get('location'),
        date=data.get('date'),
        category_id=data.get('category_id')
    )
    if updated_event:
        return jsonify(updated_event.serialize()), 200
    return jsonify({"error": "Event not found"}), 404

@event_bp.route('/event/<int:event_id>', methods=['DELETE'])
def delete_event_info(event_id):
    deleted_event = event_service.delete_event(event_id)
    if deleted_event:
        return jsonify({"message": "Event deleted successfully"}), 200
    return jsonify({"error": "Event not found"}), 404



@event_bp.route('/favorite_event', methods=['GET'])
@login_required
def favorite_event():
    categories = event_service.get_categories()
    page = request.args.get('page', 1, type=int)
    category = request.args.get('category', '')
    search = request.args.get('search', '')
    filter_type = request.args.get('filter', '')
    user_id = current_user.id

    # 构建基础查询语句
    base_query = f"""
    SELECT 
        e.*
    FROM 
        events e
    JOIN 
        favorites f ON e.id = f.event_id AND f.user_id = {user_id}
    WHERE 
        e.author_id != {user_id} and e.status = 0
    """

    # 构建计算总记录数的查询
    total_sql = f"SELECT COUNT(*) AS total_count FROM ({base_query}) AS total"

    # 添加搜索和过滤条件
    if search:
        if filter_type == 'location':
            base_query += f" AND e.location LIKE '%{search}%'"
        elif filter_type == 'date':
            base_query += f" AND e.date LIKE '%{search}%'"

    if category:
        base_query += f" AND e.category_id = {category}"

    # 添加排序条件
    base_query += " ORDER BY e.id DESC"

    # 使用分页方法
    items, pagination = event_service.paginate_results(total_sql, base_query, page, 12)

    return render_template('front/event/favorite_event.html', events=items, categories=categories, pagination=pagination)


@event_bp.route('/event_register/<int:id>', methods=['POST'])
@login_required 
def event_register(id):
    event = Event.query.get_or_404(id) 
    if event:
        registration = EventRegistration(user_id=current_user.id, event_id=event.id)
        db.session.add(registration)
        db.session.commit()
        flash('Successfully registered for the event!')
        return redirect(url_for('event_bp.event_detail', event_id=event.id))
    flash('Event not found!')
    return redirect(url_for('home'))



@event_bp.route('/quit_event', methods=['POST'])
@login_required
def quit_event():
    data = request.json
    event_id = data.get('event_id')
    event_service.delete_register(event_id, current_user.id)
    return jsonify({'success': True}), 200

@event_bp.route('/add_favorite/<int:id>', methods=['POST'])
@login_required
def add_favorite(id):
   
    event_service.add_favorite(id, current_user.id)
    return jsonify({'success': True}), 200

@event_bp.route('/delete_favorite/<int:id>', methods=['POST'])
@login_required
def delete_favorite(id):
   
    event_service.delete_favorite(id, current_user.id)
    return jsonify({'success': True}), 200

@event_bp.route('/join_event', methods=['POST'])
@login_required
def join_event():
    data = request.json
    event_id = data.get('event_id')
    event_service.add_register(event_id, current_user.id)
    return jsonify({'success': True}), 200



@event_bp.route('/offline/<int:id>', methods=['POST'])
@login_required
def offline(id):
   
    event_service.update_event_status(id,1)
    return jsonify({'success': True}), 200

@event_bp.route('/online/<int:id>', methods=['POST'])
@login_required
def online(id):
    event_service.update_event_status(id,0)
    return jsonify({'success': True}), 200


@event_bp.route('/my_event', methods=['GET'])
@login_required
def my_event():
    categories = event_service.get_categories()
    page = request.args.get('page', 1, type=int)
    category = request.args.get('category', '')
    search = request.args.get('search', '')
    filter_type = request.args.get('filter', '')
    user_id = current_user.id  # 使用 Flask-Login 获取当前用户ID

    # 构建基础查询语句
    base_query = f"""
    SELECT 
        e.*
    FROM 
        events e
    WHERE 
        e.author_id = {user_id} and e.status = 0
    """

    # 构建计算总记录数的查询
    total_sql = f"SELECT COUNT(*) AS total_count FROM ({base_query}) AS total"

    # 添加搜索和过滤条件
    if search:
        if filter_type == 'location':
            base_query += f" AND e.location LIKE '%{search}%'"
        elif filter_type == 'date':
            base_query += f" AND e.date LIKE '%{search}%'"

    if category:
        base_query += f" AND e.category_id = {category}"

    # 添加排序条件
    base_query += " ORDER BY e.id DESC"

    # 使用分页方法
    items, pagination = event_service.paginate_results(total_sql, base_query, page, 12)

    return render_template('front/event/my_event.html', events=items, categories=categories, pagination=pagination)



@event_bp.route('/event_schedule')
@login_required
def event_schedule():
    return render_template('front/event/event_dashboard.html')



@event_bp.route('/calendar_events')
def calendar_events():
    rows = event_service.query_workshop_cal()
   
    resp = jsonify({'success' : 1, 'result' : rows })	# 转化为，，，便于数据展示
    resp.status_code = 200
    return resp