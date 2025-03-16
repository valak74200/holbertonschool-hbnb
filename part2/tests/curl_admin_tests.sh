#!/bin/bash
# Script to test administrator permissions using cURL

# Set the base URL for the API
BASE_URL="http://127.0.0.1:5000/api/v1"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Function to print a separator
print_separator() {
    echo -e "\n${YELLOW}=======================================================================${NC}"
    echo -e "${YELLOW}$1${NC}"
    echo -e "${YELLOW}=======================================================================${NC}\n"
}

# Function to print a success message
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

# Function to print an error message
print_error() {
    echo -e "${RED}✗ $1${NC}"
}

# Function to print a warning message
print_warning() {
    echo -e "${YELLOW}! $1${NC}"
}

# Function to register a user
register_user() {
    local email=$1
    local first_name=$2
    local last_name=$3
    local password=$4

    print_separator "REGISTERING USER: $email"
    
    echo "POST $BASE_URL/auth/register"
    echo "Request: {\"email\": \"$email\", \"first_name\": \"$first_name\", \"last_name\": \"$last_name\", \"password\": \"$password\"}"
    
    response=$(curl -s -X POST "$BASE_URL/auth/register" \
        -H "Content-Type: application/json" \
        -d "{\"email\": \"$email\", \"first_name\": \"$first_name\", \"last_name\": \"$last_name\", \"password\": \"$password\"}")
    
    echo "Response: $response"
    
    if [[ $response == *"success"* ]]; then
        print_success "User registered successfully"
        return 0
    else
        print_error "Failed to register user"
        return 1
    fi
}

# Function to login and get a JWT token
login() {
    local email=$1
    local password=$2

    print_separator "LOGGING IN: $email"
    
    echo "POST $BASE_URL/auth/login"
    echo "Request: {\"email\": \"$email\", \"password\": \"$password\"}"
    
    response=$(curl -s -X POST "$BASE_URL/auth/login" \
        -H "Content-Type: application/json" \
        -d "{\"email\": \"$email\", \"password\": \"$password\"}")
    
    token=$(echo $response | grep -o '"access_token":"[^"]*' | sed 's/"access_token":"//')
    
    if [[ -n "$token" ]]; then
        print_success "Login successful"
        echo "Token: $token"
        echo $token
        return 0
    else
        print_error "Login failed"
        echo "Response: $response"
        return 1
    fi
}

# Function to make a user an admin
make_admin() {
    local email=$1

    print_separator "MAKING USER AN ADMIN: $email"
    
    echo "This would typically be done through a database operation or an admin interface."
    echo "For testing purposes, you can use the make_admin.py script:"
    echo "cd part2 && python scripts/make_admin.py $email"
    
    print_warning "For this test, we'll assume the user has been made an admin"
}

# Function to test creating a user as an admin
test_create_user_as_admin() {
    local admin_token=$1
    local email=$2
    local first_name=$3
    local last_name=$4
    local password=$5

    print_separator "TESTING CREATE USER AS ADMIN"
    
    echo "POST $BASE_URL/users/"
    echo "Headers: {\"Authorization\": \"Bearer $admin_token\", \"Content-Type\": \"application/json\"}"
    echo "Request: {\"email\": \"$email\", \"first_name\": \"$first_name\", \"last_name\": \"$last_name\", \"password\": \"$password\"}"
    
    response=$(curl -s -X POST "$BASE_URL/users/" \
        -H "Authorization: Bearer $admin_token" \
        -H "Content-Type: application/json" \
        -d "{\"email\": \"$email\", \"first_name\": \"$first_name\", \"last_name\": \"$last_name\", \"password\": \"$password\"}")
    
    echo "Response: $response"
    
    if [[ $response == *"success"* || $response == *"id"* ]]; then
        print_success "User created successfully as admin"
        user_id=$(echo $response | grep -o '"id":"[^"]*' | sed 's/"id":"//')
        echo "User ID: $user_id"
        echo $user_id
        return 0
    else
        print_error "Failed to create user as admin"
        return 1
    fi
}

