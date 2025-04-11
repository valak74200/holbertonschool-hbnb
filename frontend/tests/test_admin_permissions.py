"""
Script to test administrator permissions.
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
    
    # Try to parse the response as JSON, but handle the case where it's not valid JSON
    try:
        response_json = response.json()
        print(f"Response ({response.status_code}): {json.dumps(response_json, indent=2)}")
    except json.JSONDecodeError:
        print(f"Response ({response.status_code}): {response.text}")
    
    if response.status_code == 201:
        print("✅ User created successfully")
        
        # Make the user an admin using the make_admin.py script
        import subprocess
        import os
        
        print("Making the user an admin using the make_admin.py script")
        script_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts", "make_admin.py")
        result = subprocess.run(["python", script_path, email], capture_output=True, text=True)
        print(result.stdout)
        
        if "is now an admin" in result.stdout:
            print("✅ User is now an admin")
        else:
            print("❌ Failed to make user an admin")
            print(result.stderr)
        
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
    
    # Try to parse the response as JSON, but handle the case where it's not valid JSON
    try:
        response_json = response.json()
        print(f"Response ({response.status_code}): {json.dumps(response_json, indent=2)}")
    except json.JSONDecodeError:
        print(f"Response ({response.status_code}): {response.text}")
    
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
    
    # Try to parse the response as JSON, but handle the case where it's not valid JSON
    try:
        response_json = response.json()
        if response.status_code == 200:
            token = response_json.get("access_token")
            print(f"Response ({response.status_code}): {{\"access_token\": \"...token truncated...\"}}") 
            print("✅ Login successful")
            return token
        else:
            print(f"Response ({response.status_code}): {json.dumps(response_json, indent=2)}")
            print("❌ Login failed")
            return None
    except json.JSONDecodeError:
        print(f"Response ({response.status_code}): {response.text}")
        print("❌ Login failed (not valid JSON)")
        return None

def test_create_user_as_admin(token):
    """Test creating a user as an admin."""
    print_separator("TESTING USER CREATION AS ADMIN")
    
    url = f"{base_url}/users/"
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
    
    # Try to parse the response as JSON, but handle the case where it's not valid JSON
    try:
        response_json = response.json()
        print(f"Response ({response.status_code}): {json.dumps(response_json, indent=2)}")
    except json.JSONDecodeError:
        print(f"Response ({response.status_code}): {response.text}")
    
    if response.status_code == 201:
        print("✅ User created successfully as admin")
        try:
            return response.json()
        except json.JSONDecodeError:
            print("Warning: Response is not valid JSON")
            return {"success": True}
    else:
        print("❌ Failed to create user as admin")
        return None

def test_create_user_as_regular(token):
    """Test creating a user as a regular user (should fail)."""
    print_separator("TESTING USER CREATION AS REGULAR USER (SHOULD FAIL)")
    
    url = f"{base_url}/users/"
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
    
    # Try to parse the response as JSON, but handle the case where it's not valid JSON
    try:
        response_json = response.json()
        print(f"Response ({response.status_code}): {json.dumps(response_json, indent=2)}")
        if response.status_code == 403 and "Admin privileges required" in str(response_json):
            print("✅ Admin privileges required (expected)")
            return True
        else:
            print("❌ Unexpected response")
            return False
    except json.JSONDecodeError:
        print(f"Response ({response.status_code}): {response.text}")
        print("❌ Unexpected response (not valid JSON)")
        return False

def test_update_user_as_admin(token, user_id):
    """Test updating a user as an admin."""
    print_separator("TESTING USER UPDATE AS ADMIN")
    
    url = f"{base_url}/users/{user_id}"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    data = {
        "first_name": "Updated",
        "last_name": "Name",
        "email": f"updated.email.{uuid.uuid4()}@example.com",
        "password": "newpassword123"
    }
    
    print(f"PUT {url}")
    print(f"Headers: {{'Authorization': 'Bearer ...token truncated...', 'Content-Type': 'application/json'}}")
    print(f"Request: {json.dumps(data, indent=2)}")
    
    response = requests.put(url, json=data, headers=headers)
    
    # Try to parse the response as JSON, but handle the case where it's not valid JSON
    try:
        response_json = response.json()
        print(f"Response ({response.status_code}): {json.dumps(response_json, indent=2)}")
    except json.JSONDecodeError:
        print(f"Response ({response.status_code}): {response.text}")
    
    if response.status_code == 200:
        print("✅ User updated successfully as admin")
        try:
            return response.json()
        except json.JSONDecodeError:
            print("Warning: Response is not valid JSON")
            return {"success": True}
    else:
        print("❌ Failed to update user as admin")
        return None

def test_create_amenity_as_admin(token):
    """Test creating an amenity as an admin."""
    print_separator("TESTING AMENITY CREATION AS ADMIN")
    
    url = f"{base_url}/amenities/"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    data = {
        "name": f"Test Amenity {uuid.uuid4()}"
    }
    
    print(f"POST {url}")
    print(f"Headers: {{'Authorization': 'Bearer ...token truncated...', 'Content-Type': 'application/json'}}")
    print(f"Request: {json.dumps(data, indent=2)}")
    
    response = requests.post(url, json=data, headers=headers)
    
    # Try to parse the response as JSON, but handle the case where it's not valid JSON
    try:
        response_json = response.json()
        print(f"Response ({response.status_code}): {json.dumps(response_json, indent=2)}")
    except json.JSONDecodeError:
        print(f"Response ({response.status_code}): {response.text}")
    
    if response.status_code == 201:
        print("✅ Amenity created successfully as admin")
        try:
            return response.json()
        except json.JSONDecodeError:
            print("Warning: Response is not valid JSON")
            return {"id": "dummy-id", "name": data["name"], "success": True}
    else:
        print("❌ Failed to create amenity as admin")
        return None

def test_create_amenity_as_regular(token):
    """Test creating an amenity as a regular user."""
    print_separator("TESTING AMENITY CREATION AS REGULAR USER")
    
    url = f"{base_url}/amenities/"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    data = {
        "name": f"Test Amenity {uuid.uuid4()}"
    }
    
    print(f"POST {url}")
    print(f"Headers: {{'Authorization': 'Bearer ...token truncated...', 'Content-Type': 'application/json'}}")
    print(f"Request: {json.dumps(data, indent=2)}")
    
    response = requests.post(url, json=data, headers=headers)
    
    # Try to parse the response as JSON, but handle the case where it's not valid JSON
    try:
        response_json = response.json()
        print(f"Response ({response.status_code}): {json.dumps(response_json, indent=2)}")
    except json.JSONDecodeError:
        print(f"Response ({response.status_code}): {response.text}")
    
    if response.status_code == 201:
        print("✅ Amenity created successfully as regular user")
        try:
            return response.json()
        except json.JSONDecodeError:
            print("Warning: Response is not valid JSON")
            return {"id": "dummy-id", "name": data["name"], "success": True}
    else:
        print("❌ Failed to create amenity as regular user")
        return None

def test_update_amenity_as_admin(token, amenity_id):
    """Test updating an amenity as an admin."""
    print_separator("TESTING AMENITY UPDATE AS ADMIN")
    
    url = f"{base_url}/amenities/{amenity_id}"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    data = {
        "name": f"Updated Amenity {uuid.uuid4()}"
    }
    
    print(f"PUT {url}")
    print(f"Headers: {{'Authorization': 'Bearer ...token truncated...', 'Content-Type': 'application/json'}}")
    print(f"Request: {json.dumps(data, indent=2)}")
    
    response = requests.put(url, json=data, headers=headers)
    
    # Try to parse the response as JSON, but handle the case where it's not valid JSON
    try:
        response_json = response.json()
        print(f"Response ({response.status_code}): {json.dumps(response_json, indent=2)}")
    except json.JSONDecodeError:
        print(f"Response ({response.status_code}): {response.text}")
    
    if response.status_code == 200:
        print("✅ Amenity updated successfully as admin")
        try:
            return response.json()
        except json.JSONDecodeError:
            print("Warning: Response is not valid JSON")
            return {"success": True}
    else:
        print("❌ Failed to update amenity as admin")
        return None

def test_update_amenity_as_regular(token, amenity_id):
    """Test updating an amenity as a regular user."""
    print_separator("TESTING AMENITY UPDATE AS REGULAR USER")
    
    url = f"{base_url}/amenities/{amenity_id}"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    data = {
        "name": f"Updated Amenity {uuid.uuid4()}"
    }
    
    print(f"PUT {url}")
    print(f"Headers: {{'Authorization': 'Bearer ...token truncated...', 'Content-Type': 'application/json'}}")
    print(f"Request: {json.dumps(data, indent=2)}")
    
    response = requests.put(url, json=data, headers=headers)
    
    # Try to parse the response as JSON, but handle the case where it's not valid JSON
    try:
        response_json = response.json()
        print(f"Response ({response.status_code}): {json.dumps(response_json, indent=2)}")
    except json.JSONDecodeError:
        print(f"Response ({response.status_code}): {response.text}")
    
    if response.status_code == 200:
        print("✅ Amenity updated successfully as regular user")
        try:
            return response.json()
        except json.JSONDecodeError:
            print("Warning: Response is not valid JSON")
            return {"success": True}
    else:
        print("❌ Failed to update amenity as regular user")
        return None

def test_update_place_as_admin(token, place_id):
    """Test updating a place as an admin (even if not the owner)."""
    print_separator("TESTING PLACE UPDATE AS ADMIN (NOT OWNER)")
    
    url = f"{base_url}/places/{place_id}"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    data = {
        "title": f"Updated Place {uuid.uuid4()}",
        "description": "Updated by admin",
        "price": 200.0
    }
    
    print(f"PUT {url}")
    print(f"Headers: {{'Authorization': 'Bearer ...token truncated...', 'Content-Type': 'application/json'}}")
    print(f"Request: {json.dumps(data, indent=2)}")
    
    response = requests.put(url, json=data, headers=headers)
    
    # Try to parse the response as JSON, but handle the case where it's not valid JSON
    try:
        response_json = response.json()
        print(f"Response ({response.status_code}): {json.dumps(response_json, indent=2)}")
    except json.JSONDecodeError:
        print(f"Response ({response.status_code}): {response.text}")
    
    if response.status_code == 200:
        print("✅ Place updated successfully as admin (not owner)")
        try:
            return response.json()
        except json.JSONDecodeError:
            print("Warning: Response is not valid JSON")
            return {"success": True}
    else:
        print("❌ Failed to update place as admin (not owner)")
        return None

def test_update_place_as_regular(token, place_id):
    """Test updating a place as a regular user (not the owner, should fail)."""
    print_separator("TESTING PLACE UPDATE AS REGULAR USER (NOT OWNER, SHOULD FAIL)")
    
    url = f"{base_url}/places/{place_id}"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    data = {
        "title": f"Updated Place {uuid.uuid4()}",
        "description": "Updated by regular user",
        "price": 200.0
    }
    
    print(f"PUT {url}")
    print(f"Headers: {{'Authorization': 'Bearer ...token truncated...', 'Content-Type': 'application/json'}}")
    print(f"Request: {json.dumps(data, indent=2)}")
    
    response = requests.put(url, json=data, headers=headers)
    
    # Try to parse the response as JSON, but handle the case where it's not valid JSON
    try:
        response_json = response.json()
        print(f"Response ({response.status_code}): {json.dumps(response_json, indent=2)}")
        if response.status_code == 403 and "Unauthorized action" in str(response_json):
            print("✅ Unauthorized action (expected)")
            return True
        else:
            print("❌ Unexpected response")
            return False
    except json.JSONDecodeError:
        print(f"Response ({response.status_code}): {response.text}")
        print("❌ Unexpected response (not valid JSON)")
        return False

def test_update_review_as_admin(token, review_id):
    """Test updating a review as an admin (even if not the author)."""
    print_separator("TESTING REVIEW UPDATE AS ADMIN (NOT AUTHOR)")
    
    url = f"{base_url}/reviews/{review_id}"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    data = {
        "text": f"Updated review {uuid.uuid4()}",
        "rating": 4
    }
    
    print(f"PUT {url}")
    print(f"Headers: {{'Authorization': 'Bearer ...token truncated...', 'Content-Type': 'application/json'}}")
    print(f"Request: {json.dumps(data, indent=2)}")
    
    response = requests.put(url, json=data, headers=headers)
    
    # Try to parse the response as JSON, but handle the case where it's not valid JSON
    try:
        response_json = response.json()
        print(f"Response ({response.status_code}): {json.dumps(response_json, indent=2)}")
    except json.JSONDecodeError:
        print(f"Response ({response.status_code}): {response.text}")
    
    if response.status_code == 200:
        print("✅ Review updated successfully as admin (not author)")
        try:
            return response.json()
        except json.JSONDecodeError:
            print("Warning: Response is not valid JSON")
            return {"success": True}
    else:
        print("❌ Failed to update review as admin (not author)")
        return None

def test_update_review_as_regular(token, review_id):
    """Test updating a review as a regular user (not the author, should fail)."""
    print_separator("TESTING REVIEW UPDATE AS REGULAR USER (NOT AUTHOR, SHOULD FAIL)")
    
    url = f"{base_url}/reviews/{review_id}"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    data = {
        "text": f"Updated review {uuid.uuid4()}",
        "rating": 4
    }
    
    print(f"PUT {url}")
    print(f"Headers: {{'Authorization': 'Bearer ...token truncated...', 'Content-Type': 'application/json'}}")
    print(f"Request: {json.dumps(data, indent=2)}")
    
    response = requests.put(url, json=data, headers=headers)
    
    # Try to parse the response as JSON, but handle the case where it's not valid JSON
    try:
        response_json = response.json()
        print(f"Response ({response.status_code}): {json.dumps(response_json, indent=2)}")
        if response.status_code == 403 and "Unauthorized action" in str(response_json):
            print("✅ Unauthorized action (expected)")
            return True
        else:
            print("❌ Unexpected response")
            return False
    except json.JSONDecodeError:
        print(f"Response ({response.status_code}): {response.text}")
        print("❌ Unexpected response (not valid JSON)")
        return False

def test_delete_review_as_admin(token, review_id):
    """Test deleting a review as an admin (even if not the author)."""
    print_separator("TESTING REVIEW DELETION AS ADMIN (NOT AUTHOR)")
    
    url = f"{base_url}/reviews/{review_id}"
    headers = {"Authorization": f"Bearer {token}"}
    
    print(f"DELETE {url}")
    print(f"Headers: {{'Authorization': 'Bearer ...token truncated...'}}")
    
    response = requests.delete(url, headers=headers)
    
    # Try to parse the response as JSON, but handle the case where it's not valid JSON
    try:
        response_json = response.json()
        print(f"Response ({response.status_code}): {json.dumps(response_json, indent=2)}")
    except json.JSONDecodeError:
        print(f"Response ({response.status_code}): {response.text}")
    
    if response.status_code == 200:
        print("✅ Review deleted successfully as admin (not author)")
        return True
    else:
        print("❌ Failed to delete review as admin (not author)")
        return False

def test_delete_review_as_regular(token, review_id):
    """Test deleting a review as a regular user (not the author, should fail)."""
    print_separator("TESTING REVIEW DELETION AS REGULAR USER (NOT AUTHOR, SHOULD FAIL)")
    
    url = f"{base_url}/reviews/{review_id}"
    headers = {"Authorization": f"Bearer {token}"}
    
    print(f"DELETE {url}")
    print(f"Headers: {{'Authorization': 'Bearer ...token truncated...'}}")
    
    response = requests.delete(url, headers=headers)
    
    # Try to parse the response as JSON, but handle the case where it's not valid JSON
    try:
        response_json = response.json()
        print(f"Response ({response.status_code}): {json.dumps(response_json, indent=2)}")
        if response.status_code == 403 and "Unauthorized action" in str(response_json):
            print("✅ Unauthorized action (expected)")
            return True
        else:
            print("❌ Unexpected response")
            return False
    except json.JSONDecodeError:
        print(f"Response ({response.status_code}): {response.text}")
        print("❌ Unexpected response (not valid JSON)")
        return False

def create_place(token, user_id):
    """Create a place for testing."""
    print_separator("CREATING TEST PLACE")
    
    url = f"{base_url}/places/"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    data = {
        "title": f"Test Place {uuid.uuid4()}",
        "description": "A test place",
        "price": 100.0,
        "latitude": 37.7749,
        "longitude": -122.4194,
        "owner_id": user_id
    }
    
    print(f"POST {url}")
    print(f"Headers: {{'Authorization': 'Bearer ...token truncated...', 'Content-Type': 'application/json'}}")
    print(f"Request: {json.dumps(data, indent=2)}")
    
    response = requests.post(url, json=data, headers=headers)
    
    # Try to parse the response as JSON, but handle the case where it's not valid JSON
    try:
        response_json = response.json()
        print(f"Response ({response.status_code}): {json.dumps(response_json, indent=2)}")
    except json.JSONDecodeError:
        print(f"Response ({response.status_code}): {response.text}")
    
    if response.status_code == 201:
        print("✅ Place created successfully")
        try:
            return response.json()
        except json.JSONDecodeError:
            print("Warning: Response is not valid JSON")
            return {"id": "dummy-id", "success": True}
    else:
        print("❌ Failed to create place")
        return None

def create_review(token, place_id):
    """Create a review for testing."""
    print_separator("CREATING TEST REVIEW")
    
    url = f"{base_url}/reviews/"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    data = {
        "text": f"Test review {uuid.uuid4()}",
        "rating": 5,
        "place_id": place_id,
        "user_id": "dummy-id"  # This will be overridden by the server
    }
    
    print(f"POST {url}")
    print(f"Headers: {{'Authorization': 'Bearer ...token truncated...', 'Content-Type': 'application/json'}}")
    print(f"Request: {json.dumps(data, indent=2)}")
    
    response = requests.post(url, json=data, headers=headers)
    
    # Try to parse the response as JSON, but handle the case where it's not valid JSON
    try:
        response_json = response.json()
        print(f"Response ({response.status_code}): {json.dumps(response_json, indent=2)}")
    except json.JSONDecodeError:
        print(f"Response ({response.status_code}): {response.text}")
    
    if response.status_code == 201:
        print("✅ Review created successfully")
        try:
            return response.json()
        except json.JSONDecodeError:
            print("Warning: Response is not valid JSON")
            return {"id": "dummy-id", "success": True}
    else:
        print("❌ Failed to create review")
        return None

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
            # Test user creation
            test_create_user_as_admin(admin_token)
            test_create_user_as_regular(regular_token)
            
            # Get user IDs
            response = requests.get(f"{base_url}/users/")
            users = response.json()
            regular_user_id = next((user["id"] for user in users if user["email"] == regular_data["email"]), None)
            
            if regular_user_id:
                # Test user update
                test_update_user_as_admin(admin_token, regular_user_id)
            
            # Test amenity creation and update
            amenity_data = test_create_amenity_as_admin(admin_token)
            test_create_amenity_as_regular(regular_token)
            
            if amenity_data:
                amenity_id = amenity_data["id"]
                test_update_amenity_as_admin(admin_token, amenity_id)
                test_update_amenity_as_regular(regular_token, amenity_id)
            
            # Create a place as regular user
            place_data = create_place(regular_token, regular_user_id)
            
            if place_data:
                place_id = place_data["id"]
                
                # Test place update
                test_update_place_as_admin(admin_token, place_id)
                
                # Create a review as admin
                review_data = create_review(admin_token, place_id)
                
                if review_data:
                    review_id = review_data["id"]
                    
                    # Test review update and delete
                    test_update_review_as_regular(regular_token, review_id)
                    test_update_review_as_admin(admin_token, review_id)
                    
                    # Create another review for delete test
                    another_review_data = create_review(admin_token, place_id)
                    
                    if another_review_data:
                        another_review_id = another_review_data["id"]
                        test_delete_review_as_regular(regular_token, another_review_id)
                        test_delete_review_as_admin(admin_token, another_review_id)
            
            print_separator("ALL TESTS COMPLETED")
