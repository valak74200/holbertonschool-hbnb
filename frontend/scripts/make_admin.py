#!/usr/bin/env python3
"""
Script to make a user an admin.
Usage: python make_admin.py <email>
"""

import sys
import os
import json
from pathlib import Path

# Add the parent directory to the Python path so we can import the app modules
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.services.facade import facade

def make_admin(email):
    """
    Make a user with the given email an admin.
    
    Args:
        email (str): The email of the user to make an admin.
        
    Returns:
        bool: True if the user was successfully made an admin, False otherwise.
    """
    # Get the user by email
    user = facade.get_user_by_email(email)
    
    if not user:
        print(f"Error: User with email '{email}' not found.")
        return False
    
    # Check if the user is already an admin
    if user.is_admin:
        print(f"User '{email}' is already an admin.")
        return True
    
    # Update the user to be an admin
    user.is_admin = True
    
    # Save the user
    try:
        facade.update_user(user.id, {"is_admin": True})
        print(f"User '{email}' is now an admin.")
        return True
    except Exception as e:
        print(f"Error making user '{email}' an admin: {str(e)}")
        return False

def main():
    """
    Main function to parse command line arguments and make a user an admin.
    """
    if len(sys.argv) != 2:
        print("Usage: python make_admin.py <email>")
        sys.exit(1)
    
    email = sys.argv[1]
    success = make_admin(email)
    
    if success:
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
