# 🏨 HBnB Project

This project is a Flask-based API for the HBnB (Holberton Bed and Breakfast) application.

## 📁 Project Structure

- `app/`: Core application code
  - `api/`: API endpoints (organized by version)
  - `models/`: Business logic classes
  - `services/`: Facade pattern implementation
  - `persistence/`: In-memory repository implementation
- `run.py`: Entry point for running the Flask application
- `config.py`: Configuration for environment variables and application settings
- `requirements.txt`: List of Python packages needed for the project

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

## 👨‍💻 Development

This project uses a layered architecture with the Facade pattern for communication between layers. The current implementation uses an in-memory repository, which will be replaced by a database-backed solution in future iterations.

The business logic layer (models) is designed to be independent of the persistence layer, allowing for easy switching between different storage solutions in the future.

## ✅ Validation

All models include validation for their attributes:

- 👤 **User**: Validates first_name, last_name, email, and password
- 🏠 **Place**: Validates title, price, latitude, longitude, and owner_id
- ⭐ **Review**: Validates text, rating, user, and place
- 🛁 **Amenity**: Validates name

For more details on validation, see the [Testing Report](testing_report.md).
