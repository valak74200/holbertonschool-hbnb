#!/usr/bin/env python3
"""
Script to test the relationships and CRUD operations for all entities.
"""

import requests
import json
import sys
import os
import uuid

# Base URL for the API
BASE_URL = 'http://127.0.0.1:5000/api/v1'

# Test users
ADMIN_USER = {
    'email': 'admin@hbnb.io',
    'password': 'admin1234'
}

# Generate unique email addresses for each test run
def get_test_user1():
    unique_id = str(uuid.uuid4())[:8]
    return {
        'first_name': 'Test',
        'last_name': 'User1',
        'email': f'test1_{unique_id}@example.com',
        'password': 'password123'
    }

def get_test_user2():
    unique_id = str(uuid.uuid4())[:8]
    return {
        'first_name': 'Test',
        'last_name': 'User2',
        'email': f'test2_{unique_id}@example.com',
        'password': 'password123'
    }

# Test data
TEST_PLACE = {
    'title': 'Test Place',
    'description': 'A place for testing',
    'price': 100.0,
    'latitude': 40.7128,
    'longitude': -74.0060,
    'owner_id': 'placeholder'  # This will be overwritten by the API with the current user's ID
}

TEST_AMENITY = {
    'name': 'Test Amenity'
}

TEST_REVIEW = {
    'text': 'Great place!',
    'rating': 5
}

def login(email, password):
    """
    Login to the API and get an access token.
    
    Args:
        email: The email of the user
        password: The password of the user
        
    Returns:
        The access token
    """
    response = requests.post(f'{BASE_URL}/auth/login', json={
        'email': email,
        'password': password
    })
    
    if response.status_code != 200:
        print(f'Error logging in: {response.text}')
        return None
    
    return response.json()['access_token']

def register_user(user_data):
    """
    Register a new user.
    
    Args:
        user_data: The user data
        
    Returns:
        The user ID
    """
    response = requests.post(f'{BASE_URL}/users/', json=user_data)
    
    if response.status_code != 201:
        print(f'Error registering user: {response.text}')
        return None
    
    return response.json()['id']

def create_place(token, place_data):
    """
    Create a new place.
    
    Args:
        token: The access token
        place_data: The place data
        
    Returns:
        The place ID
    """
    headers = {'Authorization': f'Bearer {token}'}
    # Make a copy of the place_data to avoid modifying the original
    data = dict(place_data)
    
    # Set the owner_id to a placeholder value if it's not already set
    if 'owner_id' not in data:
        data['owner_id'] = 'placeholder'
    
    response = requests.post(f'{BASE_URL}/places/', json=data, headers=headers)
    
    if response.status_code != 201:
        print(f'Error creating place: {response.text}')
        return None
    
    return response.json()['id']

def create_amenity(token, amenity_data):
    """
    Create a new amenity.
    
    Args:
        token: The access token
        amenity_data: The amenity data
        
    Returns:
        The amenity ID
    """
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.post(f'{BASE_URL}/amenities/', json=amenity_data, headers=headers)
    
    if response.status_code != 201:
        print(f'Error creating amenity: {response.text}')
        return None
    
    return response.json()['id']

def create_review(token, review_data, place_id):
    """
    Create a new review.
    
    Args:
        token: The access token
        review_data: The review data
        place_id: The place ID
        
    Returns:
        The review ID
    """
    headers = {'Authorization': f'Bearer {token}'}
    # Make a copy of the review_data to avoid modifying the original
    data = dict(review_data)
    
    # Set the place_id
    data['place_id'] = place_id
    
    # Set the user_id to a placeholder value if it's not already set
    if 'user_id' not in data:
        data['user_id'] = 'placeholder'
    
    response = requests.post(f'{BASE_URL}/reviews/', json=data, headers=headers)
    
    if response.status_code != 201:
        print(f'Error creating review: {response.text}')
        return None
    
    return response.json()['id']

def get_place(place_id):
    """
    Get a place by ID.
    
    Args:
        place_id: The place ID
        
    Returns:
        The place data
    """
    response = requests.get(f'{BASE_URL}/places/{place_id}')
    
    if response.status_code != 200:
        print(f'Error getting place: {response.text}')
        return None
    
    return response.json()

def get_review(review_id):
    """
    Get a review by ID.
    
    Args:
        review_id: The review ID
        
    Returns:
        The review data
    """
    response = requests.get(f'{BASE_URL}/reviews/{review_id}')
    
    if response.status_code != 200:
        print(f'Error getting review: {response.text}')
        return None
    
    return response.json()

def update_place(token, place_id, place_data):
    """
    Update a place.
    
    Args:
        token: The access token
        place_id: The place ID
        place_data: The place data
        
    Returns:
        True if successful, False otherwise
    """
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.put(f'{BASE_URL}/places/{place_id}', json=place_data, headers=headers)
    
    if response.status_code != 200:
        print(f'Error updating place: {response.text}')
        return False
    
    return True

