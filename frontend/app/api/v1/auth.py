from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from app.services import facade

api = Namespace('auth', description='Authentication operations')

# Model for input validation
login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})


@api.route('/login')
class Login(Resource):
    @api.expect(login_model)
    def post(self):
        """Authenticate user and return a JWT token"""
        credentials = api.payload  # Get the email and password from the request payload
        
        # Step 1: Retrieve the user based on the provided email
        user = facade.get_user_by_email(credentials['email'])
        
        # Step 2: Check if the user exists and the password is correct
        if not user or not user.verify_password(credentials['password']):
            return {'error': 'Invalid credentials'}, 401

        # Step 3: Create a JWT token with the user's id, role, and is_admin flag
        # Include the role and is_admin flag in the token's additional claims
        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={
                'role': user.role,
                'is_admin': user.is_admin
            }
        )
        
        # Step 4: Return the JWT token to the client
        return {'access_token': access_token}, 200


@api.route('/protected')
class ProtectedResource(Resource):
    @jwt_required()
    def get(self):
        """A protected endpoint that requires a valid JWT token"""
        current_user_id = get_jwt_identity()  # Retrieve the user's identity from the token
        claims = get_jwt()  # Get the JWT claims
        role = claims.get('role', 'unknown')
        is_admin = claims.get('is_admin', False)
        
        return {
            'message': f'Hello, user {current_user_id}',
            'role': role,
            'is_admin': is_admin
        }, 200
