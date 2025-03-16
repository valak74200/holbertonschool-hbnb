# Database Setup Scripts

This directory contains scripts for setting up the database for the HBNB application. These scripts demonstrate how to create the database tables and insert data with proper UUIDs.

## Files

- `create_tables.sql`: SQL script to create the database tables with proper relationships.
- `generate_uuid.py`: Python script to generate UUIDs for database records.
- `setup_database.py`: Python script to set up the database using the SQL scripts and insert sample data.

## Database Schema

The database schema consists of the following tables:

### User Table
- `id`: CHAR(36) PRIMARY KEY (UUID format)
- `first_name`: VARCHAR(255)
- `last_name`: VARCHAR(255)
- `email`: VARCHAR(255) UNIQUE
- `password`: VARCHAR(255)
- `role`: VARCHAR(20) DEFAULT 'user'
- `is_admin`: BOOLEAN DEFAULT FALSE
- `created_at`: TIMESTAMP DEFAULT CURRENT_TIMESTAMP
- `updated_at`: TIMESTAMP DEFAULT CURRENT_TIMESTAMP

### Place Table
- `id`: CHAR(36) PRIMARY KEY (UUID format)
- `title`: VARCHAR(255)
- `description`: TEXT
- `price`: DECIMAL(10, 2)
- `latitude`: FLOAT
- `longitude`: FLOAT
- `owner_id`: CHAR(36) (Foreign key referencing User(id))
- `user_id`: CHAR(36) (Foreign key referencing User(id))
- `created_at`: TIMESTAMP DEFAULT CURRENT_TIMESTAMP
- `updated_at`: TIMESTAMP DEFAULT CURRENT_TIMESTAMP

### Amenity Table
- `id`: CHAR(36) PRIMARY KEY (UUID format)
- `name`: VARCHAR(255) UNIQUE
- `created_at`: TIMESTAMP DEFAULT CURRENT_TIMESTAMP
- `updated_at`: TIMESTAMP DEFAULT CURRENT_TIMESTAMP

### Place_Amenity Table (Many-to-Many relationship)
- `place_id`: CHAR(36) (Foreign key referencing Place(id))
- `amenity_id`: CHAR(36) (Foreign key referencing Amenity(id))
- Composite primary key for place_id and amenity_id

### Review Table
- `id`: CHAR(36) PRIMARY KEY (UUID format)
- `text`: TEXT
- `rating`: INT (Between 1 and 5)
- `user_id`: CHAR(36) (Foreign key referencing User(id))
- `place_id`: CHAR(36) (Foreign key referencing Place(id))
- `created_at`: TIMESTAMP DEFAULT CURRENT_TIMESTAMP
- `updated_at`: TIMESTAMP DEFAULT CURRENT_TIMESTAMP
- Unique constraint on the combination of user_id and place_id to ensure that a user can only leave one review per place

## Relationships

The database schema implements the following relationships:

1. **User and Place (One-to-Many)**:
   - A User can own many Places (through the owner_id foreign key)
   - A User can be associated with many Places (through the user_id foreign key)
   - Each Place has exactly one owner and one associated user

2. **Place and Review (One-to-Many)**:
   - A Place can have many Reviews
   - Each Review belongs to exactly one Place

3. **User and Review (One-to-Many)**:
   - A User can write many Reviews
   - Each Review is written by exactly one User

4. **Place and Amenity (Many-to-Many)**:
   - A Place can have many Amenities
   - An Amenity can be associated with many Places
   - The Place_Amenity table manages this many-to-many relationship

## Usage

### Creating the Database Tables

To create the database tables, you can use the `create_tables.sql` script directly with SQLite:

```bash
sqlite3 database.db < create_tables.sql
```

Or you can use the `setup_database.py` script, which will create the tables and insert sample data:

```bash
python setup_database.py
```

### Generating UUIDs

To generate UUIDs for database records, you can use the `generate_uuid.py` script:

```bash
python generate_uuid.py
```

This will generate a single UUID. To generate multiple UUIDs, you can specify a count:

```bash
python generate_uuid.py 5
```

### Inserting Data

The `setup_database.py` script demonstrates how to insert data into the database with proper UUIDs. It creates sample users, places, amenities, and reviews, and establishes the relationships between them.

## Example Queries

The `setup_database.py` script also includes example queries to demonstrate the relationships:

1. **One-to-Many: User to Places**:
   ```sql
   SELECT title, price FROM places WHERE owner_id = (SELECT id FROM users LIMIT 1)
   ```

2. **One-to-Many: Place to Reviews**:
   ```sql
   SELECT r.rating, r.text, u.first_name
   FROM reviews r
   JOIN users u ON r.user_id = u.id
   WHERE r.place_id = (SELECT id FROM places LIMIT 1)
   ```

3. **Many-to-Many: Place to Amenities**:
   ```sql
   SELECT a.name
   FROM amenities a
   JOIN place_amenity pa ON a.id = pa.amenity_id
   WHERE pa.place_id = (SELECT id FROM places ORDER BY title DESC LIMIT 1)
   ```

4. **Many-to-Many: Amenity to Places**:
   ```sql
   SELECT p.title
   FROM places p
   JOIN place_amenity pa ON p.id = pa.place_id
   WHERE pa.amenity_id = (SELECT id FROM amenities LIMIT 1)
   ```

These queries demonstrate how to navigate the relationships between the entities in the database.
