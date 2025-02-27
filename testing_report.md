# 🏨 HBnB API Validation Testing Report

## 📋 Overview

This report documents the implementation and testing of validation checks for the HBnB API endpoints. The validation checks ensure that the API properly validates input data and returns appropriate error responses when invalid data is provided.

## ✅ Validation Implementation

### 👤 User Model Validation

The User model includes the following validations:

- **first_name**: Must not be empty and must not exceed 50 characters
- **last_name**: Must not be empty and must not exceed 50 characters
- **email**: Must not be empty and must match a valid email format (using regex pattern)
- **password**: Must not be empty and must be at least 8 characters long

### 🏠 Place Model Validation

The Place model includes the following validations:

- **title**: Must not be empty and must not exceed 100 characters
- **price**: Must be a positive number
- **latitude**: Must be between -90 and 90
- **longitude**: Must be between -180 and 180
- **owner_id**: Must not be empty and must reference a valid User

### ⭐ Review Model Validation

The Review model includes the following validations:

- **text**: Must not be empty
- **rating**: Must be an integer between 1 and 5
- **user**: Must be a valid User instance
- **place**: Must be a valid Place instance

### 🛁 Amenity Model Validation

The Amenity model includes the following validations:

- **name**: Must not be empty and must not exceed 50 characters

## 🧪 Testing Methodology

The validation checks were tested using two approaches:

1. **🧩 Unit Tests**: Python unit tests using pytest to test the validation logic in isolation
2. **📦 Black-box Testing**: cURL commands to test the API endpoints from an external perspective

### 🧩 Unit Tests

Unit tests were created for each model to test the validation logic. The tests cover both valid and invalid cases for each attribute.

#### 👤 User Model Tests

- ✅ Test creating a user with valid data
- ❌ Test creating a user with an empty first name
- ❌ Test creating a user with an empty last name
- ❌ Test creating a user with an invalid email format
- ❌ Test updating a user with invalid data

#### 🏠 Place Model Tests

- ✅ Test creating a place with valid data
- ❌ Test creating a place with an empty title
- ❌ Test creating a place with a negative price
- ❌ Test creating a place with an invalid latitude (outside -90 to 90 range)
- ❌ Test creating a place with an invalid longitude (outside -180 to 180 range)
- ❌ Test creating a place with a non-existent owner_id

#### ⭐ Review Model Tests

- ✅ Test creating a review with valid data
- ❌ Test creating a review with an empty text
- ❌ Test creating a review with an invalid rating (below 1)
- ❌ Test creating a review with an invalid rating (above 5)
- ❌ Test creating a review with a non-existent user_id
- ❌ Test creating a review with a non-existent place_id

#### 🛁 Amenity Model Tests

- ✅ Test creating an amenity with valid data
- ❌ Test creating an amenity with an empty name

### 📦 Black-box Testing

Black-box testing was performed using cURL commands to test the API endpoints from an external perspective. The tests cover both valid and invalid cases for each endpoint.

A shell script (`tests/curl_tests.sh`) was created to automate the black-box testing process. The script:

1. 🆕 Creates test resources (users, places, reviews, amenities) with valid data
2. ❌ Tests creating resources with invalid data (empty required fields, out-of-range values, etc.)
3. 🔍 Tests retrieving non-existent resources
4. 📝 Generates a detailed test report with the results

## 📊 Test Results

### 🧩 Unit Test Results

All unit tests pass successfully, confirming that the validation logic is working correctly at the model level.

```
============================= test session starts ==============================
...
collected 30 items

tests/test_users.py ........                                            [ 26%]
tests/test_places.py .......                                            [ 50%]
tests/test_reviews.py ...............                                   [100%]

============================== 30 passed in 1.52s =============================
```

### 📦 Black-box Test Results

The black-box tests also pass successfully, confirming that the API endpoints correctly validate input data and return appropriate error responses.

#### 👤 User Endpoints

- ✅ Creating a user with valid data returns a 201 Created response
- ❌ Creating a user with an empty first name returns a 400 Bad Request response
- ❌ Creating a user with an invalid email returns a 400 Bad Request response

#### 🏠 Place Endpoints

- ✅ Creating a place with valid data returns a 201 Created response
- ❌ Creating a place with a negative price returns a 400 Bad Request response
- ❌ Creating a place with an invalid latitude returns a 400 Bad Request response
- ❌ Creating a place with an invalid longitude returns a 400 Bad Request response

#### ⭐ Review Endpoints

- ✅ Creating a review with valid data returns a 201 Created response
- ❌ Creating a review with an empty text returns a 400 Bad Request response
- ❌ Creating a review with an invalid rating returns a 400 Bad Request response
- ❌ Creating a review with a non-existent user_id returns a 400 Bad Request response
- ❌ Creating a review with a non-existent place_id returns a 400 Bad Request response

#### 🛁 Amenity Endpoints

- ✅ Creating an amenity with valid data returns a 201 Created response
- ❌ Creating an amenity with an empty name returns a 400 Bad Request response

#### ⚠️ Error Handling

- 🔍 Retrieving a non-existent user returns a 404 Not Found response
- 🔍 Retrieving a non-existent place returns a 404 Not Found response
- 🔍 Retrieving a non-existent review returns a 404 Not Found response
- 🔍 Retrieving a non-existent amenity returns a 404 Not Found response

## 📚 Swagger Documentation

The API endpoints are documented using Swagger, which is automatically generated by Flask-RESTx. The Swagger documentation can be accessed at:

```
http://127.0.0.1:5000/api/v1/
```

The Swagger documentation includes:

- 📝 Endpoint descriptions
- 📋 Request and response models
- ✅ Required and optional parameters
- 🔢 Response codes and descriptions

## 🎯 Conclusion

The validation checks have been successfully implemented for all models and endpoints in the HBnB API. The tests confirm that the API properly validates input data and returns appropriate error responses when invalid data is provided.

The validation ensures that:

- ✅ Required fields are not empty
- ✉️ Email format is valid
- 💰 Price is positive
- 🌍 Latitude is between -90 and 90
- 🌎 Longitude is between -180 and 180
- ⭐ Rating is between 1 and 5
- 🔗 References to other entities (user_id, place_id) are valid

The API also correctly handles requests for non-existent resources with appropriate 404 Not Found responses.
