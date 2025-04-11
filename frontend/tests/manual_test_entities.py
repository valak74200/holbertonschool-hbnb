#!/usr/bin/env python3
"""
Manual test script for entity mappings
"""
import sys
from app import create_app
from app.extensions import db
from app.models import User, Amenity, Place, Review
from app.services.facade import facade

def main():
    """
    Test the entity mappings by creating and retrieving entities
    """
    # Redirect stdout to a file
    original_stdout = sys.stdout
    with open('entity_test_output.txt', 'w') as f:
        sys.stdout = f
        
        # Create the Flask app and push the application context
        app = create_app('config.DevelopmentConfig')
        with app.app_context():
            # Clear the database
            db.drop_all()
            db.create_all()
            
            print("Testing entity mappings...")
            
            # Create a user
            print("\nCreating user...")
            user_data = {
                'first_name': 'John',
                'last_name': 'Doe',
                'email': 'john.doe.test@example.com',
                'password': 'password123'
            }
            user = facade.create_user(user_data)
            print(f"User created: {user.first_name} {user.last_name} ({user.email})")
            
            # Create a second user for reviews
            print("\nCreating second user...")
            user2_data = {
                'first_name': 'Jane',
                'last_name': 'Smith',
                'email': 'jane.smith.test@example.com',
                'password': 'password456'
            }
            user2 = facade.create_user(user2_data)
            print(f"Second user created: {user2.first_name} {user2.last_name} ({user2.email})")
            
            # Create an amenity
            print("\nCreating amenity...")
            amenity_data = {
                'name': 'WiFi'
            }
            amenity = facade.create_amenity(amenity_data)
            print(f"Amenity created: {amenity.name}")
            
            # Create a place
            print("\nCreating place...")
            place_data = {
                'title': 'Cozy Apartment',
                'description': 'A beautiful apartment in the heart of the city',
                'price': 100.0,
                'latitude': 48.8566,
                'longitude': 2.3522,
                'owner_id': user.id
            }
            place = facade.create_place(place_data)
            print(f"Place created: {place.title} (Owner: {place.owner_id})")
            
            # Create a review
            print("\nCreating review...")
            review_data = {
                'text': 'Great place to stay!',
                'rating': 5,
                'user_id': user2.id,
                'place_id': place.id
            }
            review = facade.create_review(review_data)
            print(f"Review created: Rating: {review.rating}, Text: {review.text}")
            
            # Retrieve all entities
            print("\nRetrieving all entities...")
            users = facade.get_all_users()
            amenities = facade.get_all_amenities()
            places = facade.get_all_places()
            reviews = facade.get_all_reviews()
            
            print(f"Users: {len(users)}")
            for user in users:
                print(f"  - {user.first_name} {user.last_name} ({user.email})")
            
            print(f"Amenities: {len(amenities)}")
            for amenity in amenities:
                print(f"  - {amenity.name}")
            
            print(f"Places: {len(places)}")
            for place in places:
                print(f"  - {place.title} (Owner: {place.owner_id})")
            
            print(f"Reviews: {len(reviews)}")
            for review in reviews:
                print(f"  - Rating: {review.rating}, Text: {review.text}")
            
            print("\nEntity mapping test completed successfully!")
    
    # Restore stdout
    sys.stdout = original_stdout
    print("Test completed. Results written to entity_test_output.txt")

if __name__ == "__main__":
    main()