# Function to test creating a user as a regular user (should fail)
test_create_user_as_regular() {
    local regular_token=$1
    local email=$2
    local first_name=$3
    local last_name=$4
    local password=$5

    print_separator "TESTING CREATE USER AS REGULAR USER (SHOULD FAIL)"
    
    echo "POST $BASE_URL/users/"
    echo "Headers: {\"Authorization\": \"Bearer $regular_token\", \"Content-Type\": \"application/json\"}"
    echo "Request: {\"email\": \"$email\", \"first_name\": \"$first_name\", \"last_name\": \"$last_name\", \"password\": \"$password\"}"
    
    response=$(curl -s -X POST "$BASE_URL/users/" \
        -H "Authorization: Bearer $regular_token" \
        -H "Content-Type: application/json" \
        -d "{\"email\": \"$email\", \"first_name\": \"$first_name\", \"last_name\": \"$last_name\", \"password\": \"$password\"}")
    
    echo "Response: $response"
    
    if [[ $response == *"Admin privileges required"* ]]; then
        print_success "Admin privileges required (expected)"
        return 0
    else
        print_error "Unexpected response"
        return 1
    fi
}

# Function to test updating a user as an admin
test_update_user_as_admin() {
    local admin_token=$1
    local user_id=$2
    local email=$3
    local first_name=$4
    local last_name=$5
    local password=$6

    print_separator "TESTING UPDATE USER AS ADMIN"
    
    echo "PUT $BASE_URL/users/$user_id"
    echo "Headers: {\"Authorization\": \"Bearer $admin_token\", \"Content-Type\": \"application/json\"}"
    echo "Request: {\"email\": \"$email\", \"first_name\": \"$first_name\", \"last_name\": \"$last_name\", \"password\": \"$password\"}"
    
    response=$(curl -s -X PUT "$BASE_URL/users/$user_id" \
        -H "Authorization: Bearer $admin_token" \
        -H "Content-Type: application/json" \
        -d "{\"email\": \"$email\", \"first_name\": \"$first_name\", \"last_name\": \"$last_name\", \"password\": \"$password\"}")
    
    echo "Response: $response"
    
    if [[ $response == *"success"* || $response == *"id"* ]]; then
        print_success "User updated successfully as admin"
        return 0
    else
        print_error "Failed to update user as admin"
        return 1
    fi
}

# Function to test creating an amenity as an admin
test_create_amenity_as_admin() {
    local admin_token=$1
    local name=$2

    print_separator "TESTING CREATE AMENITY AS ADMIN"
    
    echo "POST $BASE_URL/amenities/"
    echo "Headers: {\"Authorization\": \"Bearer $admin_token\", \"Content-Type\": \"application/json\"}"
    echo "Request: {\"name\": \"$name\"}"
    
    response=$(curl -s -X POST "$BASE_URL/amenities/" \
        -H "Authorization: Bearer $admin_token" \
        -H "Content-Type: application/json" \
        -d "{\"name\": \"$name\"}")
    
    echo "Response: $response"
    
    if [[ $response == *"success"* || $response == *"id"* ]]; then
        print_success "Amenity created successfully as admin"
        amenity_id=$(echo $response | grep -o '"id":"[^"]*' | sed 's/"id":"//')
        echo "Amenity ID: $amenity_id"
        echo $amenity_id
        return 0
    else
        print_error "Failed to create amenity as admin"
        return 1
    fi
}

# Function to test creating an amenity as a regular user (should fail)
test_create_amenity_as_regular() {
    local regular_token=$1
    local name=$2

    print_separator "TESTING CREATE AMENITY AS REGULAR USER (SHOULD FAIL)"
    
    echo "POST $BASE_URL/amenities/"
    echo "Headers: {\"Authorization\": \"Bearer $regular_token\", \"Content-Type\": \"application/json\"}"
    echo "Request: {\"name\": \"$name\"}"
    
    response=$(curl -s -X POST "$BASE_URL/amenities/" \
        -H "Authorization: Bearer $regular_token" \
        -H "Content-Type: application/json" \
        -d "{\"name\": \"$name\"}")
    
    echo "Response: $response"
    
    if [[ $response == *"Admin privileges required"* ]]; then
        print_success "Admin privileges required (expected)"
        return 0
    else
        print_error "Unexpected response"
        return 1
    fi
}

# Function to test updating a place as an admin (not the owner)
test_update_place_as_admin() {
    local admin_token=$1
    local place_id=$2
    local title=$3
    local description=$4
    local price=$5

    print_separator "TESTING UPDATE PLACE AS ADMIN (NOT OWNER)"
    
    echo "PUT $BASE_URL/places/$place_id"
    echo "Headers: {\"Authorization\": \"Bearer $admin_token\", \"Content-Type\": \"application/json\"}"
    echo "Request: {\"title\": \"$title\", \"description\": \"$description\", \"price\": $price}"
    
    response=$(curl -s -X PUT "$BASE_URL/places/$place_id" \
        -H "Authorization: Bearer $admin_token" \
        -H "Content-Type: application/json" \
        -d "{\"title\": \"$title\", \"description\": \"$description\", \"price\": $price}")
    
    echo "Response: $response"
    
    if [[ $response == *"success"* || $response == *"message"* ]]; then
        print_success "Place updated successfully as admin (not owner)"
        return 0
    else
        print_error "Failed to update place as admin (not owner)"
        return 1
    fi
}

