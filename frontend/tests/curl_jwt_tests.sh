#!/bin/bash

# Script to test JWT authentication using curl

# Set colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Base URL for the API
BASE_URL="http://127.0.0.1:5000/api/v1"

# Function to print section headers
print_header() {
    echo -e "\n${YELLOW}========================================================================"
    echo -e "                         $1                         "
    echo -e "========================================================================${NC}\n"
}

# Function to print response
print_response() {
    if [ $1 -eq 200 ] || [ $1 -eq 201 ]; then
        echo -e "${GREEN}Response ($1):${NC}"
    else
        echo -e "${RED}Response ($1):${NC}"
    fi
    echo "$2"
    echo ""
}

# Create a unique email for testing
EMAIL="test.user.$(date +%s)@example.com"
PASSWORD="password123"
TOKEN=""
USER_ID=""
PLACE_ID=""
REVIEW_ID=""
AMENITY_ID=""

# 1. Create a user
print_header "CREATING TEST USER"
echo "POST ${BASE_URL}/users/"
echo "Request: {\"first_name\": \"Test\", \"last_name\": \"User\", \"email\": \"${EMAIL}\", \"password\": \"${PASSWORD}\"}"

RESPONSE=$(curl -s -X POST "${BASE_URL}/users/" \
    -H "Content-Type: application/json" \
    -d '{"first_name": "Test", "last_name": "User", "email": "'${EMAIL}'", "password": "'${PASSWORD}'"}')

HTTP_STATUS=$(echo "$RESPONSE" | grep -o '"id":"[^"]*"' | cut -d'"' -f4)
if [ -n "$HTTP_STATUS" ] && [ "$HTTP_STATUS" != "null" ]; then
    USER_ID=$HTTP_STATUS
    print_response 201 "$RESPONSE"
    echo -e "${GREEN}✅ User created successfully with ID: ${USER_ID}${NC}"
else
    print_response 400 "$RESPONSE"
    echo -e "${RED}❌ Failed to create user${NC}"
    exit 1
fi

# 2. Login to get JWT token
print_header "LOGGING IN"
echo "POST ${BASE_URL}/auth/login"
echo "Request: {\"email\": \"${EMAIL}\", \"password\": \"${PASSWORD}\"}"

RESPONSE=$(curl -s -X POST "${BASE_URL}/auth/login" \
    -H "Content-Type: application/json" \
    -d "{\"email\": \"${EMAIL}\", \"password\": \"${PASSWORD}\"}")

TOKEN=$(echo "$RESPONSE" | grep -o '"access_token":"[^"]*"' | cut -d'"' -f4)
if [ -n "$TOKEN" ] && [ "$TOKEN" != "null" ]; then
    echo -e "${GREEN}Response (200): {\"access_token\": \"...token truncated...\"} ${NC}"
    echo -e "${GREEN}✅ Login successful${NC}"
else
    print_response 401 "$RESPONSE"
    echo -e "${RED}❌ Login failed${NC}"
    exit 1
fi

# 3. Test accessing a protected endpoint
print_header "ACCESSING PROTECTED ENDPOINT"
echo "GET ${BASE_URL}/auth/protected"
echo "Headers: {\"Authorization\": \"Bearer ...token truncated...\"}"

RESPONSE=$(curl -s -X GET "${BASE_URL}/auth/protected" \
    -H "Authorization: Bearer ${TOKEN}")

print_response 200 "$RESPONSE"

# 4. Test creating a place (authenticated)
print_header "CREATING A PLACE (AUTHENTICATED)"
echo "POST ${BASE_URL}/places/"
echo "Headers: {\"Authorization\": \"Bearer ...token truncated...\"}"
echo "Request: {\"title\": \"Test Place\", \"description\": \"A test place\", \"price\": 100, \"latitude\": 37.7749, \"longitude\": -122.4194}"

