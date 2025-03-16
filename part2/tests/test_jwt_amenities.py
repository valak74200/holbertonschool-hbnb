"""
Script to test JWT authentication for amenity endpoints.
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

def test_create_amenity(token):
    """Test creating an amenity (authenticated endpoint)."""
    print_separator("TESTING AMENITY CREATION (AUTHENTICATED)")
    
    url = f"{base_url}/amenities/"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    data = {
        "name": "Test Amenity"
    }
    
    print(f"POST {url}")
    print(f"Headers: {{'Authorization': 'Bearer ...token truncated...', 'Content-Type': 'application/json'}}")
    print(f"Request: {json.dumps(data, indent=2)}")
    
    response = requests.post(url, json=data, headers=headers)
    print(f"Response ({response.status_code}): {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 201:
        print("✅ Amenity created successfully")
        return response.json()
    else:
        print("❌ Failed to create amenity")
        return None

def test_create_amenity_unauthenticated():
    """Test creating an amenity without authentication."""
    print_separator("TESTING AMENITY CREATION (UNAUTHENTICATED)")
    
    url = f"{base_url}/amenities/"
    data = {
        "name": "Test Amenity"
    }
    
    print(f"POST {url}")
    print(f"Request: {json.dumps(data, indent=2)}")
    
    response = requests.post(url, json=data)
    print(f"Response ({response.status_code}): {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 401:
        print("✅ Authentication required (expected)")
    else:
        print("❌ Unexpected response")

def test_update_amenity(token, amenity_id):
    """Test updating an amenity (authenticated endpoint)."""
    print_separator("TESTING AMENITY UPDATE (AUTHENTICATED)")
    
    url = f"{base_url}/amenities/{amenity_id}"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    data = {
        "name": "Updated Test Amenity"
    }
    
    print(f"PUT {url}")
    print(f"Headers: {{'Authorization': 'Bearer ...token truncated...', 'Content-Type': 'application/json'}}")
    print(f"Request: {json.dumps(data, indent=2)}")
    
    response = requests.put(url, json=data, headers=headers)
    print(f"Response ({response.status_code}): {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200:
        print("✅ Amenity updated successfully")
        return response.json()
    else:
        print("❌ Failed to update amenity")
        return None

def test_update_amenity_unauthenticated(amenity_id):
    """Test updating an amenity without authentication."""
    print_separator("TESTING AMENITY UPDATE (UNAUTHENTICATED)")
    
    url = f"{base_url}/amenities/{amenity_id}"
    data = {
        "name": "Unauthenticated Update"
    }
    
    print(f"PUT {url}")
    print(f"Request: {json.dumps(data, indent=2)}")
    
    response = requests.put(url, json=data)
    print(f"Response ({response.status_code}): {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 401:
        print("✅ Authentication required (expected)")
    else:
        print("❌ Unexpected response")

def test_get_amenities():
    """Test getting all amenities (public endpoint)."""
    print_separator("TESTING GET ALL AMENITIES (PUBLIC)")
    
    url = f"{base_url}/amenities/"
    
    print(f"GET {url}")
    
    response = requests.get(url)
    print(f"Response ({response.status_code}): {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200:
        print("✅ Amenities retrieved successfully")
        return response.json()
    else:
        print("❌ Failed to retrieve amenities")
        return None

def test_get_amenity(amenity_id):
    """Test getting a specific amenity (public endpoint)."""
    print_separator("TESTING GET SPECIFIC AMENITY (PUBLIC)")
    
    url = f"{base_url}/amenities/{amenity_id}"
    
    print(f"GET {url}")
    
    response = requests.get(url)
    print(f"Response ({response.status_code}): {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200:
        print("✅ Amenity retrieved successfully")
        return response.json()
    else:
        print("❌ Failed to retrieve amenity")
        return None

if __name__ == "__main__":
    # Create a user
    user_data = create_user()
    
    if user_data:
        # Login and get token
        token = login(user_data["email"], user_data["password"])
        
        if token:
            # Test creating an amenity without authentication
            test_create_amenity_unauthenticated()
            
            # Test creating an amenity (authenticated)
            amenity_data = test_create_amenity(token)
            
            if amenity_data:
                amenity_id = amenity_data["id"]
                
                # Test updating the amenity without authentication
                test_update_amenity_unauthenticated(amenity_id)
                
                # Test updating the amenity (authenticated)
                test_update_amenity(token, amenity_id)
                
                # Test getting the amenity (public)
                test_get_amenity(amenity_id)
            
            # Test getting all amenities (public)
            test_get_amenities()