def update_review(token, review_id, review_data):
    """
    Update a review.
    
    Args:
        token: The access token
        review_id: The review ID
        review_data: The review data
        
    Returns:
        True if successful, False otherwise
    """
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.put(f'{BASE_URL}/reviews/{review_id}', json=review_data, headers=headers)
    
    if response.status_code != 200:
        print(f'Error updating review: {response.text}')
        return False
    
    return True

def delete_place(token, place_id):
    """
    Delete a place.
    
    Args:
        token: The access token
        place_id: The place ID
        
    Returns:
        True if successful, False otherwise
    """
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.delete(f'{BASE_URL}/places/{place_id}', headers=headers)
    
    if response.status_code != 200:
        print(f'Error deleting place: {response.text}')
        return False
    
    return True

def delete_review(token, review_id):
    """
    Delete a review.
    
    Args:
        token: The access token
        review_id: The review ID
        
    Returns:
        True if successful, False otherwise
    """
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.delete(f'{BASE_URL}/reviews/{review_id}', headers=headers)
    
    if response.status_code != 200:
        print(f'Error deleting review: {response.text}')
        return False
    
    return True

def delete_user(token, user_id):
    """
    Delete a user.
    
    Args:
        token: The access token
        user_id: The user ID
        
    Returns:
        True if successful, False otherwise
    """
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.delete(f'{BASE_URL}/users/{user_id}', headers=headers)
    
    if response.status_code != 200:
        print(f'Error deleting user: {response.text}')
        return False
    
    return True

def test_user_place_relationship():
    """
    Test the User-Place relationship.
    """
    print("\n=== Testing User-Place Relationship ===")
    
    # Get a test user with a unique email
    test_user = get_test_user1()
    
    # Register the test user
    user_id = register_user(test_user)
    if not user_id:
        print("Failed to register test user")
        return False
    
    print(f"Registered test user with ID: {user_id}")
    
    # Login as the test user
    token = login(test_user['email'], test_user['password'])
    if not token:
        print("Failed to login as test user")
        return False
    
    print("Logged in as test user")
    
    # Create a place
    place_data = dict(TEST_PLACE)
    place_id = create_place(token, place_data)
    if not place_id:
        print("Failed to create place")
        return False
    
    print(f"Created place with ID: {place_id}")
    
    # Get the place
    place = get_place(place_id)
    if not place:
        print("Failed to get place")
        return False
    
    # Verify the place owner
    if place['owner']['id'] != user_id:
        print(f"Place owner ID ({place['owner']['id']}) does not match user ID ({user_id})")
        return False
    
    print("Place owner ID matches user ID")
    
    # Update the place
    update_data = {'title': 'Updated Test Place'}
    if not update_place(token, place_id, update_data):
        print("Failed to update place")
        return False
    
    print("Updated place")
    
    # Get the updated place
    updated_place = get_place(place_id)
    if not updated_place:
        print("Failed to get updated place")
        return False
    
    # Verify the update
    if updated_place['title'] != update_data['title']:
        print(f"Place title ({updated_place['title']}) does not match update data ({update_data['title']})")
        return False
    
    print("Place title matches update data")
    
    # Delete the place
    if not delete_place(token, place_id):
        print("Failed to delete place")
        return False
    
    print("Deleted place")
    
    # Try to get the deleted place
    deleted_place = get_place(place_id)
    if deleted_place:
        print("Place was not deleted")
        return False
    
    print("Place was successfully deleted")
    
    # Delete the user
    if not delete_user(token, user_id):
        print("Failed to delete user")
        return False
    
    print("Deleted user")
    
    return True

