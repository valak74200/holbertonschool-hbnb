# 🏨 HBnB Project

This project is a Flask-based API for the HBnB (Holberton Bed and Breakfast) application.

## 📁 Project Structure

- `app/`: Core application code
  - `api/`: API endpoints (organized by version)
    - `v1/`: Version 1 of the API
      - `admin.py`: Admin-specific endpoints
      - `amenities.py`: Amenity endpoints
      - `auth.py`: Authentication endpoints
      - `decorators.py`: Custom decorators for authentication and authorization
      - `places.py`: Place endpoints
      - `reviews.py`: Review endpoints
      - `users.py`: User endpoints
  - `models/`: Business logic classes
    - `base_model.py`: Base class for all models
    - `user.py`: User model
    - `place.py`: Place model
    - `review.py`: Review model
    - `amenity.py`: Amenity model
  - `services/`: Facade pattern implementation
    - `facade.py`: Service layer that coordinates between API and persistence
  - `persistence/`: Database repository implementation
    - `repository.py`: Base repository interface
    - `sqlalchemy_repository.py`: SQLAlchemy implementation
    - `user_repository.py`: User-specific repository
    - `place_repository.py`: Place-specific repository
    - `review_repository.py`: Review-specific repository
    - `amenity_repository.py`: Amenity-specific repository
- `run.py`: Entry point for running the Flask application
- `config.py`: Configuration for environment variables and application settings
- `scripts/`: Utility scripts for database setup and management
- `tests/`: Test files for API validation and JWT authentication
- `examples/`: Example scripts demonstrating relationships

## 💼 Business Logic Layer

The business logic layer is implemented in the `app/models/` directory. It consists of the following classes:

- `BaseModel`: A base class that provides common attributes (id, created_at, updated_at) and methods for all models.
- `👤 User`: Represents a user of the application.
- `🏠 Place`: Represents a place that can be rented.
- `⭐ Review`: Represents a review for a place.
- `🛁 Amenity`: Represents an amenity that a place can have.

These classes implement the core business logic, including attribute validation and relationship management.

### 🔄 Relationships

- A User can own multiple Places (one-to-many relationship).
- A Place can have multiple Reviews (one-to-many relationship).
- A Place can have multiple Amenities (many-to-many relationship).
- A Review is associated with one User and one Place.

For more detailed information about database relationships in this application, see the [Relationships Documentation](RELATIONSHIPS.md).

You can also check out the [relationship examples script](examples/relationship_examples.py) for a practical demonstration of how to work with one-to-many and many-to-many relationships in this application.

### 🧩 Using the Models

Here are some examples of how to use the model classes:

```python
# Creating a user
user = User(first_name="John", last_name="Doe", email="john.doe@example.com")

# Creating a place
place = Place(title="Cozy Apartment", description="A nice place to stay", 
              price=100, latitude=37.7749, longitude=-122.4194, owner=user)

# Adding a review to a place
review = Review(text="Great stay!", rating=5, place=place, user=user)
place.add_review(review)

# Adding an amenity to a place
amenity = Amenity(name="Wi-Fi")
place.add_amenity(amenity)

# Updating an object
user.update({"first_name": "Jane", "last_name": "Smith"})
```

Each model includes validation for its attributes. For example, trying to set an invalid email for a User will raise a ValueError:

```python
try:
    user.email = "invalid_email"
except ValueError as e:
    print(f"Error: {e}")
```

## 🔐 Authentication & Authorization

The application uses JWT (JSON Web Token) authentication to secure the API endpoints.

### Authentication Flow

1. **User Registration**: Users register by providing their first name, last name, email, and password.
2. **User Login**: Users login with their email and password to receive a JWT token.
3. **Protected Endpoints**: Protected endpoints require a valid JWT token in the Authorization header.
4. **Public Endpoints**: Public endpoints do not require authentication.

### Protected vs. Public Endpoints

#### Protected Endpoints (Require JWT Authentication)

