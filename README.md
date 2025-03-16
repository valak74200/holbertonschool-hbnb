# HbnB - Holberton Airbnb Clone 🏠

Welcome to HbnB, a comprehensive Airbnb clone project! This application implements core features of the Airbnb platform, providing a robust solution for property listing and booking management.

## 🌟 Features

### User Management 👤
- User registration and authentication with JWT
- Profile management
- User roles and permissions (regular users and administrators)

### Property Management 🏘️
- Property listing creation and management
- Detailed property information
- Location-based property search
- Relationship management between properties and amenities

### Review System ⭐
- Property reviews and ratings
- Review validation (users cannot review their own properties)
- One review per user per property enforcement

### Amenity Management 🛋️
- Amenity creation and management (admin only)
- Many-to-many relationship between places and amenities

### Security 🔐
- JWT-based authentication
- Role-based access control
- Resource ownership validation
- Protected endpoints for sensitive operations

## 🏗️ Architecture

The project follows a structured architecture, documented through various UML diagrams:

### Class Structure 📊
- [Class Diagram](./UML/Class_Diagram.png) - Core system classes and their relationships
- [Package Diagram](./UML/Package_Diagram.png) - High-level package organization

### Sequence Flows 🔄
- [User Registration](./UML/Sequences%20diagrams/User_Registration.png) - New user onboarding process
- [Place Creation](./UML/Sequences%20diagrams/Place_Creation.png) - Property listing workflow
- [Review Submission](./UML/Sequences%20diagrams/Review_Submission.png) - User review process
- [Fetching Places](./UML/Sequences%20diagrams/Fetching_Places_List.png) - Property search and retrieval

## 📚 Documentation

Detailed documentation about the project's architecture, APIs, and features can be found in the [Documentation](./Documentation.md) file.

### Additional Documentation

- [Part 2 README](./part2/README.md) - Specific documentation for part 2 of the project
- [Relationships Documentation](./part2/RELATIONSHIPS.md) - Details about database relationships
- [Admin Permissions](./part2/ADMIN_PERMISSIONS.md) - Information about administrator permissions
- [JWT Test Report](./part2/tests/jwt_test_report.md) - Report on JWT authentication testing
- [Entity Mappings Test Summary](./part2/tests/entity_mappings_test_summary.md) - Summary of entity mappings tests
- [Scripts README](./part2/scripts/README.md) - Documentation for database setup scripts

## 🛠️ Technical Stack

- **Backend**: Python-based REST API with Flask
- **Database**: SQLAlchemy ORM with SQLite storage
- **Authentication**: JWT-based authentication system
- **API Documentation**: Flask-RESTx/Swagger
- **Testing**: Pytest, curl-based black-box testing

## 🚀 Getting Started

1. Clone the repository:
```bash
git clone https://github.com/[your-username]/HbnB.git
```

2. Install dependencies:
```bash
cd HbnB
pip install -r requirements.txt
```

3. Set up the database:
```bash
cd part2
python scripts/initialize_database.py
```

4. Start the application:
```bash
python run.py
```

5. Access the API documentation:
```
http://localhost:5000/api/v1/
```

## 🧪 Testing

The project includes comprehensive testing to ensure all functionality works as expected:

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

## 👮 Admin Features

To create an admin user:

```bash
cd part2
python scripts/make_admin.py <email>
```

Admin users have special privileges:
- Creating and modifying users
- Creating and modifying amenities
- Modifying or deleting any place or review (bypassing ownership restrictions)

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
