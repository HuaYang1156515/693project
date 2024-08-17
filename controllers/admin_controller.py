from flask import Blueprint, request, jsonify
from services.admin_service import get_admin_by_id, create_admin, update_admin, delete_admin

admin_bp = Blueprint('admin_bp', __name__)

@admin_bp.route('/admin/<int:admin_id>', methods=['GET'])
def get_admin(admin_id):
    admin = get_admin_by_id(admin_id)
    if admin:
        return jsonify(admin), 200
    return jsonify({"error": "Admin not found"}), 404

@admin_bp.route('/admin', methods=['POST'])
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
