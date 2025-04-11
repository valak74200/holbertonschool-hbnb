"""
Script to test the admin endpoints.
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

def create_admin_user():
    """Create an admin user."""
    print_separator("CREATING ADMIN USER")
    
    # Generate a unique email to avoid conflicts
    unique_id = str(uuid.uuid4())[:8]
    email = f"admin.user.{unique_id}@example.com"
    
    # Create a user with is_admin=True directly in the database
    # This would typically be done through a special admin interface or database operation
    # For testing purposes, we'll create a regular user first and then update it to be an admin
    
    url = f"{base_url}/users/"
    data = {
        "first_name": "Admin",
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
        
        # In a real application, you would update the user to be an admin through a database operation
        # For this test, we'll assume the user has been made an admin in the database
        print("⚠️ In a real application, you would need to update the user to be an admin in the database")
        print("⚠️ For this test, we'll assume the user has been made an admin")
        
        return {"email": email, "password": "password123"}
    else:
        print("❌ Failed to create admin user")
        return None

def create_regular_user():
    """Create a regular user."""
    print_separator("CREATING REGULAR USER")
    
    # Generate a unique email to avoid conflicts
    unique_id = str(uuid.uuid4())[:8]
    email = f"regular.user.{unique_id}@example.com"
    
    url = f"{base_url}/users/"
    data = {
        "first_name": "Regular",
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
        return {"email": email, "password": "password123"}
    else:
        print("❌ Failed to create regular user")
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

def test_admin_create_user(token):
    """Test creating a user through the admin endpoint."""
    print_separator("TESTING ADMIN USER CREATION")
    
    url = f"{base_url}/admin/users"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    data = {
        "first_name": "Test",
        "last_name": "User",
        "email": f"test.user.{uuid.uuid4()}@example.com",
        "password": "password123",
        "is_admin": True
    }
    
    print(f"POST {url}")
    print(f"Headers: {{'Authorization': 'Bearer ...token truncated...', 'Content-Type': 'application/json'}}")
    print(f"Request: {json.dumps(data, indent=2)}")
    
    response = requests.post(url, json=data, headers=headers)
    print(f"Response ({response.status_code}): {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 201:
        print("✅ User created successfully through admin endpoint")
        return response.json()
    else:
        print("❌ Failed to create user through admin endpoint")
        return None

def test_admin_update_user(token, user_id):
    """Test updating a user through the admin endpoint."""
    print_separator("TESTING ADMIN USER UPDATE")
    
    url = f"{base_url}/admin/users/{user_id}"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    data = {
        "first_name": "Updated",
        "last_name": "Name",
        "email": f"updated.email.{uuid.uuid4()}@example.com",
        "password": "newpassword123",
        "is_admin": True
    }
    
    print(f"PUT {url}")
    print(f"Headers: {{'Authorization': 'Bearer ...token truncated...', 'Content-Type': 'application/json'}}")
    print(f"Request: {json.dumps(data, indent=2)}")
    
    response = requests.put(url, json=data, headers=headers)
    print(f"Response ({response.status_code}): {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200:
        print("✅ User updated successfully through admin endpoint")
        return response.json()
    else:
        print("❌ Failed to update user through admin endpoint")
        return None

def test_admin_create_amenity(token):
    """Test creating an amenity through the admin endpoint."""
    print_separator("TESTING ADMIN AMENITY CREATION")
    
    url = f"{base_url}/admin/amenities"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    data = {
        "name": f"Test Amenity {uuid.uuid4()}"
    }
    
    print(f"POST {url}")
    print(f"Headers: {{'Authorization': 'Bearer ...token truncated...', 'Content-Type': 'application/json'}}")
    print(f"Request: {json.dumps(data, indent=2)}")
    
    response = requests.post(url, json=data, headers=headers)
    print(f"Response ({response.status_code}): {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 201:
        print("✅ Amenity created successfully through admin endpoint")
        return response.json()
    else:
        print("❌ Failed to create amenity through admin endpoint")
        return None

def test_admin_update_amenity(token, amenity_id):
    """Test updating an amenity through the admin endpoint."""
    print_separator("TESTING ADMIN AMENITY UPDATE")
    
    url = f"{base_url}/admin/amenities/{amenity_id}"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    data = {
        "name": f"Updated Amenity {uuid.uuid4()}"
    }
    
    print(f"PUT {url}")
    print(f"Headers: {{'Authorization': 'Bearer ...token truncated...', 'Content-Type': 'application/json'}}")
    print(f"Request: {json.dumps(data, indent=2)}")
    
    response = requests.put(url, json=data, headers=headers)
    print(f"Response ({response.status_code}): {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200:
        print("✅ Amenity updated successfully through admin endpoint")
        return response.json()
    else:
        print("❌ Failed to update amenity through admin endpoint")
        return None

def test_regular_user_admin_endpoints(token):
    """Test accessing admin endpoints as a regular user (should fail)."""
    print_separator("TESTING ADMIN ENDPOINTS AS REGULAR USER (SHOULD FAIL)")
    
    # Test creating a user
    url = f"{base_url}/admin/users"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    data = {
        "first_name": "Test",
        "last_name": "User",
        "email": f"test.user.{uuid.uuid4()}@example.com",
        "password": "password123"
    }
    
    print(f"POST {url}")
    print(f"Headers: {{'Authorization': 'Bearer ...token truncated...', 'Content-Type': 'application/json'}}")
    print(f"Request: {json.dumps(data, indent=2)}")
    
    response = requests.post(url, json=data, headers=headers)
    print(f"Response ({response.status_code}): {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 403 and "Admin privileges required" in str(response.json()):
        print("✅ Admin privileges required (expected)")
    else:
        print("❌ Unexpected response")
    
    # Test creating an amenity
    url = f"{base_url}/admin/amenities"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    data = {
        "name": f"Test Amenity {uuid.uuid4()}"
    }
    
    print(f"POST {url}")
    print(f"Headers: {{'Authorization': 'Bearer ...token truncated...', 'Content-Type': 'application/json'}}")
    print(f"Request: {json.dumps(data, indent=2)}")
    
    response = requests.post(url, json=data, headers=headers)
    print(f"Response ({response.status_code}): {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 403 and "Admin privileges required" in str(response.json()):
        print("✅ Admin privileges required (expected)")
    else:
        print("❌ Unexpected response")

if __name__ == "__main__":
    # Create an admin user
    admin_data = create_admin_user()
    
    # Create a regular user
    regular_data = create_regular_user()
    
    if admin_data and regular_data:
        # Login as admin
        admin_token = login(admin_data["email"], admin_data["password"])
        
        # Login as regular user
        regular_token = login(regular_data["email"], regular_data["password"])
        
        if admin_token and regular_token:
            # Test admin endpoints as admin
            user_data = test_admin_create_user(admin_token)
            
            if user_data:
                user_id = user_data["id"]
                test_admin_update_user(admin_token, user_id)
            
            amenity_data = test_admin_create_amenity(admin_token)
            
            if amenity_data:
                amenity_id = amenity_data["id"]
                test_admin_update_amenity(admin_token, amenity_id)
            
            # Test admin endpoints as regular user
            test_regular_user_admin_endpoints(regular_token)
            
            print_separator("ALL TESTS COMPLETED")
