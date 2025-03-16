#!/usr/bin/env python3
"""
Script to test the database by performing CRUD operations on each table.
"""

import sqlite3
import os
import sys
import uuid
import bcrypt

# Add the parent directory to the path so we can import app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def generate_uuid():
    """Generate a UUID."""
    return str(uuid.uuid4())

def generate_bcrypt_hash(password):
    """Generate a bcrypt hash for a password."""
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

def test_users_table(conn):
    """Test CRUD operations on the users table."""
    print("\n=== Testing Users Table ===")
    
    # SELECT: Verify the admin user
    print("\n1. Verifying admin user...")
    admin = conn.execute('''
        SELECT id, first_name, last_name, email, password, is_admin
        FROM users
        WHERE id = '36c9050e-ddd3-4c3b-9731-9f487208bbc1'
    ''').fetchone()
    
    if admin:
        print(f"Admin user found: {admin[1]} {admin[2]} ({admin[3]})")
        print(f"Password is hashed: {admin[4][:20]}...")
        print(f"Is admin: {admin[5]}")
    else:
        print("Admin user not found!")
    
    # INSERT: Add a new user
    print("\n2. Adding a new user...")
    new_user_id = generate_uuid()
    new_user_password = generate_bcrypt_hash("password123")
    
    try:
        conn.execute('''
            INSERT INTO users (id, first_name, last_name, email, password, role, is_admin)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (new_user_id, 'John', 'Doe', 'john@example.com', new_user_password, 'user', False))
        conn.commit()
        print(f"New user added with ID: {new_user_id}")
    except sqlite3.Error as e:
        print(f"Error adding new user: {e}")
    
    # UPDATE: Modify the user
    print("\n3. Updating the user...")
    try:
        conn.execute('''
            UPDATE users
            SET first_name = ?, last_name = ?
            WHERE id = ?
        ''', ('Johnny', 'Smith', new_user_id))
        conn.commit()
        print(f"User updated with ID: {new_user_id}")
    except sqlite3.Error as e:
        print(f"Error updating user: {e}")
    
    # SELECT: Verify the update
    updated_user = conn.execute('''
        SELECT id, first_name, last_name, email
        FROM users
        WHERE id = ?
    ''', (new_user_id,)).fetchone()
    
    if updated_user:
        print(f"Updated user: {updated_user[1]} {updated_user[2]} ({updated_user[3]})")
    else:
        print("Updated user not found!")
    
    # DELETE: Remove the user
    print("\n4. Deleting the user...")
    try:
        conn.execute('''
            DELETE FROM users
            WHERE id = ?
        ''', (new_user_id,))
        conn.commit()
        print(f"User deleted with ID: {new_user_id}")
    except sqlite3.Error as e:
        print(f"Error deleting user: {e}")
    
    # SELECT: Verify the deletion
    deleted_user = conn.execute('''
        SELECT id FROM users WHERE id = ?
    ''', (new_user_id,)).fetchone()
    
    if deleted_user:
        print(f"User still exists with ID: {deleted_user[0]}")
    else:
        print("User successfully deleted")
    
    # Test unique constraint on email
    print("\n5. Testing unique constraint on email...")
    try:
        conn.execute('''
            INSERT INTO users (id, first_name, last_name, email, password, role, is_admin)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (generate_uuid(), 'Duplicate', 'Email', 'admin@hbnb.io', generate_bcrypt_hash("password"), 'user', False))
        conn.commit()
        print("Unique constraint failed: Duplicate email was inserted!")
    except sqlite3.Error as e:
        print(f"Unique constraint working: {e}")

