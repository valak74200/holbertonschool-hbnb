#!/bin/bash

# Test script for entity mappings using cURL
# This script tests CRUD operations for all entities: User, Place, Amenity, Review

# Redirect output to a file
exec > entity_mappings_test_output.txt 2>&1

# Set the base URL
BASE_URL="http://localhost:5000/api/v1"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print section headers
print_header() {
    echo -e "\n${BLUE}==== $1 ====${NC}\n"
}

# Function to print success messages
print_success() {
    echo -e "${GREEN}SUCCESS: $1${NC}"
}

# Function to print error messages
print_error() {
    echo -e "${RED}ERROR: $1${NC}"
}

# Store tokens and IDs
USER_TOKEN=""
ADMIN_TOKEN=""
USER_ID=""
PLACE_ID=""
AMENITY_ID=""
REVIEW_ID=""

# ===== USER TESTS =====
print_header "TESTING USER ENTITY"

# Create a user
print_header "Creating a user"
TIMESTAMP=$(date +%s)
USER_RESPONSE=$(curl -s -X POST "${BASE_URL}/users/" \
    -H "Content-Type: application/json" \
    -d '{
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe.'${TIMESTAMP}'@example.com",
        "password": "password123"
    }')

echo $USER_RESPONSE
USER_ID=$(echo $USER_RESPONSE | grep -o '"id"[ ]*:[ ]*"[^"]*' | sed 's/"id"[ ]*:[ ]*"//' | sed 's/"$//')

if [ -n "$USER_ID" ]; then
    print_success "User created with ID: $USER_ID"
else
    # Try alternative format
    USER_ID=$(echo $USER_RESPONSE | grep -o '"id"[ ]*:[ ]*"[^"]*"' | sed 's/"id"[ ]*:[ ]*"//' | sed 's/"$//')
    
    if [ -n "$USER_ID" ]; then
        print_success "User created with ID: $USER_ID"
    else
        print_error "Failed to create user"
        print_error "Response was: $USER_RESPONSE"
        exit 1
    fi
fi

# Login as the user
print_header "Logging in as user"
LOGIN_RESPONSE=$(curl -s -X POST "${BASE_URL}/auth/login" \
    -H "Content-Type: application/json" \
    -d '{
        "email": "john.doe.'${TIMESTAMP}'@example.com",
        "password": "password123"
    }')

echo $LOGIN_RESPONSE
USER_TOKEN=$(echo $LOGIN_RESPONSE | grep -o '"access_token"[ ]*:[ ]*"[^"]*' | sed 's/"access_token"[ ]*:[ ]*"//' | sed 's/"$//')

if [ -n "$USER_TOKEN" ]; then
    print_success "User logged in successfully. Token: $USER_TOKEN"
else
    # Try alternative format
    USER_TOKEN=$(echo $LOGIN_RESPONSE | grep -o '"access_token"[ ]*:[ ]*"[^"]*"' | sed 's/"access_token"[ ]*:[ ]*"//' | sed 's/"$//')
    
    if [ -n "$USER_TOKEN" ]; then
        print_success "User logged in successfully. Token: $USER_TOKEN"
    else
        print_error "Failed to login as user"
        print_error "Response was: $LOGIN_RESPONSE"
        exit 1
    fi
fi

# Get user details
print_header "Getting user details"
USER_DETAILS=$(curl -s -X GET "${BASE_URL}/users/${USER_ID}" \
    -H "Authorization: Bearer ${USER_TOKEN}")

echo $USER_DETAILS

# Update user
print_header "Updating user"
UPDATE_USER_RESPONSE=$(curl -s -X PUT "${BASE_URL}/users/${USER_ID}" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer ${USER_TOKEN}" \
    -d '{
        "first_name": "Johnny",
        "last_name": "Doe"
    }')

echo $UPDATE_USER_RESPONSE

# Get all users
print_header "Getting all users"
ALL_USERS=$(curl -s -X GET "${BASE_URL}/users/")

echo $ALL_USERS

# ===== AMENITY TESTS =====
print_header "TESTING AMENITY ENTITY"

# Create an amenity
print_header "Creating an amenity"
AMENITY_RESPONSE=$(curl -s -X POST "${BASE_URL}/amenities/" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer ${USER_TOKEN}" \
    -d '{
        "name": "WiFi"
    }')

echo $AMENITY_RESPONSE
AMENITY_ID=$(echo $AMENITY_RESPONSE | grep -o '"id"[ ]*:[ ]*"[^"]*' | sed 's/"id"[ ]*:[ ]*"//' | sed 's/"$//')

