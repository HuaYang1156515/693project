from flask import Blueprint, request, jsonify
from services.category_service import (
    get_category_by_id, create_category, update_category, delete_category, get_all_categories
)

category_bp = Blueprint('category_bp', __name__)

@category_bp.route('/categories', methods=['GET'])
def get_categories():
    categories = get_all_categories()
    return jsonify([category.serialize() for category in categories]), 200

@category_bp.route('/category/<int:category_id>', methods=['GET'])
def get_category(category_id):
    category = get_category_by_id(category_id)
    if category:
        return jsonify(category.serialize()), 200
    return jsonify({"error": "Category not found"}), 404

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
