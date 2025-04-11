"""
This script demonstrates how to use the one-to-many and many-to-many relationships
in the HBNB application.
"""

import sys
import os

# Add the parent directory to the path so we can import app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity
from app.extensions import db
from app import create_app

# Create and configure the app
app = create_app('config.DevelopmentConfig')

# Push an application context to work with the database
with app.app_context():
    # Create some users
    alice = User(first_name="Alice", last_name="Smith", email="alice@example.com")
    alice.hash_password("password123")
    
    bob = User(first_name="Bob", last_name="Johnson", email="bob@example.com")
    bob.hash_password("password456")
    
    # Save users to get IDs
    db.session.add_all([alice, bob])
    db.session.commit()
    
    # Create some places (one-to-many relationship with User)
    apartment = Place(
        title="Cozy Apartment", 
        description="A nice place to stay in the city center", 
        price=100, 
        latitude=37.7749, 
        longitude=-122.4194, 
        owner_id=alice.id
    )
    
    house = Place(
        title="Spacious House", 
        description="A beautiful house with a garden", 
        price=200, 
        latitude=34.0522, 
        longitude=-118.2437, 
        owner_id=alice.id
    )
    
    # Save places to get IDs
    db.session.add_all([apartment, house])
    db.session.commit()
    
    # Create some amenities
    wifi = Amenity(name="Wi-Fi")
    pool = Amenity(name="Swimming Pool")
    kitchen = Amenity(name="Fully Equipped Kitchen")
    
    # Save amenities to get IDs
    db.session.add_all([wifi, pool, kitchen])
    db.session.commit()
    
    # Add amenities to places (many-to-many relationship)
    apartment.amenities.append(wifi)
    apartment.amenities.append(kitchen)
    
    house.amenities.append(wifi)
    house.amenities.append(pool)
    house.amenities.append(kitchen)
    
    # Create some reviews (one-to-many relationship with User and Place)
    review1 = Review(
        text="Great apartment, very clean and comfortable!", 
        rating=5, 
        place=apartment, 
        user=bob
    )
    
    review2 = Review(
        text="Nice house, but a bit far from the city center.", 
        rating=4, 
        place=house, 
        user=bob
    )
    
    # Save reviews
    db.session.add_all([review1, review2])
    db.session.commit()
    
    # Demonstrate querying the relationships
    print("\n=== One-to-Many: User to Places ===")
    print(f"User: {alice.first_name} {alice.last_name}")
    print("Places owned:")
    # Using the relationship directly
    for place in alice.places:
        print(f"- {place.title} (${place.price}/night)")
    
    print("\n=== One-to-Many: Place to Reviews ===")
    print(f"Place: {apartment.title}")
    print("Reviews:")
    # Using the relationship directly
    for review in apartment.reviews:
        print(f"- {review.rating}/5 stars: \"{review.text}\" by {review.user.first_name}")
    
    print("\n=== One-to-Many: User to Reviews ===")
    print(f"User: {bob.first_name} {bob.last_name}")
    print("Reviews written:")
    # Using the relationship directly
    for review in bob.reviews:
        print(f"- {review.rating}/5 stars for {review.place.title}: \"{review.text}\"")
    
    print("\n=== Many-to-Many: Place to Amenities ===")
    print(f"Place: {house.title}")
    print("Amenities:")
    for amenity in house.amenities:
        print(f"- {amenity.name}")
    
    print("\n=== Many-to-Many: Amenity to Places ===")
    print(f"Amenity: {wifi.name}")
    print("Places with this amenity:")
    for place in wifi.places:
        print(f"- {place.title}")
    
    # Demonstrate bidirectional navigation
    print("\n=== Bidirectional Navigation ===")
    # Start with a review
    review = Review.query.first()
    print(f"Review: {review.rating}/5 stars: \"{review.text}\"")
    # Navigate to the place
    place = review.place
    print(f"Place: {place.title}")
    # Navigate to the owner
    owner = place.owner
    print(f"Owner: {owner.first_name} {owner.last_name}")
    # Navigate to other places owned by this user
    print("Other places by this owner:")
    for other_place in owner.places:
        if other_place.id != place.id:
            print(f"- {other_place.title}")
    
    # Clean up (optional - remove if you want to keep the data)
    db.session.delete(review1)
    db.session.delete(review2)
    db.session.delete(apartment)
    db.session.delete(house)
    db.session.delete(wifi)
    db.session.delete(pool)
    db.session.delete(kitchen)
    db.session.delete(alice)
    db.session.delete(bob)
    db.session.commit()
    print("\nExample data cleaned up.")

print("\nScript completed successfully!")
