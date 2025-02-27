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

@pytest.fixture
def setup_test_data(client):
    # Create a test user
    user_response = client.post('/api/v1/users/', json={
        'first_name': 'Review',
        'last_name': 'Tester',
        'email': 'review.tester@example.com',
        'password': 'password123'
    })
    user_data = json.loads(user_response.data)
    
    # Create a test place
    place_response = client.post('/api/v1/places/', json={
        'title': 'Test Place',
        'description': 'A place for testing reviews',
        'price': 100.0,
        'latitude': 37.7749,
        'longitude': -122.4194,
        'owner_id': user_data['id']
    })
    place_data = json.loads(place_response.data)
    
    return {
        'user_id': user_data['id'],
        'place_id': place_data['id']
    }

def test_create_review(client, setup_test_data):
    response = client.post('/api/v1/reviews/', json={
        'text': 'Great place to stay!',
        'rating': 5,
        'user_id': setup_test_data['user_id'],
        'place_id': setup_test_data['place_id']
    })
    assert response.status_code == 201
    data = json.loads(response.data)
    assert 'id' in data
    assert data['text'] == 'Great place to stay!'
    assert data['rating'] == 5
    assert data['user_id'] == setup_test_data['user_id']
    assert data['place_id'] == setup_test_data['place_id']

def test_create_review_empty_text(client, setup_test_data):
    response = client.post('/api/v1/reviews/', json={
        'text': '',
        'rating': 4,
        'user_id': setup_test_data['user_id'],
        'place_id': setup_test_data['place_id']
    })
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data

def test_create_review_invalid_rating_low(client, setup_test_data):
    response = client.post('/api/v1/reviews/', json={
        'text': 'Bad rating test',
        'rating': 0,  # Invalid: below minimum
        'user_id': setup_test_data['user_id'],
        'place_id': setup_test_data['place_id']
    })
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data

def test_create_review_invalid_rating_high(client, setup_test_data):
    response = client.post('/api/v1/reviews/', json={
        'text': 'Bad rating test',
        'rating': 6,  # Invalid: above maximum
        'user_id': setup_test_data['user_id'],
        'place_id': setup_test_data['place_id']
    })
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data

def test_create_review_invalid_user_id(client, setup_test_data):
    response = client.post('/api/v1/reviews/', json={
        'text': 'Invalid user test',
        'rating': 3,
        'user_id': 'nonexistent_user_id',
        'place_id': setup_test_data['place_id']
    })
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data

def test_create_review_invalid_place_id(client, setup_test_data):
    response = client.post('/api/v1/reviews/', json={
        'text': 'Invalid place test',
        'rating': 3,
        'user_id': setup_test_data['user_id'],
        'place_id': 'nonexistent_place_id'
    })
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data

def test_get_all_reviews(client, setup_test_data):
    # Create a test review
    client.post('/api/v1/reviews/', json={
        'text': 'Review for get all test',
        'rating': 4,
        'user_id': setup_test_data['user_id'],
        'place_id': setup_test_data['place_id']
    })
    
    response = client.get('/api/v1/reviews/')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) > 0
    assert 'id' in data[0]
    assert 'text' in data[0]
    assert 'rating' in data[0]

def test_get_review(client, setup_test_data):
    # Create a test review
    create_response = client.post('/api/v1/reviews/', json={
        'text': 'Review for get test',
        'rating': 5,
        'user_id': setup_test_data['user_id'],
        'place_id': setup_test_data['place_id']
    })
    review_id = json.loads(create_response.data)['id']
    
    response = client.get(f'/api/v1/reviews/{review_id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['id'] == review_id
    assert data['text'] == 'Review for get test'
    assert data['rating'] == 5
    assert 'user' in data
    assert 'place' in data

def test_update_review(client, setup_test_data):
    # Create a test review
    create_response = client.post('/api/v1/reviews/', json={
        'text': 'Original review text',
        'rating': 3,
        'user_id': setup_test_data['user_id'],
        'place_id': setup_test_data['place_id']
    })
    review_id = json.loads(create_response.data)['id']
    
    response = client.put(f'/api/v1/reviews/{review_id}', json={
        'text': 'Updated review text',
        'rating': 4
    })
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'message' in data
    assert data['message'] == 'Review updated successfully'
    assert data['review']['text'] == 'Updated review text'
    assert data['review']['rating'] == 4

def test_update_review_invalid_rating(client, setup_test_data):
    # Create a test review
    create_response = client.post('/api/v1/reviews/', json={
        'text': 'Review for invalid update test',
        'rating': 3,
        'user_id': setup_test_data['user_id'],
        'place_id': setup_test_data['place_id']
    })
    review_id = json.loads(create_response.data)['id']
    
    response = client.put(f'/api/v1/reviews/{review_id}', json={
        'rating': 10  # Invalid: above maximum
    })
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data

def test_delete_review(client, setup_test_data):
    # Create a test review
    create_response = client.post('/api/v1/reviews/', json={
        'text': 'Review to be deleted',
        'rating': 2,
        'user_id': setup_test_data['user_id'],
        'place_id': setup_test_data['place_id']
    })
    review_id = json.loads(create_response.data)['id']
    
    response = client.delete(f'/api/v1/reviews/{review_id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'message' in data
    assert data['message'] == 'Review deleted successfully'
    
    # Verify the review is gone
    get_response = client.get(f'/api/v1/reviews/{review_id}')
    assert get_response.status_code == 404

def test_get_review_not_found(client):
    response = client.get('/api/v1/reviews/nonexistent_id')
    assert response.status_code == 404

def test_update_review_not_found(client):
    response = client.put('/api/v1/reviews/nonexistent_id', json={
        'text': 'Updated text for nonexistent review'
    })
    assert response.status_code == 404

def test_delete_review_not_found(client):
    response = client.delete('/api/v1/reviews/nonexistent_id')
    assert response.status_code == 404
