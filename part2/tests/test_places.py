import pytest
import sys
import os
from flask import json

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.services.facade import facade

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_create_place(client):
    # First, create a user to be the owner
    user_data = {
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'john@example.com',
        'password': 'password123'
    }
    print("Sending user data:", user_data)  # Debug print
    user_response = client.post('/api/v1/users/', json=user_data)
    print("User response status:", user_response.status_code)  # Debug print
    print("User response data:", user_response.data)  # Debug print
    user_data = json.loads(user_response.data)
    print("Parsed user data:", user_data)  # Debug print
    
    response = client.post('/api/v1/places/', json={
        'title': 'Cozy Apartment',
        'description': 'A nice place to stay',
        'price': 100.0,
        'latitude': 37.7749,
        'longitude': -122.4194,
        'owner_id': user_data['id']
    })
    assert response.status_code == 201
    data = json.loads(response.data)
    assert 'id' in data
    assert data['title'] == 'Cozy Apartment'
    assert data['price'] == 100.0

def test_get_all_places(client):
    response = client.get('/api/v1/places/')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) > 0
    assert 'id' in data[0]
    assert 'title' in data[0]

def test_get_place(client):
    # First, create a place
    user_response = client.post('/api/v1/users/', json={
        'first_name': 'Jane',
        'last_name': 'Doe',
        'email': 'jane@example.com',
        'password': 'password456'
    })
    user_data = json.loads(user_response.data)
    print("User data:", user_data)  # Debug print
    
    create_response = client.post('/api/v1/places/', json={
        'title': 'Luxury Villa',
        'description': 'An amazing place to stay',
        'price': 500.0,
        'latitude': 34.0522,
        'longitude': -118.2437,
        'owner_id': user_data['id']
    })
    place_data = json.loads(create_response.data)
    
    response = client.get(f'/api/v1/places/{place_data["id"]}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['id'] == place_data['id']
    assert data['title'] == 'Luxury Villa'
    assert 'owner' in data
    assert data['owner']['first_name'] == 'Jane'

def test_update_place(client):
    # First, create a place
    user_response = client.post('/api/v1/users/', json={
        'first_name': 'Bob',
        'last_name': 'Smith',
        'email': 'bob@example.com',
        'password': 'password789'
    })
    user_data = json.loads(user_response.data)
    print("User data:", user_data)  # Debug print
    
    create_response = client.post('/api/v1/places/', json={
        'title': 'Beach House',
        'description': 'Relax by the sea',
        'price': 300.0,
        'latitude': 25.7617,
        'longitude': -80.1918,
        'owner_id': user_data['id']
    })
    place_data = json.loads(create_response.data)
    
    response = client.put(f'/api/v1/places/{place_data["id"]}', json={
        'title': 'Luxury Beach House',
        'price': 350.0
    })
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'message' in data
    assert data['message'] == 'Place updated successfully'
    assert data['place']['title'] == 'Luxury Beach House'
    assert data['place']['price'] == 350.0

def test_create_place_invalid_data(client):
    response = client.post('/api/v1/places/', json={
        'title': 'Invalid Place',
        'price': -100.0,  # Invalid price
        'latitude': 1000.0,  # Invalid latitude
        'longitude': -200.0,  # Invalid longitude
        'owner_id': 'non_existent_id'
    })
    assert response.status_code == 400

def test_update_place_not_found(client):
    response = client.put('/api/v1/places/nonexistent_id', json={
        'title': 'Updated Place'
    })
    assert response.status_code == 404

def test_get_place_not_found(client):
    response = client.get('/api/v1/places/nonexistent_id')
    assert response.status_code == 404
