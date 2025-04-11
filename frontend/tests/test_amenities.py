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

def test_create_amenity(client):
    response = client.post('/api/v1/amenities/', json={'name': 'Wi-Fi'})
    assert response.status_code == 201
    data = json.loads(response.data)
    assert 'id' in data
    assert data['name'] == 'Wi-Fi'

def test_get_all_amenities(client):
    # Create a test amenity
    client.post('/api/v1/amenities/', json={'name': 'Pool'})
    
    response = client.get('/api/v1/amenities/')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) > 0
    assert 'id' in data[0]
    assert 'name' in data[0]

def test_get_amenity(client):
    # Create a test amenity
    create_response = client.post('/api/v1/amenities/', json={'name': 'Gym'})
    amenity_id = json.loads(create_response.data)['id']
    
    response = client.get(f'/api/v1/amenities/{amenity_id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['id'] == amenity_id
    assert data['name'] == 'Gym'

def test_update_amenity(client):
    # Create a test amenity
    create_response = client.post('/api/v1/amenities/', json={'name': 'Parking'})
    amenity_id = json.loads(create_response.data)['id']
    
    response = client.put(f'/api/v1/amenities/{amenity_id}', json={'name': 'Free Parking'})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'message' in data
    assert data['message'] == 'Amenity updated successfully'
    assert data['amenity']['name'] == 'Free Parking'

def test_create_amenity_invalid_data(client):
    response = client.post('/api/v1/amenities/', json={})
    assert response.status_code == 400

def test_update_amenity_not_found(client):
    response = client.put('/api/v1/amenities/nonexistent_id', json={'name': 'Updated Amenity'})
    assert response.status_code == 404

def test_get_amenity_not_found(client):
    response = client.get('/api/v1/amenities/nonexistent_id')
    assert response.status_code == 404
