#!/usr/bin/env python3
"""
Database initialization script for SEDUC API
Creates all tables including the new users table
"""

import os
import sys
from dotenv import load_dotenv

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api.app import create_app, db
from models import Aluno, Escola, Disciplina, Matricula, User
from werkzeug.security import generate_password_hash

def init_database():
    """Initialize the database with all tables"""
    app = create_app()
    
    with app.app_context():
        print("Creating database tables...")
        
        # Create all tables
        db.create_all()
        
        print("Database tables created successfully!")
        
        # Check if admin user exists, if not create one
        admin_user = User.query.filter_by(username='admin').first()
        if not admin_user:
            print("Creating default admin user...")
            admin_user = User(
                username='admin',
                password='admin123',
                email='admin@seduc.com'
            )
            db.session.add(admin_user)
            db.session.commit()
            print("Default admin user created!")
            print("Username: admin")
            print("Password: admin123")
        else:
            print("Admin user already exists")
        
        print("\nDatabase initialization completed!")
        print("You can now start the API server.")

if __name__ == '__main__':
    load_dotenv()
    init_database() 