# Function to test updating a place as a regular user (not the owner, should fail)
test_update_place_as_regular() {
    local regular_token=$1
    local place_id=$2
    local title=$3
    local description=$4
    local price=$5

    print_separator "TESTING UPDATE PLACE AS REGULAR USER (NOT OWNER, SHOULD FAIL)"
    
    echo "PUT $BASE_URL/places/$place_id"
    echo "Headers: {\"Authorization\": \"Bearer $regular_token\", \"Content-Type\": \"application/json\"}"
    echo "Request: {\"title\": \"$title\", \"description\": \"$description\", \"price\": $price}"
    
    response=$(curl -s -X PUT "$BASE_URL/places/$place_id" \
        -H "Authorization: Bearer $regular_token" \
        -H "Content-Type: application/json" \
        -d "{\"title\": \"$title\", \"description\": \"$description\", \"price\": $price}")
    
    echo "Response: $response"
    
    if [[ $response == *"Unauthorized action"* ]]; then
        print_success "Unauthorized action (expected)"
        return 0
    else
        print_error "Unexpected response"
        return 1
    fi
}

# Function to test updating a review as an admin (not the author)
test_update_review_as_admin() {
    local admin_token=$1
    local review_id=$2
    local text=$3
    local rating=$4

    print_separator "TESTING UPDATE REVIEW AS ADMIN (NOT AUTHOR)"
    
    echo "PUT $BASE_URL/reviews/$review_id"
    echo "Headers: {\"Authorization\": \"Bearer $admin_token\", \"Content-Type\": \"application/json\"}"
    echo "Request: {\"text\": \"$text\", \"rating\": $rating}"
    
    response=$(curl -s -X PUT "$BASE_URL/reviews/$review_id" \
        -H "Authorization: Bearer $admin_token" \
        -H "Content-Type: application/json" \
        -d "{\"text\": \"$text\", \"rating\": $rating}")
    
    echo "Response: $response"
    
    if [[ $response == *"success"* || $response == *"message"* ]]; then
        print_success "Review updated successfully as admin (not author)"
        return 0
    else
        print_error "Failed to update review as admin (not author)"
        return 1
    fi
}

# Function to test updating a review as a regular user (not the author, should fail)
test_update_review_as_regular() {
    local regular_token=$1
    local review_id=$2
    local text=$3
    local rating=$4

    print_separator "TESTING UPDATE REVIEW AS REGULAR USER (NOT AUTHOR, SHOULD FAIL)"
    
    echo "PUT $BASE_URL/reviews/$review_id"
    echo "Headers: {\"Authorization\": \"Bearer $regular_token\", \"Content-Type\": \"application/json\"}"
    echo "Request: {\"text\": \"$text\", \"rating\": $rating}"
    
    response=$(curl -s -X PUT "$BASE_URL/reviews/$review_id" \
        -H "Authorization: Bearer $regular_token" \
        -H "Content-Type: application/json" \
        -d "{\"text\": \"$text\", \"rating\": $rating}")
    
    echo "Response: $response"
    
    if [[ $response == *"Unauthorized action"* ]]; then
        print_success "Unauthorized action (expected)"
        return 0
    else
        print_error "Unexpected response"
        return 1
    fi
}

# Function to test deleting a review as an admin (not the author)
test_delete_review_as_admin() {
    local admin_token=$1
    local review_id=$2

    print_separator "TESTING DELETE REVIEW AS ADMIN (NOT AUTHOR)"
    
    echo "DELETE $BASE_URL/reviews/$review_id"
    echo "Headers: {\"Authorization\": \"Bearer $admin_token\"}"
    
    response=$(curl -s -X DELETE "$BASE_URL/reviews/$review_id" \
        -H "Authorization: Bearer $admin_token")
    
    echo "Response: $response"
    
    if [[ $response == *"success"* || $response == *"message"* ]]; then
        print_success "Review deleted successfully as admin (not author)"
        return 0
    else
        print_error "Failed to delete review as admin (not author)"
        return 1
    fi
}