def test_place_review_relationship():
    """
    Test the Place-Review relationship.
    """
    print("\n=== Testing Place-Review Relationship ===")
    
    # Get test users with unique emails
    test_user1 = get_test_user1()
    test_user2 = get_test_user2()
    
    # Register two test users
    user1_id = register_user(test_user1)
    if not user1_id:
        print("Failed to register test user 1")
        return False
    
    print(f"Registered test user 1 with ID: {user1_id}")
    
    user2_id = register_user(test_user2)
    if not user2_id:
        print("Failed to register test user 2")
        return False
    
    print(f"Registered test user 2 with ID: {user2_id}")
    
    # Login as test user 1
    token1 = login(test_user1['email'], test_user1['password'])
    if not token1:
        print("Failed to login as test user 1")
        return False
    
    print("Logged in as test user 1")
    
    # Login as test user 2
    token2 = login(test_user2['email'], test_user2['password'])
    if not token2:
        print("Failed to login as test user 2")
        return False
    
    print("Logged in as test user 2")
    
    # Create a place as test user 1
    place_data = dict(TEST_PLACE)
    place_id = create_place(token1, place_data)
    if not place_id:
        print("Failed to create place")
        return False
    
    print(f"Created place with ID: {place_id}")
    
    # Create a review as test user 2
    review_data = dict(TEST_REVIEW)
    review_id = create_review(token2, review_data, place_id)
    if not review_id:
        print("Failed to create review")
        return False
    
    print(f"Created review with ID: {review_id}")
    
    # Get the review
    review = get_review(review_id)
    if not review:
        print("Failed to get review")
        return False
    
    # Verify the review place
    if review['place']['id'] != place_id:
        print(f"Review place ID ({review['place']['id']}) does not match place ID ({place_id})")
        return False
    
    print("Review place ID matches place ID")
    
    # Verify the review user
    if review['user']['id'] != user2_id:
        print(f"Review user ID ({review['user']['id']}) does not match user ID ({user2_id})")
        return False
    
    print("Review user ID matches user ID")
    
    # Update the review
    update_data = {'text': 'Updated review text'}
    if not update_review(token2, review_id, update_data):
        print("Failed to update review")
        return False
    
    print("Updated review")
    
    # Get the updated review
    updated_review = get_review(review_id)
    if not updated_review:
        print("Failed to get updated review")
        return False
    
    # Verify the update
    if updated_review['text'] != update_data['text']:
        print(f"Review text ({updated_review['text']}) does not match update data ({update_data['text']})")
        return False
    
    print("Review text matches update data")
    
    # Delete the review
    if not delete_review(token2, review_id):
        print("Failed to delete review")
        return False
    
    print("Deleted review")
    
    # Try to get the deleted review
    deleted_review = get_review(review_id)
    if deleted_review:
        print("Review was not deleted")
        return False
    
    print("Review was successfully deleted")
    
    # Delete the place
    if not delete_place(token1, place_id):
        print("Failed to delete place")
        return False
    
    print("Deleted place")
    
    # Delete the users
    if not delete_user(token1, user1_id):
        print("Failed to delete user 1")
        return False
    
    print("Deleted user 1")
    
    if not delete_user(token2, user2_id):
        print("Failed to delete user 2")
        return False
    
    print("Deleted user 2")
    
    return True

def test_cascade_delete():
    """
    Test cascade delete.
    """
    print("\n=== Testing Cascade Delete ===")
    
    # Get test users with unique emails
    test_user1 = get_test_user1()
    test_user2 = get_test_user2()
    
    # Register two test users
    user1_id = register_user(test_user1)
    if not user1_id:
        print("Failed to register test user 1")
        return False
    
    print(f"Registered test user 1 with ID: {user1_id}")
    
    user2_id = register_user(test_user2)
    if not user2_id:
        print("Failed to register test user 2")
        return False
    
    print(f"Registered test user 2 with ID: {user2_id}")
    
    # Login as test user 1
    token1 = login(test_user1['email'], test_user1['password'])
    if not token1:
        print("Failed to login as test user 1")
        return False
    
    print("Logged in as test user 1")
    
    # Login as test user 2
    token2 = login(test_user2['email'], test_user2['password'])
    if not token2:
        print("Failed to login as test user 2")
        return False
    
    print("Logged in as test user 2")
    
    # Create a place as test user 1
    place_data = dict(TEST_PLACE)
    place_id = create_place(token1, place_data)
    if not place_id:
        print("Failed to create place")
        return False
    
    print(f"Created place with ID: {place_id}")
    
    # Create a review as test user 2
    review_data = dict(TEST_REVIEW)
    review_id = create_review(token2, review_data, place_id)
    if not review_id:
        print("Failed to create review")
        return False
    
    print(f"Created review with ID: {review_id}")
    
    # Delete the place
    if not delete_place(token1, place_id):
        print("Failed to delete place")
        return False
    
    print("Deleted place")
    
    # Try to get the deleted place
    deleted_place = get_place(place_id)
    if deleted_place:
        print("Place was not deleted")
        return False
    
    print("Place was successfully deleted")
    
    # Try to get the review (should be deleted with the place)
    deleted_review = get_review(review_id)
    if deleted_review:
        print("Review was not deleted with the place")
        return False
    
    print("Review was successfully deleted with the place")
    
    # Delete the users
    if not delete_user(token1, user1_id):
        print("Failed to delete user 1")
        return False
    
    print("Deleted user 1")
    
    if not delete_user(token2, user2_id):
        print("Failed to delete user 2")
        return False
    
    print("Deleted user 2")
    
    return True

def main():
    """
    Main function.
    """
    print("=== Testing Relationships and CRUD Operations ===")
    
    # Test User-Place relationship
    if not test_user_place_relationship():
        print("User-Place relationship test failed")
        return
    
    print("User-Place relationship test passed")
    
    # Test Place-Review relationship
    if not test_place_review_relationship():
        print("Place-Review relationship test failed")
        return
    
    print("Place-Review relationship test passed")
    
    # Test cascade delete
    if not test_cascade_delete():
        print("Cascade delete test failed")
        return
    
    print("Cascade delete test passed")
    
    print("\nAll tests passed!")

if __name__ == '__main__':
    main()