if [ -n "$AMENITY_ID" ]; then
    print_success "Amenity created with ID: $AMENITY_ID"
else
    # Try alternative format
    AMENITY_ID=$(echo $AMENITY_RESPONSE | grep -o '"id"[ ]*:[ ]*"[^"]*"' | sed 's/"id"[ ]*:[ ]*"//' | sed 's/"$//')
    
    if [ -n "$AMENITY_ID" ]; then
        print_success "Amenity created with ID: $AMENITY_ID"
    else
        print_error "Failed to create amenity"
        print_error "Response was: $AMENITY_RESPONSE"
        exit 1
    fi
fi

# Get amenity details
print_header "Getting amenity details"
AMENITY_DETAILS=$(curl -s -X GET "${BASE_URL}/amenities/${AMENITY_ID}")

echo $AMENITY_DETAILS

# Update amenity
print_header "Updating amenity"
UPDATE_AMENITY_RESPONSE=$(curl -s -X PUT "${BASE_URL}/amenities/${AMENITY_ID}" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer ${USER_TOKEN}" \
    -d '{
        "name": "High-Speed WiFi"
    }')

echo $UPDATE_AMENITY_RESPONSE

# Get all amenities
print_header "Getting all amenities"
ALL_AMENITIES=$(curl -s -X GET "${BASE_URL}/amenities/")

echo $ALL_AMENITIES

# ===== PLACE TESTS =====
print_header "TESTING PLACE ENTITY"

# Create a place
print_header "Creating a place"
PLACE_RESPONSE=$(curl -s -X POST "${BASE_URL}/places/" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer ${USER_TOKEN}" \
    -d '{
        "title": "Cozy Apartment",
        "description": "A beautiful apartment in the heart of the city",
        "price": 100.0,
        "latitude": 48.8566,
        "longitude": 2.3522,
        "owner_id": "'${USER_ID}'",
        "amenities": ["'${AMENITY_ID}'"]
    }')

echo $PLACE_RESPONSE
PLACE_ID=$(echo $PLACE_RESPONSE | grep -o '"id"[ ]*:[ ]*"[^"]*' | sed 's/"id"[ ]*:[ ]*"//' | sed 's/"$//')

if [ -n "$PLACE_ID" ]; then
    print_success "Place created with ID: $PLACE_ID"
else
    # Try alternative format
    PLACE_ID=$(echo $PLACE_RESPONSE | grep -o '"id"[ ]*:[ ]*"[^"]*"' | sed 's/"id"[ ]*:[ ]*"//' | sed 's/"$//')
    
    if [ -n "$PLACE_ID" ]; then
        print_success "Place created with ID: $PLACE_ID"
    else
        print_error "Failed to create place"
        print_error "Response was: $PLACE_RESPONSE"
        exit 1
    fi
fi

# Get place details
print_header "Getting place details"
PLACE_DETAILS=$(curl -s -X GET "${BASE_URL}/places/${PLACE_ID}")

echo $PLACE_DETAILS

# Update place
print_header "Updating place"
UPDATE_PLACE_RESPONSE=$(curl -s -X PUT "${BASE_URL}/places/${PLACE_ID}" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer ${USER_TOKEN}" \
    -d '{
        "title": "Luxury Apartment",
        "price": 150.0
    }')

echo $UPDATE_PLACE_RESPONSE

# Get all places
print_header "Getting all places"
ALL_PLACES=$(curl -s -X GET "${BASE_URL}/places/")

echo $ALL_PLACES

# ===== CREATE SECOND USER FOR REVIEW TESTS =====
print_header "Creating a second user for review tests"
SECOND_USER_RESPONSE=$(curl -s -X POST "${BASE_URL}/users/" \
    -H "Content-Type: application/json" \
    -d '{
        "first_name": "Jane",
        "last_name": "Smith",
        "email": "jane.smith.'${TIMESTAMP}'@example.com",
        "password": "password456"
    }')

echo $SECOND_USER_RESPONSE
SECOND_USER_ID=$(echo $SECOND_USER_RESPONSE | grep -o '"id"[ ]*:[ ]*"[^"]*' | sed 's/"id"[ ]*:[ ]*"//' | sed 's/"$//')

if [ -n "$SECOND_USER_ID" ]; then
    print_success "Second user created with ID: $SECOND_USER_ID"
