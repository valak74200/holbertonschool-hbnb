"""
Script to test the authentication flow.
"""

import requests
import json

# Base URL for the API
base_url = "http://127.0.0.1:5000/api/v1"

# Step 1: Create a user
def create_user():
    url = f"{base_url}/users/"
    data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "password": "password123"
    }
    response = requests.post(url, json=data)
    print(f"Create User Response: {response.status_code}")
    if response.status_code == 201:
        print(f"User created: {response.json()}")
    return response.json() if response.status_code == 201 else None

# Step 2: Login and get JWT token
def login():
    url = f"{base_url}/auth/login"
    data = {
        "email": "john.doe@example.com",
        "password": "password123"
    }
    response = requests.post(url, json=data)
    print(f"Login Response: {response.status_code}")
    if response.status_code == 200:
        print(f"Login successful: {response.json()}")
        return response.json().get("access_token")
    else:
        print(f"Login failed: {response.text}")
        return None

# Step 3: Access protected endpoint
def access_protected(token):
    url = f"{base_url}/auth/protected"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    print(f"Protected Endpoint Response: {response.status_code}")
    if response.status_code == 200:
        print(f"Protected endpoint accessed: {response.json()}")
    else:
        print(f"Failed to access protected endpoint: {response.text}")

if __name__ == "__main__":
    # Create a user (this might fail if the user already exists, which is fine)
    create_user()
    
    # Login and get token
    token = login()
    
    if token:
        # Access protected endpoint
        access_protected(token)
