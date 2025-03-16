# JWT Authentication Tests

This directory contains test scripts for testing the JWT authentication and authorization functionality of the HBnB API.

## Test Files

- `test_auth.py`: Tests the basic authentication flow (user creation, login, and accessing a protected endpoint).
- `test_jwt_places.py`: Tests JWT authentication for place endpoints.
- `test_jwt_reviews.py`: Tests JWT authentication for review endpoints.
- `test_jwt_users.py`: Tests JWT authentication for user endpoints.
- `test_jwt_amenities.py`: Tests JWT authentication for amenity endpoints.
- `run_jwt_tests.sh`: Shell script to run all JWT authentication tests.
- `curl_jwt_tests.sh`: Shell script to test JWT authentication using curl commands.
- `jwt_test_report.md`: Comprehensive report of JWT authentication implementation and test results.

## Running the Tests

### Prerequisites

1. Make sure the HBnB API server is running:
   ```bash
   cd part2
   python run.py
   ```

2. Install the required Python packages:
   ```bash
   pip install requests
   ```

### Running All Tests

To run all JWT authentication tests, use the provided shell script:

```bash
cd part2/tests
./run_jwt_tests.sh
```

This script will run each test file sequentially and prompt you to continue to the next test after each one completes.

### Running Tests with curl

To test the JWT authentication using curl commands, use the provided shell script:

```bash
cd part2/tests
./curl_jwt_tests.sh
```

This script will:
1. Create a test user
2. Login to get a JWT token
3. Test various endpoints with and without authentication
4. Verify that protected endpoints require authentication
5. Verify that users can only modify their own resources

Note: This script requires `jq` to be installed for JSON parsing. You can install it with:
```bash
sudo apt-get install jq  # For Debian/Ubuntu
# or
brew install jq  # For macOS
```

### Running Individual Tests

You can also run individual test files:

```bash
cd part2/tests
python test_auth.py
python test_jwt_places.py
python test_jwt_reviews.py
python test_jwt_users.py
python test_jwt_amenities.py
```

## What the Tests Verify

### Authentication Tests (`test_auth.py`)

- Creating a user
- Logging in to get a JWT token
- Accessing a protected endpoint with the JWT token

### Place Tests (`test_jwt_places.py`)

- Creating a place (authenticated)
- Creating a place without authentication (should fail)
- Updating a place (authenticated, owner)
- Updating a place that the user doesn't own (should fail)
- Getting all places (public)
- Getting a specific place (public)

### Review Tests (`test_jwt_reviews.py`)

- Creating a review (authenticated)
- Creating a review for a place the user owns (should fail)
- Creating a duplicate review for the same place (should fail)
- Updating a review (authenticated, owner)
- Updating a review that the user didn't create (should fail)
- Deleting a review (authenticated, owner)
- Deleting a review that the user didn't create (should fail)
- Getting all reviews (public)
- Getting a specific review (public)

### User Tests (`test_jwt_users.py`)

- Updating a user's profile (authenticated, self)
- Updating another user's profile (should fail)
- Updating a user's email (should fail)
- Updating a user's password (should fail)
- Getting all users (public)
- Getting a specific user (public)

### Amenity Tests (`test_jwt_amenities.py`)

- Creating an amenity (authenticated)
- Creating an amenity without authentication (should fail)
- Updating an amenity (authenticated)
- Updating an amenity without authentication (should fail)
- Getting all amenities (public)
- Getting a specific amenity (public)
