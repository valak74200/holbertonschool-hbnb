"""
This file contains decorators for the API endpoints.
"""

from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt, verify_jwt_in_request
from app.models.user import UserRole

def admin_required():
    """
    A decorator to check if the user is an admin.
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            # Verify that the JWT is present and valid
            verify_jwt_in_request()
            
            # Get the JWT claims, which include the is_admin flag
            claims = get_jwt()
            
            # Check if the user is an admin
            if not claims.get('is_admin', False):
                return {'message': 'Admin privileges required'}, 403
            
            # If the user is an admin, call the original function
            return fn(*args, **kwargs)
        return decorator
    return wrapper

def role_required(allowed_roles):
    """
    A decorator to check if the user has one of the allowed roles.
    
    :param allowed_roles: A list of roles that are allowed to access the endpoint
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            # Verify that the JWT is present and valid
            verify_jwt_in_request()
            
            # Get the JWT claims, which include the role
            claims = get_jwt()
            
            # Get the user's role from the claims
            user_role = claims.get('role', UserRole.USER)
            
            # Check if the user's role is in the allowed roles
            if user_role not in allowed_roles:
                return {'message': f'Role {user_role} not authorized. Required: {", ".join(allowed_roles)}'}, 403
            
            # If the user has an allowed role, call the original function
            return fn(*args, **kwargs)
        return decorator
    return wrapper
