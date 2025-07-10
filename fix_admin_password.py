#!/usr/bin/env python3
"""
Script para corrigir a senha do usuário admin
"""

import sys
import os
from werkzeug.security import generate_password_hash

# Add the app directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from app import create_app, db
from models import User

def fix_admin_password():
    """Fix the admin user password"""
    app = create_app()
    
    with app.app_context():
        # Find the admin user
        admin_user = User.query.filter_by(username='admin').first()
        
        if admin_user:
            print(f"Found admin user: {admin_user.username}")
            print(f"Current password hash: {admin_user.password_hash}")
            
            # Update the password
            admin_user.set_password('admin123')
            db.session.commit()
            
            print("Admin password updated successfully!")
            print("Username: admin")
            print("Password: admin123")
        else:
            print("Admin user not found!")

if __name__ == '__main__':
    fix_admin_password() 