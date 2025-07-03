import jwt
import datetime
from flask import current_app
from werkzeug.security import check_password_hash
from ..repositories.user_repository import UserRepository

class AuthService:
    def __init__(self):
        self.user_repository = UserRepository()
    
    def register_user(self, username, password, email=None):
        """Register a new user"""
        # Check if username already exists
        if self.user_repository.find_by_username(username):
            raise ValueError("Username already exists")
        
        # Check if email already exists (if provided)
        if email and self.user_repository.find_by_email(email):
            raise ValueError("Email already exists")
        
        # Validate password strength
        if len(password) < 6:
            raise ValueError("Password must be at least 6 characters long")
        
        # Create user
        user = self.user_repository.create_user(username, password, email)
        return user
    
    def authenticate_user(self, username, password):
        """Authenticate user with username and password"""
        user = self.user_repository.find_by_username(username)
        
        if not user:
            return None
        
        if not user.is_active:
            raise ValueError("User account is deactivated")
        
        if not user.check_password(password):
            return None
        
        return user
    
    def generate_token(self, user):
        """Generate JWT token for user"""
        payload = {
            'user_id': user.id,
            'username': user.username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24),
            'iat': datetime.datetime.utcnow()
        }
        
        token = jwt.encode(
            payload, 
            current_app.config['SECRET_KEY'], 
            algorithm='HS256'
        )
        
        return token
    
    def verify_token(self, token):
        """Verify JWT token and return user"""
        try:
            payload = jwt.decode(
                token, 
                current_app.config['SECRET_KEY'], 
                algorithms=['HS256']
            )
            
            user_id = payload.get('user_id')
            if user_id:
                user = self.user_repository.find_by_id(user_id)
                if user and user.is_active:
                    return user
            
            return None
            
        except jwt.ExpiredSignatureError:
            raise ValueError("Token has expired")
        except jwt.InvalidTokenError:
            raise ValueError("Invalid token")
    
    def change_password(self, user_id, current_password, new_password):
        """Change user password"""
        user = self.user_repository.find_by_id(user_id)
        
        if not user:
            raise ValueError("User not found")
        
        if not user.check_password(current_password):
            raise ValueError("Current password is incorrect")
        
        if len(new_password) < 6:
            raise ValueError("New password must be at least 6 characters long")
        
        user.set_password(new_password)
        from ..app import db
        db.session.commit()
        
        return user 