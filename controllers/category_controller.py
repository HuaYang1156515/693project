from flask import Blueprint, request, jsonify,render_template,flash,redirect,url_for
from services import category_service
from flask_login import current_user
category_bp = Blueprint('category', __name__)

@category_bp.route('/category_management', methods=['GET'])
def category_management():
    categories = category_service.get_all_categories()
    if current_user.role != 'admin':
        return render_template("front/category/category_list.html",categories=categories) 
    else:
        return render_template("admin/category/category_list.html",categories=categories) 

@category_bp.route('/create_category', methods=['GET','POST'])
def create_category():
    if request.method == 'POST':
        name = request.form['name']
        category_service.create_category(name)
        flash("create category successful")
        return redirect(url_for('category.category_management'))
    if current_user.role != 'admin':
        return render_template("front/category/create_category.html")
    else:
        return render_template("admin/category/create_category.html")

@category_bp.route('/edit_category/<int:id>', methods=['GET','POST'])
def edit_category(id):
    id = id
    category = category_service.get_category_by_id(id)
    if request.method == 'POST':
        name = request.form['name']
       
        category_service.update_category(id,name)
        flash("edit category successful")
        return redirect(url_for('category.category_management'))
    if current_user.role != 'admin':
        return render_template("front/category/edit_category.html",category=category)
    else:
        return render_template("admin/category/edit_category.html",category=category)

@category_bp.route('/delete_category', methods=['POST'])  
def delete_category():
    data = request.json  # 获取从前端传递的数据
    category_id = data.get('id')  # 提取类别ID
    category_service.delete_category(category_id)
    return jsonify({'success': True}), 200

