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

def test_create_user(client):
    response = client.post('/api/v1/users/', json={
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'john.doe@example.com',
        'password': 'password123'
    })
    assert response.status_code == 201
    data = json.loads(response.data)
    assert 'id' in data
    assert data['first_name'] == 'John'
    assert data['last_name'] == 'Doe'
    assert data['email'] == 'john.doe@example.com'

def test_create_user_empty_first_name(client):
    response = client.post('/api/v1/users/', json={
        'first_name': '',
        'last_name': 'Doe',
        'email': 'john.doe@example.com',
        'password': 'password123'
    })
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data

def test_create_user_empty_last_name(client):
    response = client.post('/api/v1/users/', json={
        'first_name': 'John',
        'last_name': '',
        'email': 'john.doe@example.com',
        'password': 'password123'
    })
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data

def test_create_user_invalid_email(client):
    response = client.post('/api/v1/users/', json={
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'invalid-email',
        'password': 'password123'
    })
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data

def test_get_all_users(client):
    # Create a test user
    client.post('/api/v1/users/', json={
        'first_name': 'Jane',
        'last_name': 'Smith',
        'email': 'jane.smith@example.com',
        'password': 'password456'
    })
    
    response = client.get('/api/v1/users/')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) > 0
    assert 'id' in data[0]
    assert 'first_name' in data[0]
    assert 'last_name' in data[0]
    assert 'email' in data[0]

def test_get_user(client):
    # Create a test user
    create_response = client.post('/api/v1/users/', json={
        'first_name': 'Bob',
        'last_name': 'Johnson',
        'email': 'bob.johnson@example.com',
        'password': 'password789'
    })
    user_id = json.loads(create_response.data)['id']
    
    response = client.get(f'/api/v1/users/{user_id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['id'] == user_id
    assert data['first_name'] == 'Bob'
    assert data['last_name'] == 'Johnson'
    assert data['email'] == 'bob.johnson@example.com'

def test_update_user(client):
    # Create a test user
    create_response = client.post('/api/v1/users/', json={
        'first_name': 'Alice',
        'last_name': 'Brown',
        'email': 'alice.brown@example.com',
        'password': 'password101'
    })
    user_id = json.loads(create_response.data)['id']
    
    response = client.put(f'/api/v1/users/{user_id}', json={
        'first_name': 'Alicia',
        'email': 'alicia.brown@example.com'
    })
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['first_name'] == 'Alicia'
    assert data['email'] == 'alicia.brown@example.com'

def test_update_user_invalid_email(client):
    # Create a test user
    create_response = client.post('/api/v1/users/', json={
        'first_name': 'Charlie',
        'last_name': 'Davis',
        'email': 'charlie.davis@example.com',
        'password': 'password202'
    })
    user_id = json.loads(create_response.data)['id']
    
    response = client.put(f'/api/v1/users/{user_id}', json={
        'email': 'invalid-email'
    })
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data

def test_get_user_not_found(client):
    response = client.get('/api/v1/users/nonexistent_id')
    assert response.status_code == 404
