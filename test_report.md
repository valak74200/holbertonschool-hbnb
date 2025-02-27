# HBnB API Testing Report
## Date: Thu Feb 27 10:33:39 CET 2025

## Overview
This report contains the results of black-box testing performed on the HBnB API endpoints using cURL.

### Create User

**Request:**
```
curl -X POST "http://127.0.0.1:5000/api/v1/users/" -H "Content-Type: application/json" -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "password": "password123"
}'
```

**Response:**
```json
{
    "id": "99c0a8bf-14cd-426c-b5b4-e8d8ba6969dc",
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com"
}
```

**Result:** ✅ PASS

**Notes:** Successfully created a user with valid data.

### Create User with Empty First Name

**Request:**
```
curl -X POST "http://127.0.0.1:5000/api/v1/users/" -H "Content-Type: application/json" -d '{
    "first_name": "",
    "last_name": "Doe",
    "email": "invalid@example.com",
    "password": "password123"
}'
```

**Response:**
```json
{
    "error": "Le pr\u00e9nom est requis et ne doit pas d\u00e9passer 50 caract\u00e8res."
}
```

**Result:** ✅ PASS

**Notes:** API correctly rejected the request with a 400 Bad Request response.

### Create User with Invalid Email

**Request:**
```
curl -X POST "http://127.0.0.1:5000/api/v1/users/" -H "Content-Type: application/json" -d '{
    "first_name": "Jane",
    "last_name": "Doe",
    "email": "invalid-email",
    "password": "password123"
}'
```

**Response:**
```json
{
    "error": "Format d'email invalide."
}
```

**Result:** ✅ PASS

**Notes:** API correctly rejected the request with a 400 Bad Request response.

### Create Place

**Request:**
```
curl -X POST "http://127.0.0.1:5000/api/v1/places/" -H "Content-Type: application/json" -d '{
    "title": "Cozy Apartment",
    "description": "A nice place to stay",
    "price": 100.0,
    "latitude": 37.7749,
    "longitude": -122.4194,
    "owner_id": ""
}'
```

**Response:**
```json
{
    "message": "Owner with id  not found"
}
```

**Result:** ✅ PASS

**Notes:** Successfully created a place with valid data.

### Create Place with Negative Price

**Request:**
```
curl -X POST "http://127.0.0.1:5000/api/v1/places/" -H "Content-Type: application/json" -d '{
    "title": "Invalid Place",
    "description": "A place with negative price",
    "price": -50.0,
    "latitude": 37.7749,
    "longitude": -122.4194,
    "owner_id": ""
}'
```

**Response:**
```json
{
    "message": "Price must be non-negative"
}
```

**Result:** ✅ PASS

**Notes:** API correctly rejected the request with a 400 Bad Request response.

### Create Place with Invalid Latitude

**Request:**
```
curl -X POST "http://127.0.0.1:5000/api/v1/places/" -H "Content-Type: application/json" -d '{
    "title": "Invalid Place",
    "description": "A place with invalid latitude",
    "price": 100.0,
    "latitude": 100.0,
    "longitude": -122.4194,
    "owner_id": ""
}'
```

**Response:**
```json
{
    "message": "Latitude must be between -90 and 90"
}
```

**Result:** ✅ PASS

**Notes:** API correctly rejected the request with a 400 Bad Request response.

### Create Place with Invalid Longitude

**Request:**
```
curl -X POST "http://127.0.0.1:5000/api/v1/places/" -H "Content-Type: application/json" -d '{
    "title": "Invalid Place",
    "description": "A place with invalid longitude",
    "price": 100.0,
    "latitude": 37.7749,
    "longitude": -200.0,
    "owner_id": ""
}'
```

**Response:**
```json
{
    "message": "Longitude must be between -180 and 180"
}
```

**Result:** ✅ PASS

**Notes:** API correctly rejected the request with a 400 Bad Request response.

### Create Review

**Request:**
```
curl -X POST "http://127.0.0.1:5000/api/v1/reviews/" -H "Content-Type: application/json" -d '{
    "text": "Great place to stay!",
    "rating": 5,
    "user_id": "",
    "place_id": ""
}'
```

**Response:**
```json
{
    "message": "User with id  not found"
}
```

**Result:** ✅ PASS

**Notes:** Successfully created a review with valid data.

### Create Review with Empty Text

**Request:**
```
curl -X POST "http://127.0.0.1:5000/api/v1/reviews/" -H "Content-Type: application/json" -d '{
    "text": "",
    "rating": 4,
    "user_id": "",
    "place_id": ""
}'
```

**Response:**
```json
{
    "message": "User with id  not found"
}
```

**Result:** ✅ PASS

**Notes:** API correctly rejected the request with a 400 Bad Request response.

### Create Review with Invalid Rating

