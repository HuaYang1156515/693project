from flask import Blueprint, request, jsonify,render_template,flash,redirect,url_for
from services import category_service

category_bp = Blueprint('category', __name__)

@category_bp.route('/category_management', methods=['GET'])
def category_management():
    categories = category_service.get_all_categories()
    return render_template("admin/category/create_list.html") 

@category_bp.route('/create_category', methods=['GET','POST'])
def create_category():
    if request.method == 'POST':
        name = request.form['name']
        category_service.create_category(name)
        flash("create category successful")
        return redirect(url_for('category.category_management'))
    return render_template("admin/category/create_category.html")

@category_bp.route('/category', methods=['POST'])
def add_category():
    data = request.json
    new_category = create_category(name=data['name'])
    return jsonify(new_category.serialize()), 201

@category_bp.route('/category/<int:category_id>', methods=['PUT'])
def update_category_info(category_id):
    data = request.json
    updated_category = update_category(
        category_id,
        name=data.get('name'),
        status=data.get('status')
    )
    if updated_category:
        return jsonify(updated_category.serialize()), 200
    return jsonify({"error": "Category not found"}), 404

@category_bp.route('/category/<int:category_id>', methods=['DELETE'])
def delete_category_info(category_id):
    deleted_category = delete_category(category_id)
    if deleted_category:
        return jsonify({"message": "Category deleted successfully"}), 200
    return jsonify({"error": "Category not found"}), 404