def test_amenities_table(conn):
    """Test CRUD operations on the amenities table."""
    print("\n=== Testing Amenities Table ===")
    
    # SELECT: Verify the initial amenities
    print("\n1. Verifying initial amenities...")
    amenities = conn.execute('''
        SELECT id, name
        FROM amenities
    ''').fetchall()
    
    print(f"Found {len(amenities)} amenities:")
    for amenity in amenities:
        print(f"- {amenity[1]} (ID: {amenity[0]})")
    
    # INSERT: Add a new amenity
    print("\n2. Adding a new amenity...")
    new_amenity_id = generate_uuid()
    
    try:
        conn.execute('''
            INSERT INTO amenities (id, name)
            VALUES (?, ?)
        ''', (new_amenity_id, 'Gym'))
        conn.commit()
        print(f"New amenity added with ID: {new_amenity_id}")
    except sqlite3.Error as e:
        print(f"Error adding new amenity: {e}")
    
    # UPDATE: Modify the amenity
    print("\n3. Updating the amenity...")
    try:
        conn.execute('''
            UPDATE amenities
            SET name = ?
            WHERE id = ?
        ''', ('Fitness Center', new_amenity_id))
        conn.commit()
        print(f"Amenity updated with ID: {new_amenity_id}")
    except sqlite3.Error as e:
        print(f"Error updating amenity: {e}")
    
    # SELECT: Verify the update
    updated_amenity = conn.execute('''
        SELECT id, name
        FROM amenities
        WHERE id = ?
    ''', (new_amenity_id,)).fetchone()
    
    if updated_amenity:
        print(f"Updated amenity: {updated_amenity[1]} (ID: {updated_amenity[0]})")
    else:
        print("Updated amenity not found!")
    
    # DELETE: Remove the amenity
    print("\n4. Deleting the amenity...")
    try:
        conn.execute('''
            DELETE FROM amenities
            WHERE id = ?
        ''', (new_amenity_id,))
        conn.commit()
        print(f"Amenity deleted with ID: {new_amenity_id}")
    except sqlite3.Error as e:
        print(f"Error deleting amenity: {e}")
    
    # SELECT: Verify the deletion
    deleted_amenity = conn.execute('''
        SELECT id FROM amenities WHERE id = ?
    ''', (new_amenity_id,)).fetchone()
    
    if deleted_amenity:
        print(f"Amenity still exists with ID: {deleted_amenity[0]}")
    else:
        print("Amenity successfully deleted")
    
    # Test unique constraint on name
    print("\n5. Testing unique constraint on name...")
    try:
        conn.execute('''
            INSERT INTO amenities (id, name)
            VALUES (?, ?)
        ''', (generate_uuid(), 'WiFi'))
        conn.commit()
        print("Unique constraint failed: Duplicate name was inserted!")
    except sqlite3.Error as e:
        print(f"Unique constraint working: {e}")

