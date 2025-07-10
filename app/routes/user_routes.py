from flask import Blueprint, request, jsonify
from services.user_service import UserService
from routes.auth_routes import token_required

user_bp = Blueprint('user', __name__)
user_service = UserService()

@user_bp.route('/', methods=['GET'])
@token_required
def get_users(current_user=None):
    """Get all users (admin only)"""
    try:
        # Check if current user is admin
        if not current_user.is_admin:
            return jsonify({'message': 'Access denied. Admin privileges required.'}), 403
        
        # Get pagination parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        search = request.args.get('search', '')
        
        # Ensure reasonable limits
        page = max(1, page)
        per_page = min(max(1, per_page), 100)  # Between 1 and 100
        
        users, total, total_pages = user_service.get_users_paginated(page, per_page, search)
        
        return jsonify({
            'users': users,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total,
                'total_pages': total_pages
            }
        }), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@user_bp.route('/<int:user_id>', methods=['GET'])
@token_required
def get_user(user_id, current_user=None):
    """Get user by ID (admin only)"""
    try:
        # Check if current user is admin
        if not current_user.is_admin:
            return jsonify({'message': 'Access denied. Admin privileges required.'}), 403
        
        user = user_service.get_user_by_id(user_id)
        if user:
            return jsonify(user), 200
        return jsonify({'message': 'User not found'}), 404
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@user_bp.route('/', methods=['POST'])
@token_required
def create_user(current_user=None):
    """Create a new user (admin only)"""
    try:
        # Check if current user is admin
        if not current_user.is_admin:
            return jsonify({'message': 'Access denied. Admin privileges required.'}), 403
        
        data = request.get_json()
        if not data:
            return jsonify({'message': 'No data provided'}), 400
        
        # Convert string values to boolean
        if 'is_admin' in data:
            data['is_admin'] = data['is_admin'] == 'true' if isinstance(data['is_admin'], str) else bool(data['is_admin'])
        
        if 'is_active' in data:
            data['is_active'] = data['is_active'] == 'true' if isinstance(data['is_active'], str) else bool(data['is_active'])
        
        user = user_service.create_user(data)
        return jsonify(user), 201
    except ValueError as e:
        return jsonify({'message': str(e)}), 400
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@user_bp.route('/<int:user_id>', methods=['PUT'])
@token_required
def update_user(user_id, current_user=None):
    """Update user (admin only)"""
    try:
        # Check if current user is admin
        if not current_user.is_admin:
            return jsonify({'message': 'Access denied. Admin privileges required.'}), 403
        
        # Prevent admin from deactivating themselves
        if user_id == current_user.id:
            return jsonify({'message': 'Cannot modify your own account'}), 400
        
        data = request.get_json()
        if not data:
            return jsonify({'message': 'No data provided'}), 400
        
        # Convert string values to boolean
        if 'is_admin' in data:
            data['is_admin'] = data['is_admin'] == 'true' if isinstance(data['is_admin'], str) else bool(data['is_admin'])
        
        if 'is_active' in data:
            data['is_active'] = data['is_active'] == 'true' if isinstance(data['is_active'], str) else bool(data['is_active'])
        
        user = user_service.update_user(user_id, data)
        if user:
            return jsonify(user), 200
        return jsonify({'message': 'User not found'}), 404
    except ValueError as e:
        return jsonify({'message': str(e)}), 400
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@user_bp.route('/<int:user_id>', methods=['DELETE'])
@token_required
def delete_user_route(user_id, current_user=None):
    """Delete user (admin only)"""
    try:
        # Check if current user is admin
        if not current_user.is_admin:
            return jsonify({'message': 'Access denied. Admin privileges required.'}), 403
        
        # Prevent admin from deleting themselves
        if user_id == current_user.id:
            return jsonify({'message': 'Cannot delete your own account'}), 400
        
        user_service.delete_user(user_id)
        return jsonify({'message': 'User deleted successfully'}), 200
    except ValueError as e:
        return jsonify({'message': str(e)}), 400
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@user_bp.route('/stats', methods=['GET'])
@token_required
def get_user_stats(current_user=None):
    """Get user statistics (admin only)"""
    try:
        # Check if current user is admin
        if not current_user.is_admin:
            return jsonify({'message': 'Access denied. Admin privileges required.'}), 403
        
        stats = user_service.get_user_stats()
        return jsonify(stats), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500 