else
    # Try alternative format
    SECOND_USER_ID=$(echo $SECOND_USER_RESPONSE | grep -o '"id"[ ]*:[ ]*"[^"]*"' | sed 's/"id"[ ]*:[ ]*"//' | sed 's/"$//')
    
    if [ -n "$SECOND_USER_ID" ]; then
        print_success "Second user created with ID: $SECOND_USER_ID"
    else
        print_error "Failed to create second user"
        print_error "Response was: $SECOND_USER_RESPONSE"
        exit 1
    fi
fi

# Login as the second user
print_header "Logging in as second user"
SECOND_LOGIN_RESPONSE=$(curl -s -X POST "${BASE_URL}/auth/login" \
    -H "Content-Type: application/json" \
    -d '{
        "email": "jane.smith.'${TIMESTAMP}'@example.com",
        "password": "password456"
    }')

echo $SECOND_LOGIN_RESPONSE
SECOND_USER_TOKEN=$(echo $SECOND_LOGIN_RESPONSE | grep -o '"access_token"[ ]*:[ ]*"[^"]*' | sed 's/"access_token"[ ]*:[ ]*"//' | sed 's/"$//')

if [ -n "$SECOND_USER_TOKEN" ]; then
    print_success "Second user logged in successfully. Token: $SECOND_USER_TOKEN"
else
    # Try alternative format
    SECOND_USER_TOKEN=$(echo $SECOND_LOGIN_RESPONSE | grep -o '"access_token"[ ]*:[ ]*"[^"]*"' | sed 's/"access_token"[ ]*:[ ]*"//' | sed 's/"$//')
    
    if [ -n "$SECOND_USER_TOKEN" ]; then
        print_success "Second user logged in successfully. Token: $SECOND_USER_TOKEN"
    else
        print_error "Failed to login as second user"
        print_error "Response was: $SECOND_LOGIN_RESPONSE"
        exit 1
    fi
fi

# ===== REVIEW TESTS =====
print_header "TESTING REVIEW ENTITY"

# Create a review (using the second user to review the place created by the first user)
print_header "Creating a review"
REVIEW_RESPONSE=$(curl -s -X POST "${BASE_URL}/reviews/" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer ${SECOND_USER_TOKEN}" \
    -d '{
        "text": "Great place to stay!",
        "rating": 5,
        "user_id": "'${SECOND_USER_ID}'",
        "place_id": "'${PLACE_ID}'"
    }')

echo $REVIEW_RESPONSE
REVIEW_ID=$(echo $REVIEW_RESPONSE | grep -o '"id"[ ]*:[ ]*"[^"]*' | sed 's/"id"[ ]*:[ ]*"//' | sed 's/"$//')

if [ -n "$REVIEW_ID" ]; then
    print_success "Review created with ID: $REVIEW_ID"
else
    # Try alternative format
    REVIEW_ID=$(echo $REVIEW_RESPONSE | grep -o '"id"[ ]*:[ ]*"[^"]*"' | sed 's/"id"[ ]*:[ ]*"//' | sed 's/"$//')
    
    if [ -n "$REVIEW_ID" ]; then
        print_success "Review created with ID: $REVIEW_ID"
    else
        print_error "Failed to create review"
        print_error "Response was: $REVIEW_RESPONSE"
        exit 1
    fi
fi

# Get review details
print_header "Getting review details"
REVIEW_DETAILS=$(curl -s -X GET "${BASE_URL}/reviews/${REVIEW_ID}")

echo $REVIEW_DETAILS

# Update review
print_header "Updating review"
UPDATE_REVIEW_RESPONSE=$(curl -s -X PUT "${BASE_URL}/reviews/${REVIEW_ID}" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer ${SECOND_USER_TOKEN}" \
    -d '{
        "text": "Amazing place to stay!",
        "rating": 5
    }')

echo $UPDATE_REVIEW_RESPONSE

# Get all reviews
print_header "Getting all reviews"
ALL_REVIEWS=$(curl -s -X GET "${BASE_URL}/reviews/")

echo $ALL_REVIEWS

# Get reviews for a specific place
print_header "Getting reviews for place"
PLACE_REVIEWS=$(curl -s -X GET "${BASE_URL}/places/${PLACE_ID}/reviews")

echo $PLACE_REVIEWS

# Delete review
print_header "Deleting review"
DELETE_REVIEW_RESPONSE=$(curl -s -X DELETE "${BASE_URL}/reviews/${REVIEW_ID}" \
    -H "Authorization: Bearer ${SECOND_USER_TOKEN}")

echo $DELETE_REVIEW_RESPONSE

print_header "ENTITY MAPPING TESTS COMPLETED"

# Print a message to the console
echo "Test completed. Results written to entity_mappings_test_output.txt"