RESPONSE=$(curl -s -X POST "${BASE_URL}/places/" \
    -H "Authorization: Bearer ${TOKEN}" \
    -H "Content-Type: application/json" \
    -d "{\"title\": \"Test Place\", \"description\": \"A test place\", \"price\": 100, \"latitude\": 37.7749, \"longitude\": -122.4194, \"owner_id\": \"${USER_ID}\"}")

PLACE_ID=$(echo "$RESPONSE" | grep -o '"id":"[^"]*"' | cut -d'"' -f4)
if [ -n "$PLACE_ID" ] && [ "$PLACE_ID" != "null" ]; then
    print_response 201 "$RESPONSE"
    echo -e "${GREEN}✅ Place created successfully with ID: ${PLACE_ID}${NC}"
else
    print_response 400 "$RESPONSE"
    echo -e "${RED}❌ Failed to create place${NC}"
    exit 1
fi

# 5. Test creating a place without authentication (should fail)
print_header "CREATING A PLACE (UNAUTHENTICATED)"
echo "POST ${BASE_URL}/places/"
echo "Request: {\"title\": \"Unauthenticated Place\", \"description\": \"This should fail\", \"price\": 100, \"latitude\": 37.7749, \"longitude\": -122.4194}"

RESPONSE=$(curl -s -X POST "${BASE_URL}/places/" \
    -H "Content-Type: application/json" \
    -d "{\"title\": \"Unauthenticated Place\", \"description\": \"This should fail\", \"price\": 100, \"latitude\": 37.7749, \"longitude\": -122.4194}")

print_response 401 "$RESPONSE"
if [[ "$RESPONSE" == *"Unauthorized"* ]]; then
    echo -e "${GREEN}✅ Authentication required (expected)${NC}"
else
    echo -e "${RED}❌ Unexpected response${NC}"
fi

# 6. Test updating a place (authenticated, owner)
print_header "UPDATING A PLACE (AUTHENTICATED, OWNER)"
echo "PUT ${BASE_URL}/places/${PLACE_ID}"
echo "Headers: {\"Authorization\": \"Bearer ...token truncated...\"}"
echo "Request: {\"title\": \"Updated Test Place\", \"description\": \"An updated test place\", \"price\": 150}"

RESPONSE=$(curl -s -X PUT "${BASE_URL}/places/${PLACE_ID}" \
    -H "Authorization: Bearer ${TOKEN}" \
    -H "Content-Type: application/json" \
    -d "{\"title\": \"Updated Test Place\", \"description\": \"An updated test place\", \"price\": 150}")

print_response 200 "$RESPONSE"
if [[ "$RESPONSE" == *"Updated Test Place"* ]]; then
    echo -e "${GREEN}✅ Place updated successfully${NC}"
else
    echo -e "${RED}❌ Failed to update place${NC}"
fi

# 7. Test getting all places (public)
print_header "GETTING ALL PLACES (PUBLIC)"
echo "GET ${BASE_URL}/places/"

RESPONSE=$(curl -s -X GET "${BASE_URL}/places/")

print_response 200 "$RESPONSE"
echo -e "${GREEN}✅ Places retrieved successfully${NC}"

# 8. Test getting a specific place (public)
print_header "GETTING A SPECIFIC PLACE (PUBLIC)"
echo "GET ${BASE_URL}/places/${PLACE_ID}"

RESPONSE=$(curl -s -X GET "${BASE_URL}/places/${PLACE_ID}")

print_response 200 "$RESPONSE"
if [[ "$RESPONSE" == *"Updated Test Place"* ]]; then
    echo -e "${GREEN}✅ Place retrieved successfully${NC}"
else
    echo -e "${RED}❌ Failed to retrieve place${NC}"
fi

# 9. Test creating an amenity (authenticated)
print_header "CREATING AN AMENITY (AUTHENTICATED)"
echo "POST ${BASE_URL}/amenities/"
echo "Headers: {\"Authorization\": \"Bearer ...token truncated...\"}"
echo "Request: {\"name\": \"Test Amenity\"}"

