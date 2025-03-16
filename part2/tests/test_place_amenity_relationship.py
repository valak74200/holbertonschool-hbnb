#!/usr/bin/env python3
"""
Script to test the many-to-many relationship between Place and Amenity.
"""

import requests
import json
import sys
import os
import uuid

# Base URL for the API
BASE_URL = 'http://127.0.0.1:5000/api/v1'

# Generate unique email addresses for each test run
def get_test_user():
    unique_id = str(uuid.uuid4())[:8]
    return {
        'first_name': 'Test',
        'last_name': 'User',
        'email': f'test_{unique_id}@example.com',
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

# Generate unique amenity names for each test run
def get_test_amenities():
    unique_id = str(uuid.uuid4())[:8]
    return [
        {'name': f'WiFi_{unique_id}'},
        {'name': f'Pool_{unique_id}'},
        {'name': f'Gym_{unique_id}'},
        {'name': f'Parking_{unique_id}'}
    ]

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

def get_amenity(amenity_id):
    """
    Get an amenity by ID.
    
    Args:
        amenity_id: The amenity ID
        
    Returns:
        The amenity data
    """
    response = requests.get(f'{BASE_URL}/amenities/{amenity_id}')
    
    if response.status_code != 200:
        print(f'Error getting amenity: {response.text}')
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

def delete_amenity(token, amenity_id):
    """
    Delete an amenity.
    
    Args:
        token: The access token
        amenity_id: The amenity ID
        
    Returns:
        True if successful, False otherwise
    """
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.delete(f'{BASE_URL}/amenities/{amenity_id}', headers=headers)
    
    if response.status_code != 200:
        print(f'Error deleting amenity: {response.text}')
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

def test_place_amenity_relationship():
    """
    Test the Place-Amenity relationship.
    """
    print("\n=== Testing Place-Amenity Relationship ===")
    
    # Get a test user with a unique email
    test_user = get_test_user()
    
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
    
    # Create amenities
    test_amenities = get_test_amenities()
    amenity_ids = []
    for amenity_data in test_amenities:
        amenity_id = create_amenity(token, amenity_data)
        if not amenity_id:
            print(f"Failed to create amenity: {amenity_data['name']}")
            return False
        amenity_ids.append(amenity_id)
        print(f"Created amenity with ID: {amenity_id}")
    
    # Create a place
    place_data = dict(TEST_PLACE)
    place_data['amenities'] = amenity_ids
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
    
    # Verify the place amenities
    if 'amenities' not in place:
        print("Place does not have amenities field")
        return False
    
    if len(place['amenities']) != len(amenity_ids):
        print(f"Place amenities count ({len(place['amenities'])}) does not match expected count ({len(amenity_ids)})")
        return False
    
    place_amenity_ids = [amenity['id'] for amenity in place['amenities']]
    for amenity_id in amenity_ids:
        if amenity_id not in place_amenity_ids:
            print(f"Amenity ID {amenity_id} not found in place amenities")
            return False
    
    print("Place amenities match expected amenities")
    
    # Update the place to remove some amenities
    update_data = {'amenities': amenity_ids[:2]}  # Keep only the first two amenities
    if not update_place(token, place_id, update_data):
        print("Failed to update place")
        return False
    
    print("Updated place")
    
    # Get the updated place
    updated_place = get_place(place_id)
    if not updated_place:
        print("Failed to get updated place")
        return False
    
    # Verify the updated place amenities
    if 'amenities' not in updated_place:
        print("Updated place does not have amenities field")
        return False
    
    if len(updated_place['amenities']) != len(update_data['amenities']):
        print(f"Updated place amenities count ({len(updated_place['amenities'])}) does not match expected count ({len(update_data['amenities'])})")
        return False
    
    updated_place_amenity_ids = [amenity['id'] for amenity in updated_place['amenities']]
    for amenity_id in update_data['amenities']:
        if amenity_id not in updated_place_amenity_ids:
            print(f"Amenity ID {amenity_id} not found in updated place amenities")
            return False
    
    print("Updated place amenities match expected amenities")
    
    # Delete the place
    if not delete_place(token, place_id):
        print("Failed to delete place")
        return False
    
    print("Deleted place")
    
    # Delete the amenities
    for amenity_id in amenity_ids:
        if not delete_amenity(token, amenity_id):
            print(f"Failed to delete amenity with ID: {amenity_id}")
            return False
        print(f"Deleted amenity with ID: {amenity_id}")
    
    # Delete the user
    if not delete_user(token, user_id):
        print("Failed to delete user")
        return False
    
    print("Deleted user")
    
    return True

def main():
    """
    Main function.
    """
    print("=== Testing Place-Amenity Relationship ===")
    
    # Test Place-Amenity relationship
    if not test_place_amenity_relationship():
        print("Place-Amenity relationship test failed")
        return
    
    print("Place-Amenity relationship test passed")
    
    print("\nAll tests passed!")

if __name__ == '__main__':
    main()
