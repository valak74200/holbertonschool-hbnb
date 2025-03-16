#!/bin/bash

# Script to run all JWT authentication tests

# Set colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print section headers
print_header() {
    echo -e "\n${YELLOW}========================================================================"
    echo -e "                         $1                         "
    echo -e "========================================================================${NC}\n"
}

# Function to run a test and check its exit status
run_test() {
    print_header "RUNNING $1"
    python "$1"
    if [ $? -eq 0 ]; then
        echo -e "\n${GREEN}✅ $1 completed successfully${NC}"
    else
        echo -e "\n${RED}❌ $1 failed${NC}"
    fi
    echo -e "\n${YELLOW}Press Enter to continue to the next test...${NC}"
    read
}

# Make sure we're in the right directory
cd "$(dirname "$0")"

# Run the tests
print_header "JWT AUTHENTICATION TESTS"

# Test authentication
run_test test_auth.py

# Test places endpoints
run_test test_jwt_places.py

# Test reviews endpoints
run_test test_jwt_reviews.py

# Test users endpoints
run_test test_jwt_users.py

# Test amenities endpoints
run_test test_jwt_amenities.py

print_header "ALL TESTS COMPLETED"
