from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review

class HBnBFacade:
    def __init__(self):
        self.repository = InMemoryRepository()

    def create_user(self, user_data):
        # Ensure all required fields are present
        required_fields = ['first_name', 'last_name', 'email', 'password']
        for field in required_fields:
            if field not in user_data:
                raise ValueError(f"Missing required field: {field}")
        
        user = User(**user_data)
        self.repository.add(user)
        return user

    def get_user(self, user_id):
        return self.repository.get(user_id)

    def get_user_by_email(self, email):
        return next((u for u in self.repository.get_all() if isinstance(u, User) and u.email == email), None)

    def get_all_users(self):
        return [u for u in self.repository.get_all() if isinstance(u, User)]

    def update_user(self, user_id, user_data):
        user = self.repository.get(user_id)
        if user and isinstance(user, User):
            user.update(user_data)
            self.repository.update(user_id, user)
        return user

    def create_amenity(self, amenity_data):
        if 'name' not in amenity_data or not amenity_data['name']:
            raise ValueError("Amenity name is required")
        amenity = Amenity(**amenity_data)
        self.repository.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        amenity = self.repository.get(amenity_id)
        if not amenity or not isinstance(amenity, Amenity):
            raise ValueError(f"Amenity with id {amenity_id} not found")
        return amenity

    def get_all_amenities(self):
        return [a for a in self.repository.get_all() if isinstance(a, Amenity)]

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.repository.get(amenity_id)
        if amenity and isinstance(amenity, Amenity):
            if 'name' not in amenity_data or not amenity_data['name']:
                raise ValueError("Amenity name is required")
            amenity.update(amenity_data)
            self.repository.update(amenity_id, amenity)
        return amenity

    # Removed duplicate create_place method

    def get_place(self, place_id):
        place = self.repository.get(place_id)
        if not place or not isinstance(place, Place):
            raise ValueError(f"Place with id {place_id} not found")
        return place

    def create_place(self, place_data):
        # Validate required fields
        required_fields = ['title', 'price', 'latitude', 'longitude', 'owner_id']
        for field in required_fields:
            if field not in place_data:
                raise ValueError(f"Missing required field: {field}")

        # Validate price, latitude, and longitude
        if float(place_data['price']) < 0:
            raise ValueError("Price must be non-negative")
        if not -90 <= float(place_data['latitude']) <= 90:
            raise ValueError("Latitude must be between -90 and 90")
        if not -180 <= float(place_data['longitude']) <= 180:
            raise ValueError("Longitude must be between -180 and 180")

        # Check if owner exists
        owner = self.repository.get(place_data['owner_id'])
        if not owner or not isinstance(owner, User):
            raise ValueError(f"Owner with id {place_data['owner_id']} not found")

        place = Place(
            title=place_data['title'],
            description=place_data.get('description'),
            price=float(place_data['price']),
            latitude=float(place_data['latitude']),
            longitude=float(place_data['longitude']),
            owner_id=place_data['owner_id']
        )
        self.repository.add(place)
        return place

    def get_place(self, place_id):
        place = self.repository.get(place_id)
        if not place or not isinstance(place, Place):
            raise ValueError(f"Place with id {place_id} not found")
        return place

    def get_all_places(self):
        return [p for p in self.repository.get_all() if isinstance(p, Place)]

    def update_place(self, place_id, place_data):
        place = self.repository.get(place_id)
        if not place or not isinstance(place, Place):
            raise ValueError(f"Place with id {place_id} not found")

        # Ensure place_data is a dictionary
        if not isinstance(place_data, dict):
            raise ValueError(f"Invalid input: expected a dictionary, got {type(place_data)}")

        # Update the place attributes
        for key, value in place_data.items():
            if hasattr(place, key):
                setattr(place, key, value)
            elif key == 'title':
                place.title = value
            elif key == 'description':
                place.description = value
            elif key == 'price':
                place.price = float(value)
            elif key == 'latitude':
                place.latitude = float(value)
            elif key == 'longitude':
                place.longitude = float(value)
            elif key == 'owner_id':
                place.owner_id = value

        # Update the place in the repository
        place.save()  # Update the updated_at timestamp
        self.repository.update(place_id, place)
        return place
        
    def create_review(self, review_data):
        """
        Create a new review.
        
        :param review_data: Dictionary containing review data
        :return: The created review object
        """
        # Validate required fields
        required_fields = ['text', 'rating', 'user_id', 'place_id']
        for field in required_fields:
            if field not in review_data:
                raise ValueError(f"Missing required field: {field}")
        
        # Validate rating
        try:
            rating = int(review_data['rating'])
            if not 1 <= rating <= 5:
                raise ValueError("Rating must be between 1 and 5")
        except (ValueError, TypeError):
            raise ValueError("Rating must be an integer between 1 and 5")
        
        # Check if user exists
        user = self.repository.get(review_data['user_id'])
        if not user or not isinstance(user, User):
            raise ValueError(f"User with id {review_data['user_id']} not found")
        
        # Check if place exists
        place = self.repository.get(review_data['place_id'])
        if not place or not isinstance(place, Place):
            raise ValueError(f"Place with id {review_data['place_id']} not found")
        
        # Create the review
        review = Review(
            text=review_data['text'],
            rating=rating,
            place=place,
            user=user
        )
        
        # Add the review to the repository
        self.repository.add(review)
        
        # Add the review to the place's reviews list
        place.add_review(review)
        self.repository.update(place.id, place)
        
        return review
    
    def get_review(self, review_id):
        """
        Get a review by ID.
        
        :param review_id: ID of the review to retrieve
        :return: The review object if found
        """
        review = self.repository.get(review_id)
        if not review or not isinstance(review, Review):
            raise ValueError(f"Review with id {review_id} not found")
        return review
    
    def get_all_reviews(self):
        """
        Get all reviews.
        
        :return: List of all review objects
        """
        return [r for r in self.repository.get_all() if isinstance(r, Review)]
    
    def get_reviews_by_place(self, place_id):
        """
        Get all reviews for a specific place.
        
        :param place_id: ID of the place to get reviews for
        :return: List of review objects for the place
        """
        # Check if place exists
        place = self.repository.get(place_id)
        if not place or not isinstance(place, Place):
            raise ValueError(f"Place with id {place_id} not found")
        
        # Return all reviews for the place
        return [r for r in self.repository.get_all() 
                if isinstance(r, Review) and r.place.id == place_id]
    
    def update_review(self, review_id, review_data):
        """
        Update a review.
        
        :param review_id: ID of the review to update
        :param review_data: Dictionary containing updated review data
        :return: The updated review object
        """
        # Check if review exists
        review = self.repository.get(review_id)
        if not review or not isinstance(review, Review):
            raise ValueError(f"Review with id {review_id} not found")
        
        # Update the review attributes
        if 'text' in review_data:
            review.text = review_data['text']
        
        if 'rating' in review_data:
            try:
                rating = int(review_data['rating'])
                if not 1 <= rating <= 5:
                    raise ValueError("Rating must be between 1 and 5")
                review.rating = rating
            except (ValueError, TypeError):
                raise ValueError("Rating must be an integer between 1 and 5")
        
        # Update the review in the repository
        review.save()  # Update the updated_at timestamp
        self.repository.update(review_id, review)
        
        return review
    
    def delete_review(self, review_id):
        """
        Delete a review.
        
        :param review_id: ID of the review to delete
        :return: True if successful, False otherwise
        """
        # Check if review exists
        review = self.repository.get(review_id)
        if not review or not isinstance(review, Review):
            raise ValueError(f"Review with id {review_id} not found")
        
        # Remove the review from the place's reviews list
        place = review.place
        if place and hasattr(place, 'reviews'):
            place.reviews = [r for r in place.reviews if r.id != review_id]
            self.repository.update(place.id, place)
        
        # Delete the review from the repository
        self.repository.delete(review_id)
        
        return True

facade = HBnBFacade()