- **POST /api/v1/places/**: Create a new place
- **PUT /api/v1/places/<place_id>**: Update a place (only the owner can update)
- **POST /api/v1/reviews/**: Create a new review
- **PUT /api/v1/reviews/<review_id>**: Update a review (only the author can update)
- **DELETE /api/v1/reviews/<review_id>**: Delete a review (only the author can delete)
- **PUT /api/v1/users/<user_id>**: Update a user (users can only update their own profile)
- **POST /api/v1/amenities/**: Create a new amenity
- **PUT /api/v1/amenities/<amenity_id>**: Update an amenity

#### Public Endpoints (No Authentication Required)

- **GET /api/v1/places/**: Retrieve a list of all places
- **GET /api/v1/places/<place_id>**: Retrieve details of a specific place
- **GET /api/v1/places/<place_id>/reviews**: Retrieve reviews for a specific place
- **GET /api/v1/reviews/**: Retrieve a list of all reviews
- **GET /api/v1/reviews/<review_id>**: Retrieve details of a specific review
- **GET /api/v1/users/**: Retrieve a list of all users
- **GET /api/v1/users/<user_id>**: Retrieve details of a specific user
- **GET /api/v1/amenities/**: Retrieve a list of all amenities
- **GET /api/v1/amenities/<amenity_id>**: Retrieve details of a specific amenity

For more details on JWT authentication, see the [JWT Test Report](tests/jwt_test_report.md).

## 👮 Admin Permissions

Administrators have special privileges that allow them to perform actions that regular users cannot.

### Admin Privileges

1. Creating and modifying users
2. Creating and modifying amenities
3. Modifying or deleting any place or review, bypassing the ownership restrictions that regular users face

### Admin Endpoints

The following endpoints are specifically for administrators:

- `POST /api/v1/admin/users`: Create a new user.
- `PUT /api/v1/admin/users/<user_id>`: Modify a user's details, including email and password.
- `POST /api/v1/admin/amenities`: Add a new amenity.
- `PUT /api/v1/admin/amenities/<amenity_id>`: Modify the details of an amenity.

For more details on admin permissions, see the [Admin Permissions Documentation](ADMIN_PERMISSIONS.md).

## 🚀 Installation

1. Clone the repository
2. Navigate to the project directory
3. Create a virtual environment:
   ```
   python3 -m venv venv
   ```
4. Activate the virtual environment:
   ```
   source venv/bin/activate
   ```
5. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## ▶️ Running the Application

To run the application, use the following command:

```
python run.py
```

The application will start in debug mode, and you can access the API documentation at `http://localhost:5000/api/v1/`.

## 🧪 Running the Tests

To run the tests for the business logic layer, use the following command:

```
python -m app.models.test_models
```

This will run all the tests defined in the `test_models.py` file.

For API validation tests, use:

```
python -m pytest tests/
```

To run black-box testing with cURL:

```
bash tests/curl_tests.sh
```

To run JWT authentication tests:

```
bash tests/run_jwt_tests.sh
```

To run admin permission tests:

```
bash tests/curl_admin_tests.sh
```

## 👨‍💻 Development

This project uses a layered architecture with the Facade pattern for communication between layers. The current implementation uses SQLAlchemy for database operations.

The business logic layer (models) is designed to be independent of the persistence layer, allowing for easy switching between different storage solutions in the future.

## 📊 Database

The application uses SQLite as the database engine. The database schema is defined in the `scripts/create_tables.sql` file.

### Database Setup

To set up the database, use the following command:

```
python scripts/initialize_database.py
```

This will create the database tables and insert sample data.

### Database Relationships

The database schema implements the following relationships:

1. **User and Place (One-to-Many)**:
   - A User can own many Places
   - Each Place has exactly one owner

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

For more details on database relationships, see the [Relationships Documentation](RELATIONSHIPS.md).

## ✅ Validation

All models include validation for their attributes:

- 👤 **User**: Validates first_name, last_name, email, and password
- 🏠 **Place**: Validates title, price, latitude, longitude, and owner_id
- ⭐ **Review**: Validates text, rating, user, and place
- 🛁 **Amenity**: Validates name

For more details on validation, see the [Testing Report](../test_report.md).
