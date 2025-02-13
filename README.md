# HbnB - Holberton Airbnb Clone 🏠

Welcome to HbnB, a comprehensive Airbnb clone project! This application implements core features of the Airbnb platform, providing a robust solution for property listing and booking management.

## 🌟 Features

### User Management 👤
- User registration and authentication
- Profile management
- User roles and permissions

### Property Management 🏘️
- Property listing creation and management
- Detailed property information
- Location-based property search
- Image upload and management

### Booking System 📅
- Real-time availability checking
- Booking management
- Reservation confirmation system

### Review System ⭐
- Property reviews and ratings
- Host reviews
- Review moderation

## 🏗️ Architecture

The project follows a structured architecture, documented through various UML diagrams:

### Class Structure 📊
- [Class Diagram](./UML/Class_Diagram.puml) - Core system classes and their relationships
- [Package Diagram](./UML/Package_Diagram.puml) - High-level package organization

### Sequence Flows 🔄
- [User Registration](./UML/Sequence%20Diagrams/User_Registration.puml) - New user onboarding process
- [Place Creation](./UML/Sequence%20Diagrams/Place_Creation.puml) - Property listing workflow
- [Review Submission](./UML/Sequence%20Diagrams/Review_Submission.puml) - User review process
- [Fetching Places](./UML/Sequence%20Diagrams/Fetching_Places_List.puml) - Property search and retrieval

## 📚 Documentation

Detailed documentation about the project's architecture, APIs, and features can be found in the [Documentation](./Documentation.md) file.

## 🛠️ Technical Stack

- Backend: Python-based REST API
- Database: SQL storage engine
- Authentication: Token-based system
- API Documentation: Swagger/OpenAPI

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
python3 setup_db.py
```

4. Start the application:
```bash
python3 app.py
```

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