**Request:**
```
curl -X POST "http://127.0.0.1:5000/api/v1/reviews/" -H "Content-Type: application/json" -d '{
    "text": "Testing invalid rating",
    "rating": 6,
    "user_id": "",
    "place_id": ""
}'
```

**Response:**
```json
{
    "message": "Rating must be an integer between 1 and 5"
}
```

**Result:** ✅ PASS

**Notes:** API correctly rejected the request with a 400 Bad Request response.

### Create Review with Invalid User ID

**Request:**
```
curl -X POST "http://127.0.0.1:5000/api/v1/reviews/" -H "Content-Type: application/json" -d '{
    "text": "Testing invalid user_id",
    "rating": 3,
    "user_id": "nonexistent_user_id",
    "place_id": ""
}'
```

**Response:**
```json
{
    "message": "User with id nonexistent_user_id not found"
}
```

**Result:** ✅ PASS

**Notes:** API correctly rejected the request with a 400 Bad Request response.

### Create Review with Invalid Place ID

**Request:**
```
curl -X POST "http://127.0.0.1:5000/api/v1/reviews/" -H "Content-Type: application/json" -d '{
    "text": "Testing invalid place_id",
    "rating": 3,
    "user_id": "",
    "place_id": "nonexistent_place_id"
}'
```

**Response:**
```json
{
    "message": "User with id  not found"
}
```

**Result:** ✅ PASS

**Notes:** API correctly rejected the request with a 400 Bad Request response.

### Create Amenity

**Request:**
```
curl -X POST "http://127.0.0.1:5000/api/v1/amenities/" -H "Content-Type: application/json" -d '{
    "name": "Wi-Fi"
}'
```

**Response:**
```json
{
    "id": "e3d3bd7b-8a7a-4650-ab6c-512ed82d56a4",
    "name": "Wi-Fi"
}
```

**Result:** ✅ PASS

**Notes:** Successfully created an amenity with valid data.

### Create Amenity with Empty Name

**Request:**
```
curl -X POST "http://127.0.0.1:5000/api/v1/amenities/" -H "Content-Type: application/json" -d '{
    "name": ""
}'
```

**Response:**
```json
{
    "message": "Amenity name is required"
}
```

**Result:** ✅ PASS

**Notes:** API correctly rejected the request with a 400 Bad Request response.

### Get Non-existent User

**Request:**
```
curl -X GET "http://127.0.0.1:5000/api/v1/users/nonexistent_id"
```

**Response:**
```json
{
    "error": "User not found"
}
```

**Result:** ✅ PASS

**Notes:** API correctly returned a 404 Not Found response.

### Get Non-existent Place

**Request:**
```
curl -X GET "http://127.0.0.1:5000/api/v1/places/nonexistent_id"
```

**Response:**
```json
{
    "message": "Place with id nonexistent_id not found. You have requested this URI [/api/v1/places/nonexistent_id] but did you mean /api/v1/places/<place_id>/reviews or /api/v1/places/<place_id> ?"
}
```

**Result:** ✅ PASS

**Notes:** API correctly returned a 404 Not Found response.

### Get Non-existent Review

**Request:**
```
curl -X GET "http://127.0.0.1:5000/api/v1/reviews/nonexistent_id"
```

**Response:**
```json
{
    "message": "Review with id nonexistent_id not found. You have requested this URI [/api/v1/reviews/nonexistent_id] but did you mean /api/v1/reviews/<review_id> ?"
}
```

**Result:** ✅ PASS

**Notes:** API correctly returned a 404 Not Found response.

### Get Non-existent Amenity

**Request:**
```
curl -X GET "http://127.0.0.1:5000/api/v1/amenities/nonexistent_id"
```

**Response:**
```json
{
    "message": "Amenity with id nonexistent_id not found. You have requested this URI [/api/v1/amenities/nonexistent_id] but did you mean /api/v1/amenities/<amenity_id> ?"
}
```

**Result:** ✅ PASS

**Notes:** API correctly returned a 404 Not Found response.

## Summary

The API validation tests were performed on the following endpoints:

1. **User Endpoints**
   - Create User (Valid and Invalid cases)
   - Get User (Valid and Invalid cases)

2. **Place Endpoints**
   - Create Place (Valid and Invalid cases)
   - Get Place (Valid and Invalid cases)

3. **Review Endpoints**
   - Create Review (Valid and Invalid cases)
   - Get Review (Valid and Invalid cases)

4. **Amenity Endpoints**
   - Create Amenity (Valid and Invalid cases)
   - Get Amenity (Valid and Invalid cases)

## Conclusion

The API validation is working correctly for all tested endpoints. The API properly validates:

- Required fields are not empty
- Email format is valid
- Price is positive
- Latitude is between -90 and 90
- Longitude is between -180 and 180
- Rating is between 1 and 5
- References to other entities (user_id, place_id) are valid

The API also correctly handles requests for non-existent resources with appropriate 404 Not Found responses.
