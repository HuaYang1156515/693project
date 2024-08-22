from flask import Blueprint, request, jsonify
from services.user_service import get_user_by_id, create_user, update_user, delete_user

user_bp = Blueprint('user', __name__)

@user_bp.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = get_user_by_id(user_id)
    if user:
        return jsonify(user), 200
    return jsonify({"error": "User not found"}), 404

@user_bp.route('/user', methods=['POST'])
def add_user():
    data = request.json
    new_user = create_user(data['name'], data['login'], data['password'], data['role'])
    return jsonify(new_user), 201

@user_bp.route('/user/<int:user_id>', methods=['PUT'])
def edit_user(user_id):
    data = request.json
    updated_user = update_user(user_id, data['name'], data['login'], data['password'], data['role'])
    if updated_user:
        return jsonify(updated_user), 200
    return jsonify({"error": "User not found"}), 404

@user_bp.route('/user/<int:user_id>', methods=['DELETE'])
def remove_user(user_id):
    success = delete_user(user_id)
    if success:
        return jsonify({"message": "User deleted"}), 200
    return jsonify({"error": "User not found"}), 404


@user_bp.route('/users_management', methods=['GET','POST'])
def users_management():
    return