from flask import Blueprint, request, jsonify,render_template,flash,redirect,url_for
from services import user_service
from config import setting
user_bp = Blueprint('user', __name__)

@user_bp.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = user_service.get_user_by_id(user_id)
    if user:
        return jsonify(user), 200
    return jsonify({"error": "User not found"}), 404

@user_bp.route('/create_user', methods=['GET','POST'])
def create_user():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        role = request.form['role']
        status = request.form['status']
        pic = request.files['pic']
        description = request.form['description']
        if pic and pic.filename:
            image_path = 'static/images/user/' + pic.filename
            pic.save(image_path)
            image_name = '/static/images/user/' + pic.filename
        else:
            image_name = setting.default_user_image
        user_service.create_user(name, name, password, role, status, description, image_name)
        flash("User inserted successfully")
        return redirect(url_for('user.users_management'))  # 重定向到用户管理页面

    return render_template('admin/users/create_user.html')  # 渲染插入用户页面

@user_bp.route('/edit_user/<int:user_id>', methods=['GET','POST'])
def edit_user(user_id):
    user = user_service.get_user_by_id(user_id)
    if request.method == 'POST':
        id = user_id
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

        user_service.update_user(id,name,password,role,status,description,image_name)
        flash("update user successfule")
        return redirect(url_for('user.users_management'))
    return render_template("admin/users/edit_user.html",user=user)

@user_bp.route('/user/<int:user_id>', methods=['DELETE'])
def remove_user(user_id):
    success = user_service.delete_user(user_id)
    if success:
        return jsonify({"message": "User deleted"}), 200
    return jsonify({"error": "User not found"}), 404


@user_bp.route('/users_management', methods=['GET','POST'])
def users_management():
    users = user_service.get_all_users()
    return render_template("admin/users/users_list.html",users=users)

