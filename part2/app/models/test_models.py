"""
Ce fichier contient des tests unitaires pour les modèles de l'application.
"""

from .user import User
from .place import Place
from .review import Review
from .amenity import Amenity

def test_user_creation():
    """Test la création d'un utilisateur."""
    user = User(first_name="John", last_name="Doe", email="john.doe@example.com")
    assert user.first_name == "John"
    assert user.last_name == "Doe"
    assert user.email == "john.doe@example.com"
    assert user.is_admin is False  # Valeur par défaut
    assert user.id is not None
    assert user.created_at is not None
    assert user.updated_at is not None
    print("Test de création d'utilisateur réussi!")

def test_place_creation():
    """Test la création d'un lieu et ses relations."""
    owner = User(first_name="Alice", last_name="Smith", email="alice.smith@example.com")
    place = Place(title="Appartement Cosy", description="Un endroit agréable pour séjourner", price=100, latitude=37.7749, longitude=-122.4194, owner=owner)
    assert place.title == "Appartement Cosy"
    assert place.price == 100
    assert place.owner == owner
    assert len(place.reviews) == 0
    assert len(place.amenities) == 0
    assert place.id is not None
    assert place.created_at is not None
    assert place.updated_at is not None
    print("Test de création de lieu réussi!")

def test_review_creation():
    """Test la création d'un avis."""
    user = User(first_name="Bob", last_name="Johnson", email="bob.johnson@example.com")
    owner = User(first_name="Alice", last_name="Smith", email="alice.smith@example.com")
    place = Place(title="Appartement Cosy", description="Un endroit agréable pour séjourner", price=100, latitude=37.7749, longitude=-122.4194, owner=owner)
    review = Review(text="Excellent séjour!", rating=5, place=place, user=user)
    assert review.text == "Excellent séjour!"
    assert review.rating == 5
    assert review.place == place
    assert review.user == user
    assert review.id is not None
    assert review.created_at is not None
    assert review.updated_at is not None
    print("Test de création d'avis réussi!")

def test_amenity_creation():
    """Test la création d'un équipement."""
    amenity = Amenity(name="Wi-Fi")
    assert amenity.name == "Wi-Fi"
    assert amenity.id is not None
    assert amenity.created_at is not None
    assert amenity.updated_at is not None
    print("Test de création d'équipement réussi!")

def test_relationships():
    """Test les relations entre les différents modèles."""
    owner = User(first_name="Alice", last_name="Smith", email="alice.smith@example.com")
    user = User(first_name="Bob", last_name="Johnson", email="bob.johnson@example.com")
    place = Place(title="Appartement Cosy", description="Un endroit agréable pour séjourner", price=100, latitude=37.7749, longitude=-122.4194, owner=owner)
    review = Review(text="Excellent séjour!", rating=5, place=place, user=user)
    amenity = Amenity(name="Wi-Fi")

    place.add_review(review)
    place.add_amenity(amenity)

    assert len(place.reviews) == 1
    assert place.reviews[0] == review
    assert len(place.amenities) == 1
    assert place.amenities[0] == amenity
    print("Test des relations réussi!")

if __name__ == "__main__":
    test_user_creation()
    test_place_creation()
    test_review_creation()
    test_amenity_creation()
    test_relationships()
    print("Tous les tests ont réussi!")
