#!/usr/bin/env python3
"""
SEDUC API - Alternative Entry Point (for running from api directory)
"""
import sys
import os

# Add the parent directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import create_app
flask_app = create_app()

if __name__ == '__main__':
    flask_app.run(debug=True, host='0.0.0.0', port=5000) 