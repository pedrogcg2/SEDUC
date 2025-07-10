#!/usr/bin/env python3
"""
SEDUC API - Alternative Entry Point (for running from api directory)
"""
import sys
import os
from sqlalchemy import create_engine, text

# Add the parent directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import create_app
flask_app = create_app()

if __name__ == '__main__':
    # Use DATABASE_URL environment variable or fallback to localhost for local development
    database_url = os.getenv('DATABASE_URL', 'postgresql://master:HgAXVS5uWph3@localhost/sqldb-seduc')
    engine = create_engine(database_url)
    with engine.connect() as conn:
        conn.execute(text('SELECT 1'))
    flask_app.run(debug=True, host='0.0.0.0', port=5000) 