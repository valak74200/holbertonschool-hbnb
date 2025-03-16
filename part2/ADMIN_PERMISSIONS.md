# Administrator Permissions

This document describes the administrator permissions implemented in the HBnB API.

## Overview

Administrators have special privileges that allow them to perform actions that regular users cannot. These privileges include:

1. Creating and modifying users
2. Creating and modifying amenities
3. Modifying or deleting any place or review, bypassing the ownership restrictions that regular users face

## Admin Endpoints

The following endpoints are specifically for administrators:

- `POST /api/v1/admin/users`: Create a new user.
- `PUT /api/v1/admin/users/<user_id>`: Modify a user's details, including email and password.
- `POST /api/v1/admin/amenities`: Add a new amenity.
- `PUT /api/v1/admin/amenities/<amenity_id>`: Modify the details of an amenity.

## Restricted Endpoints

The following endpoints are also restricted to administrators only:

- `POST /api/v1/users/`: Create a new user. The email must be unique.
- `PUT /api/v1/users/<user_id>`: Modify a user's details, including email and password. The email must not be duplicated.
- `POST /api/v1/amenities/`: Add a new amenity.
- `PUT /api/v1/amenities/<amenity_id>`: Modify the details of an amenity.

## Bypass Ownership Restrictions

Administrators can also:

- Modify or delete any place, even if they are not the owner.
- Modify or delete any review, even if they are not the author.

Example for Modifying a Place (PUT /api/v1/places/<place_id>):

```python
@api.route('/places/<place_id>')
class PlaceResource(Resource):
    @jwt_required()
    def put(self, place_id):
        # Récupère l'identité de l'utilisateur à partir du token JWT
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)
        
        # Vérifie si le lieu existe
        place = facade.get_place(place_id)
        
        # Vérifie si l'utilisateur authentifié est le propriétaire du lieu ou un administrateur
        if place.owner_id != current_user_id and not is_admin:
            api.abort(403, 'Unauthorized action')
        
        # Logic to update the place
        # ...
```

Example for Modifying a Review (PUT /api/v1/reviews/<review_id>):

```python
@api.route('/reviews/<review_id>')
class ReviewResource(Resource):
    @jwt_required()
    def put(self, review_id):
        # Récupère l'identité de l'utilisateur à partir du token JWT
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)
        
        # Vérifie si l'avis existe
        review = facade.get_review(review_id)
        
        # Vérifie si l'utilisateur authentifié est l'auteur de l'avis ou un administrateur
        if review.user.id != current_user_id and not is_admin:
            api.abort(403, 'Unauthorized action')
        
        # Logic to update the review
        # ...
```

## Implementation Details

### User Model

The `User` model includes an `is_admin` field that is set to `False` by default:

```python
def __init__(self, first_name: str, last_name: str, email: str, 
             password: str, is_admin: bool = False):
    """
    Initialise un nouvel utilisateur.

    :param first_name: Prénom de l'utilisateur
    :param last_name: Nom de famille de l'utilisateur
    :param email: Adresse email de l'utilisateur
    :param password: Mot de passe de l'utilisateur
    :param is_admin: Indique si l'utilisateur est un administrateur (par défaut False)
    """
    super().__init__()
    self.first_name = first_name
    self.last_name = last_name
    self.email = email
    self.hash_password(password)
    self.is_admin = is_admin
```

### JWT Token

The JWT token includes the `is_admin` flag in the additional claims:

```python
access_token = create_access_token(
    identity=str(user.id),
    additional_claims={'is_admin': user.is_admin}
)
```

### Role-Based Access Control (RBAC)

The API uses Role-Based Access Control (RBAC) to restrict access to certain endpoints. There are two approaches implemented:

1. **Admin Required Decorator**: A decorator that checks if the user is an admin before allowing access to the endpoint.

```python
def admin_required():
    """
    A decorator to check if the user is an admin.
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            # Verify that the JWT is present and valid
            verify_jwt_in_request()
            
            # Get the JWT claims, which include the is_admin flag
            claims = get_jwt()
            
            # Check if the user is an admin
            if not claims.get('is_admin', False):
                return {'message': 'Admin privileges required'}, 403
            
            # If the user is an admin, call the original function
            return fn(*args, **kwargs)
        return decorator
    return wrapper
```

2. **In-Function RBAC**: Checking the user's role within the endpoint function.

```python
@api.route('/amenities/')
class AmenityList(Resource):
    @jwt_required()
    def post(self):
        # Récupère l'identité de l'utilisateur à partir du token JWT
        current_user_id = get_jwt_identity()
        
        # Vérifie si l'utilisateur est un administrateur
        claims = get_jwt()
        if not claims.get('is_admin', False):
            return {'message': 'Admin privileges required'}, 403
        
        # Logic to create a new amenity
        # ...
```

### Making a User an Admin

To make a user an admin, you can use the `make_admin.py` script:

```bash
cd part2
python scripts/make_admin.py <email>
```

This script will update the user with the given email to be an admin.

### Testing Administrator Permissions

To test the administrator permissions, you can use the following scripts:

1. **Using Python**:

```bash
cd part2
python tests/test_admin_permissions.py
```

This script will create an admin user and a regular user, and then test the administrator permissions by attempting to perform various actions as both users.

2. **Using cURL**:

```bash
cd part2
./tests/curl_admin_tests.sh
```

This script provides examples of how to test the administrator permissions using cURL commands. It includes tests for:

- Creating a user as an admin:
```bash
curl -X POST "http://127.0.0.1:5000/api/v1/users/" \
  -d '{"email": "newuser@example.com", "first_name": "Admin", "last_name": "User", "password": "password123"}' \
  -H "Authorization: Bearer <admin_token>" \
  -H "Content-Type: application/json"
```

- Creating an amenity as an admin
- Updating a place as an admin (not the owner)
- Updating a review as an admin (not the author)
- Deleting a review as an admin (not the author)

The script also tests that regular users cannot perform these actions.

## Security Considerations

- Administrator privileges should be granted only to trusted users.
- The `is_admin` flag is included in the JWT token, so it's important to keep the token secure.
- The JWT token is signed with a secret key, so it cannot be tampered with.
- The `admin_required` decorator checks the `is_admin` flag in the JWT token, so it's not possible to bypass the check by modifying the request.
