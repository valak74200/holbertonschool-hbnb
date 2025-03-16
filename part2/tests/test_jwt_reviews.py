"""
Script to test JWT authentication for review endpoints.
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

def create_place(token, user_id):
    """Create a place for testing reviews."""
    print_separator("CREATING TEST PLACE")
    
    url = f"{base_url}/places/"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    data = {
        "title": "Test Place for Reviews",
        "description": "A test place created for review testing",
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

def test_create_review(token, place_id, user_id):
    """Test creating a review (authenticated endpoint)."""
    print_separator("TESTING REVIEW CREATION (AUTHENTICATED)")
    
    url = f"{base_url}/reviews/"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    data = {
        "text": "This is a test review",
        "rating": 5,
        "place_id": place_id,
        "user_id": user_id  # This will be overridden by the server
    }
    
    print(f"POST {url}")
    print(f"Headers: {{'Authorization': 'Bearer ...token truncated...', 'Content-Type': 'application/json'}}")
    print(f"Request: {json.dumps(data, indent=2)}")
    
    response = requests.post(url, json=data, headers=headers)
    print(f"Response ({response.status_code}): {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 201:
        print("✅ Review created successfully")
        return response.json()
    else:
        print("❌ Failed to create review")
        return None

def test_create_review_own_place(token, place_id, user_id):
    """Test creating a review for a place the user owns (should fail)."""
    print_separator("TESTING REVIEW CREATION FOR OWN PLACE (SHOULD FAIL)")
    
    url = f"{base_url}/reviews/"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    data = {
        "text": "This is a review for my own place",
        "rating": 5,
        "place_id": place_id,
        "user_id": user_id  # This will be overridden by the server
    }
    
    print(f"POST {url}")
    print(f"Headers: {{'Authorization': 'Bearer ...token truncated...', 'Content-Type': 'application/json'}}")
    print(f"Request: {json.dumps(data, indent=2)}")
    
    response = requests.post(url, json=data, headers=headers)
    print(f"Response ({response.status_code}): {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 400 and "You cannot review your own place" in str(response.json()):
        print("✅ Cannot review own place (expected)")
    else:
        print("❌ Unexpected response")

def test_create_duplicate_review(token, place_id, user_id):
    """Test creating a duplicate review for a place (should fail)."""
    print_separator("TESTING DUPLICATE REVIEW CREATION (SHOULD FAIL)")
    
    # First create a review
    first_review = test_create_review(token, place_id, user_id)
    
    if not first_review:
        print("❌ Cannot test duplicate review - first review failed")
        return
    
    # Try to create another review for the same place
    url = f"{base_url}/reviews/"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    data = {
        "text": "This is another review for the same place",
        "rating": 4,
        "place_id": place_id
    }
    
    print(f"POST {url}")
    print(f"Headers: {{'Authorization': 'Bearer ...token truncated...', 'Content-Type': 'application/json'}}")
    print(f"Request: {json.dumps(data, indent=2)}")
    
    response = requests.post(url, json=data, headers=headers)
    print(f"Response ({response.status_code}): {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 400 and "You have already reviewed this place" in str(response.json()):
        print("✅ Cannot create duplicate review (expected)")
    else:
        print("❌ Unexpected response")
    
    return first_review

def test_update_review(token, review_id):
    """Test updating a review (authenticated endpoint)."""
    print_separator("TESTING REVIEW UPDATE (AUTHENTICATED, OWNER)")
    
    url = f"{base_url}/reviews/{review_id}"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    data = {
        "text": "This is an updated test review",
        "rating": 4
    }
    
    print(f"PUT {url}")
    print(f"Headers: {{'Authorization': 'Bearer ...token truncated...', 'Content-Type': 'application/json'}}")
    print(f"Request: {json.dumps(data, indent=2)}")
    
    response = requests.put(url, json=data, headers=headers)
    print(f"Response ({response.status_code}): {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200:
        print("✅ Review updated successfully")
        return response.json()
    else:
        print("❌ Failed to update review")
        return None

def test_update_review_unauthorized(token, review_id):
    """Test updating a review that the user didn't create (should fail)."""
    print_separator("TESTING REVIEW UPDATE (AUTHENTICATED, NOT OWNER)")
    
    # This test assumes that review_id belongs to a different user
    url = f"{base_url}/reviews/{review_id}"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    data = {
        "text": "This update should fail",
        "rating": 1
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

def test_delete_review(token, review_id):
    """Test deleting a review (authenticated endpoint)."""
    print_separator("TESTING REVIEW DELETION (AUTHENTICATED, OWNER)")
    
    url = f"{base_url}/reviews/{review_id}"
    headers = {"Authorization": f"Bearer {token}"}
    
    print(f"DELETE {url}")
    print(f"Headers: {{'Authorization': 'Bearer ...token truncated...'}}")
    
    response = requests.delete(url, headers=headers)
    print(f"Response ({response.status_code}): {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200:
        print("✅ Review deleted successfully")
        return True
    else:
        print("❌ Failed to delete review")
        return False

def test_delete_review_unauthorized(token, review_id):
    """Test deleting a review that the user didn't create (should fail)."""
    print_separator("TESTING REVIEW DELETION (AUTHENTICATED, NOT OWNER)")
    
    # This test assumes that review_id belongs to a different user
    url = f"{base_url}/reviews/{review_id}"
    headers = {"Authorization": f"Bearer {token}"}
    
    print(f"DELETE {url}")
    print(f"Headers: {{'Authorization': 'Bearer ...token truncated...'}}")
    
    response = requests.delete(url, headers=headers)
    print(f"Response ({response.status_code}): {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 403 and "Unauthorized action" in str(response.json()):
        print("✅ Unauthorized action (expected)")
    else:
        print("❌ Unexpected response")

def test_get_reviews():
    """Test getting all reviews (public endpoint)."""
    print_separator("TESTING GET ALL REVIEWS (PUBLIC)")
    
    url = f"{base_url}/reviews/"
    
    print(f"GET {url}")
    
    response = requests.get(url)
    print(f"Response ({response.status_code}): {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200:
        print("✅ Reviews retrieved successfully")
        return response.json()
    else:
        print("❌ Failed to retrieve reviews")
        return None

def test_get_review(review_id):
    """Test getting a specific review (public endpoint)."""
    print_separator("TESTING GET SPECIFIC REVIEW (PUBLIC)")
    
    url = f"{base_url}/reviews/{review_id}"
    
    print(f"GET {url}")
    
    response = requests.get(url)
    print(f"Response ({response.status_code}): {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200:
        print("✅ Review retrieved successfully")
        return response.json()
    else:
        print("❌ Failed to retrieve review")
        return None

if __name__ == "__main__":
    # Create two users
    user1_data = create_user()
    user2_data = create_user()
    
    if user1_data and user2_data:
        # Login as user1
        token1 = login(user1_data["email"], user1_data["password"])
        
        if token1:
            # Get user1's ID from the response
            response = requests.get(f"{base_url}/users/", headers={"Authorization": f"Bearer {token1}"})
            users = response.json()
            user1_id = next((user["id"] for user in users if user["email"] == user1_data["email"]), None)
            
            if not user1_id:
                print("❌ Failed to get user1 ID")
                exit(1)
                
            # Create a place as user1
            place_data = create_place(token1, user1_id)
            
            if place_data:
                place_id = place_data["id"]
                
                # Try to review own place (should fail)
                test_create_review_own_place(token1, place_id, user1_id)
                
                # Login as user2
                token2 = login(user2_data["email"], user2_data["password"])
                
                if token2:
                    # Get user2's ID from the response
                    response = requests.get(f"{base_url}/users/", headers={"Authorization": f"Bearer {token2}"})
                    users = response.json()
                    user2_id = next((user["id"] for user in users if user["email"] == user2_data["email"]), None)
                    
                    if not user2_id:
                        print("❌ Failed to get user2 ID")
                        exit(1)
                        
                    # Create a review as user2
                    review_data = test_create_review(token2, place_id, user2_id)
                    
                    if review_data:
                        review_id = review_data["id"]
                        
                        # Try to create another review for the same place (should fail)
                        test_create_duplicate_review(token2, place_id, user2_id)
                        
                        # Update the review as user2 (owner)
                        test_update_review(token2, review_id)
                        
                        # Try to update the review as user1 (not owner, should fail)
                        test_update_review_unauthorized(token1, review_id)
                        
                        # Get the review (public)
                        test_get_review(review_id)
                        
                        # Try to delete the review as user1 (not owner, should fail)
                        test_delete_review_unauthorized(token1, review_id)
                        
                        # Delete the review as user2 (owner)
                        test_delete_review(token2, review_id)
                    
                    # Get all reviews (public)
                    test_get_reviews()
