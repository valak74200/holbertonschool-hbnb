#!/usr/bin/env python3
"""
Script to set up the database using the SQL scripts.
This demonstrates how to create the tables and insert data with proper UUIDs.
"""

import sqlite3
import os
import uuid
import sys
import hashlib

# Add the parent directory to the path so we can import app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def create_tables(conn):
    """
    Create the database tables using the SQL script.
    
    Args:
        conn: SQLite connection object
    """
    print("Creating tables...")
    
    # Create users table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id CHAR(36) PRIMARY KEY,
            first_name VARCHAR(255) NOT NULL,
            last_name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL,
            role VARCHAR(20) DEFAULT 'user',
            is_admin BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create places table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS places (
            id CHAR(36) PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            description TEXT,
            price DECIMAL(10, 2) NOT NULL,
            latitude FLOAT NOT NULL,
            longitude FLOAT NOT NULL,
            owner_id CHAR(36) NOT NULL,
            user_id CHAR(36) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    ''')
    
    # Create amenities table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS amenities (
            id CHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create place_amenity table (Many-to-Many relationship)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS place_amenity (
            place_id CHAR(36) NOT NULL,
            amenity_id CHAR(36) NOT NULL,
            PRIMARY KEY (place_id, amenity_id),
            FOREIGN KEY (place_id) REFERENCES places(id) ON DELETE CASCADE,
            FOREIGN KEY (amenity_id) REFERENCES amenities(id) ON DELETE CASCADE
        )
    ''')
    
    # Create reviews table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS reviews (
            id CHAR(36) PRIMARY KEY,
            text TEXT NOT NULL,
            rating INT NOT NULL CHECK (rating BETWEEN 1 AND 5),
            user_id CHAR(36) NOT NULL,
            place_id CHAR(36) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (place_id) REFERENCES places(id) ON DELETE CASCADE,
            UNIQUE (user_id, place_id) -- Ensure a user can only leave one review per place
        )
    ''')
    
    # Create triggers for updating timestamps
    try:
        conn.execute('''
            CREATE TRIGGER IF NOT EXISTS update_users_timestamp
            AFTER UPDATE ON users
            FOR EACH ROW
            BEGIN
                UPDATE users SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
            END
        ''')
    except sqlite3.Error as e:
        print(f"Warning: Could not create users trigger: {e}")
    
    try:
        conn.execute('''
            CREATE TRIGGER IF NOT EXISTS update_places_timestamp
            AFTER UPDATE ON places
            FOR EACH ROW
            BEGIN
                UPDATE places SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
            END
        ''')
    except sqlite3.Error as e:
        print(f"Warning: Could not create places trigger: {e}")
    
    try:
        conn.execute('''
            CREATE TRIGGER IF NOT EXISTS update_amenities_timestamp
            AFTER UPDATE ON amenities
            FOR EACH ROW
            BEGIN
                UPDATE amenities SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
            END
        ''')
    except sqlite3.Error as e:
        print(f"Warning: Could not create amenities trigger: {e}")
    
    try:
        conn.execute('''
            CREATE TRIGGER IF NOT EXISTS update_reviews_timestamp
            AFTER UPDATE ON reviews
            FOR EACH ROW
            BEGIN
                UPDATE reviews SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
            END
        ''')
    except sqlite3.Error as e:
        print(f"Warning: Could not create reviews trigger: {e}")
    
    conn.commit()
    print("Tables created successfully.")

def insert_sample_data(conn):
    """
    Insert sample data into the database.
    
    Args:
        conn: SQLite connection object
    """
    print("Inserting sample data...")
    
    # Generate UUIDs for the entities
    user1_id = str(uuid.uuid4())
    user2_id = str(uuid.uuid4())
    place1_id = str(uuid.uuid4())
    place2_id = str(uuid.uuid4())
    amenity1_id = str(uuid.uuid4())
    amenity2_id = str(uuid.uuid4())
    amenity3_id = str(uuid.uuid4())
    review1_id = str(uuid.uuid4())
    review2_id = str(uuid.uuid4())
    
    # Insert users
    conn.execute('''
        INSERT INTO users (id, first_name, last_name, email, password, role, is_admin)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (user1_id, 'Alice', 'Smith', 'alice@example.com', hashlib.sha256('password123'.encode()).hexdigest(), 'user', False))
    
    conn.execute('''
        INSERT INTO users (id, first_name, last_name, email, password, role, is_admin)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (user2_id, 'Bob', 'Johnson', 'bob@example.com', hashlib.sha256('password456'.encode()).hexdigest(), 'user', False))
    
    # Insert places
    conn.execute('''
        INSERT INTO places (id, title, description, price, latitude, longitude, owner_id, user_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (place1_id, 'Cozy Apartment', 'A nice place to stay in the city center', 100.00, 37.7749, -122.4194, user1_id, user1_id))
    
    conn.execute('''
        INSERT INTO places (id, title, description, price, latitude, longitude, owner_id, user_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (place2_id, 'Spacious House', 'A beautiful house with a garden', 200.00, 34.0522, -118.2437, user1_id, user1_id))
    
    # Insert amenities
    conn.execute('''
        INSERT INTO amenities (id, name)
        VALUES (?, ?)
    ''', (amenity1_id, 'Wi-Fi'))
    
    conn.execute('''
        INSERT INTO amenities (id, name)
        VALUES (?, ?)
    ''', (amenity2_id, 'Swimming Pool'))
    
    conn.execute('''
        INSERT INTO amenities (id, name)
        VALUES (?, ?)
    ''', (amenity3_id, 'Fully Equipped Kitchen'))
    
    # Insert place-amenity relationships
    conn.execute('''
        INSERT INTO place_amenity (place_id, amenity_id)
        VALUES (?, ?)
    ''', (place1_id, amenity1_id))
    
    conn.execute('''
        INSERT INTO place_amenity (place_id, amenity_id)
        VALUES (?, ?)
    ''', (place1_id, amenity3_id))
    
    conn.execute('''
        INSERT INTO place_amenity (place_id, amenity_id)
        VALUES (?, ?)
    ''', (place2_id, amenity1_id))
    
    conn.execute('''
        INSERT INTO place_amenity (place_id, amenity_id)
        VALUES (?, ?)
    ''', (place2_id, amenity2_id))
    
    conn.execute('''
        INSERT INTO place_amenity (place_id, amenity_id)
        VALUES (?, ?)
    ''', (place2_id, amenity3_id))
    
    # Insert reviews
    conn.execute('''
        INSERT INTO reviews (id, text, rating, user_id, place_id)
        VALUES (?, ?, ?, ?, ?)
    ''', (review1_id, 'Great apartment, very clean and comfortable!', 5, user2_id, place1_id))
    
    conn.execute('''
        INSERT INTO reviews (id, text, rating, user_id, place_id)
        VALUES (?, ?, ?, ?, ?)
    ''', (review2_id, 'Nice house, but a bit far from the city center.', 4, user2_id, place2_id))
    
    conn.commit()
    print("Sample data inserted successfully.")

def query_relationships(conn):
    """
    Query the database to demonstrate the relationships.
    
    Args:
        conn: SQLite connection object
    """
    print("\n=== One-to-Many: User to Places ===")
    user = conn.execute('''
        SELECT first_name, last_name FROM users LIMIT 1
    ''').fetchone()
    print(f"User: {user[0]} {user[1]}")
    print("Places owned:")
    
    places = conn.execute('''
        SELECT title, price FROM places WHERE owner_id = (SELECT id FROM users LIMIT 1)
    ''').fetchall()
    
    for place in places:
        print(f"- {place[0]} (${place[1]}/night)")
    
    print("\n=== One-to-Many: Place to Reviews ===")
    place = conn.execute('''
        SELECT title FROM places LIMIT 1
    ''').fetchone()
    print(f"Place: {place[0]}")
    print("Reviews:")
    
    reviews = conn.execute('''
        SELECT r.rating, r.text, u.first_name
        FROM reviews r
        JOIN users u ON r.user_id = u.id
        WHERE r.place_id = (SELECT id FROM places LIMIT 1)
    ''').fetchall()
    
    for review in reviews:
        print(f"- {review[0]}/5 stars: \"{review[1]}\" by {review[2]}")
    
    print("\n=== Many-to-Many: Place to Amenities ===")
    place = conn.execute('''
        SELECT title FROM places ORDER BY title DESC LIMIT 1
    ''').fetchone()
    print(f"Place: {place[0]}")
    print("Amenities:")
    
    amenities = conn.execute('''
        SELECT a.name
        FROM amenities a
        JOIN place_amenity pa ON a.id = pa.amenity_id
        WHERE pa.place_id = (SELECT id FROM places ORDER BY title DESC LIMIT 1)
    ''').fetchall()
    
    for amenity in amenities:
        print(f"- {amenity[0]}")
    
    print("\n=== Many-to-Many: Amenity to Places ===")
    amenity = conn.execute('''
        SELECT name FROM amenities LIMIT 1
    ''').fetchone()
    print(f"Amenity: {amenity[0]}")
    print("Places with this amenity:")
    
    places = conn.execute('''
        SELECT p.title
        FROM places p
        JOIN place_amenity pa ON p.id = pa.place_id
        WHERE pa.amenity_id = (SELECT id FROM amenities LIMIT 1)
    ''').fetchall()
    
    for place in places:
        print(f"- {place[0]}")

def main():
    """
    Main function to run when the script is executed directly.
    """
    # Database file path
    db_path = os.path.join(os.path.dirname(__file__), '..', 'instance', 'test_relationships.db')
    
    # Ensure the instance directory exists
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    # Remove the database file if it exists
    if os.path.exists(db_path):
        os.remove(db_path)
    
    # Connect to the database
    conn = sqlite3.connect(db_path)
    
    try:
        # Create the tables
        create_tables(conn)
        
        # Insert sample data
        insert_sample_data(conn)
        
        # Query the relationships
        query_relationships(conn)
        
        print("\nDatabase setup completed successfully.")
    except Exception as e:
        print(f"Error setting up database: {e}")
    finally:
        # Close the connection
        conn.close()

if __name__ == "__main__":
    main()
