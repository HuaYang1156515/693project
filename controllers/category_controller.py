from flask import Blueprint, request, jsonify,render_template,flash,redirect,url_for
from services import category_service

category_bp = Blueprint('category', __name__)

@category_bp.route('/category_management', methods=['GET'])
def category_management():
    categories = category_service.get_all_categories()
    return render_template("admin/category/category_list.html",categories=categories) 

@category_bp.route('/create_category', methods=['GET','POST'])
def create_category():
    if request.method == 'POST':
        name = request.form['name']
        category_service.create_category(name)
        flash("create category successful")
        return redirect(url_for('category.category_management'))
    return render_template("admin/category/create_category.html")

@category_bp.route('/edit_category/<int:id>', methods=['GET','POST'])
def edit_category(id):
    id = id
   
    return 

@category_bp.route('/delete_category', methods=['GET','PUT'])
def delete_category():
    data = request.json  # 获取从前端传递的数据
    category_id = data.get('id')  # 提取类别ID
    category_service.delete_category(id)
    return