def test_places_table(conn):
    """Test CRUD operations on the places table."""
    print("\n=== Testing Places Table ===")
    
    # Get the admin user ID
    admin_id = conn.execute('''
        SELECT id FROM users WHERE email = 'admin@hbnb.io'
    ''').fetchone()[0]
    
    # INSERT: Add a new place
    print("\n1. Adding a new place...")
    new_place_id = generate_uuid()
    
    try:
        conn.execute('''
            INSERT INTO places (id, title, description, price, latitude, longitude, owner_id, user_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (new_place_id, 'Luxury Apartment', 'A beautiful apartment in the city center', 150.00, 40.7128, -74.0060, admin_id, admin_id))
        conn.commit()
        print(f"New place added with ID: {new_place_id}")
    except sqlite3.Error as e:
        print(f"Error adding new place: {e}")
    
    # SELECT: Verify the place
    place = conn.execute('''
        SELECT id, title, description, price, latitude, longitude, owner_id, user_id
        FROM places
        WHERE id = ?
    ''', (new_place_id,)).fetchone()
    
    if place:
        print(f"Place found: {place[1]} (${place[3]}/night)")
        print(f"Description: {place[2]}")
        print(f"Location: {place[4]}, {place[5]}")
        print(f"Owner ID: {place[6]}")
        print(f"User ID: {place[7]}")
    else:
        print("Place not found!")
    
    # UPDATE: Modify the place
    print("\n2. Updating the place...")
    try:
        conn.execute('''
            UPDATE places
            SET title = ?, price = ?
            WHERE id = ?
        ''', ('Luxury Penthouse', 200.00, new_place_id))
        conn.commit()
        print(f"Place updated with ID: {new_place_id}")
    except sqlite3.Error as e:
        print(f"Error updating place: {e}")
    
    # SELECT: Verify the update
    updated_place = conn.execute('''
        SELECT id, title, price
        FROM places
        WHERE id = ?
    ''', (new_place_id,)).fetchone()
    
    if updated_place:
        print(f"Updated place: {updated_place[1]} (${updated_place[2]}/night)")
    else:
        print("Updated place not found!")
    
    # Test foreign key constraint
    print("\n3. Testing foreign key constraint...")
    try:
        conn.execute('''
            INSERT INTO places (id, title, description, price, latitude, longitude, owner_id, user_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (generate_uuid(), 'Invalid Place', 'A place with an invalid owner', 100.00, 40.7128, -74.0060, 'invalid-id', admin_id))
        conn.commit()
        print("Foreign key constraint failed: Place with invalid owner was inserted!")
    except sqlite3.Error as e:
        print(f"Foreign key constraint working: {e}")
    
    return new_place_id

def test_reviews_table(conn, place_id):
    """Test CRUD operations on the reviews table."""
    print("\n=== Testing Reviews Table ===")
    
    # Get the admin user ID
    admin_id = conn.execute('''
        SELECT id FROM users WHERE email = 'admin@hbnb.io'
    ''').fetchone()[0]
    
    # INSERT: Add a new review
    print("\n1. Adding a new review...")
    new_review_id = generate_uuid()
    
    try:
        conn.execute('''
            INSERT INTO reviews (id, text, rating, user_id, place_id)
            VALUES (?, ?, ?, ?, ?)
        ''', (new_review_id, 'Great place to stay!', 5, admin_id, place_id))
        conn.commit()
        print(f"New review added with ID: {new_review_id}")
    except sqlite3.Error as e:
        print(f"Error adding new review: {e}")
    
    # SELECT: Verify the review
    review = conn.execute('''
        SELECT id, text, rating, user_id, place_id
        FROM reviews
        WHERE id = ?
    ''', (new_review_id,)).fetchone()
    
    if review:
        print(f"Review found: {review[1]}")
        print(f"Rating: {review[2]}/5")
        print(f"User ID: {review[3]}")
        print(f"Place ID: {review[4]}")
    else:
        print("Review not found!")
    
    # UPDATE: Modify the review
    print("\n2. Updating the review...")
    try:
        conn.execute('''
            UPDATE reviews
            SET text = ?, rating = ?
            WHERE id = ?
        ''', ('Amazing place, would definitely stay again!', 4, new_review_id))
        conn.commit()
        print(f"Review updated with ID: {new_review_id}")
    except sqlite3.Error as e:
        print(f"Error updating review: {e}")
    
    # SELECT: Verify the update
    updated_review = conn.execute('''
        SELECT id, text, rating
        FROM reviews
        WHERE id = ?
    ''', (new_review_id,)).fetchone()
    
    if updated_review:
        print(f"Updated review: {updated_review[1]}")
        print(f"Updated rating: {updated_review[2]}/5")
    else:
        print("Updated review not found!")
    
    # Test unique constraint on user_id and place_id
    print("\n3. Testing unique constraint on user_id and place_id...")
    try:
        conn.execute('''
            INSERT INTO reviews (id, text, rating, user_id, place_id)
            VALUES (?, ?, ?, ?, ?)
        ''', (generate_uuid(), 'Duplicate review', 3, admin_id, place_id))
        conn.commit()
        print("Unique constraint failed: Duplicate review was inserted!")
    except sqlite3.Error as e:
        print(f"Unique constraint working: {e}")
    
    # DELETE: Remove the review
    print("\n4. Deleting the review...")
    try:
        conn.execute('''
            DELETE FROM reviews
            WHERE id = ?
        ''', (new_review_id,))
        conn.commit()
        print(f"Review deleted with ID: {new_review_id}")
    except sqlite3.Error as e:
        print(f"Error deleting review: {e}")
    
    # SELECT: Verify the deletion
    deleted_review = conn.execute('''
        SELECT id FROM reviews WHERE id = ?
    ''', (new_review_id,)).fetchone()
    
    if deleted_review:
        print(f"Review still exists with ID: {deleted_review[0]}")
    else:
        print("Review successfully deleted")

def test_place_amenity_table(conn, place_id):
    """Test CRUD operations on the place_amenity table."""
    print("\n=== Testing Place_Amenity Table ===")
    
    # Get an amenity ID
    amenity_id = conn.execute('''
        SELECT id FROM amenities LIMIT 1
    ''').fetchone()[0]
    
    # INSERT: Add a new place-amenity relationship
    print("\n1. Adding a new place-amenity relationship...")
    try:
        conn.execute('''
            INSERT INTO place_amenity (place_id, amenity_id)
            VALUES (?, ?)
        ''', (place_id, amenity_id))
        conn.commit()
        print(f"New place-amenity relationship added: Place {place_id} - Amenity {amenity_id}")
    except sqlite3.Error as e:
        print(f"Error adding new place-amenity relationship: {e}")
    
    # SELECT: Verify the relationship
    relationship = conn.execute('''
        SELECT p.title, a.name
        FROM place_amenity pa
        JOIN places p ON pa.place_id = p.id
        JOIN amenities a ON pa.amenity_id = a.id
        WHERE pa.place_id = ? AND pa.amenity_id = ?
    ''', (place_id, amenity_id)).fetchone()
    
    if relationship:
        print(f"Relationship found: Place '{relationship[0]}' has amenity '{relationship[1]}'")
    else:
        print("Relationship not found!")
    
    # Test primary key constraint
    print("\n2. Testing primary key constraint...")
    try:
        conn.execute('''
            INSERT INTO place_amenity (place_id, amenity_id)
            VALUES (?, ?)
        ''', (place_id, amenity_id))
        conn.commit()
        print("Primary key constraint failed: Duplicate relationship was inserted!")
    except sqlite3.Error as e:
        print(f"Primary key constraint working: {e}")
    
    # DELETE: Remove the relationship
    print("\n3. Deleting the relationship...")
    try:
        conn.execute('''
            DELETE FROM place_amenity
            WHERE place_id = ? AND amenity_id = ?
        ''', (place_id, amenity_id))
        conn.commit()
        print(f"Relationship deleted: Place {place_id} - Amenity {amenity_id}")
    except sqlite3.Error as e:
        print(f"Error deleting relationship: {e}")
    
    # SELECT: Verify the deletion
    deleted_relationship = conn.execute('''
        SELECT * FROM place_amenity
        WHERE place_id = ? AND amenity_id = ?
    ''', (place_id, amenity_id)).fetchone()
    
    if deleted_relationship:
        print(f"Relationship still exists")
    else:
        print("Relationship successfully deleted")

def test_relationships(conn):
    """Test the relationships between tables."""
    print("\n=== Testing Relationships ===")
    
    # Get the admin user ID
    admin_id = conn.execute('''
        SELECT id FROM users WHERE email = 'admin@hbnb.io'
    ''').fetchone()[0]
    
    # Create a place
    place_id = generate_uuid()
    conn.execute('''
        INSERT INTO places (id, title, description, price, latitude, longitude, owner_id, user_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (place_id, 'Test Place', 'A place for testing relationships', 100.00, 40.7128, -74.0060, admin_id, admin_id))
    
    # Create a review for the place
    review_id = generate_uuid()
    conn.execute('''
        INSERT INTO reviews (id, text, rating, user_id, place_id)
        VALUES (?, ?, ?, ?, ?)
    ''', (review_id, 'Test review', 4, admin_id, place_id))
    
    # Add amenities to the place
    amenity_ids = conn.execute('''
        SELECT id FROM amenities LIMIT 2
    ''').fetchall()
    
    for amenity_id in amenity_ids:
        conn.execute('''
            INSERT INTO place_amenity (place_id, amenity_id)
            VALUES (?, ?)
        ''', (place_id, amenity_id[0]))
    
    conn.commit()
    
    # Test User-Place relationship
    print("\n1. Testing User-Place relationship...")
    user_places = conn.execute('''
        SELECT p.id, p.title
        FROM places p
        WHERE p.owner_id = ?
    ''', (admin_id,)).fetchall()
    
    print(f"User {admin_id} owns {len(user_places)} places:")
    for place in user_places:
        print(f"- {place[1]} (ID: {place[0]})")
    
    # Test Place-Review relationship
    print("\n2. Testing Place-Review relationship...")
    place_reviews = conn.execute('''
        SELECT r.id, r.text, r.rating
        FROM reviews r
        WHERE r.place_id = ?
    ''', (place_id,)).fetchall()
    
    print(f"Place {place_id} has {len(place_reviews)} reviews:")
    for review in place_reviews:
        print(f"- {review[1]} (Rating: {review[2]}/5)")
    
    # Test User-Review relationship
    print("\n3. Testing User-Review relationship...")
    user_reviews = conn.execute('''
        SELECT r.id, r.text, p.title
        FROM reviews r
        JOIN places p ON r.place_id = p.id
        WHERE r.user_id = ?
    ''', (admin_id,)).fetchall()
    
    print(f"User {admin_id} has written {len(user_reviews)} reviews:")
    for review in user_reviews:
        print(f"- Review for '{review[2]}': {review[1]}")
    
    # Test Place-Amenity relationship
    print("\n4. Testing Place-Amenity relationship...")
    place_amenities = conn.execute('''
        SELECT a.id, a.name
        FROM amenities a
        JOIN place_amenity pa ON a.id = pa.amenity_id
        WHERE pa.place_id = ?
    ''', (place_id,)).fetchall()
    
    print(f"Place {place_id} has {len(place_amenities)} amenities:")
    for amenity in place_amenities:
        print(f"- {amenity[1]} (ID: {amenity[0]})")
    
    # Test Amenity-Place relationship
    print("\n5. Testing Amenity-Place relationship...")
    amenity_id = amenity_ids[0][0]
    amenity_places = conn.execute('''
        SELECT p.id, p.title
        FROM places p
        JOIN place_amenity pa ON p.id = pa.place_id
        WHERE pa.amenity_id = ?
    ''', (amenity_id,)).fetchall()
    
    print(f"Amenity {amenity_id} is available in {len(amenity_places)} places:")
    for place in amenity_places:
        print(f"- {place[1]} (ID: {place[0]})")
    
    # Clean up
    conn.execute('''DELETE FROM place_amenity WHERE place_id = ?''', (place_id,))
    conn.execute('''DELETE FROM reviews WHERE place_id = ?''', (place_id,))
    conn.execute('''DELETE FROM places WHERE id = ?''', (place_id,))
    conn.commit()
    print("\nTest data cleaned up.")

def main():
    """
    Main function to run when the script is executed directly.
    """
    # Database file path
    db_path = os.path.join(os.path.dirname(__file__), '..', 'instance', 'development.db')
    
    # Check if the database exists
    if not os.path.exists(db_path):
        print(f"Database not found at {db_path}")
        print("Please run initialize_database.py first.")
        sys.exit(1)
    
    # Connect to the database
    conn = sqlite3.connect(db_path)
    
    try:
        # Enable foreign keys
        conn.execute("PRAGMA foreign_keys = ON")
        
        # Test each table
        test_users_table(conn)
        test_amenities_table(conn)
        place_id = test_places_table(conn)
        test_reviews_table(conn, place_id)
        test_place_amenity_table(conn, place_id)
        
        # Test relationships
        test_relationships(conn)
        
        # Clean up
        conn.execute('''DELETE FROM places WHERE id = ?''', (place_id,))
        conn.commit()
        
        print("\nAll tests completed successfully!")
    except Exception as e:
        print(f"Error during testing: {e}")
    finally:
        # Close the connection
        conn.close()

if __name__ == "__main__":
    main()
