#!/usr/bin/env python3
"""
Script to generate a bcrypt hash for a password.
"""

import bcrypt
import sys

def generate_bcrypt_hash(password):
    """
    Generate a bcrypt hash for a password.
    
    Args:
        password (str): The password to hash
        
    Returns:
        str: The bcrypt hash of the password
    """
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    
    # Return the hash as a string
    return hashed_password.decode('utf-8')

def main():
    """
    Main function to run when the script is executed directly.
    """
    # Check if a password was provided
    if len(sys.argv) > 1:
        password = sys.argv[1]
    else:
        # If no password was provided, use the default
        password = 'admin1234'
    
    # Generate the hash
    hashed_password = generate_bcrypt_hash(password)
    
    # Print the hash
    print(f"Password: {password}")
    print(f"Bcrypt Hash: {hashed_password}")

if __name__ == "__main__":
    main()
