"""
Script to test JWT authentication for user endpoints.
"""

import requests
import json
import uuid

# Base URL for the API
base_url = "http://127.0.0.1:5000/api/v1"

def print_separator(title):
    """Print a separator with a title."""
    print("\n" + "=" * 80)
    print(f" {title} ".center(80, "="))
    print("=" * 80 + "\n")

def create_user():
    """Create a test user."""
    print_separator("CREATING TEST USER")
    
    # Generate a unique email to avoid conflicts
    unique_id = str(uuid.uuid4())[:8]
    email = f"test.user.{unique_id}@example.com"
    
    url = f"{base_url}/users/"
    data = {
        "first_name": "Test",
        "last_name": "User",
        "email": email,
        "password": "password123"
    }
    
    print(f"POST {url}")
    print(f"Request: {json.dumps(data, indent=2)}")
    
    response = requests.post(url, json=data)
    print(f"Response ({response.status_code}): {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 201:
        print("✅ User created successfully")
        return data
    else:
        print("❌ Failed to create user")
        return None

def login(email, password):
    """Login and get JWT token."""
    print_separator("LOGGING IN")
    
    url = f"{base_url}/auth/login"
    data = {
        "email": email,
        "password": password
    }
    
    print(f"POST {url}")
    print(f"Request: {json.dumps(data, indent=2)}")
    
    response = requests.post(url, json=data)
    
    if response.status_code == 200:
        token = response.json().get("access_token")
        print(f"Response ({response.status_code}): {{\"access_token\": \"...token truncated...\"}}") 
        print("✅ Login successful")
        return token
    else:
        print(f"Response ({response.status_code}): {json.dumps(response.json(), indent=2)}")
        print("❌ Login failed")
        return None

def test_update_user(token, user_id):
    """Test updating a user (authenticated endpoint)."""
    print_separator("TESTING USER UPDATE (AUTHENTICATED, SELF)")
    
    url = f"{base_url}/users/{user_id}"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    data = {
        "first_name": "Updated",
        "last_name": "Name"
    }
    
    print(f"PUT {url}")
    print(f"Headers: {{'Authorization': 'Bearer ...token truncated...', 'Content-Type': 'application/json'}}")
    print(f"Request: {json.dumps(data, indent=2)}")
    
    response = requests.put(url, json=data, headers=headers)
    print(f"Response ({response.status_code}): {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200:
        print("✅ User updated successfully")
        return response.json()
    else:
        print("❌ Failed to update user")
        return None

def test_update_user_unauthorized(token, user_id):
    """Test updating a user that is not the authenticated user (should fail)."""
    print_separator("TESTING USER UPDATE (AUTHENTICATED, NOT SELF)")
    
    # This test assumes that user_id belongs to a different user
    url = f"{base_url}/users/{user_id}"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    data = {
        "first_name": "Unauthorized",
        "last_name": "Update"
    }
    
    print(f"PUT {url}")
    print(f"Headers: {{'Authorization': 'Bearer ...token truncated...', 'Content-Type': 'application/json'}}")
    print(f"Request: {json.dumps(data, indent=2)}")
    
    response = requests.put(url, json=data, headers=headers)
    print(f"Response ({response.status_code}): {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 403 and "Unauthorized action" in str(response.json()):
        print("✅ Unauthorized action (expected)")
    else:
        print("❌ Unexpected response")

def test_update_user_email(token, user_id):
    """Test updating a user's email (should fail)."""
    print_separator("TESTING USER EMAIL UPDATE (SHOULD FAIL)")
    
    url = f"{base_url}/users/{user_id}"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    data = {
        "email": "new.email@example.com"
    }
    
    print(f"PUT {url}")
    print(f"Headers: {{'Authorization': 'Bearer ...token truncated...', 'Content-Type': 'application/json'}}")
    print(f"Request: {json.dumps(data, indent=2)}")
    
    response = requests.put(url, json=data, headers=headers)
    print(f"Response ({response.status_code}): {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 400 and "You cannot modify email or password" in str(response.json()):
        print("✅ Cannot modify email (expected)")
    else:
        print("❌ Unexpected response")

def test_update_user_password(token, user_id):
    """Test updating a user's password (should fail)."""
    print_separator("TESTING USER PASSWORD UPDATE (SHOULD FAIL)")
    
    url = f"{base_url}/users/{user_id}"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    data = {
        "password": "newpassword123"
    }
    
    print(f"PUT {url}")
    print(f"Headers: {{'Authorization': 'Bearer ...token truncated...', 'Content-Type': 'application/json'}}")
    print(f"Request: {json.dumps(data, indent=2)}")
    
    response = requests.put(url, json=data, headers=headers)
    print(f"Response ({response.status_code}): {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 400 and "You cannot modify email or password" in str(response.json()):
        print("✅ Cannot modify password (expected)")
    else:
        print("❌ Unexpected response")

def test_get_users():
    """Test getting all users (public endpoint)."""
    print_separator("TESTING GET ALL USERS (PUBLIC)")
    
    url = f"{base_url}/users/"
    
    print(f"GET {url}")
    
    response = requests.get(url)
    print(f"Response ({response.status_code}): {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200:
        print("✅ Users retrieved successfully")
        return response.json()
    else:
        print("❌ Failed to retrieve users")
        return None

def test_get_user(user_id):
    """Test getting a specific user (public endpoint)."""
    print_separator("TESTING GET SPECIFIC USER (PUBLIC)")
    
    url = f"{base_url}/users/{user_id}"
    
    print(f"GET {url}")
    
    response = requests.get(url)
    print(f"Response ({response.status_code}): {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200:
        print("✅ User retrieved successfully")
        return response.json()
    else:
        print("❌ Failed to retrieve user")
        return None

if __name__ == "__main__":
    # Create two users
    user1_data = create_user()
    user2_data = create_user()
    
    if user1_data and user2_data:
        # Login as user1
        token1 = login(user1_data["email"], user1_data["password"])
        
        if token1:
            # Get user1's ID
            users = test_get_users()
            user1_id = next((user["id"] for user in users if user["email"] == user1_data["email"]), None)
            user2_id = next((user["id"] for user in users if user["email"] == user2_data["email"]), None)
            
            if user1_id and user2_id:
                # Update user1's profile (self)
                test_update_user(token1, user1_id)
                
                # Try to update user2's profile (not self, should fail)
                test_update_user_unauthorized(token1, user2_id)
                
                # Try to update user1's email (should fail)
                test_update_user_email(token1, user1_id)
                
                # Try to update user1's password (should fail)
                test_update_user_password(token1, user1_id)
                
                # Get user1's profile (public)
                test_get_user(user1_id)
