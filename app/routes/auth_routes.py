from flask import Blueprint, request, jsonify
from functools import wraps
from services.auth_service import AuthService
from app import db

auth_bp = Blueprint('auth', __name__)
auth_service = AuthService()

def token_required(f):
    """Decorator to require authentication token"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Get token from header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]  # Bearer <token>
            except IndexError:
                return jsonify({'message': 'Invalid token format'}), 401
        
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        
        try:
            current_user = auth_service.verify_token(token)
            if not current_user:
                return jsonify({'message': 'Invalid token'}), 401
        except ValueError as e:
            return jsonify({'message': str(e)}), 401
        
        return f(*args, current_user=current_user, **kwargs)
    
    return decorated

@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user and return JWT token"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'message': 'No data provided'}), 400
        
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'message': 'Username and password are required'}), 400
        
        # Authenticate user
        user = auth_service.authenticate_user(username, password)
        
        if not user:
            return jsonify({'message': 'Invalid username or password'}), 401
        
        # Generate token
        token = auth_service.generate_token(user)
        
        return jsonify({
            'message': 'Login successful',
            'token': token,
            'user': user.to_dict()
        }), 200
        
    except ValueError as e:
        return jsonify({'message': str(e)}), 400
    except Exception as e:
        return jsonify({'message': 'Internal server error'}), 500

@auth_bp.route('/profile', methods=['GET'])
@token_required
def get_profile(current_user=None):
    """Get current user profile"""
    return jsonify({
        'user': current_user.to_dict()
    }), 200

@auth_bp.route('/change-password', methods=['POST'])
@token_required
def change_password(current_user=None):
    """Change user password"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'message': 'No data provided'}), 400
        
        current_password = data.get('current_password')
        new_password = data.get('new_password')
        
        if not current_password or not new_password:
            return jsonify({'message': 'Current password and new password are required'}), 400
        
        # Change password
        user = auth_service.change_password(current_user.id, current_password, new_password)
        
        return jsonify({
            'message': 'Password changed successfully',
            'user': user.to_dict()
        }), 200
        
    except ValueError as e:
        return jsonify({'message': str(e)}), 400
    except Exception as e:
        return jsonify({'message': 'Internal server error'}), 500

@auth_bp.route('/verify-token', methods=['POST'])
def verify_token():
    """Verify JWT token"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'message': 'No data provided'}), 400
        
        token = data.get('token')
        
        if not token:
            return jsonify({'message': 'Token is required'}), 400
        
        # Verify token
        user = auth_service.verify_token(token)
        
        if not user:
            return jsonify({'message': 'Invalid token'}), 401
        
        return jsonify({
            'message': 'Token is valid',
            'user': user.to_dict()
        }), 200
        
    except ValueError as e:
        return jsonify({'message': str(e)}), 401
    except Exception as e:
        return jsonify({'message': 'Internal server error'}), 500 