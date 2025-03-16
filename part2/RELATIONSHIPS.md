# Database Relationships in HBNB

This document explains the different types of relationships between models in the HBNB application.

## One-to-Many Relationships

In a one-to-many relationship, one record in a table can have many associated records in another table. For example, a user may place many orders, but each order is associated with one user.

### User to Place

A user can own many places, but each place has only one owner. Additionally, a user can be associated with many places.

```python
# In Place model
_owner_id = db.Column('owner_id', db.String(36), db.ForeignKey('users.id'), nullable=False)
user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

# Define the one-to-many relationship with User (owner)
owner = db.relationship('User', backref=db.backref('owned_places', lazy=True), foreign_keys=[_owner_id])

# Define the one-to-many relationship with User
user = db.relationship('User', backref=db.backref('places', lazy=True), foreign_keys=[user_id])
```

With these relationships:
- Each Place has an `owner` attribute that references the User who owns it
- Each User has an `owned_places` attribute (via backref) that contains a list of all Places they own
- Each Place has a `user` attribute that references the User associated with it
- Each User has a `places` attribute (via backref) that contains a list of all Places they are associated with
- The `foreign_keys` parameter specifies which column in the Place model references the User for each relationship

### User to Review

A user can write many reviews, but each review is written by only one user.

```python
# In Review model
user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
_user = db.relationship('User', backref=db.backref('reviews', lazy=True))
```

The `backref` argument in the relationship creates a bidirectional link, so you can access all reviews of a user using `user.reviews`.

### Place to Review

A place can have many reviews, but each review is for only one place.

```python
# In Review model
place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)
_place = db.relationship('Place', foreign_keys=[place_id])

# In Place model
reviews = db.relationship('Review', backref='place_obj', lazy=True, foreign_keys='Review.place_id')
```

With this relationship:
- Each Review has a `place` attribute that references the Place it's about
- Each Place has a `reviews` attribute that contains a list of all Reviews for that Place
- The relationship is defined in both models for clarity and to ensure proper bidirectional navigation

## Many-to-Many Relationships

In a many-to-many relationship, records in both tables can have multiple associations with records in the other table. For example, a student can enroll in many courses, and a course can have many students.

### Place to Amenity

A place can have many amenities, and an amenity can be associated with many places.

```python
# Association table
place_amenity = db.Table('place_amenity',
    db.Column('place_id', db.String(36), db.ForeignKey('places.id'), primary_key=True),
    db.Column('amenity_id', db.String(36), db.ForeignKey('amenities.id'), primary_key=True)
)

# In Place model
amenities = db.relationship('Amenity', secondary=place_amenity, 
                           backref=db.backref('places', lazy=True),
                           lazy='subquery')
```

The `secondary` argument specifies the association table to use for the many-to-many relationship. The `backref` creates a bidirectional relationship, allowing you to access all places that have a specific amenity using `amenity.places`.

With this relationship:
- Each Place has an `amenities` attribute that contains a list of all Amenities associated with it
- Each Amenity has a `places` attribute (via backref) that contains a list of all Places that have that Amenity
- The association table `place_amenity` stores the relationships between places and amenities

## Lazy Loading Options

SQLAlchemy provides several options for controlling how related objects are loaded:

- `lazy='select'` (default): Related objects are loaded when first accessed.
- `lazy='joined'`: Related objects are loaded in the same query as the parent.
- `lazy='subquery'`: Related objects are loaded in a separate query.
- `lazy='dynamic'`: Returns a query object that can be further refined.
- `lazy=True`: Synonym for 'select'.

In our application, we use `lazy=True` for most relationships, which means related objects are loaded when first accessed. For the many-to-many relationship between Place and Amenity, we use `lazy='subquery'` for better performance when loading a place with many amenities.

## Usage Examples

### One-to-Many: User to Places

```python
# Get all places owned by a user
user = User.query.get(user_id)
user_places = user.places

# Get the owner of a place
place = Place.query.get(place_id)
owner = place.owner
```

### One-to-Many: Place to Reviews

```python
# Get all reviews for a place
place = Place.query.get(place_id)
place_reviews = place.reviews

# Get the place a review is for
review = Review.query.get(review_id)
reviewed_place = review.place
```

### Many-to-Many: Place to Amenities

```python
# Get all amenities for a place
place = Place.query.get(place_id)
place_amenities = place.amenities

# Get all places with a specific amenity
amenity = Amenity.query.get(amenity_id)
places_with_amenity = amenity.places

# Add an amenity to a place
place.amenities.append(amenity)
db.session.commit()
```
