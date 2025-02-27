from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('places', description='Place operations')

# Define the models for related entities
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

# Define the review model for place details
review_model = api.model('PlaceReview', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)'),
    'user_id': fields.String(description='ID of the user')
})

# Define the place model for input validation and documentation
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(fields.String, description="List of amenities ID's"),
    'reviews': fields.List(fields.Nested(review_model), description='List of reviews')
})

# Define a model for place updates where fields are optional
place_update_model = api.model('PlaceUpdate', {
    'title': fields.String(required=False, description='Title of the place'),
    'description': fields.String(required=False, description='Description of the place'),
    'price': fields.Float(required=False, description='Price per night'),
    'latitude': fields.Float(required=False, description='Latitude of the place'),
    'longitude': fields.Float(required=False, description='Longitude of the place'),
    'owner_id': fields.String(required=False, description='ID of the owner'),
    'amenities': fields.List(fields.String, required=False, description="List of amenities ID's")
})

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model, validate=True)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new place"""
        try:
            new_place = facade.create_place(api.payload)
            return {
                'id': new_place.id,
                'title': new_place.title,
                'description': new_place.description,
                'price': new_place.price,
                'latitude': new_place.latitude,
                'longitude': new_place.longitude,
                'owner_id': new_place.owner_id
            }, 201
        except ValueError as e:
            api.abort(400, str(e))

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        places = facade.get_all_places()
        return [{
            'id': place.id,
            'title': place.title,
            'latitude': place.latitude,
            'longitude': place.longitude
        } for place in places], 200

@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        try:
            place = facade.get_place(place_id)
            owner = facade.get_user(place.owner_id)
            
            # Get reviews for this place
            reviews = []
            if hasattr(place, 'reviews'):
                reviews = [{
                    'id': review.id,
                    'text': review.text,
                    'rating': review.rating,
                    'user_id': review.user.id
                } for review in place.reviews]
            
            return {
                'id': place.id,
                'title': place.title,
                'description': place.description,
                'price': place.price,
                'latitude': place.latitude,
                'longitude': place.longitude,
                'owner': {
                    'id': owner.id,
                    'first_name': owner.first_name,
                    'last_name': owner.last_name,
                    'email': owner.email
                },
                'reviews': reviews
            }, 200
        except ValueError as e:
            api.abort(404, str(e))

    @api.expect(place_update_model, validate=True)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update a place's information"""
        try:
            # Check if place exists
            place = facade.get_place(place_id)
        except ValueError as e:
            api.abort(404, str(e))
            
        try:
            # Ensure api.payload is a dictionary
            if not isinstance(api.payload, dict):
                api.abort(400, 'Invalid payload: expected a dictionary')
            
            # Create a new dictionary with only the fields that are present in the payload
            update_data = {}
            for key, value in api.payload.items():
                if value is not None:
                    update_data[key] = value
            
            try:
                updated_place = facade.update_place(place_id, update_data)
                return {
                    'message': 'Place updated successfully',
                    'place': {
                        'id': updated_place.id,
                        'title': updated_place.title,
                        'description': updated_place.description,
                        'price': updated_place.price,
                        'latitude': updated_place.latitude,
                        'longitude': updated_place.longitude,
                        'owner_id': updated_place.owner_id
                    }
                }, 200
            except ValueError as e:
                api.abort(400, str(e))
        except Exception as e:
            api.abort(400, str(e))

@api.route('/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        try:
            reviews = facade.get_reviews_by_place(place_id)
            return [{
                'id': review.id,
                'text': review.text,
                'rating': review.rating,
                'user': {
                    'id': review.user.id,
                    'first_name': review.user.first_name,
                    'last_name': review.user.last_name
                }
            } for review in reviews], 200
        except ValueError as e:
            api.abort(404, str(e))
