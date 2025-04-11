"""
Script to test JWT authentication for place endpoints.
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

def test_create_place(token, user_id):
    """Test creating a place (authenticated endpoint)."""
    print_separator("TESTING PLACE CREATION (AUTHENTICATED)")
    
    url = f"{base_url}/places/"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    data = {
        "title": "Test Place",
        "description": "A test place created for JWT testing",
        "price": 100.0,
        "latitude": 37.7749,
        "longitude": -122.4194,
        "owner_id": user_id  # This will be overridden by the server
    }
    
    print(f"POST {url}")
    print(f"Headers: {{'Authorization': 'Bearer ...token truncated...', 'Content-Type': 'application/json'}}")
    print(f"Request: {json.dumps(data, indent=2)}")
    
    response = requests.post(url, json=data, headers=headers)
    print(f"Response ({response.status_code}): {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 201:
        print("✅ Place created successfully")
        return response.json()
    else:
        print("❌ Failed to create place")
        return None

def test_create_place_unauthenticated():
    """Test creating a place without authentication."""
    print_separator("TESTING PLACE CREATION (UNAUTHENTICATED)")
    
    url = f"{base_url}/places/"
    data = {
        "title": "Test Place",
        "description": "A test place created for JWT testing",
        "price": 100.0,
        "latitude": 37.7749,
        "longitude": -122.4194,
        "owner_id": "dummy-id"  # Include owner_id to pass validation
    }
    
    print(f"POST {url}")
    print(f"Request: {json.dumps(data, indent=2)}")
    
    response = requests.post(url, json=data)
    print(f"Response ({response.status_code}): {json.dumps(response.json(), indent=2)}")
    
    # The API might return 401 (Unauthorized) or 403 (Forbidden)
    if response.status_code in [401, 403]:
        print("✅ Authentication required (expected)")
    else:
        print("❌ Unexpected response")

def test_update_place(token, place_id):
    """Test updating a place (authenticated endpoint)."""
    print_separator("TESTING PLACE UPDATE (AUTHENTICATED, OWNER)")
    
    url = f"{base_url}/places/{place_id}"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    data = {
        "title": "Updated Test Place",
        "description": "An updated test place for JWT testing",
        "price": 150.0
    }
    
    print(f"PUT {url}")
    print(f"Headers: {{'Authorization': 'Bearer ...token truncated...', 'Content-Type': 'application/json'}}")
    print(f"Request: {json.dumps(data, indent=2)}")
    
    response = requests.put(url, json=data, headers=headers)
    print(f"Response ({response.status_code}): {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200:
        print("✅ Place updated successfully")
        return response.json()
    else:
        print("❌ Failed to update place")
        return None

def test_update_place_unauthorized(token, place_id):
    """Test updating a place that the user doesn't own."""
    print_separator("TESTING PLACE UPDATE (AUTHENTICATED, NOT OWNER)")
    
    # This test assumes that place_id belongs to a different user
    url = f"{base_url}/places/{place_id}"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    data = {
        "title": "Unauthorized Update",
        "description": "This update should fail",
        "price": 200.0
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

def test_get_places():
    """Test getting all places (public endpoint)."""
    print_separator("TESTING GET ALL PLACES (PUBLIC)")
    
    url = f"{base_url}/places/"
    
    print(f"GET {url}")
    
    response = requests.get(url)
    print(f"Response ({response.status_code}): {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200:
        print("✅ Places retrieved successfully")
        return response.json()
    else:
        print("❌ Failed to retrieve places")
        return None

def test_get_place(place_id):
    """Test getting a specific place (public endpoint)."""
    print_separator("TESTING GET SPECIFIC PLACE (PUBLIC)")
    
    url = f"{base_url}/places/{place_id}"
    
    print(f"GET {url}")
    
    response = requests.get(url)
    print(f"Response ({response.status_code}): {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200:
        print("✅ Place retrieved successfully")
        return response.json()
    else:
        print("❌ Failed to retrieve place")
        return None

if __name__ == "__main__":
    # Create a user
    user_data = create_user()
    
    if user_data:
        # Login and get token
        token = login(user_data["email"], user_data["password"])
        
        if token:
            # Get user ID from the response
            response = requests.get(f"{base_url}/users/", headers={"Authorization": f"Bearer {token}"})
            users = response.json()
            user_id = next((user["id"] for user in users if user["email"] == user_data["email"]), None)
            
            if not user_id:
                print("❌ Failed to get user ID")
                exit(1)
                
            # Test creating a place (authenticated)
            place_data = test_create_place(token, user_id)
            
            if place_data:
                place_id = place_data["id"]
                
                # Test updating the place (authenticated, owner)
                test_update_place(token, place_id)
                
                # Test getting the place (public)
                test_get_place(place_id)
            
            # Test creating a place without authentication
            test_create_place_unauthenticated()
            
            # Test getting all places (public)
            places = test_get_places()
            
            if places and len(places) > 1:
                # Test updating a place that the user doesn't own
                other_place_id = next((place["id"] for place in places if place["id"] != place_id), None)
                if other_place_id:
                    test_update_place_unauthorized(token, other_place_id)