RESPONSE=$(curl -s -X POST "${BASE_URL}/amenities/" \
    -H "Authorization: Bearer ${TOKEN}" \
    -H "Content-Type: application/json" \
    -d "{\"name\": \"Test Amenity\"}")

AMENITY_ID=$(echo "$RESPONSE" | grep -o '"id":"[^"]*"' | cut -d'"' -f4)
if [ -n "$AMENITY_ID" ] && [ "$AMENITY_ID" != "null" ]; then
    print_response 201 "$RESPONSE"
    echo -e "${GREEN}✅ Amenity created successfully with ID: ${AMENITY_ID}${NC}"
else
    print_response 400 "$RESPONSE"
    echo -e "${RED}❌ Failed to create amenity${NC}"
fi

# 10. Test creating a review (authenticated)
print_header "CREATING A REVIEW (AUTHENTICATED)"
echo "POST ${BASE_URL}/reviews/"
echo "Headers: {\"Authorization\": \"Bearer ...token truncated...\"}"
echo "Request: {\"text\": \"This is a test review\", \"rating\": 5, \"place_id\": \"${PLACE_ID}\"}"

# Create a second user to create a review (since users can't review their own places)
SECOND_EMAIL="test.user.2.$(date +%s)@example.com"
SECOND_PASSWORD="password123"

echo -e "${YELLOW}Creating a second user to test reviews...${NC}"
RESPONSE=$(curl -s -X POST "${BASE_URL}/users/" \
    -H "Content-Type: application/json" \
    -d "{\"first_name\": \"Test\", \"last_name\": \"User2\", \"email\": \"${SECOND_EMAIL}\", \"password\": \"${SECOND_PASSWORD}\"}")

SECOND_USER_ID=$(echo "$RESPONSE" | grep -o '"id":"[^"]*"' | cut -d'"' -f4)
if [ -n "$SECOND_USER_ID" ] && [ "$SECOND_USER_ID" != "null" ]; then
    echo -e "${GREEN}✅ Second user created successfully${NC}"
else
    echo -e "${RED}❌ Failed to create second user${NC}"
    exit 1
fi

echo -e "${YELLOW}Logging in as second user...${NC}"
RESPONSE=$(curl -s -X POST "${BASE_URL}/auth/login" \
    -H "Content-Type: application/json" \
    -d "{\"email\": \"${SECOND_EMAIL}\", \"password\": \"${SECOND_PASSWORD}\"}")

SECOND_TOKEN=$(echo "$RESPONSE" | grep -o '"access_token":"[^"]*"' | cut -d'"' -f4)
if [ -n "$SECOND_TOKEN" ] && [ "$SECOND_TOKEN" != "null" ]; then
    echo -e "${GREEN}✅ Second user login successful${NC}"
else
    echo -e "${RED}❌ Second user login failed${NC}"
    exit 1
fi

RESPONSE=$(curl -s -X POST "${BASE_URL}/reviews/" \
    -H "Authorization: Bearer ${SECOND_TOKEN}" \
    -H "Content-Type: application/json" \
    -d "{\"text\": \"This is a test review\", \"rating\": 5, \"place_id\": \"${PLACE_ID}\"}")

REVIEW_ID=$(echo "$RESPONSE" | grep -o '"id":"[^"]*"' | cut -d'"' -f4)
if [ -n "$REVIEW_ID" ] && [ "$REVIEW_ID" != "null" ]; then
    print_response 201 "$RESPONSE"
    echo -e "${GREEN}✅ Review created successfully with ID: ${REVIEW_ID}${NC}"
else
    print_response 400 "$RESPONSE"
    echo -e "${RED}❌ Failed to create review${NC}"
fi