# Function to test deleting a review as a regular user (not the author, should fail)
test_delete_review_as_regular() {
    local regular_token=$1
    local review_id=$2

    print_separator "TESTING DELETE REVIEW AS REGULAR USER (NOT AUTHOR, SHOULD FAIL)"
    
    echo "DELETE $BASE_URL/reviews/$review_id"
    echo "Headers: {\"Authorization\": \"Bearer $regular_token\"}"
    
    response=$(curl -s -X DELETE "$BASE_URL/reviews/$review_id" \
        -H "Authorization: Bearer $regular_token")
    
    echo "Response: $response"
    
    if [[ $response == *"Unauthorized action"* ]]; then
        print_success "Unauthorized action (expected)"
        return 0
    else
        print_error "Unexpected response"
        return 1
    fi
}

# Main function to run all tests
main() {
    # Register an admin user
    register_user "admin@example.com" "Admin" "User" "password123"
    
    # Register a regular user
    register_user "regular@example.com" "Regular" "User" "password123"
    
    # Make the admin user an admin
    make_admin "admin@example.com"
    
    # Login as admin
    admin_token=$(login "admin@example.com" "password123")
    
    # Login as regular user
    regular_token=$(login "regular@example.com" "password123")
    
    # Test creating a user as an admin
    test_create_user_as_admin "$admin_token" "newuser@example.com" "New" "User" "password123"
    
    # Test creating a user as a regular user (should fail)
    test_create_user_as_regular "$regular_token" "anotheruser@example.com" "Another" "User" "password123"
    
    # Get user IDs
    response=$(curl -s -X GET "$BASE_URL/users/")
    regular_user_id=$(echo $response | grep -o '"id":"[^"]*' | sed 's/"id":"//' | head -1)
    
    # Test updating a user as an admin
    print_separator "TESTING UPDATE USER AS ADMIN"
    echo "PUT $BASE_URL/users/$regular_user_id"
    echo "Headers: {\"Authorization\": \"Bearer $admin_token\", \"Content-Type\": \"application/json\"}"
    echo "Request: {\"email\": \"updatedemail@example.com\"}"
    
    response=$(curl -s -X PUT "$BASE_URL/users/$regular_user_id" \
        -H "Authorization: Bearer $admin_token" \
        -H "Content-Type: application/json" \
        -d "{\"email\": \"updatedemail@example.com\"}")
    
    echo "Response: $response"
    
    # Test creating an amenity as an admin
    print_separator "TESTING AMENITY CREATION AS ADMIN"
    echo "POST $BASE_URL/amenities/"
    echo "Headers: {\"Authorization\": \"Bearer $admin_token\", \"Content-Type\": \"application/json\"}"
    echo "Request: {\"name\": \"Swimming Pool\"}"
    
    response=$(curl -s -X POST "$BASE_URL/amenities/" \
        -H "Authorization: Bearer $admin_token" \
        -H "Content-Type: application/json" \
        -d "{\"name\": \"Swimming Pool\"}")
    
    echo "Response: $response"
    amenity_id=$(echo $response | grep -o '"id":"[^"]*' | sed 's/"id":"//')
    
    # Test updating an amenity as an admin
    print_separator "TESTING AMENITY UPDATE AS ADMIN"
    echo "PUT $BASE_URL/amenities/$amenity_id"
    echo "Headers: {\"Authorization\": \"Bearer $admin_token\", \"Content-Type\": \"application/json\"}"
    echo "Request: {\"name\": \"Updated Amenity\"}"
    
    response=$(curl -s -X PUT "$BASE_URL/amenities/$amenity_id" \
        -H "Authorization: Bearer $admin_token" \
        -H "Content-Type: application/json" \
        -d "{\"name\": \"Updated Amenity\"}")
    
    echo "Response: $response"
    
    # Test creating an amenity as a regular user (should fail)
    test_create_amenity_as_regular "$regular_token" "Another Amenity"
    
    # Note: The following tests require existing place and review IDs
    # You would need to create these first or use known IDs
    
    # Test updating a place as an admin (not the owner)
    # test_update_place_as_admin "$admin_token" "place_id" "Updated Title" "Updated Description" 200
    
    # Test updating a place as a regular user (not the owner, should fail)
    # test_update_place_as_regular "$regular_token" "place_id" "Updated Title" "Updated Description" 200
    
    # Test updating a review as an admin (not the author)
    # test_update_review_as_admin "$admin_token" "review_id" "Updated Review" 4
    
    # Test updating a review as a regular user (not the author, should fail)
    # test_update_review_as_regular "$regular_token" "review_id" "Updated Review" 4
    
    # Test deleting a review as an admin (not the author)
    # test_delete_review_as_admin "$admin_token" "review_id"
    
    # Test deleting a review as a regular user (not the author, should fail)
    # test_delete_review_as_regular "$regular_token" "review_id"
}

# Run the main function
main
