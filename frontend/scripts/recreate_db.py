#!/usr/bin/env python3
"""
Script to recreate the database
"""
import sys
import os

# Add the parent directory to the path so we can import app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.extensions import db

def main():
    """
    Recreate the database
    """
    app = create_app('config.DevelopmentConfig')
    with app.app_context():
        db.drop_all()
        db.create_all()
        print("Database recreated successfully!")

if __name__ == "__main__":
    main()