# 11. Test trying to review own place (should fail)
print_header "TRYING TO REVIEW OWN PLACE (SHOULD FAIL)"
echo "POST ${BASE_URL}/reviews/"
echo "Headers: {\"Authorization\": \"Bearer ...token truncated...\"}"
echo "Request: {\"text\": \"This is a review for my own place\", \"rating\": 5, \"place_id\": \"${PLACE_ID}\"}"

RESPONSE=$(curl -s -X POST "${BASE_URL}/reviews/" \
    -H "Authorization: Bearer ${TOKEN}" \
    -H "Content-Type: application/json" \
    -d "{\"text\": \"This is a review for my own place\", \"rating\": 5, \"place_id\": \"${PLACE_ID}\"}")

print_response 400 "$RESPONSE"
if [[ "$RESPONSE" == *"You cannot review your own place"* ]]; then
    echo -e "${GREEN}✅ Cannot review own place (expected)${NC}"
else
    echo -e "${RED}❌ Unexpected response${NC}"
fi

# 12. Test updating user profile (authenticated, self)
print_header "UPDATING USER PROFILE (AUTHENTICATED, SELF)"
echo "PUT ${BASE_URL}/users/${USER_ID}"
echo "Headers: {\"Authorization\": \"Bearer ...token truncated...\"}"
echo "Request: {\"first_name\": \"Updated\", \"last_name\": \"Name\"}"

RESPONSE=$(curl -s -X PUT "${BASE_URL}/users/${USER_ID}" \
    -H "Authorization: Bearer ${TOKEN}" \
    -H "Content-Type: application/json" \
    -d "{\"first_name\": \"Updated\", \"last_name\": \"Name\"}")

print_response 200 "$RESPONSE"
if [[ "$RESPONSE" == *"Updated"* ]] && [[ "$RESPONSE" == *"Name"* ]]; then
    echo -e "${GREEN}✅ User profile updated successfully${NC}"
else
    echo -e "${RED}❌ Failed to update user profile${NC}"
fi

# 13. Test trying to update another user's profile (should fail)
print_header "TRYING TO UPDATE ANOTHER USER'S PROFILE (SHOULD FAIL)"
echo "PUT ${BASE_URL}/users/${SECOND_USER_ID}"
echo "Headers: {\"Authorization\": \"Bearer ...token truncated...\"}"
echo "Request: {\"first_name\": \"Unauthorized\", \"last_name\": \"Update\"}"

RESPONSE=$(curl -s -X PUT "${BASE_URL}/users/${SECOND_USER_ID}" \
    -H "Authorization: Bearer ${TOKEN}" \
    -H "Content-Type: application/json" \
    -d "{\"first_name\": \"Unauthorized\", \"last_name\": \"Update\"}")

print_response 403 "$RESPONSE"
if [[ "$RESPONSE" == *"Unauthorized action"* ]]; then
    echo -e "${GREEN}✅ Unauthorized action (expected)${NC}"
else
    echo -e "${RED}❌ Unexpected response${NC}"
fi

# 14. Test trying to update email (should fail)
print_header "TRYING TO UPDATE EMAIL (SHOULD FAIL)"
echo "PUT ${BASE_URL}/users/${USER_ID}"
echo "Headers: {\"Authorization\": \"Bearer ...token truncated...\"}"
echo "Request: {\"email\": \"new.email@example.com\"}"

RESPONSE=$(curl -s -X PUT "${BASE_URL}/users/${USER_ID}" \
    -H "Authorization: Bearer ${TOKEN}" \
    -H "Content-Type: application/json" \
    -d "{\"email\": \"new.email@example.com\"}")

print_response 400 "$RESPONSE"
if [[ "$RESPONSE" == *"You cannot modify email or password"* ]]; then
    echo -e "${GREEN}✅ Cannot modify email (expected)${NC}"
else
    echo -e "${RED}❌ Unexpected response${NC}"
fi

print_header "ALL TESTS COMPLETED"
echo -e "${GREEN}✅ JWT authentication tests completed successfully${NC}"
