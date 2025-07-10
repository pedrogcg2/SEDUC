from repositories.user_repository import UserRepository
from werkzeug.security import generate_password_hash

class UserService:
    def __init__(self):
        self.user_repository = UserRepository()
    
    def get_all_users(self):
        """Get all users"""
        users = self.user_repository.get_all()
        return [user.to_dict() for user in users]
    
    def get_user_by_id(self, user_id):
        """Get user by ID"""
        user = self.user_repository.get_by_id(user_id)
        return user.to_dict() if user else None
    
    def create_user(self, user_data):
        """Create a new user"""
        username = user_data.get('username')
        password = user_data.get('password')
        email = user_data.get('email')
        is_admin = user_data.get('is_admin', False)
        is_active = user_data.get('is_active', True)
        
        # Validate required fields
        if not username or not password:
            raise ValueError("Username and password are required")
        
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
        user = self.user_repository.create_user(
            username=username,
            password=password,
            email=email,
            is_admin=is_admin
        )
        
        # Set active status if different from default
        if not is_active:
            user.is_active = False
            from app import db
            db.session.commit()
        
        return user.to_dict()
    
    def update_user(self, user_id, user_data):
        """Update user information"""
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        
        # Check if username is being changed and if it already exists
        new_username = user_data.get('username')
        if new_username and new_username != user.username:
            if self.user_repository.find_by_username(new_username):
                raise ValueError("Username already exists")
        
        # Check if email is being changed and if it already exists
        new_email = user_data.get('email')
        if new_email and new_email != user.email:
            if self.user_repository.find_by_email(new_email):
                raise ValueError("Email already exists")
        
        # Update fields
        update_data = {}
        
        if 'username' in user_data:
            update_data['username'] = user_data['username']
        
        if 'email' in user_data:
            update_data['email'] = user_data['email']
        
        if 'is_admin' in user_data:
            update_data['is_admin'] = user_data['is_admin']
        
        if 'is_active' in user_data:
            update_data['is_active'] = user_data['is_active']
        
        # Handle password update
        if user_data.get('password'):
            password = user_data['password']
            if len(password) < 6:
                raise ValueError("Password must be at least 6 characters long")
            user.set_password(password)
        
        # Update user
        updated_user = self.user_repository.update_user(user_id, **update_data)
        return updated_user.to_dict() if updated_user else None
    
    def delete_user(self, user_id):
        """Delete a user"""
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        
        # Don't allow admin to delete themselves
        # This check should be done at the route level with current user context
        
        from app import db
        db.session.delete(user)
        db.session.commit()
        
        return True
    
    def get_users_paginated(self, page, per_page, search=''):
        """Get users with pagination and search"""
        users, total, total_pages = self.user_repository.get_paginated(page, per_page, search)
        return [user.to_dict() for user in users], total, total_pages
    
    def get_user_stats(self):
        """Get user statistics"""
        users = self.user_repository.get_all()
        
        total = len(users)
        active = len([u for u in users if u.is_active])
        admins = len([u for u in users if u.is_admin])
        regular = total - admins
        
        return {
            'total': total,
            'active': active,
            'admins': admins,
            'regular': regular
        } 