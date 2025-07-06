from models.user import User
from repositories.base_repository import BaseRepository

class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__(User)
    
    def find_by_username(self, username):
        """Find user by username"""
        return self.model.query.filter_by(username=username).first()
    
    def find_by_email(self, email):
        """Find user by email"""
        return self.model.query.filter_by(email=email).first()
    
    def create_user(self, username, password, email=None, is_admin=False):
        """Create a new user"""
        user = User(username=username, password=password, email=email, is_admin=is_admin)
        from app import db
        db.session.add(user)
        db.session.commit()
        return user
    
    def update_user(self, user_id, **kwargs):
        """Update user information"""
        user = self.find_by_id(user_id)
        if user:
            for key, value in kwargs.items():
                if hasattr(user, key):
                    setattr(user, key, value)
            from app import db
            db.session.commit()
        return user
    
    def deactivate_user(self, user_id):
        """Deactivate a user"""
        user = self.find_by_id(user_id)
        if user:
            user.is_active = False
            from app import db
            db.session.commit()
        return user
    
    def activate_user(self, user_id):
        """Activate a user"""
        user = self.find_by_id(user_id)
        if user:
            user.is_active = True
            from app import db
            db.session.commit()
        return user
    
    def find_by_id(self, user_id):
        return self.model.query.get(user_id)