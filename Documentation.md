# 🏠 HBnB Evolution Technical Documentation

## 📑 Table of Contents
1. [Overview](#overview)
2. [UML Diagrams](#uml-diagrams)
3. [System Architecture](#system-architecture)
4. [Domain Models](#domain-models)
5. [Business Rules](#business-rules)
6. [Data Layer](#data-layer)
7. [Authentication & Authorization](#authentication--authorization)
8. [Admin Permissions](#admin-permissions)
9. [API Endpoints](#api-endpoints)
10. [Testing](#testing)

## 🎯 Overview

HBnB Evolution is a property rental platform inspired by AirBnB. The system allows users to list properties, manage bookings, and leave reviews.

### ✨ Core Features
- 👤 User registration and profile management
- 🏡 Property listing and management
- ⭐ Review and rating system
- 🛋️ Amenity management
- 🔐 JWT Authentication
- 👮 Admin permissions and role-based access control

## 📊 UML Diagrams

### 🔄 Class Diagram
The following class diagram illustrates the relationships between the main entities in our system:

![Class Diagram](UML/Class_Diagram.png)

This diagram shows the inheritance hierarchy and relationships between BaseModel, User, Place, Review, and Amenity classes, along with their attributes and methods.

### 📦 Package Diagram
The package diagram demonstrates the high-level organization of our system components:

![Package Diagram](UML/Package_Diagram.png)

This diagram illustrates how different modules are organized and their dependencies.

### ⚡ Sequence Diagrams

#### 📝 User Registration Flow
The following diagram shows the sequence of interactions during user registration:

![User Registration](UML/Sequences%20diagrams/User_Registration.png)

This diagram illustrates the steps involved when a new user registers on the platform.

#### 🏘️ Place Creation Process
The sequence for creating a new property listing:

![Place Creation](UML/Sequences%20diagrams/Place_Creation.png)

This diagram shows the interaction between different components when a user creates a new place listing.

#### 🔍 Fetching Places List
The sequence for retrieving the list of available places:

![Fetching Places](UML/Sequences%20diagrams/Fetching_Places_List.png)

This diagram demonstrates how the system handles requests for viewing available properties.

#### 📋 Review Submission Process
The sequence for submitting a review:

![Review Submission](UML/Sequences%20diagrams/Review_Submission.png)

This diagram shows the flow of interactions when a user submits a review for a place.

## 🏗️ System Architecture

The application follows a three-tier architecture:

### 1. 🖥️ Presentation Layer
- 🌐 Handles client interactions
- 🔌 Implements REST APIs
- 🔐 Manages authentication/authorization
- ✅ Validates input data

### 2. ⚙️ Business Logic Layer
- 📜 Implements core business rules
- 🔄 Manages domain models
- ✔️ Handles data validation
- 🎮 Coordinates operations

### 3. 💾 Persistence Layer
- 📁 Manages data storage
- 🔄 Implements CRUD operations
- 🛡️ Ensures data integrity
- 🔄 Manages database relationships

## 🔨 Domain Models

### 📋 BaseModel
Common attributes for all entities:
```python
class BaseModel:
    id: str          # Unique identifier
    created_at: datetime  # Creation timestamp
    updated_at: datetime  # Last update timestamp
```

### 👤 User
```python
class User(BaseModel):
    first_name: str
    last_name: str
    email: str      # Unique
    password: str   # Hashed
    is_admin: bool  # Administrator flag
```

### 🏠 Place
```python
class Place(BaseModel):
    title: str
    description: str
    price: float
    latitude: float
    longitude: float
    owner_id: str           # Reference to User
    amenities: List[str]    # List of amenity IDs
```

### ⭐ Review
```python
class Review(BaseModel):
    text: str
    rating: int        # 1-5 rating
    user_id: str      # Reference to User
    place_id: str     # Reference to Place
```

### 🛋️ Amenity
```python
class Amenity(BaseModel):
    name: str
```

## 📜 Business Rules

### 👥 User Management

#### 📝 Registration
- ✉️ Email must be unique
- 🔒 Password must be securely hashed
- ✅ Required fields: first_name, last_name, email, password

#### 🔐 Authentication
- 🔍 Email/password validation
- 🎫 JWT token generation
- 📌 Session management

#### 🛡️ Authorization
- 👮 Role-based access control (admin/regular user)
- 🔒 Resource ownership validation

### 🏘️ Place Management

#### ➕ Creation
- 👤 Only authenticated users can create places
- ✅ Required fields: title, price, location
- 👑 Owner automatically assigned

#### 🔄 Updates
- 👑 Only owner can modify place details
- 👮 Admin can moderate content

#### ❌ Deletion
- 🗑️ Only owner or admin can delete places
- 🔄 Associated reviews must be handled

### ⭐ Review Management

#### ➕ Creation
- 👤 Only authenticated users can create reviews
- 1️⃣ One review per user per place
- 🌟 Rating must be between 1-5
- ⚠️ User cannot review own property

#### ✅ Validation
- 💬 Comment cannot be empty
- ⚠️ User cannot review own property

### 🛋️ Amenity Management

#### 🔄 Operations
- 👮 Only admin can create/update/delete amenities
- 👥 All users can view amenities

#### 🔗 Association
- 🏠 Places can have multiple amenities
- 🛋️ Amenities can be associated with multiple places

## 💾 Data Layer

### 📊 Database Schema
```sql
-- Users table
CREATE TABLE users (
    id VARCHAR PRIMARY KEY,
    first_name VARCHAR NOT NULL,
    last_name VARCHAR NOT NULL,
    email VARCHAR UNIQUE NOT NULL,
    password_hash VARCHAR NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- Places table
CREATE TABLE places (
    id VARCHAR PRIMARY KEY,
    title VARCHAR NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    latitude DECIMAL(10,8),
    longitude DECIMAL(11,8),
    owner_id VARCHAR REFERENCES users(id),
    user_id VARCHAR REFERENCES users(id),
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- Reviews table
CREATE TABLE reviews (
    id VARCHAR PRIMARY KEY,
    text TEXT NOT NULL,
    rating INTEGER CHECK (rating BETWEEN 1 AND 5),
    user_id VARCHAR REFERENCES users(id),
    place_id VARCHAR REFERENCES places(id),
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    UNIQUE(user_id, place_id)
);

-- Amenities table
CREATE TABLE amenities (
    id VARCHAR PRIMARY KEY,
    name VARCHAR NOT NULL,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- Place-Amenity relationship table
CREATE TABLE place_amenity (
    place_id VARCHAR REFERENCES places(id),
    amenity_id VARCHAR REFERENCES amenities(id),
    PRIMARY KEY (place_id, amenity_id)
);
```

### 🔄 Database Relationships

#### One-to-Many Relationships

1. **User to Place**
   - A user can own many places, but each place has only one owner
   - A user can be associated with many places

2. **User to Review**
   - A user can write many reviews, but each review is written by only one user

3. **Place to Review**
   - A place can have many reviews, but each review is for only one place

#### Many-to-Many Relationships

1. **Place to Amenity**
   - A place can have many amenities
   - An amenity can be associated with many places
   - Managed through the place_amenity association table

### 🔄 Data Access Patterns

#### 👤 User Operations
```python
def create_user(user_data: dict) -> User
def get_user_by_id(user_id: str) -> User
def get_user_by_email(email: str) -> User
def update_user(user_id: str, data: dict) -> User
def delete_user(user_id: str) -> bool
```

#### 🏠 Place Operations
```python
def create_place(place_data: dict) -> Place
def get_place_by_id(place_id: str) -> Place
def get_places_by_owner(owner_id: str) -> List[Place]
def update_place(place_id: str, data: dict) -> Place
def delete_place(place_id: str) -> bool
```

#### ⭐ Review Operations
```python
def create_review(review_data: dict) -> Review
def get_place_reviews(place_id: str) -> List[Review]
def update_review(review_id: str, data: dict) -> Review
def delete_review(review_id: str) -> bool
```

#### 🛋️ Amenity Operations
```python
def create_amenity(amenity_data: dict) -> Amenity
def get_all_amenities() -> List[Amenity]
def update_amenity(amenity_id: str, data: dict) -> Amenity
def delete_amenity(amenity_id: str) -> bool
```

### ✅ Data Validation

#### 📝 Input Validation
- ✔️ Type checking
- 📋 Format validation
- ❗ Required fields verification

#### 📜 Business Rule Validation
- 👑 Ownership verification
- 🔒 Permission checking
- 🔗 Relationship validation

#### 🛡️ Data Integrity
- 🔑 Foreign key constraints
- 🎯 Unique constraints
- ✅ Data consistency checks

## 🔐 Authentication & Authorization

### JWT Authentication

The application uses JSON Web Tokens (JWT) for authentication. This provides a secure, stateless way to authenticate users and protect sensitive endpoints.

#### Authentication Flow

1. **User Registration**: Users register by providing their first name, last name, email, and password.
2. **User Login**: Users login with their email and password to receive a JWT token.
3. **Protected Endpoints**: Protected endpoints require a valid JWT token in the Authorization header.
4. **Public Endpoints**: Public endpoints do not require authentication.

#### Protected vs. Public Endpoints

##### Protected Endpoints (Require JWT Authentication)

- **POST /api/v1/places/**: Create a new place
- **PUT /api/v1/places/<place_id>**: Update a place (only the owner can update)
- **POST /api/v1/reviews/**: Create a new review
- **PUT /api/v1/reviews/<review_id>**: Update a review (only the author can update)
- **DELETE /api/v1/reviews/<review_id>**: Delete a review (only the author can delete)
- **PUT /api/v1/users/<user_id>**: Update a user (users can only update their own profile)
- **POST /api/v1/amenities/**: Create a new amenity
- **PUT /api/v1/amenities/<amenity_id>**: Update an amenity

##### Public Endpoints (No Authentication Required)

- **GET /api/v1/places/**: Retrieve a list of all places
- **GET /api/v1/places/<place_id>**: Retrieve details of a specific place
- **GET /api/v1/places/<place_id>/reviews**: Retrieve reviews for a specific place
- **GET /api/v1/reviews/**: Retrieve a list of all reviews
- **GET /api/v1/reviews/<review_id>**: Retrieve details of a specific review
- **GET /api/v1/users/**: Retrieve a list of all users
- **GET /api/v1/users/<user_id>**: Retrieve details of a specific user
- **GET /api/v1/amenities/**: Retrieve a list of all amenities
- **GET /api/v1/amenities/<amenity_id>**: Retrieve details of a specific amenity

### JWT Implementation

The JWT token includes the user's ID and admin status:

```python
access_token = create_access_token(
    identity=str(user.id),
    additional_claims={'is_admin': user.is_admin}
)
```

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

### Role-Based Access Control (RBAC)

The API uses Role-Based Access Control (RBAC) to restrict access to certain endpoints. There are two approaches implemented:

1. **Admin Required Decorator**: A decorator that checks if the user is an admin before allowing access to the endpoint.
2. **In-Function RBAC**: Checking the user's role within the endpoint function.

### Making a User an Admin

To make a user an admin, you can use the `make_admin.py` script:

```bash
cd part2
python scripts/make_admin.py <email>
```

## 🌐 API Endpoints

### User Endpoints

- `POST /api/v1/users/`: Create a new user
- `GET /api/v1/users/`: Get all users
- `GET /api/v1/users/<user_id>`: Get a specific user
- `PUT /api/v1/users/<user_id>`: Update a user (authenticated, self only)

### Place Endpoints

- `POST /api/v1/places/`: Create a new place (authenticated)
- `GET /api/v1/places/`: Get all places
- `GET /api/v1/places/<place_id>`: Get a specific place
- `PUT /api/v1/places/<place_id>`: Update a place (authenticated, owner only)
- `DELETE /api/v1/places/<place_id>`: Delete a place (authenticated, owner only)

### Review Endpoints

- `POST /api/v1/reviews/`: Create a new review (authenticated)
- `GET /api/v1/reviews/`: Get all reviews
- `GET /api/v1/reviews/<review_id>`: Get a specific review
- `PUT /api/v1/reviews/<review_id>`: Update a review (authenticated, author only)
- `DELETE /api/v1/reviews/<review_id>`: Delete a review (authenticated, author only)

### Amenity Endpoints

- `POST /api/v1/amenities/`: Create a new amenity (authenticated)
- `GET /api/v1/amenities/`: Get all amenities
- `GET /api/v1/amenities/<amenity_id>`: Get a specific amenity
- `PUT /api/v1/amenities/<amenity_id>`: Update an amenity (authenticated)

### Authentication Endpoints

- `POST /api/v1/auth/login`: Login and get a JWT token
- `POST /api/v1/auth/register`: Register a new user

### Admin Endpoints

- `POST /api/v1/admin/users`: Create a new user (admin only)
- `PUT /api/v1/admin/users/<user_id>`: Update a user (admin only)
- `POST /api/v1/admin/amenities`: Create a new amenity (admin only)
- `PUT /api/v1/admin/amenities/<amenity_id>`: Update an amenity (admin only)

## 🧪 Testing

The application includes comprehensive testing to ensure that all functionality works as expected.

### Test Types

1. **Unit Tests**: Test individual components in isolation
2. **Integration Tests**: Test the interaction between components
3. **API Tests**: Test the API endpoints using HTTP requests
4. **Authentication Tests**: Test the JWT authentication system
5. **Authorization Tests**: Test the role-based access control system

### Test Scripts

- `test_models.py`: Tests the business logic layer
- `test_auth.py`: Tests the authentication system
- `test_jwt_places.py`: Tests JWT authentication for place endpoints
- `test_jwt_reviews.py`: Tests JWT authentication for review endpoints
- `test_jwt_users.py`: Tests JWT authentication for user endpoints
- `test_jwt_amenities.py`: Tests JWT authentication for amenity endpoints
- `test_admin_permissions.py`: Tests the admin permissions system
- `test_relationships_crud.py`: Tests the database relationships
- `test_place_amenity_relationship.py`: Tests the many-to-many relationship between places and amenities

### Running Tests

To run the tests, use the following commands:

```bash
# Run model tests
python -m app.models.test_models

# Run API tests
python -m pytest tests/

# Run JWT authentication tests
cd part2/tests
./run_jwt_tests.sh

# Run curl tests
cd part2/tests
./curl_jwt_tests.sh
```

### Test Reports

- `test_report.md`: Report of API validation tests
- `jwt_test_report.md`: Report of JWT authentication tests
- `entity_mappings_test_summary.md`: Summary of entity mappings tests
